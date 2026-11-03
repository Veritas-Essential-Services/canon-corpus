#!/usr/bin/env python3
# prov: 2026-11-03 claude-opus-5-5 drafted
# fable_review: pending
"""art_gallery.py -- a review page for the draft art catalogs (data/art/drafts/),
so Adam can look through what the harvester found without opening 500 files.

    python3 pipeline/art_gallery.py        # -> build/art-gallery/ (gitignored): index.html + sprite sheets

Reads the drafts and the cached Gutenberg zips (data/corpus/art/pg/, from
`art_harvest.py --fetch`). Thumbnails are cut from the zips and packed into one
sprite sheet per shelf, so the page needs no image host: the page and its
sheets are published together. Nothing here is catalog data; rebuild at will.
"""
import html as H
import io
import json
import os
import zipfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DRAFTS = os.path.join(ROOT, "data", "art", "drafts")
CACHE = os.path.join(ROOT, "data", "corpus", "art", "pg")
OUT = os.path.join(ROOT, "build", "art-gallery")
TH = 84          # thumbnail height in a book strip
PER_BOOK = 10    # thumbnails per book
GAP = 6


def open_zip(pg, _cache={}):
    if pg not in _cache:
        z = zipfile.ZipFile(os.path.join(CACHE, f"pg{pg}-h.zip"))
        html = max((n for n in z.namelist() if n.lower().endswith((".html", ".htm", ".xhtml"))),
                   key=lambda n: z.getinfo(n).file_size)
        _cache.clear()
        _cache[pg] = (z, os.path.dirname(html))
    return _cache[pg]


def thumb(pg, src, h, wmax):
    z, base = open_zip(pg)
    try:
        im = Image.open(io.BytesIO(z.read(os.path.normpath(os.path.join(base, H.unescape(src))).replace("\\", "/"))))
        im.load()
    except Exception:  # noqa: BLE001
        return None
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        im = bg
    im = im.convert("RGB")
    w = max(1, round(im.width * h / im.height))
    if w > wmax:
        w, h2 = wmax, max(1, round(im.height * wmax / im.width))
    else:
        h2 = h
    return im.resize((w, h2), Image.LANCZOS)


def pick(rows):
    """Up to PER_BOOK rows: one of each decorative kind first, then pictures spread through the book."""
    rows = [r for r in rows if r.get("src") and r["kind"] not in ("glyph", "cover")]
    out, seen_src = [], set()
    for kind in ("initial", "headpiece", "tailpiece", "ornament"):
        for r in rows:
            if r["kind"] == kind and r["src"] not in seen_src:
                out.append(r)
                seen_src.add(r["src"])
                break
    pics = [r for r in rows if r["kind"] == "picture" and r["src"] not in seen_src]
    room = PER_BOOK - len(out)
    if pics and room > 0:
        step = max(1, len(pics) / room)
        out += [pics[int(i * step)] for i in range(min(room, len(pics)))]
    return sorted(out, key=lambda r: r["n"])


