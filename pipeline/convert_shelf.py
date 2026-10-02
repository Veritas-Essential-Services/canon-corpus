#!/usr/bin/env python3
"""Convert the CCEL ThML items of pipeline/<shelf>_shelf.json with the existing
convert_thml (structure_texts.py, imported, not modified).

    python3 pipeline/convert_shelf.py <shelf>      # after fetch_shelf.py <shelf>
Reads data/corpus/<shelf>/<slug>.xml; writes data/books/<slug>.json (gitignored)
atomically (temp + rename) and skips books already built (rule 5). Prints stats
only: units, units with scripture links, total links. It does NOT write the
committed data/books/manifest.json; registering the books there is
structure_texts.py's job, in an attended run. Gutenberg and Internet Archive
items stay as fetched (raw OCR stays raw, the Edwards precedent).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from structure_texts import convert_thml

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: convert_shelf.py <shelf>")
    name = sys.argv[1]
    shelf = json.load(open(os.path.join(HERE, f"{name}_shelf.json"), encoding="utf-8"))
    src = os.path.join(HERE, "..", "data", "corpus", name)
    out = os.path.join(HERE, "..", "data", "books")
    os.makedirs(out, exist_ok=True)
    stats = {}
    for slug in shelf.get("ccel", {}):
        path, dest = os.path.join(src, slug + ".xml"), os.path.join(out, slug + ".json")
        if not os.path.exists(path):
            stats[slug] = "not fetched"; print(slug, "not fetched"); continue
        if os.path.exists(dest):
            book = json.load(open(dest, encoding="utf-8"))
        else:
            book = convert_thml(path, slug)
            json.dump(book, open(dest + ".tmp", "w", encoding="utf-8"), ensure_ascii=False)
            os.replace(dest + ".tmp", dest)
        units = book.get("units", [])
        s = {"units": len(units), "units_with_links": sum(1 for u in units if u.get("links")),
             "links": sum(len(u.get("links", [])) for u in units)}
        stats[slug] = s
        print(slug, s, flush=True)
    return stats

if __name__ == "__main__":
    main()
