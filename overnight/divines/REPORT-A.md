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

## 2026-10-02 15:45 CDT — andrew-bonar: done
- Shelf `pipeline/andrew-bonar_shelf.json`: 2 Gutenberg (M'Cheyne Memoir; Rutherford's Letters ed. Bonar), 15 IA. 17/17 fetched, 13.3 MB, identity check clean. No CCEL Andrew Bonar exists.
- Same-name diligence: Andrew Redman Bonar (1818-1867) wrote several IA-catalogued books (Incidents of Missionary Enterprise, Life of Wellington, Hymns for Christian Families); all excluded.
- Rutherford editions are shelved as "ed. Bonar"; Adam may prefer them on a Rutherford shelf instead: his call.
- Awaiting uid minting: all 17 slugs.

## 2026-10-02 15:46 CDT — saphir: done
- Shelf `pipeline/saphir_shelf.json`: 11 IA items, 7.1 MB, identity check clean. No CCEL or Gutenberg Saphir exists.
- Includes Auberlen's Daniel and Revelation (Saphir as translator) and Carlyle's 1893 memoir (about him). Christ and Israel (1911) is posthumous, ed. David Baron, PD.
- Pending: Christ and the Scriptures (IA text file under a non-standard name); Jesus and the Sinner (1851): IA credits Saphir, but he was 20 and a student; authorship unconfirmed, so not shelved.
- Awaiting uid minting: all 11 slugs.

## 2026-10-02 15:48 CDT — edwards-gaps: done
- Audited IA (236 Edwards items 1700-1930) and Gutenberg against `edwards_shelf.json`. Most IA items are other printings of works the shelf already holds. Six verified gaps added: Religious Affections first edition (1746), Edwards's own Brainerd (1749), Freedom of the Will 1762 (1754 first edition not on IA), Erskine's Edinburgh selections from the manuscripts (1793, 1796), Hopkins's Life of Edwards (1804). Fetched, 4.8 MB.
- Two more first editions (Distinguishing Marks 1741, Humble Attempt 1747) are refused by the identity check because long-s OCR never yields "Edwards"; listed pending for a look by eye.
- The shelf now sets `_name_words: [edwards, jonathan]`, so future fetch_shelf.py runs check author identity for Edwards too. `fetch_edwards.py` still reads the shelf unchanged.
- Awaiting uid minting: the 6 new slugs.

## 2026-10-02 15:49 CDT — overflow-summa: done (census, no new shelf)
- Counted questions in the four Gutenberg Summa files and CCEL's full summa.xml. Repo coverage is complete: I 119/119, I-II 114/114, II-II 189/189, III 90/90 (adler_shelf.json), Supplement 99/99 + Appendix (ingest_summa_supplement.py from CCEL). No missing part, so no shelf was written.
- Defects: three treatise-opening questions in the Gutenberg text lack their "QUESTION n" heading line (I 116, I-II 1, II-II 183); the Supplement is not a row in adler_shelf.json. Written into the map section.

## 2026-10-02 15:51 CDT — pending sweep (queue item pending-sweep-1, added under RULES §5)
- `fetch_shelf.py`: an internet_archive row may now carry a third element, the item's text file name, for uploads whose text is not `<id>_djvu.txt`. Backward compatible (two-element rows unchanged).
- Fetched 4 items that were pending for that reason: Redemption Drawing Nigh (A. Bonar), A Stranger Here and Light and Truth: Old Testament (H. Bonar), A Call to Prayer (Ryle, a second scan that names him). Saphir's Christ and the Scriptures was refused by the identity check and stays pending.

## 2026-10-02 15:51 CDT — finding: OCR quality of lane A's raw Internet Archive text (RULES §5d)
- Method: share of word tokens (2+ letters) found in a vocabulary built from this lane's clean CCEL and Gutenberg texts (26 files, 23,477 words seen twice or more). A rough proxy: proper names and Greek/Hebrew lower it without being errors. Covers the 100 IA items fetched in this cloud session (Edwards's 31 older IA items are not on this machine).
- Spread: 50 items at 97% or better, 28 at 95-97%, 15 at 90-95%, 7 below 90%. Median 97.0%.
- Per author (median): andrew-bonar 97.2% (n=16), edwards 80.2% (n=6), flavel 96.4% (n=6), horatius-bonar 96.6% (n=24), ryle 97.4% (n=37), saphir 97.4% (n=11)
- Worst: the six 18th-century Edwards printings added by the gap audit (77-83%): long-s type read as f. These need a better text before anyone quotes from them; the Dwight/Worcester texts of the same works are the better reading copies. Next: H. Bonar's travel books (90-94%), lowered mostly by Near Eastern place names, not errors.
- Lowest 10: edwards-hopkins-life-1804 76.8%; edwards-brainerd-1749 77.6%; edwards-freedom-will-1762 79.7%; edwards-affections-1746 80.7%; edwards-misc-observations-1793 82.4%; edwards-remarks-controversies-1796 83.2%; hbonar-desert-of-sinai 89.9%; hbonar-land-of-promise 92.0%; ryle-what-good-will-it-do 92.6%; abonar-mission-to-jews 93.1%

