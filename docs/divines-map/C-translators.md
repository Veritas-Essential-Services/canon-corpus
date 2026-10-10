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

## William Archer's Ibsen (Collected Works, 1906-12)

Shelf: `pipeline/archer-ibsen_shelf.json` · fetch `python3 pipeline/fetch_shelf.py archer-ibsen` · titles `python3 pipeline/split_shelf_titles.py archer-ibsen`.
Round 11 (2026-10-10), vetoable. One title per volume; vol. 12 pending. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `archer-ibsen-vol-01` | Ibsen | Collected Works, vol. 1: Lady Inger of Ostrat; The Feast at Solhoug; Love's Comedy | William Archer, editor; each play's translator as its title page prints (William, Charles and Frances E. Archer, Mary Morison, C. H. Herford, Edmund Gosse) | 1906 | have | PG 66060 |
| `archer-ibsen-vol-02` | Ibsen | Collected Works, vol. 2: The Vikings at Helgeland; The Pretenders | William Archer, editor; each play's translator as its title page prints (William, Charles and Frances E. Archer, Mary Morison, C. H. Herford, Edmund Gosse) | 1906 | have | PG 66186 |
| `archer-ibsen-vol-03` | Ibsen | Collected Works, vol. 3: Brand | William Archer, editor; each play's translator as its title page prints (William, Charles and Frances E. Archer, Mary Morison, C. H. Herford, Edmund Gosse) | 1906 | have | PG 66238 |
| `archer-ibsen-vol-04` | Ibsen | Collected Works, vol. 4: Peer Gynt | William Archer, editor; each play's translator as its title page prints (William, Charles and Frances E. Archer, Mary Morison, C. H. Herford, Edmund Gosse) | 1906 | have | PG 66239 |
| `archer-ibsen-vol-05` | Ibsen | Collected Works, vol. 5: Emperor and Galilean | William Archer, editor; each play's translator as its title page prints (William, Charles and Frances E. Archer, Mary Morison, C. H. Herford, Edmund Gosse) | 1906 | have | PG 66240 |
| `archer-ibsen-vol-06` | Ibsen | Collected Works, vol. 6: The League of Youth; Pillars of Society | William Archer, editor; each play's translator as its title page prints (William, Charles and Frances E. Archer, Mary Morison, C. H. Herford, Edmund Gosse) | 1907 | have-raw | IA `collectedworksof06ibseiala` |
| `archer-ibsen-vol-07` | Ibsen | Collected Works, vol. 7: A Doll's House; Ghosts | William Archer, editor; each play's translator as its title page prints (William, Charles and Frances E. Archer, Mary Morison, C. H. Herford, Edmund Gosse) | 1907 | have | PG 70566 |
| `archer-ibsen-vol-08` | Ibsen | Collected Works, vol. 8: An Enemy of the People; The Wild Duck | William Archer, editor; each play's translator as its title page prints (William, Charles and Frances E. Archer, Mary Morison, C. H. Herford, Edmund Gosse) | 1907 | have | PG 70577 |
| `archer-ibsen-vol-09` | Ibsen | Collected Works, vol. 9: Rosmersholm; The Lady from the Sea | William Archer, editor; each play's translator as its title page prints (William, Charles and Frances E. Archer, Mary Morison, C. H. Herford, Edmund Gosse) | 1907 | have-raw | IA `collectedworksof09ibseiala` |
| `archer-ibsen-vol-10` | Ibsen | Collected Works, vol. 10: Hedda Gabler; The Master Builder | William Archer, editor; each play's translator as its title page prints (William, Charles and Frances E. Archer, Mary Morison, C. H. Herford, Edmund Gosse) | 1907 | have-raw | IA `collectedworkso10ibseuoft` |
| `archer-ibsen-vol-11` | Ibsen | Collected Works, vol. 11: Little Eyolf; John Gabriel Borkman; When We Dead Awaken | William Archer, editor; each play's translator as its title page prints (William, Charles and Frances E. Archer, Mary Morison, C. H. Herford, Edmund Gosse) | 1907 | have | PG 74642 |
| `archer-ibsen-vol-12` | — | From Ibsen's Workshop (A. G. Chater, 1912): collectedworkso12ibseuoft returned HTTP 500 on every try today; retry next round. | — | — | pending | — |
| — | — | single-play-gutenberg-texts: PG 4093, 4070, 4782, 7942, 8121, 18428, 18792, 19018 are single plays from the same Archer edition; the volumes are used instead so nothing is held twice. | — | — | excluded | — |
| — | — | sharp-everyman: R. Farquharson Sharp's Everyman Ibsen (PG 2446, 2467): another translator; A Doll's House in his version is on adler_shelf.json. | — | — | excluded | — |
| — | — | marx-aveling-wild-duck: PG 73631: Eleanor Marx Aveling's translation; another translator. | — | — | excluded | — |

## Magnússon and Morris (Icelandic sagas)

