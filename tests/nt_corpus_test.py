#!/usr/bin/env python3
# prov: 2026-09-26 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-26 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
# fable_review: pending
"""
nt_corpus_test.py -- the validator for data/nt/ (launch plan D2-D5, the
Greek half): the whole NT from the Robinson-Pierpont text, one folder per
book since 2026-10-02, and within it the John 1:1-18 pilot, whose counts and
house drafts are checked as they were.

Run:  python3 tests/nt_corpus_test.py

TWO HALVES, as in hymn_corpus_test.py
    OFFLINE (always runs): the committed JSONL shards and their manifest
    against pipeline/README-nt-jsonl.md -- every record keyed by an EXISTING
    verse uid, every token carrying its eight fields, the licence gate held
    (PD or own only, with the evidence recorded), nothing from MorphGNT,
    SBLGNT or Perseus, and a frozen registry replay minting zero. Also the
    transliteration scheme and the parsing grammar, on fixtures. The house
    drafts (2026-09-26): every gloss-override row points at a real token
    whose surface it names; every prose_order is a permutation of its verse's
    token positions (or the documented subset, with the rest absorbed); every
    draft row and every witness built from one says draft, and its source is
    licence own; a row Adam has answered (pipeline/review.py) says
    adam-reviewed and reviewed_on instead.

    AGAINST THE PINNED INPUTS (runs when data/corpus/ holds them, says so
    when not; `build_nt_corpus.py --fetch` gets them): a rebuild is
    byte-identical and mints nothing; every lemma is Strong's headword for
    its number; the transliteration agrees with the Strong's dictionary's own
    on every one-word headword but one; and the Beta-code cross-check really
    does stop on a changed letter or code.
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
# Greek in failure messages must print on a Windows console (cp1252 by default).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PIPE = os.path.join(REPO, "pipeline")
DATA = os.path.join(REPO, "data", "nt")
REGISTRY = os.path.join(REPO, "data", "uids", "wordhoard.uids.json")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(PIPE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, PIPE)
    spec.loader.exec_module(mod)
    return mod


U = load("wh_uid")
B = load("build_nt_corpus")
G = B.G
KJV = load("build_witnesses")

PASS = 0
FAIL = []


def check(label, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label + (("  " + str(detail)) if detail else ""))


# Measured 2026-10-02 from RP2018 (byztxt v3.3.2), the whole NT. Not estimated.
EXPECTED_NT = {"verses": 7953, "tokens": 140149, "witnesses": 7971, "alignments": 7953,
               "books": 27, "distinct_lemmas": 5380, "finite_verbs": 19571, "flagged": 28,
               # the paradigm rule and the def-head repairs (2026-10-02) took this
               # from 124,516 (88.8%) to 131,631 (93.9%)
               "glossed": 131631,
               "gloss_by_rule": {"kjv-form": 27855, "paradigm": 7103, "kjv-sole": 20489,
                                 "kjv-in-def": 52792, "def-head": 23255},
               "pronoun_nulls": 5,       # crasis only (kamoi "and me" is not "me")
               # the Byzantine text lacks these Textus Receptus verses; they keep their uids
               "kjv_without_grc": ["kjv:Acts.15.34", "kjv:Acts.24.7", "kjv:Acts.8.37", "kjv:Luke.17.36"],
               "largest_file_mb": 50}     # GitHub warns above 50 MB a file

# The pilot, John 1:1-18, measured 2026-09-26. Unchanged by the full run.
EXPECTED = {"verses": 18, "tokens": 253, "witnesses": 36, "alignments": 18,
            "distinct_lemmas": 83, "finite_verbs": 41, "flagged": 1,
            # Strong's dictionary glosses (strongs_gloss.py), measured 2026-09-26,
            # before any override: what the rule gives, kept under `was` where overridden
            # 231 until 2026-10-02; the paradigm rule glosses the 15 pronouns
            # Strong's left null (13 autos, 2 plural ego)
            "dict_glossed": 246,
            "dict_by_rule": {"kjv-form": 49, "paradigm": 15, "kjv-sole": 24, "kjv-in-def": 116,
                             "def-head": 42},
            # the house draft over it (gloss-overrides.jsonl, 2026-09-26)
            "overrides": 137, "glossed": 253,
            "gloss_by_rule": {"kjv-form": 41, "paradigm": 0, "kjv-sole": 19, "kjv-in-def": 56,
                              "def-head": 0},
            "plain": 18}
TOKEN_FIELDS = ("surface", "normalized", "search_key", "translit",
                "lemma", "parsing", "gloss", "plain_form")

# ================================================================ OFFLINE
print("--- files")
check("manifest.json exists", os.path.exists(os.path.join(DATA, "manifest.json")))
manifest = json.load(open(os.path.join(DATA, "manifest.json"), encoding="utf-8"))
missing = [fn for fn in manifest["files_sha256"] if not os.path.exists(os.path.join(DATA, fn))]
if missing:
    raise SystemExit(f"data/nt/ is not built here: {len(missing)} shard files are absent "
                     f"(they are rebuilt, not committed). Run: python3 pipeline/rebuild_bible.py")
sh = manifest["shards"]
check(f"the shards are the {EXPECTED_NT['books']} books in canonical order, one folder each",
      sh["layout"] == "book" and sh["order"] == [o for _, _, o in B.BOOKS] == manifest["selection"]["books"]
      and all(sh["books"][b]["dir"] == b for b in sh["order"]))
check("the manifest lists exactly the four files of every shard",
      sorted(manifest["files_sha256"]) == sorted(f"{b}/{k}.jsonl" for b in sh["order"] for k in B.FILES))
bad_sum = [fn for fn, want in manifest["files_sha256"].items()
           if not os.path.exists(os.path.join(DATA, fn))
           or hashlib.sha256(open(os.path.join(DATA, fn), "rb").read()).hexdigest() != want]
check("every file matches its manifest checksum", not bad_sum, bad_sum[:3])
check("no output file the manifest does not list (the pilot's flat files are gone)",
      not B.stale_outputs(DATA, set(manifest["files_sha256"]) | {"manifest.json"}),
      B.stale_outputs(DATA, set(manifest["files_sha256"]) | {"manifest.json"})[:3])
big = max(os.path.getsize(os.path.join(DATA, fn)) for fn in manifest["files_sha256"]) / 1e6
check(f"no file is over GitHub's {EXPECTED_NT['largest_file_mb']} MB warning (largest {big:.1f} MB)",
      big < EXPECTED_NT["largest_file_mb"])
check("manifest names the schema and the doc",
      manifest.get("schema") == B.SCHEMA and os.path.exists(os.path.join(REPO, manifest["doc"])))
check("row unit is the verse", manifest.get("row_unit") == "verse")
check("both pending rulings are written into the manifest as house defaults, with the way to change them",
      all(r["status"].startswith("house default") and r.get("doc")
          for r in (sh["ruling"], manifest["versification"]["ruling"]))
      and sh["ruling"]["alternatives"] and manifest["versification"]["ruling"]["alternative"])

nt = B.load_nt(REPO)
passages, witnesses, tokens, alignments = (nt[k] for k in B.FILES)
pilot = B.load_nt(REPO, pericope=B.PILOT["pericope"])
p_passages, p_witnesses, p_tokens, p_alignments = (pilot[k] for k in B.FILES)
p_uids = {p["uid"] for p in p_passages}

print("\n--- shape: the whole NT")
check("verse count", len(passages) == EXPECTED_NT["verses"], len(passages))
check("token count", len(tokens) == EXPECTED_NT["tokens"], len(tokens))
check("witness count", len(witnesses) == EXPECTED_NT["witnesses"], len(witnesses))
check("alignment count", len(alignments) == EXPECTED_NT["alignments"], len(alignments))
check("manifest counts agree with the files and the measured values",
      manifest["counts"]["tokens"] == len(tokens) and manifest["counts"]["passages"] == len(passages)
      and manifest["counts"]["distinct_lemmas"] == EXPECTED_NT["distinct_lemmas"]
      and manifest["counts"]["finite_verbs"] == EXPECTED_NT["finite_verbs"], manifest["counts"])
check("each shard's counts are its files', and they sum to the whole",
      all(sh["books"][b]["verses"] == sum(1 for p in passages if p["book"] == b) for b in sh["order"])
      and sum(v["tokens"] for v in sh["books"].values()) == len(tokens))
check("every passage is a verse", all(p["unit"] == "verse" and p["kind"] == "passage" for p in passages))
book_of = {p["uid"]: p["book"] for p in passages}
misplaced = []
for b in sh["order"]:
    for k in B.FILES:
        with open(os.path.join(DATA, b, k + ".jsonl"), encoding="utf-8") as f:
            misplaced += [f"{b}/{k}" for line in f
                          if book_of.get(B._record_uid(k, json.loads(line))) != b][:1]
check("every record sits in its own book's shard, and the loader returns the books in canon order",
      not misplaced and [p["book"] for p in passages]
      == sorted((p["book"] for p in passages), key=sh["order"].index), misplaced[:3])

print("\n--- shape: the pilot (John 1:1-18), as it was")
check("verse count", len(p_passages) == EXPECTED["verses"], len(p_passages))
check("token count", len(p_tokens) == EXPECTED["tokens"], len(p_tokens))
check("witness count", len(p_witnesses) == EXPECTED["witnesses"], len(p_witnesses))
check("alignment count", len(p_alignments) == EXPECTED["alignments"], len(p_alignments))
check("the pilot view's counts are the measured ones",
      pilot["manifest"]["counts"]["distinct_lemmas"] == EXPECTED["distinct_lemmas"]
      and pilot["manifest"]["counts"]["finite_verbs"] == EXPECTED["finite_verbs"]
      and pilot["manifest"]["selection"]["title"] == B.PILOT["title"], pilot["manifest"]["counts"])
sel = B.PILOT
check("the pilot verses are John 1:1-18, in order, with no gap, and only they carry the pericope label",
      [p["verse"] for p in p_passages] == list(range(sel["first"], sel["last"] + 1))
      and all(p["chapter"] == sel["chapter"] and p["book"] == "John" for p in p_passages)
      and {p["uid"] for p in passages if p["pericope"] is not None} == p_uids)

print("\n--- identity: the verse's existing uid, nothing minted")
committed = json.load(open(REGISTRY, encoding="utf-8"))["uids"]
by_uid = {p["uid"]: p for p in passages}
check("every uid is well-formed", all(U.is_uid(p["uid"]) for p in passages))
check("no two passages share a uid", len(by_uid) == len(passages))
moved = [p["citation"] for p in passages if committed.get(p["citation"]) != p["uid"]]
check("every uid is the committed registry's uid for its KJV-versified citation", not moved, moved[:3])
check("citations are kjv:<OSIS> and agree with osis/chapter/verse",
      all(re.fullmatch(r"kjv:[1-3]?[A-Z][A-Za-z]+\.\d+\.\d+", p["citation"])
          and p["citation"] == f"kjv:{p['osis']}"
          and p["osis"] == f"{p['book']}.{p['chapter']}.{p['verse']}" for p in passages))
check("versification is declared on every passage", all(p.get("versification") == "kjv" for p in passages))
lang_leak = [p["citation"] for p in passages if re.search(r"(^|[.:/])(grc|gr|greek)([.:/]|$)", p["citation"])]
check("no language code baked into any citation", not lang_leak, lang_leak[:3])
check("the reading of record is left where the KJV build put it",
      all(p["reading_of_record"] == KJV.READING_OF_RECORD == B.FACING for p in passages))
tmp = tempfile.mkdtemp()
try:
    copy = os.path.join(tmp, "r.json")
    shutil.copy2(REGISTRY, copy)
    reg = U.WhUidRegistry(copy, frozen=True)
    check("a FROZEN replay returns the stored uid for every verse",
          all(reg.uid_for(p["citation"]) == p["uid"] for p in passages))
    check("replay minted 0", reg.minted == 0, reg.stats())
    try:
        reg.uid_for("kjv:Rom.14.24")    # RP's placement of the doxology; no KJV verse
        refused = False
    except U.WhUidError:
        refused = True
    check("a Greek verse with no KJV uid is refused, not minted (Rom 14:24)", refused)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

import subprocess  # noqa: E402
_saved = open(os.path.join(PIPE, "build_nt_corpus.py"), encoding="utf-8").read()
_narrow = os.path.join(tempfile.mkdtemp(), "pipeline")
shutil.copytree(PIPE, _narrow, ignore=shutil.ignore_patterns("__pycache__"))
with open(os.path.join(_narrow, "build_nt_corpus.py"), "w", encoding="utf-8") as f:
    f.write(_saved.replace("SCOPE = [stem for stem, _, _ in BOOKS]", 'SCOPE = ["JOH"]', 1))
_r = subprocess.run([sys.executable, os.path.join(_narrow, "build_nt_corpus.py"), "--check",
                     "--out", os.path.join(os.path.dirname(_narrow), "out")],
                    capture_output=True, text=True)
check("a narrowed SCOPE refuses to write or --check (it would drop the other books)",
      _r.returncode != 0 and "SCOPE is narrowed" in (_r.stdout + _r.stderr), _r.stderr[-200:])
shutil.rmtree(os.path.dirname(_narrow), ignore_errors=True)

print("\n--- versification: the Romans doxology (house default), the TR-only verses")
vm = manifest["versification"]
dox = [w for w in witnesses if w.get("rp_ref")]
cit_of = {p["uid"]: p["citation"] for p in passages}
check("the map is the build's, and the doxology is the only verse placed elsewhere",
      vm["map"] == B.VERSIFICATION_MAP and len(dox) == 3 == len(vm["placed_elsewhere"]))
check("RP Rom 14:24-26 are witnesses of KJV Rom 16:25-27's existing uids, each recording RP's reference",
      [(w["rp_ref"], cit_of[w["passage_uid"]]) for w in dox]
      == [("Rom.14.24", "kjv:Rom.16.25"), ("Rom.14.25", "kjv:Rom.16.26"), ("Rom.14.26", "kjv:Rom.16.27")]
      and all(committed[cit_of[w["passage_uid"]]] == w["passage_uid"] for w in dox))
check("... in RP's reading order: straight after Rom 14:23",
      [p["citation"] for p in passages if p["book"] == "Rom"][
          [p["citation"] for p in passages if p["book"] == "Rom"].index("kjv:Rom.14.23") + 1] == "kjv:Rom.16.25")
check("no citation names RP's own placement (kjv:Rom.14.24 is not a KJV verse)",
      not any(p["citation"].startswith("kjv:Rom.14.2") and p["verse"] > 23 for p in passages))
check("the KJV verses with no Greek witness are the four Textus Receptus verses, listed, not guessed",
      vm["kjv_verses_without_grc"] == EXPECTED_NT["kjv_without_grc"] and not vm["left_out"]
      and not set(vm["kjv_verses_without_grc"]) & set(cit_of.values()))

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
check("one grc.byz witness per verse",
      sorted(w["passage_uid"] for w in witnesses if w["name"] == B.WITNESS) == sorted(by_uid))
greek = [w for w in witnesses if w["name"] == B.WITNESS]
plains = [w for w in witnesses if w["name"] == B.PLAIN]
check("every witness is the Greek or its plain line", len(greek) + len(plains) == len(witnesses),
      sorted({w["name"] for w in witnesses}))
check("language lives on the witness: lang grc, textform byzantine",
      all(w["lang"] == "grc" and w["textform"] == "byzantine" and w["role"] == "original" for w in greek))
check("the Greek is attested text, not generated, and is not the reading of record",
      all(w["text"] and not w["generated"] and w["attested"] == "Y" and w["reading_of_record"] is False
          for w in greek))
check("every witness names a source in the manifest",
      all(w["source"] in manifest["sources"] for w in witnesses))
check("paragraph_starts are token positions",
      all(isinstance(w["paragraph_starts"], list) for w in greek))
check(f"one en.plain witness per verse ({EXPECTED['plain']}), as the hymns carry it: lang en, "
      f"generated, text null, not attested, not the reading of record",
      len(plains) == EXPECTED["plain"] == manifest["counts"]["plain_witnesses"]
      and len({w["passage_uid"] for w in plains}) == len(plains)
      and all(w["lang"] == "en" and w["role"] == "plain" and w["generated"] is True and w["text"] is None
              and w["attested"] == "N" and w["reading_of_record"] is False
              and w["plain_override"] is None and isinstance(w["absorbed"], list) for w in plains))


def keys_named(obj, name):
    if isinstance(obj, dict):
        return any(k == name or keys_named(v, name) for k, v in obj.items())
    if isinstance(obj, list):
        return any(keys_named(v, name) for v in obj)
    return False


stored = [r.get("address") or r.get("uid") for r in passages + witnesses + tokens + alignments
          if keys_named(r, "plain") or keys_named(r, "wooden")]
check("`plain` and `wooden` are never stored, in any file", not stored, stored[:3])

print("\n--- the licence gate (D4)")
src = manifest["sources"]
lic = {k: v.get("license") for k, v in src.items()}
check("every source is PD or own", all(v in B.ALLOWED_LICENSES for v in lic.values()), lic)
check("every source records its evidence: where it was read, and what it says",
      all(v.get("license_basis") and all(e.get("where") and e.get("says") for e in v["license_basis"])
          and v.get("verified_on") and v.get("source_url") for v in src.values()))
check("RP's public-domain statement is recorded verbatim from the repo",
      any(e["says"] == "All the code and text contained in this folder is in the Public Domain."
          for e in src["rp2018-byztxt"]["license_basis"]))
banned = re.compile(r"morphgnt|sblgnt|perseus", re.I)
check("nothing from MorphGNT, SBLGNT or Perseus is a source, or named in any record",
      not any(banned.search(k) or banned.search(v["what"] + v["edition"]) for k, v in src.items())
      and not any(banned.search(json.dumps(r)) for r in passages + witnesses + tokens + alignments))
check("they are recorded as future layers, with their licences",
      set(manifest["future_layers"]) == {"morphgnt-sblgnt", "sblgnt", "perseus"}
      and all(v.get("license") and v.get("why_not_here") for v in manifest["future_layers"].values()))

print("\n--- tokens")
missing_f = [t["address"] for t in tokens if any(f not in t for f in TOKEN_FIELDS)]
check("every token carries all eight fields (null allowed)", not missing_f, missing_f[:3])
empty = [t["address"] for t in tokens for f in TOKEN_FIELDS if t.get(f) == ""]
check("no field is an empty string -- absence is null", not empty, empty[:3])
check("surface, normalized, search_key, translit, lemma and parsing are never null here",
      all(t[f] for t in tokens for f in ("surface", "normalized", "search_key", "translit",
                                         "lemma", "parsing")))
check("plain_form is set only by an override row",
      all(t["plain_form"] is None or t["provenance"]["gloss"]["kind"] == "contextual" for t in tokens))
check("normalized is NFC(surface)",
      all(t["normalized"] == unicodedata.normalize("NFC", t["surface"]) for t in tokens))
check("search_key is the fold of normalized", all(t["search_key"] == B.search_key(t["normalized"]) for t in tokens))
check("translit is the house scheme applied to normalized",
      all(t["translit"] == B.translit(t["normalized"]) for t in tokens))
check("no punctuation or pilcrow survives in a surface",
      all(t["surface"] == t["surface"].strip(B.PUNCT) and B.PARA not in t["surface"] for t in tokens))
check("lemma_key is Robinson's Strong's number, G<n>", all(re.fullmatch(r"G[1-9]\d*", t["lemma_key"]) for t in tokens))
badcode = [t["parsing"] for t in tokens if not B.PARSING_RE.match(t["parsing"])]
check("every parsing is a well-formed Robinson code", not badcode, badcode[:5])
alts = [a for t in tokens for a in t["provenance"]["parsing"].get("alternatives", [])]
check("every alternative parsing is a well-formed Robinson code", all(B.PARSING_RE.match(a) for a in alts))
check("every token records where its lemma, parsing and gloss came from",
      all(set(t["provenance"]) == {"lemma", "parsing", "gloss"}
          and t["provenance"]["lemma"]["source"] == "strongs-1890"
          and t["provenance"]["parsing"]["source"] == "rp2018-byztxt" for t in tokens))
flagged = [t for t in tokens if t["review"]]
check(f"exactly the tokens Robinson parses two ways are flagged ({EXPECTED_NT['flagged']} in the NT, "
      f"{EXPECTED['flagged']} in the pilot, at John 1:9)",
      len(flagged) == EXPECTED_NT["flagged"] == manifest["counts"]["tokens_flagged_for_review"]
      and sum(1 for t in flagged if t["passage_uid"] in p_uids) == EXPECTED["flagged"]
      and all(t["provenance"]["parsing"]["status"] == "alternatives" for t in flagged), len(flagged))
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
check("tokens hang only on the verses", set(toks_of) == set(by_uid))
bad_seq = [p["citation"] for p in passages
           if [t["position"] for t in toks_of[p["uid"]]] != list(range(1, len(toks_of[p["uid"]]) + 1))]
check("token positions run 1..n in every verse", not bad_seq, bad_seq[:3])
bad_text = [p["citation"] for p in passages
            if B.tokenize(wmap[U.address(p["uid"], B.WITNESS)]["text"]) != [t["surface"] for t in toks_of[p["uid"]]]]
check("every verse's Greek re-tokenizes to exactly its tokens", not bad_text, bad_text[:3])

print("\n--- glosses: Strong's dictionary glosses, by rule, never invented")
gm = manifest["gloss"]
with_g = [t for t in tokens if t["gloss"] is not None]
without = [t for t in tokens if t["gloss"] is None]
overridden = [t for t in tokens if t["provenance"]["gloss"]["kind"] == "contextual"]
dictionary = [t for t in with_g if t["provenance"]["gloss"]["kind"] == "dictionary"]


def dict_layer(t):
    """(value, provenance) of the Strong's rule for a token, whether it is the
    token's gloss or kept under `was` by an override."""
    p = t["provenance"]["gloss"]
    if p["kind"] == "contextual":
        was = dict(p["was"])
        return was.pop("value"), was
    return t["gloss"], p


