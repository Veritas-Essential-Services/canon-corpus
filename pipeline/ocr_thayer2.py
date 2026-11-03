#!/usr/bin/env python3
"""A SECOND OCR of Thayer's (1889), from the original page scans.

The first OCR (data/corpus/lexicons/thayer-pages.json, 2026-09-06) read the
archive.org PDF at 300 dpi. It stays the text of record, byte for byte. This
second reading exists for ONE job: finding headwords the first one mangled
past recognition, so convert_thayer_entries can cut an entry there (see its
`second_path`). Its text never replaces a word of the first.

Source: archive.org `greekenglishlexi00grimuoft`, the ORIGINAL JP2 scans
(the _jp2.zip, not the PDF derived from it). Engine: tesseract 5,
tessdata_best grc+eng, --psm 3, OMP_THREAD_LIMIT=1 per process (CLAUDE.md:
without it tesseract's OpenMP oversubscribes the box for identical output),
parallel across pages instead.

    python3 pipeline/ocr_thayer2.py --map         # check the leaf -> page mapping
    python3 pipeline/ocr_thayer2.py [--jobs N]    # OCR every lexicon page (resumable)
    python3 pipeline/ocr_thayer2.py --collect     # pages/*.txt -> thayer-pages-2.json

Resumable: a page whose .txt exists is skipped. Everything lands under
data/corpus/lexicons/thayer-ocr2/ (gitignored, like all of data/corpus/).
"""
import concurrent.futures as cf
import io
import json
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "..", "data", "corpus", "lexicons")
WORK = os.path.join(LEX, "thayer-ocr2")
ZIP = os.path.join(WORK, "scan_jp2.zip")
PAGES = os.path.join(WORK, "pages")
TESSDATA = os.path.join(WORK, "tessdata")
FIRST = os.path.join(LEX, "thayer-pages.json")
OUT = os.path.join(LEX, "thayer-pages-2.json")
TESSERACT = os.environ.get("TESSERACT") or (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe" if os.name == "nt" else "tesseract")
# The first OCR's page key N is the zip's leaf ..._000N.jp2. Checked with
# --map on 2026-10-02 (p.100 ἀρτύω, p.400 λειτουργικός, both readings).
LEAF_OFFSET = int(os.environ.get("THAYER_LEAF_OFFSET", "0"))


def leaves():
    with zipfile.ZipFile(ZIP) as z:
        names = sorted(n for n in z.namelist() if n.lower().endswith(".jp2"))
    return {int(os.path.splitext(n)[0].rsplit("_", 1)[1]): n for n in names}


def ocr_one(key, name):
    """Leaf -> pages/<key>.txt. Written via a temp name, so a killed run never
    leaves a half page that the next run would skip."""
    out = os.path.join(PAGES, f"{key}.txt")
    if os.path.exists(out):
        return key, "kept"
    from PIL import Image
    with zipfile.ZipFile(ZIP) as z:
        img = Image.open(io.BytesIO(z.read(name))).convert("L")
    png = os.path.join(PAGES, f"{key}.png")
    img.save(png)
    env = dict(os.environ, OMP_THREAD_LIMIT="1", TESSDATA_PREFIX=TESSDATA)
    base = os.path.join(PAGES, f"{key}.part")
    r = subprocess.run([TESSERACT, png, base, "-l", "grc+eng", "--psm", "3"],
                       env=env, capture_output=True, text=True)
    os.remove(png)
    if r.returncode != 0:
        return key, "FAIL " + r.stderr.strip()[-200:]
    os.replace(base + ".txt", out)
    return key, "ok"


def body_keys():
    """The lexicon pages: the first OCR's run of Greek running heads, up to the
    APPENDIX -- the same body convert_thayer_entries reads."""
    sys.path.insert(0, HERE)
    import structure_texts as st
    pages = json.load(open(FIRST, encoding="utf-8"))
    order = sorted(pages, key=int)
    heads = {p: st._thayer_page(pages[p])[0] for p in order}
    greek = [p for p in order if heads[p] and st.RE_GREEK.search(heads[p][0])]
    body = order[order.index(greek[0]):order.index(greek[-1]) + 1]
    for i, p in enumerate(body):
        if heads[p] and "APPENDIX" in heads[p][0].upper():
            return body[:i]
    return body


def main():
    os.makedirs(PAGES, exist_ok=True)
    lv = leaves()
    if "--collect" in sys.argv:
        got = {}
        for f in sorted(os.listdir(PAGES), key=lambda f: int(f.split(".")[0])
                        if f.split(".")[0].isdigit() else -1):
            if f.endswith(".txt") and ".part" not in f:
                got[f[:-4]] = open(os.path.join(PAGES, f), encoding="utf-8").read()
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(got, fh, ensure_ascii=False, indent=0)
        print(f"{len(got)} pages -> {os.path.relpath(OUT)}")
        return
    keys = body_keys()
    if "--map" in sys.argv:
        keys = [k for k in keys if k in ("100", "400")]
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv \
        else max(1, (os.cpu_count() or 2) - 2)
    todo = [(k, lv[int(k) + LEAF_OFFSET]) for k in keys if int(k) + LEAF_OFFSET in lv]
    print(f"{len(todo)} lexicon pages, {jobs} at a time", flush=True)
    done = 0
    with cf.ThreadPoolExecutor(jobs) as ex:
        for key, status in ex.map(lambda kn: ocr_one(*kn), todo):
            done += 1
            if status != "kept" or done % 50 == 0:
                print(f"{done}/{len(todo)} p.{key}: {status}", flush=True)
    if "--map" in sys.argv:
        first = json.load(open(FIRST, encoding="utf-8"))
        for k in keys:
            a = first[k].split("\n")[0]
            b = open(os.path.join(PAGES, f"{k}.txt"), encoding="utf-8").read().split("\n")[0]
            print(f"p.{k}: first OCR head {a!r} | second {b!r}")


if __name__ == "__main__":
    main()
