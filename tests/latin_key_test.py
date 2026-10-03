#!/usr/bin/env python3
# prov: 2026-10-02 claude-opus-5-5 drafted
# fable_review: pending
"""
latin_key_test.py -- the Latin key: Lewis & Short's entries, Whitaker's lemmas
linked to them, and the Vulgate's words.

    python3 tests/latin_key_test.py

The linking rules are tested on inline fixtures. Only the manifest is
committed (data/lemmas/latin-key/); the files themselves derive from Perseus's
CC BY-SA text and are built to build/latin-key/, so their checks run only
after a local build, and --check only when the sources are in data/corpus/.
"""

import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))

import build_latin_key as B  # noqa: E402

fails = 0


def ok(cond, msg):
    global fails
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond:
        fails += 1


def rows(name):
    with open(os.path.join(B.LOCAL, name), encoding="utf-8") as f:
        return [json.loads(l) for l in f]


def end_to_end():
    if os.path.exists(B.LS_FILE):
        r = subprocess.run([sys.executable, os.path.join(ROOT, "pipeline", "build_latin_key.py"), "--check"],
                           capture_output=True, text=True)
        ok(r.returncode == 0, "build_latin_key.py --check: byte-identical")
        if r.returncode:
            print(r.stdout + r.stderr)
    else:
        print("skip  --check: Lewis & Short not in data/corpus (python3 pipeline/build_latin_key.py --fetch)")
    print(f"\n{'FAILED' if fails else 'passed'}: {fails} failure(s)")
    sys.exit(1 if fails else 0)


# -- the linking rules, on fixtures -------------------------------------------
def E(key, hw, cls=None, pointer=False, spellings=(), typ="main", gen=None):
    return {"key": key, "headword": hw, "class": cls, "pointer": pointer,
            "spellings": list(spellings), "type": typ, "gen": gen}


fx = [E("malus1", "malus", "ADJ"), E("malus2", "malus", "N"), E("malus3", "malus", "N"),
      E("sum1", "sum"), E("sum2", "sum", pointer=True), E("sum3", "sum-"),
      E("rursus", "rursus", "ADV", spellings=["rursum"]), E("dominor", "dominor", "V"),
      E("cum1", "cum", "PREP"), E("cum2", "cum", "CONJ"), E("qui1", "qui"), E("qui2", "qui", "ADV"),
      E("x1", "x", "N"), E("x2", "x", "N", typ="spur"),
      E("populus1", "populus", "N", gen="m."), E("populus2", "populus", "N", gen="f."),
      E("rex1", "rex", "N", gen="m."), E("Rex2", "rex", "N", gen="m.")]
ix = B.indexes(fx)
ok(B.link("malus", "ADJ", *ix) == ("class", ["malus1"]), "class picks the one adjective among three malus")
ok(B.link("malus", "N", *ix)[0] == "ambiguous", "two nouns malus stay ambiguous, both listed")
ok(B.link("sum", "V", *ix) == ("headword", ["sum1"]), "a pointer entry and an affix (sum-) never take sum")
ok(B.link("rursum", "ADV", *ix) == ("spelling", ["rursus"]), "rursum is found as a spelling printed under rursus")
ok(B.link("domino", "V", *ix) == ("voice", ["dominor"]), "WORDS's domino reaches L&S's deponent dominor")
ok(B.link("cum", "CONJ", *ix) == ("class", ["cum2"]), "cum the conjunction is cum2")
ok(B.link("qui", "PRON", *ix) == ("class", ["qui1"]), "qui the pronoun: the one entry printing no other class")
ok(B.link("x", "N", *ix) == ("headword", ["x1"]), "an entry L&S marks spurious never takes a word")
ok(B.link("nemo", "N", *ix) == ("none", []), "no entry: none, nothing guessed")
ok(B.link("x", "V", *ix) == ("clash", []), "a verb whose only entry is a noun: clash, not linked")
ok(B.link("populus", "N", *ix, gender="F") == ("gender", ["populus2"]), "populus, feminine: the poplar (populus2)")
ok(B.link("rex", "N", *ix, gender="M", proper=False) == ("case", ["rex1"]), "rex, a common noun: rex1, not the name Rex2")


