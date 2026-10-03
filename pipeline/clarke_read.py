#!/usr/bin/env python3
"""
clarke_read.py -- Adam Clarke's Commentary read from the OCR of open
archive.org scans: where each note is, and what it cites.

Clarke is on no keyed site (CCEL has no Clarke). So both readings of every
note come from scans, from two printings of each Testament, and only what
both printings read is committed (build_commentary.build_scan_work).

THE PAGE. A page prints the KJV text with its marginal references and
chronology at the top and Clarke's notes below. The OCR (archive.org's
djvu text) runs them together in reading order, so a note's text is
interleaved with the Bible text, the margin and the running heads of the
page it crosses. Each chapter's notes open with a heading, "NOTES ON CHAP.
IV." (or "NOTES ON PSALM XXIII.", or in the 1835 New Testament "NOTES.--").

WHERE A NOTE IS (read_volume):
  1. The heads: "Verse 17. The priests--stood firm on dry ground]" (the
     1835 New Testament prints the bare number, "25. Judas--said, Master]").
     The verse number and the lemma, the words up to the "]".
  2. The chapter. The note headings cut the notes into runs, and a run is
     cut again where its verse numbers fall back to 1-3 (a heading the OCR
     lost). The runs are aligned in order to the volume's chapters by
     dynamic programming: a run scores, for a chapter, how far its lemmas'
     words are found in the KJV verses its heads name, plus a bonus when
     the heading's Roman numeral (read through its OCR confusions) names
     that chapter. Runs may be skipped (introductions, an OCR'd page of
     something else), chapters may be missed.
  3. A head is placed when at least two of its lemma's words are long
     enough to count (3+ letters) and at least half of them are in the KJV
     verse it names, in the chapter its run was aligned to.

WHAT A NOTE CITES (note_text, citations): the text from its head to the
next head, cut at the next chapter, in paragraphs (the OCR's blank lines).
A paragraph is dropped when it is
  - the chronology margin (A. M. 2553, An. Exod. Isr., Anno ante, Olymp.)
    or a page foot ("Vol. II. ( 2 )");
  - the Bible text: half of its word pairs are in the KJV of this chapter or
    the next;
  - the margin's references: letter-marked references ("b See Exod. xiv.
    29", "* Neh. xiii. 13"), "Or," and "Heb." glosses, or a paragraph that is
    mostly references with no run of prose.
The head's own paragraph is always kept. topical_read.refs() reads the rest
with Clarke's forms (lower-case Roman chapters, "ver. 10" and "chap. iii.
17" in the note's own book and chapter). A citation of the note's own verse
says nothing and is not kept.
"""
import collections
import re
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import topical_read as R  # noqa: E402

HEAD = re.compile(r"Verses?\s+(\d{1,3})(?:\s*[,\-–]\s*(\d{1,3}))?\s*[.,]\s*(.{0,200})", re.S)
BARE = re.compile(r"(?m)^[ \t]*(\d{1,3})(?:\s*[,\-–]\s*(\d{1,3}))?\.\s+([^\]\n]{1,90}(?:\n[^\]\n]{1,90})?)\]")
SEG = re.compile(r"NOTES(?:\s+ON\s+(?:THE\s+)?(?:CHAP|P\.?\s?SALM)[^\n]{0,14}|\.\s*[—-]|\.\s*\n)")
_HEAD_AT_START = re.compile(r"(?m)^\s*Verses?\s+\d{1,3}(?:\s*[,\-–]\s*\d{1,3})?\s*[.,]")
_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
_ROMAN_OCR = str.maketrans({"H": "II", "1": "I", "l": "I", "T": "I", "U": "II", "i": "I"})
CHRON = re.compile(r"A\.\s*M\.\s*\d|An\.\s*Exod|Anno\s+ante|Olymp|B\.\s*C\.\s*\d|Vol\.\s+[IVX]+\.\s*\(|A\.\s*U\.\s*C")
_MARK = "[a-zA-Z■•*'\">^‘’“”]{1,2}"
MARGIN = re.compile(r"(?:^|[.;,]\s+|\s)" + _MARK + r"\s+(?:[1-3]\s?[A-Z][a-z]{1,6}\.|[A-Z][a-z]{1,6}\.\s+[ivxlc]+\.|"
                    r"[A-Z][a-z]{1,6}\.\s+\d+\.\s+\d|Or,|Heb\.|Chald\.|Ver\.|Chap\.)")
