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

## 2026-10-10 10:14 CDT — mrs-o-f-walton: done
- 3/3 fetched (Gutenberg 21997, 10728, 7437), 3,046 units, 0 ~2 ids.

## 2026-10-10 10:21 CDT — kingston: done
- 3/3 fetched (Gutenberg 21474, 24812, 21477), 4,417 units, 0 ~2 ids.

## 2026-10-10 10:24 CDT — mayne-reid: done
- 3/3 fetched (Gutenberg 21237, 21239, 21238), 3,671 units, 0 ~2 ids.

## 2026-10-10 10:27 CDT — jane-and-ann-taylor: done
- 1/1 fetched (Gutenberg 77549), 419 units, 0 ~2 ids.

## 2026-10-10 10:29 CDT — michael-barrett: done
- 1/1 fetched (Gutenberg 31121), 401 units, 0 ~2 ids.

## 2026-10-10 10:32 CDT — elizabeth-prentiss: done
- 1/1 fetched (Gutenberg 37219), 400 units, 0 ~2 ids.

## 2026-10-10 10:40 CDT — hugh-miller: done
- 1/1 fetched (Gutenberg 71325), 960 units, 0 ~2 ids.

## 2026-10-10 10:43 CDT — emilie-baker: done
- 1/1 fetched (Gutenberg 45489), 1,659 units, 0 ~2 ids.

## 2026-10-10 10:46 CDT — knatchbull-hugessen: done
- 2/2 fetched (Gutenberg 44425, 44924), 1,911 units, 7 ~2 ids.

## 2026-10-10 10:49 CDT — louise-houghton: done
- 1/1 fetched (Gutenberg 45214), 1,412 units, 0 ~2 ids.

## 2026-10-10 10:52 CDT — hanford-gordon: done
- 1/1 fetched (Gutenberg 8122), 525 units, 0 ~2 ids.

## 2026-10-10 15:09 CDT — session end: paused at Adam's request
- Batches 30-35 (37 shelves, headline 239 to 270) and audit passes 11-12 committed and pushed. No batch in progress; no partial shelves on disk.
- Lock set to paused. Resume with batch 36 when reactivated.

## 2026-10-17 16:45 CDT — ginzberg: done
- 2/2 fetched (Gutenberg 2881, 2882), 1,704 units, 0 ~2 ids.

## 2026-10-17 16:50 CDT — eleanore-jewett: done
- 1/1 fetched (Gutenberg 66443), 510 units, 0 ~2 ids.

## 2026-10-17 16:56 CDT — philippine-jafl: done
- 1/1 fetched (Gutenberg 11028), 1,278 units, 0 ~2 ids.

## 2026-10-17 17:01 CDT — mary-martha-sherwood: done
- 1/1 fetched (Gutenberg 29725), 2,940 units, 0 ~2 ids.

## 2026-10-17 17:17 CDT — kingston: done
- kingston: completed, 130 more Gutenberg books (133 on the shelf), 136,262 units, 924 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:17 CDT — mayne-reid: done
- mayne-reid: completed, 47 more Gutenberg books (50 on the shelf), 108,111 units, 76 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:23 CDT — lang: done
- lang: adds Ballads of Books (IA balladsbooks00mattiala, 1888, raw OCR); all 124 items re-verified, 0 mismatches.

