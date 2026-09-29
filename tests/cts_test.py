#!/usr/bin/env python3
"""Offline checks for pipeline/cts.py, the Perseus (CapiTainS) reader, and
pipeline/perseus_survey.py. Fixtures inline; no network, no corpus needed.
With the Perseus repos fetched (perseus_catalog.py --fetch), also checks
real editions and that the committed survey regenerates byte-for-byte.

    python3 tests/cts_test.py"""
import json, os, subprocess, sys, tempfile, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(HERE, "..", "pipeline")
sys.path.insert(0, PIPE)

def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(PIPE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

cts = load("cts")

PASS = 0
FAIL = []
def check(label, cond):
    global PASS
    if cond: PASS += 1
    else: FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label)

def skip(label):
    print("skip " + label)

HEAD = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc>
<titleStmt><title>{title}</title><author>Auctor</author>{tr}</titleStmt>
<sourceDesc><biblStruct><monogr><imprint><date>{year}</date></imprint></monogr></biblStruct></sourceDesc>
</fileDesc><encodingDesc><refsDecl n="CTS">{pats}</refsDecl></encodingDesc></teiHeader>
<text><body>{body}</body></text></TEI>"""

def pat(name, xp):
    return f'<cRefPattern n="{name}" replacementPattern="#xpath({xp})"/>'

E = "/tei:TEI/tei:text/tei:body/tei:div"

# Prose, three levels, declared DEEPEST FIRST as Perseus does; a note inside
# a section; a <head> at book level; a second book.
PROSE = HEAD.format(title="Bellum", tr="", year="1914", pats=(
    pat("section", E + "/tei:div[@n='$1']/tei:div[@n='$2']/tei:div[@n='$3']")
    + pat("chapter", E + "/tei:div[@n='$1']/tei:div[@n='$2']")
    + pat("book", E + "/tei:div[@n='$1']")), body="""
<div type="edition" n="urn:cts:latinLit:x.y.z-lat1">
 <div type="textpart" subtype="book" n="1"><head>LIBER I</head>
  <div type="textpart" subtype="chapter" n="1">
   <div type="textpart" subtype="section" n="1"><p>Gallia est <note>editor: sic</note>omnis divisa.</p></div>
   <div type="textpart" subtype="section" n="2"><p>Hi omnes   lingua differunt.</p></div>
  </div></div>
 <div type="textpart" subtype="book" n="2">
  <div type="textpart" subtype="chapter" n="1">
   <div type="textpart" subtype="section" n="1"><p>Secundus liber.</p></div>
  </div></div>
</div>""")

# Verse, book.line; a duplicate line number; an empty line; a line without @n.
VERSE = HEAD.format(title="Carmen", tr="<editor role=\"translator\">T. Anglicus</editor>", year="1892", pats=(
    pat("line", E + "/tei:div[@n='$1']/tei:l[@n='$2']")
    + pat("book", E + "/tei:div[@n='$1']")), body="""
<div type="translation">
 <div type="textpart" subtype="book" n="1">
  <milestone unit="card" n="1"/>
  <l n="1">In nova fert animus</l><l n="2">corpora; di, coeptis</l>
  <l n="2">a second line two</l><l n="3"> </l><l>unnumbered</l>
 </div>
