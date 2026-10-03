#!/usr/bin/env python3
"""
build_schaff.py -- the Ante-Nicene Fathers (10 vols) and the Nicene and
Post-Nicene Fathers, series 1 and 2 (14 + 14 vols), ed. Philip Schaff et al.,
in English, from CCEL's ThML; and their alignment to the Greek and Latin
fathers already in the collection.

    python3 pipeline/build_schaff.py --fetch   # pinned ThML -> data/corpus/schaff/ (gitignored)
    python3 pipeline/build_schaff.py           # build data/books/schaff-*.json + work books + manifest
    python3 pipeline/build_schaff.py --check   # rebuild in memory: = the committed manifest entries
    python3 pipeline/build_schaff.py --report  # print the counts; writes nothing
    python3 tests/schaff_test.py               # offline, fixtures inline

SOURCE. CCEL's ThML of each volume, https://ccel.org/ccel/s/schaff/<vol>.xml,
pinned by sha256 in schaff_pins.json (CCEL is not a git repo, so the pin is
the file itself; two fetches a day apart gave the same bytes). A fetched file
whose sha256 is not the pin is refused: re-read it, then re-pin.

LICENCE (rule 6). The print edition is 1885-1900 and public domain. Each
file's own rights line is READ at build time, not assumed: every file's
<DC.Rights> reads "Public Domain" (a build stops if one does not), and 37 of
the 38 carry the comment "Copyright Christian Classics Ethereal Library" over
CCEL's electronic edition (anf01 has no such comment). CCEL's copyright page
(read 2026-10-02, RIGHTS["ccel_policy"]) asks that its editions be used "for
personal, educational, or non-profit purposes" and that permission be asked
to republish them or use them commercially. So these books are handled like
the CC BY-SA fathers: built locally, gitignored, the manifest entry committed
with a `rights` block, `redistribute_whole: false`, `commercial: ask CCEL`.

VOLUME BOOKS (`schaff-anf01` .. `schaff-npnf214`). One unit per block of the
print text: a paragraph (<p>), a stanza of verse (<verse>), a table. The unit
id is CCEL's own id for that paragraph (`schaff-anf01:viii.ii.ii-p1`), which
is also the anchor of its page at ccel.org, so the citation resolves on the
site. Each unit records the CCEL division it is in (`div`; titles in the
book's `divs` table), the print page it starts on (`page`, from <pb n>) and,
if it runs over, the page it ends on. Footnotes are lifted out of the running
text into `notes` (number as printed, text, their own scripture links), never
mixed in and never dropped. Scripture references (<scripRef>) are harvested
into links[] exactly as structure_texts.convert_thml does (its RE_SCRIP and
RE_SCRIP_PARSED), from the text and its notes; CCEL's empty commentary
markers (<scripCom>) go in `comments_on`. Headings are division titles, not
units. Left out, and counted per volume: CCEL's generated "Indexes" division
(scripture, Greek, Latin and page indexes made by CCEL, not printed by
Schaff) and the <div class="Index"> blocks inside it.

ANF10 on CCEL is a "Digital Facsimile edition": page images, no text. It is
built as a book of 0 units whose scheme says so, so the ledger records that
the volume was fetched and what it holds.

WORK BOOKS (ALIGNED). For each Greek or Latin work in the collection (the
First1KGreek and CSEL fathers, PR #7) that Schaff translates, a work book
`<counterpart slug minus -grc/-lat>-schaff` is cut from the volume: one unit
per chapter (or letter, oration, homily) at the finest level the English
numbers, keyed in the counterpart's own numbering (`justin-apology-1-schaff:5`
is 1 Apol. 5). Its text is the chapter's paragraphs from the volume book, and
`paragraphs` names those units, so the work book is a view of the volume, not
a second witness. Each unit links to the counterpart unit(s) it translates:
where the Greek is cut finer (chapter.section), the English chapter links to
every section of that chapter. An English chapter with no counterpart, or a
counterpart unit with no English, is listed under `alignment.unmatched`;
nothing is stretched to cover it. See WORKS for the table and ALIGN_NOTES for
what was checked.

The alignment is MEASURED, not claimed (measure(), verdict()): for every
work, (a) the Pearson r of log English chapter length against log counterpart
chapter length, on the diagonal and one chapter off either way (a numbering
slip shows up off the diagonal), and (b) the share of the English chapter's
capitalized words whose first five letters, spelled alike, occur in the
counterpart chapter, on and off the diagonal. A work is aligned only if the
diagonal is clearly best (length r >= 0.7 and above both offsets; or names
>= 0.2 and 1.5 times both offsets; or every unit on both sides paired and
the diagonal r above both offsets). Otherwise it is REFUSED: the work book is
still built, but no unit carries a link, and the manifest says why. Every
row was tried at its finest level first; where that was refused and a
coarser level (the book) passes, the coarser level is used and the finer
refusal is recorded in FINER_REFUSED.

CYPRIAN (ANF 5) is cut into work books the same way (`cyprian-epistles-schaff`,
`cyprian-treatises-schaff`, ...), though no Latin text of Cyprian is on GitHub
in a TEI edition (CSEL 3, Hartel 1868-71: no stoa0104 in csel-dev or
canonical-latinLit, checked 2026-10-03): they carry
no counterpart, and their manifest note says so.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import structure_texts as ST  # noqa: E402  (RE_SCRIP / RE_SCRIP_PARSED: the ThML link harvest)

BOOKS = os.environ.get("BOOKS_OUT") or os.path.join(ROOT, "data", "books")
MANIFEST = os.path.join(ROOT, "data", "books", "manifest.json")
CORPUS = os.path.join(ROOT, "data", "corpus", "schaff")
PINS_PATH = os.path.join(HERE, "schaff_pins.json")
URL = "https://ccel.org/ccel/s/schaff/{vol}.xml"
UA = "Canon-Corpus/0.1 (personal library research)"

# vol code -> (series label, volume number as cited: "ANF 1", "NPNF1 1", "NPNF2 1")
VOLUMES = {f"anf{i:02d}": ("ANF", i) for i in range(1, 11)}
VOLUMES.update({f"npnf1{i:02d}": ("NPNF1", i) for i in range(1, 15)})
VOLUMES.update({f"npnf2{i:02d}": ("NPNF2", i) for i in range(1, 15)})

RIGHTS = {
    "license": "public domain (the print edition, 1885-1900); CCEL's electronic edition is "
               "marked \"Copyright Christian Classics Ethereal Library\"",
    "attribution": "Christian Classics Ethereal Library (ccel.org), Calvin University",
    "redistribute_whole": False,
    "commercial": "ask CCEL",
    "ccel_policy": {
        "url": "https://www.ccel.org/about/copyright.html",
        "read": "2026-10-02",
        "text": "Most of the editions at the Christian Classics Ethereal library are based on "
                "books that are public domain in the United States. However, they may have "
                "copyrighted introductions, cover art, and other special contents. [...] These "
                "books may be used for personal, educational, or non-profit purposes. Contact us "
                "for permission to republish CCEL works or to use them commercially.",
    },
}

DIV = re.compile(r"^div([1-6])$")
SKIP_IN_TEXT = {"note", "index", "insertIndex", "img", "scripCom"}
SPACE = re.compile(r"\s+")


def sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def write_atomic(path, data):
    with open(path + ".tmp", "wb") as f:
        f.write(data)
    os.replace(path + ".tmp", path)


def pins():
    with open(PINS_PATH, encoding="utf-8") as f:
        return json.load(f)


def local(vol):
    return os.path.join(CORPUS, vol + ".xml")


def fetch():
    """Each pinned volume not yet present, sha256-checked before it is kept."""
    os.makedirs(CORPUS, exist_ok=True)
    for vol, want in pins().items():
        dest = local(vol)
        if os.path.exists(dest) and sha256_file(dest) == want:
            continue
        for wait in (2, 4, 8, 16, None):
            try:
                req = urllib.request.Request(URL.format(vol=vol), headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=120) as r:
                    blob = r.read()
                break
            except (urllib.error.URLError, ConnectionError, TimeoutError):
                if wait is None:
                    raise
                time.sleep(wait)
        got = hashlib.sha256(blob).hexdigest()
        if got != want:
            raise SystemExit(f"HARD STOP: {vol}: CCEL served {got[:12]}, pinned {want[:12]}; "
                             f"read the new file's rights line and structure, then re-pin")
        write_atomic(dest, blob)
        print(f"  fetched {vol}: {len(blob):,} bytes")
        time.sleep(1.0)  # be polite to CCEL


def verify_pins():
    bad = [v for v, want in pins().items()
           if not os.path.exists(local(v)) or sha256_file(local(v)) != want]
    if bad:
        raise SystemExit(f"pinned inputs missing or changed: {bad[:4]}\n"
                         f"  run: python3 pipeline/build_schaff.py --fetch")


# ---------------------------------------------------------------- reading ThML

def flat(s):
    return SPACE.sub(" ", s).strip()


def text_of(el, page=None):
    """The running text of a block: notes, index entries, images and markers
    left out (their tails kept); <br> is a space. `page`, if given, is a
    one-item list updated by every <pb> met inside, so a paragraph that runs
    over a page knows where it ends."""
    out = [el.text or ""]
    for c in el:
        if c.tag == "pb":
            if page is not None and c.get("n"):
                page[0] = c.get("n")
        elif c.tag not in SKIP_IN_TEXT:
            out.append(text_of(c, page))
        out.append(" " + (c.tail or "") if c.tag == "br" else c.tail or "")
    return "".join(out)


def verse_text(el, page=None):
    """A stanza: one line per <l>, else the text as it stands."""
    lines = [flat(text_of(l, page)) for l in el.iter("l")]
    lines = [l for l in lines if l]
    return "\n".join(lines) if lines else flat(text_of(el, page))


def table_text(el, page=None):
    rows = []
    for tr in el.iter("tr"):
        cells = [flat(text_of(td, page)) for td in tr if td.tag in ("td", "th")]
        if any(cells):
            rows.append(" | ".join(cells))
    return "\n".join(rows) if rows else flat(text_of(el, page))


def links_of(el):
    """Scripture references inside `el`, harvested as convert_thml does."""
    raw = ET.tostring(el, encoding="unicode")
    found = set()
    for m in ST.RE_SCRIP.findall(raw):
        # one osisRef may hold several references ("Bible:Gen.1.1 Bible:Gen.1.2")
        for part in m.split():
            part = re.sub(r"^Bible[^:]*:", "", part)
            if part:
                found.add(part)
    found |= {f"{b}.{c}.{v}" for b, c, v in ST.RE_SCRIP_PARSED.findall(raw)}
    return sorted(found)


def notes_of(el):
    out = []
    for n in el.iter("note"):
        t = flat(text_of(n))
        if t:
            out.append({"n": n.get("n") or "", "text": t, "links": links_of(n)})
    return out


def head_info(root):
    head = root.find("ThML.head")
    g = lambda path: [flat("".join(e.itertext())) for e in head.iter(path)]  # noqa: E731
    rights = g("DC.Rights")
    return {"title": (g("DC.Title") or [""])[0], "rights": rights,
            "creator": (g("DC.Creator") or [""])[0], "status": " ".join(g("status")),
            "published": " ".join(g("published")), "created": " ".join(g("DC.Date"))}


def is_generated_index(div):
    """CCEL's own indexes (div1 "Indexes"), not part of the printed volume."""
    return div.tag == "div1" and flat(div.get("title", "")) == "Indexes"


