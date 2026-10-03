#!/usr/bin/env python3
"""Fetch every text named in pipeline/<shelf>_shelf.json (generalised fetch_edwards.py).

    python3 pipeline/fetch_shelf.py <shelf>          # e.g. jowett-plato, from canon-corpus root
    python3 pipeline/fetch_shelf.py <shelf> --verify # re-check files on disk: right book?
Writes data/corpus/<shelf>/<slug>.(xml|txt) and <shelf>_fetch_report.json.
Resumable: a file already on disk is kept. A fetch that fails is REPORTED,
never written as an empty file (a failed measurement stored as a value reads
as data). Internet Archive items are the OCR text layer (<id>_djvu.txt), raw
and unconverted; each is checked for its title words and a plausible size.
Gutenberg items are checked for the COPYRIGHTED marker (rights gate, CLAUDE.md).

Shelf shape (same as edwards_shelf.json): "ccel", "gutenberg", "internet_archive"
dicts of slug -> [id, title, ...extra]. Optional "_ccel_author": "e/edwards"
gives the CCEL author path; an internet_archive row may carry a third element,
the item's text file name, when it is not <id>_djvu.txt; without it, the shelf name is used (first letter /
name). A CCEL entry's id may itself be a full "x/author/work" path. Optional
"_name_words": words to skip in the title check (the author's name).

Optional, added 2026-10-02 after review (all backward compatible; a shelf
without them behaves as before):
  "_surname": ["edwards", ...]   the author's (or translator's) surname, as
      whole words; one must appear in the text. Without it the old test runs:
      any `_name_words` entry as a substring, which "john" or "law" passes.
  "_surname_by_slug": {slug: [...]}  on a shelf holding several authors,
      the names THIS item must show, in place of the shelf-wide `_surname`
      (which any one author's name would pass). Added 2026-10-03.
      A bare surname that is also a common English word ("hall", "ken";
      COMMON_WORD_SURNAMES) is never matched on its own: list a multi-word
      form beside it, or the shelf stops at load (2026-10-03).
  "_translators": {slug: "Constable"}  the translator claimed for an item;
      a Gutenberg header naming someone else, or a text that never names
      them, is refused as a MISMATCH.
  "_rights_checked": {slug: reason}  keeps an archive.org item the rights
      gate would refuse (published 1930 or later, or a lending-library
      scan) after a person has read its title page.
  --verify --record writes "_checks" into the shelf (committed): per item,
      what the identity, rights-line and translator checks found, so the
      evidence outlives the gitignored fetch report.
The item's own identifier is removed from the text before any check: Google
and IA scans often print it in the OCR, which let "ryle" pass for a tract
that never names Ryle.
"""
import gzip, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}

def get(url, tries=5):
    headers = UA
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=180) as r:
                data = r.read()
            # Some Gutenberg files exist only gzip-encoded and answer a plain
            # request with HTTP 406 (PG 7825); those are asked for again
            # accepting gzip, and decompressed here.
            return gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data
        except urllib.error.HTTPError as e:
            err = e
            if e.code == 406 and headers is UA:
                headers = {**UA, "Accept-Encoding": "gzip"}
                continue
            time.sleep(2 ** i)
        except Exception as e:
            err = e
            time.sleep(2 ** i)
    raise RuntimeError(f"{url}: {err}")

def _pat(phrase):
    """A surname or phrase as whole words; spaces match any run of spaces or
    hyphens (OCR line breaks), an apostrophe is optional (M'Cheyne)."""
    words = [re.escape(w).replace("'", "['\u2019\u2018`]?") for w in phrase.lower().split()]
    return re.compile(r"(?<![a-z])" + r"[\s\-]+".join(words) + r"(?![a-z])")

def _scrub(data, ident):
    full = data.decode("utf-8", "replace").lower() if isinstance(data, bytes) else data.lower()
    if ident:
        for v in {ident.lower(), ident.lower().replace("_", " ")}:
            full = full.replace(v, " ")
    return full