## 2026-10-02 15:55 CDT — finding: can Offor's Bunyan be split into one unit per treatise? (RULES §5d)
- Vol. 1 (PG 6046): yes, cleanly. It prints a contents list of 21 items (memoir + 20 works), and every one of them appears in the body as a heading preceded by three blank lines; nothing else in the volume matches that pattern. A splitter can key on the contents list.
- Vols 2-3 (PG 6047-6048): not by a single rule. No contents list; the usual layout is title block, "BY JOHN BUNYAN" byline, then "ADVERTISEMENT BY THE EDITOR", but blank-line spacing varies, several works lack a byline, and footnote blocks and in-work headings look like titles. An automatic pass found about 60% of the work boundaries. A splitter for these volumes needs a hand-made anchor list (one title line per work), kept as a per-book rule so it reruns on refetch (rule 2). Roughly 45 works across the two volumes.
- No converter was written: the unit-id scheme for a split Offor is a citation-spine decision (rule 3) and belongs to Adam. The wishlist line in the map stands.

## 2026-10-02 15:55 CDT — session end
- Queue A drained: flavel, bunyan, ryle, horatius-bonar, andrew-bonar, saphir, edwards-gaps, overflow-summa all done; pending-sweep-1 added and done. 126 items fetched (about 93 MB, gitignored), 7 shelves written or extended, 0 uids minted.
- Shared code touched: `pipeline/fetch_shelf.py` (identity check, `--verify`, explicit IA file name; all backward compatible); new `pipeline/convert_shelf.py`. `structure_texts.py`, `fetch_sources.py` and `data/uids/` untouched. structure_test 64/64 at start and end.
- For the next lane-A worker: nothing is left in the queue. Useful next steps, in order: (1) look by eye at the `_pending` items each shelf lists as refused by the identity check; (2) a hand-made anchor list for Offor vols 2-3, if Adam rules on a unit-id scheme for split treatises; (3) better scans for the six long-s Edwards printings. Lock released.

## 2026-10-02 16:02 CDT — round 2 reopened; owen done
- Coordinator relay: keep going to the stop time with eleven default Divines (Owen, Sibbes, Baxter, Watson, Brooks, Goodwin, Rutherford, M'Cheyne prose, Matthew Henry, Calvin in CTS English, Spurgeon). Added to QUEUE-A; each gets a DIGEST-A line for Adam's veto. Lock re-taken.
- owen: `pipeline/owen_shelf.json`. 27 CCEL works fetched and converted (23,432 units, 20,976 links in total; `owen-poema` is only 4 units). The four CCEL titles already in `fetch_sources.py` are listed under `_held`, not refetched. Goold's Works, all 24 volumes, fetched as raw IA OCR (about 82 MB with the CCEL files). Volume numbers were read off title-page OCR because IA metadata numbers several Toronto scans wrongly (e.g. `owensworks04owenuoft` is Goold vol. 21). `--verify`: 0 mismatched, 0 title_weak. 0 uids minted.

## 2026-10-02 16:03 CDT — sibbes done
- `pipeline/sibbes_shelf.json`: Grosart's Complete Works, all 7 volumes, raw IA OCR (Toronto scans, about 16 MB). `--verify`: 0 mismatched. A second scan of the same set is listed as an alternate.
- CCEL: `ccel.org/ccel/s/sibbes` (and `s/sibbs`) did not resolve to an author page, and the work URLs probed served HTML, not ThML. Nothing taken from CCEL; recorded so the next worker does not re-probe blindly. No Gutenberg Sibbes. 0 uids minted.

## 2026-10-02 16:07 CDT — watson done
- `pipeline/watson_shelf.json`: 6 CCEL titles fetched and converted (5,867 units, 8,024 links), 2 IA items raw (about 9.8 MB in all). `--verify`: 0 mismatched. No Gutenberg Watson.
- Pending: four treatises found only in 1660s-1780s printings. A title count in the Select Works OCR was inconclusive (generic words), so they stay pending rather than being claimed as held. 0 uids minted.

## 2026-10-02 16:08 CDT — baxter done
- `pipeline/baxter_shelf.json`: 4 CCEL titles converted (1,275 units, 214 links: these CCEL editions carry little scripRef markup), Gutenberg's Christian Directory in 4 parts (rights lines passed the fetcher's gate), and Orme's Practical Works, all 23 volumes, raw IA OCR (about 48 MB in all). No single IA scan series is complete; the set is assembled from four series, each volume read off its title page. `--verify`: 0 mismatched.
- Dropped: CCEL `baxter/practical` turned out to be a stub (about 8.5 KB of text under 965 empty paragraphs); it is recorded under `_excluded` and its file deleted. 0 uids minted.

