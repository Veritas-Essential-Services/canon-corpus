#!/usr/bin/env python3
"""scripture_refs.py -- the master map of how old books cite scripture.

A citation in an old book is four parts, each drawn from a finite set:

    BOOK      a name form: Romans / Rom. / Rom / Ro. ; Esay (1611) ; Sap. (Latin
              Wisdom) ; 3 Kings (Douay = KJV 1 Kings) ; Apoc. ; Ps./Psal./Psalm
    ORDINAL   1 / I / i. / 1st / First (for the numbered books)
    CHAPTER   8 / viii / VIII / cap. 8 / ch. viii / chap. 8
    VERSE     :28 / . 28 / , 28 (Latin, German) / ver. 28 / v. 28 ; ranges 28-30,
              lists 28, 30

plus continuation: "Rom. 8. 28; 11. 36" carries the book, "ver. 12" carries
the chapter, "ib." / "ibid." repeats the last book. This module is that map:
find(text, profile) returns every citation in a text, resolved to KJV OSIS
ids, each with the convention it matched and how sure it is.

The hard cases are a SHORT, KNOWN list, and each has a rule:

  * one abbreviation, several books ("Jud." = Jude, Judges or Judith; "Jo." =
    John or Joshua; "Phil." = Philippians or Philemon): the candidates are
    tried against the KJV's verse list -- Jude has one chapter, so
    "Jud. 5. 3" cannot be Jude -- and when more than one survives, the
    work's PROFILE decides; if it cannot, the citation is kept as
    `ambiguous` with its candidates, for a human (the review sheet).
  * a name that means different books in different traditions ("1 Kings"
    is KJV 1 Kings to a Protestant and KJV 1 Samuel in the Douay; "2
    Esdras" is Nehemiah in the Vulgate): the PROFILE decides.
  * Psalm numbers in a Latin or Greek work (Vulgate/LXX Ps 22 = KJV Ps 23):
    the profile routes them through versification.lxx_to_kjv().
  * a book name that is also a word or a person (Job, Mark, John, Acts,
    Ruth, Amos, Numbers, "Is.", "Am."): accepted only with a chapter AND a
    verse, never on a bare chapter.

PROFILES (per work, set by whoever shelves it): "protestant" (the default:
English, KJV numbering), "douay" (English Catholic: 1-4 Kings = 1-2 Samuel,
1-2 Kings; Vulgate Psalm numbers), "vulgate" (Latin). A Puritan cites the
KJV way; Aquinas cites the Vulgate way; the same "Ps. 22." is two different
psalms in them.

Output: [{"kind": "scripture", "osis": "Rom.8.28", "raw": "Rom. viii. 28",
"start": 1234, "end": 1247, "convention": "abbrev.+roman-chapter",
"confidence": "exact" | "inferred" | "ambiguous", ...}] -- `osis` is the KJV
verse, the field Armarium indexes. A range gives one link per verse (at most
MAX_RANGE), each marked `range`. A chapter with no verse ("Rom. 8.") is kept
as `osis_chapter`, never as a verse.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
KJV = os.path.join(HERE, "..", "data", "greppable", "kjv.tsv")
KJVA = os.path.join(HERE, "..", "data", "greppable", "kjv-apocrypha.tsv")
MAX_RANGE = 40

# ---------------------------------------------------------------- the book names
# OSIS -> every name form, across English (modern, 1611/Geneva, Puritan), Latin
# (Vulgate), Douay, and scholarly abbreviation. Forms are matched case-
# insensitively, with or without a trailing period, and with the ordinal
# written any way ORDINAL allows. A form listed under several books is an
# AMBIGUITY and is resolved as the module docstring says.
NAMES = {
    "Gen": "Genesis Gen Gene Gn Ge",
    "Exod": "Exodus Exod Exo Ex Exo",
    "Lev": "Leviticus Levit Lev Lv Le",
    "Num": "Numbers Numb Num Nu Nm Numeri",
    "Deut": "Deuteronomy Deuteronomie Deut Deu Dt De",
    "Josh": "Joshua Josua Josue Josh Jos Jsh Jo",
    "Judg": "Judges Judg Jdg Jdgs Judic Judicum Jud Jg",
    "Ruth": "Ruth Ru Rt",
    "1Sam": "1Samuel 1Sam 1Sa 1S 1Sm",
    "2Sam": "2Samuel 2Sam 2Sa 2S 2Sm",
    "1Kgs": "1Kings 1Kin 1Kgs 1Ki 1K 3Kings 3Kin 3Reg 3Regum",
    "2Kgs": "2Kings 2Kin 2Kgs 2Ki 2K 4Kings 4Kin 4Reg 4Regum",
    "1Chr": "1Chronicles 1Chron 1Chr 1Ch 1Paralipomenon 1Paral 1Par",
    "2Chr": "2Chronicles 2Chron 2Chr 2Ch 2Paralipomenon 2Paral 2Par",
    "Ezra": "Ezra Ezr",
    "Neh": "Nehemiah Nehemias Nehem Neh Ne",
    "Esth": "Esther Esth Est Es",
    "Job": "Job Jb",
    "Ps": "Psalms Psalm Psal Psa Pss Ps",
    "Prov": "Proverbs Proverbes Prov Pro Prv Pr",
    "Eccl": "Ecclesiastes Ecclesiast Eccles Eccle Eccl Ecc Ec Qoheleth Qoh",
    "Song": "Canticles Canticle Cantic Cant Ct Song SongofSolomon SongofSongs",
    "Isa": "Isaiah Isaias Esay Esai Esa Isai Isa Is",
    "Jer": "Jeremiah Jeremias Jerem Jer Jr Je Hierem Hier",
    "Lam": "Lamentations Lament Lam La Threni Thren",
    "Ezek": "Ezekiel Ezechiel Ezekiel Ezech Ezek Eze Ezk Ez",
    "Dan": "Daniel Dan Dn Da",
    "Hos": "Hosea Osee Hos Ho Os",
    "Joel": "Joel Jl",
    "Amos": "Amos Am",
    "Obad": "Obadiah Abdias Obad Ob Abd",
    "Jonah": "Jonah Jonas Jon",
    "Mic": "Micah Micheas Michaeas Mich Mic Mi",
    "Nah": "Nahum Naum Nah Na",
    "Hab": "Habakkuk Habacuc Habakuk Habak Habac Hab Hb",
    "Zeph": "Zephaniah Sophonias Zeph Zep Soph Zp",
    "Hag": "Haggai Aggeus Aggaeus Hagg Hag Agg Hg",
    "Zech": "Zechariah Zacharias Zachary Zech Zach Zec Zac Zc",
    "Mal": "Malachi Malachias Malach Mal Ml",
    "Matt": "Matthew Matthaeus Matth Matt Mat Mt",
    "Mark": "Mark Marcus Marc Mar Mrk Mk Mc",
    "Luke": "Luke Lucas Luk Luc Lk Lc",
    "John": "John Joannes Joan Joh Jhn Jn Jo",
    "Acts": "Acts Actes Act Ac",
    "Rom": "Romans Rom Ro Rm",
    "1Cor": "1Corinthians 1Corinth 1Cor 1Co",
    "2Cor": "2Corinthians 2Corinth 2Cor 2Co",
    "Gal": "Galatians Galat Gal Ga",
    "Eph": "Ephesians Ephes Eph Ep",
    "Phil": "Philippians Philipp Philip Phil Php Phl",
    "Col": "Colossians Coloss Colos Col",
    "1Thess": "1Thessalonians 1Thessal 1Thess 1Thes 1Th",
    "2Thess": "2Thessalonians 2Thessal 2Thess 2Thes 2Th",
    "1Tim": "1Timothy 1Timoth 1Tim 1Ti",
    "2Tim": "2Timothy 2Timoth 2Tim 2Ti",
    "Titus": "Titus Tit Ti",
    "Phlm": "Philemon Philem Phlm Phm Phil",
    "Heb": "Hebrews Hebr Heb He",
    "Jas": "James Jacobus Jam Jas Jac Jm",
    "1Pet": "1Peter 1Petr 1Pet 1Pe 1Pt",
    "2Pet": "2Peter 2Petr 2Pet 2Pe 2Pt",
    "1John": "1John 1Joannes 1Joan 1Joh 1Jn 1Jo",
    "2John": "2John 2Joannes 2Joan 2Joh 2Jn 2Jo",
    "3John": "3John 3Joannes 3Joan 3Joh 3Jn 3Jo",
    "Jude": "Jude Judas Jud Jd",
    "Rev": "Revelation Revelations Revel Rev Re Apocalypse Apocalypsis Apoc Apc",
}
# Books outside the KJV's 66, named so a citation of them is RECOGNISED (and not
# misread as a KJV book), resolved to no KJV verse. Several also collide:
# "Jud." may be Judith, "Ecclus." is Sirach, not Ecclesiastes.
APOCRYPHA = {
    "Tob": "Tobit Tobias Tob Tb",
    "Jdt": "Judith Judit Jdt Jud Jth",
    "Wis": "Wisdom Sapientia Sap Wis Wisd WisdomofSolomon",
    "Sir": "Sirach Ecclesiasticus Ecclus Eccli Sir Ecclesiastic",
    "Bar": "Baruch Bar",
    "EpJer": "EpistleofJeremy EpistleofJeremiah EpJer",
    "1Macc": "1Maccabees 1Machabees 1Mach 1Macc 1Mac 1Ma",
    "2Macc": "2Maccabees 2Machabees 2Mach 2Macc 2Mac 2Ma",
    "1Esd": "1Esdras 1Esd",
    "2Esd": "2Esdras 2Esd",
    "PrAzar": "SongoftheThreeHolyChildren SongoftheThreeChildren SongofThreeChildren SongoftheThree SongofThree PrAzar PrAzariah Azar",
    "Sus": "Susanna Susan Sus HistSus",
    "Bel": "BelandtheDragon Bel",
    "PrMan": "PrayerofManasses PrayerofManasseh Manasses PrMan PrMa",
    "AddEsth": "RestofEsther AddEsth AddEst",
}
# Traditions whose NAMES mean other books (profile -> form -> OSIS).
PROFILE_NAMES = {
    "douay": {"1kings": "1Sam", "2kings": "2Sam", "3kings": "1Kgs", "4kings": "2Kgs",
              "1kin": "1Sam", "2kin": "2Sam", "3kin": "1Kgs", "4kin": "2Kgs",
              "1esdras": "Ezra", "2esdras": "Neh", "1esd": "Ezra", "2esd": "Neh"},
    "vulgate": {"1reg": "1Sam", "2reg": "2Sam", "3reg": "1Kgs", "4reg": "2Kgs",
                "1regum": "1Sam", "2regum": "2Sam", "3regum": "1Kgs", "4regum": "2Kgs",
                "1esdr": "Ezra", "2esdr": "Neh", "1esdras": "Ezra", "2esdras": "Neh"},
}
PROFILE_NAMES["vulgate"].update({k: v for k, v in PROFILE_NAMES["douay"].items() if k not in PROFILE_NAMES["vulgate"]})
# Default preference where one form names several books and the verse fits more than one.
PREFER = {"protestant": {"jud": "Jude", "jo": "John", "phil": "Phil", "ep": "Eph", "es": "Esth",
                         "ti": "Titus", "he": "Heb", "ez": "Ezek", "is": "Isa"},
          "douay": {"jud": "Judg", "jo": "John", "phil": "Phil", "ep": "Eph", "es": "Esth", "ti": "Titus",
                    "he": "Heb", "ez": "Ezek", "is": "Isa"},
          "vulgate": {"jud": "Judg", "jo": "John", "phil": "Phil", "ep": "Eph", "es": "Esth", "ti": "Titus",
                      "he": "Heb", "ez": "Ezek", "is": "Isa"}}
# Names that are also everyday words or persons: never accepted on a bare
# chapter, nor with a lower-case initial.
RISKY = {"job", "mark", "john", "acts", "act", "ruth", "amos", "joel", "numbers", "judges", "kings", "song",
         "is", "am", "ex", "ac", "ro", "re", "he", "ep", "ga", "col", "mal", "hab", "mic", "nah", "dan",
         "lam", "jer", "ps", "pr", "ob", "jon", "gen", "es", "da", "ho", "na", "mi", "hg", "am", "jo",
         "rev", "tit", "ti", "pro", "ne", "de", "le", "nu", "ru", "jud", "jd", "jas", "jam", "ct", "mt",
         "mk", "lk", "jn", "ec", "ez", "ch", "lamentations", "canticles", "revelation", "james", "luke",
         "matthew", "daniel", "jonah", "hosea", "micah", "titus", "jude", "baruch", "judith", "tobit", "manasses", "manasseh"}

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
    return total if 0 < total <= 176 else None


def _key(name):
    return re.sub(r"[\s.]", "", name).lower()


def _build_forms():
    forms = {}
    for table, tag in ((NAMES, "kjv"), (APOCRYPHA, "apocrypha")):
        for osis, names in table.items():
            for n in names.split():
                forms.setdefault(_key(n), []).append((osis, tag))
    for prof, table in PROFILE_NAMES.items():
        for k, osis in table.items():
            forms.setdefault(k, []).append((osis, f"profile:{prof}"))
    return forms


FORMS = _build_forms()

# ---------------------------------------------------------------- the KJV's shape, to test candidates
_SHAPE = None


def shape():
    """{book: {chapter: last verse}} from the committed KJV table."""
    global _SHAPE
    if _SHAPE is None:
        _SHAPE = {}
        for path in (KJV, KJVA):
            if not os.path.exists(path):
                continue
            with open(path, encoding="utf-8") as f:
                next(f)
                for line in f:
                    b, c, v = line.split("\t", 1)[0][4:].split(".")
                    d = _SHAPE.setdefault(b, {})
                    d[int(c)] = max(d.get(int(c), 0), int(v))
    return _SHAPE


def verse_exists(b, c, v=None):
    s = shape().get(b)
    if not s or c not in s:
        return False
    return v is None or 1 <= v <= s[c]


SINGLE_CHAPTER = {"Obad", "Phlm", "2John", "3John", "Jude", "PrAzar", "Sus", "Bel", "PrMan", "EpJer"}

# ---------------------------------------------------------------- the grammar
_names = sorted({n for names in list(NAMES.values()) + list(APOCRYPHA.values()) for n in names.split()}
                | {"Kings", "Kin", "Reg", "Regum", "Esdras", "Esdr", "Esd", "Paralipomenon", "Paral", "Par"},
                key=len, reverse=True)
_bare = sorted({re.sub(r"^[1-4]", "", n) for n in _names}, key=len, reverse=True)
ORDINAL = r"(?:(?P<ord>[1-4]|I{1,3}|IV|i{1,3}|iv)(?:st|nd|rd|d|th)?\.?\s*|(?P<ordw>First|Second|Third|Fourth|1st|2nd|3rd|4th)\s+)"
# names printed as several words; matched with any spacing, keyed without it
MULTIWORD = ["Song of the Three Holy Children", "Song of the Three Children", "Song of Three Children",
             "Song of the Three", "Epistle of Jeremy", "Epistle of Jeremiah", "Rest of Esther",
             "Bel and the Dragon", "Prayer of Manasses", "Prayer of Manasseh", "Wisdom of Solomon",
             "Song of Solomon", "Song of Songs", "Hist. Sus", "Pr. Azar", "Pr. Man", "Add. Esth", "Ep. Jer"]
for _m in MULTIWORD:
    _k = re.sub(r"[\s.]", "", _m)
    if not any(_key(n) == _k.lower() for n in _names):
        FORMS.setdefault(_k.lower(), [])
_MW = r"|".join(r"\.?\s*".join(re.escape(w) for w in re.split(r"\.?\s+", m))
                for m in sorted(MULTIWORD, key=len, reverse=True))
BOOK = r"(?P<book>" + _MW + "|" + "|".join(re.escape(n) for n in _bare if n) + r")\b\.?"
NUM = r"(?:\d{1,3}|[ivxlcIVXLC]{1,8})"
CHAP = r"(?:(?:cap|chap|chapt|ch|c)\.\s*|(?:cap|chap|chapter)\s+)?(?P<ch>" + NUM + r")"
VERSE_SEP = r"(?:\s*[:.,]\s*|\s+)(?:(?:ver|vers|verse|vv|v|vs)\.?\s*)?"
_BOOKLOOK = r"(?!\s*\.?\s*(?:" + "|".join(re.escape(n) for n in _bare if len(n) > 1) + r")\b)"
VERSE = r"(?P<vs>\d{1,3}(?:\s*[-–—]\s*\d{1,3}|\s*,\s*\d{1,3}(?!\s*[:.]\s*\d)" + _BOOKLOOK + r")*)"
RE_CITE = re.compile(r"(?<![\w])" + ORDINAL + r"?" + BOOK + r"\s*" + CHAP + r"(?:" + VERSE_SEP + VERSE + r")?"
                     r"(?!\d)(?!:\s*\d)")
# a continuation after a citation: "; 11. 36" (same book), ", ver. 12" (same chapter), "ib. 3. 4"
RE_NEXT = re.compile(r"\s*[;,]\s*(?:(?P<ib>ib|ibid|ibidem)\.?\s*)?(?:(?:(?P<ver>ver|vers|verse|vv|v)\.?\s*)"
                     r"(?P<only_vs>\d{1,3}(?:\s*[-–—]\s*\d{1,3})?)|(?P<ch>" + NUM + r")" + VERSE_SEP + VERSE + r")"
                     r"(?![\w:])")


def _num(s):
    s = s.strip()
    return int(s) if s.isdigit() else roman(s)


def _ordinal(m):
    o = m.group("ord") or m.group("ordw")
    if not o:
        return ""
    o = o.lower().rstrip(".")
    return {"first": "1", "second": "2", "third": "3", "fourth": "4", "1st": "1", "2nd": "2", "3rd": "3",
            "4th": "4"}.get(o, str(roman(o)) if roman(o) else re.sub(r"\D", "", o))


def _verses(vs):
    """'28-30, 32' -> [28, 29, 30, 32]"""
    out = []
    for part in re.split(r"\s*,\s*", vs):
        m = re.match(r"(\d+)\s*[-–—]\s*(\d+)", part)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if b >= a and b - a < MAX_RANGE:
                out.extend(range(a, b + 1))
            else:
                out.append(a)
        elif part.strip().isdigit():
            out.append(int(part))
    return out


def candidates(ordinal, book, profile):
    """[(osis, tag)] for a book form under a profile."""
    if ordinal and not FORMS.get(ordinal + _key(book)) and ordinal + _key(book) not in PROFILE_NAMES.get(profile, {}):
        ordinal = ""                       # "i Psalm li. 10": a stray OCR "i", not "1st Psalm"
    k = ordinal + _key(book)
    out = []
    prof = PROFILE_NAMES.get(profile, {})
    if k in prof:
        return [(prof[k], f"profile:{profile}")]
    for osis, tag in FORMS.get(k, []):
        if tag.startswith("profile:"):
            continue
        out.append((osis, tag))
    if not out and not ordinal:
        # "Cor. 13. 12" with its "1" lost (OCR, or a sloppy printer): every numbered book
        for o in "1234":
            out.extend((osis, tag) for osis, tag in FORMS.get(o + k, []) if not tag.startswith("profile:"))
    return out


PRMAN_VERSES = 15


def _fits(o, ch, verses):
    if o == "EpJer":                       # the KJV prints it as Baruch 6
        return verse_exists("Bar", 6, verses[0] if verses else ch)
    if o == "PrMan":                       # printed unnumbered: 15 verses in later editions, one unit here
        return 1 <= (verses[0] if verses else ch) <= PRMAN_VERSES and (not verses or ch == 1)
    return (verse_exists(o, ch, verses[0]) if verses else verse_exists(o, ch)) \
        or (o in SINGLE_CHAPTER and not verses and verse_exists(o, 1, ch))


def resolve(ordinal, book, ch, verses, profile="protestant", raw=""):
    """-> (osis book or None, confidence, [candidate books], why)
    The KJV's canonical books are tried first; the Apocrypha (the KJV's own
    fourteen books) only when no canonical book fits, or when the form can
    only mean an apocryphal book. "Jud. 5. 3" stays Judges, never Judith."""
    cands = candidates(ordinal, book, profile)
    if not cands:
        return None, None, [], "no such book form"
    if any(o == "Esth" for o, _ in cands) and ch > 10:
        # the KJV numbers the Rest of Esther 10:4-16:24, after the canonical ten chapters
        cands = cands + [("AddEsth", "apocrypha")]
    kjv_cands = [o for o, t in cands if t != "apocrypha"]
    apoc = list(dict.fromkeys(o for o, t in cands if t == "apocrypha"))
    fits = [o for o in dict.fromkeys(kjv_cands) if _fits(o, ch, verses)]
    afits = [o for o in apoc if _fits(o, ch, verses)]
    if not fits and afits:
        if len(afits) == 1:
            only = not kjv_cands
            return afits[0], "exact" if only else "inferred", afits, \
                "an apocryphal book" if only else "no canonical book has that verse; the Apocrypha does"
        return None, "ambiguous", afits, "several apocryphal books fit; a human decides"
    if not kjv_cands and not afits:
        return None, "exact", apoc, "an apocryphal book, but the KJV Apocrypha has no such verse" if apoc else "no book"
    if len(fits) == 1:
        if not ordinal and len(set(kjv_cands)) > 1 and all(o[0].isdigit() for o in kjv_cands):
            return fits[0], "inferred", fits, "its number was missing; the verse exists only in this one"
        why = "the verse exists only there" + ("; an apocryphal reading also fits" if afits else "")
        return fits[0], "exact" if len(set(kjv_cands)) == 1 and not afits else "inferred", fits + afits, why
    pref = PREFER.get(profile, {}).get(_key(book))
    if len(fits) >= 1 and pref in fits:
        return pref, "inferred", fits + afits, f"the {profile} reading of {book!r}"
    if not fits:
        return None, None, kjv_cands + apoc, "no candidate book has that chapter and verse"
    return None, "ambiguous", fits + afits, "several books fit; a human decides"


def _psalm(profile, c, v):
    """A Latin/Douay/Greek work numbers the Psalms as the Septuagint does."""
    if profile in ("douay", "vulgate", "septuagint"):
        import versification
        kjvs, rel = versification.lxx_to_kjv(f"Ps.{c}.{v}")
        return kjvs, rel
    return [f"Ps.{c}.{v}"], "same"


def find(text, profile="protestant", ocr=True):
    """Every scripture citation in `text` -> [link dict], in order."""
    out = []
    pos = 0
    while True:
        m = RE_CITE.search(text, pos)
        if not m:
            break
        pos = m.end()
        book, ordinal = m.group("book"), _ordinal(m)
        k = _key(book)
        dotted = m.group(0)[m.start("book") - m.start() + len(book):].lstrip().startswith(".")
        risky = (k in RISKY and not dotted) or (ordinal == "" and len(k) <= 2 and not dotted)
        if book[0].islower() and (risky or len(k) <= 3):
            continue                       # "is 3 and", "am 4", "job 2": words, not books
        ch = _num(m.group("ch"))
        if ch is None:
            continue
        verses = _verses(m.group("vs")) if m.group("vs") else []
        roman_ch = not m.group("ch").isdigit()
        if not verses and (risky or k in RISKY and not dotted or roman_ch and len(m.group("ch")) == 1):
            continue                       # "Mark 2" / "John 3" / "Acts 1": chapter only, too risky
        osis_book, conf, cands, why = resolve(ordinal, book, ch, verses, profile, m.group(0))
        conv = ("roman-chapter" if roman_ch else "arabic") + ("" if verses else ",chapter-only")
        base = {"kind": "scripture", "raw": m.group(0), "start": m.start(), "end": m.end(),
                "convention": conv, "profile": profile}
        emitted = _emit(out, base, osis_book, conf, cands, why, ch, verses, profile)
        # continuations: "; 11. 36", ", ver. 12", "; ib. 3. 4"
        while emitted is not None:
            n = RE_NEXT.match(text, pos)
            if not n:
                break
            pos = n.end()
            if n.group("only_vs"):
                vs = _verses(n.group("only_vs"))
                c2 = ch
            else:
                c2 = _num(n.group("ch"))
                vs = _verses(n.group("vs") or "")
                if c2 is None:
                    break
                ch = c2
            if osis_book:
                ok = verse_exists(osis_book, c2, vs[0] if vs else None)
                cb = {"kind": "scripture", "raw": n.group(0).strip(" ;,"), "start": n.start(),
                      "end": pos, "convention": "continuation", "profile": profile}
                if ok:
                    _emit(out, cb, osis_book, "inferred", [osis_book], "the book carried from the citation before",
                          c2, vs, profile)
    if ocr:
        _ocr_pass(text, out, profile)
    return out


# ---------------------------------------------------------------- OCR-damaged citations
# Scanned books (the Internet Archive shelf, Thayer) print "Mai." for Mal.,
# "Jleb." for Heb., "Lnke" for Luke, and lose the space in "Ezraix. 3". A name
# one keystroke from a known form, or one of OCR's classic confusions away, is
# accepted ONLY when a chapter and a verse follow, the correction is unique,
# and the verse exists; it is labelled confidence "ocr", never "exact".
OCR_SWAPS = [("rn", "m"), ("m", "rn"), ("Jl", "H"), ("Il", "H"), ("li", "h"), ("cl", "d"), ("ii", "u"),
             ("u", "n"), ("n", "u"), ("c", "e"), ("e", "c"), ("i", "l"), ("l", "i"), ("b", "h"), ("h", "b"),
             ("t", "l"), ("f", "s"), ("ſ", "s"), ("E", "R"), ("R", "E"), ("a", "o"), ("o", "a"),
             ("in", "m"), ("ui", "m"), ("r", "v"), ("v", "r"), ("b", "k"), ("n", "r")]
RE_OCR = re.compile(r"(?<![\w])(?:(?P<ord>[1-4I])\.?\s*)?(?P<name>[A-Z][A-Za-zſ]{1,11})(?:\.\s*|\s+)"
                    r"(?P<ch>\d{1,3}|[ivxlc]{1,7})\s*[.:,]\s*(?P<vs>\d{1,3})(?!\d)")
# "Ezraix. 10", "Lukexiii. 5", "Micahvii.8": an exact name with its Roman chapter glued on
RE_GLUED = re.compile(r"(?<![\w])(?:(?P<ord>[1-4I])\.?\s*)?(?P<name>[A-Z][a-z]{2,10}?)(?P<ch>[ivxlc]{1,7})"
                      r"\s*[.:,]\s*(?P<vs>\d{1,3})(?!\d)")
_KNOWN = None


def _known():
    global _KNOWN
    if _KNOWN is None:
        _KNOWN = {n.lower(): n for n in _bare if len(n) >= 3}
    return _KNOWN


def _ocr_book(name):
    """-> the one known form this OCR'd name most plausibly is, or None."""
    known = _known()
    low = name.lower()
    if low in known:
        return None                        # not damaged: the main pass already judged it
    found = set()
    for a, b in OCR_SWAPS:
        i = name.find(a)
        while i != -1:
            fix = (name[:i] + b + name[i + len(a):]).lower()
            if fix in known:
                found.add(known[fix])
            i = name.find(a, i + 1)
    if not found and len(low) >= 4:        # one deletion or insertion
        for k in known:
            if len(k) >= 4 and abs(len(k) - len(low)) == 1:
                long_, short = (k, low) if len(k) > len(low) else (low, k)
                if any(long_[:j] + long_[j + 1:] == short for j in range(len(long_))):
                    found.add(known[k])
    return found.pop() if len(found) == 1 else None


