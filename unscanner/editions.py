# prov: 2026-10-19 claude-opus-5-5 drafted
# fable_review: pending
"""Several scans of one book, each read by two OCR engines, merged by vote.

    python3 -m unscanner editions cs6 --scan toronto=cs6-toronto:<toronto_djvu.xml> \
                                      --scan cornell=cs6-cornell:<cornell_djvu.xml>

Adam, 2026-10-19: "run each of the different editions of the same volume against each other and
merge them intelligently and get my eyes on anything that looks off".

THE WITNESSES. Each scan gives two independent readings of every word: ours (tesseract, run by the
Unscanner, with a confidence per word) and the Internet Archive's (an older engine, its `_djvu.xml`,
with a box per word but no confidence). Two scans of two printings from the same plates (here
Toronto's 1892 and Cornell's 1896) give four readings per word, and the plates mean the lines and
page numbers match, so the readings line up word for word on almost every page.

Ours is read RAW: where the Unscanner's own collation already mended a word from the Archive's text,
the word's `was` is used, so no reading is ever counted twice.

THE VOTE, per word, on letters only (case, punctuation and accents never count as a disagreement):

  - all readings agree                                           -> agreed
  - one reading has three or more witnesses                      -> majority (auto)
  - one reading has two, every other has one, and the two span
    BOTH scans, or the book attests it (it occurs 3+ times
    elsewhere among clean readings) while no rival does           -> majority (auto)
  - a two-two split where exactly one side is attested           -> attested (auto)
  - anything else                                                -> REVIEW: Adam decides

The base text is our Toronto reading. A mend takes only the winner's letters; our punctuation and
capitalisation stay (collate._recase). Every mend and every review item is recorded with the page,
the line, all four readings and where each word sits on each scan, so the review page can show the
two scans side by side.
"""
import difflib
import json
import os
import re
from collections import Counter, defaultdict

from .collate import norm, _core_span, _recase

CLEAN_CONF = 90          # a tesseract word this sure is "clean" for attestation
ATTESTED = 3             # occurrences elsewhere that make a word the book's own
LOW_CONF = 70            # a lone disagreement is reviewed only if ours was this unsure


def key(t):
    """What a vote compares: letters; for a token with none, its digits."""
    k = norm(t)
    return k if k else re.sub(r"\D", "", t)


# ---------------------------------------------------------------- readers

def load_tesseract(work_dir):
    """The Unscanner's book.json -> {scan page n: {"label", "size", "words": [...]}}, words raw."""
    book = json.load(open(os.path.join(work_dir, "book.json"), encoding="utf-8"))
    out = {}
    for p in book["pages"]:
        words = []
        for li, ln in enumerate(p.get("lines", [])):
            for w in ln.get("words", []):
                words.append({"t": w.get("was") or w["t"], "conf": w.get("conf"), "bbox": w["bbox"], "line": li})
        out[p["n"]] = {"label": p.get("label"), "size": (p.get("w"), p.get("h")), "words": words,
                       "kind": p.get("kind")}
    return out


def load_djvu(path):
    """The Archive's _djvu.xml -> {scan page n (1-based): {"size", "words"}}; boxes as x0,y0,x1,y1."""
    x = open(path, encoding="utf-8", errors="replace").read()
    ent = lambda s: s.replace("&quot;", '"').replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<").replace("&apos;", "'")
    out = {}
    for i, m in enumerate(re.finditer(r"<OBJECT\b([^>]*)>(.*?)</OBJECT>", x, re.S)):
        attrs, body = m.group(1), m.group(2)
        h = int(re.search(r'height="(\d+)"', attrs).group(1))
        w = int(re.search(r'width="(\d+)"', attrs).group(1))
        words = []
        for li, line in enumerate(re.findall(r"<LINE>(.*?)</LINE>", body, re.S)):
            for c, t in re.findall(r'<WORD coords="([^"]+)"[^>]*>([^<]*)</WORD>', line):
                v = [int(n) for n in c.split(",")[:4]]
                words.append({"t": ent(t), "conf": None, "bbox": [v[0], v[3], v[2], v[1]], "line": li})
        out[i + 1] = {"size": (w, h), "words": words}
    return out


