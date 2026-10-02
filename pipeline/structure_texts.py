#!/usr/bin/env python3
# prov: 2026-07-22 claude-fable-5 drafted (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-06 claude-opus-5 edited (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-07 claude-opus-5 edited (from git trailer; backfilled 2026-09-30)
# fable_review: pending
"""structure_texts.py — the structure layer: source texts -> unit-id JSON.

Three converters, one output shape (the Canon Corpus JSON design, vault:
"Canon Corpus JSON layer — design (2026-07-21)"):

  TEI  (Perseus, data/corpus/perseus/*.xml)  — canonical refs born-in
  ThML (CCEL,    data/corpus/ccel/*.xml)     — scripture keylinks born-in
  KJV  (Gutenberg data/corpus/kjv_bible.txt) — book chapter:verse, exact
  LEXICON (data/corpus/lexicons/*)           — reference works keyed by lemma:
                                               Strong's H/G, Brown-Driver-Briggs

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

# Per-book corrections to a CCEL head, kept here so they rerun on refetch
# (rule 2: never hand-edit a source). rightworld's short-form creator is
# misspelt "G. K. Chesteron" on CCEL.
THML_AUTHOR_FIX = {"chesterton-rightworld": "G. K. Chesterton"}
# Books whose verse CCEL set in <pre> rather than <p> (read stanza by stanza).
# Opt-in per slug so no existing book's unit ids can move.
THML_PRE_VERSE = {"chesterton-whitehorse"}
RE_PRE = re.compile(r"<pre\b[^>]*>(.*?)</pre>", re.S | re.I)

def convert_thml(path, slug):
    raw = open(path, encoding="utf-8", errors="replace").read()
    mt = RE_TITLE.search(raw)
    title = (mt.group(1) or mt.group(2)).strip() if mt else slug
    author = THML_AUTHOR_FIX.get(slug) or thml_author(raw, slug.split("-")[0].title())
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
        if slug in THML_PRE_VERSE:
            # verse set in <pre>: one unit per stanza, lineation kept
            k = 0
            for pre in RE_PRE.finditer(seg):
                body = html.unescape(re.sub(r"<[^>]+>", "", pre.group(1)))
                for st in re.split(r"\n\s*\n", body):
                    lines = [l.strip() for l in st.strip("\n").splitlines() if l.strip()]
                    if not lines:
                        continue
                    k += 1
                    units.append({"id": f"{slug}:{did}-s{k}",
                                  "ref": f"{dtitle}, st. {k}",
                                  "text": "\n".join(lines), "links": []})
    return {"slug": slug, "title": title, "author": author,
            "source": {"path": os.path.relpath(path, CORPUS), "format": "thml",
                       "sha256": sha256(path)},
            "scheme": {"citation": "CCEL section id + paragraph",
                       "resolution": "paragraph",
                       "honesty": "ThML section ids are CCEL's stable ids; page numbers "
                                  "of print editions need an anchor table (Concordance)"},
            "units": units}

def _kjv_field_rights(map_rel):
    """The rights of each unit's `kjv` field, which comes from a TVTMS-derived
    map (CC BY 4.0), not from the public-domain text it sits beside."""
    return {"from": map_rel, "license": "CC BY 4.0",
            "attribution": "Data created by www.STEPBible.org based on work at Tyndale "
                           "House Cambridge (CC BY 4.0)",
            "source_url": "https://github.com/STEPBible/STEPBible-Data",
            "redistribute_whole": False}

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
RE_VMARK = re.compile(r"(?:(?<=^)|(?<=\s))(\d+):(\d+)(?:\s+|$)")  # markers appear inline too,
# and -- the 420-verse bug, fixed 2026-09-11 -- at END OF LINE. Gutenberg hard-wraps
# at ~70 chars; when the wrap falls immediately after a marker there is no trailing
# whitespace for \s+ to match, so the marker was read as body text and its whole verse
# merged into the previous one. 420 of 31,102 verses vanished this way, scattered over
# 60+ books, while scheme.honesty still said "exact".

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
                    cur["text"] = (cur["text"] + " " + t).strip() if cur["text"] else t
                continue
            lead = t[:marks[0].start()].strip()
            if cur and lead:
                cur["text"] = (cur["text"] + " " + lead).strip() if cur["text"] else lead
            for k, m in enumerate(marks):
                if cur:
                    units.append(cur)
                c, v = m.groups()
                seg = t[m.end(): marks[k + 1].start() if k + 1 < len(marks) else len(t)].strip()
                cur = {"id": f"{slug}:{book_osis}.{c}.{v}",
                       "ref": f"{book_name} {c}:{v}", "text": seg, "links": []}
                # seg is "" when the marker ended the line; the next line fills it
    if cur:
        units.append(cur)
    return {"slug": slug, "title": "The Holy Bible (KJV)", "author": "—",
            "source": {"path": os.path.relpath(path, CORPUS), "format": "gutenberg-txt",
                       "sha256": sha256(path)},
            "scheme": {"citation": "Book chapter:verse (OSIS ids)",
                       "resolution": "verse", "honesty": "exact"},
            "units": units}

# ---------------------------------------------------------------- Vulgate
#
# The Clementine Vulgate (1592), from the Clementine Vulgate Project's own
# files (fetch_sources.VULGATE, pinned). One file per book, one line per
# verse, "chapter:verse text". The project's markup, read from its files
# (counts measured 2026-10-02 over all 35,809 verses):
#     /        a line break inside poetry            28,860
#     \        a paragraph break (2,058 of 2,085 at a verse's end)
#     [ ... ]  a stretch set as poetry; it opens and closes mid-verse too
#     <Name>   a speaker heading (the Song of Songs: Sponsa, Sponsus, Chorus)
# `text` is the verse with the markup turned into layout ("/" a newline,
# "\" a blank line, brackets dropped, speakers lifted into `speakers`);
# `marked` is the line exactly as the file has it, so nothing is lost and
# the change is plain to see (the project asks that modifications be clear).
#
# WHAT IS NOT CLAIMED (rule 4): ids are in the VULGATE's own numbering, which
# is not the KJV's. Its Psalms follow the Greek count (Vulgate Ps 50 is KJV
# Ps 51) and count a title in verse 1, as the Hebrew does; Daniel 3
# carries the Song of the Three Children (3:24-90) and Esther its Greek
# additions (10:4-16:24). So `vulgate:Ps.50.3` stays a citation in the
# Vulgate, and no Word Hoard uid is minted here. Each unit's `kjv` says which
# KJV verse holds the same text, by the map data/versification/vulgate-kjv.json
# (pipeline/build_vulgate_versification.py, STEPBible TVTMS run against this
# very text): {"resolved": true, "target": "kjv:Ps.51.1"}, with `spans` when
# the verse holds several KJV verses; or {"resolved": false, "why": ...} for a
# psalm title (the KJV numbers none) or text the KJV's canon does not hold.

VULGATE_BOOKS = {   # file -> (OSIS, the book's Latin name)
    "Gn": ("Gen", "Genesis"), "Ex": ("Exod", "Exodus"), "Lv": ("Lev", "Leviticus"),
    "Nm": ("Num", "Numeri"), "Dt": ("Deut", "Deuteronomium"), "Jos": ("Josh", "Josue"),
    "Jdc": ("Judg", "Judicum"), "Rt": ("Ruth", "Ruth"), "1Rg": ("1Sam", "1 Regum"),
    "2Rg": ("2Sam", "2 Regum"), "3Rg": ("1Kgs", "3 Regum"), "4Rg": ("2Kgs", "4 Regum"),
    "1Par": ("1Chr", "1 Paralipomenon"), "2Par": ("2Chr", "2 Paralipomenon"),
    "Esr": ("Ezra", "1 Esdrae"), "Neh": ("Neh", "Nehemiae"), "Tob": ("Tob", "Tobiae"),
    "Jdt": ("Jdt", "Judith"), "Est": ("Esth", "Esther"), "Job": ("Job", "Job"),
    "Ps": ("Ps", "Psalmi"), "Pr": ("Prov", "Proverbia"), "Ecl": ("Eccl", "Ecclesiastes"),
    "Ct": ("Song", "Canticum Canticorum"), "Sap": ("Wis", "Sapientia"),
    "Sir": ("Sir", "Ecclesiasticus"), "Is": ("Isa", "Isaias"), "Jr": ("Jer", "Jeremias"),
    "Lam": ("Lam", "Lamentationes"), "Bar": ("Bar", "Baruch"), "Ez": ("Ezek", "Ezechiel"),
    "Dn": ("Dan", "Daniel"), "Os": ("Hos", "Osee"), "Joel": ("Joel", "Joel"),
    "Am": ("Amos", "Amos"), "Abd": ("Obad", "Abdias"), "Jon": ("Jonah", "Jonas"),
    "Mch": ("Mic", "Michaea"), "Nah": ("Nah", "Nahum"), "Hab": ("Hab", "Habacuc"),
    "Soph": ("Zeph", "Sophonias"), "Agg": ("Hag", "Aggaeus"), "Zach": ("Zech", "Zacharias"),
    "Mal": ("Mal", "Malachias"), "1Mcc": ("1Macc", "1 Machabaeorum"),
    "2Mcc": ("2Macc", "2 Machabaeorum"), "Mt": ("Matt", "Matthaeus"), "Mc": ("Mark", "Marcus"),
    "Lc": ("Luke", "Lucas"), "Jo": ("John", "Joannes"), "Act": ("Acts", "Actus Apostolorum"),
    "Rom": ("Rom", "ad Romanos"), "1Cor": ("1Cor", "1 ad Corinthios"),
    "2Cor": ("2Cor", "2 ad Corinthios"), "Gal": ("Gal", "ad Galatas"),
    "Eph": ("Eph", "ad Ephesios"), "Phlp": ("Phil", "ad Philippenses"),
    "Col": ("Col", "ad Colossenses"), "1Thes": ("1Thess", "1 ad Thessalonicenses"),
    "2Thes": ("2Thess", "2 ad Thessalonicenses"), "1Tim": ("1Tim", "1 ad Timotheum"),
    "2Tim": ("2Tim", "2 ad Timotheum"), "Tit": ("Titus", "ad Titum"),
    "Phlm": ("Phlm", "ad Philemonem"), "Hbr": ("Heb", "ad Hebraeos"),
    "Jac": ("Jas", "Jacobi"), "1Ptr": ("1Pet", "1 Petri"), "2Ptr": ("2Pet", "2 Petri"),
    "1Jo": ("1John", "1 Joannis"), "2Jo": ("2John", "2 Joannis"), "3Jo": ("3John", "3 Joannis"),
    "Jud": ("Jude", "Judae"), "Apc": ("Rev", "Apocalypsis"),
}
RE_VULG_LINE = re.compile(r"^(\d+):(\d+)\s(.*)$")
RE_VULG_SPEAKER = re.compile(r"<([^>]*)>")


def vulgate_layout(marked):
    """(text, speakers) for one verse's marked-up line."""
    speakers = [m.strip() for m in RE_VULG_SPEAKER.findall(marked)]
    t = RE_VULG_SPEAKER.sub(" ", marked).replace("[", "").replace("]", "")
    t = t.replace("\\", "\n\n").replace("/", "\n")
    t = "\n".join(re.sub(r"[ \t]+", " ", ln).strip() for ln in t.split("\n"))
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t, speakers


def _dc_map():
    """The deuterocanon map (data/versification/deuterocanon.json), or None."""
    import versification as _V
    return _V.load(_V.DC_PATH) if os.path.exists(_V.DC_PATH) else None


def _dc_key(u, ref, slug, dmap, tally):
    """Give a deuterocanonical unit its shared key, `kjva` (resolve_dc)."""
    import versification as _V
    if dmap and slug in dmap["witnesses"]:
        k = _V.resolve_dc(ref, slug, dmap)
        if k is not None:
            u["kjva"] = k
            tally[k["resolved"]] += 1


def _dc_scheme(tally):
    return ({"kjva_keyed": tally[True], "kjva_unkeyed": tally[False],
             "kjva_note": "deuterocanonical verses carry `kjva`: the shared key, the KJV "
                          "Apocrypha verse holding the same text, by "
                          "data/versification/deuterocanon.json (the house's reading, PD), "
                          "or why there is none; `weak` marks a pairing to read first"}
            if tally[True] or tally[False] else {})


