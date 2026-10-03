#!/usr/bin/env python3
"""
build_commentary.py -- the whole-Bible commentaries keyed to KJV verse ids:
which verses each comment is on, and which verses it cites.

    python3 pipeline/build_commentary.py --fetch   # CCEL's texts + the scans' OCR, sha256-pinned
    python3 pipeline/build_commentary.py           # -> data/commentary/*.jsonl + manifest.json, build/commentary/
    python3 pipeline/build_commentary.py --check   # rebuild in memory: byte-identical to the committed files
    python3 pipeline/build_commentary.py --collate # CCEL's wording vs the period scans -> collation.json

THE BOOKS (CCEL ThML; each CCEL print source recorded and checked: a print
source dated 1930 or later is flagged `ccel_print_source_check`, as
fetch_shelf.py does):
  henry   Matthew Henry, Exposition of the Old and New Testaments (1706-21;
          Acts to Revelation finished by other ministers), six volumes
  jfb     Jamieson, Fausset and Brown, Commentary Critical and Explanatory
          on the Whole Bible (1871)
  barnes  Albert Barnes, Notes on the New Testament (CCEL keyed it from
          Baker's 1949 reprint: flagged)
and one from EEBO-TCP (hand-keyed from the first edition, CC0):
  poole   Matthew Poole, Annotations upon the Holy Bible (1683-85): read by
          build_tcp_work, one comment per verse with a note (below)

A COMMENT. CCEL marks each comment's passage with an empty
<scripCom osisRef=.../>. A comment runs from its mark to the next one, or to
the next division; marks with no comment text between them are one comment,
on the most precise passage named (Henry marks the chapter, then its first
section; Barnes the verse, then its chapter). Text before a chapter's first
mark is that chapter's introduction.

TWO READINGS OF WHERE A COMMENT IS. The mark is one. The other is read from
the comment itself, never from the mark:
  henry   the verse numbers printed in the passage Henry quotes ("1 In the
          beginning ... 2 And the earth"): first and last;
  jfb     the verse number that opens the first lemma ("<b>13. pitieth</b>"),
          in the chapter of the enclosing "Chapter N" division;
  barnes  the division's title ("Matthew 2:14").
Each row says whether they agree (`anchor`: agrees / differs / unread).

WHAT A COMMENT CITES is voted as in build_topical.py: CCEL's scripRef tags
and topical_read.refs() read independently (with "ver. 31" and "ch. 3:5"
taken in the comment's own book and chapter); a citation is committed when
both read it, or when one does and print does too.

Committed: anchors and citations (kjv: ids). The prose, public domain but
CCEL's keyed text, is written to build/commentary/ only.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import topical_read as R  # noqa: E402
import tsk_read as T  # noqa: E402
import build_topical as BT  # noqa: E402

CORPUS = os.path.join(ROOT, "data", "corpus", "commentary")
OUT = os.path.join(ROOT, "data", "commentary")
BUILD = os.path.join(ROOT, "build", "commentary")
CCEL = "https://ccel.org/ccel/"
IA = "https://archive.org/download/"
TCP = "https://raw.githubusercontent.com/textcreationpartnership/"

WORKS = {
    "henry": {
        "title": "An Exposition of the Old and New Testaments (Commentary on the Whole Bible)",
        "author": "Matthew Henry (1662-1714); Acts to Revelation completed by other ministers after his death",
        "files": [
            ("henry1", "h/henry/mhc1.xml", "6eb946647f806f46129001f83013d65c51e40ac59b939ac1c51404aa50375971"),
            ("henry2", "h/henry/mhc2.xml", "673fcb4168ad946ab1e6923c0e331cc61e4adca4498fc0ee34cf1507285aa2f7"),
            ("henry3", "h/henry/mhc3.xml", "8ba9779eba5d326acbfc9acaccf2ea1fa2d6b5c48b03ab86fc5e80b0bfa5b17e"),
            ("henry4", "h/henry/mhc4.xml", "7b6ea0800caa1daab6b0c807f5b95c7567fb5d880290bbe91d848048a80486b2"),
            ("henry5", "h/henry/mhc5.xml", "8b0853b116e9a68215a594bafe29f45502d4c766e1f128cbf5fb050f45cf2518"),
            ("henry6", "h/henry/mhc6.xml", "296195d09d4fbb1e7516ea77c100dbc87ce37542c3109f9f570c3cf155b594c1"),
        ],
        "scans": [
            ("London, 1828, six volumes (NOT_IN_COPYRIGHT)", [
                ("expositionofoldn01henr", "636a85f8a1a4eed5d03052928afe4276a92374379044d9f5ff0e3b5c401ce1f1"),
                ("expositionofoldn02henr", "20a13bb63b858af42d8fb48853765a19eaba3ffd5e32c45e6e271b08f1c3de49"),
                ("expositionofoldn03henr", "afd16953a6d5ab8b9ed8b8888ece4927a29be93d095552072ef7ac0448af9857"),
                ("expositionofoldn04henr", "6b31c0416194905e0ce93ec4d2779720a22c0c759a621c5a85b15e6de4ba61e2"),
                ("expositionofoldn05henr", "7e840d9172f37cfc1ff625042d042d254f55bb242cfcc00dd85af4cd36ecc053"),
                ("expositionofoldn06henr", "faab8cbebfceb2bdb5152768566e3fbcf678dd4a2841fc03f113e18cdcc52b24"),
            ]),
        ],
    },
    "jfb": {
        "title": "A Commentary, Critical and Explanatory, on the Old and New Testaments",
        "author": "Robert Jamieson, A. R. Fausset, David Brown",
        "files": [("jfb", "j/jamieson/jfb.xml", "ce16900c4795d9bd3dc7f7aaec3fccd395c166d4d9593a14b9aae06869aab9af")],
        "scans": [
            ("1873 one-volume printing (NOT_IN_COPYRIGHT)", [
                ("commentarycritic00jami", "eb90ea6bcf888c0ae1cff1cf6467cd781dbff74469c2ec7ae253471c45518066")]),
            ("1879 one-volume printing", [
                ("commentarycritic00jami_0", "004ffabd4c3f1ab0ecc45346383eb51341a0ffa8098ac32a8e33b972a637fd53")]),
        ],
    },
    "poole": {
        "kind": "tcp",
        "title": "Annotations upon the Holy Bible",
        "author": "Matthew Poole (1624-1679); from Isaiah 59 on, finished after his death by other ministers (Vol. II)",
        "files": [
            ("poole1", TCP + "A55363/master/A55363.xml", "fc494999def0b470be3e1d826d1bb310fe2e627da7d9946067485ddc92fbe6b5"),
            ("poole2", TCP + "A55368/master/A55368.xml", "88e15a73286b932440edfa76936b374ba63360ffea2d62d0d3ba514c5cf9a6e6"),
        ],
        "scans": [],
    },
    "barnes": {
        "title": "Notes, Explanatory and Practical, on the New Testament",
        "author": "Albert Barnes (1798-1870)",
        "files": [("barnes", "b/barnes/ntnotes.xml", "88fdc365052dd5e037ce7e6d5d797b1a5b3ba8591f62b6b3755a706feb853e05")],
        "print_books": {"Matt", "Mark", "Luke", "John"},     # all the open 1840 scans cover
        "scans": [
            ("the Gospels only, 1840, two volumes (the rest of the New Testament is not checked)", [
                ("notesexplanatory01inbarn", "6ece4e6dc4f095e90d7addd5d4f6af7f67af23db74c7fba31df019a974d8a869"),
                ("notesexplanatory02barn_0", "c920932b4ae56677b20916478b75764e059a4118a066c0c90f49e4cde2cab19a")]),
        ],
    },
}

RIGHTS = {
    "license": "public-domain",
    "basis": "Henry 1706-21, Jamieson-Fausset-Brown 1871, Barnes 1832-53, Poole 1683-85; every author died before 1931."
             " Poole's transcription is EEBO-TCP's (Phase I), CC0 1.0",
    "committed": "which verses each comment is on and which verses it cites; the prose stays in build/",
    "redistribute_whole": True,
}

_FULL = {"Genesis": "Gen", "Exodus": "Exod", "Leviticus": "Lev", "Numbers": "Num", "Deuteronomy": "Deut",
         "Joshua": "Josh", "Judges": "Judg", "Ruth": "Ruth", "Ezra": "Ezra", "Nehemiah": "Neh", "Esther": "Esth",
         "Job": "Job", "Psalms": "Ps", "Proverbs": "Prov", "Ecclesiastes": "Eccl", "Song of Solomon": "Song",
         "Isaiah": "Isa", "Jeremiah": "Jer", "Lamentations": "Lam", "Ezekiel": "Ezek", "Daniel": "Dan",
         "Hosea": "Hos", "Joel": "Joel", "Amos": "Amos", "Obadiah": "Obad", "Jonah": "Jonah", "Micah": "Mic",
         "Nahum": "Nah", "Habakkuk": "Hab", "Zephaniah": "Zeph", "Haggai": "Hag", "Zechariah": "Zech",
         "Malachi": "Mal", "Matthew": "Matt", "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts",
         "Romans": "Rom", "Galatians": "Gal", "Ephesians": "Eph", "Philippians": "Phil", "Colossians": "Col",
         "Titus": "Titus", "Philemon": "Phlm", "Hebrews": "Heb", "James": "Jas", "Jude": "Jude",
         "Revelation": "Rev"}
for _n, _o in (("Samuel", "Sam"), ("Kings", "Kgs"), ("Chronicles", "Chr"), ("Corinthians", "Cor"),
               ("Thessalonians", "Thess"), ("Timothy", "Tim"), ("Peter", "Pet"), ("John", "John")):
    for _i, _w in ((1, "1"), (2, "2"), (3, "3")):
        _FULL[f"{_w} {_n}"] = f"{_i}{_o}"
        _FULL[f"{['', 'First', 'Second', 'Third'][_i]} {_n}"] = f"{_i}{_o}"
_FULL["Acts of the Apostles"] = "Acts"


def path(name):
    return os.path.join(CORPUS, name + ".xml")


def fetch():
    for w, d in WORKS.items():
        for name, rel, want in d["files"]:
            BT._get(rel if rel.startswith("https:") else CCEL + rel, path(name), want)
        for _, idents in d["scans"]:
            for ident, want in idents:
                BT._get(f"{IA}{ident}/{ident}_djvu.txt", scan_path(ident), want)


def verify():
    for w, d in WORKS.items():
        for name, rel, want in d["files"]:
            p = path(name)
            if not os.path.exists(p):
                raise SystemExit(f"{p} missing: run build_commentary.py --fetch")
            if BT.sha(p) != want:
                raise SystemExit(f"HARD STOP: {p} changed upstream (sha256 mismatch)")


def print_source(s):
    """CCEL's printSourceInfo, and whether a person must look (a year >= 1930)."""
    m = re.search(r"<printSourceInfo>(.*?)</printSourceInfo>", s[:40000], re.S)
    src = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip() if m else None
    years = [int(y) for y in re.findall(r"(?<!\d)(1[5-9]\d\d|20\d\d)(?!\d)", src or "")]
    rights = [x.strip() for x in re.findall(r"<DC\.Rights[^>]*>(.*?)</DC\.Rights>", s[:40000], re.S) if x.strip()]
    return {"ccel_print_source": src, "ccel_print_source_check": bool(years) and max(years) >= 1930,
            "ccel_dc_rights": " / ".join(rights) or None}


