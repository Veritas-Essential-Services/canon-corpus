#!/usr/bin/env python3
# prov: 2026-11-03 claude-opus-5-5 drafted (the Kipling shelf)
# fable_review: pending
"""The Kipling shelf's ledger (pipeline/kipling_shelf.json), offline: every prose row pinned to a
GITenberg commit and a sha256, first published by 1930, its uid in the registry; the verse rows
pointing at the Poetry Hoard; the completeness note present. No network, no corpus needed."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import fetch_sources  # noqa: E402

passed = failed = 0
def ok(c, m):
    global passed, failed
    print(("ok    " if c else "FAIL  ") + m)
    passed, failed = passed + bool(c), failed + (not c)

L = json.load(open(os.path.join(ROOT, "pipeline", "kipling_shelf.json"), encoding="utf-8"))
R = json.load(open(os.path.join(ROOT, "data", "uids", "wordhoard.uids.json"), encoding="utf-8"))["uids"]
G, P = L["gutenberg"], L["poetry_hoard"]
ok(len(G) >= 40 and len(P) >= 7, f"{len(G)} prose books and {len(P)} books of verse")
ok(fetch_sources.kipling_books() == G, "fetch_sources reads the ledger's prose rows, in order")
for slug, r in G.items():
    t = slug + ": "
    ok(re.fullmatch(r"kipling-[a-z0-9-]+", slug) and r["year"] <= 1930, t + f"first published {r['year']}, US public domain")
    ok(r["mirror"].startswith("https://github.com/GITenberg/") and r["mirror"].endswith("_" + str(r["id"]))
       and re.fullmatch(r"[0-9a-f]{40}", r["commit"]) and re.fullmatch(r"[0-9a-f]{64}", r["sha256"])
       and r["file"].startswith(str(r["id"])), t + "pinned: mirror of its Gutenberg number, commit, file, sha256")
for slug, r in {**G, **P}.items():
    ok(r["citation"] == "kipling:" + slug[len("kipling-"):] and R.get(r["citation"]) == r["uid"], slug + ": its work uid is the registry's (" + r["uid"] + ")")
uids = [r["uid"] for r in {**G, **P}.values()]
ok(len(set(uids)) == len(uids), "every work its own uid")
ok(all(r["armarium_slug"] == "poetryvol-" + s for s, r in P.items()), "the books of verse name the Armarium volume they become")
ok(not set(G) & set(P) and not set(G) & set(fetch_sources.GUTENBERG_EXTRA), "no book is on the shelf twice, nor fetched by another list")
ok(all(k in L for k in ("_waiting", "_pending", "_excluded")), "the completeness note: waiting, pending, excluded")
ok(all(re.search(r"\b(19[3-9]\d)\b", v) for k, v in L["_waiting"].items() if not k.startswith("_")), "every waiting book names its year after 1930")
print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
