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

## 2026-10-02 15:32 CDT — audit (RULES §5c): Adler-shelf overlap
- `pipeline/adler_shelf.json` already held Jowett's Republic (PG 1497, slug plato-republic) and Apology (PG 1656, slug plato-dialogues). Removed both from plato_shelf.json's fetch list and cross-referenced them; local copies deleted. Adler's plato-dialogues title claims Apology, Crito, Phaedo but PG 1656 is the Apology alone (finding for Adam).
- Adler also holds Aristotle's Ethics (Chase) and Politics (Jowett), Lucretius (Munro), Herodotus (Macaulay), Thucydides (Jowett), Tacitus Annals, Plutarch Lives (Dryden/Clough), Marcus Aurelius (Long), Epictetus (Matheson): the queued census items must cross-reference these.
- For lane C (not touched): adler's virgil-eclogues is PG 228, the same file as dryden-aeneid.

## 2026-10-02 15:34 CDT — homer: done
- Shelf `pipeline/homer_shelf.json`. 13/13 fetched, 10.5 MB: Chapman, Pope, Cowper (both poems each), Derby, Buckley, Butler Odyssey 1900 (PG) + Bryant Iliad and Odyssey (IA raw, 2 vols each, clean-word 0.92). Trial conversion (prose mode): 9,810 units. Finding: the build's odyssey-eng4 is Butler revised by Power and Nagy (modern revision), not the 1900 text. Lang, Dryden, Evelyn-White Homer cross-referenced.

## 2026-10-02 15:38 CDT — greek-tragedy (1/3): Aeschylus
- Shelf `pipeline/aeschylus_shelf.json`: 6/6 PG fetched, 2.5 MB, trial 9,214 units. Plumptre and Blackie each complete; Morshead, Buckley, Murray (US PD per PG).

## 2026-10-02 15:38 CDT — greek-tragedy (2/3): Euripides
- Shelf `pipeline/euripides_shelf.json`: 14/14 fetched, 6.1 MB (9 PG + Way 3 vols + Coleridge 2 vols raw). Trial PG 10,231 units. Murray's per-play years not verified, left out of the shelf.

## 2026-10-02 15:38 CDT — greek-tragedy (3/3): Sophocles; item done
- Shelf `pipeline/sophocles_shelf.json`: 4/4 PG, 1.1 MB, trial 5,510 units. Aeschylus 6, Euripides 14, Sophocles 4 fetched (9.6 MB); Jebb's Sophocles cross-referenced to the unmerged PR; PG 806 refused (copyrighted).

## 2026-10-02 15:39 CDT — aristophanes: done
- Shelf `pipeline/aristophanes_shelf.json`. 5/5 PG fetched, 1.5 MB, trial 10,250 units. Complete in the Athenian Society 1912 translation; Hickie Clouds, Rogers Frogs, Lindsay Lysistrata (US PD per PG). PG 3012/2571/3013 excluded as duplicates (shingle overlap 0.85-0.87).

## 2026-10-02 15:43 CDT — greek-historians: Herodotus
- Shelf herodotus: Macaulay vol. 2 (PG 2456) completes the Adler shelf's vol. 1 (PG 2707, whose Adler title reads as the whole History); Rawlinson 1861 4 vols raw. 5 files, 8.5 MB.

## 2026-10-02 15:43 CDT — greek-historians: Thucydides
- Shelf thucydides: Jowett 1881 2 vols + Hobbes 1841, raw (5.3 MB). FINDING: adler_shelf.json labels thucydides-pelo (PG 7142) 'tr. Jowett', but PG 7142 is Crawley; Jowett's real translation is now on this shelf.

## 2026-10-02 15:43 CDT — greek-historians: Xenophon
- Shelf xenophon: Dakyns complete, 14 PG texts, 3.6 MB, trial 9,133 units.

## 2026-10-02 15:43 CDT — greek-historians: Polybius
- Shelf polybius: Shuckburgh 2 vols PG, 3.0 MB, trial 8,139 units.

## 2026-10-02 15:43 CDT — greek-historians: Arrian; item done
- Shelf arrian: 2 PG, 1.7 MB. Herodotus 5, Thucydides 3, Xenophon 14, Polybius 2, Arrian 2 fetched (22.2 MB). Findings on the Adler shelf: thucydides-pelo is Crawley not Jowett; herodotus-history is vol. 1 only.