# Surnames that are also ordinary English words (lane A, 2026-10-03). As a
# bare whole word, "hall" or "ken" is found in nearly every book, so the
# author check would pass on anything and the gate would rest on title words
# alone. A shelf may still list such a word, but only beside a multi-word
# form ("joseph hall", "bishop hall"); the bare word is then never used to
# match, and a shelf whose only forms are bare common words stops at load.
COMMON_WORD_SURNAMES = frozenset("""
    bacon baker barrow bates bishop black bridge bridges brown burns butler
    church cook dean field fuller gale gay gill gray green grant hall henry
    hill hood hooker hope hunt james jay jewel ken king lamb lane law love
    mason more page palmer pope price prior rich rose skinner smith swift
    taylor ward wells white wood young
""".split())

def _usable(surnames):
    """The surname forms the gate may match on: never a bare common word."""
    return [n for n in surnames or [] if len(n.split()) > 1 or n.lower() not in COMMON_WORD_SURNAMES]

def check_surnames(shelf):
    """Stop at load on a name list the gate could not use: one whose every
    form is a bare common English word. Returns the problems found."""
    lists = {"_surname": shelf.get("_surname")}
    lists.update({f"_surname_by_slug[{k}]": v for k, v in shelf.get("_surname_by_slug", {}).items()})
    bad = []
    for where, names in lists.items():
        if names and not _usable(names):
            bad.append(f"{where} {names}: every form is a bare common English word; "
                       f"add a multi-word form such as \"joseph hall\" or \"bishop hall\"")
    return bad

def check_identity(r, data, key, names, kind, override=None, surname=None, ident=None,
                   translator=None):
    """Run every identity check, then refuse on any miss an override does not
    cover (fixed 2026-10-03: it used to raise at the FIRST miss, so an
    `_identity_checked` excuse for the author silently skipped the translator
    and title checks after it). An override covers only the miss it names:
    a dict {"author": reason, "title": reason} names its kinds; a plain string
    (every override written before this fix) covers the first author-or-title
    miss, the one it was written for, since nothing after it was ever checked.
    No override ever covers the translator."""
    misses = _check_identity(r, data, key, names, kind, surname, ident, translator)
    if not misses:
        return
    if isinstance(override, dict):
        covered = {k: v for k, v in override.items() if k in ("author", "title")}
    elif override:
        first = next((k for k, _ in misses if k != "translator"), None)
        covered = {first: override} if first else {}
    else:
        covered = {}
    left = [m for k, m in misses if k not in covered]
    if left:
        raise RuntimeError("; ".join(left))
    r["identity_override"] = "; ".join(f"{m} -- kept: {covered[k]}" for k, m in misses)

def _check_identity(r, data, key, names, kind, surname=None, ident=None, translator=None):
    """Refuse a scan that is not the book the shelf names (lane A, 2026-10-02).
    The title words are looked for in the WHOLE text, not just the head (title
    pages are often lost to OCR); the author's name words (`_name_words`) must
    appear somewhere. None of the title words anywhere, or no author name at
    all, is a miss: the file is not written and the item is reported FAILED as
    a MISMATCH. Some but not all title words found is kept and flagged
    `title_weak` for a human to look at. Shelves without `_name_words`, and
    titles with no checkable word, skip the respective test.
    A title with only ONE checkable word (often an editor's name, as in
    "Works, Dwight ed., vol. 2") is too thin to refuse on: a miss there is
    flagged `title_weak`, not refused. A slug listed in the shelf's
    `_identity_checked` was confirmed another way (content counts, a look by
    eye): the misses it covers (see check_identity) are kept, flagged
    `identity_override`, and the reason recorded.
    Returns every miss as (kind, message), kind in author/translator/title."""
    full = _scrub(data, ident)
    misses = []
    seen = {w: (w in full) for w in key}
    r["title_words_in_text"] = seen
    if surname:
        r["name_check"] = "surname"
        r["author_seen"] = next((n for n in _usable(surname) if _pat(n).search(full)), None)
        if not r["author_seen"]:
            misses.append(("author", f"MISMATCH: surname {surname} never appears as a word in the {kind} text"))
    elif names:
        r["name_check"] = "legacy: any _name_words substring"
        r["author_seen"] = any(n in full for n in names)
        if not r["author_seen"]:
            misses.append(("author", f"MISMATCH: no author name {sorted(names)} anywhere in the {kind} text"))
    if translator:
        r["translator_claimed"] = translator
        r["translator_in_text"] = bool(_pat(translator).search(full))
        if not r["translator_in_text"]:
            misses.append(("translator", f"MISMATCH: claimed translator {translator!r} never named in the {kind} text"))
    if len(key) >= 2 and not any(seen.values()):
        misses.append(("title", f"MISMATCH: none of the title words {key} anywhere in the {kind} text"))
    elif key and not all(seen.values()):
        r["title_weak"] = True
    return misses

