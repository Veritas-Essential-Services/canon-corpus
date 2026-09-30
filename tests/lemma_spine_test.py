#!/usr/bin/env python3
# prov: 2026-09-26 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-26 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
# fable_review: pending
"""
lemma_spine_test.py -- the Latin lemma spine (launch plan D3): Whitaker's
WORDS as the lemma source for data/hymns/tokens.jsonl.

Run:  python3 tests/lemma_spine_test.py

WHAT IT ASSERTS
    OFFLINE (always runs)
    1. The committed lemma files match their manifest checksums, and the
       manifest records the source at a pinned commit, the sha256 of every
       Whitaker file, and the licence grant VERBATIM with its evidence.
    2. Coverage: the counts in both manifests are what the token file says,
       and, taken as resolved (before Adam's answers), what was measured on
       2026-09-26 (so a regression is loud).
    3. Provenance, per token: every lemma and parsing names its source and
       carries the draft it replaced; a value from Whitaker is one of
       Whitaker's analyses of that very form; a value from the draft IS the
       draft; every non-agreement is flagged for review and nothing else is.
    4. Nothing is overwritten silently: putting each token's recorded draft
       back reproduces the pre-D3 token file's lemma/parsing exactly.
    5. The resolver's rules, on small synthetic cases, including readings
       reached by a WORDS rule (`via`) and two-words guesses.
    6. Adam's overrides: the committed file exists, every row in it is on
       its token, and loading and applying rows behaves as documented.
    AGAINST THE WHITAKER FILES (when fetched; says so when not)
    7. The pins hold, and a rebuild of the committed lemma files is
       byte-identical.
"""
import hashlib
import importlib.util
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PIPE = os.path.join(REPO, "pipeline")
LEM = os.path.join(REPO, "data", "lemmas", "whitaker-la")
HYM = os.path.join(REPO, "data", "hymns")
sys.path.insert(0, PIPE)


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(PIPE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


W = load("whitaker")
L = load("lemma_spine")
S = load("build_lemma_spine")

PASS = 0
FAIL = []


def check(label, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label + (("  " + str(detail)) if detail else ""))


def jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f]


# Measured 2026-09-26 (Whitaker at 1f2f0fb0867a, the 263 hymn tokens), after
# SYNCOPE/SLURY/FIXES/TRICKS were ported: pellicane is no longer unknown (WORDS
# reads it, wrongly, as pellex + suffix -an: disagree), and syncope adds a
# second candidate to moras and caro (agree -> agree-selected for moras).
# The forms grew with the three hymns printed from Britt 1922 (2026-09-26):
# 547 forms, 2 unknown (Sion, Isaac: proper names, which the spine does not
# load; README s.10). The token measures below stay the 263 DRAFTED tokens.
EXPECTED = {
    "hymn_forms": 547, "hymn_forms_unknown": 2,
    "lemma_from_whitaker": 244, "lemma_from_draft": 19,
    "parsing_from_whitaker": 84, "parsing_confirmed_by_whitaker": 10,
    "flagged_for_review": 24,
    "lemma_status": {"agree": 161, "agree-selected": 83, "ambiguous": 9, "disagree": 10},
    "parsing_status": {"confirmed": 10, "disagree": 5, "draft-consistent": 145,
                       "unchecked": 19, "whitaker": 84},
}
# The 505 tokens of Lauda Sion, Sacris solemniis and Verbum supernum, which
# have no house draft: lemma_spine.resolve_undrafted (README s.3b).
EXPECTED_UNDRAFTED = {
    "tokens": 505, "flagged_for_review": 198,
    "lemma_status": {"ambiguous": 193, "disagree": 3, "same-lemma": 34, "sole": 273, "unknown": 2},
    "parsing_status": {"ambiguous": 133, "unchecked": 232, "whitaker": 140},
}
GRANT = "Permission is hereby freely given for any and all use of program and data."

# ================================================================ OFFLINE
print("--- the committed lemma files")
man = json.load(open(os.path.join(LEM, "manifest.json"), encoding="utf-8"))
for fn in S.COMMITTED[:-1]:
    p = os.path.join(LEM, fn)
    check(f"{fn} exists and matches its manifest checksum",
          os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == man["files_sha256"][fn])
