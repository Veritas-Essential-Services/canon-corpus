#!/usr/bin/env python3
# prov: 2026-10-03 drafted (Claude Code)
# fable_review: pending
"""The commentary layer: the reference reader's commentary rules (the point
for the colon, 17th-century book forms, "ver. 31" and "ch. 3. 4" read in the
right book), CCEL's comments and Poole's verse numbers on fixtures (offline),
then the committed data/commentary/ files against the KJV ids and their
manifest."""
import hashlib, json, os, sys
import xml.etree.ElementTree as ET
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import topical_read as R
import build_commentary as C
import tsk_read as T

fails = passed = 0
def check(m, c):
    global fails, passed
    print(("ok    " if c else "FAIL  ") + m)
    if c: passed += 1
    else: fails += 1

def refs(text, here=None, **kw):
    return [(r["book"], r["c"], r["v"], r["v2"]) for r in R.refs(text, here=here, **kw)]

# ---- the reader, as the commentaries need it
check("JFB 1873: a point for the colon, only when asked ('Genesis 19. 1; 12. 2')",
      refs("Genesis 19. 1; 12. 2 with Exodus 15. 2", point=True) == [("Gen", 19, 1, 1), ("Gen", 12, 2, 2), ("Exod", 15, 2, 2)]
      and refs("Genesis 19. 1") == [("Gen", 19, None, None)])
check("a point-verse is not the ordinal of the next book ('Rom. 12. 17, 19. 1 Pet. 3. 9')",
      refs("Rom. 12. 17, 19. 1 Pet. 3. 9.", point=True) == [("Rom", 12, 17, 17), ("Rom", 12, 19, 19), ("1Pet", 3, 9, 9)])
check("Henry: a lower-case Roman chapter ('Heb. xi. 4'), but not after a comma ('Daniel, v. 3')",
      refs("as Heb. xi. 4", here=("Gen", 4)) == [("Heb", 11, 4, 4)]
      and refs("so Daniel, v. 3", here=("Dan", 6)) == [("Dan", 6, 3, 3)])
check("Poole's forms, only with old=True ('Psal. 104. 6. Ioh. 1. 3. Iob 38. 4')",
      refs("Psal. 104. 6. Ioh. 1. 3. Iob 38. 4.", point=True, old=True) == [("Ps", 104, 6, 6), ("John", 1, 3, 3), ("Job", 38, 4, 4)]
      and refs("Psal. 104. 6.", point=True) == [])
check("'ver. 31' after a reference is in its chapter ('Exod. 30. 25. to verse 31')",
      refs("anointed, Exod. 30.25. to verse 31.", here=("Dan", 9), point=True, old=True) == [("Exod", 30, 25, 25), ("Exod", 30, 31, 31)])
check("... but not across a sentence ('Isa. 53. 5. So here, v. 3' is the comment's own chapter)",
      refs("as Isa. 53. 5. So here, v. 3", here=("Matt", 8), point=True, old=True) == [("Isa", 53, 5, 5), ("Matt", 8, 3, 3)])
check("'ch. 1. 26' after a book named in words is in that book ('who Luke tells us ch. 1.26.')",
      refs("as the Angel Gabriel, who Luke tells us ch. 1.26. was sent", here=("Matt", 1), point=True, old=True) == [("Luke", 1, 26, 26)])
check("'Ezek. chap. 27. 28' is Ezekiel's, not the comment's book",
      refs("so did Ezek. chap. 27.28, 29. it was", here=("Jer", 25), point=True, old=True) == [("Ezek", 27, 28, 28), ("Ezek", 27, 29, 29)])
check("'Chap. 20. 12' after another book's reference is the comment's own book (Poole on Rev: 'Gal. 6.5. Chap. 20.12')",
      refs("2 Cor. 5.10. Gal. 6.5. Chap. 20.12", here=("Rev", 2), point=True, old=True) == [("2Cor", 5, 10, 10), ("Gal", 6, 5, 5), ("Rev", 20, 12, 12)])