print(f"      coverage {len(with_g)}/{len(tokens)} ({100 * len(with_g) / len(tokens):.1f}%): "
      f"dictionary by rule {gm['by_rule']}, override {gm['by_override']}, none {len(without)}")
check(f"NT gloss coverage is the measured {EXPECTED_NT['glossed']:,} of {EXPECTED_NT['tokens']:,}",
      len(with_g) == EXPECTED_NT["glossed"] and manifest["counts"]["tokens_with_gloss"] == len(with_g)
      and manifest["counts"]["tokens_without_gloss"] == len(without), (len(with_g), len(without)))
check("... split by rule as measured", gm["by_rule"] == EXPECTED_NT["gloss_by_rule"], gm["by_rule"])
pron_null = [t for t in without if t["parsing"].startswith("P-")]
check(f"every personal pronoun is glossed but the {EXPECTED_NT['pronoun_nulls']} in crasis",
      len(pron_null) == EXPECTED_NT["pronoun_nulls"] and all("-K" in t["parsing"] for t in pron_null),
      [(t["surface"], t["parsing"]) for t in pron_null][:5])
pgm = pilot["manifest"]["gloss"]
p_with = [t for t in p_tokens if t["gloss"] is not None]
check(f"pilot gloss coverage is the measured {EXPECTED['glossed']} of {EXPECTED['tokens']}",
      len(p_with) == EXPECTED["glossed"] == pilot["manifest"]["counts"]["tokens_with_gloss"], len(p_with))
