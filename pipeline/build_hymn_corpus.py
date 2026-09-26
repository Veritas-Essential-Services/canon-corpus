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
from lemma_spine import resolve, resolve_undrafted, load_overrides, apply_override, OVERRIDES, OVERRIDE_SOURCE  # noqa: E402

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
    # -- The other Corpus Christi hymns (launch plan Ring 3, "the hymns of
    # Thomas"). No vault batch: the Latin and both English renderings are
    # transcribed from Britt 1922 and checked against the scan, in
    # data/hymn-sources/ (PRINTED below). No house draft exists, so the tokens
    # carry no gloss and no prose_order: nothing is invented (README s.9).
    # Each clause is (first line, last line, why): EVERY cut says why, a
    # one-line clause included, because every one is on Adam's review sheet.
    "lauda-sion": {
        "title": "Lauda Sion Salvatorem",
        "source_file": "britt-1922-corpus-christi.json",
        "latin_source": "britt-1922-latin",
        "stanza_singable": {"source": "henry-britt-1922"},
        "stanza_literal": {"source": "britt-1922-prose-corpus-christi"},
        "cut_by": "house cut 2026-09-26 (this build), by the clause rule; unreviewed",
        "clauses": {
            1: [(1, 1, "own finite verb (Lauda, imperative); Sion is its vocative"),
                (2, 3, JOIN.format("l.3 has no verb: In hymnis et canticis goes with Lauda (l.2)")),
                (4, 4, "own finite verbs (potes, aude): the quantum ... tantum pair inside one line"),
                (5, 6, JOIN.format("l.5 has no finite verb (est understood after Quia); Nec (l.6) "
                                   "coordinates sufficis under the same Quia"))],
            2: [(1, 3, JOIN.format("thema (l.1) and Panis (l.2) are the subjects of proponitur (l.3)")),
                (4, 6, JOIN.format("the relative Quem (l.4) is the subject of datum [esse] (l.6), which "
                                   "ambigitur governs; Turbae ... duodenae (l.5) is its dative"))],
            3: [(1, 1, "own finite verbs (Sit ... sit); laus is their subject"),
                (2, 3, JOIN.format("jubilatio (l.3) is the subject of Sit ... sit (l.2)")),
                (4, 4, "own finite verb (agitur)"),
                (5, 6, JOIN.format("institutio (l.6) is the subject of recolitur (l.5)"))],
            4: [(1, 3, JOIN.format("Pascha (l.2) is the subject of terminat (l.3); In hac mensa (l.1) "
                                   "goes with it")),
                (4, 5, JOIN.format("l.4 has no verb: Vetustatem and novitas take fugat (l.5), gapped")),
                (6, 6, "own finite verb (eliminat)")],
            5: [(1, 1, "a relative clause with its own finite verb (gessit); may stand (rule s.1)"),
                (2, 3, JOIN.format("In sui memoriam (l.3) goes with Faciendum ... expressit (l.2)")),
                (4, 6, JOIN.format("Docti (l.4) agrees with the subject of Consecramus (l.6); Panem, "
                                   "vinum (l.5) are its objects"))],
            6: [(1, 1, "own finite verb (datur)"),
                (2, 3, JOIN.format("vinum (l.3) is a second subject of transit (l.2), gapped")),
                (4, 4, "two relative clauses with their own finite verbs (capis, vides); may stand"),
                (5, 6, JOIN.format("Praeter rerum ordinem (l.6) goes with firmat (l.5)"))],
            7: [(1, 3, JOIN.format("ll.1-2 have no verb: Sub diversis speciebus and Signis ... rebus "
                                   "go with Latent (l.3)")),
                (4, 4, "a complete verbless statement (est understood twice); governs nothing and "
                       "depends on nothing, so it stands, as the rule's verbless case"),
                (5, 6, JOIN.format("Sub utraque specie (l.6) goes with Manet (l.5)"))],
            8: [(1, 3, JOIN.format("the participles concisus, confractus, divisus (ll.1-2) agree with "
                                   "the subject of accipitur (l.3)")),
                (4, 5, JOIN.format("l.5 has no verb: isti and ille are subjects of sumunt, sumit (l.4), "
                                   "gapped")),
                (6, 6, "own finite verb (consumitur)")],
            9: [(1, 3, JOIN.format("ll.2-3 have no verb: the ablative Sorte (l.2) and its genitives "
                                   "Vitae, interitus (l.3) go with sumunt (l.1)")),
                (4, 4, "own finite verb (est), gapped in its second half inside the line"),
                (5, 6, JOIN.format("Vide (l.5) governs the indirect question Quam sit (l.6), and paris "
                                   "sumptionis (l.5) depends on exitus (l.6)"))],
            10: [(1, 3, JOIN.format("the ablative absolute (l.1) goes with vacilles, memento (l.2), and "
                                    "memento governs Tantum esse (l.3)")),
                 (4, 4, "a correlative clause with its own finite verb (tegitur); may stand. Joining "
                        "it to ll.1-3 would keep Tantum ... Quantum together: Adam's call"),
                 (5, 5, "own finite verb (fit)"),
                 (6, 6, "own finite verb (fit)"),
                 (7, 8, JOIN.format("status, statura (l.7) are the subjects of minuitur (l.8)"))],
            11: [(1, 2, JOIN.format("no finite verb: Ecce with the nominative panis (l.1), and Factus "
                                    "(l.2) agrees with it; a complete verbless exclamation")),
                 (3, 4, JOIN.format("no finite verb (est understood): the gerundive mittendus (l.4) "
                                    "agrees with panis (l.3)")),
                 (5, 5, "own finite verb (praesignatur)"),
                 (6, 6, "a cum-clause with its own finite verb (immolatur); may stand"),
                 (7, 7, "own finite verb (deputatur)"),
                 (8, 8, "own finite verb (Datur)")],
            12: [(1, 1, "vocatives only (Bone Pastor, panis vere): governed by nothing, a row of "
                        "their own"),
                 (2, 2, "own finite verb (miserere); Jesu is its vocative"),
                 (3, 3, "own finite verbs (pasce, tuere)"),
                 (4, 5, JOIN.format("In terra viventium (l.5) goes with videre, which fac (l.4) "
                                    "governs")),
                 (6, 10, JOIN.format("Tu (l.6) is the subject of Fac (l.10), and Tuos ... commensales, "
                                     "Cohaeredes et sodales (ll.8-9) its object and predicate; the two "
                                     "relative clauses (ll.6-7) sit inside"))],
        },
    },
    "sacris-solemniis": {
        "title": "Sacris solemniis juncta sint gaudia",
        "source_file": "britt-1922-corpus-christi.json",
        "latin_source": "britt-1922-latin",
        "stanza_singable": {"source": "chambers-cento-britt-1922"},
        "stanza_literal": {"source": "britt-1922-prose-corpus-christi"},
        "cut_by": "house cut 2026-09-26 (this build), by the clause rule; unreviewed",
        "clauses": {
            1: [(1, 1, "own finite verb (sint)"),
                (2, 2, "own finite verb (sonent), coordinate by Et"),
                (3, 4, JOIN.format("l.4 has no verb: Corda, voces, et opera stand in apposition to "
                                   "omnia (l.3)"))],
            2: [(1, 1, "own finite verb (recolitur)"),
                (2, 4, JOIN.format("creditur (l.2) governs Dedisse (l.3), and indulta (l.4) agrees with "
                                   "legitima (l.3)"))],
            3: [(1, 4, JOIN.format("one period, one finite verb (fatemur, l.4): Corpus ... datum [esse] "
                                   "(l.2) is its accusative and infinitive, and ll.1 and 3 go with it"))],
            4: [(1, 1, "own finite verb (Dedit)"),
                (2, 3, JOIN.format("the participle Dicens (l.3) agrees with the subject of Dedit (l.2); "
                                   "the words it introduces share its line")),
                (4, 4, "own finite verb (bibite), the second half of the quoted words")],
            5: [(1, 1, "own finite verb (instituit)"),
                (2, 4, JOIN.format("voluit (l.2) governs committi, whose dative Solis presbyteris is on "
                                   "l.3; the Ut-clause (l.4) is the subject of congruit (l.3)"))],
            6: [(1, 1, "own finite verb (fit)"),
                (2, 2, "own finite verb (Dat)"),
                (3, 4, JOIN.format("Pauper, servus, et humilis (l.4) are the subjects of manducat (l.3)"))],
            7: [(1, 1, "own finite verb (poscimus); Deitas is its vocative"),
                (2, 2, "own finite verbs (visita, colimus)"),
                (3, 4, JOIN.format("Ad lucem (l.4) goes with duc (l.3)"))],
        },
    },
    "verbum-supernum": {
        "title": "Verbum supernum prodiens, nec Patris linquens dexteram",
        "source_file": "britt-1922-corpus-christi.json",
        "latin_source": "britt-1922-latin",
        "stanza_singable": {"source": "neale-caswall-britt-1922"},
        "stanza_literal": {"source": "britt-1922-prose-corpus-christi"},
        "cut_by": "house cut 2026-09-26 (this build), by the clause rule; unreviewed",
        "clauses": {
            1: [(1, 4, JOIN.format("the participles prodiens, linquens, exiens (ll.1-3) agree with "
                                   "Verbum, the subject of Venit (l.4)"))],
            2: [(1, 4, JOIN.format("tradendus (l.2) agrees with the subject of tradidit (l.4); ll.1 and "
                                   "3 go with it"))],
            3: [(1, 2, JOIN.format("the dative Quibus (l.1) goes with dedit (l.2)")),
                (3, 4, JOIN.format("duplicis substantiae (l.3) depends on hominem, in the Ut-clause "
                                   "whose verb is cibaret (l.4)"))],
            4: [(1, 3, JOIN.format("Convescens (l.2) and Se moriens (l.3) take dedit (l.1), gapped, as "
                                   "Britt's note reads them; their participles agree with its subject")),
                (4, 4, "own finite verb (dat)")],
            5: [(1, 1, "a vocative (O salutaris hostia): governed by nothing, a row of its own"),
                (2, 2, "a relative clause with its own finite verb (pandis); may stand"),
                (3, 3, "own finite verb (premunt)"),
                (4, 4, "own finite verbs (Da, fer)")],
            6: [(1, 2, JOIN.format("the dative Uni trinoque Domino (l.1) goes with Sit (l.2)")),
                (3, 4, JOIN.format("vitam (l.3) is the object of donet (l.4)"))],
        },
    },
}