check("'Philip' in prose is a man, not Philippians ('as Philip had done, Chap. 8.35.' on Acts)",
      refs("as Philip had done, Chap. 8.35.", here=("Acts", 15), point=True, old=True) == [("Acts", 8, 35, 35)])
check("a point closes each reference in old print ('chap. 7.34. & 25.10. Ezek. 26.13.')",
      refs("Isa. 24.7, 8. chap. 7.34. & 25.10. Ezek. 26.13.", here=("Jer", 16), point=True, old=True)
      == [("Isa", 24, 7, 7), ("Isa", 24, 8, 8), ("Jer", 7, 34, 34), ("Jer", 25, 10, 10), ("Ezek", 26, 13, 13)])
check("'chap. 23. ver. 24' is one reference", refs("See chap. 23. ver. 24. let. d.", here=("Ezek", 26), point=True, old=True) == [("Ezek", 23, 24, 24)])
check("CCEL Barnes' running heads cite nothing ('Chapter 1 - Verse 2'); Poole's 'Chap. 3. 4' does",
      refs("MATTHEW - Chapter 1 - Verse 2 INTRODUCTION", here=("Matt", 1)) == []
      and refs("See Chap. 3. 4.", here=("Gen", 1), point=True, old=True) == [("Gen", 3, 4, 4)])

# ---- CCEL: the print source rule, and a comment runs from its mark to the next
check("print source: Baker 1949 is flagged, 1871 is not",
      C.print_source("<printSourceInfo>Grand Rapids, Mich.: Baker Book House, 1949.</printSourceInfo>")["ccel_print_source_check"]
      and not C.print_source("<printSourceInfo>1871</printSourceInfo>")["ccel_print_source_check"])
thml = ('<ThML.body><div1 title="Genesis"><div2 title="Chapter 1"><p>Of the creation.</p>'
        '<scripCom osisRef="Bible:Gen.1.1"/><p>In the beginning: see Ps 33:6.</p>'
        '<scripCom osisRef="Bible:Gen.1.2"/><p>Without form.</p></div2></div1>')
cs = C.comments(thml, "jfb")
check("comments: one per mark, each to the next", [c["anchor"][:3] for c in cs] == [("Gen", 1, 1), ("Gen", 1, 2)]
      and "Ps 33:6" in R.plain(cs[0]["raw"]))

# ---- Poole: the verse numbers inline in the TEI
NS = "http://www.tei-c.org/ns/1.0"
def tei(body):
    return ET.fromstring(f'<div xmlns="{NS}" type="chapter" n="1"><head>CHAP. I.</head><p>{body}</p></div>')
counts = {}
import collections
counts = collections.Counter()
verses, ac = C.tcp_chapter("Gen", 1, tei(
    'IN the beginning<note place="bottom">To wit, of Time. Compare Ioh. 1. 3.</note> God created. '
    '2. And the Earth<note place="margin">Psal. 104. 6.</note> was void. 3 And God said<note place="bottom">By his word.</note>.'), 3, counts)
check("Poole: notes go to the verse whose number came before ('2.' and '3' both read)",
      [(v, len(d["notes"]), len(d["margin"])) for v, d in verses] == [(1, 1, 0), (2, 0, 1), (3, 1, 0)] and ac == "agrees")
verses, ac = C.tcp_chapter("Gen", 1, tei('One<note place="bottom">a</note>. 2. Two. 2. Three<note place="bottom">c</note>. 4. Four.'), 4, counts)
check("Poole: a misprinted number between two right ones is read by order (2, 2, 4 -> 2, 3, 4)",
      [v for v, _ in verses] == [1, 3] and ac == "by order")
verses, ac = C.tcp_chapter("Gen", 1, tei('One. 2. Two<note place="bottom">a</note>. <gap reason="missing" extent="2 pages"/> '
                                         '25 Later<note place="bottom">lost</note>.'), 30, counts)
