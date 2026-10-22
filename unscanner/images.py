"""Pictures on the page: what ink no word accounts for.

A plate, a woodcut, a printer's ornament, a drop capital: none of them is text, all of them are part of
the book. They are found the same way. Take the page, mark every pixel that differs from the paper by
more than a threshold, blank out every box the OCR read as a word (padded a little), and what is left
is picture or dirt. Dirt is small; picture is not. Regions are cut from the colour scan, never redrawn.
"""
import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:          # the pipeline still runs; regions fall back to one bounding box
    cv2 = None


def paper_level(a):
    """The paper's grey: the brightest common value (the 90th percentile)."""
    return float(np.percentile(a, 90))


def ink_regions(png, words, min_frac=0.015, thresh=28, pad=6):
    """-> (coverage fraction outside words, [bbox of each region over min_frac of the page])."""
    a = np.asarray(Image.open(png).convert("L"), dtype=np.int16)
    h, w = a.shape
    ink = (paper_level(a) - a) > thresh
    # the scan's own edge (book block, shadow) is not a picture: ignore a 2% frame
    fx, fy = int(0.02 * w), int(0.02 * h)
    ink[:fy, :] = False; ink[-fy:, :] = False; ink[:, :fx] = False; ink[:, -fx:] = False
    for x0, y0, x1, y1 in words:
        ink[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad] = False
    cover = float(ink.mean())
    regions = []
    if cover < min_frac / 3:
        return cover, regions
    if cv2 is not None:
        m = ink.astype(np.uint8) * 255
        k = max(5, int(0.01 * w))
        m = cv2.dilate(m, np.ones((k, k), np.uint8))
        n, _, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
        for i in range(1, n):
            x, y, bw, bh, area = stats[i]
            if bw * bh >= min_frac * w * h:
                regions.append([int(x), int(y), int(x + bw), int(y + bh)])
        # a region inside another (a stamp on a plate) is part of it, not a second picture
        regions = [r for r in regions if not any(o is not r and o[0] <= r[0] and o[1] <= r[1]
                                                 and o[2] >= r[2] and o[3] >= r[3] for o in regions)]
    else:
        ys, xs = np.nonzero(ink)
        if len(xs):
            regions.append([int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())])
    return cover, regions


def crop(png_colour, bbox, scale, out_path, quality=88):
    """Cut a region (bbox in OCR-raster pixels; `scale` = colour dpi / OCR dpi) from the colour scan."""
    im = Image.open(png_colour).convert("RGB")
    x0, y0, x1, y1 = [int(round(v * scale)) for v in bbox]
    im.crop((x0, y0, x1, y1)).save(out_path, quality=quality)
    return out_path
