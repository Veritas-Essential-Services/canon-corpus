#!/usr/bin/env python3
# prov: 2026-10-03 drafted (Claude Code)
# fable_review: pending
"""wycliffe_test.py -- the Forshall and Madden reader (pipeline/build_wycliffe.py).
Offline fixtures; the rebuild checks run only when the pinned hOCR and the
built books are present."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import build_wycliffe as W  # noqa: E402

passed = failed = 0


def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}")


def line(words, xs=47.0):
    """A column line from (x0, x1, text) words."""
    ws = [(x0, 100, x1, 140, 90, t) for x0, x1, t in words]
    return {"bbox": (ws[0][0], 100, ws[-1][2], 140), "xs": xs, "words": ws, "text": " ".join(w[5] for w in ws)}


# -- Roman numerals as the OCR prints them
check("roman: clean", W.roman("XLII.") == 42 and W.roman("CXLIX") == 149)
check("roman: OCR's lower case and l/1 for I", W.roman("xvii") == 17 and W.roman("XIl.") == 12 and W.roman("1V") == 4)
check("roman: not a numeral", W.roman("CAP") is None and W.roman("") is None)
check("roman_cost: exact 0, unreadable 1, wrong 1.5",
      (W.roman_cost(6, "VI."), W.roman_cost(6, "Vq"), W.roman_cost(6, "VII")) == (0, 1.0, 1.5))

# -- margin figures (each misreading met in Genesis 1-6)
check("readings: digits", W.readings("12") == {12})
check("readings: 's' is 5 or 8 (Gen 1.5 'sand', 1.8 'sis')", W.readings("s") == {5, 8})
check("readings: 'IG' is 16, 'u' 11, 'H' 14 or 11", W.readings("IG") == {16} and W.readings("u") == {11}
      and W.readings("H") == {14, 11})
check("readings: a word is not a figure", W.readings("the") == set() and W.readings("Lord") == set())
check("fuzzy: exact 0, one reading 0.4, ambiguous 0.6, one digit off 0.7, else 1",
      (W.fuzzy(12, "12"), W.fuzzy(16, "IG"), W.fuzzy(5, "s"), W.fuzzy(38, "33"), W.fuzzy(5, "the"))
      == (0, 0.4, 0.6, 0.7, 1.0))

# -- headings and rubrics
check("heading: CAP. and PSALM", W.HEADING.match("CAP. XVI.").group(1).strip() == "XVI."
      and W.HEADING.match("PSALM CXLIX.").group(1).strip() == "CXLIX.")
check("heading: a verse line is not one", W.HEADING.match("Cam, and Japheth.") is None)
check("rubric: the opening and closing rubrics", bool(W.RUBRIC.search("Here bigynneth the book of Josue"))
      and bool(W.RUBRIC.search("Here endith Genesis")) and not W.RUBRIC.search("And God seide"))

# -- running heads
H = [{"bbox": (400, 180, 600, 215), "text": "XVII. 24 — XVIII. 10."}, {"bbox": (1100, 170, 1400, 210),
                                                                        "text": "GENESIS."}]
check("head_chapters: a range over two chapters", W.head_chapters(H) == (17, 18))
check("head_chapters: one chapter", W.head_chapters([{"bbox": (0, 0, 1, 1), "text": "i. 13 — 26. GENESIS."}])
      == (1, 1))
check("smooth: drops a head its neighbours contradict",
      sorted(W.smooth({1: (5, 5), 2: (5, 6), 3: (19, 19), 4: (6, 6), 5: (6, 7)})) == [1, 2, 4, 5])

# -- margins: the earlier version numbers its left margin, the later its right
e = 394
check("margin L: a figure beside the text edge",
      W.margin(line([(357, 380, "10"), (397, 480, "God"), (490, 560, "seide")]), "L", e, 50)[:2]
      == (["10"], "God seide"))
check("margin L: a figure run into the first word ('4Giauntis')",
      W.margin(line([(371, 590, "4Giauntis"), (600, 700, "forsothe")]), "L", e, 50)[:2]
      == (["4"], "Giauntis forsothe"))
check("margin L: a misread figure run into the word ('sand' = 5 and)",
      W.margin(line([(366, 470, "sand"), (480, 600, "clepide")]), "L", e, 50)[:2] == (["s"], "and clepide"))
check("margin L: a gloss far out in the margin is dropped, not read",
      W.margin(line([(232, 440, "confermeth"), (494, 600, "shal"), (610, 700, "be")]), "L", 494, 47)
      == ([], "shal be", [(232, 100, 440, 140, 90, "confermeth")]))
e = 2148
check("margin R: a figure after the text edge",
      W.margin(line([(2060, 2138, "and"), (2158, 2172, "2")]), "R", e, 50)[:2] == (["2"], "and"))
check("margin R: a figure run onto the last word ('derk-5')",
      W.margin(line([(1900, 2000, "the"), (2010, 2175, "derk-5")]), "R", e, 50)[:2] == (["5"], "the derk-"))
check("margin R: a gloss beyond the margin is dropped",
      W.margin(line([(2060, 2148, "erthe"), (2192, 2300, "Lyre")]), "R", e, 50)[:2] == ([], "erthe"))

# -- columns
body = []
for i in range(12):
    body.append(line([(394, 600, "a"), (610, 800, "b"), (810, 1000, "c"), (1010, 1220, "d")]))
    body.append(line([(1296, 1500, "e"), (1510, 1700, "f"), (1710, 1900, "g"), (1910, 2148, "h")]))
g = W.gutter(body, 2600)
check("gutter: the empty strip between the columns", g is not None and 1220 <= g[0] and g[1] <= 1300)
L, R = W.split_columns([line([(394, 700, "left"), (1114, 1389, "Eufraten;"), (1400, 1600, "right")])], (1335, 1390))
check("split: a word ABBYY stretched across the gutter stays in the left column",
      L[0]["text"] == "left Eufraten;" and R[0]["text"] == "right")

# -- decoding: margin numbers + headings -> (chapter, verse)
rows = [(1, "c", ["I."], "CAP. I."), (1, "t", [], "In the bigynnyng God made heuene and erthe."),
        (1, "m", ["2"], "The erthe was veyn."), (1, "m", ["s"], "And God seide."),
        (1, "m", ["4"], "And God sai3."), (1, "c", ["II."], "CAP. II."), (1, "t", [], "Therfor heuenes."),
        (1, "m", ["2"], "And God fillide.")]
a = W.decode(rows, {}, 2, {1: 4, 2: 3})
check("decode: headings open chapters, 's' after 2 is 3, a '2' after a heading is verse 2",
      [a[i][:2] for i in sorted(a)] == [(1, 0), (1, 2), (1, 3), (1, 4), (2, 0), (2, 2)])
units, stats = W.build_units(rows, a)
check("build_units: a chapter's first verse is the text after its heading",
      [(u["ch"], u["v"]) for u in units] == [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2)]
      and units[0]["num"] == "heading" and units[0]["text"].startswith("In the bigynnyng"))
rows2 = [(1, "c", ["I."], "CAP. I."), (1, "t", [], "a."), (1, "m", ["2"], "b. Here endith"),
         (1, "r", [], "Here endith Genesis, and here bigynneth"), (1, "t", [], "prologe of Exodus")]
u2, _ = W.build_units(rows2, W.decode(rows2, {}, 1, {1: 2}))
check("build_units: text after a closing rubric is not verse text", "prologe" not in u2[-1]["text"])
check("cut_beyond: II Paralipomenon XXXVII (the Prayer of Manasses) is not 2Chr",
      W.cut_beyond([(1, "m", ["2"], "x"), (2, "c", ["XXXVII."], "CAP. XXXVII."), (2, "t", [], "Lord")], 36)
      == ([(1, "m", ["2"], "x")], 2))

# -- the book table
codes = [b[0] for b in W.BOOKS]
vm = W.vulgate_map()
clem = []
for k in vm["vulgate_chapters"]:
    b = k.rsplit(".", 1)[0]
    if b not in clem:
        clem.append(b)
check("BOOKS: every Clementine book, once", sorted(codes) == sorted(clem) and len(codes) == 73)
check("BOOKS: leaves run forward in each volume",
      all(a <= b for _, _, a, b, _ in W.BOOKS))
check("VOLUMES: four pins", len(W.VOLUMES) == 4 and all(len(v["sha256"]) == 64 for v in W.VOLUMES.values()))

# -- the committed manifest entries
with open(W.MANIFEST, encoding="utf-8") as f:
    man = json.load(f)
for slug in ("wycliffe-earlier", "wycliffe-later"):
    e = man.get(slug)
    check(f"manifest: {slug} present", e is not None)
    if not e:
        continue
    check(f"manifest: {slug} rights read, public domain", "public domain" in e["rights"]["license"]
          and e["rights"]["redistribute_whole"] is True)
    check(f"manifest: {slug} says it is unproofread OCR", "unproofread OCR" in e["scheme"]["honesty"])
    t = e["measure"]["total"]
    check(f"manifest: {slug} measures coverage of the Clementine", t["clementine_verses"] == 35809
          and 0 < t["present"] <= t["clementine_verses"])
    check(f"manifest: {slug} every book measured", len(e["measure"]["books"]) == 73)

# -- the built books, when present
for slug in ("wycliffe-earlier", "wycliffe-later"):
    p = os.path.join(W.BOOKS_DIR, slug + ".json")
    if not os.path.exists(p):
        print(f"skip {slug}: not built")
        continue
    with open(p, "rb") as f:
        blob = f.read()
    import hashlib
    check(f"built {slug} = manifest built_sha256", hashlib.sha256(blob).hexdigest() == man[slug]["built_sha256"])
    bk = json.loads(blob)
    ids = [u["id"] for u in bk["units"]]
    check(f"built {slug}: ids unique", len(ids) == len(set(ids)))
    gen = {u["id"]: u for u in bk["units"] if u["id"].startswith(f"{slug}:Gen.1.")}
    check(f"built {slug}: Gen 1.1 is the creation", "heuene" in gen.get(f"{slug}:Gen.1.1", {}).get("text", ""))
    ps = next((u for u in bk["units"] if u["id"] == f"{slug}:Ps.50.3"), None)
    check(f"built {slug}: Ps 50.3 (Vulgate numbering) resolves to KJV Ps 51.1",
          ps is None or ps["kjv"].get("target") == "kjv:Ps.51.1")

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
