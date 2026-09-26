#!/usr/bin/env python3
"""
lemma_spine.py -- set a token's `lemma` and `parsing` from Whitaker, against
the house draft, without ever overwriting silently. Launch plan D3.

    resolve(surface, draft_lemma, draft_parsing, analyses) -> (lemma, lemma_key,
                                                            parsing, provenance, review)

`analyses` is the committed Whitaker analysis row for the token's search_key
(data/lemmas/whitaker-la/hymns.analyses.jsonl, built by build_lemma_spine.py).
Pure function: no files, no network, so the hymn build stays offline.

THE RULE (pipeline/README-lemma-spine.md s.3)
    lemma    Whitaker's lemma is taken only when its headword is the draft's
             headword, and the draft's parsing picks out one Whitaker entry.
             Otherwise the draft stays and the token is flagged for review.
    parsing  Whitaker's parse is taken only when, for that entry, Whitaker
             gives exactly ONE parse and it is consistent with the draft.
             Several parses the draft is consistent with: the draft stays, not
             flagged. No consistent parse: the draft stays, flagged.
    Every token records both values (Whitaker's and the draft's) in
    `provenance`, so nothing is lost either way.
"""

import re

from whitaker import fold

SPINE_SOURCE = "whitaker-words"
DRAFT_SOURCE = "house-draft-2026-09-14"

# -- the draft, read as features ---------------------------------------------

CASES = {"nom": "NOM", "gen": "GEN", "dat": "DAT", "acc": "ACC", "abl": "ABL",
         "voc": "VOC", "loc": "LOC"}
TENSES = {"pres": "PRES", "impf": "IMPF", "fut": "FUT", "perf": "PERF",
          "plup": "PLUP", "futp": "FUTP"}
MOODS = {"ind": "IND", "subj": "SUB", "impv": "IMP", "inf": "INF", "ptc": "PPL",
         "gerundive": "PPL"}


def draft_headword(lemma):
    """`adōrō, -āre, ...` -> adoro; `ego (pl nōs)` -> ego; `fīō + -que` -> fio."""
    if not lemma:
        return ""
    head = re.split(r"[,(+]| ", lemma.strip(), 1)[0]
    return fold(head.strip())


def draft_features(parsing):
    """The features the draft's free-text parsing commits to. Only what it
    says: a feature it does not mention is not constrained."""
    s = (parsing or "").lower()
    words = re.findall(r"[a-z]+|\d", s)
    f = {}

    def put(k, v):
        f.setdefault(k, set()).add(v)

    for w in words:
        if w in CASES:
            put("case", CASES[w])
        elif w == "sg":
            put("number", "S")
        elif w == "pl":
            put("number", "P")
        elif w in ("m", "f", "n"):
            put("gender", w.upper())
        elif w in TENSES:
            put("tense", TENSES[w])
        elif w in MOODS:
            put("mood", MOODS[w])
        elif w == "act":
            put("voice", "ACTIVE")
        elif w == "pass":
            put("voice", "PASSIVE")
        elif w == "comparative":
            put("comparison", "COMP")
        elif w == "superlative":
            put("comparison", "SUPER")
    for m in re.finditer(r"\b([123]) (sg|pl)\b", s):
        put("person", int(m.group(1)))
    for m in re.finditer(r"\b(\d)(?:st|nd|rd|th)? (decl|conj)", s):
        n, what = int(m.group(1)), m.group(2)
        # Whitaker files the 4th conjugation as 3 4.
        put("decl", (3, 4) if (what == "conj" and n == 4) else (n, None))
    if "gerundive" in s:
        put("tense", "FUT")
        put("voice", "PASSIVE")
    if "deponent" in s:
        f.pop("voice", None)          # Whitaker parses deponent forms as passive
    # part of speech, where the draft names one
    pos = set()
    if re.search(r"\badv\b", s):
        pos.add("ADV")
    if re.search(r"\bprep\b", s):
        pos.add("PREP")
    if re.search(r"(?<!\d )\bconj\b", s):
        pos.add("CONJ")
    if "interjection" in s:
        pos.add("INTERJ")
    if re.search(r"\bnoun\b", s):
        pos.add("N")
    if re.search(r"\b(pron|rel|reflexive)\b", s):
        pos.add("PRON")
    if re.search(r"\badj\b", s):
        pos.add("ADJ")
    if "ptc" in s or "gerundive" in s:
        pos.add("VPAR")
    if pos:
        f["pos"] = pos
    return f


def consistent(parse, feats):
    """Every feature the draft names must be present in Whitaker's parse and
    agree with it. Whitaker's X is a wildcard; C (common) is m or f."""
    for k, want in feats.items():
        if k == "pos":
            if parse["pos"] not in want:
                return False
            continue
        if k == "decl":
            d = parse.get("decl")
            if d is None or not any(d[0] == w and (v is None or d[1] == v) for w, v in want):
                return False
            continue
        have = parse.get(k)
        if have is None:
            return False
        if have == "X":
            continue
        if k == "gender" and have == "C":
            if not want & {"M", "F"}:
                return False
            continue
        if have not in want:
            return False
    return True


# -- rendering a Whitaker parse in the house's abbreviations -----------------

AB = {"NOM": "nom", "GEN": "gen", "DAT": "dat", "ACC": "acc", "ABL": "abl", "VOC": "voc",
      "LOC": "loc", "S": "sg", "P": "pl", "M": "m", "F": "f", "N": "n", "C": "c",
      "PRES": "pres", "IMPF": "impf", "FUT": "fut", "PERF": "perf", "PLUP": "plup",
      "FUTP": "futp", "IND": "ind", "SUB": "subj", "IMP": "impv", "INF": "inf",
      "ACTIVE": "act", "PASSIVE": "pass"}
