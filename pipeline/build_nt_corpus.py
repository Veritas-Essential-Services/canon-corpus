#!/usr/bin/env python3
# prov: 2026-09-26 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
# prov: 2026-09-26 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
# fable_review: pending
"""
build_nt_corpus.py -- the Greek New Testament in the four-file corpus format,
one row per VERSE, every record keyed by uid. The whole NT since 2026-10-02,
one folder per book (data/nt/<Book>/); the John 1:1-18 pilot is a labelled
pericope inside it. Two rulings are house defaults until Adam makes them:
VERSIFICATION_MAP (the Romans doxology) and SHARD (README s.16).

    python3 pipeline/build_nt_corpus.py --fetch     # pinned inputs -> data/corpus/ (sha256-checked)
    python3 pipeline/build_nt_corpus.py             # build, write data/nt/
    python3 pipeline/build_nt_corpus.py --check     # rebuild, assert 0 minted
                                                    #   and byte-identical output
    python3 pipeline/build_nt_corpus.py --report    # stats only, no write
    python3 pipeline/build_nt_corpus.py --survey    # the WHOLE NT, measured, never
                                                    #   written: what a full run would hit

    Output: data/nt/<Book>/{passages,witnesses,tokens,alignments}.jsonl + one
    data/nt/manifest.json. Read it with load_nt(), which follows the manifest.
    Schema: pipeline/README-nt-jsonl.md (the hymn schema, with the differences
    written down).  Validator: tests/nt_corpus_test.py.

THE SOURCE, AND WHY IT PASSES THE HOUSE RULE (ADR 0001, launch plan D4)
    The Robinson-Pierpont Byzantine Textform, from its official home
    (github.com/byztxt/byzantine-majority-text), pinned at release v3.3.2 =
    commit 27a45ff (2024-12-31), the RP2018 text. Public domain on the
    editors' own statement, read 2026-09-26; the exact wording is in SOURCES
    below and in the manifest. Its parsing codes and Strong's numbers are
    Robinson's own work in the same repo, under the same statement.

    Lemmas come from Strong's Greek Dictionary (1890, "Public Domain -- Copy
    Freely" in the file's own prologue), looked up by the Strong's number
    Robinson assigns each word. That file is byte-identical to the one this
    repo already ingests as `strongs-greek` (same sha256).

    Glosses come from the same Strong's entry by a fixed rule
    (strongs_gloss.py; README s.12): a DICTIONARY gloss, not a contextual
    translation. Where no rule fires the gloss is null and counted. A later
    contextual layer (data/nt/gloss-overrides.jsonl, `adam-reviewed` or
    `house`) replaces it, the dictionary value kept under `was`.

    The plain line walks a house prose_order (data/nt/prose-order.jsonl), the
    hymns' convention exactly: each row becomes an `en.plain` witness carrying
    prose_order / absorbed / plain_override, text null. Today every row of
    both files is a DRAFT (`draft: true`; source `house-draft` / layer
    `house`, licence own) awaiting Adam's review, and the manifest says so.

    NOT in these files, by rule: MorphGNT/SBLGNT (morphology CC BY-SA 3.0;
    the SBLGNT text CC BY 4.0, which waits on ADR 0019) and Perseus (CC
    BY-SA 4.0, a separate layer by CTS URN). Named in the manifest as future
    enrichment layers, with their licences, and nothing more.

IDENTITY: THE VERSE ALREADY HAS ONE
    A Greek verse and a KJV verse are two witnesses of ONE passage (house
    style s.2: "two editions are still two witnesses of one passage"). John
    1:1 has carried wh-AGJ6YAF47Q since 2026-09-17. So this build MINTS
    NOTHING: it opens the registry FROZEN and asks it for `kjv:John.1.N`. A
    Greek verse with no KJV uid is a versification question -- a hard stop,
    never a fresh uid. The citation slug `kjv` names the versification of
    record, not the language of the passage (see the README, s.1).

NOTHING IS GUESSED
    RP ships each verse twice: accented with punctuation (CCAT), and
    unaccented with Strong's numbers and parsing (BP5). The tokens need both,
    so the build pairs them word for word and stops on any word whose letters
    differ. It also re-reads Robinson's own Beta-code files (the repo's
    source of truth; the Unicode CSVs are its converter's output) and stops
    if a CSV word's letters or codes differ from them. Parsing is Robinson's,
    verbatim; where he gives two (John 1:9), both are kept and the token is
    flagged, not resolved.
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import unicodedata
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import wh_uid as U  # noqa: E402
import strongs_gloss as G  # noqa: E402

UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")
OUT = os.path.join(ROOT, "data", "nt")
FILES = ("passages", "witnesses", "tokens", "alignments")
SCHEMA = "wordhoard/corpus-jsonl/v1"
BUILT_ON = "2026-09-26"   # the device clock; a constant so a rebuild is byte-identical

WITNESS = "grc.byz"       # what the rendering IS: Greek, Byzantine textform
PLAIN = "en.plain"        # the plain line: the tokens walked in a house prose_order
PROSE_ORDERS = os.path.join(ROOT, "data", "nt", "prose-order.jsonl")
REVIEW_DOC = "docs/review/2026-09-26-john1-drafts.md"
FACING = "kjv.plain"      # the KJV book's reading of record (build_witnesses.py)

# ---------------------------------------------------------------------------
# Pinned inputs. sha256 measured 2026-09-26; a mismatch is a hard stop.
# ---------------------------------------------------------------------------

BYZ_TAG = "v3.3.2"
BYZ_COMMIT = "27a45ff1b7be6c17ccbfeac414f3f55732ae8e28"
BYZ_RAW = "https://raw.githubusercontent.com/byztxt/byzantine-majority-text/" + BYZ_COMMIT + "/"
STRONGS_COMMIT = "0acd2f251c2d35ff8db2dece4e0593979d3ac223"
STRONGS_RAW = "https://raw.githubusercontent.com/openscriptures/strongs/" + STRONGS_COMMIT + "/"
STRONGS_XML = "greek/StrongsGreekDictionaryXML_1.4/strongsgreek.xml"

CACHE = {"byz": os.path.join(ROOT, "data", "corpus", "byztxt", BYZ_COMMIT[:12]),
         "strongs": os.path.join(ROOT, "data", "corpus", "strongs-greek", STRONGS_COMMIT[:12])}

PINS = {
    ("byz", "LICENSE.txt"): "04e731724d985529bf93ebbe46d8b91fbf3cd9171504e64c73eeb2bafdeb711e",
    ("byz", "README.md"): "e392e0b871e515bdc347933e12484e7a3b4a7002db760b0fc91ecefe6278a9b1",
    ("byz", "source/README.md"): "8f9fe05bcb9eb172ecdf4a14275ef17a1c2bcbe5c947e339fb07e7a5f21b47cb",
    ("strongs", STRONGS_XML): "df928f01b37632f8af9f16289ce58d10b958014cb5dbd1e1ea715a8d311a0625",
}
# The 108 book files (27 books x 4), measured 2026-10-02 at BYZ_COMMIT. Kept in
# their own file so the list stays readable; same rule: a mismatch stops.
BOOK_PINS = os.path.join(HERE, "nt_pins.json")
with open(BOOK_PINS, encoding="utf-8") as _f:
    _bp = json.load(_f)
if _bp["commit"] != BYZ_COMMIT:
    raise SystemExit(f"nt_pins.json is for {_bp['commit']}, not BYZ_COMMIT {BYZ_COMMIT}")
PINS.update({("byz", rel): sha for rel, sha in _bp["files"].items()})

# byztxt file stem -> (source number, OSIS book), in canonical order: the
# order the build reads them, the shards are listed in, and load_nt() returns.
BOOKS = [("MAT", "01", "Matt"), ("MAR", "02", "Mark"), ("LUK", "03", "Luke"),
         ("JOH", "04", "John"), ("ACT", "05", "Acts"), ("ROM", "06", "Rom"),
         ("1CO", "07", "1Cor"), ("2CO", "08", "2Cor"), ("GAL", "09", "Gal"),
         ("EPH", "10", "Eph"), ("PHP", "11", "Phil"), ("COL", "12", "Col"),
         ("1TH", "13", "1Thess"), ("2TH", "14", "2Thess"), ("1TI", "15", "1Tim"),
         ("2TI", "16", "2Tim"), ("TIT", "17", "Titus"), ("PHM", "18", "Phlm"),
         ("HEB", "19", "Heb"), ("JAM", "20", "Jas"), ("1PE", "21", "1Pet"),
         ("2PE", "22", "2Pet"), ("1JO", "23", "1John"), ("2JO", "24", "2John"),
         ("3JO", "25", "3John"), ("JUD", "26", "Jude"), ("REV", "27", "Rev")]
BOOK = {stem: (num, osis) for stem, num, osis in BOOKS}
BOOK_OSIS = {osis for _, _, osis in BOOKS}

# What the build covers: every book (2026-10-02; the pilot was John 1:1-18).
# build() takes a narrowed list (tests, --report), but main() refuses to WRITE
# or --check one: the manifest would lose the other books, the way a partial
# build once rewrote data/books/manifest.json (CLAUDE.md, 2026-09-06).
SCOPE = [stem for stem, _, _ in BOOKS]

# The pilot pericope. A label, not an identity (nothing is minted for it): the
# verses in it carry `pericope`, and the reader and the John 1 review sheet
# read just these (load_nt(pericope=...)). Every other verse's pericope is null.
PILOT = {"stem": "JOH", "osis_book": "John", "chapter": 1, "first": 1, "last": 18,
         "pericope": "John.1.1-18", "title": "The Prologue of John"}

# ---------------------------------------------------------------------------
# The two rulings a full run needed, both still Adam's to make (2026-10-02).
# Each is a house DEFAULT, written so that changing it is one edit here and a
# rebuild; nothing downstream hard-codes either answer.
# ---------------------------------------------------------------------------

# Ruling 1, the Romans doxology. RP prints it as Rom 14:24-26; the KJV as Rom
# 16:25-27. Default (README s.10's recommendation): it is ONE passage whose
# position differs, so the Greek verses are witnesses of the KJV verses' uids,
# and each such witness records where RP places it (`rp_ref`). Rows stay in
# RP's reading order, so in the Rom shard they follow 14:23.
#   To rule the other way, set the values to None: those RP verses are then
#   left out (counted in the manifest, never given a fresh uid), and KJV Rom
#   16:25-27 simply have no grc.byz witness, like Acts 8:37.
VERSIFICATION_MAP = {"Rom.14.24": "Rom.16.25", "Rom.14.25": "Rom.16.26", "Rom.14.26": "Rom.16.27"}
VERSIFICATION_RULING = {
    "status": "house default, awaiting Adam's ruling",
    "default": ("the doxology is one passage: RP Rom 14:24-26 are witnesses of the KJV uids of "
                "Rom 16:25-27, each witness recording RP's own reference as rp_ref"),
    "alternative": ("set VERSIFICATION_MAP's values to None in build_nt_corpus.py and rebuild: the "
                    "three RP verses are left out and counted; nothing is minted either way"),
    "doc": "pipeline/README-nt-jsonl.md s.10, s.16",
}

# Ruling 2, file sharding. 140,149 tokens at ~540 bytes is ~76 MB, over
# GitHub's 50 MB warning as one file. Default: one folder per book,
# data/nt/<OSIS book>/{passages,witnesses,tokens,alignments}.jsonl, with one
# manifest.json over all of them (its `shards` block lists the folders in
# canonical order; load_nt() reads through it, so no consumer names a path).
#   SHARD = None writes the four flat files instead (the pilot's layout).
SHARD = "book"
SHARD_RULING = {
    "status": "house default, awaiting Adam's ruling",
    "default": ("one folder per book (data/nt/<OSIS book>/), the four files in each; one manifest "
                "over all of them; token records unchanged (provenance stays on every token)"),
    "alternatives": ["SHARD = None: four flat files (tokens.jsonl would be ~76 MB)",
                     "move the constant provenance to the manifest (README s.10; a schema change)",
                     "gitignore the tokens and rebuild them from the pins, as data/books/ is"],
    "doc": "pipeline/README-nt-jsonl.md s.10, s.16",
}

SOURCES = {
    "rp2018-byztxt": {
        "what": "Greek text (accented, punctuated), Strong's numbers and parsing codes",
        "edition": ("Maurice A. Robinson and William G. Pierpont, The New Testament in the "
                    "Original Greek: Byzantine Textform, 2018 edition, as maintained at "
                    f"github.com/byztxt/byzantine-majority-text, release {BYZ_TAG} "
                    f"(commit {BYZ_COMMIT[:7]}, 2024-12-31)"),
        "license": "PD",
        "license_basis": [
            {"where": "github.com/byztxt/byzantine-majority-text README.md, section 'Copyright'",
             "says": "All the code and text contained in this folder is in the Public Domain."},
            {"where": "github.com/byztxt/byzantine-majority-text LICENSE.txt",
             "says": ("The Unlicense: \"This is free and unencumbered software released into the "
                      "public domain.\"")},
            {"where": ("github.com/byztxt/robinson-documentation README.md (Robinson's parsing "
                       "documentation; commit 3bc6f03), section 'License?'"),
             "says": "Public Domain.  Copy freely."},
            {"where": ("RP2005 printed edition, copyright page (archive.org "
                       "newtestamentrobinsonpierpontbyzantine, OCR text layer)"),
             "says": ("Anyone is permitted to copy and distribute this text or any portion of this "
                      "text. It may be incorporated in a larger work, and/or quoted from, stored in "
                      "a database retrieval system, photocopied, reprinted, or otherwise duplicated "
                      "by anyone without prior notification, permission, compensation to the "
                      "holder, or any other restrictions. All rights to this text are released to "
                      "everyone and no one can reduce these rights at any time. Copyright is not "
                      "claimed nor asserted for the new and revised form of the Greek NT text of "
                      "this edition, nor for the original form of such as initially released into "
                      "the public domain by the editors, first as printed textual notes in 1979 "
                      "and in continuous-text electronic form in 1986.")},
            {"where": ("RP2018 printed edition, copyright page (archive.org "
                       "robinson-pierpont-2018-gnt-edition; item licence CC0 1.0)"),
             "says": ("Same release as 2005, extended to the 2018 preface, notes and text and to "
                      "the 1991, 2005 and 2010 editions. The scan's OCR layer is garbled, so the "
                      "wording is NOT quoted here; read it off the page image before quoting.")},
        ],
        "attribution": ("Requested, not required: \"it is requested that the present editors' names "
                        "and the title associated with this text as well as this disclaimer be "
                        "retained in any subsequent reproduction\" (RP2005 copyright page). "
                        "Honoured: Robinson-Pierpont, The New Testament in the Original Greek: "
                        "Byzantine Textform (2018)."),
        "source_url": "https://github.com/byztxt/byzantine-majority-text/tree/" + BYZ_COMMIT,
        "redistribute_whole": True,
        "verified": True,
        "verified_on": "2026-09-26",
        "open": ("The Unicode CSVs are the maintainers' conversion of Robinson's Beta code; this "
                 "build re-checks every word's letters and codes against the Beta files. "
                 "Accents and breathings are the converter's and are not re-checked."),
    },
    "strongs-1890": {
        "what": ("lemma: the Strong's headword for Robinson's Strong's number; gloss: a "
                 "dictionary gloss from the same entry by a fixed rule (README s.12)"),
        "edition": ("James Strong, Dictionary of the Greek Testament (1890), XML by Ulrik "
                    "Petersen (2006), openscriptures/strongs commit " + STRONGS_COMMIT[:7]),
        "license": "PD",
        "license_basis": [
            {"where": "strongsgreek.xml, <prologue>",
             "says": "Public Domain -- Copy Freely"},
        ],
        "source_url": STRONGS_RAW + STRONGS_XML,
        "redistribute_whole": True,
        "verified": True,
        "verified_on": "2026-09-26",
        "open": ("Byte-identical to this repo's `strongs-greek` book input (data/books/manifest.json, "
                 "same sha256). Strong's numbers are Robinson's, which often differ from Strong's "
                 "own (all forms of eimi -> 1510, eipon -> 3004); the headword follows Robinson's."),
    },
}
ALLOWED_LICENSES = ("PD", "own")

# Declared in the manifest only once an override row is applied (none yet).
OVERRIDE_SOURCES = {
    layer: {
        "what": f"token gloss and/or plain_form: the {layer} layer over the dictionary gloss",
        "edition": "data/nt/gloss-overrides.jsonl (pipeline/README-nt-jsonl.md s.12)",
        "license": "own",
        "license_basis": [{"where": "data/nt/gloss-overrides.jsonl",
                           "says": "house work (Adam's review or the house draft), licence own"}],
        "source_url": "data/nt/gloss-overrides.jsonl",
        "verified": True,
        "verified_on": BUILT_ON,
    } for layer in G.OVERRIDE_LAYERS}

# The plain line's prose_order: house work, one row per verse. `house-draft`
# is the only source today, and every row of it is a draft.
PROSE_SOURCES = {
    "house-draft": {
        "what": ("en.plain: the prose_order (English word order over the grc.byz token "
                 "positions, with supplied words and absorptions), README-nt-jsonl.md s.14"),
        "edition": "data/nt/prose-order.jsonl, drafted by the house (AK/Claude)",
        "license": "own",
        "license_basis": [{"where": "data/nt/prose-order.jsonl",
                           "says": "house work, licence own: a draft awaiting Adam's review"}],
        "source_url": "data/nt/prose-order.jsonl",
        "status": "draft",
        "verified": True,
        "verified_on": BUILT_ON,
        "open": "draft: awaiting Adam's review (" + REVIEW_DOC + ")",
    },
}
# Adam's reviewed rows, in either file (pipeline/review.py applies his answers
# to the review doc): one source, one declaration, whichever file uses it.
ADAM_REVIEWED = {
    "what": ("Adam's reviewed answers: token glosses / plain_forms over the dictionary gloss "
             "(gloss-overrides.jsonl, layer adam-reviewed) and the plain line's prose_order "
             "(prose-order.jsonl, source adam-reviewed)"),
    "edition": ("data/nt/gloss-overrides.jsonl and data/nt/prose-order.jsonl, the rows Adam "
                "reviewed (README-nt-jsonl.md s.12, s.14, s.15)"),
    "license": "own",
    "license_basis": [{"where": "docs/review/", "says": "Adam's own review of the house drafts, licence own"}],
    "source_url": "data/nt/",
    "verified": True,
    "verified_on": BUILT_ON,
}
OVERRIDE_SOURCES["adam-reviewed"] = ADAM_REVIEWED
PROSE_SOURCES["adam-reviewed"] = ADAM_REVIEWED
PROSE_KEYS = {"passage_uid", "citation", "prose_order", "absorbed", "plain_override",
              "source", "draft", "drafted_on", "reviewed_on", "note"}

# A capital belongs to sentence position, not to a word: the plain renderer
# lower-cases a gloss unless it holds one of these. The hymns' list plus the
# Prologue's names and titles; the hymns' own list is not changed.
PROPER_NT = ("John", "Moses", "Father")

# What the reader's KJV column shows beside the Greek. Not an input to these
# files (the alignment only names its address); recorded here so its rights
# travel with the facing witness. Rights review 2026-09-26
# (wordhoard/docs/research/2026-09-26-rights-review.md), row 6 and s.6.
FACING_WITNESS = {
    "name": FACING,
    "what": "the King James Version (1769 text), the verse under the same uid",
    "file": ("data/books/kjv.witnesses.json (gitignored; rebuilt by structure_texts.py then "
             "build_witnesses.py from data/corpus/kjv_bible.txt, Project Gutenberg)"),
    "license": "PD",
    "license_basis": [
        {"where": "wordhoard/docs/research/2026-09-26-rights-review.md, Bible editions table",
         "says": "KJV (1769): Public domain outside the UK (UK: see s.6)"},
        {"where": "wordhoard/docs/research/2026-09-26-rights-review.md s.6",
         "says": ("In the UK the Authorised Version is under the royal prerogative (letters "
                  "patent), preserved by CDPA 1988 s.171(1)(b); Cambridge University Press, the "
                  "Crown's patentee, permits up to 500 verses for liturgical and non-commercial "
                  "educational use, with its acknowledgement.")},
    ],
    "rights_note": "Crown patent: KJV print not for UK",
    "scope": ("No effect on the US site, the web rooms or household printing. A sold print "
              "product, or any copy shipped into the UK, carrying this text needs Cambridge's "
              "permission or licence (rights review s.6; UK print is out of scope for now)."),
    "translates": ("the Textus Receptus, not the Byzantine textform: the column is a second "
                   "witness to the verse, not a translation of the Greek beside it"),
}

# Enrichment that may NOT be merged into these files. Recorded so nobody has
# to re-derive why it is absent.
FUTURE_LAYERS = {
    "morphgnt-sblgnt": {
        "what": "SBLGNT morphology and lemmas (MorphGNT)",
        "license": "CC BY-SA 3.0 (morphgnt/sblgnt README, read 2026-09-26)",
        "why_not_here": ("ShareAlike: never mixed into a PD file (ADR 0001; ADR 0019 s.4). "
                         "A separate layer keyed by address, joined at read time, if ever."),
    },
    "sblgnt": {
        "what": "SBL Greek New Testament text (a second Greek witness, grc.crit)",
        "license": "CC BY 4.0 (sblgnt.com/license, read 2026-09-26 by the rights review)",
        "why_not_here": ("Under ADR 0001 CC BY is collected, never served whole; serving it waits "
                         "on ADR 0019 (proposed). If admitted it is a second WITNESS on these same "
                         "uids, in its own file with its own rights block, never merged into grc.byz."),
    },
    "perseus": {
        "what": "Perseus lemmata, morphology, treebanks",
        "license": "CC BY-SA 4.0 by default; check each file's header",
        "why_not_here": "ADR 0001: cited by CTS URN, kept as a separate layer.",
        "cts_urn": None,
        "note": ("Perseus's canonical-greekLit holds no edition of the NT that this build uses; "
                 "the URN is null, not guessed."),
    },
}

TOKEN_FIELDS = {
    "surface": "the CCAT csv verse, split on whitespace, edge punctuation off (the elision mark stays)",
    "normalized": "derived: NFC(surface)",
    "search_key": "derived: fold(normalized) -- see search_key()",
    "translit": "derived: translit(normalized) -- the house scheme, README-nt-jsonl.md s.5",
    "lemma": "strongs-1890: the headword for lemma_key; null where Strong's has none",
    "lemma_key": "rp2018-byztxt: Robinson's Strong's number, as G<n>",
    "parsing": "rp2018-byztxt: Robinson's code, verbatim; the first where he gives two (see provenance)",
    "gloss": ("strongs-1890: a DICTIONARY gloss for lemma_key by the rule in provenance.gloss.rule "
              "(README s.12), not a contextual translation; null where no rule fires. An override "
              "row (gloss-overrides.jsonl) replaces it, keeping it under provenance.gloss.was"),
    "plain_form": ("null unless an override row sets it: the gloss's form in the plain line "
                   "(a dictionary gloss has no prose form)"),
}

# ---------------------------------------------------------------------------
# Mechanical token fields (shared with the test)
# ---------------------------------------------------------------------------

# Edge punctuation in the RP csv: comma, full stop, ano teleia (U+00B7 as the
# converter writes it, and U+0387), Greek question mark (U+037E) and ASCII
# semicolon, the dash RP uses to set off a parenthesis, and the pilcrow RP
# sets before the first word of a paragraph (892 times in the NT, none in
# John 1:1-18). NOT the elision mark U+2019, which is part of the word.
PARA = chr(0x00B6)
PUNCT = (",.;:!?\"()[]-" + "".join(map(chr, (0x00B7, 0x0387, 0x037E, 0x2013, 0x2014)))
         + PARA)
ELISION = chr(0x2019) + chr(0x02BC) + "'"


def tokenize(text):
    return [w.strip(PUNCT) for w in text.split() if w.strip(PUNCT)]


def paragraph_starts(text):
    """Token positions RP marks as opening a paragraph. Editorial structure:
    kept on the witness as positions, never in a surface."""
    words = [w for w in text.split() if w.strip(PUNCT)]
    return [i for i, w in enumerate(words, 1) if PARA in w]


def normalized(surface):
    return unicodedata.normalize("NFC", surface)


def search_key(s):
    """What searches run against, and what pairs the two RP files: decompose,
    drop every combining mark (accents, breathings, iota subscript,
    diaeresis), drop the elision mark, lowercase, and write every sigma as σ.
    So `λόγος`, `ΛΟΓΟΣ` and `λογος` are one key."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch) and ch not in ELISION)
    return s.lower().replace("ς", "σ").replace("ϲ", "σ")


