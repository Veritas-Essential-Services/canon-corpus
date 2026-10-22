#!/usr/bin/env python3
# prov: 2026-07-22 claude-fable-5 drafted (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-06 claude-opus-5 edited (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-07 claude-opus-5 edited (from git trailer; backfilled 2026-09-30)
# prov: 2026-10-19 claude-opus-5-5 edited
# prov: 2026-10-20 claude-opus-5-5 edited (Aphthonius converter checks)
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

# A Christmas Carol (2026-10-16): the stave headings become clean ids and refs,
# the Contents and the title page are not text, and the default id rule (the
# Chesterton shelf above) is untouched. Fixture is invented text in PG 46's shape.
_CAR = ("A CHRISTMAS CAROL\n\nby Charles Dickens\n\n\nPREFACE\n\nI HAVE endeavoured.\n\nC. D.\n\n\n"
        "CONTENTS\n\nStave   I: Marley's Ghost\nStave  II: The First of the Three Spirits\n\n\n"
        "STAVE I:  MARLEY'S GHOST\n\nMARLEY was dead.\n\nMind!\n\n"
        "STAVE II:  THE FIRST OF THE THREE SPIRITS\n\nWhen Scrooge awoke.\n\n"
        "End of the Project Gutenberg EBook of A Christmas Carol\n")
with _tf.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _fh:
    _fh.write(_CAR)
_saved_corpus = st.CORPUS
st.CORPUS = os.path.dirname(_fh.name)
_cb = st.convert_gutenberg_prose(_fh.name, "dickens-carol", *st.GUTEN_PROSE["dickens-carol"])
st.CORPUS = _saved_corpus
os.unlink(_fh.name)
check("carol: staves are clean ids, titled refs, no Contents or title page",
      [(u["id"], u["ref"]) for u in _cb["units"]] == [
          ("dickens-carol:preface.1", "Preface, par. 1"), ("dickens-carol:preface.2", "Preface, par. 2"),
          ("dickens-carol:stave1.1", "Stave I: Marley's Ghost, par. 1"),
          ("dickens-carol:stave1.2", "Stave I: Marley's Ghost, par. 2"),
          ("dickens-carol:stave2.1", "Stave II: The First of the Three Spirits, par. 1")])
check("carol: the default division ids are unchanged for every other book",
      [u["id"] for u in _eb["units"]] == ["t:On_Lamps.1", "t:On_Lamps.2", "t:The_Mock_Goose.1"])

# G. A. Henty (2026-10-16): a two-paragraph heading ("CHAPTER I." / "A TITLE.") becomes one titled
# division; the Contents (after the Preface in one book, before it in the other) is not text; the
# Preface is kept. Fixtures are invented text in the two PG files' shapes.
def _prose(slug, body):
    global _fh
    with _tf.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _fh:
        _fh.write(body)
    saved = st.CORPUS; st.CORPUS = os.path.dirname(_fh.name)
    try:
        return st.convert_gutenberg_prose(_fh.name, slug, *st.GUTEN_PROSE[slug])
    finally:
        st.CORPUS = saved; os.unlink(_fh.name)
_hb = _prose("henty-bubastes", "TITLE PAGE\n\nPREFACE.\n\nMy dear lads, a letter.\n\nYours, G. A. H.\n\n\nCONTENTS.\n\n\n"
             " CHAPTER I.                   PAGE\n The First Thing                7\n\n CHAPTER II.\n The Second    26\n\n\n"
             "CHAPTER I.\n\nTHE FIRST THING.\n\nA paragraph.\n\nAnother.\n\nCHAPTER II.\n\nHOME AT LAST.\n\nThe end came.\n\nTHE END.\n\nAfter.\n")
check("henty: preface kept, Contents gone, two-line headings become titled chapters",
      [(u["id"], u["ref"]) for u in _hb["units"]] == [
          ("henty-bubastes:preface.1", "Preface, par. 1"), ("henty-bubastes:preface.2", "Preface, par. 2"),
          ("henty-bubastes:ch1.1", "Chapter I: The First Thing, par. 1"), ("henty-bubastes:ch1.2", "Chapter I: The First Thing, par. 2"),
          ("henty-bubastes:ch2.1", "Chapter II: Home at Last, par. 1")])
