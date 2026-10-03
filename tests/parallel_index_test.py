#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""data/parallel/kjv-parallel.tsv, one row per KJV verse naming every
version's verse(s): offline, no corpus needed. The rebuild is
build_parallel_index.py --check (it needs the built books); this checks the
committed file against the committed maps and the uid registry."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import versification as V

fails = passed = 0
def check(m, c):
    global fails, passed
    print(("ok    " if c else "FAIL  ") + m)
    if c: passed += 1
    else: fails += 1

ROOT = os.path.join(HERE, "..")
with open(os.path.join(ROOT, "data", "parallel", "kjv-parallel.tsv"), encoding="utf-8") as f:
    lines = f.read().split("\n")
head = lines[0].split("\t")
rows = {}
for line in lines[1:]:
    if line:
        cells = line.split("\t")
        rows[cells[0]] = {c: (cells[i].split(" ") if cells[i] else []) for i, c in enumerate(head)}
uids = json.load(open(os.path.join(ROOT, "data", "uids", "wordhoard.uids.json"), encoding="utf-8"))["uids"]
kjv = [k[4:] for k in uids if k.startswith("kjv:")]
C = lambda k, col: rows[k][col]

check("columns: kjv, uid, the Hebrew, the Greek NT, then the ten shelf versions",
      head == ["kjv", "uid", "hebrew", "greek_nt", "vulgate", "douay", "brenton", "geneva",
               "tyndale", "ylt", "darby", "asv", "coverdale", "bishops"])
check("Ps 14:3 is Coverdale's 14:2 (his 14:3-4, the Latin's Rom 3 insertion, are in no row)",
      C("Ps.14.3", "coverdale") == ["Ps.14.2"]
      and not any(x in ("Ps.14.3", "Ps.14.4") for r in rows.values() for x in r["coverdale"]))
check("Ps 87:1-2: the Bishops' swaps them; Coverdale's 87:1 holds both",
      C("Ps.87.1", "bishops") == ["Ps.87.2"] and C("Ps.87.2", "bishops") == ["Ps.87.1"]
      and C("Ps.87.1", "coverdale") == ["Ps.87.1"] == C("Ps.87.2", "coverdale"))
check("Tyndale: Exodus and Jonah have cells, Joshua and Isaiah none",
      C("Exod.1.1", "tyndale") == ["Exod.1.1"] and C("Jonah.1.1", "tyndale") == ["Jonah.1.1"]
      and not C("Josh.1.1", "tyndale") and not C("Isa.1.1", "tyndale"))
check("one row per KJV verse in the registry, 31,102", set(rows) == set(kjv) and len(rows) == 31102)
check("every row's uid is the registry's for that KJV verse",
      all(r["uid"] == [uids[f"kjv:{k}"]] for k, r in rows.items()))

# Rows read in each tradition's own numbering.
check("Ps 51:1: Hebrew 51:3; Vulgate, Douay and Brenton 50:3; the English Bibles 51:1",
      C("Ps.51.1", "hebrew") == ["Ps.51.3"] and C("Ps.51.1", "vulgate") == ["Ps.50.3"]
      and C("Ps.51.1", "douay") == ["Ps.50.3"] and C("Ps.51.1", "brenton") == ["Ps.50.3"]
      and C("Ps.51.1", "asv") == ["Ps.51.1"])
check("Neh 1:1 is Brenton's Ezra 11:1", C("Neh.1.1", "brenton") == ["Ezra.11.1"])
check("Num 12:16 is the Geneva's Num 13:1 (it numbers as the Hebrew there; the WLC "
      "itself keeps 12:16)", C("Num.12.16", "geneva") == ["Num.13.1"]
      and C("Num.12.16", "hebrew") == ["Num.12.16"])
check("Dan 4:1: Hebrew 3:31, Vulgate 3:98, the Geneva's merged 3:30, Brenton 4:1",
      C("Dan.4.1", "hebrew") == ["Dan.3.31"] and C("Dan.4.1", "vulgate") == ["Dan.3.98"]
      and C("Dan.4.1", "geneva") == ["Dan.3.30"] and C("Dan.4.1", "brenton") == ["Dan.4.1"])
