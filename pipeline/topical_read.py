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
    ("Sus", "Sus Susanna"),
    ("Bel", "Bel"),
]
# books that need an ordinal, and the OSIS name each ordinal makes
NUMBERED = {"Sam": "Sam", "Kgs": "Kgs", "Chr": "Chr", "Cor": "Cor", "Thess": "Thess",
            "Tim": "Tim", "Pet": "Pet", "Macc": "Macc", "Esd": "Esd"}
FORM = {}
for _b, _forms in BOOK_FORMS:
    for _f in _forms.split():
        FORM.setdefault(_f, _b)
FORM["Ti"] = "Titus"        # unnumbered Ti is Titus; 1 Ti / 2 Ti is Timothy (below)
# the 17th-century forms (Poole, 1683): I for J, and longer abbreviations.
# Only refs(old=True) reads them: "Iob" or "Luc" in a modern book is not a book.
OLD_BOOK_FORMS = [
    ("Gen", "Gene"), ("Lev", "Levit"), ("Deut", "Deuter Deutr"),
    ("Josh", "Ios Iosh Ioshua"), ("Judg", "Iudg Iudges"), ("Kgs", "King"), ("Chr", "Chro"),
    ("Neh", "Nehem"), ("Job", "Iob"), ("Ps", "Psal"), ("Isa", "Isai Esa"),
    ("Jer", "Ier Ierem Ieremiah Jerem"), ("Lam", "Lament"), ("Ezek", "Ezech Ezeck"), ("Hos", "Hose"),
    ("Joel", "Ioel"), ("Amos", "Amo"), ("Jonah", "Ionah"), ("Mic", "Mich"), ("Hab", "Habak"),
    ("Zeph", "Zephan Soph"), ("Zech", "Zach"), ("Mal", "Malach"),
    ("Matt", "Matth Math"), ("Luke", "Luc"), ("John", "Ioh Iohn"), ("Gal", "Galath"),
    ("Eph", "Ephes"), ("Col", "Colos Coloss"), ("Heb", "Hebr"), ("Jas", "Iam Iames"),
    ("Jude", "Iude"), ("Rev", "Revel"), ("Macc", "Maccab"),
]
FORM_OLD = dict(FORM)
for _b, _forms in OLD_BOOK_FORMS:
    for _f in _forms.split():
        FORM_OLD.setdefault(_f, _b)
SINGLE_CHAPTER = {"Obad", "Phlm", "2John", "3John", "Jude", "Sus", "Bel"}

_ORD = {"1": "1", "2": "2", "3": "3", "4": "4", "I": "1", "II": "2", "III": "3", "IV": "4",
        "i": "1", "ii": "2", "iii": "3", "iv": "4"}
# 3 and 4 Maccabees, 3 and 4 Esdras (the Vulgate's names for 1 and 2 Esdras)
_ORDINALS = {"Macc": ("1", "2", "3", "4"), "Esd": ("1", "2", "3", "4")}
# a two-letter form that is also an English word reads a bare chapter only with
# its point: "Is. 40" is Isaiah, "Is 40 days" is not
_WORDLIKE = {"Is", "Am", "So", "Ex", "Re"}
# names printed in several words, read as one form; the same length, so every
# "at" still indexes the text as given
_MULTI = re.compile(r"\bSong of (?:Solomon|Songs)\b|\bS\. of S\.")
# "Ps. 51:title", "Ps. 3 title", "Ps. 18 (title)": the title, which the KJV
# does not number; read as no reference, not as the whole psalm
_PS_TITLE = re.compile(r"\s*(\d{1,3})\s*[:,.]?\s*\(?\s*(?:title|tit)\b\.?\)?")
_BOOK_RE = r"(?:(?P<ord>[1234]|IV|I{1,3}|iv|i{1,3})\s?\.?\s*)?(?P<name>[A-Z][a-z]{0,13})\b[.,]?"
_NUM = r"\d{1,3}"
# chapter : verse, the colon free to float ("19 : 16", "11: 4"), or a dot (Easton's "Gen. 4.1" never; but OCR)
# chapter:verse, or (Henry, the older printings) a lower-case Roman chapter: "Heb. xi. 4"
# (and JFB's 1873 printing writes "Genesis 19. 1": a point for the colon)
_CV = re.compile(r"\s*(?:(?P<c>%s)\s*:\s*|(?P<r>[ivxlc]{1,8})\.\s*)(?P<v>%s)" % (_NUM, _NUM))
_CV_POINT = re.compile(r"\s*(?:(?P<c>%s)\s*(?::|\.(?=\s*\d))\s*|(?P<r>[ivxlc]{1,8})\.\s*)(?P<v>%s)(?!\s?[A-Z][a-z]{0,13}\.?\s*\d)" % (_NUM, _NUM))

