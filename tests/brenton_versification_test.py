#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""data/versification/brenton-kjv.json, Brenton's English Septuagint -> KJV
verse map: offline, no corpus needed. The rebuild and Brenton's invariants are
build_brenton_versification.py --check; this checks the committed file against
the uid registry and against correspondences read in both texts."""
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

m = V.load(V.BRENTON_PATH)
kjv = {k for k in json.load(open(os.path.join(HERE, "..", "data", "uids", "wordhoard.uids.json"),
                                 encoding="utf-8"))["uids"] if k.startswith("kjv:")}
T = lambda v: V.targets(v, m)
R = lambda v: V.resolve_brenton(v, m, kjv)

# The Psalms: the Greek count, the title as verse 1.
check("Ps 50:3 (Brenton) is KJV Ps 51:1; 50:1-2 are its title",
      T("Ps.50.3") == ["Ps.51.1"] and T("Ps.50.1") == T("Ps.50.2") == ["Ps.51.title"])
check("Ps 9:22 is KJV Ps 10:1 (the Greek's Ps 9 is KJV 9 and 10)", T("Ps.9.22") == ["Ps.10.1"])
check("Ps 151 has no KJV verse", "151" in R("Ps.151.1")["why"])

# Books and chapters in the Greek's own arrangement.
check("Brenton's Nehemiah is Ezra 11-23: Ezra 11:1 is KJV Neh 1:1",
      R("Ezra.11.1") == {"resolved": True, "target": "kjv:Neh.1.1"})
check("Jer 32:15 (the Greek's order) is KJV Jer 25:15", T("Jer.32.15") == ["Jer.25.15"])
check("Jeremiah's oracles: Brenton 25:15 is KJV 49:35 (Elam), 30:1 is 49:7 (Edom), 30:17 is "
      "49:1 (Ammon), 30:29 is 49:23 (Damascus); house rows",
      T("Jer.25.15") == ["Jer.49.35"] and T("Jer.30.1") == ["Jer.49.7"]
      and T("Jer.30.17") == ["Jer.49.1"] and T("Jer.30.29") == ["Jer.49.23"])
check("Jer 23:40a-b are KJV 23:7-8, which the Greek moves after 23:40",
      T("Jer.23.40a") == ["Jer.23.7"] and T("Jer.23.40b") == ["Jer.23.8"])
check("Proverbs in the Greek's order: 24:22f is KJV 30:1, 24:35 is 30:15, 24:54 is 31:1",
      T("Prov.24.22f") == ["Prov.30.1"] and T("Prov.24.35") == ["Prov.30.15"]
      and T("Prov.24.54") == ["Prov.31.1"])
check("Esther: 1:1 is addition A (no KJV verse); 1:1s is KJV 1:1",
      R("Esth.1.1")["resolved"] is False and T("Esth.1.1s") == ["Esth.1.1"])
check("Exod 39:13 is KJV 39:1 (the furnishings in the Greek's order); 39:12 has none",
      T("Exod.39.13") == ["Exod.39.1"] and R("Exod.39.12")["resolved"] is False)

# Lettered verses.
check("a lettered addition has no KJV verse, and says why",
      R("1Kgs.12.24a")["resolved"] is False and "lettered" in R("1Kgs.12.24a")["why"])
check("a lettered verse filling a gap in Brenton's numbers is the KJV verse: Lam 3:21a-c are "
      "KJV 3:22-24, Gen 31:50a is 31:51",
      [T(f"Lam.3.21{x}") for x in "abc"] == [["Lam.3.22"], ["Lam.3.23"], ["Lam.3.24"]]
      and T("Gen.31.50a") == ["Gen.31.51"] and "Gen.31.50a" in m["lettered_gap_fills"]["verses"])
check("Jer 10:9a is KJV 10:5's second half, not 10:10 (the gap fill reads the words too)",
      T("Jer.10.9a") == ["Jer.10.5"] and "Jer.10.10" in m["kjv_without_brenton_verse"])
check("a skipped letter is no verse (Brenton has 12:24i, 24k, no 24j)",
      R("1Kgs.12.24j") == {"resolved": False, "why": "no such verse in Brenton's Septuagint"}
      and R("1Kgs.12.24k")["resolved"])

# Elsewhere.
check("Lam 1:0, the prologue before verse 1, has no KJV verse", "prologue" in R("Lam.1.0")["why"])
check("Tobit has no KJV verse: not in its canon", "canon" in R("Tob.1.1")["why"])
check("Gen 1:1 numbers alike", R("Gen.1.1") == {"resolved": True, "target": "kjv:Gen.1.1"})
check("Gen 31:51 is no Brenton verse", R("Gen.31.51")["resolved"] is False)
check("resolve: one verse, two KJV verses", R("Num.27.3") ==
      {"resolved": True, "target": "kjv:Num.27.3", "spans": ["kjv:Num.27.3", "kjv:Num.27.4"]})

# The file against the registry.
vals = [t for v in m["map"].values() for t in ([v] if isinstance(v, str) else v)]
check("every target is a kjv: unit id or a psalm title",
      all(f"kjv:{t}" in kjv or t.endswith(".title") for t in vals))
check("the map lists only verses whose reference changes",
      all(([v] if isinstance(v, str) else v) != [k] for k, v in m["map"].items()))
labels = {c: V.brenton_labels(c, m) for c in m["brenton_verses"]}
check("every mapped verse is one Brenton prints",
      all(k.rsplit(".", 1)[1] in labels.get(k.rsplit(".", 1)[0], []) for k in m["map"]))
check("Brenton has 28,617 verses with text",
      sum(map(len, labels.values())) == 28617 == m["checked_against"]["brenton_verses"])
check("no_kjv_verse counts add up", sum(r["count"] for r in m["no_kjv_verse"])
      == m["counts"]["brenton_verses_with_no_kjv_verse"])
check("counts agree with the map", m["counts"]["differing_brenton_verses"] == len(m["map"])
      and m["counts"]["house_rows"] == len(m["house_rows"]))
check("every house row is in the map with the same KJV verses, or has none",
      all(T(v) == r["kjv"] if r["kjv"] else R(v)["resolved"] is False
          for v, r in m["house_rows"].items()))
reached, unresolved = set(), 0
for ch, ls in labels.items():
    for x in ls:
        r = R(f"{ch}.{x}")
        if r["resolved"]:
            reached.update(r.get("spans", [r["target"]]))
        elif "why" not in r:
            unresolved += 1
check("every Brenton verse resolves or says why", unresolved == 0)
ot = {k for k in kjv if k[4:].split(".")[0] in V.BOOKS}
check("every KJV Old Testament verse is reached from a Brenton verse, or named as having none",
      {k for k in ot if k not in reached} == {f"kjv:{e}" for e in m["kjv_without_brenton_verse"]})

# Rights: the limit travels with the data, as in the other maps.
r = m.get("rights", {})
check("rights block: CC BY 4.0, attributed, redistribute_whole false",
      r.get("license") == "CC BY 4.0" and "STEPBible" in r.get("attribution", "")
      and r.get("redistribute_whole") is False)
check("TVTMS is the same pinned file as the Hebrew map's",
      m["source"]["commit"] == V.load()["source"]["commit"]
      and m["source"]["sha256"] == V.load()["source"]["sha256"])

print(f"\n{passed} passed, {fails} failed")
sys.exit(1 if fails else 0)
