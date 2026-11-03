#!/usr/bin/env python3
"""
single_read.py -- a commentary on one book, read from the OCR of open
archive.org scans: where each comment is, and what it cites.

For the 19th-century commentaries on a single book that no library has
keyed (Hodge on Romans and Corinthians, Haldane on Romans, John Brown on
Hebrews and 1 Peter), both readings come from scans of two printings, and
only what both read is committed (build_commentary.build_scan_work).

THE PAGE. These books divide by "CHAPTER IV." headings and open each comment
with a verse head: "VERSE 1. Paul, a servant ...", "V. 2.--Which he had
promised ...", "Ver. 5. \"For unto ...", "Verses 1-3.--God, who at sundry
...". The words after the number are the lemma: the KJV words commented on.

WHERE A COMMENT IS (read_volume): the chapter headings cut the heads into
runs, and the runs are aligned in order to the book's chapters by
clarke_read's dynamic programming (lemmas against the KJV verses their heads
name, plus the heading's numeral). A head is placed when at least half of
its lemma's words (two or more, of 3+ letters) are in the KJV verse it
names: so a numbered point in the comment ("5. God is the ultimate end") or
a verse cited in passing ("V. 26 he expressly states") is not a head.

WHAT A COMMENT CITES: the text from its head to the next placed head, cut at
the next chapter heading, with running heads (short lines nearly all
capitals) taken out. topical_read.refs() reads it with the old forms
(Roman chapters, "ver. 5" in the comment's own chapter), and with
"Heb. 13, 9" where the work writes chapter and verse that way.
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clarke_read as CR  # noqa: E402
import topical_read as R  # noqa: E402

HEAD = re.compile(r"(?m)^[ \t]*(?:VERSES?|Verses?|VER\.|Ver\.|V\.)[ \t]*(\d{1,3})(?:[ \t]*[,\-–—][ \t]*(\d{1,3}))?"
                  r"[ \t]*[.,:]?[ \t]*[\-—–]*[ \t]*([^\n]{0,160}(?:\n[^\n]{0,120})?)")
BARE = re.compile(r"(?m)^[ \t]*(\d{1,3})(?:[ \t]*[,\-\u2013][ \t]*(\d{1,3}))?\.[ \t]+([A-Z][^\n]{0,160}(?:\n[^\n]{0,120})?)")
CHAPTER = re.compile(r"(?m)^[ \t]*CHAPTER[ \t]+([A-Za-z1]{1,8})\.?[ \t]*(?:PART[^\n]{0,12})?$")
_RUNNING = re.compile(r"(?m)^[^\na-z]{0,100}$")


def numeral(s):
    return CR.heading_numeral("NOTES ON CHAP. " + s + ".")


def heads(t, bare=False):
    """[(offset, verse, last verse or None, lemma)] in the order printed."""
    out = []
    for m in [*HEAD.finditer(t), *(BARE.finditer(t) if bare else [])]:
        lem = re.split(r"[\]\"”]|\.\s", m.group(3).replace("“", " ").replace("\"", " ", 1))[0]
        out.append((m.start(), int(m.group(1)), int(m.group(2)) if m.group(2) else None, " ".join(lem.split())[:120]))
    return sorted(out)


def runs(t, bare=False):
    hs = heads(t, bare)
    ms = list(CHAPTER.finditer(t))
    out = []
    starts = [(0, None)]
    for m in ms:
        num = numeral(m.group(1))
        if num is None or num != starts[-1][1]:     # "CHAPTER I. PART II." goes on with chapter I
            starts.append((m.start(), num))
    for k, (a, num) in enumerate(starts):
        z = starts[k + 1][0] if k + 1 < len(starts) else len(t)
        cur = {"num": num, "heads": [], "end": z}
        last = 0
        for h in hs:
            if not a <= h[0] < z:
                continue
            if cur["heads"] and h[1] < last - 5 and h[1] <= 3:      # a lost heading
                out.append(cur)
                cur = {"num": None, "heads": [], "end": z}
            cur["heads"].append(h)
            last = h[1]
        out.append(cur)
    return out


def read_volume(t, book, kjv, seq, bare=False):
    """[(chapter, verse, last verse or None, text)] of the placed heads, and counts."""
    rs = runs(t, bare)
    chs = [(b, c) for b, c, v in seq if v == 1 and b == book]
    got = CR.align(rs, chs, kjv)
    counts = collections.Counter(chapters=len(chs), chapters_found=len({g for g in got if g}))
    placed = []
    for r, bc in zip(rs, got):
        for at, n, n2, lem in r["heads"]:
            ok = bool(bc) and len(CR.words(lem)) >= 2 and kjv.sim(lem, bc[0], bc[1], n) >= CR.NEED
            counts["heads placed" if ok else "heads not placed"] += 1
            if ok:
                placed.append((at, r["end"], bc[1], n, n2 if n2 and n2 > n else None))
    out = []
    for k, (at, end, c, n, n2) in enumerate(placed):
        z = min(end, placed[k + 1][0]) if k + 1 < len(placed) else end
        z = min(z, at + 20000)
        out.append((c, n, n2, " ".join(_RUNNING.sub(" ", t[at:z]).split())))
    return out, counts


def citations(txt, b, c, comma=False, roman_comma=False):
    return [(r["book"], r["c"], r["v"], r["c2"], r["v2"])
            for r in R.refs(txt, here=(b, c), old=True, comma=comma, roman_comma=roman_comma)]


# ---- John Brown: a comment on a printed passage, not on a verse head
UNITS = {
    "discourse": re.compile(r"(?m)^[ \t]*DISCOURSE[ \t]+[A-Za-z1]{1,8}\.?[ \t]*$"),
    "section": re.compile(r"(?m)^[ \t]*§[ \t]*\d{1,2}\.[ \t]*[—\-]"),
}
WINDOW = 10         # words in a window of the printed passage
FIRST = 0.8         # share of a window's words in one KJV verse: the passage starts
MORE = 0.6          # ... and goes on


def _best(kjv, book, ws, near=None):
    """The KJV verse (chapter, verse) of `book` that has the most of the window's words, and the share."""
    best, at = 0.0, None
    s = " ".join(ws)
    for c in sorted(kjv.shape[book]):
        if near and not near[0] <= c <= near[0] + 1:
            continue
        for v in range(1, kjv.shape[book][c] + 1):
            x = kjv.sim(s, book, c, v)
            if x > best:
                best, at = x, (c, v)
    return at, best


