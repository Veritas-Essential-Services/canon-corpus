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

# --- round 7: what the reviewers found the reader inventing ----------------
check("'N]' is the apparatus's line marker, never a verse",
      refs("9] Ps. 18, 6. 16] Io. 1,10. 17] I Tim. 1,15.", "lat") == ["Ps 18:6", "John 1:10", "1Tim 1:15"])
check("... and '[17]' in brackets is still not taken for a marker: the reference stays, its chapter read",
      refs("8 Esth. 4, [17]", "grc") == ["Esth 4"])
check("... nor a verse closing a lemma: 'Ps. 18, 6] cf.' is Ps 18:6",
      refs("Ps. 18, 6] cf.", "lat") == ["Ps 18:6"] and refs("Ps. 18, 6 ] cf.", "lat") == ["Ps 18:6"]
      and refs("Ps. 18,  6] cf.", "lat") == ["Ps 18:6"] and refs("Ps. 18 , 6] cf.", "lat") == ["Ps 18:6"]
      and refs("Ps. XVIII, 6] cf.", "lat") == ["Ps 18:6"] and refs("Ps. xviii, 6] cf.", "lat") == ["Ps 18:6"])
check("... nor the end of a verse run closing a lemma: '3-5]', '2-3]', '6—9]', '6; 20, 9]', '6 et 9]'",
      refs("Matth. 7, 3-5] cf.", "lat") == ["Matt 7:3-5"] and refs("Es. 53, 2-3] cf.", "lat") == ["Isa 53:2-3"]
      and refs("Ps. 18, 6—9] cf.", "lat") == ["Ps 18:6-9"]
      and refs("Ps. 18, 6; 20, 9] cf.", "lat") == ["Ps 18:6", "Ps 20:9"]
      and refs("Ps. 18, 6 et 9] cf.", "lat") == ["Ps 18:6", "Ps 18:9"]
      and refs("Ps. 18, 6 — 9] cf.", "lat") == ["Ps 18:6-9"]
      and refs("Ps. 18, 6 et 9, 12] cf.", "lat") == ["Ps 18:6", "Ps 9:12"])
check("... but a number after a verse is the next line's marker: 'Es. 1, 11, 24] Ioh.'",
      refs("20] Es. 1, 11, 24] Ioh. 4, 23.", "lat") == ["Isa 1:11", "John 4:23"]
      and refs("Ps. 18, 6, 9] Io. 1, 10.", "lat") == ["Ps 18:6", "John 1:10"])
check("line runs are markers: '15-17]' (lines) and '13-217, 4]' (line 13 to page 217, line 4)",
      refs("13] Matth. 19, 8. 15-17] Matth. 19, 4.", "lat") == ["Matt 19:8", "Matt 19:4"]
      and refs("1] Apoc. 2, 6. 13-217, 4] cf. Iren.", "lat") == ["Rev 2:6"])
check("... unless they follow a chapter: 'Es. 53, 2-3, 11]' is Isa 53:2-3, then line 11",
      refs("6] Es. 53, 2-3, 11] Es. 52, 14.", "lat") == ["Isa 53:2-3", "Isa 52:14"])
check("Sulpicius cites chapters: '5 Gen. 1. 9 Gen. 2.' is Gen 1 and line 9, not Gen 1:9",
      refs("5 Gen. 1. 9 Gen. 2. 18 Gen. 4.", "lat") == ["Gen 1", "Gen 2", "Gen 4"])
check("... but a lined note that writes 'chapter, verse' keeps an OCR full stop's verse",
      refs("1 Exod. 3, 5 2 Matth. 10. 10 Luc. 10, 4", "lat") == ["Exod 3:5", "Matt 10:10", "Luke 10:4"])
check("'28, 12 et 13' is two verses, not chapter 13",
      refs("7 Deut. 28, 12 et 13. 11 Deut. 5, 1.", "lat") == ["Deut 28:12", "Deut 28:13", "Deut 5:1"])
check("'et' may go back a verse; 'et 3, 4' opens a chapter",
      refs("8] Ps. 17, 14 et 8.", "lat") == ["Ps 17:14", "Ps 17:8"]
      and refs("1 Gen. 2, 3 et 3, 4", "lat") == ["Gen 2:3", "Gen 3:4"])