# ---------------------------------------------------------------- comments
_EVENT = re.compile(r"<scripCom\b([^>]*)/?>|<div(\d)\b([^>]*)>")
_ATTR = re.compile(r'(\w+)="([^"]*)"')
_DROP = re.compile(r"<h\d\b[^>]*>.*?</h\d>|<p\b[^>]*class=\"(?:Center|t8|passage)\"[^>]*>.*?</p>", re.S)
_PASSAGE = re.compile(r"<p\b[^>]*class=\"passage\"[^>]*>(.*?)</p>", re.S)


def comments(s, work):
    """[{"anchor": (b, c, v, c2, v2), "raw": html, "title": div title, "chapter": n or None}]"""
    body = s[s.find("<ThML.body"):]
    out = []
    cur = None
    title = chapter = None

    def close():
        if cur and cur["anchor"] and R.plain(_DROP.sub("", cur["raw"])):
            out.append(cur)

    pos = 0
    for m in _EVENT.finditer(body):
        if cur is not None:
            cur["raw"] += body[pos:m.start()]
        pos = m.end()
        if m.group(2):                                   # a division starts
            close()
            a = dict(_ATTR.findall(m.group(3)))
            title = a.get("title", "")
            cm = re.match(r"(?:Chapter|CHAPTER|Psalm) (\d+)$", title)
            if cm:
                chapter = int(cm.group(1))
            elif m.group(2) in ("1", "2"):
                chapter = None
            cur = {"anchor": None, "raw": "", "title": title, "chapter": chapter}
            continue
        a = dict(_ATTR.findall(m.group(1)))
        q = R.osis_parts(re.sub(r"^Bible[^:]*:", "", a.get("osisRef", "")).split(" ")[0])
        if q is None:
            continue
        substantive = cur is not None and R.plain(_DROP.sub("", cur["raw"]))
        if cur is None:
            cur = {"anchor": q, "raw": "", "title": title, "chapter": chapter}
        elif cur["anchor"] is None:
            cur["anchor"] = q
            if substantive and q[2] is None:             # a chapter's introduction, before its mark
                close()
                cur = {"anchor": q, "raw": "", "title": title, "chapter": chapter}
        elif not substantive:
            old = cur["anchor"]
            # keep the more precise of two marks on one place (Barnes: verse, then chapter)
            if not (q[2] is None and old[2] is not None and old[:2] == q[:2]):
                cur["anchor"] = q
        else:
            close()
            cur = {"anchor": q, "raw": "", "title": title, "chapter": chapter}
    if cur is not None:
        cur["raw"] += body[pos:]
        close()
    return out