Shelf: `pipeline/morris-magnusson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py morris-magnusson` · titles `python3 pipeline/split_shelf_titles.py morris-magnusson`.
Rounds 12-13 (2026-10-10), vetoable. Includes the six-volume Saga Library. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mm-volsunga-saga` | anonymous (Old Norse) | The Story of the Volsungs (Volsunga Saga), with excerpts from the Poetic Edda | Eiríkr Magnússon and William Morris | 1870 | held elsewhere (cross-ref) | `pipeline/poetic-edda_shelf.json` → `edda-volsunga-morris` (PG 1152) |
| `mm-grettir-the-strong` | anonymous (Old Norse) | The Story of Grettir the Strong | Eiríkr Magnússon and William Morris | 1869 | have | PG 12747 |
| `mm-frithiof-the-bold` | anonymous (Old Norse) | The Story of Frithiof the Bold | Eiríkr Magnússon and William Morris | 1875 | have | PG 24420 |
| `mm-saga-library-vol-1` | anonymous (Old Norse) | The Saga Library, vol. 1: The Story of Howard the Halt; The Banded Men; Hen Thorir | William Morris and Eiríkr Magnússon | 1891 | have-raw | IA `sagalibrarydonei01snoriala` |
| `mm-saga-library-vol-2` | anonymous (Old Norse) | The Saga Library, vol. 2: The Story of the Ere-Dwellers (Eyrbyggja Saga), with The Heath-Slayings | William Morris and Eiríkr Magnússon | 1892 | have-raw | IA `sagalibrarydonei02snor` |
| `mm-saga-library-vol-3` | Snorri Sturluson | The Saga Library, vol. 3: Heimskringla, vol. I | William Morris and Eiríkr Magnússon | 1893 | have-raw | IA `sagalibrarydonei03snor` |
| `mm-saga-library-vol-4` | Snorri Sturluson | The Saga Library, vol. 4: Heimskringla, vol. II | William Morris and Eiríkr Magnússon | 1894 | have-raw | IA `sagalibrarydonei04snor` |
| `mm-saga-library-vol-5` | Snorri Sturluson | The Saga Library, vol. 5: Heimskringla, vol. III | William Morris and Eiríkr Magnússon | 1895 | have-raw | IA `sagalibrary05snoruoft` |
| `mm-saga-library-vol-6` | Snorri Sturluson | The Saga Library, vol. 6: Heimskringla, vol. IV (Magnússon's life of Snorri, notes and indexes) | Eiríkr Magnússon | 1905 | have-raw | IA `sagalibrarydonei06snor` |
| `mm-three-northern-love-stories` | anonymous (Old Norse) | Three Northern Love Stories and Other Tales | Eiríkr Magnússon and William Morris | 1875 | have-raw | IA `threenorthernlo00morrgoog` |
| — | — | pg-347: Another Grettir's Saga with no translator named (apparently G. A. Hight's 1914 Everyman version); not Magnússon and Morris. | — | — | excluded | — |
| — | — | pg-48622: Baring-Gould's Grettir the Outlaw, his own retelling; on baring-gould_shelf.json. | — | — | excluded | — |
| — | — | sagalibrary01snoruoft: Labelled vol. 1 on archive.org, but its title page reads Saga Library VOL. III (Heimskringla I); the cdl copy is used for vol. 3. | — | — | excluded | — |
| — | — | heimskringla-laing: Laing's Heimskringla (a different translation) is on sturluson_shelf.json; the Saga Library Heimskringla here is Morris and Magnússon's, a second witness. | — | — | excluded | — |
| — | — | mm-volsunga: PG 1152 (Volsunga Saga) lives on Lane D's poetic-edda_shelf.json as edda-volsunga-morris; this shelf only cross-references it. | — | — | excluded | — |

## Strindberg in English (Björkman, the Olands, Field, Schleussner)

Shelf: `pipeline/strindberg-english_shelf.json` · fetch `python3 pipeline/fetch_shelf.py strindberg-english` · titles `python3 pipeline/split_shelf_titles.py strindberg-english`.
Round 12 (2026-10-10), vetoable. Each title gates on its own translator. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `strindberg-bjorkman-plays-2` | Strindberg | Plays, second series: There Are Crimes and Crimes; Miss Julia; The Stronger; Creditors; Pariah | Edwin Björkman | 1913 | have | PG 14347 |
| `strindberg-bjorkman-plays-3` | Strindberg | Plays, third series: Swanwhite; Simoom; Debit and Credit; Advent; The Thunderstorm; After the Fire | Edwin Björkman | 1913 | have | PG 44233 |
| `strindberg-bjorkman-plays-4` | Strindberg | Plays, fourth series: The Bridal Crown; The Spook Sonata; The First Warning; Gustavus Vasa | Edwin Björkman | 1916 | have | PG 44302 |
| `strindberg-bjorkman-master-olof` | Strindberg | Master Olof | Edwin Björkman | 1915 | have | PG 7363 |
| `strindberg-oland-plays-1` | Strindberg | Plays: The Father; Countess Julie; The Outlaw; The Stronger | Edith and Warner Oland | 1912 | have | PG 8499 |
| `strindberg-oland-plays-2` | Strindberg | Plays: Comrades; Facing Death; Pariah; Easter | Edith and Warner Oland | 1912 | have | PG 8500 |
| `strindberg-field-inferno` | Strindberg | The Inferno | Claud Field | 1912 | have | PG 44108 |
| `strindberg-field-son-of-a-servant` | Strindberg | The Son of a Servant | Claud Field | 1913 | have | PG 44109 |
| `strindberg-field-zones-of-the-spirit` | Strindberg | Zones of the Spirit | Claud Field | 1913 | have | PG 44118 |
| `strindberg-field-german-lieutenant` | Strindberg | The German Lieutenant and Other Stories | Claud Field | 1915 | have | PG 46107 |
| `strindberg-field-historical-miniatures` | Strindberg | Historical Miniatures | Claud Field | 1913 | have | PG 7955 |
| `strindberg-schleussner-red-room` | Strindberg | The Red Room | Ellie Schleussner | 1913 | have | PG 37039 |
| `strindberg-schleussner-confession-of-a-fool` | Strindberg | The Confession of a Fool | Ellie Schleussner | 1912 | have | PG 44106 |
| `strindberg-schleussner-in-midsummer-days` | Strindberg | In Midsummer Days and Other Tales | Ellie Schleussner | 1913 | have | PG 6694 |
| `strindberg-bjorkman-plays-1` | Strindberg | Plays, first series: The Dream Play; The Link; The Dance of Death I and II | Edwin Björkman | 1912 | have-raw | IA `playsbyauguststr00stri` |
| — | — | pg-4970: There Are Crimes and Crimes alone: the same Björkman text is in the second series (14347). | — | — | excluded | — |
| — | — | pg-5053: Creditors and Pariah alone: the same Björkman text is in the second series. | — | — | excluded | — |
| — | — | pg-8875: The Road to Damascus, tr. Graham Rawson: the text cites a 1937 production; Rawson's translation is of 1939. Not before 1931. | — | — | excluded | — |
| — | — | pg-7956: Married (1913): no translator named. | — | — | excluded | — |
| — | — | pg-46397: Legends (1912): no translator named. | — | — | excluded | — |

## Marmaduke Pickthall (The Meaning of the Glorious Koran, 1930)

Shelf: `pipeline/pickthall_shelf.json` · fetch `python3 pipeline/fetch_shelf.py pickthall` · titles `python3 pipeline/split_shelf_titles.py pickthall`.
Round 13 (2026-10-10), vetoable. US public domain since 2026; gate override recorded. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `pickthall-meaning-of-the-glorious-koran` | The Quran | The Meaning of the Glorious Koran: An Explanatory Translation | Marmaduke Pickthall | 1930 | have-raw | IA `in.ernet.dli.2015.283503` |
| — | — | dli.ministry.16944: The same sheets reissued under a George Allen & Unwin title page (Allen & Unwin took over Knopf's London list in 1931): a later issue; the Knopf issue is used. | — | — | excluded | — |

## Katharine Prescott Wormeley (Balzac; Daudet, Sand)

Shelf: `pipeline/wormeley_shelf.json` · fetch `python3 pipeline/fetch_shelf.py wormeley` · titles `python3 pipeline/split_shelf_titles.py wormeley`.
Round 14 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `wormeley-balzac-ursula` | Honoré de Balzac | Ursula | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1223 |
| `wormeley-balzac-pierre-grassou` | Honoré de Balzac | Pierre Grassou | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1230 |
| `wormeley-balzac-unconscious-comedians` | Honoré de Balzac | Unconscious Comedians | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1242 |
| `wormeley-balzac-bureaucracy` | Honoré de Balzac | Bureaucracy | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1343 |
| `wormeley-balzac-the-secrets-of-the-princesse-de-cadignan` | Honoré de Balzac | The Secrets of the Princesse de Cadignan | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1344 |
| `wormeley-balzac-the-vicar-of-tours` | Honoré de Balzac | The Vicar of Tours | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1345 |
| `wormeley-balzac-an-old-maid` | Honoré de Balzac | An Old Maid | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1352 |
| `wormeley-balzac-madame-firmiani` | Honoré de Balzac | Madame Firmiani | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1357 |
| `wormeley-balzac-paz-la-fausse-maitresse` | Honoré de Balzac | Paz (La Fausse Maitresse) | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1369 |
| `wormeley-balzac-study-of-a-woman` | Honoré de Balzac | Study of a Woman | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1373 |
| `wormeley-balzac-vendetta` | Honoré de Balzac | Vendetta | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1374 |
| `wormeley-balzac-the-two-brothers` | Honoré de Balzac | The Two Brothers | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1380 |
| `wormeley-balzac-a-start-in-life` | Honoré de Balzac | A Start in Life | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1403 |
| `wormeley-balzac-sons-of-the-soil` | Honoré de Balzac | Sons of the Soil | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1417 |
| `wormeley-balzac-el-verdugo` | Honoré de Balzac | El Verdugo | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1425 |
| `wormeley-balzac-the-recruit` | Honoré de Balzac | The Recruit | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1426 |
| `wormeley-balzac-a-drama-on-the-seashore` | Honoré de Balzac | A Drama on the Seashore | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1427 |
| `wormeley-balzac-seraphita` | Honoré de Balzac | Seraphita | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1432 |
| `wormeley-balzac-the-red-inn` | Honoré de Balzac | The Red Inn | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1433 |
| `wormeley-balzac-juana` | Honoré de Balzac | Juana | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1437 |
| `wormeley-balzac-the-alkahest` | Honoré de Balzac | The Alkahest | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1453 |
| `wormeley-balzac-maitre-cornelius` | Honoré de Balzac | Maitre Cornelius | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1454 |
| `wormeley-balzac-the-hated-son` | Honoré de Balzac | The Hated Son | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1455 |
| `wormeley-balzac-the-illustrious-gaudissart` | Honoré de Balzac | The Illustrious Gaudissart | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1474 |
| `wormeley-balzac-a-daughter-of-eve` | Honoré de Balzac | A Daughter of Eve | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1481 |
| `wormeley-balzac-modeste-mignon` | Honoré de Balzac | Modeste Mignon | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1482 |
| `wormeley-balzac-the-hidden-masterpiece` | Honoré de Balzac | The Hidden Masterpiece | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1553 |
| `wormeley-balzac-adieu` | Honoré de Balzac | Adieu | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1554 |
| `wormeley-balzac-the-marriage-contract` | Honoré de Balzac | The Marriage Contract | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1556 |
| `wormeley-balzac-the-lily-of-the-valley` | Honoré de Balzac | The Lily of the Valley | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1569 |
| `wormeley-balzac-the-lesser-bourgeoisie` | Honoré de Balzac | The Lesser Bourgeoisie | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1641 |
| `wormeley-balzac-ferragus-chief-of-the-d-vorants` | Honoré de Balzac | Ferragus, Chief of the Dévorants | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1649 |
| `wormeley-balzac-eugenie-grandet` | Honoré de Balzac | Eugenie Grandet | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1715 |
| `wormeley-balzac-catherine-de-medici` | Honoré de Balzac | Catherine De Medici | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1854 |
| `wormeley-balzac-the-deputy-of-arcis` | Honoré de Balzac | The Deputy of Arcis | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1871 |
| `wormeley-balzac-the-village-rector` | Honoré de Balzac | The Village Rector | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1899 |
| `wormeley-balzac-beatrix` | Honoré de Balzac | Beatrix | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1957 |
| `wormeley-balzac-the-brotherhood-of-consolation` | Honoré de Balzac | The Brotherhood of Consolation | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1967 |
| `wormeley-daudet-tartarin-on-the-alps` | Alphonse Daudet | Tartarin on the Alps | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 25768 |
| `wormeley-balzac-letters-to-madame-hanska-born-countess-rzewuska` | Honoré de Balzac | Letters to Madame Hanska, born Countess Rzewuska, aft | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 54466 |
| `wormeley-sand-the-bagpipers` | George Sand | The Bagpipers | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 66513 |
| — | — | pg-7927: The Celibates collects Pierrette, The Vicar of Tours and The Two Brothers; the last two are shelved singly (1345, 1380), so the collection would hold them twice. | — | — | excluded | — |
| — | — | pg-43283: The Correspondence of Madame, Princess Palatine (ed. Wormeley): letters, edited not translated in the same sense; not checked. | — | — | excluded | — |

## Ernest Alfred Vizetelly (Zola, incl. the Three Cities)

Shelf: `pipeline/vizetelly_shelf.json` · fetch `python3 pipeline/fetch_shelf.py vizetelly` · titles `python3 pipeline/split_shelf_titles.py vizetelly`.
Round 14 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `vizetelly-zola-his-masterpiece` | Émile Zola | His Masterpiece | Ernest Alfred Vizetelly (named in the Gutenberg header as editor) | 1886-1906 (Chatto and Windus) | have | PG 15900 |
| `vizetelly-zola-the-fortune-of-the-rougons` | Émile Zola | The Fortune of the Rougons | Ernest Alfred Vizetelly (named in the Gutenberg header as editor) | 1886-1906 (Chatto and Windus) | have | PG 5135 |
| `vizetelly-zola-fruitfulness` | Émile Zola | Fruitfulness | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 10330 |
| `vizetelly-zola-abbe-mourets-transgression` | Émile Zola | Abbe Mouret's Transgression | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 14200 |
| `vizetelly-zola-the-ladies-paradise` | Émile Zola | The Ladies' Paradise | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 54726 |
| `vizetelly-zola-work-travail` | Émile Zola | Work [Travail] | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 55282 |
| `vizetelly-zola-truth-v-rit` | Émile Zola | Truth [Vérité] | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 55849 |
| `vizetelly-zola-the-rush-for-the-spoil-la-cur-e-a-realistic-nove` | Émile Zola | The Rush for the Spoil (La Curée): A Realistic Novel | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 56590 |
| `vizetelly-zola-his-excellency-son-exc-eug-ne-rougon` | Émile Zola | His Excellency [Son Exc. Eugène Rougon] | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 56654 |
| `vizetelly-zola-the-downfall-la-d-b-cle-a-story-of-the-horrors-o` | Émile Zola | The Downfall (La Débâcle): A Story of the Horrors o | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 56799 |
| `vizetelly-zola-the-conquest-of-plassans-la-conqu-te-de-plassans` | Émile Zola | The Conquest of Plassans (La Conquête de Plassans) | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 56860 |
| `vizetelly-zola-the-fat-and-the-thin` | Émile Zola | The Fat and the Thin | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 5744 |
| `vizetelly-zola-theresa-raquin` | Émile Zola | Theresa Raquin | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 6626 |
| `vizetelly-zola-lourdes` | Émile Zola | Lourdes | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 8516 |
| `vizetelly-zola-rome` | Émile Zola | Rome | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 8726 |
| `vizetelly-zola-paris` | Émile Zola | Paris | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 9169 |
| — | — | three-cities-parts: Gutenberg also splits Lourdes, Rome and Paris into volumes (8511-8515, 8721-8725, 9165-9167) and has a trilogy omnibus (9170); the complete single-novel texts (8516, 8726, 9169) are used, so nothing is held twice. | — | — | excluded | — |

## Leo Wiener's Complete Works of Count Tolstoy (1904-05)

Shelf: `pipeline/wiener-tolstoy_shelf.json` · fetch `python3 pipeline/fetch_shelf.py wiener-tolstoy` · titles `python3 pipeline/split_shelf_titles.py wiener-tolstoy`.
Round 15 (2026-10-10), vetoable. One title per volume, 24 volumes. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `wiener-tolstoy-vol-01` | Tolstoy | Complete Works, vol. 1: Childhood, Boyhood, Youth; The Incursion | Leo Wiener | 1904 | have-raw | IA `completeworksofc01tols` |
| `wiener-tolstoy-vol-02` | Tolstoy | Complete Works, vol. 2: A Landed Proprietor; The Cossacks; Sevastopol | Leo Wiener | 1904 | have-raw | IA `completeworksofc02tols` |
| `wiener-tolstoy-vol-03` | Tolstoy | Complete Works, vol. 3: A Moscow Acquaintance; The Snow-Storm; Domestic Happiness; Miscellanies | Leo Wiener | 1904 | have-raw | IA `completeworksofc03tols` |
| `wiener-tolstoy-vol-04` | Tolstoy | Complete Works, vol. 4: Pedagogical Articles; Linen-Measurer | Leo Wiener | 1904 | have-raw | IA `completeworksofc04tols` |
| `wiener-tolstoy-vol-05` | Tolstoy | Complete Works, vol. 5: War and Peace, vol. I | Leo Wiener | 1904 | have-raw | IA `completeworksofc05tols` |
| `wiener-tolstoy-vol-06` | Tolstoy | Complete Works, vol. 6: War and Peace, vol. II | Leo Wiener | 1904 | have-raw | IA `completeworksofc06tols` |
| `wiener-tolstoy-vol-07` | Tolstoy | Complete Works, vol. 7: War and Peace, vol. III | Leo Wiener | 1904 | have-raw | IA `completeworksofc07tols` |
| `wiener-tolstoy-vol-08` | Tolstoy | Complete Works, vol. 8: War and Peace, vol. IV | Leo Wiener | 1904 | have-raw | IA `completeworksof08tols` |
| `wiener-tolstoy-vol-09` | Tolstoy | Complete Works, vol. 9: Anna Karénin, vol. I | Leo Wiener | 1904 | have-raw | IA `completeworksofc09tols` |
| `wiener-tolstoy-vol-10` | Tolstoy | Complete Works, vol. 10: Anna Karénin, vol. II | Leo Wiener | 1904 | have-raw | IA `completeworksof10tols` |
| `wiener-tolstoy-vol-11` | Tolstoy | Complete Works, vol. 11: Anna Karénin, vol. III | Leo Wiener | 1904 | have-raw | IA `completeworksofc11tols` |
| `wiener-tolstoy-vol-12` | Tolstoy | Complete Works, vol. 12: Fables for Children; Stories for Children; Natural Science Stories; Popular Education; Decembrists; Moral Tales | Leo Wiener | 1904 | have-raw | IA `completeworksofc12tols` |
| `wiener-tolstoy-vol-13` | Tolstoy | Complete Works, vol. 13: My Confession; Critique of Dogmatic Theology | Leo Wiener | 1904 | have-raw | IA `completeworksofc13tols` |
| `wiener-tolstoy-vol-14` | Tolstoy | Complete Works, vol. 14: The Four Gospels Harmonized and Translated, vol. I | Leo Wiener | 1904 | have-raw | IA `completeworksofc14tols` |
| `wiener-tolstoy-vol-15` | Tolstoy | Complete Works, vol. 15: The Four Gospels Harmonized and Translated, vol. II | Leo Wiener | 1904 | have-raw | IA `completeworksofc15tols` |
| `wiener-tolstoy-vol-16` | Tolstoy | Complete Works, vol. 16: My Religion; On Life; Thoughts on God; On the Meaning of Life | Leo Wiener | 1904 | have-raw | IA `completeworksofc16tols` |
| `wiener-tolstoy-vol-17` | Tolstoy | Complete Works, vol. 17: What Shall We Do Then?; On the Moscow Census; Collected Articles | Leo Wiener | 1904 | have-raw | IA `completeworksofc17tols` |
| `wiener-tolstoy-vol-18` | Tolstoy | Complete Works, vol. 18: The Death of Ivan Ilich; Dramatic Works; The Kreutzer Sonata | Leo Wiener | 1904 | have-raw | IA `completeworksofc18tols` |
| `wiener-tolstoy-vol-19` | Tolstoy | Complete Works, vol. 19: Walk in the Light while Ye Have Light; Thoughts and Aphorisms; Letters; Miscellanies | Leo Wiener | 1904 | have-raw | IA `completeworksofc19tols` |
| `wiener-tolstoy-vol-20` | Tolstoy | Complete Works, vol. 20: The Kingdom of God is Within You; Christianity and Patriotism; Miscellanies | Leo Wiener | 1905 | have-raw | IA `completeworksofc20tols` |
| `wiener-tolstoy-vol-21` | Tolstoy | Complete Works, vol. 21: Resurrection, vol. I | Leo Wiener | 1904 | have-raw | IA `completeworksofc21tols` |
| `wiener-tolstoy-vol-22` | Tolstoy | Complete Works, vol. 22: Resurrection, vol. II; What is Art?; The Christian Teaching | Leo Wiener | 1904 | have-raw | IA `completeworksofc22tols` |
| `wiener-tolstoy-vol-23` | Tolstoy | Complete Works, vol. 23: Miscellaneous Letters and Essays | Leo Wiener | 1905 | have-raw | IA `completeworksofc23tolsiala` |
| `wiener-tolstoy-vol-24` | Tolstoy | Complete Works, vol. 24: Latest Works; Life; General Index; Bibliography | Leo Wiener | 1905 | have-raw | IA `completeworksofc24tols` |
| — | — | completeworksofc08tols: Vol. 8 copy without its title page (starts at War and Peace Part XII); the Florida copy completeworksof08tols is used. | — | — | excluded | — |
| — | — | completeworksofc10tols: Vol. 10: archive.org returned HTTP 500 for its text; completeworksof10tols is used. | — | — | excluded | — |
| — | — | completeworksofc25tols-28tols: Vols 25-28 in the same cdl run are outside Wiener's 24-volume set; not checked. | — | — | excluded | — |
| — | — | pg-38025, pg-43372: Gutenberg texts of Wiener vols 12 and 20 exist; the scans are used for the whole set from one edition. | — | — | excluded | — |

## Charles Godfrey Leland's Heine (Works, vols 1-8, 1891-93)

Shelf: `pipeline/leland-heine_shelf.json` · fetch `python3 pipeline/fetch_shelf.py leland-heine` · titles `python3 pipeline/split_shelf_titles.py leland-heine`.
Round 16 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `leland-heine-vol-1` | Heine | The Works of Heinrich Heine, vol. 1: Florentine Nights; The Memoirs of Herr von Schnabelewopski; The Rabbi of Bacharach; Shakespeare's Maidens and Women | Charles Godfrey Leland | 1891 | have-raw | IA `worksofheinrichh01heinuoft` |
| `leland-heine-vol-2` | Heine | The Works of Heinrich Heine, vol. 2: Pictures of Travel, vol. I (1823-1826) | Charles Godfrey Leland | 1891 | have-raw | IA `worksofheinrichh02hein` |
| `leland-heine-vol-3` | Heine | The Works of Heinrich Heine, vol. 3: Pictures of Travel, vol. II (1828) | Charles Godfrey Leland | 1891 | have-raw | IA `worksofheinrichh03heinuoft` |
| `leland-heine-vol-4` | Heine | The Works of Heinrich Heine, vol. 4: The Salon, or Letters on Art, Music, Popular Life and Politics | Charles Godfrey Leland | 1893 | have-raw | IA `worksofheinrichh04heinuoft` |
| `leland-heine-vol-5` | Heine | The Works of Heinrich Heine, vol. 5: Germany, vol. I | Charles Godfrey Leland | 1892 | have-raw | IA `worksofheinrichh0005char` |
| `leland-heine-vol-6` | Heine | The Works of Heinrich Heine, vol. 6: Germany, vol. II | Charles Godfrey Leland | 1892 | have-raw | IA `in.ernet.dli.2015.39308` |
| `leland-heine-vol-7` | Heine | The Works of Heinrich Heine, vol. 7: French Affairs: Letters from Paris, vol. I | Charles Godfrey Leland | 1893 | have-raw | IA `worksofheinrichh07hein` |
| `leland-heine-vol-8` | Heine | The Works of Heinrich Heine, vol. 8: French Affairs: Letters from Paris, vol. II; Lutetia | Charles Godfrey Leland | 1893 | have-raw | IA `worksofheinrichh08heinuoft` |
| — | — | worksofheinrichh12hein: Vol. XII (1905): Margaret Armour's translation of the Romancero and Last Poems, not Leland's. | — | — | excluded | — |
| — | — | vols-9-11: Book of Songs and New Poems (Brooksbank/Armour, 1904-05): other translators. | — | — | excluded | — |

## Frederick Whishaw's Dostoevsky (Vizetelly, 1887-88)

Shelf: `pipeline/whishaw_shelf.json` · fetch `python3 pipeline/fetch_shelf.py whishaw` · titles `python3 pipeline/split_shelf_titles.py whishaw`.
Round 16 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `whishaw-dostoevsky-the-idiot` | Dostoevsky | The Idiot | Frederick Whishaw | 1887 | have-raw | IA `idiot00whisgoog` |
| `whishaw-dostoevsky-friend-of-the-family-and-the-gambler` | Dostoevsky | The Friend of the Family; and The Gambler | Frederick Whishaw | 1887 | have-raw | IA `friendfamilyand00whisgoog` |
| `whishaw-dostoevsky-uncles-dream-and-the-permanent-husband` | Dostoevsky | Uncle's Dream; and The Permanent Husband | Frederick Whishaw | 1888 | have | PG 38241 |
| `whishaw-crime-and-punishment` | — | Crime and Punishment (1886): no open scan found. | — | — | pending | — |
| `whishaw-injury-and-insult` | — | Injury and Insult (1887): the only full open copy (injuryinsult00dostrich) is a Micro Photo Inc. Duopage facsimile of the 1887 third edition, a photographic reprint of mid-century date; injuryandinsult00dostgoog's title page could not be read. Adam's call whether a photo-facsimile counts as the 1887 printing. | — | — | pending | — |
| — | — | ost-english-the_idiot: A second scan of the same 1887 Idiot. | — | — | excluded | — |
| — | — | unclesdreamandp00whisgoog: The Gutenberg text (38241) of the same book is used. | — | — | excluded | — |

## S. S. Koteliansky and his Bloomsbury collaborators (Chekhov, Gorky, Bunin, Shestov)

Shelf: `pipeline/koteliansky_shelf.json` · fetch `python3 pipeline/fetch_shelf.py koteliansky` · titles `python3 pipeline/split_shelf_titles.py koteliansky`.
Round 17 (2026-10-10), vetoable. UK status varies by co-translator. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `koteliansky-chekhov-note-book` | Chekhov | Note-Book of Anton Chekhov | S. S. Koteliansky and Leonard Woolf | 1921 | have | PG 12494 |
| `koteliansky-gorky-reminiscences-of-chekhov` | Gorky | Reminiscences of Anton Chekhov | S. S. Koteliansky and Leonard Woolf | 1921 | have | PG 37129 |
| `koteliansky-gorky-reminiscences-of-tolstoy` | Gorky | Reminiscences of Leo Nicolayevitch Tolstoi | S. S. Koteliansky and Leonard Woolf | 1920 | have | PG 55284 |
| `koteliansky-countess-tolstoy-autobiography` | S. A. Tolstaya | Autobiography of Countess Tolstoy | S. S. Koteliansky and Leonard Woolf | 1922 | have | PG 38027 |
| `koteliansky-bunin-gentleman-from-san-francisco` | Bunin | The Gentleman from San Francisco and Other Stories | S. S. Koteliansky and Leonard Woolf; the title story by D. H. Lawrence and S. S. Koteliansky (the book's own erratum note) | 1922 | have | PG 44998 |
| `koteliansky-chekhov-the-bet` | Chekhov | The Bet, and Other Stories | S. S. Koteliansky and J. M. Murry | 1915 | have | PG 55283 |
| `koteliansky-kuprin-river-of-life` | Kuprin | The River of Life, and Other Stories | S. S. Koteliansky and J. M. Murry | 1916 | have | PG 58406 |
| `koteliansky-shestov-anton-tchekhov` | Shestov | Anton Tchekhov, and Other Essays | S. S. Koteliansky and J. M. Murry | 1916 | have | PG 56758 |
| `koteliansky-shestov-all-things-are-possible` | Shestov | All Things are Possible | S. S. Koteliansky (foreword by D. H. Lawrence) | 1920 | have | PG 57369 |
| `koteliansky-goldenweizer-talks-with-tolstoi` | A. B. Goldenweizer | Talks with Tolstoi | S. S. Koteliansky and Virginia Woolf | 1923 | have | PG 65159 |

## Marian Fell (Chekhov, Korolenko)

Shelf: `pipeline/marian-fell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py marian-fell` · titles `python3 pipeline/split_shelf_titles.py marian-fell`.
Round 17 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `marian-fell-chekhov-swan-song` | Chekhov | Swan Song | Marian Fell | 1912 | have | PG 1753 |
| `marian-fell-chekhov-russian-silhouettes` | Chekhov | Russian Silhouettes: More Stories of Russian Life | Marian Fell | 1915 | have | PG 66790 |
| `marian-fell-korolenko-makars-dream` | Korolenko | Makar's Dream, and Other Stories | Marian Fell | 1916 | have | PG 62555 |
| `marian-fell-chekhov-plays` | — | Her Plays by Anton Tchekoff (Scribner, 1912/1916; Uncle Vanya, Ivanoff, The Sea-Gull, The Swan Song) is on archive.org; next round. | — | — | pending | — |

## Thomas Seltzer (Gorky, Andreyev, Gogol, Sudermann)

Shelf: `pipeline/seltzer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py seltzer` · titles `python3 pipeline/split_shelf_titles.py seltzer`.
Round 17 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `seltzer-gorky-the-spy` | Gorky | The Spy: The Story of a Superfluous Man | Thomas Seltzer | 1908 | have | PG 51094 |
| `seltzer-andreyev-savva-and-life-of-man` | Andreyev | Savva and The Life of Man | Thomas Seltzer | 1914 | have | PG 13147 |
| `seltzer-gogol-inspector-general` | Gogol | The Inspector-General | Thomas Seltzer | 1916 | have | PG 3735 |
| `seltzer-sudermann-song-of-songs` | Sudermann | The Song of Songs | Thomas Seltzer | 1909 | have | PG 34791 |
| `seltzer-ostwald-natural-philosophy` | Ostwald | Natural Philosophy | Thomas Seltzer | 1910 | have | PG 43791 |
| — | — | pg-13437: Best Russian Short Stories (1917): an anthology Seltzer edited, with many translators. | — | — | excluded | — |
| — | — | pg-17241: Atlantis: Adele Szold Seltzer's translation. | — | — | excluded | — |
| — | — | pg-62880: The Glebe magazine issue: a periodical. | — | — | excluded | — |

## Nathan Haskell Dole (Tolstoy, Palacio Valdés, Verga)

Shelf: `pipeline/dole_shelf.json` · fetch `python3 pipeline/fetch_shelf.py dole` · titles `python3 pipeline/split_shelf_titles.py dole`.
Round 17 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `dole-tolstoy-where-love-is` | Tolstoy | Where Love is There God is Also | Nathan Haskell Dole | 1887 | have | PG 38616 |
| `dole-tolstoy-the-invaders` | Tolstoy | The Invaders, and Other Stories | Nathan Haskell Dole | 1887 | have | PG 56797 |
| `dole-palacio-valdes-maximina` | Palacio Valdés | Maximina | Nathan Haskell Dole | 1888 | have | PG 33244 |
| `dole-palacio-valdes-marquis-of-penalta` | Palacio Valdés | The Marquis of Peñalta (Marta y María) | Nathan Haskell Dole | 1886 | have | PG 37969 |
| `dole-verga-under-the-shadow-of-etna` | Verga | Under the Shadow of Etna: Sicilian Stories | Nathan Haskell Dole | 1896 | have | PG 37979 |
| `dole-dupuy-great-masters-of-russian-literature` | Ernest Dupuy | The Great Masters of Russian Literature in the Nineteenth Century | Nathan Haskell Dole | 1886 | have | PG 71884 |
| — | — | pg-38520: Poems of James Russell Lowell: Dole wrote the introduction; not a translation. | — | — | excluded | — |
| — | — | pg-41119: A Russian Proprietor (Tolstoy, PG 41119): not checked this round. | — | — | excluded | — |

## Ellen Marriage (Balzac, Dent's Comédie Humaine, 1895-99)

Shelf: `pipeline/ellen-marriage_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ellen-marriage` · titles `python3 pipeline/split_shelf_titles.py ellen-marriage`.
Round 18 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ellen-marriage-balzac-the-message` | Honoré de Balzac | The Message | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1189 |
| `ellen-marriage-balzac-father-goriot` | Honoré de Balzac | Father Goriot | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1237 |
| `ellen-marriage-balzac-melmoth-reconciled` | Honoré de Balzac | Melmoth Reconciled | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1277 |
| `ellen-marriage-balzac-the-magic-skin` | Honoré de Balzac | The Magic Skin | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1307 |
| `ellen-marriage-balzac-gobseck` | Honoré de Balzac | Gobseck | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1389 |
| `ellen-marriage-balzac-the-collection-of-antiquities` | Honoré de Balzac | The Collection of Antiquities | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1405 |
| `ellen-marriage-balzac-la-grenadiere` | Honoré de Balzac | La Grenadiere | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1428 |
| `ellen-marriage-balzac-two-poets` | Honoré de Balzac | Two Poets | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1443 |
| `ellen-marriage-balzac-a-distinguished-provincial-at-paris` | Honoré de Balzac | A Distinguished Provincial at Paris | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1559 |
| `ellen-marriage-balzac-eve-and-david` | Honoré de Balzac | Eve and David | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1639 |
| `ellen-marriage-balzac-the-girl-with-the-golden-eyes` | Honoré de Balzac | The Girl with the Golden Eyes | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1659 |
| `ellen-marriage-balzac-the-deserted-woman` | Honoré de Balzac | The Deserted Woman | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1729 |
| `ellen-marriage-balzac-cousin-pons` | Honoré de Balzac | Cousin Pons | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1856 |
| `ellen-marriage-balzac-albert-savarus` | Honoré de Balzac | Albert Savarus | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1898 |
| `ellen-marriage-balzac-a-woman-of-thirty` | Honoré de Balzac | A Woman of Thirty | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1950 |
| `ellen-marriage-balzac-the-duchesse-of-langeais` | Honoré de Balzac | The Duchesse of Langeais | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 469 |
| `ellen-marriage-balzac-farewell` | Honoré de Balzac | Farewell | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 5873 |
| `ellen-marriage-balzac-the-jealousies-of-a-country-town` | Honoré de Balzac | The Jealousies of a Country Town | Ellen Marriage | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 7950 |
| — | — | pg-7416: The Thirteen collects Ferragus, The Duchesse de Langeais and The Girl with the Golden Eyes; the last two are shelved singly. | — | — | excluded | — |
| — | — | pg-13159: Lost Illusions collects Two Poets, A Distinguished Provincial at Paris and Eve and David, all shelved singly. | — | — | excluded | — |
| — | — | pg-12900: Poor Relations is the series title over Cousin Pons and Cousin Betty; Cousin Pons is shelved singly and Cousin Betty is Waring's (adler_shelf.json). | — | — | excluded | — |

