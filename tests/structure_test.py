#!/usr/bin/env python3
# prov: 2026-07-22 claude-fable-5 drafted (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-06 claude-opus-5 edited (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-07 claude-opus-5 edited (from git trailer; backfilled 2026-09-30)
# fable_review: pending
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

# ------------------------------------------------- Perseus rights (all TEI)
_R_FIX = """<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt>
<title>Aeneid</title><author>Virgil</author><editor role="translator">T. C. Williams</editor>
</titleStmt></fileDesc></teiHeader><text><body xml:base="urn:cts:latinLit:phi0690.phi003.perseus-eng2">
<div type="textpart" subtype="book" n="1"><l n="1">Arms and the man I sing.</l></div></body></text></TEI>"""
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(_R_FIX); _r_path = f.name
_rb = st.convert_tei(_r_path, "aeneid-fixture", "Aen.")
check("perseus: the epic converter carries the share-alike rights block too, repo read from the urn",
      _rb["rights"]["license"] == "CC BY-SA 4.0"
      and _rb["rights"]["source_url"].endswith("canonical-latinLit")
      and "states no licence" in _rb["rights"]["note"])
os.unlink(_r_path)

# ---------------------------------------------------------- Perseus prose
PROSE_FIX = """<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt>
<title>The Histories</title><author>Herodotus</author><editor role="translator">A. D. Godley</editor>
</titleStmt></fileDesc></teiHeader><text><body><div type="translation">
<div type="textpart" subtype="Book" n="1"><head>Book One</head>
<div type="textpart" subtype="chapter" n="1">
<div type="textpart" subtype="section" n="pr"><p><milestone unit="para"/>Herodotus of
<name type="place" key="tgn,7016142"><reg>Bodrum [27.466,37.5] (inhabited place), Turkey</reg>
<placeName key="tgn,7016142">Halicarnassus</placeName></name> here sets forth.</p></div>
<div type="textpart" subtype="section" n="1"><p>The &lt;Pisidians&gt; came from the sea called
Red,<note resp="ed">Not the modern one.</note> and settled.
<quote><l><q>There is a love that makes men virtuous</q></l><l><q>And chaste</q></l></quote>
His ship and<gap reason="lost"/>his crew.</p></div>
</div></div></div></body></text></TEI>"""
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(PROSE_FIX); pr_path = f.name
pb = st.convert_tei_prose(pr_path, "hdt-fixture", "Hdt.")
pu = pb["units"]
check("prose: one unit per innermost division, id = the born-in book.chapter.section",
      [u["id"] for u in pu] == ["hdt-fixture:1.1.pr", "hdt-fixture:1.1.1"]
      and pb["scheme"]["citation"] == "Hdt. book.chapter.section")
check("prose: Perseus's gazetteer gloss is not text; the place is a TGN link",
      pu[0]["text"] == "Herodotus of Halicarnassus here sets forth."
      and pu[0]["links"] == [{"kind": "place", "target": "tgn:7016142", "name": "Halicarnassus"}])
check("prose: an editor's literal <angle brackets> are words, not a tag to strip",
      pu[1]["text"].startswith("The <Pisidians> came"))
check("prose: two verse lines the TEI runs together are never welded into one word",
      "virtuous And chaste" in pu[1]["text"])
check("prose: a lacuna separates words and is flagged, never filled",
      "and his crew." in pu[1]["text"] and pu[1]["apparatus"]["gap"] is True)
check("prose: footnote lifted out; a heading between divisions rides on the next unit",
      pu[1]["apparatus"]["notes"] == [{"by": "ed", "text": "Not the modern one."}]
      and pu[0]["apparatus"]["head"] == ["Book One"] and "Not the modern" not in pu[1]["text"])
_SPAN = PROSE_FIX.replace('n="pr"', 'n="1"').replace('subtype="section" n="1"><p>The', 'subtype="section" n="9"><p>The')
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(_SPAN); _sp_path = f.name
_sb = st.convert_tei_prose(_sp_path, "span-fixture", "Joseph. AJ")
check("prose: divisions numbered by their first section (1, 9) are SPANS, and honesty says so",
      _sb["scheme"]["resolution"] == "section (span)" and "contains it" in _sb["scheme"]["honesty"]
      and pb["scheme"]["resolution"] == "section")
os.unlink(_sp_path)
check("prose: every prose slug in the fetch manifest has an abbreviation, and back",
      set(st.TEI_PROSE) <= (set(load("fetch_sources").PERSEUS) | set(load("fetch_sources").FIRST1K)
                            | set(load("fetch_sources").CSEL))
      and set(load("fetch_sources").FIRST1K) <= set(st.TEI_PROSE) | set(st.CATENA)
      and set(load("fetch_sources").CSEL) <= set(st.TEI_PROSE))
os.unlink(pr_path)

# ---------------------------------------------------------- Perseus drama
DRAMA_FIX = """<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt>
<title>Fixture Play</title><author>Sophocles</author><editor role="translator">Richard Jebb</editor>
</titleStmt></fileDesc></teiHeader><text><body><div type="translation">
<div type="textpart" subtype="episode"><milestone unit="card" n="1"/>
<stage>Enter A.</stage>
<sp><speaker>A</speaker><l n="1">First words, <del>a doubtful phrase,</del> go on</l>
<l n="5">and on <stage>Turning.</stage> still speaking.</l></sp>
<sp><speaker>B</speaker><l n="1009a" part="F">Half a line.</l><l n="8"><gap reason="lost"/> after a gap.</l></sp>
</div><div type="textpart" subtype="choral"><sp><speaker>Chorus</speaker><l n="10">Sung.</l></sp>
<stage>Exeunt.</stage></div></div></body></text></TEI>"""
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(DRAMA_FIX); dr_path = f.name
_fixkey = ("fixture-play", "1009a")
st.TEI_DRAMA_N_FIX[_fixkey] = "6a"
dr = st.convert_tei_drama(dr_path, "fixture-play", "Fix.")
del st.TEI_DRAMA_N_FIX[_fixkey]
du = dr["units"]
check("drama: one unit per <l> segment, id = Greek line number",
      [u["id"] for u in du] == ["fixture-play:1", "fixture-play:5", "fixture-play:6a",
                                "fixture-play:8", "fixture-play:10"])
check("drama: speaker and choral section ride on each unit",
      du[0]["drama"]["speaker"] == "A" and du[2]["drama"]["speaker"] == "B"
      and du[4]["drama"] == {"speaker": "Chorus", "section": "choral", "stage": ["Exeunt."]})
check("drama: stage directions kept out of the spoken text, never dropped",
      du[0]["drama"]["stage"] == ["Enter A."] and du[1]["drama"]["stage"] == ["Turning."]
      and "Turning" not in du[1]["text"] and du[1]["text"] == "and on still speaking.")
check("drama: <del> is the translation's own text and is kept",
      "a doubtful phrase" in du[0]["text"])
check("drama: per-book line-number fix applies and is counted",
      "1 line number(s) corrected" in dr["scheme"]["note"])
check("drama: a lacuna is flagged, not invented",
      du[3]["drama"].get("gap") is True and du[3]["text"] == "after a gap.")
check("drama: honesty says segment, not exact line; translator from TEI",
      dr["scheme"]["resolution"] == "segment" and dr["source"]["translator"] == "Richard Jebb")
check("drama: rights block present, licence says share-alike, file without a licence line says so",
      dr["rights"]["license"] == "CC BY-SA 4.0" and "states no licence" in dr["rights"]["note"])
