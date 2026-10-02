#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""
build_vulgate_versification.py -- the Clementine Vulgate -> KJV verse map, so
a verse cited in the Vulgate's own numbering (vulgate:Ps.50.3) can land on the
kjv: unit that holds the same text (kjv:Ps.51.1).

    python3 pipeline/build_vulgate_versification.py --fetch    # TVTMS + the Clementine, pinned
    python3 pipeline/build_vulgate_versification.py            # build data/versification/vulgate-kjv.json
    python3 pipeline/build_vulgate_versification.py --check    # rebuild: byte-identical, every invariant holds
    python3 pipeline/build_vulgate_versification.py --measure  # do the mapped verses name the same people?
    python3 pipeline/build_vulgate_versification.py --audit-douay  # the Douay's English against the KJV's

WHY THIS EXISTS
    convert_vulgate gives every verse an id in the Vulgate's OWN numbering and
    links it to nothing, because the numbers are not the KJV's: the Psalms
    are counted as in the Greek (Vulgate Ps 50 = KJV Ps 51) with the title in
    verse 1, chapters break in other places (Vulgate Jonah 2:1 = KJV 1:17),
    and Daniel and Esther carry the Greek additions. This is the map.

THE SOURCE: STEPBible TVTMS (CC BY 4.0), the same pinned file as
build_versification.py (the Hebrew map for BDB). TVTMS gives, block by block,
the verse numbering of several traditions side by side: "English KJV",
"Hebrew", "Latin", "Greek", and, where Bibles of one tradition disagree among
themselves, extra columns ("Latin2", "LatinUndivided", ...). Each column has
TESTS that tell a Bible which column it follows ("Ps.9:39=Last": chapter 9
has 39 verses; "Est.12:6=Exist"; "Gen.6:1<Gen.6:2": fewer words).

    TVTMS's "Latin" is not the Clementine, letter for letter. So the build does
    not assume a column: in each block it RUNS the tests against the
    Clementine's own text (verse list and word counts) and follows the column
    that passes. Latin-family columns are preferred; where none passes, any
    other column that does (TVTMS has no Latin column for the NT blocks that
    split 2 Cor 13 or Rev 12); where nothing passes and nothing is assumed,
    the block is reported, not guessed. Tests the Clementine cannot answer
    (subverse counts: it has no subverses) are skipped, and counted.

