"""Scan in: fetch a PDF, rasterize a page, OCR it to hOCR, parse the hOCR.

Every step writes one file per page and skips pages already done, so a killed run resumes where it
stopped (canon-corpus rule 5). Writes go to a temp name and are renamed into place, so a half-written
page never looks finished.

🔴 tesseract runs with OMP_THREAD_LIMIT=1. Without it OpenMP oversubscribes a small box and the same
page takes several times longer for byte-identical output (measured on Thayer's, CLAUDE.md).
"""
import os
import re
import subprocess
import urllib.request
import xml.etree.ElementTree as ET

ARCHIVE_PDF = "https://archive.org/download/{id}/{id}.pdf"
NS = "{http://www.w3.org/1999/xhtml}"


def _atomic(path, data, mode="wb"):
    tmp = path + ".part"
    with open(tmp, mode) as f:
        f.write(data)
    os.replace(tmp, path)


def fetch_pdf(ident, dest):
    """archive.org identifier -> its PDF at `dest` (skipped if already there)."""
    if os.path.exists(dest):
        return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with urllib.request.urlopen(ARCHIVE_PDF.format(id=ident), timeout=300) as r:
        _atomic(dest, r.read())
    return dest


def page_count(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"^Pages:\s+(\d+)", out, re.M).group(1))


def rasterize(pdf, n, out_png, dpi=300, gray=True):
    """Page n (1-based) of `pdf` -> `out_png`. Gray for OCR; colour when a plate is cropped."""
    if os.path.exists(out_png):
        return out_png
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    stem = out_png[:-4] + ".part"
    args = ["pdftoppm", "-r", str(dpi), "-f", str(n), "-l", str(n), "-singlefile", "-png"]
    if gray:
        args.append("-gray")
    subprocess.run(args + [pdf, stem], check=True)
    os.replace(stem + ".png", out_png)
    return out_png


def ocr_page(png, out_hocr, lang="eng"):
    """png -> hOCR (words with boxes and confidences). Skipped if already done."""
    if os.path.exists(out_hocr):
        return out_hocr
    os.makedirs(os.path.dirname(out_hocr), exist_ok=True)
    base = out_hocr[:-5] + ".part"
    env = dict(os.environ, OMP_THREAD_LIMIT="1")
    subprocess.run(["tesseract", png, base, "-l", lang, "--psm", "3", "hocr"],
                   check=True, env=env, capture_output=True)
    os.replace(base + ".hocr", out_hocr)
    return out_hocr


def _title(el):
    t = el.get("title", "")
    out = {}
    for part in t.split(";"):
        part = part.strip()
        if not part:
            continue
        k, _, v = part.partition(" ")
        out[k] = v
    return out


def _bbox(props):
    return [int(x) for x in props["bbox"].split()]


def parse_hocr(path):
    """hOCR -> {"w", "h", "lines": [{"bbox", "x_size", "baseline", "words": [{"t","bbox","conf"}]}]}.

    Lines come in tesseract's reading order. Empty words (tesseract emits some for noise) are dropped,
    and a line left with no words is dropped with them.
    """
    root = ET.parse(path).getroot()
    page = next(el for el in root.iter() if el.get("class") == "ocr_page")
    x0, y0, x1, y1 = _bbox(_title(page))
    lines = []
    for el in page.iter():
        cls = el.get("class", "")
        if cls not in ("ocr_line", "ocr_header", "ocr_caption", "ocr_textfloat"):
            continue
        p = _title(el)
        words = []
        for w in el.iter():
            if w.get("class") != "ocrx_word":
                continue
            text = "".join(w.itertext()).strip()
            if not text:
                continue
            wp = _title(w)
            words.append({"t": text, "bbox": _bbox(wp), "conf": int(float(wp.get("x_wconf", 0)))})
        if not words:
            continue
        base = [float(v) for v in p.get("baseline", "0 0").split()]
        lines.append({"bbox": _bbox(p), "x_size": float(p.get("x_size", 0) or 0),
                      "baseline": base, "kind": cls, "words": words})
    return {"w": x1 - x0, "h": y1 - y0, "lines": lines}
