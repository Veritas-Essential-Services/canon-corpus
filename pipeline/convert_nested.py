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
heading text, and from a title folded in by "title_next" (a footnote mark
printed on a title, "THE FIEND.[18]"); "max": n
lets that level's headings run past the default 90 characters (a long title);
"label": {"<regex>": "<name>"} cites a heading matching <regex> by a fixed
name instead of the paragraph itself, and "keep": true also keeps such a
labelled paragraph as that level's first unit (a poem's text has no heading;
its stanza 1 marks where it begins, and is itself text); "number_repeats": true
cites the second and later headings of the same name under the same parent as
"<name> (2)", "(3)" (two different tales printed under one title, "Koshchéi
Without-Death" twice in Curtin's Russian tales), so their paragraphs neither
collide nor run on as one tale. A heading is counted only once a paragraph is
cited under it, so a Contents list of bare headings (with or without a
"start") uses up no number. With "front": true
and a "start", nothing before the start is read as a heading: a Contents that
repeats the chapter headings would otherwise file the front matter under the
last chapter it lists. Front matter is cited "front, par. n".
Illustration placeholders are removed before matching
and never become units, except that "caption": true on a level first turns an
illustration whose caption matches that level's regex into a plain paragraph
(a book that prints each story's title only on its headpiece plate). Same output contract as convert_gutenberg_prose
({id, ref, text, links[]}); structure_texts.py is imported, not modified.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from structure_texts import strip_boilerplate, apply_body_rules, sha256, CORPUS

RE_ILLUS = re.compile(r"\[Illustration[^\]]*\]", re.S)

def convert_nested(path, slug, title, author, levels, start=None, front=False):
    raw = strip_boilerplate(open(path, encoding="utf-8", errors="replace").read())
    raw, apparatus_note = apply_body_rules(raw, slug)
    for l in levels:
        if l.get("caption"):
            rx_ = re.compile(l["re"])
            def _cap(m, rx_=rx_):
                c = re.sub(r"\s+", " ", m.group(0)[len("[Illustration:"):-1]).strip()
                return f"\n\n{c}\n\n" if rx_.match(c) else m.group(0)
            raw = RE_ILLUS.sub(_cap, raw)
    raw = RE_ILLUS.sub("", raw)
    LV = [(re.compile(l["re"]), bool(l.get("title_next"))) for l in levels]
    MAX = [int(l.get("max", 90)) for l in levels]
    LABEL = [[(re.compile(k), v) for k, v in (l.get("label") or {}).items()] for l in levels]
    KEEP = [bool(l.get("keep")) for l in levels]
    STRIP = [re.compile(l["strip"]) if l.get("strip") else None for l in levels]
    NUMBER = [bool(l.get("number_repeats")) for l in levels]
    seen_heads = {}                    # (level, parent path, name) -> times seen
    to_number = set()                  # number_repeats levels whose new heading holds no text yet
    heads = [None] * len(LV)
    units, pnum, pending_title = [], 0, None
    START = re.compile(start) if start else None
    for para in re.split(r"\n\s*\n", raw):
        p = re.sub(r"\s+", " ", para).strip()
        if not p:
            continue
        if START and START.match(p):   # body begins: forget headings read from the Contents
            heads, START = [None] * len(LV), None
            pending_title = None       # ...and a title the Contents' last heading was waiting for
            seen_heads, to_number = {}, set()   # ...and which names the Contents already used
            if front:
                pnum = 0
        elif START and front:          # front matter: no headings until the body begins
            pnum += 1
            units.append({"id": f"{slug}:front.{pnum}", "ref": f"front, par. {pnum}", "text": p, "links": []})
            continue
        if pending_title is not None and len(p) < 90:
            t_ = STRIP[pending_title].sub("", p) if STRIP[pending_title] else p
            heads[pending_title] = f"{heads[pending_title]} {t_.rstrip('.')}"
            pending_title = None
            continue
        pending_title = None
        hit = next((i for i, (rx, _) in enumerate(LV) if len(p) < MAX[i] and rx.match(p)), None)
        if hit is not None:
            lab = next((v for k, v in LABEL[hit] if k.match(p)), None)
            heads[hit] = lab or (STRIP[hit].sub("", p) if STRIP[hit] else p).rstrip(".")
            for j in range(hit + 1, len(heads)):
                heads[j] = None
            if NUMBER[hit]:
                to_number.add(hit)     # counted at its first unit, not here
            pnum = 0
            if LV[hit][1]:
                pending_title = hit
            if not (KEEP[hit] and lab):
                continue
        for lv in sorted(to_number):   # a heading is counted once it holds text, so a
            k_ = (lv, tuple(heads[:lv]), heads[lv])   # Contents list (headings, no text) uses up no number
            seen_heads[k_] = seen_heads.get(k_, 0) + 1
            if seen_heads[k_] > 1:
                heads[lv] = f"{heads[lv]} ({seen_heads[k_]})"
        to_number = set()
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
