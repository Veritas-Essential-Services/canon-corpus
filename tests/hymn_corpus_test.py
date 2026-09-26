#!/usr/bin/env python3
"""
hymn_corpus_test.py -- the validator for data/hymns/*.jsonl (launch plan D1-D2).

Run:  python3 tests/hymn_corpus_test.py

TWO HALVES
    OFFLINE (always runs): validates the four committed JSONL files and their
    manifest against the schema in pipeline/README-hymn-jsonl.md -- every
    record keyed by uid, every token carrying its eight fields, `plain` never
    stored, the clause partition exact, the licence gate held, and a registry
    replay minting zero.

    AGAINST THE VAULT (runs when the Latin shelf is reachable, says so when
    not): proves the D1 fix. It first REPRODUCES the defect -- joining the
    permutation files to the passage files on `unit_id` leaves 27 of 64 and
    10 of 20 rows joined to nothing -- then shows that through uids all 84
    rows resolve, that every legacy plain line re-renders from the JSONL, and
    that a rebuild is byte-identical and mints nothing.

WHY THE FIRST HALF MATTERS MORE
    The JSONL is now the source of truth; the vault batch files are its
    history. A consumer never has the vault. So the files have to prove their
    own integrity without it.
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PIPE = os.path.join(REPO, "pipeline")
DATA = os.path.join(REPO, "data", "hymns")
REGISTRY = os.path.join(REPO, "data", "uids", "wordhoard.uids.json")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(PIPE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, PIPE)
    spec.loader.exec_module(mod)
    return mod


U = load("wh_uid")
B = load("build_hymn_corpus")

PASS = 0
FAIL = []


def check(label, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label + (("  " + str(detail)) if detail else ""))


def jsonl(name):
    out = []
    with open(os.path.join(DATA, name + ".jsonl"), encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            out.append(json.loads(line))
    return out


# Measured 2026-09-26 from the vault batch files. Not estimated.
EXPECTED = {"stanzas": 13, "clauses": 35, "tokens": 263, "witnesses": 136, "alignments": 19}
EXPECTED_CLAUSES = {"hymns:adoro-te": 23, "hymns:pange-lingua": 12}
TOKEN_FIELDS = ("surface", "normalized", "search_key", "translit",
                "lemma", "parsing", "gloss", "plain_form")

# ================================================================ OFFLINE
print("--- files")
for fn in [f + ".jsonl" for f in B.FILES] + ["manifest.json"]:
    check(f"{fn} exists", os.path.exists(os.path.join(DATA, fn)))
manifest = json.load(open(os.path.join(DATA, "manifest.json"), encoding="utf-8"))
passages, witnesses, tokens, alignments = (jsonl(f) for f in B.FILES)
for fn, want in manifest["files_sha256"].items():
    got = hashlib.sha256(open(os.path.join(DATA, fn), "rb").read()).hexdigest()
    check(f"{fn} matches its manifest checksum", got == want)
check("manifest names the schema and the doc",
      manifest.get("schema") == B.SCHEMA and os.path.exists(os.path.join(REPO, manifest["doc"])))
check("row unit is the clause", manifest.get("row_unit") == "clause")

print("\n--- shape")
clauses = [p for p in passages if p["unit"] == "clause"]
stanzas = [p for p in passages if p["unit"] == "stanza"]
check("stanza count", len(stanzas) == EXPECTED["stanzas"], len(stanzas))
check("clause count", len(clauses) == EXPECTED["clauses"], len(clauses))
check("token count", len(tokens) == EXPECTED["tokens"], len(tokens))
check("witness count", len(witnesses) == EXPECTED["witnesses"], len(witnesses))
check("alignment count", len(alignments) == EXPECTED["alignments"], len(alignments))
per_work = {}
for c in clauses:
    per_work[c["work"]] = per_work.get(c["work"], 0) + 1
check("clauses per hymn", per_work == EXPECTED_CLAUSES, per_work)
check("every passage is a stanza or a clause", len(passages) == len(clauses) + len(stanzas))

print("\n--- passages: identity")
committed = json.load(open(REGISTRY, encoding="utf-8"))["uids"]
by_uid = {p["uid"]: p for p in passages}
check("every uid is well-formed", all(U.is_uid(p["uid"]) for p in passages))
check("no two passages share a uid", len(by_uid) == len(passages))
check("no two passages share a citation", len({p["citation"] for p in passages}) == len(passages))
moved = [(p["citation"], p["uid"]) for p in passages if committed.get(p["citation"]) != p["uid"]]
check("every uid is the committed registry's uid for its citation", not moved, moved[:3])
bad_cit = [c["citation"] for c in clauses
           if not re.fullmatch(r"hymns:[a-z-]+\.st\d+\.c\d+", c["citation"])
           or c["citation"] != f"{c['work']}.st{c['stanza']}.c{c['clause']}"]
check("clause citations are <work>.st<n>.c<m>", not bad_cit, bad_cit[:3])
la_leak = [p["citation"] for p in passages if re.search(r"(^|[.:/])la([.:/]|$)", p["citation"])]
check("no language code baked into any citation", not la_leak, la_leak[:3])

print("\n--- the clause partition")
bad_part = []
for s in stanzas:
    kids = sorted((c for c in clauses if c["stanza_uid"] == s["uid"]), key=lambda c: c["clause"])
    if [c["uid"] for c in kids] != s["clauses"]:
        bad_part.append((s["citation"], "clauses list"))
        continue
    expect = 1
    for i, c in enumerate(kids, 1):
        a, b = c["lines"]
        if c["clause"] != i or a != expect or b < a:
            bad_part.append((c["citation"], c["lines"]))
        expect = b + 1
    if expect - 1 != s["lines"][1]:
        bad_part.append((s["citation"], "lines not covered"))
check("every stanza is partitioned exactly by its clauses", not bad_part, bad_part[:3])
orph = [c["citation"] for c in clauses if by_uid.get(c["stanza_uid"], {}).get("unit") != "stanza"]
check("every clause points at a stanza", not orph, orph[:3])
nowhy = [c["citation"] for c in clauses if c["lines"][1] > c["lines"][0] and not (c.get("cut") or {}).get("why")]
check("every joined clause records why its lines were joined", not nowhy, nowhy[:3])

print("\n--- witnesses")
wmap = {}
bad_w = []
for w in witnesses:
    try:
        a = U.parse_address(w["address"])
        if a["uid"] != w["passage_uid"] or a["witness"] != w["name"] or w["passage_uid"] not in by_uid:
            bad_w.append(w["address"])
    except Exception as e:
        bad_w.append(f"{w.get('address')!r}: {e}")
    wmap[w["address"]] = w
check("every witness address parses and points home", not bad_w, bad_w[:3])
check("no two witnesses share an address", len(wmap) == len(witnesses))
ror = {}
for w in witnesses:
    if w.get("reading_of_record"):
        ror.setdefault(w["passage_uid"], []).append(w["name"])
check("every clause has exactly one reading of record, la.1",
      all(ror.get(c["uid"]) == ["la.1"] for c in clauses))
check("the Latin is stored once: no stanza carries la.1",
      not [w for w in witnesses if w["name"] == "la.1" and by_uid[w["passage_uid"]]["unit"] == "stanza"])
gen_text = [w["address"] for w in witnesses if w.get("generated") and w.get("text") is not None]
check("a generated witness stores no text", not gen_text, gen_text[:3])
plains = [w for w in witnesses if w["name"] == "en.plain"]
check("every clause has an en.plain witness", {w["passage_uid"] for w in plains} == {c["uid"] for c in clauses})


def keys_named(obj, name):
    if isinstance(obj, dict):
        return any(k == name or keys_named(v, name) for k, v in obj.items())
    if isinstance(obj, list):
        return any(keys_named(v, name) for v in obj)
    return False


stored_plain = [r.get("address") or r.get("uid") for r in passages + witnesses + tokens + alignments
                if keys_named(r, "plain") or keys_named(r, "wooden")]
check("`plain` (and the wooden line) are never stored, in any file", not stored_plain, stored_plain[:3])
unknown_src = [w["address"] for w in witnesses if w.get("source") not in manifest["sources"]]
check("every witness names a source in the manifest", not unknown_src, unknown_src[:3])

print("\n--- the licence gate (D4)")
lic = {k: v.get("license") for k, v in manifest["sources"].items()}
check("every source records its licence", all(lic.values()), lic)
check("every licence is PD or own", all(v in B.ALLOWED_LICENSES for v in lic.values()), lic)
check("nothing from Perseus is merged in; enrichment keyed by CTS URN",
      "perseus" in manifest and not any("perseus" in k for k in manifest["sources"])
      and set(manifest["perseus"]["cts_urn"]) == set(manifest["works"]))

print("\n--- tokens")
missing_f = [t["address"] for t in tokens if any(f not in t for f in TOKEN_FIELDS)]
check("every token carries all eight fields (null allowed)", not missing_f, missing_f[:3])
empty = [t["address"] for t in tokens for f in TOKEN_FIELDS if t.get(f) == ""]
check("no field is an empty string -- absence is null", not empty, empty[:3])
check("surface, normalized, search_key and gloss are never null",
      all(t[f] for t in tokens for f in ("surface", "normalized", "search_key", "gloss")))
check("normalized is NFC(surface)",
      all(t["normalized"] == unicodedata.normalize("NFC", t["surface"]) for t in tokens))
check("search_key is the fold of normalized", all(t["search_key"] == B.search_key(t["normalized"]) for t in tokens))
check("translit is null on the Latin witness", all(t["translit"] is None for t in tokens if t["witness"] == "la.1"))
bad_t = []
for t in tokens:
    try:
        a = U.parse_address(t["address"])
        if a["uid"] != t["passage_uid"] or a["witness"] != f"{t['witness']}.t{t['position']:02d}":
            bad_t.append(t["address"])
    except Exception as e:
        bad_t.append(f"{t.get('address')!r}: {e}")
check("every token address parses and points home", not bad_t, bad_t[:3])

toks_of = {}
for t in tokens:
    toks_of.setdefault(t["passage_uid"], []).append(t)
check("tokens hang only on clauses", set(toks_of) == {c["uid"] for c in clauses})
bad_seq, bad_text, bad_line = [], [], []
for c in clauses:
    ts = toks_of[c["uid"]]
    if [t["position"] for t in ts] != list(range(1, len(ts) + 1)):
        bad_seq.append(c["citation"])
    la = wmap[U.address(c["uid"], "la.1")]
    if B.tokenize(la["text"]) != [t["surface"] for t in ts]:
        bad_text.append(c["citation"])
    if la["text"].count("\n") != c["lines"][1] - c["lines"][0] \
            or any(not c["lines"][0] <= t["line"] <= c["lines"][1] for t in ts):
        bad_line.append(c["citation"])
check("token positions run 1..n in every clause", not bad_seq, bad_seq[:3])
check("every clause's Latin re-tokenizes to exactly its tokens", not bad_text, bad_text[:3])
check("line numbers agree with the clause's lines", not bad_line, bad_line[:3])

print("\n--- plain is generated from prose_order")
bad_perm, empty_r, lower_i = [], [], []
for w in plains:
    ts = toks_of[w["passage_uid"]]
    p = B.permutation_problems(len(ts), w["prose_order"], w["absorbed"])
    if p:
        bad_perm.append((by_uid[w["passage_uid"]]["citation"], p))
    txt = B.render_plain(ts, w)
    if not txt or not B.render_wooden(ts):
        empty_r.append(w["address"])
    if re.search(r"(^|\s)i-", txt):
        lower_i.append(txt[:20])
check("every prose_order uses each token exactly once (or absorbs it)", not bad_perm, bad_perm[:3])
check("every clause renders a plain and a wooden line", not empty_r, empty_r[:3])
check("the pronoun I is never lower-cased in plain", not lower_i, len(lower_i))

print("\n--- alignments")
bad_al = []
for al in alignments:
    for side in al["a"] + al["b"]:
        if side["address"] not in wmap:
            bad_al.append(side["address"])
    n_a, n_b = len(al["a"]), len(al["b"])
    want = f"{'1' if n_a == 1 else 'many'}:{'1' if n_b == 1 else 'many'}"
    if al["type"] != want or al["confidence"] not in ("high", "medium", "low"):
        bad_al.append(al["alignment_id"])
check("every alignment side resolves to a witness, and its type fits", not bad_al, bad_al[:3])
drift = []
for al in (x for x in alignments if x["level"] == "section"):
    st = U.parse_address(al["a"][0]["address"])["uid"]
    if [U.parse_address(s["address"])["uid"] for s in al["b"]] != by_uid[st]["clauses"]:
        drift.append(al["alignment_id"])
check("section alignments agree with stanza membership", not drift, drift[:3])
check("every stanza-level rendering is aligned to its clauses",
      {x["a"][0]["address"] for x in alignments} ==
      {w["address"] for w in witnesses if by_uid[w["passage_uid"]]["unit"] == "stanza"})

print("\n--- the D1 join, from the committed files alone")
lj = manifest["legacy_join"]
# 27 Adoro te line rows + 12 Pange lingua clause rows. 37 of the 39 joined to
# nothing; the other two (Pange st2, st3) joined only because a one-clause
# stanza happened to share the stanza's id.
check("39 legacy hymn rows in the join table (27 + 12)", len(lj) == 39, len(lj))
bad_lj = [k for k, u in lj.items() if u not in by_uid or k not in by_uid[u]["legacy"]["unit_ids"]]
check("every legacy row id resolves to the clause uid that claims it", not bad_lj, bad_lj[:3])
claimed = [x for c in clauses for x in c["legacy"]["unit_ids"]]
check("every legacy row is claimed by exactly one clause",
      sorted(claimed) == sorted(lj) and len(set(claimed)) == len(claimed))

print("\n--- replay: the registry mints nothing")
tmp = tempfile.mkdtemp()
try:
    copy = os.path.join(tmp, "r.json")
    shutil.copy2(REGISTRY, copy)
    reg = U.WhUidRegistry(copy)
    check("replay returns the stored uid for every citation",
          all(reg.uid_for(p["citation"]) == p["uid"] for p in passages))
    check("replay minted 0", reg.minted == 0, reg.stats())
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ============================================================ AGAINST THE VAULT
print("\n--- against the vault: the defect, reproduced, then fixed")
src = next((c for c in B.SOURCE_CANDIDATES if c and os.path.isdir(c)), None)
if not src:
    print("skip  the Latin shelf is not reachable -- the D1 proof against the")
    print("      legacy files did not run. Set WORDHOARD_LATIN_DIR to run it.")
else:
    print(f"shelf {src}")
    legacy = {}
    for bn in ("01", "02"):
        batch = json.load(open(os.path.join(src, f"thomas-batch-{bn}.json"), encoding="utf-8"))
        rows = json.load(open(os.path.join(src, f"thomas-batch-{bn}-permutations.json"),
                              encoding="utf-8"))["rows"]
        pid = {p["id"]: p for p in batch["passages"]}
        by_id = sum(1 for r in rows if r["unit_id"] not in pid)
        legacy[bn] = (batch, rows, pid, by_id)
    check("BEFORE: joined on unit_id, 27 of 64 rows in batch 01 join to nothing",
          (len(legacy["01"][1]), legacy["01"][3]) == (64, 27),
          f"{legacy['01'][3]} of {len(legacy['01'][1])}")
    check("BEFORE: joined on unit_id, 10 of 20 rows in batch 02 join to nothing",
          (len(legacy["02"][1]), legacy["02"][3]) == (20, 10),
          f"{legacy['02'][3]} of {len(legacy['02'][1])}")

    unjoined = []
    for bn, (batch, rows, pid, _) in legacy.items():
        for r in rows:
            uid = lj.get(r["unit_id"]) or (pid.get(r["unit_id"]) or {}).get("uid")
            if not uid or (r["unit_id"] in lj and uid not in by_uid):
                unjoined.append(r["unit_id"])
    check("AFTER: all 84 rows resolve to a uid (hymns via the clause, prose via its passage)",
          not unjoined, unjoined[:5])
    hymn_rows = [r for bn in legacy for r in legacy[bn][1] if r["unit_id"] in lj]
    check("AFTER: no hymn row joins by unit_id any more -- every one lands on a clause uid",
          len(hymn_rows) == 39 and all(by_uid[lj[r["unit_id"]]]["unit"] == "clause" for r in hymn_rows))

    # Lossless: each legacy plain line re-renders from the JSONL.
    def fix_i(s):
        return re.sub(r"(^|\s)i-", r"\1I-", s)

    mismatch = []
    for c in clauses:
        w = wmap[U.address(c["uid"], "en.plain")]
        got = B.render_plain(toks_of[c["uid"]], w)
        olds = [next(r for bn in legacy for r in legacy[bn][1] if r["unit_id"] == u)["plain"]
                for u in c["legacy"]["unit_ids"]]
        if len(olds) == 1:
            ok = got == fix_i(olds[0])
        else:   # joined lines: the old lines, end to end
            ok = got.lower() == " ".join(olds).lower()
        if not ok:
            mismatch.append(c["citation"])
    check("every legacy plain line re-renders from the JSONL (35/35 clauses)",
          not mismatch, mismatch[:3])
    wood = [c["citation"] for c in clauses
            if B.render_wooden(toks_of[c["uid"]]) !=
            " ".join(next(r for bn in legacy for r in legacy[bn][1] if r["unit_id"] == u)["wooden"]
                     for u in c["legacy"]["unit_ids"])]
    check("every legacy wooden line re-renders from the token glosses", not wood, wood[:3])

    # Rebuild: byte-identical, zero minted.
    tmp = tempfile.mkdtemp()
    try:
        copy = os.path.join(tmp, "r.json")
        shutil.copy2(REGISTRY, copy)
        reg = U.WhUidRegistry(copy)
        data, man = B.build(src, reg)
        blobs = B.render_all(data, man)
        check("rebuild minted 0", reg.minted == 0, reg.stats())
        diff = [fn for fn, blob in blobs.items() if open(os.path.join(DATA, fn), "rb").read() != blob]
        check("rebuild is byte-identical to the committed files", not diff, diff)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
