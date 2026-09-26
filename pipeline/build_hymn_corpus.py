#!/usr/bin/env python3
"""
build_hymn_corpus.py -- the Latin hymns as four flat JSONL files, one row per
CLAUSE, every record keyed by uid.

    python3 pipeline/build_hymn_corpus.py            # build, mint once, write
    python3 pipeline/build_hymn_corpus.py --check    # rebuild, assert 0 minted
                                                     #   and byte-identical output
    python3 pipeline/build_hymn_corpus.py --report   # stats only, no write

    Source folder: $WORDHOARD_LATIN_DIR, else the vault's
    `9 - Projects/Word Hoard/data/latin-corpus` (the batch JSON's interim home).

    Output: data/hymns/{passages,witnesses,tokens,alignments}.jsonl + manifest.json
    Schema: pipeline/README-hymn-jsonl.md.  Validator: tests/hymn_corpus_test.py.

WHAT WAS WRONG (launch plan D1; measured 2026-09-26 against the vault files)
    Three granularities for one hymn, and no two agreed:

        thomas-batch-NN.json          stores a hymn by STANZA  (HYM-adoro.st1)
        thomas-batch-01-permutations  addresses Adoro te by LINE (HYM-adoro.st1.l1)
        thomas-batch-02-permutations  addresses Pange lingua by CLAUSE (...st1.c1)
        ruling 2026-09-16 (#10)       verse is stored by CLAUSE

    Joined on `unit_id`, 27 of 64 rows in batch 01 and 10 of 20 in batch 02
    join to nothing -- every hymn row except Pange lingua st2 and st3, whose
    single clause happens to share the stanza's id. (The launch plan says
    "37 of 64"; 37 is the number that DO join. The 2026-09-18 Canon OS status
    line has it right.) And where a row did join, its tokens joined by
    POSITION inside the stanza, with no id at all.

WHAT THIS DOES
    1. Cuts every hymn stanza into clauses by an explicit table (CLAUSES below).
       Pange lingua's cut is the one its retrofit already made (2026-09-16).
       Adoro te is re-cut here, by the rule in the schema doc: lines join into
       one row exactly when a word on one line depends on a finite verb on
       another. The old line rows fold into clauses; nothing is re-glossed.
    2. Mints one uid per clause citation (`hymns:adoro-te.st3.c3`) through
       wh_uid -- once, then reused forever. The stanza keeps its existing uid
       and becomes the container (it is still the unit Hopkins, Caswall and
       the Oratorium work in); the Latin text and its tokens move down to the
       clause, so the text is stored exactly once.
    3. Joins the permutation data to the passage data ONCE, here, through the
       legacy-id table, and writes everything out keyed by uid. After this no
       consumer ever needs `unit_id` or token position-in-stanza again.

NOTHING IS GUESSED, NOTHING IS WRITTEN NEW
    Every legacy row must land in exactly one clause; every clause's tokens
    must match the stanza's tokens surface for surface; every clause's text
    must re-tokenize to its tokens. Any mismatch is a hard stop, not a
    best-effort. Glosses, lemmas, parsings and plain_forms are carried as they
    were drafted; the only computed token fields are the mechanical ones
    (normalized, search_key). Where a merged clause needs a prose order, it is
    the two line orders concatenated -- no word was moved across a line break
    that was not already moved in the retrofit.

WHAT IS NOT HERE
    `plain` is never stored -- it is rendered from `prose_order` (render_plain).
    The wooden line is never stored -- it is the token glosses in Latin order.
    Nothing from Perseus (CC BY-SA): that is a separate enrichment layer keyed
    by CTS URN, and neither hymn has a Perseus edition.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import wh_uid as U  # noqa: E402
import whitaker as W  # noqa: E402
from lemma_spine import resolve  # noqa: E402

UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")
OUT = os.path.join(ROOT, "data", "hymns")
FILES = ("passages", "witnesses", "tokens", "alignments")
# The lemma spine's committed Whitaker analyses (build_lemma_spine.py). Read
# here, never recomputed, so this build and its --check stay offline.
SPINE = os.path.join(ROOT, "data", "lemmas", "whitaker-la", "hymns.analyses.jsonl")
SCHEMA = "wordhoard/corpus-jsonl/v1"

# The recut is an event with a date; it comes from the device clock, not the
# build, so a rebuild next month is byte-identical.
CUT_ON = "2026-09-26"

SOURCE_CANDIDATES = [
    os.environ.get("WORDHOARD_LATIN_DIR"),
    r"C:\Users\adamk\Obsidian\MindCastleintheCloud\9 - Projects\Word Hoard\data\latin-corpus",
    os.path.join(ROOT, "..", "..", "..", "Obsidian", "MindCastleintheCloud",
                 "9 - Projects", "Word Hoard", "data", "latin-corpus"),
]

# ---------------------------------------------------------------------------
# The cut. One entry per clause: (first line, last line, legacy unit_ids, why).
# `why` is required wherever lines are joined; a one-line clause needs none.
# ---------------------------------------------------------------------------

JOIN = "lines joined: {}"

HYMNS = {
    "adoro-te": {
        "title": "Adoro te devote",
        "legacy_prefix": "HYM-adoro",
        "batch": "thomas-batch-01.json",
        "permutations": "thomas-batch-01-permutations.json",
        "stanza_singable": {"from": "en.elegant", "source": "hopkins-1918"},
        "cut_by": "recut 2026-09-26 (this build), from the 2026-09-15 line rows",
        "clauses": {
            1: [(1, 1, ["HYM-adoro.st1.l1"], None),
                (2, 2, ["HYM-adoro.st1.l2"], None),
                (3, 3, ["HYM-adoro.st1.l3"], None),
                (4, 4, ["HYM-adoro.st1.l4"], None)],
            2: [(1, 1, ["HYM-adoro.st2.l1"], None),
                (2, 2, ["HYM-adoro.st2.l2"], None),
                (3, 3, ["HYM-adoro.st2.l3"], None),
                (4, 4, ["HYM-adoro.st2.l4"], None)],
            3: [(1, 1, ["HYM-adoro.st3.l1"], None),
                (2, 2, ["HYM-adoro.st3.l2"], None),
                (3, 4, ["HYM-adoro.st3.l3", "HYM-adoro.st3.l4"],
                 JOIN.format("l.3 has no finite verb; its participles credens "
                             "and confitens agree with the subject of Peto (l.4)"))],
            4: [(1, 1, ["HYM-adoro.st4.l1"], None),
                (2, 2, ["HYM-adoro.st4.l2"], None),
                (3, 4, ["HYM-adoro.st4.l3", "HYM-adoro.st4.l4"],
                 JOIN.format("the infinitives habere and diligere (l.4) are "
                             "governed by Fac (l.3), as credere is"))],
            5: [(1, 1, ["HYM-adoro.st5.l1"], None),
                (2, 2, ["HYM-adoro.st5.l2"], None),
                (3, 4, ["HYM-adoro.st5.l3", "HYM-adoro.st5.l4"],
                 JOIN.format("sapere (l.4) is governed by Praesta (l.3), "
                             "coordinate with vivere"))],
            6: [(1, 1, ["HYM-adoro.st6.l1"], None),
                (2, 2, ["HYM-adoro.st6.l2"], None),
                (3, 4, ["HYM-adoro.st6.l3-4"],
                 JOIN.format("quit (l.4) governs facere (l.3); already one row "
                             "in the 2026-09-15 retrofit"))],
            7: [(1, 1, ["HYM-adoro.st7.l1"], None),
                (2, 2, ["HYM-adoro.st7.l2"], None),
                (3, 4, ["HYM-adoro.st7.l3", "HYM-adoro.st7.l4"],
                 JOIN.format("Ut (l.3) takes its verb sim in l.4, and cernens "
                             "agrees with the subject of sim"))],
        },
    },
    "pange-lingua": {
        "title": "Pange lingua gloriosi corporis mysterium",
        "legacy_prefix": "HYM-pange",
        "batch": "thomas-batch-02.json",
        "permutations": "thomas-batch-02-permutations.json",
        "stanza_singable": {"from": "permutations", "source": "caswall-1849-britt-1922"},
        "stanza_literal": {"source": "britt-1922-prose"},
        "clause_elegant": {"source": "house-elegant-2026-09-15"},
        "cut_by": "the 2026-09-16 retrofit (unchanged here)",
        "clauses": {
            1: [(1, 3, ["HYM-pange.st1.c1"], JOIN.format("gloriosi (l.1) agrees with Corporis (l.2); all governed by Pange")),
                (4, 6, ["HYM-pange.st1.c2"], JOIN.format("the relative clause: Quem (l.4) waits for Rex and fudit (l.6)"))],
            2: [(1, 6, ["HYM-pange.st2"], JOIN.format("one period, one finite verb (clausit)"))],
            3: [(1, 6, ["HYM-pange.st3"], JOIN.format("one period, one finite verb (dat)"))],
            4: [(1, 2, ["HYM-pange.st4.c1"], JOIN.format("double accusative across the break, one verb (efficit)")),
                (3, 3, ["HYM-pange.st4.c2"], None),
                (4, 6, ["HYM-pange.st4.c3"], JOIN.format("ad firmandum (l.5) depends on sufficit (l.6); the si-clause rides with its main clause"))],
            5: [(1, 2, ["HYM-pange.st5.c1"], JOIN.format("hortatory subjunctive veneremur (l.2) governs l.1")),
                (3, 4, ["HYM-pange.st5.c2"], JOIN.format("jussive cedat (l.4) governs l.3")),
                (5, 6, ["HYM-pange.st5.c3"], JOIN.format("jussive praestet (l.5) governs l.6"))],
            6: [(1, 4, ["HYM-pange.st6.c1"], JOIN.format("one verb (sit, l.4) for six subjects")),
                (5, 6, ["HYM-pange.st6.c2"], JOIN.format("the doxology's second clause"))],
        },
    },
}

# Every source a field in these files comes from. The licence gate (launch
# plan D4) is: public-domain editions, or the house's own work, and nothing
# else. `license` is checked against that set by the validator.
SOURCES = {
    "roman-missal-received": {
        "what": "Latin text of both hymns",
        "edition": "received liturgical text (Roman Missal), as transcribed into the batch notes 2026-09-14/15",
        "license": "PD",
        "license_basis": "13th-century text; no modern critical edition used",
        "verified": False,
        "open": ("Adoro te is not yet checked against a named PD printing; Pange lingua was checked "
                 "against Britt 1922 and differs in orthography only (cenae/coenae, iubilatio/jubilatio, "
                 "gentium/Gentium, Britt prints no Amen). Canonical orthography is Adam's call "
                 "(Latin Hymns doc s.7, decision 2)."),
    },
    "hopkins-1918": {
        "what": "Adoro te: stanza-level metrical English (singable)",
        "edition": "Gerard Manley Hopkins, Poems, ed. Bridges (London, 1918)",
        "license": "PD",
        "license_basis": "published 1918; author d. 1889",
        "verified": False,
        "open": "Quoted from memory in the batch note; verify every stanza against the printed 1918 text before any public use.",
    },
    "caswall-1849-britt-1922": {
        "what": "Pange lingua: stanza-level metrical English (singable)",
        "edition": ("Edward Caswall's translation (Lyra Catholica, 1849) as printed in Matthew Britt, "
                    "The Hymns of the Breviary and Missal (1922), pp. 183-185, "
                    "archive.org/details/hymnsofbreviarym00britrich"),
        "license": "PD",
        "license_basis": "published 1849 and 1922",
        "verified": True,
        "verified_on": "2026-09-17",
        "open": "Britt uses American spellings (honor, fulfills); Caswall's 1849 printing presumably differs. Canonical edition is Adam's call.",
    },
    "britt-1922-prose": {
        "what": "Pange lingua: stanza-level literal prose (the PD candidate for `elegant`)",
        "edition": "Matthew Britt, The Hymns of the Breviary and Missal (1922), literal prose per stanza",
        "license": "PD",
        "license_basis": "published 1922",
        "verified": True,
    },
    "house-draft-2026-09-14": {
        "what": "token gloss (wooden), lemma, parsing, syntax; teacher notes",
        "edition": "AK/Claude machine draft, Thomas Batch 01 (2026-09-14) and 02 (2026-09-15)",
        "license": "own",
        "verified": False,
        "open": ("machine draft, unchecked by Adam. Since D3 its lemma and parsing are the fallback: "
                 "each token's `provenance` says which source its value came from."),
    },
    "whitaker-words": {
        "what": "token lemma (and parsing, where unambiguous): the Latin lemma spine, launch plan D3",
        "edition": (f"{W.VERSION}, {W.REPO_URL} at {W.COMMIT[:12]}; analyses in "
                    "data/lemmas/whitaker-la/hymns.analyses.jsonl (pipeline/README-lemma-spine.md)"),
        **{k: v for k, v in W.LICENCE.items()},
    },
    "house-retrofit-2026-09-15": {
        "what": "prose_order, plain_form, absorbed (the plain column's four mechanisms)",
        "edition": "Plain Column Retrofits, Batch 01 (2026-09-15) and 02 (2026-09-16)",
        "license": "own",
        "verified": False,
    },
    "house-elegant-2026-09-15": {
        "what": "Pange lingua: clause-level elegant prose",
        "edition": "AK, Thomas Batch 02 (2026-09-15)",
        "license": "own",
        "license_basis": "the batch file records this as PD; it is the house's own prose, recorded here as own",
        "verified": False,
    },
    "house-recut-2026-09-26": {
        "what": "the clause cut of Adoro te; concatenated prose_order for joined lines",
        "edition": "build_hymn_corpus.py CLAUSES table",
        "license": "own",
        "verified": False,
        "open": "unchecked by Adam; five joins, each with its grammatical reason in `cut.why`.",
    },
}

ALLOWED_LICENSES = ("PD", "own", "free-grant")
# `free-grant`: the copyright holder grants any and all use, unconditionally
# (Whitaker's WORDS, and nothing else yet). Not PD; admitted for lexical data
# pending Adam's ruling -- see whitaker.LICENCE["open"].

# Token fields: where each comes from. `null` in a record means "no licensed
# source yet", never "unknown by accident".
TOKEN_FIELDS = {
    "surface": "the reading of record, exactly as transcribed",
    "normalized": "derived: NFC(surface)",
    "search_key": "derived: fold(normalized) -- see search_key()",
    "translit": "null by rule on a Latin-script witness; filled only for grc/he",
    "lemma": ("whitaker-words where its headword is the draft's and one entry is picked out; "
              "else house-draft-2026-09-14, flagged in `review`. Per token: provenance.lemma"),
    "parsing": ("whitaker-words where it gives exactly one parse, the draft agrees and adds no "
                "teaching note; else house-draft-2026-09-14. Never invented. Per token: provenance.parsing"),
    "lemma_key": "whitaker-words: the WORDS dictionary form naming the lemma; null where the draft stands",
    "gloss": "house-draft-2026-09-14: the wooden gloss, Latin order",
    "plain_form": "house-retrofit-2026-09-15; null where the gloss serves as-is",
}

PERSEUS = {
    "policy": ("Perseus is CC BY-SA. Nothing from Perseus is in these files. Perseus "
               "enrichment (lemmata, morphology, treebank links) is a separate layer "
               "keyed by CTS URN and joined at read time, never merged in."),
    "cts_urn": {"hymns:adoro-te": None, "hymns:pange-lingua": None},
    "note": "Neither hymn has a Perseus/CTS edition; the URN is null, not guessed.",
}

# ---------------------------------------------------------------------------
# Mechanical token fields and the plain renderer (shared with the test)
# ---------------------------------------------------------------------------

PUNCT = ",.;:!?\"'()"


def tokenize(text):
    """The rule the batch notes were tokenized by: whitespace, edge punctuation
    off. Verified 2026-09-26 against all 13 stanzas (224 tokens, 0 mismatches)."""
    return [w.strip(PUNCT) for w in text.split() if w.strip(PUNCT)]


def normalized(surface):
    return unicodedata.normalize("NFC", surface)


def search_key(s):
    """What searches run against. Decompose, drop combining marks (macrons,
    accents), lowercase, unfold ligatures, and fold the letters Latin printers
    never agreed on: j -> i, v -> u. So `subjicit` finds `subiicit` and
    `jubilatio` finds `iubilatio`."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower()
    s = s.replace("æ", "ae").replace("œ", "oe")
    return s.translate(str.maketrans("jv", "iu"))


