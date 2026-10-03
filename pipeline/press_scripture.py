#!/usr/bin/env python3
"""press_scripture.py -- printed scripture references -> KJV verse ids.

The Press (pipeline/press_build.py) tags every scripture reference in a
polished book with the KJV unit id the rest of the suite already uses
(`kjv:Rom.8.13`, OSIS book names). This module is the one place that reads a
reference AS PRINTED in a 17th-19th century book and decides what it points at.

    parse("Rom. viii. 13")        -> ["Rom.8.13"]
    parse("Ps. cxix. 5, 6")       -> ["Ps.119.5", "Ps.119.6"]
    parse("1 John iii. 2")        -> ["1John.3.2"]
    parse("Gal. v. 17-19")        -> ["Gal.5.17", "Gal.5.18", "Gal.5.19"]
    parse("Heb. xii.")            -> ["Heb.12"]          (chapter only)

Every id is checked against the KJV versification table
(press_kjv_versification.json, 66 books / 31,102 verses, built from
pythonbible's KJV counts). A reference that names a verse the KJV does not have
is NOT silently clamped: `parse` drops it and `parse_report` says why, so the
QA report can list it (rule 4: never pretend precision).

Roman-numeral chapters are the norm in Goold's Owen and the Nichol series; the
old printers' "j" for a final "i" (xiij) is accepted.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
VERSES = json.load(open(os.path.join(HERE, "press_kjv_versification.json")))

# printed abbreviation (lowercase, no dots/spaces) -> OSIS
_NAMES = {
    "Gen": "gen genesis ge gn", "Exod": "exod exodus ex exo", "Lev": "lev leviticus le lv",
    "Num": "num numbers nu nb numb", "Deut": "deut deuteronomy de dt deu",
    "Josh": "josh joshua jos", "Judg": "judg judges jud jdg", "Ruth": "ruth ru",
    "1Sam": "1sam 1samuel 1sa isam isamuel", "2Sam": "2sam 2samuel 2sa iisam iisamuel",
    "1Kgs": "1kgs 1kings 1ki 1kin ikings ikin", "2Kgs": "2kgs 2kings 2ki 2kin iikings iikin",
    "1Chr": "1chr 1chron 1chronicles 1ch ichron", "2Chr": "2chr 2chron 2chronicles 2ch iichron",
    "Ezra": "ezra ezr", "Neh": "neh nehemiah ne", "Esth": "esth esther est",
    "Job": "job jb", "Ps": "ps psa psal psalm psalms pss", "Prov": "prov proverbs pr pro prv",
    "Eccl": "eccl eccles ecclesiastes ec ecc eccle",
    "Song": "song cant canticles songofsolomon songofsongs sol ss",
    "Isa": "isa isaiah is esa", "Jer": "jer jeremiah je jerem", "Lam": "lam lamentations la",
    "Ezek": "ezek ezekiel eze ezk", "Dan": "dan daniel da dn", "Hos": "hos hosea ho",
    "Joel": "joel joe jl", "Amos": "amos am", "Obad": "obad obadiah ob", "Jonah": "jonah jon",
    "Mic": "mic micah mi", "Nah": "nah nahum na", "Hab": "hab habakkuk", "Zeph": "zeph zephaniah zep",
    "Hag": "hag haggai", "Zech": "zech zechariah zec", "Mal": "mal malachi",
    "Matt": "matt matthew mat mt", "Mark": "mark mar mk", "Luke": "luke luk lk",
    "John": "john joh jn", "Acts": "acts act ac", "Rom": "rom romans ro",
    "1Cor": "1cor 1corinthians 1co icor", "2Cor": "2cor 2corinthians 2co iicor",
    "Gal": "gal galatians ga", "Eph": "eph ephesians ephes ep", "Phil": "phil philippians php philip",
    "Col": "col colossians coloss", "1Thess": "1thess 1thessalonians 1th 1thes ithess",
    "2Thess": "2thess 2thessalonians 2th 2thes iithess", "1Tim": "1tim 1timothy 1ti itim",
    "2Tim": "2tim 2timothy 2ti iitim", "Titus": "titus tit", "Phlm": "phlm philemon philem phm",
    "Heb": "heb hebrews he", "Jas": "jas james jam", "1Pet": "1pet 1peter 1pe ipet",
    "2Pet": "2pet 2peter 2pe iipet", "1John": "1john 1jn 1joh ijohn", "2John": "2john 2jn 2joh iijohn",
    "3John": "3john 3jn 3joh iiijohn", "Jude": "jude jud", "Rev": "rev revelation revelations re apoc",
}
ABBR = {a: osis for osis, s in _NAMES.items() for a in s.split()}
# "jud" is Judges in most printers but Jude in some; Judges wins (it is far
# more common in these books); a Jude reference prints "Jude".
ABBR["jud"] = "Judg"

_ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100}

def roman(s):
    s = s.lower().replace("j", "i")
    if not s or any(ch not in _ROMAN for ch in s):
        return None
    tot = 0
    for i, ch in enumerate(s):
        v = _ROMAN[ch]
        tot += -v if i + 1 < len(s) and _ROMAN[s[i + 1]] > v else v
    return tot

def num(s):
    s = s.strip().rstrip(".")
    return int(s) if s.isdigit() else roman(s)

def book_of(s):
    k = re.sub(r"[\s.]", "", s.lower())
    for word, n in (("first", "1"), ("second", "2"), ("third", "3")):
        if k.startswith(word):
            k = n + k[len(word):]
    return ABBR.get(k)

def valid(osis, ch, vs=None):
    chs = VERSES.get(osis)
    if not chs or not 1 <= ch <= len(chs):
        return False
    return vs is None or 1 <= vs <= chs[ch - 1]

_NUM = r"(?:\d+|[ivxlcj]+)"
RE_REF = re.compile(
    r"^\s*(?P<book>(?:[1-3]|i{1,3})?\s*[A-Za-z][A-Za-z]*\.?)\s*"
    r"(?P<ch>" + _NUM + r")\s*[.:,]?\s*(?P<rest>.*)$", re.I)

def parse_report(printed, context_book=None):
    """(ids, problems). `printed` is one reference string as the book prints it."""
    ids, problems = [], []
    s = printed.replace("–", "-").replace("—", "-").strip().rstrip(";.")
    m = RE_REF.match(s)
    if not m:
        return [], [f"unparsed: {printed!r}"]
    osis = book_of(m.group("book"))
    if not osis:
        return [], [f"unknown book: {m.group('book')!r} in {printed!r}"]
    ch = num(m.group("ch"))
    if ch is None:
        return [], [f"bad chapter in {printed!r}"]
    rest = m.group("rest").strip().rstrip(".")
    if not rest:
        if valid(osis, ch):
            return [f"{osis}.{ch}"], []
        return [], [f"no such chapter: {osis} {ch} ({printed!r})"]
    for part in re.split(r"\s*[,;]\s*|\s+and\s+", rest):
        part = part.strip().rstrip(".")
        if not part:
            continue
        r = re.match(r"^(\d+)\s*(?:-\s*(\d+))?\s*(?:ff?|&c)?\.?$", part)
        if not r:
            # "13; xiv. 2" style: a new chapter inside the same book
            r2 = re.match(r"^(" + _NUM + r")\s*[.:]\s*(\d+)(?:\s*-\s*(\d+))?$", part, re.I)
            if r2 and num(r2.group(1)):
                ch = num(r2.group(1))
                lo, hi = int(r2.group(2)), int(r2.group(3) or r2.group(2))
            else:
                problems.append(f"unparsed part {part!r} in {printed!r}")
                continue
        else:
            lo, hi = int(r.group(1)), int(r.group(2) or r.group(1))
        if hi < lo or hi - lo > 60:
            problems.append(f"implausible range {lo}-{hi} in {printed!r}")
            continue
        for v in range(lo, hi + 1):
            if valid(osis, ch, v):
                ids.append(f"{osis}.{ch}.{v}")
            else:
                problems.append(f"no such verse in the KJV: {osis} {ch}:{v} ({printed!r})")
    return ids, problems

def parse(printed):
    return parse_report(printed)[0]

def check_osis(osis_ref):
    """Validate an osisRef CCEL already supplied ('Rom.8.13', 'Rom.8.13-Rom.8.15',
    space-separated lists). Returns (ids, problems)."""
    ids, problems = [], []
    for tok in osis_ref.split():
        a, _, b = tok.partition("-")
        pa, pb = a.split("."), (b.split(".") if b else None)
        try:
            if len(pa) == 2:
                ok = valid(pa[0], int(pa[1]))
                (ids if ok else problems).append(tok if ok else f"no such chapter: {tok}")
                continue
            bk, ch, v = pa[0], int(pa[1]), int(pa[2])
            if pb:
                ch2, v2 = (int(pb[1]), int(pb[2])) if len(pb) == 3 else (ch, int(pb[-1]))
                if ch2 != ch:
                    # cross-chapter range: keep its two ends, both checked
                    for c_, v_ in ((ch, v), (ch2, v2)):
                        (ids.append(f"{bk}.{c_}.{v_}") if valid(bk, c_, v_)
                         else problems.append(f"no such verse in the KJV: {bk} {c_}:{v_}"))
                    continue
                rng = range(v, v2 + 1)
            else:
                rng = [v]
            for vv in rng:
                if valid(bk, ch, vv):
                    ids.append(f"{bk}.{ch}.{vv}")
                else:
                    problems.append(f"no such verse in the KJV: {bk} {ch}:{vv}")
        except (ValueError, IndexError):
            problems.append(f"unparsed osisRef {tok!r}")
    return ids, problems

if __name__ == "__main__":
    import sys
    for a in sys.argv[1:]:
        print(a, "->", parse_report(a))

# ---------------------------------------------------------------- context
# "verse 13", "ver. 9", "chap. iv. 3": a reference that leans on the one
# before it. Resolved against the last reference in the same section and
# reported as INFERRED, so the index and the QA can tell them apart.
RE_VERSE_ONLY = re.compile(r"^\s*(?:verses?|vers?\.|vv?\.)\s*(?P<rest>\d.*)$", re.I)
RE_ORD_VERSE = re.compile(r"^\s*(?P<v>\d+)(?:st|nd|rd|th|d)\s+verse\b", re.I)
RE_CHAP_ONLY = re.compile(r"^\s*(?:chap(?:ter)?\.?|ch\.)\s*(?P<ch>" + _NUM + r")\s*[.:,]?\s*(?P<rest>.*)$", re.I)
RE_BOOK_CHAP = re.compile(r"^\s*(?P<book>(?:[1-3]|i{1,3})?\s*[A-Za-z]+\.?)\s*,?\s*(?:chap(?:ter)?\.?|ch\.)\s*(?P<tail>.*)$", re.I)

def parse_context(printed, ctx):
    """(ids, problems, inferred). ctx is {"book": osis, "ch": int} or None and
    is updated in place by every successful reference."""
    s = " ".join(printed.replace("–", "-").replace("—", "-").split()).rstrip(";.")
    m = RE_BOOK_CHAP.match(s)
    if m and book_of(m.group("book")):
        s = f"{m.group('book')} {m.group('tail')}"
    ids, probs = parse_report(s)
    if ids:
        p = ids[-1].split(".")
        if ctx is not None:
            ctx.update(book=p[0], ch=int(p[1]))
        return ids, [], False
    if ctx and ctx.get("book"):
        mv = RE_VERSE_ONLY.match(s)
        mo = RE_ORD_VERSE.match(s)
        mc = RE_CHAP_ONLY.match(s)
        alt = None
        if mv:
            alt = f"{ctx['book']} {ctx['ch']}. {mv.group('rest')}"
        elif mo:
            alt = f"{ctx['book']} {ctx['ch']}. {mo.group('v')}"
        elif mc:
            alt = f"{ctx['book']} {mc.group('ch')}. {mc.group('rest')}"
        if alt:
            ids2, probs2 = parse_report(alt)
            if ids2:
                p = ids2[-1].split(".")
                ctx.update(book=p[0], ch=int(p[1]))
                return ids2, [], True
            return [], probs2, True
    return [], probs, False