def second_reading(c, work):
    """Where the comment's own text says it is, (b, c, v, c2, v2) or None."""
    b, ch = c["anchor"][0], c["anchor"][1]
    if work == "henry":
        nums = []
        for p in _PASSAGE.findall(c["raw"]):
            nums += [int(x) for x in re.findall(r"(?:^|\s)(\d{1,3})\s(?=[A-Z(])", R.plain(p))]
        if not nums:
            return None
        return (b, ch, nums[0], ch, nums[-1])
    if work == "jfb":
        m = re.search(r"<b>\s*(\d{1,3})\.", c["raw"])
        if not m or c["chapter"] is None:
            return None
        return (b, c["chapter"], int(m.group(1)), c["chapter"], int(m.group(1)))
    if work == "barnes":
        m = re.match(r"(.+?) (\d+):(\d+)$", c["title"] or "")
        if not m or m.group(1) not in _FULL:
            return None
        return (_FULL[m.group(1)], int(m.group(2)), int(m.group(3)), int(m.group(2)), int(m.group(3)))
    return None


def anchor_check(c, work):
    s = second_reading(c, work)
    if s is None:
        return "unread"
    a = c["anchor"]
    if a[2] is None:
        return "unread"
    if work == "jfb":                      # a lemma opens the comment on its first verse
        return "agrees" if s[:3] == a[:3] else "differs"
    return "agrees" if (s[0], s[1], s[2], s[4]) == (a[0], a[1], a[2], a[4] if a[4] is not None else a[2]) else "differs"


