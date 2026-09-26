#!/usr/bin/env python3
"""
build_lemma_spine.py -- the Latin lemma table from Whitaker's WORDS, and the
committed analyses the hymn build reads. Launch plan D3.

    python3 pipeline/build_lemma_spine.py --fetch   # fetch the pinned files (once)
    python3 pipeline/build_lemma_spine.py           # build and write
    python3 pipeline/build_lemma_spine.py --check   # rebuild; committed files
                                                    #   must be byte-identical

    In:   data/corpus/whitaker/<commit>/  DICTLINE.GEN INFLECTS.LAT UNIQUES.LAT
          ADDONS.LAT LICENCE.txt (fetched at a pinned commit, sha256-checked,
          gitignored like every fetched corpus)
          data/hymns/tokens.jsonl (for the forms to analyse: `search_key` only)

    Out:  data/lemmas/whitaker-la/
            lemmas.jsonl           the FULL table, one row per Whitaker lemma
                                   (~38k rows, ~16 MB). GITIGNORED: rebuildable
                                   from the pins; its sha256 is in the manifest.
            hymns.analyses.jsonl   COMMITTED. One row per distinct hymn form:
                                   every WORDS analysis of it.
            hymns.lemmas.jsonl     COMMITTED. The table rows those analyses
                                   name (the hymns' slice of lemmas.jsonl).
            manifest.json          COMMITTED. Source, commit, pins, licence
                                   verbatim, counts, checksums.

    The hymn build (build_hymn_corpus.py) reads only the committed files, so
    it and its --check stay offline. Format: pipeline/README-lemma-spine.md.
"""

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import whitaker as W  # noqa: E402

OUT = os.path.join(ROOT, "data", "lemmas", "whitaker-la")
TOKENS = os.path.join(ROOT, "data", "hymns", "tokens.jsonl")
SCHEMA = "wordhoard/lemma-table/v1"
COMMITTED = ("hymns.analyses.jsonl", "hymns.lemmas.jsonl", "manifest.json")


def serialize(rows):
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n" for r in rows).encode("utf-8")


def lemma_table(X):
    """One row per distinct dictionary form (WORDS's own name for a lemma).
    Entries that share a form -- e.g. the thirty `qu` lines that all head
    `qui, quae, quod` -- are one lemma with several entries."""
    rows = {}
    for i, e in enumerate(X.entries):
        form, by = X.form(i)
        key = form or f"{e['stems'][0]}  {e['part_text']}"
        r = rows.get(key)
        if r is None:
            r = rows[key] = {"key": key, "lemma": W.principal_parts(form) or None,
                             "headword": W.headword_of(form) if form else W.fold(e["stems"][0]),
                             "pos": e["part"]["pos"], "form_by": by if form else "none",
                             "entries": []}
        r["entries"].append({
            "source": f"DICTLINE.GEN:{e['lines'][0]}" if e["lines"] else e["synthetic"],
            "lines": e["lines"], "stems": e["stems"], "part": e["part_text"],
            "flags": e["flags"], "meaning": e["meaning"]})
    return [rows[k] for k in sorted(rows, key=lambda k: (W.fold(k), k))]


def hymn_forms():
    with open(TOKENS, encoding="utf-8") as f:
        toks = [json.loads(l) for l in f]
    return sorted({t["search_key"] for t in toks if t["witness"] == "la.1"}), len(toks)


def analyses_rows(X, forms):
    out = []
    for form in forms:
        merged = {}
        for a in X.analyze(form):
            k = (a["key"], a["whitaker"], a["enclitic"])
            m = merged.get(k)
            if m is None:
                m = merged[k] = {"key": a["key"], "lemma": a["lemma"], "form_by": a["form_by"],
                                 "headword": a["headword"], "pos": a["parse"]["pos"],
                                 "parse": a["parse"], "whitaker": a["whitaker"],
                                 "enclitic": a["enclitic"], "sources": []}
            if a["source"] not in m["sources"]:
                m["sources"].append(a["source"])
        out.append({"form": form, "analyses": list(merged.values())})
    return out


def build():
    X = W.Whitaker()
    table = lemma_table(X)
    forms, n_tokens = hymn_forms()
    arows = analyses_rows(X, forms)
    used = sorted({a["key"] for r in arows for a in r["analyses"]})
    by_key = {r["key"]: r for r in table}
    uniq_rows = [{"key": a["key"], "lemma": a["lemma"], "headword": a["headword"],
                  "pos": a["pos"], "form_by": a["form_by"], "entries": [
                      {"source": s} for s in a["sources"]]}
                 for r in arows for a in r["analyses"] if a["key"] not in by_key]
    seen = set()
    slice_rows = []
    for k in used:
        if k in by_key:
            slice_rows.append(by_key[k])
    for u in uniq_rows:
        if u["key"] not in seen:
            seen.add(u["key"])
            slice_rows.append(u)
    blobs = {
        "lemmas.jsonl": serialize(table),
        "hymns.analyses.jsonl": serialize(arows),
        "hymns.lemmas.jsonl": serialize(slice_rows),
    }
    found = sum(1 for r in arows if r["analyses"])
    manifest = {
        "schema": SCHEMA,
        "doc": "pipeline/README-lemma-spine.md",
        "language": "la",
        "source": {
            "name": "Whitaker's WORDS",
            "version": W.VERSION,
            "repo": W.REPO_URL,
            "commit": W.COMMIT,
            "files_sha256": {k: v for k, v in W.PINS.items()},
            "port": ("pipeline/whitaker.py: stem+ending matching, verb filters, enclitics and "
                     "dictionary forms ported from the Ada source at the same commit; TRICKS, "
                     "SLURY, SYNCOPE and FIXES are not ported."),
            **W.LICENCE,
        },
        "counts": {
            "dictline_entries": sum(1 for e in X.entries if e["lines"]),
            "synthetic_entries": sum(1 for e in X.entries if not e["lines"]),
            "lemmas": len(table),
            "lemmas_form_by_house": sum(1 for r in table if r["form_by"] == "house"),
            "inflections": len(X.inflects),
            "uniques": len(X.uniques),
            "hymn_tokens": n_tokens,
            "hymn_forms": len(forms),
            "hymn_forms_analysed": found,
            "hymn_forms_unknown": len(forms) - found,
            "hymn_lemmas": len(slice_rows),
        },
        "unknown_forms": [r["form"] for r in arows if not r["analyses"]],
        "files_sha256": {k: hashlib.sha256(v).hexdigest() for k, v in sorted(blobs.items())},
        "gitignored": ["lemmas.jsonl"],
    }
    blobs["manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return blobs, manifest


def write_atomic(path, blob):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(blob)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="fetch the pinned Whitaker files")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.fetch or not W.have_cache():
        if a.check and not a.fetch:
            raise SystemExit("the Whitaker files are not fetched; run with --fetch first")
        W.fetch()
    blobs, man = build()
    for k, v in man["counts"].items():
        print(f"  {k:<22}{v:>8,}")
    if a.check:
        stale = [fn for fn in COMMITTED
                 if not os.path.exists(os.path.join(OUT, fn))
                 or open(os.path.join(OUT, fn), "rb").read() != blobs[fn]]
        if stale:
            raise SystemExit(f"CHECK FAILED: rebuilt output differs from committed: {stale}")
        print("  CHECK PASSED: committed lemma files byte-identical.")
        return
    os.makedirs(OUT, exist_ok=True)
    for fn, blob in blobs.items():
        write_atomic(os.path.join(OUT, fn), blob)
    print(f"  wrote {OUT}")


if __name__ == "__main__":
    main()
