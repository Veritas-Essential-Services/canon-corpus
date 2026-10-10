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

## 2026-10-03 00:45 CDT — Hourly retry: two wishlist volumes found
- Bennett's Loeb Odes and Epodes (DLI scan, OCR 0.86): a later impression of the 1914 text (later series editors on the half-title, no revision notice, bibliography ends 1912); taken with the reason in `_rights_checked`. Translator claim unchecked: the OCR reads 'C. E, BENNETT'.
- Firth's Pliny, Second Series, Books VI-X (DLI scan, OCR 0.93): Walter Scott imprint, no printed date; companion of the First Series Gutenberg clears (PG 3234). Taken with the reason in `_rights_checked`; a printed date is still wanted.
- Still missing: Greek Tragic Theatre vol. II, Frazer's Pausanias vol. I, Hawkins's Claudian vol. 2, Phillimore vol. 2.
- The session stalled from about 22:25 to 00:40 CDT (tool calls refused while the safety check was rate-limited); nothing was lost.

## 2026-10-03 00:49 CDT — Review round 7, and Rouse's Lucretius
- Rouse's Loeb Lucretius from a 1924 first printing (IA, OCR 0.93; MCMXXIV title page, no reprint line, nothing later than 1921 in the front matter). Latin facing.
- Reviewer notes: aristotle-ross-v09, Bennett's Horace and Firth's Pliny listed in DIGEST-B as decisions for Adam; rows for Way's Aeschylus II-III and Martin's Horace say their year is the title page's (IA records 1906 and 1864); rows for Way's and Worsley's Iliad vol. I and Martin's Horace say how identity was confirmed.
- fetch_shelf.py: `--help`/`-h` print the usage; a missing shelf name gets a plain error. 35 fetch_shelf tests pass.
- Not done, and why: merging main into claude/armarium-divines is a no-op (main's head 97b7b5e is already an ancestor); `tests/structure_test.py` reports 64 passed on this branch, and main's copy of the file is identical.
- Checked and not taken: Foster's Livy vol. 2 and King's Tusculans on new uploads, both later revised printings (1939, 1945).

## 2026-10-03 00:53 CDT — Loeb uploads: Tacitus and Cicero
- Moore's Loeb Histories vol. I (Tacitus; MCMXXV first printing, OCR 0.94).
- Cicero's speeches in three Loebs: Watts (Pro Archia and five others; 1923), Grose Hodge (Pro Lege Manilia and three others; 1927), Freese (Pro Quinctio, Pro Roscio x2, De Lege Agraria; 1930). The scans are 1960s printings marked 'Reprinted', not revised, with no addenda; reasons in `_rights_checked`, and listed in DIGEST-B as decisions for Adam. OCR 0.92.
- Found through an uploader's 'X in N volumes [Loeb NNN]' series on IA, whose text files carry non-standard names (recorded as each row's third element).

## 2026-10-03 00:56 CDT — New shelves: Historia Augusta, Fronto
- historia-augusta (new shelf): Magie's Loeb Scriptores Historiae Augustae vols. I (MCMXXI) and II (MCMXXIV), first printings, OCR 0.89-0.90; author check per the biographers' names (Spartianus, Capitolinus, Lampridius, Vopiscus). Vol. III (1932) is past the line.
- fronto (new shelf): Haines's Loeb Correspondence of Fronto vols. I (MCMXIX) and II (MCMXX), first printings, OCR 0.82-0.83.
- Seen and not taken: IA's 1991/1993 reprints of the Magie volumes and a 1988 reprint of Fronto vol. II (which follows Haines's 1929 revision); first printings preferred.

## 2026-10-03 00:58 CDT — Held volumes: one replaced
- quintilian-butler-v1-1921: Butler's Quintilian vol. 1 from a DLI scan (OCR 0.91) whose imprint reads only 'First printed 1921', with no addendum and no year after 1930. It replaces the held quintilian-butler-v1, which carried the 1980 Bibliographical Addendum. Listed in DIGEST-B as a decision (later impression).
- Re-searched the other held volumes for clean printings: Rolfe's Suetonius vol. 1 (only the 1951 revision, in a 1970 printing), Miller's Metamorphoses vol. 1 (1971 printing), Williams's Letters to Friends vol. 3 (a 1972 printing with a 1971 note), Wright's Julian (Greek facing). None taken.

