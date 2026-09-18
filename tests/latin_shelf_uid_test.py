#!/usr/bin/env python3
"""
latin_shelf_uid_test.py -- the enforcement gate for wave 1 (the Latin shelf).

Run:  python3 tests/latin_shelf_uid_test.py

WHY THIS EXISTS, WHEN wh_uid_test.py ALREADY PASSES
    `tests/wh_uid_test.py` tests the identity MODULE -- that minting, parsing,
    tombstones and the frozen gate behave. It never opens the corpus. So on
    2026-09-18 every one of its 54 checks passed while nothing whatsoever
    asserted that the 58 Latin passages actually carry the uids that were
    minted for them, or that those uids still match the committed registry.

    That is the exact failure this vault has now twice paid for: something
    built, nobody maintaining it, and a green test reporting health about a
    different question than the one anyone cared about. The design's own §10
    puts it plainly -- "enforcement first, because backfill without it is
    wasted work."

WHAT IT ASSERTS, AND WHY EACH ONE CAN FAIL IN REAL LIFE
    1. Every passage carries `uid`, `citation` and `legacy_id`; every witness
       and token carries an `address`.  <- a record added by hand, or a
       migration rerun that was never run with --write, silently lacks them.
    2. Every uid equals the one the COMMITTED registry holds for that record's
       citation.  <- this is the one that catches identity drift: a build run
       against the wrong registry copy renames the world and everything else
       still validates. Compare against the file, not against memory.
    3. Every uid is well-formed under wh_uid, and no two records share one.
    4. Every witness/token address resolves back to its own passage's uid.
    5. The shelf's shape is what was measured on 2026-09-18: 58 / 180 / 1,148.
       A count is cheap and it is the check that notices a batch going missing.
    6. Replaying the whole shelf against a COPY of the registry mints ZERO.
    7. The constants shared with code-corpus have not drifted -- and unlike the
       literal pin in wh_uid_test.py, this reads the sibling repo's own file
       when it is reachable, so a change THERE fails HERE. The two repos have
       no shared packaging by decision (wh_uid docstring); a checked copy is
       what makes that decision honest rather than merely stated.

SCOPE
    The Latin shelf only -- wave 1. It says nothing about the KJV, which is a
    separate question and is gated on a ruling Adam has not given.
"""
import json
import os
import shutil
import sys
import tempfile
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PIPE = os.path.join(REPO, "pipeline")


