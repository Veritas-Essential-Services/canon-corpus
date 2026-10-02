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
import os, sys, json, shutil, tempfile, importlib.util

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
           '<ref ref="Gen 24:12" b="1" cBegin="24" vBegin="12">Gen 24:12</ref> '
           '<ref ref="Ps 51:3" b="19" cBegin="51" vBegin="3">Ps 51:3</ref> '
           '<ref ref="Ps 51:1" b="19" cBegin="51" vBegin="1">Ps 51:1</ref> '
           '<ref ref="Mal 4:1" b="39" cBegin="4" vBegin="1">Mal 4:1</ref></p>\n'
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
check("bdb: scripture ref keeps the book number's OSIS as stated, in Hebrew numbering",
      scr and scr[0]["osis"] == "Gen.24.12" and scr[0]["versification"] == "bhs")
check("bdb: a verse numbered alike in both schemes resolves to its kjv: unit id",
      scr[0]["resolved"] is True and scr[0]["target"] == "kjv:Gen.24.12")
check("bdb: Hebrew Ps 51:3 resolves to KJV Ps 51:1, the stated osis untouched",
      scr[1]["osis"] == "Ps.51.3" and scr[1]["target"] == "kjv:Ps.51.1")
check("bdb: Hebrew Ps 51:1 is the KJV's unnumbered title -- unresolved, and says why",
      scr[2]["resolved"] is False and "title" in scr[2]["why"] and "target" not in scr[2])
check("bdb: a reference naming no Hebrew verse stays unresolved (Mal has 3 chapters in Hebrew)",
      scr[3]["osis"] == "Mal.4.1" and scr[3]["resolved"] is False and "target" not in scr[3])
check("bdb: an entry with no Strong's number gets no strongs link",
      [l for l in bd["units"][1]["links"] if l["kind"] == "strongs"] == [])
os.unlink(bdb_path)

# ---------------------------------------------------------------- Vulgate
vd = tempfile.mkdtemp()
with open(os.path.join(vd, "Ps.lat"), "w", encoding="cp1252", newline="\r\n") as f:
    f.write("50:1 In finem. Psalmus David,\\\n"
            "50:3 [Miserere mei, Deus,/ secundum magnam misericordiam tuam;]\n")
with open(os.path.join(vd, "Ct.lat"), "w", encoding="cp1252", newline="\r\n") as f:
    f.write("1:1 [<Sponsa>Osculetur me osculo oris sui:/ quia meliora sunt ubera tua vino,]\n"
            "\n"
            "1:2 et c\u0153li.\n")
vg = st.convert_vulgate(vd, ["Ps", "Ct"], "pin")
vu = {u["id"]: u for u in vg["units"]}
check("vulgate: ids are the Vulgate's own numbering on OSIS books (Ps 50 stays 50)",
      list(vu) == ["vulgate:Ps.50.1", "vulgate:Ps.50.3", "vulgate:Song.1.1", "vulgate:Song.1.2"])
check("vulgate: '/' becomes a line break, brackets and the paragraph mark go",
      vu["vulgate:Ps.50.3"]["text"] == "Miserere mei, Deus,\nsecundum magnam misericordiam tuam;"
      and vu["vulgate:Ps.50.1"]["text"] == "In finem. Psalmus David,")
check("vulgate: the marked line is kept as the file has it",
      vu["vulgate:Ps.50.1"]["marked"] == "In finem. Psalmus David,\\")
check("vulgate: a speaker heading is lifted out of the text",
      vu["vulgate:Song.1.1"]["speakers"] == ["Sponsa"]
      and vu["vulgate:Song.1.1"]["text"].startswith("Osculetur"))
check("vulgate: read as cp1252 (the oe ligature survives)", "œ" in vu["vulgate:Song.1.2"]["text"])
check("vulgate: scheme says Vulgate numbering; ids are not rewritten, links[] stays empty",
      vg["scheme"]["versification"] == "vulgate"
      and not any(u["links"] for u in vg["units"]))
check("vulgate: each unit's `kjv` names the KJV verse by the committed map (Ps 50:3 = KJV 51:1)",
      vu["vulgate:Ps.50.3"]["kjv"] == {"resolved": True, "target": "kjv:Ps.51.1"}
      and vu["vulgate:Song.1.1"]["kjv"] == {"resolved": True, "target": "kjv:Song.1.2"})