def scale(words, frm, to):
    """Boxes from one pixel grid to another (the Archive's page vs our 300 dpi raster)."""
    if not (frm and to and frm[0] and to[0]):
        return words
    sx, sy = to[0] / frm[0], to[1] / frm[1]
    return [{**w, "bbox": [round(w["bbox"][0] * sx), round(w["bbox"][1] * sy),
                           round(w["bbox"][2] * sx), round(w["bbox"][3] * sy)]} for w in words]


# ---------------------------------------------------------------- alignment

def align(base, other):
    """{base index: other index}, one word for one word where the letters line up."""
    a = [key(w["t"]) for w in base]
    b = [key(w["t"]) for w in other]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    m = {}
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                m[i1 + k] = j1 + k
    return m


def folio(words):
    """The printed page number: a bare number on one of the page's first three lines.
    This edition sets it on its own line between two running heads ("QUACKS / 261 /
    QUACKS"), which the Unscanner's folio rule (a number at the end of a head) misses."""
    lines = defaultdict(list)
    for w in words:
        lines[w["line"]].append(w["t"])
    for li in sorted(lines)[:3]:
        t = " ".join(lines[li]).strip(" .,'")
        if re.fullmatch(r"\d{1,4}", t):
            return t
    return None


TEXT_WORDS = 120         # a page with this many words is a text page (plates and blanks are not)


def labels(scan):
    """Each text page's folio, from either engine (ours first, then the Archive's); a folio
    neither engine read is inferred when the folios on BOTH sides agree with counting text
    pages between them (plates carry no number, so they are not counted)."""
    out = {}
    for n, p in scan["tess"].items():
        lab = folio(p["words"]) or (folio(scan["djvu"][n]["words"]) if n in scan["djvu"] else None)
        if lab:
            out[n] = lab
    text = sorted(n for n, p in scan["tess"].items() if len(p["words"]) >= TEXT_WORDS)
    pos = {n: k for k, n in enumerate(text)}
    known = [n for n in text if n in out]
    for a, b in zip(known, known[1:]):
        gap = pos[b] - pos[a]
        if gap > 1 and int(out[b]) - int(out[a]) == gap:
            for k in range(1, gap):
                out[text[pos[a] + k]] = str(int(out[a]) + k)
    return out


def pair_pages(scans):
    """Printed page label -> {scan: page n}, for labels every scan reads exactly once."""
    by = {}
    for name, s in scans.items():
        labs = labels(s)
        seen = Counter(labs.values())
        for n, lab in labs.items():
            if lab and seen[lab] == 1:
                by.setdefault(lab, {})[name] = n
    return {lab: d for lab, d in by.items() if len(d) == len(scans)}


# ---------------------------------------------------------------- the vote

def load_lexicon(repo, brewer=None):
    """Words known outside this book: Webster's 1913 headwords (data/lexicons, committed) and every
    word of Brewer's Dictionary of Phrase and Fable that occurs twice (proper names, phrases)."""
    import gzip
    lex = set()
    wp = os.path.join(repo, "data", "lexicons", "webster1913.json.gz")
    if os.path.exists(wp):
        for h in json.load(gzip.open(wp, "rt", encoding="utf-8")):
            for part in h.split():
                k = key(part)
                if k:
                    lex.add(k)
    bp = brewer or os.path.join(repo, "data", "lexicons", "brewer-1894.paras.json.gz")
    if os.path.exists(bp):
        c = Counter()
        for para in json.load(gzip.open(bp, "rt", encoding="utf-8"))["paras"]:
            for line in para["lines"]:
                c.update(key(t) for t in line.split())
        lex |= {k for k, v in c.items() if v >= 2 and k}
    return lex


