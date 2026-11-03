#!/usr/bin/env python3
"""Bloom shelves, offline (no corpus needed): every Bloom addition carries its
case and passed the gates when it was fetched.

For every pipeline/*_shelf.json with a `_bloom` block:
  - each `_bloom` slug is a row in one of the source dicts (gutenberg,
    internet_archive, tcp, standard_ebooks, ccel), so no case outlives its book;
  - each case names Bloom's number(s), title, year, evidence and the case itself;
  - each row has a recorded `_checks` entry (fetch_shelf.py --verify --record)
    whose identity is ok / title_weak / identity_override;
  - no recorded rights finding refuses it: an IA, TCP or SE row is "ok" or
    carries a person's `rights_override`; no Gutenberg row is marked
    COPYRIGHTED or names a different translator;
  - every Bloom number is a real entry in docs/review/bloom/bloom-research.jsonl.
    python3 tests/bloom_shelves_test.py
"""
import glob, json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = ("gutenberg", "internet_archive", "tcp", "standard_ebooks", "ccel")
FIELDS = ("bloom_n", "bloom_title", "year", "evidence", "case")
research = {json.loads(l)["n"] for l in open(os.path.join(ROOT, "docs/review/bloom/bloom-research.jsonl"), encoding="utf-8")}
fails, nshelves, nrows = [], 0, 0
for p in sorted(glob.glob(os.path.join(ROOT, "pipeline", "*_shelf.json"))):
    d = json.load(open(p, encoding="utf-8"))
    b = d.get("_bloom")
    if not b:
        continue
    nshelves += 1
    name = os.path.basename(p)[:-len("_shelf.json")]
    rows = {s: k for k in SRC for s in d.get(k, {})}
    checks = d.get("_checks", {})
    for slug, case in b.items():
        nrows += 1
        where = f"{name}/{slug}"
        if slug not in rows:
            fails.append(f"{where}: a Bloom case with no row on the shelf")
            continue
        miss = [f for f in FIELDS if not case.get(f)]
        if miss:
            fails.append(f"{where}: case lacks {miss}")
        for n in case.get("bloom_n") or []:
            if n not in research:
                fails.append(f"{where}: Bloom number {n} is not in bloom-research.jsonl")
        c = checks.get(slug)
        if not c:
            fails.append(f"{where}: never verified (no _checks entry)")
            continue
        if c.get("identity") not in ("ok", "title_weak", "identity_override"):
            fails.append(f"{where}: identity {c.get('identity')!r}")
        rights = c.get("ia_rights") or c.get("tcp_rights") or c.get("se_rights")
        if c.get("kind") in ("ia", "tcp", "se") and not (str(rights).startswith("ok") or c.get("rights_override")):
            fails.append(f"{where}: rights {rights!r} with no override")
        if c.get("pg_copyrighted"):
            fails.append(f"{where}: COPYRIGHTED Project Gutenberg eBook")
        if c.get("translator_match") is False:
            fails.append(f"{where}: Gutenberg names translator {c.get('pg_translator')!r}")
for f in fails:
    print("FAIL", f)
print(f"bloom_shelves_test: {nshelves} shelves, {nrows} Bloom rows, {len(fails)} failures")
raise SystemExit(1 if fails else 0)