def cites(c):
    """The comment's citations as candidates (the same vote as build_topical)."""
    raw = _DROP.sub("", c["raw"])
    tags = []
    for m in re.finditer(r"<scripRef\b([^>]*)>", raw):
        o = dict(_ATTR.findall(m.group(1))).get("osisRef", "")
        tags.append({"osis": re.sub(r"^Bible[^:]*:", "", o)})
    para = {"text": R.plain(raw), "tagged": tags}
    return BT.candidates(para, here=c["anchor"][:2])


def build_work(work, shape):
    d = WORKS[work]
    rows, prose, rejected = [], [], []
    counts = collections.Counter()
    sources = []
    items = []                      # (comment, on, anchor check, [candidates])
    for name, rel, want in d["files"]:
        with open(path(name), encoding="utf-8") as f:
            s = f.read()
        ps = print_source(s)
        sources.append({"file": name, "url": CCEL + rel, "sha256": want, **ps})
        for c in comments(s, work):
            on, why = BT.kjv_id(c["anchor"], shape, BT.APOCRYPHA)
            if on is None:
                counts["anchor names no KJV verse"] += 1
                rejected.append({"anchor": list(c["anchor"]), "why": why, "text": R.plain(c["raw"])[:300]})
                continue
            items.append((c, on, anchor_check(c, work), cites(c)))

    # print: a citation that names its own book and chapter (not "ver. 3",
    # which only the comment's place resolves) is looked for in each printing,
    # aligned in order; the printings' references are read with no context.
    seq, where = [], []
    for k, (c, on, ac, cands) in enumerate(items):
        for j, x in enumerate(cands):
            if x["t"][0] != "?" and x["t"][:2] != c["anchor"][:2] and c["anchor"][0] in d.get("print_books", c["anchor"][:1]):
                seq.append("%s %s %s" % x["t"][:3])
                where.append((k, j))
    printed = collections.Counter()
    scan_stats = []
    for printing, idents in d["scans"]:
        text = ""
        for ident, _ in idents:
            with open(scan_path(ident), encoding="utf-8", errors="replace") as f:
                text += f.read() + "\n"
        # print has no comment place to lend "ch. xi. 4" a book, so only the
        # citations that name one are read there; a key without its book
        # repeats too often for diff to align (and is slow to try)
        srefs = ["%s %s %s" % (r["book"], r["c"], r["v"]) for r in R.refs(text, point=True)]
        m = BT.aligned(seq, srefs)
        for i in m:
            printed[where[i]] += 1
        scan_stats.append({"printing": printing, "scans": [i for i, _ in idents], "refs_read": len(srefs),
                           "aligned": len(m)})
    explicit = {w for w in where}

    seen = collections.Counter()
    by_class = collections.defaultdict(lambda: [0, 0])
    for k, (c, on, ac, cands) in enumerate(items):
        counts["anchor " + ac] += 1
        got, shown = [], set()
        for j, x in enumerate(cands):
            cls = "both" if x["ccel"] and x["reader"] else ("ccel-only" if x["ccel"] else "reader-only")
            counts["cite " + cls] += 1
            if (k, j) in explicit:
                by_class[cls][0] += 1
                by_class[cls][1] += bool(printed[(k, j)])
            if not (cls == "both" or printed[(k, j)]):
                rejected.append({"anchor": list(c["anchor"]), "ref": list(x["t"]), "class": cls,
                                 "text": R.plain(c["raw"])[:300]})
                continue
            rid, why = BT.kjv_id(x["t"], shape, BT.APOCRYPHA)
            if rid is None:
                counts["cite names no KJV verse" if why != "apocrypha" else "cite apocrypha"] += 1
                continue
            if printed[(k, j)]:
                shown.add(rid)
            if rid not in got:
                got.append(rid)
        base = on[4:]
        seen[base] += 1
        uid = f"{work}:{base}" if seen[base] == 1 else f"{work}:{base}~{seen[base]}"
        row = {"id": uid, "on": on, "anchor": ac, "cites": got}
        if d["scans"] and c["anchor"][0] in d.get("print_books", c["anchor"][:1]):
            row["in_print"] = len(shown)
        rows.append(row)
        counts["comments"] += 1
        counts["citations"] += len(got)
        prose.append({"id": uid, "text": R.plain(_DROP.sub("", c["raw"]))})
    V = T.Verses(shape)
    covered = set()
    for r in rows:
        b, c, v, c2, v2 = T.parse_ref_id(r["on"])
        covered.update(range(V.index[(b, c, v)], V.index[(b, c2, v2)] + 1))
    counts["verses_covered"] = len(covered)
    measure = {cls: {"refs": n, "printed": p, "share_printed": round(p / n, 4) if n else None}
               for cls, (n, p) in sorted(by_class.items())}
    return rows, prose, rejected, dict(sorted(counts.items())), sources, measure, scan_stats