# Where a hymn's text comes from when it is not a vault batch (README s.9).
PRINTED = os.path.join(ROOT, "data", "hymn-sources")
# Adam's answers to the cut review sheet (review.py; README s.9d). A missing
# file is no answers.
CUT_REVIEWED = os.path.join(PRINTED, "cut-reviewed.jsonl")

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
        "open": ("Adoro te was collated word by word against Britt 1922 (no. 79, pp. 190-191) on "
                 "2026-09-26: the words agree except paenitens/poenitens and the closing Amen, which "
                 "Britt does not print; the rest is orthography, one capital and punctuation "
                 "(`collation`). Every difference is on docs/review/2026-09-26-adoro-collation.md; "
                 "the text is unchanged until Adam answers. Pange lingua was checked "
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
        "checked_on": "2026-09-26",
        "finding": ("The 1918 Poems does not print this translation. Bridges's editorial note says no "
                    "translations of any kind are published in it, and the Project Gutenberg "
                    "transcription of the 1918 edition (ebook 22403) has no Adoro te. The edition named "
                    "above is therefore not where this text was printed. It first appeared in a later, "
                    "enlarged edition; no public-domain scan of one was reachable (archive.org has only "
                    "1948 and later printings; HathiTrust's catalogue refused an automated request)."),
        "open": ("Quoted from memory in the batch note, and not verifiable against the 1918 edition, "
                 "which lacks it. Verify every stanza against a printed text before any public use, and "
                 "correct `edition` to that printing (and its licence) when found."),
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

# The three hymns transcribed from Britt 1922 (data/hymn-sources/). One
# edition, one scan; `verified` means every line was read against the page
# image, not taken from the OCR (which misreads Nec, Quem and every ligature).
BRITT_1922 = ("Matthew Britt, The Hymns of the Breviary and Missal (London: Burns Oates & Washbourne; "
              "copyright 1922 Benziger Brothers, printed in U.S.A.)")
BRITT_SCAN = "archive.org/details/hymnsofbreviarym00britrich"
PRINTED_SOURCES = {
    "britt-1922-latin": {
        "what": "Latin text of Lauda Sion, Sacris solemniis and Verbum supernum prodiens",
        "edition": (f"{BRITT_1922}: no. 75 Lauda Sion, pp. 178-180; no. 77 Sacris solemniis, pp. 185-187; "
                    f"no. 78 Verbum supernum, p. 188. Scan {BRITT_SCAN} (scan pages n187-n199)"),
        "license": "PD",
        "license_basis": "13th-century text, printed 1922 (US publication before 1929)",
        "verified": True,
        "verified_on": "2026-09-26",
        "transcription": "data/hymn-sources/britt-1922-corpus-christi.json (conventions and every rejoined turnover listed there)",
        "open": ("Britt prints ae/oe ligatures and consonantal j (cœna, præconia, Hujus); they are kept as "
                 "printed, where Adoro te and Pange lingua carry the received text's cenae, iubilatio. "
                 "search_key folds both. The canonical orthography is Adam's call (Latin Hymns doc s.7, "
                 "decision 2; Caswall verification s.4)."),
    },
    "henry-britt-1922": {
        "what": "Lauda Sion: stanza-level metrical English (singable)",
        "edition": f"Monsignor Hugh T. Henry's translation, as printed in {BRITT_1922}, pp. 178-180 ({BRITT_SCAN})",
        "license": "PD",
        "license_basis": "published 1922 in the US (before 1929); translator d. 1946",
        "verified": True,
        "verified_on": "2026-09-26",
        "open": "one line-end hyphen kept as a compound (life-bringing, st2); listed in the transcription file.",
    },
    "chambers-cento-britt-1922": {
        "what": "Sacris solemniis: stanza-level metrical English (singable)",
        "edition": (f"'a cento based on the translation by J. D. Chambers', as printed in {BRITT_1922}, "
                    f"pp. 185-187 ({BRITT_SCAN})"),
        "license": "PD",
        "license_basis": "published 1922 in the US (before 1929); Chambers d. 1893; the cento's arranger is not named",
        "verified": True,
        "verified_on": "2026-09-26",
    },
    "neale-caswall-britt-1922": {
        "what": "Verbum supernum prodiens: stanza-level metrical English (singable)",
        "edition": (f"J. M. Neale (st. 1-4) and Edward Caswall (st. 5-6), as printed in {BRITT_1922}, "
                    f"p. 188 ({BRITT_SCAN})"),
        "license": "PD",
        "license_basis": "published 1922 in the US (before 1929); Neale d. 1866, Caswall d. 1878",
        "verified": True,
        "verified_on": "2026-09-26",
    },
    "britt-1922-prose-corpus-christi": {
        "what": "Lauda Sion, Sacris solemniis, Verbum supernum: stanza-level literal prose (the PD candidate for `elegant`)",
        "edition": (f"{BRITT_1922}, the quoted prose of the numbered notes: pp. 181-183, 187-188, 189-190 "
                    f"({BRITT_SCAN})"),
        "license": "PD",
        "license_basis": "published 1922 in the US (before 1929)",
        "verified": True,
        "verified_on": "2026-09-26",
    },
    "house-cut-2026-09-26": {
        "what": "the clause cut of Lauda Sion, Sacris solemniis and Verbum supernum",
        "edition": "build_hymn_corpus.py HYMNS[...]['clauses'], every cut with its reason in `cut.why`",
        "license": "own",
        "verified": False,
        "open": "unchecked by Adam: every cut is on docs/review/2026-09-26-thomas-cuts.md.",
    },
}

# Declared in the manifest only once an override is applied (none yet).
ADAM_REVIEWED = {
    "what": "token lemma and/or parsing: Adam's answers to the lemma review sheet",
    "edition": "data/lemmas/adam-reviewed.jsonl (pipeline/README-lemma-spine.md s.8)",
    "license": "own",
    "verified": True,
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
    "gloss": ("house-draft-2026-09-14: the wooden gloss, Latin order. Null on the hymns printed from "
              "Britt 1922, which have no house draft: a gloss is house work and none is invented"),
    "plain_form": "house-retrofit-2026-09-15; null where the gloss serves as-is",
}
# The printed hymns (no draft): lemma and parsing by lemma_spine.resolve_undrafted.
TOKEN_FIELDS_UNDRAFTED = ("lemma: whitaker-words only where WORDS has exactly one entry for the form "
                          "(status `sole`), else null and flagged; parsing: whitaker-words only where "
                          "that entry gives exactly one parse, else null (status `ambiguous`, not "
                          "flagged). Per token: provenance. README-lemma-spine.md s.3b")

PERSEUS = {
    "policy": ("Perseus is CC BY-SA. Nothing from Perseus is in these files. Perseus "
               "enrichment (lemmata, morphology, treebank links) is a separate layer "
               "keyed by CTS URN and joined at read time, never merged in."),
    "cts_urn": {f"hymns:{k}": None for k in HYMNS},
    "note": "No hymn here has a Perseus/CTS edition; the URN is null, not guessed.",
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


def render_plain(tokens, plain, proper=PROPER):
    """`plain` is the en.plain witness row. Never stored; always this.
    `proper` is the capital-keeping list; another dataset may extend it
    (build_nt_corpus.render_plain), the hymns always use PROPER."""
    if plain.get("plain_override"):
        return plain["plain_override"]
    parts = []
    for step in plain["prose_order"]:
        if isinstance(step, str):
            parts.append("[" + step + "]")
            continue
        tok = tokens[step - 1]
        word = tok["plain_form"] or tok["gloss"]
        if not any(p in word for p in proper):
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


# ---------------------------------------------------------------------------
# The printed hymns: text from data/hymn-sources/, no house draft (README s.9)
# ---------------------------------------------------------------------------

# Why a printed hymn's clause has only its Latin (the reader shows these).
NOT_STORED = {
    "en.wooden": "no token glosses: there is no house draft for this hymn, and a gloss is house work",
    "en.plain": ("no prose_order: the plain order is house work (as for the Greek before its draft), "
                 "and no source supplies one"),
    "en.elegant": "none at clause level: Britt's prose renders the stanza, and is stored there as en.literal",
}
PRINTED_STATUS = "text verified against Britt 1922; cut and lemmas unchecked"

ADAM_REVIEWED_CUT = {
    "what": "the clause cut of a printed hymn: Adam's answers to the cut review sheet",
    "edition": "data/hymn-sources/cut-reviewed.jsonl (review.py; README-hymn-jsonl.md s.9d)",
    "license": "own",
    "verified": True,
}
CUT_KEYS = {"stanza", "cut", "why", "reviewed_on", "note"}


def load_cut_reviews(path=None):
    """{stanza citation: row}. Malformed is a hard stop: an answer that cannot
    be applied must not be dropped."""
    path = path or CUT_REVIEWED
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            where = f"cut-reviewed.jsonl:{n}"
            if set(row) - CUT_KEYS or not {"stanza", "cut", "reviewed_on"} <= set(row):
                _stop(f"{where}: fields must be {sorted(CUT_KEYS)} (stanza, cut, reviewed_on required)")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["reviewed_on"]):
                _stop(f"{where}: reviewed_on must be YYYY-MM-DD")
            if row["stanza"] in out:
                _stop(f"{where}: {row['stanza']} is answered twice")
            out[row["stanza"]] = row
    return out


def partition_problem(cut, n_lines):
    """None when `cut` ([[a, b], ...]) partitions lines 1..n exactly."""
    expect = 1
    for a, b in cut:
        if a != expect or b < a:
            return f"lines {a}-{b} do not continue the partition at line {expect}"
        expect = b + 1
    if expect - 1 != n_lines:
        return f"the cut covers {expect - 1} of {n_lines} lines"
    return None


def effective_cut(st_cit, draft, row, n_lines):
    """[(a, b, why, review)] for a stanza: the draft cut, or Adam's answer.
    A re-cut keeps a draft clause's reason where its lines are unchanged; a
    new join must carry a reason of Adam's (`why`, or the row's `note`)."""
    if not row:
        return [(a, b, why, {"review": "open"}) for a, b, why in draft]
    prob = partition_problem(row["cut"], n_lines)
    if prob:
        _stop(f"{st_cit}: reviewed cut: {prob}")
    reasons = {(a, b): why for a, b, why in draft}
    stamp = {"review": "adam-reviewed", "reviewed_on": row["reviewed_on"]}
    if row.get("note"):
        stamp["note"] = row["note"]
    out = []
    for a, b in row["cut"]:
        why = (row.get("why") or {}).get(f"{a}-{b}") or reasons.get((a, b))
        if not why and row.get("note"):
            why = "Adam's cut: " + row["note"]
        if b > a and not why:
            _stop(f"{st_cit}: reviewed cut joins lines {a}-{b} with no reason (`why` or `note`)")
        out.append((a, b, why, dict(stamp)))
    return out


def clause_uid(reg, cit, lines, draft_lines, reviewed):
    """The clause's uid. A reviewed re-cut that puts different lines under a
    clause citation the draft already minted must not let the old uid mean new
    words: the citation is re-issued a fresh uid and the old one is recorded
    as superseded by it (wh_uid: never reused, never silently repointed).
    Returns (uid, superseded uid or None)."""
    old = reg.map.get(cit)
    if (reviewed and old and tuple(lines) != draft_lines
            and old not in set(reg.superseded.values())):
        new = reg.mint_free()
        reg.map[cit] = new
        reg.record_supersede(old, new)
        return new, old
    uid = reg.uid_for(cit)
    prior = next((o for o, n in reg.superseded.items() if n == uid), None)
    return uid, prior


def build_printed(key, H, reg, spine, overrides, used, cut_rows, inputs,
                  passages, witnesses, tokens, alignments):
    """One hymn from its printed-source file. Same records as the batch
    hymns, minus what only a house draft could supply."""
    path = os.path.join(PRINTED, H["source_file"])
    doc, sha = _load(PRINTED, H["source_file"])
    inputs[H["source_file"]] = sha
    work = f"hymns:{key}"
    if key not in doc["hymns"]:
        _stop(f"{work}: not in {path}")
    stanzas = doc["hymns"][key]["stanzas"]
    if sorted(s["stanza"] for s in stanzas) != sorted(H["clauses"]):
        _stop(f"{work}: stanza set in {H['source_file']} does not match the CLAUSES table")
    for sp in sorted(stanzas, key=lambda s: s["stanza"]):
        n = sp["stanza"]
        st_cit = f"{work}.st{n}"
        st_uid = reg.uid_for(st_cit)
        lines = sp["la"]
        if any(not l.strip() or "\n" in l for l in lines):
            _stop(f"{st_cit}: a blank or broken Latin line")
        draft = H["clauses"][n]
        if partition_problem([(a, b) for a, b, _ in draft], len(lines)):
            _stop(f"{st_cit}: {partition_problem([(a, b) for a, b, _ in draft], len(lines))}")
        cut = effective_cut(st_cit, draft, cut_rows.get(st_cit), len(lines))
        stanza_at = len(passages)
        clause_uids = []
        for ci, (a, b, why, review) in enumerate(cut, 1):
            if b > a and not why:
                _stop(f"{st_cit} c{ci}: lines joined with no reason recorded")
            cit = f"{st_cit}.c{ci}"
            draft_lines = tuple(draft[ci - 1][:2]) if ci <= len(draft) else None
            uid, prior = clause_uid(reg, cit, (a, b), draft_lines, review["review"] != "open")
            clause_uids.append(uid)
            text = "\n".join(lines[a - 1:b])
            c = {"by": H["cut_by"], "why": why, **review}
            if prior:
                c["supersedes"] = prior
            passages.append({
                "uid": uid, "citation": cit, "kind": "passage", "unit": "clause",
                "work": work, "stanza_uid": st_uid, "stanza": n, "clause": ci,
                "lines": [a, b], "grade": None, "memorize": None,
                "reading_of_record": "la.1", "cut": c, "notes": [],
                "status": PRINTED_STATUS,
            })
            witnesses.append({
                "address": U.address(uid, "la.1"), "passage_uid": uid, "name": "la.1",
                "lang": "la", "role": "original", "register": "medieval-latin",
                "text": text, "generated": False, "source": H["latin_source"],
                "attested": "Y", "reading_of_record": True, "page": sp["page"],
            })
            on_line = [li for li in range(a, b + 1) for _ in tokenize(lines[li - 1])]
            for i, surface in enumerate(tokenize(text), 1):
                skey = search_key(normalized(surface))
                if skey not in spine:
                    _stop(f"{cit} t{i:02d}: {skey!r} has no row in the lemma spine; "
                          "run pipeline/build_lemma_spine.py")
                lemma, lemma_key, parsing, prov, rv = resolve_undrafted(spine[skey])
                addr = U.address(uid, f"la.1.t{i:02d}")
                if addr in overrides:
                    try:
                        lemma, lemma_key, parsing, prov, rv = apply_override(
                            (lemma, lemma_key, parsing, prov, rv), surface, spine[skey], overrides[addr])
                    except ValueError as e:
                        _stop(f"lemma overrides: {e}")
                    used.add(addr)
                tokens.append({
                    "address": addr, "passage_uid": uid,
                    "witness": "la.1", "position": i, "line": on_line[i - 1],
                    "surface": surface,
                    "normalized": normalized(surface),
                    "search_key": skey,
                    "translit": None,
                    "lemma": lemma,
                    "lemma_key": lemma_key,
                    "parsing": parsing,
                    "gloss": None,
                    "plain_form": None,
                    "syntax": None,
                    "legacy_address": None,
                    "provenance": prov,
                    "review": rv,
                })
        passages.insert(stanza_at, {
            "uid": st_uid, "citation": st_cit, "kind": "passage", "unit": "stanza",
            "work": work, "stanza": n, "lines": [1, len(lines)],
            "clauses": clause_uids, "grade": None, "memorize": None,
            "teacher_notes": None, "status": PRINTED_STATUS, "page": sp["page"],
        })
        renderings = [("en.singable", "singable", "\n".join(sp["en_singable"]),
                       H["stanza_singable"]["source"], sp["en_page"]),
                      ("en.literal", "literal-prose", sp["en_literal"],
                       H["stanza_literal"]["source"], sp["literal_page"])]
        for name, role, text, source, page in renderings:
            if not text or not text.strip():
                _stop(f"{st_cit}: {name} is empty in {H['source_file']}")
            witnesses.append({
                "address": U.address(st_uid, name), "passage_uid": st_uid, "name": name,
                "lang": "en", "role": role, "text": text, "generated": False,
                "source": source, "attested": "Y", "reading_of_record": False, "page": page})
            alignments.append({
                "alignment_id": f"{U.address(st_uid, name)}~la.1",
                "level": "section", "type": f"1:{'many' if len(clause_uids) > 1 else '1'}",
                "a": [{"address": U.address(st_uid, name), "tokens": None}],
                "b": [{"address": U.address(u, "la.1"), "tokens": None} for u in clause_uids],
                "confidence": "high", "note": None,
            })


# ---------------------------------------------------------------------------
# Collation: a batch hymn's received Latin against a named PD printing
# (README s.10). Nothing here changes the text; it measures it.
# ---------------------------------------------------------------------------

# work slug -> the printed text it is collated against (data/hymn-sources/)
COLLATIONS = {"adoro-te": "britt-1922-adoro-te.json"}
# Adam's answers to the collation sheet (review.py). A missing file is no answers.
COLLATION_REVIEWED = os.path.join(PRINTED, "collation-reviewed.jsonl")
COLLATION_SHEET = "docs/review/2026-09-26-adoro-collation.md"
COLLATION_READINGS = ("received", "britt")
COLLATION_KEYS = {"id", "reading", "reviewed_on", "note"}
# What each kind of difference is. `orthography` and `capital` leave the
# search_key unchanged; `spelling` and `word` do not.
COLLATION_KINDS = {
    "orthography": "the same word in another spelling convention (ae/æ, oe/œ, i/j): search_key identical",
    "spelling": "the same word, spelled differently: search_key differs",
    "capital": "the same word, capitalised differently",
    "punctuation": "the punctuation after (or before) the word differs",
    "word": "a word one printing has and the other lacks, or a different word",
}


def _core(word):
    core = word.strip(PUNCT)
    i = word.find(core) if core else len(word)
    return core, word[:i], word[i + len(core):]


def collate(doc, passages, witnesses, tokens):
    """Every difference between a batch hymn's la.1 text and the printed text
    in `doc`, word by word, per stanza line. Words are paired after aligning
    on search_key (difflib), so a word one side lacks shows as a `word`
    difference and does not shift the rest. Returns (differences, stats); a
    difference is {id, stanza, line, address, kind, received, britt, page}.
    The id is the received token's address and the kind, or, for a word only
    the printing has, its stanza, line and position there."""
    import difflib
    work = doc["work"]
    ps = [p for p in passages if p["work"] == work]
    by_uid = {p["uid"]: p for p in ps}
    text = {w["passage_uid"]: w["text"] for w in witnesses if w["name"] == "la.1"}
    toks = {}
    for t in tokens:
        toks.setdefault(t["passage_uid"], []).append(t)
    printed = {s["stanza"]: s for s in doc["stanzas"]}
    stanzas = sorted((p for p in ps if p["unit"] == "stanza"), key=lambda p: p["stanza"])
    if sorted(printed) != [p["stanza"] for p in stanzas]:
        _stop(f"{work}: the collation file's stanzas do not match the corpus's")
    diffs = []
    stats = {"received_words": 0, "printed_words": 0, "paired": 0, "identical": 0}
    for st in stanzas:
        n, sp = st["stanza"], printed[st["stanza"]]
        # the received lines, each word with its token address
        lines = []
        for u in st["clauses"]:
            queue = list(toks[u])
            for line in text[u].split("\n"):
                words = []
                for w in line.split():
                    if w.strip(PUNCT):
                        words.append((w, queue.pop(0)["address"]))
                lines.append(words)
            if queue:
                _stop(f"{by_uid[u]['citation']}: tokens left over after its text")
        if len(lines) != len(sp["la"]):
            _stop(f"{work} st{n}: {len(lines)} received lines, {len(sp['la'])} printed")
        for li, (rec, pline) in enumerate(zip(lines, sp["la"]), 1):
            pw = pline.split()
            stats["received_words"] += len(rec)
            stats["printed_words"] += len(pw)
            ka = [search_key(normalized(_core(w)[0])) for w, _ in rec]
            kb = [search_key(normalized(_core(w)[0])) for w in pw]
            sm = difflib.SequenceMatcher(None, ka, kb, autojunk=False)
            pairs, extra = [], []
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op in ("equal", "replace") and i2 - i1 == j2 - j1:
                    pairs += list(zip(range(i1, i2), range(j1, j2)))
                else:
                    extra += [(i, None) for i in range(i1, i2)] + [(None, j) for j in range(j1, j2)]
            for i, j in pairs:
                (rw, addr), bw = rec[i], pw[j]
                rc, rpre, rpost = _core(rw)
                bc, bpre, bpost = _core(bw)
                stats["paired"] += 1
                if rw == bw:
                    stats["identical"] += 1
                    continue
                if rc != bc:
                    kind = ("capital" if rc.lower() == bc.lower() else
                            "orthography" if search_key(rc) == search_key(bc) else
                            "spelling" if search_key(rc)[:1] == search_key(bc)[:1] else "word")
                    diffs.append({"kind": kind, "received": rc, "britt": bc, "address": addr,
                                  "stanza": n, "line": li})
                if (rpre, rpost) != (bpre, bpost):
                    diffs.append({"kind": "punctuation", "received": rw, "britt": bw, "address": addr,
                                  "stanza": n, "line": li})
            for i, j in extra:
                if i is not None:
                    diffs.append({"kind": "word", "received": rec[i][0], "britt": None,
                                  "address": rec[i][1], "stanza": n, "line": li})
                else:
                    diffs.append({"kind": "word", "received": None, "britt": pw[j], "address": None,
                                  "stanza": n, "line": li, "at": j + 1})
    out = []
    for d in diffs:
        d["id"] = (f"{d['address']}:{d['kind']}" if d["address"]
                   else f"{work}.st{d['stanza']}.l{d['line']}.w{d.pop('at')}:{d['kind']}")
        d["page"] = printed[d["stanza"]]["page"]
        out.append({k: d.get(k) for k in ("id", "stanza", "line", "address", "kind",
                                           "received", "britt", "page")})
    if len({d["id"] for d in out}) != len(out):
        _stop(f"{work}: two collation differences share an id")
    return out, stats


def load_collation_reviews(path=None):
    """{difference id: row}. Malformed is a hard stop, as for the cut answers."""
    path = path or COLLATION_REVIEWED
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            where = f"collation-reviewed.jsonl:{n}"
            if set(row) - COLLATION_KEYS or not {"id", "reading", "reviewed_on"} <= set(row):
                _stop(f"{where}: fields must be {sorted(COLLATION_KEYS)} (id, reading, reviewed_on required)")
            if row["reading"] not in COLLATION_READINGS:
                _stop(f"{where}: reading must be one of {COLLATION_READINGS}")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["reviewed_on"]):
                _stop(f"{where}: reviewed_on must be YYYY-MM-DD")
            if row["id"] in out:
                _stop(f"{where}: {row['id']} is answered twice")
            out[row["id"]] = row
    return out