check("vulgate: a psalm title is not resolved, and says where it is in the KJV",
      vu["vulgate:Ps.50.1"]["kjv"]["resolved"] is False
      and vu["vulgate:Ps.50.1"]["kjv"]["kjv"] == ["Ps.51.title"])
check("vulgate: the scheme counts resolved and unresolved units",
      vg["scheme"]["kjv_resolved"] == 3 and vg["scheme"]["kjv_unresolved"] == 1)
check("vulgate: the rights block travels with the book",
      vg["rights"]["license"] == "public-domain" and "Clementine" in vg["rights"]["attribution"])
shutil.rmtree(vd)

# ---------------------------------------------------------------- Douay-Rheims
dd = tempfile.mkdtemp()
_books = [{"name": n, "chapters": []} for n in st.DOUAY_NAMES]
_books[20]["chapters"] = [{"chapter": 50, "verses": [
    {"verse": 3, "text": "Have mercy on me, O God,  according to thy great mercy."}]}]
_books[58]["chapters"] = [{"chapter": 4, "verses": [
    {"verse": 12, "text": "And we will not have you ignorant brethren, concerning them that are asleep"},
    {"verse": 18, "text": ""}]}]
_books.append({"name": "I Esdras", "chapters": [{"chapter": 1, "verses": [{"verse": 1, "text": "x"}]}]})
with open(os.path.join(dd, "DRC.json"), "w", encoding="utf-8") as f:
    json.dump({"books": _books}, f)
_vb = ["Gn Ex Lv Nm Dt Jos Jdc Rt 1Rg 2Rg 3Rg 4Rg 1Par 2Par Esr Neh Tob Jdt Est Job Ps Pr Ecl Ct "
       "Sap Sir Is Jr Lam Bar Ez Dn Os Joel Am Abd Jon Mch Nah Hab Soph Agg Zach Mal 1Mcc 2Mcc Mt "
       "Mc Lc Jo Act Rom 1Cor 2Cor Gal Eph Phlp Col 1Thes 2Thes 1Tim 2Tim Tit Phlm Hbr Jac 1Ptr "
       "2Ptr 1Jo 2Jo 3Jo Jud Apc"][0].split()
dg = st.convert_douay(os.path.join(dd, "DRC.json"), _vb, "pin")
du = {u["id"]: u for u in dg["units"]}
check("douay: ids in the Vulgate's numbering; an empty padding verse gets no id; appendix not read",
      list(du) == ["douay:Ps.50.3", "douay:1Thess.4.12"] and dg["scheme"]["empty_verses_dropped"] == 1)
check("douay: whitespace runs collapse", du["douay:Ps.50.3"]["text"].count("  ") == 0)
check("douay: the same number reads the same Clementine verse, and the KJV through the map",
      du["douay:Ps.50.3"]["vulgate"] == ["vulgate:Ps.50.3"]
      and du["douay:Ps.50.3"]["kjv"] == {"resolved": True, "target": "kjv:Ps.51.1"})
check("douay: DOUAY_ROWS carries the Douay's own breaks (1 Thess 4:12 is the Clementine's 4:13)",
      du["douay:1Thess.4.12"]["vulgate"] == ["vulgate:1Thess.4.13"]
      and du["douay:1Thess.4.12"]["kjv"]["target"] == "kjv:1Thess.4.13")
_books[20]["chapters"][0]["verses"][0]["verse"] = 99
_books[0]["name"] = "Genesys"
with open(os.path.join(dd, "DRC.json"), "w", encoding="utf-8") as f:
    json.dump({"books": _books}, f)
try:
    st.convert_douay(os.path.join(dd, "DRC.json"), _vb, "pin"); _ok = False
except ValueError:
    _ok = True
check("douay: a file whose books are not in the pinned order is refused", _ok)
shutil.rmtree(dd)

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