THE CHECK: the Clementine's own verse list (fetch_sources.VULGATE, PD,
pinned) against the KJV verses in the uid registry. The build refuses to
write unless:
  * every Clementine verse lands on a kjv: unit, or on a KJV psalm title
    (which has no unit), or is named as having no KJV verse for a stated
    reason (a book or a Greek addition the KJV's canon does not hold);
  * every KJV verse is reached from some Clementine verse, or the followed
    column says the Clementine has no verse for it.
--measure is the content check: TVTMS is a map of numbers, so it is tested
against the words. Where the two numberings differ, the Clementine verse's
proper names (the house table, data/lemmas/proper-names, with Hitchcock's
King James spellings) are looked for in the KJV verse the map names and in
the KJV verse with the same number (measured 2026-10-02: 84.9% against
12.4%). Its neighbour check found Neh 7 and 1 Chr 11 (HOUSE_ROWS). It also
flags Judg 20, left as is: there Jerome's sentences break a few words off the
KJV's, so each Clementine verse straddles the end of the KJV verse of the same
number, which is still the verse that holds most of it. Names are sparse in
poetry and prophecy, so the check sees least where a name is rarest.

WHAT THE MAP SAYS
    `map` lists only the Clementine verses whose KJV reference differs; a
    verse not in it, and in no other table, has the same number in the KJV.
    A list value is one Clementine verse holding the text of several KJV
    verses. A ".title" target is the KJV's unnumbered psalm superscription.
    Several Clementine verses may map to one KJV verse (the KJV verse is the
    longer). `no_kjv_verse` names every Clementine verse with no KJV verse,
    by range, with why. `kjv_without_vulgate_verse` names the KJV verses the
    Clementine has no verse for. `vulgate_chapters` is the Clementine's verse
    count per chapter, so a reference that is no Clementine verse is caught.
    Rights: the derived subset carries TVTMS's attribution and
    `redistribute_whole: false`, as bhs-kjv.json does.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_versification as BV  # noqa: E402  (the pinned TVTMS, fetch helpers)
import fetch_sources as FS        # noqa: E402  (the pinned Clementine)
import structure_texts as S       # noqa: E402  (its book table and verse reader)

ROOT = BV.ROOT
OUT = os.path.join(ROOT, "data", "versification", "vulgate-kjv.json")
VDIR = os.path.join(BV.CORPUS, "vulgate")
NAMES = os.path.join(ROOT, "data", "lemmas", "proper-names", "names.jsonl")
KJV_TSV = os.path.join(ROOT, "data", "greppable", "kjv.tsv")

# TVTMS book codes (SIL/Paratext; TVTMS also writes "PSA", "1CO") -> OSIS,
# for the 66 books the KJV witness holds and the Clementine's other seven.
TV2OSIS = dict(BV.TV2OSIS, **{
    "Mat": "Matt", "Mrk": "Mark", "Luk": "Luke", "Jhn": "John", "Act": "Acts",
    "Rom": "Rom", "1Co": "1Cor", "2Co": "2Cor", "Gal": "Gal", "Eph": "Eph",
    "Php": "Phil", "Col": "Col", "1Th": "1Thess", "2Th": "2Thess", "1Ti": "1Tim",
    "2Ti": "2Tim", "Tit": "Titus", "Phm": "Phlm", "Heb": "Heb", "Jas": "Jas",
    "1Pe": "1Pet", "2Pe": "2Pet", "1Jn": "1John", "2Jn": "2John", "3Jn": "3John",
    "Jud": "Jude", "Rev": "Rev",
    "Tob": "Tob", "Jdt": "Jdt", "Wis": "Wis", "Sir": "Sir", "Bar": "Bar",
    "1Ma": "1Macc", "2Ma": "2Macc",
})
TV_UPPER = {k.upper(): v for k, v in TV2OSIS.items()}
# KJV-apocrypha codes TVTMS uses in its English column for the Greek additions.
KJV_APOCRYPHA = {"S3Y": "the Song of the Three Children", "Sus": "Susanna",
                 "Bel": "Bel and the Dragon", "Ade": "the Rest of Esther"}

# Column preference inside a block, when several pass their tests.
LATIN_ORDER = ["Latin", "Latin*", "LatinUndivided", "Latin2", "Latin2*", "Latin2-DRA"]

# Where the Clementine has text the KJV witness does not: the deuterocanonical
# books (the KJV of 1611 printed them as Apocrypha; this witness has the 66)
# and the Greek additions inside Esther and Daniel. These are the ONLY places a
# Clementine verse may have no KJV verse; anything else is a hard stop.
NOT_IN_KJV_BOOKS = {
    "Tob": "Tobias: not in the KJV's canon (printed as Apocrypha, Tobit)",
    "Jdt": "Judith: not in the KJV's canon (printed as Apocrypha)",
    "Wis": "Wisdom: not in the KJV's canon (printed as Apocrypha)",
    "Sir": "Ecclesiasticus: not in the KJV's canon (printed as Apocrypha)",
    "Bar": "Baruch: not in the KJV's canon (printed as Apocrypha; Bar 6 is its Epistle of Jeremy)",
    "1Macc": "1 Machabees: not in the KJV's canon (printed as Apocrypha)",
    "2Macc": "2 Machabees: not in the KJV's canon (printed as Apocrypha)",
}
NOT_IN_KJV_RANGES = [   # (book, first (ch, v), last (ch, v), why)
    ("Esth", (10, 4), (16, 24),
     "the Greek additions to Esther, gathered at the end by Jerome; the KJV prints "
     "them as Apocrypha (the Rest of Esther)"),
    ("Dan", (3, 24), (3, 90),
     "the Song of the Three Children, a Greek addition; the KJV prints it as Apocrypha"),
    ("Dan", (13, 1), (13, 65), "Susanna (13:1-64) and the opening of Bel (13:65), "
     "Greek additions; the KJV prints them as Apocrypha"),
    ("Dan", (14, 1), (14, 42), "Bel and the Dragon, a Greek addition; the KJV prints it "
     "as Apocrypha"),
]


# Where the Clementine divides verses in places no TVTMS column does. Each row
# was read in both texts. `words` must stand in the Clementine verse (the build
# checks it) and is the Latin of the LAST KJV verse listed, so a changed source
# fails loudly. Found by the invariants (Ps 15, John 11, 2 Cor 1: a KJV verse
# nothing reached) and by --measure's neighbour check (Neh 7, 1 Chr 11: a
# list of names whose verse breaks fall elsewhere, the count unchanged).
_NEH7 = ("Neh 7:42-48: the Clementine breaks this list of returning families "
         "mid-entry, so its verses straddle the KJV's; the chapter keeps 73 verses")
_1CHR11 = ("1 Chr 11:32-35: the Clementine's breaks in the list of David's mighty men "
           "fall elsewhere (its 32 holds KJV 32-33); the chapter count is unchanged")
_DOUAY_AUDIT = ("found by --audit-douay (the Douay-Rheims English, which keeps the Clementine's "
                "verse breaks, aligned against the KJV's) and read in the Latin: Jerome "
                "re-divides the passage, so the KJV verse of the TVTMS number holds none of it")
HOUSE_ROWS = {
    "Neh.7.42": (["Neh.7.42", "Neh.7.43"], "Levit", _NEH7),
    "Neh.7.43": (["Neh.7.43"], "Cedmihel", _NEH7),
    "Neh.7.44": (["Neh.7.43", "Neh.7.44"], "Cantores", _NEH7),
    "Neh.7.45": (["Neh.7.44"], "filii Asaph", _NEH7),
    "Neh.7.46": (["Neh.7.45"], "Janitores", _NEH7),
    "Neh.7.47": (["Neh.7.46"], "Nathin", _NEH7),
    "Neh.7.48": (["Neh.7.47", "Neh.7.48"], "filii Lebana", _NEH7),
    "1Chr.11.32": (["1Chr.11.32", "1Chr.11.33"], "Eliaba Salabonites", _1CHR11),
    "1Chr.11.33": (["1Chr.11.34"], "Filii Assem", _1CHR11),
    "1Chr.11.34": (["1Chr.11.35"], "Ahiam", _1CHR11),
    "1Chr.11.35": (["1Chr.11.35"], "Eliphal", _1CHR11),
    **{v: (es, w, _DOUAY_AUDIT) for v, (es, w) in {
        # Jerome's Latin re-divides these passages (often abridging): the verse
        # TVTMS's number points to holds none of the Clementine verse's text.
        "Exod.38.25": (["Exod.38.25", "Exod.38.26"], "sexcentis tribus millibus"),
        "Exod.38.26": (["Exod.38.27"], "centum talenta argenti"),
        "Exod.38.27": (["Exod.38.27"], "Centum bases"),
        "Lev.15.20": (["Lev.15.19"], "Omnis qui tetigerit eam"),
        "Lev.15.21": (["Lev.15.20"], "in quo dormierit vel sederit"),
        "Lev.15.22": (["Lev.15.21"], "Qui tetigerit lectum ejus"),
        "Lev.15.23": (["Lev.15.22", "Lev.15.23"], "Omne vas, super quo"),
        "Num.15.12": (["Num.15.11", "Num.15.12"], "per singulos boves"),
        "Num.15.15": (["Num.15.15", "Num.15.16"], "Unum præceptum"),
        "Num.15.16": (["Num.15.17"], "Locutus est Dominus ad Moysen"),
        "Num.15.17": (["Num.15.18"], "Loquere filiis Isra"),
        "Num.27.3": (["Num.27.3", "Num.27.4"], "Cur tollitur nomen illius"),
        "Num.27.4": (["Num.27.5"], "Retulitque Moyses causam"),
        "Num.27.5": (["Num.27.6"], "Qui dixit ad eum"),
        "Num.27.6": (["Num.27.7"], "Justam rem postulant"),
        "Num.27.7": (["Num.27.8"], "Ad filios autem Isra"),
        "Num.35.23": (["Num.35.22", "Num.35.23"], "inimicitiis quidquam horum"),
        "Deut.6.12": (["Deut.6.11"], "et comederis, et saturatus"),
        "Deut.6.13": (["Deut.6.12", "Deut.6.13"], "cave diligenter ne obliviscaris"),
        "Ps.108.17": (["Ps.109.16"], "persecutus est hominem inopem"),
        "Ps.108.18": (["Ps.109.17", "Ps.109.18"], "induit maledictionem sicut vestimentum"),
        "Hos.6.2": (["Hos.6.1"], "quia ipse cepit, et sanabit nos"),
        "Hos.6.3": (["Hos.6.2", "Hos.6.3"], "in die tertia suscitabit nos"),
        "Luke.9.43": (["Luke.9.42"], "increpavit Jesus spiritum immundum"),
        "Luke.9.44": (["Luke.9.43", "Luke.9.44"], "Ponite vos in cordibus"),
        "Luke.17.35": (["Luke.17.35", "Luke.17.36"], "duo in agro"),
        "Luke.17.36": (["Luke.17.37"], "Ubi Domine"),
        "2Tim.4.8": (["2Tim.4.8", "2Tim.4.9"], "Festina ad me venire cito"),
        "2Tim.4.9": (["2Tim.4.10"], "Demas enim me reliquit"),
        "Rev.20.7": (["Rev.20.7", "Rev.20.8"], "Gog, et Magog"),
        "Rev.20.8": (["Rev.20.9"], "circuierunt castra sanctorum"),
        "Rev.20.9": (["Rev.20.10"], "missus est in stagnum"),
    }.items()},
    "Matt.5.4": (["Matt.5.5"], "Beati mites",
                 "the Vulgate orders the beatitudes meek, then mourn; the KJV mourn, then "
                 "meek. Same numbers, swapped text: TVTMS maps numbers, so it has no row"),
    "Matt.5.5": (["Matt.5.4"], "Beati qui lugent",
                 "the Vulgate orders the beatitudes meek, then mourn; the KJV mourn, then "
                 "meek. Same numbers, swapped text: TVTMS maps numbers, so it has no row"),
    "Ps.15.10": (["Ps.16.10", "Ps.16.11"], "Notas mihi fecisti vias vit",
                 "KJV 16:11 'Thou wilt shew me the path of life'; TVTMS's Latin has a "
                 "verse 15:11 the Clementine does not"),
    "John.11.56": (["John.11.56", "John.11.57"], "Dederant autem pontifices",
                   "KJV 11:57 'Now both the chief priests and the Pharisees had given a "
                   "commandment'; the Clementine ends John 11 at verse 56"),
    "2Cor.1.23": (["2Cor.1.23", "2Cor.1.24"], "non quia dominamur fidei vestr",
                  "KJV 1:24 'Not for that we have dominion over your faith'; the "
                  "Clementine ends 2 Corinthians 1 at verse 23"),
}
# Row types that record whether MANUSCRIPTS carry a verse, not how a Bible
# numbers it. Read only from a Latin-family column, never from another.
MANUSCRIPT_ROWS = {"TextMayBeMissing", "PassageMissing"}


def _stop(msg):
    raise SystemExit(f"HARD STOP: {msg}")


# ---------------------------------------------------------------- inputs

def fetch():
    BV.fetch()   # TVTMS (and the WLC, which the Hebrew map needs; harmless here)
    print(f"vulgate: {FS.fetch_vulgate()}")
    print(f"douay: {FS.fetch_douay()}")   # for --audit-douay


def _require_pins():
    if not os.path.exists(BV.TVTMS_PATH) or BV.sha256(BV.TVTMS_PATH) != BV.TVTMS_SHA256:
        _stop("TVTMS missing or changed. Run --fetch.")
    if not all(os.path.exists(os.path.join(VDIR, b + ".lat")) for b in FS.VULGATE["books"]):
        _stop("the Clementine is not fetched. Run --fetch.")
    if FS.vulgate_digest(VDIR) != FS.VULGATE["pin"]:
        _stop("the Clementine's files differ from the pin")


def vulgate_verses():
    """{'Ps.50.3': plain text} for every Clementine verse, in book order."""
    out = {}
    for b in FS.VULGATE["books"]:
        osis = S.VULGATE_BOOKS[b][0]
        with open(os.path.join(VDIR, b + ".lat"), encoding="cp1252") as f:
            for line in f:
                m = S.RE_VULG_LINE.match(line.rstrip("\r\n"))
                if m:
                    out[f"{osis}.{m.group(1)}.{m.group(2)}"] = S.vulgate_layout(m.group(3))[0]
    return out


def kjv_verses():
    uids = json.load(open(BV.REGISTRY, encoding="utf-8"))["uids"]
    return {k[4:] for k in uids if k.startswith("kjv:")}


BOOKS = [S.VULGATE_BOOKS[b][0] for b in FS.VULGATE["books"]]
BOOK_ORDER = {b: i for i, b in enumerate(BOOKS)}


def osis_key(ref):
    b, ch, v = ref.split(".")
    return (BOOK_ORDER.get(b, 99), int(ch), -1 if v == "title" else int(v))


def chapters_of(verses):
    out = {}
    for r in verses:
        b, ch, v = r.split(".")
        out[f"{b}.{ch}"] = max(out.get(f"{b}.{ch}", 0), int(v))
    return out


# ---------------------------------------------------------------- TVTMS blocks

def tvtms_blocks(path=BV.TVTMS_PATH):
    """The condensed section as blocks: {line, title, cols, tests, rows}.
    tests: {column: [condition, ...]}; rows: [(line, type, [cell per column])].
    A block's columns come from its `$` line or a later `BIBLES` row; its
    tests from `TEST:` rows (a cell per column) or from lines naming columns
    ("Latin + Greek<TAB> & Ps.9:39=Last & ..."). Lines opening with # are
    commented out in the source and skipped, as build_versification does."""
    lines = open(path, encoding="utf-8-sig").read().split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("#DataStart(Condensed)"))
    end = next(i for i, l in enumerate(lines) if i > start and l.startswith("#DataEnd(Condensed)"))
    blocks, cur = [], None
    for n, line in enumerate(lines[start + 1:end], start + 2):
        c = [x.strip() for x in line.split("\t")]
        t = c[0]
        if t.startswith("$"):
            cur = {"line": n, "title": t, "cols": [x for x in c[1:] if x],
                   "tests": {}, "named": [], "rows": []}
            blocks.append(cur)
            continue
        if cur is None or not t or t[0] in "#',>":
            continue
        if t == "BIBLES":
            cur["cols"] = [x for x in c[1:] if x]
            continue
        if t.startswith("TEST") or "TEST:" in t:
            for col, cell in zip(cur["cols"], c[1:]):
                if cell:
                    cur["tests"].setdefault(col, []).extend(
                        p.strip() for p in cell.split("&") if p.strip())
            continue
        if len(c) > 1 and c[1].startswith("&"):
            names = [x.strip() for x in re.split(r"\+", t)]
            conds = [p.strip() for p in c[1].split("&") if p.strip()]
            cur["named"].append((names, conds))
            continue
        cur["rows"].append((n, t, c[1:]))
    for b in blocks:   # named tests bind to columns once the BIBLES row is known
        for names, conds in b.pop("named"):
            for nm in names:
                col = next((x for x in b["cols"] if x.strip() == nm.strip()), None)
                if col:
                    b["tests"].setdefault(col, []).extend(conds)
    return blocks


