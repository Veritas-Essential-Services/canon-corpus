#!/usr/bin/env python3
# prov: 2026-10-03 drafted (Claude Code)
# fable_review: pending
"""
build_wycliffe.py -- the Wycliffite Bible as Forshall and Madden printed it,
*The Holy Bible ... in the earliest English versions made from the Latin
Vulgate by John Wycliffe and his followers* (Oxford, 1850), 4 vols, read
verse by verse out of the Internet Archive's OCR of the scans.

    python3 pipeline/build_wycliffe.py --fetch    # pinned hOCR -> data/corpus/wycliffe/ (gitignored, ~400 MB)
    python3 pipeline/build_wycliffe.py            # data/books/wycliffe-{earlier,later}.json + manifest entries
    python3 pipeline/build_wycliffe.py --check    # rebuild in memory: = the committed manifest entries
    python3 pipeline/build_wycliffe.py --report   # per-book measures, writes nothing
    python3 pipeline/build_wycliffe.py --survey   # where each column's chapter headings stand, for BOOKS
    python3 tests/wycliffe_test.py

SOURCE. No complete public-domain machine-readable Wycliffe exists:
eBible's engWycliffe holds nine books, Bible SuperSearch has none, and
CrossWire's complete module is CC BY-SA over an unnamed edition (awaiting
Adam; not used). So the text is the OCR (ABBYY FineReader hOCR, every word
with its box) the Internet Archive made of the University of Toronto copy,
all four volumes marked NOT_IN_COPYRIGHT:

    vol. I   Genesis - Ruth                   holybiblecontain01wycluoft  770 leaves
    vol. II  1 Kings - Psalms                 holybiblecontain02wycluoft  908 leaves
    vol. III Proverbs - 2 Maccabees           holybiblecontain03wycluoft  916 leaves
    vol. IV  the New Testament                holybiblecontain04wycluoft  786 leaves

The hOCR is pinned by sha256: the archive can re-derive its OCR, and a changed
file stops the build rather than silently changing the text.

THE PAGE. Two columns: the EARLIER version on the left, numbered in its LEFT
margin; the LATER version on the right, numbered in its RIGHT margin. Each
chapter opens with a heading in each column ('CAP. VI.', 'PSALM VII.'); the
running head gives the page's chapter and verse range in Roman and Arabic
('XVII. 24 - XVIII. 10.'). Under the text, in smaller type, the collation of
the manuscripts, whose reference letters are set as superscripts in the text
itself. In the outer margin, in smaller type, the later version's glosses
(and in the Psalter the Latin incipits). Verse numbers stand in the margin of
the LINE on which a verse begins, not before its first word.

WHAT IS READ, AND HOW. The text type is told from the apparatus by size; the
columns are split at the page's gutter (the widest empty strip near the
middle); in each column the margin words next to the text edge are the verse
numbers and anything further out is a gloss, dropped. The numbers are decoded
by a Viterbi pass (the state is chapter and verse): it prefers verse + 1,
takes a number read cleanly, undoes the OCR's letter-for-digit slips ('s' for
5, 'IG' for 16), allows a dropped or a stray marker, takes chapter breaks from
the headings, and is steered by the running head. A chapter's first verse is
the text after its heading (the later version rarely prints a '1'). Where a
verse begins mid-line the split is at the line's first sentence break, as in
build_charles.py: a guess, flagged per unit (`scan.start`).

NOT DONE (rule 2: nothing here edits the OCR). The collation letters stay
glued to the words they mark ('li3tb'); the yogh is the OCR's '3'. The text
is unproofread OCR and every book says so.

MEASURED, NOT CLAIMED. Each book of each version is measured against the
Clementine Vulgate's verse list (data/versification/vulgate-kjv.json,
`vulgate_chapters`): how many of its verse numbers have a unit, how many units
fall outside it, how many numbers were read, read with a fix, or inferred.
A book is kept verse by verse only if it clears MODE_BAR; otherwise its units
are its scan leaves. For the nine books eBible transcribes (the later version
only), each decoded later-version verse is also compared with eBible's verse
of the same number (`ebible_agreement`): a check on the verse DIVISION, made
against an independent transcription, never used to change the text. Every verse unit carries `kjv`, resolved through the
Clementine->KJV map (versification.resolve_vulgate): F&M number as the Vulgate
does, which is why ids are in the Vulgate's numbering ('wycliffe-later:Ps.50.3').

RIGHTS. Published 1850: public domain. The scans and their OCR are the
Internet Archive's, marked NOT_IN_COPYRIGHT. The built books are gitignored
like every other book; only manifest entries are committed.

Nothing is minted: unit ids are citations, not uids.
"""
import argparse
import collections
import difflib
import hashlib
import html
import json
import os
import re
import statistics as st
import sys
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import charles_ocr as C  # noqa: E402
import versification as V  # noqa: E402

BOOKS_DIR = os.path.join(ROOT, "data", "books")
MANIFEST = os.path.join(BOOKS_DIR, "manifest.json")
CACHE = os.path.join(ROOT, "data", "corpus", "wycliffe")
UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")

VOLUMES = {
    1: {"ia": "holybiblecontain01wycluoft", "title": "Vol. I: Genesis - Ruth",
        "sha256": "894d26547e8f8d75f86f6fd7dba0943a8055bbcfb13c9d50f177af87e3f8c72d"},
    2: {"ia": "holybiblecontain02wycluoft", "title": "Vol. II: I Kings - Psalms",
        "sha256": "f1dce32502f7654db2178082a53b021777732b63b6d32c72f863d8095c76b937"},
    3: {"ia": "holybiblecontain03wycluoft", "title": "Vol. III: Proverbs - II Maccabees",
        "sha256": "9e460c596cd2a62f3597fe3fbb2f901be3cb6919fcb4aa595a58cccab1b32500"},
    4: {"ia": "holybiblecontain04wycluoft", "title": "Vol. IV: the New Testament",
        "sha256": "a5e6ebc5c74ac67016cccc48930e3eb6b96e4514c8be3c439e957a0a9293c504"},
}
# eBible.org's engWycliffe (PD; copr.htm: "Public Domain"): the LATER version,
# nine books only. Used only to MEASURE the later version's verse division:
# each decoded verse is compared with eBible's verse of the same number.
EBIBLE = {"url": "https://ebible.org/Scriptures/engWycliffe_usfm.zip", "file": "engWycliffe_usfm.zip",
          "sha256": "d3bca9a2304c1c2df8b190c1bdde27baca3ddc25eb32d666da301f8c4f35ef3c",
          "books": {"Gen": "GEN", "Exod": "EXO", "Lev": "LEV", "Num": "NUM", "Deut": "DEU", "Matt": "MAT",
                    "Mark": "MRK", "Luke": "LUK", "John": "JHN"}}
