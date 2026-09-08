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
Scene V.

Dramatis Personæ

MACBETH, a general

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

# ---------------------------------------------------------------- Lexicons
# Every case below is a real defect measured against the live sources on
# 2026-09-06 while building these converters, frozen so it cannot recur.

check("strongs_id: leading zeros are formatting, not the number",
      (st.strongs_id("0175", "hebrew"), st.strongs_id("175", "hebrew"),
       st.strongs_id("H175", "hebrew"), st.strongs_id("00002", "greek"))
      == ("H175", "H175", "H175", "G2"))

SH_FIX = """<?xml version="1.0" encoding="utf-8"?>
<lexicon xmlns="http://openscriptures.github.com/morphhb/namespace">
 <entry id="H2"><w pos="n-m" pron="ab" xlit="ab" xml:lang="arc">אַב</w>
  <source>(Aramaic) corresponding to <w src="H1">1</w></source>
  <usage>father.</usage></entry>
</lexicon>"""
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(SH_FIX); sh_path = f.name
hb = st.convert_strongs_hebrew(sh_path)
u = hb["units"][0]
check("strongs-hebrew: unit id is the Strong's number", u["id"] == "strongs-hebrew:H2")
check("strongs-hebrew: lemma and translit reach the ref", "אַב" in u["ref"] and "(ab)" in u["ref"])
check("strongs-hebrew: <w src> is a cross-reference, headword <w> is not",
      [l["target"] for l in u["links"]] == ["strongs-hebrew:H1"])
os.unlink(sh_path)

SG_FIX = """<?xml version='1.0' encoding='utf-8'?>
<strongsdictionary><prologue>x</prologue><entries>
 <entry strongs="00026"><strongs>26</strongs>
  <greek BETA="A)GA/PH" unicode="ἀγάπη" translit="agape"/>
  <pronunciation strongs="ag-ah'-pay"/>
  <strongs_derivation>from <strongsref language="GREEK" strongs="0025"/>;</strongs_derivation>
  <strongs_def> love</strongs_def><kjv_def>:--love.</kjv_def>
  <see language="GREEK" strongs="5689"/></entry>
 <entry strongs="02717"><strongs>2717</strongs>  Not Used
 </entry>
</entries></strongsdictionary>"""
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(SG_FIX); sg_path = f.name
gk = st.convert_strongs_greek(sg_path)
g26 = gk["units"][0]
check("strongs-greek: derivation keeps the number it points at (not 'from ;')",
      g26["text"].startswith("from G25"))
check("strongs-greek: a ref above G5624 is a parsing code, not a cross-reference",
      [l["target"] for l in g26["links"]] == ["strongs-greek:G25"])
check("strongs-greek: Strong's own 'Not Used' numbers are kept and flagged",
      gk["units"][1]["text"] == "Not Used" and gk["units"][1]["lex"]["not_used"] is True)
os.unlink(sg_path)

BDB_FIX = ("BDBid\tStrongNumber\tcontent\n"
           "BDB6\tH6_H8\t"
           '<h1><entry>BDB6</entry></h1><div class="navigation">BDB5 | BIBLICAL HEBREW | BDB7</div>'
           '<p><bdbheb>אַב</bdbheb> noun '
           '<ref ref="Gen 24:12" b="1" cBegin="24" vBegin="12">Gen 24:12</ref></p>\n'
           "BDB7\t\t<h1>x</h1><p>no strongs equivalent</p>\n")
with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8") as f:
    f.write(BDB_FIX); bdb_path = f.name
bd = st.convert_bdb(bdb_path)
b6 = bd["units"][0]
check("bdb: one entry can carry several Strong's numbers (H6_H8 -> two links)",
      [l["target"] for l in b6["links"] if l["kind"] == "strongs"]
      == ["strongs-hebrew:H6", "strongs-hebrew:H8"])
check("bdb: header and prev|next navigation are furniture, stripped",
      "BIBLICAL HEBREW" not in b6["text"] and b6["text"].startswith("אַב"))
scr = [l for l in b6["links"] if l["kind"] == "scripture"]
check("bdb: scripture ref keeps the book number's OSIS and stays UNresolved",
      scr and scr[0]["osis"] == "Gen.24.12" and scr[0]["resolved"] is False
      and scr[0]["versification"] == "bhs")
check("bdb: an entry with no Strong's number gets no strongs link",
      [l for l in bd["units"][1]["links"] if l["kind"] == "strongs"] == [])
os.unlink(bdb_path)

