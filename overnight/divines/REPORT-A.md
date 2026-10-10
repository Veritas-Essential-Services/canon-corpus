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

## 2026-10-02 16:32 CDT — spurgeon done
- `pipeline/spurgeon_shelf.json`: 70 CCEL works fetched and converted: the Sermons in 63 volumes plus Morning and Evening, All of Grace, Faith's Checkbook, A Puritan Catechism, Commenting and Commentaries, Sermons on Proverbs, Till He Come. 194,800 units but only 6,138 scripture links: CCEL's Spurgeon files carry little scripRef markup, so the sermons' texts are not yet linked to verses. The Treasury of David, 7 vols, as raw IA OCR. About 157 MB in all, the largest shelf of the burn. `--verify`: 0 mismatched.
- CCEL's `spurgeon/treasury1`..`6` are stubs (about 4 KB of text each; the psalms are on separate web pages), recorded under `_excluded`. Rights: DC.Rights is empty in 66 files and "Public Domain" in 4; Commenting and Commentaries reproduces its 1890 title-page "All rights reserved", which is historical (Spurgeon d. 1892). 0 uids minted.

## 2026-10-02 16:33 CDT — boston done
- `pipeline/boston_shelf.json`: M'Millan's Whole Works, all 12 volumes, raw IA OCR (vol. 9 from a Google scan because the main series' text file returned HTTP 500), plus The Crook in the Lot from CCEL (439 units, 4 links). About 24 MB. `--verify`: 0 mismatched. 0 uids minted.

## 2026-10-02 16:34 CDT — gurnall done
- `pipeline/gurnall_shelf.json`: The Christian in Complete Armour (1862, intro. John Campbell), raw IA OCR, 4.6 MB. CCEL's `gurnall/armour` is a stub (about 7 KB of text). `--verify`: 0 mismatched. 0 uids minted.

## 2026-10-02 16:35 CDT — burroughs done
- `pipeline/burroughs_shelf.json`: 4 IA items raw (about 12.5 MB): the Nichol Hosea (1863, with Hall's and Reynolds's continuations) and Saints' Happiness (1867), Moses his Choice (1650), Four Books on Matthew 11 (1659). `--verify`: 0 mismatched.
- Refused by the identity check and moved to `_pending`: four 1640s-1650s scans, the Rare Jewel of Christian Contentment among them, whose OCR never contains Burroughs's name. Same pattern as Rutherford's first printings: old type defeats the name check. 0 uids minted.

## 2026-10-02 16:36 CDT — newton done
- `pipeline/newton_shelf.json` (prose; the Olney Hymns are for the hymn manifest): Messiah, 2 CCEL volumes converted (1,030 units, 1,193 links); the Works (1810), 6 vols, and Bull's Letters (1869), raw IA OCR. About 10 MB. `--verify`: 0 mismatched. 0 uids minted.

## 2026-10-02 16:38 CDT — whitefield done
- `pipeline/whitefield_shelf.json`: the Works (1771-72), all 6 volumes, clean from Gutenberg (rights lines passed); CCEL's Selected Sermons (1904, ed. Buckland) converted (2,319 units, 273 links); the Journals in 7 IA items from their first printings (1739-1756), raw. About 10 MB. `--verify`: 0 mismatched; the 1756 revised Life and Journals is flagged `title_weak` (long s). 0 uids minted.

## 2026-10-02 16:39 CDT — hodge done
- `pipeline/hodge_shelf.json`: 6 CCEL titles converted (7,133 units, 3,489 links), 8 IA items raw (about 21 MB in all). `--verify`: 0 mismatched.
- The identity check refused the 1872 scan of the 2 Corinthians commentary: its OCR never names Hodge. The 1860 scan, which does, is held instead. 0 uids minted.

## 2026-10-02 16:41 CDT — finding: OCR quality of the round 2 and 3 IA items
- Same method as round 1, with a larger vocabulary: share of word tokens (2+ letters) found among words seen twice or more in this lane's clean CCEL and Gutenberg texts (187 files, 86,585 words). Covers the 153 IA items fetched in rounds 2 and 3. Not comparable digit-for-digit with round 1's figures (smaller vocabulary then).
- Spread: 134 items at 97% or better, 7 at 95-97%, 8 at 90-95%, 4 below 90%. Median 98.9%. The Nichol, Goold and Grosart sets are uniformly good (98-99.5%).
- Per author (median): baxter 98.9, boston 99.1, brooks 98.9, burroughs 96.1, calvin 98.4, charnock 99.2, goodwin 99.0, gurnall 98.8, hodge 98.3, manton 99.1, matthew-henry 97.8, mcheyne 99.1, newton 98.7, owen 98.4, rutherford 86.9, sibbes 99.5, spurgeon 98.9, watson 97.7, whitefield 94.2.
- Lowest: owen-works-goold-17 80.4% (not bad OCR: the volume is much of it Latin, about 4,200 "est/quod/sunt/enim" against 6,500 "the/and"); rutherford-free-disputation-1649 81.8%, burroughs-four-books-matthew-1659 83.1%, rutherford-covenant-life-1655 86.9% (1640s-50s type, long s); then the Whitefield journals (92-95%, 1739-1756 type) and Treasury of David vol. 4 (91.7%).
- Practical reading: everything from the 19th-century collected editions is fit to search; the seventeenth- and eighteenth-century printings need a better text before anyone quotes from them.

## 2026-10-02 16:49 CDT — sweep of the refused items, and a regression in my own check
- Searched for other scans of every item the identity check had refused. Seven swapped in, each from a scan whose OCR names the author: Edwards's Distinguishing Marks (1742 printing) and Humble Attempt (1747); Rutherford's Due Right of Presbyteries (1644, EEBO); Burroughs's Rare Jewel (1649), Irenicum (1653, `title_weak`), Saints' Treasury (1656) and Glorious Name of God (1643), all EEBO. The refused scans are listed under `_alternates`. Still pending, no passing scan found: Rutherford's Christ Dying and Divine Right, Edwards's 1741 Distinguishing Marks, H. Bonar ×3, Ryle's Worldly Conformity, Saphir's Christ and the Scriptures.
- Regression caught: re-fetching the Edwards shelf showed my identity check (added this afternoon) would refuse 9 volumes Adam already held. Eight were Dwight-edition volumes whose only checkable title word is "dwight"; one, `edwards-worcester-04`, is genuine (content check: "religious affections" 445 times) but its 1808 OCR never yields the name. Fix in `pipeline/fetch_shelf.py`: a one-word title miss is flagged `title_weak`, not refused; a shelf's optional `_identity_checked` {slug: reason} keeps an item confirmed another way, flagged `identity_override`; the end-of-run count covers only the shelf's current slugs. Edwards re-fetched: 48 items, 0 failed. `--verify` across every lane-A shelf on disk: 0 mismatched. `tests/structure_test.py`: 64 passed. 0 uids minted.

## 2026-10-02 16:56 CDT — correction: the OCR quality figures at 16:41 were too high
- The 16:41 entry's vocabulary was contaminated. My scorer told clean texts from OCR by the fetch reports' URLs, and the Edwards report, written by the older fetch_edwards.py, carried none, so about 40 Edwards OCR files were counted as clean text and their misreadings entered the vocabulary. Re-fetching Edwards rewrote that report, and the scorer now also reads the shelves' own `internet_archive` keys.
- Corrected (194 clean files, 77,228 words): the 158 round 2-3 IA items have a median of 98.4% (not 98.9%); 126 at 97% or better, 13 at 95-97%, 1 at 90-95%, 18 below 90%. The 19th-century collected editions still score 97.8-99.3% per author. The 17th- and 18th-century printings fall further than first reported: Rutherford 77.3%, Whitefield's journals 84.8%, Burroughs 85.8% (the new EEBO scans 83-85%). The practical reading stands, more strongly: quote nothing from the old printings without a better text.

## 2026-10-02 16:56 CDT — howe done
- `pipeline/howe_shelf.json`: the Whole Works (1822, ed. Hunt, 8 vols): vols. V-VIII from CCEL, converted (5,296 units, 3,104 links); vols. I-IV raw IA OCR (median 98.2%). About 13 MB. `--verify`: 0 mismatched. The Posthumous Works (1832) are pending: the scans' volume order is unclear. 0 uids minted.

## 2026-10-02 17:00 CDT — doddridge done
- `pipeline/doddridge_shelf.json`: Rise and Progress, Regeneration and Evidences from CCEL, converted (1,382 units, 1,837 links); the Life of Colonel Gardiner from Gutenberg (rights line passed); the Leeds Works (1802-05), all 10 volumes, raw IA OCR. About 22 MB. `--verify`: 0 mismatched.
- The identity check refused the Princeton scan of vol. X (its OCR never names Doddridge); the Google scan of vol. X, which does, is held. OCR median 92.8%: vols. I-V 95-96%, vols. VI-X 87.7-90.9% (their many "paraphrase" and "improvement" headings suggest the Family Expositor, not confirmed from a title page). 0 uids minted.

## 2026-10-02 17:02 CDT — shepard done
- `pipeline/shepard_shelf.json`: Works vol. I (1853) and The Change of the Sabbath from CCEL, converted (1,643 units, 1,594 links); Works vols. II-III, the Autobiography (1832) and the Clear Sun-shine of the Gospel (1865 reprint), raw IA OCR. About 5.6 MB. `--verify`: 0 mismatched.
- The first Autobiography scan passed the identity check but held only 38 page images of a 129-page book (IA's own catalogue says so); swapped for a complete Google scan. The fetcher checks the author and title, not completeness: a sweep of page counts on every lane-A IA item is next. 0 uids minted.

## 2026-10-02 17:05 CDT — scougal done; completeness sweep
- `pipeline/scougal_shelf.json`: The Life of God in the Soul of Man from CCEL, converted (96 units, 3 links); the Works (Pittsburgh, 1830; 286 page images for xii + 272 pages) raw IA OCR, 98.8%. `--verify`: 0 mismatched. 0 uids minted.
- Completeness sweep after the partial Shepard scan: IA page images against the catalogue's page count for all 309 lane-A IA items. No other short scan found. One item has 33 images for 422 pages (`MN41487ucmf_5`, H. Bonar's Light and Truth), but it is microfilm with several pages a frame, and its 743 KB of text fits the book. Caveat: many IA records give no page count, so this check cannot clear them.

## 2026-10-02 17:09 CDT — william-law done
- `pipeline/william-law_shelf.json`: 10 CCEL titles converted (6,453 units, only 223 links: Law cites little scripture by reference); the Works (1892-93 reprint), 9 vols, raw IA OCR, median 99.5%. About 11 MB. `--verify`: 0 mismatched. CCEL `justific` is a stub; `humbleearnest` repeats two held files.
- Weak spot: the fetcher's name check is empty here, since "law" is an ordinary word, and the OCR never prints "William Law". The volumes rest on their title pages (volume numbers read) and on IA's contents note, which the text bears out by counts (vol. I "Bangor" 91 times, vol. IV "serious call" 139, vol. VI "Trapp" 40). 0 uids minted.

## 2026-10-02 17:10 CDT — gill done
- `pipeline/gill_shelf.json`: the Bodies of Doctrinal and Practical Divinity and the Solomon's Song exposition from CCEL, converted (6,611 units, 13,788 links); The Cause of God and Truth (1838, 96.1%) and the 1773 Sermons and Tracts, 2 vols (83-84%, long s), raw IA OCR. About 17 MB. `--verify`: 0 mismatched.
- The Exposition of the Bible, Gill's largest work, is pending: IA has only scattered 18th-century volumes and no complete set; several "Gill's Exposition" items are modern retypings with no library provenance and were left off. 0 uids minted.

## 2026-10-02 17:11 CDT — guthrie done
- `pipeline/guthrie_shelf.json`: The Christian's Great Interest from CCEL, converted (431 units, 5 links). Howie's Collection of Lectures and Sermons was left off: by name counts it is many Covenanters' sermons (Cargill 96, Cameron 69, Peden 45), not Guthrie's alone. 0 uids minted.

## 2026-10-02 17:12 CDT — leighton done
- `pipeline/leighton_shelf.json`: the Whole Works (London, 1830, ed. Pearson), all 4 vols, raw IA OCR, 98.7-99.0%. About 4.9 MB. `--verify`: 0 mismatched. Gutenberg's "Robert Leighton" is the novelist (1858-1934), excluded. 0 uids minted.

## 2026-10-02 17:14 CDT — alleine done
- `pipeline/alleine_shelf.json`: three IA items raw (about 1.4 MB): the Alarm (1834, 99.1%), Alleine on the Promises (1828, 93.3%), the Life and Death with his Christian Letters (1815, 98.5%). The Life is by Baxter, Theodosia Alleine and others: only the letters are his, and the digest says so. `--verify`: 0 mismatched. 0 uids minted.

## 2026-10-02 17:16 CDT — perkins done
- `pipeline/perkins_shelf.json`: the Workes (Legatt, 1616-18), 3 vols, EEBO scans, raw IA OCR, about 15 MB. The three are vols. 1-3 of one IA series; the printer's name occurs in each. OCR 71-77%, the roughest on this lane: early 17th-century type. Good for finding a passage, not for quoting one. `--verify`: 0 mismatched. 0 uids minted.

## 2026-10-02 17:18 CDT — andrew-murray done
- `pipeline/andrew-murray_shelf.json`: 11 CCEL titles and 5 Gutenberg (rights lines passed), about 3 MB; CCEL converted (3,963 units, 2,925 links). Gutenberg's The Spirit-Filled Life is John MacNeil's (Murray wrote the introduction), excluded; Lord, Teach Us To Pray (1896) shares 71% of its 8-word runs with the School of Prayer, kept as an alternate. 0 uids minted.

## 2026-10-02 17:34 CDT — review findings acted on (coordinator relay, from the Greek NT thread's review)
- **Identity check tightened, backward compatible** (`pipeline/fetch_shelf.py`). A shelf may now name `_surname`: one of those surnames must appear as a whole word (spaces match line breaks, the apostrophe in M'Cheyne is optional). Without `_surname` the old substring test runs and the report says "legacy". The item's own IA identifier is scrubbed from the text first: Google and IA scans print it into the OCR, and that is how two Ryle tracts that never name Ryle passed. All 37 lane-A shelves now carry `_surname` (Boston, Brooks and Law as two-word names, since the bare words are common). Result over all 560 items on the 37 shelves: 0 mismatched after three changes: two Ryle tracts to `_pending`; Ryle's Home Truths (1857), which had passed only on "charles", kept under `_identity_checked` (it names Helmingham, his parish, 6 times); Edwards's Worcester vol. 4 as before.
- **Rights and translator checks are now committed.** `fetch_shelf.py <shelf> --verify --record` writes `_checks` into the shelf: identity result and the surname found; Gutenberg's copyright marker and Translator line, compared with the shelf's new `_translators` claim; CCEL's DC.Rights line and copyright comment; archive.org's catalogue date, copyright status and lending collections. A new archive.org fetch is refused when the record says published 1930 or later, has no date, or sits in a lending collection, unless `_rights_checked` names the slug with a reason. Recorded on all 37 lane-A shelves: 0 rights flags. A first run flagged 17 items in IA's own `internetarchivebooks` collection; those are 1850-1911 books with downloadable text, not lending scans, so that collection no longer counts as lending.
- **CCEL non-commercial request** recorded on every lane-A CCEL item: 198 on 37 shelves, against the reviewer's 214. The difference is not explained: lane A's shelves list 198 CCEL rows now, and no row was removed. `pipeline/convert_shelf.py` now writes a `rights` block into each built book (DC.Rights, the copyright comment, CCEL's terms, `redistribute_whole: false`, `ruling: pending (Adam)`), and a `translator` where the shelf names one; already-built books were updated in place, units untouched. All 198 built books carry it.
- **Calvin's Letters:** translators recorded, David Constable for vols. 1-2, Marcus Robert Gilchrist for vols. 3-4 (each name is on the title page in the text). `_translators` now covers all 9 Calvin items (Beveridge for the Institutes and Tracts, Krasinski for the Relics); Tracts vol. 1's OCR lacks Beveridge's name and is kept under `_identity_checked` on IA's record crediting him.
- **Edwards:** the 1903 Unpublished Essay on the Trinity was held twice (CCEL clean and an IA scan); the scan moved to `_alternates`. The shelf now has 47 items. Of the 8 early printings added this burn, one (Hopkins's Life, 1804) is about Edwards, not by him; the digest says so.
- **Concise Matthew Henry:** CCEL's file names no abridger and no date. Recorded as `_rights_question` on the shelf and put to Adam.
- `tests/structure_test.py`: 64 passed. 0 uids minted.

## 2026-10-02 17:37 CDT — watts done
- `pipeline/watts_shelf.json`: the London Works (1810, ed. Burder), 6 vols, raw IA OCR (98.3-99.3%); the Leeds Works vol. 1 and the Essay on Psalmody clean from Gutenberg (rights lines passed). About 20 MB. `--verify --record`: 0 mismatched, 0 rights flags. Hymns left to the hymn manifest. 0 uids minted.

## 2026-10-02 19:40 CDT — archibald-alexander done
- `pipeline/archibald-alexander_shelf.json`: 3 CCEL titles converted (1,582 units, 183 links); 5 IA items raw (96.7-99.2%). About 7.6 MB. The surname check uses "archibald alexander" / "dr. alexander", since "alexander" alone is common and his sons share it. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 19:45 CDT — chalmers done
- `pipeline/chalmers_shelf.json`: the Works (Glasgow: Collins, 1836-42), all 25 vols from one IA series, raw OCR, 97.6-98.6% (median 98.0%). About 19 MB. Volume numbers from the title pages, which the automatic reader got wrong on 5 volumes (it picked up "vol. II" from contents pages); those 5 were checked one by one, vol. XX by its running heads. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 19:48 CDT — erskines done
- `pipeline/erskines_shelf.json`: Ebenezer's Whole Works (1871, 3 vols) and Ralph's Sermons and Practical Works (1865, 7 vols), raw IA OCR, 97.7-99.4%. About 19 MB. `--verify --record`: 0 mismatched, 0 rights flags. The surname check cannot tell the brothers apart; the split rests on the title pages and on place-name counts (Ebenezer's volumes name Stirling, his charge, 4-9 times; Ralph's name Dunfermline, his, 4-25 times). 0 uids minted.

## 2026-10-02 19:50 CDT — halyburton done
- `pipeline/halyburton_shelf.json`: the Works (Glasgow, 1833), one volume of 817 pages, raw IA OCR, 98.0%, 3.4 MB. The contents note checks out by counts ("natural religion" 179, "deists" 214, "great concern" 23). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 19:51 CDT — binning done
- `pipeline/binning_shelf.json`: the Works (Edinburgh, 1851), one volume of 659 pages, raw IA OCR, 98.0%, 3.9 MB. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 19:53 CDT — durham done
- `pipeline/durham_shelf.json`: five early printings (1680-1792), raw IA OCR, 77-85% (old type): fit for finding passages, not for quoting. About 9.3 MB. The 1659 Treatise concerning Scandal was refused (OCR never names Durham) and is pending. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 19:56 CDT — octavius-winslow done
- `pipeline/octavius-winslow_shelf.json`: 15 books (1838-1869), raw IA OCR, 90.7-98.6%, about 6.5 MB. Two scans swapped: None Like Christ for a fuller scan (89 page images, not 59), Go and Tell Jesus for the scan whose OCR names Winslow. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:03 CDT — warfield done
- `pipeline/warfield_shelf.json`: 19 lifetime books (1886-1921), raw IA OCR, median 97.5% (lowest 91.8%, the Institutes history), about 5.9 MB. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted. The posthumous Oxford Works are left out: lending scans, and the later volumes fall after the 1930 line.

## 2026-10-02 20:06 CDT — thornwell done
- `pipeline/thornwell_shelf.json`: 6 items, raw IA OCR, median 97.2% (95.5-98.0%), about 8.4 MB. Discourses on Truth: the California scan's OCR loses the author's name, so the Library of Congress scan is used, with an `_identity_checked` reason quoting its title page ("Thornweil" is the OCR's reading of Thornwell). Volume dates were read from the title pages (vols 3-4 are 1873). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted. Flagged for veto: vol. 4 carries much of his defence of slavery.

## 2026-10-02 20:09 CDT — dabney done
- `pipeline/dabney_shelf.json`: 9 items, raw IA OCR, median 96.8% (95.2-98.4%), about 13 MB. IA dates all four Discussions 1890; the title pages give 1890, 1891, 1892 and 1897 (vol. 4 printed at Mexico, Mo.), and the shelf uses the title pages. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted. Flagged for veto: Discussions vol. 4 carries much of his writing on slavery and race.

## 2026-10-02 20:17 CDT — samuel-davies done
- `pipeline/samuel-davies_shelf.json`: 3 volumes, raw IA OCR, median 98.1%, about 4.3 MB. First built from the 1864 Philadelphia edition; its vol. 1 text returned HTTP 500 four times, so the shelf moved whole to the 1845 Carter edition rather than mix editions (title pages read: Barnes, Carter, 1845, vols I-III). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.
- Round 6 queued (15 Divines, my picks, for Adam's veto): Swinnock, Thomas Adams, Clarkson, Andrew Fuller, Toplady, Romaine, Ambrose, Charles Bridges, Simeon, Robert Haldane, James Buchanan, William Cunningham, Fairbairn, John Angell James, William Jay. The scratchpad CCEL search was patched for CCEL's current author-page links; none of these has a CCEL text under the slugs tried.

## 2026-10-02 20:19 CDT — swinnock done
- `pipeline/swinnock_shelf.json`: 5 volumes, raw IA OCR, median 98.6% (97.9-98.8%), about 7.6 MB; title pages read (Nichol, vols I-V). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted. Built with a new scratchpad helper, `mkshelf.py`, that writes a shelf from a short spec.

## 2026-10-02 20:21 CDT — thomas-adams done
- `pipeline/thomas-adams_shelf.json`: 3 volumes, raw IA OCR, median 96.1% (95.7-96.8%), about 6.9 MB; title pages read (Nichol, Angus, vols I-III). The surname check uses "thomas adams", since "adams" alone is too common. A line in the first draft quoting Southey on Adams was dropped: it was not found in the text. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:22 CDT — clarkson done
- `pipeline/clarkson_shelf.json`: 3 volumes, raw IA OCR, median 99.1% (95.7-99.2%), about 6.8 MB; title pages read (Nichol, vols I-III). No printed year survives in the OCR, so the titles carry the Princeton records' 1864. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:24 CDT — andrew-fuller done
- `pipeline/andrew-fuller_shelf.json`: 1 volume (1,118 page images, 10.7 MB), raw IA OCR, 98.7%. Completeness checked by counting the main titles in the text: Gospel Worthy, Calvinistic and Socinian, Sandemanianism, Genesis and Apocalypse discourses and The Backslider are all present. The 1846 date is the catalogue's; the OCR's title page carries none. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:26 CDT — toplady done
- `pipeline/toplady_shelf.json`: 6 volumes, raw IA OCR, median 96.2% (95.5-97.3%), about 6.1 MB; title pages read (Baynes, 1825, vols I-VI). His hymns are printed inside the Works and stay there; splitting them out for the hymn manifest is for Adam to ask for. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:30 CDT — romaine done
- `pipeline/romaine_shelf.json`: 1 volume (Whole Works, 1837), raw IA OCR, 99.5%, about 5.2 MB. First built on the 1801 8-volume Works, which scored 85-88% because of its long-s type; three one-volume editions were test-fetched (98.2-99.5%) and the best taken. Its title page lists the contents, and the text was searched for each. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted. Lesson for the rest of the round: prefer a 19th-century reprint over a long-s first edition.

## 2026-10-02 20:32 CDT — isaac-ambrose done
- `pipeline/isaac-ambrose_shelf.json`: 1 volume (Works, 1829), raw IA OCR, 99.1%, about 1.8 MB; the text was searched for each of the main treatises and all are present. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:35 CDT — charles-bridges done
- `pipeline/charles-bridges_shelf.json`: 4 items, raw IA OCR, median 97.1% (96.5-98.2%), about 6.2 MB. Each Works volume's contents were read from its title page. Ecclesiastes: the California scan's OCR garbles his name, so the gate refused it; the Princeton scan, which names him, is used. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:39 CDT — simeon done
- `pipeline/simeon_shelf.json`: 21 volumes, raw IA OCR, median 98.8% (97.8-99.0%), about 34 MB. Title pages read (Holdsworth and Ball; vol. 1 Genesis to Leviticus, vol. 21 Revelation, Claude, index); the figure 2,536 is the number of the last outline in vol. 21. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:41 CDT — robert-haldane done
- `pipeline/robert-haldane_shelf.json`: 6 volumes, raw IA OCR, median 98.5% (96.6-99.0%), about 4.9 MB; title pages read. A line in the first draft about his Geneva lectures was cut as unverified. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:43 CDT — james-buchanan done
- `pipeline/james-buchanan_shelf.json`: 6 volumes, raw IA OCR, median 97.8% (97.6-98.7%), about 5.6 MB. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:46 CDT — william-cunningham done
- `pipeline/william-cunningham_shelf.json`: 5 volumes, raw IA OCR, median 98.5% (97.5-99.0%), about 8.9 MB; title pages read (Buchanan and Bannerman as editors; Historical Theology vol. 1 printed 1862, not the catalogue's 1863). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:52 CDT — fairbairn done
- `pipeline/fairbairn_shelf.json`: 9 volumes, raw IA OCR, median 98.5% (95.5-99.0%), about 12 MB. The identity gate refused two scans. Revelation of Law: the Princeton scan never prints his name, so it was swapped for the Toronto scan, which does. Prophecy: the OCR reads "Faiebairk", so an `_identity_checked` reason quotes the title page. The two Typology volumes come from two Toronto libraries, both the 1864 Clark 4th edition. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:55 CDT — john-angell-james done
- `pipeline/john-angell-james_shelf.json`: 16 of 17 volumes, raw IA OCR, median 99.0% (98.1-99.3%), about 16 MB. IA's identifiers do not follow the volume order; the shelf maps them by the catalogue's volume field, and the title pages confirm it for 14 of the 16 (vols 9 and 11 print no volume number in the opening pages). Vol. 15 has no scan with a text layer, so it is pending. The surname check uses "angell james", because "james" alone would match almost any book. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 20:57 CDT — william-jay done
- `pipeline/william-jay_shelf.json`: 4 volumes, raw IA OCR, median 98.4% (98.3-98.6%), about 13 MB. Each Works volume's contents page was read for the map line; whether the Works hold every separately printed book (Female Scripture Characters, Thoughts on Marriage) was not confirmed, so those printings are listed as alternates, not claimed. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:00 CDT — william-bridge done
- `pipeline/william-bridge_shelf.json`: 5 volumes, raw IA OCR, median 98.9% (98.3-99.2%), about 6.3 MB; title pages read (Tegg, 1845, vols I-V). The surname check uses "william bridge", because "bridge" alone is an ordinary word. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted. From here a scratchpad `run.sh` does fetch, title-page hints, verify, OCR and pages in one pass.

## 2026-10-02 21:02 CDT — edward-reynolds done
- `pipeline/edward-reynolds_shelf.json`: 6 volumes, raw IA OCR, median 96.7% (95.6-97.6%), about 7.7 MB; title pages read (1826; Chalmers's memoir). A line in the first draft crediting him with the Prayer Book's General Thanksgiving was cut: it is not in this text. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:04 CDT — william-bates done
- `pipeline/william-bates_shelf.json`: 6 items, raw IA OCR, median 95.0%; the three Google-scanned Works volumes score 89-92%, the three separate books 98-99%. IA does not number the Google scans; the volumes were identified from their title pages (II, III, IV). Vol. 1 has no scan, so three of his books printed separately stand in, and whether they make up the whole of vol. 1 was not checked. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:06 CDT — ezekiel-hopkins done
- `pipeline/ezekiel-hopkins_shelf.json`: 3 volumes, raw IA OCR, median 98.7% (98.5-99.2%), about 6.1 MB; title pages read (Quick from Pratt, vols I-III). The copies scanned are dated 1867 and 1874 by their shelfmarks, so the titles say 1867-74. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:08 CDT — robert-traill done
- `pipeline/robert-traill_shelf.json`: 2 bindings holding all 4 volumes (each volume's title page found in the text), raw IA OCR, 94.2-95.2%, about 2.8 MB. Google scans, but the alternatives are long-s 18th-century editions or a one-volume selection. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:10 CDT — george-gillespie done
- `pipeline/george-gillespie_shelf.json`: 1 Gutenberg book (Works vol. 1, 1846; its transcriber's note and title page name the edition) and 1 IA scan (Aaron's Rod, 1844, 94.5%). The 1649 Miscellany Questions was fetched, scored 74.9%, and moved to `_pending` rather than shelved. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:12 CDT — david-dickson done
- `pipeline/david-dickson_shelf.json`: 2 items, raw IA OCR, 98.4-98.8%, about 1.1 MB. Therapeutica Sacra (1697) was refused by the identity gate (long-s OCR never prints his name) and is pending with the 17th-century commentaries. The Sum of Saving Knowledge is the copy the Durham shelf excluded as chiefly Dickson's, so it is not duplicated. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:14 CDT — john-brown-haddington done
- `pipeline/john-brown-haddington_shelf.json`: 6 items, raw IA OCR, median 95.9% (93.3-98.2%), about 12 MB. IA's catalogue mixes him with other John Browns, so each title page was read: all six name him (Haddington, or professor of divinity under the Associate Synod). The surname gate alone ("brown") would not tell them apart. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:15 CDT — timothy-dwight done
- `pipeline/timothy-dwight_shelf.json`: 4 volumes, raw IA OCR, median 98.6%, about 7.2 MB; title pages read (Harper, 1846, vols I-IV). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:17 CDT — samuel-hopkins done
- `pipeline/samuel-hopkins_shelf.json`: 3 volumes, raw IA OCR, median 98.8% (98.1-98.8%), about 7.6 MB; title page read (Boston, 1854, three volumes). The memoir's author is not on the title page, so the shelf does not name him. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:18 CDT — joseph-bellamy done
- `pipeline/joseph-bellamy_shelf.json`: 2 volumes, raw IA OCR, 98.5-98.6%, about 4.4 MB; title pages read (1853, vols I-II, memoir). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:21 CDT — thomas-vincent done
- `pipeline/thomas-vincent_shelf.json`: 4 items, raw IA OCR, 90.0-98.8% (the 1701 long-s printing is the 90%), about 1.7 MB. God's Terrible Voice comes from the National Library of Medicine, whose text file has a non-standard name (given as the shelf's third field), and whose OCR reads his name "Vijvceat"; an `_identity_checked` reason quotes the title page. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:22 CDT — henry-smith done
- `pipeline/henry-smith_shelf.json`: 2 volumes, raw IA OCR, 98.6-99.1%, about 2.7 MB; title pages read (vols I-II; no printed year in the OCR, so the catalogue's 1866 is used). The surname check uses "henry smith". `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:24 CDT — lewis-bayly done
- `pipeline/lewis-bayly_shelf.json`: 1 item, raw IA OCR, 89.6% (long-s type; no 19th-century printing is on IA), about 0.8 MB. The title page is anonymous, as in every edition, so the identity gate refused it; the dedication is signed "Lewis Bailey", and an `_identity_checked` reason records that. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:26 CDT — john-preston done
- `pipeline/john-preston_shelf.json`: nothing shelved. All seven of his treatises on IA are 1630-1641 printings; fetched and scored, their OCR came to 79-81% (one more failed the identity gate), so they went to `_pending` with their identifiers and the texts were deleted. The shelf file stays so nobody repeats the search. 0 uids minted.

## 2026-10-02 21:32 CDT — john-wesley done
- `pipeline/john-wesley_shelf.json`: 4 CCEL titles (converted with `convert_shelf.py`: 27,280 units, 4,078 scripture links) and the 1826-30 Works, 10 volumes of raw IA OCR, median 98.5%, about 29 MB with the CCEL files. The CCEL Journal is Parker's abridgement transcribed from a 1951 Moody Press reprint; flagged in the digest. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:37 CDT — richard-hooker done
- `pipeline/richard-hooker_shelf.json`: 1 CCEL title and Keble's 1836 Works, 3 volumes of raw IA OCR, median 95.9% (94.5-96.2%), about 5.5 MB; title pages read (Keble, MDCCCXXXVI). Vol. 1 is a Claremont scan, vols 2-3 Toronto. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:40 CDT — jeremy-taylor done
- `pipeline/jeremy-taylor_shelf.json`: 2 CCEL titles (converted) and the Heber/Eden Whole Works, 10 volumes of raw IA OCR, median 97.3% (95.1-98.2%), about 23 MB; title pages read (Eden, MDCCCXLVII-MDCCCLIV). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:41 CDT — lancelot-andrewes done
- `pipeline/lancelot-andrewes_shelf.json`: 1 CCEL title (converted; Newman's translation recorded under `_translators`) and 6 IA volumes of raw OCR, median 97.0% (95.9-97.7%), about 7.5 MB; title pages read (MDCCCXLI-MDCCCXLIII, MDCCCXLVI; vol. 3 undated). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:50 CDT — joseph-butler done
- `pipeline/joseph-butler_shelf.json`: 2 CCEL titles (converted) and Gladstone's 1896 Works, 2 volumes of raw IA OCR (Illinois scans; the Toronto scans have no `_djvu.txt`), median 99.0%, about 1.9 MB; title pages read (1896). First shelf fetched under the fixed gates. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:51 CDT — thomas-fuller done
- `pipeline/thomas-fuller_shelf.json`: 2 CCEL titles (converted) and 4 IA volumes of raw OCR, median 96.6% (94.2-97.9%), about 6 MB; title pages read (1837, 1840). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:57 CDT — john-donne done
- `pipeline/john-donne_shelf.json`: 3 CCEL titles (converted) and Alford's 1839 Works, 6 volumes of raw IA OCR, median 96.4% (89.1-96.7%), about 10 MB; title pages read (vols I-VI). Vol. 1 is the weakest scan (89%; the other copy tried scored 74%). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 21:59 CDT — thomas-traherne done
- `pipeline/thomas-traherne_shelf.json`: 1 CCEL title (converted) and Dobell's 1903 Poetical Works (raw IA OCR, 98.4%; title page read, "4903" in the OCR). The first scan tried (Toronto) held about half the text and was swapped. Christian Ethicks 1675 is pending at 79.8%. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 22:03 CDT — john-henry-newman done
- `pipeline/john-henry-newman_shelf.json`: 1 CCEL title (converted), 5 Gutenberg texts (rights lines checked by the gate) and the Parochial and Plain Sermons, 8 volumes of raw IA OCR (Longmans 1891), median 99.3%, about 9 MB. The 1868 Toronto set was tried first: 81-91% OCR and three volumes never showed the name, so it was swapped. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted. Digest flags Newman's 1845 conversion as a veto point.

## 2026-10-02 22:06 CDT — george-herbert done
- `pipeline/george-herbert_shelf.json`: 1 CCEL title (converted) and Palmer's English Works, 3 volumes of raw IA OCR, median 95.9% (95.7-96.3%), about 1.5 MB; title pages read (MDCCCCV; vol. 1 MDCCCCXV). Vol. 3 reads low per page (757 bytes/image, mostly verse with notes); it is the fuller of the two copies compared, and the other was swapped out. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 22:11 CDT — thomas-ken done
- `pipeline/thomas-ken_shelf.json`: 3 IA items of raw OCR: Prose Works 98.4% (the scan opens with a publisher's 1855 catalogue; the title page inside reads Round, London, 1838), Manual of Prayers 98.0%, Christian Year 84.1% (verse; a second scan scored 84.9%, so the score looks like the book, not the scan). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-02 22:16 CDT — joseph-hall done
- `pipeline/joseph-hall_shelf.json`: Wynter's 1863 Works, vols 1-9 of raw IA OCR, median 98.0% (96.2-99.3%), about 17 MB; title pages read (MDCCC.LXIII). Vol. 10 is pending: the Google scan catalogued as vol. 10 reads VOL. VII on its own title page and was dropped. Vol. 3 is the Trinity College copy (the Robarts copy kept returning HTTP 500). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 00:47 CDT — isaac-barrow done
- `pipeline/isaac-barrow_shelf.json`: Napier's 1859 Theological Works, 9 volumes of raw IA OCR, median 96.3%, about 11 MB; title pages read (Napier; VOLUME I-IX). Vol. 9 scores 83.2% because much of it is Latin (about 3,300 "et" against 9,700 "the"), not because the scan is bad. Vols 7-8 are Emory scans (Toronto's vol. 7 kept returning HTTP 500, and Toronto has no vol. 8). Recorded on the full name "isaac barrow" under the new common-word guard: 9/9 matched. 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 00:48 CDT — henry-martyn done
- `pipeline/henry-martyn_shelf.json`: 3 IA items of raw OCR, median 97.4% (97.2-98.6%), about 2.8 MB; title pages read (MDCCCXXXVII; 1822). `--verify --record`: 0 mismatched, 0 rights flags; matched on "henry martyn". 0 uids minted.
- Gates, 2026-10-03 (relayed review findings, lane A owns them): `fetch_shelf.py` identity gate now collects every miss and an override covers only the miss it names, never the translator; the IA rights gate fails closed and the latest year on the record decides (815a082). A surname that is a common English word ("hall", "ken") never matches bare, and a shelf with only such forms stops at load (e1ef08b). Lane A's 13 affected shelves were re-recorded on full names: every item matched. `tests/fetch_shelf_test.py`, 35 checks.

## 2026-10-03 00:52 CDT — james-hervey done
- `pipeline/james-hervey_shelf.json`: the 1834 one-volume Whole Works, raw IA OCR, 95.3%, 5.7 MB; title page read (1834). `--verify --record`: 0 mismatched, 0 rights flags; matched on "james hervey". 0 uids minted.
- Round 9, nothing shelved: Matthew Poole (only the 1683-1700 folios on IA, long s in double columns, plus one volume of an 1861 printing) and John Trapp (the one scan, catalogued 1865, is by its own front matter the Sovereign Grace Book Club's 1958 reprint). Both are `pending` in the queue.

## 2026-10-03 00:53 CDT — henry-venn done
- `pipeline/henry-venn_shelf.json`: The Complete Duty of Man, 1838 printing, raw IA OCR, 98.8%, about 0.9 MB; title page read (1838; a "1923" in the OCR is a library stamp). `--verify --record`: 0 mismatched, 0 rights flags; matched on "henry venn". 0 uids minted.

## 2026-10-03 00:55 CDT — john-fletcher done
- `pipeline/john-fletcher_shelf.json`: the New York Works, 4 volumes of raw IA OCR, median 98.8% (97.8-99.2%), about 9 MB. The catalogue says 1833; the title pages carry no year, and the imprints differ (Carlton and Porter on vol. 1, Carlton and Lanahan on vol. 2), so the shelf says so rather than claiming 1833. `--verify --record`: 0 mismatched, 0 rights flags; matched on "john fletcher". 0 uids minted.

## 2026-10-03 00:57 CDT — robert-hall done
- `pipeline/robert-hall_shelf.json`: Bohn's Works, 6 volumes, and the Miscellaneous Works and Remains, raw IA OCR, median 98.4% (98.3-98.7%), about 7 MB; title pages read (Gregory, Bohn; no year printed, so the catalogue's 1846 is labelled as such). `--verify --record`: 0 mismatched, 0 rights flags; all 7 matched on "robert hall". 0 uids minted.

## 2026-10-03 00:59 CDT — edward-payson done
- `pipeline/edward-payson_shelf.json`: the 1851 Complete Works, 3 volumes of raw IA OCR, median 99.0%, about 4.7 MB; title pages read (1851). `--verify --record`: 0 mismatched, 0 rights flags; matched on "edward payson". 0 uids minted.

## 2026-10-03 01:00 CDT — cotton-mather done
- `pipeline/cotton-mather_shelf.json`: the Magnalia (Andrus, 2 vols) and Essays to Do Good (1808), raw IA OCR, median 93.3% (91.9-95.9%; the Magnalia is thick with Latin and Greek), about 5 MB; title pages read: the two Magnalia copies were printed in 1868 and 1858 from the 1852 copyright, and the shelf says so rather than the catalogue's 1853. `--verify --record`: 0 mismatched, 0 rights flags; matched on "cotton mather". 0 uids minted.

## 2026-10-03 01:01 CDT — john-pearson done
- `pipeline/john-pearson_shelf.json`: An Exposition of the Creed (Bell, Walford's analysis), raw IA OCR, 90.2%, 2.4 MB. The score reflects the Greek and Latin of Pearson's notes more than the scan. Title page read (Bell, Walford; no year printed, catalogue 1902). `--verify --record`: 0 mismatched, 0 rights flags; matched on "john pearson". 0 uids minted.

## 2026-10-03 01:03 CDT — william-paley done
- `pipeline/william-paley_shelf.json`: 2 CCEL titles (converted) and the one-volume Philadelphia Works, raw IA OCR, 98.1%, about 6 MB (contents as the catalogue title lists them, confirmed by headings in the text; no year on the title page, catalogue 1853). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:05 CDT — robert-south done
- `pipeline/robert-south_shelf.json`: the Oxford 1823 Sermons, 7 volumes of raw IA OCR, median 98.5% (98.1-98.6%), about 8 MB; title pages read (MDCCCXXIII; the Trinity College copy catalogued without a volume number is vol. VII by its title page). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:07 CDT — thomas-scott done
- `pipeline/thomas-scott_shelf.json`: the Essays with The Force of Truth (Edinburgh, 1825), raw IA OCR, 98.2%, 1.1 MB. `--verify --record`: 0 mismatched, 0 rights flags; matched on "thomas scott". 0 uids minted.

## 2026-10-03 01:10 CDT — william-beveridge done
- `pipeline/william-beveridge_shelf.json`: the LACT Theological Works, 12 volumes of raw IA OCR, about 15 MB; title pages read (MDCCCXLII-MDCCCXLVIII). Median 98.4%; vols 11-12 score 70% because they are Latin (5 and 8 "the" against 1,700-3,500 "et"), vol. 7 90% for the same reason in part. `--verify --record`: 0 mismatched, 0 rights flags; matched on "william beveridge". 0 uids minted.

## 2026-10-03 01:10 CDT — w-g-t-shedd done
- `pipeline/w-g-t-shedd_shelf.json`: 5 IA volumes of raw OCR, median 97.6% (96.2-98.0%), about 4.6 MB; title pages read (1888, 1894; 1863, and 1868 for the History's vol. 2). The first vol. 2 tried never showed Shedd's name and the gate refused it; another copy replaced it. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:12 CDT — j-b-lightfoot done
- `pipeline/j-b-lightfoot_shelf.json`: 1 CCEL title (converted; Lightfoot recorded as translator), 3 Gutenberg texts (rights lines checked) and 2 IA commentaries, raw OCR 92.3% each (Greek-heavy notes), about 5 MB; title pages read (1890, 1898). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:18 CDT — b-f-westcott done
- `pipeline/b-f-westcott_shelf.json`: 6 IA volumes of raw OCR, median 91.0% (88.1-97.4%; Greek text and notes), about 8 MB; title pages read (1883-1908). The gate refused a Robarts Epistles of John scan whose text layer names neither the book nor Westcott; a Claremont copy replaced it. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:21 CDT — r-c-trench done
- `pipeline/r-c-trench_shelf.json`: 4 Gutenberg texts (rights lines checked) and 3 IA volumes of raw OCR, median 95.1% (95.1-96.1%), about 5.5 MB. All 7 matched on "richard chenevix trench" ("trench" alone is a common word). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:31 CDT — john-brown-edinburgh done
- `pipeline/john-brown-edinburgh_shelf.json`: 4 IA volumes of raw OCR, median 97.4% (97.0-98.1%), about 9 MB; title pages read (1854, 1857; First Peter shows Carter and 1849 though catalogued 1855, and the shelf says both). The name check is "john brown", which his grandfather shares; titles carry the distinction. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:33 CDT — f-w-robertson done
- `pipeline/f-w-robertson_shelf.json`: 1 Gutenberg text (rights line checked) and the 1875 King set, 4 volumes of raw IA OCR, median 98.6% (98.3-98.9%), about 3.4 MB; title pages read (King, 1875). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:36 CDT — john-eadie done
- `pipeline/john-eadie_shelf.json`: Ephesians and Galatians, raw IA OCR, 94.5% and 96.7%, about 2.7 MB; title pages read (1883, MDCCCLXIX). A Philippians catalogued 1894 was fetched and then dropped: its front matter says Klock and Klock reprint, 1977. That is the second reprint today the date gate passed (after Trapp); see Defects in the digest. Thessalonians is pending (HTTP 500). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:37 CDT — henry-alford done
- `pipeline/henry-alford_shelf.json`: The Greek Testament, vols 1, 2 and 4, raw IA OCR, 82.3%, 89.9% and 93.8%, about 13 MB. Vol. 1's text layer has no Greek characters at all (450,000 or so in each of vols 2 and 4). Vol. 3 is pending. Two Boston copies were refused by the identity gate. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.
- Greek in the text layer, measured 2026-10-03 (Greek codepoints per file): 0 in Lightfoot's Galatians and Philippians, Westcott's Canon, Epistles of John, Hebrews and John vol. 2, Eadie's Ephesians, Pearson's Creed and Alford vol. 1; present in Lightfoot's Colossians (PG), Westcott's John vol. 1, Eadie's Galatians, Trench's Synonyms and Alford vols 2 and 4. Where it is 0 the Greek was read as Latin letters, as with the Thayer scan; the English is usable, the Greek is not.

## 2026-10-03 01:39 CDT — john-keble done
- `pipeline/john-keble_shelf.json`: 1 CCEL title (converted), 1 Gutenberg text (rights line checked) and 2 IA volumes of raw OCR at 98.6%, about 2.9 MB; title pages read (1847, 1877). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:45 CDT — e-b-pusey done
- `pipeline/e-b-pusey_shelf.json`: 3 IA volumes of raw OCR, about 8 MB: the Minor Prophets 81.0% (Hebrew and Greek in the notes), Daniel 95.9%, Lenten Sermons 98.6%; title pages read (1860, 1868, 1874). The Minor Prophets item offers only a plain `<id>.txt`, so `fetch_shelf.py` now accepts any `.txt` name in an IA row's third element (it required `_djvu.txt`). The gate refused A Course of Sermons on Solemn Subjects (Pusey's name never appears; several preachers). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:45 CDT — h-p-liddon done
- `pipeline/h-p-liddon_shelf.json`: 5 IA volumes of raw OCR, median 98.6% (96.5-99.1%), about 5 MB; title pages read (1867-1906). The gate refused a Christmastide in St. Paul's copy whose text never names Liddon. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:49 CDT — a-a-hodge done
- `pipeline/a-a-hodge_shelf.json`: 5 IA volumes of raw OCR, median 98.1% (97.6-98.5%), about 6 MB; title pages read (1867-1887). The Confession commentary IA catalogues as 1869 is the 1885 new edition (preface dated June 1885), so it is labelled that way. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 01:52 CDT — j-a-alexander done
- `pipeline/j-a-alexander_shelf.json`: 12 IA volumes of raw OCR, median 97.1% (94.7-98.6%), about 15 MB; title pages read (1846-1861). The text layers hold 0 Hebrew and 0 Greek characters, so the Isaiah and Psalms commentaries have lost every original-language word. The gate refused the only Primitive Church Offices copy tried (its text never names him); it is pending. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 02:00 CDT — acted on roving review (cycle 8)
- `fetch_shelf.py`: `shared_name_forms()` prints a NOTE at load for any name form another shelf also claims; "trench" added to the common-word list. `tests/fetch_shelf_test.py` 46/46, structure_test 64/64.
- Nine lane A shelves moved to distinguishing name forms and were re-recorded (`--verify --record`, 0 mismatched): hodge, a-a-hodge, john-brown-edinburgh, john-brown-haddington, perkins, andrew-bonar, horatius-bonar, ezekiel-hopkins, samuel-hopkins. j-a-alexander dropped bare "alexander"; r-c-trench re-recorded. Five items with OCR-mangled title-page names went to `_identity_checked` with the reading quoted.
- DIGEST-A: the Owen late-reprint count corrected from 25 to 26. Westcott, Alford and Lightfoot `_about` now note the overlap with PR #11.

## 2026-10-03 02:05 CDT — albert-barnes done
- `pipeline/albert-barnes_shelf.json`: CCEL's complete New Testament Notes (32 MB ThML; CCEL keyed it from the Baker 1949 reprint, so it is flagged for a person to check) plus 16 IA volumes of raw OCR, median 97.5% (87.7% for Harper Psalms vol. 3, otherwise 95.0-98.7%), about 49 MB. Title pages were read. Daniel is the 1857 printing and was relabelled. The 1847 Isaiah vol. 2 and one Life at Threescore copy never name Barnes and were swapped for copies that do. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.
- `owen_shelf.json`: per the press thread (PR #15), CCEL's o/owen/glory is a modernised text. It is held through fetch_sources.py, not this shelf, and its `_held` note now says so and points to Goold vol. 1 (owen-works-goold-01, which contains it) and EEBO-TCP A53707.

## 2026-10-03 02:09 CDT — moses-stuart done
- `pipeline/moses-stuart_shelf.json`: 8 IA volumes of raw OCR, median 96.6% (94.9-98.0%), about 11 MB; title pages read (1830-1852). Romans and Hebrews keep their Greek (55,170 and 78,809 Greek characters). I fetched the NT Grammar (1841), found 0 Greek characters and 84.5% OCR, and excluded it, as I did the Hebrew grammars. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 02:14 CDT — increase-mather done
- `pipeline/increase-mather_shelf.json`: 4 IA volumes of raw OCR, median 86.9% (84.0-95.3%; Drake's editions reprint the long s, which the OCR reads as f), about 2 MB; title pages read (1856-1900). Cases of Conscience is held back with Cotton Mather's Wonders. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.
- Round 11 opened at 02:12 CDT with 18 picks in QUEUE-A. thomas-hooker was skipped: IA has only the 1638-48 first printings and modern facsimiles, the one copy that passed read at 77.7% OCR, and three never name him.

## 2026-10-03 02:14 CDT — solomon-stoddard done
- `pipeline/solomon-stoddard_shelf.json`: 2 IA volumes of raw OCR, median 97.6%, about 0.9 MB. The Safety of Appearing's title-page year is unreadable in the OCR, so it is labelled "catalogued 1804". `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 02:16 CDT — john-cotton done
- `pipeline/john-cotton_shelf.json`: 1 IA volume (The Keyes of the Kingdom, 1843 reprint), 95.4% OCR. Nothing else of his turned up in a 19th-century edition. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:16 CDT — samuel-willard done
- `pipeline/samuel-willard_shelf.json`: 1 IA volume, the 1726 folio (1,016 page images, about 6.8 MB), 85.5% OCR. Its long s is read as f, and the title-page numeral is garbled, so it is labelled "catalogued 1726". It is the only pre-1930 copy on IA. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:22 CDT — john-tillotson done
- `pipeline/john-tillotson_shelf.json`: CCEL vols 4-10 of the 1820 Works (CCEL print source: Priestley, 1820) plus IA vols 1-2 of the same edition (98.1% and 98.9% OCR). The copy of vol. 3 that worked is catalogued as vol. 3 but its title page and sermons are vol. X, so it was dropped; the real vol. 3 is pending (HTTP 500). `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 02:22 CDT — thomas-wilson done
- `pipeline/thomas-wilson_shelf.json`: 6 IA volumes of raw OCR, median 98.6% (96.4-99.4%), about 8 MB. Each title page was read (1847, 1847, 1851, 1860, 1859, 1863). Vol. 1 turned out to be Keble's Life of Wilson, part II, and was excluded as Keble's book. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 02:24 CDT — daniel-waterland done
- `pipeline/daniel-waterland_shelf.json`: 9 IA volumes of the 1823 Clarendon Works, raw OCR, median 95.3% (94.5-97.9%), about 9 MB. Each title page shows its volume number and MDCCCXXIII. Two Claremont scans without a volume number (worksofrevdaniel0000wate, _u3f1) were not tried. `--verify --record`: 0 mismatched, 0 rights flags. 0 uids minted.

## 2026-10-03 02:24 CDT — william-wilberforce done
- `pipeline/william-wilberforce_shelf.json`: Gutenberg 25709, A Practical View (0.66 MB). The PG header is not marked copyrighted. Name forms are "william wilberforce" and "w. wilberforce" only, since bare "wilberforce" would also match his son Samuel. `--verify --record`: 0 mismatched. 0 uids minted. `scratchpad mkshelf.py` now accepts a spec with no IA items.

## 2026-10-03 02:30 CDT — j-w-alexander done
- `pipeline/j-w-alexander_shelf.json`: 3 IA volumes of raw OCR, median 97.2% (97.2-98.0%). His title pages print "JAMES W: ALEXANDER" with a colon, so that form was added to the name list. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:31 CDT — gardiner-spring done
- `pipeline/gardiner-spring_shelf.json`: 5 IA volumes of raw OCR, median 97.1% (96.5-98.5%). The two First Things volumes print his name as "gardiner'^pring" and "GARDINER SFRINQ" in the OCR; both are in `_identity_checked` with the reading quoted. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:31 CDT — samuel-miller done
- `pipeline/samuel-miller_shelf.json`: 6 IA volumes of raw OCR, median 95.6% (94.5-97.3%). The Ruling Elder copy carries the Presbyterian Board of Publication imprint, and that Board was founded in 1838, so this printing is later than the 1832 IA catalogues (an inference; its copyright year is illegible). `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:31 CDT — ichabod-spencer done
- `pipeline/ichabod-spencer_shelf.json`: 5 IA volumes of raw OCR, median 98.3% (97.7-98.8%). Sketches 1 names him only in an OCR-mangled copyright line, which is recorded in `_identity_checked`. The first second-series copy tried never names him, so a Toronto copy that does replaced it. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:36 CDT — acted on roving review (cycle 9)
- Westcott: John vol. 2, Hebrews and the Epistles of John swapped for copies whose text layer keeps the Greek: gospelaccordingt02west (80,514 Greek characters), epistletohebrew00westgoog (2nd edition 1892, 176,106) and cu31924074296629 (3rd edition 1892, 79,175). The copies replaced had 0, and are recorded in `_alternates`. The Toronto Epistles of John scan (epistlesofstjohn00westuoft) was refused because its whole text was OCR'd as Greek, English included.
- Lightfoot: Galatians is now cu31924075537088 (tenth edition, a 1921 reprint, 58,702 Greek characters) and Philippians is saintpaulsepistl00ligh (fourth edition 1878, 55,788). The 1878 title page OCR reads "J. BB; BIGHTROOT", recorded in `_identity_checked`. Eadie's Ephesians has no copy with Greek; noted in its `_about`.
- DIGEST-A: the late-reprint CCEL texts (Barnes 1949, Owen 1965-68, Wesley 1951, Lightfoot AF 1956, Calvin Relics 2008) and the modernised Owen Glory are now one item under "Decisions that are yours". The Greek bullet is updated.
- `--verify --record` on b-f-westcott, j-b-lightfoot and john-eadie: 0 mismatched.

## 2026-10-03 02:42 CDT — robert-candlish done
- `pipeline/robert-candlish_shelf.json`: 6 IA volumes of raw OCR, median 98.5% (97.0-99.2%), about 4 MB; title pages read (1854-1875). `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:42 CDT — hugh-martin done
- `pipeline/hugh-martin_shelf.json`: 4 IA volumes of raw OCR, median 98.5%. Jonah names him only as "Dr. Huofh Martin" in the publisher's note and "H. M." under the preface, recorded in `_identity_checked`; it needed retries past HTTP 500. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:42 CDT — george-smeaton done
- `pipeline/george-smeaton_shelf.json`: 3 IA volumes of raw OCR, median 98.5%, about 3.5 MB; title pages read (1868, 1870, 1882). `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:42 CDT — john-kennedy-dingwall done
- `pipeline/john-kennedy-dingwall_shelf.json`: 2 IA volumes of raw OCR, median 98.3%. Gaelic items under his name are left out of this English shelf. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:42 CDT — thomas-mccrie done
- `pipeline/thomas-mccrie_shelf.json`: 4 IA volumes of raw OCR, median 96.6% (93.5-99.0%), about 6 MB. IA catalogues the Works as 1855, but the title pages read 1856 and 1857, and the slugs carry no year. His Life of Knox (Works vol. 1) is left to the Reformers/Knox thread. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:52 CDT — retries
- henry-alford vol. 3 (greektestamentwi03alfo) came through after several HTTP 500s: Rivingtons 1856, 91.1% OCR, 273,536 Greek characters. `--verify --record`: 0 mismatched. Eadie's Thessalonians and Tillotson vol. 3 still return HTTP 500.

## 2026-10-03 02:58 CDT — alexander-maclaren done
- `pipeline/alexander-maclaren_shelf.json`: 19 CCEL ThML texts. Print sources, where CCEL names one: Hodder and Stoughton 1892-1903, Armstrong 1894. None is late. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:58 CDT — charles-finney done
- `pipeline/charles-finney_shelf.json`: 7 CCEL texts. Power from on High is keyed from a 1944 Christian Literature Crusade reprint and is flagged. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:58 CDT — e-m-bounds done
- `pipeline/e-m-bounds_shelf.json`: 7 CCEL texts. Bare "bounds" is never used as a name form. CCEL writes "E.M. Bounds" with no space, so that form was added after Purpose in Prayer was refused on the first pass. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:59 CDT — hannah-whitall-smith done
- `pipeline/hannah-whitall-smith_shelf.json`: 3 CCEL texts. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:59 CDT — r-a-torrey done
- `pipeline/r-a-torrey_shelf.json`: 3 CCEL texts. The Person and Work of the Holy Spirit is keyed from a 1974 Zondervan reprint and is flagged. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 02:59 CDT — horace-bushnell done
- `pipeline/horace-bushnell_shelf.json`: 5 CCEL texts. Print sources, where named: Scribner 1868-76. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 05:40 CDT — a-b-bruce done
- `pipeline/a-b-bruce_shelf.json`: 1 CCEL + 4 IA, all fetched. Title pages read for imprint and year. `--verify --record`: 0 mismatched. OCR 98.4% mean, lowest Humiliation 94.4%. Parabolic Teaching pending (HTTP 500). 0 uids minted.

## 2026-10-03 05:42 CDT — james-denney done
- `pipeline/james-denney_shelf.json`: 3 CCEL texts, print sources Hodder 1894 and a 1911 printing. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 05:45 CDT — review cycle 10 follow-ups
- Bounds' Weapon of Prayer moved to `_pending` (posthumous, date and renewal unverified).
- Title pages read for candlish-ephesians-1875 (A. & C. Black, 1875) and jwalexander-thoughts-preaching-1869 (Scribner, 1869): period printings; recorded in `_rights_checked`.
- Lightfoot Philippians note corrected: the 1873 third edition (stpaulsepistleto00lighuoft) carries 55,039 Greek characters.
- DIGEST: Finney 1944 and Torrey 1974 printings, Bounds hold, round 12 veto points and the PR #14 clash added under Decisions.
- The four PR #14 shelves are held unchanged.

## 2026-10-03 05:47 CDT — four round 11 shelves handed to PR #14
- Removed `george-smeaton`, `hugh-martin`, `john-kennedy-dingwall`, `thomas-mccrie` shelf files: PR #14 owns them and reconciled them in 400f0b9; checked that every source id of this branch's versions is on #14.
- Martin's Jonah corrected to the third edition of 1880 (read from the title page OCR).

## 2026-10-03 05:51 CDT — alexander-whyte done
- `pipeline/alexander-whyte_shelf.json`: 3 CCEL texts, print sources Hodder 1922 and Oliphant Anderson & Ferrier. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 05:51 CDT — h-c-g-moule done
- `pipeline/h-c-g-moule_shelf.json`: 3 CCEL texts, print sources Hodder (1902) and Elliot Stock 1909. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 05:51 CDT — f-b-meyer done
- `pipeline/f-b-meyer_shelf.json`: 3 CCEL texts. CCEL's Daily Homily is volume 2 only (1 Samuel to Job), labelled so; CCEL's Way into the Holiest carries a wrong short title ("Our Daily Homily") in its metadata, but its contents are the Hebrews book. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 05:55 CDT — john-mcleod-campbell done
- `pipeline/john-mcleod-campbell_shelf.json`: 1 CCEL text, print source Macmillan 1905. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 05:55 CDT — d-l-moody done
- `pipeline/d-l-moody_shelf.json`: 1 CCEL + 10 Gutenberg texts; no Gutenberg header carries the COPYRIGHTED marker. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 05:58 CDT — george-muller done
- `pipeline/george-muller_shelf.json`: 5 Gutenberg texts, none marked COPYRIGHTED. Editors read from the texts (Brooks; Wayland for the alternate). `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 05:58 CDT — c-h-mackintosh done
- `pipeline/c-h-mackintosh_shelf.json`: 12 Gutenberg texts, none marked COPYRIGHTED. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 06:00 CDT — phillips-brooks done
- `pipeline/phillips-brooks_shelf.json`: 4 IA + 1 Gutenberg, title pages read. `--verify --record`: 0 mismatched. OCR 99.1% mean. 0 uids minted.

## 2026-10-03 06:04 CDT — richard-watson-methodist done
- `pipeline/richard-watson-methodist_shelf.json`: 2 IA + 1 Gutenberg, title pages read. `--verify --record`: 0 mismatched. OCR 98.1%. 0 uids minted.

## 2026-10-03 06:04 CDT — abraham-booth done
- `pipeline/abraham-booth_shelf.json`: 5 IA volumes, title pages read. `--verify --record`: 0 mismatched. OCR 97.1% mean, lowest Glad Tidings 85.2% (long s). 0 uids minted.

## 2026-10-03 06:10 CDT — henry-hammond done
- `pipeline/henry-hammond_shelf.json`: 8 IA volumes, title pages read. Greek measured per Paraphrase volume: 0 / 36,496 / 0 / 163,028. `--verify --record`: 0 mismatched. OCR 97.4% mean, lowest Misc. Works vol. 2 91.6%. 0 uids minted.

## 2026-10-03 06:14 CDT — robert-sanderson done
- `pipeline/robert-sanderson_shelf.json`: 6 IA volumes, title pages read. Vol. 2 is a "0000"-style id, title page read (Oxford 1854) and recorded in `_rights_checked`; vol. 4's title page OCR reads "Egbert Sanderson", recorded in `_identity_checked`. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 06:14 CDT — review cycle 11 follow-ups
- Bare surname forms dropped: "moody" and "mr. moody" (collided with PR #14's A. Moody Stuart), "mackintosh" (Sir James Mackintosh), "moule" (other Moules). All items still verify on the full forms.
- DIGEST: the Bounds round 12 row now shows six books with Weapon pending; the six undated CCEL print sources (Meyer x3, Bruce, Whyte x2) added under Decisions.

## 2026-10-03 06:21 CDT — george-bull done
- `pipeline/george-bull_shelf.json`: 13 IA volumes, title pages read. Works vol. 7 is the Trinity College copy (the San Marino copy returned HTTP 500). `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 06:22 CDT — James Buchanan name forms
- Bare "buchanan" replaced by full forms (it collided with PR #14's robert-buchanan); all 6 items re-recorded with the author seen as "james buchanan", 0 mismatched.

## 2026-10-03 06:22 CDT — Shepard name forms
- Dropped "shepherd" from the shepard shelf: it is an ordinary English word, and every item had matched on "shepard" anyway. Re-recorded, 0 mismatched.

## 2026-10-03 06:25 CDT — edward-stillingfleet done
- `pipeline/edward-stillingfleet_shelf.json`: 8 IA volumes, title pages read (editors Pantin and Cunningham read from them). `--verify --record`: 0 mismatched. OCR 96.6% mean. 0 uids minted.

## 2026-10-03 06:32 CDT — samuel-horsley done
- `pipeline/samuel-horsley_shelf.json`: 11 IA volumes, title pages read. Hosea is signed "Samuel Lord Bishop of Rochester", recorded in `_identity_checked`. `--verify --record`: 0 mismatched. OCR 95.5% mean. 0 uids minted.

## 2026-10-03 06:33 CDT — thomas-sherlock done
- `pipeline/thomas-sherlock_shelf.json`: 5 IA volumes (vol. 3 from the Princeton copy after an HTTP 500). `--verify --record`: 0 mismatched. OCR 98.6% mean. 0 uids minted.

## 2026-10-03 06:40 CDT — benjamin-keach done
- `pipeline/benjamin-keach_shelf.json`: 5 IA volumes. Tropologia's OCR never shows the name; its title page was looked at by eye (page image n5) and recorded in `_identity_checked`. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 06:40 CDT — john-ryland done
- `pipeline/john-ryland_shelf.json`: 2 IA volumes. Two IA items catalogued under him are by others (his father; Andrew Fuller) and are excluded. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 06:40 CDT — matthew-mead done
- `pipeline/matthew-mead_shelf.json`: 1 IA volume. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 06:48 CDT — gilbert-tennent done
- `pipeline/gilbert-tennent_shelf.json`: 2 IA volumes, title pages read. `--verify --record`: 0 mismatched. OCR 83.8% (long s). 0 uids minted.

## 2026-10-03 06:48 CDT — lyman-beecher done
- `pipeline/lyman-beecher_shelf.json`: 4 IA volumes. `--verify --record`: 0 mismatched. OCR 98.5%. 0 uids minted.

## 2026-10-03 06:48 CDT — francis-asbury done
- `pipeline/francis-asbury_shelf.json`: 3 IA volumes. `--verify --record`: 0 mismatched. OCR 98.1%. 0 uids minted.

## 2026-10-03 06:48 CDT — richard-cecil done
- `pipeline/richard-cecil_shelf.json`: 2 IA volumes. `--verify --record`: 0 mismatched. OCR 98.9%. 0 uids minted.

## 2026-10-03 06:49 CDT — review cycle 12 follow-ups
- Horsley: dropped the name form "samuel, lord bishop" (any Bishop Samuel would match). The 1789 Tracts then failed, because its title page names him only by his see ("Samuel, Lord Bishop of St. David's"). That reading is now in `_identity_checked`, and the re-record shows 0 mismatched. Commit 2e7ba2e had briefly pushed the shelf without that reading, and with a stale record.
- Nettleton had already been dropped from the queue (skipped; PR #14 owns him).

## 2026-10-03 06:55 CDT — pending items retried
- A. B. Bruce: added The Parabolic Teaching of Christ, 4th ed. (Hodder, 1891). The id is "0000"-style; its title page was read and recorded in `_rights_checked`.
- Richard Cecil: added Memoirs of the Rev. John Newton (New York, 1809), whose text now loads.
- Phillips Brooks: The Purpose and Use of Comfort is the First Series of Sermons retitled, so it is an alternate, not pending.
- Still HTTP 500: Eadie's Thessalonians, Tillotson Works vol. 3.
- Poole and Trapp marked skipped in QUEUE-A: PR #14 shelves them from EEBO first printings.

## 2026-10-03 06:58 CDT — full name forms (Lane D's audit)
- owen, newton, john-preston and watts now gate on full forms ("john owen", "john newton", "john preston", "isaac watts", with title-page variants). The bare forms collided with Lane D authors (Elias Owen, Horace Newton Allen, Josephine Preston Peabody), and "watts" was weak in the same way. Owen, Newton and Watts re-recorded: 0 mismatched. Preston holds no entries to re-record. Perkins already used full forms.

## 2026-10-03 06:59 CDT — Andrew Murray translators
- The New Life and The Lord's Table are translations from the Dutch. They are now recorded in `_translator_unchecked`, the key 40 shelves already use. The New Life's preface is signed only "J.P.L." (Arbroath, 1891). The Lord's Table names no translator.

## 2026-10-03 07:13 CDT — ralph-wardlaw done
- `pipeline/ralph-wardlaw_shelf.json`: 11 IA volumes, title pages read; Ecclesiastes vol. 2 is a "0000"-style id, an 1821 original (`_rights_checked`). `--verify --record`: 0 mismatched. OCR 98.8%. 0 uids minted.

## 2026-10-03 07:13 CDT — james-haldane done
- `pipeline/james-haldane_shelf.json`: 5 IA volumes, title pages read; two IA catalogue dates (2002) contradicted by the title pages, one "0000"-style id, all recorded in `_rights_checked`. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 07:15 CDT — john-foster-essayist done
- `pipeline/john-foster-essayist_shelf.json`: 1 Gutenberg (not COPYRIGHTED) + 7 IA, title pages read. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-03 07:16 CDT — edward-bickersteth done
- `pipeline/edward-bickersteth_shelf.json`: 7 IA volumes, title pages read (Scripture Help is a "0000"-style id, an 1821 copy, in `_rights_checked`). `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 21:57 CDT — henry-melvill done
- `pipeline/henry-melvill_shelf.json`: 7 IA volumes. Public Occasions (1846) failed the name gate on an OCR artifact ("HENRY 'MELVILL"); title page read, recorded in `_identity_checked`. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 21:57 CDT — daniel-wilson-calcutta done
- `pipeline/daniel-wilson-calcutta_shelf.json`: 7 IA volumes. Evidences vol. 1 failed the name gate on an OCR artifact ("DANIEL ^WILSON"); title page read (year OCR'd "1329" = 1829), recorded in `_identity_checked`. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 22:03 CDT — j-b-mozley done
- `pipeline/j-b-mozley_shelf.json`: 8 IA volumes. Augustinian Predestination failed the name gate on letterspaced OCR ("M 0 Z L E Y"); title page read, recorded in `_identity_checked` instead of adding a garbled name form. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 22:03 CDT — r-w-church done
- `pipeline/r-w-church_shelf.json`: PG 12092 + 9 IA volumes. Gifts of Civilisation failed the name gate on OCR artifacts ("R[ W. CHURCH"); title page read, recorded in `_identity_checked`. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 22:10 CDT — norman-macleod done
- `pipeline/norman-macleod_shelf.json`: 3 PG + 4 IA. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 22:10 CDT — john-cairns done
- `pipeline/john-cairns_shelf.json`: 5 IA. Unbelief failed the name gate on OCR ("JOHN CAIKNS"); title page read, in `_identity_checked`. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 22:10 CDT — marcus-dods done
- `pipeline/marcus-dods_shelf.json`: 5 CCEL + 3 IA. Mohammed, Buddha and Christ failed the name gate on OCR ("MARC US DODS"); title page read, in `_identity_checked`. CCEL Genesis print source has no year and Like Christ none: the fetcher does not flag these (that is the PR #14 patch still awaiting Adam). `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 22:17 CDT — a-b-davidson done
- `pipeline/a-b-davidson_shelf.json`: 8 IA. Hebrews has no year on its title page (catalogued 1900; "1907-1932" in the OCR is a bookplate). Grammar and Syntax: Hebrew OCR unusable, recorded as such. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 22:17 CDT — george-matheson done
- `pipeline/george-matheson_shelf.json`: 9 IA. Natural Elements failed the name gate on OCR ("GEOEGE MATHESON"); title page read, in `_identity_checked`. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 22:17 CDT — henry-boynton-smith done
- `pipeline/henry-boynton-smith_shelf.json`: 4 IA (Apologetics is a "0000"-style id; title page reads 1882). `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 22:17 CDT — jonathan-dickinson done
- `pipeline/jonathan-dickinson_shelf.json`: 3 IA (True Scripture Doctrine is a "0000"-style id; title page reads 1841). `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 22:19 CDT — john-davenport done
- `pipeline/john-davenport_shelf.json`: 5 IA, four of them Early English Books scans with poor OCR (labelled). Power of Congregational Churches failed the name gate on OCR ("Joun DaVENPORT"); title page read, in `_identity_checked`. Catechisme excluded (OCR noise); Civil Government excluded (Cotton). `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-09 22:20 CDT: round 14 complete, lock released
- 16 shelves this round (4 on 2026-10-03, 12 on 2026-10-09 after Adam's restart). Every shelf: all remote branches checked for shelf-name and source-id clashes, `--verify --record` 0 mismatched, 0 uids minted. Stopped at the end of the round as asked.

## 2026-10-10 09:25 CDT — james-petigru-boyce done
- `pipeline/james-petigru-boyce_shelf.json`: 1 CCEL, 0 PG, 0 IA. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-10 09:25 CDT — john-l-dagg done
- `pipeline/john-l-dagg_shelf.json`: 0 CCEL, 0 PG, 3 IA. Title pages read for dagg-evidences-1869 (OCR garbles the name), recorded in `_identity_checked`. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-10 09:25 CDT — john-a-broadus done
- `pipeline/john-a-broadus_shelf.json`: 0 CCEL, 0 PG, 8 IA. Mark 1905 is a "0000"-style id; its title page shows the April 1905 first printing, recorded in `_rights_checked`. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-10 09:25 CDT — joseph-milner done
- `pipeline/joseph-milner_shelf.json`: 0 CCEL, 0 PG, 3 IA. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-10 09:25 CDT — francis-wayland done
- `pipeline/francis-wayland_shelf.json`: 0 CCEL, 0 PG, 12 IA. Title pages read for fwayland-intellectual-philosophy-1854 (OCR garbles the name), recorded in `_identity_checked`. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-10 09:25 CDT — adam-clarke done
- `pipeline/adam-clarke_shelf.json`: 1 CCEL, 0 PG, 14 IA. Commentary is 42 MB of OCR, the largest set this lane holds. `--verify --record`: 0 mismatched. 0 uids minted.

## 2026-10-10 09:25 CDT — william-burt-pope done
- `pipeline/william-burt-pope_shelf.json`: 0 CCEL, 0 PG, 7 IA. Title pages read for wbpope-compendium-1, wbpope-prayers-st-paul-1876 (OCR garbles the name), recorded in `_identity_checked`. `--verify --record`: 0 mismatched. 0 uids minted.