check("... the pilot's dictionary glosses still showing split by rule as measured",
      pgm["by_rule"] == EXPECTED["gloss_by_rule"], pgm["by_rule"])
under = [dict_layer(t) for t in p_tokens]
check(f"the dictionary layer beneath the overrides is intact: {EXPECTED['dict_glossed']} glossed, "
      f"split {EXPECTED['dict_by_rule']}",
      sum(1 for v, _ in under if v) == EXPECTED["dict_glossed"]
      and {r: sum(1 for _, p in under if p["rule"] == r) for r in G.RULE_ORDER} == EXPECTED["dict_by_rule"])
check("every dictionary gloss says strongs-1890, dictionary, and a known rule id",
      all(t["provenance"]["gloss"]["source"] == G.SOURCE and t["provenance"]["gloss"]["rule"] in G.RULE_ORDER
          for t in dictionary))
check("every null gloss is counted with its reason, and names no source or rule",
      all(t["provenance"]["gloss"]["source"] is None and t["provenance"]["gloss"]["rule"] is None
          and t["provenance"]["gloss"]["why"] for t in without)
      and gm["none"] == len(without)
      and gm["none_by_reason"] == {w: sum(1 for t in without if t["provenance"]["gloss"]["why"] == w)
                                   for w in {t["provenance"]["gloss"]["why"] for t in without}})