DRAMA_FIX2 = """<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt>
<title>Fixture Two</title><author>Euripides</author><editor role="translator">E. P. Coleridge</editor>
</titleStmt><publicationStmt><availability><licence target="x">CC BY-SA licence line</licence>
</availability></publicationStmt></fileDesc></teiHeader><text><body><div type="translation">
<l n="0" style="hidden"/>
<note resp="Coleridge" place="inline"><p>Dramatis Personae</p><p>Medea</p><p>Nurse</p></note>
<note resp="perseus" place="inline">Adapted and modernized.</note>
<div type="textpart" subtype="episode"><sp><speaker>Nurse</speaker>
<l n="1">Would that the Argo<note resp="Coleridge" n="1">The ship of Jason.</note> had never sped.</l>
</sp><stage>Enter Io<note resp="Smyth" n="561">On vase-paintings.</note></stage>
<sp><speaker>Io</speaker><l n="2">By Pluto's<note resp="Smyth">Giver of wealth.</note>stream.</l>
<l n="3">Son of <choice><sic>Jove</sic><corr>Zeus</corr></choice>.</l></sp></div></div></body></text></TEI>"""
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(DRAMA_FIX2); dr2_path = f.name
dr2 = st.convert_tei_drama(dr2_path, "fixture-two", "Fix2")
d2 = dr2["units"][0]["drama"]
check("drama: a footnote inside a line is lifted out of the spoken text, kept with its author",
      dr2["units"][0]["text"] == "Would that the Argo had never sped."
      and {"by": "Coleridge", "n": "1", "text": "The ship of Jason."} in d2["notes"])
check("drama: the cast list is kept whole at book level; an editor's front note rides on line 1",
      dr2["dramatis_personae"] == ["Medea", "Nurse"]
      and {"by": "perseus", "text": "Adapted and modernized."} in d2["notes"]
      and len(dr2["units"]) == 3)
check("drama: <choice> reads the correction and keeps what was printed under drama.sic",
      dr2["units"][2]["text"] == "Son of Zeus."
      and dr2["units"][2]["drama"]["sic"] == [{"corr": "Zeus", "sic": "Jove"}])
check("drama: a footnote lifted from between two words leaves them two words",
      dr2["units"][1]["text"] == "By Pluto's stream.")
check("drama: a footnote inside a stage direction goes to notes, not into the direction",
      dr2["units"][1]["drama"]["stage"] == ["Enter Io"]
      and {"by": "Smyth", "n": "561", "text": "On vase-paintings."} in dr2["units"][1]["drama"]["notes"])
check("drama: a licence line in the file is the one recorded",
      "CC BY-SA licence line" in dr2["rights"]["note"])
os.unlink(dr2_path)
_dramatists = ("sophocles-", "aeschylus-", "euripides-", "aristophanes-", "plautus-", "terence-")
check("drama: every play in the fetch manifest has a converter abbreviation, and back",
      {k for k in load("fetch_sources").PERSEUS if k.startswith(_dramatists)}
      == set(st.TEI_DRAMA))
os.unlink(dr_path)

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

# ------------------------------------------------- Thayer, split into entries
# Synthetic pages in Thayer's shape (headword, -gen., article; gloss). Each
# line is there to exercise one decision of convert_thayer_entries.
THAYER_PAGES = {
    "1": "PREFACE\n\n\u1F00\u03B3\u03AC\u03C0\u03B7, quoted in the preface, not an entry.\n",
    "2": "\u1F00\u03B3\u03B1\u03B8\u03CC\u03C2\n"
         "\n"
         "\u1F00\u03B3\u03B1\u03B8\u03CC\u03C2, -\u03AE, -\u03CC\u03BD, good, Mt. v. 45.\n"
         "so used of persons and things alike;\n"
         "\u03C8\u03C5\u03C7\u03AE, out of order: mid-entry Greek, not a head.\n"
         "\u1F00\u03B3\u03B1\u03B8\u03C9\u03C3\u03CD\u03BD\u03B7, -\u03B7\u03C2, \u1F21, goodness; its blank line lost.\n"
         "\n"
         "\u1F00\u03B3\u03B1\u03BB\u03BB\u03AF\u03B1\u03C3\u03B9\u03C2, -\u03B5\u03C9\u03C2, \u1F21, exultation,\n"
         "\u1F00\u03B3\u03B1\u03BC\u03BF\u03C2, in order but bare: no blank line, no lemma.\n"
         "2\n",
    "3": "\u1F00\u03B3\u03AC\u03C0\u03B7\n"
         "continued from the page before, Lk. i. 14.\n"
         "\n"
         "\u1F00\u03B3\u03AC\u03C0\u03B7, -\u03B7\u03C2, \u1F21, love, Jn. xiii. 35.\n",
    "4": "INDEX\n\n\u1F00\u03B2\u03B2\u1FB6, in the English index, not an entry.\n",
}
SG_FIX = ('<strongsdictionary><entries>'
          '<entry strongs="00018"><greek unicode="\u1F00\u03B3\u03B1\u03B8\u03CC\u03C2"/></entry>'
          '<entry strongs="00019"><greek unicode="\u1F00\u03B3\u03B1\u03B8\u03C9\u03C3\u03CD\u03BD\u03B7"/></entry>'
          '<entry strongs="00020"><greek unicode="\u1F00\u03B3\u03B1\u03BB\u03BB\u03AF\u03B1\u03C3\u03B9\u03C2"/></entry>'
          '<entry strongs="00026"><greek unicode="\u1F00\u03B3\u03AC\u03C0\u03B7"/></entry>'
          '</entries></strongsdictionary>')
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    _json.dump(THAYER_PAGES, f); te_path = f.name
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(SG_FIX); sg_path = f.name
te = st.convert_thayer_entries(te_path, strongs_path=sg_path)
heads = [u["lex"]["headword"] for u in te["units"]]
check("thayer-entries: front matter and appendix (no Greek running head) give no entries",
      all(1 < p < 4 for u in te["units"] for p in u["lex"]["pages"]))
check("thayer-entries: out-of-order mid-entry Greek is not a headword, its line stays in the entry",
      "\u03C8\u03C5\u03C7\u03AE" not in heads and "\u03C8\u03C5\u03C7\u03AE" in te["units"][0]["text"])
check("thayer-entries: a Strong's lemma in order is a headword even with its blank line lost",
      "\u1F00\u03B3\u03B1\u03B8\u03C9\u03C3\u03CD\u03BD\u03B7" in heads)
check("thayer-entries: in order but no other evidence is NOT a headword (text kept in the entry before)",
      "\u1F00\u03B3\u03B1\u03BC\u03BF\u03C2" not in heads
      and "in order but bare" in te["units"][2]["text"])
check("thayer-entries: an entry crossing a page keeps its text and links BOTH pages",
      te["units"][2]["lex"]["pages"] == [2, 3]
      and "continued from the page before" in te["units"][2]["text"]
      and [l["target"] for l in te["units"][2]["links"] if l["kind"] == "page"]
          == ["thayer:p.2", "thayer:p.3"])
check("thayer-entries: id is page + transliterated headword; ref says s.v.",
      te["units"][0]["id"] == "thayer-entries:p.2.agathos"
      and te["units"][0]["ref"] == "Thayer p. 2, s.v. \u1F00\u03B3\u03B1\u03B8\u03CC\u03C2")
check("thayer-entries: headword linked to its Strong's entry, accents matched",
      {"kind": "strongs", "target": "strongs-greek:G26", "match": "headword, accents matched"}
      in te["units"][-1]["links"])
check("thayer-entries: exactly the four real entries, in order",
      [u["id"] for u in te["units"]] == ["thayer-entries:p.2.agathos",
                                        "thayer-entries:p.2.agathosune",
                                        "thayer-entries:p.2.agalliasis",
                                        "thayer-entries:p.3.agape"])