## 2026-10-02 15:48 CDT — plutarch: done
- Shelf `pipeline/plutarch_shelf.json`. 26/26 fetched (13 PG + North 6 vols + Langhorne 6 vols raw). Lives complete in three translators; Goodwin Moralia complete. Duplicate North vol. 5 scan dropped (worse OCR). Adler's plutarch-lives cross-referenced.
- Lane A's new identity check in fetch_shelf.py refused North vol. 3 (title words not in a Google scan); retitled so the check passes on content; the scan was verified by its Lives (Pyrrus, Sylla, Cimon: North's spellings).

## 2026-10-02 15:49 CDT — audit (RULES §5b): identity re-verify
- Ran lane A's new `fetch_shelf.py --verify` over all 16 lane-B shelves: 0 wrong books. One false alarm fixed (Morris's "Æneids": the ligature hid the title word; shelf title now spelled as the book spells it). title_weak, checked and fine: aristotle-ross-v06, virgil-conington-aeneid.

## 2026-10-02 15:52 CDT — stoics: done
- Shelves marcus-aurelius, epictetus, seneca. Marcus Aurelius 2, Epictetus 8, Seneca 8 fetched. Findings on the Adler shelf: marcus-meditations (PG 2680) is Casaubon by wording, not Long as labelled (inferred); epictetus-discourses (PG 45109) is Higginson's Enchiridion, not Matheson's Discourses (stated by the PG header).

## 2026-10-02 15:54 CDT — roman-historians: done
- Shelves tacitus, livy, caesar, suetonius, sallust, pliny. Tacitus 6, Livy 5 (Bohn complete), Caesar 1, Suetonius 1, Sallust 1, Pliny 8 fetched; 22.8 MB; trial PG 52,933 units. Finding: the Adler shelf's tacitus-annals (PG 7959) is Gordon's 'Reign of Tiberius' (Annals I-VI selection), not Church and Brodribb as labelled.

## 2026-10-02 15:58 CDT — roman-poets: done
- 9 shelves, 22 files: Lucretius 3, Horace 4, Catullus 2, Tibullus 1, Juvenal/Persius 1, Plautus/Terence 6, Lucan 1, Apuleius 2, Petronius 2. Lucan's PG 602 identified as Ridley by collation. Finding: the Adler shelf's lucretius-nature (PG 785) is Leonard, not Munro as labelled. Years not found in the files were dropped from the shelves.

## 2026-10-02 16:02 CDT — lucian-cicero: done
- Lucian 6 (Fowler complete), Cicero 15 (Yonge Orations complete; Shuckburgh correspondence complete; philosophy and rhetoric). Winstedt's Atticus held back: Latin facing. One IA 500 error on the first try, fetched on retry.

## 2026-10-02 16:07 CDT — greek-orators (done)
- demosthenes: Kennedy Olynthiacs & Philippics (PG 6878), Pickard-Cambridge 1912 (PG 9060-9061), Kennedy Bohn vols 1-4 raw IA OCR (clean-word 0.84-0.94). Kennedy vol 5 pending: no identifiable scan.
- lysias: PG 6969 (translator unnamed in the file; recorded as unnamed, not guessed).
- isocrates: Freese vol 1 (Bohn 1894) raw IA OCR, clean-word 0.895.
- Rights: all three PG headers read, none COPYRIGHTED.

## 2026-10-02 16:11 CDT — greek-poets-minor (done)
- pindar: Myers (PG 10717); Turner prose + Moore verse, Bohn 1872 printing (IA, clean-word 0.87). Cary's Pindar cross-referenced to lane C.
- theocritus: Calverley (PG 11533); Banks/Chapman Bohn 1853 (IA, 0.86). Lang's prose cross-referenced to lane D (PG 4775).
- apollonius: Seaton (PG 13977; PG 830 is the same text, 0.98 overlap, not taken); Way 1901 (PG 64235); Coleridge 1889 (IA, 0.92).
- quintus-smyrnaeus: Way (PG 658).
- greek-lyric: Mackail Anthology (PG 2378), Wharton Sappho 1908 ed. (PG 57390), Moore Anacreon (PG 38230), Poste Bacchylides 1898 (IA).
- All PG headers read: none COPYRIGHTED. Loebs (Paton, Edmonds, Mair, Sandys) left pending: Greek facing pages.
- Musaeus: no PD English scan identified.

