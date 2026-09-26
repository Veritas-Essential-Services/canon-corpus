#!/usr/bin/env python3
"""
build_nt_corpus.py -- the Greek New Testament in the four-file corpus format,
one row per VERSE, every record keyed by uid. Pilot: John 1:1-18.

    python3 pipeline/build_nt_corpus.py --fetch     # pinned inputs -> data/corpus/ (sha256-checked)
    python3 pipeline/build_nt_corpus.py             # build, write data/nt/
    python3 pipeline/build_nt_corpus.py --check     # rebuild, assert 0 minted
                                                    #   and byte-identical output
    python3 pipeline/build_nt_corpus.py --report    # stats only, no write
    python3 pipeline/build_nt_corpus.py --survey    # the WHOLE NT, measured, never
                                                    #   written: what a full run would hit

    Output: data/nt/{passages,witnesses,tokens,alignments}.jsonl + manifest.json
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
    ("byz", "source/CCAT/04_JOH.TXT"): "d3d4d6179c1a1dd2fa4ec37538794d505321d081da2dd10171d14045bc53da45",
    ("byz", "source/Strongs/04_JOH.BP5"): "876b94397e61d1ae1d9531d31e9f9ec83462a699aae1a44a7b9b1f19ffa8e687",
    ("byz", "csv-unicode/ccat/no-variants/JOH.csv"): "06251d70a77f4d17e8dbde054e82ee947ef7834378348e5bcfa938803b42447b",
    ("byz", "csv-unicode/strongs/with-parsing/JOH.csv"): "c1c004f56e931630ac98cb973dea8b2da4d5220d707cd66fe980cb8c11e1fa9c",
    ("strongs", STRONGS_XML): "df928f01b37632f8af9f16289ce58d10b958014cb5dbd1e1ea715a8d311a0625",
}

# byztxt file stem -> (source number, OSIS book). The whole NT is listed so
# --survey can measure it; the pilot builds only SELECTION.
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

# The pilot. One pericope; a label, not an identity (nothing is minted for it).
SELECTION = {"stem": "JOH", "chapter": 1, "first": 1, "last": 18,
             "pericope": "John.1.1-18", "title": "The Prologue of John"}

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
    "plain_form": "null: set only by an override row (a dictionary gloss has no prose form)",
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

def build(reg):
    verify_pins()
    stem = SELECTION["stem"]
    num, osis = BOOK[stem]
    ccat = read_csv(_path("byz", f"csv-unicode/ccat/no-variants/{stem}.csv"))
    bp5 = read_csv(_path("byz", f"csv-unicode/strongs/with-parsing/{stem}.csv"))
    b_ccat = read_beta(_path("byz", f"source/CCAT/{num}_{stem}.TXT"), ":")
    b_bp5 = read_beta(_path("byz", f"source/Strongs/{num}_{stem}.BP5"), ".")
    heads = load_strongs()
    entries = G.load_entries(open(_path("strongs", STRONGS_XML), encoding="utf-8").read())
    try:
        overrides = G.load_overrides()
    except ValueError as e:
        _stop(f"gloss overrides: {e}")
    used_ov = set()

    passages, witnesses, tokens, alignments = [], [], [], []
    apparatus = {}
    ch = SELECTION["chapter"]
    for vs in range(SELECTION["first"], SELECTION["last"] + 1):
        ref = f"{osis}.{ch}.{vs}"
        citation = f"kjv:{ref}"
        if (ch, vs) not in ccat or (ch, vs) not in bp5:
            _stop(f"{ref} missing from the RP files")
        try:
            uid = reg.uid_for(citation)
        except U.WhUidError:
            _stop(f"{citation} has no uid: a versification question, not new content. "
                  f"Nothing is minted for a Greek verse.")
        try:
            surfaces, words = pair_verse(ref, ccat[(ch, vs)], bp5[(ch, vs)],
                                         b_ccat.get((ch, vs)), b_bp5.get((ch, vs)))
        except ValueError as e:
            _stop(str(e))
        for m in _APPARATUS.finditer(b_ccat.get((ch, vs), "")):
            apparatus[m.group(1)] = apparatus.get(m.group(1), 0) + 1

        passages.append({
            "uid": uid, "citation": citation, "kind": "passage", "unit": "verse",
            "book": osis, "osis": ref, "chapter": ch, "verse": vs,
            "versification": "kjv", "pericope": SELECTION["pericope"],
            "reading_of_record": FACING,
            "status": "machine-built from public-domain sources, unchecked",
        })
        text = ccat[(ch, vs)]
        witnesses.append({
            "address": U.address(uid, WITNESS), "passage_uid": uid, "name": WITNESS,
            "lang": "grc", "role": "original", "register": "koine",
            "textform": "byzantine", "text": text, "paragraph_starts": paragraph_starts(text),
            "generated": False,
            "source": "rp2018-byztxt", "attested": "Y", "reading_of_record": False,
        })
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
            gloss, prov_gloss = G.gloss_for(code, entries.get(strongs))
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
        alignments.append({
            "alignment_id": f"{U.address(uid, WITNESS)}~{FACING}",
            "level": "section", "type": "1:1",
            "a": [{"address": U.address(uid, WITNESS), "tokens": None}],
            "b": [{"address": U.address(uid, FACING), "tokens": None}],
            "confidence": "high",
            "note": ("verse to verse under one uid; the KJV translates the Textus Receptus, "
                     "so this aligns verses, not readings"),
        })

    stale = sorted(set(overrides) - used_ov)
    if stale:
        _stop(f"gloss overrides name tokens that do not exist: {stale[:5]}")
    sources = dict(SOURCES)
    inputs = {rel: want for (repo, rel), want in sorted(PINS.items())}
    for layer in sorted({overrides[a]["layer"] for a in used_ov}):
        sources[layer] = OVERRIDE_SOURCES[layer]
    if used_ov:
        inputs["gloss-overrides.jsonl"] = sha256(G.OVERRIDES)
    finite = sum(1 for t in tokens if is_finite(t["parsing"]))
    by_rule = {r: sum(1 for t in tokens if t["provenance"]["gloss"]["rule"] == r)
               for r in G.RULE_ORDER}
    by_layer = {k: sum(1 for t in tokens if t["provenance"]["gloss"]["source"] == k)
                for k in G.OVERRIDE_LAYERS}
    why_none = {}
    for t in tokens:
        if t["gloss"] is None:
            w = t["provenance"]["gloss"]["why"]
            why_none[w] = why_none.get(w, 0) + 1
    manifest = {
        "schema": SCHEMA,
        "doc": "pipeline/README-nt-jsonl.md",
        "built_on": BUILT_ON,
        "row_unit": "verse",
        "selection": dict(SELECTION, osis_book=osis),
        "counts": {"passages": len(passages), "verses": len(passages),
                   "witnesses": len(witnesses), "tokens": len(tokens),
                   "alignments": len(alignments),
                   "tokens_with_lemma": sum(1 for t in tokens if t["lemma"]),
                   "tokens_with_parsing": sum(1 for t in tokens if t["parsing"]),
                   "tokens_with_gloss": sum(1 for t in tokens if t["gloss"]),
                   "tokens_without_gloss": sum(1 for t in tokens if not t["gloss"]),
                   "tokens_flagged_for_review": sum(1 for t in tokens if t["review"]),
                   "distinct_lemmas": len({t["lemma_key"] for t in tokens}),
                   "finite_verbs": finite},
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
                    "translation."),
            "source": "strongs-1890",
            "doc": "pipeline/README-nt-jsonl.md s.12; pipeline/strongs_gloss.py",
            "rules": [{"id": r, "does": G.RULES[r]} for r in G.RULE_ORDER],
            "by_rule": by_rule,
            "by_override": by_layer,
            "none": sum(why_none.values()),
            "none_by_reason": dict(sorted(why_none.items())),
            "overrides": {"file": "data/nt/gloss-overrides.jsonl",
                          "layers": list(G.OVERRIDE_LAYERS),
                          "applied": len(used_ov),
                          "rule": ("a row replaces the dictionary gloss of one token address; "
                                   "the dictionary value and its rule are kept under "
                                   "provenance.gloss.was")},
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
            raise SystemExit(f"CHECK FAILED: rebuilt output differs from committed: {stale}")
        print("  CHECK PASSED: minted 0, output byte-identical.")
        return
    if a.report:
        return
    os.makedirs(a.out, exist_ok=True)
    for fn, blob in blobs.items():
        write_atomic(os.path.join(a.out, fn), blob)
    print(f"  wrote {a.out}")


if __name__ == "__main__":
    main()