# The house transliteration: SBL academic style (SBL Handbook of Style, 2nd
# ed., s.5.3), plus two house choices where SBL "makes no provision": iota
# subscript is written as a following i (ōi), and a diaeresis is kept (ï, ÿ).
# Accents are dropped (SBL again). README-nt-jsonl.md s.5 has the table.
_PSILI, _DASIA, _YPOG, _DIAER = "̓", "̔", "ͅ", "̈"
_BASE = {"α": "a", "β": "b", "γ": "g", "δ": "d", "ε": "e", "ζ": "z", "η": "ē", "θ": "th",
         "ι": "i", "κ": "k", "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o", "π": "p",
         "ρ": "r", "σ": "s", "ς": "s", "ϲ": "s", "τ": "t", "υ": "y", "φ": "ph", "χ": "ch",
         "ψ": "ps", "ω": "ō"}
_SUBSCRIPT = {"α": "ai", "η": "ēi", "ω": "ōi"}
_VOWELS = set("αεηιουω")
_NASAL_BEFORE = set("γκξχ")


def translit(word):
    cs = []
    for ch in unicodedata.normalize("NFD", word):
        if unicodedata.combining(ch) and cs:
            cs[-1][1].add(ch)
        else:
            cs.append([ch, set()])
    if not cs:
        return word
    upper = cs[0][0].isupper()
    low = [(b.lower(), m) for b, m in cs]
    rough, out = False, []
    for i, (b, m) in enumerate(low):
        prev = low[i - 1] if i else ("", set())
        nxt = low[i + 1] if i + 1 < len(low) else ("", set())
        if _DASIA in m and b in _VOWELS and i <= 1:        # on an initial vowel or diphthong
            rough = True
        if b == "γ" and nxt[0] in _NASAL_BEFORE:           # SBL note 1: gamma nasal
            out.append("n")
        elif b == "υ" and _DIAER not in m and (             # SBL note 4: au eu ēu ou ui
                (prev[0] in "αεηο" and prev[0] and _DIAER not in prev[1])
                or (nxt[0] == "ι" and _DIAER not in nxt[1])):
            out.append("u")
        elif b == "ρ" and (i == 0 or _DASIA in m or prev[0] == "ρ"):   # SBL note 3
            out.append("rh")
        elif b in _BASE:
            s = _SUBSCRIPT[b] if (_YPOG in m and b in _SUBSCRIPT) else _BASE[b]
            if _DIAER in m and b in "ιυ":
                s = {"ι": "ï", "υ": "ÿ"}[b]
            out.append(s)
        else:
            out.append(b)                                   # elision mark, anything else
    t = unicodedata.normalize("NFC", ("h" if rough else "") + "".join(out))
    return t[:1].upper() + t[1:] if upper else t


