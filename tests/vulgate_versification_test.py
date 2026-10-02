#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""data/versification/vulgate-kjv.json, the Clementine Vulgate -> KJV verse
map: offline, no corpus needed. The rebuild and the Clementine invariants are
build_vulgate_versification.py --check; this checks the committed file against
the uid registry and against correspondences any Douay-Rheims margin prints."""
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

m = V.load(V.VULGATE_PATH)
kjv = {k for k in json.load(open(os.path.join(HERE, "..", "data", "uids", "wordhoard.uids.json"),
                                 encoding="utf-8"))["uids"] if k.startswith("kjv:")}
T = lambda v: V.targets(v, m)
R = lambda v: V.resolve_vulgate(v, m, kjv)

# The Psalms: the Greek count, the title as verse 1.
check("Ps 50:3 (Vulgate) is KJV Ps 51:1; 50:1-2 are its title",
      T("Ps.50.3") == ["Ps.51.1"] and T("Ps.50.1") == T("Ps.50.2") == ["Ps.51.title"])
check("Ps 9:22 is KJV Ps 10:1 (Vulgate Ps 9 is KJV 9 and 10)", T("Ps.9.22") == ["Ps.10.1"])
check("Ps 113:9 is KJV Ps 115:1 (Vulgate 113 is KJV 114 and 115)",
      T("Ps.113.1") == ["Ps.114.1"] and T("Ps.113.9") == ["Ps.115.1"])
check("Ps 115:1 is KJV Ps 116:10 (KJV 116 is Vulgate 114 and 115)",
      T("Ps.114.1") == ["Ps.116.1"] and T("Ps.115.1") == ["Ps.116.10"])
check("Ps 147:1 is KJV Ps 147:12 (KJV 147 is Vulgate 146 and 147)",
      T("Ps.146.1") == ["Ps.147.1"] and T("Ps.147.1") == ["Ps.147.12"])
check("Ps 148 numbers alike", T("Ps.148.1") == ["Ps.148.1"])
check("Ps 15:10 holds KJV 16:10 and 16:11 (a house row: TVTMS's Latin has a 15:11)",
      T("Ps.15.10") == ["Ps.16.10", "Ps.16.11"])

# Elsewhere.
check("Jonah 2:1 is KJV Jonah 1:17", T("Jonah.2.1") == ["Jonah.1.17"])
check("Dan 3:91 is KJV Dan 3:24, after the Song of the Three Children",
      T("Dan.3.91") == ["Dan.3.24"] and T("Dan.3.98") == ["Dan.4.1"])
check("Song 1:1 is KJV Song 1:2 (the Clementine has no 'Song of songs' verse)",
      T("Song.1.1") == ["Song.1.2"] and "Song.1.1" in m["kjv_without_vulgate_verse"])
check("2 Cor 13:13 is KJV 13:14", T("2Cor.13.13") == ["2Cor.13.14"])
check("Rev 12:18 is KJV Rev 13:1", T("Rev.12.18") == ["Rev.13.1"])
check("John 6:52 is KJV John 6:51 (the Clementine splits 6:51)",
      T("John.6.51") == T("John.6.52") == ["John.6.51"])
check("Mal 4 numbers alike (the Clementine keeps four chapters, unlike the Hebrew)",
      T("Mal.4.1") == ["Mal.4.1"] and m["vulgate_chapters"]["Mal.4"] == 6)
check("Gen 1:1 numbers alike", T("Gen.1.1") == ["Gen.1.1"])

# What has no KJV verse, and says why.
check("Tobias has no KJV verse: not in its canon", "canon" in R("Tob.1.1")["why"])
check("Dan 3:52 (the Song of the Three Children) has none",
      R("Dan.3.52")["resolved"] is False and "Three Children" in R("Dan.3.52")["why"])
check("Esth 11:2 (a Greek addition) has none", "Esther" in R("Esth.11.2")["why"])
check("3 John 1:15 is no Clementine verse", R("3John.1.15") ==
      {"resolved": False, "why": "no such verse in the Clementine Vulgate"})

# resolve_vulgate().
check("resolve: shifted verse", R("Ps.50.3") == {"resolved": True, "target": "kjv:Ps.51.1"})
check("resolve: one verse, two KJV verses", R("Ps.15.10") ==
      {"resolved": True, "target": "kjv:Ps.16.10", "spans": ["kjv:Ps.16.10", "kjv:Ps.16.11"]})
check("resolve: a title is unresolved, with the KJV place", R("Ps.50.1")["resolved"] is False
      and R("Ps.50.1")["kjv"] == ["Ps.51.title"])

# The file against the registry.
vals = [t for v in m["map"].values() for t in ([v] if isinstance(v, str) else v)]
check("every target is a kjv: unit id or a psalm title",
      all(f"kjv:{t}" in kjv or t.endswith(".title") for t in vals))
check("the map lists only verses whose reference changes",
      all(([v] if isinstance(v, str) else v) != [k] for k, v in m["map"].items()))
check("every mapped verse is inside its chapter's Clementine count",
      all(1 <= int(k.split(".")[2]) <= m["vulgate_chapters"][k.rsplit(".", 1)[0]] for k in m["map"]))
check("the Clementine has 35,809 verses",
      sum(m["vulgate_chapters"].values()) == 35809 == m["checked_against"]["vulgate_verses"])
check("no_kjv_verse counts add up", sum(r["count"] for r in m["no_kjv_verse"])
      == m["counts"]["vulgate_verses_with_no_kjv_verse"])
check("counts agree with the map", m["counts"]["differing_vulgate_verses"] == len(m["map"])
      and m["counts"]["house_rows"] == len(m["house_rows"]))
check("every house row is in the map with the same KJV verses",
      all(T(v) == r["kjv"] for v, r in m["house_rows"].items()))
reached = set()
for ch, n in m["vulgate_chapters"].items():
    for i in range(1, n + 1):
        r = R(f"{ch}.{i}")
        if r["resolved"]:
            reached.update(r.get("spans", [r["target"]]))
check("every KJV verse is reached from a Clementine verse, or named as having none",
      {k for k in kjv if k not in reached} ==
      {f"kjv:{e}" for e in m["kjv_without_vulgate_verse"]})

# Rights: the limit travels with the data, as in bhs-kjv.json.
r = m.get("rights", {})
check("rights block: CC BY 4.0, attributed, redistribute_whole false",
      r.get("license") == "CC BY 4.0" and "STEPBible" in r.get("attribution", "")
      and r.get("redistribute_whole") is False)
check("TVTMS is the same pinned file as the Hebrew map's",
      m["source"]["commit"] == V.load()["source"]["commit"]
      and m["source"]["sha256"] == V.load()["source"]["sha256"])

print(f"\n{passed} passed, {fails} failed")
sys.exit(1 if fails else 0)