check("the full table is gitignored, not committed",
      "data/lemmas/whitaker-la/lemmas.jsonl" in open(os.path.join(REPO, ".gitignore"), encoding="utf-8").read()
      and man["gitignored"] == ["lemmas.jsonl"])
src = man["source"]
check("source pinned to a full commit", len(src["commit"]) == 40 and src["commit"] == W.COMMIT)
check("every Whitaker data file has a pinned sha256",
      set(src["files_sha256"]) == set(W.DATA_FILES) and all(len(v) == 64 for v in src["files_sha256"].values()))

print("\n--- the licence, recorded exactly")
check("licence class is free-grant, and says it is not public domain",
      src["license"] == "free-grant" and "Not public domain" in src["license_basis"])
check("the grant is quoted verbatim", any(GRANT in g for g in src["grant_verbatim"]))
check("the evidence names the author's own documentation and the port's LICENCE.txt",
      any("users.erols.com/whitaker/wordsdoc.htm" in e["url"] for e in src["evidence"])
      and any(e["url"].endswith("LICENCE.txt") for e in src["evidence"]))
check("the licence is verified, dated, and its open question stated",
      src["verified"] is True and src["verified_on"] == "2026-09-26" and "Adam" in src["open"])
hman = json.load(open(os.path.join(HYM, "manifest.json"), encoding="utf-8"))
ws = hman["sources"].get("whitaker-words", {})
check("the hymn manifest carries the same licence record",
      all(ws.get(k) == src[k] for k in ("license", "grant_verbatim", "evidence", "verified")))
check("free-grant is admitted for Whitaker only",
      [k for k, v in hman["sources"].items() if v["license"] == "free-grant"] == ["whitaker-words"])

print("\n--- coverage")
all_tokens = jsonl(os.path.join(HYM, "tokens.jsonl"))
# a drafted token came from a vault batch file and says where it sat there
tokens = [t for t in all_tokens if t["legacy_address"]]
undrafted = [t for t in all_tokens if not t["legacy_address"]]
arows = {r["form"]: r["analyses"] for r in jsonl(os.path.join(LEM, "hymns.analyses.jsonl"))}
forms = {t["search_key"] for t in all_tokens}
check("every hymn form has an analysis row, and no row is spare", set(arows) == forms,
      len(forms ^ set(arows)))
c = man["counts"]
check("hymn form counts as measured", (c["hymn_forms"], c["hymn_forms_unknown"]) ==
      (EXPECTED["hymn_forms"], EXPECTED["hymn_forms_unknown"]), (c["hymn_forms"], c["hymn_forms_unknown"]))
check("unknown_forms lists exactly the forms with no analysis",
      sorted(man["unknown_forms"]) == sorted(f for f, a in arows.items() if not a))
recount = {
    "lemma_from_whitaker": sum(t["provenance"]["lemma"]["source"] == "whitaker-words" for t in all_tokens),
    "parsing_from_whitaker": sum(t["provenance"]["parsing"]["source"] == "whitaker-words" for t in all_tokens),
    "flagged_for_review": sum(bool(t["review"]) for t in all_tokens),
}
spine = hman["lemma_spine"]
check("the hymn manifest's spine stats are what the tokens say",
      all(spine[k] == v for k, v in recount.items()), recount)


def as_resolved(t):
    """The token as the resolver left it, before any of Adam's answers (an
    answer keeps what it replaced under `was`)."""
    prov, t = dict(t["provenance"]), dict(t)
    for f in ("lemma", "parsing"):
        if prov[f]["source"] == L.OVERRIDE_SOURCE:
            prov[f] = prov[f]["was"]
    t["provenance"] = prov
    t["review"] = ((prov["lemma"]["status"] in ("disagree", "ambiguous", "unknown")
                    or prov["parsing"]["status"] == "disagree") or None)
    return t


