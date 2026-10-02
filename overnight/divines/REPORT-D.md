# Lane D (Storytellers) — append-only log

## 2026-10-02 15:25 CDT — lang: done
- Vault (CLAUDE.md's board, _STATUS notes) is not reachable from the cloud; worked from the repo only.
- Baseline `tests/structure_test.py`: 64 passed, 0 failed (before and after).
- Sources: Gutenberg catalogue CSV filtered on "Lang, Andrew"; Internet Archive author search (980 records) for books Gutenberg lacks, each id checked (metadata title, date, djvu text present). CCEL: no Lang.
- Shelf `pipeline/lang_shelf.json`: 95 Gutenberg + 29 IA = 124 items; all fetched (60.5 MB), 0 failed, 0 Gutenberg copyright markers.
- Converted the 95 Gutenberg books with the new `pipeline/convert_shelf_gutenberg.py` (imports structure_texts' convert_gutenberg_prose + contents_chapre, modifies nothing): 102,165 units; every book found at least one heading. Verse books go through the prose path (a unit is a stanza). IA OCR left raw.
- Not registered in data/books/manifest.json and NO uids minted: all 124 `lang-*` slugs await the attended minting pass.
- Excluded with reasons in the shelf: duplicate transcriptions, selections, others' books Lang only edited/introduced (Scott, Dickens, Stevenson, Perrault...), multi-author volumes.
- For Adam: "Mrs. Lang" wrote most of the later story books; they sit on this shelf under Lang's editorship with her credited in the title. Decide whether she gets her own shelf.

## 2026-10-02 15:26 CDT — lamb: done
- Shelf `pipeline/lamb_shelf.json`: E. V. Lucas's Works of Charles and Mary Lamb (1903-05, 7 vols) as the spine — Gutenberg has 6 volumes (its US-issue numbering differs from Methuen's; both recorded), IA `cu31924016657193` supplies vol. IV (Dramatic Specimens and the Garrick Plays), the one Gutenberg lacks (volume identified from the scan's own title page). Tales from Shakespeare, The Adventures of Ulysses and Poetry for Children also held standalone.
- 10/10 fetched (8.4 MB), 0 copyright markers. Converted the 9 Gutenberg items: 21,104 units. Contents of each Lucas volume checked by grepping the fetched text (Rosamund Gray, Hogarth essay in vol. I; Mrs. Leicester's School, Prince Dorus in vol. III; John Woodvil, Mr. H—— in vol. V).
- Mary Lamb credited on Tales from Shakespeare, Poetry for Children, Books for Children and the letters.
- No uids minted; all 10 `lamb-*` slugs await minting. Not in the manifest.
- Pending: clean text of Lucas vol. IV; Ainger's edition as a second witness; Lucas's 1935 Letters (probably still in copyright).

## 2026-10-02 15:27 CDT — fables-fold: done (nothing to fold)
- `git grep -il -E 'fable|aesop|a_?fable'` on the tree, then a word-bounded grep for aesop/fables/phaedrus on every `origin/*` branch: no fables work exists in canon-corpus. Hits were only KJV verses ("cunningly devised fables"), the `fable_review` provenance field, and pipeline/fetch_sources.py's note excluding a Chesterton-introduced Aesop.
- Map section carries `pending: locate earlier fables work` — it may be in a sibling repo (armarium, wordhoard) or the vault, neither reachable from this run. Nothing created, nothing re-ingested, no uids.

## 2026-10-02 15:40 CDT — overflow-verify-measure: done
- Measured OCR quality of all 30 raw IA volumes (known-word share against the shelves' own clean vocabulary): 94.4%-99.1%; table in the map section.
- Heading check across the 104 converted books: four Lang novels had their "CHAPTER I.--Title" lines missed; `convert_shelf_gutenberg.py` now takes an optional per-book `{"chapre": ...}` in the shelf row, unioned with the Contents rule (backward-compatible). Mark of Cain 3 -> 18 headings, Gold of Fairnilee 4 -> 16, Much Darker Days 4 -> 16, Prince Ricardo 4 -> 13. Lang total now 102,100 units. Three books still mostly under one heading (Nursery Rhyme Book, Aucassin, Custom and Myth new ed.), recorded, not forced.
- Re-searched pending: Tales of a Fairy Court is on neither Gutenberg nor IA. Added Beauty and the Beast (1811, attrib. Lamb; 1887 reprint, intro by Lang) to the Lamb shelf: fetched raw, 55.8 KB. Lamb shelf now 11 items.
- tests/structure_test.py: 64 passed.
