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
numbers it (Ps. 50 is the KJV's Ps 51; I-IV Reg. are 1-2 Sam, 1-2 Kgs), so OT
references in a `-lat` book go through the Clementine map
(data/versification/vulgate-kjv.json); the Greek editions cite as the
Septuagint numbers it, so OT references in a `-grc` book go through Brenton's
map (brenton-kjv.json). That is the edition family's convention, not a
reading of each note: so where the English numbering names a different KJV
verse it is kept as `alt_target`, and where the map has no such verse but the
English numbering does, that is the reading (`numbering: "english"`). NT
references are the KJV's numbering already. Every link carries `rule`, the id
of the rule that produced it:

  note/<family>     read from an editor's footnote (apparatus.notes)
  refs/<family>     read from a bracketed reference printed in the text
                    (apparatus.refs: Archambault's Justin, Schwartz's Eusebius)

and <family> is the map used: `vulgate`, `brenton` or `nt`. What is not
scripture (Philo, Homer, the father's own other works) is not read at all:
only a book in the table opens a reference.
"""
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


def parse(label, family):
    """[(book, kind, chapter, verse or None, end or None, alt_chapter or None)]."""
    s = label.replace("—", "-").replace("–", "-").replace("‒", "-")
    refs = []
    pos = 0
    lined = bool(re.match(r"\s*\d", s))
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
        while True:
            t = TOKEN.match(s, p)
            if not t:
                break
            if t.group("num"):
                b = BOOK_RE.match(s, t.start("num"))
                if b and b.group("pre") and book_of(b.group("pre"), b.group("name"), family, lined)[0]:
                    break           # "; 2 Cor. 5, 21": the next book, numbered
                # was it preceded by bare space (no separator since the last number)?
                bare = bool(toks) and toks[-1][0] == "num" and s[toks[-1][2]:t.start("num")].strip() == ""
                line = bool(LINE_AFTER.match(s, t.end()))
                toks.append(("num", t.group("num"), t.end(), bare, line))
            elif t.group("more"):
                p = t.end()
                continue
            elif t.group("paren"):
                toks.append(("paren", re.sub(r"\D", "", t.group("paren")), t.end(), False, False))
            else:
                toks.append(("sep", t.group("sep"), t.end(), False, False))
            p = t.end()
            # a number followed by a letter (a word) ends the run: "14 12 Gal."
            # is handled by `bare`; "3 sq." and "1 suiv." by the letter check
        pos = max(pos, p)
        found = _refs(book, kind, toks)
        if len(fold(m.group("name"))) <= 2:
            # a one- or two-letter name is also a manuscript siglum ("Mt 7",
            # "Hl 19"): it opens a reference only with a verse
            found = [r for r in found if r[3] is not None]
        refs += found
    return refs


def _refs(book, kind, toks):
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
        if not (i + 1 < n and toks[i][0] == "sep" and toks[i][1] in (",", ".", ":") and num_at(i + 1)
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
        while i + 1 < n and toks[i][0] == "sep" and toks[i][1] in ("-", ".", ",") and cont_at(i + 1) \
                and toks[i + 1][1].isdigit():
            # ", 41, 5" or ". 20, 2": the number opens a new chapter of the same book
            if toks[i][1] in (",", ".") and i + 3 < n and toks[i + 2][0] == "sep" and toks[i + 2][1] == "," \
                    and num_at(i + 3):
                i += 1
                break
            w = int(toks[i + 1][1])
            if toks[i][1] == "-":
                b, k, c, vv, _, a = out[-1]
                if w > vv:
                    out[-1] = (b, k, c, vv, w, a)
            elif w > out[-1][3]:
                out.append((book, kind, ch, w, None, alt))
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


def resolve(ref, family, ctx):
    """The link fields for one reference, with the id of the rule that made it."""
    book, kind, ch, v, end, alt = ref
    out = {"ref": printed(ref)}
    if kind == "deutero":
        return {**out, "resolved": False, "why": "a book outside the KJV", "map": None}
    if v is None:
        return {**out, "resolved": False, "why": "cites a whole chapter, not a verse", "map": None}
    nt = book in NT
    mapname = "nt" if nt else ("vulgate" if family == "lat" else "brenton")

    def one(verse):
        direct = f"kjv:{book}.{ch}.{verse}"
        if nt:
            return ({"resolved": True, "target": direct} if direct in ctx["kjv_ids"]
                    else {"resolved": False, "why": "no such verse in the KJV (an OCR digit?)"})
        osis = f"{book}.{ch}.{verse}"
        if mapname == "vulgate":
            r = V.resolve_vulgate(osis, ctx["vmap"], ctx["kjv_ids"]) if f"{book}.{ch}" in \
                ctx["vmap"]["vulgate_chapters"] else {"resolved": False, "why": "no such chapter in the Clementine Vulgate"}
        else:
            r = V.resolve_brenton(osis, ctx["bmap"], ctx["kjv_ids"])
        if direct not in ctx["kjv_ids"]:
            return r
        if r.get("resolved"):
            return r if r["target"] == direct else {**r, "alt_target": direct}
        if r.get("why", "").startswith("no such"):
            return {"resolved": True, "target": direct, "numbering": "english",
                    "why_numbering": f"the {mapname} numbering has no such verse; the English numbering fits"}
        return r

    r = one(v)
    out.update({k: r[k] for k in ("resolved", "target", "spans", "alt_target", "numbering",
                                  "why_numbering", "why") if k in r})
    if r.get("resolved") and end and end > v:
        last = one(end)
        if last.get("resolved"):
            out["through"] = last["target"]
    out["map"] = mapname
    return out


# One letter apart, and OCR reads one for the other ("Job. 4, 35" in a GCS
# note on John is Joh. 4, 35). A reference is read as its twin only when its
# own book has no such verse and the twin has it; the link says so.
OCR_TWIN = {"Job": "John", "John": "Job"}


def links_for(label, family, source, ctx):
    """Every scripture link in one note or bracketed reference."""
    out = []
    for ref in parse(label, family):
        r = resolve(ref, family, ctx)
        rule = f"{source}/{r.pop('map') or 'none'}"
        twin = OCR_TWIN.get(ref[0])
        if not r["resolved"] and ref[3] and twin and r.get("why", "").startswith("no such"):
            t = resolve((twin,) + ref[1:], family, ctx)
            if t["resolved"]:
                rule = f"{source}/{t.pop('map')}+ocr-twin"
                r = {**t, "ref": r["ref"], "read_as": twin,
                     "why_read": f"{ref[0]} has no such verse; OCR confuses {ref[0]} and {twin}"}
        r["rule"] = rule
        out.append(r)
    return out