## 2026-10-17 17:23 CDT — horatio-alger: done
- horatio-alger: completed, 103 more Gutenberg books (105 on the shelf), 260,068 units, 685 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:23 CDT — ballantyne: done
- ballantyne: completed, 86 more Gutenberg books (88 on the shelf), 114,526 units, 58 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:23 CDT — oliver-optic: done
- oliver-optic: completed, 80 more Gutenberg books (83 on the shelf), 141,694 units, 1325 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:23 CDT — molesworth: done
- molesworth: completed, 50 more Gutenberg books (58 on the shelf), 71,899 units, 138 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:23 CDT — aloe: done
- aloe: completed, 44 more Gutenberg books (46 on the shelf), 30,201 units, 102 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:23 CDT — james-otis: done
- james-otis: completed, 53 more Gutenberg books (55 on the shelf), 77,037 units, 47 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:29 CDT — martha-finley: done
- martha-finley: completed, 35 more Gutenberg books (38 on the shelf), 71,016 units, 224 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:29 CDT — sophie-may: done
- sophie-may: completed, 19 more Gutenberg books (24 on the shelf), 21,330 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:29 CDT — annie-fellows-johnston: done
- annie-fellows-johnston: completed, 27 more Gutenberg books (37 on the shelf), 25,796 units, 83 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:29 CDT — burgess: done
- burgess: completed, 14 more Gutenberg books (40 on the shelf), 16,563 units, 22 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:29 CDT — ewing: done
- ewing: completed, 11 more Gutenberg books (18 on the shelf), 19,842 units, 314 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:29 CDT — hesba-stretton: done
- hesba-stretton: completed, 12 more Gutenberg books (15 on the shelf), 11,385 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:38 CDT — yonge: done
- yonge: completed, 58 more Gutenberg books (64 on the shelf), 144,769 units, 8979 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:38 CDT — burnett: done
- burnett: completed, 35 more Gutenberg books (42 on the shelf), 47,126 units, 1971 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:38 CDT — garis: done
- garis: completed, 29 more Gutenberg books (64 on the shelf), 80,385 units, 19 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:39 CDT — susan-warner: done
- susan-warner: completed, 27 more Gutenberg books (29 on the shelf), 116,395 units, 3086 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:39 CDT — richards: done
- richards: completed, 34 more Gutenberg books (43 on the shelf), 34,506 units, 66 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:39 CDT — jacob-abbott: done
- jacob-abbott: completed, 25 more Gutenberg books (29 on the shelf), 27,177 units, 51 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:39 CDT — marryat: done
- marryat: completed, 26 more Gutenberg books (29 on the shelf), 61,742 units, 782 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:39 CDT — stockton: done
- stockton: completed, 35 more Gutenberg books (38 on the shelf), 41,634 units, 490 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:39 CDT — alcott: done
- alcott: completed, 32 more Gutenberg books (41 on the shelf), 47,940 units, 667 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:39 CDT — wiggin: done
- wiggin: completed, 26 more Gutenberg books (32 on the shelf), 21,085 units, 469 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — seton: done
- seton: completed, 11 more Gutenberg books (14 on the shelf), 13,104 units, 1011 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — coolidge: done
- coolidge: completed, 6 more Gutenberg books (15 on the shelf), 13,052 units, 16 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — church: done
- church: completed, 8 more Gutenberg books (17 on the shelf), 12,924 units, 275 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — abbie-brown: done
- abbie-brown: completed, 11 more Gutenberg books (14 on the shelf), 8,560 units, 23 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — charles-g-d-roberts: done
- charles-g-d-roberts: completed, 27 more Gutenberg books (29 on the shelf), 19,213 units, 323 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — talbot-baines-reed: done
- talbot-baines-reed: completed, 11 more Gutenberg books (16 on the shelf), 48,216 units, 114 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — grinnell: done
- grinnell: completed, 7 more Gutenberg books (11 on the shelf), 12,120 units, 6 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — mrs-o-f-walton: done
- mrs-o-f-walton: completed, 9 more Gutenberg books (12 on the shelf), 10,211 units, 7 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — eleanor-porter: done
- eleanor-porter: completed, 11 more Gutenberg books (14 on the shelf), 28,645 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — aldrich: done
- aldrich: completed, 15 more Gutenberg books (16 on the shelf), 6,125 units, 59 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — marshall-saunders: done
- marshall-saunders: completed, 15 more Gutenberg books (16 on the shelf), 32,241 units, 499 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — thomas-hughes: done
- thomas-hughes: completed, 5 more Gutenberg books (6 on the shelf), 9,485 units, 112 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:45 CDT — katharine-pyle: done
- katharine-pyle: completed, 6 more Gutenberg books (13 on the shelf), 11,283 units, 68 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:52 CDT — baum: done
- baum: completed, 50 more Gutenberg books (65 on the shelf), 81,391 units, 66 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:52 CDT — edgeworth: done
- edgeworth: completed, 19 more Gutenberg books (20 on the shelf), 38,155 units, 5012 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:53 CDT — craik: done
- craik: completed, 12 more Gutenberg books (15 on the shelf), 26,576 units, 19 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:53 CDT — harris-remus: done
- harris-remus: completed, 14 more Gutenberg books (18 on the shelf), 19,040 units, 40 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 17:53 CDT — ouida: done
- ouida: completed, 23 more Gutenberg books (26 on the shelf), 43,737 units, 2498 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:00 CDT — mark-twain: done
- mark-twain: completed, 65 more Gutenberg books (70 on the shelf), 53,221 units, 3275 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:00 CDT — jack-london: done
- jack-london: completed, 47 more Gutenberg books (49 on the shelf), 57,643 units, 6128 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:00 CDT — stevenson: done
- stevenson: completed, 2 more Gutenberg books (47 on the shelf), 35,579 units, 68 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:00 CDT — irving: done
- irving: completed, 18 more Gutenberg books (22 on the shelf), 24,509 units, 1934 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:00 CDT — steel: done
- steel: completed, 16 more Gutenberg books (18 on the shelf), 34,661 units, 728 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:10 CDT — fenn: done
- fenn: new shelf, 128 Gutenberg books, 395,207 units, 680 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:10 CDT — edward-ellis: done
- edward-ellis: new shelf, 73 Gutenberg books, 89,976 units, 409 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:10 CDT — castlemon: done
- castlemon: new shelf, 52 Gutenberg books, 70,481 units, 10 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:10 CDT — gordon-stables: done
- gordon-stables: new shelf, 39 Gutenberg books, 69,522 units, 1111 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:10 CDT — altsheler: done
- altsheler: new shelf, 35 Gutenberg books, 68,668 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:10 CDT — kirk-munroe: done
- kirk-munroe: new shelf, 21 Gutenberg books, 24,374 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:10 CDT — le-feuvre: done
- le-feuvre: new shelf, 36 Gutenberg books, 58,798 units, 911 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:10 CDT — everett-green: done
- everett-green: new shelf, 27 Gutenberg books, 36,146 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:10 CDT — lt-meade: done
- lt-meade: new shelf, 61 Gutenberg books, 116,447 units, 212 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:10 CDT — giberne: done
- giberne: new shelf, 39 Gutenberg books, 60,530 units, 2075 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:10 CDT — collingwood: done
- collingwood: new shelf, 34 Gutenberg books, 33,877 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:20 CDT — haggard: done
- haggard: new shelf, 59 Gutenberg books, 98,007 units, 986 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:20 CDT — weyman: done
- weyman: new shelf, 26 Gutenberg books, 52,133 units, 185 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:20 CDT — zane-grey: done
- zane-grey: new shelf, 27 Gutenberg books, 56,438 units, 90 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:20 CDT — curwood: done
- curwood: new shelf, 27 Gutenberg books, 27,064 units, 3 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:20 CDT — westerman: done
- westerman: new shelf, 47 Gutenberg books, 74,910 units, 145 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:20 CDT — brereton: done
- brereton: new shelf, 20 Gutenberg books, 31,295 units, 10 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:20 CDT — barbour: done
- barbour: new shelf, 76 Gutenberg books, 109,526 units, 178 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:20 CDT — carolyn-wells: done
- carolyn-wells: new shelf, 65 Gutenberg books, 111,419 units, 31 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:20 CDT — pansy: done
- pansy: new shelf, 22 Gutenberg books, 25,225 units, 423 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:20 CDT — emily-holt: done
- emily-holt: new shelf, 23 Gutenberg books, 41,359 units, 761 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:29 CDT — anthony-hope: done
- anthony-hope: new shelf, 35 Gutenberg books, 71,124 units, 55 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:32 CDT — laura-lee-hope: done
- laura-lee-hope: new shelf, 73 Gutenberg books, 108,402 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:32 CDT — allen-chapman: done
- allen-chapman: new shelf, 28 Gutenberg books, 44,282 units, 66 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:32 CDT — vandercook: done
- vandercook: new shelf, 30 Gutenberg books, 28,133 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:32 CDT — margaret-penrose: done
- margaret-penrose: new shelf, 28 Gutenberg books, 49,176 units, 9 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:32 CDT — joanna-mathews: done
- joanna-mathews: new shelf, 14 Gutenberg books, 16,509 units, 25 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:32 CDT — amanda-douglas: done
- amanda-douglas: new shelf, 21 Gutenberg books, 47,292 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:32 CDT — joseph-hocking: done
- joseph-hocking: new shelf, 12 Gutenberg books, 33,522 units, 57 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:41 CDT — burt-standish: done
- burt-standish: new shelf, 59 Gutenberg books, 147,563 units, 340 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:41 CDT — irving-hancock: done
- irving-hancock: new shelf, 40 Gutenberg books, 77,566 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:41 CDT — alice-emerson: done
- alice-emerson: new shelf, 25 Gutenberg books, 35,024 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:41 CDT — stratemeyer: done
- stratemeyer: new shelf, 104 Gutenberg books, 226,455 units, 234 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:41 CDT — victor-appleton: done
- victor-appleton: new shelf, 46 Gutenberg books, 64,065 units, 68 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:41 CDT — frank-webster: done
- frank-webster: new shelf, 25 Gutenberg books, 38,030 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:41 CDT — emerson-hough: done
- emerson-hough: new shelf, 28 Gutenberg books, 44,661 units, 30 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:41 CDT — sarah-orne-jewett: done
- sarah-orne-jewett: new shelf, 11 Gutenberg books, 8,638 units, 288 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:50 CDT — william-o-stoddard: done
- william-o-stoddard: new shelf, 14 Gutenberg books, 24,357 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:50 CDT — edward-everett-hale: done
- edward-everett-hale: new shelf, 11 Gutenberg books, 10,593 units, 62 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:50 CDT — sara-ware-bassett: done
- sara-ware-bassett: new shelf, 17 Gutenberg books, 23,994 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:50 CDT — frank-gee-patchin: done
- frank-gee-patchin: new shelf, 15 Gutenberg books, 31,062 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:51 CDT — william-macleod-raine: done
- william-macleod-raine: new shelf, 23 Gutenberg books, 50,934 units, 10 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:51 CDT — harold-bindloss: done
- harold-bindloss: new shelf, 46 Gutenberg books, 101,904 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:51 CDT — e-phillips-oppenheim: done
- e-phillips-oppenheim: new shelf, 58 Gutenberg books, 135,883 units, 5708 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 18:51 CDT — william-le-queux: done
- william-le-queux: new shelf, 93 Gutenberg books, 174,556 units, 46 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:00 CDT — edgar-wallace: done
- edgar-wallace: new shelf, 44 Gutenberg books, 99,259 units, 1827 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:00 CDT — ew-hornung: done
- ew-hornung: new shelf, 29 Gutenberg books, 41,558 units, 196 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:00 CDT — mary-roberts-rinehart: done
- mary-roberts-rinehart: new shelf, 29 Gutenberg books, 49,183 units, 1612 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:00 CDT — js-fletcher: done
- js-fletcher: new shelf, 22 Gutenberg books, 34,338 units, 11 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:00 CDT — frank-packard: done
- frank-packard: new shelf, 13 Gutenberg books, 23,186 units, 14 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:00 CDT — aew-mason: done
- aew-mason: new shelf, 22 Gutenberg books, 40,747 units, 45 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:00 CDT — ww-jacobs: done
- ww-jacobs: new shelf, 19 Gutenberg books, 33,177 units, 158 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:00 CDT — jerome-k-jerome: done
- jerome-k-jerome: new shelf, 31 Gutenberg books, 24,814 units, 1691 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:10 CDT — john-kendrick-bangs: done
- john-kendrick-bangs: new shelf, 39 Gutenberg books, 28,298 units, 830 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:10 CDT — irvin-cobb: done
- irvin-cobb: new shelf, 26 Gutenberg books, 21,735 units, 13 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:10 CDT — ef-benson: done
- ef-benson: new shelf, 52 Gutenberg books, 74,602 units, 2184 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:10 CDT — quiller-couch: done
- quiller-couch: new shelf, 42 Gutenberg books, 61,319 units, 1798 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:10 CDT — sr-crockett: done
- sr-crockett: new shelf, 21 Gutenberg books, 47,257 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:10 CDT — robert-barr: done
- robert-barr: new shelf, 21 Gutenberg books, 40,782 units, 394 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:11 CDT — robert-w-chambers: done
- robert-w-chambers: new shelf, 46 Gutenberg books, 148,165 units, 2387 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:11 CDT — george-barr-mccutcheon: done
- george-barr-mccutcheon: new shelf, 35 Gutenberg books, 63,270 units, 872 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:21 CDT — eden-phillpotts: done
- eden-phillpotts: new shelf, 28 Gutenberg books, 48,160 units, 2022 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:21 CDT — thackeray: done
- thackeray: new shelf, 30 Gutenberg books, 36,386 units, 97 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:21 CDT — melville: done
- melville: new shelf, 16 Gutenberg books, 21,854 units, 937 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:21 CDT — henry-james: done
- henry-james: new shelf, 88 Gutenberg books, 75,620 units, 5590 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:21 CDT — howells: done
- howells: new shelf, 89 Gutenberg books, 75,851 units, 5581 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:21 CDT — gaskell: done
- gaskell: new shelf, 19 Gutenberg books, 24,041 units, 474 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:21 CDT — george-meredith: done
- george-meredith: new shelf, 28 Gutenberg books, 48,697 units, 1179 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:21 CDT — bulwer-lytton: done
- bulwer-lytton: new shelf, 34 Gutenberg books, 75,938 units, 23842 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:32 CDT — charles-reade: done
- charles-reade: new shelf, 16 Gutenberg books, 69,933 units, 2301 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:32 CDT — blackmore: done
- blackmore: new shelf, 23 Gutenberg books, 34,890 units, 961 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:32 CDT — gissing: done
- gissing: new shelf, 24 Gutenberg books, 66,144 units, 8206 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:32 CDT — joseph-conrad: done
- joseph-conrad: new shelf, 36 Gutenberg books, 36,820 units, 4488 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:32 CDT — chesterton: done
- chesterton: new shelf, 23 Gutenberg books, 14,345 units, 23 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:32 CDT — arnold-bennett: done
- arnold-bennett: new shelf, 50 Gutenberg books, 75,549 units, 6091 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:32 CDT — galsworthy: done
- galsworthy: new shelf, 53 Gutenberg books, 97,198 units, 23247 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:32 CDT — bret-harte: done
- bret-harte: new shelf, 57 Gutenberg books, 45,576 units, 2014 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:43 CDT — braddon: done
- braddon: new shelf, 65 Gutenberg books, 121,301 units, 227 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:43 CDT — mrs-oliphant: done
- mrs-oliphant: new shelf, 124 Gutenberg books, 138,815 units, 4280 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:43 CDT — disraeli: done
- disraeli: new shelf, 17 Gutenberg books, 30,415 units, 7860 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:43 CDT — ainsworth: done
- ainsworth: new shelf, 16 Gutenberg books, 50,891 units, 1529 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:43 CDT — gpr-james: done
- gpr-james: new shelf, 50 Gutenberg books, 92,831 units, 4910 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:43 CDT — fielding: done
- fielding: new shelf, 12 Gutenberg books, 12,967 units, 847 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:43 CDT — samuel-richardson: done
- samuel-richardson: new shelf, 14 Gutenberg books, 26,144 units, 1921 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:43 CDT — fanny-burney: done
- fanny-burney: new shelf, 17 Gutenberg books, 37,620 units, 724 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:55 CDT — goldsmith: done
- goldsmith: new shelf, 9 Gutenberg books, 7,831 units, 1075 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:55 CDT — mrs-henry-wood: done
- mrs-henry-wood: new shelf, 36 Gutenberg books, 129,540 units, 937 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:55 CDT — humphry-ward: done
- humphry-ward: new shelf, 33 Gutenberg books, 71,028 units, 3292 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:55 CDT — marie-corelli: done
- marie-corelli: new shelf, 25 Gutenberg books, 46,147 units, 993 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:55 CDT — george-moore: done
- george-moore: new shelf, 16 Gutenberg books, 26,127 units, 243 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:55 CDT — sterne: done
- sterne: new shelf, 4 Gutenberg books, 4,264 units, 1234 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:55 CDT — peacock: done
- peacock: new shelf, 6 Gutenberg books, 5,711 units, 19 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 19:55 CDT — dickens-works: done
- dickens-works: new shelf, 61 Gutenberg books, 97,561 units, 4667 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:06 CDT — hardy-works: done
- hardy-works: new shelf, 24 Gutenberg books, 49,645 units, 7539 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:06 CDT — walter-scott-works: done
- walter-scott-works: new shelf, 41 Gutenberg books, 81,321 units, 13470 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:06 CDT — george-eliot-works: done
- george-eliot-works: new shelf, 14 Gutenberg books, 23,410 units, 107 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:06 CDT — austen-works: done
- austen-works: new shelf, 4 Gutenberg books, 3,271 units, 66 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:06 CDT — bronte-works: done
- bronte-works: new shelf, 8 Gutenberg books, 15,031 units, 91 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:06 CDT — wilkie-collins-works: done
- wilkie-collins-works: new shelf, 30 Gutenberg books, 64,134 units, 7888 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:06 CDT — hgwells-works: done
- hgwells-works: new shelf, 70 Gutenberg books, 92,629 units, 8428 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:06 CDT — conan-doyle-works: done
- conan-doyle-works: new shelf, 71 Gutenberg books, 69,355 units, 767 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:18 CDT — defoe-works: done
- defoe-works: new shelf, 43 Gutenberg books, 22,414 units, 1791 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:18 CDT — cather-works: done
- cather-works: new shelf, 10 Gutenberg books, 10,314 units, 2645 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:18 CDT — poe-works: done
- poe-works: new shelf, 15 Gutenberg books, 10,750 units, 479 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:18 CDT — trollope-works: done
- trollope-works: new shelf, 81 Gutenberg books, 168,715 units, 1547 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:18 CDT — cooper-works: done
- cooper-works: new shelf, 38 Gutenberg books, 74,483 units, 5496 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:18 CDT — hawthorne-works: done
- hawthorne-works: new shelf, 78 Gutenberg books, 19,898 units, 1536 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:18 CDT — stephen-crane-works: done
- stephen-crane-works: new shelf, 13 Gutenberg books, 12,315 units, 455 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:18 CDT — bierce-works: done
- bierce-works: new shelf, 23 Gutenberg books, 17,776 units, 1358 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:30 CDT — o-henry-works: done
- o-henry-works: new shelf, 16 Gutenberg books, 18,991 units, 89 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:30 CDT — henty-works: done
- henty-works: new shelf, 97 Gutenberg books, 163,907 units, 457 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:30 CDT — wharton-works: done
- wharton-works: new shelf, 47 Gutenberg books, 42,895 units, 706 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:30 CDT — burroughs-works: done
- burroughs-works: new shelf, 30 Gutenberg books, 38,011 units, 7 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:30 CDT — wodehouse-works: done
- wodehouse-works: new shelf, 51 Gutenberg books, 109,358 units, 958 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:30 CDT — tarkington-works: done
- tarkington-works: new shelf, 25 Gutenberg books, 34,517 units, 1065 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:30 CDT — buchan-works: done
- buchan-works: new shelf, 16 Gutenberg books, 18,482 units, 189 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 20:31 CDT — lester-chadwick: done
- lester-chadwick: new shelf, 18 Gutenberg books, 34,968 units, 27 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:06 CDT — joseph-c-lincoln: done
- joseph-c-lincoln: new shelf, 20 Gutenberg books, 54,914 units, 474 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:06 CDT — bm-bower: done
- bm-bower: new shelf, 36 Gutenberg books, 33,251 units, 5 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:06 CDT — clarence-mulford: done
- clarence-mulford: new shelf, 11 Gutenberg books, 19,181 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:06 CDT — peter-kyne: done
- peter-kyne: new shelf, 11 Gutenberg books, 19,596 units, 121 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:06 CDT — fergus-hume: done
- fergus-hume: new shelf, 65 Gutenberg books, 146,359 units, 14 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:06 CDT — anna-katharine-green: done
- anna-katharine-green: new shelf, 37 Gutenberg books, 51,323 units, 338 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:06 CDT — james-grant: done
- james-grant: new shelf, 70 Gutenberg books, 110,796 units, 148 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:07 CDT — charles-lever: done
- charles-lever: new shelf, 46 Gutenberg books, 121,283 units, 312 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:25 CDT — marion-crawford: done
- marion-crawford: new shelf, 52 Gutenberg books, 95,562 units, 956 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:25 CDT — charles-dudley-warner: done
- charles-dudley-warner: new shelf, 44 Gutenberg books, 29,122 units, 3466 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:25 CDT — mary-jane-holmes: done
- mary-jane-holmes: new shelf, 46 Gutenberg books, 73,388 units, 596 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:25 CDT — clark-russell: done
- clark-russell: new shelf, 42 Gutenberg books, 47,073 units, 98 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:25 CDT — borrow-works: done
- borrow-works: new shelf, 17 Gutenberg books, 26,488 units, 1165 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:25 CDT — richard-harding-davis: done
- richard-harding-davis: new shelf, 42 Gutenberg books, 25,183 units, 169 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:25 CDT — stowe-works: done
- stowe-works: new shelf, 33 Gutenberg books, 47,017 units, 1435 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:25 CDT — oliver-wendell-holmes: done
- oliver-wendell-holmes: new shelf, 17 Gutenberg books, 29,577 units, 1675 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:41 CDT — walter-besant: done
- walter-besant: new shelf, 33 Gutenberg books, 68,471 units, 769 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:41 CDT — southworth: done
- southworth: new shelf, 33 Gutenberg books, 122,011 units, 456 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:41 CDT — grant-allen: done
- grant-allen: new shelf, 31 Gutenberg books, 26,365 units, 26 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:41 CDT — le-fanu: done
- le-fanu: new shelf, 32 Gutenberg books, 48,683 units, 372 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:41 CDT — hopkinson-smith: done
- hopkinson-smith: new shelf, 28 Gutenberg books, 26,094 units, 337 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:41 CDT — amelia-barr: done
- amelia-barr: new shelf, 27 Gutenberg books, 44,336 units, 266 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:41 CDT — thomas-nelson-page: done
- thomas-nelson-page: new shelf, 27 Gutenberg books, 20,093 units, 207 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:41 CDT — florence-marryat: done
- florence-marryat: new shelf, 27 Gutenberg books, 25,727 units, 76 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:58 CDT — wj-locke: done
- wj-locke: new shelf, 26 Gutenberg books, 53,327 units, 88 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:58 CDT — mary-wilkins-freeman: done
- mary-wilkins-freeman: new shelf, 25 Gutenberg books, 39,306 units, 7 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:58 CDT — wilde-works: done
- wilde-works: new shelf, 23 Gutenberg books, 12,412 units, 2319 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:58 CDT — stacpoole: done
- stacpoole: new shelf, 34 Gutenberg books, 47,023 units, 1608 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:59 CDT — gertrude-atherton: done
- gertrude-atherton: new shelf, 32 Gutenberg books, 43,659 units, 9527 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:59 CDT — robert-hichens: done
- robert-hichens: new shelf, 31 Gutenberg books, 70,045 units, 6533 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:59 CDT — orczy-works: done
- orczy-works: new shelf, 29 Gutenberg books, 58,364 units, 1348 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 21:59 CDT — angela-brazil: done
- angela-brazil: new shelf, 27 Gutenberg books, 38,016 units, 6 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:16 CDT — algernon-blackwood: done
- algernon-blackwood: new shelf, 27 Gutenberg books, 34,103 units, 1572 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:16 CDT — hamlin-garland: done
- hamlin-garland: new shelf, 24 Gutenberg books, 42,790 units, 1198 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:16 CDT — stewart-edward-white: done
- stewart-edward-white: new shelf, 23 Gutenberg books, 37,374 units, 2448 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:16 CDT — may-sinclair: done
- may-sinclair: new shelf, 22 Gutenberg books, 57,447 units, 959 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:16 CDT — upton-sinclair-works: done
- upton-sinclair-works: new shelf, 41 Gutenberg books, 64,686 units, 4256 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:17 CDT — winston-churchill-novels: done
- winston-churchill-novels: new shelf, 15 Gutenberg books, 75,752 units, 7972 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:17 CDT — gilbert-parker: done
- gilbert-parker: new shelf, 37 Gutenberg books, 88,795 units, 4235 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:17 CDT — percy-keese-fitzhugh: done
- percy-keese-fitzhugh: new shelf, 42 Gutenberg books, 49,615 units, 95 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:35 CDT — roy-j-snell: done
- roy-j-snell: new shelf, 22 Gutenberg books, 27,591 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:36 CDT — john-henry-goldfrap: done
- john-henry-goldfrap: new shelf, 45 Gutenberg books, 69,935 units, 91 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:36 CDT — madeline-leslie: done
- madeline-leslie: new shelf, 43 Gutenberg books, 20,987 units, 77 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:36 CDT — amy-blanchard: done
- amy-blanchard: new shelf, 42 Gutenberg books, 55,480 units, 19 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:36 CDT — arthur-scott-bailey: done
- arthur-scott-bailey: new shelf, 41 Gutenberg books, 20,692 units, 9 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:36 CDT — josephine-chase: done
- josephine-chase: new shelf, 39 Gutenberg books, 53,664 units, 104 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:36 CDT — clarence-young: done
- clarence-young: new shelf, 26 Gutenberg books, 49,383 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:36 CDT — evelyn-raymond: done
- evelyn-raymond: new shelf, 24 Gutenberg books, 31,257 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:56 CDT — grace-livingston-hill: done
- grace-livingston-hill: new shelf, 25 Gutenberg books, 32,212 units, 243 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:56 CDT — lucy-ellen-guernsey: done
- lucy-ellen-guernsey: new shelf, 47 Gutenberg books, 56,597 units, 93 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:56 CDT — ts-arthur: done
- ts-arthur: new shelf, 36 Gutenberg books, 50,901 units, 202 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:56 CDT — charles-king: done
- charles-king: new shelf, 29 Gutenberg books, 24,190 units, 122 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:56 CDT — frank-frankfort-moore: done
- frank-frankfort-moore: new shelf, 17 Gutenberg books, 28,394 units, 85 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:56 CDT — louis-becke: done
- louis-becke: new shelf, 39 Gutenberg books, 17,566 units, 2100 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:56 CDT — charles-egbert-craddock: done
- charles-egbert-craddock: new shelf, 40 Gutenberg books, 34,383 units, 172 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 22:56 CDT — bm-croker: done
- bm-croker: new shelf, 26 Gutenberg books, 36,012 units, 18 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:24 CDT — ellis-parker-butler: done
- ellis-parker-butler: new shelf, 26 Gutenberg books, 14,600 units, 29 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:24 CDT — israel-zangwill: done
- israel-zangwill: new shelf, 16 Gutenberg books, 38,402 units, 1007 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:24 CDT — edmund-yates: done
- edmund-yates: new shelf, 24 Gutenberg books, 24,494 units, 16 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:24 CDT — william-black: done
- william-black: new shelf, 21 Gutenberg books, 35,046 units, 156 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:24 CDT — edward-bellamy: done
- edward-bellamy: new shelf, 21 Gutenberg books, 7,920 units, 38 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:24 CDT — mary-johnston: done
- mary-johnston: new shelf, 21 Gutenberg books, 39,400 units, 2182 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:24 CDT — ellen-glasgow: done
- ellen-glasgow: new shelf, 15 Gutenberg books, 34,146 units, 3272 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:24 CDT — theodore-dreiser: done
- theodore-dreiser: new shelf, 16 Gutenberg books, 40,110 units, 2523 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:48 CDT — ian-maclaren: done
- ian-maclaren: new shelf, 10 Gutenberg books, 7,547 units, 252 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:48 CDT — maurice-hewlett: done
- maurice-hewlett: new shelf, 19 Gutenberg books, 20,725 units, 39 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:48 CDT — henry-seton-merriman: done
- henry-seton-merriman: new shelf, 17 Gutenberg books, 33,066 units, 198 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:48 CDT — george-washington-cable: done
- george-washington-cable: new shelf, 14 Gutenberg books, 26,184 units, 220 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:48 CDT — sabatini-works: done
- sabatini-works: new shelf, 20 Gutenberg books, 42,768 units, 37 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-17 23:48 CDT — montgomery-works: done
- montgomery-works: new shelf, 6 Gutenberg books, 10,135 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-18 00:15 CDT — session end: PAUSED at Adam's request
- Adam (via the coordinator, 2026-10-18 04:34Z): "Pause this project please". Finished the step in progress, pushed everything, released the lock.
- This burn session (from 2026-10-17 21:32Z): 279 Lane D commits, 187 new shelves holding 6,338 Gutenberg books, plus completions: batches 36-50, the "-works" shelves for the major English and American novelists (Dickens through Henty, Wharton, Wodehouse and the rest, pre-1931 only where told), and batch 49-50 novelists (Le Fanu, Zangwill, Dreiser, Glasgow, Cable, Sabatini and others).
- Fixes: duplicate-check flaw (DIGEST item 26), Chesterton overlap with main (item 25), post-1930 holds (item 24).
- RESUME POINT: next is batch 51, candidates not yet started: children's and popular authors with no shelf on any branch (check again before starting). The ones surveyed and still free: none left from the batch-50 list. Possible next: authors with only a single-title reading-list shelf (standing rule: Lane D completes them), and a renewal check for the DIGEST item 24 holds if Adam says so. Helper scripts lived in the session scratch area and are gone; the shelf format and gates are in pipeline/fetch_shelf.py and overnight/divines/precommit-D.py.

