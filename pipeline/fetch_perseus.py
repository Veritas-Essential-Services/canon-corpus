#!/usr/bin/env python3
"""Fetch the Perseus TEI texts named in a shelf's "perseus" section.

    python3 pipeline/fetch_perseus.py <shelf>          # from canon-corpus root
    python3 pipeline/fetch_perseus.py <shelf> --verify # re-check files on disk
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
latest year printed there is recorded, and a year after 1930 is refused (US
public domain is publication in or before 1930, as of 2026) unless the shelf's
`_rights_checked` ({slug: reason}) says why it is still safe. The MARKUP is
Perseus's and is licensed separately: the licence stated in the file is
recorded, else the repository's README statement (CC BY-SA 4.0 for both
canonical repos). That licence travels with the file in the report, so a
consumer sees "attribution + share-alike" without opening it.
Resumable: a file already on disk is kept. A failed fetch is reported, never
written as an empty file.
"""
import json, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}
PD_CUTOFF = 1930
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
    a, b = tail.split(".")[:2]
    repo = repo_for(tail)
    path = f"data/{a}/{b}/{tail}.xml"
    return repo, [f"https://raw.githubusercontent.com/{repo}/master/{path}",
                  f"https://cdn.jsdelivr.net/gh/{repo}@master/{path}"]

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

def check(data, tail, translator, slug, shelf):
    """Identity + rights. Returns the report fields; raises to refuse."""
    text = data.decode("utf-8", "replace")
    if "<TEI" not in text[:5000]:
        raise RuntimeError("not a TEI file")
    head = text[:text.find("</teiHeader>")] if "</teiHeader>" in text else text[:20000]
    r = {"urn_in_file": tail in text}
    # "Vince, J. H." -> Vince; "J. H. Vince" -> Vince; "W. R. M. Lamb (ed.)" -> Lamb
    who = re.sub(r"\(.*?\)", "", translator or "").split(" and ")[0].strip()
    sn = who.split(",")[0].strip() if "," in who else (who.split() or [""])[-1]
    r["translator_checked"] = sn
    if sn and sn.lower() not in head.lower():
        raise RuntimeError(f"MISMATCH: translator '{sn}' not in the file's header")
    src = re.search(r"<sourceDesc.*?</sourceDesc>", head, re.S)
    # tags stripped first: years inside attributes (archive.org ids such as
    # in.ernet.dli.2015.12682) are not printing dates
    src_text = re.sub(r"<[^>]+>", " ", src.group(0)) if src else ""
    years = [int(y) for y in re.findall(r"\b(1[5-9]\d\d|20\d\d)\b", src_text)]
    r["source_years"] = sorted(set(years))
    lic = re.search(r'<licen[cs]e[^>]*target="([^"]+)"', head) or re.search(r"<licen[cs]e[^>]*>(.*?)</licen", head, re.S)
    r["markup_licence_in_file"] = lic.group(1).strip() if lic else None
    late = [y for y in years if y > PD_CUTOFF]
    if late:
        why = shelf.get("_rights_checked", {}).get(slug)
        if not why:
            raise RuntimeError(f"RIGHTS: source year {max(late)} is after {PD_CUTOFF}; add _rights_checked to keep")
        r["rights_override"] = why
    if not years:
        r["rights_flag"] = "no year in sourceDesc: date from the shelf's rights_note only"
    return r

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
    for slug, row in rows.items():
        tail, title, translator, note = (list(row) + [None] * 4)[:4]
        repo, urls = urls_for(tail)
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
        print(slug, r["status"], r.get("bytes", r.get("error", "")), flush=True)
        if not verify:
            json.dump(report, open(rep_path + ".tmp", "w"), indent=1)
            os.replace(rep_path + ".tmp", rep_path)
    bad = [s for s, r in report.items() if s in rows and r["status"] == "FAILED"]
    print(f"{len(rows)} perseus items, {len(bad)} failed: {bad}")

if __name__ == "__main__":
    main()
