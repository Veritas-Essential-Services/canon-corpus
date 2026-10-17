#!/usr/bin/env python3
"""The Summa contra Gentiles, Latin and English, keyed by BOOK and CHAPTER.

    python3 pipeline/build_aquinas_scg.py --fetch   # the 1894 Latin OCR (one volume)
    python3 pipeline/build_aquinas_scg.py           # books + parallel file + key
    python3 pipeline/build_aquinas_scg.py --check   # key byte-identical

The key is the citation: SCG.1.13 = Contra Gentiles I, 13. Three witnesses:
  la        Corpus Thomisticum (the Leonine, 1918-30), paragraphs numbered as
            the Leonine numbers them (n. 1, 2 ...). Local only, as for the
            Summa (docs/AQUINAS.md, The Latin question).
  la1894    The editio Romana (Rome: Forzani, 1894), one volume, raw Internet
            Archive OCR: US public domain, so this is the Latin that can be
            shared. It numbers as the editions before the Leonine did (as
            Rickaby does), and is placed on the Leonine's chapters by its text.
  dominican The English Dominican Fathers' literal translation "from the latest
            Leonine edition" (Burns Oates, 1923-28): Books I, II, III. Raw
            Internet Archive OCR (pipeline/aquinas_shelf.json); Book IV (1929)
            was not found. US public domain.
  rickaby   Joseph Rickaby's annotated, ABRIDGED Of God and His Creatures
            (1905), clean from CCEL: all four books, many chapters shortened or
            left out. US public domain.
The committed key (data/aquinas/scg-key.jsonl) says per chapter which
witnesses have it and how many paragraphs each prints; it holds no text but
the English chapter titles.
"""
import hashlib, html, json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
CT = os.path.join(ROOT, "data", "corpus", "corpus-thomisticum")
SHELF = os.path.join(ROOT, "data", "corpus", "aquinas")
BOOKS = os.path.join(ROOT, "data", "books")
KEY_OUT = os.path.join(ROOT, "data", "aquinas", "scg-key.jsonl")
MANIFEST = os.path.join(BOOKS, "manifest.json")
DOMINICAN = [("aquinas-scg-dominican-b1", 1, 1), ("aquinas-scg-dominican-b2", 2, 1),
             ("aquinas-scg-dominican-b3p1", 3, 1), ("aquinas-scg-dominican-b3p2", 3, 84)]

def roman(s):
    if s.isdigit():
        return int(s)
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    s = s.upper()
    if not s or any(c not in vals for c in s):
        return None
    n = 0
    for i, c in enumerate(s):
        v = vals[c]
        n += -v if i + 1 < len(s) and vals[s[i + 1]] > v else v
    return n

def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()

def ref_of(key):
    _, b, c = key.split(".")
    return f"SCG {['', 'I', 'II', 'III', 'IV'][int(b)]}, {c}"

# ------------------------------------------------------------- Latin (CT)
RE_CT = re.compile(r'<(?:P|DIV)[^>]*TITLE="Contra Gentiles, lib\. (\d) cap\. (\d+)(?:-(\d+))?\s+(n\. (\d+)|tit\.)"[^>]*>(.*?)</(?:P|DIV)>', re.S)

def parse_la():
    ch = {}
    for f in sorted(x for x in os.listdir(CT) if re.fullmatch(r"scg\d+\.html", x)):
        s = open(os.path.join(CT, f), "rb").read().decode("latin-1")
        for m in RE_CT.finditer(s):
            b, c, c2, kind, n, inner = m.groups()
            inner = re.sub(r'^\s*<A NAME="\d+">\s*<SPAN CLASS="[a-z]+">.*?</SPAN>\s*</A>', "", inner, flags=re.S)
            key = f"SCG.{b}.{int(c)}"
            d = ch.setdefault(key, {"title": "", "paras": [], "covers": [int(c)] + ([int(c2)] if c2 else [])})
            if kind == "tit.":
                d["title"] = clean(inner)
            else:
                d["paras"].append(clean(inner))
    # the Leonine prints some pairs as one chapter under the first number
    # (I, 51-52; III, 95-96): a number missing after a chapter is covered by it
    for k in sorted(ch, key=keysort):
        b, c = k.split(".")[1], int(k.split(".")[2])
        nxt = max(ch[k]["covers"]) + 1
        if f"SCG.{b}.{nxt}" not in ch and any(f"SCG.{b}.{x}" in ch for x in range(nxt + 1, nxt + 3)):
            ch[k]["covers"].append(nxt)
    return ch