def passage(seg, book, kjv, look=1500):
    """Where the printed passage in a unit's opening starts and ends: ((c, v), (c, v2), end offset) or None.

    The opening is read in windows of ten words. The passage starts at the
    first window with 80% of its words in one KJV verse,
    and runs while each window has 60% in a verse at or a few past the last."""
    toks = [(m.start(), m.end(), m.group().lower()) for m in re.finditer(r"[A-Za-z]{3,}", seg[:look + 2500])]
    i, start = 0, None
    while i + WINDOW <= len(toks) and toks[i][0] < look:
        at, s = _best(kjv, book, [w for _, _, w in toks[i:i + WINDOW]])
        if at and s >= FIRST:
            start = at
            break
        i += 2
    if not start:
        return None
    last, end = start, toks[i + WINDOW - 1][1]
    j = i + WINDOW
    while j + WINDOW <= len(toks):
        at, s = _best(kjv, book, [w for _, _, w in toks[j:j + WINDOW]], near=last)
        if not at or s < MORE or at < last or (at[0] == last[0] and at[1] > last[1] + 4):
            break
        last, end = at, toks[j + WINDOW - 1][1]
        j += WINDOW
    return start, last, end


PASSAGE_HEAD = re.compile(r"(?m)^[^\n]{0,14}?[A-Za-z]{2,7}\.?[ \t]+([ivxlcIVXLC\u00a51]{1,6})\.?[ \t]*(\d{1,3})"
                          r"(?:[ \t]*[,\-\u2013][ \t]*(\d{1,3}))?\.?[ \t]*[\u2014\-]+[ \t]*")


