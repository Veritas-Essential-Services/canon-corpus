#!/usr/bin/env python3
# prov: 2026-10-03 drafted (Claude Code)
# fable_review: pending
"""The topical and dictionary layer: the reference reader rule by rule on
lines as the four books (and their scans) print them, the vote on fixtures
(offline, no corpus needed), then the committed data/topical/ files against
the KJV ids and their manifest."""
import collections, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import topical_read as R
import build_topical as B
import tsk_read as T

fails = passed = 0
def check(m, c):
    global fails, passed
    print(("ok    " if c else "FAIL  ") + m)
    if c: passed += 1
    else: fails += 1

def refs(text):
    return [(r["book"], r["c"], r["v"], r["c2"], r["v2"]) for r in R.refs(text)]

shape = T.kjv_shape()

# ---- the reader
check("Nave print: a book carries over ';' and ','",
      refs("Lineage of, Ex. 6:16-20; Josh. 21:10, 13; 1 Chr. 6:3.") ==
      [("Exod", 6, 16, 6, 20), ("Josh", 21, 10, 21, 10), ("Josh", 21, 13, 21, 13), ("1Chr", 6, 3, 6, 3)])
check("Smith print: the colon floats ('19 : 16, 17')",
      refs("1 Kings 19 : 16, 17. (B.C. about 900.)") == [("1Kgs", 19, 16, 19, 16), ("1Kgs", 19, 17, 19, 17)])
check("CCEL's Nave: 'Ge 48:5,14' and a new book after ';'",
      refs("Of Joseph's sons Ge 48:5,14; Ex 2:5-10") == [("Gen", 48, 5, 48, 5), ("Gen", 48, 14, 48, 14), ("Exod", 2, 5, 2, 10)])
check("whole chapters after ';' (Nave's 'Jer 20:4-7; 21; 22')",
      refs("Jer 20:4-7; 21; 22") == [("Jer", 20, 4, 20, 7), ("Jer", 21, None, 21, None), ("Jer", 22, None, 22, None)])
check("a number before a book is its ordinal, not a chapter ('Eze 12; 2Sa 4')",
      refs("Eze 12; 2Sa 4") == [("Ezek", 12, None, 12, None), ("2Sam", 4, None, 4, None)])
check("nor a verse ('Ge 48:5, 2 Sam 3:1')",
      refs("Ge 48:5, 2 Sam 3:1") == [("Gen", 48, 5, 48, 5), ("2Sam", 3, 1, 3, 1)])
check("single-chapter books: 'Jude 9' and 'Jude 1:3' are both verses",
      refs("Jude 9; Jude 1:3; Ob 1:3") == [("Jude", 1, 9, 1, 9), ("Jude", 1, 3, 1, 3), ("Obad", 1, 3, 1, 3)])
check("ordinals: 1Jo, 2 John, II Sam., 1 Ti; a bare Ti is Titus",
      refs("1Jo 3:12; 2 John 7; II Sam. 7:14; 1 Ti 2:5; Ti 1:5") ==
      [("1John", 3, 12, 3, 12), ("2John", 1, 7, 1, 7), ("2Sam", 7, 14, 7, 14), ("1Tim", 2, 5, 2, 5), ("Titus", 1, 5, 1, 5)])
check("a bare Jo. names no book (Joshua or John)", refs("Jo 3:16") == [])
check("OCR comma after the book ('Num, 12: 2')", refs("Miriam and Aaron. Num, 12: 2.") == [("Num", 12, 2, 12, 2)])
check("Torrey's Jdj is Judges", refs("Jdj 6:22-24") == [("Judg", 6, 22, 6, 24)])
check("a chapter range ('Lev. 11-15; Num. 19.')",
      refs("Lev. 11-15; Num. 19.") == [("Lev", 11, None, 15, None), ("Num", 19, None, 19, None)])
check("a range across chapters ('Ge 16:1-17:3')", refs("Ge 16:1-17:3") == [("Gen", 16, 1, 17, 3)])
check("the Apocrypha is read ('1Ma 7:40,45; Ecclus. 4:1')",
      refs("1Ma 7:40,45; Ecclus. 4:1") == [("1Macc", 7, 40, 7, 40), ("1Macc", 7, 45, 7, 45), ("Sir", 4, 1, 4, 1)])