RE_CELLREF = re.compile(
    r"^(?:([1-4]?[A-Za-z]{2,3})\.)?(\d+):(\d+|Title)(?:\.(\d+))?"
    r"(?:-(?:(\d+):)?(\d+)(?:\.(\d+))?)?$")


def expand(cell, sizes):
    """A TVTMS cell -> [(book, ch, v, sub)] (v 'title' for a psalm title, sub
    None for a whole verse). None when the cell names no verse (Absent,
    NoVerse, Empty) or cannot be read. `sizes` gives chapter lengths, for
    ranges that cross a chapter ("Gen.31:55--32:32" style, written 31:55-32:32)."""
    cell = re.sub(r"\s*\[[^\]]*\]|\s*\([^)]*\)", "", cell).strip()
    if not cell:
        return None
    out, book = [], None
    for part in (p.strip() for p in cell.split(";")):
        part = part.replace("--", "-")
        m = RE_CELLREF.match(part)
        if not m:
            return None
        b, ch, a, sa, ch2, z, sz = m.groups()
        b = b or book
        if b is None:
            return None
        book = b
        osis = TV_UPPER.get(b.upper()) or (b if b in KJV_APOCRYPHA else None)
        if osis is None:
            return None
        ch = int(ch)
        if a == "Title":
            out.append((osis, ch, "title", None))
            continue
        a = int(a)
        if z is None:
            out.append((osis, ch, a, int(sa) if sa else None))
        elif ch2 is not None:            # crosses a chapter
            for c in range(ch, int(ch2) + 1):
                lo = a if c == ch else 1
                hi = int(z) if c == int(ch2) else sizes.get(f"{osis}.{c}", 0)
                out += [(osis, c, v, None) for v in range(lo, hi + 1)]
        elif sa is not None:             # a run of subverses of one verse
            out += [(osis, ch, a, s) for s in range(int(sa), int(sz or sa) + 1)]
        else:
            out += [(osis, ch, v, None) for v in range(a, int(z) + 1)]
    return out