check("thayer-entries: honesty says INFERRED; the page book still says NOT segmented",
      "INFERRED" in te["scheme"]["honesty"] and te["scheme"]["segmentation"]["weak"] == 1)
te0 = st.convert_thayer_entries(te_path)
check("thayer-entries: without Strong's it still builds, drops lemma-only heads, and says so",
      "WITHOUT Strong's" in te0["scheme"]["note"]
      and "\u1F00\u03B3\u03B1\u03B8\u03C9\u03C3\u03CD\u03BD\u03B7" not in
          [u["lex"]["headword"] for u in te0["units"]])
check("thayer-entries: deterministic -- same input, same bytes",
      _json.dumps(st.convert_thayer_entries(te_path, strongs_path=sg_path), ensure_ascii=False)
      == _json.dumps(te, ensure_ascii=False))
check("thayer-entries: key ignores accents, breathings, case, final sigma",
      st.thayer_key("\u1F08\u03B3\u03B1\u03B8\u03CC\u03C2") == st.thayer_key("\u03B1\u03B3\u03B1\u03B8\u03BF\u03C3")
      and st.thayer_translit("\u1FE5\u1FC6\u03BC\u03B1") == "rhema")
check("thayer-entries: weighted chain is the max-weight strictly increasing run",
      st._lis_weighted(["b", "a", "c", "b", "d"], [1, 1, 1, 3, 1]) == [1, 3, 4])
os.unlink(te_path); os.unlink(sg_path)

# Two ways the first cut dropped real entries (review of PR #7, 2026-10-02):
# a one-letter headword (the article), and two headwords told apart only by
# an accent (εἰμί "I am" / εἶμι "I go").
EIMI, EIMI2 = "\u03B5\u1F30\u03BC\u03AF", "\u03B5\u1F36\u03BC\u03B9"
TH2 = {"5": "\u1F41\n\n"
            + EIMI + ", I am.\n"
            + EIMI + ", cited again mid-entry.\n\n"
            + EIMI2 + ", I go.\n\n"
            "\u03BD\u03CD\u03BE, -\u03BA\u03C4\u03CC\u03C2, \u1F21, night.\n\n"
            "\u1F41, \u1F21, \u03C4\u03CC, the article.\n"
            "\u03B2, a lone letter numeral line.\n\n"
            "\u03C0\u03B1\u03C4\u03AE\u03C1, -\u03C4\u03C1\u03CC\u03C2, \u1F41, father.\n"}
SG2 = ('<strongsdictionary><entries>'
       '<entry strongs="03571"><greek unicode="\u03BD\u03CD\u03BE"/></entry>'
       '<entry strongs="03588"><greek unicode="\u1F41"/></entry>'
       '<entry strongs="03962"><greek unicode="\u03C0\u03B1\u03C4\u03AE\u03C1"/></entry>'
       '<entry strongs="01510"><greek unicode="' + EIMI + '"/></entry>'
       '<entry strongs="01511"><greek unicode="' + EIMI2 + '"/></entry>'
       '</entries></strongsdictionary>')
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    _json.dump(TH2, f); t2_path = f.name
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(SG2); s2_path = f.name
t2 = st.convert_thayer_entries(t2_path, strongs_path=s2_path)
h2 = [u["lex"]["headword"] for u in t2["units"]]
check("thayer-entries: a one-letter headword (the article) is an entry when it opens a "
      "paragraph and is a Strong's lemma; a lone numeral letter is not",
      h2[2:] == ["\u03BD\u03CD\u03BE", "\u1F41", "\u03C0\u03B1\u03C4\u03AE\u03C1"]
      and "\u03B2" not in h2 and "numeral" in t2["units"][3]["text"])
check("thayer-entries: accent-only homographs are two entries; the same form cited again is not",
      h2[:2] == [EIMI, EIMI2] and "cited again" in t2["units"][0]["text"])
check("thayer-entries: accents pick the Strong's number among homographs",
      [l["target"] for u in t2["units"][:2] for l in u["links"] if l["kind"] == "strongs"]
      == ["strongs-greek:G1510", "strongs-greek:G1511"])
os.unlink(t2_path); os.unlink(s2_path)

# What the 2026-10-02 rebuild added: headwords followed by ; or [, misread
# headwords read back to the one Strong's lemma they can be, and the stop at
# the APPENDIX (whose later pages carry Greek running heads again).
TH3 = {"6": "βαρέω\n\n"
            "Bapéw, -ῶ : to burden.\n\n"
            "Γεθσημανῆ [or -νεί], Gethsemane.\n\n"
            "γυμνάζω; [pf. pass.] to exercise.\n\n"
            "Δυσανίας, -ου, ὁ, Lysanias.\n\n"
            "ὁράω, -ῶ; to see, the last entry.\n",
       "7": "APPENDIX.\n\nψυχή, in a vocabulary list.\n",
       "8": "ὤφθην\n\nὤφθην, 1 aor. pass. of ὁράω.\n"}
SG3 = ('<strongsdictionary><entries>'
       '<entry strongs="00916"><greek unicode="βαρέω"/></entry>'
       '<entry strongs="01068"><greek unicode="Γεθσημανῆ"/></entry>'
       '<entry strongs="01128"><greek unicode="γυμνάζω"/></entry>'
       '<entry strongs="03078"><greek unicode="Λυσανίας"/></entry>'
       '<entry strongs="03708"><greek unicode="ὁράω"/></entry>'
       '</entries></strongsdictionary>')
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    _json.dump(TH3, f); t3_path = f.name
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(SG3); s3_path = f.name
t3 = st.convert_thayer_entries(t3_path, strongs_path=s3_path)
ids3 = [u["id"] for u in t3["units"]]
check("thayer-entries: a headword followed by ';' or '[' is a candidate",
      "thayer-entries:p.6.gethsemane" in ids3 and "thayer-entries:p.6.gumnazo" in ids3)
check("thayer-entries: a Greek headword one letter off a lemma is read back (Δυσανίας -> Λυσανίας)",
      "thayer-entries:p.6.lusanias" in ids3
      and t3["units"][ids3.index("thayer-entries:p.6.lusanias")]["lex"]["headword"]
          == "Δυσανίας"
      and {"kind": "strongs", "target": "strongs-greek:G3078",
           "match": "headword, OCR misread read back"}
          in t3["units"][ids3.index("thayer-entries:p.6.lusanias")]["links"])
check("thayer-entries: a headword OCR'd in Latin lookalikes is read back (Bapéw -> βαρέω)",
      ids3[0] == "thayer-entries:p.6.bareo"
      and t3["units"][0]["lex"]["headword_read"] == "βαρέω"
      and "ocr-read" in t3["units"][0]["lex"]["evidence"])
check("thayer-entries: the last entry stops at the APPENDIX; later Greek-headed pages add nothing",
      ids3[-1] == "thayer-entries:p.6.horao" and t3["units"][-1]["lex"]["pages"] == [6]
      and len(ids3) == 5 and t3["scheme"]["segmentation"]["ocr_read_entries"] == 2)
check("thayer-entries: a near-miss of a lemma the OCR spells right is NOT read as it (ἄγαμος)",
      not any(u["lex"].get("headword_read") for u in te["units"]))
check("thayer-entries: reading needs ONE lemma; two within reach is no reading",
      st.thayer_read("αβγδε", {}, {5: ["αβγδζ", "αβγδη"]}) is None
      and st.thayer_read("αβγδε", {}, {5: ["αβγδζ"]})
          == "αβγδζ")

# A headword the first OCR mangled past reading, printed clean by the second.
TH4 = {"6": "βαρέω\n\n"
            "βαρέω, -ῶ : to burden, weigh down.\n\n"
            "#qq%9, -ov, 6, Lysanias, tetrarch of Abilene, Lk. iii. 1.\n\n"
            "ὁράω, -ῶ; to see, the last entry.\n"}
