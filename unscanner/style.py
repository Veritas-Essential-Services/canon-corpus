"""Italic and small capitals, read from the ink (tesseract 5 does not report either).

ITALIC. Roman letters stand upright, so a roman word's ink, summed down each column, piles into sharp
peaks at the stems. An italic word's stems lean; its columns blur. Shear the word back by each slant in
turn and keep the slant that makes the columns sharpest: a roman word is sharpest near 0, an italic one
near 0.2 (about 11 degrees). A word is italic when the best slant is at least 0.12 AND it beats upright
by at least 6% -- the margin keeps a roman word with one sloped letter (an "A", a "v") roman.

SMALL CAPITALS. On a page, the lower-case x-height Xh is the median ink height of words made only of
x-height letters (a c e m n o r s u v w x z); the capital height Ch is the median of words in capitals.
A word the OCR read in capitals whose letters after the first stand nearer Xh than Ch is set in small
capitals. If its first letter stands at Ch, it is a capital followed by small capitals ("Ulysses",
which the OCR reads ULYSSES); otherwise all small capitals.

Both are measurements, so both are reported with their counts, and both can be wrong on a dirty scan.
"""
import re
import statistics

import numpy as np

SLANTS = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35]
XLET = re.compile(r"^[acemnorsuvwxz]{2,}$")
CAPW = re.compile(r"^[A-PR-Z]{2,}$")     # no Q (its tail descends)


def _binarize(a):
    lo, hi = np.percentile(a, 5), np.percentile(a, 95)
    return a < (lo + hi) / 2


def _crop(page, bbox):
    x0, y0, x1, y1 = bbox
    return page[max(0, y0):y1, max(0, x0):x1]


def slant(crop_bool):
    """-> (best slant, gain of best over upright). crop_bool: True where ink."""
    ys, xs = np.nonzero(crop_bool)
    if len(xs) < 30:
        return 0.0, 0.0
    yb = crop_bool.shape[0]
    scores = []
    for s in SLANTS:
        xp = np.round(xs - s * (yb - ys)).astype(int)
        xp -= xp.min()
        col = np.bincount(xp)
        scores.append(float((col.astype(np.float64) ** 2).sum()))
    i = int(np.argmax(scores))
    return SLANTS[i], scores[i] / scores[0] - 1.0 if scores[0] else 0.0


def ink_height(crop_bool):
    rows = np.nonzero(crop_bool.any(axis=1))[0]
    return int(rows[-1] - rows[0] + 1) if len(rows) else 0


def page_heights(page, words):
    xh = [ink_height(_binarize(_crop(page, w["bbox"]))) for w in words if XLET.match(w["t"])]
    ch = [ink_height(_binarize(_crop(page, w["bbox"]))) for w in words if CAPW.match(w["t"])]
    return (statistics.median(xh) if len(xh) >= 5 else None,
            statistics.median(ch) if len(ch) >= 2 else None)


def mark_page(page, lines):
    """Set w["it"] and w["sc"] on every word of a page. page: 2-D grey array. Returns counts."""
    words = [w for ln in lines for w in ln["words"]]
    xh, ch = page_heights(page, words)
    n_it = n_sc = 0
    for w in words:
        c = _crop(page, w["bbox"])
        if c.size == 0:
            continue
        b = _binarize(c)
        letters = re.sub(r"[^A-Za-z]", "", w["t"])
        if len(letters) >= 3:
            s, gain = slant(b)
            if s >= 0.12 and gain >= 0.06:
                w["it"] = True
                n_it += 1
        if xh and ch and ch > 1.2 * xh and CAPW.match(letters or "-") and len(letters) >= 2:
            k = max(1, b.shape[1] // len(letters))
            rest = ink_height(b[:, k:])
            if rest and abs(rest - xh) < abs(rest - ch):
                first = ink_height(b[:, :k])
                w["sc"] = "cap" if abs(first - ch) < abs(first - xh) else "all"
                n_sc += 1
    return {"italic": n_it, "smallcaps": n_sc, "x_height": xh, "cap_height": ch}


def display(w):
    """A word as a reader should see it in plain text: small capitals in their real case."""
    t = w["t"]
    if w.get("sc") == "cap":
        out, first = [], True
        for ch in t:
            out.append(ch if (first or not ch.isalpha()) else ch.lower())
            first = first and not ch.isalpha()
        return "".join(out)
    if w.get("sc") == "all":
        return t.lower()
    return t
