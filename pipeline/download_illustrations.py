"""Download the illustration catalog's best copies to a drive you own.

Run this on your own computer (the cloud sandbox cannot reach the image
archives). It reads data/art/catalog.json, and for every work with a source
it saves the largest image the source offers:

  - IIIF image service  -> {service}/full/max/0/default.jpg (falls back to full/full/)
  - IIIF manifest       -> every canvas in the manifest, largest size each
  - Library of Congress -> every page's largest file (usually the master TIFF or
                           JPEG 2000), read from loc.gov's JSON API, because its
                           manifest.json sits behind a bot wall
  - Wikimedia Commons   -> the original file (a source's `image`, or the file a
                           commons.wikimedia.org/wiki/File: page names)
  - plain image URL     -> saved as is
  - web page only       -> listed in _not_downloaded.txt for you to fetch by hand

Layout on the drive:  <dest>/<Artist>/<year> <Work>/<nn>.<ext>
Every saved file is recorded with its source URL and sha256 in
<dest>/_downloads.jsonl. The run is resumable: files already there are skipped,
and a killed run leaves no half-written file (temp file + rename).

    python pipeline/download_illustrations.py E:\\Illustrations
    python pipeline/download_illustrations.py E:\\Illustrations --artist "Rackham"
    python pipeline/download_illustrations.py E:\\Illustrations --dry-run
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, "..", "data", "art", "catalog.json")
UA = "WordHoard-illustration-backup/1.0 (personal archival copy)"
PAUSE = 1.0  # seconds between requests: be polite to the libraries


def safe(name, n=80):
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", name or "untitled").strip(" .")
    return name[:n] or "untitled"


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read(), r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            if e.code in (404, 403, 400):
                raise
            time.sleep(2 ** (i + 1))
        except Exception:  # noqa: BLE001 -- network hiccup: back off and retry
            time.sleep(2 ** (i + 1))
    raise RuntimeError(f"gave up after {tries} tries: {url}")


def ext_for(ctype, url):
    for key, ext in (("tiff", ".tif"), ("png", ".png"), ("jp2", ".jp2"), ("jpeg", ".jpg"), ("jpg", ".jpg")):
        if key in (ctype or "").lower():
            return ext
    m = re.search(r"\.(tiff?|png|jp2|jpe?g)(?:$|\?)", url, re.I)
    return "." + m.group(1).lower().replace("jpeg", "jpg") if m else ".jpg"


def iiif_image(service):
    """The largest rendering of one IIIF image service (v3 'max', v2 'full')."""
    service = service.rstrip("/")
    service = re.sub(r"/info\.json$", "", service)
    last = None
    for size in ("max", "full"):
        url = f"{service}/full/{size}/0/default.jpg"
        try:
            blob, ctype = get(url)
            return blob, ctype, url
        except Exception as e:  # noqa: BLE001
            last = e
    raise last


def manifest_services(manifest):
    """Image service URLs for every canvas in a IIIF v2 or v3 manifest."""
    out = []
    for seq in manifest.get("sequences", []):  # v2
        for canvas in seq.get("canvases", []):
            for img in canvas.get("images", []):
                res = img.get("resource", {})
                svc = res.get("service", {})
                svc = svc[0] if isinstance(svc, list) and svc else svc
                out.append(svc.get("@id") or svc.get("id") or res.get("@id"))
    for canvas in manifest.get("items", []):  # v3
        for page in canvas.get("items", []):
            for anno in page.get("items", []):
                body = anno.get("body", {})
                svc = body.get("service", [])
                svc = svc[0] if isinstance(svc, list) and svc else svc
                out.append((svc or {}).get("id") or (svc or {}).get("@id") or body.get("id"))
    return [u for u in out if u]


def loc_files(url):
    """The largest file of every page of a loc.gov item or resource."""
    base = url.split("manifest.json")[0].split("?")[0].rstrip("/") + "/?fo=json"
    d = json.loads(get(base)[0])
    pages = [page for res in d.get("resources", []) for page in res.get("files", [])]
    out = []
    for page in pages:
        files = [f for f in page if f.get("url") and f.get("size") and str(f.get("mimetype", "")).startswith("image/")]
        if files:
            out.append(max(files, key=lambda f: f["size"])["url"])
    return out


def commons_original(page_url):
    """The original file behind a commons.wikimedia.org/wiki/File: page."""
    title = urllib.parse.unquote(page_url.split("/wiki/", 1)[1])
    q = urllib.parse.urlencode({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url",
                                "format": "json", "formatversion": 2})
    d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q)[0])
    pages = d["query"]["pages"]
    return pages[0]["imageinfo"][0]["url"] if pages and pages[0].get("imageinfo") else None


def save(path, blob):
    tmp = path + ".part"
    with open(tmp, "wb") as f:
        f.write(blob)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dest", help="folder on your external drive")
    ap.add_argument("--artist", help="only artists whose name contains this")
    ap.add_argument("--catalog", default=CATALOG)
    ap.add_argument("--dry-run", action="store_true", help="list what would be fetched")
    a = ap.parse_args()

    catalog = json.load(open(a.catalog, encoding="utf-8"))
    os.makedirs(a.dest, exist_ok=True)
    log = open(os.path.join(a.dest, "_downloads.jsonl"), "a", encoding="utf-8")
    manual = []
    saved = skipped = failed = 0

    for artist in catalog:
        if a.artist and a.artist.lower() not in artist["artist"].lower():
            continue
        for work in artist.get("works", []):
            if work.get("pd_us") is not True:
                continue  # only works confirmed public domain in the US
            folder = os.path.join(a.dest, safe(artist["artist"]),
                                  safe(f"{work.get('published') or 'undated'} {work['title']}"))
            targets = []  # (kind, url, source)
            for src in work.get("sources", []):
                if src.get("iiif") and "www.loc.gov" in src["iiif"]:
                    targets.append(("loc", src["iiif"], src))
                elif src.get("iiif"):
                    kind = "manifest" if "manifest" in src["iiif"] else "service"
                    targets.append((kind, src["iiif"], src))
                elif src.get("image"):
                    targets.append(("image", src["image"], src))
                elif re.match(r"https://commons\.wikimedia\.org/wiki/File:", src.get("url", "")):
                    targets.append(("commons", src["url"], src))
                elif re.search(r"\.(tiff?|png|jp2|jpe?g)(?:$|\?)", src.get("url", ""), re.I):
                    targets.append(("image", src["url"], src))
                else:
                    manual.append(f"{artist['artist']} | {work['title']} | {src.get('url')}")
            if not targets:
                continue
            if a.dry_run:
                kind, url, _ = targets[0]
                print(f"{kind:8} {artist['artist']} / {work['title']}: {url}")
                continue
            os.makedirs(folder, exist_ok=True)
            # The catalog lists the best source first; fall back to the next if one fails.
            services = None
            for kind, url, src in targets:
                try:
                    if kind == "manifest":
                        services = manifest_services(json.loads(get(url)[0]))
                    elif kind == "loc":
                        services, kind = loc_files(url), "image"
                    elif kind == "commons":
                        services, kind = [u for u in [commons_original(url)] if u], "image"
                    else:
                        services = [url]
                    if services:
                        break
                except Exception as e:  # noqa: BLE001
                    print(f"  source failed, trying next: {url} ({e})", file=sys.stderr)
            if not services:
                failed += 1
                manual.extend(f"{artist['artist']} | {work['title']} | {u}" for _, u, _ in targets)
                continue
            try:
                for i, svc in enumerate(services, 1):
                    stem = os.path.join(folder, f"{i:03d}")
                    if any(os.path.exists(stem + e) for e in (".jpg", ".tif", ".png", ".jp2")):
                        skipped += 1
                        continue
                    if kind == "image":
                        blob, ctype = get(svc)
                        got = svc
                    else:
                        blob, ctype, got = iiif_image(svc)
                    path = stem + ext_for(ctype, got)
                    save(path, blob)
                    log.write(json.dumps({"artist": artist["artist"], "work": work["title"],
                                          "file": os.path.relpath(path, a.dest), "url": got,
                                          "host": src.get("host"), "bytes": len(blob),
                                          "sha256": hashlib.sha256(blob).hexdigest()}) + "\n")
                    log.flush()
                    saved += 1
                    print(f"  saved {os.path.relpath(path, a.dest)}  {len(blob) // 1024:,} KB")
                    time.sleep(PAUSE)
            except Exception as e:  # noqa: BLE001 -- report and carry on; rerun resumes
                failed += 1
                print(f"  FAILED {artist['artist']} / {work['title']}: {e}", file=sys.stderr)

    if manual:
        with open(os.path.join(a.dest, "_not_downloaded.txt"), "w", encoding="utf-8") as f:
            f.write("Web pages with no direct image or IIIF link. Open each and download by hand.\n\n")
            f.write("\n".join(manual) + "\n")
    print(f"\nsaved {saved}, already there {skipped}, failed {failed}, by hand {len(manual)}")


if __name__ == "__main__":
    main()
