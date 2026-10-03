#!/usr/bin/env python3
"""
topical_read.py -- read scripture references the way a printed page writes
them, and read CCEL's topical and dictionary books.

Two jobs, one grammar:

  * refs(text) reads "Ex. 6:16-20; Josh. 21:10, 13", "1 Kings 19 : 16, 17",
    "Ge 48:5,14", "Jude 9" -- the forms Nave, Torrey, Easton and Smith print,
    and the forms CCEL displays. It is used on CCEL's displayed text (to check
    CCEL's own tagging) and on the scans' OCR (to check CCEL against print).
  * ccel_entries(path) walks a ThML dictionary (<term>/<def>) and gives each
    entry its paragraphs, their outline depth, and the references CCEL tagged
    in them (osisRef), each with the text CCEL displayed for it.

Nothing here decides what is committed; build_topical.py does.
"""
import html
import re

# OSIS book (or, for numbered books, the book without its ordinal) -> the
# forms print uses for it. A form is matched whole, after an optional ordinal.
BOOK_FORMS = [
    ("Gen", "Gen Ge Genesis Gn"),
    ("Exod", "Ex Exod Exo Exodus"),
    ("Lev", "Lev Le Leviticus Lv"),
    ("Num", "Num Nu Numb Numbers Nm"),
    ("Deut", "Deut De Deu Deuteronomy Dt"),
    ("Josh", "Josh Jos Joshua"),
    ("Judg", "Judg Jud Judges Jdg Jg Jdj"),
    ("Ruth", "Ruth Ru"),
    ("Sam", "Sam Sa Samuel"),
    ("Kgs", "Kings Ki Kgs Kin"),
    ("Chr", "Chr Ch Chron Chronicles"),
    ("Ezra", "Ezra Ezr"),
    ("Neh", "Neh Ne Nehemiah"),
    ("Esth", "Esth Es Est Esther"),
    ("Job", "Job"),
    ("Ps", "Ps Psa Psalm Psalms Pss"),
    ("Prov", "Prov Pr Pro Proverbs"),
    ("Eccl", "Eccl Ec Ecc Eccles Ecclesiastes Eccle"),
    ("Song", "Song So Cant Canticles Sol"),
    ("Isa", "Isa Is Isaiah"),
    ("Jer", "Jer Je Jeremiah"),
    ("Lam", "Lam La Lamentations"),
    ("Ezek", "Ezek Eze Ezekiel Ezk"),
    ("Dan", "Dan Da Daniel"),
    ("Hos", "Hos Ho Hosea"),
    ("Joel", "Joel Joe"),
    ("Amos", "Amos Am"),
    ("Obad", "Obad Ob Obadiah"),
    ("Jonah", "Jonah Jon"),
    ("Mic", "Mic Mi Micah"),
    ("Nah", "Nah Na Nahum"),
    ("Hab", "Hab Habakkuk"),
    ("Zeph", "Zeph Zep Zephaniah"),
    ("Hag", "Hag Hagg Haggai"),
    ("Zech", "Zech Zec Zechariah"),
    ("Mal", "Mal Malachi"),
    ("Matt", "Matt Mt Mat Matthew"),
    ("Mark", "Mark Mr Mk Mar"),
    ("Luke", "Luke Lu Lk Luk"),
    ("John", "John Joh Jno Jn"),
    ("Acts", "Acts Ac Act"),
    ("Rom", "Rom Ro Romans"),
    ("Cor", "Cor Co Corinthians"),
    ("Gal", "Gal Ga Galatians"),
    ("Eph", "Eph Ephesians"),
    ("Phil", "Phil Php Philippians Philip"),
    ("Col", "Col Colossians"),
    ("Thess", "Thess Th Thes Thessalonians"),
    ("Tim", "Tim Ti Timothy"),
    ("Titus", "Titus Tit"),
    ("Phlm", "Phlm Philem Phm Philemon"),
    ("Heb", "Heb Hebrews"),
    ("Jas", "Jas Jam James"),
    ("Pet", "Pet Pe Peter"),
    ("Jude", "Jude"),
    ("Rev", "Rev Re Revelation Apoc"),
    # the Apocrypha, which the dictionaries cite; never a kjv: id
    ("Tob", "Tob Tobit"),
    ("Jdt", "Jdt Judith Jth"),
    ("Wis", "Wis Wisd Wisdom"),
    ("Sir", "Sir Ecclus Ecclesiasticus Ecclu"),
    ("Bar", "Bar Baruch"),
    ("Macc", "Macc Mac Ma Maccabees"),
    ("Esd", "Esd Esdr Esdras"),
]
# books that need an ordinal, and the OSIS name each ordinal makes
NUMBERED = {"Sam": "Sam", "Kgs": "Kgs", "Chr": "Chr", "Cor": "Cor", "Thess": "Thess",
            "Tim": "Tim", "Pet": "Pet", "Macc": "Macc", "Esd": "Esd"}
