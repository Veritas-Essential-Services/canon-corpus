#!/usr/bin/env python3
"""Measure every Perseus edition and translation, and shelve NONE of them.

    python3 pipeline/perseus_catalog.py --fetch   # first: the repos + catalog (~1.1 GB, gitignored)
    python3 pipeline/perseus_survey.py            # every edition through cts.walk(); writes the survey
    python3 pipeline/perseus_survey.py --check    # the committed survey is what the pinned repos give

Writes data/perseus/survey.jsonl (COMMITTED: one row per edition, facts about
the edition, no text) and data/perseus/survey.meta.json (the Perseus commits
it was measured at, and the totals). Nothing lands in data/books/ and the
manifest is untouched: which of these go on a shelf is Adam's call, and each
still needs its rights line read (CLAUDE.md, the 2026-07-26 gate).

Why a survey before a shelf: three Armarium rebuilds died for want of disk
because sizes were estimated, not measured. This measures.

Each row: urn, repo, kind (edition / translation), lang, author, work, label,
file, bytes, scheme (citation levels, shallow -> deep), units (non-empty leaf
citations), chars, dup_citations, empty_units, imprint_years and a `rights`
PROMPT, never a verdict:
  "imprint <= 1930"      every printed year is 1930 or earlier (US public
                         domain for a US publication as of 2026-01-01; still
                         read the header -- a later translator can hide here)
  "imprint 1931+: read"  a later printing is named; it may be a reprint, or
                         the edition itself may be in copyright (Shorey's
                         Loeb Republic, 1935)
  "no imprint date"      nothing to go on; read the header
and `status`: ok / no-scheme / parse-error / missing-file / empty."""
import csv, json, os, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cts

ROOT = os.path.join(HERE, "..")
PERSEUS = os.path.join(ROOT, "data", "corpus", "perseus")
OUT = os.path.join(ROOT, "data", "perseus")
PD_THROUGH = 1930  # US: published 1930 or earlier is public domain as of 2026-01-01


def rights_prompt(years):
    if not years:
        return "no imprint date"
    return f"imprint <= {PD_THROUGH}" if max(years) <= PD_THROUGH else f"imprint {PD_THROUGH + 1}+: read"


def survey_row(r):
    row = {k: r[k] for k in ("urn", "repo", "kind", "lang", "author", "work", "label", "file")}
    row["bytes"] = int(r["bytes"]) if r["bytes"] else None
    path = os.path.join(PERSEUS, r["file"])
    if not os.path.exists(path):
        return dict(row, status="missing-file")
    try:
        scheme, leaves = cts.walk(path)
        years = cts.imprint_years(path)
    except ValueError:
        return dict(row, status="no-scheme")
    except Exception as e:  # ET.ParseError and friends: Perseus ships a few broken files
        return dict(row, status="parse-error", error=f"{type(e).__name__}: {e}"[:160])
    texts = [t for _, t in leaves if t]
    cites = Counter(".".join(refs) for refs, t in leaves if t)
    row.update(scheme=scheme, units=len(texts), chars=sum(len(t) for t in texts),
               dup_citations=sum(n - 1 for n in cites.values() if n > 1),
               empty_units=len(leaves) - len(texts),
               imprint_years=years, rights=rights_prompt(years),
               status="ok" if texts else "empty")
    return row


def build():
    cat = os.path.join(PERSEUS, "perseus_catalog.csv")
    if not os.path.exists(cat):
        sys.exit("no catalog: run python3 pipeline/perseus_catalog.py --fetch first")
    with open(cat, encoding="utf-8") as f:
        rows = sorted(csv.DictReader(f), key=lambda r: r["urn"])
    out = [survey_row(r) for r in rows]
    with open(os.path.join(PERSEUS, "perseus_catalog.pinned.json"), encoding="utf-8") as f:
        pinned = json.load(f)
    totals = defaultdict(lambda: {"editions": 0, "units": 0, "chars": 0})
    for r in out:
        if r["status"] == "ok":
            k = f"{r['kind']}/{r['lang']}/{r['rights']}"
            totals[k]["editions"] += 1; totals[k]["units"] += r["units"]; totals[k]["chars"] += r["chars"]
    meta = {"perseus_commits": pinned, "pd_through": PD_THROUGH,
            "status": dict(sorted(Counter(r["status"] for r in out).items())),
            "totals": dict(sorted(totals.items())),
            "licence": "Rows are facts about Perseus Digital Library editions (CC BY-SA 4.0, "
                       "github.com/PerseusDL); no text is stored here."}
    return out, meta


def dump(out, meta):
    lines = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in out)
    return lines, json.dumps(meta, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def main():
    out, meta = build()
    lines, m = dump(out, meta)
    paths = (os.path.join(OUT, "survey.jsonl"), os.path.join(OUT, "survey.meta.json"))
    if "--check" in sys.argv:
        same = all(os.path.exists(p) and open(p, encoding="utf-8", newline="").read() == s
                   for p, s in zip(paths, (lines, m)))
        print("CHECK PASSED: survey byte-identical." if same else "CHECK FAILED: the survey differs from the pinned repos.")
        sys.exit(0 if same else 1)
    os.makedirs(OUT, exist_ok=True)
    for p, s in zip(paths, (lines, m)):
        with open(p + ".tmp", "w", encoding="utf-8", newline="\n") as f:
            f.write(s)
        os.replace(p + ".tmp", p)
    print(f"{len(out)} editions -> {paths[0]}")
    print("status:", meta["status"])
    for k, v in meta["totals"].items():
        print(f"  {k:<46} {v['editions']:>5} editions {v['units']:>9,} units {v['chars'] / 1e6:>7.1f}M chars")


if __name__ == "__main__":
    main()
