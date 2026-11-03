#!/usr/bin/env python3
# prov: 2026-11-03 claude-opus-5-5 drafted
# fable_review: pending
"""art_harvest.py -- draft catalogs of page art from Gutenberg's illustrated HTML
editions (docs/ART-PLAN.md, section 4a).

    python3 pipeline/art_harvest.py --fetch pyle lang        # the shelves' HTML zips -> data/corpus/art/pg/ (gitignored)
    python3 pipeline/art_harvest.py pyle lang                # -> data/art/drafts/<slug>.jsonl + index.json
    python3 pipeline/art_harvest.py --check pyle lang        # rebuild from the cached zips: byte-identical
    python3 pipeline/art_harvest.py --candidates             # ornaments that recur across books

Adam, 2026-10-23: catalog every illustration, flourish and decorated initial,
with an anchor for where each sits, so a book can be rebuilt with its art.
2026-11-03: carry the plan past the King Arthur pilot to the illustrated books
already on the shelves.

DRAFTS, NOT THE CATALOG. No uid is minted here (minting waits for Adam's word,
ART-PLAN section 8). A row's address is a fact about the Gutenberg file that no
later fix can move: `pg503:images/i012.jpg#2` is the second time that image
file is placed in ebook 503. Rows carry no scan leaf: Gutenberg says WHERE a
piece sits and gives a copy of it; the scan that gives it at full size, with a
leaf and a box, is a later pass per book (the King Arthur example shows it).

ONE ROW PER PLACEMENT, in reading order: a picture, an ornament, or an initial,
with the printed page it sits on (when Gutenberg kept the page numbers), the
last heading before it, its place (before-heading / after-heading /
paragraph-start / in-text / end-of-section), its caption, and the words that
follow it (`before_quote`), which is how an anchor finds its spot in the house
text (ART-PLAN section 3). An image's pixel size, sha256 and dHash (a 64-bit
picture of its shape, robust to rescaling) come from the zip itself.

WHAT IS A GUESS. `kind` is set by rule and says so (`kind_by`):
  initial     a drop capital: an image whose alt text is one letter, an image or
              span whose class says so (dropcap, letra, initial...), or a small
              image just before a paragraph that opens with a broken word
  ornament    the same image placed 3+ times in the book (a printer's block), or
              a band at least 4x as wide as tall
  tailpiece   a small image ending a section (the next thing is a heading)
  cover       the cover image
  picture     everything else: it shows something -> the Pinacotheca
Full-page or not cannot be told from Gutenberg's resized copies: that waits for
the scan. Every row is unreviewed (`review`).

RIGHTS (rule 6; US public domain is the only test). A file whose header says
"COPYRIGHTED Project Gutenberg" is refused. A book's art is `pd_us: true` when
the shelf's own date for the edition is before 1931, otherwise "check".
"""
import argparse
import hashlib
import html as H
import io
import json
import os
import re
import sys
import time
import urllib.request
import zipfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, "data", "corpus", "art", "pg")
OUT = os.path.join(ROOT, "data", "art", "drafts")
ZIP_URL = "https://www.gutenberg.org/cache/epub/{id}/pg{id}-h.zip"
IMG_URL = "https://www.gutenberg.org/cache/epub/{id}/{src}"
UA = "WordHoard-art-catalog/1.0 (public-domain illustration study)"
PAUSE = 2.0   # seconds between Gutenberg requests

DROP_CLASS = re.compile(r"^(?:drop-?cap\w*|dcap|dropcap\w*|letra|initial\w*|init|firstletter|first-letter|"
                        r"bigletter|big-letter|illuminated|dc|capdrop|cap|largecap|bigcap|drop)$", re.I)
DROP_SRC = re.compile(r"(?:drop|initial|init|dcap|dropcap|letter|ltr|cap)[-_]?[a-z]?\d*\.\w+$", re.I)
PAGE_ID = re.compile(r"^(?:page|pg|p)[-_]?([0-9]+|[ivxlcdm]+)$", re.I)
SKIP_ID = re.compile(r"^pg-(?:header|footer)$")
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCKS = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "li", "table", "tr", "td",
          "figure", "figcaption", "br", "center", "pre", "dd", "dt"}
