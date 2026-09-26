#!/usr/bin/env python3
"""
whitaker_tricks.py -- what WORDS does when a form is not simply stem + ending:
SYNCOPE, SLURY, FIXES (prefixes and suffixes) and TRICKS, and the order it
tries them in. Ported rule for rule from the Ada source at whitaker.COMMIT:

    words_engine-trick_tables.ads/.adb   the tables below, row for row, in order
    words_engine-tricks.adb              Syncope, Try_Tricks, Try_Slury
    words_engine-word_package.adb        Prune_Stems, Apply_Prefix,
                                         Apply_Suffix, Reduce_Stem_List
    words_engine-parse.adb               Pass, Enclitic, Tricks_Enclitic,
                                         Parse_Latin_Word (the order of attempts)
    support_utils-addons_package.adb     Load_Addons, Subtract_Prefix/Suffix

Every analysis these rules produce carries `via`: the list of rules that
turned the form into one WORDS could read, e.g.
    [{"kind": "TRICK", "table": "E_Tricks", "rule": "flip e/ae", "as": "caelum", ...}]
so nothing reached by a trick can pass for a plain dictionary hit.

WHERE THIS PORT DEPARTS FROM THE ADA, AND WHY (each is also in the README)
  * The forms are search keys, already folded (j -> i, v -> u). The tables
    are folded the same way before use, so a rule written with v or j (e.g.
    `uol`/`vul`, `dij`/`disj`, medieval `v`/`b`) acts on u or i. On folded
    text WORDS's u/v distinction cannot be recovered; `u` is always a vowel
    to Double_Consonants.
  * WORDS decides "the perfect system" (syncope) and "a form of eo" (the
    `is` -> `iis` trick) by looking only at the LAST record in its parse
    array, whose order comes from a bubble sort on internal record numbers.
    Here any analysis of that kind qualifies.
  * Slur's second branch (`attuli` -> `adtuli`) compares strings of unequal
    length, which in Ada is always False: it can never fire, so it is not
    ported.
  * Whether the fixes try prefix-first or suffix-first depends in WORDS on a
    stale package variable (Pdl_Index, left by the previous dictionary
    search). Here it is recomputed for the form itself.
  * Not ported: Roman numerals, the non-enclitic TACKONs and PACKONs
    (Try_Tackons, Process_Packons), qu-pronoun TICKONs, and the second,
    duplicate syncope pass and Do_Only_Fixes re-parse inside Enclitic.
    WORDS skips all tricks on a capitalised word it takes for a name; search
    keys are lower case, so here every form is tried.
"""

from whitaker import fold

# ---------------------------------------------------------------------------
# The tables (words_engine-trick_tables.ads / .adb), verbatim and in order.
# (op, x1, x2, max). `max` is kept for the record: Iter_Tricks stops at the
# first rule that parses, whatever its Max, because a hit always leaves at
# least two records (the marker and a parse).
# ---------------------------------------------------------------------------

FF, FLIP, INTERNAL, SLUR = "flip_flop", "flip", "internal", "slur"