# Robinson's parsing grammar (robinson-documentation PARSING.COD and
# DECLINE.COD, 7 June 2009). The validator runs every code through it; a
# renderer can call describe_parsing() for the long form. Nothing is stored.
_INDECL = r"(?:ADV|CONJ|COND|PRT|PREP|INJ|ARAM|HEB|N-PRI|A-NUI|N-LI|N-OI)"
_SUFFIX = r"(?:-(?:S|C|ABB|I|N|K|ATT))*"
_CASE, _NUM, _GEN = "NVGDA", "SP", "MFN"
PARSING_RE = re.compile(
    rf"^(?:{_INDECL}{_SUFFIX}"
    rf"|[NARCDTKIXQ]-[{_CASE}][{_NUM}][{_GEN}]{_SUFFIX}"
    rf"|F-[123][{_CASE}][{_NUM}][{_GEN}]{_SUFFIX}"
    rf"|S-[123][{_NUM}][{_CASE}][{_NUM}][{_GEN}]{_SUFFIX}"
    rf"|P-[123]?[{_CASE}][{_NUM}][{_GEN}]?{_SUFFIX}"
    rf"|V-2?[PIFARL][AMPEDON][ISOMNP](?:-[123][{_NUM}]|-[{_CASE}][{_NUM}][{_GEN}])?(?:-ATT)?)$")