TH4_2 = {"6": "βαρέω\n\n"
              "βαρέω, -ῶ : to burden, weigh down.\n\n"
              "Λυσανίας, -ου, ὁ, Lysanias, tetrarch of Abilene, Lk. iii. 1.\n\n"
              "ὁράω, -ῶ; to see, the last entry.\n"}
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    _json.dump(TH4, f); t4_path = f.name
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    _json.dump(TH4_2, f); t4b_path = f.name
t4a = st.convert_thayer_entries(t4_path, strongs_path=s3_path)
t4 = st.convert_thayer_entries(t4_path, strongs_path=s3_path, second_path=t4b_path)
ly = [u for u in t4["units"] if u["lex"].get("headword_read") == "Λυσανίας"]
check("thayer-entries: a second OCR cuts an entry where the first lost the headword",
      len(t4a["units"]) == 2 and len(t4["units"]) == 3 and len(ly) == 1
      and "second-ocr" in ly[0]["lex"]["evidence"]
      and t4["scheme"]["segmentation"]["second_ocr_entries"] == 1)
check("thayer-entries: the second OCR gives the boundary only; the text is the first OCR's",
      ly[0]["text"].startswith("#qq%9, -ov, 6, Lysanias")
      and "strongs-greek:G3078" in [l["target"] for l in ly[0]["links"]])
os.unlink(t4_path); os.unlink(t4b_path)
os.unlink(t3_path); os.unlink(s3_path)

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

# ---------------------------------------------------------------- 2026-09-11
# Three defects found by phrase extraction, each of which passed every check
# the suite had at the time. Apparatus and dropped verses are invisible to a
# parser that has no opinion about what the work is.

# (1) the 420-verse bug: a verse marker at END OF LINE. Gutenberg hard-wraps at
# ~70 chars; when the wrap lands right after a marker there is no trailing
# whitespace, so RE_VMARK missed it, the marker was read as body text, and the
# whole verse merged into its predecessor. 420 of 31,102 verses, silently.
_eol = st.RE_VMARK.findall("and begat Jared: 5:16")
check("kjv: verse marker at end of line is still a marker", _eol == [("5", "16")])
check("kjv: marker mid-line still works",
      st.RE_VMARK.findall("5:15 And Mahalaleel lived: 5:16 And") == [("5", "15"), ("5", "16")])
check("kjv: a bare colon is not a marker", st.RE_VMARK.findall("daughters:") == [])

# (2) apparatus inside the work -- BODY_RULES must remove it and say so
_body, _note = st.apply_body_rules("alpha\nTRANSLATION.\nthe epic itself\n"
                                   "TRANSLITERATION.\nsa-am-ha-ku-ma\n", "gilgamesh")
check("body rules: keeps only TRANSLATION sections", _body.strip() == "the epic itself")
check("body rules: records what it removed", _note and "apparatus removed" in _note)
_b2, _n2 = st.apply_body_rules("x\ny\n", "treasure_island")
check("body rules: a work with no rule is untouched", _b2 == "x\ny\n" and _n2 is None)

# (3) a translator's marginal gloss opens on one line and closes on the next,
# so the scrub has to run over the joined text or it leaves both halves behind
_g, _ = st.apply_body_rules("\n".join(["I."] * 0 + ["I.", "line one {a gloss that",
                                                     "runs on} line two", "ADDENDA."]), "beowulf")
check("body rules: multi-line gloss is removed whole", "{" not in _g and "}" not in _g)
check("body rules: text around the gloss survives", "line two" in _g)

# ------------------------------------------- Shakespeare: the six poems
# The Complete Works is 38 plays AND 6 poems. The parser recognised a work by
# "an ALL-CAPS line with a Contents block after it", and not one of the six
# poems has one. So The Sonnets -- which sit before the first play -- were
# DROPPED ENTIRELY, all 154 of them, with no error; and A Lover's Complaint,
# The Passionate Pilgrim, The Phoenix and the Turtle, The Rape of Lucrece and
# Venus and Adonis were filed as 609 lines of The Winter's Tale, Act V Sc. iii.

# str.title() capitalises the letter after an apostrophe. The play's name is in
# the ref of EVERY one of its units, so this reached search results and copied
# citations, not only a heading.
check("shakespeare: apostrophes are not capitalised",
      st.sh_titlecase("ALL’S WELL THAT ENDS WELL") == "All’s Well That Ends Well")
check("shakespeare: small words in a title stay small",
      st.sh_titlecase("THE TRAGEDY OF ANTONY AND CLEOPATRA")
      == "The Tragedy of Antony and Cleopatra")
check("shakespeare: the first word is never lowered",
      st.sh_titlecase("A MIDSUMMER NIGHT’S DREAM") == "A Midsummer Night’s Dream")

# Where the poem proper begins. Prose apparatus is hard-wrapped to 71 columns;
# no verse line in the six poems exceeds 56. Lucrece line 1 must be "From the
# besieged Ardea all in post" and not the first line of its dedication.
_LUC = [["TO THE RIGHT HONOURABLE", "HENRY WRIOTHESLEY, EARL OF SOUTHAMPTON,",
         "and Baron of Titchfield."],
        ["The love I dedicate to your Lordship is without end; whereof this",
         "pamphlet, without beginning, is but a superfluous moiety. The warrant"],
        ["THE ARGUMENT."],
        ["Lucius Tarquinius (for his excessive pride surnamed Superbus), after he",
         "had caused his own father-in-law, Servius Tullius, to be cruelly"],
        ["From the besieged Ardea all in post,", "Borne by the trustless wings of",
         "false desire,", "Lust-breathed Tarquin leaves the Roman host,"]]
check("shakespeare: a poem starts after its dedication and argument",
      st._sh_poem_start(_LUC) == 4)
check("shakespeare: an ALL-CAPS block is apparatus, not the poem's first line",
      st._sh_poem_start([["TO THE RIGHT HONOURABLE", "HENRY WRIOTHESLEY,",
                          "and Baron of Titchfield."],
                         ["Even as the sun with purple-colour’d face",
                          "Had ta’en his last leave of the weeping morn,",
                          "Rose-cheek’d Adonis hied him to the chase;"]]) == 1)

_SON = """THE SONNETS

                    1

From fairest creatures we desire increase,
That thereby beauty’s rose might never die,

                    2

When forty winters shall besiege thy brow,
And dig deep trenches in thy beauty’s field,

THE END"""
_su = st.convert_sh_poem(_SON.splitlines()[1:], "sonnets", "The Sonnets")
check("shakespeare: each sonnet is one unit, numbered by the text",
      [u["id"] for u in _su]
      == ["shakespeare:sonnets.1.1", "shakespeare:sonnets.2.1"])
check("shakespeare: a sonnet's ref names the sonnet", _su[0]["ref"] == "Sonnet 1")
check("shakespeare: a sonnet is kept whole, so it copies as a poem",
      _su[0]["text"].count("\n") == 1 and "beauty’s rose" in _su[0]["text"])
# "THE END" became line 15 of Sonnet 154, which has fourteen.
check("shakespeare: Gutenberg's end marker is not a line of the poem",
      all("THE END" not in u["text"] for u in _su))
# The sonnet number is itself an indented bare numeral, so a marginal-number
# stripper without a lookbehind ate it and merged all 154 into one poem.
check("shakespeare: the sonnet number survives the marginal-number stripper",
      _su[1]["lines"] == [1, 2])

_VEN = """VENUS AND ADONIS

Even as the sun with purple-colour’d face
Had ta’en his last leave of the weeping morn,
Saith that the world hath ending with thy life.     12"""
_vu = st.convert_sh_poem(_VEN.splitlines()[1:], "venus-and-adonis", "Venus and Adonis")
check("shakespeare: the printed marginal line number is stripped from the verse",
      _vu and "12" not in _vu[0]["text"].splitlines()[-1])
