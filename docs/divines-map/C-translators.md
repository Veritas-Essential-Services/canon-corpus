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

## F. Max Müller (Upanishads, Dhammapada)

Shelf: `pipeline/muller_shelf.json` · fetch `python3 pipeline/fetch_shelf.py muller` · titles `python3 pipeline/split_shelf_titles.py muller`.
Round 6, lane C's choice; vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `muller-upanishads` | Upanishads | The Upanishads (twelve principal Upanishads) | F. Max Müller | 1879-1884 | have-raw | IA `upanishads01mluoft` + IA `p2upanishads00mluoft` |
| `muller-dhammapada` | Dhammapada | Dhammapada | F. Max Müller | 1881 | have | PG 2017 |
| `muller-rig-veda-1869` | — | Müller's Rig-Veda-Sanhita vol. 1 (hymns to the Maruts, 1869): only that volume was ever published; not fetched. | — | — | pending | — |

## Sir Edwin Arnold (Bhagavad Gita)

Shelf: `pipeline/edwin-arnold_shelf.json` · fetch `python3 pipeline/fetch_shelf.py edwin-arnold` · titles `python3 pipeline/split_shelf_titles.py edwin-arnold`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `edwin-arnold-bhagavad-gita` | Bhagavad Gita | The Song Celestial (Bhagavad Gita) | Sir Edwin Arnold | 1885 | have | PG 2388 |
| `edwin-arnold-indian-idylls` | — | Indian Idylls (1883, episodes of the Mahabharata): not on Gutenberg; IA not checked this run. | — | — | pending | — |
| — | — | light-of-asia: The Light of Asia (1879): Arnold's own poem. | — | — | excluded | — |

## R. T. H. Griffith (Ramayana, Rigveda)

Shelf: `pipeline/griffith_shelf.json` · fetch `python3 pipeline/fetch_shelf.py griffith` · titles `python3 pipeline/split_shelf_titles.py griffith`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `griffith-ramayana` | Valmiki | The Ramayana | Ralph T. H. Griffith | 1870 | have | PG 24869 |
| `griffith-rigveda` | Rigveda | The Hymns of the Rigveda, 10 mandalas | Ralph T. H. Griffith | 1889 | have-raw | IA `in.ernet.dli.2015.195721` + IA `in.ernet.dli.2015.195722` |
| `griffith-atharvaveda` | — | Hymns of the Atharva-veda (1895-96), the Samaveda (1893), the White Yajurveda (1899): on IA; not fetched this run. | — | — | pending | — |

## J. M. Rodwell (Koran)