def convert_vulgate(vdir, books, digest, slug="vulgate"):
    """`books`: file names in canonical order; `digest`: the pinned digest."""
    import sys as _sys
    if HERE not in _sys.path:       # loaded by path (the tests do), not as a script
        _sys.path.insert(0, HERE)
    import versification as _V
    vmap, kjv_ids = None, set()
    if os.path.exists(_V.VULGATE_PATH):
        vmap = _V.load(_V.VULGATE_PATH)
        with open(os.path.join(HERE, "..", "data", "uids", "wordhoard.uids.json"), encoding="utf-8") as f:
            kjv_ids = {k for k in json.load(f)["uids"] if k.startswith("kjv:")}
    resolved = {True: 0, False: 0}
    dmap, dc = _dc_map(), {True: 0, False: 0}
    units = []
    for b in books:
        osis, name = VULGATE_BOOKS[b]
        with open(os.path.join(vdir, b + ".lat"), encoding="cp1252") as f:
            for n, line in enumerate(f, 1):
                line = line.rstrip("\r\n")
                if not line.strip():
                    continue
                m = RE_VULG_LINE.match(line)
                if not m:
                    raise ValueError(f"{b}.lat line {n}: not 'chapter:verse text'")
                c, v, marked = m.groups()
                text, speakers = vulgate_layout(marked)
                u = {"id": f"{slug}:{osis}.{c}.{v}", "ref": f"{name} {c}:{v}",
                     "text": text, "links": [], "marked": marked}
                if speakers:
                    u["speakers"] = speakers
                if vmap:
                    u["kjv"] = _V.resolve_vulgate(f"{osis}.{c}.{v}", vmap, kjv_ids)
                    resolved[u["kjv"]["resolved"]] += 1
                _dc_key(u, f"{osis}.{c}.{v}", slug, dmap, dc)
                units.append(u)
    return {"slug": slug, "title": "Biblia Sacra Vulgatae Editionis (Clementine Vulgate, 1592)",
            "author": "—",
            "source": {"path": os.path.relpath(vdir, CORPUS), "format": "clementine-lat",
                       "sha256": digest,
                       "sha256_of": "name<TAB>sha256 lines of the book files, sorted"},
            "scheme": {"citation": "Book chapter:verse in the Vulgate's own numbering (OSIS book ids)",
                       "resolution": "verse", "honesty": "exact",
                       "versification": "vulgate",
                       "kjv_resolved": resolved[True], "kjv_unresolved": resolved[False],
                       **_dc_scheme(dc),
                       "note": "Ids follow the Clementine numbering, NOT the KJV's: the "
                               "Psalms are numbered as in the Greek (Vulgate Ps 50 = KJV "
                               "Ps 51) with a title counted in verse 1, Daniel 3 holds 3:24-90 "
                               "and Esther 10:4-16:24 the Greek additions. Each unit's `kjv` "
                               "names the KJV verse(s) holding the same text, by the map "
                               "data/versification/vulgate-kjv.json (STEPBible TVTMS, CC BY "
                               "4.0, tested against this text), or says why there is none; "
                               "no uids minted. `text` is the verse with the "
                               "project's markup turned into line and paragraph breaks; "
                               "`marked` is the file's line as is. The Clementine appendix "
                               "(Prayer of Manasses, 3-4 Esdras) is not in the source."},
            "rights": {"license": "public-domain",
                       "attribution": "The Clementine Vulgate Project (vulsearch.sourceforge.net)",
                       "source_url": "https://github.com/BibleGet-I-O/Clementine-Vulgate",
                       "requests": "acknowledge the source; report typographical errors to the "
                                   "project; make modifications clear (requests, not a licence)",
                       "kjv_field": _kjv_field_rights("data/versification/vulgate-kjv.json")},
            "units": units}

# ---------------------------------------------------------------- Douay-Rheims
#
# The Douay-Rheims, Challoner revision (fetch_sources.DOUAY, pinned): the
# Vulgate's English companion. One JSON file, books -> chapters -> verses, its
# first 73 books in the Clementine's order and, nearly everywhere, the
# Clementine's numbering. So a unit's id is in that numbering (douay:Ps.50.3)
# and `vulgate` names the Clementine verse(s) holding the same text: the same
# number, except at DOUAY_ROWS, where this edition breaks verses elsewhere.
# `kjv` follows through the Vulgate map (data/versification/vulgate-kjv.json).
#
# WHAT IS NOT CLAIMED (rule 4): the file pads its versification with EMPTY
# verses where the KJV numbers a verse it has not got (John 11:57, 2 Cor
# 1:24, 1 Thess 4:18 ...). An empty verse is no verse of the Douay: it is
# dropped, and counted in the scheme, never given an id. DOUAY_ROWS was found
# by aligning this English against the KJV's (build_vulgate_versification.py
# --audit-douay) and read verse by verse against the Latin.

DOUAY_NAMES = [   # the file's own book names, in order: a reordered file fails loudly
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges",
    "Ruth", "I Samuel", "II Samuel", "I Kings", "II Kings", "I Chronicles",
    "II Chronicles", "Ezra", "Nehemiah", "Tobit", "Judith", "Esther", "Job", "Psalms",
    "Proverbs", "Ecclesiastes", "Song of Solomon", "Wisdom", "Sirach", "Isaiah",
    "Jeremiah", "Lamentations", "Baruch", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
    "Malachi", "I Maccabees", "II Maccabees", "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "I Corinthians", "II Corinthians", "Galatians", "Ephesians", "Philippians",
    "Colossians", "I Thessalonians", "II Thessalonians", "I Timothy", "II Timothy",
    "Titus", "Philemon", "Hebrews", "James", "I Peter", "II Peter", "I John", "II John",
    "III John", "Jude", "Revelation of John"]

# Douay verse -> (the Clementine verse(s) holding its text, words that stand in
# the Douay verse), where that is not the verse of the same number. Each was
# read against the Latin; the words are checked, so a changed file fails loudly.
DOUAY_ROWS = {
    # A third element names the KJV verse(s) outright, where the Douay splits a
    # Clementine verse that holds several KJV verses (Clementine Ps 15:10 is the
    # KJV's 16:10-11; the Douay's 15:10 and 15:11 are one each).
    "Ps.15.10": (["Ps.15.10"], "not leave my soul in hell", ["Ps.16.10"]),
    "Ps.15.11": (["Ps.15.10"], "made known to me the ways of life", ["Ps.16.11"]),
    "Ps.42.5": (["Ps.42.4", "Ps.42.5"], "give praise upon the harp"),
    "Ps.42.6": (["Ps.42.5"], "Hope in God"),
    "Ps.125.7": (["Ps.125.6"], "carrying their sheaves"),
    "Ps.135.27": (["Ps.135.26"], "Lord of lords"),
    "Isa.45.24": (["Isa.45.23"], "every knee shall be bowed"),
    "Isa.45.25": (["Isa.45.24"], "In the Lord are my justices"),
    "Isa.45.26": (["Isa.45.25"], "seed of Israel be justified"),
    "Acts.8.8": (["Acts.8.7"], "taken with the palsy"),
    "Acts.8.9": (["Acts.8.8", "Acts.8.9"], "great joy in that city"),
    "1Thess.4.11": (["1Thess.4.11", "1Thess.4.12"], "walk honestly"),
    "1Thess.4.12": (["1Thess.4.13"], "concerning them that are asleep"),
    "1Thess.4.13": (["1Thess.4.14"], "Jesus died and rose again"),
    "1Thess.4.14": (["1Thess.4.15"], "in the word of the Lord"),
    "1Thess.4.15": (["1Thess.4.16"], "voice of an archangel"),
    "1Thess.4.16": (["1Thess.4.17"], "taken up together with them"),
    "1Thess.4.17": (["1Thess.4.18"], "comfort ye one another"),
    "2Thess.2.10": (["2Thess.2.10", "2Thess.2.11"], "operation of error"),
    "2Thess.2.11": (["2Thess.2.12"], "That all may be judged"),
    "2Thess.2.12": (["2Thess.2.13"], "give thanks to God always"),
    "2Thess.2.13": (["2Thess.2.14"], "called you by our gospel"),
    "2Thess.2.14": (["2Thess.2.15"], "hold the traditions"),
    "2Thess.2.15": (["2Thess.2.16"], "who hath loved us"),
    "2Thess.2.16": (["2Thess.2.17"], "Exhort your hearts"),
}


def douay_vulgate(ref, vchapters):
    """The Clementine verse(s) Douay verse `ref` ('Ps.42.6') reads."""
    if ref in DOUAY_ROWS:
        return list(DOUAY_ROWS[ref][0])
    b, c, v = ref.split(".")
    return [ref] if 1 <= int(v) <= vchapters.get(f"{b}.{c}", 0) else []


def convert_douay(path, books, sha, slug="douay"):
    """`books`: the Clementine's file names in canonical order (for the OSIS
    ids); `sha`: the pinned sha256."""
    import sys as _sys
    if HERE not in _sys.path:
        _sys.path.insert(0, HERE)
    import versification as _V
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    names = [b["name"] for b in data["books"][:len(DOUAY_NAMES)]]
    if names != DOUAY_NAMES:
        raise ValueError(f"Douay book order differs from the pinned file's: {names[:5]}...")
    vmap, kjv_ids = None, set()
    if os.path.exists(_V.VULGATE_PATH):
        vmap = _V.load(_V.VULGATE_PATH)
        with open(os.path.join(HERE, "..", "data", "uids", "wordhoard.uids.json"), encoding="utf-8") as f:
            kjv_ids = {k for k in json.load(f)["uids"] if k.startswith("kjv:")}
    vch = vmap["vulgate_chapters"] if vmap else {}
    units, empty = [], 0
    resolved = {True: 0, False: 0}
    dmap, dc = _dc_map(), {True: 0, False: 0}
    for b, book in zip(books, data["books"]):
        osis = VULGATE_BOOKS[b][0]
        for ch in book["chapters"]:
            for vs in ch["verses"]:
                text = re.sub(r"\s+", " ", vs["text"]).strip()
                if not text:
                    empty += 1
                    continue
                ref = f"{osis}.{ch['chapter']}.{vs['verse']}"
                if ref in DOUAY_ROWS and DOUAY_ROWS[ref][1] not in text:
                    raise ValueError(f"DOUAY_ROWS {ref}: {DOUAY_ROWS[ref][1]!r} is not in the verse")
                u = {"id": f"{slug}:{ref}", "ref": f"{book['name']} {ch['chapter']}:{vs['verse']}",
                     "text": text, "links": []}
                if vmap:
                    vl = douay_vulgate(ref, vch)
                    u["vulgate"] = [f"vulgate:{x}" for x in vl]
                    rs = [_V.resolve_vulgate(x, vmap, kjv_ids) for x in vl]
                    named = DOUAY_ROWS[ref][2] if len(DOUAY_ROWS.get(ref, ())) > 2 else None
                    if named:
                        ks = [f"kjv:{k}" for k in named]
                        if any(k not in kjv_ids for k in ks):
                            raise ValueError(f"DOUAY_ROWS {ref}: {ks} is not a KJV unit")
                        u["kjv"] = {"resolved": True, "target": ks[0]}
                        if len(ks) > 1:
                            u["kjv"]["spans"] = ks
                    elif rs and all(r["resolved"] for r in rs):
                        ts = []
                        for r in rs:
                            for t in r.get("spans", [r["target"]]):
                                if t not in ts:
                                    ts.append(t)
                        u["kjv"] = {"resolved": True, "target": next(t for t in ts if t.startswith("kjv:"))}
                        if len(ts) > 1:
                            u["kjv"]["spans"] = ts
                    else:
                        why = next((r for r in rs if not r["resolved"]), None)
                        u["kjv"] = dict(why) if why else {"resolved": False,
                                                          "why": "no Clementine verse holds this text"}
                    resolved[u["kjv"]["resolved"]] += 1
                _dc_key(u, ref, slug, dmap, dc)
                units.append(u)
    return {"slug": slug, "title": "The Holy Bible, Douay-Rheims Version (Challoner revision)",
            "author": "Richard Challoner (reviser); Gregory Martin et al. (translators)",
            "source": {"path": os.path.relpath(path, CORPUS), "format": "scrollmapper-json",
                       "sha256": sha},
            "scheme": {"citation": "Book chapter:verse in the Vulgate's numbering (OSIS book ids)",
                       "resolution": "verse", "honesty": "exact",
                       "versification": "vulgate",
                       "empty_verses_dropped": empty,
                       "kjv_resolved": resolved[True], "kjv_unresolved": resolved[False],
                       **_dc_scheme(dc),
                       "note": "The Clementine Vulgate's English companion, numbered as the "
                               "Vulgate is. `vulgate` names the Clementine verse(s) holding the "
                               "same text (the same number except at structure_texts.DOUAY_ROWS); "
                               "`kjv` follows through data/versification/vulgate-kjv.json. "
                               "Empty verses in the file (versification padding) are dropped, "
                               "never given ids. The file's five appendix books (3-4 Esdras, "
                               "Prayer of Manasses, an additional psalm, Laodiceans) are not "
                               "read: the Clementine source has no text for them."},
            "rights": {"license": "public-domain",
                       "attribution": "Douay-Rheims Bible, Challoner revision, via "
                                      "scrollmapper/bible_databases",
                       "source_url": "https://github.com/scrollmapper/bible_databases",
                       "rights_line": "DRC: Douay-Rheims Bible, Challoner Revision. "
                                      "License: Public Domain",
                       "kjv_field": _kjv_field_rights("data/versification/vulgate-kjv.json")},
            "units": units}

# ---------------------------------------------------------------- Brenton
#
# Brenton's English Septuagint (1851), from eBible.org's own USFM archive
# (fetch_sources.BRENTON, pinned: the archive kept unaltered in a GitHub
# repository, because ebible.org is out of this sandbox's reach). One file per
# book. Read: the scripture books; not read: the front matter, Brenton's
# introductions, and his appendix of Alexandrinus readings (FRT, INT, BAK,
# OTH, XX*), and NEH, eBible's own copy of Nehemiah RENUMBERED to the KJV
# (Brenton prints Nehemiah as chapters 11-23 of "Ezra and Nehemiah", the
# Greek's 2 Esdras, and that is the file read).
#
# Markup, read from the files: \v and \c number; \add ... \add* are the
# words Brenton supplies (in italics in print), \sc small capitals, \it
# italics: kept as plain words, with `marked` holding the verse's USFM as is.
# \f ... \f* are Brenton's footnotes and \x ... \x* his cross references:
# out of `text`, into `notes`. \d (a psalm title) and \p, \nb are layout.
#
# WHAT IS NOT CLAIMED (rule 4): ids are in BRENTON's numbering, the Greek's,
# not the KJV's: the Psalms counted as in the Greek with the title as verse 1,
# Jeremiah's oracles in the Greek's order, the Greek's additions LETTERED
# after the verse they follow (1Kgs.12.24a, Esth.1.1b), verses the Greek lacks
# simply absent. `kjv` names the KJV verse(s) holding the same text by the map
# data/versification/brenton-kjv.json (build_brenton_versification.py), or says
# why there is none. No uids are minted.