## 2026-10-03 01:00 CDT — Ovid and Velleius Loebs
- Mozley's Loeb Art of Love and Other Poems (Ars Amatoria, Remedia, Medicamina, Nux, Ibis, Halieuticon, Consolatio ad Liviam): MCMXXIX first printing, OCR 0.87.
- Shipley's Loeb Velleius Paterculus and Res Gestae Divi Augusti (1924): a 1961 plain reprint ('Reprinted 1955, 1961'), no later matter; on roman-epitomators with its own author check. Listed in DIGEST-B as a decision.

## 2026-10-03 01:03 CDT — Demosthenes and Marcus Aurelius
- Leland's Orations of Demosthenes, new edition (1806, 2 vols; OCR 0.91-0.92).
- Marcus Aurelius: Casaubon's Meditations (Everyman 1906, from the 1948 reprint, reason in `_rights_checked`; OCR 0.95), Rendall's To Himself (2nd ed., 1898; 0.89), Collier's Conversation with Himself (1701; 0.82; translator unchecked, OCR reads 'Cortrier'), Collier revised by Zimmern (Camelot, 1887; 0.93). The shelf's old 'Rendall and Collier pending' note is closed.
- Refused on OCR: Gillies's Lysias and Isocrates (1778; 0.71).

## 2026-10-03 01:08 CDT — Aristotle: the older translators
- Raw IA, title pages read, OCR 0.84-0.93: Taylor's Metaphysics (1801); Browne's Bohn Ethics (1850); Owen's Bohn Organon (1853, 2 vols); the Bohn literal Rhetoric with Buckley's Poetic (1857); Peters's Ethics (1881); Welldon's Rhetoric (1886), Ethics (1892) and Politics (1901 printing of 1883).
- Gutenberg: Ellis's Politics (PG 6762); the Everyman Ethics (PG 8438), which names no translator, so none is claimed (usually given as D. P. Chase, not verified).
- Translator claims unchecked because the OCR garbles the name: Browne ('E. W. BROWNE'), Peters ('PETEES'), Welldon's Politics ('J. EK. C.').
- Skipped: Jowett's 1885 Politics (the same translation is in Oxford vol. X); Edghill's Categories on Gutenberg (the same translation is in Oxford vol. I).

## 2026-10-03 01:12 CDT — Plato and Lucian
- Plato: Whewell's Platonic Dialogues for English Readers (vol. I, 2nd ed. 1860, DLI scan; vols. II 1860 and III 1861), noted as abridged in parts, as his preface says; Davies and Vaughan's Republic (Golden Treasury, 1892 printing of 1852); Spens's Republic (1763 translation, Everyman 1906 edition in its 1919 reprint). OCR 0.91-0.98.
- Lucian: Tooke's Lucian of Samosata (1820, 2 vols; OCR 0.94).
- Not found: Church's Trial and Death of Socrates (the 1880 scan has no text file).

## 2026-10-03 01:13 CDT — Xenophon, Minor Works (1813)
- The Minor Works of Xenophon 'by several hands' (1813; OCR 0.92): Welwood's Banquet and Bradley's Economics are named on their section titles; the Memoirs of Socrates and Hiero carry no name (the Memoirs is usually given to Sarah Fielding; not verified, not claimed).

## 2026-10-03 01:15 CDT — Greek tragedy: more translators
- Sophocles: Whitelaw's verse (1883; OCR 0.90); Dale's verse (1824, 2 vols; 0.89).
- Aeschylus: Campbell's prose Oresteia (1893; 0.92); Walter and C. E. S. Headlam's prose Plays (Bell, 1909; 0.82); Warr's Oresteia (George Allen, 1900; 0.88).
- Not taken: Cookson's Everyman Aeschylus (the scan's introduction cites a 1936 book).
- Correction: the Palmer Odyssey row named a Boston publisher not read from the file; it now gives only the preface date the title page shows.

## 2026-10-03 01:16 CDT — Pindar and the Bohn Hesiod
- Paley's prose Odes of Pindar (1868; OCR 0.88; translator unchecked, OCR reads 'PA LET').
- Banks's Bohn Works of Hesiod, Callimachus and Theognis (1856; OCR 0.84), with the verse of Elton (Hesiod), Tytler (Callimachus) and Frere (Theognis) appended, which answers the Tytler wishlist line.
- Refused on OCR: Tytler's 1793 Callimachus (0.767, just under the bar), Polwhele's Theocritus (0.68).

