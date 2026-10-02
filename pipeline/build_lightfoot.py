#!/usr/bin/env python3
"""
build_lightfoot.py -- the Apostolic Fathers in English, J. B. Lightfoot and
J. R. Harmer's translation (1891), from CCEL's ThML, aligned to Kirsopp Lake's
Greek (pipeline/build_apostolic_fathers.py) chapter by chapter and, where it
can be measured, section by section.

    python3 pipeline/build_lightfoot.py --fetch    # CCEL ThML, sha256-pinned -> data/corpus/lightfoot/ (gitignored)
    python3 pipeline/build_lightfoot.py            # build data/books/<work>-lightfoot.json + manifest entries
    python3 pipeline/build_lightfoot.py --check    # rebuild in memory: = the committed manifest entries
    python3 pipeline/build_lightfoot.py --survey   # every chapter: Lightfoot's pieces vs Lake's sections
    python3 tests/lightfoot_test.py

Needs the Greek built first (python3 pipeline/build_apostolic_fathers.py
--fetch), because the alignment reads Lake's books. Nothing here edits them.

SOURCE AND RIGHTS (rule 6, read 2026-10-02 in the file itself). CCEL's
ThML of "The Apostolic Fathers", ccel.org/ccel/lightfoot/fathers.xml,
612,511 bytes, pinned by sha256 in fetch_sources.LIGHTFOOT. Its head says
<DC.Rights>Public Domain</DC.Rights> and printSourceInfo "Baker Book House,
1956", a photographic reprint of Lightfoot & Harmer (London: Macmillan,
1891). Lightfoot died in 1889, Harmer in 1944; the translation, published 1891, is PD.
The file carries one other rights statement, an XML comment at the top of the
head: "Copyright Christian Classics Ethereal Library" -- CCEL's claim on its
own preparation (markup, headings). The file states NO non-commercial
condition. So: the text is PD and may be quoted and served; CCEL's prepared
file is not mirrored whole (redistribute_whole false) until Adam rules
otherwise -- the books are gitignored in any case, and only the manifest
entries are committed.

WHAT IS IN IT. The nine works of Lake's set: 1-2 Clement, the seven letters of
Ignatius (middle recension), Polycarp to the Philippians, the Martyrdom of
Polycarp, the Didache, Barnabas, Hermas, Diognetus. NOT in this file: the
fragments of Papias and the Reliques of the Elders, which the 1891 volume
also printed; CCEL's edition stops at Diognetus (checked: 15 div2s, the last
"The Epistle to Diognetus").

THE ALIGNMENT, in two steps.

1. Chapters, by rule. Lightfoot's headings give the chapter ("1 Clem. 4",
"IgnEph. Prologue"), and Lake's chapters are the same chapters, so every
English chapter names its Greek chapter. Hermas is the exception: CCEL heads
only the Vision, Mandate or Similitude ("Parable"), and inside a part the
chapters show only as an indented first paragraph -- and some indents are not
chapter starts (Vis. 3 has 17 indents for Lake's 13 chapters). So in a Hermas
part: if Lightfoot has exactly as many pieces as Lake has sections and every
one of Lake's chapter starts falls on an indented piece, Lake's chapter starts
are taken (corroborated, not assumed); else if the indents are exactly as many
as Lake's chapters, the indents are the chapters; else the part is one unit.
One per-book rule (SPLIT) moves the Moscow epilogue that Lightfoot prints
inside Mart. Pol. 22 to Lake's separate `epilogus_alius`, witnessed by
Lightfoot's own footnote on its first paragraph.

2. Sections, by measurement. Inside a chapter CCEL breaks the text into
paragraphs (and verse blocks, the prayers): "pieces". Mostly they are Lake's
sections one for one, but not always (a piece may hold two sections; two
pieces may share one; a boundary may fall a clause off). So the pieces are
aligned to Lake's sections by their lengths (a Gale-Church style alignment:
each piece's English length against its Greek's, scaled by the work's own
English/Greek ratio; beads 1:1, 1:2, 2:1, 1:3, 3:1, 2:2, a penalty on all but
1:1 that is the prior read off the counts), and every alignment whose cost
is within MARGIN of the best is kept.
A boundary between units is drawn only where ALL of those near-best
alignments agree. So each unit is the finest block the measurement supports:
one section (`1clement-lightfoot:4.7` translates `1clement-lake:4.7`), a run
of sections (`1clement-lightfoot:5.5-6`), or, where nothing inside it can be
told apart, the whole chapter (`ignatius-lightfoot:Phld.1` translates Ign.
Phld. 1.1-2).
Every unit is keyed by the Greek it translates and links to each Greek unit
(type "original", align "section" | "range" | "chapter"); `lex.lightfoot`
keeps Lightfoot's own heading, `lex.pieces` how many CCEL paragraphs it holds.

THE CONFIDENCE, measured and recorded in each book's `alignment` block:
length_test -- for the chapters where the piece and section counts agree, the
share of 1:1 pairs whose length ratio is within x1.5 of the work's, against
the same share when the pairing is shifted by one piece (the control);
name_test -- an independent check the alignment never saw: of the proper
names in each English unit (NAMES), how many have their Greek stem in the
Greek the unit links to, against the Greek of the next unit (the control);
and how many Greek sections are reached by section, in a run, or by chapter.
All works together (2026-10-02): length 1795/1811 (99.1%) vs 717/1446
(49.6%); names 253/259 (97.7%) vs 39/256 (15.2%). Of the six misses, two are
the Latin of Pol. Phil. 11 (Paulus), not an alignment fault.
Section boundaries in a translation are approximate (a clause may sit on the
other side), which the honesty field says.

LINKS. Each English unit links to the Greek unit(s) it translates (type
"original"). The Greek books are not rewritten to link back, because that
would change their committed built_sha256 (build_apostolic_fathers.py is not
this script's to edit). ThML scripRefs are harvested into links[] as in every
CCEL book: this file has exactly one, a CCEL auto-tag on the heading
"Revelation 5" (Lightfoot's name for Hermas's fifth Vision), not on the text;
headings are not unit text, so it is reported and not harvested.
"""
import argparse
import hashlib
import json
import math
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_apostolic_fathers as A  # noqa: E402
import fetch_sources as FS  # noqa: E402

