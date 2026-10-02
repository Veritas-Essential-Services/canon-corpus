#!/usr/bin/env python3
"""Nesting-aware prose converter: Book > Part > Chapter (or any depth).

structure_texts.convert_gutenberg_prose keeps ONE running heading, so a book
whose chapters restart inside each part (Pyle's King Arthur: "The Book of
Three Worthies" > "PART II" > "Chapter First") repeats "Chapter First" a dozen
times and its unit ids only stay unique through `~n` suffixes, which no reader
can cite. Here each heading level is its own regex; a heading sets its level,
clears every deeper level and restarts the paragraph count, and the citation
is the whole path:

    The Book of Three Worthies / PART II The Winning of a Sword / Chapter First, par. 3

Called by convert_shelf_gutenberg.py when a shelf row carries
{"levels": [{"re": "<regex>", "title_next": true}, ...]}, outermost first, and
optionally "start": "<regex>" -- the first paragraph matching it begins the
body, and every heading read before it (a Contents list) is forgotten.
"title_next" folds the next short paragraph into that heading (a part number
followed by its name). "strip": "<regex>" removes matches from that level's
heading text (a footnote mark printed on a title, "THE FIEND.[18]"); "max": n
lets that level's headings run past the default 90 characters (a long title).
Illustration placeholders are removed before matching
and never become units. Same output contract as convert_gutenberg_prose
({id, ref, text, links[]}); structure_texts.py is imported, not modified.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from structure_texts import strip_boilerplate, apply_body_rules, sha256, CORPUS

RE_ILLUS = re.compile(r"\[Illustration[^\]]*\]", re.S)

def convert_nested(path, slug, title, author, levels, start=None):
    raw = strip_boilerplate(open(path, encoding="utf-8", errors="replace").read())
    raw, apparatus_note = apply_body_rules(raw, slug)
    raw = RE_ILLUS.sub("", raw)
    LV = [(re.compile(l["re"]), bool(l.get("title_next"))) for l in levels]
    MAX = [int(l.get("max", 90)) for l in levels]
    STRIP = [re.compile(l["strip"]) if l.get("strip") else None for l in levels]
    heads = [None] * len(LV)
    units, pnum, pending_title = [], 0, None
    START = re.compile(start) if start else None
    for para in re.split(r"\n\s*\n", raw):
        p = re.sub(r"\s+", " ", para).strip()
        if not p:
            continue
        if START and START.match(p):   # body begins: forget headings read from the Contents
            heads, START = [None] * len(LV), None
        if pending_title is not None and len(p) < 90:
            heads[pending_title] = f"{heads[pending_title]} {p.rstrip('.')}"
            pending_title = None
            continue
        pending_title = None
        hit = next((i for i, (rx, _) in enumerate(LV) if len(p) < MAX[i] and rx.match(p)), None)
        if hit is not None:
            heads[hit] = (STRIP[hit].sub("", p) if STRIP[hit] else p).rstrip(".")
            for j in range(hit + 1, len(heads)):
                heads[j] = None
            pnum = 0
            if LV[hit][1]:
                pending_title = hit
            continue
        pnum += 1
        path_ = [h for h in heads if h]
        ref = (" / ".join(path_) + f", par. {pnum}") if path_ else f"par. {pnum}"
        key = ".".join(h.replace(" ", "_") for h in path_) or "x"
        units.append({"id": f"{slug}:{key}.{pnum}", "ref": ref, "text": p, "links": []})
    return {"slug": slug, "title": title, "author": author,
            "source": {"path": os.path.relpath(path, CORPUS), "format": "gutenberg-txt",
                       "sha256": sha256(path)},
            "scheme": {"apparatus": apparatus_note, "citation": "heading path + paragraph",
                       "resolution": "paragraph",
                       "honesty": f"{len(LV)} nested heading levels detected by per-book rules; "
                                  "paragraph running within the innermost heading"},
            "units": units}