## 2026-10-03 01:21 CDT — Seneca (Morell 1786), Apuleius (Taylor 1822), review round 8
- Seneca: Thomas Morell's Epistles to Lucilius, 1786, both volumes (Woodfall for Robinson); the translator's name OCRs garbled on each title page, so the claim is recorded as unchecked with the OCR spelling
- Apuleius: Thomas Taylor's 1822 Metamorphosis; a second scan of the same edition excluded
- Review round 8: the Everyman Ethics (PG 8438) moved to _held as a duplicate of the Adler shelf's aristotle-ethics; the duplicate Rendall 1898 row dropped (same IA item as marcus-aurelius-rendall); Bennett now carries a translator check (surname, since the title page OCRs 'C. E, BENNETT'); Firth vol. 2's date marked inferred; the digest's Adam decisions narrowed to Ross v09, and the stale 'Bennett not found' line removed

## 2026-10-03 01:30 CDT — Aeschines (new), Livy XXI-XXV, Quintilian (Watson), stale notes
- Aeschines: new shelf with Charles Darwin Adams's three speeches (Loeb 1919) from Perseus TEI; the record also gives 1958, the printing Perseus keyed from, so each row carries a _rights_checked reason
- Livy: Church and Brodribb's Books XXI-XXV, The Second Punic War (Macmillan, 1883)
- Quintilian: Watson's Bohn Institutes, vol. I from Bell's 1903 reprint from the 1856 stereotype plates and vol. II from 1856; this fills the 'Watson, no scan located' gap
- Eighteen 'pending' notes refreshed where the work was already held (Carter's Epictetus, Cary's Herodotus, Buckley's Euripides vol. II, Golding's Caesar, Holland's Livy, Murray's Homer, C. F. Smith's Thucydides, the Bohn Plato, Bysshe, Elton's Hesiod and others); the Brookes More note now agrees with the Perseus source record (Cornhill, 1922)

## 2026-10-03 01:35 CDT — Perseus census fill: Smyth, Norlin, Perrin, Godley, Hicks, Rackham
- Aeschylus: Smyth's Loeb (1922-26), seven plays; Perseus marks these files modernized
- Isocrates: Norlin's Loeb vols. 1-2 (1928-29), eleven speeches; Van Hook's vol. 3 (1945) not taken
- Plutarch: Perrin's Lives (Loeb 1914-26), 66 texts
- Herodotus: Godley's Loeb (1920-25), whole Histories, in Perseus's modernized text (its header says archaisms were removed and the text revised)
- Diogenes Laertius: Hicks's Loeb (1925), whole Lives
- Aristotle: Rackham's Nicomachean Ethics (Loeb 1926) as a second Ethics witness; Freese's Rhetoric refused (1947 printing in its record, no reason stated)
- Apollodorus: Frazer's Epitome joins his Library

