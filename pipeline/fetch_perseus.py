#!/usr/bin/env python3
"""Fetch the Perseus TEI texts named in a shelf's "perseus" section.

    python3 pipeline/fetch_perseus.py <shelf>          # from canon-corpus root
    python3 pipeline/fetch_perseus.py <shelf> --verify # re-check files on disk
    python3 pipeline/fetch_perseus.py <shelf> --verify --record  # and commit the findings
    python3 pipeline/fetch_perseus.py <shelf> --record  # fetch, then commit this run's findings
Writes data/corpus/<shelf>/<slug>.xml and <shelf>_perseus_report.json.

A separate file on purpose: fetch_shelf.py ignores the "perseus" key, so a
shelf that gains one fetches exactly as before there (relay RULES 2a).

Shelf rows:  "perseus": {slug: [cts_tail, title, translator, rights_note]}
  cts_tail   e.g. "tlg0014.tlg020.perseus-eng2" (the URN after urn:cts:<ns>:)
  title      the work, for the report
  translator the translator's name as the shelf records it; the SURNAME must
             appear in the file's header or the file is refused (identity)
  rights_note a human line: why the translation is public domain
The repository is chosen from the id: tlg + "1st1K" -> OpenGreekAndLatin/
First1KGreek; other tlg -> PerseusDL/canonical-greekLit; phi/stoa ->
PerseusDL/canonical-latinLit. Files are read from raw.githubusercontent.com
(jsDelivr as a fallback), the only routes that reach GitHub from a sandbox.

Rights gate. The TRANSLATION's date comes from the file's own sourceDesc: the
latest year printed there is recorded, and a year of 1930 or later is
refused unless the shelf's `_rights_checked` ({slug: reason}) says why it is
safe. That is fail-closed and matches fetch_shelf.py's Internet Archive gate:
1930 itself is US public domain from 2026-01-01, but a person states it. A sourceDesc
with no year at all is refused the same way: nothing was checked. The MARKUP is
Perseus's and is licensed separately: the licence stated in the file is
recorded, else the repository's README statement (CC BY-SA 4.0 for both
canonical repos). That licence travels with the file in the report, so a
consumer sees "attribution + share-alike" without opening it.
Identity, as fetch_shelf.py does it since the 2026-10-02 review (optional
keys, all backward compatible): `_surname` (the author's names) must appear
as a whole word in the file's header, or the item's own `_surname_by_slug`
entry on a shelf of several authors; `_translators` ({slug: surname}), when
it names the item, replaces the surname taken from the row; names match as
whole words, never substrings; `_identity_checked` ({slug: reason}) keeps a
would-be MISMATCH that a person confirmed. `--verify --record` writes
"_perseus_checks" into the shelf (committed: findings only, no text), so the
evidence outlives the gitignored report; fetch_shelf.py's "_checks" covers
the other kinds and does not see Perseus rows.
Resumable: a file already on disk is kept. A failed fetch is reported, never
written as an empty file.
"""
import json, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}
PD_CUTOFF = 1930  # this year and later need a `_rights_checked` reason (as fetch_shelf.py's IA gate)
REPO_LICENCE = {
    "PerseusDL/canonical-greekLit": "CC BY-SA 4.0 (repository README: Perseus Digital Library markup)",
    "PerseusDL/canonical-latinLit": "CC BY-SA 4.0 (repository README: Perseus Digital Library markup)",
    "OpenGreekAndLatin/First1KGreek": "see licence in file (First1KGreek states it per file)",
}

def repo_for(tail):
    if tail.startswith("tlg") and ".1st1K-" in tail:
        return "OpenGreekAndLatin/First1KGreek"
    if tail.startswith("tlg"):
        return "PerseusDL/canonical-greekLit"
    if tail.startswith(("phi", "stoa")):
        return "PerseusDL/canonical-latinLit"
    raise ValueError(f"no repository known for {tail}")

def urls_for(tail):
    """(repo, urls). A 1st1K id is tried in canonical-greekLit first: some
    First1KGreek translations (Thucydides 1st1K-eng1/2) live there."""
    a, b = tail.split(".")[:2]
    path = f"data/{a}/{b}/{tail}.xml"
    repo = repo_for(tail)
    repos = (["PerseusDL/canonical-greekLit", repo]
             if repo == "OpenGreekAndLatin/First1KGreek" else [repo])
    return repos, [u for r in repos for u in
                   (f"https://raw.githubusercontent.com/{r}/master/{path}",
                    f"https://cdn.jsdelivr.net/gh/{r}@master/{path}")]