# The measures are of Whitaker against the draft, so they are taken as
# resolved: Adam answering a flag (review.py apply) does not move them.
measured = load("build_hymn_corpus").spine_stats([as_resolved(t) for t in tokens])
for k in ("lemma_from_whitaker", "lemma_from_draft", "parsing_from_whitaker",
          "parsing_confirmed_by_whitaker", "flagged_for_review", "lemma_status", "parsing_status"):
    check(f"coverage: {k} as measured (as resolved, before Adam's answers)",
          measured[k] == EXPECTED[k], measured[k])
check("lemma coverage from Whitaker is over 90%", measured["lemma_from_whitaker"] / len(tokens) > 0.9,
      f"{measured['lemma_from_whitaker']}/{len(tokens)}")

print("\n--- provenance, per token")
OV = L.load_overrides()
bad_src, bad_w, bad_d, bad_flag, bad_key, bad_ov = [], [], [], [], [], []
for t in tokens:
    lp, pp = t["provenance"]["lemma"], t["provenance"]["parsing"]
    if L.OVERRIDE_SOURCE in (lp["source"], pp["source"]):
        # Adam's answer: it must be the row's; the checks below then run on
        # what it replaced, which the token keeps under `was`
        o = OV.get(t["address"])
        if not o or (lp["source"] == L.OVERRIDE_SOURCE and t["lemma_key"] != o.get("lemma_key")) \
                or (pp["source"] == L.OVERRIDE_SOURCE and t["parsing"] != o["parsing"]):
            bad_ov.append(t["address"])
        if lp["source"] == L.OVERRIDE_SOURCE:
            lp = dict(lp["was"], draft=lp["draft"])
            t = dict(t, lemma=lp.pop("value"), lemma_key=lp.pop("lemma_key"))
        if pp["source"] == L.OVERRIDE_SOURCE:
            pp = dict(pp["was"], draft=pp["draft"])
            t = dict(t, parsing=pp.pop("value"))
    if lp["source"] not in hman["sources"] or pp["source"] not in hman["sources"]:
        bad_src.append(t["address"])
    A = arows[t["search_key"]]
    if lp["source"] == "whitaker-words":
        mine = [a for a in A if a["key"] == t["lemma_key"]]
        if not mine or t["lemma"] != (mine[0]["lemma"] or lp["draft"]) \
                or mine[0]["headword"] != L.draft_headword(lp["draft"]):
            bad_w.append(t["address"])
    elif t["lemma"] != lp["draft"] or t["lemma_key"] is not None:
        bad_d.append(t["address"])
    if pp["source"] == "whitaker-words":
        mine = [a for a in A if a["key"] == t["lemma_key"]]
        if pp["status"] != "whitaker" or len({(a["whitaker"], a["enclitic"]) for a in mine}) != 1 \
                or pp["whitaker"] != mine[0]["whitaker"]:
            bad_w.append(t["address"])
    elif t["parsing"] != pp["draft"]:
        bad_d.append(t["address"])
    disagreeing = lp["status"] in ("disagree", "ambiguous", "unknown") or pp["status"] == "disagree"
    if t["address"] in OV:
        pass            # Adam's answer clears the reasons it answers
    elif disagreeing != bool(t["review"]):
        bad_flag.append(t["address"])
    if "draft" not in lp or "draft" not in pp:
        bad_key.append(t["address"])
check("every lemma and parsing names a source in the manifest", not bad_src, bad_src[:3])
check("an adam-reviewed value is exactly the override row's", not bad_ov, bad_ov[:3])
check("every token records the draft value, whichever source won", not bad_key, bad_key[:3])
check("a Whitaker value is Whitaker's own analysis of that form, with the draft's headword",
      not bad_w, bad_w[:3])
check("a draft value is exactly the draft, with no lemma_key", not bad_d, bad_d[:3])
check("flagged for review exactly when Whitaker disagrees, is ambiguous, or has nothing",
      not bad_flag, bad_flag[:3])
check("review is a list of reasons or null, never empty",
      all(t["review"] is None or (isinstance(t["review"], list) and t["review"]) for t in tokens))
check("no lemma or parsing is an empty string or null",
      all(t["lemma"] and t["parsing"] for t in tokens))

print("\n--- the undrafted tokens (the printed hymns)")
check("undrafted token count", len(undrafted) == EXPECTED_UNDRAFTED["tokens"], len(undrafted))