# ---------------------------------------------------------------- the tests

RE_COND = re.compile(r"^(.+?)(=|<|>)(.+)$")
RE_TREF = re.compile(r"^([1-4]?[A-Za-z]{2,3})\.(\d+):(\d+|TextBeforeV1)(?:\.(\d+))?(?:\*(\d+))?$")


class Undecidable(Exception):
    pass


def _tref(s):
    m = RE_TREF.match(s.strip())
    if not m:
        raise Undecidable(s)
    b, ch, v, sub, mul = m.groups()
    osis = TV_UPPER.get(b.upper())
    if osis is None:
        raise Undecidable(s)
    return osis, int(ch), v, sub, int(mul or 1)


def _words(side, vul):
    total = 0
    for term in side.split("+"):
        osis, ch, v, sub, mul = _tref(term)
        if v == "TextBeforeV1" or (sub not in (None, "0")):
            raise Undecidable(term)
        total += mul * len(vul.get(f"{osis}.{ch}.{v}", "").split())
    return total


def holds(cond, vul, sizes):
    """Does TVTMS condition `cond` hold for the Clementine? Raises
    Undecidable for what its text cannot answer (subverses, letter chapters)."""
    cond = cond.replace(" ", "")
    m = RE_COND.match(cond)
    if not m:
        raise Undecidable(cond)
    lhs, op, rhs = m.groups()
    if op == "=":
        osis, ch, v, sub, _ = _tref(lhs)
        what = rhs.lower()
        if v == "TextBeforeV1":
            # The Clementine prints a psalm's title as its verse 1: never before it.
            if what == "exist":
                return False
            if what == "notexist":
                return True
            raise Undecidable(cond)
        if sub is not None:
            raise Undecidable(cond)
        key = f"{osis}.{ch}.{v}"
        if what == "last":
            return sizes.get(f"{osis}.{ch}") == int(v)
        if what == "exist":
            return bool(vul.get(key, "").strip())
        if what == "notexist":
            return not vul.get(key, "").strip()
        raise Undecidable(cond)
    return _words(lhs, vul) < _words(rhs, vul) if op == "<" else _words(lhs, vul) > _words(rhs, vul)