def _ocr_pass(text, out, profile):
    covered = [(d["start"], d["end"]) for d in out]
    for rx, kind in ((RE_GLUED, "glued"), (RE_OCR, "damaged")):
        for m in rx.finditer(text):
            if any(a <= m.start() < b or a < m.end() <= b for a, b in covered):
                continue
            name = m.group("name")
            if kind == "glued":
                book = _known().get(name.lower())
            else:
                book = _ocr_book(name)
            if not book:
                continue
            ch, v = _num(m.group("ch")), int(m.group("vs"))
            if ch is None:
                continue
            o = m.group("ord") or ""
            ordinal = "1" if o == "I" else o
            osis_book, conf, cands, why = resolve(ordinal, book, ch, [v], profile)
            if osis_book is None or conf == "ambiguous":
                continue
            base = {"kind": "scripture", "raw": m.group(0), "start": m.start(), "end": m.end(),
                    "convention": f"ocr-{kind}", "profile": profile, "ocr_read_as": book}
            _emit(out, base, osis_book, "ocr", cands, f"read as {book!r}: {why}", ch, [v], profile)
            covered.append((m.start(), m.end()))
    out.sort(key=lambda d: d["start"])


def _emit(out, base, osis_book, conf, cands, why, ch, verses, profile):
    if osis_book is None:
        if conf is None and cands and verses:
            # "Numb. xii. 24" (Num 12 has 16 verses): the source's slip or its OCR's
            out.append(dict(base, confidence="not-a-verse", candidates=cands, resolved=False, why=why,
                            chapter=ch, verses=verses))
            return None
        if conf == "exact" and cands:      # an apocryphal book: recognised, no KJV verse
            out.append(dict(base, book=cands[0], confidence="exact", resolved=False, why=why))
        elif conf == "ambiguous":
            out.append(dict(base, confidence="ambiguous", candidates=cands, resolved=False, why=why,
                            chapter=ch, verses=verses))
        return None if conf is None else osis_book
    if osis_book in SINGLE_CHAPTER and not verses:
        ch, verses = 1, [ch]
    if not verses:
        out.append(dict(base, osis_chapter=f"{osis_book}.{ch}", confidence=conf, resolved=True, why=why))
        return osis_book
    if osis_book == "EpJer":
        osis_book, ch = "Bar", 6          # the KJV prints the Epistle of Jeremy as Baruch 6
    if osis_book == "PrMan":               # every verse is part of the KJV's one paragraph
        out.append(dict(base, osis="PrMan.1.1", confidence=conf, resolved=True, why=why, mapped="part"))
        return osis_book
    for i, v in enumerate(verses):
        if osis_book == "Ps":
            kjvs, rel = _psalm(profile, ch, v)
        else:
            kjvs, rel = [f"{osis_book}.{ch}.{v}"], "same"
        for k in kjvs:
            b, c, vv = k.split(".")
            if not verse_exists(b, int(c), int(vv)):
                continue
            d = dict(base, osis=k, confidence=conf, resolved=True, why=why)
            if len(verses) > 1:
                d["range"] = True
            if rel not in ("same", None):
                d["mapped"] = rel
            out.append(d)
    return osis_book