_WORDS = {
    "pos": {"N": "noun", "A": "adj", "R": "rel pron", "C": "recip pron", "D": "dem pron",
            "T": "article", "K": "correl pron", "I": "interrog pron", "X": "indef pron",
            "Q": "correl/interrog pron", "F": "refl pron", "S": "poss adj", "P": "pers pron",
            "V": "verb"},
    "case": {"N": "nom", "V": "voc", "G": "gen", "D": "dat", "A": "acc"},
    "num": {"S": "sg", "P": "pl"}, "gen": {"M": "masc", "F": "fem", "N": "neut"},
    "tense": {"P": "pres", "I": "impf", "F": "fut", "A": "aor", "R": "perf", "L": "plupf"},
    "voice": {"A": "act", "M": "mid", "P": "pass", "E": "mid/pass", "D": "mid dep",
              "O": "pass dep", "N": "mid/pass dep"},
    "mood": {"I": "ind", "S": "subj", "O": "opt", "M": "impv", "N": "inf", "P": "ptc"},
    "suffix": {"S": "superl", "C": "compar", "ABB": "abbrev", "I": "interrog", "N": "neg",
               "K": "crasis with kai", "ATT": "Attic"},
    "indecl": {"ADV": "adverb", "CONJ": "conjunction", "COND": "conditional", "PRT": "particle",
               "PREP": "preposition", "INJ": "interjection", "ARAM": "Aramaic word",
               "HEB": "Hebrew word", "N-PRI": "indecl proper noun", "A-NUI": "indecl numeral",
               "N-LI": "indecl letter", "N-OI": "indecl noun"},
}


def describe_parsing(code):
    """Robinson's code in words, e.g. V-2ADI-3S -> '3 sg 2nd aor mid dep ind'."""
    if not PARSING_RE.match(code):
        raise ValueError(f"not a Robinson code: {code!r}")
    W = _WORDS
    for k, v in sorted(W["indecl"].items(), key=lambda kv: -len(kv[0])):
        if code == k or code.startswith(k + "-"):
            rest = [W["suffix"][s] for s in code[len(k):].split("-") if s]
            return " ".join([v] + rest)
    head, *parts = code.split("-")
    if head == "V":
        tvm = parts[0]
        second = tvm.startswith("2")
        t, v, m = tvm[-3], tvm[-2], tvm[-1]
        words = []
        if len(parts) > 1 and parts[1] != "ATT":
            p = parts[1]
            if p[0] in "123":
                words += [p[0], W["num"][p[1]]]
            else:
                words += [W["case"][p[0]], W["num"][p[1]], W["gen"][p[2]]]
        words += [("2nd " if second else "") + W["tense"][t], W["voice"][v], W["mood"][m]]
        if parts[-1] == "ATT":
            words.append("Attic")
        return " ".join(words)
    body, suffixes = parts[0], parts[1:]
    words = [W["pos"][head]]
    if body[0] in "123":
        words.append(body[0])
        body = body[1:]
        if head == "S":
            words.append("poss " + W["num"][body[0]])
            body = body[1:]
    words.append(W["case"][body[0]])
    words.append(W["num"][body[1]])
    if len(body) > 2:
        words.append(W["gen"][body[2]])
    words += [W["suffix"][s] for s in suffixes]
    return " ".join(words)


def render_plain(tokens, plain):
    """A verse's plain line: the hymns' render_plain() over its tokens and its
    en.plain witness, the Prologue's names kept capitalised. Never stored."""
    import build_hymn_corpus as H   # lazily: the build itself never renders
    return H.render_plain(tokens, plain, proper=H.PROPER + PROPER_NT)


def _is_pos(x):
    return isinstance(x, int) and not isinstance(x, bool)


def permutation_problems(n_tokens, prose_order, absorbed):
    """The hymns' rule: every token used exactly once, by the order or by
    absorption. None when it holds."""
    accounted = sorted([x for x in prose_order if _is_pos(x)] + list(absorbed))
    if accounted == list(range(1, n_tokens + 1)):
        return None
    return {"missing": [n for n in range(1, n_tokens + 1) if n not in accounted],
            "duplicated": sorted({n for n in accounted if accounted.count(n) > 1}),
            "out_of_range": [n for n in accounted if not 1 <= n <= n_tokens]}


