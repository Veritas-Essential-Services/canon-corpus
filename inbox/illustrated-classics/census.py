# prov: 2026-10-23 claude-opus-5-5 drafted
"""Census of a book's illustrated editions, run where the network is open (the ThinkPad).

Facts and links only: catalogue records, file lists, image sizes, and the
'List of Illustrations' section of each scan's OCR (captions and page numbers).
No page images are downloaded.

    py -3 census.py "Treasure Island" "Stevenson" treasure-island 1930 [--gutenberg 120]

Writes into ./census/<slug>/ beside this script:
  ia-search.json        archive.org search hits (texts, published <= year)
  ia-meta/<id>.json     each hit's metadata + file list (trimmed)
  ia-loi/<id>.txt       the List of Illustrations block found in that scan's OCR
  commons.json          Commons files under the book's category tree, with size and credit
  loc.json              Library of Congress search hits
  gutenberg.json        Project Gutenberg catalogue rows for the title
  gutenberg-<n>.txt     the plain text of the given ebook (for passage anchors)
Resumable: anything already on disk is not fetched again.
"""
import json, os, re, sys, time, urllib.parse, urllib.request, csv, io, ssl

# Python 3.13+ sets VERIFY_X509_STRICT, which rejects archive.org's older GoDaddy root; keep full verification otherwise.
CTX = ssl.create_default_context()
CTX.verify_flags &= ~ssl.VERIFY_X509_STRICT

UA = "WordHoard-IllustratedClassics/1.0 (https://thewordhoard.com; edition census)"


def get(url, raw=False, tries=5):
    for i in range(tries):
        try:
            time.sleep(0.4)
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90, context=CTX) as r:
                b = r.read()
                return b if raw else json.loads(b)
        except urllib.error.HTTPError as e:
            if e.code in (403, 404, 410):
                return None
            time.sleep(3 * 2 ** i)
        except Exception as e:  # noqa: BLE001
            print("  retry", url[:90], e)
            time.sleep(3 * 2 ** i)
    print("  GAVE UP", url)
    return None


def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        if isinstance(obj, str):
            f.write(obj)
        else:
            json.dump(obj, f, ensure_ascii=False, indent=1)


LOI = re.compile(r"^\s*(LIST\s+OF\s+(FULL[- ]PAGE\s+)?(ILLUSTRATIONS|PLATES|PICTURES)|ILLUSTRATIONS|PLATES|LIST OF COLOU?R(ED)? PLATES)\s*\.?\s*$", re.I | re.M)


def loi_block(text):
    """The List of Illustrations section: from its heading to the first chapter heading, at most 220 lines."""
    m = LOI.search(text[:120000])
    if not m:
        return None
    rest = text[m.start():m.start() + 40000].splitlines()
    out = []
    for n, line in enumerate(rest):
        if n > 3 and re.match(r"^\s*(PART\s+[IVX1-6]+|CHAPTER\s+[IVX1]+\b|TREASURE ISLAND\s*$|THE OLD BUCCANEER)", line, re.I) and len(out) > 6:
            break
        out.append(line)
        if len(out) >= 220:
            break
    return "\n".join(out)


