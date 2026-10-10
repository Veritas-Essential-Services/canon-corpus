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

## 2026-10-02 16:31 CDT — ruskin-golden-river: done
- 1/1 fetched (Gutenberg 33673, Ginn 1885 with Doyle's pictures), 0 copyright markers; 248 units by chapter, 0 duplicate ids. No uids minted; not in manifest.

## 2026-10-02 16:32 CDT — wilde-fairy-tales: done
- 2/2 fetched (Gutenberg), 0 copyright markers; 1,006 units, all 9 tales found as headings, 0 duplicate ids. No uids minted; not in manifest.

## 2026-10-02 16:33 CDT — dickens-christmas: done
- 5/5 fetched (Gutenberg), 0 copyright markers; 3,689 units, 0 duplicate ids; each book cited by its own staves, quarters, chirps, parts or Gifts. No uids minted; not in manifest.

## 2026-10-02 16:34 CDT — collodi: done
- 2/2 fetched: Della Chiesa 1914 (Gutenberg 500; 1,757 units, 36 chapters) and Murray 1892 (IA raw OCR, translator confirmed on the title page). PG 16865 held back: no translator named. No uids minted; not in manifest.

## 2026-10-02 16:35 CDT — lofting: done
- 7/7 fetched (6 Gutenberg, 1 IA raw: Caravan 1926 first printing); 5,086 units, 0 duplicate ids. Circus, Zoo, Garden pending (only later printings with new front matter found). No uids minted; not in manifest.

## 2026-10-02 16:40 CDT — session end (fourth run)
- Relay 4 done, one commit per author: grahame 5, barrie 26, baum 15, ruskin-golden-river 1, wilde-fairy-tales 2, dickens-christmas 5, collodi 2 (1 raw), lofting 7 (1 raw). 63 new slugs; 479 in the lane await minting. 0 Gutenberg copyright markers. No uids minted; manifest, structure_texts.py and fetch_sources.py untouched.
- §5: all 479 shelf URLs across 24 shelves resolve (4 transient failures, all 206 on recheck). Every slug is in the map. tests/structure_test.py 64 passed.
- Side job for the upkeep thread, at the coordinator's request: in a scratch worktree, removed afterwards with nothing committed, ran contents_key_diff.py on the 36 CHESTERTON_GUTENBERG books. Result: 0 ids change. Sent to that session.
- Held back: Pinocchio PG 16865 (no translator named); Lofting's Circus, Zoo and Garden (later printings only). Baum's non-Oz books are pending Adam.
- Next Lane D worker: queue empty; upkeep only.

## 2026-10-02 16:48 CDT — jacobs-fairy: done
- 6/6 fetched (Gutenberg 7439, 14241, 7885, 34453, 7128, 26019), 8,226 units, 0 duplicate ids. English Fairy Tales by a Contents title list (43 tales) with repeat_continues (the JACK THE GIANT-KILLER display line); More English by its own Contents. 35862 held back as a probable retitling of Celtic Fairy Tales.

## 2026-10-02 16:48 CDT — dasent: done
- 2/2 fetched (Gutenberg 8933, 36385), 5,716 units; translator Dasent captured from both headers. Fjeld: 14 ids carry ~2 (two different tales titled The Haunted Mill; The Companion headed over frame and tale).

## 2026-10-02 16:48 CDT — ralston: done
- 1/1 fetched (Gutenberg 22373), 3,465 units, nested Chapter > tale, all 51 tales found. convert_nested.py gains two opt-in level keys: strip (a footnote mark on a title) and max (a title longer than 90 characters, used by Colum). 10 ~2 ids from Contents summaries.

## 2026-10-02 16:49 CDT — perrault: done
- 3/3 fetched (Gutenberg 17208, 29021, 31431), 1,894 units, 0 duplicate ids; translators Welsh, Mansion, Johnson captured from the headers. Samber/Mansion via contents_only (all 10 tales; the house rule missed Puss in Boots and Cinderilla). PG 33511 pending (no translator named); PG 33931 is French.

## 2026-10-02 16:49 CDT — colum: done
- 7/7 fetched (Gutenberg 3495, 16867, 24493, 53252, 24737, 37881, 69724), 6,414 units, 2 ~2 ids (Odysseus front matter). King of Ireland's Son, Odysseus, Gateways nested; Golden Fleece by its own Contents. 2395 left out as the older transcription of 37881.

## 2026-10-02 16:57 CDT — audit-5: done
- §5 lane-wide audit, written up in `AUDIT-D.md` and summarised in DIGEST-D. 497 URLs over 29 shelves resolve (4 transient failures answered on retry); every slug is in the map. No source id is held twice in the repo. About a dozen books are reprinted inside another Lane D volume (text-measured). The IA Hunt Grimm (1884) duplicates the PG Hunt. Raw OCR: 43 A, 11 B. `macdonald-for-the-right` was removed: Franzos's novel, tr. Julie Sutter, MacDonald's preface only. Five Andersen rows name no translator; listed for Adam.

## 2026-10-02 16:57 CDT — session end (fifth run)
- Relay 5 done. Spot-check of the Chesterton zero sent to the upkeep thread; DIGEST item 2 corrected (99 truncated headings, 68 missed, not 1,229). Five folk-tale shelves added: jacobs-fairy (6), dasent (2), ralston (1), perrault (3), colum (7), 25,715 units. convert_nested.py gained opt-in per-level `strip` and `max`. Lock released. Queue: 34/34 done.

## 2026-10-02 17:08 CDT — malory: done
- 3/3 fetched (Gutenberg 1251, 1252, 46853), 4,737 units. Nested Book > Chapter; convert_nested.py gains opt-in level label/keep and a front option (front matter before 'start' is not read for headings); ralston and colum-adventures-of-odysseus now use front (Ralston's 10 Contents ~2 ids gone).

## 2026-10-02 17:09 CDT — beowulf: done
- 4/4 fetched (Gutenberg 16328, 20431, 50742, 981), 2,181 units, 1 ~2 id; translators Hall, Morris, Kirtlan, Gummere captured from the headers.

## 2026-10-02 17:09 CDT — poetic-edda: done
- 1/1 fetched (Gutenberg 73533), 4,703 units, nested Poem > note/text/notes; 14 ~2 ids in Brot af Sigurtharkvithu (its NOTES heading is run into prose in the source).

## 2026-10-02 17:09 CDT — kalevala: done
- 1/1 fetched (Gutenberg 5186), 1,534 units, 0 ~2 ids; cut by rune; translator Crawford captured from the header.

## 2026-10-02 17:09 CDT — sagas: done
- Sagas: dasent shelf gains Burnt Njal (Gutenberg 17919, 4,096 units, 0 ~2, by chapter) and Gisli the Outlaw (IA storygislioutla00dasegoog, raw OCR, grade A). PG 597 left out as the older transcription; the Orkneyingers' Saga (1894) not found as a usable scan. Sturluson on its own shelf (next commit).

## 2026-10-02 17:09 CDT — sturluson: done
- 2/2 fetched (Gutenberg 598, 18947), 3,554 units. Heimskringla nested Saga > chapter (all 16 sagas, 0 ~2); translator unnamed in the file, identified as Laing rev. Anderson (1889) by collation with IA heimskringlaorsa01snor and the --L./--Ed. note signatures. Younger Edda tr. Anderson, 3 ~2 ids.

## 2026-10-02 17:09 CDT — dutt: done
- 2/2 fetched (Gutenberg 19630; IA RamayanaTheEpicOfRama..., file Ramayana_the_epic_of_Rama_prince_of_Indi_djvu.txt), 2,072 units, 0 ~2 ids; Mahabharata nested Book > canto; Ramayana raw OCR grade B (96.8% word hit).

## 2026-10-02 17:13 CDT — mabinogion: done
- Guest's Mabinogion is already held by lane C (`pipeline/guest_shelf.json`, PG 5160). Cross-referenced only; no second shelf.

## 2026-10-02 17:13 CDT — session end (sixth run)
- Relay 6 done. Six new shelves and the Dasent shelf extended: malory (3), beowulf (4), poetic-edda (1), kalevala (1), sturluson (2), dutt (1 + 1 raw), dasent (+1, +1 raw). 22,877 new units. convert_nested.py gains opt-in level `label`/`keep` and a `front` option; ralston and colum Odysseus now use front. All 512 Lane D URLs resolve (5 transient failures answered on retry); map complete. Lock released. Queue: 42/42 done.

## 2026-10-02 17:19 CDT — yeats-folk: done
- 3/3 fetched (Gutenberg 33887, 31763, 10459), 2,829 units, 2 ~2 ids. Batch 7 (world folk tales), chosen by Lane D under the coordinator's standing relay.

## 2026-10-02 17:19 CDT — hyde: done
- 2/2 fetched (Gutenberg 45910; IA besidefirecollec00hyde), 1,803 units, 0 ~2 ids; Beside the Fire raw OCR, grade C from its facing Irish text.

## 2026-10-02 17:19 CDT — gregory: done
- 5/5 fetched (Gutenberg 14465, 76322, 43973, 43974; IA cuchulainofmuirt00greg_0), 4,694 units, 11 ~2 ids (Visions and Beliefs).

## 2026-10-02 17:19 CDT — campbell-highlands: done
- 4/4 fetched (IA populartalesofwe01campuoft, populartalesofw02campuoft, populartalesofwe03campuoft, populartalesofwe40camp), raw OCR; grades C, D, C, A, the low ones from facing Gaelic (spot-checked).

## 2026-10-02 17:20 CDT — ozaki: done
- 3/3 fetched (Gutenberg 4018, 41437, 45933), 3,587 units, 11 ~2 ids.

## 2026-10-02 17:20 CDT — mitford: done
- 1/1 fetched (Gutenberg 13015), 1,630 units, 7 ~2 ids; contents_only.

## 2026-10-02 17:20 CDT — steel: done
- 2/2 fetched (Gutenberg 6145, 17034), 3,888 units; Punjab nested (0 ~2), English Fairy Tales 24 ~2 from captions.

## 2026-10-02 17:20 CDT — crane: done
- 1/1 fetched (Gutenberg 23634), 1,963 units, 0 ~2 ids; nested chapter > tale, notes apart.

## 2026-10-02 17:20 CDT — grinnell: done
- 4/4 fetched (Gutenberg 36923, 11547, 66596, 13833), 3,491 units, 6 ~2 ids.

## 2026-10-02 17:20 CDT — harris-remus: done
- 4/4 fetched (Gutenberg 2306, 26429, 55676, 22282), 5,087 units, 21 ~2 ids. Content flagged for Adam in DIGEST.

## 2026-10-02 17:29 CDT — burnett: done
- 7/7 fetched (Gutenberg 113, 146, 137, 479, 384, 8574, 10466), 8,539 units, 0 ~2 ids.

## 2026-10-02 17:29 CDT — alcott: done
- 9/9 fetched (Gutenberg 514, 2788, 3499, 2726, 2804, 2787, 3795, 2786, 163), 17,897 units, 0 ~2 ids.

## 2026-10-02 17:29 CDT — spyri: done
- 4/4 fetched (Gutenberg 1448, 20781, 9383, 9075), 4,227 units, 0 ~2 ids.

## 2026-10-02 17:29 CDT — sewell: done
- 1/1 fetched (Gutenberg 271), 925 units, 0 ~2 ids.

## 2026-10-02 17:29 CDT — dodge: done
- 1/1 fetched (Gutenberg 764), 2,093 units, 0 ~2 ids.

## 2026-10-02 17:29 CDT — montgomery: done
- 13/13 fetched (Gutenberg 45, 47, 51, 544, 5343, 3796, 1354, 5340, 5342, 316, 5341, 61236, 67979), 21,864 units, 1 ~2 ids.

## 2026-10-02 17:29 CDT — wiggin: done
- 6/6 fetched (Gutenberg 498, 1375, 721, 10540, 18531, 15630), 5,387 units, 6 ~2 ids.

## 2026-10-02 17:29 CDT — ewing: done
- 7/7 fetched (Gutenberg 7865, 15592, 62783, 5601, 17772, 19360, 19859), 8,842 units, 6 ~2 ids.

## 2026-10-02 17:29 CDT — molesworth: done
- 8/8 fetched (Gutenberg 15569, 17175, 33544, 39375, 29380, 39748, 43127, 6676), 8,042 units, 0 ~2 ids.

## 2026-10-02 17:29 CDT — wyss: done
- 1/1 fetched (Gutenberg 41659), 2,544 units, 0 ~2 ids.

## 2026-10-02 19:42 CDT — church: done
- 9/9 fetched (Gutenberg 74231, 6370, 40622, 14994, 24030, 43982, 78980, 55765, 75339), 5,770 units, 214 ~2 ids.

## 2026-10-02 19:42 CDT — guerber: done
- 7/7 fetched (Gutenberg 39250, 73021, 28497, 12455, 13983, 64163, 16840), 13,366 units, 0 ~2 ids.

## 2026-10-02 19:42 CDT — peabody: done
- 1/1 fetched (Gutenberg 9313), 436 units, 0 ~2 ids.

## 2026-10-02 19:42 CDT — golden-legend: done
- 7/7 Internet Archive volumes fetched as raw OCR; not converted (the Edwards precedent).

## 2026-10-02 19:42 CDT — canton: done
- 1/1 fetched (Gutenberg 22112), 934 units, 0 ~2 ids.

## 2026-10-02 19:42 CDT — abbie-brown: done
- 1/1 fetched (Gutenberg 28990), 656 units, 0 ~2 ids.

## 2026-10-02 19:42 CDT — steedman: done
- 1/1 fetched (Gutenberg 36674), 732 units, 0 ~2 ids.

## 2026-10-02 19:49 CDT — edda-widen: done
- 3/3 fetched (Gutenberg 73533, 14726, 1152), 9,018 units, 20 ~2 ids.

## 2026-10-02 19:49 CDT — kalevala-kirby: done
- 3/3 fetched (Gutenberg 5186, 25953, 33089), 4,722 units, 1 ~2 ids.

## 2026-10-02 19:50 CDT — yeats-stories: done
- 5/5 fetched (Gutenberg 33887, 31763, 10459, 5793, 5795), 3,129 units, 3 ~2 ids.

## 2026-10-02 19:50 CDT — grace-james: done
- 1/1 fetched (Gutenberg 35853), 1,870 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — griffis: done
- 1/1 fetched (Gutenberg 29337), 741 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — dayrell: done
- 2/2 fetched (Gutenberg 34655, 70959), 1,287 units, 1 ~2 ids.

## 2026-10-02 19:50 CDT — cronise-ward: done
- 1/1 fetched (Gutenberg 48828), 1,366 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — bleek: done
- 1/1 fetched (Gutenberg 73413), 420 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — fillmore: done
- 2/2 fetched (Gutenberg 32217, 33002), 2,996 units, 14 ~2 ids.

## 2026-10-02 19:50 CDT — mijatovich: done
- 1/1 fetched (Gutenberg 45321), 963 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — petrovitch: done
- 1/1 fetched (Gutenberg 38571), 2,057 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — frere: done
- 1/1 fetched (Gutenberg 36696), 1,120 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — lal-behari-day: done
- 1/1 fetched (Gutenberg 38488), 387 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — crooke-rouse: done
- 1/1 fetched (Gutenberg 30635), 1,395 units, 9 ~2 ids.

## 2026-10-02 19:50 CDT — natesa-sastri: done
- 1/1 fetched (Gutenberg 37002), 950 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — bain: done
- 2/2 fetched (Gutenberg 29672, 64807), 1,335 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — giles-liaozhai: done
- 1/1 fetched (Gutenberg 43629), 1,894 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — zitkala-sa: done
- 1/1 fetched (Gutenberg 338), 439 units, 0 ~2 ids.

## 2026-10-02 19:50 CDT — eastman: done
- 1/1 fetched (Gutenberg 28099), 600 units, 1 ~2 ids.

## 2026-10-02 19:50 CDT — busk: done
- 1/1 fetched (Gutenberg 45859), 1,411 units, 3 ~2 ids.

## 2026-10-02 19:50 CDT — webster-basque: done
- 1/1 fetched (Gutenberg 34902), 2,404 units, 23 ~2 ids.

## 2026-10-02 20:07 CDT — milne: done
- 5/5 fetched (Gutenberg 67098, 73011, 70271, 70516, 27771), 4,958 units, 2 ~2 ids.

## 2026-10-02 20:07 CDT — craik: done
- 3/3 fetched (Gutenberg 496, 30494, 19734), 3,272 units, 19 ~2 ids.

## 2026-10-02 20:07 CDT — ingelow: done
- 2/2 fetched (Gutenberg 32867, 21014), 1,639 units, 0 ~2 ids.

## 2026-10-02 20:07 CDT — stockton: done
- 3/3 fetched (Gutenberg 12067, 20836, 71032), 2,204 units, 1 ~2 ids.

## 2026-10-02 20:07 CDT — burgess: done
- 26/26 fetched (Gutenberg 2557, 20877, 39706, 14958, 21286, 46988, 17250, 1825, 5844, 46866, 14732, 11915, 5110, 25301, 14375, 37952, 43596, 22816, 12630, 15521, 46952, 19092, 5846, 46951, 21015, 46950), 9,353 units, 22 ~2 ids.

## 2026-10-02 20:07 CDT — lagerlof: done
- 2/2 fetched (Gutenberg 10935, 44818), 4,385 units, 0 ~2 ids.

## 2026-10-02 20:07 CDT — laboulaye: done
- 1/1 fetched (Gutenberg 26386), 1,111 units, 0 ~2 ids.

## 2026-10-02 20:08 CDT — hauff: done
- 2/2 fetched (Gutenberg 32109, 74947), 3,126 units, 0 ~2 ids.

## 2026-10-02 20:08 CDT — gatty: done
- 2/2 fetched (Gutenberg 5074, 11319), 1,626 units, 0 ~2 ids.

## 2026-10-02 20:08 CDT — edgeworth: done
- 1/1 fetched (Gutenberg 3655), 3,828 units, 0 ~2 ids.

## 2026-10-02 20:10 CDT — baldwin: done
- 6/6 fetched (Gutenberg 6866, 11582, 15616, 18442, 54214, 66819), 6,263 units, 0 ~2 ids.

## 2026-10-02 20:10 CDT — macgregor: done
- 3/3 fetched (Gutenberg 25654, 26181, 22175), 1,791 units, 8 ~2 ids.

## 2026-10-02 20:10 CDT — gilbert: done
- 1/1 fetched (Gutenberg 22396), 2,573 units, 1 ~2 ids.

## 2026-10-02 20:10 CDT — knowles: done
- 1/1 fetched (Gutenberg 12753), 1,702 units, 14 ~2 ids.

## 2026-10-02 20:10 CDT — rolleston: done
- 2/2 fetched (Gutenberg 14749, 34081), 3,450 units, 0 ~2 ids.

## 2026-10-02 20:10 CDT — hull: done
- 2/2 fetched (Gutenberg 52963, 69131), 1,859 units, 1 ~2 ids.

## 2026-10-02 20:10 CDT — weston: done
- 6/6 fetched (Gutenberg 47297, 47298, 8447, 45514, 66084, 46234), 3,143 units, 12 ~2 ids.

## 2026-10-02 20:29 CDT — de-morgan: done
- 2/2 fetched (Gutenberg 38976, 69875), 1,457 units, 0 ~2 ids.

## 2026-10-02 20:29 CDT — frances-browne: done
- 1/1 fetched (Gutenberg 26018), 421 units, 0 ~2 ids.

## 2026-10-02 20:29 CDT — stroebe: done
- 2/2 fetched (Gutenberg 37193, 38070), 1,515 units, 0 ~2 ids.

## 2026-10-02 20:30 CDT — perkins: done
- 13/13 fetched (Gutenberg 3496, 3497, 3642, 3774, 4012, 4086, 4091, 9966, 16644, 28425, 28426, 28431, 28889), 7,280 units, 0 ~2 ids.

## 2026-10-02 20:30 CDT — richards: done
- 9/9 fetched (Gutenberg 7790, 7824, 19892, 43336, 49748, 49751, 35281, 41603, 49724), 6,182 units, 13 ~2 ids.

## 2026-10-02 20:30 CDT — yonge: done
- 6/6 fetched (Gutenberg 3048, 3696, 4364, 5313, 6489, 4538), 5,064 units, 0 ~2 ids.

## 2026-10-02 20:34 CDT — lady-wilde: done
- 1/1 fetched (Gutenberg 61436), 2,552 units, 19 ~2 ids.

## 2026-10-02 20:34 CDT — croker: done
- 1/1 fetched (Gutenberg 39752), 1,213 units, 1 ~2 ids.

## 2026-10-02 20:34 CDT — keightley: done
- 1/1 fetched (Gutenberg 41006), 3,358 units, 8 ~2 ids.

## 2026-10-02 20:34 CDT — morrison: done
- 1/1 fetched (Gutenberg 51762), 686 units, 0 ~2 ids.

## 2026-10-02 20:34 CDT — robert-hunt: done
- 1/1 fetched (Gutenberg 59033), 1,907 units, 3 ~2 ids.

## 2026-10-02 20:34 CDT — baring-gould: done
- 5/5 fetched (Gutenberg 36127, 5324, 36638, 48736, 48622), 9,511 units, 0 ~2 ids.

## 2026-10-02 20:41 CDT — incident: Lane A's perkins shelf overwritten, restored
- f582443 (Lucy Fitch Perkins) wrote over `pipeline/perkins_shelf.json`, Lane A's William Perkins shelf. The new-shelf helper did not check for an existing file. The coordinator relayed the reviewer's catch.
- 8c69ae2 restores the file byte for byte from 2acacb0 and moves the Twins books to `pipeline/lfperkins_shelf.json` (slugs `lfperkins-*`).
- Guard: `overnight/divines/precommit-D.py` (installed as the clone's pre-commit hook) refuses a commit that changes a shelf with another lane's commit in its history; the helper refuses an existing file.
- 88bc65a: `_surname`, `_translators` and recorded `_checks` on 63 shelves (the subject says 64, wrongly). 0 mismatches, 0 rights flags.

## 2026-10-02 20:49 CDT — leland: done
- 4/4 fetched (Gutenberg 6803, 32786, 62335, 78673), 5,603 units, 4 ~2 ids.

## 2026-10-02 20:49 CDT — schoolcraft: done
- 4/4 fetched (Gutenberg 21620, 35152, 35175, 48469), 3,584 units, 2 ~2 ids.

## 2026-10-02 20:49 CDT — cushing: done
- 2/2 fetched (Gutenberg 54682, 48342), 2,973 units, 9 ~2 ids.

## 2026-10-02 20:49 CDT — mooney: done
- 1/1 fetched (Gutenberg 45634), 3,565 units, 3 ~2 ids.

## 2026-10-02 20:49 CDT — judson: done
- 5/5 fetched (Gutenberg 2503, 22083, 44935, 47146, 48409), 4,593 units, 63 ~2 ids.

## 2026-10-02 20:49 CDT — nassau: done
- 1/1 fetched (Gutenberg 58900), 1,528 units, 0 ~2 ids.

## 2026-10-02 21:03 CDT — coolidge: done
- 9/9 fetched (Gutenberg 8994, 5141, 8995, 15798, 28724, 27678, 27223, 35186, 58762), 8,508 units, 10 ~2 ids.

## 2026-10-02 21:04 CDT — lucretia-hale: done
- 2/2 fetched (Gutenberg 3028, 15546), 2,135 units, 1 ~2 ids.

## 2026-10-02 21:04 CDT — margaret-sidney: done
- 12/12 fetched (Gutenberg 2770, 5632, 6418, 6987, 7498, 26122, 71128, 7434, 35178, 71146, 71215, 49471), 31,901 units, 61 ~2 ids.

## 2026-10-02 21:04 CDT — eleanor-porter: done
- 3/3 fetched (Gutenberg 1450, 6100, 440), 5,849 units, 0 ~2 ids.

## 2026-10-02 21:04 CDT — jean-webster: done
- 4/4 fetched (Gutenberg 157, 238, 21048, 21639), 5,620 units, 0 ~2 ids.

## 2026-10-02 21:04 CDT — gruelle: done
- 5/5 fetched (Gutenberg 18190, 17371, 11315, 62440, 78535), 3,792 units, 0 ~2 ids.

## 2026-10-02 21:04 CDT — albert-paine: done
- 5/5 fetched (Gutenberg 24410, 28192, 28193, 28204, 28302), 2,074 units, 4 ~2 ids.

## 2026-10-02 21:04 CDT — de-vere: done
- 3/3 fetched (Gutenberg 7165, 29121, 78491), 2,151 units, 29 ~2 ids.

## 2026-10-02 21:10 CDT — westervelt: done
- 5/5 fetched (Gutenberg 32601, 39195, 66516, 66547, 66357), 4,502 units, 0 ~2 ids.

## 2026-10-02 21:10 CDT — fansler: done
- 1/1 fetched (Gutenberg 8299), 3,379 units, 87 ~2 ids.

## 2026-10-02 21:10 CDT — kremnitz: done
- 1/1 fetched (Gutenberg 20552), 1,443 units, 0 ~2 ids.

## 2026-10-02 21:10 CDT — eells: done
- 3/3 fetched (Gutenberg 24714, 21678, 34431), 2,257 units, 0 ~2 ids.

## 2026-10-02 21:10 CDT — rasmussen: done
- 1/1 fetched (Gutenberg 28932), 1,435 units, 0 ~2 ids.

## 2026-10-02 21:10 CDT — horace-allen: done
- 1/1 fetched (Gutenberg 55539), 416 units, 0 ~2 ids.

## 2026-10-02 21:10 CDT — berens: done
- 1/1 fetched (Gutenberg 22381), 1,428 units, 0 ~2 ids.

## 2026-10-02 21:10 CDT — sara-bryant: done
- 2/2 fetched (Gutenberg 474, 16693), 2,398 units, 6 ~2 ids.

## 2026-10-02 21:23 CDT — garis: done
- 35/35 fetched (Gutenberg 5262, 5900, 11156, 13087, 15280, 15281, 15282, 17807, 18599, 32334, 42574, 54995, 60017, 61082, 67990, 69458, 70295, 71213, 73603, 75192, 75474, 50405, 56950, 61671, 61695, 61735, 70017, 70627, 70783, 71185, 71515, 71594, 72607, 72612, 72746), 26,226 units, 14 ~2 ids.

## 2026-10-02 21:23 CDT — keary: done
- 1/1 fetched (Gutenberg 41283), 1,075 units, 0 ~2 ids.

## 2026-10-02 21:23 CDT — jean-lang: done
- 4/4 fetched (Gutenberg 22693, 68127, 41350, 14416), 4,017 units, 0 ~2 ids.

## 2026-10-02 21:23 CDT — francillon: done
- 1/1 fetched (Gutenberg 45416), 1,159 units, 0 ~2 ids.

## 2026-10-02 21:23 CDT — ouida: done
- 3/3 fetched (Gutenberg 5834, 75655, 50032), 2,223 units, 0 ~2 ids.

## 2026-10-02 21:23 CDT — stratton-porter: done
- 11/11 fetched (Gutenberg 111, 125, 286, 349, 532, 533, 9489, 3722, 904, 59823, 35188), 23,021 units, 1 ~2 ids.

## 2026-10-02 21:24 CDT — note
- The Garis commit (3088b95) says "34 books in all"; the shelf holds 35. The DIGEST row says 35.

## 2026-10-02 21:37 CDT — basile: done
- 1/1 fetched (Gutenberg 2198), 683 units, 0 ~2 ids.

## 2026-10-02 21:37 CDT — straparola: done
- 1/1 fetched (Gutenberg 75257), 795 units, 0 ~2 ids.

## 2026-10-02 21:37 CDT — gesta-romanorum: done
- 1/1 fetched (Gutenberg 58655), 1,470 units, 0 ~2 ids.

## 2026-10-02 21:37 CDT — babbitt: done
- 2/2 fetched (Gutenberg 62514, 7518), 893 units, 0 ~2 ids.

## 2026-10-02 21:37 CDT — abby-diaz: done
- 4/4 fetched (Gutenberg 69482, 68833, 70939, 34335), 4,396 units, 0 ~2 ids.

## 2026-10-02 21:37 CDT — beatrice-clay: done
- 1/1 fetched (Gutenberg 15551), 309 units, 0 ~2 ids.

## 2026-10-02 21:37 CDT — poulsson: done
- 1/1 fetched (Gutenberg 36465), 797 units, 0 ~2 ids.

## 2026-10-02 21:37 CDT — thorne-thomsen: done
- 1/1 fetched (Gutenberg 49201), 324 units, 0 ~2 ids.

## 2026-10-02 21:47 CDT — convert_nested fix (coordinator relay)
- `convert_nested.py`: a body start now also forgets a title the Contents' last heading was waiting for. Before, a book whose Contents ended on a title_next heading cited its first body heading as "None BOOK ONE". New test `tests/convert_nested_test.py` (11 checks) fails on the old code and passes on the new. Rebuilt all 85 Lane D books that use the nested converter in memory: no unit id or ref changes, so no Lane D book carried the bug.
- `split_shelf_titles.py` (stale titles file after a failed split) is Lane C's file; not touched here.

## 2026-10-02 21:55 CDT — skinner: done
- 2/2 fetched (Gutenberg 6615, 24732), 1,810 units, 0 ~2 ids.

## 2026-10-02 21:55 CDT — wilhelm: done
- 1/1 fetched (Gutenberg 29939), 1,526 units, 0 ~2 ids.

## 2026-10-02 21:56 CDT — gale-korean: done
- 1/1 fetched (Gutenberg 51002), 776 units, 0 ~2 ids.

## 2026-10-02 21:57 CDT — bompas: done
- 1/1 fetched (Gutenberg 11938), 1,409 units, 1 ~2 ids.

## 2026-10-02 21:58 CDT — barker-sinclair: done
- 1/1 fetched (Gutenberg 66923), 425 units, 0 ~2 ids.

## 2026-10-02 21:58 CDT — rafy: done
- 1/1 fetched (Gutenberg 37884), 505 units, 0 ~2 ids.

## 2026-10-02 21:59 CDT — glinski: done
- 1/1 fetched (Gutenberg 36668), 635 units, 0 ~2 ids.

## 2026-10-02 22:00 CDT — baudis: done
- 1/1 fetched (Gutenberg 52596), 796 units, 0 ~2 ids.

## 2026-10-02 22:01 CDT — wardrop: done
- 1/1 fetched (Gutenberg 44536), 773 units, 0 ~2 ids.

## 2026-10-02 22:16 CDT — jones-kropf: done
- 1/1 fetched (Gutenberg 42981), 3,152 units, 0 ~2 ids.

## 2026-10-02 22:17 CDT — emerson: done
- 1/1 fetched (Gutenberg 8675), 490 units, 0 ~2 ids.

## 2026-10-02 22:18 CDT — thrum: done
- 1/1 fetched (Gutenberg 18450), 1,216 units, 0 ~2 ids.

## 2026-10-02 22:18 CDT — sellers: done
- 1/1 fetched (Gutenberg 31481), 867 units, 0 ~2 ids.

## 2026-10-02 22:19 CDT — grierson: done
- 1/1 fetched (Gutenberg 37532), 1,661 units, 0 ~2 ids.

## 2026-10-03 00:41 CDT — angus-hall: done
- 1/1 fetched (Gutenberg 67085), 1,386 units, 0 ~2 ids.

## 2026-10-03 00:42 CDT — oconnor: done
- 1/1 fetched (Gutenberg 75000), 827 units, 0 ~2 ids.

## 2026-10-03 00:42 CDT — russell: done
- 1/1 fetched (Gutenberg 75089), 471 units, 0 ~2 ids.

## 2026-10-03 00:43 CDT — jameson: done
- 2/2 fetched (Gutenberg 69581, 12047), 3,486 units, 0 ~2 ids.

## 2026-10-03 00:44 CDT — griffis-b21: done
- 5/5 fetched (Gutenberg 7871, 9368, 69739, 67180, 67256), 4,342 units, 0 ~2 ids.

## 2026-10-03 00:45 CDT — ralston-tibetan: done
- 1/1 fetched (Gutenberg 66870), 1,848 units, 0 ~2 ids.

## 2026-10-03 00:58 CDT — review round 6 and Lane A's surname gate (e1ef08b)
- 31 Lane D shelves now name their author in full in `_surname` (e.g. "andrew lang", "beatrice e. clay", "james scarth gale", "charles m. skinner", "w. h. barker", "mrs. a. w. hall"), replacing bare words that occur in most English books. Each form was matched against every book on its shelf before the change, then `fetch_shelf --verify --record` re-run on all 31: 0 mismatches, 0 rights flags. All 163 Lane D shelves pass the new load-time check.
- The change exposed one wrong attribution: `lang-devil-dancers` is a Christian Literature Society for India pamphlet "compiled from Lang, Caldwell, Conway, Tylor ... and others". Moved to `_held` on the lang shelf (DIGEST decision 16).
- basile: the translator note no longer quotes the book's text. andersen: punctuation in three translator notes.
- Grierson and Skinner: undated in the text; the Internet Archive catalogue dates are now recorded with the record ids. Grierson's life dates, which came from memory and not from the text or a record, were removed.
- DIGEST: the minting list is now counted from the shelf files (926 slugs on 163 shelves) instead of hand-summed by batch; the headline says 161 storytellers and lists batch 21.

## 2026-10-03 01:18 CDT — review round 7 and Lane A's CCEL print-source check (36ca012)
- jean-lang: `_surname` is now "jean lang" (it was bare "lang", which Andrew Lang's books also pass); re-recorded, 4/4 seen.
- basile: the translator note describes the 1911 printing's prefatory note instead of quoting it.
- macdonald (Lane D's only CCEL shelf, 31 CCEL items): re-recorded under 36ca012. 23 have a print source on CCEL's page, 8 have none. Correction to the first version of this line, which said none was 1930 or later: four are, and fetch_shelf flags them `ccel_print_source_check`: The Miracles of Our Lord (J. J. Flynn, c1987), The Vicar's Daughter (Sunrise Books, 2001), Salted with Fire (Sunrise Books, 1989) and The Princess and Curdie (D. McKay [1934]). All four are reprints of MacDonald's own nineteenth-century texts, not critical editions, so they stay on the shelf; whether a modern reprint added anything is not known from the record, and republishing waits on a look (DIGEST decision 17).

## 2026-10-03 01:52 CDT — abbie-brown-b22: done
- 2/2 fetched (Gutenberg 44622, 16140), 1,488 units, 0 ~2 ids.

## 2026-10-03 01:53 CDT — katharine-pyle: done
- 7/7 fetched (Gutenberg 3230, 48593, 47178, 49001, 25913, 48351, 66919), 8,810 units, 0 ~2 ids.

## 2026-10-03 01:54 CDT — spence: done
- 8/8 fetched (Gutenberg 56550, 53080, 42390, 16539, 43662, 45137, 38530, 30871), 11,920 units, 0 ~2 ids.

## 2026-10-03 01:55 CDT — hearn: done
- 6/6 fetched (Gutenberg 16261, 55473, 1210, 15320, 34215, 8128), 3,958 units, 0 ~2 ids.

## 2026-10-03 01:55 CDT — mackenzie: done
- 4/4 fetched (Gutenberg 10089, 16653, 47228, 67344), 8,194 units, 0 ~2 ids.

## 2026-10-03 01:56 CDT — stephens: done
- 2/2 fetched (Gutenberg 2892, 65950), 4,001 units, 0 ~2 ids.

## 2026-10-03 01:57 CDT — van-dyke: done
- 5/5 fetched (Gutenberg 16291, 4384, 16134, 1603, 15936), 1,537 units, 0 ~2 ids.

## 2026-10-03 01:59 CDT — irving: done
- 4/4 fetched (Gutenberg 2048, 13514, 49947, 77685), 4,507 units, 0 ~2 ids.

## 2026-10-03 02:12 CDT — curtin-folk: done
- 6/6 fetched (Gutenberg 36540, 50011, 63866, 39106, 64176, 73418), 19,986 units, 0 ~2 ids.

## 2026-10-03 02:14 CDT — larminie: done
- 1/1 fetched (Gutenberg 57858), 1,529 units, 0 ~2 ids.

## 2026-10-03 02:15 CDT — langloh-parker: done
- 1/1 fetched (Gutenberg 3833), 403 units, 0 ~2 ids.

## 2026-10-03 02:16 CDT — pitman: done
- 1/1 fetched (Gutenberg 18674), 942 units, 0 ~2 ids.

## 2026-10-03 02:17 CDT — clouston: done
- 3/3 fetched (Gutenberg 13032, 57468, 60316), 3,318 units, 0 ~2 ids.

## 2026-10-03 02:18 CDT — holbrook: done
- 2/2 fetched (Gutenberg 22420, 20853), 1,415 units, 0 ~2 ids.

## 2026-10-03 02:20 CDT — chodzko: done
- 1/1 fetched (Gutenberg 25555), 1,390 units, 0 ~2 ids.

## 2026-10-03 02:21 CDT — magnus: done
- 1/1 fetched (Gutenberg 62509), 2,830 units, 0 ~2 ids.

## 2026-10-03 02:22 CDT — gaster: done
- 1/1 fetched (Gutenberg 43059), 1,601 units, 0 ~2 ids.

## 2026-10-03 02:23 CDT — theal: done
- 1/1 fetched (Gutenberg 71335), 1,264 units, 0 ~2 ids.

## 2026-10-03 02:25 CDT — nixon-roulet: done
- 1/1 fetched (Gutenberg 73293), 811 units, 0 ~2 ids.

## 2026-10-03 02:27 CDT — mclaughlin: done
- 1/1 fetched (Gutenberg 341), 680 units, 0 ~2 ids.

## 2026-10-03 02:28 CDT — friedlander: done
- 1/1 fetched (Gutenberg 72880), 331 units, 0 ~2 ids.

## 2026-10-03 02:29 CDT — ginzberg: done
- 2/2 fetched (Gutenberg 1493, 1494), 1,836 units, 0 ~2 ids.

## 2026-10-03 02:30 CDT — ewald: done
- 6/6 fetched (Gutenberg 31167, 31708, 65029, 62910, 62912, 40553), 4,968 units, 0 ~2 ids.

## 2026-10-03 02:32 CDT — elizabeth-harrison: done
- 1/1 fetched (Gutenberg 33980), 459 units, 0 ~2 ids.

## 2026-10-03 02:33 CDT — howes: done
- 2/2 fetched (Gutenberg 20366, 38063), 1,135 units, 0 ~2 ids.

## 2026-10-03 02:34 CDT — dracott: done
- 1/1 fetched (Gutenberg 58816), 1,117 units, 0 ~2 ids.

## 2026-10-03 02:36 CDT — wratislaw: done
- 1/1 fetched (Gutenberg 48761), 565 units, 0 ~2 ids.

## 2026-10-03 02:37 CDT — borrow: done
- 1/1 fetched (Gutenberg 16244), 115 units, 0 ~2 ids.

## 2026-10-03 02:50 CDT — pauline-johnson: done
- 1/1 fetched (Gutenberg 28483), 466 units, 0 ~2 ids.

## 2026-10-03 02:52 CDT — leamy: done
- 1/1 fetched (Gutenberg 29311), 715 units, 0 ~2 ids.

## 2026-10-03 02:53 CDT — basil-chamberlain: done
- 3/3 fetched (Gutenberg 29287, 25590, 30024), 272 units, 0 ~2 ids.

## 2026-10-03 02:55 CDT — cyrus-macmillan: done
- 1/1 fetched (Gutenberg 36241), 357 units, 0 ~2 ids.

## 2026-10-03 02:56 CDT — werner: done
- 1/1 fetched (Gutenberg 15250), 1,227 units, 0 ~2 ids.

## 2026-10-03 02:58 CDT — sikes: done
- 1/1 fetched (Gutenberg 34704), 2,072 units, 0 ~2 ids.

## 2026-10-03 02:59 CDT — tregarthen: done
- 2/2 fetched (Gutenberg 37245, 40246), 1,903 units, 0 ~2 ids.

## 2026-10-03 03:01 CDT — ebbutt: done
- 1/1 fetched (Gutenberg 25502), 1,680 units, 0 ~2 ids.

## 2026-10-03 03:02 CDT — maurice-baring: done
- 1/1 fetched (Gutenberg 36008), 769 units, 0 ~2 ids.

## 2026-10-03 03:04 CDT — evelyn-sharp: done
- 2/2 fetched (Gutenberg 30400, 40573), 1,714 units, 0 ~2 ids.

## 2026-10-03 03:05 CDT — mr-james: done
- 2/2 fetched (Gutenberg 15874, 24089), 703 units, 0 ~2 ids.

## 2026-10-03 03:07 CDT — macgowan: done
- 1/1 fetched (Gutenberg 26070), 690 units, 0 ~2 ids.

## 2026-10-03 05:42 CDT — session end (standing relay, batches 22-25)
- Four batches chosen under the standing relay, each a DIGEST row Adam may veto: batch 22 (7 shelves and two more Abbie Farwell Brown books; 36 books, 42,927 units), batch 23 (11 world folk-tale shelves; 19 books, 35,489 units), batch 24 (9 folk-tale, sacred-legend and children's-story shelves; 16 books, 11,206 units), batch 25 (12 folk-tale, legend and fairy-story shelves; 17 books, 12,568 units). Every book retention-checked (no prose paragraph lost), compared against every built book, and `--verify --record`ed: 0 mismatches, 0 rights flags.
- Held once as the same book: Jacobs's Celtic Folk and Fairy Tales (81%), Irving's Pennell Alhambra (66%), Leamy's Golden Spears (89%), an undated second Legends of Vancouver (92%). Held for Adam: Ginzberg's Legends of the Jews vols. 3-4 (tr. Paul Radin, UK copyright to 2029; DIGEST 18).
- convert_nested.py gained `number_repeats` (counted once a heading holds text, after reviewer cycle 9) and `repeat_continues`; tests 17 passed, structure_test 64 passed. Reviewer cycle 9's name forms fixed (Webster, Wilde, Perkins).
- Ninth audit pass in AUDIT-D §11: 983 URLs on 181 shelves resolve except Lang's Lockhart vol. 1 (HTTP 500, local copy intact).
- Nothing minted; manifest, fetch_sources.py, structure_texts.py and the uid map untouched. DIGEST: 200 storytellers, 1,016 slugs on 202 shelves waiting for the attended uid pass. Lock released. Queue: 215/215 done.

## 2026-10-03 05:44 CDT — lock retaken
- The session end above was early: I read the stop time as Saturday 07:00, but RUN-CONTROL's stop_after is Sunday 2026-10-04 07:00 CDT. RUN-CONTROL was already right and was not touched. Lane D resumes with batch 26.

## 2026-10-03 05:55 CDT — elias-owen: done
- 1/1 fetched (Gutenberg 20096), 1,848 units, 0 ~2 ids.

## 2026-10-03 05:57 CDT — kincaid: done
- 2/2 fetched (Gutenberg 11167, 76982), 284 units, 0 ~2 ids.

## 2026-10-03 05:59 CDT — cornelius-mathews: done
- 1/1 fetched (Gutenberg 22248), 1,673 units, 0 ~2 ids.

## 2026-10-03 06:00 CDT — andrew-campbell: done
- 1/1 fetched (Gutenberg 35060), 398 units, 0 ~2 ids.

## 2026-10-03 06:02 CDT — jennie-hall: done
- 1/1 fetched (Gutenberg 24811), 1,123 units, 0 ~2 ids.

## 2026-10-03 06:04 CDT — flora-cooke: done
- 1/1 fetched (Gutenberg 30800), 934 units, 0 ~2 ids.

## 2026-10-03 06:05 CDT — maud-lindsay: done
- 3/3 fetched (Gutenberg 15929, 62748, 23735), 1,721 units, 0 ~2 ids.

## 2026-10-03 06:07 CDT — bain-polevoi: done
- 1/1 fetched (Gutenberg 34705), 259 units, 0 ~2 ids.

## 2026-10-03 06:23 CDT — catherine-sinclair: done
- 1/1 fetched (Gutenberg 32811), 1,077 units, 0 ~2 ids.

## 2026-10-03 06:25 CDT — hesba-stretton: done
- 3/3 fetched (Gutenberg 50104, 30555, 12172), 1,336 units, 0 ~2 ids.

## 2026-10-03 06:27 CDT — bottrell: done
- 2/2 fetched (Gutenberg 41761, 75799), 3,408 units, 0 ~2 ids.

## 2026-10-03 06:28 CDT — aikin-barbauld: done
- 1/1 fetched (Gutenberg 53323), 3,110 units, 0 ~2 ids.

## 2026-10-03 06:30 CDT — marryat: done
- 3/3 fetched (Gutenberg 6471, 1412, 21551), 5,964 units, 0 ~2 ids.

## 2026-10-03 06:32 CDT — thomas-hughes: done
- 1/1 fetched (Gutenberg 1480), 1,403 units, 0 ~2 ids.

## 2026-10-03 06:34 CDT — ballantyne: done
- 2/2 fetched (Gutenberg 646, 21736), 3,159 units, 0 ~2 ids.

## 2026-10-03 06:36 CDT — martha-finley: done
- 3/3 fetched (Gutenberg 6440, 14280, 9963), 7,344 units, 0 ~2 ids.

## 2026-10-03 06:38 CDT — mark-twain: done
- 5/5 fetched (Gutenberg 74, 76, 1837, 91, 93), 7,094 units, 0 ~2 ids.

## 2026-10-03 06:40 CDT — aldrich: done
- 1/1 fetched (Gutenberg 1948), 998 units, 0 ~2 ids.

## 2026-10-03 07:06 CDT — seton: done
- 3/3 fetched (Gutenberg 3031, 9330, 9333), 1,192 units, 0 ~2 ids.

## 2026-10-03 07:08 CDT — charles-g-d-roberts: done
- 2/2 fetched (Gutenberg 46040, 25718), 1,080 units, 0 ~2 ids.

## 2026-10-03 07:10 CDT — jack-london: done
- 2/2 fetched (Gutenberg 215, 910), 1,405 units, 0 ~2 ids.

## 2026-10-03 07:12 CDT — marshall-saunders: done
- 1/1 fetched (Gutenberg 10226), 1,458 units, 0 ~2 ids.

## 2026-10-03 07:15 CDT — annie-fellows-johnston: done
- 10/10 fetched (Gutenberg 9407, 15741, 40463, 15122, 38939, 39599, 26215, 21248, 39594, 15867), 11,527 units, 0 ~2 ids.

## 2026-10-03 07:17 CDT — susan-warner: done
- 2/2 fetched (Gutenberg 28376, 8874), 15,370 units, 0 ~2 ids.

## 2026-10-03 07:19 CDT — aloe: done
- 2/2 fetched (Gutenberg 29863, 60149), 1,808 units, 0 ~2 ids.

## 2026-10-03 07:21 CDT — horatio-alger: done
- 2/2 fetched (Gutenberg 5348, 54006), 4,110 units, 0 ~2 ids.

## 2026-10-03 07:24 CDT — siddha-mohana-mitra: done
- 1/1 fetched (Gutenberg 11310), 593 units, 0 ~2 ids.

## 2026-10-03 07:26 CDT — james-otis: done
- 2/2 fetched (Gutenberg 7478, 27702), 1,919 units, 0 ~2 ids.

## 2026-10-03 07:28 CDT — ceredig-davies: done
- 1/1 fetched (Gutenberg 53915), 1,701 units, 0 ~2 ids.

## 2026-10-03 07:30 CDT — aw-moore: done
- 1/1 fetched (Gutenberg 77469), 1,143 units, 0 ~2 ids.

## 2026-10-03 07:32 CDT — dennys: done
- 1/1 fetched (Gutenberg 76198), 682 units, 0 ~2 ids.

## 2026-10-03 07:34 CDT — mackinlay: done
- 1/1 fetched (Gutenberg 56034), 438 units, 0 ~2 ids.

## 2026-10-03 07:37 CDT — kalakaua: done
- 1/1 fetched (Gutenberg 56597), 2,677 units, 0 ~2 ids.

## 2026-10-03 07:39 CDT — busk-roman: done
- 1/1 fetched (Gutenberg 48771), 3,421 units, 0 ~2 ids.

## 2026-10-03 07:41 CDT — baring-gould-otc: done
- 1/1 fetched (Gutenberg 72268), 4,212 units, 0 ~2 ids.

## 2026-10-10 09:03 CDT — sophie-may: done
- 5/5 fetched (Gutenberg 24711, 14202, 25484, 49686, 16390), 4,105 units, 0 ~2 ids.

## 2026-10-10 09:05 CDT — jacob-abbott: done
- 4/4 fetched (Gutenberg 25274, 11140, 24993, 25548), 3,862 units, 0 ~2 ids.

## 2026-10-10 09:07 CDT — oliver-optic: done
- 3/3 fetched (Gutenberg 24557, 15002, 14762), 5,463 units, 0 ~2 ids.

## 2026-10-10 09:09 CDT — james-cowan: done
- 1/1 fetched (Gutenberg 73766), 156 units, 0 ~2 ids.

## 2026-10-10 09:11 CDT — kate-mccosh-clark: done
- 1/1 fetched (Gutenberg 69782), 441 units, 0 ~2 ids.

## 2026-10-10 09:13 CDT — ranger-gull: done
- 1/1 fetched (Gutenberg 41935), 635 units, 0 ~2 ids.

## 2026-10-10 09:16 CDT — saintine: done
- 1/1 fetched (Gutenberg 44430), 1,301 units, 0 ~2 ids.

## 2026-10-10 09:18 CDT — busk-hofer: done
- 1/1 fetched (Gutenberg 44746), 1,849 units, 0 ~2 ids.

## 2026-10-10 09:22 CDT — hardwick: done
- 1/1 fetched (Gutenberg 39934), 1,651 units, 0 ~2 ids.

## 2026-10-10 09:25 CDT — harland-wilkinson: done
- 1/1 fetched (Gutenberg 41148), 1,507 units, 0 ~2 ids.

## 2026-10-10 09:27 CDT — armistead: done
- 1/1 fetched (Gutenberg 42359), 1,064 units, 0 ~2 ids.

## 2026-10-10 09:29 CDT — burton-harrison: done
- 1/1 fetched (Gutenberg 37348), 910 units, 0 ~2 ids.

## 2026-10-10 09:31 CDT — toru-dutt: done
- 1/1 fetched (Gutenberg 23245), 364 units, 0 ~2 ids.

## 2026-10-10 09:34 CDT — rice-davies: done
- 1/1 fetched (Gutenberg 39539), 1,011 units, 0 ~2 ids.

## 2026-10-10 09:36 CDT — mary-eastman: done
- 1/1 fetched (Gutenberg 10794), 1,184 units, 0 ~2 ids.

## 2026-10-10 09:38 CDT — napier: done
- 1/1 fetched (Gutenberg 15792), 403 units, 0 ~2 ids.

## 2026-10-10 09:40 CDT — patrick-buchan: done
- 1/1 fetched (Gutenberg 37375), 218 units, 0 ~2 ids.

## 2026-10-10 09:43 CDT — furness: done
- 1/1 fetched (Gutenberg 30233), 51 units, 0 ~2 ids.

## 2026-10-10 09:45 CDT — montalba: done
- 1/1 fetched (Gutenberg 34956), 1,111 units, 0 ~2 ids.

## 2026-10-10 09:50 CDT — thomas-day: done
- 2/2 fetched (Gutenberg 30274, 42805), 1,247 units, 0 ~2 ids.

## 2026-10-10 09:52 CDT — farrar: done
- 3/3 fetched (Gutenberg 23126, 23127, 24329), 6,485 units, 0 ~2 ids.

## 2026-10-10 09:54 CDT — talbot-baines-reed: done
- 5/5 fetched (Gutenberg 24632, 21044, 21037, 21035, 21137), 14,545 units, 0 ~2 ids.

## 2026-10-10 09:56 CDT — de-amicis: done
- 1/1 fetched (Gutenberg 28961), 1,593 units, 0 ~2 ids.

## 2026-10-10 09:58 CDT — wilhelm-busch: done
- 1/1 fetched (Gutenberg 28847), 162 units, 0 ~2 ids.

## 2026-10-10 10:01 CDT — edward-lear: done
- 4/4 fetched (Gutenberg 13646, 13647, 13648, 13649), 908 units, 5 ~2 ids.

## 2026-10-10 10:04 CDT — palmer-cox: done
- 3/3 fetched (Gutenberg 32210, 58598, 40502), 1,820 units, 0 ~2 ids.

## 2026-10-10 10:09 CDT — kate-greenaway: done
- 2/2 fetched (Gutenberg 22888, 19541), 349 units, 2 ~2 ids.

## 2026-10-10 10:11 CDT — mary-martha-sherwood: done
- 2/2 fetched (Gutenberg 63295, 58754), 114 units, 3 ~2 ids.