BRENTON_BOOKS = {   # USFM id -> OSIS (the id's book code)
    "GEN": "Gen", "EXO": "Exod", "LEV": "Lev", "NUM": "Num", "DEU": "Deut", "JOS": "Josh",
    "JDG": "Judg", "RUT": "Ruth", "1SA": "1Sam", "2SA": "2Sam", "1KI": "1Kgs", "2KI": "2Kgs",
    "1CH": "1Chr", "2CH": "2Chr", "EZR": "Ezra", "JOB": "Job", "PSA": "Ps",
    "PRO": "Prov", "ECC": "Eccl", "SNG": "Song", "ISA": "Isa", "JER": "Jer", "LAM": "Lam",
    "EZK": "Ezek", "HOS": "Hos", "JOL": "Joel", "AMO": "Amos", "OBA": "Obad", "JON": "Jonah",
    "MIC": "Mic", "NAM": "Nah", "HAB": "Hab", "ZEP": "Zeph", "HAG": "Hag", "ZEC": "Zech",
    "MAL": "Mal", "TOB": "Tob", "JDT": "Jdt", "ESG": "Esth", "WIS": "Wis", "SIR": "Sir",
    "BAR": "Bar", "LJE": "EpJer", "SUS": "Sus", "BEL": "Bel", "1MA": "1Macc", "2MA": "2Macc",
    "1ES": "1Esd", "MAN": "PrMan", "3MA": "3Macc", "4MA": "4Macc", "DAG": "Dan",
}
BRENTON_SKIP = {"FRT", "INT", "BAK", "OTH", "XXA", "XXB", "XXC", "NEH"}
RE_USFM_NOTE = re.compile(r"\\(f|x) .*?\\\1\*", re.S)
RE_USFM_MARK = re.compile(r"\\[a-z]+[0-9]*\*?")
RE_USFM_PARA = re.compile(r"\\(?:p|d|nb|b|q[0-9]?|m)(?=\s|$)")   # layout: a space
RE_USFM_CHAR = re.compile(r"\\[a-z]+[0-9]*(?:\*| )")          # \add ... \add*: the words stay


def brenton_note(raw):
    """A footnote's or cross reference's text, its markers dropped."""
    body = re.sub(r"^\\[fx] \S+\s*", "", raw)[:-3]
    body = re.sub(r"\\(fr|xo) \S+\s*", "", body)
    return re.sub(r"\s+", " ", RE_USFM_MARK.sub(" ", body)).strip()


def brenton_verses(zpath):
    """[(osis, book name, chapter, verse label, marked USFM)] in file order,
    scripture books only. A label is "12"; "24a" for a lettered addition; "0"
    for text before a chapter's verse 1. Refuses a repeated label."""
    import zipfile
    out = []
    with zipfile.ZipFile(zpath) as z:
        for name in sorted(z.namelist(), key=lambda n: int(n.split("-")[0]) if n[0].isdigit() else 999):
            if not name.endswith(".usfm"):
                continue
            code = name.split("-", 1)[1][:3]
            if code in BRENTON_SKIP:
                continue
            if code not in BRENTON_BOOKS:
                raise ValueError(f"Brenton {name}: an unknown book")
            t = z.read(name).decode("utf-8")
            title = re.search(r"^\\h (.+?)\s*$", t, re.M).group(1)
            ch, seen, in_verse = None, set(), False
            for part in re.split(r"(\\c \d+|\\v \S+)", t):
                m = re.match(r"\\(c|v) (\S+)$", part)
                if m and m.group(1) == "c":
                    ch, in_verse = m.group(2), False
                    continue
                if m:
                    if (ch, m.group(2)) in seen:
                        raise ValueError(f"Brenton {code} {ch}:{m.group(2)} twice")
                    seen.add((ch, m.group(2)))
                    out.append([BRENTON_BOOKS[code], title, ch, m.group(2), ""])
                    in_verse = True
                    continue
                if in_verse:
                    out[-1][4] += part
                elif ch is not None and RE_USFM_MARK.sub("", RE_USFM_NOTE.sub("", part)).strip():
                    # Text Brenton prints before a chapter's verse 1 (the
                    # Greek's prologue to Lamentations): verse "0".
                    seen.add((ch, "0"))
                    out.append([BRENTON_BOOKS[code], title, ch, "0", part])
    return [tuple(x[:4]) + (x[4].strip(),) for x in out]


def brenton_text(marked):
    """(text, notes) for one verse's USFM."""
    notes = [brenton_note(m.group(0)) for m in RE_USFM_NOTE.finditer(marked)]
    t = RE_USFM_PARA.sub(" ", RE_USFM_NOTE.sub("", marked))
    t = re.sub(r"\s+", " ", RE_USFM_CHAR.sub("", t)).strip()
    if "\\" in t:
        raise ValueError(f"Brenton: a marker left in {t[:80]!r}")
    return t, notes


def convert_brenton(zpath, sha, slug="brenton"):
    import sys as _sys
    if HERE not in _sys.path:
        _sys.path.insert(0, HERE)
    import versification as _V
    bmap, kjv_ids = None, set()
    if os.path.exists(_V.BRENTON_PATH):
        bmap = _V.load(_V.BRENTON_PATH)
        with open(os.path.join(HERE, "..", "data", "uids", "wordhoard.uids.json"), encoding="utf-8") as f:
            kjv_ids = {k for k in json.load(f)["uids"] if k.startswith("kjv:")}
    resolved = {True: 0, False: 0}
    dmap, dc = _dc_map(), {True: 0, False: 0}
    units, empty = [], []
    for osis, title, c, v, marked in brenton_verses(zpath):
        text, notes = brenton_text(marked)
        if not text:
            empty.append(f"{osis}.{c}.{v}")     # Prov 30:1: only a note ("see chapter 24")
            continue
        u = {"id": f"{slug}:{osis}.{c}.{v}", "ref": f"{title} {c}:{v}", "text": text,
             "links": [], "marked": marked}
        if notes:
            u["notes"] = notes
        if bmap:
            u["kjv"] = _V.resolve_brenton(f"{osis}.{c}.{v}", bmap, kjv_ids)
            resolved[u["kjv"]["resolved"]] += 1
        _dc_key(u, f"{osis}.{c}.{v}", slug, dmap, dc)
        units.append(u)
    return {"slug": slug, "title": "The Septuagint in English (Brenton, 1851)",
            "author": "Sir Lancelot Charles Lee Brenton (translator)",
            "source": {"path": os.path.relpath(zpath, CORPUS), "format": "ebible-usfm-zip",
                       "sha256": sha},
            "scheme": {"citation": "Book chapter:verse in Brenton's (the Greek's) numbering; "
                                   "the Greek's additions lettered (OSIS book ids)",
                       "resolution": "verse", "honesty": "exact",
                       "versification": "lxx-brenton",
                       "kjv_resolved": resolved[True], "kjv_unresolved": resolved[False],
                       **_dc_scheme(dc),
                       "empty_verses_not_units": empty,
                       "note": "Ids follow Brenton's numbering, NOT the KJV's: the Psalms "
                               "as in the Greek with a title as verse 1, Jeremiah's oracles "
                               "in the Greek's order, Nehemiah as chapters 11-23 of Ezra "
                               "(the Greek's 2 Esdras), the Greek's additions lettered after "
                               "the verse they follow. Each unit's `kjv` names the KJV "
                               "verse(s) holding the same text by "
                               "data/versification/brenton-kjv.json, or says why there is "
                               "none; no uids minted. `text` drops Brenton's notes, which "
                               "are in `notes`; `marked` is the verse's USFM as is. eBible's "
                               "corrections to the printing are in the text; its "
                               "KJV-renumbered Nehemiah and Brenton's appendix are not read."},
            "rights": {"license": "public-domain",
                       "attribution": "Brenton's English Septuagint, transcribed and corrected "
                                      "by eBible.org (eng-Brenton)",
                       "source_url": "https://ebible.org/eng-Brenton/",
                       "requests": "eBible asks that errors in the text be reported to it",
                       "kjv_field": _kjv_field_rights("data/versification/brenton-kjv.json")},
            "units": units}

# ---------------------------------------------------------------- historic English Bibles
#
# Geneva 1599, Tyndale, Young's, Darby, the ASV 1901 (fetch_sources.ENGLISH:
# scrollmapper's JSON of CrossWire's modules, pinned). A module sits on the
# KJV's verse grid, so the ids are its slots: the Bible's own numbers, except
# where a chapter numbers otherwise and its overflow is merged into the last
# slot. Each unit's `kjv` comes from data/versification/<slug>-kjv.json
# (build_english_versification.py), read off the English against the KJV's.
# Empty slots are not units. The text is the source's, never edited.

# Per-book rules (golden rule 2: fixes live here, so they rerun on refetch).
# Darby: CrossWire's module marks every "God", and scrollmapper's stripping of
# the mark ate the space before it. The glued forms, counted in the source:
# after a letter ("In the beginningGod", "OGod", "Am IGod"), after
# punctuation (",God" 97 times, "]God", ":God", ".God", "?God", ";God") and
# after a plural possessive ("fathers'God", Acts 24:14), with "Godhead"
# twice. No English word ends in a letter or this punctuation and runs on
# into "God". Left alone: an opening quote ("'God", Matt 1:23) and Ps 59:10's
# dash ("me, —God"), where the source has its space before the dash.
ENGLISH_RULES = {
    "darby": [(re.compile(r"(?<=[A-Za-z0-9,.;:?!\]])(?=God(?:head)?\b)|(?<=s')(?=God\b)"), " ",
               "a space restored before 'God', lost when the source's markup was stripped")],
    "tyndale": [(re.compile(r"\b(sayde|them|him|saynge)(?=(?:Wylt|And|Beholde|Whe)\b)"), r"\1 ",
                 "a space restored between two words the source runs together (Gen 18:23, "
                 "19:9, 27:39, 32:17); 'BenIamin' and 'xM' (Rev 9:16) are left as printed")],
    "geneva": [(re.compile(r"\btoAsaph\b"), "to Asaph",
                "a space restored in Ps 75:1's title ('committed toAsaph')")],
}


def convert_english(path, slug, sha):
    import sys as _sys
    if HERE not in _sys.path:
        _sys.path.insert(0, HERE)
    import versification as _V
    import fetch_sources as _fs
    e = _fs.ENGLISH[slug]
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    with open(os.path.join(HERE, "..", "data", "uids", "wordhoard.uids.json"), encoding="utf-8") as f:
        kjv_ids = {k for k in json.load(f)["uids"] if k.startswith("kjv:")}
    with open(os.path.join(HERE, "..", "data", "greppable", "kjv.tsv"), encoding="utf-8") as f:
        books = list(dict.fromkeys(l.split("\t", 1)[0][4:].split(".")[0]
                                   for l in f if l.startswith("kjv:")))
    if len(data["books"]) != len(books):
        raise ValueError(f"{slug}: {len(data['books'])} books, expected {len(books)}")
    emap = None
    if os.path.exists(_V.english_path(slug)):
        emap = _V.load(_V.english_path(slug))
    units, empty, fixed = [], 0, 0
    resolved = {True: 0, False: 0}
    for osis, book in zip(books, data["books"]):
        for ch in book["chapters"]:
            for vs in ch["verses"]:
                text = re.sub(r"\s+", " ", vs["text"]).strip()
                if not text:
                    empty += 1
                    continue
                for rx, rep, _why in ENGLISH_RULES.get(slug, []):
                    text, n = rx.subn(rep, text)
                    fixed += n
                ref = f"{osis}.{ch['chapter']}.{vs['verse']}"
                u = {"id": f"{slug}:{ref}", "ref": f"{book['name']} {ch['chapter']}:{vs['verse']}",
                     "text": text, "links": []}
                if emap:
                    u["kjv"] = _V.resolve_english(ref, emap, kjv_ids)
                    resolved[u["kjv"]["resolved"]] += 1
                units.append(u)
    merged = sum(isinstance(x, list) for x in emap["map"].values()) if emap else 0
    return {"slug": slug, "title": e["title"], "author": e["author"],
            "source": {"path": os.path.relpath(path, CORPUS), "format": "scrollmapper-json",
                       "sha256": sha},
            "scheme": {"citation": "Book chapter:verse as the source's CrossWire module "
                                   "numbers it (the KJV's grid; OSIS book ids)",
                       "resolution": "verse",
                       "honesty": "exact" if not merged else
                                  f"exact, except {merged} verses holding several KJV verses "
                                  f"(a merged last slot or the Bible's own division)",
                       "versification": f"{slug} (CrossWire, KJV grid)",
                       "kjv_resolved": resolved[True], "kjv_unresolved": resolved[False],
                       "empty_slots_not_units": empty,
                       **({"coverage": e["coverage"]} if "coverage" in e else {}),
                       **({"rules": [{"why": w, "applied": fixed}
                                     for _r, _p, w in ENGLISH_RULES[slug]]}
                          if slug in ENGLISH_RULES else {}),
                       "note": "Ids are the module's slots: the Bible's own numbers wherever it "
                               "numbers as the KJV does; where a chapter numbers otherwise "
                               + ("(the Geneva follows the Hebrew in Num 13, Dan 4 and others) "
                                  if slug == "geneva" else
                                  "(the map's `aligned_chapters` lists any; often none) ")
                               + "its verses fill the KJV's slots in order and the overflow sits "
                               "in the last slot. Each unit's `kjv` names the KJV verse(s) "
                               "holding the same words, by "
                               f"data/versification/{slug}-kjv.json; no uids minted."},
            "rights": {"license": "public-domain",
                       "attribution": f"{e['title']}, via scrollmapper/bible_databases "
                                      "(from CrossWire's SWORD module)",
                       "source_url": "https://github.com/scrollmapper/bible_databases",
                       "rights_line": e["readme"]},
            "units": units}