# ------------------------------------------- Latin, Rome 1894 (OCR, PD)
LA1894_ID = "summaecontragent00thom"
LA1894 = os.path.join(ROOT, "data", "corpus", "aquinas-1894", LA1894_ID + ".txt")
RE_CAPUT = re.compile(r"^C\s?A\s?P\s?U\s?T\s+([A-Za-z1l]+)\s*[.,:]?\s*$")
RE_RUNHEAD = re.compile(r"^(\d+\s+)?LIBER\s+\S+\s+\S{2,4}\.?\s+\S+(\s+\S{1,4})?$|^\d{1,4}$")

def fetch_1894():
    import urllib.request
    if os.path.exists(LA1894) and os.path.getsize(LA1894) > 1000000:
        return
    os.makedirs(os.path.dirname(LA1894), exist_ok=True)
    url = f"https://archive.org/download/{LA1894_ID}/{LA1894_ID}_djvu.txt"
    req = urllib.request.Request(url, headers={"User-Agent": "Canon-Corpus/0.1 (personal library research)"})
    data = urllib.request.urlopen(req, timeout=600).read()
    with open(LA1894 + ".tmp", "wb") as f:
        f.write(data)
    os.replace(LA1894 + ".tmp", LA1894)
    print(f"{LA1894_ID}: {len(data):,} bytes")

def parse_la1894(path):
    """The editio Romana of 1894 (Forzani), one volume, cut by its CAPUT
    headings and numbered as it numbers itself: the pre-Leonine numbering,
    the one Rickaby translates (its Book III has 164 chapters), placed on the
    Leonine's by `align_1894`. A numeral misread by the OCR ('vni', 'XVIL')
    is read from the sequence; a chapter whose heading the OCR lost runs into
    the one before, and is recorded."""
    lines = [re.sub(r"\s+", " ", l).strip() for l in open(path, encoding="utf-8", errors="replace")]
    end = next((i for i, l in enumerate(lines) if l.startswith("INDEX CAPITULORUM")), len(lines))
    ch, repairs, book, expect, cur, para, state = {}, [], 0, 1, None, [], None

    def flush():
        nonlocal para
        if cur is not None and para:
            t = ""
            for ln in para:
                t = t[:-1] + ln if re.search(r"[a-z]-$", t) and re.match(r"[a-z]", ln) else (t + " " + ln).strip()
            if state == "title":
                cur["title"] = (cur["title"] + " " + t).strip()
            else:
                cur["paras"].append(t)
        para = []

    for l in lines[:end]:
        m = RE_CAPUT.match(l)
        if m:
            w = m.group(1).upper()
            num = 1 if w.startswith("PRIM") else ocr_roman(w.replace("N", "II").replace("U", "II").rstrip("LR") or w)
            if num == 1 and expect > 3:
                book, expect = book + 1, 1
            elif book == 0:
                book = 1
            n = num if num in (expect, expect + 1, expect + 2) else expect
            flush()
            for lost in range(expect, n):
                repairs.append(f"{book}.{lost}: heading not found by OCR; its text is in the chapter before")
            cur = {"title": "", "paras": [], "own": n}
            ch[f"SCG.{book}.{n}"] = cur
            expect, state = n + 1, "title"
            continue
        if cur is None:
            continue
        if RE_RUNHEAD.match(l) or not l:
            flush()
            continue
        if state == "title" and not (capitals(l) or l.startswith("(")):
            flush()
            state = "body"
        para.append(l)
    flush()
    for k, d in ch.items():
        out = []
        for p in d["paras"]:
            if out and re.match(r"[a-z,;:(]", p):
                out[-1] += " " + p
            else:
                out.append(p)
        d["paras"] = out
    return ch, repairs

