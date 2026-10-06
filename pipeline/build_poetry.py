#!/usr/bin/env python3
# prov: 2026-10-06 claude-opus-5-5 drafted
# fable_review: pending
"""
build_poetry.py -- the Word Hoard poetry section: AmblesideOnline's poetry
selections, and the house's heroic addendum beside them, as one catalog and
as Mnemonicon memory packs a child can bank straight into memory work.

    python3 pipeline/build_poetry.py --fetch    # fetch the pinned Gutenberg books (resumable)
    python3 pipeline/build_poetry.py            # build, mint once, write
    python3 pipeline/build_poetry.py --check    # rebuild, assert 0 minted and byte-identical
    python3 pipeline/build_poetry.py --report   # print the extraction table; write nothing

    Input:  data/poetry/selections/ao.jsonl               (AO's schedule, curated)
            data/poetry/selections/addendum-heroic.jsonl  (the house's proposals, curated)
            data/poetry/sources.json                      (the Gutenberg books, pinned by sha256)
            data/corpus/gitenberg/<n>.txt                 (fetched; gitignored)
    Output: data/poetry/catalog-ao.jsonl                  (COMMITTED)
            data/poetry/catalog-addendum-heroic.jsonl     (COMMITTED)
            data/poetry/texts.jsonl                       (COMMITTED; public domain only)
            exports/mnemonicon/poetry/<pack>.json         (COMMITTED; one per year and term)
    Tests:  tests/poetry_test.py

TWO LAYERS, ONE SHAPE
    A selection row says WHERE a poem sits (layer, year, term, order) and WHAT
    it is (poet, title, first publication, the public-domain book that holds
    it). The AO layer is AmblesideOnline's schedule as AO prints it; the
    addendum is the house's own proposal set (heroic, adventurous, vocational
    verse), tagged `addendum-heroic`, with the same year/term slots so it sits
    beside the AO list without mixing into it. A poem in both layers is ONE
    poem: one citation, one uid, one Mnemonicon piece id.

THE RIGHTS RULE (US, as of 1 January 2026)
    Copyright follows the edition, not the poet's death (ADR 0001). So the
    test is the TEXT WE HOST: if it comes from a book published before 1931,
    its US term has run out (95 years from publication) and the house hosts it
    in full. Anything else is linked out, never hosted:
      pd           text from a pre-1931 printing           -> host: full
      in-copyright first published 1931 or later           -> host: link
      uncertain    no pre-1931 printing found, or a fact
                   we could not establish                  -> host: link
    Each row carries the reasoning in words (`rights.basis`), and a second
    line for readers outside the US (`rights.elsewhere`): in life+70
    countries a poet who died after 1955 is still in copyright there.
    The Gutenberg header is read too: a "COPYRIGHTED Project Gutenberg
    eBook" is refused outright (the Kafka rule, CLAUDE.md 2026-07-26).

THE TEXT
    Never typed, never pasted: every hosted text is cut by this script from a
    pinned Project Gutenberg file (sha256 in sources.json), between the poem's
    heading and the next heading, with per-book rules where the book needs
    them (`extract` in the selection row). A text that cannot be found is not
    guessed at: the row drops to `host: link` and says why.

THE PACKS
    The Mnemonicon's own import format (see export_mnemonicon_pack.py): a JSON
    array of whole pieces. id = uuid5 of the poem's wh-uid, in the same
    namespace as the hymn packs, so a re-import adds nothing and a poem in two
    packs is one piece. Category "Poetry" (a song: "Song").
"""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "poetry")
SEL = os.path.join(DATA, "selections")
CORPUS = os.path.join(ROOT, "data", "corpus", "gitenberg")
PACKS = os.path.join(ROOT, "exports", "mnemonicon", "poetry")
UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")

sys.path.insert(0, HERE)
import wh_uid as U  # noqa: E402

_spec = importlib.util.spec_from_file_location("export_mnemonicon_pack", os.path.join(HERE, "export_mnemonicon_pack.py"))
_X = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_X)
NAMESPACE = _X.NAMESPACE          # one namespace for every Word Hoard piece: never change it

