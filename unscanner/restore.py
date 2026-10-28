"""Restore a scanned page for print and reading: paper to pure white, ink kept, pictures intact.

Adam, 2026-10-28: *"brighten the pages to become pure white so that it would use no ink in between
lines and in the margins or blank pages"*, with the best OCR laid invisibly over the scan.

A library scan photographs the paper as well as the print. Cream paper, foxing, the shadow of the
gutter, show-through from the other side of the leaf: all of it is grey or tan to a printer, and a
printer lays ink for every pixel that is not exactly white. So the rule here is simple to state:

    every pixel that is paper becomes 255; every pixel that is ink keeps its tone.

The steps, each measured rather than guessed, and each counted in the page's report:

| step | what is measured | the rule |
|---|---|---|
| flatten | the paper, block by block (its 95th-percentile grey); blocks inside a picture are filled from their neighbours | divide by it: uneven light, a gutter shadow, yellowing all come out level |
| white point | the paper's level after flattening | everything within `white` of the paper is 255 |
| black point | the darkest 0.5% of the page's real ink (under 128, capped at 64) | that tone and darker is 0; between, a straight line, so an engraving's greys stay greys |
| deskew | the angle (to 0.05 deg) at which the text lines' projection is sharpest | rotate, filling with white; skipped under 0.1 deg |
| edges | ink that touches the scan's edge (book block, shadow, tape) and lies in the outer 4% | removed |
| specks | dark dots of a few pixels with no other ink near them | removed; a full stop has neighbours, a speck of dirt does not |
| margins | the bounding box of what is left, padded | outside it is white |
| blank | a page with no ink left after the above | written as a pure white page |

Colour is kept only when the page's INK is coloured (a colour plate, a rubricated initial); a
black-and-white page on cream paper is written in grey, since the cream is exactly what is removed.

Nothing here redraws a line. A pixel either becomes paper or keeps its scanned tone (stretched to the
black point). Pictures come through at the scan's full resolution: a halftone keeps its dots, a pen
drawing keeps every hatch. What is NOT done: no sharpening, no inpainting of torn paper, no AI
upscaling. Those invent detail; this does not.
"""
import json
import os
import subprocess

import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None


def _need_cv2():
    if cv2 is None:
        raise SystemExit("restore needs OpenCV: pip install opencv-python-headless")


