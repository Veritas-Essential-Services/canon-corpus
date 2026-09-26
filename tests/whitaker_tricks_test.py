#!/usr/bin/env python3
"""
whitaker_tricks_test.py -- WORDS's SYNCOPE, SLURY, FIXES, TRICKS, Roman
numerals and non-enclitic TACKONs as ported in pipeline/whitaker_tricks.py:
one check per ported rule.

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
    4b. Roman numerals: Roman_Number rule by rule (ones, tens, hundreds,
       thousands; what it refuses), Bad_Roman_Number, the numeral read beside
       a plain parse, from the form as written, and the ill-formed numeral
       replacing Two_Words at the end of TRICKS.
    4c. TACKONs: the sweep by part of speech, the PRON declension test, the
       ADJ that skips all checks, the NOUN quirk, first hit wins, the
       enclitics skipped, and Word less a tackon being Word again.
    AGAINST THE WHITAKER FILES (when fetched; says so when not)
    5. The Python tables are the Ada tables, row for row, in order
       (words_engine-trick_tables.ads/.adb at the pinned commit).
    6. Real words through each mechanism, prefixes and suffixes included.
    7. On the hymns: the rules never take a plain analysis away, and they
       recover medieval respellings of hymn forms (measured 2026-09-26).
    8. The TACKON list is ADDONS.LAT's, the Roman digits are the Ada's, and
       real words through each tackon and numeral.
    9. Stem keys as makedict_main.adb writes them (a one-stem COMP/SUPER
       adjective or adverb, a NUM of one sort) and the adverb's own
       comparison-from-key: found by the Vulgate benchmark, 2026-09-26.
    10. PACKONs and TICKONs (Word's Qu block), also found by the benchmark:
       the list, the n -> m of -dam, the cu- stem, the declension match, the
       meaning-prefix test, when they run, and the house heading.
    4e. (offline) Capitalisation, parse.adb Is_Capitalized: no TRICKS on a
       word written capitalised, and nothing else skipped; the house names
       table consulted for a capitalised form only.
    11. Capitalisation on real words (Hiram, Absalom), and the Ada's test.
    12. The house supplement: every row reads each form it cites,
       `only_forms` adds nothing elsewhere, an `of` row is read as
       Whitaker's lemma with the house row as source, a bad row stops.
    13. PACK headings: the house's by default, the real ones on request.
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

print("\n--- 4b. Roman numerals (roman_numerals_package.adb)")
good = {"I": 1, "III": 3, "IIII": 4, "IV": 4, "V": 5, "VIII": 8, "VIIII": 9, "IX": 9, "XIV": 14,
        "XIX": 19, "XL": 40, "XXXX": 40, "XLIX": 49, "XC": 90, "XCIX": 99, "CX": 110, "CXL": 140,
        "CD": 400, "CCCC": 400, "DC": 600, "CM": 900, "MCM": 1900, "MCMXCIX": 1999, "MMMM": 4000,
        "mdclxvi": 1666}
got = {k: T.roman_number(k) for k in good}
check("Roman_Number: well-formed numerals, either case", got == good,
      {k: v for k, v in got.items() if v != good[k]})
refused = ["IIIII", "IIX", "VX", "IL", "VL", "XCL", "IM", "XXXXX", "CCCCC", "MMMMM", "VV", "LL", "DD", "VIX"]
check("Roman_Number refuses what its comments forbid (IIX, VL, XCL, IM, VIX ...: 0, not a numeral)",
      all(T.roman_number(k) == 0 for k in refused), [k for k in refused if T.roman_number(k)])
check("A_Roman_Digit: M D C L X V I only; U is not a digit, nor any other letter",
      T.only_roman_digits("MdClXvI") and not T.only_roman_digits("xiu") and not T.only_roman_digits("xij"))
bad = {"IIX": 8, "VX": 5, "IL": 49, "MIM": 1999, "IIIII": 5, "XCL": 140}
got = {k: T.bad_roman_number(k) for k in bad}
check("Bad_Roman_Number: the lenient reading (IIX = 8, MIM = 1999)", got == bad, got)
r = T.parse_latin_word(Fake({"ui": [N]}), "ui", raw="vi")
check("a numeral is read first, and plain parsing goes on beside it (vi: 6 and vis)",
      [a["parse"]["pos"] for a in r] == ["NUM", "N"] and r[0]["via"][0]["kind"] == "ROMAN"
      and r[0]["via"][0]["value"] == 6 and r[0]["parse"]["sort"] == "CARD")
check("the numeral is read from the form as written: a search key has lost its v",
      T.parse_latin_word(Fake({}), "xiu") == []
      and T.parse_latin_word(Fake({}), "xiu", raw="xiv")[0]["via"][0]["value"] == 14)
X = Fake({"cil": [N], "xxi": [N]})
check("an ill-formed numeral ends TRICKS and replaces what Two_Words found (Pa_Last := 1)",
      [a["via"][0].get("table") for a in T.tricks(X, "cilxxi")] == ["Bad_Roman_Number"]
      and T.tricks(X, "cilxxi")[0]["via"][0]["value"] == 170)
X.use_roman = False
check("with the numerals switched off, Two_Words stands",
      {a["via"][0]["kind"] for a in T.tricks(X, "cilxxi")} == {"TWO_WORDS"})

print("\n--- 4c. the non-enclitic TACKONs (word_package.adb, Try_Tackons)")
ENC = [{"tack": t, "entry": {"pos": "X"}, "line": 0, "meaning": ""} for t in ("que", "ne", "ue", "est")]


def tk(tack, pos, decl=None, line=1):
    e = {"pos": pos}
    if decl:
        e["decl"] = decl
    return {"tack": tack, "entry": e, "line": line, "meaning": tack + " meaning"}


class TFake(Fake):
    """Fake, with Word ending in Try_Tackons as whitaker.Whitaker.plain does."""
    def __init__(self, known, tackons):
        super().__init__(known)
        self.tackon_items = ENC + tackons

    def plain(self, w):
        return super().plain(w) or T.try_tackons(self, W.fold(w), self.plain)


PRON5 = {"entry": 6, "parse": {"pos": "PRON", "decl": [5, 1]}}
PRON3 = {"entry": 7, "parse": {"pos": "PRON", "decl": [3, 1]}}
ADJ11 = {"entry": 8, "parse": {"pos": "ADJ", "decl": [1, 1]}}
N31 = {"entry": 9, "parse": {"pos": "N", "decl": [3, 1]}}
N21 = {"entry": 10, "parse": {"pos": "N", "decl": [2, 1]}}
MET = tk("met", "PRON", (5, 0), 42)
check("Subtract_Tackon: only from a longer word",
      T.subtract_tackon("egomet", "met") == "ego" and T.subtract_tackon("met", "met") is None
      and T.subtract_tackon("mecum", "met") is None)
r = TFake({"ego": [PRON5]}, [MET]).plain("egomet")
check("a PRON tackon keeps a PRON whose declension fits, and says so in `via`",
      r and r[0]["via"][0] == {"kind": "TACKON", "tackon": "met", "as": "ego", "source": "ADDONS.LAT:42",
                               "explain": "met meaning"})
check("a PRON of another declension is dropped: no hit",
      TFake({"hic": [PRON3]}, [MET]).plain("hicmet") == [])
r = TFake({"ego": [PRON5, N21]}, [MET]).plain("egomet")
check("a record of another part of speech is dropped", [a["entry"] for a in r] == [6])
check("an ADJ tackon skips every check, even the declension ('Forego all checks')",
      TFake({"quantus": [ADJ11]}, [tk("cumque", "ADJ", (9, 9))]).plain("quantuscumque")[0]["via"][0]["tackon"]
      == "cumque")
r = TFake({"me": [PRON5]}, [tk("pte", "ADJ", (1, 0), 1), tk("pte", "PRON", (4, 0), 2),
                            tk("pte", "PRON", (5, 0), 3)]).plain("mepte")
check("tackons are tried in ADDONS order until one hits (mepte: the third -pte)",
      r and all(a["via"][0]["source"] == "ADDONS.LAT:3" for a in r))
r = TFake({"hic": [PRON3]}, [tk("ce", "PRON", (3, 1), 1), tk("ce", "PRON", (3, 0), 2)]).plain("hicce")
check("the first tackon that hits wins ('Be happy with one')",
      len(r) == 1 and r[0]["via"][0]["source"] == "ADDONS.LAT:1")
check("a NOUN tackon keeps a noun of its declension",
      TFake({"pater": [N31]}, [tk("familias", "N", (3, 0))]).plain("paterfamilias")[0]["via"][0]["tackon"]
      == "familias")
r = TFake({"lupus": [N21]}, [tk("familias", "N", (3, 0))]).plain("lupusfamilias")
check("the Ada's NOUN quirk: a noun of another declension is neither a hit nor deleted, and stays unmarked",
      r and r[0]["entry"] == 10 and not r[0].get("via"))
check("the first four TACKONs (the enclitics) are not Try_Tackons's",
      TFake({"ego": [PRON5]}, [MET]).plain("egoque") == [])
r = TFake({"ego": [PRON5]}, [MET, tk("pte", "PRON", (5, 0))]).plain("egometpte")
check("Word less a tackon is Word again, tackons and all (egometpte)",
      r and [v["tackon"] for v in r[0]["via"]] == ["pte", "met"])
r = T.parse_latin_word(TFake({"egomet": [N], "ego": [PRON5]}, [MET]), "egomet")
check("tackons run only when Word found nothing", [a["entry"] for a in r] == [0])


print("\n--- 4d. stem keys (makedict_main.adb) and the adverb's comparison")
E = lambda part, stems: {"part": part, "stems": stems}
check("a one-stem ADJ SUPER is keyed 4, COMP 3 (pessi, interi)",
      W.stem_keys(E({"pos": "ADJ", "decl": (0, 0), "co": "SUPER"}, ["pessi", "", "", ""])) == [("pessi", 4)]
      and W.stem_keys(E({"pos": "ADJ", "decl": (0, 0), "co": "COMP"}, ["interi", "", "", ""])) == [("interi", 3)])
check("a one-stem ADV COMP is keyed 2, SUPER 3",
      W.stem_keys(E({"pos": "ADV", "co": "COMP"}, ["magis", "", "", ""])) == [("magis", 2)]
      and W.stem_keys(E({"pos": "ADV", "co": "SUPER"}, ["maxime", "", "", ""])) == [("maxime", 3)])
check("a NUM of one sort is keyed by it: CARD 1, ORD 2, DIST 3, ADVERB 4",
      [W.stem_keys(E({"pos": "NUM", "decl": (2, 0), "sort": so, "value": 0}, ["x", "", "", ""]))[0][1]
       for so in ("CARD", "ORD", "DIST", "ADVERB")] == [1, 2, 3, 4])
check("everything else by its slot, blanks and zzz skipped",
      W.stem_keys(E({"pos": "ADJ", "decl": (1, 1), "co": "X"}, ["bon", "bon", "meli", "zzz"]))
      == [("bon", 1), ("bon", 2), ("meli", 3)]
      and W.stem_keys(E({"pos": "NUM", "decl": (1, 1), "sort": "X", "value": 1}, ["un", "prim", "singul", "semel"]))
      == [("un", 1), ("prim", 2), ("singul", 3), ("semel", 4)])
check("an adverb's comparison from its key is 1 POS, 2 COMP, 3 SUPER (not the adjective's 1-2/3/4)",
      [W.adv_comp_from_key(k) for k in (1, 2, 3)] == ["POS", "COMP", "SUPER"]
      and [W.adj_comp_from_key(k) for k in (1, 2, 3, 4)] == ["POS", "POS", "COMP", "SUPER"])

print("\n--- 4e. capitalisation (parse.adb Is_Capitalized) and the names table")
check("Is_Capitalized: A-Z then a-z, two letters or more",
      [T.is_capitalized(x) for x in ("Absalom", "Ab", "ABSALOM", "absalom", "A", "", None, "\u00c6gyptus", "aB")]
      == [True, True, False, False, False, False, False, False, False])
X = Fake({"caelum": [N]})
check("no TRICKS on a capitalised form (Celum: nothing), as the Ada's Parse_Latin_Word",
      T.parse_latin_word(X, "celum", raw="Celum") == [])
check("the same form written lower-case is still reached by a trick (celum -> caelum)",
      via0(T.parse_latin_word(X, "celum", raw="celum")).get("as") == "caelum")
check("with only a search key (no raw), nothing is capitalised: tricks run as before",
      via0(T.parse_latin_word(X, "celum")).get("as") == "caelum")
check("nor TRICKS on a capitalised form less an enclitic (Celumque)",
      T.parse_latin_word(X, "celumque", raw="Celumque") == []
      and T.parse_latin_word(X, "celumque", raw="celumque") != [])
X = Fake({"attuli": [PERF]})
check("SLURY still runs on a capitalised form (it is in Pass, before the test)",
      via0(T.parse_latin_word(X, "adtuli", raw="Adtuli")).get("kind") == "SLURY")
X = Fake({"amavisti": [PERF]})
check("SYNCOPE still runs on a capitalised form",
      via0(T.parse_latin_word(X, "amasti", raw="Amasti")).get("kind") == "SYNCOPE")
X = Fake({"caelum": [N]})
X.use_caps = False
check("switched off (use_caps False), a capitalised form gets its tricks again",
      via0(T.parse_latin_word(X, "celum", raw="Celum")).get("as") == "caelum")
NAME = {"entry": None, "unique": None, "name": {"lemma": "Jonathas", "headword": "ionathas", "source": "t"},
        "parse": {"pos": "proper"}}
X = Fake({})
X.names = {"ionathae": [NAME]}
check("the names table is consulted for a capitalised form",
      [a["name"]["lemma"] for a in T.parse_latin_word(X, "ionathae", raw="Jonathae")] == ["Jonathas"])
check("... and not for the same form written lower-case", T.parse_latin_word(X, "ionathae", raw="jonathae") == [])
r = T.parse_latin_word(X, "ionathaeque", raw="Jonathaeque")
check("a name less an enclitic (Jonathaeque = Jonathae + -que)",
      [(a["name"]["lemma"], a.get("enclitic")) for a in r] == [("Jonathas", "que")])
X = Fake({"ionathae": [N]})
X.names = {"ionathae": [NAME]}
r = T.parse_latin_word(X, "ionathae", raw="Jonathae")
check("a name sits beside WORDS's own reading, as a name in DICTLINE would",
      sorted(str(a.get("entry")) for a in r) == ["0", "None"])
check("a names hit stops SLURY and FIXES, as any plain reading does",
      [v["kind"] for a in r for v in a.get("via", [])] == [])

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

    # the 222 forms of the two drafted hymns, as first measured; then every
    # form, the three hymns printed from Britt 1922 included
    drafted = {json.loads(l)["search_key"] for l in open(os.path.join(REPO, "data", "hymns", "tokens.jsonl"),
                                                        encoding="utf-8") if json.loads(l)["legacy_address"]}

    def measure(rows):
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
        return n, before, after

    n, before, after = measure([r for r in rows if r["form"] in drafted])
    # measured 2026-09-26: 30 respellings; 3 recovered before the port, 22 after
    check("medieval respellings of hymn forms (ae>e, oe>e, ti>ci, doubled>single): 3 -> 22 of 30",
          (n, before, after) == (30, 3, 22), (n, before, after))
    # measured 2026-09-26 on all 547 forms: 80 respellings; 9 before, 53 after
    m = measure(rows)
    check("the same on every hymn form, the printed hymns included: 9 -> 53 of 80",
          m == (80, 9, 53), m)


    print("\n--- 8. TACKONs and Roman numerals, against the files")
    add = W.load_addons(os.path.join(W.CACHE, "ADDONS.LAT"))
    check("the first four TACKONs are the enclitics parse.adb tries (que, ne, ve, est)",
          [t["tack"] for t in add["tackons"][:4]] == ["que", "ne", "ue", "est"] == X.tackons[:4])
    # ADDONS.LAT at the pinned commit, read by eye 2026-09-26: the TACKONs
    # "that are not PACKONS", in file order
    check("Try_Tackons's list is ADDONS.LAT's, in order, with its parts of speech",
          [(t["tack"], t["entry"]["pos"]) for t in add["tackons"][4:]] ==
          [("cumque", "ADJ"), ("cunque", "ADJ"), ("cine", "PRON"), ("pte", "ADJ"), ("pte", "PRON"),
           ("pte", "PRON"), ("ce", "PRON"), ("modi", "PRON"), ("modi", "PRON"), ("dem", "PRON"),
           ("cum", "PRON"), ("uis", "ADJ"), ("met", "PRON"), ("familias", "N")],
          [t["tack"] for t in add["tackons"][4:]])
    check("PACKONs are kept apart (PACK 1/2, meaning 'PACKON w/'), as Load_Addons does",
          add["packons"] and all(t["entry"]["pos"] == "PACK" for t in add["packons"])
          and not any(t["entry"]["pos"] == "PACK" for t in add["tackons"]))
    if W.have_ada():
        rn = open(os.path.join(W.CACHE, "ada", "words_engine-roman_numerals_package.adb"),
                  encoding="latin-1").read()
        rn = re.sub(r"--[^\n]*", "", rn)
        vals = {a.lower(): int(v) for a, v in re.findall(r"when '(\w)' \| '\w'\s*=>\s*return\s+(\d+);", rn)}
        check("the Roman digits and values are the Ada's (Value; U commented out)", vals == T.ROMAN_VALUE, vals)
    for form, head, tack in [("egomet", "ego", "met"), ("mecum", "ego", "cum"), ("nobiscum", "nos", "cum"),
                             ("quantuscumque", "quantus", "cumque"), ("suapte", "suus", "pte"),
                             ("mepte", "ego", "pte"), ("huiusmodi", "hic", "modi"),
                             ("paterfamilias", "pater", "familias"), ("hicine", "hic", "cine"),
                             ("hocce", "hic", "ce")]:
        check(f"{form}: {head} + -{tack}",
              any(a["headword"] == head and a["via"] and a["via"][0].get("tackon") == tack
                  for a in X.analyze(form)))
    r = X.analyze("MCMXCIX")
    check("MCMXCIX is a Roman numeral, 1999, NUM 2 0 CARD",
          r and r[0]["via"][0]["value"] == 1999 and r[0]["whitaker"] == "NUM 2 0 X X X CARD"
          and r[0]["form_by"] == "whitaker-roman")
    check("vi is both 6 and a form of vis", {a["headword"] for a in X.analyze("vi")} >= {"ui", "uis"})
    check("iix, ill-formed, is read leniently as 8", [a["via"][0].get("value") for a in X.analyze("iix")] == [8])
    X.use_tackons = X.use_roman = False
    check("switched off, egomet is unknown and xiv is not a numeral",
          X.analyze("egomet") == [] and not any(a["via"] and a["via"][0]["kind"] == "ROMAN"
                                                for a in X.analyze("xiv")))
    X.use_tackons = X.use_roman = True


    print("\n--- 9. stem keys and adverb comparison, against the files")
    if W.have_ada():
        md = open(os.path.join(W.CACHE, "ada", "makedict_main.adb"), encoding="latin-1").read()
        md = re.sub(r"--[^\n]*", "", md)
        got = {(pos.upper(), val.upper()): int(k) for pos, val, k in re.findall(
            r"De\.Part\.Pofs = (Adj|Adv|Num)\s+and then\s+De\.Part\.\w+\.(?:Co|Sort) = (\w+)\s+then\s+"
            r"Put \(Stemlist, De\.Stems \(1\)\);.*?Integer_IO\.Put \(Stemlist, (\d), 2\)", md, re.S)}
        check("the one-stem keys are makedict_main.adb's", got == W.ONE_STEM_KEY, got)
        ws = open(os.path.join(W.CACHE, "ada", "support_utils-word_support_package.adb"), encoding="latin-1").read()
        m = re.search(r"function Adv_Comp_From_Key.*?end Adv_Comp_From_Key", ws, re.S).group(0)
        ada = {int(k): v.upper() for k, v in re.findall(r"when (\d)\s*=>\s*return (\w+);", m)}
        check("Adv_Comp_From_Key is the Ada's", ada == {k: W.adv_comp_from_key(k) for k in ada}, ada)

    def parses(form):
        return {(a["headword"], a["whitaker"]) for a in X.analyze(form) if not a["via"]}
    for form, want in [("pessimum", ("pessimus", "ADJ 0 0 ACC S M SUPER")),
                       ("summus", ("summus", "ADJ 0 0 NOM S M SUPER")),
                       ("interiora", ("interior", "ADJ 0 0 ACC P N COMP")),
                       ("proximam", ("proximus", "ADJ 0 0 ACC S F SUPER")),
                       ("pejus", ("male", "ADV COMP")), ("pessime", ("male", "ADV SUPER")),
                       ("magis", ("magis", "ADV COMP"))]:
        check(f"{form}: {want[0]} {want[1]}", want in parses(form), sorted(parses(form))[:3])
    check("vicesimo: an ordinal of viginti (NUM ... ORD)",
          any(a["whitaker"].endswith("ORD") and a["headword"] == "uiginti" for a in X.analyze("vicesimo")))


    print("\n--- 10. PACKONs and TICKONs (Word's Qu block), against the files")
    check("the PACKONs are ADDONS.LAT's, in order",
          [t["tack"] for t in X.packons] == ["cumque", "cunque", "que", "piam", "quam", "dam", "nam", "cum",
                                            "uis", "libet", "lubet"], [t["tack"] for t in X.packons])
    check("the TICKONs are ADDONS.LAT's (PREFIX with root PACK)",
          [t["fix"] for t in X.tickons] == ["ec", "ne", "nescio", "neu", "seu", "si"])

    def keys(form):
        return {(a["key"], a["whitaker"]) for a in X.analyze(form)}
    DAM = "qui, quae, quod + -dam  PACK"
    for form, want in [("quaedam", (DAM, "PRON 1 0 NOM P F")), ("quemdam", (DAM, "PRON 1 0 ACC S M")),
                       ("quicumque", ("qui, quae, quod + -cumque  PACK", "PRON 1 1 NOM S M")),
                       ("quidquam", ("qui, quae, quod + -quam  PACK", "PRON 1 6 NOM S N")),
                       ("quispiam", ("quis, quid + -piam  PACK", "PRON 1 2 NOM S C")),
                       ("quilibet", ("qui, quae, quod + -libet  PACK", "PRON 1 0 NOM P M"))]:
        check(f"{form}: {want[0].split('  ')[0]}, {want[1]}", want in keys(form), sorted(keys(form))[:3])
    check("-dam turns a final n back to m (quendam is read as quem + dam)",
          (DAM, "PRON 1 0 ACC S M") in keys("quendam"))
    check("the cu- stem (key 2) is looked up too (cuiusdam)", (DAM, "PRON 1 0 GEN S X") in keys("cuiusdam"))
    check("the PACK entry must have exactly the ending's declension (quidquam: only the 1 6 entry)",
          {w.split()[2] for _, w in keys("quidquam")} == {"6"})
    check("the meaning test compares a prefix, as the Ada does: -cum also finds (w/-cumque) entries",
          {k for k, _ in keys("quocum")} >= {"quis, quid + -cum  PACK", "qui, quae, quod + -cumque  PACK"})
    check("PACKONs run only when the form reads as at most one qu-pronoun record (quem: no PACKON)",
          not any(a["via"] for a in X.analyze("quem")) and any(a["via"] for a in X.analyze("quemque")))
    r = X.analyze("quaedam")
    check("a PACK lemma's heading is the house's, composed from the pronoun's and the tackon",
          r and r[0]["form_by"] == "house" and r[0]["headword"] == "qui"
          and r[0]["via"][0]["kind"] == "PACKON" and r[0]["via"][0]["tackon"] == "dam")
    r = X.analyze("siqua")
    check("a TICKON before a qu-pronoun: siqua = si + qua",
          r and all(a["via"][0]["kind"] == "TICKON" and a["via"][0]["fix"] == "si" for a in r)
          and {a["headword"] for a in r} >= {"quis"})
    check("nescioquis = nescio + quis", any(a["via"] and a["via"][0].get("fix") == "nescio" for a in X.analyze("nescioquis")))
    X.use_packons = False
    check("switched off, quaedam is only a two-words guess and siqua has no reading",
          {v["kind"] for a in X.analyze("quaedam") for v in a["via"]} == {"TWO_WORDS"}
          and X.analyze("siqua") == [])
    X.use_packons = True

    print("\n--- 11. capitalisation on real words")
    if W.have_ada():
        ada = open(os.path.join(W.CACHE, "ada", "words_engine-parse.adb"), encoding="latin-1").read()
        check("the Ada skips Try_Tricks only when Ignore_Unknown_Names and Capitalized",
              re.search(r"if \(Pa_Last = 0\)\s+and then\s+not \(Words_Mode \(Ignore_Unknown_Names\)"
                        r"\s+and Capitalized\)", ada) is not None
              and re.search(r"Input_Word \(Input_Word'First\) in 'A' \.\. 'Z' and then\s+"
                            r"Input_Word \(Input_Word'First \+ 1\) in 'a' \.\. 'z'", ada) is not None)

    def heads(f):
        return {(a["headword"], tuple(v["kind"] for v in a["via"])) for a in X.analyze(f)}

    check("hiram, lower-case, is read by a trick (internal h/); Hiram, capitalised, is not read",
          any("TRICK" in k for _, k in heads("hiram")) and heads("Hiram") == set())
    check("Absalom keeps its prefix reading (abs-): WORDS runs the FIXES on names too",
          any("PREFIX" in k for _, k in heads("Absalom")))
    X.use_caps = False
    check("with use_caps off, Hiram is read by the trick again", any("TRICK" in k for _, k in heads("Hiram")))
    X.use_caps = True

    print("\n--- 12. the house supplement")
    rows = W.load_house_supplement()
    XH = W.Whitaker(house_supplement=True)
    unread = [(r["id"], f) for r in rows for f in r["attested"]
              if not any(a.get("house") == r["id"] for a in XH.analyze(f))]
    check(f"every row ({len(rows)}) reads each form it cites as attested", not unread, unread[:5])
    check("every row is the house's and says why",
          all(r["provenance"] == "house" and r["justification"] for r in rows))
    bad = [(r["id"], a["source"]) for r in rows for f in r["attested"] for a in XH.analyze(f)
           if a.get("house") == r["id"] and not a["source"].startswith("house-supplement.jsonl:")]
    check("a house reading names its row as its source, never a DICTLINE line", not bad, bad[:3])
    r = XH.analyze("basim")
    check("an `of` row is read as Whitaker's lemma (basim: bas, baseos/is, ACC S)",
          [(a["key"], a["whitaker"]) for a in r] == [("bas, baseos/is  N F", "N 3 9 ACC S F")])
    check("pharisaeus is a lemma of its own, headed by the house (form_by house)",
          {(a["key"], a["form_by"]) for a in XH.analyze("pharisaeorum")}
          == {("pharisaeus, pharisaei  N (2nd) M", "house")})
    check("only_forms adds nothing elsewhere: prophetis stays propheta's alone",
          {a["key"] for a in XH.analyze("prophetis")} == {a["key"] for a in X.analyze("prophetis")})
    check("... and without the supplement those forms have no plain reading (pharisaei, setim)",
          not [a for a in X.analyze("pharisaei") if not a["via"]] and not [a for a in X.analyze("setim") if not a["via"]])
    for broken, why in (({"id": "x", "provenance": "house", "stems": ["x"], "part": "N 9 9 N T",
                          "attested": {"x": 1}}, "no justification"),
                        ({"id": "x", "provenance": "wiktionary", "stems": ["x"], "part": "N 9 9 N T",
                          "attested": {"x": 1}, "justification": "j"}, "provenance not house"),
                        ({"id": "x", "provenance": "house", "of": "nothing  N",
                          "forms": [{"form": "x", "parse": "N 9 9 X X N"}],
                          "attested": {"x": 1}, "justification": "j"}, "`of` not a Whitaker form"),
                        ({"id": "x", "provenance": "house", "stems": ["zz"], "part": "N 9 9 N T",
                          "only_forms": ["qq"], "attested": {"qq": 1}, "justification": "j"},
                         "stems that do not read the form")):
        try:
            W.Whitaker(house_supplement=[dict(broken, line=1)])
            ok = False
        except SystemExit:
            ok = True
        check(f"a bad row stops the build ({why})", ok)

    print("\n--- 13. PACK headings")
    XR = W.Whitaker(pack_headings="real")
    check("by default a PACK lemma keeps the house heading (quaedam: qui, quae, quod + -dam)",
          {a["key"] for a in X.analyze("quaedam")} == {"qui, quae, quod + -dam  PACK"})
    check("with pack_headings='real' it is quidam's own (quidam, quaedam, quoddam; headword quidam)",
          {(a["key"], a["headword"], a["form_by"]) for a in XR.analyze("quaedam")}
          == {("quidam, quaedam, quoddam  PACK", "quidam", "house")})
    check("quisquam, filed ADJECT by WORDS, is headed quisquam, never 'quiquam'",
          {a["key"] for a in XR.analyze("quisquam")} >= {"quisquam, quaequam, quidquam  PACK"})
    check("quis + -cum has no nominative to head it and keeps the house heading",
          "quis, quid + -cum  PACK" in {a["key"] for a in XR.analyze("quocum")})
    house_pack = {tuple(re.match(r"(.*) \+ -(\w+)  PACK", X.form(i)[0]).groups())
                  for i, e in enumerate(X.entries) if e["part"]["pos"] == "PACK" and X.form(i)[1] == "house"}
    check("every house PACK heading has an entry in HOUSE_PACK_HEADWORDS",
          house_pack == set(W.HOUSE_PACK_HEADWORDS), sorted(house_pack ^ set(W.HOUSE_PACK_HEADWORDS)))
    try:
        W.Whitaker(pack_headings="latin")
        ok = False
    except ValueError:
        ok = True
    check("any other pack_headings value is refused", ok)

print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
