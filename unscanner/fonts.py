"""Font matching: which open typeface is closest to the one the book was printed in?

The design note named this the real unknown of faithful re-typesetting. The method is plain and
checkable. Take words the OCR read with high confidence. Cut each from the scan. Set the same word in
every candidate font, crop it to its ink, and stretch it onto the scan's box. Score two things:

  - SHAPE: the correlation of the two images once both are blurred a little (so a one-pixel
    misregistration does not count as a different letter);
  - WIDTH: a typeface's character is mostly in how wide it sets a word at a given height, so a set
    word whose width-to-height ratio differs from the scan's is penalised by exp(-3 |log ratio|)
    BEFORE it is stretched (stretching would otherwise hide exactly the difference we are measuring).

A font's score is the mean over the sample words; the report lists every candidate, best first, with the
point size the match implies. Every candidate is an OFL font from the Fontsource npm mirror of Google
Fonts, pinned by version, so the matched font can be embedded in the HTML and EPUB it produces. A best
match is the closest of the candidates, not proof of the original face: the report says so.
"""
import io
import json
import math
import os
import re
import subprocess
import tarfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

VERSION = "5.3.0"
# family: (fontsource package, why it is a candidate)
CANDIDATES = {
    "Libre Caslon Text": ("libre-caslon-text", "Caslon: the default English book face to 1900"),
    "EB Garamond": ("eb-garamond", "Garamond: old style, French"),
    "Sorts Mill Goudy": ("sorts-mill-goudy", "Goudy Old Style (1915)"),
    "Goudy Bookletter 1911": ("goudy-bookletter-1911", "Goudy's Kennerley (1911)"),
    "Old Standard TT": ("old-standard-tt", "the late-19th-c. 'modern' book face"),
    "Libre Baskerville": ("libre-baskerville", "Baskerville: transitional"),
    "Crimson Text": ("crimson-text", "old style, after Minion/Garamond"),
    "Cormorant Garamond": ("cormorant-garamond", "Garamond, display-leaning"),
    "IM Fell English": ("im-fell-english", "Fell types (17th c.)"),
    "Linden Hill": ("linden-hill", "Goudy Deepdene"),
    "Fanwood Text": ("fanwood-text", "Fournier"),
    "Libre Bodoni": ("libre-bodoni", "Bodoni: modern"),
    "Gelasio": ("gelasio", "Georgia metrics; a 19th-c. 'Scotch' feel"),
    "Spectral": ("spectral", "contemporary book face (control)"),
}
WORD = re.compile(r"^[A-Za-z]{4,12}$")


def _pkg_files(cache, pkg):
    d = os.path.join(cache, pkg)
    if os.path.isdir(d) and os.listdir(d):
        return d
    os.makedirs(cache, exist_ok=True)
    tgz = subprocess.run(["npm", "pack", f"@fontsource/{pkg}@{VERSION}", "--silent",
                          "--pack-destination", cache], capture_output=True, text=True)
    name = (tgz.stdout.strip().splitlines() or [""])[-1]
    path = os.path.join(cache, name)
    if tgz.returncode or not os.path.exists(path):
        return None
    tmp = d + ".part"
    os.makedirs(tmp, exist_ok=True)
    with tarfile.open(path) as t:
        for m in t.getmembers():
            base = os.path.basename(m.name)
            if re.match(rf"{re.escape(pkg)}-latin-(400|700)-(normal|italic)\.woff2?$", base) or base == "LICENSE":
                open(os.path.join(tmp, base), "wb").write(t.extractfile(m).read())
    os.remove(path)
    os.replace(tmp, d)
    return d


def fetch_fonts(cache, only=None):
    """-> {family: {"dir", "regular", "italic"|None, "pkg", "why"}} for every candidate that fetched."""
    out = {}
    for fam, (pkg, why) in CANDIDATES.items():
        if only and fam not in only:
            continue
        d = _pkg_files(cache, pkg)
        if not d:
            continue
        reg = os.path.join(d, f"{pkg}-latin-400-normal.woff")
        ita = os.path.join(d, f"{pkg}-latin-400-italic.woff")
        if os.path.exists(reg):
            out[fam] = {"dir": d, "regular": reg, "italic": ita if os.path.exists(ita) else None,
                        "pkg": pkg, "version": VERSION, "why": why}
    return out


