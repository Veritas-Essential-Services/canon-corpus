# Lane B digest — Classical (English translations)
<!-- refreshed 2026-10-02 17:31 CDT by the lane B worker -->

**Held:** 84 shelves, 691 files (249 clean Gutenberg texts, 199 raw Internet Archive OCR volumes, 243 Perseus TEI texts at the time; 132 after the 21:10 review moved 111 duplicates to `_held`), 388 MB on the worker's disk. Corpus text is gitignored; the shelves (`pipeline/<author>_shelf.json`) are the record. Nothing converted into the build manifest and **nothing minted** (no uid minting during a burst). Every shelf lists its pending wishlist and its exclusions with reasons; the map section is `docs/divines-map/B-classical.md`.

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
| Plutarch (North, Langhorne, Stewart-Long; Goodwin Moralia; Holland's Morals) | 13 / 14 + 91 Perseus Moralia (Goodwin 1874 ed.; Babbitt vols. 1-2) | none known |
| Marcus Aurelius, Epictetus, Seneca | 13 / 5 | Gummere's Epistles (Latin facing) |
| Tacitus, Livy, Caesar, Suetonius, Sallust, Pliny | 20 / 2 | Holland's Livy/Suetonius/Pliny |
| Lucretius, Horace, Catullus, Tibullus, Juvenal, Plautus & Terence, Lucan, Apuleius, Petronius | 17 / 5 | Creech, Smart, Rowe |
| Lucian, Cicero | 16 / 6 + 52 Perseus Lucian (Harmon 1913-25, E. J. Smith, the Fowlers) | Francklin's complete Lucian |
| Greek orators (Demosthenes, Lysias, Isocrates) | 4 / 6 + 54 Perseus (Vince 1926 and 1930, Lamb 1930) | none known |
| Greek poets (Pindar, Theocritus, Apollonius, Quintus, lyric and Anthology) | 9 / 4 | Paton, Edmonds, Mair (Greek-facing Loebs); Musaeus |
| Late philosophy (Diogenes, Plotinus incl. MacKenna 1917-30 complete, Porphyry, Iamblichus, Proclus, Sextus, Julian, Boethius) | 21 / 8 | Wright's Julian vol. 3 (Greek facing) |
| Geographers and historians (Pausanias, Strabo, Appian, Diodorus, Dio, Athenaeus, Procopius, Greek romances) | 20 / 7 | Frazer's translation volume (1898) |
| Science (Euclid, Archimedes, Apollonius of Perga, Hippocrates, Galen, Aretaeus, Theophrastus, Hero, Ptolemy) | 6 / 9 + 27 Perseus (Adams's Hippocrates and Aretaeus, Jones, Heath, Brock) | Heath 2nd ed. (1926) |
| Latin silver and late (Martial, Statius, Claudian, Quintilian, Vitruvius, Gellius, Ammianus, Ausonius, Frontinus, Celsus, Cato/Varro, Phaedrus, Watson's epitomators, Justinian) | 9 / 20 | Hawkins's Claudian vol. 2 |
| Dionysius of Halicarnassus, Augustus | 2 / 0 | |

## Added since the first digest (2026-10-02, 16:35-17:05 CDT)

- **61 Latin-facing Loeb volumes (1912-1930)** on 20 existing shelves, e.g. Gummere's Seneca Epistles, Fairclough's Virgil, Miller's Metamorphoses, Rolfe's Suetonius/Sallust/Gellius, Butler's Quintilian, Foster's Livy 1, 3-5, Williams's Cicero Letters to Friends. Winstedt's Letters to Atticus now from clean Gutenberg. Refused: Livy vol. 2 (scan is the 1939 revised printing), Plautus vols. 4-5 (1932, 1938), Basore vol. 3 (1935).
- **Older English translators from the map's wishlists:** Potter's Aeschylus and Wodhull's complete Euripides (Greek Tragic Theatre, 1809), Swanwick, Plumptre's Sophocles, Creech's Lucretius, Rowe's Lucan vol. 1, Carter's Epictetus, Cary's Herodotus, Holland's Pliny (1601) and Livy (1659 ed.), Gordon's Tacitus (5 vols.), Hampton's Polybius, Smith's Thucydides, Collier's and Rendall's Marcus, Norgate's Iliad, Hobbes's Homer, Cranch's Aeneid, T. C. Williams's Georgics, Elton's Hesiod, Bysshe's Memorabilia.
- **fetch_shelf.py** now reads Gutenberg files served only gzip-encoded (one-line retry on HTTP 406); Robinson's Archimedes fetched with it.
- **Grey area for you:** some kept Loeb scans are later reprints (e.g. 1931-1969) of pre-1931 editions with no revision notice; two carry pre-1930 revisions (Miller's Seneca vol. 2, Fairclough's Horace, both 1929). Their text is that of the pre-1931 edition.

## Added since the second digest (2026-10-02, 17:07-17:31 CDT)

- **243 Perseus TEI English texts** (132 since the 21:10 review: 111 duplicates moved to `_held`) under a new `"perseus"` key in 19 shelves, fetched by a new, separate `pipeline/fetch_perseus.py` (fetch_shelf.py is unchanged for them). Deduped against the 309 Perseus ids on PR #7; Philo (PR #8) and the fathers, apocrypha and Bible rows left to their owners. Each file's own sourceDesc dates the translation (all 1930 or earlier, except one reprint noted under Defects); the markup licence travels in each `<shelf>_perseus_report.json`.
- **Five missing volumes found under other ids:** Nixon's Plautus vol. 2 (1917), Francklin's complete Sophocles (1759), Beloe's Gellius vol. 2 (1795), Kennedy's Demosthenes vol. 5 (1878) and Rowe's Lucan vol. 2 (1812). Title pages were read.
- **Refused or held:** King's Tusculans (only the 1945 revised printing has text), Wright's Julian vol. 3 (Greek facing). Still not found: Frazer's Pausanias vol. 1, Hawkins's Claudian vol. 2, and vol. 2 of the 1809 Greek Tragic Theatre.

## Look at these first (Adam)

1. **The Adler shelf has six wrong labels**, all checked against the Gutenberg files: `thucydides-pelo` (PG 7142) is Crawley, not Jowett; `tacitus-annals` (PG 7959) is Gordon's Annals I-VI selection, not Church & Brodribb; `epictetus-discourses` (PG 45109) is Higginson's Enchiridion, not Matheson's Discourses; `lucretius-nature` (PG 785) is Leonard, not Munro; `herodotus-history` (PG 2707) is Macaulay vol. 1 only; `plato-dialogues` (PG 1656) is the Apology alone. One more is inferred, not stated: `marcus-meditations` (PG 2680) reads as Casaubon, not Long. Lane B cross-references them and fetched the real translations; the Adler file itself was not touched.
2. **The build's `odyssey-eng4` is Butler revised by Power and Nagy** (a modern revision), not Butler's 1900 text. The plain 1900 text is now on the Homer shelf.
3. **No duplicate uids:** two Jowett texts already on the Adler shelf (Republic, Apology) were taken off the Plato fetch list and cross-referenced.

## Decisions that are yours

- **Mint:** every lane B slug awaits your single-writer minting pass. Do raw IA volumes get uids, or only converted texts?
- **US-only public domain:** a few Gutenberg texts are PD in the US but not in life+70 countries (Murray's Euripides, Sophocles and Aeschylus, and now his Rhesus from Perseus; Humphries's Aeneid; Fyfe's Histories; Lindsay's Lysistrata; Rouse's Apocolocyntosis; Firebaugh's Satyricon). Also the Oxford Aristotle as a whole. Keep or drop?
- **Perseus share-alike:** the 132 Perseus texts are PD translations in CC BY-SA 4.0 markup. Serving the TEI (or anything built from its markup) means crediting Perseus and sharing changes alike. Taking the plain text out of the markup is the usual reading of what is free. Your call on how Armarium serves them.
- **Babbitt's Moralia vols. 1-2 (1927-28):** shelved here as US PD by date. PR #7's notes exclude "Moralia (Babbitt)" for copyright, probably for the later volumes (1931-), which are not shelved here. Confirm the line.
- **Bilingual Loebs:** Latin-facing Loebs of 1930 or earlier are now taken (Statius, Quintilian, Ausonius, Frontinus), because Latin OCR is legible. Greek-facing Loebs are still held back as pending, because their Greek OCR is junk (Paton, Edmonds, Mair, Sandys, Hicks, Cary's Dio). Keep that line?
- **More US-only PD:** several 1913-1930 Loebs and MacKenna's Plotinus are PD in the US by publication date. In life+70 countries each translator's death date decides; not checked per translator.
- **One rule for later printings, your call (applies to all of these at once):** each is a public-domain translation, but the copy scanned or keyed is a printing made after 1930 that says 'reprinted', not 'revised'. Kept for now, each with its reason in the shelf's `_rights_checked`: `aristotle-ross-v09` (1931 impression of 1925), `aristotle-ross-v02` (lithographic reprint of 1930 sheets), `horace-bennett-loeb-odes` (later Loeb impression of 1914), the three Cicero Loebs `cicero-watts-pro-archia-etc` (1923), `cicero-grose-hodge-pro-lege-manilia-etc` (1927) and `cicero-freese-pro-quinctio-etc` (1930) from 1960s reprints, `quintilian-butler-v1-1921` (later series editors, no addendum), `velleius-shipley-res-gestae` (1961 reprint of 1924), `marcus-aurelius-casaubon-everyman` (1948 reprint of the 1906 Everyman), the three `aeschines-perseus-adams-*` (1919 text, keyed from a 1958 printing) and the twelve `isaeus-perseus-forster-*` (1927 text, keyed from a 1962 printing). In the same position but refused, because no reason was written when it came up: Freese's Loeb Rhetoric on Perseus (1926 text, 1947 printing; `aristotle_shelf.json` `_excluded`), and Duff's Loeb Silius Italicus vol. I (1927 text, only a 1961 reprint scanned; `silius_shelf.json` `_excluded`). Keep the whole class (and take Freese), or drop the whole class?
- **Perseus's modernized texts, your call:** Godley's Herodotus (`herodotus-perseus-godley-histories`) and the seven Smyth Aeschylus plays (`aeschylus-perseus-smyth-*`) are not the translations as printed: each Perseus header says the text was modernized to remove archaisms, by a named Perseus editor, and then revised. The translations are public domain; the modernization is Perseus's, under the same CC BY-SA 4.0 as its markup. Kept for now as Perseus's modernized witnesses, each with a `_rights_checked` reason, and `fetch_perseus.py` now refuses any modernized file that lacks one. Keep them as modernized witnesses, or drop them and wait for the printed Loebs?
- **Undated or inferred, listed so you can see them (no decision asked):** `pliny-younger-firth-letters-2` prints no date; its date is inferred from the First Series, which Gutenberg clears, in the same Scott Library imprint. Three Harmon Lucian files on Perseus print no year; they are dated from the volume they name (vol. 1, 1913).
- **Unassigned:** Josephus (Whiston, PG 2846-2850) and Prudentius (Pope, PG 14959) are on no lane's shelf. Lane B left them alone, since they may belong to lane A.

## Defects

- Mathematical OCR (Heath's Euclid, Archimedes, Conics) is the weakest raw text: clean-word 0.73-0.83.
- One Perseus source is a later reprint: Aretaeus (Adams 1856) was digitised from a 1972 photographic reprint. It is kept, with the reason in the shelf's `_rights_checked`.
- Re-verify on 2026-10-02: all 84 lane B shelves pass `fetch_shelf.py --verify`, with 0 wrong books.

- Raw OCR is unproofread: clean-word ratio 0.74-0.95 per volume (worst: Oxford Aristotle vol. VI 0.81, Jowett's Thucydides notes 0.79).
- Two Gutenberg texts name no translator and were identified by collation: Rhoades's Eclogues (PG 230), Ridley's Lucan (PG 602).
- Verse texts need the verse converter; tried divisions are recorded as `_convert_hints` in the Virgil and Ovid shelves.

## Review fixes, 2026-10-02 21:10 CDT (for Adam)
- **Duplicates now under `_held`, not fetched as second witnesses:** 111 Perseus TEI rows that repeat a translation already on the same shelf (Plutarch's Goodwin Moralia 77, Adams's Hippocrates 17 and Aretaeus 4, Brock's Galen, Burton and Smithers's Catullus, Heath's Euclid, Conington's Odes, Long and Higginson's Epictetus 4, the Fowlers' Lucian 2, Rolfe's Julius, Murray's Rhesus). 132 Perseus rows remain. Also held: Cary's Pindar (lane C's cary shelf), PG 6762 and 8438 (Adler shelf), Edghill's Categories (Oxford vol. I).
- **Adler shelf label error, yours to fix:** `adler_shelf.json` labels PG 6762 (aristotle-politics) "tr. Jowett", but Gutenberg's header names William Ellis (his 1776 translation). Lane B does not edit that file.
- **Held back on rights:** Seneca his Tenne Tragedies (Tudor Translations, 1927) carries T. S. Eliot's introduction: US public domain by date, but not life+70. Take the text without it, or the 1581 or 1887 printings?
- **Withdrawn again:** Smart's 1756 Horace and Thornton's 1767 Plautus. The ECCO OCR is 0.65-0.76, and nothing new justified retaking them.
- **Collated:** PG 14020 (anonymous literal Horace) matches Smart's prose as Buckley revised it (107 of 200 sampled 8-word runs), not the 1756 form. Both are kept; is one enough?

## Review fixes, round 3 (2026-10-02 21:17 CDT, for Adam)
- **Translator checks now use full names.** A one-word claim such as "long", "west" or "smith" matched almost any English text. 614 claims were rewritten to the fullest form the text itself prints (e.g. "george long", "thomas gordon", "john mason good", "george baker"); 7 distinctive surnames stay one word (Golding, Yonge, Kennedy, Poste, Merrick, Langhorne, Hampton). Several values were junk from the old parser ("german", "eugene", "john", "catalogue", "edition", "super") and are fixed.
- **Moved to `_translator_unchecked`** where no full name survives in the OCR: Gilbert West's Pindar, North's Plutarch vol. 3, Lodge's Seneca 1614, Heath's Archimedes (garbled title page), Evelyn White's Ausonius vol. 1, Watson's Cicero On Oratory, plus three catalogue attributions (Norgate's Iliad, Laurent's Pindar, Lewis's Thebaid) and Plato's Alcibiades II. The texts are kept; only the proof is missing.
- **Curtius:** Brende 1553 (OCR prints "lohn Brence") and Digby vol. 2 (no title page) now carry translator claims kept by `_identity_checked`, with the reason.
- **Gates tightened:** `fetch_perseus.py` refuses a file whose sourceDesc prints no year unless `_rights_checked` dates it (three Harmon vol. 1 pieces, 1913, are dated that way); `fetch_shelf.py` matches the Gutenberg Translator(s) header by whole word, never substring.
- **Held back on rights (six volumes), 21:25 CDT.** No converter rule can drop added matter yet (the converter is not lane B's file), so these are now `_held`, not fetched, each with its source id kept for retaking:
  - two scans are REVISED texts, not the pre-1931 ones: Rolfe's Suetonius vol. 1 (revised 1951) and Williams's Cicero Letters to Friends vol. 3 (revised with additions 1954);
  - four carry a later bibliography: Nixon's Plautus vol. 3 (note of 1979), Butler's Quintilian vol. 1 (addendum of 1980), Miller's Metamorphoses vol. 1 (1960s-70s items), and Wright's Julian vol. 1, whose Gutenberg transcription (PG 48664) includes the 1980 addendum.
  The four addenda are bare reading lists (a few dozen citations). Lists of facts like that may not be protectable at all; that is your call. One word releases them, or a converter cut rule does.

## Added since the review fixes (2026-10-02, 21:08-21:54 CDT)
- **Clean Perseus texts that were waiting:** Plato in the Loeb versions of Fowler, Lamb and Bury (35 dialogues and the Letters, 1914-29), Xenophon's Memorabilia, Oeconomicus, Symposium, Apology and minor works (Marchant, Todd), Brookes More's complete blank-verse Metamorphoses (1922), and Jones's Epidemics. The map's old line saying More's complete text was "not cleared" is replaced: Perseus encodes the 1922 Cornhill printing, all 15 books.
- **Seven new small shelves:** Jordanes, Sidonius, Isaeus, Herodas, Rutilius Namatianus, Solinus, and the two Greek voyages (Periplus, Hanno). Plus Herschel's Frontinus, Royston's Lycophron, Chariton (1764), Xenophon of Ephesus (1727) and Codrington's Justin.
- **Unnamed translators, flagged not guessed:** Chariton 1764 ("made by two young persons"), Xenophon of Ephesus 1727 (name illegible; often given as John Rooke, not verified), the Ovid collections of 1813 and 1855.
- **Each book now checked against its own author** on shelves holding several (a Lycophron used to pass on "Callimachus").
- **Victorian scholars' versions (21:55-22:05):** Lonsdale and Lee's Globe Virgil and Horace, Davidson-Buckley Virgil, Slater's Silvae, Cranstoun's Catullus and Propertius, Jebb's prose Sophocles, and Way's verse Sophocles (Part I) and Aeschylus (all three parts). Way's Sophocles Part II (1914) is not on IA.
- **Homer's Victorian translators (22:08):** Morris, Palmer, Worsley, Conington, Newman, and Way's Iliad and Odyssey: ten volumes, so the Homer shelf now spans Chapman to Murray.
- **Satirists and comedy (22:13):** three more Juvenals (Madan, Badham, Hodgson), Hickie's and Mitchell's Aristophanes, Mair's Hesiod, Hallard's Theocritus, and Taylor's Pythagorean fragments.
- **Horace, Catullus, Claudian (00:41):** three more Horaces (Martin, Bulwer-Lytton, Gladstone), Lamb's Catullus, and two Claudian translators (Strutt, Howard).
- **Two wishlist volumes found (00:45):** Bennett's Loeb Horace and Firth's second Pliny volume, both on Indian digital-library scans. Each was taken on stated evidence rather than a clean date (neither needs a decision; see the bullet on later impressions): the Bennett is a later printing of the 1914 text, and the Firth scan prints no year.
- **Rouse's Lucretius (00:49):** the 1924 Loeb, from a true first printing. Also the reviewer's round-7 fixes and a `fetch_shelf.py --help` fix.
- **Tacitus and Cicero Loebs (00:53):** Moore's Histories from a 1925 first printing, and three volumes of Cicero's speeches (Watts, Grose Hodge, Freese) from later plain reprints. The Cicero ones are added to your decisions list.
- **Two new shelves (00:56):** the Historia Augusta (Magie, vols. I-II) and Fronto's letters with Marcus Aurelius (Haines, vols. I-II), all from first printings.
- **Quintilian vol. 1 recovered (00:58):** a scan without the 1980 addendum replaces the held volume, so Butler's Quintilian is complete again. The other five held volumes are still held.
- **Ovid and Velleius (01:00):** Mozley's Art of Love volume (1929, first printing) and Shipley's Velleius Paterculus with the Res Gestae (1924 text, later plain reprint).
- **Demosthenes and Marcus Aurelius (01:03):** Leland's Demosthenes, and four more Marcus Aurelius translators (Casaubon, Collier twice, Rendall).
- **Aristotle's older translators (01:08):** eleven volumes from before the Oxford translation (Taylor, Bohn's Browne, Owen and Buckley, Peters, Welldon), plus Ellis's Politics and the Everyman Ethics.
- **Plato and Lucian (01:12):** Whewell's three-volume Plato for English readers, the Davies-Vaughan and Spens Republics, and Tooke's two-volume Lucian.
- **Xenophon's Minor Works (01:13):** the 1813 'several hands' volume (Welwood's Banquet, Bradley's Economics, and an unsigned Memoirs of Socrates).
- **Greek tragedy (01:15):** Whitelaw's and Dale's Sophocles; Campbell's, the Headlams' and Warr's Aeschylus.
- **Pindar and the Bohn Hesiod (01:16):** Paley's Pindar, and Banks's Hesiod-Callimachus-Theognis volume, which brings Tytler's Callimachus in by the back door.
- **Seneca and Apuleius (01:21):** Morell's 1786 Epistles (2 vols) and Taylor's 1822 Apuleius taken. Review round 8 applied: two duplicate rows withdrawn (Everyman Ethics, a second Rendall row), and the later-impression list now asks you only about Ross v09.
- **Aeschines, Livy and Quintilian (01:30):** a new Aeschines shelf (Adams's Loeb speeches, from Perseus; the record names a 1958 printing of the 1919 text, so it waits on the later-printings decision above), Church and Brodribb's Livy XXI-XXV (1883), and Watson's two-volume Quintilian. Eighteen stale 'pending' notes now say the work is held.
- **Perseus fill (01:35):** 88 English-only Perseus texts by translators not yet held: Perrin's Plutarch Lives (66), Norlin's Isocrates (11), Smyth's Aeschylus (7), Godley's Herodotus, Hicks's Diogenes Laertius, Rackham's Ethics and Frazer's Epitome. Godley and Smyth come in Perseus's modernized spelling, and the rows say so; Freese's Rhetoric (1947 printing) is held back with the later-printings decision above.
- **Perseus 'check' rows (01:38):** Forster's Isaeus (twelve speeches, 1927 text in a 1962 printing, waiting on the later-printings decision above) and Miller's Cyropaedia (1914; the census had confused Miller's death year for a printing). Nothing else in the Perseus census is both public domain and lane B's.
- **Five more second translators (01:45):** Ridley's Lucan (1896 and the revised 1905), Lewis's Thebaid (2 vols), Wheelwright's complete Aristophanes (2 vols, 1837), Cary's and Wheelwright's Pindar, and Littlebury's Herodotus (2 vols, 1737).
- **Bohn and Victorian verse (01:52):** Martin's complete Horace (2 vols), the Kennedys' Virgil (2 vols), half of Pitt and Warton's 1763 Virgil, Burges's Greek Anthology, the Bohn Martial and Kelly's Erotica (which also carries Lamb's whole verse Catullus, so the missing Lamb vol. II matters less). Pitt's 1740 Aeneid and Potter's Sophocles were refused for OCR.
- **Review round 9 (01:57):** the later printings and Perseus's modernized texts are now two decisions for you, above, instead of being settled in the lane. Every Perseus text carries its CC BY-SA limit (redistribute_whole false) in the shelf. A duplicate Cary Pindar row was withdrawn.
- **Nicomachus and the Hermetica (02:04):** D'Ooge's Introduction to Arithmetic (1926), and a new Hermetica shelf with Chambers's translation (1882), Everard's Divine Pymander (1884 reprint of 1650) and Mead's three-volume Thrice-Greatest Hermes (1906).
- **Late Platonists (02:10):** Stanhope's Epictetus with Simplicius's commentary (1741), Taylor's Sallust on the Gods with Demophilus (1793), and a new Orphica shelf with Taylor's Hymns of Orpheus (1787). Taylor's Julian orations, the 1896 Alciphron and Scott's Hermetica were refused for OCR.
- **Proclus and Boethius (02:13):** Taylor's two-volume Proclus on the Timaeus (1820), Ridpath's Boethius (1785) and Colville's (1556, in Bax's 1897 edition). Queen Elizabeth's Boethius is on the retry list (archive.org errors).
- **Seneca's tragedies (02:15):** Bradshaw's 1902 prose translation.
- **Alexander in India (02:17):** McCrindle's 1893 translations from Arrian, Curtius, Diodoros, Plutarch and Justin.
- **Silius Italicus (02:18):** new shelf; Tytler's 1828 verse Punics vol. I. Duff's Loeb vol. I joins the later-printings decision.
- **Cebes (02:20):** new shelf; Guthrie's 1910 translation of the Tablet.
- **Bohn gaps (02:23):** Riley's Lucan (1853) and M'Mahon's Metaphysics (1857). Aelian and Mela have no readable English scan.
- **More single translations (02:27):** Walford's Aristotle, Webster's Medea, King's Julian (with Gregory Nazianzen's Invectives), and four Prometheus Bound versions.
- **Agamemnon (02:30):** four more versions (Harford 1831, Milman 1865, Paton 1907, Locke Ellis 1920). Harford's name is from the catalogue only.
