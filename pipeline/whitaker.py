#!/usr/bin/env python3
"""
whitaker.py -- William Whitaker's WORDS (Latin), read from its own data files.

    The four files WORDS runs on are fetched at a pinned commit of the
    maintained port (github.com/mk270/whitakers-words), checked against
    sha256 pins below, and kept under data/corpus/whitaker/ (gitignored, like
    every fetched corpus). Nothing here is hand-typed Latin: every lemma, stem
    and ending comes from those files.

    DICTLINE.GEN  ~39k dictionary lines: four stems, part of speech, flags,
                  English meaning (fixed columns)
    INFLECTS.LAT  ~1,800 endings: which stem they attach to, and the parse
    UNIQUES.LAT   irregular forms that no stem + ending produces
    ADDONS.LAT    tackons (-que, -ne, -ve ...) and prefixes/suffixes

WHAT IS PORTED, AND WHAT IS NOT
    Ported from the Ada source at the same commit, rule for rule:
      * stem + ending matching, with u=v and i=j (word_package.adb,
        Array_Stems; the "<=" containment rules of inflections_package.adb)
      * the verb filters (list_sweep.adb, Allowed_Stem): imperatives only in
        the 2nd/3rd person, the bare imperative only for dic/duc/fac/fer,
        IMPERS only in the 3rd person, DEP and SEMIDEP voice rules
      * uniques first, then the regular analysis; the enclitics que/ne/ve/est
        when nothing else parses, and -que even when something does
        (parse.adb, Enclitic)
      * the dictionary form, character for character
        (support_utils-dictionary_form.adb)
    NOT ported (so an `unknown` here may still be a word WORDS would get):
      TRICKS (spelling tricks such as ii/i, medieval spellings), SLURY
      (assimilated prefixes), SYNCOPE, FIXES (prefix/suffix composition),
      PACKONs other than via UNIQUES, Roman numerals, and WORDS's
      frequency trimming. Every analysis is kept; none is discarded as rare.

    One gap is filled by the house and marked: WORDS prints NO dictionary form
    for pronouns of declension 1 (qui/quis) and 5 (ego/tu/nos/vos/sui) -- its
    dictionary_form raises Not_Found and returns "". HOUSE_PRONOUN_FORMS
    supplies the conventional heading for those entries, and every lemma
    built that way carries `form_by: "house"`.

LICENCE (verified 2026-09-26; recorded verbatim in the manifest)
    Not public domain. Copyright William A. Whitaker (1936-2010), with an
    unconditional grant: "Permission is hereby freely given for any and all
    use of program and data." See LICENCE below and pipeline/README-lemma-spine.md.
"""

import hashlib
import os
import re
import unicodedata
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

REPO_URL = "https://github.com/mk270/whitakers-words"
COMMIT = "1f2f0fb0867a896d7b9284a03d615ed635d6f992"
RAW = "https://raw.githubusercontent.com/mk270/whitakers-words/" + COMMIT + "/"
VERSION = "WORDS 1.97F data (mk270 port)"
CACHE = os.path.join(ROOT, "data", "corpus", "whitaker", COMMIT[:12])

# sha256 of each file at COMMIT, measured 2026-09-26. A mismatch is a hard stop.
PINS = {
    "DICTLINE.GEN": "8f6c0fc84d12859abc863eac84ddd49b7e039503855ca34c1d44a6e78abf7569",
    "INFLECTS.LAT": "dd0f019669719d820f690a6199286f6f54addfb06e959a7592699f8c7e6d2a9b",
    "UNIQUES.LAT": "ed81efca10ec23d96e992724a98538c820f489b6ea3658afb1356ce6d2f7c8e2",
    "ADDONS.LAT": "7a7f40b3020913882e8bfa156ebe01ee3f640b4505ef2b79c8836ef6b8a948fb",
    "LICENCE.txt": "de533c3fb7c4a54b6d2deb5e56624947850bd2121c1de206ba5ee59b72c119a3",
}

