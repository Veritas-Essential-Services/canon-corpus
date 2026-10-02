# Lane B (Classical (English translations)) — append-only log

## 2026-10-02 15:17 CDT — plato-jowett: done
- Vault not reachable from the cloud; worked from the repo (noted once).
- Created `pipeline/fetch_shelf.py` (generalised fetch_edwards.py; adds the Gutenberg COPYRIGHTED gate and refuses 404 pages served as 200).
- Shelf `pipeline/plato_shelf.json`: 29 Gutenberg dialogues (all of Jowett's 3rd ed.) + IA `b24750189_0001..0005` (1892 Clarendon, raw OCR). 34 of 34 fetched (29 PG dialogues, 5 IA vols of the 1892 Clarendon set), 16.6 MB. Trial conversion of the PG texts with convert_gutenberg_prose: 22,162 paragraph units, 1.5M words. Not added to the build manifest (fetch_sources.py is off-limits during the burst) and not minted. No Stephanus numbers in the PG texts; IA set is raw OCR.
- Finding: Alcibiades II and Eryxias were translated by Jowett's secretary Matthew Knight, not Jowett; recorded per title.
- Baseline: tests/structure_test.py 64 passed before and after.
- Awaits minting: all 29 plato-* slugs (+ the 5 raw volumes if Adam wants them addressable).

## 2026-10-02 15:22 CDT — aristotle-ross: done-with-defects
- Shelf `pipeline/aristotle_shelf.json`. 10 Oxford volumes (I, II, IV-XI) + Hammond 1902 De Anima/Parva Naturalia gap-fill fetched as raw IA OCR, 12.0 MB, ~2.0M words, clean-word ratio 0.81-0.89 per volume. Vol. III (1931) and XII (1952) pending on rights. meteorologica00aris fetched then removed: it is all of vol. III (contains the 1931 De Anima).
- Defects: raw OCR only; vol. III and XII missing (rights); Bekker margins survive in vols. VIII–XI (hundreds of matches) but hardly at all in I–VII.
- Finding: the IA item `meteorologica00aris` is mis-catalogued; check sub-title pages, not IA metadata, before trusting a "separate issue".
- Awaits minting: 11 aristotle-* slugs, once Adam decides whether raw volumes get uids.

## 2026-10-02 15:23 CDT — hesiod: done
- Shelf `pipeline/hesiod_shelf.json`. PG 348 fetched (548 KB). Trial conversion: 1,491 paragraph units, 90.5K words; 510 inline '(ll. N)' line references available for a finer scheme later. Not minted.

## 2026-10-02 15:25 CDT — ovid: done
- Shelf `pipeline/ovid_shelf.json`. 9/9 fetched, 7.5 MB: Riley prose for the whole corpus (6 clean PG texts + 2 Bohn volumes raw), Howard 1807 and Golding 1567 Metamorphoses. Trial conversion of PG texts: 4,610 paragraph units. Dryden titles cross-referenced to lane C's slugs. PG 21920 refused (copyrighted). Not minted.
- Raw OCR clean-word ratios: Golding 0.95, Riley Fasti 0.91, Riley Heroides 0.88.

## 2026-10-02 15:28 CDT — virgil: done
- Shelf `pipeline/virgil_shelf.json`. 10/10 fetched, 5.8 MB: Rhoades and Conington each complete (clean PG + raw IA), plus Aeneids by Mackail, Morris, Taylor, Humphries and Mackail's Eclogues/Georgics. Trial conversion: verse texts 3,135 units via convert_gutenberg_verse (divres recorded in the shelf), Conington/Mackail Aeneid prose 1,714. PG 230's translator identified as Rhoades by collation. Dryden cross-referenced. Not minted.
- Added `_convert_hints` (divre + trial units) to the virgil and ovid shelves so the eventual manifest entries need no rediscovery.

## 2026-10-02 15:30 CDT — overflow-perseus: done
- Census only (no fetch: the pipeline needs a PERSEUS entry in fetch_sources.py). Scaife catalogue: 923 English greekLit/latinLit texts, 82 authors; 3 in build, 34 same translation held, 54 author-shelf, 832 gap (625 likely US PD). docs/perseus-census.md + .csv, pipeline/perseus_census.py. Finding: Williams's Aeneid is already in the build (aeneid-williams); Virgil map corrected.
- GitHub API and zip downloads for PerseusDL are blocked from cloud threads (403); raw file URLs and the Scaife catalogue work.
