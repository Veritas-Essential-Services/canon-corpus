#!/usr/bin/env python3
"""
fathers_scripture.py -- the scripture references in the editors' notes to the
Greek and Latin fathers, read and resolved to KJV unit ids. Used by
tag_fathers.py; the same idea as af_scripture.py (PR #8, Lake's notes), for
editions that cite in four languages:

  CSEL (Latin)        "10 cf. Gal. 2, 14 12 Gal. 2, 14. 15"  "II Reg. 11, 3-5. 27"
  GCS (German)        "Vgl. Luk. 7, 28; Matth. 11, 11."
  Archambault (French)"cf. Deut., IV, 34; Exod., VI, 1 suiv.; XIII, 21"
  English editors     "John i. 3."   "S. Joan. viii. 39."   "cf. Ge xi 4"

READING. A reference is a book abbreviation (table BOOKS, per language family)
followed by a chapter (Arabic, or Roman in either case) and verse(s). After
the verse, more verses follow only across punctuation ("14. 15", "3-5. 27",
"31-32"); a number after bare space is the next LINE NUMBER of the critical
apparatus ("Gal. 2, 14 12 Gal."), never a verse. "; 11, 11" and ", et XXXI,
13" are further chapters of the same book. A chapter in brackets after a
chapter ("Hier. 32 (39), 30": the Septuagint's and the Hebrew's numbers) is
kept as `alt_chapter`. A book with no verse ("Gen. 18") cites a chapter and
stays unresolved, saying so.

NUMBERING (rule 4). The Latin editions cite the Old Testament as the Vulgate
numbers it (Ps. 50 is the KJV's Ps 51; I-IV Reg. are 1-2 Sam, 1-2 Kgs), and
the Greek editions mostly cite the Psalms as the Septuagint numbers them; but
editors differ, so each edition's numbering per class of book (Psalms,
Jeremiah, the rest) is MEASURED by fathers_numbering.py and committed in
data/fathers/numbering.json, and resolve() reads a reference through that:
the Clementine map (vulgate-kjv.json), Brenton's (brenton-kjv.json), the
Hebrew's (bhs-kjv.json, where a psalm's title is verse 1, as BDB cites), or
the KJV's chapter and verse as printed. Where another numbering names a
different KJV verse it is kept as `alt_target`; where the edition's
numbering has no such verse but another has, that one is the reading and
`numbering` says so. Every OT link says its `numbering` (vulgate, lxx,
hebrew, english). NT references are the KJV's numbering already. Every link carries `rule`, the id
of the rule that produced it:

  note/<map>        read from an editor's footnote (apparatus.notes)
  refs/<map>        read from a bracketed reference printed in the text
                    (apparatus.refs: Archambault's Justin, Schwartz's Eusebius)

and <map> is the numbering read: `vulgate`, `brenton`, `kjv` (the English)
or `nt`, with `+content` where an edition that mixes numberings was read
reference by reference by the father's own words. What is not
scripture (Philo, Homer, the father's own other works) is not read at all:
only a book in the table opens a reference.
"""
import collections
import re
import unicodedata

import versification as V

NT = ["Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil",
      "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas", "1Pet",
      "2Pet", "1John", "2John", "3John", "Jude", "Rev"]
SINGLE_CHAPTER = {"Obad", "Phlm", "2John", "3John", "Jude"}