FORM = {}
for _b, _forms in BOOK_FORMS:
    for _f in _forms.split():
        FORM.setdefault(_f, _b)
FORM["Ti"] = "Titus"        # unnumbered Ti is Titus; 1 Ti / 2 Ti is Timothy (below)
SINGLE_CHAPTER = {"Obad", "Phlm", "2John", "3John", "Jude"}

_ORD = {"1": "1", "2": "2", "3": "3", "I": "1", "II": "2", "III": "3", "i": "1", "ii": "2", "iii": "3"}
_BOOK_RE = r"(?:(?P<ord>[123]|I{1,3}|i{1,3})\s?\.?\s*)?(?P<name>[A-Z][a-z]{0,13})\b[.,]?"
_NUM = r"\d{1,3}"
# chapter : verse, the colon free to float ("19 : 16", "11: 4"), or a dot (Easton's "Gen. 4.1" never; but OCR)
_CV = re.compile(r"\s*(?P<c>%s)\s*:\s*(?P<v>%s)" % (_NUM, _NUM))
_TOKEN = re.compile(_BOOK_RE)


def book_of(ordinal, name):
    """("1", "Kings") -> "1Kgs"; (None, "Ge") -> "Gen"; None if not a book."""
    b = FORM.get(name)
    if name == "Jo" and ordinal:      # 1 Jo. is an epistle; a bare Jo. is Joshua or John, neither
        b = "John"
    if b is None:
        return None
    o = _ORD.get(ordinal) if ordinal else None
    if b in NUMBERED:
        return (o + b) if o in ("1", "2") else None
    if b == "Titus" and name == "Ti" and o:
        return o + "Tim" if o in ("1", "2") else None
    if b == "John" and o:
        return o + "John" if o in ("1", "2", "3") else None
    if o:
        return None
    return b


def refs(text):
    """Every reference in text, in order: [{"book", "c", "v", "c2", "v2", "at"}].
    A book carries over to a following "c:v" after ";" or "," and to bare
    verse numbers after "," or "and"; a range ends at a verse ("16-20") or a
    chapter:verse ("16:1-17:3")."""
    out = []
    text = text.replace("\u2014", "-").replace("\u2013", "-")
    n = len(text)
    i = 0
    book = chapter = None
    end = -1
    while i < n:
        if book and i == end:
            k = _CONT.match(text, i)
            if k:
                j = k.end()
                cv = _CV.match(text, j)
                if cv:
                    i = end = _take(text, cv, book, out)
                    chapter = out[-1]["c2"]
                    continue
                if k.group(1) == ";" and chapter is not None and book not in SINGLE_CHAPTER:
                    ch = _CHAPTER.match(text, j)
                    if ch:
                        c = int(ch.group(1))
                        c2 = int(ch.group(2)) if ch.group(2) else c
                        out.append({"book": book, "c": c, "v": None, "c2": c2, "v2": None, "at": j})
                        chapter = c2
                        i = end = ch.end()
                        continue
                vm = _VERSE.match(text, j)
                if vm and k.group(1) != ";" and out[-1]["v"] is not None:
                    v = int(vm.group(1))
                    v2 = int(vm.group(2)) if vm.group(2) else v
                    out.append({"book": book, "c": chapter, "v": v, "c2": chapter, "v2": v2, "at": j})
                    i = end = vm.end()
                    continue
            book = None
        if i == 0 or not text[i - 1].isalnum():
            m = _TOKEN.match(text, i)
            if m:
                b = book_of(m.group("ord"), m.group("name"))
                if b:
                    cv = _CV.match(text, m.end())
                    if cv and b not in SINGLE_CHAPTER:
                        book = b
                        i = end = _take(text, cv, book, out, i)
                        chapter = out[-1]["c2"]
                        continue
                    if cv and b in SINGLE_CHAPTER and cv.group("c") == "1":     # "Jude 1:3"
                        book = b
                        i = end = _take(text, cv, book, out, i)
                        chapter = 1
                        continue
                    ch = _CHAPTER.match(text, m.end()) if b not in SINGLE_CHAPTER else None
                    if ch:
                        book = b
                        c = int(ch.group(1))
                        c2 = int(ch.group(2)) if ch.group(2) else c
                        out.append({"book": b, "c": c, "v": None, "c2": c2, "v2": None, "at": i})
                        chapter = c2
                        i = end = ch.end()
                        continue
                    vm = _VERSE.match(text, m.end()) if b in SINGLE_CHAPTER else None
                    if vm:
                        book, chapter = b, 1
                        v = int(vm.group(1))
                        v2 = int(vm.group(2)) if vm.group(2) else v
                        out.append({"book": b, "c": 1, "v": v, "c2": 1, "v2": v2, "at": i})
                        i = end = vm.end()
                        continue
                i = max(m.end(), i + 1)
                continue
        i += 1
    return out