# -- the context rules, on fixtures ------------------------------------------
def R(target, wkey="w", pos="N", case=None, efreq=0, ifreq="A", proper=False, linked=True,
      number=None, gender=None, enclitic=None):
    return {"target": tuple(target), "linked": linked, "wkey": wkey, "pos": pos, "case": case,
            "number": number, "gender": gender, "enclitic": enclitic, "efreq": efreq, "ifreq": ifreq, "iage": "X", "proper": proper}


def T(form, Rs, punct=False, cased=None):
    return {"form": form, "cased": cased or form, "R": Rs, "punct_after": punct}


est = T("est", [R(["edo2"], "edo, esse", "V", efreq=2), R(["sum1"], "sum, esse", "V", efreq=0)])
ok(B.resolve(est, None, None) == ("sum1", ["rare-entry"]), "est: edo (WORDS grade C) loses to sum (A): rare-entry")
ejus = T("ejus", [R(["is"], "is, ea, id", "PRON", "GEN"), R(["idem"], "idem, eadem, idem", "PRON", "GEN")])
ok(B.resolve(ejus, None, None) == ("is", ["idem-dem"]), "ejus is not idem without -dem: idem-dem")
cum = T("cum", [R(["cum1"], "cum PREP", "PREP", "ABL"), R(["cum2"], "cum ADV", "ADV")])
eo = T("eo", [R(["is"], "is", "PRON", "ABL")])
autem = T("autem", [R(["autem"], "autem", "CONJ")])
Iesus = T("jesus", [R(["Jesus"], "Jesus", "N", None, proper=True)], cased="Jesus")
longe = T("longe", [R(["longe"], "longe", "ADV")])
ok(B.resolve(cum, eo, None) == ("cum1", ["prep-object"]), "cum eo: a preposition with its ablative")
ok(B.resolve(cum, autem, None) == ("cum2", ["no-prep-object"]), "cum autem: no object, so the conjunction")
ok(B.resolve(cum, Iesus, None)[0] == "cum1", "a name with no case may be the object")
ok(B.resolve(cum, longe, None) == (None, []), "a preposition can take an adverb (a longe): left null")
ok(B.resolve(T("cum", cum["R"], punct=True), autem, None) == ("cum2", ["no-prep-object"]),
   "a clause ending after it: no object")
quis = T("quis", [R(["quis1", "quis2"], "quis, quid", "PRON", "NOM"), R(["qui1"], "qui, quae, quod", "PRON", "NOM")])
ok(B.resolve(quis, None, "si") == ("quis2", ["si-quis"]), "si quis: the indefinite (quis2)")
ok(B.resolve(quis, None, "nisi") == (None, []), "nisi qui(s) may be relative: left null")
panes = T("panes", [R(["panis"], "panis", "N", "NOM"), R(["Pan"], "Pan", "N", "NOM")])
ok(B.resolve(panes, None, None) == ("panis", ["proper-lower"]), "panes, lower-case: bread, not the god Pan")
dominum = T("dominum", [R(["domina"], "domina", "N", "GEN", ifreq="C"), R(["dominus"], "dominus", "N", "ACC")])
ok(B.resolve(dominum, None, None) == ("dominus", ["rare-inflection"]),
   "dominum as domina's genitive plural is an ending WORDS grades C: rare-inflection")
salutare = T("salutare", [R(["saluto"], "saluto", "V", efreq=0),
                           R(["salutaris"], "salutaris", "N", "ACC", efreq=2, number="S", gender="N")])