def decide(readings, vocab, scan_of, lexicon=frozenset(), joined=None):
    """readings: {witness: key}. -> (verdict, winning key or None).
    `joined`: {key: key joined with the next word}, for a word broken at the line end."""
    support = defaultdict(set)
    for wit, k in readings.items():
        if k:
            support[k].add(wit)
    if len(support) <= 1:
        return "agreed", next(iter(support), None)
    ranked = sorted(support.items(), key=lambda kv: -len(kv[1]))
    top, top_w = ranked[0]
    second = len(ranked[1][1])
    att = {k: vocab.get(k, 0) for k in support}
    if len(top_w) >= 3 and len(top_w) > second:
        return "majority", top
    if len(top_w) == 2 and second == 1:
        both_scans = len({scan_of[w] for w in top_w}) > 1
        if both_scans or (att[top] >= ATTESTED and all(att[k] < ATTESTED for k in support if k != top)):
            return "majority", top
    if len(top_w) == 2 and second == 2 and len(ranked) == 2:
        a, b = ranked[0][0], ranked[1][0]
        if att[a] >= ATTESTED and att[b] < 2:
            return "attested", a
        if att[b] >= ATTESTED and att[a] < 2:
            return "attested", b
    # Last: the language itself. Exactly one candidate a known word (Webster 1913, or twice in
    # Brewer's Dictionary), with at least two witnesses behind it -> that one.
    def word(k):
        if len(k) < 3:
            return False                  # a lone letter or pair proves nothing
        if k in lexicon:
            return True
        for suf in ("s", "es", "d", "ed", "ing", "ly", "er", "est", "ness"):
            stem = k[:-len(suf)]
            if k.endswith(suf) and len(stem) >= 3 and (stem in lexicon or stem + "e" in lexicon):
                return True               # Webster lists headwords: "flared" is "flare"
        return False
    known = lambda k: word(k) or bool(joined and joined.get(k) and word(joined[k]))
    real = [k for k, ws in support.items() if known(k)]
    if len(real) == 1 and len(support[real[0]]) >= 2:
        return "lexicon", real[0]
    return "review", None


