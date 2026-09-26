#!/usr/bin/env python3
"""
proper_names_test.py -- the house proper-names table (pipeline/proper_names.py,
data/lemmas/proper-names/).

Run:  python3 tests/proper_names_test.py

WHAT IT ASSERTS
    OFFLINE (always runs)
    1. The spelling keys that match Vulgate names to Hitchcock's (King James)
       headwords, and the three match tiers, first tier that finds wins.
    2. The paradigms: a nominative heads its attested oblique forms; a form
       claimed first never heads a later class; a Hitchcock headword is never
       another name's oblique form; the consonant-stem and -am conditions;
       a form claimed twice keeps both; an unclaimed form is "one form".
    3. The committed table: its manifest's checksum, one row per lemma, pos
       `proper`, headword = the folded lemma, every form tokens > 0 and
       capitalised mid-sentence, no form in two rows unless marked shared,
       Hitchcock entries carried verbatim with their tier, the licences.
    4. load(): every form of every row is a `proper` reading of its lemma.
    AGAINST THE SOURCES (when the Vulgate, Hitchcock and Whitaker are fetched)
    5. Rebuilding gives the committed files byte for byte, and the table
       holds what the method says (Aaron one form; Jonathas's forms;
       Nathinaeis not an -is nominative). The house supplement's
       `attested` counts are the Vulgate's.
"""
import importlib.util
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PIPE = os.path.join(REPO, "pipeline")
sys.path.insert(0, PIPE)


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(PIPE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


W = load("whitaker")
P = load("proper_names")

PASS = 0
FAIL = []


def check(label, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label + (("  " + str(detail)) if detail else ""))


print("--- 1. spelling keys and Hitchcock tiers")
check("exact: case and hyphens aside (Beth-el = Bethel)", P.exact_key("Beth-el") == P.exact_key("Bethel"))
check("spelling: z/s, k/c (Zadok = Sadoc)", P.spelling_key("Zadok") == P.spelling_key("Sadoc"))
check("spelling: sh/s, a final h dropped (Bashan = Basan; Elah = Ela)",
      P.spelling_key("Bashan") == P.spelling_key("Basan") and P.spelling_key("Elah") == P.spelling_key("Ela"))
check("spelling: j/i/y, ph/f, th/t, ae/e, doubled letters single",
      P.spelling_key("Jephthae") == P.spelling_key("iefte") and P.spelling_key("Abbia") == P.spelling_key("Abia"))
check("spelling does not reach e/he (Ezechias is not Hezekiah)",
      P.spelling_key("Ezechias") not in [P.spelling_key("Hezekiah")] + P.ending_keys("Hezekiah"))
H = P.Hitchcock([{"id": "1", "term": "Aaron", "meaning": "m1"}, {"id": "2", "term": "Elah", "meaning": "m2"},
                 {"id": "3", "term": "Elam", "meaning": "m3"}, {"id": "4", "term": "Jonathan", "meaning": "m4"},
                 {"id": "5", "term": "Tobiah", "meaning": "m5"}, {"id": "6", "term": "Gadi", "meaning": "m6"},
                 {"id": "7", "term": "Abraham", "meaning": "m7"}, {"id": "8", "term": "Micha", "meaning": "m8"}])
check("exact tier", H.match("Aaron")[0] == "exact")
check("spelling tier (Ela ~ Elah)", H.match("Ela")[0] == "spelling" and H.match("Ela")[1][0]["term"] == "Elah")
check("ending tier (Tobias less -s ~ Tobiah)", H.match("Tobias")[0] == "ending")
check("no match (Jonathas; Jonathan differs in its last letter)", H.match("Jonathas") == (None, []))
check("is_name is the exact tier only (Elam yes; Ela, which is Elah only by spelling, no)",
      H.is_name("Elam") and not H.is_name("Ela"))

print("\n--- 2. paradigms")
forms = ["jonathas", "jonathae", "jonatha", "ela", "elam", "gad", "gadi", "simon", "simonis", "simonem",
         "nathinaei", "nathinaeis", "nathinaeorum", "jordanis", "jordanem", "jordane", "abraham", "abrahae",
         "jerosolymam", "jerosolymae", "aaron", "michas", "michae", "micha", "jojada", "jojadae"]
heads, claims = P.paradigms(forms, H)
check("Jonathas heads Jonathae and Jonatha", sorted(heads["jonathas"][1]) == ["jonatha", "jonathae"])
check("Jonatha, already Jonathas's, never heads the -a class", "jonatha" not in heads)
check("Elam, a Hitchcock headword, is not Ela's accusative", "elam" not in claims)
check("Gadi, a Hitchcock headword, is not Gad's genitive", "gadi" not in claims)
check("Simon heads Simonis and Simonem (consonant stem); Simonis is no -is nominative",
      sorted(heads["simon"][1]) == ["simonem", "simonis"] and "simonis" not in heads)
check("Nathinaeis (a vowel before -is) is no -is nominative; Nathinaei heads the plural",
      "nathinaeis" not in heads and sorted(heads["nathinaei"][1]) == ["nathinaeis", "nathinaeorum"])
check("Jordanis heads Jordanem and Jordane (no Jordan written)", sorted(heads["jordanis"][1]) == ["jordane", "jordanem"])
check("Jojada heads Jojadae in the -a class, not as a consonant stem",
      P.ENDINGS[heads["jojada"][0]][0] == "a")
check("Abraham, a Hitchcock name, heads Abrahae (-am class)", heads.get("abraham", (None, []))[1] == ["abrahae"])
check("Jerosolymam, no Hitchcock name, heads nothing in the -am class", "jerosolymam" not in heads)
check("a form two nominatives claim keeps both (Michae: Michas, and Micha, a Hitchcock name)",
      sorted(claims["michae"]) == ["micha", "michas"] and "micha" not in claims)
counts = {f: 2 for f in forms}
mid = {f: 1 for f in forms}
written = {f: {f[:1].upper() + f[1:]: 2} for f in forms}
rows, _, _ = P.build_rows(counts, mid, written, {f: "unknown" for f in forms}, H)
byl = {r["lemma"]: r for r in rows}
check("an unclaimed form is its own lemma, 'one form' (Aaron)", byl["Aaron"]["paradigm"] == "one form"
      and list(byl["Aaron"]["forms"]) == ["aaron"])
check("a row carries its Hitchcock entry verbatim with the tier",
      byl["Aaron"]["hitchcock"] == [{"term": "Aaron", "id": "1", "match": "exact", "meaning": "m1"}])
check("a row's forms carry their ending from the nominative's stem",
      byl["Jonathas"]["forms"]["jonathae"]["ending"] == "ae")
check("the lemma keeps the text's spelling with j (Jonathas) and folds for the headword (ionathas)",
      byl["Jonathas"]["headword"] == "ionathas")
check("lemma_spelling: diacritics off, ligature opened, case kept",
      P.lemma_spelling({"Israël": 3, "Israel": 1}) == "Israel" and P.lemma_spelling({"Ægyptus": 1}) == "Aegyptus")

print("\n--- 3. the committed table")
man = json.load(open(os.path.join(P.OUT, "manifest.json"), encoding="utf-8"))
blob = open(P.NAMES, "rb").read()
import hashlib  # noqa: E402
check("names.jsonl matches its manifest's sha256", hashlib.sha256(blob).hexdigest() == man["files_sha256"]["names.jsonl"])
check("names.jsonl is LF-only UTF-8", b"\r" not in blob)
rows = [json.loads(l) for l in blob.decode("utf-8").splitlines()]
check(f"one row per lemma ({len(rows)}), as the manifest counts", len(rows) == man["counts"]["lemmas"])
check("every row is pos `proper` with headword = the folded lemma",
      all(r["pos"] == "proper" and r["headword"] == W.fold(r["lemma"]) for r in rows))
check("every form has tokens and was capitalised mid-sentence at least once",
      all(v["tokens"] > 0 and v["mid_sentence"] > 0 for r in rows for v in r["forms"].values()))
check("a row's tokens are its forms' tokens", all(r["tokens"] == sum(v["tokens"] for v in r["forms"].values()) for r in rows))
seen = {}
for r in rows:
    for f, v in r["forms"].items():
        seen.setdefault(f, []).append(bool(v.get("shared")))
dups = [f for f, s in seen.items() if len(s) > 1 and not all(s)]
check("a form in two rows is marked shared in both", not dups, dups[:5])
check("forms in two rows as the manifest counts", sum(1 for s in seen.values() if len(s) > 1)
      == man["counts"]["forms_with_two_lemmas"])
check("Hitchcock entries carry term, id, tier and meaning, and one tier per row",
      all(set(h) == {"term", "id", "match", "meaning"} and h["match"] in ("exact", "spelling", "ending")
          and len({x["match"] for x in r["hitchcock"]}) == 1 for r in rows for h in r["hitchcock"]))
check("the manifest records both sources' licences: PD Vulgate, PD Hitchcock",
      man["sources"]["vulgate"]["license"] == "public-domain"
      and man["sources"]["hitchcock"]["license"] == "public-domain"
      and man["sources"]["hitchcock"]["sha256"] == P.HITCHCOCK_SHA256 and man["provenance"] == "house")
check("Whitaker is used only to leave forms out, and says so",
      "nothing of it is copied" in man["sources"]["whitaker"]["used_for"])
check("paradigm classes are the method's", {r["paradigm"] for r in rows} <= {c for _, _, c, _ in P.ENDINGS} | {"one form"})

print("\n--- 4. load()")
idx = P.load()
check("every form of every row is a key", all(W.fold(f) in idx for r in rows for f in r["forms"]))
a = idx[W.fold("aaron")][0]
check("a reading is `proper`, names its lemma and its row",
      a["parse"] == {"pos": "proper"} and a["name"]["lemma"] == "Aaron"
      and a["name"]["source"].startswith("proper-names/names.jsonl:"))
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "n.jsonl")
    with open(p, "w", encoding="utf-8") as f:
        f.write(json.dumps({"lemma": "Jonathas", "headword": "ionathas", "forms": {"jonathae": {}, "jonatha": {}}}) + "\n")
    t = P.load(p)