TRICKS = {
    "a": [(FF, "adgn", "agn", 0), (FF, "adsc", "asc", 0), (FF, "adsp", "asp", 0),
          (FF, "arqui", "arci", 0), (FF, "arqu", "arcu", 0), (FLIP, "ae", "e", 0),
          (FLIP, "al", "hal", 0), (FLIP, "am", "ham", 0), (FLIP, "ar", "har", 0),
          (FLIP, "aur", "or", 0)],
    "d": [(FLIP, "dampn", "damn", 0), (FF, "dij", "disj", 0), (FF, "dir", "disr", 0),
          (FF, "dir", "der", 0), (FF, "del", "dil", 0)],
    "e": [(FF, "ecf", "eff", 0), (FF, "ecs", "exs", 0), (FF, "es", "ess", 0),
          (FF, "ex", "exs", 0), (FLIP, "eid", "id", 0), (FLIP, "el", "hel", 0),
          (FLIP, "e", "ae", 0)],
    "f": [(FF, "faen", "fen", 0), (FF, "faen", "foen", 0), (FF, "fed", "foed", 0),
          (FF, "fet", "foet", 0), (FLIP, "f", "ph", 0)],
    "g": [(FLIP, "gna", "na", 0)],
    "h": [(FLIP, "har", "ar", 0), (FLIP, "hal", "al", 0), (FLIP, "ham", "am", 0),
          (FLIP, "hel", "el", 0), (FLIP, "hol", "ol", 0), (FLIP, "hum", "um", 0)],
    "k": [(FLIP, "k", "c", 0), (FLIP, "c", "k", 0)],
    "l": [(FF, "lub", "lib", 1)],
    "m": [(FF, "mani", "manu", 1)],
    "n": [(FLIP, "na", "gna", 0), (FF, "nihil", "nil", 0)],
    "o": [(FF, "obt", "opt", 1), (FF, "obs", "ops", 1), (FLIP, "ol", "hol", 0),
          (FLIP, "opp", "op", 1), (FLIP, "or", "aur", 0)],
    "p": [(FLIP, "ph", "f", 0), (FF, "pre", "prae", 1)],
    "s": [(FF, "subsc", "susc", 0), (FF, "subsp", "susp", 0), (FF, "subc", "susc", 0),
          (FF, "succ", "susc", 0), (FF, "subt", "supt", 0), (FF, "subt", "sust", 0)],
    "t": [(FF, "transv", "trav", 0)],
    "u": [(FLIP, "ul", "hul", 0), (FLIP, "uol", "vul", 0)],
    "y": [(FLIP, "y", "i", 0)],
    "z": [(FLIP, "z", "di", 0)],
}

ANY_TRICKS = [
    (INTERNAL, "ae", "e", 0), (INTERNAL, "bul", "bol", 0), (INTERNAL, "bol", "bul", 0),
    (INTERNAL, "cl", "cul", 0), (INTERNAL, "cu", "quu", 0), (INTERNAL, "f", "ph", 0),
    (INTERNAL, "ph", "f", 0), (INTERNAL, "h", "", 0), (INTERNAL, "oe", "e", 0),
    (INTERNAL, "vul", "vol", 0), (INTERNAL, "vol", "vul", 0), (INTERNAL, "uol", "vul", 0),
]

# Harrington/Elliott, as the Ada comments cite them
MEDIAEVAL_TRICKS = [
    (INTERNAL, "col", "caul", 0),
    (INTERNAL, "e", "ae", 0), (INTERNAL, "o", "u", 0), (INTERNAL, "i", "y", 0),
    (INTERNAL, "ism", "sm", 0), (INTERNAL, "isp", "sp", 0), (INTERNAL, "ist", "st", 0),
    (INTERNAL, "iz", "z", 0), (INTERNAL, "esm", "sm", 0), (INTERNAL, "esp", "sp", 0),
    (INTERNAL, "est", "st", 0), (INTERNAL, "ez", "z", 0),
    (INTERNAL, "di", "z", 0), (INTERNAL, "f", "ph", 0), (INTERNAL, "is", "ix", 0),
    (INTERNAL, "b", "p", 0), (INTERNAL, "d", "t", 0), (INTERNAL, "v", "b", 0),
    (INTERNAL, "v", "f", 0), (INTERNAL, "v", "f", 0), (INTERNAL, "s", "x", 0),
    (INTERNAL, "ci", "ti", 0),
    (INTERNAL, "nt", "nct", 0), (INTERNAL, "s", "ns", 0),
    (INTERNAL, "ch", "c", 0), (INTERNAL, "c", "ch", 0), (INTERNAL, "th", "t", 0),
    (INTERNAL, "t", "th", 0),
]

SLUR_TRICKS = {
    "a": [(FF, "abs", "aps", 0), (FF, "acq", "adq", 0), (FF, "ante", "anti", 0),
          (FF, "auri", "aure", 0), (FF, "auri", "auru", 0), (SLUR, "ad", None, 0)],
    "c": [(FLIP, "circum", "circun", 0), (FF, "con", "com", 0), (FLIP, "co", "com", 0),
          (FLIP, "co", "con", 0), (FF, "conl", "coll", 0)],
    "i": [(SLUR, "in", None, 1), (FF, "inb", "imb", 1), (FF, "inp", "imp", 1)],
    "n": [(FLIP, "nun", "non", 0)],
    "o": [(SLUR, "ob", None, 0)],
    "q": [(FF, "quadri", "quadru", 0)],
    "s": [(FLIP, "se", "ce", 0), (SLUR, "sub", None, 0)],
}