_hf = _prose("henty-freedom", "CONTENTS\n\n   I  Glen One\n  II  Glen Two\n\n\nPREFACE.\n\nMy dear lads.\n\n\n"
             "Chapter I\n\nGlen One\n\n\nFirst words.\n\nChapter II\n\nThe King's Blood Hound\n\nMore words.\n\nTHE END\n")
check("henty: title-case headings too; a Contents before the Preface is cut",
      [(u["id"], u["ref"]) for u in _hf["units"]] == [
          ("henty-freedom:preface.1", "Preface, par. 1"), ("henty-freedom:ch1.1", "Chapter I: Glen One, par. 1"),
          ("henty-freedom:ch2.1", "Chapter II: The King's Blood Hound, par. 1")])

# Alfred J. Church from archive.org OCR (2026-10-16): page furniture goes, headings repeated on the
# half-title and plate pages open a chapter only once, a page break's cut paragraph is rejoined, a
# word broken at the margin is mended, a short last line ends a paragraph, unnumbered sections open
# by name, and a heading's speck is trimmed. Invented text in the scans' shape.
_OCR = ("TITLE  PAGE\n\nCONTENTS\n\nI.  THE  FIRST  .  .  15\n\n"
        "CHAPTER    I\nTHE    FIRST    TALE\n\n\nCHAPTER    I\nTHE    FIRST    TALE\n\n\n"
        "THE    BOOK    FOR    BOYS\nAND    GIRLS\n\n\nCHAPTER    I\n\nTHE    FIRST    TALE   *\n\n"
        "There  was  a  long  line  of  ships  upon  the\nshore  and  they  wept.\n"
        "Then  the  king  spoke  to  them  all  and  he\nsaid  that  the  ships  must  go  over  the\n\n15\n\n\n"
        "THE  BOOK  FOR  BOYS  AND  GIRLS\n\nj  j\n\nsea  to  the  far  and  distant  coun-\n"
        "try  of  the  Trojans  and  so  they  all  did.\n\n"
        "16\n\n\nTHE   FIRST   TALE\n\nThey  came  home  at  the  last  and  were  safe\nand  sound.\n\n"
        "CHAPTER    II\n\nOF    PHCENIX\n\nA  second  tale  begins  here  and  goes  on.\n\n"
        "THE  END  OF  TROY\n\nTHE  END  OF  TROY\n\nThe  last  words  are  these.\n")
with _tf.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _fh:
    _fh.write(_OCR)
_saved_corpus = st.CORPUS; st.CORPUS = os.path.dirname(_fh.name)
_ob = st.convert_archive_ocr_prose(_fh.name, "t", "T", "A", "x", ("THE END OF TROY",), {"Phcenix": "Phoenix"})
st.CORPUS = _saved_corpus; os.unlink(_fh.name)
check("ocr: chapters once each, titled, specks trimmed, heading fixed, unnumbered section by name",
      [(u["id"], u["ref"]) for u in _ob["units"]] == [
          ("t:ch1.1", "Chapter I: The First Tale, par. 1"), ("t:ch1.2", "Chapter I: The First Tale, par. 2"),
          ("t:ch1.3", "Chapter I: The First Tale, par. 3"),
          ("t:ch2.1", "Chapter II: Of Phoenix, par. 1"), ("t:the-end-of-troy.1", "The End of Troy, par. 1")])
check("ocr: a short last line ends a paragraph; running heads, page numbers and specks are gone",
      _ob["units"][0]["text"] == "There was a long line of ships upon the shore and they wept."
      and _ob["units"][1]["text"].startswith("Then the king"))
check("ocr: a paragraph cut by a page break is one paragraph, and a word broken at the margin is mended",
      _ob["units"][1]["text"].endswith("go over the sea to the far and distant country of the Trojans and so they all did."))
check("ocr: the book says it is unproofread OCR", "UNPROOFREAD OCR" in _ob["scheme"]["honesty"])

