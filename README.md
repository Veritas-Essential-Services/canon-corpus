---
model_log:
  - 2026-07-22 claude-fable-5 drafted (from git trailer; backfilled 2026-09-30)
  - 2026-09-26 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
  - 2026-09-27 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
fable_review: pending
---
# canon-corpus

The shared source + structure layer of the Canon OS: manifest-driven
fetchers for public-domain texts (Perseus TEI, CCEL ThML, Project
Gutenberg) and converters that turn them into unit-id JSON with canonical
citations, scripture keylinks, and honest resolution metadata.

*Commit the manifest and the recipe; the texts refetch.* Corpus and built
JSON are gitignored — `data/books/manifest.json` (checksums, schemes,
provenance) is the committed record of the collection.

## Build the library

    python3 pipeline/fetch_sources.py       # fetch sources -> data/corpus/
    python3 pipeline/structure_texts.py     # convert       -> data/books/*.json

## Consumers

- [armarium](../armarium) — the personal Libronix (search, reverse
  concordance, reader). Expects this repo as a sibling checkout.
- patrimonium — the Nomenclator's card backs.
- Memoria / the Resolver — future.

## Tests

    python3 tests/structure_test.py         # 83 offline checks, no corpus needed
    python3 tests/versification_test.py     # the Hebrew->KJV verse map (BDB's citations)
    python3 tests/vulgate_versification_test.py  # the Clementine Vulgate->KJV verse map
    python3 tests/hymn_corpus_test.py       # the hymn JSONL validator (D1-D2)
    python3 tests/lemma_spine_test.py       # the Latin lemma spine (D3)
    python3 tests/nt_corpus_test.py         # the Greek NT JSONL validator (D2-D5 pilot)
    python3 tests/reader_test.py            # the reader: deterministic, self-contained, every token (D5)
    python3 tests/review_test.py            # review.py end to end, on a temp copy of the repo
    python3 tests/lemma_bridge_test.py      # English lemma bridge (ADR 0012): shew/show, holpen/help in real FTS5
    python3 tests/remint_maxims_test.py     # remint_maxims.py end to end, on a temp copy

## Adam's review sheets

    python3 pipeline/review.py status               # answered vs open, per sheet
    python3 pipeline/review.py apply <sheet.md>     # his answers -> override rows, rebuild, --check
    python3 pipeline/review.py render [--check]     # the sheets, regenerated from the data

`docs/review/2026-09-26-lemma-flags.md` (24 Latin tokens -> `data/lemmas/adam-reviewed.jsonl`)
and `docs/review/2026-09-26-john1-drafts.md` (137 house glosses and 18 plain lines ->
`data/nt/gloss-overrides.jsonl`, `data/nt/prose-order.jsonl`). The answers `ok`/`✓`,
`draft→` and a value are explained in `pipeline/README-lemma-spine.md` s.8b and
`pipeline/README-nt-jsonl.md` s.15. Anything ambiguous stops the run and names the row.

## Adam's maxims: re-mint to house uids (prepared, not run)

    python3 pipeline/remint_maxims.py            # dry run (the default): writes nothing
    python3 pipeline/remint_maxims.py --write    # mint maxims:AK-00n in the registry; write the Hoard records
    python3 pipeline/remint_maxims.py --check    # the written records match the source and the registry

**The maxims are private, and this repo is public.** Since 2026-09-27 the
source and its records live in the Word Hoard house repo, cloned beside this
one (or set `WORDHOARD_HOUSE`): `wordhoard/data/maxims/maxims-original.jsonl`
stays as filed, and `--write` adds `wordhoard/data/maxims/maxims-original.hoard.jsonl`,
one `passage/maxim` Hoard record per maxim, `ak-maxim-000n` kept in `legacy[]`.
That file is what the Florilegium's Propria imports. Their `maxims:` citations
go in the house's private registry; only the bare uids come back here, as
`reserved` (see `data/uids/`).

## Latin hymns (JSONL)

`data/hymns/` holds *Adoro te* and *Pange lingua* as four flat JSONL files
(passages, witnesses, tokens, alignments), one row per clause, every record
keyed by uid. Schema and rules: `pipeline/README-hymn-jsonl.md`.
Each token's lemma comes from Whitaker's WORDS where it agrees with the house
draft (launch plan D3): `pipeline/README-lemma-spine.md`.

## Greek New Testament (JSONL, pilot)

`data/nt/` holds John 1:1-18 from the Robinson-Pierpont Byzantine text
(public domain) in the same four files, one row per verse. Each verse is a
witness of the KJV verse's existing uid, so nothing is minted. Parsing is
Robinson's; lemmas are Strong's headwords. Schema, licence evidence,
transliteration scheme and the full-NT plan: `pipeline/README-nt-jsonl.md`.

## The reader (reverse interlinear, D5)

    python3 pipeline/render_reader.py       # -> build/reader/reader.html (gitignored)

One renderer over both datasets: *Adoro te*, *Pange lingua* and John 1:1-18 in
one self-contained HTML file (inline CSS and JS, no network, no web fonts,
light and dark, readable at 375px). Each passage shows the original, with every
word tappable for lemma, parsing and translit, and then the columns wooden /
plain / elegant / singable. A column the data cannot fill is shown empty with
its reason: the Greek has no glosses yet, so it has no wooden or plain line.
`wooden` and `plain` come from `render_wooden()` / `render_plain()` in
`build_hymn_corpus.py` and are never stored. Each source's licence and
attribution is on the page. The agreement marks are drawn from the draft's
`syntax` notes and toggle between two candidate forms. The choice between them
is Adam's: `docs/reader-agreement-marks.md`.

Extracted from the patrimonium repo 2026-07-22; pre-extraction history
lives there (through commit `d33503e`).
