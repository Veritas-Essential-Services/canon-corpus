#!/usr/bin/env python3
"""structure_texts.py — the structure layer: source texts -> unit-id JSON.

Three converters, one output shape (the Canon Corpus JSON design, vault:
"Canon Corpus JSON layer — design (2026-07-21)"):

  TEI  (Perseus, data/corpus/perseus/*.xml)  — canonical refs born-in
  ThML (CCEL,    data/corpus/ccel/*.xml)     — scripture keylinks born-in
  KJV  (Gutenberg data/corpus/kjv_bible.txt) — book chapter:verse, exact

Output: data/books/<slug>.json (gitignored — rebuildable) and
data/books/manifest.json (committed — checksums, schemes, provenance).

Every unit: {id, ref, text, links[]} — id is the citation hub
(canonical citation <-> unit id <-> any edition's page). The scheme's
`honesty` field states real resolution; we never pretend precision.

Run:  python3 pipeline/structure_texts.py          # build all available
"""
import os, re, json, hashlib, html
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "data", "corpus")
BOOKS = os.environ.get("BOOKS_OUT") or os.path.join(HERE, "..", "data", "books")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()

# ---------------------------------------------------------------- TEI (Perseus)

def tei_meta(root):
    ns = {"t": "http://www.tei-c.org/ns/1.0"}
    title = root.find(".//t:titleStmt/t:title", ns)
    author = root.find(".//t:titleStmt/t:author", ns)
    transl = root.find(".//t:titleStmt/t:editor[@role='translator']", ns)
    return (title.text if title is not None else "?",
            (author.text or "?") if author is not None else "?",
            (transl.text or "").strip() if transl is not None else "")

def convert_tei(path, slug, abbrev):
    """Books contain either 'card' divs (prose keyed to original lineation)
    or <l> lines (verse). Units: card, or 20-line block."""
    raw = open(path, encoding="utf-8").read()
    root = ET.fromstring(raw)
    title, author, transl = tei_meta(root)
    ns = {"t": "http://www.tei-c.org/ns/1.0"}
    units = []
    mode = None
    for book in root.iter("{http://www.tei-c.org/ns/1.0}div"):
        if book.get("subtype") != "book":
            continue
        bn = book.get("n")
        cards = [d for d in book.iter("{http://www.tei-c.org/ns/1.0}div")
                 if d.get("subtype") == "card"]
        if cards:
            mode = "cards"
            for c in cards:
                cn = c.get("n")
                text = clean(ET.tostring(c, encoding="unicode", method="text"))
                if text:
                    units.append({"id": f"{slug}:{bn}.{cn}",
                                  "ref": f"{abbrev} {bn}.{cn}",
                                  "text": text, "links": []})
        else:
            mode = "lines"
            lines = [(l.get("n"), clean(ET.tostring(l, encoding="unicode", method="text")))
                     for l in book.iter("{http://www.tei-c.org/ns/1.0}l")]
            lines = [(n, t) for n, t in lines if t]
            for i in range(0, len(lines), 20):
                block = lines[i:i + 20]
                lo = block[0][0] or str(i + 1); hi = block[-1][0] or str(i + len(block))
                units.append({"id": f"{slug}:{bn}.{lo}",
                              "ref": f"{abbrev} {bn}.{lo}-{hi}",
                              "text": " ".join(t for _, t in block), "links": []})
    honesty = ("cards anchored to original-language line numbers; prose translation, "
               "so refs are line-block anchors, not exact lines" if mode == "cards"
               else "translator's lineation, 20-line blocks; exact to the block")
    return {"slug": slug, "title": title, "author": author,
            "source": {"path": os.path.relpath(path, CORPUS), "format": "tei",
                       "translator": transl, "sha256": sha256(path)},
            "scheme": {"citation": f"{abbrev} book.line", "resolution": mode,
                       "honesty": honesty},
            "units": units}

# ---------------------------------------------------------------- ThML (CCEL)