# ---------------------------------------------------------------- the Unscanner's reading of a scan
_UN = {"slug": "t", "title": "T", "author": "A", "source": {"format": "unscanner", "font_match": "X"},
       "scheme": {"apparatus": "a", "citation": "chapter + paragraph", "resolution": "paragraph",
                  "honesty": "UNPROOFREAD OCR (tesseract) of a library scan"},
       "units": [{"id": "t:ch1.1", "ref": "Chapter I: Of Things, par. 1", "text": "Once.", "links": [],
                  "pages": [21, 22], "printed": ["15", "16"]}]}
with _tf.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as _fh:
    _json.dump(_UN, _fh)
_saved_corpus = st.CORPUS; st.CORPUS = os.path.dirname(_fh.name)
_ub = st.convert_unscanned(_fh.name, "t", "T", "A", "x")
st.CORPUS = _saved_corpus; os.unlink(_fh.name)
check("unscanned: units, their scan pages and printed labels, and the Unscanner's honesty carried through",
      _ub["units"][0]["printed"] == ["15", "16"] and _ub["units"][0]["id"] == "t:ch1.1"
      and _ub["source"]["format"] == "unscanner" and "UNPROOFREAD" in _ub["scheme"]["honesty"])

# ---------------------------------------------------------------- Aphthonius, three editions (2026-10-20)
# Invented fixtures only: placeholder words, never a line of any edition.
_KEYS = [k for k, _ in st.PROGYM_EXERCISES]
_FILL = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do"

def _hocr(pages):
    out = ["<html><body>"]
    for lines in pages:
        out.append("<div class='ocr_page' title='bbox 0 0 1000 1500'><p class='ocr_par'>")
        for (x0, y0, xs, text) in lines:
            ws = "".join(f"<span class='ocrx_word' title='bbox 0 0 1 1'>{w}</span> " for w in text.split())
            out.append(f"<span class='ocr_line' title='bbox {x0} {y0} {x0 + 500} {y0 + 30}; x_size {xs}'>{ws}</span>")
        out.append("</p></div>")
    return "\n".join(out + ["</body></html>"])

def _rabe_page(head, heading, text, app=True):
    L = [] if head is None else [(300, 100, 23, head)]
    y = 160
    if heading:
        L.append((300, y, 31, heading)); y += 50
    for t in text:
        L.append((100, y, 30, t)); y += 36
    L.append((800, y - 36, 30, "5"))                 # Rabe's line number in the right margin
    if app:
        y += 60
        for k in range(4):
            L.append((100, y, 24, f"{k + 3} ΑΒ 12 ΓΔ 3")); y += 25
    return L

_rp = [[] for _ in range(st.RABE_PAGE_OFFSET + 2)]          # scan pages before the text
_rp[-1] = [(200, 40, 48, "ΑΦΘΟΝΙΟΥ ΣΟΦΙΣΤΟΥ"), (200, 90, 48, "ΠΡΟΓΥΜΝΑΣΜΑΤΑ")] + \
    _rabe_page(None, "Ι. ΠΕΡΙ ΜΥΘΟΥ", ["αλφα βητα γαμμα δελ-", "τα εψιλον ζητα."])
for n, k in enumerate(_KEYS[1:], 2):
    _rp.append(_rabe_page(f"ΠΡΟΓΥΜΝΑΣΜΑΤΑ (Ι) {n}", "ΧΙ. «ΠΕΡΙ ΤΙΝΟΣ.", ["ηθος καππα λαμβδα.", "μυ νυ ξι ομικρον."]))
with _tf.NamedTemporaryFile("w", suffix=".hocr.html", delete=False, encoding="utf-8") as _fh:
    _fh.write(_hocr(_rp))
_saved_corpus = st.CORPUS; st.CORPUS = os.path.dirname(_fh.name)
_gb = st.convert_rabe_hocr(_fh.name, "g", "G", "A", "x")
_rp[-1] = _rabe_page("ΠΡΟΓΥΜΝΑΣΜΑΤΑ (Ι) 14", None, ["ηθος καππα."])       # the law's heading lost
with open(_fh.name, "w", encoding="utf-8") as _f2:
    _f2.write(_hocr(_rp))
