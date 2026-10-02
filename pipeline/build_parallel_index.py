#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""
build_parallel_index.py -- one row per KJV verse, naming the verse(s) that
hold the same text in every version on the shelf, each in that version's
OWN numbering. Generated; never hand-edit.

    python3 pipeline/build_parallel_index.py           # write data/parallel/kjv-parallel.tsv
    python3 pipeline/build_parallel_index.py --check   # rebuild: byte-identical

    kjv      uid           hebrew    vulgate   douay     brenton   geneva    ...
    Ps.51.1  wh-...        Ps.51.3   Ps.50.3   Ps.50.3   Ps.50.3   Ps.51.1   ...

A cell lists the version's verses, space-separated, in the version's order.
It is empty where the version has no verse for the KJV verse: the book is not
in it (Tyndale here has ten books; Brenton's Nehemiah is in his Ezra column
as Ezra 11-23, so it is not empty), or the version leaves the verse out (the
ASV's Acts 8:37). A version's verse
that holds several KJV verses appears in each of their rows. A version's
verse with NO KJV verse (Tobit, the Greek's additions, psalm titles) is in
no row: the index is keyed by the KJV, and each map's `no_kjv_verse` says why.

WHERE EACH COLUMN COMES FROM (nothing here is a new judgement):
  hebrew    data/versification/bhs-kjv.json (the WLC's verse list, TVTMS)
  greek_nt  data/nt/passages.jsonl + witnesses.jsonl: the RP2018 Greek is a
            witness of the KJV verse's own passage, so its ref is the KJV's.
            On this branch only the John 1:1-18 pilot; the whole Greek NT
            (PR #8) fills the column when it lands.
  vulgate, douay, brenton, geneva, tyndale, ylt, darby, asv
            each unit's `kjv` in data/books/<slug>.json (gitignored: built by
            structure_texts.py from the pinned sources, through the committed
            maps). The build stops if a book is missing rather than write an
            index with a silent hole.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import versification as V  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "data", "parallel", "kjv-parallel.tsv")
BOOKS = os.path.join(ROOT, "data", "books")
SHELF = ["vulgate", "douay", "brenton", "geneva", "tyndale", "ylt", "darby", "asv"]
COLUMNS = ["kjv", "uid", "hebrew", "greek_nt"] + SHELF


def _stop(msg):
    raise SystemExit(f"HARD STOP: {msg}")


def kjv_order():
    out = []
    with open(os.path.join(ROOT, "data", "greppable", "kjv.tsv"), encoding="utf-8") as f:
        for line in f:
            if line.startswith("kjv:"):
                out.append(line.split("\t", 1)[0][4:])
    return out


def _kjv_of(r):
    """The KJV verses a resolution names (psalm titles dropped: no row)."""
    if r.get("resolved"):
        ts = r.get("spans", [r["target"]])
    else:
        ts = r.get("kjv", [])
    return [t[4:] if t.startswith("kjv:") else t for t in ts if not t.endswith(".title")]


def columns():
    rows = {}

    def add(k, col, ref):
        cell = rows.setdefault(k, {}).setdefault(col, [])
        if ref not in cell:
            cell.append(ref)

    heb = V.load()
    for ch, n in heb["hebrew_chapters"].items():
        for v in range(1, n + 1):
            ref = f"{ch}.{v}"
            for k in V.targets(ref, heb):
                if not k.endswith(".title"):
                    add(k, "hebrew", ref)
    nt = os.path.join(ROOT, "data", "nt")
    greek = set()
    with open(os.path.join(nt, "witnesses.jsonl"), encoding="utf-8") as f:
        for line in f:
            w = json.loads(line)
            if w.get("lang") == "grc" and w.get("role") == "original":
                greek.add(w["passage_uid"])
    with open(os.path.join(nt, "passages.jsonl"), encoding="utf-8") as f:
        for line in f:
            p = json.loads(line)
            if p["uid"] in greek and p["citation"].startswith("kjv:"):
                add(p["citation"][4:], "greek_nt", p["osis"])
    for slug in SHELF:
        path = os.path.join(BOOKS, f"{slug}.json")
        if not os.path.exists(path):
            _stop(f"data/books/{slug}.json is missing: run --fetch for its source, then "
                  f"pipeline/structure_texts.py")
        with open(path, encoding="utf-8") as f:
            book = json.load(f)
        for u in book["units"]:
            if "kjv" not in u:
                _stop(f"{u['id']} has no `kjv`: build its map before the book")
            ref = u["id"].split(":", 1)[1]
            for k in _kjv_of(u["kjv"]):
                add(k, slug, ref)
    return rows


def build():
    order = kjv_order()
    with open(os.path.join(ROOT, "data", "uids", "wordhoard.uids.json"), encoding="utf-8") as f:
        uids = json.load(f)["uids"]
    rows = columns()
    stray = sorted(set(rows) - set(order))
    if stray:
        _stop(f"rows for verses the KJV does not have: {stray[:10]}")
    lines = ["\t".join(COLUMNS)]
    for k in order:
        r = rows.get(k, {})
        uid = uids.get(f"kjv:{k}")
        if not uid:
            _stop(f"kjv:{k} has no uid in the registry")
        lines.append("\t".join([k, uid]
                               + [" ".join(r.get(c, [])) for c in COLUMNS[2:]]))
    return ("\n".join(lines) + "\n").encode("utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    blob = build()
    rel = os.path.relpath(OUT, ROOT)
    if a.check:
        if not os.path.exists(OUT) or open(OUT, "rb").read() != blob:
            _stop(f"{rel} missing or differs from a rebuild")
        print(f"OK: {rel} byte-identical")
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT + ".tmp", "wb") as f:
        f.write(blob)
    os.replace(OUT + ".tmp", OUT)
    rows = blob.count(b"\n") - 1
    print(f"wrote {rel}: {rows} rows")


if __name__ == "__main__":
    main()