RE_DIV2 = re.compile(r"<div[1-4]\b([^>]*)>", re.I)  # flat scan, any level — paragraphs belong to the preceding div
RE_ATTR = re.compile(r'(\w+)="([^"]*)"')
RE_PARA = re.compile(r"<p\b[^>]*>(.*?)</p>", re.S | re.I)
# osisRef prefix varies: "Bible:Rom.8.13" and "Bible.kjv:1John.4.8" both occur
RE_SCRIP = re.compile(r'<scripRef\b[^>]*osisRef="Bible[^:"]*:([^"]+)"[^>]*>', re.I)
# fallback: files with parsed="kjv|Rom|8|13|0|0" or "|Rom|8|13|0|0" and no osisRef
RE_SCRIP_PARSED = re.compile(r'<scripRef\b(?![^>]*osisRef=)[^>]*parsed="[a-z]*\|([1-3]?[A-Za-z]+)\|(\d+)\|(\d+)\|', re.I)
RE_TITLE = re.compile(r"<DC\.Title[^>]*>([^<]+)</DC\.Title>|<title>([^<]+)</title>", re.I)
RE_CREATOR_SHORT = re.compile(r'<DC\.Creator[^>]*sub="Author"[^>]*scheme="short-form"[^>]*>\s*([^<]*?)\s*<', re.I)
RE_CREATOR = re.compile(r'<DC\.Creator[^>]*sub="Author"[^>]*>\s*([^<]*?)\s*<', re.I)

def thml_author(raw, fallback):
    for rx in (RE_CREATOR_SHORT, RE_CREATOR):
        for m in rx.finditer(raw):
            name = m.group(1).strip()
            if name:
                return name
    return fallback

def convert_thml(path, slug):
    raw = open(path, encoding="utf-8", errors="replace").read()
    mt = RE_TITLE.search(raw)
    title = (mt.group(1) or mt.group(2)).strip() if mt else slug
    author = thml_author(raw, slug.split("-")[0].title())
    units = []
    divs = list(RE_DIV2.finditer(raw))
    if len(divs) < 2:  # no usable divisions — treat whole body as one
        class _Fake:  # minimal stand-in with the two methods used below
            def __init__(s, pos): s._p = pos
            def group(s, _): return ""
            def end(s): return s._p
            def start(s): return s._p
        divs = [_Fake(0)]
    for i, m in enumerate(divs):
        attrs = dict(RE_ATTR.findall(m.group(1)))
        did = attrs.get("id", f"d{i}")
        dtitle = attrs.get("shorttitle") or attrs.get("title") or attrs.get("type", "")
        seg = raw[m.end(): divs[i + 1].start() if i + 1 < len(divs) else len(raw)]
        for j, pm in enumerate(RE_PARA.finditer(seg), 1):
            ptext = clean(pm.group(1))
            if len(ptext) < 40:
                continue
            links = set(RE_SCRIP.findall(pm.group(1)))
            links |= {f"{b}.{c}.{v}" for b, c, v in RE_SCRIP_PARSED.findall(pm.group(1))}
            links = sorted(links)
            units.append({"id": f"{slug}:{did}-p{j}",
                          "ref": f"{dtitle}, par. {j}",
                          "text": ptext, "links": links})
    return {"slug": slug, "title": title, "author": author,
            "source": {"path": os.path.relpath(path, CORPUS), "format": "thml",
                       "sha256": sha256(path)},
            "scheme": {"citation": "CCEL section id + paragraph",
                       "resolution": "paragraph",
                       "honesty": "ThML section ids are CCEL's stable ids; page numbers "
                                  "of print editions need an anchor table (Concordance)"},
            "units": units}

# ---------------------------------------------------------------- KJV (Gutenberg)

