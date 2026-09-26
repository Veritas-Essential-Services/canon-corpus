#!/usr/bin/env python3
"""
nt_corpus_test.py -- the validator for data/nt/*.jsonl (launch plan D2-D5,
the Greek half). Pilot: John 1:1-18 from the Robinson-Pierpont text.

Run:  python3 tests/nt_corpus_test.py

TWO HALVES, as in hymn_corpus_test.py
    OFFLINE (always runs): the four committed JSONL files and their manifest
    against pipeline/README-nt-jsonl.md -- every record keyed by an EXISTING
    verse uid, every token carrying its eight fields, the licence gate held
    (PD or own only, with the evidence recorded), nothing from MorphGNT,
    SBLGNT or Perseus, and a frozen registry replay minting zero. Also the
    transliteration scheme and the parsing grammar, on fixtures.

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


def jsonl(name):
    with open(os.path.join(DATA, name + ".jsonl"), encoding="utf-8") as f:
        return [json.loads(line) for line in f]


# Measured 2026-09-26 from RP2018 (byztxt v3.3.2). Not estimated.
EXPECTED = {"verses": 18, "tokens": 253, "witnesses": 18, "alignments": 18,
            "distinct_lemmas": 83, "finite_verbs": 41, "flagged": 1}
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
check("row unit is the verse", manifest.get("row_unit") == "verse")

print("\n--- shape")
check("verse count", len(passages) == EXPECTED["verses"], len(passages))
check("token count", len(tokens) == EXPECTED["tokens"], len(tokens))
check("witness count", len(witnesses) == EXPECTED["witnesses"], len(witnesses))
check("alignment count", len(alignments) == EXPECTED["alignments"], len(alignments))
check("manifest counts agree with the files",
      manifest["counts"]["tokens"] == len(tokens) and manifest["counts"]["passages"] == len(passages)
      and manifest["counts"]["distinct_lemmas"] == EXPECTED["distinct_lemmas"]
      and manifest["counts"]["finite_verbs"] == EXPECTED["finite_verbs"], manifest["counts"])
check("every passage is a verse", all(p["unit"] == "verse" and p["kind"] == "passage" for p in passages))
sel = manifest["selection"]
check("the verses are the selection, in order, with no gap",
      [p["verse"] for p in passages] == list(range(sel["first"], sel["last"] + 1))
      and all(p["chapter"] == sel["chapter"] for p in passages))

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
check("language lives on the witness: lang grc, textform byzantine",
      all(w["lang"] == "grc" and w["textform"] == "byzantine" and w["role"] == "original" for w in witnesses))
check("the Greek is attested text, not generated, and is not the reading of record",
      all(w["text"] and not w["generated"] and w["attested"] == "Y" and w["reading_of_record"] is False
          for w in witnesses))
check("every witness names a source in the manifest",
      all(w["source"] in manifest["sources"] for w in witnesses))
check("paragraph_starts are token positions",
      all(isinstance(w["paragraph_starts"], list) for w in witnesses))


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
check("gloss and plain_form are null: no PD source gives them",
      all(t["gloss"] is None and t["plain_form"] is None for t in tokens))
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
check("every token records where its lemma and parsing came from",
      all(set(t["provenance"]) == {"lemma", "parsing"}
          and t["provenance"]["lemma"]["source"] == "strongs-1890"
          and t["provenance"]["parsing"]["source"] == "rp2018-byztxt" for t in tokens))
flagged = [t for t in tokens if t["review"]]
check("exactly the tokens Robinson parses two ways are flagged (John 1:9)",
      len(flagged) == EXPECTED["flagged"]
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
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    heads = B.load_strongs()
    check("every lemma is Strong's headword for its number",
          all(t["lemma"] == heads[int(t["lemma_key"][1:])] for t in tokens))

    x = open(B._path("strongs", B.STRONGS_XML), encoding="utf-8").read()
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
