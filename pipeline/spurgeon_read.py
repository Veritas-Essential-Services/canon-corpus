#!/usr/bin/env python3
"""
spurgeon_read.py -- the Exposition in Spurgeon's Treasury of David, read
from the OCR of open archive.org scans: which verses each comment is on, and
what it cites.

CCEL's Treasury of David is page images only (its XML holds no text), and no
other keyed text has a library's provenance. So both readings come from
scans, of two printings set apart: London (Marshall Brothers, six volumes)
and New York (Funk & Wagnalls, seven volumes). Only what both printings read
is committed (build_commentary.build_scan_work's rule, applied by
build_spurgeon_work).

THE PAGE. Each psalm has an "EXPOSITION." section, then "EXPLANATORY NOTES
AND QUAINT SAYINGS" (other authors, quoted) and "HINTS TO PREACHERS". Only
the Exposition is Spurgeon's own running comment, so only it is read. In it
the KJV text is printed a few verses at a time ("2 The kings of the earth set
themselves ..."), the first verse of a psalm or section unnumbered, and his
comment follows each group.

WHERE A COMMENT IS (read_volume):
  1. The Expositions, each from its heading to the next notes heading.
  2. Which psalm each is: the Expositions are aligned in order to the
     volume's psalms by dynamic programming, scoring how far the printed
     verse lines' words are in the KJV verses their numbers name (Psalm 119,
     printed in sections, may take several in a row).
  3. A verse line is a line opening with a number whose words are at least
     half in that KJV verse, the numbers rising. The text after a group of
     verse lines, up to the next one, is the comment on that group; a short
     block that is itself mostly the KJV's words is the verse running on.
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clarke_read as CR  # noqa: E402
import topical_read as R  # noqa: E402

EXPO = re.compile(r"(?m)^[ \t]*EXPOSITION(?:[ \t]+OF[ \t]+VERSES?[^\n]{0,40})?[ \t]*[.,]?[ \t]*$")
# where the Exposition stops: the notes (by heading, or by their "Verse 1. --" form), the hints, the next psalm
END = re.compile(r"(?m)^[ \t]*(?:EXPLANATORY\s+NOTES|NOTES\s+ON\s+VERSES?|HINTS\s+TO|PSALM\s+[CLXVI]{1,9}\.\s*$"
                 r"|Verses?\s+\d{1,3}(?:\s*[,\-\u2014]+\s*\d{1,3})?\s*\.\s*[\-\u2014])")
LINE = re.compile(r"(?m)^[ \t]*(\d{1,3})[ \t]+([A-Za-z‘“'\"(][^\n]{8,})$")
RUNNING = re.compile(r"(?m)^[ \t]*PSALM\s+THE\s+[A-Z\- ]+\.?[ \t]*\d*[ \t]*$|^[ \t]*\d+[ \t]+(?:THE\s+)?TREASURY\s+OF\s+DAVID\.?[ \t]*$")
NEED = 0.5
LIMIT = 250000


def expositions(t):
    out = []
    ms = list(EXPO.finditer(t))
    for k, m in enumerate(ms):
        e = END.search(t, m.end())
        ends = [m.end() + LIMIT, len(t)] + ([e.start()] if e else []) + ([ms[k + 1].start()] if k + 1 < len(ms) else [])
        out.append((m.end(), min(ends)))
    return out


def verse_lines(seg, b, c, kjv):
    """The numbered verse lines of one Exposition read as psalm c: [(offset, end, verse, sim)].

    Every line whose words are at least half in the verse its number names
    is a candidate; of those, the chain with rising numbers that scores
    highest is kept, so one stray line (a quotation that happens to open
    with a number) cannot shut out the rest."""
    n = kjv.shape[b].get(c, 0)
    cand = []
    for m in LINE.finditer(seg):
        v = int(m.group(1))
        if not 0 < v <= n:
            continue
        s = kjv.sim(m.group(2), b, c, v)
        if s >= NEED and len(CR.words(m.group(2))) >= 2:
            cand.append((m.start(), m.end(), v, s))
    best, back = [], []
    for i, (_, _, v, s) in enumerate(cand):
        j = max((k for k in range(i) if cand[k][2] < v), key=lambda k: best[k], default=None)
        best.append(s + (best[j] if j is not None else 0))
        back.append(j)
    out = []
    i = max(range(len(cand)), key=lambda k: best[k], default=None)
    while i is not None:
        out.append(cand[i])
        i = back[i]
    return out[::-1]


def first_verse(seg, b, c, kjv, lines):
    """The unnumbered verse that opens the section: the first verse before the first numbered one."""
    head = seg[:lines[0][0]] if lines else seg[:600]
    words = CR.words(head[:300])
    if len(words) < 3:
        return None
    hi = lines[0][2] - 1 if lines else min(kjv.shape[b][c], 1)
    for v in range(hi, 0, -1):
        if kjv.sim(" ".join(words[:12]), b, c, v) >= NEED:
            return v
    return None


def score(seg, b, c, kjv):
    ls = verse_lines(seg, b, c, kjv)
    return sum(s - 0.3 for _, _, _, s in ls) + (1.0 if first_verse(seg, b, c, kjv, ls) else 0.0)


def align(segs, chs, b, kjv, again=frozenset({119})):
    """Each Exposition to a psalm or none, in order; a psalm in `again` may take several in a row."""
    S, C = len(segs), len(chs)
    sc = [[score(s, b, c, kjv) for c in chs] for s in segs]
    NEG = float("-inf")
    dp = [[NEG] * (C + 1) for _ in range(S + 1)]
    bk = [[None] * (C + 1) for _ in range(S + 1)]
    for c in range(C + 1):
        dp[0][c] = 0.0
    for i in range(1, S + 1):
        for c in range(C + 1):
            best = (dp[i - 1][c] - 0.2, ("skip", c))
            if c > 0:
                best = max(best, (dp[i][c - 1], ("left", c - 1)), key=lambda x: x[0])
                take = max(dp[i - 1][c - 1], dp[i - 1][c] if chs[c - 1] in again else NEG)
                prev = c - 1 if dp[i - 1][c - 1] >= (dp[i - 1][c] if chs[c - 1] in again else NEG) else c
                if take + sc[i - 1][c - 1] > best[0] and sc[i - 1][c - 1] > 0:
                    best = (take + sc[i - 1][c - 1], ("take", prev))
            dp[i][c], bk[i][c] = best
    out = [None] * S
    i, c = S, max(range(C + 1), key=lambda k: dp[S][k])
    while i > 0:
        kind, pc = bk[i][c]
        if kind == "left":
            c = pc
        elif kind == "skip":
            i -= 1
        else:
            out[i - 1] = chs[c - 1]
            i, c = i - 1, pc
    return out


HEAD = re.compile(r"(?m)^[ \t]*(\d{1,3})(?:[ \t]*[,\-][ \t]*(\d{1,3}))?[ \t]*\.[ \t]+(?=\S)")


def groups(seg, b, c, kjv):
    """The printed verse lines in groups: [(first verse, last verse, where the group's comment starts)]."""
    ls = verse_lines(seg, b, c, kjv)
    fv = first_verse(seg, b, c, kjv, ls)
    marks = ([(0, 0, fv)] if fv else []) + [(a, z, v) for a, z, v, _ in ls]
    out = []
    group = None
    for k, (a, z, v) in enumerate(marks):
        nxt = marks[k + 1][0] if k + 1 < len(marks) else len(seg)
        block = seg[z:nxt]
        if group is None:
            group = [v, v, a]
        group[1] = v
        words = CR.words(block)
        kw = kjv.verse_words(b, c, v) | (kjv.verse_words(b, c, v + 1) if v + 1 <= kjv.shape[b][c] else set())
        running_on = len(block) < 400 and (not words or sum(w in kw for w in words) / len(words) >= 0.6)
        if running_on and k + 1 < len(marks):
            continue
        out.append((group[0], group[1], z, nxt))
        group = None
    return out


def comments(seg, b, c, kjv, counts=None):
    """[(first verse, last verse, comment text)] of one Exposition read as psalm c.

    The comment after a group of printed verses is on that group. Where it
    is cut by numbered heads ("2. \u201cHe maketh me ...\u201d"), each head opens a
    comment on its own verse (or "4, 5." verses). A head is read only when
    its number is past every verse already commented on and not past the
    group's last verse, so a page or footnote number is never a head; the
    group may be one Spurgeon printed in several pieces (Ps 103 prints
    verses 6-19 across a page and then comments on each).
    A group's own comment needs 40 words: less is a page's running matter."""
    seg = RUNNING.sub(" ", seg)
    out, done = [], 0
    for lo, hi, a, z in groups(seg, b, c, kjv):
        block = seg[a:z]
        heads, last = [], done
        for m in HEAD.finditer(block):
            v = int(m.group(1))
            v2 = int(m.group(2)) if m.group(2) else v
            if last < v <= hi and v <= v2 <= hi:
                heads.append((m.start(), m.end(), v, v2))
                last = v2
        pre = block[:heads[0][0]] if heads else block
        if len(CR.words(pre)) >= 40:
            out.append((lo, hi, " ".join(pre.split())))
            if counts is not None:
                counts["comments on a group of verses"] += 1
        elif not heads and counts is not None:
            counts["verse groups with no comment of their own"] += 1
        for k, (s, e, v, v2) in enumerate(heads):
            nxt = heads[k + 1][0] if k + 1 < len(heads) else len(block)
            out.append((v, v2, " ".join(block[e:nxt].split())))
            if counts is not None:
                counts["comments under a numbered head"] += 1
        if heads or len(CR.words(pre)) >= 40:
            done = max(done, last if heads else hi)
    return out


def read_volume(t, b0, b1, kjv, seq):
    """The volume's comments: {(psalm, first verse): {"last", "text"}}, and counts."""
    order = list(dict.fromkeys(x for x, _, _ in seq))
    chs = [c for b, c, v in seq if b == "Ps" and v == 1 and b0 <= c <= b1]
    segs = [t[a:z] for a, z in expositions(t)]
    got = align(segs, chs, "Ps", kjv)
    counts = collections.Counter(expositions=len(segs), psalms=len(chs), psalms_found=len({g for g in got if g}))
    out = collections.OrderedDict()
    for s, c in zip(segs, got):
        if c is None:
            counts["expositions not placed"] += 1
            continue
        for v1, v2, text in comments(s, "Ps", c, kjv, counts):
            k = (c, v1)
            if k in out:
                out[k]["text"] += "\n\n" + text
                out[k]["last"] = max(out[k]["last"], v2)
            else:
                out[k] = {"last": v2, "text": text}
    del order
    return out, counts


def citations(txt, c):
    return [(r["book"], r["c"], r["v"], r["c2"], r["v2"]) for r in R.refs(txt, here=("Ps", c), old=True)]
