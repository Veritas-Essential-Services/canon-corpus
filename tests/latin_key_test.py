#!/usr/bin/env python3
# prov: 2026-10-02 claude-opus-5-5 drafted
# fable_review: pending
"""
latin_key_test.py -- the Latin key (data/lemmas/latin-key/): Lewis & Short's
entries, Whitaker's lemmas linked to them, and the Vulgate's words.

    python3 tests/latin_key_test.py

Runs offline on the committed files. The linking rules are tested on inline
fixtures; --check runs only when the sources are in data/corpus/.
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
    with open(os.path.join(B.OUT, name), encoding="utf-8") as f:
        return [json.loads(l) for l in f]


# -- the linking rules, on fixtures -------------------------------------------
def E(key, hw, cls=None, pointer=False, spellings=(), typ="main"):
    return {"key": key, "headword": hw, "class": cls, "pointer": pointer,
            "spellings": list(spellings), "type": typ}


fx = [E("malus1", "malus", "ADJ"), E("malus2", "malus", "N"), E("malus3", "malus", "N"),
      E("sum1", "sum"), E("sum2", "sum", pointer=True), E("sum3", "sum-"),
      E("rursus", "rursus", "ADV", spellings=["rursum"]), E("dominor", "dominor", "V"),
      E("cum1", "cum", "PREP"), E("cum2", "cum", "CONJ"), E("qui1", "qui"), E("qui2", "qui", "ADV"),
      E("x1", "x", "N"), E("x2", "x", "N", typ="spur")]
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
ok(B.ls_fold("a^credula") == "acredula" and B.ls_fold("ăd-ōro") == "adoro",
   "Perseus's quantity marks and hyphens fold away")
ok(B.ls_class(None, "f.") == "N" and B.ls_class("v. dep.", None) == "V" and B.ls_class("P. a.", None) == "ADJ",
   "L&S's printed class read in WORDS's terms")

# -- the committed files -----------------------------------------------------
man = json.load(open(os.path.join(B.OUT, "manifest.json"), encoding="utf-8"))
for name, meta in man["files"].items():
    with open(os.path.join(B.OUT, name), "rb") as f:
        blob = f.read()
    ok(hashlib.sha256(blob).hexdigest() == meta["sha256"] and blob.count(b"\n") == meta["rows"],
       f"{name}: sha256 and row count are the manifest's")
rights = man["sources"]["lewis-short"]["rights"]
ok(rights["redistribute_whole"] is False and "CC BY-SA" in rights["license"] and "Perseus" in rights["attribution"],
   "L&S rights block: CC BY-SA, attribution, not redistributed whole")

ls = rows("lewis-short.jsonl")
LS_FIELDS = {"key", "citation", "perseus_id", "homograph", "type", "headword", "spellings",
             "class", "class_by", "pointer"}
ok(len(ls) == man["counts"]["lewis_short_entries"] == 51645, "51,645 L&S entries")
ok(all(set(r) == LS_FIELDS for r in ls), "L&S rows carry pointers and facts only, never definition text")
ok(all(r["citation"] == "lewis-short:" + r["key"] for r in ls), "every citation is lewis-short:<key>")
keys = {r["key"] for r in ls}
ok(len(keys) == len(ls), "L&S keys are unique")
by = {r["key"]: r for r in ls}
ok(by["super10"]["headword"] == "superfio", "headword is the printed spelling, not the key (super10 = super-fio)")

wl = rows("whitaker-ls.jsonl")
ok(all(set(r["ls"]) <= keys for r in wl), "every Whitaker link names a real L&S key")
ok(all((r["status"] == "none") == (not r["ls"]) for r in wl), "a lemma has keys exactly when it is linked")
ok(all(len(r["ls"]) == 1 for r in wl if r["status"] in B.LINKED), "a linked lemma names one entry")
W_ = {r["whitaker"]: r for r in wl}
ok(W_.get("verbum, verbi  N (2nd) N", {}).get("ls") == ["verbum"], "verbum -> lewis-short:verbum")

forms = {r["form"]: r for r in rows("vulgate-forms.jsonl")}
ok(sum(r["tokens"] for r in forms.values()) == 612029, "every running word of the Vulgate is counted (612,029)")
ok(forms["deus"]["status"] == "sure" and forms["deus"]["ls"] == ["deus"], "deus is sure: lewis-short:deus")
ok(forms["est"]["status"] == "several" and {"sum1", "edo2"} <= set(forms["est"]["ls"]),
   "est stays several: sum and edo (to eat), never chosen")
ok(all(set(r["ls"]) <= keys for r in forms.values()), "every form names real L&S keys")

conc = {r["key"]: r for r in rows("vulgate-concordance.jsonl")}
ok(set(conc) <= keys, "every concordance key is an L&S key")
ok("John.1.1" in conc["verbum"]["sure"], "In principio erat Verbum: John 1:1 is under verbum, sure")
ok("Ps.22.1" in conc["dominus"]["sure"], "Dominus regit me: Vulgate Ps 22:1 is under dominus")
ok(all(not (set(r["sure"]) & set(r["possible"])) for r in conc.values()),
   "a verse is sure or possible for a key, never both")

# -- the build, end to end ---------------------------------------------------
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
