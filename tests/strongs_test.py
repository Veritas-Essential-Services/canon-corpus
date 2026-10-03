#!/usr/bin/env python3
# prov: 2026-10-02 claude-opus-5-5 drafted
# fable_review: pending
"""
strongs_test.py -- data/strongs/ (pipeline/build_strongs.py, README-strongs.md).

Run:  python3 tests/strongs_test.py

OFFLINE (always): the table is the whole H1-H8674 / G1-G5624 numbering, one
row each, in the house key form; every word has exactly one proposed uid, and
no proposed uid is held by anything in the registry (mapped, tombstoned or
reserved); the registry itself holds no strongs: citation unless the proposal
says registered; witness files carry citations only, never lexicon text;
every concordance passage is a real passage uid of its corpus, and every
corpus token's key is in the table.

AGAINST THE SOURCES (when data/corpus/lexicons/ holds them): a rebuild is
byte-identical and proposes nothing new.
"""
import json
import os
import re
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import build_strongs as B  # noqa: E402
import wh_uid  # noqa: E402

fails = 0


def ok(c, m):
    global fails
    print(("ok    " if c else "FAIL  ") + m)
    if not c:
        fails += 1


def rows(name):
    return B.read_jsonl(os.path.join(B.OUT, name))


def local_rows(name):
    """A file built from the KJV tags: build/strongs/ only, never committed."""
    p = os.path.join(B.LOCAL, name)
    return B.read_jsonl(p) if os.path.exists(p) else None


# -- the key -----------------------------------------------------------------
for raw, lang, want in (("G0026", None, ("G26", None)), ("26", "greek", ("G26", None)),
                        ("H2617", None, ("H2617", None)), ("0175", "hebrew", ("H175", None)),
                        ("G0001G", None, ("G1", "G")), ("H1254a", None, ("H1254", "a")),
                        ("h 12", None, (None, None)), ("H0", None, (None, None)),
                        ("26", None, (None, None)), ("", None, (None, None)),
                        ("strongs:G26", None, (None, None))):
    ok(B.normalize(raw, lang) == want, f"normalize({raw!r}, {lang}) -> {want}")

# -- the table ---------------------------------------------------------------
table = rows("strongs.jsonl")
keys = [t["strongs"] for t in table]
ok(len(table) == 14298, f"14,298 rows (got {len(table):,})")
ok(set(keys) == {f"H{n}" for n in range(1, 8675)} | {f"G{n}" for n in range(1, 5625)},
   "exactly H1-H8674 and G1-G5624")
ok(keys == sorted(keys, key=B.sort_key), "rows in key order, Hebrew first")
ok(all(re.fullmatch(r"[HG][1-9]\d*", k) for k in keys), "every key is the house form (no zero padding)")
ok(all(t["citation"] == f"strongs:{t['strongs']}" for t in table), "citation is strongs:<key>")
ok(all(t["entry"] == ("strongs-hebrew:" if t["strongs"][0] == "H" else "strongs-greek:") + t["strongs"]
       for t in table), "entry names the 1890 dictionary unit")
not_used = [t["strongs"] for t in table if t.get("not_used")]
ok(len(not_used) == 101 and "G2717" in not_used and all(k[0] == "G" for k in not_used),
   f"101 Greek 'Not Used' numbers flagged, G2717 among them (got {len(not_used)})")
ok(all(t["lemma"] for t in table if not t.get("not_used")), "every used number has a lemma")
by = {t["strongs"]: t for t in table}
nfc = lambda x: unicodedata.normalize("NFC", x)
ok(nfc(by["G26"]["lemma"]) == nfc("ἀγάπη") and nfc(by["H2617"]["lemma"]) == nfc("חֶסֶד"), "ἀγάπη is G26, חֶסֶד is H2617")
ok(by["G26"]["see"] == ["G25"], "G26 points at G25 (its derivation)")
ok(all(s in by for t in table for s in t["see"]), "every see-also resolves inside the table")
ok(sum(t["lang"] == "arc" for t in table) > 600, "Aramaic entries marked arc")

# -- proposed uids -------------------------------------------------------------
props = rows("proposed-uids.jsonl")
reg = wh_uid.WhUidRegistry(B.REGISTRY)
held = reg.all_uids() | reg.reserved
ok([p["strongs"] for p in props] == [k for k in keys if k not in set(not_used)],
   "one proposal per used number, in table order; none for 'Not Used'")