# Abbreviations, as folded by fold(): accents and dots gone, lower case, a
# numeric prefix in Arabic. Shared by both families unless a family table
# overrides it.
COMMON = {
    "gen": "Gen", "genes": "Gen", "ge": "Gen", "gn": "Gen",
    "ex": "Exod", "exod": "Exod", "exo": "Exod",
    "lev": "Lev", "leu": "Lev", "levit": "Lev", "lv": "Lev",
    "num": "Num", "nomb": "Num", "nm": "Num",
    "deut": "Deut", "dt": "Deut", "dtn": "Deut", "deuter": "Deut", "dent": "Deut",
    "ios": "Josh", "jos": "Josh", "iosue": "Josh", "josue": "Josh", "josh": "Josh",
    "rut": "Ruth", "ruth": "Ruth",
    "1sam": "1Sam", "2sam": "2Sam",
    "1reg": "1Sam", "2reg": "2Sam", "3reg": "1Kgs", "4reg": "2Kgs",
    "1regn": "1Sam", "2regn": "2Sam", "3regn": "1Kgs", "4regn": "2Kgs",
    "1rois": "1Sam", "2rois": "2Sam", "3rois": "1Kgs", "4rois": "2Kgs",
    "1kings": "1Kgs", "2kings": "2Kgs", "1kgs": "1Kgs", "2kgs": "2Kgs",
    "1par": "1Chr", "2par": "2Chr", "1paral": "1Chr", "2paral": "2Chr",
    "1chron": "1Chr", "2chron": "2Chr", "1chr": "1Chr", "2chr": "2Chr",
    "esr": "Ezra", "esra": "Ezra", "ezra": "Ezra", "1esdr": "Ezra", "2esdr": "Neh",
    "neh": "Neh", "esth": "Esth", "est": "Esth",
    "iob": "Job", "job": "Job", "hiob": "Job",
    "ps": "Ps", "psalm": "Ps", "pss": "Ps", "psal": "Ps",
    "prov": "Prov", "prou": "Prov", "spr": "Prov", "prv": "Prov",
    "eccl": "Eccl", "eccles": "Eccl", "ecclesiastes": "Eccl", "pred": "Eccl", "koh": "Eccl",
    "cant": "Song", "hl": "Song", "cantic": "Song",
    "is": "Isa", "es": "Isa", "esai": "Isa", "isai": "Isa", "jes": "Isa", "ies": "Isa",
    "isa": "Isa", "esa": "Isa",
    "ier": "Jer", "jer": "Jer", "hier": "Jer", "ierem": "Jer", "jerem": "Jer",
    "thren": "Lam", "lam": "Lam", "klgl": "Lam",
    "ez": "Ezek", "ezech": "Ezek", "hez": "Ezek", "ezek": "Ezek", "ezec": "Ezek",
    "dan": "Dan", "os": "Hos", "hos": "Hos", "osee": "Hos",
    "ioel": "Joel", "joel": "Joel", "am": "Amos", "amos": "Amos",
    "abd": "Obad", "obd": "Obad", "obad": "Obad",
    "ion": "Jonah", "jon": "Jonah", "iona": "Jonah", "jona": "Jonah",
    "mich": "Mic", "mi": "Mic", "mic": "Mic", "nah": "Nah", "hab": "Hab", "habac": "Hab",
    "soph": "Zeph", "zeph": "Zeph", "zef": "Zeph",
    "agg": "Hag", "hag": "Hag", "zach": "Zech", "sach": "Zech", "zech": "Zech",
    "mal": "Mal", "malach": "Mal",
    "mt": "Matt", "matth": "Matt", "matt": "Matt", "mat": "Matt",
    "mc": "Mark", "mr": "Mark", "marc": "Mark", "mk": "Mark", "mark": "Mark", "mrk": "Mark",
    "lc": "Luke", "luc": "Luke", "luk": "Luke", "lk": "Luke", "luke": "Luke",
    "io": "John", "ioh": "John", "joh": "John", "ioan": "John", "joan": "John", "jn": "John",
    "john": "John", "jean": "John", "iohann": "John",
    "act": "Acts", "acta": "Acts", "apg": "Acts", "actes": "Acts", "acts": "Acts",
    "rom": "Rom", "1cor": "1Cor", "2cor": "2Cor", "1kor": "1Cor", "2kor": "2Cor",
    "gal": "Gal", "eph": "Eph", "ephes": "Eph", "phil": "Phil", "philipp": "Phil", "phl": "Phil",
    "col": "Col", "kol": "Col", "coloss": "Col",
    "1thess": "1Thess", "2thess": "2Thess", "1thes": "1Thess", "2thes": "2Thess",
    "1th": "1Thess", "2th": "2Thess",
    "1tim": "1Tim", "2tim": "2Tim", "tit": "Titus", "philem": "Phlm", "phm": "Phlm",
    "hebr": "Heb", "heb": "Heb",
    "iac": "Jas", "jac": "Jas", "jak": "Jas", "jas": "Jas", "iak": "Jas",
    "1petr": "1Pet", "2petr": "2Pet", "1pet": "1Pet", "2pet": "2Pet", "1pt": "1Pet", "2pt": "2Pet",
    "1ioh": "1John", "2ioh": "2John", "3ioh": "3John", "1joh": "1John", "2joh": "2John",
    "3joh": "3John", "1io": "1John", "2io": "2John", "3io": "3John", "1jo": "1John",
    "2jo": "2John", "3jo": "3John", "1ioan": "1John", "1jean": "1John", "1john": "1John",
    "lue": "Luke", "mare": "Mark",            # OCR: c read as e
    "apoc": "Rev", "apok": "Rev", "apk": "Rev", "offb": "Rev", "rev": "Rev", "apc": "Rev",
}
# Where the two families read one abbreviation differently. Latin "Iud." is
# Iudicum (Judges), and Jude is "Iudae"; the German editors write "Richt." for
# Judges and "Jud." for Jude.
FAMILY = {
    "lat": {"iud": "Judg", "iudic": "Judg", "iudae": "Jude", "iuda": "Jude", "jud": "Judg"},
    "grc": {"jud": "Jude", "iud": "Jude", "judae": "Jude", "richt": "Judg", "ri": "Judg",
            "jug": "Judg", "judic": "Judg", "iudic": "Judg"},
}
# The Septuagint's Esdras: 1 Esdras is the apocryphal book, 2 Esdras is Ezra
# and Nehemiah in one (Brenton's Ezra 11-23 is Nehemiah, and his map says so).
# The Vulgate's 1 and 2 Esdras are Ezra and Nehemiah (COMMON).
# The Vulgate's appendix has 3 and 4 Esdras: the Apocrypha's 1 and 2 Esdras.
FAMILY_DEUTERO = {"grc": {"1esdr": "1Esd", "3esdr": "1Esd", "4esdr": "2Esd"},
                  "lat": {"3esdr": "1Esd", "4esdr": "2Esd"}}
