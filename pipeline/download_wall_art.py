"""Save the wall-art collection as TV-ready pictures on a drive you own.

Run this on your own computer (a USB stick for the TV, or a folder you sync to
it). It reads data/art/wall/collection.json and, for every work, asks
Wikimedia Commons for a copy that fits a 4K screen (3840x2160) without
upscaling past what the original holds, then saves it.

Two ways to save:

  - default        -> the picture scaled to fit 3840x2160, centred on a dark
                      mat so the TV's photo app shows the whole painting and
                      never crops it. Needs Pillow:  pip install pillow
  - --as-is        -> Commons' 4K-fit copy as it comes (no mat; the TV may
                      crop or stretch a tall portrait). Needs nothing extra.

  --caption        -> also letter the title, painter and year small in the
                      bottom corner of the mat (default mode only).
  --room louvre    -> one room only: louvre, versailles, nelson-atkins, romantic.
  --featured       -> only the works marked featured.
  --size 1920x1080 -> a different screen (a 1080p TV, say).

Layout on the drive:  <dest>/<room>/<nnn> <Painter> - <Title>.jpg
Every saved file is recorded with its source URL and sha256 in
<dest>/_downloads.jsonl. The run is resumable: files already there are
skipped, and a killed run leaves no half-written file (temp file + rename).

    python pipeline/download_wall_art.py E:\\WallArt
    python pipeline/download_wall_art.py E:\\WallArt --caption
    python pipeline/download_wall_art.py E:\\WallArt --room versailles --dry-run
"""
import argparse
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
COLLECTION = os.path.join(HERE, "..", "data", "art", "wall", "collection.json")
UA = "WordHoard-wall-art/1.0 (personal copy for a home picture frame)"
PAUSE = 1.0  # seconds between requests: Wikimedia throttles bursts
MAT = (24, 22, 20)  # warm near-black, kinder than pure black on an OLED


def safe(name, n=90):
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", name or "untitled").strip(" .")
    return name[:n] or "untitled"


def get(url, tries=6):
    wait = 4
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (400, 403, 404):
                raise
            ra = e.headers.get("Retry-After")
            time.sleep(int(ra) if ra and ra.isdigit() else wait)
        except Exception:  # noqa: BLE001 -- network hiccup: back off and retry
            time.sleep(wait)
        wait = min(wait * 2, 120)
    raise RuntimeError(f"gave up after {tries} tries: {url}")


def fit_urls(files, w, h):
    """Commons' own copy of each file scaled to fit w x h (never larger than the original)."""
    out = {}
    for i in range(0, len(files), 50):
        chunk = files[i:i + 50]
        q = urllib.parse.urlencode({"action": "query", "titles": "|".join("File:" + f for f in chunk),
                                    "prop": "imageinfo", "iiprop": "url|size", "iiurlwidth": w,
                                    "iiurlheight": h, "format": "json", "formatversion": 2})
        d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))
        norm = {n["to"]: n["from"] for n in d["query"].get("normalized", [])}
        for p in d["query"]["pages"]:
            ii = (p.get("imageinfo") or [{}])[0]
            name = norm.get(p["title"], p["title"])[5:]
            # Commons returns the original when it is already smaller than the box.
            out[name] = ii.get("thumburl") or ii.get("url")
        time.sleep(PAUSE)
    return out


def matted(blob, w, h, caption=None):
    from PIL import Image, ImageDraw, ImageFont  # imported here so --as-is needs no Pillow
    im = Image.open(io.BytesIO(blob)).convert("RGB")
    s = min(w / im.width, h / im.height)
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), MAT)
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    if caption:
        draw = ImageDraw.Draw(canvas)
        size = max(14, h // 80)
        try:
            font = ImageFont.truetype("georgia.ttf", size)
        except OSError:
            try:
                font = ImageFont.truetype("DejaVuSerif.ttf", size)
            except OSError:
                font = ImageFont.load_default()
        box = draw.textbbox((0, 0), caption, font=font)
        tw, th = box[2] - box[0], box[3] - box[1]
        pad = size
        # Only letter the caption where it falls on the mat, never across the painting.
        clear_below = (h - im.height) // 2 >= th + 2 * pad
        clear_right = (w - im.width) // 2 >= tw + 2 * pad
        if clear_below or clear_right:
            draw.text((w - tw - pad, h - th - pad - box[1]), caption, font=font, fill=(150, 142, 130))
    buf = io.BytesIO()
    canvas.save(buf, "JPEG", quality=92, optimize=True)
    return buf.getvalue()


def save(path, blob):
    tmp = path + ".part"
    with open(tmp, "wb") as f:
        f.write(blob)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dest", help="folder on your drive or USB stick")
    ap.add_argument("--room", choices=["louvre", "versailles", "nelson-atkins", "romantic"])
    ap.add_argument("--featured", action="store_true", help="only the featured works")
    ap.add_argument("--as-is", action="store_true", help="save Commons' 4K-fit copy without a mat")
    ap.add_argument("--caption", action="store_true", help="letter title, painter and year on the mat")
    ap.add_argument("--size", default="3840x2160", help="screen size, WIDTHxHEIGHT")
    ap.add_argument("--collection", default=COLLECTION)
    ap.add_argument("--dry-run", action="store_true", help="list what would be fetched")
    a = ap.parse_args()
    W, H = (int(x) for x in a.size.lower().split("x"))

    works = json.load(open(a.collection, encoding="utf-8"))["works"]
    works = [x for x in works if (not a.room or x["room"] == a.room) and (not a.featured or x.get("featured"))]
    if not a.as_is:
        try:
            import PIL  # noqa: F401
        except ImportError:
            sys.exit("The matted copies need Pillow: run  pip install pillow  (or use --as-is).")

    print(f"{len(works)} works; asking Commons for {W}x{H} copies...")
    urls = fit_urls([x["image"]["file"] for x in works], W, H)
    os.makedirs(a.dest, exist_ok=True)
    log = open(os.path.join(a.dest, "_downloads.jsonl"), "a", encoding="utf-8")
    saved = skipped = failed = 0
    for n, work in enumerate(works, 1):
        folder = os.path.join(a.dest, work["room"])
        name = safe(f"{work['order']:03d} {work['artist'] or 'Unknown'} - {work['title']}") + ".jpg"
        path = os.path.join(folder, name)
        url = urls.get(work["image"]["file"])
        if a.dry_run:
            print(f"{work['room']:14} {name}  <-  {url}")
            continue
        if os.path.exists(path):
            skipped += 1
            continue
        if not url:
            failed += 1
            print(f"  no Commons copy found: {work['title']}", file=sys.stderr)
            continue
        os.makedirs(folder, exist_ok=True)
        try:
            blob = get(url)
            if not a.as_is:
                cap = f"{work['title']}  ·  {work['artist'] or 'Unknown'}" + (f", {work['year']}" if work.get("year") else "")
                blob = matted(blob, W, H, cap if a.caption else None)
            save(path, blob)
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  failed: {work['title']} ({e})", file=sys.stderr)
            continue
        log.write(json.dumps({"qid": work["qid"], "file": path, "source": url,
                              "sha256": hashlib.sha256(blob).hexdigest()}, ensure_ascii=False) + "\n")
        log.flush()
        saved += 1
        print(f"[{n}/{len(works)}] {name}")
        time.sleep(PAUSE)
    if not a.dry_run:
        print(f"saved {saved}, already there {skipped}, failed {failed}")


if __name__ == "__main__":
    main()
