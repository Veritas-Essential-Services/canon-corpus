#!/usr/bin/env python3
# prov: 2026-10-23 claude-opus-5-5 drafted
# fable_review: pending
"""Offline checks for data/stories/ (the Illustrated Classics story layer) and
data/art/illustrated-classics/. No network, no corpus needed.
    python3 tests/stories_test.py"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import build_stories as B  # noqa: E402
import wh_uid as U  # noqa: E402

PASS, FAIL = 0, []


def check(label, cond):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label)


reg = json.load(open(B.UIDS, encoding="utf-8"))["uids"]
TI = os.path.join(B.STORIES, "treasure-island")
story = json.load(open(os.path.join(TI, "story.json"), encoding="utf-8"))
figures = B.read_jsonl(os.path.join(TI, "figures.jsonl"))
scenes = B.read_jsonl(os.path.join(TI, "scenes.jsonl"))
tel = story["tellings"][0]

check("Treasure Island: 34 chapters, 1,424 house units, 55 scenes, 20 figures",
      len(tel["chapters"]) == 34 and tel["units"] == 1424 and len(scenes) == 55 and len(figures) == 20)
rows = [story] + figures + scenes
check("every story, figure and scene has a well-formed, unique uid",
      all(U.is_uid(r.get("uid", "")) for r in rows) and len({r["uid"] for r in rows}) == len(rows))
check("the registry holds each citation -> uid exactly as the files say",
      reg.get("story-treasure-island:story") == story["uid"]
      and all(reg.get(f"story-treasure-island:figure.{f['id']}") == f["uid"] for f in figures)
      and all(reg.get(f"story-treasure-island:scene.{s['id']}") == s["uid"] for s in scenes))
check("every scene names known figures and a known setting",
      all(set(s["figures"]) <= {f["id"] for f in figures} and s["setting"] in story["settings"] for s in scenes))
check("every anchor is a treasure_island unit inside its chapter's paragraph count",
      all(s["at"].startswith("treasure_island:") and 1 <= s["para"] <= tel["chapters"][s["chapter"] - 1]["paras"]
          for s in scenes))
check("scenes run in story order", [(s["chapter"], s["para"]) for s in scenes]
      == sorted((s["chapter"], s["para"]) for s in scenes))
check("no row carries book text: titles and looks are short paraphrase",
      all(len(s["title"]) <= 80 for s in scenes) and all(len(l["fact"]) <= 120 for f in figures for l in f["looks"]))

problems = []
B.validate("x", {"settings": {"a": ""}, "tellings": [{"id": "t", "book": "b", "chapters": [{"n": 1, "paras": 3}]}]},
           [{"id": "f", "looks": []}],
           [{"id": "s1", "telling": "t", "chapter": 1, "para": 9, "at": "b:x.1", "figures": ["nobody"], "setting": "z"}],
           problems)
check("validate catches a paragraph out of range, an unknown figure and an unknown setting",
      len(problems) == 3)

r = subprocess.run([sys.executable, os.path.join(ROOT, "pipeline", "build_stories.py"), "--check"],
                   capture_output=True, text=True)
check("build_stories.py --check: mint 0, byte-identical", r.returncode == 0 and "mint 0" in r.stdout)

ed = json.load(open(os.path.join(ROOT, "data", "art", "illustrated-classics", "treasure-island", "editions.json"),
                    encoding="utf-8"))
check("every edition has a rights answer for the US and the UK/EU, with its basis",
      all(isinstance(e["rights"]["us"], bool) and isinstance(e["rights"]["uk_eu"], bool) and e["rights"]["basis"]
          for e in ed["editions"]))
check("nothing held for rights is marked as an anchor or fill",
      all(e["role"] == "hold" for e in ed["editions"] if not (e["rights"]["us"] and e["rights"]["uk_eu"])))
check("an edition is US public domain only if published before 1931",
      all(e["year"] < 1931 for e in ed["editions"] if e["rights"]["us"]))

print(f"\n{PASS} passed, {len(FAIL)} failed")
sys.exit(1 if FAIL else 0)
