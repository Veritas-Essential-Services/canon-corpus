#!/usr/bin/env python3
"""
philo_test.py -- the validator for the Philo books (pipeline/build_philo.py;
Cohn-Wendland's Greek and Yonge's English, from First1KGreek).

    python3 tests/philo_test.py

OFFLINE (always): the committed manifest entries (rights block, CC BY-SA
label, alignment counts), the pins, and the scripture-reference rules on
fixtures (the versification maps are committed).

AGAINST THE PINNED TEI (when data/corpus/first1k/ holds it and data/nt/ is
built): a rebuild equals every manifest entry, the editors' references are out
of the Greek text, the OCR cruft is out of the English, and known passages are
where they belong.
"""
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "pipeline"))
import build_philo as P  # noqa: E402
import af_scripture as S  # noqa: E402

PASS = FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"ok   {label}")
    else:
        FAIL += 1
        print(f"FAIL {label}  {detail}")


# The sections the English file lacks (On the Special Laws only); every other
# treatise aligns one to one.
SPEC_UNMATCHED = 58

print("--- manifest")
man = json.load(open(P.MANIFEST, encoding="utf-8"))
slugs = [f"philo-{k}-{ed}" for _, k, _, _ in P.WORKS for ed in P.EDITIONS]
check("62 books: 31 treatises, Greek and English", len(slugs) == 62 and all(s in man for s in slugs),
      [s for s in slugs if s not in man][:5])
check("every entry carries the rights block: CC BY-SA 4.0, PD text, not served whole",
      all(man[s]["rights"]["redistribute_whole"] is False and "CC BY-SA 4.0" in man[s]["rights"]["license"]
          and P.COMMIT in man[s]["rights"]["source_url"] for s in slugs if s in man))
bad = []
for _, k, _, _ in P.WORKS:
    g, e = man.get(f"philo-{k}-cw", {}), man.get(f"philo-{k}-yonge", {})
    want = SPEC_UNMATCHED if k == "spec" else 0
    if not (g and e and e["units"] == e["alignment"]["matched"] == g["alignment"]["matched"]
            and g["units"] - g["alignment"]["matched"] == want == len(g["alignment"]["unmatched"])
            and not e["alignment"]["unmatched"]):
        bad.append(k)
check("every English section has its Greek; the Greek lacks an English only in Spec. (58 listed)",
      not bad, bad)
check("Spec.'s unmatched Greek sections are 1.177-193 and eight runs in book 2",
      man["philo-spec-cw"]["alignment"]["unmatched"][:2] == ["1.177", "1.178"]
      and "2.124" in man["philo-spec-cw"]["alignment"]["unmatched"])
check("the Greek books carry Strong's tagging and scripture counts; the English do not",
      all("tagging" in man[f"philo-{k}-cw"] and "scripture_refs" in man[f"philo-{k}-cw"]
          and "tagging" not in man[f"philo-{k}-yonge"] for _, k, _, _ in P.WORKS))
refs = sum(man[f"philo-{k}-cw"]["scripture_refs"] for _, k, _, _ in P.WORKS)
res = sum(man[f"philo-{k}-cw"]["scripture_refs_resolved"] for _, k, _, _ in P.WORKS)
check("Cohn-Wendland's scripture references: 1,835, of which 1,826 resolve to a KJV verse",
      (refs, res) == (1835, 1826), (refs, res))
check("books are gitignored (CC BY-SA, rule 6)",
      "data/books/*.json" in open(os.path.join(REPO, ".gitignore"), encoding="utf-8").read())
pins = P.pins()
check("all 62 TEI files are pinned by sha256",
      len(pins) == 62 and all(re.fullmatch(r"[0-9a-f]{64}", v) for v in pins.values()))

print("--- the editors' references, on fixtures")
lab = lambda raw, last=None: S.parse_label(P.cw_label(raw, last) or "")  # noqa: E731
check("'I Reg. 1,28' is 1 Samuel (1 Kingdoms)", lab("I Reg. 1,28") == [("lxx", "1Sam", 1, 28, None)])
check("'III Reg. 17,10' is 1 Kings", lab("III Reg. 17,10") == [("lxx", "1Kgs", 17, 10, None)])
check("'Psalm. 77,49' is a psalm", lab("Psalm. 77,49") == [("lxx", "Ps", 77, 49, None)])
check("'ibid. 2' after Gen. 30,1 is Gen 30:2", lab("ibid. 2", ("Gen.", 30, 1)) == [("lxx", "Gen", 30, 2, None)])
check("'ib. 6, 12' after Num. 6,9 is Num 6:12", lab("ib. 6, 12", ("Num.", 6, 9)) == [("lxx", "Num", 6, 12, None)])
check("'ib. v. 16' is a verse of the same chapter", lab("ib. v. 16", ("Lev.", 16, 1)) == [("lxx", "Lev", 16, 16, None)])
check("'Gen. 17,15. 16' is two verses of one chapter",
      lab("Gen. 17,15. 16") == [("lxx", "Gen", 17, 15, None), ("lxx", "Gen", 17, 16, None)])