def collate(scans, base_scan, lexicon=frozenset()):
    """scans: {name: {"tess": pages, "djvu": pages}} -> result dict (pages, mends, review, stats)."""
    wit_order = [(s, e) for s in scans for e in ("tess", "djvu")]
    scan_of = {f"{s}.{e}": s for s, e in wit_order}
    vocab = Counter()
    for s, d in scans.items():
        for p in d["tess"].values():
            vocab.update(key(w["t"]) for w in p["words"] if (w["conf"] or 0) >= CLEAN_CONF)
        for p in d["djvu"].values():
            vocab.update(key(w["t"]) for w in p["words"])
    pairs = pair_pages(scans)
    stats = Counter()
    pages, mends, review = [], [], []
    for lab, ns in sorted(pairs.items(), key=lambda kv: kv[1][base_scan]):
        base = scans[base_scan]["tess"][ns[base_scan]]
        bw = base["words"]
        maps = {}
        for s, e in wit_order:
            if (s, e) == (base_scan, "tess"):
                continue
            pg = scans[s][e].get(ns[s])
            if not pg:
                continue
            words = pg["words"]
            if e == "djvu":
                words = scale(words, pg["size"], scans[s]["tess"][ns[s]]["size"])
            maps[f"{s}.{e}"] = (words, align(bw, words))
        out_words = []
        for i, w in enumerate(bw):
            rd = {f"{base_scan}.tess": key(w["t"])}
            for wit, (words, m) in maps.items():
                if i in m:
                    rd[wit] = key(words[m[i]]["t"])
            if not rd[f"{base_scan}.tess"]:
                out_words.append(w["t"])
                continue
            if len(rd) < 3:
                stats["thin"] += 1
                out_words.append(w["t"])
                continue
            joined = None
            if w["t"].rstrip().endswith("-") and i + 1 < len(bw):
                nxt = key(bw[i + 1]["t"])
                joined = {k: k + nxt for k in rd.values() if k}
            verdict, win = decide(rd, vocab, scan_of, lexicon, joined)
            base_k = rd[f"{base_scan}.tess"]
            if win and win != base_k and len(base_k) >= 3 and len(win) < 0.6 * len(base_k):
                verdict = "review"        # never cut a word short: that is a misaligned split
                stats["shortened"] += 1
            stats[verdict] += 1
            t = w["t"]
            item = None
            if verdict in ("majority", "attested", "lexicon") and win != rd[f"{base_scan}.tess"]:
                lo, hi = _core_span(t)
                src = next(words[m[i]]["t"] for wit, (words, m) in maps.items() if i in m and rd[wit] == win) \
                    if any(rd.get(wit) == win for wit in maps) else win
                letters = norm(src) or src.strip()        # the Archive's words can carry a trailing space
                t = t[:lo] + _recase(letters, t[lo:hi]) + t[hi:]
                stats["mended"] += 1
                item = "mend"
            elif verdict == "review":
                item = "review"
            if item:
                where = {f"{base_scan}.tess": {"n": ns[base_scan], "bbox": w["bbox"], "t": w["t"], "conf": w["conf"]}}
                for wit, (words, m) in maps.items():
                    if i in m:
                        s = wit.split(".")[0]
                        where[wit] = {"n": ns[s], "bbox": words[m[i]]["bbox"], "t": words[m[i]]["t"],
                                      "conf": words[m[i]]["conf"]}
                line = [x["t"] for x in bw if x["line"] == w["line"]]
                rec = {"page": lab, "index": i, "base": w["t"], "result": t, "verdict": verdict,
                       "line": " ".join(line), "readings": where}
                (mends if item == "mend" else review).append(rec)
            out_words.append(t)
        pages.append({"label": lab, "scans": ns, "words": len(bw), "text": " ".join(out_words),
                      "tokens": out_words, "line_of": [w["line"] for w in bw]})
    stats["pages"] = len(pages)
    stats["words"] = sum(p["words"] for p in pages)
    return {"pages": pages, "mends": mends, "review": review, "stats": dict(stats)}


# ---------------------------------------------------------------- the review page's data

def crop_pair(rec, scan_dirs, pad=(150, 14), height=34, quality=62):
    """One small JPEG: the word in its line on each scan, stacked (first scan on top), boxed red."""
    from PIL import Image, ImageDraw
    import io
    strips = []
    for s, d in scan_dirs.items():
        r = rec["readings"].get(f"{s}.tess") or rec["readings"].get(f"{s}.djvu")
        if not r:
            continue
        png = os.path.join(d, "gray", f"{r['n']:04d}.png")
        if not os.path.exists(png):
            continue
        im = Image.open(png).convert("L")
        x0, y0, x1, y1 = r["bbox"]
        box = (max(0, x0 - pad[0]), max(0, y0 - pad[1]), min(im.width, x1 + pad[0]), min(im.height, y1 + pad[1]))
        c = im.crop(box).convert("RGB")
        ImageDraw.Draw(c).rectangle([x0 - box[0] - 3, y0 - box[1] - 3, x1 - box[0] + 3, y1 - box[1] + 3],
                                    outline=(196, 40, 40), width=3)
        strips.append(c.resize((max(1, round(c.width * height / c.height)), height)))
    if not strips:
        return None
    W = max(x.width for x in strips)
    out = Image.new("RGB", (W, sum(x.height for x in strips) + 3 * (len(strips) - 1)), (255, 255, 255))
    y = 0
    for x in strips:
        out.paste(x, (0, y))
        y += x.height + 3
    buf = io.BytesIO()
    out.save(buf, "JPEG", quality=quality, optimize=True)
    return buf.getvalue()


