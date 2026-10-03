#!/usr/bin/env python3
"""press_text.py -- plain-text sources -> Press documents.

  convert_gutenberg  a Project Gutenberg transcription (whole book, or one
                     treatise extracted from a Works volume by its title line)
  convert_ia         an Internet Archive OCR text layer, one treatise
                     extracted from a Works volume and cleaned (see that
                     function for exactly what is and is not touched)

Both return the same Press document press_thml.convert does, so rendering,
QA and proofing are shared.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from press_thml import esc, guard_start, wrap
from press_scripture import parse_context

# ------------------------------------------------------------------ shared
# A printed reference: "Psa 66:17,18", "I Cor 14:15", "Rom. viii. 13", "2 Cor. v. 17"
_BOOKWORD = r"(?:[1-3]|I{1,3})?\s?[A-Z][a-z]{1,12}\.?"
RE_REF_ARABIC = re.compile(r"(?<![A-Za-z])(" + _BOOKWORD + r")\s(\d{1,3}):(\d{1,3}(?:\s?[-–,]\s?\d{1,3})*)")
RE_REF_ROMAN = re.compile(r"(?<![A-Za-z])(" + _BOOKWORD + r")\s([ivxlc]{1,7})\.\s?(\d{1,3}(?:\s?[-–,]\s?\d{1,3})*)\b")

def tag_refs(text_md, conv):
    """Wrap printed references in an already-escaped markdown string."""
    def sub(m, roman):
        printed = m.group(0)
        book = m.group(1)
        s = f"{book} {m.group(2)}{'.' if roman else ':'} {m.group(3)}" if roman else \
            f"{book} {m.group(2)}:{m.group(3)}"
        ids, probs, inf = parse_context(s, conv.ctx)
        if not ids:
            # not a reference after all ("Vol 3:4" etc.): say nothing unless it looked like one
            if not probs or "unknown book" not in probs[0]:
                conv.problems += [f"{conv.section}: {p}" for p in probs]
            return printed
        conv.refs.append({"printed": printed, "ids": ids, "section": conv.section})
        return wrap(printed, "[", ']{.scripture osis="' + " ".join(ids) + '"}')
    text_md = RE_REF_ARABIC.sub(lambda m: sub(m, False), text_md)
    text_md = RE_REF_ROMAN.sub(lambda m: sub(m, True), text_md)
    return text_md

class Doc:
    def __init__(self, slug):
        self.slug = slug
        self.blocks, self.notes, self.refs, self.problems = [], {}, [], []
        self.section, self.ctx, self.nsec = None, {}, 0
    def heading(self, md, level=1):
        self.nsec += 1
        self.section = f"s{self.nsec}"
        self.ctx = {}
        self.blocks.append({"k": "heading", "md": md, "level": level, "anchor": self.section,
                            "section": self.section})
    def add(self, k, md, **kw):
        self.blocks.append({"k": k, "md": md, "section": self.section, **kw})
    def out(self):
        return {"meta": {}, "blocks": self.blocks, "notes": self.notes, "refs": self.refs,
                "problems": self.problems}

def inline_plain(s):
    """Plain transcription text -> escaped markdown; _x_ is PG's italic."""
    s = re.sub(r"\s+", " ", s).strip()
    parts = re.split(r"(_[^_]+_)", s)
    out = []
    for p in parts:
        if len(p) > 2 and p.startswith("_") and p.endswith("_"):
            out.append(wrap(esc(p[1:-1]), "*", "*"))
        else:
            out.append(esc(p))
    return "".join(out)

def is_heading(par):
    letters = re.sub(r"[^A-Za-z]", "", par)
    return (len(par) < 120 and len(letters) >= 3 and letters.isupper()
            and not re.match(r"^[IVXLC]+\.?$", par.strip()))

