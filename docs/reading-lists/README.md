# Classical reading lists → public-domain ingest

<!-- model: claude-opus-5-5 drafted 2026-10-10 (project thread) -->

Every work on the published reading lists of eight classical-Christian schools and publishers, deduplicated, checked against everything canon-corpus holds on **any** branch, and the missing public-domain titles ingested in batches.

| List | Evidence | How complete |
|---|---|---|
| Classical Conversations (Foundations, Essentials, Challenge A–IV) | CC bookstore bundles + CC's "117 must-read books" | Challenge levels complete; Foundations/Essentials have no literature list |
| Canon Press (Moscow, ID) | the shop catalogue (Canon Classics, Christian Heritage Series, reprints) | complete for pre-1930 titles |
| New Saint Andrews College | 2027 undergraduate catalog; graduate CCS courses | catalog often names authors, not works |
| Logos School | elementary literature list; grade 1–8 reading guides; secondary overview | high-school lists are not public |
| Logos Online School | Integrated Humanities course pages (Omnibus I–VI) + electives | good |
| Bethlehem College & Seminary | 2012–13 and 2026–27 catalogs; faculty posts | partial: no published great-books list exists |
| Memoria Press | grade curriculum sets 1–12, Memoria Academy, Highlands Latin School | good |
| CiRCE Institute | site blocked automated reading; titles came from search summaries of CiRCE pages | weakest: check in a browser before relying on a row |

## Files

- `READING-LISTS.tsv`: one row per work: lists it appears on, status, what is held or where to get it, public-domain note, ingest batch.
- `sources/*.tsv`: the raw rows per list, each with the URL it was read from.

Status values: `held` (on some branch), `ingested` (fetched by this work), `partial`, `missing` (PD, not held), `short` (a story or speech whose source is still to find), `lane` (claimed by a relay lane or another thread), `notpd`, `modern`.

Public domain here means US: published 1930 or earlier (as of 2026). UK terms are noted where an author died after 1955. A translation needs its own PD translator; the modern translations several lists assign (Fagles, Fitzgerald, West) are not PD, and the held PD translations stand in for them.

## Batches

Shelves follow the relay convention (`pipeline/<name>_shelf.json`, `fetch_shelf.py <shelf> --verify --record`, `convert_shelf_gutenberg.py <shelf>`); corpus text and built JSON stay gitignored, and nothing is minted. Shelf names are checked against every branch before each batch; where a relay lane already owns an author's shelf, this work uses a distinct name (`hawthorne-rl`, `stephen-crane`, `rwemerson`).

### Batch 1 (2026-10-10): English and American novels

12 shelves, 27 Gutenberg texts, 51,135 units. Every item passed the identity, rights-line and translator checks (`_checks` recorded in each shelf).

| Shelf | Works |
|---|---|
| `austen` | Pride and Prejudice, Sense and Sensibility, Mansfield Park, Northanger Abbey, Persuasion (Emma already held: `austen-emma`) |
| `defoe` | Robinson Crusoe |
| `dickens` | A Tale of Two Cities, Great Expectations, Oliver Twist, David Copperfield, Bleak House, Hard Times |
| `bronte` | Jane Eyre, Wuthering Heights |
| `hawthorne-rl` | The Scarlet Letter |
| `mshelley` | Frankenstein |
| `douglass` | Narrative of the Life of Frederick Douglass |
| `stephen-crane` | The Red Badge of Courage |
| `thoreau` | Walden, with Civil Disobedience |
| `rwemerson` | Essays, First and Second Series |
| `poe` | Works, Raven Edition, vols 1–5 |
| `marlowe` | Doctor Faustus |

Three books needed a chapter rule because their Contents and body headings differ in case: Great Expectations, The Red Badge of Courage, Frankenstein (Letters and Chapters).