def read_volume(raw_bytes, vol):
    """(units, divs, info, skipped) for one ThML volume."""
    root = ET.fromstring(raw_bytes)
    info = head_info(root)
    if info["rights"] != ["Public Domain"]:
        raise SystemExit(f"HARD STOP: {vol}: DC.Rights reads {info['rights']!r}, not "
                         f"'Public Domain'; read the rights before building")
    body = root.find("ThML.body")
    units, divs = [], {}
    skipped = {"generated_index_divs": 0, "generated_index_blocks": 0}
    page = [None]
    pending_com = []
    seen = set()

    def emit(el, div_id, kind):
        start = page[0]
        if kind == "verse":
            t = verse_text(el, page)
        elif kind == "table":
            t = table_text(el, page)
        else:
            t = flat(text_of(el, page))
        if not t:
            return
        uid = el.get("id") or f"{div_id}-u{len(units) + 1}"
        if uid in seen:
            raise SystemExit(f"HARD STOP: {vol}: two blocks carry the id {uid}")
        seen.add(uid)
        u = {"id": f"schaff-{vol}:{uid}", "ref": "", "text": t, "links": links_of(el),
             "div": div_id, "page": start}
        if page[0] != start:
            u["page_end"] = page[0]
        notes = notes_of(el)
        if notes:
            u["notes"] = notes
        com = [x.get("osisRef", "").split(":", 1)[-1] for x in el.iter("scripCom")]
        com = pending_com + [c for c in com if c]
        if com:
            u["comments_on"] = com
            pending_com.clear()
        units.append(u)

    def walk(el, div_id):
        for c in el:
            if DIV.match(c.tag):
                if is_generated_index(c):
                    skipped["generated_index_divs"] += 1
                    skipped["generated_index_blocks"] += sum(1 for _ in c.iter("p"))
                    continue
                did = c.get("id") or f"{div_id}.{len(divs)}"
                divs[did] = {"title": flat(c.get("title", "")), "parent": div_id,
                             "level": int(c.tag[3:]), "number": div_number(c)}
                if c.get("type"):
                    divs[did]["type"] = c.get("type")
                walk(c, did)
            elif c.tag == "pb":
                if c.get("n"):
                    page[0] = c.get("n")
            elif c.tag == "p":
                emit(c, div_id, "p")
            elif c.tag == "verse":
                emit(c, div_id, "verse")
            elif c.tag == "table":
                emit(c, div_id, "table")
            elif c.tag == "scripCom":
                if c.get("osisRef"):
                    pending_com.append(c.get("osisRef").split(":", 1)[-1])
            elif c.tag == "div":
                # <div class="Index">: CCEL's generated index blocks
                skipped["generated_index_blocks"] += sum(1 for _ in c.iter("p"))
            elif c.tag in ("ol", "ul"):
                for li in c.iter("li"):
                    emit(li, div_id, "p")
            # headings (h1-h6) are division titles; ThML.head inside the body is
            # CCEL's per-work catalogue record; hr is a rule.
            elif c.tag in ("blockquote",):
                walk(c, div_id)

    walk(body, None)
    series, n = VOLUMES[vol]
    for u in units:
        u["ref"] = f"{series} {n}:{u['page']}" if u["page"] else f"{series} {n}"
    return units, divs, info, skipped


