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


# Measured 2026-09-26 from the vault batch files (Adoro te, Pange lingua) and
# data/hymn-sources/ (the three hymns printed from Britt 1922). Not estimated.
EXPECTED = {"stanzas": 38, "clauses": 109, "tokens": 768, "witnesses": 260, "alignments": 69}
EXPECTED_CLAUSES = {"hymns:adoro-te": 23, "hymns:pange-lingua": 12, "hymns:lauda-sion": 45,
                    "hymns:sacris-solemniis": 17, "hymns:verbum-supernum": 12}
# The batch hymns' records as committed at e9ed7f0, before the printed hymns
# were added after them: (lines, sha256 of those lines). They must never move.
BATCH_PREFIX = {"passages": (48, "c9b582e7d06aa6fc"), "witnesses": (136, "a0c1a713bb01146b"),
                "tokens": (263, "a8cb618ecc5a53c6"), "alignments": (19, "12ebace38a924b79")}
PRINTED_WORKS = {"hymns:lauda-sion", "hymns:sacris-solemniis", "hymns:verbum-supernum"}
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
# Adam's lemma answers (review.py) legitimately rewrite batch tokens; only
# then is tokens.jsonl's prefix allowed to move.
answered_batch = any('"adam-reviewed"' in line for line in
                     open(os.path.join(DATA, "tokens.jsonl"), encoding="utf-8").readlines()[:BATCH_PREFIX["tokens"][0]])
for fn, (n, want) in BATCH_PREFIX.items():
    with open(os.path.join(DATA, fn + ".jsonl"), "rb") as f:
        head = b"".join(f.readlines()[:n])
    if fn == "tokens" and answered_batch:
        print("skip  tokens.jsonl prefix: Adam's lemma answers have changed batch tokens")
        continue
    check(f"{fn}.jsonl: the Adoro te / Pange lingua records are byte-identical to e9ed7f0",
          hashlib.sha256(head).hexdigest()[:16] == want)

print("\n--- shape")
# A reviewed re-cut (data/hymn-sources/cut-reviewed.jsonl) changes a printed
# hymn's clause count, and its la.1 witnesses with it: the measure is of the
# draft cut, adjusted by exactly what Adam's answers change.
recut = {}
for st_cit, row in B.load_cut_reviews().items():
    slug, st = st_cit.split(":", 1)[1].split(".st")
    d = len(row["cut"]) - len(B.HYMNS[slug]["clauses"][int(st)])
    recut[f"hymns:{slug}"] = recut.get(f"hymns:{slug}", 0) + d
EXPECTED["clauses"] += sum(recut.values())
EXPECTED["witnesses"] += sum(recut.values())
for w, d in recut.items():
    EXPECTED_CLAUSES[w] += d
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
batch_clauses = [c for c in clauses if c["work"] not in PRINTED_WORKS]
printed_clauses = [c for c in clauses if c["work"] in PRINTED_WORKS]
check("every batch-hymn clause has an en.plain witness",
      {w["passage_uid"] for w in plains} == {c["uid"] for c in batch_clauses})
gen_printed = [w["address"] for w in witnesses if w["passage_uid"] in {c["uid"] for c in printed_clauses}
               and w["name"] != "la.1"]
check("a printed-hymn clause stores only its Latin (no wooden, plain or elegant witness is stored)",
      not gen_printed, gen_printed[:3])
check("the manifest says why each printed hymn has no plain or elegant, and how its wooden is made "
      "(dictionary glosses, at render time)",
      all(set(manifest["works"][w].get("not_stored", {})) == {"en.plain", "en.elegant"}
          and "DICTIONARY glosses" in manifest["works"][w].get("wooden_from", "")
          for w in PRINTED_WORKS))


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
check("every licence is PD, own, or (Whitaker only) free-grant",
      all(v in ("PD", "own") or (v == "free-grant" and k == "whitaker-words") for k, v in lic.items()), lic)
check("nothing from Perseus is merged in; enrichment keyed by CTS URN",
      "perseus" in manifest and not any("perseus" in k for k in manifest["sources"])
      and set(manifest["perseus"]["cts_urn"]) == set(manifest["works"]))