## 2026-10-22 22:08 CDT — william-carleton: done
- william-carleton: new shelf, 19 Gutenberg books, 34,095 units, 9 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:09 CDT — bertram-mitford: done
- bertram-mitford: new shelf, 27 Gutenberg books, 46,410 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:09 CDT — louis-tracy: done
- louis-tracy: new shelf, 30 Gutenberg books, 59,909 units, 223 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:09 CDT — bl-farjeon: done
- bl-farjeon: new shelf, 29 Gutenberg books, 61,676 units, 684 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:10 CDT — ann-s-stephens: done
- ann-s-stephens: new shelf, 29 Gutenberg books, 87,204 units, 1709 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:10 CDT — molly-elliot-seawell: done
- molly-elliot-seawell: new shelf, 28 Gutenberg books, 28,378 units, 119 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:11 CDT — meredith-nicholson: done
- meredith-nicholson: new shelf, 27 Gutenberg books, 42,906 units, 3726 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:11 CDT — francis-lynde: done
- francis-lynde: new shelf, 26 Gutenberg books, 50,415 units, 105 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:12 CDT — richard-marsh: done
- richard-marsh: new shelf, 25 Gutenberg books, 54,448 units, 1206 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:13 CDT — mrs-de-horne-vaizey: done
- mrs-de-horne-vaizey: new shelf, 23 Gutenberg books, 28,636 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:13 CDT — harvey-ralphson: done
- harvey-ralphson: new shelf, 21 Gutenberg books, 34,391 units, 51 ~2 ids; verify 0 mismatches, 0 rights flags; 2 failed to fetch.

