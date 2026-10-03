#!/usr/bin/env python3
"""press_ocr.py -- one treatise out of a scanned Works volume -> a Press document.

    python3 pipeline/press_ocr.py --heads <archive.org id>   # running heads per leaf: find a treatise's leaves
    python3 pipeline/press_ocr.py --page <id> <leaf>         # one page as the Press reads it

Source: the volume's ABBYY FineReader XML (press_abbyy), which keeps italics,
font sizes and the position of every line. The catalog entry names the
treatise's leaves: "source": {"kind": "ia-extract", ..., "leaves": [first, last]},
optionally "start"/"end" regexes for the first/last paragraph when a treatise
begins or ends mid-page.

What the Press does to the OCR, and nothing more:
  - drops the running head and the printed page number of every page (both
    are kept: the page number becomes the page's invisible anchor)
  - drops printers' signature marks at the foot of a page ("VOL. I. C")
  - takes smaller-type paragraphs at the foot of a page as that page's
    footnotes, and ties each to its call mark in the text when the marks and
    the notes can be paired one-to-one (call marks the second engine saw are
    added first, where unambiguous); otherwise the notes print at the foot of
    their page, as "Notes to p. N", and the QA counts them as page notes
  - rejoins a word hyphenated across a line end, unless the volume itself
    prints that word hyphenated elsewhere (so "self-denial" stays)
  - rejoins a paragraph broken by a page turn
  - removes the space 19th-century compositors set before ; : ? ! and ,
  - keeps italics (scripture quoted in italic stays italic)
  - applies the book's OCR corrections (pipeline/press_rules/<slug>.json
    "ocr_fixes", each tied to a leaf, from press_proof's two-engine collation)
Spelling, capitals and punctuation are otherwise the printed page's.
"""
import difflib, json, os, re, statistics, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import press_abbyy, press_build
from press_thml import esc, guard_start, wrap
from press_text import Doc, tag_refs

NOTE_MARKS = "*†‡§‖¶^•°"

def run_md(text, italic):
    t = esc(text)
    return wrap(t, "*", "*") if italic and t.strip() and re.search(r"[A-Za-z]", t) else t

def line_text(line):
    return "".join(r[0] for r in line["runs"])

def par_text(par):
    return " ".join(line_text(l) for l in par["lines"])

def par_fs(par):
    sizes = [(r[3], len(r[0].strip())) for l in par["lines"] for r in l["runs"] if r[0].strip() and r[3]]
    if not sizes:
        return 0
    tot = sum(n for _, n in sizes)
    return sum(f * n for f, n in sizes) / max(1, tot)

def body_size(pages):
    c = Counter()
    for p in pages:
        for par in p["pars"]:
            for l in par["lines"]:
                for r in l["runs"]:
                    if r[3]:
                        c[round(r[3])] += len(r[0])
    return c.most_common(1)[0][0] if c else 10

RE_HEAD_NUM = re.compile(r"^\W{0,2}[\dSOlIoJ][\dSOlIoJ ]{0,4}\W{0,2}\s|\s\W{0,2}[\dSOlIoJ][\dSOlIoJ ]{0,4}\W{0,2}$"
                         r"|^\W{0,2}\d[\dSOlIoJ]{0,3}\W{0,2}$")   # or the page number alone
RE_SIGNATURE = re.compile(r"^(VOL\.?|Vol\.?|VOI\.)\s*[IVXL1]+\.?\s*[A-Z2-9]{0,3}\.?$")

def head_key(t):
    return re.sub(r"[^a-z]", "", t.lower())

def like_head(t, known):
    """A garbled running head ("494 divine conduct; on,") is still the volume's
    running head when its letters are close to one read cleanly elsewhere."""
    k = head_key(t)
    return len(k) >= 6 and any(difflib.SequenceMatcher(None, k, h).ratio() >= 0.6 for h in known)

def column(body):
    """The text column of a page: left and right edges of its full lines."""
    ls = [l["box"] for p in body if len(p["lines"]) >= 3 for l in p["lines"]]
    if not ls:
        return None
    return statistics.median(b[0] for b in ls), statistics.median(b[2] for b in ls)