print("\n--- tokens")
missing_f = [t["address"] for t in tokens if any(f not in t for f in TOKEN_FIELDS)]
check("every token carries all eight fields (null allowed)", not missing_f, missing_f[:3])
empty = [t["address"] for t in tokens for f in TOKEN_FIELDS if t.get(f) == ""]
check("no field is an empty string -- absence is null", not empty, empty[:3])
printed_uids = {c["uid"] for c in printed_clauses}
no_prov = [t["address"] for t in tokens
           if not all(k in t for k in ("lemma_key", "provenance", "review"))
           or set(t["provenance"]) != ({"lemma", "parsing", "gloss"} if t["passage_uid"] in printed_uids
                                       else {"lemma", "parsing"})]
check("every token records where its lemma and parsing came from (D3), and a printed token its gloss",
      not no_prov, no_prov[:3])
check("surface, normalized and search_key are never null",
      all(t[f] for t in tokens for f in ("surface", "normalized", "search_key")))
check("gloss is never null on a batch hymn (its house draft)",
      all(t["gloss"] for t in tokens if t["passage_uid"] not in printed_uids))
check("a printed hymn's tokens carry no plain_form or syntax (there is no draft); a gloss only from "
      "Whitaker's dictionary rule or an override row",
      all(t["plain_form"] is None and t["syntax"] is None
          and (t["gloss"] is None or t["provenance"]["gloss"]["source"] in ("whitaker-words", "house",
                                                                             "adam-reviewed"))
          for t in tokens if t["passage_uid"] in printed_uids))
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
check("a printed-hymn passage has no legacy ids (there were none)",
      not [p for p in passages if p["work"] in PRINTED_WORKS and "legacy" in p])
check("every legacy row id resolves to the clause uid that claims it", not bad_lj, bad_lj[:3])
claimed = [x for c in batch_clauses for x in c["legacy"]["unit_ids"]]
check("every legacy row is claimed by exactly one clause",
      sorted(claimed) == sorted(lj) and len(set(claimed)) == len(claimed))

print("\n--- the printed hymns (Britt 1922, data/hymn-sources/)")
L = load("lemma_spine")
for w in sorted(PRINTED_WORKS):
    sf = manifest["works"][w].get("source_file")
    check(f"{w} names its source file, and it exists", sf and os.path.exists(os.path.join(REPO, sf)), sf)
sf = os.path.join(REPO, manifest["works"]["hymns:lauda-sion"]["source_file"])
raw_src = open(sf, "rb").read()
src_doc = json.loads(raw_src.decode("utf-8"))
check("the source file's sha256 is in the manifest's inputs",
      manifest["inputs_sha256"].get(os.path.basename(sf)) == hashlib.sha256(raw_src).hexdigest())
check("the edition is named, PD, with its scan", src_doc["edition"]["license"] == "PD"
      and src_doc["scan"]["archive_id"] == "hymnsofbreviarym00britrich"
      and all(p["image_sha256"] and p["page"] for p in src_doc["scan"]["pages_read"]))
bad_src, bad_page = [], []
for c in printed_clauses:
    slug = c["work"].split(":", 1)[1]
    sp = next(s for s in src_doc["hymns"][slug]["stanzas"] if s["stanza"] == c["stanza"])
    la = wmap[U.address(c["uid"], "la.1")]
    if la["text"].split("\n") != sp["la"][c["lines"][0] - 1:c["lines"][1]]:
        bad_src.append(c["citation"])
    if la.get("page") != sp["page"]:
        bad_page.append(c["citation"])
check("every printed clause's Latin is its lines of the source file, exactly", not bad_src, bad_src[:3])
check("every printed witness records its printed page", not bad_page and all(
    w.get("page") for w in witnesses
    if by_uid[w["passage_uid"]]["work"] in PRINTED_WORKS), bad_page[:3])
st_rend = [w for w in witnesses if by_uid[w["passage_uid"]]["work"] in PRINTED_WORKS
           and by_uid[w["passage_uid"]]["unit"] == "stanza"]
check("every printed stanza has en.singable and en.literal, and nothing else",
      sorted(w["name"] for w in st_rend) == sorted(["en.singable", "en.literal"] * sum(
          1 for s in stanzas if s["work"] in PRINTED_WORKS)))
check("every printed witness is PD and verified against the scan",
      all(manifest["sources"][w["source"]]["license"] == "PD" and manifest["sources"][w["source"]]["verified"]
          for w in witnesses if by_uid[w["passage_uid"]]["work"] in PRINTED_WORKS))
nowhy_all = [c["citation"] for c in printed_clauses if not c["cut"].get("why")]
check("every printed-hymn cut, one-line clauses included, says why", not nowhy_all, nowhy_all[:3])
check("every printed-hymn cut is open or answered by Adam",
      all(c["cut"].get("review") in ("open", "adam-reviewed") for c in printed_clauses))
