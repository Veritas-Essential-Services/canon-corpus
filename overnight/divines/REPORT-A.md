# Lane A (Divines) — append-only log

## 2026-10-02 15:17 CDT — flavel: done
- Vault not reachable from the cloud; worked from the repo only (noted once).
- Shelf `pipeline/flavel_shelf.json`: 5 CCEL + 6 Internet Archive (1820 Whole Works, complete set `wholeworksofjohn01..06flav`, each id resolved and title/volume checked). `flavel-fountain` listed under `_held`, not refetched. No Gutenberg Flavel exists.
- Fetched 11/11 via `pipeline/fetch_shelf.py flavel` (lane B's generalised fetcher; added an optional `_held` key to my shelf, which the fetcher ignores). 12.1 MB IA OCR (1.83M words), 3.6 MB CCEL ThML.
- New file `pipeline/convert_shelf.py <shelf>`: runs the existing `convert_thml` on a shelf's CCEL items into gitignored `data/books/`, prints stats, never writes the committed manifest. Flavel CCEL: 4,622 units, 1,895 units with links, 4,361 scripture links. IA OCR stays raw.
- `tests/structure_test.py`: baseline 64 passed / 0 failed; unchanged after.
- Awaiting uid minting (Adam's attended pass): all 11 flavel slugs.
- Pending/wishlist in the map: a second 1820 scan (U. Toronto), 1701/1716/1762/1770/1799 editions, Gaelic 1879 translation. Excluded: modern reprints 1930–2017, and seven same-name non-Flavel authors.

## 2026-10-02 15:18 CDT — bunyan: done
- Shelf `pipeline/bunyan_shelf.json`. Collected Works = Offor 1854 (3 vols) from Gutenberg as clean text (PG 6046-6048; PG 6049 is the same in one file, not fetched). Plus PG singles 3270, 3548, 3613, 3614, 13750 and CCEL badman, grace, miscellaneous. `bunyan-pilgrim`, `bunyan-holy_war` listed under `_held`. All PG headers checked: none carry the COPYRIGHTED marker.
- Fetched 11/11 (12.3 MB Offor, 2.2M words). CCEL converted: 1,400 units, 501 scripture links. Offor stays unstructured (it is one file per volume of ~60 treatises; a splitter is a wishlist item).
- Defects for Adam: CCEL `miscellaneous` and PG 3613 are probably the same pieces; *An Exhortation to Peace and Unity* is of doubted authorship.
- Four titles not found under their usual names in Offor (Relation of the Imprisonment, Profitable Meditations, Vindication of Some Gospel Truths, the Map of salvation) — marked pending/to confirm in the map.
- structure_test 64/64. Awaiting uid minting: all 11 bunyan slugs.

## 2026-10-02 15:37 CDT — ryle: done; fetch_shelf.py identity check added
- Shelf `pipeline/ryle_shelf.json`: 3 CCEL, 3 Gutenberg, 36 Internet Archive. Expository Thoughts assembled from single lifetime volumes, each identified by the chapter range of its own section headings (Matthew from CCEL; Mark 1863; Luke 1-10, Luke 11-24 1862; John 1-6 1866, John 7-12, John 13-21). 42/42 fetched, 22.3 MB. CCEL converted: 4,157 units, 1,604 scripture links.
- **fetch_shelf.py change (asked by the coordinator after a review):** the title check only recorded, never refused. Added `check_identity`: title words are now looked for in the whole text, and a scan with none of the title words anywhere, or (when the shelf sets `_name_words`) no author name anywhere, is REFUSED as MISMATCH and never written. Partial title matches are kept and flagged `title_weak`. Parenthetical notes in a shelf title are no longer used as check words. New `--verify` mode re-checks files already on disk. Backward compatible: shelves without `_name_words` skip the author test.
- Re-verified every file already fetched: flavel 11/11, bunyan 11/11 clean. Ryle: 2 tracts (Worldly Conformity, A Call to Prayer) never name Ryle in their text; removed from the shelf to `_pending`. 3 flagged `title_weak` and kept (Home Truths 1859, Are You Forgiven?, Do You Pray?: OCR lost the title page; content checked by counts).
- CCEL defect: CCEL's `twobears` XML is empty (402 bytes); the 1869 IA scan is held instead.
- structure_test 64/64. Awaiting uid minting: all 42 ryle slugs.

## 2026-10-02 15:43 CDT — horatius-bonar: done
- Shelf `pipeline/horatius-bonar_shelf.json`, prose only. 24 fetched (CCEL God's Way of Peace, The Rent Veil; 22 IA lifetime printings), 12.4 MB. CCEL converted: 574 units, 135 scripture links.
- The new identity check refused 4 scans whose OCR never names Bonar (God's Way of Holiness, Kelso Tracts, Redeem the Time, Light and Truth OT); moved to `_pending`.
- CCEL defect: Follow the Lamb, How Shall I Go to God and Words to Winners of Souls are listed on CCEL's Bonar page but their XML is not served (an error page). Two are held from IA instead.
- Hymn collections listed as "see hymn manifest". Awaiting uid minting: all 24 slugs.