# NOT "l. 1": the scholarly abbreviation for a line is also the Roman numeral
# L, so the reader's contents read "A Lover's Complaint, l" as a division.
check("shakespeare: an unsectioned poem cites by a bare line number",
      _vu[0]["ref"] == "Venus and Adonis, 1" and _vu[0]["lines"] == [1, 3])

# The manifest guard. A work that produces nothing is a build failure -- this
# is the check whose absence let 154 sonnets disappear without a word.
check("shakespeare: the book's front Contents is the manifest",
      st.sh_manifest(["Contents", "", "    THE SONNETS", "    THE TEMPEST",
                      "    VENUS AND ADONIS", "    CYMBELINE", "    MACBETH", ""])
      == ["THE SONNETS", "THE TEMPEST", "VENUS AND ADONIS", "CYMBELINE", "MACBETH"])
check("shakespeare: a play's own act/scene table is not the manifest",
      st.sh_manifest(["Contents", "", "ACT I", "Scene I.", "ACT V", "Scene V.", ""]) == [])

# Author shelves (Chesterton, 2026-09-29). An essay collection prints its
# titles in CAPITALS in the Contents and in title case in the body, so the
# headings are read from the book's own Contents. Fixture is invented text.
import tempfile as _tf
_ESS = ("CONTENTS\n\n  I. ON LAMPS                 7\n  II. THE MOCK GOOSE ~ ~ ~   12\n\n\n\n\n"
        "On Lamps ~ ~ ~ ~\n\nFirst paragraph about lamps.\n\nSecond about lamps.\n\n"
        "The Mock Goose\n\nA paragraph about geese.\n")
with _tf.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _fh:
    _fh.write(_ESS)
_saved_corpus = st.CORPUS
st.CORPUS = os.path.dirname(_fh.name)
_rx = st.contents_chapre(_fh.name)
_eb = st.convert_gutenberg_prose(_fh.name, "t", "T", "A", _rx)
st.CORPUS = _saved_corpus
os.unlink(_fh.name)
_refs = [u["ref"] for u in _eb["units"]]
check("shelf: a title-case body heading is found from the CAPS Contents",
      _refs == ["On Lamps, par. 1", "On Lamps, par. 2", "The Mock Goose, par. 1"])
check("shelf: numbering and page numbers are not part of a Contents key",
      st._contents_key("  II. THE MOCK GOOSE ~ ~ ~   12") == "THE MOCK GOOSE")
check("shelf: a book with no Contents falls back to the CAPS rule",
      st.contents_chapre.__doc__ and st.CAPS_HEADING in _rx)
check("thml: <pre> verse is read only where a book opts in",
      "chesterton-whitehorse" in st.THML_PRE_VERSE and len(st.THML_PRE_VERSE) == 1)

# Perseus TEI P4 (Tacitus, 2026-10-02): <TEI.2>, no namespace, numbered
# <div1>/<div2>, and HTML entities only the DTD defines. Lifted into the P5
# shape in memory. Invented text.
_P4 = ('<?xml version="1.0"?>\n<!DOCTYPE TEI.2 PUBLIC "-//TEI P4//DTD Main DTD Driver File//EN" '
       '"http://www.tei-c.org/Guidelines/DTD/tei2.dtd">\n'
       '<TEI.2><teiHeader><fileDesc><titleStmt><title>Annals</title><author>Tacitus</author>'
       '<editor role="translator">A. Church</editor><editor role="translator">W. Brodribb</editor>'
       '</titleStmt></fileDesc></teiHeader><text><body xml:base="urn:cts:latinLit:phi1351.phi005.perseus-eng1">'
       '<div1 type="book" n="1"><head>BOOK I</head>'
       '<div2 type="chapter" n="1"><p>The C&aelig;sars ruled.</p></div2>'
       '<div2 type="chapter" n="2"><p>Then Asiniu<name>s</name> spoke.</p></div2>'
       '<div2 type="chapter" n="3"><p><gap/></p></div2>'
       '</div1></body></text></TEI.2>')
with _tf.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as _fh:
    _fh.write(_P4)
_saved_corpus = st.CORPUS
st.CORPUS = os.path.dirname(_fh.name)
_p4 = st.convert_tei_prose(_fh.name, "tac", "Tac. Ann.")
st.CORPUS = _saved_corpus
os.unlink(_fh.name)
_p4u = {u["id"]: u for u in _p4["units"]}
check("tei-p4: div1/div2 become book.chapter units",
      list(_p4u) == ["tac:1.1", "tac:1.2"] and _p4["scheme"]["citation"] == "Tac. Ann. book.chapter")
check("tei-p4: a DTD-only entity (&aelig;) is read, not fatal",
      _p4u["tac:1.1"]["text"] == "The Cæsars ruled.")
check("tei-p4: every translator the title names is recorded",
      _p4["source"]["translator"] == "A. Church & W. Brodribb")
check("tei-p4: a textless division's lacuna rides on the unit before it",
      _p4u["tac:1.2"]["apparatus"].get("gap") is True)
check("tei-p4: the urn still picks the latinLit repository",
      "canonical-latinLit" in _p4["rights"]["source_url"])
check("tei-p4: every Tacitus book carries the 1942-reprint caveat",
      all(s in st.TEI_RIGHTS_NOTE for s in st.TEI_PROSE if s.startswith("tacitus-")))

# Cicero (2026-10-02). Invented text. Sections as milestones inside the
# paragraphs, a numbering slip, beta-code Greek, a name with no space after
# it, two Greek words tagged back to back, and an argument beside chapters.
_CIC = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt>'
        '<title>On Old Age</title><author>Cicero</author></titleStmt></fileDesc></teiHeader>'
        '<text><body xml:base="urn:cts:latinLit:phi0474.phi051.perseus-eng1">'
        '<div type="translation"><head>Cato on old age</head>'
        '<p><milestone unit="chapter" n="1"/><milestone unit="section" n="1"/>First, '
        '<placeName key="tgn,7000874">Rome</placeName>was great; the <foreign xml:lang="greek">'
        'filo/sofos</foreign> agrees.<note>A note.</note> <milestone unit="section" n="2"/>Second '
        'part of the same paragraph.</p><p>Still two, <foreign xml:lang="grc">ναὸς</foreign>'
        '<foreign xml:lang="grc">ἐν</foreign> said.</p><p><milestone unit="section" n="2"/>Third.</p>'
        '</div></body></text></TEI>')
with _tf.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as _fh:
    _fh.write(_CIC)
_saved = (st.CORPUS, dict(st.TEI_PROSE_CUT), dict(st.TEI_PROSE_N_FIX))
st.CORPUS = os.path.dirname(_fh.name)
st.TEI_PROSE_CUT["cic"] = ("section",)
st.TEI_PROSE_N_FIX["cic"] = {("section", "2", 2): "3"}
_cb = st.convert_tei_prose(_fh.name, "cic", "Cic. Sen.")
st.CORPUS = _saved[0]; st.TEI_PROSE_CUT.clear(); st.TEI_PROSE_CUT.update(_saved[1])
st.TEI_PROSE_N_FIX.clear(); st.TEI_PROSE_N_FIX.update(_saved[2])
os.unlink(_fh.name)
_cu = {u["id"]: u for u in _cb["units"]}
check("milestones: one unit per section, cut mid-paragraph",
      list(_cu) == ["cic:1", "cic:2", "cic:3"] and _cb["scheme"]["citation"] == "Cic. Sen. section")