check("the manifest's by_rule and by_override counts are the files'",
      all(n == sum(1 for t in dictionary if t["provenance"]["gloss"]["rule"] == r)
          for r, n in gm["by_rule"].items())
      and all(n == sum(1 for t in overridden if t["provenance"]["gloss"]["source"] == k)
              for k, n in gm["by_override"].items()))
check("the manifest says the dictionary glosses are NOT a contextual translation",
      gm["kind"] == "dictionary" and "NOT a contextual translation" in gm["not"]
      and [r["id"] for r in gm["rules"]] == list(G.RULE_ORDER)
      and "dictionary" in manifest["token_fields"]["gloss"].lower())
consistent = {}
for t in tokens:
    consistent.setdefault((t["lemma_key"], t["parsing"]), set()).add(dict_layer(t)[0])
check("deterministic: one Strong's number and parsing, one dictionary gloss, in every verse",
      all(len(v) == 1 for v in consistent.values()),
      [k for k, v in consistent.items() if len(v) > 1][:3])
check("no gloss or plain_form is an empty string or carries markup",
      all(s.strip() == s and s and not re.search(r"[<>()\[\]:]", s)
          for t in with_g for s in (t["gloss"], t["plain_form"]) if s is not None))
check("the override file exists and names both layers",
      os.path.exists(G.OVERRIDES) and gm["overrides"]["file"] == "data/nt/gloss-overrides.jsonl"
      and gm["overrides"]["layers"] == ["adam-reviewed", "house"])

print("\n--- the house drafts: gloss overrides (layer house, draft)")
ov_rows = [json.loads(line) for line in open(G.OVERRIDES, encoding="utf-8") if line.strip()]
tok_by = {t["address"]: t for t in tokens}
check(f"{EXPECTED['overrides']} override rows, all loaded and all applied",
      len(ov_rows) == EXPECTED["overrides"] == len(G.load_overrides()) == gm["overrides"]["applied"]
      == len(overridden), (len(ov_rows), gm["overrides"]["applied"]))
nowhere = [r["address"] for r in ov_rows if r["address"] not in tok_by]
check("every override row points at a real token", not nowhere, nowhere[:3])
wrong_s = [r["address"] for r in ov_rows if r["address"] in tok_by and tok_by[r["address"]]["surface"] != r["surface"]]
check("... whose surface it names", not wrong_s, wrong_s[:3])
landed = [r["address"] for r in ov_rows
          if tok_by[r["address"]]["gloss"] != r.get("gloss", tok_by[r["address"]]["gloss"])
          or tok_by[r["address"]]["plain_form"] != r.get("plain_form")]
check("... and the token carries the row's gloss and plain_form", not landed, landed[:3])
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def drafted(r):      # a house draft awaiting review
    return (r.get("layer", r.get("source")) in ("house", "house-draft") and r.get("draft") is True
            and DATE.fullmatch(r.get("drafted_on") or "") and "reviewed_on" not in r)


def reviewed(r):     # an answer Adam gave on the review sheet (pipeline/review.py apply)
    return (r.get("layer", r.get("source")) == "adam-reviewed" and "draft" not in r
            and "drafted_on" not in r and DATE.fullmatch(r.get("reviewed_on") or ""))


ov_draft = [r for r in ov_rows if r.get("draft")]
ov_by = G.load_overrides()
check("every row is a house draft (layer house, draft true, drafted_on) or Adam's reviewed answer "
      "(layer adam-reviewed, reviewed_on), with a one-line reason",
      all((drafted(r) or reviewed(r)) and r.get("note") and "\n" not in r["note"] for r in ov_rows))
check("... and every overridden token says so: its row's layer, contextual, draft or reviewed_on as the "
      "row is, the dictionary gloss kept",
      all(p["source"] == ov["layer"] and p["kind"] == "contextual"
          and (p.get("draft") is True and p["drafted_on"] == ov["drafted_on"] and "reviewed_on" not in p
               if ov.get("draft") else "draft" not in p and p["reviewed_on"] == ov["reviewed_on"])
          and p["was"]["source"] in (G.SOURCE, None) and "value" in p["was"]
          for t in overridden for p, ov in [(t["provenance"]["gloss"], ov_by[t["address"]])]))
