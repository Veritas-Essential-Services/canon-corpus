#!/usr/bin/env python3
# prov: 2026-10-28 claude-opus-5-5 drafted
# fable_review: pending
"""Offline checks for unscanner/restore.py: paper to pure white, ink and pictures kept, blank pages
blank. Pages are drawn here (uneven cream paper, show-through, a speck, text bars, a grey picture), so
no scan is needed. The PDF check runs only if tesseract and pikepdf are installed.
Run: python3 tests/restore_test.py
"""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import numpy as np                                      # noqa: E402
from PIL import Image                                   # noqa: E402

from unscanner import restore as R                      # noqa: E402

PASS, FAIL = 0, []


def check(name, ok):
    global PASS
    if ok:
        PASS += 1
    else:
        FAIL.append(name)
        print("FAIL", name)


def paper(w=900, h=1300, seed=1):
    """Cream paper, darker towards the gutter, with grain: RGB uint8."""
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 1, w)[None, :]
    base = 236 - 22 * (1 - x) ** 6                       # gutter shadow on the left
    g = base + rng.normal(0, 2.0, (h, w))
    rgb = np.stack([g + 15, g, g - 30], 2)               # cream: red high, blue low
    return np.clip(rgb, 0, 255).astype(np.uint8)


def draw_page(tmp):
    a = paper()
    for y in range(200, 700, 40):                       # "text": dark bars of letter height
        for x in range(120, 760, 70):
            a[y:y + 18, x:x + 50] = 30
    pic = np.tile(np.linspace(40, 200, 400)[None, :], (300, 1))    # a grey picture: a ramp
    a[800:1100, 250:650] = pic[:, :, None].astype(np.uint8)
    a[1200, 850] = 20                                    # a speck in the margin
    a[400:420, 0:6] = 0                                  # tape at the scan's edge
    p = os.path.join(tmp, "page.png")
    Image.fromarray(a).save(p)
    return p


def draw_blank(tmp):
    a = paper(seed=2).astype(np.int16)
    for y in range(200, 1100, 40):                       # show-through: faint text from the other side
        a[y:y + 18, 150:750] -= 18
    p = os.path.join(tmp, "blank.png")
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(p)
    return p


def main():
    tmp = tempfile.mkdtemp()
    try:
        src = draw_page(tmp)
        out = os.path.join(tmp, "out.png")
        rep = R.restore_page(src, out)
        b = np.asarray(Image.open(out))
        check("grey, not colour, for black ink on cream", b.ndim == 2 and rep["colour"] is False)
        check("margins pure white", (b[:150, :] == 255).all() and (b[:, 830:] == 255).all())
        check("gutter shadow gone between the lines", (b[225:235, 120:760] == 255).mean() > 0.99)
        check("text stays dark", b[205:213, 125:165].mean() < 40)
        check("picture keeps its greys", 60 < b[900:1000, 300:600].mean() < 200
              and len(np.unique(b[900:1000, 300:600])) > 30)
        check("speck removed", b[1195:1205, 845:855].min() == 255 and rep["specks"] >= 1)
        check("edge tape removed", (b[395:425, 0:10] == 255).all() and rep["edge_artefacts"] >= 1)
        check("ink drops", rep["ink_after"] < rep["ink_before"])
        check("written atomically (no .part left)", not os.path.exists(out + ".part"))

        rep = R.restore_page(draw_blank(tmp), os.path.join(tmp, "blank-out.png"))
        bb = np.asarray(Image.open(os.path.join(tmp, "blank-out.png")))
        check("show-through page is blank", rep["kind"] == "blank" and (bb == 255).all())

        # deskew: rotate the page 1.5 degrees and measure it back
        g = np.asarray(Image.open(out))
        tilted = R.rotate(g, 1.5) if R.cv2 is not None else g
        check("skew measured", abs(R.skew_angle(tilted) + 1.5) <= 0.15)

        # coloured ink is kept as colour
        a = paper()
        a[300:500, 200:600] = [190, 30, 30]
        cp = os.path.join(tmp, "red.png")
        Image.fromarray(a).save(cp)
        rep = R.restore_page(cp, os.path.join(tmp, "red-out.png"))
        check("red ink kept as colour", rep["colour"] is True)

        try:
            import pikepdf  # noqa: F401
            have_pdf = shutil.which("tesseract") is not None
        except ImportError:
            have_pdf = False
        if have_pdf:
            pdf = os.path.join(tmp, "book.pdf")
            notes = R.build_pdf([out], pdf, os.path.join(tmp, "ocr"))
            check("pdf written", os.path.getsize(pdf) > 0)
            check("the ramp is one picture", len(notes[0]["pictures"]) == 1)
        else:
            print("skip: pdf check (needs tesseract and pikepdf)")
    finally:
        shutil.rmtree(tmp)
    print(f"{PASS} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
