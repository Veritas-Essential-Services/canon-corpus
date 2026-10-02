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
import os, re, json, hashlib, html, html.entities, unicodedata
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
    # Every translator the title names, not just the first: Strabo is
    # Hamilton & Falconer, Tacitus is Church & Brodribb.
    transl = [(t.text or "").strip()
              for t in root.findall(".//t:titleStmt/t:editor[@role='translator']", ns)]
    return (title.text if title is not None else "?",
            (author.text or "?") if author is not None else "?",
            " & ".join(t for t in transl if t))


def tei_load(path):
    """Parse a Perseus TEI file. Most are TEI P5. The older ones are TEI P4
    (<TEI.2>, no namespace, numbered <div1>/<div2>, and HTML entities like
    &aelig; that only their DTD defines). Those are lifted into the P5 shape
    in memory -- namespaced, each numbered div a textpart -- so one set of
    converters reads both. The source file is never touched (rule 2). An
    unnumbered div (Agricola's lone book) stays a wrapper, not a level."""
    parser = ET.XMLParser()
    parser.entity.update({k: chr(v) for k, v in html.entities.name2codepoint.items()})
    root = ET.parse(path, parser=parser).getroot()
    if root.tag != "TEI.2":
        return root
    for e in root.iter():
        if not isinstance(e.tag, str) or e.tag.startswith("{"):
            continue
        if re.fullmatch(r"div\d", e.tag):
            if e.get("n") is not None:
                e.set("subtype", e.get("type") or "")
                e.set("type", "textpart")
            e.tag = TEI_NS + "div"
        else:
            e.tag = TEI_NS + e.tag
    return root

def perseus_rights(root):
    """The rights block every Perseus-derived book carries. The translations
    are PD; Perseus's TEI, and any modernizing of the wording it did (the
    title says when), are CC BY-SA 4.0 -- share-alike. The licence is read
    from the file where the file states one; the repository (greekLit or
    latinLit) is read from the file's own CTS urn."""
    T = "{http://www.tei-c.org/ns/1.0}"
    lic = root.find(f".//{T}publicationStmt//{T}licence")
    body = root.find(f".//{T}body")
    base = (body.get("{http://www.w3.org/XML/1998/namespace}base") or "") if body is not None else ""
    if not base:
        d = root.find(f".//{T}body/{T}div")
        base = (d.get("n") or "") if d is not None else ""
    repo = "canonical-latinLit" if ":latinLit:" in base else "canonical-greekLit"
    return {"license": "CC BY-SA 4.0",
            "attribution": f"Perseus Digital Library, Tufts University (PerseusDL/{repo})",
            "source_url": f"https://github.com/PerseusDL/{repo}",
            "redistribute_whole": True,
            "note": ("licence line read from this file: " + clean("".join(lic.itertext()))
                     if lic is not None else
                     "this file states no licence; the repository's licence is CC BY-SA 4.0")
                    + ". The translation itself is public domain; the TEI, and any "
                      "modernizing of the wording Perseus did (the title says when), are "
                      "share-alike: a derivative must credit Perseus and carry the same "
                      "licence."}


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
            "rights": perseus_rights(root),
            "units": units}

TEI_NS = "{http://www.tei-c.org/ns/1.0}"


TEI_BLOCKS = {TEI_NS + t for t in ("l", "lg", "p", "div", "head", "item", "list",
                                   "quote", "sp", "speaker", "ab", "gap")}


def tei_pieces(e, _parent=None):
    """itertext(), minus Perseus's gazetteer: inside <name type="place"> a
    <reg> holds "Bodrum [27.466,37.5] (inhabited place), Turkey..." -- the
    modern place it resolves to, not the translator's words."""
    if e.tag == TEI_NS + "reg" and _parent == TEI_NS + "name":
        return
    if e.text:
        yield e.text
    for c in e:
        yield from tei_pieces(c, e.tag)
        if c.tail:
            yield c.tail


