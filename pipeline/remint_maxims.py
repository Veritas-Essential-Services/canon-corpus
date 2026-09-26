#!/usr/bin/env python3
"""
remint_maxims.py -- give Adam's original maxims house uids, as Hoard records,
WITHOUT touching the file they were filed in.

    python3 pipeline/remint_maxims.py            # DRY RUN (the default): what would be minted and written
    python3 pipeline/remint_maxims.py --write    # mint in the registry; write the Hoard records
    python3 pipeline/remint_maxims.py --check    # the written records agree with the source and the registry

WHAT IS WRONG TODAY
    data/maxims/maxims-original.jsonl (filed 2026-09-05) keys its three records
    `ak-maxim-0001` .. `ak-maxim-0003`: a kind in the id and a person's initials,
    which the house style forbids (ADR 0015; wh_uid.py docstring). The Hoard
    Record (wordhoard ADR 0018, docs/architecture/hoard-record.md s4) says old ids
    go in `legacy[]`, never used as keys, and each maxim becomes a
    `passage/maxim` record with a plain `wh-` uid.

WHAT THIS DOES -- ADDITIVE, NEVER DESTRUCTIVE
    - The source file is READ ONLY. Its ids, dates and statuses stay as filed
      (ADR 0014: "Dates on AK-001/2/3 stay as filed").
    - Each record's uid comes from the registry (data/uids/wordhoard.uids.json),
      keyed on the citation `maxims:<ref>` (`maxims:AK-001`): minted once,
      reused forever after, so a second --write mints nothing.
    - The Hoard records go to a NEW file, data/maxims/maxims-original.hoard.jsonl,
      one per line, written deterministically (same input, same bytes). It is
      what the Florilegium's Propria imports (Import, on the Propria page).
    - `legacy[]` carries the old id and the ref, so every pointer at
      `ak-maxim-000n` or `AK-00n` can be followed to the new uid.
    - A `kept` founder carries the kept_basis Adam ruled on 2026-09-05 (vault:
      "Word Hoard -- Maxim Unit Type and Propria", decision 3): they were kept
      the day they were coined, before the cooling-off rule existed, and a
      corpus about exceptions should not quietly except itself. kept_on is not
      recorded in the source, so it stays null rather than being guessed.

NOTHING IS GUESSED
    A field this script does not know, an id not of the form ak-maxim-NNNN, a
    record with no `ref`, or a `supersedes` that names no record here, is a
    HARD FAILURE, not a best effort. Nothing is dropped silently.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wh_uid as U  # noqa: E402

ROOT = os.path.dirname(HERE)
DEFAULT_SRC = os.path.join(ROOT, "data", "maxims", "maxims-original.jsonl")
DEFAULT_MANIFEST = os.path.join(ROOT, "data", "maxims", "maxims-original.manifest.json")
DEFAULT_OUT = os.path.join(ROOT, "data", "maxims", "maxims-original.hoard.jsonl")
DEFAULT_UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")

OLD_ID_RE = re.compile(r"^ak-maxim-\d{4}$")
SLUG = "maxims"
TOOL = "canon-corpus/remint_maxims"
FOUNDING_BASIS = ("founding record — adjudicated in conversation 2026-09-05, "
                  "before the cooling-off rule existed")

# Every field the 2026-09-05 records carry, and where it goes. A field not
# listed here stops the run: a new field is a decision, not a default.
KNOWN = {"uid", "type", "provenance", "status", "visibility", "author", "coined_on",
         "coined_precision", "revision", "supersedes", "ref", "text", "form", "scope",
         "subjects", "chars", "note", "ancestors", "kept_on", "kept_basis"}
STATUSES = {"draft", "kept", "retired"}
PRECISIONS = {"day": 10, "month": 7, "year": 4}


class RemintError(SystemExit):
    pass


def read_source(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except ValueError as e:
                raise RemintError(f"{path}:{n}: not JSON ({e})")
    return rows


def check_source(rows):
    seen, refs = set(), set()
    for r in rows:
        old = r.get("uid")
        if not OLD_ID_RE.match(old or ""):
            raise RemintError(f"not an ak-maxim-NNNN id: {old!r}. Nothing is guessed; fix the source or this script.")
        if old in seen:
            raise RemintError(f"{old} appears twice in the source")
        seen.add(old)
        extra = set(r) - KNOWN
        if extra:
            raise RemintError(f"{old}: unknown field(s) {sorted(extra)}. Map them in KNOWN/to_record before re-minting.")
        if r.get("type") != "maxim":
            raise RemintError(f"{old}: type is {r.get('type')!r}, not 'maxim'")
        if not r.get("ref") or not re.match(r"^[A-Za-z0-9][A-Za-z0-9.\-]*$", r["ref"]):
            raise RemintError(f"{old}: needs a ref like AK-001 (it becomes the citation)")
        if r["ref"] in refs:
            raise RemintError(f"{old}: ref {r['ref']} is used twice")
        refs.add(r["ref"])
        if r.get("status") not in STATUSES:
            raise RemintError(f"{old}: status {r.get('status')!r} is not one of {sorted(STATUSES)}")
        p = r.get("coined_precision") or "day"
        if p not in PRECISIONS or len(r.get("coined_on") or "") != PRECISIONS[p]:
            raise RemintError(f"{old}: coined_on {r.get('coined_on')!r} does not fit precision {p!r}")
        if not isinstance(r.get("text"), str) or not r["text"]:
            raise RemintError(f"{old}: no text")
    for r in rows:
        s = r.get("supersedes")
        if s is not None and s not in seen:
            raise RemintError(f"{r['uid']}: supersedes {s!r}, which is not in this file")


def citation_for(r):
    return f"{SLUG}:{r['ref']}"


def to_record(r, uid, uid_of_old, filed_on, src_rel):
    status = r["status"]
    basis = r.get("kept_basis")
    if status == "kept" and not basis and not r.get("kept_on"):
        basis = FOUNDING_BASIS
    return {
        "hoard": "1",
        "uid": uid,
        "kind": "passage",
        "type": "maxim",
        "citation": citation_for(r),
        "lang": "en",
        "title": None,
        "body": {
            "text": r["text"],
            "note": r.get("note"),
            "coined_on": r["coined_on"],
            "coined_precision": r.get("coined_precision") or "day",
            "form": r.get("form"),
            "scope": r.get("scope"),
            "subjects": r.get("subjects") or [],
            "ancestors": r.get("ancestors") or [],
            "chars": r.get("chars"),
            "kept_on": r.get("kept_on"),
            "kept_basis": basis if status == "kept" else r.get("kept_basis"),
        },
        "refs": {},
        "text_as_met": None,
        "provenance": {
            "origin": r.get("provenance") or "original",
            "author": r.get("author"),
            "entered_by": None,
            "chosen_by": None,
            "tool": TOOL,
            "created_at": filed_on,
        },
        "rights": {"license": "own", "shareable": False, "redistribute_whole": False},
        "status": status,
        "scope": {"visibility": r.get("visibility") or "private", "profile_id": None,
                  "household_id": None, "owner_user_id": None},
        "lineage": {"revision": r.get("revision") or 1,
                    "supersedes": uid_of_old[r["supersedes"]] if r.get("supersedes") else None,
                    "forked_from": None, "split_from": None, "merged_from": [], "tombstone_of": None},
        "facets": {},
        "tags": ["ref:" + r["ref"]],
        "legacy": [{"room": "canon-corpus", "id": r["uid"], "file": src_rel},
                   {"room": "vault", "id": r["ref"]}],
        "updated_at": filed_on,
    }


def build(rows, reg, filed_on, src_rel):
    """-> (records, plan). Mints through `reg` for any citation it has not seen."""
    uid_of_old, plan = {}, []
    for r in rows:
        cit = citation_for(r)
        had = cit in reg.map
        uid_of_old[r["uid"]] = reg.uid_for(cit)
        plan.append({"old": r["uid"], "citation": cit, "uid": uid_of_old[r["uid"]], "new": not had, "status": r["status"]})
    records = [to_record(r, uid_of_old[r["uid"]], uid_of_old, filed_on, src_rel) for r in rows]
    return records, plan


def dump(records):
    return "".join(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for x in records)


def filed_date(manifest_path):
    try:
        with open(manifest_path, encoding="utf-8") as f:
            d = json.load(f).get("generated")
    except (OSError, ValueError):
        d = None
    if not d or not re.match(r"^\d{4}-\d{2}-\d{2}$", d):
        raise RemintError(f"{manifest_path}: needs a `generated` date (YYYY-MM-DD); the records' filing date comes from it")
    return d


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="mint in the registry and write the Hoard records")
    mode.add_argument("--check", action="store_true", help="verify the written records; write nothing")
    ap.add_argument("--src", default=DEFAULT_SRC)
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--uids", default=DEFAULT_UIDS)
    a = ap.parse_args(argv)

    rows = read_source(a.src)
    check_source(rows)
    filed_on = filed_date(a.manifest)
    src_rel = "data/maxims/" + os.path.basename(a.src)
    reg = U.WhUidRegistry(a.uids)
    records, plan = build(rows, reg, filed_on, src_rel)
    text = dump(records)

    if a.check:
        bad = []
        if reg.minted:
            bad.append(f"{reg.minted} citation(s) have no uid in the registry yet: run --write")
        if not os.path.exists(a.out):
            bad.append(f"{a.out} does not exist: run --write")
        else:
            with open(a.out, encoding="utf-8") as f:
                have = f.read().replace("\r\n", "\n")
            if have != text:
                bad.append(f"{a.out} does not match what the source and registry make: run --write, or find who edited it")
        for b in bad:
            print("FAIL " + b)
        if not bad:
            print(f"ok   {len(records)} maxims: every record matches its source row and its registry uid")
        return 1 if bad else 0

    print(f"{'WRITE' if a.write else 'DRY RUN'}: {len(rows)} maxims from {os.path.relpath(a.src, ROOT)}")
    for p in plan:
        rec = next(x for x in records if x["uid"] == p["uid"])
        print(f"  {p['old']}  ->  {p['uid'] if not (p['new'] and not a.write) else '(would mint)':<15} "
              f"{p['citation']:<16} {p['status']:<6}"
              + ("  kept_basis: founding record" if rec["body"]["kept_basis"] == FOUNDING_BASIS else ""))
    new = sum(1 for p in plan if p["new"])
    print(f"  registry: {new} to mint, {len(plan) - new} already there")
    print(f"  source file: untouched ({os.path.relpath(a.src, ROOT)})")
    if not a.write:
        print(f"  would write {len(records)} Hoard records to {os.path.relpath(a.out, ROOT)}. Nothing was written. Run with --write.")
        return 0
    reg.save()
    tmp = a.out + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, a.out)
    print(f"  wrote {len(records)} Hoard records to {os.path.relpath(a.out, ROOT)}; registry saved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