def convert_volume(vol, path=None):
    path = path or local(vol)
    with open(path, "rb") as f:
        raw = f.read()
    units, divs, info, skipped = read_volume(raw, vol)
    fill_numbers(divs)
    series, n = VOLUMES[vol]
    facsimile = not units and "Facsimile" in info["status"]
    has_comment = b"<!-- Copyright Christian Classics Ethereal Library -->" in raw[:4000]
    rights = dict(RIGHTS)
    rights["rights_line_as_read"] = {"DC.Rights": info["rights"][0],
                                     "file_comment": ("Copyright Christian Classics Ethereal Library"
                                                      if has_comment else None)}
    rights["source_url"] = URL.format(vol=vol)
    return {
        "slug": f"schaff-{vol}",
        "title": info["title"],
        "author": "ed. Philip Schaff" + (" and Henry Wace" if series == "NPNF2" else ""),
        "source": {"path": os.path.relpath(path, os.path.join(ROOT, "data", "corpus")),
                   "format": "thml-ccel", "url": URL.format(vol=vol), "sha256": sha256_file(path),
                   "series": series, "volume": n, "ccel_status": info["status"] or None,
                   "printed": info["published"] or None, "ccel_created": info["created"] or None},
        "scheme": {
            "citation": f"{series} {n}:<print page>; unit id = CCEL paragraph id",
            "resolution": "paragraph" if not facsimile else "none (page images only)",
            "honesty": ("exact to CCEL's paragraphs, whose ids are CCEL's stable anchors; the print "
                        "page is the <pb> before the paragraph (page_end if it runs over). Footnotes "
                        "are in `notes`, not `text`. CCEL's own proofing note is in "
                        "source.ccel_status." if not facsimile else
                        "CCEL's edition of this volume is a digital facsimile (page images); there "
                        "is no text to unit, so the book has none"),
            "note": "headings are division titles (book.divs), not units; CCEL's generated indexes "
                    "left out (counts in `skipped`)",
        },
        "rights": rights,
        "skipped": skipped,
        "divs": divs,
        "units": units,
    }


# ---------------------------------------------------------------- numbering

ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}
ORDINAL = {w: i for i, w in enumerate(
    "first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth "
    "thirteenth fourteenth fifteenth sixteenth seventeenth eighteenth nineteenth twentieth"
    .split(), 1)}
NUMBERED_TYPES = {"book", "chapter", "letter", "epistle", "section", "homily", "oration",
                  "sermon", "tractate", "lecture", "part", "treatise", "psalm", "canon",
                  "discourse", "dialogue", "conference", "testament", "version", "division"}
KEYWORD = re.compile(r"\b(?:Book|Chapter|Chap\.|Letter|Epistle|Oration|Homily|Sermon|Lecture|"
                     r"Section|Treatise|Tractate|Discourse|Dialogue|Conference|Psalm|Part)\s+"
                     r"(?:the\s+)?([IVXLCDM]+|\d+|[A-Z][a-z]+)\b\.?")
LEADING = re.compile(r"^\s*\[?([IVXLCDM]+|\d+)\]?(?:[.:]|\s*[—–-]|$)")
SAID = re.compile(r"^[A-Z][^:.]{2,80}? said:")
INLINE_NUM = re.compile(r"^\s*(?:Chap(?:ter|\.)\s+)?\[?([IVXLC]+|\d+)\]?\.\s")


def roman(s):
    """An arabic or roman numeral as an int, or None."""
    s = s.strip().rstrip(".")
    if s.isdigit():
        return int(s)
    s = s.lower()
    if not s or any(ch not in ROMAN for ch in s):
        return None
    total = 0
    for i, ch in enumerate(s):
        v = ROMAN[ch]
        total += -v if i + 1 < len(s) and ROMAN[s[i + 1]] > v else v
    return total


def div_number(div):
    """The number the print edition gives a division, or None if it gives
    none (a preface, an introduction, a title page).

    1. CCEL's own `type` + `n` (type="Chapter" n="XVII"), where CCEL typed it.
    2. The title: "Chapter II.—Justice demanded.", "Book First.—Visions".
    3. A numeral opening the title: "XII. To Eustochium".
    """
    t = (div.get("type") or "").lower()
    if t in NUMBERED_TYPES and div.get("n"):
        n = roman(div.get("n"))
        if n is not None:
            return n
    title = flat(div.get("title") or "")
    m = KEYWORD.search(title)
    if m:
        w = m.group(1)
        n = ORDINAL.get(w.lower()) if w.istitle() and len(w) > 1 and not roman(w) else roman(w)
        if n is not None:
            return n
    m = LEADING.match(title)
    if m:
        return roman(m.group(1))
    return None