def tei_clean(s):
    """clean() for text that came out of an XML parser: it is already plain
    text, so a literal "<Pisidians>" (an editor's angle-bracket supplement in
    Godley) is words, not a tag, and must not be stripped as one."""
    return clean(s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def tei_note(e):
    return {k: v for k, v in (("by", e.get("resp") or ""), ("n", e.get("n") or ""),
                              ("text", tei_clean(" ".join(tei_pieces(e))))) if v}


def tei_split(el):
    """An element's reading text, with what is not reading text lifted out.

    Stage directions and footnotes are not the text: they come back
    separately (stage, notes), keep everything else including <del>, the
    translation's own brackets. A lifted note or stage direction leaves a
    space where it sat when letters touch on both sides: Perseus often has
    "Pluto's<note>..</note>stream", which reads as one word once the note is
    gone. <choice> reads the correction or regularization and keeps what was
    printed (sic / orig) beside it. Returns (text, stage, notes, sic)."""
    T = TEI_NS
    parts, stage, notes, sics = [], [], [], []

    def lift(e):
        if parts and e.tail and parts[-1][-1:].isalnum() and e.tail[:1].isalnum():
            parts.append(" ")
        if e.tail: parts.append(e.tail)

    def walk(e, parent=None):
        if e.tag == T + "reg" and parent == T + "name":
            if e.tail: parts.append(e.tail)       # gazetteer, not text
            return
        if e.tag == T + "stage" and e is not el:
            t, s2, n2, c2 = tei_split(e)          # a stage direction may carry a footnote
            stage.extend([t] + s2); notes.extend(n2); sics.extend(c2)
            lift(e)
            return
        if e.tag == T + "note":
            notes.append(tei_note(e))
            lift(e)
            return
        if e.tag == T + "choice" and (e.find(T + "corr") is not None
                                      or e.find(T + "reg") is not None):
            # <choice><sic>Bacchus</sic><corr>Dionysus</corr></choice>: the
            # reading text takes the correction (Perseus's modernizing, or a
            # fixed typo); what the edition printed is kept, never thrown away.
            good = e.find(T + "corr") if e.find(T + "corr") is not None else e.find(T + "reg")
            bad = e.find(T + "sic") if e.find(T + "sic") is not None else e.find(T + "orig")
            parts.append("".join(good.itertext()))
            if bad is not None:
                sics.append({"corr": clean("".join(good.itertext())),
                             "sic": clean("".join(bad.itertext()))})
            if e.tail: parts.append(e.tail)
            return
        # A verse line or paragraph is a break even when the TEI runs them
        # together ("virtuous</q></l><l><q>And"): never weld two lines.
        block = e is not el and e.tag in TEI_BLOCKS
        if block: parts.append("\x00")
        if e.text: parts.append(e.text)
        for c in e:
            walk(c, e.tag)
        if block: parts.append("\x00")
        if e is not el and e.tail: parts.append(e.tail)
    walk(el)
    joined = re.sub(r"\x00+(?=\s*[;:,.!?)\]])", "", "".join(parts)).replace("\x00", " ")
    return (tei_clean(joined), [s for s in stage if s],
            [n for n in notes if n.get("text")], sics)


# Perseus PROSE: histories and treatises in English, nested textpart divs
# (book / chapter / section) carrying the canonical citation born-in. One
# unit per innermost div, so "Hdt. 1.1.1" is exact to the section.
TEI_PROSE = {
    "herodotus-histories-godley": "Hdt.",
    "thucydides-history-crawley": "Thuc.",
    "xenophon-anabasis-brownson": "Xen. Anab.",
    "xenophon-hellenica-brownson": "Xen. Hell.",
    "xenophon-cyropaedia-miller": "Xen. Cyr.",
    "plutarch-theseus-perrin": "Plut. Theseus",
    "plutarch-romulus-perrin": "Plut. Romulus",
    "plutarch-comparison-theseus-romulus-perrin": "Plut. Comparison of Theseus and Romulus",
    "plutarch-lycurgus-perrin": "Plut. Lycurgus",
    "plutarch-numa-perrin": "Plut. Numa",
    "plutarch-comparison-lycurgus-numa-perrin": "Plut. Comparison of Lycurgus and Numa",
    "plutarch-solon-perrin": "Plut. Solon",
    "plutarch-publicola-perrin": "Plut. Publicola",
    "plutarch-comparison-solon-publicola-perrin": "Plut. Comparison of Solon and Publicola",
    "plutarch-themistocles-perrin": "Plut. Themistocles",
    "plutarch-camillus-perrin": "Plut. Camillus",
    "plutarch-pericles-perrin": "Plut. Pericles",
    "plutarch-fabius-maximus-perrin": "Plut. Fabius Maximus",
    "plutarch-comparison-pericles-fabius-maximus-perrin": "Plut. Comparison of Pericles and Fabius Maximus",
    "plutarch-alcibiades-perrin": "Plut. Alcibiades",
    "plutarch-caius-marcius-coriolanus-perrin": "Plut. Caius Marcius Coriolanus",
    "plutarch-comparison-alcibiades-coriolanus-perrin": "Plut. Comparison of Alcibiades and Coriolanus",
    "plutarch-timoleon-perrin": "Plut. Timoleon",
    "plutarch-aemilius-paulus-perrin": "Plut. Aemilius Paulus",
    "plutarch-comparison-timoleon-aemilius-perrin": "Plut. Comparison of Timoleon and Aemilius",
    "plutarch-pelopidas-perrin": "Plut. Pelopidas",
    "plutarch-marcellus-perrin": "Plut. Marcellus",
    "plutarch-comparison-pelopidas-marcellus-perrin": "Plut. Comparison of Pelopidas and Marcellus",
    "plutarch-aristides-perrin": "Plut. Aristides",
    "plutarch-marcus-cato-perrin": "Plut. Marcus Cato",
    "plutarch-comparison-aristides-marcus-cato-perrin": "Plut. Comparison of Aristides and Marcus Cato",
    "plutarch-philopoemen-perrin": "Plut. Philopoemen",
    "plutarch-titus-flamininus-perrin": "Plut. Titus Flamininus",
    "plutarch-comparison-philopoemen-titus-perrin": "Plut. Comparison of Philopoemen and Titus",
    "plutarch-pyrrhus-perrin": "Plut. Pyrrhus",
    "plutarch-caius-marius-perrin": "Plut. Caius Marius",
    "plutarch-lysander-perrin": "Plut. Lysander",
    "plutarch-sulla-perrin": "Plut. Sulla",
    "plutarch-comparison-lysander-sulla-perrin": "Plut. Comparison of Lysander and Sulla",
    "plutarch-cimon-perrin": "Plut. Cimon",
    "plutarch-lucullus-perrin": "Plut. Lucullus",
    "plutarch-comparison-lucullus-cimon-perrin": "Plut. Comparison of Lucullus and Cimon",
    "plutarch-nicias-perrin": "Plut. Nicias",
    "plutarch-crassus-perrin": "Plut. Crassus",
    "plutarch-comparison-nicias-crassus-perrin": "Plut. Comparison of Nicias and Crassus",
    "plutarch-eumenes-perrin": "Plut. Eumenes",
    "plutarch-sertorius-perrin": "Plut. Sertorius",
    "plutarch-comparison-sertorius-eumenes-perrin": "Plut. Comparison of Sertorius and Eumenes",
    "plutarch-agesilaus-perrin": "Plut. Agesilaus",
    "plutarch-pompey-perrin": "Plut. Pompey",
    "plutarch-comparison-agesilaus-pompey-perrin": "Plut. Comparison of Agesilaus and Pompey",
    "plutarch-alexander-perrin": "Plut. Alexander",
    "plutarch-caesar-perrin": "Plut. Caesar",
    "plutarch-phocion-perrin": "Plut. Phocion",
    "plutarch-cato-the-younger-perrin": "Plut. Cato the Younger",
    "plutarch-agis-cleomenes-perrin": "Plut. Agis and Cleomenes",
    "plutarch-tiberius-caius-gracchus-perrin": "Plut. Tiberius and Caius Gracchus",
    "plutarch-comparison-agis-cleomenes-the-gracchi-perrin": "Plut. Comparison of Agis and Cleomenes and the Gracchi",
    "plutarch-demosthenes-perrin": "Plut. Demosthenes",
    "plutarch-cicero-perrin": "Plut. Cicero",
    "plutarch-comparison-demosthenes-cicero-perrin": "Plut. Comparison of Demosthenes and Cicero",
    "plutarch-demetrius-perrin": "Plut. Demetrius",
    "plutarch-antony-perrin": "Plut. Antony",
    "plutarch-comparison-demetrius-antony-perrin": "Plut. Comparison of Demetrius and Antony",
    "plutarch-dion-perrin": "Plut. Dion",
    "plutarch-brutus-perrin": "Plut. Brutus",
    "plutarch-comparison-dion-brutus-perrin": "Plut. Comparison of Dion and Brutus",
    "plutarch-aratus-perrin": "Plut. Aratus",
    "plutarch-artaxerxes-perrin": "Plut. Artaxerxes",
    "plutarch-galba-perrin": "Plut. Galba",
    "plutarch-otho-perrin": "Plut. Otho",
    "polybius-histories-shuckburgh": "Polyb.",
    "josephus-antiquities-whiston": "Joseph. AJ",
    "josephus-life-whiston": "Joseph. Vit.",
    "josephus-against-apion-whiston": "Joseph. Ap.",
    "josephus-jewish-war-whiston": "Joseph. BJ",
    "strabo-geography-hamilton": "Strab.",
    "apollodorus-library-frazer": "Apollod.",
    "apollodorus-epitome-frazer": "Apollod. Epit.",
    "diogenes-laertius-lives-hicks": "Diog. Laert.",
    "epictetus-discourses-higginson": "Epict. Diss.",
    "epictetus-handbook-higginson": "Epict. Ench.",
    "aeschines-timarchus-adams": "Aeschin. 1",
    "aeschines-embassy-adams": "Aeschin. 2",
    "aeschines-ctesiphon-adams": "Aeschin. 3",
    "caesar-gallic-war-mcdevitte": "Caes. Gal.",
    "caesar-civil-war-peskett": "Caes. Civ.",
    "tacitus-agricola-church": "Tac. Ag.",
    "tacitus-germania-church": "Tac. Ger.",
    "tacitus-dialogus-church": "Tac. Dial.",
    "tacitus-histories-church": "Tac. Hist.",
    "tacitus-annals-church": "Tac. Ann.",
    "suetonius-julius-thomson": "Suet. Jul.",
    "suetonius-augustus-thomson": "Suet. Aug.",
    "suetonius-tiberius-thomson": "Suet. Tib.",
    "suetonius-caligula-thomson": "Suet. Calig.",
    "suetonius-claudius-thomson": "Suet. Claud.",
    "suetonius-nero-thomson": "Suet. Ner.",
    "suetonius-galba-thomson": "Suet. Galb.",
    "suetonius-otho-thomson": "Suet. Otho",
    "suetonius-vitellius-thomson": "Suet. Vit.",
    "suetonius-vespasian-thomson": "Suet. Vesp.",
    "suetonius-titus-thomson": "Suet. Tit.",
    "suetonius-domitian-thomson": "Suet. Dom.",
}

# A per-book line appended to the Perseus rights note, where the edition
# Perseus keyed carries matter whose provenance the file does not settle.
TEI_RIGHTS_NOTE = {s: ("Perseus keyed this text from the Modern Library's 1942 reprint of "
                       "Church & Brodribb (Macmillan, 1864-77). The translation is theirs "
                       "and public domain; whether the marginal headings (apparatus.head "
                       "and apparatus.notes here, never the reading text) are Church & "
                       "Brodribb's or the 1942 reprint's was not checked against the "
                       "Macmillan scan.")
                   for s in ("tacitus-agricola-church", "tacitus-germania-church",
                             "tacitus-dialogus-church", "tacitus-histories-church",
                             "tacitus-annals-church")}
RE_TGN = re.compile(r"tgn,(\d+)")


def convert_tei_prose(path, slug, abbrev):
    T = TEI_NS
    root = tei_load(path)
    title, author, transl = tei_meta(root)
    body = root.find(f".//{T}body")
    units, pending_head, levels = [], [], []
    nnotes = 0

    def is_part(e):
        return e.tag == T + "div" and e.get("type") == "textpart"

    def visit(e, path_ns):
        nonlocal nnotes
        kids = [c for c in e if is_part(c)]
        if is_part(e) and e.get("subtype") and e.get("subtype").lower() not in levels:
            levels.append(e.get("subtype").lower())
        if is_part(e) and not kids:
            text, _stage, notes, sic = tei_split(e)
            ref = ".".join(path_ns)
            links, seen = [], set()
            for pl in e.iter(T + "placeName"):
                m = RE_TGN.search(pl.get("key") or "")
                if m and m.group(1) not in seen:
                    seen.add(m.group(1))
                    links.append({"kind": "place", "target": f"tgn:{m.group(1)}",
                                  "name": clean("".join(pl.itertext()))})
            app = {}
            if pending_head:
                app["head"] = list(pending_head); pending_head.clear()
            if notes:
                app["notes"] = notes; nnotes += len(notes)
            if sic:
                app["sic"] = sic
            if e.find(f".//{T}gap") is not None:
                app["gap"] = True               # a lacuna: flagged, never filled
            if text:
                u = {"id": f"{slug}:{ref}", "ref": f"{abbrev} {ref}", "text": text,
                     "links": links}
                if app:
                    u["apparatus"] = app
                units.append(u)
            elif units and app:
                for k, v in app.items():
                    a = units[-1].setdefault("apparatus", {})
                    if v is True:
                        a[k] = True             # a lacuna in a textless division
                    else:
                        a.setdefault(k, []).extend(v)
            return
        for c in e:
            if is_part(c):
                visit(c, path_ns + [c.get("n") or "?"])
            elif any(is_part(d) for d in c.iter()):
                visit(c, path_ns)               # a wrapper (the translation div)
            elif c.tag != T + "milestone":
                # Text between divisions (a book's <head>, an argument):
                # kept, riding on the next unit as apparatus.head.
                t, _s, n2, _c = tei_split(c)
                if t:
                    pending_head.append(t)
                if n2:
                    pending_head.extend(n["text"] for n in n2)

    visit(body, [])
    if pending_head and units:
        units[-1].setdefault("apparatus", {}).setdefault("head", []).extend(pending_head)
    places = sum(len(u["links"]) for u in units)
    # Is each unit ONE numbered division, or a run of them? Josephus in
    # Perseus is divided at Whiston's paragraphs, numbered by their first
    # Niese section (AJ 1.1, 1.5, 1.27...): a citation of AJ 1.3 lives in
    # unit 1.1. Measured, not assumed: count numbering jumps between
    # siblings.
    jumps = steps = 0
    for a, b in zip(units, units[1:]):
        pa, pb_ = a["id"].split(":", 1)[1].split("."), b["id"].split(":", 1)[1].split(".")
        if pa[:-1] == pb_[:-1] and pa[-1].isdigit() and pb_[-1].isdigit():
            steps += 1
            jumps += int(pb_[-1]) - int(pa[-1]) > 1
    spans = steps and jumps / steps > 0.1
    honesty = ("each unit is the run of numbered sections from its id to the next "
               f"unit's ({jumps:,} of {steps:,} steps skip numbers): a citation "
               "resolves to the unit that contains it" if spans else
               "exact to the source's innermost division (the standard section "
               "numbering, born-in from Perseus)")
    rights = perseus_rights(root)
    if slug in TEI_RIGHTS_NOTE:
        rights["note"] += " " + TEI_RIGHTS_NOTE[slug]
    return {"slug": slug, "title": title, "author": author,
            "source": {"path": os.path.relpath(path, CORPUS), "format": "tei",
                       "translator": transl, "sha256": sha256(path)},
            "scheme": {"citation": f"{abbrev} {'.'.join(levels)}",
                       "resolution": (levels[-1] if levels else "section")
                                     + (" (span)" if spans else ""),
                       "honesty": honesty,
                       "note": f"Perseus TEI, one unit per innermost textpart div. "
                               f"{nnotes} translator's/editor's footnote(s) lifted out of "
                               f"the reading text into apparatus.notes; text between "
                               f"divisions (headings, arguments) kept as apparatus.head; "
                               f"{places} place reference(s) linked by Getty TGN id "
                               f"(Perseus's gazetteer glosses dropped from the text, the "
                               f"id kept)."},
            "rights": rights,
            "units": units}


# Perseus drama: Greek plays in prose translation, marked up as <sp> speeches
# whose <l n="..."> segments are anchored to the GREEK line numbers -- the
# citation every commentary uses (Ant. 450). One unit per segment, so a
# citation resolves to the segment containing it.
TEI_DRAMA = {
    "sophocles-trachiniae-jebb": "Soph. Trach.",
    "sophocles-antigone-jebb": "Soph. Ant.",
    "sophocles-ajax-jebb": "Soph. Aj.",
    "sophocles-oedipus-tyrannus-jebb": "Soph. OT",
    "sophocles-electra-jebb": "Soph. El.",
    "sophocles-philoctetes-jebb": "Soph. Phil.",
    "sophocles-oedipus-colonus-jebb": "Soph. OC",
    "aeschylus-supplices-smyth": "Aesch. Supp.",
    "aeschylus-persians-smyth": "Aesch. Pers.",
    "aeschylus-prometheus-smyth": "Aesch. PV",
    "aeschylus-seven-smyth": "Aesch. Sept.",
    "aeschylus-agamemnon-smyth": "Aesch. Ag.",
    "aeschylus-libation-bearers-smyth": "Aesch. Cho.",
    "aeschylus-eumenides-smyth": "Aesch. Eum.",
    "euripides-cyclops-coleridge": "Eur. Cyc.",
    "euripides-alcestis-coleridge": "Eur. Alc.",
    "euripides-medea-coleridge": "Eur. Med.",
    "euripides-heracleidae-coleridge": "Eur. Heracl.",
    "euripides-hippolytus-coleridge": "Eur. Hipp.",
    "euripides-andromache-coleridge": "Eur. Andr.",
    "euripides-hecuba-coleridge": "Eur. Hec.",
    "euripides-suppliants-coleridge": "Eur. Supp.",
    "euripides-heracles-coleridge": "Eur. HF",
    "euripides-ion-coleridge": "Eur. Ion",
    "euripides-trojan-women-coleridge": "Eur. Tro.",
    "euripides-electra-coleridge": "Eur. El.",
    "euripides-iphigenia-tauris-coleridge": "Eur. IT",
    "euripides-helen-coleridge": "Eur. Hel.",
    "euripides-phoenissae-coleridge": "Eur. Phoen.",
    "euripides-orestes-coleridge": "Eur. Or.",
    "euripides-bacchae-buckley": "Eur. Ba.",
    "euripides-iphigenia-aulis-coleridge": "Eur. IA",
    "euripides-rhesus-coleridge": "Eur. Rh.",
    "aristophanes-clouds-hickie": "Ar. Nub.",
}
# Per-book line-number fixes (rule 2: never hand-edit a source; fix here so it
# reruns on refetch). Each is a typo in the Perseus file, shown by context.
TEI_DRAMA_N_FIX = {
    # Antigone's half-line completing Oedipus' 1099 ("Where? Where?" /
    # "Father, father,"), between 1099 and 1100: the file says 1009a.
    ("sophocles-oedipus-colonus-jebb", "1009a"): "1099a",
    # Between 405 and 410, a line number with a stray digit.
    ("aeschylus-supplices-smyth", "4097"): "407",
    # Between 1187 and 1189, and between 562 and 564: digits dropped / doubled.
    ("euripides-iphigenia-tauris-coleridge", "188"): "1188",
    ("euripides-helen-coleridge", "5563"): "563",
}


def convert_tei_drama(path, slug, abbrev):
    T = "{http://www.tei-c.org/ns/1.0}"
    root = tei_load(path)
    title, author, transl = tei_meta(root)
    body = root.find(f".//{T}body")
    units, pending_stage, pending_notes, pending_sic, fixes, gaps = [], [], [], [], 0, 0
    section, speaker, personae = "", "", []

    note_of, seg_text = tei_note, tei_split

    def visit(e):
        nonlocal section, speaker, fixes, gaps
        tag = e.tag
        if tag == T + "div" and e.get("type") == "textpart":
            section = e.get("subtype") or section
        elif tag == T + "speaker":
            speaker = clean("".join(e.itertext()))
            return
        elif tag == T + "stage":
            t, s2, n2, c2 = seg_text(e)
            pending_stage.extend(x for x in [t] + s2 if x)
            pending_notes.extend(n2)
            pending_sic.extend(c2)
            return
        elif tag == T + "note":
            ps = [clean(" ".join(p.itertext())) for p in e.iter(T + "p")]
            if ps and ps[0].lower() == "dramatis personae":
                personae.extend(x for x in ps[1:] if x)     # the cast list, kept whole
            else:
                n = note_of(e)
                if n.get("text"):
                    pending_notes.append(n)
            return
        elif tag == T + "l":
            n = e.get("n") or ""
            if (slug, n) in TEI_DRAMA_N_FIX:
                n = TEI_DRAMA_N_FIX[(slug, n)]
                fixes += 1
            text, inner, inotes, isic = seg_text(e)
            gap = e.find(f".//{T}gap") is not None
            gaps += gap
            drama = {"speaker": speaker, "section": section}
            if pending_stage or inner:
                drama["stage"] = pending_stage + inner
            if pending_notes or inotes:
                drama["notes"] = pending_notes + inotes
            if pending_sic or isic:
                drama["sic"] = pending_sic + isic
            if gap:
                drama["gap"] = True
            pending_stage.clear()
            pending_notes.clear()
            pending_sic.clear()
            if text:
                units.append({"id": f"{slug}:{n}", "ref": f"{abbrev} {n}",
                              "text": text, "links": [], "drama": drama})
            elif units:
                for k in ("stage", "notes", "sic"):
                    if drama.get(k):
                        units[-1]["drama"].setdefault(k, []).extend(drama[k])
            else:
                pending_stage.extend(drama.get("stage", []))
                pending_notes.extend(drama.get("notes", []))
                pending_sic.extend(drama.get("sic", []))
            return
        elif tag == T + "sp":
            speaker = ""
        for c in e:
            visit(c)

    visit(body)
    if units:                                   # the closing exit, a last note
        for k, v in (("stage", pending_stage), ("notes", pending_notes), ("sic", pending_sic)):
            if v:
                units[-1]["drama"].setdefault(k, []).extend(v)
    nnotes = sum(len(u["drama"].get("notes", [])) for u in units)
    book = {"slug": slug, "title": title, "author": author,
            "source": {"path": os.path.relpath(path, CORPUS), "format": "tei",
                       "translator": transl, "sha256": sha256(path)},
            "scheme": {"citation": f"{abbrev} line (Greek lineation)",
                       "resolution": "segment",
                       "honesty": "prose translation segmented at Greek line numbers: "
                                  "a citation resolves to the segment that contains it "
                                  "(segments run 1-5 Greek lines), not to an exact line",
                       "note": f"Perseus TEI, one unit per <l> segment; speaker, choral "
                               f"section and stage directions under each unit's `drama` "
                               f"(stage directions are kept out of the spoken text, never "
                               f"dropped). {fixes} line number(s) corrected by "
                               f"TEI_DRAMA_N_FIX; {gaps} segment(s) contain a lacuna the "
                               f"translator marks as lost (drama.gap). {nnotes} footnote(s) "
                               f"lifted out of the spoken text into drama.notes"
                               + (f"; the cast list is under dramatis_personae ({len(personae)})"
                                  if personae else "") + "."},
            "rights": perseus_rights(root),
            "units": units}
    if personae:
        book["dramatis_personae"] = personae
    return book

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
# reference string, plus the OSIS book/chapter/verse it states) and is NOT
# resolved to a kjv: unit id. A labelled hole beats a confident wrong label;
# resolving these needs a versification map, which is its own piece of work.

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
    units, furniture, extended = [], 0, 0
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
                links.append({"kind": "scripture", "osis": key,
                              "ref": clean(label) or key, "versification": "bhs",
                              "resolved": False})
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
                               "source's own (Hebrew/BHS) versification and are NOT resolved "
                               "to kjv: unit ids -- Psalms superscriptions shift the numbering. "
                               f"{furniture} navigation/header furniture blocks stripped; "
                               f"{extended} refs above H{HEBREW_MAX} dropped as extended "
                               "Strong's prefix/particle codes."},
            "units": units}

