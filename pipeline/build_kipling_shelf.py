#!/usr/bin/env python3
# prov: 2026-11-03 claude-opus-5-5 drafted (Adam: "Give me a kippling shelf")
# fable_review: pending
"""build_kipling_shelf.py -- give every book on the Kipling shelf its work uid.

The ledger is pipeline/kipling_shelf.json. A book is a WORK (HOUSE STYLE R1, R6:
the kind is on the record, never in the uid), cited `kipling:<work>` (R3, the
way `aphthonius:progym` names a work): the prose books in `gutenberg` (built
here, data/books/kipling-<work>.json) and the books of verse in `poetry_hoard`
(wordhoard apps/poetryhoard/data/volumes.json, shelf "kipling", which the
Armarium binds as `poetryvol-kipling-<work>`). Each row carries its `citation`
and `uid`; the registry, data/uids/wordhoard.uids.json, is the single home
(R8), so pipeline/bank_uids.py --check passes on the ledger too.

    python3 pipeline/build_kipling_shelf.py           # mint what is new, write uids into the ledger
    python3 pipeline/build_kipling_shelf.py --check   # registry frozen: must mint 0, ledger must agree
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wh_uid import WhUidRegistry, WhUidError  # noqa: E402

LEDGER = os.path.join(HERE, "kipling_shelf.json")
REGISTRY = os.path.join(HERE, "..", "data", "uids", "wordhoard.uids.json")
SECTIONS = ("gutenberg", "poetry_hoard")


def citation(slug):
    return "kipling:" + slug[len("kipling-"):]


def main(argv):
    check = "--check" in argv
    d = json.load(open(LEDGER, encoding="utf-8"))
    reg = WhUidRegistry(REGISTRY, frozen=check)
    bad = []
    for sec in SECTIONS:
        for slug, row in d[sec].items():
            c = citation(slug)
            try:
                u = reg.uid_for(c)
            except WhUidError as e:
                bad.append(str(e))
                continue
            if check and (row.get("citation") != c or row.get("uid") != u):
                bad.append(f"{slug}: the ledger says {row.get('citation')} {row.get('uid')}, the registry {c} {u}")
            row["citation"], row["uid"] = c, u
    if check:
        if bad:
            print("\n".join(bad))
            sys.exit(1)
        n = sum(len(d[s]) for s in SECTIONS)
        print(f"kipling shelf: {n} works, every uid in the registry and the ledger, minted 0")
        return
    reg.save()
    tmp = LEDGER + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    os.replace(tmp, LEDGER)
    print(f"kipling shelf: minted {reg.minted}, reused {reg.reused}")


if __name__ == "__main__":
    main(sys.argv[1:])