BOOKS = A.BOOKS
MANIFEST = A.MANIFEST
SRC = os.path.join(ROOT, "data", "corpus", "lightfoot", "fathers.xml")
# The length alignment (step 2 of THE ALIGNMENT). Fixed numbers, not tuned per chapter.
BEADS = ((1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 2))
MARGIN = 4.0     # alignments within this of the best (squared-z units; a likelihood
                 # factor of e^2, about 7) all have a say on the boundaries
# The penalty on a bead other than 1:1 is not set by hand: it is the prior read
# off the file (penalty()), -2 ln(P(one given non-1:1 bead) / P(1:1)), where the
# share of non-1:1 beads is the least the piece/section counts force.
KBEST = 64       # alignments kept per cell; if the 64th is still within MARGIN, the chapter is one unit

# CCEL's div2s in file order -> (Lake slug, Ignatius letter or None).
DIVS = [
    ("1clement-lake", None), ("2clement-lake", None),
    ("ignatius-lake", "Eph"), ("ignatius-lake", "Magn"), ("ignatius-lake", "Trall"),
    ("ignatius-lake", "Rom"), ("ignatius-lake", "Phld"), ("ignatius-lake", "Smyrn"),
    ("ignatius-lake", "Pol"),
    ("polycarp-phil-lake", None), ("martyrdom-polycarp-lake", None), ("didache-lake", None),
    ("barnabas-lake", None), ("hermas-lake", None), ("diognetus-lake", None),
]
# Lightfoot's chapter heading prefix per div (checked: a heading that does not
# match stops the build).
HEAD = {"1clement-lake": r"1 Clem\.", "2clement-lake": r"2 Clem\.", "polycarp-phil-lake": r"PolPhil\.",
        "martyrdom-polycarp-lake": r"MartPol\.", "didache-lake": r"Did\.", "barnabas-lake": r"Barn\.",
        "diognetus-lake": r"Diogn\."}
# Lightfoot's "Prologue" is Lake's address, which Lake keys differently per work.
PROLOGUE = {"1clement-lake": "preface", "polycarp-phil-lake": "praef.sal",
            "martyrdom-polycarp-lake": "praef", "ignatius-lake": "{letter}.praef"}
# Hermas: Lightfoot's 27 part headings, in order, -> Lake's Vis/Mand/Sim.
HERMAS_PARTS = ([("Vis", i) for i in range(1, 6)] + [("Mand", i) for i in range(1, 13)]
                + [("Sim", i) for i in range(1, 11)])