check("load() folds j to i in its keys (jonathae -> ionathae)", sorted(t) == ["ionatha", "ionathae"])

print("\n--- 5. against the sources")
import benchmark_whitaker as B  # noqa: E402
have = W.have_cache() and os.path.exists(P.HITCHCOCK_CACHE) and all(
    os.path.exists(os.path.join(B.CACHE, b + ".lat")) for b in B.BOOKS)
if not have:
    print("skip  the Vulgate, Hitchcock or Whitaker is not fetched "
          "(benchmark_whitaker.py --fetch; proper_names.py --fetch; build_lemma_spine.py --fetch)")
else:
    blobs, m2 = P.build()
    check("a rebuild gives the committed files byte for byte",
          all(open(os.path.join(P.OUT, fn), "rb").read() == blobs[fn] for fn in P.COMMITTED))
    byl = {r["lemma"]: r for r in rows}
    check("Aaron: one form, 322 tokens, Hitchcock's Aaron (exact)",
          byl["Aaron"]["paradigm"] == "one form" and byl["Aaron"]["tokens"] == 322
          and byl["Aaron"]["hitchcock"][0]["match"] == "exact")
    check("Jonathas heads Jonathae and Jonatha", set(byl["Jonathas"]["forms"]) == {"jonathas", "jonathae", "jonatha"})
    counts = P.census(B)[0]
    try:
        B.check_attestation(W.load_house_supplement(), counts)
        ok = True
    except SystemExit as e:
        ok = str(e)
    check("the house supplement's `attested` counts are the Vulgate's, form for form", ok is True, ok)
    check("no -is nominative with a vowel before its ending (Nathinaeis, Sabaeis)",
          not [r["lemma"] for r in rows if r["paradigm"] == "3rd declension, -is" and r["lemma"][-3] in "aeiouy"])

print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