## 2026-10-02 16:09 CDT — brooks done
- `pipeline/brooks_shelf.json`: Grosart's Complete Works, all 6 volumes, raw IA OCR (Toronto scans, volume numbers read off title pages). `--verify`: 0 mismatched. CCEL `ccel/brooks` returned 404; no Gutenberg Brooks. 0 uids minted.

## 2026-10-02 16:13 CDT — goodwin done
- `pipeline/goodwin_shelf.json`: Nichol's Works, all 12 volumes, raw IA OCR. `--verify`: 0 mismatched.
- Name traps recorded under `_excluded`: Gutenberg's only "Thomas Goodwin" (PG 52639, Moses and Aaron) is the schoolmaster who died in 1642, and CCEL's `goodwin` is William Watson Goodwin's Greek Grammar. 0 uids minted.

## 2026-10-02 16:15 CDT — rutherford done
- `pipeline/rutherford_shelf.json`: 2 CCEL titles converted (920 units, 1,509 links), 3 IA items raw. The three Bonar-edited items on the Andrew Bonar shelf are listed under `_held` and were not refetched (the shelf move asked about in the digest is still yours).
- The identity check refused three 1640s first printings (Christ Dying 1647, Due Right 1644, Divine Right 1646): their OCR never contains Rutherford's name in any spelling. Moved to `_pending`. Free Disputation (1649) passed but is flagged `title_weak` (long s garbles "against"). 0 uids minted.

## 2026-10-02 16:19 CDT — mcheyne done
- `pipeline/mcheyne_shelf.json` (prose only; hymns are for the hymn manifest): 5 IA items raw. The Memoir and the Mission of Inquiry stay on the Andrew Bonar shelf (`_held`). `--verify`: 0 mismatched.
- The 1854 Google scan of the Additional Remains returned HTTP 500 on three tries; the 1849 printing (`MN5152ucmf_2`) is held instead and the 1854 scan listed as an alternate. 0 uids minted.

## 2026-10-02 16:20 CDT — matthew-henry done
- `pipeline/matthew-henry_shelf.json`: the whole Commentary (6 CCEL volumes) and the Concise Commentary fetched and converted: 37,105 units, 66,593 scripture links. CCEL's rights line on all seven reads public domain (checked in each file). Plus 2 IA items raw (Miscellaneous Works 1830, 9.3 MB; Life of Philip Henry). About 76 MB in all. `--verify`: 0 mismatched. 0 uids minted.

## 2026-10-02 16:26 CDT — calvin done
- Census: `CALVIN_COMMENTARIES` in `fetch_sources.py` holds all 45 Calvin Translation Society commentary volumes; nothing is missing from that series.
- `pipeline/calvin_shelf.json` adds the verified gaps: Institutes (Beveridge 1845; chapter headings confirm Beveridge's wording, though the file also carries Norton's 1581 prefatory matter and a CCEL introduction) and A Treatise on Relics from CCEL (3,818 units, 3,076 links; both rights lines read public domain, though Relics records a 2008 Prometheus reprint as its source, so its front matter wants a look before anyone republishes it); Bonnet's Letters vols 1-2 from Gutenberg (rights lines passed) and vols 3-4 from IA; the CTS Tracts, 3 vols, from IA. About 14 MB. `--verify`: 0 mismatched.
- Not taken: CCEL's Latin Institutio files are stubs (about 4,000 characters each); CCEL's "Three Volumes of Sermons" is the French Corpus Reformatorum text, out of scope for an English CTS shelf. 0 uids minted.

## 2026-10-02 16:29 CDT — round 3 opened; charnock done
- The coordinator's eleven defaults are done or in flight (Spurgeon still fetching). The relay asked for more Divines until the stop time, so lane A added eight of its own picks to QUEUE-A (Charnock, Manton, Boston, Gurnall, Burroughs, Newton prose, Whitefield, Hodge), each marked in the queue and in DIGEST-A as the worker's choice, open to Adam's veto.
- charnock: `pipeline/charnock_shelf.json`: 6 CCEL discourses converted (1,511 units, 2,775 links); Nichol's Complete Works, 5 vols, raw IA OCR (about 16 MB in all). `--verify`: 0 mismatched. 0 uids minted.
- Finding (rights, rule 6): every CCEL file fetched by this lane, in both rounds, opens with the XML comment "Copyright Christian Classics Ethereal Library": CCEL's claim over its markup. The DC.Rights field in round 2's 48 files reads "Public Domain" in 15 and is empty in 33; none says non-commercial. The texts are PD; republishing CCEL's markup itself is the thing to check per work.

## 2026-10-02 16:31 CDT — manton done
- `pipeline/manton_shelf.json`: Nisbet's Complete Works, all 22 volumes: 9 clean from CCEL (converted: 19,631 units, 30,564 links) and 13 raw IA OCR, one slug per volume whichever source holds it (about 48 MB). `--verify`: 0 mismatched. 0 uids minted.