## 2026-10-22 22:13 CDT — lillian-elizabeth-roy: done
- lillian-elizabeth-roy: new shelf, 22 Gutenberg books, 33,995 units, 76 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:14 CDT — harold-macgrath: done
- harold-macgrath: new shelf, 22 Gutenberg books, 44,178 units, 89 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:14 CDT — david-graham-phillips: done
- david-graham-phillips: new shelf, 22 Gutenberg books, 43,827 units, 2624 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — mary-hartwell-catherwood: done
- mary-hartwell-catherwood: new shelf, 21 Gutenberg books, 15,807 units, 1730 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — ridgwell-cullum: done
- ridgwell-cullum: new shelf, 21 Gutenberg books, 51,427 units, 160 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — mary-hazelton-wade: done
- mary-hazelton-wade: new shelf, 19 Gutenberg books, 10,802 units, 72 ~2 ids; verify 0 mismatches, 0 rights flags; 2 failed to fetch.

## 2026-10-22 22:15 CDT — the-duchess: done
- the-duchess: new shelf, 20 Gutenberg books, 40,366 units, 1329 ~2 ids; verify 0 mismatches, 0 rights flags; 1 failed to fetch.

## 2026-10-22 22:15 CDT — hall-caine: done
- hall-caine: new shelf, 20 Gutenberg books, 60,656 units, 18926 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — tw-speight: done
- tw-speight: new shelf, 20 Gutenberg books, 20,938 units, 3 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — edwin-l-sabin: done
- edwin-l-sabin: new shelf, 20 Gutenberg books, 37,030 units, 53 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — george-cary-eggleston: done
- george-cary-eggleston: new shelf, 20 Gutenberg books, 25,996 units, 85 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — eglanton-thorne: done
- eglanton-thorne: new shelf, 19 Gutenberg books, 20,401 units, 7 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — jc-snaith: done
- jc-snaith: new shelf, 19 Gutenberg books, 36,903 units, 2745 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — emma-leslie: done
- emma-leslie: new shelf, 19 Gutenberg books, 13,636 units, 7 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — bernard-capes: done
- bernard-capes: new shelf, 19 Gutenberg books, 42,875 units, 2049 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — ep-roe: done
- ep-roe: new shelf, 19 Gutenberg books, 43,142 units, 9 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — irving-bacheller: done
- irving-bacheller: new shelf, 18 Gutenberg books, 24,996 units, 107 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — mrs-jh-riddell: done
- mrs-jh-riddell: new shelf, 18 Gutenberg books, 22,596 units, 8 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:15 CDT — williamsons: done
- williamsons: new shelf, 34 Gutenberg books, 54,524 units, 2542 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:16 CDT — three name-gate refusals cleared
- harvey-ralphson: new shelf, 23 Gutenberg books, 37,387 units, 51 ~2 ids; verify 0 mismatches, 0 rights flags (name check per book for 2, see _surname_by_slug).
- mary-hazelton-wade: new shelf, 21 Gutenberg books, 11,792 units, 72 ~2 ids; verify 0 mismatches, 0 rights flags (name check per book for 2, see _surname_by_slug).
- the-duchess: new shelf, 21 Gutenberg books, 44,271 units, 1329 ~2 ids; verify 0 mismatches, 0 rights flags (name check per book for 1, see _surname_by_slug).