def choose_column(block, vul, sizes, tally):
    """(column, how, failed) for `block`: the column the Clementine follows.
    A column passes when every test the Clementine can answer holds, and at
    least one could be answered. Latin-family columns are preferred, then any
    other that passes. When none passes and the block has a Latin column, the
    Latin column with the fewest failed tests is followed and its failures
    are recorded: the invariants and --measure then judge it, and HOUSE_ROWS
    carries what it gets wrong. A block with no Latin column that nothing
    passes is left alone (the Clementine keeps the KJV's numbers there)."""
    cols, tests = block["cols"], block["tests"]
    cands = [c for c in cols if not c.startswith("English")]
    score = {}
    for col in cands:
        failed, decided = [], 0
        for cond in tests.get(col, []):
            try:
                r = holds(cond, vul, sizes)
            except Undecidable:
                tally["undecidable"] += 1
                continue
            decided += 1
            if not r:
                failed.append(cond)
        score[col] = (failed, decided)
    passing = [c for c in cands if score[c][1] and not score[c][0]]
    latin = [c for c in LATIN_ORDER if c in passing]
    if latin:
        return latin[0], "tests", []
    if passing:
        return passing[0], "tests (no Latin column passes)", []
    lat = [c for c in LATIN_ORDER if c in cands]
    if not lat:
        return None, "no column passes; no Latin column", []
    if not tests.get(lat[0]):
        return lat[0], "no tests for the Latin column", []
    best = min(lat, key=lambda c: (len(score[c][0]), LATIN_ORDER.index(c)))
    return best, "fallback: nearest Latin column", score[best][0]


# ---------------------------------------------------------------- build

def _in_ranges(ref):
    b, ch, v = ref.split(".")
    if b in NOT_IN_KJV_BOOKS:
        return NOT_IN_KJV_BOOKS[b]
    for book, lo, hi, why in NOT_IN_KJV_RANGES:
        if b == book and lo <= (int(ch), int(v)) <= hi:
            return why
    return None


def _ref(x):
    return f"{x[0]}.{x[1]}.{x[2]}"


def block_pairs(blk, col, kcol, vsizes, ksizes, latin=True):
    """(pairs, absent) that one block says for the followed column:
    pairs [(Clementine verse, KJV verse)], absent {KJV verse: (note, line,
    Clementine verse holding its text or None)}. A KJV subverse past .0 is a
    Greek addition the KJV witness does not print: its target ends in '+'."""
    cols = blk["cols"]
    ik, il = cols.index(kcol), cols.index(col)
    pairs, absent = [], {}
    for n, typ, cells in blk["rows"]:
        if max(ik, il) >= len(cells) or (not latin and typ in MANUSCRIPT_ROWS):
            continue
        kc, lc = cells[ik], cells[il]
        E = expand(kc, ksizes)
        if not E or all(e[0] in NOT_IN_KJV_BOOKS for e in E):
            continue
        Ek = []
        for e in E:
            k = _ref(e) + ("+" if e[3] not in (None, 0) else "")
            if k not in Ek:
                Ek.append(k)
        if any(k.endswith("+") for k in Ek) and any(not k.endswith("+") for k in Ek):
            Ek = [k for k in Ek if not k.endswith("+")]
        m = re.match(r"^Absent(?:\s*\[=(.+)\])?$", lc)
        if m or lc in ("NoVerse", "Empty"):
            # The Clementine has no verse of this number for the KJV verse;
            # with [=X] its text is inside Clementine verse X.
            held = sorted({_ref(x) for x in (expand(m.group(1), vsizes) or [])}) if m and m.group(1) else []
            for e in Ek:
                if e.endswith("+"):
                    continue
                absent[e] = (f"{typ}: {col} {lc}", n, held[0] if held else None)
                for h in held:
                    pairs.append((h, e))
            continue
        L = expand(lc, vsizes)
        if not L:
            continue
        Lv = []
        for x in L:   # subverses are pieces of one verse: the verse is the unit
            if _ref(x) not in Lv:
                Lv.append(_ref(x))
        if len(Ek) == len(Lv):
            pairs += list(zip(Lv, Ek))
        elif len(Lv) == 1:
            pairs += [(Lv[0], e) for e in Ek]
        elif len(Ek) == 1:
            pairs += [(l, Ek[0]) for l in Lv]
        else:
            _stop(f"TVTMS line {n}: {kc!r} vs {col} {lc!r} do not align")
    return pairs, absent


def build_map(vul, kjv):
    """Clementine verse -> [KJV verse, ...] for every verse TVTMS speaks of.
    Blocks followed by a Latin-family column are applied first. A block
    followed by another column (the NT blocks about a verse some Greek
    manuscripts lack, e.g. Matt 17:21) only tests whether a verse NUMBER
    exists, which a renumbered Clementine chapter can pass by accident; so
    it may not touch a Clementine or KJV verse a Latin block already placed."""
    vsizes, ksizes = chapters_of(vul), chapters_of(kjv)
    tally = {"undecidable": 0, "pairs_yielded_to_a_latin_block": 0}
    v2e, kjv_absent, followed, left_alone = {}, {}, {}, []
    staged = []
    for blk in tvtms_blocks():
        kcol = next((c for c in blk["cols"] if c.startswith("English KJV")), None)
        if kcol is None:
            continue
        code = re.match(r"^\$([1-4]?[A-Za-z]{2,3})\.", blk["title"])
        book = TV_UPPER.get(code.group(1).upper()) if code else None
        if book is None or book in NOT_IN_KJV_BOOKS:
            continue    # Greek Esther (Esg), 1-4 Esdras, the deuterocanon: nothing to map
        col, how, failed = choose_column(blk, vul, vsizes, tally)
        if col is None:
            left_alone.append(f"line {blk['line']} {blk['title']}: {how}")
            continue
        f = {"line": blk["line"], "column": col, "how": how}
        if failed:
            f["failed_tests"] = failed
        followed[blk["title"]] = f
        staged.append((col in LATIN_ORDER, blk["title"], block_pairs(blk, col, kcol, vsizes, ksizes,
                                                                    col in LATIN_ORDER)))

    placed_v, placed_e = set(), set()
    for latin in (True, False):
        for is_latin, title, (pairs, absent) in staged:
            if is_latin != latin:
                continue
            for v, e in pairs:
                if not latin and (v in placed_v or e in placed_e):
                    tally["pairs_yielded_to_a_latin_block"] += 1
                    continue
                got = v2e.setdefault(v, [])
                if e not in got:
                    got.append(e)
            for e, (note, n, held) in absent.items():
                if not latin and e in placed_e:
                    tally["pairs_yielded_to_a_latin_block"] += 1
                    continue
                kjv_absent[e] = {"tvtms": note, "line": n}
                if held:
                    kjv_absent[e]["text_in_vulgate"] = held
        if latin:
            placed_v = set(v2e)
            placed_e = {e for es in v2e.values() for e in es} | set(kjv_absent)
    for v, (es, words, _why) in HOUSE_ROWS.items():
        if words not in vul.get(v, ""):
            _stop(f"HOUSE_ROWS {v}: {words!r} is not in the Clementine's verse")
        v2e[v] = list(es)
    for v in v2e:
        v2e[v].sort(key=lambda e: osis_key(e.rstrip("+")))
    return v2e, kjv_absent, followed, left_alone, tally


