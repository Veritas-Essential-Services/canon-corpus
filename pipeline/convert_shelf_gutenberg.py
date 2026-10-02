#!/usr/bin/env python3
"""Convert the GUTENBERG items of pipeline/<shelf>_shelf.json with the existing
convert_gutenberg_prose + contents_chapre (structure_texts.py, imported, not
modified) -- the same path the Chesterton shelf takes in structure_texts.main().

    python3 pipeline/convert_shelf_gutenberg.py <shelf>   # after fetch_shelf.py <shelf>

The companion of convert_shelf.py (which does a shelf's CCEL ThML). Reads
data/corpus/<shelf>/<slug>.txt; writes data/books/<slug>.json (gitignored)
atomically (temp + rename), skips books already built (rule 5), and makes unit
ids unique the way structure_texts.main() does (`~2` suffix). Headings come from
each book's own Contents; paragraphs run within a heading. Verse books go
through the same prose path, so a "paragraph" there is a stanza; the scheme's
honesty field already says headings are detected, not known.

Prints and writes stats only (units, headings found, bytes) to
data/corpus/<shelf>/<shelf>_convert_report.json (gitignored). It does NOT write
the committed data/books/manifest.json and does NOT touch data/uids/:
registering and minting are attended, single-writer steps.
Internet Archive items stay raw OCR (the Edwards precedent).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from structure_texts import convert_gutenberg_prose, contents_chapre

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: convert_shelf_gutenberg.py <shelf>")
    name = sys.argv[1]
    shelf = json.load(open(os.path.join(HERE, f"{name}_shelf.json"), encoding="utf-8"))
    author = shelf.get("_author", name)
    src = os.path.join(HERE, "..", "data", "corpus", name)
    out = os.path.join(HERE, "..", "data", "books")
    os.makedirs(out, exist_ok=True)
    stats = {}
    for slug, row in shelf.get("gutenberg", {}).items():
        path, dest = os.path.join(src, slug + ".txt"), os.path.join(out, slug + ".json")
        if not os.path.exists(path):
            stats[slug] = {"status": "not fetched"}; print(slug, "not fetched"); continue
        if os.path.exists(dest):
            book = json.load(open(dest, encoding="utf-8"))
        else:
            book = convert_gutenberg_prose(path, slug, row[1], author, contents_chapre(path))
            seen = {}
            for u in book["units"]:
                if u["id"] in seen:
                    seen[u["id"]] += 1
                    u["id"] = f"{u['id']}~{seen[u['id']]}"
                else:
                    seen[u["id"]] = 1
            with open(dest + ".tmp", "w", encoding="utf-8") as f:
                json.dump(book, f, ensure_ascii=False)
            os.replace(dest + ".tmp", dest)
        units = book.get("units", [])
        heads = {u["ref"].rsplit(", par.", 1)[0] for u in units if ", par." in u["ref"]}
        s = {"status": "built", "units": len(units), "headings": len(heads),
             "chars": sum(len(u["text"]) for u in units)}
        stats[slug] = s
        print(slug, s, flush=True)
    rep = os.path.join(src, f"{name}_convert_report.json")
    if os.path.isdir(src):
        json.dump(stats, open(rep + ".tmp", "w"), indent=1)
        os.replace(rep + ".tmp", rep)
    built = [s for s in stats.values() if s["status"] == "built"]
    print(f"{len(built)} built, {sum(s['units'] for s in built)} units, "
          f"{sum(1 for s in built if s['headings'] == 0)} with no heading detected")
    return stats

if __name__ == "__main__":
    main()