_CV_ANY_COMMA = re.compile(r"\s*(?:(?P<c>%s)\s*[:,]\s*|(?P<r>[ivxlc]{1,8})[.,]\s*)(?P<v>%s)" % (_NUM, _NUM))
_CV_COMMA = re.compile(r"\s*(?:(?P<c>%s)\s*:\s*|(?P<r>[ivxlc]{1,8})[.,]\s*)(?P<v>%s)" % (_NUM, _NUM))


def _chap(cv):
    return int(cv.group("c")) if cv.group("c") else _roman(cv.group("r"))


def _roman(r):
    vals = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100}
    n = 0
    for a, b in zip(r, r[1:] + " "):
        n += -vals[a] if b != " " and vals[b] > vals[a] else vals[a]
    return n
_TOKEN = re.compile(_BOOK_RE)


def book_of(ordinal, name, forms=FORM):
    """("1", "Kings") -> "1Kgs"; (None, "Ge") -> "Gen"; None if not a book."""
    b = forms.get(name)
    if name == "Jo" and ordinal:      # 1 Jo. is an epistle; a bare Jo. is Joshua or John, neither
        b = "John"
    if b is None:
        return None
    o = _ORD.get(ordinal) if ordinal else None
    if b in NUMBERED:
        return (o + b) if o in _ORDINALS.get(b, ("1", "2")) else None
    if b == "Titus" and name == "Ti" and o:
        return o + "Tim" if o in ("1", "2") else None
    if o == "4":
        return None
    if b == "John" and o:
        return o + "John" if o in ("1", "2", "3") else None
    if o:
        return None
    return b


