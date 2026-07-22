#!/usr/bin/env python3
"""render_markdown.py — the Press's raw-material machine: structure JSON → markdown.

Reads data/books/<slug>.json (the unit-id spine) and writes clean,
Pandoc-ready markdown:

  - YAML frontmatter (title, author, source) so Pandoc can title/typeset it
  - division headings detected from each unit's `ref` (chapter / book / act)
  - PROSE reflowed to paragraphs; SCRIPTURE with verse numbers; VERSE and DRAMA
    kept as flowing blocks (see the honesty note below)
  - scripture keylinks rendered as real footnotes — a study edition, not a reprint
  - a light typographic tidy (the search JSON left spaces around punctuation)

Scheme-aware via each book's `scheme.resolution`:
  paragraph    → prose (Owen, Flavel, Bunyan, Edwards, prose Gutenberg)
  verse        → scripture (KJV): book/chapter headings + verse numbers
  line-block   → poetry (Milton, Dante, Beowulf, Faust)  ⚠ see note
  cards/lines  → classical verse (Perseus TEI: Homer, Virgil) ⚠ see note
  speech-block → drama (Shakespeare) ⚠ see note

⚠ HONESTY NOTE — verse & drama: this JSON was built to *find* passages, so verse
lines were space-joined and a speech's speaker was folded into its block. The
markdown here is therefore PUBLISHABLE FOR THE PROSE SHELF and readable-but-not-
print-perfect for poetry/drama. Lineated poetry needs a one-time converter
refinement (preserve newlines in structure_texts) — flagged, not done here.

Run:
  python3 pipeline/render_markdown.py                # all books → data/markdown/
  python3 pipeline/render_markdown.py owen-mort      # one book → stdout
  python3 pipeline/render_markdown.py owen-mort out.md
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS = os.path.join(HERE, "..", "data", "books")
OUT = os.path.join(HERE, "..", "data", "markdown")

# OSIS book abbreviations → readable names, for footnote text.
OSIS_NAMES = {
    "Gen": "Genesis", "Exod": "Exodus", "Lev": "Leviticus", "Num": "Numbers",
    "Deut": "Deuteronomy", "Josh": "Joshua", "Judg": "Judges", "Ruth": "Ruth",
    "1Sam": "1 Samuel", "2Sam": "2 Samuel", "1Kgs": "1 Kings", "2Kgs": "2 Kings",
    "1Chr": "1 Chronicles", "2Chr": "2 Chronicles", "Ezra": "Ezra",
    "Neh": "Nehemiah", "Esth": "Esther", "Job": "Job", "Ps": "Psalm",
    "Prov": "Proverbs", "Eccl": "Ecclesiastes", "Song": "Song of Solomon",
    "Isa": "Isaiah", "Jer": "Jeremiah", "Lam": "Lamentations", "Ezek": "Ezekiel",
    "Dan": "Daniel", "Hos": "Hosea", "Joel": "Joel", "Amos": "Amos",
    "Obad": "Obadiah", "Jonah": "Jonah", "Mic": "Micah", "Nah": "Nahum",
    "Hab": "Habakkuk", "Zeph": "Zephaniah", "Hag": "Haggai", "Zech": "Zechariah",
    "Mal": "Malachi", "Matt": "Matthew", "Mark": "Mark", "Luke": "Luke",
    "John": "John", "Acts": "Acts", "Rom": "Romans", "1Cor": "1 Corinthians",
    "2Cor": "2 Corinthians", "Gal": "Galatians", "Eph": "Ephesians",
    "Phil": "Philippians", "Col": "Colossians", "1Thess": "1 Thessalonians",
    "2Thess": "2 Thessalonians", "1Tim": "1 Timothy", "2Tim": "2 Timothy",
    "Titus": "Titus", "Phlm": "Philemon", "Heb": "Hebrews", "Jas": "James",
    "1Pet": "1 Peter", "2Pet": "2 Peter", "1John": "1 John", "2John": "2 John",
    "3John": "3 John", "Jude": "Jude", "Rev": "Revelation",
}

def _one_ref(osis):
    parts = osis.split(".")
    if len(parts) == 3:
        book, ch, v = parts
        return f"{OSIS_NAMES.get(book, book)} {ch}:{v}"
    if len(parts) == 2:
        book, ch = parts
        return f"{OSIS_NAMES.get(book, book)} {ch}"
    return osis

def osis_pretty(raw):
    """Turn a keylink value into readable citation text. Handles the messy
    ThML cases: 'Bible:'/'Bible.kjv:' prefixes, ranges ('A.1.1-A.1.2'), and
    several refs in one string. 'Rom.8.13' → 'Romans 8:13'."""
    raw = re.sub(r"\bBible(\.\w+)?:", "", raw)
    out = []
    for token in raw.split():
        if "-" in token:
            a, b = token.split("-", 1)
            out.append(f"{_one_ref(a)}–{_one_ref(b)}")
        else:
            out.append(_one_ref(token))
    return ", ".join(out)

def tidy(text):
    """Undo the search layer's spacing around punctuation, for clean prose."""
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)          # ' ,' → ','
    text = re.sub(r"([“‘(])\s+", r"\1", text)              # '“ x' / '( x' → '“x' / '(x'
    text = re.sub(r"\s+([”’)])", r"\1", text)              # 'x ”' / 'x )' → 'x”' / 'x)'
    text = re.sub(r"\s+—\s+", "—", text)                   # spaced em dash tighten a touch
    text = re.sub(r"_([^_]+)_", r"*\1*", text)             # Gutenberg _italics_ → md *italics*
    text = re.sub(r"  +", " ", text)
    return text.strip()