# ---------------------------------------------------------------- Poole (EEBO-TCP)
# The 1683/85 folio prints the KJV text with its verse numbers inline ("2. And
# the Earth", "33 And every"), Poole's notes at the foot keyed to a word of
# the verse (<note place="bottom">), and the parallel places in the margin
# (<note place="margin">). TCP keyed it by hand from the page images and
# marks what it could not read (<gap>), never guessing.
NS = "{http://www.tei-c.org/ns/1.0}"
# a note's place in the text; a page TCP's images lack; a verse number
_TCP_EV = re.compile(r"\x00(\d+)\x00|\x01|(?<![\w〉◊,.:;\-\x00])(\d{1,3})[.,▪]?(?=\s*[^\s\d.,▪])")
_GAP = " \u25ca "            # an unread word, letter or Greek: never read across


def tcp_flat(e):
    """A note's text: a gap is a mark nothing is read across; an end-of-line hyphen joins."""
    out = []

    def go(x, top=False):
        tag = x.tag[len(NS):]
        if tag == "gap":
            out.append(_GAP)
        elif tag == "g" and x.get("ref") == "char:EOLhyphen":
            pass
        elif tag == "note" and not top:
            pass
        else:
            if x.text:
                out.append(x.text)
            for c in x:
                go(c)
                out.append(c.tail or "")
    go(e, True)
    return " ".join("".join(out).split())


def _tcp_stream(e, out):
    tag = e.tag[len(NS):]
    if tag == "note":
        out.append(("note", e))
        return
    if tag == "gap":
        out.append(("missing" if e.get("reason") == "missing" else "t", _GAP))
        return
    if tag == "head":
        return
    if not (tag == "g" and e.get("ref") == "char:EOLhyphen") and e.text:
        out.append(("t", e.text))
    for c in e:
        _tcp_stream(c, out)
        if c.tail:
            out.append(("t", c.tail))