# ------------------------------------------------- English Dominican (OCR)
RE_HEAD_ODD = re.compile(r"^CHAPTER\s+[IVXLC]+\.?\s+\S{1,4}$")
RE_HEAD_EVEN = re.compile(r"^(\d+\s+)?THE\s+SUMMA\s+CONTRA\s+GENTILES(\s+\S{1,4})?$", re.I)
RE_CHAP = re.compile(r"^CHAPTERS?\s+(.+?)\.?$")

def ocr_roman(tok):
    """CHAPTER numerals as the OCR reads them: 'n' and 'H' for II, 'in' for
    III, 'XL VII' with a space, 'l' or '1' for I."""
    t = tok.replace(" ", "").replace("n", "II").replace("H", "II").replace("l", "I").replace("1", "I").replace("i", "I")
    return roman(t)

def chapter_heading(line, nxt):
    """(first, last) chapter numbers if `line` is a chapter heading, else None.
    A running head carries the page number after the numeral; a heading
    doesn't, and is followed by the title in capitals."""
    m = RE_CHAP.match(line)
    if not m:
        return None
    toks = m.group(1).split()
    if toks and re.fullmatch(r"\d+|[a-z]{1,3}\d*|\S*\d\S*", toks[-1]) and len(toks) > 1 and not re.search(r"\bAND\b", m.group(1), re.I):
        if re.fullmatch(r"\d+", toks[-1]) or ocr_roman(" ".join(toks[:-1])):
            return None
    parts = re.split(r"\s+AND\s+", m.group(1), flags=re.I)
    if len(parts) > 1 and len(parts[-1].split()) > 1:     # "CHAPTERS VIII AND IX 19": a running head
        return None
    nums = [ocr_roman(x) for x in parts]
    # a heading is followed by its title in capitals; a running head by the
    # page's text, or by a bare page number
    return (nums[0], nums[-1], capitals(nxt))
def capitals(line):
    """Mostly capitals (the OCR sometimes lower-cases a word of a title)."""
    letters = re.findall(r"[A-Za-z]", line)
    return len(letters) >= 3 and sum(c.isupper() for c in letters) >= 0.6 * len(letters)

RE_FOOT = re.compile(r"^[1-9*]\s+\S.{0,60}$")

RE_TOC = re.compile(r"(?:-\s+){2}|-\s+[\dIl]{1,3}\s*$|\s[\dIl]{1,3}\s+[IVXLC]+[.,]\s")

def parse_dominican(path, book, first):
    lines = [re.sub(r"\s+", " ", l).strip() for l in open(path, encoding="utf-8", errors="replace")]
    ch, cur, cur_n, expect, para, state = {}, None, None, first, [], None

    def flush():
        nonlocal para
        if cur is not None and para:
            t = " ".join(para)
            t = re.sub(r"(\w)- (\w)", r"\1\2", t)
            if state == "title":
                cur["title"] = (cur["title"] + " " + t).strip()
            else:
                cur["paras"].append(t)
        para = []

    for i, l in enumerate(lines):
        nxt = next((x for x in lines[i + 1:i + 4] if x), "")
        h = chapter_heading(l, nxt)
        if h and h[2] and (h[0] in (expect, expect + 1) or h[0] is None):
            flush()
            n = h[0] or expect
            if n != expect:
                ch.setdefault("_repairs", []).append(f"chapter {expect} heading not found; text runs into {n}")
            cur, cur_n = {"title": "", "paras": []}, n
            ch[f"SCG.{book}.{n}"] = cur
            last = h[1] if h[1] and h[1] > n else n
            if last > n:                     # "CHAPTERS XXVIII AND XXIX": one heading, two chapters
                cur["covers"] = list(range(n, last + 1))
            expect, state = last + 1, "title"
            continue
        if cur is None:
            continue
        if RE_HEAD_ODD.match(l) or RE_HEAD_EVEN.match(l) or re.fullmatch(r"\d{1,3}|\W{1,3}", l):
            flush()          # a page break ends the line group; the paragraph rejoins below
            continue
        if RE_FOOT.match(l) and (i + 1 >= len(lines) or not lines[i + 1]):
            continue
        if not l:
            flush()
            continue
        if state == "title" and RE_TOC.search(l):
            # a table of contents (leaders, page numbers, the next numeral):
            # not the chapter; the text proper starts at a later heading
            del ch[f"SCG.{book}.{cur_n}"]
            cur, para, expect = None, [], cur_n
            ch.pop("_repairs", None)
            continue
        if state == "title" and not capitals(l):
            flush()
            state = "body"
        para.append(l)
    flush()
    # a paragraph broken by a page (it starts lower-case) is rejoined
    for k, d in ch.items():
        if k.startswith("_"):
            continue
        out = []
        for p in d["paras"]:
            if out and re.match(r"[a-z,;:(]", p):
                out[-1] += " " + p
            else:
                out.append(p)
        d["paras"] = out
    return ch