# ---------------------------------------------------------------- the KJV's Apocrypha
#
# The fourteen books the KJV prints as Apocrypha, from eBible.org's KJV
# Cambridge Paragraph Bible (fetch_sources.KJVA, PD, pinned). Read for one
# purpose: their verse numbers are the SHARED KEY the deuterocanon map aligns
# the Vulgate, the Douay and Brenton under (build_deuterocanon.py), and their
# English is what those maps are audited against. Ids are `kjva:Tob.1.1`, in
# the KJV's own numbering.
#
# Two things in the file are not plain verses, and each has a rule:
#   * Sirach opens with two prologues (an uncertain author's, then the
#     translator's), printed before 1:1 with no verse number: units
#     kjva:Sir.0.1 and kjva:Sir.0.2.
#   * The Rest of Esther is printed in the Greek's order (each addition where
#     the Greek places it), with the KJV's chapter number as \cp and verse
#     numbers that do not run as the KJV's (its 12:1-6 are 12a, 13-17). The
#     KJV numbers it 10:4-16:24, in Jerome's order. KJVA_ESTHER gives, segment
#     by segment in the file's order, the KJV verse the segment starts at;
#     verses are counted on from there, and each segment must end where the
#     KJV's chapter or passage does. Units are in the KJV's order.
KJVA_BOOKS = {   # USFM id -> the shared key's book id (OSIS)
    "TOB": "Tob", "JDT": "Jdt", "ESG": "AddEsth", "WIS": "Wis", "SIR": "Sir", "BAR": "Bar",
    "S3Y": "PrAzar", "SUS": "Sus", "BEL": "Bel", "1MA": "1Macc", "2MA": "2Macc",
    "1ES": "1Esd", "MAN": "PrMan", "2ES": "2Esd",
}
KJVA_ESTHER = [   # (KJV chapter, first verse, last verse), in the file's order
    (11, 2, 12), (12, 1, 6), (13, 1, 7), (13, 8, 18), (14, 1, 19), (15, 1, 16),
    (16, 1, 24), (10, 4, 13), (11, 1, 1),
]


def kjva_verses(zpath):
    """[(osis, book name, chapter, verse, marked USFM)] for the Apocrypha, in
    the KJV's numbering and order."""
    import zipfile
    out = []
    with zipfile.ZipFile(zpath) as z:
        for name in sorted(z.namelist()):
            code = name.split("-", 1)[1][:3] if "-" in name else ""
            if not name.endswith(".usfm") or code not in KJVA_BOOKS:
                continue
            osis = KJVA_BOOKS[code]
            t = z.read(name).decode("utf-8")
            title = re.search(r"^\\h (.+?)\s*$", t, re.M).group(1)
            rows, ch, seg, fresh = [], None, -1, True
            if code == "SIR":   # the two prologues, before 1:1
                head = t.split("\\c 1", 1)[0]
                pro = re.findall(r"\\im (.*?)(?=\\is1|\\im|\Z)", head, re.S)
                if len(pro) != 2:
                    raise ValueError(f"KJVA Sirach: {len(pro)} prologues, expected 2")
                rows += [[osis, title, 0, i, p] for i, p in enumerate(pro, 1)]
            for part in re.split(r"(\\c \d+|\\cp \d+|\\v \S+)", t):
                m = re.match(r"\\(c|cp|v) (\S+)$", part)
                if m and m.group(1) in ("c", "cp"):
                    if m.group(1) == "cp" and code != "ESG":
                        raise ValueError(f"KJVA {code}: an unexpected \\cp")
                    if m.group(1) == "c":
                        ch = int(m.group(2))
                    fresh = True    # Esther: the next verse opens a new segment
                    continue
                if m and code == "ESG":
                    if fresh:
                        seg, fresh = seg + 1, False
                        kc, lo, hi = KJVA_ESTHER[seg]
                        v = lo
                    else:
                        v += 1
                        if v > hi:
                            raise ValueError(f"KJVA Esther: segment {seg + 1} runs past {kc}:{hi}")
                    rows.append([osis, title, kc, v, ""])
                    continue
                if m:
                    if not m.group(2).isdigit():
                        raise ValueError(f"KJVA {code} {ch}:{m.group(2)}: not a number")
                    rows.append([osis, title, ch, int(m.group(2)), ""])
                    continue
                if rows and (code != "SIR" or rows[-1][2] != 0):
                    rows[-1][4] += part
            if code == "ESG":
                for r in rows:   # where the file prints the KJV's own number, it must agree
                    vp = re.match(r"\s*\\vp (\d+)\\vp\*", r[4])
                    if vp and int(vp.group(1)) != r[3]:
                        raise ValueError(f"KJVA Esther {r[2]}:{r[3]} prints itself as {vp.group(1)}")
                want = [(c, v) for c, lo, hi in KJVA_ESTHER for v in range(lo, hi + 1)]
                if [(r[2], r[3]) for r in rows] != want:
                    raise ValueError(f"KJVA Esther: {len(rows)} verses do not fill 10:4-16:24 "
                                     f"segment by segment")
                rows.sort(key=lambda r: (r[2], r[3]))
            seen = set()
            for r in rows:
                if (r[2], r[3]) in seen:
                    raise ValueError(f"KJVA {code} {r[2]}:{r[3]} twice")
                seen.add((r[2], r[3]))
            out += [tuple(r[:4]) + (r[4].strip(),) for r in rows]
    return out


RE_KJVA_DROP = re.compile(r"\\vp \S+\\vp\*|\\(?:iex|ms1|imi) [^\n]*")


def convert_kjva(zpath, sha, slug="kjva"):
    units = []
    for osis, title, ch, v, marked in kjva_verses(zpath):
        # \vp is the printed number (checked above), \iex and \ms1 the
        # editor's placement notes and headings, \mi a paragraph: not text.
        text, notes = brenton_text(re.sub(r"\\mi(?=\s|$)", " ", RE_KJVA_DROP.sub(" ", marked)))
        if not text:
            raise ValueError(f"KJVA {osis} {ch}:{v} is empty")
        ref = f"{title} {ch}:{v}" if ch else f"{title}, prologue {v}"
        units.append({"id": f"{slug}:{osis}.{ch}.{v}", "ref": ref, "text": text,
                      "links": [], "marked": marked, **({"notes": notes} if notes else {})})
    books = list(dict.fromkeys(u["id"].split(":")[1].split(".")[0] for u in units))
    return {"slug": slug, "title": "The Apocrypha of the King James Version (Cambridge "
                                   "Paragraph Bible)",
            "author": "the King James translators (1611); F. H. A. Scrivener (ed., 1873)",
            "source": {"path": os.path.relpath(zpath, CORPUS), "format": "usfm-zip",
                       "sha256": sha},
            "scheme": {"citation": "Book chapter:verse in the KJV's own numbering (OSIS book "
                                   "ids); Sirach's two prologues are chapter 0",
                       "resolution": "verse", "honesty": "exact",
                       "versification": "kjv-apocrypha",
                       "books": books,
                       "note": "The KJV's Apocrypha only (the Old and New Testaments of this "
                               "file are not read: the shelf's KJV is the Gutenberg text). "
                               "These verse numbers are the shared key of "
                               "data/versification/deuterocanon.json. The Rest of Esther is "
                               "renumbered 10:4-16:24 from the file's Greek-order segments "
                               "(structure_texts.KJVA_ESTHER); every other number is the "
                               "file's."},
            "rights": {"license": "public-domain",
                       "attribution": "KJV Cambridge Paragraph Bible, eBible.org (engkjvcpb)",
                       "source_url": "https://ebible.org/engkjvcpb/",
                       "rights_line": "Public Domain",
                       "note": "eBible: letters patent restrict printing the KJV in the "
                               "United Kingdom; elsewhere it is in the public domain"},
            "units": units}

# ---------------------------------------------------------------- Lexicons
#
# A lexicon is not a linear text; it is a reference work keyed by lemma. It
# still fits this pipeline's one output shape with no schema change, because
# the unit id was always the citation hub -- and for a lexicon the canonical
# citation IS the entry number:
#
#     strongs-hebrew:H2617  <->  the printed entry H2617  <->  any edition's page
#
# The cross-references a lexicon is full of (a Greek entry citing a Hebrew
# one, a BDB entry carrying its Strong's number) go in links[] -- the same
# field the ThML scripRef harvest already fills for Calvin. Ingested this way
# the lexicons are one connected graph, not three isolated word lists.
#
# Structured lexical fields hang off each unit under "lex", so the unit
# contract {id, ref, text, links[]} stays exactly what every converter emits.
#
# WHAT IS NOT CLAIMED HERE (rule 4, honesty fields are load-bearing):
# BDB cites scripture in HEBREW versification, which parts company with the
# KJV's -- most visibly in the Psalms, where a Hebrew superscription is
# counted as verse 1 and every later verse in that psalm is off by one. So a
# scripture citation is recorded as what the source actually said (its own
# reference string, plus the OSIS book/chapter/verse it states). A labelled
# hole beats a confident wrong label.
#
# Since 2026-10-02 that hole is filled where it can be: the Hebrew -> KJV map
# (data/versification/bhs-kjv.json, pipeline/build_versification.py) turns
# the stated reference into a kjv: unit id, added as `target` with
# `resolved: true`; the stated `osis` is kept as it was. A citation of a psalm
# title (the KJV's unnumbered superscription) or of a verse the KJV lacks
# stays `resolved: false` and says why. `build_versification.py --measure`
# is the evidence BDB numbers in Hebrew: where the two schemes differ, the
# entry's own word is in the cited Hebrew verse 72% of the time and in the
# same-numbered KJV verse 5.5%.

HEB_NS = "{http://openscriptures.github.com/morphhb/namespace}"

# BDB's <ref b="..."> is the Protestant canonical book number (1 = Genesis).
BOOKNUM2OSIS = {i + 1: osis for i, (_t, osis, _n) in enumerate(KJV_BOOKS)}


def strongs_id(raw, lang):
    """'0175' | '175' | 'H175' -> 'H175'. The leading zeros are a formatting
    artifact of the source files, never part of the number."""
    s = str(raw or "").strip().upper()
    prefix = "H" if lang == "hebrew" else "G"
    if s[:1] in ("H", "G"):
        prefix, s = s[0], s[1:]
    s = s.lstrip("0") or "0"
    return prefix + s


def el_text(el):
    """Flatten an element and its children to plain text, document order."""
    if el is None:
        return ""
    return clean(ET.tostring(el, encoding="unicode", method="text"))


def convert_strongs_hebrew(path, slug="strongs-hebrew"):
    """Strong's Hebrew Dictionary (1890). H1-H8674."""
    root = ET.parse(path).getroot()
    units = []
    for e in root.findall(HEB_NS + "entry"):
        sid = strongs_id(e.get("id"), "hebrew")
        w = e.find(HEB_NS + "w")
        lemma = (w.text or "").strip() if w is not None else ""
        lex = {"lemma": lemma,
               "translit": (w.get("xlit") or "") if w is not None else "",
               "pron": (w.get("pron") or "") if w is not None else "",
               "pos": (w.get("pos") or "") if w is not None else "",
               "lang": (w.get("{http://www.w3.org/XML/1998/namespace}lang") or "")
                       if w is not None else "",
               "derivation": el_text(e.find(HEB_NS + "source")),
               "kjv_usage": el_text(e.find(HEB_NS + "usage"))}
        meaning = el_text(e.find(HEB_NS + "meaning"))
        lex["meaning"] = meaning
        # a <w src="H1"> inside the entry is a cross-reference, not the headword
        links = [{"kind": "strongs", "target": f"{slug}:{strongs_id(r.get('src'), 'hebrew')}"}
                 for r in e.iter(HEB_NS + "w") if r.get("src")]
        text = " ".join(p for p in (lex["derivation"], meaning, lex["kjv_usage"]) if p)
        units.append({"id": f"{slug}:{sid}",
                      "ref": f"{sid} {lemma}".strip() + (f" ({lex['translit']})" if lex["translit"] else ""),
                      "text": text, "links": links, "lex": lex})
    return {"slug": slug,
            "title": "Strong's Hebrew Dictionary",
            "author": "James Strong (1890)",
            "source": {"path": os.path.relpath(path, CORPUS), "format": "lexicon-xml",
                       "sha256": sha256(path)},
            "scheme": {"citation": "Strong's number (H1-H8674)",
                       "resolution": "entry", "honesty": "exact",
                       "note": "Dictionary text is public domain; this transcription is "
                               "the OpenScriptures HebrewLexicon (CC BY 4.0 on the markup). "
                               "Cross-references resolved; no scripture links in this source."},
            "units": units}


def greek_derivation(el):
    """<strongs_derivation> carries its cross-references as EMPTY elements whose
    number lives in an attribute, so plain text-flattening yields 'from ;'.
    Put the number back where the reader expects to see it."""
    if el is None:
        return ""
    out = []
    def walk(node):
        if node.tag == "strongsref":
            lang = "H" if (node.get("language") or "").lower().startswith("hebrew") else "G"
            out.append(strongs_id(node.get("strongs"), "hebrew" if lang == "H" else "greek"))
        if node.text:
            out.append(node.text)
        for kid in node:
            walk(kid)
            if kid.tail:
                out.append(kid.tail)
    if el.text:
        out.append(el.text)
    for kid in el:
        walk(kid)
        if kid.tail:
            out.append(kid.tail)
    return clean(" ".join(out))