## 2026-10-22 22:19 CDT — alex-mcveigh-miller: done
- alex-mcveigh-miller: new shelf, 39 Gutenberg books, 77,993 units, 3628 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:19 CDT — florence-warden: done
- florence-warden: new shelf, 18 Gutenberg books, 34,682 units, 217 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:20 CDT — georgie-sheldon: done
- georgie-sheldon: new shelf, 18 Gutenberg books, 45,125 units, 67 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:20 CDT — luis-senarens: done
- luis-senarens: new shelf, 18 Gutenberg books, 33,145 units, 1543 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:20 CDT — st-george-rathborne: done
- st-george-rathborne: new shelf, 18 Gutenberg books, 29,677 units, 33 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:21 CDT — elinor-glyn: done
- elinor-glyn: new shelf, 18 Gutenberg books, 25,513 units, 1236 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:21 CDT — ethel-m-dell: done
- ethel-m-dell: new shelf, 18 Gutenberg books, 66,934 units, 2621 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:22 CDT — james-de-mille: done
- james-de-mille: new shelf, 17 Gutenberg books, 41,416 units, 306 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:22 CDT — f-anstey: done
- f-anstey: new shelf, 17 Gutenberg books, 25,852 units, 2674 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:22 CDT — sarah-tytler: done
- sarah-tytler: new shelf, 17 Gutenberg books, 12,957 units, 632 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:23 CDT — arthur-b-reeve: done
- arthur-b-reeve: new shelf, 16 Gutenberg books, 35,907 units, 351 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:23 CDT — alfred-henry-lewis: done
- alfred-henry-lewis: new shelf, 15 Gutenberg books, 20,708 units, 145 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:23 CDT — ruth-lamb: done
- ruth-lamb: new shelf, 17 Gutenberg books, 12,453 units, 1546 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — prentiss-ingraham: done
- prentiss-ingraham: new shelf, 17 Gutenberg books, 43,730 units, 52 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — cyrus-townsend-brady: done
- cyrus-townsend-brady: new shelf, 17 Gutenberg books, 26,856 units, 133 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — marion-ames-taggart: done
- marion-ames-taggart: new shelf, 16 Gutenberg books, 20,885 units, 9 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — randall-parrish: done
- randall-parrish: new shelf, 15 Gutenberg books, 27,234 units, 17 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — r-austin-freeman: done
- r-austin-freeman: new shelf, 16 Gutenberg books, 28,887 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — ralph-connor: done
- ralph-connor: new shelf, 15 Gutenberg books, 32,450 units, 5 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — guy-boothby: done
- guy-boothby: new shelf, 16 Gutenberg books, 22,130 units, 45 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — rolf-boldrewood: done
- rolf-boldrewood: new shelf, 16 Gutenberg books, 26,164 units, 306 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — constance-fenimore-woolson: done
- constance-fenimore-woolson: new shelf, 15 Gutenberg books, 24,823 units, 981 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — talbot-mundy: done
- talbot-mundy: new shelf, 15 Gutenberg books, 27,969 units, 1038 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — s-weir-mitchell: done
- s-weir-mitchell: new shelf, 15 Gutenberg books, 22,091 units, 485 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — helen-hunt-jackson: done
- helen-hunt-jackson: new shelf, 14 Gutenberg books, 14,725 units, 88 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — julian-hawthorne: done
- julian-hawthorne: new shelf, 15 Gutenberg books, 13,184 units, 616 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — john-habberton: done
- john-habberton: new shelf, 14 Gutenberg books, 18,744 units, 166 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:24 CDT — harold-frederic: done
- harold-frederic: new shelf, 14 Gutenberg books, 17,826 units, 136 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:25 CDT — rosa-nouchette-carey: done
- rosa-nouchette-carey: new shelf, 14 Gutenberg books, 33,129 units, 2240 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:25 CDT — john-fox-jr: done
- john-fox-jr: new shelf, 13 Gutenberg books, 10,427 units, 64 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:26 CDT — alfred-henry-lewis: Wolfville Days restored
- The post-1930 scan read the 2001 copyright on Gutenberg's own header text in an old-format file as the book's. The scan now skips Gutenberg's header and legal lines. alfred-henry-lewis: new shelf, 16 Gutenberg books, 21,941 units, 145 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:29 CDT — max-brand: done
- max-brand: new shelf, 17 Gutenberg books, 28,769 units, 206 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:29 CDT — hugh-walpole: done
- hugh-walpole: new shelf, 18 Gutenberg books, 38,378 units, 6416 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:29 CDT — anne-douglas-sedgwick: done
- anne-douglas-sedgwick: new shelf, 17 Gutenberg books, 26,119 units, 4279 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:30 CDT — nell-speed: done
- nell-speed: new shelf, 15 Gutenberg books, 19,497 units, 170 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:30 CDT — richard-dowling: done
- richard-dowling: new shelf, 16 Gutenberg books, 18,789 units, 109 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:31 CDT — louis-joseph-vance: done
- louis-joseph-vance: new shelf, 15 Gutenberg books, 36,443 units, 129 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:31 CDT — david-christie-murray: done
- david-christie-murray: new shelf, 15 Gutenberg books, 10,354 units, 109 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:31 CDT — samuel-merwin: done
- samuel-merwin: new shelf, 13 Gutenberg books, 25,279 units, 65 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:31 CDT — sydney-c-grier: done
- sydney-c-grier: new shelf, 15 Gutenberg books, 30,849 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:32 CDT — zona-gale: done
- zona-gale: new shelf, 14 Gutenberg books, 20,206 units, 76 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:32 CDT — holman-day: done
- holman-day: new shelf, 14 Gutenberg books, 36,916 units, 4417 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:32 CDT — whyte-melville: done
- whyte-melville: new shelf, 14 Gutenberg books, 20,696 units, 61 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — fred-m-white: done
- fred-m-white: new shelf, 14 Gutenberg books, 23,994 units, 392 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — laura-rountree-smith: done
- laura-rountree-smith: new shelf, 14 Gutenberg books, 8,684 units, 383 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — martin-ross: done
- martin-ross: new shelf, 14 Gutenberg books, 15,052 units, 261 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — myrtle-reed: done
- myrtle-reed: new shelf, 14 Gutenberg books, 25,115 units, 108 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — susanna-moodie: done
- susanna-moodie: new shelf, 14 Gutenberg books, 17,198 units, 13 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — thomas-a-janvier: done
- thomas-a-janvier: new shelf, 14 Gutenberg books, 4,101 units, 376 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — will-n-harben: done
- will-n-harben: new shelf, 14 Gutenberg books, 23,077 units, 2768 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — jackson-gregory: done
- jackson-gregory: new shelf, 13 Gutenberg books, 20,857 units, 48 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — george-gibbs: done
- george-gibbs: new shelf, 13 Gutenberg books, 32,909 units, 17 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — james-lane-allen: done
- james-lane-allen: new shelf, 14 Gutenberg books, 10,775 units, 1463 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — arthur-train: done
- arthur-train: new shelf, 12 Gutenberg books, 14,974 units, 741 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — garrett-p-serviss: done
- garrett-p-serviss: new shelf, 12 Gutenberg books, 19,120 units, 166 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — natalie-sumner-lincoln: done
- natalie-sumner-lincoln: new shelf, 13 Gutenberg books, 24,264 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — basil-king: done
- basil-king: new shelf, 13 Gutenberg books, 28,315 units, 1064 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — hulbert-footner: done
- hulbert-footner: new shelf, 13 Gutenberg books, 33,668 units, 1175 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — frank-t-bullen: done
- frank-t-bullen: new shelf, 13 Gutenberg books, 7,238 units, 84 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — may-agnes-fleming: done
- may-agnes-fleming: new shelf, 12 Gutenberg books, 34,149 units, 146 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:33 CDT — harold-bell-wright: done
- harold-bell-wright: new shelf, 11 Gutenberg books, 18,704 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:36 CDT — edgar-saltus: done
- edgar-saltus: new shelf, 15 Gutenberg books, 13,845 units, 230 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:36 CDT — bloundelle-burton: done
- bloundelle-burton: new shelf, 14 Gutenberg books, 20,599 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:37 CDT — arlo-bates: done
- arlo-bates: new shelf, 14 Gutenberg books, 19,984 units, 404 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:37 CDT — mary-russell-mitford: done
- mary-russell-mitford: new shelf, 13 Gutenberg books, 818 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:37 CDT — aunt-fanny: done
- aunt-fanny: new shelf, 13 Gutenberg books, 5,967 units, 235 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:37 CDT — mary-imlay-taylor: done
- mary-imlay-taylor: new shelf, 12 Gutenberg books, 19,916 units, 259 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:38 CDT — arthur-w-marchmont: done
- arthur-w-marchmont: new shelf, 12 Gutenberg books, 39,187 units, 41 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:38 CDT — maria-thompson-daviess: done
- maria-thompson-daviess: new shelf, 12 Gutenberg books, 9,649 units, 65 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:38 CDT — will-levington-comfort: done
- will-levington-comfort: new shelf, 12 Gutenberg books, 19,021 units, 69 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:39 CDT — geraldine-bonner: done
- geraldine-bonner: new shelf, 12 Gutenberg books, 21,021 units, 3855 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:39 CDT — dillon-wallace: done
- dillon-wallace: new shelf, 11 Gutenberg books, 13,161 units, 11 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:39 CDT — margaret-m-robertson: done
- margaret-m-robertson: new shelf, 11 Gutenberg books, 20,689 units, 162 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:39 CDT — george-w-peck: done
- george-w-peck: new shelf, 10 Gutenberg books, 5,606 units, 136 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:39 CDT — frances-trego-montgomery: done
- frances-trego-montgomery: new shelf, 11 Gutenberg books, 6,883 units, 6 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:39 CDT — alice-duer-miller: done
- alice-duer-miller: new shelf, 11 Gutenberg books, 12,739 units, 8 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:39 CDT — archibald-marshall: done
- archibald-marshall: new shelf, 11 Gutenberg books, 16,638 units, 40 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:39 CDT — annette-lyster: done
- annette-lyster: new shelf, 11 Gutenberg books, 10,447 units, 28 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:39 CDT — george-griffith: done
- george-griffith: new shelf, 11 Gutenberg books, 15,787 units, 134 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:39 CDT — homer-greene: done
- homer-greene: new shelf, 11 Gutenberg books, 15,025 units, 22 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:40 CDT — fanny-fern: done
- fanny-fern: new shelf, 11 Gutenberg books, 10,845 units, 151 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:40 CDT — sara-jeannette-duncan: done
- sara-jeannette-duncan: new shelf, 11 Gutenberg books, 12,338 units, 18 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:40 CDT — norman-duncan: done
- norman-duncan: new shelf, 11 Gutenberg books, 16,364 units, 66 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:40 CDT — margaret-deland: done
- margaret-deland: new shelf, 11 Gutenberg books, 16,645 units, 1302 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:40 CDT — harriet-t-comstock: done
- harriet-t-comstock: new shelf, 11 Gutenberg books, 22,281 units, 10 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:40 CDT — mary-cholmondeley: done
- mary-cholmondeley: new shelf, 11 Gutenberg books, 16,883 units, 936 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:40 CDT — hezekiah-butterworth: done
- hezekiah-butterworth: new shelf, 11 Gutenberg books, 19,439 units, 533 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:40 CDT — clara-louise-burnham: done
- clara-louise-burnham: new shelf, 11 Gutenberg books, 28,067 units, 206 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:40 CDT — charlotte-m-brame: done
- charlotte-m-brame: new shelf, 11 Gutenberg books, 20,558 units, 127 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:40 CDT — frank-norris: done
- frank-norris: new shelf, 10 Gutenberg books, 16,149 units, 1072 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:42 CDT — anne-warner: done
- anne-warner: new shelf, 10 Gutenberg books, 15,734 units, 152 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:42 CDT — amy-walton: done
- amy-walton: new shelf, 10 Gutenberg books, 8,122 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:42 CDT — eva-march-tappan: done
- eva-march-tappan: new shelf, 10 Gutenberg books, 5,989 units, 74 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:43 CDT — robert-neilson-stephens: done
- robert-neilson-stephens: new shelf, 10 Gutenberg books, 17,156 units, 14 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:43 CDT — charles-alden-seltzer: done
- charles-alden-seltzer: new shelf, 10 Gutenberg books, 16,713 units, 45 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:43 CDT — hl-sayler: done
- hl-sayler: new shelf, 10 Gutenberg books, 13,720 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:43 CDT — major-john-richardson: done
- major-john-richardson: new shelf, 10 Gutenberg books, 9,619 units, 1276 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:43 CDT — alice-hegan-rice: done
- alice-hegan-rice: new shelf, 10 Gutenberg books, 13,646 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:44 CDT — helen-leah-reed: done
- helen-leah-reed: new shelf, 10 Gutenberg books, 13,294 units, 15 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:44 CDT — opie-read: done
- opie-read: new shelf, 9 Gutenberg books, 15,087 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags; 1 failed to fetch.

## 2026-10-22 22:44 CDT — anna-chapin-ray: done
- anna-chapin-ray: new shelf, 10 Gutenberg books, 17,992 units, 8 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:44 CDT — mabel-quiller-couch: done
- mabel-quiller-couch: new shelf, 10 Gutenberg books, 9,818 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:44 CDT — j-macdonald-oxley: done
- j-macdonald-oxley: new shelf, 10 Gutenberg books, 8,372 units, 79 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — john-oxenham: done
- john-oxenham: new shelf, 10 Gutenberg books, 20,971 units, 897 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — neil-munro: done
- neil-munro: new shelf, 9 Gutenberg books, 12,334 units, 53 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — egerton-castle: done
- egerton-castle: new shelf, 10 Gutenberg books, 18,865 units, 1406 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — ada-cambridge: done
- ada-cambridge: new shelf, 10 Gutenberg books, 9,388 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — saki: done
- saki: new shelf, 9 Gutenberg books, 6,609 units, 160 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — morley-roberts: done
- morley-roberts: new shelf, 9 Gutenberg books, 11,679 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — james-payn: done
- james-payn: new shelf, 9 Gutenberg books, 7,168 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — barry-pain: done
- barry-pain: new shelf, 9 Gutenberg books, 9,416 units, 354 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — arthur-morrison: done
- arthur-morrison: new shelf, 9 Gutenberg books, 8,772 units, 1431 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — don-marquis: done
- don-marquis: new shelf, 7 Gutenberg books, 8,144 units, 39 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — henry-lawson: done
- henry-lawson: new shelf, 8 Gutenberg books, 9,466 units, 15 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — elijah-kellogg: done
- elijah-kellogg: new shelf, 9 Gutenberg books, 13,658 units, 20 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — augusta-j-evans: done
- augusta-j-evans: new shelf, 9 Gutenberg books, 24,864 units, 221 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — dane-coolidge: done
- dane-coolidge: new shelf, 9 Gutenberg books, 12,134 units, 10 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — everett-t-tomlinson: done
- everett-t-tomlinson: new shelf, 9 Gutenberg books, 15,211 units, 9 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — frank-h-spearman: done
- frank-h-spearman: new shelf, 9 Gutenberg books, 15,615 units, 18 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:45 CDT — florence-l-barclay: done
- florence-l-barclay: new shelf, 8 Gutenberg books, 12,680 units, 6 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:46 CDT — opie-read: one name-gate refusal cleared
- opie-read: new shelf, 10 Gutenberg books, 16,281 units, 67 ~2 ids; verify 0 mismatches, 0 rights flags (Up Terrapin River checks for his full name, as its Gutenberg header gives it).

