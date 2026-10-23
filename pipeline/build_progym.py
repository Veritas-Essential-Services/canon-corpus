#!/usr/bin/env python3
# prov: 2026-10-20 claude-opus-5-5 drafted (the Word Hoard's ProGym room: Aphthonius into the Armarium)
# fable_review: pending
"""
build_progym.py -- compose Aphthonius's Progymnasmata, in three editions, into ONE work with
fourteen passages (the exercises), three witnesses each, and one uid per exercise.

    python3 pipeline/build_progym.py              # build + mint
    python3 pipeline/build_progym.py --check      # rebuild, assert 0 minted
    python3 pipeline/build_progym.py --report     # stats only, no write

WHAT THIS IS NOT
    Not a converter. It parses nothing: the three editions are structure_texts.py's books
    (aphthonius-rabe, aphthonius-agricola, rainolde-foundacion), and their unit ids already carry
    the exercise (`aphthonius-rabe:chreia.8`). If any of them is rebuilt, rerun this; it will mint zero.

THE MODEL, which is the KJV's (build_witnesses.py) unchanged
    A passage has one uid; each edition is a WITNESS. Here the passage is an exercise, not a verse,
    because no two of these editions can be aligned below it: Rabe cites by page, Agricola's Latin
    and Rainolde's English by paragraph, and Rainolde is an adaptation with his own model orations.
    So a witness records which of its edition's units make up the exercise, never a copy of the text;
    the text stays in the edition's own book.

CITATIONS
    The work is `aphthonius:progym`; an exercise is `aphthonius:progym.<key>`, with the ProGym room's
    own keys (fable ... law). The room stores the exercise's uid as `armarium_uid`
    (wordhoard apps/progym/data/exercises.json).
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BOOKS = os.environ.get("BOOKS_OUT") or os.path.join(ROOT, "data", "books")
UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")
OUT = os.path.join(BOOKS, "aphthonius.witnesses.json")

sys.path.insert(0, HERE)
import wh_uid as U  # noqa: E402
from structure_texts import PROGYM_EXERCISES  # noqa: E402

WORK = "aphthonius:progym"

# Witness name -> its edition. The name says what the rendering IS (language, then edition).
WITNESSES = {
    "grc.rabe": {"book": "aphthonius-rabe", "lang": "grc", "kind": "text",
                 "note": "Aphthonius's Greek, ed. Hugo Rabe (Teubner, Rhetores Graeci X, 1926), the edition "
                         "scholars cite by page. Unproofread OCR."},
    "la.agricola": {"book": "aphthonius-agricola", "lang": "la", "kind": "translation",
                    "note": "Rudolph Agricola's Latin (Paris, 1540), the version the Renaissance schools used. "
                            "Unproofread OCR; the long s reads as f."},
    "en.rainolde": {"book": "rainolde-foundacion", "lang": "en", "kind": "adaptation",
                    "note": "Richard Rainolde, The Foundacion of Rhetorike (1563), the first English "
                            "progymnasmata: Aphthonius's method with Rainolde's own models, by way of "
                            "Lorichius's Latin. A witness to the exercise, not to Aphthonius's wording."},
}
READING_OF_RECORD = "grc.rabe"


def load(slug):
    p = os.path.join(BOOKS, slug + ".json")
    if not os.path.exists(p):
        sys.exit(f"missing input: {p}\nBuild it first: python3 pipeline/structure_texts.py")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def compose(books, reg):
    """books: witness name -> edition book. Returns the work document."""
    passages = []
    for key, label in PROGYM_EXERCISES:
        cite = f"{WORK}.{key}"
        rec = {"uid": reg.uid_for(cite), "id": cite, "n": len(passages) + 1, "label": label,
               "witnesses": {}}
        for w, book in books.items():
            units = [u for u in book["units"] if u["id"].split(":", 1)[1].split(".", 1)[0] == key]
            if not units:
                raise ValueError(f"{w}: the {key} exercise has no units in {book['slug']}")
            entry = {"units": [u["id"] for u in units],
                     "words": sum(len(u["text"].split()) for u in units)}
            pages = [u["page"] for u in units if "page" in u]
            if pages:
                entry["pages"] = [min(pages), max(pages)]
            rec["witnesses"][w] = entry
        passages.append(rec)
    return {
        "slug": "aphthonius",
        "uid": reg.uid_for(WORK),
        "id": WORK,
        "title": "Aphthonius, Progymnasmata",
        "author": "Aphthonius of Antioch (4th-5th c.)",
        "scheme": {
            "citation": "aphthonius:progym.<exercise> (fable, narrative, chreia, maxim, refutation, "
                        "confirmation, commonplace, encomium, invective, comparison, characterization, "
                        "description, thesis, law)",
            "resolution": "exercise; below it, each witness's own units (Rabe's page, a paragraph)",
            "honesty": "the fourteen exercises are found in every witness by its own headings, and every "
                       "converter fails the build unless all fourteen are found in order. Below the "
                       "exercise nothing is aligned: the editions do not share pages or paragraphs, and "
                       "Rainolde's models are his own. Two witnesses are unproofread OCR.",
            "identity": U.WhUidRegistry.SCHEME,
            "reading_of_record": READING_OF_RECORD,
        },
        "witnesses": {w: cfg for w, cfg in WITNESSES.items()},
        "units": passages,
    }


def build(write=True, check=False):
    books = {w: load(cfg["book"]) for w, cfg in WITNESSES.items()}
    reg = U.WhUidRegistry(UIDS)
    doc = compose(books, reg)
    for p in doc["units"]:
        print(f"  {p['n']:>2} {p['id']:<34} {p['uid']}  " +
              "  ".join(f"{w} {e['words']:>5}w" for w, e in p["witnesses"].items()))
    s = reg.stats()
    print(f"  uids minted {s['minted']:,} / reused {s['reused']:,} / registry total {s['total']:,}")
    if check:
        reg.assert_no_mint()
        print("  CHECK PASSED: a rebuild moved no identifier.")
        return doc
    if write:
        reg.save()
        os.makedirs(BOOKS, exist_ok=True)
        tmp = OUT + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        os.replace(tmp, OUT)
        print(f"  wrote {OUT}")
        print(f"  wrote {UIDS}   <- COMMIT THIS")
    return doc


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--check", action="store_true", help="rebuild and assert zero uids minted")
    ap.add_argument("--report", action="store_true", help="stats only; write nothing")
    a = ap.parse_args()
    build(write=not a.report, check=a.check)
