#!/usr/bin/env python3
"""
whitaker_tricks_test.py -- WORDS's SYNCOPE, SLURY, FIXES and TRICKS as ported
in pipeline/whitaker_tricks.py: one check per ported rule.

Run:  python3 tests/whitaker_tricks_test.py

WHAT IT ASSERTS
    OFFLINE (always runs; a stand-in dictionary that knows a few words)
    1. Every row of every trick table fires, in each direction it has, and
       writes what the Ada writes; a SLUR does not fire before a vowel.
    2. The five syncope rules, and which of them need the perfect system.
    3. The procedures: eo's is -> iis, Adj_Terminal_Iis, Double_Consonants,
       Two_Words (with Common_Prefix and the compound-number trim), the
       table-before-Any_Tricks order, first-rule-wins, SLURY's if/elsif
       FLIP_FLOP against TRICKS's if/if.
    4. The order of attempts (parse.adb): a plain parse stops everything but
       syncope and -que; SLURY only when plain fails; no syncope beside a
       form of esse; TRICKS only when nothing else, then on the form less an
       enclitic.
    AGAINST THE WHITAKER FILES (when fetched; says so when not)
    5. The Python tables are the Ada tables, row for row, in order
       (words_engine-trick_tables.ads/.adb at the pinned commit).
    6. Real words through each mechanism, prefixes and suffixes included.
    7. On the hymns: the rules never take a plain analysis away, and they
       recover medieval respellings of hymn forms (measured 2026-09-26).
"""
import importlib.util
import json
import os
import re
import sys

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
T = load("whitaker_tricks")

PASS = 0
FAIL = []


def check(label, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label + (("  " + str(detail)) if detail else ""))


# ================================================================ OFFLINE
class Fake:
    """Knows exactly the words it is given. `plain` is Word without fixes."""
    tackons = ["que", "ne", "ve", "est"]
    stem_index = {}
    prefixes, suffixes = [], []

    def __init__(self, known):
        self.known = {W.fold(k): v for k, v in known.items()}

    def plain(self, w):
        return [dict(a, parse=dict(a["parse"])) for a in self.known.get(W.fold(w), [])]

    def cuts(self, w):
        return []


N = {"entry": 0, "parse": {"pos": "N", "decl": [2, 1]}}
PERF = {"entry": 1, "parse": {"pos": "V", "decl": [1, 1]}, "stem_key": 3}
PRES = {"entry": 1, "parse": {"pos": "V", "decl": [1, 1]}, "stem_key": 1}


def tword_of(X):
    return lambda t: X.plain(t)


def via0(r):
    return r[0]["via"][0] if r and r[0].get("via") else {}


print("--- 1. every table row fires, as the Ada writes it")
TAIL = "grkr"          # no trick's pattern contains g, r or k
tables = [("TRICK", T.TABLE_NAMES[c], rows, False) for c, rows in T.TRICKS.items()] + \
         [("TRICK", "Any_Tricks", T.ANY_TRICKS, False), ("TRICK", "Mediaeval_Tricks", T.MEDIAEVAL_TRICKS, False)] + \
         [("SLURY", T.SLUR_TABLE_NAMES[c], rows, True) for c, rows in T.SLUR_TRICKS.items()]
bad = []
n_rows = 0
for kind, name, rows, excl in tables:
    for op, x1, x2, mx in rows:
        n_rows += 1
        f1, f2 = W.fold(x1), W.fold(x2 or "")
        cases = []
        if op == T.FLIP:
            cases = [(f1 + TAIL, f2 + TAIL)]
        elif op == T.FF:
            cases = [(f1 + TAIL, f2 + TAIL), (f2 + TAIL, f1 + TAIL)]
        elif op == T.INTERNAL:
            cases = [("gr" + f1 + "kr", "gr" + f2 + "kr")]
        else:
            cases = [(f1 + "t" + TAIL, f1[:-1] + "tt" + TAIL)]
        for given, want in cases:
            X = Fake({want: [N]})
            r = T._iter(tword_of(X), given, [(op, x1, x2, mx)], kind, name, excl)
            v = via0(r)
            if not r or v.get("as") != want or v.get("kind") != kind or v.get("table") != name:
                bad.append((name, op, x1, x2, given))