spine = {}
with open(os.path.join(REPO, "data", "lemmas", "whitaker-la", "hymns.analyses.jsonl"), encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        spine[r["form"]] = r["analyses"]
drift = [t["address"] for t in tokens if t["passage_uid"] in printed_uids
         and (L.resolve_undrafted(spine[t["search_key"]])[:3] != (t["lemma"], t["lemma_key"], t["parsing"]))
         and t["provenance"]["lemma"]["source"] != "adam-reviewed"
         and t["provenance"]["parsing"]["source"] != "adam-reviewed"]
check("every printed token's lemma and parsing are what the spine's no-draft rule gives", not drift, drift[:3])
invented = [t["address"] for t in tokens if t["passage_uid"] in printed_uids
            and ((t["lemma"] and t["provenance"]["lemma"]["source"] not in ("whitaker-words", "adam-reviewed"))
                 or (t["parsing"] and t["provenance"]["parsing"]["source"] not in ("whitaker-words", "adam-reviewed")))]
check("no printed token has a lemma or parsing from anywhere but Whitaker or Adam", not invented, invented[:3])
unflagged = [t["address"] for t in tokens if t["passage_uid"] in printed_uids and t["lemma"] is None
             and not t["review"]]
check("a printed token with no lemma is flagged for review", not unflagged, unflagged[:3])

print("\n--- the collation: Adoro te's received Latin against Britt 1922 (README s.10)")
rms = manifest["sources"]["roman-missal-received"]
col = rms.get("collation", {}).get("hymns:adoro-te")
check("the received text's source carries the Adoro te collation", bool(col))
if col:
    cpath = os.path.join(REPO, col["file"])
    craw = open(cpath, "rb").read()
    cdoc = json.loads(craw.decode("utf-8"))
    check("the collation file exists and its sha256 is the manifest's",
          hashlib.sha256(craw).hexdigest() == col["file_sha256"])
    check("... and it is NOT an input of the text (inputs_sha256 unchanged by a collation)",
          os.path.basename(cpath) not in manifest["inputs_sha256"])
    check("the collation names Britt no. 79, pp. 190-191, each page image hashed",
          cdoc["edition"]["britt_number"] == 79 and [p["page"] for p in cdoc["scan"]["pages_read"]] == [190, 191]
          and all(re.fullmatch(r"[0-9a-f]{64}", p["image_sha256"]) for p in cdoc["scan"]["pages_read"]))
    diffs, cstats = B.collate(cdoc, passages, witnesses, tokens)
    kinds = {}
    for d in diffs:
        kinds[d["kind"]] = kinds.get(d["kind"], 0) + 1
    check("re-collated from the committed JSONL, the counts are the manifest's",
          cstats == col["words"] and len(diffs) == col["differences"] and kinds == col["by_kind"], (cstats, kinds))
    # Measured 2026-09-26 from the page images: 149 received words, 148 printed.
    check("every printed word pairs with a received one (149 received, 148 printed, 148 paired)",
          (cstats["received_words"], cstats["printed_words"], cstats["paired"]) == (149, 148, 148), cstats)
    check("25 differences: 12 punctuation, 10 orthography, 1 capital, 1 spelling, 1 word",
          kinds == {"punctuation": 12, "orthography": 10, "capital": 1, "spelling": 1, "word": 1}, kinds)
    sk = sorted((d["received"], d["britt"] or "") for d in diffs if d["kind"] in ("spelling", "word"))
    check("only two change a search_key: paenitens/pœnitens and the Amen Britt does not print",
          sk == [("Amen.", ""), ("paenitens", "pœnitens")], sk)
    orth = [d for d in diffs if d["kind"] == "orthography"
            and B.search_key(d["received"]) != B.search_key(d["britt"])]
    check("every orthography difference folds to the same search_key", not orth, orth[:2])
    toks_by = {t["address"] for t in tokens}
    check("every difference names a real received token (none is Britt-only)",
          all(d["address"] in toks_by for d in diffs))
    rv = col["review"]
    check("the review counts add up, and the source is verified only when every row is answered `received`",
          rv["answered"] + rv["open"] == len(diffs)
          and rms["verified"] == (rv["open"] == 0 and rv["britt"] == 0))
print("\n--- glosses: Whitaker dictionary glosses on the printed hymns (README s.11)")
WG = load("whitaker_gloss")
gm = manifest.get("gloss") or {}
ptoks = [t for t in tokens if t["passage_uid"] in printed_uids]
lemmas_tab = WG.load_lemmas()
check("the manifest's gloss block is dictionary, whitaker-words, free-grant, and covers exactly the "
      "printed hymns", gm.get("kind") == "dictionary" and gm.get("source") == "whitaker-words"
      and gm.get("license") == "free-grant" and set(gm.get("applies_to", ())) == PRINTED_WORKS)
check("... and says it is NOT a contextual translation", "NOT a contextual translation" in gm.get("not", ""))
check("... with every rule id and what it does", [r["id"] for r in gm.get("rules", [])] == list(WG.RULE_ORDER))
check("the Whitaker source record says it now supplies glosses too",
      "gloss" in manifest["sources"]["whitaker-words"]["what"])
redo = [t["address"] for t in ptoks if t["provenance"]["gloss"].get("kind") != "contextual"
        and WG.gloss_for(t, lemmas_tab) != (t["gloss"], t["provenance"]["gloss"])]
check("every printed token's gloss is what the rule gives from the committed lemma table (never invented)",
      not redo, redo[:3])
# Measured 2026-09-26: 505 printed tokens, 307 with a lemma, 282 glossed (91.9% of those with a
# lemma, 55.8% of all): pron-case 13, first-sense 269. The 223 without: 198 have no lemma yet (the
# lemma sheet), 23 have a lemma whose WORDS entries disagree (in, ad, cum, juxta, vel), 1 first
# sense is no word gloss (sacramentum), 1 entry has no meaning line (memento, a UNIQUES form).
counted = (gm.get("tokens"), gm.get("tokens_with_lemma"), gm.get("glossed"), gm.get("glossed_of_lemma"))
check("the gloss block's counts are the tokens'",
      counted == (len(ptoks), sum(1 for t in ptoks if t["lemma"]), sum(1 for t in ptoks if t["gloss"]),
                  sum(1 for t in ptoks if t["gloss"] and t["lemma"]))
      and gm.get("none") == sum(1 for t in ptoks if t["gloss"] is None)
      == sum(gm.get("none_by_reason", {}).values()), counted)
check("every null gloss says why, and names no source",
      all(t["provenance"]["gloss"]["source"] is None and t["provenance"]["gloss"]["why"]
          for t in ptoks if t["gloss"] is None))
# Adam's lemma and cut answers move these numbers (a new lemma is a new gloss): pin them as measured
# only while none is applied to a printed hymn.
answered = any(t["provenance"]["lemma"]["source"] == "adam-reviewed" for t in ptoks) or any(
    c["cut"].get("review") == "adam-reviewed" for c in printed_clauses)
if answered:
    print("skip  Adam's answers are applied to the printed hymns: the as-measured gloss counts are not pinned")
else:
    check("coverage as measured (before Adam's answers): 282 of 505, i.e. 282 of the 307 with a lemma",
          counted == (505, 307, 282, 282), counted)
    check("... split by rule: pron-case 13, first-sense 269",
          gm.get("by_rule") == {"pron-case": 13, "first-sense": 269}, gm.get("by_rule"))
    check("... and 223 null: 198 no lemma, 23 entries disagree, 1 no word gloss, 1 no meaning line",
          sorted(gm.get("none_by_reason", {}).values()) == [1, 1, 23, 198], gm.get("none_by_reason"))
check("a printed token with no lemma has no gloss", all(t["gloss"] is None for t in ptoks if not t["lemma"]))
notfrom = []
for t in ptoks:
    pg = t["provenance"]["gloss"]
    if pg.get("kind") != "dictionary":
        continue
    keys = [t["lemma_key"]] if t["lemma_key"] else t["provenance"]["lemma"]["whitaker"]
    words = " ".join(WG.meaning(lemmas_tab[k]) or "" for k in keys).replace("_", " ").lower()
    if not all(re.search(r"(?<![a-z])" + re.escape(w.lower()) + r"(?![a-z])", words)
               for w in t["gloss"].split("-") if w):
        notfrom.append((t["surface"], t["gloss"]))
check("every dictionary gloss is words of its WORDS meaning line", not notfrom, notfrom[:3])
check("hyphenated: one chunk per Latin word, as the house glosses",
      all(" " not in t["gloss"] for t in ptoks if t["gloss"]))
batch_prov = [t["address"] for t in tokens if t["passage_uid"] not in printed_uids and "gloss" in t["provenance"]]
check("the batch hymns' house glosses are not touched (no gloss provenance added there)", not batch_prov)
gov = os.path.join(DATA, "gloss-overrides.jsonl")
check("the gloss override file exists and is read by the build (empty: no house draft invented)",
      os.path.exists(gov) and WG.load_overrides(gov) == {} and gm["overrides"]["applied"] == 0)

print("\n--- the gloss rule, on fixtures")


def row(m):
    return {"entries": [{"meaning": m}]}


def fx(key, m, parse=None, lemma="x"):
    tok = {"lemma": lemma, "lemma_key": key,
           "provenance": {"lemma": {}, "parsing": {"whitaker": parse}}}
    return WG.gloss_for(tok, {key: row(m)})


check("first-sense: cut at ';' then ','; a slashed group gives its first member",
      fx("do, dare  V", "give; dedicate; grant/bestow;")[0] == "give"
      and fx("facio  V", "make/build/construct; do;")[0] == "make"
      and fx("jubilatio  N", "wild/loud shouting; whooping;")[0] == "wild-shouting")
check("first-sense: parentheses and brackets off; a verb's 'to', a noun's article dropped",
      fx("video  V", "(PASS) seem, look at;")[0] == "seem"
      and fx("eo  V", "to go, walk;")[0] == "go" and fx("res  N", "a thing; affair;")[0] == "thing"
      and fx("opus  N", "[opus est => useful] need; work;")[0] == "need")
check("first-sense: an interjection's '!' separates senses; '_' joins words",
      fx("ecce  INTERJ", "behold! see! look!;")[0] == "behold"
      and fx("ceterus  ADJ", "the_other; the_others (pl.).")[0] == "the-other")
check("first-sense: more than four words is null, with the reason",
      fx("sacramentum  N", "sum deposited in a civil process, guaranty;")[0] is None
      and "not a word gloss" in fx("sacramentum  N", "sum deposited in a civil process, guaranty;")[1]["why"])
check("pron-case: every parse in one slot picks the first English form for it",
      fx("nos  PRON", "we (pl.), us;", ["PRON 5 3 ABL P C", "PRON 5 3 DAT P C"]) ==
      ("us", {"source": "whitaker-words", "by": "lemma_key", "rule": "pron-case", "kind": "dictionary"})
      and fx("nos  PRON", "we (pl.), us;", "PRON 5 3 NOM P C")[0] == "we")
check("pron-case: parses in two slots fall through to first-sense",
      fx("nos  PRON", "we (pl.), us;", ["PRON 5 3 ACC P C", "PRON 5 3 NOM P C"]) ==
      ("we", {"source": "whitaker-words", "by": "lemma_key", "rule": "first-sense", "kind": "dictionary"}))
same = {"lemma": "in", "lemma_key": None,
        "provenance": {"lemma": {"whitaker": ["in  PREP  ABL", "in  PREP  ACC"]}, "parsing": {}}}
two = {"in  PREP  ABL": row("in, on;"), "in  PREP  ACC": row("into;")}
check("a same-lemma token is glossed only when every entry agrees; else null, naming them",
      WG.gloss_for(same, two)[0] is None and "ABL -> in; PREP  ACC -> into" in WG.gloss_for(same, two)[1]["why"]
      and WG.gloss_for(same, {"in  PREP  ABL": row("in, on;"), "in  PREP  ACC": row("in; into;")})[0] == "in")
check("no lemma, no gloss", WG.gloss_for({"lemma": None, "lemma_key": None, "provenance": {}}, {})[0] is None)
ov = {"address": "a", "surface": "Lauda", "gloss": "praise", "layer": "house", "draft": True,
      "drafted_on": "2026-09-26"}
g, _, pv = WG.apply_override("recommend", None, {"source": "whitaker-words", "rule": "first-sense"}, "Lauda", ov)
check("an override row replaces the dictionary gloss, keeps it under `was`, and a draft says so",
      g == "praise" and pv["kind"] == "contextual" and pv["draft"] is True
      and pv["was"] == {"value": "recommend", "source": "whitaker-words", "rule": "first-sense"})

hop = manifest["sources"]["hopkins-1918"]
check("Hopkins stays unverified, with the finding recorded (the 1918 Poems does not print it)",
      hop["verified"] is False and "does not print" in hop.get("finding", ""))

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
    for c in batch_clauses:
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
    wood = [c["citation"] for c in batch_clauses
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