def status_count(ts, f):
    out = {}
    for t in ts:
        pv = t["provenance"][f]
        k = (pv["was"] if pv["source"] == L.OVERRIDE_SOURCE else pv)["status"]
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))


OVU = L.load_overrides()
for f in ("lemma", "parsing"):
    got = status_count(undrafted, f)
    check(f"undrafted {f} status as measured (before Adam's answers)",
          got == EXPECTED_UNDRAFTED[f + "_status"], got)
bad_u = [t["address"] for t in undrafted if t["address"] not in OVU and
         (t["lemma"], t["lemma_key"], t["parsing"],
          {k: v for k, v in t["provenance"].items() if k != "gloss"}, t["review"]) !=
         L.resolve_undrafted(arows[t["search_key"]])]
check("every undrafted token is exactly what resolve_undrafted gives (its gloss provenance aside: "
      "whitaker_gloss.py)", not bad_u, bad_u[:3])
check("an undrafted token records that it had no draft",
      all(t["provenance"]["lemma"]["draft"] is None and t["provenance"]["parsing"]["draft"] is None
          for t in undrafted))
check("an undrafted token with no lemma is flagged; a sole or same-lemma one is not",
      all(bool(t["review"]) == (t["provenance"]["lemma"]["status"] in ("ambiguous", "unknown", "disagree"))
          for t in undrafted if t["address"] not in OVU))
check("flagged undrafted tokens as measured (before Adam's answers)",
      sum(1 for t in undrafted if t["review"] or t["address"] in OVU) == EXPECTED_UNDRAFTED["flagged_for_review"])

print("\n--- nothing overwritten silently")
# The drafts, restored, must be exactly the pre-D3 values. Those came from the
# vault's batch files; the committed hymn file before D3 is git history, so
# check against the vault when it is reachable, and against the recorded
# drafts' own shape otherwise.
B = load("build_hymn_corpus")
shelf = next((x for x in B.SOURCE_CANDIDATES if x and os.path.isdir(x)), None)
if shelf:
    drafts = {}
    for H in (H for H in B.HYMNS.values() if "batch" in H):
        batch = json.load(open(os.path.join(shelf, H["batch"]), encoding="utf-8"))
        for p in batch["passages"]:
            if not p["id"].startswith(H["legacy_prefix"] + "."):
                continue
            for w in p["witnesses"]:
                for tk in w.get("tokens") or []:
                    drafts[tk.get("address")] = (tk.get("lemma") or None, tk.get("parsing") or None)
    miss = [t["address"] for t in tokens
            if drafts.get(t["legacy_address"]) != (t["provenance"]["lemma"]["draft"],
                                                   t["provenance"]["parsing"]["draft"])]
    check("every recorded draft is the vault batch file's value, token for token", not miss, miss[:3])
else:
    print("skip  the Latin shelf is not reachable; drafts not compared with the batch files")

print("\n--- the resolver's rules")


def A_(key, lemma, head, parse, pos=None, enc=None):
    return {"key": key, "lemma": lemma, "headword": head, "pos": pos or parse["pos"],
            "form_by": "whitaker", "parse": parse, "whitaker": " ".join(str(v) for v in parse.values()),
            "enclitic": enc, "sources": ["DICTLINE.GEN:1"]}


V1 = {"pos": "V", "decl": [1, 1], "tense": "PRES", "voice": "ACTIVE", "mood": "IND", "person": 1, "number": "S"}
P1 = {"pos": "PREP", "case": "ACC"}
P2 = {"pos": "PREP", "case": "ABL"}
r = L.resolve_undrafted([A_("adoro  V", "adoro, adorare", "adoro", V1)])
check("no draft, one entry, one parse: Whitaker's lemma, key and parse (sole), not flagged",
      r[:3] == ("adoro, adorare", "adoro  V", "1 sg pres ind act, 1 conj")
      and r[3]["lemma"]["status"] == "sole" and r[3]["lemma"]["draft"] is None and r[4] is None)
r = L.resolve_undrafted([A_("in  PREP  ACC", "in", "in", P1), A_("in  PREP  ABL", "in", "in", P2)])
check("no draft, two entries of one word: the lemma, no key, no parse, not flagged (same-lemma)",
      r[:3] == ("in", None, None) and r[3]["lemma"]["status"] == "same-lemma" and r[4] is None)
