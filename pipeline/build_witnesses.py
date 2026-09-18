#!/usr/bin/env python3
"""
build_witnesses.py -- compose the KJV's two transcriptions into ONE book with
two witnesses and one uid per verse.

    python3 pipeline/build_witnesses.py                 # build + mint
    python3 pipeline/build_witnesses.py --check         # rebuild, assert 0 minted
    python3 pipeline/build_witnesses.py --report        # stats only, no write

WHAT THIS IS NOT
    NOT a third KJV recipe. It parses nothing and transcribes nothing; it
    COMPOSES two existing converter outputs. The 2026-09-11b ruling stands --
    "two recipes for one file is the exact drift this project keeps getting
    bitten by" -- and this deliberately does not become a third. If either
    input is rebuilt, rerun this; it will mint zero.

WHY TWO WITNESSES AND NOT ONE FILE
    Measured 2026-09-17/18, and the second line is the finding:

        kjv.source  31,102 verses  gutenberg, this repo's own source of record
        kjv.italic  31,102 verses  pythonbible-kjv, supplied-word italics marked

        identical once supplied-word marks are set aside   29,517  (94.9%)
        genuinely disagreeing                               1,585  ( 5.1%)

    The 1,585 are not markup. They are spelling (`Tubalcain` / `Tubal-cain`),
    hyphenation, punctuation and capitalisation differences between two
    published editions of the KJV. Neither is wrong. A script that picked a
    winner would be manufacturing a text no edition prints, so each one is
    flagged `transcriptions_differ` and classified in kjv.adjudication.json.

    And the brackets are not noise: they are the KJV's translator-supplied-word
    italics. If Milton echoes a phrase containing a supplied word he echoed the
    ENGLISH, not the Hebrew. That is a finding the corpus should be able to
    state, which is why the marks are preserved rather than stripped.

    Until 2026-09-17 there was no way to say "one passage, two renderings",
    because `kjv:Gen.1.2` was doing identity AND address at once. So the repo
    did the only thing available and kept two files with COLLIDING ids -- and
    half the Bible's identifiers named two different strings. This script is
    that problem dissolving into an ordinary witness.

THE MODEL, which is the hymn/Latin model unchanged
    Ruled 2026-09-15: a passage has one id; `wooden`, `plain`, `elegant`,
    `singable` hang off it as witnesses, and a singable English verse is a
    WITNESS, not a separate text. A KJV verse with italics marked and the same
    verse with italics resolved is exactly that relation.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BOOKS = os.path.join(ROOT, "data", "books")
UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")
OUT = os.path.join(BOOKS, "kjv.witnesses.json")

sys.path.insert(0, HERE)
import wh_uid as U  # noqa: E402

# Witness name -> (file, source of record, what the text carries).
# The name says what the rendering IS, never where it came from, because a
# source can be replaced without the rendering changing meaning.
WITNESSES = {
    "kjv.source": {
        "file": "kjv.source.json",
        "source": "data/corpus/kjv_bible.txt (Project Gutenberg), read by adjudicate_kjv.py",
        "marks_supplied_words": False,
        "note": ("The repo's own source of record, read correctly: 31,102 verses, "
                 "66 books, zero numbering gaps. Supersedes kjv.json, which is the "
                 "same edition read by the pre-f5866fe parser and 420 verses short."),
    },
    "kjv.italic": {
        "file": "kjv.complete.json",
        "source": "pythonbible-kjv",
        "marks_supplied_words": True,
        "note": ("A SECOND EDITION, not a rendering of the first. Carries the "
                 "translator-supplied-word italics as [brackets] -- the reason it "
                 "is kept -- and differs from kjv.source in spelling, hyphenation "
                 "and punctuation in ways that are edition differences, not errors."),
    },
}

# Which witness a bare citation resolves to when nobody asks for one.
#
# kjv.source. It is verse-perfect (proved by adjudicate_kjv.py against the file
# it is parsed from, structurally, with no heading string matched), it is the
# edition this repo actually holds, and it carries no external dependency.
# kjv.italic is kept for the supplied-word information and as the second
# reading that makes adjudication possible at all -- NOT as the default text,
# because it is a different edition and defaulting to it would silently swap
# which KJV the corpus means.
READING_OF_RECORD = "kjv.source"

_WS = re.compile(r"\s+")
_BRACKET = re.compile(r"[\[\]]")


def debracket(s):
    """The text with supplied-word marking removed. NOT a normalisation --
    this is still the printed text, just without the italic marks. The
    matching surface (lowercased, depunctuated) is data/greppable/kjv.norm.tsv
    and is generated elsewhere; do not reimplement it here."""
    return _WS.sub(" ", _BRACKET.sub("", s)).strip()


def load(name):
    p = os.path.join(BOOKS, name)
    if not os.path.exists(p):
        sys.exit(f"missing input: {p}\n"
                 f"Both KJV builds must be present. This script composes; it "
                 f"does not parse.")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def build(write=True, check=False):
    books = {w: load(cfg["file"]) for w, cfg in WITNESSES.items()}
    units = {w: {u["id"]: u for u in b["units"]} for w, b in books.items()}

    for w, d in units.items():
        print(f"  {w:<14} {len(d):>7,} units  ({WITNESSES[w]['file']})")

    every_id = set()
    for d in units.values():
        every_id |= set(d)

    # Order by the reading of record, then anything it lacks, so the output is
    # stable across runs and a diff means a real change.
    ordered = [u["id"] for u in books[READING_OF_RECORD]["units"]]
    ordered += sorted(every_id - set(ordered))

    reg = U.WhUidRegistry(UIDS)
    out_units = []
    stats = {"both": 0, "only": {w: 0 for w in WITNESSES},
             "differ_debracketed": 0, "identical_debracketed": 0, "supplied_total": 0}

    for cid in ordered:
        present = {w: units[w][cid] for w in WITNESSES if cid in units[w]}
        uid = reg.uid_for(cid)
        rec = {"uid": uid, "id": cid, "witnesses": {}, "flags": []}

        ref = next((p.get("ref") for p in present.values() if p.get("ref")), None)
        if ref:
            rec["ref"] = ref

        # links[] is the ThML scripRef harvest -- identical across witnesses by
        # construction, so it belongs on the passage, not on a rendering.
        links = []
        for p in present.values():
            for l in p.get("links") or []:
                if l not in links:
                    links.append(l)
        if links:
            rec["links"] = links

        for w, p in present.items():
            text = p.get("text", "")
            entry = {"text": text}
            if WITNESSES[w]["marks_supplied_words"]:
                n = text.count("[")
                entry["supplied"] = n
                stats["supplied_total"] += n
            rec["witnesses"][w] = entry

        if len(present) == len(WITNESSES):
            stats["both"] += 1
            texts = {debracket(p.get("text", "")) for p in present.values()}
            if len(texts) > 1:
                stats["differ_debracketed"] += 1
                rec["flags"].append("transcriptions_differ")
            else:
                stats["identical_debracketed"] += 1
        else:
            missing = [w for w in WITNESSES if w not in present]
            for w in missing:
                rec["flags"].append(f"missing:{w}")
            for w in WITNESSES:
                if w not in missing:
                    stats["only"][w] += 1

        if not rec["flags"]:
            del rec["flags"]
        out_units.append(rec)

    doc = {
        "slug": "kjv",
        "title": "The Holy Bible (KJV)",
        "author": "—",
        "scheme": {
            "citation": "Book chapter:verse (OSIS ids)",
            "resolution": "verse",
            # Golden rule 4: honesty fields are load-bearing; never pretend
            # precision. The old manifest claimed "exact" on a file missing
            # 420 verses. This says what is actually true.
            "honesty": ("verse-perfect: 31,102 verses, 66 books, 1,189 chapters, "
                        "zero numbering gaps in BOTH witnesses, proved by "
                        "pipeline/adjudicate_kjv.py against the raw source. "
                        "NOT word-perfect across witnesses: they are two "
                        "editions and disagree in 1,585 verses after "
                        "supplied-word marks are set aside; every "
                        "disagreement is classified in kjv.adjudication.json "
                        "and none is repaired."),
            "identity": U.WhUidRegistry.SCHEME,
            "reading_of_record": READING_OF_RECORD,
        },
        "witnesses": {w: {k: v for k, v in cfg.items() if k != "file"}
                      for w, cfg in WITNESSES.items()},
        "units": out_units,
    }

    print()
    print(f"  passages                    {len(out_units):>7,}")
    print(f"    both witnesses            {stats['both']:>7,}")
    for w in WITNESSES:
        print(f"    only {w:<21}{stats['only'][w]:>7,}")
    print(f"  transcriptions identical    {stats['identical_debracketed']:>7,}"
          f"   (after removing supplied-word marks)")
    print(f"  transcriptions DIFFER       {stats['differ_debracketed']:>7,}"
          f"   <- real editorial divergence, flagged per passage")
    print(f"  supplied words marked       {stats['supplied_total']:>7,}")
    print()
    s = reg.stats()
    print(f"  uids minted {s['minted']:,} / reused {s['reused']:,} "
          f"/ registry total {s['total']:,}")

    if check:
        reg.assert_no_mint()
        print("  CHECK PASSED: a rebuild moved no identifier.")
        return doc, reg

    if write:
        reg.save()
        os.makedirs(BOOKS, exist_ok=True)
        tmp = OUT + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        os.replace(tmp, OUT)
        print(f"  wrote {OUT}")
        print(f"  wrote {UIDS}   <- COMMIT THIS")
    return doc, reg


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--check", action="store_true",
                    help="rebuild and assert zero uids minted (the production gate)")
    ap.add_argument("--report", action="store_true",
                    help="stats only; write nothing")
    args = ap.parse_args()
    build(write=not args.report, check=args.check)