Shelf: `pipeline/rodwell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rodwell` · titles `python3 pipeline/split_shelf_titles.py rodwell`.
Round 6, vetoable. Suras in his chronological order. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rodwell-koran` | The Qur'an | The Koran | J. M. Rodwell | 1861 | have | PG 2800 |
| — | — | pg-3434: Gutenberg 3434 is the same Rodwell translation (an older file); not fetched twice. | — | — | excluded | — |

## George Sale (Koran)

Shelf: `pipeline/sale_shelf.json` · fetch `python3 pipeline/fetch_shelf.py sale` · titles `python3 pipeline/split_shelf_titles.py sale`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `sale-koran` | The Qur'an | The Koran | George Sale | 1734 | have | PG 7440 |
| `sale-preliminary-discourse` | — | Sale's Preliminary Discourse (his long introduction): check whether PG 7440 carries it; if not, a scan of an 1825+ edition. | — | — | pending | — |

## E. H. Palmer (Qur'an)

Shelf: `pipeline/palmer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py palmer` · titles `python3 pipeline/split_shelf_titles.py palmer`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `palmer-quran` | The Qur'an | The Qur'an | E. H. Palmer | 1880 | have-raw | IA `1922707.0006.001.umich.edu` + IA `thequraan09unknuoft` |
| — | — | qurn01unkngoog: Google copy of part II, a duplicate of the Toronto copy (both hold chapters XVII-CXIV; found in the second review round 2026-10-03). Toronto kept for its better OCR. | — | — | excluded | — |

## E. H. Whinfield (Rumi's Masnavi)

Shelf: `pipeline/whinfield_shelf.json` · fetch `python3 pipeline/fetch_shelf.py whinfield` · titles `python3 pipeline/split_shelf_titles.py whinfield`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `whinfield-masnavi` | Rumi | Masnavi (abridged) | E. H. Whinfield | 1887 | have-raw | IA `cu31924026910251` |
| `whinfield-omar` | — | Whinfield's Omar Khayyam quatrains are inside Gutenberg 38511, a 1903 compilation with FitzGerald's and Nicolas's versions; it would need cutting by marker. Not fetched. | — | — | pending | — |

## R. A. Nicholson (Rumi, Hujwiri)

Shelf: `pipeline/nicholson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py nicholson` · titles `python3 pipeline/split_shelf_titles.py nicholson`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `nicholson-kashf-al-mahjub` | Hujwiri | Kashf al-Mahjub | Reynold A. Nicholson | 1911 | have | PG 64786 |
| `nicholson-divani-shamsi-tabriz` | Rumi | Selected Poems from the Divani Shamsi Tabriz | Reynold A. Nicholson | 1898 | have-raw | IA `india.history.resource.111025` |
| `nicholson-mathnawi` | — | The Mathnawi translation (Gibb series, 1925-40): vols 1-2 (1926, 1930) are US PD; the rest are not. Not fetched. | — | — | pending | — |

## Southey as translator (Amadis, the Cid)

Shelf: `pipeline/southey_shelf.json` · fetch `python3 pipeline/fetch_shelf.py southey` · titles `python3 pipeline/split_shelf_titles.py southey`.
Round 7, lane C's choice; vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `southey-chronicle-of-the-cid` | Chronicle of the Cid (Crónica del Cid and others) | Chronicle of the Cid | Robert Southey | 1808 | have | PG 8491 |
| `southey-amadis-of-gaul` | Lobeira / Montalvo | Amadis of Gaul, 4 vols | Robert Southey | 1803 | have-raw | IA `amadisofgaul01lobeuoft` + PG 51099 + PG 52941 + PG 55005 |
| — | — | southey-own-poems: Thalaba, Madoc, the Life of Nelson etc.: Southey's own works. | — | — | excluded | — |

## Coleridge as translator (Wallenstein)

Shelf: `pipeline/coleridge_shelf.json` · fetch `python3 pipeline/fetch_shelf.py coleridge` · titles `python3 pipeline/split_shelf_titles.py coleridge`.
Round 7, vetoable. Gutenberg text placed by hand (cache URL 404s), see `_manual_fetch`. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `coleridge-piccolomini` | Schiller | The Piccolomini (Wallenstein, part 2) | Samuel Taylor Coleridge | 1800 | have | PG 6786 |
| `coleridge-death-of-wallenstein` | Schiller | The Death of Wallenstein (Wallenstein, part 3) | Samuel Taylor Coleridge | 1800 | have | PG 6787 |
| — | — | wallensteins-lager: Wallenstein's Camp (part 1) was not translated by Coleridge. | — | — | excluded | — |

## John and E. A. Bowring (Chamisso, Goethe, Heine)

Shelf: `pipeline/bowring_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bowring` · titles `python3 pipeline/split_shelf_titles.py bowring`.
Round 7, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bowring-peter-schlemihl` | Chamisso | Peter Schlemihl | John Bowring | 1824 | have | PG 21943 |
| `bowring-goethe-poems` | Goethe | Poems, in the original metres | Edgar Alfred Bowring | 1853 | have | PG 1287 |
| `bowring-heine-poems` | Heine | Poems, complete | Edgar Alfred Bowring | 1859 | have | PG 52882 |
| `john-bowring-anthologies` | — | Sir John Bowring's Specimens of the Russian Poets (1821-23), Servian Popular Poetry (1827), Poetry of the Magyars (1830): on IA; not fetched this run. | — | — | pending | — |

## John Anster (Faust I)

