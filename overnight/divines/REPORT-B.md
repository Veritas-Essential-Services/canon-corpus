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