LENDING = {"inlibrary", "printdisabled", "lendinglibrary"}  # not "internetarchivebooks": IA's own scans, PD ones included

def ia_rights(ident):
    """The rights gate for an archive.org item, from its catalogue record. A
    published year of 1930 or later, or a lending-library collection (the
    controlled-lending scans of in-copyright books), is flagged CHECK; the
    caller refuses a new fetch on it unless `_rights_checked` names the slug.
    The caller refuses anything that is not "ok" (fixed 2026-10-03: an
    unreachable catalogue used to read "unchecked" and slip past a gate that
    only refused "CHECK"). The latest year on the record decides: "1965
    [c1890]" is a 1965 printing, not an 1890 one (it used min, 2026-10-03)."""
    rec = {"ia_rights": "unchecked"}
    try:
        m = json.loads(get(f"https://archive.org/metadata/{ident}/metadata", tries=3))["result"]
    except Exception as e:
        rec["ia_rights"] = f"unchecked: catalogue not reachable ({str(e)[:60]})"
        return rec
    date = str(m.get("date") or "")
    cols = m.get("collection") or []
    cols = [cols] if isinstance(cols, str) else cols
    # "186-?" (decade known, year not) counts as its decade's first year
    years = [int(y.replace("-", "0").replace("?", "0"))
             for y in re.findall(r"(?<!\d)(1[4-9]\d[\d\-?]|20\d\d)(?!\d)", date)]
    rec.update({"ia_date": date or None,
                "ia_possible_copyright_status": m.get("possible-copyright-status"),
                "ia_lending": sorted(set(cols) & LENDING) or None})
    why = []
    if years and max(years) >= 1930:
        why.append(f"published {max(years)}")
    if not years:
        why.append("no date on the record")
    if rec["ia_lending"]:
        why.append("lending-library scan")
    rec["ia_rights"] = ("CHECK: " + "; ".join(why)) if why else f"ok: published {max(years)}"
    return rec

CCEL_TERMS = ("CCEL asks that some of its prepared editions not be used commercially "
              "(CLAUDE.md rule 6); republishing waits on Adam's ruling")

def ccel_rights(data):
    t = data.decode("utf-8", "replace") if isinstance(data, bytes) else data
    m = re.findall(r"<DC\.Rights[^>]*>(.*?)</DC\.Rights>", t, re.S)
    return {"ccel_dc_rights": " / ".join(x.strip() for x in m if x.strip()) or None,
            "ccel_copyright_comment": "Copyright Christian Classics Ethereal Library" in t[:5000],
            "ccel_terms": CCEL_TERMS}

def pg_rights(data, r, claimed=None):
    head = data[:20000].decode("utf-8", "replace") if isinstance(data, bytes) else data[:20000]
    r["pg_copyrighted"] = "copyrighted project gutenberg" in head.lower()
    # a header naming several translators continues on indented lines
    # (PG 66350: "Translator: George Chapman" / "        Sir Charles Abraham Elton")
    m = re.search(r"^Translators?:[ \t]*(.+(?:\r?\n[ \t]+\S.*)*)", head, re.M)
    r["pg_translator"] = "; ".join(x.strip() for x in m.group(1).splitlines() if x.strip()) if m else None
    if claimed and r["pg_translator"]:
        # whole words, never a substring ("long" must not match "Longfellow")
        r["translator_match"] = bool(_pat(claimed).search(r["pg_translator"].lower()))
    return r

def surname_for(shelf, slug):
    """The names an item must show: its own `_surname_by_slug` entry when the
    shelf gives one, else the shelf-wide `_surname`."""
    return shelf.get("_surname_by_slug", {}).get(slug) or shelf.get("_surname")

