#!/usr/bin/env python3
"""
build_commentaries.py -- six public-domain commentaries and lectures, shelved
as drafts, keyed where they can be by the verse they comment on.

    python3 pipeline/build_commentaries.py --fetch    # pinned sources -> data/corpus/commentaries/ (gitignored, ~170 MB)
    python3 pipeline/build_commentaries.py            # build data/books/<slug>.json + manifest entries
    python3 pipeline/build_commentaries.py --check    # rebuild in memory: = the committed manifest entries
    python3 pipeline/build_commentaries.py --report   # per-book measures, writes nothing
    python3 tests/commentaries_test.py

THE BOOKS, AND WHICH PRINTING (every one printed before 1929: US public domain)

  lightfoot-galatians     J. B. Lightfoot, St Paul's Epistle to the Galatians,
                          10th ed. (1890), the Macmillan reprint of 1910.
                          Internet Archive saintpaulsepistl00lighrich (UC copy).
  lightfoot-philippians   J. B. Lightfoot, St Paul's Epistle to the Philippians,
                          3rd ed. (Macmillan, 1873). stpaulsepistleto00lighuoft (Toronto copy).
  lightfoot-colossians    J. B. Lightfoot, St Paul's Epistles to the Colossians
                          and to Philemon (Macmillan, 1875, the first edition):
                          Project Gutenberg #50857, a proofread transcription.
  westcott-hebrews        B. F. Westcott, The Epistle to the Hebrews, 2nd ed.
                          (Macmillan, 1892). epistletohebrew00westgoog (Harvard copy).
  westcott-john           B. F. Westcott, The Epistles of St John, 3rd ed.
                          (Macmillan, 1892). cu31924074296629 (Cornell copy).
  hort-ante-nicene        F. J. A. Hort, Six Lectures on the Ante-Nicene Fathers
                          (Macmillan, 1895). sixlecturesonant00hortrich (UC copy): by page,
                          each page carrying its lecture (`lecture`).

Project Gutenberg has only the Colossians (searched 2026-10-03 by author and
title); its Greek is real Unicode and its markup gives the verse anchors of
Lightfoot's Greek text and every note paragraph, so that book is exact. The
other five are read from the Internet Archive's OCR (hOCR, word boxes),
chosen by measuring every candidate scan's text layer (the comment above
CANDIDATES lists the numbers): the other Toronto scans of Lightfoot (and the 1879
Colossians) have NO Greek codepoints at all, every Greek word turned into
Latin letters, as Thayer's and Abbott-Smith's scans were; the John scan from
Toronto was OCR'd as Greek throughout, its English unreadable. The scans
chosen keep the notes' Greek as Greek.

THE CITATION SPINE. A commentary is cited by the verse it comments on. On a
commentary page the epistle's text stands at the top in large type and the
notes run below in two columns; a note on a new verse opens an indented
paragraph with the verse number ("6. οὕτως ταχέως] ..."), a paraphrase of a
run of verses with the run ("6—9. ..."), and every other note opens with its
lemma alone. So each indented number is a candidate verse opener, and it is
accepted only if the sequence allows it: the same chapter at or after the
current verse (within the KJV's verse count and a bounded gap), or the next
chapter's first verses where the page's running head (OCR, read fuzzily) or
the end of the chapter says so. An accepted opener starts (or continues) the
unit `<slug>:<chapter>.<verse>` (`lightfoot-galatians:2.20`; a run is
`1.6-9`; in a volume of several epistles the book leads: `westcott-john:
2John.1.6`, `lightfoot-colossians:Phlm.1.4-7`), and every line after it,
in reading order (left column, then right), belongs to it until the next
accepted opener. A rejected candidate stays in the text where it stands and
is counted. Each note unit links to the KJV verse(s) it comments on
(`type: comments-on`). Notes before the first opener are the unit `title`.

What a commentary page holds besides the notes is kept, never dropped: the
epistle's text block (and, in Westcott, the critical apparatus printed under
it) is the unit `leaf.N.text`; a single-column passage that begins on a
commentary page after the notes (a detached note) is the page unit `leaf.N`.
Every page that is not laid out in note columns (introductions, detached
notes, Westcott's additional notes, dissertations, essays, index) is a page
unit, `leaf.N` (the scan leaf, as the Charles books), the printed folio in
`scan.printed_page` where the running head gives it (or its neighbours do:
`scan.printed_page_from`). Lines the OCR made of accents alone (the
diacritics of the large Greek type, read as a line of their own) are
dropped and counted.

The Colossians from Gutenberg: notes by the same rule, but read off the
transcription's paragraphs and its verse anchors (no OCR, no guessing of
chapters: a note's verse number is matched to the latest Greek verse anchor
with that number). Lightfoot's Greek text is kept per verse
(`text.Col.1.3`), the introduction, dissertations and index by printed page
(`p.17`, the transcription marks every page break), footnotes on the unit
whose text carries their reference mark (`notes`), marginal summaries in
`sidenotes`.

SCRIPTURE. Every unit's English references ("Rom. ix. 16", "1 Cor. i. 1")
are read by fathers_scripture.parse (the same reader as the fathers' English
editors) and resolved in the KJV's own numbering, which these English
editors use; a reference to a verse the KJV lacks, to a whole chapter, or to
a book outside the KJV stays `resolved: false` with its reason. "ver. 8"
and "vv. 8, 9" in a note mean the verse of the same chapter, and Westcott's
"c. x. 11" the same epistle (`rule: self/...`).

HONESTY. The five scanned books are unproofread OCR and every honesty field
says so; their notes' boundaries rest on verse numbers read off the page and
checked only against the sequence. Nothing is minted: ids are citations.

THE SECOND SHELF (Alford, Bengel, Keil & Delitzsch: one book per volume) is
the table SECOND and its own reader, build_book_2b: see the comment above
SECOND for the scans measured and chosen, and harvest_2b for how Keil &
Delitzsch's Old Testament numbering is measured and mapped.
"""
import argparse
import collections
import hashlib
import html
import json
import os
import re
import statistics as st
import sys
import unicodedata
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import charles_ocr as C  # noqa: E402
import fathers_scripture as FS  # noqa: E402

BOOKS_DIR = os.path.join(ROOT, "data", "books")
MANIFEST = os.path.join(BOOKS_DIR, "manifest.json")
CACHE = os.path.join(ROOT, "data", "corpus", "commentaries")
UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")
STRONGS = os.path.join(ROOT, "data", "strongs", "strongs.jsonl")
NT_JOHN = os.path.join(ROOT, "data", "nt", "John", "passages.jsonl")

# The candidate scans, measured 2026-10-03 on each item's _djvu.txt: Greek
# letters as a share of all letters; Greek tokens (3+ letters) found among
# Strong's Greek lemmas, the forms of data/nt/John and the Greek of PG
# #50857; English tokens found in the dwyl word list (data/corpus/proof).
#   Galatians   saintpaulsepistl00lighrich 1910  6.8%  65.9%  92.6%   <- chosen (IA: NOT_IN_COPYRIGHT)
#               cu31924075537088 (a 1921 reprint) 6.8% 66.5% 92.7%
#               saintpaulepistle00lighuoft 1914, saintpaulsepistl00lighuoft 1890,
#               sa590770400lighuoft 1880, stpaulsepistleto00ligh 1870: 0.0% Greek
#   Philippians stpaulsepistleto00lighuoft 1873  7.3%  65.6%  92.4%   <- chosen
#               saintpaulsepistl00ligh 1878      7.3%  65.1%  92.1%
#               epistlephilippia00lighuoft 1903, a590773100lighuoft 1898: 0.0% Greek
#   Colossians  PG #50857 (1875)                11.5%  (transcribed)   93.3%   <- chosen
#               saintpaulsepistl00unknuoft 1879: 0.0% Greek, English 82.6%
#   Hebrews     epistletohebrew00westgoog 1892 13.6%  64.2%  88.9%   <- chosen
#               epistletohebrews0000broo_a4f0 1889: 0.0% Greek
#   John        cu31924074296629 1892           9.2%  74.0%  92.2%   <- chosen
#               epistlesstjohn00dclgoog 1892     9.2%  73.7%  92.2%
#               epistlesstjohng00westgoog 1886   9.0%  69.0%  91.7%
#               epistlesofstjohn00westuoft 1886, TheEpistlesOfStJohnTheGreekText:
#               ~100% Greek letters (the English OCR'd as Greek)
#   Hort        sixlecturesonant00hortrich 1895  (no Greek)  96.3%   <- chosen
#               sixlecturesonan00hortgoog 95.3%, sixlecturesonant00hortuoft 94.9%
CANDIDATES = None

GUTENBERG = {
    "lightfoot-colossians": {
        "pg": 50857,
        "url": "https://www.gutenberg.org/cache/epub/50857/pg50857-images.html",
        "file": "pg50857-images.html",
        "sha256": "5d62c4f3b025f31c71d724c26b143cebec11636983e9be797d9fcab090b688d3",
        "title": "St Paul's Epistles to the Colossians and to Philemon",
        "short": "Lightfoot, Col.",
        "author": "J. B. Lightfoot",
        "edition": ("J. B. Lightfoot, Saint Paul's Epistles to the Colossians and to Philemon: a revised "
                    "text with introductions, notes, and dissertations (London: Macmillan, 1875), the first "
                    "edition (title page as transcribed)"),
        "printed": 1875,
        "regions": {"ΠΡΟΣ ΚΟΛΑΣΣΑΕΙΣ": "Col", "ΠΡΟΣ ΦΙΛΗΜΟΝΑ": "Phlm"},
        "anchor": {"Col": re.compile(r'^(I|II|III|IV)_(\d+)$'), "Phlm": re.compile(r'^(ph)_(\d+)$')},
    },
}

SCANS = {
    "lightfoot-galatians": {
        "ia": "saintpaulsepistl00lighrich",
        "sha256": "fc65644766c7e56822907235645bcecfc878521f804f4c7870320057e05f282c",
        "title": "St Paul's Epistle to the Galatians",
        "short": "Lightfoot, Gal.",
        "author": "J. B. Lightfoot",
        "edition": ("J. B. Lightfoot, Saint Paul's Epistle to the Galatians: a revised text with introduction, "
                    "notes, and dissertations, 10th ed. (1890); this copy the reprint of 1910 (London: "
                    "Macmillan, 1910), as its title page and imprint read"),
        "printed": 1910,
        "copy": "University of California Libraries",
        "ia_rights": "NOT_IN_COPYRIGHT",
        "leaves": (8, 403),
        "epistles": [("Gal", 90, 244)],
        "apparatus": False,
    },
    "lightfoot-philippians": {
        "ia": "stpaulsepistleto00lighuoft",
        "sha256": "c7829cd1fd0666dbc339c4702c3e1b34165b573b83c4cf41b38a6407f5539d66",
        "title": "St Paul's Epistle to the Philippians",
        "short": "Lightfoot, Phil.",
        "author": "J. B. Lightfoot",
        "edition": ("J. B. Lightfoot, Saint Paul's Epistle to the Philippians: a revised text with "
                    "introduction, notes, and dissertations, 3rd ed. (London and Cambridge: Macmillan, 1873), "
                    "as its title page reads"),
        "printed": 1873,
        "copy": "University of Toronto (Robarts)",
        "ia_rights": "NOT_IN_COPYRIGHT",
        "leaves": (9, 362),
        "epistles": [("Phil", 95, 181)],
        "apparatus": False,
    },
    "westcott-hebrews": {
        "ia": "epistletohebrew00westgoog",
        "sha256": "2785db294c9077843e33c9305b30a8467fff12583f9c903675e8dcc22e0b33d3",
        "title": "The Epistle to the Hebrews",
        "short": "Westcott, Heb.",
        "author": "B. F. Westcott",
        "edition": ("B. F. Westcott, The Epistle to the Hebrews: the Greek text with notes and essays, 2nd ed. "
                    "(London and New York: Macmillan, 1892), as its title page reads (first ed. 1889)"),
        "printed": 1892,
        "copy": "Harvard University (Google scan)",
        "ia_rights": "NOT_IN_COPYRIGHT",
        "leaves": (9, 594),
        "epistles": [("Heb", 94, 542)],
        "apparatus": True,
    },
    "westcott-john": {
        "ia": "cu31924074296629",
        "sha256": "06dfd59ea42ff4aa504f0cc6089848ec92cf70da4f0fa909e5a1b6e9e6833134",
        "title": "The Epistles of St John",
        "short": "Westcott, Epp. John",
        "author": "B. F. Westcott",
        "edition": ("B. F. Westcott, The Epistles of St John: the Greek text with notes and essays, 3rd ed. "
                    "(Cambridge and London: Macmillan, 1892), as its title page reads (first ed. 1883)"),
        "printed": 1892,
        "copy": "Cornell University Library",
        "ia_rights": None,
        "leaves": (9, 441),
        "epistles": [("1John", 64, 281), ("2John", 284, 293), ("3John", 296, 306)],
        "apparatus": True,
    },
    "hort-ante-nicene": {
        "ia": "sixlecturesonant00hortrich",
        "sha256": "acffe34d110c2a486981e1510b618a7dd9b282181724e346de710e7cd31dfb93",
        "title": "Six Lectures on the Ante-Nicene Fathers",
        "short": "Hort, Ante-Nicene Fathers",
        "author": "F. J. A. Hort",
        "edition": ("F. J. A. Hort, Six Lectures on the Ante-Nicene Fathers (London and New York: Macmillan, "
                    "1895), as its title page reads; delivered 1890, published after his death by his son"),
        "printed": 1895,
        "copy": "University of California Libraries",
        "ia_rights": "NOT_IN_COPYRIGHT",
        "leaves": None,           # measured: the leaves that carry text, title page to the printer's imprint
        "epistles": [],
        "apparatus": False,
    },
}
ORDER = ["lightfoot-galatians", "lightfoot-philippians", "lightfoot-colossians",
         "westcott-hebrews", "westcott-john", "hort-ante-nicene"]
MULTI = {"lightfoot-colossians", "westcott-john"}    # volumes of several epistles: ids lead with the book

# ------------------------------------------------------------------ files


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_atomic(path, data):
    with open(path + ".tmp", "wb") as f:
        f.write(data)
    os.replace(path + ".tmp", path)