KJV_BOOKS = [
    ("The First Book of Moses: Called Genesis", "Gen", "Genesis"),
    ("The Second Book of Moses: Called Exodus", "Exod", "Exodus"),
    ("The Third Book of Moses: Called Leviticus", "Lev", "Leviticus"),
    ("The Fourth Book of Moses: Called Numbers", "Num", "Numbers"),
    ("The Fifth Book of Moses: Called Deuteronomy", "Deut", "Deuteronomy"),
    ("The Book of Joshua", "Josh", "Joshua"),
    ("The Book of Judges", "Judg", "Judges"),
    ("The Book of Ruth", "Ruth", "Ruth"),
    ("The First Book of Samuel", "1Sam", "1 Samuel"),
    ("The Second Book of Samuel", "2Sam", "2 Samuel"),
    ("The First Book of the Kings", "1Kgs", "1 Kings"),
    ("The Second Book of the Kings", "2Kgs", "2 Kings"),
    ("The First Book of the Chronicles", "1Chr", "1 Chronicles"),
    ("The Second Book of the Chronicles", "2Chr", "2 Chronicles"),
    ("Ezra", "Ezra", "Ezra"),
    ("The Book of Nehemiah", "Neh", "Nehemiah"),
    ("The Book of Esther", "Esth", "Esther"),
    ("The Book of Job", "Job", "Job"),
    ("The Book of Psalms", "Ps", "Psalms"),
    ("The Proverbs", "Prov", "Proverbs"),
    ("Ecclesiastes", "Eccl", "Ecclesiastes"),
    ("The Song of Solomon", "Song", "Song of Solomon"),
    ("The Book of the Prophet Isaiah", "Isa", "Isaiah"),
    ("The Book of the Prophet Jeremiah", "Jer", "Jeremiah"),
    ("The Lamentations of Jeremiah", "Lam", "Lamentations"),
    ("The Book of the Prophet Ezekiel", "Ezek", "Ezekiel"),
    ("The Book of Daniel", "Dan", "Daniel"),
    ("Hosea", "Hos", "Hosea"),
    ("Joel", "Joel", "Joel"),
    ("Amos", "Amos", "Amos"),
    ("Obadiah", "Obad", "Obadiah"),
    ("Jonah", "Jonah", "Jonah"),
    ("Micah", "Mic", "Micah"),
    ("Nahum", "Nah", "Nahum"),
    ("Habakkuk", "Hab", "Habakkuk"),
    ("Zephaniah", "Zeph", "Zephaniah"),
    ("Haggai", "Hag", "Haggai"),
    ("Zechariah", "Zech", "Zechariah"),
    ("Malachi", "Mal", "Malachi"),
    ("The Gospel According to Saint Matthew", "Matt", "Matthew"),
    ("The Gospel According to Saint Mark", "Mark", "Mark"),
    ("The Gospel According to Saint Luke", "Luke", "Luke"),
    ("The Gospel According to Saint John", "John", "John"),
    ("The Acts of the Apostles", "Acts", "Acts"),
    ("The Epistle of Paul the Apostle to the Romans", "Rom", "Romans"),
    ("The First Epistle of Paul the Apostle to the Corinthians", "1Cor", "1 Corinthians"),
    ("The Second Epistle of Paul the Apostle to the Corinthians", "2Cor", "2 Corinthians"),
    ("The Epistle of Paul the Apostle to the Galatians", "Gal", "Galatians"),
    ("The Epistle of Paul the Apostle to the Ephesians", "Eph", "Ephesians"),
    ("The Epistle of Paul the Apostle to the Philippians", "Phil", "Philippians"),
    ("The Epistle of Paul the Apostle to the Colossians", "Col", "Colossians"),
    ("The First Epistle of Paul the Apostle to the Thessalonians", "1Thess", "1 Thessalonians"),
    ("The Second Epistle of Paul the Apostle to the Thessalonians", "2Thess", "2 Thessalonians"),
    ("The First Epistle of Paul the Apostle to Timothy", "1Tim", "1 Timothy"),
    ("The Second Epistle of Paul the Apostle to Timothy", "2Tim", "2 Timothy"),
    ("The Epistle of Paul the Apostle to Titus", "Titus", "Titus"),
    ("The Epistle of Paul the Apostle to Philemon", "Phlm", "Philemon"),
    ("The Epistle of Paul the Apostle to the Hebrews", "Heb", "Hebrews"),
    ("The General Epistle of James", "Jas", "James"),
    ("The First Epistle General of Peter", "1Pet", "1 Peter"),
    ("The Second General Epistle of Peter", "2Pet", "2 Peter"),
    ("The First Epistle General of John", "1John", "1 John"),
    ("The Second Epistle General of John", "2John", "2 John"),
    ("The Third Epistle General of John", "3John", "3 John"),
    ("The General Epistle of Jude", "Jude", "Jude"),
    ("The Revelation of Saint John the Divine", "Rev", "Revelation"),
]
TITLE2OSIS = {t: (o, n) for t, o, n in KJV_BOOKS}
RE_VMARK = re.compile(r"(?:(?<=^)|(?<=\s))(\d+):(\d+)\s+")  # markers appear inline too