ok(all(wh_uid.is_uid(p["uid"]) for p in props), "every proposal is a well-formed wh- uid")
ok(len({p["uid"] for p in props}) == len(props), "no two proposals share a uid")
ok(all(p["kind"] == "lexeme" and p["citation"] == f"strongs:{p['strongs']}" for p in props),
   "kind lexeme, citation strongs:<key>")
clash = [p for p in props if p["status"] == "proposed" and p["uid"] in held]
ok(not clash, f"no proposed uid is held by the registry ({len(clash)} clash)")
ok(all(reg.map.get(p["citation"]) == p["uid"] for p in props if p["status"] == "registered"),
   "every 'registered' proposal is in the registry with the same uid")
stray = [c for c in reg.map if c.startswith("strongs:")
         and c not in {p["citation"] for p in props if p["status"] == "registered"}]
ok(not stray, "the registry holds no strongs: citation the proposals don't account for")

# -- witnesses ---------------------------------------------------------------
wit = rows("witnesses.jsonl")
ok([w["strongs"] for w in wit] == keys, "one witness row per table row")
CIT = re.compile(r"^[a-z0-9][a-z0-9.\-]*:[A-Za-z0-9.\-_]+$")
cits = [c for w in wit for v in w["witnesses"].values() for c in ([v] if isinstance(v, str) else v)]
ok(all(CIT.match(c) for c in cits), f"witnesses are citations only, no text ({len(cits):,} links)")
ok(all(set(w["witnesses"]) <= {"strongs-1890", *B.WITNESSES, *(n + "-shared" for n in B.WITNESSES)} for w in wit),
   "only known witness books")
ok(wit[[w["strongs"] for w in wit].index("H430")]["witnesses"].get("bdb") == ["bdb-hebrew:BDB430"],
   "H430: BDB's own entry only; the entry for YHWH, which also lists it, is bdb-shared")
ww = {w["strongs"]: w["witnesses"] for w in wit}
ok("bdb-hebrew:BDB2965" in ww["H2617"].get("bdb", []), "H2617 חֶסֶד is witnessed by BDB2965")
ok("tbesg-greek:G0001G" in ww["G1"].get("tbesg", []) and "tbesg-greek:G0001H" in ww["G1"]["tbesg"],
   "G1 keeps both of TBESG's words (alpha and the interjection)")
ok(all(not k.startswith("H") or "lsj" not in v for k, v in ww.items()), "no Greek lexicon on a Hebrew number")

# -- concordance -------------------------------------------------------------
conc = rows("concordance.jsonl")
man = json.load(open(os.path.join(B.OUT, "manifest.json"), encoding="utf-8"))
ok(all(c["strongs"] in by for c in conc), "every concordance key is in the table")
ok(not any(by[c["strongs"]].get("not_used") for c in conc), "no 'Not Used' number occurs")
for name, rel in B.CORPORA.items():
    toks = B.load_corpus(name)
    if toks is None:
        print(f"skip  {rel}: shards not built here (python3 pipeline/rebuild_bible.py)")
        continue
    pu = {t["passage_uid"] for t in toks}
    ntok = len(toks)
    got = [u for c in conc for u in c["passages"].get(name, [])]
    if not got and man["concordance"][name]["tokens_without_key"] == man["concordance"][name]["tokens"]:
        print(f"skip  {rel}: its tokens carry no Strong's key (withheld by the licence gate)")
        continue
    ok(got and set(got) <= pu, f"{name}: every concordance passage is a {rel} passage uid ({len(got):,} links)")
    ok(sum(c["tokens"].get(name, 0) for c in conc) == ntok == man["concordance"][name]["tokens"],
       f"{name}: token counts sum to the corpus ({ntok:,})")
    ok(all(len(set(c["passages"][name])) == len(c["passages"][name]) for c in conc if name in c["passages"]),
       f"{name}: a passage is listed once per number")
cc = {c["strongs"]: c for c in conc}
if "nt" in cc.get("G26", {}).get("passages", {}):
    ok(cc["G26"]["tokens"]["nt"] == 116, f"ἀγάπη G26 occurs 116 times in the NT (got {cc['G26']['tokens']['nt']})")