def load_prose_orders(path=None):
    """{passage uid: row}, from `path` or PROSE_ORDERS. A missing file is no
    orders. A malformed row is a hard stop, as for the gloss overrides."""
    path = path or PROSE_ORDERS
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            where = f"{os.path.basename(path)}:{n}"
            extra = set(row) - PROSE_KEYS
            if extra:
                raise ValueError(f"{where}: unknown fields {sorted(extra)}")
            for k in ("passage_uid", "citation", "source"):
                if not isinstance(row.get(k), str) or not row[k]:
                    raise ValueError(f"{where}: `{k}` is required")
            if row["source"] not in PROSE_SOURCES:
                raise ValueError(f"{where}: source must be one of {sorted(PROSE_SOURCES)}")
            if "draft" in row and row["draft"] is not True:
                raise ValueError(f"{where}: `draft` is true or absent")
            if PROSE_SOURCES[row["source"]].get("status") == "draft" and not row.get("draft"):
                raise ValueError(f"{where}: a {row['source']} row is a draft: `draft: true`")
            if row.get("draft") and PROSE_SOURCES[row["source"]].get("status") != "draft":
                raise ValueError(f"{where}: a {row['source']} row is reviewed, never a draft")
            dated, undated = (("drafted_on", "reviewed_on") if row.get("draft")
                              else ("reviewed_on", "drafted_on"))
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row.get(dated) or "") or undated in row:
                raise ValueError(f"{where}: carries `{dated}` (YYYY-MM-DD), not `{undated}`")
            order, absorbed = row.get("prose_order"), row.get("absorbed")
            if not isinstance(order, list) or not order or not isinstance(absorbed, list):
                raise ValueError(f"{where}: prose_order (not empty) and absorbed are lists")
            if any(not _is_pos(x) and not (isinstance(x, str) and x and x.strip() == x)
                   for x in order) or not all(_is_pos(x) for x in absorbed):
                raise ValueError(f"{where}: prose_order holds positions and supplied words only")
            if row.get("plain_override") is not None:
                raise ValueError(f"{where}: plain_override is null (no verse needs one yet)")
            if row["passage_uid"] in out:
                raise ValueError(f"{where}: {row['passage_uid']} is ordered twice")
            out[row["passage_uid"]] = row
    return out


FINITE_MOODS = set("ISOM")


def is_finite(code):
    """A finite verb (indicative, subjunctive, optative, imperative): the
    anchor of the proposed Greek clause rule (README s.8)."""
    m = re.match(r"^V-2?[PIFARL][AMPEDON]([ISOMNP])", code or "")
    return bool(m) and m.group(1) in FINITE_MOODS


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _path(repo, rel):
    return os.path.join(CACHE[repo], *rel.split("/"))


def _url(repo, rel):
    return (BYZ_RAW if repo == "byz" else STRONGS_RAW) + rel


def fetch(extra=(), quiet=False):
    """Download every pinned file not already cached with the right sha256.
    `extra` names further byztxt files (the --survey books), which are
    fetched at the same commit but are NOT pinned: the survey reads them and
    writes nothing."""
    for (repo, rel), want in list(PINS.items()) + [(("byz", r), None) for r in extra]:
        p = _path(repo, rel)
        if os.path.exists(p) and (want is None or sha256(p) == want):
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not quiet:
            print(f"  fetch {rel}")
        with urllib.request.urlopen(_url(repo, rel), timeout=120) as r:
            blob = r.read()
        got = hashlib.sha256(blob).hexdigest()
        if want and got != want:
            raise SystemExit(f"HARD STOP: {rel} sha256 {got} != pinned {want}")
        tmp = p + ".tmp"
        with open(tmp, "wb") as f:
            f.write(blob)
        os.replace(tmp, p)


def verify_pins():
    bad = [rel for (repo, rel), want in PINS.items()
           if not os.path.exists(_path(repo, rel)) or sha256(_path(repo, rel)) != want]
    if bad:
        raise SystemExit(f"pinned inputs missing or changed: {bad}\n"
                         f"  run: python3 pipeline/build_nt_corpus.py --fetch")


def _stop(msg):
    raise SystemExit("HARD STOP: " + msg)


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return {(int(r["chapter"]), int(r["verse"])): r["text"] for r in csv.DictReader(f)}


_CODE = re.compile(r"^\{([A-Z0-9-]+)\}$")


def parse_parsed(text):
    """A BP5 line (csv or Beta) -> [(word, [(strongs, code), ...])].
    Robinson writes `word 3056 {N-NSM}`; where he gives two readings of one
    form he repeats the pair (`2064 {V-PNP-ASM} 2064 {V-PNP-NSN}`)."""
    out = []
    for tok in text.split():
        if tok.isdigit():
            if not out:
                _stop(f"a number before any word: {text[:60]!r}")
            out[-1][1].append([int(tok), None])
        elif _CODE.match(tok):
            if not out or not out[-1][1] or out[-1][1][-1][1] is not None:
                _stop(f"a code with no number before it: {text[:60]!r}")
            out[-1][1][-1][1] = _CODE.match(tok).group(1)
        else:
            out.append((tok, []))
    for w, pairs in out:
        if not pairs or any(c is None for _, c in pairs):
            _stop(f"word without a (number, code) pair: {w!r}")
    return [(w, [tuple(p) for p in pairs]) for w, pairs in out]


# Robinson's Beta code, letters only (the cross-check ignores diacritics).
_BETA = dict(zip("ABGDEZHQIKLMNCOPRSTUFXYW", "αβγδεζηθικλμνξοπρστυφχψω"))


def beta_letters(tok):
    return "".join(_BETA[c] for c in tok.upper() if c in _BETA)


def read_beta(path, sep):
    """Robinson's source file -> {(ch, vs): line body}. CCAT lines are
    `01:09 ...` (sep ':'), BP5 lines `01.09 ...` (sep '.')."""
    out = {}
    with open(path, encoding="latin-1") as f:
        for line in f:
            m = re.match(rf"^(\d+){re.escape(sep)}(\d+)\s+(.*)$", line.rstrip("\r\n"))
            if m:
                out[(int(m.group(1)), int(m.group(2)))] = m.group(3)
    return out


_APPARATUS = re.compile(r"\{([A-Z])\s[^}]*\}")


def load_strongs():
    x = open(_path("strongs", STRONGS_XML), encoding="utf-8").read()
    heads = {}
    for n, uni in re.findall(r'<entry strongs="(\d+)">\s*<strongs>\d+</strongs>\s*'
                             r'<greek BETA="[^"]*" unicode="([^"]*)"', x):
        heads[int(n)] = uni
    return heads


# ---------------------------------------------------------------------------
# The verse: pair the two RP files, check both against Robinson's Beta
# ---------------------------------------------------------------------------

def pair_verse(ref, accented, parsed, beta_ccat, beta_bp5):
    """Returns (surfaces, [(word, pairs)]) or raises. Every check here is a
    hard stop in the build and a counted problem in --survey."""
    surfaces = tokenize(accented)
    words = parse_parsed(parsed)
    if len(surfaces) != len(words):
        raise ValueError(f"{ref}: {len(surfaces)} accented words, {len(words)} parsed")
    for i, (s, (w, _)) in enumerate(zip(surfaces, words), 1):
        if search_key(s) != search_key(w):
            raise ValueError(f"{ref} word {i}: accented and parsed files spell it differently")
    if beta_bp5 is not None:
        bw = parse_parsed(beta_bp5)
        if [(search_key(beta_letters(w)), p) for w, p in bw] != \
                [(search_key(w), p) for w, p in words]:
            raise ValueError(f"{ref}: parsed csv disagrees with Robinson's BP5 Beta file")
    if beta_ccat is not None:
        main = _APPARATUS.sub(" ", beta_ccat)
        bl = [beta_letters(t) for t in main.split()]
        if [search_key(b) for b in bl if b] != [search_key(s) for s in surfaces]:
            raise ValueError(f"{ref}: accented csv disagrees with Robinson's CCAT Beta file")
    return surfaces, words


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def _book_inputs(stem):
    num, _ = BOOK[stem]
    return (read_csv(_path("byz", f"csv-unicode/ccat/no-variants/{stem}.csv")),
            read_csv(_path("byz", f"csv-unicode/strongs/with-parsing/{stem}.csv")),
            read_beta(_path("byz", f"source/CCAT/{num}_{stem}.TXT"), ":"),
            read_beta(_path("byz", f"source/Strongs/{num}_{stem}.BP5"), "."))


def in_pilot(osis, ch, vs):
    return osis == PILOT["osis_book"] and ch == PILOT["chapter"] and PILOT["first"] <= vs <= PILOT["last"]