LICENCE = {
    "license": "free-grant",
    "license_basis": ("Copyright William A. Whitaker (1936-2010), with an unconditional grant "
                      "of any and all use of program and data. Not public domain."),
    "grant_verbatim": [
        ("This is a free program, which means it is proper to copy it and pass it on to your "
         "friends. Consider it a developmental item for which there is no charge. However, just "
         "for form, it is Copyrighted (c). Permission is hereby freely given for any and all use "
         "of program and data. You can sell it as your own, but at least tell me."),
        ("All parts of the WORDS system, source code and data files, are made freely available "
         "to anyone who wishes to use them, for whatever purpose."),
    ],
    "evidence": [
        {"what": "the author's own documentation, WORDS 1.97F (sections 'Licence' and the program notice)",
         "url": "http://web.archive.org/web/20101227020317/http://users.erols.com/whitaker/wordsdoc.htm",
         "sha256": "67cd077c01defdd81480ede38d798551050dcd30a13a83a1ef19be80a9c608fe",
         "note": ("also: 'The source and data are freely available for anyone to use for any "
                  "purpose. It may be converted to other languages, used in pieces, or modified "
                  "in any way without further permission or notification.'")},
        {"what": "LICENCE.txt in the maintained port, at the pinned commit",
         "url": RAW + "LICENCE.txt",
         "sha256": PINS["LICENCE.txt"]},
    ],
    "verified": True,
    "verified_on": "2026-09-26",
    "attribution": "WORDS, a Latin dictionary, by Colonel William Whitaker (USAF, Retired)",
    "open": ("The grant is not the house's PD-or-own gate (launch plan D4 / ADR 0001). It is "
             "admitted here as its own class, `free-grant`, pending Adam's ruling. The grant "
             "asks, as a courtesy, 'at least tell me'; the author died in 2010."),
}

DATA_FILES = ("DICTLINE.GEN", "INFLECTS.LAT", "UNIQUES.LAT", "ADDONS.LAT", "LICENCE.txt")


# ---------------------------------------------------------------------------
# Fetch (pinned, verified, resumable)
# ---------------------------------------------------------------------------

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def fetch(cache=CACHE, quiet=False):
    os.makedirs(cache, exist_ok=True)
    for fn in DATA_FILES:
        p = os.path.join(cache, fn)
        if os.path.exists(p) and sha256(p) == PINS[fn]:
            continue
        if not quiet:
            print(f"  fetch {fn}")
        with urllib.request.urlopen(RAW + fn, timeout=120) as r:
            blob = r.read()
        got = hashlib.sha256(blob).hexdigest()
        if got != PINS[fn]:
            raise SystemExit(f"HARD STOP: {fn} sha256 {got} != pinned {PINS[fn]}")
        tmp = p + ".tmp"
        with open(tmp, "wb") as f:
            f.write(blob)
        os.replace(tmp, p)
    return cache


def have_cache(cache=CACHE):
    return all(os.path.exists(os.path.join(cache, fn)) for fn in DATA_FILES)


def verify_cache(cache=CACHE):
    bad = [fn for fn in DATA_FILES if sha256(os.path.join(cache, fn)) != PINS[fn]]
    if bad:
        raise SystemExit(f"HARD STOP: cached Whitaker files differ from the pins: {bad}")


# ---------------------------------------------------------------------------
# Folding: WORDS treats u=v and i=j, and ignores case.
# ---------------------------------------------------------------------------