# ---------------------------------------------------------------- the library-wide harvest
HARVEST_VERSION = 2
# Which books cite the Vulgate/Douay way. A Puritan cites the KJV way; the
# Dominican Fathers' Summa cites "Ps. 22" meaning KJV Ps 23 and "3 Kings".
PROFILE_BY_SLUG = (("aquinas", "douay"),)
# Books never harvested: lexicons (their references come parsed from the
# source), the Bible itself, and CCEL ThML, whose scripRef tags are the
# publisher's own answer key (measured against, never overwritten).
SKIP_FORMATS = {"thml", "lexicon-tsv", "lexicon-xml", "lexicon-ocr", "lexicon-tsv-subset",
                "perseus-lexicon-tei", "abbott-smith-tei", "gutenberg-txt:kjv"}
SKIP_SLUGS = {"kjv", "kjv-apocrypha"}


def profile_for(slug):
    return next((p for pre, p in PROFILE_BY_SLUG if slug.startswith(pre)), "protestant")


def harvest_book(book):
    """Find every scripture citation in a built book, IN PLACE: each unit's
    links[] gains one dict per verse cited (osis, raw, start/end in the
    unit's text, convention, confidence). Idempotent (a harvested book of
    this version is left alone); records its counts in scheme.scripture.
    Returns the counts, or None when the book is not one to harvest."""
    fmt = (book.get("source") or {}).get("format", "")
    if fmt in SKIP_FORMATS or book.get("slug") in SKIP_SLUGS:
        return None
    done = (book.get("scheme") or {}).get("scripture", {})
    if done.get("harvest") == HARVEST_VERSION:
        return done
    prof = profile_for(book.get("slug", ""))
    from collections import Counter
    c = Counter()
    for u in book["units"]:
        links = [l for l in u.get("links", []) if not (isinstance(l, dict) and l.get("harvest"))]
        for d in find(u.get("text", ""), prof):
            d["harvest"] = HARVEST_VERSION
            links.append(d)
            c[d["confidence"]] += 1
            c["verse links" if d.get("osis") else "other"] += 1
        u["links"] = links
    stats = {"harvest": HARVEST_VERSION, "profile": prof, **dict(sorted(c.items()))}
    book.setdefault("scheme", {})["scripture"] = stats
    return stats


