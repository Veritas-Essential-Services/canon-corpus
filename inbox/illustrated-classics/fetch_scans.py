# prov: 2026-10-23 claude-opus-5-5 drafted
"""Fetch whole-book scans from archive.org, for mining plates, flourishes and ornaments.

    py -3 fetch_scans.py <slug> <id> [<id> ...]

For each identifier, writes into ./scans/<slug>/<id>/ beside this script:
  meta.json                    the item's full archive.org metadata
  the page-image JP2 ZIP, Djvu XML, Scandata and Page Numbers JSON
  (or, when there is no JP2 ZIP, the first Text PDF instead, else the TIFF ZIP)
Resumable and atomic: files download to .part and are renamed when complete;
a file already present at the size archive.org lists is skipped.
"""
import json, os, ssl, sys, time, urllib.parse, urllib.request

UA = "WordHoard-IllustratedClassics/1.0 (https://thewordhoard.com; edition census)"
# Python 3.13+ sets VERIFY_X509_STRICT, which rejects archive.org's older GoDaddy root; keep full verification otherwise.
CTX = ssl.create_default_context()
CTX.verify_flags &= ~ssl.VERIFY_X509_STRICT
WANT = ("Single Page Processed JP2 ZIP", "Djvu XML", "Scandata", "Page Numbers JSON")
CHUNK = 1 << 20
REPORT = 100 * (1 << 20)


def open_url(url, start=0):
    h = {"User-Agent": UA}
    if start:
        h["Range"] = f"bytes={start}-"
    return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=120, context=CTX)


def get_json(url, tries=5):
    for i in range(tries):
        try:
            time.sleep(0.4)
            with open_url(url) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001
            print("  retry", url[:90], e)
            time.sleep(3 * 2 ** i)
    print("  GAVE UP", url)
    return None


def download(url, path, size, tries=6):
    """Download to path.part (resuming it if present), then rename. Returns bytes fetched this run, or None."""
    part = path + ".part"
    fetched = 0
    for i in range(tries):
        have = os.path.getsize(part) if os.path.exists(part) else 0
        if size and have > size:
            os.replace(part, part + ".bad")
            have = 0
        try:
            with open_url(url, have) as r:
                if have and r.status != 206:  # server ignored the Range: start over
                    have = 0
                mark = have // REPORT
                with open(part, "ab" if have else "wb") as f:
                    while True:
                        b = r.read(CHUNK)
                        if not b:
                            break
                        f.write(b)
                        have += len(b)
                        fetched += len(b)
                        if have // REPORT > mark:
                            mark = have // REPORT
                            print(f"    {have / (1 << 20):,.0f} MB" + (f" of {size / (1 << 20):,.0f} MB" if size else ""))
            if size and have != size:
                raise IOError(f"short read: {have} of {size} bytes")
            os.replace(part, path)
            return fetched
        except Exception as e:  # noqa: BLE001
            print("  retry", os.path.basename(path), e)
            time.sleep(3 * 2 ** i)
    print("  GAVE UP", url)
    return None


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    slug, ids = sys.argv[1], sys.argv[2:]
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scans", slug)
    total = 0
    for ident in ids:
        d = os.path.join(root, ident)
        os.makedirs(d, exist_ok=True)
        mp = os.path.join(d, "meta.json")
        if os.path.exists(mp):
            m = json.load(open(mp, encoding="utf-8"))
        else:
            m = get_json("https://archive.org/metadata/" + urllib.parse.quote(ident))
            if not m or not m.get("files"):
                print(ident, ": no metadata")
                continue
            with open(mp + ".part", "w", encoding="utf-8") as f:
                json.dump(m, f, ensure_ascii=False, indent=1)
            os.replace(mp + ".part", mp)
        md = m.get("metadata", {})
        print(f"{ident}: {md.get('title')} | {md.get('publisher')} | {md.get('date')}")
        files = [f for f in m["files"] if f.get("format") in WANT]
        if not any(f["format"] == WANT[0] for f in files):
            # Google-scanned items carry neither; their page images come as a TIFF ZIP instead.
            alt = ([f for f in m["files"] if f.get("format") == "Text PDF"]
                   or [f for f in m["files"] if f.get("format") == "Single Page Processed TIFF ZIP"])
            files += alt[:1]
            print("  no JP2 ZIP;", "taking " + alt[0]["name"] if alt else "no Text PDF or TIFF ZIP either")
        for f in files:
            size = int(f.get("size") or 0)
            path = os.path.join(d, f["name"].replace("/", "_"))
            if os.path.exists(path) and (not size or os.path.getsize(path) == size):
                print("  have", f["name"])
                continue
            print(f"  get {f['name']} ({size / (1 << 20):,.1f} MB)")
            url = f"https://archive.org/download/{urllib.parse.quote(ident)}/{urllib.parse.quote(f['name'])}"
            got = download(url, path, size)
            if got is not None:
                total += got
    print(f"done: {root}  ({total / (1 << 20):,.1f} MB fetched this run)")


if __name__ == "__main__":
    main()
