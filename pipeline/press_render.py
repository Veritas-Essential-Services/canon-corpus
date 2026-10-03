#!/usr/bin/env python3
"""press_render.py -- a Press document -> one publish-ready Pandoc Markdown book.

The book is laid out the way a modern reprint of a Puritan classic is:

  YAML metadata (title, subtitle, author, original date, source edition,
      rights) -- Pandoc builds the EPUB/print title page from it
  The original title page, set as printed (its own unnumbered section)
  Front matter and body, headings from the source's own division tree
  Footnotes, numbered through the book
  Index of Scripture References, generated from the tagged references and
      linked back to the section each one is cited in
  A Note on the Text: source edition, method, and every change the Press made

Nothing is modernised. Spelling, punctuation and capitalisation are the source
edition's; the only changes are typographic (whitespace, markup) and the
per-book corrections listed in the Note on the Text, each with its evidence.
"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from press_scripture import VERSES

OSIS_ORDER = list(VERSES)
OSIS_NAMES = {
    "Gen": "Genesis", "Exod": "Exodus", "Lev": "Leviticus", "Num": "Numbers", "Deut": "Deuteronomy",
    "Josh": "Joshua", "Judg": "Judges", "Ruth": "Ruth", "1Sam": "1 Samuel", "2Sam": "2 Samuel",
    "1Kgs": "1 Kings", "2Kgs": "2 Kings", "1Chr": "1 Chronicles", "2Chr": "2 Chronicles",
    "Ezra": "Ezra", "Neh": "Nehemiah", "Esth": "Esther", "Job": "Job", "Ps": "Psalms",
    "Prov": "Proverbs", "Eccl": "Ecclesiastes", "Song": "Song of Solomon", "Isa": "Isaiah",
    "Jer": "Jeremiah", "Lam": "Lamentations", "Ezek": "Ezekiel", "Dan": "Daniel", "Hos": "Hosea",
    "Joel": "Joel", "Amos": "Amos", "Obad": "Obadiah", "Jonah": "Jonah", "Mic": "Micah",
    "Nah": "Nahum", "Hab": "Habakkuk", "Zeph": "Zephaniah", "Hag": "Haggai", "Zech": "Zechariah",
    "Mal": "Malachi", "Matt": "Matthew", "Mark": "Mark", "Luke": "Luke", "John": "John",
    "Acts": "Acts", "Rom": "Romans", "1Cor": "1 Corinthians", "2Cor": "2 Corinthians",
    "Gal": "Galatians", "Eph": "Ephesians", "Phil": "Philippians", "Col": "Colossians",
    "1Thess": "1 Thessalonians", "2Thess": "2 Thessalonians", "1Tim": "1 Timothy",
    "2Tim": "2 Timothy", "Titus": "Titus", "Phlm": "Philemon", "Heb": "Hebrews", "Jas": "James",
    "1Pet": "1 Peter", "2Pet": "2 Peter", "1John": "1 John", "2John": "2 John", "3John": "3 John",
    "Jude": "Jude", "Rev": "Revelation"}

def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)

def anchor_id(slug, section):
    return f"{slug}-s-{re.sub(r'[^0-9A-Za-z]+', '-', section or 'x').strip('-')}"

def plain(md):
    """Markdown inline -> plain words (for index entries)."""
    s = re.sub(r"\[\^[^\]]+\]", "", md)
    s = re.sub(r"\[\]\{[^}]*\}", "", s)
    s = re.sub(r"\]\{[^}]*\}", "", s).replace("[", "")
    s = re.sub(r"[*]", "", s).replace("\\", "")
    return re.sub(r"\s+", " ", s).strip()

def render(doc, meta):
    """doc: Press document; meta: the catalog entry (title, author, ...)."""
    slug = meta["slug"]
    L = []
    y = {"title": meta["title"], "subtitle": meta.get("subtitle"), "author": meta["author"],
         "date": meta.get("first_published"), "lang": meta.get("lang", "en-GB"),
         "rights": meta.get("rights_line"), "source-edition": meta.get("source_edition"),
         "description": meta.get("description"), "press-slug": slug,
         "toc": True, "toc-depth": 2}
    L.append("---")
    for k, v in y.items():
        if v is None:
            continue
        L.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    L.append("---\n")

    blocks = doc["blocks"]
    seen_sections = {}
    pending_pb = []
    i = 0
    in_tp = False
    tp_lines = []
    for b in blocks:
        k = b["k"]
        if k == "titlepage_start":
            in_tp, tp_lines = True, []
            continue
        if k == "titlepage_end":
            in_tp = False
            if tp_lines:
                L.append("# The Original Title Page {.unnumbered .unlisted .titlepage}\n")
                L.append("::: {.titlepage}")
                for cls, md in tp_lines:
                    L.append(f"[{md}]{{.tp-{cls or 'line'}}}\n")
                L.append(":::\n")
            continue
        if in_tp:
            if k in ("tp", "para", "display", "heading", "signature"):
                tp_lines.append((b.get("cls"), b["md"]))
            continue
        if k == "heading":
            lvl = max(1, min(6, b["level"]))
            attrs = []
            # house style: a heading carries no closing full stop ("Chapter I." -> "Chapter I")
            # (an abbreviation keeps its stop: "St.", "Mr.", "p.", "ver.")
            h = b["md"].strip()
            if not re.search(r"\b(?:St|Mr|Mrs|Dr|Mt|ver|viz|ch|chap|p|pp|ib|ibid|Ibid|cf|Cf|&c)\.$", h):
                h = re.sub(r"\.\s*$", "", h)
            b = dict(b, md=h)
            if b.get("anchor") and not b.get("sub"):
                aid = anchor_id(slug, b["anchor"])
                if aid in seen_sections:
                    aid += f"-{len(seen_sections)}"
                seen_sections[aid] = plain(b["md"])
                attrs.append("#" + aid)
            attrs.append(".unnumbered")   # the books number their own chapters
            L.append("#" * lvl + " " + b["md"] + (" {" + " ".join(attrs) + "}" if attrs else "") + "\n")
        elif k == "signature":
            L.append("::: {.signature}\n" + b["md"] + "\n:::\n")
        elif k == "argument":
            L.append("::: {.argument}\n" + b["md"] + "\n:::\n")
        elif k == "display":
            L.append("::: {.display .%s}\n%s\n:::\n" % (b.get("cls") or "h", b["md"]))
        elif k == "para":
            L.append("".join(pending_pb) + b["md"] + "\n")
            pending_pb = []
        elif k == "quote":
            L.append("> " + b["md"].replace("\n", "\n> ") + "\n")
        elif k == "list":
            for j, it in enumerate(b["items"], 1):
                L.append((f"{j}. " if b.get("ordered") else "- ") + it)
            L.append("")
        elif k == "table":
            rows = b["rows"]
            if rows:
                w = max(len(r) for r in rows)
                rows = [r + [""] * (w - len(r)) for r in rows]
                L.append("| " + " | ".join(rows[0]) + " |")
                L.append("|" + "---|" * w)
                for r in rows[1:]:
                    L.append("| " + " | ".join(r) + " |")
                L.append("")
        elif k == "pb":
            pending_pb.append(b["md"])
        elif k == "pagefoot":
            # notes whose call marks the scan lost: kept at the foot of their page
            L.append("::: {.pagefoot}")
            L.append(f"[Notes{' to p. ' + b['page'] if b.get('page') else ''}]{{.pagefoot-head}}\n")
            for md in b["notes"]:
                L.append(md + "\n")
            L.append(":::\n")
    # footnotes (a note whose call the source lost is printed after the text,
    # under its own heading, rather than dropped or guessed into place)
    body_md = "\n".join(L)
    called = {k: v for k, v in doc.get("notes", {}).items() if f"[^{k}]" in body_md}
    orphans = {k: v for k, v in doc.get("notes", {}).items() if k not in called}
    if called:
        L.append("")
        for label, md in called.items():
            L.append(f"[^{label}]: {md}\n")
    if orphans:
        L.append("# Further Notes {.unnumbered .orphan-notes}\n")
        L.append("*These notes stand in the source edition, but the transcription lost the marks that tie "
                 "them to the text. They are given here in their printed order until each is placed "
                 "against the scan.*\n")
        for label, md in orphans.items():
            # never a Markdown list: Pandoc would renumber it, and indent a
            # second paragraph into a code block
            paras = [p.strip() for p in md.split("\n\n") if p.strip()] or [""]
            L.append(f"[{label.lstrip('n')}.]{{.note-num}} {paras[0]}\n")
            for p in paras[1:]:
                L.append(p + "\n")
    # index of scripture references
    idx = {}
    for r in doc.get("refs", []):
        for vid in r["ids"]:
            parts = vid.split(".")
            bk = parts[0]
            idx.setdefault(bk, {}).setdefault(vid, [])
            sec = r["section"]
            if sec not in idx[bk][vid]:
                idx[bk][vid].append(sec)
    if idx:
        L.append("# Index of Scripture References {.unnumbered .index}\n")
        for bk in sorted(idx, key=OSIS_ORDER.index):
            L.append(f"## {OSIS_NAMES[bk]} {{.unnumbered .unlisted}}\n")
            def key(v):
                p = v.split(".")
                return (int(p[1]), int(p[2]) if len(p) > 2 else 0)
            lines = []
            for vid in sorted(idx[bk], key=key):
                p = vid.split(".")
                label = f"{p[1]}:{p[2]}" if len(p) > 2 else f"{p[1]}"
                links = []
                for sec in idx[bk][vid]:
                    aid = anchor_id(slug, sec)
                    name = seen_sections.get(aid)
                    links.append(f"[{name}](#{aid})" if name else "")
                links = [x for x in links if x]
                lines.append(f"{label} {'; '.join(links)}" if links else label)
            L.append("\\\n".join(lines) + "\n")
    # note on the text
    L.append("# A Note on the Text {.unnumbered .colophon}\n")
    for para in meta.get("note_on_text", []):
        L.append(para + "\n")
    md = "\n".join(L)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return unique_ids(md)

def unique_ids(md):
    """Every element id once: a page number printed twice (a new pagination in
    the prelims, a reprinted leaf) would otherwise give a duplicate id, which
    makes the EPUB invalid. The second becomes -2, and so on."""
    seen = {}
    def one(m):
        i = m.group(1)
        seen[i] = seen.get(i, 0) + 1
        return "{#" + (i if seen[i] == 1 else f"{i}-{seen[i]}")
    return re.sub(r"\{#([^\s}]+)", one, md)
