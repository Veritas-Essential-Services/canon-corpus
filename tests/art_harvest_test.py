#!/usr/bin/env python3
# prov: 2026-11-03 claude-opus-5-5 drafted
"""Offline checks for pipeline/art_harvest.py: a made-up Gutenberg HTML zip, built in memory."""
import io
import json
import os
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import art_harvest as A  # noqa: E402
from PIL import Image  # noqa: E402

FAILS = []


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def png(w, h, shade=0):
    im = Image.new("RGB", (w, h), (255, 255, 255))
    for x in range(w):
        for y in range(h):
            if (x * 7 + y * 3 + shade) % 11 < 5:
                im.putpixel((x, y), (0, 0, 0))
    b = io.BytesIO()
    im.save(b, "PNG")
    return b.getvalue()


HTML = """<html><body>
<section id="pg-header"><img src="images/pglogo.png" alt="logo"><p>The Project Gutenberg eBook of Test, 1999 release</p></section>
<h1>THE TEST BOOK</h1>
<p>NEW YORK: 1901.</p>
<span class="pagenum"><a id="page_1">{1}</a></span>
<h2><img src="images/head.png" alt="Chapter One."></h2>
<p><span class="dropcap">O</span>NCE upon a time there was a test.</p>
<div class="figcenter"><img src="images/plate1.png" alt="[Illustration]"><p class="caption">The hero sets out</p></div>
<p>The story goes on, past the picture <img src="images/brand.png" alt="brand"> and a symbol.</p>
<p><a href="images/plate1.png"><img src="images/enlarge.png" alt="[Enlarge]"></a></p>
<div><img src="images/band.png"></div>
<p>More words before the end of the chapter.</p>
<div><img src="images/tail.png"></div>
<span class="pagenum"><a id="page_2">{2}</a></span>
<h2>Chapter Two.</h2>
<p><img src="images/drop_t.png" alt="T">HE second chapter opens with a picture letter.</p>
<div><img src="images/band.png"></div>
<h2>Chapter Three.</h2>
<div><img src="images/band.png"></div>
<p>The end.</p>
<section id="pg-footer"><p>End of the Project Gutenberg eBook, 2004</p></section>
</body></html>"""


def make_zip(path, html):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("pg1-images.html", html)
        z.writestr("images/head.png", png(400, 120, 1))
        z.writestr("images/plate1.png", png(300, 400, 2))
        z.writestr("images/brand.png", png(20, 20, 3))
        z.writestr("images/enlarge.png", png(40, 20, 4))
        z.writestr("images/band.png", png(400, 40, 5))
        z.writestr("images/tail.png", png(60, 50, 6))
        z.writestr("images/drop_t.png", png(80, 80, 7))
        z.writestr("images/pglogo.png", png(50, 50, 8))


with tempfile.TemporaryDirectory() as tmp:
    zp = os.path.join(tmp, "pg1-h.zip")
    make_zip(zp, HTML)
    (rows, summ), how = A.harvest("test-book", 1, "The Test Book", None, zp)
    by = {}
    for r in rows:
        by.setdefault(r.get("src") or "type", []).append(r)
    print(json.dumps(summ["kinds"]))

    check("boilerplate images are left out", "images/pglogo.png" not in by)
    check("Gutenberg's enlarge button is left out, and counted", "images/enlarge.png" not in by and summ["icons_skipped"] == 1)
    check("a span drop cap is an initial with its letter and word",
          by["type"][0]["kind"] == "initial" and by["type"][0]["letter"] == "O" and by["type"][0]["word"] == "ONCE")
    check("a type initial's address does not depend on the pictures before it", by["type"][0]["citation"] == "pg1:type-initial#1")
    t = by["images/drop_t.png"][0]
    check("an image whose alt is one letter is an initial", t["kind"] == "initial" and t["letter"] == "T")
    check("the text after a picture initial is recorded as Gutenberg has it", t["word"] == "HE")
    check("html_has_letter is false when the text lost the letter", t["html_has_letter"] is False)
    h = by["images/head.png"][0]
    check("a picture inside a heading is placed in-heading", h["place"] == "in-heading")
    check("a heading set as a picture takes its alt as its text", by["images/plate1.png"][0]["heading"] == "Chapter One.")
    p = by["images/plate1.png"][0]
    check("a figure's caption is read", p.get("caption") == "The hero sets out")
    check("the caption is not part of the anchor text", "hero sets out" not in p["before_quote"])
    check("a placeholder alt is dropped", "alt" not in p)
    check("the printed page comes from the page anchor", p["printed_page"] == "1" and t["printed_page"] == "2")
    check("a 20 px symbol is a glyph, not art", by["images/brand.png"][0]["kind"] == "glyph")
    check("an image placed three times is an ornament", all(r["kind"] == "ornament" for r in by["images/band.png"]))
    check("each placement has its own address", [r["citation"] for r in by["images/band.png"]] ==
          ["pg1:images/band.png#1", "pg1:images/band.png#2", "pg1:images/band.png#3"])
    tail = by["images/tail.png"][0]
    check("a small image just before a heading is a tailpiece, at the end of its section",
          tail["kind"] == "tailpiece" and tail["place"] == "end-of-section")
    check("the anchor quote is the words that follow", p["before_quote"].startswith("The story goes on"))
    check("pixel size, sha256 and dHash come from the zip", p["px"] == [300, 400] and len(p["sha256"]) == 16 and len(p["dhash"]) == 16)
    check("rows are in reading order", [r["n"] for r in rows] == list(range(1, len(rows) + 1)))
    check("rights: a title-page year before 1931 makes it US public domain, the transcriber's 1999 does not count",
          summ["rights"]["pd_us"] is True and "1901" in summ["rights"]["basis"])

    (rows2, _), _ = A.harvest("test-book", 1, "The Test Book", None, zp)
    check("the harvest is deterministic", rows == rows2)

    zc = os.path.join(tmp, "pg2-h.zip")
    make_zip(zc, HTML.replace("<h1>", "<p>*** This is a COPYRIGHTED Project Gutenberg eBook ***</p><h1>"))
    res, how = A.harvest("bad", 2, "Bad", 1900, zc)
    check("a COPYRIGHTED Gutenberg file is refused", res is None and how.startswith("REFUSED"))

    zl = os.path.join(tmp, "pg3-h.zip")
    make_zip(zl, HTML.replace("NEW YORK: 1901.", "NEW YORK: 1937."))
    (_, s3), _ = A.harvest("late", 3, "Late", 1905, zl)
    check("a later printing on the title page sends the book to a rights check", s3["rights"]["pd_us"] == "check")

check("dHash distance is a bit count", A.ham("ffff000000000000", "fff0000000000000") == 4)
check("shape test: same aspect within 25%", A._same_shape({"px": [100, 50]}, {"px": [110, 50]})
      and not A._same_shape({"px": [100, 50]}, {"px": [50, 100]}))

print(f"\n{'ALL OK' if not FAILS else str(len(FAILS)) + ' FAILED'}")
sys.exit(1 if FAILS else 0)