EDITION = ("Josiah Forshall and Frederic Madden (eds), The Holy Bible, containing the Old and New "
           "Testaments, with the Apocryphal Books, in the earliest English versions made from the Latin "
           "Vulgate by John Wycliffe and his followers, 4 vols (Oxford: University Press, 1850)")
VERSIONS = {"earlier": ("L", "the earlier version (c. 1382), F&M's left column"),
            "later": ("R", "the later version (c. 1395), F&M's right column")}

# Vulgate book (the Clementine's code, as vulgate-kjv.json names it), volume,
# first and last scan leaf (0-based: archive.org/details/<ia>/page/n<leaf>),
# and F&M's name. Filled from --survey: the first leaf is the one whose
# columns open chapter I; the last is the next book's first leaf when the
# next book starts on it (the reader stops at that book's heading).
STARTS = {
    1: [("Gen", 150, "Genesis"), ("Exod", 264, "Exodus"), ("Lev", 364, "Leviticus"), ("Num", 435, "Numbers"),
        ("Deut", 535, "Deuteronomy"), ("Josh", 627, "Joshua"), ("Judg", 686, "Judges"), ("Ruth", 749, "Ruth"),
        (None, 759, None)],
    2: [("1Sam", 15, "I Kings"), ("2Sam", 99, "II Kings"), ("1Kgs", 167, "III Kings"),
        ("2Kgs", 245, "IV Kings"), ("1Chr", 325, "I Paralipomenon"), ("2Chr", 395, "II Paralipomenon"),
        ("Ezra", 488, "I Esdras"), ("Neh", 514, "II Esdras"), (None, 551, "III Esdras (not in the Clementine)"),
        ("Tob", 586, "Tobit"), ("Jdt", 612, "Judith"), ("Esth", 646, "Esther"), ("Job", 681, "Job"),
        ("Ps", 748, "Psalms"), (None, 897, None)],
    3: [("Prov", 9, "Proverbs"), ("Eccl", 61, "Ecclesiastes"), ("Song", 80, "Song of Solomon"),
        ("Wis", 92, "Wisdom"), ("Sir", 131, "Ecclesiasticus"), ("Isa", 234, "Isaiah"), ("Jer", 351, "Jeremiah"),
        ("Lam", 479, "Lamentations"), ("Bar", 491, "Baruch"), ("Ezek", 508, "Ezekiel"), ("Dan", 628, "Daniel"),
        ("Hos", 677, "Hosea"), ("Joel", 693, "Joel"), ("Amos", 700, "Amos"), ("Obad", 714, "Obadiah"),
        ("Jonah", 717, "Jonah"), ("Mic", 722, "Micah"), ("Nah", 732, "Nahum"), ("Hab", 737, "Habakkuk"),
        ("Zeph", 743, "Zephaniah"), ("Hag", 749, "Haggai"), ("Zech", 753, "Zechariah"), ("Mal", 774, "Malachi"),
        ("1Macc", 781, "I Maccabees"), ("2Macc", 853, "II Maccabees"), (None, 905, None)],
    4: [("Matt", 9, "Matthew"), ("Mark", 94, "Mark"), ("Luke", 150, "Luke"), ("John", 241, "John"),
        ("Rom", 311, "Romans"), ("1Cor", 345, "I Corinthians"), ("2Cor", 380, "II Corinthians"),
        ("Gal", 403, "Galatians"), ("Eph", 415, "Ephesians"), ("Phil", 427, "Philippians"),
        ("Col", 436, "Colossians"), (None, 446, "Laodiceans (not in the Clementine)"),
        ("1Thess", 447, "I Thessalonians"), ("2Thess", 455, "II Thessalonians"), ("1Tim", 460, "I Timothy"),
        ("2Tim", 471, "II Timothy"), ("Titus", 479, "Titus"), ("Phlm", 484, "Philemon"), ("Heb", 488, "Hebrews"),
        ("Acts", 515, "Deeds of Apostles"), ("Jas", 602, "James"), ("1Pet", 612, "I Peter"),
        ("2Pet", 622, "II Peter"), ("1John", 629, "I John"), ("2John", 638, "II John"), ("3John", 640, "III John"),
        ("Jude", 642, "Jude"), ("Rev", 647, "Apocalypse"), (None, 689, None)],
}
# (code, vol, first leaf, last leaf, F&M's name): a book runs to the next
# book's first leaf, where the reader stops at that book's rubric or heading
BOOKS = [(code, vol, a, nxt, name) for vol, rows in STARTS.items()
         for (code, a, name), (_, nxt, _) in zip(rows, rows[1:]) if code]

# a book of a version is read verse by verse only if at least this share of
# the Clementine's verse numbers have a unit and this share of its numbers
# were read off the page (as printed or with a letter-for-digit fix). The read
# bar is lower than Charles's (0.6) because it was measured: in the later
# version's Genesis and Matthew, 82% and 69% of the verses whose number was
# INFERRED read like eBible's verse of that number (91% and 85% of all).
MODE_BAR = {"coverage": 0.75, "read": 0.4}
T_TEXT = 42          # x_size between the apparatus (35-39) and the text (43-52)

# ------------------------------------------------------------------ fetch


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


def hocr_path(vol):
    return os.path.join(CACHE, VOLUMES[vol]["ia"] + "_hocr.html")


def download(url, dest, sha):
    if os.path.exists(dest) and sha256_file(dest) == sha:
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "canon-corpus/wycliffe"})
    with urllib.request.urlopen(req, timeout=900) as r, open(dest + ".tmp", "wb") as f:
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
    for vol, v in VOLUMES.items():
        download(f"https://archive.org/download/{v['ia']}/{v['ia']}_hocr.html", hocr_path(vol), v["sha256"])
        print(f"  {v['ia']}: hOCR present, sha256 pinned")
    download(EBIBLE["url"], os.path.join(CACHE, EBIBLE["file"]), EBIBLE["sha256"])
    print("  engWycliffe_usfm.zip (eBible, the later version's nine books, for the measure): present, sha256 pinned")


