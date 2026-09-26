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
    via      An analysis WORDS reached only by a rule (a spelling trick,
             syncope, a prefix or suffix) says so in `via`; a lemma taken
             from one records it. WORDS's two-words guesses ("If not obvious,
             probably incorrect") are never taken: a form with nothing else
             stays `unknown`, the guess recorded.

OVERRIDES (Adam's answers to the review sheet)
    data/lemmas/adam-reviewed.jsonl, one row per token address. `load_overrides`
    validates the file; `apply_override` puts a row onto a resolved token with
    provenance `adam-reviewed`, keeping the draft and what it replaced.
"""

import json
import os
import re

from whitaker import fold

SPINE_SOURCE = "whitaker-words"
DRAFT_SOURCE = "house-draft-2026-09-14"
OVERRIDE_SOURCE = "adam-reviewed"
OVERRIDES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "data", "lemmas", "adam-reviewed.jsonl")

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
    # "conj + subj" says what the conjunction governs, not the word's mood
    s = re.sub(r"\+ subj\b", "", s)
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
    if re.search(r"\bindecl\b", s):
        put("decl", (9, None))
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


VOCAB = (set(CASES) | set(TENSES) | set(MOODS) |
         {"sg", "pl", "m", "f", "n", "act", "pass", "decl", "conj", "adv", "prep", "pron",
          "pers", "rel", "noun", "adj", "ptc", "deponent", "comparative", "superlative",
          "interjection", "indecl", "reflexive", "st", "nd", "rd", "th"})


def annotations(parsing):
    """Words in the draft's parsing that are not parse features -- teaching
    notes such as `impersonal`, `(-io)`, `postpos`, `+ subj`. A draft that
    carries them is kept verbatim even where Whitaker confirms it."""
    s = (parsing or "").lower()
    extra = [w for w in re.findall(r"[^\W\d_]+", s) if w not in VOCAB]
    if re.search(r"conj \+ subj", s):
        extra.append("+ subj")
    return extra


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
                   if x not in (None, "X", "C"))
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


def lemma_hints(draft_lemma):
    """What the draft's lemma says beyond its headword: a part of speech (a
    gender tag means a noun; -a/-um or -e endings an adjective) and its other
    principal parts. Used only to choose among Whitaker entries that share
    the draft's headword -- never to overrule Whitaker."""
    s = draft_lemma or ""
    pos = None
    if re.search(r"(^|\s)[mfn]\.(\s|$)", s):
        pos = {"N"}
    elif re.search(r"-a,\s*-um|,\s*-e$|-ae,\s*-a", s):
        pos = {"ADJ"}
    parts = [fold(x.strip()).lstrip("-") for x in s.split(",")[1:]]
    parts = [re.sub(r"[^a-z]", "", x.split()[0]) for x in parts if x.split()]
    return pos, [x for x in parts if len(x) >= 2]


def _narrow(cands, draft_lemma):
    """Soft filters, in order; each applies only if it leaves someone."""
    pos, parts = lemma_hints(draft_lemma)
    if len({a["key"] for a in cands}) > 1 and pos:
        c = [a for a in cands if a["pos"] in pos]
        cands = c or cands
    if len({a["key"] for a in cands}) > 1 and parts:
        def score(a):
            have = re.split(r"[,\s]+", fold(a["lemma"] or ""))
            return sum(1 for p in parts if any(h.endswith(p) for h in have))
        best = max(score(a) for a in cands)
        if best:
            cands = [a for a in cands if score(a) == best]
    if len({a["key"] for a in cands}) > 1 and draft_lemma:
        lower = draft_lemma.strip()[:1].islower()
        c = [a for a in cands if (a["lemma"] or a["key"])[:1].islower() == lower]
        cands = c or cands
    return cands


def _parse_id(a):
    return (a["whitaker"], a.get("enclitic"))


def _kinds(a):
    return {v["kind"] for v in a.get("via") or []}


def _named(a):
    """How a disagreeing Whitaker reading is listed: its lemma, and the rule
    that reached it when there was one."""
    name = a["lemma"] or a["key"]
    fx = [f"{v['kind'].lower()} -{v['fix']}" for v in a.get("via") or [] if v["kind"] in ("PREFIX", "SUFFIX")]
    return name + (f" (by {', '.join(fx)})" if fx else "")


# -- the resolver --------------------------------------------------------------

