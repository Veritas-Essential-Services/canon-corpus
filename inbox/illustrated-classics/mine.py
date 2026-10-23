# prov: 2026-10-23 claude-opus-5-5 drafted
"""Mine a whole-book scan for its pictures: plates, in-text pictures and ornaments.

Runs where the scans are (the ThinkPad). Reads what fetch_scans.py saved in
scans/<slug>/<id>/ (the JP2 zip, the OCR's djvu.xml, scandata.xml,
page_numbers.json) and writes mine/<slug>/<id>/:

  leaves.jsonl   one row per page: its viewer index n (archive.org's /page/nN),
                 jp2 file, printed page number, word count, ink, colour, a kind
                 guess (plate, text, text+art, blank), and every region of ink
                 that is not text, with its box in full-size pixels and a kind
                 guess (plate, in-text, headpiece, tailpiece, initial, border)
  sheet-plates-NN.jpg     contact sheets of the pages guessed to be plates
  sheet-ornaments-NN.jpg  contact sheets of the non-text regions on text pages
                 (small JPEGs, labelled, for a person or Claude to review)

Facts and guesses only. Nothing here is a final tag: the catalogue is made
from these rows after the sheets are looked at. Text is never stored, only
word COUNTS and boxes (house rule: no book text). Resumable per scan.

    py -3 -m pip install pillow        (once)
    py -3 mine.py <slug> [<id> ...]    (default: every scan under scans/<slug>/)
"""
import json, math, os, re, sys, zipfile
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
GRID = 96          # analysis grid: GRID cells across the page width
THUMB = 280        # contact-sheet cell size, px


def page_words(djvu_path):
    """{page file stem: (width, height, [(l, t, r, b), ...])} from the OCR's djvu.xml."""
    out = {}
    if not os.path.exists(djvu_path):
        return out
    for _, obj in ET.iterparse(djvu_path, events=("end",)):
        if obj.tag != "OBJECT":
            continue
        stem = None
        for p in obj.iter("PARAM"):
            if p.get("name") == "PAGE":
                stem = os.path.splitext(p.get("value", ""))[0]
        if stem is None:
            stem = os.path.splitext(os.path.basename(obj.get("usemap", "")))[0]
        boxes = []
        for w in obj.iter("WORD"):
            c = [int(v) for v in re.findall(r"-?\d+", w.get("coords", ""))[:4]]
            if len(c) == 4:
                l, b, r, t = c
                boxes.append((min(l, r), min(t, b), max(l, r), max(t, b)))
        out[stem] = (int(obj.get("width", 0) or 0), int(obj.get("height", 0) or 0), boxes)
        obj.clear()
    return out


def access_leaves(scandata_path):
    """Leaf numbers archive.org shows in its viewer, in order (None = all)."""
    if not os.path.exists(scandata_path):
        return None
    root = ET.parse(scandata_path).getroot()
    keep = []
    for p in root.iter("page"):
        acc = (p.findtext("addToAccessFormats") or "true").strip().lower()
        if acc == "true":
            keep.append(int(p.get("leafNum")))
    return keep or None


def printed_numbers(pn_path):
    if not os.path.exists(pn_path):
        return {}
    d = json.load(open(pn_path, encoding="utf-8"))
    return {int(p["leafNum"]): p.get("pageNumber") or None for p in d.get("pages", [])}


def ink_grid(im):
    """Grey image -> (cols, rows, cell ink fraction list, threshold)."""
    w, h = im.size
    cols = GRID
    rows = max(1, round(GRID * h / w))
    small = im.resize((cols * 4, rows * 4))
    px = list(small.tobytes())
    hist = sorted(px)
    paper = hist[int(len(hist) * 0.7)]          # the paper tone
    thr = max(40, paper - 70)
    cells = []
    for r in range(rows):
        for c in range(cols):
            n = 0
            for y in range(r * 4, r * 4 + 4):
                base = y * cols * 4 + c * 4
                n += sum(1 for v in px[base:base + 4] if v < thr)
            cells.append(n / 16)
    return cols, rows, cells, thr