def ebible_verses():
    """{(code, ch, v): words} from eBible's later version, or None if not fetched."""
    p = os.path.join(CACHE, EBIBLE["file"])
    if not os.path.exists(p) or sha256_file(p) != EBIBLE["sha256"]:
        return None
    inv = {u: c for c, u in EBIBLE["books"].items()}
    out = {}
    with zipfile.ZipFile(p) as z:
        for n in z.namelist():
            m = re.match(r'\d+-([A-Z0-9]{3})engWycliffe\.usfm$', n)
            if not m or m.group(1) not in inv:
                continue
            c, cur = 0, None
            for ln in z.read(n).decode("utf-8").splitlines():
                mc = re.match(r'\\c (\d+)', ln)
                if mc:
                    c = int(mc.group(1))
                    continue
                mv = re.match(r'\\v (\d+) (.*)', ln)
                if mv:
                    cur = (inv[m.group(1)], c, int(mv.group(1)))
                    out[cur] = mv.group(2)
                elif cur and not ln.startswith("\\"):
                    out[cur] += " " + ln
    return {k: words(re.sub(r'\\[a-z0-9]+\*?', ' ', t)) for k, t in out.items()}


def words(t):
    """Lower-case words, the yogh (OCR '3') read as eBible's 'y'."""
    return re.findall(r'[a-z]+', t.lower().replace('3', 'y').replace('ȝ', 'y'))


def ebible_agreement(code, units, eb, vmap, kids):
    """Of the decoded verses eBible also has, how many read like eBible's verse
    (word-sequence similarity >= 0.6), fairly (>= 0.35), or not. eBible numbers
    as the KJV does (Deut 12.32 where the Vulgate has 13.1), so each verse is
    taken to its KJV verse(s) through the Clementine->KJV map first."""
    c = collections.Counter()
    for u in units:
        r = V.resolve_vulgate(f"{code}.{u['ch']}.{u['v']}", vmap, kids)
        if not r.get("resolved"):
            continue
        ks = [tuple([code] + [int(x) for x in t.split(":", 1)[1].split(".")[1:]])
              for t in r.get("spans", [r["target"]]) if not t.endswith(".title")]
        if not ks or any(k not in eb for k in ks):
            continue
        ref = [w for k in ks for w in eb[k]]
        r = difflib.SequenceMatcher(None, words(u["text"]), ref, autojunk=False).ratio()
        c["compared"] += 1
        c["agree" if r >= 0.6 else ("partly" if r >= 0.35 else "disagree")] += 1
    return {k: c[k] for k in ("compared", "agree", "partly", "disagree")}

# ------------------------------------------------------------------ hOCR (ABBYY)

# ABBYY's hOCR orders a line's attributes class, lang, title, id, so the
# Charles regexes (class, id, title) do not match it
LINE = re.compile(r'<span class="ocr_line"[^>]*?title="bbox (\d+) (\d+) (\d+) (\d+);[^"]*?x_size ([\d.]+)[^"]*"[^>]*>')
WORD = re.compile(r'<span class="ocrx_word"[^>]*?title="bbox (\d+) (\d+) (\d+) (\d+); x_wconf (\d+)[^"]*"[^>]*>'
                  r'(.*?)</span>', re.S)


def read_hocr(path):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    out = []
    for p in s.split('<div class="ocr_page"')[1:]:
        ms = list(LINE.finditer(p))
        lines = []
        for i, m in enumerate(ms):
            seg = p[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(p)]
            words = [(int(w.group(1)), int(w.group(2)), int(w.group(3)), int(w.group(4)), int(w.group(5)),
                      html.unescape(re.sub('<[^>]+>', '', w.group(6))).strip()) for w in WORD.finditer(seg)]
            words = [w for w in words if w[5]]
            if words:
                lines.append({"bbox": tuple(map(int, m.group(1, 2, 3, 4))), "xs": float(m.group(5)),
                              "words": words, "text": " ".join(w[5] for w in words)})
        bb = re.search(r'bbox 0 0 (\d+) (\d+)', p)
        out.append({"w": int(bb.group(1)), "h": int(bb.group(2)), "lines": lines})
    return out


_PAGES = {}


def pages(vol):
    """The volume's leaves, parsed once and cached (gzipped JSON) beside the hOCR."""
    if vol in _PAGES:
        return _PAGES[vol]
    v = VOLUMES[vol]
    cache = os.path.join(CACHE, f"{v['ia']}.{v['sha256'][:12]}.pages.json.gz")
    if not os.path.exists(cache):
        src = hocr_path(vol)
        if not os.path.exists(src) or sha256_file(src) != v["sha256"]:
            raise SystemExit(f"pinned hOCR missing or changed: {src}\n  run: python3 pipeline/build_wycliffe.py --fetch")
        C.save_pages(read_hocr(src), cache)
    _PAGES[vol] = C.load_pages(cache)
    return _PAGES[vol]

# ------------------------------------------------------------------ numbers

ROMAN_FIX = str.maketrans({'l': 'I', '1': 'I', 'i': 'I', '|': 'I', 'v': 'V', 'x': 'X', 'c': 'C', 'J': 'I',
                           'j': 'I', '!': 'I', ']': 'I'})
ROMAN_VAL = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}


def roman(s):
    """An OCR'd Roman numeral as a number, or None."""
    t = re.sub(r'[\s.,:;\'"’‘*-]', '', s).translate(ROMAN_FIX)
    if not t or any(c not in ROMAN_VAL for c in t):
        return None
    n = 0
    for i, c in enumerate(t):
        v = ROMAN_VAL[c]
        n += -v if i + 1 < len(t) and ROMAN_VAL[t[i + 1]] > v else v
    return n if 0 < n < 200 else None


# the OCR's misreadings of F&M's margin figures, as found in Genesis 1-6
# against the verse each must be ('sand' at Gen 1.5, 'a' at 1.8, 'e' at 1.6,
# 'H' at 1.14, 'u' at 1.11, 'IG' at 6.16)
ALT = {'I': '1', 'l': '1', 'i': '1', 't': '1', '|': '1', '!': '1', ']': '1', 'j': '1', 'J': '1',
       'O': '0', 'o': '0', 'D': '0', 'Q': '0', 'S': '58', 's': '58', 'a': '82', 'e': '6', 'G': '6',
       'b': '6', 'g': '9', 'q': '9', 'Z': '2', 'z': '2', 'B': '8', 'T': '7'}