check("'Gen. 1,27. 2,7' is a second chapter",
      lab("Gen. 1,27. 2,7") == [("lxx", "Gen", 1, 27, None), ("lxx", "Gen", 2, 7, None)])
check("'Gen. 2,7—9' is a range", lab("Gen. 2,7—9") == [("lxx", "Gen", 2, 7, 9)])
check("beta-code Latin restored: 'Lev. 26, 19. ξφ. δευτ. 28,23' cites Deuteronomy too",
      lab("Lev. 26, 19. ξφ. δευτ. 28,23") == [("lxx", "Lev", 26, 19, None), ("lxx", "Deut", 28, 23, None)])
check("'ibid.' alone is the verse last cited", lab("ibid.", ("Exod.", 3, 14)) == [("lxx", "Exod", 3, 14, None)])
check("a parenthesis naming no book is not a reference", P.cw_label("10, 23", None) is None)

ctx = P.scripture_context()
r = P.resolve(("lxx", "Ps", 77, 49, None), ctx)
check("Psalms are numbered as the LXX: Ps 77:49 is kjv:Ps.78.49, via Brenton",
      r["target"] == "kjv:Ps.78.49" and r["numbering"] == "lxx" and r["via"] == "brenton-kjv", r)
r = P.resolve(("lxx", "Deut", 23, 13, None), ctx)
check("elsewhere the KJV's numbers: Deut 23:13 (the paddle) is kjv:Deut.23.13; Brenton's reading kept",
      r["target"] == "kjv:Deut.23.13" and r["alt_target"] == "kjv:Deut.23.12" and r["numbering"] == "english", r)
r = P.resolve(("lxx", "Exod", 38, 26, None), ctx)
check("Exodus 35-40 by the LXX's chapters, via Brenton",
      r["resolved"] and r["numbering"] == "lxx" and r["via"] == "brenton-kjv", r)
check("a whole chapter does not resolve", not P.resolve(("lxx", "Gen", 34, None, None), ctx)["resolved"])

have = all(os.path.exists(P.local(r)) for r in pins)
nt_built = os.path.exists(os.path.join(REPO, "data", "nt", "Rev", "tokens.jsonl"))
if not (have and nt_built):
    print("\nskip  the pinned TEI or the built NT is missing "
          "(build_philo.py --fetch; rebuild_bible.py); the rebuild checks did not run")
else:
    print("--- rebuild")
    built = P.build()
    check("a rebuild equals every committed manifest entry",
          all(man.get(s) == e for s, (_, _, e) in built.items()),
          [s for s, (_, _, e) in built.items() if man.get(s) != e][:5])
    u = {x["id"]: x for b, _, _ in built.values() for x in b["units"]}
    check("On the Creation opens as Cohn prints it, and as Yonge Englished it",
          u["philo-opif-cw:1"]["text"].startswith("Τῶν ἄλλων νομοθετῶν")
          and u["philo-opif-yonge:1"]["text"].startswith("Of other lawgivers"))
    check("Conf. 146: the Logos, God's first-born, 'the eldest of his angels'",
          "τὸν πρωτόγονον αὐτοῦ λόγον" in u["philo-conf-cw:146"]["text"]
          and "first-born word" in u["philo-conf-yonge:146"]["text"])
    leg = u["philo-leg-cw:2.27"]
    check("Leg. 2.27 quotes the paddle, and its reference left the text for links[]",
          "πάσσαλος" in leg["text"] and "Deut." not in leg["text"]
          and any(x.get("target") == "kjv:Deut.23.13" for x in leg["links"]))
    greek = [x for i, x in u.items() if i.endswith("-cw:" + i.split(":")[1]) and "-cw:" in i]
    left = [x["id"] for x in greek if re.search(r"\((?:cf\. )?(?:Gen|Exod|Lev|Num|Deut|Psalm|ib)[^()]*\)", x["text"])]
    check("no editors' reference is left in any Greek text", not left, left[:5])
    check("Cohn-Wendland's additions are printed in angle brackets",
          sum(x["text"].count("⟨") for x in greek) > 500)
    eng = [x for i, x in u.items() if "-yonge:" in i]
    check("Bohn's running heads and colophons are out of the English",
          not any(re.search(r"HADDON|PHILO JUDAUS|ON SPECIAL LAWS\. 32", x["text"]) for x in eng))
    check("every unit's counterpart link points both ways",
          all(l["target"] in u and any(m.get("target") == x["id"] for m in u[l["target"]]["links"])
              for x in u.values() for l in x["links"] if l.get("type") in ("translation", "original")))

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