tuum = T("tuum", [R(["tuus"], "tuus", "ADJ", "ACC", number="S", gender="N"),
                  R(["tuus"], "tuus", "ADJ", "ACC", number="S", gender="M")])
ok(B.resolve(salutare, tuum, None) == ("salutaris", ["possessive-agrees"]),
   "salutare tuum: a noun agreeing with tuum, not the verb (possessive-agrees, before rare-entry)")
peccata = T("peccata", [R(["peccatum"], "peccatum", "N", "NOM", efreq=0),
                        R(["pecco"], "pecco", "VPAR", "NOM", efreq=2)])
ok(B.resolve(T("peccata", peccata["R"]), None, None) == (None, []),
   "frequency never swaps a noun for a verb of its stem: peccata stays null, not pecco")
absque = T("absque", [R(["abs"], "abs", "PREP", "ABL", enclitic="que"), R(["absque1"], "absque", "PREP", "ABL", efreq=3)])
ok(B.resolve(absque, None, None) == ("absque1", ["whole-word"]), "absque is the preposition, not abs + -que: whole-word")
cumR = [R(["cum1"], "cum PREP", "PREP", "ABL"), R(["cum2"], "cum ADV", "ADV")]
David = T("david", [R(["David"], "David", "N", None, proper=True)], cased="David")
rescisset = T("rescisset", [R(["rescisco"], "rescisco", "V")])
ok(B.resolve(T("cum", cumR), David, "quod", None, rescisset) == (None, []),
   "Quod cum David rescisset: a name then a verb may be the clause's subject, so cum stays null")
vero = T("vero", [R(["verus"], "verus", "ADJ", "ABL"), R(["vero"], "vero", "ADV")])
ok(B.resolve(T("cum", cumR), vero, "et") == ("cum2", ["no-prep-object"]),
   "cum vero: vero stands second in its clause, so cum opened it: not 'with'")
sanctus = T("sanctus", [R(["sanctus"], "sanctus", "ADJ", "NOM"), R(["sancio"], "sancio", "VPAR", "NOM")])
ok(B.resolve(sanctus, None, None) == (None, []), "adjective or participle, both common: null, never guessed")
ok(B.ls_fold("a^credula") == "acredula" and B.ls_fold("ăd-ōro") == "adoro",
   "Perseus's quantity marks and hyphens fold away")
ok(B.ls_class(None, "f.") == "N" and B.ls_class("v. dep.", None) == "V" and B.ls_class("P. a.", None) == "ADJ",
   "L&S's printed class read in WORDS's terms")

# -- the committed manifest; the CC BY-SA files stay out of git ---------------
man = json.load(open(os.path.join(B.OUT, "manifest.json"), encoding="utf-8"))
rights = man["sources"]["lewis-short"]["rights"]
ok(rights["redistribute_whole"] is False and "CC BY-SA" in rights["license"] and "Perseus" in rights["attribution"],
   "L&S rights block: CC BY-SA, attribution, not redistributed whole")
ok(set(man["files"]) == set(B.LOCAL_FILES) and "gitignored" in man["files_dir"],
   "the manifest lists every built file and says where they live (gitignored)")
tracked = subprocess.run(["git", "ls-files", "data/lemmas/latin-key", "build/latin-key"], cwd=ROOT,
                         capture_output=True, text=True).stdout.split()
if os.path.exists(os.path.join(ROOT, ".git")):   # a file in a worktree
    ok(tracked == ["data/lemmas/latin-key/manifest.json", "data/lemmas/latin-key/manifest.json.prov.md"],
       "git tracks only the manifest: nothing derived from Lewis & Short is committed")
else:
    print("skip  git tracking check: not a git checkout")

missing = {n for n in man["files"] if not os.path.exists(os.path.join(B.LOCAL, n))}
for n in sorted(missing):
    print(f"skip  {n}: not in build/latin-key (python3 pipeline/build_latin_key.py)")
if missing - {"strongs-latin.jsonl"}:       # strongs-latin also needs the local KJV tags
    end_to_end()