ALT_MULTI = {'H': ('14', '11'), 'u': ('11',), 'n': ('11',), 'U': ('11',)}


def readings(tok):
    """Every number an OCR token of a margin figure can be read as."""
    t = tok.strip('.,:;\'"_*()[]{}’‘“”-—')
    if not t or len(t) > 3:
        return set()
    if t.isdigit():
        return {int(t)}
    outs = {''}
    for c in t:
        if c.isdigit():
            opts = (c,)
        elif c in ALT_MULTI:
            opts = ALT_MULTI[c]
        elif c in ALT:
            opts = tuple(ALT[c])
        else:
            return set()
        outs = {o + x for o in outs for x in opts}
    return {int(o) for o in outs if o and len(o) <= 3}


def fuzzy(n, tok):
    """The cost of reading margin token tok as verse n."""
    if tok == str(n):
        return 0.0
    r = readings(tok)
    if n in r:
        return 0.4 if len(r) == 1 else 0.6
    t = tok.strip('.,:;')
    if t.isdigit() and len(t) == len(str(n)) and sum(a != b for a, b in zip(t, str(n))) == 1:
        return 0.7
    return 1.0


def roman_cost(n, s):
    r = roman(s)
    if r == n:
        return 0.0
    if r is None:
        return 1.0
    return 1.5

# ------------------------------------------------------------------ the page

HEADING = re.compile(r'^\W{0,2}(?:C\s?A\s?[PF]|Cap|PSALM\w*|SALM\w*|Psalm\w*)\W{0,3}\s*([IVXLCivxlc1l|\]J!]'
                     r'[IVXLCivxlc1l|\]J!.\s]{0,9})\W{0,3}$')
RUBRIC = re.compile(r'(b[iey]g[iy]nn|begynn|biginn|\bend[iey]th\b|\beend[iey]th\b|\bendeth\b)', re.I)


def body_lines(p):
    """The page's text-type lines, below the running head. The apparatus
    (smaller type) is under the text, the glosses (smaller type) beside it."""
    H = p["h"]
    head = [l for l in p["lines"] if l["bbox"][3] < H * 0.075]
    body = [l for l in p["lines"] if l["bbox"][3] >= H * 0.075 and l["xs"] >= T_TEXT
            and not (l["bbox"][1] > H * 0.93 and len(l["words"]) <= 2)]
    return head, body