HERMAS_HEAD = re.compile(r"^(?:Vision \d+|Revelation 5|Mandate \d+|Parables Which He Spake With Me|"
                         r"Another Parable|Parable \d+)$")
HERMAS_GROUP = {"Herm.Vis", "Herm.Mand", "Herm.Sim"}

RIGHTS = {
    "license": "public domain (Lightfoot & Harmer, 1891; the file's DC.Rights reads "
               "'Public Domain'); CCEL's head also carries the comment 'Copyright Christian "
               "Classics Ethereal Library', its claim on the prepared file; no non-commercial "
               "condition is stated in the file",
    "attribution": "Christian Classics Ethereal Library (ccel.org/ccel/lightfoot/fathers), "
                   "from the Baker Book House reprint (1956) of J. B. Lightfoot and J. R. Harmer, "
                   "The Apostolic Fathers (London: Macmillan, 1891)",
    "source_url": "https://www.ccel.org/ccel/lightfoot/fathers.xml",
    "redistribute_whole": False,
}


def clean(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip()


def fetch():
    print(f"  lightfoot: {FS.fetch_lightfoot()}")


def verify_pin():
    if not os.path.exists(SRC) or A.sha256_file(SRC) != FS.LIGHTFOOT["sha256"]:
        raise SystemExit(f"pinned input missing or changed: {SRC}\n"
                         f"  run: python3 pipeline/build_lightfoot.py --fetch")


def text_of(el, notes):
    """Running text of an element; <note>s go to `notes`, not the text."""
    out = [el.text or ""]
    for c in el:
        if c.tag == "note":
            notes.append(clean("".join(c.itertext())))
        else:
            out.append(text_of(c, notes))
        out.append(c.tail or "")
    return "".join(out)


def pieces(div):
    """A div2 as a list of ('head', text, scripRefs) and ('piece', text, indented,
    notes, scripRefs, kind). A piece is a <p> or a <verse> block (its lines
    joined by newlines)."""
    out = []
    for el in div:
        refs = [r.get("osisRef") or r.get("passage") for r in el.iter("scripRef")]
        if el.tag in ("h2", "h3"):
            out.append(("head", clean("".join(el.itertext())), refs))
        elif el.tag == "p":
            notes = []
            raw = text_of(el, notes)
            out.append(("piece", clean(raw), raw.lstrip("\n").startswith("   "), notes, refs, "p"))
        elif el.tag == "verse":
            lines = [clean("".join(l.itertext())) for l in el.iter("l")]
            out.append(("piece", "\n".join(x for x in lines if x), False, [], refs, "verse"))
        else:
            raise SystemExit(f"HARD STOP: unexpected <{el.tag}> in {div.get('id')}")
    return out




# Per-book rule (rule 2: the source is never edited; this reruns on refetch).
# Lightfoot prints the Moscow manuscript's epilogue inside Mart. Pol. 22, after
# 22.3, with a footnote on its first paragraph ("... as read in the Moscow
# ms."); Lake prints it apart, as `epilogus_alius`. (slug, chapter, first piece
# moved, Lake chapter it goes to, word the footnote on that piece must contain)
SPLIT = [("martyrdom-polycarp-lake", "22", 4, "epilogus_alius", "Moscow")]


def read():
    """[[lake slug, Lake chapter id (Hermas: part id), Lightfoot heading, [piece...]], ...]
    in file order, plus the scripRefs found in headings (reported, not harvested)."""
    root = ET.parse(SRC).getroot()
    rights = root.find(".//DC.Rights")
    if rights is None or clean(rights.text or "") != "Public Domain":
        raise SystemExit("HARD STOP: the file's DC.Rights is no longer 'Public Domain'; re-read it")
    divs = list(root.find("ThML.body").iter("div2"))
    if len(divs) != len(DIVS):
        raise SystemExit(f"HARD STOP: {len(divs)} works in the file, {len(DIVS)} expected")
    chapters, head_refs = [], []
    for div, (slug, letter) in zip(divs, DIVS):
        items = pieces(div)
        if items[0][0] != "head":
            raise SystemExit(f"HARD STOP: {div.get('id')} has no title heading")
        cur, part = None, -1
        for it in items[1:]:   # [0] is the work's title
            if it[0] == "head":
                h, refs = it[1], it[2]
                if refs:
                    head_refs.append({"heading": h, "scripRef": refs, "div": div.get("id")})
                if slug == "hermas-lake":
                    if h in HERMAS_GROUP:
                        continue
                    if not HERMAS_HEAD.match(h):
                        raise SystemExit(f"HARD STOP: Hermas heading {h!r} not recognised")
                    part += 1
                    kind, num = HERMAS_PARTS[part]
                    cur = [slug, f"{kind}.{num}", h, []]
                    chapters.append(cur)
                    continue
                pre = HEAD.get(slug) or rf"Ign{letter}\."
                m = re.fullmatch(pre + r" (Prologue|\d+)", h)
                if not m:
                    raise SystemExit(f"HARD STOP: {slug}: heading {h!r} not recognised")
                ch = (PROLOGUE[slug].format(letter=letter) if m.group(1) == "Prologue"
                      else (f"{letter}." if letter else "") + m.group(1))
                cur = [slug, ch, h, []]
                chapters.append(cur)
                continue
            if cur is None:
                raise SystemExit(f"HARD STOP: {slug}: text before the first chapter heading")
            cur[3].append(it)
        if slug == "hermas-lake" and part != len(HERMAS_PARTS) - 1:
            raise SystemExit(f"HARD STOP: Hermas has {part + 1} parts, {len(HERMAS_PARTS)} expected")
    return chapters, head_refs


def lake_books():
    out = {}
    for slug, *_ in A.WORKS:
        p = os.path.join(BOOKS, slug + ".json")
        if not os.path.exists(p):
            raise SystemExit(f"{p} is not built: run python3 pipeline/build_apostolic_fathers.py --fetch")
        with open(p, encoding="utf-8") as f:
            out[slug] = json.load(f)
    return out


def chapter_of(cid):
    """Lake's chapter for a section id: '4.7' -> '4', 'Vis.3.1.2' -> 'Vis.3.1'.
    A unit with no section number (Mart. Pol. 'praef', Pol. Phil. 'praef.sal')
    is its own chapter."""
    head, _, last = cid.rpartition(".")
    return head if head and last.isdigit() else cid


def lake_chapters(book):
    """Lake chapter id -> [(section id, text, ref)] in order."""
    chs = {}
    for u in book["units"]:
        cid = u["id"].split(":", 1)[1]
        chs.setdefault(chapter_of(cid), []).append((cid, u["text"], u["ref"]))
    return chs


def hermas_chapters(part, heading, items, lake):
    """A Hermas part's pieces cut into Lake's chapters (THE ALIGNMENT, step 1).
    Returns ([(chapter id, heading, pieces)], how)."""
    chs = [(k, v) for k, v in lake.items() if k.rsplit(".", 1)[0] == part]
    sizes = [len(v) for _, v in chs]
    starts = [sum(sizes[:i]) for i in range(len(sizes))]
    indents = [i for i, it in enumerate(items) if it[2]]
    if not indents or indents[0] != 0:
        raise SystemExit(f"HARD STOP: Hermas {part} does not open on an indented paragraph")
    if len(items) == sum(sizes) and set(starts) <= set(indents):
        cuts, how = starts, "lake-starts-on-indents"
    elif len(indents) == len(chs):
        cuts, how = indents, "indents"
    else:
        return [(part, heading, items)], "part"
    out = []
    for n, ((ch, _), a) in enumerate(zip(chs, cuts)):
        b = cuts[n + 1] if n + 1 < len(cuts) else len(items)
        out.append((ch, f"{heading}, ch. {n + 1}", items[a:b]))
    return out, how


def spans(chapters, lakes):
    """Every (slug, Lake chapter, Lightfoot heading, pieces, Lake sections), with the
    Hermas parts cut into chapters and the SPLIT rows applied; plus how each Hermas
    part was cut."""
    out, how = [], {}
    rows = [list(r) for r in chapters]
    for slug, ch, first, to, witness in SPLIT:
        hit = [r for r in rows if r[0] == slug and r[1] == ch]
        if len(hit) != 1 or len(hit[0][3]) <= first or not any(witness in n for n in hit[0][3][first][3]):
            raise SystemExit(f"HARD STOP: SPLIT row {slug} {ch} no longer matches the file")
        r = hit[0]
        rows.insert(rows.index(r) + 1, [slug, to, r[2] + f" (from par. {first + 1})", r[3][first:]])
        r[3] = r[3][:first]
    for slug, ch, head, items in rows:
        lake = lakes[slug]
        if slug == "hermas-lake":
            parts, how[ch] = hermas_chapters(ch, head, items, lake)
            for c, h, its in parts:
                out.append((slug, c, h, its, lake.get(c) or [x for k, v in lake.items()
                                                             if k.rsplit(".", 1)[0] == c for x in v]))
            continue
        if ch not in lake:
            raise SystemExit(f"HARD STOP: {slug}: Lightfoot's {head!r} names no Lake chapter ({ch})")
        out.append((slug, ch, head, items, lake[ch]))
    return out, how


# ------------------------------------------------------------ the length alignment
def calibrate(rows):
    """Per work: the English/Greek length ratio (median) and the spread of its log
    (1.4826 x median absolute deviation), from the chapters whose piece and
    section counts agree, paired 1:1."""
    import statistics as st
    by = {}
    for slug, _, _, items, secs in rows:
        if len(items) == len(secs):
            by.setdefault(slug, []).extend(len(it[1]) / max(1, len(s[1])) for it, s in zip(items, secs))
    cal = {}
    for slug, rs in by.items():
        ratio = st.median(rs)
        logs = [math.log(r / ratio) for r in rs]
        cal[slug] = (ratio, 1.4826 * st.median(abs(x) for x in logs))
    return cal


def penalty(rows):
    """(penalty, beads forced, sections): the prior on a non-1:1 bead, from the
    least number of them the counts force (|pieces - sections| per chapter)."""
    forced = sum(abs(len(items) - len(secs)) for _, _, _, items, secs in rows)
    total = sum(len(secs) for *_, secs in rows)
    p = forced / total
    return 2 * math.log((1 - p) / (p / (len(BEADS) - 1))), forced, total


def kbest(E, G, ratio, sd, pen, k=KBEST):
    """The k cheapest monotone alignments of piece lengths E to section lengths G,
    as [(cost, (bead, ...))], cheapest first."""
    n, m = len(E), len(G)
    best = {(0, 0): [(0.0, ())]}
    for i in range(n + 1):
        for j in range(m + 1):
            if i == j == 0:
                continue
            cand = []
            for a, b in BEADS:
                prev = best.get((i - a, j - b))
                if not prev:
                    continue
                z = math.log(max(1, sum(E[i - a:i])) / (max(1, sum(G[j - b:j])) * ratio)) / sd
                c = z * z + (0.0 if (a, b) == (1, 1) else pen)
                cand.extend((pc + c, path + ((a, b),)) for pc, path in prev)
            if cand:
                cand.sort()
                best[(i, j)] = cand[:k]
    return best.get((n, m), [])


def points(path):
    i = j = 0
    out = {(0, 0)}
    for a, b in path:
        i, j = i + a, j + b
        out.add((i, j))
    return out


def blocks(E, G, ratio, sd, pen):
    """(blocks, best cost, how many alignments had a say): each block is
    (first piece, end piece, first section, end section), cut only where every
    alignment within MARGIN of the best agrees."""
    paths = kbest(E, G, ratio, sd, pen)
    if not paths:
        return [(0, len(E), 0, len(G))], None, 0
    near = [p for c, p in paths if c <= paths[0][0] + MARGIN]
    if len(near) == KBEST:
        return [(0, len(E), 0, len(G))], paths[0][0], len(near)
    cuts = sorted(set.intersection(*(points(p) for p in near)))
    return [(a[0], b[0], a[1], b[1]) for a, b in zip(cuts, cuts[1:])], paths[0][0], len(near)


# The second, independent test: proper names. Each English name, where it
# occurs in a unit, should have its Greek stem in the Greek that unit links to
# (accents, breathings and case dropped). The control is the Greek of the NEXT
# unit. Names chosen because each is frequent in the English and written one
# way in the Greek; stems are matched as substrings of the stripped Greek.
NAMES = {
    "Moses": "μωυσ", "Polycarp": "πολυκαρπ", "Israel": "ισραηλ", "Syria": "συρι", "David": "δαυ",
    "Jacob": "ιακωβ", "Hermas": "ερμα", "Abraham": "αβρααμ", "Smyrna": "σμυρν", "Egypt": "αιγυπτ",
    "Paul": "παυλ", "Irenaeus": "ειρηναι", "Rome": "ρωμ", "Cain": "καιν", "Isaac": "ισαακ",
    "Joseph": "ιωσηφ", "Peter": "πετρ", "Abel": "αβελ", "Adam": "αδαμ", "Burrhus": "βουρρ",
    "Satan": "σαταν", "Herod": "ηρωδ", "Caesar": "καισαρ", "Corinth": "κορινθ", "Daniel": "δανιηλ",
    "Onesimus": "ονησιμ", "Pilate": "πιλατ", "Antioch": "αντιοχ", "Sinai": "σινα", "Rebecca": "ρεβεκκ",
    "Manasseh": "μανασσ", "Aaron": "ααρων", "Enoch": "ενωχ", "Rahab": "ρααβ", "Ezekiel": "ιεζεκιηλ",
    "Ephesus": "εφεσ", "Crocus": "κροκ", "Theophorus": "θεοφορ", "Ignatius": "ιγνατι",
}


def _bare(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c)).replace("ς", "σ")