check("Poole: after pages missing from the images, nothing is placed", [v for v, _ in verses] == [2] and ac == "differs")
el = ET.fromstring(f'<note xmlns="{NS}" place="bottom">see Ier. <gap reason="illegible"/> 51. 15. and Matth<g ref="char:EOLhyphen"/>ew 5. 3.</note>')
check("Poole: an unread word is a mark, and an end-of-line hyphen joins",
      C.tcp_flat(el) == "see Ier. ◊ 51. 15. and Matthew 5. 3.")

# ---- Clarke, read from scans (clarke_read.py), on fixtures
import clarke_read as CR
check("Clarke: a note heading's Roman numeral through its OCR ('XLH' is 42, 'HI' is 3); 'NOTES.--' has none",
      CR.heading_numeral("NOTES ON CHAP. XLH.") == 42 and CR.heading_numeral("NOTES ON PSALM HI.") == 3
      and CR.heading_numeral("NOTES.\u2014") is None)
check("Clarke: heads 'Verse 17. lemma]' and, in the 1835 New Testament, '25. lemma]'",
      [h[1:] for h in CR.heads("Verse 17. The priests\u2014stood firm] They stood")] == [(17, None, "The priests\u2014stood firm")]
      and [h[1:] for h in CR.heads("x\n25. Judas\u2014said, Master,\nis it I] What", bare=True)] == [(25, None, "Judas\u2014said, Master, is it I")]
      and CR.heads("x\n25. Judas] What") == [])
_shape = {"Gen": {1: 3, 2: 3, 3: 2}}
_kjv = CR.Kjv({"kjv:Gen.1.1": "In the beginning God created the heaven and the earth.",
               "kjv:Gen.1.2": "And the earth was without form, and void; and darkness was upon the face of the deep.",
               "kjv:Gen.1.3": "And God said, Let there be light: and there was light.",
               "kjv:Gen.2.1": "Thus the heavens and the earth were finished, and all the host of them.",
               "kjv:Gen.2.2": "And on the seventh day God ended his work which he had made.",
               "kjv:Gen.2.3": "And God blessed the seventh day, and sanctified it.",
               "kjv:Gen.3.1": "Now the serpent was more subtil than any beast of the field.",
               "kjv:Gen.3.2": "And the woman said unto the serpent, We may eat of the fruit."}, _shape)
_runs = [{"num": None, "heads": [(0, 1, None, "the beginning created"), (1, 3, None, "Let there be light")]},
         {"num": 7, "heads": [(2, 1, None, "the serpent was more subtil")]}]
check("Clarke: runs align to chapters in order by their lemmas, a chapter with no notes skipped (and a misread numeral outvoted)",
      CR.align(_runs, [("Gen", 1), ("Gen", 2), ("Gen", 3)], _kjv) == [("Gen", 1), ("Gen", 3)])
check("Clarke: the chronology margin, the Bible text, and the margin's references are not the note",
      CR.classify("A. M. 3278. B. C. 726.", "Gen", 1, _kjv) == "chronology"
      and CR.classify("And the earth was without form, and void; and darkness was upon the face", "Gen", 1, _kjv) == "bible"
      and CR.classify("xxiv. 11 ; 2 Kings xvii. 13 ; 1 Chron. xxvi. 28 ; xxix. 29 ; 2 Chron.", "Gen", 1, _kjv) == "margin"
      and CR.classify("P Mai. iii. 10. 1 Or, store-houses. * Neh. xiii. 13.", "Gen", 1, _kjv) == "margin"
      and CR.classify("Jeremiah gives us his character at large, chap. xxii. 13, to which the reader will refer.", "Gen", 1, _kjv) == "note")
check("Clarke: 'ver. 407' after 'Iliad i.,' is Homer's line; 'See ver. 35' is this chapter's",
      CR.citations("Iliad i., ver. 407. See ver. 35, and Exod. iii. 7", "Exod", 9) == [("Exod", 9, 35, 9, 35), ("Exod", 3, 7, 3, 7)])

# ---- the committed files
D = os.path.join(ROOT, "data", "commentary")
man = json.load(open(os.path.join(D, "manifest.json"), encoding="utf-8"))
check("manifest: rights block, public domain, prose not committed",
      man["rights"]["license"] == "public-domain" and "prose" in man["rights"]["committed"])