N3 = {"pos": "N", "decl": [3, 1], "case": "NOM", "number": "S", "gender": "M"}
r = L.resolve_undrafted([A_("panis, panis  N", "panis, panis", "panis", N3),
                         A_("pane, panis  N", "pane, panis", "pane", N3)])
check("no draft, two words: no lemma, flagged, the candidates listed (ambiguous)",
      r[:3] == (None, None, None) and r[3]["lemma"]["status"] == "ambiguous"
      and len(r[3]["lemma"]["whitaker"]) == 2 and r[4])
r = L.resolve_undrafted([A_("te  PRON", "tu", "tu", {"pos": "PRON", "case": "ACC"}),
                         A_("te  PRON", "tu", "tu", {"pos": "PRON", "case": "ABL"})])
check("no draft, one entry, two parses: the lemma, no parse, NOT flagged (ambiguous parsing)",
      r[0] == "tu" and r[2] is None and r[3]["parsing"]["status"] == "ambiguous" and r[4] is None)
r = L.resolve_undrafted([])
check("no draft, no analysis: nothing, flagged (unknown)",
      r[:3] == (None, None, None) and r[3]["lemma"]["status"] == "unknown" and r[4])
r = L.resolve("adōrō, -āre", "1 sg pres ind act", [A_("adoro  V", "adoro, adorare", "adoro", V1)])
check("agree: Whitaker's lemma and its one parse are taken; the draft is recorded",
      r[0] == "adoro, adorare" and r[1] == "adoro  V" and r[3]["lemma"]["draft"] == "adōrō, -āre"
      and r[3]["parsing"]["status"] == "whitaker" and r[4] is None)
r = L.resolve("amō", "1 sg pres ind act", [A_("adoro  V", "adoro, adorare", "adoro", V1)])
check("disagree: another headword -> the draft stays, flagged",
      r[0] == "amō" and r[1] is None and r[3]["lemma"]["status"] == "disagree" and r[4])
r = L.resolve("adōrō", "1 sg pres ind act", [])
check("unknown: no analysis -> the draft stays, flagged", r[0] == "adōrō" and r[4]
      and r[3]["lemma"]["status"] == "unknown")
r = L.resolve("adōrō", "1 sg pres ind act", [A_("adoro  V (1st)", "adoro, adorare", "adoro", V1),
                                             A_("adoro  V (3rd)", "adoro, adorere", "adoro", V1)])
check("ambiguous: two entries, nothing in the draft to choose -> draft stays, flagged",
      r[0] == "adōrō" and r[3]["lemma"]["status"] == "ambiguous" and r[4])
r = L.resolve("adōrō, -āre", "1 sg pres ind act", [A_("adoro  V (1st)", "adoro, adorare", "adoro", V1),
                                                   A_("adoro  V (3rd)", "adoro, adorere", "adoro", V1)])
check("the draft's own principal parts choose among entries", r[1] == "adoro  V (1st)" and r[4] is None)
V2 = dict(V1, person=3)
r = L.resolve("adōrō", "1 sg pres ind act", [A_("adoro  V", "adoro, adorare", "adoro", V2)])
check("parse conflict: lemma agrees, parsing keeps the draft, flagged",
      r[0] == "adoro, adorare" and r[2] == "1 sg pres ind act"
      and r[3]["parsing"]["status"] == "disagree" and r[4])
r = L.resolve("adōrō", "1 sg pres ind act, irregular", [A_("adoro  V", "adoro, adorare", "adoro", V1)])
check("a draft with a teaching note is confirmed, not replaced",
      r[2] == "1 sg pres ind act, irregular" and r[3]["parsing"]["status"] == "confirmed" and r[4] is None)
N1 = {"pos": "N", "decl": [3, 1], "case": "NOM", "number": "S", "gender": "F"}
N2 = dict(N1, case="VOC")
r = L.resolve("deitās", "nom sg", [A_("deitas  N", "deitas, deitatis", "deitas", N1),
                                   A_("deitas  N", "deitas, deitatis", "deitas", N2)])