def printed_head(seg, book, kjv, look=700):
    """A passage head ("1 PET. i. 3-5.-- Blessed be the God ...") near the unit's start, checked by the
    words printed after it: ((c, v), (c, v2), end offset) or None."""
    for m in PASSAGE_HEAD.finditer(seg[:look]):
        c = numeral(m.group(1).replace("\u00a5", "v").replace("1", "i").upper())
        v = int(m.group(2))
        v2 = int(m.group(3)) if m.group(3) else v
        if not c or c not in kjv.shape[book] or not 1 <= v <= v2 <= kjv.shape[book][c]:
            continue
        if kjv.sim(" ".join(CR.words(seg[m.end():m.end() + 200])[:WINDOW]), book, c, v) < CR.NEED:
            continue
        return (c, v), (c, v2), m.end()
    return None


def read_passages(t, book, kjv, unit):
    """[(chapter, verse, last verse or None, text)] of the units whose passage is read, and counts.

    A unit is a discourse or section of at least 3,000 characters (a shorter
    one is an entry in the contents). Its passage is its printed head when
    one is read and the words after it are that verse's; else the printed
    text found by windows (passage()) in its opening. A passage running into
    the next chapter is taken to its first chapter's end."""
    heads = [m.end() for m in UNITS[unit].finditer(t)]
    for m in PASSAGE_HEAD.finditer(t):          # a passage head whose unit heading the OCR lost
        if not any(0 <= m.start() - h < 700 for h in heads) and printed_head(t[m.start():m.start() + 700], book, kjv):
            heads.append(m.start())
    heads.sort()
    counts = collections.Counter(units=len(heads))
    out = []
    for k, a in enumerate(heads):
        z = heads[k + 1] if k + 1 < len(heads) else min(len(t), a + 200000)
        seg = t[a:z]
        if len(seg) < 3000:
            counts["units too short: the contents"] += 1
            continue
        p = printed_head(seg, book, kjv)
        how = "printed head"
        if not p:
            p, how = passage(seg, book, kjv, look=700), "printed text"
        if not p:
            counts["units with no passage read"] += 1
            continue
        (c, v), (c2, v2), e = p
        if c2 != c:
            v2 = kjv.shape[book][c]
        counts["units placed by their " + how] += 1
        out.append((c, v, v2 if v2 > v else None, " ".join(_RUNNING.sub(" ", seg[e:]).split())))
    return out, counts


def read_free(t, book, kjv):
    """John Brown's Hebrews: his CHAPTERs are the divisions of his argument, not the Bible's chapters, so a
    verse head ("Ver. 5.", "Verses 1-3.--") is placed by its lemma alone: in the chapter, at or after the last
    one placed, whose verse that number names has half its words (the nearest such chapter wins). The
    printed passages that open his sections are read as in read_passages. Each comment runs to the next.
    [(chapter, verse, last verse or None, text)], and counts."""
    counts = collections.Counter()
    found = []
    for at, n, n2, lem in heads(t):
        found.append((at, "head", (n, n2, lem)))
    for m in UNITS["section"].finditer(t):
        found.append((m.end(), "section", None))
    found.sort()
    placed, last = [], 1
    for at, kind, x in found:
        if kind == "head":
            n, n2, lem = x
            if len(CR.words(lem)) < 2:
                counts["verse heads with no lemma"] += 1
                continue
            cs = [c for c in sorted(kjv.shape[book]) if c >= last and kjv.sim(lem, book, c, n) >= CR.NEED]
            if not cs:
                counts["verse heads not placed"] += 1
                continue
            c, v, v2, e = cs[0], n, n2 if n2 and n2 > n else None, at
            counts["verse heads placed"] += 1
        else:
            p = printed_head(t[at:at + 700], book, kjv) or passage(t[at:at + 6000], book, kjv, look=700)
            if not p or p[0][0] < last:
                counts["sections with no passage read"] += 1
                continue
            (c, v), (c2, v2), e = p
            v2 = (v2 if c2 == c else kjv.shape[book][c])
            v2, e = (v2 if v2 > v else None), at + e
            counts["sections placed by their printed passage"] += 1
        placed.append((e, c, v, v2))
        last = c
    out = []
    for k, (e, c, v, v2) in enumerate(placed):
        z = placed[k + 1][0] if k + 1 < len(placed) else min(len(t), e + 60000)
        out.append((c, v, v2, " ".join(_RUNNING.sub(" ", t[e:z]).split())))
    return out, counts