def gutter(body, W):
    """(x0, x1) of the widest empty strip between 30% and 70% of the width, or None."""
    # column lines only: a full-width line (a prologue, a title) runs across the gutter
    words = [w for l in body if len(l["words"]) >= 4 and l["bbox"][2] - l["bbox"][0] < 0.6 * W
             for w in l["words"] if len(w[5]) > 1 or w[5].isalnum()]
    if len(words) < 25:
        return None
    step = 5
    cov = [0] * (W // step + 2)
    for w in words:
        for x in range(w[0] // step, w[2] // step + 1):
            cov[x] += 1
    # a word the OCR ran across the gutter (leaf 177 of vol. I) must not hide it
    lo = min(cov[int(W * 0.3) // step: int(W * 0.7) // step])
    if lo > 3:
        return None
    best, run = None, None
    for i in range(int(W * 0.3) // step, int(W * 0.7) // step):
        if cov[i] <= lo:
            run = (run[0], i) if run else (i, i)
            if best is None or run[1] - run[0] > best[1] - best[0]:
                best = run
        else:
            run = None
    if best is None or (best[1] - best[0]) * step < 25:
        return None
    return best[0] * step, (best[1] + 1) * step


def split_columns(body, g):
    """Each line's words by side of the gutter: (left lines, right lines)."""
    mid = (g[0] + g[1]) / 2
    sides = {"L": [], "R": []}
    for l in body:
        # where ABBYY ran a left-column line into the right column's, it
        # stretched the left column's last word across the gutter ('Crist,'
        # on leaf 9 of vol. IV): that word is the left column's
        left, right = [], []
        for w in l["words"]:
            if w[0] < g[0] - 10 and w[2] > g[1]:
                left.append((w[0], w[1], g[0], w[3], w[4], w[5]))
            elif (w[0] + w[2]) / 2 < mid:
                left.append(w)
            else:
                right.append(w)
        for side, ws in (("L", left), ("R", right)):
            if ws:
                sides[side].append({"bbox": (min(w[0] for w in ws), min(w[1] for w in ws),
                                             max(w[2] for w in ws), max(w[3] for w in ws)),
                                    "xs": l["xs"], "words": ws, "text": " ".join(w[5] for w in ws)})
    return sides["L"], sides["R"]


def edge(col, side, xs):
    """The column's text edge on the numbered side: the commonest start (left
    column) or end (right column) of full lines of text."""
    c = collections.Counter()
    vals = []
    for l in col:
        if len(l["words"]) < 4:
            continue
        x = l["words"][0][0] if side == "L" else l["words"][-1][2]
        t = l["words"][0][5] if side == "L" else l["words"][-1][5]
        if side == "L" and not t[:1].isalpha():
            continue
        if side == "R" and not t[-1:].isalpha() and not t.endswith(('-', ',', ';', '.')):
            continue
        c[int(x // (0.25 * xs))] += 1
        vals.append(x)
    if not c:
        return None
    b, _ = c.most_common(1)[0]
    cand = sorted(x for x in vals if int(x // (0.25 * xs)) in (b - 1, b, b + 1))
    return cand[len(cand) // 2]


def local_edges(col, side, xs):
    """The text edge at each line. A scan can be skewed (leaf 171 of vol. I
    drifts 20 px down the page), so the edge is the median of the nearest
    full lines', not one value for the page."""
    e0 = edge(col, side, xs)
    if e0 is None:
        return [None] * len(col)
    pts = []
    for l in col:
        if len(l["words"]) < 4:
            continue
        w = l["words"][0] if side == "L" else l["words"][-1]
        t = w[5]
        x = w[0] if side == "L" else w[2]
        if abs(x - e0) > 1.0 * xs:
            continue
        if side == "L" and not t[:1].isalpha():
            continue
        if side == "R" and (not t[-1:].isalpha() and not t.endswith(('-', ',', ';', '.'))):
            continue
        pts.append(((l["bbox"][1] + l["bbox"][3]) / 2, x))
    out = []
    for l in col:
        y = (l["bbox"][1] + l["bbox"][3]) / 2
        near = sorted(pts, key=lambda p: abs(p[0] - y))[:9]
        out.append(st.median(x for _, x in near) if len(near) >= 3 else e0)
    return out


def margin(l, side, e, xs):
    """(margin tokens, text words, dropped words) of one column line."""
    ws = sorted(l["words"], key=lambda w: w[0])
    toks, text, drop = [], [], []
    if side == "L":
        for w in ws:
            t = w[5]
            if w[2] < e - 0.8 * xs and not (bool(readings(t)) and w[2] >= e - 1.4 * xs):
                if not toks and not text:
                    drop.append(w)          # a gloss or an incipit in the outer margin
                    continue
            if not text and w[0] < e - 0.3 * xs:
                if w[2] <= e + 0.3 * xs or (readings(t) and len(text) == 0 and len(t) <= 3
                                            and len(ws) > 1):
                    toks.append(C.digits(t))
                    continue
                m = re.match(r'^(\d{1,3})(\D.*)$', t)
                if m:
                    toks.append(m.group(1))
                    text.append(m.group(2))
                    continue
                k = max(1, round(len(t) * (e - w[0]) / max(1, w[2] - w[0])))
                if k < len(t) and readings(t[:k]) and t[k:k + 1].isalpha():
                    toks.append(t[:k])
                    text.append(t[k:])
                    continue
            text.append(t)
    else:
        keep = []
        for w in ws:
            if w[0] > e + 0.8 * xs and not (bool(readings(w[5])) and w[0] <= e + 1.2 * xs):
                drop.append(w)              # a gloss in the outer margin
                continue
            keep.append(w)
        tail = []
        while keep:
            w = keep[-1]
            t = w[5]
            if w[0] > e - 0.2 * xs and w[2] > e + 0.3 * xs and bool(readings(t)):
                tail.insert(0, C.digits(t))
                keep.pop()
                continue
            if w[2] > e + 0.4 * xs and w[0] < e:
                m = (re.match(r'^(.*?\D)(\d{1,3})$', t)
                     or re.match(r'^(.*?[A-Za-z,;.:-])(\d[0-9IlioOsSaeGzZ]{0,2})$', t))   # 'Raphayrn,2o'
                if m and readings(m.group(2)):
                    tail.insert(0, m.group(2))
                    keep[-1] = w[:5] + (m.group(1),)
                    break
                k = max(1, round(len(t) * (w[2] - e) / max(1, w[2] - w[0])))
                if k < len(t) and readings(t[-k:]) and t[-k - 1:-k].isalpha() and len(t) - k >= 2:
                    tail.insert(0, t[-k:])
                    keep[-1] = w[:5] + (t[:-k],)
            break
        toks = tail[-1:]
        text = [w[5] for w in keep]
    return toks, " ".join(text).strip(), drop


def head_chapters(head):
    """The running head's chapter range: 'XVII. 24 - XVIII. 10.' -> (17, 18)."""
    t = " ".join(l["text"] for l in sorted(head, key=lambda l: l["bbox"][0]))
    toks = t.split()
    first = last = None
    dash = False
    for i, tok in enumerate(toks):
        if re.fullmatch(r'[-—–~]+', tok) or tok.startswith(('—', '-')):
            dash = True
        core = tok.rstrip('.,:;')
        if re.fullmatch(r'[IVXLCivxlc]{1,7}\.?', tok) and tok.endswith('.') and len(core) >= 1:
            r = roman(core)
            if r is None or core.isupper() is False and len(core) < 2 and core not in ('i', 'v', 'x'):
                continue
            nxt = toks[i + 1] if i + 1 < len(toks) else ''
            if not re.match(r'^[0-9IlioSs]', nxt):
                continue
            if first is None:
                first = r
            elif dash:
                last = r
    if first is None:
        return None
    return (first, last or first)


_GUTTERS = {}


def volume_gutters(vol):
    """The usual gutter of the volume's versos and rectos (leaf parity): the
    median of the gutters found. A page whose OCR ran the columns' lines
    together (a book's first page, under a full-width prologue) uses it."""
    if vol not in _GUTTERS:
        found = {0: [], 1: []}
        for lf, p in enumerate(pages(vol)):
            g = gutter(body_lines(p)[1], p["w"])
            if g:
                found[lf % 2].append(g)
        _GUTTERS[vol] = {k: (int(st.median(a for a, _ in v)), int(st.median(b for _, b in v)))
                         for k, v in found.items() if v}
    return _GUTTERS[vol]


def fallback_gutter(body, g):
    """g, if most lines with text on both sides of it leave it empty."""
    if not g:
        return None
    both = [l for l in body if len(l["words"]) >= 4 and l["bbox"][0] < g[0] and l["bbox"][2] > g[1]]
    cross = [l for l in both if any(w[0] < g[0] - 10 and w[2] > g[1] + 10 for w in l["words"])]
    return g if len(both) >= 3 and len(cross) <= 0.5 * len(both) else None


def leaf_rows(p, side, default=None):
    """Rows of one column of one leaf, top to bottom: (kind, tokens, text).
    kind: 'c' chapter heading (tokens = [roman]), 'r' rubric, 'm' a line with
    a margin number, 't' text."""
    head, body = body_lines(p)
    g = gutter(body, p["w"]) or fallback_gutter(body, default)
    if g is None:
        return None, head_chapters(head), 0
    cols = dict(zip("LR", split_columns(body, g)))
    col = C.merge_rows(cols[side]) if cols[side] else []
    col = sorted(col, key=lambda l: l["bbox"][1])
    if not col:
        return [], head_chapters(head), 0
    xs = st.median(l["xs"] for l in col)
    es = local_edges(col, side, xs)
    rows, dropped = [], 0
    for l, e in zip(col, es):
        txt = l["text"].strip()
        m = HEADING.match(txt)
        if m and len(l["words"]) <= 5:
            rows.append(("c", [m.group(1)], txt))
            continue
        if e is None:
            rows.append(("t", [], txt))
            continue
        toks, text, drop = margin(l, side, e, xs)
        dropped += len(drop)
        if RUBRIC.search(text) and re.search(r'\b(He+re|Her|Heer)\b', text):
            rows.append(("r", [], text))
            continue
        toks = [t for t in toks if t]
        rows.append(("m" if toks else "t", toks, text))
    return rows, head_chapters(head), dropped

# ------------------------------------------------------------------ decoding

RESYNC = 7.0


def book_rows(vol, a, b, side, nxt_same_leaf):
    """The column's rows for a book: from the first chapter heading on its
    first leaf to (on a last leaf it shares with the next book) the next
    book's opening rubric or first heading."""
    P = pages(vol)
    rows, heads, stats = [], {}, collections.Counter()
    for lf in range(a, b + 1):
        rr, hc, dropped = leaf_rows(P[lf], side, volume_gutters(vol).get(lf % 2))
        stats["gloss_words_dropped"] += dropped
        if rr is None:
            stats["single_column_leaves_skipped"] += 1
            continue
        if hc:
            heads[lf] = hc
        if lf == a:
            k = next((i for i, r in enumerate(rr) if r[0] == "c" and roman(r[1][0]) == 1), None)
            if k is None:
                # no 'CAP. I.' read: the book's opening rubric ('Here bigynneth
                # the bok of Sapience') stands for it
                ks = [i for i, r in enumerate(rr) if r[0] == "r" and re.search(r'b[iey]g[iy]nn|begynn', r[2], re.I)]
                if ks:
                    k = ks[-1]
                    rr = rr[:k] + [("c", ["I."], "[opening rubric]")] + rr[k + 1:]
                    stats["chapter_1_from_rubric"] += 1
                else:
                    k = 0
                    stats["chapter_1_not_marked"] += 1
            rr = rr[k:]
        if lf == b and nxt_same_leaf and lf != a:
            k = next((i for i, r in enumerate(rr) if r[0] == "r" or (r[0] == "c" and roman(r[1][0]) == 1)), None)
            if k is not None:
                rr = rr[:k]
        for r in rr:
            rows.append((lf,) + r)
    return rows, heads, stats


def cut_beyond(rows, max_ch):
    """Stop at a heading for a chapter the Clementine does not have (the
    Prayer of Manasses that F&M print as II Paralipomenon XXXVII)."""
    for i, r in enumerate(rows):
        if r[1] == "c" and (roman(r[2][0]) or 0) == max_ch + 1:
            return rows[:i], len(rows) - i
    return rows, 0


def smooth(heads):
    pgs = sorted(heads)
    out = {}
    for i, p in enumerate(pgs):
        nb = [heads[q][0] for q in pgs[max(0, i - 3):i + 4] if q != p]
        if nb and abs(heads[p][0] - st.median(nb)) <= 2 and heads[p][1] >= heads[p][0]:
            out[p] = heads[p]
    return out


def decode(rows, heads, max_ch, nverses):
    """Viterbi over chapter headings and margin numbers.
    Returns {row index: (ch, v, how)}, how in 'chapter', 'verse', 'stray'."""
    ev = [i for i, r in enumerate(rows) if r[1] in "cm"]
    beam = {(0, 0): (0.0, None, None)}
    hist = []
    for i in ev:
        lf, kind, toks, _ = rows[i]
        nb = {}

        def put(s, cost, prev, how):
            if s[0] > max_ch or s[0] < 0:
                return
            if s[1] > nverses.get(s[0], 0) + 3:
                return
            if s not in nb or cost < nb[s][0]:
                nb[s] = (cost, prev, how)
        for (c, v), (cost, _, _) in beam.items():
            if kind == "c":
                s0 = toks[0]
                for k in (1, 2, 3):
                    put((c + k, 0), cost + (k - 1) * 2.5 + roman_cost(c + k, s0), (c, v), "chapter")
                r = roman(s0)
                if r and r > c + 3:
                    put((r, 0), cost + RESYNC, (c, v), "chapter")
                put((c, v), cost + 4.0, (c, v), "stray")
            else:
                s0 = toks[0]
                for k in range(1, 6):
                    # after a heading verse 1 is already open (the later version seldom
                    # prints its 1), so the first number met is as likely 2 as 1
                    skip = max(0, k - 2) if v == 0 else k - 1
                    put((c, v + k), cost + skip * 1.2 + fuzzy(v + k, s0), (c, v), "verse")
                if re.fullmatch(r'\d{1,3}', s0) and int(s0) not in range(v + 1, v + 6):
                    put((c, int(s0)), cost + RESYNC, (c, v), "verse")
                for nv in (1, 2):
                    put((c + 1, nv), cost + 4.0 + (nv - 1) + fuzzy(nv, s0), (c, v), "verse")
                put((c, v), cost + (2.0 if not readings(s0) else 3.0), (c, v), "stray")
        hc = heads.get(lf)
        if hc:
            for s in list(nb):
                if s[0] and not hc[0] <= s[0] <= hc[1]:
                    nb[s] = (nb[s][0] + 1.0,) + nb[s][1:]
        beam = dict(sorted(nb.items(), key=lambda kv: kv[1][0])[:300])
        hist.append(beam)
    if not hist:
        return {}
    s = min(beam, key=lambda x: beam[x][0])
    path = []
    for h in reversed(hist):
        path.append((s, h[s][2]))
        s = h[s][1]
    path.reverse()
    return {i: (st_[0], st_[1], how) for i, (st_, how) in zip(ev, path)}


def build_units(rows, assign):
    """Verse units: {ch, v, text, leaves, num, start}."""
    units, cur, stats = [], None, collections.Counter()
    for i, (lf, kind, toks, text) in enumerate(rows):
        if kind == "r":
            stats["rubric_lines_dropped"] += 1
            cur = None
            continue
        a = assign.get(i)
        if kind == "c" and a and a[2] == "chapter":
            ch = a[0]
            cur = {"ch": ch, "v": 1, "text": "", "leaves": [lf], "num": "heading", "start": "heading"}
            units.append(cur)
            stats["chapters"] += 1
            continue
        if kind == "m" and a and a[2] == "verse":
            ch, v, _ = a
            s0 = toks[0]
            how = "read" if s0 == str(v) else ("fuzzy" if fuzzy(v, s0) < 1 else "inferred")
            off, sh = C.verse_start(text, cur["text"] if cur else "")
            if cur is not None and off:
                cur["text"] = C.join(cur["text"], text[:off].strip())
                text = text[off:]
            elif cur is not None and sh == "line":
                # no break in the numbered line: the verse began at the last
                # sentence break of the line before ('... sees. And | 11 God sai3')
                tail = cur["text"][-45:]
                ms = list(C.SENT.finditer(tail))
                if ms and len(tail) - ms[-1].end() <= 25:
                    cut = len(cur["text"]) - len(tail) + ms[-1].end()
                    text = C.join(cur["text"][cut:].strip(), text)
                    cur["text"] = cur["text"][:cut].strip()
                    sh = "sentence-before"
            if cur and (cur["ch"], cur["v"]) == (ch, v):
                cur["text"] = C.join(cur["text"], text)
                if cur["num"] == "heading":
                    cur["num"] = how
                continue
            stats[how] += 1
            stats["start:" + sh] += 1
            cur = {"ch": ch, "v": v, "text": text, "leaves": [lf], "num": how, "start": sh}
            units.append(cur)
            continue
        if kind in "cm":
            stats["stray_markers"] += 1
        if cur is not None and text:
            cur["text"] = C.join(cur["text"], text)
            if cur["leaves"][-1] != lf:
                cur["leaves"].append(lf)
    units = [u for u in units if u["text"].strip()]
    for u in units:
        if u["num"] == "heading":
            stats["heading"] += 1
    return units, stats


def vulgate_map():
    return V.load(V.VULGATE_PATH)


def kjv_ids():
    if not os.path.exists(UIDS):
        return set()
    with open(UIDS, encoding="utf-8") as f:
        return {k for k in json.load(f)["uids"] if k.startswith("kjv:")}


def decode_book(code, vol, a, b, side, nxt_same_leaf, vmap):
    vc = vmap["vulgate_chapters"]
    nverses = {int(k.rsplit(".", 1)[1]): n for k, n in vc.items() if k.rsplit(".", 1)[0] == code}
    rows, heads, st1 = book_rows(vol, a, b, side, nxt_same_leaf)
    rows, cut = cut_beyond(rows, max(nverses))
    if cut:
        st1["rows_after_last_clementine_chapter_dropped"] = cut
    heads = smooth(heads)
    assign = decode(rows, heads, max(nverses), nverses)
    units, st2 = build_units(rows, assign)
    st1.update(st2)
    return units, st1, heads, nverses


def survey():
    """Each leaf where a column's heading reads chapter I (or a book's
    opening rubric stands), for filling BOOKS."""
    for vol in VOLUMES:
        P = pages(vol)
        print(f"== vol {vol}")
        for lf, p in enumerate(P):
            out = []
            for side in "LR":
                rr, hc, _ = leaf_rows(p, side, volume_gutters(vol).get(lf % 2))
                if not rr:
                    continue
                for r in rr:
                    if r[0] == "c" and roman(r[1][0]) == 1:
                        out.append(f"{side}:{r[2]}")
                    elif r[0] == "r" and re.search(r'bigynn|begynn|bygynn|biginn', r[2], re.I):
                        out.append(f"{side}:r:{r[2][:50]}")
            if out:
                head, _ = body_lines(p)
                print(lf, " | ".join(out), "||", " ".join(l["text"] for l in head)[:60])


# ------------------------------------------------------------------ books


def page_units(vol, a, b, side, name):
    """The book's text in this column, one unit per leaf (the fallback when
    its verses cannot be decoded well enough)."""
    rows, _, _ = book_rows(vol, a, b, side, True)
    by = collections.OrderedDict()
    for lf, kind, _, text in rows:
        if kind in "tm" and text:
            by.setdefault(lf, []).append(text)
    out = []
    for lf, ts in by.items():
        t = ""
        for x in ts:
            t = C.join(t, x)
        out.append((lf, t))
    return out


def measure_book(units, stats, heads, nverses):
    exp = {(c, v) for c, n in nverses.items() for v in range(1, n + 1)}
    have = collections.Counter((u["ch"], u["v"]) for u in units)
    hs = set(have)
    n = len(units)
    read = stats["read"] + stats["fuzzy"]
    by_leaf = collections.defaultdict(set)
    for u in units:
        by_leaf[u["leaves"][0]].add(u["ch"])
    ok = tot = 0
    for lf, h in heads.items():
        if lf in by_leaf:
            tot += 1
            ok += bool(by_leaf[lf] & set(range(h[0], h[1] + 1)))
    m = {"verses": n,
         "clementine_verses": len(exp), "present": len(exp & hs), "beyond_clementine": len(hs - exp),
         "duplicate_numbers": sum(1 for k, c in have.items() if c > 1),
         "number_read": stats["read"], "number_read_with_fix": stats["fuzzy"],
         "number_inferred": stats["inferred"], "verse_1_after_heading": stats["heading"],
         "start": {k[6:]: c for k, c in sorted(stats.items()) if k.startswith("start:")},
         "running_heads_agree": [ok, tot]}
    for k in ("gloss_words_dropped", "rubric_lines_dropped", "stray_markers", "single_column_leaves_skipped",
              "chapter_1_from_rubric", "chapter_1_not_marked", "rows_after_last_clementine_chapter_dropped"):
        if stats.get(k):
            m[k] = stats[k]
    m["_read_share"] = read / n if n else 0.0
    return m


def build_version(version, vmap, kids, only=None, eb=None):
    side, label = VERSIONS[version]
    slug = f"wycliffe-{version}"
    units, measures = [], {}
    for code, vol, a, b, name in BOOKS:
        if only and code not in only:
            continue
        vu, stats, heads, nverses = decode_book(code, vol, a, b, side, True, vmap)
        m = measure_book(vu, stats, heads, nverses)
        read = m.pop("_read_share")
        if version == "later" and eb and code in EBIBLE["books"]:
            m["ebible_agreement"] = ebible_agreement(code, vu, eb, vmap, kids)
        cov = m["present"] / m["clementine_verses"]
        good = cov >= MODE_BAR["coverage"] and read >= MODE_BAR["read"]
        m["resolution"] = "verse" if good else "page"
        if good:
            seen = collections.Counter()
            for u in vu:
                cite = f"{code}.{u['ch']}.{u['v']}"
                seen[cite] += 1
                uid = f"{slug}:{cite}" + (f"~{seen[cite]}" if seen[cite] > 1 else "")
                unit = {"id": uid, "ref": f"{name} {u['ch']}:{u['v']}", "text": u["text"].strip(), "links": [],
                        "scan": {"volume": vol, "leaves": u["leaves"], "number": u["num"], "start": u["start"]}}
                if seen[cite] > 1:
                    unit["scan"]["duplicate_number"] = True
                else:
                    unit["kjv"] = V.resolve_vulgate(cite, vmap, kids)
                units.append(unit)
        else:
            m["refused"] = (f"verse decoding below the bar (Clementine verses present {cov:.0%}, numbers read "
                            f"{read:.0%}): built by scan leaf instead")
            for lf, t in page_units(vol, a, b, side, name):
                units.append({"id": f"{slug}:{code}.leaf.{vol}.{lf}", "ref": f"{name}, vol. {vol} leaf {lf}",
                              "text": t, "links": [], "scan": {"volume": vol, "leaves": [lf]}})
        measures[code] = m
    tot = {k: sum(m[k] for m in measures.values()) for k in
           ("verses", "clementine_verses", "present", "beyond_clementine", "duplicate_numbers",
            "number_read", "number_read_with_fix", "number_inferred", "verse_1_after_heading")}
    tot["books_by_verse"] = sum(1 for m in measures.values() if m["resolution"] == "verse")
    tot["books_by_leaf"] = sum(1 for m in measures.values() if m["resolution"] == "page")
    tot["kjv_resolved"] = sum(1 for u in units if u.get("kjv", {}).get("resolved"))
    agr = [m["ebible_agreement"] for m in measures.values() if "ebible_agreement" in m]
    if agr:
        tot["ebible_agreement"] = {k: sum(x[k] for x in agr) for k in agr[0]}
    honesty = ("verse numbers decoded from the margin OCR of the 1850 scans; each unit says how its number was "
               "got (scan.number: read as printed, read with a letter-for-digit fix, inferred from the sequence, "
               "or 'heading' for a chapter's first verse, which follows its heading unnumbered); a verse that "
               "begins mid-line is split at a sentence break, a guess flagged in scan.start; the manuscripts' "
               "collation letters stay glued to the words they mark and the yogh is the OCR's '3'; text is "
               "unproofread OCR. Coverage of the Clementine's verses is measured per book (measure.books); a "
               "book below the bar is given by scan leaf, not by verse")
    book = {"slug": slug, "title": f"The Wycliffite Bible, {label.split(',')[0]} (Forshall and Madden 1850)",
            "author": "John Wycliffe and his followers; ed. Josiah Forshall and Frederic Madden",
            "edition": EDITION, "version": label,
            "source": {"format": "ia-hocr", "volumes": {str(k): {"ia": v["ia"], "sha256": v["sha256"]}
                                                        for k, v in VOLUMES.items()}},
            "scheme": {"citation": "Book.chapter.verse in the Clementine Vulgate's numbering (F&M number as "
                                   "the Vulgate); ids not linked to kjv: units, each unit's `kjv` resolves it",
                       "resolution": "verse",
                       "honesty": honesty},
            "rights": {"license": "public domain (published 1850); the scans and their OCR are the Internet "
                                  "Archive's, marked NOT_IN_COPYRIGHT",
                       "attribution": "Internet Archive, holybiblecontain01-04wycluoft (University of Toronto, "
                                      "Robarts Library copy)",
                       "source_url": "https://archive.org/details/holybiblecontain01wycluoft",
                       "redistribute_whole": True},
            "measure": {"total": tot, "books": measures, "mode_bar": MODE_BAR},
            "units": units}
    return slug, book


def entry(book, blob):
    return {"title": book["title"], "author": book["author"], "format": book["source"]["format"],
            "sha256": hashlib.sha256(json.dumps(book["source"]["volumes"], sort_keys=True).encode()).hexdigest(),
            "units": len(book["units"]),
            "scheme": dict(book["scheme"], note=f"{book['edition']}; {book['version']}"),
            "source": book["source"], "rights": book["rights"], "measure": book["measure"],
            "built_sha256": hashlib.sha256(blob).hexdigest()}


def build(only=None):
    vmap = vulgate_map()
    kids = kjv_ids()
    eb = ebible_verses()
    out = {}
    for version in VERSIONS:
        slug, book = build_version(version, vmap, kids, only, eb)
        blob = json.dumps(book, ensure_ascii=False).encode("utf-8")
        out[slug] = (book, blob, entry(book, blob))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--survey", action="store_true")
    ap.add_argument("books", nargs="*", help="Clementine book codes (report only)")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    if a.survey:
        survey()
        return
    if a.books and not a.report:
        raise SystemExit("a partial build would rewrite the books without the rest: use --report with book codes")
    built = build(a.books or None)
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    for slug, (book, _, e) in built.items():
        t = e["measure"]["total"]
        print(f"  {slug}: {e['units']} units; Clementine verses present {t['present']}/{t['clementine_verses']} "
              f"({t['present'] / t['clementine_verses']:.1%}); numbers read {t['number_read']}, with a fix "
              f"{t['number_read_with_fix']}, inferred {t['number_inferred']}; kjv resolved {t['kjv_resolved']}; "
              f"books by verse {t['books_by_verse']}, by leaf {t['books_by_leaf']}")
        if a.report:
            for code, m in e["measure"]["books"].items():
                print(f"    {code:<7}{m['resolution']:<6}{m['present']:>5}/{m['clementine_verses']:<5}"
                      f" beyond {m['beyond_clementine']:<3} dup {m['duplicate_numbers']:<3}"
                      f" read {m['number_read'] + m['number_read_with_fix']}/{m['verses']}"
                      f" heads {m['running_heads_agree'][0]}/{m['running_heads_agree'][1]}"
                      + (f" eBible {m['ebible_agreement']['agree']}/{m['ebible_agreement']['compared']}"
                         if "ebible_agreement" in m else ""))
    if a.report:
        return
    if a.check:
        bad = [s for s, (_, blob, e) in built.items() if manifest.get(s) != e]
        if bad:
            raise SystemExit(f"CHECK FAILED: rebuilt books differ from the manifest: {bad}")
        print("  CHECK PASSED: both versions = their committed manifest entries (built_sha256).")
        return
    for slug, (_, blob, e) in built.items():
        write_atomic(os.path.join(BOOKS_DIR, slug + ".json"), blob)
        manifest[slug] = e
    write_atomic(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    print(f"  wrote {len(built)} books + {len(manifest)}-entry manifest")


if __name__ == "__main__":
    main()
