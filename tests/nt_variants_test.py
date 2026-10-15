#!/usr/bin/env python3
"""
nt_variants_test.py -- the validator for the NT variant apparatus
(pipeline/build_nt_variants.py; STEPBible's TAGNT, eight printed editions).

    python3 tests/nt_variants_test.py

OFFLINE (always): the committed manifest entry (rights block, counts), the
pins, and the parsing rules on fixtures copied from TAGNT's rows.

AGAINST THE PINNED TAGNT (when data/corpus/tagnt/ holds it and data/nt/ is
built): a rebuild equals the manifest entry, the famous variants read as they
should, and nothing of TAGNT's English or Spanish is in the book.
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
import build_nt_variants as V  # noqa: E402

PASS = FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"ok   {label}")
    else:
        FAIL += 1
        print(f"FAIL {label}  {detail}")


print("--- manifest")
man = json.load(open(V.MANIFEST, encoding="utf-8"))
e = man.get(V.SLUG, {})
check("the apparatus has a manifest entry", bool(e))
check("its rights block: CC BY 4.0, STEPBible's request honoured, not served whole",
      e.get("rights", {}).get("redistribute_whole") is False
      and "CC BY 4.0" in e["rights"]["license"] and V.COMMIT in e["rights"]["source_url"])
s = e.get("stats", {})
check("every TAGNT word and verse was read: 142,096 words, 7,957 verses",
      (s.get("words"), s.get("verses")) == (142096, 7957), s)
check("4,737 verses carry an apparatus; 8,198 readings, 1,724 of them significant",
      (e.get("units"), s.get("readings"), s.get("significant")) == (4737, 8198, 1724),
      (e.get("units"), s.get("readings"), s.get("significant")))
check("the book is gitignored (rule 6)",
      "data/books/*.json" in open(os.path.join(REPO, ".gitignore"), encoding="utf-8").read())
check("both TAGNT files are pinned by sha256",
      len(V.FILES) == 2 and all(re.fullmatch(r"[0-9a-f]{64}", v) for v in V.FILES.values()))

print("--- parsing rules, on fixtures")
eds, extra = V.editions_of("NA28+NA27+Tyn+SBL+WH+Treg+TR»1+Byz«14.24+03+P66")
check("editions: in place, displaced by words, moved to another verse; manuscripts kept apart",
      eds == {"NA28": 0, "NA27": 0, "Tyn": 0, "SBL": 0, "WH": 0, "Treg": 0, "TR": 1,
              "Byz": "at 14.24"} and extra == ["03", "P66"], (eds, extra))
check("a word in every edition is no variant; upper case is significant, lower case minor",
      not V.significant("NKO") and V.significant("K") and V.significant("N(K)O")
      and not V.significant("N(k)O") and not V.significant("k"))
mv = V.meaning_variants("ἐν τοῖς οὐρανοῖς (T=en tois ouranois) in the heavens - "
                        "G1722=PREP + G3588=T-DPM + G3772=N-DPM in: TR+Byz")
check("a slot's other words: Greek, numbers and editions kept, TAGNT's English dropped",
      mv == [{"greek": "ἐν τοῖς οὐρανοῖς", "strongs": ["G1722", "G3588", "G3772"],
              "grammar": ["PREP", "T-DPM", "N-DPM"], "editions": ["TR", "Byz"]}], mv)
check("spelling variants by edition",
      V.spelling_variants("Tyn+WH: Δαυεὶδ ; +TR: Δαβὶδ ; ")
      == [{"editions": ["Tyn", "WH"], "greek": "Δαυεὶδ"}, {"editions": ["TR"], "greek": "Δαβὶδ"}])
check("a verse is filed under the KJV's number where TAGNT brackets one",
      V.ROW.match("2Co.13.13[13.14]#01=NKO").groups()[3:5] == ("13", "14"))

have = all(os.path.exists(V.local(r)) for r in V.FILES)
nt_built = os.path.exists(os.path.join(REPO, "data", "nt", "Rev", "tokens.jsonl"))
if not (have and nt_built):
    print("\nskip  the pinned TAGNT or the built NT is missing "
          "(build_nt_variants.py --fetch; rebuild_bible.py); the rebuild checks did not run")
else:
    print("--- rebuild")
    book, blob, built = V.build()
    check("a rebuild equals the committed manifest entry", built == e)
    u = {x["id"].split(":", 1)[1]: x for x in book["units"]}
    uids = json.load(open(os.path.join(REPO, "data", "uids", "wordhoard.uids.json"), encoding="utf-8"))["uids"]
    check("every unit names an existing KJV verse and its uid",
          all(f"kjv:{k}" in uids and x["lex"]["passage_uid"] == uids[f"kjv:{k}"] for k, x in u.items()))
    r = u["Matt.6.13"]["lex"]["readings"][-1]
    check("Matt 6:13: the doxology is TR and Byz's, a significant variant",
          r["words"][0] == "ὅτι" and r["in"] == ["TR", "Byz"] and r["significant"])
    r = u["1John.5.7"]["lex"]["readings"][0]
    check("1 John 5:7: the Comma is the TR's alone", r["in"] == ["TR"] and "Byz" in r["omit"])
    check("Acts 8:37 (no RP2018 verse) is filed on its KJV uid, the TR's alone",
          u["Acts.8.37"]["lex"]["readings"][0]["in"] == ["TR"])
    r = u["1Tim.3.16"]["lex"]["readings"][0]
    check("1 Tim 3:16: ὃς in the critical editions, θεὸς in TR and Byz, not an omission",
          r["words"] == ["ὃς"] and r["instead"][0]["greek"] == "θεὸς" and r["omit"] == [])
    check("Rom 16:25: the Byzantine text prints the doxology at 14:24, after 14:23",
          u["Rom.16.25"]["lex"]["word_order"][0]["moved"] == {"Byz": "at 14.24"})
    multi = [x for x in u.values() if "tagnt_refs" in x["lex"]]
    check(f"a KJV verse fed by two TAGNT verses lists both, and every entry names its own ({len(multi)}, "
          "Matt 17:14 among them)",
          "Matt.17.14" in u and "tagnt_refs" in u["Matt.17.14"]["lex"]
          and all(len(x["lex"]["tagnt_refs"]) > 1 and x["lex"]["tagnt_ref"] == x["lex"]["tagnt_refs"][0]
                  and all(e.get("tagnt") in x["lex"]["tagnt_refs"]
                          for k in ("readings", "meaning_variants", "word_order", "spelling_variants", "witnesses")
                          for e in x["lex"][k]) for x in multi)
          and not any("tagnt" in e for x in u.values() if "tagnt_refs" not in x["lex"]
                      for k in ("readings", "spelling_variants") for e in x["lex"][k]))
    check("nothing of TAGNT's English (Berean) or Spanish is in the book",
          "do deliver" not in blob.decode("utf-8") and "lleves" not in blob.decode("utf-8"))

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