def tcp_chapter(b, c, el, n_verses, counts):
    """One chapter -> [(verse, {"notes": [...], "margin": [...]})], and how its
    verse numbers read: "agrees" (2..N in order), "by order" (a misprinted
    number between two right ones, read as the one between), "differs"."""
    seg = []
    _tcp_stream(el, seg)
    notes, parts = [], []
    for k, x in seg:
        if k == "note":
            parts.append(" \x00%d\x00 " % len(notes))
            notes.append(x)
        elif k == "missing":
            parts.append(" \x01 ")
        else:
            parts.append(x)
    ev = list(_TCP_EV.finditer("".join(parts)))
    nums = {i: int(m.group(2)) for i, m in enumerate(ev) if m.group(2)}
    keys = sorted(nums)
    fixed = 0
    for a, i, z in zip(keys, keys[1:], keys[2:]):          # Exod 29 prints 36 twice: the second is 37
        if nums[a] + 2 == nums[z] and nums[i] != nums[a] + 1 and 1 < nums[a] + 1 <= n_verses:
            nums[i] = nums[a] + 1
            fixed += 1
    cur, seen, dead = 1, [1], False
    com = {}
    for i, m in enumerate(ev):
        if m.group(0) == "\x01":                           # pages missing from the images: the rest is unplaced
            dead = True
            counts["chapters with pages missing"] += 1
            continue
        if m.group(1) is not None:
            x = notes[int(m.group(1))]
            if dead:
                counts["notes after missing pages, dropped"] += 1
                continue
            com.setdefault(cur, {"notes": [], "margin": []})["margin" if x.get("place") == "margin" else "notes"].append(tcp_flat(x))
            continue
        if dead:
            continue
        n = nums[i]
        if cur < n <= min(cur + 3, n_verses):
            cur = n
            seen.append(n)
    counts["verse numbers misprinted, read by order"] += fixed
    full = seen == list(range(1, n_verses + 1))
    return sorted(com.items()), ("by order" if fixed else "agrees") if full and not dead else "differs"


def tcp_books(work):
    """The book divisions, in canonical order, of every volume."""
    import xml.etree.ElementTree as ET
    out = []
    for name, _, _ in WORKS[work]["files"]:
        root = ET.parse(path(name)).getroot()
        for d in root.find(".//" + NS + "text").iter(NS + "div"):
            if d.get("type") in ("book", "biblical_commentary"):
                out.append(d)
    return out


def tcp_header(name):
    with open(path(name), encoding="utf-8") as f:
        head = f.read(20000)
    date = re.search(r"<edition>\s*<date>([^<]+)</date>", head)
    cc0 = "publicdomain/zero/1.0" in head
    return {"edition_date": date.group(1) if date else None, "tcp_licence": "CC0 1.0" if cc0 else "check"}


def build_tcp_work(work, shape):
    """Poole: one comment per verse that has a note. One reading of each
    citation (the transcription is hand-keyed, double-checked by TCP; there is
    no second text): committed when it names a KJV verse and no unread word
    touches it."""
    d = WORKS[work]
    order = list(shape)
    books = tcp_books(work)
    if len(books) != len(order):
        raise SystemExit(f"{work}: {len(books)} book divisions, not {len(order)}")
    rows, prose, rejected = [], [], []
    counts = collections.Counter()
    sources = [{"file": n, "url": u, "sha256": w, **tcp_header(n)} for n, u, w in d["files"]]
    for b, div in zip(order, books):
        chs = [x for x in div.iter(NS + "div") if x.get("type") in ("chapter", "Psalm")] or [div]
        ns = [int(x.get("n") or 1) for x in chs]
        for i in range(1, len(ns) - 1):        # Psalm 45 is headed "PSAL. LXV.": read by its order
            if ns[i] != ns[i - 1] + 1 and ns[i - 1] + 2 == ns[i + 1]:
                ns[i] = ns[i - 1] + 1
                counts["chapter numbers misprinted, read by order"] += 1
        for x, c in zip(chs, ns):
            if c not in shape[b]:
                counts["chapter names no KJV chapter"] += 1
                continue
            verses, ac = tcp_chapter(b, c, x, shape[b][c], counts)
            counts["chapters " + ac] += 1
            for v, got in verses:
                cites, pars = [], []
                for kind, dest in (("notes", cites), ("margin", pars)):
                    for t in got[kind]:
                        for r in R.refs(t, here=(b, c), point=True, old=True):
                            if "\u25ca" in t[max(0, r["at"] - 2):r["at"] + 18]:
                                counts["cite next to an unread word, dropped"] += 1
                                rejected.append({"on": [b, c, v], "ref": [r["book"], r["c"], r["v"]], "why": "unread word",
                                                 "text": t[max(0, r["at"] - 40):r["at"] + 40]})
                                continue
                            rid, why = BT.kjv_id((r["book"], r["c"], r["v"], r["c2"], r["v2"]), shape, BT.APOCRYPHA)
                            if rid is None:
                                counts["cite apocrypha" if why == "apocrypha" else "cite names no KJV verse"] += 1
                                if why != "apocrypha":
                                    rejected.append({"on": [b, c, v], "ref": [r["book"], r["c"], r["v"]], "why": why,
                                                     "text": t[max(0, r["at"] - 40):r["at"] + 40]})
                                continue
                            if rid not in dest:
                                dest.append(rid)
                on = "kjv:%s.%d.%d" % (b, c, v)
                row = {"id": f"{work}:{on[4:]}", "on": on, "anchor": ac, "cites": cites, "parallels": pars}
                rows.append(row)
                counts["comments"] += 1
                counts["notes"] += len(got["notes"])
                counts["citations"] += len(cites)
                counts["parallels"] += len(pars)
                counts["unread words in the notes"] += sum(t.count("\u25ca") for t in got["notes"] + got["margin"])
                prose.append({"id": row["id"], "notes": got["notes"], "margin": got["margin"]})
    counts["verses_covered"] = len(rows)
    return rows, prose, rejected, dict(sorted(counts.items())), sources, None, []