def convert_kjv(path, slug="kjv"):
    units, cur = [], None
    book_osis = book_name = None
    seen_titles = set()
    skip_alias = False   # "Otherwise Called:" / "Commonly Called:" precede
    with open(path, encoding="utf-8", errors="replace") as f:  # Vulgate-style alternate titles — never book starts
        for line in f:
            t = line.strip()
            if not t:
                continue
            if t in ("Otherwise Called:", "Commonly Called:"):
                skip_alias = True
                continue
            if skip_alias:
                skip_alias = False
                continue   # the alias title itself — ignore entirely
            if t in TITLE2OSIS:
                # first occurrence is the TOC; a repeat = the book actually starts
                if t in seen_titles:
                    book_osis, book_name = TITLE2OSIS[t]
                else:
                    seen_titles.add(t)
                continue
            if not book_osis or not t:
                continue
            marks = list(RE_VMARK.finditer(t))
            if not marks:
                if cur:
                    cur["text"] += " " + t
                continue
            lead = t[:marks[0].start()].strip()
            if cur and lead:
                cur["text"] += " " + lead
            for k, m in enumerate(marks):
                if cur:
                    units.append(cur)
                c, v = m.groups()
                seg = t[m.end(): marks[k + 1].start() if k + 1 < len(marks) else len(t)].strip()
                cur = {"id": f"{slug}:{book_osis}.{c}.{v}",
                       "ref": f"{book_name} {c}:{v}", "text": seg, "links": []}
    if cur:
        units.append(cur)
    return {"slug": slug, "title": "The Holy Bible (KJV)", "author": "—",
            "source": {"path": os.path.relpath(path, CORPUS), "format": "gutenberg-txt",
                       "sha256": sha256(path)},
            "scheme": {"citation": "Book chapter:verse (OSIS ids)",
                       "resolution": "verse", "honesty": "exact"},
            "units": units}

# ---------------------------------------------------------------- Gutenberg .txt