# Common_Prefix: first halves Two_Words refuses (they are also prepositions)
COMMON_PREFIXES = ("dis", "ex", "in", "per", "prae", "pro", "re", "si", "sub", "super", "trans")

TABLE_NAMES = {**{c: c.upper() + "_Tricks" for c in TRICKS}}
SLUR_TABLE_NAMES = {c: c.upper() + "_Slur_Tricks" for c in SLUR_TRICKS}

VOWELS = set("aeiouy")


def _f(x):
    return fold(x) if x else x


def _is_vowel(c):
    return c in VOWELS


# ---------------------------------------------------------------------------
# The engine. `X` is a whitaker.Whitaker; `X.plain(w)` is Word_Package.Word
# without fixes (uniques + stem/ending), each analysis a dict with `via`.
# ---------------------------------------------------------------------------

def _tag(analyses, step):
    for a in analyses:
        a["via"] = [step] + a.get("via", [])
    return analyses


def _perfect(analyses):
    """Pa (Pa_Last).IR.Qual.Pofs = V and Pa (Pa_Last).IR.Key = 3."""
    return any(a["parse"]["pos"] == "V" and a.get("stem_key") == 3 for a in analyses)


# -- SYNCOPE (tricks.adb, Syncope) -------------------------------------------

SYNCOPE_EXPLAIN = {
    "ii => ivi": "Syncopated perfect ivi can drop 'v' without contracting vowel",
    "s => vis": "Syncopated perfect often drops the 'v' and contracts vowel",
    "r => v.r": "Syncopated perfect often drops the 'v' and contracts vowel",
    "ier => iver": "Syncopated perfect often drops the 'v' and contracts vowel",
    "s/x => +is": "Syncopated perfect sometimes drops the 'is' after 's' or 'x'",
}


def syncope(X, s):
    """Gildersleeve and Lodge 131. Five rules in order; each walks the form
    from the right and stops at the first rewrite WORDS can parse."""
    def attempt(rule, positions, rewrite, need_perfect):
        for i in positions:
            t = rewrite(i)
            if t is None:
                continue
            r = X.plain(t)
            if r:
                if need_perfect and not _perfect(r):
                    return None
                return _tag(r, {"kind": "SYNCOPE", "rule": rule, "as": fold(t),
                                "explain": SYNCOPE_EXPLAIN[rule]})
        return None

    n = len(s)
    for rule, pos, rw, perf in (
        ("ii => ivi", range(n - 2, -1, -1),
         lambda i: s[:i + 1] + "v" + s[i + 1:] if s[i:i + 2] == "ii" else None, True),
        # the one rule whose hits stand even outside the perfect system
        ("s => vis", range(n - 3, -1, -1),
         lambda i: s[:i + 1] + "vi" + s[i + 1:] if s[i:i + 2] in ("as", "es", "is", "os") else None, False),
        ("r => v.r", range(n - 3, 0, -1),
         lambda i: s[:i + 1] + "ve" + s[i + 1:] if s[i:i + 2] in ("ar", "er", "or") else None, True),
        ("ier => iver", range(n - 4, -1, -1),
         lambda i: s[:i + 1] + "v" + s[i + 1:] if s[i:i + 3] == "ier" else None, True),
        ("s/x => +is", range(n - 3, -1, -1),
         lambda i: s[:i + 1] + "is" + s[i + 1:] if s[i] in "sx" else None, True),
    ):
        r = attempt(rule, pos, rw, perf)
        if r:
            return r
    return []


# -- the three rewrites TRICKS and SLURY share --------------------------------

def _flip(tword, s, x1, x2, kind, table, explain=None):
    x1, x2 = _f(x1), _f(x2)
    if len(s) >= len(x1) + 2 and s.startswith(x1):
        t = x2 + s[len(x1):]
        r = tword(t)
        if r:
            return _tag(r, {"kind": kind, "table": table, "rule": f"flip {x1}/{x2}", "as": t,
                            "explain": explain or f"An initial '{x1}' may have replaced usual '{x2}'"})
    return []


