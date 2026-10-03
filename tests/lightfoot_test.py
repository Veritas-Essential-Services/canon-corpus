#!/usr/bin/env python3
"""
lightfoot_test.py -- the validator for Lightfoot & Harmer's English Apostolic
Fathers (pipeline/build_lightfoot.py; CCEL ThML, aligned to Lake's Greek).

    python3 tests/lightfoot_test.py

OFFLINE (always): the committed manifest entries (rights block, counts, the
alignment's own measurements), the pin, and the rules on fixtures: reading a
ThML piece (indent, footnote, verse block), Lake's chapter of a section id,
cutting a Hermas part into chapters, the length alignment (it must pair what
the lengths show and refuse to cut what they do not), and unit keys.

AGAINST THE PINNED FILE (when data/corpus/lightfoot/ holds it and Lake's books
are built): a rebuild equals every committed manifest entry, and known
passages sit where Lake prints them.
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "pipeline"))
import build_lightfoot as L  # noqa: E402
import build_apostolic_fathers as A  # noqa: E402
import fetch_sources as FS  # noqa: E402

PASS = FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"ok   {label}")
    else:
        FAIL += 1
        print(f"FAIL {label}  {detail}")


EXPECTED = {  # slug: (units, Greek sections, by section, in a run, by chapter)
    "1clement-lightfoot": (379, 400, 359, 41, 0), "2clement-lightfoot": (114, 118, 111, 7, 0),
    "ignatius-lightfoot": (198, 205, 191, 6, 8), "polycarp-phil-lightfoot": (38, 38, 38, 0, 0),
    "martyrdom-polycarp-lightfoot": (56, 59, 54, 5, 0), "didache-lightfoot": (100, 100, 100, 0, 0),
    "barnabas-lightfoot": (191, 194, 188, 6, 0), "hermas-lightfoot": (704, 727, 684, 43, 0),
    "diognetus-lightfoot": (96, 100, 94, 6, 0),
}

# ================================================================ OFFLINE
print("--- manifest")
man = json.load(open(L.MANIFEST, encoding="utf-8"))
slugs = [w[0].replace("-lake", "-lightfoot") for w in A.WORKS]
check("nine English books, one per Greek book of Lake's set", sorted(slugs) == sorted(EXPECTED))
check("each has a committed manifest entry", all(s in man for s in slugs), [s for s in slugs if s not in man])
ents = {s: man.get(s, {}) for s in slugs}
check("rights: PD, the file's own lines recorded (DC.Rights, CCEL's copyright comment, "
      "no non-commercial term), not served whole",
      all(e.get("rights", {}).get("redistribute_whole") is False
          and e["rights"]["license"] == "public-domain"
          and "Public Domain" in e["rights"]["note"]
          and "Copyright Christian Classics Ethereal Library" in e["rights"]["note"]
          and "no non-commercial condition" in e["rights"]["note"]
          and e["rights"].get("commercial") == "ask CCEL"
          and "non-profit" in e["rights"]["ccel_policy"]["text"]
          and e["rights"]["source_url"] == FS.LIGHTFOOT["url"] for e in ents.values()))
check("every entry names the pinned file (sha256 = fetch_sources.LIGHTFOOT)",
      all(e.get("sha256") == FS.LIGHTFOOT["sha256"] for e in ents.values()))
got = {s: (e.get("units"), e.get("alignment", {}).get("lake_sections"),
           *(e.get("alignment", {}).get("sections_reached", {}).get(k) for k in ("section", "range", "chapter")))
       for s, e in ents.items()}
check("units and resolutions are the expected ones", got == EXPECTED,
      {s: g for s, g in got.items() if g != EXPECTED.get(s)})
check("every Greek section is reached by some English unit (none unreached)",
      all(e["alignment"]["lake_sections_unreached"] == [] for e in ents.values()))
greek_counts = {w[0].replace("-lake", "-lightfoot"): man.get(w[0], {}).get("units") for w in A.WORKS}
check("the Greek sections counted are Lake's own manifest counts",
      all(e["alignment"]["lake_sections"] == greek_counts[s] for s, e in ents.items()))
lt = [sum(e["alignment"]["length_test"][k][i] for e in ents.values())
      for k in ("pairs_within_x1.5", "control_shifted_by_one") for i in (0, 1)]
check(f"length test: >= 95% of 1:1 pairs within x1.5 ({lt[0]}/{lt[1]}), control <= 70% ({lt[2]}/{lt[3]})",
      lt[0] / lt[1] >= 0.95 and lt[2] / lt[3] <= 0.70)
nm = [sum(e["alignment"]["name_test"][k][i] for e in ents.values())
      for k in ("names_in_linked_greek", "control_next_unit") for i in (0, 1)]
check(f"name test: >= 90% of English names in the linked Greek ({nm[0]}/{nm[1]}), "
      f"control <= 40% ({nm[2]}/{nm[3]})", nm[0] / nm[1] >= 0.90 and nm[2] / nm[3] <= 0.40)
check("every entry records the built book's sha256 (the book itself is gitignored)",
      all(re.fullmatch(r"[0-9a-f]{64}", e.get("built_sha256", "")) for e in ents.values()))
check("honesty says section boundaries are approximate and what is only by run or chapter",
      all("approximate" in e["scheme"]["honesty"] and "only by chapter" in e["scheme"]["honesty"]
          for e in ents.values()))
check("Hermas records how each of its 27 parts was cut into chapters",
      len(ents["hermas-lightfoot"]["alignment"].get("hermas_parts", {})) == 27)
check("the books are gitignored, never committed",
      "data/books/*.json" in open(os.path.join(REPO, ".gitignore"), encoding="utf-8").read())
check("the source lands outside data/corpus/ccel/ (structure_texts.py must not build it twice)",
      "/ccel/" not in L.SRC.replace(os.sep, "/"))

print("--- reading ThML (fixtures)")
div = ET.fromstring(
    '<div2 id="x"><h2 id="a">1 Clem. 1</h2>'
    '<p id="p1">\n   By reason of the sudden calamities\n<br /><br />\n</p>'
    '<p id="p2">\nFor who <note place="foot" id="n" n="1">A footnote.</note>did not approve'
    ' <scripRef osisRef="Bible:Rom.8.13" passage="Rom 8:13">x</scripRef></p>'
    '<verse id="v"><l id="l1">  O Lord God,  </l><l id="l2">the Father</l></verse></div2>')
ps = L.pieces(div)
check("a heading is a head", ps[0][:2] == ("head", "1 Clem. 1"))
check("an indented first paragraph is marked (it opens a chapter)", ps[1][2] is True and ps[2][2] is False)
check("text is whitespace-normalised", ps[1][1] == "By reason of the sudden calamities")
check("a footnote leaves the text and is kept apart", ps[2][1] == "For who did not approve x"
      and ps[2][3] == ["A footnote."], ps[2])
check("scripRefs are harvested from the piece", ps[2][4] == ["Bible:Rom.8.13"])
check("a verse block is one piece, its lines kept", ps[3][1] == "O Lord God,\nthe Father" and ps[3][5] == "verse")

print("--- Lake's chapters")
check("chapter_of: section -> chapter", L.chapter_of("4.7") == "4" and L.chapter_of("Vis.3.1.2") == "Vis.3.1"
      and L.chapter_of("Eph.praef.1") == "Eph.praef")
check("chapter_of: a unit with no section is its own chapter",
      L.chapter_of("praef") == "praef" and L.chapter_of("praef.sal") == "praef.sal")


def piece(n, indent=False, text=None):
    return ("piece", text or "x" * n, indent, [], [], "p")


lake = {"Vis.2.1": [("Vis.2.1.1", "", ""), ("Vis.2.1.2", "", "")],
        "Vis.2.2": [("Vis.2.2.1", "", ""), ("Vis.2.2.2", "", ""), ("Vis.2.2.3", "", "")]}
# five pieces, three indents: the extra indent (piece 2) is not a chapter start
items = [piece(1, True), piece(1), piece(1, True), piece(1, True), piece(1)]
cut, how = L.hermas_chapters("Vis.2", "Vision 2", items, lake)
check("Hermas: Lake's chapter starts, corroborated by indents, beat an extra indent",
      how == "lake-starts-on-indents" and [len(c[2]) for c in cut] == [2, 3], (how, [len(c[2]) for c in cut]))
items = [piece(1, True), piece(1), piece(1, True), piece(1)]
cut, how = L.hermas_chapters("Vis.2", "Vision 2", items, lake)
check("Hermas: counts differ, indents = chapters -> the indents cut", how == "indents"
      and [len(c[2]) for c in cut] == [2, 2])
items = [piece(1, True), piece(1), piece(1), piece(1, True), piece(1, True), piece(1, True)]
cut, how = L.hermas_chapters("Vis.2", "Vision 2", items, lake)
check("Hermas: neither holds -> the part is one unit, not a guess", how == "part" and len(cut) == 1)

print("--- the length alignment (fixtures)")
pen = 12.0
b, _, _ = L.blocks([100, 200, 300], [100, 200, 300], 1.0, 0.1, pen)
check("equal counts, lengths agree -> one unit per section", b == [(0, 1, 0, 1), (1, 2, 1, 2), (2, 3, 2, 3)], b)
b, _, _ = L.blocks([100, 500, 300], [100, 200, 300, 300], 1.0, 0.1, pen)
check("one piece twice its section's length -> it takes two sections",
      b == [(0, 1, 0, 1), (1, 2, 1, 3), (2, 3, 3, 4)], b)
b, _, _ = L.blocks([100, 100, 100], [150, 150], 1.0, 0.1, pen)
check("no way to tell which pieces share a section -> one block, never a guess", b == [(0, 3, 0, 2)], b)
check("penalty is the prior read off the counts", abs(L.penalty(
    [("s", "1", "", [piece(1)] * 9, [0] * 10)])[0] - 2 * __import__("math").log(0.9 / (0.1 / 5))) < 1e-9)

print("--- unit keys")
secs = [("5.5", "g", "1 Clem. 5.5"), ("5.6", "g", "1 Clem. 5.6")]
u = L.make_unit("1clement-lightfoot", "1clement-lake", "5", "1 Clem. 5", [piece(3, text="abc")], secs, False)
check("a run of sections is keyed by its range and links to each", u["id"] == "1clement-lightfoot:5.5-6"
      and u["ref"] == "1 Clem. 5.5-6 (Lightfoot)"
      and [x["target"] for x in u["links"]] == ["1clement-lake:5.5", "1clement-lake:5.6"]
      and all(x["align"] == "range" and x["type"] == "original" for x in u["links"]), u)
u = L.make_unit("didache-lightfoot", "didache-lake", "9", "Did. 9", [piece(3, text="abc")],
                [("9.1", "", "Did. 9.1"), ("9.2", "", "Did. 9.2")], True)
check("a whole chapter is keyed by the chapter", u["id"] == "didache-lightfoot:9" and u["ref"] == "Did. 9 (Lightfoot)"
      and u["lex"]["align"] == "chapter")
u = L.make_unit("ignatius-lightfoot", "ignatius-lake", "Eph.1", "IgnEph. 1", [piece(3, text="abc")],
                [("Eph.1.1", "", "Ign. Eph. 1.1")], False)
check("one section: keyed by Lake's section id", u["id"] == "ignatius-lightfoot:Eph.1.1"
      and u["lex"] == {"lightfoot": "IgnEph. 1", "pieces": 1, "align": "section"})

# ================================================================ AGAINST THE PINNED FILE
have = os.path.exists(L.SRC) and all(os.path.exists(os.path.join(L.BOOKS, w[0] + ".json")) for w in A.WORKS)
if not have:
    print("\nskip  the pinned ThML or Lake's books are missing (build_apostolic_fathers.py --fetch; "
          "build_lightfoot.py --fetch); the rebuild checks did not run")
else:
    print("--- against the pinned file")
    built, measured, rows = L.build()
    check("a rebuild = every committed manifest entry (built_sha256)",
          all(man.get(s) == e for s, (_, _, e) in built.items()),
          [s for s, (_, _, e) in built.items() if man.get(s) != e])
    units = {u["id"]: u for b, _, _ in built.values() for u in b["units"]}
    for uid, words in [
        ("1clement-lightfoot:5.4", "Peter"),
        ("1clement-lightfoot:4.12", "Dathan and Abiram"),
        ("ignatius-lightfoot:Rom.4.1", "of my own free will I die for God"),
        ("hermas-lightfoot:Vis.1.1.1", "Rhoda"),
        ("hermas-lightfoot:Sim.9.1.1", "angel of repentance"),
        ("didache-lightfoot:9.4", "broken bread was scattered upon the mountains"),
        ("diognetus-lightfoot:5.5", "sojourners"),
    ]:
        check(f"{uid} holds what Lake's section holds ({words!r})", words in units.get(uid, {}).get("text", ""))
    ep = [u for u in units.values() if u["id"].startswith("martyrdom-polycarp-lightfoot:epilogus_alius")]
    check("the Moscow epilogue is under Lake's epilogus_alius, with Lightfoot's footnote",
          ep and any("Moscow" in n for u in ep for n in u["lex"].get("notes", [])))
    check("no unit text is empty, and no id repeats",
          all(u["text"] for u in units.values()) and len(units) == sum(len(b["units"]) for b, _, _ in built.values()))
    check("the one scripRef in the file is on a heading (Hermas 'Revelation 5') and is not harvested",
          [h["heading"] for h in measured["heading_scripRefs_not_harvested"]] == ["Revelation 5"]
          and not any(x.get("source") == "ccel-scripRef" for u in units.values() for x in u["links"]))

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