def get(urls, tries=3):
    err = None
    for url in urls:
        for i in range(tries):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                    return r.read(), url
            except Exception as e:
                err = e
                if getattr(e, "code", None) == 404:
                    break
                time.sleep(2 ** i)
    raise RuntimeError(f"{urls[0]}: {err}")

def _pat(phrase):
    """A name as whole words (same rule as fetch_shelf.py): spaces match runs
    of spaces or hyphens, an apostrophe is optional."""
    words = [re.escape(w).replace("'", "['\u2019\u2018`]?") for w in phrase.lower().split()]
    return re.compile(r"(?<![a-z])" + r"[\s\-]+".join(words) + r"(?![a-z])")

def check(data, tail, translator, slug, shelf):
    """Identity + rights. Returns the report fields; raises to refuse. An
    identity miss is kept only when `_identity_checked` names the slug; the
    rights gate runs either way and is never overridden here."""
    r, misses = _check(data, tail, translator, slug, shelf)
    if misses:
        why = shelf.get("_identity_checked", {}).get(slug)
        if not why:
            raise RuntimeError(misses[0])
        r["identity_override"] = f"{'; '.join(misses)} -- kept: {why}"
    return r

def _check(data, tail, translator, slug, shelf):
    text = data.decode("utf-8", "replace")
    if "<TEI" not in text[:5000]:
        raise RuntimeError("not a TEI file")
    head = text[:text.find("</teiHeader>")] if "</teiHeader>" in text else text[:20000]
    head_l = head.lower()
    r, misses = {"urn_in_file": tail in text}, []
    surnames = shelf.get("_surname_by_slug", {}).get(slug) or shelf.get("_surname")
    if surnames:
        r["author_seen"] = next((n for n in surnames if _pat(n).search(head_l)), None)
        if not r["author_seen"]:
            misses.append(f"MISMATCH: surname {surnames} never appears as a word in the file's header")
    # "Vince, J. H." -> Vince; "J. H. Vince" -> Vince; "W. R. M. Lamb (ed.)" -> Lamb
    who = re.sub(r"\(.*?\)", "", translator or "").split(" and ")[0].strip()
    sn = who.split(",")[0].strip() if "," in who else (who.split() or [""])[-1]
    if who in ("", "?") or who.lower().startswith(("unnamed", "anonymous")):
        sn = ""  # nothing to check against; flagged, not refused
        r["translator_unchecked"] = True
    sn = shelf.get("_translators", {}).get(slug) or sn
    r["translator_checked"] = sn
    if sn and not _pat(sn).search(head_l):
        misses.append(f"MISMATCH: translator '{sn}' not in the file's header")
    # "</sourceDesc" may close on the next line (Plato's Laws, tlg0059.tlg034)
    src = re.search(r"<sourceDesc.*?</sourceDesc\s*>", head, re.S)
    # tags stripped first: years inside attributes (archive.org ids such as
    # in.ernet.dli.2015.12682) are not printing dates
    src_text = re.sub(r"<[^>]+>", " ", src.group(0)) if src else ""
    years = [int(y) for y in re.findall(r"\b(1[5-9]\d\d|20\d\d)\b", src_text)]
    r["source_years"] = sorted(set(years))
    lic = re.search(r'<licen[cs]e[^>]*target="([^"]+)"', head) or re.search(r"<licen[cs]e[^>]*>(.*?)</licen", head, re.S)
    r["markup_licence_in_file"] = lic.group(1).strip() if lic else None
    late = [y for y in years if y >= PD_CUTOFF]
    if late:
        why = shelf.get("_rights_checked", {}).get(slug)
        if not why:
            raise RuntimeError(f"RIGHTS: source year {max(late)} is {PD_CUTOFF} or later; add _rights_checked to keep")
        r["rights_override"] = why
    if not years:
        # no printing date to check: refused unless a person dated it another way
        why = shelf.get("_rights_checked", {}).get(slug)
        if not why:
            raise RuntimeError("RIGHTS: no year in sourceDesc; add _rights_checked to keep")
        r["rights_flag"] = "no year in sourceDesc"
        r["rights_override"] = why
    return r, misses

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: fetch_perseus.py <shelf> [--verify]   (reads pipeline/<shelf>_shelf.json)")
    name = sys.argv[1]
    shelf = json.load(open(os.path.join(HERE, f"{name}_shelf.json"), encoding="utf-8"))
    rows = shelf.get("perseus", {})
    others = set(shelf.get("ccel", {}))  # ccel rows also land as <slug>.xml
    clash = others & set(rows)
    if clash:
        sys.exit(f"perseus slugs collide with ccel slugs: {sorted(clash)}")
    out = os.path.join(ROOT, "data", "corpus", name)
    os.makedirs(out, exist_ok=True)
    rep_path = os.path.join(out, f"{name}_perseus_report.json")
    report = json.load(open(rep_path)) if os.path.exists(rep_path) else {}
    verify = "--verify" in sys.argv[2:]
    seen = set()  # the rows this run actually checked: only these are recorded
    for slug, row in rows.items():
        tail, title, translator, note = (list(row) + [None] * 4)[:4]
        repos, urls = urls_for(tail)
        repo = repos[0]
        dest = os.path.join(out, slug + ".xml")
        base = {"urn": f"urn:cts:{'greekLit' if tail.startswith('tlg') else 'latinLit'}:{tail}",
                "repo": repo, "title": title, "translator": translator, "rights_note": note,
                "markup_licence_repo": REPO_LICENCE[repo]}
        try:
            if os.path.exists(dest) and os.path.getsize(dest) > 2000:
                data, url = open(dest, "rb").read(), urls[0]
                r = {**base, **check(data, tail, translator, slug, shelf),
                     "status": "kept", "bytes": len(data), "url": url}
            elif verify:
                continue
            else:
                data, url = get(urls)
                repo = next(r for r in repos if r in url)
                base["repo"], base["markup_licence_repo"] = repo, REPO_LICENCE[repo]
                if len(data) < 2000:
                    raise RuntimeError(f"only {len(data)} bytes")
                r = {**base, **check(data, tail, translator, slug, shelf),
                     "status": "fetched", "bytes": len(data), "url": url}
                open(dest + ".tmp", "wb").write(data)
                os.replace(dest + ".tmp", dest)
                time.sleep(0.5)
        except Exception as e:
            r = {**base, "status": "FAILED", "error": str(e), "url": urls[0]}
        report[slug] = r
        seen.add(slug)
        print(slug, r["status"], r.get("bytes", r.get("error", "")), flush=True)
        if not verify:
            json.dump(report, open(rep_path + ".tmp", "w"), indent=1)
            os.replace(rep_path + ".tmp", rep_path)
    bad = [s for s in rows if s in seen and report[s]["status"] == "FAILED"]
    print(f"{len(rows)} perseus items, {len(bad)} failed: {bad}")
    if "--record" in sys.argv[2:] and rows:
        if len(seen) < len(rows):
            print(f"not recorded (no local file, not checked this run): {sorted(set(rows) - seen)}")
        record(name, {s: report[s] for s in rows if s in seen})

