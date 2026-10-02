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

## 2026-10-02 15:27 CDT — overflow-verify-measure: done
- Measured OCR quality of all 30 raw IA volumes (known-word share against the shelves' own clean vocabulary): 94.4%-99.1%; table in the map section.
- Heading check across the 104 converted books: four Lang novels had their "CHAPTER I.--Title" lines missed; `convert_shelf_gutenberg.py` now takes an optional per-book `{"chapre": ...}` in the shelf row, unioned with the Contents rule (backward-compatible). Mark of Cain 3 -> 18 headings, Gold of Fairnilee 4 -> 16, Much Darker Days 4 -> 16, Prince Ricardo 4 -> 13. Lang total now 102,100 units. Three books still mostly under one heading (Nursery Rhyme Book, Aucassin, Custom and Myth new ed.), recorded, not forced.
- Re-searched pending: Tales of a Fairy Court is on neither Gutenberg nor IA. Added Beauty and the Beast (1811, attrib. Lamb; 1887 reprint, intro by Lang) to the Lamb shelf: fetched raw, 55.8 KB. Lamb shelf now 11 items.
- tests/structure_test.py: 64 passed.

## 2026-10-02 15:30 CDT — overflow-boundaries: done
- Found: the house ALL-CAPS heading fallback splits stories and letters at signatures ("C. LAMB"), addressee lines, captions and part numerals; same heading recurs, so unit ids collide (Lucas letters vol. VI had 1,748 `~n` duplicates, vol. VII 1,932).
- `convert_shelf_gutenberg.py` gained two shelf-row options (backward-compatible; structure_texts.py untouched): `{"chapre_only": regex}` and `{"contents_only": true}` (the book's own Contents, read leniently, no caps fallback).
- Lucas letters now cite as `LETTER 263A, par. 4`: 259 and 354 letters, 0 duplicate ids. 30 books moved to own-Contents headings, each adopted only when it lands within 15% of its Contents count with no more duplicates (rule applied mechanically, list in the shelves). Blue/Red/Green Fairy Books = 37/37/42 tales; Tales from Shakespeare = 20 tales + preface.
- Totals now: Lang 102,483 units, Lamb 22,015. tests/structure_test.py 64 passed.
- Not fixed (recorded in the map): Helen of Troy (stanza-numbered verse), Elia volume and Lucas vol. I (Contents don't match body headings), some poetry books (Contents list first lines).

## 2026-10-02 15:32 CDT — session end
- Items: lang, lamb, fables-fold, overflow-verify-measure, overflow-boundaries — all done. Lock released.
- Next Lane D worker: the queue is empty. Do §5 upkeep only: re-check that each shelf identifier still resolves, and keep the map in line with the shelves. Don't invent new authors. Adam decides whether the lane grows (see DIGEST-D.md).
- Local-only by design (gitignored, gone with this container): data/corpus/{lang,lamb}/ and data/books/{lang,lamb}-*.json. `fetch_shelf.py <shelf>` then `convert_shelf_gutenberg.py <shelf>` rebuilds them.

## 2026-10-02 15:46 CDT — macdonald: done
- 61/61 fetched (31 CCEL, 27 Gutenberg, 3 IA raw), 36.5 MB, 0 failed, 0 copyright markers; 102687 units converted. Fantasies, fairy tales, novels, sermons, poetry. CCEL ThML first (Unspoken Sermons carry 67 scripture links in total). 10 Gutenberg books use their own Contents for headings. No uids minted; not in manifest.

## 2026-10-02 15:46 CDT — grimm: done
- 3/3 fetched (0 CCEL, 1 Gutenberg, 2 IA raw), 4.8 MB, 0 failed, 0 copyright markers; 1769 units converted. Margaret Hunt's Household Tales (1884). Gutenberg text cites by tale number (`53 Little Snow-White`): exactly 200 tales + 10 Children's Legends. The 1884 2-vol edition (Lang's introduction, the Grimms' notes) is raw OCR. Taylor/Edwardes and Lucy Crane are pending alternates. No uids minted; not in manifest.

## 2026-10-02 15:46 CDT — andersen: done
- 16/16 fetched (0 CCEL, 9 Gutenberg, 7 IA raw), 14.8 MB, 0 failed, 0 copyright markers; 12713 units converted. Victorian translations side by side, translator in each title: Dulcken, Mary Howitt, Bushby, Fuller, Peachey, Brækstad, Mrs Edgar Lucas, Craigie 1914. PG 27200's translator is unnamed; its wording matches Mrs. H. B. Paull's (unverified). Hersholt excluded (copyright). No uids minted; not in manifest.

## 2026-10-02 15:46 CDT — kingsley: done
- 43/43 fetched (0 CCEL, 43 Gutenberg, 0 IA raw), 19.9 MB, 0 failed, 0 copyright markers; 42788 units converted. All 43 English Gutenberg texts: The Heroes, The Water-Babies, the novels, poems, sermons, lectures. Water-Babies cites by its 8 chapters. No uids minted; not in manifest.

## 2026-10-02 15:46 CDT — hawthorne-wonder: done
- 4/4 fetched (0 CCEL, 4 Gutenberg, 0 IA raw), 1.2 MB, 0 failed, 0 copyright markers; 2887 units converted. Children's books only: A Wonder-Book, Tanglewood Tales, Grandfather's Chair, Biographical Stories. Novels and tales listed pending for Adam. No uids minted; not in manifest.

## 2026-10-02 15:46 CDT — bulfinch: done
- 4/4 fetched (0 CCEL, 4 Gutenberg, 0 IA raw), 2.7 MB, 0 failed, 0 copyright markers; 7772 units converted. Age of Fable, Age of Chivalry and Legends of Charlemagne held as three works, plus Oregon and Eldorado. No uids minted; not in manifest.

## 2026-10-02 15:46 CDT — pyle: done
- 20/20 fetched (0 CCEL, 19 Gutenberg, 1 IA raw), 8.0 MB, 0 failed, 0 copyright markers; 24597 units converted. Robin Hood, the four Arthur books, Pepper & Salt, Wonder Clock, Twilight Land, the novels and pirate tales; Garden Behind the Moon as raw OCR. Illustrator-only books excluded. Arthur books' Book>Part>Chapter nesting is a known citation gap. No uids minted; not in manifest.

## 2026-10-02 15:47 CDT — session end (second run)
- Seven storytellers shelved, converted and committed, one commit each: macdonald, grimm, andersen, kingsley, hawthorne-wonder, bulfinch, pyle. They were added at the coordinator's relay; Adam may veto.
- §5 verification: all 286 shelf URLs across the 9 Lane D shelves resolve (HEAD/range), and every slug appears in the map section. tests/structure_test.py: 64 passed.
- convert_shelf_gutenberg.py: an [Illustration] placeholder is never a heading. Five books rebuilt.
- Known gaps (in the map): Pyle's Arthur books nest Book > Part > Chapter; Helen of Troy needs stanza-aware conversion; Andersen PG 27200's translator is unverified.
- Next Lane D worker: the queue is empty again. Do upkeep only unless Adam adds authors.

## 2026-10-02 15:50 CDT — pyle-nesting: done
- New `pipeline/convert_nested.py`: heading levels outermost-first, each a regex. A heading clears deeper levels, and citations carry the whole path. `title_next` folds a part's name into its number, and `start` forgets headings read from a Contents list. Pyle's four Arthur books now have 0 duplicate unit ids (The Champions of the Round Table alone had 990 `~n` suffixes before; the commit message's "~2,000" was an overstatement). tests 64 passed.

## 2026-10-02 15:59 CDT — carroll: done
- 16/19 fetched (16 Gutenberg), 0 copyright markers; 14,130 units. Alices by chapter; Symbolic Logic and Game of Logic by nested Book > Chapter > Section path via convert_nested.py; Tangled Tale by Knot. Pending: Condensation of Determinants and Curiosa Mathematica I-II (no Gutenberg plain text). No uids minted; not in manifest.

## 2026-10-02 16:00 CDT — kipling: done
- 5/5 fetched (Gutenberg), 0 copyright markers; 6,452 units, 0 duplicate ids. Jungle Book, Second Jungle Book, Just So Stories, Puck of Pook's Hill, Rewards and Fairies. New convert_shelf_gutenberg option repeat_continues for a story title printed twice (over its epigraph and over the story). Other Kipling books pending Adam. No uids minted; not in manifest.

## 2026-10-02 16:05 CDT — stevenson: done
- 45/45 fetched (Gutenberg), 0 copyright markers; 34,834 units. Treasure Island cross-referenced to fetch_sources.py (PG 120), not refetched. New convert_shelf_gutenberg option sub (essay > numbered section). Letters cite recipient + place/date line; plays by play/act/tableau/scene. Swanston Edition pending. No uids minted; not in manifest.

## 2026-10-02 16:08 CDT — chesterton-gaps: done
- 5/5 fetched as raw IA OCR (all title words found; scans dated 1926-1929). Incredulity of Father Brown, Outline of Sanity, Return of Don Quixote, Robert Louis Stevenson, Generally Speaking (the 1929 US printing of a 1928 book). The 61 held works cross-referenced; 1929-1930 books pending. No uids minted; not in manifest.

## 2026-10-02 16:11 CDT — aesop: done
- 2/2 fetched (Gutenberg), 0 copyright markers; 768 units (Townsend 503 in 311 fables+front matter, Jacobs 265 in 82 fables). Found a structure_texts.py Contents bug: _contents_key strips a lowercase roman 'page number' with no separator, eating title endings in c/i/l/v/x (Council -> Coun, Jewel -> Jewe), so those headings are never found. Worked around in convert_shelf_gutenberg's lenient reader only; 9 earlier contents_only books rebuilt (mostly more headings found), map unit counts refreshed. Earlier fables work still unlocated. No uids minted; not in manifest.

## 2026-10-02 16:13 CDT — nesbit: done
- 33/33 fetched (Gutenberg), 0 copyright markers; 48,200 units. Bastable and Psammead books, Railway Children, Arden books, fantasies, dragon and fairy collections, Shakespeare retellings, Royal Children, adult novels, stories, verse. 16 books read chapters from their own Contents. Remaining ~n ids are in publishers' back-matter. No uids minted; not in manifest.

## 2026-10-02 16:14 CDT — potter: done
- 21/21 fetched (Gutenberg), 0 copyright markers; 2,337 units. 20 little books (1902-1922) and The Fairy Caravan (US 1929, by chapter). Gutenberg compilations 572/582 and duplicate transcriptions excluded; later little books not on Gutenberg pending. No uids minted; not in manifest.

## 2026-10-02 16:17 CDT — §5 verification (third run)
- All 413 shelf URLs across the 16 Lane D shelves resolve (one Gutenberg connection reset, 206 on recheck). Every slug appears in the map. tests/structure_test.py 64 passed.
- Measured the structure_texts.py Contents-tail bug: 1,229 Contents titles in 224 of the 382 files under data/corpus/ lose trailing c/i/l/v/x letters. Reported in DIGEST item 2; not fixed in structure_texts.py.
- DIGEST rewritten for the third run: 413 slugs await minting; decision list updated.

## 2026-10-02 16:18 CDT — potter: done
- Gap fill: 2 Internet Archive scans added as raw OCR: Pigling Bland (1913 text, 1987 reprint scan) and Little Pig Robinson (1930, undated Warne printing; US PD since 2026). Appley Dapply not found. 23 slugs.

## 2026-10-02 16:19 CDT — nesbit: gap fill
- Lays and Legends (1886, first series) added as raw Internet Archive OCR (laysandlegends00nesbgoog, 203 KB, 1886 imprint). 34 slugs.

## 2026-10-02 16:19 CDT — session end (third run)
- Relay 3 done, one commit per author: pyle-nesting (convert_nested.py), carroll 16, kipling 5, stevenson 45, chesterton-gaps 5 (raw OCR), aesop 2, nesbit 33 + 1 raw, potter 21 + 2 raw. 130 new slugs; 416 in the lane await minting. No uids minted; manifest untouched; structure_texts.py and fetch_sources.py untouched.
- convert_shelf_gutenberg.py gained the sub and repeat_continues options and a separator-aware lenient Contents reader. The house _contents_key tail bug is measured and reported (DIGEST item 2), not fixed.
- Defects: three Carroll maths works have no plain text; Stevenson Letters 38 ~n ids; Townsend Aesop 10 repeated titles; publishers' back-matter in some Nesbit files; Potter's little books cite by paragraph only.
- Next Lane D worker: the queue is empty. Upkeep only unless Adam adds authors or answers the DIGEST's widen-or-not list (Kipling, Hawthorne, Chesterton 1929-30, Swanston, other Aesops).

## 2026-10-02 16:21 CDT — grahame: done
- 5/5 fetched (Gutenberg), 0 copyright markers; 2,115 units, 0 duplicate ids. Wind in the Willows, Golden Age, Dream Days, Pagan Papers, The Headswoman. No uids minted; not in manifest.

## 2026-10-02 16:24 CDT — barrie: done
- 26/26 fetched (Gutenberg), 0 copyright markers; 29,025 units. Peter Pan novel, 1928 play, Kensington Gardens, Little White Bird, Thrums, Tommy novels, sketches, 11 plays by act. PG 70315 dropped as a duplicate of Echoes of the War. No uids minted; not in manifest.

## 2026-10-02 16:30 CDT — baum: done
- 15/15 fetched (Gutenberg; Little Wizard Stories from 25519 because 19467 has no text file), 0 copyright markers; 18,663 units, 0 duplicate ids. The 14 Oz novels by chapter (Land of Oz: 21 of 24 chapter titles found) + Little Wizard Stories. Other Baum books pending. No uids minted; not in manifest.