def fold(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower()
    s = s.replace("æ", "ae").replace("œ", "oe")
    return s.translate(str.maketrans("jv", "iu"))


# ---------------------------------------------------------------------------
# DICTLINE.GEN
# ---------------------------------------------------------------------------

def _part(tokens):
    """The part-of-speech entry of a DICTLINE line, as a dict."""
    pos = tokens[0]
    t = tokens[1:]
    if pos == "N":
        return {"pos": pos, "decl": (int(t[0]), int(t[1])), "gender": t[2], "kind": t[3]}
    if pos in ("PRON", "PACK"):
        return {"pos": pos, "decl": (int(t[0]), int(t[1])), "kind": t[2]}
    if pos == "ADJ":
        return {"pos": pos, "decl": (int(t[0]), int(t[1])), "co": t[2]}
    if pos == "NUM":
        return {"pos": pos, "decl": (int(t[0]), int(t[1])), "sort": t[2], "value": int(t[3])}
    if pos == "V":
        return {"pos": pos, "decl": (int(t[0]), int(t[1])), "kind": t[2]}
    if pos == "ADV":
        return {"pos": pos, "co": t[0]}
    if pos == "PREP":
        return {"pos": pos, "case": t[0]}
    return {"pos": pos}


def load_dictline(path):
    """One entry per dictionary item. A meaning that starts with '|' continues
    the entry above it (same stems, same part): it is folded into that entry."""
    entries = []
    with open(path, encoding="latin-1", newline="") as f:
        lines = f.read().splitlines()
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        stems = [line[i:i + 19].strip() for i in range(0, 76, 19)]
        part_text = " ".join(line[76:100].split())
        flags = line[100:110].split()
        meaning = line[110:].rstrip()
        if meaning.startswith("|") and entries and entries[-1]["stems"] == stems \
                and entries[-1]["part_text"] == part_text:
            entries[-1]["meaning"] += " " + meaning[1:].strip()
            entries[-1]["lines"].append(n)
            continue
        entries.append({"lines": [n], "stems": stems, "part_text": part_text,
                        "part": _part(part_text.split()),
                        "flags": dict(zip(("age", "area", "geo", "freq", "source"), flags)),
                        "meaning": meaning.strip()})
    return entries


# WORDS has no DICTLINE line for `sum`: makedict_main.adb inserts it into the
# general dictionary as it builds (stems s / blank / fu / fut, V 5 1 TO_BE).
# Ported as that program writes it.
ESSE = {"lines": [], "stems": ["s", "", "fu", "fut"], "part_text": "V 5 1 TO_BE",
        "part": {"pos": "V", "decl": (5, 1), "kind": "TO_BE"},
        "flags": {"age": "X", "area": "X", "geo": "X", "freq": "A", "source": "X"},
        "meaning": "be; exist; (also used to form verb perfect passive tenses) with NOM PERF PPL",
        "synthetic": "makedict_main.adb (ESSE)"}


# ---------------------------------------------------------------------------
# INFLECTS.LAT
# ---------------------------------------------------------------------------

# fields before `key len [ending] age freq`, per part of speech
QUAL = {
    "N": ("which", "var", "case", "number", "gender"),
    "PRON": ("which", "var", "case", "number", "gender"),
    "ADJ": ("which", "var", "case", "number", "gender", "comparison"),
    "NUM": ("which", "var", "case", "number", "gender", "sort"),
    "V": ("which", "var", "tense", "voice", "mood", "person", "number"),
    "VPAR": ("which", "var", "case", "number", "gender", "tense", "voice", "mood"),
    "SUPINE": ("which", "var", "case", "number", "gender"),
    "ADV": ("comparison",),
    "PREP": ("case",),
    "CONJ": (),
    "INTERJ": (),
}


def _qual(pos, vals):
    q = {"pos": pos}
    for name, v in zip(QUAL[pos], vals):
        q[name] = int(v) if name in ("which", "var", "person") else v
    if "which" in q:
        q["decl"] = (q.pop("which"), q.pop("var"))
    return q


def load_inflects(path):
    out = []
    with open(path, encoding="latin-1") as f:
        for n, raw in enumerate(f, 1):
            line = raw.split("--", 1)[0].strip()
            if not line:
                continue
            t = line.split()
            pos = t[0]
            k = len(QUAL[pos])
            q = _qual(pos, t[1:1 + k])
            key, size = int(t[1 + k]), int(t[2 + k])
            ending = t[3 + k] if size else ""
            if len(ending) != size:
                raise SystemExit(f"INFLECTS.LAT:{n}: ending {ending!r} is not {size} long")
            out.append({"line": n, "qual": q, "key": key, "ending": fold(ending)})
    return out


# ---------------------------------------------------------------------------
# UNIQUES.LAT and ADDONS.LAT
# ---------------------------------------------------------------------------

def load_uniques(path):
    with open(path, encoding="latin-1") as f:
        rows = [(n, l.rstrip("\r\n")) for n, l in enumerate(f, 1)]
    rows = [(n, l) for n, l in rows if l.strip() and not l.startswith("--")]
    out = []
    for i in range(0, len(rows) - 2, 3):
        (n, word), (_, qline), (_, meaning) = rows[i:i + 3]
        t = qline.split()
        pos = t[0]
        q = _qual(pos, t[1:1 + len(QUAL[pos])])
        out.append({"line": n, "word": word.strip(), "qual": q, "meaning": meaning.strip()})
    return out


def load_tackons(path):
    """The TACKON list in file order (WORDS's first four -- que, ne, ve, est --
    are the enclitics parse.adb tries)."""
    out = []
    with open(path, encoding="latin-1") as f:
        lines = [l.rstrip("\r\n") for l in f]
    for i, l in enumerate(lines):
        if l.startswith("TACKON "):
            parts = l.split()
            if len(parts) >= 2 and re.fullmatch(r"[a-z]+", parts[1]):
                out.append(parts[1])
    return out


# ---------------------------------------------------------------------------
# The dictionary form (a port of support_utils-dictionary_form.adb)
# ---------------------------------------------------------------------------

FST = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th"}

# The house completion for the pronoun headings WORDS does not print.
# Keyed by (stem 1, declension which, kind). Conventional dictionary headings.
HOUSE_PRONOUN_FORMS = {
    ("qu", 1, "REL"): "qui, quae, quod",
    ("qu", 1, "ADJECT"): "qui, quae, quod",
    ("qu", 1, "INTERR"): "quis, quid",
    ("qu", 1, "INDEF"): "quis, quid",
    ("aliqu", 1, "ADJECT"): "aliqui, aliqua, aliquod",
    ("aliqu", 1, "INDEF"): "aliquis, aliquid",
    ("ego", 5, "PERS"): "ego, mei",
    ("tu", 5, "PERS"): "tu, tui",
    ("n", 5, "PERS"): "nos, nostrum",
    ("v", 5, "PERS"): "vos, vestrum",
    ("zzz", 5, "REFLEX"): "-, sui",
}


def dictionary_form(e):
    """(form, form_by). form_by is 'whitaker' or 'house'."""
    s = e["stems"]
    p = e["part"]
    pos = p["pos"]
    w, v = p.get("decl", (0, 0))

    def add(stem, infl):
        return (stem.strip() + infl.strip())

    if pos == "PREP":
        return f"{s[0]}  PREP  {p['case']}", "whitaker"
    if s[1:] == ["", "", ""] and not (
            (pos == "N" and w == 9) or
            (pos == "ADJ" and (w == 9 or p["co"] in ("COMP", "SUPER"))) or
            (pos == "V" and (w, v) in ((9, 8), (9, 9)))):
        return f"{s[0]}  {pos}", "whitaker"

    ox = ["", "", "", ""]
    if pos == "N":
        tbl = {
            1: {1: ("a", "ae"), 6: ("e", "es"), 7: ("es", "ae"), 8: ("as", "ae")},
            2: {1: ("us", "i"), 2: ("um", "i"), 3: ("", "i"),
                4: ("um" if p["gender"] == "N" else "us", "(i)"),
                5: ("us", ""), 6: ("os", "i"), 7: ("", "yos/i"), 8: ("on", "i"), 9: ("us", "i")},
            4: {1: ("us", "us"), 2: ("u", "us"), 3: ("us", "u"), 4: ("", "u")},
        }
        if w in tbl:
            if v in tbl[w]:
                a, b = tbl[w][v]
                ox[0], ox[1] = add(s[0], a), add(s[1], b)
        elif w == 3:
            ox[0] = add(s[0], "")
            ox[1] = add(s[1], "os/is" if v in (7, 9) else "is")
        elif w == 5:
            ox[0], ox[1] = add(s[0], "es"), add(s[1], "ei")
        elif w == 9:
            if v == 8:
                ox[0], ox[1] = add(s[0], "."), "abb."
            elif v == 9:
                ox[0], ox[1] = add(s[0], ""), "undeclined"
        else:
            return "", "whitaker"
    elif pos == "PRON":
        if w == 3:
            ox[0], ox[1] = add(s[0], "ic"), add(s[0], "aec")
            ox[2] = add(s[0], "oc") if v == 1 else add(s[0], "uc") if v == 2 else ""
        elif w == 4:
            if v == 1:
                ox[:3] = add(s[0], "s"), add(s[1], "a"), add(s[0], "d")
            elif v == 2:
                ox[:3] = add(s[0], "dem"), add(s[1], "adem"), add(s[0], "dem")
        elif w == 6:
            ox[0], ox[1] = add(s[0], "e"), add(s[0], "a")
            ox[2] = add(s[0], "ud") if v == 1 else add(s[0], "um") if v == 2 else ""
        elif w == 9:
            if v == 8:
                ox[0], ox[1] = add(s[0], "."), "abb."
            elif v == 9:
                ox[0], ox[1] = add(s[0], ""), "undeclined"
        else:
            house = HOUSE_PRONOUN_FORMS.get((s[0], w, p["kind"]))
            return (f"{house}  PRON", "house") if house else ("", "whitaker")
    elif pos == "ADJ":
        co = p["co"]
        if co == "COMP":
            ox[:3] = add(s[0], "or"), add(s[0], "or"), add(s[0], "us")
        elif co == "SUPER":
            ox[:3] = add(s[0], "mus"), add(s[0], "ma"), add(s[0], "mum")
        elif co == "POS":
            if w == 1:
                t1 = {1: ("us", "a", "um"), 2: ("", "a", "um"), 3: ("us", "a", "um (gen -ius)"),
                      4: ("", "a", "um"), 5: ("us", "a", "ud")}
                if v not in t1:
                    return "", "whitaker"
                a, b, c = t1[v]
                ox[:3] = add(s[0], a), add(s[1], b), add(s[1], c)
            elif w == 2:
                t2 = {1: ("-", add(s[0], "e"), "-"), 2: ("-", "a", "-"),
                      3: (add(s[0], "es"), add(s[0], "es"), add(s[0], "es")),
                      6: (add(s[0], "os"), add(s[0], "os"), "-"),
                      7: (add(s[0], "os"), "-", "-"), 8: ("-", "-", add(s[1], "on"))}
                if v in t2:
                    ox[:3] = t2[v]
            elif w == 3:
                t3 = {1: (add(s[0], ""), "(gen.)", add(s[1], "is")),
                      2: (add(s[0], "is"), add(s[1], "is"), add(s[1], "e")),
                      3: (add(s[0], ""), add(s[1], "is"), add(s[1], "e")),
                      6: (add(s[0], ""), "(gen.)", add(s[1], "os"))}
                if v in t3:
                    ox[:3] = t3[v]
            elif (w, v) == (9, 8):
                ox[0], ox[1] = add(s[0], "."), "abb."
            elif (w, v) == (9, 9):
                ox[0], ox[1] = add(s[0], ""), "undeclined"
            else:
                return "", "whitaker"
        elif co == "X":
            cmp_, sup = add(s[2], "or -or -us"), add(s[3], "mus -a -um")
            if w == 1:
                if v == 1:
                    ox = [add(s[0], "us"), add(s[1], "a -um"), cmp_, sup]
                elif v == 2:
                    ox = [add(s[0], ""), add(s[1], "a -um"), cmp_, sup]
            elif w == 3:
                if v == 1:
                    ox = [add(s[0], ""), add(s[1], "is (gen.)"), cmp_, sup]
                elif v == 2:
                    ox = [add(s[0], "is"), add(s[1], "e"), cmp_, sup]
                elif v == 3:
                    ox = [add(s[0], ""), add(s[1], "is -e"), cmp_, sup]
            elif w == 9:
                ox = [add(s[0], ""), "undeclined", cmp_, sup]
            else:
                return "", "whitaker"
    elif pos == "ADV" and p["co"] == "X":
        ox[:3] = add(s[0], ""), add(s[1], ""), add(s[2], "")
    elif pos == "V":
        kind = p["kind"]
        if kind == "DEP":
            ox[2] = "DEP"
            ox[3] = add(s[3], "us sum")
            if w == 1:
                ox[0], ox[1] = add(s[0], "or"), add(s[1], "ari")
            elif w == 2:
                ox[0], ox[1] = add(s[0], "eor"), add(s[1], "eri")
            elif w == 3:
                ox[0] = add(s[0], "or")
                ox[1] = add(s[1], "iri") if v == 4 else add(s[1], "i")
            else:
                return "", "whitaker"
        elif kind == "PERFDEF":
            ox = [add(s[2], "i"), add(s[2], "isse"), add(s[3], "us"), ""]
        elif kind == "IMPERS" and s[0][:3] == "zzz" and s[1][:3] == "zzz":
            ox[:3] = add(s[2], "it"), add(s[2], "isse"), add(s[3], "us est")
        else:
            if kind == "IMPERS":
                if w == 1:
                    ox[0] = add(s[0], "at")
                elif w == 2:
                    ox[0] = add(s[0], "et")
                elif w == 3:
                    if v == 2 or s[0].strip()[-1:] == "i":
                        ox[0] = add(s[0], "t")
                    else:
                        ox[0] = add(s[0], "it")
                elif w == 5 and v == 1:
                    ox[0] = add(s[0], "est")
                elif w == 7 and v in (1, 2):
                    ox[0] = add(s[0], "t")
            else:
                if w == 2:
                    ox[0] = add(s[0], "eo")
                elif w == 5:
                    ox[0] = add(s[0], "um")
                elif (w, v) == (7, 2):
                    ox[0] = add(s[0], "am")
                else:
                    ox[0] = add(s[0], "o")
            if w == 1:
                ox[1] = add(s[1], "are")
            elif w == 2:
                ox[1] = add(s[1], "ere")
            elif w == 3:
                if v == 2:
                    ox[1] = add(s[1], "re")
                elif v == 3:
                    ox[1] = add(s[1], "ieri") if s[1].strip() == "f" else add(s[1], "eri")
                elif v == 4:
                    ox[1] = add(s[1], "ire")
                else:
                    ox[1] = add(s[1], "ere")
            elif w == 5:
                if v == 1:
                    ox[1] = add(s[1], "esse")
                elif v == 2:
                    ox[1] = add(s[0], "e")
            elif w == 6:
                if v == 1:
                    ox[1] = add(s[1], "re")
                elif v == 2:
                    ox[1] = add(s[1], "le")
            elif w == 7:
                if v == 3:
                    ox[1] = add(s[1], "se")
            elif w == 8:
                ox[1] = add(s[1], {1: "are", 2: "ere", 3: "ere", 4: "ire"}.get(v, "ere"))
            elif w == 9:
                if v == 8:
                    ox[0], ox[1] = add(s[0], "."), "abb."
                elif v == 9:
                    ox[0], ox[1] = add(s[0], ""), "undeclined"
            if kind == "IMPERS":
                ox[2] = add(s[2], "it")
                ox[3] = add(s[3], "us est")
            elif kind == "SEMIDEP":
                ox[3] = add(s[3], "us sum")
            elif (w, v) == (5, 1):
                ox[2], ox[3] = add(s[2], "i"), add(s[3], "urus")
            elif w == 8:
                ox[2], ox[3] = "additional", "forms"
            elif w == 9:
                ox[2], ox[3] = "BLANK", "BLANK"
            else:
                ox[2], ox[3] = add(s[2], "i"), add(s[3], "us")
        if (w, v) == (6, 1):
            ox[2] = ox[2] + "(ii)"
    elif pos == "NUM" and p["sort"] == "X":
        if w == 1:
            t = {1: ("us -a -um", "us -a -um", "i -ae -a", ""),
                 2: ("o -ae o", "us -a -um", "i -ae -a", ""),
                 3: ("es -es -ia", "us -a -um", "i -ae -a", ""),
                 4: ("i -ae -a", "us -a -um", "i -ae -a", "ie (n)s")}
            if v in t:
                ox = [add(s[i], t[v][i]) for i in range(4)]
        elif w == 2:
            ox = [add(s[0], ""), add(s[1], "us -a -um"), add(s[2], "i -ae -a"), add(s[3], "ie (n)s")]
    elif pos == "NUM" and p["sort"] == "CARD":
        if w == 1:
            t = {1: ("us", "a", "um"), 2: ("o", "ae", "o"), 3: ("es", "es", "ia"), 4: ("i", "ae", "a")}
            if v in t:
                ox[:3] = [add(s[0], x) for x in t[v]]
        elif w == 2:
            ox[0] = add(s[0], "")
    elif pos == "NUM" and p["sort"] == "ORD":
        ox[:3] = add(s[0], "us"), add(s[0], "a"), add(s[0], "um")
    elif pos == "NUM" and p["sort"] == "DIST":
        ox[:3] = add(s[0], "i"), add(s[0], "ae"), add(s[0], "a")
    else:
        ox[0] = add(s[0], "")

    form = ""
    if ox[0][:3] == "zzz":
        form = "-"
    elif ox[0]:
        form = ox[0]
    if ox[1][:3] == "zzz":
        form += ", -"
    elif ox[1]:
        form += ", " + ox[1]
    if ox[2][:3] == "zzz":
        form += ", -"
    elif ox[2][:3] == "DEP" or ox[2][:5] == "BLANK":
        pass
    elif ox[2]:
        form += ", " + ox[2]
    if ox[3][:3] == "zzz":
        form += ", -"
    elif ox[3][:5] == "BLANK":
        pass
    elif ox[3]:
        form += ", " + ox[3]
    form = form.strip() + "  " + pos
    if pos == "N":
        if 1 <= w <= 5 and 1 <= v <= 5:
            form += f" ({FST[w]})"
        form += " " + p["gender"]
    if pos == "V":
        if w in (1, 2, 3):
            if v == 1:
                form += f" ({FST[w]})"
            elif (w, v) == (3, 4):
                form += f" ({FST[4]})"
        if p["kind"] in ("GEN", "DAT", "ABL", "TRANS", "INTRANS", "IMPERS", "DEP", "SEMIDEP", "PERFDEF"):
            form += " " + p["kind"]
    return form.strip(), "whitaker"


def headword_of(form):
    """The first principal part of a dictionary form, folded, for comparison."""
    parts = form.split("  ", 1)[0].split(",")
    for p in parts:
        p = p.strip()
        if p and p != "-":
            return fold(p.split()[0])
    return ""


def principal_parts(form):
    return form.split("  ", 1)[0].strip()


# ---------------------------------------------------------------------------
# The analyzer
# ---------------------------------------------------------------------------

def decn_le(left, right):
    """inflections_package.adb: an inflection's (which, var) contains the
    dictionary entry's when equal, (0,0) (except for which 9), or (which, 0)."""
    return right == left or (right == (0, 0) and left[0] != 9) or right == (left[0], 0)


def gender_le(left, right):
    return right == left or (right == "C" and left != "N") or right == "X"


def comp_le(left, right):
    return right == left or right == "X"


EFF_POS = {"VPAR": "V", "SUPINE": "V"}
MOOD_ORDER = ("X", "IND", "SUB", "IMP", "INF", "PPL")


def adj_comp_from_key(key):
    return {1: "POS", 2: "POS", 3: "COMP", 4: "SUPER"}.get(key, "X")


class Whitaker:
    def __init__(self, cache=CACHE):
        verify_cache(cache)
        self.cache = cache
        self.entries = load_dictline(os.path.join(cache, "DICTLINE.GEN"))
        self.inflects = load_inflects(os.path.join(cache, "INFLECTS.LAT"))
        self.uniques = load_uniques(os.path.join(cache, "UNIQUES.LAT"))
        self.tackons = load_tackons(os.path.join(cache, "ADDONS.LAT"))
        self.entries.append(ESSE)
        self.stem_index = {}
        for i, e in enumerate(self.entries):
            if e["part"]["pos"] == "PACK":
                continue          # PACKONs are reached only through UNIQUES here
            for k, st in enumerate(e["stems"], 1):
                if st != "zzz" and (st or e is ESSE):
                    self.stem_index.setdefault(fold(st), []).append((i, k))
        self.by_ending = {}
        for inf in self.inflects:
            self.by_ending.setdefault(inf["ending"], []).append(inf)
        self._forms = {}

    # -- lemma identity ---------------------------------------------------
    def form(self, i):
        if i not in self._forms:
            self._forms[i] = dictionary_form(self.entries[i])
        return self._forms[i]

    # -- matching ---------------------------------------------------------
    def _match(self, e, k, stem, inf):
        p, q = e["part"], inf["qual"]
        ipos = q["pos"]
        if EFF_POS.get(ipos, ipos) != p["pos"]:
            return None
        if not (inf["key"] == k or inf["key"] == 0):
            return None
        pos = p["pos"]
        if pos == "N":
            if decn_le(p["decl"], q["decl"]) and gender_le(p["gender"], q["gender"]):
                return {"pos": "N", "decl": p["decl"], "case": q["case"], "number": q["number"],
                        "gender": p["gender"]}
        elif pos == "PRON":
            if decn_le(p["decl"], q["decl"]):
                return {"pos": "PRON", "decl": p["decl"], "case": q["case"], "number": q["number"],
                        "gender": q["gender"]}
        elif pos == "ADJ":
            if decn_le(p["decl"], q["decl"]) and (comp_le(q["comparison"], p["co"]) or
                                                  q["comparison"] == "X" or p["co"] == "X"):
                com = p["co"] if p["co"] in ("POS", "COMP", "SUPER") else adj_comp_from_key(k)
                return {"pos": "ADJ", "decl": p["decl"], "case": q["case"], "number": q["number"],
                        "gender": q["gender"], "comparison": com}
        elif pos == "NUM":
            if decn_le(p["decl"], q["decl"]) and inf["key"] == k:
                return {"pos": "NUM", "decl": p["decl"], "case": q["case"], "number": q["number"],
                        "gender": q["gender"], "sort": p["sort"] if p["sort"] != "X" else
                        {1: "CARD", 2: "ORD", 3: "DIST", 4: "ADVERB"}.get(k, "X")}
        elif pos == "ADV":
            if comp_le(p["co"], q["comparison"]) or q["comparison"] == "X" or p["co"] == "X":
                com = p["co"] if p["co"] in ("POS", "COMP", "SUPER") else adj_comp_from_key(k)
                return {"pos": "ADV", "comparison": com}
        elif pos == "V":
            if not decn_le(p["decl"], q["decl"]):
                return None
            if ipos == "V":
                a = {"pos": "V", "decl": p["decl"], "tense": q["tense"], "voice": q["voice"],
                     "mood": q["mood"], "person": q["person"], "number": q["number"]}
                return a if self._allowed_verb(e, stem, a, inf) else None
            if ipos == "VPAR":
                return {"pos": "VPAR", "decl": p["decl"], "case": q["case"], "number": q["number"],
                        "gender": q["gender"], "tense": q["tense"], "voice": q["voice"], "mood": "PPL"}
            if ipos == "SUPINE":
                return {"pos": "SUPINE", "decl": p["decl"], "case": q["case"], "number": q["number"],
                        "gender": q["gender"]}
        elif pos == "PREP":
            if p["case"] == q["case"]:
                return {"pos": "PREP", "case": q["case"]}
        elif pos in ("CONJ", "INTERJ"):
            return {"pos": pos}
        return None

    @staticmethod
    def _allowed_verb(e, stem, a, inf):
        """list_sweep.adb, Allowed_Stem, for V."""
        kind = e["part"]["kind"]
        if (a["decl"], a["tense"], a["voice"], a["mood"], a["person"], a["number"]) == \
                ((3, 1), "PRES", "ACTIVE", "IMP", 2, "S") and inf["ending"] == "":
            if stem[-3:] not in ("dic", "duc", "fac", "fer"):
                return False
        if a["mood"] == "IMP" and not ((a["tense"] == "PRES" and a["person"] == 2) or
                                       (a["tense"] == "FUT" and a["person"] in (2, 3))):
            return False
        if kind == "IMPERS" and a["person"] != 3:
            return False
        mi = MOOD_ORDER.index(a["mood"]) if a["mood"] in MOOD_ORDER else 0
        if kind == "DEP":
            if a["voice"] == "ACTIVE" and a["mood"] == "INF" and a["tense"] == "FUT":
                pass
            elif a["voice"] == "ACTIVE" and 1 <= mi <= 4:
                return False
        if kind == "SEMIDEP" and 1 <= mi <= 3 and (
                (a["voice"] == "PASSIVE" and a["tense"] in ("PRES", "IMPF", "FUT")) or
                (a["voice"] == "ACTIVE" and a["tense"] in ("PERF", "PLUP", "FUTP"))):
            return False
        return True

    def _word(self, w):
        out = []
        seen = set()
        for u in self.uniques:
            if fold(u["word"]) == w:
                out.append({"entry": None, "unique": u, "parse": dict(u["qual"])})
        for cut in range(0, min(len(w), 8) + 1):
            ending = w[len(w) - cut:] if cut else ""
            stem = w[:len(w) - cut]
            if ending not in self.by_ending or stem not in self.stem_index:
                continue
            for (i, k) in self.stem_index.get(stem, ()):
                e = self.entries[i]
                for inf in self.by_ending[ending]:
                    a = self._match(e, k, stem, inf)
                    # one analysis per (entry, parse): INFLECTS lists some
                    # endings twice (variant spellings, ages); WORDS shows one.
                    if a and (i, repr(sorted(a.items()))) not in seen:
                        seen.add((i, repr(sorted(a.items()))))
                        out.append({"entry": i, "unique": None, "parse": a,
                                    "inflect_line": inf["line"], "stem_key": k})
        return out

    def analyze(self, word):
        """Every WORDS analysis of `word`, as dicts. Deterministic order."""
        w = fold(word)
        res = self._word(w)
        # parse.adb, Enclitic: with a parse in hand only -que is tried; without
        # one, que/ne/ve/est in turn, stopping at the first that strips.
        encl = ("que",) if res else tuple(self.tackons[:4])
        for t in encl:
            if w.endswith(t) and len(w) > len(t):
                more = self._word(w[:-len(t)])
                for a in more:
                    a["enclitic"] = t
                res += more
                break
        return [self._describe(a) for a in res]

    def _describe(self, a):
        p = {k: (list(v) if isinstance(v, tuple) else v) for k, v in a["parse"].items()}
        if a["unique"] is not None:
            u = a["unique"]
            key = f"{u['word']}  {u['qual']['pos']}  (UNIQUES)"
            return {"key": key, "lemma": u["word"], "form_by": "whitaker-unique",
                    "headword": fold(u["word"]), "parse": p, "whitaker": _qual_text(p),
                    "enclitic": a.get("enclitic"), "source": f"UNIQUES.LAT:{u['line']}"}
        form, by = self.form(a["entry"])
        e = self.entries[a["entry"]]
        return {"key": form or f"{e['stems'][0]}  {e['part_text']}", "lemma": principal_parts(form) or None,
                "form_by": by, "headword": headword_of(form) if form else fold(e["stems"][0]),
                "parse": p, "whitaker": _qual_text(p), "enclitic": a.get("enclitic"),
                "source": f"DICTLINE.GEN:{e['lines'][0]}" if e["lines"] else e["synthetic"],
                "inflect": f"INFLECTS.LAT:{a['inflect_line']}"}


def _qual_text(p):
    """The parse as WORDS prints it, e.g. `V 1 1 PRES ACTIVE IND 1 S`."""
    order = {
        "N": ("decl", "case", "number", "gender"),
        "PRON": ("decl", "case", "number", "gender"),
        "ADJ": ("decl", "case", "number", "gender", "comparison"),
        "NUM": ("decl", "case", "number", "gender", "sort"),
        "V": ("decl", "tense", "voice", "mood", "person", "number"),
        "VPAR": ("decl", "case", "number", "gender", "tense", "voice", "mood"),
        "SUPINE": ("decl", "case", "number", "gender"),
        "ADV": ("comparison",),
        "PREP": ("case",),
    }.get(p["pos"], ())
    bits = [p["pos"]]
    for f in order:
        v = p.get(f)
        if isinstance(v, list):
            bits += [str(x) for x in v]
        elif v is not None:
            bits.append(str(v))
    return " ".join(bits)