check("milestones: a section ends where the next begins",
      _cu["cic:1"]["text"].endswith("agrees.") and _cu["cic:2"]["text"].startswith("Second part"))
check("milestones: a section runs across paragraphs",
      "Still two" in _cu["cic:2"]["text"])
check("milestones: the title before the first section rides as head",
      _cu["cic:1"]["apparatus"]["head"] == ["Cato on old age"])
check("milestones: the chapter is recorded beside the section",
      _cu["cic:1"].get("milestones") == {"chapter": "1"})
check("milestones: a note stays with its own section",
      [n["text"] for n in _cu["cic:1"]["apparatus"]["notes"]] == ["A note."]
      and "notes" not in _cu["cic:2"].get("apparatus", {}))
check("n-fix: a repeated section number is corrected by rule",
      "Third" in _cu["cic:3"]["text"])
check("beta code: Greek written in ASCII becomes Unicode",
      "φιλόσοφος" in _cu["cic:1"]["text"] and "nbeta" not in _cb["scheme"]["note"]
      and "1 Greek phrase(s)" in _cb["scheme"]["note"])
check("beta code: capital diphthongs, iota subscript, final sigma",
      st.beta_to_unicode("*)eumolpidw=n tw=| qew=|") == "Εὐμολπιδῶν τῷ θεῷ")
check("beta code: transliteration with no beta marks is left alone",
      not st.RE_BETA.search("marna"))
check("weld: a name with no space after it gets one",
      "Rome was great" in _cu["cic:1"]["text"])
check("weld: two Greek words tagged back to back are two words",
      "ναὸς ἐν said" in _cu["cic:2"]["text"])
check("weld: a one-letter suffix the markup split off stays joined",
      not st.RE_NAME_WELD.match("s ") and st.RE_NAME_WELD.match("was"))
_ARG = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title>Phil</title>'
        '</titleStmt></fileDesc></teiHeader><text><body>'
        '<div type="textpart" subtype="speech" n="1">'
        '<div type="textpart" subtype="argumnt" n="arg"><p>The argument.</p></div>'
        '<div type="textpart" subtype="chapter" n="1"><p>One.</p></div></div></body></text></TEI>')
with _tf.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as _fh:
    _fh.write(_ARG)
st.CORPUS = os.path.dirname(_fh.name)
_ab = st.convert_tei_prose(_fh.name, "ph", "Cic. Phil.")
st.CORPUS = _saved[0]
os.unlink(_fh.name)
check("levels: an unnumbered argument beside numbered chapters is not a level",
      _ab["scheme"]["citation"] == "Cic. Phil. speech.chapter"
      and [u["id"] for u in _ab["units"]] == ["ph:1.arg", "ph:1.1"])

# Cicero's letters (Shuckburgh). Invented text: a letter split in two, a
# citation printed twice under two Shuckburgh numbers, an essay on a letter
# with no number of its own, another collection's letter, an exact copy,
# and Greek tagged straight after an English word.
_LET = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title>Letters</title>'
        '<editor role="translator">E. S. Shuckburgh</editor></titleStmt></fileDesc></teiHeader>'
        '<text><body xml:base="urn:cts:latinLit:phi0474.phi057.perseus-eng1"><div type="translation">'
        '<div n="text=A:book=1:letter=5" type="letter" xml:id="s1"><epigraph><p>An intro.</p></epigraph>'
        '<head>I (A I, 5)</head><opener>TO ATTICUS</opener><p>Dear friend, the <foreign xml:lang="greek">'
        'kaqh=kon</foreign> of it.</p></div>'
        '<div n="text=A:book=12:letter=5.1-2" type="letter" xml:id="s2"><p>First half.</p></div>'
        '<div n="text=A:book=12:letter=5.4" type="letter" xml:id="s3"><p>Second half.</p></div>'
        '<div n="text=A:book=4:letter=1" type="letter" xml:id="s4"><p>One.</p></div>'
        '<div n="text=A:book=4:letter=1" type="letter" xml:id="s5"><p>Another.</p></div>'
        '<div n="text=A:book=1:letter=5" type="letter"><head>ESSAY (LETTER I)</head><p>On it.</p></div>'
        '<div n="text=Q FR:book=1:letter=1" type="letter" xml:id="s6"><p>To Quintus.</p></div>'
        '<div n="text=A:book=12:letter=5.4" type="letter" xml:id="s3"><p>Second half.</p></div>'
        '<div n="text=A:book=2:letter=1" type="letter" xml:id="s7"><p>A word of<foreign xml:lang="grc">'
        'συμπόσια</foreign> here.</p></div>'
        '</div></body></text></TEI>')
with _tf.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as _fh:
    _fh.write(_LET)
st.CORPUS = os.path.dirname(_fh.name)
_lb = st.convert_tei_letters(_fh.name, "att", "Cic. Att.", "A")
st.CORPUS = _saved[0]
os.unlink(_fh.name)
_lu = {u["id"]: u for u in _lb["units"]}
check("letters: one unit per letter at its canonical citation",
      list(_lu) == ["att:1.5", "att:12.5.1-2", "att:12.5.4", "att:4.1~s4", "att:4.1~s5", "att:2.1"])
check("letters: Shuckburgh's own number rides on each unit",
      _lu["att:1.5"]["edition"] == {"shuckburgh": 1})
check("letters: his introduction and head are apparatus, the letter is text",
      _lu["att:1.5"]["apparatus"]["head"] == ["An intro.", "I (A I, 5)"]
      and _lu["att:1.5"]["text"].startswith("TO ATTICUS Dear friend"))
check("letters: an essay with no number rides on its letter as appendix",
      _lu["att:1.5"]["apparatus"]["appendix"] == ["ESSAY (LETTER I) On it."])
check("letters: another collection's letter and an exact copy are not built",
      "1 letter(s) of other collections" in _lb["scheme"]["note"]
      and "1 exact duplicate(s)" in _lb["scheme"]["note"])
check("letters: beta-code Greek is Unicode in the letter",
      "καθῆκον" in _lu["att:1.5"]["text"])
check("weld: Greek tagged straight after an English word is a new word",
      "of συμπόσια here" in _lu["att:2.1"]["text"])

# Lucian and Appian (2026-10-02): a speaker label and a tagged number with
# no space before the next word.
_lbl = st.tei_split(st.ET.fromstring(
    '<p xmlns="http://www.tei-c.org/ns/1.0"><label>Pamphilus</label>True, indeed! He slew'
    '<date when="1500">1500</date>, and <label>A</label>s</p>'))[0]
check("weld: a speaker label is its own word", _lbl.startswith("Pamphilus True, indeed!"))
check("weld: a number tagged straight after a word is its own word", "slew 1500," in _lbl)

check("honesty: every override names a prose book; every Appian book but the preface has one",
      all(k in st.TEI_PROSE for k in st.TEI_PROSE_HONESTY)
      and all(k in st.TEI_PROSE for k in st.TEI_PROSE_LEVELS)
      and all(k in st.TEI_PROSE_HONESTY for k in st.TEI_PROSE
              if k.startswith("appian-") and "preface" not in k))

# Roman comedy (Plautus, Terence; 2026-10-02). Invented text: acts and
# scenes, a scene head, the Latin line.
_PL = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title>Am</title>'
       '</titleStmt></fileDesc></teiHeader><text><body xml:base="urn:cts:latinLit:phi0119.phi001.perseus-eng2">'
       '<div type="translation"><div type="textpart" subtype="act" n="1">'
       '<div type="textpart" subtype="scene" n="1"><head>THE PROLOGUE.</head>'
       '<sp><speaker>MERCURY</speaker><l n="1">As you buy and sell,</l><l n="6">so hear me.</l></sp>'
       '</div><div type="textpart" subtype="scene" n="2"><sp><speaker>SOSIA</speaker>'
       '<l n="153">Who is bolder than I?</l></sp></div></div></div></body></text></TEI>')