def review_data(result, scan_dirs, volume, spot=("lexicon", "attested")):
    """Items for the review page: every review word, and the riskier automatic fixes to spot-check."""
    import base64
    def readings(rec):
        groups = {}
        for wit, r in rec["readings"].items():
            k = key(r["t"])
            if not k:
                continue
            g = groups.setdefault(k, {"text": r["t"].strip(), "by": []})
            g["by"].append(wit)
        return sorted(groups.values(), key=lambda g: -len(g["by"]))
    def context(rec):
        line, w = rec["line"], rec["base"]
        i = line.find(w)
        return line if i < 0 else line[:i] + "⟦" + w + "⟧" + line[i + len(w):]
    items = []
    for kind, recs in (("review", result["review"]),
                       ("spot", [m for m in result["mends"] if m["verdict"] in spot])):
        for rec in recs:
            img = crop_pair(rec, scan_dirs)
            items.append({"id": f"v{volume}-p{rec['page']}-i{rec['index']}", "kind": kind, "page": rec["page"],
                          "context": context(rec), "base": rec["base"], "result": rec["result"],
                          "verdict": rec["verdict"], "readings": readings(rec),
                          "img": base64.b64encode(img).decode() if img else None})
    auto = [{"page": m["page"], "from": m["base"], "to": m["result"]}
            for m in result["mends"] if m["verdict"] not in spot]
    return {"volume": volume, "stats": result["stats"], "items": items, "auto": auto}


# ---------------------------------------------------------------- the merged text

def page_lines(page, base=None, base_scan=None, mends=None):
    """A collated page -> its lines, each a list of word strings (one per base-scan word).
    A page from a collation older than `tokens`/`line_of` is rebuilt from the base scan
    (base = load_tesseract(base dir)) and its mends ({(page, index): text}); splitting the old flat
    text on spaces is not safe, a mend could hold one ("5. .")."""
    if "tokens" in page:
        words, line_of = page["tokens"], page["line_of"]
    else:
        bw = base[page["scans"][base_scan]]["words"]
        words = [(mends or {}).get((page["label"], i), w["t"]) for i, w in enumerate(bw)]
        line_of = [w["line"] for w in bw]
    lines, last = [], object()
    for w, li in zip(words, line_of):
        if li != last:
            lines.append([])
            last = li
        lines[-1].append(w)
    return lines


def _page_furniture(bp):
    """Line indexes of a base-scan page (book.json page) that are page furniture: the Unscanner's own
    `drop`, plus a short all-capitals first line near the top that its 12% band missed (this book's
    running heads sit at 12-14%: "RABAGAS 2", "RICHARD III.")."""
    out = set(bp.get("drop") or [])
    if bp["lines"]:
        ln = bp["lines"][0]
        txt = " ".join(w["t"] for w in ln["words"])
        letters = re.sub(r"[^A-Za-z]", "", txt)
        if ln["bbox"][1] < 0.16 * bp["h"] and len(ln["words"]) <= 4 and letters and letters.isupper():
            out.add(0)
    return out