check("'2 et 3 Exod.': after 'et' the number is a verse, not a chapter, even with a book next",
      refs("Gen. 1, 2 et 3 Exod. 4, 5", "lat") == ["Gen 1:2", "Gen 1:3", "Exod 4:5"])
check("... but '3 Esdr.' is a book: the Vulgate's 3 and 4 Esdras are the Apocrypha's 1 and 2 Esdras",
      refs("Gen. 1, 2 et 3 Esdr. 4, 5", "lat") == ["Gen 1:2", "1Esd 4:5"]
      and refs("20 3 Esdr. 3, 4 sqq.", "lat") == ["1Esd 3:4"] and refs("IV Esdr. 2, 1", "lat") == ["2Esd 2:1"])
check("GCS: a spaced em-dash between entries is no range",
      refs("2 vgl. Deut. 29, 5 — 15 — 18", "grc") == ["Deut 29:5"]
      and refs("6 Vgl. Röm. 4, 17. — 8 Esth. 4, 2", "grc") == ["Rom 4:17", "Esth 4:2"])
check("... but one that ends the entry is ('Matth. 7, 3 — 5;')",
      refs("23 ff Matth. 7, 3 — 5; Luk. 6, 41. 42", "grc")[0] == "Matt 7:3-5")
check("a verse before the next book is the verse ('Is. 53, 4 Matth.'), not a numbered book",
      refs("cf. Is. 53, 4 Matth. 8, 17", "lat") == ["Isa 53:4", "Matt 8:17"])
check("a range into another chapter keeps its start and invents nothing",
      refs("Act. 21, 30 - 23,2", "lat") == ["Acts 21:30"] and refs("Matth. 5, 3-7, 29", "lat") == ["Matt 5:3"])
ctx_ = T.scripture_context()
r = F.resolve(F.parse("III Reg. 20 (21), 13", "lat")[0], "lat", ctx_)
check("a bracket is read by both its numbers: III Reg. 20 (21), 13 is Naboth, the KJV's 1 Kgs 21:13 "
      "(the chapters swap, so with no order measured the other stays open)",
      r["target"] == "kjv:1Kgs.21.13" and r["bracket"] == "greek-first"
      and r.get("alt_target") == "kjv:1Kgs.20.13")
r = F.resolve(F.parse("III Reg. 20 (21), 13", "lat")[0], "lat", ctx_, bracket_pref="greek-first")
check("... and in an edition whose brackets go Greek-first, it is decided", r["target"] == "kjv:1Kgs.21.13"
      and "numbering_undecided" not in r)
r = F.resolve(F.parse("Psalm. 73 (74), 5", "grc")[0], "grc", ctx_)
check("Dindorf's 'Psalm. 73 (74), 5' (the axes) is the KJV's 74:5, whatever a content vote says",
      r["target"] == "kjv:Ps.74.5" and r["map"] == "brenton+bracket")
r = F.resolve(F.parse("Hier. 31 (38), 31", "lat")[0], "lat", ctx_)
check("Reiter puts the Hebrew first: 'Hier. 31 (38), 31' is the KJV's Jer 31:31",
      r["target"] == "kjv:Jer.31.31" and r["bracket"] == "kjv-first")
r = F.resolve(F.parse("Jes. 9, 6", "grc")[0], "grc", ctx_, lambda b: ("lxx", False))
check("Swete's Isaiah 9 is the English chapter: Holl's 'Jes. 9, 6' is the KJV's 9:6, not 9:7",
      r["target"] == "kjv:Isa.9.6")
r = F.resolve(F.parse("Jerem. 32, 1. 2", "grc")[0], "grc", ctx_, lambda b: ("lxx", False))
check("Swete's Jer 32:1 is the cup, the KJV's 25:15", r["target"] == "kjv:Jer.25.15")
r = F.resolve(F.parse("Ps. 112, 7-9", "grc")[0], "grc", ctx_, lambda b: ("lxx", False))
check("a range's end is read in its start's numbering: LXX Ps 112:7-9 is the KJV's 113:7-9",
      r["target"] == "kjv:Ps.113.7" and r.get("through") == "kjv:Ps.113.9")
