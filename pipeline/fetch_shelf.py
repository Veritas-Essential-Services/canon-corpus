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

def check_identity(r, data, key, names, kind):
    """Refuse a scan that is not the book the shelf names (lane A, 2026-10-02).
    The title words are looked for in the WHOLE text, not just the head (title
    pages are often lost to OCR); the author's name words (`_name_words`) must
    appear somewhere. None of the title words anywhere, or no author name at
    all, raises: the file is not written and the item is reported FAILED as a
    MISMATCH. Some but not all title words found is kept and flagged
    `title_weak` for a human to look at. Shelves without `_name_words`, and
    titles with no checkable word, skip the respective test."""
    full = data.decode("utf-8", "replace").lower()
    seen = {w: (w in full) for w in key}
    r["title_words_in_text"] = seen
    if names:
        r["author_seen"] = any(n in full for n in names)
        if not r["author_seen"]:
            raise RuntimeError(f"MISMATCH: no author name {sorted(names)} anywhere in the {kind} text")
    if key and not any(seen.values()):
        raise RuntimeError(f"MISMATCH: none of the title words {key} anywhere in the {kind} text")
    if key and not all(seen.values()):
        r["title_weak"] = True

def verify(name, shelf, out, skip, names):
    """--verify: re-run the identity check over files already on disk."""
    bad = []
    for slug, title, url, ext, kind in jobs_for(shelf, name):
        dest = os.path.join(out, slug + ext)
        if not os.path.exists(dest):
            continue
        key = [w for w in re.findall(r"[a-z]{5,}", re.sub(r"\(.*?\)", "", title).lower()) if w not in skip][:2]
        r = {}
        try:
            check_identity(r, open(dest, "rb").read(), key, names, kind)
            flag = "title_weak" if r.get("title_weak") else "ok"
        except RuntimeError as e:
            flag = str(e)
            bad.append(slug)
        print(slug, flag, flush=True)
    print(f"verify: {len(bad)} mismatched: {bad}")

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
    if len(sys.argv) < 2:
        sys.exit("usage: fetch_shelf.py <shelf>   (reads pipeline/<shelf>_shelf.json)")
    name = sys.argv[1]
    shelf = json.load(open(os.path.join(HERE, f"{name}_shelf.json"), encoding="utf-8"))
    out = os.path.join(ROOT, "data", "corpus", name)
    os.makedirs(out, exist_ok=True)
    skip = set(w.lower() for w in shelf.get("_name_words", [])) | {"works", "volume", "vol"}
    names = set(w.lower() for w in shelf.get("_name_words", []))
    if "--verify" in sys.argv[2:]:
        return verify(name, shelf, out, skip, names)
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
            check_identity(r, data, key, names, kind)
            if kind == "gutenberg":
                r["pg_copyrighted"] = "copyrighted project gutenberg" in low
                m = re.search(r"^Translator:\s*(.+)$", head, re.M)
                r["pg_translator"] = m.group(1).strip() if m else None
                if r["pg_copyrighted"]:
                    raise RuntimeError("COPYRIGHTED Project Gutenberg eBook: rights gate refuses it")
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
    bad = [s for s, r in report.items() if r["status"] == "FAILED"]
    print(f"{len(report)} items, {len(bad)} failed: {bad}")

if __name__ == "__main__":
    main()