try:
    st.convert_rabe_hocr(_fh.name, "g", "G", "A", "x"); _miss = False
except ValueError:
    _miss = True
st.CORPUS = _saved_corpus; os.unlink(_fh.name)
_g = {u["id"]: u for u in _gb["units"]}
check("rabe: fourteen exercises in order, one unit per exercise per Rabe page",
      [u["id"] for u in _gb["units"]][:3] == ["g:fable.1", "g:narrative.2", "g:chreia.3"]
      and len(_gb["units"]) == 14 and _gb["units"][-1]["id"] == "g:law.14")
check("rabe: the apparatus, running head, title and margin numbers are dropped; a broken word is mended",
      _g["g:fable.1"]["text"] == "αλφα βητα γαμμα δελτα εψιλον ζητα." and "ΑΒ" not in _g["g:narrative.2"]["text"]
      and "apparatus dropped by rule (56 lines)" in _gb["scheme"]["apparatus"])
check("rabe: a citation resolves to Rabe's page, and says so", _g["g:chreia.3"]["ref"] == "Chreia, Rabe p. 3"
      and _g["g:chreia.3"]["page"] == 3 and "never the line" in _gb["scheme"]["honesty"])
check("rabe: a missing heading fails the build", _miss)

def _djvu(pages):
    out = ["<DjVuXML><BODY>"]
    for lines in pages:
        out.append('<OBJECT data="x" type="image/x.djvu">')
        for (x0, y0, text) in lines:
            ws, x = [], x0
            for w in text.split():
                ws.append(f'<WORD coords="{x},{y0 + 40},{x + 20 * len(w)},{y0}">{w}</WORD>'); x += 20 * len(w) + 15
            out.append("<LINE>" + " ".join(ws) + "</LINE>")
        out.append("</OBJECT>")
    return "\n".join(out + ["</BODY></DjVuXML>"])

_AH = ["Fabula.", "Narratio. II.", "Chria, fiue vfus. III.", "Sententia.", "Defirudio fiue fubuerfio. V.",
       "Confirmatio fiue affeueratio. VI.", "Locus communis. VII.", "Laus. VIII.", "Vituperatio. IX.",
       "Comparatio. X.", "Ethopoeia. XI.", "Deferiptio. XII.", "Thefis. XIII.", "Legillatio. XIIII."]
_ap = [[(300, 300, "Fabula"), (300, 400, "Sententia")]]                            # the Censura's table
for n, h in enumerate(_AH):
    page = [(240, 400, _FILL), (240, 480, _FILL + " vnum."), (300, 560, _FILL + " duo"),
            (1700, 560, "Nota."), (240, 640, _FILL), (400, 20, "APHTHONII SOPHISTAE")]
    page.append((700, 320, h))
    if n == 0:                                   # the title, set after the text in the file's own order
        page.append((500, 200, "Rodolpho Agricola interprete."))
    _ap.append(page)
_ap.append([(240, 300, "AVTOR INNOMINATVS DE"), (240, 400, _FILL)])
with _tf.NamedTemporaryFile("w", suffix=".djvu.xml", delete=False, encoding="utf-8") as _fh:
    _fh.write(_djvu(_ap))
_saved_corpus = st.CORPUS; st.CORPUS = os.path.dirname(_fh.name)
_lb = st.convert_agricola_djvu(_fh.name, "l", "L", "A", "x")
st.CORPUS = _saved_corpus; os.unlink(_fh.name)
_l = {u["id"]: u for u in _lb["units"]}
check("agricola: lines in reading order; the Censura skipped; fourteen exercises from misread headings",
      [i for i in _l if i.endswith(".1")] == [f"l:{k}.1" for k in _KEYS] + ["l:appendix.1"])
check("agricola: an indent opens a paragraph; side-notes and running heads dropped",
      _l["l:fable.1"]["text"] == _FILL + " " + _FILL + " vnum." and _l["l:fable.2"]["text"].startswith(_FILL + " duo")
      and "Nota" not in _l["l:fable.2"]["text"] and "APHTHONII" not in _l["l:law.2"]["text"]
      and "side-notes (14 lines)" in _lb["scheme"]["apparatus"])

