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
    the notes can be paired one-to-one; otherwise the notes print after the
    chapter (honestly unplaced) and the QA counts them
  - rejoins a word hyphenated across a line end, unless the volume itself
    prints that word hyphenated elsewhere (so "self-denial" stays)
  - rejoins a paragraph broken by a page turn
  - removes the space 19th-century compositors set before ; : ? ! and ,
  - keeps italics (scripture quoted in italic stays italic)
  - applies the book's OCR corrections (pipeline/press_rules/<slug>.json
    "ocr_fixes", each tied to a leaf, from press_proof's two-engine collation)
Spelling, capitals and punctuation are otherwise the printed page's.
"""
import json, os, re, statistics, sys
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

RE_HEAD_NUM = re.compile(r"^\W{0,2}[\dSOlIoJ][\dSOlIoJ ]{0,4}\W{0,2}\s|\s\W{0,2}[\dSOlIoJ][\dSOlIoJ ]{0,4}\W{0,2}$")
RE_SIGNATURE = re.compile(r"^(VOL\.?|Vol\.?|VOI\.)\s*[IVXL1]+\.?\s*[A-Z2-9]{0,3}\.?$")

def classify_page(page, body_fs):
    """-> (running_head_text or None, body pars, note pars)"""
    pars = [p for p in page["pars"] if par_text(p).strip()]
    head = None
    if pars:
        p0 = pars[0]
        t0 = par_text(p0).strip()
        top = p0["box"][1] < page["h"] * 0.12 if page["h"] else True
        if top and len(p0["lines"]) == 1 and (RE_HEAD_NUM.search(t0) or (t0.isupper() and len(t0) < 70)):
            head = t0
            pars = pars[1:]
    while pars and RE_SIGNATURE.match(par_text(pars[-1]).strip()):
        pars = pars[:-1]
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

def par_md(par, keep_hyphen, words, fixes=None):
    """Lines -> one markdown string: italics kept, line-end hyphens resolved."""
    out = []
    lines = par["lines"]
    for li, l in enumerate(lines):
        segs = [[r[0], r[1]] for r in l["runs"]]
        if fixes:
            for f in fixes:
                for s in segs:
                    if f["from"] in s[0] and not f.get("_done"):
                        s[0] = s[0].replace(f["from"], f["to"], 1)
                        f["_done"] = True
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
    for f in rules.get("ocr_fixes", []):
        fixes_by_leaf.setdefault(f["leaf"], []).append(dict(f))
    d = Doc(slug)
    d.notes = {}
    started = not src.get("start")
    nnote = 0
    carry = None    # a paragraph broken by the page turn
    for page in rng:
        head, body, notes = classify_page(page, bfs)
        pn = printed_page(head)
        fixes = fixes_by_leaf.get(page["i"], [])
        anchor = f"[]{{#{slug}-p{re.sub(r'[^0-9A-Za-z]', '', pn or str(page['i']))} .pb n=\"{pn or ''}\" leaf=\"{page['i']}\"}}"
        page_notes = [par_md(n, keep, words, fixes) for n in notes]
        first_body = True
        for par in body:
            raw = par_text(par).strip()
            if not started:
                if re.search(src["start"], raw):
                    started = True
                else:
                    continue
            if src.get("end") and re.search(src["end"], raw) and page["i"] >= b - 1:
                started = False
                break
            md = par_md(par, keep, words, fixes)
            if not md:
                continue
            fs = par_fs(par)
            letters = re.sub(r"[^A-Za-z]", "", raw)
            is_head = (len(raw) < 140 and len(par["lines"]) <= 3 and letters and
                       (letters.isupper() or fs > bfs * 1.15))
            if is_head:
                if carry:
                    d.add("para", guard_start(tag_refs(carry, d))); carry = None
                d.heading(md, level=1)
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
                carry = md
            else:
                d.add("para", guard_start(tag_refs(md, d)))
        # footnotes of this page
        calls = []
        if page_notes:
            for k, nmd in enumerate(page_notes):
                nnote += 1
                lab = f"n{nnote}"
                d.notes[lab] = tag_refs(re.sub(r"^[" + re.escape(NOTE_MARKS) + r"\d\s]{1,3}", "", nmd).strip(), d)
                calls.append(lab)
            d.blocks.append({"k": "pagenotes", "labels": calls, "section": d.section, "leaf": page["i"]})
    if carry:
        d.add("para", guard_start(tag_refs(carry, d)))
    attach_note_calls(d)
    if d.nsec == 0:
        d.heading(esc(e["title"]))
    return d.out()

RE_CALL = re.compile(r"(?<=[A-Za-z.,;:’'”\)])([" + re.escape(esc(NOTE_MARKS)) + r"]|\\\*|\\\^|[¹²³⁴⁵⁶⁷⁸⁹])(?=[\s,.;:)]|$)")

def attach_note_calls(d):
    """Pair each page's footnotes with the call marks in that page's text,
    in order; pairing only when the counts agree."""
    blocks = d.blocks
    for bi, b in enumerate(blocks):
        if b.get("k") != "pagenotes":
            continue
        # the paragraphs of the same page: back to the previous pagenotes block
        j = bi - 1
        paras = []
        while j >= 0 and blocks[j].get("k") != "pagenotes":
            if blocks[j].get("k") == "para":
                paras.insert(0, j)
            j -= 1
        hits = [(pj, m) for pj in paras for m in RE_CALL.finditer(blocks[pj]["md"])]
        if len(hits) == len(b["labels"]) and hits:
            # replace right to left so offsets hold
            for (pj, m), lab in reversed(list(zip(hits, b["labels"]))):
                md = blocks[pj]["md"]
                blocks[pj]["md"] = md[:m.start()] + f"[^{lab}]" + md[m.end():]
            b["placed"] = True
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