check("a reference's position is its book's start (for the heading)",
      R.refs(".Marriage of Ex 6:23")[0]["at"] == len(".Marriage of "))
# edge cases (review 2026-10-03)
check("refs: a psalm's title is no reference, not the whole psalm",
      refs("Ps. 3 title") == refs("Ps. 51:title") == refs("Psalm 90 (title)") == []
      and refs("Ps. 51:title; 52:1") == [("Ps", 52, 1, 52, 1)])
check("refs: a one-chapter book keeps its verses after ';'",
      refs("Jude 6; 14") == [("Jude", 1, 6, 1, 6), ("Jude", 1, 14, 1, 14)])
check("refs: chapters listed with ',' are each a chapter",
      refs("Ps. 23, 24") == [("Ps", 23, None, 23, None), ("Ps", 24, None, 24, None)]
      and refs("Ps. 23, 1 Sam. 4") == [("Ps", 23, None, 23, None), ("1Sam", 4, None, 4, None)])
check("refs: 3 and 4 Maccabees, Susanna and Bel are read (as Apocrypha), 4 John is not",
      refs("3 Macc. 1:1") == [("3Macc", 1, 1, 1, 1)] and refs("IV Macc. 2:3") == [("4Macc", 2, 3, 2, 3)]
      and refs("Sus. 45") == [("Sus", 1, 45, 1, 45)] and refs("4 John 3") == [])
check("refs: 'Song of Solomon' and 'S. of S.' are the Song, positions kept",
      refs("Song of Solomon 2:1") == [("Song", 2, 1, 2, 1)]
      and R.refs("see S. of S. 2:1, 3")[1]["at"] == len("see S. of S. 2:1, "))
check("... but Nave's own 'Ex 32; Ac 7:40' is Exodus 32 (punctuation, not a word, follows)",
      refs("Makes the golden calf Ex 32; Ac 7:40") == [("Exod", 32, None, 32, None), ("Acts", 7, 40, 7, 40)])
check("refs: 'Is 40 days' is not Isaiah; 'Is. 40' and 'Am 5:24' still are",
      refs("Is 40 days") == [] and refs("Is. 40") == [("Isa", 40, None, 40, None)]
      and refs("Am 5:24") == [("Amos", 5, 24, 5, 24)])
check("osis: a range, a chapter, a cross-book range", R.osis_parts("Gen.4.1-Gen.4.16") == ("Gen", 4, 1, 4, 16)
      and R.osis_parts("2Sam.4") == ("2Sam", 4, None, 4, None) and R.osis_parts("Gen.50.26-Exod.1.1") is None)

# ---- the vote, on fixtures
para = {"text": "Diotrephes 3Jo 1:9,10", "tagged": [{"osis": "3John.1.1", "shown": "3Jo 1"}, {"osis": "3John.1.10", "shown": "10"}]}
c = B.candidates(para)
got = {(x["t"][:3], x["ccel"], x["reader"]) for x in c}
check("candidates: CCEL's mistag of 'Jude 1:9'-style refs is ccel-only; the verse it missed is reader-only",
      (("3John", 1, 1), True, False) in got and (("3John", 1, 9), False, True) in got and (("3John", 1, 10), True, True) in got)
check("kjv_id: a verse, a whole chapter, a range", B.kjv_id(("Gen", 1, 1, 1, 1), shape, B.APOCRYPHA)[0] == "kjv:Gen.1.1"
      and B.kjv_id(("Gen", 2, None, 2, None), shape, B.APOCRYPHA)[0] == "kjv:Gen.2.1-25"
      and B.kjv_id(("Gen", 1, None, 2, None), shape, B.APOCRYPHA)[0] == "kjv:Gen.1.1-2.25")
check("kjv_id: no such verse / chapter", B.kjv_id(("1Chr", 7, 88, 7, 88), shape, B.APOCRYPHA) == (None, "no such verse")
      and B.kjv_id(("Gal", 7, None, 7, None), shape, B.APOCRYPHA) == (None, "no such chapter"))