_RN = ["*** START OF THE PROJECT GUTENBERG EBOOK X ***", "", "¶ A booke cal-", "led x.", "",
       "¶ _To the right honorable and my singuler good Lorde,_", "", "Dedication words here.", "",
       "¶ _The contentes of_", "", "A list.", "", "[Fol. j.r]", "", "Introduction words",
       "[Sidenote: A note", "over two lines]", "go on here.", ""]
for k, h, nth in st.RAINOLDE_HEADS:
    if k == "comparison":
        _RN += ["¶ A comparison.", "", "Inside the dispraise.", ""]
    _RN += [h, "", f"Body of the {k}.", "", "¶ The praise.", "", "More words.", ""]
_RN += ["       *       *       *       *       *", "", "Errata.", "*** END OF THE PROJECT GUTENBERG EBOOK X ***"]
with _tf.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _fh:
    _fh.write("\n".join(_RN))
_saved_corpus = st.CORPUS; st.CORPUS = os.path.dirname(_fh.name)
_eb = st.convert_rainolde(_fh.name, "r", "R", "A")
st.CORPUS = _saved_corpus; os.unlink(_fh.name)
_e = {u["id"]: u for u in _eb["units"]}
check("rainolde: front matter kept without the title page or contents; side-notes and folios gone",
      [u["text"] for u in _eb["units"] if u["id"].startswith("r:front.")] ==
      ["¶ _To the right honorable and my singuler good Lorde,_", "Dedication words here.",
       "Introduction words go on here."])
check("rainolde: the exercise opens at the named occurrence of its heading, sub-headings are their own units",
      _e["r:comparison.2"]["text"] == "Body of the comparison." and _e["r:comparison.3"].get("heading")
      and "Inside the dispraise." in [_e[i]["text"] for i in _e if i.startswith("r:invective.")]
      and _e["r:law.2"]["text"] == "Body of the law." and "Errata." not in [u["text"] for u in _eb["units"]])
# ---------------------------------------------------------------- Brewer (1894)
# Fixture shaped like extract_brewer.py's output. Every line is a case the
# live build met (2026-10-19), written fresh -- not Brewer's text.
_BR = {"source_sha256": "x", "pages": 3, "toc": [["A", 1], ["B", 3]], "furniture_lines": 0,
       "paras": [
    {"p": 1, "top": True, "lines": ["A"]},
    {"p": 1, "top": False, "lines": ["The first letter."]},
    {"p": 1, "top": False, "lines": ["A.B"]},
    {"p": 1, "top": False, "lines": ["(See Abel.)"]},
    {"p": 1, "top": False, "lines": ["Abel"]},
    {"p": 1, "top": False, "lines": ["A shepherd (Gen. iv. 2——4). Also Psalm cliv. 1, and", "Kings vi. 2."]},
    {"p": 1, "top": False, "lines": ["Fresh as a morning breeze in spring"]},
    {"p": 2, "top": True, "lines": ["and so continued over the page."]},
    {"p": 2, "top": False, "lines": ["Cato was so called. (B.C. 234.)"]},
    {"p": 2, "top": False, "lines": ["Acorns"]},
    {"p": 2, "top": False, "lines": ["Oak fruit. (See above.) (See under Abels.)"]},
    {"p": 2, "top": False, "lines": ["Acre"]},
    {"p": 3, "top": True, "lines": ["Bacon"]},
    {"p": 3, "top": False, "lines": ["Bring home the bacon. 1 Sam. ii. 3."]},
    {"p": 3, "top": False, "lines": ["Bacon"]},
    {"p": 3, "top": False, "lines": ["The philosopher."]}]}
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as _fb:
    _json.dump(_BR, _fb)