GREEK_MAX = 5624        # G1-G5624 is the whole dictionary. A <see>/<strongsref>
                        # above it is a Robinson grammar/parsing code riding in
                        # the same attribute, not a lexicon entry -- emitting
                        # those as cross-references manufactures dangling links.


def convert_strongs_greek(path, slug="strongs-greek"):
    """Strong's Greek Dictionary (1890). G1-G5624."""
    root = ET.parse(path).getroot()
    entries = root.find("entries")
    units = []
    grammar_refs = 0
    for e in entries.findall("entry"):
        sid = strongs_id(e.get("strongs"), "greek")
        g = e.find("greek")
        lemma = (g.get("unicode") or "") if g is not None else ""
        pr = e.find("pronunciation")
        kjv = el_text(e.find("kjv_def")).lstrip(": -—").strip()
        lex = {"lemma": lemma,
               "translit": (g.get("translit") or "") if g is not None else "",
               "beta": (g.get("BETA") or "") if g is not None else "",
               "pron": (pr.get("strongs") or "") if pr is not None else "",
               "derivation": greek_derivation(e.find("strongs_derivation")),
               "meaning": el_text(e.find("strongs_def")),
               "kjv_usage": kjv}
        links, seen = [], set()
        for r in list(e.iter("see")) + list(e.iter("strongsref")):
            lang = "hebrew" if (r.get("language") or "").lower().startswith("hebrew") else "greek"
            tid = strongs_id(r.get("strongs"), lang)
            if lang == "greek" and int(tid[1:] or 0) > GREEK_MAX:
                grammar_refs += 1        # parsing code, not a dictionary entry
                continue
            target = f"{'strongs-hebrew' if lang == 'hebrew' else slug}:{tid}"
            if target in seen:
                continue
            seen.add(target)
            links.append({"kind": "strongs", "target": target})
        text = " ".join(p for p in (lex["derivation"], lex["meaning"], kjv) if p)
        if not text:
            # Strong's own placeholder numbers say "Not Used" as loose text on
            # the entry, with no child elements. Keep what the book says.
            text = clean("".join(e.itertext()).replace(str(int(e.get("strongs"))), "", 1))
            lex["not_used"] = text.lower().startswith("not used")
        units.append({"id": f"{slug}:{sid}",
                      "ref": f"{sid} {lemma}".strip() + (f" ({lex['translit']})" if lex["translit"] else ""),
                      "text": text, "links": links, "lex": lex})
    return {"slug": slug,
            "title": "Strong's Greek Dictionary",
            "author": "James Strong (1890)",
            "source": {"path": os.path.relpath(path, CORPUS), "format": "lexicon-xml",
                       "sha256": sha256(path)},
            "scheme": {"citation": "Strong's number (G1-G5624)",
                       "resolution": "entry", "honesty": "exact",
                       "note": "Dictionary text is public domain; transcription from the "
                               "OpenScriptures strongs repo (Sandborg-Petersen lineage). "
                               "Cross-references to Hebrew entries resolved across books; "
                               f"{grammar_refs} refs above G{GREEK_MAX} dropped as Robinson "
                               "parsing codes, not entries. Strong's own 'Not Used' "
                               "placeholder numbers are kept, flagged lex.not_used."},
            "units": units}


HEBREW_MAX = 8674       # H1-H8674 is the whole dictionary; see GREEK_MAX.
RE_BDB_FURNITURE = re.compile(r'<h1>.*?</h1>|<div class="navigation">.*?</div>', re.S)
RE_BDB_REF = re.compile(r'<ref\b[^>]*?\bb="(\d+)"[^>]*?\bcBegin="(\d+)"[^>]*?\bvBegin="(\d+)"[^>]*?>'
                        r'(.*?)</ref>', re.S)


def convert_bdb(path, slug="bdb-hebrew"):
    """Brown-Driver-Briggs (1906), unabridged. Tab-separated:
    BDBid \\t StrongNumber \\t content(HTML)."""
    import csv as _csv
    _csv.field_size_limit(1 << 27)          # single entries run past 200k chars
    import sys as _sys
    if HERE not in _sys.path:       # loaded by path (the tests do), not as a script
        _sys.path.insert(0, HERE)
    import versification as _V
    units, furniture, extended = [], 0, 0
    resolved = {True: 0, False: 0}
    vmap, kjv_ids = None, set()
    if os.path.exists(_V.PATH):
        vmap = _V.load()
        with open(os.path.join(HERE, "..", "data", "uids", "wordhoard.uids.json"), encoding="utf-8") as f:
            kjv_ids = {k for k in json.load(f)["uids"] if k.startswith("kjv:")}
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        rows = _csv.reader(f, delimiter="\t")
        header = next(rows, None)
        for row in rows:
            if len(row) < 3:
                continue
            bdbid, strong, content = row[0].strip(), row[1].strip(), row[2]
            if not bdbid:
                continue
            # Page furniture, stripped by pattern and counted -- never silently.
            # The <h1> repeats the entry id and the nav strip is prev|next
            # links; neither is lexicon content, and both would otherwise open
            # every single entry's text with "BDB2965 [ H2617 ] BDB2964 |
            # BIBLICAL HEBREW | BDB2966".
            body, n = RE_BDB_FURNITURE.subn("", content)
            furniture += n
            links = []
            # A BDB entry can map to SEVERAL Strong's numbers ("H6_H8" = this
            # root covers H6 through H8). One link each; H0/blank is "no
            # Strong's equivalent" and gets none.
            for part in re.split(r"[_,;/\s]+", strong):
                if not part.strip():
                    continue
                tid = strongs_id(part, "hebrew")
                if tid in ("H0", "H"):
                    continue
                if int(tid[1:] or 0) > HEBREW_MAX:
                    extended += 1   # H9000+ = extended Strong's for prefixes and
                    continue        # particles, not entries in the 1890 dictionary
                links.append({"kind": "strongs", "target": f"strongs-hebrew:{tid}"})
            # scripture citations: recorded as stated, deliberately unresolved
            seen_refs = set()
            for b, c, v, label in RE_BDB_REF.findall(body):
                osis = BOOKNUM2OSIS.get(int(b))
                if not osis:
                    continue
                key = f"{osis}.{c}.{v}"
                if key in seen_refs:
                    continue
                seen_refs.add(key)
                link = {"kind": "scripture", "osis": key,
                        "ref": clean(label) or key, "versification": "bhs",
                        "resolved": False}
                if vmap:
                    link.update(_V.resolve(key, vmap, kjv_ids))
                resolved[link["resolved"]] += 1
                links.append(link)
            lemma = ""
            m = re.search(r"<bdbheb>(.*?)</bdbheb>", body, re.S)
            if m:
                lemma = clean(m.group(1))
            units.append({"id": f"{slug}:{bdbid}",
                          "ref": f"{bdbid} {lemma}".strip() +
                                 (f" [{strongs_id(strong, 'hebrew')}]" if strong else ""),
                          "text": clean(body),
                          "links": links,
                          "lex": {"lemma": lemma,
                                  "strongs": strongs_id(strong, "hebrew") if strong else ""}})
    return {"slug": slug,
            "title": "A Hebrew and English Lexicon of the Old Testament (Brown-Driver-Briggs)",
            "author": "Francis Brown, S. R. Driver & C. A. Briggs (1906)",
            "source": {"path": os.path.relpath(path, CORPUS), "format": "lexicon-tsv",
                       "sha256": sha256(path)},
            "scheme": {"citation": "BDB entry id (BDB1-BDB9000s); Strong's number where mapped",
                       "resolution": "entry", "honesty": "exact text, partial keying",
                       "note": "Unabridged. 9,176 of 10,022 entries carry a Strong's number; "
                               "the rest are cross-reference and sub-root entries with no "
                               "Strong's equivalent. Scripture citations are recorded in the "
                               "source's own (Hebrew/BHS) versification (`osis`, as stated) and "
                               "resolved to a kjv: unit id (`target`) through the Hebrew->KJV "
                               "map data/versification/bhs-kjv.json (STEPBible TVTMS, CC BY "
                               f"4.0): {resolved[True]:,} resolved, {resolved[False]:,} left "
                               "unresolved with the reason (psalm titles, which the KJV does "
                               "not number; references that name no Hebrew verse; NT "
                               "references). "
                               f"{furniture} navigation/header furniture blocks stripped; "
                               f"{extended} refs above H{HEBREW_MAX} dropped as extended "
                               "Strong's prefix/particle codes."},
            "units": units}

GRK = "Ͱ-Ͽἀ-῿̀-ͯ"
RE_GREEK = re.compile(f"[{GRK}]")
RE_THAYER_HEAD = re.compile(rf"^([{GRK}][{GRK}’'\-]*)\s*[,.]\s+")


def convert_thayer(path, slug="thayer"):
    """Thayer's Greek-English Lexicon of the New Testament (1889), OCR'd.

    WHY THE UNIT IS A PAGE AND NOT AN ENTRY.

    Every other lexicon here arrives as data with its entries already
    delimited. Thayer's does not exist as data -- see the note in
    fetch_sources.py -- so its entries have to be inferred from OCR, and they
    cannot be inferred reliably. Measured on this scan (2026-09-06): requiring
    a paragraph break before a Greek headword finds 4,532 entries; dropping
    that requirement finds 7,983. Thayer's really has about 5,600. The strict
    rule loses entries wherever OCR dropped a blank line; the loose rule
    promotes mid-entry Greek words and mis-read small-caps in the front
    matter. Neither number is the entry list, and averaging two wrong answers
    does not produce a right one.

    So the unit is the printed page, which is exact, verifiable against the
    scan, and is already what this project's citation hub is built on --
    canonical citation <-> unit id <-> any edition's page. Detected headwords
    ride along on each page under lex.headwords, explicitly flagged heuristic,
    because they are genuinely useful for lookup and harmless when wrong.
    Someone refining entry detection later can do it against a stable
    page-anchored base without re-running a four-hour OCR.
    """
    pages = json.load(open(path, encoding="utf-8"))
    units = []
    heads_total = 0
    for pno in sorted(pages, key=int):
        raw = pages[pno]
        lines = raw.split("\n")
        # Page furniture: line 1 of a body page is the running head (the Greek
        # catchword) and bare page numbers sit on their own line. Stripped by
        # pattern and counted, never silently.
        furniture = []
        if lines and lines[0].strip() and len(lines[0].strip()) < 40:
            furniture.append(lines[0].strip())
            lines = lines[1:]
        body_lines = []
        for l in lines:
            if re.fullmatch(r"\s*\d{1,4}\s*", l):
                furniture.append(l.strip())
                continue
            body_lines.append(l)
        text = clean("\n".join(body_lines))
        if not text:
            continue
        headwords = []
        for i, l in enumerate(body_lines):
            if i and body_lines[i - 1].strip():
                continue                      # paragraph-initial only
            m = RE_THAYER_HEAD.match(l.strip())
            if m and len(m.group(1)) > 1:
                headwords.append(m.group(1))
        heads_total += len(headwords)
        units.append({"id": f"{slug}:p.{int(pno)}",
                      "ref": f"Thayer p. {int(pno)}",
                      "text": text, "links": [],
                      "lex": {"headwords": headwords,
                              "headwords_are": "heuristic (paragraph-initial Greek word); "
                                               "not an entry list -- see converter docstring",
                              "running_head": furniture[0] if furniture else "",
                              "greek_chars": len(RE_GREEK.findall(text))}})
    greek = sum(u["lex"]["greek_chars"] for u in units)
    return {"slug": slug,
            "title": "A Greek-English Lexicon of the New Testament (Thayer)",
            "author": "C. L. W. Grimm & C. G. Wilke, tr./rev./enl. Joseph Henry Thayer (1889)",
            "source": {"path": os.path.relpath(path, CORPUS), "format": "lexicon-ocr",
                       "sha256": sha256(path)},
            "scheme": {"citation": "printed page of the 1889 edition",
                       "resolution": "page",
                       "honesty": "page-exact; entries NOT segmented",
                       "note": f"OCR'd from the Internet Archive scan "
                               f"(greekenglishlexi00grimuoft, 760pp) with tesseract "
                               f"grc+eng at 300dpi on 2026-09-06, because no "
                               f"machine-readable Thayer's exists: that scan's own text "
                               f"layer contains ZERO Greek codepoints. This pass recovered "
                               f"{greek:,}. 744 pages carry text; the other 16 were checked "
                               f"individually and are the two cloth covers plus 14 blank "
                               f"leaves. {heads_total:,} headwords detected heuristically and "
                               f"flagged as such -- Thayer's has ~5,600 entries and OCR "
                               f"cannot delimit them reliably, so no entry claim is made. "
                               f"Text is OCR output: it has not been proofread against the "
                               f"page, and Greek diacritics are where OCR errs most."},
            "units": units}

RE_STEP_ROW = re.compile(r"^[GH]\d{4}\t")


RE_STEP_KEY = re.compile(r"^([GH]\d+[A-Za-z]*)")


def _step_one_target(key, slug):
    """One key -> one unit id. A Hebrew key points out of this book: STEPBible's
    Greek files cross-reference Hebrew for transliterated names (ἀββά -> H0002,
    σαβαώθ -> H6635)."""
    if key[:1] == "H":
        return f"strongs-hebrew:{strongs_id(re.sub(r'[A-Za-z]+$', '', key[1:]), 'hebrew')}"
    return f"{slug}:{key}"


