#!/usr/bin/env python3
"""
build_kjv_italic.py -- data/books/kjv.complete.json, the `kjv.italic` witness.

    python3 pipeline/build_kjv_italic.py

build_witnesses.py composes two KJV builds. kjv.json comes from
structure_texts.py; this is the other one. Until 2026-10-17 the recipe for
kjv.complete.json lived only on the machine that first built it, so a lost
data/books/ meant the identity gate could not run anywhere.

It parses nothing. Its source is the COMMITTED data/greppable/kjv.tsv, the
pythonbible-kjv text with the translators' supplied words in [brackets],
written by build_kjv.py. So the witness rebuilds from the repo alone, with no
package and no network. Refs are "Book c:v" from structure_texts.KJV_BOOKS.
Atomic write (rule 5).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "data", "greppable", "kjv.tsv")
OUT = os.path.join(ROOT, "data", "books", "kjv.complete.json")

sys.path.insert(0, HERE)
from structure_texts import KJV_BOOKS  # noqa: E402

NAME = {o: n for _t, o, n in KJV_BOOKS}


def build():
    units = []
    with open(SRC, encoding="utf-8") as f:
        next(f)  # header: id, text
        for line in f:
            cid, text = line.rstrip("\n").split("\t", 1)
            osis, c, v = cid.split(":", 1)[1].rsplit(".", 2)
            units.append({"id": cid, "ref": f"{NAME[osis]} {c}:{v}",
                          "text": text, "links": []})
    return {"slug": "kjv", "title": "The Holy Bible (KJV)", "author": "—",
            "source": {"path": "data/greppable/kjv.tsv", "format": "pythonbible-kjv tsv"},
            "units": units}


if __name__ == "__main__":
    doc = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    os.replace(tmp, OUT)
    print(f"wrote {OUT}: {len(doc['units']):,} verses")