def sheet(items, path, h):
    """items: [[(Image, meta), ...] per row] -> one JPEG; returns per-row [(x, y, w, h, meta)]."""
    W = max((sum(im.width + GAP for im, _ in row) for row in items), default=1)
    Hh = len(items) * (h + GAP)
    canvas = Image.new("RGB", (max(W, 1), max(Hh, 1)), (255, 255, 255))
    layout = []
    for i, row in enumerate(items):
        x, y, cells = 0, i * (h + GAP), []
        for im, meta in row:
            canvas.paste(im, (x, y + (h - im.height) // 2))
            cells.append([x, y, im.width, h, meta])
            x += im.width + GAP
        layout.append(cells)
    canvas.save(path, quality=62, optimize=True, progressive=True)
    return layout, canvas.size


def meta(r):
    m = {"k": r["kind"], "p": r.get("printed_page"), "h": (r.get("heading") or "")[:60]}
    if r.get("caption") or r.get("alt"):
        m["c"] = (r.get("caption") or r.get("alt"))[:90]
    if r.get("letter"):
        m["l"] = r["letter"]
    return m


def main():
    os.makedirs(os.path.join(OUT, "s"), exist_ok=True)
    index = json.load(open(os.path.join(DRAFTS, "_index.json"), encoding="utf-8"))
    books = index["books"]
    shelves = {}
    for slug, b in books.items():
        shelves.setdefault(b.get("shelf", "?"), []).append(slug)
    data = {"shelves": [], "groups": [], "initials": None, "totals": {}, "skipped": len(index["skipped"])}
    totals = {}
    all_initials = {}
    for shelf in sorted(shelves):
        rows_for_sheet, booksmeta = [], []
        for slug in sorted(shelves[shelf]):
            b = books[slug]
            for k, v in b["kinds"].items():
                totals[k] = totals.get(k, 0) + v
            rows = [json.loads(l) for l in open(os.path.join(DRAFTS, f"{slug}.jsonl"), encoding="utf-8")]
            for r in rows:
                if r["kind"] == "initial" and r.get("src") and r.get("dhash") and r["dhash"] not in all_initials:
                    all_initials[r["dhash"]] = r
            cells = []
            for r in pick(rows):
                im = thumb(r["pg"], r["src"], TH, 170)
                if im:
                    cells.append((im, meta(r)))
            rows_for_sheet.append(cells)
            booksmeta.append({"slug": slug, "title": b["title"], "pg": b["pg"], "kinds": b["kinds"],
                              "n": b["placements"], "pd": b["rights"]["pd_us"], "basis": b["rights"]["basis"],
                              "pages": b["pages_known"], "caps": b["captions"]})
        layout, size = sheet(rows_for_sheet, os.path.join(OUT, "s", f"{shelf}.jpg"), TH)
        for bm, cells in zip(booksmeta, layout):
            bm["cells"] = cells
        data["shelves"].append({"shelf": shelf, "sheet": f"s/{shelf}.jpg", "size": size, "books": booksmeta})
        print(f"  {shelf}: {len(booksmeta)} books", flush=True)
    # decorated initials, one of each design
    inits = sorted(all_initials.values(), key=lambda r: (r.get("letter") or "~", r["book"]))[:420]
    per_row, rows_i = 14, []
    for i in range(0, len(inits), per_row):
        row = []
        for r in inits[i:i + per_row]:
            im = thumb(r["pg"], r["src"], 72, 90)
            if im:
                row.append((im, {"l": r.get("letter"), "b": r["book"], "w": r.get("word")}))
        rows_i.append(row)
    lay, size = sheet(rows_i, os.path.join(OUT, "s", "_initials.jpg"), 72)
    data["initials"] = {"sheet": "s/_initials.jpg", "size": size, "cells": [c for row in lay for c in row],
                        "count": len(all_initials)}
    # ornaments shared across books
    gpath = os.path.join(DRAFTS, "_ornament-candidates.jsonl")
    rows_g, gmeta = [], []
    if os.path.exists(gpath):
        for line in open(gpath, encoding="utf-8"):
            g = json.loads(line)
            row = []
            for m in g["members"][:7]:
                pg = int(m["citation"].split(":")[0][2:])
                src = m["citation"].split(":", 1)[1].rsplit("#", 1)[0]
                im = thumb(pg, src, 64, 200)
                if im:
                    row.append((im, {"c": m["citation"]}))
            rows_g.append(row)
            gmeta.append({"group": g["group"], "books": g["books"], "members": len(g["members"])})
    lay, size = sheet(rows_g, os.path.join(OUT, "s", "_groups.jpg"), 64)
    for gm, cells in zip(gmeta, lay):
        gm["cells"] = cells
    data["groups"] = {"sheet": "s/_groups.jpg", "size": size, "rows": gmeta}
    data["totals"] = dict(sorted(totals.items(), key=lambda kv: -kv[1]))
    data["books"] = len(books)
    tpl = open(os.path.join(HERE, "art_gallery.html"), encoding="utf-8").read()
    page = tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    total = sum(os.path.getsize(os.path.join(OUT, "s", n)) for n in os.listdir(os.path.join(OUT, "s")))
    print(f"wrote {OUT}/index.html ({len(page):,} bytes) + {len(os.listdir(os.path.join(OUT, 's')))} sheets ({total:,} bytes)")


if __name__ == "__main__":
    main()
