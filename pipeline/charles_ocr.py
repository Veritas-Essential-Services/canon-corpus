#!/usr/bin/env python3
"""
charles_ocr.py -- read R. H. Charles's *Apocrypha and Pseudepigrapha of the
Old Testament* (Oxford, 1913) out of the Internet Archive's OCR of the scans.

There is no machine-readable edition, so the text comes from the scans' own
OCR (hOCR: every word with its box on the page). This module reads that
layout. It is the parser only; pipeline/build_charles.py decides the books,
the ids and the manifest. Nothing here edits the OCR (rule 2): every fix is a
rule that reruns on refetch.

THE PAGE. A text page of Charles has a running head ("THE BOOK OF TOBIT 5.
10-15", the chapter and verse range the page carries); the translation in
the larger type; and, under it, the notes and the critical apparatus in
smaller type. Verse numbers stand in the LEFT MARGIN of the line on which a
verse begins, not in front of the verse's first word. Chapter numbers are
bold numerals further out in the margin.

  split_body()    body vs notes: the split that best separates large type
                  above from small type below (tesseract's x_size), moved
                  up past any block of critical apparatus
  columns()       one column, or two with a gutter (I Esdras prints 1 Esdras
                  beside its canonical parallel; only the left is Esdras)
  margin_tokens() the text edge of a column and the words left of it
  decode()        a Viterbi pass over the margin numerals. The OCR misreads
                  old-style figures (a 3 for an 8, "δι" for 51), drops some
                  and invents others, so a number is evidence, not a fact.
                  The state is (part, chapter, verse); the costs prefer
                  verse+1, take a number read cleanly, allow a dropped
                  marker or a chapter break, and are steered by the page's
                  running head (itself OCR, so a head that disagrees with
                  its neighbours is discarded).
  verse_start()   where in its first line a verse begins: the line start if
                  the previous verse ended a sentence there, else the first
                  sentence break in the line, else the line start (flagged).
"""
import collections
import gzip
import html
import json
import re
import statistics as st

# ------------------------------------------------------------------ hOCR

LINE = re.compile(r'<span class="(ocr_line|ocr_caption|ocr_header|ocr_textfloat)" id="[^"]+" '
                  r'title="bbox (\d+) (\d+) (\d+) (\d+);[^"]*?x_size ([\d.]+)[^"]*">')
WORD = re.compile(r'<span class="ocrx_word"[^>]*title="bbox (\d+) (\d+) (\d+) (\d+); '
                  r'x_wconf (\d+)[^"]*"[^>]*>(.*?)</span>', re.S)


def read_hocr(path):
    """[{w, h, lines: [{bbox, xs, words: [(x0, y0, x1, y1, conf, text)], text}]}], one per leaf."""
    with open(path, encoding="utf-8") as f:
        s = f.read()
    out = []
    for p in s.split('<div class="ocr_page"')[1:]:
        ms = list(LINE.finditer(p))
        lines = []
        for i, m in enumerate(ms):
            seg = p[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(p)]
            words = [(int(w.group(1)), int(w.group(2)), int(w.group(3)), int(w.group(4)),
                      int(w.group(5)), html.unescape(re.sub('<[^>]+>', '', w.group(6))))
                     for w in WORD.finditer(seg)]
            lines.append({"bbox": tuple(map(int, m.group(2, 3, 4, 5))), "xs": float(m.group(6)),
                          "words": words, "text": " ".join(w[5] for w in words)})
        bb = re.search(r'bbox 0 0 (\d+) (\d+)', p)
        out.append({"w": int(bb.group(1)), "h": int(bb.group(2)), "lines": lines})
    return out


def save_pages(pages, path):
    with gzip.open(path + ".tmp", "wt", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False)
    import os
    os.replace(path + ".tmp", path)