check("several parses the draft fits: draft parsing kept, not flagged",
      r[2] == "nom sg" and r[3]["parsing"]["status"] == "draft-consistent" and r[4] is None)
r = L.resolve("deitās", "voc sg (= nom)", [A_("deitas  N", "deitas, deitatis", "deitas", N1)])
check("a draft naming two cases is never narrowed by Whitaker", r[2] == "voc sg (= nom)")


def via(a, *steps):
    return dict(a, via=list(steps))


TRICK = {"kind": "TRICK", "table": "Mediaeval_Tricks", "rule": "internal e/ae", "as": "adoro"}
r = L.resolve("adōrō, -āre", "1 sg pres ind act", [via(A_("adoro  V", "adoro, adorare", "adoro", V1), TRICK)])
check("a lemma reached by a WORDS trick is taken, and says which trick",
      r[1] == "adoro  V" and r[3]["lemma"]["via"] == [TRICK] and r[4] is None)
r = L.resolve("adōrō, -āre", "1 sg pres ind act", [A_("adoro  V", "adoro, adorare", "adoro", V1),
                                                   via(A_("adoro  V", "adoro, adorare", "adoro", V1), TRICK)])
check("a lemma Whitaker also reaches plainly records no `via`", "via" not in r[3]["lemma"])
SUF = {"kind": "SUFFIX", "fix": "an", "source": "ADDONS.LAT:1"}
r = L.resolve("pellicānus, -ī m.", "voc sg", [via(A_("pellex  N", "pellex, pellicis", "pellex", N2), SUF)])
check("a reading only by prefix/suffix formation: disagree, named with its suffix, its own reason",
      r[3]["lemma"]["status"] == "disagree" and r[3]["lemma"]["whitaker"] == ["pellex, pellicis (by suffix -an)"]
      and r[4] == ["lemma: Whitaker reaches this form only by prefix/suffix word formation"])
TW1 = {"kind": "TWO_WORDS", "rule": "two words", "as": "pelli+cane", "part": 1}
TW2 = dict(TW1, part=2)
r = L.resolve("pellicānus, -ī m.", "voc sg", [via(A_("pellis  N", "pellis, pellis", "pellis", N2), TW1),
                                              via(A_("canis  N", "canis, canis", "canis", N2), TW2)])
check("a two-words guess is never taken: unknown, the guess recorded",
      r[3]["lemma"]["status"] == "unknown" and r[0] == "pellicānus, -ī m." and r[3]["lemma"]["candidates"] == 0
      and r[3]["lemma"]["whitaker_guess"] == ["pelli+cane part 1: pellis, pellis",
                                              "pelli+cane part 2: canis, canis"])

print("\n--- Adam's overrides")
answered = {t["address"] for t in all_tokens
            if L.OVERRIDE_SOURCE in (t["provenance"]["lemma"]["source"], t["provenance"]["parsing"]["source"])}
check("the overrides file is committed, and every row in it is applied to its token (review.py writes it)",
      os.path.exists(L.OVERRIDES) and answered == set(OV), sorted(answered ^ set(OV))[:3])
check("the hymn manifest declares adam-reviewed exactly when a row is applied",
      (L.OVERRIDE_SOURCE in hman["sources"]) == bool(OV))


def loads(*rows):
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        for r_ in rows:
            f.write(json.dumps(r_) + "\n")
    try:
        return L.load_overrides(path)
    except ValueError as e:
        return str(e)
    finally:
        os.remove(path)


ROW = {"address": "wh-X/la.1.t01", "surface": "Adoro", "lemma_key": "adoro  V", "reviewed_on": "2026-09-27"}
check("a well-formed row loads, keyed by token address", loads(ROW) == {"wh-X/la.1.t01": ROW})
check("a missing file is no overrides", L.load_overrides(os.path.join(HERE, "no-such-file.jsonl")) == {})
check("a row that sets nothing is refused",
      "sets none" in loads({k: v for k, v in ROW.items() if k != "lemma_key"}))
check("a row without its surface, or with a bad date, is refused",
      "surface" in loads({k: v for k, v in ROW.items() if k != "surface"})
      and "reviewed_on" in loads(dict(ROW, reviewed_on="27 Sept")))
