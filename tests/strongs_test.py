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
ok(all(set(w["witnesses"]) <= {"strongs-1890", *B.WITNESSES} for w in wit), "only known witness books")
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
    base = os.path.join(ROOT, rel)
    if not os.path.isdir(base):
        print(f"skip  {rel}: not in this checkout")
        continue
    pu = set()
    ntok = 0
    for book in B._books(base):
        pu |= {p["uid"] for p in B.read_jsonl(os.path.join(base, book, "passages.jsonl"))}
        ntok += sum(1 for _ in open(os.path.join(base, book, "tokens.jsonl"), encoding="utf-8"))
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

# -- the English half: KJV tags ----------------------------------------------
kt = rows("kjv-tags.jsonl")
kjv_uids = {c: u for c, u in reg.map.items() if c.startswith("kjv:")}
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
ren = {r["strongs"]: r["renderings"] for r in rows("kjv-renderings.jsonl")}
ok(ren["H430"].get("god", 0) > 2000 and "LORD" in ren.get("H3068", {}),
   "renderings: H430 is mostly god; H3068 keeps LORD in capitals")
ok(sum(sum(v.values()) for v in ren.values()) == len(alltags), "renderings count every tag once")
ku = {u for c in conc for u in c["passages"].get("kjv", [])}
ok(ku and ku <= set(kjv_uids.values()), "concordance kjv passages are KJV verse uids")

# -- OSHB's CC BY layer: built locally, never committed -------------------------
r = subprocess.run(["git", "-C", ROOT, "ls-files", "build/strongs"], capture_output=True, text=True)
ok(r.returncode == 0 and not r.stdout.strip(), "no OSHB layer file is tracked by git")
ok(man["oshb_layer"]["license"] == "CC BY 4.0" and man["oshb_layer"]["redistribute_whole"] is False,
   "the manifest labels the OSHB layer CC BY, not for redistribution")
if os.path.isdir(B.OSHB_OUT) and os.path.isdir(os.path.join(ROOT, "data", "ot")):
    lay = [x for f in sorted(os.listdir(B.OSHB_OUT)) if f.endswith(".jsonl")
           for x in B.read_jsonl(os.path.join(B.OSHB_OUT, f))]
    ot_tok = {}
    for book in B._books(os.path.join(ROOT, "data", "ot")):
        for t in B.read_jsonl(os.path.join(ROOT, "data", "ot", book, "tokens.jsonl")):
            ot_tok[t["address"]] = t["surface"]
    ok(len(lay) == len(ot_tok) and all(ot_tok.get(x["address"]) == x["surface"] for x in lay),
       f"OSHB layer: one row per data/ot token, surfaces agree ({len(lay):,})")
    ok(all(B.normalize(k)[0] in by for x in lay for k in x["strongs"]),
       "OSHB layer: every key is in the table")
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