def name_check(units, greek):
    """(names found in the linked Greek, names, found in the next unit's Greek
    instead -- the control, units with a next)."""
    bare = [_bare(" ".join(greek[x["target"]] for x in u["links"] if x.get("type") == "original"))
            for u in units]
    hit = tot = ctl = ctl_tot = 0
    for i, u in enumerate(units):
        for name, stem in NAMES.items():
            if not re.search(rf"\b{name}\b", u["text"]):
                continue
            tot += 1
            hit += stem in bare[i]
            if i + 1 < len(units):
                ctl_tot += 1
                ctl += stem in bare[i + 1]
    return hit, tot, ctl, ctl_tot


def shift_control(rows, cal):
    """Per work [pairs within x1.5 of the work's ratio, pairs, the same for the
    pairing shifted by one piece, shifted pairs], over the chapters whose
    counts agree."""
    tol = math.log(1.5)
    out = {}
    for slug, _, _, items, secs in rows:
        c = out.setdefault(slug, [0, 0, 0, 0])
        if len(items) != len(secs):
            continue
        ratio = cal[slug][0]
        for i, (it, s) in enumerate(zip(items, secs)):
            c[1] += 1
            c[0] += abs(math.log(len(it[1]) / max(1, len(s[1])) / ratio)) < tol
            if i + 1 < len(secs):
                c[3] += 1
                c[2] += abs(math.log(len(it[1]) / max(1, len(secs[i + 1][1])) / ratio)) < tol
    return out