for name, meta in man["files"].items():
    if name in missing:
        continue
    with open(os.path.join(B.LOCAL, name), "rb") as f:
        blob = f.read()
    ok(hashlib.sha256(blob).hexdigest() == meta["sha256"] and blob.count(b"\n") == meta["rows"],
       f"{name}: sha256 and row count are the manifest's")

ls = rows("lewis-short.jsonl")
LS_FIELDS = {"key", "citation", "perseus_id", "homograph", "type", "headword", "spellings",
             "class", "class_by", "gen", "pointer", "points_to"}
ok(len(ls) == man["counts"]["lewis_short_entries"] == 51645, "51,645 L&S entries")
ok(all(set(r) == LS_FIELDS for r in ls), "L&S rows carry pointers and facts only, never definition text")
ok(all(r["citation"] == "lewis-short:" + r["key"] for r in ls), "every citation is lewis-short:<key>")
keys = {r["key"] for r in ls}
ok(len(keys) == len(ls), "L&S keys are unique")
by = {r["key"]: r for r in ls}
ok(by["super10"]["headword"] == "superfio", "headword is the printed spelling, not the key (super10 = super-fio)")

wl = rows("whitaker-ls.jsonl")
ok(all(set(r["ls"]) <= keys for r in wl), "every Whitaker link names a real L&S key")
ok(all((r["status"] in ("none", "clash")) == (not r["ls"]) for r in wl), "a lemma has keys exactly when it is linked")
ok(all(len(r["ls"]) == 1 for r in wl if r["status"] in B.LINKED), "a linked lemma names one entry")
W_ = {r["whitaker"]: r for r in wl}
ok(W_.get("verbum, verbi  N (2nd) N", {}).get("ls") == ["verbum"], "verbum -> lewis-short:verbum")
ok(W_["vis  V  (UNIQUES)"]["status"] == "clash" and not W_["vis  V  (UNIQUES)"]["ls"],
   "vis, 'you want', is not linked to L&S's vis, 'force'")
ok(W_["canto, cantonis  N (3rd) M"]["status"] == "clash", "canto, cantonis (a noun) is not canto, to sing")
ok(by["miror"]["class"] == "V" and by["miror"]["gen"] is None and by["abstineo"]["class"] == "V",
   "L&S's v. n. (an intransitive verb) is not read as a neuter noun: miror, abstineo are verbs")

forms = {r["form"]: r for r in rows("vulgate-forms.jsonl")}
ok(sum(r["tokens"] for r in forms.values()) == 612029, "every running word of the Vulgate is counted (612,029)")
ok(forms["deus"]["status"] == "sure" and forms["deus"]["ls"] == ["deus"], "deus is sure: lewis-short:deus")
ok(forms["est"]["status"] == "several" and {"sum1", "edo2"} <= set(forms["est"]["ls"]),
   "est stays several: sum and edo (to eat), never chosen")
ok(all(set(r["ls"]) <= keys for r in forms.values()), "every form names real L&S keys")
ok(forms["vis"]["status"] == "several" and forms["vis"]["unresolved"] == forms["vis"]["tokens"],
   "the form vis stays several (force, or you want): never sure")

conc = {r["key"]: r for r in rows("vulgate-concordance.jsonl")}
ok(set(conc) <= keys, "every concordance key is an L&S key")
ok("John.1.1" in conc["verbum"]["sure"], "In principio erat Verbum: John 1:1 is under verbum, sure")
ok("Ps.22.1" in conc["dominus"]["sure"], "Dominus regit me: Vulgate Ps 22:1 is under dominus")
ok(all(not (set(r["sure"]) & set(r["possible"])) for r in conc.values()),
   "a verse is sure or possible for a key, never both")
ok(all(set(rule.split("+")) <= set(B.RULES) for r in conc.values() for rule in r["resolved"]),
   "every resolution names its rules, and only known rule ids")