def collation_block(key, passages, witnesses, tokens):
    """The verification fields a collation adds to the received text's source
    record: what was compared, how many words, every kind of difference, and
    where Adam's answers stand. Returns (block, all answered `received`,
    latest reviewed_on). An answer for Britt's reading is recorded, not
    applied: the text is the batch note's, and a change to it is made there."""
    doc, sha = _load(PRINTED, COLLATIONS[key])
    diffs, stats = collate(doc, passages, witnesses, tokens)
    ids = {d["id"] for d in diffs}
    answers = load_collation_reviews()
    stale = sorted(set(answers) - ids)
    if stale:
        _stop(f"collation answers name differences that do not exist: {stale[:5]}")
    kinds = {k: sum(1 for d in diffs if d["kind"] == k) for k in COLLATION_KINDS}
    by_reading = {r: sum(1 for x in answers.values() if x["reading"] == r) for r in COLLATION_READINGS}
    read = doc["scan"]["pages_read"]
    block = {
        "against": (f"Matthew Britt, The Hymns of the Breviary and Missal (1922), no. "
                    f"{doc['edition']['britt_number']}, pp. {read[0]['page']}-{read[-1]['page']} "
                    f"(scan {BRITT_SCAN} {read[0]['scan_page']}-{read[-1]['scan_page']}), "
                    "read from the page images"),
        "file": "data/hymn-sources/" + COLLATIONS[key],
        "file_sha256": sha,
        "collated_on": doc["transcription"]["on"],
        "words": stats,
        "differences": len(diffs),
        "by_kind": {k: v for k, v in kinds.items() if v},
        "search_key_changes": sum(1 for d in diffs if d["kind"] in ("spelling", "word")),
        "kinds": {k: COLLATION_KINDS[k] for k, v in kinds.items() if v},
        "review": {"sheet": COLLATION_SHEET,
                   "answers": "data/hymn-sources/collation-reviewed.jsonl",
                   "answered": len(answers), "open": len(diffs) - len(answers), **by_reading},
    }
    done = bool(diffs) and len(answers) == len(diffs) and not by_reading["britt"]
    return block, done, max((r["reviewed_on"] for r in answers.values()), default=None)