def resolve(draft_lemma, draft_parsing, analyses):
    """Returns (lemma, lemma_key, parsing, provenance, review). review is a
    list of reasons for Adam, or None."""
    review = []
    hw = draft_headword(draft_lemma)
    feats = draft_features(draft_parsing)
    guesses = [a for a in analyses or [] if "TWO_WORDS" in _kinds(a)]
    A = [a for a in analyses or [] if "TWO_WORDS" not in _kinds(a)]
    H = [a for a in A if a["headword"] == hw]
    C = [a for a in H if consistent(a["parse"], feats)]
    keys_A = sorted({a["key"] for a in A})

    lp = {"source": SPINE_SOURCE, "draft": draft_lemma, "candidates": len(keys_A)}
    pp = {"source": SPINE_SOURCE, "draft": draft_parsing}
    lemma, key, parsing = draft_lemma, None, draft_parsing

    if not A:
        lp.update(status="unknown", source=DRAFT_SOURCE,
                  note="WORDS (as ported here) has no analysis of this form")
        if guesses:
            lp["note"] = "WORDS has only a two-words guess, which is never taken"
            two = [(v["as"], v["part"], g["lemma"] or g["key"])
                   for g in guesses for v in g["via"] if v["kind"] == "TWO_WORDS"]
            lp["whitaker_guess"] = [f"{s} part {n}: {l}" for s, n, l in sorted(set(two))]
        pp.update(status="unchecked", source=DRAFT_SOURCE)
        review.append("lemma: Whitaker has no analysis")
    elif not H:
        lp.update(status="disagree", source=DRAFT_SOURCE,
                  whitaker=sorted({_named(a) for a in A}))
        pp.update(status="unchecked", source=DRAFT_SOURCE)
        if all(_kinds(a) & {"PREFIX", "SUFFIX"} for a in A):
            review.append("lemma: Whitaker reaches this form only by prefix/suffix word formation")
        else:
            review.append("lemma: Whitaker's headword differs from the draft's")
    else:
        pick = sorted({a["key"] for a in _narrow(C if C else H, draft_lemma)})
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
            if all(a.get("via") for a in mine):
                # the lemma is Whitaker's only by a rule: say which
                lp["via"] = mine[0]["via"]
            parses = sorted({_parse_id(a) for a in mine})
            ok = sorted({_parse_id(a) for a in mine if consistent(a["parse"], feats)})
            pp["whitaker_parses"] = len(parses)
            # Whitaker's parse replaces the draft only when Whitaker gives one
            # and the draft committed to one value per feature it names
            # ("voc sg (= nom)" names two cases: the draft stays).
            single = all(len(v) == 1 for k, v in feats.items() if k != "pos")
            if len(parses) == 1 and ok and single:
                a = mine[0]
                notes = annotations(draft_parsing)
                if notes:
                    pp.update(status="confirmed", source=DRAFT_SOURCE, whitaker=a["whitaker"],
                              kept_for=notes)
                else:
                    dep = key.endswith(" DEP")
                    parsing = render(a["parse"], deponent=dep, enclitic=a.get("enclitic"))
                    pp.update(status="whitaker", whitaker=a["whitaker"])
            elif ok:
                pp.update(status="draft-consistent", source=DRAFT_SOURCE,
                          consistent=len(ok))
            else:
                pp.update(status="disagree", source=DRAFT_SOURCE,
                          whitaker=[p[0] + (f" +{p[1]}" if p[1] else "") for p in parses])
                review.append("parsing: no Whitaker parse agrees with the draft")
    return lemma, key, parsing, {"lemma": lp, "parsing": pp}, (review or None)


# -- Adam's overrides (README-lemma-spine.md s.8) -------------------------------

OVERRIDE_KEYS = {"address", "surface", "lemma", "lemma_key", "parsing", "reviewed_on", "note"}


def load_overrides(path=OVERRIDES):
    """{token address: row}. A missing file is no overrides. Any malformed
    row is a hard stop: an answer that cannot be applied must not be dropped."""
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            where = f"{os.path.basename(path)}:{n}"
            extra = set(row) - OVERRIDE_KEYS
            if extra:
                raise ValueError(f"{where}: unknown fields {sorted(extra)}")
            for k in ("address", "surface", "reviewed_on"):
                if not isinstance(row.get(k), str) or not row[k]:
                    raise ValueError(f"{where}: `{k}` is required")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["reviewed_on"]):
                raise ValueError(f"{where}: reviewed_on must be YYYY-MM-DD")
            if not {"lemma", "lemma_key", "parsing"} & set(row):
                raise ValueError(f"{where}: sets none of lemma, lemma_key, parsing")
            if row["address"] in out:
                raise ValueError(f"{where}: {row['address']} is overridden twice")
            out[row["address"]] = row
    return out


def apply_override(resolved, surface, analyses, ov):
    """Put one of Adam's answers onto a token `resolve` has already settled.

    `resolved` is resolve()'s (lemma, lemma_key, parsing, provenance, review).
    The row may set `lemma_key` alone (take that Whitaker entry: it must be one
    of Whitaker's analyses of this form, and its principal parts become the
    lemma), `lemma` with or without a `lemma_key`, and/or `parsing`. What it
    does not set is left as resolved. The replaced provenance is kept under
    `was`, and the draft stays recorded. Review reasons for what Adam answered
    are cleared; any others stand."""
    lemma, key, parsing, prov, review = resolved
    if ov["surface"] != surface:
        raise ValueError(f"{ov['address']}: override is for {ov['surface']!r}, the token is {surface!r}")
    prov = {k: dict(v) for k, v in prov.items()}
    stamp = {"source": OVERRIDE_SOURCE, "status": OVERRIDE_SOURCE, "reviewed_on": ov["reviewed_on"]}
    if ov.get("note"):
        stamp["note"] = ov["note"]
    done = set()
    if "lemma" in ov or "lemma_key" in ov:
        new_key = ov.get("lemma_key")
        if new_key is not None:
            mine = [a for a in analyses or [] if a["key"] == new_key]
            if not mine:
                raise ValueError(f"{ov['address']}: lemma_key {new_key!r} is not one of Whitaker's "
                                 "analyses of this form")
        new_lemma = ov["lemma"] if "lemma" in ov else (mine[0]["lemma"] or new_key)
        if not new_lemma:
            raise ValueError(f"{ov['address']}: lemma may not be empty")
        was = {"value": lemma, "lemma_key": key, **prov["lemma"]}
        prov["lemma"] = {**stamp, "draft": prov["lemma"]["draft"], "was": was}
        lemma, key = new_lemma, new_key
        done.add("lemma:")
    if "parsing" in ov:
        if not ov["parsing"]:
            raise ValueError(f"{ov['address']}: parsing may not be empty")
        was = {"value": parsing, **prov["parsing"]}
        prov["parsing"] = {**stamp, "draft": prov["parsing"]["draft"], "was": was}
        parsing = ov["parsing"]
        done.add("parsing:")
    left = [r for r in review or [] if not any(r.startswith(d) for d in done)]
    return lemma, key, parsing, prov, (left or None)