# -- the English half: KJV tags (built locally; rights call pending) ------------
import hashlib  # noqa: E402
kjv_uids = {c: u for c, u in reg.map.items() if c.startswith("kjv:")}
IN_GIT = os.path.exists(os.path.join(ROOT, ".git"))   # a file in a worktree
r = subprocess.run(["git", "-C", ROOT, "ls-files", "data/strongs", "build"], capture_output=True, text=True)
tracked = set(r.stdout.split())
allowed = {f"data/strongs/{n}" for n in B.FILES} | {f"data/strongs/{n}.prov.md" for n in B.FILES}
if IN_GIT:
    ok(r.returncode == 0 and tracked <= allowed,
       "git tracks only the committed Strong's files: nothing built from the KJV tags (rights call pending)")
else:
    print("skip  git tracking checks: not a git checkout")
ok(man["local"]["rights"]["committed"] is False and "GPL" in man["local"]["rights"]["license"],
   "the manifest labels the KJV-tag files: not committed, the GPL question named")
ok(set(man["local"]["files"]) == set(B.LOCAL_FILES), "the manifest records every local file's sha256")
ok(not any("kjv" in c["passages"] for c in conc), "the committed concordance holds no KJV-tag links")
kt = local_rows("kjv-tags.jsonl")
alltags = None
if kt is None:
    print("skip  KJV tags: not built here (python3 pipeline/build_strongs.py --fetch, then build)")
else:
    for name in B.LOCAL_FILES:
        p = os.path.join(B.LOCAL, name)
        ok(os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest()
           == man["local"]["files"][name]["sha256"], f"build/strongs/{name}: sha256 is the manifest's")
    ok(len(kt) == 31102 == len(kjv_uids), f"one row per KJV verse ({len(kt):,})")
    ok(all(kjv_uids.get(r["citation"]) == r["passage_uid"] for r in kt),
       "every row's passage_uid is the registry's uid for its citation")
    alltags = [t for r in kt for t in r["tags"] + r.get("title_tags", [])]
    ok(all(k in by and not by[k].get("not_used") for _, k in alltags),
       f"every tag is a used number in the table ({len(alltags):,} tags)")
    ok(man["kjv"]["tags"] == len(alltags) == 349308, "349,308 tags, as the source carries")
    g11 = next(r for r in kt if r["citation"] == "kjv:Gen.1.1")
    ok(["beginning", "H7225"] in g11["tags"] and ["God", "H430"] in g11["tags"],
       "Gen 1:1: beginning is H7225, God is H430")
    j316 = next(r for r in kt if r["citation"] == "kjv:John.3.16")
    ok(["loved", "G25"] in j316["tags"], "John 3:16: loved is G25")
    ps3 = next(r for r in kt if r["citation"] == "kjv:Ps.3.1")
    ok(["Absalom", "H53"] in ps3.get("title_tags", []), "Psalm 3's title is kept beside verse 1, not in it")
    ren = {r["strongs"]: r["renderings"] for r in local_rows("kjv-renderings.jsonl")}
    ok(ren["H430"].get("god", 0) > 2000 and "LORD" in ren.get("H3068", {}),
       "renderings: H430 is mostly god; H3068 keeps LORD in capitals")
    ok(sum(sum(v.values()) for v in ren.values()) == len(alltags), "renderings count every tag once")
    ku = {u for c in local_rows("concordance-kjv.jsonl") for u in c["passages"]}
    ok(ku and ku <= set(kjv_uids.values()), "concordance kjv passages are KJV verse uids")

# -- parallels ----------------------------------------------------------------
par = rows("parallels.jsonl")
pp = {r["kjv"]: r["parallels"] for r in par}
ok(all(("kjv:" + r["kjv"]) in kjv_uids for r in par), "every parallels row is a KJV verse")
ok(pp.get("Ps.23.1", {}).get("vulgate") == ["vulgate:Ps.22.1"] and pp["Ps.23.1"].get("douay") == ["douay:Ps.22.1"],
   "Psalm 23:1 is Psalm 22:1 in the Vulgate and the Douay")
ok("Gen.1.1" not in pp, "a verse with the same number everywhere is not listed")
ok(pp.get("Gen.49.32", {}).get("vulgate") == [], "Gen 49:32, which the Clementine lacks, says so with []")
ok(all(i.startswith(n + ":") for v in pp.values() for n, ids in v.items() for i in ids),
   "parallel ids name their own Bible")