def download(url, dest, sha):
    if os.path.exists(dest) and sha256_file(dest) == sha:
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "canon-corpus/commentaries"})
    with urllib.request.urlopen(req, timeout=600) as r, open(dest + ".tmp", "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    got = sha256_file(dest + ".tmp")
    if got != sha:
        os.remove(dest + ".tmp")
        raise SystemExit(f"{url}: sha256 {got} != pinned {sha}")
    os.replace(dest + ".tmp", dest)


def fetch():
    for slug, g in GUTENBERG.items():
        download(g["url"], os.path.join(CACHE, g["file"]), g["sha256"])
        print(f"  {slug}: PG #{g['pg']} present, sha256 pinned")
    for slug, s in SCANS.items():
        # the item's rights field, read live: a changed status stops the fetch
        meta = json.load(urllib.request.urlopen(f"https://archive.org/metadata/{s['ia']}", timeout=120))
        got = meta.get("metadata", {}).get("possible-copyright-status")
        if got != s["ia_rights"]:
            raise SystemExit(f"{s['ia']}: possible-copyright-status {got!r} != recorded {s['ia_rights']!r}")
        f = f"{s['ia']}_hocr.html"
        download(f"https://archive.org/download/{s['ia']}/{f}", os.path.join(CACHE, f), s["sha256"])
        print(f"  {slug}: {s['ia']} hOCR present, sha256 pinned; rights field {got!r}")

# ------------------------------------------------------------------ hOCR

LINE = re.compile(r'<span class="(?:ocr_line|ocr_caption|ocr_header|ocr_textfloat)"([^>]*)>')
WORD = re.compile(r'<span class="ocrx_word"([^>]*)>(.*?)</span>', re.S)
TITLE = re.compile(r'title="([^"]*)"')


def _title(attrs):
    m = TITLE.search(attrs)
    t = m.group(1) if m else ""
    bb = re.search(r'bbox (\d+) (\d+) (\d+) (\d+)', t)
    xs = re.search(r'x_size ([\d.]+)', t)
    cf = re.search(r'x_wconf (\d+)', t)
    return (tuple(map(int, bb.groups())) if bb else (0, 0, 0, 0),
            float(xs.group(1)) if xs else 0.0, int(cf.group(1)) if cf else 0)


def read_hocr(path):
    """charles_ocr.read_hocr's output, from either attribute order (the
    Hort file puts lang before title)."""
    with open(path, encoding="utf-8") as f:
        s = f.read()
    out = []
    for p in s.split('<div class="ocr_page"')[1:]:
        ms = list(LINE.finditer(p))
        lines = []
        for i, m in enumerate(ms):
            seg = p[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(p)]
            bbox, xs, _ = _title(m.group(1))
            words = []
            for w in WORD.finditer(seg):
                wb, _, conf = _title(w.group(1))
                t = html.unescape(re.sub('<[^>]+>', '', w.group(2))).strip()
                if t:
                    words.append(wb + (conf, t))
            if words:
                lines.append({"bbox": bbox, "xs": xs, "words": words, "text": " ".join(w[5] for w in words)})
        bb = re.search(r'bbox 0 0 (\d+) (\d+)', p)
        out.append({"w": int(bb.group(1)), "h": int(bb.group(2)), "lines": lines})
    return out


def pages(slug):
    s = SCANS[slug]
    src = os.path.join(CACHE, f"{s['ia']}_hocr.html")
    cache = os.path.join(CACHE, f"{s['ia']}.{s['sha256'][:12]}.pages.json.gz")
    if os.path.exists(cache):
        return C.load_pages(cache)
    if not os.path.exists(src) or sha256_file(src) != s["sha256"]:
        raise SystemExit(f"pinned hOCR missing or changed: {src}\n  run: python3 pipeline/build_commentaries.py --fetch")
    C.save_pages(read_hocr(src), cache)
    return C.load_pages(cache)

# ------------------------------------------------------------------ the page


def is_junk(l, med):
    """A line the OCR made of the large Greek type's accents and breathings
    alone ('U / 4 ‘ “-'), or nothing legible: small type, or short tokens."""
    t = l["text"]
    if not any(c.isalnum() for c in t):
        return True
    toks = [w[5] for w in l["words"]]
    longw = sum(1 for x in toks if sum(c.isalpha() for c in x) >= 3)
    if longw >= 4:
        return False
    if med and l["xs"] < 0.62 * med:
        return True
    lens = [sum(c.isalpha() for c in x) for x in toks]
    return len(toks) >= 3 and sum(lens) / len(toks) < 2.0


def headlike(l):
    t = l["text"].strip()
    if not t or len(l["words"]) > 9:
        return False
    if re.search(r'[\[\]\(\)\{\}]', t) and re.search(r'\d', t):
        return True
    if re.fullmatch(r'[^\w]*\d{1,3}[^\w]*', t):
        return True
    letters = [c for c in t if c.isalpha()]
    return bool(letters) and sum(c.isupper() for c in letters) >= 0.6 * len(letters)


REF_OPEN = re.compile(r'[\[\(\{]\s*([^\[\]\(\)\{\}]{1,18})$')
REF_CLOSE = re.compile(r'^\s*([^\[\]\(\)\{\}]{1,18}?)\s*[\]\)\}]')


def split_head(text):
    """(verse reference or None, rest) of a running-head line: 'EPISTLE TO THE
    GALATIANS. [I. 2, 3' -> ('I. 2, 3', 'EPISTLE TO THE GALATIANS.')."""
    m = REF_OPEN.search(text)
    if m and re.search(r'\d', m.group(1)):
        return m.group(1).strip(), text[:m.start()]
    m = REF_CLOSE.match(text)
    if m and re.search(r'\d', m.group(1)):
        return m.group(1).strip(), text[m.end():]
    return None, text


ROMANISH = str.maketrans({"Ι": "I", "ι": "I", "l": "I", "L": "I", "1": "I", "|": "I", "!": "I", "T": "I",
                          "t": "I", "i": "I", "Ί": "I", "Π": "II", "Η": "II", "H": "II", "Υ": "V", "v": "V",
                          "Χ": "X", "x": "X", "E": "I"})


def head_chapter(ref, nch):
    """The chapter of a running head's reference, read fuzzily ('IL. 4' is
    II, 'ΠῚ. 8' is III, '1. 6' is I), or None."""
    if not ref:
        return None
    r = "".join(c for c in unicodedata.normalize("NFD", ref) if not unicodedata.combining(c))
    m = re.match(r'\s*([^\W\d_]{1,5}|[|!]{1,4})\s*[.,:;]?\s*\d', r)
    if m:
        n = FS.roman(m.group(1).translate(ROMANISH))
        return n if n and 1 <= n <= nch else None
    m = re.match(r'\s*(\d)\s*\.\s*\d', r)
    if m and 1 <= int(m.group(1)) <= nch:
        return int(m.group(1))
    return None


def head_verses(ref):
    return [int(x) for x in re.findall(r'\d{1,2}', ref or "")]


def analyse(p):
    """Head, page number, verse reference, body lines and junk count of a leaf."""
    L = [l for l in p["lines"] if l["words"] and l["text"].strip()]
    many = [l["xs"] for l in L if len(l["words"]) >= 4]
    med = st.median(many) if many else None
    junk = [l for l in L if is_junk(l, med)]
    L = sorted([l for l in L if l not in junk], key=lambda l: l["bbox"][1])
    head = []
    if L:
        top = L[0]
        band = [l for l in L if l["bbox"][1] <= top["bbox"][3] - 0.3 * (top["bbox"][3] - top["bbox"][1])]
        head = [l for l in band if headlike(l)]
    ref, nums, rests = None, [], []
    for l in sorted(head, key=lambda l: l["bbox"][0]):
        r, rest = split_head(l["text"])
        if r and ref is None:
            ref = r
        rests.append(rest)
        nums += [int(t) for t in re.findall(r'(?<![\w.])(\d{1,3})(?![\w])', rest)]
    body = [l for l in L if l not in head]
    # a lone folio at the foot (chapter-opening pages print it there)
    foot = [l for l in body if l["bbox"][1] > 0.88 * p["h"] and re.fullmatch(r'\d{1,3}', l["text"].strip())]
    for l in foot:
        nums.append(int(l["text"].strip()))
    body = [l for l in body if l not in foot]
    title = " ".join(re.sub(r'[\d\W_]+', ' ', r).strip() for r in rests).strip()
    return {"head": " | ".join(l["text"] for l in sorted(head, key=lambda l: l["bbox"][0])),
            "ref": ref, "nums": nums, "title": title, "body": body, "junk": len(junk), "med": med}


def text_box(lines):
    xs0 = sorted(l["bbox"][0] for l in lines if len(l["words"]) >= 3)
    xs1 = sorted(l["bbox"][2] for l in lines if len(l["words"]) >= 3)
    if not xs0:
        return None
    return xs0[len(xs0) // 10], xs1[(9 * len(xs1)) // 10]


STOP = set("the and of to in is that which as be it by with for this not was his he are an on from but "
           "or have has its their they we our".split())


def layout(a, W, apparatus):
    """Split a leaf's body into: the epistle text above the notes, the
    apparatus under it, the notes in reading order (left column, then right),
    and a single-column tail. None if the leaf is not laid out in note columns."""
    body = a["body"]
    box = text_box(body)
    if not box:
        return None
    x0, x1 = box
    cx, tw = (x0 + x1) / 2, x1 - x0
    slack = 0.02 * W
    left = [l for l in body if l["bbox"][2] < cx + slack]
    right = [l for l in body if l["bbox"][0] > cx - slack]
    wide = lambda l: l["bbox"][2] - l["bbox"][0] > 0.28 * tw  # noqa: E731
    pairs = []
    for l in left:
        if not wide(l):
            continue
        for r in right:
            if wide(r) and abs(r["bbox"][1] - l["bbox"][1]) < 0.7 * max(l["xs"], 10):
                pairs.append((l, r))
                break
    if len(pairs) < 4:
        return None
    note_xs = st.median([l["xs"] for pr in pairs for l in pr])
    y_tc = min(min(l["bbox"][1], r["bbox"][1]) for l, r in pairs)
    in_cols = [l for l in left + right]
    zone_end = max(l["bbox"][3] for l in in_cols if l["bbox"][1] >= y_tc - 0.3 * note_xs)
    above, cols_l, cols_r, tail = [], [], [], []
    for l in body:
        y0 = l["bbox"][1]
        if y0 < y_tc - 0.3 * note_xs:
            above.append(l)
        elif l in left:
            cols_l.append(l)
        elif l in right:
            cols_r.append(l)
        elif y0 > zone_end - 0.3 * note_xs:
            tail.append(l)
        else:
            cols_l.append(l)          # a line across the gutter inside the notes: read with the left
    # The epistle's text is set in a larger type than the notes. A page whose
    # matter above the columns is in body type is an essay or a detached note
    # with its footnotes in two columns, not a commentary page.
    note_h = st.median([l["bbox"][3] - l["bbox"][1] for pr in pairs for l in pr])
    large = [l for l in above if l["bbox"][3] - l["bbox"][1] >= 1.25 * note_h or l["xs"] >= 1.25 * note_xs]
    small = [l for l in above if l not in large]
    prose = [l for l in small if sum(w[5].lower().strip(".,;:") in STOP for w in l["words"]) >= 2]
    if len(prose) >= 3:
        return None
    app, pre = [], []
    for l in small:
        (app if apparatus and l["xs"] < 0.92 * note_xs else pre).append(l)
    return {"text": large, "apparatus": app, "pre": pre, "left": C.merge_rows(cols_l),
            "right": C.merge_rows(cols_r), "tail": tail, "note_xs": note_xs}


def margin(col):
    xs = sorted(l["bbox"][0] for l in col if len(l["words"]) >= 3)
    return xs[len(xs) // 4] if xs else (min(l["bbox"][0] for l in col) if col else 0)


OPENER = re.compile(r'^[‘“"\'(]?(?:([IVXΙΠ][IVXLlΙΠ]{0,3})\.\s*)?([0-9IlOoSτt]{1,2})'
                    r'((?:\s*(?:[,—–\-]+|\s+and)\s*[0-9IlOoSτt]{1,2}){1,4})?\s*[.,]\s+(?=\D)')
RUN_LAST = re.compile(r'([0-9IlOoSτt]{1,2})\s*$')


def opener(text):
    """A verse number opening a note: (chapter printed with it or None, n,
    end of a run or None, 'read'|'read-fix') or None. 'II. 1, 2. ...' names
    its chapter; 'to.' is 10 with the OCR's letters undone."""
    m = OPENER.match(text)
    if not m:
        return None
    n = C.num(m.group(2))
    last = RUN_LAST.search(m.group(3)).group(1) if m.group(3) else None
    e = C.num(last) if last else None
    if n is None or n == 0 or (last and e is None):
        return None
    cp = FS.roman(m.group(1).translate(ROMANISH)) if m.group(1) else None
    if m.group(1) and not cp:
        return None
    fix = not m.group(2).isdigit() or bool(last and not last.isdigit())
    if e is not None and e <= n:
        e = None
    return cp, n, e, "read-fix" if fix else "read"


def stream(lay):
    """Note lines in reading order, each with whether it is indented."""
    out = [(l, True) for l in lay["pre"]]     # full-width matter above the columns: may open a verse
    for col in (lay["left"], lay["right"]):
        mg = margin(col)
        for l in col:
            ind = l["bbox"][0] - mg
            out.append((l, 0.45 * lay["note_xs"] <= ind <= 2.6 * lay["note_xs"]))
    return out

# ------------------------------------------------------------------ verses


def kjv_ids():
    with open(UIDS, encoding="utf-8") as f:
        return {k for k in json.load(f)["uids"] if k.startswith("kjv:")}


def verse_counts(ids, book):
    out = collections.defaultdict(int)
    for k in ids:
        b, c, v = k[4:].rsplit(".", 2)
        if b == book:
            out[int(c)] = max(out[int(c)], int(v))
    return dict(out)


class Decoder:
    """The verse sequence of one epistle's notes. An opener is accepted in
    the current chapter at or after the current verse (within the chapter's
    KJV verse count, and no further ahead than the page's running head allows),
    or as the opening verses of the next chapter where the running head or
    the end of the chapter says the chapter has turned."""
    GAP = 10

    def __init__(self, counts):
        self.counts = counts
        self.nch = max(counts)
        self.c, self.v = 1, 0

    def offer(self, n, e, hc, hv, cp=None, hsure=False, ahead=()):
        """hc: the chapter of the page's running head (None if unread); hsure:
        the next or previous leaf's head agrees with it; hv: the verse numbers
        the heads print; cp: a chapter printed with the opener itself."""
        c, v, cnt = self.c, self.v, self.counts
        if cp is not None:
            # a chapter printed with the number: taken if it is this one or the next
            if cp == c + 1 and n <= 4:
                return self._take(cp, n, e)
            if cp != c:
                if hsure and cp == hc and n <= cnt.get(cp, 0):
                    return self._take(cp, n, e)
                return None
        if hsure and hc is not None and hc not in (c, c + 1) and n <= cnt.get(hc, 0):
            return self._take(hc, n, e)      # two agreeing running heads put the notes elsewhere: follow them
        limit = max(hv) + 2 if hv else v + self.GAP
        if v <= n <= cnt.get(c, 0) and n <= max(limit, v + 3) and n - v <= self.GAP + 6:
            if not (hc == c + 1 and n <= 3 and v >= 3):
                return self._take(c, n, e)
        if c + 1 <= self.nch and n <= 4 and n < max(v, 1) \
                and (hc == c + 1 or (hc is None and v >= cnt.get(c, 0) - 3)):
            # a new chapter opens at its first verse: a later number with a '1.'
            # close behind is a list inside a note (or an additional note), not the turn
            if n > 1 and any(a[1] == 1 and a[0] in (None, c + 1) for a in ahead):
                return None
            return self._take(c + 1, n, e)
        if v - 2 <= n < v and n >= 1 and hc in (None, c):
            # a note on a verse just passed (Lightfoot takes 3 after 4 at Gal 1.3):
            # taken, and the sequence stays where it was
            return c, n, (e if e and e <= cnt.get(c, 0) and e - n <= 15 else None)
        return None

    def _take(self, c, n, e):
        if e is not None and (e > self.counts.get(c, 0) or e - n > 15):
            e = None
        self.c, self.v = c, n
        return c, n, e

# ------------------------------------------------------------------ scripture

FS.FAMILY.setdefault("eng", {}).update({
    "judg": "Judg", "judges": "Judg", "jude": "Jude", "jud": "Jude", "james": "Jas",
    "apoc": "Rev", "hebr": "Heb", "philem": "Phlm", "lk": "Luke", "mk": "Mark", "jn": "John",
})
SELF_VER = re.compile(r'\b(?:ver|vv|vers)\.\s*(\d{1,2})((?:\s*[,–—-]\s*\d{1,2}(?!\s*[a-zA-Z]{2,}\.))*)')
SELF_C = re.compile(r'\bc\.\s*([ivxl]{1,6})\.\s*(\d{1,2})\b')


_CHAPTERS = {}


def chapters(ids):
    if not _CHAPTERS:
        for k in ids:
            b, c, _ = k[4:].rsplit(".", 2)
            _CHAPTERS[b] = max(_CHAPTERS.get(b, 0), int(c))
    return _CHAPTERS


def scripture(text, ids, own=None, chapter=None):
    """English references in a unit's text, resolved in the KJV's numbering."""
    out, seen = [], set()
    for r in FS.parse("¶ " + text, "eng"):
        book, kind, ch, v, end, alt = r
        p = FS.printed(r)
        if p in seen:
            continue
        seen.add(p)
        if kind != "kjv":
            out.append({"ref": p, "resolved": False, "why": "a book outside the KJV", "rule": "text/kjv"})
            continue
        if v is None:
            why = ("cites a whole chapter, not a verse" if ch <= chapters(ids).get(book, 0) else
                   "no such chapter: another work cited by the same abbreviation (Ignatius's Ephesians...), "
                   "or an OCR misreading")
            out.append({"ref": p, "resolved": False, "why": why, "rule": "text/kjv"})
            continue
        t = f"kjv:{book}.{ch}.{v}"
        if t not in ids:
            out.append({"ref": p, "resolved": False, "why": "no such verse in the KJV (an OCR misreading, or "
                        "another numbering)", "rule": "text/kjv"})
            continue
        x = {"ref": p, "target": t, "resolved": True, "numbering": "english", "rule": "text/kjv"}
        if end and f"kjv:{book}.{ch}.{end}" in ids:
            x["through"] = f"kjv:{book}.{ch}.{end}"
        out.append(x)
    if own:
        hits = []
        if chapter:
            for m in SELF_VER.finditer(text):
                vs = [int(m.group(1))] + [int(x) for x in re.findall(r'\d{1,2}', m.group(2))]
                hits += [("self/ver", chapter, x) for x in vs]
        for m in SELF_C.finditer(text):
            c = FS.roman(m.group(1))
            if c:
                hits.append(("self/c", c, int(m.group(2))))
        for rule, c, v in hits:
            t = f"kjv:{own}.{c}.{v}"
            p = f"{own} {c}:{v}"
            if p in seen:
                continue
            seen.add(p)
            if t in ids:
                out.append({"ref": p, "target": t, "resolved": True, "numbering": "english", "rule": rule})
            else:
                out.append({"ref": p, "resolved": False, "why": "no such verse in the KJV", "rule": rule})
    return out

# ------------------------------------------------------------------ Greek


def _fold(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if not unicodedata.combining(c)).replace("ς", "σ").replace("ϲ", "σ")


GREEK_WORD = re.compile(r'[Ͱ-Ͽἀ-῿]+')
_VOCAB = None


def greek_vocab():
    """Strong's Greek lemmas and the forms of John in data/nt (both committed):
    a fixed yardstick for how much OCR'd Greek is Greek words."""
    global _VOCAB
    if _VOCAB is None:
        v = set()
        with open(STRONGS, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                if d["strongs"].startswith("G"):
                    v |= {_fold(w) for w in GREEK_WORD.findall(d.get("lemma") or "")}
        with open(NT_JOHN, encoding="utf-8") as f:
            for line in f:
                v |= {_fold(w) for w in GREEK_WORD.findall(line)}
        _VOCAB = v
    return _VOCAB


def greek_measure(texts):
    letters = greek = mixed = 0
    toks = known = 0
    vocab = greek_vocab()
    for t in texts:
        for c in t:
            if c.isalpha():
                letters += 1
                if 'Ͱ' <= c <= 'Ͽ' or 'ἀ' <= c <= '῿':
                    greek += 1
        for w in re.findall(r'\w+', t):
            g = any('Ͱ' <= c <= 'Ͽ' or 'ἀ' <= c <= '῿' for c in w)
            if g and any('a' <= c.lower() <= 'z' for c in w):
                mixed += 1
        for w in GREEK_WORD.findall(t):
            if len(w) >= 3:
                toks += 1
                known += _fold(w) in vocab
    return {"greek_letters": greek, "greek_share_of_letters": round(greek / letters, 4) if letters else 0,
            "greek_tokens_3plus": toks, "greek_tokens_in_reference_vocab": round(known / toks, 4) if toks else 0,
            "mixed_script_tokens": mixed}

# ------------------------------------------------------------------ printed pages


def printed_pages(nums_by_leaf):
    """{leaf: (page, 'read'|'neighbours')}. A folio read in the head is
    trusted when the leaves around it agree on the offset (leaf -> page);
    a leaf whose folio was not read takes the offset its nearest read
    neighbours on both sides agree on."""
    offs = {}
    for leaf, nums in nums_by_leaf.items():
        for n in nums:
            offs.setdefault(leaf, []).append(n - leaf)
    leaves = sorted(nums_by_leaf)
    good = {}
    for leaf in leaves:
        win = collections.Counter(o for q in leaves if abs(q - leaf) <= 12 and q != leaf for o in offs.get(q, []))
        for o in offs.get(leaf, []):
            if win[o] >= 2:
                good[leaf] = o
                break
    out = {leaf: (leaf + o, "read") for leaf, o in good.items()}
    gl = sorted(good)
    for leaf in leaves:
        if leaf in out:
            continue
        before = [q for q in gl if q < leaf and leaf - q <= 6]
        after = [q for q in gl if q > leaf and q - leaf <= 6]
        if before and after and good[before[-1]] == good[after[0]]:
            out[leaf] = (leaf + good[before[-1]], "neighbours")
    return out

# ------------------------------------------------------------------ scanned books


def ids_prefix(slug, book):
    return f"{book}." if slug in MULTI else ""


def page_unit(slug, s, leaf, lines, a, pp, extra=None):
    cols = C.columns(lines, max(l["bbox"][2] for l in lines) + 1) if lines else [lines]
    text = ""
    for col in cols:
        for l in col:
            text = C.join(text, l["text"])
        if len(cols) > 1 and col is not cols[-1]:
            text += " |"
    scan = {"leaves": [leaf]}
    if leaf in pp:
        scan["printed_page"] = pp[leaf][0]
        if pp[leaf][1] != "read":
            scan["printed_page_from"] = pp[leaf][1]
    if a["head"]:
        scan["running_head"] = a["head"]
    if len(cols) > 1:
        scan["columns"] = len(cols)
    u = {"id": f"{slug}:leaf.{leaf}",
         "ref": f"{s['short']}, " + (f"p. {pp[leaf][0]}" if leaf in pp else f"leaf {leaf}"),
         "kind": "page", "text": text, "links": [], "scan": scan}
    if a["title"]:
        u["section"] = a["title"]
    if extra:
        u["scan"].update(extra)
    return u


LECTURE = re.compile(r'LECTURE\s+([IVX]{1,4})\.')


def note_ref(s, book, c=None, n=None, e=None):
    """'Lightfoot on Gal 2.20': the commentator, then the verse his note is on."""
    who = s["short"].split(",")[0]
    if c is None:
        return f"{who} on {book}"
    return f"{who} on {book} {c}.{n}" + (f"-{e}" if e else "")


def hort_leaves(P):
    """Title page to the printer's imprint: the leaves with the book's text."""
    first = next(i for i, p in enumerate(P)
                 if any("LECTURES" in l["text"] for l in p["lines"]))
    # the imprint is printed twice, on the title verso and after the last page: the text ends at the last
    last = max(i for i, p in enumerate(P)
               if any("PRINTED BY" in l["text"].upper() and "CLAY" in l["text"].upper() for l in p["lines"]))
    return first, last


def build_scan(slug, ids):
    s = SCANS[slug]
    P = pages(slug)
    a0, b0 = s["leaves"] if s["leaves"] else hort_leaves(P)
    A = {leaf: analyse(P[leaf]) for leaf in range(a0, b0 + 1)}
    pp = printed_pages({leaf: a["nums"] for leaf, a in A.items()})
    seg = {}
    for book, x, y in s["epistles"]:
        for leaf in range(x, y + 1):
            seg[leaf] = book
    units, notes = [], collections.OrderedDict()
    m = collections.Counter()
    decoders = {book: Decoder(verse_counts(ids, book)) for book, _, _ in s["epistles"]}
    # pass 1: every leaf read; note lines collected with their page's evidence
    lines = []
    for leaf in range(a0, b0 + 1):
        a = A[leaf]
        m["junk_lines_dropped"] += a["junk"]
        lay = layout(a, P[leaf]["w"], s["apparatus"]) if leaf in seg else None
        if lay is None:
            if a["body"]:
                units.append(page_unit(slug, s, leaf, a["body"], a, pp))
                m["leaves_page"] += 1
            continue
        book = seg[leaf]
        nch = decoders[book].nch
        m["leaves_commentary"] += 1
        hc = 1 if nch == 1 else head_chapter(a["ref"], nch)
        nxt, prv = A.get(leaf + 1), A.get(leaf - 1)
        hc_next = (1 if nch == 1 else head_chapter(nxt["ref"], nch)) if nxt else None
        hc_prev = (1 if nch == 1 else head_chapter(prv["ref"], nch)) if prv else None
        hsure = hc is not None and hc in (hc_next, hc_prev)
        hv = head_verses(a["ref"]) + (head_verses(nxt["ref"]) if nxt and hc_next == hc else [])
        if lay["text"] or lay["apparatus"]:
            t = ""
            for l in lay["text"]:
                t = C.join(t, l["text"])
            u = {"id": f"{slug}:leaf.{leaf}.text",
                 "ref": f"{s['short']}, " + (f"p. {pp[leaf][0]}" if leaf in pp else f"leaf {leaf}") + ", text",
                 "kind": "epistle-text", "book": book, "text": t, "links": [],
                 "scan": {"leaves": [leaf]}}
            if lay["apparatus"]:
                u["apparatus"] = " ".join(l["text"] for l in lay["apparatus"])
            if a["head"]:
                u["scan"]["running_head"] = a["head"]
            if leaf in pp:
                u["scan"]["printed_page"] = pp[leaf][0]
            units.append(u)
        for l, indented in stream(lay):
            o = opener(l["text"]) if indented else None
            lines.append({"book": book, "leaf": leaf, "line": l, "indented": indented, "o": o,
                          "hc": hc, "hc_next": hc_next, "hv": hv, "hsure": hsure})
        if lay["tail"]:
            units.append(page_unit(slug, s, leaf, lay["tail"], a, pp, {"after_notes": True}))
            m["leaves_with_tail"] += 1
    # pass 2: the verse sequence, each candidate seeing the next few candidates
    current = {}
    cand = [i for i, x in enumerate(lines) if x["o"]]
    nxt_cand = {i: [(lines[j]["o"][0], lines[j]["o"][1]) for j in cand[k + 1:k + 7] if lines[j]["book"] == lines[i]["book"]]
                for k, i in enumerate(cand)}
    for i, x in enumerate(lines):
        book, leaf, l, indented, o = x["book"], x["leaf"], x["line"], x["indented"], x["o"]
        dec = decoders[book]
        hc = x["hc"]
        if hc is None and x["hc_next"] is not None and x["hc_next"] > dec.c:
            hc = x["hc_next"]
        cur = current.get(book)
        took = None
        if o:
            took = dec.offer(o[1], o[2], hc, x["hv"], o[0], x["hsure"], nxt_cand[i])
            m["openers_accepted" if took else "openers_rejected"] += 1
            if took and o[3] == "read-fix":
                m["openers_read_with_fix"] += 1
        if took:
            c, n, e = took
            key = f"{ids_prefix(slug, book)}{c}.{n}" + (f"-{e}" if e else "")
            if key not in notes:
                notes[key] = {"book": book, "c": c, "n": n, "e": e, "text": "", "leaves": [], "pages": []}
            cur = current[book] = key
        if cur is None:
            cur = current[book] = f"{ids_prefix(slug, book)}title"
            notes.setdefault(cur, {"book": book, "c": None, "n": None, "e": None, "text": "",
                                   "leaves": [], "pages": []})
        nu = notes[cur]
        nu["text"] = nu["text"] + "\n" + l["text"] if (indented and nu["text"]) else C.join(nu["text"], l["text"])
        if leaf not in nu["leaves"]:
            nu["leaves"].append(leaf)
            if leaf in pp and pp[leaf][0] not in nu["pages"]:
                nu["pages"].append(pp[leaf][0])
    for key, nu in notes.items():
        book = nu["book"]
        if nu["c"] is None:
            ref, links = f"{note_ref(s, book)}, before the first note", []
        else:
            vs = range(nu["n"], (nu["e"] or nu["n"]) + 1)
            links = [{"target": f"kjv:{book}.{nu['c']}.{v}", "type": "comments-on",
                      "resolved": f"kjv:{book}.{nu['c']}.{v}" in ids} for v in vs]
            ref = note_ref(s, book, nu["c"], nu["n"], nu["e"])
        u = {"id": f"{slug}:{key}", "ref": ref, "kind": "note", "book": book, "text": nu["text"], "links": links,
             "scan": {"leaves": nu["leaves"]}}
        if nu["pages"]:
            u["scan"]["printed_pages"] = nu["pages"]
        units.append(u)
    order = {"page": 0, "epistle-text": 0, "note": 1}
    units.sort(key=lambda u: (min(u["scan"]["leaves"]), order[u["kind"]]))
    if not s["epistles"]:
        # a book of lectures: each page says which lecture it is in, from the
        # 'LECTURE I.' heading that opens it (the ids stay the leaves)
        lect = None
        for u in units:
            mm = LECTURE.match(u["scan"].get("running_head", ""))
            if mm:
                lect = FS.roman(mm.group(1)) or lect
                m["lecture_headings"] += 1
            if lect:
                u["lecture"] = lect
    return units, m, (a0, b0), pp

# ------------------------------------------------------------------ Gutenberg

BLOCK = re.compile(r'<(h[1-6]|p|li|td)\b([^>]*)>(.*?)</\1>'
                   r'|<div class="(sidenote[^"]*)">(.*?)</div>'
                   r'|<div(?: class="([^"]*)")?>((?:(?!<div)(?!</div>)(?!<h[1-6])(?!<p\b)(?!<li\b)(?!<td\b).)*?)</div>',
                   re.S)
PAGENO = re.compile(r'<span class="pageno" id="Page_([0-9ivxlc]+)">[^<]*</span>')
ARROW = re.compile(r'<a href="#Page_[0-9ivxlc]+" class="pginternal">\s*(?:→|←|&gt;|&lt;|>|<)?\s*</a>')
ANCHOR = re.compile(r'<a id="([A-Za-z]+_\d+)"></a>(?:<sup>\d+</sup>)?')
FNREF = re.compile(r'<a id="(r\d+)"></a>')


def clean(x):
    x = ARROW.sub("", x)
    x = re.sub(r'<br\s*/?>', ' ', x)
    x = re.sub(r'<[^>]+>', '', x)
    return re.sub(r'\s+', ' ', html.unescape(x)).strip()


NOTE_OPEN = re.compile(r'^(?:([IV]{1,3})\.\s*)?(\d{1,2})(?:\s*[,–—-]\s*(\d{1,2}))?\.\s')


def gutenberg_rights(raw):
    head = raw[:raw.find("*** START")]
    if "COPYRIGHTED Project Gutenberg" in raw[:raw.find("*** START") + 2000] or "COPYRIGHTED" in head:
        raise SystemExit("the Gutenberg header says COPYRIGHTED: not shelved")
    m = re.search(r'This eBook is for the use of anyone anywhere in the United States[^<]*?(?=<|\n\n)', head)
    return re.sub(r'\s+', ' ', m.group(0)).strip() if m else None


def build_gutenberg(slug, ids):
    g = GUTENBERG[slug]
    src = os.path.join(CACHE, g["file"])
    if not os.path.exists(src) or sha256_file(src) != g["sha256"]:
        raise SystemExit(f"pinned file missing or changed: {src}\n  run: python3 pipeline/build_commentaries.py --fetch")
    with open(src, encoding="utf-8") as f:
        raw = f.read()
    rights_line = gutenberg_rights(raw)
    body = raw[raw.find("*** START"):raw.find("*** END")]
    fn_at = body.find('<div class="footnote"')
    main, fns = body[:fn_at], body[fn_at:]
    footnotes = {m.group(1): clean(m.group(2))
                 for m in re.finditer(r'<div class="footnote" id="(f\d+)">(.*?)</div>', fns, re.S)}
    m = collections.Counter()
    pages = collections.OrderedDict()      # page -> unit
    notes = collections.OrderedDict()
    greek = collections.OrderedDict()      # (book, c, v) -> text
    seen_anchor = []                       # (book, c, v) in order
    page, section, region = "front", None, None
    cur_note, cur_verse = None, None
    fn_home = {}
    roman_ch = {"I": 1, "II": 2, "III": 3, "IV": 4, "ph": 1}
    covered = 0
    for b in BLOCK.finditer(main):
        tag, inner = b.group(1), b.group(3)
        cm = re.search(r'class="([^"]*)"', b.group(2) or "")
        cls = cm.group(1) if cm else ""
        if tag is None and b.group(4):
            tag, cls, inner = "sidenote", b.group(4), b.group(5)
        elif tag is None:
            tag, cls, inner = "div", b.group(6) or "", b.group(7)
        if tag in ("h2", "h3"):
            t = clean(inner)
            region = next((bk for k, bk in g["regions"].items() if t.startswith(k)), None)
            section = t
            cur_note = None
        # split the block at page breaks
        parts = PAGENO.split(inner)
        segs = [(None, parts[0])] + [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]
        for i, (pg, frag) in enumerate(segs):
            if pg is not None:
                page = pg
            t = clean(frag)
            covered += len(t)
            if not t:
                continue
            refs = FNREF.findall(frag)
            if tag in ("h2", "h3"):
                hp = _page(pages, slug, page, section, g)
                hp.setdefault("headings", []).append(t)
                for r in refs:
                    fn_home[r] = ("page", page)
                continue
            if region:
                book = region
                if tag == "p" and "c000" in cls.split() and t.endswith("]"):
                    continue                                  # the running head ("I. 3]")
                if tag == "p" and "c032" in cls.split():       # Lightfoot's Greek text
                    pieces = re.split(r'<a id="([A-Za-z]+_\d+)"></a>', frag)
                    for j, piece in enumerate(pieces):
                        if j % 2 == 1:
                            mm = g["anchor"][book].match(piece)
                            if mm:
                                cur_verse = (book, roman_ch[mm.group(1)], int(mm.group(2)))
                                seen_anchor.append(cur_verse)
                            continue
                        x = clean(re.sub(r'<sup>\d+</sup>', '', piece))
                        if x and cur_verse:
                            greek[cur_verse] = (greek.get(cur_verse, "") + " " + x).strip()
                    continue
                mo = NOTE_OPEN.match(t) if (tag == "p" and i == 0) else None
                if mo:
                    n = int(mo.group(2))
                    e = int(mo.group(3)) if mo.group(3) and int(mo.group(3)) > n else None
                    c0 = cur_verse[1] if cur_verse and cur_verse[0] == book else 1
                    seen = {(x[1], x[2]) for x in seen_anchor if x[0] == book}
                    # the chapter of the latest Greek verse, unless the number is
                    # well past it and was printed in the chapter before (a note
                    # on 1.29 after the text has turned to 2.1)
                    if mo.group(1):
                        c = FS.roman(mo.group(1))           # 'IV. 1.' names its chapter
                    elif (c0, n) not in seen and (c0 - 1, n) in seen and n > cur_verse[2] + 2:
                        c = c0 - 1
                    else:
                        c = c0
                    m["openers"] += 1
                    if (c, n) not in seen:
                        m["openers_before_their_verse_anchor"] += 1
                    cur_note = f"{book}.{c}.{n}" + (f"-{e}" if e else "")
                    notes.setdefault(cur_note, {"book": book, "c": c, "n": n, "e": e, "paras": [], "pages": []})
                if cur_note is None:
                    cur_note = f"{book}.title"
                    notes.setdefault(cur_note, {"book": book, "c": None, "n": None, "e": None,
                                                "paras": [], "pages": []})
                nu = notes[cur_note]
                if i > 0 and nu["paras"]:
                    nu["paras"][-1] += " " + t              # the paragraph runs on over a page break
                else:
                    nu["paras"].append(t)
                if page not in nu["pages"]:
                    nu["pages"].append(page)
                for r in refs:
                    fn_home[r] = ("note", cur_note)
                continue
            u = _page(pages, slug, page, section, g)
            if tag == "sidenote":
                u.setdefault("sidenotes", []).append(t)
            else:
                u["_paras"].append(t)       # a paragraph cut by a page break: its second half opens the new page
            for r in refs:
                fn_home[r] = ("page", page)
    units = []
    for key, nu in notes.items():
        book = nu["book"]
        u = {"id": f"{slug}:{key}", "ref": note_ref(g, book, nu["c"], nu["n"], nu["e"]), "kind": "note",
             "book": book, "text": "\n".join(nu["paras"]), "links": [], "pages": nu["pages"]}
        if nu["c"] is not None:
            vs = range(nu["n"], (nu["e"] or nu["n"]) + 1)
            u["links"] = [{"target": f"kjv:{book}.{nu['c']}.{v}", "type": "comments-on",
                           "resolved": f"kjv:{book}.{nu['c']}.{v}" in ids} for v in vs]
        units.append(u)
    for (book, c, v), t in greek.items():
        units.append({"id": f"{slug}:text.{book}.{c}.{v}", "ref": f"{g['short']} {book} {c}.{v}, text",
                      "kind": "epistle-text", "book": book, "text": t,
                      "links": [{"target": f"kjv:{book}.{c}.{v}", "type": "text-of",
                                 "resolved": f"kjv:{book}.{c}.{v}" in ids}]})
    for pg, u in pages.items():
        u["text"] = "\n".join(u.pop("_paras"))
        units.append(u)
    byid = {u["id"]: u for u in units}
    for r, (kind, where) in fn_home.items():
        f = footnotes.get("f" + r[1:])
        if f is None:
            continue
        uid = f"{slug}:{where}" if kind == "note" else f"{slug}:p.{where}"
        byid[uid].setdefault("notes", []).append(f)
    m["footnotes"] = len(footnotes)
    m["footnotes_placed"] = sum(1 for r in fn_home if "f" + r[1:] in footnotes)
    total = len(clean(main))
    m["text_chars_captured"] = round(covered / total, 4) if total else 0
    return units, m, rights_line


def _page(pages, slug, page, section, g):
    if page not in pages:
        pages[page] = {"id": f"{slug}:p.{page}", "ref": f"{g['short']}, p. {page}", "kind": "page",
                       "text": "", "links": [], "_paras": []}
        if section:
            pages[page]["section"] = section
    return pages[page]


# ================================================================== the second shelf (2026-10-03)
#
# Henry Alford's Greek Testament (vols II-IV), J. A. Bengel's Gnomon in the
# T. & T. Clark English (vols II-IV), and Keil & Delitzsch's Biblical
# Commentary on the Old Testament (the Pentateuch and Delitzsch on the Psalms;
# Isaiah measured but not shelved), all from Internet Archive hOCR, every scan chosen by measuring
# its text layer (2026-10-03, on each item's _djvu.txt: Greek letters as a share
# of all letters; Greek tokens of 3+ letters found in the Strong's/John
# vocabulary above; English tokens found in the dwyl word list; Hebrew letters
# as a share of all letters):
#
#   Alford I (Gospels)  greektestamentwi01alfo 1849-cat. (Lane A's item), greektestamentwidv01alfo 1874,
#                       greektestamentwi189801alfo 1897: 0.0% Greek (every Greek word in Latin letters);
#                       greektestament00alfogoog 1849, greektestamentw00unkngoog 1863: ~100% Greek letters
#                       (the English OCR'd as Greek). bub_gb_YOY2AAAAMAAJ (Michigan): its text layer would
#                       not download (HTTP 500, 2026-10-03). NOT SHELVED: no scan keeps both languages.
#   Alford II           greektestamentwi02alfo 3rd ed. 1857  17.3%  34.1%  84.1%   <- chosen (Lane A's item)
#                       greektestamentwiptsl02alfo 1899 (7th ed., new impr.) 17.1% 34.8% 84.0% (not clearly better)
#                       greektestamentw02alfo 1849-cat., greektestamentwidvr02alfo 1874, greektestamentwi0002alfo
#                       1859: 0.0% Greek; greektestament02alfo 1868: ~100% Greek letters
#   Alford III          greektestamentwi00alfo 4th ed. 1865  15.4%  35.5%  86.8%   <- chosen (Lane A has no vol. III)
#                       greektestamentw03alfo 1849-cat. 15.8% 35.5% 86.5%; greektestamentwi0003alfo 1859: 0.0%;
#                       greektestament03alfo 1868: ~100% Greek letters; greektestamentwi03alfo 1856: no text layer (HTTP 500)
#   Alford IV           greektestamentwi04alfo 4th ed., Boston (Lee & Shepard) 14.0% 35.7% 87.6%  <- chosen (Lane A's item)
#                       greektestamentwi5604alfo 3rd ed. 1866 13.6% 35.5% 87.4%; greektestamentwiptsl04alfo 1897 14.0% 35.3%
#   Bengel I, V         every scan of the English Gnomon's vols I and V (gnomonofthenewte01benguoft 1857,
#                       gnomonofnewt01beng 1873, gnomonofnewtest01beng 1873, cu31924092350515 1877,
#                       cu31924092350531 1866, gnomonofnewtesta05beng 1859, the Philadelphia 2-vol. translation
#                       gnomonnewtestam00benggoog 1864 and johnalbertbenge00benggoog 1860...): 0.0% Greek. NOT SHELVED.
#   Bengel II + III     gnomonofnewtesta23beng 1873 (7th ed., vols II and III bound as one) 6.3% 34.4% 95.8%  <- chosen
#                       cu31924092350523 1877 (vol. II only) 5.9% 33.1% 95.7%; cu31924092350499 1877 (vol. III): 0.0%
#   Bengel IV           cu31924092350507 1877 (7th ed.) 7.5% 32.4% 95.3%   <- chosen
#                       gnomonofnewtesta03benguoft 1873: 0.0% Greek
#   (Neither CCEL nor Project Gutenberg has Bengel's Gnomon or Keil & Delitzsch: searched 2026-10-03.)
#   K&D: no scan of any volume keeps its Hebrew (0.00% Hebrew letters in all 40 measured: the pointed
#   Hebrew is OCR'd as Latin-letter debris). Chosen by English share:
#   Pentateuch I        thepentateuch01keiluoft 1878 95.2%  <- (pentateuch01keil 1866 95.1%, biblicalcomm01keiluoft 1869 94.8%)
#   Pentateuch II       biblicalcomm02keiluoft 1872 95.3%   <- (pentateuch02keiluoft 1872 95.2%)
#   Pentateuch III      pentateuch03keiluoft 1871 95.2%     <- (biblicalcommenta03keiluoft 1867 94.9%, pentateuch03keil 94.7%)
#   Psalms I            commentarypsalm01deliuoft 1880 91.6% <- (biblicalcommenta187101deli 1871 91.2%, ...188001 1877 91.2%)
#   Psalms II           biblicalcommenta187102deli 1871 91.3% <- (biblicalcommenta188002deli 1877 91.1%)
#   Psalms III          commentarypsalm03deliuoft 1880 92.0% <- (biblicalcommenta03deli 1877 91.2%, biblicalcomment02unkngoog no hOCR)
#   Isaiah I, II        biblicalcommenta1deliuoft / biblicalcoisaiah02deliuoft 1890 (4th ed.) 93.3% / 93.0%
#                       (isaiahsprophecie01/02deliuoft 1884 93.3/93.1%; the 1867 Indian-library scans 92.8/93.1%).
#                       NOT SHELVED YET: Delitzsch's Isaiah does not open its sections 'Ver. 3.' as the Pentateuch
#                       and the Psalms do (39 such openers in vol. I's 400 pages, against ~600 verses; the 1867
#                       translation measures the same on its text layer). It needs a reader keyed by the running
#                       heads ('CHAPTER V. 11, 12.', recto only) instead. Their hOCR, measured 2026-10-03:
#                       f05085fa5e015134f3b67c6bca38f35b539d0b4debfbad6b8eba09f4c7ccbb6a (vol. I),
#                       349c3a341f55971b7307b9f8dd95d91d0dc39e95925547968a97f36e988a0858 (vol. II).

def _alford(vol, ia, sha, edition, printed, copy, rights, leaves, books, lane_a):
    return {"ia": ia, "sha256": sha, "title": f"The Greek Testament, vol. {vol}", "short": f"Alford, Gk Test. {vol}",
            "author": "Henry Alford", "edition": edition, "printed": printed, "copy": copy, "ia_rights": rights,
            "leaves": leaves, "epistles": books, "apparatus": True, "reader": "alford", "lane_a": lane_a}


def _bengel(vol, ia, sha, edition, printed, copy, rights, leaves, books):
    return {"ia": ia, "sha256": sha, "title": f"Gnomon of the New Testament, vol. {vol}", "short": f"Bengel, Gnomon {vol}",
            "author": "J. A. Bengel", "edition": edition, "printed": printed, "copy": copy, "ia_rights": rights,
            "leaves": leaves, "epistles": books, "apparatus": False, "reader": "bengel"}


def _kd(title, short, author, ia, sha, edition, printed, copy, rights, leaves, books):
    return {"ia": ia, "sha256": sha, "title": title, "short": short, "author": author, "edition": edition,
            "printed": printed, "copy": copy, "ia_rights": rights, "leaves": leaves, "epistles": books,
            "apparatus": False, "reader": "kd"}


_ALF = ("Henry Alford, The Greek Testament: with a critically revised text, a digest of various readings, "
        "marginal references to verbal and idiomatic usage, prolegomena, and a critical and exegetical commentary")
_BEN = ("John Albert Bengel, Gnomon of the New Testament, now first translated into English, revised and edited "
        "by Andrew R. Fausset (Edinburgh: T. & T. Clark)")
_KD = "C. F. Keil and F. Delitzsch, Biblical Commentary on the Old Testament (Edinburgh: T. & T. Clark, Clark's Foreign Theological Library)"
_KDP = "C. F. Keil and F. Delitzsch"
SECOND = {
    "alford-commentary-2": _alford(
        "II", "greektestamentwi02alfo", "d19889cfbb6cf820564721633a48e0e26204a10bdf4a56211648400d56853a7e",
        f"{_ALF}, vol. II (Acts, Romans, Corinthians), 3rd ed. (London: Rivingtons; Cambridge: Deighton, Bell, 1857), "
        "as its title page reads", 1857, "University of California Libraries", "NOT_IN_COPYRIGHT", (5, 794),
        [("Acts", 105, 392), ("Rom", 393, 549), ("1Cor", 550, 698), ("2Cor", 699, 794)], True),
    "alford-commentary-3": _alford(
        "III", "greektestamentwi00alfo", "0d6492f87b3e3ce6a6adee9a61d5ff9832fd6f4ed83f1f5c5601511e5a7d26fd",
        f"{_ALF}, vol. III (Galatians to Philemon), 4th ed. (London: Rivingtons; Cambridge: Deighton, Bell, 1865), "
        "as its title page reads", 1865, "Boston University School of Theology", None, (7, 579),
        [("Gal", 145, 211), ("Eph", 212, 295), ("Phil", 296, 339), ("Col", 340, 391), ("1Thess", 392, 427),
         ("2Thess", 428, 443), ("1Tim", 444, 510), ("2Tim", 511, 551), ("Titus", 552, 572), ("Phlm", 573, 579)],
        False),
    "alford-commentary-4": _alford(
        "IV", "greektestamentwi04alfo", "770fee70202d9a1a3ccd92aacc00072cda2496ed124f984993dd70879ea544d5",
        f"{_ALF}, vol. IV (Hebrews to the Revelation), 4th ed. (Boston: Lee and Shepard; New York: Lee, Shepard and "
        "Dillingham), the American issue of Rivingtons' London edition; the title page is undated, the item's "
        "catalogue date is 1874", 1874, "Princeton Theological Seminary Library", "NOT_IN_COPYRIGHT", (5, 1057),
        [("Heb", 307, 579), ("Jas", 580, 636), ("1Pet", 637, 694), ("2Pet", 695, 726), ("1John", 727, 821),
         ("2John", 822, 827), ("3John", 828, 834), ("Jude", 835, 849), ("Rev", 850, 1057)], True),
    "bengel-gnomon-2": _bengel(
        "II", "gnomonofnewtesta23beng", "174e4034973d12427eea4bd705a47342e3be3274e9b03996b1d1027b5e593478",
        f"{_BEN}, vol. II (Luke, John, Acts), tr. Andrew R. Fausset, seventh edition (1873), as its title page "
        "reads; bound with vol. III", 1873,
        "Princeton Theological Seminary Library", "NOT_IN_COPYRIGHT", (9, 754),
        [("Luke", 13, 237), ("John", 238, 527), ("Acts", 528, 754)]),
    "bengel-gnomon-3": _bengel(
        "III", "gnomonofnewtesta23beng", "174e4034973d12427eea4bd705a47342e3be3274e9b03996b1d1027b5e593478",
        f"{_BEN}, vol. III (Romans, Corinthians), tr. James Bryce, seventh edition (1873), as its own title "
        "page (leaf 755) reads; bound after vol. II",
        1873, "Princeton Theological Seminary Library", "NOT_IN_COPYRIGHT", (755, 1199),
        [("Rom", 757, 960), ("1Cor", 961, 1110), ("2Cor", 1111, 1199)]),
    "bengel-gnomon-4": _bengel(
        "IV", "cu31924092350507", "ac11e9768744c1f7d7b1b98a7b0acfb3a17aefa66b3d63c178fa5dd66a385e1c",
        f"{_BEN}, vol. IV (Galatians to Hebrews), tr. James Bryce, seventh edition (1877), as its title page reads", 1877,
        "Cornell University Library", None, (4, 509),
        [("Gal", 8, 66), ("Eph", 67, 125), ("Phil", 126, 163), ("Col", 164, 195), ("1Thess", 196, 218),
         ("2Thess", 219, 244), ("1Tim", 245, 295), ("2Tim", 296, 323), ("Titus", 324, 333), ("Phlm", 334, 338),
         ("Heb", 339, 509)]),
}
# How each scan was chosen, carried into the manifest (scheme.scan_choice), so a reader of the manifest
# sees the other witnesses without opening this file.
SCAN_CHOICE = {
    "alford-commentary-2": "Lane A's item (same scan); measured against greektestamentwiptsl02alfo (1899): "
                           "Greek 17.3% vs 17.1% of letters, Greek tokens known 34.1% vs 34.8%: not clearly better",
    "alford-commentary-3": "greektestamentwi00alfo (4th ed., 1865; Lane A has no vol. III): Greek 15.4%, known 35.5%; "
                           "greektestamentw03alfo 15.8%/35.5% is a catalogue-1849 copy of unstated edition",
    "alford-commentary-4": "Lane A's item (same scan); measured against greektestamentwi5604alfo (3rd ed., 1866): "
                           "Greek 14.0% vs 13.6%, known 35.7% vs 35.5%",
    "bengel-gnomon-2": "gnomonofnewtesta23beng (vols. II and III bound as one): Greek 6.3%, known 34.4%; "
                       "cu31924092350523 (1877, vol. II) 5.9%/33.1%",
    "bengel-gnomon-3": "gnomonofnewtesta23beng (vols. II and III bound as one); cu31924092350499 (1877, vol. III): "
                       "0.0% Greek",
    "bengel-gnomon-4": "cu31924092350507 (1877): Greek 7.5%, known 32.4%; gnomonofnewtesta03benguoft (1873): 0.0% Greek",
}
# the chapter a volume's notes on a book begin at, where an earlier volume holds the book's start
FIRST_CHAPTER = {"keil-delitzsch-pentateuch-2": {"Exod": 12}, "delitzsch-psalms-2": {"Ps": 36},
                 "delitzsch-psalms-3": {"Ps": 84}}
for _k in SECOND:
    if _k in SCAN_CHOICE:
        SECOND[_k]["scan_choice"] = SCAN_CHOICE[_k]
    if _k in FIRST_CHAPTER:
        SECOND[_k]["first_chapter"] = FIRST_CHAPTER[_k]
SCANS.update(SECOND)
ORDER.extend(SECOND)
MULTI.update(k for k, s in SECOND.items() if len(s["epistles"]) > 1)

# ------------------------------------------------------------------ second shelf: Alford's page

ALF_APP = {"rec", "om", "ins", "txt", "bef", "aft", "rel", "latt", "vss", "syrr", "copt", "arm", "eth", "aeth",
           "vulg", "al", "chr", "thdrt", "lat-ff", "goth", "syr", "it", "elz", "lachm", "tischdf"}


def alford_layout(a, W):
    """Alford's page: the Greek text (with its marginal references), the
    digest of readings under it, then the notes in two columns. The columns
    are the largest cluster of side-by-side line pairs; everything above them
    is text or digest; the digest begins at the first line that reads like it
    (a verse number, or the digest's sigla: rec, om, txt, ins...)."""
    body = a["body"]
    box = text_box(body)
    if not box:
        return None
    x0, x1 = box
    cx, tw = (x0 + x1) / 2, x1 - x0
    slack = 0.02 * W
    left = [l for l in body if l["bbox"][2] < cx + slack]
    right = [l for l in body if l["bbox"][0] > cx - slack]
    wide = lambda l: l["bbox"][2] - l["bbox"][0] > 0.3 * tw  # noqa: E731
    pairs = []
    for l in left:
        if not wide(l):
            continue
        for r in right:
            if wide(r) and abs(r["bbox"][1] - l["bbox"][1]) < 0.7 * max(l["xs"], 10):
                pairs.append((l, r))
                break
    if len(pairs) < 4:
        return None
    lh = st.median([l["bbox"][3] - l["bbox"][1] for pr in pairs for l in pr])
    pairs.sort(key=lambda pr: pr[0]["bbox"][1])
    clusters = [[pairs[0]]]
    for pr in pairs[1:]:
        if pr[0]["bbox"][1] - clusters[-1][-1][0]["bbox"][1] > 3.5 * lh:
            clusters.append([])
        clusters[-1].append(pr)
    zone = max(reversed(clusters), key=len)
    if len(zone) < 4:
        return None
    note_xs = st.median([l["xs"] for pr in zone for l in pr])
    y_tc = min(min(l["bbox"][1], r["bbox"][1]) for l, r in zone)
    cols = [l for l in left + right if l["bbox"][1] >= y_tc - 0.3 * note_xs]
    zone_end = max(l["bbox"][3] for l in cols)
    above, cols_l, cols_r, tail = [], [], [], []
    for l in body:
        y0 = l["bbox"][1]
        if y0 < y_tc - 0.3 * note_xs:
            above.append(l)
        elif l in left:
            cols_l.append(l)
        elif l in right:
            cols_r.append(l)
        elif y0 > zone_end - 0.3 * note_xs:
            tail.append(l)
        else:
            cols_l.append(l)
    prose = [l for l in above if sum(w[5].lower().strip(".,;:") in STOP for w in l["words"]) >= 3]
    if len(prose) >= 4:
        return None                     # prose above two columns: a prolegomena page with footnotes
    above.sort(key=lambda l: l["bbox"][1])
    start = None
    for l in above:
        toks = [w[5].lower().strip(".,;:()[]") for w in l["words"]]
        sig = sum(t in ALF_APP for t in toks)
        if l["bbox"][2] - l["bbox"][0] > 0.5 * tw and (sig >= 2 or (re.match(r'\s*\d{1,2}\.\s', l["text"]) and sig >= 1)):
            start = l["bbox"][1]
            break
    text = [l for l in above if start is None or l["bbox"][1] < start]
    app = [l for l in above if start is not None and l["bbox"][1] >= start]
    return {"text": text, "apparatus": app, "left": C.merge_rows(cols_l), "right": C.merge_rows(cols_r),
            "tail": tail, "note_xs": note_xs}


ALF_OPEN = re.compile(r'(?<![\w.,;:\-])(?:([IVX]{1,5})\.\s*)?(\d{1,2})((?:\s*[,—–\-]+\s*\d{1,2}){0,3})\s?\.\s?'
                      r'(?:[\]\)\}\|]|[17J]{1,2}(?=\s)|(?=\s?[Ͱ-Ͽἀ-῿]))')
ALF_ABBR = {"ver", "vv", "vers", "ch", "chap", "c", "p", "pp", "cf", "see", "comp", "ib", "ibid", "l", "ll", "sect",
            "§", "v", "ff", "art", "no", "fol", "col", "bk", "lib", "ed", "vol", "n", "note", "and", "&"}


def alford_cands(text, prev):
    """Inline verse openers in a line of Alford's notes ('9.] As we said',
    '5. ᾧ ἡ δόξα', '6—10.| ANNOUNCEMENT'): [(pos, (chapter or None, n, end, how))].
    A number counts only after the end of a clause and not after a numeral or
    a reference's abbreviation ('Rom. ix. 3.' 'ver. 8.' are references)."""
    out = []
    for m in ALF_OPEN.finditer(text):
        before = (prev + " " + text[:m.start()]).rstrip()
        if before:
            if before[-1] not in ".)]};:!?’”\"'—|·":
                continue
            w = before.split()[-1].strip(".,;:()[]{}’‘'\"")
            if re.fullmatch(r'[ivxlcIVXLC]+|\d+', w) or w.lower() in ALF_ABBR:
                continue
        n = int(m.group(2))
        run = re.findall(r'\d{1,2}', m.group(3) or "")
        e = int(run[-1]) if run and int(run[-1]) > n else None
        cp = FS.roman(m.group(1)) if m.group(1) else None
        if n == 0 or (m.group(1) and not cp):
            continue
        out.append((m.start(), (cp, n, e, "read")))
    return out


ALF_ROMAN = str.maketrans({"Ι": "I", "Χ": "X", "Υ": "V", "l": "I", "1": "I", "|": "I"})


def alford_head(a, nch):
    """(chapter, verse numbers) of an Alford running head: its roman chapter
    stands alone or before the verses ('IV. 15—18.'), read only from the
    letters a roman numeral can have."""
    if nch == 1:
        return 1, head_verses(a["head"])
    for piece in re.split(r'\s*\|\s*|\s{2,}', a["head"]):
        for m in re.finditer(r'(?<![\w])([IVXΙΧΥl1|]{1,6})(?![A-Za-zͰ-Ͽἀ-῿])[.,:]?\s*((?:\d{1,2}\s*[—–\-,.]*\s*){0,3})', piece):
            tok = m.group(1).translate(ALF_ROMAN)
            if not re.fullmatch(r'[IVX]+', tok) or (tok == "I" and not m.group(1) in ("I", "Ι")):
                continue
            c = FS.roman(tok)
            if c and 1 <= c <= nch:
                return c, [int(x) for x in re.findall(r'\d{1,2}', m.group(2) or "")]
    return None, []

# ------------------------------------------------------------------ second shelf: the single-column page


def sc_page(p):
    """A single-column page (Bengel, Keil & Delitzsch): its running head,
    folio, body lines with whether each opens a paragraph, and the footnote
    block at the foot (smaller type), as (head, nums, body, foot, junk)."""
    L = [l for l in p["lines"] if l["words"] and l["text"].strip()]
    if not L:
        return "", [], [], [], 0
    many = [l for l in L if len(l["words"]) >= 4]
    med = st.median([l["xs"] for l in many]) if many else None
    medh = st.median([l["bbox"][3] - l["bbox"][1] for l in many]) if many else None
    L.sort(key=lambda l: l["bbox"][1])
    head = []
    if len(L) > 1 and len(L[0]["words"]) <= 10 and L[0]["bbox"][1] < 0.12 * p["h"]:
        t = L[0]
        letters = [c for c in t["text"] if c.isalpha()]
        if letters and sum(c.isupper() for c in letters) >= 0.5 * len(letters):
            head = [l for l in L if l["bbox"][1] < t["bbox"][3] - 0.3 * (t["bbox"][3] - t["bbox"][1])]
    rest = [l for l in L if l not in head]
    nums = []
    for l in head:
        for tok in l["text"].split():
            if re.fullmatch(r'\d{1,3}', tok) and (tok is l["text"].split()[0] or tok is l["text"].split()[-1]):
                nums.append(int(tok))
    # signature marks and a lone folio at the foot
    sig = [l for l in rest if l["bbox"][1] > 0.9 * p["h"] and len(l["words"]) <= 6
           and (re.fullmatch(r'[\W\d]*\d{1,3}[\W]*', l["text"].strip()) or re.search(r'VOL\.', l["text"]))]
    for l in sig:
        if re.fullmatch(r'\d{1,3}', l["text"].strip()):
            nums.append(int(l["text"].strip()))
    rest = [l for l in rest if l not in sig]
    junk = [l for l in rest if not any(c.isalnum() for c in l["text"])]
    rest = [l for l in rest if l not in junk]
    foot = []
    wh = lambda l: st.median([w[3] - w[1] for w in l["words"]])  # noqa: E731  (the type's height, per line)
    medw = st.median([wh(l) for l in many]) if many else None
    if medh:
        small = lambda l: wh(l) < 0.9 * medw or (med and l["xs"] < 0.88 * med)  # noqa: E731
        for l in reversed(rest):
            if small(l) or (foot and len(l["words"]) < 4):
                foot.insert(0, l)
            else:
                break
        while foot and not small(foot[0]):
            foot.pop(0)
        if len(foot) == len(rest):
            foot = []                   # a page all in small type is text, not footnotes
    body = [l for l in rest if l not in foot]
    xs0 = sorted(l["bbox"][0] for l in body if len(l["words"]) >= 4)
    mg = xs0[len(xs0) // 5] if xs0 else 0
    em = med or 40
    out = [(l, 0.6 * em <= l["bbox"][0] - mg <= 4.5 * em) for l in body]
    return " | ".join(l["text"] for l in sorted(head, key=lambda l: l["bbox"][0])), nums, out, foot, len(junk)


HEAD_ROMAN = str.maketrans({"Ι": "I", "Χ": "X", "Υ": "V", "l": "I", "|": "I"})


def sc_head(head, nch):
    """(chapter, verse numbers) of a single-column running head: 'CHAP. L.
    15-21.', 'PSALM XXXV. 1—3.', 'ST JOHN IV. 7-10.', 'EPHESIANS IV. 14, 15.'"""
    t = head.translate(HEAD_ROMAN)
    for m in re.finditer(r'(?<![A-Za-z])([IVXLC]{1,8})(?![A-Za-z])[.,:]?((?:\s*\d{1,3}\s*[—–\-,.]*){0,4})', t):
        c = FS.roman(m.group(1))
        if c and 1 <= c <= nch:
            vs = [int(x) for x in re.findall(r'\d{1,3}', m.group(2) or "") if int(x) <= 180]
            return c, vs
    if nch == 1:
        return 1, [int(x) for x in re.findall(r'\b\d{1,2}\b', t)]
    return None, []


BENGEL_OPEN = re.compile(r'^[‘“"\'(]?(?:([IVX]{1,5})\.\s*)?(\d{1,2})((?:\s*(?:[,—–\-]+|\s+and)\s*\d{1,2}){0,4})'
                         r'\s*[.,]\s*\d?\s*(?=[^\d\s])')
KD_OPEN = re.compile(r'[‘“"\'(]?(?:[VY][eco]r?s?|Ver)\s?[.,]\s*(\d{1,3})'
                     r'((?:\s*(?:[,—–\-]+|\s+and)\s*\d{1,3}){0,6})(?:\s*sqq?\.?)?(?:\s*[.,:;]|\s+(?=[a-z]))')


def sc_cand(text, reader):
    """A verse number opening a paragraph (Bengel): '14. μηκέτι)', '7.1 °Ex
    τῆς'."""
    m = BENGEL_OPEN.match(text)
    if not m:
        return None
    cp = FS.roman(m.group(1)) if m.group(1) else None
    if m.group(1) and not cp:
        return None
    n, run = int(m.group(2)), m.group(3)
    nums = [int(x) for x in re.findall(r'\d{1,2}', run or "")]
    e = nums[-1] if nums and nums[-1] > n else None
    return (cp, n, e, "read") if n else None


def kd_cands(text):
    """Keil & Delitzsch's section openers: 'Ver. 3.', 'Vers. 14-19.', 'Vers.
    9-12 contain', with a capital V (a reference inside a sentence is 'ver.
    3'), at the start of a line or after a dash or a sentence's end, where they
    run on inside a paragraph ('... rooted there. — Ver. 3. As Adam ...'):
    [(pos, (None, n, end, how))]."""
    out = []
    for m in KD_OPEN.finditer(text):
        before = text[:m.start()].rstrip()
        if before and before[-1] not in "—–-.;:!?)”\"'":
            continue
        n = int(m.group(1))
        nums = [int(x) for x in re.findall(r'\d{1,3}', m.group(2) or "")]
        e = nums[-1] if nums and nums[-1] > n else None
        if n:
            out.append((m.start(), (None, n, e, "read")))
    return out

PSALM_TITLE = re.compile(r'^\W{0,3}[PFr][SB]A[LI]M\s+([IVXLCl1]{1,9})[.,]?(?:\s*[-—–]\s*([IVXLCl1]{1,9})[.,]?)?\s*$')


def psalm_title(l, W, last):
    """Delitzsch's title line over each psalm ('PSALM XXXVI.', 'PSALM
    XLII.-XLIII.'), centred in the column: the psalm's number, read where it
    is the next psalm or a near one after the last read (a final I is often
    OCR'd as L: 'PSALM XLL'), else None."""
    m = PSALM_TITLE.match(l["text"])
    if not m or l["bbox"][0] < 0.15 * W:
        return None
    raw = m.group(1).replace("l", "I").replace("1", "I")
    for tok in (raw, raw[:-1] + "I" if raw.endswith("L") else None):
        n = FS.roman(tok) if tok else None
        if n and 1 <= n <= 150 and (last is None or last < n <= last + 3):
            return n
    return None

# ------------------------------------------------------------------ second shelf: numbering (Keil & Delitzsch)


_VMAP = None


def vmap():
    global _VMAP
    if _VMAP is None:
        import versification as V
        _VMAP = V.load()
    return _VMAP


def heb_counts(book):
    out = {}
    for k, n in vmap()["hebrew_chapters"].items():
        b, c = k.rsplit(".", 1)
        if b == book:
            out[int(c)] = n
    return out


def numbering_votes(pairs, ids):
    """Existence votes over (book, chapter, verse) as printed: a verse only the
    Hebrew (WLC) has is a vote for the Hebrew numbering, a verse only the KJV
    has a vote for the KJV's; a verse both have (or neither) says nothing."""
    heb = only_heb = only_kjv = 0
    for b, c, v in pairs:
        h = 1 <= v <= vmap()["hebrew_chapters"].get(f"{b}.{c}", 0)
        k = f"kjv:{b}.{c}.{v}" in ids
        if h and not k:
            only_heb += 1
        elif k and not h:
            only_kjv += 1
        heb += 1
    return {"read": heb, "only_hebrew": only_heb, "only_kjv": only_kjv}


def decide(v):
    """hebrew / kjv when one side has at least 5 votes and twice the other's;
    otherwise undecided (and then each reference is read where it exists)."""
    if v["only_hebrew"] >= 5 and v["only_hebrew"] >= 2 * v["only_kjv"]:
        return "hebrew"
    if v["only_kjv"] >= 5 and v["only_kjv"] >= 2 * v["only_hebrew"]:
        return "kjv"
    return "undecided"


def ot_link(b, c, v, numbering, ids, rule):
    """A link to an OT verse printed in `numbering` (hebrew / kjv / undecided)."""
    import versification as V
    osis = f"{b}.{c}.{v}"
    if numbering == "undecided":
        h = 1 <= v <= vmap()["hebrew_chapters"].get(f"{b}.{c}", 0)
        k = f"kjv:{osis}" in ids
        numbering = "hebrew" if (h and not k) else "kjv"
        rule += "/undecided"
    if numbering == "hebrew":
        r = V.resolve(osis, vmap(), ids)
        out = {"printed": osis, "numbering": "hebrew", "rule": rule}
        out.update(r)
        return out
    t = f"kjv:{osis}"
    if t in ids:
        return {"printed": osis, "target": t, "resolved": True, "numbering": "kjv", "rule": rule}
    return {"printed": osis, "resolved": False, "numbering": "kjv", "why": "no such verse in the KJV", "rule": rule}

# ------------------------------------------------------------------ second shelf: the build


def build_scan_2b(slug, ids):
    s = SCANS[slug]
    reader = s["reader"]
    P = pages(slug)
    a0, b0 = s["leaves"]
    seg = {}
    for book, x, y in s["epistles"]:
        for leaf in range(x, y + 1):
            seg[leaf] = book
    m = collections.Counter()
    units = []
    A = {leaf: analyse(P[leaf]) for leaf in range(a0, b0 + 1)}
    nums = {leaf: list(a["nums"]) for leaf, a in A.items()}
    SC = {}
    if reader != "alford":
        for leaf in range(a0, b0 + 1):
            SC[leaf] = sc_page(P[leaf])
            nums[leaf] = sorted(set(nums[leaf]) | set(SC[leaf][1]))
    pp = printed_pages(nums)
    kjv_counts = {book: verse_counts(ids, book) for book, _, _ in s["epistles"]}
    nch = {book: max(c) for book, c in kjv_counts.items()}
    items = []
    last_psalm = None
    for leaf in range(a0, b0 + 1):
        a = A[leaf]
        book = seg.get(leaf)
        if reader == "alford":
            m["junk_lines_dropped"] += a["junk"]
            lay = alford_layout(a, P[leaf]["w"]) if book else None
            if lay is None:
                if a["body"]:
                    units.append(page_unit(slug, s, leaf, a["body"], a, pp))
                    m["leaves_page"] += 1
                continue
            m["leaves_commentary"] += 1
            hc, hv = alford_head(a, nch[book])
            if lay["text"] or lay["apparatus"]:
                t = ""
                for l in lay["text"]:
                    t = C.join(t, l["text"])
                u = {"id": f"{slug}:leaf.{leaf}.text",
                     "ref": f"{s['short']}, " + (f"p. {pp[leaf][0]}" if leaf in pp else f"leaf {leaf}") + ", text",
                     "kind": "epistle-text", "book": book, "text": t, "links": [], "scan": {"leaves": [leaf]}}
                if lay["apparatus"]:
                    u["apparatus"] = " ".join(l["text"] for l in lay["apparatus"])
                if a["head"]:
                    u["scan"]["running_head"] = a["head"]
                if leaf in pp:
                    u["scan"]["printed_page"] = pp[leaf][0]
                units.append(u)
            prev = ""
            for col in (lay["left"], lay["right"]):
                for l in col:
                    items.append({"book": book, "leaf": leaf, "text": l["text"], "para": False,
                                  "cands": alford_cands(l["text"], prev), "hc": hc, "hv": hv})
                    prev = l["text"]
            if lay["tail"]:
                units.append(page_unit(slug, s, leaf, lay["tail"], a, pp, {"after_notes": True}))
                m["leaves_with_tail"] += 1
        else:
            head, _, body, foot, junk = SC[leaf]
            m["junk_lines_dropped"] += junk
            if not book:
                lines = [l for l, _ in body] + foot
                if lines:
                    aa = dict(a, head=head or a["head"])
                    units.append(page_unit(slug, s, leaf, lines, aa, pp))
                    m["leaves_page"] += 1
                continue
            m["leaves_commentary"] += 1
            hc, hv = sc_head(head, 150 if book == "Ps" else nch[book])
            hv = [v for v in hv if v not in SC[leaf][1]]          # not the folio
            prev = ""
            for l, para in body:
                ps = psalm_title(l, P[leaf]["w"], last_psalm) if book == "Ps" else None
                if ps:
                    last_psalm = ps
                    items.append({"book": book, "leaf": leaf, "text": l["text"], "para": True, "psalm": ps,
                                  "cands": [], "hc": hc, "hv": hv, "head": head})
                    m["psalm_titles_read"] += 1
                    continue
                if reader == "kd":
                    cands = kd_cands(l["text"])
                else:
                    c = sc_cand(l["text"], reader) if para else None
                    cands = [(0, c)] if c else []
                items.append({"book": book, "leaf": leaf, "text": l["text"], "para": para,
                              "cands": cands, "hc": hc, "hv": hv, "head": head})
                prev = l["text"]
            if foot:
                m["footnote_lines"] += len(foot)
                t = ""
                for l in foot:
                    t = C.join(t, l["text"])
                items.append({"book": book, "leaf": leaf, "text": t, "foot": True, "cands": [], "hc": hc, "hv": hv})
    # heads confirmed by the nearest headed leaves (a verso head may name only
    # the book): sure when a neighbour agrees, or the chapter lies between them
    headed = {}
    for it in items:
        if it["hc"] is not None:
            headed.setdefault(it["leaf"], (it["book"], it["hc"]))

    def near(leaf, book, step):
        for k in range(1, 4):
            h = headed.get(leaf + step * k)
            if h:
                return h[1] if h[0] == book else None
        return None
    for it in items:
        hn, hp = near(it["leaf"], it["book"], 1), near(it["leaf"], it["book"], -1)
        it["hc_next"] = hn
        it["hsure"] = it["hc"] is not None and (it["hc"] in (hn, hp) or (
            hn is not None and hp is not None and hp <= it["hc"] <= hn))
    # which numbering the volume's own verses are in (Keil & Delitzsch only)
    numbering = {}
    if reader == "kd":
        for book in kjv_counts:
            pairs = []
            seen_heads = set()
            for it in items:
                if it["book"] != book or it["hc"] is None:
                    continue
                if it["leaf"] not in seen_heads:
                    seen_heads.add(it["leaf"])
                    pairs += [(book, it["hc"], v) for v in it["hv"]]
                pairs += [(book, it["hc"], o[1]) for _, o in it["cands"]]
                pairs += [(book, it["hc"], o[2]) for _, o in it["cands"] if o[2]]
            v = numbering_votes(pairs, ids)
            v["decision"] = decide(v)
            numbering[book] = v
        m["numbering_own"] = numbering
    counts = {}
    for book in kjv_counts:
        if numbering.get(book, {}).get("decision") == "hebrew":
            counts[book] = heb_counts(book)
        elif numbering.get(book, {}).get("decision") == "undecided":
            hc_ = heb_counts(book)
            counts[book] = {c: max(n, hc_.get(c, 0)) for c, n in kjv_counts[book].items()}
        else:
            counts[book] = kjv_counts[book]
    decoders = {}
    for book in counts:
        d = HeadDecoder(counts[book])
        if reader == "kd":
            d.GAP, d.USE_HV = 30, False     # K&D's heads give the page's verses, not a bound on the notes
        d.c = s.get("first_chapter", {}).get(book, 1)     # a volume continuing a book starts where it does
        decoders[book] = d
    notes = decode_2b(slug, items, decoders, pp, m)
    for key, nu in notes.items():
        book = nu["book"]
        if nu["c"] is None:
            ref, links = f"{note_ref(s, book)}, before the first note", []
        elif nu.get("intro"):
            ref, links = f"{note_ref(s, book)} {nu['c']}, introduction", []
        else:
            vs = range(nu["n"], (nu["e"] or nu["n"]) + 1)
            nb = numbering.get(book, {}).get("decision")
            if nb:                  # an OT volume: its numbering measured, the Hebrew mapped
                links = [dict(ot_link(book, nu["c"], v, nb, ids, "comments-on"), type="comments-on") for v in vs]
                for lk in links:
                    lk.pop("rule", None)
            else:
                links = [{"target": f"kjv:{book}.{nu['c']}.{v}", "type": "comments-on",
                          "resolved": f"kjv:{book}.{nu['c']}.{v}" in ids} for v in vs]
            ref = note_ref(s, book, nu["c"], nu["n"], nu["e"])
        u = {"id": f"{slug}:{key}", "ref": ref, "kind": "intro" if nu.get("intro") else "note", "book": book,
             "text": nu["text"], "links": links, "scan": {"leaves": nu["leaves"]}}
        if nu["pages"]:
            u["scan"]["printed_pages"] = nu["pages"]
        if nu["notes"]:
            u["notes"] = nu["notes"]
        units.append(u)
    order = {"page": 0, "epistle-text": 0, "intro": 1, "note": 1}
    units.sort(key=lambda u: (min(u["scan"]["leaves"]), order[u["kind"]]))
    return units, m, (a0, b0), pp


class HeadDecoder(Decoder):
    """The base sequence, with three ways out of a missed chapter turn, each
    only where the base sequence refuses the number and only FORWARD:
    (1) a running head confirmed by its neighbours (hsure) names a later
    chapter that has the verse (K&D open a chapter's notes wherever its first
    section starts, 'Vers. 7-17', not at verse 1-4); (2) a chapter printed
    with the number ('VII. 1-40.', Alford's section heads) names a later
    chapter, at its verse 1-3, the page's running head names the same
    chapter, and the next numbers read go on from there;
    (3) three refusals running, each under a running head naming the same
    later chapter, which has the verse: the sequence was lost, the heads
    agree, follow them."""

    USE_HV = True

    def __init__(self, counts):
        super().__init__(counts)
        self.stuck = []

    def offer(self, n, e, hc, hv, cp=None, hsure=False, ahead=()):
        if not self.USE_HV:
            hv = ()
        nxt = [a for a in list(ahead)[:2]]
        if cp is not None and cp > self.c and len(nxt) == 2 and all(
                a[0] is None and self.v < a[1] <= self.counts.get(self.c, 0) and a[1] > n + 3 for a in nxt):
            return None         # 'IV. 1' while the numbers after it go on in this chapter: a reference
        r = super().offer(n, e, hc, hv, cp, hsure, ahead)
        if r is not None:
            self.stuck = []
            return r
        later = lambda c: c is not None and self.c < c <= self.nch and n <= self.counts.get(c, 0)  # noqa: E731
        if cp is None and hsure and later(hc) and (not hv or n <= max(hv) + 2):
            r = self._take(hc, n, e)
        elif cp is not None and later(cp) and cp == hc and n <= 3 \
                and all(a[0] is None and n <= a[1] <= n + 12 for a in list(ahead)[:2]):
            r = self._take(cp, n, e)
        elif cp is None and later(hc):
            self.stuck.append(hc)
            if len(self.stuck) >= 3 and len(set(self.stuck[-3:])) == 1:
                r = self._take(hc, n, e)
        else:
            self.stuck = []
        if r is not None:
            self.stuck = []
        return r


def decode_2b(slug, items, decoders, pp, m):
    """The verse sequence over the reading-order lines: each candidate opener
    is offered to its book's Decoder (seeing the next few candidates); a
    number far ahead of the sequence while a nearer one follows close behind
    is a misreading and is refused."""
    notes = collections.OrderedDict()
    current = {}
    flat = [(i, j) for i, it in enumerate(items) for j in range(len(it["cands"]))]
    seg, k = [], 0
    for it in items:
        k += 1 if it.get("psalm") else 0
        seg.append((it["book"], k))       # a psalm's title closes the look-ahead
    ahead = {}
    for k, (i, j) in enumerate(flat):
        ahead[(i, j)] = [items[i2]["cands"][j2][1][:2] for i2, j2 in flat[k + 1:k + 7] if seg[i2] == seg[i]]

    def unit(key, book, c=None, n=None, e=None):
        return notes.setdefault(key, {"book": book, "c": c, "n": n, "e": e, "text": "", "leaves": [], "pages": [],
                                      "notes": []})

    def put(key, text, leaf, para):
        nu = notes[key]
        if text:
            nu["text"] = nu["text"] + "\n" + text if (para and nu["text"]) else C.join(nu["text"], text)
        if leaf not in nu["leaves"]:
            nu["leaves"].append(leaf)
            if leaf in pp and pp[leaf][0] not in nu["pages"]:
                nu["pages"].append(pp[leaf][0])

    for i, it in enumerate(items):
        book, leaf = it["book"], it["leaf"]
        dec = decoders[book]
        pre = ids_prefix(slug, book)
        if current.get(book) is None:
            current[book] = f"{pre}title"
            unit(current[book], book)
        if it.get("foot"):
            unit(current[book], book)["notes"].append(it["text"])
            put(current[book], "", leaf, False)
            continue
        if it.get("psalm"):
            # a psalm's title line: the sequence moves to it, and what precedes its first verse note
            # (Delitzsch's introduction to the psalm) is the unit <c>.intro
            dec.c, dec.v = it["psalm"], 0
            current[book] = f"{pre}{it['psalm']}.intro"
            unit(current[book], book, it["psalm"])["intro"] = True
            put(current[book], it["text"], leaf, True)
            continue
        hc = it["hc"]
        if hc is None and it.get("hc_next") is not None and it["hc_next"] > dec.c:
            hc = it["hc_next"]
        pos, para = 0, it["para"]
        for j, (p, o) in enumerate(it["cands"]):
            cp, n, e, how = o
            nxt = ahead[(i, j)]
            if cp is None and n > dec.v + 1 and any(a[0] is None and dec.v < a[1] < n for a in nxt[:3]):
                m["openers_out_of_sequence"] += 1
                continue
            took = dec.offer(n, e, hc, it["hv"], cp, it["hsure"], nxt)
            m["openers_accepted" if took else "openers_rejected"] += 1
            if not took:
                continue
            c, n2, _ = took
            e2 = e if (e and n2 < e <= dec.counts.get(c, 0) and e - n2 <= 60) else None
            put(current[book], it["text"][pos:p].strip(), leaf, para)
            key = f"{pre}{c}.{n2}" + (f"-{e2}" if e2 else "")
            unit(key, book, c, n2, e2)
            current[book] = key
            pos, para = p, True
        put(current[book], it["text"][pos:].strip(), leaf, para)
    return notes


def harvest_2b(slug, units, ids):
    """Scripture in the second shelf's units. Alford and Bengel: the English
    references in the KJV's numbering, as the first shelf. Keil & Delitzsch:
    which numbering the volume cites the OT in is MEASURED (existence votes,
    Psalms and the other OT books apart), and each OT reference is resolved in
    it, the Hebrew through data/versification/bhs-kjv.json."""
    s = SCANS[slug]
    if s["reader"] != "kd":
        n = r = 0
        own_single = s["epistles"][0][0] if len(s["epistles"]) == 1 else None
        for u in units:
            book = u.get("book") or own_single
            ch = None
            if u["kind"] == "note":
                mm = re.match(r'(?:[1-3]?[A-Za-z]+\.)?(\d+)\.\d', u["id"].split(":", 1)[1])
                ch = int(mm.group(1)) if mm else None
            text = u["text"] + " " + " ".join(u.get("notes", []))
            found = scripture(text, ids, own=book if u["kind"] in ("note", "page") else None, chapter=ch)
            u["links"] += found
            n += len(found)
            r += sum(1 for x in found if x["resolved"])
        return n, r, {}
    import versification as V
    parsed = []
    votes = {"Ps": [], "other": []}
    for u in units:
        text = u["text"] + " " + " ".join(u.get("notes", []))
        refs = FS.parse("¶ " + text, "eng")
        parsed.append(refs)
        for book, kind, ch, v, end, alt in refs:
            if kind == "kjv" and v is not None and book in V.BOOKS:
                votes["Ps" if book == "Ps" else "other"].append((book, ch, v))
    measure = {}
    for k, pairs in votes.items():
        vv = numbering_votes(pairs, ids)
        vv["decision"] = decide(vv)
        measure[k] = vv
    own_num = {}
    n = r = 0
    for u, refs in zip(units, parsed):
        found, seen = [], set()
        for ref in refs:
            book, kind, ch, v, end, alt = ref
            p = FS.printed(ref)
            if p in seen:
                continue
            seen.add(p)
            if kind != "kjv":
                found.append({"ref": p, "resolved": False, "why": "a book outside the KJV", "rule": "text/kjv"})
                continue
            if v is None:
                found.append({"ref": p, "resolved": False, "why": "cites a whole chapter, not a verse", "rule": "text"})
                continue
            if book in V.BOOKS:
                cls = "Ps" if book == "Ps" else "other"
                x = dict(ref=p, **ot_link(book, ch, v, measure[cls]["decision"], ids, f"text/{cls}"))
            else:
                t = f"kjv:{book}.{ch}.{v}"
                x = ({"ref": p, "target": t, "resolved": True, "numbering": "kjv", "rule": "text/nt"} if t in ids else
                     {"ref": p, "resolved": False, "why": "no such verse in the KJV", "rule": "text/nt"})
            found.append(x)
        if u["kind"] == "note" and u.get("book"):
            mm = re.match(r'(?:[1-3]?[A-Za-z]+\.)?(\d+)\.\d', u["id"].split(":", 1)[1])
            if mm:
                b, c = u["book"], int(mm.group(1))
                nb = own_num.setdefault(b, s["_numbering"].get(b, {}).get("decision", "kjv"))
                for mt in SELF_VER.finditer(u["text"]):
                    for v in [int(mt.group(1))] + [int(x) for x in re.findall(r'\d{1,2}', mt.group(2))]:
                        p = f"{b} {c}:{v}"
                        if p not in seen:
                            seen.add(p)
                            found.append(dict(ref=p, **ot_link(b, c, v, nb, ids, "self/ver")))
                for mt in KD_CHAP.finditer(u["text"]):
                    c2 = FS.roman(mt.group(1))
                    p = f"{b} {c2}:{mt.group(2)}"
                    if c2 and p not in seen and c2 <= max(heb_counts(b)):
                        seen.add(p)
                        found.append(dict(ref=p, **ot_link(b, c2, int(mt.group(2)), nb, ids, "self/chap")))
        u["links"] += found
        n += len(found)
        r += sum(1 for x in found if x.get("resolved"))
    return n, r, {"numbering_references": measure}


KD_CHAP = re.compile(r'\b(?:chap|ch)\.\s*([ivxlc]{1,8})\.\s*(\d{1,3})\b')   # 'chap. ii. 4': the same book
HEBREW = re.compile(r'[֐-׿]')


def honesty_2b(slug):
    s = SCANS[slug]
    if s["reader"] == "alford":
        return ("notes keyed by verse where the OCR'd page lets them be: Alford runs his verse notes on inline "
                "('9.] As we said', '5. ᾧ ἡ δόξα'), so a verse number after the end of a clause, followed by a "
                "bracket or by Greek, and not after a reference's numeral or abbreviation, is a candidate, "
                "accepted when the verse sequence (and the fuzzily read running head) allows it; every following "
                "line, left column then right, belongs to it; boundaries are only as good as the numbers read off "
                "the page, and a misread or rejected number merges a verse's notes into the verse before (counts in "
                "measure); the Greek text block per leaf (leaf.N.text) with the digest of readings under it "
                "(apparatus) and the marginal references run into the text; every other page by scan leaf "
                "(leaf.N, the folio in scan.printed_page where read); unproofread OCR")
    if s["reader"] == "bengel":
        return ("notes keyed by verse where the OCR'd page lets them be: an indented paragraph opening with a verse "
                "number ('14. μηκέτι)') is a candidate, accepted when the verse sequence and the running head "
                "allow it; following paragraphs belong to it until the next; the translator's footnotes (the "
                "smaller type at a page's foot) go in `notes` of the unit open at that point; boundaries are only "
                "as good as the numbers read off the page (counts in measure); every other page by scan leaf "
                "(leaf.N); unproofread OCR")
    return ("notes keyed by verse where the OCR'd page lets them be: an indented paragraph opening 'Ver. 3.' or "
            "'Vers. 14-19.' is a candidate, accepted when the verse sequence and the running head ('CHAP. I. "
            "14-19.', 'PSALM V. 5—7.') allow it; following paragraphs, including the introduction to the next "
            "section, belong to it until the next accepted opener; ids are in the numbering the volume prints, "
            "MEASURED per book (measure.numbering_own) and linked to the KJV through bhs-kjv.json where it is the "
            "Hebrew's; the OT references in the text are resolved in the numbering measured for them "
            "(measure.numbering_references); footnotes in `notes`; every other page by scan leaf (leaf.N); the "
            "Hebrew words are lost: the OCR read the pointed Hebrew as Latin-letter debris, which stays in the "
            "text as printed by the OCR, unremoved; unproofread OCR")


def citation_2b(slug):
    lead = "book.chapter.verse" if slug in MULTI else "chapter.verse"
    extra = ", in the numbering the volume prints (scheme.numbering)" if SCANS[slug]["reader"] == "kd" else ""
    text = "leaf.N.text; " if SCANS[slug]["reader"] == "alford" else ""
    return (f"note: {lead} of the verse commented on{extra} (a run of verses: {lead}-end); {text}everything else: "
            "scan leaf (leaf.N; folio in scan.printed_page)")


def build_book_2b(slug, ids):
    """build_book for the second shelf: the same book shape, with the reader,
    the numbering measured, and Hebrew retention in measure."""
    s = SCANS[slug]
    units, m, (a0, b0), pp = build_scan_2b(slug, ids)
    s["_numbering"] = m.get("numbering_own", {})
    rights = {"license": f"public domain in the US (printed {s['printed']}); the scan and its OCR are the "
                         "Internet Archive's",
              "ia_possible_copyright_status": s["ia_rights"] or "(the item's metadata carries no rights field)",
              "attribution": f"Internet Archive, {s['ia']} ({s['copy']} copy)",
              "source_url": f"https://archive.org/details/{s['ia']}",
              "redistribute_whole": True}
    m["printed_page_read"] = sum(1 for x in pp.values() if x[1] == "read")
    m["printed_page_from_neighbours"] = sum(1 for x in pp.values() if x[1] != "read")
    n_links, n_resolved, extra = harvest_2b(slug, units, ids)
    numbering_own = m.pop("numbering_own", None)
    kinds = collections.Counter(u["kind"] for u in units)
    measure = {"units": dict(sorted(kinds.items())), **dict(sorted(m.items()))}
    cov = {}
    for b, _, _ in s["epistles"]:
        allv = {k for k in ids if k.startswith(f"kjv:{b}.")}
        cl = lambda u: [x for x in u["links"] if x.get("type") == "comments-on"]  # noqa: E731
        have = {x["target"] for u in units if u["kind"] == "note" and u.get("book") == b
                for x in cl(u) if x.get("resolved")}
        single = {x["target"] for u in units if u["kind"] == "note" and u.get("book") == b
                  for x in cl(u) if x.get("resolved") and len(cl(u)) == 1}
        chs = sorted({int(t.rsplit(".", 2)[1]) for t in have})
        cov[b] = {"kjv_verses": len(allv), "commented": len(have), "with_own_note": len(single)}
        if chs and (chs[0] > 1 or chs[-1] < max(verse_counts(ids, b))):
            # a volume holding part of a book: the verses of the chapters its notes reach
            cov[b]["chapters"] = [chs[0], chs[-1]]
            cov[b]["kjv_verses_in_chapters"] = sum(1 for k in allv if chs[0] <= int(k.rsplit(".", 2)[1]) <= chs[-1])
    measure["kjv_coverage"] = cov
    measure["scripture_links"] = {"read": n_links, "resolved": n_resolved}
    if numbering_own is not None:
        measure["numbering_own"] = numbering_own
    measure.update(extra)
    measure["greek"] = greek_measure(u["text"] for u in units)
    letters = heb = 0
    for u in units:
        letters += sum(c.isalpha() for c in u["text"])
        heb += len(HEBREW.findall(u["text"]))
    measure["hebrew"] = {"hebrew_letters": heb, "hebrew_share_of_letters": round(heb / letters, 4) if letters else 0}
    scheme = {"citation": citation_2b(slug), "resolution": "verse-note", "honesty": honesty_2b(slug), "status": "draft"}
    if numbering_own is not None:
        scheme["numbering"] = {b: v["decision"] for b, v in numbering_own.items()}
    if s.get("lane_a"):
        scheme["same_scan_as"] = "Lane A's raw-OCR shelf of this IA item (pipeline/henry-alford_shelf.json, branch claude/armarium-divines)"
    if s.get("scan_choice"):
        scheme["scan_choice"] = s["scan_choice"]
    source = {"format": "ia-hocr", "sha256": s["sha256"], "ia": s["ia"], "leaves": [a0, b0]}
    s.pop("_numbering", None)
    return {"slug": slug, "title": s["title"], "author": s["author"], "edition": s["edition"], "source": source,
            "scheme": scheme, "rights": rights, "measure": measure, "units": units}


# ------------------------------------------------------------------ books


def harvest(slug, units, ids):
    own = None
    if slug in SCANS and len(SCANS[slug]["epistles"]) == 1:
        own = SCANS[slug]["epistles"][0][0]
    n = r = 0
    for u in units:
        book = u.get("book") or own
        ch = None
        if u["kind"] == "note":
            k = u["id"].split(":", 1)[1]
            mm = re.match(r'(?:[1-3]?[A-Za-z]+\.)?(\d+)\.\d', k)
            ch = int(mm.group(1)) if mm else None
        text = u["text"] + " " + " ".join(u.get("notes", []))
        found = scripture(text, ids, own=book if u["kind"] in ("note", "page") else None, chapter=ch)
        u["links"] += found
        n += len(found)
        r += sum(1 for x in found if x["resolved"])
    return n, r


def honesty(slug, ocr):
    if not ocr:
        return ("notes keyed by verse exactly as the Project Gutenberg transcription marks them: a note "
                "paragraph opening with a verse number (or a run, '3-8.') starts that verse's unit, its chapter "
                "the latest verse anchor in Lightfoot's Greek text with that number; following lemma notes "
                "belong to it; Lightfoot's Greek text per verse (text.<book>.<c>.<v>); introductions, "
                "dissertations and index by printed page (p.N) as the transcription marks page breaks, "
                "footnotes on the unit holding their reference mark, marginal summaries in 'sidenotes'; the "
                "transcription is proofread (Distributed Proofreaders), not checked here against the print")
    if slug == "hort-ante-nicene":
        return ("page-exact: one unit per scan leaf (leaf.N), the printed folio in scan.printed_page where the "
                "running head gives it or its neighbours agree on it (scan.printed_page_from); each page"
                " carries the lecture it falls in (`lecture`, from the LECTURE headings), but lectures and paragraphs are NOT units; unproofread OCR")
    return ("notes keyed by verse where the OCR'd page lets them be: an indented verse number opening a note "
            "paragraph is accepted when the verse sequence (and the fuzzily read running head) allows it, "
            "and every following line, left column then right, belongs to it; boundaries are therefore only "
            "as good as the numbers read off the page, and a misread or rejected number merges a verse's notes "
            "into the verse before (counts in measure); the epistle's text block per leaf (leaf.N.text, with "
            "the critical apparatus under it where printed); every other page (introduction, detached and "
            "additional notes, dissertations, essays, index) by scan leaf (leaf.N, the folio in "
            "scan.printed_page where read); lines of bare accents dropped and counted; marginal summaries "
            "may be run into their lines; unproofread OCR")


def citation(slug, ocr):
    if slug == "hort-ante-nicene":
        return "scan leaf (leaf.N), one per printed page; the folio, where read, in scan.printed_page"
    lead = "book.chapter.verse" if slug in MULTI else "chapter.verse"
    pages = "printed page (p.N)" if not ocr else "scan leaf (leaf.N; folio in scan.printed_page)"
    return (f"note: {lead} of the verse commented on (a run of verses: {lead}-end); epistle text: "
            + ("text.book.chapter.verse" if not ocr else "leaf.N.text") + f"; everything else: {pages}")


def build_book(slug, ids):
    if slug in SECOND:
        return build_book_2b(slug, ids)      # the second shelf's reader
    ocr = slug in SCANS
    if ocr:
        s = SCANS[slug]
        units, m, (a0, b0), pp = build_scan(slug, ids)
        source = {"format": "ia-hocr", "sha256": s["sha256"], "ia": s["ia"], "leaves": [a0, b0]}
        rights = {"license": f"public domain in the US (printed {s['printed']}); the scan and its OCR are the "
                             "Internet Archive's",
                  "ia_possible_copyright_status": s["ia_rights"] or "(the item's metadata carries no rights field)",
                  "attribution": f"Internet Archive, {s['ia']} ({s['copy']} copy)",
                  "source_url": f"https://archive.org/details/{s['ia']}",
                  "redistribute_whole": True}
        meta = s
        m["printed_page_read"] = sum(1 for x in pp.values() if x[1] == "read")
        m["printed_page_from_neighbours"] = sum(1 for x in pp.values() if x[1] != "read")
    else:
        g = GUTENBERG[slug]
        units, m, line = build_gutenberg(slug, ids)
        source = {"format": "gutenberg-html", "sha256": g["sha256"], "pg": g["pg"], "url": g["url"]}
        rights = {"license": f"public domain in the US (printed {g['printed']}); Project Gutenberg's header is "
                             "not marked COPYRIGHTED",
                  "gutenberg_header": line,
                  "attribution": f"Project Gutenberg eBook #{g['pg']} (KD Weeks, Colin Bell and the Online "
                                 "Distributed Proofreading Team)",
                  "source_url": f"https://www.gutenberg.org/ebooks/{g['pg']}",
                  "redistribute_whole": True}
        meta = g
    n_links, n_resolved = harvest(slug, units, ids)
    kinds = collections.Counter(u["kind"] for u in units)
    measure = {"units": dict(sorted(kinds.items())), **dict(sorted(m.items()))}
    eps = [e[0] for e in SCANS[slug]["epistles"]] if ocr else list(GUTENBERG[slug]["regions"].values())
    if eps:
        cov = {}
        for b in eps:
            allv = {k for k in ids if k.startswith(f"kjv:{b}.")}
            have = {x["target"] for u in units if u["kind"] == "note" and u.get("book") == b
                    for x in u["links"] if x.get("type") == "comments-on" and x["resolved"]}
            single = {x["target"] for u in units if u["kind"] == "note" and u.get("book") == b
                      for x in u["links"] if x.get("type") == "comments-on" and x["resolved"]
                      and len([y for y in u["links"] if y.get("type") == "comments-on"]) == 1}
            cov[b] = {"kjv_verses": len(allv), "commented": len(have), "with_own_note": len(single)}
        measure["kjv_coverage"] = cov
    measure["scripture_links"] = {"read": n_links, "resolved": n_resolved}
    measure["greek"] = greek_measure(u["text"] for u in units)
    book = {"slug": slug, "title": meta["title"], "author": meta["author"], "edition": meta["edition"],
            "source": source,
            "scheme": {"citation": citation(slug, ocr), "resolution": "verse-note" if eps else "page",
                       "honesty": honesty(slug, ocr), "status": "draft"},
            "rights": rights, "measure": measure, "units": units}
    return book


def entry(book, blob):
    src = book["source"]
    where = f"PG #{src['pg']}" if "pg" in src else f"scan leaves {src['leaves'][0]}-{src['leaves'][1]} of {src['ia']}"
    return {"title": book["title"], "author": book["author"], "format": src["format"], "sha256": src["sha256"],
            "units": len(book["units"]),
            "scheme": dict(book["scheme"], note=f"{book['edition']}; {where}"),
            "rights": book["rights"], "measure": book["measure"],
            "built_sha256": hashlib.sha256(blob).hexdigest()}


def build(slugs=None):
    ids = kjv_ids()
    out = {}
    for slug in ORDER:
        if slugs and slug not in slugs:
            continue
        book = build_book(slug, ids)
        blob = json.dumps(book, ensure_ascii=False).encode("utf-8")
        out[slug] = (book, blob, entry(book, blob))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("books", nargs="*")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    built = build(a.books)
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    for slug, (book, _, e) in built.items():
        m = e["measure"]
        cov = " ".join(f"{b} {c['commented']}/{c['kjv_verses']}" for b, c in m.get("kjv_coverage", {}).items())
        print(f"  {slug:<22}{e['units']:>5} units  {dict(m['units'])}  {cov}  "
              f"scripture {m['scripture_links']['resolved']}/{m['scripture_links']['read']}  "
              f"greek {m['greek']['greek_share_of_letters']:.1%} known {m['greek']['greek_tokens_in_reference_vocab']:.1%}")
        if a.report:
            print("      " + json.dumps({k: v for k, v in m.items() if k not in ("units", "greek")},
                                        ensure_ascii=False))
    if a.report:
        return
    if a.check:
        bad = [s for s, (_, blob, e) in built.items() if manifest.get(s) != e]
        if bad:
            raise SystemExit(f"CHECK FAILED: rebuilt books differ from the manifest: {bad}")
        print("  CHECK PASSED: every book = its committed manifest entry (built_sha256).")
        return
    for slug, (_, blob, e) in built.items():
        write_atomic(os.path.join(BOOKS_DIR, slug + ".json"), blob)
        manifest[slug] = e
    write_atomic(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    print(f"  wrote {len(built)} books + {len(manifest)}-entry manifest")


if __name__ == "__main__":
    main()
