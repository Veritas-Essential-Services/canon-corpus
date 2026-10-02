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
