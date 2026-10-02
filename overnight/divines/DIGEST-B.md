# Lane B digest — Classical (English translations)
<!-- refreshed 2026-10-02 16:35 CDT by the lane B worker -->

**Held:** 84 shelves, 357 files (243 clean Gutenberg texts, 114 raw Internet Archive OCR volumes), 262 MB on the worker's disk. Corpus text is gitignored; the shelves (`pipeline/<author>_shelf.json`) are the record. Nothing converted into the build manifest and **nothing minted** (no uid minting during a burst). Every shelf lists its pending wishlist and its exclusions with reasons; the map section is `docs/divines-map/B-classical.md`.

| Author | Held (clean / raw) | Pending, short |
|---|---|---|
| Plato (Jowett) | 27 / 5 | Bohn Plato for the dialogues Jowett omitted |
| Aristotle (Oxford, Smith & Ross) | 0 / 11 | vol. III (US PD 2027-01-01), vol. XII (1952) |
| Hesiod (Evelyn-White) | 1 / 0 | Elton |
| Ovid (Riley; Golding, Howard) | 6 / 3 | Marlowe's Elegies, Brookes More |
| Virgil (Rhoades, Conington, + 4 Aeneids) | 7 / 3 | Williams's Eclogues/Georgics |
| Homer (Chapman, Pope, Cowper, Derby, Buckley, Butler, Bryant) | 9 / 4 | Murray's Loebs |
| Aeschylus, Euripides, Sophocles | 19 / 5 | Smyth, Potter, Plumptre's Sophocles |
| Aristophanes | 5 / 0 | Rogers complete, Frere |
| Herodotus, Thucydides, Xenophon, Polybius, Arrian | 20 / 7 | Cary, Loebs |
| Plutarch (North, Langhorne, Stewart-Long; Goodwin Moralia) | 13 / 12 | Holland's Morals |
| Marcus Aurelius, Epictetus, Seneca | 13 / 5 | Gummere's Epistles (Latin facing) |
| Tacitus, Livy, Caesar, Suetonius, Sallust, Pliny | 20 / 2 | Holland's Livy/Suetonius/Pliny |
| Lucretius, Horace, Catullus, Tibullus, Juvenal, Plautus & Terence, Lucan, Apuleius, Petronius | 17 / 5 | Creech, Smart, Rowe |
| Lucian, Cicero | 16 / 6 | Winstedt's Atticus |
| Greek orators (Demosthenes, Lysias, Isocrates) | 4 / 5 | Kennedy vol. 5 |
| Greek poets (Pindar, Theocritus, Apollonius, Quintus, lyric and Anthology) | 9 / 4 | Paton, Edmonds, Mair (Greek-facing Loebs); Musaeus |
| Late philosophy (Diogenes, Plotinus incl. MacKenna 1917-30 complete, Porphyry, Iamblichus, Proclus, Sextus, Julian, Boethius) | 21 / 8 | Wright's Julian vol. 3 |
| Geographers and historians (Pausanias, Strabo, Appian, Diodorus, Dio, Athenaeus, Procopius, Greek romances) | 20 / 7 | Taylor's Pausanias vol. 3, Frazer |
| Science (Euclid, Archimedes, Apollonius of Perga, Hippocrates, Galen, Aretaeus, Theophrastus, Hero, Ptolemy) | 5 / 9 | Robinson's Method (fetcher can't read PG 7825) |
| Latin silver and late (Martial, Statius, Claudian, Quintilian, Vitruvius, Gellius, Ammianus, Ausonius, Frontinus, Celsus, Cato/Varro, Phaedrus, Watson's epitomators, Justinian) | 9 / 19 | Beloe's Gellius vol. 2, Hawkins's Claudian vol. 2 |
| Dionysius of Halicarnassus, Augustus | 2 / 0 | |

## Look at these first (Adam)

1. **The Adler shelf has six wrong labels**, all checked against the Gutenberg files: `thucydides-pelo` (PG 7142) is Crawley, not Jowett; `tacitus-annals` (PG 7959) is Gordon's Annals I-VI selection, not Church & Brodribb; `epictetus-discourses` (PG 45109) is Higginson's Enchiridion, not Matheson's Discourses; `lucretius-nature` (PG 785) is Leonard, not Munro; `herodotus-history` (PG 2707) is Macaulay vol. 1 only; `plato-dialogues` (PG 1656) is the Apology alone. One more is inferred, not stated: `marcus-meditations` (PG 2680) reads as Casaubon, not Long. Lane B cross-references them and fetched the real translations; the Adler file itself was not touched.
2. **The build's `odyssey-eng4` is Butler revised by Power and Nagy** (a modern revision), not Butler's 1900 text. The plain 1900 text is now on the Homer shelf.
3. **No duplicate uids:** two Jowett texts already on the Adler shelf (Republic, Apology) were taken off the Plato fetch list and cross-referenced.

## Decisions that are yours

- **Mint:** every lane B slug awaits your single-writer minting pass. Do raw IA volumes get uids, or only converted texts?
- **US-only public domain:** a few Gutenberg texts are PD in the US but not in life+70 countries (Murray's Euripides, Sophocles and Aeschylus; Humphries's Aeneid; Fyfe's Histories; Lindsay's Lysistrata; Rouse's Apocolocyntosis; Firebaugh's Satyricon). Also the Oxford Aristotle as a whole. Keep or drop?
- **Perseus:** `docs/perseus-census.md` counts 832 English texts the repo lacks, 625 likely US PD. Fetching them needs a `PERSEUS` manifest entry or a Perseus mode in `fetch_shelf.py`.
- **Bilingual Loebs:** Latin-facing Loebs of 1930 or earlier are now taken (Statius, Quintilian, Ausonius, Frontinus), because Latin OCR is legible. Greek-facing Loebs are still held back as pending, because their Greek OCR is junk (Paton, Edmonds, Mair, Sandys, Hicks, Cary's Dio). Keep that line?
- **More US-only PD:** several 1913-1930 Loebs and MacKenna's Plotinus are PD in the US by publication date. In life+70 countries each translator's death date decides; not checked per translator.
- **Unassigned:** Josephus (Whiston, PG 2846-2850) and Prudentius (Pope, PG 14959) are on no lane's shelf. Lane B left them alone, since they may belong to lane A.

## Defects

- Mathematical OCR (Heath's Euclid, Archimedes, Conics) is the weakest raw text: clean-word 0.73-0.83.
- `fetch_shelf.py` cannot read Gutenberg files that are served only gzip-encoded (PG 7825 answers HTTP 406). A backward-compatible fix would send `Accept-Encoding: gzip` and decompress.
- Re-verify on 2026-10-02: all 84 lane B shelves pass `fetch_shelf.py --verify`, with 0 wrong books.

- Raw OCR is unproofread: clean-word ratio 0.74-0.95 per volume (worst: Oxford Aristotle vol. VI 0.81, Jowett's Thucydides notes 0.79).
- Two Gutenberg texts name no translator and were identified by collation: Rhoades's Eclogues (PG 230), Ridley's Lucan (PG 602).
- Verse texts need the verse converter; tried divisions are recorded as `_convert_hints` in the Virgil and Ovid shelves.
