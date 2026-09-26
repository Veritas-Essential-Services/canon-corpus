#!/usr/bin/env python3
"""
export_mnemonicon_pack.py -- the hymn JSONL as Mnemonicon import files, one per
hymn. Launch plan C5, first link: a stanza becomes a Mnemonicon recite item
(which the Memoria later takes as a proof).

    python3 pipeline/export_mnemonicon_pack.py              # write exports/mnemonicon/
    python3 pipeline/export_mnemonicon_pack.py --check      # regenerate, assert byte-identical
    python3 pipeline/export_mnemonicon_pack.py --by clause  # one piece per clause instead
    python3 pipeline/export_mnemonicon_pack.py --lines verse    # keep the hymn's verse lines
    python3 pipeline/export_mnemonicon_pack.py --witness pange-lingua=en.literal

    Input:  data/hymns/{passages,witnesses}.jsonl + manifest.json (read only)
    Output: exports/mnemonicon/<slug>.json            (by stanza; committed)
            exports/mnemonicon/<slug>.clauses.json    (--by clause; not committed)
    Tests:  tests/mnemonicon_pack_test.py (the validator; offline)
            tests/mnemonicon_pack_browser_test.js (imports it into the real page)

THE FORMAT IS THE MNEMONICON'S OWN
    Read from `The Mnemonicon Website/site/app.js` (importFiles, repairPiece,
    newPiece) and sync.js (toRow): a file is a JSON ARRAY of whole pieces,
    the same shape as a backup and as the 2026-09-23 memory-work packs.

        {id, createdAt, updatedAt, title, source, category, translation,
         text, notes, tags, srs: {reps, ease, interval, due}, history: []}

    The import adds a piece unless the bank already has its id, or its
    title + source + text (pieceSig). So:
      * `id` is a uuid (the cloud column is one) DERIVED from the passage uid
        (uuid5), never random: a regenerated file re-imports as nothing new.
      * `source` names the hymn, not the English witness. Swapping the
        witness then changes neither id nor signature, and cannot duplicate
        a piece on a card where sync has re-keyed it.
      * createdAt/due come from the corpus's own date (manifest `cut_on`), so
        the file is byte-identical on every run. A due date in the past means
        "due now", which is what a new learning piece is.

WHERE THE ENGLISH GOES
    In the Mnemonicon, `translation` is the NAME of a version -- a one-line
    <input> placeholdered "ESV, KJV…", shown in the review header. So it gets
    the witness's label ("Hopkins 1918"). The English itself goes in `notes`
    (a textarea, shown on the detail page and never during recitation), with
    its lines joined by " / ", followed by the attribution. `text` is the
    Latin reading of record (la.1) and nothing else.

GRANULARITY
    By stanza (default): one piece per stanza, one LINE per CLAUSE -- the
    house row unit (ruling #10), so line-by-line recitation never reveals half
    a clause. `--lines verse` keeps the printed verse lines instead.
    By clause (`--by clause`): one piece per clause. The English witnesses
    render whole stanzas, so a clause piece's notes carry its stanza's English
    and say so.

THE LICENCE GATE
    Only a witness whose manifest source is licensed `PD` is exported. The
    house's own prose (`own`), Whitaker's grant (`free-grant`) and anything
    generated (en.wooden, en.plain) are refused with an error, not skipped:
    a pack is something handed to other people. The Latin must pass the same
    gate.
"""

import argparse
import json
import os
import sys
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "hymns")
OUT = os.path.join(ROOT, "exports", "mnemonicon")

# One namespace for every Mnemonicon piece made from a Word Hoard passage.
# Changing it renames every exported piece: never change it.
NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "https://thewordhoard.com/mnemonicon/piece")

# The Mnemonicon's category list (site/index.html, #f-category). A hymn is sung.
CATEGORY = "Song"

# Per hymn: the short name a piece's title uses, the attribution line, and
# which English witness a pack carries by default. The default is the one the data marks singable (Hopkins; Caswall).
HYMNS = {
    "adoro-te": {
        "short": "Adoro te",
        "author": "attributed to St Thomas Aquinas",
        "witness": "en.singable",
    },
    "pange-lingua": {
        "short": "Pange lingua",
        "author": "St Thomas Aquinas",
        "witness": "en.singable",
    },
}

# A short label per source: the `translation` field for English, and the
# attribution line for the Latin.
LABELS = {
    "roman-missal-received": "the received text of the Roman Missal",
    "hopkins-1918": "Hopkins 1918",
    "caswall-1849-britt-1922": "Caswall 1849 (Britt 1922)",
    "britt-1922-prose": "Britt 1922, literal prose",
}

PD = "PD"