def checks_for(slug, kind, data, url, shelf, key, names, ident):
    """Everything --record commits for one item (no body text, only findings)."""
    r = {"kind": kind, "checked": time.strftime("%Y-%m-%d")}
    try:
        check_identity(r, data, key, names, kind, shelf.get("_identity_checked", {}).get(slug),
                       surname_for(shelf, slug), ident, shelf.get("_translators", {}).get(slug))
        r["identity"] = ("identity_override" if r.get("identity_override")
                         else "title_weak" if r.get("title_weak") else "ok")
    except RuntimeError as e:
        r["identity"] = str(e)
    for k in ("title_words_in_text", "identity_override"):
        r.pop(k, None)
    if kind == "gutenberg":
        pg_rights(data, r, shelf.get("_translators", {}).get(slug))
    elif kind == "ccel":
        r.update(ccel_rights(data))
    elif kind == "ia":
        r.update(ia_rights(ident))
        if slug in shelf.get("_rights_checked", {}):
            r["rights_override"] = shelf["_rights_checked"][slug]
    return r

def verify(name, shelf, out, skip, names, record=False):
    """--verify: re-run the identity check over files already on disk."""
    bad, flagged, checks = [], [], {}
    for slug, title, url, ext, kind in jobs_for(shelf, name):
        dest = os.path.join(out, slug + ext)
        if not os.path.exists(dest):
            continue
        key = [w for w in re.findall(r"[a-z]{5,}", re.sub(r"\(.*?\)", "", title).lower()) if w not in skip][:2]
        ident = ident_of(shelf, slug, kind)
        data = open(dest, "rb").read()
        if record:
            c = checks_for(slug, kind, data, url, shelf, key, names, ident)
            checks[slug] = c
            flag = c["identity"]
            if flag not in ("ok", "title_weak", "identity_override"):
                bad.append(slug)
            rights = c.get("ia_rights", "")
            if (c["kind"] == "ia" and not rights.startswith("ok") and not c.get("rights_override")) \
                    or c.get("pg_copyrighted") \
                    or c.get("translator_match") is False:
                flagged.append(slug)
                flag += f" | RIGHTS {rights or c.get('pg_translator')}"
            print(slug, flag, flush=True)
            continue
        r = {}
        try:
            check_identity(r, data, key, names, kind, shelf.get("_identity_checked", {}).get(slug),
                           surname_for(shelf, slug), ident, shelf.get("_translators", {}).get(slug))
            flag = ("identity_override" if r.get("identity_override")
                    else "title_weak" if r.get("title_weak") else "ok")
        except RuntimeError as e:
            flag = str(e)
            bad.append(slug)
        print(slug, flag, flush=True)
    if record:
        path = os.path.join(HERE, f"{name}_shelf.json")
        fresh = json.load(open(path, encoding="utf-8"))
        fresh["_checks"] = checks
        json.dump(fresh, open(path + ".tmp", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        open(path + ".tmp", "a", encoding="utf-8").write("\n")
        os.replace(path + ".tmp", path)
        print(f"recorded _checks for {len(checks)} items in {name}_shelf.json; rights flags: {flagged}")
    print(f"verify: {len(bad)} mismatched: {bad}")

def ident_of(shelf, slug, kind):
    if kind == "ia":
        return shelf.get("internet_archive", {})[slug][0]
    return None

def jobs_for(shelf, name):
    ccel_author = shelf.get("_ccel_author") or f"{name[0]}/{name}"
    jobs = []
    for slug, row in shelf.get("ccel", {}).items():
        work = row[0]
        path = work if work.count("/") >= 2 else f"{ccel_author}/{work}"
        jobs.append((slug, row[1], f"https://ccel.org/ccel/{path}.xml", ".xml", "ccel"))
    for slug, row in shelf.get("gutenberg", {}).items():
        pg = row[0]
        jobs.append((slug, row[1], f"https://www.gutenberg.org/cache/epub/{pg}/pg{pg}.txt", ".txt", "gutenberg"))
    for slug, row in shelf.get("internet_archive", {}).items():
        ident = row[0]
        # optional third element: the item's text file when IA did not name it
        # <id>_djvu.txt (some uploads keep the uploader's file name)
        fname = row[2] if len(row) > 2 and str(row[2]).endswith("_djvu.txt") else f"{ident}_djvu.txt"
        url = f"https://archive.org/download/{ident}/" + urllib.parse.quote(fname)
        jobs.append((slug, row[1], url, ".txt", "ia"))
    return jobs

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) >= 2 else "usage: fetch_shelf.py <shelf>   (reads pipeline/<shelf>_shelf.json)")
    name = sys.argv[1]
    path = os.path.join(HERE, f"{name}_shelf.json")
    if not os.path.exists(path):
        sys.exit(f"no shelf named {name!r}: {path} does not exist (usage: fetch_shelf.py <shelf> [--verify [--record]])")
    shelf = json.load(open(path, encoding="utf-8"))
    bad = check_surnames(shelf)
    if bad:
        sys.exit(f"{name}_shelf.json: " + "; ".join(bad))
    out = os.path.join(ROOT, "data", "corpus", name)
    os.makedirs(out, exist_ok=True)
    skip = set(w.lower() for w in shelf.get("_name_words", [])) | {"works", "volume", "vol"}
    names = set(w.lower() for w in shelf.get("_name_words", []))
    if "--verify" in sys.argv[2:]:
        return verify(name, shelf, out, skip, names, record="--record" in sys.argv[2:])
    rep_path = os.path.join(out, f"{name}_fetch_report.json")
    report = json.load(open(rep_path)) if os.path.exists(rep_path) else {}
    for slug, title, url, ext, kind in jobs_for(shelf, name):
        dest = os.path.join(out, slug + ext)
        if os.path.exists(dest) and os.path.getsize(dest) > 5000:
            prev = report.get(slug, {})
            report[slug] = {**prev, "status": "kept", "bytes": os.path.getsize(dest), "url": url}
            continue
        try:
            data = get(url)
            if len(data) < 5000:
                raise RuntimeError(f"only {len(data)} bytes")
            if ext == ".txt" and data.lstrip()[:15].lower().startswith((b"<!doctype", b"<html")):
                raise RuntimeError("got an HTML page, not text (a 404 or error page served as 200)")
            head = data[:20000].decode("utf-8", "replace")
            low = head.lower()
            r = {"status": "fetched", "bytes": len(data), "url": url}
            key = [w for w in re.findall(r"[a-z]{5,}", re.sub(r"\(.*?\)", "", title).lower()) if w not in skip][:2]
            r["title_words_seen"] = {w: (w in low) for w in key}
            claimed = shelf.get("_translators", {}).get(slug)
            check_identity(r, data, key, names, kind,
                           shelf.get("_identity_checked", {}).get(slug),
                           surname_for(shelf, slug), ident_of(shelf, slug, kind), claimed)
            if kind == "gutenberg":
                pg_rights(data, r, claimed)
                if r["pg_copyrighted"]:
                    raise RuntimeError("COPYRIGHTED Project Gutenberg eBook: rights gate refuses it")
                if r.get("translator_match") is False:
                    raise RuntimeError(f"MISMATCH: Gutenberg names translator {r['pg_translator']!r}, the shelf claims {claimed!r}")
            if kind == "ia":
                r.update(ia_rights(ident_of(shelf, slug, kind)))
                if not r["ia_rights"].startswith("ok") and slug not in shelf.get("_rights_checked", {}):
                    raise RuntimeError(f"RIGHTS: {r['ia_rights']}; read the title page, then list the slug in _rights_checked")
            open(dest + ".tmp", "wb").write(data)
            os.replace(dest + ".tmp", dest)
            report[slug] = r
        except Exception as e:
            report[slug] = {"status": "FAILED", "error": str(e), "url": url}
        print(slug, report[slug]["status"], report[slug].get("bytes", ""), flush=True)
        json.dump(report, open(rep_path + ".tmp", "w"), indent=1)
        os.replace(rep_path + ".tmp", rep_path)
        time.sleep(1)
    json.dump(report, open(rep_path + ".tmp", "w"), indent=1)
    os.replace(rep_path + ".tmp", rep_path)
    # count only the shelf's current slugs: a report can keep rows for
    # entries since moved to _pending or _alternates
    current = {j[0] for j in jobs_for(shelf, name)}
    bad = [s for s, r in report.items() if s in current and r["status"] == "FAILED"]
    print(f"{len(current)} items, {len(bad)} failed: {bad}")

if __name__ == "__main__":
    main()