## 2026-10-03 01:38 CDT — Perseus 'check' rows: Isaeus (Forster), Xenophon (Miller)
- Isaeus: Forster's Loeb (1927), twelve speeches; Perseus keyed the 1962 printing, reason in _rights_checked
- Xenophon: Miller's Cyropaedia (Loeb 1914); the census's '1949' is Miller's death year
- The census is now exhausted for lane B: what remains is post-1930 Loebs (Murray's and Vince's later Demosthenes, Harmon's and Babbitt's later volumes), modern translations (Svarlien's Pindar and Bacchylides), or other lanes' authors

## 2026-10-03 01:45 CDT — Lucan (Ridley), Statius (Lewis), Aristophanes (Wheelwright), Pindar (Cary, Wheelwright), Herodotus (Littlebury)
- Lucan: Ridley's blank-verse Pharsalia, first edition (Longmans, 1896) and his revised second edition (1905)
- Statius: William Lillington Lewis's verse Thebaid, both volumes of the Becket second edition (IA dates them 1767 and 1773; the vol. I imprint year OCRs garbled)
- Aristophanes: C. A. Wheelwright's complete Comedies in blank verse, 2 vols (Oxford, Talboys; IA 1837)
- Pindar: Henry Francis Cary's Pindar in English Verse (Moxon; IA 1833) and Wheelwright's Pindar (Valpy, 1830)
- Herodotus: Isaac Littlebury's translation, third edition, 2 vols (1737)

## 2026-10-03 01:52 CDT — Horace (Martin), Virgil (Kennedy; Pitt and Warton), Greek Anthology (Burges), Martial (Bohn), Catullus/Tibullus (Kelly)
- Horace: Theodore Martin's complete Works in verse, 2 vols (Blackwood, 1881)
- Virgil: the Works in verse by Rann Kennedy and Charles Rann Kennedy, 2 vols (1849); Pitt and Warton's Works of Virgil in English Verse (Dodsley, 1763), vols. I and III of four (vols. II and IV not found); Pitt's 1740 Aeneid refused for OCR
- Greek Anthology: Burges's Bohn prose with metrical versions (1854), on the greek-lyric shelf
- Martial: the Bohn Epigrams (Bell, 1877), prose with verse versions; no translator named, none claimed
- Catullus and Tibullus: Kelly's Bohn Erotica (1854), which also prints Lamb's metrical Catullus whole (the missing Lamb vol. II's poems) and Grainger's Tibullus
- Sophocles: Potter's 1820 translation refused for OCR (0.758)

## 2026-10-03 01:57 CDT — Review round 9
- Later printings: Ross v09 and v02, Bennett, three Cicero Loebs, Quintilian Butler v1, Velleius, Casaubon Everyman, Adams's Aeschines (1958), Forster's Isaeus (1962) and the refused Freese Rhetoric (1947) are one decision for Adam in DIGEST-B; nothing in the class is decided in-lane
- Godley's Herodotus and seven Smyth Aeschylus plays are Perseus-modernized texts: each has a _rights_checked reason naming the modernizer its header gives, a DIGEST-B decision, and fetch_perseus.py now refuses any modernized file without a reason
- Every kept Perseus finding (lane B, 290 texts) now carries a rights block with redistribute_whole false; markup_licence_in_file is recorded only where the file itself states a licence (Godley's and Smyth's files do not, so their block cites the repository README)
- pindar-cary-1833 withdrawn: the same IA scan as lane C's cary-pindar, already cross-referenced
- Unchecked translators: Lewis vol. I now matches ('Lillington Lewis' in the dedication); Ridley 1896, Paley, Watson vol. II, Morell (2), Lewis vol. II and Littlebury (2) print the name nowhere the OCR can read, so each stays under _translator_unchecked with the title page's OCR spelling

## 2026-10-03 02:04 CDT — Nicomachus (D'Ooge), Hermetica (new)
- Nicomachus: D'Ooge's Introduction to Arithmetic with Robbins and Karpinski's studies (University of Michigan Studies; Macmillan, 1926), on the greek-mechanics-astronomy shelf; date from the title page, IA records none
- Hermetica: new shelf. John David Chambers's translation from the Greek (T. & T. Clark, 1882); Everard's Divine Pymander (1650) in Redway's 1884 reprint with Hargrave Jennings's introduction; G. R. S. Mead's Thrice-Greatest Hermes, all three volumes (1906)
- Gellius: a stale 'Beloe vol. 2 pending' note closed; vol. 2 was already held

## 2026-10-03 02:10 CDT — Epictetus (Stanhope), Sallustius (Taylor), Orphic Hymns (Taylor)
- Epictetus: Stanhope's Epictetus his Morals with Simplicius his Comment, fifth edition (1741)
- Pythagoreans: Taylor's Sallust on the Gods and the World with Demophilus's Pythagoric Sentences (Jeffery; IA 1793); the book names no translator, so none is claimed
- Orphica: new shelf, Taylor's Mystical Initiations; or, Hymns of Orpheus (1787, first edition); IA's mysticalhymnsor00taylgoog, catalogued 1824, is Dobell's 1896 reprint
- Refused for OCR: Taylor's Two Orations of Julian (1793), the 1896 Alciphron, Scott's Hermetica vol. I

## 2026-10-03 02:13 CDT — Proclus on the Timaeus (Taylor), Boethius (Ridpath, Colville)
- Proclus: Taylor's Commentaries of Proclus on the Timaeus of Plato, 2 vols (printed for the author; IA 1820)
- Boethius: Philip Ridpath's Consolation (Dilly, 1785); George Colville's 1556 translation in Ernest Belfort Bax's edition (Nutt, 1897; Tudor English, unlike Chaucer's Middle English Boece, which the shelf leaves out)
- Retry list: Queen Elizabeth's Englishings of Boethius (EETS, 1899), archive.org 500

## 2026-10-03 02:15 CDT — Seneca tragedies (Bradshaw)
- Seneca: Watson Bradshaw's prose Ten Tragedies (Swan Sonnenschein, 1902)
- Tenne Tragedies (Tudor Translations, 1927) still held for Adam (Eliot introduction)

## 2026-10-03 02:17 CDT — Arrian and others (McCrindle)
- Arrian shelf: McCrindle's Invasion of India by Alexander the Great (Constable, 1893), Arrian, Curtius, Diodoros, Plutarch, Justin

## 2026-10-03 02:18 CDT — Silius Italicus (Tytler)
- New shelf silius: Tytler's verse Punics vol. I (Calcutta, 1828)
- Duff's Loeb vol. I (1961 reprint) held for Adam; added to the later-printings decision
- Duff vol. II (first printed 1934) not taken

## 2026-10-03 02:20 CDT — Cebes (Guthrie)
- New shelf cebes: Guthrie's Greek Pilgrim's Progress (1910)
- Healey 1610 and two 18th-century versions refused on OCR

## 2026-10-03 02:23 CDT — Bohn gaps (Lucan, Aristotle)
- Lucan: Riley's literal prose Pharsalia (Bohn, 1853)
- Aristotle: M'Mahon's literal Metaphysics (Bohn, 1857)
- Refused on OCR (EEBO, 0.57-0.74): Stanley's Aelian 1665/1666, Fleming's Aelian 1576, Bingham's Tactiks of Aelian 1616, Golding's Mela 1585; the 1670 Aelian answers 500 (added to the retry)

## 2026-10-03 02:27 CDT — Bohn and single plays
- Aristotle: Walford's Politics and Economics (Bohn, 1853)
- Euripides: Augusta Webster's verse Medea (1868)
- Julian: C. W. King's Julian the Emperor (Bohn, 1888), with Gregory Nazianzen's Invectives and Libanius' Monody
- Aeschylus: Prometheus Bound by Augusta Webster (1866), C. B. Cayley (1867), Paul Elmer More (1899), Edwyn Bevan (1902)

## 2026-10-03 02:30 CDT — Aeschylus: Agamemnons
- Aeschylus: Agamemnon by J. S. Harford (1831, translator unchecked), H. H. Milman (1865, with the Bacchae), W. R. Paton (1907), Locke Ellis (1920)
- Not taken: Trevelyan's Oresteia (Greek facing, OCR 0.51) and Greek-facing school editions

## 2026-10-03 02:35 CDT — Reviewer cycle 9
- Distinguishing name forms on seven shelves (Maximus, Xenophon, Apollonius, Sallust, Hermes); all items re-pass
- McCrindle label kept at 1893 on the title page's evidence; IA's 1896 noted
- Virgil Pitt vol. III: title_weak explained (Æneid ligature), title page recorded
- Plutarch: stale Holland exclusion removed

## 2026-10-03 02:38 CDT — Euripides and Aristophanes
- Euripides: Oxford literal prose Hecuba, Orestes, Phoenissae, Medea (1820s; translator unnamed)
- Aristophanes: Walsh's Acharnians, Knights, Clouds (Bohn, 1848)
- Aristophanes: Comedies (Clouds, Plutus, Frogs, Birds; Valpy, 1812)
- Aristophanes: Oxford literal Plutus and Frogs (Talboys, 1822; unnamed)
- Aristophanes: Acharnians in verse by Billson (1882) and Tyrrell (1883)

## 2026-10-03 02:43 CDT — Horace; retry
- Horace: verse Odes by C. S. Mathews (1867), H. H. Pierce (1884), W. H. Cudworth (1917)
- Retry: three items now show metadata but their text still answers 500 (Queen Elizabeth's Boethius, the 1670 Aelian, Sheppard's Oedipus); the rest unchanged

## 2026-10-03 02:45 CDT — Virgil: Aeneids
- Virgil: Aeneid by G. K. Rickards (I-VI, 1871), John D. Long (1879), Oliver Crane (1888), Sir Charles Bowen (Eclogues and I-VI, 1889)
- IA aeneidvirgil00rickgoog mislabelled (Rickards, not Ravensworth); Ravensworth's VII-XII still wanted

## 2026-10-03 02:47 CDT — Virgil: Georgics and Eclogues
- Virgil: Georgics by William Sotheby (1808), R. D. Blackmore (1871), Harriet Waters Preston (1881), Lord Burghclere (I-II, 1900)
- Virgil: Bucolics by T. W. C. Edwards (1825); Eclogues by T. F. Royds (1922)
- Retry list: I. P. Smith's Eclogues (1909), 500

## 2026-10-03 02:50 CDT — Minor Latin poets
- New shelf latin-minor-poets: Calpurnius (Scott, 1890), Publilius Syrus (Lyman, 1856), Distichs of Cato (Chase, 1922), Grattius (Wase, 1654)
- Wase's date: IA gives 1654; the title page OCR reads 1664; label states both

## 2026-10-03 02:52 CDT — Presocratics
- New shelf presocratics: Heraclitus (G. T. W. Patrick, 1889), Empedocles in verse (W. E. Leonard, 1908)
- Fairbanks's First Philosophers of Greece refused on OCR; Burnet not taken (a study)

## 2026-10-03 02:53 CDT — Plato
- Plato: F. J. Church, Trial and Death of Socrates (Euthyphro, Apology, Crito, Phaedo)
- Plato: A. D. Lindsay's Republic (Everyman, 3rd ed. 1923)
- Plato: E. M. Cope's literal Gorgias (1864) and Phaedo (1875)
- Wright's Phaedrus, Lysis and Protagoras: the only scan found answers 404

## 2026-10-03 02:55 CDT — Plato (2)
- Plato: J. Wright's Phaedrus, Lysis, Protagoras (1888); S. W. Dyde's Theaetetus (1899); Talks with Athenian Youths (1891, translator unnamed in the volume); F. A. Paley's Philebus (1879)
- No text layer on IA: a Theaetetus (1875), two Menos (1869, 1880), Socrates (1879), The Judgment of Socrates (1898)

## 2026-10-03 03:00 CDT — Cicero (older translations)
- Cicero: Guthrie's Epistles to Atticus (1752 vol. I; 1806 vols. II-III)
- Cicero: Guthrie's Offices, Cato, Laelius, Paradoxes, Scipio's Dream (1755); his On Oratory and Orators (1808, 2 vols.)
- Cicero: Heberden's Letters to Atticus (1825, 2 vols.); Francklin's Nature of the Gods (1829); Jeans's Life and Letters (1887)
- Three translator claims unchecked with reasons (OCR'd name, lost title page, name only in advertisements)

## 2026-10-03 05:44 CDT — Thucydides, Pliny; cycle 10
- Thucydides: S. T. Bloomfield's annotated translation (1829, 3 vols.)
- Pliny: Orrery's Letters of Pliny the Younger (vol. I 1751, vol. II 1752)
- Cycle 10: Paley 1879 confirmed; Perseus licence stated in _about on seven shelves (not in _rights_checked, which is the gate's override)
- Gap 03:02-05:40: tool rate limit

## 2026-10-03 05:57 CDT — Cycle 11, recoveries, Persius and Juvenal
- Horace name forms changed so they no longer match Horace Bushnell (reviewer)
- _perseus_licence statement on the 21 Perseus shelves; fetch_perseus.py documents it; 4 new tests
- Storage-node workaround for archive.org/download 500s: Melmoth vol. I, Queen Elizabeth's Englishings (EETS 1899), Sheppard's Oedipus (1922), Perley Smith's Eclogues (1909)
- Aelian 1670 refused (OCR 0.66)
- juvenal: Wollaston's Persius (1841) and Leeper's Juvenal (1902)

## 2026-10-03 06:05 CDT — Homer verse translations
- homer: 15 translators, 22 volumes (Mackail, Cotterill, Carnarvon, Munford, I. C. Wright, Blackie, Cayley, Merivale, Morrice, Musgrave, Barnard, Schomberg, H. S. Wright, Cordery, Sotheby)
- Missing companion volumes: Munford I, Wright II, Musgrave I, Sotheby III (503)
- Refused: Green 1884 (OCR 0.53); Herschel 1866 404
- verify: 47 items, 0 mismatched

## 2026-10-03 06:10 CDT — Sophocles, Catullus, Propertius, Tacitus, Sallust, Martial
- sophocles: Trevelyan 1919, Plaistowe (c. 1892), Oxford prose 1886, Morshead 1895, E. P. Coleridge 1905
- catullus: Nott vol. I 1795 (catalogue attribution), Hart-Davies 1879, Stuttaford 1912
- propertius: Phillimore 1906; tacitus: Ramsay's Annals (2 vols.); sallust: Pollard 1882; martial: Nixon 1911
- Refused on OCR: Cholmeley's Theocritus, the 1720 Tibullus, Nott vol. II
- Held: Pott and Wright's Martial (printing date not on the title page)

## 2026-10-03 06:14 CDT — Ovid and Euripides
- ovid: Henry King 1871 (translator unchecked: OCR 'ICING')
- ovid: Garth 1826 and More's Book I not kept (Dryden shelf, lane C; Perseus)
- euripides: Fitz-Gerald 1867, Lawton 1889, Beloit Class of 1900 (1898), Kynaston 1906
- Excerpts skipped: Goldwin Smith, McBride

## 2026-10-03 06:21 CDT — Demosthenes, Conington, retries
- demosthenes: Brougham 1840 and Collier 1876 (translators unchecked: OCR)
- virgil: Conington's verse Aeneid (1867 American edition)
- Refused: Laurent's Herodotus I, Simpson's Crown, Murphy's Lucian (all copies)
- Storage-node retry: four dark items still dark

## 2026-10-03 06:26 CDT — Horace and Virgil
- horace: 11 translators (Francis, Deazeley, Hughes, Forsyth, Hague, Marris, Whyte Melville, Ravensworth, O'Brien, Phelps, Green)
- virgil: Thornhill's Aeneid, King and Rose Eclogues and Georgics
- Whyte Melville: identity quoted from the title page (author printed only as 'Horace')

## 2026-10-03 06:30 CDT — Lucretius, Terence, Plautus
- lucretius: 1743 anon. prose (vol. I), Watson and Good 1851, Johnson 1872, 1879 private, Baring 1884
- roman-comedy: Echard's Terence 1733, Evans's Trinummus 1883
- Refused: 1743 vol. II (0.7798), Thornton's Plautus (0.70)

## 2026-10-03 06:33 CDT — Anacreon
- greek-lyric: Fawkes (IA 1760), Girdlestone 1804, T. J. Arnold (IA 1869)
- Refused on OCR: Anacreon 1735, Bullen's Stanley 1893
- Greek-facing Loebs measured 0.53-0.74 on the whole-text bar; left pending

## 2026-10-03 06:39 CDT — Juvenal, Celsus, Longinus, name checks
- juvenal: Owen 1786, William Smart 1829, Wallace 1848
- celsus: Collier 1831, Lee vol. I 1831
- longinus: Dublin graduate 1821, Spurdens 1836, Oxford M.A. 1841, Stebbing 1867
- Name checks: common-word surnames (king, smart, green) now checked as the printed full name or marked unchecked

## 2026-10-03 06:43 CDT — Aristotle gap-fill (2)
- Robert Williams, Nicomachean Ethics (1869), 0.94
- Thomas Taylor, Rhetoric, Poetic and Nicomachean Ethics vol. II (1818), 0.91
- Refused: Taylor's Treatises on the Soul (1808), OCR truncated
- Not refetched: Chase 1847 Ethics, Jowett 1885 Politics (texts already held)

## 2026-10-03 06:45 CDT — Aristophanes gap-fill (2)
- Thomas Mitchell, Comedies vol. I (1820), 0.90; completes his set
- W. J. Hickie, Bohn vol. II (1853), 0.83; completes his set (IA misdates it 1822)

## 2026-10-03 06:56 CDT — Gap-fill (7) and review fixes
- C. R. Moore, Elegies of Propertius (1870), 0.86
- J. Hart, Herodian's History (1749, catalogue date), 0.87; translator unchecked
- Valerius Flaccus Book I: anonymous verse (catalogue [1808], attributed to T. Noble by the catalogue only), 0.87; H. G. Blomfield prose (1916), 0.88
- Refused: Sherburne's Sphere of Manilius (1675), OCR 0.69
- Review: Plaistowe, Rose, Arnold dated from bound-in lists and prefaces (1898, 1866, 1868)
- Review: 27 translator checks moved to full names; H. S. Wright and Moore unchecked

## 2026-10-03 06:59 CDT — Dark volumes found
- J. G. Frazer, Pausanias vol. I: Translation (1898), DLI scan, 0.92
- William Sotheby, Odyssey Books I-XII (vol. III, 1834), Google scan, 0.80; completes his four-volume set

## 2026-10-03 07:03 CDT — Homer gap-fill (3)
- T. S. Brandreth, Iliad vol. I (Pickering; catalogue 1846), 0.88
- Sir Charles Du Cane, Odyssey I-XII (1880), 0.88
- J. Henry Dart, Iliad in English hexameters (1865), 0.87
- John Purves, prose Iliad, ed. Abbott (1891), 0.93

## 2026-10-03 07:08 CDT — Virgil and Horace title sweeps
- E. M. Millington, Eclogues in rhythmic prose (1870), 0.88
- Robert Hoblyn, Georgics I in blank verse (1825), 0.84
- J. O. Sargent, Horatian Echoes (1893), 0.89
- F. Coutts and W. H. Pollock, Icarian Flights (1920), 0.89
- 'A Native of America', Lyric Works of Horace (Philadelphia 1786), 0.85; translator unchecked
- H. N. Jones, Odes I-II (1865), 0.89
- G. Fenwick, Odes II (1918), 0.90
- W. H. Mills, Nineteen Odes (1920), 0.92
- Refused under the OCR bar: ECCO Neville Georgics 1767, 1750 Georgics, 1794 Aeneid, 1787 Aeneid II, 1753 prose Horace

## 2026-10-03 07:11 CDT — Sophocles title sweep
- Sir George Young, Dramas in English verse (IA 1888), 0.91
- Sir F. H. Doyle, Oedipus King of Thebes (1849), 0.87
- Roscoe Mongan, literal Oedipus Tyrannus (1865), 0.89
- A. C. A. Hull, Oedipus at Colonus (1894), 0.88
- G. H. Palmer, Antigone (copyright 1899), 0.91

## 2026-10-03 07:13 CDT — Aeschylus, Euripides, Juvenal title sweeps
- Anonymous ('a Member of the University of Oxford'), Bacchae and Heraclidae literally translated (1846), 0.92
- Refused under the OCR bar: Conington's Agamemnon 1848 (0.74), a W. F. Alcestis 1870 (0.77), Hadley's Alcestis (0.68), an ECCO 1786 Hippolytus and Iphigenia (0.71)
- Skipped as already covered: Madan's Juvenal (Dublin 1822), Dryden's multi-hand Juvenal and Persius (1812; the Dryden shelf)

## 2026-10-03 07:17 CDT — Cicero title sweep
- James S. Reid, Academics (1880), 0.93; translator unchecked
- Benjamin E. Smith, De Amicitia (copyright 1897), 0.91
- Robert Black, Death No Bane, Tusculan I (1889), 0.87
- Catullus, Tibullus, Lucretius, Theocritus: nothing new

## 2026-10-03 07:19 CDT — Roman historians title sweep
- John Aikin, Germania and Agricola, 3rd ed. (Oxford; IA 1815), 0.86
- Refused under the OCR bar: Bladen's Caesar 1732 and 1737 (ECCO, 0.77, 0.76), Sallust 1709 (0.66), Suetonius 1726 (0.42)

## 2026-10-03 07:21 CDT — Greek prose title sweep
- R. W. Mackay, Sophistes (1868), 0.88
- Not taken: Kennedy's Theaetetus (Greek facing, 0.60); ECCO Xenophon copies already covered by the held multi-hand volume

## 2026-10-10 09:11 CDT — Round 2026-10-10a: title sweeps, plus Ransome
- Ransome shelf: book 1 held (US public domain since 2026-01-01); books 2-12 excluded with their US dates; none UK-free until 2038
- Added 9 volumes across Seneca, Pindar, Greek lyric, Marcus Aurelius, Lucian
- Held back for Adam: Index Expurgatorius of Martial (1868); Carr's Dialogues of Lucian (title-page rule)
- Excluded under the OCR bar: the 1773 Martial (0.43), the 1806 Anacreon (0.70), Murphy's Lucian (0.68)