## 2026-10-22 22:47 CDT — mabel-osgood-wright: done
- mabel-osgood-wright: new shelf, 9 Gutenberg books, 13,197 units, 80 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:48 CDT — frances-mary-peard: done
- frances-mary-peard: new shelf, 9 Gutenberg books, 15,508 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:48 CDT — roy-norton: done
- roy-norton: new shelf, 9 Gutenberg books, 3,441 units, 6 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:48 CDT — blanche-mcmanus: done
- blanche-mcmanus: new shelf, 9 Gutenberg books, 6,299 units, 5 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:48 CDT — anne-manning: done
- anne-manning: new shelf, 9 Gutenberg books, 8,709 units, 22 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:48 CDT — henry-leverage: done
- henry-leverage: new shelf, 9 Gutenberg books, 7,282 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:48 CDT — tc-harbaugh: done
- tc-harbaugh: new shelf, 9 Gutenberg books, 9,617 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:49 CDT — elizabeth-gordon: done
- elizabeth-gordon: new shelf, 9 Gutenberg books, 2,739 units, 299 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:49 CDT — ge-farrow: done
- ge-farrow: new shelf, 9 Gutenberg books, 8,182 units, 98 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:49 CDT — madeline-brandeis: done
- madeline-brandeis: new shelf, 4 Gutenberg books, 2,382 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:49 CDT — frederick-orin-bartlett: done
- frederick-orin-bartlett: new shelf, 9 Gutenberg books, 19,019 units, 30 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:49 CDT — charles-w-whistler: done
- charles-w-whistler: new shelf, 8 Gutenberg books, 16,054 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:49 CDT — allen-upward: done
- allen-upward: new shelf, 8 Gutenberg books, 14,748 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — catharine-parr-traill: done
- catharine-parr-traill: new shelf, 8 Gutenberg books, 5,132 units, 161 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — mabell-sc-smith: done
- mabell-sc-smith: new shelf, 8 Gutenberg books, 12,626 units, 11 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — mary-e-ropes: done
- mary-e-ropes: new shelf, 8 Gutenberg books, 4,279 units, 3 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — roger-pocock: done
- roger-pocock: new shelf, 8 Gutenberg books, 13,494 units, 1316 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — old-sleuth: done
- old-sleuth: new shelf, 8 Gutenberg books, 13,026 units, 5 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — hc-mcneile: done
- hc-mcneile: new shelf, 8 Gutenberg books, 10,532 units, 2173 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — lucy-foster-madison: done
- lucy-foster-madison: new shelf, 8 Gutenberg books, 15,071 units, 138 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — robert-leighton: done
- robert-leighton: new shelf, 8 Gutenberg books, 11,770 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — henry-herbert-knibbs: done
- henry-herbert-knibbs: new shelf, 8 Gutenberg books, 14,451 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — herbert-jenkins: done
- herbert-jenkins: new shelf, 7 Gutenberg books, 16,171 units, 873 ~2 ids; verify 0 mismatches, 0 rights flags; 1 failed to fetch.

## 2026-10-22 22:50 CDT — cutcliffe-hyne: done
- cutcliffe-hyne: new shelf, 8 Gutenberg books, 10,502 units, 7 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — thomas-w-hanshew: done
- thomas-w-hanshew: new shelf, 8 Gutenberg books, 12,450 units, 646 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — edith-k-dunton: done
- edith-k-dunton: new shelf, 8 Gutenberg books, 11,731 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — j-storer-clouston: done
- j-storer-clouston: new shelf, 8 Gutenberg books, 16,833 units, 2498 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — jos-e-badger: done
- jos-e-badger: new shelf, 8 Gutenberg books, 7,527 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:50 CDT — emily-ponsonby: done
- emily-ponsonby: new shelf, 11 Gutenberg books, 10,535 units, 138 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:51 CDT — batch 56 follow-ups
- herbert-jenkins: new shelf, 8 Gutenberg books, 18,512 units, 952 ~2 ids; verify 0 mismatches, 0 rights flags (Malcolm Sage, Detective checks for his full name, as its Gutenberg header gives it).
- madeline-brandeis: new shelf, 5 Gutenberg books, 3,246 units, 3 ~2 ids; verify 0 mismatches, 0 rights flags (Little Philippe of Belgium (copyright 1930) taken after the scan was corrected to let 1930 through).
- The post-1930 scan now treats 1930 as public domain (it had held a 1930 book); no earlier batch had held a 1930 book.

## 2026-10-22 22:55 CDT — mary-shelley-works: done
- mary-shelley-works: new shelf, 22 Gutenberg books, 15,728 units, 2677 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:55 CDT — stoker-works: done
- stoker-works: new shelf, 10 Gutenberg books, 15,338 units, 811 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:56 CDT — forster-works: done
- forster-works: new shelf, 11 Gutenberg books, 12,778 units, 263 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:56 CDT — christie-works: done
- christie-works: new shelf, 13 Gutenberg books, 31,468 units, 664 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:56 CDT — terhune-works: done
- terhune-works: new shelf, 13 Gutenberg books, 17,192 units, 15 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:56 CDT — dcfisher-works: done
- dcfisher-works: new shelf, 12 Gutenberg books, 19,433 units, 394 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:57 CDT — eggleston-works: done
- eggleston-works: new shelf, 12 Gutenberg books, 13,899 units, 1072 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:57 CDT — von-arnim-works: done
- von-arnim-works: new shelf, 15 Gutenberg books, 23,240 units, 933 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:58 CDT — william-morris-works: done
- william-morris-works: new shelf, 27 Gutenberg books, 22,226 units, 933 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:58 CDT — ev-lucas: done
- ev-lucas: new shelf, 21 Gutenberg books, 22,635 units, 736 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:59 CDT — guy-thorne: done
- guy-thorne: new shelf, 17 Gutenberg books, 28,337 units, 101 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:59 CDT — samuel-hopkins-adams: done
- samuel-hopkins-adams: new shelf, 15 Gutenberg books, 38,545 units, 6387 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:59 CDT — elizabeth-stuart-phelps: done
- elizabeth-stuart-phelps: new shelf, 15 Gutenberg books, 11,795 units, 293 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:59 CDT — owen-wister: done
- owen-wister: new shelf, 14 Gutenberg books, 14,375 units, 342 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:59 CDT — edna-ferber: done
- edna-ferber: new shelf, 13 Gutenberg books, 17,854 units, 82 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:59 CDT — ford-madox-ford: done
- ford-madox-ford: new shelf, 13 Gutenberg books, 17,172 units, 4416 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:59 CDT — kathleen-norris: done
- kathleen-norris: new shelf, 13 Gutenberg books, 25,228 units, 5735 ~2 ids; verify 0 mismatches, 0 rights flags.


## 2026-10-22 22:59 CDT — elsie-singmaster: done
- elsie-singmaster: new shelf, 11 Gutenberg books, 12,621 units, 143 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:59 CDT — edna-lyall: done
- edna-lyall: new shelf, 10 Gutenberg books, 21,825 units, 88 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:59 CDT — max-beerbohm: done
- max-beerbohm: new shelf, 11 Gutenberg books, 4,114 units, 44 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 22:59 CDT — harry-leon-wilson: done
- harry-leon-wilson: new shelf, 11 Gutenberg books, 21,059 units, 14 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:01 CDT — christie-works: records refreshed
- christie-works: new shelf, 16 Gutenberg books, 39,475 units, 664 ~2 ids; verify 0 mismatches, 0 rights flags (The Big Four, The Seven Dials Mystery and The Mysterious Mr. Quin taken: their texts carry the 1927-1930 copyright and its renewal, which is no sign of later matter).

## 2026-10-22 23:01 CDT — max-brand: records refreshed
- max-brand: new shelf, 18 Gutenberg books, 31,214 units, 206 ~2 ids; verify 0 mismatches, 0 rights flags (The Garden of Eden taken: copyright 1922, renewed 1950).

