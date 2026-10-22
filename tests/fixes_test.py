#!/usr/bin/env python3
# prov: 2026-10-20 claude-opus-5-5 drafted
# fable_review: pending
"""Offline checks for the fix library's profile (unscanner/fixes.py): a tiny library and a made-up
book, no fetched sources needed. Run: python3 tests/fixes_test.py"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from unscanner import fixes as FX      # noqa: E402

ok = bad = 0


def check(name, cond):
    global ok, bad
    print(("ok   " if cond else "FAIL ") + name)
    ok += bool(cond)
    bad += (not cond)


def page(words):
    return {"n": 1, "kind": "text", "drop": [], "lines": [{"words": [{"t": t, "conf": c} for t, c in words]}]}


# a book whose face reads c as e: "ealled" by habit (confidently), "pieture" now and then
text = [("called", 95)] * 30 + [("ealled", 92)] * 6 + [("picture", 95)] * 4 + [("pieture", 60)] * 2 + \
       [("church", 95)] * 12 + [("chureh", 70)] * 2 + [("Hugo", 96)] * 3 + [("huge", 95)] + \
       [("abandon'd", 95)] + [("foon", 50)] + [("soon", 95)] * 5 + [("bad", 95)] * 4 + [("had", 95)] * 40 + \
       [("enfants", 93)] * 2 + [("enfans", 50)] + [("collected", 95)] * 3 + [("colleeted", 60)] * 2 + \
       [("hence", 95)] * 3 + [("henee", 55)] * 3 + [("watched", 95)] * 2 + [("watehed", 55)] * 2 + \
       [("eclogue", 95)] + [("eelogue", 55)] * 2 + [("speech", 95)] * 2 + [("speeeh", 55)] * 2
book = {"pages": [page(text)]}
lex = {"called", "picture", "church", "huge", "soon", "bad", "had", "collected", "hence", "watched",
       "eclogue", "speech", "abandoned", "contend"}
lib = [
    {"id": "u:1", "kind": "word", "match": "chureh", "replace": "church", "source": "underwood", "file": "x"},
    {"id": "u:2", "kind": "word", "match": "hugo", "replace": "huge", "source": "underwood", "file": "x"},
    {"id": "u:3", "kind": "word", "match": "foon", "replace": "soon", "source": "underwood", "file": "x"},
    {"id": "u:4", "kind": "normalize", "match": "abandon'd", "replace": "abandoned", "source": "underwood", "file": "x"},
    {"id": "g:1", "kind": "stealth", "match": "bad", "replace": "had", "source": "guiguts", "file": "x"},
    {"id": "u:5", "kind": "word", "match": "nowhere", "replace": "now here", "source": "underwood", "file": "x"},
    {"id": "i:1", "kind": "char", "match": "e", "replace": "c", "source": "icdar2019", "file": "x", "weight": 17},
    {"id": "i:2", "kind": "char", "match": "f", "replace": "s", "source": "icdar2019", "file": "x", "weight": 72},
]
prof = FX.profile(book, lex, lib)
traits = {(t["wrong"], t["right"]): t["state"] for t in prof["traits"]}
check("the face's trait is found: e read for c", traits.get(("e", "c")) == "on")
check("the long s is not this face's (f for s stays off or flagged)", traits.get(("f", "s")) != "on")
st = {r: prof["rules"].get(r, {}).get("state", "off") for r in ("u:1", "u:2", "u:3", "u:4", "g:1", "u:5")}
check("a borrowed rule on this face's confusion is on (chureh -> church)", st["u:1"] == "on")
check("a long-s rule is not on in a book without long s (foon -> soon)", st["u:3"] != "on")
check("a normalization is never on (abandon'd)", st["u:4"] == "off")
check("a stealth scanno is for a person (bad / had)", st["g:1"] == "flag")
check("a rule that never fires is off", st["u:5"] == "off")
ev = FX.Evidence(book, lex)
fix = FX.fixer(prof, ev)
check("a confident habit is still a misreading: ealled -> called", (fix("ealled") or [None])[0] == "called")
check("the case is kept: Pieture, -> Picture,", (fix("Pieture,") or [None])[0] == "Picture,")
check("a name the book prints cleanly is left alone (Hugo)", fix("Hugo") is None)
check("a word printed cleanly that is no confusion stays (enfants)", fix("enfants") is None)
check("half a word at the margin is left alone (Colleet-)", fix("Colleet-") is None)
check("a dictionary word is left alone (called)", fix("called") is None)
print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
