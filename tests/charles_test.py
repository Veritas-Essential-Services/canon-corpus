#!/usr/bin/env python3
"""charles_test.py -- the Charles 1913 reader (pipeline/charles_ocr.py,
pipeline/build_charles.py). Offline fixtures; the rebuild checks run only
when the pinned hOCR and the built books are present."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import charles_ocr as C  # noqa: E402
import build_charles as B  # noqa: E402

passed = failed = 0


def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}")


# -- numbers as the OCR prints them
check("num: digits as read", C.num("45") == 45)
check("num: letter-for-digit fixes on short tokens", C.num("Il") == 11 and C.num("ς") == 5 and C.num("to") == 10)
check("num: a word is not a number", C.num("the") is None and C.num("1l1l") is None)
check("fuzzy: exact 0, fixed 0.4, one digit off 0.7, else 1",
      (C.fuzzy_eq(12, "12"), C.fuzzy_eq(11, "Il"), C.fuzzy_eq(38, "33"), C.fuzzy_eq(5, "x")) == (0, 0.4, 0.7, 1.0))
check("alts: old-style 3 and 8 are confused", 13 in C.alts(18) and 18 in C.alts(13))

# -- running heads
check("head: chapter range", C.head_range("BOOK OF ENOCH 12. 5—14. 4") == (12, 5, 14, 4))
check("head: one chapter", C.head_range("SIRACH 4, 17-25") == (4, 17, 4, 25))
check("head: none", C.head_range("INTRODUCTION") is None)
check("head: Esther's letters", B.letter_head("THE ADDITIONS TO ESTHER. B5—C 5") == (2, 5, 3, 5))
check("head_ok: tolerates 3/8", C.head_ok((18, 1, 18, 5), 13) and not C.head_ok((12, 1, 12, 9), 15))
heads = {1: (5, 1, 5, 9), 2: (5, 10, 5, 20), 3: (19, 1, 19, 9), 4: (5, 21, 6, 2), 5: (6, 3, 6, 10)}
check("smooth_heads: drops a head its neighbours contradict", 3 not in C.smooth_heads(heads)
      and 4 in C.smooth_heads(heads))

# -- where a verse begins in its numbered line
check("verse_start: previous verse ended the line", C.verse_start("And he said", "the end.") == (0, "line-start"))
off, how = C.verse_start("whole world, and commanded me. And he", "the Lord of Israel, the most high")
check("verse_start: mid-line, at the sentence break", how == "sentence" and off > 0)
check("verse_start: no break: the line start, flagged", C.verse_start("and so on", "and") == (0, "line"))
check("verse_start: a clause ended at ';' opens the next line in lower case",
      C.verse_start("we shall go safe. And he said", "and fear thou not;") == (0, "line-start"))
check("join: a line-end hyphen joins a word", C.join("there-", "fore") == "therefore"
      and C.join("a", "b") == "a b")

# -- headings in the body are not verse text
check("is_heading: Charles's section heads", C.is_heading("V. 1-8. Victories of Judas over the Edomites")
      and C.is_heading("(b) IV. 20-28. Practical Precepts") and not C.is_heading("And Judas went"))


# -- apparatus that slipped past the type-size split
check("is_apparatus_text: a line of Greek sigla is apparatus",
      C.is_apparatus_text("(cum δ cf. δ) αἰιχμαλ. N*] +pe NCA N.] > BA καθοτι ΒᾺ et quoniam"))
check("is_apparatus_text: Charles's English is not",
      not C.is_apparatus_text("And whomsoever Sennacherib slew, when he had come fleeing from Judaea [in the days]"))

# -- the proofreading pass (pipeline/proof_charles.py)
import proof_charles as PC  # noqa: E402
check("proof: an OCR-typical edit finds the word", "modern" in PC.candidates("rnodern", {"modern", "model"})
      and "the" in PC.candidates("tbe", {"the"}))
check("proof: no candidate when none is a word", PC.candidates("xqzv", {"the"}) == [])


# -- one printed line the OCR cut in two
def ln(x0, y0, x1, y1, t):
    ws = t.split()
    return {"bbox": (x0, y0, x1, y1), "xs": 50.0, "text": t,
            "words": [(x0 + i, y0, x0 + i + 1, y1, 95, w) for i, w in enumerate(ws)]}


m = C.merge_rows([ln(346, 1275, 1507, 1328, "Then there assembled"), ln(217, 1281, 265, 1316, "28"),
                  ln(286, 1333, 1507, 1387, "inhabitants of the country")])
check("merge_rows: a margin number set lower than its line rejoins it",
      len(m) == 2 and m[0]["text"] == "28 Then there assembled")
m = C.merge_rows([ln(677, 864, 1514, 919, "Then Daniel took"), ln(223, 865, 613, 920, "27 granted thee.")])
check("merge_rows: a line split mid-way is read left to right",
      len(m) == 1 and m[0]["text"] == "27 granted thee. Then Daniel took")


# -- the decoder
def rows(spec):
    """spec: list of (leaf, token or None, tall)"""
    return [(lf, "m", [(t, tall)], f"text {i}") if t is not None else (lf, "t", [], f"text {i}")
            for i, (lf, t, tall) in enumerate(spec)]


r = rows([(1, "1", False), (1, "2", False), (1, "3", False), (1, "4", False)])
a = C.decode(r, {}, True)
check("decode: clean sequence", [a[i] for i in sorted(a)] == [(0, 1, 1), (0, 1, 2), (0, 1, 3), (0, 1, 4)])
r = rows([(1, "1", False), (1, "2", False), (1, "S", False), (1, "4", False), (1, "x?", False), (1, "6", False)])
a = C.decode(r, {}, True)
check("decode: OCR slips decoded from the sequence", [a[i][2] for i in sorted(a)] == [1, 2, 3, 4, 5, 6])
r = rows([(1, "1", False), (1, "2", False), (1, "4", False), (1, "5", False)])
a = C.decode(r, {}, True)
check("decode: a dropped marker is a gap, not a renumbering", [a[i][2] for i in sorted(a)] == [1, 2, 4, 5])
spec = [(1, str(i), False) for i in range(1, 30)] + [(2, "2", True), (2, "2", False), (2, "3", False), (2, "4", False)]
r = rows(spec)
a = C.decode(r, {1: (1, 1, 1, 29), 2: (1, 30, 2, 4)}, True)
got = [a[i] for i in sorted(a)][-4:]
check("decode: a bold chapter numeral starts the next chapter", got[0][1] == 2 and got[-1] == (0, 2, 4))
spec = [(1, str(i), False) for i in range(1, 12)] + [(2, "1", False), (2, "2", False), (2, "3", False)]
a = C.decode(rows(spec), {}, True, max_ch=1)
check("decode: max chapter is a hard limit", all(v[1] == 1 for v in a.values()))
spec = [(1, "1", False), (1, "2", False), (1, "3", False), (1, "4", False), (1, "5", False), (1, "6", False),
        (2, "1", True), (2, "2", False), (2, "3", False)]
a = C.decode(rows(spec), {}, True, parts=2, part_of_page={1: 0, 2: 1})
check("decode: parts restart the numbering (the Testaments)", [a[i] for i in sorted(a)][-3:]
      == [(1, 1, 1), (1, 1, 2), (1, 1, 3)])

units, stats = C.build_units(rows([(1, "1", False), (1, None, False), (2, "2", False)]),
                             {0: (0, 1, 1), 2: (0, 1, 2)})
check("build_units: continuation lines join their verse, leaves recorded",
      len(units) == 2 and units[0]["text"] == "text 0 text 1" and units[1]["leaves"] == [2])


# -- the Sibylline line numbers
def page(lines):
    return {"w": 2000, "h": 3000, "lines": [
        {"bbox": (200, 300 + 50 * i, 1800, 340 + 50 * i), "xs": 42.0,
         "words": [(200 + 10 * j, 300 + 50 * i, 205 + 10 * j, 340 + 50 * i, 95, w) for j, w in enumerate(t.split())],
         "text": t} for i, t in enumerate(lines)]}


P = [page(["(1) O ye mortal men (2) why do ye", "(3) Do ye not tremble"]),
     page(["(1) One God (2) who alone", "(1) Book three begins (2) and goes on"])]
u, s = C.sibyl_units(P, [0, 1], 38, ["frag1", "frag2", "3"])
check("sibyl: a '(1)' after more than two lines starts the next part",
      [(x["part"], x["v"]) for x in u] == [(0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (2, 1), (2, 2)])
P = [page(["(696) a (97) b (98) c (99) d (700) e (1) f (3) g"])]
u, s = C.sibyl_units(P, [0], 38, ["3"])
check("sibyl: dropped hundreds are restored, a slip is inferred",
      [x["v"] for x in u] == [696, 697, 698, 699, 700, 701, 703] and u[-1]["num"] == "read")

# -- the table
check("table: every book's leaves run forward", all(b[4] < b[5] for b in B.BOOKS))
check("table: slugs unique", len({b[0] for b in B.BOOKS}) == len(B.BOOKS))
check("table: parallel-column books are built by page",
      {b[0] for b in B.BOOKS if b[6] == "columns"} == {"adam", "2en", "ahikar"})
check("cite: part names carry no stray dot",
      B.cite("testxii", {"parts": ["Jos."]}, {"part": 0, "ch": 3, "v": 7}) == "Jos.3.7")
check("table: Gregg's Esther is flagged in its rights",
      "addesth" in [b[0] for b in B.BOOKS])

# -- the committed manifest entries (present after a build)
with open(B.MANIFEST, encoding="utf-8") as f:
    man = json.load(f)
ents = {k: v for k, v in man.items() if k.startswith("charles-")}
if ents:
    check("manifest: one entry per book", len(ents) == len(B.BOOKS))
    check("manifest: every entry has an honesty field and a rights block",
          all(e["scheme"].get("honesty") and e.get("rights") for e in ents.values()))
    check("manifest: Esther not marked for whole redistribution",
          ents["charles-addesth"]["rights"]["redistribute_whole"] is False)
    check("manifest: verse books carry their measure",
          all(e["measure"].get("verses") for e in ents.values() if e["scheme"]["resolution"] == "verse"))
    k = ents["charles-1macc"]["measure"].get("kjv_verse_numbers")
    check("manifest: I Maccabees has over 90% of the KJV's verse numbers", k and k["present"] >= 0.9 * k["kjv"])

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