FAMILY["grc"].update({"2esdr": "Ezra"})
# Books outside the KJV: read, so a reference to them is counted, never resolved.
DEUTERO = {"tob": "Tob", "iudith": "Jdt", "judith": "Jdt", "jdt": "Jdt", "sap": "Wis",
           "weish": "Wis", "wisd": "Wis", "sir": "Sir", "eccli": "Sir", "ecclus": "Sir",
           "bar": "Bar", "1macc": "1Macc", "2macc": "2Macc", "1mac": "1Macc", "2mac": "2Macc"}

# A book name right after one of these is part of another work's title.
NOT_AFTER = re.compile(r"(?:\b(?:bell|Ant|Antiq|Philo|Cyril|Iosephus|Josephus)\.?|\bde)\s*$")

ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100}


def roman(s):
    s = s.lower()
    if not s or any(ch not in ROMAN for ch in s):
        return None
    total, prev = 0, 0
    for ch in reversed(s):
        v = ROMAN[ch]
        total = total - v if v < prev else total + v
        prev = max(prev, v)
    return total


CYRILLIC = str.maketrans("АВЕНІКМОРСТХаеорсхі", "ABEHIKMOPCTXaeopcxi")


def fold(s):
    s = unicodedata.normalize("NFD", s.translate(CYRILLIC))
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower()
    return re.sub(r"[\s.]", "", s)


PREFIX = {"i": "1", "ii": "2", "iii": "3", "iv": "4", "1": "1", "2": "2", "3": "3", "4": "4"}

# A book: an optional numeral prefix, a word starting upper case (or all upper
# case, as Archambault prints), an optional dot and comma. "S." (Saint) may
# precede it and is skipped.
BOOK_RE = re.compile(r"(?<![\w])(?:(?P<pre>IV|III|II|I|[1-4])\.?\s?)?(?P<name>[A-ZÀ-ÝА-Я][a-zà-ÿA-ZÀ-Ýа-яА-Я]{0,11})"
                     r"(?![\w])\.?,?\s*(?=[0-9IVXLCivxlc])")
NUM = r"(?:\d{1,3}|[IVXLC]{1,7}|[ivxlc]{1,7})"
TOKEN = re.compile(r"\s*(?:(?P<num>\d{1,3}|[IVXLC]{1,7}\b|[ivxlc]{1,7}\b)|(?P<paren>\(\s*\d{1,3}\s*\))"
                   r"|(?P<sep>[,.;:\-]|et\b)|(?P<more>(?:suiv|sqq|sq|ff|f|ss|s)\b\.?))")
# After a verse, a number followed by a word is the apparatus's next LINE
# number ("Matth. 1, 15. 25 Luc."), unless the word says "and following".
LINE_AFTER = re.compile(r"\s+(?!(?:suiv|sqq|sq|ff|f|ss|s|et)\b)[^\W\d_]")