def fill_numbers(divs):
    """CCEL often types a run of divisions (type="Chapter") but gives `n`
    only to the first (at least four in five of the rest have none), and the title carries no number ("Wide Scope of the
    Word Idolatry."). Where a parent's divisions of one type are numbered
    1, then (nearly) nothing ... they are numbered in order, and marked
    `number_inferred` (a stray stated `n` at odds with its place is kept as
    `number_stated`); a run with any other pattern is left alone. An
    untyped division standing between two of the run (anf03's "Dress as
    Connected with Idolatry." between Chapters XVII and XIX) is one of it.
    The alignment measure then tests the inferred numbers like any other."""
    kids_of = {}
    for k, v in divs.items():
        kids_of.setdefault(v["parent"], []).append(k)
    for kids in kids_of.values():
        types = {}
        for i, k in enumerate(kids):
            if divs[k].get("type"):
                types.setdefault(divs[k]["type"], []).append(i)
        for idx in types.values():
            run = kids[idx[0]: idx[-1] + 1]
            nums = [divs[k]["number"] for k in run]
            if (len(run) > 1 and nums[0] == 1
                    and sum(x is None for x in nums) >= 0.8 * (len(nums) - 1)):
                for i, k in enumerate(run, 1):
                    if divs[k]["number"] != i:
                        if divs[k]["number"] is not None:
                            # a stray n at odds with its place (anf03 Marc. 4.25 says X)
                            divs[k]["number_stated"] = divs[k]["number"]
                        divs[k]["number"] = i
                        divs[k]["number_inferred"] = True


# ---------------------------------------------------------------- work books

def work_chapters(divs, units, work_div, levels):
    """{key: [unit ids]} in document order, and the ids outside any key.

    A key is the print numbers of the numbered divisions under `work_div`, the
    first `levels` of them ("1.5" = book 1, chapter 5). A paragraph belongs to
    the deepest numbered division above it, folded to `levels`; one that sits
    in an unnumbered division, or above the numbered level, has no key."""
    def path(div_id):
        out = []
        while div_id and div_id != work_div:
            out.append(div_id)
            div_id = divs[div_id]["parent"]
        return list(reversed(out)) if div_id == work_div else None

    def div_key(p, depth):
        nums = []
        for d in p:
            n = divs[d].get("number")
            if n is not None:
                nums.append(str(n))
            if len(nums) == depth:
                break
        return ".".join(nums) if len(nums) == depth else None

    chapters, outside, spans = {}, [], {}
    if levels == "speakers":
        # The Seventh Council of Carthage: each bishop's sentence opens
        # "<Name> of <see> said:"; they are numbered in order (the
        # sententiae episcoporum, 1-87 in the editions).
        cur = 0
        for u in units:
            if path(u["div"]) is None:
                continue
            if SAID.match(u["text"]):
                cur += 1
            if cur:
                chapters.setdefault(str(cur), []).append(u["id"])
            else:
                outside.append(u["id"])
        return chapters, outside, spans
    if isinstance(levels, str):
        # "inline" or "<n>+inline": the last level's numbers are printed at
        # the head of a paragraph ("I. Those who ..."), not as divisions.
        # One counts only if it is the next in sequence (restarting under
        # each division of the first n levels), so a numeral that happens to
        # open a paragraph is not taken. One missing numeral (XVII, then XIX)
        # is allowed: the chapter before the gap covers both (`spans`).
        base = int(levels.split("+")[0]) if "+" in levels else 0
        prefix, cur = None, 0
        for u in units:
            p = path(u["div"])
            if p is None:
                continue
            pre = div_key(p, base) if base else ""
            if pre is None:
                outside.append(u["id"])
                continue
            if pre != prefix:
                prefix, cur = pre, 0
            m = INLINE_NUM.match(u["text"])
            n = roman(m.group(1)) if m else None
            if n == cur + 1 or (cur and n == cur + 2):
                if n == cur + 2:
                    spans.setdefault(f"{pre}.{cur}".lstrip("."), []).append(f"{pre}.{cur + 1}".lstrip("."))
                cur = n
            if cur:
                chapters.setdefault(f"{pre}.{cur}".lstrip("."), []).append(u["id"])
            else:
                outside.append(u["id"])
        return chapters, outside, spans
    for u in units:
        p = path(u["div"])
        if p is None:
            continue
        k = div_key(p, levels)
        if k is not None:
            chapters.setdefault(k, []).append(u["id"])
        else:
            outside.append(u["id"])
    return chapters, outside, spans
    for u in units:
        p = path(u["div"])
        if p is None:
            continue
        nums = []
        for d in p:
            n = divs[d].get("number")
            if n is not None:
                nums.append(str(n))
            if len(nums) == levels:
                break
        if len(nums) == levels:
            chapters.setdefault(".".join(nums), []).append(u["id"])
        else:
            outside.append(u["id"])
    return chapters, outside, spans


def pearson(xs, ys):
    import math
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if not sx or not sy:
        return None
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy), 3)


GREEK_LATIN = dict(zip("αβγδεζηθικλμνξοπρσςτυφχψω",
                       ["a", "b", "g", "d", "e", "z", "e", "t", "i", "k", "l", "m", "n", "x", "o",
                        "p", "r", "s", "s", "t", "i", "f", "k", "ps", "o"]))
NAME = re.compile(r"\b[A-Z][a-zæœ]{4,}")
WORD = re.compile(r"[^\W\d_]{5,}")


def name_key(word):
    """A name's first five letters in one spelling for English, Latin and
    Greek: accents off, Greek letters romanized, c/k, ph/f, th/t, y/i, j/i."""
    import unicodedata
    w = "".join(ch for ch in unicodedata.normalize("NFD", word.lower())
                if not unicodedata.combining(ch))
    w = "".join(GREEK_LATIN.get(ch, ch) for ch in w)
    for a, b in (("ph", "f"), ("th", "t"), ("ch", "k"), ("c", "k"), ("y", "i"), ("j", "i"),
                 ("æ", "ae"), ("œ", "oe")):
        w = w.replace(a, b)
    return w[:5]


def names_in(text, english):
    if english:
        return {name_key(w) for w in NAME.findall(text)}
    return {name_key(w) for w in WORD.findall(text)}