def _step_targets(raw, slug):
    """A target cell is a key, optionally followed by a compound in parentheses:
    'G0473 (G0473+G3739)' means this word is built from those two. Reading the
    whole cell as one key manufactures dangling links (104 of them, measured
    2026-09-06) and loses the compound's parts, which are the interesting bit.
    Returns (primary, [parts])."""
    raw = (raw or "").strip()
    if not raw:
        return None, []
    m = RE_STEP_KEY.match(raw)
    if not m:
        return None, []
    primary = _step_one_target(m.group(1), slug)
    parts = []
    inner = re.search(r"\(([^)]*)\)", raw)
    if inner:
        for piece in re.split(r"[+,]", inner.group(1)):
            pm = RE_STEP_KEY.match(piece.strip())
            if pm:
                parts.append(_step_one_target(pm.group(1), slug))
    return primary, parts


def _step_body(html):
    """LSJ's hover citations live in title= attributes and carry REAL GREEK --
    973,610 characters of quoted ancient authors in the full LSJ, 44% of all
    the Greek in the file. Stripping tags first throws every one of them away,
    silently. Pull them inline before clean() runs."""
    html = re.sub(r'<a\b[^>]*\btitle="([^"]*)"[^>]*>(.*?)</a>', r" \2 [\1] ", html, flags=re.S)
    html = re.sub(r'<[^>]*\btitle="([^"]*)"[^>]*>', r" [\1] ", html)
    return clean(html)


def convert_stepbible_greek(paths, slug, title, author, scheme_note):
    """STEPBible's Greek lexicons (TBESG brief / TFLSJ full LSJ), 8-column TSV.

    KEYED ON THE EXTENDED STRONG'S NUMBER, WHICH IS NOT COLUMN 0.

    The obvious readings of this file are both wrong and both lose text, so
    they are worth naming (measured 2026-09-06):

      * Column 2 looks like the key. It is not -- it is the TARGET of a
        cross-reference. Keying on it merges Ἀπολλύων (G0623) into Ἀβαδδών
        (G0003), because Apollyon is "a Name of" Abaddon.
      * Column 0 looks like the key. It is not either -- G0001 carries TWO
        different words, the letter α and the interjection ἆ, told apart only
        by the extended suffix (G0001G vs G0001H). Keying on column 0 drops
        one definition of every such pair.

    The real key is the extended Strong's number that opens column 1. Grouping
    on it yields one unit per row with zero collisions across all three files,
    which is what "Extended Strongs" means and what the file header says.

    Column 1 also carries the relation ("= a Name of", "= the Greek of"), and
    column 2 its target, so those become links[] exactly as the Strong's
    cross-references do.
    """
    units, relations = [], 0
    for path in paths:
        for line in open(path, encoding="utf-8", errors="replace"):
            if not RE_STEP_ROW.match(line):
                continue
            c = line.rstrip("\n").split("\t")
            if len(c) < 8:
                continue
            m = re.match(r"^(\S+)\s*=\s*(.*)$", c[1].strip())
            if not m:
                continue
            key, relation = m.group(1), m.group(2).strip()
            target, parts = _step_targets(c[2], slug)
            links = []
            if relation and target and target != f"{slug}:{key}":
                links.append({"kind": "lexical", "relation": relation, "target": target})
                relations += 1
            for part in parts:
                if part != f"{slug}:{key}":
                    links.append({"kind": "lexical", "relation": "a Combination of",
                                  "target": part})
                    relations += 1
            lemma, translit, pos, gloss, body = c[3], c[4], c[5], c[6], c[7]
            text = " ".join(p for p in (gloss, _step_body(body)) if p)
            units.append({"id": f"{slug}:{key}",
                          "ref": f"{key} {lemma}".strip() + (f" ({translit})" if translit else ""),
                          "text": text, "links": links,
                          "lex": {"lemma": lemma, "translit": translit,
                                  "pos": pos, "gloss": gloss,
                                  "strongs": strongs_id(re.sub(r"[A-Za-z]+$", "", key[1:]), "greek")
                                             if key[:1] == "G" else ""}})
    return {"slug": slug, "title": title, "author": author,
            "source": {"path": ", ".join(os.path.relpath(p, CORPUS) for p in paths),
                       "format": "lexicon-tsv",
                       "sha256": sha256(paths[0])},
            # ---- rights are load-bearing here, not decoration ----
            # CC BY 4.0 permits redistribution outright. STEPBible additionally
            # ASKS that the data not be mirrored, so that corrections flow from
            # one source. Honored, and enforced by where the bytes live: the
            # source TSV and the built JSON are both gitignored, so nothing but
            # this pointer is ever committed or published. A consumer (Armarium)
            # may quote, cite and link; it must not serve the whole text.
            "rights": {"license": "CC BY 4.0",
                       "attribution": "Data created by www.STEPBible.org based on work "
                                      "at Tyndale House Cambridge (CC BY 4.0)",
                       "source_url": "https://github.com/STEPBible/STEPBible-Data",
                       "redistribute_whole": False,
                       "note": "Licence permits redistribution; the maintainers request "
                               "you point people at github.com/STEPBible rather than "
                               "mirror it. Quote and cite freely WITH attribution; do "
                               "not serve or ship the whole lexicon."},
            "scheme": {"citation": "Extended Strong's number (e.g. G0001G)",
                       "resolution": "entry", "honesty": "exact",
                       "note": scheme_note + f" {relations} cross-references "
                               "('a Name of', 'the Greek of', 'a Spelling of', ...) "
                               "resolved into links[], including into strongs-hebrew "
                               "for transliterated Hebrew names."},
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

# ---------------------------------------------- per-book body extraction
#
# Gutenberg files ship the apparatus INSIDE the work: a translator's
# introduction, a glossary, an appendix of corrections, a parallel
# transliteration. None of it is marked as anything other than more text, so a
# converter reads it as the author's own words and every measurement
# downstream inherits it. Rule 2 says never hand-edit a source text, so the
# boundaries live here and rerun on every refetch.
#
# Found 2026-09-11 by phrase extraction, which is a good apparatus detector
# precisely because apparatus repeats itself:
#   gilgamesh  -- ~70% of the file is Jastrow's monograph plus two blocks of
#                 transliterated Akkadian. Its top "fingerprint phrases" were
#                 `iz za ka r am a` and `i pu sa am ma iz`.
#   beowulf    -- CONTENTS at line 64 opens a roman-numeral division that then
#                 swallows the preface, bibliography and both glossaries; the
#                 poem's own `I.` is not until line 937. The glossary of proper
#                 names was sitting inside unit Beo XIV.217.

BODY_RULES = {
    "beowulf": {
        "start_at": r"^I\.\s*$", "start_min_line": 900,
        "stop_at":  r"^ADDENDA\.",
        "scrub": [r"\[\s*\d{1,3}\s*\]",   # inline footnote references
                  r"\{[^}]*\}"],            # the translator's marginal glosses
    },
    "gilgamesh": {
        # The English epic appears ONLY inside TRANSLATION sections.
        "keep_between": (r"^TRANSLATION\.\s*$",
                         r"^(?:TRANSLITERATION\.|CORRECTIONS\b|APPENDIX\b|NOTES\b)"),
        # Jastrow's philological notes are interleaved with the translation and
        # have no header, so they cannot be a section boundary -- treating them
        # as one cut the epic from 12,268 words to 2,461. They are PARAGRAPH
        # shaped: they open with "Line NN." and run to the next blank line.
        "scrub": [r"\[\s*\d{1,3}\s*\]",
                  r"(?m)^Lines?\s+\d+[^\n]*(?:\n(?!\s*$)[^\n]*)*"],
    },
}

def apply_body_rules(raw, slug):
    """Keep only the lines that are the work. Returns (text, note); the note
    goes into scheme.apparatus so the file states what was removed (rule 4)."""
    r = BODY_RULES.get(slug)
    if not r:
        return raw, None
    lines = raw.splitlines()
    n0 = len(lines)
    if "keep_between" in r:
        start_rx, stop_rx = (re.compile(x) for x in r["keep_between"])
        out, keeping = [], False
        for ln in lines:
            t = ln.strip()
            if start_rx.match(t):
                keeping = True
                continue
            if keeping and stop_rx.match(t):
                keeping = False
                continue
            if keeping:
                out.append(ln)
        lines = out
    else:
        start_rx = re.compile(r["start_at"])
        stop_rx = re.compile(r["stop_at"]) if r.get("stop_at") else None
        lo = 0
        for i, ln in enumerate(lines):
            if i + 1 >= r.get("start_min_line", 0) and start_rx.match(ln.strip()):
                lo = i
                break
        hi = len(lines)
        if stop_rx:
            for i in range(lo, len(lines)):
                if stop_rx.match(lines[i].strip()):
                    hi = i
                    break
        lines = lines[lo:hi]
    # scrubs run over the joined text, not line by line: a translator's
    # marginal gloss routinely opens on one line and closes on the next, and a
    # per-line regex silently leaves both halves behind.
    text = "\n".join(lines)
    for pat in r.get("scrub", []):
        text = re.compile(pat, re.S).sub(" ", text)
    lines = text.splitlines()
    note = (f"apparatus removed by BODY_RULES: kept {len(lines)} of {n0} source "
            f"lines; the remainder is front matter, glossary, appendix or "
            f"non-English parallel text, not the work")
    return "\n".join(lines), note


def convert_gutenberg_verse(path, slug, title, author, abbr, divre, cantica=None):
    """Verse works: divisions (book/canto), 12-line blocks. `cantica` maps a
    higher header (HELL->Inf) so Divine Comedy gets Inf/Purg/Par prefixes.
    Contents-list entries collapse: their between-heading segment is empty."""
    raw = strip_boilerplate(open(path, encoding="utf-8", errors="replace").read())
    raw, apparatus_note = apply_body_rules(raw, slug)
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
            "scheme": {"apparatus": apparatus_note, "citation": f"{abbr} division.line", "resolution": "line-block",
                       "honesty": "division exact; line = running line within division "
                                  "(translation lineation), 12-line blocks"},
            "units": units}

def convert_gutenberg_prose(path, slug, title, author, chapre):
    """Prose: paragraphs grouped under detected chapter headings."""
    raw = strip_boilerplate(open(path, encoding="utf-8", errors="replace").read())
    raw, apparatus_note = apply_body_rules(raw, slug)
    CH = re.compile(chapre) if chapre else None
    units, chap, pnum = [], None, 0
    for para in re.split(r"\n\s*\n", raw):
        p = re.sub(r"\s+", " ", para).strip()
        if not p:
            continue
        if CH and CH.match(p) and len(p) < 90:
            chap = re.sub(r"(\s*~)+$", "", p).rstrip(".")   # "Lamp-Posts ~ ~ ~" leaders
            pnum = 0
            continue
        pnum += 1
        ref = f"{chap}, par. {pnum}" if chap else f"par. {pnum}"
        cid = f"{slug}:{(chap or 'x').replace(' ', '_')}.{pnum}"
        units.append({"id": cid, "ref": ref, "text": p, "links": []})
    return {"slug": slug, "title": title, "author": author,
            "source": {"path": os.path.relpath(path, CORPUS), "format": "gutenberg-txt",
                       "sha256": sha256(path)},
            "scheme": {"apparatus": apparatus_note, "citation": "chapter + paragraph", "resolution": "paragraph",
                       "honesty": "chapter headings detected; paragraph running within chapter"},
            "units": units}

RE_CONTENTS_HEAD = re.compile(r"^\s*(TABLE OF )?CONTENTS\.?\s*$", re.I | re.M)
RE_CONTENTS_NUM = re.compile(r"^(?:CHAPTER|CHAP\.)?\s*(?:[IVXLC]+|\d+)?\s*[.:)]?\s*", re.I)
RE_CONTENTS_TAIL = re.compile(r"[\s.~_*·…]*(?:\d+|[ivxlc]+)?\s*$")
# The one-line fallback: a short paragraph with no lower-case letters and at
# least three capitals in a row (ESSAY TITLES, CHAPTER I, THE BLUE CROSS).
CAPS_HEADING = r"(?=[^a-z]*[A-Z]{3})[^a-z]{3,88}"

def _contents_key(line):
    t = RE_CONTENTS_NUM.sub("", line.strip(), count=1)
    t = RE_CONTENTS_TAIL.sub("", t).strip(" .:-—")
    return t

def contents_chapre(path):
    """Heading regex for a Gutenberg prose book, read from the book's OWN
    Contents: an essay collection prints its titles in title case in the body
    ("The Meaning of Mock Turkey") and in capitals in the Contents, so no
    single house regex finds them all. Every Contents entry becomes an
    alternative (case-insensitive, any numbering, any trailing page number or
    leader), unioned with CAPS_HEADING. No Contents -> CAPS_HEADING alone."""
    raw = strip_boilerplate(open(path, encoding="utf-8", errors="replace").read())
    m = RE_CONTENTS_HEAD.search(raw)
    keys = []
    if m:
        blank_run = 0
        for line in raw[m.end():].splitlines()[:400]:
            if not line.strip():
                blank_run += 1
                if blank_run >= 4 and keys:
                    break
                continue
            blank_run = 0
            if len(line.strip()) > 80 and keys and not re.search(r"\d\s*$", line):
                break     # ran off the end of the Contents into running prose
            k = _contents_key(line)
            if k.upper() in ("PAGE", "CHAPTER", "CONTENTS") or not re.search(r"[A-Za-z]{3}", k):
                continue
            if 3 <= len(k) <= 80:
                keys.append(k)
    alts = sorted({re.escape(k).replace(r"\ ", r"\s+") for k in keys}, key=len, reverse=True)
    body = f"(?:CHAPTER\\s+|CHAP\\.\\s+)?(?:[IVXLC]+|\\d+)?\\s*[.:)]?\\s*(?:{'|'.join(alts)})[\\s.~_*]*$"
    return f"(?i:{body})|(?-i:{CAPS_HEADING}$)" if alts else f"{CAPS_HEADING}$"