def strip_boilerplate(raw):
    m = re.search(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG.*?\*\*\*", raw, re.I)
    if m:
        raw = raw[m.end():]
    m = re.search(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG", raw, re.I)
    if m:
        raw = raw[:m.start()]
    return raw

def _flush_verse(units, slug, abbr, div, lines):
    """Chunk a division's lines into 12-line blocks with running line refs."""
    for i in range(0, len(lines), 12):
        block = lines[i:i + 12]
        start = i + 1
        units.append({"id": f"{slug}:{div}.{start}",
                      "ref": f"{abbr} {div}.{start}", "text": " ".join(block),
                      "links": []})

def convert_gutenberg_verse(path, slug, title, author, abbr, divre, cantica=None):
    """Verse works: divisions (book/canto), 12-line blocks. `cantica` maps a
    higher header (HELL->Inf) so Divine Comedy gets Inf/Purg/Par prefixes.
    Contents-list entries collapse: their between-heading segment is empty."""
    raw = strip_boilerplate(open(path, encoding="utf-8", errors="replace").read())
    units, div, cur_cantica, buf = [], None, "", []
    DIV = re.compile(divre)
    CANT = re.compile(cantica[0]) if cantica else None
    for line in raw.splitlines():
        t = line.strip()
        if CANT:
            cm = CANT.match(t)
            if cm:
                cur_cantica = cantica[1].get(cm.group(1).upper(), cm.group(1))
                continue
        dm = DIV.match(t)
        if dm:
            if div is not None:
                _flush_verse(units, slug, abbr, div, buf)
            label = next((g for g in dm.groups() if g), dm.group(0))
            div = f"{cur_cantica}{label}" if cur_cantica else label
            buf = []
            continue
        if div is not None and t:
            buf.append(t)
    if div is not None:
        _flush_verse(units, slug, abbr, div, buf)
    return {"slug": slug, "title": title, "author": author,
            "source": {"path": os.path.relpath(path, CORPUS), "format": "gutenberg-txt",
                       "sha256": sha256(path)},
            "scheme": {"citation": f"{abbr} division.line", "resolution": "line-block",
                       "honesty": "division exact; line = running line within division "
                                  "(translation lineation), 12-line blocks"},
            "units": units}

def convert_gutenberg_prose(path, slug, title, author, chapre):
    """Prose: paragraphs grouped under detected chapter headings."""
    raw = strip_boilerplate(open(path, encoding="utf-8", errors="replace").read())
    CH = re.compile(chapre) if chapre else None
    units, chap, pnum = [], None, 0
    for para in re.split(r"\n\s*\n", raw):
        p = re.sub(r"\s+", " ", para).strip()
        if not p:
            continue
        if CH and CH.match(p) and len(p) < 90:
            chap = p.rstrip(".")
            pnum = 0
            continue
        pnum += 1
        ref = f"{chap}, par. {pnum}" if chap else f"par. {pnum}"
        cid = f"{slug}:{(chap or 'x').replace(' ', '_')}.{pnum}"
        units.append({"id": cid, "ref": ref, "text": p, "links": []})
    return {"slug": slug, "title": title, "author": author,
            "source": {"path": os.path.relpath(path, CORPUS), "format": "gutenberg-txt",
                       "sha256": sha256(path)},
            "scheme": {"citation": "chapter + paragraph", "resolution": "paragraph",
                       "honesty": "chapter headings detected; paragraph running within chapter"},
            "units": units}

RE_SH_ACT = re.compile(r"^ACT\s+([IVXL]+)", re.I)
RE_SH_SCENE = re.compile(r"^SCENE\s+([IVXL0-9]+)", re.I)
RE_SH_PLAY = re.compile(r"^[A-Z][A-Z0-9 ,'&-]{5,58}$")
SH_NOTPLAY = re.compile(r"^(ACT|SCENE|CONTENTS|DRAMATIS|PROLOGUE|EPILOGUE|CHORUS|"
                        r"THE END|FINIS|INDUCTION|PERSONS|THE PERSONS)\b", re.I)

def convert_shakespeare(path, slug="shakespeare"):
    """Complete Works (Gutenberg 100): play -> act -> scene -> speech-block.
    Play = ALL-CAPS heading (no trailing period) whose next ~10 lines contain
    an ACT or 'Contents' marker; disambiguates play titles from SPEAKER lines."""
    raw = strip_boilerplate(open(path, encoding="utf-8", errors="replace").read())
    lines = raw.splitlines()
    units = []
    play = act = scene = None
    pidx = bidx = 0
    buf = []
    def flush():
        nonlocal buf, bidx
        text = " ".join(x.strip() for x in buf if x.strip()).strip()
        buf = []
        if text and play:
            bidx_local = len(units)
            loc = f"{play}"
            if act: loc += f", Act {act}"
            if scene: loc += f" Sc. {scene}"
            units.append({"id": f"{slug}:{pidx}.{bidx}", "ref": loc,
                          "text": text, "links": []})
    for i, line in enumerate(lines):
        t = line.strip()
        am = RE_SH_ACT.match(t)
        if am:
            flush(); act, scene = am.group(1), None; continue
        sm = RE_SH_SCENE.match(t)
        if sm:
            flush(); scene = sm.group(1); continue
        if (RE_SH_PLAY.match(t) and not t.endswith(".") and not SH_NOTPLAY.match(t)):
            lookahead = "\n".join(lines[i + 1:i + 11])
            if re.search(r"^\s*(ACT\s+[IVX]|Contents|Dramatis)", lookahead, re.M | re.I):
                flush()
                play, act, scene = t.title(), None, None
                pidx += 1; bidx = 0
                continue
        if not t:
            if buf: flush(); bidx += 1
        else:
            buf.append(t)
    flush()
    return {"slug": slug, "title": "The Complete Works of William Shakespeare",
            "author": "William Shakespeare",
            "source": {"path": os.path.relpath(path, CORPUS), "format": "gutenberg-txt",
                       "sha256": sha256(path)},
            "scheme": {"citation": "Play, Act Scene (speech-block)", "resolution": "speech-block",
                       "honesty": "play/act/scene detected from headings; block = speech or "
                                  "paragraph within scene, not through-numbered line"},
            "units": [u for u in units if len(u["text"]) > 1]}

# slug -> converter job. Verse works give (abbr, division-regex[, cantica]).
GUTEN_VERSE = {
    "paradise_lost": ("Paradise Lost", "John Milton", "PL", r"^BOOK\s+([IVXLC]+)", None),
    "paradise_regained": ("Paradise Regained", "John Milton", "PR",
                          r"^THE\s+(FIRST|SECOND|THIRD|FOURTH)\s+BOOK", None),
    "divine_comedy": ("The Divine Comedy", "Dante Alighieri (tr. Cary)", "DC",
                      r"^CANTO\s+([IVXLC]+)",
                      (r"^(HELL|PURGATORY|PARADISE)$", {"HELL": "Inf.", "PURGATORY": "Purg.", "PARADISE": "Par."})),
    "beowulf": ("Beowulf", "tr. Francis B. Gummere", "Beo", r"^([IVXLC]+)\."),
    "faust": ("Faust, Part I", "Goethe (tr. Bayard Taylor)", "Faust",
              r"^SCENE\s+([IVXL]+)|^(PROLOGUE IN HEAVEN)$"),
}
GUTEN_PROSE = {
    "gilgamesh": ("The Gilgamesh Epic (Old Babylonian)", "tr. Morris Jastrow & A. Clay",
                  r"^(TABLET|COLUMN|CHAPTER|PART)\b"),
    "treasure_island": ("Treasure Island", "Robert Louis Stevenson",
                        r"^(PART\s+\w+|Chapter\s+\d+|[0-9]+\.)"),
}

# ---------------------------------------------------------------- driver

def main():
    os.makedirs(BOOKS, exist_ok=True)
    manifest = {}
    jobs = []
    kjv = os.path.join(CORPUS, "kjv_bible.txt")
    if os.path.exists(kjv):
        jobs.append(("kjv", lambda: convert_kjv(kjv)))
    tei_abbrevs = {"iliad-butler": "Il.", "odyssey-eng4": "Od.", "aeneid-williams": "Aen."}
    pdir = os.path.join(CORPUS, "perseus")
    if os.path.isdir(pdir):
        for fn in sorted(os.listdir(pdir)):
            slug = fn[:-4]
            path = os.path.join(pdir, fn)
            jobs.append((slug, lambda p=path, s=slug: convert_tei(p, s, tei_abbrevs.get(s, s))))
    cdir = os.path.join(CORPUS, "ccel")
    if os.path.isdir(cdir):
        for fn in sorted(os.listdir(cdir)):
            slug = fn[:-4]
            path = os.path.join(cdir, fn)
            jobs.append((slug, lambda p=path, s=slug: convert_thml(p, s)))
    # Gutenberg .txt shelf
    for slug, spec in GUTEN_VERSE.items():
        path = os.path.join(CORPUS, slug + ".txt")
        if os.path.exists(path):
            title, author, abbr, divre = spec[0], spec[1], spec[2], spec[3]
            cantica = spec[4] if len(spec) > 4 else None
            jobs.append((slug, lambda p=path, s=slug, t=title, a=author, ab=abbr,
                         d=divre, c=cantica: convert_gutenberg_verse(p, s, t, a, ab, d, c)))
    for slug, (title, author, chapre) in GUTEN_PROSE.items():
        path = os.path.join(CORPUS, slug + ".txt")
        if os.path.exists(path):
            jobs.append((slug, lambda p=path, s=slug, t=title, a=author, c=chapre:
                         convert_gutenberg_prose(p, s, t, a, c)))
    shk = os.path.join(CORPUS, "shakespeare.txt")
    if os.path.exists(shk):
        jobs.append(("shakespeare", lambda: convert_shakespeare(shk)))
    force = "--force" in os.sys.argv
    for slug, job in jobs:
        out = os.path.join(BOOKS, slug + ".json")
        if os.path.exists(out) and not force:   # resumable: reuse, still record in manifest
            book = json.load(open(out, encoding="utf-8"))
            manifest[slug] = {"title": book["title"], "author": book["author"],
                              "format": book["source"]["format"],
                              "sha256": book["source"]["sha256"],
                              "units": len(book["units"]), "scheme": book["scheme"]}
            print(f"{slug}: {len(book['units'])} units (kept)")
            continue
        book = job()
        seen = {}                       # guarantee unique unit ids (stable refs)
        for u in book["units"]:
            if u["id"] in seen:
                seen[u["id"]] += 1
                u["id"] = f"{u['id']}~{seen[u['id']]}"
            else:
                seen[u["id"]] = 1
        with open(out + ".tmp", "w", encoding="utf-8") as f:   # atomic write
            json.dump(book, f, ensure_ascii=False)
        os.replace(out + ".tmp", out)
        manifest[slug] = {"title": book["title"], "author": book["author"],
                          "format": book["source"]["format"],
                          "sha256": book["source"]["sha256"],
                          "units": len(book["units"]),
                          "scheme": book["scheme"]}
        print(f"{slug}: {len(book['units'])} units — {book['title']}")
    with open(os.path.join(BOOKS, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, ensure_ascii=False)
    print(f"MANIFEST: {len(manifest)} books")

if __name__ == "__main__":
    main()