with _tf.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as _fh:
    _fh.write(_PL)
st.CORPUS = os.path.dirname(_fh.name)
_pb = st.convert_tei_drama(_fh.name, "am", "Pl. Am.")
st.CORPUS = _saved[0]
os.unlink(_fh.name)
_pu = {u["id"]: u for u in _pb["units"]}
check("roman comedy: cited by the Latin line",
      _pb["scheme"]["citation"] == "Pl. Am. line (Latin lineation)")
check("roman comedy: act and scene ride on each unit",
      _pu["am:1"]["drama"].get("act") == "1" and _pu["am:153"]["drama"].get("scene") == "2")
check("roman comedy: a scene head is kept, on the next unit",
      _pu["am:1"]["drama"].get("head") == ["THE PROLOGUE."] and "head" not in _pu["am:6"]["drama"])
check("drama honesty: segment length is measured, not assumed",
      "the longest runs 147" in _pb["scheme"]["honesty"])

# The Greek fathers from First1KGreek (2026-10-02). Invented text in a
# "first1k" folder: a section milestone OUTSIDE the chapter it opens, an
# OCR'd code-point name, a Latin-letter slip, the edition's sourceDesc.
_GK = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title>Protr</title>'
       '<author>Clement</author></titleStmt><publicationStmt><availability><licence>CC BY-SA 4.0'
       '</licence></availability></publicationStmt><sourceDesc><biblStruct><monogr>'
       '<editor>&gt;Otto Stählin</editor><title>Protrepticus</title><imprint><publisher>Hinrichs'
       '</publisher><pubPlace>Leipzig</pubPlace><date>1905</date></imprint></monogr></biblStruct>'
       '</sourceDesc></fileDesc></teiHeader><text><body><div type="edition" xml:lang="grc">'
       '<milestone unit="section" n="1"/><div type="textpart" subtype="chapter" n="1">'
       '<p>ἄλφα βῆτα <milestone unit="section" n="2"/>γάμμα τῆU+03F2 λέrει</p></div>'
       '<milestone unit="section" n="3"/><div type="textpart" subtype="chapter" n="2">'
       '<p>δέλτα</p></div></div></body></text></TEI>')
_gd = _tf.mkdtemp()
os.makedirs(os.path.join(_gd, "first1k"))
_gp = os.path.join(_gd, "first1k", "gk.xml")
open(_gp, "w", encoding="utf-8").write(_GK)
st.CORPUS = _gd
st.TEI_PROSE_CUT["gk"] = ("section",)
_gb = st.convert_tei_prose(_gp, "gk", "Clem. Protr.")
_np = os.path.join(_gd, "gk.xml")                  # the same file, NOT from First1KGreek
open(_np, "w", encoding="utf-8").write(_GK)
_nb = st.convert_tei_prose(_np, "gk", "Clem. Protr.")
del st.TEI_PROSE_CUT["gk"]
st.CORPUS = _saved[0]
_gu = {u["id"]: u for u in _gb["units"]}
check("fathers: a section milestone outside its chapter opens that chapter's text",
      list(_gu) == ["gk:1.1", "gk:1.2", "gk:2.3"] and _gu["gk:1.1"]["text"] == "ἄλφα βῆτα")
check("fathers: the edition is recorded, a stray '>' in the editor dropped",
      _gb["source"]["edition"]["editor"] == "Otto Stählin"
      and _gb["source"]["edition"]["date"] == "1905" and _gb["source"]["language"] == "grc")
check("fathers: rights credit First1KGreek and name the printed edition",
      _gb["rights"]["attribution"].startswith("First1KGreek")
      and "Otto Stählin, Protrepticus, Leipzig, 1905" in _gb["rights"]["note"])
check("fathers: a code-point name is decoded; a Latin-letter word is counted, not changed",
      "τῆϲ" in _gu["gk:1.2"]["text"] and "λέrει" in _gu["gk:1.2"]["text"]
      and _gu["gk:1.2"]["apparatus"]["latin_letters"] == 1 and "apparatus" not in _gu["gk:2.3"])
check("fathers: honesty names the printed edition whose numbering the ids are",
      "(Otto Stählin, 1905)" in _gb["scheme"]["honesty"]
      and "born-in from Perseus" in _nb["scheme"]["honesty"])
check("fathers: outside First1KGreek the same markup is not taken for an original",
      "edition" not in _nb["source"] and "latin_letters" not in str(_nb["units"])
      and _nb["rights"]["attribution"].startswith("Perseus"))
# An English translation from First1KGreek: the translator is the printed
# book's author; the rights say translation, not edition.
_EN = (_GK.replace('<div type="edition" xml:lang="grc">', '<div type="translation" xml:lang="eng">')
       .replace('<editor>&gt;Otto Stählin</editor>', '<author>James, Montague Rhodes</author>')
       .replace('<date>1905</date>', '<date>1924</date>'))
_ep = os.path.join(_gd, "first1k", "en.xml")
open(_ep, "w", encoding="utf-8").write(_EN)
st.CORPUS = _gd
_eb = st.convert_tei_prose(_ep, "en", "Act. Thom.")
st.CORPUS = _saved[0]
check("fathers: a First1KGreek translation names its translator and says so in the rights",
      _eb["source"]["translator"] == "James, Montague Rhodes" and "edition" not in _eb["source"]
      and "The translation is public domain (James, Montague Rhodes" in _eb["rights"]["note"]
      and "(James, Montague Rhodes, 1924)" in _eb["scheme"]["honesty"])
_open = open(_gp, encoding="utf-8").read().replace("<p>δέλτα", "<p>³δέλτα")
open(_gp, "w", encoding="utf-8").write(_open)
st.CORPUS = _gd
st.TEI_PROSE_VERSE_NUMERALS.add("gk")
_vb = st.convert_tei_prose(_gp, "gk", "1 En.")
st.TEI_PROSE_VERSE_NUMERALS.discard("gk")
st.CORPUS = _saved[0]
check("fathers: a verse number glued to the verse's first word is dropped, and counted",
      _vb["units"][-1]["text"] == "δέλτα" and "1 printed verse number(s)" in _vb["scheme"]["note"])
# CSEL (Open Greek and Latin, Latin): the edition's rights and language,
# the OCR caveat, and an unnumbered preface named by what it is.
_CS = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title>De Anima</title>'
       '<author>Tertullian</author></titleStmt><publicationStmt><availability><licence>CC BY-SA 4.0'
       '</licence></availability></publicationStmt><sourceDesc><biblStruct><monogr><editor>Emil '
       'Kroymann</editor><title>Opera</title><imprint><pubPlace>Vienna</pubPlace><date>1906</date>'
       '</imprint></monogr></biblStruct></sourceDesc></fileDesc></teiHeader><text><body>'
       '<div type="edition" xml:lang="lat"><div type="textpart" subtype="preface"><p>Praefatio.</p></div>'
       '<div type="textpart" subtype="chapter" n="1"><p>Felix sacramentum aquae nostrae.</p></div>'
       '</div></body></text></TEI>')
os.makedirs(os.path.join(_gd, "csel"), exist_ok=True)
_csp = os.path.join(_gd, "csel", "tertullian-de-baptismo-lat.xml")
open(_csp, "w", encoding="utf-8").write(_CS)
_csb = st.convert_tei_prose(_csp, "tertullian-de-baptismo-lat", "Tert. Bapt.")
check("csel: a Latin edition, its rights read from the file, the OCR caveat in honesty",
      _csb["source"]["language"] == "lat" and _csb["source"]["edition"]["date"] == "1906"
      and "The Latin text is a public-domain printed edition (Emil Kroymann" in _csb["rights"]["note"]
      and _csb["rights"]["source_url"].endswith("OpenGreekAndLatin/csel-dev")
      and "NOT proofread" in _csb["scheme"]["honesty"] and ".." not in _csb["scheme"]["honesty"])