def compute():
    _require_pins()
    vul, kjv = vulgate_verses(), kjv_verses()
    v2e, kjv_absent, followed, left_alone, tally = build_map(vul, kjv)

    target, no_kjv, nowhere, clash = {}, {}, [], []
    for v in vul:
        why = _in_ranges(v)
        if why:
            no_kjv[v] = why
            real = [e for e in v2e.get(v, []) if not e.endswith("+")
                    and e.split(".")[0] not in KJV_APOCRYPHA and e in kjv]
            if real:
                clash.append((v, real))
            continue
        es = [e for e in v2e.get(v, [v]) if not e.endswith("+")]
        es = [e for e in es if e.split(".")[0] not in KJV_APOCRYPHA]
        bad = [e for e in es if not e.endswith(".title") and e not in kjv]
        if not es or bad:
            nowhere.append((v, v2e.get(v, [v])))
            continue
        target[v] = es
    if nowhere:
        _stop(f"{len(nowhere)} Clementine verse(s) land on no KJV verse and are in no "
              f"stated exception, first {nowhere[:8]}")
    if clash:
        _stop(f"{len(clash)} verse(s) in a stated no-KJV range that TVTMS maps to a KJV "
              f"verse, first {clash[:5]}")
    reached = {e for es in target.values() for e in es}
    orphans = sorted(kjv - reached - set(kjv_absent), key=osis_key)
    if orphans:
        _stop(f"{len(orphans)} KJV verse(s) reached from no Clementine verse, first {orphans[:8]}")
    return {"target": target, "no_kjv": no_kjv, "reached": reached, "kjv_absent": kjv_absent,
            "followed": followed, "left_alone": left_alone, "tally": tally,
            "vul": vul, "kjv": kjv}


def _runs(refs):
    """Consecutive verses of one chapter as 'Book.ch.a-b' runs."""
    out, cur = [], None
    for r in refs:
        b, ch, v = r.split(".")
        if cur and cur[0] == (b, ch) and int(v) == cur[2] + 1:
            cur[2] = int(v)
        else:
            if cur:
                out.append(cur)
            cur = [(b, ch), int(v), int(v)]
    if cur:
        out.append(cur)
    return [f"{b}.{ch}.{a}" + (f"-{z}" if z != a else "") for (b, ch), a, z in out]


def build():
    r = compute()
    vul, kjv, target = r["vul"], r["kjv"], r["target"]
    diff = {}
    for v in sorted(target, key=osis_key):
        es = target[v]
        if es != [v]:
            diff[v] = es[0] if len(es) == 1 else es
    # The Clementine verses with no KJV verse, as runs, grouped by reason.
    by_why = {}
    for v in sorted(r["no_kjv"], key=osis_key):
        by_why.setdefault(r["no_kjv"][v], []).append(v)
    whole = {why: b for b, why in NOT_IN_KJV_BOOKS.items()}
    no_kjv = [{"verses": [f"{whole[why]} (the whole book)"] if why in whole else _runs(vs),
               "count": len(vs), "why": why} for why, vs in by_why.items()]
    absent = {e: r["kjv_absent"][e]["tvtms"] for e in sorted(r["kjv_absent"], key=osis_key)
              if e in kjv and e not in r["reached"]}
    merged = {e: r["kjv_absent"][e]["text_in_vulgate"] for e in sorted(r["kjv_absent"], key=osis_key)
              if e in kjv and "text_in_vulgate" in r["kjv_absent"][e]}
    unusual = {t: f for t, f in r["followed"].items() if f["column"] != "Latin" or f["how"] != "tests"}
    titles = sum(1 for es in target.values() for e in es if e.endswith(".title"))
    many = {}
    for v, es in target.items():
        for e in es:
            many.setdefault(e, []).append(v)
    return {
        "note": ("Clementine Vulgate -> KJV verse numbers. Only the Clementine verses whose "
                 "KJV reference differs are in `map`; any other verse not named in "
                 "`no_kjv_verse` has the same number in the KJV. A list value is one "
                 "Clementine verse holding text of several KJV verses; several Clementine "
                 "verses may share one KJV verse. A '.title' target is the KJV's unnumbered "
                 "psalm superscription, which has no kjv: unit id. vulgate_chapters is the "
                 "Clementine's verse count per chapter. Built by "
                 "pipeline/build_vulgate_versification.py; do not hand-edit."),
        "from": "vulgate", "to": "kjv",
        "source": {
            "name": "TVTMS - Translators Versification Traditions with Methodology for "
                    "Standardisation (STEPBible.org)",
            "url": "https://github.com/STEPBible/STEPBible-Data",
            "commit": BV.TVTMS_COMMIT, "sha256": BV.TVTMS_SHA256,
            "columns_read": ["English KJV", "the column whose tests the Clementine passes, "
                             "block by block (usually 'Latin'); see blocks_not_plain_latin"],
            "changes": ("Reformatted: only the condensed section is read, for the books the "
                        "KJV witness holds; in each block one column is followed, chosen by "
                        "running TVTMS's own tests on the Clementine; rows where the two agree "
                        "are dropped; book codes become OSIS; ranges are expanded to single "
                        "verses and subverses folded into their verse. house_rows adds the "
                        "correspondences TVTMS does not have; nothing of TVTMS's is altered."),
        },
        "rights": {
            "license": "CC BY 4.0",
            "attribution": ("Data created by www.STEPBible.org based on work at Tyndale "
                            "House Cambridge (CC BY 4.0)"),
            "source_url": "https://github.com/STEPBible/STEPBible-Data",
            "redistribute_whole": False,
        },
        "checked_against": {
            "name": "the Clementine Vulgate Project's text (PD), as fetch_sources.VULGATE pins it",
            "url": f"https://github.com/{FS.VULGATE['repo']}", "commit": FS.VULGATE["commit"],
            "sha256": FS.VULGATE["pin"],
            "vulgate_verses": len(vul), "kjv_verses": len(kjv),
            "vulgate_verses_landing_on_no_kjv_verse_unexplained": 0,
            "kjv_verses_reached_from_no_vulgate_verse": len(absent),
            "tvtms_blocks_followed": len(r["followed"]),
            "tvtms_tests_the_clementine_cannot_answer": r["tally"]["undecidable"],
            "pairs_from_non_latin_blocks_yielding_to_a_latin_block":
                r["tally"]["pairs_yielded_to_a_latin_block"],
        },
        "counts": {"differing_vulgate_verses": len(diff), "to_psalm_titles": titles,
                   "spanning_several_kjv_verses": sum(isinstance(x, list) for x in diff.values()),
                   "kjv_verses_shared_by_several_vulgate_verses":
                       sum(len(vs) > 1 for e, vs in many.items()),
                   "vulgate_verses_with_no_kjv_verse": len(r["no_kjv"]),
                   "house_rows": len(HOUSE_ROWS)},
        "blocks_not_plain_latin": unusual,
        "house_rows": {v: {"kjv": es, "why": why} for v, (es, _w, why) in HOUSE_ROWS.items()},
        "vulgate_chapters": chapters_of(sorted(vul, key=osis_key)),
        "no_kjv_verse": no_kjv,
        "kjv_text_in_another_vulgate_verse": merged,
        "kjv_without_vulgate_verse": absent,
        "map": diff,
    }


