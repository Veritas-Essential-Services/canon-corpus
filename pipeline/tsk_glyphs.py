#!/usr/bin/env python3
"""
tsk_glyphs.py -- read the Treasury's 3s and 8s again, from the page image.

THE PROBLEM. The Treasury's figures are an old face whose 3 has a round,
nearly closed top. Tesseract reads it as 8 -- not now and then but most of the
time: in the archive.org OCR of both scans, references containing an "8" are
found in an independent cross-reference set (OpenBible.info, used only to
measure) 53-55% of the time against 81-83% for references with neither digit.
"Ps. 83.6" in the OCR of Gen 1:1 is Ps 33:6 on the page. Two scans of the same
plates do not help: both OCRs make the same mistake.

THE FIX. Every 3 or 8 inside a reference is cropped from the page image (the
character's x-range from the OCR, its word's height), cut to its ink and
scaled to 14x20 grey levels, and a small network says 3 or 8.

ITS TEACHER IS THE BIBLE, NOT ANOTHER LIST. The labels it learns from come
from the KJV's own shape, nothing else: a reference with exactly one 3/8 in
it, where the reading as printed names no verse (Ps. 184.3; Ge. 88.5) but the
swapped digit does, labels that glyph by the swap; where the swap names no
verse but the reading does, it labels it as read. 76,828 glyphs labelled that
way across the two scans; held out, the network agrees with 99.1% of them.
OpenBible.info is never a label: it is the yardstick in README-xrefs.md.

A glyph the network is sure of (p >= 0.9 either way) is read as it says; one it
is not sure of keeps the OCR's reading and its reference is marked "unsure".

    python3 pipeline/tsk_glyphs.py --train   # relearn the model from the scans (build_xrefs.py does this)
"""
import io
import json
import os
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MODEL = os.path.join(ROOT, "data", "xrefs", "glyph-3-8.json")
FW, FH = 14, 20
SURE = 0.9
SWAP = {"3": "8", "8": "3"}


def feature(gray):
    """A crop (2-D uint8, ink dark) -> the vector the network reads, or None
    if the crop holds no clear glyph. Ink is cut to its bounding box and scaled
    to FW x FH; the box's height:width ratio is the last value."""
    from PIL import Image
    g = gray.astype(np.float32)
    lo, hi = np.percentile(g, 3), np.percentile(g, 97)
    if hi - lo < 30:
        return None
    ink = np.clip((hi - g) / (hi - lo), 0, 1)
    m = ink > 0.5
    rows = np.where(m.sum(1) > 0)[0]
    cols = np.where(m.sum(0) > 0)[0]
    if len(rows) < 6 or len(cols) < 4:
        return None
    sub = ink[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
    im = Image.fromarray((sub * 255).astype(np.uint8)).resize((FW, FH), Image.BILINEAR)
    v = np.asarray(im, dtype=np.float32).ravel() / 255.0
    return np.concatenate([v, [sub.shape[0] / max(1, sub.shape[1])]])


def page_features(zip_path, member, boxes):
    """[(glyph, feature or None)] for one page's glyph boxes."""
    from PIL import Image
    with zipfile.ZipFile(zip_path) as z:
        try:
            img = np.asarray(Image.open(io.BytesIO(z.read(member))).convert("L"))
        except KeyError:
            return [(b, None) for b in boxes]
    out = []
    for b in boxes:
        _, x0, x1, y0, y1, _ = b
        crop = img[max(0, y0 - 1):y1 + 2, max(0, x0 - 1):x1 + 2]
        out.append((b, feature(crop) if crop.size else None))
    return out


class Model:
    """A one-hidden-layer network, p(glyph is a 3)."""

    def __init__(self, d):
        self.d = d
        self.mu, self.sd = np.array(d["mu"]), np.array(d["sd"])
        self.W1, self.b1 = np.array(d["W1"]), np.array(d["b1"])
        self.W2, self.b2 = np.array(d["W2"]), float(d["b2"])

    @classmethod
    def load(cls, path=MODEL):
        with open(path, encoding="utf-8") as f:
            return cls(json.load(f))

    def p3(self, X):
        Z = (np.asarray(X) - self.mu) / self.sd
        h = np.maximum(0, Z @ self.W1 + self.b1)
        return 1 / (1 + np.exp(-(h @ self.W2 + self.b2)))


def train(X, Y, seed=0, hidden=48, epochs=60, lr=0.05):
    """Fit the network; returns (model dict, held-out report). Deterministic for
    a given seed and input order."""
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    cut = int(0.8 * len(X))
    tr, te = idx[:cut], idx[cut:]
    mu = X[tr].mean(0)
    sd = X[tr].std(0) + 1e-6
    Z = (X - mu) / sd
    W1 = rng.normal(0, 0.1, (Z.shape[1], hidden))
    b1 = np.zeros(hidden)
    W2 = rng.normal(0, 0.1, hidden)
    b2 = 0.0
    for _ in range(epochs):
        for bs in np.array_split(rng.permutation(tr), max(1, len(tr) // 256)):
            x, y = Z[bs], Y[bs]
            h = np.maximum(0, x @ W1 + b1)
            p = 1 / (1 + np.exp(-(h @ W2 + b2)))
            g = (p - y) / len(bs)
            gW2 = h.T @ g + 1e-4 * W2
            gb2 = g.sum()
            gh = np.outer(g, W2) * (h > 0)
            gW1 = x.T @ gh + 1e-4 * W1
            gb1 = gh.sum(0)
            W1 -= lr * gW1
            b1 -= lr * gb1
            W2 -= lr * gW2
            b2 -= lr * gb2
    d = {"mu": mu.tolist(), "sd": sd.tolist(), "W1": W1.tolist(), "b1": b1.tolist(),
         "W2": W2.tolist(), "b2": float(b2)}
    m = Model(d)
    p = m.p3(X[te])
    sure = (p >= SURE) | (p <= 1 - SURE)
    yt = Y[te] > 0.5
    report = {
        "labelled": int(len(X)), "labelled_as_3": int(Y.sum()), "held_out": int(len(te)),
        "held_out_agreement": round(float(((p > 0.5) == yt).mean()), 4),
        "held_out_sure_share": round(float(sure.mean()), 4),
        "held_out_sure_agreement": round(float(((p[sure] > 0.5) == yt[sure]).mean()), 4),
        "held_out_8_recall": round(float(((p <= 0.5) & ~yt).sum() / max(1, (~yt).sum())), 4),
        "seed": seed, "hidden": hidden, "epochs": epochs, "features": f"{FW}x{FH} ink + aspect",
    }
    d["report"] = report
    return d, report


def decide(p):
    """p(3) -> "3", "8" or None (unsure: keep the OCR's reading)."""
    if p >= SURE:
        return "3"
    if p <= 1 - SURE:
        return "8"
    return None