# A capital belongs to sentence position, not to a word; these glosses keep
# theirs wherever they land. Union of the two retrofits' lists, unchanged.
PROPER = ("God", "Deit", "Jesu", "Lord", "Thomas", "Truth", "Son", "Amen",
          "Metaphys", "Godhead", "Christ", "Word", "Blood", "Body", "Virgin",
          "King", "Begetter", "Begotten", "Sacrament", "Law", "Fruit")


def _decap(word):
    if word == "I" or word.startswith("I-"):
        return word          # the pronoun is never lower-cased (retrofit printed 'i-confess')
    for i, ch in enumerate(word):
        if ch.isalpha():
            if word[i:].isupper() and len(word[i:]) > 1:
                return word
            return word[:i] + ch.lower() + word[i + 1:]
    return word


def _recap(word):
    for i, ch in enumerate(word):
        if ch.isalpha():
            return word[:i] + ch.upper() + word[i + 1:]
    return word


def render_wooden(tokens):
    return " ".join(t["gloss"] for t in tokens)


def render_plain(tokens, plain):
    """`plain` is the en.plain witness row. Never stored; always this."""
    if plain.get("plain_override"):
        return plain["plain_override"]
    parts = []
    for step in plain["prose_order"]:
        if isinstance(step, str):
            parts.append("[" + step + "]")
            continue
        tok = tokens[step - 1]
        word = tok["plain_form"] or tok["gloss"]
        if not any(p in word for p in PROPER):
            word = _decap(word)
        parts.append(word)
    if parts:
        parts[0] = _recap(parts[0])
    return " ".join(parts)


