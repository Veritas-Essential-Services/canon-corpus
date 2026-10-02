# Lane A (Divines) — digest
<!-- model: claude-opus-5-5, refreshed 2026-10-02 16:03 CDT -->

Read this first. Detail is in REPORT-A.md; the checklist is docs/divines-map/A-divines.md.

## Held, by author (burn 1, 2026-10-02)

| Author | Shelf | Clean (CCEL/Gutenberg) | Raw IA OCR | Pending | Excluded |
|---|---|---|---|---|---|
| John Flavel | flavel_shelf.json | 5 CCEL (+ Fountain already held) | 6 (Whole Works 1820, complete) | Toronto rescan, earlier editions, Gaelic | modern reprints, 7 same-name people |
| John Bunyan | bunyan_shelf.json | 3 CCEL + 8 Gutenberg incl. Offor's Works 1854 (3 vols) | 0 | Stebbing's Works, 1692/1771 editions, an Offor splitter | Chaplin anthology, paraphrases, Oxford ed. |
| J.C. Ryle | ryle_shelf.json | 3 CCEL + 3 Gutenberg | 37 (Expository Thoughts 6 vols + books and tracts) | Worldly Conformity (no name in OCR) | Thomson's Sabbath, reprints, translations |
| Horatius Bonar (prose) | horatius-bonar_shelf.json | 2 CCEL | 24 | 3 refused scans, How Shall I Go to God, Light and Truth: Revelation | hymns (see hymn manifest), edited works |
| Andrew Bonar | andrew-bonar_shelf.json | 2 Gutenberg | 16 | Visitor's Book of Texts | Andrew Redman Bonar, Bonar Law |
| Adolph Saphir | saphir_shelf.json | 0 (none exists) | 11 | Christ and the Scriptures, Jesus and the Sinner | other Saphirs |
| Jonathan Edwards (gap audit) | edwards_shelf.json | unchanged | +6 first editions/early printings | Distinguishing Marks 1741, Humble Attempt 1747, Freedom of Will 1754 | Yale-only texts |
| Aquinas Summa (census) | none needed | the whole Summa is already held | | | |

126 items fetched this burn (120 for the six authors, 6 Edwards gaps), about 93 MB. None are minted: **every new slug awaits your single-writer uid pass.**

## Round 2: added for your veto (coordinator's default picks)

Adam did not choose these; the coordinator picked them as defaults while you were away. Say the word and any shelf is dropped before merge.

| Author | Shelf | Clean (CCEL/Gutenberg) | Raw IA OCR | Pending | Excluded |
|---|---|---|---|---|---|
| John Owen | owen_shelf.json | 27 CCEL (+4 already held) | 24 (Goold Works 1850-55, complete incl. Hebrews) | none | Banner reprints, modern editions |
| Richard Sibbes | sibbes_shelf.json | 0 (no CCEL or Gutenberg found) | 7 (Grosart Complete Works 1862-64, complete) | a clean Bruised Reed | modern editions; Kater-Sibbes (different author) |

## Defects to look at
- Six 18th-century Edwards printings OCR at 77-83% (long s); quote from Dwight/Worcester instead.
- Bunyan: CCEL "Miscellaneous Pieces" and Gutenberg 3613 are probably the same pieces twice.
- CCEL serves no text for several titles it lists (Bonar: Follow the Lamb, How Shall I Go to God, Winners of Souls; Ryle: The Two Bears). Held from IA where possible.
- Summa: three treatise-opening questions lack a QUESTION heading in the Gutenberg text; the Supplement is not a row in adler_shelf.json.

## Decisions that are yours
- Mint uids for the new slugs.
- Six items the identity check refused because their OCR never names the author (listed under `_pending` in each shelf): shelve them after a look by eye, or leave them out.
- *An Exhortation to Peace and Unity*: doubted Bunyan attribution; keep it on his shelf or not.
- Rutherford editions (Letters, two sermon books) sit on the Andrew Bonar shelf as "ed. Bonar": move them to a Rutherford shelf if you prefer.
- `pipeline/fetch_shelf.py` now refuses wrong-book scans and takes an explicit IA text file name; `pipeline/convert_shelf.py` is new. Both want your review before merge.
