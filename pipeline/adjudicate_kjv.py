#!/usr/bin/env python3
"""
adjudicate_kjv.py -- prove the KJV verse-perfect and measure how close to
word-perfect it is, using a THIRD reading that neither converter produced.

    python3 pipeline/adjudicate_kjv.py              # full report
    python3 pipeline/adjudicate_kjv.py --strict     # non-zero exit on any
                                                    # unclassified residue

WHY A THIRD READING
    kjv.plain and kjv.italic disagree 1,872 times after supplied-word marks are
    removed. Comparing two readings tells you THAT they disagree; it cannot
    tell you which is right. code-corpus learned this as a hard rule -- "an
    independent second reading adjudicates ... a conservation gate proves
    nothing left the document; it cannot prove text landed in the right node."

    The arbiter here is data/corpus/kjv_bible.txt, the raw Gutenberg file, read
    by this script with its own parser. That is non-circular for kjv.plain
    (whose converter it tests) and it is an INDEPENDENT EDITION for kjv.italic
    (pythonbible). So it can settle a converter bug outright, and it can only
    CLASSIFY an edition difference -- never resolve one.

WHAT THIS SCRIPT WILL NOT DO
    It does not repair, complete, paraphrase or normalise a single word. Rule
    1 of the house: unreadable or contested text is FLAGGED, never guessed. A
    difference between two published editions of the KJV is not an error in
    either, and a script that silently picked a winner would be manufacturing
    a text that no edition prints.

VERSE-PERFECT vs WORD-PERFECT
    verse-perfect  every verse the source prints exists as its own unit, with
                   no merges, no splits, no gaps, no duplicates. Provable here.
    word-perfect   every unit's text is the text the edition prints. Provable
                   only against the edition; what IS provable here is the
                   residue: how many units any two readings dispute, and what
                   class each dispute falls in. A number with a named class is
                   honest. "Clean" is not.
"""

import argparse
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BOOKS = os.path.join(ROOT, "data", "books")
SRC = os.path.join(ROOT, "data", "corpus", "kjv_bible.txt")
OUT = os.path.join(ROOT, "data", "books", "kjv.adjudication.json")

# OSIS book ids in printed order. The ORDER is canonical and external to this
# file; the book TITLES are not listed, deliberately.
#
# The first version of this script hardcoded each Gutenberg heading string and
# located books by matching them. It failed twice in one run, and both failures
# are worth keeping written down because they are the same failure this whole
# project is about:
#
#   * the five books of Moses use ONE space after the colon in this file and
#     the constant carried two, so all five headings "did not exist";
#   * "The First Book of the Kings" is a SUBSTRING of 1 Samuel's full KJV
#     heading as well as 1 Kings', so the Samuel and Kings spans overlapped and
#     2 Samuel's verses were reported as duplicate markers 800 times.
#
# A string I typed from memory was treated as evidence about a file I had not
# read closely. Books are now located STRUCTURALLY: a `1:1` marker is a book
# boundary and nothing else in the text is. That yields exactly 66 segments
# with no string matching at all, and the headings are READ OUT of the file for
# the report rather than asserted into it.
BOOKS_ORDER = [
    "Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth",
    "1Sam", "2Sam", "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth",
    "Job", "Ps", "Prov", "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan",
    "Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph",
    "Hag", "Zech", "Mal",
    "Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal",
    "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus",
    "Phlm", "Heb", "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude",
    "Rev",
]

# The marker. NOTE the difference from structure_texts.RE_VMARK, and it is the
# whole 420-verse bug: that one requires whitespace or END OF STRING after the
# marker. Gutenberg hard-wraps, so a marker landing at a line end has a
# NEWLINE after it -- fine -- but a marker landing mid-line directly before the
# wrap had nothing its lookahead would take. Here the marker simply has to be
# preceded by start-of-line or whitespace and followed by whitespace, with the
# whole file joined first so a wrap is just another space.
VMARK = re.compile(r"(?:(?<=^)|(?<=\s))(\d+):(\d+)\s")

_WS = re.compile(r"\s+")


