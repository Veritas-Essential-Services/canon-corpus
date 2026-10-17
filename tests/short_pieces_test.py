"""Offline checks for pipeline/extract_short_pieces.py (fixtures inline)."""
import os, sys, tempfile, json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
import extract_short_pieces as x

passed = failed = 0


def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print("FAIL", name)


BOOK = {"units": [
    {"id": "b:x.1", "text": "front"},
    {"id": "b:VIII_THE_RANSOM_OF_RED_CHIEF.1", "text": "a"},
    {"id": "b:VIII_THE_RANSOM_OF_RED_CHIEF.2", "text": "b"},
    {"id": "b:IX_THE_MARRY_MONTH_OF_MAY.1", "text": "c"},
    {"id": "b:X_THE_MAY_QUEEN.1", "text": "d"},
]}

got = x.cut_heading(BOOK, "Ransom of Red Chief")
check("heading match takes every unit under it", [u["text"] for u in got["units"]] == ["a", "b"])
check("heading reported", got["heading"] == "VIII_THE_RANSOM_OF_RED_CHIEF")
check("punctuation and case ignored", x.cut_heading(BOOK, "ransom, of red-chief")["heading"].startswith("VIII"))
try:
    x.cut_heading(BOOK, "may")
    check("ambiguous heading refused", False)
except LookupError:
    check("ambiguous heading refused", True)
try:
    x.cut_heading(BOOK, "Gift of the Magi")
    check("missing heading refused", False)
except LookupError:
    check("missing heading refused", True)

LINES = ["title page\n", "THE NECKLACE\n", "She was one of those\n", "pretty girls\n", "THE PIECE OF STRING\n", "x\n"]
got = x.cut_lines(LINES, r"^THE NECKLACE", r"^THE PIECE OF STRING")
check("line cut stops before the end marker", got["lines"] == [2, 4] and got["text"].endswith("pretty girls"))
got = x.cut_lines(LINES, r"^THE NECKLACE", "")
check("empty end runs to the cap or end of file", got["lines"] == [2, 6])
try:
    x.cut_lines(LINES, r"^THE NECKLACE", r"^NEVER")
    check("missing end marker refused", False)
except LookupError:
    check("missing end marker refused", True)
try:
    x.cut_lines(LINES, r"^NOPE", "")
    check("missing start refused", False)
except LookupError:
    check("missing start refused", True)

with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "m.tsv")
    with open(p, "w") as f:
        f.write("\t".join(x.FIELDS) + "\n")
        f.write("\t".join(["a"] + [""] * (len(x.FIELDS) - 1)) + "\n")
        f.write("\t".join(["a"] + [""] * (len(x.FIELDS) - 1)) + "\n")
    try:
        x.load(p)
        check("duplicate piece id refused", False)
    except SystemExit:
        check("duplicate piece id refused", True)
    os.makedirs(os.path.join(d, "data", "books"))
    with open(os.path.join(d, "data", "books", "b.json"), "w") as f:
        json.dump(BOOK, f)
    row = {"locator": "heading:red chief", "source": "b", "shelf": "s"}
    check("resolve reads data/books/<source>.json", len(x.resolve(row, root=d)["units"]) == 2)

if os.path.exists(x.MANIFEST):
    rows = x.load()
    check("committed manifest has the expected columns and unique ids", len(rows) > 0)
    check("every committed row has a known status",
          all(r["status"] in ("ok", "held", "lane", "notpd", "nosource", "todo") for r in rows))
    check("every ok row names a shelf, a source and a locator",
          all(r["shelf"] and r["source"] and r["locator"] for r in rows if r["status"] == "ok"))

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