# ------------------------------------------------------- Rickaby (CCEL)
def parse_rickaby(path):
    raw = open(path, encoding="utf-8").read()
    found, book = [], None
    divs = list(re.finditer(r'<div([12])\b([^>]*)>', raw))
    for i, m in enumerate(divs):
        at = dict(re.findall(r'(\w+)="([^"]*)"', m.group(2)))
        t = at.get("title", "")
        seg = raw[m.end(): divs[i + 1].start() if i + 1 < len(divs) else len(raw)]
        if m.group(1) == "1":
            mb = re.match(r"Book (I|II|III|IV)\b", t)
            book = roman(mb.group(1)) if mb else None
            continue
        t = re.sub(r"^Chapter\s+(?=Chapter)", "", t)            # "Chapter Chapter XCVIII"
        mc = re.match(r"Chapt?e?rs? ([IVXLC]+|\d+)((?:\s*(?:,|and|&amp;|-|\u2013)\s*[IVXLC]+)*)\.?\s*(.*)", t)
        if not book or not mc:
            continue
        paras = [clean(p) for p in re.findall(r"<p\b[^>]*>(.*?)</p>", seg, re.S)]
        found.append((book, roman(mc.group(1)), mc.group(2), clean(mc.group(3)), [p for p in paras if p]))
    ch, last = {}, {}
    for i, (book, n, rest, title, paras) in enumerate(found):
        prev = last.get(book, 0)
        nxt = found[i + 1][1] if i + 1 < len(found) and found[i + 1][0] == book else None
        # a misprinted numeral: "CXVI" between XCV and XCVII, a number used
        # twice. He does reorder a few chapters (IV, 54-55 before 50), so a
        # number lower than the last is kept while it is still unused.
        if n is None or (nxt and prev < nxt < n and n > prev + 10) or f"SCG.{book}.{n}" in ch:
            n = prev + 1
        # "Chapter XXXII, XXXV": the arguments (32) and, joined to them, their
        # solution (35), so a list, not a range; "XLI-XLV" is a range
        covers = [n]
        for sep, x in re.findall(r"(,|and|&amp;|-|\u2013)\s*([IVXLC]+)", rest):
            v = roman(x)
            if v and v > covers[-1]:
                covers += list(range(covers[-1] + 1, v + 1)) if sep in "-\u2013" else [v]
        last[book] = max(prev, n)
        ch[f"SCG.{book}.{n}"] = {"title": title, "paras": paras, "own": n, "own_covers": covers}
    return ch

STOP = set("that which there from with this have does doth their them they what when into upon such shall".split())

def twords(t):
    return {w.rstrip("s") for w in re.findall(r"[a-z]{4,}", t.lower()) if w not in STOP}

