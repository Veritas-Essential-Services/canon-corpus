#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""data/versification/<slug>-kjv.json, the historic English Bibles -> KJV
verse maps: offline, no corpus needed. The rebuild and the invariants are
build_english_versification.py --check; this checks the committed files
against the uid registry and against correspondences read in both texts."""
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

kjv = {k for k in json.load(open(os.path.join(HERE, "..", "data", "uids", "wordhoard.uids.json"),
                                 encoding="utf-8"))["uids"] if k.startswith("kjv:")}
SLUGS = ["geneva", "tyndale", "ylt", "darby", "asv"]
M = {s: V.load(V.english_path(s)) for s in SLUGS}
T = lambda s, v: V.targets(v, M[s])
R = lambda s, v: V.resolve_english(v, M[s], kjv)

# The Geneva numbers as the Hebrew in places; the module poured those verses
# into the KJV's slots, the overflow merged into the chapter's last slot.
check("Geneva Num 13:1 is KJV Num 12:16 (the Hebrew's numbering)",
      T("geneva", "Num.13.1") == ["Num.12.16"] and T("geneva", "Num.13.2") == ["Num.13.1"])
check("Geneva Dan 3:30, a merged last slot, holds KJV 3:30 and 4:1-3; Geneva 4:1 is KJV 4:4",
      T("geneva", "Dan.3.30") == ["Dan.3.30", "Dan.4.1", "Dan.4.2", "Dan.4.3"]
      and T("geneva", "Dan.4.1") == ["Dan.4.4"])
check("Geneva Job 39:1 is KJV 38:39; its Job 41:1 is KJV 41:10",
      T("geneva", "Job.39.1") == ["Job.38.39"] and T("geneva", "Job.41.1") == ["Job.41.10"])
check("Geneva Rev 12:18 ('I stood on the sea sand') is the start of KJV 13:1",
      T("geneva", "Rev.12.18") == ["Rev.13.1"])
check("the Geneva has no 'Song of songs' verse: KJV Song 1:1 is named as reached from none",
      "Song.1.1" in M["geneva"]["kjv_without_verse"] and T("geneva", "Song.1.1") == ["Song.1.2"])
check("Geneva chapters read off the English are listed with both scores",
      {"Num.13", "Dan.4", "Job.40"} <= set(M["geneva"]["aligned_chapters"])
      and all(a["aligned"] > a["same_numbers"] for a in M["geneva"]["aligned_chapters"].values()))

# The others number as the KJV almost everywhere.
check("Darby and the ASV swap Phil 1:16-17, as the revisers' Greek orders them",
      all(T(s, "Phil.1.16") == ["Phil.1.17"] and T(s, "Phil.1.17") == ["Phil.1.16"]
          for s in ("darby", "asv")))
check("the ASV prints no Comma Johanneum: its 1 John 5:7 is KJV 5:6b",
      T("asv", "1John.5.7") == ["1John.5.6"] and "Comma" in M["asv"]["kjv_without_verse"]["1John.5.7"])
check("the ASV's omitted verses (Acts 8:37, John 5:4) are named, not hidden",
      {"Acts.8.37", "John.5.4"} <= set(M["asv"]["kjv_without_verse"])
      and R("asv", "Acts.8.37")["resolved"] is False)
check("Young's Gen 18:12 is KJV 18:11 (his numbers run one ahead in 18:11-14)",
      T("ylt", "Gen.18.12") == ["Gen.18.11"] and T("ylt", "Gen.18.14") == ["Gen.18.13", "Gen.18.14"])
check("Tyndale's Matt 5:48 holds KJV 5:47-48 (its 5:47 slot is empty)",
      T("tyndale", "Matt.5.48") == ["Matt.5.47", "Matt.5.48"]
      and R("tyndale", "Matt.5.47")["resolved"] is False)
check("this Tyndale holds ten books only (Genesis, the Gospels, Acts, Romans, 1 Corinthians, "
      "Hebrews, Revelation): Exodus is no verse of it",
      R("tyndale", "Exod.1.1")["resolved"] is False
      and len({c.split(".")[0] for c in M["tyndale"]["chapters"]}) == 10)
check("resolve: one verse, several KJV verses",
      R("geneva", "Dan.3.30") == {"resolved": True, "target": "kjv:Dan.3.30",
                                  "spans": ["kjv:Dan.3.30", "kjv:Dan.4.1", "kjv:Dan.4.2",
                                            "kjv:Dan.4.3"]})

# Each file against the registry.
for s, m in M.items():
    vals = [t for v in m["map"].values() for t in ([v] if isinstance(v, str) else v)]
    check(f"{s}: every target is a kjv: unit id", all(f"kjv:{t}" in kjv for t in vals))
    check(f"{s}: the map lists only verses whose reference changes",
          all(([v] if isinstance(v, str) else v) != [k] for k, v in m["map"].items()))
    check(f"{s}: every house row is in the map with its KJV verses",
          all(T(s, v) == r["kjv"] for v, r in m["house_rows"].items() if r["kjv"]))
    reached, verses = set(), 0
    for ch, have in m["chapters"].items():
        nums = range(1, have + 1) if isinstance(have, int) else map(int, have.split(","))
        for n in nums:
            verses += 1
            r = R(s, f"{ch}.{n}")
            if r["resolved"]:
                reached.update(r.get("spans", [r["target"]]))
    books = {c.split(".")[0] for c in m["chapters"]}
    check(f"{s}: {verses:,} verses; every KJV verse of its books is reached or named as not",
          verses == m["checked_against"]["verses"]
          and {k for k in kjv if k[4:].split(".")[0] in books and k not in reached}
          == {f"kjv:{e}" for e in m["kjv_without_verse"]})
    check(f"{s}: public domain, with the source's rights line and pin",
          m["rights"]["license"] == "public-domain" and "Public Domain" in m["source"]["rights_line"]
          and m["source"]["commit"].startswith("e1b254c"))

print(f"\n{passed} passed, {fails} failed")
sys.exit(1 if fails else 0)