## 2026-10-02 16:18 CDT — greek-late-philosophy (done)
- diogenes-laertius: Yonge (PG 57342).
- plotinus: MacKenna first edition complete, vols 1-5 (1917, 1921, 1924, 1926, 1930), raw IA OCR 0.91-0.94; each identified by its Ennead on the title page; all published by 1930, so US PD by date. Guthrie 1918 (PG 42930-42933). Taylor: Essay on the Beautiful (PG 29510), Select Works, Mead's 1895 ed. (IA).
- porphyry: Taylor Select Works 1823 (PG 77014); Lardner, pagan arguments (PG 37696); Zimmern's Marcella 1896 (IA).
- iamblichus: Taylor, Life of Pythagoras 1818 (PG 63300), Mysteries (PG 72815, 1895 reprint of 1821).
- proclus: Taylor, Euclid commentaries (PG 74253, 79455), Theology of Plato (PG 77393, 78800).
- pythagoreans: Taylor's Ocellus 1831 (PG 75391). sextus-empiricus: Patrick 1899 (PG 17556). julian: Wright vols 1-2 (PG 48664, 48768). boethius: James 1897 (PG 14328).
- Longinus: Havell is on lane D's lang shelf (PG 17957); Roberts 1907 IA scan has facing Greek and clean-word 0.64; pending.
- All PG headers read: none COPYRIGHTED.