def survey(books_dir, export=None):
    """Every built book: what the harvest found, and -- on the CCEL books,
    whose scripRef tags are the publisher's own answer key -- how the
    resolver does against them (it never writes to those books)."""
    import glob, json
    from collections import Counter
    tot, key = Counter(), Counter()
    rows = []
    for p in sorted(glob.glob(os.path.join(books_dir, "*.json"))):
        if p.endswith("manifest.json"):
            continue
        try:
            book = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(book, dict) or "units" not in book:
            continue
        fmt = (book.get("source") or {}).get("format", "")
        if fmt == "thml":
            for u in book["units"]:
                truth = {l for l in u.get("links", []) if isinstance(l, str)}
                ours = {d["osis"] for d in find(u.get("text", ""), profile_for(book["slug"])) if d.get("osis")}
                key["publisher's refs"] += len(truth)
                key["ours"] += len(ours)
                key["both"] += len(truth & ours)
            continue
        st = harvest_book(json.loads(json.dumps(book)))
        if not st:
            continue
        tot.update({k: v for k, v in st.items() if isinstance(v, int) and k != "harvest"})
        rows.append((book["slug"], st.get("verse links", 0), st.get("ambiguous", 0), st.get("not-a-verse", 0)))
        if export:
            for u in book["units"]:
                for d in find(u.get("text", ""), profile_for(book["slug"])):
                    export.write("\t".join([u["id"], d.get("osis", ""), d["confidence"], d["convention"],
                                              d["raw"].replace("\t", " ")]) + "\n")
    return tot, key, rows


