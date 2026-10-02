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
    python3 tests/ot_corpus_test.py         # the Hebrew OT JSONL validator
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

## Greek New Testament (JSONL)

`data/nt/` holds the whole New Testament from the Robinson-Pierpont
Byzantine text (public domain): 7,953 verses, 140,149 words, one folder per
book with the same four files, one row per verse, and one manifest over all
of them. John 1:1-18 is the pilot the house drafts and the reader cover. Each verse is a
witness of the KJV verse's existing uid, so nothing is minted. Parsing is
Robinson's; lemmas are Strong's headwords. Schema, licence evidence,
transliteration scheme and the two rulings still open (the Romans doxology,
the sharding): `pipeline/README-nt-jsonl.md` s.16.

## Hebrew Old Testament (JSONL)

`data/ot/` holds the whole Old Testament from the Westminster Leningrad Codex
(public domain): 23,142 KJV verses, 305,124 words, laid out like the NT. Each
Hebrew verse is mapped to its KJV verse through `data/versification/bhs-kjv.json`
and is a witness of that verse's existing uid, so nothing is minted. Ketiv and
qere are both kept. The OSHB lemmas and morphology are CC BY 4.0, so they are
left out of this public repo. Schema, licence evidence and the open rulings
(psalm titles, spans, joined verses): `pipeline/README-ot-jsonl.md`.

Both testaments rebuild from pinned sources in under a minute:
`python3 pipeline/rebuild_bible.py` fetches the pinned inputs (one shallow git
fetch per source repo, sha256-checked), builds, and checks the result is
byte-identical. `--verify` does the same in memory and writes nothing.

## Apostolic Fathers (Greek)

Nine books from Kirsopp Lake's Loeb edition (1912-13, public domain), built
from the First1KGreek TEI: 1 and 2 Clement, the seven letters of Ignatius,
Polycarp to the Philippians, the Martyrdom of Polycarp, the Didache, Barnabas,
Hermas and Diognetus. That is 1,941 sections and 64,890 words, cited the
standard way (`1 Clem. 1.1`, `Ign. Eph. 1.1`, `Herm. Sim. 9.1.1`). The TEI
is CC BY-SA 4.0, so the books are built locally and only their manifest
entries are committed, each labelled. 85% of the Greek words carry a Strong's
number by fixed rules against the Greek NT; the rest are left blank, never
guessed. Lake's scripture references resolve to KJV verses, the Old Testament
through Brenton's Septuagint map, and the ones First1KGreek keyed to the wrong
book are flagged. `python3 pipeline/build_apostolic_fathers.py --fetch`. Lightfoot's
English is aligned to it (next section).

## Apostolic Fathers (English, Lightfoot)

Lightfoot and Harmer's translation (1891, public domain), from CCEL's ThML
(pinned by sha256), as nine books matching Lake's nine. Every English unit is
keyed by the Greek it translates (`1clement-lightfoot:4.7` is `1 Clem. 4.7`)
and links to it. Chapters match by rule; inside a chapter CCEL's paragraphs
are placed on Lake's sections by their lengths, and a boundary is drawn only
where every near-best alignment agrees. Of Lake's 1,941 sections, 1,819 have
an English unit of their own, 114 are reached in a run of two or three, and 8
(four Ignatius chapters) only by chapter. Measured: 99.1% of the one-to-one
pairs have the work's own length ratio (49.6% when shifted by one), and 97.7%
of the proper names in the English are in the linked Greek (15.2% in the next
unit's). Papias is not in CCEL's file. Built locally;
manifest entries committed. `python3 pipeline/build_lightfoot.py --fetch`.

## Josephus (Greek and English)

The Antiquities, the Jewish War, the Life and Against Apion: Niese's Greek
(1885-95) and Whiston's English (1737), both public domain, from the Perseus
TEI, which is CC BY-SA (built locally, labelled in the manifest). Each work's
two books are aligned by Whiston's book.chapter.section (`Ant. 18.3.3`), and
every Greek unit also gives its Niese sections (`18.63-64`), so either
citation finds it. 2,304 aligned units; 72% of the Greek words carry a
Strong's number. `python3 pipeline/build_josephus.py --fetch`.

## Philo (Greek and English)

The 31 treatises of Philo of Alexandria that survive in Greek: Cohn-Wendland's
Greek (1896-1915) and Yonge's English (1854-55), both public domain, from the
First1KGreek TEI, which is CC BY-SA (built locally, labelled in the manifest).
62 books, cited by treatise and Cohn-Wendland section (`Spec. 1.177`) and
aligned section for section; only *On the Special Laws* has Greek sections the
English file lacks, 58 of them, listed. The editors' 1,836 scripture
references are moved out of the Greek into links, and 1,827 resolve to a KJV
verse (`--measure` shows how they number). 70% of the Greek words carry a
Strong's number. `python3 pipeline/build_philo.py --fetch`.

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