shape = T.kjv_shape()
V = T.Verses(shape)
def valid(rid):
    b, c, v, c2, v2 = T.parse_ref_id(rid)
    return (b, c, v) in V.index and (b, c2, v2) in V.index and V.index[(b, c, v)] <= V.index[(b, c2, v2)]
for w in C.WORKS:
    raw = open(os.path.join(D, w + ".jsonl"), "rb").read()
    L = man["layers"][w]
    check(f"{w}: sha256 = manifest", hashlib.sha256(raw).hexdigest() == L["sha256"])
    rows = [json.loads(x) for x in raw.decode("utf-8").splitlines()]
    check(f"{w}: rows = manifest ({len(rows)})", len(rows) == L["rows"] == L["counts"]["comments"])
    ids = [r["id"] for r in rows]
    check(f"{w}: ids unique and prefixed", len(set(ids)) == len(ids) and all(i.startswith(w + ":") for i in ids))
    refs_all = [x for r in rows for x in [r["on"]] + r["cites"] + r.get("parallels", [])]
    check(f"{w}: every place is a KJV verse or run of verses ({len(refs_all)})", all(valid(x) for x in refs_all))
    check(f"{w}: citations = manifest", sum(len(r["cites"]) for r in rows) == L["counts"]["citations"])
    check(f"{w}: anchors are read, not assumed", {r["anchor"] for r in rows}
          <= {"agrees", "differs", "unread", "by order", "both printings", "one printing"})
    check(f"{w}: no prose committed", all(set(r) <= {"id", "on", "anchor", "cites", "parallels", "in_print"} for r in rows))
    tc = L["treasury_check"]["cites"]
    check(f"{w}: the Treasury lists its citations at that verse far more than at an unrelated one",
          tc["in_treasury_at_that_verse"] > 10 * tc["in_treasury_at_an_unrelated_verse"])
srcs = {w: L["source"]["files"] for w, L in man["layers"].items()}
check("Barnes: CCEL's print source (Baker, 1949) is flagged for a person to look at",
      srcs["barnes"][0]["ccel_print_source_check"] is True)
check("Poole: both volumes CC0, first edition dated", [(f["tcp_licence"], f["edition_date"]) for f in srcs["poole"]]
      == [("CC0 1.0", "1683"), ("CC0 1.0", "1685")])
check("Clarke: two printings of each Testament, every scan pinned",
      {(f["testament"], f["printing"].split(", ")[-2]) for f in srcs["clarke"]}
      == {("Old Testament", "1843"), ("Old Testament", "1846"), ("New Testament", "1846"), ("New Testament", "1835")}
      and all(len(f["sha256"]) == 64 for f in srcs["clarke"]))
_cl = [json.loads(x) for x in open(os.path.join(D, "clarke.jsonl"), encoding="utf-8")]
check("Clarke: a note placed in one printing only commits no citation",
      all(not r["cites"] for r in _cl if r["anchor"] == "one printing")
      and sum(r["anchor"] == "both printings" for r in _cl) > 12000)
check("Clarke: no note cites its own verse", all(r["on"].split("-")[0] not in r["cites"] for r in _cl))
check("Poole: two thirds of the margin's parallel places are the Treasury's too",
      man["layers"]["poole"]["treasury_check"]["parallels"]["in_treasury_at_that_verse"] > 0.6)
col = json.load(open(os.path.join(D, "collation.json"), encoding="utf-8"))
check("collation: every CCEL work's wording was compared with a period printing",
      set(col) == {w for w, d in C.WORKS.items() if d["scans"]} and all(p["located"] >= 300 for x in col.values() for p in x.values()))

import commentary
cm = commentary.Commentary()
check("loader: John 3:16 has a comment in every work", {r["work"] for r in cm.on("kjv:John.3.16")} == set(C.WORKS))
check("loader: and is cited from elsewhere", any(h["on"] != "kjv:John.3.16" for h in cm.citing("kjv:John.3.16")))

print(f"\n{passed} passed, {fails} failed")
sys.exit(1 if fails else 0)