def measure(keys, elen, clen, etext=None, ctext=None):
    """How well the aligned chapters agree, on the diagonal and one off
    (English chapter i against counterpart i-1 and i+1). keys: the matched
    keys in English document order.

    - length: Pearson r of log chapter lengths;
    - names: the share of the English chapter's capitalized words (5+
      letters: names, mostly) whose first five letters, spelled alike
      (name_key), occur in the counterpart chapter. Abridged translations
      (NPNF gives some letters only in part) defeat the length test; the
      names still find their chapter."""
    import math
    e = [math.log(1 + elen[k]) for k in keys]
    c = [math.log(1 + clen[k]) for k in keys]
    ratio = sorted(elen[k] / clen[k] for k in keys if clen[k])
    m = {"pairs": len(keys), "r_log_length": pearson(e, c),
         "r_offset_minus1": pearson(e[1:], c[:-1]),
         "r_offset_plus1": pearson(e[:-1], c[1:]),
         "median_length_ratio": round(ratio[len(ratio) // 2], 2) if ratio else None}
    if etext is not None:
        en = [names_in(etext[k], True) for k in keys]
        cn = [names_in(ctext[k], False) for k in keys]

        def share(pairs):
            got = [len(a & b) / len(a) for a, b in pairs if a]
            return round(sum(got) / len(got), 3) if got else None
        m["names_diagonal"] = share(zip(en, cn))
        m["names_offset_minus1"] = share(zip(en[1:], cn[:-1]))
        m["names_offset_plus1"] = share(zip(en[:-1], cn[1:]))
    return m


def verdict(m):
    """'aligned', 'unmeasured' (fewer than 5 pairs: too few to measure) or
    'refused'. Aligned if either test puts the diagonal clearly best: length
    r >= 0.7 and above both offsets, or the names share >= 0.2 and at least
    1.5 times both offsets, or every unit on both sides is paired
    (`one_to_one`) and the length r on the diagonal beats both offsets."""
    if m["pairs"] < 5 or m["r_log_length"] is None:
        return "unmeasured"
    off = [r for r in (m["r_offset_minus1"], m["r_offset_plus1"]) if r is not None]
    if m["r_log_length"] >= 0.7 and all(m["r_log_length"] > r for r in off):
        return "aligned"
    if m.get("one_to_one") and m["r_log_length"] > 0 and all(m["r_log_length"] > r for r in off):
        return "aligned"
    d = m.get("names_diagonal")
    noff = [x for x in (m.get("names_offset_minus1"), m.get("names_offset_plus1")) if x is not None]
    if d is not None and d >= 0.2 and all(d >= 1.5 * x for x in noff):
        return "aligned"
    return "refused"


def compact(keys, limit=150):
    """A list of unit keys, or past `limit` a count per top-level key (Origen's
    Commentary on John: the 26 books ANF does not translate, by book)."""
    if len(keys) <= limit:
        return keys
    by = {}
    for k in keys:
        by[k.split(".")[0]] = by.get(k.split(".")[0], 0) + 1
    return {"count": len(keys), "by_top_level": by}


def build_work(w, vol_book, cp_book):
    """One English work book cut from its volume, aligned to `cp_book` (or None)."""
    slug, vol, work_div, cp_slug, levels = w["slug"], w["vol"], w["div"], w.get("counterpart"), w["levels"]
    divs = vol_book["divs"]
    if work_div not in divs:
        raise SystemExit(f"HARD STOP: {slug}: {vol} has no division {work_div}")
    by_id = {u["id"]: u for u in vol_book["units"]}
    chapters, outside, spans = work_chapters(divs, vol_book["units"], work_div, levels)
    if not chapters:
        raise SystemExit(f"HARD STOP: {slug}: no numbered chapters under {vol} {work_div}")
    cp_units = {}
    if cp_book is not None:
        for u in cp_book["units"]:
            cp_units.setdefault(u["id"].split(":", 1)[1], u)
    series, n = VOLUMES[vol]
    units, elen, clen, matched, cp_hit = [], {}, {}, [], set()
    etext, ctext = {}, {}
    for key, pids in chapters.items():
        text = "\n\n".join(by_id[p]["text"] for p in pids)
        first, last = by_id[pids[0]], by_id[pids[-1]]
        u = {"id": f"{slug}:{key}", "ref": f"{w['abbrev']} {key}", "text": text, "links": [],
             "paragraphs": pids, "page": first["page"]}
        end = last.get("page_end") or last["page"]
        if end != first["page"]:
            u["page_end"] = end
        keys = [key] + spans.get(key, [])
        if spans.get(key):
            u["spans"] = keys
        hits = [k for k in cp_units if any(k == x or k.startswith(x + ".") for x in keys)]
        for k in hits:
            u["links"].append({"target": f"{cp_slug}:{k}", "type": "original", "resolved": True})
            cp_hit.add(k)
        if hits:
            elen[key] = len(text)
            clen[key] = sum(len(cp_units[k]["text"]) for k in hits)
            etext[key] = text
            ctext[key] = " ".join(cp_units[k]["text"] for k in hits)
            matched.append(key)
        units.append(u)
    book = {
        "slug": slug, "title": w["title"], "author": w["author"],
        "source": {"path": vol_book["source"]["path"], "format": "thml-ccel",
                   "url": vol_book["source"]["url"], "sha256": vol_book["source"]["sha256"],
                   "series": series, "volume": n, "division": work_div,
                   "division_title": divs[work_div]["title"], "derived_from": vol_book["slug"]},
        "scheme": {
            "citation": f"{w['abbrev']} {w['level_names']}",
            "resolution": w["level_names"].split(".")[-1],
            "honesty": ("one unit per numbered division of Schaff's English, keyed by its print "
                        "numbers; the text is the volume book's paragraphs (`paragraphs`), and the "
                        "footnotes and scripture links stay on those. " + w.get("honesty", "")).strip(),
        },
        "rights": vol_book["rights"],
        "units": units,
    }
    if w.get("note"):
        book["scheme"]["note"] = w["note"]
    if outside:
        book["scheme"]["outside"] = (f"{len(outside)} paragraphs under {vol} {work_div} sit in no "
                                     f"numbered division (introductions, notes, summaries); they are "
                                     f"in the volume book only")
    if cp_book is None:
        book["alignment"] = {"counterpart": None, "units": len(units), "matched": 0,
                             "note": w.get("no_counterpart", "")}
        return book
    m = measure(matched, elen, clen, etext, ctext)
    m["one_to_one"] = len(matched) == len(units) and len(cp_hit) == len(cp_units)
    v = verdict(m)
    if v == "unmeasured" and not (len(matched) == len(units) and len(cp_hit) == len(cp_units)):
        # too few chapters to measure, and the two do not even agree in count
        v = "refused"
    if v == "refused":   # measured and failed: no link is kept
        for u in units:
            u["links"] = []
        matched, cp_hit = [], set()
    book["alignment"] = {
        "counterpart": cp_slug, "verdict": v, "level": w["level_names"],
        "units": len(units), "matched": len(matched),
        "unmatched": [u["id"].split(":", 1)[1] for u in units if not u["links"]],
        "counterpart_units": len(cp_units), "counterpart_matched": len(cp_hit),
        "counterpart_unmatched": compact([k for k in cp_units if k not in cp_hit]),
        "measure": m,
    }
    return book


# ---------------------------------------------------------------- the table

# (vol, CCEL division, levels, counterpart, level names). levels: how many
# numbered divisions make the key (1 = chapter, 2 = book.chapter), "inline"
# when the numbers open paragraphs, "<n>+inline" for both. Every row was
# tried at its finest level first; where that was refused by the measure
# and a coarser level passes, the coarser level is the row, and the finer
# result is recorded in FINER_REFUSED (the evidence, re-run by --report).
ALIGNED = [
    ("anf01", "viii.ii", 1, "justin-apology-1-grc", "chapter"),
    ("anf01", "viii.iii", 1, "justin-apology-2-grc", "chapter"),
    ("anf01", "viii.iv", 1, "justin-dialogue-trypho-grc", "chapter"),
    ("anf02", "iii.ii", 1, "tatian-oratio-grc", "chapter"),
    ("anf02", "iv.ii", 2, "theophilus-ad-autolycum-grc", "book.chapter"),
    ("anf02", "v.ii", 1, "athenagoras-legatio-grc", "chapter"),
    ("anf02", "v.iii", 1, "athenagoras-de-resurrectione-grc", "chapter"),
    ("anf02", "vi.ii", 1, "clement-protrepticus-grc", "chapter"),
    ("anf02", "vi.iii", 2, "clement-paedagogus-grc", "book.chapter"),
    ("anf02", "vi.v", "inline", "clement-quis-dives-grc", "chapter"),
    ("anf03", "iv.iv", 1, "tertullian-de-idololatria-lat", "chapter"),
    ("anf03", "iv.v", 1, "tertullian-de-spectaculis-lat", "chapter"),
    ("anf03", "iv.viii", 2, "tertullian-ad-nationes-lat", "book.chapter"),
    ("anf03", "iv.x", 1, "tertullian-de-testimonio-animae-lat", "chapter"),
    ("anf03", "iv.xi", 1, "tertullian-de-anima-lat", "chapter"),
    ("anf03", "v.iv", 2, "tertullian-adversus-marcionem-lat", "book.chapter"),
    ("anf03", "v.v", 1, "tertullian-adversus-hermogenem-lat", "chapter"),
    ("anf03", "v.vi", 1, "tertullian-adversus-valentinianos-lat", "chapter"),
    ("anf03", "v.viii", 1, "tertullian-de-resurrectione-carnis-lat", "chapter"),
    ("anf03", "v.ix", 1, "tertullian-adversus-praxean-lat", "chapter"),
    ("anf03", "v.x", 1, "tertullian-scorpiace-lat", "chapter"),
    ("anf03", "v.xi", 1, "pseudo-tertullian-adversus-omnes-haereses-lat", "chapter"),
    ("anf03", "vi.iii", 1, "tertullian-de-baptismo-lat", "chapter"),
    ("anf03", "vi.iv", 1, "tertullian-de-oratione-lat", "chapter"),
    ("anf03", "vi.vi", 1, "passio-perpetuae-grc", "chapter"),
    ("anf03", "vi.vii", 1, "tertullian-de-patientia-lat", "chapter"),
    ("anf04", "iii.viii", 1, "tertullian-de-pudicitia-lat", "chapter"),
    ("anf04", "iii.ix", 1, "tertullian-de-ieiunio-lat", "chapter"),
    ("anf04", "iv.iii", 1, "minucius-felix-octavius-lat", "chapter"),
    ("anf04", "vi.ix", 2, "origen-contra-celsum-grc", "book.chapter"),
    ("anf05", "iii.iii", 1, "hippolytus-refutatio-grc", "book"),
    ("anf06", "xi.iii", 2, "methodius-symposium-grc", "discourse.chapter"),
    ("anf06", "xii.iii", 2, "arnobius-adversus-nationes-lat", "book.chapter"),
    ("anf07", "iii.ii", 2, "lactantius-divinae-institutiones-lat", "book.chapter"),
    ("anf07", "iii.ii.viii", 1, "lactantius-epitome-lat", "chapter"),
    ("anf07", "iii.iii", 1, "lactantius-de-ira-dei-lat", "chapter"),
    ("anf07", "iii.iv", 1, "lactantius-de-opificio-dei-lat", "chapter"),
    ("anf07", "iii.v", 1, "lactantius-de-mortibus-persecutorum-lat", "chapter"),
    ("anf08", "iv.iii", "inline", "clement-excerpta-theodoto-grc", "excerpt"),
    ("anf09", "ix.iii.i", "inline", "testament-of-abraham-a-grc", "chapter"),
    ("anf09", "ix.iii.ii", "inline", "testament-of-abraham-b-grc", "chapter"),
    ("anf09", "xv.iii", 1, "origen-commentary-john-grc", "book"),
    ("npnf101", "vi", 1, "augustine-confessiones-lat", "book"),
    ("npnf101", "vii.1", 1, "augustine-epistulae-lat", "letter"),
    ("npnf102", "iv", 2, "augustine-de-civitate-dei-lat", "book.chapter"),
    ("npnf103", "iv.iv", 1, "augustine-de-fide-et-symbolo-lat", "chapter"),
    ("npnf103", "iv.vi", 1, "augustine-de-utilitate-credendi-lat", "chapter"),
    ("npnf103", "v.ii", 1, "augustine-de-bono-coniugali-lat", "chapter"),
    ("npnf103", "v.iii", 1, "augustine-de-sancta-virginitate-lat", "chapter"),
    ("npnf103", "v.v", 1, "augustine-de-mendacio-lat", "chapter"),
    ("npnf103", "v.vi", 1, "augustine-contra-mendacium-lat", "chapter"),
    ("npnf103", "v.vii", 1, "augustine-de-opere-monachorum-lat", "chapter"),
    ("npnf104", "iv.vi", 1, "augustine-de-duabus-animabus-lat", "chapter"),
    ("npnf104", "iv.ix", 1, "augustine-contra-faustum-lat", "book"),
    ("npnf104", "iv.x", 1, "augustine-de-natura-boni-lat", "chapter"),
    ("npnf104", "v.v", 1, "augustine-contra-litteras-petiliani-lat", "book"),
    ("npnf105", "x", 2, "augustine-de-peccatorum-meritis-lat", "book.chapter"),
    ("npnf105", "xi", 1, "augustine-de-spiritu-et-littera-lat", "chapter"),
    ("npnf105", "xii", 1, "augustine-de-natura-et-gratia-lat", "chapter"),
    ("npnf105", "xiv", 1, "augustine-de-gestis-pelagii-lat", "chapter"),
    ("npnf105", "xv.iii", 1, "augustine-de-gratia-christi-lat", "chapter"),
    ("npnf105", "xvii", 2, "augustine-de-natura-et-origine-animae-lat", "book.chapter"),
    ("npnf105", "xviii", 2, "augustine-contra-duas-epistulas-pelagianorum-lat", "book.chapter"),
    ("npnf106", "vi", 1, "augustine-de-consensu-evangelistarum-lat", "book"),
    ("npnf201", "iii", 2, "eusebius-historia-ecclesiastica-grc", "book.chapter"),
    ("npnf201", "iii.xiv", 1, "eusebius-martyrs-palestine-grc", "chapter"),
    ("npnf201", "iv.vi", 2, "eusebius-vita-constantini-grc", "book.chapter"),
    ("npnf201", "iv.vii", 1, "eusebius-oratio-ad-coetum-grc", "chapter"),
    ("npnf201", "iv.viii", 1, "eusebius-laudes-constantini-grc", "chapter"),
    ("npnf202", "ii", 2, "socrates-historia-ecclesiastica-grc", "book.chapter"),
    ("npnf202", "iii", 2, "sozomen-historia-ecclesiastica-grc", "book.chapter"),
    ("npnf203", "iv.viii", 1, "theodoret-historia-ecclesiastica-grc", "book"),
    ("npnf204", "vii.ii", 1, "athanasius-de-incarnatione-grc", "chapter"),
    ("npnf204", "xiv.ii", 1, "athanasius-de-decretis-grc", "chapter"),
    ("npnf204", "xxi.ii.i", "inline", "athanasius-contra-arianos-1-grc", "section"),
    ("npnf204", "xxi.ii.iii", "inline", "athanasius-contra-arianos-2-grc", "section"),
    ("npnf204", "xxi.ii.iv", "inline", "athanasius-contra-arianos-3-grc", "section"),
    ("npnf204", "xxi.ii.vi", "inline", "athanasius-contra-arianos-4-grc", "section"),
    ("npnf206", "v", 1, "jerome-epistulae-lat", "letter"),
    ("npnf207", "iii.xiii", "inline", "gregory-nazianzen-oration-27-grc", "chapter"),
    ("npnf207", "iii.xiv", "inline", "gregory-nazianzen-oration-28-grc", "chapter"),
    ("npnf207", "iii.xv", "inline", "gregory-nazianzen-oration-29-grc", "chapter"),
    ("npnf207", "iii.xvi", "inline", "gregory-nazianzen-oration-30-grc", "chapter"),
    ("npnf207", "iii.xvii", "inline", "gregory-nazianzen-oration-31-grc", "chapter"),
    ("npnf211", "ii.ii", 1, "sulpicius-vita-martini-lat", "chapter"),
    ("npnf211", "ii.iii", 1, "sulpicius-epistulae-lat", "letter"),
    ("npnf211", "ii.iv", 2, "sulpicius-dialogi-lat", "dialogue.chapter"),
    ("npnf211", "ii.vi", 2, "sulpicius-chronica-lat", "book.chapter"),
]

# The finer level, tried first and refused by the measure (verdict "refused"
# when built at that level); kept so --report re-runs the evidence.
FINER_REFUSED = {
    "hippolytus-refutatio-grc": (2, "book.chapter: ANF's chapters are not Wendland's"),
    "origen-commentary-john-grc": (2, "book.chapter: ANF's chapters are not Preuschen's sections"),
    "augustine-confessiones-lat": (2, "book.chapter: CSEL (Knöll) numbers the Confessions by "
                                      "sections, not the chapters NPNF prints"),
    "augustine-contra-faustum-lat": (2, "book.chapter: NPNF prints no chapter divisions"),
    "theodoret-historia-ecclesiastica-grc": (2, "book.chapter: NPNF's chapter numbers are not "
                                                "Parmentier's"),
    "augustine-contra-litteras-petiliani-lat": (2, "book.chapter: NPNF's chapters are not CSEL's "
                                                   "sections"),
    "augustine-de-consensu-evangelistarum-lat": (2, "book.chapter: NPNF's chapters are not CSEL's "
                                                    "sections"),
}

# Cyprian (ANF 5). No Latin: CSEL 3 (Hartel, 1868-71) is not in csel-dev or
# any other GitHub source found, so these books carry no counterpart.
CYPRIAN_NOTE = ("No Latin counterpart: Cyprian's Latin (CSEL 3, Hartel 1868-71) is not on "
                "GitHub in a TEI edition: no stoa0104 (Cyprian) in OpenGreekAndLatin/csel-dev "
                "or PerseusDL/canonical-latinLit (checked 2026-10-03), so this English stands "
                "alone; the keys are ANF's own numbers (the Oxford numbering of the letters), "
                "not Hartel's.")
CYPRIAN = [
    ("cyprian-epistles-schaff", "anf05", "iv.iv", 1, "letter", "Cypr. Ep.",
     "The Epistles of Cyprian"),
    ("cyprian-treatises-schaff", "anf05", "iv.v", "1+inline", "treatise.chapter", "Cypr. Tr.",
     "The Treatises of Cyprian"),
    ("cyprian-seventh-council-schaff", "anf05", "iv.vi.i", "speakers", "sententia", "Sent. episc.",
     "The Seventh Council of Carthage under Cyprian"),
    ("cyprian-dubia-schaff", "anf05", "iv.vii", "1+inline", "treatise.chapter", "Ps.-Cypr.",
     "Treatises Attributed to Cyprian on Questionable Authority"),
    ("cyprian-vita-pontius-schaff", "anf05", "iv.iii", "inline", "chapter", "Pont. Vit. Cypr.",
     "The Life and Passion of Cyprian, by Pontius the Deacon"),
]


def work_rows(manifest):
    """Every work book as a dict build_work reads."""
    rows = []
    for vol, div, levels, cp, names in ALIGNED:
        e = manifest.get(cp)
        if e is None:
            raise SystemExit(f"HARD STOP: counterpart {cp} is not in the manifest")
        series, n = VOLUMES[vol]
        rows.append({"slug": re.sub(r"-(grc|lat)$", "", cp) + "-schaff", "vol": vol, "div": div,
                     "levels": levels, "counterpart": cp, "level_names": names,
                     "abbrev": ST.TEI_PROSE.get(cp, cp),
                     "title": f"{e['title']} (English, {series} {n})",
                     "author": f"{e['author']}; English in {series} {n}, ed. Schaff"})
    for slug, vol, div, levels, names, abbrev, title in CYPRIAN:
        rows.append({"slug": slug, "vol": vol, "div": div, "levels": levels, "counterpart": None,
                     "level_names": names, "abbrev": abbrev, "title": title + " (English, ANF 5)",
                     "author": "Cyprian of Carthage" + (" (attributed)" if "dubia" in slug else "")
                               + "; English in ANF 5, ed. Schaff",
                     "no_counterpart": CYPRIAN_NOTE})
    return rows


# ---------------------------------------------------------------- counterparts

OGL_DIRS = ("first1k", "csel")


def counterpart(slug, manifest):
    """The PR #7 book: data/books/<slug>.json if built from the committed
    source, else converted in memory from data/corpus/{first1k,csel}/ by
    structure_texts.convert_tei_prose (the converter that built it). None if
    its source is not fetched (python3 pipeline/fetch_sources.py)."""
    want = manifest[slug]["sha256"]
    p = os.path.join(BOOKS, slug + ".json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            book = json.load(f)
        if book["source"]["sha256"] == want:
            return book
    for d in OGL_DIRS:
        src = os.path.join(ROOT, "data", "corpus", d, slug + ".xml")
        if os.path.exists(src):
            if sha256_file(src) != want:
                raise SystemExit(f"HARD STOP: {src} is not the source the manifest pins")
            return ST.convert_tei_prose(src, slug, ST.TEI_PROSE[slug])
    return None


# ---------------------------------------------------------------- build

def volume_stats(book):
    u = book["units"]
    pages = [x["page"] for x in u if x.get("page")]
    return {"paragraphs": len(u), "chars": sum(len(x["text"]) for x in u),
            "notes": sum(len(x.get("notes", [])) for x in u),
            "scripture_links": sum(len(x["links"]) for x in u)
                               + sum(len(n["links"]) for x in u for n in x.get("notes", [])),
            "divisions": len(book["divs"]),
            "first_page": pages[0] if pages else None, "last_page": pages[-1] if pages else None}


def entry(book, blob):
    e = {"title": book["title"], "author": book["author"], "format": book["source"]["format"],
         "sha256": book["source"]["sha256"], "units": len(book["units"]),
         "scheme": book["scheme"], "rights": book["rights"]}
    if "skipped" in book:
        e["stats"] = volume_stats(book)
        e["skipped"] = book["skipped"]
        e["source"] = {k: book["source"][k] for k in ("url", "series", "volume", "ccel_status",
                                                      "printed")}
    else:
        e["source"] = {k: book["source"][k] for k in ("url", "derived_from", "division",
                                                      "division_title")}
        e["alignment"] = book["alignment"]
    e["built_sha256"] = hashlib.sha256(blob).hexdigest()
    return e


def build(only=None):
    """{slug: (book, blob, entry)} for every volume and work book (or those of `only` volumes)."""
    verify_pins()
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    rows = work_rows(manifest)
    out, missing = {}, []
    for vol in VOLUMES:
        if only and vol not in only:
            continue
        vb = convert_volume(vol)
        blob = json.dumps(vb, ensure_ascii=False).encode("utf-8")
        out[vb["slug"]] = (vb, blob, entry(vb, blob))
        for w in (r for r in rows if r["vol"] == vol):
            cp = counterpart(w["counterpart"], manifest) if w["counterpart"] else None
            if w["counterpart"] and cp is None:
                missing.append(w["counterpart"])
                continue
            wb = build_work(w, vb, cp)
            wblob = json.dumps(wb, ensure_ascii=False).encode("utf-8")
            out[w["slug"]] = (wb, wblob, entry(wb, wblob))
    return out, missing


def report(built):
    tot = {"paragraphs": 0, "chars": 0, "notes": 0, "scripture_links": 0}
    for slug, (b, _, e) in built.items():
        if "stats" in e:
            s = e["stats"]
            for k in tot:
                tot[k] += s[k]
            print(f"  {slug:<16}{s['paragraphs']:>6} paras {s['chars']:>10,} chars {s['notes']:>6} notes "
                  f"{s['scripture_links']:>6} scripture  pp. {s['first_page']}-{s['last_page']}")
    print(f"  volumes: {tot['paragraphs']:,} paragraphs, {tot['chars']:,} chars, {tot['notes']:,} notes, "
          f"{tot['scripture_links']:,} scripture links")
    verdicts = {}
    for slug, (b, _, e) in built.items():
        a = e.get("alignment")
        if not a:
            continue
        v = a.get("verdict", "no counterpart")
        verdicts.setdefault(v, []).append(slug)
        m = a.get("measure") or {}
        print(f"  {slug:<48}{v:<14}{a['units']:>5} units {a['matched']:>5} matched "
              f"{a.get('counterpart_matched', 0):>5}/{a.get('counterpart_units', 0):<5} cp "
              f"r={m.get('r_log_length')} names={m.get('names_diagonal')}")
    for v, s in verdicts.items():
        print(f"  {v}: {len(s)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--vol", action="append", help="build only these volumes (repeatable)")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    built, missing = build(a.vol)
    report(built)
    if missing:
        print(f"  NOT BUILT (counterpart source not fetched; run fetch_sources.py): {missing}")
    if a.report:
        return
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    if a.check:
        bad = [s for s, (_, blob, e) in built.items() if manifest.get(s) != e]
        if bad:
            raise SystemExit(f"CHECK FAILED: rebuilt books differ from the manifest: {bad}")
        print(f"  CHECK PASSED: {len(built)} books = their committed manifest entries.")
        return
    os.makedirs(BOOKS, exist_ok=True)
    for slug, (_, blob, e) in built.items():
        write_atomic(os.path.join(BOOKS, slug + ".json"), blob)
        manifest[slug] = e
    write_atomic(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    print(f"  wrote {len(built)} books + {len(manifest)}-entry manifest")


if __name__ == "__main__":
    main()