_sc = st.CORPUS; st.CORPUS = os.path.dirname(_fb.name)
_bb = st.convert_brewer(_fb.name); st.CORPUS = _sc; os.unlink(_fb.name)
_bu = {u["id"]: u for u in _bb["units"]}
check("brewer: headwords found; abbreviation (no full stop) kept; verse line and sentence are not headwords",
      [u["id"] for u in _bb["units"]] == ["brewer:a", "brewer:a-b", "brewer:abel", "brewer:acorns",
                                          "brewer:bacon", "brewer:bacon"])
check("brewer: a missed line stays in the entry before it -- nothing lost",
      "Fresh as a morning breeze" in _bu["brewer:abel"]["text"]
      and "Cato was so called" in _bu["brewer:abel"]["text"])
check("brewer: page-top paragraph rejoined to an unfinished one; entry spans both pages",
      "spring and so continued" in _bu["brewer:abel"]["text"] and _bu["brewer:abel"]["lex"]["pages"] == [1, 2])
check("brewer: a bodiless headword ('Acre') is folded back as text, not a unit",
      "brewer:acre" not in _bu and _bu["brewer:acorns"]["text"].endswith("Acre"))
_sl = [l for l in _bu["brewer:abel"]["links"] if l["kind"] == "scripture"]
check("brewer: scripture parsed (range kept as end); Psalm 154 and number-less Kings refused",
      [(l["target"], l.get("end")) for l in _sl] == [("kjv:Gen.4.2", "Gen.4.4")]
      and "Gen. iv. 2–4" in _bu["brewer:abel"]["text"])
check("brewer: numbered book takes its number (1 Sam. -> 1Sam)",
      any(l.get("target") == "kjv:1Sam.2.3" for l in _bb["units"][4]["links"]))
check("brewer: 'See X' resolves (also 'under', plural); 'see above' is not a link",
      _bu["brewer:a-b"]["links"] == [{"kind": "see", "target": "brewer:abel"}]
      and _bu["brewer:acorns"]["links"] == [{"kind": "see", "target": "brewer:abel"}])
check("brewer: honesty says segmented by rule, misses kept in text",
      _bb["scheme"]["resolution"] == "entry" and "segmented by rule" in _bb["scheme"]["honesty"])

# The shipped copy of a local source (2026-10-19): a fresh clone has no PDF,
# so fetch_sources unpacks data/lexicons/<x>.gz -- and refuses a wrong one.
import gzip as _gz, hashlib as _hl
fs = load("fetch_sources")
_td = tempfile.mkdtemp()
_raw = b'{"paras":[]}'
with _gz.open(os.path.join(_td, "s.gz"), "wb") as _g: _g.write(_raw)
_spec = ("x", "recipe", "lexicons/out.json", "s.gz", _hl.sha256(_raw).hexdigest(), "n")
_c = os.path.join(_td, "corpus")
_r1 = fs.unpack_local(_spec, corpus=_c, root=_td)
check("local source: shipped copy unpacked byte-for-byte, then left alone",
      open(os.path.join(_c, "lexicons/out.json"), "rb").read() == _raw and "sha256 checked" in _r1
      and fs.unpack_local(_spec, corpus=_c, root=_td) == "present")
os.unlink(os.path.join(_c, "lexicons/out.json"))
try:
    fs.unpack_local(_spec[:4] + ("0" * 64, "n"), corpus=_c, root=_td); _refused = False
except RuntimeError:
    _refused = True
check("local source: a shipped copy that is not the pinned bytes is refused",
      _refused and not os.path.exists(os.path.join(_c, "lexicons/out.json")))
check("local source: brewer's pins are declared (source PDF + unpacked paragraphs)",
      len(fs.LOCAL_SOURCES["brewer"][0]) == 64 and len(fs.LOCAL_SOURCES["brewer"][4]) == 64
      and fs.LOCAL_SOURCES["brewer"][3].startswith("data/lexicons/"))

check("shipped working text: both Church Homers declared, pinned, shipped copies present",
      all(len(fs.SHIPPED_WORKING_TEXT[x][4]) == 64 and os.path.exists(os.path.join(HERE, "..", fs.SHIPPED_WORKING_TEXT[x][3]))
          for x in ("church-iliad-boys", "church-odyssey-boys")))

print(f"\n{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