check("the manifest counts the draft rows and points at the review doc",
      gm["overrides"]["draft"] == len(ov_draft) == manifest["drafts"]["gloss_override_rows"]
      and os.path.exists(os.path.join(REPO, manifest["drafts"]["review_doc"]))
      and manifest["drafts"]["status"] == ("awaiting Adam's review"
                                           if ov_draft or any(w.get("draft") for w in plains)
                                           else "none open: every row reviewed"))
check("word glosses, not paraphrase: no gloss or plain_form over four words",
      all(len(re.split(r"[ -]", s)) <= 4 for r in ov_rows for s in (r.get("gloss"), r.get("plain_form")) if s))
check("every null the dictionary left in the pilot is now glossed (22, of which the paradigm rule "
      "now takes 15; the house drafts keep the other 7)",
      all(t["gloss"] for t in p_tokens)
      and sum(1 for t in overridden if t["provenance"]["gloss"]["was"]["value"] is None) == 22 - 15)
check("... and every override row is in the pilot (the drafts cover John 1:1-18 only)",
      all(t["passage_uid"] in p_uids for t in overridden))

print("\n--- the house drafts: prose_order (en.plain, house-draft)")
po_rows = B.load_prose_orders()
check("one prose_order row per pilot verse, and each became that verse's en.plain",
      set(po_rows) == p_uids == {w["passage_uid"] for w in plains}
      and all(po_rows[w["passage_uid"]]["prose_order"] == w["prose_order"]
              and po_rows[w["passage_uid"]]["absorbed"] == w["absorbed"] for w in plains))
perm_bad = [by_uid[w["passage_uid"]]["citation"] for w in plains
            if B.permutation_problems(len(toks_of[w["passage_uid"]]), w["prose_order"], w["absorbed"])]
check("every prose_order is a permutation of its verse's token positions, the absorbed making up the rest",
      not perm_bad, perm_bad[:3])
check("... using the hymns' own rule (build_hymn_corpus.permutation_problems agrees)",
      all(B.permutation_problems(len(toks_of[w["passage_uid"]]), w["prose_order"], w["absorbed"])
          == load("build_hymn_corpus").permutation_problems(len(toks_of[w["passage_uid"]]),
                                                             w["prose_order"], w["absorbed"])
          for w in plains))
check("a supplied word is a non-empty string; every other step a position",
      all(isinstance(s, int) or (isinstance(s, str) and s.strip() == s and s) for w in plains
          for s in w["prose_order"]))
check("every en.plain is a house draft (draft true, drafted_on, source house-draft) or Adam's "
      "(source adam-reviewed, reviewed_on), as its row is",
      all((drafted(w) or reviewed(w)) and w["source"] == po_rows[w["passage_uid"]]["source"]
          and w.get("drafted_on") == po_rows[w["passage_uid"]].get("drafted_on")
          and w.get("reviewed_on") == po_rows[w["passage_uid"]].get("reviewed_on") for w in plains)
      and manifest["prose_order"]["draft"] == sum(1 for w in plains if w.get("draft"))
      == manifest["drafts"]["prose_orders"])
rendered = {w["passage_uid"]: B.render_plain(toks_of[w["passage_uid"]], w) for w in plains}
check("render_plain() produces a line for every verse, gloss or plain_form for every walked token",
      all(line and "None" not in line for line in rendered.values()))
check("... and keeps the Prologue's names capitalised (John, Moses, Father, God, Word)",
      all(n in " ".join(rendered.values()) for n in ("John", "Moses", "Father", "God", "Word")))
used = {r["layer"] for r in ov_rows} | {w["source"] for w in plains}
check("the licence gate: every layer and prose source in use (house, house-draft, adam-reviewed) is a "
      "source, licence own; a draft source says draft",
      all(src.get(k, {}).get("license") == "own" for k in used)
      and ("house-draft" not in used or src["house-draft"].get("status") == "draft")
      and ("house" not in used or not ov_draft or "draft" in src["house"].get("open", "")))
check("... and the manifest records both files' checksums as inputs",
      manifest["inputs_sha256"].get("gloss-overrides.jsonl") == B.sha256(G.OVERRIDES)
      and manifest["inputs_sha256"].get("prose-order.jsonl") == B.sha256(B.PROSE_ORDERS))

print("\n--- the gloss rule, on fixtures (invented entries, not Strong's text)")
E = G.Entry
ent = E(1, "from G2; something said; by implication, a word", ":--account, cause, word.")
check("the definition picks among the alphabetised KJV renderings (word, not account)",
      G.gloss_for("N-NSM", ent) == ("word", {"source": G.SOURCE, "by": "lemma_key",
                                              "rule": "kjv-in-def", "kind": "dictionary"}))
check("X and + renderings are skipped; one left is kjv-sole",
      G.gloss_for("N-NSM", E(2, "x", ":--X exceeding, + at all, lamp."))[0] == "lamp"
      and G.gloss_for("N-NSM", E(2, "x", ":--X exceeding, + at all, lamp."))[1]["rule"] == "kjv-sole")
check("a noun takes Strong's noun variant (dark(-ness) -> darkness)",
      G.gloss_for("N-NSF", E(3, "dimness", ":--dark(-ness)."))[0] == "darkness"
      and G.gloss_for("A-NSF", E(3, "dimness", ":--dark(-ness)."))[0] == "dark")
check("no rendering in the definition: a noun takes the definition head, derivation set aside",
      G.gloss_for("N-NSM", E(4, "from G5; (properly) a commencement, or chief", ":--beginning, rule."))
      == ("commencement", {"source": G.SOURCE, "by": "lemma_key", "rule": "def-head", "kind": "dictionary"}))
check("... a verb loses its leading 'to'",
      G.gloss_for("V-PAI-3S", E(5, "a primary verb; to procreate", ":--bear, beget."))[0] == "procreate")
check("... a function word takes nothing (null, with the reason)",
      G.gloss_for("CONJ", E(6, "properly, other things", ":--and, but."))[0] is None
      and "function word" in G.gloss_for("CONJ", E(6, "properly, other things", ":--and, but."))[1]["why"])
check("a two-letter rendering counts only at the head of a clause ('in front of' is not 'of')",
      G.gloss_for("PREP", E(7, "in front of", ":--before, of."))[0] is None
      and G.gloss_for("PREP", E(8, '"in," at', ":--at, in."))[0] == "in")
pr = E(9, "the reflexive pronoun self", ":--her, it(-self), them, they.")
check("pronouns agree in person, number, gender and case: Strong's form first",
      G.gloss_for("P-ASF", pr)[0] == "her" and G.gloss_for("P-ASN", pr)[0] == "it"
      and G.gloss_for("P-DPM", pr)[0] == "them" and G.gloss_for("P-NPM", pr)[0] == "they"
      and G.gloss_for("P-DPM", pr)[1]["rule"] == "kjv-form")
check("... then the paradigm, for a personal pronoun Strong's lists no form for (P-GSM -> his)",
      G.gloss_for("P-GSM", pr) == ("his", {"source": G.SOURCE, "by": "lemma_key", "rule": "paradigm",
                                           "kind": "dictionary"})
      and G.gloss_for("P-2GP", E(12, "the personal pronoun of the second person singular", ":--thou."))[0]
      == "your")