class LicenceRefused(Exception):
    """A witness that is not public domain was asked to leave the house."""


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load(data_dir=DATA):
    passages = {p["uid"]: p for p in read_jsonl(os.path.join(data_dir, "passages.jsonl"))}
    witnesses = {w["address"]: w for w in read_jsonl(os.path.join(data_dir, "witnesses.jsonl"))}
    with open(os.path.join(data_dir, "manifest.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    return passages, witnesses, manifest


def piece_id(uid):
    """The piece's id: stable for ever, and a uuid as the cloud requires."""
    return str(uuid.uuid5(NAMESPACE, uid))


def gate(witness, manifest):
    """Return the witness's source record, or refuse it."""
    if witness.get("generated") or witness.get("text") is None:
        raise LicenceRefused(f"{witness['address']} is generated, not a text: not exported")
    src = manifest["sources"].get(witness["source"])
    if src is None:
        raise LicenceRefused(f"{witness['address']}: source {witness['source']!r} is not in the manifest")
    if src.get("license") != PD:
        raise LicenceRefused(
            f"{witness['address']}: source {witness['source']!r} is licensed "
            f"{src.get('license')!r}, not PD: a pack carries public-domain text only")
    return src


def english(witness):
    return " / ".join(l.strip() for l in witness["text"].split("\n") if l.strip())


def build(slug, by="stanza", lines="clause", witness_name=None, data=None):
    """The pieces for one hymn, in reading order."""
    passages, witnesses, manifest = data or load()
    work = f"hymns:{slug}"
    if work not in manifest["works"] or slug not in HYMNS:
        raise SystemExit(f"unknown hymn {slug!r}")
    title = manifest["works"][work]["title"]
    hymn = HYMNS[slug]
    wname = witness_name or hymn["witness"]
    when = manifest["cut_on"] + "T00:00:00.000Z"
    stanzas = sorted((p for p in passages.values() if p["work"] == work and p["unit"] == "stanza"),
                     key=lambda p: p["stanza"])

    def latin(clause_uid):
        w = witnesses[f"{clause_uid}/la.1"]
        gate(w, manifest)
        return w["text"]

    out = []
    for st in stanzas:
        w = witnesses.get(f"{st['uid']}/{wname}")
        if w is None:
            raise SystemExit(f"{st['citation']} has no {wname} witness")
        src = gate(w, manifest)
        if w.get("lang") != "en":
            raise SystemExit(f"{w['address']} is not English")
        label = LABELS.get(w["source"], w["source"])
        la_key = witnesses[f"{st['clauses'][0]}/la.1"]["source"]
        attribution = (f"Latin: {title}, {hymn['author']}; {LABELS.get(la_key, la_key)}. "
                       f"English: {src['edition']}. Both public domain.")
        if not src.get("verified"):
            attribution += " (The English is not yet checked against the printed edition.)"

        if by == "stanza":
            units = [(st, st["clauses"], f"{hymn['short']}, st. {st['stanza']}")]
        else:
            units = [(passages[c], [c], f"{hymn['short']}, st. {st['stanza']}, cl. {passages[c]['clause']}")
                     for c in st["clauses"]]
        for unit, clause_uids, piece_title in units:
            texts = [latin(c) for c in clause_uids]
            if lines == "clause":
                texts = [" ".join(t.split("\n")) for t in texts]
            head = "English (whole stanza)" if by == "clause" else "English"
            notes = (f"{head}: {english(w)}\n\n{attribution}\n"
                     f"Word Hoard {unit['citation']} · {unit['uid']}")
            out.append({
                "id": piece_id(unit["uid"]),
                "createdAt": when,
                "updatedAt": when,
                "title": piece_title,
                "source": f"{title} ({hymn['author']})",
                "category": CATEGORY,
                "translation": label,
                "text": "\n".join(texts),
                "notes": notes,
                "tags": ["latin", "hymn", slug],
                "srs": {"reps": 0, "ease": 2.5, "interval": 0, "due": when},
                "history": [],
            })
    return out, {"witness": wname, "source": w["source"], "label": label}


def render(pieces):
    """As the app's own export writes it: two-space JSON, then a newline."""
    return (json.dumps(pieces, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def filename(slug, by):
    return f"{slug}.json" if by == "stanza" else f"{slug}.clauses.json"


def write_atomic(path, blob):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(blob)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--by", choices=("stanza", "clause"), default="stanza")
    ap.add_argument("--lines", choices=("clause", "verse"), default="clause",
                    help="a piece's lines: one per clause (default) or the printed verse lines")
    ap.add_argument("--witness", action="append", default=[], metavar="SLUG=NAME",
                    help="the English witness for a hymn, e.g. pange-lingua=en.literal")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    chosen = dict(x.split("=", 1) for x in a.witness)
    data = load()
    blobs = {}
    for slug in HYMNS:
        try:
            pieces, used = build(slug, a.by, a.lines, chosen.get(slug), data)
        except LicenceRefused as e:
            raise SystemExit(f"REFUSED: {e}")
        blobs[filename(slug, a.by)] = render(pieces)
        print(f"  {slug:<14}{len(pieces):>3} pieces   English: {used['witness']} ({used['source']})")

    if a.check:
        stale = [fn for fn, blob in blobs.items()
                 if not os.path.exists(os.path.join(a.out, fn))
                 or open(os.path.join(a.out, fn), "rb").read() != blob]
        if stale:
            raise SystemExit(f"CHECK FAILED: regenerated pack differs from committed: {stale}")
        print("  CHECK PASSED: packs byte-identical.")
        return
    os.makedirs(a.out, exist_ok=True)
    for fn, blob in blobs.items():
        write_atomic(os.path.join(a.out, fn), blob)
    print(f"  wrote {a.out}")


if __name__ == "__main__":
    main()
