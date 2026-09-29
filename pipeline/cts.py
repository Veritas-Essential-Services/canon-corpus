#!/usr/bin/env python3
"""cts.py -- read any Perseus (CapiTainS) TEI file by the citation scheme it
declares about itself.

Every file in PerseusDL/canonical-greekLit and canonical-latinLit carries a
<refsDecl n="CTS"> whose <cRefPattern>s say, as XPath, where each citation
level lives: Caesar's Gallic War is book/chapter/section
(`tei:div[@n='$1']/tei:div[@n='$2']/tei:div[@n='$3']`), Ovid's Metamorphoses
is book/line (`tei:div[@n='$1']/tei:l[@n='$2']`). structure_texts.convert_tei
knows only the two shapes the first three Perseus books had (book>card,
book>line); this module follows the file's own declaration instead, so one
converter covers the collection. Measured 2026-09-29: 2,049 of 2,097
editions/translations declare a scheme (18 are malformed XML, 23 declare
none, 7 are catalogued under a filename Perseus does not ship).

    walk(path)                 -> (scheme, [(ref_tuple, text)])
    convert_cts(path, slug)    -> a book in the {id, ref, text, links[]} shape

The unit is the file's DEEPEST citation level, exactly as declared -- a
section of Caesar, a line of Ovid, a Stephanus section of Plato. That is the
honest resolution: `scheme.honesty` says "exact" because the id IS the
edition's own citation. Whether verse should be shelved as single lines or
blocks is a shelving decision for the caller, not something this module
decides (convert_tei's 20-line blocks are unchanged).

Ids are `<slug>:<citation>`, the citation being the CTS passage reference
(`1.1.1`, `327a`). The manifest records the edition's CTS URN, so an id stays
short and the URN stays exact (CLAUDE.md rule 3). Perseus's XML is CC BY-SA
4.0; the rights block says so, and anything built on it inherits it.

Pure standard library; no network."""
import hashlib, os, re, xml.etree.ElementTree as ET

T = "{http://www.tei-c.org/ns/1.0}"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
RE_XPATH = re.compile(r"#xpath\((.*)\)\s*$", re.S)
RE_STEP = re.compile(r"(/{1,2})([\w:.*-]+)(\[[^\]]*\])?")
RE_PRED = re.compile(r"@([\w:]+)\s*=\s*['\"]([^'\"]*)['\"]")
SKIP = {T + "note", T + "bibl"}  # editorial apparatus, not the text


def _tag(step):
    return T + step.split(":", 1)[1] if step.startswith("tei:") else step


def scheme_of(root):
    """[(level_name, xpath)] from shallowest to deepest, or None."""
    decl = next((d for d in root.iter(T + "refsDecl") if d.get("n") == "CTS"), None)
    if decl is None:
        return None
    pats = []
    for p in decl.iter(T + "cRefPattern"):
        m = RE_XPATH.search(p.get("replacementPattern") or "")
        if m:
            pats.append((p.get("n") or "?", m.group(1)))
    if not pats:
        return None
    return sorted(pats, key=lambda p: p[1].count("$"))


def _steps(xpath):
    """'/tei:TEI/tei:text/.../tei:l[@n='$2']' -> [(axis, tag, literals, captures)]"""
    out = []
    for axis, name, pred in RE_STEP.findall(xpath):
        literals, capture = {}, False
        for attr, val in RE_PRED.findall(pred or ""):
            if val.startswith("$"):
                capture = True  # this step records the element's @n
            else:
                literals[attr] = val
        out.append((axis, _tag(name), literals, capture))
    return out