</div>""")

# Drama: lines inside speeches, reached by the descendant axis.
DRAMA = HEAD.format(title="Fabula", tr="", year="1935", pats=pat("line", E + "//tei:l[@n='$1']"), body="""
<div type="edition"><sp><speaker>A.</speaker><l n="1">prima</l></sp><sp><l n="2">secunda</l></sp></div>""")

NOSCHEME = """<?xml version="1.0"?><TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><div type="edition"><p>x</p></div></body></text></TEI>"""

tmp = tempfile.mkdtemp()
def write(name, s):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)
    return p

prose, verse, drama, nos = (write(n, s) for n, s in (("p.xml", PROSE), ("v.xml", VERSE), ("d.xml", DRAMA), ("n.xml", NOSCHEME)))

# --- scheme and walk
scheme, leaves = cts.walk(prose)
check("scheme is read shallow -> deep from a deepest-first refsDecl", scheme == ["book", "chapter", "section"])
check("prose: one leaf per deepest citation, in document order",
      [r for r, _ in leaves] == [("1", "1", "1"), ("1", "1", "2"), ("2", "1", "1")])
check("a <note> is left out of the text, its tail kept", leaves[0][1] == "Gallia est omnis divisa.")
check("whitespace is collapsed", leaves[1][1] == "Hi omnes lingua differunt.")
check("a book-level <head> is not a unit and not in any leaf", all("LIBER" not in t for _, t in leaves))

scheme, leaves = cts.walk(verse)
check("verse: book.line", scheme == ["book", "line"])
check("verse: an <l> without @n is not a citable leaf", all(r[-1] for r, _ in leaves) and len(leaves) == 4)
check("the translation div is followed like an edition div", leaves[0][1] == "In nova fert animus")

scheme, leaves = cts.walk(drama)
check("the descendant axis (//) finds lines inside speeches", [r for r, _ in leaves] == [("1",), ("2",)])
check("a speaker label is not part of a line", leaves[0][1] == "prima")

try:
    cts.walk(nos); check("a file with no CTS refsDecl raises ValueError", False)
except ValueError:
    check("a file with no CTS refsDecl raises ValueError", True)

# --- convert_cts: the shape every converter emits
b = cts.convert_cts(prose, "bellum", urn="urn:cts:latinLit:x.y.z-lat1")
check("ids are <slug>:<citation>", [u["id"] for u in b["units"]] == ["bellum:1.1.1", "bellum:1.1.2", "bellum:2.1.1"])
check("every unit has id, ref, text, links[]", all(set(u) == {"id", "ref", "text", "links"} for u in b["units"]))
check("the manifest-bound fields: urn, sha256, citation, resolution",
      b["source"]["urn"].endswith("x.y.z-lat1") and len(b["source"]["sha256"]) == 64
      and b["scheme"]["citation"] == "book.chapter.section" and b["scheme"]["resolution"] == "section")
check("honesty says exact when no citation repeats", b["scheme"]["honesty"].startswith("exact") and "repeat" not in b["scheme"]["honesty"])
check("the rights block names CC BY-SA and share-alike",
      b["rights"]["license"].startswith("CC BY-SA 4.0") and b["rights"]["share_alike"] is True)

v = cts.convert_cts(verse, "carmen")
ids = [u["id"] for u in v["units"]]
check("a repeated citation is kept with a ~2 suffix, never dropped", ids == ["carmen:1.1", "carmen:1.2", "carmen:1.2~2"])
check("an empty leaf is not a unit", len(v["units"]) == 3)
check("honesty counts the repeats", "1 citation(s) repeat" in v["scheme"]["honesty"])
check("the translator is read from the header", v["source"]["translator"] == "T. Anglicus")
check("the header urn is used when none is given", cts.convert_cts(prose, "b")["source"]["urn"] == "urn:cts:latinLit:x.y.z-lat1")

# --- rights evidence
check("imprint years are read from sourceDesc dates", cts.imprint_years(prose) == [1914])
ps = load("perseus_survey")
check("rights prompt: 1930 or earlier", ps.rights_prompt([1892, 1914]) == "imprint <= 1930")
check("rights prompt: any later printing asks for a reading", ps.rights_prompt([1914, 1935]) == "imprint 1931+: read")
check("rights prompt: no date", ps.rights_prompt([]) == "no imprint date")

# --- against the real collection, when it is here
PERSEUS = os.path.join(HERE, "..", "data", "corpus", "perseus-repos")
real = os.path.join(PERSEUS, "canonical-latinLit", "data", "phi0448", "phi001", "phi0448.phi001.perseus-lat2.xml")
if os.path.exists(real):
    c = cts.convert_cts(real, "caesar-bg")
    check("Caesar BG (lat2): book.chapter.section, first unit is Gallia est omnis divisa",
          c["scheme"]["citation"] == "book.chapter.section" and c["units"][0]["id"] == "caesar-bg:1.1.1"
          and c["units"][0]["text"].startswith("Gallia est omnis divisa in partes tres"))
    check("Caesar BG (lat2): 2,150 sections, none repeated", len(c["units"]) == 2150 and "repeat" not in c["scheme"]["honesty"])
    ov = os.path.join(PERSEUS, "canonical-latinLit", "data", "phi0959", "phi006", "phi0959.phi006.perseus-lat2.xml")
    o = cts.convert_cts(ov, "ovid-met")
    check("Ovid Met. (lat2): book.line, ends at 15.879 vivam", o["units"][-1]["id"] == "ovid-met:15.879"
          and o["units"][-1]["text"].endswith("vivam."))
    if os.path.exists(os.path.join(HERE, "..", "data", "perseus", "survey.jsonl")):
        r = subprocess.run([sys.executable, os.path.join(PIPE, "perseus_survey.py"), "--check"],
                           capture_output=True, text=True)
        check("perseus_survey.py --check: the committed survey is what the pinned repos give",
              r.returncode == 0 and "CHECK PASSED" in r.stdout)
    rows = [json.loads(l) for l in open(os.path.join(HERE, "..", "data", "perseus", "survey.jsonl"), encoding="utf-8")]
    check("the survey stores no text, only facts", all("text" not in r for r in rows))
else:
    skip("the Perseus repos are not fetched (python3 pipeline/perseus_catalog.py --fetch)")

print(f"\n{PASS} passed, {len(FAIL)} failed")
for f in FAIL:
    print("  FAIL", f)
sys.exit(1 if FAIL else 0)