check("csel: an unnumbered part is named by its subtype; a mislabelled title is fixed by slug",
      [u["id"].split(":")[1] for u in _csb["units"]] == ["preface", "1"]
      and _csb["title"] == "De Baptismo" and "latin_letters" not in str(_csb["units"]))
# A catena (Cramer): kephalaia, margin verse numbers, a lemma that runs on
# over a second mark, a page-line <lb n> left unplaced, a misprinted margin
# placed by the measured file, an unplaced kephalaion, and a placement file
# that no longer fits the source.
_CT = ('<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title>Cat</title>'
       '</titleStmt><sourceDesc><biblStruct><monogr><title>Catenae</title><imprint><date>1840</date>'
       '</imprint></monogr></biblStruct></sourceDesc></fileDesc></teiHeader><text><body>'
       '<div type="edition" xml:lang="grc">'
       '<div type="textpart" subtype="chapter" n="1"><head>ΚΕΦ. Α.</head><p>Περὶ μάγων.</p>'
       '<note type="marginal">1</note><p>Τοῦ δὲ Ἰησοῦ <note type="marginal">2</note>γεννηθέντος.</p>'
       '<p>Χρυσοστόμου. ὅτι ἦλθον.</p><lb n="5"/><p>Ὠριγένους. οὐκ.</p>'
       '<note type="marginal">9</note><p>Καὶ ἰδοὺ.</p>'
       '</div><div type="textpart" subtype="chapter" n="2"><note type="marginal">1</note>'
       '<p>Ἐν δὲ ταῖς ἡμέραις.</p></div>'
       '<div type="textpart" subtype="chapter" n="3"><head>ΚΕΦ. Γ.</head><p>Λόγος.</p></div>'
       '</div></body></text></TEI>')
_cp = os.path.join(_gd, "first1k", "cat.xml")
open(_cp, "w", encoding="utf-8").write(_CT)
_cj = os.path.join(_gd, "cat.json")


def _cat_placed(placed):
    _json.dump({"honesty": "h", "placed": placed}, open(_cj, "w", encoding="utf-8"))


_saved_cd = st.CATENA_DIR
st.CATENA["cat"] = ("Cat. Matt.", "Matt", "MAT")
st.CATENA_DIR, st.CORPUS = _gd, _gd
_cm = [(i["ord"], i["k"], i["n"], i["src"]) for i in st.catena_marks(
    st.tei_load(_cp).find(f".//{st.TEI_NS}body")) if i["kind"] == "mark"]
_cat_placed([{"ord": 0, "k": "1", "n": "1", "src": "margin", "chapter": 2, "verse": 1, "score": 0.9},
             {"ord": 2, "k": "1", "n": "9", "src": "margin", "chapter": 2, "verse": 3, "score": 0.2},
             {"ord": 3, "k": "2", "n": "1", "src": "margin", "chapter": 3, "verse": 1, "score": 1.0}])
_cb = st.convert_catena(_cp, "cat")
_cu = {u["id"].split(":")[1]: u for u in _cb["units"]}
_cat_placed([{"ord": 2, "k": "1", "n": "5", "src": "margin", "chapter": 2, "verse": 5, "score": 1.0}])
try:
    st.convert_catena(_cp, "cat"); _cbad = False
except ValueError:
    _cbad = True
del st.CATENA["cat"]
st.CATENA_DIR, st.CORPUS = _saved_cd, _saved[0]
check("catena: candidates are margin numbers and bare <lb n>; a mark inside the lemma is not one",
      _cm == [(0, "1", "1", "margin"), (1, "1", "5", "lb"), (2, "1", "9", "margin"),
              (3, "2", "1", "margin")])
check("catena: a placed mark is its chapter.verse; a mark inside the lemma makes a range",
      list(_cu) == ["2.1-2", "2.3", "3.1", "k3"]
      and [l["target"] for l in _cu["2.1-2"]["links"]] == ["kjv:Matt.2.1", "kjv:Matt.2.2"])
check("catena: the heading and title before the first mark ride on the first unit",
      _cu["2.1-2"]["apparatus"]["head"] == ["ΚΕΦ. Α.", "Περὶ μάγων."]
      and _cu["2.1-2"]["text"] == "Τοῦ δὲ Ἰησοῦ γεννηθέντος. Χρυσοστόμου. ὅτι ἦλθον. Ὠριγένους. οὐκ.")
check("catena: a misprinted margin is placed by the file, its printed number kept; weak below 0.3",
      _cu["2.3"]["milestones"] == {"kephalaion": "1", "margin": "9"}
      and _cu["2.3"]["links"][0]["match"] == "weak")
check("catena: an unplaced kephalaion is one unlinked unit; a file that no longer fits fails",
      _cu["k3"]["links"] == [] and _cbad)
_pc = load("place_catena")
_nt = {1: {1: {"αλφα", "βητα", "γαμμα"}, 5: {"δελτα", "εψιλον", "ζητα"}},
       2: {1: {"ηλιος", "θαλασσα", "ιωτα"}, 2: {"καππα", "λαμβδα", "μυ"}}}
_pg = _pc.place([(0, "1", "1", "margin", {"αλφα", "βητα", "γαμμα"}),
                 (1, "1", "5", "lb", {"ουδεν", "αλλο", "τουτο"}),
                 (2, "2", "1", "margin", {"ηλιος", "θαλασσα", "ιωτα"}),
                 (3, "2", "9", "margin", {"καππα", "λαμβδα", "μυ"})], _nt)
check("place_catena: chapters advance; a page-line <lb> is left out; a wrong margin is read by its lemma",
      _pg == {0: (1, 1, 1.0), 2: (2, 1, 1.0), 3: (2, 2, 1.0)})
_pg2 = _pc.place([(0, "1", "1", "lb", {"αλφα", "βητα", "γαμμα"}),
                  (1, "1", "5", "lb", {"δελτα", "εψιλον", "ζητα"}),
                  (2, "2", "2", "lb", {"ουδεν", "αλλο", "τουτο"})], _nt)
check("place_catena: a bare number not a multiple of 5 is a printed verse; a multiple of 5 must earn it",
      _pg2 == {0: (1, 1, 1.0), 1: (1, 5, 1.0), 2: (2, 2, 0.0)})
_ct2 = st.ET.fromstring('<body xmlns="http://www.tei-c.org/ns/1.0"><div subtype="chapter" n="sup1">'
                        '<lb n="7"/><p>α</p></div><div subtype="chapter" n="1"><lb n="7"/><p>β</p>'
                        '</div></body>')
check("catena: numbers in the supplement, contents or index are never verse candidates",
      [i["k"] for i in st.catena_marks(_ct2) if i["kind"] == "mark"] == ["1"])
check("place_catena: two shared words are not a 100% match for a two-word lemma",
      _pc.score({"αλφα", "βητα"}, {"αλφα", "βητα", "γαμμα", "δελτα"}) < 0.7)
_bt, _br, _bf = st.tei_brackets("ὑψηλῷ [cf. Deut., v, 45]· εὐ[fol. 51]δαιμονίαν [καὶ] [ΙS., II, 2] τε [?]")
check("fathers: bracketed references and folios lifted; Greek supplements stay",
      _bt == "ὑψηλῷ· εὐδαιμονίαν [καὶ] τε [?]" and _br == ["cf. Deut., v, 45", "ΙS., II, 2"]
      and _bf == ["51"])

print(f"\n{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