def centred_italic(par, col):
    """A sub-heading set as a short centred italic line ("First Demand.")."""
    runs = [r for l in par["lines"] for r in l["runs"] if r[0].strip()]
    t = par_text(par).strip()
    if not col or len(par["lines"]) != 1 or not runs or not all(r[1] for r in runs) or len(t.split()) > 7:
        return False
    w = col[1] - col[0]
    l, r = par["box"][0], par["box"][2]
    return l > col[0] + 0.12 * w and r < col[1] - 0.12 * w and abs((l + r) / 2 - (col[0] + col[1]) / 2) < 0.12 * w

def classify_page(page, body_fs, known_heads=()):
    """-> (running_head_text or None, body pars, note pars)"""
    pars = [p for p in page["pars"] if par_text(p).strip()]
    head = None
    if pars:
        p0 = pars[0]
        t0 = par_text(p0).strip()
        top = p0["box"][1] < page["h"] * 0.12 if page["h"] else True
        if top and len(p0["lines"]) == 1 and (RE_HEAD_NUM.search(t0) or (t0.isupper() and len(t0) < 70)
                                              or like_head(t0, known_heads)):
            head = t0
            pars = pars[1:]
    def foot_mark(p):
        # a short line at the very foot: a gathering mark ("Aa3", "Dd 3"), a
        # volume signature ("VOL. IV."), never a note or text
        t = par_text(p).strip()
        low = p["box"][1] > page["h"] * 0.86 if page["h"] else False
        return (len(p["lines"]) == 1 and len(t) <= 14 and low and len(pars) > 1)
    while pars and (RE_SIGNATURE.match(par_text(pars[-1]).strip()) or foot_mark(pars[-1]) or
                    not re.search(r"[A-Za-z0-9]{2}", par_text(pars[-1]))):
        pars = pars[:-1]     # a signature mark ("VOL. I. A"), or specks read as text
    notes = []
    while pars:
        last = pars[-1]
        fs = par_fs(last)
        low = last["box"][1] > page["h"] * 0.55 if page["h"] else True
        if fs and fs < body_fs * 0.86 and low and len(pars) > 1:
            notes.insert(0, last)
            pars = pars[:-1]
        else:
            break
    return head, pars, notes

def printed_page(head):
    if not head:
        return None
    m = re.match(r"^\W{0,2}(\d{1,4})\b", head) or re.search(r"\b(\d{1,4})\W{0,2}$", head)
    if m:
        return m.group(1)
    m = re.match(r"^([ivxlcdm]{1,8})\b", head.lower()) or re.search(r"\b([ivxlcdm]{1,8})\.?$", head.lower())
    return m.group(1) if m else None

def collect_hyphenated(pages):
    """Words the volume prints with a hyphen mid-line: those keep it at a line end."""
    keep = Counter()
    for p in pages:
        for par in p["pars"]:
            for l in par["lines"]:
                for m in re.finditer(r"\b([A-Za-z]{2,})-([A-Za-z]{2,})\b", line_text(l)):
                    keep[(m.group(1) + m.group(2)).lower()] += 1
    return keep

def fix_rx(f):
    """Whole-word pattern for a fix; a space in a split misread ('othei s',
    'puiT^ose') matches one to three non-letters: spaces, a line-end hyphen, a
    stray mark."""
    # stray marks the proof's tokens drop ('puiT^ose') may sit between letters
    parts = [r"[\^~]?".join(re.escape(c) for c in x) for x in f["from"].split()]
    return re.compile(r"(?<![A-Za-z])" + r"[^A-Za-z*]{1,3}".join(parts) + r"(?![A-Za-z])")

