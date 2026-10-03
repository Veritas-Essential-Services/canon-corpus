# Translator shelves (each title its own uid; cross-referenced by author sections)

## Dryden

Shelf: `pipeline/dryden_shelf.json` · fetch `python3 pipeline/fetch_shelf.py dryden` · cut titles `python3 pipeline/split_shelf_titles.py dryden`.
Clean text = Project Gutenberg's transcription of Scott's *Works of John Dryden* (18 vols, 1808; PG reprints the 1821 2nd ed.) Titles are cut from those volumes by heading marker; not yet converted to unit-id JSON (the existing converters need a `fetch_sources.py` manifest entry, which the relay may not edit). **No uids minted** — every title awaits Adam's minting pass. Translator for every row: John Dryden (the Garth Metamorphoses is many hands).

Overlap: `dryden-metamorphoses` (Garth 1826, all translators) contains `dryden-ovid-metamorphoses` (Scott 12, Dryden's share). Two witnesses of Dryden's lines, not two passages.

| Title slug | Translates | Work | Status | Source |
|---|---|---|---|---|
| `dryden-aeneid` | Virgil | Aeneid, 12 books (1697) | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `virgil-eclogues` (PG 228; adler's title "Eclogues, Georgics, Aeneid" is wrong, PG 228 is the Aeneid only). Scott 14–15 is a second witness. |
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

Shelf: `pipeline/garnett_shelf.json` · fetch `python3 pipeline/fetch_shelf.py garnett` · titles `python3 pipeline/split_shelf_titles.py garnett`.
All first published 1894–1927: US public domain (pre-1931), UK PD since 2017. Year = first publication of her translation; later printings scanned are recorded in the shelf as `scan_edition`. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `garnett-karamazov` | Dostoevsky | The Brothers Karamazov | Constance Garnett | 1912 | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `dostoevsky-karamazov` (PG 28054) |
| `garnett-idiot` | Dostoevsky | The Idiot | Constance Garnett | 1913 | have-raw | IA `idiotnovelinfour0000fyod` |
| `garnett-possessed` | Dostoevsky | The Possessed | Constance Garnett | 1913 | have | PG 8117 |
| `garnett-crime-and-punishment` | Dostoevsky | Crime and Punishment | Constance Garnett | 1914 | have | PG 2554 |
| `garnett-gambler` | Dostoevsky | The Gambler, and Other Stories | Constance Garnett | 1914 | have-raw | IA `dostoyevsky_fyodor_1821_1881_gambler` |
| `garnett-house-of-the-dead` | Dostoevsky | The House of the Dead | Constance Garnett | 1915 | have-raw | IA `bwb_O4-BDO-591` |
| `garnett-insulted-and-injured` | Dostoevsky | The Insulted and Injured | Constance Garnett | 1915 | have-raw | IA `cu31924026647549` |
| `garnett-raw-youth` | Dostoevsky | A Raw Youth | Constance Garnett | 1916 | have-raw | IA `rawyouth0000fyod` |
| `garnett-eternal-husband` | Dostoevsky | The Eternal Husband, and Other Stories | Constance Garnett | 1917 | have-raw | IA `eternalhusbandot00dost_3` |
| `garnett-white-nights` | Dostoevsky | White Nights, and Other Stories (incl. Notes from Underground) | Constance Garnett | 1918 | have | PG 36034 |
| `garnett-honest-thief` | Dostoevsky | An Honest Thief, and Other Stories | Constance Garnett | 1919 | have-raw | IA `bwb_O8-AOQ-295` |
| `garnett-friend-of-the-family` | Dostoevsky | The Friend of the Family; and Another Story (Novels vol. XII) | Constance Garnett | 1920 | have-raw | IA `friendoffamily0000fyod` |
| `garnett-anna-karenina` | Tolstoy | Anna Karenina | Constance Garnett | 1901 | have | PG 1399 |
| `garnett-death-of-ivan-ilyitch` | Tolstoy | The Death of Ivan Ilyitch, and Other Stories | Constance Garnett | 1902 | have-raw | IA `deathofivanilyit00tols` |
| `garnett-kingdom-of-god` | Tolstoy | "The Kingdom of God Is Within You" | Constance Garnett | 1894 | have | PG 43302 |
| `garnett-christianity-and-patriotism` | Tolstoy | Christianity and Patriotism, with Pertinent Extracts from Other Essays | Constance Garnett | 1922 | have-raw | IA `christianitypatr00tols` |
| `garnett-chekhov-darling` | Chekhov | Tales of Chekhov vol. 1: The Darling, and Other Stories | Constance Garnett | 1916 | have | PG 13416 |
| `garnett-chekhov-duel` | Chekhov | Tales of Chekhov vol. 2: The Duel, and Other Stories | Constance Garnett | 1916 | have | PG 13505 |
| `garnett-chekhov-lady-with-the-dog` | Chekhov | Tales of Chekhov vol. 3: The Lady with the Dog, and Other Stories | Constance Garnett | 1917 | have | PG 13415 |
| `garnett-chekhov-party` | Chekhov | Tales of Chekhov vol. 4: The Party, and Other Stories | Constance Garnett | 1917 | have | PG 13413 |
| `garnett-chekhov-wife` | Chekhov | Tales of Chekhov vol. 5: The Wife, and Other Stories | Constance Garnett | 1918 | have | PG 1883 |
| `garnett-chekhov-bishop` | Chekhov | Tales of Chekhov vol. 7: The Bishop, and Other Stories | Constance Garnett | 1919 | have | PG 13419 |
| `garnett-chekhov-chorus-girl` | Chekhov | Tales of Chekhov vol. 8: The Chorus Girl, and Other Stories | Constance Garnett | 1920 | have | PG 13418 |
| `garnett-chekhov-schoolmistress` | Chekhov | Tales of Chekhov vol. 9: The Schoolmistress, and Other Stories | Constance Garnett | 1920 | have | PG 1732 |
| `garnett-chekhov-horse-stealers` | Chekhov | Tales of Chekhov vol. 10: The Horse-Stealers, and Other Stories | Constance Garnett | 1921 | have | PG 13409 |
| `garnett-chekhov-schoolmaster` | Chekhov | Tales of Chekhov vol. 11: The Schoolmaster, and Other Stories | Constance Garnett | 1921 | have | PG 13412 |
| `garnett-chekhov-cooks-wedding` | Chekhov | Tales of Chekhov vol. 12: The Cook's Wedding, and Other Stories | Constance Garnett | 1922 | have | PG 13417 |
| `garnett-chekhov-love` | Chekhov | Tales of Chekhov vol. 13: Love, and Other Stories | Constance Garnett | 1922 | have | PG 13414 |
| `garnett-chekhov-witch` | Chekhov | Tales of Chekhov vol. 6: The Witch, and Other Stories | Constance Garnett | 1918 | have-raw | IA `witchotherstorie00chek_0` |
| `garnett-chekhov-letters` | Chekhov | Letters of Anton Chekhov to His Family and Friends | Constance Garnett | 1920 | have | PG 6408 |
| `garnett-chekhov-plays-1` | Chekhov | The Plays of Tchehov vol. 1: The Cherry Orchard, and Other Plays | Constance Garnett | 1923 | have-raw | IA `bwb_KU-274-007` |
| `garnett-chekhov-plays-2` | Chekhov | The Plays of Tchehov vol. 2: Three Sisters, and Other Plays | Constance Garnett | 1923 | have-raw | IA `bwb_KU-774-685` |
| `garnett-turgenev-rudin` | Turgenev | Rudin | Constance Garnett | 1894 | have | PG 6900 |
| `garnett-turgenev-house-of-gentlefolk` | Turgenev | A House of Gentlefolk | Constance Garnett | 1894 | have | PG 5721 |
| `garnett-turgenev-on-the-eve` | Turgenev | On the Eve | Constance Garnett | 1895 | have | PG 6902 |
| `garnett-turgenev-fathers-and-children` | Turgenev | Fathers and Children | Constance Garnett | 1895 | have | PG 30723 |
| `garnett-turgenev-smoke` | Turgenev | Smoke | Constance Garnett | 1896 | have | PG 40813 |
| `garnett-turgenev-torrents-of-spring` | Turgenev | The Torrents of Spring | Constance Garnett | 1897 | have | PG 9911 |
| `garnett-turgenev-lear-of-the-steppes` | Turgenev | A Lear of the Steppes, etc. | Constance Garnett | 1898 | have | PG 52642 |
| `garnett-turgenev-dream-tales` | Turgenev | Dream Tales and Prose Poems | Constance Garnett | 1897 | have | PG 8935 |
| `garnett-turgenev-diary-of-a-superfluous-man` | Turgenev | The Diary of a Superfluous Man, and Other Stories | Constance Garnett | 1899 | have | PG 9615 |
| `garnett-turgenev-desperate-character` | Turgenev | A Desperate Character, and Other Stories | Constance Garnett | 1899 | have | PG 8871 |
| `garnett-turgenev-jew` | Turgenev | The Jew, and Other Stories | Constance Garnett | 1899 | have | PG 8696 |
| `garnett-turgenev-knock-knock-knock` | Turgenev | Knock, Knock, Knock, and Other Stories | Constance Garnett | 1921 | have | PG 7120 |
| `garnett-turgenev-sportsmans-sketches` | Turgenev | A Sportsman's Sketches (2 vols) | Constance Garnett | 1895 | have | PG 8597 + PG 8744 |
| `garnett-turgenev-virgin-soil` | Turgenev | Virgin Soil (2 vols) | Constance Garnett | 1896 | have-raw | IA `virginsoil01turguoft` + IA `virginsoil02turguoft` |
| `garnett-turgenev-two-friends` | Turgenev | The Two Friends, and Other Stories | Constance Garnett | 1921 | have-raw | IA `twofriendsothers00turgrich` |
| `garnett-gogol-dead-souls` | Gogol | Dead Souls (Works of Gogol vols 1-2) | Constance Garnett | 1922 | have-raw | IA `p1theworksofniko01gogo` + IA `pt2theworksofnik01gogouoft` |
| `garnett-ostrovsky-storm` | Ostrovsky | The Storm (play) | Constance Garnett | 1899 | have | PG 7991 |
| `garnett-goncharov-common-story` | Goncharov | A Common Story | Constance Garnett | 1894 | have-raw | IA `cu31924026662183` |
| `garnett-herzen-my-past-and-thoughts` | Herzen | My Past and Thoughts (6 vols) | Constance Garnett | 1924-27 | have | PG 76599 … PG 78377 (6 vols) |
| `garnett-gogol-overcoat` | Gogol | The Overcoat, and Other Stories | Constance Garnett | 1923 | have-raw | IA `overcoatothersto0000niko` |
| `garnett-gogol-dikanka` | Gogol | Evenings on a Farm near Dikanka | Constance Garnett | 1926 | have-raw | IA `Dikanka` |
| `garnett-notes-from-underground` | Dostoevsky | Notes from Underground | Constance Garnett | 1918 | have | PG 36034 (cut from the volume) |
| `garnett-gogol-other` | — | Works of Gogol: The Government Inspector and Other Plays (1926) and Mirgorod (1928) - pre-1931, PD; no verified Garnett scan found (IA mirgorodgogol is a 1924 Potsdam Russian edition, not hers). | — | — | pending | — |
| `garnett-dostoevsky-poor-folk` | — | Poor Folk / Uncle's Dream: no Garnett version verified. The 1915 'Poor Folk and The Gambler' scans on IA are the Everyman (C. J. Hogarth) translation. Whether Garnett ever published these is unverified - do not list as hers without a title page. | — | — | pending | — |
| `garnett-war-and-peace-1904` | — | Heinemann 1904 first printing, wanted to replace the later scan. | — | — | pending | — |
| `garnett-turgenev-novels-1894` | — | The rest of the 15-vol Heinemann set as scans (e.g. IA novelsofivanturg02turg ...): only to replace PG texts if they prove defective. | — | — | pending | — |
| `garnett-war-and-peace` | — | Garnett's War and Peace (Heinemann 1904): the only scan found (bwb_P9-DUB-268) is a 1931+ Modern Library Giant. Pre-1931 IA War and Peace scans are other translators (Maude, Dole, Wiener). Removed 2026-10-02; a 1904 Heinemann or McClure scan would restore it. | — | — | pending | — |
| — | — | pg-600, pg-6536: Notes from Underground standalone: duplicates the text inside garnett-white-nights. | — | — | excluded | — |
| — | — | pg-4602: Older transcription of the same Kingdom of God translation; PG 43302 kept. | — | — | excluded | — |
| — | — | pg-1944: The Witch and Other Stories: almost certainly Garnett's Tales vol. 6, but the PG file names no translator; the dated IA scan is used instead. | — | — | excluded | — |
| — | — | pg-2638, pg-2197, pg-2302, pg-1081, pg-47935: The Idiot (Eva Martin), The Gambler and Poor Folk (C. J. Hogarth), Dead Souls (D. J. Hogarth), Fathers and Sons (Hogarth): not Garnett. | — | — | excluded | — |
| — | — | ia-houseofdeadorpri00dostuoft: House of the Dead 1911: predates Garnett's 1915 version; no Garnett on the title page. | — | — | excluded | — |
| — | — | ia-warpeace01tols_0: War and Peace, Carlton House edition, undated: rule - undatable printings excluded. | — | — | excluded | — |
| — | — | ia-dli/in.ernet scans: Digital Library of India copies: their _djvu.txt files 404 at the expected path; Cornell/Toronto/other scans used instead. | — | — | excluded | — |
| — | — | chekhov-plays-1930-modern-library: The Plays of Anton Tchekov (Modern Library, 1929-30): a reprint of the 1923 volumes, which are used. | — | — | excluded | — |
| — | — | ia-mirgorodgogol: Mirgorod, Potsdam 1924 (Kiepenheuer): a Russian-language edition, not Garnett. | — | — | excluded | — |
| — | — | ia-poorfolkgambler00dost: Poor Folk; The Gambler (1915): Everyman edition, C. J. Hogarth's translation. | — | — | excluded | — |
| — | — | ia-honestthief0000fyod: Heinemann printing reset in 1957 (imprint: first published 1919, reprinted 1923, new impression 1950, reprinted (reset) 1957, reprinted 1962): post-1930 resetting, replaced. | — | — | excluded | — |
| — | — | ia-bwb_KR-628-394: Cherry Orchard and Other Plays, Phoenix Library: imprint 'first issued in the Phoenix Library 1935, reprinted 1940' (a review caught the date; the first pick was wrongly dated 1923). Replaced by the 1925 Chatto printing. | — | — | excluded | — |
| — | — | rawyouth00dostuoft: IA dates it Heinemann 1916, but its imprint page reads 'new impression 1956': a post-1930 printing (review 2026-10-02). | — | — | excluded | — |
| — | — | rawyouthnovelint00dost: IA dates it Macmillan 1916; imprint page reads 'reprinted 1923, 1950, 1956, 1964, 1970': a 1970s printing. | — | — | excluded | — |
| — | — | cu31924014422020: Cornell copy IA-dated 1914, but its imprint page lists new impressions to 1957: a 1957 printing (review 2026-10-02). | — | — | excluded | — |
| — | — | novelsoffyodordo12dost: IA-dated 1920; imprint page reads 'new impression 1949, reprinted 1951, 1961, 1969, 1974'. | — | — | excluded | — |
| — | — | friendoffamily0000unse_r7t4: Heinemann 1920 per IA; imprint page reads reprinted to 1969. | — | — | excluded | — |
| — | — | bwb_P9-DUB-268: Modern Library Giant War and Peace (Random House). IA dates it 1910, but the Giants series began in 1931: a post-1930 printing. | — | — | excluded | — |

## Cary (Dante, Pindar)

Shelf: `pipeline/cary_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cary` · titles `python3 pipeline/split_shelf_titles.py cary`.
Added at the coordinator's relay, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cary-inferno` | Dante | Inferno (Hell) | Henry Francis Cary | 1805-06; revised 1814 | held elsewhere (cross-ref) | `pipeline/fetch_sources.py` → `divine_comedy` (PG 8800) |
| `cary-purgatorio` | Dante | Purgatorio | Henry Francis Cary | 1814 | held elsewhere (cross-ref) | `pipeline/fetch_sources.py` → `divine_comedy` (PG 8800) |
| `cary-paradiso` | Dante | Paradiso | Henry Francis Cary | 1814 | held elsewhere (cross-ref) | `pipeline/fetch_sources.py` → `divine_comedy` (PG 8800) |
| `cary-pindar` | Pindar | Odes (Olympian, Pythian, Nemean, Isthmian) | Henry Francis Cary | 1833 | have-raw | IA `pindarinenglish00carygoog` |
| `cary-aristophanes-birds` | — | Cary's Birds of Aristophanes (1824): no scan found this run. | — | — | pending | — |
| `cary-dore-illustrated` | — | PG 8779-8800 Doré-illustrated Cary: same text split into parts (excluded as duplicates; images are the only difference). | — | — | pending | — |
| — | — | pg-1008: Divine Comedy complete: same text as 1005-1007 together. | — | — | excluded | — |
| — | — | pg-10660: Lives of the English Poets: Cary's own prose, not a translation. | — | — | excluded | — |

## Longfellow (Dante and shorter translations)

Shelf: `pipeline/longfellow_shelf.json` · fetch `python3 pipeline/fetch_shelf.py longfellow` · titles `python3 pipeline/split_shelf_titles.py longfellow`.
Added at the coordinator's relay, vetoable. His Virgil and Ovid pieces stay with lane B. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `longfellow-inferno` | Dante | Inferno | Henry Wadsworth Longfellow | 1867 | have | PG 1001 |
| `longfellow-purgatorio` | Dante | Purgatorio | Henry Wadsworth Longfellow | 1867 | have | PG 1002 |
| `longfellow-paradiso` | Dante | Paradiso | Henry Wadsworth Longfellow | 1867 | have | PG 1003 |
| `longfellow-translations` | various | Translations (Complete Poetical Works): Coplas de Manrique, Spanish ballads and sonnets, Frithiof's Saga passages, German lyrics, Beowulf passage, French, Italian (Michelangelo sonnets, Dante passages), Portuguese, Eastern | Henry Wadsworth Longfellow | 1833-1882 | have | PG 1365 (cut from the volume) |
| `longfellow-latin-pieces` | — | Virgil's First Eclogue and Ovid in Exile, inside longfellow-poetical-works: cross-ref -> lane B's Virgil/Ovid sections; not cut here. | — | — | pending | — |
| `longfellow-poets-and-poetry-of-europe` | — | The Poets and Poetry of Europe (1845): an anthology mostly of OTHER translators; only Longfellow's own pieces would belong here. | — | — | pending | — |
| — | — | pg-1004: Divine Comedy complete: same text as 1001-1003. | — | — | excluded | — |
| — | — | original-poems: Hiawatha, Evangeline etc. are his own poems, not translations (an author section would hold them). | — | — | excluded | — |

## Florio (Montaigne, Decameron)

Shelf: `pipeline/florio_shelf.json` · fetch `python3 pipeline/fetch_shelf.py florio` · titles `python3 pipeline/split_shelf_titles.py florio`.
Added at the coordinator's relay, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `florio-montaigne-essays` | Montaigne | Essayes (3 books), 6 vols | John Florio | 1603 | have-raw | IA `essayestranslate01montuoft` … IA `essayestranslate06montuoft` (6 vols) |
| `florio-decameron` | Boccaccio | The Decameron (first complete English, 1620) | attributed to John Florio (published anonymously, 1620) | 1620 | have | PG 52617 + PG 52618 |
| `florio-montaigne-1603-folio` | — | The 1603 first edition (IA MontaigneImages / McGill 1632 folio): only images or long-s OCR; the 1906 reprint is used. | — | — | pending | — |
| `florio-montaigne-everyman` | — | Everyman (1910) or Temple Classics (1897) Florio sets: alternate witnesses if the Gibbings OCR proves weak. | — | — | pending | — |
| — | — | pg-56200: Queen Anna's New World of Words: Florio's dictionary, not a translation (could join a lexicon shelf, Adam's call). | — | — | excluded | — |
| — | — | pg-3600-cotton: PG's Montaigne Essays is Charles Cotton's translation, not Florio. | — | — | excluded | — |

## Burton (Arabian Nights, Camoens)

Shelf: `pipeline/burton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py burton` · titles `python3 pipeline/split_shelf_titles.py burton`.
Added at the coordinator's relay, vetoable. Catullus, Kama Sutra and Pentamerone are listed but not fetched: your call on content. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `burton-arabian-nights` | The Thousand and One Nights (Arabic) | The Book of the Thousand Nights and a Night, 10 vols | Richard Francis Burton | 1885 | have | PG 51252 … PG 58360 (10 vols) |
| `burton-supplemental-nights` | The Thousand and One Nights (Arabic) | Supplemental Nights, 6 vols (vol. 3 in two PG parts) | Richard Francis Burton | 1886-88 | have | PG 59156 … PG 64384 (7 vols) |
| `burton-lusiads` | Camoens | Os Lusiadas | Richard Francis Burton | 1880 | have | PG 77660 + PG 77661 |
| `burton-camoens-lyricks` | Camoens | The Lyricks: sonnets, canzons, odes and sextines | Richard Francis Burton | 1884 | have-raw | IA `cu31924102142985` |
| `burton-catullus` | — | The Carmina of Catullus (1894, with Leonard Smithers; PG 20732): PD; held back for Adam's call on content, not rights. | — | — | pending | — |
| `burton-kama-sutra` | — | Kama Sutra (1883, with Arbuthnot and Bhide; PG 27827): PD; Adam's call on content. | — | — | pending | — |
| `burton-pentamerone` | — | Basile, Il Pentamerone (1893): the IA copy found is a 1927 reprint (ilpentameroneort0000basi); PD as a pre-1931 printing - listed, not fetched, for the same content call. | — | — | pending | — |
| `burton-vikram` | — | Vikram and the Vampire (PG 2400/48511): Burton's free adaptation of the Baital Pachisi, not a translation; PG names no translator. | — | — | pending | — |
| — | — | pg-3435..3450: Older PG transcriptions of the same Nights and Supplemental Nights; the DP proofread editions (51252..64384) are used. | — | — | excluded | — |
| — | — | pg-6036: The Kasidah: Burton's own poem presented as a translation (a literary mask). | — | — | excluded | — |
| — | — | travel-books: Pilgrimage to Al-Madinah, Lake Regions, etc.: his own prose, not translations (an author section would hold them). | — | — | excluded | — |

## Maude (Tolstoy, PD editions only)

Shelf: `pipeline/maude_shelf.json` · fetch `python3 pipeline/fetch_shelf.py maude` · titles `python3 pipeline/split_shelf_titles.py maude`.
Added at the coordinator's relay, vetoable. Only printings before 1931; where the file gives no year, the title rests on Gutenberg's US clearance, which the Tr. column says. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `maude-war-and-peace` | Tolstoy | War and Peace | Aylmer and Louise Maude | pre-1931 printing per Project Gutenberg's US copyright clearance; the file states no edition year | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `tolstoy-warpeace` (PG 2600) |
| `maude-resurrection` | Tolstoy | Resurrection | Louise Maude | 1900 (Dodd, Mead, 'by my authority' note signed by Tolstoy); exact year not printed in the file | have | PG 1938 |
| `maude-father-sergius` | Tolstoy | Father Sergius | Aylmer and Louise Maude | pre-1931 printing per Project Gutenberg's US copyright clearance; the file states no edition year | have | PG 985 |
| `maude-master-and-man` | Tolstoy | Master and Man | Aylmer and Louise Maude | pre-1931 printing per Project Gutenberg's US copyright clearance; the file states no edition year | have | PG 986 |
| `maude-cossacks` | Tolstoy | The Cossacks | Aylmer and Louise Maude | pre-1931 printing per Project Gutenberg's US copyright clearance; the file states no edition year | have | PG 4761 |
| `maude-what-men-live-by` | Tolstoy | What Men Live By, and Other Tales | Aylmer and Louise Maude | pre-1931 printing per Project Gutenberg's US copyright clearance; the file states no edition year | have | PG 6157 |
| `maude-plays` | Tolstoy | Plays, Complete Edition including the Posthumous Plays (6 plays) | Louise and Aylmer Maude | 1914 ed. | have | PG 26661 … PG 26666 (6 vols) |
| `maude-what-is-art` | Tolstoy | What Is Art? | Aylmer Maude | 1904 (Funk & Wagnalls, stated) | have | PG 64908 |
| `maude-the-devil` | Tolstoy | The Devil | Aylmer Maude | 1926 ('First published in 1926', stated) | have | PG 67224 |
| `maude-three-days` | Tolstoy | Three Days in the Village, and Other Sketches | Aylmer and Louise Maude | 1910 (Free Age Press, stated) | have | PG 51018 |
| `maude-anna-karenina` | — | Anna Karenina, tr. L. & A. Maude (World's Classics 1918): not on PG under their names; look for a pre-1931 scan. | — | — | pending | — |
| `maude-centenary` | — | The Centenary Edition (OUP 1928-37, 21 vols): only the volumes printed before 1931 qualify; per-volume dating needed. | — | — | pending | — |
| — | — | pg-28920: War and Peace Book 1 only: part of PG 2600. | — | — | excluded | — |
| — | — | pg-52242, pg-78278: Aylmer Maude's own books (Life of Tolstoy, Life of Marie Stopes): not translations. | — | — | excluded | — |
| — | — | pg-79027: Tolstoy on Art: Maude as editor/compiler; overlaps What Is Art?. | — | — | excluded | — |
| — | — | other-maudes: PG items by Alice Maude Kellogg, Maude Alma, F. N. Maude, Maude Wholohan: different people. | — | — | excluded | — |
| — | — | pg-26472: Newer transcription of What Men Live By: its .txt returns 404 on Gutenberg's cache (2026-10-02); PG 6157 used. | — | — | excluded | — |
| — | — | pg-26660: Plays: Complete Edition, front matter only (the transcriber's note says the plays are posted separately as 26661-26666, which are used). | — | — | excluded | — |

## Cotton (Montaigne)

Shelf: `pipeline/cotton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cotton` · titles `python3 pipeline/split_shelf_titles.py cotton`.
Added by lane C under the coordinator's keep-going relay, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cotton-montaigne-essays` | Montaigne | Essays, 3 books (with Hazlitt's notes and the Letters) | Charles Cotton (rev. W. C. Hazlitt) | 1685-86; Hazlitt revision 1877 | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `montaigne-essays` (PG 3600) |
| `cotton-scarron-lucian` | — | Cotton's Scarronides (burlesque Virgil): non-Dryden Virgil belongs to lane B; listed only. | — | — | pending | — |
| — | — | pg-3581..3599: The same Cotton/Hazlitt text in 19 parts; PG 3600 complete used. | — | — | excluded | — |

## Ormsby (Don Quixote)

Shelf: `pipeline/ormsby_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ormsby` · titles `python3 pipeline/split_shelf_titles.py ormsby`.
Added by lane C, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ormsby-don-quixote` | Cervantes | Don Quixote, Parts I-II | John Ormsby | 1885 | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `cervantes-quixote` (PG 996) |
| — | — | pg-5903..5946, pg-28842: Doré-illustrated or partial Gutenberg copies of the same Ormsby text. | — | — | excluded | — |

## Urquhart & Motteux (Rabelais; Motteux's Quixote)

Shelf: `pipeline/urquhart-motteux_shelf.json` · fetch `python3 pipeline/fetch_shelf.py urquhart-motteux` · titles `python3 pipeline/split_shelf_titles.py urquhart-motteux`.
Added by lane C, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `urquhart-motteux-rabelais` | Rabelais | Gargantua and Pantagruel, Books I-V | Thomas Urquhart (Books I-III), Peter Anthony Motteux (IV-V) | 1653-1694 | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `rabelais-gargantua` (PG 1200) |
| `motteux-don-quixote` | Cervantes | The History of Don Quixote | Peter Anthony Motteux | 1700-03 | have | PG 35993 |
| — | — | pg-8166..8170: Doré-illustrated Rabelais, same text in parts. | — | — | excluded | — |

## FitzGerald (Omar, Jami, Calderón)

Shelf: `pipeline/fitzgerald_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fitzgerald` · titles `python3 pipeline/split_shelf_titles.py fitzgerald`.
Added by lane C, vetoable. His Greek plays stay with lane B. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fitzgerald-rubaiyat-salaman` | Omar Khayyam; Jami | Rubáiyát (the editions as printed in this volume) and Salámán and Absál | Edward FitzGerald | 1859-79 / 1856 | have | PG 22535 |
| `fitzgerald-calderon` | Calderon | Eight Dramas of Calderon, freely translated | Edward FitzGerald | 1853/1865 | have | PG 63776 |
| `fitzgerald-agamemnon` | — | FitzGerald's Agamemnon (1865) and Oedipus plays: Greek tragedy is lane B's queued item; cross-ref only. | — | — | pending | — |
| `fitzgerald-bird-parliament` | — | Attar's Bird Parliament (in his Letters and Literary Remains, 1889): needs a scan. | — | — | pending | — |
| — | — | pg-246, pg-35260: Single Rubaiyat editions, contained in PG 22535. | — | — | excluded | — |
| — | — | pg-2587: Life Is a Dream (PG header: tr. FitzGerald): his version is 'Such Stuff as Dreams Are Made Of', which is printed inside PG 63776. Not fetched as a likely duplicate; not compared line by line. | — | — | excluded | — |
| — | — | pg-10315: Persian Literature anthology: mixed translators. | — | — | excluded | — |

## Bayard Taylor (Faust)

Shelf: `pipeline/taylor_shelf.json` · fetch `python3 pipeline/fetch_shelf.py taylor` · titles `python3 pipeline/split_shelf_titles.py taylor`.
Added by lane C, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `taylor-faust-part-1` | Goethe | Faust, Part I | Bayard Taylor | 1870 | held elsewhere (cross-ref) | `pipeline/fetch_sources.py` → `faust` (PG 14591) |
| `taylor-faust-part-2` | Goethe | Faust, Part II | Bayard Taylor | 1871 | have-raw | IA `goethetaylorfaust02` |
| — | — | original-works: Taylor's own travel books, novels and poems: not translations. | — | — | excluded | — |

## E. W. Lane (Thousand and One Nights)

Shelf: `pipeline/lane_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lane` · titles `python3 pipeline/split_shelf_titles.py lane`.
Added by lane C, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lane-arabian-nights` | The Thousand and One Nights (Arabic) | The Thousand and One Nights, 3 vols | Edward William Lane | 1838-40 (1859 ed.) | have-raw | PG 34206 + IA `thousandonenight02harvuoft` + IA `thousandonenight03laneuoft` |
| `lane-selections-kuran` | — | Selections from the Kur-an (PG 44515): Lane as translator of Quranic passages; Adam's call whether scripture of other faiths belongs on a translator shelf. | — | — | pending | — |
| — | — | pg-41110: Arabian Society in the Middle Ages: Lane's notes, not a translation. | — | — | excluded | — |
| — | — | pg-70796: Modern Egyptians: Lane's own book. | — | — | excluded | — |
| — | — | ia-emory-1883: Chatto 1883 set (emory.edu): its text files are not at the standard path. | — | — | excluded | — |

## Lady Charlotte Guest (Mabinogion)

Shelf: `pipeline/guest_shelf.json` · fetch `python3 pipeline/fetch_shelf.py guest` · titles `python3 pipeline/split_shelf_titles.py guest`.
Added by lane C, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `guest-mabinogion` | Welsh tales (Red Book of Hergest) | The Mabinogion | Lady Charlotte Guest | 1838-49 | have | PG 5160 |
| — | — | pg-19959, 19973, 19976: O. M. Edwards's 3-vol reprint of the same Guest text; PG 5160 used. | — | — | excluded | — |
| — | — | pg-15551, pg-67425: Retellings (Clay; Lanier's Boy's Mabinogion), not translations. | — | — | excluded | — |

## Rossetti (Vita Nuova, Early Italian Poets)

Shelf: `pipeline/rossetti_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rossetti` · titles `python3 pipeline/split_shelf_titles.py rossetti`.
Round 4, lane C's choice under the coordinator's standing instruction; vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rossetti-vita-nuova` | Dante | La Vita Nuova (The New Life) | Dante Gabriel Rossetti | 1861 | have | PG 41085 |
| `rossetti-early-italian-poets` | Ciullo d'Alcamo, Guido Guinizelli, Guido Cavalcanti, Cino da Pistoia, Dante and others | The Early Italian Poets (Part I: poets before Dante; Part II: Dante and his circle, incl. the Vita Nuova) | Dante Gabriel Rossetti | 1861 | have-raw | IA `earlyitalianpo00rossuoft` |
| `rossetti-dante-and-his-circle-1874` | — | The 1874 rearranged edition (Ellis & White): a second witness of the same translations; not fetched. | — | — | pending | — |
| — | — | original-poems: Rossetti's own poems (House of Life etc.): not translations. | — | — | excluded | — |

## Fairfax (Tasso)

Shelf: `pipeline/fairfax_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fairfax` · titles `python3 pipeline/split_shelf_titles.py fairfax`.
Round 4, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fairfax-jerusalem-delivered` | Tasso | Jerusalem Delivered (Gerusalemme Liberata), 20 books | Edward Fairfax | 1600 | have | PG 392 |

## W. S. Rose (Ariosto)

Shelf: `pipeline/rose_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rose` · titles `python3 pipeline/split_shelf_titles.py rose`.
Round 4, vetoable. Gutenberg text placed by hand (its cache URL 404s); the URL is in the shelf's `_manual_fetch`. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rose-orlando-furioso` | Ariosto | Orlando Furioso, 46 cantos | William Stewart Rose | 1831 | have | PG 615 |

## Shelton (Don Quixote)

Shelf: `pipeline/shelton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py shelton` · titles `python3 pipeline/split_shelf_titles.py shelton`.
Round 4, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `shelton-don-quixote` | Cervantes | Don Quixote, Parts I-II | Thomas Shelton | 1612-1620 | have-raw | IA `historyofvalorou00cerv` + IA `historyofvalorou02cerviala` + IA `historyofvalorou03cerviala` |
| `shelton-1612-1620-originals` | — | The 1612 and 1620 first editions are on IA (cervantessheltondonquixote01/02): early-modern OCR; not fetched. | — | — | pending | — |

## C. E. Norton (Dante, prose)

Shelf: `pipeline/norton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py norton` · titles `python3 pipeline/split_shelf_titles.py norton`.
Round 4, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `norton-hell` | Dante | Inferno (Hell), prose | Charles Eliot Norton | 1891 | have-raw | IA `divinecomedyofda01dantiala` |
| `norton-purgatory` | Dante | Purgatorio, prose | Charles Eliot Norton | 1892 | have-raw | IA `divinecomedyofda02dantiala` |
| `norton-paradise` | Dante | Paradiso, prose | Charles Eliot Norton | 1892 | have-raw | IA `divinecomedyofda03dantiala` |
| `norton-new-life` | Dante | La Vita Nuova (The New Life) | Charles Eliot Norton | 1867 | have-raw | IA `newlifeofdanteal00dant_1` |

## John Payne (Villon, Decameron)

Shelf: `pipeline/payne_shelf.json` · fetch `python3 pipeline/fetch_shelf.py payne` · titles `python3 pipeline/split_shelf_titles.py payne`.
Round 4, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `payne-decameron` | Boccaccio | The Decameron | John Payne | 1886 | have | PG 23700 |
| `payne-villon` | Villon | Poems (Lesser and Greater Testament, Ballades) | John Payne | 1878 | have-raw | IA `poemsofmasterfra00villiala` |
| `payne-thousand-nights` | — | Payne's Book of the Thousand Nights and One Night (Villon Society 1882-84, 9 vols): Burton's and Lane's are already shelved; the IA set is incomplete and not fetched. Your call. | — | — | pending | — |
| `payne-bandello` | — | Novels of Matteo Bandello (1890, 6 vols): on IA; not fetched this run. | — | — | pending | — |

## Carlyle as translator (Goethe, German tales)

Shelf: `pipeline/carlyle_shelf.json` · fetch `python3 pipeline/fetch_shelf.py carlyle` · titles `python3 pipeline/split_shelf_titles.py carlyle`.
Round 4, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `carlyle-wilhelm-meister` | Goethe | Wilhelm Meister's Apprenticeship and Travels | Thomas Carlyle | 1824-1827 | have | PG 36483 + PG 78139 |
| `carlyle-german-tales` | Musaeus, Tieck, Richter | German Romance tales | Thomas Carlyle | 1827 | have | PG 38779 |
| — | — | carlyle-own-works: Sartor Resartus, The French Revolution etc.: Carlyle's own works, not translations. | — | — | excluded | — |

## Jeremiah Curtin (Sienkiewicz)

Shelf: `pipeline/curtin_shelf.json` · fetch `python3 pipeline/fetch_shelf.py curtin` · titles `python3 pipeline/split_shelf_titles.py curtin`.
Round 5, lane C's choice; vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `curtin-quo-vadis` | Sienkiewicz | Quo Vadis | Jeremiah Curtin | 1896 | have | PG 2853 |
| `curtin-with-fire-and-sword` | Sienkiewicz | With Fire and Sword (Trilogy I) | Jeremiah Curtin | 1890 | have | PG 37027 |
| `curtin-the-deluge` | Sienkiewicz | The Deluge (Trilogy II) | Jeremiah Curtin | 1891 | have | PG 37198 + PG 37308 |
| `curtin-pan-michael` | Sienkiewicz | Pan Michael (Trilogy III) | Jeremiah Curtin | 1893 | have | PG 37361 |
| `curtin-on-the-field-of-glory` | Sienkiewicz | On the Field of Glory | Jeremiah Curtin | 1906 | have | PG 37406 |
| `curtin-knights-of-the-cross` | — | The Knights of the Cross (1900): Gutenberg's edition is not Curtin's; no Curtin scan checked this run. | — | — | pending | — |
| `curtin-myths` | — | Curtin's own collections of Irish, Russian and Native American myths: his own fieldwork rather than translations of a work; left out. | — | — | pending | — |

## Isabel Hapgood (Hugo, Gorky, Turgenev, Bunin)

Shelf: `pipeline/hapgood_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hapgood` · titles `python3 pipeline/split_shelf_titles.py hapgood`.
Round 5, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hapgood-les-miserables` | Hugo | Les Misérables | Isabel F. Hapgood | 1887 | have | PG 135 |
| `hapgood-gorky-orloff` | Gorky | Orlóff and His Wife: Tales of the Barefoot Brigade | Isabel F. Hapgood | 1901 | have | PG 55636 |
| `hapgood-bunin-village` | Bunin | The Village | Isabel F. Hapgood | 1923 | have | PG 59981 |
| `hapgood-turgenev-first-love` | Turgenev | First Love, and Other Stories | Isabel F. Hapgood | 1904 | have | PG 56878 |
| `hapgood-turgenev-superfluous-man` | Turgenev | The Diary of a Superfluous Man, and Other Stories | Isabel F. Hapgood | 1904 | have | PG 41201 |
| `hapgood-turgenev-reckless-character` | Turgenev | A Reckless Character, and Other Stories | Isabel F. Hapgood | 1904 | have | PG 15994 |
| `hapgood-turgenev-nobleman` | Turgenev | A Nobleman's Nest | Isabel F. Hapgood | 1903 | have | PG 25771 |
| `hapgood-tolstoy` | — | Hapgood's Tolstoy (Childhood, Boyhood, Youth 1886; Sevastopol 1888): not on Gutenberg in her version; IA not checked this run. | — | — | pending | — |

## James Legge (Chinese classics)

Shelf: `pipeline/legge_shelf.json` · fetch `python3 pipeline/fetch_shelf.py legge` · titles `python3 pipeline/split_shelf_titles.py legge`.
Round 5, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `legge-tao-teh-king` | Laozi | Tao Te Ching | James Legge | 1891 | have | PG 216 |
| `legge-analects` | Confucius | Analects | James Legge | 1861 | have | PG 3330 |
| `legge-faxian` | Faxian | A Record of Buddhistic Kingdoms | James Legge | 1886 | have | PG 2124 |
| `legge-sacred-books` | — | The rest of Legge's Sacred Books of the East (Shu King, Shih King, Yi King, Li Ki, Zhuangzi: SBE 3, 16, 27-28, 39-40): on IA, not fetched this run. | — | — | pending | — |
| — | — | pg-3100-4094: Gutenberg 3100 and 4094 are the Chinese-language text of the Chinese Classics, not the translation. | — | — | excluded | — |

## H. A. and Lionel Giles (Chinese)

Shelf: `pipeline/giles_shelf.json` · fetch `python3 pipeline/fetch_shelf.py giles` · titles `python3 pipeline/split_shelf_titles.py giles`.
Round 5, vetoable. Lionel Giles is US PD only (UK until end-2028). Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `giles-chuang-tzu` | Zhuangzi | Chuang Tzu | Herbert A. Giles | 1889 | have | PG 59709 |
| `giles-strange-stories` | Pu Songling | Strange Stories from a Chinese Studio | Herbert A. Giles | 1880 | have | PG 43629 |
| `giles-art-of-war` | Sunzi | The Art of War | Lionel Giles | 1910 | have | PG 132 |
| `giles-sayings-of-confucius` | Confucius | The Sayings of Confucius | Lionel Giles | 1907 | have | PG 46389 |
| — | — | giles-own-works: H. A. Giles's History of Chinese Literature and China and the Chinese: his own works. | — | — | excluded | — |

## Arthur Waley (pre-1931 only)

Shelf: `pipeline/waley_shelf.json` · fetch `python3 pipeline/fetch_shelf.py waley` · titles `python3 pipeline/split_shelf_titles.py waley`.
Round 5, vetoable. 🔴 US PD only: UK copyright runs to the end of 2036. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `waley-170-chinese-poems` | Chinese poets | A Hundred and Seventy Chinese Poems | Arthur Waley | 1918 | have | PG 42290 |
| `waley-more-translations` | Chinese poets | More Translations from the Chinese | Arthur Waley | 1919 | have | PG 16500 |
| `waley-li-po` | Li Bai | The Poet Li Po | Arthur Waley | 1919 | have | PG 43274 |
| `waley-no-plays` | Zeami and others | The No Plays of Japan | Arthur Waley | 1921 | have | PG 43304 |
| `waley-genji-1-3` | Murasaki Shikibu | The Tale of Genji, parts 1-3 (The Tale of Genji; The Sacred Tree; A Wreath of Cloud) | Arthur Waley | 1925-1927 | have | PG 66057 + PG 67111 + PG 75852 |
| `waley-pillow-book` | Sei Shonagon | The Pillow-Book of Sei Shonagon | Arthur Waley | 1928 | have | PG 76016 |
| `waley-genji-4-6` | — | Genji parts 4-6 (Blue Trousers 1928, The Lady of the Boat 1932, The Bridge of Dreams 1933): part 4 is US PD but not on Gutenberg; parts 5-6 are after 1930 and are refused. | — | — | pending | — |
| — | — | waley-after-1930: The Way and its Power (1934), the Analects (1938), Monkey (1942): still in copyright. | — | — | excluded | — |

## John Hoole (Tasso)

Shelf: `pipeline/hoole_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hoole` · titles `python3 pipeline/split_shelf_titles.py hoole`.
Round 5, vetoable. 1803 printing still uses the long s (OCR reads s as f). Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hoole-jerusalem-delivered` | Tasso | Jerusalem Delivered, 20 books | John Hoole | 1763 | have-raw | IA `jerusalemdeliver01tassiala` + IA `jerusalemdeliver02tassiala` |
| `hoole-orlando-furioso` | — | Hoole's Ariosto (1783): only 18th-century long-s printings and incomplete Google sets of the 1807 edition found. Not fetched. | — | — | pending | — |

## Sir John Harington (Ariosto, 1591)

Shelf: `pipeline/harington_shelf.json` · fetch `python3 pipeline/fetch_shelf.py harington` · titles `python3 pipeline/split_shelf_titles.py harington`.
Round 5, vetoable. Early-modern OCR, 66% of tokens in a modern vocabulary: a defect. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `harington-orlando-furioso` | Ariosto | Orlando Furioso, 46 books | Sir John Harington | 1591 | have-raw | IA `orlandofuriosoin00ario_0` |