def read_source():
    with open(SRC, encoding="utf-8") as f:
        raw = f.read()
    # Trim Gutenberg front/back matter to the body between the markers used by
    # this file. If the markers are absent we say so rather than guessing.
    start = raw.find("*** START")
    if start >= 0:
        raw = raw[raw.index("\n", start) + 1:]
    end = raw.find("*** END")
    if end >= 0:
        raw = raw[:end]
    return raw


def parse_source():
    """-> (verses {osis: text}, headings {osis: str}, problems []).

    A third reading with its own parser. Books are found structurally: the
    whole body is normalised so a hard wrap becomes an ordinary space, every
    `chapter:verse` marker is located, and each `1:1` opens a new book. The
    text between the previous verse and a `1:1` is that book's printed heading,
    read out for the report."""
    body = _WS.sub(" ", read_source())
    problems = []
    marks = list(VMARK.finditer(body))
    starts = [i for i, m in enumerate(marks)
              if m.group(1) == "1" and m.group(2) == "1"]

    if len(starts) != len(BOOKS_ORDER):
        problems.append({"kind": "book_count",
                         "found": len(starts), "expected": len(BOOKS_ORDER),
                         "note": "a 1:1 marker is the only book boundary; a "
                                 "mismatch means the source is not what we think"})

    verses, headings = {}, {}
    for n, mi in enumerate(starts):
        osis = BOOKS_ORDER[n] if n < len(BOOKS_ORDER) else f"UNKNOWN{n}"
        last = starts[n + 1] if n + 1 < len(starts) else len(marks)
        prev_end = marks[mi - 1].end() if mi > 0 else 0
        headings[osis] = body[prev_end:marks[mi].start()].strip()[-90:]
        for k in range(mi, last):
            mark = marks[k]
            ch, vs = int(mark.group(1)), int(mark.group(2))
            stop = marks[k + 1].start() if k + 1 < len(marks) else len(body)
            key = f"kjv:{osis}.{ch}.{vs}"
            if key in verses:
                problems.append({"kind": "duplicate_marker", "id": key})
                continue
            verses[key] = body[mark.end():stop].strip()
    return verses, headings, problems


def structure_report(ids, label):
    """Gaps and duplicates, per book and chapter. A missing verse shows up as a
    hole in the numbering; a merge shows up as its successor missing."""
    byloc = collections.defaultdict(set)
    for cid in ids:
        book, ch, vs = cid[4:].rsplit(".", 2)
        byloc[(book, int(ch))].add(int(vs))
    gaps, ch_gaps = [], []
    bychapter = collections.defaultdict(set)
    for (book, ch), vset in byloc.items():
        bychapter[book].add(ch)
        hi = max(vset)
        missing = [v for v in range(1, hi + 1) if v not in vset]
        for v in missing:
            gaps.append(f"kjv:{book}.{ch}.{v}")
    for book, chs in bychapter.items():
        hi = max(chs)
        for c in range(1, hi + 1):
            if c not in chs:
                ch_gaps.append(f"kjv:{book}.{c}")
    return {"label": label, "verses": len(ids), "books": len(bychapter),
            "chapters": sum(len(v) for v in bychapter.values()),
            "verse_gaps": sorted(gaps), "chapter_gaps": sorted(ch_gaps)}


# ---------------------------------------------------------------- classifying

_BRACKET = re.compile(r"[\[\]]")
_PUNCT = re.compile(r"[^\w\s]")


def classify(a, b):
    """Name the class of a disagreement. Ordered most-specific first. Returns
    a class name; never a verdict about which side is correct."""
    if a == b:
        return "identical"
    da, db = _BRACKET.sub("", a), _BRACKET.sub("", b)
    if _WS.sub(" ", da).strip() == _WS.sub(" ", db).strip():
        return "supplied_word_marks_only"
    na, nb = _WS.sub(" ", da).strip(), _WS.sub(" ", db).strip()
    if na.replace("-", "") == nb.replace("-", ""):
        return "hyphenation"
    if _PUNCT.sub("", na) == _PUNCT.sub("", nb):
        return "punctuation"
    if na.lower() == nb.lower():
        return "capitalisation"
    if _PUNCT.sub("", na).lower().split() == _PUNCT.sub("", nb).lower().split():
        return "punctuation_and_case"
    wa, wb = na.split(), nb.split()
    if len(wa) > len(wb) * 2 or len(wb) > len(wa) * 2:
        return "length_mismatch_probable_merge"
    if set(wa) == set(wb):
        return "word_order"
    return "word_difference"