GRK = "Ͱ-Ͽἀ-῿̀-ͯ"
RE_GREEK = re.compile(f"[{GRK}]")
RE_THAYER_HEAD = re.compile(rf"^([{GRK}][{GRK}’'\-]*)\s*[,.]\s+")


def _thayer_page(raw):
    """One OCR page -> (furniture, body_lines). Page furniture: line 1 of a
    body page is the running head (the Greek catchword) and bare page numbers
    sit on their own line. Stripped by pattern and counted, never silently.
    Shared by the page book and the entry book so both see the same body."""
    lines = raw.split("\n")
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
    return furniture, body_lines


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
        furniture, body_lines = _thayer_page(pages[pno])
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

# ------------------------------------------------- Thayer, split into entries
#
# A SECOND book over the same OCR, not a change to the first. `thayer` stays
# the page book, byte for byte: its ids (thayer:p.300) are citations and rule 3
# says existing id schemes don't move without a vault ruling. `thayer-entries`
# is a new door onto the same pages, one unit per inferred entry, and every
# entry links back to the page(s) it sits on so it can always be checked
# against the scan.

# Greek -> Latin for ids only (never for display). Rough breathing becomes h.
_GR2LAT = dict(zip("αβγδεζηθικλμνξοπρστυφχψως",
                   ["a", "b", "g", "d", "e", "z", "e", "th", "i", "k", "l", "m", "n",
                    "x", "o", "p", "r", "s", "t", "u", "ph", "ch", "ps", "o", "s"]))