check("... but never in crasis, nor for an entry Strong's does not call a pronoun",
      G.gloss_for("P-1DS-K", E(13, "so also the dative case", ":--I."))[0] is None
      and G.gloss_for("P-1DS", E(14, "a primary word", ":--I."))[0] is None)
check("a demonstrative with no agreeing form goes on to the sense rules (an article never does)",
      G.gloss_for("D-ASM", E(15, "truly this", ":--whiles."))[0] == "whiles"
      and G.gloss_for("T-NSM", E(16, "the", ":--whiles."))[0] is None)
check("def-head: a multi-word '(or ...)' alternative ends the head; a dangling 'in a good' is dropped",
      G.gloss_for("V-PAI-3S", E(17, "to lower (or with violence) demolish", ":--+ cast down."))[0] == "lower"
      and G.gloss_for("V-PAI-3S", E(18, "to render (or esteem) glorious", ":--+ honour."))[0]
      == "render glorious"
      and G.gloss_for("N-NSN", E(19, "a boast (properly, the object) in a good or a bad sense", ":--+ glory."))[0]
      == "boast")
check("the two entries whose ':--' Petersen's XML lost are repaired (G3372 length, G259)",
      G.gloss_for("N-NSN", G.load_entries(open(B._path("strongs", B.STRONGS_XML), encoding="utf-8").read())[3372])
      [0] == "length" if os.path.exists(B._path("strongs", B.STRONGS_XML)) else True)
check("first-person forms read the person digit (P-1GS -> me, P-1DP -> none)",
      G.gloss_for("P-1GS", E(10, "", ":--I, me."))[0] == "me"
      and G.gloss_for("P-1NS", E(10, "", ":--I, me."))[0] == "I"
      and G.gloss_for("P-1DP", E(10, "", ":--I, me."))[0] is None)
check("the article is 'the' in every case", all(
    G.gloss_for(c, E(11, "the", ":--the, this, that, one, he, she, it, etc."))[0] == "the"
    for c in ("T-NSM", "T-GPM", "T-DSF", "T-ASN")))
check("no entry: null, never a guess", G.gloss_for("N-NSM", None)[0] is None)
check("the same inputs give the same answer (a pure function)",
      G.gloss_for("N-NSM", ent) == G.gloss_for("N-NSM", ent))
