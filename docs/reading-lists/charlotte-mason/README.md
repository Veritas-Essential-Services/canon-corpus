# Charlotte Mason's reading lists

`MASON.tsv` lists every book Charlotte Mason's schools set or she named, one row per title, with what became of it. Built 2026-10-27 (the gap check) and 2026-10-30 (the ingest, reading-lists batch 10), at Adam's request.

## Where the titles come from

- **PNEU programmes** (the termly booklists of the Parents' National Educational Union): AmblesideOnline's transcriptions of programmes 1, 2, 42-44 and 90-96, and archive.org scans of programmes 99, 104, 108, 112, 113, 116, 120 and 127. The `forms` column says which programme and form set each book.
- **The Home Education series**, all six volumes: books Mason recommends or sets.

Not seen: programmes 3-41 and 45-89 and most of 97-126, so this is a sample of roughly 25 of about 130 terms, not the whole of what the schools read. Forms V-VI are thin.

## Columns

`title, author, year, kind, source` describe the book (`source`: pneu-programme and/or home-education-series). `flag` marks rows that are not reading-list books: `quoted only` and `criticised` (Mason quotes or argues with the book), `post-Mason 1949 sample` (a programme after her death). `evidence` gives the pages the title was read from.

`status`:

| Status | Meaning |
|---|---|
| `held` | on some branch before this work; `slugs` names it |
| `shelved` | added in batch 10; `shelf` and `slugs` name it |
| `nosource` | public domain, but no downloadable text was found (the note says what was searched) |
| `unknown` | the book could not be identified, or its date could not be settled |
| `notpd` | published after 1930 |
| `held-back` | a source was found and rejected after reading its title page (the note says why) |
| `laned` | a novel by an author another lane owns |
| `deferred` | left out on purpose (the note says why) |
| `missing` | a flagged row (quoted, criticised, 1949) that was not worked |

Original-language set texts (French, German, Italian) are shelved in the original where a PD text exists; a few rows are held only through an English translation, and the note says so.

## Sources and checks

Public domain means US: published 1930 or earlier. Every shelved text went through `fetch_shelf.py --verify --record`; the evidence is in each shelf's `_checks`. Scans dated 1930 or undated were read by eye and listed in `_rights_checked`; scans whose OCR garbles the author's name are in `_identity_checked` with the title-page reading.

gutenberg.org was blocked from the cloud session that did this work, so Gutenberg texts were placed from archive.org's mirror of Project Gutenberg (collection `gutenberg`) and checked there. The shelves record the Gutenberg number as usual, so `fetch_shelf.py` on the PC fetches the current file from gutenberg.org; 16 texts that have no archive.org copy were not fetched here and wait for that run: Aytoun's Lays, Kipling's The Five Nations (2), Fyleman's The Fairy Flute, Frewen Lord's Tales from Westminster Abbey, Prescott's Conquest of Mexico (4), Hartwig's The Polar World, Stopes's The Study of Plant Life, Buckley's Winners in Life's Race, Brown's Marjorie Fleming, Charles's Attila and His Conquerors, and de Staël's De l'Allemagne (2).