def build(src, reg):
    passages, witnesses, tokens, alignments = [], [], [], []
    inputs = {}
    spine, spine_sha = load_spine()
    try:
        overrides = load_overrides()
    except ValueError as e:
        _stop(f"lemma overrides: {e}")
    used = set()
    legacy_map = {}          # legacy unit_id -> clause uid (the join, done once)

    cut_rows = load_cut_reviews()
    for key, H in HYMNS.items():
        if "source_file" in H:
            build_printed(key, H, reg, spine, overrides, used, cut_rows, inputs,
                          passages, witnesses, tokens, alignments)
            continue
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
                    addr = U.address(uid, f"la.1.t{i:02d}")
                    if addr in overrides:
                        try:
                            lemma, lemma_key, parsing, prov, review = apply_override(
                                (lemma, lemma_key, parsing, prov, review), st["surface"],
                                spine[skey], overrides[addr])
                        except ValueError as e:
                            _stop(f"lemma overrides: {e}")
                        used.add(addr)
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

    stale = sorted(set(overrides) - used)
    if stale:
        _stop(f"lemma overrides name tokens that do not exist: {stale[:5]}")
    stale_cuts = sorted(set(cut_rows) - {p["citation"] for p in passages if p["unit"] == "stanza"})
    if stale_cuts:
        _stop(f"cut review rows name stanzas that do not exist: {stale_cuts[:5]}")
    if cut_rows:
        with open(CUT_REVIEWED, "rb") as f:
            inputs["cut-reviewed.jsonl"] = hashlib.sha256(f.read()).hexdigest()
    sources = dict(SOURCES)
    for key in COLLATIONS:
        block, done, on = collation_block(key, passages, witnesses, tokens)
        rec = dict(sources["roman-missal-received"])
        rec["collation"] = {**rec.get("collation", {}), f"hymns:{key}": block}
        if done:
            rec.update(verified=True, verified_on=on)
        sources["roman-missal-received"] = rec
    if any("source_file" in H for H in HYMNS.values()):
        sources.update(PRINTED_SOURCES)
        if cut_rows:
            sources[OVERRIDE_SOURCE + "-cut"] = ADAM_REVIEWED_CUT
    if used:
        sources[OVERRIDE_SOURCE] = ADAM_REVIEWED
        with open(OVERRIDES, "rb") as f:
            inputs["adam-reviewed.jsonl"] = hashlib.sha256(f.read()).hexdigest()

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
                                 "cut_by": H["cut_by"],
                                 **({"source_file": "data/hymn-sources/" + H["source_file"],
                                     "token_fields": TOKEN_FIELDS_UNDRAFTED,
                                     "not_stored": NOT_STORED} if "source_file" in H else {})}
                  for k, H in HYMNS.items()},
        "licence_gate": {"allowed": list(ALLOWED_LICENSES),
                         "rule": "launch plan D4 / ADR 0001: public-domain editions or own work only"},
        "sources": sources,
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