def book_of(pre, name, family, lined=False):
    """(book, kind) or (None, None). In an apparatus that numbers its lines
    (CSEL, GCS: the label opens with a number), books are numbered in Roman
    and an Arabic number before a book is the line: "3 Joh. 13, 8" is John,
    unless the name alone is no book ("1 Cor.")."""
    if lined and pre and pre.isdigit():
        b = book_of(None, name, family)
        if b[0]:
            return b
    key = fold(name)
    if pre:
        key = PREFIX.get(pre.lower(), "") + key
    if key in FAMILY_DEUTERO.get(family, {}):
        return FAMILY_DEUTERO[family][key], "deutero"
    table = FAMILY.get(family, {})
    if key in table:
        return table[key], "kjv"
    if key in COMMON:
        return COMMON[key], "kjv"
    if key in DEUTERO:
        return DEUTERO[key], "deutero"
    if pre and pre.isdigit():
        # "2 Ps. 44, 2": the 2 is the apparatus's line number, not "2 Ps."
        return book_of(None, name, family)
    return None, None


def as_num(tok):
    if tok.isdigit():
        return int(tok)
    return roman(tok)


# "Ps. 18, " / "Ps. xviii , ": a book word, then its chapter and a comma,
# before a number; or such a reference running on by "-", "et" or a new
# chapter ("Ps. 18, 6-", "Ps. 18, 6 et ", "Ps. 18, 6; 20, "). Never after a
# bare ", ": "Es. 1, 11, 24]" is a verse, then the next line's marker. So a
# number after "et" ("Ps. 17, 14 et 12]") is always a verse, never a marker.
VERSE_BEFORE = re.compile(r"(?<![^\W\d_])(?!et\b)(?:[^\W\d_]{2,}\.?|[^\W\d_]\.)\s*"
                          r"(?:\d{1,3}|(?<![^\W\d_])[IVXLCivxlc]{1,7})\s*,\s*"
                          r"(?:\d{1,3}\s*(?:[-—–]|(?:;|et)\s*\d{1,3}\s*,|et\b)\s*)*$")


def parse(label, family):
    """[(book, kind, chapter, verse or None, end or None, alt_chapter or None)]."""
    # "9] Ps. 18, 6. 16] Io. 1,10.": an apparatus marker "N]" (the line a
    # note belongs to) is never a verse, and a spaced em-dash is the GCS
    # separator between entries ("Röm. 4, 17. — 8 Esth.", "29, 5 — 15 — 18"),
    # unless the number after it ends the entry ("Matth. 7, 3 — 5;": a
    # range). Both become a stop no number can be read across. "[17]" is a verse.
    # A verse right after a book's chapter closes a lemma ("Ps. 18, 6] cf.",
    # "Ps. XVIII, 6] cf."), so it stays. A number after a verse or a page
    # ("Es. 1, 11, 24] Ioh.", "15-196, 11] cf.") is the next line's marker.
    # "9-11]" (lines 9 to 11) and "13-217, 4]" (line 13 to page 217, line 4)
    # are one marker each, unless they follow a book's chapter ("Ps. 18, 6-9]":
    # verses closing a lemma; "Es. 53, 2-3, 11]": verses, then a line).
    label = re.sub(r"(?<![\w\[])\d{1,3}\s?[-—–]\s?\d{1,4}(?:\s?,\s?\d{1,3})?\s?\]",
                   lambda m: m.group(0) if VERSE_BEFORE.search(label, 0, m.start()) else " | ", label)
    s = re.sub(r"(?<![\w\[])\d{1,3}\s?f{0,2}\]",
               lambda m: m.group(0) if VERSE_BEFORE.search(label, 0, m.start()) else " | ", label)
    s = re.sub(r"(?:^|\s)—(?!\s?\d{1,3}\s?(?:[.,;)\]]|$))", " | ", s)
    s = s.replace("—", "-").replace("–", "-").replace("‒", "-")
    refs = []
    pos = 0
    lined = bool(re.match(r"\s*\d", s))
    # a lined note that mostly writes "Book. chapter. line Book" (Sulpicius'
    # Chronica: "5 Gen. 1. 9 Gen. 2.") cites chapters; its "1. 9" is not a
    # verse. One that mostly writes "chapter, verse" keeps an OCR full stop's
    # verse ("2 Matth. 10. 10 Luc. 10, 4").
    dots = len(re.findall(r"[A-Z][A-Za-z]+\.\s?\d{1,3}\.\s?\d{1,3}\s?(?:I{1,3}\s)?[A-Z]", s))
    chapters_lined = lined and dots > len(re.findall(r"\d\s?,\s?\d", s))
    while True:
        m = BOOK_RE.search(s, pos)
        if not m:
            break
        book, kind = book_of(m.group("pre"), m.group("name"), family, lined)
        pos = m.end()
        if book and NOT_AFTER.search(s, 0, m.start()):
            book = None             # "bell. Iud. IIII 1": Josephus, not Judges
        if not book:
            pos = m.start("name") + 1
            continue
        # tokens after the book: numbers, separators, a bracketed number
        toks = []
        p = pos
        after_more = False
        while True:
            t = TOKEN.match(s, p)
            if not t:
                break
            if t.group("num"):
                b = BOOK_RE.match(s, t.start("num"))
                if b and b.group("pre"):
                    nb = book_of(b.group("pre"), b.group("name"), family, lined)[0]
                    if nb and nb != book_of(None, b.group("name"), family)[0]:
                        break       # "; 2 Cor. 5, 21": the next book, numbered
                    # "Is. 53, 4 Matth.": the number is not part of the next
                    # book's name, so it is this reference's verse (or a line)
                # was it preceded by bare space (no separator since the last number)?
                bare = bool(toks) and toks[-1][0] == "num" and s[toks[-1][2]:t.start("num")].strip() == ""
                # "Psal. 7, 16ff. 23 Exod.": after "and following" a number is
                # the apparatus's next line, not a chapter
                bare = bare or after_more
                line = bool(LINE_AFTER.match(s, t.end()))
                toks.append(("num", t.group("num"), t.end(), bare, line))
            elif t.group("more"):
                p = t.end()
                after_more = True
                continue
            elif t.group("paren"):
                toks.append(("paren", re.sub(r"\D", "", t.group("paren")), t.end(), False, False))
            else:
                toks.append(("sep", t.group("sep"), t.end(), False, False))
            after_more = False
            p = t.end()
            # a number followed by a letter (a word) ends the run: "14 12 Gal."
            # is handled by `bare`; "3 sq." and "1 suiv." by the letter check
        pos = max(pos, p)
        found = _refs(book, kind, toks, chapters_lined)
        if len(fold(m.group("name"))) <= 2:
            # a one- or two-letter name is also a manuscript siglum ("Mt 7",
            # "Hl 19"): it opens a reference only with a verse
            found = [r for r in found if r[3] is not None]
        refs += found
    return refs