def treasury_measure(rows, shape):
    """An outside check: the share of a work's citations that the Treasury
    (data/xrefs/tsk.jsonl, read from its own 1830s scans) also lists at the
    same verse, against the share at an unrelated verse (the verse 1,000 on).
    A measure only: nothing is kept or dropped by it."""
    p = os.path.join(ROOT, "data", "xrefs", "tsk.jsonl")
    if not os.path.exists(p):
        return None
    V = T.Verses(shape)

    def verses(rid):
        b, c, v, c2, v2 = T.parse_ref_id(rid)
        return range(V.index[(b, c, v)], V.index[(b, c2, v2)] + 1)
    tsk = {}
    with open(p, encoding="utf-8") as f:
        for raw in f:
            r = json.loads(raw)
            tsk[r["verse"]] = {k for g in r["groups"] for x in g["refs"] for k in verses(x)}
    out = {}
    for kind in ("cites", "parallels"):
        n = hit = base = 0
        for r in rows:
            if kind not in r:
                continue
            on = [V.seq[k] for k in verses(r["on"])]       # a comment on a passage: the Treasury on any verse of it
            mine = set().union(*(tsk.get("kjv:%s.%d.%d" % x, set()) for x in on))
            other = set().union(*(tsk.get("kjv:%s.%d.%d" % V.seq[(V.index[x] + 1000) % len(V.seq)], set()) for x in on))
            if not mine:
                continue
            for x in r[kind]:
                vs = set(verses(x))
                n += 1
                hit += bool(vs & mine)
                base += bool(vs & other)
        if n:
            out[kind] = {"refs": n, "in_treasury_at_that_verse": round(hit / n, 4),
                         "in_treasury_at_an_unrelated_verse": round(base / n, 4)}
    return out


def scan_path(ident):
    return os.path.join(CORPUS, "scans", ident + ".txt")


