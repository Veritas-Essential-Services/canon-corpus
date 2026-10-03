#!/usr/bin/env python3
"""press_thml.py -- a CCEL ThML file -> a Press document (publishable structure).

structure_texts.convert_thml builds the SEARCH spine: paragraphs flattened to
plain text, footnotes and italics gone. That is right for finding passages and
wrong for printing them. This reads the same source file and keeps everything
a typesetter needs:

  - the division tree, as heading levels (a lone wrapping div1 is the book
    itself, so its children become chapters)
  - the chapter "argument" (Goold's chapter summaries), italic, as printed
  - italics, bold, small capitals, foreign-language spans (lang tags for EPUB)
  - footnotes, numbered through the book
  - every scripture reference, kept AS PRINTED and tagged with its KJV verse
    ids (press_scripture.check_osis validates CCEL's own osisRef against the
    KJV versification; anything that fails is listed, never clamped)
  - the print edition's page breaks, as invisible anchors (`[]{#p-12 .pb}`), so
    every paragraph can still be checked against the scan of that page
  - the source title page, as its own block

Dropped on purpose: CCEL's generated indexes and contents (the Press rebuilds
both from the text) and CCEL's own description/staff prose (theirs, not the
author's).

A Press document is {"meta", "blocks", "notes", "refs", "problems"}; every
block's "md" is Pandoc Markdown. press_render.py turns it into a book.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import press_dom
from press_scripture import check_osis, parse_context

SKIP_DIV_TITLES = re.compile(r"^\s*(indexes|index of|contents\.?$|table of contents)", re.I)
HEADS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}
LANGS = {"la": "la", "lat": "la", "gr": "grc", "el": "grc", "grc": "grc", "he": "he",
         "heb": "he", "fr": "fr", "de": "de", "it": "it", "es": "es", "nl": "nl"}

_ESC = re.compile(r"([\\*_\[\]`<>$^~@|])")

def esc(s):
    return _ESC.sub(r"\\\1", s)

def ws(s):
    return re.sub(r"\s+", " ", s)

# A paragraph that STARTS like a list marker or a heading must not become one.
_LEAD = re.compile(r"^(\(?(?:\d+|[A-Za-z]|[ivxlcdmIVXLCDM]+)\.?)([.)])(\s)")

def guard_start(md):
    md = md.lstrip()
    m = _LEAD.match(md)
    if m:
        md = m.group(1) + "\\" + m.group(2) + m.group(3) + md[m.end():]
    if md[:1] in "#>:%+-=" or md[:2] in ("* ",):
        md = "\\" + md
    return md

def wrap(md, left, right):
    """Emphasis that Pandoc will honour: no space just inside the markers."""
    core = md.strip()
    if not core:
        return md
    lead = md[: len(md) - len(md.lstrip())]
    trail = md[len(md.rstrip()):]
    return f"{lead}{left}{core}{right}{trail}"

class Conv:
    def __init__(self, slug):
        self.slug = slug
        self.blocks, self.notes, self.refs, self.problems = [], {}, [], []
        self.nfoot = 0
        self.section = None
        self.ctx = {}

    # ------------------------------------------------------------ inline
    def inline(self, node):
        out = []
        for c in node.children:
            if isinstance(c, str):
                out.append(esc(ws(c)))
                continue
            t, a = c.tag, c.attrs
            style = (a.get("style") or "").lower()
            cls = (a.get("class") or "")
            if t in ("i", "em"):
                out.append(wrap(self.inline(c), "*", "*"))
            elif t in ("b", "strong"):
                out.append(wrap(self.inline(c), "**", "**"))
            elif t == "sup":
                inner = self.inline(c).strip()
                out.append(f"^{inner.replace(' ', chr(92) + ' ')}^" if inner else "")
            elif t == "sub":
                inner = self.inline(c).strip()
                out.append(f"~{inner.replace(' ', chr(92) + ' ')}~" if inner else "")
            elif t == "scripref":
                out.append(self.scripref(c))
            elif t == "note":
                out.append(self.footnote(c))
            elif t == "pb":
                n = a.get("n")
                if n:
                    out.append(f"[]{{#{self.slug}-p{re.sub(r'[^0-9A-Za-z]', '', n)} .pb n=\"{n}\"}}")
            elif t == "br":
                out.append("\\\n")
            elif t == "a" and "TOC" in cls:
                continue
            elif t == "span" or t == "foreign":
                inner = self.inline(c)
                if "uppercase" in style:
                    inner = inner.upper()
                lang = LANGS.get((a.get("lang") or "").lower()) or ("grc" if "Greek" in cls else None) \
                    or ("he" if "Hebrew" in cls else None)
                attrs = []
                if "small-caps" in style:
                    attrs.append(".smallcaps")
                if lang:
                    attrs.append(f"lang={lang}")
                out.append(wrap(inner, "[", "]{" + " ".join(attrs) + "}") if attrs and inner.strip() else inner)
            elif t in ("script", "style"):
                continue
            else:  # name, cite, a, term, unclear ... keep the words
                out.append(self.inline(c))
        return "".join(out)

    def scripref(self, c):
        printed = self.inline(c)
        osis = (c.attrs.get("osisref") or "")
        osis = " ".join(x.split(":", 1)[1] if ":" in x else x for x in osis.split())
        inferred = False
        parsed = c.attrs.get("parsed") or ""
        m = re.match(r"[a-z]*\|([1-3]?[A-Za-z]+)\|(\d+)\|(\d+)\|", parsed)
        if osis:
            ids, probs = check_osis(osis)
        elif m and m.group(3) != "0":
            ids, probs = check_osis(f"{m.group(1)}.{m.group(2)}.{m.group(3)}")
        else:
            ids, probs, inferred = parse_context(c.text(), self.ctx)
        if ids and not inferred:
            p = ids[-1].split(".")
            self.ctx.update(book=p[0], ch=int(p[1]))
        r = {"printed": ws(c.text()).strip(), "ids": ids, "section": self.section}
        if inferred:
            r["inferred"] = True
        self.refs.append(r)
        self.problems += [f"{self.section}: {p}" for p in probs]
        if not ids:
            return printed
        cls = ".scripture .inferred" if inferred else ".scripture"
        return wrap(printed, "[", "]{" + cls + ' osis="' + " ".join(ids) + '"}')

    def footnote(self, c):
        self.nfoot += 1
        label = f"n{self.nfoot}"
        paras = [self.inline(p).strip() for p in c.iter("p")] or [self.inline(c).strip()]
        self.notes[label] = "\n\n    ".join(p for p in paras if p)
        return f"[^{label}]"

    # ------------------------------------------------------------ blocks
    def add(self, kind, md=None, **kw):
        b = {"k": kind, "section": self.section}
        if md is not None:
            b["md"] = md
        b.update(kw)
        self.blocks.append(b)

    def block(self, node, level, titlepage=False):
        for c in node.children:
            if isinstance(c, str):
                if c.strip():
                    self.add("para", guard_start(esc(ws(c)).strip()))
                continue
            t = c.tag
            if re.fullmatch(r"div[1-6]", t) or (t == "div" and c.find("p")):
                self.div(c, level)
            elif t in HEADS:
                md = self.inline(c).strip()
                if md:
                    self.add("heading", md, level=min(6, level + 1), sub=True)
            elif t == "argument":
                self.add("argument", guard_start(self.inline(c).strip()))
            elif t == "p":
                md = self.inline(c).strip()
                if not md:
                    continue
                cls = c.attrs.get("class") or ""
                if titlepage:
                    self.add("tp", md, cls=cls)
                elif cls in ("h1", "h2", "h3", "h4"):
                    self.add("display", md, cls=cls)
                else:
                    self.add("para", guard_start(md), cls=cls or None)
            elif t in ("ul", "ol"):
                items = [guard_start(self.inline(li).strip()) for li in c.children
                         if not isinstance(li, str) and li.tag == "li"]
                self.add("list", items=[i for i in items if i], ordered=(t == "ol"))
            elif t == "table":
                rows = [[self.inline(td).strip() for td in tr.children if not isinstance(td, str)
                         and td.tag in ("td", "th")] for tr in c.iter("tr")]
                self.add("table", rows=[r for r in rows if any(r)])
            elif t in ("blockquote", "verse", "l", "lg"):
                self.add("quote", guard_start(self.inline(c).strip()))
            elif t == "pb":
                n = c.attrs.get("n")
                if n:
                    self.add("pb", n=n, md=f"[]{{#{self.slug}-p{re.sub(r'[^0-9A-Za-z]', '', n)} .pb n=\"{n}\"}}")
            elif t in ("insertindex", "script", "style", "hr"):
                continue
            else:
                self.block(c, level, titlepage)

    def div(self, d, level):
        a = d.attrs
        title = (a.get("title") or "").strip()
        dtype = (a.get("type") or "").lower()
        if SKIP_DIV_TITLES.match(title) or dtype in ("index", "indexes", "toc"):
            return
        self.section = a.get("id") or self.section
        self.ctx = {}
        first = next((c for c in d.children if not isinstance(c, str) and c.tag != "pb"), None)
        has_head = first is not None and first.tag in HEADS
        tp = dtype == "titlepage" or title.lower().rstrip(".") == "title page"
        if tp:
            self.add("titlepage_start")
            self.block(d, level, titlepage=True)
            self.add("titlepage_end")
            return
        if has_head:
            # the div's own printed heading(s): every leading h* element
            heads = []
            for c in list(d.children):
                if isinstance(c, str):
                    if c.strip():
                        break
                    continue
                if c.tag == "pb":
                    continue
                if c.tag in HEADS:
                    heads.append(c)
                    continue
                break
            md = " ".join(self.inline(h).strip() for h in heads)
            self.add("heading", md, level=level, anchor=self.section, shorttitle=a.get("shorttitle") or title)
            rest = type(d)(d.tag, d.attrs)
            rest.children = [c for c in d.children if c not in heads]
            self.block(rest, level)
        else:
            self.add("heading", esc(title), level=level, anchor=self.section, shorttitle=a.get("shorttitle") or title)
            self.block(d, level)

def convert(path, slug):
    raw = open(path, encoding="utf-8", errors="replace").read()
    body_at = raw.find("<ThML.body")
    head, body = raw[:body_at], raw[body_at:]
    root = press_dom.parse(body)
    meta = {}
    for tag in ("DC.Title", "pubHistory", "published"):
        m = re.search(rf"<{re.escape(tag)}[^>]*>(.*?)</{re.escape(tag)}>", head, re.S)
        if m and m.group(1).strip():
            meta[tag] = ws(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    m = re.search(r'<DC\.Creator[^>]*scheme="file-as"[^>]*>(.*?)<', head, re.S)
    if m:
        meta["file_as"] = ws(m.group(1)).strip()
    c = Conv(slug)
    tops = [n for n in root.iter() if n.tag == "div1"]
    content = [n for n in tops if not SKIP_DIV_TITLES.match(n.attrs.get("title", ""))]
    if len(content) == 1:
        # one wrapping div1 is the book: its children are the chapters
        c.section = content[0].attrs.get("id")
        c.block(content[0], 1)
    else:
        for d in content:
            c.div(d, 1)
    return {"meta": meta, "blocks": c.blocks, "notes": c.notes, "refs": c.refs,
            "problems": c.problems}

if __name__ == "__main__":
    import json
    doc = convert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "book")
    print(json.dumps({k: (v if k != "blocks" else v[:40]) for k, v in doc.items() if k != "notes"},
                     indent=1, ensure_ascii=False)[:6000])