# ---------------------------------------------------------------- measure

def _norm(w):
    """A name's letters with the regular Latin/English spelling differences
    folded (j=i=y, z=s, ph=f, th=t, sh=s, ch=c, k=c, ae=oe=e, doubled letters
    single): Sion and Zion, Josaphat and Jehoshaphat's tail, meet."""
    w = w.lower().replace("æ", "ae").replace("œ", "oe").replace("ë", "e").replace("-", "")
    for a, b in (("ae", "e"), ("oe", "e"), ("ph", "f"), ("th", "t"), ("sh", "s"),
                 ("ch", "c"), ("j", "i"), ("y", "i"), ("z", "s"), ("k", "c"), ("h", "")):
        w = w.replace(a, b)
    return re.sub(r"(.)\1", r"\1", w)


def name_index():
    """{Clementine form: {normalised KJV spelling}} from the house names table,
    for the names Hitchcock (the KJV's spellings) knows."""
    out = {}
    with open(NAMES, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            terms = {_norm(h["term"]) for h in d["hitchcock"] if " " not in h["term"]}
            if terms:
                for form in d["forms"]:
                    out[form] = terms
    return out


def kjv_words():
    out = {}
    with open(KJV_TSV, encoding="utf-8") as f:
        for line in f:
            i, _, t = line.rstrip("\n").partition("\t")
            if i.startswith("kjv:"):
                out[i[4:]] = {_norm(w) for w in re.findall(r"[A-Za-z-]+", t)}
    return out


def vulgate_names(text, names):
    out = set()
    for w in re.findall(r"[A-Za-zæœëÆŒ]+", text):
        w = w.lower().replace("æ", "ae").replace("œ", "oe").replace("ë", "e")
        for c in (w, w[:-3] if w.endswith("que") else None):
            if c and c in names:
                out |= names[c]
                break
    return out


def measure(r=None, show=40):
    """Where the map moves a verse, are the Clementine verse's names in the
    KJV verse the map names, or in the KJV verse with the same number?"""
    r = r or compute()
    names, kw = name_index(), kjv_words()
    n = {"same": 0, "same_hit": 0, "moved": 0, "moved_hit": 0, "moved_samenum_hit": 0}
    misses = []
    for v, es in r["target"].items():
        es = [e for e in es if not e.endswith(".title")]     # the KJV prints no title text here
        ns = vulgate_names(r["vul"][v], names)
        if not es or not ns:
            continue
        hit = any(ns & kw.get(e, set()) for e in es)
        if es == [v]:
            n["same"] += 1
            n["same_hit"] += hit
            continue
        n["moved"] += 1
        n["moved_hit"] += hit
        n["moved_samenum_hit"] += bool(ns & kw.get(v, set()))
        if not hit:
            misses.append((v, es, sorted(ns)))
    print("Clementine verses with a proper name the KJV spells (Hitchcock):")
    print(f"  numbered as in the KJV: {n['same']:,}; the name is in that KJV verse: "
          f"{n['same_hit']:,} ({n['same_hit'] / max(n['same'], 1):.1%})")
    print(f"  moved by the map:       {n['moved']:,}; in the KJV verse the map names: "
          f"{n['moved_hit']:,} ({n['moved_hit'] / max(n['moved'], 1):.1%}); in the KJV verse "
          f"with the same number: {n['moved_samenum_hit']:,} "
          f"({n['moved_samenum_hit'] / max(n['moved'], 1):.1%})")
    for m in misses[:show]:
        print("  miss:", *m)
    # The neighbour check: a verse whose names miss the KJV verse it lands on
    # but stand in the KJV verse next to it. Scattered, it is two verses that
    # share a name; several in one chapter, it is a run of verse breaks the
    # map does not know (how Neh 7 and 1 Chr 11 were found).
    near = {}
    for v, es in r["target"].items():
        es = [e for e in es if not e.endswith(".title")]
        ns = vulgate_names(r["vul"][v], names)
        if not es or not ns or any(ns & kw.get(e, set()) for e in es):
            continue
        b, ch, x = es[0].split(".")
        if any(ns & kw.get(f"{b}.{ch}.{int(x) + d}", set()) for d in (-1, 1)):
            near.setdefault(f"{b}.{ch}", []).append(v)
    runs = {c: vs for c, vs in near.items() if len(vs) >= 3}
    print(f"names found only in a neighbouring KJV verse: {sum(map(len, near.values()))} "
          f"verses; chapters with 3 or more: {len(runs)}")
    for c, vs in sorted(runs.items(), key=lambda kv: osis_key(kv[0] + ".1")):
        print(f"  {c}: {', '.join(vs)}")
    return n, misses, runs


# ---------------------------------------------------------------- audit (Douay)

_STOP = set("the and of to in that he his him they them a i is was for unto shall be with it "
            "not all thou thy thee me my which by from upon as are but ye you their have this "
            "at o will said were there when on or so out an no who your had her she hath we "
            "our us also then because what into one let".split())
_BEADS = [(1, 1, 0), (1, 2, .05), (2, 1, .05), (1, 0, .3), (0, 1, .3), (2, 2, .1),
          (1, 3, .1), (3, 1, .1)]


def _etoks(t):
    return {w[:5] for w in re.findall(r"[a-z]+", t.lower()) if w not in _STOP and len(w) > 2}


def _dice(a, b):
    return 2 * len(a & b) / (len(a) + len(b)) if a and b else 0.0


def audit_douay(show=80):
    """The weak spot of --measure is that names are rare in poetry and prophecy.
    The Douay-Rheims is the Clementine in English, verse for verse (its own
    breaks are structure_texts.DOUAY_ROWS), so its English can be aligned
    against the KJV's everywhere: a monotonic alignment (1-1, 1-2, 2-1, 2-2,
    1-3, 3-1 and gaps; Dice overlap of content-word stems) inside a band of
    ten verses around where the map puts each verse. A Douay verse whose
    aligned KJV verses share nothing with the ones the map gives is listed,
    with its neighbours, for reading. Not a gate: titles, Jerome's paraphrase
    and lists of names make honest noise. What reading found went into
    HOUSE_ROWS (Jerome's re-divisions) and DOUAY_ROWS (the Douay's own).
    Measured 2026-10-02 after both: 31,083 verses aligned, 10 listed, all read
    and left: Matt 5:4-5 (a swap, which a monotonic alignment cannot draw; the
    map has it right), Ps 5, Ps 72 and Exod 39 (verses that straddle, the map
    naming the KJV verse that holds most), Num 33 (a list of stations whose
    words repeat), Ps 71:1 (a title)."""
    drc = os.path.join(BV.CORPUS, "douay", "DRC.json")
    if not os.path.exists(drc) or BV.sha256(drc) != FS.DOUAY["sha256"]:
        _stop("the Douay-Rheims is not fetched (or differs from its pin). Run --fetch.")
    book = S.convert_douay(drc, FS.VULGATE["books"], FS.DOUAY["sha256"])
    kj = {}
    with open(KJV_TSV, encoding="utf-8") as f:
        for line in f:
            i, _, t = line.rstrip("\n").partition("\t")
            if i.startswith("kjv:"):
                kj[i[4:]] = t
    kord = list(kj)
    kidx = {k: i for i, k in enumerate(kord)}
    KT = [_etoks(kj[k]) for k in kord]
    units = [u for u in book["units"] if u["kjv"]["resolved"]]
    by_book = {}
    for u in units:
        by_book.setdefault(u["id"].split(":")[1].split(".")[0], []).append(u)
    flagged = []
    for bk, us in by_book.items():
        ks = [i for i, k in enumerate(kord) if k.split(".")[0] == bk]
        k0, M = ks[0], len(ks)
        DT = [_etoks(u["text"]) for u in us]
        guess = [kidx[u["kjv"]["target"][4:]] - k0 for u in us]
        n = len(us)
        best = {(0, 0): (0.0, None)}
        for i in range(n + 1):
            c = guess[min(i, n - 1)]
            for j in range(max(0, c - 10), min(M, c + 10) + 1):
                if (i, j) not in best:
                    continue
                sc = best[(i, j)][0]
                for a, b, pen in _BEADS:
                    ni, nj = i + a, j + b
                    if ni > n or nj > M:
                        continue
                    A = set().union(*DT[i:ni]) if a else set()
                    B_ = set().union(*KT[k0 + j:k0 + nj]) if b else set()
                    s2 = sc + (_dice(A, B_) if a and b else 0) - pen
                    if (ni, nj) not in best or best[(ni, nj)][0] < s2:
                        best[(ni, nj)] = (s2, (i, j))
        cur = max((k for k in best if k[0] == n), key=lambda k: best[k][0])
        al = {}
        while best[cur][1]:
            pi, pj = best[cur][1]
            for x in range(pi, cur[0]):
                al[x] = [kord[k0 + y] for y in range(pj, cur[1])]
            cur = (pi, pj)
        for x, u in enumerate(us):
            mine = {t[4:] for t in u["kjv"].get("spans", [u["kjv"]["target"]]) if t.startswith("kjv:")}
            if al.get(x) and not mine & set(al[x]):
                flagged.append((u["id"], sorted(mine, key=osis_key), al[x]))
    chapters = {}
    for f in flagged:
        chapters.setdefault(f[0].split(":")[1].rsplit(".", 1)[0], []).append(f)
    print(f"Douay verses aligned to the KJV by their English: {len(units):,}")
    print(f"  where the alignment shares no KJV verse with the map: {len(flagged)} "
          f"verses in {len(chapters)} chapters")
    for c, fs in sorted(chapters.items(), key=lambda kv: -len(kv[1]))[:show]:
        print(f"  {c} ({len(fs)}): " + "; ".join(f"{i.split(':')[1]} map {m} / English {e}"
                                                  for i, m, e in fs[:3]))
    return flagged


def render(doc):
    return (json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--audit-douay", action="store_true")
    a = ap.parse_args()
    if a.audit_douay:
        audit_douay()
        return
    if a.fetch:
        fetch()
        return
    if a.measure:
        measure()
        return
    blob = render(build())
    rel = os.path.relpath(OUT, ROOT)
    if a.check:
        if not os.path.exists(OUT):
            _stop(f"{rel} missing")
        if open(OUT, "rb").read() != blob:
            _stop(f"{rel} differs from a rebuild")
        print(f"OK: {rel} byte-identical; every invariant holds")
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT + ".tmp", "wb") as f:
        f.write(blob)
    os.replace(OUT + ".tmp", OUT)
    print(f"wrote {rel}: {json.loads(blob)['counts']}")


if __name__ == "__main__":
    main()
