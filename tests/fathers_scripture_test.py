#!/usr/bin/env python3
"""Offline tests for fathers_scripture.py: the editors' scripture references
in the Greek and Latin fathers, read and resolved. No network, no corpus (the
versification maps and the uid registry are committed).
Run:  python3 tests/fathers_scripture_test.py

Every fixture is a note as an edition prints it (CSEL, GCS, Archambault, the
English editors), and each check names the trap it guards.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import fathers_scripture as F  # noqa: E402
import tag_fathers as T  # noqa: E402

PASS = 0
FAIL = []


def check(label, cond):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)


def refs(label, family):
    return [F.printed(r) for r in F.parse(label, family)]


# --- reading ---------------------------------------------------------------
check("CSEL: a number after bare space is the next line, not a verse",
      refs("10 cf. Gal. 2, 14 12 Gal. 2, 14. 15", "lat") == ["Gal 2:14", "Gal 2:14", "Gal 2:15"])
check("CSEL: a number after a verse and before a book is the next line",
      refs("23 Matth. 1, 15. 25 Luc. 3, 23.", "lat") == ["Matt 1:15", "Luke 3:23"])
check("CSEL: II Reg. is 2 Samuel; a range and a further verse",
      refs("20 cf. II Reg. 11, 3-5. 27 22 Ps. 50, 6", "lat") == ["2Sam 11:3-5", "2Sam 11:27", "Ps 50:6"])
check("CSEL: an em-dash range, then a new book after a semicolon",
      refs("15 Eph. 5, 31—32; Matth. 19, 5", "lat") == ["Eph 5:31-32", "Matt 19:5"])
check("CSEL: '. 20, 2' opens a new chapter of the same book",
      refs("13 cf. Apoc. 12. 9. 20, 2", "lat") == ["Rev 12:9", "Rev 20:2"])
check("CSEL: Jerome's '32 (39), 30' keeps the other chapter number",
      refs("4 *Hier. 32 (39), 30", "lat") == ["Jer 32(39):30"])
check("Latin Iud. is Judges; German Jud. is Jude",
      refs("4 Iud. 1, 19", "lat") == ["Judg 1:19"] and refs("Jud. 9", "grc") == ["Jude 1:9"])
check("an Arabic number before a book in a line-numbered note is the line",
      refs("1 vgl. I Kor. 12. 31. — 3 Joh. 13, 8.", "grc") == ["1Cor 12:31", "John 13:8"])
check("... unless the name alone is no book (1 Cor.)",
      refs("1 Cor. i. 24.", "grc") == ["1Cor 1:24"])
check("a numbered book after a semicolon starts a new reference",
      refs("1 Cor. 15, 28; 2 Cor. 5, 21", "lat") == ["1Cor 15:28", "2Cor 5:21"])
check("Archambault: Roman chapters, 'suiv.', '; XIII, 21' and ', et' in one book",
      refs("cf. Deut., IV, 34; Exod., VI, 1 suiv.; XIII, 21; XVI, 10, et Actes, XIII, 17", "grc")
      == ["Deut 4:34", "Exod 6:1", "Exod 13:21", "Exod 16:10", "Acts 13:17"])
check("Archambault: 'XV, 1, 2' is two verses",
      refs("cf. JEAN, XV, 1, 2", "grc") == ["John 15:1", "John 15:2"])
check("English editors: lower-case Roman chapters, 'S.' before the book",
      refs("S. Joan. viii. 39.", "grc") == ["John 8:39"] and refs("cf. Ge xi 4", "grc") == ["Gen 11:4"])
check("GCS: '2 Ps.' is line 2 and the Psalms",
      refs("2 Ps. 44, 2 – 3 Ps. 44, 2.", "grc") == ["Ps 44:2", "Ps 44:2"])
check("OCR: a Cyrillic H in Hier. and 'Lue.' for Luc. are read",
      refs("3 *Нier. 17, 19", "lat") == ["Jer 17:19"] and refs("11 cf. Lue. 15, 22", "lat") == ["Luke 15:22"])
check("not scripture: Philo, Josephus, Lactantius's own books",
      refs("1 Philo de sacr. 13 (172, 17; I 224, 2 C.)", "lat") == []
      and refs("et de bell. Iud. IIII 1, 44", "lat") == []
      and refs("INSTITUTIONES 3-7] IV 13, 8.", "lat") == [])
check("a two-letter siglum with no verse is not a reference",
      refs("20 paster Mt. 2 emeritos", "lat") == [])

# --- resolving -------------------------------------------------------------
ctx = T.scripture_context()


def one(label, family):
    return F.links_for(label, family, "note", ctx)


r = one("22 Ps. 50, 6", "lat")[0]
check("Latin OT goes through the Vulgate map: Ps 50:6 is the KJV's Ps 51:4",
      r["resolved"] and r["target"] == "kjv:Ps.51.4" and r["rule"] == "note/vulgate"
      and r.get("alt_target") == "kjv:Ps.50.6")
r = one("17 Ps. 32, 17.", "grc")[0]
check("Greek OT goes through Brenton: Ps 32:17 is the KJV's Ps 33:17",
      r["resolved"] and r["target"] == "kjv:Ps.33.17" and r["rule"] == "note/brenton")
r = one("21 Ioh. 1, 14", "lat")[0]
check("NT is the KJV's numbering", r["target"] == "kjv:John.1.14" and r["rule"] == "note/nt")
r = one("20 cf. II Reg. 11, 3-5", "lat")[0]
check("a range keeps its last verse", r["target"] == "kjv:2Sam.11.3" and r["through"] == "kjv:2Sam.11.5")
r = one("27 Vgl. Job. 4, 35.", "grc")[0]
check("OCR twin: Job 4:35 does not exist, John 4:35 does",
      r["resolved"] and r["target"] == "kjv:John.4.35" and r["rule"].endswith("+ocr-twin")
      and r["read_as"] == "John")
r = one("3 Gen. 18", "lat")[0]
check("a whole chapter stays unresolved, saying so", not r["resolved"] and "chapter" in r["why"])
r = one("6 Tob. 12, 19", "lat")[0]
check("a book outside the KJV stays unresolved", not r["resolved"] and "outside" in r["why"])
r = one("27 Matth. 6, 84", "lat")[0]
check("a verse that does not exist stays unresolved", not r["resolved"])

check("Greek 1 Esdras is the apocryphal book; 2 Esdras 11 is Nehemiah 1 by Brenton's map",
      not one("Vgl. 1 Esdr. 4, 41", "grc")[0]["resolved"]
      and one("Vgl. 2 Esdr. 11, 1", "grc")[0]["target"] == "kjv:Neh.1.1")
check("Latin 2 Esdras is Nehemiah", one("4 II Esdr. 8, 10", "lat")[0]["target"] == "kjv:Neh.8.10")

# --- each edition's numbering (fathers_numbering.py) ------------------------
import fathers_numbering as N  # noqa: E402

eng = lambda b: ("english", False)  # noqa: E731
heb = lambda b: ("hebrew", False)  # noqa: E731
r = F.resolve(F.parse("Psal. 72, 8", "grc")[0], "grc", ctx, eng)
check("an edition measured as English-numbered reads Ps 72:8 as the KJV's, LXX kept as alt",
      r["target"] == "kjv:Ps.72.8" and r.get("alt_target") == "kjv:Ps.73.8"
      and r["numbering"] == "english" and r["map"] == "kjv")
r = F.resolve(F.parse("Psal. 7, 16ff.", "grc")[0], "grc", ctx, heb)
check("a Hebrew-numbered edition counts the psalm's title as verse 1: Ps 7:16 is the KJV's 7:15",
      r["target"] == "kjv:Ps.7.15" and r["numbering"] == "hebrew" and r["map"] == "bhs")
check("'Psal. 7, 16ff. 23 Exod.': the 23 after 'ff.' is the next line, not Ps 23",
      refs("18 Psal. 7, 16ff. 23 Exod. 3, 2", "grc") == ["Ps 7:16", "Exod 3:2"])
r = F.resolve(F.parse("Ps. 113, 25", "grc")[0], "grc", ctx, eng)
check("... and a verse only the Septuagint numbers falls back to its map, saying so",
      r["resolved"] and r["numbering"] == "lxx" and "english numbering has no such verse" in r["why_numbering"])
r = F.resolve(F.parse("Ps. 132, 7", "grc")[0], "grc", ctx)
check("an LXX-numbered edition still reads a verse only the English has as the English",
      r["target"] == "kjv:Ps.132.7" and r["numbering"] == "english")
R = N.readings("Dan", 3, 24, "lat", ctx)
check("a Vulgate verse with no KJV verse (Dan 3:24, the Song of the Three) exists",
      R["vulgate"] == N.NO_KJV and R["english"] == "kjv:Dan.3.24")
R = N.readings("Ps", 7, 1, "grc", ctx)
check("a psalm title is verse 1 in the Hebrew count and exists there", R["hebrew"] == N.NO_KJV)
W = {"existence": 2.9, "chapter": 2.1, "verse": 1.07}
P = {"lxx": 0.8, "hebrew": 0.08, "english": 0.12}
C = __import__("collections").Counter
check("one existence and one chapter vote for the English outweigh a pool that is 80% LXX",
      N.decide(C({"existence:english": 1, "content_chapter:english": 1}), "grc", P, W)[0] == "english")
check("a vote two numberings share helps both; the content vote between them decides",
      N.decide(C({"existence:hebrew+english": 1, "content_verse:hebrew": 2}), "grc", P, W)[0] == "hebrew")
check("one verse-level vote against the same pool: it leans on the pool",
      N.decide(C({"content_verse:english": 1}), "grc", P, W)[0] == "lxx")
check("ten votes split evenly: mixed, read reference by reference",
      N.is_mixed(C({"content_chapter:english": 5, "content_verse:lxx": 5}), "grc"))
m = N.load()
check("the committed measure: Pusey's Psalms are Septuagint-numbered",
      m[0][("grc", "Philip Edward Pusey", "Ps")][0] == "lxx")

print(f"{PASS} passed, {len(FAIL)} failed")
if FAIL:
    for f in FAIL:
        print("  FAILED:", f)
    sys.exit(1)
