#!/usr/bin/env python3
"""Checks for pipeline/versification.py: TVTMS's test language, the reference
parser, and the committed Septuagint -> KJV map against known facts of the
Greek numbering. The map is committed, so the fact checks always run; with
the sources fetched (versification.py --fetch) the map must also rebuild
byte-for-byte.

    python3 tests/versification_test.py"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import versification as V

PASS = 0
FAIL = []
def check(label, cond):
    global PASS
    if cond: PASS += 1
    else: FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label)

# ---------------------------------------------------------------- TVTMS's tests, judged against a Bible
b = V.Bible({("Gen", "5", "31"): 12, ("Gen", "6", "1"): 30, ("Gen", "6", "2"): 20, ("Psa", "3", "1"): 9})
check("=Exist / =NotExist", b.test("Gen.5:31=Exist") and b.test("Gen.5:32=NotExist"))
check("=Last is the chapter's last verse", b.test("Gen.5:31=Last") and not b.test("Gen.5:30=Last"))
check("word counts: > and <", b.test("Gen.6:1>Gen.6:2") and not b.test("Gen.6:1<Gen.6:2"))
check("word counts: *2 doubles a side", b.test("Gen.6:2*2>Gen.6:1") and b.test("Gen.6:1<Gen.6:2*2"))
check("a subverse never exists in an edition that prints whole verses", b.test("Gen.6:1.2=NotExist") and not b.test("Gen.6:1.2=Exist"))
check("a Psalm title numbered as v.1 means no text before v.1", b.test("Psa.3:TextBeforeV1=NotExist"))
check("TVTMS's one upper-case code (PSA.118) is read", V.RE_REF.match("PSA.118:176").groups()[0] == "Psa")
check("an unknown test kind is undecided, never True", b.test("LPsa.3:1=Last") is None)
check("an empty test is no condition", b.test("") is True)

# ---------------------------------------------------------------- reference lists and ranges
check("a list carries its book: 'Gen.5:32; 6:1'",
      [r[:3] for r in V.standard_refs("Gen.5:32; 6:1", "Gen")] == [("Gen", "5", "32"), ("Gen", "6", "1")])
check("'Absent' is no verse", V.standard_refs("Absent [=Gen.50:22]", "Gen") == [])
check("a range across a chapter is expanded by the chapter's last verse",
      V.expand(V.standard_refs("Gen.2:24-3:2", "Gen"), {("Gen", "2"): "25"})
      == [("Gen", "2", "24", False), ("Gen", "2", "25", False), ("Gen", "3", "1", False), ("Gen", "3", "2", False)])
check("a subverse marks the verse as a part", V.standard_refs("Gen.3:1!a", "Gen")[0][3] is True)

# ---------------------------------------------------------------- the committed map: known facts of the Greek
FACTS = [
    ("Ps.3.1", [], "title"),                    # Swete numbers the title as v.1
    ("Ps.3.2", ["Ps.3.1"], "renumbered"),
    ("Ps.9.22", ["Ps.10.1"], "renumbered"),     # Greek Ps 9 = Hebrew 9 + 10
    ("Ps.22.1", ["Ps.23.1"], "renumbered"),     # "The LORD is my shepherd"
    ("Ps.50.3", ["Ps.51.1"], "renumbered"),     # the Miserere
    ("Ps.113.9", ["Ps.115.1"], "renumbered"),   # Greek 113 = Hebrew 114 + 115
    ("Ps.147.1", ["Ps.147.12"], "renumbered"),  # Greek 146-147 = Hebrew 147
    ("Ps.151.1", [], "not-in-kjv"),
    ("Exod.20.13", ["Exod.20.14"], "renumbered"),  # the Greek order of the commandments
    ("Exod.20.15", ["Exod.20.13"], "renumbered"),
    ("Gen.6.1", ["Gen.5.32", "Gen.6.1"], "several"),  # Swete has no 5:32; its text is in 6:1
    ("1Kgs.20.27", ["1Kgs.21.27"], "renumbered"),  # 3 Kingdoms swaps chapters 20 and 21
    ("Jer.26.2", ["Jer.46.2"], "renumbered"),   # the oracles against the nations moved
    ("Jer.25.15", ["Jer.49.35"], "renumbered"),
    ("Dan.3.24", [], "not-in-kjv"),             # the Prayer of Azariah begins
    ("Dan.3.91", ["Dan.3.24"], "renumbered"),
    ("Dan.3.98", ["Dan.4.1"], "renumbered"),
    ("2Esd.11.1", ["Neh.1.1"], "same"),         # Esdras B = Ezra 1-10 + Nehemiah 1-13
    ("Sir.1.1", [], "not-in-kjv"),
]
for lxx, kjv, rel in FACTS:
    got = V.lxx_to_kjv(lxx)
    check(f"map: LXX {lxx} -> {' '.join(kjv) or '(none)'} [{rel}]", got == (kjv, rel))

rows = [l.rstrip("\n").split("\t") for l in open(V.MAP, encoding="utf-8")][1:]
check("map: one row per Swete verse, no duplicates", len(rows) == len({r[0] for r in rows}))
kjv_ids = {l.split("\t", 1)[0][4:] for l in open(V.KJV, encoding="utf-8")}
check("map: every KJV verse it names exists in the KJV", all(k in kjv_ids for r in rows for k in r[1].split()))
check("map: a verse outside the KJV names no KJV verse", all(not r[1] for r in rows if r[2] in ("not-in-kjv", "title")))
import json
meta = json.load(open(os.path.join(V.OUT, "lxx-kjv.meta.json"), encoding="utf-8"))
chk = meta["check_against_brenton"]
check("independent check: where the map moves a verse, its proper names agree far more often than not",
      chk["the map's verse shares more names"] > 50 * max(1, chk["the same-number verse shares more names"]) / 5
      and chk["the map's verse shares more names"] > 10 * chk["the same-number verse shares more names"])
check("the map's rights name TVTMS (CC BY) and Swete/First1KGreek (CC BY-SA)",
      meta["sources"]["tvtms"]["license"] == "CC BY 4.0" and "CC BY-SA" in meta["sources"]["swete"]["license"])

if os.path.exists(os.path.join(V.SRC, "tvtms.txt")) and os.path.isdir(os.path.join(V.SWETE, "data")):
    r = subprocess.run([sys.executable, os.path.join(HERE, "..", "pipeline", "versification.py"), "--check"],
                       capture_output=True, text=True)
    check("versification.py --check: the committed map is what the pinned sources give", r.returncode == 0)
else:
    print("skip the sources are not fetched (python3 pipeline/versification.py --fetch)")

print(f"\n{PASS} passed, {len(FAIL)} failed")
for f in FAIL:
    print("  FAIL", f)
sys.exit(1 if FAIL else 0)
