#!/usr/bin/env python3
"""Fetch every text named in pipeline/<shelf>_shelf.json (generalised fetch_edwards.py).

    python3 pipeline/fetch_shelf.py <shelf>          # e.g. jowett-plato, from canon-corpus root
Writes data/corpus/<shelf>/<slug>.(xml|txt) and <shelf>_fetch_report.json.
Resumable: a file already on disk is kept. A fetch that fails is REPORTED,
never written as an empty file (a failed measurement stored as a value reads
as data). Internet Archive items are the OCR text layer (<id>_djvu.txt), raw
and unconverted; each is checked for its title words and a plausible size.
Gutenberg items are checked for the COPYRIGHTED marker (rights gate, CLAUDE.md).

Shelf shape (same as edwards_shelf.json): "ccel", "gutenberg", "internet_archive"
dicts of slug -> [id, title, ...extra]. Optional "_ccel_author": "e/edwards"
gives the CCEL author path; without it, the shelf name is used (first letter /
name). A CCEL entry's id may itself be a full "x/author/work" path. Optional
"_name_words": words to skip in the title check (the author's name).
"""
import json, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}

def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                return r.read()
        except Exception as e:
            err = e
            time.sleep(2 ** i)
    raise RuntimeError(f"{url}: {err}")

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
        jobs.append((slug, row[1], f"https://archive.org/download/{ident}/{ident}_djvu.txt", ".txt", "ia"))
    return jobs

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: fetch_shelf.py <shelf>   (reads pipeline/<shelf>_shelf.json)")
    name = sys.argv[1]
    shelf = json.load(open(os.path.join(HERE, f"{name}_shelf.json"), encoding="utf-8"))
    out = os.path.join(ROOT, "data", "corpus", name)
    os.makedirs(out, exist_ok=True)
    skip = set(w.lower() for w in shelf.get("_name_words", [])) | {"works", "volume", "vol"}
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
            key = [w for w in re.findall(r"[a-z]{5,}", title.lower()) if w not in skip][:2]
            r["title_words_seen"] = {w: (w in low) for w in key}
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