def _text(el):
    """The element's text, notes and bibliographic apparatus left out."""
    parts = []
    def rec(e):
        if e.tag in SKIP:
            return
        if e.text:
            parts.append(e.text)
        for c in e:
            rec(c)
            if c.tail:
                parts.append(c.tail)
    rec(el)
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def walk(path):
    """Follow the deepest declared pattern. Returns (scheme, leaves), where
    scheme is the level names shallow->deep and leaves is [(refs, text)] in
    document order. Raises ValueError when the file declares no scheme."""
    root = ET.parse(path).getroot()
    pats = scheme_of(root)
    if pats is None:
        raise ValueError("no CTS refsDecl")
    doc = ET.Element("doc")
    doc.append(root)
    nodes = [(doc, ())]
    for axis, tag, literals, capture in _steps(pats[-1][1]):
        nxt = []
        for el, refs in nodes:
            cands = list(el) if axis == "/" else [d for d in el.iter() if d is not el]
            for c in cands:
                if tag != "*" and c.tag != tag:
                    continue
                if any(c.get(a) != v for a, v in literals.items()):
                    continue
                if capture:
                    n = c.get("n")
                    if n is None:
                        continue
                    nxt.append((c, refs + (n.strip(),)))
                else:
                    nxt.append((c, refs))
        nodes = nxt
    return [name for name, _ in pats], [(refs, _text(el)) for el, refs in nodes]


def meta(path):
    root = ET.parse(path).getroot()
    body_div = next((d for d in root.iter(T + "div") if d.get("type") in ("edition", "translation")), None)
    def first(xp):
        e = root.find(xp)
        return re.sub(r"\s+", " ", "".join(e.itertext())).strip() if e is not None else ""
    return {"title": first(f".//{T}titleStmt/{T}title"),
            "author": first(f".//{T}titleStmt/{T}author"),
            "translator": first(f".//{T}titleStmt/{T}editor[@role='translator']"),
            "urn": (body_div.get("n") or "") if body_div is not None else "",
            "lang": (body_div.get(XML_LANG) if body_div is not None else None) or root.get(XML_LANG) or ""}


def imprint_years(path):
    """Every year printed in the source description's <date>s. EVIDENCE for a
    rights reading, never a verdict: Perseus records modern reprints and
    digitisations here too (Brenton's 1851 Septuagint reads 2000)."""
    root = ET.parse(path).getroot()
    sd = root.find(f".//{T}sourceDesc")
    if sd is None:
        return []
    txt = " ".join((d.get("when") or "") + " " + "".join(d.itertext()) for d in sd.iter(T + "date"))
    return sorted({int(y) for y in re.findall(r"\b(1[4-9]\d\d|20[0-2]\d)\b", txt)})


def convert_cts(path, slug, urn=None):
    """A book in the shape every converter emits. Duplicate citations (a file
    that numbers two passages alike) keep the first id and suffix the rest
    with `~2`, `~3`, and the scheme says how many; nothing is dropped. `urn`
    overrides the header's, which many Latin files leave off their edition div."""
    scheme, leaves = walk(path)
    m = meta(path)
    if urn:
        m["urn"] = urn
    units, seen, dups = [], {}, 0
    for refs, text in leaves:
        if not text:
            continue
        cite = ".".join(refs)
        seen[cite] = seen.get(cite, 0) + 1
        uid = f"{slug}:{cite}" if seen[cite] == 1 else f"{slug}:{cite}~{seen[cite]}"
        dups += seen[cite] > 1
        units.append({"id": uid, "ref": f"{m['title']} {cite}", "text": text, "links": []})
    with open(path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    honesty = "exact: the id is the edition's own CTS citation"
    if dups:
        honesty += f"; {dups} citation(s) repeat in the source and carry a ~n suffix"
    corpus = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "corpus"))
    rel = os.path.relpath(os.path.abspath(path), corpus)
    return {"slug": slug, "title": m["title"], "author": m["author"],
            "source": {"path": path if rel.startswith("..") else rel.replace(os.sep, "/"),
                       "format": "cts-tei", "urn": m["urn"],
                       "translator": m["translator"], "sha256": digest},
            "scheme": {"citation": ".".join(scheme), "resolution": scheme[-1], "honesty": honesty},
            "rights": {"license": "CC BY-SA 4.0 (Perseus Digital Library markup)",
                       "attribution": "Perseus Digital Library, Tufts University",
                       "source_url": "https://github.com/PerseusDL",
                       "share_alike": True},
            "units": units}