def permutation_problems(n_tokens, prose_order, absorbed):
    """Every token used exactly once, by the order or by absorption."""
    used = [s for s in prose_order if isinstance(s, int)]
    accounted = sorted(used + list(absorbed))
    if accounted == list(range(1, n_tokens + 1)):
        return None
    return {"missing": [n for n in range(1, n_tokens + 1) if n not in accounted],
            "duplicated": sorted({n for n in accounted if accounted.count(n) > 1}),
            "out_of_range": [n for n in accounted if not 1 <= n <= n_tokens]}


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def find_source():
    for c in SOURCE_CANDIDATES:
        if c and os.path.isdir(c):
            return c
    raise SystemExit("could not find the Latin shelf. Looked in:\n  "
                     + "\n  ".join(c or "<WORDHOARD_LATIN_DIR unset>" for c in SOURCE_CANDIDATES))


def _load(d, fn):
    p = os.path.join(d, fn)
    with open(p, "rb") as f:
        raw = f.read()
    return json.loads(raw.decode("utf-8")), hashlib.sha256(raw).hexdigest()


def _witness(p, tail):
    for w in p["witnesses"]:
        if w["witness_id"] == f"{p['id']}.{tail}":
            return w
    raise SystemExit(f"{p['id']}: no witness {tail!r}")