# ------------------------------------------------------------------ Gutenberg
def pg_body(raw):
    a = re.search(r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG[^\n]*\n", raw)
    b = re.search(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG", raw)
    return raw[a.end() if a else 0: b.start() if b else len(raw)]

def convert_gutenberg(path, slug, e):
    raw = open(path, encoding="utf-8-sig").read().replace("\r\n", "\n")
    body = pg_body(raw)
    marker = e["source"].get("extract")
    if marker:
        body = extract_offor(body, marker)
    pars = [p.strip("\n") for p in re.split(r"\n\s*\n", body) if p.strip()]
    # footnotes: a "FOOTNOTES:" line, then "N text" / "[N] text" paragraphs
    notes_raw = {}
    if "FOOTNOTES:" in pars:
        k = pars.index("FOOTNOTES:")
        for p in pars[k + 1:]:
            m = re.match(r"^\[?(\d{1,3})[\].]?\s+(.*)$", p, re.S)
            if m:
                notes_raw[m.group(1)] = m.group(2)
            elif notes_raw:
                last = list(notes_raw)[-1]
                notes_raw[last] += "\n\n" + p
        pars = pars[:k]
    d = Doc(slug)
    # title page: the opening run of capitalised lines, up to the first real paragraph
    tp = []
    while pars and len(tp) < 16:
        flat0 = re.sub(r"\s+", " ", pars[0])
        if re.match(r"^(ADVERTISEMENT|PREFACE|TO THE READER|THE EPISTLE|EPISTLE|INTRODUCTION|DEDICATION)", flat0) \
                or (len(flat0) > 260 and not is_heading(flat0)):
            break
        tp.append(pars.pop(0))
    if tp:
        d.blocks.append({"k": "titlepage_start", "section": "tp"})
        for t in tp:
            d.blocks.append({"k": "tp", "md": inline_plain(t), "cls": None, "section": "tp"})
        d.blocks.append({"k": "titlepage_end", "section": "tp"})
    expect = [1]
    def take(n):
        """A note call is accepted only near where the sequence says it should
        be (a missing note in the source must not derail the rest)."""
        if str(n) in notes_raw and f"n{n}" not in d.notes and expect[0] <= n <= expect[0] + 4:
            expect[0] = n + 1
            d.notes[f"n{n}"] = tag_refs(inline_plain(notes_raw[str(n)]), d)
            return True
        return False
    def note_call(m):
        n = int(m.group(1))
        return f"{m.group(0)[:-len(m.group(1))]}[^n{n}]" if take(n) else m.group(0)
    def glued_to_verse(m):
        # "Ephesians 1:192": verse 19 with note 2 glued on, when 192 is no verse
        book, ch, vs, tail = m.group(1), m.group(2), m.group(3), m.group(4)
        from press_scripture import parse_report
        if parse_report(f"{book} {ch}:{vs}{tail}")[0] or not parse_report(f"{book} {ch}:{vs}")[0]:
            return m.group(0)
        return f"{book} {ch}:{vs}[^n{int(tail)}]" if take(int(tail)) else m.group(0)
    for p in pars:
        flat = re.sub(r"\s+", " ", p).strip()
        if is_heading(flat):
            if re.fullmatch(r"(?:[A-Z][A-Za-z]*,? \d{4}\. )?(?:[A-Z][A-Za-z.]*\.? ?){1,4}\.?", flat) \
                    and d.blocks and d.blocks[-1]["k"] == "para" and len(flat.split()) <= 5:
                d.add("signature", inline_plain(flat))   # "GEO. OFFOR.", "HACKNEY, 1850. GEORGE OFFOR."
                continue
            d.heading(inline_plain(flat), level=1)
            continue
        md = inline_plain(flat)
        # footnote calls: digits glued to a word or closing punctuation, in sequence
        md = re.sub(r"(" + _BOOKWORD + r")\s(\d{1,3}):(\d{1,3}?)(\d{1,2})(?=[\s,.;)]|$)", glued_to_verse, md)
        md = re.sub(r"(?<=[A-Za-z.;!?’”)\]])(\d{1,3})(?=[\s,.;:—”’)]|$)", note_call, md)
        md = tag_refs(md, d)
        d.add("para", guard_start(md))
    for k, v in notes_raw.items():
        if f"n{k}" not in d.notes:
            d.problems.append(f"footnote {k} has no call in the text")
            d.notes[f"n{k}"] = tag_refs(inline_plain(v), d)
    if d.nsec == 0:
        d.heading(esc(e["title"]))
    return d.out()

def extract_offor(body, marker):
    """One treatise out of an Offor Works volume: from its title line (the
    occurrence in the body, not the volume's contents list) through its own
    FOOTNOTES block, up to the next treatise's title."""
    lines = body.split("\n")
    starts = [i for i, l in enumerate(lines) if l.strip().upper().startswith(marker.upper())]
    # the contents list is indented and early; the title proper is followed by
    # a long text within 400 lines
    start = next((i for i in starts if not lines[i].startswith(" ")), None)
    if start is None:
        raise RuntimeError(f"extract marker {marker!r} not found")
    rest = lines[start:]
    k = next((i for i, l in enumerate(rest) if l.strip() == "FOOTNOTES:"), None)
    if k is None:
        return "\n".join(rest)
    # footnote paragraphs run until four blank lines (PG separates treatises so)
    j = k + 1
    blank = 0
    while j < len(rest):
        blank = blank + 1 if not rest[j].strip() else 0
        if blank >= 3:
            break
        j += 1
    return "\n".join(rest[:j])

# ------------------------------------------------------------------ Internet Archive OCR
def convert_ia(path, slug, e):
    import press_ocr
    return press_ocr.convert(path, slug, e)