def build(write=True):
    verify()
    shape = T.kjv_shape()
    files, layers = {}, {}
    for w, d in WORKS.items():
        print(f"{w}: reading")
        if d.get("kind") == "tcp":
            rows, prose, rejected, counts, sources, measure, scans = build_tcp_work(w, shape)
        else:
            rows, prose, rejected, counts, sources, measure, scans = build_work(w, shape)
        files[f"{w}.jsonl"] = BT.dumps(rows)
        layers[w] = {"file": f"data/commentary/{w}.jsonl",
                     "sha256": hashlib.sha256(files[f"{w}.jsonl"].encode()).hexdigest(),
                     "rows": len(rows), "counts": counts,
                     "explicit_citations_by_reading": measure, "print_check": scans,
                     "treasury_check": treasury_measure(rows, shape),
                     "source": {"title": d["title"], "author": d["author"],
                                "edition": "EEBO-TCP TEI (hand-keyed from the first edition)" if d.get("kind") == "tcp" else "CCEL ThML",
                                "files": sources}}
        print(f"  {counts}")
        if write:
            os.makedirs(BUILD, exist_ok=True)
            for name, data in ((f"{w}.rejected.jsonl", rejected), (f"{w}.text.jsonl", prose)):
                tmp = os.path.join(BUILD, name + ".tmp")
                with open(tmp, "w", encoding="utf-8") as f:
                    f.write(BT.dumps(data))
                os.replace(tmp, os.path.join(BUILD, name))
    manifest = {"about": "Whole-Bible commentaries keyed to KJV verse ids. pipeline/build_commentary.py; rules in pipeline/README-commentary.md",
                "rights": RIGHTS, "layers": layers}
    files["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    if write:
        os.makedirs(OUT, exist_ok=True)
        for name, data in files.items():
            tmp = os.path.join(OUT, name + ".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(data)
            os.replace(tmp, os.path.join(OUT, name))
        print("wrote " + ", ".join(f"data/commentary/{n}" for n in files))
    return files


# ---------------------------------------------------------------- collation
# Is CCEL's wording the period wording? A fixed sample of comments is found
# in each work's scans (a four-word run that occurs once there) and its next
# 80 words are aligned with the scan's. What differs is counted: the old
# forms print has where CCEL has another word, and -our / -or spellings.
ARCHAIC = {"hath", "doth", "saith", "spake", "shew", "shewed", "shewn", "unto", "toward", "afterward",
           "exceeding", "ye", "thee", "thou", "thy", "hast", "dost", "whilst", "amongst", "betwixt", "viz"}


def collate(work, n=400):
    import difflib
    import random
    d = WORKS[work]
    words = lambda t: [w.lower() for w in re.findall(r"[A-Za-z]+", t)]
    out = {}
    for printing, idents in d["scans"]:
        sc = []
        for ident, _ in idents:
            with open(scan_path(ident), encoding="utf-8", errors="replace") as f:
                sc += words(f.read())
        idx = collections.defaultdict(list)
        for i in range(len(sc) - 3):
            idx[" ".join(sc[i:i + 4])].append(i)
        rows = []
        with open(os.path.join(BUILD, work + ".text.jsonl"), encoding="utf-8") as f:
            for raw in f:
                r = json.loads(raw)
                if r["id"].split(":")[1].split(".")[0] in d.get("print_books", {r["id"].split(":")[1].split(".")[0]}):
                    if len(words(r["text"])) > 120:
                        rows.append(r)
        rnd = random.Random(1)
        sample = rnd.sample(rows, min(n, len(rows)))
        found = tot = same = 0
        old_new, kept, spell = collections.Counter(), collections.Counter(), collections.Counter()
        for r in sample:
            cw = words(r["text"])
            hit = next(((k, idx[g][0]) for k in range(20, len(cw) - 80, 7)
                        for g in [" ".join(cw[k:k + 4])] if len(idx.get(g, ())) == 1), None)
            if not hit:
                continue
            a, b = cw[hit[0]:hit[0] + 80], sc[hit[1]:hit[1] + 90]
            sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
            m = sum(x.size for x in sm.get_matching_blocks())
            if m < 50:
                continue
            found += 1
            tot += len(a)
            same += m
            for op, a1, a2, b1, b2 in sm.get_opcodes():
                if op == "equal":
                    kept.update(w for w in a[a1:a2] if w in ARCHAIC)
                elif op == "replace" and a2 - a1 == 1 and b2 - b1 == 1:
                    x, y = a[a1], b[b1]
                    if y in ARCHAIC and x != y:
                        old_new[f"{y} -> {x}"] += 1
                    if x.replace("our", "or") == y and x != y:
                        spell["CCEL -our, print -or"] += 1
                    if y.replace("our", "or") == x and x != y:
                        spell["CCEL -or, print -our"] += 1
        out[printing] = {"sampled": len(sample), "located": found, "word_agreement": round(same / tot, 4) if tot else None,
                         "print_old_form_ccel_other": dict(old_new.most_common(12)),
                         "old_forms_kept": dict(kept.most_common(8)), "spelling": dict(spell)}
    return out


def collate_all():
    res = {w: collate(w) for w, d in WORKS.items() if d["scans"]}
    p = os.path.join(OUT, "collation.json")
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    os.replace(tmp, p)
    print(json.dumps(res, indent=1))


def check():
    files = build(write=False)
    bad = [n for n, data in files.items()
           if not os.path.exists(os.path.join(OUT, n)) or open(os.path.join(OUT, n), encoding="utf-8").read() != data]
    if bad:
        raise SystemExit("check: differs: " + ", ".join(bad))
    print("check: byte-identical")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--collate", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    elif a.collate:
        collate_all()
    elif a.check:
        check()
    else:
        build()


if __name__ == "__main__":
    main()
