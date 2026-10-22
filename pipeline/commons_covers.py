"""Match Saturday Evening Post covers on Wikimedia Commons to the illustration catalog.

For each artist below, reads the Commons category of their Post covers (file
names, pixel sizes, URLs, through the Commons API) and reads the cover's date
from the file name. Then, in data/art/catalog.json:

  - a work whose `publication` names that Post date gets a Wikimedia Commons
    source (the largest file for the date), marked verified "fetched";
  - with --add, dated covers the catalog does not yet list are added as new
    works ("magazine cover", pd_us true when published before 1931).

Commons is not a IIIF server; it serves the original file and resized copies,
so these sources carry `image` (the original) and `display` (1280px) instead of
`iiif`. Covers on Commons are mostly ~600x800 scans; a few are ~1600x2100.

    python3 pipeline/commons_covers.py          # attach sources to existing works
    python3 pipeline/commons_covers.py --add    # ...and add the covers not yet listed
"""
import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, "..", "data", "art", "catalog.json")
API = "https://commons.wikimedia.org/w/api.php"
UA = "WordHoard-catalog/1.0 (https://thewordhoard.com; illustration catalog)"
CATEGORIES = {
    "Norman Rockwell": "Category:Norman Rockwell's Saturday Evening Post covers",
    "J. C. Leyendecker": "Category:J. C. Leyendecker's Saturday Evening Post covers",
    "N. C. Wyeth": "Category:N.C. Wyeth's Saturday Evening Post covers",
}
MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def api(**p):
    p.update(format="json", formatversion=2)
    url = API + "?" + urllib.parse.urlencode(p)
    for i in range(6):
        try:
            time.sleep(1.0)
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                return json.load(r)
        except Exception:  # noqa: BLE001 -- 429s: back off
            time.sleep(5 * 2 ** i)
    raise RuntimeError("Commons API gave up: " + url)


def files(cat):
    out, cont = [], {}
    while True:
        d = api(action="query", generator="categorymembers", gcmtitle=cat, gcmtype="file", gcmlimit=200,
                prop="imageinfo", iiprop="size|url", iiurlwidth=1280, **cont)
        for p in d.get("query", {}).get("pages", []):
            ii = (p.get("imageinfo") or [{}])[0]
            if ii.get("url"):
                out.append({"title": p["title"], "w": ii["width"], "h": ii["height"], "url": ii["url"].split("?")[0],
                            "display": (ii.get("thumburl") or ii["url"]).split("?")[0], "page": ii["descriptionurl"]})
        if "continue" not in d:
            return out
        cont = d["continue"]


def date_of(name):
    """A cover's date from its Commons file name, or None. Handles the forms in use:
    1917-06-16 · 1921-6-4 · 1916 12 23 · 12Mar1921 · 19 Aug 1911 · August 27, 1927."""
    n = name.replace("_", " ")
    m = re.search(r"(1[89]\d\d)[-  ](\d{1,2})[-  ](\d{1,2})(?!\d)", n)
    if m:
        y, mo, d = map(int, m.groups())
    else:
        m = re.search(r"(\d{1,2}) ?([A-Za-z]{3})[a-z]* ?(1[89]\d\d)", n)
        if m and m.group(2).lower() in MONTHS:
            d, mo, y = int(m.group(1)), MONTHS[m.group(2).lower()], int(m.group(3))
        else:
            m = re.search(r"([A-Za-z]{3})[a-z]* (\d{1,2}), (1[89]\d\d)", n)
            if not (m and m.group(1).lower() in MONTHS):
                return None
            mo, d, y = MONTHS[m.group(1).lower()], int(m.group(2)), int(m.group(3))
    try:
        return datetime.date(y, mo, d).isoformat()
    except ValueError:
        return None


def main():
    add = "--add" in sys.argv
    cat = json.load(open(CATALOG, encoding="utf-8"))
    today = datetime.date.today().isoformat()
    for artist, category in CATEGORIES.items():
        entry = next(a for a in cat if a["artist"] == artist)
        best = {}
        for f in files(category):
            dt = date_of(f["title"])
            if dt and (dt not in best or f["w"] * f["h"] > best[dt]["w"] * best[dt]["h"]):
                best[dt] = f
        attached = added = 0
        for dt, f in sorted(best.items()):
            src = {"host": "Wikimedia Commons", "url": f["page"], "image": f["url"], "display": f["display"],
                   "best_size": f"{f['w']}x{f['h']}", "iiif": None, "verified": "fetched", "checked": today}
            works = [w for w in entry["works"] if dt in (w.get("publication") or "")]
            for w in works:
                if not any(s.get("url") == f["page"] for s in w["sources"]):
                    w["sources"].insert(0, src)
                    attached += 1
            if not works and add:
                y = int(dt[:4])
                entry["works"].append({
                    "title": f"Saturday Evening Post cover, {dt}", "kind": "magazine cover", "published": y,
                    "publication": f"The Saturday Evening Post, {dt}", "plates": None,
                    "pd_us": True if y < 1931 else "check", "sources": [src],
                    "notes": "Added from the Commons category of the artist's Post covers; date read from the file name, subject title not yet recorded."})
                added += 1
        print(f"{artist}: {len(best)} dated covers on Commons; {attached} sources attached, {added} covers added")
    tmp = CATALOG + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(cat, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    os.replace(tmp, CATALOG)


if __name__ == "__main__":
    main()