def _stop(msg):
    raise SystemExit("HARD STOP: " + msg)


def load_spine():
    if not os.path.exists(SPINE):
        _stop(f"{SPINE} is missing: run pipeline/build_lemma_spine.py")
    with open(SPINE, "rb") as f:
        raw = f.read()
    rows = [json.loads(l) for l in raw.decode("utf-8").splitlines()]
    return {r["form"]: r["analyses"] for r in rows}, hashlib.sha256(raw).hexdigest()


def spine_stats(tokens):
    """Coverage and disagreement counts, for the manifest and the test."""
    def count(field):
        out = {}
        for t in tokens:
            k = t["provenance"][field]["status"]
            out[k] = out.get(k, 0) + 1
        return dict(sorted(out.items()))
    n = len(tokens)
    lw = sum(1 for t in tokens if t["provenance"]["lemma"]["source"] == "whitaker-words")
    pw = sum(1 for t in tokens if t["provenance"]["parsing"]["source"] == "whitaker-words")
    return {
        "tokens": n,
        "lemma_from_whitaker": lw,
        "lemma_from_draft": n - lw,
        "parsing_from_whitaker": pw,
        "parsing_confirmed_by_whitaker": sum(1 for t in tokens
                                             if t["provenance"]["parsing"]["status"] == "confirmed"),
        "lemma_status": count("lemma"),
        "parsing_status": count("parsing"),
        "flagged_for_review": sum(1 for t in tokens if t["review"]),
    }