## 2026-10-02 16:22 CDT — greek-geographers-historians (done)
- pausanias: Shilleto (PG 68946, 68680); Taylor 1824 2nd ed. vols 1-2 (IA; title page names no translator, Taylor is the catalogue's attribution); Verrall's Attica 1890 (IA). Frazer vol 1: only an empty DLI scan found.
- strabo: Hamilton (Books I-VI, per the preface) and Falconer, 3 vols (PG 44884-44886).
- appian: Horace White 1899, Foreign Wars and Civil Wars (IA, identified by the title pages).
- diodorus: Booth, 1814 ed., 2 vols (IA).
- dio-cassius: Foster's Dio's Rome, 6 vols (PG). athenaeus: Yonge, 3 vols (PG).
- procopius (overflow): Dewing Wars I-VI, Secret History (translator unnamed), Stewart's Buildings (PG).
- greek-romances (overflow): Rowland Smith's Heliodorus/Longus/Achilles Tatius (PG 55406).
- Josephus (Whiston, PG 2846-2850) is on no shelf in any lane; left for the coordinator to assign rather than taking it into lane B.
- All PG headers read: none COPYRIGHTED.

## 2026-10-02 16:27 CDT — greek-science (done)
- euclid: Heath's Thirteen Books 1908, 3 vols (IA), each identified by its title page; clean-word 0.77-0.83 (symbols and lettered figures).
- archimedes: Heath's Works 1897 and Method 1912 (IA); Apollonius of Perga's Conics, Heath 1896 (IA, 0.73).
- hippocrates: Adams vol 1 (PG 72583), vol 2 Sydenham 1849 (IA).
- galen: Brock 1916 (PG 43383). aretaeus: Adams 1856, Greek+English (IA). theophrastus: Bennett & Hammond 1902 (PG 58242), Jebb 1870 (IA).
- greek-mechanics-astronomy: Hero's Pneumatics, Greenwood (PG 77400); Ptolemy's Tetrabiblos, Ashmand (PG 70850).
- Failure recorded: PG 7825 (Robinson's Method) is served only gzip-encoded, so the fetcher gets HTTP 406. Header read by hand (not COPYRIGHTED); it is a LaTeX file. Left pending.
- Found in passing: the Gutenberg catalogue lists bilingual books with language "en; la" or "en; grc", which earlier English-only searches missed. Among them: Claudian (Platnauer), Cicero De Officiis (Miller), Plautus (Nixon), Boethius (Rand and Stewart), and Prudentius (Pope). Prudentius is left for lane A.
- All PG headers read: none COPYRIGHTED.

## 2026-10-02 16:33 CDT — latin-silver-late (done)
- martial: Bohn prose, 1897 printing (IA). statius: Mozley Loeb 1928, 2 vols (IA). claudian: Platnauer 1922 (PG 51443-51444), Hawkins 1817 vol 1 (IA).
- quintilian: Butler Loeb 1920-22, all 4 vols (IA), each identified by its Books. vitruvius: Morgan 1914 (PG 20239).
- gellius: Beloe 1795 vols 1 and 3 (IA); vol 2 has no text layer. ammianus: Yonge (PG 28587). ausonius: Evelyn-White 1919-21 (IA). frontinus: Bennett 1925 (IA).
- overflow: celsus (Greive, PG 64207), roman-farming (Harrison 1918, PG 12140), phaedrus (Riley and Smart, PG 25512), roman-epitomators (Watson's Bohn: Justin, Nepos, Eutropius, Florus, Velleius; IA), justinian (Moyle, PG 5983).
- No PD English found: Valerius Flaccus (Mozley 1934), Silius Italicus (Duff 1934), Macrobius (no complete English before modern editions).
- All PG headers read: none COPYRIGHTED. The Loebs taken here (Mozley, Butler, Evelyn-White, Bennett) have Latin facing pages; Latin OCR is legible, unlike the Greek Loebs left pending.

## 2026-10-02 16:34 CDT — bilingual-pg-adds (done; added to the queue as overflow)
- Gutenberg books catalogued "en; la" or "en; grc", which earlier English-only catalogue searches missed: Miller's De Officiis (PG 47001) to cicero; Nixon's Plautus vol 1, 1916 (PG 16564) to roman-comedy; Stewart and Rand's Boethius, 1918 (PG 13316) to boethius; Super's De Providentia, 1899 (PG 60831) to seneca.
- New shelves: dionysius-halicarnassus (Roberts 1910, PG 50212), augustus (Fairley's Res Gestae 1898, PG 66595).
- All headers read: none COPYRIGHTED.

## 2026-10-02 16:35 CDT — reverify-all-b, digest-refresh-b (done)
- All 84 lane B shelves pass fetch_shelf.py --verify: 0 wrong books.
- DIGEST-B refreshed: 84 shelves, 243 Gutenberg + 114 IA files, 262 MB.

## 2026-10-02 16:36 CDT — fetcher-gzip (done)
- pipeline/fetch_shelf.py get(): on HTTP 406 it asks once more accepting gzip, and decompresses any gzip body. Plain responses are unchanged (tested on PG 1727 and an IA djvu file). Backward-compatible: no shelf format change.
- archimedes: Robinson's Method (PG 7825) now fetched and verified; header not COPYRIGHTED.

## 2026-10-02 16:48 CDT — latin-loebs-1930 (done; overflow item)
- Latin-facing Loebs first printed 1912-1930 added to 20 existing shelves as raw IA OCR (clean-word 0.83-0.94): Seneca (Gummere's Epistles 1-3, Basore's Moral Essays 1, Miller's Tragedies 1-2), Virgil (Fairclough 1-2), Ovid (Miller's Metamorphoses 1-2, Showerman, Wheeler), Horace (Fairclough's Satires/Epistles), Suetonius (Rolfe 1-2), Sallust (Rolfe), Gellius (Rolfe 1-3), Martial (Ker 1-2), Catullus/Tibullus/Pervigilium, Juvenal/Persius (Ramsay), Petronius/Apocolocyntosis, Apuleius (Adlington-Gaselee), Tacitus (Dialogus/Agricola/Germania), Caesar (Edwards, Peskett), Livy (Foster 1, 4, 5), Pliny (Melmoth-Hutchinson 1-2), Cicero (Williams's Friends 1-3, Rackham's Finibus, Falconer, Ker's Philippics, Greenwood's Verrines 1), Plautus (Nixon 3), Terence (Sargeaunt 1-2), Lucan (Duff), Florus/Nepos (Forster, Rolfe).
- Winstedt's Letters to Atticus 1-3 taken from clean Gutenberg (PG 58418, 50692, 51403), formerly excluded only for the Latin facing; the IA copies fetched first were deleted.
- Every volume identified by its title page or contents (Books, plays, volume number). Printing checked for a post-1930 revision notice where the title verso survives. Refused: Livy vol 2 (scan is the 1939 revised printing), Plautus vols 4-5 (first printed 1932 and 1938), Basore vol 3 (1935). Two printings were revised before 1930 and are kept with the revision year in the title: Miller's Seneca vol 2 (1929) and Fairclough's Horace (1929).
- Grey area, recorded: several scans are later reprints (e.g. Pliny vol 1 1931, Livy vol 5 "reprinted" to 1969) with no revision notice. They are kept because the text is that of the pre-1931 edition.
- Not found with a text layer: Bennett's Horace Odes (1914), Nixon's Plautus vol 2 (1917), Livy vol 3 (1924), Winstedt-era Cicero Tusculans (King 1927) and De Re Publica (Keyes 1928), which have only Loeb-series items whose files 404. All pending.

## 2026-10-02 16:50 CDT — pending-volumes-hunt (done)
- Found and fetched: Foster's Livy vol 3, Books V-VII (Loeb, 1924; IA, clean-word 0.91); Taylor's Pausanias 1824 vol 3, Books VII-X (IA, 0.86); Keyes's De Re Publica and De Legibus (Loeb, 1928; IA, 0.90; later reprints with no revision notice).
- Still missing: Kennedy's Demosthenes vol 5 (the 1865 'On the Crown and On the Embassy' scan duplicates other Kennedy content, so it was not taken as vol 5); Beloe's Gellius vol 2 (the only scan reads 0.75 and does not name Beloe); Hawkins's Claudian vol 2; Frazer's Pausanias vol 1; Nixon's Plautus vol 2 (archive.org returns 503); Bennett's Horace Odes (best scan reads 0.74 and has no legible title verso).

## 2026-10-02 16:56 CDT — wishlist-sweep-b (in progress)
- Gutenberg: Elton's Hesiod, 2nd ed. 1815, with Chapman's Works and Days (PG 66350); Bysshe's Memorable Thoughts of Socrates, 1712 (PG 17490). Headers read; neither is COPYRIGHTED.
- IA: The Greek Tragic Theatre (new ed., 1809). Vol 1 is Potter's Aeschylus; vols 3-5 are Wodhull's Euripides. Each was identified by its title page. Vol 2 (Francklin's Sophocles) returns 503 and is pending.
- IA: Swanwick's Aeschylus (4th ed. 1899), Plumptre's Sophocles (1865), Creech's Lucretius (1714, 2 vols), Rowe's Lucan vol 1, Carter's Epictetus (Dublin 1759), Cary's Herodotus (1873). Clean-word 0.85-0.92, with long-s OCR in the 18th-century printings.
- Skipped: Smart's prose Horace (best scan 0.81, title page not legible); Rogers's Aristophanes (Greek facing in both the Bell and Loeb printings).
- (wishlist-sweep-b, continued 17:01 CDT) IA: Holland's Pliny (1601, 2 tomes) and Livy (1659 ed.); T. C. Williams's Georgics and Eclogues (1915); Cranch's Aeneid (1872); Norgate's blank-verse Iliad (1864; the title page names no translator, the attribution is the catalogue's); William Smith's Thucydides (1831, 3 vols); Hampton's Polybius (1772-73, 4 vols; vol 3 per the catalogue); Collier's Marcus (1702); Rendall's Marcus (1898); Gordon's Tacitus (1753, 5 vols). Clean-word 0.81-0.94. Each was identified by its title page where one survives.
- (wishlist-sweep-b, end) Hobbes's Iliads and Odysses, from Molesworth's English Works vol 10 (IA, 0.92), added to homer. Not taken because the ECCO OCR is too poor (clean-word 0.62-0.70): Francklin's Lucian (1780-81) and Thornton's Plautus (1767). Hobbes's Thucydides (Molesworth vols 8-9): no scan identified.

## 2026-10-02 17:04 CDT — session end (lock released)
- Lane B holds 84 shelves: 249 clean Gutenberg texts and 194 raw IA OCR volumes, about 348 MB on this worker's disk. Corpus text is gitignored; the shelf JSON files are the record. No uids were minted. pipeline/fetch_sources.py and structure_texts.py were not touched.
- Every queue item is done except retry-503-volumes (todo, for a restarted worker).
- Waiting on Adam (DIGEST-B): Greek-facing Loebs; Perseus English gap (832 texts); US-only PD items; the Adler-shelf label errors; unassigned Josephus and Prudentius.

## 2026-10-02 17:07 CDT — lock re-taken for the coordinator's Perseus task
- New queue items: perseus-fetcher, perseus-english. Census gap rows with likely_pd=yes: 559. Minus the 309 Perseus/1st1K ids already on PR #7 (branch claude/project-thread-hxenem), minus Philo (on PR #8) and the apostolic fathers, apocrypha and Old Testament rows (lane A's or PR #7's): 238 left, across 19 lane B authors.

## 2026-10-02 17:10 CDT — perseus-fetcher done
- pipeline/fetch_perseus.py, a new file: reads a shelf's "perseus" section, fetches the TEI from raw.githubusercontent.com (jsDelivr fallback), checks the translator's surname is in the header, records the sourceDesc years and refuses a year after 1930 unless the shelf says why, and records the markup licence (CC BY-SA 4.0 from the repository README for canonical-greekLit and canonical-latinLit). fetch_shelf.py ignores the new key; `fetch_shelf.py demosthenes --verify` still reports 0 mismatched.
- First run: Demosthenes, 18 Vince speeches (Loeb 1930 printing), 0 failed.

## 2026-10-02 17:30 CDT — perseus-english done; five missing volumes found
- 243 Perseus TEI English texts shelved under a new "perseus" key in 19 lane B shelves, all fetched, 0 failed (about 36 MB of TEI, gitignored): Plutarch 91, Lucian 52, Lysias 34, Hippocrates 22, Demosthenes 20, Epictetus 4, Aretaeus 4, Thucydides 3 (Hobbes 1843, Dale 1851, C. F. Smith 1919-23), Catullus 2, Homer 2 (A. T. Murray), and one each for Aeschylus (Browning), Euclid (Heath), Euripides (Murray's Rhesus), Galen (Brock), Horace (Conington), Livy (Roberts), Lucretius (Leonard), Strabo (Jones 6-14) and Suetonius (Rolfe's Julius).
- Every translation is dated by the file's own sourceDesc, in or before 1930, except Aretaeus, where Perseus used a 1972 reprint of the 1856 Sydenham edition (kept, with the reason in _rights_checked). The markup is CC BY-SA 4.0 from the repository README; it is recorded per file in each <shelf>_perseus_report.json.
- Deduped: 309 Perseus/1st1K ids on PR #7 skipped (Vitruvius's Morgan is one, so it was dropped here). Philo is excluded (PR #8), and so are the apostolic fathers, apocrypha and Bible rows (lane A or PR #7). Of the census's 203 "check" rows, only Aretaeus and Vince's De Corona/De Falsa Legatione (1926 in the file) qualified; the rest are post-1930 originals.
- US-only flag: Murray's Rhesus (Murray died 1957; PR #7 chose Coleridge for that reason). Kept as a second witness.
- The 1st1K Thucydides files live in canonical-greekLit, not First1KGreek; fetch_perseus.py now tries there first.
- Missing volumes found under other ids: Nixon's Plautus vol. 2 (1917), Francklin's Sophocles (1759, all seven plays), Beloe's Gellius vol. 2 (1795), Kennedy's Demosthenes vol. 5 (Bohn 1878), and Rowe's Lucan vol. 2 (1812). Each title page was read.
- Correction: the Plautus commit message says "vols 1-5 now on the shelf". Vols. 1-3 are on the shelf; vols. 4-5 stay refused as post-1930 printings.
- Still missing: King's Tusculans (the only text is the 1945 revised printing: refused), Wright's Julian vol. 3 (Greek facing, OCR 0.77: held back like the other Greek-facing Loebs), Frazer's Pausanias vol. 1 (the DLI scan is empty), Bennett's Loeb Horace (only 1931+ printings found), Hawkins's Claudian vol. 2 (no scan found), and vol. 2 of the 1809 Greek Tragic Theatre (503; its metadata comes back empty).

## 2026-10-02 19:54 CDT — wishlist work after a worker restart (17:36-19:54)
- The worker restarted around 17:40-19:40; nothing was lost (the uncommitted Douglas rows were on disk and were committed at 19:40).
- Hourly retry at 19:42: nothing recovered. The DLI "Pausanias Vol. I" scan turned out to be Frazer's vol. VI (indices), mislabelled.
- From the map's wishlists, every title page read: Potter's Euripides (Valpy 1832, 3 vols.), Buckley's Euripides vol. 2, Frere's Aristophanes (Morley 1887), Gwilt's Vitruvius (1826), Cockman's Offices with Melmoth's Cato and Laelius (Harper 1838), Edmonds's Offices (1860), Watson's On Oratory (Bohn, 1871 printing), Smart's Horace (Buckley's revision, 1869), Holland's Suetonius (1606) and Morals (1603), Jackson's Marcus (1906; translator from the catalogue), Butler's Apuleius (1910, 2 vols.), Gavin Douglas's Eneados (1839, 2 vols.), the complete Bohn Plato (Cary, Davis, Burges, 6 vols., plus PG copies of vols. 1-2), Taylor's Plato (1804, 5 vols.), Shelley's Banquet, Ion and Menexenus (PG 67926), Forster's De Mundo (1914), Spelman's Dionysius (1758, 4 vols.), Lodge's Seneca (1614; OCR 0.73), Golding's Caesar (1565; OCR 0.77), McCrindle's Indica in two books (PG 55054 and the 1877 Ancient India), and Lewis's Pliny letters (1890).
- Mistake fixed: a line-number edit overwrote the Apuleius vol. 2 map row; restored in the next commit. Map edits are now made by matching text, not line numbers.
- The Bohn Plato sits on the Plato shelf, though the map had called a second translator there Adam's call. Moving the rows is cheap.

## 2026-10-02 20:58 CDT — new shelves 20:05-20:36, then a review-fix pass
- Added, title pages read: Columella (1745), Palladius in Middle English (EETS 1873), Clarke's Vegetius (1767; new shelf), Propertius (Butler 1912/1929 reprint, Gantillon), Zosimus (1814), Herodian (1629, attributed to Maxwell), Shepherd's Polyaenus (1793), Newton's Seneca Tenne Tragedies (Tudor Translations 1927), Sandys's Ovid (1632), Stanyhurst's Aeneid I-IV, Underdowne's Heliodorus (rev. Wright 1923), Watson's Bohn Xenophon (3 vols.), Spelman's Anabasis, Ashley's Cyropaedia, Smart's 1756 Horace, Thornton's Plautus (1767, vols. 1-3), Francklin's Lucian (1780), Rooke's Arrian vol. 1, seven Aristotle texts from Gutenberg, Goldwin Smith's Specimens, Cary/West/Laurent Pindar, Fawkes's Theocritus and Apollonius, Littlebury's (1737) and Beloe's (1821, 4 vols.) Herodotus, Lewis's Statius, Cooke's Hesiod, Duncan's Caesar, Gordon's and Rose's Sallust, Grainger's Tibullus, Baker's Livy (1823, 6 vols.), and a new Curtius shelf (Brende 1553, Digby 1714).
- Refused: Duff's Silius Italicus (vol. 2 first printed 1934; the vol. 1 scan carries a 1933 preface). Skipped: Chaucer's Boece (the Boethius shelf already excludes Middle English Boethius), the 1656 Artemidorus (OCR unusable), the 1699 Tablet of Cebes (OCR 0.68, translator unknown).
- Review-fix pass (coordinator's relay; the reviewer's lane B messages never reached this session, so the fixes follow lane A's and the reviewer's lane A/C findings): `_surname` on all 97 shelves; `_translators` for 741 items (each surname found as a word in its text); 67 items in `_translator_unchecked` with the reason. `fetch_shelf.py --verify --record`: `_checks` for 565 items, 0 mismatched, 0 open rights flags. `fetch_perseus.py` took the same fixes and recorded `_perseus_checks` for 243 items, 0 failed. Correction: commit 2795e4b's message says 742 and 66; the counts are 741 and 67.
- fetch_shelf.py fix (backward compatible): multi-translator Gutenberg headers are read whole.
- Hourly retry at 20:45: nothing recovered (Greek Tragic Theatre vol. 2 still 503; no new Frazer, Hawkins or Phillimore scans).

## 2026-10-02 21:17 CDT — review round 3 and 4 fixes
- Added Good's Lucretius (1805, 2 vols, IA raw; title page read). Removed the stale "Creech pending" exclusion.
- Translator claims rewritten to full names on 614 items; 10 moved to `_translator_unchecked` with reasons; Curtius Brende and Digby vol. 2 claims added under `_identity_checked`.
- fetch_perseus.py: a sourceDesc with no year is refused unless `_rights_checked`; three Harmon vol. 1 (1913) rows dated that way. `--record` no longer writes an empty `_perseus_checks` into shelves without Perseus rows.
- fetch_shelf.py: PG `Translators?:` header, whole-word translator match.
- Stale rows fixed: Nixon vol. 2 exclusion, Sophocles Plumptre exclusion, Nixon vol. 3 date (1924 is right; the scan is a reprint with a 1979 note, flagged), Perseus counts in DIGEST-B.
- All 97 lane B shelves re-recorded: `fetch_shelf.py --verify --record` 0 mismatched; `fetch_perseus.py --verify --record` 0 failed.

## 2026-10-02 21:25 CDT — later-matter sweep
- Swept every lane B text's front matter for post-1930 revisions or addenda. Six held back on rights (`_held`, not fetched, local copies removed): suetonius-rolfe-v1 (revised 1951), cicero-williams-friends-v3 (revised 1954), plautus-nixon-v3 (1979 note), quintilian-butler-v1 (1980 addendum), ovid-miller-metamorphoses-v1 (1960s-70s bibliography), julian-wright-v1 (PG transcription includes the 1980 addendum). Other later dates found were reprint lines or library stamps.

## 2026-10-02 21:54 CDT — acquisitions since 21:25, and review rounds 5-6
- Perseus TEI (clean, not on PR #7): Xenophon, Marchant and Todd, 11 works (1923-25); Plato, Fowler, Lamb and Bury, 35 texts (1914-29); Brookes More's complete Metamorphoses (Cornhill, 1922); Ovid's Art of Love volume (1855) and Epistles (1813), translators unnamed; Jones's Epidemics I and III (1923). Shorey's Republic excluded (file dated 1935-37).
- New shelves (raw IA unless noted): jordanes (Mierow, 1908 PG and 1915), sidonius (Dalton, 1915, 2 vols), isaeus (Sir William Jones, 1779), herodas (Sharpley, 1906), rutilius (Savage-Armstrong's verse, ed. Keene, 1907), solinus (Golding, 1587), periploi (Schoff's Periplus, 1912; Falconer's Hanno, 1797).
- Added to shelves: frontinus (Herschel, 1899), late-greek-poets (Royston's Lycophron, 1806), greek-romances (Chariton 1764, 2 vols; Xenophon of Ephesus 1727), roman-epitomators (Codrington's Justin, 1688).
- Refused on OCR quality: Longus 1733 (0.69), Mawer's Oppian 1736 (0.76), Aelian 1665 (0.57), Francis's Horace 1743/1746 (0.61-0.64), Roberts's Demetrius 1902 (Greek facing, 0.59-0.72).
- fetch_perseus.py: record() labels each failure by cause and records only this run's rows; 1930 now needs a stated reason (52 Vince/Lamb rows given one); "</sourceDesc" across a line break is read.
- fetch_shelf.py (lane A's 815a082 pulled): new optional `_surname_by_slug`, so each book on a multi-author shelf is checked for its own author (13 shelves). Curtius Brende and Digby vol. 2 moved to `_translator_unchecked` (no override covers a translator now). Aristotle Oxford vols. I, IV-XI dated from their title pages in `_rights_checked` (vol. IX is a 1931 impression of 1925).
- Hourly retry at 21:31: nothing recovered.

## 2026-10-02 22:05 CDT — Victorian scholars' versions
- Added (raw IA, title pages read, OCR 0.86-0.94): Davidson's prose Virgil revised by Buckley (Harper, 1874); Lonsdale and Lee's Globe Virgil (1871) and Horace (1874); Slater's Silvae (1908); Cranstoun's Catullus (1867) and Propertius (1875); Jebb's prose Sophocles (1904); Way's Sophocles Part I (1909) and Aeschylus Parts I-III (1906-08).
- Way's Aeschylus I and III failed the surname test because the OCR reads the ligature as "JESCHYLUS"; title pages checked and recorded in `_identity_checked`. Way's Sophocles Part II (1914) not found on IA: wishlist.
- Francis's Horace (1743/1746, OCR 0.61-0.64) recorded in the Horace shelf's `_excluded`.
- `fetch_shelf.py --verify --record` on all seven shelves: 0 mismatched, 0 rights flags.

## 2026-10-02 22:08 CDT — Homer's Victorian translators
- Added (raw IA, title pages read, OCR 0.88-0.93): Morris's verse Odyssey (1887); Palmer's prose Odyssey (preface 1891); Worsley's Spenserian Odyssey (1861-62, 2 vols); Way's Odyssey (3rd ed., 1904); Newman's Iliad (1856); the Worsley-Conington Spenserian Iliad (1865, 1868); Way's Iliad (1886, 1888).
- Way's Iliad vol. I is in `_translator_unchecked`: the title-page OCR garbles his name.
- `fetch_shelf.py --verify --record` on homer: 25 items, 0 mismatched, 0 rights flags.

## 2026-10-02 22:13 CDT — Juvenal, Aristophanes, Hesiod, Theocritus, Pythagoreans
- Added (raw IA, title pages read, OCR 0.85-0.93): Mair's prose Hesiod (1908); Hickie's Bohn Aristophanes vol. I (1887 printing); Mitchell's Aristophanes vol. II (Clouds, Wasps; 1822); Madan's literal Juvenal and Persius (1814); Badham's verse Juvenal (1814); Hodgson's Juvenal (1807); Hallard's Theocritus (1901, revised from 1894); Taylor's Political Fragments of the Pythagoreans (1822).
- Refused on OCR: Aristaenetus (Halhed and Sheridan, 1771; 0.54), Madan's 1789 ECCO edition (0.63; held from 1814). Wanted: Hickie vol. II (IA has no text file), Mitchell vol. I.
- `fetch_shelf.py --verify --record` on the five shelves: 0 mismatched, 0 rights flags.

## 2026-10-03 00:41 CDT — Horace, Catullus, Claudian
- Added (raw IA, title pages read, OCR 0.84-0.89): Theodore Martin's Odes (Boston, 1866); Edward Bulwer-Lytton's Odes and Epodes (1869, Latin facing); Gladstone's Odes (preface 1894); George Lamb's Catullus vol. I (1821); Strutt's Claudian (1814); Howard's Translations from Claudian (1823).
- Not taken: Dart's Tibullus (1720; OCR 0.69), Pott and Wright's Martial (no printed date in the scan), Wickham's prose Horace (title page missing from the OCR).
- `fetch_shelf.py --verify --record` on the five shelves: 0 mismatched, 0 rights flags.