# Brenton's English Septuagint (eBible USFM in a zip). Fixture is invented
# text in eBible's markup; the kjv fields come from the committed map.
import zipfile as _zf
_bz = os.path.join(_tf.mkdtemp(), "eng-Brenton_usfm.zip")
with _zf.ZipFile(_bz, "w") as _z:
    _z.writestr("19-PSAeng-Brenton.usfm",
                "\\id PSA - Brenton\n\\h Psalms \n\\c 50  \n\\d\n\\v 1 For the end, a Psalm,  \n"
                "\\v 2 when Nathan came.   \n\\p\n\\v 3 \\sc Have\\sc* mercy \\f + \\fr 50:3 "
                "\\fqa Gr. \\ft pity.\\f*upon me.  \n")
    _z.writestr("18-NEHeng-Brenton.usfm", "\\id NEH\n\\h Nehemiah\n\\c 1\n\\v 1 skipped\n")
    _z.writestr("27-LAMeng-Brenton.usfm",
                "\\id LAM\n\\h Lamentations \n\\c 1  \n\\p [And it came to pass, and said]  \n"
                "\\p\n\\v 1 \\sc Aleph.\\sc* How does the city sit solitary!   \n")
    _z.writestr("12-1KIeng-Brenton.usfm",
                "\\id 1KI\n\\h 3 Kingdoms\n\\c 12\n\\v 24a And king Solomon slept.\n")
_bb = st.convert_brenton(_bz, "pin")
_bu = {u["id"]: u for u in _bb["units"]}
check("brenton: ids are Brenton's own numbering (Ps 50 stays 50, a lettered verse keeps its "
      "letter, the text before Lam 1:1 is verse 0); eBible's KJV-numbered NEH is not read",
      list(_bu) == ["brenton:1Kgs.12.24a", "brenton:Ps.50.1", "brenton:Ps.50.2",
                    "brenton:Ps.50.3", "brenton:Lam.1.0", "brenton:Lam.1.1"])
check("brenton: notes leave the text for `notes`; character markers go; `marked` is as is",
      _bu["brenton:Ps.50.3"]["text"] == "Have mercy upon me."
      and "pity" in _bu["brenton:Ps.50.3"]["notes"][0]
      and _bu["brenton:Ps.50.3"]["marked"].startswith("\\sc Have"))
check("brenton: each unit's `kjv` comes from the committed map (Ps 50:3 = KJV 51:1)",
      _bu["brenton:Ps.50.3"]["kjv"] == {"resolved": True, "target": "kjv:Ps.51.1"}
      and _bu["brenton:Ps.50.1"]["kjv"]["kjv"] == ["Ps.51.title"]
      and _bu["brenton:1Kgs.12.24a"]["kjv"]["resolved"] is False
      and _bu["brenton:Lam.1.0"]["kjv"]["resolved"] is False)
check("brenton: scheme and rights say what the book is",
      _bb["scheme"]["versification"] == "lxx-brenton"
      and _bb["rights"]["license"] == "public-domain")

# The historic English Bibles (scrollmapper JSON on CrossWire's KJV grid).
# Fixture is invented text in the source's shape: 66 books, two verses.
_ej = {"books": [{"name": f"Book{i}", "chapters": []} for i in range(66)]}
_ej["books"][0] = {"name": "Genesis", "chapters": [{"chapter": 1, "verses": [
    {"verse": 1, "chapter": 1, "name": "Genesis 1:1", "text": "In the beginningGod made it."},
    {"verse": 2, "chapter": 1, "name": "Genesis 1:2", "text": "  "}]}]}
_ej["books"][49] = {"name": "Philippians", "chapters": [{"chapter": 1, "verses": [
    {"verse": 16, "chapter": 1, "name": "Philippians 1:16", "text": "the one do it of love,"}]}]}
_ep = os.path.join(_tf.mkdtemp(), "Darby.json")
with open(_ep, "w", encoding="utf-8") as _fh:
    json.dump(_ej, _fh)
_eb = st.convert_english(_ep, "darby", "pin")
_eu = {u["id"]: u for u in _eb["units"]}
check("english: ids are the source's slots on OSIS books; an empty slot is no unit",
      list(_eu) == ["darby:Gen.1.1", "darby:Phil.1.16"] and _eb["scheme"]["empty_slots_not_units"] == 1)
check("english: Darby's per-book rule restores the space the markup ate before 'God'",
      _eu["darby:Gen.1.1"]["text"] == "In the beginning God made it."
      and _eb["scheme"]["rules"][0]["applied"] == 1)
check("english: each unit's `kjv` comes from the committed map (Darby Phil 1:16 is KJV 1:17)",
      _eu["darby:Phil.1.16"]["kjv"] == {"resolved": True, "target": "kjv:Phil.1.17"}
      and _eu["darby:Gen.1.1"]["kjv"] == {"resolved": True, "target": "kjv:Gen.1.1"})
check("english: rights say public domain and carry the source's own rights line",
      _eb["rights"]["license"] == "public-domain" and "Public Domain" in _eb["rights"]["rights_line"])

print(f"\n{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