check(f"all {n_rows} table rows rewrite the form as the Ada does, each direction", not bad, bad[:4])
X = Fake({"attrkr": [N]})
check("SLUR does not fire before a vowel (ad + vowel is left alone)",
      not T._slur(tword_of(X), "adakr", "ad", "A_Slur_Tricks")
      and T._slur(tword_of(X), "adtrkr", "ad", "A_Slur_Tricks"))
X = Fake({"esgrkr": [N]})
r1 = T._flip_flop(tword_of(X), "essgrkr", "es", "ess", "TRICK", "E_Tricks", False)
r2 = T._flip_flop(tword_of(X), "essgrkr", "es", "ess", "SLURY", "E_Tricks", True)
check("FLIP_FLOP: TRICKS tries the reverse after a failed match (if/if), SLURY does not (if/elsif)",
      r1 and via0(r1)["as"] == "esgrkr" and r2 == [])
check("a FLIP needs two letters beyond the pattern (S'Length >= X1'Length + 2)",
      not T._flip(tword_of(Fake({"aek": [N]})), "ek", "e", "ae", "TRICK", "E_Tricks")
      and T._flip(tword_of(Fake({"aekk": [N]})), "ekk", "e", "ae", "TRICK", "E_Tricks"))
X = Fake({"grbkrbk": [N], "grbkrpk": [N]})
r = T._internal(tword_of(X), "grpkrpk", "p", "b", "Mediaeval_Tricks")
check("INTERNAL rewrites one occurrence at a time, leftmost first", via0(r).get("as") == "grbkrpk")

print("\n--- 2. syncope")
cases = [("ii => ivi", "audiit", "audiuit"), ("s => vis", "amasti", "amauisti"),
         ("r => v.r", "amarunt", "amauerunt"), ("ier => iver", "audierunt", "audiuerunt"),
         ("s/x => +is", "dixti", "dixisti")]
for rule, form, full in cases:
    r = T.syncope(Fake({full: [PERF]}), form)
    check(f"syncope {rule}: {form} is read as {full}",
          r and via0(r)["kind"] == "SYNCOPE" and via0(r)["rule"] == rule and via0(r)["as"] == full)
need = [(rule, form, full) for rule, form, full in cases if rule != "s => vis"]
check("four of the five rules keep a hit only in the perfect system (stem key 3)",
      all(T.syncope(Fake({full: [PRES]}), form) == [] for _, form, full in need))
check("'s => vis' keeps its hit even outside the perfect system (the Ada returns on any hit)",
      T.syncope(Fake({"amauisti": [PRES]}), "amasti") != [])
check("syncope walks from the right: the last 'ii' is tried first",
      via0(T.syncope(Fake({"iiiuit": [PERF], "iuiit": [PERF]}), "iiiit")).get("as") == "iiiuit")

print("\n--- 3. the TRICKS procedures")
EO = {"entry": 2, "parse": {"pos": "V", "decl": [6, 1]}}
check("eo: an initial 'is' is tried as 'iis', kept only for eo (V 6 1)",
      via0(T.tricks(Fake({"iisset": [EO]}), "isset")).get("rule") == "is => iis"
      and T.tricks(Fake({"iisset": [N]}), "isset") == [])
ADJ = lambda case: {"entry": 3, "parse": {"pos": "ADJ", "decl": [1, 1], "case": case, "number": "P"}}
check("Adj_Terminal_Iis: -is read as -iis, only for ADJ 1 1 DAT/ABL P",
      via0(T.tricks(Fake({"impiis": [ADJ("DAT")]}), "impis")).get("table") == "Adj_Terminal_Iis"
      and T.tricks(Fake({"impiis": [ADJ("NOM")]}), "impis") == [])