def _refs(book, kind, toks, lined=False):
    out = []
    i = 0
    n = len(toks)

    def num_at(j):
        return j < n and toks[j][0] == "num" and not toks[j][3]

    def cont_at(j):
        return num_at(j) and not toks[j][4]

    while i < n:
        if toks[i][0] != "num" or (toks[i][3] and out):
            if toks[i][0] == "num":
                break               # a bare-space number: the next line number
            if toks[i][0] == "sep" and toks[i][1] in (";", "et", ","):
                i += 1
                continue
            i += 1
            continue
        ch = as_num(toks[i][1])
        if ch is None:
            break
        i += 1
        alt = None
        if i < n and toks[i][0] == "paren":
            alt = int(toks[i][1])
            i += 1
        if book in SINGLE_CHAPTER:
            out.append((book, kind, 1, ch, None, None))
            # "Jude 9. 14": more verses
            while i + 1 < n and toks[i][0] == "sep" and toks[i][1] in (".", ",", "-") and cont_at(i + 1) \
                    and toks[i + 1][1].isdigit():
                v = int(toks[i + 1][1])
                if toks[i][1] == "-":
                    out[-1] = out[-1][:4] + (v, None)
                else:
                    out.append((book, kind, 1, v, None, None))
                i += 2
            continue
        # chapter, then a separator, then a verse
        # "5 Gen. 1. 9 Gen. 2." (Sulpicius cites chapters): in a note that
        # cites chapters (`lined` here), chapter and a full stop is a whole
        # chapter, and the number after it the next line's
        line_next = lined and i + 1 < n and toks[i][1] == "."
        if line_next or not (i + 1 < n and toks[i][0] == "sep" and toks[i][1] in (",", ".", ":") and num_at(i + 1)
                             and toks[i + 1][1].isdigit()):
            # "John i 3" (Philocalia): a Roman chapter, a bare space, a verse
            if i < n and toks[i][0] == "num" and toks[i][1].isdigit() and not toks[i - 1][1].isdigit():
                v = int(toks[i][1])
                out.append((book, kind, ch, v, None, alt))
                i += 1
                continue
            out.append((book, kind, ch, None, None, alt))
            if i < n and toks[i][0] == "sep" and toks[i][1] in (";", "et"):
                continue
            break
        v = int(toks[i + 1][1])
        out.append((book, kind, ch, v, None, alt))
        i += 2
        # more verses of this chapter: "-32", ". 15", ", 41", "3-5. 27"
        while i + 1 < n and toks[i][0] == "sep" and toks[i][1] in ("-", ".", ",", "et") \
                and (cont_at(i + 1) or (toks[i][1] == "et" and num_at(i + 1))) \
                and toks[i + 1][1].isdigit():
            # ("2 et 3 Exod.": after "et" the number is a verse even with a book next)
            # ", 41, 5", ". 20, 2" or "et 3, 4": the number opens a new chapter of the same book
            if toks[i][1] in (",", ".", "et") and i + 3 < n and toks[i + 2][0] == "sep" and toks[i + 2][1] == "," \
                    and num_at(i + 3):
                i += 1
                break
            # "21, 30 - 23, 2": a range into another chapter. The link keeps
            # its first verse; the end chapter is not a verse of this one.
            if toks[i][1] == "-" and i + 3 < n and toks[i + 2][0] == "sep" and toks[i + 2][1] == "," \
                    and num_at(i + 3):
                i += 4
                break
            w = int(toks[i + 1][1])
            if toks[i][1] == "-":
                b, k, c, vv, _, a = out[-1]
                if w > vv:
                    out[-1] = (b, k, c, vv, w, a)
            elif w > out[-1][3] or (toks[i][1] == "et" and w != out[-1][3]):
                out.append((book, kind, ch, w, None, alt))   # "17, 14 et 8": et may go back
            else:
                break
            i += 2
        if i < n and toks[i][0] == "num" and not toks[i][3]:
            continue                # the new chapter found above
        if i < n and toks[i][0] == "sep" and toks[i][1] in (";", "et", ","):
            i += 1
            continue
        break
    return out


