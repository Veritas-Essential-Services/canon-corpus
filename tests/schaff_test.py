#!/usr/bin/env python3
"""tests/schaff_test.py -- build_schaff.py on inline fixtures (no corpus needed),
then, if the books are built, the committed manifest entries.

    python3 tests/schaff_test.py
"""
import json
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import build_schaff as B  # noqa: E402

passed = failed = 0


def check(name, ok):
    global passed, failed
    if ok:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}")


HEAD = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright Christian Classics Ethereal Library -->
<ThML><ThML.head><electronicEdInfo><status>Carefully proofed</status><DC>
<DC.Title>ANF01. Fixture</DC.Title><DC.Rights>{rights}</DC.Rights></DC></electronicEdInfo>
<printSourceInfo><published>Edinburgh: T&amp;T Clark</published></printSourceInfo></ThML.head>
<ThML.body>"""

BODY = """
<div1 id="i" title="Title Page"><p id="i-p1">Front matter.</p></div1>
<div1 id="ii" title="JUSTIN">
 <div2 id="ii.i" title="The First Apology">
  <p id="ii.i-p0">Unnumbered introduction.</p>
  <div3 id="ii.i.i" n="i" title="Chapter I.&#8212;Address.">
   <pb n="163" id="pb1"/>
   <p id="ii.i.i-p1">To the Emperor<note n="5" id="ii.i.i-p1.1" place="end"><p id="ii.i.i-p2">See <scripRef osisRef="Bible:Rom.13.1" parsed="|Rom|13|1|0|0">Rom. xiii. 1</scripRef>.</p></note> Titus.</p>
   <p id="ii.i.i-p3">Second <pb n="164" id="pb2"/> paragraph<br/>after a break, <scripRef osisRef="Bible:John.1.1 Bible:John.1.2">John i. 1, 2</scripRef>.</p>
  </div3>
  <div3 id="ii.i.ii" type="Chapter" n="I" title="Justice demanded."><p id="ii.i.ii-p1">Chapter one by type.</p></div3>
  <div3 id="ii.i.iii" type="Chapter" title="No number given."><p id="ii.i.iii-p1">Chapter two, inferred.</p></div3>
  <div3 id="ii.i.iv" title="An untyped chapter between."><p id="ii.i.iv-p1">Chapter three, sandwiched.</p></div3>
  <div3 id="ii.i.v" type="Chapter" title="Last."><p id="ii.i.v-p1">Chapter four.</p></div3>
  <div3 id="ii.i.vi" title="Elucidation."><p id="ii.i.vi-p1">After the run.</p></div3>
 </div2>
 <div2 id="ii.ii" title="Who is the Rich Man">
  <p id="ii.ii-p1">I. First chapter.</p>
  <p id="ii.ii-p2">continues.</p>
  <p id="ii.ii-p3">II. Second.</p>
  <p id="ii.ii-p4">IV. Fourth, the third numeral missing.</p>
  <p id="ii.ii-p5">X. A stray numeral is not a chapter.</p>
  <verse id="ii.ii-v1"><l>a line</l><l>another</l></verse>
 </div2>