# ------------------------------------------------------------ the books
def chapter_ref(secs):
    """Lake's printed ref for a whole chapter: 'Did. 9.1' -> 'Did. 9'."""
    ref = secs[0][2]
    return ref.rsplit(".", 1)[0] if chapter_of(secs[0][0]) != secs[0][0] else ref


def make_unit(eslug, lslug, ch, head, its, secs, whole):
    """One English unit: pieces `its` translating Lake sections `secs`."""
    if len(secs) == 1:
        key, ref, align = secs[0][0], secs[0][2], "section"
    elif whole:
        key, ref, align = ch, chapter_ref(secs), "chapter"
    else:
        last = secs[-1][0].rsplit(".", 1)[1]
        key, ref, align = f"{secs[0][0]}-{last}", f"{secs[0][2]}-{last}", "range"
    links = [{"target": f"{lslug}:{s[0]}", "type": "original", "align": align, "resolved": True}
             for s in secs]
    for it in its:   # the ThML scripRefs, as in every CCEL book (this file has none in its text)
        links.extend({"osis": r, "source": "ccel-scripRef", "resolved": False} for r in it[4])
    lex = {"lightfoot": head, "pieces": len(its), "align": align}
    notes = [n for it in its for n in it[3]]
    if notes:
        lex["notes"] = notes
    return {"id": f"{eslug}:{key}", "ref": f"{ref} (Lightfoot)",
            "text": "\n".join(it[1] for it in its), "links": links, "lex": lex}