LAYERS = ("ao", "addendum-heroic")
AS_OF = 2026                      # the year the rights rule is computed for
PD_BEFORE = AS_OF - 95            # published before this year: US public domain
LIFE70_BEFORE = AS_OF - 70        # died before this year: out of copyright in life+70 countries
CUT_ON = "2026-10-06"             # the packs' createdAt/due; keeps them byte-identical
LONG = 120                        # a hosted poem longer than this is split into parts
PART = 40                         # a part holds at most about this many lines


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def read_jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def jsonl(rows):
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows).encode("utf-8")


def write_atomic(path, blob):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(blob)
    os.replace(tmp, path)


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower().replace("&", " and ")
    s = re.sub(r"[’'`]", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def norm(s):
    """A title as compared: case, accents, punctuation and a leading article
    or roman numeral don't count."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[’'`]", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    s = re.sub(r"^(?:[ivxlc]+|\d+)\s+(?=\D)", "", s)
    return s


def citation(row):
    """poetry:<poet>.<title> -- the address; the uid is the identity."""
    v = f".{row['variant']}" if row.get("variant") else ""   # a second poem of one title in one term
    return f"poetry:{slug(row['poet'])}.{slug(row['title'])}{v}"


def gutenberg_url(n):
    return f"https://www.gutenberg.org/ebooks/{n}"


# ---------------------------------------------------------------------------
# Sources: fetch and pin
# ---------------------------------------------------------------------------

def load_sources():
    with open(os.path.join(DATA, "sources.json"), encoding="utf-8") as f:
        return json.load(f)


def book_path(n):
    return os.path.join(CORPUS, f"{n}.txt")


def fetch(sources):
    os.makedirs(CORPUS, exist_ok=True)
    bad = []
    for n, s in sorted(sources["books"].items(), key=lambda kv: int(kv[0])):
        p = book_path(n)
        if os.path.exists(p):
            continue
        try:
            with urllib.request.urlopen(s["raw_url"], timeout=60) as r:
                blob = r.read()
        except Exception as e:  # noqa: BLE001 -- report and carry on; resumable
            bad.append((n, str(e)))
            continue
        write_atomic(p, blob)
        print(f"  fetched {n:>6}  {len(blob):>9,} bytes  {s['title']}")
    for n, e in bad:
        print(f"  FAILED  {n}: {e}")
    return not bad


def read_book(n, src):
    """The book's text between the Gutenberg START and END lines, after the
    rights checks. Refuses a copyrighted eBook and a file that is not the
    pinned one."""
    p = book_path(n)
    if not os.path.exists(p):
        return None, "not fetched (run --fetch)"
    blob = open(p, "rb").read()
    sha = hashlib.sha256(blob).hexdigest()
    if src.get("sha256") and src["sha256"] != sha:
        return None, f"sha256 {sha[:12]} is not the pinned {src['sha256'][:12]}"
    text = blob.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
    head = text[:6000]
    if re.search(r"COPYRIGHTED\s+PROJECT\s+GUTENBERG", head, re.I):
        return None, "the Gutenberg header says COPYRIGHTED: refused"
    m1 = re.search(r"^\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG.*$", text, re.M | re.I)
    m2 = re.search(r"^\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG.*$", text, re.M | re.I)
    if m1 and m2:
        text = text[m1.end():m2.start()]
    return text.split("\n"), sha


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def _clean_heading(line):
    s = line.strip()
    s = re.sub(r"^\[?(?:[IVXLC]+|\d+)[.:)\]]?\s+", "", s)     # "XIV. Where go the boats?"
    s = re.sub(r"\s*\[\d+(?::\d+)?\]", "", s)                     # footnote anchors, [3] or [491:1]
    return norm(s)


def find_heading(lines, title, start_after=0, occurrence=None):
    """Indexes of lines that are this poem's heading. A heading stands alone:
    a blank line (or the file's start) above it."""
    want = norm(title)
    hits = []
    for i in range(start_after, len(lines)):
        if not lines[i].strip() or len(lines[i].strip()) > 120:
            continue
        if _clean_heading(lines[i]) != want:
            continue
        if i > 0 and lines[i - 1].strip() and not re.match(r"^\s*(?:[IVXLC]+|\d+)\.?\s*$", lines[i - 1]):
            continue
        hits.append(i)
    return hits


def _is_body_start(lines, i):
    """A poem body begins at a non-blank line; skip epigraph-ish bracketed notes? no -- keep everything."""
    return bool(lines[i].strip())


def extract(lines, title, rule=None):
    """Return (text, how) or (None, why). The heading is the LAST standalone
    occurrence of the title that is followed by verse (so the contents page,
    which lists titles one under another, never wins), unless the rule says
    otherwise. The body ends at the first run of `gap` blank lines (default 2)
    that is followed by something that is not more of the poem, or at a rule's
    `end` pattern."""
    rule = rule or {}
    start_after = 0
    if rule.get("after"):
        for i, l in enumerate(lines):
            if re.search(rule["after"], l):
                start_after = i + 1
                break
    if rule.get("first_line"):                 # an untitled poem: it begins at its first line
        fl = re.compile(rule["first_line"])
        found = [i for i in range(start_after, len(lines)) if fl.search(lines[i])]
        if not found:
            return None, f"first line {rule['first_line']!r} not found"
        return _body(lines, found[rule.get("occurrence", 0)], rule, found[rule.get("occurrence", 0)])
    hits = find_heading(lines, rule.get("heading") or title, start_after)
    if not hits:
        return None, f"heading {rule.get('heading') or title!r} not found"
    cands = [h for h in hits if not _in_contents(lines, h)]
    # a poem whose first line repeats its title: the heading wins, the line stays in the poem
    cands = [h for k, h in enumerate(cands) if not (k and h - cands[k - 1] <= 3)]
    if not cands:
        return None, f"heading {title!r} found only in a contents list"
    if rule.get("occurrence") is not None:
        cands = [cands[rule["occurrence"]]]
    # the last occurrence that yields verse: a contents page or an editor's
    # introduction comes before the poem, never after it
    best = None
    for h in reversed(cands):
        i = h + 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        text, how = _body(lines, i, rule, h)
        if text and _prose(text) and not rule.get("prose_ok"):
            text, how = None, "what follows the heading is prose, not verse"
        if text and (text.count("\n") + 1 >= 2 or rule.get("short")):
            return text, how
        best = best or (text, how)
    return best if best and best[0] else (None, "no verse follows the heading")


def _in_contents(lines, h):
    """Is the heading at h an entry in a contents list? Then most of the next
    few lines are entries too: short, heading-like, or ending in a page number."""
    nxt = [l for l in lines[h + 1:h + 14] if l.strip()][:5]
    if len(nxt) < 3:
        return False
    entry = sum(1 for l in nxt if _is_heading(l) or re.search(r"\s\d+\s*$", l)
                or re.search(r"\.{3,}", l))
    return entry >= 4


def _prose(text):
    """Wrapped prose, not verse: long lines, many of them starting mid-sentence."""
    ls = [l.strip() for l in text.split("\n") if l.strip()]
    if len(ls) < 4:
        return False
    lower = sum(1 for l in ls if l[0].islower())
    avg = sum(len(l) for l in ls) / len(ls)
    return avg > 52 and lower / len(ls) > 0.3


NUMERAL = re.compile(r"\s*(?:[IVXLC]+|\d+)\.?\s*$")


def _next_section(lines, j):
    """After a gap: is what follows a numbered part of the same poem (a bare
    numeral, then verse), rather than the next poem (a numeral, then a title)?"""
    nxt = [k for k in range(j + 1, min(j + 12, len(lines))) if lines[k].strip()][:2]
    if len(nxt) < 2 or not NUMERAL.fullmatch(lines[nxt[0]]):
        return False
    after = lines[nxt[1]]
    return not _is_heading(after) and not NUMERAL.fullmatch(after) and not after.lstrip().startswith("[")


def _is_note(block):
    """An editor's line between a heading and its poem ("First printed in 1830.")."""
    text = " ".join(l.strip() for l in block if l.strip())
    return bool(text) and len(block) <= 3 and bool(
        re.search(r"\b(?:printed|published|written|composed|reprinted|text of|edition)\b", text, re.I))


def _is_heading(line):
    """A line that opens the next poem: short, and set in capitals (or a bare
    section numeral)."""
    t = line.strip()
    if not t or len(t) > 80:
        return False
    letters = re.sub(r"[^A-Za-z]", "", t)
    return len(letters) >= 3 and letters.upper() == letters


def _body(lines, i, rule, h):
    skip = rule.get("skip", 0)                # lines after the heading that are not the poem (a dedication)
    i += skip
    while i < len(lines) and not lines[i].strip():
        i += 1
    gap = rule.get("gap", 2)
    end_re = re.compile(rule["end"]) if rule.get("end") else None
    body, blanks = [], 0
    j = i
    while j < len(lines):
        l = lines[j]
        if end_re and end_re.search(l):
            break
        if re.match(r"^\s*\[(?:Illustration|Footnote|Sidenote)", l, re.I):
            while j < len(lines) and not lines[j].rstrip().endswith("]"):
                j += 1                         # a caption block, however many lines: not the poem
            j += 1
            while j < len(lines) and not lines[j].strip():
                j += 1                         # nor the blank lines around it: invisible, not a break
            continue
        if not l.strip():
            blanks += 1
            if blanks >= gap:
                if _is_note(body):             # an editor's note, not the poem: go on past it
                    body, blanks = [], 0
                    j += 1
                    continue
                if body and rule.get("parts") and _next_section(lines, j):
                    j += 1                     # "2" after a gap, then verse: the poem's next part
                    continue
                break
        elif re.fullmatch(r"\s*(?:[IVXLC]+|\d+)\.?\s*", l):
            if body and body[-1] != "":        # a stanza or section number: a break, not text
                body.append("")
            blanks = 0
        elif blanks and body and not rule.get("keep_headings") and _is_heading(l):
            break                              # the next poem's heading after a single blank line
        else:
            if blanks and body and body[-1] != "":
                body.append("")
            blanks = 0
            body.append(l.rstrip())
        j += 1
    while body and not body[-1].strip():
        body.pop()
    if rule.get("max_stanzas"):
        out, n = [], 0
        for l in body:
            if not l:
                n += 1
                if n >= rule["max_stanzas"]:
                    break
            out.append(l)
        body = out
    if rule.get("trim"):                       # a per-book stray: an attribution run onto a line, a gloss mark
        body = [re.sub(rule["trim"], "", l) for l in body]
    body = _tidy(body, rule)
    if not body:
        return None, "empty body"
    return "\n".join(body), f"line {h + 1}"


def _tidy(body, rule):
    """Dedent to the poem's own left margin (keep relative indents); drop
    Gutenberg's [Illustration] lines and footnote anchors; underscores that
    mark italics are removed."""
    out = []
    for l in body:
        if re.match(r"^\s*\[(?:Illustration|Footnote|Sidenote)[^\]]*\]?\s*$", l, re.I):
            continue
        if re.fullmatch(r"\s*\{\d+\}\s*", l):
            continue                                                  # a page number, {17}
        l = re.sub(r"\[(?:\d+(?::\d+)?|[A-Z]|[a-z]{1,3}|[ivxlc]{1,6})\]", "", l)  # anchors: [3] [491:1] [A] [mq] [viii]
        l = re.sub(r"\{\d+\}", "", l)
        l = re.sub(r"(\S)\s{3,}\d{1,4}\s*$", r"\1", l)              # an editor's margin line number
        l = l.replace("_", "")
        out.append(l)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    # collapse doubled blank lines left by removed lines
    tidy = []
    for l in out:
        if not l.strip() and tidy and not tidy[-1].strip():
            continue
        tidy.append(l)
    indents = [len(l) - len(l.lstrip()) for l in tidy if l.strip()]
    m = min(indents) if indents else 0
    return [l[m:].rstrip() if l.strip() else "" for l in tidy]


# ---------------------------------------------------------------------------
# Rights
# ---------------------------------------------------------------------------

def rights(row, src, text_ok, why):
    fp = row.get("first_pub") or {}
    fy = fp.get("year")
    died = row.get("poet_died")
    ps = row.get("pd_source") or {}
    ey = ps.get("edition_year")
    if died and died >= LIFE70_BEFORE:
        elsewhere = (f"{row['poet']} died {died}: in countries that count life + 70 years "
                     f"(UK, EU, Canada since 2022, Australia) this is in copyright until "
                     f"1 January {died + 71}. Hosted here under US law only.")
    elif died:
        elsewhere = f"{row['poet']} died {died}: out of copyright in life + 70 countries too."
    else:
        elsewhere = "Poet's death year not recorded; check before relying on it outside the US."

    pg = f"Project Gutenberg #{ps['gutenberg']}" if ps.get("gutenberg") else None
    first = (f" First published {fy}" + (f" in {fp['work']}" if fp.get("work") else "") + ".") if fy else ""
    if pg and text_ok and ey and ey < PD_BEFORE:
        basis = (f"US public domain: the text hosted here is from {ps['work']} ({ey}), "
                 f"published before {PD_BEFORE}, so its 95-year US term has run out. {pg}.")
        if fy and fy != ey:
            basis += first
        return {"us": "pd", "basis": basis, "elsewhere": elsewhere}, "full"
    if pg and text_ok and not ey and fy and fy < PD_BEFORE:
        basis = (f"US public domain: first published {fy}" + (f" in {fp['work']}" if fp.get("work") else "")
                 + f", before {PD_BEFORE}. The text is from {ps['work']}, {pg}, which Gutenberg issues as "
                 f"US public domain (no copyright notice in its header); the file does not date its edition.")
        return {"us": "pd", "basis": basis, "elsewhere": elsewhere}, "full"
    if pg and text_ok and not ey and not fy and died and died < PD_BEFORE:
        basis = (f"US public domain: {row['poet']} died in {died}, before {PD_BEFORE}, and the text is from "
                 f"{ps['work']}, {pg}, which Gutenberg issues as US public domain (no copyright notice in its "
                 f"header). First publication date not recorded; the edition is undated in the file.")
        return {"us": "pd", "basis": basis, "elsewhere": elsewhere}, "full"
    if fy and fy >= PD_BEFORE:
        basis = (f"In copyright in the US: first published {fy}" + (f" ({fp['work']})" if fp.get("work") else "")
                 + f", within 95 years. Linked out, not hosted.")
        return {"us": "in-copyright", "basis": basis, "elsewhere": elsewhere}, "link"
    if ps.get("gutenberg") and ey and ey < PD_BEFORE:
        basis = (f"US public domain: {ps['work']} ({ey}), Project Gutenberg #{ps['gutenberg']}, was published "
                 f"before {PD_BEFORE}. Not hosted yet: the text has not been cut from a pinned copy"
                 + (f" ({why})" if why else "") + ". Linked out until it is.")
        return {"us": "pd", "basis": basis, "elsewhere": elsewhere}, "link"
    if fy and fy < PD_BEFORE:
        basis = (f"US public domain: first published {fy}" + (f" ({fp['work']})" if fp.get("work") else "")
                 + f", before {PD_BEFORE}. Not hosted yet: no public-domain printing of the text has been "
                 f"pinned as a source" + (f" ({why})" if why else "") + ". Linked out until one is.")
        return {"us": "pd", "basis": basis, "elsewhere": elsewhere}, "link"
    basis = ("Uncertain: first publication not established" + (f"; {why}" if why else "")
             + ". Linked out, not hosted.")
    return {"us": "uncertain", "basis": basis, "elsewhere": elsewhere}, "link"


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def pack_name(row):
    if row["layer"] == "ao":
        y = row["year"]
        y = f"y{int(y):02d}" if str(y).isdigit() else str(y)
        t = f"-t{row['term']}" if row.get("term") else ""
        return f"ao-{y}{t}"
    return f"heroic-y{int(row['year']):02d}-t{row['term']}"


def tags_for(row):
    t = ["poetry", row["layer"]]
    y = str(row["year"])
    if row["layer"] == "ao":
        yt = f"ao-y{y}"
        t.append(yt)
        if row.get("term"):
            t.append(f"{yt}-t{row['term']}")
    else:
        t.append(row.get("kind") or "heroic")
        t.append(f"year-{y}")
    t.append(slug(row["poet"]))
    return [x.lower() for x in t]


def split_parts(text):
    """A long poem as parts of whole stanzas, about PART lines each."""
    stanzas = []
    for s in (s for s in text.split("\n\n") if s.strip()):
        ls = s.split("\n")
        while len(ls) > PART + 10:             # a verse paragraph too long to bank whole:
            cut = max((k for k in range(PART // 2, PART + 1) if re.search(r"[.;!?]['\u2019\"]?$", ls[k - 1])),
                      default=PART)            # break after a sentence near PART lines
            stanzas.append("\n".join(ls[:cut]))
            ls = ls[cut:]
        stanzas.append("\n".join(ls))
    parts, cur, n = [], [], 0
    for s in stanzas:
        k = s.count("\n") + 1
        if cur and n + k > PART:
            parts.append(cur)
            cur, n = [], 0
        cur.append(s)
        n += k
    if cur:
        parts.append(cur)
    return ["\n\n".join(p) for p in parts]


def build(reg, report=False):
    sources = load_sources()
    books = {}
    catalogs = {layer: [] for layer in LAYERS}
    texts = {}
    log = []
    seen = {}
    for layer in LAYERS:
        for row in read_jsonl(os.path.join(SEL, f"{layer}.jsonl")):
            row = dict(row)
            row["layer"] = layer
            cit = citation(row)
            uid = reg.uid_for(cit)
            ps = row.get("pd_source") or {}
            text, why = None, row.get("no_text_reason")
            n = str(ps.get("gutenberg")) if ps.get("gutenberg") else None
            if n and not row.get("no_text_reason"):
                if n not in sources["books"]:
                    why = f"PG #{n} is not in sources.json"
                else:
                    if n not in books:
                        books[n] = read_book(n, sources["books"][n])
                    lines, info = books[n]
                    if lines is None:
                        why = info
                    else:
                        text, how = extract(lines, row.get("printed_title") or row["title"], row.get("extract"))
                        if text is None:
                            why = how
                        elif row.get("max_lines") and text.count("\n") + 1 > row["max_lines"]:
                            why = f"extracted {text.count(chr(10)) + 1} lines, more than the {row['max_lines']} expected"
                            text = None
                        else:
                            why = None
            r, host = rights(row, sources["books"].get(n) if n else None, text is not None, why)
            if host == "full" and row.get("host") == "link":
                host = "link"              # a curator's call to link a PD poem (e.g. an epic too long to bank)
            link = ((gutenberg_url(n) if n else None) or row.get("link") or row.get("ao_page")
                    or "https://www.gutenberg.org/ebooks/search/?query="
                    + urllib.parse.quote_plus(f"{row['title']} {row['poet']}"))
            out = {
                "uid": uid, "citation": cit, "layer": layer, "tags": tags_for(row),
                "year": row["year"], "term": row.get("term"), "order": row.get("order"),
                "poet": row["poet"], "poet_died": row.get("poet_died"), "title": row["title"],
                "first_pub": row.get("first_pub"), "pd_source": row.get("pd_source"),
                "rights": r, "host": host, "link": link,
                "ao_page": row.get("ao_page"), "ao_id": row.get("ao_id"), "ref": row.get("ref"),
                "kind": row.get("kind"), "notes": row.get("notes") or "",
                "pack": pack_name(row) if host == "full" else None,
            }
            if layer == "addendum-heroic":
                out["status"] = "proposed"
            catalogs[layer].append(out)
            if host == "full":
                lines_n = text.count("\n") + 1
                prev = texts.get(uid)
                if prev and prev["text"] != text:
                    raise SystemExit(f"{cit}: two layers extracted different texts")
                texts[uid] = {"uid": uid, "citation": cit, "poet": row["poet"], "title": row["title"],
                              "source": {"gutenberg": int(n), "work": ps["work"], "edition_year": ps["edition_year"],
                                         "sha256": sources["books"][n].get("sha256")},
                              "lines": lines_n, "text": text}
            log.append((layer, row["year"], row.get("term"), row["poet"], row["title"], host,
                        texts[uid]["lines"] if host == "full" else 0, why or ""))
            seen.setdefault(cit, []).append(layer)
    return catalogs, texts, log


def pieces_for(cat_rows, texts, layer_title):
    when = CUT_ON + "T00:00:00.000Z"
    packs = {}
    for row in cat_rows:
        if row["host"] != "full":
            continue
        t = texts[row["uid"]]
        src = row["pd_source"]
        fp = row.get("first_pub") or {}
        source = row["poet"] + (f", {fp['work']} ({fp['year']})" if fp.get("work") and fp.get("year") else "")
        where = (f"AmblesideOnline Year {row['year']}" + (f", Term {row['term']}" if row.get("term") else "")
                 if row["layer"] == "ao" else
                 f"Heroic addendum (proposed), beside AO Year {row['year']}, Term {row['term']}")
        base_notes = (f"{where}.\nText: {src['work']} ({src['edition_year']}), Project Gutenberg #{src['gutenberg']}.\n"
                      f"{row['rights']['basis']}\nWord Hoard {row['citation']} · {row['uid']}")
        category = "Song" if row.get("kind") == "song" else "Poetry"
        parts = split_parts(t["text"]) if t["lines"] > LONG else [t["text"]]
        for k, body in enumerate(parts, 1):
            if len(parts) == 1:
                pid, title, notes = str(uuid.uuid5(NAMESPACE, row["uid"])), row["title"], base_notes
            else:
                pid = str(uuid.uuid5(NAMESPACE, f"{row['uid']}#part{k}"))
                title = f"{row['title']}, part {k} of {len(parts)}"
                notes = base_notes + f"\nA long poem, banked in {len(parts)} parts of whole stanzas."
            packs.setdefault(row["pack"], []).append({
                "id": pid, "createdAt": when, "updatedAt": when,
                "title": title, "source": source, "category": category, "translation": "",
                "text": body, "notes": notes, "tags": row["tags"],
                "srs": {"reps": 0, "ease": 2.5, "interval": 0, "due": when}, "history": [],
            })
    return packs


def render_all(catalogs, texts):
    blobs = {}
    for layer, rows in catalogs.items():
        blobs[os.path.join(DATA, f"catalog-{layer}.jsonl")] = jsonl(rows)
        for name, pieces in pieces_for(rows, texts, layer).items():
            blobs[os.path.join(PACKS, f"{name}.json")] = _X.render(pieces)
    blobs[os.path.join(DATA, "texts.jsonl")] = jsonl(sorted(texts.values(), key=lambda t: t["citation"]))
    return blobs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--uids", default=UIDS)
    a = ap.parse_args()
    if a.fetch:
        ok = fetch(load_sources())
        print("  DONE: all fetched/present" if ok else "  some fetches failed; rerun (resumable)")
        return
    reg = U.WhUidRegistry(a.uids)
    catalogs, texts, log = build(reg)
    if a.report:
        for l in log:
            print("  " + " | ".join(str(x) for x in l))
    blobs = render_all(catalogs, texts)
    for layer, rows in catalogs.items():
        full = sum(r["host"] == "full" for r in rows)
        print(f"  {layer:<16}{len(rows):>5} poems  {full:>4} hosted  {len(rows) - full:>4} linked out")
    print(f"  texts {len(texts)}   packs {sum(1 for p in blobs if p.startswith(PACKS))}")
    s = reg.stats()
    print(f"  uids minted {s['minted']} / reused {s['reused']} / registry total {s['total']:,}")
    if a.check:
        reg.assert_no_mint()
        stale = [os.path.relpath(p, ROOT) for p, b in blobs.items() if not os.path.exists(p) or open(p, "rb").read() != b]
        have = {os.path.join(PACKS, f) for f in os.listdir(PACKS)} if os.path.isdir(PACKS) else set()
        extra = sorted(os.path.relpath(p, ROOT) for p in have - set(blobs))
        if stale or extra:
            raise SystemExit(f"CHECK FAILED: differs from committed: {stale} extra: {extra}")
        print("  CHECK PASSED: minted 0, output byte-identical.")
        return
    if a.report:
        return
    if os.path.isdir(PACKS):
        for f in os.listdir(PACKS):
            if os.path.join(PACKS, f) not in blobs:
                os.remove(os.path.join(PACKS, f))
    for p, b in blobs.items():
        write_atomic(p, b)
    reg.save()
    print(f"  wrote {os.path.relpath(DATA, ROOT)}/ and {os.path.relpath(PACKS, ROOT)}/")
    if s["minted"]:
        print(f"  wrote {os.path.relpath(a.uids, ROOT)}   <- COMMIT THIS")


if __name__ == "__main__":
    main()