## Clara Bell (Ebers, Eckstein, Hillern, Jókai and other German/Hungarian novels; Balzac)

Shelf: `pipeline/clara-bell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py clara-bell` · titles `python3 pipeline/split_shelf_titles.py clara-bell`.
Round 18 (2026-10-10), vetoable. Ebers complete texts only, not the PG part-files. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `clara-bell-balzac-a-prince-of-bohemia` | Honoré de Balzac | A Prince of Bohemia | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1812 |
| `clara-bell-balzac-a-second-home` | Honoré de Balzac | A Second Home | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1810 |
| `clara-bell-balzac-an-episode-under-the-terror` | Honoré de Balzac | An Episode under the Terror | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1456 |
| `clara-bell-balzac-another-study-of-woman` | Honoré de Balzac | Another Study of Woman | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1714 |
| `clara-bell-balzac-at-the-sign-of-the-cat-and-racket` | Honoré de Balzac | At the Sign of the Cat and Racket | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1680 |
| `clara-bell-balzac-colonel-chabert` | Honoré de Balzac | Colonel Chabert | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1954 |
| `clara-bell-balzac-domestic-peace` | Honoré de Balzac | Domestic Peace | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1411 |
| `clara-bell-balzac-facino-cane` | Honoré de Balzac | Facino Cane | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1737 |
| `clara-bell-balzac-gaudissart-ii` | Honoré de Balzac | Gaudissart II | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1475 |
| `clara-bell-balzac-honorine` | Honoré de Balzac | Honorine | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1683 |
| `clara-bell-balzac-la-grande-breteche` | Honoré de Balzac | La Grande Breteche | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1710 |
| `clara-bell-balzac-louis-lambert` | Honoré de Balzac | Louis Lambert | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1943 |
| `clara-bell-balzac-massimilla-doni` | Honoré de Balzac | Massimilla Doni | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1811 |
| `clara-bell-balzac-sarrasine` | Honoré de Balzac | Sarrasine | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1826 |
| `clara-bell-balzac-the-atheists-mass` | Honoré de Balzac | The Atheist's Mass | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1220 |
| `clara-bell-balzac-the-ball-at-sceaux` | Honoré de Balzac | The Ball at Sceaux | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1305 |
| `clara-bell-balzac-the-commission-in-lunacy` | Honoré de Balzac | The Commission in Lunacy | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1410 |
| `clara-bell-balzac-the-country-doctor` | Honoré de Balzac | The Country Doctor | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1350 |
| `clara-bell-balzac-the-elixir-of-life` | Honoré de Balzac | The Elixir of Life | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1215 |
| `clara-bell-balzac-the-exiles` | Honoré de Balzac | The Exiles | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1884 |
| `clara-bell-balzac-the-purse` | Honoré de Balzac | The Purse | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1196 |
| `clara-bell-balzac-the-works-of-honor-de-balzac-about-catherine-de-m` | Honoré de Balzac | The Works of Honoré de Balzac: About Catherine de' M | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 37285 |
| `clara-bell-balzac-z-marcas` | Honoré de Balzac | Z. Marcas | Clara Bell | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1841 |
| `clara-bell-couperus-footsteps-of-fate` | Louis Couperus | Footsteps of Fate | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 34678 |
| `clara-bell-ebers-a-thorny-path` | Georg Ebers | A Thorny Path | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 5542 |
| `clara-bell-ebers-homo-sum` | Georg Ebers | Homo Sum | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 5499 |
| `clara-bell-ebers-margery-gred-a-tale-of-old-nuremberg` | Georg Ebers | Margery (Gred): A Tale Of Old Nuremberg | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 5560 |
| `clara-bell-ebers-serapis` | Georg Ebers | Serapis | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 5507 |
| `clara-bell-ebers-the-bride-of-the-nile` | Georg Ebers | The Bride of the Nile | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 5529 |
| `clara-bell-ebers-the-emperor` | Georg Ebers | The Emperor | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 5493 |
| `clara-bell-ebers-the-sisters` | Georg Ebers | The Sisters | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 5466 |
| `clara-bell-ebers-uarda-a-romance-of-ancient-egypt` | Georg Ebers | Uarda: a Romance of Ancient Egypt | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 5449 |
| `clara-bell-eckstein-quintus-claudius-vol-1` | Ernst Eckstein | Quintus Claudius: A Romance of Imperial Rome. Volume 1 | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 47221 |
| `clara-bell-eckstein-quintus-claudius-vol-2` | Ernst Eckstein | Quintus Claudius: A Romance of Imperial Rome. Volume 2 | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 47222 |
| `clara-bell-gald-s-leon-roch-a-romance-vol-1-of-2` | Benito Pérez Galdós | Leon Roch: A Romance, vol. 1 (of 2) | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 48752 |
| `clara-bell-gald-s-leon-roch-a-romance-vol-2-of-2` | Benito Pérez Galdós | Leon Roch: A Romance, vol. 2 (of 2) | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 49272 |
| `clara-bell-gald-s-marianela` | Benito Pérez Galdós | Marianela | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 48818 |
| `clara-bell-hillern-the-hour-will-come` | Wilhelmine von Hillern | The Hour Will Come: A Tale of an Alpine Cloister (Volumes I and II) | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 36811 |
| `clara-bell-hillern-the-vulture-maiden-die-geier-wally` | Wilhelmine von Hillern | The Vulture Maiden [Die Geier-Wally.] | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 36827 |
| `clara-bell-huysmans-the-cathedral` | J.-K. Huysmans | The Cathedral | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 15067 |
| `clara-bell-karadordevic-enchanted-india` | Bozidar Karadordevic | Enchanted India | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 57153 |
| `clara-bell-maupassant-pierre-and-jean` | Guy de Maupassant | Pierre and Jean | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 3804 |
| `clara-bell-vald-froth-a-novel` | Armando Palacio Valdé | Froth: A Novel | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 38411 |
| — | — | ebers-volume-splits: Gutenberg's per-volume splits of Uarda, The Sisters, The Emperor, Homo Sum, Serapis, The Bride of the Nile, A Thorny Path and Margery are left out; the complete texts (5449, 5466, 5493, 5499, 5507, 5529, 5542, 5560) are used. | — | — | excluded | — |
| — | — | pg-7958: The Napoleon of the People is an extract from The Country Doctor (1350), shelved whole. | — | — | excluded | — |
| — | — | two-volume-novels: Leon Roch (48752, 49272) and Quintus Claudius (47221, 47222) have no complete Gutenberg text; each Gutenberg volume is shelved as its own title. | — | — | excluded | — |

## James Waring (Balzac, Dent)

Shelf: `pipeline/waring_shelf.json` · fetch `python3 pipeline/fetch_shelf.py waring` · titles `python3 pipeline/split_shelf_titles.py waring`.
Round 18 (2026-10-10), vetoable. His Cousin Betty is held on adler_shelf.json. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `waring-balzac-the-firm-of-nucingen` | Honoré de Balzac | The Firm of Nucingen | James Waring | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1294 |
| `waring-balzac-scenes-from-a-courtesans-life` | Honoré de Balzac | Scenes from a Courtesan's Life | James Waring | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1660 |
| `waring-balzac-the-muse-of-the-department` | Honoré de Balzac | The Muse of the Department | James Waring | 1895-1900 (Dent, ed. George Saintsbury) | have | PG 1912 |
| `waring-balzac-cousin-betty` | Honoré de Balzac | Cousin Betty | James Waring | 1895-1900 (Dent, ed. George Saintsbury) | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `balzac-cousinbette` (PG 1749) |
| — | — | pg-7929: Parisians in the Country is the series title over The Illustrious Gaudissart and The Muse of the Department; Waring's Muse is shelved singly and Gaudissart is Wormeley's (wormeley_shelf.json). | — | — | excluded | — |

## Alexander Teixeira de Mattos (Fabre, Maeterlinck, Couperus, Leblanc, Chateaubriand)

Shelf: `pipeline/teixeira-de-mattos_shelf.json` · fetch `python3 pipeline/fetch_shelf.py teixeira-de-mattos` · titles `python3 pipeline/split_shelf_titles.py teixeira-de-mattos`.
Round 19 (2026-10-10), vetoable. Carl Ewald is left to the other lane's ewald_shelf.json. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `teixeira-de-mattos-chateaubriand-memoirs-vol-1` | François-René Chateaubriand | The Memoirs of François René, Vicomte de Chateaubriand, vol. 1 of 6 | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 54743 |
| `teixeira-de-mattos-chateaubriand-memoirs-vol-2` | François-René Chateaubriand | The Memoirs of François René, Vicomte de Chateaubriand, vol. 2 of 6 | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 54788 |
| `teixeira-de-mattos-chateaubriand-memoirs-vol-3` | François-René Chateaubriand | The Memoirs of François René, Vicomte de Chateaubriand, vol. 3 of 6 | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 54807 |
| `teixeira-de-mattos-chateaubriand-memoirs-vol-4` | François-René Chateaubriand | The Memoirs of François René, Vicomte de Chateaubriand, vol. 4 of 6 | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 54879 |
| `teixeira-de-mattos-chateaubriand-memoirs-vol-5` | François-René Chateaubriand | The Memoirs of François René, Vicomte de Chateaubriand, vol. 5 of 6 | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 55070 |
| `teixeira-de-mattos-chateaubriand-memoirs-vol-6` | François-René Chateaubriand | The Memoirs of François René, Vicomte de Chateaubriand, vol. 6 of 6 | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 55124 |
| `teixeira-de-mattos-couperus-dr-adriaan` | Louis Couperus | Dr. Adriaan | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 34761 |
| `teixeira-de-mattos-couperus-ecstasy-a-study-of-happiness-a-novel` | Louis Couperus | Ecstasy, A Study of Happiness: A Novel | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 37770 |
| `teixeira-de-mattos-couperus-majesty-a-novel` | Louis Couperus | Majesty: A Novel | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 33779 |
| `teixeira-de-mattos-couperus-old-people-and-the-things-that-pass` | Louis Couperus | Old People and the Things That Pass | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 48271 |
| `teixeira-de-mattos-couperus-small-souls` | Louis Couperus | Small Souls | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 34021 |
| `teixeira-de-mattos-couperus-the-hidden-force-a-story-of-modern-java` | Louis Couperus | The Hidden Force: A Story of Modern Java | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 34725 |
| `teixeira-de-mattos-couperus-the-inevitable` | Louis Couperus | The Inevitable | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 43005 |
| `teixeira-de-mattos-couperus-the-later-life` | Louis Couperus | The Later Life | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 37578 |
| `teixeira-de-mattos-couperus-the-law-inevitable` | Louis Couperus | The Law Inevitable | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 43827 |
| `teixeira-de-mattos-couperus-the-tour-a-story-of-ancient-egypt` | Louis Couperus | The Tour: A Story of Ancient Egypt | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 37497 |
| `teixeira-de-mattos-couperus-the-twilight-of-the-souls` | Louis Couperus | The Twilight of the Souls | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 34458 |
| `teixeira-de-mattos-fabre-bramble-bees-and-others` | Jean-Henri Fabre | Bramble-Bees and Others | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 3421 |
| `teixeira-de-mattos-fabre-more-beetles` | Jean-Henri Fabre | More Beetles | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 67201 |
| `teixeira-de-mattos-fabre-more-hunting-wasps` | Jean-Henri Fabre | More Hunting Wasps | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 3462 |
| `teixeira-de-mattos-fabre-the-glow-worm-and-other-beetles` | Jean-Henri Fabre | The Glow-Worm and Other Beetles | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 27868 |
| `teixeira-de-mattos-fabre-the-hunting-wasps` | Jean-Henri Fabre | The Hunting Wasps | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 67110 |
| `teixeira-de-mattos-fabre-the-life-and-love-of-the-insect` | Jean-Henri Fabre | The Life and Love of the Insect | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 68974 |
| `teixeira-de-mattos-fabre-the-life-of-the-caterpillar` | Jean-Henri Fabre | The Life of the Caterpillar | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 66762 |
| `teixeira-de-mattos-fabre-the-life-of-the-fly-with-which-are-inter` | Jean-Henri Fabre | The Life of the Fly; With Which are Interspersed Some Chapters of Autobiography | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 3422 |
| `teixeira-de-mattos-fabre-the-life-of-the-grasshopper` | Jean-Henri Fabre | The Life of the Grasshopper | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 66650 |
| `teixeira-de-mattos-fabre-the-life-of-the-scorpion` | Jean-Henri Fabre | The Life of the Scorpion | Alexander Teixeira de Mattos (with Bernard Miall) | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 66744 |
| `teixeira-de-mattos-fabre-the-life-of-the-spider` | Jean-Henri Fabre | The Life of the Spider | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 1887 |
| `teixeira-de-mattos-fabre-the-life-of-the-weevil` | Jean-Henri Fabre | The Life of the Weevil | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 66844 |
| `teixeira-de-mattos-fabre-the-mason-bees` | Jean-Henri Fabre | The Mason-Bees | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 2884 |
| `teixeira-de-mattos-fabre-the-mason-wasps` | Jean-Henri Fabre | The Mason-Wasps | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 66854 |
| `teixeira-de-mattos-fabre-the-sacred-beetle-and-others` | Jean-Henri Fabre | The Sacred Beetle, and Others | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 66743 |
| `teixeira-de-mattos-fabre-the-wonders-of-instinct-chapters-in-the` | Jean-Henri Fabre | The Wonders of Instinct: Chapters in the Psychology of Insects | Alexander Teixeira de Mattos (with Bernard Miall) | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 3754 |
| `teixeira-de-mattos-leblanc-813` | Maurice Leblanc | 813 | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 34758 |
| `teixeira-de-mattos-leblanc-the-choice-of-life` | Georgette Leblanc | The Choice of Life | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 22411 |
| `teixeira-de-mattos-leblanc-the-eyes-of-innocence` | Maurice Leblanc | The eyes of innocence | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 73662 |
| `teixeira-de-mattos-leblanc-the-frontier` | Maurice Leblanc | The Frontier | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 28480 |
| `teixeira-de-mattos-leblanc-the-hollow-needle-further-adventures-of` | Maurice Leblanc | The Hollow Needle; Further adventures of Arsène Lupin | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 4017 |
| `teixeira-de-mattos-leblanc-the-secret-of-sarek` | Maurice Leblanc | The Secret of Sarek | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 34939 |
| `teixeira-de-mattos-leblanc-the-three-eyes` | Maurice Leblanc | The Three Eyes | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 34653 |
| `teixeira-de-mattos-leblanc-the-tremendous-event` | Maurice Leblanc | The Tremendous Event | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 33386 |
| `teixeira-de-mattos-maeterlinck-death` | Maurice Maeterlinck | Death | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 31354 |
| `teixeira-de-mattos-maeterlinck-gleanings-from-maeterlinck` | Maurice Maeterlinck | Gleanings from Maeterlinck | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 67625 |
| `teixeira-de-mattos-maeterlinck-joyzelle` | Maurice Maeterlinck | Joyzelle | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 47486 |
| `teixeira-de-mattos-maeterlinck-mary-magdalene-a-play-in-three-acts` | Maurice Maeterlinck | Mary Magdalene: A Play in Three Acts | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 67806 |
| `teixeira-de-mattos-maeterlinck-mountain-paths` | Maurice Maeterlinck | Mountain Paths | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 66893 |
| `teixeira-de-mattos-maeterlinck-old-fashioned-flowers-and-other-out-of-d` | Maurice Maeterlinck | Old Fashioned Flowers, and other out-of-door studies | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 55591 |
| `teixeira-de-mattos-maeterlinck-our-eternity` | Maurice Maeterlinck | Our Eternity | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 50399 |
| `teixeira-de-mattos-maeterlinck-our-friend-the-dog` | Maurice Maeterlinck | Our Friend the Dog | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 18214 |
| `teixeira-de-mattos-maeterlinck-the-betrothal-a-sequel-to-the-blue-bird` | Maurice Maeterlinck | The Betrothal A Sequel to the Blue Bird; A Fairy Play in Five Acts and Eleven Scenes | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 34343 |
| `teixeira-de-mattos-maeterlinck-the-blue-bird-a-fairy-play-in-six-acts` | Maurice Maeterlinck | The Blue Bird: A Fairy Play in Six Acts | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 8606 |
| `teixeira-de-mattos-maeterlinck-the-burgomaster-of-stilemonde-a-play-in` | Maurice Maeterlinck | The Burgomaster of Stilemonde: A Play in Three Acts | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 47830 |
| `teixeira-de-mattos-maeterlinck-the-double-garden` | Maurice Maeterlinck | The Double Garden | Alexander Teixeira de Mattos (with Alfred Sutro) | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 48504 |
| `teixeira-de-mattos-maeterlinck-the-miracle-of-saint-anthony` | Maurice Maeterlinck | The miracle of Saint Anthony | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 70550 |
| `teixeira-de-mattos-maeterlinck-the-unknown-guest` | Maurice Maeterlinck | The Unknown Guest | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 2033 |
| `teixeira-de-mattos-maeterlinck-the-wrack-of-the-storm` | Maurice Maeterlinck | The Wrack of the Storm | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 17861 |
| `teixeira-de-mattos-paoli-their-majesties-as-i-knew-them-personal` | Xavier Paoli | Their Majesties as I Knew Them Personal Reminiscences of the Kings and Queens of Europe | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 45786 |
| `teixeira-de-mattos-streuvels-the-path-of-life` | Stijn Streuvels | The Path of Life | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 8437 |
| `teixeira-de-mattos-tocqueville-the-recollections-of-alexis-de-tocquevil` | Alexis de Tocqueville | The Recollections of Alexis de Tocqueville | Alexander Teixeira de Mattos | 1894-1922 (he died 1921; see the Gutenberg header) | have | PG 37892 |
| — | — | pg-27991: The Blue Bird for Children: Perkins's retelling for schools, not the play. | — | — | excluded | — |
| — | — | pg-45812: Insect Adventures: Louise Zimm's selection for children from the translation. | — | — | excluded | — |
| — | — | pg-67000: Fabre's Book of Insects: Mrs Rodolph Stawell's retelling, not the translation itself. | — | — | excluded | — |
| — | — | pg-28755: A 6 KB Gutenberg stub for The Hollow Needle; the full text is 4017. | — | — | excluded | — |
| — | — | ewald: Carl Ewald (31167, 31708, 35543, 62883, 62910, 62912, 65029): Ewald has his own shelf on another lane (ewald_shelf.json), which already holds five of these; the two it lacks (My Little Boy 35543, The Old Room 62883) are left for that shelf's owner. | — | — | excluded | — |

## Mary J. Serrano (Galdós, Pardo Bazán, Zola, Eça de Queirós)