ORD = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}


def _ab(v):
    return AB.get(v, str(v).lower())


def render(parse, deponent=False, enclitic=None):
    p = parse
    pos = p["pos"]
    gcn = " ".join(_ab(x) for x in (p.get("gender"), p.get("case"), p.get("number"))
                   if x not in (None, "X"))
    if pos == "N":
        out = " ".join(_ab(x) for x in (p["case"], p["number"]) if x != "X")
        w = p["decl"][0]
        out = (out + ", " if out else "") + (f"{w} decl" if 1 <= w <= 5 else "indecl")
    elif pos in ("ADJ", "PRON", "NUM"):
        out = gcn
        if p.get("comparison") in ("COMP", "SUPER"):
            out = ("comparative, " if p["comparison"] == "COMP" else "superlative, ") + out
        if pos == "PRON":
            out = "pron, " + out
    elif pos == "V":
        w, v = p["decl"]
        if p["mood"] == "INF":
            out = f"{_ab(p['tense'])} inf"
        else:
            out = f"{p['person']} {_ab(p['number'])} {_ab(p['tense'])} {_ab(p['mood'])}"
        if deponent:
            out = "deponent, " + out
        else:
            out += " " + _ab(p["voice"])
        if (w, v) == (3, 4):
            out += ", 4 conj"
        elif 1 <= w <= 3:
            out += f", {w} conj"
    elif pos == "VPAR":
        if (p["tense"], p["voice"]) == ("FUT", "PASSIVE"):
            head = "gerundive"
        else:
            head = f"{_ab(p['tense'])} {_ab(p['voice'])} ptc"
            if deponent:
                head = f"{_ab(p['tense'])} ptc (deponent)"
        out = head + (", " + gcn if gcn else "")
    elif pos == "ADV":
        out = "adv" + {"COMP": ", comparative", "SUPER": ", superlative"}.get(p.get("comparison"), "")
    elif pos == "PREP":
        out = f"prep + {_ab(p['case'])}"
    elif pos == "CONJ":
        out = "conj"
    elif pos == "INTERJ":
        out = "interjection"
    else:
        out = pos.lower()
    if enclitic:
        out += f" + enclitic -{enclitic}"
    return out


def _parse_id(a):
    return (a["whitaker"], a.get("enclitic"))


# -- the resolver --------------------------------------------------------------

def resolve(draft_lemma, draft_parsing, analyses):
    """Returns (lemma, lemma_key, parsing, provenance, review). review is a
    list of reasons for Adam, or None."""
    review = []
    hw = draft_headword(draft_lemma)
    feats = draft_features(draft_parsing)
    A = analyses or []
    H = [a for a in A if a["headword"] == hw]
    C = [a for a in H if consistent(a["parse"], feats)]
    keys_A = sorted({a["key"] for a in A})
    keys_H = sorted({a["key"] for a in H})
    keys_C = sorted({a["key"] for a in C})

    lp = {"source": SPINE_SOURCE, "draft": draft_lemma, "candidates": len(keys_A)}
    pp = {"source": SPINE_SOURCE, "draft": draft_parsing}
    lemma, key, parsing = draft_lemma, None, draft_parsing

    if not A:
        lp.update(status="unknown", source=DRAFT_SOURCE,
                  note="WORDS (as ported here) has no analysis of this form")
        pp.update(status="unchecked", source=DRAFT_SOURCE)
        review.append("lemma: Whitaker has no analysis")
    elif not H:
        lp.update(status="disagree", source=DRAFT_SOURCE,
                  whitaker=sorted({a["lemma"] or a["key"] for a in A}))
        pp.update(status="unchecked", source=DRAFT_SOURCE)
        review.append("lemma: Whitaker's headword differs from the draft's")
    else:
        pick = keys_C if keys_C else keys_H
        if len(pick) != 1:
            lp.update(status="ambiguous", source=DRAFT_SOURCE, whitaker=pick)
            pp.update(status="unchecked", source=DRAFT_SOURCE)
            review.append("lemma: the draft's headword matches several Whitaker entries")
        else:
            key = pick[0]
            mine = [a for a in H if a["key"] == key]
            lemma = mine[0]["lemma"] or draft_lemma
            lp.update(status="agree" if len(keys_A) == 1 else "agree-selected",
                      form_by=mine[0]["form_by"], sources=mine[0]["sources"])
            parses = sorted({_parse_id(a) for a in mine})
            ok = sorted({_parse_id(a) for a in mine if consistent(a["parse"], feats)})
            pp["whitaker_parses"] = len(parses)
            if len(parses) == 1 and ok:
                a = mine[0]
                dep = key.endswith(" DEP")
                parsing = render(a["parse"], deponent=dep, enclitic=a.get("enclitic"))
                pp.update(status="agree-unique", whitaker=a["whitaker"])
            elif ok:
                pp.update(status="draft-consistent", source=DRAFT_SOURCE,
                          consistent=len(ok))
            else:
                pp.update(status="disagree", source=DRAFT_SOURCE,
                          whitaker=[p[0] + (f" +{p[1]}" if p[1] else "") for p in parses])
                review.append("parsing: no Whitaker parse agrees with the draft")
    return lemma, key, parsing, {"lemma": lp, "parsing": pp}, (review or None)