def _flip_flop(tword, s, x1, x2, kind, table, exclusive):
    """X1 -> X2 at the start; then X2 -> X1. SLURY's version is if/elsif
    (`exclusive`); TRICKS's tries the second even after the first matched."""
    x1, x2 = _f(x1), _f(x2)
    first = len(s) >= len(x1) + 2 and s.startswith(x1)
    if first:
        t = x2 + s[len(x1):]
        r = tword(t)
        if r:
            return _tag(r, {"kind": kind, "table": table, "rule": f"flip_flop {x1}/{x2}", "as": t,
                            "explain": f"An initial '{x1}' may be rendered by '{x2}'"})
    if exclusive and first:
        return []
    if len(s) >= len(x2) + 2 and s.startswith(x2):
        t = x1 + s[len(x2):]
        r = tword(t)
        if r:
            return _tag(r, {"kind": kind, "table": table, "rule": f"flip_flop {x2}/{x1}", "as": t,
                            "explain": f"An initial '{x2}' may be rendered by '{x1}'"})
    return []


def _internal(tword, s, x1, x2, table):
    x1, x2 = _f(x1), _f(x2)
    for i in range(0, len(s) - len(x1) + 1):
        if s[i:i + len(x1)] == x1:
            t = s[:i] + x2 + s[i + len(x1):]
            r = tword(t)
            if r:
                return _tag(r, {"kind": "TRICK", "table": table, "rule": f"internal {x1}/{x2}",
                                "as": t, "explain": f"An internal '{x1}' might be rendered by '{x2}'"})
    return []


def _slur(tword, s, x1, table):
    """An initial `ad`/`in`/`ob`/`sub` before a consonant may be assimilated:
    adtuli is tried as attuli. (The reverse branch is dead in the Ada.)"""
    sl = len(x1)
    if len(s) >= sl + 2 and s.startswith(x1) and not _is_vowel(s[sl]):
        t = x1[:-1] + s[sl] + s[sl:]
        r = tword(t)
        if r:
            return _tag(r, {"kind": "SLURY", "table": table, "rule": f"slur {x1}/{x1[:-1]}~", "as": t,
                            "explain": f"An initial '{x1}' may be rendered by {x1[:-1]}~"})
    return []


def _iter(tword, s, rows, kind, table, exclusive_ff):
    for op, x1, x2, _max in rows:
        if op == FF:
            r = _flip_flop(tword, s, x1, x2, kind, table, exclusive_ff)
        elif op == FLIP:
            r = _flip(tword, s, x1, x2, kind, table,
                      None if kind == "TRICK" else f"An initial '{_f(x1)}' may be rendered by '{_f(x2)}'")
        elif op == INTERNAL:
            r = _internal(tword, s, x1, x2, table)
        else:
            r = _slur(tword, s, x1, table)
        if r:
            return r            # Finished: the first rule that parses wins
    return []


# -- SLURY (tricks.adb, Try_Slury) --------------------------------------------

def slury(X, s):
    """Assimilated prefixes. Its Tword runs with prefixes off: plain + syncope."""
    rows = SLUR_TRICKS.get(s[:1])
    if not rows:
        return []
    return _iter(lambda t: X.plain(t) + syncope(X, t), s, rows, "SLURY", SLUR_TABLE_NAMES[s[0]], True)


# -- TRICKS (tricks.adb, Try_Tricks) ------------------------------------------

def _adj_terminal_iis(X, s):
    if len(s) > 3 and s.endswith("is"):
        t = s[:-2] + "iis"
        r = [a for a in X.plain(t)
             if a["parse"]["pos"] == "ADJ" and tuple(a["parse"]["decl"]) == (1, 1)
             and a["parse"]["case"] in ("DAT", "ABL") and a["parse"]["number"] == "P"]
        if r:
            return _tag(r, {"kind": "TRICK", "table": "Adj_Terminal_Iis", "rule": "iis -> is", "as": t,
                            "explain": "A Terminal 'iis' on ADJ 1 1 DAT/ABL P might drop 'i'"})
    return []


def _double_consonants(tword, s):
    for i in range(1, len(s) - 1):
        if not _is_vowel(s[i]) and _is_vowel(s[i - 1]) and _is_vowel(s[i + 1]):
            t = s[:i + 1] + s[i] + s[i + 1:]
            r = tword(t)
            if r:
                return _tag(r, {"kind": "TRICK", "table": "Double_Consonants",
                                "rule": f"{s[i]} -> {s[i]}{s[i]}", "as": t,
                                "explain": "A doubled consonant may be rendered by just the single  MEDIEVAL"})
    return []