check("Mal 4:5 is Brenton's 3:22 and the Hebrew's 3:23",
      C("Mal.4.5", "brenton") == ["Mal.3.22"] and C("Mal.4.5", "hebrew") == ["Mal.3.23"])
check("Phil 1:16 is the Vulgate's, Darby's and the ASV's 1:17 (the Greek's order)",
      all(C("Phil.1.16", c) == ["Phil.1.17"] for c in ("vulgate", "douay", "darby", "asv")))
check("Acts 8:37: empty for Darby and the ASV, which leave it out",
      C("Acts.8.37", "darby") == [] == C("Acts.8.37", "asv") and C("Acts.8.37", "ylt") == ["Acts.8.37"])
NT = {"Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil", "Col",
      "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet", "1John",
      "2John", "3John", "Jude", "Rev"}
check("the Greek NT column holds the whole NT, each on its KJV verse; empty only for the four "
      "verses the Byzantine text lacks (Luke 17:36, Acts 8:37, 15:34, 24:7)",
      {k for k, r in rows.items() if k.split(".")[0] in NT and not r["greek_nt"]}
      == {"Luke.17.36", "Acts.8.37", "Acts.15.34", "Acts.24.7"}
      and all(r["greek_nt"] == [k] for k, r in rows.items() if r["greek_nt"]))
check("the Old Testament has no Greek NT cell and the New no Hebrew cell",
      not C("Gen.1.1", "greek_nt") and not C("Matt.1.1", "hebrew") and not C("Matt.1.1", "brenton"))

# Against the committed maps.
heb = V.load()
check("every Hebrew verse the map sends to a KJV verse is in that row",
      all(f"{ch}.{v}" in C(k, "hebrew") for ch, n in heb["hebrew_chapters"].items()
          for v in range(1, n + 1) for k in V.targets(f"{ch}.{v}", heb) if not k.endswith(".title")))
check("the Hebrew cell is empty only for the KJV verses the Hebrew map names as having none",
      {k for k in kjv if k.split(".")[0] in V.BOOKS and not C(k, "hebrew")}
      <= set(heb["kjv_without_hebrew_verse"]))
for slug in ("geneva", "tyndale", "ylt", "darby", "asv", "coverdale", "bishops"):
    m = V.load(V.english_path(slug))
    ok = all(v in C(e, slug) for v, es in m["map"].items() for e in ([es] if isinstance(es, str) else es))
    books = {c.split(".")[0] for c in m["chapters"]}
    empty = {k for k in kjv if k.split(".")[0] in books and not C(k, slug)}
    check(f"{slug}: every moved verse is in its KJV rows; its empty cells are exactly the "
          f"verses its map names as having none", ok and empty == set(m["kjv_without_verse"]))
b = V.load(V.BRENTON_PATH)
check("brenton: every moved verse is in its KJV rows",
      all(v in C(e, "brenton") for v, es in b["map"].items()
          for e in ([es] if isinstance(es, str) else es) if not e.endswith(".title")))
check("brenton: its empty Old Testament cells are exactly the verses its map names",
      {k for k in kjv if k.split(".")[0] in V.BOOKS and not C(k, "brenton")}
      == set(b["kjv_without_brenton_verse"]))
vg = V.load(V.VULGATE_PATH)
check("vulgate: its empty cells are exactly the verses its map names",
      {k for k in kjv if not C(k, "vulgate")} == set(vg["kjv_without_vulgate_verse"]))
labels = {c: set(V.brenton_labels(c, b)) for c in b["brenton_verses"]}
check("every Brenton ref in the index is a verse Brenton prints",
      all(x.rsplit(".", 1)[1] in labels.get(x.rsplit(".", 1)[0], ()) for r in rows.values()
          for x in r["brenton"]))

print(f"\n{passed} passed, {fails} failed")
sys.exit(1 if fails else 0)