def refs(text, here=None, point=False, old=False, roman_comma=False, comma=False):
    """Every reference in text, in order: [{"book", "c", "v", "c2", "v2", "at"}].
    A book carries over to a following "c:v" after ";" or "," and to bare
    verse numbers after "," or "and"; a range ends at a verse ("16-20") or a
    chapter:verse ("16:1-17:3").

    here=(book, chapter) is the passage a commentary is on: then "ver. 31",
    "v. 3", "verses 25-27" are verses of that chapter and "ch. 3:5" / "ch. 3"
    a place in that book. Without it they are not references.

    old=True also reads the 17th-century book forms (OLD_BOOK_FORMS).

    point=True also reads "Genesis 19. 1" (JFB's 1873 printing): only for
    the commentaries' print check, where a point after a chapter is the colon.
    The topical books' scans print "Gen. 19. 1" too rarely to need it, and
    there it misreads more than it finds.

    roman_comma=True also reads a comma after a Roman chapter ("Luke iii, 31"),
    as CCEL's Wesley prints them; comma=True a comma after any chapter ("Heb.
    13, 9"), as CCEL's Hodge does (there "Ps. 23, 24" is a verse, not two psalms)."""
    _CV = _CV_POINT if point else (_CV_ANY_COMMA if comma else _CV_COMMA if roman_comma else globals()["_CV"])
    forms = FORM_OLD if old else FORM
    out = []
    text = text.replace("\u2014", "-").replace("\u2013", "-")
    text = _MULTI.sub(lambda m: "Song".ljust(len(m.group(0))), text)
    n = len(text)
    i = 0
    book = chapter = None
    end = -1
    while i < n:
        if book and i == end:
            k = (_CONT_POINT if point else _CONT).match(text, i)
            if k:
                j = k.end()
                cv = _CV.match(text, j)
                if cv:
                    i = end = _take(text, cv, book, out)
                    chapter = out[-1]["c2"]
                    continue
                prev_v = out[-1]["v"] if out else None      # nothing yet: "Ps. 3 title; 4:1"
                if (k.group(1) == ";" or prev_v is None) and chapter is not None \
                        and book not in SINGLE_CHAPTER:
                    ch = _CHAPTER.match(text, j)
                    if ch:
                        c = int(ch.group(1))
                        c2 = int(ch.group(2)) if ch.group(2) else c
                        out.append({"book": book, "c": c, "v": None, "c2": c2, "v2": None, "at": j, "end": ch.end()})
                        chapter = c2
                        i = end = ch.end()
                        continue
                vm = _VERSE.match(text, j)
                if vm and (k.group(1) != ";" or book in SINGLE_CHAPTER) and prev_v is not None:
                    v = int(vm.group(1))
                    v2 = int(vm.group(2)) if vm.group(2) else v
                    out.append({"book": book, "c": chapter, "v": v, "c2": chapter, "v2": v2, "at": j, "end": vm.end()})
                    i = end = vm.end()
                    continue
            book = None
        # "Ver. 3", "Chap. 3. 4" capitalised only in the old books: CCEL's
        # Barnes heads its comments "Chapter 1 - Verse 2", which cite nothing
        if here and (i == 0 or not text[i - 1].isalnum()) and text[i] in ("vVcC" if old else "vc"):
            rm = _REL_V.match(text, i)
            if rm and _context(text, i, out, here, forms)[1] is not None:
                book, chapter = _context(text, i, out, here, forms)
                v = int(rm.group(1))
                v2 = int(rm.group(2)) if rm.group(2) else v
                out.append({"book": book, "c": chapter, "v": v, "c2": chapter, "v2": v2, "at": i, "end": rm.end()})
                i = end = rm.end()
                continue
            rm = _REL_CH.match(text, i)
            if rm:
                book = _context(text, i, out, here, forms, chapter_ref=True)[0]
                c = int(rm.group(1)) if rm.group(1).isdigit() else _roman(rm.group(1))
                if rm.group(2):
                    v = int(rm.group(2))
                    v2 = int(rm.group(3)) if rm.group(3) else v
                    out.append({"book": book, "c": c, "v": v, "c2": c, "v2": v2, "at": i, "end": rm.end()})
                else:
                    out.append({"book": book, "c": c, "v": None, "c2": c, "v2": None, "at": i, "end": rm.end()})
                chapter = c
                i = end = rm.end()
                continue
        if i == 0 or not text[i - 1].isalnum():
            m = _TOKEN.match(text, i)
            if m:
                b = book_of(m.group("ord"), m.group("name"), forms)
                if b:
                    cv = _CV.match(text, m.end())
                    if cv and cv.group("r") and text[i:m.end()].endswith(","):
                        cv = None        # "Daniel, v. 3" is a verse of here, not Daniel 5:3
                    if cv and b not in SINGLE_CHAPTER:
                        book = b
                        i = end = _take(text, cv, book, out, i)
                        chapter = out[-1]["c2"]
                        continue
                    if cv and b in SINGLE_CHAPTER and _chap(cv) == 1:     # "Jude 1:3"
                        book = b
                        i = end = _take(text, cv, book, out, i)
                        chapter = 1
                        continue
                    pt = _PS_TITLE.match(text, m.end()) if b == "Ps" else None
                    if pt:
                        book, chapter = b, int(pt.group(1))
                        i = end = pt.end()
                        continue
                    ch = _CHAPTER.match(text, m.end()) if b not in SINGLE_CHAPTER else None
                    # "Is 40 days" is prose; Nave's "Ex 32; Ac 7:40" is not: without
                    # its point, a word-like form reads a chapter only before punctuation
                    if ch and m.group("name") in _WORDLIKE and not m.group(0).endswith(".") \
                            and re.match(r"\s*[A-Za-z]", text[ch.end():]):
                        ch = None
                    if ch:
                        book = b
                        c = int(ch.group(1))
                        c2 = int(ch.group(2)) if ch.group(2) else c
                        out.append({"book": b, "c": c, "v": None, "c2": c2, "v2": None, "at": i, "end": ch.end()})
                        chapter = c2
                        i = end = ch.end()
                        continue
                    vm = _VERSE.match(text, m.end()) if b in SINGLE_CHAPTER else None
                    if vm:
                        book, chapter = b, 1
                        v = int(vm.group(1))
                        v2 = int(vm.group(2)) if vm.group(2) else v
                        out.append({"book": b, "c": 1, "v": v, "c2": 1, "v2": v2, "at": i, "end": vm.end()})
                        i = end = vm.end()
                        continue
                i = max(m.end(), i + 1)
                continue
        i += 1
    return out