RE_SH_ACT = re.compile(r"^ACT\s+([IVXL]+)", re.I)
RE_SH_SCENE = re.compile(r"^SCENE\s+([IVXL0-9]+)", re.I)
# The class must admit the CURLY apostrophe (U+2019) and the semicolon. Until
# 2026-09-07 it held only the ASCII apostrophe, so five real plays were never
# detected at all and their text was filed under whichever play preceded them:
# ALL'S WELL, LOVE'S LABOUR'S LOST, A MIDSUMMER NIGHT'S DREAM, THE WINTER'S TALE
# (curly apostrophe) and TWELFTH NIGHT; OR, WHAT YOU WILL (semicolon).
RE_SH_PLAY = re.compile("^[A-Z][A-Z0-9 ,;.'’&-]{5,70}$")
SH_NOTPLAY = re.compile(r"^(ACT|SCENE|CONTENTS|DRAMATIS|PROLOGUE|EPILOGUE|CHORUS|"
                        r"THE END|FINIS|INDUCTION|PERSONS|THE PERSONS)\b", re.I)

# What an editor does NOT give a line number to: the speaker's name, and a
# stage direction. Counting those put "To be, or not to be" at line 86 when
# every printed edition calls it 3.1.56 — a citation that looks exact and is
# thirty lines wrong, which is worse than no line number at all.
RE_SH_SPEAKER = re.compile(r"^[A-Z][A-Z0-9 ,'’.-]{0,31}\.$")
RE_SH_STAGE = re.compile(r"^\[|^(Enter|Exit|Exeunt|Re-enter|Alarum|Flourish|"
                         r"Sennet|Retreat|Manet)\b")
def sh_numbered(t):
    """True if this line takes a line number."""
    return not (RE_SH_SPEAKER.match(t) or RE_SH_STAGE.match(t))

# A row of a play's own contents table, not a division of the play itself.
RE_SH_CONTENTS_ROW = re.compile(
    r"^(Contents|ACT\b|INDUCTION\b|PROLOGUE\b|EPILOGUE\b|Scene\b)", re.I)
RE_SH_DRAMATIS = re.compile(r"^(Dramatis\s+Person|DRAMATIS\s+PERSON)", re.I)

SH_ROMAN = [("XL",40),("X",10),("IX",9),("V",5),("IV",4),("I",1)]
def sh_roman(r):
    """Roman numeral -> int, for act and scene numbers. Returns 0 if unreadable."""
    r = (r or "").upper().strip()
    if r.isdigit(): return int(r)
    total, i = 0, 0
    vals = {"I":1,"V":5,"X":10,"L":50,"C":100}
    while i < len(r):
        if r[i] not in vals: return 0
        if i+1 < len(r) and r[i+1] in vals and vals[r[i+1]] > vals[r[i]]:
            total += vals[r[i+1]] - vals[r[i]]; i += 2
        else:
            total += vals[r[i]]; i += 1
    return total

# Regnal numbers, so the histories slug as scholars name them.
SH_REGNAL = {"second":"ii","third":"iii","fourth":"iv","fifth":"v",
             "sixth":"vi","eighth":"viii"}
# NOT "the comedy of": stripping it leaves "errors", which names nothing.
SH_STRIP = [r"^the tragedy of ", r"^the tragedie of ",
            r"^the life and death of ", r"^the life of ", r"^the history of ",
            r"^the famous history of the life of ", r"^the "]

SH_SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "from", "if",
            "in", "into", "nor", "of", "on", "or", "the", "to", "upon", "with"}

def sh_titlecase(s):
    """ALL'S WELL THAT ENDS WELL -> All's Well That Ends Well.

    str.title() capitalises the letter after an apostrophe, so it produced
    "All'S Well", "Love'S Labour'S Lost" and "The Winter'S Tale". Not merely a
    heading: a play's name is in the ref of every one of its units, so the
    error reached search results and copied citations too.
    """
    words = re.sub(r"\s+", " ", (s or "").strip().lower()).split()
    out = []
    for i, w in enumerate(words):
        small = w.strip(",;:.") in SH_SMALL
        if 0 < i < len(words) - 1 and small:
            out.append(w)
        else:
            out.append(re.sub(r"^([a-z\u00e0-\u00ff])",
                              lambda m: m.group(1).upper(), w))
    return " ".join(out)

def sh_manifest(lines):
    """The works this book says it contains, in order, from its own front
    Contents -- 38 plays and 6 poems.

    THIS IS THE CHECK THAT WAS MISSING. The Sonnets sit before the first play
    and have no Contents block of their own, so nothing recognised them as a
    work: flush() returns early while no work is open, and all 154 were
    dropped. No error, no warning, and the book still looked right because the
    38 plays were all present. A parser that can silently lose a sixth of its
    source needs a manifest to be checked against, and the book carries one.
    """
    # EVERY play carries its own "Contents" block too, listing "ACT I" and
    # "Scene I." -- so take the first Contents whose entries are work TITLES
    # rather than act and scene rows. Without that the guard read a play's
    # table as the book's manifest and failed the offline fixture.
    for start in [i for i, l in enumerate(lines) if l.strip() == "Contents"]:
        out = []
        for l in lines[start + 1:start + 90]:
            t = l.strip()
            if not t:
                if out:
                    break
                continue
            out.append(t)
        if len(out) >= 5 and not any(RE_SH_CONTENTS_ROW.match(t) for t in out):
            return out
    return []

RE_SH_SECTION = re.compile(r"^(\d{1,3}|[IVXL]{1,6})$")
RE_SH_ENDMARK = re.compile(r"^(THE END|FINIS|THE END\.|FINIS\.)$", re.I)

# Venus and Adonis carries the printed edition's marginal line numbers inside
# the text -- "Saith that the world hath ending with thy life.     12" -- on
# 196 of its 204 stanzas. Left in, they corrupt the line for reading, copying,
# search and the vocabulary digest alike.
# The lookbehind is load-bearing: without it this also ate the SONNET
# NUMBERS, which are themselves an indented bare numeral on a line of
# their own, and all 154 sonnets silently merged into one continuous
# 2,308-line poem. A marginal number only counts as one when the line
# has text in front of it.
RE_SH_MARGIN = re.compile(r"(?<=\S)\s{3,}\d{1,4}\s*$")

def _sh_blocks(lines):
    """Blank-line-separated blocks: a stanza, a sonnet, a paragraph."""
    out, cur = [], []
    for l in lines:
        if l.strip():
            cur.append(RE_SH_MARGIN.sub("", l).strip())
        elif cur:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out

def _sh_allcaps(t):
    return t.upper() == t and bool(re.search(r"[A-Z]", t))

def _sh_poem_start(blocks):
    """The block where the poem proper begins, so Lucrece line 1 is "From the
    besieged Ardea all in post" and not the first line of its dedication.

    Measured across all six poems: the prose apparatus is hard-wrapped and runs
    to 71 characters, while no verse line in any of them exceeds 56. So a block
    whose longest line passes 58 is prose, and the poem starts at the first
    verse-shaped block of three or more lines that follows the last prose seen
    SO FAR (not the last prose anywhere -- some verse later in the Sonnets runs
    long, which made a whole-poem scan pick block 199 of Venus) and that does
    not open with an ALL-CAPS heading: TO THE RIGHT HONOURABLE, THE ARGUMENT.,
    VENUS AND ADONIS.
    """
    last_prose = -1
    for i, bl in enumerate(blocks):
        if max(len(x) for x in bl) > 58:
            last_prose = i
            continue
        if len(bl) >= 3 and not _sh_allcaps(bl[0]) and i > last_prose:
            return i
    return 0

def convert_sh_poem(lines, slug, title, book="shakespeare"):
    """One of the six poems, as its own work.

    Sections where the text numbers them (the 154 sonnets; the Passionate
    Pilgrim's I-XX); otherwise one continuous run of numbered verse lines.
    Dedications and arguments are kept as unnumbered apparatus so they cannot
    shift the line numbers of the poem they precede.
    """
    blocks = _sh_blocks(lines)
    start = _sh_poem_start(blocks)
    units, section, label, lineno, appar = [], 0, None, 0, 0
    for i, bl in enumerate(blocks):
        if len(bl) == 1 and RE_SH_SECTION.match(bl[0]):
            label = bl[0]
            section = sh_roman(bl[0])
            lineno = 0
            continue
        # Gutenberg's end markers are not lines of the poem. Left in, "THE END"
        # became line 15 of Sonnet 154, which has fourteen.
        if len(bl) == 1 and RE_SH_ENDMARK.match(bl[0]):
            continue
        text = "\n".join(bl)
        # A lone ALL-CAPS line inside a poem is a heading, not a line of verse:
        # "THRENOS" was being numbered, which made The Phoenix and the Turtle
        # 68 lines long where it is 67. Kept as text, excluded from the count.
        if i >= start and len(bl) == 1 and _sh_allcaps(bl[0]):
            appar += 1
            units.append({
                "id": "%s:%s.%d.%ds%d" % (book, slug, section, lineno, appar),
                "ref": title, "text": text, "lines": None,
                "kind": "heading", "links": []})
            continue
        if i < start:
            appar += 1
            units.append({
                "id": "%s:%s.%d.%ds%d" % (book, slug, section, lineno, appar),
                "ref": title, "text": text, "lines": None,
                "kind": "apparatus", "links": []})
            continue
        first = lineno + 1
        lineno += len(bl)
        if slug == "sonnets" and section:
            ref = "Sonnet %d" % section
        elif label:
            ref = "%s, %s" % (title, label)
        else:
            # "l. 145" and not ", l." -- the scholarly abbreviation for a line
            # collides with the Roman numeral L (fifty), so the reader's table
            # of contents read "A Lover's Complaint, l" as a numbered division
            # and stopped trimming there. A bare number cites just as well.
            ref = "%s, %d" % (title, first)
        units.append({
            "id": "%s:%s.%d.%d" % (book, slug, section, first),
            "ref": ref, "text": text, "lines": [first, lineno], "links": []})
    return units

def sh_play_slug(title):
    """A stable, readable slug per play, derived from the title itself rather
    than from a hand-written abbreviation table (which would be one more thing
    to get wrong). 'The Tragedy Of Macbeth' -> macbeth; 'The First Part Of King
    Henry The Fourth' -> henry-iv-1."""
    t = re.sub(r"\s+", " ", title.strip().lower()).replace("’", "'")
    m = re.match(r"^the (first|second|third) part of (?:king )?henry the (\w+)", t)
    if m:
        part = {"first":"1","second":"2","third":"3"}[m.group(1)]
        return "henry-%s-%s" % (SH_REGNAL.get(m.group(2), m.group(2)), part)
    m = re.match(r"^(?:the life (?:and death )?of )?king (henry|richard|john)"
                 r"(?: the (\w+))?", t)
    if m:
        reg = SH_REGNAL.get(m.group(2) or "", m.group(2) or "")
        if not reg:                      # King John: no regnal number
            return "king-%s" % m.group(1)
        return ("%s-%s" % (m.group(1), reg)).strip("-")
    for pat in SH_STRIP:
        t2 = re.sub(pat, "", t)
        if t2 != t: t = t2; break
    t = t.split(",")[0].split(";")[0]
    t = re.sub(r"[^a-z0-9 ]", "", t)
    return re.sub(r"\s+", "-", t.strip())[:40] or "untitled"