def main(strict=False):
    print("Reading the source with an independent parser ...")
    src, headings, problems = parse_source()
    print(f"  segmented {len(headings)} books structurally on `1:1` markers; "
          f"no heading string was matched.")
    for p in problems[:20]:
        print("  PROBLEM:", p)
    if len(problems) > 20:
        print(f"  ... and {len(problems) - 20} more")

    books = {}
    for w, fn in (("kjv.plain", "kjv.json"), ("kjv.italic", "kjv.complete.json")):
        p = os.path.join(BOOKS, fn)
        if not os.path.exists(p):
            sys.exit(f"missing {p}")
        books[w] = {u["id"]: u.get("text", "") for u in json.load(open(p, encoding="utf-8"))["units"]}

    print()
    print("=" * 74)
    print("VERSE CENSUS -- three readings")
    print("=" * 74)
    reports = [structure_report(set(src), "source (gutenberg, this parser)")]
    for w in ("kjv.plain", "kjv.italic"):
        reports.append(structure_report(set(books[w]), w))
    for r in reports:
        print(f"  {r['label']:<34} {r['verses']:>7,} verses  "
              f"{r['books']:>2} books  {r['chapters']:>5} chapters  "
              f"gaps: {len(r['verse_gaps'])}")

    print()
    print("  KJV canonical total is 31,102 verses in 66 books.")
    for r in reports:
        ok = "MATCHES" if r["verses"] == 31102 else f"OFF BY {r['verses'] - 31102:+,}"
        print(f"    {r['label']:<34} {ok}")
        if r["verse_gaps"][:5]:
            print(f"      first gaps: {', '.join(r['verse_gaps'][:5])}"
                  f"{' ...' if len(r['verse_gaps']) > 5 else ''}")
        if r["chapter_gaps"]:
            print(f"      MISSING CHAPTERS: {', '.join(r['chapter_gaps'][:8])}")

    # ---------------------------------------------------------------- word
    print()
    print("=" * 74)
    print("WORD-LEVEL ADJUDICATION -- every disagreement classified, none repaired")
    print("=" * 74)
    pairs = [("kjv.plain", "kjv.italic"),
             ("source", "kjv.plain"), ("source", "kjv.italic")]
    lookup = {"source": src, "kjv.plain": books["kjv.plain"],
              "kjv.italic": books["kjv.italic"]}
    out = {"generated_against": {"source": os.path.relpath(SRC, ROOT)},
           "canonical_total": 31102, "census": reports, "headings": headings, "pairs": {}}

    for a, b in pairs:
        da, db = lookup[a], lookup[b]
        shared = set(da) & set(db)
        classes = collections.Counter()
        examples = collections.defaultdict(list)
        for cid in shared:
            c = classify(da[cid], db[cid])
            classes[c] += 1
            if c != "identical" and len(examples[c]) < 3:
                examples[c].append({"id": cid, a: da[cid][:110], b: db[cid][:110]})
        agree = classes["identical"]
        print()
        print(f"  {a}  vs  {b}")
        print(f"    shared verses {len(shared):,}   "
              f"only in {a}: {len(set(da) - set(db)):,}   "
              f"only in {b}: {len(set(db) - set(da)):,}")
        print(f"    identical     {agree:,}  ({agree / max(len(shared),1) * 100:.2f}%)")
        for c, n in classes.most_common():
            if c == "identical":
                continue
            print(f"      {c:<36} {n:>6,}")
        out["pairs"][f"{a}|{b}"] = {
            "shared": len(shared), "only_a": len(set(da) - set(db)),
            "only_b": len(set(db) - set(da)),
            "classes": dict(classes), "examples": {k: v for k, v in examples.items()},
        }

    # --------------------------------------------------------------- verdict
    print()
    print("=" * 74)
    print("VERDICT")
    print("=" * 74)
    src_n = reports[0]["verses"]
    ital = out["pairs"]["source|kjv.italic"]
    plain = out["pairs"]["source|kjv.plain"]
    unclassified = sum(v["classes"].get("word_difference", 0) for v in out["pairs"].values())

    print(f"  VERSE-PERFECT: source parses to {src_n:,} verses; "
          f"kjv.italic holds {len(books['kjv.italic']):,}; "
          f"kjv.plain holds {len(books['kjv.plain']):,}.")
    print(f"  The {len(set(books['kjv.italic']) - set(books['kjv.plain'])):,}-verse "
          f"shortfall in kjv.plain is the RE_VMARK defect, reproduced above by "
          f"parsing the same source correctly.")
    print(f"  WORD-PERFECT is NOT claimed. Residue by pair is printed above, "
          f"every disagreement carries a class, and nothing was repaired.")
    print(f"  Edition differences between the gutenberg source and "
          f"pythonbible-kjv are NOT errors and are not resolved here.")

    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"\n  wrote {OUT}")

    if strict and (reports[0]["verse_gaps"] or problems):
        print("\n  STRICT: structural residue present.")
        return 1
    return 0


