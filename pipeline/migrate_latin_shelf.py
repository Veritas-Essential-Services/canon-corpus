#!/usr/bin/env python3
"""
migrate_latin_shelf.py -- give the Corpus Thomisticum shelf house-conforming
citations and uids, WITHOUT breaking anything that already points at it.

    python3 pipeline/migrate_latin_shelf.py --dir "<...>/data/latin-corpus" --report
    python3 pipeline/migrate_latin_shelf.py --dir "<...>/data/latin-corpus" --write
    python3 pipeline/migrate_latin_shelf.py --dir "<...>/data/latin-corpus" --check

WHAT IS WRONG TODAY
    The Latin shelf invented its own addressing -- `ST-I.q2.a3.co.s01`,
    `HYM-adoro.st1.la.1`, `HYM-adoro.st1.t01` -- against the house grammar
    `<slug>:<path>`. Armarium CLAUDE.md rule 3 forbids exactly this, and the
    Rooms note (2026-09-17 §3) flagged it as needing a ruling BEFORE the JSONL
    grows large enough that renaming hurts. It is 1,386 ids and has no
    consumers yet, so this is the cheap moment.

    The grammar is also genuinely ambiguous: `ST-I-II.q90.a4.sc` uses `-` as
    both the work separator AND part of the work name (Prima Secundae). Any
    parser splitting on `-` gets it wrong. Nothing parses it yet -- which is
    the only reason that is still cheap to fix.

WHAT THIS DOES -- ADDITIVE, NEVER DESTRUCTIVE
    Every record KEEPS its existing `id` untouched, and gains:

        uid       wh-XXXXXXXXXX      minted once, immutable, from wh_uid.py
        citation  thomas-summa:I.q2.a3.co.s01     house grammar
        address   wh-XXXXXXXXXX/la.1              on witnesses
                  wh-XXXXXXXXXX/la.1.t04          on tokens

    So `thomas-batch-01-permutations.json`, which joins to the passages by
    `unit_id` and whose tokens carry NO id at all (they join by POSITION),
    keeps working exactly as before. Nothing is renamed, so nothing dangles.
    The old `id` becomes the legacy key and can be dropped in a later pass,
    once something actually reads `citation`.

NOTHING IS GUESSED
    The work map below is explicit. An id whose prefix is not in it is a HARD
    FAILURE, not a best-effort slug. The last time something in this system
    guessed a name from a string it invented five projects out of a directory
    listing, and the rule that came out of it is the one this file obeys:
    a filename is not evidence.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wh_uid as U  # noqa: E402

DEFAULT_UIDS = os.path.join(os.path.dirname(HERE), "data", "uids", "wordhoard.uids.json")

# old prefix -> (new slug, evidence). The evidence column is the `work` field
# found on the records carrying that prefix, so the mapping can be checked
# against the data rather than trusted.
WORK_MAP = {
    "ST-I":     ("thomas-summa", "Summa Theologiae I q.2 a.3"),
    "ST-I-II":  ("thomas-summa", "Summa Theologiae I-II q.90 a.4"),
    "HYM-adoro": ("hymns",       "Adoro te devote"),
    "HYM-pange": ("hymns",       "Pange lingua gloriosi corporis mysterium"),
}

# For hymns the printed work title is the path root, so it must be named, not
# derived. `adoro` -> `adoro-te` is a judgement about the hymn's incipit and
# belongs in a table a human can read and correct.
HYMN_PATH = {"HYM-adoro": "adoro-te", "HYM-pange": "pange-lingua"}


def split_id(old):
    """-> (prefix, rest). Longest matching prefix wins, so ST-I-II beats ST-I."""
    for pre in sorted(WORK_MAP, key=len, reverse=True):
        if old == pre or old.startswith(pre + "."):
            return pre, old[len(pre):].lstrip(".")
    raise SystemExit(
        f"UNMAPPED id prefix in {old!r}.\n"
        f"Add it to WORK_MAP with the `work` field that justifies it. "
        f"This is a hard stop on purpose: guessing a slug from a string is "
        f"how this vault generated five projects out of a directory listing.")


def citation_for(old):
    pre, rest = split_id(old)
    slug, _ = WORK_MAP[pre]
    if pre.startswith("HYM-"):
        return f"{slug}:{HYMN_PATH[pre]}.{rest}" if rest else f"{slug}:{HYMN_PATH[pre]}"
    # ST-I -> I, ST-I-II -> I-II : the part after the first dash is the part
    # number and stays verbatim, which is precisely what the old grammar could
    # not express unambiguously.
    part = pre.split("-", 1)[1]
    return f"{slug}:{part}.{rest}" if rest else f"{slug}:{part}"


def witness_tail(witness_id, passage_id):
    """`HYM-adoro.st1.la.1` under passage `HYM-adoro.st1` -> `la.1`."""
    if not witness_id.startswith(passage_id + "."):
        raise SystemExit(f"witness {witness_id!r} is not under passage {passage_id!r} "
                         f"-- refusing to guess where it belongs")
    return witness_id[len(passage_id) + 1:]


def run(d, write=False, check=False, uids=DEFAULT_UIDS):
    reg = U.WhUidRegistry(uids)
    files = [f for f in sorted(os.listdir(d))
             if re.match(r"thomas-batch-\d+\.json$", f)]
    if not files:
        sys.exit(f"no thomas-batch-NN.json under {d}")

    totals = {"passages": 0, "witnesses": 0, "tokens": 0}
    slugs = {}
    for fn in files:
        p = os.path.join(d, fn)
        doc = json.load(open(p, encoding="utf-8"))
        for psg in doc.get("passages", []):
            old = psg["id"]
            cit = citation_for(old)
            slugs.setdefault(cit.split(":")[0], 0)
            slugs[cit.split(":")[0]] += 1
            uid = reg.uid_for(cit)
            psg["uid"] = uid
            psg["citation"] = cit
            psg["legacy_id"] = old
            totals["passages"] += 1
            for w in psg.get("witnesses", []):
                tail = witness_tail(w["witness_id"], old)
                w["address"] = U.address(uid, tail)
                w["legacy_witness_id"] = w["witness_id"]
                totals["witnesses"] += 1
                for t in w.get("tokens", []):
                    ttail = witness_tail(t["token_id"], old)
                    # a token's address hangs off its WITNESS, not the passage
                    t["address"] = U.address(uid, f"{tail}.{ttail}")
                    t["legacy_token_id"] = t["token_id"]
                    totals["tokens"] += 1
        doc.setdefault("identity", {})
        doc["identity"] = {
            "scheme": U.WhUidRegistry.SCHEME,
            "migrated": "2026-09-18",
            "note": ("Every record keeps its original `id` as `legacy_id`. "
                     "`citation` is the house grammar <slug>:<path>; `uid` is "
                     "the immutable identity; witness and token `address` "
                     "fields hang off the uid. Nothing was renamed, so the "
                     "permutation files' unit_id join is unaffected."),
        }
        if write:
            tmp = p + ".tmp"
            json.dump(doc, open(tmp, "w", encoding="utf-8", newline="\n"),
                      ensure_ascii=False, indent=1)
            os.replace(tmp, p)
            print(f"  rewrote {fn}")
        else:
            print(f"  {fn}: {len(doc.get('passages', []))} passages (dry run)")

    print()
    for k, v in totals.items():
        print(f"  {k:<12}{v:>6,}")
    print(f"  slugs       {slugs}")
    s = reg.stats()
    print(f"  uids minted {s['minted']:,} / reused {s['reused']:,} "
          f"/ registry total {s['total']:,}")

    if check:
        reg.assert_no_mint()
        print("  CHECK PASSED: a rerun moved no identifier.")
        return
    if write:
        reg.save()
        print(f"  wrote {uids}   <- COMMIT THIS")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--uids", default=DEFAULT_UIDS)
    a = ap.parse_args()
    run(a.dir, write=a.write, check=a.check, uids=a.uids)