check("kjv_id: Esther 16 and Daniel 13 are the Greek additions, not KJV verses",
      B.kjv_id(("Esth", 16, 10, 16, 10), shape, B.APOCRYPHA) == (None, "apocrypha")
      and B.kjv_id(("Dan", 13, 1, 13, 1), shape, B.APOCRYPHA) == (None, "apocrypha")
      and B.kjv_id(("Esth", 10, 3, 10, 3), shape, B.APOCRYPHA)[0] == "kjv:Esth.10.3")
check("kjv_id: Sirach is the Apocrypha", B.kjv_id(("Sir", 4, 1, 4, 1), shape, B.APOCRYPHA) == (None, "apocrypha"))
check("heading: Nave's outline marks go, the words stay", B.heading("–Lineage of Ex 6:16-20") == "Lineage of")
check("heading: Torrey's dash goes", B.heading("Is of God — Ps 65:4.") == "Is of God")
check("slug", B.slug("Abel, Stone Of") == "abel-stone-of" and B.slug("ASS (DONKEY)") == "ass-donkey")
check("aligned: diff keeps order", B.aligned(["a", "b", "c", "d"], ["a", "x", "c", "d"]) == {0, 2, 3})

# ---- the committed files
D = os.path.join(ROOT, "data", "topical")
man = json.load(open(os.path.join(D, "manifest.json"), encoding="utf-8"))
check("manifest: rights block, public domain, prose not committed",
      man["rights"]["license"] == "public-domain" and "prose" in man["rights"]["committed"])
V = T.Verses(shape)
ids = set()
for w in B.WORKS:
    raw = open(os.path.join(D, w + ".jsonl"), "rb").read()
    L = man["layers"][w]
    check(f"{w}: sha256 = manifest", hashlib.sha256(raw).hexdigest() == L["sha256"])
    rows = [json.loads(x) for x in raw.decode("utf-8").splitlines()]
    check(f"{w}: rows = manifest ({len(rows)})", len(rows) == L["rows"])
    uids = [r["id"] for r in rows]
    check(f"{w}: ids unique and prefixed", len(set(uids)) == len(uids) and all(u.startswith(w + ":") for u in uids))
    ids |= set(uids)
    bad = n = 0
    places = []
    for r in rows:
        for t in (r["topics"] if "topics" in r else [r]):
            places.append(t)
            for rid in t["refs"]:
                n += 1
                b, c, v, c2, v2 = T.parse_ref_id(rid)
                if (b, c, v) not in V.index or (b, c2, v2) not in V.index or V.index[(b, c, v)] > V.index[(b, c2, v2)]:
                    bad += 1
    check(f"{w}: every reference is a KJV verse or run of verses ({n})", bad == 0 and n == L["counts"]["refs_in_rows"])
    check(f"{w}: in_print never exceeds the references", all(0 <= t["in_print"] <= len(t["refs"]) for t in places))
    check(f"{w}: no prose committed", all("text" not in r for r in rows))
    check(f"{w}: Apocrypha never as kjv:", all(not x.startswith("kjv:") for r in rows for t in (r.get("topics") or [r]) for x in t.get("apocrypha", [])))
    meas = L["by_reading"]
    check(f"{w}: two readings agree more often than either alone is printed",
          meas["both"]["share_printed"] > meas["ccel-only"]["share_printed"])

import topical
tp = topical.Topical()
hits = tp.by_verse("kjv:John.3.16")
check("loader: John 3:16 is cited in all four books' worth of places (Nave and Torrey at least)",
      {"nave", "torrey"} <= {h["work"] for h in hits})
check("loader: a range cites every verse in it (Nave's Nicodemus, John 3:1-21, reaches 3:20)",
      any(h["ref"] == "kjv:John.3.1-21" for h in tp.by_verse("kjv:John.3.20")))
check("loader: Easton's Abdon, with its Hitchcock id", (tp.entry("easton:abdon") or {}).get("hitchcock") == "a-p0.22")

print(f"\n{passed} passed, {fails} failed")
sys.exit(1 if fails else 0)