# ---- division detection: (path_labels, verse_number_or_None, is_verse_body) ----

RE_KJV = re.compile(r"^(.+?)\s+(\d+):(\d+)$")             # Genesis 1:1
RE_PAR = re.compile(r"^(.*?),\s*par\.\s*\d+\s*$", re.I)    # Chapter I, par. 3
RE_LINEBLOCK = re.compile(r"^(.*)\.(\d+)$")                # PL I.13  /  DC Inf.IX.97

def analyze(ref, resolution):
    """Return (path, verse_no, is_verse) where path is a list of
    (level, label) coarsest-first for headings above this unit."""
    if resolution == "verse":                             # scripture
        m = RE_KJV.match(ref)
        if m:
            book, ch, v = m.group(1), m.group(2), m.group(3)
            return [(1, book), (2, f"Chapter {ch}")], v, False
        return [(2, ref)], None, False
    if resolution == "paragraph":                         # prose
        m = RE_PAR.match(ref)
        div = m.group(1).strip() if m else ref
        return [(2, div)], None, False
    if resolution == "speech-block":                      # drama
        if ", " in ref:
            play, loc = ref.split(", ", 1)
            return [(1, play), (2, loc)], None, False
        return [(1, ref)], None, False
    # line-block / cards / lines → verse
    m = RE_LINEBLOCK.match(ref)
    div = m.group(1).strip() if m else ref
    return [(2, div)], None, True

def render(book):
    slug = book["slug"]
    title = book.get("title", slug)
    author = book.get("author", "")
    resolution = book.get("scheme", {}).get("resolution", "paragraph")
    src = book.get("source", {})
    transl = src.get("translator")

    out = ["---", f'title: "{title}"']
    if author and author != "—":
        out.append(f'author: "{author}"')
    if transl:
        out.append(f'translator: "{transl}"')
    out += [f'source_format: "{src.get("format","")}"',
            f'slug: "{slug}"',
            "generated_by: render_markdown.py (canon-corpus)",
            "---", ""]
    out += [f"# {title}", ""]
    if author and author != "—":
        out.append(f"*{author}*" + (f", translated by {transl}" if transl else ""))
        out.append("")

    footnotes = []            # (fid, text)
    seen_path = []            # last emitted (level,label) chain
    fn_map = {}               # raw osis link → sequential fid

    for u in book["units"]:
        path, verse_no, is_verse = analyze(u["ref"], resolution)
        # emit headings for the shallowest level that changed (and deeper)
        changed_from = None
        for i, node in enumerate(path):
            if i >= len(seen_path) or seen_path[i] != node:
                changed_from = i
                break
        if changed_from is not None:
            for level, label in path[changed_from:]:
                out += ["", f'{"#" * min(level + 1, 6)} {tidy(str(label))}', ""]
        seen_path = path

        text = tidy(u["text"])
        if not text:
            continue

        # scripture footnotes — sequential ids keep the markdown clean
        for osis in u.get("links", []):
            if osis not in fn_map:
                fn_map[osis] = f"fn{len(fn_map) + 1}"
                footnotes.append((fn_map[osis], osis_pretty(osis)))
            text = text + f"[^{fn_map[osis]}]"

        if verse_no:                                      # scripture verse number
            out.append(f"**{verse_no}** {text}")
            out.append("")
        else:                                             # prose / verse / drama block
            out.append(text)
            out.append("")

    if footnotes:
        out += ["", "---", ""]
        for fid, txt in footnotes:
            out.append(f"[^{fid}]: {txt}")

    return "\n".join(out).rstrip() + "\n"

def main():
    args = [a for a in sys.argv[1:]]
    if args:
        slug = args[0]
        book = json.load(open(os.path.join(BOOKS, slug + ".json"), encoding="utf-8"))
        md = render(book)
        if len(args) > 1:
            open(args[1], "w", encoding="utf-8").write(md)
            print(f"{slug} → {args[1]} ({len(md):,} bytes)")
        else:
            sys.stdout.write(md)
        return
    os.makedirs(OUT, exist_ok=True)
    n = 0
    import glob
    for path in sorted(glob.glob(os.path.join(BOOKS, "*.json"))):
        if path.endswith("manifest.json"):
            continue
        book = json.load(open(path, encoding="utf-8"))
        md = render(book)
        dest = os.path.join(OUT, book["slug"] + ".md")
        open(dest, "w", encoding="utf-8").write(md)
        print(f"{book['slug']}: {len(md):,} bytes → {os.path.relpath(dest)}")
        n += 1
    print(f"MARKDOWN: {n} books → {os.path.relpath(OUT)}")

if __name__ == "__main__":
    main()