TITLES = {slug: title for slug, _, title, _, _ in A.WORKS}
AUTHORS = {slug: author for slug, _, _, author, _ in A.WORKS}


def book_of(eslug, slug, b, lake_book, cal, pen, hermas_how, tests):
    ratio, sd = cal[slug]
    units = b["units"]
    lake_ids = [u["id"].split(":", 1)[1] for u in lake_book["units"]]
    reached = {}
    for u in units:
        for x in u["links"]:
            if x.get("type") == "original":
                reached[x["target"].split(":", 1)[1]] = x["align"]
    by_align = {k: sum(1 for v in reached.values() if v == k) for k in ("section", "range", "chapter")}
    book = {
        "slug": eslug,
        "title": TITLES[slug] + " (English)",
        "author": AUTHORS[slug] + ", tr. J. B. Lightfoot and J. R. Harmer",
        "source": {"path": os.path.relpath(SRC, os.path.join(ROOT, "data", "corpus")),
                   "format": "thml", "lang": "en",
                   "edition": "J. B. Lightfoot and J. R. Harmer, The Apostolic Fathers "
                              "(London: Macmillan, 1891), as reprinted by Baker Book House "
                              "(1956) and prepared by CCEL (2012)",
                   "sha256": FS.LIGHTFOOT["sha256"]},
        "scheme": {"citation": f"Lake's citation ({lake_book['scheme']['citation']}), "
                               "naming the Greek the English unit translates",
                   "resolution": "section where the lengths show it; else a run of sections; "
                                 "else the chapter",
                   "honesty": ("Lightfoot's chapters are Lake's by rule"
                               + ("; inside a Hermas part, Lake's chapter starts where Lightfoot's "
                                  "indents corroborate them, else the indents where they are as "
                                  "many as Lake's chapters" if slug == "hermas-lake" else "")
                               + f". {by_align['section']} of the {len(lake_ids)} Greek sections "
                               "have an English unit of their own, placed by length (every "
                               "near-best alignment agreeing; alignment.length_test and "
                               "name_test measure it), but a section boundary in a translation "
                               "is approximate: a clause may sit on the other side. "
                               f"{by_align['range']} are reached only in a run of sections and "
                               f"{by_align['chapter']} only by chapter. The English is CCEL's "
                               "transcription, not proofread here."),
                   "note": "Lightfoot's footnotes are in lex.notes, not `text`; verse blocks "
                           "(prayers) keep their lines."},
        "rights": dict(RIGHTS),
        "alignment": {
            "counterpart": slug,
            "direction": "English -> Greek only (the Greek books are not rewritten)",
            "units": len(units),
            "lake_sections": len(lake_ids),
            "sections_reached": by_align,
            "lake_sections_unreached": [i for i in lake_ids if i not in reached],
            "chapters": len(b["chapters"]),
            "chapters_counts_disagree": [c["chapter"] for c in b["chapters"] if not c["counts_agree"]],
            "chapters_whole": [c["chapter"] for c in b["chapters"] if c["units"] == 1 and c["sections"] > 1],
            "length_test": {"pairs_within_x1.5": tests["length"][:2],
                            "control_shifted_by_one": tests["length"][2:]},
            "name_test": {"names_in_linked_greek": tests["names"][:2],
                          "control_next_unit": tests["names"][2:]},
            "length_ratio": round(ratio, 3),
            "length_log_spread": round(sd, 3),
            "method": f"beads {' '.join(f'{x}:{y}' for x, y in BEADS)}; penalty {pen[0]:.2f} "
                      f"(-2 ln of the prior: {pen[1]} non-1:1 beads forced in {pen[2]} sections, "
                      f"all works); "
                      f"margin {MARGIN}; ratio and spread from this work's count-agreeing chapters",
        },
        "units": units,
    }
    if slug == "hermas-lake":
        book["alignment"]["hermas_parts"] = hermas_how
    return book


