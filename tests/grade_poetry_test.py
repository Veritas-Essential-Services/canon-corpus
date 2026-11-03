#!/usr/bin/env python3
# prov: 2026-11-03 claude-opus-5-5 drafted
# fable_review: pending
"""
grade_poetry_test.py -- the graded volume (pipeline/grade_poetry.py).

Run:  python3 tests/grade_poetry_test.py

Offline. Rebuilds the graded files in memory and asserts they match what is
committed; checks every poem in every catalog is graded exactly once, every
band is one of the five, AO's year always wins, every placing book is in the
book table, and no file passes the 5 MB cap.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "pipeline"))
from build_poetry import read_parts  # noqa: E402

G = os.path.join(REPO, "data", "poetry", "graded")
BANDS = ["nursery", "y1-3", "y4-6", "y7-9", "y10-12"]
fails = 0


def ok(cond, msg):
    global fails
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond:
        fails += 1


r = subprocess.run([sys.executable, os.path.join(REPO, "pipeline", "grade_poetry.py"), "--check"],
                   capture_output=True, text=True)
ok(r.returncode == 0, "the committed graded files match a rebuild " + (r.stderr.strip() or ""))

rows = [json.loads(l) for l in open(os.path.join(G, "graded.jsonl"), encoding="utf-8")]
uids = [x["uid"] for x in rows]
ok(len(uids) == len(set(uids)), f"{len(rows)} poems, each graded once")

cat = set()
for layer in ["catalog-ao", "catalog-addendum-heroic", "catalog-collections", "catalog-treasury"]:
    cat |= {r["uid"] for r in read_parts(os.path.join(REPO, "data", "poetry", layer))}
ok(cat == set(uids), "every poem in every catalog is in the volume, and no more")
ok(all(x["band"] in BANDS for x in rows), "every band is one of the five")


def ao_band(y):
    return "y1-3" if y <= 3 else "y4-6" if y <= 6 else "y7-9" if y <= 9 else "y10-12"


ao = [x for x in rows if isinstance(x["ao_year"], int)]
ok(all(x["band"] == ao_band(x["ao_year"]) for x in ao), f"AO's year places all {len(ao)} AO-dated poems")
table = json.load(open(os.path.join(G, "book-bands.json"), encoding="utf-8"))
known = {int(k) for k in table["books"]}
missing = {b for x in rows for b in x["found_in"]} - known
ok(not missing, "every book a poem was found in has a band in book-bands.json " + str(sorted(missing)))
ok([x["rank"] for x in rows] == list(range(1, len(rows) + 1)), "ranks run 1..n in file order")
ok(all(BANDS.index(a["band"]) <= BANDS.index(b["band"]) for a, b in zip(rows, rows[1:])), "the volume runs band by band")

big = []
for d, _, fs in os.walk(G):
    for f in fs:
        if os.path.getsize(os.path.join(d, f)) > 5_000_000:
            big.append(f)
ok(not big, "no graded file over 5 MB " + str(big))

print("grade_poetry: " + ("all passed" if not fails else f"{fails} failed"))
sys.exit(1 if fails else 0)