def load(name, path=None):
    path = path or os.path.join(PIPE, name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


U = load("wh_uid")

REGISTRY = os.path.join(REPO, "data", "uids", "wordhoard.uids.json")

# The shelf lives in the VAULT, not in this repo -- deliberately, per the
# 2026-09-17 ruling that vault folders do not mirror the room structure. So the
# path has to be given rather than assumed. Env var wins; otherwise the known
# locations are tried in order and the failure NAMES what it looked for,
# because "no such file" with no path in it has cost sessions before.
CANDIDATES = [
    os.environ.get("WORDHOARD_LATIN_DIR"),
    r"C:\Users\adamk\Obsidian\MindCastleintheCloud\9 - Projects\Word Hoard\data\latin-corpus",
    os.path.join(REPO, "..", "..", "..", "Obsidian", "MindCastleintheCloud",
                 "9 - Projects", "Word Hoard", "data", "latin-corpus"),
]

# Measured 2026-09-18 by parsing the two batch files. Not estimated.
EXPECTED = {"passages": 58, "witnesses": 180, "tokens": 1148}
EXPECTED_SLUGS = {"thomas-summa": 45, "hymns": 13}

PASS = 0
FAIL = []


def check(label, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label + (("  " + str(detail)) if detail else ""))


def find_shelf():
    for c in CANDIDATES:
        if c and os.path.isdir(c):
            return c
    return None


shelf = find_shelf()
if not shelf:
    print("FAIL could not find the Latin shelf. Looked in:")
    for c in CANDIDATES:
        print("       " + (c or "<WORDHOARD_LATIN_DIR unset>"))
    print("\nSet WORDHOARD_LATIN_DIR to the folder holding thomas-batch-NN.json.")
    sys.exit(1)

print(f"shelf     {shelf}")
print(f"registry  {REGISTRY}\n")

if not os.path.exists(REGISTRY):
    print(f"FAIL the committed registry is missing: {REGISTRY}")
    print("     Without it nothing can say whether a uid moved. This is fatal.")
    sys.exit(1)

committed = json.load(open(REGISTRY, encoding="utf-8"))["uids"]

batches = sorted(f for f in os.listdir(shelf)
                 if f.startswith("thomas-batch-") and f.endswith(".json")
                 and "permutation" not in f)
check("shelf holds batch files", bool(batches), batches)

# --------------------------------------------------------------- walk the shelf
passages, witnesses, tokens = [], [], []
for fn in batches:
    doc = json.load(open(os.path.join(shelf, fn), encoding="utf-8"))
    for p in doc.get("passages", []):
        passages.append((fn, p))
        for w in p.get("witnesses", []):
            witnesses.append((fn, p, w))
            for t in w.get("tokens", []):
                tokens.append((fn, p, w, t))

print("--- shape")
check("passage count", len(passages) == EXPECTED["passages"],
      f"{len(passages)} (expected {EXPECTED['passages']})")
check("witness count", len(witnesses) == EXPECTED["witnesses"],
      f"{len(witnesses)} (expected {EXPECTED['witnesses']})")
check("token count", len(tokens) == EXPECTED["tokens"],
      f"{len(tokens)} (expected {EXPECTED['tokens']})")

# ------------------------------------------------- 1. every record has its fields
print("\n--- every record carries its identity")
missing_uid = [p["id"] for _, p in passages if not p.get("uid")]
check("no passage lacks a uid", not missing_uid, missing_uid[:5] or "58/58 present")

missing_cit = [p.get("uid") for _, p in passages if not p.get("citation")]
check("no passage lacks a citation", not missing_cit, missing_cit[:5])

missing_legacy = [p.get("uid") for _, p in passages if not p.get("legacy_id")]
check("no passage lost its legacy id", not missing_legacy, missing_legacy[:5])

missing_waddr = [w.get("legacy_witness_id") for _, _, w in witnesses if not w.get("address")]
check("no witness lacks an address", not missing_waddr, missing_waddr[:5])

missing_taddr = [t.get("legacy_token_id") for _, _, _, t in tokens if not t.get("address")]
check("no token lacks an address", not missing_taddr, missing_taddr[:5])

# ------------------------------------- 2. THE check: no uid moved off the registry
print("\n--- identity has not moved (against the committed registry)")
unknown, moved = [], []
for _, p in passages:
    cit, uid = p.get("citation"), p.get("uid")
    if cit not in committed:
        unknown.append(cit)
    elif committed[cit] != uid:
        moved.append((cit, committed[cit], uid))
check("every citation is in the committed registry", not unknown, unknown[:5])
check("NO UID CHANGED against the committed registry", not moved, moved[:3])

# ------------------------------------------------------- 3. well-formed and unique
print("\n--- well-formed and unique")
bad = []
for _, p in passages:
    if not U.is_uid(p.get("uid") or ""):
        bad.append((p.get("citation"), p.get("uid")))
check("every uid is well-formed under wh_uid", not bad, bad[:5])

uids = [p.get("uid") for _, p in passages]
check("no two passages share a uid", len(set(uids)) == len(uids),
      f"{len(set(uids))} distinct / {len(uids)}")

cits = [p.get("citation") for _, p in passages]
check("no two passages share a citation", len(set(cits)) == len(cits),
      f"{len(set(cits))} distinct / {len(cits)}")

slugs = {}
for c in cits:
    s = c.split(":")[0]
    slugs[s] = slugs.get(s, 0) + 1
check("citation slugs are the mapped ones", slugs == EXPECTED_SLUGS, slugs)

# ------------------------------------------- 4. addresses hang off their own passage
print("\n--- addresses resolve to their own passage")
stray_w = []
for _, p, w in witnesses:
    try:
        if U.parse_address(w["address"])["uid"] != p["uid"]:
            stray_w.append(w["address"])
    except Exception as e:
        stray_w.append(f"{w.get('address')!r}: {e}")
check("every witness address parses and points home", not stray_w, stray_w[:3])

stray_t = []
for _, p, w, t in tokens:
    try:
        a = U.parse_address(t["address"])
        if a["uid"] != p["uid"]:
            stray_t.append(t["address"])
    except Exception as e:
        stray_t.append(f"{t.get('address')!r}: {e}")
check("every token address parses and points home", not stray_t, stray_t[:3])

# -------------------------------------------------- 6. a replay must mint nothing
print("\n--- replay: rebuilding the shelf mints nothing")
tmp = tempfile.mkdtemp()
try:
    copy = os.path.join(tmp, "wordhoard.uids.json")
    shutil.copy2(REGISTRY, copy)
    reg = U.WhUidRegistry(copy)
    ok = True
    for _, p in passages:
        if reg.uid_for(p["citation"]) != p["uid"]:
            ok = False
    check("replay returns the stored uid for every citation", ok)
    check("replay minted 0", reg.minted == 0,
          f"minted={reg.minted} reused={reg.reused}")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ------------------------------------------- 7. the shared grammar has not drifted
print("\n--- shared grammar with code-corpus")
sibling = os.path.join(REPO, "..", "code-corpus", "build", "uid.py")
if os.path.exists(sibling):
    try:
        CC = load("cc_uid", sibling)
        check("alphabet matches code-corpus (read from its own file)",
              CC.ALPHABET == U.ALPHABET, CC.ALPHABET)
        check("code-corpus still excludes I/L/O/U",
              not (set("ILOU") & set(CC.ALPHABET)))
        check("the two id spaces stay disjoint",
              not U.is_uid("asme-a17.1-2016-4K7M9X"))
    except Exception as e:
        check("code-corpus uid.py is importable for the pin", False, e)
else:
    # Not a failure: the sibling repo need not be checked out. But say so,
    # rather than printing a green line that means nothing.
    print("skip  code-corpus not checked out beside this repo -- pin not verified")
    print(f"      looked for {os.path.normpath(sibling)}")

print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