def build():
    verify_pin()
    lakes_raw = lake_books()
    lakes = {s: lake_chapters(b) for s, b in lakes_raw.items()}
    chapters, head_refs = read()
    rows, hermas_how = spans(chapters, lakes)
    cal = calibrate(rows)
    pen = penalty(rows)
    books = {}
    for slug, ch, head, items, secs in rows:
        eslug = slug.replace("-lake", "-lightfoot")
        b = books.setdefault(eslug, {"units": [], "chapters": [], "lake": slug})
        if not items:
            raise SystemExit(f"HARD STOP: {eslug} {ch}: no text")
        ratio, sd = cal[slug]
        bl, _, _ = blocks([len(it[1]) for it in items], [len(s[1]) for s in secs], ratio, sd, pen[0])
        whole = len(bl) == 1 and len(secs) > 1
        for a, z, c, d in bl:
            b["units"].append(make_unit(eslug, slug, ch, head, items[a:z], secs[c:d], whole))
        b["chapters"].append({"chapter": ch, "pieces": len(items), "sections": len(secs),
                              "units": len(bl), "counts_agree": len(items) == len(secs)})
    greek = {u["id"]: u["text"] for bk in lakes_raw.values() for u in bk["units"]}
    length = shift_control(rows, cal)
    out = {}
    tot = [0] * 8
    for eslug, b in books.items():
        tests = {"length": length[b["lake"]], "names": list(name_check(b["units"], greek))}
        tot = [x + y for x, y in zip(tot, tests["length"] + tests["names"])]
        book = book_of(eslug, b["lake"], b, lakes_raw[b["lake"]], cal, pen, hermas_how, tests)
        blob = json.dumps(book, ensure_ascii=False).encode("utf-8")
        out[eslug] = (book, blob, entry(book, blob))
    measured = {"length": tot[:4], "names": tot[4:], "heading_scripRefs_not_harvested": head_refs}
    return out, measured, rows