def _two_words(X, s):
    """Two words run together. WORDS's own verdict on its guesses: 'If not
    obvious, probably incorrect'. They are tagged, and the resolver never
    takes one as a lemma."""
    n = len(s)
    if n < 5:
        return []
    i = 2
    while i < n - 2:
        r1, mid = [], None
        while i < n - 2:
            if s[:i] not in COMMON_PREFIXES:
                r1 = X.plain(s[:i])
                if r1:
                    mid = i
                    break
            i += 1
        if not r1:
            return []
        r2 = X.plain(s[mid:])
        if r2:
            if any(a["parse"]["pos"] == "NUM" for a in r1) and any(a["parse"]["pos"] == "NUM" for a in r2):
                r1 = [a for a in r1 if a["parse"]["pos"] == "NUM"]     # Trim_Output: a compound number
                r2 = [a for a in r2 if a["parse"]["pos"] == "NUM"]
            split = s[:mid] + "+" + s[mid:]
            for part, r in ((1, r1), (2, r2)):
                _tag(r, {"kind": "TWO_WORDS", "rule": "two words", "as": split, "part": part,
                         "explain": f"May be 2 words combined ({split}) If not obvious, probably incorrect"})
            return r1 + r2
        i += 1
    return []


def tricks(X, s):
    """Try_Tricks, in its order. Its Tword is plain + syncope."""
    def tword(t):
        return X.plain(t) + syncope(X, t)

    if s[:1] == "i":
        # for some forms of eo the stem "i" grates with an "is..." ending
        if s.startswith("is"):
            t = "i" + s
            r = tword(t)
            if any(a["parse"]["pos"] == "V" and tuple(a["parse"]["decl"]) == (6, 1) for a in r):
                return _tag(r, {"kind": "TRICK", "table": "eo", "rule": "is => iis", "as": t,
                                "explain": "Some forms of eo stem 'i' grates with an 'is .. .' ending, so 'is' -> 'iis'"})
    elif s[:1] in TRICKS:
        r = _iter(tword, s, TRICKS[s[0]], "TRICK", TABLE_NAMES[s[0]], False)
        if r:
            return r
    r = _iter(tword, s, ANY_TRICKS, "TRICK", "Any_Tricks", False)
    if r:
        return r
    r = _adj_terminal_iis(X, s)
    if r:
        return r
    # Do_Medieval_Tricks (on by default)
    r = _iter(tword, s, MEDIAEVAL_TRICKS, "TRICK", "Mediaeval_Tricks", False)
    if r:
        return r
    # Double_Consonants does not end the search: Two_Words runs after it
    return _double_consonants(tword, s) + _two_words(X, s)


# -- FIXES (word_package.adb, Prune_Stems and friends) -------------------------

def _pos_le(left, right):
    return right == left or (left == "PACK" and right == "PRON") or right == "X"


def _abbrev(part):
    return part["pos"] in ("N", "ADJ") and tuple(part["decl"]) == (9, 8)


def _subtract_prefix(stem, P):
    z = len(P["fix"])
    if len(stem) > z and stem[:z] == P["fix"] and (P["connect"] == " " or stem[z] == P["connect"]):
        return stem[z:]
    return None


def _subtract_suffix(stem, S):
    z = len(S["fix"])
    if len(stem) > z and stem[-z:] == S["fix"] and (S["connect"] == " " or stem[-z - 1] == S["connect"]):
        return stem[:-z]
    return None


def _reduce(X, cuts, prefix, suffix):
    """Reduce_Stem_List: dictionary entries under the stem left when the
    prefix and/or suffix are taken off, matched against the full form's
    endings -- the suffix first turning the entry into its target part."""
    out, seen = [], set()
    for stem, ending in cuts:
        r = stem
        if suffix is not None:
            r = _subtract_suffix(r, suffix)
            if r is None:
                continue
        if prefix is not None:
            r = _subtract_prefix(r, prefix)
            if r is None:
                continue
        for (i, k) in X.stem_index.get(r, ()):
            e = X.entries[i]
            part, key = e["part"], k
            if suffix is not None:
                if _abbrev(part):
                    continue
                if not (_pos_le(part["pos"], suffix["root"]) and
                        (suffix["root_key"] in (k, 0))):
                    continue
                part, key = suffix["target"], suffix["target_key"]
            if prefix is not None:
                if _abbrev(part) or part["pos"] in ("INTERJ", "CONJ"):
                    continue
                if not (part["pos"] == prefix["root"] or prefix["root"] == "X"):
                    continue
            eff = dict(e, part=part)
            for inf in X.by_ending[ending]:
                a = X._match(eff, key, r, inf)
                if a and (i, repr(sorted(a.items()))) not in seen:
                    seen.add((i, repr(sorted(a.items()))))
                    via = []
                    if prefix is not None:
                        via.append({"kind": "PREFIX", "fix": prefix["fix"], "source": f"ADDONS.LAT:{prefix['line']}",
                                    "explain": prefix["meaning"]})
                    if suffix is not None:
                        via.append({"kind": "SUFFIX", "fix": suffix["fix"], "source": f"ADDONS.LAT:{suffix['line']}",
                                    "explain": suffix["meaning"]})
                    out.append({"entry": i, "unique": None, "parse": a, "inflect_line": inf["line"],
                                "stem_key": k, "via": via})
    return out