def summarize(passages, witnesses, tokens, alignments):
    """(counts, gloss counts) for any set of records: the whole NT for the
    manifest, or one pericope for load_nt()'s view of it. Read off the
    records themselves, so the two can never disagree."""
    plains = [w for w in witnesses if w["name"] == PLAIN]
    counts = {"passages": len(passages), "verses": len(passages),
              "witnesses": len(witnesses), "plain_witnesses": len(plains),
              "tokens": len(tokens),
              "alignments": len(alignments),
              "tokens_with_lemma": sum(1 for t in tokens if t["lemma"]),
              "tokens_with_parsing": sum(1 for t in tokens if t["parsing"]),
              "tokens_with_gloss": sum(1 for t in tokens if t["gloss"]),
              "tokens_without_gloss": sum(1 for t in tokens if not t["gloss"]),
              "tokens_flagged_for_review": sum(1 for t in tokens if t["review"]),
              "distinct_lemmas": len({t["lemma_key"] for t in tokens}),
              "finite_verbs": sum(1 for t in tokens if is_finite(t["parsing"]))}
    why_none = {}
    for t in tokens:
        if t["gloss"] is None:
            w = t["provenance"]["gloss"]["why"]
            why_none[w] = why_none.get(w, 0) + 1
    gloss = {
        "by_rule": {r: sum(1 for t in tokens if t["provenance"]["gloss"]["rule"] == r)
                    for r in G.RULE_ORDER},
        "by_override": {k: sum(1 for t in tokens if t["provenance"]["gloss"]["source"] == k)
                        for k in G.OVERRIDE_LAYERS},
        "none": sum(why_none.values()),
        "none_by_reason": dict(sorted(why_none.items())),
        "applied": sum(1 for t in tokens if t["provenance"]["gloss"]["kind"] == "contextual"),
        "draft": sum(1 for t in tokens if t["provenance"]["gloss"].get("draft")),
    }
    return counts, gloss