def entry(book, blob):
    return {"title": book["title"], "author": book["author"], "format": book["source"]["format"],
            "sha256": book["source"]["sha256"], "units": len(book["units"]),
            "scheme": book["scheme"], "rights": book["rights"], "alignment": book["alignment"],
            "built_sha256": hashlib.sha256(blob).hexdigest()}


def survey(rows):
    cal = calibrate(rows)
    pen = penalty(rows)[0]
    for slug, ch, head, items, secs in rows:
        ratio, sd = cal[slug]
        bl, cost, near = blocks([len(i[1]) for i in items], [len(s[1]) for s in secs], ratio, sd, pen)
        shape = " ".join(f"{b - a}:{d - c}" for a, b, c, d in bl)
        flag = "" if all(b - a == 1 == d - c for a, b, c, d in bl) else "  <--"
        print(f"  {slug[:-5]:<18}{ch:<16}{len(items):>3} pieces {len(secs):>3} sections  "
              f"units {shape}{flag}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--survey", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    built, measured, rows = build()
    if a.survey:
        return survey(rows)
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    tot = {"units": 0, "lake": 0, "section": 0, "range": 0, "chapter": 0}
    for slug, (book, _, e) in built.items():
        al = e["alignment"]
        r = al["sections_reached"]
        for k in ("section", "range", "chapter"):
            tot[k] += r[k]
        tot["units"] += e["units"]
        tot["lake"] += al["lake_sections"]
        print(f"  {slug:<30}{e['units']:>5} units; of {al['lake_sections']:>4} Greek sections "
              f"{r['section']:>4} by section {r['range']:>3} in a run {r['chapter']:>3} by chapter "
              f"{len(al['lake_sections_unreached']):>2} unreached")
    print(f"  {'all':<30}{tot['units']:>5} units; of {tot['lake']:>4} Greek sections "
          f"{tot['section']:>4} by section {tot['range']:>3} in a run {tot['chapter']:>3} by chapter")
    t, nt, s, ns = measured["length"]
    print(f"  length test, chapters whose counts agree: {t}/{nt} 1:1 pairs within x1.5 "
          f"({100 * t / nt:.1f}%); shifted by one piece: {s}/{ns} ({100 * s / ns:.1f}%)")
    t, nt, s, ns = measured["names"]
    print(f"  name test, every unit: {t}/{nt} English names found in the linked Greek "
          f"({100 * t / nt:.1f}%); in the next unit's Greek: {s}/{ns} ({100 * s / ns:.1f}%)")
    for h in measured["heading_scripRefs_not_harvested"]:
        print(f"  scripRef on a heading, not harvested: {h}")
    if a.report:
        return
    if a.check:
        bad = [s for s, (_, blob, e) in built.items() if manifest.get(s) != e
               or (os.path.exists(os.path.join(BOOKS, s + ".json"))
                   and open(os.path.join(BOOKS, s + ".json"), "rb").read() != blob)]
        if bad:
            raise SystemExit(f"CHECK FAILED: rebuilt books differ from the manifest: {bad}")
        print("  CHECK PASSED: every book = its committed manifest entry (built_sha256).")
        return
    for slug, (_, blob, e) in built.items():
        A.write_atomic(os.path.join(BOOKS, slug + ".json"), blob)
        manifest[slug] = e
    A.write_atomic(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    print(f"  wrote {len(built)} books + {len(manifest)}-entry manifest")


if __name__ == "__main__":
    main()