ov_tmp = tempfile.mkdtemp()
try:
    def bad(rows):
        p = os.path.join(ov_tmp, "o.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            f.write("".join(json.dumps(r) + "\n" for r in rows))
        try:
            G.load_overrides(p)
            return False
        except ValueError:
            return True
    row = {"address": "wh-AGJ6YAF47Q/grc.byz.t05", "surface": "λόγος", "gloss": "Word",
           "layer": "adam-reviewed", "reviewed_on": "2026-09-27"}
    check("an override row loads", not bad([row]))
    check("a malformed override row is a hard stop (unknown layer, no date, twice, empty gloss)",
          bad([dict(row, layer="guess")]) and bad([{k: v for k, v in row.items() if k != "reviewed_on"}])
          and bad([row, row]) and bad([dict(row, gloss=" ")]) and bad([dict(row, lemma="x")]))
    g, pf, prov = G.apply_override("something said", None,
                                   {"source": G.SOURCE, "by": "lemma_key", "rule": "def-head",
                                    "kind": "dictionary"}, "λόγος", row)
    check("an override replaces the gloss and keeps the dictionary one under `was`",
          g == "Word" and pf is None and prov["source"] == "adam-reviewed" and prov["kind"] == "contextual"
          and prov["was"]["value"] == "something said" and prov["was"]["rule"] == "def-head")
    draft = {k: v for k, v in row.items() if k != "reviewed_on"}
    draft.update(layer="house", draft=True, drafted_on="2026-09-26", note="a reason")
    check("a draft row loads: layer house, draft true, drafted_on", not bad([draft]))
    check("a draft row is refused in Adam's layer, with reviewed_on, without drafted_on, or draft: false",
          bad([dict(draft, layer="adam-reviewed")]) and bad([dict(draft, reviewed_on="2026-09-27")])
          and bad([{k: v for k, v in draft.items() if k != "drafted_on"}]) and bad([dict(draft, draft=False)])
          and bad([dict(row, drafted_on="2026-09-26")]))
    _, _, dprov = G.apply_override("something said", None, {"source": G.SOURCE, "rule": "def-head"},
                                   "λόγος", draft)
    check("... and its provenance says draft, with the date it was drafted, not reviewed",
          dprov["draft"] is True and dprov["drafted_on"] == "2026-09-26" and "reviewed_on" not in dprov
          and dprov["source"] == "house" and dprov["note"] == "a reason")

    def po_bad(rows):
        p = os.path.join(ov_tmp, "p.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            f.write("".join(json.dumps(r) + "\n" for r in rows))
        try:
            B.load_prose_orders(p)
            return False
        except ValueError:
            return True
    po = {"passage_uid": "wh-AGJ6YAF47Q", "citation": "kjv:John.1.1", "prose_order": [2, "the", 1],
          "absorbed": [3], "plain_override": None, "source": "house-draft", "draft": True,
          "drafted_on": "2026-09-26"}
    check("a prose_order row loads", not po_bad([po]))
    check("a malformed prose_order row is a hard stop (not a draft, unknown source, a bool or empty "
          "step, twice, an override line, reviewed_on on a draft)",
          po_bad([{k: v for k, v in po.items() if k != "draft"}]) and po_bad([dict(po, source="kjv")])
          and po_bad([dict(po, prose_order=[1, True])]) and po_bad([dict(po, prose_order=[1, ""])])
          and po_bad([po, po]) and po_bad([dict(po, plain_override="x")])
          and po_bad([dict(po, reviewed_on="2026-09-27")]) and po_bad([dict(po, prose_order=[])]))
    done = {k: v for k, v in po.items() if k not in ("draft", "drafted_on")}
    done.update(source="adam-reviewed", reviewed_on="2026-09-27")
    check("Adam's reviewed prose_order loads (source adam-reviewed, reviewed_on), and is never a draft",
          not po_bad([done]) and po_bad([dict(done, draft=True, drafted_on="2026-09-26")])
          and po_bad([{k: v for k, v in done.items() if k != "reviewed_on"}]))
    check("the permutation rule: a missing, repeated or out-of-range position is reported",
          B.permutation_problems(3, [2, "the", 1], [3]) is None
          and B.permutation_problems(3, [1, 2], [])["missing"] == [3]
          and B.permutation_problems(3, [1, 2, 2, 3], [])["duplicated"] == [2]
          and B.permutation_problems(3, [1, 2, 3, 4], [])["out_of_range"] == [4])
    try:
        G.apply_override("x", None, {}, "ὁ", row)
        wrong = False
    except ValueError:
        wrong = True
    check("... and refuses a row whose surface is not the token's", wrong)
finally:
    shutil.rmtree(ov_tmp, ignore_errors=True)

print("\n--- alignments")
bad_al = []
for al in alignments:
    a, b = al["a"][0]["address"], al["b"][0]["address"]
    pa, pb = U.parse_address(a), U.parse_address(b)
    if a not in wmap or pb["uid"] != pa["uid"] or pb["witness"] not in KJV.WITNESSES:
        bad_al.append(al["alignment_id"])
    if al["type"] != "1:1" or al["confidence"] not in ("high", "medium", "low") \
            or al["alignment_id"] != f"{a}~{pb['witness']}":
        bad_al.append(al["alignment_id"])
check("every alignment faces grc.byz with a KJV witness of the same uid", not bad_al, bad_al[:3])

print("\n--- the transliteration scheme (SBL Handbook 5.3, with the house choices)")
FIXTURES = [
    ("κύριος", "kyrios"),          # SBL note 4: independent upsilon is y
    ("ὕμνος", "hymnos"),           # note 5: rough breathing on an initial vowel
    ("αἵρεσις", "hairesis"),       # note 5: ... or diphthong
    ("Πύρρος", "Pyrrhos"),         # note 3: the second rho of a medial double rho
    ("ῥῆμα", "rhēma"),             # note 3: initial rho
    ("ἄγγελος", "angelos"),        # note 1: gamma nasal before g
    ("ἀνάγκη", "anankē"),          # ... before k
    ("ἔλεγχος", "elenchos"),       # ... before ch
    ("εὐαγγέλιον", "euangelion"),  # note 4: eu
    ("υἱός", "huios"),             # note 4: ui, with the rough breathing
    ("Ἰησοῦς", "Iēsous"),          # note 2: eta with a macron; capitals kept
    ("ᾠδή", "ōidē"),               # house: iota subscript as a following i
    ("Μωϋσῆς", "Mōÿsēs"),          # house: diaeresis kept, and it breaks the diphthong
    ("δι’", "di’"),                # the elision mark stays
]
bad_fx = [(g, B.translit(g), want) for g, want in FIXTURES if B.translit(g) != want]
check(f"{len(FIXTURES)} fixtures transliterate as the scheme says", not bad_fx, bad_fx)

print("\n--- the parsing grammar")
DESCRIBE = [("V-2ADI-3S", "3 sg 2nd aor mid dep ind"), ("V-PNP-ASM", "acc sg masc pres mid/pass dep ptc"),
            ("V-RAI-3S-ATT", "3 sg perf act ind Attic"), ("V-2ADN", "2nd aor mid dep inf"),
            ("P-1DP", "pers pron 1 dat pl"), ("A-NSM-N", "adj nom sg masc neg"),
            ("CONJ-N", "conjunction neg"), ("N-PRI", "indecl proper noun"),
            ("S-2PDSM", "poss adj 2 poss pl dat sg masc")]
bad_d = [(c, B.describe_parsing(c), w) for c, w in DESCRIBE if B.describe_parsing(c) != w]
check("Robinson codes decode to words", not bad_d, bad_d)
check("a malformed code is refused", not B.PARSING_RE.match("V-XYZ") and not B.PARSING_RE.match("N-NS"))
check("finite = indicative, subjunctive, optative, imperative",
      B.is_finite("V-IAI-3S") and B.is_finite("V-AAS-3P") and not B.is_finite("V-PAP-NSM")
      and not B.is_finite("V-2ADN") and not B.is_finite("N-NSM"))

# ============================================================ AGAINST THE PINS
print("\n--- against the pinned inputs")
pinned = all(os.path.exists(B._path(r, rel)) and B.sha256(B._path(r, rel)) == want
             for (r, rel), want in B.PINS.items())
if not pinned:
    print("skip  the pinned inputs are not in data/corpus/ -- the rebuild and cross-checks")
    print("      did not run. `python3 pipeline/build_nt_corpus.py --fetch` gets them.")
else:
    tmp = tempfile.mkdtemp()
    try:
        copy = os.path.join(tmp, "r.json")
        shutil.copy2(REGISTRY, copy)
        reg = U.WhUidRegistry(copy, frozen=True)
        data, man = B.build(reg)
        blobs = B.render_all(data, man)
        check("rebuild minted 0", reg.minted == 0, reg.stats())
        diff = [fn for fn, blob in blobs.items() if open(os.path.join(DATA, fn), "rb").read() != blob]
        check("rebuild is byte-identical to the committed files", not diff, diff)

        # The two rulings are one edit each. Prove it: rule the doxology the other
        # way, and write the pilot flat, on Romans and John alone.
        saved_scope, saved_map, saved_shard = B.SCOPE, B.VERSIFICATION_MAP, B.SHARD
        try:
            B.SCOPE = ["ROM"]
            B.VERSIFICATION_MAP = {k: None for k in saved_map}
            reg2 = U.WhUidRegistry(copy, frozen=True)
            d3, m3 = B.build(reg2)
            v3 = m3["versification"]
            check("ruling the doxology out instead: the three RP verses are left out and counted, "
                  "KJV Rom 16:25-27 have no Greek witness, and nothing is minted",
                  v3["left_out"] == ["Rom.14.24", "Rom.14.25", "Rom.14.26"] and not v3["placed_elsewhere"]
                  and v3["kjv_verses_without_grc"] == ["kjv:Rom.16.25", "kjv:Rom.16.26", "kjv:Rom.16.27"]
                  and len(d3["passages"]) == sh["books"]["Rom"]["verses"] - 3 and reg2.minted == 0, v3)
            B.SCOPE, B.VERSIFICATION_MAP, B.SHARD = ["JOH"], saved_map, None
            d4, m4 = B.build(U.WhUidRegistry(copy, frozen=True))
            b4 = B.render_all(d4, m4)
            check("sharding off instead: the four flat files, John's records byte for byte",
                  sorted(b4) == sorted([f"{k}.jsonl" for k in B.FILES] + ["manifest.json"])
                  and all(b4[f"{k}.jsonl"] == open(os.path.join(DATA, "John", f"{k}.jsonl"), "rb").read()
                          for k in B.FILES))
            flat_root = os.path.join(tmp, "flat")
            os.makedirs(os.path.join(flat_root, "data", "nt"))
            for fn, blob in b4.items():
                with open(os.path.join(flat_root, "data", "nt", fn), "wb") as f:
                    f.write(blob)
            fl = B.load_nt(flat_root)
            check("... and load_nt() reads a flat layout once, not once per book",
                  len(fl["passages"]) == sh["books"]["John"]["verses"]
                  and len(fl["tokens"]) == sh["books"]["John"]["tokens"])
        finally:
            B.SCOPE, B.VERSIFICATION_MAP, B.SHARD = saved_scope, saved_map, saved_shard
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    heads = B.load_strongs()
    check("every lemma is Strong's headword for its number",
          all(t["lemma"] == heads[int(t["lemma_key"][1:])] for t in tokens))

    x = open(B._path("strongs", B.STRONGS_XML), encoding="utf-8").read()
    entries = G.load_entries(x)
    check("Strong's XML reads as 5,624 entries", len(entries) == 5624, len(entries))
    memo = {}

    def gloss_of(t):
        k = (t["parsing"], t["lemma_key"])
        if k not in memo:
            memo[k] = G.gloss_for(t["parsing"], entries.get(int(t["lemma_key"][1:])))
        return memo[k]
    regloss = [t["address"] for t in tokens if gloss_of(t) != dict_layer(t)]
    check("every token's dictionary gloss and provenance re-derive from Strong's by the rule "
          "(under `was` where an override replaced it)", not regloss, regloss[:3])
    invented = []
    for t in tokens:
        en = entries[int(t["lemma_key"][1:])]
        g, p = dict_layer(t)
        if g is None:
            continue
        rule = p["rule"]
        if rule == "paradigm":     # the house paradigm's form, and it agrees
            ok = (g == G.paradigm_form(t["parsing"], en)
                  and G.form_fits(g, G.features(t["parsing"])))
        elif rule == "def-head":     # Strong's words, his parentheses taken out (README s.12)
            ok = set(g.lower().split()) <= set(re.findall(r"[\w'-]+", en.definition.lower().replace('"', "")))
        else:
            ok = any(g == b or g in v for b, v in G.usable(en))
        if not ok:
            invented.append((t["address"], rule))
    check("never invented: a KJV-rule gloss is one of the entry's usable KJV renderings, "
          "a def-head gloss is words of Strong's definition", not invented, invented[:3])

    # A real override row, through the real build, into a temp registry copy,
    # with no prose orders (they walk tokens only the full override file glosses).
    # John alone (B.SCOPE): these builds test the override and order rules, not the NT.
    tmp = tempfile.mkdtemp()
    saved, saved_po, saved_scope = G.OVERRIDES, B.PROSE_ORDERS, B.SCOPE
    john = [t for t in tokens if book_of[t["passage_uid"]] == "John"]
    try:
        B.SCOPE = ["JOH"]
        copy = os.path.join(tmp, "r.json")
        shutil.copy2(REGISTRY, copy)
        t5 = next(t for t in john if t["lemma_key"] == "G3056")
        B.PROSE_ORDERS = os.path.join(tmp, "absent.jsonl")
        G.OVERRIDES = os.path.join(tmp, "o.jsonl")
        with open(G.OVERRIDES, "w", encoding="utf-8") as f:
            f.write(json.dumps({"address": t5["address"], "surface": t5["surface"], "gloss": "Word",
                                "layer": "house", "reviewed_on": "2026-09-26",
                                "note": "test row"}, ensure_ascii=False) + "\n")
        d2, m2 = B.build(U.WhUidRegistry(copy, frozen=True))
        t5b = next(t for t in d2["tokens"] if t["address"] == t5["address"])
        others = [t for t in d2["tokens"] if t["address"] != t5["address"]]

        def bare(t):    # the committed token with its override taken off
            g, p = dict_layer(t)
            return dict(t, gloss=g, plain_form=None, provenance=dict(t["provenance"], gloss=p))
        check("an override row reaches its token through the build, the dictionary gloss kept",
              t5b["gloss"] == "Word" and t5b["provenance"]["gloss"]["source"] == "house"
              and t5b["provenance"]["gloss"]["was"]["value"] == dict_layer(t5)[0]
              and others == [bare(t) for t in john if t["address"] != t5["address"]])
        check("... and the manifest declares the layer (licence own) and the file's checksum",
              m2["sources"].get("house", {}).get("license") == "own"
              and "gloss-overrides.jsonl" in m2["inputs_sha256"]
              and m2["gloss"]["overrides"]["applied"] == 1 and m2["gloss"]["by_override"]["house"] == 1)
        check("... and with no prose_order file there is no en.plain and no house-draft source",
              not any(w["name"] == B.PLAIN for w in d2["witnesses"]) and "house-draft" not in m2["sources"]
              and m2["drafts"]["prose_orders"] == 0)
        G.OVERRIDES = saved
        rows = [json.loads(line) for line in open(saved_po, encoding="utf-8")]

        def stops_with(rs):
            with open(B.PROSE_ORDERS, "w", encoding="utf-8") as f:
                f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rs))
            try:
                B.build(U.WhUidRegistry(copy, frozen=True))
                return False
            except SystemExit:
                return True
        B.PROSE_ORDERS = os.path.join(tmp, "p.jsonl")
        check("the committed drafts build cleanly from a copy", not stops_with(rows))
        short = dict(rows[0], prose_order=[s for s in rows[0]["prose_order"] if s != 1])
        check("a prose_order that drops a token stops the build", stops_with([short] + rows[1:]))
        check("... and so does one naming the wrong citation for its uid",
              stops_with([dict(rows[0], citation="kjv:John.1.2")] + rows[1:]))
        G.OVERRIDES = os.path.join(tmp, "absent-o.jsonl")
        check("... and one walking a token with no gloss (the drafts without their glosses)",
              stops_with(rows))
        G.OVERRIDES = os.path.join(tmp, "o.jsonl")
        B.PROSE_ORDERS = os.path.join(tmp, "absent.jsonl")
        with open(G.OVERRIDES, "w", encoding="utf-8") as f:
            f.write(json.dumps({"address": t5["address"][:-2] + "99", "surface": "x", "gloss": "y",
                                "layer": "house", "reviewed_on": "2026-09-26"}) + "\n")
        try:
            B.build(U.WhUidRegistry(copy, frozen=True))
            stopped = False
        except SystemExit:
            stopped = True
        check("... and a row for a token that does not exist stops the build", stopped)
    finally:
        G.OVERRIDES, B.PROSE_ORDERS, B.SCOPE = saved, saved_po, saved_scope
        shutil.rmtree(tmp, ignore_errors=True)
    pairs = re.findall(r'<entry strongs="\d+">\s*<strongs>\d+</strongs>\s*<greek BETA="[^"]*" '
                       r'unicode="([^"]*)" translit="([^"]*)"', x)

    def no_accents(s):
        return unicodedata.normalize("NFC", "".join(
            c for c in unicodedata.normalize("NFD", s) if c not in "̀́̂͂"))

    one = [(g, t) for g, t in pairs if " " not in g]
    disagree = [g for g, t in one if B.translit(g) != no_accents(t)]
    # The one: χξϛ, the number 666, which Strong's spells out as "chx stigma".
    check(f"translit agrees with Strong's own on {len(one) - 1:,} of {len(one):,} one-word "
          f"headwords (accents set aside)", len(one) == 5506 and len(disagree) == 1, disagree[:3])

    ccat = B.read_csv(B._path("byz", "csv-unicode/ccat/no-variants/JOH.csv"))
    bp5 = B.read_csv(B._path("byz", "csv-unicode/strongs/with-parsing/JOH.csv"))
    b_ccat = B.read_beta(B._path("byz", "source/CCAT/04_JOH.TXT"), ":")
    b_bp5 = B.read_beta(B._path("byz", "source/Strongs/04_JOH.BP5"), ".")
    k = (1, 16)

    def stops(**kw):
        args = dict(accented=ccat[k], parsed=bp5[k], beta_ccat=b_ccat[k], beta_bp5=b_bp5[k])
        args.update(kw)
        try:
            B.pair_verse("John.1.16", **args)
            return False
        except ValueError:
            return True

    check("the pairing passes on the real verse", not stops())
    check("... and stops on one changed letter in Robinson's CCAT Beta",
          stops(beta_ccat=b_ccat[k].replace("PLHRW", "PLHRO", 1)))
    check("... and on one changed code in Robinson's BP5 Beta",
          stops(beta_bp5=b_bp5[k].replace("{N-GSN}", "{N-GSM}", 1)))
    check("... and on a dropped word in the parsed csv",
          stops(parsed=bp5[k].split(" ", 3)[3]))
    check("the apparatus is stripped, not read as text (1:16-18 carry NA notes)",
          sum(man["apparatus_in_selection"]["by_siglum"].values()) >= 3)

print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
