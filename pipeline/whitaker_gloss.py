#!/usr/bin/env python3
# prov: 2026-09-26 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
# fable_review: pending
"""
whitaker_gloss.py -- a DICTIONARY gloss for a Latin token, from the English
meaning line of its Whitaker's WORDS entry, by a fixed rule. The Latin twin of
strongs_gloss.py. Never a contextual translation, and never invented: where no
rule fires, the gloss is null and the build counts it with the reason.

    lemmas = load_lemmas(path)                     # {WORDS key: lemma-table row}
    gloss, prov = gloss_for(token, lemmas)

Pure functions over the committed lemma table (data/lemmas/whitaker-la/
hymns.lemmas.jsonl, which carries each entry's DICTLINE meaning): no network,
no Whitaker cache needed. Rules and counts: pipeline/README-hymn-jsonl.md s.11.

WHAT A WORDS ENTRY GIVES
    One meaning line per DICTLINE entry, senses separated by ";", alternatives
    within a sense by "," or "/", notes in (parentheses) and [brackets]
    ("(PASS) seem", "[fiat => so be it]"). WORDS puts a word's first sense
    first, but not by frequency: laudo's is "recommend", sacramentum's a
    Roman legal deposit. The rule does not try to rescue those; the override
    layer does (below).

WHICH ENTRY
    The token's `lemma_key` names one WORDS dictionary form; the first DICTLINE
    entry under it (WORDS's own line order) is read. A token with a lemma but
    no key (status `same-lemma`: every WORDS entry for the form has one
    headword, e.g. `in` PREP ABL / ACC) is glossed only when every candidate
    entry gives the same gloss; otherwise null, with the candidates' glosses
    in the reason. A token with no lemma gets no gloss.

THE RULE, in order; the first that fires sets the gloss (its id goes on the token)
    pron-case   Pronouns (WORDS PRON) whose every WORDS parse for the form falls
                in one case slot (nominative/vocative; accusative/dative/
                ablative; genitive): the first alternative of the first sense
                that is an English pronoun form for that slot (FORMS). "nos"
                gives "we"; "nobis" (ABL/DAT) gives "us".
    first-sense The first sense: the meaning line with (parentheses) and
                [brackets] off, cut at the first ";", then at the first ","
                (or "!"); a slashed group gives its first member ("make/
                build" -> "make", "wild/loud shouting" -> "wild shouting").
                Part-of-speech sanity: a verb's leading
                "to" and a noun's leading article are dropped, terminal
                "!"/"." go; the result must be English words, at most four.
                A multi-word gloss is hyphenated (the hymns' wooden style:
                one chunk per Latin word).
    (none)      null, with the reason.

OVERRIDES (the later contextual layer)
    data/hymns/gloss-overrides.jsonl, one row per token address, the shape
    of data/nt/gloss-overrides.jsonl (strongs_gloss.load_overrides, which
    reads both). It replaces the dictionary gloss; the dictionary value and
    its rule are kept under provenance `was`. Empty today: no house draft is
    invented for these hymns.

LICENCE
    WORDS is `free-grant`, not PD (whitaker.LICENCE; README-lemma-spine s.1).
    The meaning lines are Whitaker's; each gloss is a few words cut from one.
"""

import json
import os
import re

import strongs_gloss as G

SOURCE = "whitaker-words"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEMMAS = os.path.join(ROOT, "data", "lemmas", "whitaker-la", "hymns.lemmas.jsonl")
OVERRIDES = os.path.join(ROOT, "data", "hymns", "gloss-overrides.jsonl")
RULES = {
    "pron-case": ("pronoun whose WORDS parses share one case slot: the first alternative of the first "
                  "sense that is an English pronoun form for that slot"),
    "first-sense": ("the first sense of the WORDS meaning line: (parentheses) and [brackets] off, cut at "
                    "the first ';', then the first ','; a slashed group gives its first member; a verb's "
                    "'to' and a noun's article dropped; at most four words, hyphenated"),
}
RULE_ORDER = ("pron-case", "first-sense")

# English pronoun form -> the case slots it serves. `nom` covers the
# vocative, `obl` the accusative, dative and ablative.
FORMS = {
    "i": "nom", "me": "obl", "my": "gen", "we": "nom", "us": "obl", "our": "gen",
    "you": "nom obl", "your": "gen", "thou": "nom", "thee": "obl", "thy": "gen", "thine": "gen",
    "he": "nom", "him": "obl", "his": "gen", "she": "nom", "her": "obl gen",
    "it": "nom obl", "its": "gen", "they": "nom", "them": "obl", "their": "gen",
    "this": "nom obl gen", "these": "nom obl gen", "that": "nom obl gen", "those": "nom obl gen",
    "who": "nom", "whom": "obl", "whose": "gen", "which": "nom obl gen", "what": "nom obl",
}
_SLOT = {"NOM": "nom", "VOC": "nom", "ACC": "obl", "DAT": "obl", "ABL": "obl", "GEN": "gen"}


