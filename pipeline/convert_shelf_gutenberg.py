#!/usr/bin/env python3
"""Convert the GUTENBERG items of pipeline/<shelf>_shelf.json with the existing
convert_gutenberg_prose + contents_chapre (structure_texts.py, imported, not
modified) -- the same path the Chesterton shelf takes in structure_texts.main().

    python3 pipeline/convert_shelf_gutenberg.py <shelf>   # after fetch_shelf.py <shelf>

The companion of convert_shelf.py (which does a shelf's CCEL ThML). Reads
data/corpus/<shelf>/<slug>.txt; writes data/books/<slug>.json (gitignored)
atomically (temp + rename), skips books already built (rule 5), and makes unit
ids unique the way structure_texts.main() does (`~2` suffix). Headings come from
each book's own Contents; paragraphs run within a heading. A shelf row may add a
third element {"chapre": "<regex>"} for a book whose chapter lines the Contents
rule misses ("CHAPTER I.--A Tale of Two Clubs."); it is unioned with the
Contents rule. {"contents_only": true} uses only the book's own Contents, read
leniently (lenient_contents_chapre), without the ALL-CAPS fallback (a book whose
caps lines are part numbers or captions, not headings); {"chapre_only": "<regex>"}
replaces the rule outright (Lucas's letters: "LETTER 12" and nothing else). Verse books go
through the same prose path, so a "paragraph" there is a stanza; the scheme's
honesty field already says headings are detected, not known.

Prints and writes stats only (units, headings found, bytes) to
data/corpus/<shelf>/<shelf>_convert_report.json (gitignored). It does NOT write
the committed data/books/manifest.json and does NOT touch data/uids/:
registering and minting are attended, single-writer steps.
Internet Archive items stay raw OCR (the Edwards precedent).
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from structure_texts import convert_gutenberg_prose, contents_chapre, strip_boilerplate, _contents_key

RE_CONTENTS_HEAD_LOOSE = re.compile(r"^\s*_?(TABLE OF )?CONTENTS\.?_?\s*$", re.I | re.M)

def lenient_contents_chapre(path):
    """contents_chapre's idea, made forgiving, for {"contents_only": true} books:
    the Contents may be set in _italics_, and a title's punctuation and hyphens
    may differ between Contents and body ("CINDERELLA; OR," / "CINDERELLA, OR";
    "RIDING-HOOD" / "RIDING HOOD"), so only the letters and digits of each title
    must match, in order. No ALL-CAPS fallback. None if no Contents is found."""
    raw = strip_boilerplate(open(path, encoding="utf-8", errors="replace").read())
    m = RE_CONTENTS_HEAD_LOOSE.search(raw)
    if not m:
        return None
    keys, blank_run = [], 0
    for line in raw[m.end():].splitlines()[:400]:
        if not line.strip():
            blank_run += 1
            if blank_run >= 4 and keys:
                break
            continue
        blank_run = 0
        if len(line.strip()) > 80 and keys and not re.search(r"\d\s*$", line):
            break
        k = _contents_key(line.replace("_", " "))
        if k.upper() in ("PAGE", "CHAPTER", "CONTENTS") or not re.search(r"[A-Za-z]{3}", k):
            continue
        if 3 <= len(k) <= 80:
            keys.append(k)
    toks = {tuple(re.findall(r"[A-Za-z0-9]+", k)) for k in keys}
    alts = sorted((r"[\W_]*".join(t) for t in toks if t), key=len, reverse=True)
    if not alts:
        return None
    return (r"(?i:[\W_]*(?:CHAPTER\s+)?(?:[IVXLC]+|\d+)?\s*[.:)]?[\W_]*(?:"
            + "|".join(alts) + r")[\W_\d]*)$")

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
            chapre = contents_chapre(path)
            opts = row[2] if len(row) > 2 and isinstance(row[2], dict) else {}
            if opts.get("contents_only"):     # the book's own Contents, leniently, no caps fallback
                chapre = lenient_contents_chapre(path) or chapre
            if opts.get("chapre"):     # per-book heading rule, unioned with the Contents one
                chapre = f"(?:{opts['chapre']})|{chapre}"
            if opts.get("chapre_only"):  # per-book heading rule that REPLACES the Contents one
                chapre = opts["chapre_only"]
            # an illustration placeholder is never a heading (a Contents of plates can
            # list them, and illustrated transcriptions put one on every page)
            chapre = rf"(?!\[?Illustration)(?:{chapre})"
            book = convert_gutenberg_prose(path, slug, row[1], author, chapre)
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
