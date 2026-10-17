"""Cut assigned short pieces (stories, poems, fables, speeches, excerpts) out of
the collections that hold them.

A short piece is rarely a book of its own: The Ransom of Red Chief lives in
O. Henry's Whirligigs, The Necklace in a Maupassant volume. So the collection is
fetched as an ordinary shelf item, and this script reads the committed manifest
docs/short-pieces/SHORT-PIECES.tsv, finds each piece inside its collection, and
writes data/shorts/<piece>.json (gitignored, rebuildable like data/books).

Two ways to locate a piece (column `locator`):
  heading:<words>      a converted book (data/books/<source>.json): every unit
                       whose heading id contains <words> (case and punctuation
                       ignored). Must match exactly one heading.
  lines:<start>|<end>  a raw text (data/corpus/<shelf>/<source>.txt, e.g. an
                       Internet Archive OCR scan): from the first line matching
                       regex <start> up to, not including, the next line
                       matching regex <end> (or 400 lines if <end> is empty).
Rows with status other than `ok` are listed but not cut.

    python3 pipeline/extract_short_pieces.py           # build data/shorts/
    python3 pipeline/extract_short_pieces.py --check   # every ok row resolves once; writes nothing

Never prints a piece's text. Writes are atomic (temp file + rename)."""
import csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MANIFEST = os.path.join(ROOT, "docs", "short-pieces", "SHORT-PIECES.tsv")
BOOKS = os.path.join(ROOT, "data", "books")
CORPUS = os.path.join(ROOT, "data", "corpus")
OUT = os.path.join(ROOT, "data", "shorts")
FIELDS = ["piece", "title", "author", "date", "kind", "lists", "shelf", "source", "locator", "status", "note"]


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def heading_of(unit_id):
    """'o-henry-whirligigs:VIII_THE_RANSOM.12' -> 'VIII_THE_RANSOM'."""
    return unit_id.split(":", 1)[1].rsplit(".", 1)[0]


def cut_heading(book, words):
    want = norm(words)
    heads = []
    for u in book["units"]:
        h = heading_of(u["id"])
        if want in norm(h.replace("_", " ")) and h not in heads:
            heads.append(h)
    if len(heads) != 1:
        raise LookupError(f"heading {words!r} matched {len(heads)} headings: {heads[:5]}")
    units = [u for u in book["units"] if heading_of(u["id"]) == heads[0]]
    return {"heading": heads[0], "units": units}


def cut_lines(lines, start, end):
    s = re.compile(start)
    i = next((n for n, l in enumerate(lines) if s.search(l)), None)
    if i is None:
        raise LookupError(f"start {start!r} not found")
    e = re.compile(end) if end else None
    j = next((n for n in range(i + 1, len(lines)) if e and e.search(lines[n])), None)
    if j is None:
        if e:
            raise LookupError(f"end {end!r} not found after line {i + 1}")
        j = min(i + 400, len(lines))
    return {"lines": [i + 1, j], "text": "".join(lines[i:j]).strip()}


def resolve(row, root=ROOT):
    kind, _, arg = row["locator"].partition(":")
    if kind == "heading":
        path = os.path.join(root, "data", "books", row["source"] + ".json")
        with open(path, encoding="utf-8") as f:
            return cut_heading(json.load(f), arg)
    if kind == "lines":
        start, _, end = arg.partition("|")
        path = os.path.join(root, "data", "corpus", row["shelf"], row["source"] + ".txt")
        with open(path, encoding="utf-8", errors="replace") as f:
            return cut_lines(f.readlines(), start, end)
    raise ValueError(f"unknown locator kind {kind!r}")


def load(path=MANIFEST):
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if rows and list(rows[0].keys()) != FIELDS:
        raise SystemExit(f"{path}: columns must be {FIELDS}")
    seen = set()
    for r in rows:
        if r["piece"] in seen:
            raise SystemExit(f"duplicate piece id {r['piece']}")
        seen.add(r["piece"])
    return rows


def write_atomic(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def main(argv):
    check = "--check" in argv
    rows = load()
    ok = [r for r in rows if r["status"] == "ok"]
    bad, built = [], 0
    if not check:
        os.makedirs(OUT, exist_ok=True)
    for r in ok:
        try:
            got = resolve(r)
        except (OSError, LookupError, ValueError) as e:
            bad.append((r["piece"], str(e)))
            continue
        if check:
            continue
        ocr = r["locator"].startswith("lines:")
        write_atomic(os.path.join(OUT, r["piece"] + ".json"), {
            "piece": r["piece"], "title": r["title"], "author": r["author"], "date": r["date"],
            "kind": r["kind"], "lists": [x.strip() for x in r["lists"].split(";") if x.strip()],
            "source": {"shelf": r["shelf"], "item": r["source"], "locator": r["locator"]},
            "honesty": ("raw text cut by line range from the collection; OCR is unproofread"
                        if ocr else "units cut from the converted collection by heading"),
            **got})
        built += 1
    for p, e in bad:
        print(f"UNRESOLVED {p}: {e}")
    print(f"{len(rows)} pieces, {len(ok)} ok, {len(bad)} unresolved"
          + ("" if check else f", {built} written to data/shorts/"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