RECORD_KEYS = ("urn", "repo", "translator_checked", "translator_unchecked", "author_seen",
               "source_years", "rights_flag", "rights_override", "markup_licence_in_file",
               "markup_licence_repo", "identity_override", "status", "error")

def outcome(r):
    """What a row's check came to, from the error's own prefix: a refusal on
    identity is not a refusal on rights, and neither is a network failure."""
    if r["status"] != "FAILED":
        return "identity_override" if r.get("identity_override") else "ok"
    err = r.get("error", "")
    return ("MISMATCH" if err.startswith("MISMATCH") else
            "RIGHTS refused" if err.startswith("RIGHTS") else "not checked: fetch error")

def record(name, found):
    """Commit the findings of THIS run into the shelf as "_perseus_checks" (no
    body text), keeping the shelf file's own indent. Rows the run did not
    check (no local file under --verify) are left out, never copied from an
    old report."""
    path = os.path.join(HERE, f"{name}_shelf.json")
    raw = open(path, encoding="utf-8").read()
    second = raw.split("\n")[1] if "\n" in raw else ""
    indent = (len(second) - len(second.lstrip())) or 1
    shelf = json.loads(raw)
    day = time.strftime("%Y-%m-%d")
    shelf["_perseus_checks"] = {
        s: {"checked": day, "identity": outcome(r),
            **{k: r[k] for k in RECORD_KEYS if k in r and r[k] not in (None, [])}}
        for s, r in found.items()}
    open(path + ".tmp", "w", encoding="utf-8").write(json.dumps(shelf, indent=indent, ensure_ascii=False) + "\n")
    os.replace(path + ".tmp", path)
    print(f"recorded _perseus_checks for {len(found)} items in {name}_shelf.json")

if __name__ == "__main__":
    main()