def build(src, reg):
    passages, witnesses, tokens, alignments = [], [], [], []
    inputs = {}
    spine, spine_sha = load_spine()
    legacy_map = {}          # legacy unit_id -> clause uid (the join, done once)

    for key, H in HYMNS.items():
        batch, h1 = _load(src, H["batch"])
        perms, h2 = _load(src, H["permutations"])
        inputs[H["batch"]] = h1
        inputs[H["permutations"]] = h2
        work = f"hymns:{key}"
        rows = {r["unit_id"]: r for r in perms["rows"]
                if r["unit_id"].startswith(H["legacy_prefix"] + ".")}
        claimed = []
        stanzas = [p for p in batch["passages"] if p["id"].startswith(H["legacy_prefix"] + ".")]
        if sorted(int(p["id"].rsplit(".st", 1)[1]) for p in stanzas) != sorted(H["clauses"]):
            _stop(f"{work}: stanza set in {H['batch']} does not match the CLAUSES table")

        for sp in sorted(stanzas, key=lambda p: int(p["id"].rsplit(".st", 1)[1])):
            n = int(sp["id"].rsplit(".st", 1)[1])
            st_cit = f"{work}.st{n}"
            if sp.get("citation") != st_cit:
                _stop(f"{sp['id']}: citation {sp.get('citation')!r} != {st_cit!r}")
            st_uid = reg.uid_for(st_cit)
            if st_uid != sp.get("uid"):
                _stop(f"{st_cit}: registry uid {st_uid} != batch uid {sp.get('uid')} -- identity moved")
            la = _witness(sp, "la.1")
            lines = la["text"].split("\n")
            st_tokens = la["tokens"]
            if tokenize(la["text"]) != [t["surface"] for t in st_tokens]:
                _stop(f"{st_cit}: stanza text does not re-tokenize to its tokens")

            cursor = 0
            prev_last = 0
            clause_uids = []
            stanza_at = len(passages)      # the container row goes ahead of its clauses
            for ci, (a, b, legacy_ids, why) in enumerate(H["clauses"][n], 1):
                if a != prev_last + 1 or b < a or b > len(lines):
                    _stop(f"{st_cit} c{ci}: lines {a}-{b} do not continue the partition")
                if b > a and not why:
                    _stop(f"{st_cit} c{ci}: lines joined with no reason recorded")
                prev_last = b
                lrows = []
                for lid in legacy_ids:
                    if lid not in rows:
                        _stop(f"{lid}: not a row in {H['permutations']}")
                    lrows.append(rows[lid])
                    claimed.append(lid)
                    if "source_lines" in rows[lid]:
                        m = re.match(r"st(\d+) ll?\.(\d+)(?:-(\d+))?$", rows[lid]["source_lines"])
                        if not m or (int(m.group(1)), int(m.group(2)), int(m.group(3) or m.group(2))) != (n, a, b):
                            _stop(f"{lid}: source_lines {rows[lid]['source_lines']!r} disagree with the table ({a}-{b})")

                text = "\n".join(lines[a - 1:b])
                surf = tokenize(text)
                ptoks = [t for r in lrows for t in r["tokens"]]
                if [t["surface"] for t in ptoks] != surf:
                    _stop(f"{st_cit} c{ci}: permutation tokens do not match lines {a}-{b}")
                stoks = st_tokens[cursor:cursor + len(surf)]
                if [t["surface"] for t in stoks] != surf:
                    _stop(f"{st_cit} c{ci}: stanza tokens do not match lines {a}-{b}")

                # prose order: the rows' orders, concatenated with offsets.
                order, absorbed, off = [], [], 0
                for r in lrows:
                    if r.get("plain_override"):
                        _stop(f"{r['unit_id']}: carries a plain_override; merge it by hand")
                    order += [s + off if isinstance(s, int) else s for s in r["prose_order"]]
                    absorbed += [s + off for s in r["absorbed"]]
                    off += len(r["tokens"])
                prob = permutation_problems(len(surf), order, absorbed)
                if prob:
                    _stop(f"{st_cit} c{ci}: bad permutation {prob}")
                grades = {r["grade"] for r in lrows}
                mems = {r["mem"] for r in lrows}
                if len(mems) != 1:
                    _stop(f"{st_cit} c{ci}: rows disagree on memorize {mems}")

                cit = f"{st_cit}.c{ci}"
                uid = reg.uid_for(cit)
                clause_uids.append(uid)
                for lid in legacy_ids:
                    legacy_map[lid] = uid

                passages.append({
                    "uid": uid, "citation": cit, "kind": "passage", "unit": "clause",
                    "work": work, "stanza_uid": st_uid, "stanza": n, "clause": ci,
                    "lines": [a, b], "grade": max(grades), "memorize": mems.pop(),
                    "reading_of_record": "la.1",
                    "cut": {"by": H["cut_by"], "why": why},
                    "notes": [r["note"] for r in lrows if r.get("note")],
                    "status": "machine-draft, unchecked",
                    "legacy": {"unit_ids": legacy_ids},
                })
                witnesses.append({
                    "address": U.address(uid, "la.1"), "passage_uid": uid, "name": "la.1",
                    "lang": "la", "role": "original", "register": la.get("register"),
                    "text": text, "generated": False, "source": "roman-missal-received",
                    "attested": la.get("attested"), "reading_of_record": True,
                    "cut_from": la.get("address"),
                })
                witnesses.append({
                    "address": U.address(uid, "en.wooden"), "passage_uid": uid, "name": "en.wooden",
                    "lang": "en", "role": "wooden", "text": None, "generated": True,
                    "generated_from": "la.1 token gloss, Latin order",
                    "source": "house-draft-2026-09-14", "attested": "N", "reading_of_record": False,
                })
                witnesses.append({
                    "address": U.address(uid, "en.plain"), "passage_uid": uid, "name": "en.plain",
                    "lang": "en", "role": "plain", "text": None, "generated": True,
                    "generated_from": "la.1 tokens walked in prose_order",
                    "prose_order": order, "absorbed": absorbed, "plain_override": None,
                    "source": "house-retrofit-2026-09-15" if len(lrows) == 1 else "house-recut-2026-09-26",
                    "attested": "N", "reading_of_record": False,
                })
                if H.get("clause_elegant"):
                    els = [r["elegant"] for r in lrows]
                    witnesses.append({
                        "address": U.address(uid, "en.elegant"), "passage_uid": uid, "name": "en.elegant",
                        "lang": "en", "role": "elegant", "text": " ".join(els), "generated": False,
                        "source": H["clause_elegant"]["source"], "attested": "N",
                        "reading_of_record": False,
                    })
                # the stanza line each token sits on, for verse display
                on_line = [li for li in range(a, b + 1) for _ in tokenize(lines[li - 1])]
                for i, (st, pt) in enumerate(zip(stoks, ptoks), 1):
                    if st["gloss_en"] != pt["wooden"]:
                        _stop(f"{st['token_id']}: gloss {st['gloss_en']!r} != permutation {pt['wooden']!r}")
                    skey = search_key(normalized(st["surface"]))
                    if skey not in spine:
                        _stop(f"{st['token_id']}: {skey!r} has no row in the lemma spine; "
                              "run pipeline/build_lemma_spine.py")
                    lemma, lemma_key, parsing, prov, review = resolve(
                        st.get("lemma") or None, st.get("parsing") or None, spine[skey])
                    tokens.append({
                        "address": U.address(uid, f"la.1.t{i:02d}"), "passage_uid": uid,
                        "witness": "la.1", "position": i, "line": on_line[i - 1],
                        "surface": st["surface"],
                        "normalized": normalized(st["surface"]),
                        "search_key": skey,
                        "translit": None,
                        "lemma": lemma,
                        "lemma_key": lemma_key,
                        "parsing": parsing,
                        "gloss": st["gloss_en"],
                        "plain_form": pt["plain_form"],
                        "syntax": st.get("syntax") or None,
                        "legacy_address": st.get("address"),
                        "provenance": prov,
                        "review": review,
                    })
                cursor += len(surf)

            if cursor != len(st_tokens) or prev_last != len(lines):
                _stop(f"{st_cit}: the clauses do not cover the stanza "
                      f"({cursor}/{len(st_tokens)} tokens, {prev_last}/{len(lines)} lines)")

            passages.insert(stanza_at, {
                "uid": st_uid, "citation": st_cit, "kind": "passage", "unit": "stanza",
                "work": work, "stanza": n, "lines": [1, len(lines)],
                "clauses": clause_uids, "grade": sp.get("grade"), "memorize": sp.get("memorize"),
                "teacher_notes": sp.get("teacher_notes"),
                "status": sp.get("status"), "legacy": {"id": sp["id"]},
            })

            # stanza-level renderings: they render the stanza, not a clause.
            sing = H["stanza_singable"]
            if sing["from"] == "permutations":
                texts = {rows[lid]["singable"] for c in H["clauses"][n] for lid in c[2]}
                if len(texts) != 1:
                    _stop(f"{st_cit}: clause rows disagree on the singable stanza")
                stext, legacy_w = texts.pop().replace(" / ", "\n"), None
            else:
                w = _witness(sp, sing["from"])
                stext, legacy_w = w["text"], w["address"]
            sw = {"address": U.address(st_uid, "en.singable"), "passage_uid": st_uid,
                  "name": "en.singable", "lang": "en", "role": "singable", "text": stext,
                  "generated": False, "source": sing["source"], "attested": "Y",
                  "reading_of_record": False}
            if legacy_w:
                sw["legacy_address"] = legacy_w
            witnesses.append(sw)
            stanza_renderings = ["en.singable"]
            if H.get("stanza_literal"):
                witnesses.append({
                    "address": U.address(st_uid, "en.literal"), "passage_uid": st_uid,
                    "name": "en.literal", "lang": "en", "role": "literal-prose",
                    "text": perms["elegant_alternative"]["by_stanza"][f"st{n}"],
                    "generated": False, "source": H["stanza_literal"]["source"],
                    "attested": "Y", "reading_of_record": False})
                stanza_renderings.append("en.literal")

            for name in stanza_renderings:
                conf, note = "high", None
                if key == "adoro-te" and n == 6:
                    conf, note = "medium", ("Hopkins opens this stanza with a clause "
                                            "that has no counterpart in the Latin")
                alignments.append({
                    "alignment_id": f"{U.address(st_uid, name)}~la.1",
                    "level": "section", "type": f"1:{'many' if len(clause_uids) > 1 else '1'}",
                    "a": [{"address": U.address(st_uid, name), "tokens": None}],
                    "b": [{"address": U.address(u, "la.1"), "tokens": None} for u in clause_uids],
                    "confidence": conf, "note": note,
                })

        missing = sorted(set(rows) - set(claimed))
        if missing:
            _stop(f"{work}: legacy rows land in no clause: {missing}")
        if len(claimed) != len(set(claimed)):
            _stop(f"{work}: a legacy row lands in two clauses")

    manifest = {
        "schema": SCHEMA,
        "doc": "pipeline/README-hymn-jsonl.md",
        "cut_on": CUT_ON,
        "row_unit": "clause",
        "counts": {"passages": len(passages),
                   "clauses": sum(1 for p in passages if p["unit"] == "clause"),
                   "stanzas": sum(1 for p in passages if p["unit"] == "stanza"),
                   "witnesses": len(witnesses), "tokens": len(tokens),
                   "alignments": len(alignments)},
        "works": {f"hymns:{k}": {"title": H["title"], "reading_of_record": "la.1",
                                 "cut_by": H["cut_by"]} for k, H in HYMNS.items()},
        "licence_gate": {"allowed": list(ALLOWED_LICENSES),
                         "rule": "launch plan D4 / ADR 0001: public-domain editions or own work only"},
        "sources": SOURCES,
        "token_fields": TOKEN_FIELDS,
        "perseus": PERSEUS,
        "lemma_spine": {"doc": "pipeline/README-lemma-spine.md",
                        "analyses": "data/lemmas/whitaker-la/hymns.analyses.jsonl",
                        **spine_stats(tokens)},
        "legacy_join": legacy_map,
        "inputs_sha256": {**inputs, "hymns.analyses.jsonl": spine_sha},
        "files_sha256": {},
    }
    return {"passages": passages, "witnesses": witnesses, "tokens": tokens,
            "alignments": alignments}, manifest


