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

    python3 tests/structure_test.py         # 60 offline checks, no corpus needed
    python3 tests/hymn_corpus_test.py       # the hymn JSONL validator (D1-D2)

## Latin hymns (JSONL)

`data/hymns/` holds *Adoro te* and *Pange lingua* as four flat JSONL files
(passages, witnesses, tokens, alignments), one row per clause, every record
keyed by uid. Schema and rules: `pipeline/README-hymn-jsonl.md`.

Extracted from the patrimonium repo 2026-07-22; pre-extraction history
lives there (through commit `d33503e`).