def align(rs, slots, score, W=12, join=0.15):
    """Monotonic alignment of chapters `rs` (each with its own number `own`)
    onto `slots` [(number, payload)]: each chapter goes to a slot at or after
    the one before, within W of its own number; two may share a slot (`join`
    is the cost), and a step in the own numbers should be the same step in
    the slots. Returns {slot index: [chapters]}."""
    m, S, NEG = len(rs), len(slots), -1e9
    if not m or not S:
        return {}
    best = [[NEG] * S for _ in range(m)]
    back = [[None] * S for _ in range(m)]
    for i, r in enumerate(rs):
        for j in range(S):
            if abs(slots[j][0] - r["own"]) > W:
                continue
            if i == 0:
                best[i][j] = score(r, j)
                continue
            v, a = NEG, None
            for j0 in range(max(0, j - W), j + 1):
                if best[i - 1][j0] > NEG / 2:
                    d = abs((r["own"] - rs[i - 1]["own"]) - (slots[j][0] - slots[j0][0]))
                    c = best[i - 1][j0] - 0.1 * min(3, d) - (join if j0 == j else 0.0)
                    if c > v:
                        v, a = c, j0
            if a is not None:
                best[i][j], back[i][j] = v + score(r, j), a
    j = max(range(S), key=lambda x: best[m - 1][x])
    placed = {}
    for i in range(m - 1, -1, -1):
        placed.setdefault(j, []).insert(0, rs[i])
        j = back[i][j]
    return placed

def joined(group):
    return {"title": " / ".join(g["title"] for g in group), "own": group[0]["own"],
            "paras": [p for g in group for p in g["paras"]],
            "own_covers": sorted({c for g in group for c in g.get("own_covers", [g["own"]])})}

STOP_LA = set("quod esse enim autem etiam igitur sicut quae quia sunt sint ergo omnis omne aliquid "
              "aliquod unde secundum ipsum ipsa ipse eius ejus huius hujus quam quidem praeterea item potest".split())

def lwords(t):
    import aquinas_st_1894 as o
    return {x for x in o.words(t) if x not in STOP_LA}

def align_1894(old, la):
    """The 1894 chapters onto the Leonine's, by their Latin: the opening of
    each old chapter against every three-paragraph window of a Leonine
    chapter (so the second half of a joint chapter is found), Dice of the
    words. Returns ({leonine key: chapter}, {(book, old number): leonine key})."""
    out, where = {}, {}
    for book in (1, 2, 3, 4):
        rs = sorted([v for k, v in old.items() if k.split(".")[1] == str(book)], key=lambda v: v["own"])
        keys = sorted((int(k.split(".")[2]), k) for k in la if k.split(".")[1] == str(book))
        slots = [(n, [lwords(" ".join(la[k]["paras"][i:i + 3])) for i in range(max(1, len(la[k]["paras"]) - 2))])
                 for n, k in keys]
        heads = {id(r): lwords(" ".join(r["paras"][:3])) for r in rs}
        def score(r, j):
            A = heads[id(r)]
            if not A:
                return 0.0
            return max((2 * len(A & B) / (len(A) + len(B)) for B in slots[j][1] if B), default=0.0)
        placed = align(rs, slots, score, W=8)
        for j, group in placed.items():
            k = f"SCG.{book}.{slots[j][0]}"
            out[k] = joined(group)
            out[k]["fit"] = round(min(score(g, j) for g in group), 2)
            for g in group:
                where[(book, g["own"])] = k
    return out, where

def align_rickaby(ric, dom, where):
    """Rickaby translates the pre-Leonine numbering (his Book III runs to 164;
    the Leonine's to 163): the 1894 edition's. His chapter goes where the 1894
    chapter of his number was placed on the Leonine (`where`, from the Latin).
    Where the 1894 OCR lost that heading, his title is aligned with the
    English Dominican titles instead (Books I-III); failing both, his own
    number stands. Two of his chapters may fall in one Leonine chapter (his
    III, 96 "That God does not hear all Prayers" is the second half of the
    Leonine's joint III, 95-96), and are then joined. Returns {leonine key:
    chapter}, with `own_covers` kept on each, and the count of chapters
    placed by each route."""
    by_title, routes = {}, Counter()
    for book in (1, 2, 3):
        rs = sorted([v for k, v in ric.items() if k.split(".")[1] == str(book)], key=lambda v: v["own"])
        slots = sorted((int(k.split(".")[2]), d["title"]) for k, d in dom.items() if k.split(".")[1] == str(book))
        if not rs or not slots:
            continue
        def score(r, j):
            a, b = twords(r["title"]), twords(slots[j][1])
            return 2 * len(a & b) / (len(a) + len(b)) if a and b else 0.0   # Dice: a short title does not win by being short
        for j, group in align(rs, slots, score).items():
            for r in group:
                by_title[id(r)] = f"SCG.{book}.{slots[j][0]}"
    groups = {}
    for k0, r in sorted(ric.items(), key=lambda kv: keysort(kv[0])):
        book = int(k0.split(".")[1])
        if (book, r["own"]) in where:
            k, route = where[(book, r["own"])], "latin"
        elif id(r) in by_title:
            k, route = by_title[id(r)], "title"
        else:
            k, route = k0, "own"
        routes[route] += 1
        groups.setdefault(k, []).append(r)
    return {k: joined(g) for k, g in groups.items()}, routes