ok("Gen.3.8" in conc["cum2"]["resolved"].get("no-prep-object", []), "Gen 3:8 et cum audissent: cum2, no-prep-object")
ok("John.1.1" in conc["sum1"]["sure"] and "John.1.1" in conc["principium"]["possible"],
   "John 1:1: erat sure as sum1; principio (noun, or the verb principio) left possible, never settled by frequency")
out = man["counts"]["vulgate_tokens_by_outcome"]
ok(sum(out.values()) == 612029 and out["unresolved"] < 0.21 * 612029,
   f"unresolved words {out['unresolved']} ({100 * out['unresolved'] / 612029:.1f}%), under 21%")
kind = man["counts"]["vulgate_tokens_resolved_by_kind"]
ok(sum(kind.values()) == out["resolved"], "every resolved word is counted as grammar or prior-only, apart")
ok(forms["peccata"]["resolved"].get("rare-entry") is None and forms["tribus"]["resolved"].get("rare-entry") is None,
   "peccata and tribus are never settled by frequency (pecco, tres)")
ok(forms["absque"]["resolved"] == {"whole-word": forms["absque"]["tokens"]}, "every absque is the preposition absque")
ok(forms["septimo"]["ls"] == ["septimus"], "septimo is septimus, the ordinal, not septem")
ok(forms["caelos"]["ls"] == ["caelum2"], "caelos is caelum2 (heaven): the pointer caelus, 'v. caelum', is followed")
ok(forms["humiliter"]["ls"] == ["humiliter"], "humiliter: a pointer to an adjective is not followed for an adverb")
ok("1Sam.23.9" not in str(conc["cum1"]["resolved"]), "1 Sam 23:9 Quod cum David rescisset: not cum 'with'")
for f in sorted(B.OWN_LEMMA_STANDS):
    ok(not forms[f]["resolved"].get("rare-entry"), f"{f} is never forced off its own lemma by frequency")
ok(forms["populus"]["unresolved"] == 0 and forms["populus"]["resolved"].get("rare-entry", 0) > 400,
   "populus is the people (populus1), not the poplar: the own-lemma list is a list, not a rule")
ok(forms["omne"]["unresolved"] == 0 and forms["omne"]["ls"] == ["omnis"], "omne is omnis, every time")

# -- Strong's -> the Vulgate's Latin -------------------------------------------
if "strongs-latin.jsonl" in missing:
    end_to_end()
eq = {r["strongs"]: r for r in rows("strongs-latin.jsonl")}
first = {k: r["latin"][0]["ls"] for k, r in eq.items()}
for num, word in (("G26", "caritas"), ("G25", "diligo"), ("H2617", "misericordia"), ("H3068", "dominus"),
                  ("G1577", "ecclesia"), ("G1680", "spes"), ("H7307", "spiritus")):
    ok(first.get(num) == word, f"{num}: the Vulgate's first word for it is {word}")
ok([x["ls"] for x in eq["G26"]["latin"]] == ["caritas", "dilectio"], "agape: caritas, then dilectio, nothing else")
rule = man["counts"]["strongs_latin"]["rule"]
ok(all(x["verses"] >= rule["min_verses"] and x["dice"] >= rule["min_dice"] for r in eq.values() for x in r["latin"]),
   "every pair is seen in 3+ verses with Dice 0.1+")
ok(all(r["latin"] == sorted(r["latin"], key=lambda x: -x["dice"]) and len(r["latin"]) <= rule["max"]
       for r in eq.values()), "each number's words are ranked by score, at most five")
ok(all(set(x["ls"] for x in r["latin"]) <= keys for r in eq.values()), "every Latin word is an L&S key")
ok(all((r["evidence"] == "thin") == (r["verses"] < rule["thin_below"]) for r in eq.values()),
   "a number seen in fewer than 10 KJV verses is marked thin")

end_to_end()