def merged_text(result, answers, volume, base=None, base_scan=None, book=None):
    """The volume's text with every answer put in place of its word, its page furniture (running
    heads, folios) taken out, and every word broken at a margin, a column or a page ("Cuf-" / "fey",
    "ex-" / "plained") made one word again by the Unscanner's own rule 6, and 6b for ranges, small
    capitals and names (layout.join_tokens). Adam, 2026-10-20: "Fix all words split across lines."

    Paragraphs come from the Unscanner's blocks (book = the base scan's book.json), in reading order,
    a column at a time; a block marked `cont` (it starts unindented at the top of a column or a page)
    continues the paragraph before it. A break is only rejoined inside a paragraph.

    answers: {"v<vol>-p<page>-i<index>": text}, already ranked by the caller (Adam's pick over
    Claude's read over a rule's clear). -> ([{"type", "pages", "text"}], rejoin log)."""
    from . import layout as L
    mends = {(m["page"], m["index"]): m["result"] for m in result.get("mends", [])}
    bpages = {p["n"]: p for p in book["pages"]}
    stream = []
    for p in result["pages"]:
        lines = page_lines(p, base, base_scan, mends)
        i = 0
        for ln in lines:
            for j in range(len(ln)):
                a = answers.get(f"v{volume}-p{p['label']}-i{i}")
                if a is not None:
                    ln[j] = a
                i += 1
        bp = bpages[p["scans"][base_scan]]
        drop = set(bp.get("drop") or [])
        at = {tuple(ln["bbox"]): li for li, ln in enumerate(bp["lines"])}
        for bl in bp.get("blocks", []):
            lis = [at.get(tuple(ln["bbox"])) for ln in bl["lines"]]
            words = [[{"t": w} for w in lines[li] if w] for li in lis if li is not None and li not in drop]
            words = [ws for ws in words if ws]
            if not words:
                continue
            # continues the paragraph before: marked `cont` by the Unscanner, or (verse running on into
            # the next column or page, which starts indented) it begins with a lower-case word right
            # after a word broken at the margin. No paragraph of this book begins in lower case.
            prev_end = stream[-1]["lines"][-1][-1]["t"] if stream and stream[-1]["lines"] else ""
            run_on = prev_end.endswith("-") and not prev_end.endswith("--") and words[0][0]["t"][:1].islower()
            if stream and (run_on or (bl.get("cont") and stream[-1]["type"] == "para" and bl["type"] == "para")):
                stream[-1]["lines"] += words
                if p["label"] not in stream[-1]["pages"]:
                    stream[-1]["pages"].append(p["label"])
            else:
                stream.append({"type": bl["type"], "lines": words, "pages": [p["label"]]})
    # the evidence is the whole volume, as the Unscanner's is (it reads lines as {"words": [...]})
    hyph, whole = L.hyphen_evidence([{"lines": [{"words": ln} for g in stream for ln in g["lines"]]}])
    log = L.new_log()
    dictionary = L.load_dictionary(os.path.join(os.path.dirname(__file__), ".."))
    out = []
    for g in stream:
        toks = L.join_tokens(g["lines"], hyph, whole, log, more=True, dictionary=dictionary)
        out.append({"type": g["type"], "pages": g["pages"], "text": L.tokens_text(toks)})
    authors = L.attribution_names(g["text"] for g in out)
    log["dashes"] = {}
    # at a block's edge: a quotation's source set on its own line ("- Tennyson, The Princess") takes
    # the attribution dash; any other block opening with a lone "-" loses it (dirt); a number range
    # broken across two blocks ("(1276-" / "1347).") is one range
    k = 0
    while k < len(out):
        g = out[k]
        if g["text"].endswith(" -") and k + 1 < len(out):   # a block ending in a lone dash: carry it on
            g["text"] = g["text"][:-2]
            out[k + 1]["text"] = "- " + out[k + 1]["text"]
        if g["text"] in ("-", "—", "_"):                 # a block that is only a dash: carry it on
            out.pop(k)
            if k < len(out):
                out[k]["text"] = "- " + out[k]["text"]
            continue
        if g["text"].startswith("- "):
            name = re.sub(r"^[^\w]+", "", g["text"][2:].split(" ")[0]).split(",")[0].rstrip(".")
            g["text"] = ("—" if name in authors else "") + g["text"][2:]
            log["dashes"]["attribution dash" if name in authors else "stray hyphen dropped"] = \
                log["dashes"].get("attribution dash" if name in authors else "stray hyphen dropped", 0) + 1
        if k and re.search(r"\d-$", out[k - 1]["text"]) and re.match(r"\d", g["text"]):
            out[k - 1]["text"] = out[k - 1]["text"][:-1] + "–" + g["text"]
            out[k - 1]["pages"] += [x for x in g["pages"] if x not in out[k - 1]["pages"]]
            out.pop(k)
            continue
        k += 1
    for g in out:
        g["text"], c = L.dashes(g["text"], authors)
        for k, v in c.items():
            log["dashes"][k] = log["dashes"].get(k, 0) + v
    return out, log