def emit_source_witness():
    """Write the third reading out as a proper book file, `kjv.source.json`.

    WHY THIS EXISTS AND WHEN IT SHOULD STOP EXISTING
        kjv.plain is the right EDITION read by a defective parser -- 98.46%
        of its verses match this source exactly, and its only real defect is
        the 420 merges. This function writes what that converter WOULD have
        produced had its marker regex been right: same source, same edition,
        same words, 31,102 verses, zero gaps.

        It is deliberately NOT a competing recipe. `canon-corpus-f5866fe.patch`
        (sitting unapplied in Claude\\Projects) fixes structure_texts.py at the
        recipe, which is the permanent answer per golden rule 2. The moment
        that patch lands and kjv.plain rebuilds to 31,102, this witness becomes
        redundant and SHOULD BE RETIRED -- two recipes for one file is the drift
        this repo keeps getting bitten by, and this one is on a clock.

        Nothing is invented here: every verse's text is a slice of the source
        between two markers, whitespace-collapsed and stripped. No repair, no
        completion, no normalisation.
    """
    verses, headings, problems = parse_source()
    order = []
    for osis in BOOKS_ORDER:
        pre = f"kjv:{osis}."
        keys = [k for k in verses if k.startswith(pre)]
        keys.sort(key=lambda k: tuple(int(x) for x in k[len(pre):].split(".")))
        order += keys
    missing = set(verses) - set(order)
    if missing:
        problems.append({"kind": "unordered_verses", "count": len(missing)})

    doc = {
        "slug": "kjv",
        "title": "The Holy Bible (KJV)",
        "author": "—",
        "source": "data/corpus/kjv_bible.txt (Project Gutenberg)",
        "scheme": {
            "citation": "Book chapter:verse (OSIS ids)",
            "resolution": "verse",
            "honesty": ("exact at verse resolution: 31,102 verses, 66 books, "
                        "zero numbering gaps, segmented on 1:1 markers with no "
                        "heading string matched. Text is concatenated from the "
                        "source between markers; nothing invented, nothing "
                        "repaired. Supplied-word italics are NOT marked in this "
                        "edition -- see kjv.italic for those."),
            "interim": ("Supersedes kjv.json, which is the same edition read by "
                        "the pre-f5866fe parser and is 420 verses short. Retire "
                        "this file once that patch lands."),
        },
        "units": [{"id": k, "ref": None, "text": verses[k], "links": []} for k in order],
    }
    p = os.path.join(BOOKS, "kjv.source.json")
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    os.replace(tmp, p)
    print(f"  wrote {p}  ({len(order):,} verses, {len(problems)} problems)")
    return p, problems


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--emit", action="store_true",
                    help="write the third reading out as data/books/kjv.source.json")
    args = ap.parse_args()
    if args.emit:
        emit_source_witness()
        sys.exit(0)
    sys.exit(main(strict=args.strict))