def apply_fixes(segs, fixes):
    """A leaf's OCR fixes, as whole words (never inside a longer word), every
    occurrence on the leaf. A misread that spans two runs (an italic change
    mid-word) merges them, keeping the first run's style."""
    for f in fixes:
        rx = fix_rx(f)
        hit = False
        for s in segs:
            s[0], n = rx.subn(f["to"], s[0])
            hit = hit or n > 0
        if not hit:
            text = "".join(s[0] for s in segs)
            m = rx.search(text)
            if m:
                pos, a = 0, None
                for k, s in enumerate(segs):
                    if a is None and pos + len(s[0]) > m.start():
                        a = k
                    pos += len(s[0])
                    if pos >= m.end():
                        merged = "".join(x[0] for x in segs[a:k + 1])
                        segs = segs[:a] + [[rx.sub(f["to"], merged, 1), segs[a][1]]] + segs[k + 1:]
                        hit = True
                        break
        if hit:
            f["_done"] = True
    return segs

def par_md(par, keep_hyphen, words, fixes=None):
    """Lines -> one markdown string: italics kept, line-end hyphens resolved."""
    out = []
    lines = par["lines"]
    for li, l in enumerate(lines):
        segs = [[r[0], r[1]] for r in l["runs"]]
        if fixes:
            segs = apply_fixes(segs, fixes)
        text = "".join(s[0] for s in segs)
        nxt = line_text(lines[li + 1]) if li + 1 < len(lines) else ""
        if text.rstrip().endswith("-") and nxt[:1].islower():
            head = re.search(r"([A-Za-z]+)-\s*$", text)
            tail = re.match(r"([a-z]+)", nxt)
            joined = (head.group(1) + tail.group(1)).lower() if head and tail else ""
            if joined and keep_hyphen.get(joined, 0) and not press_build.known(joined, words):
                sep = ""          # "self-" + "denial": keep the hyphen, no space
            else:
                # drop the hyphen: strip it from the last run
                for s in reversed(segs):
                    if s[0].rstrip():
                        s[0] = re.sub(r"-\s*$", "", s[0])
                        break
                sep = ""
        else:
            sep = " "
        out.append("".join(run_md(s[0], s[1]) for s in segs) + sep)
    md = "".join(out)
    md = re.sub(r"\*\*", "", md)                       # adjacent italic runs merge
    md = re.sub(r"\s+", " ", md).strip()
    md = re.sub(r"\s+([;:,?!.])(?=\s|$|\*)", r"\1", md)  # compositor's space before ; : , ? ! .
    for f in fixes or []:
        if not f.get("_done"):     # a misread split across a line end, rejoined above
            md, n = fix_rx(f).subn(f["to"], md)
            f["_done"] = n > 0
    return md

