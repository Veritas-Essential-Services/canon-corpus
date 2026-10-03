#!/usr/bin/env python3
"""
tsk_read.py -- read the Treasury of Scripture Knowledge out of a scan's OCR.

The Treasury (Bagster, c. 1830s; the Revell/Bagster printings with R. A.
Torrey's introduction) prints, verse by verse through the whole Bible, a
catchword from the verse and the places that bear on it:

    1 beginning. Pr. 8. 22-24; 16.4. Mar. 13. 19. Jno. 1. 1-3. ...
    2 without. Job 26.7. Is. 45.18. ...

This module turns one scan's OCR, already laid out in columns and lines
(tsk_layout.py), into entries: (KJV verse, catchword, references). Nothing
here decides between two scans or corrects a digit; that is build_xrefs.py's
job. Every reference keeps the text it was read from.

THE READING, in order (each a rule a test pins):
  1. Book and chapter come from the sequence, not from headings alone.
     The Treasury runs Genesis to Revelation in KJV order; a chapter heading
     ("CHAP. XII.", "PSALM XXIII.") whose numeral is the next chapter starts
     it; an entry numbered 1 after the heading was lost starts it too.
  2. An entry is a line opening with a verse number and then a word or a
     book abbreviation. Its number must be AFTER the last entry's and inside
     the chapter's KJV verse count; else the line is a continuation (e.g.
     "1 Ki. 4. 33." inside verse 20's entry). Small skips are normal: the
     Treasury has no entry for some verses.
  3. References: a book abbreviation, "ch." (this book) or "ver." (this
     chapter), then chapter.verse, verse lists with commas, ranges with a
     dash, further chapters after a semicolon. A word ends the run; the words
     before the first reference of a run are its catchword.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# (OSIS, the Treasury's own abbreviations, then forms the OCR makes of them).
# A form listed under two books is ambiguous and is resolved later by which
# reading names a verse that exists.
BOOKS = [
    ("Gen", "Ge Gen Go"), ("Exod", "Ex Hx Bx Wx Hix Ix Tix"), ("Lev", "Le Lev"),
    ("Num", "Nu Num"), ("Deut", "De Deu Do"), ("Josh", "Jos Jo"),
    ("Judg", "Ju Jud Tu Iu"), ("Ruth", "Ru"), ("1Sam", "1Sa"), ("2Sam", "2Sa"),
    ("1Kgs", "1Ki"), ("2Kgs", "2Ki"), ("1Chr", "1Ch 1Oh"), ("2Chr", "2Ch 2Oh"),
    ("Ezra", "Ezr Hzr Ezy Ear Bzr"), ("Neh", "Ne"), ("Esth", "Es Hs Bs Est"),
    ("Job", "Job"), ("Ps", "Ps Pa Pg Psa"), ("Prov", "Pr Py Pro"),
    ("Eccl", "Ec Ee Eo Bc Ecc"), ("Song", "Ca Can So"), ("Isa", "Is Ts Ig Isa"),
    ("Jer", "Je Jer Jo"), ("Lam", "La Lam"),
    ("Ezek", "Eze Hze Bze Hize Exe Haze Tze Wize Ez"), ("Dan", "Da Dan"),
    ("Hos", "Ho Hos"), ("Joel", "Joel Joe"), ("Amos", "Am"), ("Obad", "Ob Obad"),
    ("Jonah", "Jon"), ("Mic", "Mi Mic"), ("Nah", "Na Nah"), ("Hab", "Hab"),
    ("Zeph", "Zep"), ("Hag", "Hag"), ("Zech", "Zec Zee Zeo Zech"), ("Mal", "Mal"),
    ("Matt", "Mat Mt"), ("Mark", "Mar Har Mk"), ("Luke", "Lu Ln Liu Lm Lk"),
    ("John", "Jno Ino Jn"), ("Acts", "Ac Ao Ae Act"), ("Rom", "Ro Bo Ko Rom"),
    ("1Cor", "1Co 1Oo 1Go"), ("2Cor", "2Co 2Oo 2Go"), ("Gal", "Ga Gal"),
    ("Eph", "Ep Hp Bp Eph"), ("Phil", "Phi Php"), ("Col", "Col Gol Co"),
    ("1Thess", "1Th"), ("2Thess", "2Th"), ("1Tim", "1Ti"), ("2Tim", "2Ti"),
    ("Titus", "Tit"), ("Phlm", "Phile Phm Philem"), ("Heb", "He Heb"),
    ("Jas", "Ja Jas"), ("1Pet", "1Pe 1Po"), ("2Pet", "2Pe 2Po"),
    ("1John", "1Jno 1Ino 1Jn"), ("2John", "2Jno 2Ino 2Jn"), ("3John", "3Jno 3Ino 3Jn"),
    ("Jude", "Jude"), ("Rev", "Re Ke Rev"),
]
ORDER = [b for b, _ in BOOKS]
ABBREV = {}
for _osis, _forms in BOOKS:
    for _f in _forms.split():
        ABBREV.setdefault(_f, []).append(_osis)
SINGLE_CHAPTER = {"Obad", "Phlm", "2John", "3John", "Jude"}
# Heb. followed by a word is "Hebrew" (a marginal reading), not Hebrews: the
# reader only takes an abbreviation as a book when a number follows it.

def kjv_shape(path=None):
    """{book: {chapter: verse count}} from the committed KJV unit ids."""
    path = path or os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")
    with open(path, encoding="utf-8") as f:
        uids = json.load(f)["uids"]
    shape = {b: {} for b in ORDER}
    for k in uids:
        if k.startswith("kjv:"):
            b, c, v = k[4:].split(".")
            c, v = int(c), int(v)
            if v > shape[b].get(c, 0):
                shape[b][c] = v
    return shape


# ---------------------------------------------------------------- numerals
_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
_ROMAN_OCR = str.maketrans({"l": "I", "1": "I", "|": "I", "Y": "V", "y": "V",
                            "v": "V", "x": "X", "i": "I", "c": "C", "T": "I"})


def roman(s):
    s = s.translate(_ROMAN_OCR).upper()
    s = re.sub(r"[^IVXLC]", "", s)
    if not s:
        return None
    total = 0
    for i, ch in enumerate(s):
        v = _ROMAN[ch]
        nxt = _ROMAN[s[i + 1]] if i + 1 < len(s) else 0
        total += -v if v < nxt else v
    return total if total > 0 else None


# ---------------------------------------------------------------- tokens
_CLEAN = re.compile(r"[^A-Za-z0-9.,;:\- ]")
_DATE = re.compile(r"\b(?:A|a)\.?\s?(?:M|m)\.?\s*(?:cir\.\s*)?\d{1,4}\.?"
                   r"|\b(?:B|b)\.\s?(?:C|c|O|o|0)\.?\s*(?:cir\.\s*)?\d{1,4}\.?"
                   r"|\b(?:A|a)\.\s?(?:D|d)\.?\s*\d{1,4}\.?")
_TOK = re.compile(r"""
    (?P<book>(?:\b[123]\s?)?\b[A-Z][a-z]{0,5})[.,]?\s?(?=\d)   # abbreviation, a number follows
  | (?P<ch>\bch)[.,]\s?(?=\d)
  | (?P<ver>\b(?:ver|v|vs))[.,]\s?(?=\d)
  | (?P<num>\d{1,3})
  | (?P<sep>[.,;:\-])
  | (?P<word>[A-Za-z]+)