Shelf: `pipeline/serrano_shelf.json` · fetch `python3 pipeline/fetch_shelf.py serrano` · titles `python3 pipeline/split_shelf_titles.py serrano`.
Round 19 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `serrano-bazan-a-wedding-trip` | Emilia Pardo Bazán | A Wedding Trip | Mary J. Serrano | 1889-1895 (see the Gutenberg header) | have | PG 54577 |
| `serrano-bazan-morrina-homesickness` | Emilia Pardo Bazán | Morriña (Homesickness) | Mary J. Serrano | 1889-1895 (see the Gutenberg header) | have | PG 54742 |
| `serrano-bazan-the-swan-of-vilamorta` | Emilia Pardo Bazán | The Swan of Vilamorta | Mary J. Serrano | 1889-1895 (see the Gutenberg header) | have | PG 54105 |
| `serrano-galdos-dona-perfecta` | Benito Pérez Galdós | Doña Perfecta | Mary J. Serrano | 1889-1895 (see the Gutenberg header) | have | PG 2462 |
| `serrano-queiros-dragon-s-teeth` | Eça de Queirós | Dragon's teeth | Mary J. Serrano | 1889-1895 (see the Gutenberg header) | have | PG 74442 |
| `serrano-zola-doctor-pascal` | Émile Zola | Doctor Pascal | Mary J. Serrano | 1889-1895 (see the Gutenberg header) | have | PG 10720 |

## Mary Howitt (Fredrika Bremer)

Shelf: `pipeline/mary-howitt_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mary-howitt` · titles `python3 pipeline/split_shelf_titles.py mary-howitt`.
Round 19 (2026-10-10), vetoable. Her Andersen is on andersen_shelf.json. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mary-howitt-bremer-strife-and-peace` | Fredrika Bremer | Strife and Peace | Mary Howitt | 1843-1844 (see the Gutenberg header) | have | PG 20156 |
| `mary-howitt-bremer-the-home-or-life-in-sweden` | Fredrika Bremer | The Home; Or, Life in Sweden | Mary Howitt | 1843-1844 (see the Gutenberg header) | have | PG 20746 |
| — | — | andersen: Andersen's True Story of My Life (7007) and Wonderful Stories for Children (43600) in her translation are already on andersen_shelf.json. | — | — | excluded | — |

## Lucie, Lady Duff Gordon (Meinhold's Amber Witch; The French in Algiers)

Shelf: `pipeline/duff-gordon_shelf.json` · fetch `python3 pipeline/fetch_shelf.py duff-gordon` · titles `python3 pipeline/split_shelf_titles.py duff-gordon`.
Round 19 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `duff-gordon-lamping-alby-the-french-in-algiers` | Clemens Lamping; Ernest Alby | The French in Algiers: The Soldier of the Foreign Legion; and The Prisoners of Abd-el-Kader | Lucie Duff Gordon | 1844-1845 (see the Gutenberg header) | have | PG 58081 |
| `duff-gordon-meinhold-mary-schweidler-the-amber-witch-the-most` | Wilhelm Meinhold | Mary Schweidler, the amber witch The most interesting trial for witchcraft ever known, printed from an imperfect manuscript by her father, Abraham Schweidler, the pastor of Coserow in the island of Usedom / edited by W. Meinhold ; translated from the German by Lady Duff Gordon. | Lucie Duff Gordon | 1844-1845 (see the Gutenberg header) | have | PG 8743 |

## Bernard Miall (Nexø's Pelle, Rolland's Tolstoy, Maeterlinck's Poems, Fabre)

Shelf: `pipeline/bernard-miall_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bernard-miall` · titles `python3 pipeline/split_shelf_titles.py bernard-miall`.
Round 20 (2026-10-10), vetoable. Only translations printed before 1931. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bernard-miall-brieux-woman-on-her-own-false-gods-and-the-red` | Eugène Brieux | Woman on Her Own, False Gods and The Red Robe | Bernard Miall (with J. B. Fagan and Charlotte Shaw) | 1911-1921 (see the Gutenberg header) | have | PG 27201 |
| `bernard-miall-calderon-latin-america-its-rise-and-progress` | Francisco García Calderón | Latin America: Its Rise and Progress | Bernard Miall | 1911-1921 (see the Gutenberg header) | have | PG 62541 |
| `bernard-miall-fabre-social-life-in-the-insect-world` | Jean-Henri Fabre | Social Life in the Insect World | Bernard Miall | 1911-1921 (see the Gutenberg header) | have | PG 18350 |
| `bernard-miall-fabre-the-life-of-jean-henri-fabre-the-entomol` | Augustin Fabre | The life of Jean Henri Fabre, the entomologist, 1823-1910 | Bernard Miall | 1911-1921 (see the Gutenberg header) | have | PG 72936 |
| `bernard-miall-legros-fabre-poet-of-science` | Georges Victor Legros | Fabre, Poet of Science | Bernard Miall | 1911-1921 (see the Gutenberg header) | have | PG 3489 |
| `bernard-miall-maeterlinck-poems` | Maurice Maeterlinck | Poems | Bernard Miall | 1911-1921 (see the Gutenberg header) | have | PG 50043 |
| `bernard-miall-martinez-the-argentine-in-the-twentieth-century` | Alberto B. Martínez | The Argentine in the Twentieth Century | Bernard Miall | 1911-1921 (see the Gutenberg header) | have | PG 45261 |
| `bernard-miall-massart-belgians-under-the-german-eagle` | Jean Massart | Belgians Under the German Eagle | Bernard Miall | 1911-1921 (see the Gutenberg header) | have | PG 51716 |
| `bernard-miall-nexo-pelle-the-conqueror` | Martin Andersen Nexø | Pelle the Conqueror (complete) | Bernard Miall (with Jessie Muir) | 1911-1921 (see the Gutenberg header) | have | PG 7795 |
| `bernard-miall-rolland-tolstoy` | Romain Rolland | Tolstoy | Bernard Miall | 1911-1921 (see the Gutenberg header) | have | PG 49435 |
| — | — | teixeira: The Wonders of Instinct (3754) and The Life of the Scorpion (66744), shared with Teixeira de Mattos, are on teixeira-de-mattos_shelf.json. | — | — | excluded | — |
| — | — | pelle-volumes: Pelle the Conqueror's four Gutenberg part-files (7791-7794) are left out; the complete text (7795) is used. | — | — | excluded | — |

## Jessie Muir (Jonas Lie, Bojer, Fleuron)

Shelf: `pipeline/jessie-muir_shelf.json` · fetch `python3 pipeline/fetch_shelf.py jessie-muir` · titles `python3 pipeline/split_shelf_titles.py jessie-muir`.
Round 20 (2026-10-10), vetoable. Her half of Pelle is on bernard-miall. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `jessie-muir-bojer-the-power-of-a-lie` | Johan Bojer | The Power of a Lie | Jessie Muir | 1894-1921 (see the Gutenberg header) | have | PG 58620 |
| `jessie-muir-fleuron-grim-the-story-of-a-pike` | Svend Fleuron | Grim: The Story of a Pike | Jessie Muir (with J. Alexander) | 1894-1921 (see the Gutenberg header) | have | PG 40921 |
| `jessie-muir-lie-one-of-life-s-slaves` | Jonas Lie | One of Life's Slaves | Jessie Muir | 1894-1921 (see the Gutenberg header) | have | PG 15853 |
| `jessie-muir-lie-the-visionary-pictures-from-nordland` | Jonas Lie | The Visionary: Pictures From Nordland | Jessie Muir | 1894-1921 (see the Gutenberg header) | have | PG 13922 |
| — | — | pelle: Pelle the Conqueror (7795 complete; part-files 7791, 7794) is on bernard-miall_shelf.json. | — | — | excluded | — |

## Sir Lascelles Wraxall (Aimard's frontier tales; the 1862 Les Misérables)

Shelf: `pipeline/wraxall_shelf.json` · fetch `python3 pipeline/fetch_shelf.py wraxall` · titles `python3 pipeline/split_shelf_titles.py wraxall`.
Round 20 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `wraxall-aimard-last-of-the-incas-a-romance-of-the-pampa` | Gustave Aimard | Last of the Incas: A Romance of the Pampas | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 44514 |
| `wraxall-aimard-stronghand-or-the-noble-revenge` | Gustave Aimard | Stronghand; or, The Noble Revenge | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 44672 |
| `wraxall-aimard-the-adventurers` | Gustave Aimard | The adventurers | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 43716 |
| `wraxall-aimard-the-bee-hunters-a-tale-of-adventure` | Gustave Aimard | The Bee Hunters: A Tale of Adventure | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 44375 |
| `wraxall-aimard-the-freebooters-a-story-of-the-texan-war` | Gustave Aimard | The Freebooters: A Story of the Texan War | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 40602 |
| `wraxall-aimard-the-gold-seekers-a-tale-of-california` | Gustave Aimard | The Gold-Seekers: A Tale of California | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 42532 |
| `wraxall-aimard-the-indian-chief-the-story-of-a-revoluti` | Gustave Aimard | The Indian Chief: The Story of a Revolution | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 42742 |
| `wraxall-aimard-the-indian-scout-a-story-of-the-aztec-ci` | Gustave Aimard | The Indian Scout: A Story of the Aztec City | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 44196 |
| `wraxall-aimard-the-pirates-of-the-prairies-adventures-i` | Gustave Aimard | The Pirates of the Prairies: Adventures in the American Desert | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 42117 |
| `wraxall-aimard-the-prairie-flower-a-tale-of-the-indian` | Gustave Aimard | The Prairie Flower: A Tale of the Indian Border | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 43925 |
| `wraxall-aimard-the-rebel-chief-a-tale-of-guerilla-life` | Gustave Aimard | The Rebel Chief: A Tale of Guerilla Life | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 44421 |
| `wraxall-aimard-the-red-track-a-story-of-social-life-in` | Gustave Aimard | The Red Track: A Story of Social Life in Mexico | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 42834 |
| `wraxall-aimard-the-smuggler-chief-a-novel` | Gustave Aimard | The Smuggler Chief: A Novel | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 44454 |
| `wraxall-aimard-the-tiger-slayer-a-tale-of-the-indian-de` | Gustave Aimard | The Tiger-Slayer: A Tale of the Indian Desert | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 42535 |
| `wraxall-aimard-the-trail-hunter-a-tale-of-the-far-west` | Gustave Aimard | The Trail-Hunter: A Tale of the Far West | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 42115 |
| `wraxall-aimard-the-trapper-s-daughter-a-story-of-the-ro` | Gustave Aimard | The Trapper's Daughter: A Story of the Rocky Mountains | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 42119 |
| `wraxall-aimard-the-trappers-of-arkansas-or-the-loyal-he` | Gustave Aimard | The Trappers of Arkansas; or, The Loyal Heart | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 43473 |
| `wraxall-aimard-the-treasure-of-pearls-a-romance-of-adve` | Gustave Aimard | The Treasure of Pearls: A Romance of Adventures in California | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 46276 |
| `wraxall-hugo-les-miserables-v-1-5-fantine` | Victor Hugo | Les Misérables, v. 1/5: Fantine | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 48731 |
| `wraxall-hugo-les-miserables-v-2-5-cosette` | Victor Hugo | Les Misérables, v. 2/5: Cosette | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 48732 |
| `wraxall-hugo-les-miserables-v-3-5-marius` | Victor Hugo | Les Misérables, v. 3/5: Marius | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 48733 |
| `wraxall-hugo-les-miserables-v-4-5-the-idyll-and-the-e` | Victor Hugo | Les Misérables, v. 4/5: The Idyll and the Epic | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 48734 |
| `wraxall-hugo-les-miserables-v-5-5-jean-valjean` | Victor Hugo | Les Misérables, v. 5/5: Jean Valjean | Lascelles Wraxall | 1861-1865 (see the Gutenberg header) | have | PG 48735 |

## Ernest Dowson (Les liaisons dangereuses; Balzac)

Shelf: `pipeline/dowson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py dowson` · titles `python3 pipeline/split_shelf_titles.py dowson`.
Round 20 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `dowson-balzac-a-passion-in-the-desert` | Honoré de Balzac | A Passion in the Desert | Ernest Dowson | 1896-1898 (see the Gutenberg header) | have | PG 1555 |
| `dowson-laclos-les-liaisons-dangereuses-volume-1-of-2` | Choderlos de Laclos | Les liaisons dangereuses, volume 1 (of 2) | Ernest Dowson | 1896-1898 (see the Gutenberg header) | have | PG 69891 |
| `dowson-laclos-les-liaisons-dangereuses-volume-2-of-2` | Choderlos de Laclos | Les liaisons dangereuses, volume 2 (of 2) | Ernest Dowson | 1896-1898 (see the Gutenberg header) | have | PG 69913 |

## Arthur Machen as translator (Casanova's Memoirs, 1894)

Shelf: `pipeline/machen-casanova_shelf.json` · fetch `python3 pipeline/fetch_shelf.py machen-casanova` · titles `python3 pipeline/split_shelf_titles.py machen-casanova`.
Round 21 (2026-10-10), vetoable. One complete text, not Gutenberg's 30 part-files. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `machen-casanova-casanova-the-memoirs-of-jacques-casanova-de-seing` | Giacomo Casanova | The Memoirs of Jacques Casanova de Seingalt, 1725-1798. Complete | Arthur Machen | 1894 (see the Gutenberg header) | have | PG 2981 |
| — | — | casanova-splits: Gutenberg's 30 part-files (2951-2980), the 6-volume set (39301-39306) and the quotes digest (7538) are left out; the complete text (2981) is used. | — | — | excluded | — |

## George Burnham Ives (George Sand, Daudet, Mérimée, Bourget)

Shelf: `pipeline/ives_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ives` · titles `python3 pipeline/split_shelf_titles.py ives`.
Round 21 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ives-aicard-king-of-camargue` | Jean Aicard | King of Camargue | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 33867 |
| `ives-balzac-honore-de-balzac` | Honoré de Balzac | Honoré de Balzac | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 51820 |
| `ives-bernard-geofroy-tory` | Auguste Bernard | Geofroy Tory | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 60542 |
| `ives-bourget-the-weight-of-the-name` | Paul Bourget | The weight of the name | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 68859 |
| `ives-daudet-the-nabob-vol-1-of-2` | Alphonse Daudet | The Nabob, Vol. 1 (of 2) | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 20646 |
| `ives-daudet-the-nabob-vol-2-of-2` | Alphonse Daudet | The Nabob, Vol. 2 (of 2) | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 21329 |
| `ives-kock-monsieur-cherami` | Paul de Kock | Monsieur Cherami | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 34338 |
| `ives-merimee-prosper-merimee-s-short-stories` | Prosper Mérimée | Prosper Mérimée's Short Stories | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 67643 |
| `ives-sand-antonia` | George Sand | Antonia | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 65170 |
| `ives-sand-indiana` | George Sand | Indiana | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 63445 |
| `ives-sand-les-beaux-messieurs-de-bois-dore-vol-1-o` | George Sand | Les beaux messieurs de Bois-Doré Vol. 1 (of 2) | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 69331 |
| `ives-sand-les-beaux-messieurs-de-bois-dore-vol-2-o` | George Sand | Les beaux messieurs de Bois-Doré Vol. 2 (of 2) | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 69332 |
| `ives-sand-she-and-he-lavinia-memoir` | George Sand | She and he; Lavinia; Memoir | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 68045 |
| `ives-sand-the-devil-s-pool` | George Sand | The Devil's Pool | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 12816 |
| `ives-sand-the-piccinino-volume-1-of-2` | George Sand | The Piccinino, Volume 1 (of 2) | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 69839 |
| `ives-sand-the-piccinino-volume-2-of-2-the-last-of` | George Sand | The Piccinino, Volume 2 (of 2); The last of Aldinis | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 69840 |
| `ives-sand-the-sin-of-monsieur-antoine-volume-1-of` | George Sand | The Sin of Monsieur Antoine, Volume 1 (of 2) | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 67460 |
| `ives-sand-the-sin-of-monsieur-antoine-volume-2-of` | George Sand | The Sin of Monsieur Antoine, Volume 2 (of 2) and Leone Leoni | George Burnham Ives | 1898-1909 (see the Gutenberg header) | have | PG 67461 |
| — | — | pg-28810: Gutenberg 28810 (The Devil's Pool) has no plain-text file; 12816 is used. | — | — | excluded | — |

## C. J. Hogarth (Tolstoy's trilogy, Dostoevsky, Oblomov, Turgenev)

Shelf: `pipeline/cj-hogarth_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cj-hogarth` · titles `python3 pipeline/split_shelf_titles.py cj-hogarth`.
Round 21 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cj-hogarth-andreyev-the-life-of-man-a-play-in-five-acts` | Leonid Andreyev | The Life of Man: A Play in Five Acts | C. J. Hogarth | 1912-1926 (see the Gutenberg header) | have | PG 49852 |
| `cj-hogarth-dostoyevsky-poor-folk` | Fyodor Dostoyevsky | Poor Folk | C. J. Hogarth | 1912-1926 (see the Gutenberg header) | have | PG 2302 |
| `cj-hogarth-dostoyevsky-the-gambler` | Fyodor Dostoyevsky | The Gambler | C. J. Hogarth | 1912-1926 (see the Gutenberg header) | have | PG 2197 |
| `cj-hogarth-goncharov-oblomov` | Ivan Goncharov | Oblomov | C. J. Hogarth | 1912-1926 (see the Gutenberg header) | have | PG 54700 |
| `cj-hogarth-gorky-through-russia` | Maksim Gorky | Through Russia | C. J. Hogarth | 1912-1926 (see the Gutenberg header) | have | PG 2288 |
| `cj-hogarth-melgunov-the-red-terror-in-russia` | Sergei Melgunov | The red terror in Russia | C. J. Hogarth | 1912-1926 (see the Gutenberg header) | have | PG 77104 |
| `cj-hogarth-tolstoy-boyhood` | Leo Tolstoy | Boyhood | C. J. Hogarth | 1912-1926 (see the Gutenberg header) | have | PG 2450 |
| `cj-hogarth-tolstoy-childhood` | Leo Tolstoy | Childhood | C. J. Hogarth | 1912-1926 (see the Gutenberg header) | have | PG 2142 |
| `cj-hogarth-tolstoy-youth` | Leo Tolstoy | Youth | C. J. Hogarth | 1912-1926 (see the Gutenberg header) | have | PG 2637 |
| `cj-hogarth-turgenev-fathers-and-sons` | Ivan Turgenev | Fathers and Sons | C. J. Hogarth | 1912-1926 (see the Gutenberg header) | have | PG 47935 |
| — | — | pg-19680: A second Gutenberg copy of Childhood; 2142 is used. | — | — | excluded | — |

## Herman Bernstein (Andreyev, Gorky, Chekhov)

Shelf: `pipeline/herman-bernstein_shelf.json` · fetch `python3 pipeline/fetch_shelf.py herman-bernstein` · titles `python3 pipeline/split_shelf_titles.py herman-bernstein`.
Round 21 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `herman-bernstein-andreyev-anathema-a-tragedy-in-seven-scenes` | Leonid Andreyev | Anathema: A Tragedy in Seven Scenes | Herman Bernstein | 1901-1922 (see the Gutenberg header) | have | PG 49606 |
| `herman-bernstein-andreyev-satan-s-diary` | Leonid Andreyev | Satan's Diary | Herman Bernstein | 1901-1922 (see the Gutenberg header) | have | PG 42665 |
| `herman-bernstein-andreyev-the-crushed-flower-and-other-stories` | Leonid Andreyev | The Crushed Flower, and Other Stories | Herman Bernstein | 1901-1922 (see the Gutenberg header) | have | PG 5779 |
| `herman-bernstein-andreyev-the-seven-who-were-hanged` | Leonid Andreyev | The Seven Who Were Hanged | Herman Bernstein | 1901-1922 (see the Gutenberg header) | have | PG 6722 |
| `herman-bernstein-andreyev-the-sorrows-of-belgium-a-play-in-six-sce` | Leonid Andreyev | The Sorrows of Belgium: A Play in Six Scenes | Herman Bernstein | 1901-1922 (see the Gutenberg header) | have | PG 49596 |
| `herman-bernstein-andreyev-the-waltz-of-the-dogs` | Leonid Andreyev | The waltz of the dogs | Herman Bernstein | 1901-1922 (see the Gutenberg header) | have | PG 78902 |
| `herman-bernstein-chekhov-the-slanderer` | Anton Chekhov | The Slanderer | Herman Bernstein | 1901-1922 (see the Gutenberg header) | have | PG 23055 |
| `herman-bernstein-gorky-the-man-who-was-afraid` | Maksim Gorky | The Man Who Was Afraid | Herman Bernstein | 1901-1922 (see the Gutenberg header) | have | PG 2709 |
| `herman-bernstein-turgenev-the-rendezvous` | Ivan Turgenev | The Rendezvous | Herman Bernstein | 1901-1922 (see the Gutenberg header) | have | PG 23056 |

