# Lane B digest — Classical (English translations)
<!-- refreshed 2026-10-02 17:31 CDT by the lane B worker -->

**Held:** 84 shelves, 691 files (249 clean Gutenberg texts, 199 raw Internet Archive OCR volumes, 243 Perseus TEI texts), 388 MB on the worker's disk. Corpus text is gitignored; the shelves (`pipeline/<author>_shelf.json`) are the record. Nothing converted into the build manifest and **nothing minted** (no uid minting during a burst). Every shelf lists its pending wishlist and its exclusions with reasons; the map section is `docs/divines-map/B-classical.md`.

| Author | Held (clean / raw) | Pending, short |
|---|---|---|
| Plato (Jowett; Bohn Cary-Davis-Burges; Taylor 1804) | 29 / 16 | Shelley |
| Aristotle (Oxford, Smith & Ross) | 0 / 11 | vol. III (US PD 2027-01-01), vol. XII (1952) |
| Hesiod (Evelyn-White) | 1 / 0 | Elton |
| Ovid (Riley; Golding, Howard) | 6 / 3 | Marlowe's Elegies, Brookes More |
| Virgil (Rhoades, Conington, + 4 Aeneids) | 7 / 3 | Williams's Eclogues/Georgics |
| Homer (Chapman, Pope, Cowper, Derby, Buckley, Butler, Bryant) | 9 / 4 + 2 Perseus (A. T. Murray's Loebs) | none known |
| Aeschylus, Euripides, Sophocles | 19 / 7 + 2 Perseus (Browning's Agamemnon, Murray's Rhesus) | Smyth is on PR #7 |
| Aristophanes | 5 / 0 | Rogers complete, Frere |
| Herodotus, Thucydides, Xenophon, Polybius, Arrian | 20 / 7 + 3 Perseus Thucydides (Hobbes, Dale, C. F. Smith) | the Greek-facing Loebs |
| Plutarch (North, Langhorne, Stewart-Long; Goodwin Moralia) | 13 / 12 + 91 Perseus Moralia (Goodwin 1874 ed.; Babbitt vols. 1-2) | Holland's Morals in a cleaner copy |
| Marcus Aurelius, Epictetus, Seneca | 13 / 5 | Gummere's Epistles (Latin facing) |
| Tacitus, Livy, Caesar, Suetonius, Sallust, Pliny | 20 / 2 | Holland's Livy/Suetonius/Pliny |
| Lucretius, Horace, Catullus, Tibullus, Juvenal, Plautus & Terence, Lucan, Apuleius, Petronius | 17 / 5 | Creech, Smart, Rowe |
| Lucian, Cicero | 16 / 6 + 52 Perseus Lucian (Harmon 1913-25, E. J. Smith, the Fowlers) | Francklin's complete Lucian |
| Greek orators (Demosthenes, Lysias, Isocrates) | 4 / 6 + 54 Perseus (Vince 1926 and 1930, Lamb 1930) | none known |
| Greek poets (Pindar, Theocritus, Apollonius, Quintus, lyric and Anthology) | 9 / 4 | Paton, Edmonds, Mair (Greek-facing Loebs); Musaeus |
| Late philosophy (Diogenes, Plotinus incl. MacKenna 1917-30 complete, Porphyry, Iamblichus, Proclus, Sextus, Julian, Boethius) | 21 / 8 | Wright's Julian vol. 3 (Greek facing) |
| Geographers and historians (Pausanias, Strabo, Appian, Diodorus, Dio, Athenaeus, Procopius, Greek romances) | 20 / 7 | Taylor's Pausanias vol. 3, Frazer |
| Science (Euclid, Archimedes, Apollonius of Perga, Hippocrates, Galen, Aretaeus, Theophrastus, Hero, Ptolemy) | 6 / 9 + 27 Perseus (Adams's Hippocrates and Aretaeus, Jones, Heath, Brock) | Heath 2nd ed. (1926) |
| Latin silver and late (Martial, Statius, Claudian, Quintilian, Vitruvius, Gellius, Ammianus, Ausonius, Frontinus, Celsus, Cato/Varro, Phaedrus, Watson's epitomators, Justinian) | 9 / 20 | Hawkins's Claudian vol. 2 |
| Dionysius of Halicarnassus, Augustus | 2 / 0 | |

## Added since the first digest (2026-10-02, 16:35-17:05 CDT)

- **61 Latin-facing Loeb volumes (1912-1930)** on 20 existing shelves, e.g. Gummere's Seneca Epistles, Fairclough's Virgil, Miller's Metamorphoses, Rolfe's Suetonius/Sallust/Gellius, Butler's Quintilian, Foster's Livy 1, 3-5, Williams's Cicero Letters to Friends. Winstedt's Letters to Atticus now from clean Gutenberg. Refused: Livy vol. 2 (scan is the 1939 revised printing), Plautus vols. 4-5 (1932, 1938), Basore vol. 3 (1935).
- **Older English translators from the map's wishlists:** Potter's Aeschylus and Wodhull's complete Euripides (Greek Tragic Theatre, 1809), Swanwick, Plumptre's Sophocles, Creech's Lucretius, Rowe's Lucan vol. 1, Carter's Epictetus, Cary's Herodotus, Holland's Pliny (1601) and Livy (1659 ed.), Gordon's Tacitus (5 vols.), Hampton's Polybius, Smith's Thucydides, Collier's and Rendall's Marcus, Norgate's Iliad, Hobbes's Homer, Cranch's Aeneid, T. C. Williams's Georgics, Elton's Hesiod, Bysshe's Memorabilia.
- **fetch_shelf.py** now reads Gutenberg files served only gzip-encoded (one-line retry on HTTP 406); Robinson's Archimedes fetched with it.
- **Grey area for you:** some kept Loeb scans are later reprints (e.g. 1931-1969) of pre-1931 editions with no revision notice; two carry pre-1930 revisions (Miller's Seneca vol. 2, Fairclough's Horace, both 1929). Their text is that of the pre-1931 edition.

## Added since the second digest (2026-10-02, 17:07-17:31 CDT)

- **243 Perseus TEI English texts** under a new `"perseus"` key in 19 shelves, fetched by a new, separate `pipeline/fetch_perseus.py` (fetch_shelf.py is unchanged for them). Deduped against the 309 Perseus ids on PR #7; Philo (PR #8) and the fathers, apocrypha and Bible rows left to their owners. Each file's own sourceDesc dates the translation (all 1930 or earlier, except one reprint noted under Defects); the markup licence travels in each `<shelf>_perseus_report.json`.
- **Five missing volumes found under other ids:** Nixon's Plautus vol. 2 (1917), Francklin's complete Sophocles (1759), Beloe's Gellius vol. 2 (1795), Kennedy's Demosthenes vol. 5 (1878) and Rowe's Lucan vol. 2 (1812). Title pages were read.
- **Refused or held:** King's Tusculans (only the 1945 revised printing has text), Wright's Julian vol. 3 (Greek facing). Still not found: Frazer's Pausanias vol. 1, Bennett's Loeb Horace, Hawkins's Claudian vol. 2, and vol. 2 of the 1809 Greek Tragic Theatre.

## Look at these first (Adam)

1. **The Adler shelf has six wrong labels**, all checked against the Gutenberg files: `thucydides-pelo` (PG 7142) is Crawley, not Jowett; `tacitus-annals` (PG 7959) is Gordon's Annals I-VI selection, not Church & Brodribb; `epictetus-discourses` (PG 45109) is Higginson's Enchiridion, not Matheson's Discourses; `lucretius-nature` (PG 785) is Leonard, not Munro; `herodotus-history` (PG 2707) is Macaulay vol. 1 only; `plato-dialogues` (PG 1656) is the Apology alone. One more is inferred, not stated: `marcus-meditations` (PG 2680) reads as Casaubon, not Long. Lane B cross-references them and fetched the real translations; the Adler file itself was not touched.
2. **The build's `odyssey-eng4` is Butler revised by Power and Nagy** (a modern revision), not Butler's 1900 text. The plain 1900 text is now on the Homer shelf.
3. **No duplicate uids:** two Jowett texts already on the Adler shelf (Republic, Apology) were taken off the Plato fetch list and cross-referenced.

## Decisions that are yours

- **Mint:** every lane B slug awaits your single-writer minting pass. Do raw IA volumes get uids, or only converted texts?
- **US-only public domain:** a few Gutenberg texts are PD in the US but not in life+70 countries (Murray's Euripides, Sophocles and Aeschylus, and now his Rhesus from Perseus; Humphries's Aeneid; Fyfe's Histories; Lindsay's Lysistrata; Rouse's Apocolocyntosis; Firebaugh's Satyricon). Also the Oxford Aristotle as a whole. Keep or drop?
- **Perseus share-alike:** the 243 Perseus texts are PD translations in CC BY-SA 4.0 markup. Serving the TEI (or anything built from its markup) means crediting Perseus and sharing changes alike. Taking the plain text out of the markup is the usual reading of what is free. Your call on how Armarium serves them.
- **Babbitt's Moralia vols. 1-2 (1927-28):** shelved here as US PD by date. PR #7's notes exclude "Moralia (Babbitt)" for copyright, probably for the later volumes (1931-), which are not shelved here. Confirm the line.
- **Bilingual Loebs:** Latin-facing Loebs of 1930 or earlier are now taken (Statius, Quintilian, Ausonius, Frontinus), because Latin OCR is legible. Greek-facing Loebs are still held back as pending, because their Greek OCR is junk (Paton, Edmonds, Mair, Sandys, Hicks, Cary's Dio). Keep that line?
- **More US-only PD:** several 1913-1930 Loebs and MacKenna's Plotinus are PD in the US by publication date. In life+70 countries each translator's death date decides; not checked per translator.
- **Unassigned:** Josephus (Whiston, PG 2846-2850) and Prudentius (Pope, PG 14959) are on no lane's shelf. Lane B left them alone, since they may belong to lane A.

## Defects

- Mathematical OCR (Heath's Euclid, Archimedes, Conics) is the weakest raw text: clean-word 0.73-0.83.
- One Perseus source is a later reprint: Aretaeus (Adams 1856) was digitised from a 1972 photographic reprint. It is kept, with the reason in the shelf's `_rights_checked`.
- Re-verify on 2026-10-02: all 84 lane B shelves pass `fetch_shelf.py --verify`, with 0 wrong books.

- Raw OCR is unproofread: clean-word ratio 0.74-0.95 per volume (worst: Oxford Aristotle vol. VI 0.81, Jowett's Thucydides notes 0.79).
- Two Gutenberg texts name no translator and were identified by collation: Rhoades's Eclogues (PG 230), Ridley's Lucan (PG 602).
- Verse texts need the verse converter; tried divisions are recorded as `_convert_hints` in the Virgil and Ovid shelves.
