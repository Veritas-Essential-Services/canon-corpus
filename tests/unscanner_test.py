#!/usr/bin/env python3
# prov: 2026-10-16 claude-opus-5-5 drafted
# fable_review: pending
"""Offline checks for the Unscanner (unscanner/). No network, no scan needed: pages are built here
from word boxes, and the image checks draw their own ink. The end-to-end check runs only if tesseract
is installed, on a page this test sets in a font and then reads back.  Run: python3 tests/unscanner_test.py
"""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import numpy as np                                      # noqa: E402
from PIL import Image, ImageDraw, ImageFont             # noqa: E402

from unscanner import book as BK                        # noqa: E402
from unscanner import collate as C                      # noqa: E402
from unscanner import emit as E                         # noqa: E402
from unscanner import fonts as F                        # noqa: E402
from unscanner import images as I                       # noqa: E402
from unscanner import layout as L                       # noqa: E402
from unscanner import scan as S                         # noqa: E402
from unscanner import style as ST                       # noqa: E402

PASS, FAIL = 0, []


def check(label, cond):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label)


W, H, B, LM, RM = 1200, 2000, 40, 100, 1100


def line(text, x0, y, x1=None, size=B, conf=95):
    ws = text.split()
    x1 = x1 if x1 is not None else min(RM, x0 + 22 * len(text))
    total = sum(len(w) for w in ws) + len(ws) - 1
    out, x = [], x0
    for w in ws:
        wd = (x1 - x0) * len(w) / total
        out.append({"t": w, "bbox": [int(x), y, int(x + wd), y + size - 8], "conf": conf})
        x += wd + (x1 - x0) / total
    return {"bbox": [x0, y, x1, y + size], "x_size": float(size), "baseline": [0, -8], "kind": "ocr_line",
            "words": out}


def page(n, lines, kind="text"):
    return {"n": n, "w": W, "h": H, "lines": lines, "kind": kind, "figures": []}


FULL = "the quick brown fox jumps over the lazy dog and runs"

# ---------------------------------------------------------------- hOCR parse
HOCR = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"><body>
<div class='ocr_page' title='image "x.png"; bbox 0 0 1230 2055; ppageno 0'>
 <span class='ocr_line' title="bbox 179 148 1173 186; baseline 0.001 -2; x_size 48.3; x_descenders 12">
  <span class='ocrx_word' title='bbox 179 148 285 185; x_wconf 95'>THE</span>
  <span class='ocrx_word' title='bbox 317 148 554 185; x_wconf 41'>CYC@OPS</span>
  <span class='ocrx_word' title='bbox 600 148 610 185; x_wconf 0'> </span>
 </span>
 <span class='ocr_line' title="bbox 1 1 2 2; x_size 3"><span class='ocrx_word' title='bbox 1 1 2 2; x_wconf 0'></span></span>
