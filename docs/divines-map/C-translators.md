# Translator shelves (each title its own uid; cross-referenced by author sections)

## Dryden

Shelf: `pipeline/dryden_shelf.json` · fetch `python3 pipeline/fetch_shelf.py dryden` · cut titles `python3 pipeline/split_shelf_titles.py dryden`.
Clean text = Project Gutenberg's transcription of Scott's *Works of John Dryden* (18 vols, 1808; PG reprints the 1821 2nd ed.) + PG 228. Titles are cut from those volumes by heading marker; not yet converted to unit-id JSON (the existing converters need a `fetch_sources.py` manifest entry, which the relay may not edit). **No uids minted** — every title awaits Adam's minting pass.

| Title slug | Translates | Work | Status | Source |
|---|---|---|---|---|
| `dryden-aeneid` | Virgil | Aeneid, 12 books (1697) | have | PG 228 (also Scott 14–15) |
| `dryden-aeneid-dedication` | Virgil | Dedication of the Aeneis (Dryden's essay) | have | Scott 14 |
| `dryden-georgics` | Virgil | Georgics I–IV (1697) | have | Scott 14 |
| `dryden-eclogues` | Virgil | Pastorals I–X (1697) | have | Scott 13 |
| `dryden-metamorphoses` | Ovid | Metamorphoses I–XV, Garth composite ed. (1717; 1826 reprint) — **many hands**, Dryden's share is I, XII and episodes | have-raw | IA `ovidsmetamorphos00ovid` |
| `dryden-ovid-metamorphoses` | Ovid | Metamorphoses: Dryden's own share (I, XII, Ajax & Ulysses, Pythagorean Philosophy, 9 episodes) | have | Scott 12 |
| `dryden-ovid-epistles` | Ovid | Heroides: Canace, Helen, Dido (1680) | have | Scott 12 |
| `dryden-ovid-art-of-love` | Ovid | Ars Amatoria I | have | Scott 12 |
| `dryden-ovid-amores` | Ovid | Amores I.1, I.4 | have | Scott 12 |
| `dryden-theocritus` | Theocritus | Idylls III, XVIII, XXIII, XXVII | have | Scott 12 |
| `dryden-lucretius` | Lucretius | De Rerum Natura, selections I–V | have | Scott 12 |
| `dryden-horace` | Horace | Odes I.3, I.9, I.29; Epode 2 | have | Scott 12 |
| `dryden-iliad` | Homer | Iliad I; Hector and Andromache (VI) | have | Scott 12 |
| `dryden-juvenal` | Juvenal | Satires I, III, VI, X, XVI + Discourse on Satire (1693) | have | Scott 13 |
| `dryden-persius` | Persius | Satires I–VI (1693) | have | Scott 13 |
| `dryden-fables-chaucer` | Chaucer (modernised) | Fables: Palamon & Arcite, Cock & Fox, Flower & Leaf, Wife of Bath, Good Parson (1700) | have | Scott 11 |
| `dryden-fables-boccaccio` | Boccaccio | Fables: Sigismonda, Theodore & Honoria, Cymon & Iphigenia (1700) | have | Scott 11 |
| `dryden-veni-creator` | Latin hymn | Veni Creator Spiritus, paraphrased | have | Scott 11 |
| `dryden-xavier` | Bouhours | Life of St Francis Xavier (1688) | have | Scott 16 |
| `dryden-art-of-painting` | Du Fresnoy | De Arte Graphica (1695) | have | Scott 17 |
| `dryden-history-of-the-league` | Maimbourg | History of the League, complete (1684) | have-raw | IA `historyofleague00maim` (long-s OCR) |
| `dryden-fables-1700` | — | Fables Ancient and Modern, 1st ed. (to restore Dryden's own order) | pending | IA `mdu-rare-075246` |
| `dryden-juvenal-1693` | Juvenal | the whole 1693 book incl. the other translators' satires | pending | IA `juvenaldrydensatires` |
| `dryden-virgil-1697` | Virgil | Works of Virgil as a book (folio or a later reprint) | pending | IA `worksvirgilcont00drydgoog` (1721) |
| `dryden-garth-metamorphoses-1717` | Ovid | Garth 1st ed. | pending | IA, long-s OCR; 1826 reprint preferred |
| `dryden-xavier-1688` | Bouhours | 1st ed. | pending | IA `gpl_1784827` |
| — | Plutarch | "Dryden's Plutarch" | excluded | 41 translators; Malone: "Dryden translated none of the Lives" |
| — | Polybius, Lucian | Dryden's prefaces to others' translations | excluded | not translations |
| — | — | PG 24901, John Fairfield Dryden (US senator) | excluded | wrong Dryden |

## Garnett
