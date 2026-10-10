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

### Batch 2 (2026-10-10): novels and adventure

23 shelves, 43 Gutenberg texts, 75,708 units, all checks passed.

| Shelf | Works |
|---|---|
| `stoker` | Dracula |
| `hardy` | Far from the Madding Crowd |
| `wilkie-collins` | The Woman in White |
| `wilde-novels` | The Picture of Dorian Gray (the fairy tales are Lane D's `wilde-fairy-tales`) |
| `conan-doyle` | A Study in Scarlet, The Sign of the Four, Adventures, Memoirs, The Hound of the Baskervilles, The Return of Sherlock Holmes, The Lost World, The White Company |
| `hgwells` | The Time Machine, The Invisible Man, The War of the Worlds |
| `verne` | Twenty Thousand Leagues under the Sea (the 1872 translation; F. P. Walter's modern one is excluded) |
| `walter-scott` | Ivanhoe, The Talisman |
| `george-eliot` | Silas Marner (Middlemarch already held) |
| `kipling-novels` | Kim, The Man Who Would Be King, Stalky & Co. (children's books are Lane D's `kipling`) |
| `henty` | The Cat of Bubastes, The Dragon and the Raven, Winning His Spurs, By Right of Conquest, In the Reign of Terror, With Lee in Virginia, In the Heart of the Rockies, Redskin and Cow-Boy |
| `orczy` | The Scarlet Pimpernel |
| `john-buchan` | The Thirty-Nine Steps |
| `tennyson` | Idylls of the King |
| `twain-rl` | A Connecticut Yankee, Sketches New and Old (boys' books are the `mark-twain` shelf) |
| `cather` | My Ántonia |
| `tarkington` | Penrod |
| `sabatini` | Scaramouche |
| `terhune` | Lad: A Dog |
| `allen-french` | The Story of Rolf and the Viking's Bow |
| `jane-porter` | The Scottish Chiefs |
| `margery-williams` | The Velveteen Rabbit |
| `dcfisher` | Understood Betsy (US PD; UK until 2029) |

Held back: Conan Doyle's Case-Book (1927) pending a per-story date check.
