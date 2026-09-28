#!/usr/bin/env python3
"""Fetch every public-domain Jonathan Edwards text named in edwards_shelf.json.

    python3 pipeline/fetch_edwards.py            # from canon-corpus root
Writes data/corpus/edwards/<slug>.(xml|txt) and edwards_fetch_report.json.
Resumable: a file already on disk is kept. A fetch that fails is REPORTED,
never written as an empty file (a failed measurement stored as a value reads
as data). Internet Archive items are the OCR text layer (<id>_djvu.txt),
raw and unconverted; each is checked for its title words and a plausible size.
"""
import json, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "data", "corpus", "edwards")
UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}
SHELF = json.load(open(os.path.join(HERE, "edwards_shelf.json"), encoding="utf-8"))

def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                return r.read()
        except Exception as e:
            err = e
            time.sleep(2 ** i)
    raise RuntimeError(f"{url}: {err}")

def main():
    os.makedirs(OUT, exist_ok=True)
    report = {}
    jobs = []
    for slug, (work, title, _) in SHELF["ccel"].items():
        jobs.append((slug, title, f"https://ccel.org/ccel/e/edwards/{work}.xml", ".xml"))
    for slug, (pg, title) in SHELF["gutenberg"].items():
        jobs.append((slug, title, f"https://www.gutenberg.org/cache/epub/{pg}/pg{pg}.txt", ".txt"))
    for slug, (ident, title) in SHELF["internet_archive"].items():
        jobs.append((slug, title, f"https://archive.org/download/{ident}/{ident}_djvu.txt", ".txt"))
    for slug, title, url, ext in jobs:
        dest = os.path.join(OUT, slug + ext)
        if os.path.exists(dest) and os.path.getsize(dest) > 5000:
            report[slug] = {"status": "kept", "bytes": os.path.getsize(dest), "url": url}
            continue
        try:
            data = get(url)
            if len(data) < 5000:
                raise RuntimeError(f"only {len(data)} bytes")
            open(dest + ".tmp", "wb").write(data)
            os.replace(dest + ".tmp", dest)
            head = data[:20000].decode("utf-8", "replace").lower()
            key = [w for w in re.findall(r"[a-z]{5,}", title.lower()) if w not in ("works", "edwards")][:2]
            report[slug] = {"status": "fetched", "bytes": len(data), "url": url,
                            "edwards_named": "edwards" in head,
                            "title_words_seen": {w: (w in head) for w in key}}
        except Exception as e:
            report[slug] = {"status": "FAILED", "error": str(e), "url": url}
        print(slug, report[slug]["status"], report[slug].get("bytes", ""), flush=True)
        time.sleep(1)
    json.dump(report, open(os.path.join(OUT, "edwards_fetch_report.json"), "w"), indent=1)
    bad = [s for s, r in report.items() if r["status"] == "FAILED"]
    print(f"{len(report)} items, {len(bad)} failed: {bad}")

if __name__ == "__main__":
    main()