MARGIN_START = re.compile(r"\s*" + _MARK + r"\s+")
CLASSICAL = re.compile(r"Iliad|Odyss|\u00c6neid|neid\b|Georg|Ecl\.|Ibid|ibid|Virg|Hom\.|Horat|Ovid|Met\.|lib\.|Lib\.|[A-Z][a-z]+\s+[ivxlcIVXLC]+\.,")
NEED = 0.5          # share of the lemma's words in the KJV verse it names
OFF_CHAPTER = 0.5   # share of a paragraph's word pairs in the chapter's KJV: the Bible text
SKIP = 0.2          # what skipping a run costs the alignment
BASE = 0.35         # what a lemma is expected to share with an unrelated verse
NUMERAL = 1.5       # the bonus when the heading's numeral names the chapter


def words(s):
    return [w for w in re.findall(r"[a-z]+", s.lower()) if len(w) > 2]


def pairs(s):
    w = re.findall(r"[a-z]+", s.lower())
    return set(zip(w, w[1:]))


class Kjv:
    """The KJV's words per verse and word pairs per chapter, for the lemma test."""

    def __init__(self, text, shape):
        self.text, self.shape = text, shape
        self._w, self._p = {}, {}

    def verse_words(self, b, c, v):
        k = (b, c, v)
        if k not in self._w:
            self._w[k] = set(words(self.text["kjv:%s.%d.%d" % k]))
        return self._w[k]

    def chapter_pairs(self, b, c):
        if (b, c) not in self._p:
            self._p[(b, c)] = set().union(*(pairs(self.text["kjv:%s.%d.%d" % (b, c, v)])
                                            for v in range(1, self.shape[b][c] + 1)))
        return self._p[(b, c)]

    def sim(self, lemma, b, c, v):
        w = words(lemma)
        if not w or not 1 <= v <= self.shape[b].get(c, 0):
            return 0.0
        kw = self.verse_words(b, c, v)
        return sum(x in kw for x in w) / len(w)


def heads(t, bare=False):
    """[(offset, verse, last verse or None, lemma)] in the order printed."""
    out = []
    for m in HEAD.finditer(t):
        tail = m.group(3)
        k = re.search(r"[\]\\^]", tail)
        lem = tail[:k.start()] if k and k.start() < 160 else tail[:70]
        out.append((m.start(), int(m.group(1)), int(m.group(2)) if m.group(2) else None, " ".join(lem.split())))
    if bare:
        for m in BARE.finditer(t):
            out.append((m.start(), int(m.group(1)), int(m.group(2)) if m.group(2) else None, " ".join(m.group(3).split())))
    return sorted(out)


def heading_numeral(s):
    """"NOTES ON CHAP. XLH." -> 42 (H is II to the OCR); None if unread."""
    if not re.match(r"NOTES\s+ON", s):
        return None
    s = re.sub(r"^NOTES\s+ON\s+(?:THE\s+)?(?:CHAP|P\.?\s?SALM)\.?", "", s)
    s = re.sub(r"[^IVXLCHlTUi1]", "", s).translate(_ROMAN_OCR)
    if not s or not re.fullmatch(r"[IVXLC]+", s):
        return None
    v = 0
    for a, b in zip(s, s[1:] + " "):
        x = _ROMAN[a]
        v += -x if b != " " and _ROMAN.get(b, 0) > x else x
    return v


def runs(t, bare=False):
    hs = heads(t, bare)
    ms = list(SEG.finditer(t))
    out = []
    for k, m in enumerate(ms):
        end = ms[k + 1].start() if k + 1 < len(ms) else len(t)
        cur = {"num": heading_numeral(m.group(0)), "heads": []}
        last = 0
        for h in hs:
            if not m.start() <= h[0] < end:
                continue
            if cur["heads"] and h[1] < last - 5 and h[1] <= 3:      # a lost heading
                out.append(cur)
                cur = {"num": None, "heads": []}
            cur["heads"].append(h)
            last = h[1]
        out.append(cur)
    return out


def chapters(seq, b0, b1):
    """The (book, chapter)s from b0 to b1, in canonical order."""
    order = list(dict.fromkeys(b for b, _, _ in seq))
    books = set(order[order.index(b0):order.index(b1) + 1])
    return [(b, c) for b, c, v in seq if v == 1 and b in books]


def run_score(r, bc, kjv):
    b, c = bc
    sc = 0.0
    for _, n, _, lem in r["heads"]:
        if not 1 <= n <= kjv.shape[b][c]:
            sc -= 0.5
            continue
        if len(words(lem)) < 2:
            continue
        sc += kjv.sim(lem, b, c, n) - BASE
    if r["num"] is not None and r["num"] == c:
        sc += NUMERAL
    return sc