</div1>
<div1 id="iii" title="Indexes"><div2 id="iii.i" title="Index of Scripture References"><p id="iii.i-p1">Gen 1:1</p></div2></div1>
</ThML.body></ThML>"""


def fixture(rights="Public Domain"):
    return (HEAD.format(rights=rights) + BODY).encode("utf-8")


units, divs, info, skipped = B.read_volume(fixture(), "anf01")
B.fill_numbers(divs)
by = {u["id"].split(":", 1)[1]: u for u in units}

check("unit id is CCEL's paragraph id, prefixed by the volume slug", "ii.i.i-p1" in by
      and units[0]["id"] == "schaff-anf01:i-p1")
check("footnote lifted out of the text, kept in notes with its number",
      by["ii.i.i-p1"]["text"] == "To the Emperor Titus."
      and by["ii.i.i-p1"]["notes"][0]["n"] == "5"
      and "Rom. xiii. 1" in by["ii.i.i-p1"]["notes"][0]["text"])
check("a note's own <p> is not a unit", "ii.i.i-p2" not in by)
check("scripture harvested from text and notes (convert_thml's regexes); one osisRef, two refs",
      by["ii.i.i-p1"]["links"] == ["Rom.13.1"]
      and by["ii.i.i-p3"]["links"] == ["John.1.1", "John.1.2"])
check("print page from the <pb> before; page_end when a <pb> falls inside",
      by["ii.i.i-p1"]["page"] == "163" and "page_end" not in by["ii.i.i-p1"]
      and by["ii.i.i-p3"]["page"] == "163" and by["ii.i.i-p3"]["page_end"] == "164")
check("<br> is a space", "paragraph after a break" in by["ii.i.i-p3"]["text"])
check("a stanza keeps its lines", by["ii.ii-v1"]["text"] == "a line\nanother")
check("CCEL's generated Indexes left out and counted",
      "iii.i-p1" not in by and skipped["generated_index_divs"] == 1)
check("the rights line is read: DC.Rights recorded as read", info["rights"] == ["Public Domain"])
try:
    B.read_volume(fixture("Copyright 2004"), "anf01")
    check("a file whose DC.Rights is not Public Domain stops the build", False)
except SystemExit:
    check("a file whose DC.Rights is not Public Domain stops the build", True)

check("numbers: title 'Chapter I.--' -> 1; type+n -> 1",
      divs["ii.i.i"]["number"] == 1 and divs["ii.i.ii"]["number"] == 1)
check("numbers: a typed run numbered only at its head is filled in order, inferred",
      divs["ii.i.iii"]["number"] == 2 and divs["ii.i.iii"].get("number_inferred"))
check("numbers: an untyped division inside the run is part of it; one after it is not",
      divs["ii.i.iv"]["number"] == 3 and divs["ii.i.v"]["number"] == 4
      and divs["ii.i.vi"]["number"] is None)
check("roman(): roman and arabic, junk is None",
      B.roman("XLIV") == 44 and B.roman("12") == 12 and B.roman("Against") is None)
check("div_number: 'Book First' is 1, 'Letter XXII. To Eustochium' is 22, a preface is None",
      B.div_number(ET.Element("div2", {"title": "Book First.—Visions"})) == 1
      and B.div_number(ET.Element("div2", {"title": "Letter XXII. To Eustochium"})) == 22
      and B.div_number(ET.Element("div2", {"title": "Preface."})) is None)

ch, out, spans = B.work_chapters(divs, units, "ii.ii", "inline")
check("inline: numerals opening paragraphs, in sequence; one missing numeral spans",
      list(ch) == ["1", "2", "4"] and spans == {"2": ["3"]}
      and ch["1"] == ["schaff-anf01:ii.ii-p1", "schaff-anf01:ii.ii-p2"])
check("inline: a stray numeral out of sequence is not a chapter", "10" not in ch
      and "schaff-anf01:ii.ii-p5" in ch["4"])

# a counterpart with the same numbering, and one shifted by a chapter
vb = {"slug": "schaff-anf01", "divs": divs, "units": units,
      "source": {"path": "schaff/anf01.xml", "url": "u", "sha256": "s"}, "rights": {"x": 1}}
w = {"slug": "fixture-schaff", "vol": "anf01", "div": "ii.ii", "levels": "inline",
     "counterpart": "fixture-grc", "level_names": "chapter", "abbrev": "Fix.", "title": "t",
     "author": "a"}
cp = {"units": [{"id": "fixture-grc:1.1", "text": "x" * 30}, {"id": "fixture-grc:1.2", "text": "y"},
                {"id": "fixture-grc:2", "text": "z" * 7}, {"id": "fixture-grc:3", "text": "q"},
                {"id": "fixture-grc:4", "text": "w" * 40}]}
wb = B.build_work(w, vb, cp)
u1 = wb["units"][0]
check("too few chapters to measure but every unit paired both ways -> kept as 'unmeasured'",
      wb["alignment"]["verdict"] == "unmeasured" and wb["alignment"]["measure"]["one_to_one"])
check("work unit links every counterpart section of its chapter (1 -> 1.1, 1.2)",
      [x["target"] for x in u1["links"]] == ["fixture-grc:1.1", "fixture-grc:1.2"])
check("work unit names its volume paragraphs and keeps no copy of the notes",
      u1["paragraphs"] == ["schaff-anf01:ii.ii-p1", "schaff-anf01:ii.ii-p2"] and "notes" not in u1)
check("a spanning unit links both chapters",
      [x["target"] for x in wb["units"][1]["links"]] == ["fixture-grc:2", "fixture-grc:3"]
      and wb["units"][1]["spans"] == ["2", "3"])
cp["units"].append({"id": "fixture-grc:praef", "text": "p"})
wb = B.build_work(w, vb, cp)
check("too few to measure and a counterpart unit unpaired -> refused, no links, listed",
      wb["alignment"]["verdict"] == "refused" and not any(u["links"] for u in wb["units"])
      and "praef" in wb["alignment"]["counterpart_unmatched"])

m = B.measure(list("abcdef"), dict(zip("abcdef", [10, 100, 30, 300, 50, 500])),
              dict(zip("abcdef", [12, 110, 33, 290, 60, 480])))
check("measure: matching lengths on the diagonal -> aligned", B.verdict(m) == "aligned")
m = B.measure(list("abcdef"), dict(zip("abcdef", [10, 100, 30, 300, 50, 500])),
              dict(zip("abcdef", [480, 12, 110, 33, 290, 60])))
check("measure: lengths that fit one chapter off -> refused", B.verdict(m) == "refused")
check("name_key spells Greek, Latin and English alike",
      B.name_key("Κωνσταντῖνος") == B.name_key("Constantine") == B.name_key("Constantinus"))

# ---------------------------------------------------------------- the committed record
with open(os.path.join(ROOT, "data", "books", "manifest.json"), encoding="utf-8") as f:
    man = json.load(f)
vols = [k for k in man if k.startswith("schaff-")]
if not vols:
    print(f"\n{passed} passed, {failed} failed (manifest has no Schaff entries yet: run build_schaff.py)")
    sys.exit(1 if failed else 0)
check("38 volume entries in the manifest", len(vols) == 38)
check("every volume's rights block: PD as read, CCEL's non-commercial request, no whole redistribution",
      all(man[k]["rights"]["rights_line_as_read"]["DC.Rights"] == "Public Domain"
          and man[k]["rights"]["redistribute_whole"] is False
          and "non-profit" in man[k]["rights"]["ccel_policy"]["text"] for k in vols))
check("ANF 10 is the facsimile: 0 units, and its scheme says why",
      man["schaff-anf10"]["units"] == 0 and "facsimile" in man["schaff-anf10"]["scheme"]["honesty"])
works = {k: v for k, v in man.items() if k.endswith("-schaff")}
check("every work entry has an alignment block with a verdict or a no-counterpart note",
      works and all("verdict" in v["alignment"] or v["alignment"].get("note") for v in works.values()))
check("a refused work carries no matched units",
      all(v["alignment"]["matched"] == 0 for v in works.values()
          if v["alignment"].get("verdict") == "refused"))
cy = [k for k in works if k.startswith("cyprian-")]
check("Cyprian is here as a work set, and says it has no Latin counterpart",
      len(cy) >= 4 and all(works[k]["alignment"]["counterpart"] is None
                           and "CSEL 3" in works[k]["alignment"]["note"] for k in cy))
check("pins cover the 38 volumes", sorted(B.pins()) == sorted(B.VOLUMES))

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