def thayer_key(word):
    """The alphabetising key: accents, breathings, case, final sigma and stray
    apostrophes/hyphens all ignored. OCR errs most in diacritics (see the page
    book's honesty field), so ordering on bare letters is what survives it."""
    d = unicodedata.normalize("NFD", word)
    d = "".join(c for c in d if not unicodedata.combining(c)).lower()
    d = d.replace("ς", "σ").replace("ϲ", "σ")
    return re.sub(r"[^α-ω]", "", d)


def thayer_form(word):
    """The headword WITH its accents (case and final sigma still ignored):
    what tells εἰμί 'I am' from εἶμι 'I go', which thayer_key merges."""
    d = unicodedata.normalize("NFC", word).lower()
    return d.replace("ς", "σ").replace("ϲ", "σ")


def thayer_translit(word):
    d = unicodedata.normalize("NFD", word)
    rough = "̔" in d[:4]
    out = "".join(_GR2LAT.get(c, "") for c in thayer_key(word))
    if rough and out.startswith("r"):
        return "rh" + out[1:]              # ῥῆμα -> rhema, not hrema
    return ("h" + out) if rough else out


def _lis_weighted(keys, weights, forms=None, homograph=None):
    """Max-weight STRICTLY increasing subsequence, in reading order. Fenwick
    tree over key ranks: O(n log n), n ~ 8k. Returns the chosen indices.
    Ties on total weight go to the EARLIER predecessor, so a rerun on the same
    input picks the same chain -- the build must be deterministic.

    One exception to "strictly": two candidates may share a key when both are
    flagged `homograph` and their accented `forms` differ -- εἰμί then εἶμι,
    two real entries that only an accent tells apart. A repeated mention of
    the SAME form never qualifies, which is what keeps a headword cited again
    mid-entry from opening a second entry."""
    ranks = {k: i + 1 for i, k in enumerate(sorted(set(keys)))}
    size = len(ranks)
    tree = [(0, -1)] * (size + 1)          # (best weight, index) per prefix

    def query(r):                          # best over ranks 1..r
        best = (0, -1)
        while r > 0:
            if tree[r][0] > best[0]:
                best = tree[r]
            r -= r & -r
        return best

    def update(r, val):
        while r <= size:
            if val[0] > tree[r][0]:
                tree[r] = val
            r += r & -r

    dp, prev = [0] * len(keys), [-1] * len(keys)
    same = {}                              # key -> {form: (best dp, index)}, homographs only
    for i, k in enumerate(keys):
        r = ranks[k]
        w, j = query(r - 1)                # strictly smaller keys only
        if homograph and homograph[i]:
            for f, (hw, hj) in sorted(same.get(k, {}).items()):
                if f != forms[i] and hw > w:
                    w, j = hw, hj
        dp[i], prev[i] = w + weights[i], j
        update(r, (dp[i], i))
        if homograph and homograph[i]:
            bucket = same.setdefault(k, {})
            if dp[i] > bucket.get(forms[i], (0, -1))[0]:
                bucket[forms[i]] = (dp[i], i)
    if not keys:
        return []
    end = max(range(len(keys)), key=lambda i: (dp[i], -i))
    chain = []
    while end != -1:
        chain.append(end)
        end = prev[end]
    return chain[::-1]