def align(rs, chs, kjv):
    """Each run to a chapter or none, the chapters strictly in order."""
    S, C = len(rs), len(chs)
    dp = [[0.0] * (C + 1) for _ in range(S + 1)]
    bk = [[None] * (C + 1) for _ in range(S + 1)]
    for i in range(1, S + 1):
        dp[i][0], bk[i][0] = dp[i - 1][0] - SKIP, "skip"
        for c in range(1, C + 1):
            dp[i][c], bk[i][c] = max((dp[i][c - 1], "left"), (dp[i - 1][c] - SKIP, "skip"),
                                     (dp[i - 1][c - 1] + run_score(rs[i - 1], chs[c - 1], kjv), "take"))
    i, c, out = S, C, [None] * S
    while i > 0:
        k = bk[i][c]
        if k == "left":
            c -= 1
        elif k == "skip":
            i -= 1
        else:
            out[i - 1] = chs[c - 1]
            i, c = i - 1, c - 1
    return out


def read_volume(t, b0, b1, kjv, seq, bare=False):
    """The volume's heads: [{"at", "n", "n2", "lemma", "chapter", "sim", "placed"}], and counts."""
    rs = runs(t, bare)
    chs = chapters(seq, b0, b1)
    got = align(rs, chs, kjv)
    out = []
    counts = collections.Counter(chapters=len(chs), chapters_found=len(set(g for g in got if g)))
    for r, bc in zip(rs, got):
        for at, n, n2, lem in r["heads"]:
            s = kjv.sim(lem, bc[0], bc[1], n) if bc else 0.0
            ok = bool(bc) and len(words(lem)) >= 2 and s >= NEED
            out.append({"at": at, "n": n, "n2": n2, "lemma": lem, "chapter": bc, "sim": s, "placed": ok})
            counts["heads"] += 1
            counts["heads placed" if ok else "heads not placed"] += 1
    return out, counts


_REFLIKE = re.compile(r"\b[ivxlcIVXLC]{1,7}\.\s*\d|\d\s*[;,]\s*(?:\d|[ivxlc]+\.)")
_ROMANISH = re.compile(r"[ivxlc]+|[IVXLC]+")


def prose_words(p):
    """The words of a paragraph that are neither book names nor Roman numerals."""
    return [w for w in re.findall(r"[A-Za-z]{3,}", p)
            if w not in R.FORM_OLD and w not in ("Chron", "Kings", "Sam", "Psa", "See", "Chap", "Ver", "ver", "chap", "and", "Comp") and not _ROMANISH.fullmatch(w)]


def classify(p, b, c, kjv):
    if CHRON.search(p):
        return "chronology"
    pp = pairs(p)
    if len(pp) >= 4:
        cp = kjv.chapter_pairs(b, c) | (kjv.chapter_pairs(b, c + 1) if c + 1 in kjv.shape[b] else set())
        if sum(x in cp for x in pp) / len(pp) >= OFF_CHAPTER:
            return "bible"
    mk = MARGIN.findall(p)
    if len(mk) >= 2 or (mk and MARGIN_START.match(p)) or re.search(r"(?:\b|[a-z])Or,\s|(?:\b|[a-z])Heb\.\s(?!xi)", p):
        return "margin"
    if _REFLIKE.search(p) and len(prose_words(p)) < 4:
        return "margin"         # a run of references with no prose: the margin, cut by the OCR's lines
    rs = R.refs(p, here=(b, c), old=True)
    if rs:
        cover = sum(r["end"] - r["at"] for r in rs) / max(1, len(p.strip()))
        if MARGIN_START.match(p) and cover >= 0.3:
            return "margin"
        if cover >= 0.55 and not re.search(r"[a-z]{4,}\s+[a-z]{4,}\s+[a-z]{4,}", p):
            return "margin"
    return "note"


def note_text(t, hs, i, kjv, limit=4000):
    """The note at heads[i]: its kept paragraphs, and what was dropped."""
    h = hs[i]
    end = hs[i + 1]["at"] if i + 1 < len(hs) else h["at"] + limit
    seg = t[h["at"]:end]
    m = re.search(r"\n\s*(?:NOTES\s+ON|CHAPTER\s+[IVXLC]+\.)", seg)
    if m:
        seg = seg[:m.start()]
    b, c = h["chapter"]
    kept, dropped = [], collections.Counter()
    for k, p in enumerate(re.split(r"\n\s*\n", seg)):
        x = "note" if k == 0 else classify(p, b, c, kjv)
        if x == "note":
            kept.append(_HEAD_AT_START.sub(" ", p))
        else:
            dropped[x] += 1
    return "\n\n".join(" ".join(p.split()) for p in kept if p.strip()), dropped


def citations(txt, b, c):
    """The refs() readings of a note's kept text, as (book, c, v, c2, v2); a
    whole chapter is None for v (the caller widens it)."""
    out = []
    for r in R.refs(txt, here=(b, c), old=True):
        if re.match(r"[vV]er", txt[r["at"]:r["at"] + 3]) and CLASSICAL.search(txt[max(0, r["at"] - 18):r["at"]]):
            continue        # "Iliad i., ver. 407": a line of Homer, not a verse of this chapter
        out.append((r["book"], r["c"], r["v"], r["c2"], r["v2"]))
    return out