def _apply_prefix(X, cuts, suffix):
    """The first prefix, in ADDONS order, that yields a reading ('we accept
    only one prefix')."""
    for P in X.prefixes:
        r = _reduce(X, cuts, P, suffix)
        if r:
            return r
    return []


def _apply_suffix(X, cuts):
    """Every suffix that yields a reading; where a suffix's stem is not in the
    dictionary, a prefix is tried on it as well. Returns (analyses, whether the
    LAST suffix tried yielded -- the Ada's Sxx, which decides whether the bare
    prefix is tried next)."""
    out, last = [], False
    for S in X.suffixes:
        red = [(st, en) for st, en in cuts if _subtract_suffix(st, S) is not None]
        if not red:
            continue
        if any(_subtract_suffix(st, S) in X.stem_index for st, _ in red):
            r = _reduce(X, red, None, S)
        else:
            r = _apply_prefix(X, red, S)
        out += r
        last = bool(r)
    return out, last


def fixes(X, w):
    """Prune_Stems with Do_Only_Fixes: nothing plain was found."""
    cuts = X.cuts(w)
    if not any(st in X.stem_index for st, _ in cuts):
        r = _apply_prefix(X, cuts, None)
        if r:
            return r
        r, _ = _apply_suffix(X, cuts)
        return r
    r, last = _apply_suffix(X, cuts)
    if not last:
        r += _apply_prefix(X, cuts, None)
    return r


# -- the order of attempts (parse.adb, Parse_Latin_Word / Pass) ----------------

def parse_latin_word(X, w):
    """Every analysis WORDS would give `w` (a folded search key), in the order
    it tries: plain; SLURY if nothing; SYNCOPE unless a form of esse is
    there; the enclitics; FIXES if still nothing (and the enclitics again,
    with fixes); TRICKS if still nothing, then TRICKS on the form less an
    enclitic."""
    res = X.plain(w)
    if not res:
        res = slury(X, w)
    if not any(a["parse"]["pos"] == "V" and tuple(a["parse"]["decl"]) == (5, 1) for a in res):
        res += syncope(X, w)
    done = False

    def enclitic(res, with_fixes):
        # with a parse in hand only -que is tried; without one, que/ne/ve/est
        # in turn, stopping at the first that strips
        for t in (X.tackons[:1] if res else X.tackons[:4]):
            if w.endswith(t) and len(w) > len(t):
                less = w[:-len(t)]
                if with_fixes:
                    more = fixes(X, less)
                else:
                    more = X.plain(less) or slury(X, less)
                for a in more:
                    a["enclitic"] = t
                return more
        return []

    more = enclitic(res, False)
    done = bool(more)
    res += more
    if not res:
        res = fixes(X, w)
        if not done:
            res += enclitic(res, True)
    if not res:
        res = tricks(X, w)
        if not res:
            for t in X.tackons[:4]:
                if w.endswith(t) and len(w) > len(t):
                    res = tricks(X, w[:-len(t)])
                    for a in res:
                        a["enclitic"] = t
                    break
    return res


def parse_plain(X, w):
    """The analyzer before these rules were ported (2026-09-26 morning): plain
    stem + ending, and the enclitics. Kept to measure what the rules add, and
    to prove they never take a plain analysis away."""
    res = X.plain(w)
    for t in (X.tackons[:1] if res else X.tackons[:4]):
        if w.endswith(t) and len(w) > len(t):
            more = X.plain(w[:-len(t)])
            for a in more:
                a["enclitic"] = t
            res += more
            break
    return res