def main():
    """python3 pipeline/scripture_refs.py "text ..." [--profile douay]
       python3 pipeline/scripture_refs.py --survey [data/books] [--export citations.tsv]"""
    if "--survey" in sys.argv:
        d = next((a for a in sys.argv[sys.argv.index("--survey") + 1:] if not a.startswith("--")),
                 os.path.join(HERE, "..", "data", "books"))
        ex = open(sys.argv[sys.argv.index("--export") + 1], "w", encoding="utf-8") if "--export" in sys.argv else None
        if ex:
            ex.write("unit_id\tosis\tconfidence\tconvention\traw\n")
        tot, key, rows = survey(d, ex)
        for slug, n, amb, nav in sorted(rows, key=lambda r: -r[1]):
            print(f"  {slug:<40} {n:>7,} verse links  {amb:>4} ambiguous  {nav:>4} not-a-verse")
        print("TOTAL", dict(tot))
        if key["publisher's refs"]:
            print(f"CCEL answer key: {key['publisher' + chr(39) + 's refs']:,} tagged refs; the resolver finds "
                  f"{key['both']:,} of them ({key['both'] / key['publisher' + chr(39) + 's refs']:.1%}) "
                  f"and {key['ours'] - key['both']:,} it does not tag")
        return
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prof = sys.argv[sys.argv.index("--profile") + 1] if "--profile" in sys.argv else "protestant"
    if prof in args:
        args.remove(prof)
    import json
    for link in find(" ".join(args), prof):
        print(json.dumps(link, ensure_ascii=False))


if __name__ == "__main__":
    main()