check("Double_Consonants: a single consonant between vowels is tried doubled",
      via0(T.tricks(Fake({"sabbatum": [N]}), "sabatum")).get("rule") == "b -> bb")
tw = T._two_words(Fake({"me": [N], "ipsum": [N]}), "meipsum")
check("Two_Words: first half, then the rest; both halves tagged with the split",
      [a["via"][0]["part"] for a in tw] == [1, 2] and {a["via"][0]["as"] for a in tw} == {"me+ipsum"})
check("Two_Words moves on when a first half leaves no second word (mei+psum fails; meip+sum)",
      {a["via"][0]["as"] for a in T._two_words(Fake({"mei": [N], "meip": [N], "sum": [N]}), "meipsum")}
      == {"meip+sum"})
check("Two_Words never splits off a Common_Prefix (in, per, sub ...)",
      T._two_words(Fake({"in": [N], "credo": [N]}), "incredo") == [])
check("Two_Words skips forms under five letters", T._two_words(Fake({"ab": [N], "ab": [N]}), "abab") == [])
NUM = {"entry": 4, "parse": {"pos": "NUM"}}
tw = T._two_words(Fake({"duo": [NUM, N], "decem": [NUM]}), "duodecem")
check("Two_Words: two numbers make a compound number, and only the NUM readings stay",
      tw and all(a["parse"]["pos"] == "NUM" for a in tw))
check("the first letter's table is tried before Any_Tricks",
      via0(T.tricks(Fake({"aegrkae": [N], "egrke": [N]}), "egrkae")).get("table") == "E_Tricks")
check("first rule that parses wins: nothing later in the table is tried",
      len(T.tricks(Fake({"aelgrk": [N], "helgrk": [N]}), "elgrk")) == 1)
check("Double_Consonants does not stop Two_Words (the Ada runs both)",
      {a["via"][0]["kind"] for a in T.tricks(Fake({"sabbatum": [N], "sab": [N], "atum": [N]}), "sabatum")}
      == {"TRICK", "TWO_WORDS"})

print("\n--- 4. the order of attempts")
check("a plain parse is taken, and no trick is tried",
      [a.get("via") for a in T.parse_latin_word(Fake({"celum": [N], "caelum": [N]}), "celum")] == [None])
check("SLURY is tried only when the plain parse fails",
      via0(T.parse_latin_word(Fake({"committo": [N]}), "comitto")).get("kind") == "SLURY")
ESSE = {"entry": 5, "parse": {"pos": "V", "decl": [5, 1]}}
check("no syncope beside a form of esse",
      T.parse_latin_word(Fake({"isti": [ESSE], "iuisti": [PERF]}), "isti") == [dict(ESSE, parse=dict(ESSE["parse"]))])
check("syncope runs beside a plain parse (WORDS's 'Pure SYNCOPE')",
      len(T.parse_latin_word(Fake({"moras": [N], "moueras": [PERF]}), "moras")) == 2)
r = T.parse_latin_word(Fake({"praeclarus": [N]}), "preclarusque")
check("TRICKS on the form less an enclitic, last of all (Tricks_Enclitic)",
      r and r[0]["enclitic"] == "que" and via0(r)["rule"] == "flip_flop pre/prae")
check("an unknown stays unknown", T.parse_latin_word(Fake({}), "qqqqqq") == [])

# ======================================================= AGAINST THE FILES
print("\n--- against the Whitaker files")
if not W.have_cache():
    print("skip  the Whitaker files are not fetched (python3 pipeline/build_lemma_spine.py --fetch)")