VOID = {"img", "br", "hr", "meta", "link", "input", "col", "area", "base", "wbr", "source"}
FIG = re.compile(r"fig|illus|image|caption|plate|center|picture|imag", re.I)


# ----------------------------------------------------------------------------- the shelves

def shelf_books(name):
    """-> [(slug, pg id, title, year or None)] from pipeline/<name>_shelf.json."""
    d = json.load(open(os.path.join(HERE, f"{name}_shelf.json"), encoding="utf-8"))
    out = []
    for slug, row in (d.get("gutenberg") or {}).items():
        if isinstance(row, dict):
            pg, title, year = row.get("id"), row.get("title", ""), row.get("year")
        else:
            pg, title, year = row[0], row[1] if len(row) > 1 else "", None
        if not isinstance(pg, int):
            continue
        if year is None:
            m = re.search(r"\((?:[^()]*?\b)?(1[4-9]\d\d)\b[^()]*\)\s*$", title) or re.search(r"\b(1[4-9]\d\d)\b", title)
            year = int(m.group(1)) if m else None
        out.append((slug, pg, title, year))
    return out


def fetch(pg):
    dest = os.path.join(CACHE, f"pg{pg}-h.zip")
    if os.path.exists(dest):
        return dest, "present"
    os.makedirs(CACHE, exist_ok=True)
    for i in range(4):
        try:
            req = urllib.request.Request(ZIP_URL.format(id=pg), headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
            if data[:2] != b"PK":
                return None, "not a zip"
            with open(dest + ".tmp", "wb") as f:
                f.write(data)
            os.replace(dest + ".tmp", dest)
            return dest, f"{len(data):,} bytes"
        except urllib.error.HTTPError as e:   # noqa: PERF203
            if e.code == 404:
                return None, "no HTML zip (404)"
            if i == 3:
                return None, f"HTTP {e.code}"
        except Exception as e:  # noqa: BLE001
            if i == 3:
                return None, f"failed: {e}"
        time.sleep(PAUSE * (2 ** i))
    return None, "failed"


# ----------------------------------------------------------------------------- the walk

class Walk(HTMLParser):
    """Reading-order walk of one HTML file: the text (boilerplate, page numbers and
    captions left out), and where in it each picture, page number and heading falls."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []          # chunks of running text
        self.n = 0              # its length so far
        self.stack = []         # [tag, classes, id, flags]
        self.events = []        # (offset, kind, data)
        self.skip = 0           # inside boilerplate, a page number or a caption
        self.boiler = 0         # inside Gutenberg's own header or footer
        self.heading = None     # [start offset, chunks]
        self.capture = None     # caption being read: [stack depth, chunks, event]
        self.last_block_end = 0

    def _push_text(self, s):
        if not s:
            return
        if self.text and not self.text[-1].endswith(" ") and s.startswith(" "):
            pass
        self.text.append(s)
        self.n += len(s)

    def _space(self):
        if self.text and not self.text[-1].endswith(" "):
            self._push_text(" ")

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        ident = a.get("id") or ""
        flags = set()
        if SKIP_ID.match(ident) or any(c.startswith("pg-boilerplate") for c in cls):
            flags.add("skip")
            flags.add("boiler")
        if any(c == "pagenum" or c.startswith("pagenum") or c == "pageno" for c in cls):
            flags.add("skip")
        m = PAGE_ID.match(ident) or (PAGE_ID.match(a.get("name") or ""))
        if m and not self.boiler:
            self.events.append((self.n, "page", m.group(1)))
        if any(DROP_CLASS.match(c) for c in cls) and tag in ("span", "p", "div", "b", "big", "strong", "font"):
            flags.add("dropcap")
            self.events.append((self.n, "dropspan", {"cls": " ".join(cls), "start": self.n}))
        if tag in BLOCKS:
            self._space()
        if tag in HEADINGS and not self.skip:
            self.heading = [self.n, []]
        if tag == "img":
            if not self.skip:
                self._img(a, cls)
            return
        if tag in VOID:
            return
        self.stack.append([tag, cls, ident, flags])
        if "skip" in flags:
            self.skip += 1
        if "boiler" in flags:
            self.boiler += 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def _img(self, a, cls):
        ctx = [c for fr in self.stack[-4:] for c in fr[1]]
        alt = (a.get("alt") or "").strip()
        ev = {"src": a.get("src", ""), "alt": alt, "title": (a.get("title") or "").strip(),
              "cls": cls, "ctx": ctx, "in_heading": self.heading is not None,
              "style_wh": _wh(a), "caption": []}
        if self.heading is not None and alt and not re.fullmatch(r"\[?illustration\]?", alt, re.I):
            self.heading[1].append(" " + alt + " ")   # a heading set as a picture: its alt is its text
        self.events.append((self.n, "img", ev))
        # a caption is text after the picture inside its own figure container
        for depth in range(len(self.stack) - 1, max(-1, len(self.stack) - 4), -1):
            fr = self.stack[depth]
            if fr[0] in ("div", "figure", "p", "span", "td") and any(FIG.search(c) for c in fr[1]) or fr[0] == "figure":
                self.capture = [depth, [], ev]
                break

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        # pop to the matching tag (HTML in the wild is not always well nested)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                while len(self.stack) > i:
                    fr = self.stack.pop()
                    if "skip" in fr[3]:
                        self.skip -= 1
                    if "boiler" in fr[3]:
                        self.boiler -= 1
                    if self.capture and len(self.stack) <= self.capture[0]:
                        cap = re.sub(r"\s+", " ", "".join(self.capture[1])).strip()
                        self.capture[2]["caption"] = cap
                        self.capture = None
                break
        if tag in HEADINGS and self.heading is not None:
            t = re.sub(r"\s+", " ", "".join(self.heading[1])).strip()
            self.events.append((self.heading[0], "heading", {"text": t, "end": self.n, "tag": tag}))
            self.heading = None
        if tag in BLOCKS:
            self._space()

    def handle_data(self, data):
        if self.skip:
            return
        if self.capture is not None:
            self.capture[1].append(data)
            return
        s = re.sub(r"\s+", " ", data)
        if self.heading is not None:
            self.heading[1].append(s)
        if s.strip() or (self.text and not self.text[-1].endswith(" ")):
            self._push_text(s)


def _wh(a):
    w, h = a.get("width"), a.get("height")
    st = a.get("style") or ""
    m = re.search(r"width:\s*(\d+)px", st)
    w = w or (m.group(1) if m else None)
    m = re.search(r"height:\s*(\d+)px", st)
    h = h or (m.group(1) if m else None)
    try:
        return [int(float(w)), int(float(h))] if w and h else None
    except ValueError:
        return None


# ----------------------------------------------------------------------------- pixels

def dhash(im):
    """64-bit difference hash: shrink to 9x8 grey, compare neighbours. Two copies of
    one printer's block hash within a few bits of each other whatever their size."""
    from PIL import Image
    g = im.convert("L").resize((9, 8), Image.LANCZOS)
    px = list(g.get_flattened_data() if hasattr(g, "get_flattened_data") else g.getdata())
    bits = 0
    for y in range(8):
        for x in range(8):
            bits = (bits << 1) | (px[y * 9 + x] > px[y * 9 + x + 1])
    return f"{bits:016x}"


def ham(a, b):
    return bin(int(a, 16) ^ int(b, 16)).count("1")


def image_facts(z, path):
    from PIL import Image
    try:
        data = z.read(path)
    except KeyError:
        return None
    facts = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
        facts["px"] = [im.width, im.height]
        if im.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            im = im.convert("RGBA")
            bg.paste(im, mask=im.split()[3])
            im = bg
        facts["dhash"] = dhash(im)
    except Exception:  # noqa: BLE001  (an SVG, a broken file: size and hash only)
        pass
    return facts


# ----------------------------------------------------------------------------- one book

def main_html(z):
    names = [n for n in z.namelist() if n.lower().endswith((".html", ".htm", ".xhtml"))]
    if not names:
        return None
    return max(names, key=lambda n: z.getinfo(n).file_size)


def harvest(slug, pg, title, year, zpath):
    z = zipfile.ZipFile(zpath)
    name = main_html(z)
    if not name:
        return None, "no HTML in the zip"
    raw = z.read(name).decode("utf-8", errors="replace")
    if re.search(r"COPYRIGHTED\s+Project\s+Gutenberg", raw[:20000], re.I):
        return None, "REFUSED: copyrighted Project Gutenberg ebook"
    base = os.path.dirname(name)
    w = Walk()
    w.feed(raw)
    w.close()
    text = "".join(w.text)

    events = [e for _, e in sorted(enumerate(w.events), key=lambda t: (t[1][0], t[0]))]
    heads = [(off, d) for off, k, d in events if k == "heading"]
    imgs = [(off, seq, d) for seq, (off, k, d) in enumerate(w.events) if k == "img"]
    srcs = {}
    for _, _, d in imgs:
        srcs[d["src"]] = srcs.get(d["src"], 0) + 1

    facts = {}
    for s in srcs:
        p = os.path.normpath(os.path.join(base, H.unescape(s))).replace("\\", "/")
        facts[s] = image_facts(z, p) or {}
    areas = sorted(f["px"][0] * f["px"][1] for f in facts.values() if f.get("px"))
    typical = areas[(3 * len(areas)) // 4] if areas else 1   # the book's larger pictures (75th percentile)

    def quote(off, n=70):
        return re.sub(r"\s+", " ", text[off:off + 160]).strip()[:n]

    def page_at(off):
        p = None
        for o, k, d in events:
            if o > off:
                break
            if k == "page":
                p = d
        return p

    def heading_before(off):
        t = None
        for o, d in heads:
            if d["end"] <= off:
                t = d["text"]
            else:
                break
        return t

    def next_heading_gap(off):
        for o, d in heads:
            if o >= off:
                return len(text[off:o].strip())
        return None

    def prev_heading_gap(off):
        g = None
        for o, d in heads:
            if d["end"] <= off:
                g = len(text[d["end"]:off].strip())
        return g

    rows, seen = [], {}
    cover_done = False
    # drop-cap spans: letter = text from the span's start to its first space
    for seq, (off, k, d) in enumerate(w.events):
        if k == "dropspan":
            word = re.match(r"\s*(\S+)", text[off:off + 40])
            letter = (word.group(1)[:1] if word else "")
            if not letter.isalpha():
                continue
            rows.append({"_off": (off, seq), "kind": "initial", "kind_by": f"class:{d['cls']}", "style": "type",
                         "letter": letter.upper(), "word": _word(text, off), "src": None})
    icons = 0
    for off, seq, d in imgs:
        src = d["src"]
        if NAV.search(src) or NAV_ALT.fullmatch(d["alt"] or ""):
            icons += 1          # Gutenberg's own buttons ("enlarge"), not the book's art
            continue
        seen[src] = seen.get(src, 0) + 1
        f = facts.get(src, {})
        px = f.get("px") or d["style_wh"]
        alt = d["alt"]
        r = {"_off": (off, seq), "src": src, "n_of_src": seen[src], "_inh": d["in_heading"]}
        nxt = text[off:off + 40]
        role = _role(" ".join(x for x in (alt, d["caption"] if isinstance(d["caption"], str) else "", d["title"]) if x))
        letter_alt = re.fullmatch(r"\[?([A-Za-z])\]?\.?", alt or "")
        is_drop_cls = any(DROP_CLASS.match(c) or re.search(r"drop|initial|dcap", c, re.I) for c in d["cls"] + d["ctx"])
        small = px and max(px) <= 260
        word = _word(text, off)
        if _le(next_heading_gap(off), 2):   # an initial set before the chapter's title opens the text after it
            for o, hd in heads:
                if o >= off:
                    word = _word(text, hd["end"])
                    break
        if letter_alt or (is_drop_cls and small) or (DROP_SRC.search(src) and small and nxt[:1].isalpha()):
            letter = letter_alt.group(1).upper() if letter_alt else (alt[:1].upper() if alt[:1].isalpha() else None)
            r.update(kind="initial", kind_by="alt-letter" if letter_alt else "class-or-name",
                     letter=letter, word=word, html_has_letter=_text_has(word, letter))
        elif (re.search(r"cover", src, re.I) or re.search(r"\bcover\b", alt, re.I)) and not cover_done:
            r.update(kind="cover", kind_by="name")
            cover_done = True
        elif px and max(px) <= 32:
            r.update(kind="glyph", kind_by="tiny")
        elif role and role[0] in ("headpiece", "tailpiece", "initial", "ornament", "vignette"):
            r.update(kind=role[0] if role[0] != "vignette" else "picture", kind_by=f"label:{role[1].lower()}")
            if role[0] == "initial":
                r.update(letter=None, word=word)
        elif srcs[src] >= 3:
            r.update(kind="ornament", kind_by=f"repeat:{srcs[src]}")
        elif px and px[0] >= 4 * px[1] and px[1] <= 160:
            r.update(kind="ornament", kind_by="band")
        elif px and px[0] * px[1] <= 0.2 * typical and _le(next_heading_gap(off), 2):
            r.update(kind="tailpiece", kind_by="small-before-heading")
        else:
            r.update(kind="picture", kind_by="default")
        if role and role[0] == "frontispiece":
            r["role"] = "frontispiece"
        r.update(alt=alt if alt and not JUNK_ALT.fullmatch(alt) else None,
                 caption=(d["caption"] if isinstance(d["caption"], str) else "") or None, title=d["title"] or None, px=px,
                 sha256=f.get("sha256", "")[:16] or None, dhash=f.get("dhash"))
        rows.append(r)

    rows.sort(key=lambda r: r["_off"])
    n_type = 0
    for i, r in enumerate(rows, 1):
        off = r.pop("_off")[0]
        ng, pgap = next_heading_gap(off), prev_heading_gap(off)
        if r["kind"] == "initial":
            place = "paragraph-start"
        elif r.pop("_inh", False):
            place = "in-heading"
        elif _le(ng, 2):
            place = "before-heading" if r["kind"] != "tailpiece" else "end-of-section"
        elif _le(pgap, 2):
            place = "after-heading"
        else:
            place = "in-text"
        if r.get("src"):
            cit = f"pg{pg}:{r['src']}#{r['n_of_src']}"
        else:
            n_type += 1
            cit = f"pg{pg}:type-initial#{n_type}"
        row = {"citation": cit, "book": slug, "pg": pg, "n": i, "kind": r["kind"], "kind_by": r["kind_by"],
               "printed_page": page_at(off), "heading": heading_before(off), "place": place,
               "before_quote": quote(off)}
        for k in ("role", "letter", "word", "html_has_letter", "style", "alt", "caption", "title", "px", "sha256", "dhash"):
            if r.get(k) is not None:
                row[k] = r[k]
        if r.get("src"):
            row["src"] = r["src"]
        rows[i - 1] = row

    # the title page and copyright lines; a transcriber's or scanner's note is not the edition
    front = [int(y) for line in re.split(r"(?<=[.;\n])\s+", text[:8000]) if not TRANSCRIBER.search(line)
             for y in re.findall(r"\b(1[5-9]\d\d)\b", line)]
    if year and year < 1931 and (not front or max(front) < 1931):
        rights = {"pd_us": True, "basis": f"edition of {year}, the shelf's date (US public domain: before 1931)"}
    elif not year and front and max(front) < 1931:
        rights = {"pd_us": True, "basis": f"latest year in the Gutenberg file's title page and copyright lines is "
                                          f"{max(front)} (US public domain: before 1931)"}
    else:
        rights = {"pd_us": "check", "basis": "no edition date before 1931 found (shelf: %s; front matter: %s); "
                                             "read the title page" % (year, max(front) if front else None)}
    for r in rows:
        r["pd_us"] = rights["pd_us"]
    summary = {"slug": slug, "pg": pg, "title": title, "year": year, "html": os.path.basename(name),
               "placements": len(rows), "images": len(seen), "icons_skipped": icons,
               "kinds": _count(r["kind"] for r in rows),
               "pages_known": sum(1 for r in rows if r["printed_page"]),
               "captions": sum(1 for r in rows if r.get("caption")), "rights": rights}
    return (rows, summary), "ok"


TRANSCRIBER = re.compile(r"produc|transcri|e-?text|e-?book|scann|digiti|gutenberg|isbn|proofread|"
                         r"html version|internet archive|google|online|release|updated|posted", re.I)
NAV = re.compile(r"(?:^|/)(?:enlarge|zoom|magnif\w*|icon\w*|arrow\w*|button\w*|spacer|blank|pixel|"
                 r"transparent|1x1)\.\w+$", re.I)
NAV_ALT = re.compile(r"\[?(?:enlarge|click to enlarge|larger image|full size)\]?", re.I)
JUNK_ALT = re.compile(r"\[?(?:illustration|image|picture|img|figure)\]?|(?:image|img|illus|fig|ill|i)[\W_]*\d+\w*", re.I)
ROLES = [("frontispiece", r"frontispiece"), ("headpiece", r"head[- ]?piece|chapter head(?:ing)? ornament|heading ornament"),
         ("tailpiece", r"tail[- ]?piece|end[- ]?piece|finis ornament"), ("initial", r"\b(?:drop[- ]?cap|initial letter|decorated initial|illuminated initial)\b"),
         ("ornament", r"\b(?:ornament|decoration|decorative|flourish|fleuron|border|divider|separator|vignette ornament)\b"),
         ("vignette", r"\bvignette\b")]


def _role(s):
    for role, pat in ROLES:
        m = re.search(pat, s or "", re.I)
        if m:
            return role, m.group(0)
    return None


def _le(v, n):
    return v is not None and v <= n


def _word(text, off):
    m = re.match(r"\s*([\w'’-]+)", text[off:off + 40])
    return m.group(1) if m else None


def _text_has(word, letter):
    """Does Gutenberg's HTML spell the opening word with the initial's letter? Often not: the
    letter lives in the picture, and the HTML reads "nce upon a time". Gutenberg's .txt, which
    the house text is built from, almost always has the whole word (checked 2026-11-03 on Jacobs's
    Indian Fairy Tales, Burgess's Paddy the Beaver and Kidnapped: 67 of 69). A rebuilt page must
    keep the letter in the text and draw the picture over it (ART-PLAN 3a)."""
    if not word or not letter:
        return None
    return word[:1].upper() == letter


def _count(it):
    c = {}
    for x in it:
        c[x] = c.get(x, 0) + 1
    return dict(sorted(c.items()))


# ----------------------------------------------------------------------------- across books

def _same_shape(a, b, tol=0.25):
    if not a.get("px") or not b.get("px"):
        return False
    ra, rb = a["px"][0] / a["px"][1], b["px"][0] / b["px"][1]
    return abs(ra / rb - 1) <= tol


def candidates(threshold=10):
    """Ornaments that may recur across books: dHash within `threshold` bits and the same shape
    (width:height within 25%), in 2+ books. CANDIDATES: about half survive a look by eye
    (2026-11-03: the Scribner Press colophon and Pyle's Arthur bands and tailpieces do; plain type
    letters of one face and unrelated triangles of the same layout do not)."""
    pool = []
    for fn in sorted(os.listdir(OUT)):
        if not fn.endswith(".jsonl") or fn.startswith("_"):
            continue
        seen = set()
        for line in open(os.path.join(OUT, fn), encoding="utf-8"):
            r = json.loads(line)
            if r["kind"] in ("ornament", "tailpiece", "headpiece", "initial") and r.get("dhash") and (r["book"], r["src"]) not in seen:
                seen.add((r["book"], r["src"]))
                if r["dhash"] in ("0000000000000000", "ffffffffffffffff"):
                    continue
                pool.append(r)
    groups, used = [], set()
    for i, a in enumerate(pool):
        if i in used:
            continue
        g = [a]
        for j in range(i + 1, len(pool)):
            if j not in used and ham(a["dhash"], pool[j]["dhash"]) <= threshold and _same_shape(a, pool[j]):
                g.append(pool[j])
                used.add(j)
        if len({r["book"] for r in g}) >= 2:
            groups.append(g)
    out = os.path.join(OUT, "_ornament-candidates.jsonl")
    with open(out + ".tmp", "w", encoding="utf-8") as f:
        for n, g in enumerate(sorted(groups, key=lambda g: -len(g)), 1):
            f.write(json.dumps({"group": n, "books": sorted({r["book"] for r in g}),
                                "members": [{"citation": r["citation"], "kind": r["kind"], "dhash": r["dhash"],
                                             "px": r.get("px"), "url": r.get("url")} for r in g]},
                               ensure_ascii=False) + "\n")
    os.replace(out + ".tmp", out)
    return len(groups)


# ----------------------------------------------------------------------------- main

def write_atomic(path, text):
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(path + ".tmp", path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("shelves", nargs="*")
    ap.add_argument("--fetch", action="store_true", help="download missing HTML zips first")
    ap.add_argument("--check", action="store_true", help="rebuild and compare, write nothing")
    ap.add_argument("--candidates", action="store_true", help="group ornaments recurring across books")
    ap.add_argument("--min", type=int, default=3, help="keep a book only with this many placements (default 3)")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    index_path = os.path.join(OUT, "_index.json")
    index = json.load(open(index_path, encoding="utf-8")) if os.path.exists(index_path) else {"books": {}, "skipped": {}}
    bad = 0
    for shelf in a.shelves:
        for slug, pg, title, year in shelf_books(shelf):
            zpath = os.path.join(CACHE, f"pg{pg}-h.zip")
            if not os.path.exists(zpath):
                if not a.fetch:
                    continue
                zpath, how = fetch(pg)
                print(f"  fetch {slug} (pg{pg}): {how}", flush=True)
                if not zpath:
                    index["skipped"][slug] = how
                    continue
                time.sleep(PAUSE)
            res, how = harvest(slug, pg, title, year, zpath)
            if not res:
                index["skipped"][slug] = how
                print(f"  {slug}: {how}")
                continue
            rows, summ = res
            dest = os.path.join(OUT, f"{slug}.jsonl")
            if summ["placements"] < a.min:
                index["skipped"][slug] = f"{summ['placements']} placements: not an illustrated edition"
                index["books"].pop(slug, None)
                if os.path.exists(dest) and not a.check:
                    os.remove(dest)
                continue
            body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
            summ["shelf"] = shelf
            if a.check:
                old = open(dest, encoding="utf-8").read() if os.path.exists(dest) else None
                if old != body:
                    bad += 1
                    print(f"  DIFFERS: {slug}")
                continue
            write_atomic(dest, body)
            index["books"][slug] = summ
            index["skipped"].pop(slug, None)
            print(f"  {slug}: {summ['placements']} placements {summ['kinds']}", flush=True)
    if not a.check and a.shelves:
        index["books"] = dict(sorted(index["books"].items()))
        index["skipped"] = dict(sorted(index["skipped"].items()))
        write_atomic(index_path, json.dumps(index, ensure_ascii=False, indent=1) + "\n")
    if a.candidates:
        print(f"ornament groups across books: {candidates()}")
    if a.check:
        print("check:", "byte-identical" if not bad else f"{bad} books differ")
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