ok(pp.get("Ps.23.1", {}).get("brenton") == ["brenton:Ps.22.1"], "Psalm 23:1 is Brenton's Psalm 22:1")
ok(not any("brenton" in v for o, v in pp.items() if o.split(".")[0] in B.NT_BOOKS),
   "no New Testament verse is listed for Brenton (the Septuagint has none)")

# -- the concordance view (local) ---------------------------------------------
view = local_rows("concordance-view.jsonl") if kt is not None else None
if view is None:
    print("skip  concordance view: not built here")
else:
    vb = {r["strongs"]: r for r in view}
    ok([r["strongs"] for r in view] == [k for k in keys if k not in set(not_used)],
       f"one view row per used number ({len(view):,})")
    occ = lambda r: r["kjv"]["occurrences"] + r["kjv"]["psalm_title_occurrences"]
    ok(all(occ(r) == sum(r["kjv"]["renderings"].values()) for r in view),
       "each row's renderings add up to its KJV occurrences, Psalm titles included")
    ok(sum(occ(r) for r in view) == len(alltags), "the view counts every KJV tag once")
    ok(vb["H4210"]["kjv"]["verses"] == [] and "Ps.3" in vb["H4210"]["kjv"]["psalm_titles"],
       "mizmor (H4210) stands only in Psalm titles: filed under the titles, never under verse 1")
    ok(all(set(r["parallels"]) <= set(r["kjv"]["verses"]) and all(pp[o] == v for o, v in r["parallels"].items())
           for r in view), "a row's parallels are its own verses, as parallels.jsonl gives them")
    ok(all(r["lexicons"] == ww[r["strongs"]] for r in view), "a row's lexicons are its witnesses row")
    ok("Ps.23.1" in vb["H7462"]["kjv"]["verses"] and vb["H7462"]["parallels"]["Ps.23.1"]["vulgate"] == ["vulgate:Ps.22.1"],
       "H7462 (shepherd): Ps 23:1, with its Vulgate verse 22:1")
    ok(vb["G26"]["kjv"]["renderings"].get("charity") == 28, "G26: the KJV renders it charity 28 times")

# -- OSHB's CC BY layer: built locally, never committed -------------------------
r = subprocess.run(["git", "-C", ROOT, "ls-files", "build/strongs"], capture_output=True, text=True)
if IN_GIT:
    ok(r.returncode == 0 and not r.stdout.strip(), "nothing under build/strongs (OSHB layer, KJV-tag files) is tracked")
ok(man["oshb_layer"]["license"] == "CC BY 4.0" and man["oshb_layer"]["redistribute_whole"] is False,
   "the manifest labels the OSHB layer CC BY, not for redistribution")
ot_toks = B.load_corpus("ot")
if os.path.isdir(B.OSHB_OUT) and ot_toks is not None:
    lay = [x for f in sorted(os.listdir(B.OSHB_OUT)) if f.endswith(".jsonl")
           for x in B.read_jsonl(os.path.join(B.OSHB_OUT, f))]
    ot_tok = {t["address"]: t["surface"] for t in ot_toks}
    ok(len(lay) == len(ot_tok) and all(ot_tok.get(x["address"]) == x["surface"] for x in lay),
       f"OSHB layer: one row per data/ot token, surfaces agree ({len(lay):,})")
    ok(all(re.fullmatch(r"H[1-9]\d*", k) and k in by for x in lay for k in x["strongs"]),
       "OSHB layer: every key is plain H<n> and in the table")
    ok(all(len(x.get("augment", x["strongs"])) == len(x["strongs"]) for x in lay),
       "OSHB layer: augment letters ride beside their keys, one each")
else:
    print("skip  OSHB layer: not built here")

# -- rebuild -----------------------------------------------------------------
srcs = [os.path.join(B.LEX, s["file"]) for s in B.SOURCES.values()]
if all(os.path.exists(p) for p in srcs):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "pipeline", "build_strongs.py"), "--check"],
                       capture_output=True, text=True)
    ok(r.returncode == 0, "build_strongs.py --check: byte-identical, 0 proposed")
    if r.returncode:
        print(r.stdout + r.stderr)
else:
    print("skip  --check: Strong's sources not in data/corpus/lexicons (python3 pipeline/fetch_sources.py)")

print(f"\n{'FAILED' if fails else 'passed'}: {fails} failure(s)")
sys.exit(1 if fails else 0)
