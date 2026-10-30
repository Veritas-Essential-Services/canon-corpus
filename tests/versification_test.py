#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""data/versification/bhs-kjv.json, the Hebrew -> KJV verse map: offline, no
corpus needed. The rebuild and the WLC invariants are build_versification.py
--check; this checks the committed file against the uid registry and against
correspondences anyone can verify in a printed Bible."""
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

m = V.load()
kjv = {k for k in json.load(open(os.path.join(HERE, "..", "data", "uids", "wordhoard.uids.json"),
                                 encoding="utf-8"))["uids"] if k.startswith("kjv:")}
T = lambda h: V.targets(h, m)

# Correspondences printed in any Hebrew-English Bible's margin.
check("Gen 32:1 (Heb) is KJV Gen 31:55", T("Gen.32.1") == ["Gen.31.55"])
check("Exod 7:26 (Heb) is KJV Exod 8:1", T("Exod.7.26") == ["Exod.8.1"])
check("Joel 3:1 (Heb) is KJV Joel 2:28", T("Joel.3.1") == ["Joel.2.28"])
check("Joel 4:1 (Heb) is KJV Joel 3:1", T("Joel.4.1") == ["Joel.3.1"])
check("Mal 3:19 (Heb) is KJV Mal 4:1", T("Mal.3.19") == ["Mal.4.1"])
check("Ps 51:3 (Heb) is KJV Ps 51:1, the title taking two Hebrew verses",
      T("Ps.51.3") == ["Ps.51.1"] and T("Ps.51.1") == T("Ps.51.2") == ["Ps.51.title"])
check("Ps 3:1 (Heb) is the KJV's title", T("Ps.3.1") == ["Ps.3.title"])
check("Isa 63:19 (Heb) holds KJV 63:19 and 64:1", T("Isa.63.19") == ["Isa.63.19", "Isa.64.1"])
check("Ps 23 numbers alike (no title verse in the Hebrew count shift)", T("Ps.23.1") == ["Ps.23.1"])
check("a verse not in the map keeps its number", T("Gen.1.1") == ["Gen.1.1"])

# The file against the registry.
targets = [t for v in m["map"].values() for t in ([v] if isinstance(v, str) else v)]
check("every target is a kjv: unit id or a psalm title",
      all(f"kjv:{t}" in kjv or t.endswith(".title") for t in targets))
check("the map lists only verses whose number changes",
      all(([v] if isinstance(v, str) else v) != [k] for k, v in m["map"].items()))
check("every mapped Hebrew verse is inside its chapter's WLC count",
      all(1 <= int(k.split(".")[2]) <= m["hebrew_chapters"][k.rsplit(".", 1)[0]] for k in m["map"]))
check("the WLC has 23,213 verses in 929 chapters",
      sum(m["hebrew_chapters"].values()) == 23213 and len(m["hebrew_chapters"]) == 929)
check("Malachi has 3 chapters in Hebrew", "Mal.4" not in m["hebrew_chapters"] and "Mal.3" in m["hebrew_chapters"])
check("counts agree with the map", m["counts"]["differing_hebrew_verses"] == len(m["map"]))

# Rights (CLAUDE.md, STEPBible section): the limit travels with the data.
r = m.get("rights", {})
check("rights block: CC BY 4.0, attributed, redistribute_whole false",
      r.get("license") == "CC BY 4.0" and "STEPBible" in r.get("attribution", "")
      and r.get("redistribute_whole") is False)
check("source pinned by commit and sha256", len(m["source"]["commit"]) == 40 and len(m["source"]["sha256"]) == 64)

# resolve(): what a BDB link gets.
R = lambda h: V.resolve(h, m, kjv)
check("resolve: shifted verse", R("Ps.51.3") == {"resolved": True, "target": "kjv:Ps.51.1"})
check("resolve: one Hebrew verse, two KJV verses", R("Isa.63.19") ==
      {"resolved": True, "target": "kjv:Isa.63.19", "spans": ["kjv:Isa.63.19", "kjv:Isa.64.1"]})
check("resolve: psalm title is unresolved, with the KJV place and the reason",
      R("Ps.51.1")["resolved"] is False and R("Ps.51.1")["kjv"] == ["Ps.51.title"])
check("resolve: Mal 4:1 is no Hebrew verse, so it is NOT passed through to kjv:Mal.4.1",
      R("Mal.4.1")["resolved"] is False and "target" not in R("Mal.4.1"))
check("resolve: NT reference is left alone", R("John.1.1")["resolved"] is False)

print(f"\n{passed} passed, {fails} failed")
sys.exit(1 if fails else 0)