def main():
    title, author, slug, maxyear = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    pg = None
    if "--gutenberg" in sys.argv:
        pg = sys.argv[sys.argv.index("--gutenberg") + 1]
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "census", slug)
    os.makedirs(base, exist_ok=True)

    # 1. archive.org
    p = os.path.join(base, "ia-search.json")
    if not os.path.exists(p):
        q = f'title:("{title}") AND creator:({author}) AND mediatype:texts AND year:[1800 TO {maxyear}]'
        fl = ["identifier", "title", "date", "year", "publisher", "creator", "contributor", "description",
              "subject", "collection", "imagecount", "possible-copyright-status", "rights", "language", "volume"]
        url = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(
            [("q", q)] + [("fl[]", f) for f in fl] + [("rows", "1000"), ("output", "json")])
        r = get(url)
        save(p, r["response"]["docs"] if r else [])
    docs = json.load(open(p, encoding="utf-8"))
    print("archive.org:", len(docs), "hits")
    for d in docs:
        ident = d["identifier"]
        mp = os.path.join(base, "ia-meta", ident + ".json")
        if not os.path.exists(mp):
            m = get("https://archive.org/metadata/" + urllib.parse.quote(ident))
            if m:
                files = [{k: f.get(k) for k in ("name", "format", "size")} for f in m.get("files", [])
                         if f.get("format") in ("Text PDF", "Single Page Processed JP2 ZIP", "Djvu XML", "DjVuTXT", "Scandata", "Page Numbers JSON", "Additional Text PDF")]
                save(mp, {"metadata": m.get("metadata", {}), "files": files})
        lp = os.path.join(base, "ia-loi", ident + ".txt")
        if not os.path.exists(lp) and os.path.exists(mp):
            meta = json.load(open(mp, encoding="utf-8"))
            txt = [f["name"] for f in meta.get("files", []) if f.get("format") == "DjVuTXT"]
            block = None
            if txt:
                b = get(f"https://archive.org/download/{urllib.parse.quote(ident)}/{urllib.parse.quote(txt[0])}", raw=True)
                if b:
                    block = loi_block(b.decode("utf-8", "replace"))
            save(lp, block or "(no List of Illustrations found in the OCR)")
    # 2. Commons: the book's category tree, two levels down
    p = os.path.join(base, "commons.json")
    if not os.path.exists(p):
        api = "https://commons.wikimedia.org/w/api.php?"
        seen, files, queue = set(), {}, [(f"Category:{title}", 0)]
        while queue:
            cat, depth = queue.pop(0)
            if cat in seen:
                continue
            seen.add(cat)
            cont = {}
            while True:
                r = get(api + urllib.parse.urlencode({"action": "query", "format": "json", "list": "categorymembers",
                                                      "cmtitle": cat, "cmlimit": "500", "cmtype": "file|subcat", **cont}))
                if not r:
                    break
                for m in r["query"]["categorymembers"]:
                    if m["ns"] == 14 and depth < 3:
                        queue.append((m["title"], depth + 1))
                    elif m["ns"] == 6:
                        files.setdefault(m["title"], []).append(cat)
                if "continue" not in r:
                    break
                cont = r["continue"]
        rows = []
        names = list(files)
        for i in range(0, len(names), 40):
            r = get(api + urllib.parse.urlencode({"action": "query", "format": "json", "prop": "imageinfo",
                                                  "titles": "|".join(names[i:i + 40]), "iiprop": "url|size|mime|extmetadata",
                                                  "iiextmetadatafilter": "Artist|DateTimeOriginal|ImageDescription|LicenseShortName|Credit|ObjectName"}))
            for pgx in (r or {}).get("query", {}).get("pages", {}).values():
                ii = (pgx.get("imageinfo") or [{}])[0]
                em = {k: re.sub(r"<[^>]+>", "", v.get("value", ""))[:300] for k, v in ii.get("extmetadata", {}).items()}
                rows.append({"file": pgx["title"], "categories": files.get(pgx["title"]), "px": [ii.get("width"), ii.get("height")],
                             "mime": ii.get("mime"), "url": ii.get("url"), "page": ii.get("descriptionurl"), "meta": em})
        save(p, {"categories": sorted(seen), "files": rows})
    print("commons:", len(json.load(open(p, encoding="utf-8"))["files"]), "files")
    # 3. Library of Congress
    p = os.path.join(base, "loc.json")
    if not os.path.exists(p):
        r = get("https://www.loc.gov/books/?" + urllib.parse.urlencode({"q": f"{title} {author}", "fo": "json", "c": "150", "dates": f"1800/{maxyear}"}))
        save(p, [{k: x.get(k) for k in ("title", "date", "id", "url", "contributor", "description", "online_format", "image_url")}
                 for x in (r or {}).get("results", [])])
    # 4. Gutenberg catalogue and text
    p = os.path.join(base, "gutenberg.json")
    if not os.path.exists(p):
        b = get("https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv", raw=True)
        rows = []
        if b:
            for row in csv.DictReader(io.StringIO(b.decode("utf-8", "replace"))):
                if title.lower() in (row.get("Title") or "").lower():
                    rows.append(row)
        save(p, rows)
    if pg:
        p = os.path.join(base, f"gutenberg-{pg}.txt")
        if not os.path.exists(p):
            b = get(f"https://www.gutenberg.org/cache/epub/{pg}/pg{pg}.txt", raw=True)
            if b:
                save(p, b.decode("utf-8", "replace"))
    print("done:", base)


if __name__ == "__main__":
    main()