## Eleanor Marx Aveling (Madame Bovary, Ibsen, Lissagaray)

Shelf: `pipeline/eleanor-marx-aveling_shelf.json` · fetch `python3 pipeline/fetch_shelf.py eleanor-marx-aveling` · titles `python3 pipeline/split_shelf_titles.py eleanor-marx-aveling`.
Round 21 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `eleanor-marx-aveling-flaubert-madame-bovary` | Gustave Flaubert | Madame Bovary | Eleanor Marx Aveling | 1886-1895 (see the Gutenberg header) | have | PG 2413 |
| `eleanor-marx-aveling-ibsen-the-lady-from-the-sea` | Henrik Ibsen | The Lady from the Sea | Eleanor Marx Aveling | 1886-1895 (see the Gutenberg header) | have | PG 2765 |
| `eleanor-marx-aveling-ibsen-the-wild-duck` | Henrik Ibsen | The wild duck | Eleanor Marx Aveling | 1886-1895 (see the Gutenberg header) | have | PG 73631 |
| `eleanor-marx-aveling-lissagaray-history-of-the-commune-of-1871` | Prosper-Olivier Lissagaray | History of the Commune of 1871 | Eleanor Marx Aveling | 1886-1895 (see the Gutenberg header) | have | PG 36043 |
| `eleanor-marx-aveling-plekhanov-anarchism-and-socialism` | Georgi Plekhanov | Anarchism and Socialism | Eleanor Marx Aveling | 1886-1895 (see the Gutenberg header) | have | PG 30506 |

## R. Nisbet Bain's fiction (Jókai, Jonas Lie, Gorky)

Shelf: `pipeline/bain-jokai_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bain-jokai` · titles `python3 pipeline/split_shelf_titles.py bain-jokai`.
Round 21 (2026-10-10), vetoable. His folk-tale books are on lane D's bain_shelf.json. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bain-jokai-gorky-tales-from-gorky` | Maksim Gorky | Tales from Gorky | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 56870 |
| `bain-jokai-jokai-a-hungarian-nabob` | Mór Jókai | A Hungarian Nabob | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 20978 |
| `bain-jokai-jokai-eyes-like-the-sea-a-novel` | Mór Jókai | Eyes Like the Sea: A Novel | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 31642 |
| `bain-jokai-jokai-halil-the-pedlar-a-tale-of-old-stambul` | Mór Jókai | Halil the Pedlar: A Tale of Old Stambul | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 17597 |
| `bain-jokai-jokai-midst-the-wild-carpathians` | Mór Jókai | 'Midst the Wild Carpathians | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 37339 |
| `bain-jokai-jokai-pretty-michal` | Mór Jókai | Pretty Michal | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 31886 |
| `bain-jokai-jokai-tales-from-jokai` | Mór Jókai | Tales From Jókai | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 37286 |
| `bain-jokai-jokai-the-day-of-wrath` | Mór Jókai | The Day of Wrath | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 23608 |
| `bain-jokai-jokai-the-lion-of-janina-or-the-last-days-of-t` | Mór Jókai | The Lion of Janina; Or, The Last Days of the Janissaries: A Turkish Novel | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 32234 |
| `bain-jokai-jokai-the-poor-plutocrats` | Mór Jókai | The Poor Plutocrats | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 18705 |
| `bain-jokai-jokai-the-slaves-of-the-padishah` | Mór Jókai | The Slaves of the Padishah | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 39048 |
| `bain-jokai-lie-weird-tales-from-northern-seas` | Jonas Lie | Weird Tales from Northern Seas | R. Nisbet Bain | 1893-1904 (see the Gutenberg header) | have | PG 13508 |
| — | — | folk-tales: Cossack Fairy Tales (29672), Polevoi's Russian Fairy Tales (34705) and Kúnos's Turkish Fairy Tales (64807) are on bain_shelf.json (lane D). | — | — | excluded | — |

## Mary J. Safford (Ebers, Felix Dahn, Mühlbach, Nordau)

Shelf: `pipeline/safford_shelf.json` · fetch `python3 pipeline/fetch_shelf.py safford` · titles `python3 pipeline/split_shelf_titles.py safford`.
Round 22 (2026-10-10), vetoable. Ebers complete texts only. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `safford-bashkirtseff-marie-bashkirtseff-from-childhood-to-gir` | Marie Bashkirtseff | Marie Bashkirtseff (From Childhood to Girlhood) | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 13916 |
| `safford-dahn-a-captive-of-the-roman-eagles` | Felix Dahn | A Captive of the Roman Eagles | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 32220 |
| `safford-dahn-felicitas-a-tale-of-the-german-migration` | Felix Dahn | Felicitas: A Tale of the German Migrations: A.D. 476 | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 32222 |
| `safford-dahn-the-scarlet-banner` | Felix Dahn | The Scarlet Banner | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 32461 |
| `safford-ebers-a-question` | Georg Ebers | A Question | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 5588 |
| `safford-ebers-a-word-only-a-word-complete` | Georg Ebers | A Word, Only a Word — Complete | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 5577 |
| `safford-ebers-arachne-complete` | Georg Ebers | Arachne — Complete | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 5516 |
| `safford-ebers-barbara-blomberg-complete` | Georg Ebers | Barbara Blomberg — Complete | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 5571 |
| `safford-ebers-cleopatra-complete` | Georg Ebers | Cleopatra — Complete | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 5482 |
| `safford-ebers-in-the-blue-pike-complete` | Georg Ebers | In the Blue Pike — Complete | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 5587 |
| `safford-ebers-in-the-fire-of-the-forge-a-romance-of-ol` | Georg Ebers | In the Fire of the Forge: A Romance of Old Nuremberg — Complete | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 5551 |
| `safford-ebers-joshua-complete` | Georg Ebers | Joshua — Complete | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 5472 |
| `safford-ebers-the-burgomaster-s-wife-complete` | Georg Ebers | The Burgomaster's Wife — Complete | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 5583 |
| `safford-ebers-the-story-of-my-life-complete` | Georg Ebers | The Story of My Life — Complete | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 5599 |
| `safford-eckstein-the-chaldean-magician` | Ernst Eckstein | The Chaldean Magician | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 59851 |
| `safford-hamerling-aspasia` | Robert Hamerling | Aspasia | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 76058 |
| `safford-heyse-the-romance-of-the-canoness-a-life-histo` | Paul Heyse | The Romance of the Canoness: A Life-History | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 33879 |
| `safford-hillern-on-the-cross-a-romance-of-the-passion-pl` | Wilhelmine von Hillern | On the Cross: A Romance of the Passion Play at Oberammergau | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 36725 |
| `safford-jokai-the-corsair-king` | Mór Jókai | The Corsair King | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 26865 |
| `safford-mariager-pictures-of-hellas-five-tales-of-ancient` | Peder Mariager | Pictures of Hellas: Five Tales of Ancient Greece | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 56929 |
| `safford-muhlbach-a-conspiracy-of-the-carbonari` | Luise Mühlbach | A Conspiracy of the Carbonari | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 16396 |
| `safford-nordau-soap-bubbles` | Max Nordau | Soap bubbles | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 77764 |
| `safford-nordau-the-dwarf-s-spectacles-and-other-fairy-t` | Max Nordau | The dwarf's spectacles, and other fairy tales | Mary J. Safford | 1880-1910 (see the Gutenberg header) | have | PG 77279 |
| — | — | ebers-volume-splits: Gutenberg's per-volume part-files of the Ebers novels are left out; the complete texts are used. | — | — | excluded | — |
| — | — | pg-5592: The Complete Short Works of Georg Ebers is a Gutenberg compilation with more than one translator; A Question (5588) is shelved singly. | — | — | excluded | — |

## Annis Lee Wister (Marlitt, E. Werner, Ossip Schubin)

Shelf: `pipeline/wister_shelf.json` · fetch `python3 pipeline/fetch_shelf.py wister` · titles `python3 pipeline/split_shelf_titles.py wister`.
Round 22 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `wister-bethusy-huc-the-eichhofs-a-romance` | Valeska Bethusy-Huc | The Eichhofs: A Romance | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 35311 |
| `wister-glumer-a-noble-name-or-donninghausen` | Claire von Glümer | A Noble Name; or, Dönninghausen | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 36550 |
| `wister-hillern-only-a-girl-or-a-physician-for-the-soul` | Wilhelmine von Hillern | Only a Girl: or, A Physician for the Soul. | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 36709 |
| `wister-marlitt-at-the-councillor-s-or-a-nameless-histor` | E. (Eugenie) Marlitt | At the Councillor's; or, A Nameless History | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 43393 |
| `wister-marlitt-gold-elsie` | E. (Eugenie) Marlitt | Gold Elsie | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 42426 |
| `wister-schubin-countess-erika-s-apprenticeship` | Ossip Schubin | Countess Erika's Apprenticeship | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 35531 |
| `wister-schubin-erlach-court` | Ossip Schubin | Erlach Court | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 35541 |
| `wister-schubin-o-thou-my-austria` | Ossip Schubin | "O Thou, My Austria!" | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 35454 |
| `wister-streckfuss-castle-hohenwald-a-romance` | Adolf Streckfuss | Castle Hohenwald: A Romance | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 34892 |
| `wister-streckfuss-quicksands` | Adolf Streckfuss | Quicksands | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 34953 |
| `wister-streckfuss-the-lonely-house` | Adolf Streckfuss | The Lonely House | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 34917 |
| `wister-streckfuss-too-rich-a-romance` | Adolf Streckfuss | Too Rich: A Romance | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 34995 |
| `wister-werner-saint-michael-a-romance` | E. Werner | Saint Michael: A Romance | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 35116 |
| `wister-werner-the-alpine-fay-a-romance` | E. Werner | The Alpine Fay: A Romance | Annis Lee Wister | 1868-1900 (see the Gutenberg header) | have | PG 35229 |

## A. R. Allinson (Anatole France, Brantôme, Fantômas)

Shelf: `pipeline/allinson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py allinson` · titles `python3 pipeline/split_shelf_titles.py allinson`.
Round 22 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `allinson-brantome-lives-of-fair-and-gallant-ladies-vol-1` | Pierre de Bourdeille, seigneur de Brantôme | Lives of Fair and Gallant Ladies. Vol 1 | A. R. Allinson | 1901-1924 (see the Gutenberg header) | have | PG 67025 |
| `allinson-brantome-lives-of-fair-and-gallant-ladies-vol-2` | Pierre de Bourdeille, seigneur de Brantôme | Lives of Fair and Gallant Ladies. Vol 2. | A. R. Allinson | 1901-1924 (see the Gutenberg header) | have | PG 67026 |
| `allinson-dumas-the-wolf-leader` | Alexandre Dumas | The Wolf-Leader | A. R. Allinson | 1901-1924 (see the Gutenberg header) | have | PG 51054 |
| `allinson-france-child-life-in-town-and-country` | Anatole France | Child Life in Town and Country | A. R. Allinson | 1901-1924 (see the Gutenberg header) | have | PG 25408 |
| `allinson-france-the-aspirations-of-jean-servien` | Anatole France | The Aspirations of Jean Servien | A. R. Allinson | 1901-1924 (see the Gutenberg header) | have | PG 11060 |
| `allinson-france-the-merrie-tales-of-jacques-tournebroche` | Anatole France | The Merrie Tales of Jacques Tournebroche | A. R. Allinson | 1901-1924 (see the Gutenberg header) | have | PG 25407 |
| `allinson-france-the-well-of-saint-clare` | Anatole France | The Well of Saint Clare | A. R. Allinson | 1901-1924 (see the Gutenberg header) | have | PG 18728 |
| `allinson-lemonnier-birds-and-beasts` | Camille Lemonnier | Birds and Beasts | A. R. Allinson | 1901-1924 (see the Gutenberg header) | have | PG 51847 |
| `allinson-souvestre-the-long-arm-of-fantomas` | Pierre Souvestre | The long arm of Fantômas | A. R. Allinson | 1901-1924 (see the Gutenberg header) | have | PG 71587 |

## W. W. Worster (Hamsun, Bojer, Gunnarsson)

Shelf: `pipeline/worster_shelf.json` · fetch `python3 pipeline/fetch_shelf.py worster` · titles `python3 pipeline/split_shelf_titles.py worster`.
Round 22 (2026-10-10), vetoable. Rasmussen and Lagerlöf left to their own shelves. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `worster-bojer-the-great-hunger` | Johan Bojer | The Great Hunger | W. W. Worster (with Charles Archer) | 1918-1923 (see the Gutenberg header) | have | PG 2943 |
| `worster-buchholtz-egholm-and-his-god` | Johannes Buchholtz | Egholm and his God | W. W. Worster | 1918-1923 (see the Gutenberg header) | have | PG 46913 |
| `worster-gunnarsson-guest-the-one-eyed` | Gunnar Gunnarsson | Guest the One-Eyed | W. W. Worster | 1918-1923 (see the Gutenberg header) | have | PG 62455 |
| `worster-hamsun-growth-of-the-soil` | Knut Hamsun | Growth of the Soil | W. W. Worster | 1918-1923 (see the Gutenberg header) | have | PG 10984 |
| `worster-hamsun-mothwise` | Knut Hamsun | Mothwise | W. W. Worster | 1918-1923 (see the Gutenberg header) | have | PG 46220 |
| `worster-hamsun-pan` | Knut Hamsun | Pan | W. W. Worster | 1918-1923 (see the Gutenberg header) | have | PG 7214 |
| `worster-hamsun-wanderers` | Knut Hamsun | Wanderers | W. W. Worster | 1918-1923 (see the Gutenberg header) | have | PG 7762 |
| `worster-nilsen-dry-fish-and-wet` | Anthon Bernhard Elias Nilsen (Elias Kræmmer) | Dry fish and wet | W. W. Worster | 1918-1923 (see the Gutenberg header) | have | PG 35918 |
| — | — | pg-28932: Rasmussen's Eskimo Folk-Tales is on rasmussen_shelf.json (another lane). | — | — | excluded | — |
| — | — | pg-71086: Lagerlöf's The Outcast (1922) is left for lagerlof_shelf.json (another lane), which does not hold it yet. | — | — | excluded | — |

## Arthur G. Chater (Amundsen, Nansen, Brandes, Hamsun)

Shelf: `pipeline/chater_shelf.json` · fetch `python3 pipeline/fetch_shelf.py chater` · titles `python3 pipeline/split_shelf_titles.py chater`.
Round 22 (2026-10-10), vetoable. One title is a 1930 Knopf printing. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `chater-amundsen-the-south-pole-an-account-of-the-norwegi` | Roald Amundsen | The South Pole; an account of the Norwegian Antarctic expedition in the "Fram," 1910-12 — Volume 1 and Volume 2 | Arthur G. Chater | 1911-1930 (see the Gutenberg header) | have | PG 4229 |
| `chater-brandes-friedrich-nietzsche` | Georg Brandes | Friedrich Nietzsche | Arthur G. Chater | 1911-1930 (see the Gutenberg header) | have | PG 47588 |
| `chater-duun-the-trough-of-the-wave` | Olav Duun | The trough of the wave | Arthur G. Chater | 1911-1930 (see the Gutenberg header) | have | PG 79140 |
| `chater-hamsun-victoria` | Knut Hamsun | Victoria | Arthur G. Chater | 1911-1930 (see the Gutenberg header) | have | PG 74458 |
| `chater-key-love-and-marriage` | Ellen Key | Love and Marriage | Arthur G. Chater | 1911-1930 (see the Gutenberg header) | have | PG 57592 |
| `chater-nansen-in-northern-mists-arctic-exploration-in-vol-1` | Fridtjof Nansen | In Northern Mists: Arctic Exploration in Early Times (Volume 1 of 2) | Arthur G. Chater | 1911-1930 (see the Gutenberg header) | have | PG 40633 |
| `chater-nansen-in-northern-mists-arctic-exploration-in-vol-2` | Fridtjof Nansen | In Northern Mists: Arctic Exploration in Early Times (Volume 2 of 2) | Arthur G. Chater | 1911-1930 (see the Gutenberg header) | have | PG 40634 |
| — | — | south-pole-volumes: The South Pole's two Gutenberg volume files (3414, 3415) are left out; 4229 holds both volumes. | — | — | excluded | — |

## Daniel De Leon (Sue's Mysteries of the People; Bebel)

Shelf: `pipeline/de-leon_shelf.json` · fetch `python3 pipeline/fetch_shelf.py de-leon` · titles `python3 pipeline/split_shelf_titles.py de-leon`.
Round 22 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `de-leon-bebel-woman-under-socialism` | August Bebel | Woman under socialism | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 30646 |
| `de-leon-sue-the-abbatial-crosier-or-bonaik-and-septi` | Eugène Sue | The Abbatial Crosier; or, Bonaik and Septimine. A Tale of a Medieval Abbess | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 33274 |
| `de-leon-sue-the-blacksmith-s-hammer-or-the-peasant-c` | Eugène Sue | The Blacksmith's Hammer; or, The Peasant Code: A Tale of the Grand Monarch | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 34987 |
| `de-leon-sue-the-branding-needle-or-the-monastery-of` | Eugène Sue | The Branding Needle; or, The Monastery of Charolles | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 33618 |
| `de-leon-sue-the-carlovingian-coins-or-the-daughters` | Eugène Sue | The Carlovingian Coins; Or, The Daughters of Charlemagne | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 33021 |
| `de-leon-sue-the-casque-s-lark-or-victoria-the-mother` | Eugène Sue | The Casque's Lark; or, Victoria, the Mother of the Camps | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 33868 |
| `de-leon-sue-the-executioner-s-knife-or-joan-of-arc` | Eugène Sue | The Executioner's Knife; Or, Joan of Arc | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 37399 |
| `de-leon-sue-the-galley-slave-s-ring-or-the-family-of` | Eugène Sue | The Galley Slave's Ring; or, The Family of Lebrenn | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 37225 |
| `de-leon-sue-the-gold-sickle-or-hena-the-virgin-of-th` | Eugène Sue | The Gold Sickle; Or, Hena, The Virgin of The Isle of Sen. A Tale of Druid Gaul | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 31752 |
| `de-leon-sue-the-infant-s-skull-or-the-end-of-the-wor` | Eugène Sue | The Infant's Skull; Or, The End of the World. A Tale of the Millennium | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 31759 |
| `de-leon-sue-the-iron-arrow-head-or-the-buckler-maide` | Eugène Sue | The Iron Arrow Head or The Buckler Maiden: A Tale of the Northman Invasion | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 34452 |
| `de-leon-sue-the-iron-pincers-or-mylio-and-karvel-a-t` | Eugène Sue | The Iron Pincers; or, Mylio and Karvel: A Tale of the Albigensian Crusades | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 33114 |
| `de-leon-sue-the-iron-trevet-or-jocelyn-the-champion` | Eugène Sue | The Iron Trevet; or, Jocelyn the Champion: A Tale of the Jacquerie | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 34390 |
| `de-leon-sue-the-pilgrim-s-shell-or-fergan-the-quarry` | Eugène Sue | The Pilgrim's Shell; Or, Fergan the Quarryman: A Tale from the Feudal Times | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 34531 |
| `de-leon-sue-the-pocket-bible-or-christian-the-printe` | Eugène Sue | The Pocket Bible; or, Christian the Printer: A Tale of the Sixteenth Century | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 35067 |
| `de-leon-sue-the-poniard-s-hilt-or-karadeucq-and-rona` | Eugène Sue | The Poniard's Hilt; Or, Karadeucq and Ronan. A Tale of Bagauders and Vagres | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 31782 |
| `de-leon-sue-the-silver-cross-or-the-carpenter-of-naz` | Eugène Sue | The Silver Cross; Or, The Carpenter of Nazareth | Daniel De Leon | 1904-1911 (see the Gutenberg header) | have | PG 32743 |
| `de-leon-sue-the-sword-of-honor-or-the-foundation-of` | Eugène Sue | The Sword of Honor; or, The Foundation of the French Republic | Daniel De Leon (with Solon De Leon) | 1904-1911 (see the Gutenberg header) | have | PG 35633 |

