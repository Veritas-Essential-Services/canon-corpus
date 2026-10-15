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

# Fixed in review (2026-10-02): each read in both texts.
check("review: the Douay's split of Clementine Ps 15:10 lands one verse in each KJV row",
      C("Ps.16.10", "douay") == ["Ps.15.10"] and C("Ps.16.11", "douay") == ["Ps.15.11"])
check("review: KJV Ps 99:1 holds Vulgate and Brenton 98:1 only; Ps 98:1 holds 97:1",
      C("Ps.99.1", "vulgate") == ["Ps.98.1"] and C("Ps.99.1", "brenton") == ["Ps.98.1"]
      and C("Ps.98.1", "vulgate") == ["Ps.97.1"])
check("review: Tyndale has no words for the KJV's Luke 17:36 or Rev 21:26 (Bible SuperSearch "
      "keeps 17:37 and 21:27 in their own slots)",
      C("Luke.17.36", "tyndale") == [] and C("Luke.17.37", "tyndale") == ["Luke.17.37"]
      and C("Rev.21.26", "tyndale") == [] and C("Rev.21.27", "tyndale") == ["Rev.21.27"])
check("review: Brenton's 35:16 holds the KJV's Gen 35:21; Josh 19:47-48 swapped",
      C("Gen.35.21", "brenton") == ["Gen.35.16"] and C("Josh.19.47", "brenton") == ["Josh.19.48"])
check("review: Young's Hos 13:9 is the end of the KJV's 13:8; Darby prints no 1 John 5:7",
      C("Hos.13.8", "ylt") == ["Hos.13.8", "Hos.13.9"] and C("1John.5.7", "darby") == [])
check("review: Brenton's 2 Sam 23:29 reaches into the KJV's 23:30; his 23:37a-c are the KJV's "
      "Hiddai, Abi-albon and Naharai",
      C("2Sam.23.30", "brenton") == ["2Sam.23.29", "2Sam.23.37a"]
      and C("2Sam.23.31", "brenton") == ["2Sam.23.29", "2Sam.23.37b"]
      and C("2Sam.23.37", "brenton") == ["2Sam.23.37", "2Sam.23.37c"])
check("review: the Douay's empty cells are the Vulgate's plus only 1 Kgs 17:19 and Prov 30:29, "
      "the two verses this Douay truly lacks",
      {k for k in rows if not C(k, "douay")}
      == {k for k in rows if not C(k, "vulgate")} | {"1Kgs.17.19", "Prov.30.29"})
check("review: the Douay's Isa 46:11, 2 Sam 13:38 and Ps 150:5 hold the next verse's words; its "
      "Isa 46:12 is the KJV's 46:13",
      C("Isa.46.12", "douay") == ["Isa.46.11"] and C("Isa.46.13", "douay") == ["Isa.46.12"]
      and C("2Sam.13.39", "douay") == ["2Sam.13.38"] and C("Ps.150.6", "douay") == ["Ps.150.5"])
readme = open(os.path.join(ROOT, "data", "parallel", "README.md"), encoding="utf-8").read()
check("the rights note travels with the index: TVTMS named, CC BY 4.0, attributed",
      "CC BY 4.0" in readme and "TVTMS" in readme and "www.STEPBible.org" in readme
      and "redistribute_whole: false" in readme)
check("the rights note says the greek_nt column is the whole NT, empty only where the "
      "Byzantine text lacks the verse", "whole New Testament" in readme
      and "Luke 17:36, Acts 8:37, 15:34, 24:7" in readme)
check("the rights note names every house-read English column",
      all(c in readme for c in ("geneva", "tyndale", "ylt", "darby", "asv", "coverdale", "bishops")))

print(f"\n{passed} passed, {fails} failed")
sys.exit(1 if fails else 0)