## 2026-10-22 23:03 CDT — justin-h-mccarthy: done
- justin-h-mccarthy: new shelf, 10 Gutenberg books, 10,477 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:04 CDT — robert-grant: done
- robert-grant: new shelf, 10 Gutenberg books, 9,959 units, 1256 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:04 CDT — eliza-follen: done
- eliza-follen: new shelf, 10 Gutenberg books, 2,411 units, 37 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:04 CDT — sherwood-anderson: done
- sherwood-anderson: new shelf, 10 Gutenberg books, 9,649 units, 2279 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:04 CDT — arthur-hornblow: done
- arthur-hornblow: new shelf, 8 Gutenberg books, 16,533 units, 9 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:04 CDT — arthur-colton: done
- arthur-colton: new shelf, 7 Gutenberg books, 8,429 units, 134 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:04 CDT — lewis-wingfield: done
- lewis-wingfield: new shelf, 7 Gutenberg books, 4,550 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:05 CDT — katharine-tynan: done
- katharine-tynan: new shelf, 7 Gutenberg books, 7,975 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:05 CDT — jt-trowbridge: done
- jt-trowbridge: new shelf, 7 Gutenberg books, 13,956 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:05 CDT — wc-scully: done
- wc-scully: new shelf, 7 Gutenberg books, 5,613 units, 76 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:05 CDT — leroy-scott: done
- leroy-scott: new shelf, 7 Gutenberg books, 18,367 units, 34 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:05 CDT — john-reed-scott: done
- john-reed-scott: new shelf, 7 Gutenberg books, 21,042 units, 35 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — marah-ellis-ryan: done
- marah-ellis-ryan: new shelf, 7 Gutenberg books, 16,843 units, 28 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — mary-c-rowsell: done
- mary-c-rowsell: new shelf, 7 Gutenberg books, 7,649 units, 29 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — nina-rhoades: done
- nina-rhoades: new shelf, 7 Gutenberg books, 10,348 units, 826 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — melville-davisson-post: done
- melville-davisson-post: new shelf, 7 Gutenberg books, 9,159 units, 499 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — henry-wallace-phillips: done
- henry-wallace-phillips: new shelf, 7 Gutenberg books, 5,078 units, 28 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — isabel-ostrander: done
- isabel-ostrander: new shelf, 7 Gutenberg books, 12,164 units, 65 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — ruth-ogden: done
- ruth-ogden: new shelf, 6 Gutenberg books, 4,645 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — honore-morrow: done
- honore-morrow: new shelf, 7 Gutenberg books, 18,072 units, 2139 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — louise-jordan-miln: done
- louise-jordan-miln: new shelf, 7 Gutenberg books, 12,721 units, 197 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — leonard-merrick: done
- leonard-merrick: new shelf, 7 Gutenberg books, 10,697 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — laura-jean-libbey: done
- laura-jean-libbey: new shelf, 7 Gutenberg books, 14,555 units, 17 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — edwin-lefevre: done
- edwin-lefevre: new shelf, 7 Gutenberg books, 11,027 units, 1083 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — nat-gould: done
- nat-gould: new shelf, 7 Gutenberg books, 14,811 units, 35 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — montague-glass: done
- montague-glass: new shelf, 7 Gutenberg books, 13,524 units, 7 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — wa-fraser: done
- wa-fraser: new shelf, 7 Gutenberg books, 11,308 units, 194 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — paul-leicester-ford: done
- paul-leicester-ford: new shelf, 7 Gutenberg books, 14,641 units, 18 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — richard-dehan: done
- richard-dehan: new shelf, 7 Gutenberg books, 24,370 units, 1591 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:06 CDT — ernest-bramah: done
- ernest-bramah: new shelf, 7 Gutenberg books, 9,969 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:09 CDT — marietta-holley: done
- marietta-holley: new shelf, 29 Gutenberg books, 36,102 units, 117 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:09 CDT — charles-garvice: done
- charles-garvice: new shelf, 12 Gutenberg books, 50,116 units, 70 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:09 CDT — herbert-carter: done
- herbert-carter: new shelf, 12 Gutenberg books, 16,636 units, 3 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:10 CDT — william-pitt-scargill: done
- william-pitt-scargill: new shelf, 9 Gutenberg books, 4,146 units, 618 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:10 CDT — jessie-fothergill: done
- jessie-fothergill: new shelf, 9 Gutenberg books, 15,123 units, 124 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:10 CDT — allan-pinkerton: done
- allan-pinkerton: new shelf, 7 Gutenberg books, 9,198 units, 870 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:10 CDT — f-w-bain: done
- f-w-bain: new shelf, 8 Gutenberg books, 2,138 units, 238 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:10 CDT — f-colburn-adams: done
- f-colburn-adams: new shelf, 8 Gutenberg books, 7,288 units, 3 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:10 CDT — lurana-sheldon: done
- lurana-sheldon: new shelf, 7 Gutenberg books, 6,727 units, 7 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — william-john-hopkins: done
- william-john-hopkins: new shelf, 7 Gutenberg books, 8,673 units, 1218 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — george-v-hobart: done
- george-v-hobart: new shelf, 7 Gutenberg books, 4,117 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — henry-william-herbert: done
- henry-william-herbert: new shelf, 7 Gutenberg books, 9,801 units, 352 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — l-allen-harker: done
- l-allen-harker: new shelf, 7 Gutenberg books, 12,497 units, 7 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — willis-george-emerson: done
- willis-george-emerson: new shelf, 6 Gutenberg books, 8,262 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — christabel-r-coleridge: done
- christabel-r-coleridge: new shelf, 7 Gutenberg books, 13,519 units, 44 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — heman-white-chaplin: done
- heman-white-chaplin: new shelf, 7 Gutenberg books, 1,173 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — boyd-cable: done
- boyd-cable: new shelf, 7 Gutenberg books, 6,131 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — rhoda-broughton: done
- rhoda-broughton: new shelf, 7 Gutenberg books, 16,627 units, 909 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — hjalmar-hjorth-boyesen: done
- hjalmar-hjorth-boyesen: new shelf, 7 Gutenberg books, 6,663 units, 776 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — kate-langley-bosher: done
- kate-langley-bosher: new shelf, 7 Gutenberg books, 4,766 units, 5 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — robert-montgomery-bird: done
- robert-montgomery-bird: new shelf, 7 Gutenberg books, 9,104 units, 825 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — w-l-alden: done
- w-l-alden: new shelf, 7 Gutenberg books, 3,378 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — a-d-t-whitney: done
- a-d-t-whitney: new shelf, 6 Gutenberg books, 12,126 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — brand-whitlock: done
- brand-whitlock: new shelf, 6 Gutenberg books, 11,472 units, 2575 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — frederick-whishaw: done
- frederick-whishaw: new shelf, 6 Gutenberg books, 6,597 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — george-ethelbert-walsh: done
- george-ethelbert-walsh: new shelf, 6 Gutenberg books, 3,898 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — frances-eleanor-trollope: done
- frances-eleanor-trollope: new shelf, 6 Gutenberg books, 6,723 units, 3 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:11 CDT — meadows-taylor: done
- meadows-taylor: new shelf, 6 Gutenberg books, 13,792 units, 27 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:12 CDT — netta-syrett: done
- netta-syrett: new shelf, 6 Gutenberg books, 8,590 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:13 CDT — annie-s-swan: done
- annie-s-swan: new shelf, 6 Gutenberg books, 7,942 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:13 CDT — halliwell-sutcliffe: done
- halliwell-sutcliffe: new shelf, 6 Gutenberg books, 16,108 units, 91 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:13 CDT — cynthia-stockley: done
- cynthia-stockley: new shelf, 6 Gutenberg books, 10,710 units, 974 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:13 CDT — w-pett-ridge: done
- w-pett-ridge: new shelf, 6 Gutenberg books, 7,902 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:15 CDT — eugene-manlove-rhodes: done
- eugene-manlove-rhodes: new shelf, 6 Gutenberg books, 7,514 units, 53 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:15 CDT — alfred-ollivant: done
- alfred-ollivant: new shelf, 6 Gutenberg books, 21,238 units, 1220 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:15 CDT — cleveland-moffett: done
- cleveland-moffett: new shelf, 6 Gutenberg books, 11,188 units, 5 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:15 CDT — christy-mathewson: done
- christy-mathewson: new shelf, 6 Gutenberg books, 7,201 units, 8 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:16 CDT — bessie-marchant: done
- bessie-marchant: new shelf, 6 Gutenberg books, 9,535 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:16 CDT — lucas-malet: done
- lucas-malet: new shelf, 6 Gutenberg books, 11,194 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:16 CDT — charles-major: done
- charles-major: new shelf, 6 Gutenberg books, 11,469 units, 48 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:16 CDT — william-magnay: done
- william-magnay: new shelf, 6 Gutenberg books, 11,824 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:16 CDT — s-levett-yeats: done
- s-levett-yeats: new shelf, 6 Gutenberg books, 9,518 units, 5 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:16 CDT — ada-leverson: done
- ada-leverson: new shelf, 6 Gutenberg books, 12,101 units, 25 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — frederic-arnold-kummer: done
- frederic-arnold-kummer: new shelf, 6 Gutenberg books, 7,222 units, 4 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — vaughan-kester: done
- vaughan-kester: new shelf, 5 Gutenberg books, 16,422 units, 116 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — florence-finch-kelly: done
- florence-finch-kelly: new shelf, 6 Gutenberg books, 6,617 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — frederic-stewart-isham: done
- frederic-stewart-isham: new shelf, 6 Gutenberg books, 12,340 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — bracebridge-hemyng: done
- bracebridge-hemyng: new shelf, 6 Gutenberg books, 19,183 units, 72 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — l-p-gratacap: done
- l-p-gratacap: new shelf, 6 Gutenberg books, 5,294 units, 48 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — tom-gallon: done
- tom-gallon: new shelf, 6 Gutenberg books, 10,651 units, 25 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — izola-l-forrester: done
- izola-l-forrester: new shelf, 6 Gutenberg books, 8,047 units, 3 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — leo-edwards: done
- leo-edwards: new shelf, 6 Gutenberg books, 10,562 units, 12 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — paul-laurence-dunbar: done
- paul-laurence-dunbar: new shelf, 6 Gutenberg books, 7,668 units, 137 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — l-dougall: done
- l-dougall: new shelf, 6 Gutenberg books, 9,529 units, 2257 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — a-d-crake: done
- a-d-crake: new shelf, 6 Gutenberg books, 14,094 units, 212 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — bertha-m-clay: done
- bertha-m-clay: new shelf, 6 Gutenberg books, 12,276 units, 71 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — george-randolph-chester: done
- george-randolph-chester: new shelf, 6 Gutenberg books, 10,693 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — charles-w-chesnutt: done
- charles-w-chesnutt: new shelf, 6 Gutenberg books, 6,512 units, 242 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:17 CDT — percy-james-brebner: done
- percy-james-brebner: new shelf, 6 Gutenberg books, 15,065 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:18 CDT — l-adams-beck: done
- l-adams-beck: new shelf, 6 Gutenberg books, 9,582 units, 109 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:18 CDT — jane-barlow: done
- jane-barlow: new shelf, 6 Gutenberg books, 2,879 units, 134 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:19 CDT — willis-boyd-allen: done
- willis-boyd-allen: new shelf, 6 Gutenberg books, 4,844 units, 108 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:19 CDT — deborah-alcock: done
- deborah-alcock: new shelf, 5 Gutenberg books, 9,814 units, 651 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:19 CDT — walter-aimwell: done
- walter-aimwell: new shelf, 6 Gutenberg books, 6,297 units, 119 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:19 CDT — albert-w-aiken: done
- albert-w-aiken: new shelf, 6 Gutenberg books, 7,904 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:19 CDT — grace-aguilar: done
- grace-aguilar: new shelf, 6 Gutenberg books, 8,208 units, 555 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:19 CDT — andy-adams: done
- andy-adams: new shelf, 6 Gutenberg books, 4,020 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:19 CDT — william-allen-white: done
- william-allen-white: new shelf, 5 Gutenberg books, 6,315 units, 15 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — stanley-waterloo: done
- stanley-waterloo: new shelf, 5 Gutenberg books, 3,975 units, 101 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — c-c-waddell: done
- c-c-waddell: new shelf, 5 Gutenberg books, 5,956 units, 30 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — metta-victoria-fuller-victor: done
- metta-victoria-fuller-victor: new shelf, 5 Gutenberg books, 4,518 units, 51 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — s-s-van-dine: done
- s-s-van-dine: new shelf, 5 Gutenberg books, 13,459 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — d-f-e-sykes: done
- d-f-e-sykes: new shelf, 5 Gutenberg books, 5,347 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — arthur-d-howden-smith: done
- arthur-d-howden-smith: new shelf, 5 Gutenberg books, 14,996 units, 8 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — william-gilmore-simms: done
- william-gilmore-simms: new shelf, 5 Gutenberg books, 7,958 units, 147 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — douglass-sherley: done
- douglass-sherley: new shelf, 5 Gutenberg books, 492 units, 25 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — george-w-m-reynolds: done
- george-w-m-reynolds: new shelf, 5 Gutenberg books, 38,087 units, 74 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — baillie-reynolds: done
- baillie-reynolds: new shelf, 5 Gutenberg books, 13,659 units, 371 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — arthur-j-rees: done
- arthur-j-rees: new shelf, 5 Gutenberg books, 10,161 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — herbert-quick: done
- herbert-quick: new shelf, 5 Gutenberg books, 7,675 units, 33 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — margaret-horton-potter: done
- margaret-horton-potter: new shelf, 5 Gutenberg books, 9,528 units, 42 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — marmaduke-william-pickthall: done
- marmaduke-william-pickthall: new shelf, 5 Gutenberg books, 6,642 units, 412 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — edward-parrott: done
- edward-parrott: new shelf, 5 Gutenberg books, 6,404 units, 5 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — w-h-h-murray: done
- w-h-h-murray: new shelf, 5 Gutenberg books, 1,414 units, 70 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — favell-lee-mortimer: done
- favell-lee-mortimer: new shelf, 5 Gutenberg books, 2,462 units, 26 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:20 CDT — w-c-morrow: done
- w-c-morrow: new shelf, 5 Gutenberg books, 5,101 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:22 CDT — margaret-warner-morley: done
- margaret-warner-morley: new shelf, 5 Gutenberg books, 5,071 units, 11 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:22 CDT — philip-verrill-mighels: done
- philip-verrill-mighels: new shelf, 5 Gutenberg books, 9,690 units, 23 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:22 CDT — margaret-hill-mccarter: done
- margaret-hill-mccarter: new shelf, 5 Gutenberg books, 10,312 units, 614 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:22 CDT — katherine-mansfield: done
- katherine-mansfield: new shelf, 5 Gutenberg books, 5,289 units, 117 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:22 CDT — julia-magruder: done
- julia-magruder: new shelf, 5 Gutenberg books, 4,494 units, 9 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:22 CDT — james-m-ludlow: done
- james-m-ludlow: new shelf, 5 Gutenberg books, 7,360 units, 110 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:22 CDT — frances-little: done
- frances-little: new shelf, 5 Gutenberg books, 2,473 units, 2 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:22 CDT — ottilie-a-liljencrantz: done
- ottilie-a-liljencrantz: new shelf, 5 Gutenberg books, 6,213 units, 12 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:23 CDT — thomas-dick-lauder: done
- thomas-dick-lauder: new shelf, 5 Gutenberg books, 7,779 units, 354 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:23 CDT — eleanor-m-ingram: done
- eleanor-m-ingram: new shelf, 5 Gutenberg books, 7,549 units, 38 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:23 CDT — hubback: done
- hubback: new shelf, 5 Gutenberg books, 10,803 units, 1762 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:23 CDT — william-hope-hodgson: done
- william-hope-hodgson: new shelf, 5 Gutenberg books, 6,021 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:23 CDT — corra-harris: done
- corra-harris: new shelf, 5 Gutenberg books, 3,936 units, 217 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — arthur-preston-hankins: done
- arthur-preston-hankins: new shelf, 5 Gutenberg books, 9,303 units, 11 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — grace-greenwood: done
- grace-greenwood: new shelf, 5 Gutenberg books, 2,590 units, 258 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — charles-gilson: done
- charles-gilson: new shelf, 5 Gutenberg books, 7,302 units, 3 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — jacques-futrelle: done
- jacques-futrelle: new shelf, 5 Gutenberg books, 6,260 units, 2359 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — henry-blake-fuller: done
- henry-blake-fuller: new shelf, 5 Gutenberg books, 7,710 units, 1177 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — m-e-francis: done
- m-e-francis: new shelf, 5 Gutenberg books, 9,521 units, 373 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — w-bert-foster: done
- w-bert-foster: new shelf, 5 Gutenberg books, 8,243 units, 1 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — george-allan-england: done
- george-allan-england: new shelf, 5 Gutenberg books, 14,407 units, 119 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — finley-peter-dunne: done
- finley-peter-dunne: new shelf, 5 Gutenberg books, 2,276 units, 58 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — alfred-w-drayson: done
- alfred-w-drayson: new shelf, 5 Gutenberg books, 4,248 units, 21 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — emma-c-dowd: done
- emma-c-dowd: new shelf, 5 Gutenberg books, 11,089 units, 7 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — francis-worcester-doughty: done
- francis-worcester-doughty: new shelf, 5 Gutenberg books, 9,171 units, 16 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — maud-diver: done
- maud-diver: new shelf, 5 Gutenberg books, 15,638 units, 4509 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — george-cupples: done
- george-cupples: new shelf, 5 Gutenberg books, 1,292 units, 10 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — stephen-angus-douglas-cox: done
- stephen-angus-douglas-cox: new shelf, 5 Gutenberg books, 4,853 units, 3 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:24 CDT — george-waldo-browne: done
- george-waldo-browne: new shelf, 5 Gutenberg books, 7,190 units, 17 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:26 CDT — earl-derr-biggers: done
- earl-derr-biggers: new shelf, 5 Gutenberg books, 9,497 units, 0 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:28 CDT — storytellers-tail-01: done
- storytellers-tail-01: new shelf, 94 Gutenberg books, 143,415 units, 6977 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:28 CDT — storytellers-tail-02: done
- storytellers-tail-02: new shelf, 96 Gutenberg books, 127,242 units, 4331 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:29 CDT — storytellers-tail-03: done
- storytellers-tail-03: new shelf, 77 Gutenberg books, 103,326 units, 5815 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:32 CDT — storytellers-tail-04: done
- storytellers-tail-04: new shelf, 66 Gutenberg books, 74,741 units, 5222 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:33 CDT — storytellers-tail-05: done
- storytellers-tail-05: new shelf, 66 Gutenberg books, 85,604 units, 315 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:36 CDT — storytellers-tail-06: done
- storytellers-tail-06: new shelf, 64 Gutenberg books, 94,740 units, 5552 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:36 CDT — storytellers-tail-07: done
- storytellers-tail-07: new shelf, 64 Gutenberg books, 113,868 units, 1191 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:36 CDT — storytellers-tail-08: done
- storytellers-tail-08: new shelf, 66 Gutenberg books, 128,442 units, 4352 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:36 CDT — storytellers-tail-09: done
- storytellers-tail-09: new shelf, 51 Gutenberg books, 74,558 units, 3116 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:38 CDT — storytellers-tail-10: done
- storytellers-tail-10: new shelf, 54 Gutenberg books, 76,550 units, 3823 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:39 CDT — storytellers-tail-11: done
- storytellers-tail-11: new shelf, 54 Gutenberg books, 71,939 units, 1496 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:40 CDT — storytellers-tail-12: done
- storytellers-tail-12: new shelf, 54 Gutenberg books, 68,669 units, 1624 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:41 CDT — storytellers-tail-13: done
- storytellers-tail-13: new shelf, 54 Gutenberg books, 76,672 units, 331 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:41 CDT — storytellers-tail-14: done
- storytellers-tail-14: new shelf, 54 Gutenberg books, 79,150 units, 2123 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:41 CDT — storytellers-tail-15: done
- storytellers-tail-15: new shelf, 52 Gutenberg books, 66,092 units, 2513 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:41 CDT — storytellers-tail-16: done
- storytellers-tail-16: new shelf, 54 Gutenberg books, 79,629 units, 6225 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:41 CDT — storytellers-tail-17: done
- storytellers-tail-17: new shelf, 29 Gutenberg books, 36,320 units, 338 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:43 CDT — storytellers-tail-18: done
- storytellers-tail-18: new shelf, 30 Gutenberg books, 35,985 units, 1725 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:43 CDT — storytellers-tail-19: done
- storytellers-tail-19: new shelf, 30 Gutenberg books, 30,851 units, 2096 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:44 CDT — storytellers-tail-20: done
- storytellers-tail-20: new shelf, 30 Gutenberg books, 40,756 units, 2808 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:45 CDT — storytellers-tail-21: done
- storytellers-tail-21: new shelf, 30 Gutenberg books, 26,902 units, 798 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:46 CDT — storytellers-tail-22: done
- storytellers-tail-22: new shelf, 30 Gutenberg books, 32,008 units, 1389 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:46 CDT — storytellers-tail-23: done
- storytellers-tail-23: new shelf, 30 Gutenberg books, 31,156 units, 2046 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:46 CDT — storytellers-tail-24: done
- storytellers-tail-24: new shelf, 30 Gutenberg books, 26,621 units, 563 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:46 CDT — storytellers-tail-25: done
- storytellers-tail-25: new shelf, 30 Gutenberg books, 37,418 units, 1751 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:46 CDT — storytellers-tail-26: done
- storytellers-tail-26: new shelf, 30 Gutenberg books, 38,974 units, 455 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:46 CDT — storytellers-tail-27: done
- storytellers-tail-27: new shelf, 30 Gutenberg books, 34,233 units, 1376 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:46 CDT — storytellers-tail-28: done
- storytellers-tail-28: new shelf, 30 Gutenberg books, 34,553 units, 888 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:46 CDT — storytellers-tail-29: done
- storytellers-tail-29: new shelf, 29 Gutenberg books, 32,793 units, 1019 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:48 CDT — storytellers-tail-30: done
- storytellers-tail-30: new shelf, 30 Gutenberg books, 30,825 units, 3419 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:48 CDT — storytellers-tail-31: done
- storytellers-tail-31: new shelf, 30 Gutenberg books, 44,844 units, 154 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:49 CDT — storytellers-tail-32: done
- storytellers-tail-32: new shelf, 29 Gutenberg books, 41,187 units, 1733 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:50 CDT — storytellers-tail-33: done
- storytellers-tail-33: new shelf, 30 Gutenberg books, 31,889 units, 1864 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:50 CDT — storytellers-tail-34: done
- storytellers-tail-34: new shelf, 29 Gutenberg books, 31,915 units, 174 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:51 CDT — storytellers-tail-35: done
- storytellers-tail-35: new shelf, 30 Gutenberg books, 38,531 units, 346 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:52 CDT — storytellers-tail-36: done
- storytellers-tail-36: new shelf, 30 Gutenberg books, 29,606 units, 284 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:52 CDT — storytellers-tail-37: done
- storytellers-tail-37: new shelf, 30 Gutenberg books, 36,457 units, 1761 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:53 CDT — storytellers-tail-38: done
- storytellers-tail-38: new shelf, 29 Gutenberg books, 33,908 units, 467 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:54 CDT — storytellers-tail-39: done
- storytellers-tail-39: new shelf, 30 Gutenberg books, 34,637 units, 765 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:54 CDT — storytellers-tail-40: done
- storytellers-tail-40: new shelf, 30 Gutenberg books, 31,710 units, 1562 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:54 CDT — storytellers-tail-41: done
- storytellers-tail-41: new shelf, 30 Gutenberg books, 27,960 units, 712 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:54 CDT — storytellers-tail-42: done
- storytellers-tail-42: new shelf, 30 Gutenberg books, 34,359 units, 3511 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:54 CDT — storytellers-tail-43: done
- storytellers-tail-43: new shelf, 30 Gutenberg books, 37,365 units, 1035 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:54 CDT — storytellers-tail-44: done
- storytellers-tail-44: new shelf, 30 Gutenberg books, 36,413 units, 1492 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:54 CDT — storytellers-tail-45: done
- storytellers-tail-45: new shelf, 30 Gutenberg books, 29,343 units, 984 ~2 ids; verify 0 mismatches, 0 rights flags.

## 2026-10-22 23:54 CDT — storytellers-tail-46: done
- storytellers-tail-46: new shelf, 30 Gutenberg books, 31,120 units, 875 ~2 ids; verify 0 mismatches, 0 rights flags.