def build(reg):
    verify_pins()
    heads = load_strongs()
    entries = G.load_entries(open(_path("strongs", STRONGS_XML), encoding="utf-8").read())
    try:
        overrides = G.load_overrides()
    except ValueError as e:
        _stop(f"gloss overrides: {e}")
    try:
        orders = load_prose_orders()
    except ValueError as e:
        _stop(f"prose orders: {e}")
    used_ov, used_po = set(), set()

    passages, witnesses, tokens, alignments = [], [], [], []
    apparatus = {}
    shards = {}
    placed, left_out = [], []
    gloss_memo = {}
    for stem in SCOPE:
        _, osis = BOOK[stem]
        ccat, bp5, b_ccat, b_bp5 = _book_inputs(stem)
        shard = {"verses": 0, "tokens": 0}
        for ch, vs in sorted(set(ccat) | set(bp5)):
            rp_ref = f"{osis}.{ch}.{vs}"
            if (ch, vs) not in ccat or (ch, vs) not in bp5:
                _stop(f"{rp_ref} is in one RP csv only")
            ref = VERSIFICATION_MAP.get(rp_ref, rp_ref)
            if ref is None:              # ruled out: counted, never minted
                left_out.append(rp_ref)
                continue
            kch, kvs = (int(x) for x in ref.rsplit(".", 2)[1:])
            citation = f"kjv:{ref}"
            try:
                uid = reg.uid_for(citation)
            except U.WhUidError:
                _stop(f"{citation} has no uid: a versification question, not new content. "
                      f"Nothing is minted for a Greek verse (see VERSIFICATION_MAP).")
            try:
                surfaces, words = pair_verse(rp_ref, ccat[(ch, vs)], bp5[(ch, vs)],
                                             b_ccat.get((ch, vs)), b_bp5.get((ch, vs)))
            except ValueError as e:
                _stop(str(e))
            for m in _APPARATUS.finditer(b_ccat.get((ch, vs), "")):
                apparatus[m.group(1)] = apparatus.get(m.group(1), 0) + 1

            passages.append({
                "uid": uid, "citation": citation, "kind": "passage", "unit": "verse",
                "book": osis, "osis": ref, "chapter": kch, "verse": kvs,
                "versification": "kjv",
                "pericope": PILOT["pericope"] if in_pilot(osis, kch, kvs) else None,
                "reading_of_record": FACING,
                "status": "machine-built from public-domain sources, unchecked",
            })
            text = ccat[(ch, vs)]
            gw = {
                "address": U.address(uid, WITNESS), "passage_uid": uid, "name": WITNESS,
                "lang": "grc", "role": "original", "register": "koine",
                "textform": "byzantine", "text": text, "paragraph_starts": paragraph_starts(text),
                "generated": False,
                "source": "rp2018-byztxt", "attested": "Y", "reading_of_record": False,
            }
            if ref != rp_ref:
                gw["rp_ref"] = rp_ref
                placed.append({"rp": rp_ref, "kjv": ref, "uid": uid})
            witnesses.append(gw)
            first_tok = len(tokens)
            for pos, (surface, (_, pairs)) in enumerate(zip(surfaces, words), 1):
                strongs, code = pairs[0]
                head = heads.get(strongs)
                review = []
                prov_parse = {"source": "rp2018-byztxt", "scheme": "robinson-2009",
                              "status": "single"}
                if len(pairs) > 1:
                    prov_parse["status"] = "alternatives"
                    prov_parse["alternatives"] = [c for _, c in pairs[1:]]
                    review.append("Robinson gives more than one parsing; the first is shown, "
                                  "none is chosen")
                if len({s for s, _ in pairs}) > 1:
                    review.append("Robinson gives more than one Strong's number")
                if head is None:
                    review.append(f"Strong's has no entry G{strongs}")
                norm = normalized(surface)
                address = U.address(uid, f"{WITNESS}.t{pos:02d}")
                if (code, strongs) not in gloss_memo:     # a pure function: same inputs, same gloss
                    gloss_memo[(code, strongs)] = G.gloss_for(code, entries.get(strongs))
                gloss, prov_gloss = gloss_memo[(code, strongs)]
                prov_gloss = dict(prov_gloss)
                plain_form = None
                if address in overrides:
                    try:
                        gloss, plain_form, prov_gloss = G.apply_override(
                            gloss, plain_form, prov_gloss, surface, overrides[address])
                    except ValueError as e:
                        _stop(f"gloss overrides: {e}")
                    used_ov.add(address)
                tokens.append({
                    "address": address,
                    "passage_uid": uid, "witness": WITNESS, "position": pos,
                    "surface": surface, "normalized": norm, "search_key": search_key(norm),
                    "translit": translit(norm),
                    "lemma": head, "lemma_key": f"G{strongs}", "parsing": code,
                    "gloss": gloss, "plain_form": plain_form, "syntax": None,
                    "provenance": {
                        "lemma": {"source": "strongs-1890", "by": "rp2018-byztxt Strong's number",
                                  "status": "headword" if head else "none"},
                        "parsing": prov_parse,
                        "gloss": prov_gloss,
                    },
                    "review": review or None,
                })
            po = orders.get(uid)
            if po:
                if po["citation"] != citation:
                    _stop(f"prose orders: {uid} is {citation}, the row says {po['citation']}")
                vtoks = tokens[first_tok:]
                prob = permutation_problems(len(vtoks), po["prose_order"], po["absorbed"])
                if prob:
                    _stop(f"prose orders: {citation} is not a permutation of its tokens: {prob}")
                gaps = [t["position"] for t in vtoks
                        if t["position"] in po["prose_order"] and not (t["plain_form"] or t["gloss"])]
                if gaps:
                    _stop(f"prose orders: {citation} walks tokens with no gloss: {gaps}")
                w = {"address": U.address(uid, PLAIN), "passage_uid": uid, "name": PLAIN,
                     "lang": "en", "role": "plain", "text": None, "generated": True,
                     "generated_from": f"{WITNESS} tokens walked in prose_order",
                     "prose_order": po["prose_order"], "absorbed": po["absorbed"],
                     "plain_override": None, "source": po["source"], "attested": "N",
                     "reading_of_record": False}
                if po.get("draft"):
                    w.update(draft=True, drafted_on=po["drafted_on"])
                else:
                    w["reviewed_on"] = po["reviewed_on"]
                if po.get("note"):
                    w["note"] = po["note"]
                witnesses.append(w)
                used_po.add(uid)
            alignments.append({
                "alignment_id": f"{U.address(uid, WITNESS)}~{FACING}",
                "level": "section", "type": "1:1",
                "a": [{"address": U.address(uid, WITNESS), "tokens": None}],
                "b": [{"address": U.address(uid, FACING), "tokens": None}],
                "confidence": "high",
                "note": ("verse to verse under one uid; the KJV translates the Textus Receptus, "
                         "so this aligns verses, not readings"),
            })
            shard["verses"] += 1
            shard["tokens"] += len(tokens) - first_tok
        shards[osis] = dict(shard, dir=osis if SHARD == "book" else "")

    # A row for a book outside a narrowed SCOPE is not stale, only not built
    # this time. Anything else unused is: a token or verse that does not exist.
    books = {BOOK[s][1] for s in SCOPE}
    cit_of = {u: c for c, u in reg.map.items()}

    def elsewhere(uid):
        c = cit_of.get(uid, "")
        return c.startswith("kjv:") and c[4:].rsplit(".", 2)[0] in BOOK_OSIS - books
    stale = sorted(a for a in set(overrides) - used_ov if not elsewhere(a.split("/", 1)[0]))
    if stale:
        _stop(f"gloss overrides name tokens that do not exist: {stale[:5]}")
    stale = sorted(u for u in set(orders) - used_po if not elsewhere(u))
    if stale:
        _stop(f"prose orders name verses outside the selection: {stale[:5]}")
    built = {p["citation"] for p in passages}
    no_grc = sorted(c for c in reg.map if c.startswith("kjv:")
                    and c[4:].rsplit(".", 2)[0] in books and c not in built)
    sources = dict(SOURCES)
    inputs = {rel: want for (repo, rel), want in sorted(PINS.items())
              if repo == "strongs" or not rel.startswith(("source/", "csv-unicode/"))
              or any(f"/{s}.csv" in rel or f"_{s}." in rel for s in SCOPE)}
    for layer in sorted({overrides[a]["layer"] for a in used_ov}):
        sources[layer] = dict(OVERRIDE_SOURCES[layer])
        if any(overrides[a].get("draft") for a in used_ov if overrides[a]["layer"] == layer):
            sources[layer]["open"] = ("rows marked draft: true are the house's proposals, awaiting "
                                      "Adam's review (" + REVIEW_DOC + ")")
    for src in sorted({orders[u]["source"] for u in used_po}):
        sources[src] = PROSE_SOURCES[src]
    if used_ov:
        inputs["gloss-overrides.jsonl"] = sha256(G.OVERRIDES)
    if used_po:
        inputs["prose-order.jsonl"] = sha256(PROSE_ORDERS)
    plains = [w for w in witnesses if w["name"] == PLAIN]
    counts, gc = summarize(passages, witnesses, tokens, alignments)
    manifest = {
        "schema": SCHEMA,
        "doc": "pipeline/README-nt-jsonl.md",
        "built_on": BUILT_ON,
        "row_unit": "verse",
        "selection": {"title": "The Greek New Testament (Robinson-Pierpont 2018)",
                      "books": [BOOK[s][1] for s in SCOPE], "pilot": PILOT},
        "counts": counts,
        "shards": {"layout": SHARD or "flat", "order": [BOOK[s][1] for s in SCOPE],
                   "books": shards, "ruling": SHARD_RULING},
        "versification": {
            "of_record": "kjv",
            "map": VERSIFICATION_MAP,
            "ruling": VERSIFICATION_RULING,
            "placed_elsewhere": placed,
            "left_out": left_out,
            "kjv_verses_without_grc": no_grc,
            "note": ("kjv_verses_without_grc are KJV verses the Byzantine text does not carry "
                     "(Textus Receptus readings), plus any the map leaves out. They keep their "
                     "uids and simply have no grc.byz witness; nothing is guessed."),
        },
        "identity": {
            "rule": ("a Greek verse is a witness of the verse passage that already exists; "
                     "registry opened frozen; nothing minted"),
            "citation_slug": "kjv names the versification of record, not the language",
            "reading_of_record": {"value": FACING,
                                  "declared_by": "pipeline/build_witnesses.py (READING_OF_RECORD)",
                                  "note": "unchanged here; swapping it to grc.byz is a ruling"},
        },
        "witness": {"name": WITNESS, "lang": "grc", "textform": "byzantine",
                    "facing": FACING},
        "licence_gate": {"allowed": list(ALLOWED_LICENSES),
                         "rule": "launch plan D4 / ADR 0001: public-domain editions or own work only"},
        "sources": sources,
        "gloss": {
            "kind": "dictionary",
            "not": ("NOT a contextual translation. Each gloss is Strong's 1890 dictionary sense "
                    "for the token's Strong's number, chosen by a fixed rule: the same number "
                    "and form class get the same gloss in every verse, whatever the verse means. "
                    "A wooden line built from them is a dictionary interlinear, not a "
                    "translation. Where an override row applies, the token's gloss is "
                    "contextual instead (provenance.gloss.kind), and a draft row says draft."),
            "source": "strongs-1890",
            "doc": "pipeline/README-nt-jsonl.md s.12; pipeline/strongs_gloss.py",
            "rules": [{"id": r, "does": G.RULES[r]} for r in G.RULE_ORDER],
            "by_rule": gc["by_rule"],
            "by_override": gc["by_override"],
            "none": gc["none"],
            "none_by_reason": gc["none_by_reason"],
            "overrides": {"file": "data/nt/gloss-overrides.jsonl",
                          "layers": list(G.OVERRIDE_LAYERS),
                          "applied": gc["applied"],
                          "draft": gc["draft"],
                          "rule": ("a row replaces the dictionary gloss of one token address; "
                                   "the dictionary value and its rule are kept under "
                                   "provenance.gloss.was. A draft row (draft: true, layer house) "
                                   "awaits Adam's review and says so in provenance.gloss.draft")},
        },
        "prose_order": {
            "file": "data/nt/prose-order.jsonl",
            "witness": PLAIN,
            "convention": ("the hymns' (README-hymn-jsonl.md s.5): an integer is a token position "
                           "(its plain_form, else its gloss); a string is a supplied word, shown "
                           "[bracketed]; an absorbed position is carried by a neighbour's form; "
                           "every token is used exactly once. Rendered by render_plain(), never "
                           "stored"),
            "verses": len(plains),
            "draft": sum(1 for w in plains if w.get("draft")),
            "sources": sorted({w["source"] for w in plains}),
        },
        "drafts": {
            "status": ("awaiting Adam's review" if gc["draft"] or any(w.get("draft") for w in plains)
                       else "none open: every row reviewed"),
            "review_doc": REVIEW_DOC,
            "gloss_override_rows": gc["draft"],
            "prose_orders": sum(1 for w in plains if w.get("draft")),
            "how_to_accept": ("drop draft/drafted_on and date the row reviewed_on (a gloss row "
                              "that is now Adam's becomes layer adam-reviewed); rebuild"),
        },
        "facing_witness": FACING_WITNESS,
        "future_layers": FUTURE_LAYERS,
        "token_fields": TOKEN_FIELDS,
        "translit": {"scheme": "sbl-academic+house",
                     "doc": "pipeline/README-nt-jsonl.md s.5",
                     "house_choices": {"iota_subscript": "following i (ōi)",
                                       "diaeresis": "kept (ï, ÿ)", "accents": "dropped"}},
        "parsing_scheme": {"name": "robinson-2009",
                           "doc": ("byztxt/byzantine-majority-text source/README.md; "
                                   "byztxt/robinson-documentation doc/PARSING.COD, DECLINE.COD")},
        "apparatus_in_selection": {
            "note": ("RP's CCAT file carries variant notes in {..} blocks; these files hold the "
                     "main text only. Counts by siglum (N = Nestle-Aland)."),
            "by_siglum": dict(sorted(apparatus.items()))},
        "inputs_sha256": inputs,
        "files_sha256": {},
    }
    return {"passages": passages, "witnesses": witnesses, "tokens": tokens,
            "alignments": alignments}, manifest


def serialize(records):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8")


def shard_path(book, name):
    """The output path of one file of one book, relative to data/nt/."""
    return f"{book}/{name}" if SHARD == "book" else name


def _book_of(data):
    """{passage uid: OSIS book}, which places every record in its shard."""
    return {p["uid"]: p["book"] for p in data["passages"]}


def _record_uid(kind, r):
    if kind == "passages":
        return r["uid"]
    if kind == "alignments":
        return U.parse_address(r["a"][0]["address"])["uid"]
    return r["passage_uid"]