def load_pages(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        pages = json.load(f)
    for p in pages:
        for l in p["lines"]:
            l["bbox"] = tuple(l["bbox"])
            l["words"] = [tuple(w) for w in l["words"]]
    return pages

# ------------------------------------------------------------------ numbers

DIG = str.maketrans({'I': '1', 'l': '1', 'i': '1', '|': '1', 'O': '0', 'o': '0', 'ο': '0',
                     'Ο': '0', 'S': '5', 's': '5', 'ς': '5', 'g': '9', 'Z': '2', 'z': '2',
                     'B': '8', 'Β': '8', 'Ι': '1', 'T': '7', 'τ': '7', 'b': '6', 'G': '6',
                     't': '1'})


def num(tok, strict=False):
    """An OCR token as a number: digits as read, or (short tokens only) with
    the usual letter-for-digit confusions undone."""
    t = tok.strip('.,:;’‘\'"_—-()[]{}*')
    if not t:
        return None
    if t.isdigit():
        return int(t)
    if strict or len(t) > 3:
        return None
    u = t.translate(DIG)
    return int(u) if u.isdigit() else None


def digits(t):
    return t.strip('.,:;’‘\'"_—*')


def numlike(t):
    if num(t) is not None:
        return True
    return 0 < len(t) <= 3 and '-' not in t and all(c in '0123456789IlOoSsgZBτδσιςοϑὃΟΙ' for c in t)


def fuzzy_eq(x, s):
    """The cost of reading the OCR string s as the number x."""
    if s == str(x):
        return 0.0
    if num(s) == x:
        return 0.4
    t = s.translate(DIG)
    if t.isdigit() and len(t) == len(str(x)) and sum(a != b for a, b in zip(t, str(x))) == 1:
        return 0.7
    return 1.0


# old-style figures the OCR confuses in the running heads
SWAP = {'3': '38', '8': '83', '1': '17', '7': '71', '5': '56', '6': '65', '0': '09', '9': '90'}


def alts(n):
    out = {''}
    for d in str(n):
        out = {o + x for o in out for x in SWAP.get(d, d)}
    return {int(o) for o in out}

# ------------------------------------------------------------------ the page

APP = re.compile(r'(^|\s)[a-z]{1,2}-[a-z]{1,2}(\s|$)|\s>\s?|Lit\.|Reading|\bLuc\b|Syro-Hex|\bcrit\.')


def is_app(l):
    """A line of critical apparatus (sigla, 'Lit.', '>' for 'omits')."""
    return st.mean(w[4] for w in l["words"]) < 80 or bool(APP.search(l["text"]))


def is_apparatus_text(text):
    """A line of notes or apparatus that the type-size split let into the body:
    Greek (or Hebrew the OCR read as Greek) makes up a third of its letters, or
    it is thick with sigla ('] > |'). Charles's English never is (Tob 1.18)."""
    letters = [c for c in text if c.isalpha()]
    if len(letters) >= 8 and sum(not ('a' <= c.lower() <= 'z') for c in letters) >= 0.3 * len(letters):
        return True
    return sum(text.count(c) for c in ']>|') >= 3


def split_body(p, T, head_frac=0.065):
    """(head lines, body lines, note lines). T is the x_size between the two
    type sizes, measured per volume."""
    L = [l for l in p["lines"] if l["words"] and l["text"].strip()]
    H = p["h"]
    head = [l for l in L if l["bbox"][3] < H * head_frac]
    rest = sorted([l for l in L if l["bbox"][3] >= H * head_frac
                   and not (l["bbox"][1] > H * 0.92 and len(l["words"]) <= 2)],
                  key=lambda l: l["bbox"][1])
    rest = [l for l in rest if not (l["bbox"][2] < p["w"] * 0.04 or l["bbox"][0] > p["w"] * 0.97)]
    if not rest:
        return head, [], []
    w = [(1 if l["xs"] >= T else -1) * min(len(l["words"]), 6) for l in rest]
    pref = [0]
    for b in w:
        pref.append(pref[-1] + b)
    tot = pref[-1]
    k = max(range(len(rest) + 1), key=lambda k: (pref[k] - (tot - pref[k]), k))
    pitch = st.median([b["bbox"][1] - a["bbox"][1] for a, b in zip(rest, rest[1:])] or [50])
    for j in range(k - 1, 0, -1):
        if rest[j]["bbox"][1] - rest[j - 1]["bbox"][3] > 0.9 * pitch:
            block = rest[j:k]
            if block and sum(is_app(l) for l in block) >= 0.6 * len(block):
                k = j
            break
    while k > 0 and APP.search(rest[k - 1]["text"]) and st.mean(x[4] for x in rest[k - 1]["words"]) < 85:
        k -= 1
    return head, rest[:k], rest[k:]


def split_at_gutter(lines, W):
    """The OCR sometimes reads straight across a two-column page, joining a
    left-column line to its right-hand neighbour ('... the four- | Jerusalem:
    and they killed ...', 1 Esd 1.1). Cut such a line where a wide gap, or a
    printed column rule '|', falls in the middle of the page."""
    out = []
    for l in lines:
        ws = l["words"]
        cut = None
        for i in range(1, len(ws)):
            a, b = ws[i - 1], ws[i]
            mid = (a[2] + b[0]) / 2
            if not (0.4 * W < mid < 0.6 * W):
                continue
            if b[0] - a[2] > 1.2 * l["xs"] or b[5] in ("|", "||") or a[5] in ("|", "||"):
                cut = i
                break
        if cut is None:
            out.append(l)
            continue
        left = [w for w in ws[:cut] if w[5] not in ("|", "||")]
        right = [w for w in ws[cut:] if w[5] not in ("|", "||")]
        for part in (left, right):
            if part:
                out.append(dict(l, words=part, text=" ".join(w[5] for w in part),
                                bbox=(part[0][0], min(w[1] for w in part), part[-1][2],
                                      max(w[3] for w in part))))
    return out


def columns(lines, W):
    """One column, or two split at a gutter near the middle."""
    if not lines:
        return [lines]
    left = [l for l in lines if l["bbox"][2] < W * 0.56]
    right = [l for l in lines if l["bbox"][0] > W * 0.44]
    full = [l for l in lines if l not in left and l not in right]
    if len(left) >= 4 and len(right) >= 4 and len(full) <= max(2, 0.15 * len(lines)):
        return [sorted(left, key=lambda l: l["bbox"][1]), sorted(right, key=lambda l: l["bbox"][1])]
    return [sorted(lines, key=lambda l: l["bbox"][1])]


def merge_rows(col):
    """The OCR sometimes cuts one printed line in two: a margin number as a
    line of its own, set a few pixels lower than its text (Bel 28), or a line
    split mid-way ('27 granted thee.' | 'Then Daniel took'). Sorted by their
    tops, the halves come out in the wrong order. Lines that share most of
    their height are one printed line: join them, words left to right."""
    out = []
    for l in sorted(col, key=lambda l: l["bbox"][1]):
        if out:
            m = out[-1]
            lo, hi = max(m["bbox"][1], l["bbox"][1]), min(m["bbox"][3], l["bbox"][3])
            h = min(m["bbox"][3] - m["bbox"][1], l["bbox"][3] - l["bbox"][1])
            gap = max(l["bbox"][0] - m["bbox"][2], m["bbox"][0] - l["bbox"][2])
            num_only = [x for x in (m, l) if all(numlike(digits(w[5])) for w in x["words"])]
            # a line that already carries a margin number does not take a second one
            # (1 Macc 4.22: the OCR set '23' in the line above its own, '22' beside it)
            taken = num_only and any(numlike(digits(x["words"][0][5])) for x in (m, l) if x is not num_only[0])
            if 0 <= gap < 2 * m["xs"] and h > 0 and hi - lo > 0.85 * h and not taken:
                words = sorted(m["words"] + l["words"], key=lambda w: w[0])
                out[-1] = dict(m, words=words, text=" ".join(w[5] for w in words),
                               bbox=(min(m["bbox"][0], l["bbox"][0]), min(m["bbox"][1], l["bbox"][1]),
                                     max(m["bbox"][2], l["bbox"][2]), max(m["bbox"][3], l["bbox"][3])))
                continue
        out.append(l)
    return out


def is_marginal(w, edge, xs):
    t = w[5].strip('.,:;’‘\'"_—*“”()[]')
    if w[0] >= edge - 0.3 * xs:
        return False
    if any(c.isdigit() for c in t):
        return True
    if t.isalpha():
        return w[2] < edge - 0.3 * xs and len(t) <= 3
    return w[2] - w[0] >= 0.25 * xs or w[2] < edge - 0.3 * xs


def margin_tokens(col):
    """(text edge, x_size, [(line, margin words, text words)]) for one column.
    The edge is the commonest left edge of lines that open with a word."""
    xs = st.median([l["xs"] for l in col]) if col else 40
    c = collections.Counter()
    for l in col:
        w = l["words"][0]
        t = w[5].strip('‘“"(')
        if len(l["words"]) >= 3 and t[:1].isalpha() and len(t) >= 3:
            c[int(w[0] // (0.25 * xs))] += 1
    if c:
        b, _ = c.most_common(1)[0]
        cand = sorted(l["words"][0][0] for l in col
                      if len(l["words"]) >= 3 and int(l["words"][0][0] // (0.25 * xs)) in (b - 1, b, b + 1))
        edge = cand[len(cand) // 4]
    else:
        edge = min((l["words"][0][0] for l in col), default=0)
    out = []
    for l in col:
        mw = []
        for w in l["words"]:
            if is_marginal(w, edge, xs):
                mw.append(w)
            else:
                break
        tw = list(l["words"][len(mw):])
        if mw:
            m = re.match(r'^(\d+)([A-Za-z‘“(].*)$', mw[-1][5])   # "4the" = verse 4 + "the"
            if m:
                w = mw[-1]
                mw[-1] = (w[0], w[1], w[0] + (w[2] - w[0]) * len(m.group(1)) // len(w[5]), w[3], w[4], m.group(1))
                tw.insert(0, (w[0], w[1], w[2], w[3], w[4], m.group(2)))
        out.append((l, mw, tw))
    return edge, xs, out


HEADRX = re.compile(r'([0-9IlOoSsgZBτ]{1,3})\s*[.,:;]\s*([0-9IlOoSsgZBτ]{1,3}[ab]?)\s*'
                    r'(?:[-—–~:.]+\s*(?:([0-9IlOoSsgZBτ]{1,3})\s*[.,:;]\s*)?([0-9IlOoSsgZBτ]{1,3}))?')


def head_text(head_lines):
    return " ".join(l["text"] for l in sorted(head_lines, key=lambda l: l["bbox"][0]))


def head_range(t):
    """'BOOK OF ENOCH 12. 5—14. 4' -> (12, 5, 14, 4)."""
    m = HEADRX.search(t)
    if not m:
        return None
    a = num(m.group(1))
    b = num(m.group(2).rstrip('ab'))
    c = num(m.group(3)) if m.group(3) else a
    d = num(m.group(4)) if m.group(4) else b
    if a is None or c is None:
        return None
    return (a, b, c, d)


def head_ok(h, ch):
    return h[0] <= ch <= h[2] or ch in alts(h[0]) or ch in alts(h[2])


def smooth_heads(heads):
    """Drop a running head whose chapter disagrees with its neighbours'
    (an OCR misreading of the head itself, '19' for '12')."""
    pgs = sorted(heads)
    out = {}
    for i, p in enumerate(pgs):
        nb = [heads[q][0] for q in pgs[max(0, i - 3):i + 4] if q != p]
        if nb and min(abs(x - st.median(nb)) for x in alts(heads[p][0])) <= 2:
            out[p] = heads[p]
    return out


def printed_page(p):
    """The folio at the foot of the page, if the OCR read one."""
    H = p["h"]
    for l in p["lines"]:
        if l["bbox"][1] > H * 0.9 and len(l["words"]) == 1 and l["words"][0][5].isdigit():
            return int(l["words"][0][5])
    return None

# ------------------------------------------------------------------ verses

HEADING = re.compile(r'^\(?[a-z0-9]?\)?\s*[IVXLCl1]{1,6}\s*[.:]\s*[\dIl]{1,3}\s*[-–—.]|^\(?[a-z]\)\s')


def is_heading(text):
    """Charles's section heads in the body ('V. 1-8. Victories of Judas ...')."""
    return bool(HEADING.match(text)) or len(re.findall(r'\d+\s*[-–]\s*\d+', text)) >= 2


def collect(pages, leaves, T, layout, head_fn=head_range):
    """Body rows in reading order: (leaf, kind, tokens, text), kind 'm' (a
    margin-numbered line), 't' (text), 'h' (a section heading, dropped), 'a'
    (apparatus that slipped into the body, dropped).
    Also the running head of each leaf, and the leaves printed in two
    columns. A two-column page in these books is two witnesses side by side
    (the LXX and Theodotion in Bel and Susanna, the alpha and beta texts of
    the Testaments), the right one numbered in its right margin, which this
    reader does not read; so only the left column is kept, and the leaves are
    listed for the measure."""
    rows, heads, twocol = [], {}, []
    for pg in leaves:
        p = pages[pg]
        head, body, _ = split_body(p, T)
        hr = head_fn(head_text(head))
        if hr:
            heads[pg] = hr
        cols = columns(split_at_gutter(body, p["w"]), p["w"])
        if len(cols) == 2:
            cols = cols[:1]
            twocol.append(pg)
        for col in cols:
            edge, xs, rr = margin_tokens(merge_rows(col))
            hts = [w[3] - w[1] for l, mw, tw in rr for w in mw if digits(w[5]).isdigit()]
            dh = st.median(hts) if hts else 0.6 * xs
            for l, mw, tw in rr:
                text = " ".join(w[5] for w in tw).strip()
                mw = [w for w in mw if not w[5].startswith('(') and (w[2] - w[0] >= 0.2 * xs)]
                if is_apparatus_text(l["text"]):
                    rows.append((pg, 'a', [], text))
                    continue
                if is_heading(text) and not mw:
                    rows.append((pg, 'h', [], text))
                    continue
                toks = [(digits(w[5]), (w[3] - w[1]) > 1.3 * dh) for w in mw
                        if numlike(digits(w[5])) or (w[2] >= edge - 1.6 * xs and len(digits(w[5])) <= 3)]
                rows.append((pg, 'm' if toks else 't', toks, text))
    return rows, heads, twocol


RESYNC = 7.0


def decode(rows, heads, chapters=True, start_ch=1, max_ch=None, parts=None, part_of_page=None):
    """Viterbi over the margin markers; returns {row index: (part, ch, v)}."""
    marks = [i for i, r in enumerate(rows) if r[1] == 'm']
    beam = {(0, start_ch if chapters else 0, 0): (0.0, None)}
    hist = []
    for i in marks:
        pg, _, toks, _ = rows[i]
        tall = any(t for _, t in toks)
        vals = [s for s, t in toks if not t] or [s for s, t in toks]
        s0 = vals[0] if vals else ''
        nb = {}
        for (pt, c, vv), (cost, _) in beam.items():
            cands = [((pt, c, vv + k), (k - 1) * 1.2 + fuzzy_eq(vv + k, s0) + (1.5 if tall and chapters else 0))
                     for k in range(1, 6)]
            if re.fullmatch(r'\d{1,3}', s0) and int(s0) != vv + 1:
                cands.append(((pt, c, int(s0)), RESYNC))
                if chapters:
                    cands.append(((pt, c + 1, int(s0)), RESYNC + 0.7))
            if chapters:
                for nv in (1, 2, 3):
                    cc = 2.0 + (nv - 1) * 1.0
                    if tall:
                        cc -= 1.6
                        tt = [s for s, t in toks if t]
                        if tt and tt[0].startswith(str(c + 1)):
                            cc -= 0.5
                        if len(toks) > 1:
                            cc += min(fuzzy_eq(nv, s0), 0.8)
                    else:
                        cc += fuzzy_eq(nv, s0)
                    cands.append(((pt, c + 1, nv), cc))
            if parts and pt + 1 < parts:
                cands.append(((pt + 1, start_ch, 1),
                              2.5 + (0 if tall else fuzzy_eq(1, s0)) - (1.0 if tall else 0)))
            for st2, cc in cands:
                if max_ch and st2[1] > max_ch:
                    continue
                tot = cost + cc
                if st2 not in nb or tot < nb[st2][0]:
                    nb[st2] = (tot, (pt, c, vv))
        hr = heads.get(pg)
        if chapters and hr:
            for s2 in list(nb):
                if not head_ok(hr, s2[1]):
                    nb[s2] = (nb[s2][0] + 1.0, nb[s2][1])
        if part_of_page and part_of_page.get(pg) is not None:
            p = part_of_page[pg]
            for s2 in list(nb):
                if s2[0] < p or s2[0] > p + 1:
                    nb[s2] = (nb[s2][0] + 3.0, nb[s2][1])
        beam = dict(sorted(nb.items(), key=lambda kv: kv[1][0])[:400])
        hist.append(beam)
    if not hist:
        return {}
    s = min(beam, key=lambda x: beam[x][0])
    path = []
    for h in reversed(hist):
        path.append(s)
        s = h[s][1]
    path.reverse()
    return dict(zip(marks, path))


SENT = re.compile(r'[.?!:;][’”\'")\]]*\s+(?=[\[(‘“"]?[A-Z])')


def verse_start(line_text, prev_text):
    """(offset, how): where in its first line a verse begins."""
    end = re.search(r'([.?!:;])[’”\'")\]]*\s*$', prev_text or "")
    if not prev_text or (end and (re.match(r'[\[(‘“"]?[A-Z]', line_text)
                                  or end.group(1) in ";:")):
        # the previous line ended a clause: a verse Charles numbers at a
        # semicolon opens its line in lower case (Tob 5.17 'we shall go safe')
        return 0, 'line-start'
    ms = list(SENT.finditer(line_text))
    if len(ms) == 1:
        return ms[0].end(), 'sentence'
    if ms:
        return ms[0].end(), 'sentence-first'
    return 0, 'line'


def join(a, b):
    if not a:
        return b
    if not b:
        return a
    if a.endswith('-') and b[:1].islower():
        return a[:-1] + b
    return a + ' ' + b


def build_units(rows, assign):
    """Verse units from decoded rows: {part, ch, v, text, leaves, num, start}."""
    units, cur, stats = [], None, collections.Counter()
    for i, (pg, kind, toks, text) in enumerate(rows):
        if kind == 'h':
            stats['heading-dropped'] += 1
            continue
        if kind == 'a':
            stats['apparatus-dropped'] += 1
            continue
        if kind == 'm':
            pt, c, v = assign[i]
            s0 = ([s for s, t in toks if not t] or [s for s, t in toks])[0]
            how = 'read' if s0 == str(v) else ('fuzzy' if fuzzy_eq(v, s0) < 1 else 'inferred')
            off, sh = verse_start(text, cur['text'] if cur else '')
            if cur is not None and off:
                cur['text'] = join(cur['text'], text[:off].strip())
                text = text[off:]
            if cur and (cur['part'], cur['ch'], cur['v']) == (pt, c, v):
                cur['text'] = join(cur['text'], text)
                continue
            stats[how] += 1
            stats['start:' + sh] += 1
            cur = {'part': pt, 'ch': c, 'v': v, 'text': text, 'leaves': [pg], 'num': how, 'start': sh}
            units.append(cur)
        elif cur is not None and text:
            cur['text'] = join(cur['text'], text)
            if cur['leaves'][-1] != pg:
                cur['leaves'].append(pg)
    return units, stats


def head_agreement(units, heads):
    """Of the pages whose running head was read, how many have a decoded
    verse whose chapter is the head's first or last chapter."""
    by = collections.defaultdict(set)
    for u in units:
        for lf in u['leaves'][:1]:
            by[lf].add(u['ch'])
    tot = ok = 0
    for pg, h in heads.items():
        if pg in by:
            tot += 1
            ok += bool(by[pg] & {h[0], h[2]})
    return ok, tot

# ------------------------------------------------------------------ lines

SIBMARK = re.compile(r'\((\d{1,4})\)')


def sibyl_units(pages, leaves, T, parts):
    """The Sibylline Oracles: Charles prints prose with each Greek line's
    number inline, '(41)', the hundreds dropped after the first ('(97)'
    after 696). A number that is not the next line, or the next but a few,
    is an OCR slip and is taken as the next line (flagged)."""
    text = []
    for pg in leaves:
        _, body, _ = split_body(pages[pg], T)
        for col in columns(body, pages[pg]["w"]):
            for l in col:
                if not is_heading(l["text"]):
                    text.append((pg, l["text"]))
    units, cur, part, L = [], None, -1, 0
    stats = collections.Counter()
    for pg, t in text:
        pos = 0
        for m in SIBMARK.finditer(t):
            n = int(m.group(1))
            if cur is not None:
                cur['text'] = join(cur['text'], t[pos:m.start()].strip())
            pos = m.end()
            if n == 1 and part + 1 < len(parts) and (part < 0 or (L >= 2 and L % 100 not in (99, 0))):
                part, L, how = part + 1, 1, 'read'          # a new book or fragment
            elif n >= 100 and L < n and (n < L + 200 or L == 0):
                L, how = n, 'read'                          # printed in full
            else:
                cand = (L // 100) * 100 + n
                if cand <= L:
                    cand += 100                             # '(1)' after '(700)' is 701
                if 0 < cand - L <= 4:
                    L, how = cand, 'read'
                else:
                    L, how = L + 1, 'inferred'
            if part < 0:
                part = 0
            stats[how] += 1
            cur = {'part': part, 'ch': 0, 'v': L, 'text': '', 'leaves': [pg], 'num': how, 'start': 'exact'}
            units.append(cur)
        if cur is not None:
            cur['text'] = join(cur['text'], t[pos:].strip())
            if cur['leaves'][-1] != pg:
                cur['leaves'].append(pg)
    return units, stats
