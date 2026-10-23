# prov: 2026-10-23 claude-opus-5-5 drafted
"""Download a whole book that lives on Wikimedia Commons as one file per page.

Some books are on Commons, not archive.org: Maastricht University Library's
1927 Dulac Treasure Island is Category:MU KPB 025 - Treasure Island, 286 page
scans. This saves every file in the category, in name order, into
scans/<slug>/<folder>/pages/ as 0001.jpg, 0002.jpg, ..., with pages.json
recording each page's Commons file, original URL and size. mine.py reads a
pages/ folder the same way as a JP2 zip. Resumable and atomic.

    py -3 fetch_commons_pages.py treasure-island commons-mu-kpb-025 "Category:MU KPB 025 - Treasure Island"
"""
import json, os, ssl, sys, time, urllib.parse, urllib.request

UA = "WordHoard-IllustratedClassics/1.0 (https://thewordhoard.com; whole-book scans)"
CTX = ssl.create_default_context()
CTX.verify_flags &= ~getattr(ssl, "VERIFY_X509_STRICT", 0)
API = "https://commons.wikimedia.org/w/api.php?"


def get(url, raw=False):
    for i in range(6):
        try:
            time.sleep(0.3)
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120, context=CTX) as r:
                b = r.read()
                return b if raw else json.loads(b)
        except Exception as e:  # noqa: BLE001
            print("  retry", e)
            time.sleep(3 * 2 ** i)
    print("  GAVE UP", url)
    return None


def main():
    slug, folder, cat = sys.argv[1], sys.argv[2], sys.argv[3]
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scans", slug, folder)
    os.makedirs(os.path.join(out, "pages"), exist_ok=True)
    files, cont = [], {}
    while True:
        r = get(API + urllib.parse.urlencode({"action": "query", "format": "json", "list": "categorymembers",
                                              "cmtitle": cat, "cmtype": "file", "cmlimit": "500", **cont}))
        if not r:
            break
        files += [m["title"] for m in r["query"]["categorymembers"] if m["title"].lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff"))]
        if "continue" not in r:
            break
        cont = r["continue"]
    files.sort()
    pages = []
    for i in range(0, len(files), 40):
        r = get(API + urllib.parse.urlencode({"action": "query", "format": "json", "prop": "imageinfo",
                                              "titles": "|".join(files[i:i + 40]), "iiprop": "url|size"}))
        info = {p["title"]: p.get("imageinfo", [{}])[0] for p in (r or {}).get("query", {}).get("pages", {}).values()}
        for t in files[i:i + 40]:
            ii = info.get(t, {})
            pages.append({"file": t, "url": ii.get("url"), "page": ii.get("descriptionurl"), "px": [ii.get("width"), ii.get("height")]})
    for n, p in enumerate(pages, 1):
        ext = os.path.splitext(p["file"])[1].lower()
        p["local"] = f"{n:04d}{'.jpg' if ext == '.jpeg' else ext}"
        dest = os.path.join(out, "pages", p["local"])
        if os.path.exists(dest) or not p["url"]:
            continue
        b = get(p["url"], raw=True)
        if b:
            with open(dest + ".part", "wb") as f:
                f.write(b)
            os.replace(dest + ".part", dest)
        if n % 25 == 0:
            print(f"  {n}/{len(pages)}")
    with open(os.path.join(out, "pages.json"), "w", encoding="utf-8") as f:
        json.dump({"category": cat, "pages": pages}, f, ensure_ascii=False, indent=1)
    print("done:", len(pages), "pages")


if __name__ == "__main__":
    main()