def strongs_greek_lemmas(path):
    """Strong's Greek headwords -> {thayer_key: [(G-number, thayer_form), ...]}. Strong's
    covers the same New Testament vocabulary Thayer's does, so a candidate
    headword that IS a Strong's lemma is far likelier to open an entry than a
    Greek word that merely starts a line."""
    out = {}
    for e in ET.parse(path).getroot().find("entries").findall("entry"):
        g = e.find("greek")
        if g is None or not g.get("unicode"):
            continue
        out.setdefault(thayer_key(g.get("unicode")), []).append(
            (strongs_id(e.get("strongs"), "greek"), thayer_form(g.get("unicode"))))
    return out


def convert_thayer_entries(path, slug="thayer-entries", strongs_path=None,
                           page_slug="thayer"):
    """Thayer's (1889) one unit per ENTRY, inferred from the page OCR.

    The page book's docstring explains why neither line rule alone finds the
    entries: requiring a blank line before a Greek headword finds 4,532 (OCR
    drops blank lines), dropping the requirement finds 7,983 (it promotes Greek
    words that merely start a line). This converter adds the one fact both
    rules ignore: A LEXICON IS IN ALPHABETICAL ORDER.

      1. Body pages only: the run from the first page whose running head has
         Greek in it to the last. Preface, abbreviations and the English-index
         appendix are outside that run and contribute no entries.
      2. Candidates: every line that opens with a Greek word and a comma or
         full stop -- the LOOSE rule, so an entry whose blank line OCR lost is
         still a candidate.
      3. Weight each: 1, +1 if paragraph-initial (the strict rule), +1 if the
         word is a Strong's Greek lemma (accents ignored).
      4. Keep the max-weight strictly-increasing chain under thayer_key.
         Mid-entry Greek is mostly out of order with its neighbours, so the
         chain drops it; a real headword that OCR garbled at its first letter
         falls out too, and its text joins the entry before it (counted).
      5. A chain member must ALSO be paragraph-initial or a Strong's lemma.
         A bare line-initial Greek word that merely happens to sort in order
         is not evidence of an entry.
      6. Two exceptions. A ONE-LETTER headword (ὁ the article, ἤ, ὦ) is a
         candidate only with a paragraph break AND a Strong's match, since a
         lone letter is usually a numeral. And two headwords that differ ONLY
         by accent (εἰμί / εἶμι) may share a key on the chain when both open
         a paragraph and match a Strong's lemma accent for accent.

    The result is a heuristic and says so: the count is reported against the
    ~5,600 entries Thayer's really has, every unit links back to the exact
    page(s) it was cut from, and the page book is untouched.
    """
    pages = json.load(open(path, encoding="utf-8"))
    order = sorted(pages, key=int)
    parsed = {p: _thayer_page(pages[p]) for p in order}
    greek_head = [p for p in order if parsed[p][0] and RE_GREEK.search(parsed[p][0][0])]
    body = order[order.index(greek_head[0]):order.index(greek_head[-1]) + 1] if greek_head else []

    lemmas = strongs_greek_lemmas(strongs_path) if strongs_path else {}

    lines, cands = [], []                  # lines: (page, text); cands index into lines
    for p in body:
        prev_blank = True                  # a page/column top counts as a break
        for l in parsed[p][1]:
            s = l.strip()
            if not s:
                prev_blank = True
                continue
            m = RE_THAYER_HEAD.match(s)       # anywhere, not only after a blank line
            k = thayer_key(m.group(1)) if m else ""
            # One-letter headwords are real (ὁ the article, ἤ, ὦ) but a lone
            # Greek letter starting a line is usually a numeral or a siglum,
            # so one letter needs BOTH a paragraph break and a Strong's lemma.
            if k and (len(k) > 1 or (prev_blank and k in lemmas)):
                hw = m.group(1)
                f = thayer_form(hw)
                exact = any(f == lf for _, lf in lemmas.get(k, ()))
                cands.append({"line": len(lines), "page": p, "head": hw, "key": k,
                              "form": f, "para": prev_blank, "strongs": k in lemmas,
                              "homograph": prev_blank and exact})
            lines.append((p, s))
            prev_blank = False

    weights = [1 + c["para"] + c["strongs"] for c in cands]
    chain = _lis_weighted([c["key"] for c in cands], weights,
                          [c["form"] for c in cands], [c["homograph"] for c in cands])
    heads = [cands[i] for i in chain if cands[i]["para"] or cands[i]["strongs"]]
    stats = {"candidates": len(cands),
             "off_order": len(cands) - len(chain),
             "weak": len(chain) - len(heads),
             "paragraph_initial_candidates": sum(c["para"] for c in cands)}

    units, used_ids, strongs_linked, ambiguous = [], set(), 0, 0
    for n, h in enumerate(heads):
        stop = heads[n + 1]["line"] if n + 1 < len(heads) else len(lines)
        span = lines[h["line"]:stop]
        spanned = []
        for p, _ in span:
            if p not in spanned:
                spanned.append(p)
        pno = int(h["page"])
        base = f"{slug}:p.{pno}.{thayer_translit(h['head']) or 'x'}"
        unit_id, i = base, 2
        while unit_id in used_ids:
            unit_id, i = f"{base}-{i}", i + 1
        used_ids.add(unit_id)
        links = [{"kind": "page", "target": f"{page_slug}:p.{int(p)}"} for p in spanned]
        # Accents decide first (εἰμί G1510, not εἶμι); only when the OCR'd
        # accents match nothing do they get ignored.
        pairs = lemmas.get(h["key"], [])
        exact = [g for g, f in pairs if f == h["form"]]
        gs = exact or [g for g, _ in pairs]
        if len(gs) == 1:
            links.append({"kind": "strongs", "target": f"strongs-greek:{gs[0]}",
                          "match": "headword, accents matched" if exact
                                   else "headword, accents ignored"})
            strongs_linked += 1
        elif gs:
            ambiguous += 1
        units.append({"id": unit_id,
                      "ref": f"Thayer p. {pno}, s.v. {h['head']}",
                      "text": clean(" ".join(t for _, t in span)),
                      "links": links,
                      "lex": {"headword": h["head"],
                              "pages": [int(p) for p in spanned],
                              "evidence": [w for w, on in (("paragraph-initial", h["para"]),
                                                           ("strongs-lemma", h["strongs"]),
                                                           ("alphabetical-order", True)) if on],
                              **({"strongs_candidates": gs} if len(gs) > 1 else {}),
                              "greek_chars": len(RE_GREEK.findall(" ".join(t for _, t in span)))}})
    target = 5600
    src = {"path": os.path.relpath(path, CORPUS), "format": "lexicon-ocr", "sha256": sha256(path)}
    if strongs_path:
        src["strongs_sha256"] = sha256(strongs_path)
    return {"slug": slug,
            "title": "A Greek-English Lexicon of the New Testament (Thayer), by entry",
            "author": "C. L. W. Grimm & C. G. Wilke, tr./rev./enl. Joseph Henry Thayer (1889)",
            "source": src,
            "scheme": {"citation": "page of the 1889 edition + headword (s.v.)",
                       "resolution": "entry",
                       "honesty": "entries INFERRED from OCR; not proofread; "
                                  "ids provisional until segmentation is ruled on",
                       "segmentation": stats,
                       "note": f"{len(units):,} entries inferred from the page OCR of "
                               f"{len(body)} body pages, against the ~{target:,} Thayer's "
                               f"really has. Rule: line-initial Greek headword, kept only "
                               f"on the max-weight alphabetical chain and only if "
                               f"paragraph-initial or a Strong's lemma (see "
                               f"convert_thayer_entries). {stats['off_order']:,} candidates "
                               f"dropped as out of alphabetical order, {stats['weak']:,} "
                               f"in order but with no other evidence. A real entry the "
                               f"rule missed is not lost: its text is inside the entry "
                               f"before it. Every unit links to the page(s) of the page "
                               f"book `{page_slug}` it was cut from, which is the "
                               f"checkable citation. "
                               + (f"{strongs_linked:,} entries linked to strongs-greek by "
                                  f"headword (accents ignored); {ambiguous:,} matched more "
                                  f"than one Strong's lemma and are left unlinked with the "
                                  f"candidates under lex.strongs_candidates."
                                  if strongs_path else
                                  "Built WITHOUT Strong's Greek (not fetched): the lemma "
                                  "evidence and strongs links are absent from this build.")},
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
    # Thayer's by entry: the same OCR as the page book, cut into entries. It
    # uses Strong's Greek as evidence when that file is fetched (it is a plain
    # GitHub fetch, so it normally is); without it the build still runs and
    # its note says the lemma evidence is absent.
    th = os.path.join(CORPUS, "lexicons", "thayer-pages.json")
    sg = os.path.join(CORPUS, "lexicons", "strongs-greek.xml")
    if os.path.exists(th):
        jobs.append(("thayer-entries", lambda: convert_thayer_entries(
            th, strongs_path=sg if os.path.exists(sg) else None)))
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
            if slug in TEI_DRAMA:
                jobs.append((slug, lambda p=path, s=slug: convert_tei_drama(p, s, TEI_DRAMA[s])))
                continue
            if slug in TEI_PROSE:
                jobs.append((slug, lambda p=path, s=slug: convert_tei_prose(p, s, TEI_PROSE[s])))
                continue
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
                              "units": len(book["units"]), "scheme": book["scheme"],
                              **({"rights": book["rights"]} if book.get("rights") else {})}
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
                          "scheme": book["scheme"],
                          **({"rights": book["rights"]} if book.get("rights") else {})}
        print(f"{slug}: {len(book['units'])} units — {book['title']}")
    with open(os.path.join(BOOKS, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, ensure_ascii=False)
    print(f"MANIFEST: {len(manifest)} books")

if __name__ == "__main__":
    main()