Shelf: `pipeline/anster_shelf.json` · fetch `python3 pipeline/fetch_shelf.py anster` · titles `python3 pipeline/split_shelf_titles.py anster`.
Round 7, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `anster-faust-part-1` | Goethe | Faust, Part I (verse) | John Anster | 1835 | have-raw | IA `firstpartgoethe00anstgoog` |
| `anster-faust-part-2` | — | Anster's Part II (1864): not fetched this run. | — | — | pending | — |
| — | — | fausttransanster00goetuoft: IA catalogues it as Anster's (Harper 1886), but its title page reads 'translated into English verse ... by John Stuart Blackie', Macmillan 1880: a different translation. Refused by the identity gate 2026-10-03. | — | — | excluded | — |

## Abraham Hayward (Faust I, prose)

Shelf: `pipeline/hayward_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hayward` · titles `python3 pipeline/split_shelf_titles.py hayward`.
Round 7, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hayward-faust-part-1` | Goethe | Faust, Part I (prose) | Abraham Hayward | 1833 | have-raw | IA `faustdramatichay00goetuoft` |

## P. H. Wicksteed (Paradiso, Convivio)

Shelf: `pipeline/wicksteed_shelf.json` · fetch `python3 pipeline/fetch_shelf.py wicksteed` · titles `python3 pipeline/split_shelf_titles.py wicksteed`.
Round 7, vetoable. Paradiso has the Italian facing: OCR mixes both. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `wicksteed-paradiso` | Dante | Paradiso (prose, Italian facing) | Philip H. Wicksteed | 1899 | have-raw | IA `paradisoofdantea00dantuoft` |
| `wicksteed-convivio` | Dante | Convivio | Philip H. Wicksteed | 1903 | have-raw | IA `convivioofdantea00dant` |
| `wicksteed-latin-works` | — | The Latin Works of Dante (Temple Classics 1904): Wicksteed did the letters and eclogues, A. G. Ferrers Howell the rest; translator per piece needed. Not fetched. | — | — | pending | — |
| — | — | six-sermons: Dante: Six Sermons (PG 36479): Wicksteed's own work. | — | — | excluded | — |

## J. C. Mangan (German Anthology)

Shelf: `pipeline/mangan_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mangan` · titles `python3 pipeline/split_shelf_titles.py mangan`.
Round 7, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mangan-german-anthology` | Goethe, Schiller, Uhland, Rückert and others | Anthologia Germanica (German Anthology) | James Clarence Mangan | 1845 | have-raw | IA `anthologiagerma02manggoog` + IA `anthologiagerma03manggoog` |
| `mangan-irish` | — | Mangan's translations from the Irish (The Poets and Poetry of Munster, 1849): not fetched. | — | — | pending | — |

## J. A. Symonds as translator (Cellini, sonnets, goliards)