def printed(ref):
    book, _, ch, v, end, alt = ref
    return f"{book} {ch}" + (f"({alt})" if alt else "") + (f":{v}" if v else "") + (f"-{end}" if end else "")


FAMILY_NUMBERING = {"lat": "vulgate", "grc": "lxx"}
# The rule id names the map a numbering is read through.
MAP_OF = {"vulgate": "vulgate", "lxx": "brenton", "hebrew": "bhs", "english": "kjv"}
FALLBACK = {"lat": ("vulgate", "english", "hebrew"), "grc": ("lxx", "english", "hebrew")}


# The Septuagint these editors cite is Swete's (1887-94) or older, and
# Brenton's map follows Rahlfs where they part: Swete's Isa 9 is the English
# chapter (Rahlfs moved its 9:1 to 8:23), his Jer 32:1-24 is Rahlfs' 32:15-38
# (the cup, the KJV's 25:15-38), his Mal 4:1-6 Rahlfs' 3:19-24.
# (book, chapter) -> verse -> (chapter, verse) in Brenton's numbering.
SWETE = {
    ("Isa", 9): lambda v: (8, 23) if v == 1 else (9, v - 1),
    ("Jer", 32): lambda v: (32, v + 14) if v <= 24 else None,
    ("Mal", 4): lambda v: (3, v + 18) if v <= 6 else None,
}


def read_in(numbering, book, ch, v, ctx):
    """One OT verse read in one numbering: the versification module's fields
    (resolved, target, why), plus `exists` when the numbering has the verse
    but the KJV numbers none for it (a psalm title, a Greek addition)."""
    osis = f"{book}.{ch}.{v}"
    try:
        if numbering == "english":
            d = f"kjv:{osis}"
            return ({"resolved": True, "target": d} if d in ctx["kjv_ids"]
                    else {"resolved": False, "why": "no such verse in the KJV"})
        if numbering == "vulgate":
            if f"{book}.{ch}" not in ctx["vmap"]["vulgate_chapters"]:
                return {"resolved": False, "why": "no such chapter in the Clementine Vulgate"}
            r = V.resolve_vulgate(osis, ctx["vmap"], ctx["kjv_ids"])
        elif numbering == "lxx":
            sw = SWETE.get((book, ch))
            cv = sw(v) if sw else (ch, v)
            if cv is None:
                return {"resolved": False, "why": "no such verse in Swete's Septuagint"}
            r = V.resolve_brenton(f"{book}.{cv[0]}.{cv[1]}", ctx["bmap"], ctx["kjv_ids"])
        else:
            if book not in V.BOOKS or f"{book}.{ch}" not in ctx["hmap"]["hebrew_chapters"]:
                return {"resolved": False, "why": "no such chapter in the Hebrew Bible (WLC)"}
            r = V.resolve(osis, ctx["hmap"], ctx["kjv_ids"])
    except (ValueError, KeyError):
        return {"resolved": False, "why": "no such verse in that numbering"}
    if not r.get("resolved") and not r.get("why", "").startswith("no such"):
        r = {**r, "exists": True}
    return r


