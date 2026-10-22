#!/usr/bin/env python3
# prov: 2026-10-20 claude-opus-5-5 drafted
# fable_review: pending
"""Offline checks for what Character Sketches vol. 6 taught the Unscanner (2026-10-20): two columns,
running heads over each column, signature marks, margin breaks (rules 6b-6d), dashes (rule 7).
No scan needed. Run: python3 tests/editions_test.py"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from unscanner import layout as L      # noqa: E402

ok = bad = 0


def check(name, cond):
    global ok, bad
    print(("ok   " if cond else "FAIL ") + name)
    ok += bool(cond)
    bad += (not cond)


def line(x0, y0, x1, y1, *words):
    return {"bbox": [x0, y0, x1, y1], "x_size": y1 - y0, "words": [{"t": w, "conf": 90, "bbox": [x0, y0, x1, y1]} for w in words]}


# two columns, a running head over each, a signature mark at the foot of the right one
W, H = 2400, 3242
left = [line(640, 400, 760, 440, "RICE")] + [line(300, 500 + 52 * i, 1130, 545 + 52 * i, *"a line of the left column".split()) for i in range(40)]
right = [line(1130, 400, 1190, 440, "293"), line(1450, 400, 1780, 440, "RICHARD", "III.")] + \
    [line(1185, 500 + 52 * i, 2050, 545 + 52 * i, *"a line of the right column".split()) for i in range(40)] + \
    [line(1966, 2844, 2001, 2865, "lll")]
p = {"n": 7, "w": W, "h": H, "lines": left + right}
check("two columns found", L.find_columns(p) == 2)
check("each line knows its column", p["lines"][0]["col"] == 0 and p["lines"][-1]["col"] == 1)
one = {"n": 8, "w": W, "h": H, "lines": [line(300, 500 + 52 * i, 2050, 545 + 52 * i, "one", "column") for i in range(30)]}
check("a one-column page stays one column", L.find_columns(one) == 1 and "col" not in one["lines"][0])
p["columns"] = 2
f = L.find_furniture([p])[7]
check("the running head over each column is dropped", {0, 41, 42} <= f["drop"])
check("the signature mark at the column's foot is dropped", len(p["lines"]) - 1 in f["drop"])
check("body lines are kept", 5 not in f["drop"] and 50 not in f["drop"])

# margin breaks
D = frozenset(["first-rate", "pasture", "congress", "condition", "pervert", "knife", "grinder", "between", "go-between"])


def join(*lines, dictionary=D):
    log = L.new_log()
    toks = L.join_tokens([[{"t": w} for w in ln] for ln in lines], {}, {}, log, more=True, dictionary=dictionary)
    return L.tokens_text(toks)


check("small caps across the margin: Dia- / MONDS.) -> DIAMONDS.)", join(["(See", "Dia-"], ["MONDS.)"]) == "(See DIAMONDS.)")
check("a name's hyphen is kept: Fitz- / James", join(["Fitz-"], ["James"]) == "Fitz-James")
check("a range: 1630- / 1706", join(["(1630-"], ["1706)."]) == "(1630-1706).")
check("Webster solid: pas- / ture -> pasture", join(["pas-"], ["ture"]) == "pasture")
check("Webster solid with an ending: con- / ditions -> conditions", join(["con-"], ["ditions"]) == "conditions")
check("Webster hyphened: first- / rate -> first-rate", join(["first-"], ["rate"]) == "first-rate")
check("two words, no headword: knife- / grinder -> knife-grinder", join(["knife-"], ["grinder"]) == "knife-grinder")
check("an already hyphened word: go-be- / tween -> go-between", join(["go-be-"], ["tween"]) == "go-between")
check("a name broken mid-word: Copper- / field -> Copperfield", join(["Copper-"], ["field"]) == "Copperfield")
check("OCR dirt: be- - / cause -> because", join(["be-", "-"], ["cause"]) == "because")
check("OCR dirt: con-- / temptibly -> contemptibly", join(["con--"], ["temptibly"]) == "contemptibly")
check("OCR dirt: Decem- / ‘ber -> December", join(["Decem-"], ["‘ber"]) == "December")
check("a stray hyphen before a function word: called- / the", join(["called-"], ["the"]) == "called the")
check("off by default: no dictionary, no 6b", L.tokens_text(L.join_tokens([[{"t": "Fitz-"}], [{"t": "James"}]], {}, {}, L.new_log())) == "Fitz- James")

# dashes
au = frozenset(["Tennyson", "Byron"])
check("range takes an en dash", L.dashes("(1554-1628).")[0] == "(1554–1628).")
check("a range broken at the margin", L.dashes("(1276- 1347).")[0] == "(1276–1347).")
check("an em dash set close", L.dashes("stream.” — Spenser, Faery Queen")[0] == "stream.”—Spenser, Faery Queen")
check("a lone dash before a known author is the attribution dash", L.dashes("the pyramid. - Tennyson, The Princess", au)[0] == "the pyramid.—Tennyson, The Princess")
check("a lone dash before a new entry is dirt", L.dashes("(1593). - Pinch (Tom), clerk", au)[0] == "(1593). Pinch (Tom), clerk")
check("a lone dash mid-sentence is dirt", L.dashes("wife of - Sir Henry", au)[0] == "wife of Sir Henry")
check("St.- Leonard -> St. Leonard", L.dashes("St. Barbara and St.- Leonard.")[0] == "St. Barbara and St. Leonard.")
check("authors are the book's own", "Tennyson" in L.attribution_names(["a.—Tennyson, x", "b.—Tennyson, y"]))
print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