def load_lemmas(path=None):
    """{WORDS key: row} from the committed lemma table."""
    out = {}
    with open(path or LEMMAS, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                out[r["key"]] = r
    return out


def meaning(row):
    """The first DICTLINE entry's meaning line, or None."""
    for e in (row or {}).get("entries") or []:
        return (e.get("meaning") or "").strip() or None
    return None


def _strip_notes(s):
    """(parentheses) and [brackets] off, nested or not."""
    prev = None
    while prev != s:
        prev, s = s, re.sub(r"\([^()]*\)|\[[^\[\]]*\]", " ", s)
    return re.sub(r"\s+", " ", s.replace("(", " ").replace(")", " ")
                  .replace("[", " ").replace("]", " ")).strip()


def first_sense(m):
    """The first non-empty sense of a meaning line, notes off."""
    for sense in _strip_notes(m).split(";"):
        s = sense.strip(" ,.")
        if s:
            return s
    return ""


def alternatives(sense):
    """A sense's alternatives in order: split at ',' (and '!', which WORDS
    uses between an interjection's senses), and within each, every slashed
    group reduced to its first member ("make/build" -> "make", "wild/loud
    shouting" -> "wild shouting"). WORDS's "_" joins words ("the_other")."""
    out = []
    for part in re.split(r"[,!]", sense.replace("_", " ")):
        a = re.sub(r"([A-Za-z][\w'-]*)(?:/[\w'-]+)+", r"\1", part).strip()
        if a:
            out.append(a)
    return out


def pos_of(key):
    """The WORDS part of speech in a dictionary form (`hic, haec, hoc  PRON`)."""
    m = re.search(r"\s{2}(N|V|ADJ|ADV|PRON|PREP|CONJ|INTERJ|NUM|PACK|VPAR|SUPINE|TACKON|PREFIX|SUFFIX)\b", key)
    return m.group(1) if m else None


def case_slot(token):
    """One case slot shared by every WORDS parse of the token, or None."""
    w = ((token.get("provenance") or {}).get("parsing") or {}).get("whitaker")
    parses = [w] if isinstance(w, str) else list(w or [])
    slots = set()
    for p in parses:
        bits = p.split()
        if not bits or bits[0] != "PRON" or len(bits) < 4:
            return None
        slots.add(_SLOT.get(bits[3]))
    return slots.pop() if len(slots) == 1 and None not in slots else None


def tidy(g, pos):
    """Part-of-speech sanity on a cut sense -> a gloss, or None."""
    g = g.strip(" .!?;:").strip()
    if pos == "V":
        g = re.sub(r"^to\s+", "", g, flags=re.I)
    if pos == "N":
        g = re.sub(r"^(?:a|an|the)\s+", "", g, flags=re.I)
    if not g or len(g.split()) > 4 or not re.fullmatch(r"[A-Za-z][A-Za-z' -]*[A-Za-z]|[A-Za-z]", g):
        return None
    return "-".join(g.split())


def gloss_for_key(key, row, slot=None):
    """(gloss or None, rule or why) for one WORDS entry."""
    m = meaning(row)
    if not m:
        return None, "the lemma table carries no meaning line for this entry"
    pos = pos_of(key)
    sense = first_sense(m)
    if pos == "PRON" and slot:
        for a in alternatives(sense):
            if slot in FORMS.get(a.lower(), "").split():
                return a, "pron-case"
    alts = alternatives(sense)
    g = tidy(alts[0], pos) if alts else None
    if g:
        return g, "first-sense"
    return None, "the first sense is not a word gloss (more than four words, or not English words)"


def gloss_for(token, lemmas):
    """(gloss or None, provenance) for a hymn token with no house gloss."""
    def none(why, **extra):
        return None, {"source": None, "by": None, "rule": None, "kind": None, "why": why, **extra}

    key = token.get("lemma_key")
    if key:
        g, rule = gloss_for_key(key, lemmas.get(key), case_slot(token))
        if g:
            return g, {"source": SOURCE, "by": "lemma_key", "rule": rule, "kind": "dictionary"}
        return none(rule)
    if not token.get("lemma"):
        return none("no lemma: the gloss is read from the lemma's WORDS entry")
    cands = ((token.get("provenance") or {}).get("lemma") or {}).get("whitaker") or []
    got = {k: gloss_for_key(k, lemmas.get(k), case_slot(token)) for k in cands}
    glosses = {g for g, _ in got.values()}
    if cands and len(glosses) == 1 and None not in glosses:
        rules = {r for _, r in got.values()}
        return glosses.pop(), {"source": SOURCE, "by": "lemma", "rule": sorted(rules)[0],
                               "kind": "dictionary", "entries": len(cands)}
    return none("the lemma's WORDS entries give different first senses: "
                + "; ".join(f"{k.split('  ', 1)[1] if '  ' in k else k} -> {g or '(none)'}"
                            for k, (g, _) in got.items()))


# The override layer: strongs_gloss's, pointed at the hymns' file.
def load_overrides(path=None):
    return G.load_overrides(path or OVERRIDES)


apply_override = G.apply_override
