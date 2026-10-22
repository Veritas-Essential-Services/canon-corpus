#!/usr/bin/env python3
"""pipeline/shelf_overlaps.py: two shelves naming one source are found, and
nothing else is. Fixtures are inline; the last block runs on this checkout."""
import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import shelf_overlaps as S  # noqa: E402

fails = passes = 0
def ok(c, m):
    global fails, passes
    print(("ok    " if c else "FAIL  ") + m)
    if c: passes += 1
    else: fails += 1


print("--- normalize")
ok(S.normalize("gutenberg", 16328, "x", {}) == "16328", "a Gutenberg number as an int")
ok(S.normalize("gutenberg", "PG016328", "x", {}) == "16328", "'PG016328' is the same book as 16328")
ok(S.normalize("internet_archive", "WorksOfJohnOwen01", "x", {}) == "worksofjohnowen01",
   "IA identifiers compare without case")
ok(S.normalize("ccel", "mort", "owen", {"_ccel_author": "o/owen"}) == "o/owen/mort",
   "a bare CCEL work takes the shelf's _ccel_author")
ok(S.normalize("ccel", "mort", "owen", {}) == "o/owen/mort", "without _ccel_author, the shelf name")
ok(S.normalize("ccel", "e/edwards/will", "flavel", {}) == "e/edwards/will", "a full CCEL path is kept")
ok(S.normalize("ccel", "life", "flavel", {}) != S.normalize("ccel", "life", "scougal", {}),
   "two authors' CCEL works called 'life' are different books")
ok(S.normalize("gutenberg", "", "x", {}) is None and S.normalize("gutenberg", None, "x", {}) is None,
   "an empty id names nothing")

shelves = {
    "beowulf": {"gutenberg": {"beowulf-hall": [16328, "Beowulf, tr. Hall"],
                              "beowulf-gummere": [981, "Beowulf, tr. Gummere"]}},
    "fetch_sources": {"gutenberg": {"beowulf": [16328, "beowulf"]}},
    "owen": {"_ccel_author": "o/owen",
             "ccel": {"owen-mort": ["mort", "Mortification", ""]},
             "internet_archive": {"owen-works-01": ["worksofjohnowen01", "Works vol. 1"],
                                  "owen-works-01b": ["WorksOfJohnOwen01", "Works vol. 1 again"]},
             "_held": {"owen-glory": "already in fetch_sources.py"},
             "_pending": {"owen-x": "IA worksofjohnowen01"}},
    "puritans": {"internet_archive": {"owen-works-01": ["otherscan01", "another book, same slug"]},
                 "_excluded": {"x": ["worksofjohnowen01", "excluded rows are not fetches"]}},
    "flavel": {"ccel": {"flavel-life": ["life", "Life", ""]}},
    "scougal": {"ccel": {"scougal-life": ["life", "Life of God", ""]}},
}
lanes = {"beowulf": "D", "fetch_sources": "main", "owen": "A", "puritans": "A",
         "flavel": "A", "scougal": "A"}

print("--- overlaps")
found = S.overlaps(shelves, lanes)
by_id = {(o["kind"], o["id"]): o for o in found}
ok(("gutenberg", "16328") in by_id, "PG 16328 in a lane shelf and in fetch_sources.py is found")
ok(by_id[("gutenberg", "16328")]["scope"] == "cross-lane", "...and is cross-lane (lane D vs main)")
o = by_id.get(("internet_archive", "worksofjohnowen01"))
ok(o is not None and o["scope"] == "same-lane" and o["same_shelf"],
   "one IA item listed twice in one shelf, differing only in case, is same-lane, one shelf")
ok(("gutenberg", "981") not in by_id, "a source named once is not reported")
ok(not any(k[0] == "ccel" for k in by_id), "Flavel's 'life' and Scougal's 'life' are not an overlap")
ok(all(r["slug"] not in ("owen-glory", "owen-x", "x") for o in found for r in o["rows"]),
   "_held, _pending and _excluded rows are not counted")
ok(found and found[0]["scope"] == "cross-lane", "cross-lane overlaps sort first")
both_main = S.overlaps({"a": {"gutenberg": {"s": [1, "t"]}}, "b": {"gutenberg": {"s2": [1, "t"]}}},
                       {"a": "main", "b": "main"})
ok(both_main and both_main[0]["scope"] == "on-main", "two merged shelves sharing a source are on-main")
ok(S.overlaps({"a": {"gutenberg": {"s": [1, "t"]}}, "b": {"gutenberg": {"s2": [1, "t"]}}})[0]["scope"]
   == "cross-lane", "an unknown lane counts as cross-lane (nobody is known to own both)")

print("--- slug clashes")
cl = {c["id"]: c for c in S.slug_clashes(shelves, lanes)}
ok("owen-works-01" in cl and not cl["owen-works-01"]["same_source"],
   "one slug for two different sources in two shelves is a clash")
ok("beowulf-hall" not in cl, "a slug used once is not a clash")

print("--- fetch_sources.py is read, not run")
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "pipeline"))
    with open(os.path.join(d, "pipeline", "fetch_sources.py"), "w", encoding="utf-8") as f:
        f.write('raise SystemExit("executed!")\n'
                'GUTENBERG_EXTRA = {"beowulf": 16328}\n'
                'CCEL = {"owen-mort": ("owen", "mort", "Mortification")}\n'
                'CHESTERTON_GUTENBERG = {"chesterton-x": (2015, "A Miscellany", "G. K. C.")}\n'
                'CHESTERTON_CCEL = {"chesterton-america": ("america", "What I Saw")}\n'
                'PERSEUS = {"iliad-butler": ("canonical-greekLit", "tlg0012/tlg001/tlg0012.tlg001.perseus-eng4.xml", "Iliad")}\n')
    root = S.ROOT
    S.ROOT = d
    try:
        m = S.manifest_shelf()
    finally:
        S.ROOT = root
ok(m["gutenberg"]["beowulf"][0] == 16328 and m["gutenberg"]["chesterton-x"][0] == 2015,
   "GUTENBERG_EXTRA and CHESTERTON_GUTENBERG are read")
ok(m["ccel"]["owen-mort"][0] == "o/owen/mort" and m["ccel"]["chesterton-america"][0] == "c/chesterton/america",
   "CCEL rows become full author/work paths")
ok(m["perseus"]["iliad-butler"][0] == "tlg0012.tlg001.perseus-eng4", "a Perseus path becomes its URN")

print("--- this checkout")
try:
    real = S.load_shelves()
    real["fetch_sources"] = S.manifest_shelf()
    n = sum(1 for _ in S.entries(real))
    ok(n > 0, f"{len(real)} shelves here, {n} fetch rows read")
except Exception as e:  # noqa: BLE001
    ok(False, f"reading this checkout's shelves raised {e!r}")

print(f"\n{passes} passed, {fails} failed")
sys.exit(1 if fails else 0)