def convert_shakespeare(path, slug="shakespeare"):
    """Complete Works (Gutenberg 100): play -> act -> scene -> speech-block,
    with the verse LINEATION PRESERVED and each block carrying its line range.

    Before 2026-09-07 this joined every line of a speech with a space, so
    "To be, or not to be" was stored as one 1,505-character prose paragraph and
    0 of 38,434 units contained a newline. The source has perfect lineation;
    the parser was destroying it. Line numbers are therefore never IN the text
    — they are a property of the line, rendered in a gutter, so a reader copies
    the poem and gets the poem.

    A play heading is an ALL-CAPS line followed, past blanks, by a line reading
    exactly "Contents". That is what separates a real title from a Dramatis
    Personae entry (A COURTESAN, BANDITTI, PRIEST, SHERIFF OF WILTSHIRE were all
    previously admitted as plays) and from the table of contents at the front.
    """
    raw = strip_boilerplate(open(path, encoding="utf-8", errors="replace").read())
    lines = raw.splitlines()

    # The book's own front Contents is the manifest: 38 plays and 6 poems. The
    # poems are found here rather than in the main loop, because the loop's
    # test for a work is "an ALL-CAPS line with a Contents block after it" and
    # NOT ONE OF THE SIX POEMS HAS ONE. The Sonnets were therefore dropped
    # outright and the other five were swallowed by whatever play preceded
    # them -- all of A Lover's Complaint, The Passionate Pilgrim, The Phoenix
    # and the Turtle, The Rape of Lucrece and Venus and Adonis were filed as
    # lines of The Winter's Tale, Act V Scene iii.
    manifest = sh_manifest(lines)
    man_slugs = [sh_play_slug(t) for t in manifest]
    poem_at, expect = {}, 0
    if manifest:
        # Candidates are taken IN MANIFEST ORDER. A cast list can hold a line
        # that slugs to a real work -- Richard II's Dramatis Personae opens
        # with "KING RICHARD THE SECOND" -- and an order-checked gate rejects
        # it, because that work has already been taken.
        man_end = next(i for i, l in enumerate(lines) if l.strip() == "Contents") \
                  + len(manifest)
        starts = []
        for i, line in enumerate(lines):
            if i <= man_end or expect >= len(man_slugs):
                continue
            t = line.strip()
            if not RE_SH_PLAY.match(t) or t.endswith(".") or SH_NOTPLAY.match(t):
                continue
            if sh_play_slug(t) != man_slugs[expect]:
                continue
            starts.append((i, man_slugs[expect], sh_titlecase(t)))
            expect += 1
        for n, (i, sl, title) in enumerate(starts):
            end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
            # A play has acts; a poem does not. That is the whole distinction,
            # and it is read from the text rather than from a list of titles.
            if not any(RE_SH_ACT.match(x.strip()) for x in lines[i + 1:end]):
                poem_at[i] = (sl, title, end)

    units = []
    skip_until = -1
    play = playslug = None
    act = scene = None
    act_n = scene_n = 0
    lineno = 0                    # running line within the current scene
    buf = []                      # [(lineno, text)]
    nonlocal_stage = [0]          # stage directions seen, for their ids
    in_contents = False           # inside a play's own table of contents
    contents_run = 0              # lines consumed by it, as a safety cap

    def ref_now():
        r = play
        if act: r += ", Act %s" % act
        if scene: r += " Sc. %s" % scene
        return r

    def flush():
        nonlocal buf
        rows = [(n, t) for n, t in buf if t]
        buf = []
        if not rows or not playslug:
            return
        text = "\n".join(t for _, t in rows)
        numbered = [n for n, _ in rows if n]
        if not numbered:
            # A stage direction standing alone. It takes no line number, but it
            # is still text and must stay findable — dropping it would quietly
            # delete "Enter Hamlet." and 5,000 like it from the corpus.
            nonlocal_stage[0] += 1
            units.append({
                "id": "%s:%s.%d.%d.%ds%d" % (slug, playslug, act_n, scene_n,
                                             lineno, nonlocal_stage[0]),
                "ref": ref_now(), "text": text, "lines": None,
                "kind": "stage", "links": []})
            return
        first, last = numbered[0], numbered[-1]
        units.append({
            "id": "%s:%s.%d.%d.%d" % (slug, playslug, act_n, scene_n, first),
            "ref": ref_now(), "text": text,
            "lines": [first, last],          # the range, for the citation
            "links": []})

    for i, line in enumerate(lines):
        if i < skip_until:
            continue
        if i in poem_at:
            # Emit the poem HERE, in source order, rather than appending all
            # six at the end -- the Sonnets come before the first play.
            flush()
            p_slug, p_title, p_end = poem_at[i]
            units.extend(convert_sh_poem(lines[i + 1:p_end], p_slug, p_title, slug))
            play = playslug = None
            act = scene = None
            act_n = scene_n = lineno = 0
            skip_until = p_end
            continue
        t = line.strip()

        # Each play opens with its own table of contents, whose entries read
        # "ACT V" and "Scene II" and were being consumed as real act/scene
        # markers. The front matter then inherited the LAST act and scene in
        # the table, and its units collided with the real Act V Scene II later
        # in the play — 263 duplicate ids across 38 plays. Skip the table.
        if in_contents:
            contents_run += 1
            # The table ends at the cast list. Not at "the first line that isn't
            # a contents row": plays differ, and Antony puts each scene's title
            # on the line AFTER its "Scene I." — which ended the block early and
            # emitted the whole table as text.
            # Ends at the cast list. Verified 2026-09-08: all 38 plays carry a
            # "Dramatis Personae" block within 220 lines of their heading, so
            # this terminator is sufficient; the 200-line cap is the seatbelt.
            # (Ending on the first speaker label instead looks tempting and is
            # wrong: Romeo's table trips it early and emits the cast heading as
            # a unit at 5.3.1, colliding with the real Act V Scene III.)
            if RE_SH_DRAMATIS.match(t) or contents_run > 200:
                in_contents = False   # fall through and treat this line normally
            else:
                continue

        am = RE_SH_ACT.match(t)
        if am:
            flush(); act, act_n = am.group(1), sh_roman(am.group(1))
            scene, scene_n, lineno = None, 0, 0
            continue
        sm = RE_SH_SCENE.match(t)
        if sm:
            flush(); scene, scene_n = sm.group(1), sh_roman(sm.group(1))
            lineno = 0; nonlocal_stage[0] = 0
            continue
        if (RE_SH_PLAY.match(t) and not t.endswith(".") and not SH_NOTPLAY.match(t)):
            # A play's own heading is followed by its Contents block. The TOC at
            # the front is followed by more titles; a Dramatis entry by more names.
            ahead = [x.strip() for x in lines[i + 1:i + 9]]
            if any(x == "Contents" for x in ahead):
                flush()
                play, act, scene = sh_titlecase(t), None, None
                playslug = sh_play_slug(t)
                act_n = scene_n = lineno = 0
                nonlocal_stage[0] = 0
                in_contents = True     # the heading rule guarantees one follows
                contents_run = 0
                continue
        if not t:
            if buf: flush()
        else:
            # Speaker labels and stage directions stay in the text but take no
            # line number, which is how an edition counts.
            if sh_numbered(t):
                lineno += 1
                buf.append((lineno, t))
            else:
                buf.append((0, t))
    flush()

    # 🔴 A work that produced nothing is a BUILD FAILURE, not an omission. This
    # is the guard whose absence let 154 sonnets disappear without a word.
    produced = {u["id"].split(":", 1)[1].split(".")[0] for u in units}
    missing = [t for t, sl in zip(manifest, man_slugs) if sl not in produced]
    if manifest and missing:
        raise ValueError(
            "shakespeare: %d of %d works in the book's own Contents produced no "
            "units: %s" % (len(missing), len(manifest), ", ".join(missing)))

    return {"slug": slug, "title": "The Complete Works of William Shakespeare",
            "author": "William Shakespeare",
            "source": {"path": os.path.relpath(path, CORPUS), "format": "gutenberg-txt",
                       "sha256": sha256(path)},
            "scheme": {"citation": "plays play.act.scene.line (shakespeare:macbeth.5.5.17); "
                                   "poems poem.section.line (shakespeare:sonnets.18.1, "
                                   "shakespeare:venus-and-adonis.0.145)",
                       "resolution": "speech-block or stanza, with its line range; "
                                     "a sonnet is one unit, so the poem is copied whole",
                       "honesty": "act/scene from headings; lineation preserved from "
                                  "the source; lines numbered per scene, counting spoken "
                                  "lines only (speaker names and stage directions excluded, "
                                  "as an editor excludes them). This Gutenberg text is our "
                                  "edition of record: numbers land within a line or two of "
                                  "standard editions where verse is unshared, and drift "
                                  "further where editors join a verse line split between "
                                  "speakers. Verify against a printed edition before any "
                                  "number is published as exact."},
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
    # Seed from the committed manifest, never start empty. The manifest IS the
    # collection (rule 1) and a run only sees the sources fetched locally, so
    # starting empty means a partial-corpus build silently deletes the
    # acquisitions ledger for every book it didn't happen to build. Found the
    # hard way 2026-09-06: a lexicons-only run rewrote a 66-book manifest with
    # 3 entries.
    manifest = {}
    mpath = os.path.join(BOOKS, "manifest.json")
    if os.path.exists(mpath):
        try:
            manifest = json.load(open(mpath, encoding="utf-8"))
        except (ValueError, OSError):
            manifest = {}
    jobs = []
    kjv = os.path.join(CORPUS, "kjv_bible.txt")
    if os.path.exists(kjv):
        jobs.append(("kjv", lambda: convert_kjv(kjv)))
    for slug, fn, conv in (("strongs-hebrew", "strongs-hebrew.xml", convert_strongs_hebrew),
                           ("strongs-greek",  "strongs-greek.xml",  convert_strongs_greek),
                           ("bdb-hebrew",     "bdb-hebrew.tsv",     convert_bdb),
                           ("thayer",         "thayer-pages.json",  convert_thayer)):
        p = os.path.join(CORPUS, "lexicons", fn)
        if os.path.exists(p):
            jobs.append((slug, lambda p=p, s=slug, c=conv: c(p, s)))
    for slug, files, title, author, note in (
        ("tbesg-greek", ["tbesg-greek.txt"],
         "Translators Brief Lexicon of Extended Strong's for Greek (TBESG)",
         "Abbott-Smith definitions, ed. Tyndale House / STEPBible.org",
         "Brief NT/LXX Greek lexicon based on Abbott-Smith (1922), edited to the "
         "extended Strong's numbering and filled from Middle Liddell where "
         "Abbott-Smith lacks an entry."),
        ("lsj-greek", ["tflsj-greek-0-5624.txt", "tflsj-greek-extra.txt"],
         "Liddell-Scott-Jones Greek Lexicon, Bible edition (TFLSJ)",
         "H. G. Liddell, R. Scott & H. S. Jones; ed. Tyndale House / STEPBible.org",
         "The full LSJ edited by Tyndale House scholars, abbreviations expanded, "
         "keyed to extended Strong's; the two files (0-5624 and the 6000+ extras "
         "for LXX and variant vocabulary) are one book."),
    ):
        ps = [os.path.join(CORPUS, "lexicons", f) for f in files]
        if all(os.path.exists(x) for x in ps):
            jobs.append((slug, lambda ps=ps, s=slug, t=title, a=author, n=note:
                         convert_stepbible_greek(ps, s, t, a, n)))
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
    # Author shelves declared in fetch_sources.py (Chesterton, 2026-09-29):
    # headings come from each book's own Contents, not a hand-written regex.
    import fetch_sources as _fs
    for slug, (_gid, title, author) in getattr(_fs, "CHESTERTON_GUTENBERG", {}).items():
        path = os.path.join(CORPUS, slug + ".txt")
        if os.path.exists(path):
            jobs.append((slug, lambda p=path, s=slug, t=title, a=author:
                         convert_gutenberg_prose(p, s, t, a, contents_chapre(p))))
    vdir = os.path.join(CORPUS, "vulgate")
    if os.path.isdir(vdir) and all(os.path.exists(os.path.join(vdir, b + ".lat"))
                                   for b in _fs.VULGATE["books"]):
        jobs.append(("vulgate", lambda: convert_vulgate(vdir, _fs.VULGATE["books"],
                                                         _fs.vulgate_digest(vdir))))
    drc = os.path.join(CORPUS, "douay", "DRC.json")
    if os.path.exists(drc):
        jobs.append(("douay", lambda: convert_douay(drc, _fs.VULGATE["books"], sha256(drc))))
    bz = os.path.join(CORPUS, "brenton", "eng-Brenton_usfm.zip")
    if os.path.exists(bz):
        jobs.append(("brenton", lambda: convert_brenton(bz, sha256(bz))))
    kz = os.path.join(CORPUS, "kjva", "engkjvcpb_usfm.zip")
    if os.path.exists(kz):
        jobs.append(("kjva", lambda: convert_kjva(kz, sha256(kz))))
    for eslug, e in _fs.ENGLISH.items():
        ep = os.path.join(CORPUS, "english", e["file"])
        if os.path.exists(ep):
            jobs.append((eslug, lambda p=ep, s=eslug: convert_english(p, s, sha256(p))))
    shk = os.path.join(CORPUS, "shakespeare.txt")
    if os.path.exists(shk):
        jobs.append(("shakespeare", lambda: convert_shakespeare(shk)))
    force = "--force" in os.sys.argv
    # A Bible's `kjv` fields come from a committed map, read at build time. A
    # kept book records the map it was built with; a changed (or newly built)
    # map rebuilds it, so the fields never go stale behind the resume.
    vdir_ = os.path.join(HERE, "..", "data", "versification")
    map_of = {"vulgate": ["vulgate-kjv.json", "deuterocanon.json"],
              "douay": ["vulgate-kjv.json", "deuterocanon.json"],
              "brenton": ["brenton-kjv.json", "deuterocanon.json"],
              **{s_: [f"{s_}-kjv.json"] for s_ in _fs.ENGLISH}}

    def map_sha(slug):
        """sha256 of the book's map(s): one, or several joined, as present."""
        mps = [os.path.join(vdir_, m) for m in map_of.get(slug, [])]
        shas = [sha256(mp) for mp in mps if os.path.exists(mp)]
        if not shas:
            return None
        if len(shas) == 1 and len(mps) == 1:
            return shas[0]
        return hashlib.sha256(" ".join(shas).encode("ascii")).hexdigest()
    for slug, job in jobs:
        out = os.path.join(BOOKS, slug + ".json")
        book = None
        if os.path.exists(out) and not force:   # resumable: reuse, still record in manifest
            book = json.load(open(out, encoding="utf-8"))
            if book["scheme"].get("kjv_map_sha256") != map_sha(slug):
                print(f"{slug}: its KJV map changed since it was built: rebuilding")
                book = None
        if book is not None:
            manifest[slug] = {"title": book["title"], "author": book["author"],
                              "format": book["source"]["format"],
                              "sha256": book["source"]["sha256"],
                              "units": len(book["units"]), "scheme": book["scheme"],
                              **({"rights": book["rights"]} if book.get("rights") else {})}
            print(f"{slug}: {len(book['units'])} units (kept)")
            continue
        book = job()
        if map_sha(slug):
            book["scheme"]["kjv_map_sha256"] = map_sha(slug)
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
                          "scheme": book["scheme"],
                          **({"rights": book["rights"]} if book.get("rights") else {})}
        print(f"{slug}: {len(book['units'])} units — {book['title']}")
    with open(os.path.join(BOOKS, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, ensure_ascii=False)
    print(f"MANIFEST: {len(manifest)} books")

if __name__ == "__main__":
    main()