def colourfulness(rgb):
    s = rgb.resize((120, max(1, round(120 * rgb.size[1] / rgb.size[0]))))
    raw = s.tobytes()
    vals = []
    for k in range(0, len(raw), 3):
        r, g, b = raw[k], raw[k + 1], raw[k + 2]
        vals.append((r - g, 0.5 * (r + g) - b))
    n = len(vals)
    mrg = sum(v[0] for v in vals) / n
    myb = sum(v[1] for v in vals) / n
    srg = math.sqrt(sum((v[0] - mrg) ** 2 for v in vals) / n)
    syb = math.sqrt(sum((v[1] - myb) ** 2 for v in vals) / n)
    return round(math.sqrt(srg ** 2 + syb ** 2) + 0.3 * math.sqrt(mrg ** 2 + myb ** 2), 1)  # Hasler-Suesstrunk


def regions(cols, rows, cells, text_cells):
    """Connected non-text ink, as cell boxes, inside a 3% margin."""
    mx, my = max(1, cols * 3 // 100), max(1, rows * 3 // 100)
    on = set()
    for r in range(my, rows - my):
        for c in range(mx, cols - mx):
            if cells[r * cols + c] > 0.06 and (r, c) not in text_cells:
                on.add((r, c))
    seen, out = set(), []
    for start in sorted(on):
        if start in seen:
            continue
        stack, comp = [start], []
        seen.add(start)
        while stack:
            r, c = stack.pop()
            comp.append((r, c))
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nb = (r + dr, c + dc)
                    if nb in on and nb not in seen:
                        seen.add(nb)
                        stack.append(nb)
        if len(comp) < 6:
            continue
        rs, cs = [p[0] for p in comp], [p[1] for p in comp]
        out.append({"cells": len(comp), "box": (min(cs), min(rs), max(cs) + 1, max(rs) + 1)})
    return out


def guess_region(box, cols, rows, text_top, text_bottom):
    l, t, r, b = box
    w, h = (r - l) / cols, (b - t) / rows
    if w > 0.6 and h > 0.55:
        return "plate"
    if h < 0.03 and w > 0.4:
        return "border"
    if text_top is not None and b <= text_top + 1:
        return "headpiece"
    if text_bottom is not None and t >= text_bottom - 1:
        return "tailpiece"
    if w < 0.16 and h < 0.12:
        return "initial" if text_top is not None and l / cols < 0.35 else "ornament"
    return "in-text"


def sheet(items, path_fmt, label):
    """items: [(PIL image, caption)] -> contact sheets of 4 x 5."""
    per = 20
    for s in range(0, len(items), per):
        chunk = items[s:s + per]
        cols = 4
        rows = math.ceil(len(chunk) / cols)
        canvas = Image.new("RGB", (cols * THUMB, rows * (THUMB + 18)), "white")
        d = ImageDraw.Draw(canvas)
        for i, (im, cap) in enumerate(chunk):
            t = ImageOps.contain(im.convert("RGB"), (THUMB - 8, THUMB - 8))
            x, y = (i % cols) * THUMB, (i // cols) * (THUMB + 18)
            canvas.paste(t, (x + 4 + (THUMB - 8 - t.size[0]) // 2, y + 4))
            d.text((x + 4, y + THUMB), cap[:44], fill="black")
        canvas.save(path_fmt % (s // per + 1), quality=70)
    print(f"  {label}: {len(items)} on {math.ceil(len(items) / per) if items else 0} sheet(s)")


def mine(slug, ident):
    src = os.path.join(HERE, "scans", slug, ident)
    out = os.path.join(HERE, "mine", slug, ident)
    done = os.path.join(out, "leaves.jsonl")
    if os.path.exists(done):
        print(ident, "already mined")
        return
    os.makedirs(out, exist_ok=True)
    zips = [f for f in os.listdir(src) if f.endswith("_jp2.zip")]
    if not zips:
        print(ident, "no JP2 zip; skipped")
        return
    words = page_words(os.path.join(src, ident + "_djvu.xml"))
    acc = access_leaves(os.path.join(src, ident + "_scandata.xml"))
    pnums = printed_numbers(os.path.join(src, ident + "_page_numbers.json"))
    zf = zipfile.ZipFile(os.path.join(src, zips[0]))
    names = sorted(n for n in zf.namelist() if n.lower().endswith(".jp2"))
    rows_out, plates, orns = [], [], []
    for name in names:
        stem = os.path.splitext(os.path.basename(name))[0]
        leaf = int(re.search(r"_(\d+)$", stem).group(1))
        if acc is not None and leaf not in acc:
            continue
        n = acc.index(leaf) if acc is not None else len(rows_out)
        with zf.open(name) as fh:
            im = Image.open(fh)
            im.reduce = 2                       # quarter size: plenty for finding ink
            im.load()
            rgb = im.convert("RGB")
        full_w, full_h = im.size[0] * 4, im.size[1] * 4
        grey = rgb.convert("L")
        cols, rws, cells, _ = ink_grid(grey)
        ww, wh, boxes = words.get(stem, (0, 0, []))
        text_cells = set()
        tops, bots = [], []
        if ww and wh:
            for (l, t, r, b) in boxes:
                c0, c1 = int(l / ww * cols), int(r / ww * cols)
                r0, r1 = int(t / wh * rws), int(b / wh * rws)
                tops.append(r0)
                bots.append(r1)
                for rr in range(max(0, r0 - 1), min(rws, r1 + 2)):
                    for cc in range(max(0, c0 - 1), min(cols, c1 + 2)):
                        text_cells.add((rr, cc))
        text_top = min(tops) if len(boxes) > 20 else None
        text_bottom = max(bots) if len(boxes) > 20 else None
        regs = regions(cols, rws, cells, text_cells)
        ink = round(sum(cells) / len(cells), 3)
        col = colourfulness(rgb)
        found = []
        for i, g in enumerate(sorted(regs, key=lambda g: -g["cells"])):
            l, t, r, b = g["box"]
            kind = guess_region(g["box"], cols, rws, text_top, text_bottom)
            px = [round(l / cols * full_w), round(t / rws * full_h), round((r - l) / cols * full_w), round((b - t) / rws * full_h)]
            found.append({"i": i, "kind_guess": kind, "box_px": px,
                          "box_frac": [round(l / cols, 3), round(t / rws, 3), round((r - l) / cols, 3), round((b - t) / rws, 3)]})
        big = any(f["kind_guess"] == "plate" for f in found)
        if ink < 0.01 and not found:
            kind = "blank"
        elif big and len(boxes) < 60:
            kind = "plate"
        elif found:
            kind = "text+art"
        else:
            kind = "text"
        row = {"n": n, "leaf": leaf, "file": os.path.basename(name), "printed_page": pnums.get(leaf),
               "px": [full_w, full_h], "words": len(boxes), "ink": ink, "colourfulness": col,
               "kind_guess": kind, "regions": found}
        rows_out.append(row)
        if kind == "plate":
            plates.append((rgb, f"n{n} p{pnums.get(leaf) or '-'} c{col:.0f}"))
        else:
            for f in found:
                if f["kind_guess"] == "plate":
                    continue
                x, y, w, h = [v // 4 for v in f["box_px"]]
                crop = rgb.crop((x, y, x + max(w, 4), y + max(h, 4)))
                orns.append((crop, f"n{n}.{f['i']} {f['kind_guess']}"))
        if len(rows_out) % 25 == 0:
            print(f"  {ident}: {len(rows_out)} pages")
    sheet(plates, os.path.join(out, "sheet-plates-%02d.jpg"), "plates")
    sheet(orns, os.path.join(out, "sheet-ornaments-%02d.jpg"), "ornaments")
    with open(done + ".part", "w", encoding="utf-8") as f:
        for r in rows_out:
            f.write(json.dumps(r) + "\n")
    os.replace(done + ".part", done)
    print(ident, f"{len(rows_out)} pages, {len(plates)} plate guesses, {len(orns)} ornament guesses")


def main():
    slug = sys.argv[1]
    ids = sys.argv[2:] or sorted(os.listdir(os.path.join(HERE, "scans", slug)))
    for ident in ids:
        mine(slug, ident)


if __name__ == "__main__":
    main()