r = F.resolve(F.parse("Ps. 112, 7-10", "grc")[0], "grc", ctx_, lambda b: ("lxx", False))
check("a range end the start's numbering lacks (LXX Ps 112:10) is dropped, never read back to 112",
      r["target"] == "kjv:Ps.113.7" and "through" not in r)

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
check("an LXX editor's lxx+hebrew votes (a title as verse 1) lend the Hebrew nothing against the English",
      N.shares(C({"existence:lxx": 100, "existence:lxx+hebrew": 20, "content_verse:english": 5}), "grc")["hebrew"]
      < 0.01)
check("... while a hebrew+english vote still counts against the LXX",
      N.shares(C({"existence:lxx": 10, "existence:hebrew+english": 10}), "grc")["lxx"] < 0.6)
L = {"vulgate": 0.94, "hebrew": 0.05, "english": 0.01}
got = N.decide(C({"existence:hebrew": 1}), "lat", L, W, "vulgate", 0.94)
check("one OCR digit does not move an edition off the pool's numbering; the rival stays open",
      got[0] == "vulgate" and got[2] == ["hebrew"])
got = N.decide(C({"existence:hebrew+english": 1, "content_chapter:hebrew+english": 1}), "grc", P, W, "lxx", 0.8)
check("two votes the Hebrew and English share rule out the LXX but leave those two undecided",
      got[0] != "lxx" and set([got[0]] + got[2]) == {"hebrew", "english"})
m = N.load()
check("the committed measure: Pusey's Psalms are Septuagint-numbered",
      m[0][("grc", "Philip Edward Pusey", "Ps")][0] == "lxx")
check("the committed measure: Heikel's Psalms are English-numbered, the Hebrew undecided",
      m[0][("grc", "Ivar A. Heikel", "Ps")][0] == "english"
      and m[0][("grc", "Ivar A. Heikel", "Ps")][2] == ("hebrew",))
check("the committed measure: Halm's rest is the Vulgate's, decided (its one Hebrew vote was a line number)",
      m[0][("lat", "Karl Halm", "rest")][0] == "vulgate" and m[0][("lat", "Karl Halm", "rest")][2] == ())
check("the committed measure: Reifferscheid & Wissowa's Psalms are the Vulgate's (no invented verse votes)",
      m[0][("lat", "August Reifferscheid & Georg Wissowa", "Ps")][0] == "vulgate")
got = N.decide(C({"existence:lxx": 1}), "grc", {"lxx": 0.46, "hebrew": 0.0, "english": 0.54}, W, "english", 0.54)
check("one vote against a near-even pool is not overruled by it: the pool's numbering stays open instead",
      got[0] == "lxx" and "english" in got[2])
nobody = N.scheme_for({"source": {"edition": {"editor": "Nobody Listed"}}}, "grc", m)
check("an editor with no row reads as the pool, with the pool's undecided rivals, like a listed one with no votes",
      nobody("Jer") == m[1][("grc", "Jer")])
# the Latin "rest" pool as it stood: 200 rounds stopped at vulgate 0.9421, the fixed point is 0.9422
V8 = C({"existence:hebrew": 5, "existence:hebrew+english": 5, "existence:vulgate": 71,
        "existence:vulgate+english": 104, "existence:vulgate+hebrew": 11})
check("shares() runs to a fixed point, not a fixed number of rounds: 200 rounds is not there yet",
      N.shares(V8, "lat") == N.shares(V8, "lat", tol=1e-15, rounds=10 ** 6)
      and N.shares(V8, "lat") != N.shares(V8, "lat", tol=0, rounds=200))
heikel = N.scheme_for({"source": {"edition": {"editor": "Ivar A. Heikel"}}}, "grc", m)
r = F.resolve(F.parse("Psal. 7, 16ff.", "grc")[0], "grc", ctx, heikel)
check("... so his Ps 7:16 names both verses and says the numbering is undecided",
      {r["target"], r.get("alt_target")} == {"kjv:Ps.7.15", "kjv:Ps.7.16"} and r.get("numbering_undecided"))
r = F.resolve(F.parse("Psal. 72, 8", "grc")[0], "grc", ctx, heikel)
check("... and his Ps 72:8 is the KJV's, the Hebrew and English agreeing", r["target"] == "kjv:Ps.72.8"
      and "numbering_undecided" not in r)

print(f"{PASS} passed, {len(FAIL)} failed")
if FAIL:
    for f in FAIL:
        print("  FAILED:", f)
    sys.exit(1)