_CONT = re.compile(r"\s*([;,]|and\b|&)\s*(?:and\s+)?")
# Poole and the older printings close each reference with a point: "chap. 7. 34. & 25. 10."
_CONT_POINT = re.compile(r"\.?\s*([;,]|and\b|&)\s*(?:and\s+)?")
# a number is not a chapter or verse if a ":" or digit follows, or if it is the
# ordinal of the next book ("; 2 Sam. 4", "; 2Sa 4")
_NOT_AFTER = r"(?![\d:]|\s*:|\s?[A-Z][a-z]{0,13}[.,]?\s*\d)"
_REL_V = re.compile(r"(?:[Vv]erses|[Vv]erse|[Vv]ers|[Vv]er|vv|v)\.?\s*(\d{1,3})(?:\s*-\s*(\d{1,3}))?(?![\d:])")
_REL_CH = re.compile(r"(?:[Cc]hapter|[Cc]hap|[Cc]ap|[Cc]h)\.?\s*(\d{1,3}|[ivxlc]{1,8}(?=\.))(?:(?:\s*[:.]\s*|\s*,\s*(?=[Vv]))(?:(?:[Vv]er(?:se)?|v)\.?\s*)?(\d{1,3})(?:\s*-\s*(\d{1,3}))?)?" + _NOT_AFTER)
# a whole chapter (or run of chapters): a number not followed by ":" or another digit
_CHAPTER = re.compile(r"\s*(%s)(?:\s*-\s*(%s))?" % (_NUM, _NUM) + _NOT_AFTER)
_VERSE = re.compile(r"\s*(%s)(?:\s*-\s*(%s))?" % (_NUM, _NUM) + _NOT_AFTER)


_NEAR = 40     # characters: a reference this close lends "ver. 31" its book and chapter
_NAMED = re.compile(_BOOK_RE.replace("(?P<ord>", "(?P<o>").replace("(?P<name>", "(?P<n>"))


# names a sentence may give a book in, without a point ("as Luke tells us");
# a shorter form only counts with its point ("Ezek. chap."), and "Philip" is a man
_SPELLED = {"Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
            "Samuel", "Kings", "Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Psalm",
            "Proverbs", "Ecclesiastes", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel",
            "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
            "Haggai", "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
            "Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "Thessalonians",
            "Timothy", "Titus", "Philemon", "Hebrews", "James", "Peter", "Jude", "Revelation"}


def _context(text, i, out, here, forms, chapter_ref=False):
    """(book, chapter) for a relative "ver. 31" / "ch. 3. 4" at i: a book
    named just before with no number after it ("as Luke tells us, ch. 1. 26",
    "Ezek. chap. 27. 28"); else the reference just read, if it ended within
    _NEAR characters in the same sentence ("Exod. 30. 25. to ver. 31"); else
    the comment's own place. "Chap. 20. 12" right after another book's
    reference is still the comment's own book (Poole: "Gal. 6. 5. Chap. 20.
    12" on Revelation), so chapter_ref skips the second rule."""
    last_end = out[-1].get("end", -10 ** 9) if out else -10 ** 9
    win_from = max(0, i - 40, last_end)
    win = text[win_from:i]
    last = None
    for m in _NAMED.finditer(win):
        last = m
    # a short form only with its point ("So here" is not the Song)
    if last and not re.search(r"\d", win[last.end():]) and len(win[last.end():].split()) <= 3 \
            and (last.group(0).endswith(".") or last.group("n") in _SPELLED):
        b = book_of(last.group("o"), last.group("n"), forms)
        if b:
            return b, here[1] if b == here[0] else None
    if not chapter_ref and out and last_end > i - _NEAR and out[-1]["c2"] is not None \
            and not re.search(r"[.;:?!]\s+[A-Z]|\(|\)", text[last_end:i + 1]):
        return out[-1]["book"], out[-1]["c2"]
    return here


_RANGE = re.compile(r"\s*-\s*(%s)(?:\s*:\s*(%s))?" % (_NUM, _NUM))


def _take(text, cv, book, out, at=None):
    c, v = _chap(cv), int(cv.group("v"))
    j = cv.end()
    c2, v2 = c, v
    r = _RANGE.match(text, j)
    if r:
        if r.group(2):
            c2, v2 = int(r.group(1)), int(r.group(2))
        else:
            v2 = int(r.group(1))
        j = r.end()
    out.append({"book": book, "c": c, "v": v, "c2": c2, "v2": v2, "at": cv.start() if at is None else at, "end": j})
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
