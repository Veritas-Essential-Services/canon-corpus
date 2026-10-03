#!/usr/bin/env python3
"""press_tcp.py -- an EEBO-TCP transcription (TEI P5) -> a Press document.

The Text Creation Partnership keyed thousands of 17th-century books from the
page images of the first editions, twice over, by hand, and released Phase I
under CC0. For a Puritan title that no 19th-century editor reprinted (Watson's
Godly Man's Picture, Burroughs's Rare Jewel, Perkins's Arte of Prophecying),
that is a far better witness than any OCR: it is the first edition, as
printed, by people.

    catalog: "source": {"kind": "tcp", "id": "A30598", "edition": "..."}
    fetched from github.com/textcreationpartnership/<id>/<id>.xml

What the Press does to the transcription, and nothing more:
  - long s becomes s (a letterform, not a spelling); every other spelling,
    capital and stop is the first edition's
  - a word broken at a line end (<g ref="char:EOLhyphen"/>) is joined
  - marginal notes (<note place="margin">), mostly scripture references,
    become footnotes at the point the transcribers placed them
  - what the keyers could not read (<gap reason="illegible">) prints as
    ⟨•⟩ per letter, ⟨word⟩, ⟨…⟩; Greek and Hebrew they did not key
    (<gap reason="foreign">) prints as ⟨Greek⟩. Each is counted and listed
    for a person to supply from the page image: nothing is guessed in.
  - a table of contents and an errata list are left out of the text (the
    errata are listed in the Note on the Text, not silently applied)
"""
import os, re, sys
import xml.etree.ElementTree as ET
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from press_thml import esc, guard_start, wrap
from press_text import Doc, tag_refs

NS = "{http://www.tei-c.org/ns/1.0}"
SKIP_DIVS = {"table_of_contents", "contents", "errata", "publishers_advertisement", "index", "table"}

def tag(el):
    return el.tag.replace(NS, "")

def clean(s):
    return (s or "").replace("ſ", "s").replace("­", "")