def render_all(data, manifest):
    book_of = _book_of(data)
    order = manifest["shards"]["order"]
    blobs = {}
    if SHARD == "book":
        for k, recs in data.items():
            per = {b: [] for b in order}
            for r in recs:
                per[book_of[_record_uid(k, r)]].append(r)
            for b in order:
                blobs[shard_path(b, f"{k}.jsonl")] = serialize(per[b])
    else:
        blobs = {f"{k}.jsonl": serialize(v) for k, v in data.items()}
    manifest["files_sha256"] = {k: hashlib.sha256(v).hexdigest() for k, v in sorted(blobs.items())}
    blobs["manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return blobs


# Files in data/nt/ that are inputs, not build output: never stale, never removed.
INPUT_FILES = ("gloss-overrides.jsonl", "prose-order.jsonl")


def stale_outputs(out, blobs):
    """Build-output files under `out` that this build would not write (e.g. the
    pilot's flat files after sharding): --check fails on them, a write removes them."""
    found = []
    for d, _, fs in os.walk(out):
        for f in fs:
            if f.endswith(".jsonl") or f == "manifest.json":
                rel = os.path.relpath(os.path.join(d, f), out).replace(os.sep, "/")
                if rel not in blobs and rel not in INPUT_FILES:
                    found.append(rel)
    return sorted(found)


def load_nt(root=ROOT, pericope=None, books=None):
    """The committed NT as {passages, witnesses, tokens, alignments, manifest},
    whatever the shard layout: it reads the files the manifest lists, in its
    canonical order. `books` (OSIS) reads only those shards; `pericope` keeps
    only the verses carrying that label (the pilot: PILOT["pericope"]), and then
    the manifest returned is a VIEW whose counts, gloss counts and selection
    describe just those verses (the files' checksums stay the whole NT's)."""
    d = os.path.join(root, "data", "nt")
    with open(os.path.join(d, "manifest.json"), encoding="utf-8") as fh:
        man = json.load(fh)
    sh = man.get("shards") or {}
    flat = sh.get("layout", "flat") == "flat"
    order = [None] if flat else sh["order"]
    if books is None and pericope == PILOT["pericope"]:
        books = [PILOT["osis_book"]]
    out = {k: [] for k in FILES}
    for b in order:
        if b is not None and books is not None and b not in books:
            continue
        for k in FILES:
            rel = f"{k}.jsonl" if b is None else f"{sh['books'][b]['dir']}/{k}.jsonl"
            with open(os.path.join(d, rel), encoding="utf-8") as fh:
                out[k].extend(json.loads(line) for line in fh if line.strip())
    if pericope is not None:
        keep = {p["uid"] for p in out["passages"] if p.get("pericope") == pericope}
        out = {k: [r for r in out[k] if _record_uid(k, r) in keep] for k in FILES}
        counts, gc = summarize(out["passages"], out["witnesses"], out["tokens"], out["alignments"])
        man = dict(man, counts=counts,
                   selection=dict(PILOT) if pericope == PILOT["pericope"] else {"pericope": pericope},
                   gloss=dict(man["gloss"], by_rule=gc["by_rule"], by_override=gc["by_override"],
                              none=gc["none"], none_by_reason=gc["none_by_reason"],
                              overrides=dict(man["gloss"]["overrides"], applied=gc["applied"],
                                             draft=gc["draft"])))
    out["manifest"] = man
    return out


def write_atomic(path, blob):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(blob)
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# Survey: the whole NT, read and measured, never written
# ---------------------------------------------------------------------------

def survey(reg_path):
    extra = []
    for stem, num, _ in BOOKS:
        extra += [f"csv-unicode/ccat/no-variants/{stem}.csv",
                  f"csv-unicode/strongs/with-parsing/{stem}.csv",
                  f"source/CCAT/{num}_{stem}.TXT", f"source/Strongs/{num}_{stem}.BP5"]
    fetch(extra, quiet=True)
    reg = U.WhUidRegistry(reg_path, frozen=True)
    heads = load_strongs()
    kjv_nt = {c for c in reg.map if c.startswith("kjv:")
              and c[4:].rsplit(".", 2)[0] in {o for _, _, o in BOOKS}}
    stats = {"verses": 0, "tokens": 0, "no_kjv_uid": [], "pair_fail": [], "alternatives": 0,
             "no_strongs_head": 0, "bad_code": 0, "finite": 0}
    seen = set()
    for stem, num, osis in BOOKS:
        ccat = read_csv(_path("byz", f"csv-unicode/ccat/no-variants/{stem}.csv"))
        bp5 = read_csv(_path("byz", f"csv-unicode/strongs/with-parsing/{stem}.csv"))
        b_ccat = read_beta(_path("byz", f"source/CCAT/{num}_{stem}.TXT"), ":")
        b_bp5 = read_beta(_path("byz", f"source/Strongs/{num}_{stem}.BP5"), ".")
        for key in sorted(set(ccat) | set(bp5)):
            ref = f"{osis}.{key[0]}.{key[1]}"
            stats["verses"] += 1
            seen.add("kjv:" + ref)
            if "kjv:" + ref not in reg.map:
                stats["no_kjv_uid"].append(ref)
            if key not in ccat or key not in bp5:
                stats["pair_fail"].append((ref, "in one csv only"))
                continue
            try:
                _, words = pair_verse(ref, ccat[key], bp5[key], b_ccat.get(key), b_bp5.get(key))
            except (ValueError, SystemExit) as e:
                stats["pair_fail"].append((ref, str(e).split(": ", 1)[-1]))
                continue
            for _, pairs in words:
                stats["tokens"] += 1
                stats["alternatives"] += len(pairs) > 1
                stats["no_strongs_head"] += pairs[0][0] not in heads
                stats["bad_code"] += not PARSING_RE.match(pairs[0][1])
                stats["finite"] += is_finite(pairs[0][1])
    stats["kjv_verses_without_rp"] = sorted(kjv_nt - seen)
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="download the pinned inputs, then build")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--survey", action="store_true", help="measure the whole NT; writes nothing")
    ap.add_argument("--uids", default=UIDS)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()

    if a.fetch or a.survey:
        fetch()
    if a.survey:
        s = survey(a.uids)
        for k, v in s.items():
            print(f"  {k:<24}{v if isinstance(v, int) else len(v):>8,}")
        for k in ("no_kjv_uid", "kjv_verses_without_rp"):
            print(f"  {k}: {' '.join(s[k][:40])}")
        print("  first pair failures:", s["pair_fail"][:12])
        return

    if not a.report and sorted(SCOPE) != sorted(BOOK):
        raise SystemExit("HARD STOP: SCOPE is narrowed; writing or checking it would drop the other "
                         "books from data/nt/. Use --report, or restore SCOPE to every book.")
    # FROZEN: a Greek verse reuses its verse's uid or the build stops.
    reg = U.WhUidRegistry(a.uids, frozen=True)
    data, manifest = build(reg)
    blobs = render_all(data, manifest)
    for k, v in manifest["counts"].items():
        print(f"  {k:<28}{v:>6,}")
    s = reg.stats()
    print(f"  uids minted {s['minted']} / reused {s['reused']} / registry total {s['total']:,}")
    reg.assert_no_mint()

    if a.check:
        stale = [fn for fn, blob in blobs.items()
                 if not os.path.exists(os.path.join(a.out, fn))
                 or open(os.path.join(a.out, fn), "rb").read() != blob]
        if stale:
            raise SystemExit(f"CHECK FAILED: rebuilt output differs from committed: {stale[:8]}")
        extra = stale_outputs(a.out, blobs)
        if extra:
            raise SystemExit(f"CHECK FAILED: output files this build does not write: {extra[:8]}")
        print("  CHECK PASSED: minted 0, output byte-identical.")
        return
    if a.report:
        return
    os.makedirs(a.out, exist_ok=True)
    # Shards first, the manifest last: a killed run leaves the old manifest
    # pointing at files that are each whole (temp file + rename).
    for fn, blob in sorted(blobs.items(), key=lambda kv: kv[0] == "manifest.json"):
        os.makedirs(os.path.dirname(os.path.join(a.out, fn)), exist_ok=True)
        write_atomic(os.path.join(a.out, fn), blob)
    for fn in stale_outputs(a.out, blobs):
        os.remove(os.path.join(a.out, fn))
        print(f"  removed {fn} (no longer written by this layout)")
    print(f"  wrote {a.out}: {len(blobs)} files")


if __name__ == "__main__":
    main()