def convert(path, slug, e):
    src = e["source"]
    ident = src.get("ia") or json.load(open(os.path.join(HERE, f"{src['shelf']}_shelf.json"),
                                            encoding="utf-8"))["internet_archive"][src["volume"]][0]
    pages = press_abbyy.load(ident)
    a, b = src["leaves"]
    rng = pages[a:b + 1]
    bfs = body_size(rng)
    keep = collect_hyphenated(pages)
    words = press_build.wordlist()
    rules = press_build.load_rules(slug)
    fixes_by_leaf = {}
    all_fixes = []
    for f in rules.get("ocr_fixes", []):
        if not any(g["from"] == f["from"] and g["leaf"] == f["leaf"] for g in all_fixes):
            all_fixes.append(dict(f))
    for f in all_fixes:
        # the collation can place a word on the neighbouring leaf at a page
        # turn; a misread is never a real word, so the neighbours are safe
        for lf in (f["leaf"], f["leaf"] - 1, f["leaf"] + 1):
            fixes_by_leaf.setdefault(lf, []).append(f)
    d = Doc(slug)
    d.notes = {}
    started = not src.get("start")
    nnote = 0
    carry = None    # a paragraph broken by the page turn
    carry_leaf = None
    tp = src.get("titlepage") or {}
    if tp and tp["leaf"] < a:
        rng = [pages[tp["leaf"]]] + rng     # the title page stands before the treatise's leaves
    ended = False
    # the running heads read cleanly, to recognise the garbled ones
    clean = Counter(head_key(re.sub(r"\d", "", h)) for h in
                    (classify_page(p, bfs)[0] for p in rng) if h and re.search(r"\d", h))
    known_heads = [k for k, n in clean.most_common(8) if n >= 3 and len(k) >= 6]
    for page in rng:
        if ended:
            break
        if page["i"] == tp.get("leaf"):
            # the edition's own title page: every paragraph from `from` on is a
            # title-page line; nothing on it is a heading or a note
            pars = [p for p in page["pars"] if par_text(p).strip()]
            k0 = next((k for k, p in enumerate(pars) if re.search(tp["from"], par_text(p).strip())), None)
            if k0 is not None:
                # `until`: the title page stops at the paragraph that matches it
                k1 = next((k for k, p in enumerate(pars) if k > k0 and tp.get("until")
                           and re.search(tp["until"], par_text(p).strip())), len(pars))
                before, pars, after = pars[:k0], pars[k0:k1], pars[k1:]
                page = dict(page, pars=before + after)
                fixes = fixes_by_leaf.get(page["i"], [])
                d.blocks.append({"k": "titlepage_start", "section": "tp"})
                for p in pars:
                    md = par_md(p, keep, words, fixes)
                    if not re.search(r"[A-Za-z]{2}", md):
                        continue      # a rule or an ornament read as specks
                    # display lines by their form, not their measured size (a
                    # facsimile title page is reduced, and its sizes don't separate)
                    t = par_text(p).strip()
                    letters = re.sub(r"[^A-Za-z]", "", t)
                    cls = ("h2" if letters.isupper() and len(t) < 40 else
                           "h3" if len(t) < 60 else "h4")
                    d.blocks.append({"k": "tp", "md": md, "cls": cls, "section": "tp"})
                d.blocks.append({"k": "titlepage_end", "section": "tp"})
        n0 = len(d.blocks)
        from_leaf = carry_leaf if carry is not None else None
        head, body, notes = classify_page(page, bfs, known_heads)
        pn = printed_page(head)
        fixes = fixes_by_leaf.get(page["i"], [])
        anchor = f"[]{{#{slug}-p{re.sub(r'[^0-9A-Za-z]', '', pn or str(page['i']))} .pb n=\"{pn or ''}\" leaf=\"{page['i']}\"}}"
        page_notes = [par_md(n, keep, words, fixes) for n in notes]
        col = column(body)
        first_body = True
        took = False      # did any of this page's text go into the treatise?
        for par in body:
            raw = par_text(par).strip()
            if not started:
                if src.get("start") and re.search(src["start"], raw):
                    started = True
                else:
                    continue
            if src.get("end") and re.search(src["end"], raw) and page["i"] >= b - 1:
                started, ended = False, True
                break
            took = True
            md = par_md(par, keep, words, fixes)
            if not md:
                continue
            fs = par_fs(par)
            letters = re.sub(r"[^A-Za-z]", "", raw)
            # a heading is set in capitals, or in larger type and starting with a
            # capital over at least two words (a misread size never makes one
            # word a heading)
            is_head = (len(raw) < 140 and len(par["lines"]) <= 3 and
                       (len(letters) >= 3 or raw.strip(" .,").upper() in ("AN", "TO", "OR", "OF", "IN", "BY")) and
                       (letters.isupper() or (fs > bfs * 1.15 and raw.lstrip("*_")[:1].isupper()
                                              and len(raw.split()) >= 2)))
            sub = centred_italic(par, col) and len(letters) >= 3
            is_head = is_head and not sub
            words_n = len(raw.split())
            if is_head and col and words_n <= 4 and d.blocks and d.blocks[-1].get("k") == "para" \
                    and par["box"][0] > (col[0] + col[1]) / 2 - 0.05 * (col[1] - col[0]):
                # a name set right, after the text: the signature ("RICHARD BAXTER.")
                d.add("signature", md)
                continue
            if is_head or sub:
                if carry:
                    d.add("para", guard_start(tag_refs(carry, d))); carry = None
                if sub:
                    md = md.strip("*")    # the heading's own style replaces the italic
                prev = [x for x in d.blocks[-2:] if x.get("k") != "pb"]
                if not sub and prev and prev[-1].get("k") == "heading" and prev[-1]["level"] == 1 \
                        and d.blocks[-1].get("k") in ("heading", "pb") and len(prev[-1]["md"]) < 60 \
                        and not prev[-1]["md"].rstrip("*").endswith("."):
                    # a title set over several lines ("AN EPISTLE" / "TO THE" /
                    # "UNCONVERTED READER") is one heading
                    prev[-1]["md"] += " " + md
                else:
                    d.heading(md, level=2 if sub else 1)
                if first_body:
                    d.add("pb", anchor, n=pn or "", leaf=page["i"]); first_body = False
                continue
            if first_body:
                md = anchor + md
                first_body = False
            if carry is not None:
                if md.lstrip("[]{}#.").strip()[:1].islower() or re.search(r"[A-Za-z,;\-]$", carry):
                    md = carry + (" " if not carry.endswith("-") else "") + md
                    md = re.sub(r"(?<=[a-z])- (\[\]\{[^}]*\})?(?=[a-z])", lambda m: (m.group(1) or ""), md)
                else:
                    d.add("para", guard_start(tag_refs(carry, d)))
                carry = None
            if par is body[-1] and not re.search(r"[.!?:”’'\")\]]\*?$", md):
                carry, carry_leaf = md, page["i"]
            else:
                d.add("para", guard_start(tag_refs(md, d)))
        # which leaves each new paragraph stands on (a carried one spans two)
        for blk in d.blocks[n0:]:
            if blk.get("k") == "para" and "leaves" not in blk:
                blk["leaves"] = sorted({page["i"], from_leaf if from_leaf is not None else page["i"]})
                from_leaf = None
        # footnotes of this page (none from a page the treatise has not reached)
        calls = []
        if page_notes and took:
            for k, nmd in enumerate(page_notes):
                nnote += 1
                lab = f"n{nnote}"
                # the note's own mark ("\\* ", "† "), and nothing more: never an
                # italic's opening * ("*Ibid.*") nor the "1" of "1 Cor."
                d.notes[lab] = tag_refs(re.sub(r"^(?:\\[*^]|[†‡§‖¶•°])\s*", "", nmd).strip(), d)
                calls.append(lab)
            d.blocks.append({"k": "pagenotes", "labels": calls, "section": d.section, "leaf": page["i"],
                             "page": pn or "", "end_page": ended})
    if carry:
        d.add("para", guard_start(tag_refs(carry, d)))
        d.blocks[-1]["leaves"] = [carry_leaf]
    missed = [f for f in all_fixes if not f.get("_done")]
    if missed:
        d.problems.append(f"{len(missed)} OCR fix(es) found no match on their leaf: " +
                          "; ".join(f"{f['leaf']}:{f['from']!r}" for f in missed[:12]))
    attach_note_calls(d, ident)
    if d.nsec == 0:
        d.heading(esc(e["title"]))
    return d.out()