def _cv(target):
    """"kjv:Ps.74.5" or "Ps.74.5" -> ("Ps", 74, 5)."""
    b, c, v = target.split(":")[-1].split(".")
    return b, int(c), int(v)


def _through(first, last):
    """A range's end, kept only in the same book and not before its start."""
    (b1, c1, v1), (b2, c2, v2) = _cv(first), _cv(last)
    return last if b1 == b2 and (c2, v2) > (c1, v1) else None


# The Greek side of a bracketed chapter pair ("III Reg. 20 (21), 13",
# "Psalm. 73 (74), 5", "Hier. 31 (38)"): the Septuagint's (and in a Latin
# book the Vulgate's) number beside the Hebrew-English one.
BRACKET_SIDES = {"lat": ("vulgate", "lxx"), "grc": ("lxx",)}


def bracket_orders(ref, family, ctx):
    """Which order a bracketed reference can be read in: "greek-first" (the
    first number is the Greek side's chapter and the bracket the KJV's) or
    "kjv-first", each with (numbering, fields). Both orders fit only where the
    two numberings swap whole chapters (1 Kgs 20/21)."""
    book, kind, ch, v, end, alt = ref
    got = {}
    for order, (gch, kch) in (("greek-first", (ch, alt)), ("kjv-first", (alt, ch))):
        for x in BRACKET_SIDES[family]:
            r = read_in(x, book, gch, v, ctx)
            if r.get("resolved") and _cv(r["target"])[:2] == (book, kch):
                f = {"resolved": True, "target": r["target"]}
                if end and end > v:
                    e = read_in(x, book, gch, end, ctx)
                    if e.get("resolved") and _through(r["target"], e["target"]):
                        f["through"] = e["target"]
                got[order] = (x, f)
                break
    return got


def bracket_pref(labels, family, ctx):
    """An editor prints his brackets one way round: the order this book's
    brackets that fit only one way take, by majority (None if none, or tied)."""
    n = collections.Counter()
    for lab in labels:
        for ref in parse(lab, family):
            if ref[5] and ref[3] is not None and ref[1] == "kjv" and ref[0] not in NT:
                o = bracket_orders(ref, family, ctx)
                if len(o) == 1:
                    n[next(iter(o))] += 1
    if not n or n["greek-first"] == n["kjv-first"]:
        return None
    return n.most_common(1)[0][0]


def bracketed(ref, family, ctx, pref=None):
    """Link fields for a bracketed reference read by its two numbers, or None
    if neither order lands (then it is read like any other reference)."""
    o = bracket_orders(ref, family, ctx)
    if not o:
        return None
    if len(o) == 1:
        order = next(iter(o))
        how = "the only order that lands"
    else:
        order = pref or "greek-first"
        how = "this edition's order" if pref else "both orders land; no order measured for this edition"
    x, f = o[order]
    out = {**f, "numbering": x, "map": MAP_OF[x] + "+bracket", "bracket": order, "why_bracket": how}
    if len(o) == 2 and not pref:
        other = o["kjv-first" if order == "greek-first" else "greek-first"][1]
        if other["target"] != f["target"]:
            out["alt_target"] = other["target"]
            out["numbering_undecided"] = ["bracket order"]
            out["undecided_targets"] = [other["target"]]
    return out