Shelf: `pipeline/symonds_shelf.json` · fetch `python3 pipeline/fetch_shelf.py symonds` · titles `python3 pipeline/split_shelf_titles.py symonds`.
Round 8, lane C's choice; vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `symonds-cellini-autobiography` | Cellini | The Autobiography of Benvenuto Cellini | John Addington Symonds | 1888 | have | PG 4028 |
| `symonds-michelangelo-campanella-sonnets` | Michelangelo, Campanella | Sonnets, in rhymed English | John Addington Symonds | 1878 | have | PG 10314 |
| `symonds-wine-women-and-song` | Carmina Burana and other goliard poets | Wine, Women, and Song (medieval Latin students' songs) | John Addington Symonds | 1884 | have | PG 18044 |
| — | — | symonds-own-works: Renaissance in Italy, the Life of Michelangelo (PG 11242) etc.: Symonds's own works. | — | — | excluded | — |

## J. S. Blackie (Faust; Aeschylus cross-referenced)

Shelf: `pipeline/blackie_shelf.json` · fetch `python3 pipeline/fetch_shelf.py blackie` · titles `python3 pipeline/split_shelf_titles.py blackie`.
Round 8, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `blackie-faust-part-1` | Goethe | Faust, Part I (verse) | John Stuart Blackie | 1834 | have | PG 63203 |
| `blackie-aeschylus` | Aeschylus | The Lyrical Dramas of Aeschylus | John Stuart Blackie | 1850 | held elsewhere (cross-ref) | `pipeline/aeschylus_shelf.json` → `aeschylus-blackie` (PG 59225) |

## Sir Theodore Martin (Wilhelm Tell)

Shelf: `pipeline/theodore-martin_shelf.json` · fetch `python3 pipeline/fetch_shelf.py theodore-martin` · titles `python3 pipeline/split_shelf_titles.py theodore-martin`.
Round 8, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `theodore-martin-wilhelm-tell` | Schiller | Wilhelm Tell | Sir Theodore Martin | 1847 | have | PG 6788 |
| `theodore-martin-others` | — | Martin's Faust (1865-86), Vita Nuova (1862), Catullus (1861) and Heine (1878): on IA, not fetched this run. His Horace overlaps lane B's horace shelf; check there first. | — | — | pending | — |
| — | — | book-of-ballads: The Book of Ballads (PG 44798, with Aytoun): parodies, not translations. | — | — | excluded | — |

## Lafcadio Hearn as translator (Gautier, Flaubert)

Shelf: `pipeline/hearn_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hearn` · titles `python3 pipeline/split_shelf_titles.py hearn`.
Round 8, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hearn-gautier-cleopatras-nights` | Gautier | One of Cleopatra's Nights and Other Fantastic Romances | Lafcadio Hearn | 1882 | have | PG 39397 |
| `hearn-flaubert-temptation` | Flaubert | The Temptation of St. Anthony | Lafcadio Hearn | 1910 | have | PG 52225 |
| — | — | pg-25053: Gutenberg 25053 is another Temptation of St. Antony with no translator named; not Hearn's. | — | — | excluded | — |
| — | — | hearn-own-works: Kwaidan, Glimpses of Unfamiliar Japan etc.: Hearn's own books. | — | — | excluded | — |

## C. K. Scott Moncrieff (Proust, Stendhal, Roland, Beowulf, Abelard)

Shelf: `pipeline/scott-moncrieff_shelf.json` · fetch `python3 pipeline/fetch_shelf.py scott-moncrieff` · titles `python3 pipeline/split_shelf_titles.py scott-moncrieff`.
Round 9 (2026-10-10), vetoable. Later Proust volumes and the Red and the Black wait for a pre-1931 scan. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `moncrieff-proust-swanns-way` | Proust | Swann's Way | C. K. Scott Moncrieff | 1922 | have | PG 7178 |
| `moncrieff-proust-within-a-budding-grove` | Proust | Within a Budding Grove | C. K. Scott Moncrieff | 1924 | have | PG 63532 |
| `moncrieff-proust-guermantes-way` | Proust | The Guermantes Way | C. K. Scott Moncrieff | 1925 | have | PG 73425 |
| `moncrieff-song-of-roland` | anonymous (Old French) | The Song of Roland | C. K. Scott Moncrieff | 1919 | have | PG 391 |
| `moncrieff-stendhal-charterhouse-of-parma` | Stendhal | The Charterhouse of Parma | C. K. Scott Moncrieff | 1925 | have | PG 66374 + PG 66375 |
| `moncrieff-beowulf` | anonymous (Old English) | Widsith, Beowulf, Finnsburgh, Waldere, Deor | C. K. Scott Moncrieff | 1921 | have-raw | IA `widsithbeowulff00scotuoft` |
| `moncrieff-stendhal-abbess-of-castro` | Stendhal | The Abbess of Castro and Other Tales | C. K. Scott Moncrieff | 1926 | have-raw | IA `abbessofcastro0000cksc` |
| `moncrieff-abelard-and-heloise` | Abelard and Heloise | The Letters of Abelard and Heloise | C. K. Scott Moncrieff | 1925 | have-raw | IA `lettersofabelard0000abel` |
| `moncrieff-stendhal-armance` | Stendhal | Armance | C. K. Scott Moncrieff | 1928 | have-raw | IA `armance0000sten` |
| `moncrieff-proust-cities-of-the-plain` | — | 1927/1929: US PD, but the only open scans (citiesofplain0000prou_b6a6, dli.ernet.16336) are Chatto reprints of 1960 and 1971. | — | — | pending | — |
| `moncrieff-proust-the-captive` | — | 1929: US PD, but captive00prourich is a Random House printing listing 1932 and 1947; dli.ernet.16281 is a 1957 Chatto reprint. | — | — | pending | — |
| `moncrieff-proust-sweet-cheat-gone` | — | 1930: US PD since 2026, but every open scan is a 1957+ Random House or 1970 Vintage printing (copyright-renewal lines). | — | — | pending | — |
| `moncrieff-pirandello-shoot` | — | 1926: shoot0000luig is the 1934 'Nobel Prize Edition'; shoot-luigi-pirandello is a Gutenberg-Australia text of unstated edition. | — | — | pending | — |
| `moncrieff-pirandello-old-and-young` | — | 1928: only volume 2 is open (oldyoung02pira); volume 1 not found. | — | — | pending | — |
| `moncrieff-lauzun` | — | Memoirs of the Duc de Lauzun (1928): translated jointly with Aldington and Rutherford; not checked. | — | — | pending | — |
| `moncrieff-stendhal-red-and-black` | — | 1926: US PD. redblack0000mari_e9r8, _h6c2 and _z4c1 are all Modern Library printings by Random House (1931 or later; e9r8's back list carries Modern Library Giant numbers). redblack0000unse_p8m8 is the 1926 first printing but volume one only; volume two not found open. | — | — | pending | — |
| — | — | moncrieff-past-recaptured: Time Regained / The Past Recaptured is Stephen Hudson's and Frederick Blossom's, not Scott Moncrieff's (he died in 1930). | — | — | excluded | — |

## Arthur W. Ryder (Kalidasa, Little Clay Cart, Panchatantra, Gita)

Shelf: `pipeline/ryder_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ryder` · titles `python3 pipeline/split_shelf_titles.py ryder`.
Round 10 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ryder-kalidasa-shakuntala-and-other-works` | Kalidasa | Translations of Shakuntala and Other Works | Arthur W. Ryder | 1912 | have | PG 16659 |
| `ryder-sudraka-little-clay-cart` | Sudraka | The Little Clay Cart | Arthur W. Ryder | 1905 | have | PG 21020 |
| `ryder-twenty-two-goblins` | Sivadasa (Vetalapanchavimsati) | Twenty-Two Goblins | Arthur W. Ryder | 1917 | have | PG 2290 |
| `ryder-panchatantra` | Panchatantra (anonymous) | The Panchatantra | Arthur W. Ryder | 1925 | have-raw | IA `panchatantra035159mbp` |
| `ryder-bhagavad-gita` | Bhagavad-gita | The Bhagavad-gita | Arthur W. Ryder | 1929 | have-raw | IA `bhagavadgita0000unse_g1d6` |
| `ryder-dandin-ten-princes` | — | 1927: US PD, but the only open scan (bwb_W7-BOY-629) is the third impression, 1960. | — | — | pending | — |
| — | — | ryder-golds-gloom: Gold's Gloom (1925) is a selection from his Panchatantra, already shelved whole. | — | — | excluded | — |
| — | — | pg-52309: A second Gutenberg Twenty-Two Goblins; 2290 is used. | — | — | excluded | — |

## Gertrude Bell (Hafiz)

Shelf: `pipeline/gertrude-bell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py gertrude-bell` · titles `python3 pipeline/split_shelf_titles.py gertrude-bell`.
Round 10 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bell-hafiz-divan` | Hafiz | Poems from the Divan of Hafiz | Gertrude Lowthian Bell | 1897 | have | PG 74883 |
| — | — | bell-own-works: The Desert and the Sown, her letters: her own books. | — | — | excluded | — |

## The Oscar Levy Nietzsche (Common, Zimmern, Ludovici and others)

Shelf: `pipeline/levy-nietzsche_shelf.json` · fetch `python3 pipeline/fetch_shelf.py levy-nietzsche` · titles `python3 pipeline/split_shelf_titles.py levy-nietzsche`.
Round 10 (2026-10-10), vetoable. Each title gates on its own translator. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `levy-nietzsche-zarathustra` | Nietzsche | Thus Spake Zarathustra | Thomas Common | 1909 | have | PG 1998 |
| `levy-nietzsche-beyond-good-and-evil` | Nietzsche | Beyond Good and Evil | Helen Zimmern | 1907 | have | PG 4363 |
| `levy-nietzsche-human-all-too-human-1` | Nietzsche | Human, All-Too-Human, Part I | Helen Zimmern | 1909 | have | PG 51935 |
| `levy-nietzsche-human-all-too-human-2` | Nietzsche | Human, All-Too-Human, Part II | Paul V. Cohn | 1911 | have | PG 37841 |
| `levy-nietzsche-dawn-of-day` | Nietzsche | The Dawn of Day | J. M. Kennedy | 1911 | have | PG 39955 |
| `levy-nietzsche-joyful-wisdom` | Nietzsche | The Joyful Wisdom | Thomas Common (poetry by Paul V. Cohn and Maude Dominica Petre) | 1910 | have | PG 52881 |
| `levy-nietzsche-genealogy-of-morals` | Nietzsche | The Genealogy of Morals | Horace B. Samuel (with J. M. Kennedy) | 1910 | have | PG 52319 |
| `levy-nietzsche-birth-of-tragedy` | Nietzsche | The Birth of Tragedy | Wm. A. Haussmann | 1909 | have | PG 51356 |
| `levy-nietzsche-thoughts-out-of-season-2` | Nietzsche | Thoughts Out of Season, Part II | Adrian Collins | 1909 | have | PG 38226 |
| `levy-nietzsche-early-greek-philosophy` | Nietzsche | Early Greek Philosophy and Other Essays | Maximilian A. Mügge | 1911 | have | PG 51548 |
| `levy-nietzsche-twilight-and-antichrist` | Nietzsche | The Twilight of the Idols; The Antichrist | Anthony M. Ludovici | 1911 | have | PG 52263 |
| `levy-nietzsche-ecce-homo` | Nietzsche | Ecce Homo | Anthony M. Ludovici (poetry by Paul V. Cohn) | 1911 | have | PG 52190 |
| `levy-nietzsche-case-of-wagner` | Nietzsche | The Case of Wagner, Nietzsche contra Wagner, Selected Aphorisms | Anthony M. Ludovici | 1911 | have | PG 25012 |
| `levy-nietzsche-will-to-power-1` | Nietzsche | The Will to Power, Books I and II | Anthony M. Ludovici | 1909 | have | PG 52914 |
| `levy-nietzsche-will-to-power-2` | Nietzsche | The Will to Power, Books III and IV | Anthony M. Ludovici | 1910 | have | PG 52915 |
| `levy-nietzsche-missing-volumes` | — | Levy vols not on Gutenberg in this pass: Thoughts Out of Season I (Ludovici), Miscellaneous Aphorisms (Human All-Too-Human II), the Future of our Educational Institutions (Kennedy), Poems, Letters, the Index. Look on archive.org next round. | — | — | pending | — |
| — | — | pg-52124: A second Gutenberg Joyful Wisdom from the same Levy volume; 52881 (Distributed Proofreaders) is used. | — | — | excluded | — |
| — | — | pg-19322: Mencken's own Antichrist translation (1918), not Levy's; its front matter carries 1923-1924 dates; a separate translator. | — | — | excluded | — |
| — | — | pg-38145: Alexander Harvey's 1908 Human, All Too Human selection, not Levy's. | — | — | excluded | — |
| — | — | pg-19634: Another Beyond Good and Evil with no translator in the header; not checked. | — | — | excluded | — |

## Arthur Ransome as translator (Gourmont; Old Peter's Russian Tales)

Shelf: `pipeline/ransome-translations_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ransome-translations` · titles `python3 pipeline/split_shelf_titles.py ransome-translations`.
2026-10-10, vetoable. His Swallows and Amazons is on Lane B's `ransome_shelf.json`, not here. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ransome-old-peters-russian-tales` | Russian folk tales, retold | Old Peter's Russian Tales | Arthur Ransome | 1916 | have | PG 16981 |
| `ransome-gourmont-night-in-the-luxembourg` | Remy de Gourmont | A Night in the Luxembourg | Arthur Ransome | 1912 | have | PG 46766 |
| — | — | ransome-own-books: Swallows and Amazons and the rest of the series: Ransome's own books, on Lane B's ransome_shelf.json. | — | — | excluded | — |