def _ink(a):
    lo, hi = np.percentile(a, 5), np.percentile(a, 95)
    return a < (lo + hi) / 2


def _tight(b):
    rows, cols = np.nonzero(b.any(axis=1))[0], np.nonzero(b.any(axis=0))[0]
    if not len(rows) or not len(cols):
        return None
    return b[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]


def render_word(font_path, text, px=100):
    f = ImageFont.truetype(font_path, px)
    x0, y0, x1, y1 = f.getbbox(text)
    im = Image.new("L", (x1 - x0 + 20, y1 - y0 + 20), 255)
    ImageDraw.Draw(im).text((10 - x0, 10 - y0), text, font=f, fill=0)
    return _tight(np.asarray(im) < 128)


def _blur(b, r=1.5):
    im = Image.fromarray((b * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r)), dtype=np.float64)


def score_word(obs, ren):
    """obs, ren: tight boolean ink arrays. -> (score, width ratio)."""
    if obs is None or ren is None or obs.shape[0] < 8 or obs.shape[1] < 8:
        return None, None
    ratio = (ren.shape[1] / ren.shape[0]) / (obs.shape[1] / obs.shape[0])
    im = Image.fromarray((ren * 255).astype(np.uint8)).resize((obs.shape[1], obs.shape[0]), Image.BILINEAR)
    r = _blur(np.asarray(im) > 127)
    o = _blur(obs)
    r -= r.mean(); o -= o.mean()
    den = math.sqrt((r * r).sum() * (o * o).sum())
    corr = float((r * o).sum() / den) if den else 0.0
    return corr * math.exp(-3 * abs(math.log(ratio))), ratio


def sample_words(pages, images, limit=80):
    """[(text, tight ink array, ocr px height)] from high-confidence plain words on text pages."""
    out = []
    for p in pages:
        if p.get("kind") != "text" or p["n"] not in images:
            continue
        a = np.asarray(Image.open(images[p["n"]]).convert("L"))
        body = [ln for b in p.get("blocks", []) if b["type"] == "para" for ln in b["lines"]] \
            if "blocks" in p else p["lines"]          # body text only: not headings, not front matter
        for ln in body:
            for w in ln["words"]:
                if w["conf"] >= 92 and WORD.match(w["t"]) and not w.get("it") and not w.get("sc"):
                    x0, y0, x1, y1 = w["bbox"]
                    t = _tight(_ink(a[y0:y1, x0:x1]))
                    if t is not None:
                        out.append((w["t"], t))
                if len(out) >= limit:
                    return out
    return out


def match(words, fonts, dpi=300):
    """-> ranked [{"family", "score", "width_ratio", "pt", "n"}], best first."""
    rows = []
    for fam, info in fonts.items():
        scores, ratios, sizes = [], [], []
        for text, obs in words:
            ren = render_word(info["regular"], text)
            s, r = score_word(obs, ren)
            if s is None:
                continue
            scores.append(s); ratios.append(r)
            sizes.append(100 * obs.shape[0] / ren.shape[0])     # px per em on the scan
        if scores:
            rows.append({"family": fam, "score": round(float(np.mean(scores)), 4),
                         "width_ratio": round(float(np.median(ratios)), 3),
                         "pt": round(float(np.median(sizes)) * 72 / dpi, 1), "n": len(scores),
                         "pkg": info["pkg"], "why": info["why"]})
    rows.sort(key=lambda r: -r["score"])
    return rows


def css_face(info, family, embed_dir=None, rel=""):
    """@font-face rules for the matched family (woff2 preferred), copying files into embed_dir."""
    rules = []
    d = info["dir"]
    for style in ("normal", "italic"):
        for wt in ("400", "700"):
            base = f"{info['pkg']}-latin-{wt}-{style}"
            for ext, fmt in (("woff2", "woff2"), ("woff", "woff")):
                src = os.path.join(d, f"{base}.{ext}")
                if os.path.exists(src):
                    if embed_dir:
                        os.makedirs(embed_dir, exist_ok=True)
                        open(os.path.join(embed_dir, f"{base}.{ext}"), "wb").write(open(src, "rb").read())
                    rules.append(f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{wt};"
                                 f"src:url('{rel}{base}.{ext}') format('{fmt}');}}")
                    break
    return "\n".join(rules)