_CONT = re.compile(r"\s*([;,]|and\b|&)\s*(?:and\s+)?")
# a number is not a chapter or verse if a ":" or digit follows, or if it is the
# ordinal of the next book ("; 2 Sam. 4", "; 2Sa 4")
_NOT_AFTER = r"(?![\d:]|\s*:|\s?[A-Z][a-z]{0,13}[.,]?\s*\d)"
# a whole chapter (or run of chapters): a number not followed by ":" or another digit
_CHAPTER = re.compile(r"\s*(%s)(?:\s*-\s*(%s))?" % (_NUM, _NUM) + _NOT_AFTER)
_VERSE = re.compile(r"\s*(%s)(?:\s*-\s*(%s))?" % (_NUM, _NUM) + _NOT_AFTER)


def _take(text, cv, book, out, at=None):
    c, v = int(cv.group("c")), int(cv.group("v"))
    j = cv.end()
    c2, v2 = c, v
    r = re.match(r"\s*-\s*(%s)(?:\s*:\s*(%s))?" % (_NUM, _NUM), text[j:])
    if r:
        if r.group(2):
            c2, v2 = int(r.group(1)), int(r.group(2))
        else:
            v2 = int(r.group(1))
        j += r.end()
    out.append({"book": book, "c": c, "v": v, "c2": c2, "v2": v2, "at": cv.start() if at is None else at})
    return j


# ---------------------------------------------------------------- CCEL ThML
_TERM = re.compile(r"<term\b[^>]*>(.*?)</term>\s*<def\b[^>]*>(.*?)</def>", re.S)
_P = re.compile(r"<p\b([^>]*)>(.*?)</p>", re.S)
_SCRIP = re.compile(r"<scripRef\b([^>]*)>(.*?)</scripRef>", re.S)
_ATTR = re.compile(r'(\w+)="([^"]*)"')
_OSIS = re.compile(r"^([1-3]?[A-Za-z]+)\.(\d+)(?:\.(\d+))?(?:-([1-3]?[A-Za-z]+)\.(\d+)(?:\.(\d+))?)?$")


def plain(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def osis_parts(osis):
    """"Gen.4.1-Gen.4.16" -> ("Gen", 4, 1, 4, 16); "Gen.4" -> ("Gen", 4, None, 4, None).
    A range across books, or anything else, -> None."""
    m = _OSIS.match(osis)
    if not m:
        return None
    b, c, v, b2, c2, v2 = m.groups()
    if b2 and b2 != b:
        return None
    c = int(c)
    v = int(v) if v else None
    if b2:
        c2 = int(c2)
        v2 = int(v2) if v2 else None
    else:
        c2, v2 = c, v
    return (b, c, v, c2, v2)


def ccel_entries(path):
    """[{"term", "paras": [{"depth", "text", "tagged": [{"osis", "shown"}]}]}]
    in file order. depth comes from class="indexN" (N-1), else 0. The cross
    index at the back of the book (class bbook/bref) is not an entry."""
    with open(path, encoding="utf-8") as f:
        s = f.read()
    body = s[s.find("<ThML.body"):]
    out = []
    for tm in _TERM.finditer(body):
        term = plain(tm.group(1))
        paras = []
        for pm in _P.finditer(tm.group(2)):
            attrs = dict(_ATTR.findall(pm.group(1)))
            cls = attrs.get("class", "")
            dm = re.match(r"index(\d)", cls)
            depth = int(dm.group(1)) - 1 if dm else 0
            inner = pm.group(2)
            tagged = []
            for sm in _SCRIP.finditer(inner):
                osis = dict(_ATTR.findall(sm.group(1))).get("osisRef", "")
                tagged.append({"osis": re.sub(r"^Bible[^:]*:", "", osis), "shown": plain(sm.group(2))})
            paras.append({"depth": depth, "text": plain(inner), "tagged": tagged})
        out.append({"term": term, "paras": paras})
    return out