""", re.X)


def _blank(m):
    return " " * len(m.group(0))


def tokens(text):
    """[(kind, value, (start, end))]. Cleaning blanks characters in place, so a
    span indexes the text as read (and the glyphs under it)."""
    text = _DATE.sub(_blank, _CLEAN.sub(" ", text))
    out = []
    for m in _TOK.finditer(text):
        k = m.lastgroup
        v = m.group(k)
        span = m.span(k)
        if k == "book":
            key = re.sub(r"\s", "", v)
            # an unknown capitalised word before a number is kept as a
            # "badbook": its reference is read but has no book (counted)
            out.append(("book" if key in ABBREV else "badbook", key, span))
        else:
            out.append((k, v, span))
    return out


def refs(text, book=None, chapter=None):
    """[(catchword, [ref, ...])] from one entry's text. A ref is a dict:
    {"abbr": the abbreviation as read, or "ch"/"ver";
     "c": chapter (None for "ver": the entry's), "v": verse (None: the whole chapter),
     "c2", "v2": a range's end (None if none),
     "at": {"c"|"v"|"c2"|"v2": (start, end) of that number in `text`}}.
    Books are not resolved here."""
    toks = tokens(text)
    runs = []
    kw = []
    i = 0
    n = len(toks)

    def num_at(j):
        return j < n and toks[j][0] == "num"

    def sep_at(j, s):
        return j < n and toks[j][0] == "sep" and toks[j][1] in s

    while i < n:
        k, v, _ = toks[i]
        if k in ("book", "ch", "ver", "badbook"):
            if not runs or kw:
                runs.append([" ".join(kw).strip(), []])
                kw = []
            abbr = v if k in ("book", "badbook") else k
            i += 1
            c, c_at = None, None
            group = []
            expect_chapter = k != "ver"
            if k == "book" and set(ABBREV[v]) <= SINGLE_CHAPTER:
                # Ob. 3, Jude 14, 15: a one-chapter book is cited by verse
                c, expect_chapter = 1, False
            while num_at(i):
                a, a_at = int(toks[i][1]), toks[i][2]
                i += 1
                if expect_chapter:
                    # chapter, then "." (or the OCR's "," or ":") and a verse
                    if sep_at(i, ".,:") and num_at(i + 1):
                        c, c_at = a, a_at
                        group.append({"abbr": abbr, "c": c, "v": int(toks[i + 1][1]), "c2": None,
                                      "v2": None, "at": {"c": c_at, "v": toks[i + 1][2]}})
                        i += 2
                    else:
                        c, c_at = a, a_at
                        group.append({"abbr": abbr, "c": c, "v": None, "c2": None, "v2": None,
                                      "at": {"c": c_at}})
                    expect_chapter = False
                else:
                    r = {"abbr": abbr, "c": c, "v": a, "c2": None, "v2": None, "at": {"v": a_at}}
                    if c == 1 and c_at is None and k == "book":
                        r["one_chapter"] = True
                    if c_at:
                        r["at"]["c"] = c_at
                    group.append(r)
                if sep_at(i, "-") and num_at(i + 1):
                    b, b_at = int(toks[i + 1][1]), toks[i + 1][2]
                    i += 2
                    last = group[-1]
                    if sep_at(i, ".:") and num_at(i + 1) and last["v"] is not None:
                        # across chapters: c.v-c2.v2
                        last["c2"], last["v2"] = b, int(toks[i + 1][1])
                        last["at"]["c2"], last["at"]["v2"] = b_at, toks[i + 1][2]
                        c, c_at = b, b_at
                        i += 2
                    elif last["v"] is None:
                        last["c2"] = b               # chapters a-b
                        last["at"]["c2"] = b_at
                    else:
                        last["v2"] = b
                        last["at"]["v2"] = b_at
                if sep_at(i, ","):
                    i += 1
                    continue
                if sep_at(i, ";"):
                    i += 1
                    expect_chapter = k != "ver" and not (k == "book" and set(ABBREV[v]) <= SINGLE_CHAPTER)
                    continue
                break
            if k == "badbook":
                for r in group:
                    r["bad"] = True
            runs[-1][1].extend(group)
        elif k == "word":
            kw.append(v)
            i += 1
        else:
            i += 1
    return [(c, rs) for c, rs in runs if rs]


# ---------------------------------------------------------------- running heads
HEAD_BOOKS = [
    ("GENESIS", "Gen"), ("EXODUS", "Exod"), ("LEVITICUS", "Lev"), ("NUMBERS", "Num"),
    ("DEUTERONOMY", "Deut"), ("JOSHUA", "Josh"), ("JUDGES", "Judg"), ("RUTH", "Ruth"),
    ("1SAMUEL", "1Sam"), ("2SAMUEL", "2Sam"), ("1KINGS", "1Kgs"), ("2KINGS", "2Kgs"),
    ("1CHRONICLES", "1Chr"), ("2CHRONICLES", "2Chr"), ("EZRA", "Ezra"),
    ("NEHEMIAH", "Neh"), ("ESTHER", "Esth"), ("JOB", "Job"), ("PSALMS", "Ps"),
    ("PSALM", "Ps"), ("PROVERBS", "Prov"), ("ECCLESIASTES", "Eccl"),
    ("SOLOMONSSONG", "Song"), ("ISAIAH", "Isa"), ("JEREMIAH", "Jer"),
    ("LAMENTATIONS", "Lam"), ("EZEKIEL", "Ezek"), ("DANIEL", "Dan"), ("HOSEA", "Hos"),
    ("JOEL", "Joel"), ("AMOS", "Amos"), ("OBADIAH", "Obad"), ("JONAH", "Jonah"),
    ("MICAH", "Mic"), ("NAHUM", "Nah"), ("HABAKKUK", "Hab"), ("ZEPHANIAH", "Zeph"),
    ("HAGGAI", "Hag"), ("ZECHARIAH", "Zech"), ("MALACHI", "Mal"), ("MATTHEW", "Matt"),
    ("MARK", "Mark"), ("LUKE", "Luke"), ("JOHN", "John"), ("THEACTS", "Acts"),
    ("ACTS", "Acts"), ("ROMANS", "Rom"), ("1CORINTHIANS", "1Cor"),
    ("2CORINTHIANS", "2Cor"), ("GALATIANS", "Gal"), ("EPHESIANS", "Eph"),
    ("PHILIPPIANS", "Phil"), ("COLOSSIANS", "Col"), ("1THESSALONIANS", "1Thess"),
    ("2THESSALONIANS", "2Thess"), ("1TIMOTHY", "1Tim"), ("2TIMOTHY", "2Tim"),
    ("TITUS", "Titus"), ("PHILEMON", "Phlm"), ("HEBREWS", "Heb"), ("JAMES", "Jas"),
    ("1PETER", "1Pet"), ("2PETER", "2Pet"), ("1JOHN", "1John"), ("2JOHN", "2John"),
    ("3JOHN", "3John"), ("JUDE", "Jude"), ("REVELATION", "Rev"),
]


def _similar(a, b):
    import difflib
    return difflib.SequenceMatcher(None, a, b).ratio()


def parse_head(text):
    """A running head ("B.C. 1913. GENESIS, XVII. A.M. 2091.") -> (book, chapter) or None.
    The book name is matched loosely (the OCR misspells: 2SAMURL, ISATAH); the
    numeral after it is read as a Roman number (the first, for PSALMS, XVI-XVIII)."""
    m = re.search(r"((?:[123I]\s?)?(?:THE\s+)?(?:SOLOMON.?S\s+)?[A-Z]{3,}[A-Z\s]*?)[,.]?\s+([IVXLCYlTx|\s]{1,10})\b", text)
    if not m:
        return None
    name = re.sub(r"[^A-Z0-9]", "", m.group(1).replace("I ", "1").replace("I", "1", 1)
                  if re.match(r"I\s?[A-Z]", m.group(1)) else re.sub(r"[^A-Z0-9]", "", m.group(1)))
    best, score = None, 0.0
    for full, osis in HEAD_BOOKS:
        r = _similar(name, full)
        if r > score:
            best, score = osis, r
    if score < 0.8:
        return None
    num = roman(m.group(2).replace(" ", ""))
    return (best, num) if num else None


# ---------------------------------------------------------------- the alignment
# Line kinds the reader takes as evidence: an ENTRY (a verse number opening a
# line), a HEADING (CHAP./PSALM and a numeral). Everything else is text that
# belongs to the entry above it (or to a chapter's summary, which is dropped).
_HEAD = re.compile(r"^\W*(?:C\s?[HN]\s?A\s?P|OHAP|CHAF|GHAP|CRAP|CIIAP|CHAD)\W+([IVXLCilYTvx1|]+)\b")
_PSALM = re.compile(r"^\W*P\s?[SB8]\s?A\s?L\s?M\W+([IVXLCilYTvx1|]+)\b")
_ENTRY = re.compile(r"^[^\w]{0,6}(\d{1,3})[^\w\s.,;:]{0,2}\s+(?=[A-Za-z])")

# Digits this face's OCR confuses (measured on the scans, README-xrefs.md):
# the old-style 3 read as 8 above all, then 2/9, 1/4/7 and 5/6.
CONFUSE = {"8": "3", "3": "8", "4": "1", "1": "47", "7": "1", "9": "2", "2": "9", "6": "5", "5": "6"}

# Scores (README-xrefs.md s.2). A verse number read as printed outweighs one
# reached through a confused digit; every verse the alignment passes over
# without an entry costs a little (the Treasury skips few verses).
S_EXACT, S_ALT, S_NUMBERED, S_HEAD, P_SKIP = 4.0, 2.5, 1.0, 3.0, 0.35
# A step of more than NEAR_VERSES from one chosen line to the next is a jump,
# and costs P_JUMP besides: it is what keeps a chain in one place when the
# numbers alone would fit anywhere.
NEAR_VERSES, P_JUMP = 40, 8.0


def digit_alternatives(s):
    """Every other number reachable by swapping confusable digits."""
    out = {""}
    for ch in s:
        nxt = set()
        for o in out:
            nxt.add(o + ch)
            for alt in CONFUSE.get(ch, ""):
                nxt.add(o + alt)
        out = nxt
    return tuple(sorted({int(o) for o in out if o and int(o) != int(s)}))


def _numbered_book_follows(rest):
    m = re.match(r"\s*([A-Z][a-z]{0,4})[.,]?\s?\d", rest)
    return bool(m) and m.group(1) in {"Sa", "Ki", "Ch", "Co", "Th", "Ti", "Pe", "Jno", "Oh", "Oo", "Go"}


class Verses:
    """The KJV verse sequence; slot 2k is verse k, slot 2k-1 the start of its
    chapter (only for verse 1), so a heading sits just before its first verse."""

    def __init__(self, shape):
        self.seq = []
        self.index = {}
        for b in ORDER:
            for c in sorted(shape[b]):
                for v in range(1, shape[b][c] + 1):
                    self.index[(b, c, v)] = len(self.seq)
                    self.seq.append((b, c, v))
        self.shape = shape
        self.chapters = [(b, c) for b in ORDER for c in sorted(shape[b])]
        self.chap_index = {bc: i for i, bc in enumerate(self.chapters)}


class _MaxTree:
    """Range maximum over slots, with the argument (a segment tree)."""

    def __init__(self, n):
        size = 1
        while size < n:
            size *= 2
        self.size = size
        self.t = [(-1e18, None)] * (2 * size)

    def update(self, i, val):
        i += self.size
        if val[0] <= self.t[i][0]:
            return
        self.t[i] = val
        i //= 2
        while i:
            a, b = self.t[2 * i], self.t[2 * i + 1]
            self.t[i] = a if a[0] >= b[0] else b
            i //= 2

    def query(self, lo, hi):
        """max over slots lo <= s < hi"""
        best = (-1e18, None)
        lo += self.size
        hi += self.size
        while lo < hi:
            if lo & 1:
                if self.t[lo][0] > best[0]:
                    best = self.t[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                if self.t[hi][0] > best[0]:
                    best = self.t[hi]
            lo //= 2
            hi //= 2
        return best


def page_windows(heads, verses, npages):
    """For each page, the chapters its entries may belong to: from the page
    head before it (less three chapters) to the page head after it (plus
    one). Heads out of order (an OCR misreading of the name or numeral) are
    dropped first: the longest increasing run of heads is kept."""
    pts = [(p, verses.chap_index[(b, c)]) for p, (b, c) in sorted(heads.items())
           if (b, c) in verses.chap_index]
    # longest non-decreasing subsequence on chapter index
    import bisect
    tails, tails_i, prev = [], [], [None] * len(pts)
    for i, (_, ci) in enumerate(pts):
        j = bisect.bisect_right(tails, ci)
        if j == len(tails):
            tails.append(ci)
            tails_i.append(i)
        else:
            tails[j] = ci
            tails_i[j] = i
        prev[i] = tails_i[j - 1] if j else None
    keep = []
    k = tails_i[-1] if tails_i else None
    while k is not None:
        keep.append(pts[k])
        k = prev[k]
    keep.reverse()
    kept = dict(keep)
    out = {}
    pages = sorted(kept)
    last = len(verses.chapters) - 1
    for p in range(npages):
        before = [q for q in pages if q <= p]
        after = [q for q in pages if q >= p]
        lo = kept[before[-1]] - 3 if before else 0
        hi = kept[after[0]] + 1 if after else last
        out[p] = (max(0, lo), min(last, hi))
    return out, kept


def align(lines, shape, heads=None, npages=None):
    """lines: [(text, where, ...)], where[0] the page. Returns (entries, log);
    an entry is {"verse": (book, chapter, verse), "rule": "read"|"digit",
    "read": the number as printed, "lines": the line indices it spans,
    "start": where its text begins in its first line, "where": the lines' places}.

    A global alignment, not a walk: every line that could open an entry or a
    chapter is offered the verses its number (or a confused reading of it)
    could be, inside its page's window; the chain through the KJV order with
    the best score is the reading. A misread number then costs one entry, not
    the sync of every entry after it."""
    V = Verses(shape)
    windows = None
    if heads:
        windows, _ = page_windows(heads, V, (npages or max(x[1][0] for x in lines) + 1))
    nslots = 2 * len(V.seq) + 2
    tree = _MaxTree(nslots)
    tree.update(0, (0.0, None))          # the start
    nodes = []                           # (line index, slot, score, back node, kind, rule)
    for li, (text, where, *_) in enumerate(lines):
        t = text.strip()
        opts = []
        lo_c, hi_c = (windows[where[0]] if windows else (0, len(V.chapters) - 1))
        m = _HEAD.match(t) or _PSALM.match(t)
        if m:
            num = roman(m.group(1))
            if num:
                for ci in range(lo_c, hi_c + 1):
                    b, c = V.chapters[ci]
                    if c == num:
                        opts.append((2 * V.index[(b, c, 1)] + 1, S_HEAD, "heading", "heading"))
        m = _ENTRY.match(t)
        if m:
            n = int(m.group(1))
            alts = digit_alternatives(m.group(1))
            numbered = n <= 3 and _numbered_book_follows(t[m.end():])
            for ci in range(lo_c, hi_c + 1):
                b, c = V.chapters[ci]
                mv = shape[b][c]
                for a in (n,) + alts:
                    if 1 <= a <= mv:
                        sc = S_EXACT if a == n else S_ALT
                        if numbered:
                            sc = S_NUMBERED
                        opts.append((2 * V.index[(b, c, a)] + 2, sc, "entry",
                                     "read" if a == n else "digit"))
        if not opts:
            continue
        new = []
        for slot, sc, kind, rule in opts:
            w = max(0, slot - 2 * NEAR_VERSES)
            best = tree.query(w, slot)       # best chain ending shortly before this slot
            far = tree.query(0, w)
            if far[0] - P_JUMP > best[0]:
                best = (far[0] - P_JUMP, far[1])
            if best[0] < -1e17:
                continue
            # stored values carry +P_SKIP*position, so the verses skipped
            # between predecessor and this slot cost P_SKIP each
            score = best[0] + sc - P_SKIP * (slot // 2 - 1)
            new.append((li, slot, score, best[1], kind, rule))
        for nd in new:
            nodes.append(nd)
            # stored value is offset so later queries can apply the skip penalty
            tree.update(nd[1], (nd[2] + P_SKIP * (nd[1] // 2), len(nodes) - 1))
    if not nodes:
        return [], {}
    end = max(range(len(nodes)), key=lambda i: nodes[i][2] - P_SKIP * (len(V.seq) - nodes[i][1] // 2))
    chain = []
    k = end
    while k is not None:
        chain.append(nodes[k])
        k = nodes[k][3]
    chain.reverse()
    # entries: an entry node's text runs to the next chosen node's line
    entries = []
    log = {"entries": 0, "headings": 0, "by_rule": {}}
    for i, nd in enumerate(chain):
        li, slot, score, back, kind, rule = nd
        if kind == "heading":
            log["headings"] += 1
            continue
        end_li = chain[i + 1][0] if i + 1 < len(chain) else len(lines)
        b, c, v = V.seq[slot // 2 - 1]
        first = lines[li][0]
        lead = len(first) - len(first.lstrip())
        m = _ENTRY.match(first.strip())
        entries.append({"verse": (b, c, v), "rule": rule, "read": m.group(1),
                        "lines": list(range(li, end_li)), "start": lead + m.end(),
                        "where": [lines[j][1] for j in range(li, end_li)]})
        log["by_rule"][rule] = log["by_rule"].get(rule, 0) + 1
    log["entries"] = len(entries)
    return entries, log


def join_lines(lines, glyphs=None):
    """Entry lines -> one string (and, given each line's glyph list, the glyph
    under every character of it; None under a space). A word broken at a
    line's end by a hyphen is joined."""
    out, og = "", []
    for i, t in enumerate(lines):
        g = list(glyphs[i]) if glyphs else [None] * len(t)
        if out.endswith("-") and t[:1].islower():
            out, og = out[:-1] + t, og[:-1] + g
        elif out:
            out, og = out + " " + t, og + [None] + g
        else:
            out, og = t, g
    return (out, og) if glyphs else out


def entry_text(lines, entry):
    """An aligned entry's text, and the glyph under each character of it."""
    ts, gs = [], []
    for k, j in enumerate(entry["lines"]):
        t, _, g = lines[j]
        if k == 0:
            t, g = t[entry["start"]:], g[entry["start"]:]
        lead = len(t) - len(t.lstrip())
        t = t.strip()
        ts.append(t)
        gs.append(g[lead:lead + len(t)])
    return join_lines(ts, gs)


def resolve(r, book, chapter, shape):
    """A read reference -> the KJV verse ranges it can name: [(book, c, v, c2, v2)].
    "ver." is the entry's chapter, "ch." the entry's book; an abbreviation the
    OCR makes of two books gives one candidate per book that has the verse.
    A whole chapter is its first to last verse; a range that runs backwards
    or past the chapter keeps only its first verse. Empty: no such verse."""
    if r.get("bad"):
        return []
    if r["abbr"] == "ver":
        cands = [(book, chapter)]
    elif r["abbr"] == "ch":
        cands = [(book, r["c"])]
    else:
        cands = [(b, r["c"]) for b in ABBREV.get(r["abbr"], [])]
    out = []
    for b, c in cands:
        if c is None or c not in shape[b]:
            continue
        if r["v"] is None:
            c2 = r["c2"] or c
            if c2 in shape[b] and c2 >= c:
                out.append((b, c, 1, c2, shape[b][c2]))
            continue
        if not 1 <= r["v"] <= shape[b][c]:
            continue
        if r["c2"]:
            if r["c2"] in shape[b] and r["c2"] > c and 1 <= (r["v2"] or 0) <= shape[b][r["c2"]]:
                out.append((b, c, r["v"], r["c2"], r["v2"]))
            continue
        v2 = r["v2"] or r["v"]
        if v2 < r["v"] or v2 > shape[b][c]:
            v2 = r["v"]
        out.append((b, c, r["v"], c, v2))
    return out


def ref_id(t):
    """(book, c, v, c2, v2) -> "kjv:Book.c.v", "kjv:Book.c.v-v2" or "kjv:Book.c.v-c2.v2"."""
    b, c, v, c2, v2 = t
    if (c2, v2) == (c, v):
        return f"kjv:{b}.{c}.{v}"
    if c2 == c:
        return f"kjv:{b}.{c}.{v}-{v2}"
    return f"kjv:{b}.{c}.{v}-{c2}.{v2}"


def parse_ref_id(s):
    """The inverse of ref_id."""
    b, rest = s[4:].split(".", 1)
    if "-" not in rest:
        c, v = map(int, rest.split("."))
        return (b, c, v, c, v)
    a, z = rest.split("-")
    c, v = map(int, a.split("."))
    if "." in z:
        c2, v2 = map(int, z.split("."))
    else:
        c2, v2 = c, int(z)
    return (b, c, v, c2, v2)
