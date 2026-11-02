#!/usr/bin/env python3
# prov: 2026-11-02 claude-opus-5-5 drafted (Adam: "get all of the uids attached to each of the pieces that are ready for them")
# fable_review: pending
"""
bank_uids.py -- record in the registry the uids a room minted on its own.

HOUSE STYLE R8: the registry is the single home for which uid names which
citation. Some catalogues mint their uids where they are made -- the
Armarium's picture catalogues (wordhoard/apps/armarium/data/plates/*.json)
mint a `wh-` uid per plate, checked against this registry, and say "bank them
there". Until they are banked this registry cannot refuse to mint one of
them a second time, and nothing can look a plate's uid up.

This script reads any JSON or JSONL file, finds every object carrying both a
`uid` (a wh- uid) and a `citation`, and banks the pair with
WhUidRegistry.bank(): it never mints and never moves a uid. A citation that
already holds another uid, or a uid already held by anything else, stops the
run before anything is written.

    python3 pipeline/bank_uids.py FILE...           # bank, then save
    python3 pipeline/bank_uids.py --check FILE...   # exit 1 if anything is unbanked
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wh_uid import WhUidRegistry, WhUidError, is_uid  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")


def pairs_in(obj, out):
    if isinstance(obj, dict):
        u, c = obj.get("uid"), obj.get("citation")
        if isinstance(u, str) and isinstance(c, str) and is_uid(u):
            out.append((c, u))
        for v in obj.values():
            pairs_in(v, out)
    elif isinstance(obj, list):
        for v in obj:
            pairs_in(v, out)
    return out


def read(path):
    with open(path, encoding="utf-8") as f:
        if path.endswith(".jsonl"):
            return [json.loads(l) for l in f if l.strip()]
        return json.load(f)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--registry", default=REGISTRY)
    a = ap.parse_args(argv)
    reg = WhUidRegistry(a.registry)
    seen, todo = {}, []
    for path in a.files:
        for c, u in pairs_in(read(path), []):
            if seen.get(c, u) != u:
                raise WhUidError(f"{c!r} carries two uids across the files: {seen[c]} and {u}")
            seen[c] = u
            if reg.map.get(c) != u:
                todo.append((c, u, path))
    if a.check:
        print(f"{len(seen)} citation/uid pairs, {len(todo)} not banked")
        for c, u, p in todo[:20]:
            print(f"  {u} {c}  ({os.path.basename(p)})")
        return 1 if todo else 0
    n = sum(1 for c, u, _ in todo if reg.bank(c, u))
    reg.save()
    print(f"{len(seen)} citation/uid pairs; banked {n}; minted 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