## George P. Upton (McClurg's Life Stories for Young People; Nohl's composer lives)

Shelf: `pipeline/upton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py upton` · titles `python3 pipeline/split_shelf_titles.py upton`.
Round 23 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `upton-becker-achilles` | Karl Friedrich Becker | Achilles | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 62453 |
| `upton-becker-ulysses-of-ithaca` | Karl Friedrich Becker | Ulysses of Ithaca | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 59750 |
| `upton-campe-christopher-columbus` | Joachim Heinrich Campe | Christopher Columbus | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 62366 |
| `upton-campe-hernando-cortes` | Joachim Heinrich Campe | Hernando Cortes | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 59732 |
| `upton-henning-the-maid-of-orleans` | Friedrich Henning | The Maid of Orleans | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 65431 |
| `upton-hocker-arnold-of-winkelried-the-hero-of-sempach` | Gustav Höcker | Arnold of Winkelried, the Hero of Sempach | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 59751 |
| `upton-hoffmann-ludwig-van-beethoven` | Franz Hoffmann | Ludwig Van Beethoven | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 62742 |
| `upton-hoffmann-mozart-s-youth` | Franz Hoffmann | Mozart's Youth | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 65302 |
| `upton-hoffmann-the-little-dauphin` | Franz Hoffmann | The Little Dauphin | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 62650 |
| `upton-horn-maria-theresa` | W. O. von Horn | Maria Theresa | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 62527 |
| `upton-jeanrenaud-the-duke-of-brittany` | Henriette Jeanrenaud | The Duke of Brittany | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 60257 |
| `upton-kemper-maximilian-in-mexico` | J. Kemper | Maximilian in Mexico | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 62449 |
| `upton-kuchler-elizabeth-empress-of-austria-and-queen-o` | Carl Küchler | Elizabeth, Empress of Austria and Queen of Hungary | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 60408 |
| `upton-kuchler-queen-maria-sophia-of-naples-a-forgotten` | Carl Küchler | Queen Maria Sophia of Naples, a Forgotten Heroine | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 65606 |
| `upton-kuhn-barbarossa` | Franz Kühn | Barbarossa | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 65142 |
| `upton-merz-louise-queen-of-prussia` | Heinrich Merz | Louise, Queen of Prussia | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 65549 |
| `upton-muller-memories-a-story-of-german-love` | F. Max (Friedrich Max) Müller | Memories: A Story of German Love | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 14521 |
| `upton-nohl-life-of-haydn` | Ludwig Nohl | Life of Haydn | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 67827 |
| `upton-nohl-life-of-liszt` | Ludwig Nohl | Life of Liszt | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 68522 |
| `upton-nohl-life-of-wagner` | Ludwig Nohl | Life of Wagner | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 31526 |
| `upton-oertel-william-penn` | Hugo Oertel | William Penn | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 62656 |
| `upton-plehn-emin-pasha` | M. C. Plehn | Emin Pasha | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 59691 |
| `upton-schmidt-charlemagne` | Ferdinand Schmidt | Charlemagne | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 59882 |
| `upton-schmidt-george-washington` | Ferdinand Schmidt | George Washington | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 60236 |
| `upton-schmidt-gods-and-heroes` | Ferdinand Schmidt | Gods and Heroes | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 59956 |
| `upton-schmidt-gudrun` | Ferdinand Schmidt | Gudrun | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 59626 |
| `upton-schmidt-the-nibelungs` | Ferdinand Schmidt | The Nibelungs | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 73227 |
| `upton-schmidt-the-youth-of-the-great-elector` | Ferdinand Schmidt | The Youth of the Great Elector | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 59929 |
| `upton-schrader-frederick-the-great-and-the-seven-years` | Ferdinand Schrader | Frederick the Great and the Seven Years' War | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 65827 |
| `upton-tegner-the-frithiof-saga` | Esaias Tegnér | The Frithiof Saga | George P. Upton (with Ferdinand Schmidt) | 1875-1911 (see the Gutenberg header) | have | PG 59689 |
| `upton-tschudi-eugenie-empress-of-the-french` | Clara Tschudi | Eugenie, Empress of the French | George P. Upton (with Erich Holm) | 1875-1911 (see the Gutenberg header) | have | PG 62965 |
| `upton-walter-emperor-william-first-the-great-war-and` | A. Walter | Emperor William First, the Great War and Peace Hero | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 62451 |
| `upton-willys-swiss-heroes-an-historical-romance-of-th` | A. A. Willys | Swiss Heroes: An Historical Romance of the Time of Charles the Bold | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 61788 |
| `upton-wurdig-prince-eugene-the-noble-knight` | L. (Ludwig) Würdig | Prince Eugene, the Noble Knight | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 59733 |
| `upton-ziemssen-johann-sebastian-bach` | Ludwig Ziemssen | Johann Sebastian Bach | George P. Upton | 1875-1911 (see the Gutenberg header) | have | PG 65747 |

## Grace Isabel Colbron (Groner's Joe Muller detective stories)

Shelf: `pipeline/colbron_shelf.json` · fetch `python3 pipeline/fetch_shelf.py colbron` · titles `python3 pipeline/split_shelf_titles.py colbron`.
Round 23 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `colbron-groner-the-case-of-the-golden-bullet` | Auguste Groner | The Case of the Golden Bullet | Grace Isabel Colbron | 1910 (see the Gutenberg header) | have | PG 1836 |
| `colbron-groner-the-case-of-the-lamp-that-went-out` | Auguste Groner | The Case of the Lamp That Went Out | Grace Isabel Colbron | 1910 (see the Gutenberg header) | have | PG 1832 |
| `colbron-groner-the-case-of-the-pocket-diary-found-in-th` | Auguste Groner | The Case of the Pocket Diary Found in the Snow | Grace Isabel Colbron | 1910 (see the Gutenberg header) | have | PG 1834 |
| `colbron-groner-the-case-of-the-pool-of-blood-in-the-pas` | Auguste Groner | The Case of the Pool of Blood in the Pastor's Study | Grace Isabel Colbron | 1910 (see the Gutenberg header) | have | PG 1835 |
| `colbron-groner-the-case-of-the-registered-letter` | Auguste Groner | The Case of the Registered Letter | Grace Isabel Colbron | 1910 (see the Gutenberg header) | have | PG 1833 |

## Isaac Goldberg (Baroja, Blasco Ibáñez, Brazilian Tales, Gourmont, Pinski)

Shelf: `pipeline/isaac-goldberg_shelf.json` · fetch `python3 pipeline/fetch_shelf.py isaac-goldberg` · titles `python3 pipeline/split_shelf_titles.py isaac-goldberg`.
Round 23 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `isaac-goldberg-baroja-the-quest` | Pío Baroja | The Quest | Isaac Goldberg | 1917-1927 (see the Gutenberg header) | have | PG 8496 |
| `isaac-goldberg-baroja-weeds` | Pío Baroja | Weeds | Isaac Goldberg | 1917-1927 (see the Gutenberg header) | have | PG 61183 |
| `isaac-goldberg-brazilian-tales` | Various Brazilian authors (Machado de Assis and others) | Brazilian Tales | Isaac Goldberg | 1917-1927 (see the Gutenberg header) | have | PG 21040 |
| `isaac-goldberg-gourmont-philosophic-nights-in-paris` | Remy de Gourmont | Philosophic Nights in Paris | Isaac Goldberg | 1917-1927 (see the Gutenberg header) | have | PG 46759 |
| `isaac-goldberg-gourmont-stories-in-green-zinzolin-rose-purple-ma` | Remy de Gourmont | Stories in green, zinzolin, rose, purple, mauve, lilac and orange | Isaac Goldberg | 1917-1927 (see the Gutenberg header) | have | PG 79446 |
| `isaac-goldberg-gourmont-stories-in-yellow-black-white-blue-viole` | Remy de Gourmont | Stories in yellow, black, white, blue, violet and red | Isaac Goldberg | 1917-1927 (see the Gutenberg header) | have | PG 78436 |
| `isaac-goldberg-ibanez-luna-benamor` | Vicente Blasco Ibáñez | Luna Benamor | Isaac Goldberg | 1917-1927 (see the Gutenberg header) | have | PG 21870 |
| `isaac-goldberg-ibanez-the-torrent-entre-naranjos` | Vicente Blasco Ibáñez | The Torrent (Entre Naranjos) | Isaac Goldberg (with Arthur Livingston) | 1917-1927 (see the Gutenberg header) | have | PG 11674 |
| `isaac-goldberg-pinski-temptations` | David Pinski | Temptations | Isaac Goldberg | 1917-1927 (see the Gutenberg header) | have | PG 71439 |

## Thomas Roscoe (Lanzi's History of Painting in Italy; Pellico)

Shelf: `pipeline/thomas-roscoe_shelf.json` · fetch `python3 pipeline/fetch_shelf.py thomas-roscoe` · titles `python3 pipeline/split_shelf_titles.py thomas-roscoe`.
Round 23 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `thomas-roscoe-lanzi-the-history-of-painting-in-italy-vol-1-o` | Luigi Lanzi | The History of Painting in Italy, Vol. 1 (of 6) | Thomas Roscoe | 1824-1853 (see the Gutenberg header) | have | PG 34479 |
| `thomas-roscoe-lanzi-the-history-of-painting-in-italy-vol-2-o` | Luigi Lanzi | The History of Painting in Italy, Vol. 2 (of 6) | Thomas Roscoe | 1824-1853 (see the Gutenberg header) | have | PG 34585 |
| `thomas-roscoe-lanzi-the-history-of-painting-in-italy-vol-3-o` | Luigi Lanzi | The History of Painting in Italy, Vol. 3 (of 6) | Thomas Roscoe | 1824-1853 (see the Gutenberg header) | have | PG 34645 |
| `thomas-roscoe-lanzi-the-history-of-painting-in-italy-vol-4-o` | Luigi Lanzi | The History of Painting in Italy, Vol. 4 (of 6) | Thomas Roscoe | 1824-1853 (see the Gutenberg header) | have | PG 38967 |
| `thomas-roscoe-lanzi-the-history-of-painting-in-italy-vol-5-o` | Luigi Lanzi | The History of Painting in Italy, Vol. 5 (of 6) | Thomas Roscoe | 1824-1853 (see the Gutenberg header) | have | PG 39996 |
| `thomas-roscoe-lanzi-the-history-of-painting-in-italy-vol-6-o` | Luigi Lanzi | The History of Painting in Italy, Vol. 6 (of 6) | Thomas Roscoe | 1824-1853 (see the Gutenberg header) | have | PG 41533 |
| `thomas-roscoe-pellico-my-ten-years-imprisonment` | Silvio Pellico | My Ten Years' Imprisonment | Thomas Roscoe | 1824-1853 (see the Gutenberg header) | have | PG 2792 |
| `thomas-roscoe-tales-of-humour-gallantry-romance` | Various European authors (selected; with J. Y. Akerman) | Tales of Humour, Gallantry & Romance, Selected and Translated from the Italian | Thomas Roscoe (with John Yonge Akerman) | 1824-1853 (see the Gutenberg header) | have | PG 44561 |

## John Durand (Taine's Origins of Contemporary France; Philosophy of Art)

Shelf: `pipeline/durand_shelf.json` · fetch `python3 pipeline/fetch_shelf.py durand` · titles `python3 pipeline/split_shelf_titles.py durand`.
Round 23 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `durand-taine-the-ancient-regime` | Hippolyte Taine | The Ancient Regime | John Durand | 1865-1894 (see the Gutenberg header) | have | PG 2577 |
| `durand-taine-the-french-revolution-volume-1` | Hippolyte Taine | The French Revolution - Volume 1 | John Durand | 1865-1894 (see the Gutenberg header) | have | PG 2578 |
| `durand-taine-the-french-revolution-volume-2` | Hippolyte Taine | The French Revolution - Volume 2 | John Durand | 1865-1894 (see the Gutenberg header) | have | PG 2579 |
| `durand-taine-the-french-revolution-volume-3` | Hippolyte Taine | The French Revolution - Volume 3 | John Durand | 1865-1894 (see the Gutenberg header) | have | PG 2580 |
| `durand-taine-the-modern-regime-volume-1` | Hippolyte Taine | The Modern Regime, Volume 1 | John Durand | 1865-1894 (see the Gutenberg header) | have | PG 2581 |
| `durand-taine-the-modern-regime-volume-2` | Hippolyte Taine | The Modern Regime, Volume 2 | John Durand | 1865-1894 (see the Gutenberg header) | have | PG 2582 |
| `durand-taine-the-philosophy-of-art` | Hippolyte Taine | The Philosophy of Art | John Durand | 1865-1894 (see the Gutenberg header) | have | PG 52980 |
| — | — | pg-23524: Gutenberg's combined table of contents for the Origins, not a text. | — | — | excluded | — |

## Charles Timothy Brooks (Goethe's Faust; Jean Paul)

Shelf: `pipeline/ct-brooks_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ct-brooks` · titles `python3 pipeline/split_shelf_titles.py ct-brooks`.
Round 23 (2026-10-10), vetoable. His Busch stays on wilhelm-busch. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ct-brooks-goethe-faust-a-tragedy-part-1-translated-from-t` | Johann Wolfgang von Goethe | Faust: a Tragedy [part 1], Translated from the German of Goethe | Charles Timothy Brooks | 1856-1883 (see the Gutenberg header) | have | PG 14460 |
| `ct-brooks-jean-paul-hesperus-vol-1` | Jean Paul | Hesperus; or, Forty-Five Dog-Post-Days: A Biography. Vol. I. | Charles Timothy Brooks | 1856-1883 (see the Gutenberg header) | have | PG 36071 |
| `ct-brooks-jean-paul-hesperus-vol-2` | Jean Paul | Hesperus; or, Forty-Five Dog-Post-Days: A Biography. Vol. II. | Charles Timothy Brooks | 1856-1883 (see the Gutenberg header) | have | PG 36087 |
| `ct-brooks-jean-paul-the-invisible-lodge` | Jean Paul | The Invisible Lodge | Charles Timothy Brooks | 1856-1883 (see the Gutenberg header) | have | PG 36353 |
| `ct-brooks-jean-paul-titan-a-romance-v-1-of-2` | Jean Paul | Titan: A Romance. v. 1 (of 2) | Charles Timothy Brooks | 1856-1883 (see the Gutenberg header) | have | PG 35664 |
| `ct-brooks-jean-paul-titan-a-romance-v-2-of-2` | Jean Paul | Titan: A Romance. v. 2 (of 2) | Charles Timothy Brooks | 1856-1883 (see the Gutenberg header) | have | PG 36403 |
| — | — | busch: Max and Maurice (28847) is on wilhelm-busch_shelf.json; Plish and Plum (37188) is left for that shelf's owner. | — | — | excluded | — |

## Lady Wallace (Mozart, Beethoven and Mendelssohn letters; Auerbach)

Shelf: `pipeline/lady-wallace_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lady-wallace` · titles `python3 pipeline/split_shelf_titles.py lady-wallace`.
Round 23 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lady-wallace-auerbach-joseph-in-the-snow-vol-1` | Berthold Auerbach | Joseph in the Snow, and The Clockmaker. In Three Volumes. Vol. I. | Lady Wallace | 1862-1867 (see the Gutenberg header) | have | PG 33162 |
| `lady-wallace-auerbach-joseph-in-the-snow-vol-2` | Berthold Auerbach | Joseph in the Snow, and The Clockmaker. In Three Volumes. Vol. II. | Lady Wallace | 1862-1867 (see the Gutenberg header) | have | PG 33163 |
| `lady-wallace-auerbach-joseph-in-the-snow-vol-3` | Berthold Auerbach | Joseph in the Snow, and The Clockmaker. In Three Volumes. Vol. III. | Lady Wallace | 1862-1867 (see the Gutenberg header) | have | PG 33164 |
| `lady-wallace-beethoven-beethoven-s-letters-1790-1826-volume-1` | Ludwig van Beethoven | Beethoven's Letters 1790-1826, Volume 1 | Lady Wallace | 1862-1867 (see the Gutenberg header) | have | PG 13065 |
| `lady-wallace-beethoven-beethoven-s-letters-1790-1826-volume-2` | Ludwig van Beethoven | Beethoven's Letters 1790-1826, Volume 2 | Lady Wallace | 1862-1867 (see the Gutenberg header) | have | PG 13272 |
| `lady-wallace-mendelssohn-letters-1833-1847` | Felix Mendelssohn-Bartholdy | Letters of Felix Mendelssohn-Bartholdy from 1833 to 1847 | Lady Wallace | 1862-1867 (see the Gutenberg header) | have | PG 50473 |
| `lady-wallace-mendelssohn-letters-italy-switzerland` | Felix Mendelssohn-Bartholdy | Letters of Felix Mendelssohn Bartholdy from Italy and Switzerland | Lady Wallace | 1862-1867 (see the Gutenberg header) | have | PG 39384 |
| `lady-wallace-mozart-the-letters-of-wolfgang-amadeus-mozart-v` | Wolfgang Amadeus Mozart | The Letters of Wolfgang Amadeus Mozart — Volume 01 | Lady Wallace | 1862-1867 (see the Gutenberg header) | have | PG 5307 |

## Ellen E. Frewer (Verne's Dick Sands; Schweinfurth; Holub)

Shelf: `pipeline/frewer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py frewer` · titles `python3 pipeline/split_shelf_titles.py frewer`.
Round 23 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `frewer-cahun-the-adventures-of-captain-mago-or-a-phoe` | David-Léon Cahun | The adventures of Captain Mago; or, a Phoenician expedition, B.C. 1000 | Ellen E. Frewer | 1873-1881 (see the Gutenberg header) | have | PG 47582 |
| `frewer-holub-seven-years-in-south-africa-volume-1-of` | Emil Holub | Seven years in South Africa, volume 1 (of 2) | Ellen E. Frewer | 1873-1881 (see the Gutenberg header) | have | PG 74281 |
| `frewer-holub-seven-years-in-south-africa-volume-2-of` | Emil Holub | Seven years in South Africa, volume 2 (of 2) | Ellen E. Frewer | 1873-1881 (see the Gutenberg header) | have | PG 74291 |
| `frewer-schweinfurth-the-heart-of-africa-vol-1-of-2` | Georg August Schweinfurth | The heart of Africa, Vol. 1 (of 2) | Ellen E. Frewer | 1873-1881 (see the Gutenberg header) | have | PG 71621 |
| `frewer-schweinfurth-the-heart-of-africa-vol-2-of-2` | Georg August Schweinfurth | The heart of Africa, Vol. 2 (of 2) | Ellen E. Frewer | 1873-1881 (see the Gutenberg header) | have | PG 71622 |
| `frewer-verne-dick-sands-the-boy-captain` | Jules Verne | Dick Sands, the Boy Captain | Ellen E. Frewer | 1873-1881 (see the Gutenberg header) | have | PG 9150 |

## Laura Ensor (Loti, Daudet, Maupassant)

