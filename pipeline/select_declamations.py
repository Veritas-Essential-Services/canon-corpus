#!/usr/bin/env python3
# prov: 2026-11-03 claude-opus-5-5 drafted
# fable_review: pending
"""
select_declamations.py -- the pool's prose pieces (speeches, orations and
the readers' prose lessons) as the poetry section's `declamations` layer.

    python3 pipeline/select_declamations.py --fetch   # fetch the books' mirror copies and pin them
    python3 pipeline/select_declamations.py           # write data/poetry/selections/declamations.jsonl
    python3 pipeline/build_poetry.py                  # then build as usual (mints the new uids once)

    Input:  data/poetry/pool/pool.jsonl        (the candidates; kind "prose" here)
            data/poetry/pool/rows/<pg>.jsonl   (each book's own title, author, first line and order)
            data/poetry/pool/sources.json      (each book's year, audience, mirror URL)
            data/poetry/selections/*.jsonl     (the other layers: a piece already there is not repeated)
    Output: data/poetry/selections/declamations.jsonl   (COMMITTED; the build's input)
            data/poetry/sources.json                    (a `mirror` pin added to each book used)

WHICH PIECES
    Every pool row of kind "prose" (667), plus the declamations the Schoolroom
    Treasury plan names that a pool book prints but its parser missed (PLAN_EXTRA:
    the Crispin's Day speech, from Patriotic Song, 1901). A piece whose text is
    already in another layer (the pool's parser sometimes called a verse lesson
    prose) is not repeated; a speech printed by two pool books is one row.

WHICH COPY OF THE BOOK
    The pool's rows were parsed from the GITenberg mirror's transcription of
    each book; the build's pins (sources.json `sha256`) are gutenberg.org's
    later files, which this sandbox could not reach. So the declamations are
    cut from the mirror copy, pinned on its own (`mirror`: raw_url, sha256,
    encoding) and recorded in each row (`pd_source.copy: "mirror"`).

WHERE THE CUT BEGINS AND ENDS
    At the piece's heading the reader skips what the editor put above the
    text: a byline, a date or place line in parentheses, a bracketed or
    indented headnote (kept as `headnote`), McGuffey's life of the author
    (which the Sixth Reader closes with "###", and the Fourth and Fifth with
    the text's paragraph "1."). The cut ends before the next heading (a
    capitals line or a section numeral after two blank lines, or a centred
    one after one), before
    McGuffey's NOTES, DEFINITIONS and EXERCISES, and above a signature or
    credit line at the foot (kept as `signed`). Paragraph breaks are kept;
    the transcription's wrapped lines are joined; a reader's paragraph
    numbers are dropped. The rule is stored in the row (`extract`:
    first_line, occurrence, end, gap, reflow, para_numbers) and the build
    replays it; a rule that does not replay to the same text is refused.

WHAT IS REFUSED (the row stays, linked out, with the reason)
    A cut that runs into the next piece of the book, one that is the editor's
    note rather than the piece, one under MIN_WORDS, one over MAX_WORDS
    (longer than any piece a pupil would declaim: it has run on), and one
    whose first line or heading cannot be found.

GRADE HINTS
    `grade_hint`: the pool's `audiences` for the piece, and for a McGuffey
    reader its number and lesson numeral, so a later pass can band them.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_poetry as B  # noqa: E402
import select_treasury as S  # noqa: E402

OUT = os.path.join(B.SEL, "declamations.jsonl")
LAYER = "declamations"
MCGUFFEY = {14668: 2, 14766: 3, 14880: 4, 15040: 5, 16751: 6}
MIN_WORDS = 20
MAX_WORDS = 4000          # longer than any piece a pupil would declaim whole (the speakers' longest run near 4,000)
RUNAWAY = 1500            # lines from the start without reaching an end: refused
STOP = re.compile(r"^\s*(?:NOTES?\b|Notes?\.|DEFINITIONS\b|EXERCISES\b|SLATE WORK\b|End of (?:the )?Project Gutenberg)")
LESSON = re.compile(r"^LESSON [IVXLC]+\.?\s*$")     # McGuffey's Second and Third: a lesson's head, blank line above or not
EDITORIAL = re.compile(r"\b(?:the editor'?s?|this collection|this volume|permission to (?:include|use|reprint)"
                       r"|thanks are due)\b", re.I)
NOTE = re.compile(r"^\s*\[Transcriber")   # a transcriber's note inside a piece: skipped, like a footnote
# The Third Reader's transcription keeps its running heads and page numbers (tab-led) and stray signature marks ("3,3")
DROP = {14766: r"^\s*\d*\s*\t|^\d,\d+\.?\s*$"}
# McGuffey's life of the author: a name, then dates ("Maria Edgeworth (b. 1767, d. 1849)", "Noah Porter, 1811-1892,")
BIO = re.compile(r"^[A-Z][^.()]{0,70}?(?:\(b\. ?1\d{3}|,\s*1\d{3}\s*-\s*1\d{3})")

# The Treasury plan's declamations (docs/context/schoolroom-treasury-poetry-plan.md).
PLAN = {
    "p02839": "The Gettysburg Address (Lincoln, 1863)",
    "p04903": "\"Give me liberty, or give me death!\" (Patrick Henry, as printed by Wirt)",
    "p04907": "\"Give me liberty, or give me death!\" (Patrick Henry, as printed by Wirt)",
}
# The pool left the author blank where the book names him only in the heading.
HEADING_AUTHOR = {"p04907": "Patrick Henry"}      # "SPEECH OF PATRICK HENRY, IN THE CONVENTION ..."
ONE_MAN = [{"William Pitt", "Lord Chatham"}]      # Pitt the elder, Earl of Chatham: the books print either name
SMALL = {"a", "an", "the", "of", "and", "in", "on", "to", "at", "for", "by", "with", "from", "or", "upon", "into", "vs"}
PLAN_EXTRA = [
    {"pool_id": None, "title": "St. Crispin's Day at Agincourt", "author": "William Shakespeare",
     "first_line": "‘This day is called the feast of Crispian:", "kind": "prose", "n_books": 1,
     "books": [52133], "audiences": ["general"], "also_in": [],
     "named_in_plan": "Crispin's Day speech (Henry V)",
     "note": "Not in the pool: Patriotic Song (1901), a pool book, prints it under this heading, "
             "but the pool's parser for that book missed it. It is verse, and in no other layer. The anthology "
             "prints it abridged: the four lines from \"We few, we happy few, we band of brothers\" to \"This "
             "day shall gentle his condition\" are not in it."},
]


# ---------------------------------------------------------------------------
# Lines
# ---------------------------------------------------------------------------

def is_head(l):
    """A heading line: capitals (a 49291 heading carries "--_Author._" or a
    date after its title, McGuffey's a page number in parentheses; a small
    word like "vs." or "and" may stand in lower case), or a section numeral."""
    t = l.strip()
    if not t or len(t) > 110 or t.startswith("["):
        return False
    if "--" in t:
        t = t.split("--")[0]
    t = re.sub(r"\(\d+\)", "", t)
    t = re.sub(r"\b(?:vs|and|of|the|de|von|van|to|in|on|a)\b\.?", "", t)
    letters = re.sub(r"[^A-Za-z]", "", t)
    return (len(letters) >= 2 and letters.isupper()) or bool(re.fullmatch(r"[IVXLC]+\.?", t.strip()))


def indent(l):
    return len(l) - len(l.lstrip())


def para_at(L, i):
    """The paragraph (indexes of its lines) starting at line i."""
    out = []
    while i < len(L) and L[i].strip():
        out.append(i)
        i += 1
    return out


def first_line_hits(L, fl):
    want = S.fold(fl)
    if len(want.split()) < 2:
        return []
    return [i for i, l in enumerate(L) if l.strip() and S.fold(re.sub(r"^\s*\d{1,2}\.\s+", "", l)) == want]


def heading_above(L, i, title):
    """The piece's heading above line i: the nearest heading block (within 80
    lines, not past a McGuffey LESSON line) that names the title; a heading
    may run over several lines, or stand in lower case when it is the title
    itself. Failing that, the nearest heading block, if two blank lines
    stand above it (the pool took 46427's titles from its contents, which
    shorten the printed headings). None when there is neither."""
    want = B.norm(title)
    nearest = None
    for k in range(i - 1, max(-1, i - 80), -1):
        exact = bool(want) and B._clean_heading(re.sub(r"\(\d+\)", "", L[k])) == want and not L[k - 1].strip()
        if not (is_head(L[k]) or exact):
            continue
        a = k
        while a > 0 and L[a - 1].strip() and is_head(L[a - 1]) and not L[a - 1].startswith("\t"):
            a -= 1
        b = k
        while b + 1 < len(L) and L[b + 1].strip() and (is_head(L[b + 1]) or not re.search(r"[a-z]", L[b + 1])
                                                         or "".join(L[a:b + 1]).count("_") % 2):
            b += 1                                # (an italic byline run over two lines: "--_Hon. S. S. Cox, ...")
        block = B._clean_heading(re.sub(r"\(\d+\)", "", " ".join(x.strip() for x in L[a:b + 1])))
        if exact or want and (block == want or block.startswith(want + " ")
                              or len(want) > 6 and (want in block or (block in want and len(block) > 6))):
            return a, b, True
        if nearest is None:
            nearest = (a, b, False) if a > 1 and not L[a - 1].strip() and not L[a - 2].strip() else False
        if LESSON.match(L[k]):
            break                                 # past the lesson's own head: not this piece
    return nearest or None


def text_start(L, h_end, book, front):
    """Skip what the editor set between the heading and the text; `front`
    collects it (the headnote)."""
    nxt = next_heading(L, h_end + 1, drop=re.compile(DROP[book]) if book in DROP else None)
    if book in MCGUFFEY:
        for k in range(h_end + 1, nxt):
            if re.fullmatch(r"#{2,}", L[k].strip()):
                front.append(" ".join(L[q].strip() for q in range(h_end + 1, k) if L[q].strip()))
                return first_text(L, k + 1, front)
        for k in range(h_end + 1, nxt):
            if re.match(r"^\s*1\.\s+\S", L[k]):
                pre = [L[q].strip() for q in range(h_end + 1, k) if L[q].strip()]
                if pre:
                    front.append(" ".join(pre))
                return k
        i = next((k for k in range(h_end + 1, nxt) if L[k].strip()), None)
        m = BIO.match(L[i].strip()) if i is not None else None
        if m:                                   # the life, then any paragraph more about the author
            sur = re.sub(r"\s*,$", "", m.group(0).split("(")[0].split(",")[0]).split()[-1]
            while i is not None and i < nxt and (BIO.match(L[i].strip()) or re.match(
                    rf"^(?:\w+\s+){{0,2}}{re.escape(sur)}\b", L[i].strip())):
                p = para_at(L, i)
                front.append(" ".join(L[q].strip() for q in p))
                i = next((k for k in range(p[-1] + 1, nxt) if L[k].strip()), None)
            return first_text(L, i, front) if i is not None else None
    return first_text(L, h_end + 1, front)


def first_text(L, i, front):
    while i < len(L):
        l = L[i]
        t = l.strip()
        if not t:
            i += 1
            continue
        p = para_at(L, i)
        words = " ".join(L[k].strip() for k in p)
        if re.match(r"^SCENE\b", t):                                # a play's stage setting: the editor's, not spoken
            front.append(words)
            i = p[-1] + 1
            continue
        if (is_head(l) and "--" not in t) or not re.search(r"[A-Za-z]", t):   # title run-on, "(CONCLUDED.)", "1775."
            i += 1
            continue
        if re.match(r"^_?(?:BY|By)\s+[A-Z]", t) and len(t) <= 60:    # a byline
            i += 1
            continue
        if re.fullmatch(r"\(.*\)\.?", words) or (t.startswith("[") and words.rstrip(".").endswith("]")):
            if not NOTE.match(t):
                front.append(words)                                 # (_December, 1918_)  [To be spoken ...]
            i = p[-1] + 1
            continue
        after = next((k for k in range(p[-1] + 1, min(len(L), p[-1] + 6)) if L[k].strip()), None)
        if (min(indent(L[k]) for k in p) >= 4 and after is not None
                and indent(L[after]) <= min(indent(L[k]) for k in p) - 3):
            front.append(words)                                     # an indented headnote over the text
            i = p[-1] + 1
            continue
        return i
    return None


def next_heading(L, i, limit=None, drop=None):
    """The first line from i that ends a piece: McGuffey's apparatus, or a
    heading (capitals or a numeral) after two blank lines, or one blank line
    when it is centred."""
    blanks = 0
    end = len(L) if limit is None else min(len(L), limit)
    for j in range(i, end):
        l = L[j]
        if not l.strip() or (drop and drop.search(l)):         # a dropped running head counts as a blank
            blanks += 1
            continue
        if j > i and LESSON.match(l):
            return j
        if j > i and blanks >= 2 and re.fullmatch(r"\s*PART\s+[IVXLC]+\.?\s*", l, re.I):
            nxt = next((L[k] for k in range(j + 1, min(len(L), j + 8)) if L[k].strip()), "")
            if not is_head(nxt):           # "PART II." of a play, then its scene: the piece goes on
                blanks = 0
                continue
            return j                       # a part of the book, then the next heading
        if j > i and blanks and (STOP.match(l) or is_head(l) and (blanks >= 2 or indent(l) >= 10)):
            return j                       # a centred heading (7211's numerals) needs only one blank above it
        blanks = 0
    return end


def credit_line(l, verse, above=""):
    """A signature or credit line at the foot of a piece."""
    t = l.strip()
    if not t or len(t) > 70:
        return False
    if re.match(r"^(?:--|—)\s*\S", t) and len(t) <= 50:
        return True
    if re.fullmatch(r"_[^_]+_\.?", t) or re.match(r"^\((?:Sgd|Signed)\.?\)", t):
        return True
    if (not verse and re.fullmatch(r"(?:(?:Dr|Mr|Mrs|Rev|Hon)\.\s+)?(?:[A-Z][a-z]*\.?\s+){1,3}[A-Z][a-z]+\.?", t)
            and re.search(r"[.!?\"'\u201d\u2019]\s*$", above)):
        return True                                   # a name on its own line at the foot: "Dr. John Aiken"
    return indent(l) >= (30 if verse else 20)


def is_prose(lines):
    """Wrapped prose, not verse: long lines, or lines that often begin
    mid-sentence (a reader's paragraph numbers set aside)."""
    ls = [re.sub(r"^\d{1,2}\.\s+", "", l.strip()) for l in lines if l.strip()]
    if not ls:
        return False
    avg = sum(map(len, ls)) / len(ls)
    lower = sum(1 for l in ls if l[0].islower()) / len(ls)
    indented = sum(1 for l in lines if l.strip() and l.startswith(" ")) / len(ls)
    if indented > 0.6:                     # set in from the margin, as these books set verse (prose stands at it)
        return False
    # long verse lines run over with a hanging indent ("...dying and\n  dead!--"): a paragraph that starts at
    # the margin and goes on set in (a quotation set in whole is not counted)
    base = min(indent(l) for l in lines if l.strip())
    hang, rest, first = 0, 0, None
    for l in lines:
        if not l.strip():
            first = None
        elif first is None:
            first = indent(l)
        elif first == base:
            rest += 1
            hang += indent(l) > first + 1
    if rest and hang / rest > 0.25:
        return False
    return (avg > 58 or (avg > 40 and lower > 0.3) or (lower > 0.2 and indented < 0.1)
            or B._prose("\n".join(ls)))


# ---------------------------------------------------------------------------
# The cut
# ---------------------------------------------------------------------------

def cut(L, book, entry, row, next_row):
    """(text, sel-fields) or (None, why)."""
    fl = (row.get("first_line") or "").strip() if row else entry["first_line"]
    hits = first_line_hits(L, fl) if fl else []
    title = row["title"] if row else entry["title"]
    head = None
    for i in [i for i in hits if not B._in_contents(L, i)] + [i for i in hits if B._in_contents(L, i)]:
        head = heading_above(L, i, title)       # (a play's cast list looks like a contents page: tried last)
        if head:
            break
    if head is None and row:                     # no usable first line: the heading alone
        for k, l in enumerate(L):
            if (is_head(l) and B._clean_heading(re.sub(r"\(\d+\)", "", l)) == B.norm(title)
                    and k > 1 and not L[k - 1].strip()):
                if not B._in_contents(L, k):
                    head = (k, k, True)
                    while head[1] + 1 < len(L) and L[head[1] + 1].strip() and (
                            is_head(L[head[1] + 1]) or not re.search(r"[a-z]", L[head[1] + 1])):
                        head = (k, head[1] + 1, True)
    if head is None:
        return None, "the piece's heading was not found above its first line" if hits else "first line not found in the book"
    if book in MCGUFFEY and not head[2]:
        return None, (f"the heading above it ({L[head[0]].strip()}) is not the piece's: an exercise of excerpts "
                      f"in the reader's introduction, not one piece")
    front = []
    s = text_start(L, head[1], book, front)
    if s is None:
        return None, "no text after the heading"
    drop = re.compile(DROP[book]) if book in DROP else None
    e = next_heading(L, s + 1, s + RUNAWAY, drop)
    if e >= s + RUNAWAY:
        return None, f"no next heading within {RUNAWAY} lines: the cut has run on"
    if e < len(L) and re.match(r"^\s*(?:SCENE|ACT|PART)\b", L[e]):
        return None, "a play in several scenes: the book's headings do not show where it ends"
    body = [k for k in range(s, e) if L[k].strip() and not (drop and drop.search(L[k]))]
    if not body:
        return None, "no text after the heading"
    opening = [L[k] for k in range(s, e) if not (drop and drop.search(L[k]))]
    opening = opening[:next((q for q in range(len(opening)) if sum(1 for x in opening[:q] if x.strip()) >= 20),
                            len(opening))]
    verse = not is_prose(opening)          # the opening twenty lines decide (a closing verse quotation does not)
    signed, last = None, body[-1]
    while len(body) > 2 and credit_line(L[body[-1]], verse, L[body[-2]]) and not (
            not verse and re.match(r"^\s*(?:--|\u2014)", L[body[-1]]) and indent(L[body[-2]]) >= 4):
        # (a "--Byron." under a verse quotation that closes a prose piece is the quotation's, and stays)
        signed, last = (L[body[-1]].strip() + (" " + signed if signed else "")), body[-1]
        body.pop()
    stop = last if signed else e
    rule = {"first_line": S.loose(L[s]), "gap": 99, "keep_headings": True}
    if any(NOTE.match(L[k]) for k in range(s, e)):
        rule["skip_notes"] = NOTE.pattern
    if drop:
        rule["drop"] = DROP[book]
    rule["occurrence"] = [i for i, l in enumerate(L) if re.search(rule["first_line"], l)].index(s)
    if stop < len(L):
        rule["end"] = S.loose(L[stop])
    if not verse:
        rule["reflow"] = True
        if book in MCGUFFEY and re.match(r"^\s*1\.\s+\S", L[s]):
            rule["para_numbers"] = True
        if drop:                                # its blank lines are page breaks, not paragraphs
            rule["join_pages"] = True
            if not rule.get("para_numbers"):
                rule["speakers"] = True
    text, how = B.extract(L, title, rule)
    if text is None:
        return None, how
    # a signature standing over three blank lines and then more text: the cut has run past the piece's end
    for k in range(s, stop - 3):
        if (L[k].strip() and credit_line(L[k], verse) and not any(L[q].strip() for q in range(k + 1, k + 4))
                and any(L[q].strip() for q in range(k + 4, stop))):
            return None, "the cut runs past a signature into what follows"
    # the rule must replay to exactly this cut: its end line is the first line from the start that matches it
    if rule.get("end") and any(re.search(rule["end"], L[k]) for k in range(s, stop)):
        return None, "the stored rule does not replay to the same cut"
    # refusals
    paras = [p for p in text.split("\n\n") if p.strip()]
    if next_row:
        nfl = S.fold(next_row.get("first_line"))
        nt = B.norm(next_row["title"])
        for l in text.split("\n"):
            if (nfl and len(nfl.split()) >= 4 and S.fold(l).startswith(nfl)) or (nt and len(nt) > 3 and B._clean_heading(l) == nt and is_head(l)):
                return None, "the cut runs into the next piece"
    if BIO.match(paras[0]):
        return None, "the cut is the editor's note on the author, not the piece"
    if all(p.lstrip().startswith("[") for p in paras):
        return None, "the cut is an editor's bracketed note"
    if any(p.strip().startswith("[") and p.strip().endswith("]") and len(p.split()) > 8 for p in paras):
        return None, "the cut holds an editor's bracketed note"
    n = len(text.split())
    if n < 400 and (EDITORIAL.search(text) or S.fold(title) in S.fold(S.pool_books().get(book, {}).get("title", ""))):
        return None, "the cut is the book's own front matter (the editor's thanks or a title page), not a piece"
    if n < MIN_WORDS:
        return None, f"the cut is {n} words: too short to be the piece"
    if n > MAX_WORDS:
        return None, f"the cut is {n} words, over the {MAX_WORDS}-word cap for one declamation"
    heading = " ".join(L[k].strip() for k in range(head[0], head[1] + 1))
    m = lesson_of(L, head) if book in MCGUFFEY else None
    out = {"extract": rule, "first_line": L[s].strip(), "form": "verse" if verse else "prose",
           "printed_heading": heading, "lesson": m if m and book in MCGUFFEY else None}
    if front:
        out["headnote"] = " ".join(front)[:600]
    if signed:
        out["signed"] = signed.strip("_ ").strip()
    return text, out


# ---------------------------------------------------------------------------
# Authors
# ---------------------------------------------------------------------------

def author_names(raw):
    """One spelling per author across the layer: the poets table's name when
    it knows the author, else the fullest of the books' spellings that share
    a surname and first initial ("A. Lincoln", "Lincoln" -> "Abraham Lincoln")."""
    poets, exact, by_sur = S.poet_table()
    canon = {a: S.canonical(a, poets, exact, by_sur) for a in raw}
    groups = {}
    for a, (n, _) in canon.items():
        if n == "Anonymous":
            continue
        toks = S.fold(n).split()
        if toks:
            groups.setdefault(toks[-1], set()).add(n)
    out = {}
    for a, (n, died) in canon.items():
        toks = S.fold(n).split()
        if n != "Anonymous" and n not in poets and toks:
            same = [m for m in groups[toks[-1]]
                    if len(toks) == 1 or S.fold(m).split()[0][0] == toks[0][0] or len(S.fold(m).split()) == 1]
            full = [m for m in same if len(S.fold(m).split()) > 1 and "." not in m.split()[0]]
            if len(toks) == 1 and len({S.fold(m).split()[0] for m in full}) != 1:
                full = []                                       # "Adams": which Adams? keep the book's spelling
            if full:
                n = max(full, key=lambda m: (len(m), m))
        out[a] = (n, died)
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

NUMBERED = re.compile(r"^(?:LESSON\s+)?([IVXLC]+|\d+)\.(?:\s+\S.*)?$")


def lesson_of(L, head):
    """A McGuffey piece's lesson number: "LESSON XL." above the title (Second and Third Readers), else
    the numeral of its own heading -- unless the heading is one of a lesson's numbered pieces (I., II.,
    ... under "XXIV. SHORT SELECTIONS IN PROSE."), which take the lesson's number."""
    for k in range(head[0], max(-1, head[0] - 30), -1):  # past the vocabulary list under the lesson line
        if LESSON.match(L[k]):
            return LESSON.match(L[k]).group(0).split()[1].rstrip(".")
        if k < head[0] and NUMBERED.match(L[k].strip()) and is_head(L[k]):
            break
    num = lambda h: int(h) if h.isdigit() else roman(h)  # noqa: E731
    m = NUMBERED.match(L[head[0]].strip())
    if not m or not is_head(L[head[0]]):
        return None
    k, want = head[0], num(m.group(1))
    while want > 1:                                   # up through the lesson's earlier pieces, II. then I.
        k = next((q for q in range(k - 1, max(-1, k - 400), -1) if NUMBERED.match(L[q]) and is_head(L[q])), None)
        if k is None or num(NUMBERED.match(L[k]).group(1)) != want - 1:
            return m.group(1)
        want -= 1
    parent = next((q for q in range(k - 1, max(-1, k - 40), -1) if NUMBERED.match(L[q]) and is_head(L[q])), None)
    if parent is not None and not NUMBERED.match(L[parent]).group(1).isdigit() \
            and num(NUMBERED.match(L[parent]).group(1)) > 1:    # "XXIV. SHORT SELECTIONS" over "I."
        return NUMBERED.match(L[parent]).group(1)
    return m.group(1)


def roman(s):
    v = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    return sum(-v[c] if k + 1 < len(s) and v[c] < v[s[k + 1]] else v[c] for k, c in enumerate(s))


def title_from_heading(h):
    """A printed heading as a title: numeral, page number and final stop off, capitals to title case."""
    t = re.sub(r"\(\d+\)", "", h)
    t = re.sub(r"^\s*(?:[IVXLC]+|\d+)\.\s+", "", t).strip().rstrip(".").strip()
    if t.isupper():
        ws = t.lower().split()
        t = " ".join(w if k and w in SMALL else w[:1].upper() + w[1:] for k, w in enumerate(ws))
    return t


def base_title(rows, r):
    """The title of the piece a "The Same Continued" row goes on from."""
    by_order = {x["order"]: x for x in rows}
    k = r["order"] - 1
    while k in by_order and re.match(r"^the same\b", by_order[k]["title"], re.I):
        k -= 1
    t = by_order[k]["title"] if k in by_order else r["title"]
    return t.rstrip(", ")


def same_piece(a, b):
    """Two printings of one speech: the same ten opening words, one perhaps
    after a salutation the other leaves off ("Mr. President, It is natural ...").
    The caller also asks that the authors agree."""
    a, b = S.fold(a).split(), S.fold(b).split()
    return len(a) >= 10 and len(b) >= 10 and any(a[d:d + 10] == b[:10] or b[d:d + 10] == a[:10] for d in range(4))


def decl_books(entries):
    return sorted({n for e in entries for n in e["books"]})


def fetch_and_pin(books):
    """Fetch each book's mirror copy and pin it under the book's sources.json
    entry, as `mirror` (raw_url, sha256, encoding)."""
    pool = {b["pg_id"]: b for b in json.load(open(os.path.join(S.POOL, "sources.json"), encoding="utf-8"))
            if b.get("pg_id")}
    path = os.path.join(B.DATA, "sources.json")
    src = json.load(open(path, encoding="utf-8"))
    ok = True
    for n in books:
        s = src["books"].get(str(n))
        url = pool.get(n, {}).get("raw_url")
        if not s or not url:
            print(f"  #{n}: not pinned in sources.json, or no mirror URL")
            ok = False
            continue
        p = B.book_path(str(n), mirror=True)
        if s.get("mirror") and os.path.exists(p):
            continue
        blob = open(p, "rb").read() if os.path.exists(p) else S.get(url)
        if not blob:
            print(f"  FAILED {n}: {url}")
            ok = False
            continue
        sha = hashlib.sha256(blob).hexdigest()
        if s.get("mirror") and s["mirror"]["sha256"] != sha:
            print(f"  #{n}: the mirror file is not the pinned one ({sha[:12]})")
            ok = False
            continue
        try:
            blob.decode("utf-8")
            enc = "utf-8"
        except UnicodeDecodeError:
            enc = "cp1252"
        B.write_atomic(p, blob)
        s["mirror"] = {"raw_url": url, "sha256": sha, "encoding": enc}
        print(f"  pinned mirror {n:>6}  {len(blob):>9,} bytes  {enc}  {s['title'][:50]}")
        time.sleep(0.5)
    B.write_atomic(path, (json.dumps(src, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    return ok


def other_layers():
    """fold(first 8 words of the first line) -> citation, for every poem in the other layers."""
    seen = {}
    for layer in B.LAYERS:
        if layer == LAYER:
            continue
        for r in B.read_jsonl(os.path.join(B.SEL, f"{layer}.jsonl")):
            if r.get("first_line"):
                seen.setdefault(S.words(r["first_line"], 8), B.citation(r))
    for t in B.read_parts(os.path.join(B.DATA, "texts")):
        first = next((l for l in t["text"].split("\n") if l.strip()), "")
        seen.setdefault(S.words(first, 8), t["citation"])
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="fetch and pin the books' mirror copies first")
    a = ap.parse_args()
    pool = [e for e in B.read_jsonl(os.path.join(S.POOL, "pool.jsonl")) if e["kind"] == "prose"]
    entries = pool + PLAN_EXTRA
    books = decl_books(entries)
    if a.fetch and not fetch_and_pin(books):
        print("  some mirror copies failed; rerun (resumable)")
    sources = B.load_sources()["books"]
    pbooks = S.pool_books()
    rows = S.book_rows()
    names = author_names({e.get("author") or "" for e in entries} | set(HEADING_AUTHOR.values()))
    taken = other_layers()
    loaded = {}

    def lines_of(n):
        if n not in loaded:
            s = sources.get(str(n))
            loaded[n] = B.read_book(str(n), s, mirror=True)[0] if s else None
        return loaded[n]

    out, used, by_first = [], {}, {}
    merged = {}          # (book, order) -> the row a printing was merged into (None: a continuation; False: its own row)
    stats = {"pieces": len(entries), "cut": 0, "link": 0, "elsewhere": [], "twice": []}
    for e in entries:
        ordered = sorted(e["books"], key=lambda n: (0 if S.edition_year(pbooks.get(n, {})) else 1, n))
        tried, got = [], None
        for n in ordered:
            b = pbooks.get(n)
            src = sources.get(str(n))
            if not b or not src or src.get("copyrighted_header") or not src.get("mirror"):
                tried.append(f"#{n} has no pinned mirror copy")
                continue
            L = lines_of(n)
            if L is None:
                tried.append(f"#{n} not fetched")
                continue
            rs = rows.get(n, [])
            r = S.member_row(e, rs) if e.get("pool_id") else None
            if e.get("pool_id") and not r:
                tried.append(f"#{n} has no row for it")
                continue
            nxt = next((x for x in rs if x["order"] == r["order"] + 1), None) if r else None
            text, info = cut(L, n, e, r, nxt)
            if text is None:
                tried.append(f"#{n}: {info}")
                continue
            got = (n, b, r, text, info)
            break
        cont = None
        if got and got[2] and re.match(r"^the same\b", e["title"], re.I):
            k = got[2]["order"] - 1
            while (got[0], k) in merged and merged[(got[0], k)] is None:
                k -= 1
            cont = merged.get((got[0], k))
        if got and got[2]:
            merged[(got[0], got[2]["order"])] = None if re.match(r"^the same\b", e["title"], re.I) else False
        if cont:                                    # the rest of a printing already merged into another row
            cont["other_printings"].append({"gutenberg": got[0], "pool_id": e.get("pool_id")})
            stats["twice"].append((e.get("pool_id"), e["title"], cont.get("pool_id")))
            continue
        lead = S.words(got[4]["first_line"], 8) if got else None
        if lead and lead in taken:
            stats["elsewhere"].append((e.get("pool_id"), e["title"], taken[lead]))
            continue
        who = names.get(e.get("author") or HEADING_AUTHOR.get(e.get("pool_id")) or "", ("Anonymous", None))[0]
        twin = next((f for f in by_first.values() if got and same_piece(f["first_line"], got[4]["first_line"])
                     and (who == "Anonymous" or f["poet"] == "Anonymous"
                          or S.fold(who).split()[-1] == S.fold(f["poet"]).split()[-1]
                          or {who, f["poet"]} in ONE_MAN)), None)
        if twin:
            first = twin
            first.setdefault("other_printings", []).append({"gutenberg": got[0], "pool_id": e.get("pool_id")})
            first["books"] = sorted(set(first["books"]) | set(e["books"]))
            first["n_books"] = len(first["books"])
            first["grade_hint"]["audiences"] = sorted(set(first["grade_hint"]["audiences"]) | set(e.get("audiences") or []))
            stats["twice"].append((e.get("pool_id"), e["title"], first.get("pool_id")))
            if got[2]:
                merged[(got[0], got[2]["order"])] = first
            continue
        author = e.get("author") or HEADING_AUTHOR.get(e.get("pool_id")) or ""
        poet, died = names.get(author, ("Anonymous", None))
        if poet == "Anonymous" and got and got[4].get("signed"):
            sig = re.sub(r"^(?:--|—)\s*", "", got[4]["signed"]).strip(" ._")
            if 2 <= len(sig.split()) <= 5 and not re.search(r"\d|permission|from\b", sig, re.I):
                poet, died = names.get(sig) or S.canonical(sig, *S.poet_table())
        n0 = got[0] if got else ordered[0]
        b0 = pbooks.get(n0, {})
        sel = {"poet": poet, "poet_died": died, "title": e["title"], "year": None, "term": None, "order": None,
               "pool_id": e.get("pool_id"), "n_books": e["n_books"], "books": e["books"],
               "grade_hint": {"audiences": e.get("audiences") or []}}
        if n0 in MCGUFFEY:
            sel["grade_hint"]["mcguffey_reader"] = MCGUFFEY[n0]
        named = PLAN.get(e.get("pool_id")) or e.get("named_in_plan")
        if named:
            sel["named_in_plan"] = named
        sel["pd_source"] = {"gutenberg": n0, "work": S.work_name(b0) if b0 else f"PG #{n0}",
                            "edition_year": S.edition_year(b0), "copy": "mirror"}
        if got:
            n, b, r, text, info = got
            if r and S.fold(r["title"]) != S.fold(e["title"]):
                sel["printed_title"] = r["title"]
            if e["title"].endswith(","):            # the pool cut the heading off at its line break
                sel["title"] = title_from_heading(info["printed_heading"])
            same = re.match(r"^the same\b\s*(concluded|continued)?", e["title"], re.I)
            if same and r:                          # "THE SAME CONCLUDED.": the piece it goes on from
                sel["printed_title"] = e["title"]
                sel["title"] = f"{base_title(rows.get(n, []), r)}, {(same.group(1) or 'continued').lower()}"
            elif re.search(r"\((?:CONCLUDED|CONTINUED)\.?\)", info["printed_heading"]):
                sel["title"] += ", " + re.search(r"\((CONCLUDED|CONTINUED)", info["printed_heading"]).group(1).lower()
            lesson = info.pop("lesson", None)
            sel.update(info)
            if n in MCGUFFEY and lesson:
                sel["grade_hint"]["lesson"] = lesson
            sel["form"] = info["form"]
            sel["notes"] = (f"Cut from #{n} ({b['title']}) at \"{info['first_line'][:70]}\"; "
                            f"in {e['n_books']} of the pool's books." + (f" {e['note']}" if e.get("note") else ""))
            by_first[S.words(info["first_line"], 8)] = sel
            stats["cut"] += 1
        else:
            sel["form"] = "prose"
            sel["no_text_reason"] = "no clean cut: " + "; ".join(tried)[:300]
            sel["notes"] = f"In {e['n_books']} of the pool's books; not cut." + (f" {e['note']}" if e.get("note") else "")
            stats["link"] += 1
        sel["layer"] = LAYER
        cit = B.citation(sel)
        if cit in used:
            sel["variant"] = B.slug(S.words(sel.get("first_line") or e.get("first_line") or "", 4)) or e.get("pool_id")
            cit = B.citation(sel)
            if cit in used:
                sel["variant"] = e.get("pool_id") or "plan"
                cit = B.citation(sel)
        used[cit] = True
        del sel["layer"]
        out.append(sel)
    B.write_atomic(OUT, B.jsonl(out))
    print(f"  {stats['pieces']} pieces ({len(pool)} prose rows in the pool, {len(PLAN_EXTRA)} from the plan): "
          f"{len(out)} rows, {stats['cut']} cut, {stats['link']} linked out")
    print(f"  {len(stats['elsewhere'])} already in another layer; {len(stats['twice'])} a second printing of a row")
    for p, t, c in stats["elsewhere"]:
        print(f"    elsewhere  {p}  {t[:50]}  -> {c}")
    for p, t, f in stats["twice"]:
        print(f"    twice      {p}  {t[:50]}  -> {f}")
    print(f"  wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