else:
    if not W.have_ada():
        print("skip  the pinned Ada source is not fetched; tables not compared")
    else:
        print("--- 5. the tables are the Ada's")
        ada = os.path.join(W.CACHE, "ada")
        text = open(os.path.join(ada, "words_engine-trick_tables.adb"), encoding="latin-1").read() + \
            open(os.path.join(ada, "words_engine-trick_tables.ads"), encoding="latin-1").read()
        text = re.sub(r"--[^\n]*", "", text)
        row = re.compile(r'\(\s*(?:1\s*=>\s*)?\(?Max\s*=>\s*(\d),\s*Op\s*=>\s*TC_(\w+),\s*'
                         r'(?:FF1|FF3|I1|S1)\s*=>\s*\+"(\w*)"(?:,\s*(?:FF2|FF4|I2)\s*=>\s*\+"(\w*)")?')
        OPS = {"Flip_Flop": T.FF, "Flip": T.FLIP, "Internal": T.INTERNAL, "Slur": T.SLUR}

        def ada_table(name):
            m = re.search(name + r"\s*:\s*constant TricksT\s*:=\s*(.*?)\);\s*\n", text, re.S)
            return [(OPS[o], a, (b if o != "Slur" else None), int(mx))
                    for mx, o, a, b in row.findall(m.group(1))] if m else None

        mism = []
        for c, rows in T.TRICKS.items():
            if ada_table(T.TABLE_NAMES[c]) != rows:
                mism.append(T.TABLE_NAMES[c])
        for c, rows in T.SLUR_TRICKS.items():
            if ada_table(T.SLUR_TABLE_NAMES[c]) != rows:
                mism.append(T.SLUR_TABLE_NAMES[c])
        for name, rows in (("Any_Tricks", T.ANY_TRICKS), ("Mediaeval_Tricks", T.MEDIAEVAL_TRICKS)):
            if ada_table(name) != rows:
                mism.append(name)
        check("every trick table is the Ada's, row for row, in order", not mism, mism)
        letters = re.findall(r"when '(\w)' =>\s*return (\w)_Tricks;", text)
        check("the first-letter dispatch covers exactly the Ada's letters",
              sorted(c for c, _ in letters) == sorted(T.TRICKS))
        slur_letters = re.findall(r"when '(\w)' =>\s*return (\w)_Slur_Tricks;", text)
        check("the SLURY dispatch covers exactly the Ada's letters",
              sorted(c for c, _ in slur_letters) == sorted(T.SLUR_TRICKS))
        cp = re.search(r"Common_Prefixes : constant Strings := \((.*?)\);", text, re.S)
        check("Common_Prefix is the Ada's list", tuple(re.findall(r'"(\w+)"', cp.group(1))) == T.COMMON_PREFIXES)

    print("\n--- 6. real words, each mechanism")
    X = W.Whitaker()

    def reached(form, head, kind, detail=None, enclitic=None):
        for a in X.analyze(form):
            kinds = [v["kind"] for v in a["via"]]
            if a["headword"] == head and kind in kinds and (enclitic is None or a["enclitic"] == enclitic):
                v = a["via"][kinds.index(kind)]
                if detail is None or detail in (v.get("rule"), v.get("fix"), v.get("table")):
                    return True
        return False

    for form, head, kind, det in [
        ("audiit", "audio", "SYNCOPE", "ii => ivi"), ("amasti", "amo", "SYNCOPE", "s => vis"),
        ("amarunt", "amo", "SYNCOPE", "r => v.r"), ("audierunt", "audio", "SYNCOPE", "ier => iver"),
        ("dixti", "dico", "SYNCOPE", "s/x => +is"),
        ("obpono", "oppono", "SLURY", "slur ob/o~"), ("subpono", "suppono", "SLURY", "slur sub/su~"),
        ("comloco", "conloco", "SLURY", "flip_flop com/con"), ("comitto", "committo", "SLURY", "flip co/com"),
        ("superbenedictus", "benedictus", "PREFIX", "super"), ("condulcesco", "dulcesco", "PREFIX", "con"),
        ("inamabiliter", "inamabilis", "SUFFIX", "iter"),
        ("preclarus", "praeclarus", "TRICK", "P_Tricks"), ("ecfero", "effero", "TRICK", "E_Tricks"),
        ("ymbrem", "imber", "TRICK", "Y_Tricks"),
        ("cene", "cena", "TRICK", "internal e/ae"), ("peticio", "petitio", "TRICK", "internal ci/ti"),
        ("catedra", "cathedra", "TRICK", "internal t/th"),
        ("impis", "impius", "TRICK", "Adj_Terminal_Iis"), ("isset", "eo", "SYNCOPE", "s => vis"),
        ("sabatum", "sabbatum", "TRICK", "Double_Consonants"), ("ocasio", "occasio", "TRICK", "Double_Consonants"),
        ("meipsum", "ipse", "TWO_WORDS", None),
    ]:
        check(f"{form}: {head} via {kind} {det or ''}".rstrip(), reached(form, head, kind, det))
    check("superlaudabiliter: a prefix and a suffix together (super- + laudabilis + -iter)",
          any([v["kind"] for v in a["via"]] == ["PREFIX", "SUFFIX"] and a["headword"] == "laudabilis"
              for a in X.analyze("superlaudabiliter")))
    check("preclarusque: tricks on the form less -que", reached("preclarusque", "praeclarus", "TRICK", enclitic="que"))
    check("a double trick is out of reach, as in WORDS (leticia needs ae and ti)",
          not any(a["headword"] == "laetitia" for a in X.analyze("leticia")))
    check("every rule-reached analysis names its rule; a plain one has none",
          all(isinstance(a["via"], list) for a in X.analyze("moras"))
          and any(not a["via"] for a in X.analyze("moras")))

    print("\n--- 7. on the hymns")
    rows = [json.loads(l) for l in open(os.path.join(REPO, "data", "lemmas", "whitaker-la",
                                                     "hymns.analyses.jsonl"), encoding="utf-8")]
    lost = []
    for r in rows:
        plain = {(a.get("entry"), repr(sorted(a["parse"].items())), a.get("enclitic"))
                 for a in T.parse_plain(X, r["form"])}
        now = {(a.get("entry"), repr(sorted(a["parse"].items())), a.get("enclitic"))
               for a in T.parse_latin_word(X, r["form"])}
        if plain - now:
            lost.append(r["form"])
    check("no hymn form loses a plain analysis to the rules", not lost, lost[:5])

    def respell(w):
        out = {}
        if "ae" in w:
            out["ae>e"] = w.replace("ae", "e")
        if "oe" in w:
            out["oe>e"] = w.replace("oe", "e")
        if re.search(r"ti(?=[aeiou])", w[1:]):
            out["ti>ci"] = w[0] + re.sub(r"ti(?=[aeiou])", "ci", w[1:])
        m = re.search(r"([bcdfglmnprst])\1", w)
        if m:
            out["double>single"] = w[:m.start()] + w[m.start() + 1:]
        return out

    n = before = after = 0
    for r in rows:
        heads = {a["headword"] for a in r["analyses"] if not a.get("via")}
        for t in respell(r["form"]).values():
            n += 1
            b = {W.headword_of(X.form(a["entry"])[0]) if a["entry"] is not None else W.fold(a["unique"]["word"])
                 for a in T.parse_plain(X, t)}
            A = {a["headword"] for a in X.analyze(t) if "TWO_WORDS" not in {v["kind"] for v in a["via"]}}
            before += bool(heads & b)
            after += bool(heads & A)
    # measured 2026-09-26: 30 respellings; 3 recovered before the port, 22 after
    check("medieval respellings of hymn forms (ae>e, oe>e, ti>ci, doubled>single): 3 -> 22 of 30",
          (n, before, after) == (30, 3, 22), (n, before, after))

print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
