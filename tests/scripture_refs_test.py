#!/usr/bin/env python3
"""Checks for pipeline/scripture_refs.py, the master map of how old books
cite scripture: one example per convention, the hard cases and their rules,
and the words that must never be taken for books. Offline.

    python3 tests/scripture_refs_test.py"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import scripture_refs as S

PASS = 0
FAIL = []
def check(label, cond, detail=""):
    global PASS
    if cond: PASS += 1
    else: FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label + ("" if cond else f"   {detail}"))

def osis(text, profile="protestant", **kw):
    return [d.get("osis") for d in S.find(text, profile, **kw) if d.get("osis")]

def one(text, want, profile="protestant", label=None):
    got = osis(text, profile)
    check(label or f"{text!r} -> {want}", got == want, got)

# ---------------------------------------------------------------- the conventions
one("Rom. 8:28", ["Rom.8.28"], label="modern: Rom. 8:28")
one("Romans 8:28", ["Rom.8.28"], label="full name: Romans 8:28")
one("Rom. 8. 28.", ["Rom.8.28"], label="Puritan: Rom. 8. 28.")
one("Rom. viii. 28", ["Rom.8.28"], label="Roman chapter: Rom. viii. 28")
one("Psal. cxix. 105", ["Ps.119.105"], label="Roman chapter that starts with c: Psal. cxix. 105")
one("Rom 8, 28", ["Rom.8.28"], label="Latin / German comma: Rom 8, 28")
one("Rom. cap. 8. v. 28", ["Rom.8.28"], label="cap. / v.: Rom. cap. 8. v. 28")
one("Rom. ch. viii. ver. 28", ["Rom.8.28"], label="ch. / ver.: Rom. ch. viii. ver. 28")
one("1 Cor. 13. 12", ["1Cor.13.12"], label="numbered book: 1 Cor. 13. 12")
one("I Cor. xiii. 12", ["1Cor.13.12"], label="Roman ordinal: I Cor. xiii. 12")
one("First Corinthians 13:12", ["1Cor.13.12"], label="spelled ordinal: First Corinthians 13:12")
one("2 Pet. i. 19-21", ["2Pet.1.19", "2Pet.1.20", "2Pet.1.21"], label="a range gives each verse")
one("Isaiah lxi. 1, 2, 3", ["Isa.61.1", "Isa.61.2", "Isa.61.3"], label="a verse list gives each verse")
one("Psalm li. 10—12", ["Ps.51.10", "Ps.51.11", "Ps.51.12"], label="an em-dash range")
one("Esay 53. 5", ["Isa.53.5"], label="1611 spelling: Esay")
one("Apoc. xxi. 4", ["Rev.21.4"], label="Apoc. = Revelation")
one("Cant. ii. 16", ["Song.2.16"], label="Cant. = Song of Songs")

# ---------------------------------------------------------------- continuations
one("1 Cor. 2. 9; 13. 12.", ["1Cor.2.9", "1Cor.13.12"], label="'; 13. 12' carries the book")
one("Acts 2. 38, ver. 41", ["Acts.2.38", "Acts.2.41"], label="', ver. 41' carries the chapter")
one("Sap. 1. 1, 2 Pet. i. 19", ["2Pet.1.19"], label="a verse list stops at the next book (2 Pet. is not verse 2)")

# ---------------------------------------------------------------- the hard cases, each with its rule
one("Jud. 5. 3", ["Judg.5.3"], label="Jud. 5. 3 can only be Judges (Jude has one chapter)")
one("Jud. 3", ["Jude.1.3"], label="Jud. 3: a one-chapter book's verse")
one("Phil. 4. 13", ["Phil.4.13"], label="Phil. 4. 13 can only be Philippians")
one("Philem. 10", ["Phlm.1.10"], label="Philem. 10: a one-chapter book")
one("3 Kings 8. 27", ["1Kgs.8.27"], label="3 Kings is KJV 1 Kings in every tradition")
one("1 Kings 8. 27", ["1Kgs.8.27"], label="1 Kings under the Protestant profile is 1 Kings")
one("1 Kings 17. 45", ["1Sam.17.45"], "douay", label="1 Kings under the Douay profile is 1 Samuel")
one("Ps. 22. 1", ["Ps.22.1"], label="Ps. 22 under the Protestant profile is Ps 22")
one("Ps. 22. 1", ["Ps.23.1"], "douay", label="Ps. 22 under the Douay profile is KJV Ps 23 (Vulgate numbering)")
one("Cor. 15. 55", ["1Cor.15.55"], label="Cor. with its number lost: only 1 Cor has a chapter 15")
d = S.find("Cor. 13. 12")
check("Cor. 13. 12 with its number lost is AMBIGUOUS (1 and 2 Cor both have 13:12): kept for a human",
      d and d[0]["confidence"] == "ambiguous" and set(d[0]["candidates"]) == {"1Cor", "2Cor"} and "osis" not in d[0], d)
d = S.find("Ecclus. 3. 18")
check("Ecclus. is Sirach, recognised, not linked to a KJV verse",
      d and d[0].get("book") == "Sir" and d[0]["resolved"] is False and "osis" not in d[0])
one("Eccles. 12. 13", ["Eccl.12.13"], label="Eccles. is Ecclesiastes")
d = S.find("Miriam, Numb. xii. 24,")
check("a citation of no real verse is KEPT as not-a-verse, never linked, never dropped",
      d and d[0]["confidence"] == "not-a-verse" and "osis" not in d[0])

# ---------------------------------------------------------------- OCR, labelled as such
for text, want in (("Jleb. x. 29", "Heb.10.29"), ("Mai. iii. 18", "Mal.3.18"), ("Lnke xvi. 26", "Luke.16.26"),
                   ("Eev. 3: 20", "Rev.3.20"), ("Ezraix. 10", "Ezra.9.10")):
    d = S.find(text)
    check(f"OCR: {text!r} -> {want}, confidence 'ocr'", d and d[0].get("osis") == want and d[0]["confidence"] == "ocr", d)
check("OCR repair can be switched off", osis("Jleb. x. 29", ocr=False) == [])

# ---------------------------------------------------------------- never a book
for text in ("He came to Rome. 3. 4 people", "In Luke 2 the child", "Mark 12 men went", "Ruth 2 years",
             "He is 3. 4 feet", "Amos 3 times", "his job 2 days", "page 12. 3 of the Lamb. 5. 6", "I am 3. 4 years"):
    check(f"not a citation: {text!r}", osis(text) == [], osis(text))
one("Job 14. 5", ["Job.14.5"], label="but Job with a chapter AND a verse is a citation")

# ---------------------------------------------------------------- the link's shape
d = S.find("see Rom. viii. 28 there")[0]
check("a link carries osis, raw, its span, convention, confidence, profile",
      d["osis"] == "Rom.8.28" and d["raw"] == "Rom. viii. 28" and d["start"] == 4 and d["end"] == 17
      and d["convention"] == "roman-chapter" and d["confidence"] == "exact" and d["profile"] == "protestant")
check("roman(): cxix = 119, xiv = 14, not a numeral = None", S.roman("cxix") == 119 and S.roman("xiv") == 14 and S.roman("abc") is None)


# ---------------------------------------------------------------- the harvest over a built book
import copy, json, tempfile
book = {"slug": "flavel-sample", "title": "t", "source": {"format": "gutenberg-txt"},
        "scheme": {"honesty": "x"},
        "units": [{"id": "flavel-sample:1", "text": "as Rom. viii. 28 saith, and Heb. 11. 6.", "links": ["Rom.8.28"]},
                  {"id": "flavel-sample:2", "text": "no scripture here", "links": []}]}
st = S.harvest_book(book)
u = book["units"][0]
check("harvest: each verse cited becomes a link dict with osis, beside the unit's existing links",
      u["links"][0] == "Rom.8.28" and [l["osis"] for l in u["links"][1:]] == ["Rom.8.28", "Heb.11.6"])
check("harvest: the counts go into scheme.scripture", book["scheme"]["scripture"]["verse links"] == 2 and st["exact"] == 2)
before = json.dumps(book, sort_keys=True)
S.harvest_book(book)
check("harvest: running it twice changes nothing", json.dumps(book, sort_keys=True) == before)
book["scheme"]["scripture"]["harvest"] = 0
S.harvest_book(book)
check("harvest: a newer harvest replaces its own links, never duplicates them",
      [l["osis"] for l in book["units"][0]["links"][1:]] == ["Rom.8.28", "Heb.11.6"])
aq = {"slug": "aquinas-summa", "source": {"format": "gutenberg-txt"}, "scheme": {},
      "units": [{"id": "aquinas-summa:1", "text": "as it is written (Ps. 22. 1)", "links": []}]}
S.harvest_book(aq)
check("harvest: Aquinas's Summa is read with the Douay profile (its Ps. 22 is KJV Ps 23)",
      aq["units"][0]["links"][0]["osis"] == "Ps.23.1" and aq["scheme"]["scripture"]["profile"] == "douay")
for fmt in ("thml", "lexicon-tsv", "perseus-lexicon-tei"):
    check(f"harvest: a {fmt} book is left alone", S.harvest_book({"slug": "x", "source": {"format": fmt}, "units": []}) is None)
check("harvest: the Bible itself is left alone", S.harvest_book({"slug": "kjv", "source": {"format": "gutenberg-txt"}, "units": []}) is None)
d = tempfile.mkdtemp()
json.dump(book, open(os.path.join(d, "flavel-sample.json"), "w", encoding="utf-8"))
json.dump({"slug": "ccel-x", "source": {"format": "thml"}, "units": [{"id": "ccel-x:1", "text": "see Rom. 8. 28 and Heb. xi. 6", "links": ["Rom.8.28", "Heb.11.6"]}]},
          open(os.path.join(d, "ccel-x.json"), "w", encoding="utf-8"))
ex = open(os.path.join(d, "c.tsv"), "w", encoding="utf-8")
tot, key, rows = S.survey(d, ex)
ex.close()
check("survey: CCEL's own scripRef tags are the answer key (2 tagged, 2 found)", key["publisher's refs"] == 2 and key["both"] == 2)
check("survey: the export has one row per citation found", len(open(os.path.join(d, "c.tsv"), encoding="utf-8").readlines()) == 2)

print(f"\n{PASS} passed, {len(FAIL)} failed")
for f in FAIL:
    print("  FAIL", f)
sys.exit(1 if FAIL else 0)
