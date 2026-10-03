#!/usr/bin/env python3
# fable_review: pending
"""
ot_corpus_test.py -- the validator for data/ot/ (the Hebrew Old Testament,
Westminster Leningrad Codex, one folder per book). README: pipeline/README-ot-jsonl.md.

    python3 tests/ot_corpus_test.py

OFFLINE (always): the shards against their manifest, every record keyed by an
EXISTING KJV verse uid (a frozen replay mints 0), the licence gate held (PD
only; no OSHB lemma, morphology, id or morpheme split anywhere), every WLC
verse accounted for (a passage, a joined verse, or a listed psalm title),
ketiv/qere well-formed, and every witness re-tokenizing to its tokens.

AGAINST THE PINNED WLC (when data/corpus/wlc/ holds it): a rebuild is
byte-identical and mints 0, and a narrowed SCOPE refuses to write.
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PIPE = os.path.join(REPO, "pipeline")
DATA = os.path.join(REPO, "data", "ot")
REGISTRY = os.path.join(REPO, "data", "uids", "wordhoard.uids.json")
sys.path.insert(0, PIPE)
import wh_uid as U  # noqa: E402
import build_ot_corpus as O  # noqa: E402
import versification as VM  # noqa: E402

PASS, FAIL = 0, []


def check(label, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label + (("  " + str(detail)[:300]) if detail != "" and not cond else ""))


# Measured 2026-10-02 from WLC 4.20 (OSHB 3d15126). Not estimated.
EXPECTED = {"books": 39, "wlc_verses": 23213, "verses": 23142, "tokens": 305124,
            "titles_left_out": 67, "joined": 4, "spans": 2, "ketiv": 1264, "qere_only": 9, "divided": 12,
            "kjv_without_hbo": ["kjv:Isa.64.1", "kjv:Neh.7.68", "kjv:Ps.13.6"]}

print("--- files")
man = json.load(open(os.path.join(DATA, "manifest.json"), encoding="utf-8"))
missing = [fn for fn in man["files_sha256"] if not os.path.exists(os.path.join(DATA, fn))]
sh = man["shards"]
check(f"{EXPECTED['books']} shards, the KJV's book order, one folder each",
      sh["layout"] == "book" and sh["order"] == O.BOOKS and len(O.BOOKS) == EXPECTED["books"]
      and all(sh["books"][b]["dir"] == b for b in sh["order"]))
check("the manifest lists exactly the four files of every shard",
      sorted(man["files_sha256"]) == sorted(f"{b}/{k}.jsonl" for b in sh["order"] for k in O.FILES))
if missing:
    # Only the manifest is committed; the shards are rebuilt. Say so and stop
    # cleanly rather than failing a fresh clone.
    check("the manifest's counts are the measured ones",
          man["counts"]["verses"] == EXPECTED["verses"] and man["counts"]["tokens"] == EXPECTED["tokens"],
          man["counts"])
    print(f"\nSKIPPED: the shard checks -- data/ot/ is not built here ({len(missing)} of "
          f"{len(man['files_sha256'])} files absent; rebuilt, not committed). "
          f"Run: python3 pipeline/rebuild_bible.py")
    if FAIL:
        print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
        sys.exit(1)
    print(f"{PASS} passed, 0 failed (shard checks skipped)")
    sys.exit(0)
bad = [fn for fn, want in man["files_sha256"].items()
       if hashlib.sha256(open(os.path.join(DATA, fn), "rb").read()).hexdigest() != want]
check("every file matches its checksum", not bad, bad[:3])
check("no output file the manifest does not list",
      not O.stale_outputs(DATA, set(man["files_sha256"]) | {"manifest.json"}))
big = max(os.path.getsize(os.path.join(DATA, fn)) for fn in man["files_sha256"]) / 1e6
check(f"no file over GitHub's 50 MB warning (largest {big:.1f} MB)", big < 50)

ot = O.load_ot(REPO)
passages, witnesses, tokens, alignments = (ot[k] for k in O.FILES)
by_uid = {p["uid"]: p for p in passages}

print("\n--- shape")
c = man["counts"]
check("verse, witness, alignment and token counts are the measured ones and the manifest's",
      len(passages) == len(witnesses) == len(alignments) == EXPECTED["verses"] == c["verses"]
      and len(tokens) == EXPECTED["tokens"] == c["tokens"], (len(passages), len(tokens)))
check("each shard's counts are its records'",
      all(sh["books"][b]["verses"] == sum(1 for p in passages if p["book"] == b)
          and sh["books"][b]["tokens"] == sum(1 for t in tokens if by_uid[t["passage_uid"]]["book"] == b)
          for b in sh["order"]))

print("\n--- identity: the KJV verse's existing uid, nothing minted")
committed = json.load(open(REGISTRY, encoding="utf-8"))["uids"]
check("no two passages share a uid", len(by_uid) == len(passages))
moved = [p["citation"] for p in passages if committed.get(p["citation"]) != p["uid"]]
check("every uid is the committed registry's uid for its kjv: citation", not moved, moved[:3])
check("citations are kjv:<OSIS> and agree with book/chapter/verse",
      all(p["citation"] == f"kjv:{p['osis']}" == f"kjv:{p['book']}.{p['chapter']}.{p['verse']}"
          for p in passages))
tmp = tempfile.mkdtemp()
try:
    shutil.copy2(REGISTRY, os.path.join(tmp, "r.json"))
    reg = U.WhUidRegistry(os.path.join(tmp, "r.json"), frozen=True)
    check("a frozen replay returns the stored uid for every verse and mints 0",
          all(reg.uid_for(p["citation"]) == p["uid"] for p in passages) and reg.minted == 0)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\n--- versification: every WLC verse accounted for")
v = man["versification"]
vm = VM.load()
check("the map is the committed one", v["map_sha256"] == hashlib.sha256(open(VM.PATH, "rb").read()).hexdigest())
wlc_of = {}
for w in witnesses:
    refs = w.get("wlc_ref", by_uid[w["passage_uid"]]["osis"])
    for r in ([refs] if isinstance(refs, str) else refs):
        wlc_of[r] = w["passage_uid"]
titles = [x["wlc"] for x in v["left_out"]]
check(f"{EXPECTED['wlc_verses']:,} WLC verses = {EXPECTED['verses']:,} passages + "
      f"{EXPECTED['joined']} joined + {EXPECTED['titles_left_out']} psalm titles, none twice",
      len(wlc_of) + len(titles) == EXPECTED["wlc_verses"] == c["wlc_verses_read"]
      and not set(wlc_of) & set(titles) and len(titles) == EXPECTED["titles_left_out"]
      and len(v["joined"]) == EXPECTED["joined"] and len(v["spans"]) == EXPECTED["spans"])
check("every left-out verse is one the map sends to a psalm title, which has no uid",
      all(VM.targets(x["wlc"], vm)[0].endswith(".title") and "kjv:" + x["kjv"] not in committed
          for x in v["left_out"]))
check("every witness's WLC verse(s) map to its passage (the first target for a span)",
      all(by_uid[u]["osis"] in VM.targets(r, vm) for r, u in wlc_of.items()))
check("a renumbered witness says where the WLC has it (wlc_ref); an unrenumbered one does not",
      all(("wlc_ref" in w) == (w.get("wlc_ref", by_uid[w["passage_uid"]]["osis"])
                               != by_uid[w["passage_uid"]]["osis"]) for w in witnesses))
joined = [w for w in witnesses if isinstance(w.get("wlc_ref"), list)]
check("a joined witness lists its WLC verses and where each starts",
      len(joined) == EXPECTED["joined"]
      and all(len(w["wlc_ref"]) == len(w["wlc_verse_starts"]) == 2 and w["wlc_verse_starts"][0] == 1
              for w in joined))
check("the KJV OT verses with no Hebrew witness are listed: Neh 7:68 and the second half of each span",
      v["kjv_verses_without_hbo"] == EXPECTED["kjv_without_hbo"])
check("the open rulings are in the manifest as house defaults",
      all(r["status"].startswith("house default") for r in v["rulings"].values())
      and sh["ruling"]["status"].startswith("house default"))

print("\n--- the licence gate: PD only")
src = man["sources"]
check("every source is PD, with its evidence", all(s["license"] in O.ALLOWED_LICENSES and s["license_basis"]
                                                   for s in src.values()))
check("no token carries a lemma, lemma_key, parsing or gloss (OSHB's are CC BY 4.0)",
      not any(t[k] for t in tokens for k in ("lemma", "lemma_key", "parsing", "gloss", "plain_form", "translit")))
check("... and the manifest says why, once",
      man["token_provenance"]["every_token"]["lemma"]["status"] == "withheld"
      and all(t["provenance"] is None for t in tokens))
leak = [r.get("address") for r in witnesses + tokens
        if re.search(r'"(?:lemma|morph|id|n)": "[^"]+"|/', json.dumps(
            {k: v for k, v in r.items() if k in ("text", "surface", "normalized", "qere", "qere_only")},
            ensure_ascii=False))]
check("no OSHB morpheme slash or attribute in any text", not leak, leak[:3])

print("\n--- tokens and text")
toks = {}
for t in tokens:
    toks.setdefault(t["passage_uid"], []).append(t)
check("tokens hang only on the verses, positions 1..n",
      set(toks) == set(by_uid) and all([t["position"] for t in ts] == list(range(1, len(ts) + 1))
                                        for ts in toks.values()))
retok = [w["address"] for w in witnesses if O.tokenize(w["text"]) != [t["surface"] for t in toks[w["passage_uid"]]]]
check("every witness's text re-tokenizes to exactly its tokens", not retok, retok[:3])
check("addresses parse and point home",
      all(U.parse_address(t["address"])["uid"] == t["passage_uid"] for t in tokens))
check("search_key is consonants only, final forms folded",
      all(t["search_key"] == O.search_key(t["normalized"]) and re.fullmatch(r"[א-ת]+", t["search_key"])
          and not re.search("[ךםןףץ]", t["search_key"]) for t in tokens))
ket = [t for t in tokens if t.get("ketiv")]
check(f"{EXPECTED['ketiv']:,} ketiv tokens, unpointed as the codex writes them, each with its qere or null",
      len(ket) == EXPECTED["ketiv"] == c["ketiv"]
      and all(not re.search("[\u05b0-\u05bc\u05c1\u05c2\u05c7]", t["surface"]) for t in ket)
      and all(t["qere"] is None or t["qere"] for t in ket)
      and all(t["qere"] is None for t in ket if t.get("not_read"))
      and all(t.get("qere") or t.get("not_read") or t.get("qere_at") for t in ket))
check(f"{EXPECTED['qere_only']} qere wela ketiv readings recorded on their witness, not as tokens",
      sum(len(w.get("qere_only", [])) for w in witnesses) == EXPECTED["qere_only"] == c["qere_only"])
check(f"the {EXPECTED['divided']} words OSHB divided with no space between are one codex word again",
      c["words_oshb_divided"] == EXPECTED["divided"]
      and man["wlc_notes_by_n"].get("exegesis", 0) >= EXPECTED["divided"])
check("section marks are pe, samekh or null", {w["section_mark"] for w in witnesses} <= {"pe", "samekh", None})
shema = "\u05e9\u05c1\u05b0\u05de\u05b7\u0596\u05e2"   # the codex's mark order, written out
check("the Shema (Deut 6:4) opens as the codex prints it, its large ayin kept as a letter",
      next(w for w in witnesses if by_uid[w["passage_uid"]]["osis"] == "Deut.6.4")["text"].split()[0] == shema)

print("\n--- alignments")
check("every alignment faces hbo.wlc with kjv.plain of the same uid, or of both verses of a span",
      all(al["a"][0]["address"] == U.address(U.parse_address(al["a"][0]["address"])["uid"], O.WITNESS)
          and (al["type"] == "1:1" and U.parse_address(al["b"][0]["address"])["uid"]
               == U.parse_address(al["a"][0]["address"])["uid"] or al["type"] == "1:2")
          for al in alignments))

print("\n--- against the pinned WLC")
import build_versification as V  # noqa: E402
if not all(os.path.exists(os.path.join(V.WLC_DIR, b + ".xml")) for b in O.BOOKS):
    print("skip  the WLC is not in data/corpus/wlc/: build_versification.py --fetch gets it")
else:
    tmp = tempfile.mkdtemp()
    try:
        shutil.copy2(REGISTRY, os.path.join(tmp, "r.json"))
        reg = U.WhUidRegistry(os.path.join(tmp, "r.json"), frozen=True)
        d, m = O.build(reg)
        blobs = O.render_all(d, m)
        diff = [fn for fn, b in blobs.items() if open(os.path.join(DATA, fn), "rb").read() != b]
        check("rebuild is byte-identical and mints 0", not diff and reg.minted == 0, diff[:3])
        narrow = os.path.join(tmp, "pipeline")
        shutil.copytree(PIPE, narrow, ignore=shutil.ignore_patterns("__pycache__"))
        src_py = open(os.path.join(narrow, "build_ot_corpus.py"), encoding="utf-8").read()
        with open(os.path.join(narrow, "build_ot_corpus.py"), "w", encoding="utf-8") as f:
            f.write(src_py.replace("SCOPE = list(BOOKS)", 'SCOPE = ["Gen"]', 1))
        r = subprocess.run([sys.executable, os.path.join(narrow, "build_ot_corpus.py"), "--check",
                            "--out", os.path.join(tmp, "out")], capture_output=True, text=True)
        check("a narrowed SCOPE refuses to write or --check", r.returncode != 0
              and "SCOPE is narrowed" in r.stdout + r.stderr, r.stderr[-200:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