def paper_map(gray, block=None, gap=45):
    """The paper's own brightness everywhere on the page, ink and pictures removed.

    The page is cut into blocks; a block's paper is its 95th-percentile grey. A block whose value is
    far below the page's usual paper (more than `gap`) is inside a picture or a dense block of ink, so
    its paper is unknown and is filled in from the blocks around it. A max filter would do for text,
    but inside a large dark picture it takes the picture for paper and bleaches it."""
    h, w = gray.shape
    block = block or max(24, w // 40)
    gh, gw = -(-h // block), -(-w // block)
    pad = np.pad(gray, ((0, gh * block - h), (0, gw * block - w)), mode="edge")
    tiles = pad.reshape(gh, block, gw, block).transpose(0, 2, 1, 3).reshape(gh, gw, -1)
    grid = np.percentile(tiles, 95, axis=2).astype(np.float32)
    usual = float(np.median(grid))
    unknown = grid < usual - gap
    if unknown.all():
        grid[:] = usual
    elif unknown.any():
        g8 = np.clip(grid, 0, 255).astype(np.uint8)
        grid = cv2.inpaint(g8, unknown.astype(np.uint8), 3, cv2.INPAINT_TELEA).astype(np.float32)
    grid = cv2.GaussianBlur(grid, (3, 3), 0)
    return cv2.resize(grid, (w, h), interpolation=cv2.INTER_CUBIC)


def flatten(gray):
    """-> gray / paper * 255: uneven light, a gutter shadow, yellowing all come out level."""
    paper = np.maximum(paper_map(gray), 1)
    return np.clip(gray.astype(np.float32) / paper * 255.0, 0, 255)


def levels(flat, white=24, black_pct=0.5):
    """-> uint8. Within `white` of the paper is 255; the darkest ink is 0; a straight line between."""
    ink = flat[flat < 128]                         # real ink only: show-through never gets this dark
    lo = min(float(np.percentile(ink, black_pct)), 64.0) if ink.size > 500 else 0.0
    hi = 255.0 - white
    out = (flat - lo) / max(1.0, hi - lo) * 255.0
    out[flat >= hi] = 255
    return np.clip(out, 0, 255).astype(np.uint8), lo


def skew_angle(gray, limit=3.0, step=0.05):
    """The angle that makes the rows of ink most unequal (text lines sharpest). 0 when there is no text."""
    small = cv2.resize(gray, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    ink = (small < 160).astype(np.uint8)
    if ink.mean() < 0.002:
        return 0.0
    h, w = ink.shape
    best, best_a = -1.0, 0.0
    for a in np.arange(-limit, limit + step / 2, step):
        m = cv2.getRotationMatrix2D((w / 2, h / 2), a, 1.0)
        r = cv2.warpAffine(ink, m, (w, h), flags=cv2.INTER_NEAREST, borderValue=0)
        s = float(np.var(r.sum(1)))
        if s > best:
            best, best_a = s, float(a)
    return round(best_a, 2)


def rotate(gray, angle):
    h, w = gray.shape
    m = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    return cv2.warpAffine(gray, m, (w, h), flags=cv2.INTER_CUBIC, borderValue=255)


def clean_ink(img, edge=0.04, speck=60, lonely=24, thresh=200):
    """Remove edge artefacts and lonely specks; -> (img, counts)."""
    h, w = img.shape
    ink = (img < thresh).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
    near = cv2.dilate(ink, np.ones((2 * lonely + 1, 2 * lonely + 1), np.uint8))
    ex, ey = int(edge * w), int(edge * h)
    kill, n_edge, n_speck = np.zeros(n, bool), 0, 0
    for i in range(1, n):
        x, y, bw, bh, area = st[i]
        x1, y1 = x + bw, y + bh
        at_edge = x <= 1 or y <= 1 or x1 >= w - 1 or y1 >= h - 1
        in_frame = x1 <= ex or y1 <= ey or x >= w - ex or y >= h - ey
        if at_edge and (in_frame or bw < ex or bh < ey):
            kill[i], n_edge = True, n_edge + 1
        elif area <= speck:
            # lonely = no other component's ink inside the window around it
            x0, y0 = max(0, x - lonely), max(0, y - lonely)
            win = lab[y0:y1 + lonely, x0:x1 + lonely]
            if not np.any((win != 0) & (win != i)):
                kill[i], n_speck = True, n_speck + 1
    out = img.copy()
    out[kill[lab]] = 255
    return out, {"edge_artefacts": int(n_edge), "specks": int(n_speck)}


def content_box(img, thresh=200, min_area=30, pad=0.012):
    """Bounding box of the ink worth keeping, padded; None for a blank page."""
    h, w = img.shape
    ink = (img < thresh).astype(np.uint8)
    n, _, st, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
    keep = [st[i] for i in range(1, n) if st[i][4] >= min_area]
    if not keep:
        return None
    x0 = min(s[0] for s in keep); y0 = min(s[1] for s in keep)
    x1 = max(s[0] + s[2] for s in keep); y1 = max(s[1] + s[3] for s in keep)
    p = int(pad * w)
    return [int(max(0, x0 - p)), int(max(0, y0 - p)), int(min(w, x1 + p)), int(min(h, y1 + p))]


def ink_is_coloured(rgb, gray, thresh=200, chroma=70, frac=0.05):
    """True when a real share of the INK (not the paper) is coloured. Black ink on cream paper
    measures a chroma of about 35 (King Arthur); red or blue ink is well over 100."""
    ink = gray < thresh
    if ink.sum() < 1000:
        return False
    a = rgb[ink].astype(np.int16)
    c = a.max(1) - a.min(1)
    return float((c > chroma).mean()) > frac


def restore_page(src, dst, deskew=True, white=24):
    """Restore one page image; -> report dict. `dst` is written atomically (PNG, lossless)."""
    _need_cv2()
    im = Image.open(src)
    rgb = np.asarray(im.convert("RGB"))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    rep = {"src": os.path.basename(src), "size": [gray.shape[1], gray.shape[0]]}

    flat = flatten(gray)
    out, black = levels(flat, white=white)
    rep["black_point"] = round(black, 1)
    angle = skew_angle(out) if deskew else 0.0
    if abs(angle) >= 0.1:
        out = rotate(out, angle)
    rep["skew_deg"] = angle if abs(angle) >= 0.1 else 0.0
    out, counts = clean_ink(out)
    rep.update(counts)
    box = content_box(out)
    if box is None:
        out[:] = 255
        rep["kind"] = "blank"
    else:
        x0, y0, x1, y1 = box
        mask = np.full(out.shape, True)
        mask[y0:y1, x0:x1] = False
        out[mask] = 255
        rep["content_box"] = box
        rep["kind"] = "page"

    colour = box is not None and ink_is_coloured(rgb, gray)
    if colour:
        # keep the ink's hue: scale each channel by the same paper estimate, then whiten what is paper
        f = np.stack([flatten(rgb[:, :, c]) for c in range(3)], 2)
        if rep["skew_deg"]:
            f = np.stack([rotate(f[:, :, c].astype(np.uint8), angle) for c in range(3)], 2)
        paper = out == 255
        f = np.clip((f - black) / max(1.0, 255 - white - black) * 255, 0, 255).astype(np.uint8)
        f[paper] = 255
        res = Image.fromarray(f, "RGB")
    else:
        res = Image.fromarray(out, "L")
    rep["colour"] = bool(colour)

    a = np.asarray(res.convert("L"), dtype=np.float32)
    g0 = gray.astype(np.float32)
    rep["ink_before"] = round(float((255 - g0).sum() / (255 * g0.size)), 4)   # share of a full black page
    rep["ink_after"] = round(float((255 - a).sum() / (255 * a.size)), 4)
    rep["white_px_before"] = round(float((g0 >= 255).mean()), 4)
    rep["white_px_after"] = round(float((a >= 255).mean()), 4)

    dpi = im.info.get("dpi") or (300, 300)
    tmp = dst + ".part"
    res.save(tmp, format="PNG", dpi=tuple(int(round(d)) for d in dpi), optimize=True)
    os.replace(tmp, dst)
    return rep


def ocr_layer(png, out_base, lang="eng", tessdata=None):
    """tesseract -> hOCR + a text-only PDF page (the invisible words, nothing drawn)."""
    env = dict(os.environ, OMP_THREAD_LIMIT="1")
    cmd = ["tesseract", png, out_base, "-l", lang, "--psm", "3", "-c", "textonly_pdf=1"]
    if tessdata:
        cmd[3:3] = ["--tessdata-dir", tessdata]
    subprocess.run(cmd + ["pdf", "hocr"], check=True, env=env,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_base + ".pdf", out_base + ".hocr"


def picture_boxes(img, words, min_frac=0.004, pad=6):
    """Boxes of the ink no OCR word accounts for (as unscanner/images.py), merged; small ones are left
    with the text. A pen drawing, a headpiece, a decorated initial: each is one box."""
    h, w = img.shape
    ink = (img < 255).astype(np.uint8)
    for x0, y0, x1, y1 in words:
        ink[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad] = 0
    k = max(5, int(0.012 * w))
    m = cv2.dilate(ink, np.ones((k, k), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    boxes = [[int(x), int(y), int(x + bw), int(y + bh)] for x, y, bw, bh, a in st[1:]
             if bw * bh >= min_frac * w * h]
    return [b for b in boxes if not any(o is not b and o[0] <= b[0] and o[1] <= b[1]
                                        and o[2] >= b[2] and o[3] >= b[3] for o in boxes)]


def _hocr_words(path):
    import re
    s = open(path, encoding="utf-8").read()
    return [list(map(int, m)) for m in re.findall(r"ocrx_word'[^>]*bbox (\d+) (\d+) (\d+) (\d+)", s)]


def mixed_page(png, hocr, textonly_pdf, colour_png=None, dpi=300, scale=2, quality=82):
    """One PDF page in the 'mixed' convention (ScanTailor's name for it):

    - text and rules: a 1-bit stencil at `scale` x the scan's resolution (smoothed before the
      threshold, so letters are clean at 600 dpi), CCITT G4, painted black;
    - pictures: the restored grey (or colour) cut to each picture's box, JPEG;
    - paper: nothing at all. The page is white because nothing is drawn there, which is the only
      way a lossy picture codec cannot leave a faint tint in the margins;
    - words: tesseract's invisible text layer, underneath, so the page is searchable and copyable.
    """
    import io
    import pikepdf
    img = np.asarray(Image.open(png).convert("L"))
    h, w = img.shape
    boxes = picture_boxes(img, _hocr_words(hocr))
    text = img.copy()
    for x0, y0, x1, y1 in boxes:
        text[y0:y1, x0:x1] = 255
    big = cv2.resize(text, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC)
    bits = Image.fromarray(((big < 128) * 255).astype(np.uint8)).convert("1")   # 1 = ink after invert
    from PIL import TiffImagePlugin
    TiffImagePlugin.STRIP_SIZE = 1 << 30            # one strip: a PDF CCITT stream is one image, not strips
    buf = io.BytesIO()
    Image.eval(bits.convert("L"), lambda v: 255 - v).convert("1").save(buf, format="TIFF", compression="group4")
    tif = Image.open(io.BytesIO(buf.getvalue()))
    assert len(tif.tag_v2[273]) == 1
    off, cnt = tif.tag_v2[273][0], tif.tag_v2[279][0]
    g4 = buf.getvalue()[off:off + cnt]

    pdf = pikepdf.open(textonly_pdf)
    page = pdf.pages[0]
    pw, ph = float(page.mediabox[2]), float(page.mediabox[3])
    sx, sy = pw / w, ph / h
    if pikepdf.Name.Resources not in page.obj:
        page.obj.Resources = pikepdf.Dictionary()
    if pikepdf.Name.XObject not in page.obj.Resources:
        page.obj.Resources.XObject = pikepdf.Dictionary()
    xo = page.obj.Resources.XObject
    ops = []
    src = Image.open(colour_png) if colour_png else Image.fromarray(img, "L")
    for i, (x0, y0, x1, y1) in enumerate(boxes):
        jb = io.BytesIO()
        src.crop((x0, y0, x1, y1)).save(jb, format="JPEG", quality=quality, optimize=True)
        name = pikepdf.Name(f"/Pic{i}")
        xo[name] = pikepdf.Stream(pdf, jb.getvalue(), Type=pikepdf.Name.XObject, Subtype=pikepdf.Name.Image,
                                  Width=x1 - x0, Height=y1 - y0, BitsPerComponent=8,
                                  ColorSpace=pikepdf.Name.DeviceRGB if src.mode == "RGB" else pikepdf.Name.DeviceGray,
                                  Filter=pikepdf.Name.DCTDecode)
        ops.append(f"q {(x1 - x0) * sx:.3f} 0 0 {(y1 - y0) * sy:.3f} {x0 * sx:.3f} {ph - y1 * sy:.3f} cm {name} Do Q")
    if g4:
        xo[pikepdf.Name.Text] = pikepdf.Stream(
            pdf, g4, Type=pikepdf.Name.XObject, Subtype=pikepdf.Name.Image, Width=w * scale, Height=h * scale,
            ImageMask=True, BitsPerComponent=1, Filter=pikepdf.Name.CCITTFaxDecode,
            DecodeParms=pikepdf.Dictionary(K=-1, Columns=w * scale, Rows=h * scale, BlackIs1=False),
            Decode=pikepdf.Array([1, 0]))
        ops.append(f"q 0 g {pw:.3f} 0 0 {ph:.3f} 0 0 cm /Text Do Q")
    page.contents_add(pdf.make_stream("\n".join(ops).encode()), prepend=False)
    return pdf, {"pictures": boxes}


def build_pdf(pngs, out_pdf, workdir, lang="eng", tessdata=None):
    """Restored pages -> one searchable PDF in the mixed convention; -> per-page notes."""
    import pikepdf
    os.makedirs(workdir, exist_ok=True)
    book, notes = pikepdf.new(), []
    keep = []
    for png in pngs:
        base = os.path.join(workdir, os.path.splitext(os.path.basename(png))[0])
        tpdf, hocr = ocr_layer(png, base, lang, tessdata)
        one, note = mixed_page(png, hocr, tpdf)
        keep.append(one)
        book.pages.append(one.pages[0])
        notes.append(dict(note, page=os.path.basename(png)))
    tmp = out_pdf + ".part"
    book.save(tmp, compress_streams=True)
    os.replace(tmp, out_pdf)
    return notes


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Restore scanned pages: paper to white, ink and pictures kept.")
    ap.add_argument("pages", nargs="+", help="page images (png, jpg, jp2)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--white", type=int, default=24, help="how close to the paper counts as paper (0-255)")
    ap.add_argument("--no-deskew", action="store_true")
    ap.add_argument("--pdf", help="also write one searchable PDF of the restored pages (mixed convention)")
    ap.add_argument("--tessdata", help="tessdata dir (use tessdata_best)")
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    reps = []
    for p in a.pages:
        name = os.path.splitext(os.path.basename(p))[0] + ".png"
        reps.append(restore_page(p, os.path.join(a.out, name), deskew=not a.no_deskew, white=a.white))
        print(json.dumps(reps[-1]))
    with open(os.path.join(a.out, "restore-report.json"), "w") as f:
        json.dump(reps, f, indent=1)
    if a.pdf:
        pngs = [os.path.join(a.out, r["src"].rsplit(".", 1)[0] + ".png") for r in reps]
        notes = build_pdf(pngs, a.pdf, os.path.join(a.out, "ocr"), tessdata=a.tessdata)
        print(json.dumps(notes))


if __name__ == "__main__":
    main()
