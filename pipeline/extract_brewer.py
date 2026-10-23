#!/usr/bin/env python3
# prov: 2026-10-19 claude-opus-5-5 drafted
# fable_review: pending
"""extract_brewer.py -- Brewer's Dictionary of Phrase and Fable (1894) from
Adam's PDF into page-anchored paragraphs, for structure_texts.convert_brewer.

    python3 pipeline/extract_brewer.py --pdf PATH/TO/Brewers_...1894.pdf

WHY THIS IS NOT A FETCH. Every other lexicon here is downloaded from a
pinned URL. Brewer's is not, because the best text found is a PDF Adam
supplied (2026-10-19): a born-digital typeset of the "New and Enlarged
Edition of 1894" (htmldoc 1.8.23, 2003, Times-Roman body; no scan, no OCR).
The archive.org scans of the 1894-95 printings exist
(e.g. dictionaryofphra01brew, 1895) but their text layers are OCR and would
be a worse reading. So the PDF is the source of record, pinned by sha256
below, and this script is the recipe that turns it into corpus. A different
PDF -- even another copy of "the same" book -- is refused; that is the
point of the pin.

Output: data/corpus/lexicons/brewer-1894.paras.json (gitignored with the rest
of the corpus), and the same bytes gzipped to data/lexicons/
brewer-1894.paras.json.gz, which IS committed: that is how a fresh clone with
no PDF (the hosted rebuild) still builds Brewer's. The JSON is written
compact and the gzip with mtime=0, so the bytes are reproducible and the
pinned PARAS_SHA256 in fetch_sources.py holds. Needs PyMuPDF.

WHAT A PARAGRAPH IS HERE. The typeset gives every paragraph -- headword and
body alike -- the same 26.4pt gap, with 13.2pt between wrapped lines, so a
gap > 20pt opens a paragraph. The page furniture (running title top and
bottom, folio) is set in Helvetica and dropped by font, never by guessing.
The first paragraph on each page is flagged `top`: a page break looks like
a paragraph break, and only the converter, knowing which lines are
headwords, can tell which `top` paragraphs are really continuations.
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "corpus", "lexicons", "brewer-1894.paras.json")
# The same paragraphs, COMMITTED (2026-10-19), so a fresh clone -- the hosted
# Armarium's rebuild above all -- can build Brewer's without the PDF.
# fetch_sources.py unpacks it into OUT after checking PARAS_SHA256.
SHIPPED = os.path.join(ROOT, "data", "lexicons", "brewer-1894.paras.json.gz")
SHA256 = "f575cef46c5a94fb2eaab194c0e19bfc740900ec73094b3980a0ebe8bf95fd5c"
PARA_GAP = 20.0


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract(pdf):
    import pymupdf
    doc = pymupdf.open(pdf)
    toc = [[t, pg] for lv, t, pg in doc.get_toc()
           if lv == 2 and len(t) == 1 and t.isalpha()]
    paras, furniture = [], 0
    for pno in range(doc.page_count):
        prev_y, first = None, True
        for block in doc[pno].get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                spans = [s for s in line["spans"] if not s["font"].startswith("Helvetica")]
                if len(spans) < len(line["spans"]):
                    furniture += 1
                if not spans:
                    continue
                text = "".join(s["text"] for s in spans)
                y = line["bbox"][1]
                new = prev_y is None or y - prev_y > PARA_GAP or y < prev_y
                prev_y = y
                if new or not paras:
                    paras.append({"p": pno + 1, "top": first, "lines": [text]})
                    first = False
                else:
                    paras[-1]["lines"].append(text)
    return {"source_sha256": sha256(pdf), "pages": doc.page_count,
            "toc": toc, "furniture_lines": furniture, "paras": paras}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--any-pdf", action="store_true",
                    help="skip the sha256 pin (only for testing a different copy)")
    a = ap.parse_args()
    got = sha256(a.pdf)
    if got != SHA256 and not a.any_pdf:
        sys.exit(f"REFUSED: {a.pdf} sha256 {got}\n  is not the pinned source {SHA256}")
    data = extract(a.pdf)
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT + ".tmp", "wb") as f:                       # atomic, rule 5
        f.write(raw)
    os.replace(OUT + ".tmp", OUT)
    import gzip
    with open(SHIPPED + ".tmp", "wb") as f:
        with gzip.GzipFile(fileobj=f, mode="wb", compresslevel=9, mtime=0, filename="") as g:
            g.write(raw)
    os.replace(SHIPPED + ".tmp", SHIPPED)
    print(f"paragraphs sha256 {hashlib.sha256(raw).hexdigest()}  ->  {SHIPPED}")
    print(f"{OUT}: {len(data['paras']):,} paragraphs from {data['pages']:,} pages, "
          f"{len(data['toc'])} letter sections, {data['furniture_lines']:,} furniture lines dropped")


if __name__ == "__main__":
    main()