class Conv:
    def __init__(self, slug):
        self.d = Doc(slug)
        self.d.notes = {}
        self.slug = slug
        self.nnote = 0
        self.gaps = []          # (kind, extent, section)
        self.errata = []
        self.pending_pb = None
        self.span = None        # (from, until) regexes: a treatise inside a larger volume
        self.on = True

    # -------------------------------------------------------------- inline
    def inline(self, el, top=True):
        out = [esc(clean(el.text)) if el.text else ""]
        for c in el:
            t = tag(c)
            if t == "hi":
                inner = self.inline(c, False)
                rend = c.get("rend") or ""
                if "sup" in rend:
                    out.append(f"^{inner.strip()}^" if inner.strip() else "")
                else:
                    out.append(wrap(inner, "*", "*") if inner.strip() else inner)
            elif t == "g":
                ref = c.get("ref") or ""
                if ref in ("char:EOLhyphen", "char:EOLunhyphen"):
                    pass
                else:
                    out.append(esc(clean(c.text)))
            elif t == "gap":
                out.append(self.gap(c))
            elif t == "note":
                out.append(self.note(c))
            elif t == "pb":
                out.append(self.pb(c))
            elif t == "lb":
                out.append(" ")
            elif t in ("list", "p", "lg", "l", "table"):
                # block content inside a paragraph: kept as running text
                out.append(" " + self.inline(c, False) + " ")
            elif t == "item":
                out.append(" " + self.inline(c, False) + " ")
            elif t == "label":
                out.append(self.inline(c, False) + " ")
            else:   # q, bibl, seg, name, date, foreign, ...: keep the words
                out.append(self.inline(c, False))
            if c.tail:
                out.append(esc(clean(c.tail)))
        s = "".join(out)
        if top:
            s = re.sub(r"\s+", " ", s).strip()
            s = re.sub(r"\s+([;:,?!.])(?=\s|$|\*)", r"\1", s)
        return s

    def gap(self, c):
        reason = c.get("reason") or ""
        extent = c.get("extent") or ""
        self.gaps.append((reason, extent, self.d.section))
        if reason.startswith("foreign"):
            return "[⟨Greek or Hebrew⟩]{.gap}"
        if reason.startswith("duplicate"):
            return ""
        m = re.match(r"(\d+) letter", extent)
        if m:
            return "[" + "⟨•⟩" * int(m.group(1)) + "]{.gap}"
        if "word" in extent:
            n = int(re.match(r"(\d+)", extent).group(1)) if re.match(r"\d", extent) else 1
            return "[" + " ".join(["⟨word⟩"] * n) + "]{.gap}"
        return "[⟨…⟩]{.gap}"

    def note(self, c):
        if not self.on:
            return ""
        self.nnote += 1
        lab = f"n{self.nnote}"
        body = self.inline(c)
        self.d.notes[lab] = tag_refs(body, self.d)
        return f"[^{lab}]"

    def pb(self, c):
        facs = c.get("facs") or ""
        img = facs.rsplit(":", 1)[-1] if facs else ""
        n = c.get("n") or ""
        key = re.sub(r"[^0-9A-Za-z]", "", n) if n else f"i{img}"
        return f"[]{{#{self.slug}-p{key} .pb n=\"{n}\" img=\"{img}\"}}"

    # -------------------------------------------------------------- blocks
    def gate(self, el):
        """With a span, only the paragraphs from `from` up to (not including)
        `until` are set; decided on the paragraph's words before converting it."""
        if not self.span:
            return True
        raw = " ".join("".join(el.itertext()).split()).replace("ſ", "s")
        if not self.on and self.span[0] and re.search(self.span[0], raw) and not getattr(self, "done", False):
            self.on = True
        elif self.on and self.span[1] and re.search(self.span[1], raw):
            self.on, self.done = False, True
        return self.on

    def para(self, md, kind="para"):
        if not self.on:
            return
        md = md.strip()
        if not md or not re.search(r"[A-Za-z0-9⟨]", md):
            return
        self.d.add(kind, guard_start(tag_refs(md, self.d)) if kind == "para" else md)

    def div(self, el, level):
        typ = (el.get("type") or "").lower()
        if typ in SKIP_DIVS:
            if typ == "errata":
                self.errata.append(self.inline(el))
            return
        if typ == "title_page":
            self.d.blocks.append({"k": "titlepage_start", "section": "tp"})
            for c in el.iter():
                if tag(c) in ("p", "item", "head", "byline", "docImprint", "docTitle", "titlePart"):
                    if tag(c) == "p" and any(tag(x) == "list" for x in c):
                        # the paragraph's own words before its list, then the items
                        lead = esc(clean(c.text or "")).strip()
                        if lead:
                            self.d.blocks.append({"k": "tp", "md": lead, "cls": "h2", "section": "tp"})
                        continue
                    if tag(c) == "p" and c.find(f"{NS}list") is None:
                        md = self.inline(c)
                    elif tag(c) == "item" or tag(c) == "head":
                        md = self.inline(c)
                    else:
                        continue
                    if md:
                        self.d.blocks.append({"k": "tp", "md": md, "cls": "h3", "section": "tp"})
            self.d.blocks.append({"k": "titlepage_end", "section": "tp"})
            return
        heads = [c for c in el if tag(c) == "head"]
        if heads and self.on:
            self.d.heading(" ".join(self.inline(h) for h in heads), level=min(level, 3))
        for c in el:
            t = tag(c)
            if t == "head":
                continue
            if t == "div":
                self.div(c, level + 1)
            elif t == "p":
                if self.gate(c):
                    self.para(self.inline(c))
            elif t == "list":
                for it in c:
                    if tag(it) == "item":
                        self.para(self.inline(it))
                    elif tag(it) == "head":
                        self.para(self.inline(it))
            elif t in ("epigraph", "q", "quote", "lg"):
                self.para(self.inline(c), "quote")
            elif t in ("trailer", "opener", "salute", "dateline", "byline", "argument"):
                self.para(self.inline(c), "display")
            elif t in ("closer", "signed"):
                self.para(self.inline(c), "signature")
            elif t == "pb":
                if self.on:
                    self.d.add("pb", self.pb(c))
            elif t == "note":
                # a margin note between paragraphs: attach to the next paragraph's start
                self.d.add("pb", self.note(c))
            elif t in ("milestone", "gap", "figure"):
                continue
            else:
                self.para(self.inline(c))

def convert(path, slug, texts=None, span=None):
    """`texts`: in a volume of several works, which of them (1-based) to set.
    `span`: [from, until] paragraph regexes, for a treatise printed inside a
    larger work (the title page of the volume is kept, as its provenance)."""
    root = ET.parse(path).getroot()
    text = root.find(f"{NS}text")
    c = Conv(slug)
    if span:
        c.span, c.on = span, False

    def walk(t):
        # a volume of several works is <text><group><text>...</text></group></text>
        for part in t:
            if tag(part) == "group":
                subs = [x for x in part if tag(x) == "text"]
                for i, sub in enumerate(subs, 1):
                    if not texts or i in texts:
                        walk(sub)
                continue
            for el in part:
                if tag(el) == "div":
                    c.div(el, 1)
                elif tag(el) == "pb":
                    c.d.add("pb", c.pb(el))
    walk(text)
    doc = c.d.out()
    doc["gaps"] = c.gaps
    doc["errata"] = c.errata
    illegible = sum(1 for g in c.gaps if g[0].startswith("illegible"))
    foreign = sum(1 for g in c.gaps if g[0].startswith("foreign"))
    if illegible:
        doc["problems"].append(f"{illegible} place(s) the keyers could not read, printed ⟨•⟩/⟨word⟩: "
                               "to be supplied from the page images")
    if foreign:
        doc["problems"].append(f"{foreign} Greek or Hebrew passage(s) the keyers did not transcribe, "
                               "printed ⟨Greek or Hebrew⟩")
    return doc

if __name__ == "__main__":
    import json
    d = convert(sys.argv[1], "t")
    print(json.dumps({k: v for k, v in d.items() if k not in ("blocks", "notes")}, ensure_ascii=False)[:3000])
    for b in d["blocks"][:30]:
        print(b.get("k"), (b.get("md") or "")[:120])