# ---------------------------------------------------------------- Thayer (OCR)
import json as _json
THAYER_FIX = {"300": "\u1F21\u03B3\u03AD\u03BF\u03BC\u03B1\u03B9\n"
                     "rator of Judaea to the governor of Syria.\n"
                     "300\n"
                     "\n"
                     "\u1F21\u03B4\u03BF\u03BD\u03AE, -\u1FC6\u03C2, \u1F21, pleasure, Lk. viii. 14.\n"
                     "not a headword line, mid-entry \u03C3\u1FF6\u03C2, though it looks like one\n"}
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    _json.dump(THAYER_FIX, f); th_path = f.name
tb = st.convert_thayer(th_path)
tu = tb["units"][0]
check("thayer: unit is the printed page, not a guessed entry",
      tu["id"] == "thayer:p.300" and tb["scheme"]["resolution"] == "page")
check("thayer: running head and bare page number are furniture, stripped",
      "\u1F21\u03B3\u03AD\u03BF\u03BC\u03B1\u03B9" not in tu["text"] and "300" not in tu["text"]
      and tu["lex"]["running_head"] == "\u1F21\u03B3\u03AD\u03BF\u03BC\u03B1\u03B9")
check("thayer: headword detected only paragraph-initially (mid-entry Greek is not one)",
      tu["lex"]["headwords"] == ["\u1F21\u03B4\u03BF\u03BD\u03AE"])
check("thayer: honesty says entries are NOT segmented",
      "NOT segmented" in tb["scheme"]["honesty"])
os.unlink(th_path)

# ------------------------------------------------------------ STEPBible Greek
# Every case is a defect measured against the live files on 2026-09-06. Two of
# them silently LOSE TEXT, which is why they are frozen here.
STEP_FIX = (
    "header line, ignored\n"
    # same Strong's number, two different words -- keying on col0 drops one
    "G0001\tG0001G =\tG0001G\t\u03B1, \u1F08\u03BB\u03C6\u03B1\tAlpha\tG:N-LI\tAlpha\t"
    '<b>\u1F04\u03BB\u03C6\u03B1</b>, <a href="x" title="quoted \u03C3\u03C5\u03BB\u03BB\u03B1\u03B2\u1F74\u03BD">Refs</a>\n'
    "G0001\tG0001H =\tG0001H\t\u1F86\ta\tG:INJ\tah!\t<b>\u1F14\u1FB1</b>, interjection\n"
    # col2 is a TARGET, not a key -- keying on it merges these two entries
    "G0623\tG0623 = a Name of\tG0003\t\u1F08\u03C0\u03BF\u03BB\u03BB\u03CD\u03C9\u03BD\tApolluon\tN:N--T\tApollyon\t<b>x</b>\n"
    # compound target: 'G0473 (G0473+G3739)' is a key plus its parts
    "G0503\tG0503 = a Combination of\tG0473 (G0473+G3739)\t\u1F00\u03BD\u03C4\u03AF\tanti\tG:P\tover against\t<b>y</b>\n")
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write(STEP_FIX); step_path = f.name
sb = st.convert_stepbible_greek([step_path], "lsj-greek", "T", "A", "n.")
byid = {u["id"]: u for u in sb["units"]}
check("stepbible: keyed on the EXTENDED number, so one Strong's number can hold two words",
      "lsj-greek:G0001G" in byid and "lsj-greek:G0001H" in byid
      and byid["lsj-greek:G0001G"]["text"] != byid["lsj-greek:G0001H"]["text"])
check("stepbible: column 2 is a cross-reference TARGET, not the entry key",
      "lsj-greek:G0623" in byid
      and [l["target"] for l in byid["lsj-greek:G0623"]["links"]] == ["lsj-greek:G0003"])
check("stepbible: a compound target yields the key AND its parts, no dangling string",
      {l["target"] for l in byid["lsj-greek:G0503"]["links"]}
      == {"lsj-greek:G0473", "lsj-greek:G3739"})
check("stepbible: Greek quoted inside title= attributes survives tag-stripping",
      "\u03C3\u03C5\u03BB\u03BB\u03B1\u03B2\u1F74\u03BD" in byid["lsj-greek:G0001G"]["text"])
check("stepbible: non-PD source carries a rights block that names the limit",
      sb["rights"]["redistribute_whole"] is False
      and sb["rights"]["license"] == "CC BY 4.0"
      and sb["rights"]["attribution"] and sb["rights"]["source_url"])
os.unlink(step_path)

print(f"\n{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