</div></body></html>"""
with tempfile.NamedTemporaryFile("w", suffix=".hocr", delete=False, encoding="utf-8") as fh:
    fh.write(HOCR)
hp = S.parse_hocr(fh.name)
os.unlink(fh.name)
check("hocr: page size, one line, empty words and the wordless line dropped",
      (hp["w"], hp["h"], len(hp["lines"]), [w["t"] for w in hp["lines"][0]["words"]]) == (1230, 2055, 1, ["THE", "CYC@OPS"]))
check("hocr: boxes, confidences and x_size read", hp["lines"][0]["words"][1]["conf"] == 41
      and hp["lines"][0]["words"][0]["bbox"] == [179, 148, 285, 185] and hp["lines"][0]["x_size"] == 48.3)

# ---------------------------------------------------------------- furniture
def body(y0, n=6):
    return [line(FULL, LM, y0 + i * 50, RM) for i in range(n)]


pgs = [
    page(10, [line("12 THE BOOK OF TALES", LM, 100, 700)] + body(200)),
    page(11, [line("THE FIRST TALE", 400, 100, 800)] + body(200) + [line("13", 580, 1850, 620)]),
    page(12, [line("THE BOOK OF TALES", LM, 100, 700)] + body(200) + [line("=o", 580, 1850, 620, conf=30)]),
    page(13, [line("THE FIRST TALE", 400, 100, 800)] + body(200) + [line("15", 580, 1850, 620)]),
    page(14, [line("THe B0OK OF TALE5", LM, 100, 700, conf=40)] + body(200)),
    page(15, [line("CHAPTER II", 500, 400, 700)] + body(600)),
]
fu = L.find_furniture(pgs)
check("furniture: a top line with a number at its head gives the folio and is dropped",
      fu[10]["label"] == "12" and 0 in fu[10]["drop"] and fu[10]["head"] == "THE BOOK OF TALES")
check("furniture: a recurring capital top line is a running head", fu[11]["head"] == "THE FIRST TALE")
check("furniture: a centred foot number is the folio", fu[11]["label"] == "13" and len(pgs[1]["lines"]) - 1 in fu[11]["drop"])
check("furniture: an unreadable folio is inferred when both neighbours agree, and flagged",
      fu[12]["label"] == "14" and fu[12]["inferred"] and len(pgs[2]["lines"]) - 1 in fu[12]["drop"])
check("furniture: a mangled running head still counts (similarity), so it is not text",
      fu[14]["head"] is not None and 0 in fu[14]["drop"])
check("furniture: a CHAPTER line is never a running head", fu[15]["head"] is None and not fu[15]["drop"])

seq = [page(30 + k, body(200) + [line(str(lab), 580, 1850, 620)]) for k, lab in enumerate([24, 25, 20, 27, 28])]
fs = L.find_furniture(seq)
check("furniture: a folio read wrongly ('26' read '20') is corrected by the sequence on both sides, and flagged",
      fs[32]["label"] == "26" and fs[32]["inferred"] == "corrected" and fs[31]["label"] == "25" and not fs[31]["inferred"])

# ---------------------------------------------------------------- blocks
pb = page(20, [
    line(FULL, LM, 200, RM),                                  # continues the last page's paragraph
    line("end of it.", LM, 250, 400),
    line(FULL, LM + 40, 300, RM),                             # indent: new paragraph
    line(FULL, LM, 350, RM),
    line("Sing, O Muse, of the man", LM + 200, 400, 700),     # deep indent: verse
    line("who wandered far and long", LM + 200, 450, 720),
    line(FULL, LM, 500, RM),
    line("CHAPTER III", 500, 600, 700),
    line("THE CAVE", 520, 660, 680),
    line(FULL, LM, 760, RM),                                   # first line after a heading: a paragraph
    line("BIG WORDS HERE", 300, 820, 900, size=int(B * 1.4)),
])
bl = L.build_blocks(pb, B, LM, RM, set())
check("blocks: types in order", [b["type"] for b in bl] == ["para", "para", "quote", "para", "heading", "para", "heading"])
check("blocks: the unindented first line continues the previous page", bl[0]["cont"] and len(bl[0]["lines"]) == 2)
check("blocks: an indent starts a paragraph that is not a continuation", not bl[1]["cont"] and len(bl[1]["lines"]) == 2)
check("blocks: verse keeps its two lines together", len(bl[2]["lines"]) == 2)
check("blocks: CHAPTER and its centred capital title are one heading block", len(bl[4]["lines"]) == 2)

# ---------------------------------------------------------------- hyphens
ev = [page(1, [line("a well-known man and a tomorrow", LM, 100, RM), line("good and fine words", LM, 150, RM)])]
hy, wh = L.hyphen_evidence(ev)
log = L.new_log()
toks = L.join_tokens([[{"t": "a"}, {"t": "well-"}], [{"t": "known"}, {"t": "man"}], [{"t": "to-"}], [{"t": "morrow"}],
                      [{"t": "un-"}], [{"t": "heard"}], [{"t": "THE"}, {"t": "END-"}], [{"t": "Of"}]], hy, wh, log)
check("hyphens: the book's own compound keeps its hyphen; a printed whole word is joined; caps after is left",
      L.tokens_text(toks) == "a well-known man tomorrow unheard THE END- Of")
check("hyphens: counted, and the unattested join listed for review",
      (log["kept"], log["joined"], log["joined_unattested"], log["doubtful"]) == (1, 1, 1, ["un-heard"]))

# ---------------------------------------------------------------- assemble: chapters, half-titles, units
def tp(n, lines):
    p = page(n, lines)
    p["blocks"] = L.build_blocks(p, B, LM, RM, set())
    return p


book = [
    tp(1, [line("CONTENTS", 520, 300, 680), line("I. The Cave . . 1", LM, 400, RM)]),
    tp(2, [line("CHAPTER I", 500, 600, 700, conf=50), line("THE CAVF", 520, 660, 680, conf=40)]),     # half-title
    tp(3, [line("CHAPTER I", 500, 300, 700), line("THE CAVE", 520, 360, 680)]
       + [line(FULL, LM + 40, 450, RM), line("ended here.", LM, 500, 400), line(FULL, LM + 40, 550, RM)]),
    tp(4, [line(FULL, LM, 200, RM), line("so it went on.", LM, 250, 500)]),
    page(5, [line("HE SAW THE GIANT", 300, 1900, 900, conf=60)], kind="plate"),
    tp(6, [line("and on.", LM, 200, 300), line("THE CAVE", 520, 300, 680), line(FULL, LM + 40, 400, RM)]),
    tp(7, [line("CHAPTER. II", 500, 300, 700), line("THE END OF ALL", 400, 360, 800), line(FULL, LM + 40, 450, RM),
           line("THE END OF TROY", 420, 600, 780), line(FULL, LM + 40, 700, RM)]),
]
book[4]["figures"] = [[100, 100, 1100, 1800]]
front, divs, _ = BK.assemble(book, "t", extra_heads=("THE END OF TROY",))
check("assemble: front matter before the first CHAPTER; chapters once each; the better reading of a title wins",
      [d["label"] for d in divs] == ["Chapter I: The Cave", "Chapter II: The End of All", "The End of Troy"]
      and any(s["type"] == "heading" and s["text"] == "CONTENTS" for s in front))
u = BK.units(divs, "t")
check("assemble: a paragraph runs across a page and across a plate; the title reprinted mid-chapter is dropped",
      [x["id"] for x in u] == ["t:ch1.1", "t:ch1.2", "t:ch1.3", "t:ch2.1", "t:the-end-of-troy.1"]
      and u[1]["pages"] == [3, 4, 6] and u[1]["text"].endswith("so it went on. and on."))
check("assemble: the plate stays in the reading stream (for the editions), not in the units",
      any(s["type"] == "plate" for s in divs[0]["items"]) and all("HE SAW" not in x["text"] for x in u))
check("assemble: a 'CHAPTER.' with a stray stop is still a chapter", divs[1]["key"] == "ch2")

# ---------------------------------------------------------------- roman numerals
check("roman: I, iv, XIV, XXIII, l->I, digits", [BK.roman(x) for x in ("I", "iv", "XIV", "XXIII", "l", "12")] == [1, 4, 14, 23, 1, 12]
      and BK.to_roman(23) == "XXIII")

# ---------------------------------------------------------------- collation
cp = [page(1, [{"words": [{"t": "“Xow,", "conf": 40}, {"t": "said", "conf": 96}, {"t": "Athené", "conf": 60},
                          {"t": "thev", "conf": 85}, {"t": "€YCLOPS", "conf": 20}]},
               {"words": [{"t": "Now", "conf": 95}, {"t": "Now", "conf": 95}, {"t": "CYCLOPS", "conf": 95},
                          {"t": "Cyclops", "conf": 93}, {"t": "they", "conf": 95}, {"t": "they", "conf": 95}]}])]
r = C.collate(cp, "\"Now, said Athene they CYCLOPS Now Now CYCLOPS Cyclops they they")
got = [w["t"] for w in cp[0]["lines"][0]["words"]]
check("collate: an unsure, unattested word takes the witness's attested reading, keeping our punctuation and case",
      got[0] == "“Now," and got[4] == "CYCLOPS" and cp[0]["lines"][0]["words"][0]["was"] == "“Xow,")
check("collate: the witness dropping an accent is not a disagreement (Athené stays)", got[2] == "Athené")
check("collate: a word read with confidence 80+ is never overwritten, even if wrong", got[3] == "thev")
check("collate: every mend is reported", r["mended"] == 2 and r["agreement"] > 0.5)

# ---------------------------------------------------------------- images: pictures, italic, small caps
tmp = tempfile.mkdtemp()
im = Image.new("L", (W, H), 235)
d = ImageDraw.Draw(im)
d.rectangle([200, 300, 1000, 1200], fill=60)            # a picture
for k in range(10):
    d.rectangle([150 + 90 * k, 1500, 210 + 90 * k, 1530], fill=20)    # "words"
png = os.path.join(tmp, "p.png")
im.save(png)
words = [[150 + 90 * k, 1500, 210 + 90 * k, 1530] for k in range(10)]
cover, regions = I.ink_regions(png, words)
check("images: ink no word covers is found as one region of the right size",
      len(regions) == 1 and abs(regions[0][0] - 200) < 30 and abs(regions[0][3] - 1200) < 30 and cover > 0.25)
check("images: a page that is mostly picture with few words is a plate",
      L.page_kind({"lines": [line("A CAPTION", 400, 1500, 800)]}, cover) == "plate")
check("images: a page with no word read surely and no picture is blank",
      L.page_kind({"lines": [line("~", 400, 1500, 420, conf=10)]}, 0.0) == "blank")

stems = np.zeros((60, 200), bool)
for x in range(10, 190, 20):
    stems[:, x:x + 4] = True
lean = np.zeros_like(stems)
ys, xs = np.nonzero(stems)
lean[ys, np.clip(xs + ((60 - ys) * 0.2).astype(int), 0, 199)] = True
check("style: upright stems are roman, stems leaning 0.2 are italic",
      ST.slant(stems)[0] == 0.0 and ST.slant(lean)[0] >= 0.15 and ST.slant(lean)[1] >= 0.06)
check("style: small capitals shown in their real case", ST.display({"t": "ULYSSES,", "sc": "cap"}) == "Ulysses,"
      and ST.display({"t": "“ONCE", "sc": "cap"}) == "“Once" and ST.display({"t": "AND", "sc": "all"}) == "and")


# ---------------------------------------------------------------- fonts
def find_font(names):
    for n in names:
        try:
            ImageFont.truetype(n, 20)
            return n
        except OSError:
            continue
    return None


fa = find_font(["DejaVuSerif.ttf", "georgia.ttf", "LiberationSerif-Regular.ttf"])
fb = find_font(["DejaVuSans.ttf", "arial.ttf", "LiberationSans-Regular.ttf"])
if fa and fb:
    words = []
    for t in ("Ulysses", "wandered", "harbour", "giant", "shepherd", "morning"):
        f = ImageFont.truetype(fa, 56)
        x0, y0, x1, y1 = f.getbbox(t)
        img = Image.new("L", (x1 - x0 + 10, y1 - y0 + 10), 240)
        ImageDraw.Draw(img).text((5 - x0, 5 - y0), t, font=f, fill=30)
        words.append((t, F._tight(F._ink(np.asarray(img)))))
    rank = F.match(words, {"A": {"regular": fa, "pkg": "a", "why": ""}, "B": {"regular": fb, "pkg": "b", "why": ""}}, dpi=300)
    check("fonts: a page set in face A matches A over B, with the right point size",
          rank[0]["family"] == "A" and rank[0]["score"] > rank[1]["score"] + 0.05 and abs(rank[0]["pt"] - 56 * 72 / 300) < 1.5)
else:
    print("skip fonts: no two system fonts found")

# ---------------------------------------------------------------- editions
work = BK.Work(tmp, "t")
os.makedirs(work.p("img"), exist_ok=True)
os.makedirs(work.p("gray"), exist_ok=True)
Image.new("RGB", (40, 40), (200, 100, 50)).save(work.p("img", "p0005-1.jpg"))
for p in book:
    p.setdefault("label", None); p.setdefault("drop", [])
    Image.new("L", (W, H), 230).save(work.p("gray", f"{p['n']:04d}.png"))
meta = {"slug": "t", "title": "Tales & More", "author": "A. N. Author", "ident": "x", "source": "test", "rights": "PD (test)",
        "modified": "2026-10-16T00:00:00Z", "colophon": "test", "pt": 11}
imgs = {(5, 0): "p0005-1.jpg"}
rf = open(E.reflow_html(work, meta, front, divs, imgs, "Georgia", None, book), encoding="utf-8").read()
check("editions: the reflowed book has every chapter, the plate, and escaped text",
      rf.count("<h2 ") == 3 and "p0005-1.jpg" in rf and "Tales &amp; More" in rf)
ep = E.epub(work, meta, front, divs, imgs, "Georgia", None, book)
import zipfile                                           # noqa: E402
z = zipfile.ZipFile(ep)
check("editions: the EPUB has mimetype first and stored, a nav, the chapters and the plate",
      z.namelist()[0] == "mimetype" and z.getinfo("mimetype").compress_type == zipfile.ZIP_STORED
      and "OEBPS/nav.xhtml" in z.namelist() and "OEBPS/ch2.xhtml" in z.namelist() and "OEBPS/p0005-1.jpg" in z.namelist())
import xml.dom.minidom as MD                             # noqa: E402
ok = True
for n in z.namelist():
    if n.endswith((".xhtml", ".opf", ".xml")):
        try:
            MD.parseString(z.read(n))
        except Exception:
            ok = False
check("editions: every EPUB document is well-formed XML", ok)
uj = E.units_json(work, meta, BK.units(divs, "t"), book, {"confidence": {"mean_conf": 90}})
import json                                              # noqa: E402
ub = json.load(open(uj, encoding="utf-8"))
check("editions: units carry the corpus shape, scan pages, and an honesty field that says unproofread",
      set(ub["units"][0]) >= {"id", "ref", "text", "links", "pages"} and "UNPROOFREAD" in ub["scheme"]["honesty"])

# ---------------------------------------------------------------- end to end (needs tesseract)
if shutil.which("tesseract") and fa:
    f = ImageFont.truetype(fa, 44)
    im = Image.new("L", (1230, 2000), 235)
    d = ImageDraw.Draw(im)
    text = ["CHAPTER IV", "THE NEW SHIP",
            "    Now the men had made ready a ship, and", "they set the mast in its place and drew up",
            "the stones that held her to the shore.", "    Then a wind came up from the west, and",
            "the sail filled, and they went on their way."]
    y = 200
    for t in text:
        x = 615 - d.textlength(t, font=f) / 2 if t.isupper() else 120
        d.text((x, y), t, font=f, fill=25)
        y += 90 if t.isupper() else 62
    gp = os.path.join(tmp, "e2e.png")
    im.save(gp)
    hocr = S.ocr_page(gp, os.path.join(tmp, "e2e.hocr"))
    pe = S.parse_hocr(hocr)
    pe["n"] = 1
    Lm, Rm = L.measures([pe])[1]
    pe["blocks"] = L.build_blocks(pe, L.body_size([pe]), Lm, Rm, set())
    pe["kind"], pe["figures"] = "text", []
    fr, dv, _ = BK.assemble([pe], "e")
    uu = BK.units(dv, "e")
    check("end to end: a set page OCRs back into one chapter, titled, with two paragraphs",
          len(dv) == 1 and dv[0]["label"] == "Chapter IV: The New Ship" and len(uu) == 2
          and uu[1]["text"].startswith("Then a wind"))
else:
    print("skip end to end: tesseract or a serif font not found")

shutil.rmtree(tmp, ignore_errors=True)
print(f"\n{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