Shelf: `pipeline/laura-ensor_shelf.json` · fetch `python3 pipeline/fetch_shelf.py laura-ensor` · titles `python3 pipeline/split_shelf_titles.py laura-ensor`.
Round 23 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `laura-ensor-daudet-artists-wives` | Alphonse Daudet | Artists' Wives | Laura Ensor | 1887-1896 (see the Gutenberg header) | have | PG 22522 |
| `laura-ensor-daudet-robert-helmont-diary-of-a-recluse-1870-1` | Alphonse Daudet | Robert Helmont: Diary of a Recluse, 1870-1871 | Laura Ensor | 1887-1896 (see the Gutenberg header) | have | PG 51235 |
| `laura-ensor-loti-madame-chrysantheme` | Pierre Loti | Madame Chrysanthème | Laura Ensor | 1887-1896 (see the Gutenberg header) | have | PG 15335 |
| `laura-ensor-massalska-memoirs-of-the-princesse-de-ligne-vol-1` | Apolonia Helena Massalska | Memoirs of the Princesse de Ligne, Vol. 1 (of 2) | Laura Ensor | 1887-1896 (see the Gutenberg header) | have | PG 71048 |
| `laura-ensor-massalska-memoirs-of-the-princesse-de-ligne-vol-2` | Apolonia Helena Massalska | Memoirs of the Princesse de Ligne, Vol. 2 (of 2) | Laura Ensor | 1887-1896 (see the Gutenberg header) | have | PG 71051 |
| `laura-ensor-maupassant-afloat-sur-l-eau` | Guy de Maupassant | Afloat (Sur l'eau) | Laura Ensor | 1887-1896 (see the Gutenberg header) | have | PG 49318 |

## Dora Knowlton Ranous (D'Annunzio's The Flame; Zibeline)

Shelf: `pipeline/ranous_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ranous` · titles `python3 pipeline/split_shelf_titles.py ranous`.
Round 23 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ranous-d-annunzio-the-flame` | Gabriele D'Annunzio | The Flame | Dora Knowlton Ranous | 1900-1906 (see the Gutenberg header) | have | PG 60601 |
| `ranous-massa-zibeline-complete` | Philippe Massa | Zibeline — Complete | Dora Knowlton Ranous | 1900-1906 (see the Gutenberg header) | have | PG 3934 |
| — | — | zibeline-volumes: Zibeline's three Gutenberg volume files are left out; the complete text (3934) is used. | — | — | excluded | — |

## Eden and Cedar Paul (Zweig, Rolland, Schnitzler, Emil Ludwig)

Shelf: `pipeline/eden-cedar-paul_shelf.json` · fetch `python3 pipeline/fetch_shelf.py eden-cedar-paul` · titles `python3 pipeline/split_shelf_titles.py eden-cedar-paul`.
Round 24 (2026-10-10), vetoable. Sexology titles left out by judgment. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `eden-cedar-paul-engel-the-elements-of-child-protection` | Sigmund Engel | The Elements of Child-protection | Eden Paul | 1915-1929 (see the Gutenberg header) | have | PG 58787 |
| `eden-cedar-paul-kurella-cesare-lombroso-a-modern-man-of-science` | Hans Kurella | Cesare Lombroso, a modern man of science | Eden Paul | 1915-1929 (see the Gutenberg header) | have | PG 61423 |
| `eden-cedar-paul-loria-karl-marx` | Achille Loria | Karl Marx | Eden and Cedar Paul | 1915-1929 (see the Gutenberg header) | have | PG 48446 |
| `eden-cedar-paul-ludwig-diana` | Emil Ludwig | Diana | Eden and Cedar Paul | 1915-1929 (see the Gutenberg header) | have | PG 77479 |
| `eden-cedar-paul-ludwig-napoleon` | Emil Ludwig | Napoleon | Eden and Cedar Paul | 1915-1929 (see the Gutenberg header) | have | PG 79253 |
| `eden-cedar-paul-riou-the-diary-of-a-french-private-war-impris` | Gaston Riou | The Diary of a French Private: War-Imprisonment, 1914-1915 | Eden and Cedar Paul | 1915-1929 (see the Gutenberg header) | have | PG 57287 |
| `eden-cedar-paul-rolland-the-forerunners` | Romain Rolland | The Forerunners | Eden and Cedar Paul | 1915-1929 (see the Gutenberg header) | have | PG 31313 |
| `eden-cedar-paul-schnitzler-casanova-s-homecoming` | Arthur Schnitzler | Casanova's Homecoming | Eden and Cedar Paul | 1915-1929 (see the Gutenberg header) | have | PG 9310 |
| `eden-cedar-paul-zweig-jeremiah-a-drama-in-nine-scenes` | Stefan Zweig | Jeremiah: A Drama in Nine Scenes | Eden and Cedar Paul | 1915-1929 (see the Gutenberg header) | have | PG 39402 |
| `eden-cedar-paul-zweig-romain-rolland-the-man-and-his-work` | Stefan Zweig | Romain Rolland: The Man and His Work | Eden and Cedar Paul | 1915-1929 (see the Gutenberg header) | have | PG 34888 |
| — | — | sexology: Left out by lane C's judgment, not for rights: A Young Girl's Diary (752), Moll's The Sexual Life of the Child (28402), Bloch's The Sexual Life of Our Time (60968) and Kisch's The Sexual Life of Woman (63274), medical and psychoanalytic works of the 1910s-20s. Adam can ask for them. | — | — | excluded | — |

## T. Bailey Saunders (Schopenhauer's essays; Goethe's Maxims)

Shelf: `pipeline/bailey-saunders_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bailey-saunders` · titles `python3 pipeline/split_shelf_titles.py bailey-saunders`.
Round 24 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bailey-saunders-goethe-maxims-and-reflections` | Johann Wolfgang von Goethe | Maxims and Reflections | T. Bailey Saunders | 1889-1896 (see the Gutenberg header) | have | PG 33670 |
| `bailey-saunders-schopenhauer-the-essays-of-arthur-schopenhauer-counse` | Arthur Schopenhauer | The Essays of Arthur Schopenhauer; Counsels and Maxims | T. Bailey Saunders | 1889-1896 (see the Gutenberg header) | have | PG 10715 |
| `bailey-saunders-schopenhauer-the-essays-of-arthur-schopenhauer-on-hum` | Arthur Schopenhauer | The Essays of Arthur Schopenhauer; On Human Nature | T. Bailey Saunders | 1889-1896 (see the Gutenberg header) | have | PG 10739 |
| `bailey-saunders-schopenhauer-the-essays-of-arthur-schopenhauer-religi` | Arthur Schopenhauer | The Essays of Arthur Schopenhauer; Religion, a Dialogue, Etc. | T. Bailey Saunders | 1889-1896 (see the Gutenberg header) | have | PG 10833 |
| `bailey-saunders-schopenhauer-the-essays-of-arthur-schopenhauer-studie` | Arthur Schopenhauer | The Essays of Arthur Schopenhauer; Studies in Pessimism | T. Bailey Saunders | 1889-1896 (see the Gutenberg header) | have | PG 10732 |
| `bailey-saunders-schopenhauer-the-essays-of-arthur-schopenhauer-the-ar` | Arthur Schopenhauer | The Essays of Arthur Schopenhauer; The Art of Literature | T. Bailey Saunders | 1889-1896 (see the Gutenberg header) | have | PG 10714 |
| `bailey-saunders-schopenhauer-the-essays-of-arthur-schopenhauer-the-ar-pg10731` | Arthur Schopenhauer | The Essays of Arthur Schopenhauer; the Art of Controversy | T. Bailey Saunders | 1889-1896 (see the Gutenberg header) | have | PG 10731 |
| `bailey-saunders-schopenhauer-the-essays-of-arthur-schopenhauer-the-wi` | Arthur Schopenhauer | The Essays of Arthur Schopenhauer: the Wisdom of Life | T. Bailey Saunders | 1889-1896 (see the Gutenberg header) | have | PG 10741 |
| — | — | pg-26586: A second Gutenberg copy of Studies in Pessimism; 10732 is used. | — | — | excluded | — |

## Joseph McCabe (Haeckel, Voltaire, Ferrer)

Shelf: `pipeline/mccabe_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mccabe` · titles `python3 pipeline/split_shelf_titles.py mccabe`.
Round 24 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mccabe-bolsche-haeckel` | Wilhelm Bölsche | Haeckel | Joseph McCabe | 1900-1922 (see the Gutenberg header) | have | PG 70451 |
| `mccabe-guardia-the-origin-and-ideals-of-the-modern-scho` | Francisco Ferrer Guardia | The Origin and Ideals of the Modern School | Joseph McCabe | 1900-1922 (see the Gutenberg header) | have | PG 66644 |
| `mccabe-haeckel-last-words-on-evolution-a-popular-retros` | Ernst Haeckel | Last Words on Evolution: A Popular Retrospect and Summary | Joseph McCabe | 1900-1922 (see the Gutenberg header) | have | PG 53639 |
| `mccabe-haeckel-the-evolution-of-man-volume-1` | Ernst Haeckel | The Evolution of Man — Volume 1 | Joseph McCabe | 1900-1922 (see the Gutenberg header) | have | PG 6430 |
| `mccabe-haeckel-the-evolution-of-man-volume-2` | Ernst Haeckel | The Evolution of Man — Volume 2 | Joseph McCabe | 1900-1922 (see the Gutenberg header) | have | PG 6710 |
| `mccabe-haeckel-the-riddle-of-the-universe-at-the-close` | Ernst Haeckel | The Riddle of the Universe at the close of the nineteenth century | Joseph McCabe | 1900-1922 (see the Gutenberg header) | have | PG 42968 |
| `mccabe-haeckel-the-wonders-of-life-a-popular-study-of-b` | Ernst Haeckel | The Wonders of Life: A Popular Study of Biological Philosophy | Joseph McCabe | 1900-1922 (see the Gutenberg header) | have | PG 46652 |
| `mccabe-nordmann-einstein-and-the-universe-a-popular-expo` | Charles Nordmann | Einstein and the universe: A popular exposition of the famous theory | Joseph McCabe | 1900-1922 (see the Gutenberg header) | have | PG 68462 |
| `mccabe-voltaire-toleration-and-other-essays` | Voltaire | Toleration and other essays | Joseph McCabe | 1900-1922 (see the Gutenberg header) | have | PG 64858 |

## R. Farquharson Sharp (Ibsen and Bjørnson for Everyman)

Shelf: `pipeline/farquharson-sharp_shelf.json` · fetch `python3 pipeline/fetch_shelf.py farquharson-sharp` · titles `python3 pipeline/split_shelf_titles.py farquharson-sharp`.
Round 24 (2026-10-10), vetoable. A Doll's House held on adler_shelf.json. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `farquharson-sharp-bjornson-three-comedies` | Bjørnstjerne Bjørnson | Three Comedies | R. Farquharson Sharp | 1910-1915 (Everyman's Library; see the Gutenberg header) | have | PG 7366 |
| `farquharson-sharp-bjornson-three-dramas` | Bjørnstjerne Bjørnson | Three Dramas | R. Farquharson Sharp | 1910-1915 (Everyman's Library; see the Gutenberg header) | have | PG 7844 |
| `farquharson-sharp-ibsen-a-doll-s-house` | Henrik Ibsen | A Doll's House | R. Farquharson Sharp | 1910 (Everyman's Library) | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `ibsen-dollshouse` (PG 2542) |
| `farquharson-sharp-ibsen-an-enemy-of-the-people` | Henrik Ibsen | An Enemy of the People | R. Farquharson Sharp | 1910-1915 (Everyman's Library; see the Gutenberg header) | have | PG 2446 |
| `farquharson-sharp-ibsen-ghosts-a-domestic-tragedy-in-three-acts` | Henrik Ibsen | Ghosts: A Domestic Tragedy in Three Acts | R. Farquharson Sharp | 1910-1915 (Everyman's Library; see the Gutenberg header) | have | PG 2467 |
| `farquharson-sharp-ibsen-pillars-of-society` | Henrik Ibsen | Pillars of Society | R. Farquharson Sharp | 1910-1915 (Everyman's Library; see the Gutenberg header) | have | PG 2296 |
| `farquharson-sharp-ibsen-rosmersholm` | Henrik Ibsen | Rosmersholm | R. Farquharson Sharp | 1910-1915 (Everyman's Library; see the Gutenberg header) | have | PG 2289 |
| — | — | pg-15492: A 1920s Haldeman-Julius reprint of A Doll's House; the Everyman text is used. | — | — | excluded | — |
| — | — | pg-2542: A Doll's House (2542) is on adler_shelf.json; a cross-reference title points to it. | — | — | excluded | — |

## Mary Morison (Brandes's Main Currents and Shakespeare; Bjørnson)

Shelf: `pipeline/mary-morison_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mary-morison` · titles `python3 pipeline/split_shelf_titles.py mary-morison`.
Round 24 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mary-morison-bjornson-mary` | Bjørnstjerne Bjørnson | Mary | Mary Morison | 1898-1909 (see the Gutenberg header) | have | PG 33300 |
| `mary-morison-brandes-main-currents-vol-1` | Georg Brandes | Main Currents in Nineteenth Century Literature - 1. The Emigrant Literature | Mary Morison (with Diana White) | 1898-1909 (see the Gutenberg header) | have | PG 47675 |
| `mary-morison-brandes-main-currents-vol-2` | Georg Brandes | Main Currents in Nineteenth Century Literature - 2. The Romantic School in Germany | Mary Morison (with Diana White) | 1898-1909 (see the Gutenberg header) | have | PG 47781 |
| `mary-morison-brandes-main-currents-vol-3` | Georg Brandes | Main Currents in Nineteenth Century Literature - 3. The Reaction in France | Mary Morison (with Diana White) | 1898-1909 (see the Gutenberg header) | have | PG 47794 |
| `mary-morison-brandes-main-currents-vol-4` | Georg Brandes | Main Currents in Nineteenth Century Literature - 4. Naturalism in England | Mary Morison (with Diana White) | 1898-1909 (see the Gutenberg header) | have | PG 47892 |
| `mary-morison-brandes-main-currents-vol-5` | Georg Brandes | Main Currents in Nineteenth Century Literature - 5. The Romantic School in France | Mary Morison (with Diana White) | 1898-1909 (see the Gutenberg header) | have | PG 47950 |
| `mary-morison-brandes-main-currents-vol-6` | Georg Brandes | Main Currents in Nineteenth Century Literature - 6. Young Germany | Mary Morison (with Diana White) | 1898-1909 (see the Gutenberg header) | have | PG 48042 |
| `mary-morison-brandes-william-shakespeare-a-critical-study` | Georg Brandes | William Shakespeare: A Critical Study | Mary Morison (with William Archer, Diana White) | 1898-1909 (see the Gutenberg header) | have | PG 50724 |

## Diana White (Dubois's Timbuctoo)

Shelf: `pipeline/diana-white_shelf.json` · fetch `python3 pipeline/fetch_shelf.py diana-white` · titles `python3 pipeline/split_shelf_titles.py diana-white`.
Round 24 (2026-10-10), vetoable. Her Brandes is on mary-morison. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `diana-white-dubois-timbuctoo-the-mysterious` | Félix Dubois | Timbuctoo the mysterious | Diana White | 1896 (see the Gutenberg header) | have | PG 78611 |
| — | — | brandes: Her Brandes volumes with Mary Morison are on mary-morison_shelf.json. | — | — | excluded | — |

## Robert Black (Guizot's Popular History of France)

Shelf: `pipeline/robert-black_shelf.json` · fetch `python3 pipeline/fetch_shelf.py robert-black` · titles `python3 pipeline/split_shelf_titles.py robert-black`.
Round 24 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `robert-black-guizot-a-popular-history-of-france-from-the-ear` | François Guizot | A Popular History of France from the Earliest Times | Robert Black | 1869-1881 (see the Gutenberg header) | have | PG 28879 |
| — | — | guizot-volumes: The six Gutenberg volume files (11951-11956) are left out; the complete text (28879) is used. | — | — | excluded | — |

## E. M. Waller (Dumas's My Memoirs; Mérimée)

Shelf: `pipeline/waller_shelf.json` · fetch `python3 pipeline/fetch_shelf.py waller` · titles `python3 pipeline/split_shelf_titles.py waller`.
Round 24 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `waller-dumas-my-memoirs-vol-i-1802-to-1821` | Alexandre Dumas | My Memoirs, Vol. I, 1802 to 1821 | E. M. Waller | 1903-1909 (see the Gutenberg header) | have | PG 49678 |
| `waller-dumas-my-memoirs-vol-ii-1822-to-1825` | Alexandre Dumas | My Memoirs, Vol. II, 1822 to 1825 | E. M. Waller | 1903-1909 (see the Gutenberg header) | have | PG 50113 |
| `waller-dumas-my-memoirs-vol-iii-1826-to-1830` | Alexandre Dumas | My Memoirs, Vol. III, 1826 to 1830 | E. M. Waller | 1903-1909 (see the Gutenberg header) | have | PG 50426 |
| `waller-dumas-my-memoirs-vol-iv-1830-to-1831` | Alexandre Dumas | My Memoirs, Vol. IV, 1830 to 1831 | E. M. Waller | 1903-1909 (see the Gutenberg header) | have | PG 50630 |
| `waller-dumas-my-memoirs-vol-v-1831-to-1832` | Alexandre Dumas | My Memoirs, Vol. V, 1831 to 1832 | E. M. Waller | 1903-1909 (see the Gutenberg header) | have | PG 50768 |
| `waller-dumas-my-memoirs-vol-vi-1832-to-1833` | Alexandre Dumas | My Memoirs, Vol. VI, 1832 to 1833 | E. M. Waller | 1903-1909 (see the Gutenberg header) | have | PG 51105 |
| `waller-merimee-abbe-aubain-and-mosaics` | Prosper Mérimée | Abbé Aubain and Mosaics | E. M. Waller | 1903-1909 (see the Gutenberg header) | have | PG 35004 |

## Fred Rothwell (Bergson's Laughter; Schuré)

Shelf: `pipeline/rothwell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rothwell` · titles `python3 pipeline/split_shelf_titles.py rothwell`.
Round 24 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rothwell-bergson-laughter-an-essay-on-the-meaning-of-the` | Henri Bergson | Laughter: An Essay on the Meaning of the Comic | Fred Rothwell (with Cloudesley Brereton) | 1910-1923 (see the Gutenberg header) | have | PG 4352 |
| `rothwell-ohnet-the-woman-of-mystery` | Georges Ohnet | The woman of mystery | Fred Rothwell | 1910-1923 (see the Gutenberg header) | have | PG 69149 |
| `rothwell-pascal-reincarnation-a-study-in-human-evolution` | Théophile Pascal | Reincarnation: A Study in Human Evolution | Fred Rothwell | 1910-1923 (see the Gutenberg header) | have | PG 21533 |
| `rothwell-roujon-battles-bivouacs-a-french-soldier-s-note` | Jacques Roujon | Battles & Bivouacs: A French soldier's note-book | Fred Rothwell | 1910-1923 (see the Gutenberg header) | have | PG 58231 |
| `rothwell-schure-pythagoras-and-the-delphic-mysteries` | Edouard Schuré | Pythagoras and the Delphic mysteries | Fred Rothwell | 1910-1923 (see the Gutenberg header) | have | PG 76522 |

## Sir Clements Markham (Hakluyt Society: Cieza de León, Quirós, Vespucci; Lazarillo)

Shelf: `pipeline/markham_shelf.json` · fetch `python3 pipeline/fetch_shelf.py markham` · titles `python3 pipeline/split_shelf_titles.py markham`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `markham-anonymous-the-life-of-lazarillo-de-tormes` | Anonymous | The Life of Lazarillo de Tormes | Clements R. Markham | 1864-1918 (see the Gutenberg header) | have | PG 53489 |
| `markham-leon-the-travels-of-pedro-de-cieza-de-leon-a` | Pedro de Cieza de León | The travels of Pedro de Cieza de Léon, A.D. 1532-50, | Clements R. Markham | 1864-1918 (see the Gutenberg header) | have | PG 48770 |
| `markham-leon-the-travels-of-pedro-de-cieza-de-leon-pa` | Pedro de Cieza de León | The travels of Pedro de Cieza de Léon; part 2 | Clements R. Markham | 1864-1918 (see the Gutenberg header) | have | PG 48785 |
| `markham-leon-the-war-of-chupas` | Pedro de Cieza de León | The War of Chupas | Clements R. Markham | 1864-1918 (see the Gutenberg header) | have | PG 56486 |
| `markham-leon-the-war-of-quito` | Pedro de Cieza de León | The War of Quito | Clements R. Markham | 1864-1918 (see the Gutenberg header) | have | PG 49095 |
| `markham-queiros-the-voyages-of-pedro-fernandez-de-quiros` | Pedro Fernandes de Queirós | The Voyages of Pedro Fernandez de Quiros, 1595 to 1606. Volume 1 | Clements R. Markham | 1864-1918 (see the Gutenberg header) | have | PG 41200 |
| `markham-vespucci-the-letters-of-amerigo-vespucci-and-othe` | Amerigo Vespucci | The Letters of Amerigo Vespucci, and Other Documents Illustrative of His Career | Clements R. Markham | 1864-1918 (see the Gutenberg header) | have | PG 36924 |

## Thomasina Ross (Humboldt's Personal Narrative; Tschudi; Bouterwek)

Shelf: `pipeline/thomasina-ross_shelf.json` · fetch `python3 pipeline/fetch_shelf.py thomasina-ross` · titles `python3 pipeline/split_shelf_titles.py thomasina-ross`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `thomasina-ross-bouterwek-spanish-portuguese-literature-vol-1` | Friedrich Bouterwek | History of Spanish and Portuguese Literature (Vol 1 of 2) | Thomasina Ross | 1823-1853 (see the Gutenberg header) | have | PG 55829 |
| `thomasina-ross-bouterwek-spanish-portuguese-literature-vol-2` | Friedrich Bouterwek | History of Spanish and Portuguese Literature (Vol 2 of 2) | Thomasina Ross | 1823-1853 (see the Gutenberg header) | have | PG 56396 |
| `thomasina-ross-castro-el-buscapie` | Adolfo de Castro | El Buscapié | Thomasina Ross | 1823-1853 (see the Gutenberg header) | have | PG 64011 |
| `thomasina-ross-humboldt-personal-narrative-vol-1` | Alexander von Humboldt | Personal Narrative of Travels to the Equinoctial Regions of America, During the Year 1799-1804 — Volume 1 | Thomasina Ross | 1823-1853 (see the Gutenberg header) | have | PG 6322 |
| `thomasina-ross-humboldt-personal-narrative-vol-2` | Alexander von Humboldt | Personal Narrative of Travels to the Equinoctial Regions of America, During the Year 1799-1804 — Volume 2 | Thomasina Ross | 1823-1853 (see the Gutenberg header) | have | PG 7014 |
| `thomasina-ross-humboldt-personal-narrative-vol-3` | Alexander von Humboldt | Personal Narrative of Travels to the Equinoctial Regions of America, During the Year 1799-1804 — Volume 3 | Thomasina Ross | 1823-1853 (see the Gutenberg header) | have | PG 7254 |
| `thomasina-ross-tschudi-travels-in-peru-on-the-coast-in-the-sier` | Johann Jakob von Tschudi | Travels in Peru, on the Coast, in the Sierra, Across the Cordilleras and the Andes, into the Primeval Forests | Thomasina Ross | 1823-1853 (see the Gutenberg header) | have | PG 26745 |

## Henry Llewellyn Williams (Dumas's Marie Antoinette romances; Aimard)

Shelf: `pipeline/hl-williams_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hl-williams` · titles `python3 pipeline/split_shelf_titles.py hl-williams`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hl-williams-aimard-the-red-river-half-breed-a-tale-of-the-w` | Gustave Aimard | The Red River Half-Breed: A Tale of the Wild North-West | Henry Llewellyn Williams | 1878-1900 (see the Gutenberg header) | have | PG 45047 |
| `hl-williams-dumas-balsamo-the-magician-or-the-memoirs-of-a` | Alexandre Dumas | Balsamo, the magician; or, the memoirs of a physician | Henry Llewellyn Williams | 1878-1900 (see the Gutenberg header) | have | PG 45822 |
| `hl-williams-dumas-the-countess-of-charny-or-the-execution` | Alexandre Dumas | The Countess of Charny; or, The Execution of King Louis XVI | Henry Llewellyn Williams | 1878-1900 (see the Gutenberg header) | have | PG 42757 |
| `hl-williams-dumas-the-hero-of-the-people-a-historical-roma` | Alexandre Dumas | The Hero of the People: A Historical Romance of Love, Liberty and Loyalty | Henry Llewellyn Williams | 1878-1900 (see the Gutenberg header) | have | PG 42681 |
| `hl-williams-dumas-the-mesmerist-s-victim` | Alexandre Dumas | The Mesmerist's Victim | Henry Llewellyn Williams | 1878-1900 (see the Gutenberg header) | have | PG 42690 |
| `hl-williams-dumas-the-royal-life-guard-or-the-flight-of-th` | Alexandre Dumas | The Royal Life Guard; or, the flight of the royal family. | Henry Llewellyn Williams | 1878-1900 (see the Gutenberg header) | have | PG 43633 |

## Beatrice Marshall (Sudermann; Karin Michaëlis)

Shelf: `pipeline/beatrice-marshall_shelf.json` · fetch `python3 pipeline/fetch_shelf.py beatrice-marshall` · titles `python3 pipeline/split_shelf_titles.py beatrice-marshall`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `beatrice-marshall-michaelis-elsie-lindtner` | Karin Michaëlis | Elsie Lindtner | Beatrice Marshall | 1898-1912 (see the Gutenberg header) | have | PG 68837 |
| `beatrice-marshall-sudermann-john-the-baptist-a-play` | Hermann Sudermann | John the Baptist: A Play | Beatrice Marshall | 1898-1912 (see the Gutenberg header) | have | PG 34383 |
| `beatrice-marshall-sudermann-regina-or-the-sins-of-the-fathers` | Hermann Sudermann | Regina, or the Sins of the Fathers | Beatrice Marshall | 1898-1912 (see the Gutenberg header) | have | PG 33892 |
| `beatrice-marshall-sudermann-the-song-of-songs` | Hermann Sudermann | The Song of Songs | Beatrice Marshall | 1898-1912 (see the Gutenberg header) | have | PG 34361 |
| `beatrice-marshall-sudermann-the-undying-past` | Hermann Sudermann | The Undying Past | Beatrice Marshall | 1898-1912 (see the Gutenberg header) | have | PG 34156 |

## Alys Hallard (the Goncourts, Gyp, Doumic)

Shelf: `pipeline/alys-hallard_shelf.json` · fetch `python3 pipeline/fetch_shelf.py alys-hallard` · titles `python3 pipeline/split_shelf_titles.py alys-hallard`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `alys-hallard-buffin-brave-belgians` | Camille Buffin | Brave Belgians | Alys Hallard | 1896-1915 (see the Gutenberg header) | have | PG 58509 |
| `alys-hallard-doumic-george-sand-some-aspects-of-her-life-and` | René Doumic | George Sand: Some Aspects of Her Life and Writings | Alys Hallard | 1896-1915 (see the Gutenberg header) | have | PG 138 |
| `alys-hallard-goncourt-renee-mauperin` | Edmond de Goncourt | Renée Mauperin | Alys Hallard | 1896-1915 (see the Gutenberg header) | have | PG 24604 |
| `alys-hallard-gyp-bijou` | Gyp | Bijou | Alys Hallard | 1896-1915 (see the Gutenberg header) | have | PG 36199 |

## Bertha Ness (E. Werner; Gottschall)

Shelf: `pipeline/bertha-ness_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bertha-ness` · titles `python3 pipeline/split_shelf_titles.py bertha-ness`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bertha-ness-gottschall-withered-leaves-a-novel-vol-1-of-3` | Rudolf von Gottschall | Withered Leaves: A Novel. Vol. 1 (of 3) | Bertha Ness | 1875-1885 (see the Gutenberg header) | have | PG 35371 |
| `bertha-ness-gottschall-withered-leaves-a-novel-vol-2-of-3` | Rudolf von Gottschall | Withered Leaves: A Novel.  Vol. 2 (of 3) | Bertha Ness | 1875-1885 (see the Gutenberg header) | have | PG 35372 |
| `bertha-ness-gottschall-withered-leaves-a-novel-vol-3-of-3` | Rudolf von Gottschall | Withered Leaves: A Novel. Vol. 3 (of 3) | Bertha Ness | 1875-1885 (see the Gutenberg header) | have | PG 35373 |
| `bertha-ness-werner-riven-bonds-vol-i` | E. Werner | Riven Bonds. Vol. I. | Bertha Ness | 1875-1885 (see the Gutenberg header) | have | PG 35283 |
| `bertha-ness-werner-riven-bonds-vol-ii` | E. Werner | Riven Bonds.  Vol. II. | Bertha Ness | 1875-1885 (see the Gutenberg header) | have | PG 35284 |

## M. W. Macdowall (Fritz Reuter; Franzos; Wägner)

Shelf: `pipeline/macdowall_shelf.json` · fetch `python3 pipeline/fetch_shelf.py macdowall` · titles `python3 pipeline/split_shelf_titles.py macdowall`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `macdowall-franzos-the-jews-of-barnow-stories` | Karl Emil Franzos | The Jews of Barnow: Stories | M. W. Macdowall | 1878-1883 (see the Gutenberg header) | have | PG 34617 |
| `macdowall-reuter-an-old-story-of-my-farming-days-vol-1-of` | Fritz Reuter | An Old Story of My Farming Days Vol. 1 (of 3). | M. W. Macdowall | 1878-1883 (see the Gutenberg header) | have | PG 35849 |
| `macdowall-reuter-an-old-story-of-my-farming-days-vol-2-of` | Fritz Reuter | An Old Story of My Farming Days Vol. 2 (of 3). | M. W. Macdowall | 1878-1883 (see the Gutenberg header) | have | PG 35850 |
| `macdowall-reuter-an-old-story-of-my-farming-days-vol-3-of` | Fritz Reuter | An Old Story of My Farming Days Vol. 3 (of 3). | M. W. Macdowall | 1878-1883 (see the Gutenberg header) | have | PG 35851 |
| `macdowall-wagner-epics-and-romances-of-the-middle-ages` | Wilhelm Wägner | Epics and Romances of the Middle Ages | M. W. Macdowall | 1878-1883 (see the Gutenberg header) | have | PG 46923 |

## R. P. Gillies (Hoffmann's Devil's Elixir; Fouqué's Magic Ring)

Shelf: `pipeline/gillies_shelf.json` · fetch `python3 pipeline/fetch_shelf.py gillies` · titles `python3 pipeline/split_shelf_titles.py gillies`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `gillies-hoffmann-the-devil-s-elixir-vol-1-of-2` | E. T. A. (Ernst Theodor Amadeus) Hoffmann | The Devil's Elixir, Vol. 1 (of 2) | R. P. Gillies | 1824-1825 (see the Gutenberg header) | have | PG 36494 |
| `gillies-hoffmann-the-devil-s-elixir-vol-2-of-2` | E. T. A. (Ernst Theodor Amadeus) Hoffmann | The Devil's Elixir, Vol. 2 (of 2) | R. P. Gillies | 1824-1825 (see the Gutenberg header) | have | PG 37005 |
| `gillies-motte-fouque-the-magic-ring-vol-1-of-3` | Friedrich Heinrich Karl La Motte-Fouqué | The magic ring, Vol. 1 (of 3) | R. P. Gillies | 1824-1825 (see the Gutenberg header) | have | PG 77097 |
| `gillies-motte-fouque-the-magic-ring-vol-2-of-3` | Friedrich Heinrich Karl La Motte-Fouqué | The magic ring, Vol. 2 (of 3) | R. P. Gillies | 1824-1825 (see the Gutenberg header) | have | PG 77098 |
| `gillies-motte-fouque-the-magic-ring-vol-3-of-3` | Friedrich Heinrich Karl La Motte-Fouqué | The magic ring, Vol. 3 (of 3) | R. P. Gillies | 1824-1825 (see the Gutenberg header) | have | PG 77099 |

## Christina Tyrrell (E. Werner)

Shelf: `pipeline/christina-tyrrell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py christina-tyrrell` · titles `python3 pipeline/split_shelf_titles.py christina-tyrrell`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `christina-tyrrell-werner-fickle-fortune` | E. Werner | Fickle Fortune | Christina Tyrrell | 1876-1886 (see the Gutenberg header) | have | PG 39194 |
| `christina-tyrrell-werner-no-surrender` | E. Werner | No Surrender | Christina Tyrrell | 1876-1886 (see the Gutenberg header) | have | PG 35096 |
| `christina-tyrrell-werner-success-and-how-he-won-it` | E. Werner | Success and How He Won It | Christina Tyrrell | 1876-1886 (see the Gutenberg header) | have | PG 35032 |
| `christina-tyrrell-werner-under-a-charm-a-novel-vol-i` | E. Werner | Under a Charm: A Novel. Vol. I | Christina Tyrrell | 1876-1886 (see the Gutenberg header) | have | PG 35251 |
| `christina-tyrrell-werner-under-a-charm-a-novel-vol-ii` | E. Werner | Under a Charm: A Novel. Vol. II | Christina Tyrrell | 1876-1886 (see the Gutenberg header) | have | PG 35252 |
| `christina-tyrrell-werner-under-a-charm-a-novel-vol-iii` | E. Werner | Under a Charm: A Novel. Vol. III | Christina Tyrrell | 1876-1886 (see the Gutenberg header) | have | PG 35253 |

## N. D'Anvers, i.e. Nancy Bell (Verne; Nadaillac; Plauchut)

Shelf: `pipeline/d-anvers_shelf.json` · fetch `python3 pipeline/fetch_shelf.py d-anvers` · titles `python3 pipeline/split_shelf_titles.py d-anvers`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `d-anvers-hourst-french-enterprise-in-africa` | Hourst | French enterprise in Africa | N. D'Anvers | 1873-1899 (see the Gutenberg header) | have | PG 71649 |
| `d-anvers-nadaillac-manners-and-monuments-of-prehistoric-peo` | Jean-François-Albert du Pouget Nadaillac | Manners and Monuments of Prehistoric Peoples | N. D'Anvers | 1873-1899 (see the Gutenberg header) | have | PG 3309 |
| `d-anvers-plauchut-china-and-the-chinese` | Edmond Plauchut | China and the Chinese | N. D'Anvers | 1873-1899 (see the Gutenberg header) | have | PG 63733 |
| `d-anvers-verne-celebrated-travels-and-travellers-part-3` | Jules Verne | Celebrated Travels and Travellers, Part 3. | N. D'Anvers | 1873-1899 (see the Gutenberg header) | have | PG 26658 |
| `d-anvers-verne-the-blockade-runners` | Jules Verne | The Blockade Runners | N. D'Anvers | 1873-1899 (see the Gutenberg header) | have | PG 8992 |
| `d-anvers-verne-the-fur-country-or-seventy-degrees-north` | Jules Verne | The Fur Country: Or, Seventy Degrees North Latitude | N. D'Anvers | 1873-1899 (see the Gutenberg header) | have | PG 8991 |

## Arthur Livingston (Blasco Ibáñez, Quiroga, Farrère)

Shelf: `pipeline/livingston_shelf.json` · fetch `python3 pipeline/fetch_shelf.py livingston` · titles `python3 pipeline/split_shelf_titles.py livingston`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `livingston-farrere-the-house-of-the-secret-la-maison-des-ho` | Claude Farrère | The House of the Secret (La maison des hommes vivants) | Arthur Livingston | 1917-1923 (see the Gutenberg header) | have | PG 65709 |
| `livingston-ibanez-mayflower-flor-de-mayo-a-tale-of-the-val` | Vicente Blasco Ibáñez | Mayflower (Flor de mayo): A Tale of the Valencian Seashore | Arthur Livingston | 1917-1923 (see the Gutenberg header) | have | PG 29577 |
| `livingston-montessori-the-montessori-elementary-material` | Maria Montessori | The Montessori Elementary Material | Arthur Livingston | 1917-1923 (see the Gutenberg header) | have | PG 42869 |
| `livingston-quiroga-south-american-jungle-tales` | Horacio Quiroga | South American Jungle Tales | Arthur Livingston | 1917-1923 (see the Gutenberg header) | have | PG 46051 |
| — | — | pg-11674: The Torrent (with Isaac Goldberg) is on isaac-goldberg_shelf.json. | — | — | excluded | — |

## Barrett H. Clark (Rostand, Rolland and other French plays)

Shelf: `pipeline/barrett-clark_shelf.json` · fetch `python3 pipeline/fetch_shelf.py barrett-clark` · titles `python3 pipeline/split_shelf_titles.py barrett-clark`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `barrett-clark-bernard-french-without-a-master` | Tristan Bernard | French without a master | Barrett H. Clark | 1914-1918 (see the Gutenberg header) | have | PG 70884 |
| `barrett-clark-bouchor-a-christmas-tale-in-one-act` | Maurice Bouchor | A Christmas Tale: in One Act | Barrett H. Clark | 1914-1918 (see the Gutenberg header) | have | PG 61613 |
| `barrett-clark-pailleron-the-art-of-being-bored-a-comedy-in-three` | Edouard Pailleron | The Art of Being Bored: A Comedy in Three Acts | Barrett H. Clark | 1914-1918 (see the Gutenberg header) | have | PG 53334 |
| `barrett-clark-rolland-the-fourteenth-of-july-and-danton-two-pl` | Romain Rolland | The Fourteenth of July, and Danton: Two Plays of the French Revolution | Barrett H. Clark | 1914-1918 (see the Gutenberg header) | have | PG 49438 |
| `barrett-clark-rostand-the-romancers-a-comedy-in-three-acts` | Edmond Rostand | The Romancers: A Comedy in Three Acts | Barrett H. Clark | 1914-1918 (see the Gutenberg header) | have | PG 17581 |

## E. M. Lamond (Grisar's Luther, 6 vols)

Shelf: `pipeline/lamond_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lamond` · titles `python3 pipeline/split_shelf_titles.py lamond`.
Round 25 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lamond-grisar-luther-vol-1-of-6` | Hartmann Grisar | Luther, vol. 1 of 6 | E. M. Lamond | 1913-1917 (see the Gutenberg header) | have | PG 48995 |
| `lamond-grisar-luther-vol-2-of-6` | Hartmann Grisar | Luther, vol. 2 of 6 | E. M. Lamond | 1913-1917 (see the Gutenberg header) | have | PG 49065 |
| `lamond-grisar-luther-vol-3-of-6` | Hartmann Grisar | Luther, vol. 3 of 6 | E. M. Lamond | 1913-1917 (see the Gutenberg header) | have | PG 49106 |
| `lamond-grisar-luther-vol-4-of-6` | Hartmann Grisar | Luther, vol. 4 of 6 | E. M. Lamond | 1913-1917 (see the Gutenberg header) | have | PG 49135 |
| `lamond-grisar-luther-vol-5-of-6` | Hartmann Grisar | Luther, vol. 5 of 6 | E. M. Lamond | 1913-1917 (see the Gutenberg header) | have | PG 49171 |
| `lamond-grisar-luther-vol-6-of-6` | Hartmann Grisar | Luther, vol. 6 of 6 | E. M. Lamond | 1913-1917 (see the Gutenberg header) | have | PG 54811 |

## Arthur Ransome as translator (Gourmont; Old Peter's Russian Tales)

Shelf: `pipeline/ransome-translations_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ransome-translations` · titles `python3 pipeline/split_shelf_titles.py ransome-translations`.
2026-10-10, vetoable. His Swallows and Amazons is on Lane B's `ransome_shelf.json`, not here. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ransome-old-peters-russian-tales` | Russian folk tales, retold | Old Peter's Russian Tales | Arthur Ransome | 1916 | have | PG 16981 |
| `ransome-gourmont-night-in-the-luxembourg` | Remy de Gourmont | A Night in the Luxembourg | Arthur Ransome | 1912 | have | PG 46766 |
| — | — | ransome-own-books: Swallows and Amazons and the rest of the series: Ransome's own books, on Lane B's ransome_shelf.json. | — | — | excluded | — |
