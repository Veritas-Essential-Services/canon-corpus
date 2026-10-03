#!/usr/bin/env python3
"""
tsk_layout.py -- a scan's character OCR (archive.org `_chocr.html.gz`) laid
out as the Treasury prints it: two columns, read left then right, line by
line, each character with the box it was read from.

Why not the plain-text OCR (`_djvu.txt`): it reads some lines straight across
the gutter, gluing the end of a left-column line to the start of a right-column
one ("1-5. Strife arises ... | restores to the king of ... ch.10.10"). Here the
gutter is found per page (the x with least ink between 38% and 62% of the
width), each of tesseract's lines is cut at it, and the halves go to their
columns. A character keeps its box, so a digit can be looked at again in the
page image (tsk_glyphs.py).

    python3 pipeline/tsk_layout.py <scan>_chocr.html.gz <out>.jsonl.gz

Output, one page per line: {"p": page, "W", "H", "g": gutter x,
"cols": [[line: [word: {"t": text, "b": [x0,y0,x1,y1], "c": conf,
"ch": [[char, x0, x1, conf], ...]}]]]}.
"""
import gzip
import html
import json
import os
import re
import sys

PAGE = re.compile(r'class="ocr_page" id="page_(\d+)" title="[^"]*?bbox 0 0 (\d+) (\d+)')
WORD = re.compile(r'class="ocrx_word" id="[^"]+" title="bbox (\d+) (\d+) (\d+) (\d+); x_wconf (\d+)')
CHAR = re.compile(r'class="ocrx_cinfo" title="x_bboxes (\d+) (\d+) (\d+) (\d+); x_conf ([\d.]+)">(.*?)</span>')
LINE = re.compile(r'class="ocr_(?:line|caption|textfloat|header)"')


def raw_pages(path):
    """((page, W, H), [word]) per page, words in tesseract's order with its line id."""
    page, words, w, lid = None, [], None, 0
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for raw in f:
            m = PAGE.search(raw)
            if m:
                if page:
                    yield page, words
                page, words, w = (int(m.group(1)), int(m.group(2)), int(m.group(3))), [], None
                continue
            if LINE.search(raw):
                lid += 1
                continue
            m = WORD.search(raw)
            if m:
                x0, y0, x1, y1, c = map(int, m.groups())
                w = {"b": [x0, y0, x1, y1], "c": c, "l": lid, "ch": []}
                words.append(w)
                continue
            m = CHAR.search(raw)
            if m and w is not None:
                a, _, cx, _ = map(int, m.groups()[:4])
                w["ch"].append([html.unescape(m.group(6)), a, cx, round(float(m.group(5)))])
    if page:
        yield page, words


def gutter(words, width):
    """The x between the columns: least word coverage in the middle band."""
    lo, hi = int(width * 0.38), int(width * 0.62)
    cov = [0] * (hi - lo)
    for w in words:
        x0, _, x1, _ = w["b"]
        for x in range(max(x0, lo), min(x1, hi)):
            cov[x - lo] += 1
    if not cov:
        return width // 2
    mid = len(cov) // 2
    return lo + min(range(len(cov)), key=lambda i: (cov[i], abs(i - mid)))


def lines_of(words):
    """Group by tesseract's line id, order by height on the page."""
    by = {}
    for w in words:
        by.setdefault(w["l"], []).append(w)
    lines = [(sum((w["b"][1] + w["b"][3]) / 2 for w in ws) / len(ws),
              sorted(ws, key=lambda w: w["b"][0])) for ws in by.values()]
    lines.sort(key=lambda t: t[0])
    return [ws for _, ws in lines]


def layout(path):
    for (pno, width, height), words in raw_pages(path):
        words = [w for w in words if w["ch"]]
        g = gutter(words, width)
        cols = [[w for w in words if (w["b"][0] + w["b"][2]) / 2 < g],
                [w for w in words if (w["b"][0] + w["b"][2]) / 2 >= g]]
        yield {"p": pno, "W": width, "H": height, "g": g,
               "cols": [[[{"t": "".join(c[0] for c in w["ch"]), "b": w["b"], "c": w["c"], "ch": w["ch"]}
                          for w in line] for line in lines_of(col)] for col in cols]}


def build(src, out):
    tmp = out + ".tmp"
    with gzip.open(tmp, "wt", encoding="utf-8") as f:
        for p in layout(src):
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    os.replace(tmp, out)


def load_lines(path, parse_head):
    """The line stream the reader aligns, from a layout file.

    Returns (lines, heads, npages): lines = [(text, (page, col, line), glyphs)],
    glyphs one per character of text (None under the space between words),
    a glyph = (page, x0, x1, y0, y1, conf) with y0/y1 its word's. The running
    head (the words within 30 px of the top of the page's text) is taken out
    of the stream and read with `parse_head` into heads[page]."""
    lines, heads, npages = [], {}, 0
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for raw in f:
            p = json.loads(raw)
            npages = max(npages, p["p"] + 1)
            words = [w for c in p["cols"] for ln in c for w in ln]
            if not words:
                continue
            real = [w for w in words if len(w["t"]) > 1 or w["t"].isalpha()] or words
            band = min((w["b"][1] + w["b"][3]) / 2 for w in real) + 30
            head = sorted((w for w in words if (w["b"][1] + w["b"][3]) / 2 < band), key=lambda w: w["b"][0])
            h = parse_head(" ".join(w["t"] for w in head))
            if h:
                heads[p["p"]] = h
            for ci, col in enumerate(p["cols"]):
                for li, ln in enumerate(col):
                    if all((w["b"][1] + w["b"][3]) / 2 < band for w in ln):
                        continue
                    text, glyphs = "", []
                    for w in ln:
                        if text:
                            text += " "
                            glyphs.append(None)
                        for c, x0, x1, conf in w["ch"]:
                            for ch in c:
                                text += ch
                                glyphs.append((p["p"], x0, x1, w["b"][1], w["b"][3], conf))
                    lines.append((text, (p["p"], ci, li), glyphs))
    return lines, heads, npages


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