def resolve(ref, family, ctx, scheme=None, vote=None, bracket_pref=None):
    """The link fields for one reference, with the id of the rule that made it.

    `scheme(book)` -> (numbering, per_reference[, undecided]) is the edition's
    measured numbering for that class of book (fathers_numbering.py); without
    one, the family's. `undecided` names the numberings its evidence leaves
    open: where one reads another verse, the link carries it as `alt_target`
    and lists it in `numbering_undecided`. `vote` is the set of numberings the content vote links_for()
    took for this reference's group favours, used only in a class whose
    edition mixes numberings."""
    book, kind, ch, v, end, alt = ref
    out = {"ref": printed(ref)}
    if kind == "deutero":
        return {**out, "resolved": False, "why": "a book outside the KJV", "map": None}
    if v is None:
        return {**out, "resolved": False, "why": "cites a whole chapter, not a verse", "map": None}
    if book in NT:
        direct = f"kjv:{book}.{ch}.{v}"
        if direct in ctx["kjv_ids"]:
            out.update({"resolved": True, "target": direct})
            last = f"kjv:{book}.{ch}.{end}" if end and end > v else None
            if last in ctx["kjv_ids"]:
                out["through"] = last
        else:
            out.update({"resolved": False, "why": "no such verse in the KJV (an OCR digit?)"})
        out["map"] = "nt"
        return out
    if alt:
        b = bracketed(ref, family, ctx, bracket_pref)
        if b:
            return {**out, **b}
    numbering, per_ref, *rest = scheme(book) if scheme else (FAMILY_NUMBERING[family], False)
    undecided = tuple(rest[0]) if rest else ()
    how = "edition"
    if per_ref and vote:
        if numbering not in vote:
            numbering = next(x for x in FALLBACK[family] if x in vote)
        how = "content"
        undecided = ()
    order = [numbering] + [x for x in FALLBACK[family] if x != numbering]

    def one(verse):
        """(fields, numbering read)."""
        rs = {x: read_in(x, book, ch, verse, ctx) for x in order}
        first = rs[numbering]
        if first.get("resolved") or first.get("exists"):
            used, r = numbering, first
        else:
            used = next((x for x in order[1:] if rs[x].get("resolved")), None)
            if used is None:
                return {"resolved": False, "why": f"no such verse in any numbering ({', '.join(order)})"}, numbering
            r = {**rs[used], "why_numbering": f"the {numbering} numbering has no such verse; the {used} numbering fits"}
        r = {k: r[k] for k in ("resolved", "target", "spans", "why", "why_numbering") if k in r}
        if r.get("resolved"):
            # A rival the edition's evidence leaves open comes first; the link
            # says the numbering is not settled wherever that rival reads
            # another verse.
            open_ = [x for x in undecided if x != used and rs[x].get("resolved")
                     and rs[x]["target"] != r["target"]] if used == numbering else []
            other = next((rs[x]["target"] for x in open_ + [x for x in order if x != used]
                          if rs[x].get("resolved") and rs[x]["target"] != r["target"]), None)
            if other:
                r["alt_target"] = other
            if open_:
                # alt_target holds one; every open rival's reading is listed
                r["numbering_undecided"] = open_
                r["undecided_targets"] = list(dict.fromkeys(rs[x]["target"] for x in open_))
        return r, used

    r, used = one(v)
    out.update(r)
    out["numbering"] = used
    if r.get("resolved") and end and end > v:
        # the end in the numbering the start was read in, never another
        last = read_in(used, book, ch, end, ctx)
        if last.get("resolved") and _through(r["target"], last["target"]):
            out["through"] = last["target"]
    out["map"] = MAP_OF[used] + ("+content" if how == "content" else "")
    return out


# One letter apart, and OCR reads one for the other ("Job. 4, 35" in a GCS
# note on John is Joh. 4, 35). A reference is read as its twin only when its
# own book has no such verse and the twin has it; the link says so.
OCR_TWIN = {"Job": "John", "John": "Job"}


def group_votes(refs, family, ctx, scheme, unit_words):
    """{index: vote} for references in a class whose edition mixes
    numberings: each run of references to one chapter of one book is one
    quotation, read by one content vote (fathers_numbering.group_vote)."""
    if not (scheme and unit_words is not None and "bren" in ctx):
        return {}
    import fathers_numbering as FN
    out, i = {}, 0
    while i < len(refs):
        book, kind, ch, v = refs[i][:4]
        j = i + 1
        while j < len(refs) and refs[j][0] == book and refs[j][2] == ch:
            j += 1
        if kind == "kjv" and book not in NT and scheme(book)[1]:
            items = [(book, ch, r[3]) for r in refs[i:j] if r[3] is not None]
            vote = FN.group_vote(ctx["bren"], unit_words, items, ctx, family) if items else None
            if vote:
                out.update({k: vote for k in range(i, j)})
        i = j
    return out


def links_for(label, family, source, ctx, scheme=None, unit_words=None, bracket_pref=None):
    """Every scripture link in one note or bracketed reference."""
    out = []
    refs = parse(label, family)
    votes = group_votes(refs, family, ctx, scheme, unit_words)
    for i, ref in enumerate(refs):
        r = resolve(ref, family, ctx, scheme, votes.get(i), bracket_pref)
        rule = f"{source}/{r.pop('map') or 'none'}"
        twin = OCR_TWIN.get(ref[0])
        if not r["resolved"] and ref[3] and twin and r.get("why", "").startswith("no such"):
            t = resolve((twin,) + ref[1:], family, ctx, scheme, votes.get(i), bracket_pref)
            if t["resolved"]:
                rule = f"{source}/{t.pop('map')}+ocr-twin"
                r = {**t, "ref": r["ref"], "read_as": twin,
                     "why_read": f"{ref[0]} has no such verse; OCR confuses {ref[0]} and {twin}"}
        r["rule"] = rule
        out.append(r)
    return out