def serialize(records):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8")


def render_all(data, manifest):
    blobs = {f"{k}.jsonl": serialize(v) for k, v in data.items()}
    manifest["files_sha256"] = {k: hashlib.sha256(v).hexdigest() for k, v in sorted(blobs.items())}
    blobs["manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return blobs


def write_atomic(path, blob):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(blob)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--uids", default=UIDS)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()

    src = find_source()
    reg = U.WhUidRegistry(a.uids)
    data, manifest = build(src, reg)
    blobs = render_all(data, manifest)
    for k, v in manifest["counts"].items():
        print(f"  {k:<12}{v:>6,}")
    s = reg.stats()
    print(f"  uids minted {s['minted']} / reused {s['reused']} / registry total {s['total']:,}")

    if a.check:
        reg.assert_no_mint()
        stale = [fn for fn, blob in blobs.items()
                 if not os.path.exists(os.path.join(a.out, fn))
                 or open(os.path.join(a.out, fn), "rb").read() != blob]
        if stale:
            raise SystemExit(f"CHECK FAILED: rebuilt output differs from committed: {stale}")
        print("  CHECK PASSED: minted 0, output byte-identical.")
        return
    if a.report:
        return
    os.makedirs(a.out, exist_ok=True)
    for fn, blob in blobs.items():
        write_atomic(os.path.join(a.out, fn), blob)
    reg.save()
    print(f"  wrote {a.out}")
    if s["minted"]:
        print(f"  wrote {a.uids}   <- COMMIT THIS")


if __name__ == "__main__":
    main()