RE_CALL = re.compile(r"(?<=[A-Za-z.,;:’'”\)])(\\\*|\\\^|[†‡§‖¶•°¹²³⁴⁵⁶⁷⁸⁹])(?=[\s,.;:)]|$)")  # never an italic's *

RE_TESS_CALL = re.compile(r"([A-Za-z]{2,})([.,;:!?’')]{0,2}) ?([*†‡§])(?=\s|$)")

def tess_calls(ident, leaf):
    """Call marks the second engine saw on a page, as (word, punctuation):
    read from press_proof's cached Tesseract text, never fetched here."""
    p = os.path.join(press_abbyy.IA_DIR, "tess", ident or "", f"{leaf}.txt")
    if not ident or not os.path.exists(p):
        return []
    lines = open(p, encoding="utf-8").read().split("\n")
    out = []
    for ln in lines[1:]:                    # line 0 is the running head
        if re.match(r"\s*[*†‡§]", ln):        # the notes begin
            break
        out += [(m.group(1), m.group(2)) for m in RE_TESS_CALL.finditer(ln)]
    return out

def attach_note_calls(d, ident=None):
    """Pair each page's footnotes with the call marks in that page's text, in
    order, and only when the counts agree. Where ABBYY lost marks, the marks
    Tesseract saw are added first, each only where its word is unambiguous."""
    blocks = d.blocks
    for bi, b in enumerate(blocks):
        if b.get("k") != "pagenotes":
            continue
        # every paragraph standing on this leaf, including one carried over the
        # page turn (added after this block, when the next page completes it)
        paras = [j for j in range(len(blocks)) if blocks[j].get("k") == "para" and b["leaf"] in blocks[j].get("leaves", [])]
        saved = {pj: blocks[pj]["md"] for pj in paras}

        def on_page(pj, m, leaf=b["leaf"]):
            # a paragraph crossing a page turn: only the part on this leaf counts
            md = blocks[pj]["md"]
            a = md.find(f'leaf="{leaf}"}}')
            start = a if a >= 0 else 0
            nxt = re.search(r'leaf="(\d+)"\}', md[start + 1:])
            end = start + 1 + nxt.start() if nxt and int(nxt.group(1)) != leaf else len(md)
            if a < 0 and blocks[pj]["leaves"][0] != leaf:
                return False
            return start <= m.start() < end

        def calls():
            return [(pj, m) for pj in paras for m in RE_CALL.finditer(blocks[pj]["md"]) if on_page(pj, m)]
        hits = calls()
        if len(hits) < len(b["labels"]):
            for word, punct in tess_calls(ident, b["leaf"]):
                rx = re.compile(r"(?<![A-Za-z])" + re.escape(word) + re.escape(punct) + r"(?![A-Za-z\\\[])")
                where = [(pj, m) for pj in paras for m in rx.finditer(blocks[pj]["md"]) if on_page(pj, m)]
                if len(where) == 1:
                    pj, m = where[0]
                    md = blocks[pj]["md"]
                    blocks[pj]["md"] = md[:m.end()] + "\\*" + md[m.end():]
            hits = calls()
        if len(hits) == len(b["labels"]) and hits:
            # replace right to left so offsets hold
            for (pj, m), lab in reversed(list(zip(hits, b["labels"]))):
                md = blocks[pj]["md"]
                blocks[pj]["md"] = md[:m.start()] + f"[^{lab}]" + md[m.end():]
            b["placed"] = True
        else:
            for pj, md in saved.items():         # no pairing: take back what was added
                blocks[pj]["md"] = md
        if not b.get("placed") and paras:
            # The scan lost the call marks (both engines miss a superior * as
            # often as they see it), so the notes cannot be tied to a word.
            # They print where the page printed them: after the page's text,
            # marked as that page's notes, never guessed into a sentence.
            if b.get("end_page"):
                d.problems.append(f"leaf {b['leaf']}: the treatise ends on this page; {len(b['labels'])} "
                                  "unplaced note(s) there may belong to what follows")
            blocks[bi] = {"k": "pagefoot", "page": b.get("page", ""),
                          "notes": [d.notes.pop(lab) for lab in b["labels"]]}
    d.blocks = [x for x in blocks if x.get("k") != "pagenotes"]

def heads(ident):
    pages = press_abbyy.load(ident)
    bfs = body_size(pages)
    for p in pages:
        h, body, notes = classify_page(p, bfs)
        first = par_text(body[0])[:70] if body else ""
        print(p["i"], "|", (h or "")[:60], "|", first if not h or len(body) < 3 else "")

if __name__ == "__main__":
    if sys.argv[1] == "--heads":
        heads(sys.argv[2])
    elif sys.argv[1] == "--page":
        pages = press_abbyy.load(sys.argv[2])
        p = pages[int(sys.argv[3])]
        h, body, notes = classify_page(p, body_size(pages))
        print("HEAD:", h)
        for x in body:
            print("BODY:", par_text(x)[:200])
        for x in notes:
            print("NOTE:", par_text(x)[:200])