check("an unknown field is refused (a typo must not be silently ignored)",
      "unknown fields" in loads(dict(ROW, lemm="x")))
check("the same token twice is refused", "twice" in loads(ROW, ROW))

AN = [A_("adoro  V", "adoro, adorare", "adoro", V1), A_("adoro  V (3rd)", "adoro, adorere", "adoro", V1)]
base = L.resolve("adōrō", "1 sg pres ind act", AN)          # ambiguous, flagged
out = L.apply_override(base, "Adoro", AN, ROW)
check("lemma_key alone takes that Whitaker entry: its lemma, provenance adam-reviewed, the draft kept",
      out[0] == "adoro, adorare" and out[1] == "adoro  V" and out[3]["lemma"]["source"] == "adam-reviewed"
      and out[3]["lemma"]["draft"] == "adōrō" and out[3]["lemma"]["was"]["status"] == "ambiguous"
      and out[3]["lemma"]["was"]["value"] == "adōrō" and out[4] is None)
check("what the row does not set stays as resolved", out[2] == base[2] and out[3]["parsing"] == base[3]["parsing"])
out = L.apply_override(base, "Adoro", AN, {"address": "a", "surface": "Adoro", "reviewed_on": "2026-09-27",
                                           "lemma": "adōrō, -āre", "note": "house spelling"})
check("a lemma of Adam's own, with no Whitaker key, is taken as written",
      out[0] == "adōrō, -āre" and out[1] is None and out[3]["lemma"]["note"] == "house spelling")
pbase = L.resolve("adōrō", "1 sg pres ind act", [A_("adoro  V", "adoro, adorare", "adoro", V2)])
out = L.apply_override(pbase, "Adoro", AN, {"address": "a", "surface": "Adoro", "reviewed_on": "2026-09-27",
                                            "parsing": "3 sg pres ind act, 1 conj"})
check("a parsing override clears the parsing reason and keeps the replaced value under `was`",
      out[2] == "3 sg pres ind act, 1 conj" and out[3]["parsing"]["was"]["value"] == "1 sg pres ind act"
      and out[3]["parsing"]["was"]["status"] == "disagree" and out[4] is None and out[0] == pbase[0])
out = L.apply_override((base[0], base[1], base[2], base[3], ["lemma: x", "parsing: y"]), "Adoro", AN,
                       {"address": "a", "surface": "Adoro", "reviewed_on": "2026-09-27", "parsing": "p"})
check("reasons Adam did not answer stand", out[4] == ["lemma: x"])


def raises(fn):
    try:
        fn()
    except ValueError:
        return True
    return False


check("a lemma_key that is not one of Whitaker's analyses of the form is refused",
      raises(lambda: L.apply_override(base, "Adoro", AN, dict(ROW, lemma_key="amo  V"))))
check("an override whose surface is not the token's is refused (the text moved)",
      raises(lambda: L.apply_override(base, "Adorote", AN, ROW)))

# ============================================================ AGAINST THE FILES
print("\n--- against the Whitaker files")
if not W.have_cache():
    print("skip  the Whitaker files are not fetched (python3 pipeline/build_lemma_spine.py --fetch);")
    print("      the pins and the rebuild did not run.")
else:
    bad = [fn for fn in W.DATA_FILES if W.sha256(os.path.join(W.CACHE, fn)) != W.PINS[fn]]
    check("every fetched file matches its pin", not bad, bad)
    lic = open(os.path.join(W.CACHE, "LICENCE.txt"), encoding="utf-8").read()
    check("LICENCE.txt at the pinned commit contains the grant", " ".join(GRANT.split()) in " ".join(lic.split()))
    blobs, m2 = S.build()
    diff = [fn for fn in S.COMMITTED if open(os.path.join(LEM, fn), "rb").read() != blobs[fn]]
    check("rebuild of the committed lemma files is byte-identical", not diff, diff)
    check("the full table's checksum is the manifest's",
          hashlib.sha256(blobs["lemmas.jsonl"]).hexdigest() == man["files_sha256"]["lemmas.jsonl"])

print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
