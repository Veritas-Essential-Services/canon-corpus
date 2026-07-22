#!/usr/bin/env python3
"""Offline test suite for the structure layer (canon-corpus). No network,
no corpus needed — fixtures inline. Run:  python3 tests/structure_test.py

Split from patrimonium's tests/armarium_test.py at the 2026-07-22
extraction: the converter checks live here; the engine checks live in the
armarium repo's tests/armarium_test.py. 18 checks."""
import os, sys, tempfile, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(HERE, "..", "pipeline")

def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(PIPE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

st = load("structure_texts")

PASS = 0
FAIL = []
def check(label, cond):
    global PASS
    if cond: PASS += 1
    else: FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label)

# ---------------------------------------------------------------- KJV fixture
KJV_FIX = """The Gospel According to Saint John
The Epistle of Paul the Apostle to the Romans

*** START ***

The Gospel According to Saint John


1:1 In the beginning was the Word, and the Word was with God, and the
Word was God. 1:2 The same was in the beginning with God.

The Epistle of Paul the Apostle to the Romans

Otherwise Called:

The Gospel According to Saint John


1:1 Paul, a servant of Jesus Christ, called to be an apostle,
separated unto the gospel of God, 1:2 (Which he had promised afore by
his prophets in the holy scriptures,)
"""
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write(KJV_FIX); kjv_path = f.name
book = st.convert_kjv(kjv_path)
d = {u["id"]: u for u in book["units"]}
check("kjv: 4 verses parsed", len(book["units"]) == 4)
check("kjv: John 1:1 text", d.get("kjv:John.1.1", {}).get("text", "").startswith("In the beginning was the Word"))
check("kjv: inline marker split (John 1:2)", "kjv:John.1.2" in d)
check("kjv: alias header ignored (no dupe John)", d.get("kjv:Rom.1.1", {}).get("text", "").startswith("Paul, a servant"))
check("kjv: no duplicate ids", len(d) == len(book["units"]))
os.unlink(kjv_path)

# ---------------------------------------------------------------- ThML fixture
THML_FIX = """<?xml version="1.0"?><ThML><ThML.head>
<generalInfo><title>Test Treatise</title></generalInfo>
<printSourceInfo><DC.Creator sub="Author" scheme="file-as">Owen, John</DC.Creator></printSourceInfo>
</ThML.head><ThML.body>
<div1 id="i" title="Chapter I." shorttitle="Chapter I" type="Chapter">
<p>This paragraph is long enough to count as a unit because it exceeds the
minimum length and cites <scripRef passage="Rom. viii. 13" osisRef="Bible:Rom.8.13">Rom. viii. 13</scripRef> within it.</p>
<p>short</p>
<p>A second real paragraph, also comfortably beyond the minimum length used
by the converter, citing <scripRef passage="1 John iv. 8" parsed="kjv|1John|4|8|0|0" osisRef="Bible.kjv:1John.4.8">1 John iv. 8</scripRef> in the Communion style.</p>
</div1></ThML.body></ThML>"""
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(THML_FIX); thml_path = f.name
tb = st.convert_thml(thml_path, "test-treatise")
check("thml: 2 units (short filtered)", len(tb["units"]) == 2)
check("thml: keylink extracted", tb["units"][0]["links"] == ["Rom.8.13"])
check("thml: Bible.kjv osisRef variant", tb["units"][1]["links"] == ["1John.4.8"])
check("thml: author from DC.Creator", "Owen" in tb["author"])
os.unlink(thml_path)

# ---------------------------------------------------------------- TEI fixture
TEI_FIX = """<?xml version="1.0"?><TEI xmlns="http://www.tei-c.org/ns/1.0">
<teiHeader><fileDesc><titleStmt><title>Test Epic</title><author>Homer</author>
<editor role="translator">S. Butler</editor></titleStmt></fileDesc></teiHeader>
<text><body><div type="translation">
<div type="textpart" n="1" subtype="book">
<div type="textpart" n="1" subtype="card"><p>Sing, O goddess, the anger of Achilles.</p></div>
<div type="textpart" n="43" subtype="card"><p>And the son of Peleus answered him.</p></div>
</div></div></body></text></TEI>"""
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(TEI_FIX); tei_path = f.name
eb = st.convert_tei(tei_path, "test-epic", "Ep.")
check("tei: 2 card units", len(eb["units"]) == 2)
check("tei: card ref carries line anchor", eb["units"][1]["ref"] == "Ep. 1.43")
check("tei: translator recorded", eb["source"]["translator"] == "S. Butler")
os.unlink(tei_path)

# ---------------------------------------------------------------- Gutenberg verse
PL_FIX = """*** START OF THE PROJECT GUTENBERG EBOOK TEST ***

               BOOK I

               BOOK II

BOOK I

Of Mans First Disobedience, and the Fruit
Of that Forbidden Tree, whose mortal tast
Brought Death into the World, and all our woe.

BOOK II

High on a Throne of Royal State, which far
Outshon the wealth of Ormus and of Ind.
*** END OF THE PROJECT GUTENBERG EBOOK TEST ***"""
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write(PL_FIX); pl_path = f.name
vb = st.convert_gutenberg_verse(pl_path, "pl", "Paradise Lost", "Milton", "PL", r"^BOOK\s+([IVXLC]+)")
refs = [u["ref"] for u in vb["units"]]
check("gutenberg-verse: contents list collapses (2 books only)",
      sorted(set(u["ref"].split(".")[0] for u in vb["units"])) == ["PL I", "PL II"])
check("gutenberg-verse: first line ref", vb["units"][0]["ref"] == "PL I.1")
check("gutenberg-verse: text captured", "Disobedience" in vb["units"][0]["text"])
os.unlink(pl_path)

# ---------------------------------------------------------------- Shakespeare
SHK_FIX = """*** START OF THE PROJECT GUTENBERG EBOOK TEST ***
THE TRAGEDY OF MACBETH

Contents

ACT I
Scene I.

ACT V
SCENE V.

MACBETH.
Tomorrow, and tomorrow, and tomorrow,
It is a tale told by an idiot, full of sound and fury.
*** END OF THE PROJECT GUTENBERG EBOOK TEST ***"""
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write(SHK_FIX); shk_path = f.name
sb = st.convert_shakespeare(shk_path)
fury = [u for u in sb["units"] if "sound and fury" in u["text"]]
check("shakespeare: play detected (not ACT)", any("Macbeth" in u["ref"] for u in sb["units"]))
check("shakespeare: act/scene in ref", fury and "Act V" in fury[0]["ref"] and "Sc. V" in fury[0]["ref"])
check("shakespeare: 'ACT V' not treated as a play", not any(u["ref"].startswith("Act ") for u in sb["units"]))
os.unlink(shk_path)

print(f"\n{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