# -------------------------------------------------------------- build
def keysort(k):
    _, b, c = k.split(".")
    return (int(b), int(c))

def build(check=False):
    la = parse_la()
    dom, repairs = {}, {}
    for slug, book, first in DOMINICAN:
        d = parse_dominican(os.path.join(SHELF, slug + ".txt"), book, first)
        repairs[slug] = d.pop("_repairs", [])
        dom.update(d)
    old, repairs["la1894"] = parse_la1894(LA1894)
    o94, where = align_1894(old, la)
    ric, routes = align_rickaby(parse_rickaby(os.path.join(SHELF, "aquinas-gentiles-rickaby.xml")), dom, where)
    covered = {f"SCG.{k.split('.')[1]}.{c}": k for k, v in la.items() for c in v["covers"][1:]}
    # Rickaby joins a chapter of arguments to the later chapter that answers
    # them ("Chapters XXXII, XXXV"): the answering chapter is read in his
    ric_in = {}
    for k, v in ric.items():
        b, n = k.split(".")[1], int(k.split(".")[2])
        cs = v["own_covers"]
        for prev, c in zip(cs, cs[1:]):
            if c != prev + 1:
                ric_in[f"SCG.{b}.{c + n - v['own']}"] = k
    rows = []
    for k in sorted(set(la) | set(dom) | set(ric) | set(ric_in) | set(o94), key=keysort):
        r = {"key": k, "ref": ref_of(k)}
        if k in la:
            r["la_paras"] = len(la[k]["paras"])
            if len(la[k]["covers"]) > 1:
                r["la_covers"] = la[k]["covers"]
        elif k in covered:
            r["la_in"] = covered[k]
        if k in dom:
            r["dominican_paras"] = len(dom[k]["paras"])
            t = re.sub(r"^(CHAPTERS?\s+[IVXLCn]+[.,]?\s*|[IVXLC]+\.\s+)", "", dom[k]["title"]).strip(" |")
            r["title_en"] = t.capitalize() if t.isupper() else t
        if k in ric:
            r["rickaby_paras"] = len(ric[k]["paras"])
            r["title_rickaby"] = ric[k]["title"]
            if ric[k]["own_covers"] != [int(k.split(".")[2])]:
                r["rickaby_numbered"] = ric[k]["own_covers"]
        elif k in ric_in:
            r["rickaby_in"] = ric_in[k]
        if k in o94:
            r["la1894_paras"] = len(o94[k]["paras"])
            r["la1894_fit"] = o94[k]["fit"]
            if o94[k]["own_covers"] != [int(k.split(".")[2])]:
                r["la1894_numbered"] = o94[k]["own_covers"]
        has = [w for w, d in (("la", la), ("la1894", o94), ("dominican", dom), ("rickaby", ric))
               if k in d or (w == "la" and k in covered) or (w == "rickaby" and k in ric_in)]
        r["witnesses"] = has
        if "la" in has and "dominican" in has and k in la:
            r["paras_match"] = r["la_paras"] == r["dominican_paras"]
        rows.append(r)
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    if check:
        ok = open(KEY_OUT, encoding="utf-8").read() == text
        print("check ok" if ok else "CHECK FAILED: data/aquinas/scg-key.jsonl differs from a rebuild")
        return 0 if ok else 1
    os.makedirs(os.path.dirname(KEY_OUT), exist_ok=True)
    with open(KEY_OUT + ".tmp", "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(KEY_OUT + ".tmp", KEY_OUT)

    def book(slug, title, author, ch):
        units = []
        for k in sorted(ch, key=keysort):
            units.append({"id": f"{slug}:{k[4:]}", "key": k, "ref": ref_of(k), "text": ch[k]["title"], "links": [], "part": "title"})
            for j, p in enumerate(ch[k]["paras"], 1):
                units.append({"id": f"{slug}:{k[4:]}.{j}", "key": f"{k}.{j}", "ref": f"{ref_of(k)}, par. {j}", "text": p, "links": []})
        b = {"slug": slug, "title": title, "author": author, "units": units}
        with open(os.path.join(BOOKS, slug + ".json.tmp"), "w", encoding="utf-8") as f:
            json.dump(b, f, ensure_ascii=False)
        os.replace(os.path.join(BOOKS, slug + ".json.tmp"), os.path.join(BOOKS, slug + ".json"))
        return b
    bl = book("aquinas-scg-la", "Summa contra Gentiles (Latin, Leonine text via Corpus Thomisticum)", "Thomas Aquinas", la)
    bo = book("aquinas-scg-la1894", "Summa contra Gentiles (Latin, editio Romana 1894); raw OCR", "Thomas Aquinas", o94)
    bd = book("aquinas-scg-en-dominican", "The Summa contra Gentiles, Books I-III (English Dominican Fathers, 1923-28); raw OCR",
              "Thomas Aquinas (tr. English Dominican Fathers)", dom)
    br = book("aquinas-scg-en-rickaby", "Of God and His Creatures (Contra Gentiles, abridged and annotated, 1905)",
              "Thomas Aquinas (tr. Joseph Rickaby)", ric)
    par = [{"key": r["key"], "ref": r["ref"],
            "la": la.get(r["key"]), "la1894": o94.get(r["key"]), "dominican": dom.get(r["key"]),
            "rickaby": ric.get(r["key"])} for r in rows]
    with open(os.path.join(BOOKS, "aquinas-scg.parallel.json.tmp"), "w", encoding="utf-8") as f:
        json.dump(par, f, ensure_ascii=False)
    os.replace(os.path.join(BOOKS, "aquinas-scg.parallel.json.tmp"), os.path.join(BOOKS, "aquinas-scg.parallel.json"))
    manifest(rows, bl, bo, bd, br, repairs, routes)
    c = Counter(tuple(r["witnesses"]) for r in rows)
    print(f"{len(rows)} chapters: {dict(c)}; paragraph counts equal (la vs dominican): "
          f"{sum(1 for r in rows if r.get('paras_match'))}/{sum(1 for r in rows if 'paras_match' in r)}")
    for s, rep in repairs.items():
        if rep:
            print(" ", s, rep[:3])
    return 0

def sha_files(paths):
    h = hashlib.sha256()
    for p in paths:
        h.update(open(p, "rb").read())
    return h.hexdigest()

def manifest(rows, bl, bo, bd, br, repairs, routes):
    m = json.load(open(MANIFEST, encoding="utf-8"))
    sch = {"citation": "book and chapter (SCG.1.13 = Contra Gentiles I, 13); paragraphs numbered within the chapter",
           "resolution": "chapter (paragraph within it)", "key_file": "data/aquinas/scg-key.jsonl"}
    n = lambda w: sum(1 for r in rows if w in r["witnesses"])
    m["aquinas-scg-la"] = {"title": bl["title"], "author": bl["author"], "format": "corpus-thomisticum-html",
        "sha256": sha_files([os.path.join(CT, f) for f in sorted(os.listdir(CT)) if f.startswith("scg")]),
        "units": len(bl["units"]),
        "scheme": {**sch, "honesty": "exact: the Leonine's own chapter and paragraph numbers"},
        "source": "https://www.corpusthomisticum.org/iopera.html (Leonine edition, Rome 1918-1930)",
        "rights": {"license": "underlying text public domain; electronic edition claimed by the publisher",
                   "publisher_notice": "(c) Fundacion Tomas de Aquino quoad hanc editionem. Iura omnia asservantur",
                   "redistribute_whole": False, "pending": "Adam's ruling: docs/AQUINAS.md, The Latin question"},
        "builder": "pipeline/build_aquinas_scg.py", "note": f"{n('la')} chapters."}
    m["aquinas-scg-la1894"] = {"title": bo["title"], "author": bo["author"], "format": "ia-djvu-ocr",
        "sha256": sha_files([LA1894]), "units": len(bo["units"]),
        "scheme": {**sch, "honesty": "chapter placed on the Leonine number by its Latin (the opening of each chapter against the Leonine's text: la1894_fit in the key); its own pre-Leonine numbers kept as la1894_numbered where they differ; unproofread OCR, a pre-Leonine text; paragraphs are the OCR's"},
        "source": f"https://archive.org/details/{LA1894_ID}",
        "rights": {"license": "public-domain", "basis": "Rome: Forzani, 1894; US public domain", "redistribute_whole": True},
        "builder": "pipeline/build_aquinas_scg.py",
        "note": f"{n('la1894')} chapters; {len(repairs['la1894'])} headings lost by the OCR, their text in the chapter before (repairs, by its own numbers).",
        "repairs": repairs["la1894"]}
    m["aquinas-scg-en-dominican"] = {"title": bd["title"], "author": bd["author"], "format": "ia-djvu-ocr",
        "sha256": sha_files([os.path.join(SHELF, s + ".txt") for s, _, _ in DOMINICAN]),
        "units": len(bd["units"]),
        "scheme": {**sch, "honesty": "chapter-exact (headings checked in sequence); paragraphs are the OCR's, unproofread, and do not always match the Leonine's numbering (paras_match in the key file); some page footnotes may survive in the text"},
        "source": "pipeline/aquinas_shelf.json (Internet Archive: " + ", ".join(s for s, _, _ in DOMINICAN) + ")",
        "rights": {"license": "public-domain", "basis": "London: Burns Oates & Washbourne, 1923-1928; US public domain", "redistribute_whole": True},
        "builder": "pipeline/build_aquinas_scg.py",
        "note": f"Books I-III, {n('dominican')} chapters. Book IV (1929) not found on the Archive.",
        "repairs": [f"{s}: {x}" for s, _, _ in DOMINICAN for x in repairs[s]]}
    m["aquinas-scg-en-rickaby"] = {"title": br["title"], "author": br["author"], "format": "thml",
        "sha256": sha_files([os.path.join(SHELF, "aquinas-gentiles-rickaby.xml")]),
        "units": len(br["units"]),
        "scheme": {**sch, "honesty": "he numbers as the 1894 Latin does (pre-Leonine); each chapter is placed on the Leonine number through the 1894 chapter of the same number, or, where the 1894 OCR lost that heading, by his title against the Dominican's; his own numbers kept as rickaby_numbered; ABRIDGED: chapters shortened, joined or left out, and his notes are mixed into the text"},
        "source": "https://ccel.org/ccel/a/aquinas/gentiles.xml",
        "rights": {"license": "public-domain", "basis": "London: Burns & Oates, 1905; US public domain", "redistribute_whole": True,
                   "ccel_terms": "CCEL asks non-commercial use of some prepared editions: check before republishing"},
        "builder": "pipeline/build_aquinas_scg.py", "note": f"{n('rickaby')} chapters across all four books; placed by the Latin {routes['latin']}, by title {routes['title']}, by his own number {routes['own']}."}
    with open(MANIFEST + ".tmp", "w", encoding="utf-8") as f:
        f.write(json.dumps(m, ensure_ascii=False, indent=1) + "\n")
    os.replace(MANIFEST + ".tmp", MANIFEST)

if __name__ == "__main__":
    if "--fetch" in sys.argv:
        fetch_1894()
        sys.exit(0)
    sys.exit(build("--check" in sys.argv))
