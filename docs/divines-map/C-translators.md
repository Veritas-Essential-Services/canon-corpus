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
| `garnett-war-and-peace-vol3` | Tolstoy | War and Peace, vol. III of 3 (Parts XI to the Epilogue) | Constance Garnett | 1904 | have-raw | IA `in.ernet.dli.2015.170286` |
| `garnett-gogol-other` | — | Works of Gogol: The Government Inspector and Other Plays (1926) and Mirgorod (1928) - pre-1931, PD; no verified Garnett scan found (IA mirgorodgogol is a 1924 Potsdam Russian edition, not hers). Re-searched 2026-10-17: still no pre-1931 scan of either volume on the Internet Archive. | — | — | pending | — |
| `garnett-dostoevsky-poor-folk` | — | Poor Folk / Uncle's Dream: no Garnett version verified. The 1915 'Poor Folk and The Gambler' scans on IA are the Everyman (C. J. Hogarth) translation. Whether Garnett ever published these is unverified - do not list as hers without a title page. | — | — | pending | — |
| `garnett-war-and-peace-1904` | — | Heinemann 1904 first printing, wanted to replace the later scan. | — | — | pending | — |
| `garnett-turgenev-novels-1894` | — | The rest of the 15-vol Heinemann set as scans (e.g. IA novelsofivanturg02turg ...): only to replace PG texts if they prove defective. | — | — | pending | — |
| `garnett-war-and-peace` | — | Garnett's War and Peace (Heinemann 1904), volumes I and II: no pre-1931 scan found (searched 2026-10-17: the IA copies are Dole, Maude, Wiener, Bell or post-1930 Random House). Volume III is held as garnett-war-and-peace-vol3 from the DLI Heinemann 1904 scan. Found 2026-10-17: archive.org warpeace01tols_0 is the COMPLETE novel in Garnett's translation (title page: 'Translated by Constance Garnett', Carlton House, New York, printed by J. J. Little & Ives; Duke University copy). IA dates it 1900, but the printing carries no date and Carlton House editions are reprints from the 1930s or later, so it is held back under the pre-1931 printing rule. The words are the 1904 translation and are public domain; if Adam accepts late reprints of public-domain texts (the same ruling as the thirteen flagged in DIGEST-C), this scan supplies volumes I and II. | — | — | pending | — |
| `garnett-chekhov-letters-to-knipper` | — | The Letters of Anton Pavlovitch Tchehov to Olga Leonardovna Knipper (Chatto 1925 / Doran 1926): only a 1966 Blom reprint is on the Internet Archive (lettersofantonpa0000chek); held back as a facsimile until Adam rules on facsimiles. | — | — | pending | — |
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
| — | — | ia-warpeace0000coun_g3a9: Random House War and Peace in Garnett's translation, IA-dated 1910 but a Modern Library printing (the Garnett Modern Library edition began in 1931): post-1930. | — | — | excluded | — |
| — | — | ia-warpeace0000lyof: Scribner's 1904 'Novels and Other Works of Lyof N. Tolstoi', War and Peace vols III, IV and VI (also warpeace0000lyof_p5p4, warpeace0000lyof_p3p0): Crowell copyright 1899, Nathan Haskell Dole's translation, not Garnett's. Checked 2026-10-17. | — | — | excluded | — |

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
| — | — | pg-27827: The Kama Sutra (Burton and Bhide, 1883): left off by judgment, not rights, like the Pauls' sexology titles. Adam can ask for it. | — | — | excluded | — |

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
| `maude-anna-karenina-1` | Tolstoy | Anna Karenina, vol. I of 2 | Louise and Aylmer Maude | 1918 | have-raw | IA `annakarenina0001leot_t2s6` |
| `maude-anna-karenina-2` | Tolstoy | Anna Karenina, vol. II of 2 | Louise and Aylmer Maude | 1918 | have-raw | IA `annakarenina0002leot_k3j8` |
| `maude-essays-and-letters` | Tolstoy | Essays and Letters | Aylmer Maude | 1903 | have-raw | IA `essaysletters00tols` |
| `maude-sevastopol` | Tolstoy | Sevastopol and Other Military Tales | Louise and Aylmer Maude | 1901 | have-raw | IA `sevastopolandot00maudgoog` |
| `maude-confession` | Tolstoy | A Confession and What I Believe | Aylmer Maude | 1921 | have-raw | IA `confessionwhatib00tols` |
| `maude-hadji-murad` | Tolstoy | Hadji Murad, with The Light that Shines in Darkness, The Man who was Dead, The Cause of it All and other posthumous works | Aylmer Maude | 1912 | have-raw | IA `hadjimuradlightt00tols` |
| `maude-first-step` | Tolstoy | The First Step: An Essay on the Morals of Diet, to which are added two stories | Aylmer Maude | 1900 | have-raw | IA `firststepanessa00maudgoog` |
| `maude-pamphlets` | Tolstoy | Pamphlets, translated from the Russian | Aylmer Maude (several pieces signed by him; the rest unsigned Free Age Press translations) | 1900 | have-raw | IA `pamphletstransl00tolsgoog` |
| `maude-centenary` | — | The Centenary Edition (OUP 1928-37, 21 vols): only the volumes printed before 1931 qualify; per-volume dating needed. | — | — | pending | — |
| — | — | pg-28920: War and Peace Book 1 only: part of PG 2600. | — | — | excluded | — |
| — | — | pg-52242, pg-78278: Aylmer Maude's own books (Life of Tolstoy, Life of Marie Stopes): not translations. | — | — | excluded | — |
| — | — | pg-79027: Tolstoy on Art: Maude as editor/compiler; overlaps What Is Art?. | — | — | excluded | — |
| — | — | other-maudes: PG items by Alice Maude Kellogg, Maude Alma, F. N. Maude, Maude Wholohan: different people. | — | — | excluded | — |
| — | — | pg-26472: Newer transcription of What Men Live By: its .txt returns 404 on Gutenberg's cache (2026-10-02); PG 6157 used. | — | — | excluded | — |
| — | — | pg-26660: Plays: Complete Edition, front matter only (the transcriber's note says the plays are posted separately as 26661-26666, which are used). | — | — | excluded | — |
| — | — | ia-twentythreetales0000tols: Twenty-Three Tales (Maudes, OUP 1906): the only scan found is a 1954+ World's Classics reprint. Checked 2026-10-17. | — | — | excluded | — |
| — | — | ia-whatisreligionot00tols: What Is Religion? (Crowell 1902) is translated by V. Tchertkoff and A. C. Fifield, not the Maudes. | — | — | excluded | — |

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

## John Payne (Villon, Decameron; since round 81 also Bandello, Hafiz vol. I and three volumes of Flowers of France)

Shelf: `pipeline/payne_shelf.json` · fetch `python3 pipeline/fetch_shelf.py payne` · titles `python3 pipeline/split_shelf_titles.py payne`.
Round 4, vetoable. Round 81 (2026-10-17), vetoable: eight titles added. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `payne-alaeddin-and-the-enchanted-lamp` | Anonymous (from the Arabian Nights) | Alaeddin and the Enchanted Lamp | John Payne | 1889 | have | PG 5100 |
| `payne-decameron` | Boccaccio | The Decameron | John Payne | 1886 | have | PG 23700 |
| `payne-villon` | Villon | Poems (Lesser and Greater Testament, Ballades) | John Payne | 1878 | have-raw | IA `poemsofmasterfra00villiala` |
| `payne-bandello-1` | Bandello | The Novels of Matteo Bandello, Bishop of Agen, vol. I | John Payne | 1890 | have-raw | IA `novelsofmatteoba01band` |
| `payne-bandello-2` | Bandello | The Novels of Matteo Bandello, Bishop of Agen, vol. II | John Payne | 1890 | have-raw | IA `novelsofmatteoba02band` |
| `payne-bandello-4` | Bandello | The Novels of Matteo Bandello, Bishop of Agen, vol. IV | John Payne | 1890 | have-raw | IA `novelsofmatteoba04band` |
| `payne-bandello-5` | Bandello | The Novels of Matteo Bandello, Bishop of Agen, vol. V | John Payne | 1890 | have-raw | IA `novelsofmatteoba05band` |
| `payne-bandello-6` | Bandello | The Novels of Matteo Bandello, Bishop of Agen, vol. VI | John Payne | 1890 | have-raw | IA `novelsofmatteoba06band` |
| `payne-hafiz-1` | Hafiz | The Poems of Shemseddin Mohammed Hafiz of Shiraz, now first completely done into English verse, vol. I | John Payne | 1901 | have-raw | IA `poemsshemseddin00socigoog` |
| `payne-flowers-romantic-1` | Hugo to Leconte de Lisle | Flowers of France: the Romantic Period, Hugo to Leconte de Lisle, vol. I | John Payne | 1906 | have-raw | IA `flowersoffrance01payn` |
| `payne-flowers-romantic-2` | Hugo to Leconte de Lisle | Flowers of France: the Romantic Period, Hugo to Leconte de Lisle, vol. II | John Payne | 1906 | have-raw | IA `flowersoffrancer02payn` |
| `payne-flowers-renaissance` | Ronsard to Saint-Amant | Flowers of France: the Renaissance Period, from Ronsard to Saint-Amant | John Payne | 1907 | have-raw | IA `flowersoffrancer00payn` |
| `payne-thousand-nights` | — | Payne's Book of the Thousand Nights and One Night (Villon Society 1882-84, 9 vols): Burton's and Lane's are already shelved; the IA set is incomplete and not fetched. Your call. | — | — | pending | — |
| `payne-bandello` | — | Novels of Matteo Bandello (1890, 6 vols): vols I, II and IV-VI are now held. Vol. III was not found online. | — | — | pending | — |
| `payne-hafiz` | — | The Poems of Hafiz (1901, 3 vols): vol. I is held; vols II and III were not found online. | — | — | pending | — |
| — | — | payne-ibn-et-tefrid: The Quatrains of Ibn et Tefrid (1921) were left out: not checked whether they are a translation or Payne's own verse under an invented name. | — | — | excluded | — |

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
| `curtin-on-the-field-of-glory` | Sienkiewicz | On the Field of Glory | Jeremiah Curtin | 1906 | have | PG 37406 |
| `curtin-orzeszkowa-the-argonauts` | Eliza Orzeszkowa | The Argonauts | Jeremiah Curtin | 1901 | have | PG 20537 |
| `curtin-pan-michael` | Sienkiewicz | Pan Michael (Trilogy III) | Jeremiah Curtin | 1893 | have | PG 37361 |
| `curtin-prus-the-pharaoh-and-the-priest` | Bolesław Prus | The Pharaoh and the Priest | Jeremiah Curtin | 1902 | have | PG 23646 |
| `curtin-quo-vadis` | Sienkiewicz | Quo Vadis | Jeremiah Curtin | 1896 | have | PG 2853 |
| `curtin-sienkiewicz-children-of-the-soil` | Henryk Sienkiewicz | Children of the Soil | Jeremiah Curtin | 1895 | have | PG 44939 |
| `curtin-sienkiewicz-hania` | Henryk Sienkiewicz | Hania | Jeremiah Curtin | 1897 | have | PG 36583 |
| `curtin-sienkiewicz-in-vain` | Henryk Sienkiewicz | In Vain | Jeremiah Curtin | 1899 | have | PG 46454 |
| `curtin-sienkiewicz-let-us-follow-him` | Henryk Sienkiewicz | Let Us Follow Him | Jeremiah Curtin | 1897 | have | PG 41988 |
| `curtin-sienkiewicz-life-and-death` | Henryk Sienkiewicz | Life and Death, and Other Legends and Stories | Jeremiah Curtin | 1904 | have | PG 35736 |
| `curtin-sienkiewicz-lillian-morris` | Henryk Sienkiewicz | Lillian Morris, and Other Stories | Jeremiah Curtin | 1894 | have | PG 47527 |
| `curtin-the-deluge` | Sienkiewicz | The Deluge (Trilogy II) | Jeremiah Curtin | 1891 | have | PG 37198 + PG 37308 |
| `curtin-with-fire-and-sword` | Sienkiewicz | With Fire and Sword (Trilogy I) | Jeremiah Curtin | 1890 | have | PG 37027 |
| `curtin-knights-of-the-cross` | — | The Knights of the Cross (1900): Gutenberg's edition is not Curtin's; no Curtin scan checked this run. | — | — | pending | — |
| `curtin-myths` | — | Curtin's own collections of Irish, Russian and Native American myths: his own fieldwork rather than translations of a work; left out. | — | — | pending | — |
| — | — | pg-35499: The Pharaoh and the Priest again: a second Gutenberg transcription of the same Curtin translation; this shelf keeps 23646. | — | — | excluded | — |

## Isabel Hapgood (Hugo, Gorky, Turgenev, Bunin)

Shelf: `pipeline/hapgood_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hapgood` · titles `python3 pipeline/split_shelf_titles.py hapgood`.
Round 5, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hapgood-bunin-village` | Bunin | The Village | Isabel F. Hapgood | 1923 | have | PG 59981 |
| `hapgood-gorky-orloff` | Gorky | Orlóff and His Wife: Tales of the Barefoot Brigade | Isabel F. Hapgood | 1901 | have | PG 55636 |
| `hapgood-hugo-notre-dame-de-paris` | Victor Hugo | Notre-Dame de Paris | Isabel Florence Hapgood | 1888 | have | PG 2610 |
| `hapgood-les-miserables` | Hugo | Les Misérables | Isabel F. Hapgood | 1887 | have | PG 135 |
| `hapgood-leskov-the-steel-flea` | Nikolai Leskov | The Steel Flea | Isabel Florence Hapgood | 1916 | have | PG 61172 |
| `hapgood-tolstoy-on-the-significance-of-science-and-art` | Leo Tolstoy | On the Significance of Science and Art | Isabel Florence Hapgood | 1887 | have | PG 3631 |
| `hapgood-tolstoy-sevastopol` | Leo Tolstoy | Sevastopol | Isabel Florence Hapgood | 1888 | have | PG 47197 |
| `hapgood-tolstoy-the-census-in-moscow` | Leo Tolstoy | The Census in Moscow | Isabel Florence Hapgood | 1887 | have | PG 3540 |
| `hapgood-tolstoy-what-to-do` | Leo Tolstoy | What to Do? Thoughts Evoked by the Census of Moscow | Isabel Florence Hapgood | 1887 | have | PG 3541 |
| `hapgood-turgenev-first-love` | Turgenev | First Love, and Other Stories | Isabel F. Hapgood | 1904 | have | PG 56878 |
| `hapgood-turgenev-nobleman` | Turgenev | A Nobleman's Nest | Isabel F. Hapgood | 1903 | have | PG 25771 |
| `hapgood-turgenev-reckless-character` | Turgenev | A Reckless Character, and Other Stories | Isabel F. Hapgood | 1904 | have | PG 15994 |
| `hapgood-turgenev-superfluous-man` | Turgenev | The Diary of a Superfluous Man, and Other Stories | Isabel F. Hapgood | 1904 | have | PG 41201 |
| `hapgood-tolstoy-childhood` | — | Hapgood's Childhood, Boyhood, Youth (1886): not on Gutenberg in her version; IA not checked. (Her Sevastopol was found on Gutenberg in round 35.) | — | — | pending | — |
| — | — | pg-3630: What to Do? again: a second Gutenberg file of the same Hapgood translation; this shelf keeps 3541. | — | — | excluded | — |

## James Legge (Chinese classics: the complete Chinese Classics, first edition 1861-72, since round 75; the Shu King, Yi King, Li Ki and Kwang-ze from the Sacred Books of the East since round 64)

Shelf: `pipeline/legge_shelf.json` · fetch `python3 pipeline/fetch_shelf.py legge` · titles `python3 pipeline/split_shelf_titles.py legge`.
Round 5, vetoable. Round 64 (2026-10-17), vetoable: six SBE volumes added. Round 75 (2026-10-17), vetoable: the Chinese Classics, 8 volumes, added. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `legge-tao-teh-king` | Laozi | Tao Te Ching | James Legge | 1891 | have | PG 216 |
| `legge-analects` | Confucius | Analects | James Legge | 1861 | have | PG 3330 |
| `legge-faxian` | Faxian | A Record of Buddhistic Kingdoms | James Legge | 1886 | have | PG 2124 |
| `legge-shu-king` | The Shujing, the Shijing (religious portions) and the Xiaojing | The Shu King, the Religious Portions of the Shih King, the Hsiao King | James Legge | 1879 | have-raw | IA `in.ernet.dli.2015.4712` |
| `legge-yi-king` | The Yijing (Book of Changes) | The Yi King | James Legge | 1882 | have-raw | IA `in.ernet.dli.2015.188091` |
| `legge-li-ki-1` | The Liji (Book of Rites) | The Li Ki, books I-X | James Legge | 1885 | have-raw | IA `in.ernet.dli.2015.152465` |
| `legge-li-ki-2` | The Liji (Book of Rites) | The Li Ki, books XI-XLVI | James Legge | 1885 | have-raw | IA `in.ernet.dli.2015.188096` |
| `legge-kwang-ze-1` | Zhuangzi | The Writings of Kwang-ze, books I-XVII, with Legge's brief notices of the books (from The Texts of Taoism, part I) | James Legge | 1891 | have-raw | IA `in.ernet.dli.2015.45262` (cut from the volume) |
| `legge-kwang-ze-2` | Zhuangzi and the Taishang Ganying Pian, with appendixes | The Texts of Taoism, part II: Kwang-ze books XVIII-XXXIII, the Thai-Shang Tractate of Actions and their Retributions, and eight appendixes | James Legge | 1891 | have-raw | IA `in.ernet.dli.2015.45263` |
| `legge-cc-1` | The Confucian Analects, the Great Learning and the Doctrine of the Mean, with prolegomena | The Chinese Classics, vol. I: Confucian Analects, the Great Learning, and the Doctrine of the Mean | James Legge | 1861 | have-raw | IA `chineseclassics01legg_0` |
| `legge-cc-2` | The Mencius | The Chinese Classics, vol. II: the Works of Mencius | James Legge | 1861 | have-raw | IA `chineseclassics02legg_0` |
| `legge-cc-3-1` | The Shujing (Book of Documents), part 1 | The Chinese Classics, vol. III, part I: the Shoo King | James Legge | 1865 | have-raw | IA `chineseclassics31legg` |
| `legge-cc-3-2` | The Shujing (Book of Documents), part 2 | The Chinese Classics, vol. III, part II: the Shoo King | James Legge | 1865 | have-raw | IA `chineseclassics32legg` |
| `legge-cc-4-1` | The Shijing (Book of Poetry), part 1 | The Chinese Classics, vol. IV, part I: the She King | James Legge | 1871 | have-raw | IA `chineseclassics41legg_0` |
| `legge-cc-4-2` | The Shijing (Book of Poetry), part 2 | The Chinese Classics, vol. IV, part II: the She King | James Legge | 1871 | have-raw | IA `chineseclassics42legg_0` |
| `legge-cc-5-1` | The Chunqiu (Spring and Autumn Annals) with the Zuo zhuan, part 1 | The Chinese Classics, vol. V, part I: the Ch'un Ts'ew, with the Tso Chuen | James Legge | 1872 | have-raw | IA `chineseclassics51legg` |
| `legge-cc-5-2` | The Chunqiu (Spring and Autumn Annals) with the Zuo zhuan, part 2 | The Chinese Classics, vol. V, part II: the Ch'un Ts'ew, with the Tso Chuen | James Legge | 1872 | have-raw | IA `chineseclassics52legg` |
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
| — | — | art-of-war-other-files: PG 17405 and 66706 are two more Gutenberg files of Lionel Giles's 1910 Art of War, already shelved here from PG 132: duplicates, not shelved (round 39). | — | — | excluded | — |

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

## Sir Edwin Arnold (Bhagavad Gita; since round 78 also the Hitopadesa, the Gita Govinda, Indian Idylls and the Katha Upanishad)

Shelf: `pipeline/edwin-arnold_shelf.json` · fetch `python3 pipeline/fetch_shelf.py edwin-arnold` · titles `python3 pipeline/split_shelf_titles.py edwin-arnold`.
Round 6, vetoable. Round 78 (2026-10-17), vetoable: four titles added. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `edwin-arnold-bhagavad-gita` | Bhagavad Gita | The Song Celestial (Bhagavad Gita) | Sir Edwin Arnold | 1885 | have | PG 2388 |
| `edwin-arnold-book-of-good-counsels` | The Hitopadesa | The Book of Good Counsels | Sir Edwin Arnold | 1861 | have-raw | IA `cu31924074412994` |
| `edwin-arnold-indian-poetry` | Jayadeva's Gita Govinda, two books of the Mahabharata, proverbs from the Hitopadesa, and other poems | Indian Poetry, containing 'The Indian Song of Songs' from the Sanskrit of the Gita Govinda of Jayadeva | Sir Edwin Arnold | (undated eighth impression; see the note) | have | PG 25965 |
| `edwin-arnold-indian-idylls` | Episodes of the Mahabharata (Nala and Damayanti, Savitri and others) | Indian Idylls, from the Sanskrit of the Mahabharata | Sir Edwin Arnold | 1883 | have-raw | IA `indianidyllsfrom00arnouoft` |
| `edwin-arnold-secret-of-death` | The Katha Upanishad | The Secret of Death, from the Sanskrit, with some Collected Poems | Sir Edwin Arnold | 1885 | have-raw | IA `secretofdeathfro00arnouoft` |
| — | — | light-of-asia: The Light of Asia (1879): Arnold's own poem. | — | — | excluded | — |

## R. T. H. Griffith (Ramayana, Rigveda; since round 79 also the Atharva-Veda, Samaveda, White Yajurveda, Idylls from the Sanskrit and Jami's Yusuf and Zulaikha)

Shelf: `pipeline/griffith_shelf.json` · fetch `python3 pipeline/fetch_shelf.py griffith` · titles `python3 pipeline/split_shelf_titles.py griffith`.
Round 6, vetoable. Round 79 (2026-10-17), vetoable: six titles added. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `griffith-ramayana` | Valmiki | The Ramayana | Ralph T. H. Griffith | 1870 | have | PG 24869 |
| `griffith-rigveda` | Rigveda | The Hymns of the Rigveda, 10 mandalas | Ralph T. H. Griffith | 1889 | have-raw | IA `in.ernet.dli.2015.195721` + IA `in.ernet.dli.2015.195722` |
| `griffith-atharva-1` | Atharva-Veda | The Hymns of the Atharva-Veda, vol. I (Books I-VII) | Ralph T. H. Griffith | 1895 | have-raw | IA `in.ernet.dli.2015.274134` |
| `griffith-atharva-2` | Atharva-Veda | The Hymns of the Atharva-Veda, vol. II | Ralph T. H. Griffith | 1896 | have-raw | IA `in.ernet.dli.2015.274135` |
| `griffith-samaveda` | Samaveda | The Hymns of the Samaveda | Ralph T. H. Griffith | 1893 | have-raw | IA `in.ernet.dli.2015.180573` |
| `griffith-white-yajurveda` | White Yajurveda | The Texts of the White Yajurveda | Ralph T. H. Griffith | 1899 | have-raw | IA `textswhiteyajur01grifgoog` |
| `griffith-idylls` | Kalidasa, Valmiki and the Mahabharata | Idylls from the Sanskrit | Ralph T. H. Griffith | 1866 | have-raw | IA `idyllsfromsansk00grifgoog` |
| `griffith-yusuf` | Jami | Yusuf and Zulaikha | Ralph T. H. Griffith | 1882 | have-raw | IA `ysufzulaikhapo00jamiuoft` |
| — | — | griffith-white-yajurveda-1987: textswhiteyajur00grifgoog is a 1987 Munshiram Manoharlal reprint; the 1899 Lazarus scan was used. | — | — | excluded | — |
| — | — | griffith-later-editions: Later Lazarus editions (Atharva-Veda 1916-17, Samaveda 1907 and 1926, White Yajurveda 1927) were passed over for the first editions. | — | — | excluded | — |
| — | — | griffith-birth-of-the-war-god: Already held on singles-literature (Project Gutenberg 31968). | — | — | excluded | — |

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

## E. H. Whinfield (Rumi's Masnavi; since round 79 also the Gulshan i Raz, Omar Khayyam's Quatrains and Jami's Lawa'ih)

Shelf: `pipeline/whinfield_shelf.json` · fetch `python3 pipeline/fetch_shelf.py whinfield` · titles `python3 pipeline/split_shelf_titles.py whinfield`.
Round 6, vetoable. Round 79 (2026-10-17), vetoable: three titles added. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `whinfield-masnavi` | Rumi | Masnavi (abridged) | E. H. Whinfield | 1887 | have-raw | IA `cu31924026910251` |
| `whinfield-gulshan` | Mahmud Shabistari | Gulshan i Raz: the Mystic Rose Garden | E. H. Whinfield | 1880 | have-raw | IA `gulshanirazmysti00shabuoft` |
| `whinfield-quatrains` | Omar Khayyam | The Quatrains of Omar Khayyam | E. H. Whinfield | 1882 | have-raw | IA `in.ernet.dli.2015.38800` |
| `whinfield-lawaih` | Jami | Lawa'ih: a Treatise on Sufism | E. H. Whinfield and Mirza Muhammad Kazvini | 1906 | have-raw | IA `lawaihvolxvi014972mbp` |
| — | — | whinfield-omar-pg38511: Gutenberg 38511 mixes Whinfield with FitzGerald and Nicolas; the 1882 Trübner scan is used instead. | — | — | excluded | — |

## R. A. Nicholson (Rumi, Hujwiri; since round 79 also Ibn al-Arabi's Tarjuman al-Ashwaq, Translations of Eastern Poetry and Prose and the Mathnawi vol. II)

Shelf: `pipeline/nicholson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py nicholson` · titles `python3 pipeline/split_shelf_titles.py nicholson`.
Round 6, vetoable. Round 79 (2026-10-17), vetoable: three titles added. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `nicholson-kashf-al-mahjub` | Hujwiri | Kashf al-Mahjub | Reynold A. Nicholson | 1911 | have | PG 64786 |
| `nicholson-divani-shamsi-tabriz` | Rumi | Selected Poems from the Divani Shamsi Tabriz | Reynold A. Nicholson | 1898 | have-raw | IA `india.history.resource.111025` |
| `nicholson-tarjuman` | Ibn al-Arabi | The Tarjuman al-Ashwaq: a Collection of Mystical Odes | Reynold A. Nicholson | 1911 | have-raw | IA `tarjumanalashwaq00ibnaiala` |
| `nicholson-eastern-poetry` | various Arabic and Persian authors | Translations of Eastern Poetry and Prose | Reynold A. Nicholson | 1922 | have-raw | IA `translationsofea00nich` |
| `nicholson-mathnawi-2` | Rumi | The Mathnawi of Jalalu'ddin Rumi, vol. II: translation of the First and Second Books | Reynold A. Nicholson | 1926 | have-raw | IA `in.ernet.dli.2015.70297` |
| `nicholson-mathnawi` | — | The rest of the Mathnawi (Gibb series, 1925-40): the translation of Books I-II (vol. II, 1926) is now held. Vol. IV (1930) waits on the 1930 ruling; the volumes after 1930 are out. Vols I (1925) and III (1929) were not taken because the series puts the Persian text in the odd volumes; check that before adding either. | — | — | pending | — |
| — | — | nicholson-mathnawi-2-reprint: mathnawiofjalalu0006unse is a 1990 reprint of vol. II (reprint list on its verso); the 1926 DLI scan was used. | — | — | excluded | — |

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
| `bowring-anthology-of-jugoslav-poetry` | Serbian lyric poets (anthology, ed. Beatrice L. Stevenson) | An Anthology of Jugoslav Poetry: Serbian Lyrics | John Bowring (with Owen Meredith and others; ed. Beatrice L. Stevenson) | 1920 anthology of 19th-century translations (see the Gutenberg header) | have | PG 36091 |
| `bowring-goethe-poems` | Goethe | Poems, in the original metres | Edgar Alfred Bowring | 1853 | have | PG 1287 |
| `bowring-heine-poems` | Heine | Poems, complete | Edgar Alfred Bowring | 1859 | have | PG 52882 |
| `bowring-peter-schlemihl` | Chamisso | Peter Schlemihl | John Bowring | 1824 | have | PG 21943 |
| `bowring-servian-popular-poetry` | Serbian folk poetry (Vuk Karadžić's collection) | Servian Popular Poetry | John Bowring | 1827 (see the Gutenberg header) | have | PG 39028 |
| `bowring-specimens-of-the-russian-poets-vol-1` | various Russian poets (anthology) | Specimens of the Russian Poets, vol. 1 (of 2) | John Bowring | 1821 (see the Gutenberg header) | have | PG 78744 |
| `bowring-specimens-of-the-russian-poets-vol-2` | various Russian poets (anthology) | Specimens of the Russian Poets, vol. 2 (of 2) | John Bowring | 1823 (see the Gutenberg header) | have | PG 78745 |
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
| `symonds-gozzi-memoirs-vol-1` | Carlo Gozzi | The Memoirs of Count Carlo Gozzi, vol. 1 | John Addington Symonds | 1890 (see the Gutenberg header) | have | PG 38266 |
| `symonds-gozzi-memoirs-vol-2` | Carlo Gozzi | The Memoirs of Count Carlo Gozzi, vol. 2 | John Addington Symonds | 1890 (see the Gutenberg header) | have | PG 33225 |
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
| — | — | pg-2782: Wilhelm Tell again: another Gutenberg file of Martin's translation, already held as 6788. | — | — | excluded | — |

## Lafcadio Hearn as translator (Gautier, Flaubert)

Shelf: `pipeline/hearn_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hearn` · titles `python3 pipeline/split_shelf_titles.py hearn`.
Round 8, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hearn-gautier-cleopatras-nights` | Gautier | One of Cleopatra's Nights and Other Fantastic Romances | Lafcadio Hearn | 1882 | have | PG 39397 |
| `hearn-flaubert-temptation` | Flaubert | The Temptation of St. Anthony | Lafcadio Hearn | 1910 | have | PG 52225 |
| — | — | pg-25053: Gutenberg 25053 is another Temptation of St. Antony with no translator named; not Hearn's. | — | — | excluded | — |
| — | — | hearn-own-works: Kwaidan, Glimpses of Unfamiliar Japan etc.: Hearn's own books. | — | — | excluded | — |
| — | — | pg-22660-22662: King Candaules, Clarimonde and The Mummy's Foot: single stories from One of Cleopatra's Nights (39397), already held whole. | — | — | excluded | — |

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
| `moncrieff-proust-the-captive` | Proust | The Captive (La Prisonnière) | C. K. Scott Moncrieff | 1929 | have-raw | IA `captive0000marc_d6q4` |
| `moncrieff-lauzun` | Armand Louis de Gontaut, duc de Lauzun | Memoirs of the Duc de Lauzun | C. K. Scott Moncrieff | 1928 | have-raw | IA `memoirsofducdela0000cksc` |
| `moncrieff-proust-cities-of-the-plain` | — | 1927/1929: US PD, but the only open scans (citiesofplain0000prou_b6a6, dli.ernet.16336) are Chatto reprints of 1960 and 1971. Checked 2026-10-17: bwb_S0-BHU-960 is the Boni edition in one volume, 'Published January, 1930': a 1930 printing, so it waits on the same 1930 ruling as the five titles in DIGEST-C. citiesofplainvol0000marc_f0l7 is Boni 1927 volume two only; volume one not found open. The Modern Library copies list 1932. | — | — | pending | — |
| `moncrieff-proust-sweet-cheat-gone` | — | 1930: US PD since 2026, but every open scan is a 1957+ Random House or 1970 Vintage printing (copyright-renewal lines). | — | — | pending | — |
| `moncrieff-pirandello-shoot` | — | 1926: shoot0000luig is the 1934 'Nobel Prize Edition'; shoot-luigi-pirandello is a Gutenberg-Australia text of unstated edition. | — | — | pending | — |
| `moncrieff-pirandello-old-and-young` | — | 1928: only volume 2 is open (oldyoung02pira); volume 1 not found. | — | — | pending | — |
| `moncrieff-stendhal-red-and-black` | — | 1926: US PD. redblack0000mari_e9r8, _h6c2 and _z4c1 are all Modern Library printings by Random House (1931 or later; e9r8's back list carries Modern Library Giant numbers). redblack0000unse_p8m8 is the 1926 first printing but volume one only; volume two not found open. Checked 2026-10-17: bwb_Y0-CAN-926 is both volumes in one, but the Liveright 'Black & Gold Edition, February, 1937'. | — | — | pending | — |
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
| `levy-nietzsche-beyond-good-and-evil` | Nietzsche | Beyond Good and Evil | Helen Zimmern | 1907 | have | PG 4363 |
| `levy-nietzsche-birth-of-tragedy` | Nietzsche | The Birth of Tragedy | Wm. A. Haussmann | 1909 | have | PG 51356 |
| `levy-nietzsche-case-of-wagner` | Nietzsche | The Case of Wagner, Nietzsche contra Wagner, Selected Aphorisms | Anthony M. Ludovici | 1911 | have | PG 25012 |
| `levy-nietzsche-dawn-of-day` | Nietzsche | The Dawn of Day | J. M. Kennedy | 1911 | have | PG 39955 |
| `levy-nietzsche-early-greek-philosophy` | Nietzsche | Early Greek Philosophy and Other Essays | Maximilian A. Mügge | 1911 | have | PG 51548 |
| `levy-nietzsche-ecce-homo` | Nietzsche | Ecce Homo | Anthony M. Ludovici (poetry by Paul V. Cohn) | 1911 | have | PG 52190 |
| `levy-nietzsche-future-of-our-educational-institutions` | Nietzsche | On the Future of our Educational Institutions; Homer and Classical Philology; We Philologists | J. M. Kennedy | 1909 | have | PG 51580 |
| `levy-nietzsche-genealogy-of-morals` | Nietzsche | The Genealogy of Morals | Horace B. Samuel (with J. M. Kennedy) | 1910 | have | PG 52319 |
| `levy-nietzsche-human-all-too-human-1` | Nietzsche | Human, All-Too-Human, Part I | Helen Zimmern | 1909 | have | PG 51935 |
| `levy-nietzsche-human-all-too-human-2` | Nietzsche | Human, All-Too-Human, Part II | Paul V. Cohn | 1911 | have | PG 37841 |
| `levy-nietzsche-joyful-wisdom` | Nietzsche | The Joyful Wisdom | Thomas Common (poetry by Paul V. Cohn and Maude Dominica Petre) | 1910 | have | PG 52881 |
| `levy-nietzsche-thoughts-out-of-season-1` | Nietzsche | Thoughts Out of Season, Part I | Anthony M. Ludovici | 1909 | have | PG 51710 |
| `levy-nietzsche-thoughts-out-of-season-2` | Nietzsche | Thoughts Out of Season, Part II | Adrian Collins | 1909 | have | PG 38226 |
| `levy-nietzsche-twilight-and-antichrist` | Nietzsche | The Twilight of the Idols; The Antichrist | Anthony M. Ludovici | 1911 | have | PG 52263 |
| `levy-nietzsche-will-to-power-1` | Nietzsche | The Will to Power, Books I and II | Anthony M. Ludovici | 1909 | have | PG 52914 |
| `levy-nietzsche-will-to-power-2` | Nietzsche | The Will to Power, Books III and IV | Anthony M. Ludovici | 1910 | have | PG 52915 |
| `levy-nietzsche-zarathustra` | Nietzsche | Thus Spake Zarathustra | Thomas Common | 1909 | have | PG 1998 |
| `levy-nietzsche-missing-volumes` | — | Levy vols still not on Gutenberg: Miscellaneous Aphorisms, Poems, Letters, the Index. (Thoughts Out of Season I and vol. 3, the Future of our Educational Institutions, were found in round 35.) | — | — | pending | — |
| — | — | pg-52124: A second Gutenberg Joyful Wisdom from the same Levy volume; 52881 (Distributed Proofreaders) is used. | — | — | excluded | — |
| — | — | pg-19322: Mencken's own Antichrist translation (1918), not Levy's; its front matter carries 1923-1924 dates; a separate translator. | — | — | excluded | — |
| — | — | pg-38145: Alexander Harvey's 1908 Human, All Too Human selection, not Levy's. | — | — | excluded | — |
| — | — | pg-19634: Another Beyond Good and Evil with no translator in the header; not checked. | — | — | excluded | — |
| — | — | pg-5652: Thoughts Out of Season I again: an earlier Gutenberg file of Ludovici's translation; this shelf keeps 51710, the Levy edition. | — | — | excluded | — |
| — | — | pg-28146: On the Future of our Educational Institutions alone; 51580 holds it with the rest of Levy vol. 3. | — | — | excluded | — |
| — | — | pg-18188: Homer and Classical Philology alone; part of Levy vol. 3 (51580). | — | — | excluded | — |
| — | — | pg-18267: We Philologists alone; part of Levy vol. 3 (51580). | — | — | excluded | — |
| — | — | pg-52166: The Case of Wagner again: another file of Levy vol. 8, already held as 25012. | — | — | excluded | — |

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
| `archer-ibsen-vol-12` | Ibsen | Collected Works, vol. 12: From Ibsen's Workshop (notes, scenarios and drafts of the modern plays) | A. G. Chater; introduction by William Archer | 1911 | have-raw | IA `fromibsensworksh00ibseuoft` |
| — | — | single-play-gutenberg-texts: PG 4093, 4070, 4782, 7942, 8121, 18428, 18792, 19018 are single plays from the same Archer edition; the volumes are used instead so nothing is held twice. | — | — | excluded | — |
| — | — | sharp-everyman: R. Farquharson Sharp's Everyman Ibsen (PG 2446, 2467): another translator; A Doll's House in his version is on adler_shelf.json. | — | — | excluded | — |
| — | — | marx-aveling-wild-duck: PG 73631: Eleanor Marx Aveling's translation; another translator. | — | — | excluded | — |

## Magnússon and Morris (Icelandic sagas)

Shelf: `pipeline/morris-magnusson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py morris-magnusson` · titles `python3 pipeline/split_shelf_titles.py morris-magnusson`.
Rounds 12-13 (2026-10-10), vetoable. Includes the six-volume Saga Library. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mm-frithiof-the-bold` | anonymous (Old Norse) | The Story of Frithiof the Bold | Eiríkr Magnússon and William Morris | 1875 | have | PG 24420 |
| `mm-grettir-the-strong` | anonymous (Old Norse) | The Story of Grettir the Strong | Eiríkr Magnússon and William Morris | 1869 | have | PG 12747 |
| `mm-gunnlaug-worm-tongue` | anonymous (Old Norse) | The Story of Gunnlaug the Worm-Tongue and Raven the Skald | Eiríkr Magnússon and William Morris | 1869 (as printed 1875) | have | PG 24421 |
| `mm-saga-library-vol-1` | anonymous (Old Norse) | The Saga Library, vol. 1: The Story of Howard the Halt; The Banded Men; Hen Thorir | William Morris and Eiríkr Magnússon | 1891 | have-raw | IA `sagalibrarydonei01snoriala` |
| `mm-saga-library-vol-2` | anonymous (Old Norse) | The Saga Library, vol. 2: The Story of the Ere-Dwellers (Eyrbyggja Saga), with The Heath-Slayings | William Morris and Eiríkr Magnússon | 1892 | have-raw | IA `sagalibrarydonei02snor` |
| `mm-saga-library-vol-3` | Snorri Sturluson | The Saga Library, vol. 3: Heimskringla, vol. I | William Morris and Eiríkr Magnússon | 1893 | have-raw | IA `sagalibrarydonei03snor` |
| `mm-saga-library-vol-4` | Snorri Sturluson | The Saga Library, vol. 4: Heimskringla, vol. II | William Morris and Eiríkr Magnússon | 1894 | have-raw | IA `sagalibrarydonei04snor` |
| `mm-saga-library-vol-5` | Snorri Sturluson | The Saga Library, vol. 5: Heimskringla, vol. III | William Morris and Eiríkr Magnússon | 1895 | have-raw | IA `sagalibrary05snoruoft` |
| `mm-saga-library-vol-6` | Snorri Sturluson | The Saga Library, vol. 6: Heimskringla, vol. IV (Magnússon's life of Snorri, notes and indexes) | Eiríkr Magnússon | 1905 | have-raw | IA `sagalibrarydonei06snor` |
| `mm-three-northern-love-stories` | anonymous (Old Norse) | Three Northern Love Stories and Other Tales | Eiríkr Magnússon and William Morris | 1875 | have-raw | IA `threenorthernlo00morrgoog` |
| `mm-volsunga-saga` | anonymous (Old Norse) | The Story of the Volsungs (Volsunga Saga), with excerpts from the Poetic Edda | Eiríkr Magnússon and William Morris | 1870 | held elsewhere (cross-ref) | `pipeline/poetic-edda_shelf.json` → `edda-volsunga-morris` (PG 1152) |
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
| `strindberg-bjorkman-master-olof` | Strindberg | Master Olof | Edwin Björkman | 1915 | have | PG 7363 |
| `strindberg-bjorkman-plays-1` | Strindberg | Plays, first series: The Dream Play; The Link; The Dance of Death I and II | Edwin Björkman | 1912 | have-raw | IA `playsbyauguststr00stri` |
| `strindberg-bjorkman-plays-2` | Strindberg | Plays, second series: There Are Crimes and Crimes; Miss Julia; The Stronger; Creditors; Pariah | Edwin Björkman | 1913 | have | PG 14347 |
| `strindberg-bjorkman-plays-3` | Strindberg | Plays, third series: Swanwhite; Simoom; Debit and Credit; Advent; The Thunderstorm; After the Fire | Edwin Björkman | 1913 | have | PG 44233 |
| `strindberg-bjorkman-plays-4` | Strindberg | Plays, fourth series: The Bridal Crown; The Spook Sonata; The First Warning; Gustavus Vasa | Edwin Björkman | 1916 | have | PG 44302 |
| `strindberg-field-german-lieutenant` | Strindberg | The German Lieutenant and Other Stories | Claud Field | 1915 | have | PG 46107 |
| `strindberg-field-historical-miniatures` | Strindberg | Historical Miniatures | Claud Field | 1913 | have | PG 7955 |
| `strindberg-field-inferno` | Strindberg | The Inferno | Claud Field | 1912 | have | PG 44108 |
| `strindberg-field-son-of-a-servant` | Strindberg | The Son of a Servant | Claud Field | 1913 | have | PG 44109 |
| `strindberg-field-the-growth-of-a-soul` | Strindberg | The Growth of a Soul | Claud Field | 1913 | have | PG 44107 |
| `strindberg-field-zones-of-the-spirit` | Strindberg | Zones of the Spirit | Claud Field | 1913 | have | PG 44118 |
| `strindberg-howard-lucky-pehr` | Strindberg | Lucky Pehr | Velma Swanston Howard | 1912 | have | PG 8510 |
| `strindberg-oland-plays-1` | Strindberg | Plays: The Father; Countess Julie; The Outlaw; The Stronger | Edith and Warner Oland | 1912 | have | PG 8499 |
| `strindberg-oland-plays-2` | Strindberg | Plays: Comrades; Facing Death; Pariah; Easter | Edith and Warner Oland | 1912 | have | PG 8500 |
| `strindberg-schleussner-confession-of-a-fool` | Strindberg | The Confession of a Fool | Ellie Schleussner | 1912 | have | PG 44106 |
| `strindberg-schleussner-in-midsummer-days` | Strindberg | In Midsummer Days and Other Tales | Ellie Schleussner | 1913 | have | PG 6694 |
| `strindberg-schleussner-red-room` | Strindberg | The Red Room | Ellie Schleussner | 1913 | have | PG 37039 |
| — | — | pg-4970: There Are Crimes and Crimes alone: the same Björkman text is in the second series (14347). | — | — | excluded | — |
| — | — | pg-5053: Creditors and Pariah alone: the same Björkman text is in the second series. | — | — | excluded | — |
| — | — | pg-8875: The Road to Damascus, tr. Graham Rawson: the text cites a 1937 production; Rawson's translation is of 1939. Not before 1931. | — | — | excluded | — |
| — | — | pg-7956: Married (1913): no translator named. | — | — | excluded | — |
| — | — | pg-46397: Legends (1912): no translator named. | — | — | excluded | — |
| — | — | pg-45375: Plays, First Series (Björkman) on Gutenberg: the same series is held from archive.org (sb-bjorkman-plays-1). | — | — | excluded | — |

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
| `wormeley-balzac-a-daughter-of-eve` | Honoré de Balzac | A Daughter of Eve | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1481 |
| `wormeley-balzac-a-drama-on-the-seashore` | Honoré de Balzac | A Drama on the Seashore | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1427 |
| `wormeley-balzac-a-start-in-life` | Honoré de Balzac | A Start in Life | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1403 |
| `wormeley-balzac-adieu` | Honoré de Balzac | Adieu | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1554 |
| `wormeley-balzac-an-historical-mystery` | Honoré de Balzac | An Historical Mystery (The Gondreville Mystery) | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1678 |
| `wormeley-balzac-an-old-maid` | Honoré de Balzac | An Old Maid | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1352 |
| `wormeley-balzac-beatrix` | Honoré de Balzac | Beatrix | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1957 |
| `wormeley-balzac-bureaucracy` | Honoré de Balzac | Bureaucracy | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1343 |
| `wormeley-balzac-catherine-de-medici` | Honoré de Balzac | Catherine De Medici | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1854 |
| `wormeley-balzac-cesar-birotteau` | Honoré de Balzac | Rise and Fall of César Birotteau | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1942 |
| `wormeley-balzac-el-verdugo` | Honoré de Balzac | El Verdugo | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1425 |
| `wormeley-balzac-eugenie-grandet` | Honoré de Balzac | Eugenie Grandet | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1715 |
| `wormeley-balzac-ferragus-chief-of-the-d-vorants` | Honoré de Balzac | Ferragus, Chief of the Dévorants | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1649 |
| `wormeley-balzac-juana` | Honoré de Balzac | Juana | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1437 |
| `wormeley-balzac-letters-to-madame-hanska-born-countess-rzewuska` | Honoré de Balzac | Letters to Madame Hanska, born Countess Rzewuska, aft | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 54466 |
| `wormeley-balzac-madame-firmiani` | Honoré de Balzac | Madame Firmiani | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1357 |
| `wormeley-balzac-maitre-cornelius` | Honoré de Balzac | Maitre Cornelius | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1454 |
| `wormeley-balzac-modeste-mignon` | Honoré de Balzac | Modeste Mignon | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1482 |
| `wormeley-balzac-paz-la-fausse-maitresse` | Honoré de Balzac | Paz (La Fausse Maitresse) | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1369 |
| `wormeley-balzac-pierre-grassou` | Honoré de Balzac | Pierre Grassou | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1230 |
| `wormeley-balzac-pierrette` | Honoré de Balzac | Pierrette | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1704 |
| `wormeley-balzac-seraphita` | Honoré de Balzac | Seraphita | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1432 |
| `wormeley-balzac-sons-of-the-soil` | Honoré de Balzac | Sons of the Soil | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1417 |
| `wormeley-balzac-study-of-a-woman` | Honoré de Balzac | Study of a Woman | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1373 |
| `wormeley-balzac-the-alkahest` | Honoré de Balzac | The Alkahest | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1453 |
| `wormeley-balzac-the-brotherhood-of-consolation` | Honoré de Balzac | The Brotherhood of Consolation | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1967 |
| `wormeley-balzac-the-chouans` | Honoré de Balzac | The Chouans | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1921 |
| `wormeley-balzac-the-deputy-of-arcis` | Honoré de Balzac | The Deputy of Arcis | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1871 |
| `wormeley-balzac-the-hated-son` | Honoré de Balzac | The Hated Son | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1455 |
| `wormeley-balzac-the-hidden-masterpiece` | Honoré de Balzac | The Hidden Masterpiece | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1553 |
| `wormeley-balzac-the-illustrious-gaudissart` | Honoré de Balzac | The Illustrious Gaudissart | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1474 |
| `wormeley-balzac-the-lesser-bourgeoisie` | Honoré de Balzac | The Lesser Bourgeoisie | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1641 |
| `wormeley-balzac-the-lily-of-the-valley` | Honoré de Balzac | The Lily of the Valley | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1569 |
| `wormeley-balzac-the-marriage-contract` | Honoré de Balzac | The Marriage Contract | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1556 |
| `wormeley-balzac-the-recruit` | Honoré de Balzac | The Recruit | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1426 |
| `wormeley-balzac-the-red-inn` | Honoré de Balzac | The Red Inn | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1433 |
| `wormeley-balzac-the-secrets-of-the-princesse-de-cadignan` | Honoré de Balzac | The Secrets of the Princesse de Cadignan | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1344 |
| `wormeley-balzac-the-two-brothers` | Honoré de Balzac | The Two Brothers | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1380 |
| `wormeley-balzac-the-vicar-of-tours` | Honoré de Balzac | The Vicar of Tours | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1345 |
| `wormeley-balzac-the-village-rector` | Honoré de Balzac | The Village Rector | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1899 |
| `wormeley-balzac-unconscious-comedians` | Honoré de Balzac | Unconscious Comedians | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1242 |
| `wormeley-balzac-ursula` | Honoré de Balzac | Ursula | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1223 |
| `wormeley-balzac-vendetta` | Honoré de Balzac | Vendetta | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 1374 |
| `wormeley-daudet-tartarin-on-the-alps` | Alphonse Daudet | Tartarin on the Alps | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 25768 |
| `wormeley-sand-the-bagpipers` | George Sand | The Bagpipers | Katharine Prescott Wormeley | 1885-1900 (Roberts Brothers) | have | PG 66513 |
| — | — | pg-7927: The Celibates collects Pierrette, The Vicar of Tours and The Two Brothers; the last two are shelved singly (1345, 1380), so the collection would hold them twice. | — | — | excluded | — |
| — | — | pg-43283: The Correspondence of Madame, Princess Palatine (ed. Wormeley): letters, edited not translated in the same sense; not checked. | — | — | excluded | — |

## Ernest Alfred Vizetelly (Zola, incl. the Three Cities)

Shelf: `pipeline/vizetelly_shelf.json` · fetch `python3 pipeline/fetch_shelf.py vizetelly` · titles `python3 pipeline/split_shelf_titles.py vizetelly`.
Round 14 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `vizetelly-zola-abbe-mourets-transgression` | Émile Zola | Abbe Mouret's Transgression | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 14200 |
| `vizetelly-zola-fruitfulness` | Émile Zola | Fruitfulness | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 10330 |
| `vizetelly-zola-his-excellency-son-exc-eug-ne-rougon` | Émile Zola | His Excellency [Son Exc. Eugène Rougon] | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 56654 |
| `vizetelly-zola-his-masterpiece` | Émile Zola | His Masterpiece | Ernest Alfred Vizetelly (named in the Gutenberg header as editor) | 1886-1906 (Chatto and Windus) | have | PG 15900 |
| `vizetelly-zola-lourdes` | Émile Zola | Lourdes | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 8516 |
| `vizetelly-zola-money` | Émile Zola | Money (L'Argent) | Ernest Alfred Vizetelly | 1894 (Chatto and Windus) | have | PG 56987 |
| `vizetelly-zola-paris` | Émile Zola | Paris | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 9169 |
| `vizetelly-zola-rome` | Émile Zola | Rome | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 8726 |
| `vizetelly-zola-the-conquest-of-plassans-la-conqu-te-de-plassans` | Émile Zola | The Conquest of Plassans (La Conquête de Plassans) | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 56860 |
| `vizetelly-zola-the-downfall-la-d-b-cle-a-story-of-the-horrors-o` | Émile Zola | The Downfall (La Débâcle): A Story of the Horrors o | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 56799 |
| `vizetelly-zola-the-fat-and-the-thin` | Émile Zola | The Fat and the Thin | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 5744 |
| `vizetelly-zola-the-fortune-of-the-rougons` | Émile Zola | The Fortune of the Rougons | Ernest Alfred Vizetelly (named in the Gutenberg header as editor) | 1886-1906 (Chatto and Windus) | have | PG 5135 |
| `vizetelly-zola-the-ladies-paradise` | Émile Zola | The Ladies' Paradise | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 54726 |
| `vizetelly-zola-the-rush-for-the-spoil-la-cur-e-a-realistic-nove` | Émile Zola | The Rush for the Spoil (La Curée): A Realistic Novel | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 56590 |
| `vizetelly-zola-theresa-raquin` | Émile Zola | Theresa Raquin | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 6626 |
| `vizetelly-zola-truth-v-rit` | Émile Zola | Truth [Vérité] | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 55849 |
| `vizetelly-zola-work-travail` | Émile Zola | Work [Travail] | Ernest Alfred Vizetelly | 1886-1906 (Chatto and Windus) | have | PG 55282 |
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
| `leland-heine-scheffel-gaudeamus` | Joseph Victor von Scheffel | Gaudeamus! Humorous Poems | Charles Godfrey Leland | 1872 | have | PG 35848 |
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
| `koteliansky-bunin-gentleman-from-san-francisco` | Bunin | The Gentleman from San Francisco and Other Stories | S. S. Koteliansky and Leonard Woolf; the title story by D. H. Lawrence and S. S. Koteliansky (the book's own erratum note) | 1922 | have | PG 44998 |
| `koteliansky-chekhov-note-book` | Chekhov | Note-Book of Anton Chekhov | S. S. Koteliansky and Leonard Woolf | 1921 | have | PG 12494 |
| `koteliansky-chekhov-the-bet` | Chekhov | The Bet, and Other Stories | S. S. Koteliansky and J. M. Murry | 1915 | have | PG 55283 |
| `koteliansky-countess-tolstoy-autobiography` | S. A. Tolstaya | Autobiography of Countess Tolstoy | S. S. Koteliansky and Leonard Woolf | 1922 | have | PG 38027 |
| `koteliansky-dostoevsky-stavrogins-confession` | Fyodor Dostoevsky | Stavrogin's Confession and The Plan of The Life of a Great Sinner | S. S. Koteliansky and Virginia Woolf | 1922 | have | PG 57050 |
| `koteliansky-goldenweizer-talks-with-tolstoi` | A. B. Goldenweizer | Talks with Tolstoi | S. S. Koteliansky and Virginia Woolf | 1923 | have | PG 65159 |
| `koteliansky-gorky-reminiscences-of-chekhov` | Gorky | Reminiscences of Anton Chekhov | S. S. Koteliansky and Leonard Woolf | 1921 | have | PG 37129 |
| `koteliansky-gorky-reminiscences-of-tolstoy` | Gorky | Reminiscences of Leo Nicolayevitch Tolstoi | S. S. Koteliansky and Leonard Woolf | 1920 | have | PG 55284 |
| `koteliansky-kuprin-river-of-life` | Kuprin | The River of Life, and Other Stories | S. S. Koteliansky and J. M. Murry | 1916 | have | PG 58406 |
| `koteliansky-shestov-all-things-are-possible` | Shestov | All Things are Possible | S. S. Koteliansky (foreword by D. H. Lawrence) | 1920 | have | PG 57369 |
| `koteliansky-shestov-anton-tchekhov` | Shestov | Anton Tchekhov, and Other Essays | S. S. Koteliansky and J. M. Murry | 1916 | have | PG 56758 |

## Marian Fell (Chekhov, Korolenko)

Shelf: `pipeline/marian-fell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py marian-fell` · titles `python3 pipeline/split_shelf_titles.py marian-fell`.
Round 17 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `marian-fell-chekhov-plays` | Anton Chekhov | Plays: Uncle Vanya, Ivanoff, The Sea-Gull, The Swan Song | Marian Fell | 1912 | have-raw | IA `cu31924063791770` |
| `marian-fell-chekhov-russian-silhouettes` | Chekhov | Russian Silhouettes: More Stories of Russian Life | Marian Fell | 1915 | have | PG 66790 |
| `marian-fell-chekhov-swan-song` | Chekhov | Swan Song | Marian Fell | 1912 | have | PG 1753 |
| `marian-fell-korolenko-makars-dream` | Korolenko | Makar's Dream, and Other Stories | Marian Fell | 1916 | have | PG 62555 |

## Thomas Seltzer (Gorky, Andreyev, Gogol, Sudermann)

Shelf: `pipeline/seltzer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py seltzer` · titles `python3 pipeline/split_shelf_titles.py seltzer`.
Round 17 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `seltzer-andreyev-savva-and-life-of-man` | Andreyev | Savva and The Life of Man | Thomas Seltzer | 1914 | have | PG 13147 |
| `seltzer-gogol-inspector-general` | Gogol | The Inspector-General | Thomas Seltzer | 1916 | have | PG 3735 |
| `seltzer-gorky-the-spy` | Gorky | The Spy: The Story of a Superfluous Man | Thomas Seltzer | 1908 | have | PG 51094 |
| `seltzer-ostwald-natural-philosophy` | Ostwald | Natural Philosophy | Thomas Seltzer | 1910 | have | PG 43791 |
| `seltzer-sudermann-song-of-songs` | Sudermann | The Song of Songs | Thomas Seltzer | 1909 | have | PG 34791 |
| — | — | pg-13437: Best Russian Short Stories (1917): an anthology Seltzer edited, with many translators. | — | — | excluded | — |
| — | — | pg-17241: Atlantis: Adele Szold Seltzer's translation; it is on adele-seltzer_shelf.json (round 35). | — | — | excluded | — |
| — | — | pg-62880: The Glebe magazine issue: a periodical. | — | — | excluded | — |
| — | — | pg-3165: Rashi: Adele Szold Seltzer's translation; it is on adele-seltzer_shelf.json (round 35). | — | — | excluded | — |
| — | — | pg-22354: The Adventures of Maya the Bee: Adele Szold Seltzer's translation; it is on adele-seltzer_shelf.json (round 35). | — | — | excluded | — |
| — | — | pg-33943: Woman: Adele Szold Seltzer's translation; it is on adele-seltzer_shelf.json (round 35). | — | — | excluded | — |
| — | — | pg-34358: Iolanthe's Wedding: Adele Szold Seltzer's translation; it is on adele-seltzer_shelf.json (round 35). | — | — | excluded | — |

## Nathan Haskell Dole (Tolstoy, Palacio Valdés, Verga)

Shelf: `pipeline/dole_shelf.json` · fetch `python3 pipeline/fetch_shelf.py dole` · titles `python3 pipeline/split_shelf_titles.py dole`.
Round 17 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `dole-dupuy-great-masters-of-russian-literature` | Ernest Dupuy | The Great Masters of Russian Literature in the Nineteenth Century | Nathan Haskell Dole | 1886 | have | PG 71884 |
| `dole-palacio-valdes-marquis-of-penalta` | Palacio Valdés | The Marquis of Peñalta (Marta y María) | Nathan Haskell Dole | 1886 | have | PG 37969 |
| `dole-palacio-valdes-maximina` | Palacio Valdés | Maximina | Nathan Haskell Dole | 1888 | have | PG 33244 |
| `dole-suttner-when-thoughts-will-soar` | Bertha von Suttner | When Thoughts Will Soar | Nathan Haskell Dole | 1914 | have | PG 63599 |
| `dole-tolstoy-the-invaders` | Tolstoy | The Invaders, and Other Stories | Nathan Haskell Dole | 1887 | have | PG 56797 |
| `dole-tolstoy-where-love-is` | Tolstoy | Where Love is There God is Also | Nathan Haskell Dole | 1887 | have | PG 38616 |
| `dole-verga-under-the-shadow-of-etna` | Verga | Under the Shadow of Etna: Sicilian Stories | Nathan Haskell Dole | 1896 | have | PG 37979 |
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
| `clara-bell-balzac-a-man-of-business` | Honoré de Balzac | A Man of Business | Clara Bell | 1890s (Dent) | have | PG 1813 |
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
| `clara-bell-schubin-our-own-set` | Ossip Schubin | Our Own Set | Clara Bell | 1884 | have | PG 35673 |
| `clara-bell-vald-froth-a-novel` | Armando Palacio Valdé | Froth: A Novel | Clara Bell | before 1931 (see the Gutenberg header) | have | PG 38411 |
| `clara-bell-van-eeden-little-johannes` | Frederik van Eeden | Little Johannes | Clara Bell (introduction by Andrew Lang) | 1895 | have | PG 40656 |
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
| `de-leon-marx-the-eighteenth-brumaire-of-louis-bonaparte` | Karl Marx | The Eighteenth Brumaire of Louis Bonaparte | Daniel De Leon | 1898 | have | PG 1346 |
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

## Julius West (Chekhov's Plays, Second Series)

Shelf: `pipeline/julius-west_shelf.json` · fetch `python3 pipeline/fetch_shelf.py julius-west` · titles `python3 pipeline/split_shelf_titles.py julius-west`.
Round 26 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `julius-west-chekhov-plays-second-series` | Anton Chekhov | Plays, Second Series: On the High Road, The Proposal, The Wedding, The Bear, A Tragedian in Spite of Himself, The Anniversary, The Three Sisters, The Cherry Orchard | Julius West | 1916 | have | PG 7986 |

## George Calderon (Chekhov's Seagull and Cherry Orchard; Ilya Tolstoy)

Shelf: `pipeline/george-calderon_shelf.json` · fetch `python3 pipeline/fetch_shelf.py george-calderon` · titles `python3 pipeline/split_shelf_titles.py george-calderon`.
Round 26 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `george-calderon-ilya-tolstoy-reminiscences` | Ilya Tolstoy | Reminiscences of Tolstoy, by His Son | George Calderon | 1914 | have | PG 813 |
| `george-calderon-chekhov-two-plays` | Anton Chekhov | Two Plays by Tchekhof: The Seagull; The Cherry Orchard | George Calderon | 1912 | have-raw | IA `twoplaysbytchekh00chekiala` |

## Thomas Johnes (Monstrelet's Chronicles)

Shelf: `pipeline/johnes_shelf.json` · fetch `python3 pipeline/fetch_shelf.py johnes` · titles `python3 pipeline/split_shelf_titles.py johnes`.
Round 27 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `johnes-monstrelet-chronicles-vol-01` | Enguerrand de Monstrelet | The chronicles of Enguerrand de Monstrelet, Vol. 01 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 50839 |
| `johnes-monstrelet-chronicles-vol-02` | Enguerrand de Monstrelet | The chronicles of Enguerrand de Monstrelet, Vol. 02 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 52607 |
| `johnes-monstrelet-chronicles-vol-03` | Enguerrand de Monstrelet | The Chronicles of Enguerrand de Monstrelet, Vol. 03 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 52911 |
| `johnes-monstrelet-chronicles-vol-04` | Enguerrand de Monstrelet | The chronicles of Enguerrand de Monstrelet, Vol. 04 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 52889 |
| `johnes-monstrelet-chronicles-vol-05` | Enguerrand de Monstrelet | The chronicles of Enguerrand de Monstrelet, Vol. 05 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 73983 |
| `johnes-monstrelet-chronicles-vol-06` | Enguerrand de Monstrelet | The chronicles of Enguerrand de Monstrelet, Vol. 06 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 64948 |
| `johnes-monstrelet-chronicles-vol-07` | Enguerrand de Monstrelet | The chronicles of Enguerrand de Monstrelet, Vol. 07 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 58083 |
| `johnes-monstrelet-chronicles-vol-08` | Enguerrand de Monstrelet | The chronicles of Enguerrand de Monstrelet, Vol. 08 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 63913 |
| `johnes-monstrelet-chronicles-vol-09` | Enguerrand de Monstrelet | The chronicles of Enguerrand de Monstrelet, Vol. 09 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 73160 |
| `johnes-monstrelet-chronicles-vol-10` | Enguerrand de Monstrelet | The chronicles of Enguerrand de Monstrelet, Vol. 10 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 65396 |
| `johnes-monstrelet-chronicles-vol-11` | Enguerrand de Monstrelet | The chronicles of Enguerrand de Monstrelet, Vol. 11 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 74647 |
| `johnes-monstrelet-chronicles-vol-12` | Enguerrand de Monstrelet | The chronicles of Enguerrand de Monstrelet, Vol. 12 [of 13] | Thomas Johnes | 1809-1810 (see the Gutenberg header) | have | PG 65721 |

## R. H. M. Elwes (Spinoza)

Shelf: `pipeline/elwes_shelf.json` · fetch `python3 pipeline/fetch_shelf.py elwes` · titles `python3 pipeline/split_shelf_titles.py elwes`.
Round 27 (2026-10-10), vetoable. Ethics held on adler_shelf.json. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `elwes-spinoza-ethics` | Benedictus de Spinoza | Ethics | R. H. M. Elwes | 1883 | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `spinoza-ethics` (PG 3800) |
| `elwes-spinoza-on-the-improvement-of-the-understanding` | Benedictus de Spinoza | On the Improvement of the Understanding | R. H. M. Elwes | 1883 (Bohn's Philosophical Library; see the Gutenberg header) | have | PG 1016 |
| `elwes-spinoza-theologico-political-treatise-part-1` | Benedictus de Spinoza | Theologico-Political Treatise — Part 1 | R. H. M. Elwes | 1883 (Bohn's Philosophical Library; see the Gutenberg header) | have | PG 989 |
| `elwes-spinoza-theologico-political-treatise-part-2` | Benedictus de Spinoza | Theologico-Political Treatise — Part 2 | R. H. M. Elwes | 1883 (Bohn's Philosophical Library; see the Gutenberg header) | have | PG 990 |
| `elwes-spinoza-theologico-political-treatise-part-3` | Benedictus de Spinoza | A Theological-Political Treatise [Part III] | R. H. M. Elwes | 1883 (Bohn's Philosophical Library; see the Gutenberg header) | have | PG 991 |
| `elwes-spinoza-theologico-political-treatise-part-4` | Benedictus de Spinoza | A Theological-Political Treatise [Part IV] | R. H. M. Elwes | 1883 (Bohn's Philosophical Library; see the Gutenberg header) | have | PG 992 |
| — | — | ethics: The Ethics: the complete text (3800) is on adler_shelf.json; Gutenberg's five part-files (919-975) are left out. | — | — | excluded | — |

## William F. Fleming (Voltaire's Philosophical Dictionary)

Shelf: `pipeline/fleming_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fleming` · titles `python3 pipeline/split_shelf_titles.py fleming`.
Round 27 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fleming-voltaire-a-philosophical-dictionary-volume-01` | Voltaire | A Philosophical Dictionary, Volume 01 | William F. Fleming | 1901 (see the Gutenberg header) | have | PG 35621 |
| `fleming-voltaire-a-philosophical-dictionary-volume-02` | Voltaire | A Philosophical Dictionary, Volume 02 | William F. Fleming | 1901 (see the Gutenberg header) | have | PG 35622 |
| `fleming-voltaire-a-philosophical-dictionary-volume-03` | Voltaire | A Philosophical Dictionary, Volume 03 | William F. Fleming | 1901 (see the Gutenberg header) | have | PG 35623 |
| `fleming-voltaire-a-philosophical-dictionary-volume-04` | Voltaire | A Philosophical Dictionary, Volume 04 | William F. Fleming | 1901 (see the Gutenberg header) | have | PG 35624 |
| `fleming-voltaire-a-philosophical-dictionary-volume-05` | Voltaire | A Philosophical Dictionary, Volume 05 | William F. Fleming | 1901 (see the Gutenberg header) | have | PG 35625 |
| `fleming-voltaire-a-philosophical-dictionary-volume-06` | Voltaire | A Philosophical Dictionary, Volume 06 | William F. Fleming | 1901 (see the Gutenberg header) | have | PG 35626 |
| `fleming-voltaire-a-philosophical-dictionary-volume-07` | Voltaire | A Philosophical Dictionary, Volume 07 | William F. Fleming | 1901 (see the Gutenberg header) | have | PG 35627 |
| `fleming-voltaire-a-philosophical-dictionary-volume-08` | Voltaire | A Philosophical Dictionary, Volume 08 | William F. Fleming | 1901 (see the Gutenberg header) | have | PG 35628 |
| `fleming-voltaire-a-philosophical-dictionary-volume-09` | Voltaire | A Philosophical Dictionary, Volume 09 | William F. Fleming | 1901 (see the Gutenberg header) | have | PG 35629 |
| `fleming-voltaire-a-philosophical-dictionary-volume-10` | Voltaire | A Philosophical Dictionary, Volume 10 | William F. Fleming | 1901 (see the Gutenberg header) | have | PG 35630 |
| `fleming-voltaire-the-works-of-voltaire-vol-iv-of-xliii` | Voltaire | The Works of Voltaire, Vol. IV of XLIII. | William F. Fleming | 1901 (see the Gutenberg header) | have | PG 49726 |

## M. L. McClure (Maspero's History of Egypt and the Ancient East)

Shelf: `pipeline/mcclure_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mcclure` · titles `python3 pipeline/split_shelf_titles.py mcclure`.
Round 27 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mcclure-maspero-history-of-egypt-chaldaea-syria-babyloni` | G. (Gaston) Maspero | History of Egypt, Chaldæa, Syria, Babylonia, and Assyria | M. L. McClure | 1903-1906 (see the Gutenberg header) | have | PG 28876 |
| — | — | maspero-volumes: Gutenberg's volume files are left out; the complete text (28876) is used. | — | — | excluded | — |

## Douglas Ainslie (Croce)

Shelf: `pipeline/ainslie_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ainslie` · titles `python3 pipeline/split_shelf_titles.py ainslie`.
Round 27 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ainslie-croce-aesthetic-1909` | Benedetto Croce | Aesthetic as Science of Expression and General Linguistic | Douglas Ainslie | 1909-1922 (see the Gutenberg header) | have | PG 9306 |
| `ainslie-croce-aesthetic-1922` | Benedetto Croce | Æsthetic as science of expression and general linguistic | Douglas Ainslie | 1909-1922 (see the Gutenberg header) | have | PG 54618 |
| `ainslie-croce-ariosto-shakespeare-and-corneille` | Benedetto Croce | Ariosto, Shakespeare and Corneille | Douglas Ainslie | 1909-1922 (see the Gutenberg header) | have | PG 54165 |
| `ainslie-croce-logic-as-the-science-of-the-pure-concept` | Benedetto Croce | Logic as the Science of the Pure Concept | Douglas Ainslie | 1909-1922 (see the Gutenberg header) | have | PG 54137 |
| `ainslie-croce-the-philosophy-of-the-practical-economic` | Benedetto Croce | The Philosophy of the Practical: Economic and Ethic | Douglas Ainslie | 1909-1922 (see the Gutenberg header) | have | PG 54938 |
| `ainslie-croce-theory-history-of-historiography` | Benedetto Croce | Theory & History of Historiography | Douglas Ainslie | 1909-1922 (see the Gutenberg header) | have | PG 54642 |

## Charles E. Derbyshire (Rizal)

Shelf: `pipeline/derbyshire_shelf.json` · fetch `python3 pipeline/fetch_shelf.py derbyshire` · titles `python3 pipeline/split_shelf_titles.py derbyshire`.
Round 27 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `derbyshire-rizal-the-indolence-of-the-filipino` | José Rizal | The Indolence of the Filipino | Charles E. Derbyshire | 1912-1913 (see the Gutenberg header) | have | PG 6885 |
| `derbyshire-rizal-the-philippines-a-century-hence` | José Rizal | The Philippines a Century Hence | Charles E. Derbyshire | 1912-1913 (see the Gutenberg header) | have | PG 35899 |
| `derbyshire-rizal-the-reign-of-greed` | José Rizal | The Reign of Greed | Charles E. Derbyshire | 1912-1913 (see the Gutenberg header) | have | PG 10676 |
| `derbyshire-rizal-the-social-cancer-a-complete-english-ver` | José Rizal | The Social Cancer: A Complete English Version of Noli Me Tangere | Charles E. Derbyshire | 1912-1913 (see the Gutenberg header) | have | PG 6737 |

## Gilbert Cannan (Rolland's Jean-Christophe)

Shelf: `pipeline/gilbert-cannan_shelf.json` · fetch `python3 pipeline/fetch_shelf.py gilbert-cannan` · titles `python3 pipeline/split_shelf_titles.py gilbert-cannan`.
Round 27 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `gilbert-cannan-chekhov-the-house-with-the-mezzanine-and-other-s` | Anton Pavlovich Chekhov | The House with the Mezzanine and Other Stories | Gilbert Cannan (with S. S. Koteliansky) | 1910-1917 (see the Gutenberg header) | have | PG 27411 |
| `gilbert-cannan-rolland-jean-christophe-in-paris-the-market-plac` | Romain Rolland | Jean-Christophe in Paris: The Market-Place, Antoinette, the House | Gilbert Cannan | 1910-1917 (see the Gutenberg header) | have | PG 8149 |
| `gilbert-cannan-rolland-jean-christophe-journey-s-end` | Romain Rolland | Jean-Christophe Journey's End | Gilbert Cannan | 1910-1917 (see the Gutenberg header) | have | PG 7967 |
| `gilbert-cannan-rolland-jean-christophe-volume-i` | Romain Rolland | Jean-Christophe, Volume I | Gilbert Cannan | 1910-1917 (see the Gutenberg header) | have | PG 7979 |

## Ludwig Lewisohn (Wassermann, Sudermann)

Shelf: `pipeline/lewisohn_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lewisohn` · titles `python3 pipeline/split_shelf_titles.py lewisohn`.
Round 27 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lewisohn-sudermann-the-indian-lily-and-other-stories` | Hermann Sudermann | The Indian Lily and Other Stories | Ludwig Lewisohn | 1911-1922 (see the Gutenberg header) | have | PG 9994 |
| `lewisohn-wassermann-the-goose-man` | Jakob Wassermann | The Goose Man | Ludwig Lewisohn (with Allen Wilson Porterfield) | 1911-1922 (see the Gutenberg header) | have | PG 25345 |
| `lewisohn-wassermann-the-world-s-illusion-volume-1-of-2-eva` | Jakob Wassermann | The World's Illusion, Volume 1 (of 2): Eva | Ludwig Lewisohn | 1911-1922 (see the Gutenberg header) | have | PG 54794 |
| `lewisohn-wassermann-the-world-s-illusion-volume-2-of-2-ruth` | Jakob Wassermann | The World's Illusion, Volume 2 (of 2): Ruth | Ludwig Lewisohn | 1911-1922 (see the Gutenberg header) | have | PG 57847 |

## Henri Van Laun (Taine's History of English Literature; La Bruyère)

Shelf: `pipeline/van-laun_shelf.json` · fetch `python3 pipeline/fetch_shelf.py van-laun` · titles `python3 pipeline/split_shelf_titles.py van-laun`.
Round 27 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `van-laun-bruyere-the-characters-of-jean-de-la-bruyere` | Jean de La Bruyère | The "Characters" of Jean de La Bruyère | Henri Van Laun | 1871-1885 (see the Gutenberg header) | have | PG 46633 |
| `van-laun-taine-history-of-english-literature-volume-1-o` | Hippolyte Taine | History of English Literature Volume 1 (of 3) | Henri Van Laun | 1871-1885 (see the Gutenberg header) | have | PG 61308 |
| `van-laun-taine-history-of-english-literature-volume-2-o` | Hippolyte Taine | History of English Literature Volume 2 (of 3) | Henri Van Laun | 1871-1885 (see the Gutenberg header) | have | PG 61382 |
| `van-laun-taine-history-of-english-literature-volume-3-o` | Hippolyte Taine | History of English Literature Volume 3 (of 3) | Henri Van Laun | 1871-1885 (see the Gutenberg header) | have | PG 61510 |

## Eugene Mason (Wace, Layamon, Marie de France, Aucassin)

Shelf: `pipeline/eugene-mason_shelf.json` · fetch `python3 pipeline/fetch_shelf.py eugene-mason` · titles `python3 pipeline/split_shelf_titles.py eugene-mason`.
Round 27 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `eugene-mason-aucassin-and-nicolette` | Various (medieval French) | Aucassin & Nicolette, and Other Mediæval Romances and Legends | Eugene Mason | 1910-1912 (Everyman's Library; see the Gutenberg header) | have | PG 38110 |
| `eugene-mason-layamon-brut` | Layamon | Layamon's Brut | Eugene Mason | 1910-1912 (Everyman's Library; see the Gutenberg header) | have | PG 14305 |
| `eugene-mason-marie-de-france-lays` | Marie de France | French Mediaeval Romances from the Lays of Marie de France | Eugene Mason | 1910-1912 (Everyman's Library; see the Gutenberg header) | have | PG 11417 |
| `eugene-mason-wace-arthurian-chronicles-roman-de-brut` | Wace | Arthurian Chronicles: Roman de Brut | Eugene Mason | 1910-1912 (Everyman's Library; see the Gutenberg header) | have | PG 10472 |

## Eleanor Grove (Ebers's An Egyptian Princess)

Shelf: `pipeline/eleanor-grove_shelf.json` · fetch `python3 pipeline/fetch_shelf.py eleanor-grove` · titles `python3 pipeline/split_shelf_titles.py eleanor-grove`.
Round 27 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `eleanor-grove-ebers-an-egyptian-princess-complete` | Georg Ebers | An Egyptian Princess — Complete | Eleanor Grove | 1880 (see the Gutenberg header) | have | PG 5460 |
| — | — | volumes: The ten Gutenberg part-files are left out; the complete text (5460) is used. | — | — | excluded | — |

## Lady Mary Loyd (Mérimée, Stendhal's Chartreuse of Parma)

Shelf: `pipeline/mary-loyd_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mary-loyd` · titles `python3 pipeline/split_shelf_titles.py mary-loyd`.
Round 28 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mary-loyd-joinville-memoirs` | François d'Orléans, Prince de Joinville | Memoirs (Vieux Souvenirs) of the Prince de Joinville | Lady Mary Loyd | 1895-1905 (see the Gutenberg header) | have | PG 5716 |
| `mary-loyd-merimee-carmen` | Prosper Mérimée | Carmen | Lady Mary Loyd | 1895-1905 (see the Gutenberg header) | have | PG 2465 |
| `mary-loyd-merimee-colomba` | Prosper Mérimée | Colomba | Lady Mary Loyd | 1895-1905 (see the Gutenberg header) | have | PG 2708 |
| `mary-loyd-stendhal-the-chartreuse-of-parma` | Stendhal | The Chartreuse of Parma | Lady Mary Loyd | 1895-1905 (see the Gutenberg header) | have | PG 57638 |

## H. E. Krehbiel (Thayer's Life of Beethoven; Kerst's Mozart)

Shelf: `pipeline/krehbiel_shelf.json` · fetch `python3 pipeline/fetch_shelf.py krehbiel` · titles `python3 pipeline/split_shelf_titles.py krehbiel`.
Round 28 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `krehbiel-kerst-mozart-the-man-and-the-artist` | Wolfgang Amadeus Mozart | Mozart: The Man and the Artist, as Revealed in His Own Words | Henry Edward Krehbiel | 1905-1921 (see the Gutenberg header) | have | PG 4042 |
| `krehbiel-thayer-life-of-beethoven-vol-1` | Alexander Wheelock Thayer | The Life of Ludwig van Beethoven, Volume I | Henry Edward Krehbiel | 1905-1921 (see the Gutenberg header) | have | PG 43591 |
| `krehbiel-thayer-life-of-beethoven-vol-2` | Alexander Wheelock Thayer | The Life of Ludwig van Beethoven, Volume II | Henry Edward Krehbiel | 1905-1921 (see the Gutenberg header) | have | PG 43592 |
| `krehbiel-thayer-life-of-beethoven-vol-3` | Alexander Wheelock Thayer | The Life of Ludwig van Beethoven, Volume III | Henry Edward Krehbiel | 1905-1921 (see the Gutenberg header) | have | PG 43593 |

## Frances Cashel Hoey (Rémusat's Memoirs; Verne)

Shelf: `pipeline/frances-hoey_shelf.json` · fetch `python3 pipeline/fetch_shelf.py frances-hoey` · titles `python3 pipeline/split_shelf_titles.py frances-hoey`.
Round 28 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `frances-hoey-challamel-the-history-of-fashion-in-france` | Augustin Challamel | The history of fashion in France | Frances Cashel Hoey (with John Lillie) | 1880-1898 (see the Gutenberg header) | have | PG 76717 |
| `frances-hoey-remusat-memoirs-vol-1` | Madame de Rémusat | Memoirs of the Empress Josephine, Vol. 1 of 2 | Frances Cashel Hoey (with John Lillie) | 1880-1898 (see the Gutenberg header) | have | PG 49175 |
| `frances-hoey-remusat-memoirs-vol-2` | Madame de Rémusat | Memoirs of the Empress Josephine, Vol. 2 of 2 | Frances Cashel Hoey (with John Lillie) | 1880-1898 (see the Gutenberg header) | have | PG 49176 |
| `frances-hoey-verne-an-antarctic-mystery` | Jules Verne | An Antarctic Mystery | Frances Cashel Hoey | 1880-1898 (see the Gutenberg header) | have | PG 10339 |

## H. W. Dulcken (Ida Pfeiffer's travels)

Shelf: `pipeline/dulcken_shelf.json` · fetch `python3 pipeline/fetch_shelf.py dulcken` · titles `python3 pipeline/split_shelf_titles.py dulcken`.
Round 28 (2026-10-10), vetoable. His Andersen is on andersen_shelf.json. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `dulcken-pfeiffer-a-visit-to-the-holy-land-egypt-and-italy` | Ida Pfeiffer | A Visit to the Holy Land, Egypt, and Italy | H. W. Dulcken | 1852-1861 (see the Gutenberg header) | have | PG 12561 |
| `dulcken-pfeiffer-the-last-travels-of-ida-pfeiffer-inclusi` | Ida Pfeiffer | The last travels of Ida Pfeiffer: inclusive of a visit to Madagascar, with a biographical memoir of the author | H. W. Dulcken | 1852-1861 (see the Gutenberg header) | have | PG 60474 |
| — | — | andersen: What the Moon Saw (27000) is on andersen_shelf.json; The Nightingale (71096) is left for that shelf's owner. | — | — | excluded | — |

## Edgar Prestage (Azurara's Chronicle of Guinea; Eça de Queirós)

Shelf: `pipeline/prestage_shelf.json` · fetch `python3 pipeline/fetch_shelf.py prestage` · titles `python3 pipeline/split_shelf_titles.py prestage`.
Round 28 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `prestage-alcoforado-the-letters-of-a-portuguese-nun` | Mariana Alcoforado (attributed; perhaps Guilleragues) | The Letters of a Portuguese Nun | Edgar Prestage | 1893 | have | PG 57403 |
| `prestage-queiros-our-lady-of-the-pillar` | Eça de Queirós | Our Lady of the Pillar | Edgar Prestage | 1896-1906 (see the Gutenberg header) | have | PG 56670 |
| `prestage-queiros-the-sweet-miracle` | Eça de Queirós | The sweet miracle | Edgar Prestage | 1896-1906 (see the Gutenberg header) | have | PG 74802 |
| `prestage-zurara-chronicle-of-guinea-vol-1` | Gomes Eannes de Zurara | The Chronicle of the Discovery and Conquest of Guinea. Vol. I | Edgar Prestage (with C. Raymond Beazley) | 1896-1906 (see the Gutenberg header) | have | PG 35738 |
| `prestage-zurara-chronicle-of-guinea-vol-2` | Gomes Eannes de Zurara | The Chronicle of the Discovery and Conquest of Guinea. Vol. II | Edgar Prestage (with C. Raymond Beazley) | 1896-1906 (see the Gutenberg header) | have | PG 35764 |

## Dorothy Bussy (Gide)

Shelf: `pipeline/dorothy-bussy_shelf.json` · fetch `python3 pipeline/fetch_shelf.py dorothy-bussy` · titles `python3 pipeline/split_shelf_titles.py dorothy-bussy`.
Round 28 (2026-10-10), vetoable. One 1930 Knopf printing. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `dorothy-bussy-gide-strait-is-the-gate-la-porte-etroite` | André Gide | Strait is the gate (La porte étroite) | Dorothy Bussy | 1924-1930 (see the Gutenberg header) | have | PG 79693 |
| `dorothy-bussy-gide-the-counterfeiters` | André Gide | The counterfeiters | Dorothy Bussy | 1924-1930 (see the Gutenberg header) | have | PG 76965 |
| `dorothy-bussy-gide-the-immoralist` | André Gide | The immoralist | Dorothy Bussy | 1924-1930 (see the Gutenberg header) | have | PG 78975 |
| `dorothy-bussy-gide-the-vatican-swindle` | André Gide | The Vatican swindle | Dorothy Bussy | 1924-1930 (see the Gutenberg header) | have | PG 73838 |

## M. H. Dziewicki (Reymont's The Peasants)

Shelf: `pipeline/dziewicki_shelf.json` · fetch `python3 pipeline/fetch_shelf.py dziewicki` · titles `python3 pipeline/split_shelf_titles.py dziewicki`.
Round 28 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `dziewicki-reymont-the-peasants-vol-1` | Władysław Stanisław Reymont | The peasants, [vol. 1] | Michael Henry Dziewicki | 1924-1925 (see the Gutenberg header) | have | PG 75846 |
| `dziewicki-reymont-the-peasants-vol-2` | Władysław Stanisław Reymont | The peasants, [vol. 2] | Michael Henry Dziewicki | 1924-1925 (see the Gutenberg header) | have | PG 76328 |
| `dziewicki-reymont-the-peasants-vol-3` | Władysław Stanisław Reymont | The peasants, [vol. 3] | Michael Henry Dziewicki | 1924-1925 (see the Gutenberg header) | have | PG 76330 |
| `dziewicki-reymont-the-peasants-vol-4` | Władysław Stanisław Reymont | The peasants, [vol. 4] | Michael Henry Dziewicki | 1924-1925 (see the Gutenberg header) | have | PG 76329 |

## Anna Swanwick (Goethe, Schiller)

Shelf: `pipeline/swanwick_shelf.json` · fetch `python3 pipeline/fetch_shelf.py swanwick` · titles `python3 pipeline/split_shelf_titles.py swanwick`.
Round 28 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `swanwick-goethe-egmont` | Johann Wolfgang von Goethe | Egmont | Anna Swanwick | 1843-1850 (see the Gutenberg header) | have | PG 1945 |
| `swanwick-goethe-iphigenia-in-tauris` | Johann Wolfgang von Goethe | Iphigenia in Tauris | Anna Swanwick | 1843-1850 (see the Gutenberg header) | have | PG 15850 |
| `swanwick-schiller-the-maid-of-orleans-a-tragedy` | Friedrich Schiller | The Maid of Orleans: A Tragedy | Anna Swanwick | 1843-1850 (see the Gutenberg header) | have | PG 6792 |

## John Oxenford (Goethe's Autobiography; Tales from the German)

Shelf: `pipeline/oxenford_shelf.json` · fetch `python3 pipeline/fetch_shelf.py oxenford` · titles `python3 pipeline/split_shelf_titles.py oxenford`.
Round 28 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `oxenford-goethe-the-autobiography-of-goethe` | Johann Wolfgang von Goethe | The Autobiography of Goethe | John Oxenford (with A. J. W. Morrison) | 1844-1848 (see the Gutenberg header) | have | PG 52654 |
| `oxenford-tales-from-the-german` | Various (Hauff, Hoffmann and others) | Tales from the German, comprising specimens from the most celebrated authors | John Oxenford (with C. A. Feiling) | 1844-1848 (see the Gutenberg header) | have | PG 32046 |
| — | — | pg-5733: Truth and Fiction (5733) is Oxenford's part alone, about half the text of the full Bohn Autobiography (52654), which is used. | — | — | excluded | — |

## Sir Monier Monier-Williams (Sakoontala; the Siksha-Patri)

Shelf: `pipeline/monier-williams_shelf.json` · fetch `python3 pipeline/fetch_shelf.py monier-williams` · titles `python3 pipeline/split_shelf_titles.py monier-williams`.
Round 28 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `monier-williams-kalidasa-sakoontala-or-the-lost-ring-an-indian-dr` | Kālidāsa | Sakoontala; Or, The Lost Ring: An Indian Drama | Monier Monier-Williams | 1853-1882 (see the Gutenberg header) | have | PG 12169 |
| `monier-williams-siksha-patri` | Sahajanand Swami (the Svami-Narayana sect) | The Siksha-Patri of the Svami-Narayana Sect | Monier Monier-Williams | 1853-1882 (see the Gutenberg header) | have | PG 7261 |
| — | — | pg-13268: Hindu Literature (Colonial Press, 1900) is a compilation of several translators (Arnold, Toru Dutt and others), not his alone. | — | — | excluded | — |

## John J. Lalor (Roscher; Nohl's Mozart and Beethoven)

Shelf: `pipeline/lalor_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lalor` · titles `python3 pipeline/split_shelf_titles.py lalor`.
Round 28 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lalor-nohl-life-of-beethoven` | Ludwig Nohl | Life of Beethoven | John J. Lalor | 1878-1881 (see the Gutenberg header) | have | PG 69693 |
| `lalor-nohl-life-of-mozart` | Ludwig Nohl | Life of Mozart | John J. Lalor | 1878-1881 (see the Gutenberg header) | have | PG 67828 |
| `lalor-roscher-principles-of-political-economy-vol-1` | Wilhelm Roscher | Principles of Political Economy, Vol. 1 | John J. Lalor | 1878-1881 (see the Gutenberg header) | have | PG 27698 |
| `lalor-roscher-principles-of-political-economy-vol-2` | Wilhelm Roscher | Principles of Political Economy, Vol. 2 | John J. Lalor | 1878-1881 (see the Gutenberg header) | have | PG 38655 |

## Sir Walter Armstrong (Perrot and Chipiez's histories of ancient art)

Shelf: `pipeline/walter-armstrong_shelf.json` · fetch `python3 pipeline/fetch_shelf.py walter-armstrong` · titles `python3 pipeline/split_shelf_titles.py walter-armstrong`.
Round 28 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `walter-armstrong-perrot-chipiez-art-in-ancient-egypt-vol-1` | Georges Perrot and Charles Chipiez | A History of Art in Ancient Egypt, Vol. 1 (of 2) | Walter Armstrong | 1883-1884 (see the Gutenberg header) | have | PG 40144 |
| `walter-armstrong-perrot-chipiez-art-in-ancient-egypt-vol-2` | Georges Perrot and Charles Chipiez | A History of Art in Ancient Egypt, Vol. 2 (of 2) | Walter Armstrong | 1883-1884 (see the Gutenberg header) | have | PG 40149 |
| `walter-armstrong-perrot-chipiez-art-in-chaldaea-assyria-vol-1` | Georges Perrot and Charles Chipiez | A history of art in Chaldæa & Assyria, Vol. 1 (of 2) | Walter Armstrong | 1883-1884 (see the Gutenberg header) | have | PG 28072 |
| `walter-armstrong-perrot-chipiez-art-in-chaldaea-assyria-vol-2` | Georges Perrot and Charles Chipiez | A history of art in Chaldæa & Assyria, Vol. 2 (of 2) | Walter Armstrong | 1883-1884 (see the Gutenberg header) | have | PG 71842 |

## W. G. Waters (Montaigne's Journal of Travels in Italy, 3 vols)

Shelf: `pipeline/ww-waters_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ww-waters` · titles `python3 pipeline/split_shelf_titles.py ww-waters`.
Round 29 (2026-10-10), vetoable. Straparola stays on its own shelf. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ww-waters-montaigne-journal-of-travels-vol-1` | Michel de Montaigne | The journal of Montaigne's travels in Italy by way of Switzerland and Germany in 1580 and 1581, Volume 1 (of 3) | W. G. Waters | 1903 (see the Gutenberg header) | have | PG 70838 |
| `ww-waters-montaigne-journal-of-travels-vol-2` | Michel de Montaigne | The journal of Montaigne's travels in Italy by way of Switzerland and Germany in 1580 and 1581, Volume 2 (of 3) | W. G. Waters | 1903 (see the Gutenberg header) | have | PG 70839 |
| `ww-waters-montaigne-journal-of-travels-vol-3` | Michel de Montaigne | The journal of Montaigne's travels in Italy by way of Switzerland and Germany in 1580 and 1581, Volume 3 (of 3) | W. G. Waters | 1903 (see the Gutenberg header) | have | PG 70840 |
| — | — | pg-75257: The Nights of Straparola is on straparola_shelf.json. | — | — | excluded | — |

## Edna Worthley Underwood (Hafiz; Mickiewicz's Crimean Sonnets; Balkan and foreign stories)

Shelf: `pipeline/edna-underwood_shelf.json` · fetch `python3 pipeline/fetch_shelf.py edna-underwood` · titles `python3 pipeline/split_shelf_titles.py edna-underwood`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `edna-underwood-famous-stories-from-foreign-countries` | Various | Famous stories from foreign countries | Edna Worthley Underwood | 1912-1922 (see the Gutenberg header) | have | PG 75466 |
| `edna-underwood-hafiz-songs-of-hafiz` | Hafiz | Songs of Hafiz | Edna Worthley Underwood | 1912-1922 (see the Gutenberg header) | have | PG 77453 |
| `edna-underwood-mickiewicz-sonnets-from-the-crimea` | Adam Mickiewicz | Sonnets from the Crimea | Edna Worthley Underwood | 1912-1922 (see the Gutenberg header) | have | PG 27069 |
| `edna-underwood-short-stories-from-the-balkans` | Various | Short stories from the Balkans | Edna Worthley Underwood | 1912-1922 (see the Gutenberg header) | have | PG 73663 |

## Ellen Frothingham (Lessing's Laocoon; Hermann and Dorothea; Auerbach's Edelweiss)

Shelf: `pipeline/ellen-frothingham_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ellen-frothingham` · titles `python3 pipeline/split_shelf_titles.py ellen-frothingham`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ellen-frothingham-auerbach-edelweiss-a-story` | Berthold Auerbach | Edelweiss: A Story | Ellen Frothingham | 1869-1874 (see the Gutenberg header) | have | PG 33007 |
| `ellen-frothingham-goethe-hermann-and-dorothea` | Johann Wolfgang von Goethe | Hermann and Dorothea | Ellen Frothingham | 1869-1874 (see the Gutenberg header) | have | PG 1958 |
| `ellen-frothingham-lessing-laocoon` | Gotthold Ephraim Lessing | Laocoon | Ellen Frothingham | 1869-1874 (see the Gutenberg header) | have | PG 73078 |

## R. Dillon Boylan (Werther; Schiller's Don Carlos)

Shelf: `pipeline/boylan_shelf.json` · fetch `python3 pipeline/fetch_shelf.py boylan` · titles `python3 pipeline/split_shelf_titles.py boylan`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `boylan-goethe-the-sorrows-of-young-werther` | Johann Wolfgang von Goethe | The Sorrows of Young Werther | R. Dillon Boylan | 1847-1854 (see the Gutenberg header) | have | PG 2527 |
| `boylan-schiller-don-carlos-a-play` | Friedrich Schiller | Don Carlos: A Play | R. Dillon Boylan | 1847-1854 (see the Gutenberg header) | have | PG 6789 |
| — | — | pg-78269: The Princess and the Tiger is a Haldeman-Julius Little Blue Book extract of his Goethe. | — | — | excluded | — |

## Thomas Holcroft (Beaumarchais's Marriage of Figaro; Trenck's Life, 2 vols)

Shelf: `pipeline/holcroft_shelf.json` · fetch `python3 pipeline/fetch_shelf.py holcroft` · titles `python3 pipeline/split_shelf_titles.py holcroft`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `holcroft-beaumarchais-the-follies-of-a-day-or-the-marriage-of` | Beaumarchais | The Follies of a Day; or, The Marriage of Figaro | Thomas Holcroft | 1785-1788 (see the Gutenberg header) | have | PG 64953 |
| `holcroft-trenck-life-vol-1` | Friedrich von der Trenck | The Life and Adventures of Baron Trenck, Volume 1 | Thomas Holcroft | 1785-1788 (see the Gutenberg header) | have | PG 2668 |
| `holcroft-trenck-life-vol-2` | Friedrich von der Trenck | The Life and Adventures of Baron Trenck, Volume 2 | Thomas Holcroft | 1785-1788 (see the Gutenberg header) | have | PG 2669 |

## Margaret Armour (The Fall of the Nibelungs; Wagner's Ring in two volumes)

Shelf: `pipeline/margaret-armour_shelf.json` · fetch `python3 pipeline/fetch_shelf.py margaret-armour` · titles `python3 pipeline/split_shelf_titles.py margaret-armour`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `margaret-armour-nibelungenlied-the-fall-of-the-nibelungs` | Anonymous (the Nibelungenlied) | The Fall of the Nibelungs | Margaret Armour | 1897-1911 (see the Gutenberg header) | have | PG 3636 |
| `margaret-armour-wagner-siegfried-the-twilight-of-the-gods` | Richard Wagner | Siegfried & The Twilight of the Gods | Margaret Armour | 1897-1911 (see the Gutenberg header) | have | PG 49507 |
| `margaret-armour-wagner-the-rhinegold-the-valkyrie` | Richard Wagner | The Rhinegold & The Valkyrie | Margaret Armour | 1897-1911 (see the Gutenberg header) | have | PG 48214 |

## Florence Simmonds (Corroyer's Gothic Architecture; Duhamel; Le Goffic)

Shelf: `pipeline/florence-simmonds_shelf.json` · fetch `python3 pipeline/fetch_shelf.py florence-simmonds` · titles `python3 pipeline/split_shelf_titles.py florence-simmonds`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `florence-simmonds-corroyer-gothic-architecture` | Édouard Corroyer | Gothic Architecture | Florence Simmonds | 1893-1918 (see the Gutenberg header) | have | PG 54701 |
| `florence-simmonds-duhamel-the-new-book-of-martyrs` | Georges Duhamel | The New Book of Martyrs | Florence Simmonds | 1893-1918 (see the Gutenberg header) | have | PG 4325 |
| `florence-simmonds-goffic-dixmude-the-epic-of-the-french-marines-o` | Charles Le Goffic | Dixmude: The epic of the French marines (October 17-November 10, 1914) | Florence Simmonds | 1893-1918 (see the Gutenberg header) | have | PG 33929 |

## Bernard Guilbert Guerney (Bunin; Kuprin's Sulamith and Yama)

Shelf: `pipeline/guerney_shelf.json` · fetch `python3 pipeline/fetch_shelf.py guerney` · titles `python3 pipeline/split_shelf_titles.py guerney`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `guerney-bunin-the-dreams-of-chang-and-other-stories` | Ivan Alekseevich Bunin | The dreams of Chang and other stories | Bernard Guilbert Guerney | 1922-1923 (see the Gutenberg header) | have | PG 78224 |
| `guerney-kuprin-sulamith-a-romance-of-antiquity` | A. I. (Aleksandr Ivanovich) Kuprin | Sulamith: A Romance of Antiquity | Bernard Guilbert Guerney | 1922-1923 (see the Gutenberg header) | have | PG 33444 |
| `guerney-kuprin-yama-the-pit-a-novel-in-three-parts` | A. I. (Aleksandr Ivanovich) Kuprin | Yama [The Pit], a Novel in Three Parts | Bernard Guilbert Guerney | 1922-1923 (see the Gutenberg header) | have | PG 4706 |

## Else C. M. Benecke (three volumes of Polish tales)

Shelf: `pipeline/benecke_shelf.json` · fetch `python3 pipeline/fetch_shelf.py benecke` · titles `python3 pipeline/split_shelf_titles.py benecke`.
Round 29 (2026-10-10), vetoable. Selected Polish Tales is keyed from a 1944 reprint of the 1921 text: flagged. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `benecke-more-tales-by-polish-authors` | Various Polish authors (Sienkiewicz, Prus, Żeromski and others) | More Tales by Polish Authors | Else C. M. Benecke (with Marie Busch) | 1915-1921 (see the Gutenberg header) | have | PG 35457 |
| `benecke-selected-polish-tales` | Various Polish authors (Sienkiewicz, Prus, Żeromski and others) | Selected Polish Tales | Else C. M. Benecke (with Marie Busch) | 1915-1921 (see the Gutenberg header) | have | PG 8378 |
| `benecke-tales-by-polish-authors` | Various Polish authors (Sienkiewicz, Prus, Żeromski and others) | Tales by Polish Authors | Else C. M. Benecke | 1915-1921 (see the Gutenberg header) | have | PG 35456 |

## H. T. Lowe-Porter (Mann's Buddenbrooks, 2 vols; Three Essays)

Shelf: `pipeline/lowe-porter_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lowe-porter` · titles `python3 pipeline/split_shelf_titles.py lowe-porter`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lowe-porter-mann-buddenbrooks-vol-1` | Thomas Mann | Buddenbrooks, volume 1 of 2 | H. T. Lowe-Porter | 1924-1929 (see the Gutenberg header) | have | PG 72961 |
| `lowe-porter-mann-buddenbrooks-vol-2` | Thomas Mann | Buddenbrooks, volume 2 of 2 | H. T. Lowe-Porter | 1924-1929 (see the Gutenberg header) | have | PG 72962 |
| `lowe-porter-mann-three-essays` | Thomas Mann | Three essays | H. T. Lowe-Porter | 1924-1929 (see the Gutenberg header) | have | PG 76837 |

## Richard Aldington (Benda's Great Betrayal; Cyrano's Voyages; Sologub)

Shelf: `pipeline/aldington_shelf.json` · fetch `python3 pipeline/fetch_shelf.py aldington` · titles `python3 pipeline/split_shelf_titles.py aldington`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `aldington-benda-the-great-betrayal-la-trahison-des-clerc` | Julien Benda | The great betrayal (La trahison des clercs) | Richard Aldington | 1916-1928 (see the Gutenberg header) | have | PG 78218 |
| `aldington-bergerac-voyages-to-the-moon-and-the-sun` | Cyrano de Bergerac | Voyages to the Moon and the Sun | Richard Aldington | 1916-1928 (see the Gutenberg header) | have | PG 74000 |
| `aldington-sologub-the-little-demon` | Fyodor Sologub | The Little Demon | Richard Aldington (with John Cournos) | 1916-1928 (see the Gutenberg header) | have | PG 48912 |
| `aldington-letters-of-voltaire-and-frederick` | Voltaire and Frederick the Great | Letters of Voltaire and Frederick the Great | Richard Aldington | 1927 | have-raw | IA `lettersofvoltair0000rich` |
| `aldington-dangerous-acquaintances` | — | Laclos, Dangerous Acquaintances (Les Liaisons dangereuses), tr. Richard Aldington (Routledge, 1924): the only open scan (archive.org dli.ministry.01293) carries no imprint date, so its printing cannot be shown to be before 1931. | — | — | pending | — |

## L. Dora Schmitz (Haeckel's History of Creation, 2 vols)

Shelf: `pipeline/dora-schmitz_shelf.json` · fetch `python3 pipeline/fetch_shelf.py dora-schmitz` · titles `python3 pipeline/split_shelf_titles.py dora-schmitz`.
Round 29 (2026-10-10), vetoable. Schliemann stays on its own shelf. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `dora-schmitz-haeckel-the-history-of-creation-vol-1` | Ernst Haeckel | The History of Creation, Vol. 1 (of 2) | L. Dora Schmitz | 1876 (see the Gutenberg header) | have | PG 40472 |
| `dora-schmitz-haeckel-the-history-of-creation-vol-2` | Ernst Haeckel | The History of Creation, Vol. 2 (of 2) | L. Dora Schmitz | 1876 (see the Gutenberg header) | have | PG 40473 |
| — | — | pg-45190: Schliemann's Troy and Its Remains is on schliemann_shelf.json. | — | — | excluded | — |

## Frances A. Welby (Flammarion; Ostwald's Gorki; Ribot)

Shelf: `pipeline/welby_shelf.json` · fetch `python3 pipeline/fetch_shelf.py welby` · titles `python3 pipeline/split_shelf_titles.py welby`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `welby-flammarion-astronomy-for-amateurs` | Camille Flammarion | Astronomy for Amateurs | Frances A. Welby | 1899-1905 (see the Gutenberg header) | have | PG 25267 |
| `welby-ostwald-maxim-gorki` | Hans Ostwald | Maxim Gorki | Frances A. Welby | 1899-1905 (see the Gutenberg header) | have | PG 22046 |
| `welby-ribot-the-evolution-of-general-ideas` | Th. (Théodule) Ribot | The evolution of general ideas | Frances A. Welby | 1899-1905 (see the Gutenberg header) | have | PG 70911 |

## Mrs. Wilfrid Jackson (Anatole France: The Gods are Athirst, Jerome Coignard, Revolt of the Angels)

Shelf: `pipeline/emilie-jackson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py emilie-jackson` · titles `python3 pipeline/split_shelf_titles.py emilie-jackson`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `emilie-jackson-france-the-gods-are-athirst` | Anatole France | The Gods are Athirst | Mrs. Wilfrid Jackson | 1913-1914 (see the Gutenberg header) | have | PG 24010 |
| `emilie-jackson-france-the-opinions-of-jerome-coignard` | Anatole France | The opinions of Jérôme Coignard | Mrs. Wilfrid Jackson | 1913-1914 (see the Gutenberg header) | have | PG 74713 |
| `emilie-jackson-france-the-revolt-of-the-angels` | Anatole France | The Revolt of the Angels | Mrs. Wilfrid Jackson | 1913-1914 (see the Gutenberg header) | have | PG 32596 |
| `emilie-jackson-mercier-picture-of-paris` | Louis-Sébastien Mercier | The Picture of Paris before and after the Revolution | Wilfrid and Emilie Jackson | 1929 | have-raw | IA `pictureofparisbe0000loui` |

## Cranstoun Metcalfe (Fantomas; two Verne novels)

Shelf: `pipeline/metcalfe_shelf.json` · fetch `python3 pipeline/fetch_shelf.py metcalfe` · titles `python3 pipeline/split_shelf_titles.py metcalfe`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `metcalfe-souvestre-fantomas` | Pierre Souvestre | Fantômas | Cranstoun Metcalfe | 1915-1924 (see the Gutenberg header) | have | PG 27794 |
| `metcalfe-verne-the-castaways-of-the-flag` | Jules Verne | The castaways of the flag | Cranstoun Metcalfe | 1915-1924 (see the Gutenberg header) | have | PG 61600 |
| `metcalfe-verne-their-island-home` | Jules Verne | Their island home | Cranstoun Metcalfe | 1915-1924 (see the Gutenberg header) | have | PG 74418 |

## Mary Wollstonecraft as translator (Young Grandison, 2 vols; Necker)

Shelf: `pipeline/wollstonecraft_shelf.json` · fetch `python3 pipeline/fetch_shelf.py wollstonecraft` · titles `python3 pipeline/split_shelf_titles.py wollstonecraft`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `wollstonecraft-cambon-young-grandison-vol-1` | Madame de Cambon | Young Grandison, volume 1 (of 2) | Mary Wollstonecraft | 1788-1790 (see the Gutenberg header) | have | PG 68481 |
| `wollstonecraft-cambon-young-grandison-vol-2` | Madame de Cambon | Young Grandison, volume 2 (of 2) | Mary Wollstonecraft | 1788-1790 (see the Gutenberg header) | have | PG 69736 |
| `wollstonecraft-necker-of-the-importance-of-religious-opinions` | Jacques Necker | Of the importance of religious opinions | Mary Wollstonecraft | 1788-1790 (see the Gutenberg header) | have | PG 76773 |

## Florence Constable Bicknell (four Fabre books)

Shelf: `pipeline/bicknell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bicknell` · titles `python3 pipeline/split_shelf_titles.py bicknell`.
Round 29 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bicknell-fabre-animal-life-in-field-and-garden` | Jean-Henri Fabre | Animal Life in Field and Garden | Florence Constable Bicknell | 1917-1921 (see the Gutenberg header) | have | PG 66755 |
| `bicknell-fabre-field-forest-and-farm` | Jean-Henri Fabre | Field, Forest and Farm | Florence Constable Bicknell | 1917-1921 (see the Gutenberg header) | have | PG 67813 |
| `bicknell-fabre-our-humble-helpers-familiar-talks-on-the` | Jean-Henri Fabre | Our Humble Helpers: Familiar Talks on the Domestic Animals | Florence Constable Bicknell | 1917-1921 (see the Gutenberg header) | have | PG 67073 |
| `bicknell-fabre-the-story-book-of-science` | Jean-Henri Fabre | The Story-book of Science | Florence Constable Bicknell | 1917-1921 (see the Gutenberg header) | have | PG 56795 |

## Mrs. Chapman Coleman (Luise Mühlbach's historical novels)

Shelf: `pipeline/chapman-coleman_shelf.json` · fetch `python3 pipeline/fetch_shelf.py chapman-coleman` · titles `python3 pipeline/split_shelf_titles.py chapman-coleman`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `chapman-coleman-muhlbach-berlin-and-sans-souci-or-frederick-the-g` | Luise Mühlbach | Berlin and Sans-Souci; Or, Frederick the Great and His Friends | Mrs. Chapman Coleman | 1867-1869 (see the Gutenberg header) | have | PG 4205 |
| `chapman-coleman-muhlbach-frederick-the-great-and-his-family-a-his` | Luise Mühlbach | Frederick the Great and His Family: A Historical Novel | Mrs. Chapman Coleman | 1867-1869 (see the Gutenberg header) | have | PG 3537 |
| `chapman-coleman-muhlbach-goethe-and-schiller-an-historical-romanc` | Luise Mühlbach | Goethe and Schiller: An Historical Romance | Mrs. Chapman Coleman | 1867-1869 (see the Gutenberg header) | have | PG 46883 |
| `chapman-coleman-muhlbach-mohammed-ali-and-his-house` | Luise Mühlbach | Mohammed Ali and His House | Mrs. Chapman Coleman | 1867-1869 (see the Gutenberg header) | have | PG 3320 |
| `chapman-coleman-muhlbach-queen-hortense-a-life-picture-of-the-nap` | Luise Mühlbach | Queen Hortense: A Life Picture of the Napoleonic Era | Mrs. Chapman Coleman | 1867-1869 (see the Gutenberg header) | have | PG 12019 |

## Count de Soissons (Sienkiewicz, Orzeszkowa, Kraszewski)

Shelf: `pipeline/soissons_shelf.json` · fetch `python3 pipeline/fetch_shelf.py soissons` · titles `python3 pipeline/split_shelf_titles.py soissons`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `soissons-kraszewski-count-bruhl` | Józef Ignacy Kraszewski | Count Brühl | Count S. C. de Soissons | 1898-1901 (see the Gutenberg header) | have | PG 37624 |
| `soissons-kraszewski-the-countess-cosel-a-romance-of-history` | Józef Ignacy Kraszewski | The Countess Cosel: A Romance of History of the Times of Augustus the Strong | Count S. C. de Soissons | 1898-1901 (see the Gutenberg header) | have | PG 37623 |
| `soissons-orzeszkowa-an-obscure-apostle-a-dramatic-story` | Eliza Orzeszkowa | An Obscure Apostle: A Dramatic Story | Count S. C. de Soissons | 1898-1901 (see the Gutenberg header) | have | PG 28400 |
| `soissons-sienkiewicz-so-runs-the-world` | Henryk Sienkiewicz | So Runs the World | Count S. C. de Soissons | 1898-1901 (see the Gutenberg header) | have | PG 10546 |

## Thomas J. McCormack (Mach's Popular Scientific Lectures; Weismann)

Shelf: `pipeline/mccormack_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mccormack` · titles `python3 pipeline/split_shelf_titles.py mccormack`.
Round 30 (2026-10-10), vetoable. His Lagrange and Schubert are pending (PDF only on Gutenberg). Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mccormack-mach-popular-scientific-lectures` | Ernst Mach | Popular scientific lectures | Thomas J. McCormack | 1895-1898 (see the Gutenberg header) | have | PG 39508 |
| `mccormack-weismann-on-germinal-selection-as-a-source-of-def` | August Weismann | On Germinal Selection as a Source of Definite Variation | Thomas J. McCormack | 1895-1898 (see the Gutenberg header) | have | PG 34077 |
| `pg-25387` | — | Mathematical Essays and Recreations: Gutenberg publishes this mathematics book only as PDF/LaTeX, with no plain-text file to fetch. Left for a later pass that finds a period scan on the Internet Archive. | — | — | pending | — |
| `pg-36640` | — | Lectures on Elementary Mathematics: Gutenberg publishes this mathematics book only as PDF/LaTeX, with no plain-text file to fetch. Left for a later pass that finds a period scan on the Internet Archive. | — | — | pending | — |

## Mrs. Georgina Malcolm (Freytag's Pictures of German Life, 4 vols)

Shelf: `pipeline/georgina-malcolm_shelf.json` · fetch `python3 pipeline/fetch_shelf.py georgina-malcolm` · titles `python3 pipeline/split_shelf_titles.py georgina-malcolm`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `georgina-malcolm-freytag-pictures-of-german-life-15th-17th-vol-1` | Gustav Freytag | Pictures of German Life in the XVth, XVIth, and XVIIth Centuries, Vol. I. | Mrs. Georgina Malcolm | 1862-1863 (see the Gutenberg header) | have | PG 33794 |
| `georgina-malcolm-freytag-pictures-of-german-life-15th-17th-vol-2` | Gustav Freytag | Pictures of German Life in the XVth, XVIth, and XVIIth Centuries, Vol. II. | Mrs. Georgina Malcolm | 1862-1863 (see the Gutenberg header) | have | PG 33795 |
| `georgina-malcolm-freytag-pictures-of-german-life-18th-19th-vol-1` | Gustav Freytag | Pictures of German Life in the XVIIIth and XIXth Centuries, Vol. I. | Mrs. Georgina Malcolm | 1862-1863 (see the Gutenberg header) | have | PG 33818 |
| `georgina-malcolm-freytag-pictures-of-german-life-18th-19th-vol-2` | Gustav Freytag | Pictures of German Life in the XVIIIth and XIXth Centuries, Vol. II. | Mrs. Georgina Malcolm | 1862-1863 (see the Gutenberg header) | have | PG 33819 |

## Denis Florence MacCarthy (four Calderón dramas)

Shelf: `pipeline/denis-maccarthy_shelf.json` · fetch `python3 pipeline/fetch_shelf.py denis-maccarthy` · titles `python3 pipeline/split_shelf_titles.py denis-maccarthy`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `denis-maccarthy-calderon-life-is-a-dream` | Pedro Calderón de la Barca | Life Is a Dream | Denis Florence MacCarthy | 1853-1873 (see the Gutenberg header) | have | PG 6363 |
| `denis-maccarthy-calderon-the-purgatory-of-st-patrick` | Pedro Calderón de la Barca | The Purgatory of St. Patrick | Denis Florence MacCarthy | 1853-1873 (see the Gutenberg header) | have | PG 6371 |
| `denis-maccarthy-calderon-the-two-lovers-of-heaven-chrysanthus-and` | Pedro Calderón de la Barca | The Two Lovers of Heaven: Chrysanthus and Daria A Drama of Early Christian Rome | Denis Florence MacCarthy | 1853-1873 (see the Gutenberg header) | have | PG 12173 |
| `denis-maccarthy-calderon-the-wonder-working-magician` | Pedro Calderón de la Barca | The Wonder-Working Magician | Denis Florence MacCarthy | 1853-1873 (see the Gutenberg header) | have | PG 6372 |

## Hannibal Evans Lloyd (Prince Maximilian of Wied's Travels, 3 parts; Iffland)

Shelf: `pipeline/hannibal-lloyd_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hannibal-lloyd` · titles `python3 pipeline/split_shelf_titles.py hannibal-lloyd`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hannibal-lloyd-iffland-the-nephews-a-play-in-five-acts` | August Wilhelm Iffland | The Nephews: A Play, in Five Acts. | Hannibal Evans Lloyd | 1799-1843 (see the Gutenberg header) | have | PG 31667 |
| `hannibal-lloyd-wied-travels-in-the-interior-of-north-america-part-1` | Maximilian Wied | Maximilian, Prince of Wied's, Travels in the Interior of North America, 1832-1834, part 1 | Hannibal Evans Lloyd | 1799-1843 (see the Gutenberg header) | have | PG 38784 |
| `hannibal-lloyd-wied-travels-in-the-interior-of-north-america-part-2` | Maximilian Wied | Maximilian, Prince of Wied's, Travels in the Interior of North America, 1832-1834, part 2 | Hannibal Evans Lloyd | 1799-1843 (see the Gutenberg header) | have | PG 47392 |
| `hannibal-lloyd-wied-travels-in-the-interior-of-north-america-part-3` | Maximilian Wied | Maximilian, Prince of Wied's, Travels in the Interior of North America, 1832-1834, part 3 and appendix | Hannibal Evans Lloyd | 1799-1843 (see the Gutenberg header) | have | PG 48235 |

## John Cournos (Sologub's The Created Legend; The Old House)

Shelf: `pipeline/cournos_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cournos` · titles `python3 pipeline/split_shelf_titles.py cournos`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cournos-sologub-the-created-legend` | Fyodor Sologub | The Created Legend | John Cournos | 1915-1916 (see the Gutenberg header) | have | PG 7480 |
| `cournos-sologub-the-old-house-and-other-tales` | Fyodor Sologub | The Old House, and Other Tales | John Cournos | 1915-1916 (see the Gutenberg header) | have | PG 48452 |
| — | — | pg-48912: The Little Demon is on aldington_shelf.json (lane C). | — | — | excluded | — |
| — | — | pg-68357: Short-Story Masterpieces vol. 4 is an anthology edited by Esenwein; Cournos is one of several translators. | — | — | excluded | — |
| — | — | pg-74071: Short-Story Masterpieces vol. 3: same reason. | — | — | excluded | — |

## Lily Wolffsohn (Dahn's A Struggle for Rome, 3 vols)

Shelf: `pipeline/lily-wolffsohn_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lily-wolffsohn` · titles `python3 pipeline/split_shelf_titles.py lily-wolffsohn`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lily-wolffsohn-dahn-a-struggle-for-rome-v-1` | Felix Dahn | A Struggle for Rome, v. 1 | Lily Wolffsohn | 1878 (see the Gutenberg header) | have | PG 32271 |
| `lily-wolffsohn-dahn-a-struggle-for-rome-v-2` | Felix Dahn | A Struggle for Rome, v. 2 | Lily Wolffsohn | 1878 (see the Gutenberg header) | have | PG 32330 |
| `lily-wolffsohn-dahn-a-struggle-for-rome-v-3` | Felix Dahn | A Struggle for Rome, v. 3 | Lily Wolffsohn | 1878 (see the Gutenberg header) | have | PG 32377 |

## David Shea and Anthony Troyer (The Dabistán, 3 vols)

Shelf: `pipeline/shea-troyer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py shea-troyer` · titles `python3 pipeline/split_shelf_titles.py shea-troyer`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `shea-troyer-the-dabistan-vol-1` | Attributed to Muhsin Fani (authorship disputed) | The Dabistán, or School of manners, Volume 1 (of 3) translated from the original Persian, with notes and illustrations | David Shea and Anthony Troyer | 1843 (see the Gutenberg header) | have | PG 63275 |
| `shea-troyer-the-dabistan-vol-2` | Attributed to Muhsin Fani (authorship disputed) | The Dabistán, or School of manners, Volume 2 (of 3) translated from the original Persian, with notes and illustrations | David Shea and Anthony Troyer | 1843 (see the Gutenberg header) | have | PG 63276 |
| `shea-troyer-the-dabistan-vol-3` | Attributed to Muhsin Fani (authorship disputed) | The Dabistán, or School of manners, Volume 3 (of 3) translated from the original Persian, with notes and illustrations | David Shea and Anthony Troyer | 1843 (see the Gutenberg header) | have | PG 63277 |

## Pauline D. Townsend (Jahn's Life of Mozart, 3 vols)

Shelf: `pipeline/pauline-townsend_shelf.json` · fetch `python3 pipeline/fetch_shelf.py pauline-townsend` · titles `python3 pipeline/split_shelf_titles.py pauline-townsend`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `pauline-townsend-jahn-life-of-mozart-vol-1-of-3` | Otto Jahn | Life of Mozart, Vol. 1 (of 3) | Pauline D. Townsend | 1882 (see the Gutenberg header) | have | PG 43411 |
| `pauline-townsend-jahn-life-of-mozart-vol-2-of-3` | Otto Jahn | Life of Mozart, Vol. 2 (of 3) | Pauline D. Townsend | 1882 (see the Gutenberg header) | have | PG 43412 |
| `pauline-townsend-jahn-life-of-mozart-vol-3-of-3` | Otto Jahn | Life of Mozart, Vol. 3 (of 3) | Pauline D. Townsend | 1882 (see the Gutenberg header) | have | PG 43413 |

## J. Arthur and Margaret R. Thomson (Weismann's Evolution Theory; Otto; Brehm)

Shelf: `pipeline/thomson-weismann_shelf.json` · fetch `python3 pipeline/fetch_shelf.py thomson-weismann` · titles `python3 pipeline/split_shelf_titles.py thomson-weismann`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `thomson-weismann-brehm-from-north-pole-to-equator-studies-of-wi` | Alfred Edmund Brehm | From North Pole to Equator: Studies of Wild Life and Scenes in Many Lands | Margaret R. Thomson | 1896-1907 (see the Gutenberg header) | have | PG 68142 |
| `thomson-weismann-otto-naturalism-and-religion` | Rudolf Otto | Naturalism and Religion | J. Arthur Thomson and Margaret R. Thomson | 1896-1907 (see the Gutenberg header) | have | PG 31794 |
| `thomson-weismann-weismann-the-evolution-theory-vol-1-of-2` | August Weismann | The Evolution Theory, Vol. 1 of 2 | J. Arthur Thomson and Margaret R. Thomson | 1896-1907 (see the Gutenberg header) | have | PG 64227 |
| `thomson-weismann-weismann-the-evolution-theory-vol-2-of-2` | August Weismann | The Evolution Theory, Vol. 2 of 2 | J. Arthur Thomson and Margaret R. Thomson | 1896-1907 (see the Gutenberg header) | have | PG 65049 |

## S. E. A. H. Stephenson (Spielhagen's The Breaking of the Storm, 3 vols)

Shelf: `pipeline/ssa-stephenson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ssa-stephenson` · titles `python3 pipeline/split_shelf_titles.py ssa-stephenson`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ssa-stephenson-spielhagen-the-breaking-of-the-storm-vol-i` | Friedrich Spielhagen | The Breaking of the Storm, Vol. I. | S. E. A. H. Stephenson | 1877 (see the Gutenberg header) | have | PG 34657 |
| `ssa-stephenson-spielhagen-the-breaking-of-the-storm-vol-ii` | Friedrich Spielhagen | The Breaking of the Storm, Vol. II. | S. E. A. H. Stephenson | 1877 (see the Gutenberg header) | have | PG 34658 |
| `ssa-stephenson-spielhagen-the-breaking-of-the-storm-vol-iii` | Friedrich Spielhagen | The Breaking of the Storm, Vol. III. | S. E. A. H. Stephenson | 1877 (see the Gutenberg header) | have | PG 34659 |

## William Robson (Michaud's History of the Crusades, 3 vols)

Shelf: `pipeline/robson-michaud_shelf.json` · fetch `python3 pipeline/fetch_shelf.py robson-michaud` · titles `python3 pipeline/split_shelf_titles.py robson-michaud`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `robson-michaud-michaud-the-history-of-the-crusades-vol-1-of-3` | J. Fr. (Joseph Fr.) Michaud | The History of the Crusades (vol. 1 of 3) | William Robson | 1852 (see the Gutenberg header) | have | PG 49104 |
| `robson-michaud-michaud-the-history-of-the-crusades-vol-2-of-3` | J. Fr. (Joseph Fr.) Michaud | The History of the Crusades (vol. 2 of 3) | William Robson | 1852 (see the Gutenberg header) | have | PG 49118 |
| `robson-michaud-michaud-the-history-of-the-crusades-vol-3-of-3` | J. Fr. (Joseph Fr.) Michaud | The History of the Crusades (vol. 3 of 3) | William Robson | 1852 (see the Gutenberg header) | have | PG 49167 |

## William Painter (The Palace of Pleasure, 3 vols)

Shelf: `pipeline/painter_shelf.json` · fetch `python3 pipeline/fetch_shelf.py painter` · titles `python3 pipeline/split_shelf_titles.py painter`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `painter-the-palace-of-pleasure-vol-1` | Various (Italian, French and classical novelle: Boccaccio, Bandello, Livy and others) | The Palace of Pleasure, Volume 1 | William Painter | 1566-1567 (Jacobs's edition, 1890) | have | PG 20241 |
| `painter-the-palace-of-pleasure-vol-2` | Various (Italian, French and classical novelle: Boccaccio, Bandello, Livy and others) | The Palace of Pleasure, Volume 2 | William Painter | 1566-1567 (Jacobs's edition, 1890) | have | PG 34053 |
| `painter-the-palace-of-pleasure-vol-3` | Various (Italian, French and classical novelle: Boccaccio, Bandello, Livy and others) | The Palace of Pleasure, Volume 3 | William Painter | 1566-1567 (Jacobs's edition, 1890) | have | PG 34840 |

## C. T. Campion (Schweitzer: Primeval Forest; Philosophy of Civilization)

Shelf: `pipeline/campion_shelf.json` · fetch `python3 pipeline/fetch_shelf.py campion` · titles `python3 pipeline/split_shelf_titles.py campion`.
Round 30 (2026-10-10), vetoable. On the Edge of the Primeval Forest is keyed from a 1937 reprint: flagged. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `campion-schweitzer-civilization-and-ethics` | Albert Schweitzer | Civilization and ethics | C. T. Campion | 1922-1923 (see the Gutenberg header) | have | PG 76061 |
| `campion-schweitzer-on-the-edge-of-the-primeval-forest` | Albert Schweitzer | On the edge of the primeval forest | C. T. Campion | 1922-1923 (see the Gutenberg header) | have | PG 50015 |
| `campion-schweitzer-the-decay-and-the-restoration-of-civiliz` | Albert Schweitzer | The decay and the restoration of civilization | C. T. Campion | 1922-1923 (see the Gutenberg header) | have | PG 75958 |

## Israel Friedlaender (Dubnow's History of the Jews in Russia and Poland, 3 vols)

Shelf: `pipeline/friedlaender_shelf.json` · fetch `python3 pipeline/fetch_shelf.py friedlaender` · titles `python3 pipeline/split_shelf_titles.py friedlaender`.
Round 30 (2026-10-10), vetoable. Volume 2 is keyed from a 1946 reprint: flagged. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `friedlaender-dubnow-history-of-the-jews-in-russia-and-poland-vol-1` | Simon Dubnow | History of the Jews in Russia and Poland, Volume 1 [of 3] From the Beginning until the Death of Alexander I (1825) | Israel Friedlaender | 1916-1920 (see the Gutenberg header) | have | PG 41547 |
| `friedlaender-dubnow-history-of-the-jews-in-russia-and-poland-vol-2` | Simon Dubnow | History of the Jews in Russia and Poland, Volume 2 [of 3] From the Death of Alexander I until the Death of Alexander III (1825-1894) | Israel Friedlaender | 1916-1920 (see the Gutenberg header) | have | PG 15729 |
| `friedlaender-dubnow-history-of-the-jews-in-russia-and-poland-vol-3` | Simon Dubnow | History of the Jews in Russia and Poland, Volume 3 [of 3] From the Accession of Nicholas II until the Present Day | Israel Friedlaender | 1916-1920 (see the Gutenberg header) | have | PG 47212 |

## Aline Delano (Tolstoy's Kingdom of God; Hugo's Ninety-Three; Korolenko)

Shelf: `pipeline/aline-delano_shelf.json` · fetch `python3 pipeline/fetch_shelf.py aline-delano` · titles `python3 pipeline/split_shelf_titles.py aline-delano`.
Round 30 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `aline-delano-hugo-ninety-three` | Victor Hugo | Ninety-Three | Aline Delano | 1888-1899 (see the Gutenberg header) | have | PG 49372 |
| `aline-delano-korolenko-the-blind-musician` | Vladimir Galaktionovich Korolenko | The Blind Musician | Aline Delano | 1888-1899 (see the Gutenberg header) | have | PG 59497 |
| `aline-delano-tolstoy-the-kingdom-of-god-is-within-you-what-is` | Leo Tolstoy | The Kingdom of God is Within You; What is Art? | Aline Delano | 1888-1899 (see the Gutenberg header) | have | PG 43409 |

## Gregory Zilboorg (Zamyatin's We, 1924; Andreyev's He Who Gets Slapped)

Shelf: `pipeline/zilboorg_shelf.json` · fetch `python3 pipeline/fetch_shelf.py zilboorg` · titles `python3 pipeline/split_shelf_titles.py zilboorg`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `zilboorg-andreyev-he-who-gets-slapped-a-play-in-four-acts` | Leonid Andreyev | He Who Gets Slapped: A Play in Four Acts | Gregory Zilboorg | 1921-1924 (see the Gutenberg header) | have | PG 37961 |
| `zilboorg-zamiatin-we` | Evgenii Ivanovich Zamiatin | We | Gregory Zilboorg | 1921-1924 (see the Gutenberg header) | have | PG 61963 |

## Avrahm Yarmolinsky (Saltykov's A Family of Noblemen; The Shield)

Shelf: `pipeline/yarmolinsky_shelf.json` · fetch `python3 pipeline/fetch_shelf.py yarmolinsky` · titles `python3 pipeline/split_shelf_titles.py yarmolinsky`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `yarmolinsky-gorky-the-shield` | Maksim Gorky | The shield | Avrahm Yarmolinsky | 1917 (see the Gutenberg header) | have | PG 19453 |
| `yarmolinsky-saltykov-a-family-of-noblemen` | Mikhail Evgrafovich Saltykov | A family of noblemen | Avrahm Yarmolinsky | 1917 (see the Gutenberg header) | have | PG 44237 |

## Katharine Wylde (Deledda's Ashes and Nostalgia)

Shelf: `pipeline/katharine-wylde_shelf.json` · fetch `python3 pipeline/fetch_shelf.py katharine-wylde` · titles `python3 pipeline/split_shelf_titles.py katharine-wylde`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `katharine-wylde-deledda-ashes-cenere-a-sardinian-story` | Grazia Deledda | Ashes (Cenere): A Sardinian Story | Katharine Wylde | 1905-1908 (see the Gutenberg header) | have | PG 63962 |
| `katharine-wylde-deledda-nostalgia` | Grazia Deledda | Nostalgia | Katharine Wylde | 1905-1908 (see the Gutenberg header) | have | PG 53905 |

## Winifred Stephens (Anatole France's Life of Joan of Arc; Clio)

Shelf: `pipeline/winifred-stephens_shelf.json` · fetch `python3 pipeline/fetch_shelf.py winifred-stephens` · titles `python3 pipeline/split_shelf_titles.py winifred-stephens`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `winifred-stephens-france-clio` | Anatole France | Clio | Winifred Stephens | 1909-1922 (see the Gutenberg header) | have | PG 50670 |
| `winifred-stephens-france-the-life-of-joan-of-arc-vol-1-and-2` | Anatole France | The Life of Joan of Arc, Vol. 1 and 2 | Winifred Stephens | 1909-1922 (see the Gutenberg header) | have | PG 19488 |

## Paul Selver (Čapek's R.U.R. and The Insect Play)

Shelf: `pipeline/selver_shelf.json` · fetch `python3 pipeline/fetch_shelf.py selver` · titles `python3 pipeline/split_shelf_titles.py selver`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `selver-capek-and-so-ad-infinitum-the-life-of-the-inse` | Karel Čapek | 'And So Ad Infinitum' (The Life of the Insects) An Entomological Review, in Three Acts, a Prologue and an Epilogue | Paul Selver | 1923 (see the Gutenberg header) | have | PG 61420 |
| `selver-capek-r-u-r-rossum-s-universal-robots-a-fantas` | Karel Čapek | R.U.R. (Rossum's Universal Robots) A Fantastic Melodrama in Three Acts and an Epilogue | Paul Selver (with Nigel Playfair) | 1923 (see the Gutenberg header) | have | PG 59112 |

## J. M. Rigg (Boccaccio's Decameron, 2 vols)

Shelf: `pipeline/rigg_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rigg` · titles `python3 pipeline/split_shelf_titles.py rigg`.
Round 31 (2026-10-10), vetoable. A separate translation from Payne's. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rigg-boccaccio-the-decameron-vol-1` | Giovanni Boccaccio | The Decameron, Volume I | J. M. Rigg | 1903 (see the Gutenberg header) | have | PG 3726 |
| `rigg-boccaccio-the-decameron-vol-2` | Giovanni Boccaccio | The Decameron, Volume II | J. M. Rigg | 1903 (see the Gutenberg header) | have | PG 13102 |

## Arthur Hornblow (D'Annunzio's The Intruder; The Triumph of Death)

Shelf: `pipeline/hornblow_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hornblow` · titles `python3 pipeline/split_shelf_titles.py hornblow`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hornblow-d-annunzio-the-intruder` | Gabriele D'Annunzio | The Intruder | Arthur Hornblow | 1896-1898 (see the Gutenberg header) | have | PG 54236 |
| `hornblow-d-annunzio-the-triumph-of-death` | Gabriele D'Annunzio | The Triumph of Death | Arthur Hornblow | 1896-1898 (see the Gutenberg header) | have | PG 54272 |

## Hanna Astrup Larsen (Jacobsen's Marie Grubbe; Niels Lyhne)

Shelf: `pipeline/hanna-larsen_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hanna-larsen` · titles `python3 pipeline/split_shelf_titles.py hanna-larsen`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hanna-larsen-jacobsen-marie-grubbe-a-lady-of-the-seventeenth-c` | J. P. (Jens Peter) Jacobsen | Marie Grubbe, a Lady of the Seventeenth Century | Hanna Astrup Larsen | 1917-1919 (see the Gutenberg header) | have | PG 54845 |
| `hanna-larsen-jacobsen-niels-lyhne` | J. P. (Jens Peter) Jacobsen | Niels Lyhne | Hanna Astrup Larsen | 1917-1919 (see the Gutenberg header) | have | PG 55389 |

## J. E. Crawford Flitch (Unamuno's Tragic Sense of Life; Essays and Soliloquies)

Shelf: `pipeline/flitch_shelf.json` · fetch `python3 pipeline/fetch_shelf.py flitch` · titles `python3 pipeline/split_shelf_titles.py flitch`.
Round 31 (2026-10-10), vetoable. Tragic Sense is keyed from a 1954 Dover reprint: flagged. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `flitch-unamuno-essays-and-soliloquies` | Miguel de Unamuno | Essays and soliloquies | J. E. Crawford Flitch | 1921-1925 (see the Gutenberg header) | have | PG 71260 |
| `flitch-unamuno-tragic-sense-of-life` | Miguel de Unamuno | Tragic Sense Of Life | J. E. Crawford Flitch | 1921-1925 (see the Gutenberg header) | have | PG 14636 |

## Benjamin F. Glazer (Molnár's Liliom; Fashions for Men and The Swan)

Shelf: `pipeline/glazer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py glazer` · titles `python3 pipeline/split_shelf_titles.py glazer`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `glazer-molnar-fashions-for-men-and-the-swan` | Ferenc Molnár | Fashions for men, and The swan | Benjamin F. Glazer | 1921-1922 (see the Gutenberg header) | have | PG 75610 |
| `glazer-molnar-liliom` | Ferenc Molnár | Liliom | Benjamin F. Glazer | 1921-1922 (see the Gutenberg header) | have | PG 48749 |

## F. E. Bunnett (Fouqué's Undine; Memoirs of Leonora Christina)

Shelf: `pipeline/bunnett_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bunnett` · titles `python3 pipeline/split_shelf_titles.py bunnett`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bunnett-motte-fouque-undine` | Friedrich Heinrich Karl La Motte-Fouqué | Undine | F. E. Bunnett | 1872 and earlier (see the Gutenberg header) | have | PG 3714 |
| `bunnett-ulfeldt-memoirs-of-leonora-christina-daughter-of` | Leonora Christina Ulfeldt | Memoirs of Leonora Christina, Daughter of Christian IV. of Denmark Written During Her Imprisonment in the Blue Tower at Copenhagen 1663-1685 | F. E. Bunnett | 1872 and earlier (see the Gutenberg header) | have | PG 38128 |

## Constance Bache (Letters of Franz Liszt, 2 vols)

Shelf: `pipeline/constance-bache_shelf.json` · fetch `python3 pipeline/fetch_shelf.py constance-bache` · titles `python3 pipeline/split_shelf_titles.py constance-bache`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `constance-bache-liszt-letters-of-franz-liszt-vol-1` | Franz Liszt | Letters of Franz Liszt -- Volume 1 from Paris to Rome: Years of Travel as a Virtuoso | Constance Bache | 1894 (see the Gutenberg header) | have | PG 3689 |
| `constance-bache-liszt-letters-of-franz-liszt-vol-2` | Franz Liszt | Letters of Franz Liszt -- Volume 2 from Rome to the End | Constance Bache | 1894 (see the Gutenberg header) | have | PG 3750 |

## Francis Hueffer (Correspondence of Wagner and Liszt, 2 vols)

Shelf: `pipeline/hueffer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hueffer` · titles `python3 pipeline/split_shelf_titles.py hueffer`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hueffer-correspondence-of-wagner-and-liszt-vol-1` | Richard Wagner | Correspondence of Wagner and Liszt — Volume 1 | Francis Hueffer | 1888 (see the Gutenberg header) | have | PG 3835 |
| `hueffer-correspondence-of-wagner-and-liszt-vol-2` | Richard Wagner | Correspondence of Wagner and Liszt — Volume 2 | Francis Hueffer | 1888 (see the Gutenberg header) | have | PG 4234 |

## F. M. Atkinson and J. H. Lepper (De Coster's Legend of Ulenspiegel, 2 vols)

Shelf: `pipeline/atkinson-lepper_shelf.json` · fetch `python3 pipeline/fetch_shelf.py atkinson-lepper` · titles `python3 pipeline/split_shelf_titles.py atkinson-lepper`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `atkinson-lepper-de-coster-the-legend-of-ulenspiegel-vol-1` | Charles De Coster | The Legend of Ulenspiegel, Volume 1 (of 2) And Lamme Goedzak, and their Adventures Heroical, Joyous and Glorious in the Land of Flanders and Elsewhere | F. M. Atkinson and John Heron Lepper | 1918 (see the Gutenberg header) | have | PG 38247 |
| `atkinson-lepper-de-coster-the-legend-of-ulenspiegel-vol-2` | Charles De Coster | The Legend of Ulenspiegel, Volume 2 (of 2) And Lamme Goedzak, and their Adventures Heroical, Joyous and Glorious in the Land of Flanders and Elsewhere | F. M. Atkinson and John Heron Lepper | 1918 (see the Gutenberg header) | have | PG 40004 |

## Charles Francis Atkinson (Spengler's The Decline of the West, 2 vols)

Shelf: `pipeline/cf-atkinson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cf-atkinson` · titles `python3 pipeline/split_shelf_titles.py cf-atkinson`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cf-atkinson-spengler-the-decline-of-the-west-vol-1` | Oswald Spengler | The decline of the West, Volume 1 | Charles Francis Atkinson | 1926-1928 (see the Gutenberg header) | have | PG 72344 |
| `cf-atkinson-spengler-the-decline-of-the-west-vol-2` | Oswald Spengler | The decline of the West, Volume 2 | Charles Francis Atkinson | 1926-1928 (see the Gutenberg header) | have | PG 78914 |

## H. Bencraft Joly (Dream of the Red Chamber, 2 books)

Shelf: `pipeline/joly_shelf.json` · fetch `python3 pipeline/fetch_shelf.py joly` · titles `python3 pipeline/split_shelf_titles.py joly`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `joly-cao-hung-lou-meng-dream-of-the-red-chamber-vol-1` | Xueqin Cao | Hung Lou Meng, or, the Dream of the Red Chamber, a Chinese Novel, Book I | H. Bencraft Joly | 1892-1893 (see the Gutenberg header) | have | PG 9603 |
| `joly-cao-hung-lou-meng-dream-of-the-red-chamber-vol-2` | Xueqin Cao | Hung Lou Meng, or, the Dream of the Red Chamber, a Chinese Novel, Book II | H. Bencraft Joly | 1892-1893 (see the Gutenberg header) | have | PG 9604 |

## Steven T. Byington (Stirner's The Ego and His Own; Eltzbacher's Anarchism)

Shelf: `pipeline/byington_shelf.json` · fetch `python3 pipeline/fetch_shelf.py byington` · titles `python3 pipeline/split_shelf_titles.py byington`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `byington-eltzbacher-anarchism` | Paul Eltzbacher | Anarchism | Steven T. Byington | 1907-1908 (see the Gutenberg header) | have | PG 36690 |
| `byington-stirner-the-ego-and-his-own` | Max Stirner | The Ego and His Own | Steven T. Byington | 1907-1908 (see the Gutenberg header) | have | PG 34580 |

## J. T. Bealby (Hoffmann's Weird Tales, 2 vols)

Shelf: `pipeline/bealby_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bealby` · titles `python3 pipeline/split_shelf_titles.py bealby`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bealby-hoffmann-weird-tales-vol-1-of-2` | E. T. A. (Ernst Theodor Amadeus) Hoffmann | Weird Tales. Vol. 1 (of 2) | J. T. Bealby | 1885 (see the Gutenberg header) | have | PG 31377 |
| `bealby-hoffmann-weird-tales-vol-2-of-2` | E. T. A. (Ernst Theodor Amadeus) Hoffmann | Weird Tales, Vol. 2 (of 2) | J. T. Bealby | 1885 (see the Gutenberg header) | have | PG 31439 |

## William Hazlitt the younger (Huc's Travels in Tartary, Thibet, and China, 2 vols)

Shelf: `pipeline/hazlitt-huc_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hazlitt-huc` · titles `python3 pipeline/split_shelf_titles.py hazlitt-huc`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hazlitt-huc-travels-in-tartary-thibet-and-china-vol-1` | Evariste Régis Huc | Travels in Tartary, Thibet, and China during the years 1844-5-6. Volume 1 | William Hazlitt (the younger) | 1852 (see the Gutenberg header) | have | PG 32747 |
| `hazlitt-huc-travels-in-tartary-thibet-and-china-vol-2` | Evariste Régis Huc | Travels in Tartary, Thibet, and China During the years 1844-5-6. Volume 2 | William Hazlitt (the younger) | 1852 (see the Gutenberg header) | have | PG 33269 |

## John Ingram Lockhart (Memoirs of Bernal Díaz del Castillo, 2 vols)

Shelf: `pipeline/lockhart-diaz_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lockhart-diaz` · titles `python3 pipeline/split_shelf_titles.py lockhart-diaz`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lockhart-diaz-memoirs-of-bernal-diaz-del-castillo-vol-1` | Bernal Díaz del Castillo | The Memoirs of the Conquistador Bernal Diaz del Castillo, Vol 1 (of 2) Written by Himself Containing a True and Full Account of the Discovery and Conquest of Mexico and New Spain. | John Ingram Lockhart | 1844 (see the Gutenberg header) | have | PG 32474 |
| `lockhart-diaz-memoirs-of-bernal-diaz-del-castillo-vol-2` | Bernal Díaz del Castillo | The Memoirs of the Conquistador Bernal Diaz del Castillo, Vol 2 (of 2) Written by Himself Containing a True and Full Account of the Discovery and Conquest of Mexico and New Spain. | John Ingram Lockhart | 1844 (see the Gutenberg header) | have | PG 32475 |

## Florence Crewe-Jones (Malot's Nobody's Boy; Nobody's Girl)

Shelf: `pipeline/crewe-jones_shelf.json` · fetch `python3 pipeline/fetch_shelf.py crewe-jones` · titles `python3 pipeline/split_shelf_titles.py crewe-jones`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `crewe-jones-malot-nobody-s-boy-sans-famille` | Hector Malot | Nobody's boy (Sans famille) | Florence Crewe-Jones | 1916-1922 (see the Gutenberg header) | have | PG 25102 |
| `crewe-jones-malot-nobody-s-girl-en-famille` | Hector Malot | Nobody's Girl (En Famille) | Florence Crewe-Jones | 1916-1922 (see the Gutenberg header) | have | PG 27690 |

## W. J. Greenstreet (Dastre's Life and Death)

Shelf: `pipeline/greenstreet_shelf.json` · fetch `python3 pipeline/fetch_shelf.py greenstreet` · titles `python3 pipeline/split_shelf_titles.py greenstreet`.
Round 31 (2026-10-10), vetoable. His Poincaré is pending (PDF only on Gutenberg). Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `greenstreet-dastre-life-and-death` | A. (Albert) Dastre | Life and death | W. J. Greenstreet | 1905-1911 (see the Gutenberg header) | have | PG 65699 |
| `pg-37157` | — | Poincaré's Science and Hypothesis: Gutenberg publishes it only as PDF/LaTeX, with no plain-text file to fetch. Left for a later pass that finds a period scan. | — | — | pending | — |

## Patrick James Stirling (Bastiat's Economic Sophisms; Harmonies)

Shelf: `pipeline/stirling-bastiat_shelf.json` · fetch `python3 pipeline/fetch_shelf.py stirling-bastiat` · titles `python3 pipeline/split_shelf_titles.py stirling-bastiat`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `stirling-bastiat-bastiat-economic-sophisms` | Frédéric Bastiat | Economic Sophisms | Patrick James Stirling | 1860-1873 (see the Gutenberg header) | have | PG 44145 |
| `stirling-bastiat-bastiat-harmonies-of-political-economy-translate` | Frédéric Bastiat | Harmonies of Political Economy Translated from the Third French Edition, with a Notice of the Life and Writings of the Author | Patrick James Stirling | 1860-1873 (see the Gutenberg header) | have | PG 45002 |

## Sofie Delffs (Scheffel's Ekkehard, 2 vols)

Shelf: `pipeline/delffs_shelf.json` · fetch `python3 pipeline/fetch_shelf.py delffs` · titles `python3 pipeline/split_shelf_titles.py delffs`.
Round 31 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `delffs-scheffel-ekkehard-a-tale-of-the-tenth-century-vol-1` | Joseph Victor von Scheffel | Ekkehard: A Tale of the Tenth Century. Vol. 1 (of 2) | Sofie Delffs | 1872 (see the Gutenberg header) | have | PG 35846 |
| `delffs-scheffel-ekkehard-a-tale-of-the-tenth-century-vol-2` | Joseph Victor von Scheffel | Ekkehard: A Tale of the Tenth Century. Vol. 2 (of 2) | Sofie Delffs | 1872 (see the Gutenberg header) | have | PG 35847 |

## George Egerton (Hamsun's Hunger)

Shelf: `pipeline/egerton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py egerton` · titles `python3 pipeline/split_shelf_titles.py egerton`.
Round 31 (2026-10-10), vetoable. Knopf's bowdlerised 1920 text; duplicate copy left out. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `egerton-hamsun-hunger` | Knut Hamsun | Hunger | George Egerton | 1899 (see the Gutenberg header) | have | PG 76692 |
| — | — | pg-8387: Hunger again: the same Knopf text from its 1921 eighth printing; this shelf keeps the 1920 first printing (76692). | — | — | excluded | — |

## Elise L. Lathrop (three Ossip Schubin novels)

Shelf: `pipeline/elise-lathrop_shelf.json` · fetch `python3 pipeline/fetch_shelf.py elise-lathrop` · titles `python3 pipeline/split_shelf_titles.py elise-lathrop`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `elise-lathrop-schubin-asbein-from-the-life-of-a-virtuoso` | Ossip Schubin | Asbeïn: From the Life of a Virtuoso | Elise L. Lathrop | 1890-1891 (see the Gutenberg header) | have | PG 35396 |
| `elise-lathrop-schubin-boris-lensky` | Ossip Schubin | Boris Lensky | Elise L. Lathrop | 1890-1891 (see the Gutenberg header) | have | PG 35491 |
| `elise-lathrop-schubin-felix-lanzberg-s-expiation` | Ossip Schubin | Felix Lanzberg's Expiation | Elise L. Lathrop | 1890-1891 (see the Gutenberg header) | have | PG 35571 |

## Joseph von Hammer-Purgstall (Evliya Çelebi's Travels, 2 parts)

Shelf: `pipeline/hammer-purgstall_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hammer-purgstall` · titles `python3 pipeline/split_shelf_titles.py hammer-purgstall`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hammer-purgstall-celebi-narrative-of-travels-in-europe-asia-and-vol-1` | Evliya Çelebi | Narrative of Travels in Europe, Asia, and Africa, in the Seventeenth Century, Vol. I | Joseph von Hammer-Purgstall | 1834-1850 (see the Gutenberg header) | have | PG 53597 |
| `hammer-purgstall-celebi-narrative-of-travels-in-europe-asia-and-vol-2` | Evliya Çelebi | Narrative of Travels in Europe, Asia, and Africa, in the Seventeenth Century, Vol. II | Joseph von Hammer-Purgstall | 1834-1850 (see the Gutenberg header) | have | PG 54255 |
| — | — | pg-56464: Turkish Literature (Colonial Press, 1901) is an anthology with several translators (Wilson, Arnot, Gibb and others). | — | — | excluded | — |

## Nathaniel Greene (Van der Velde's Tales from the German; Mühlbach)

Shelf: `pipeline/nathaniel-greene_shelf.json` · fetch `python3 pipeline/fetch_shelf.py nathaniel-greene` · titles `python3 pipeline/split_shelf_titles.py nathaniel-greene`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `nathaniel-greene-muhlbach-the-daughter-of-an-empress` | Luise Mühlbach | The Daughter of an Empress | Nathaniel Greene | 1837-1867 (see the Gutenberg header) | have | PG 2132 |
| `nathaniel-greene-velde-tales-from-the-german-vol-1` | Carl Franz van der Velde | Tales from the German.  Volume I. | Nathaniel Greene | 1837-1867 (see the Gutenberg header) | have | PG 32478 |
| `nathaniel-greene-velde-tales-from-the-german-vol-2` | Carl Franz van der Velde | Tales from the German.  Volume II. | Nathaniel Greene | 1837-1867 (see the Gutenberg header) | have | PG 32444 |

## H. Mainwaring Dunstan (Belot's A Parisian Sultana, 3 vols)

Shelf: `pipeline/dunstan_shelf.json` · fetch `python3 pipeline/fetch_shelf.py dunstan` · titles `python3 pipeline/split_shelf_titles.py dunstan`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `dunstan-belot-a-parisian-sultana-vol-1` | Adolphe Belot | A Parisian Sultana, Vol. 1 (of 3) | H. Mainwaring Dunstan | 1879 (see the Gutenberg header) | have | PG 58677 |
| `dunstan-belot-a-parisian-sultana-vol-2` | Adolphe Belot | A Parisian Sultana, Vol. 2 (of 3) | H. Mainwaring Dunstan | 1879 (see the Gutenberg header) | have | PG 58678 |
| `dunstan-belot-a-parisian-sultana-vol-3` | Adolphe Belot | A Parisian Sultana, Vol. 3 (of 3) | H. Mainwaring Dunstan | 1879 (see the Gutenberg header) | have | PG 58679 |

## Thomas De Quincey as translator (Walladmor, 2 vols)

Shelf: `pipeline/de-quincey-walladmor_shelf.json` · fetch `python3 pipeline/fetch_shelf.py de-quincey-walladmor` · titles `python3 pipeline/split_shelf_titles.py de-quincey-walladmor`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `de-quincey-walladmor-alexis-walladmor-vol-1` | Willibald Alexis | Walladmor, Vol. 1 (of 2) "Freely Translated into German from the English of Sir Walter Scott." And Now Freely Translated from the German into English. | Thomas De Quincey | 1825 (see the Gutenberg header) | have | PG 31563 |
| `de-quincey-walladmor-alexis-walladmor-vol-2` | Willibald Alexis | Walladmor, Vol. 2 (of 2) "Freely Translated into German from the English of Sir Walter Scott." And Now Freely Translated from the German into English. | Thomas De Quincey | 1825 (see the Gutenberg header) | have | PG 31568 |
| — | — | pg-35948: The Campaner Thal and Other Writings is a Jean Paul miscellany with several translators (Carlyle, Juliette Bauer, De Quincey). | — | — | excluded | — |

## Jane Frances Chapman (Ingemann's King Eric and the Outlaws, 3 vols)

Shelf: `pipeline/jane-chapman_shelf.json` · fetch `python3 pipeline/fetch_shelf.py jane-chapman` · titles `python3 pipeline/split_shelf_titles.py jane-chapman`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `jane-chapman-ingemann-king-eric-and-the-outlaws-vol-1` | Bernhard Severin Ingemann | King Eric and the Outlaws, Vol. 1 or, the Throne, the Church, and the People in the Thirteenth Century. | Jane Frances Chapman | 1843 (see the Gutenberg header) | have | PG 36631 |
| `jane-chapman-ingemann-king-eric-and-the-outlaws-vol-2` | Bernhard Severin Ingemann | King Eric and the Outlaws, Vol. 2 or, the Throne, the Church, and the People in the Thirteenth Century. | Jane Frances Chapman | 1843 (see the Gutenberg header) | have | PG 36632 |
| `jane-chapman-ingemann-king-eric-and-the-outlaws-vol-3` | Bernhard Severin Ingemann | King Eric and the Outlaws, Vol. 3 or, the Throne, the Church, and the People in the Thirteenth Century. | Jane Frances Chapman | 1843 (see the Gutenberg header) | have | PG 36633 |

## Mrs. Anna S. Bushby (The Danes, Sketched by Themselves, 3 vols)

Shelf: `pipeline/bushby_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bushby` · titles `python3 pipeline/split_shelf_titles.py bushby`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bushby-the-danes-sketched-by-themselves-vol-1` | Various Danish writers (compiled and translated by Mrs. Bushby) | The Danes, Sketched by Themselves. Vol. 1 (of 3) A Series of Popular Stories by the Best Danish Authors | Mrs. Anna S. Bushby | 1864 (see the Gutenberg header) | have | PG 37831 |
| `bushby-the-danes-sketched-by-themselves-vol-2` | Various Danish writers (compiled and translated by Mrs. Bushby) | The Danes, Sketched by Themselves. Vol. 2 (of 3) A Series of Popular Stories by the Best Danish Authors | Mrs. Anna S. Bushby | 1864 (see the Gutenberg header) | have | PG 37832 |
| `bushby-the-danes-sketched-by-themselves-vol-3` | Various Danish writers (compiled and translated by Mrs. Bushby) | The Danes, Sketched by Themselves. Vol. 3 (of 3) A Series of Popular Stories by the Best Danish Authors | Mrs. Anna S. Bushby | 1864 (see the Gutenberg header) | have | PG 37833 |
| — | — | pg-26491: Andersen's The Sand-Hills of Jutland is already shelved elsewhere. | — | — | excluded | — |

## B. G. Babington (Hecker's Black Death; Epidemics of the Middle Ages)

Shelf: `pipeline/babington_shelf.json` · fetch `python3 pipeline/fetch_shelf.py babington` · titles `python3 pipeline/split_shelf_titles.py babington`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `babington-hecker-the-black-death-in-the-fourteenth-centur` | Justus Friedrich Carl Hecker | The Black Death in the Fourteenth Century | B. G. Babington | 1833-1844 (see the Gutenberg header) | have | PG 52413 |
| `babington-hecker-the-epidemics-of-the-middle-ages` | Justus Friedrich Carl Hecker | The Epidemics of the Middle Ages | B. G. Babington | 1833-1844 (see the Gutenberg header) | have | PG 63232 |
| — | — | pg-1739: The Black Death and the Dancing Mania is Henry Morley's 1888 Cassell reprint of two parts of the 1844 Epidemics, which this shelf holds whole. | — | — | excluded | — |

## Raphael Meldola (Weismann's Studies in the Theory of Descent, 2 vols)

Shelf: `pipeline/meldola_shelf.json` · fetch `python3 pipeline/fetch_shelf.py meldola` · titles `python3 pipeline/split_shelf_titles.py meldola`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `meldola-weismann-studies-in-the-theory-of-descent-vol-1` | August Weismann | Studies in the Theory of Descent, Volume I | Raphael Meldola | 1882 (see the Gutenberg header) | have | PG 47847 |
| `meldola-weismann-studies-in-the-theory-of-descent-vol-2` | August Weismann | Studies in the Theory of Descent, Volume II | Raphael Meldola | 1882 (see the Gutenberg header) | have | PG 47848 |
| — | — | pg-47849: The two volumes again in one file; this shelf keeps them separately (47847, 47848). | — | — | excluded | — |

## Jean Paul Richter (The Notebooks of Leonardo da Vinci, 2 vols)

Shelf: `pipeline/jp-richter_shelf.json` · fetch `python3 pipeline/fetch_shelf.py jp-richter` · titles `python3 pipeline/split_shelf_titles.py jp-richter`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `jp-richter-leonardo-the-notebooks-of-leonardo-da-vinci-vol-1` | Leonardo da Vinci | The Notebooks of Leonardo Da Vinci — Volume 1 | Jean Paul Richter | 1883 (see the Gutenberg header) | have | PG 4998 |
| `jp-richter-leonardo-the-notebooks-of-leonardo-da-vinci-vol-2` | Leonardo da Vinci | The Notebooks of Leonardo Da Vinci — Volume 2 | Jean Paul Richter | 1883 (see the Gutenberg header) | have | PG 4999 |
| — | — | pg-5000: The two volumes again in one file; this shelf keeps them separately (4998, 4999). | — | — | excluded | — |

## Lord Stanley of Alderley (Barbosa; Pigafetta's Magellan; Alvares)

Shelf: `pipeline/lord-stanley_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lord-stanley` · titles `python3 pipeline/split_shelf_titles.py lord-stanley`.
Round 32 (2026-10-10), vetoable. Barbosa is keyed from a 1970 facsimile: flagged. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lord-stanley-alvares-narrative-of-the-portuguese-embassy-to-a` | Francisco Alvares | Narrative of the Portuguese embassy to Abyssinia during the years 1520-1527 | Henry E. J. Stanley, Lord Stanley of Alderley | 1866-1881 (see the Gutenberg header) | have | PG 72622 |
| `lord-stanley-barbosa-a-description-of-the-coasts-of-east-afri` | Duarte Barbosa | A Description of the Coasts of East Africa and Malabar in the Beginning of the Sixteenth Century | Henry E. J. Stanley, Lord Stanley of Alderley | 1866-1881 (see the Gutenberg header) | have | PG 38253 |
| `lord-stanley-pigafetta-the-first-voyage-round-the-world-by-mage` | Antonio Pigafetta | The first voyage round the world, by Magellan | Henry E. J. Stanley, Lord Stanley of Alderley | 1866-1881 (see the Gutenberg header) | have | PG 74723 |

## Francis J. Ziegler (Wedekind's The Awakening of Spring; Such is Life)

Shelf: `pipeline/ziegler_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ziegler` · titles `python3 pipeline/split_shelf_titles.py ziegler`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ziegler-wedekind-such-is-life-a-play-in-five-acts` | Frank Wedekind | Such is Life: A Play in Five Acts | Francis J. Ziegler | 1909-1912 (see the Gutenberg header) | have | PG 45228 |
| `ziegler-wedekind-the-awakening-of-spring-a-tragedy-of-chi` | Frank Wedekind | The Awakening of Spring: A Tragedy of Childhood | Francis J. Ziegler | 1909-1912 (see the Gutenberg header) | have | PG 35242 |

## W. Fitzwater Wray (Barbusse's Under Fire; Light)

Shelf: `pipeline/fitzwater-wray_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fitzwater-wray` · titles `python3 pipeline/split_shelf_titles.py fitzwater-wray`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fitzwater-wray-barbusse-light` | Henri Barbusse | Light | W. Fitzwater Wray | 1917-1919 (see the Gutenberg header) | have | PG 12904 |
| `fitzwater-wray-barbusse-under-fire-the-story-of-a-squad` | Henri Barbusse | Under Fire: The Story of a Squad | W. Fitzwater Wray | 1917-1919 (see the Gutenberg header) | have | PG 4380 |

## Otto Wenckstern (Eötvös's The Village Notary; Schlesinger)

Shelf: `pipeline/wenckstern_shelf.json` · fetch `python3 pipeline/fetch_shelf.py wenckstern` · titles `python3 pipeline/split_shelf_titles.py wenckstern`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `wenckstern-eotvos-the-village-notary-a-romance-of-hungaria` | József Eötvös | The Village Notary: A Romance of Hungarian Life | Otto Wenckstern | 1850-1853 (see the Gutenberg header) | have | PG 34819 |
| `wenckstern-schlesinger-saunterings-in-and-about-london` | Max Schlesinger | Saunterings in and about London | Otto Wenckstern | 1850-1853 (see the Gutenberg header) | have | PG 46571 |

## Albert D. Vandam (Sastrow's Memoirs; the Congress of Vienna)

Shelf: `pipeline/vandam_shelf.json` · fetch `python3 pipeline/fetch_shelf.py vandam` · titles `python3 pipeline/split_shelf_titles.py vandam`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `vandam-la-garde-chambonas-anecdotal-recollections-of-the-congress` | Auguste de La Garde-Chambonas | Anecdotal Recollections of the Congress of Vienna | Albert D. Vandam | 1902 (see the Gutenberg header) | have | PG 54061 |
| `vandam-sastrow-bartholomew-sastrow-being-the-memoirs-of` | Bartholomäus Sastrow | Bartholomew Sastrow: Being the Memoirs of a German Burgomaster | Albert D. Vandam | 1902 (see the Gutenberg header) | have | PG 33891 |

## Ernest Untermann (Engels's Origin of the Family; Dietzgen)

Shelf: `pipeline/untermann_shelf.json` · fetch `python3 pipeline/fetch_shelf.py untermann` · titles `python3 pipeline/split_shelf_titles.py untermann`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `untermann-dietzgen-the-positive-outcome-of-philosophy` | Joseph Dietzgen | The positive outcome of philosophy | Ernest Untermann | 1902-1906 (see the Gutenberg header) | have | PG 39964 |
| `untermann-engels-the-origin-of-the-family-private-propert` | Friedrich Engels | The origin of the family, private property, and the state | Ernest Untermann | 1902-1906 (see the Gutenberg header) | have | PG 33111 |

## Alma Strettell (Verhaeren's Poems; Memoirs of Mistral)

Shelf: `pipeline/strettell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py strettell` · titles `python3 pipeline/split_shelf_titles.py strettell`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `strettell-mistral-memoirs-of-mistral` | Frédéric Mistral | Memoirs of Mistral | Alma Strettell (with Constance Elizabeth Maud) | 1899-1907 (see the Gutenberg header) | have | PG 56040 |
| `strettell-verhaeren-poems-of-emile-verhaeren` | Emile Verhaeren | Poems of Emile Verhaeren | Alma Strettell | 1899-1907 (see the Gutenberg header) | have | PG 33792 |

## Lionel Strachey (Memoirs of Madame Vigée Lebrun; The Gray Nun)

Shelf: `pipeline/lionel-strachey_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lionel-strachey` · titles `python3 pipeline/split_shelf_titles.py lionel-strachey`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lionel-strachey-eschstruth-the-gray-nun` | Nataly von Eschstruth | The Gray Nun | Lionel Strachey | 1903-1905 (see the Gutenberg header) | have | PG 23220 |
| `lionel-strachey-vigee-lebrun-the-memoirs-of-madame-vigee-lebrun` | Louise-Elisabeth Vigée-Lebrun | The Memoirs of Madame Vigée Lebrun | Lionel Strachey | 1903-1905 (see the Gutenberg header) | have | PG 31934 |

## Edward Storer (Il Novellino; Pirandello's Three Plays)

Shelf: `pipeline/storer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py storer` · titles `python3 pipeline/split_shelf_titles.py storer`.
Round 32 (2026-10-10), vetoable. Three Plays is keyed from a post-1934 printing: flagged. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `storer-il-novellino-the-hundred-old-tales` | Anonymous (Il Novellino, 13th century) | Il Novellino: The hundred old tales | Edward Storer | 1922-1925 (see the Gutenberg header) | have | PG 68831 |
| `storer-pirandello-three-plays` | Luigi Pirandello | Three Plays | Edward Storer (with Arthur [Translator] Livingstone) | 1922-1925 (see the Gutenberg header) | have | PG 42148 |
| `storer-facetiae-of-poggio` | Poggio Bracciolini and other medieval story-tellers | The Facetiae of Poggio and Other Medieval Story-Tellers | Edward Storer | 1928 | have-raw | IA `facetiaeofpoggio0000brac` |

## Herman Scheffauer (Heine's Atta Troll; Mann's Bashan and I)

Shelf: `pipeline/scheffauer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py scheffauer` · titles `python3 pipeline/split_shelf_titles.py scheffauer`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `scheffauer-heine-atta-troll` | Heinrich Heine | Atta Troll | Herman Scheffauer | 1913-1923 (see the Gutenberg header) | have | PG 31305 |
| `scheffauer-mann-bashan-and-i` | Thomas Mann | Bashan and I | Herman Scheffauer | 1913-1923 (see the Gutenberg header) | have | PG 61284 |

## Percy Pinkerton (Artsybashev's Sanine; La Bohème libretto)

Shelf: `pipeline/pinkerton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py pinkerton` · titles `python3 pipeline/split_shelf_titles.py pinkerton`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `pinkerton-artsybashev-sanine` | Mikhail Artsybashev | Sanine | Percy Pinkerton | 1896-1914 (see the Gutenberg header) | have | PG 9051 |
| `pinkerton-giacosa-libretto-la-boheme` | Giuseppe Giacosa | Libretto: La Bohème | Percy Pinkerton (with William Grist) | 1896-1914 (see the Gutenberg header) | have | PG 13843 |

## Leo Ongley (Blasco Ibáñez's The Temptress; Gálvez)

Shelf: `pipeline/ongley_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ongley` · titles `python3 pipeline/split_shelf_titles.py ongley`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ongley-galvez-nacha-regules` | Manuel Gálvez | Nacha Regules | Leo Ongley | 1922-1923 (see the Gutenberg header) | have | PG 59441 |
| `ongley-ibanez-the-temptress-la-tierra-de-todos` | Vicente Blasco Ibáñez | The Temptress (La tierra de todos) | Leo Ongley | 1922-1923 (see the Gutenberg header) | have | PG 63649 |

## Jessie Lemont (Rilke's Poems; Auguste Rodin)

Shelf: `pipeline/jessie-lemont_shelf.json` · fetch `python3 pipeline/fetch_shelf.py jessie-lemont` · titles `python3 pipeline/split_shelf_titles.py jessie-lemont`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `jessie-lemont-rilke-auguste-rodin` | Rainer Maria Rilke | Auguste Rodin | Jessie Lemont (with Hans Trausil) | 1918-1919 (see the Gutenberg header) | have | PG 45605 |
| `jessie-lemont-rilke-poems` | Rainer Maria Rilke | Poems | Jessie Lemont | 1918-1919 (see the Gutenberg header) | have | PG 38594 |

## Lee M. Hollander (Kierkegaard selections, 1923; Einarsson)

Shelf: `pipeline/hollander_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hollander` · titles `python3 pipeline/split_shelf_titles.py hollander`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hollander-einarsson-sword-and-crozier-drama-in-five-acts` | Indriði Einarsson | Sword and crozier, drama in five acts | Lee M. Hollander | 1912-1923 (see the Gutenberg header) | have | PG 15298 |
| `hollander-kierkegaard-selections-from-the-writings-of-kierkega` | Søren Kierkegaard | Selections from the Writings of Kierkegaard | Lee M. Hollander | 1912-1923 (see the Gutenberg header) | have | PG 60333 |

## Gertrude Hall (Verlaine's Poems; Rostand's Chantecler)

Shelf: `pipeline/gertrude-hall_shelf.json` · fetch `python3 pipeline/fetch_shelf.py gertrude-hall` · titles `python3 pipeline/split_shelf_titles.py gertrude-hall`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `gertrude-hall-rostand-chantecler-play-in-four-acts` | Edmond Rostand | Chantecler: Play in Four Acts | Gertrude Hall | 1895-1910 (see the Gutenberg header) | have | PG 10747 |
| `gertrude-hall-verlaine-poems-of-paul-verlaine` | Paul Verlaine | Poems of Paul Verlaine | Gertrude Hall | 1895-1910 (see the Gutenberg header) | have | PG 8426 |

## Jethro Bithell (Zweig's Verhaeren; Turandot)

Shelf: `pipeline/bithell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bithell` · titles `python3 pipeline/split_shelf_titles.py bithell`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bithell-gozzi-turandot-princess-of-china-a-chinoiserie` | Carlo Gozzi | Turandot, Princess of China: A Chinoiserie in Three Acts | Jethro Bithell | 1913-1914 (see the Gutenberg header) | have | PG 26730 |
| `bithell-zweig-emile-verhaeren` | Stefan Zweig | Émile Verhaeren | Jethro Bithell | 1913-1914 (see the Gutenberg header) | have | PG 35387 |

## M. Prichard Agnetti (Fogazzaro's The Patriot; Leila)

Shelf: `pipeline/agnetti_shelf.json` · fetch `python3 pipeline/fetch_shelf.py agnetti` · titles `python3 pipeline/split_shelf_titles.py agnetti`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `agnetti-fogazzaro-leila` | Antonio Fogazzaro | Leila | M. Prichard Agnetti | 1906-1911 (see the Gutenberg header) | have | PG 78258 |
| `agnetti-fogazzaro-the-patriot-piccolo-mondo-antico` | Antonio Fogazzaro | The Patriot (Piccolo Mondo Antico) | M. Prichard Agnetti | 1906-1911 (see the Gutenberg header) | have | PG 33778 |

## Mamah Bouton Borthwick (Ellen Key)

Shelf: `pipeline/borthwick_shelf.json` · fetch `python3 pipeline/fetch_shelf.py borthwick` · titles `python3 pipeline/split_shelf_titles.py borthwick`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `borthwick-key-the-morality-of-woman-and-other-essays` | Ellen Key | The Morality of Woman, and Other Essays | Mamah Bouton Borthwick | 1911-1912 (see the Gutenberg header) | have | PG 34267 |
| `borthwick-key-the-woman-movement` | Ellen Key | The Woman Movement | Mamah Bouton Borthwick | 1911-1912 (see the Gutenberg header) | have | PG 60840 |

## George Kamensky (Mendeleyev's Principles of Chemistry, 2 vols)

Shelf: `pipeline/kamensky_shelf.json` · fetch `python3 pipeline/fetch_shelf.py kamensky` · titles `python3 pipeline/split_shelf_titles.py kamensky`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `kamensky-mendeleyev-the-principles-of-chemistry-vol-1` | Dmitry Ivanovich Mendeleyev | The Principles of Chemistry, Volume I | George Kamensky | 1891 (see the Gutenberg header) | have | PG 51326 |
| `kamensky-mendeleyev-the-principles-of-chemistry-vol-2` | Dmitry Ivanovich Mendeleyev | The Principles of Chemistry, Volume II | George Kamensky | 1891 (see the Gutenberg header) | have | PG 54210 |

## Benjamin Bucknall (Viollet-le-Duc)

Shelf: `pipeline/bucknall_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bucknall` · titles `python3 pipeline/split_shelf_titles.py bucknall`.
Round 32 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bucknall-viollet-le-duc-annals-of-a-fortress` | Eugène-Emmanuel Viollet-le-Duc | Annals of a Fortress | Benjamin Bucknall | 1874-1875 (see the Gutenberg header) | have | PG 41426 |
| `bucknall-viollet-le-duc-how-to-build-a-house` | Eugène-Emmanuel Viollet-le-Duc | How to build a house | Benjamin Bucknall | 1874-1875 (see the Gutenberg header) | have | PG 71669 |

## Laura E. Kendall (Verne, Ernest Daudet, Gaboriau)

Shelf: `pipeline/laura-kendall_shelf.json` · fetch `python3 pipeline/fetch_shelf.py laura-kendall` · titles `python3 pipeline/split_shelf_titles.py laura-kendall`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `laura-kendall-daudet-which-or-between-two-women` | Ernest Daudet | Which? Or, Between Two Women | Laura E. Kendall | 1886-1888 (see the Gutenberg header) | have | PG 21838 |
| `laura-kendall-gaboriau-a-thousand-francs-reward-and-military-sk` | Emile Gaboriau | A Thousand Francs Reward; and, Military Sketches | Laura E. Kendall | 1886-1888 (see the Gutenberg header) | have | PG 43730 |
| `laura-kendall-verne-ticket-no-9672` | Jules Verne | Ticket No. "9672" | Laura E. Kendall | 1886-1888 (see the Gutenberg header) | have | PG 13527 |

## R. S. Townsend (Turgenev's Virgin Soil; Tolstoi for the Young)

Shelf: `pipeline/rs-townsend_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rs-townsend` · titles `python3 pipeline/split_shelf_titles.py rs-townsend`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rs-townsend-tolstoy-tolstoi-for-the-young-select-tales-from` | Leo Tolstoy | Tolstoi for the young: Select tales from Tolstoi | R. S. Townsend | 1911-1917 (see the Gutenberg header) | have | PG 51708 |
| `rs-townsend-turgenev-virgin-soil` | Ivan Sergeevich Turgenev | Virgin Soil | R. S. Townsend | 1911-1917 (see the Gutenberg header) | have | PG 2466 |

## Silvanus P. Thompson (Huygens's Treatise on Light; Gilbert's De Magnete)

Shelf: `pipeline/silvanus-thompson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py silvanus-thompson` · titles `python3 pipeline/split_shelf_titles.py silvanus-thompson`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `silvanus-thompson-gilbert-on-the-magnet-magnetick-bodies-also-and` | William Gilbert | On the magnet, magnetick bodies also, and on the great magnet the earth a new physiology, demonstrated by many arguments & experiments | Silvanus P. Thompson | 1900-1912 (see the Gutenberg header) | have | PG 33810 |
| `silvanus-thompson-huygens-treatise-on-light` | Christiaan Huygens | Treatise on light | Silvanus P. Thompson | 1900-1912 (see the Gutenberg header) | have | PG 14725 |

## Surendranath Tagore (The Home and the World; My Reminiscences)

Shelf: `pipeline/surendranath-tagore_shelf.json` · fetch `python3 pipeline/fetch_shelf.py surendranath-tagore` · titles `python3 pipeline/split_shelf_titles.py surendranath-tagore`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `surendranath-tagore-tagore-my-reminiscences` | Rabindranath Tagore | My Reminiscences | Surendranath Tagore | 1917-1919 (see the Gutenberg header) | have | PG 22217 |
| `surendranath-tagore-tagore-the-home-and-the-world` | Rabindranath Tagore | The Home and the World | Surendranath Tagore | 1917-1919 (see the Gutenberg header) | have | PG 7166 |

## Rabindranath Tagore as translator (Songs of Kabir; The Crescent Moon)

Shelf: `pipeline/rabindranath-tagore_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rabindranath-tagore` · titles `python3 pipeline/split_shelf_titles.py rabindranath-tagore`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rabindranath-tagore-kabir-songs-of-kabir` | Kabir | Songs of Kabir | Rabindranath Tagore | 1913-1915 (see the Gutenberg header) | have | PG 6519 |
| `rabindranath-tagore-tagore-the-crescent-moon` | Rabindranath Tagore | The Crescent Moon | Rabindranath Tagore | 1913-1915 (see the Gutenberg header) | have | PG 6520 |

## Arthur Symons (Baudelaire's Poems in Prose; D'Annunzio's Child of Pleasure)

Shelf: `pipeline/arthur-symons_shelf.json` · fetch `python3 pipeline/fetch_shelf.py arthur-symons` · titles `python3 pipeline/split_shelf_titles.py arthur-symons`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `arthur-symons-baudelaire-poems-in-prose` | Charles Baudelaire | Poems in Prose | Arthur Symons | 1898-1905 (see the Gutenberg header) | have | PG 50489 |
| `arthur-symons-d-annunzio-the-child-of-pleasure` | Gabriele D'Annunzio | The Child of Pleasure | Georgina Harding (prose) and Arthur Symons (verse) | 1898-1905 (see the Gutenberg header) | have | PG 20015 |

## F. C. de Sumichrast (two volumes of his Gautier)

Shelf: `pipeline/sumichrast_shelf.json` · fetch `python3 pipeline/fetch_shelf.py sumichrast` · titles `python3 pipeline/split_shelf_titles.py sumichrast`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `sumichrast-gautier-my-private-menagerie-from-the-works-of-t` | Théophile Gautier | My Private Menagerie from The Works of Theophile Gautier Volume 19 | Frederick C. de Sumichrast | 1900-1903 (see the Gutenberg header) | have | PG 30760 |
| `sumichrast-gautier-the-romance-of-a-mummy-and-egypt-the-wor` | Théophile Gautier | The Romance of a Mummy and Egypt The Works of Theophile Gautier, Volume 5 | Frederick C. de Sumichrast | 1900-1903 (see the Gutenberg header) | have | PG 27724 |

## Rose Strunsky (Tolstoy's Journal, 1895-99; Gorky's The Confession)

Shelf: `pipeline/rose-strunsky_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rose-strunsky` · titles `python3 pipeline/split_shelf_titles.py rose-strunsky`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rose-strunsky-gorky-the-confession-a-novel` | Maksim Gorky | The Confession: A Novel | Rose Strunsky | 1916-1917 (see the Gutenberg header) | have | PG 55828 |
| `rose-strunsky-tolstoy-the-journal-of-leo-tolstoi-first-volume1` | Leo Tolstoy | The Journal of Leo Tolstoi (First Volume—1895-1899) | Rose Strunsky | 1916-1917 (see the Gutenberg header) | have | PG 46272 |

## Charles Wharton Stork (Modern Swedish Masterpieces; Söderberg)

Shelf: `pipeline/cw-stork_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cw-stork` · titles `python3 pipeline/split_shelf_titles.py cw-stork`.
Round 33 (2026-10-10), vetoable. Martin Birck's Youth is a 1930 first edition. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cw-stork-soderberg-martin-birck-s-youth` | Hjalmar Söderberg | Martin Birck's youth | Charles Wharton Stork | 1923-1930 (see the Gutenberg header) | have | PG 78363 |
| `cw-stork-stork-modern-swedish-masterpieces-short-storie` | Charles Wharton Stork | Modern Swedish Masterpieces: Short Stories | Charles Wharton Stork | 1923-1930 (see the Gutenberg header) | have | PG 64808 |

## S. A. Stern (Auerbach's On the Heights; Waldfried)

Shelf: `pipeline/adler-stern_shelf.json` · fetch `python3 pipeline/fetch_shelf.py adler-stern` · titles `python3 pipeline/split_shelf_titles.py adler-stern`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `adler-stern-auerbach-on-the-heights-a-novel` | Berthold Auerbach | On the Heights: A Novel | S. A. Stern | 1867-1874 (see the Gutenberg header) | have | PG 33294 |
| `adler-stern-auerbach-waldfried-a-novel` | Berthold Auerbach | Waldfried: A Novel | S. A. Stern | 1867-1874 (see the Gutenberg header) | have | PG 32446 |

## Mary G. Steegmann (Deledda's The Woman and the Priest; The Mother)

Shelf: `pipeline/steegmann_shelf.json` · fetch `python3 pipeline/fetch_shelf.py steegmann` · titles `python3 pipeline/split_shelf_titles.py steegmann`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `steegmann-deledda-the-mother` | Grazia Deledda | The mother | Mary G. Steegmann | 1922-1923 (see the Gutenberg header) | have | PG 77111 |
| `steegmann-deledda-the-woman-the-priest` | Grazia Deledda | The Woman & the Priest | Mary G. Steegmann | 1922-1923 (see the Gutenberg header) | have | PG 53918 |

## Wolf von Schierbrand (Keller's Seldwyla Folks; Bilse)

Shelf: `pipeline/schierbrand_shelf.json` · fetch `python3 pipeline/fetch_shelf.py schierbrand` · titles `python3 pipeline/split_shelf_titles.py schierbrand`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `schierbrand-bilse-a-little-garrison-a-realistic-novel-of-g` | Fritz Oswald Bilse | A Little Garrison: A Realistic Novel of German Army Life of To-day | Wolf von Schierbrand | 1904-1919 (see the Gutenberg header) | have | PG 31248 |
| `schierbrand-keller-seldwyla-folks-three-singular-tales` | Gottfried Keller | Seldwyla Folks: Three Singular Tales | Wolf von Schierbrand | 1904-1919 (see the Gutenberg header) | have | PG 34505 |

## M. Schele de Vere (two Spielhagen novels)

Shelf: `pipeline/schele-de-vere_shelf.json` · fetch `python3 pipeline/fetch_shelf.py schele-de-vere` · titles `python3 pipeline/split_shelf_titles.py schele-de-vere`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `schele-de-vere-spielhagen-problematic-characters-a-novel` | Friedrich Spielhagen | Problematic Characters: A Novel | M. Schele de Vere | 1869-1870 (see the Gutenberg header) | have | PG 34748 |
| `schele-de-vere-spielhagen-through-night-to-light-a-novel` | Friedrich Spielhagen | Through Night to Light: A Novel | M. Schele de Vere | 1869-1870 (see the Gutenberg header) | have | PG 34598 |
| — | — | pg-44430: Saintine's Myths of the Rhine is already shelved elsewhere. | — | — | excluded | — |

## Mrs. Sabine (Humboldt's Aspects of Nature, 2 vols)

Shelf: `pipeline/elizabeth-sabine_shelf.json` · fetch `python3 pipeline/fetch_shelf.py elizabeth-sabine` · titles `python3 pipeline/split_shelf_titles.py elizabeth-sabine`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `elizabeth-sabine-humboldt-aspects-of-nature-vol-1` | Alexander von Humboldt | Aspects of nature, in different lands and different climates (Vol. 1 of 2) with scientific elucidations | Elizabeth Juliana Sabine (Mrs. Sabine) | 1849 (see the Gutenberg header) | have | PG 67183 |
| `elizabeth-sabine-humboldt-aspects-of-nature-vol-2` | Alexander von Humboldt | Aspects of nature, in different lands and different climates (Vol. 2 of 2) with scientific elucidations | Elizabeth Juliana Sabine (Mrs. Sabine) | 1849 (see the Gutenberg header) | have | PG 68953 |

## Hermione Ramsden (Laura Marholm)

Shelf: `pipeline/ramsden_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ramsden` · titles `python3 pipeline/split_shelf_titles.py ramsden`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ramsden-marholm-six-modern-women-psychological-sketches` | Laura Marholm | Six modern women: Psychological sketches | Hermione Ramsden | 1896-1899 (see the Gutenberg header) | have | PG 68655 |
| `ramsden-marholm-we-women-and-our-authors` | Laura Marholm | We Women and Our Authors | Hermione Ramsden | 1896-1899 (see the Gutenberg header) | have | PG 67577 |

## Thomas Sergeant Perry (Imbert de Saint-Amand)

Shelf: `pipeline/ts-perry_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ts-perry` · titles `python3 pipeline/split_shelf_titles.py ts-perry`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ts-perry-saint-amand-the-court-of-the-empress-josephine` | Imbert de Saint-Amand | The Court of the Empress Josephine | Thomas Sergeant Perry | 1890-1891 (see the Gutenberg header) | have | PG 9831 |
| `ts-perry-saint-amand-the-happy-days-of-the-empress-marie-loui` | Imbert de Saint-Amand | The Happy Days of the Empress Marie Louise | Thomas Sergeant Perry | 1890-1891 (see the Gutenberg header) | have | PG 8575 |

## Karl Friedrich Neumann (the China Sea pirates; Vahram's Chronicle)

Shelf: `pipeline/neumann_shelf.json` · fetch `python3 pipeline/fetch_shelf.py neumann` · titles `python3 pipeline/split_shelf_titles.py neumann`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `neumann-vahram-vahram-s-chronicle-of-the-armenian-kingd` | Vahram | Vahram's chronicle of the Armenian kingdom in Cilicia, during the time of the Crusades. | Charles Fried. Neumann | 1831 (see the Gutenberg header) | have | PG 60171 |
| `neumann-yuan-history-of-the-pirates-who-infested-the` | Yung-lun Yüan | History of the Pirates Who Infested the China Sea From 1807 to 1810 | Charles Fried. Neumann | 1831 (see the Gutenberg header) | have | PG 44261 |

## Lady Moreton (Coloma's Don John of Austria; Perez the Mouse)

Shelf: `pipeline/lady-moreton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lady-moreton` · titles `python3 pipeline/split_shelf_titles.py lady-moreton`.
Round 33 (2026-10-10), vetoable. Perez the Mouse is keyed from a 1935 reprint: flagged. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lady-moreton-coloma-perez-the-mouse` | Luis Coloma | Perez the Mouse | Lady Moreton | 1912-1914 (see the Gutenberg header) | have | PG 29447 |
| `lady-moreton-coloma-the-story-of-don-john-of-austria` | Luis Coloma | The Story of Don John of Austria | Lady Moreton | 1912-1914 (see the Gutenberg header) | have | PG 53383 |

## Emily Jakowleff and Dora B. Montefiore (Gorky)

Shelf: `pipeline/jakowleff-montefiore_shelf.json` · fetch `python3 pipeline/fetch_shelf.py jakowleff-montefiore` · titles `python3 pipeline/split_shelf_titles.py jakowleff-montefiore`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `jakowleff-montefiore-gorky-the-orloff-couple-and-malva` | Maksim Gorky | The Orloff Couple, and Malva | Emily Jakowleff and Dora B. Montefiore | 1901-1902 (see the Gutenberg header) | have | PG 55582 |
| `jakowleff-montefiore-gorky-the-outcasts-and-other-stories` | Maksim Gorky | The Outcasts, and Other Stories | Emily Jakowleff and Dora B. Montefiore (with Vera Volkhovsky) | 1901-1902 (see the Gutenberg header) | have | PG 55861 |

## Edgar Jepson (Leblanc's Arsène Lupin; Leroux)

Shelf: `pipeline/jepson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py jepson` · titles `python3 pipeline/split_shelf_titles.py jepson`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `jepson-leblanc-arsene-lupin` | Maurice Leblanc | Arsène Lupin | Edgar Jepson | 1909-1912 (see the Gutenberg header) | have | PG 4014 |
| `jepson-leroux-the-man-with-the-black-feather` | Gaston Leroux | The Man with the Black Feather | Edgar Jepson | 1909-1912 (see the Gutenberg header) | have | PG 46343 |

## Sivert and Elizabeth Hjerleid (Bjørnson)

Shelf: `pipeline/hjerleid_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hjerleid` · titles `python3 pipeline/split_shelf_titles.py hjerleid`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hjerleid-bjornson-ovind-a-story-of-country-life-in-norway` | Bjørnstjerne Bjørnson | Ovind: A Story of Country Life in Norway | Sivert and Elizabeth Hjerleid | 1869 (see the Gutenberg header) | have | PG 37727 |
| `hjerleid-bjornson-the-fisher-girl` | Bjørnstjerne Bjørnson | The Fisher Girl | Sivert and Elizabeth Hjerleid | 1869 (see the Gutenberg header) | have | PG 37725 |

## John D. Godman (Levasseur's Lafayette in America, 2 vols)

Shelf: `pipeline/godman_shelf.json` · fetch `python3 pipeline/fetch_shelf.py godman` · titles `python3 pipeline/split_shelf_titles.py godman`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `godman-levasseur-lafayette-in-america-in-1824-and-1825-vol-1` | Auguste Levasseur | Lafayette in America in 1824 and 1825, Vol. 1 (of 2) Or, Journal of a Voyage to the United States | John D. Godman | 1829 (see the Gutenberg header) | have | PG 61518 |
| `godman-levasseur-lafayette-in-america-in-1824-and-1825-vol-2` | Auguste Levasseur | Lafayette in America in 1824 and 1825, Vol. 2 (of 2) Or, Journal of a Voyage to the United States | John D. Godman | 1829 (see the Gutenberg header) | have | PG 61778 |

## Selina Gaye (two Jósika novels)

Shelf: `pipeline/selina-gaye_shelf.json` · fetch `python3 pipeline/fetch_shelf.py selina-gaye` · titles `python3 pipeline/split_shelf_titles.py selina-gaye`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `selina-gaye-josika-king-matthias-and-the-beggar-boy` | Miklós Jósika | King Matthias and the Beggar Boy | Selina Gaye | 1904 and earlier (see the Gutenberg header) | have | PG 36816 |
| `selina-gaye-josika-neath-the-hoof-of-the-tartar-or-the-scou` | Miklós Jósika | 'Neath the Hoof of the Tartar; Or, The Scourge of God | Selina Gaye | 1904 and earlier (see the Gutenberg header) | have | PG 36203 |

## J. H. Freese (The Library of Photius; Niemann)

Shelf: `pipeline/freese_shelf.json` · fetch `python3 pipeline/fetch_shelf.py freese` · titles `python3 pipeline/split_shelf_titles.py freese`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `freese-i-the-library-of-photius-volume-1-of-1` | Saint Photius I | The library of Photius, Volume 1 (of 1) | J. H. Freese | 1904-1920 (see the Gutenberg header) | have | PG 79139 |
| `freese-niemann-the-coming-conquest-of-england` | August Niemann | The Coming Conquest of England | J. H. Freese | 1904-1920 (see the Gutenberg header) | have | PG 2026 |
| — | — | pg-10828: Livy's Roman History is not his translation (Freese is only credited as an editor) and is already shelved elsewhere. | — | — | excluded | — |

## Duncan Forbes (Hatim Taï; Bagh o Bahar)

Shelf: `pipeline/duncan-forbes_shelf.json` · fetch `python3 pipeline/fetch_shelf.py duncan-forbes` · titles `python3 pipeline/split_shelf_titles.py duncan-forbes`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `duncan-forbes-dihlavi-bagh-o-bahar-or-tales-of-the-four-darwes` | Amir Khusraw Dihlavi | Bagh O Bahar, or Tales of the Four Darweshes | Duncan Forbes | 1830-1857 (see the Gutenberg header) | have | PG 12370 |
| `duncan-forbes-forbes-the-adventures-of-hatim-tai-a-romance` | Duncan Forbes | The adventures of Hatim Taï, a romance | Duncan Forbes | 1830-1857 (see the Gutenberg header) | have | PG 70290 |

## Jacob S. Fassett (Pío Baroja)

Shelf: `pipeline/fassett_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fassett` · titles `python3 pipeline/split_shelf_titles.py fassett`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fassett-baroja-the-city-of-the-discreet` | Pío Baroja | The city of the discreet | Jacob S. Fassett | 1917-1920 (see the Gutenberg header) | have | PG 56324 |
| `fassett-baroja-youth-and-egolatry` | Pío Baroja | Youth and Egolatry | Jacob S. Fassett (with Frances L. Phillips) | 1917-1920 (see the Gutenberg header) | have | PG 8148 |

## Charles De Kay (Rolland's Pierre and Luce; Daudet's Numa Roumestan)

Shelf: `pipeline/de-kay_shelf.json` · fetch `python3 pipeline/fetch_shelf.py de-kay` · titles `python3 pipeline/split_shelf_titles.py de-kay`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `de-kay-daudet-numa-roumestan` | Alphonse Daudet | Numa Roumestan | Charles De Kay | 1882-1922 (see the Gutenberg header) | have | PG 69808 |
| `de-kay-rolland-pierre-and-luce` | Romain Rolland | Pierre and Luce | Charles De Kay | 1882-1922 (see the Gutenberg header) | have | PG 31542 |

## Fanny S. Copeland (Croatian Tales of Long Ago; The Slav Nations)

Shelf: `pipeline/fanny-copeland_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fanny-copeland` · titles `python3 pipeline/split_shelf_titles.py fanny-copeland`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fanny-copeland-brlic-mazuranic-croatian-tales-of-long-ago` | Ivana Brlic-Mazuranic | Croatian Tales of Long Ago | Fanny S. Copeland | 1915-1924 (see the Gutenberg header) | have | PG 60095 |
| `fanny-copeland-tucic-the-slav-nations` | Srdan Tucic | The Slav Nations | Fanny S. Copeland | 1915-1924 (see the Gutenberg header) | have | PG 54348 |

## Oliver C. Colt (Marbot's Memoirs; Tartarin de Tarascon)

Shelf: `pipeline/oliver-colt_shelf.json` · fetch `python3 pipeline/fetch_shelf.py oliver-colt` · titles `python3 pipeline/split_shelf_titles.py oliver-colt`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `oliver-colt-daudet-tartarin-de-tarascon` | Alphonse Daudet | Tartarin de Tarascon | Oliver C. Colt | 1892 and earlier (see the Gutenberg header) | have | PG 2375 |
| `oliver-colt-marbot-the-memoirs-of-general-baron-de-marbot` | Jean-Baptiste-Antoine-Marcelin Marbot | The Memoirs of General Baron de Marbot | Oliver C. Colt | 1892 and earlier (see the Gutenberg header) | have | PG 2401 |

## I. G. Burnham (Gautier's Mademoiselle de Maupin, 2 vols)

Shelf: `pipeline/burnham-maupin_shelf.json` · fetch `python3 pipeline/fetch_shelf.py burnham-maupin` · titles `python3 pipeline/split_shelf_titles.py burnham-maupin`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `burnham-maupin-gautier-mademoiselle-de-maupin-volume-1-of-2` | Théophile Gautier | Mademoiselle de Maupin, Volume 1 (of 2) | I. G. Burnham | 1897-1900 (see the Gutenberg header) | have | PG 48893 |
| `burnham-maupin-gautier-mademoiselle-de-maupin-volume-2-of-2` | Théophile Gautier | Mademoiselle de Maupin, Volume 2 (of 2) | I. G. Burnham | 1897-1900 (see the Gutenberg header) | have | PG 48894 |

## Henry F. Brownson (Balmes's Fundamental Philosophy, 2 vols)

Shelf: `pipeline/hf-brownson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hf-brownson` · titles `python3 pipeline/split_shelf_titles.py hf-brownson`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hf-brownson-balmes-fundamental-philosophy-vol-1-of-2` | Jaime Luciano Balmes | Fundamental Philosophy, Vol. 1 (of 2) | Henry F. Brownson | 1856 (see the Gutenberg header) | have | PG 48149 |
| `hf-brownson-balmes-fundamental-philosophy-vol-2-of-2` | Jaime Luciano Balmes | Fundamental Philosophy, Vol. 2 (of 2) | Henry F. Brownson | 1856 (see the Gutenberg header) | have | PG 49244 |

## William Aspenwall Bradley (Gourmont's Decadence; Flamenca)

Shelf: `pipeline/wa-bradley_shelf.json` · fetch `python3 pipeline/fetch_shelf.py wa-bradley` · titles `python3 pipeline/split_shelf_titles.py wa-bradley`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `wa-bradley-bradley-the-story-of-flamenca` | William Aspenwall Bradley | The story of Flamenca | William Aspenwall Bradley | 1921-1922 (see the Gutenberg header) | have | PG 75417 |
| `wa-bradley-gourmont-decadence-and-other-essays-on-the-cultur` | Remy de Gourmont | Decadence, and Other Essays on the Culture of Ideas | William Aspenwall Bradley | 1921-1922 (see the Gutenberg header) | have | PG 46728 |

## T. G. Bonney (Pierotti's Jerusalem Explored)

Shelf: `pipeline/bonney_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bonney` · titles `python3 pipeline/split_shelf_titles.py bonney`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bonney-pierotti-jerusalem-explored-volume-1text-being-a` | Ermete Pierotti | Jerusalem Explored, Volume 1—Text Being a Description of the Ancient and Modern City, with Numerous Illustrations Consisting of Views, Ground Plans and Sections | T. G. Bonney | 1864 (see the Gutenberg header) | have | PG 41569 |
| — | — | pg-44241: Jerusalem Explored vol. 2 is the plates volume: images with captions, nearly no text to read or cite. | — | — | excluded | — |

## S. E. Boggs (two Jókai novels)

Shelf: `pipeline/se-boggs_shelf.json` · fetch `python3 pipeline/fetch_shelf.py se-boggs` · titles `python3 pipeline/split_shelf_titles.py se-boggs`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `se-boggs-jokai-the-nameless-castle` | Mór Jókai | The nameless castle | S. E. Boggs | 1898-1902 (see the Gutenberg header) | have | PG 14048 |
| `se-boggs-jokai-told-by-the-death-s-head` | Mór Jókai | Told by the death's head | S. E. Boggs | 1898-1902 (see the Gutenberg header) | have | PG 34770 |

## Max A. Drezmal (Sienkiewicz's In Desert and Wilderness; Whirlpools)

Shelf: `pipeline/drezmal_shelf.json` · fetch `python3 pipeline/fetch_shelf.py drezmal` · titles `python3 pipeline/split_shelf_titles.py drezmal`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `drezmal-sienkiewicz-in-desert-and-wilderness` | Henryk Sienkiewicz | In Desert and Wilderness | Max A. Drezmal | 1910-1912 (see the Gutenberg header) | have | PG 30365 |
| `drezmal-sienkiewicz-whirlpools-a-novel-of-modern-poland` | Henryk Sienkiewicz | Whirlpools: A Novel of Modern Poland | Max A. Drezmal | 1910-1912 (see the Gutenberg header) | have | PG 37426 |

## E. B. Cowell (the Sarva-Darsana-Samgraha; the Tattva-Muktavali)

Shelf: `pipeline/cowell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cowell` · titles `python3 pipeline/split_shelf_titles.py cowell`.
Round 33 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cowell-gaudapurnanandacakravarti-the-tattva-muktavali` | active 17th century Gaudapurnanandacakravarti | The Tattva-Muktavali | E. B. Cowell | 1882 (see the Gutenberg header) | have | PG 7175 |
| `cowell-madhava-the-sarva-darsana-samgraha-or-review-of` | Madhava | The Sarva-Darsana-Samgraha Or, Review of the Different Systems of Hindu Philosophy | E. B. Cowell (with Archibald Edward Gough) | 1882 (see the Gutenberg header) | have | PG 34125 |

## William Whiston (The Works of Josephus, 5 titles)

Shelf: `pipeline/whiston_shelf.json` · fetch `python3 pipeline/fetch_shelf.py whiston` · titles `python3 pipeline/split_shelf_titles.py whiston`.
Round 34 (2026-10-10), vetoable. Lane B left Josephus unassigned. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `whiston-josephus-against-apion` | Flavius Josephus | Against Apion | William Whiston | 1737 (see the Gutenberg header) | have | PG 2849 |
| `whiston-josephus-antiquities-of-the-jews` | Flavius Josephus | Antiquities of the Jews | William Whiston | 1737 (see the Gutenberg header) | have | PG 2848 |
| `whiston-josephus-discourse-to-the-greeks-concerning-hades` | Flavius Josephus | An Extract out of Josephus's Discourse to The Greeks Concerning Hades | William Whiston | 1737 (see the Gutenberg header) | have | PG 2847 |
| `whiston-josephus-the-life-of-flavius-josephus` | Flavius Josephus | The Life of Flavius Josephus | William Whiston | 1737 (see the Gutenberg header) | have | PG 2846 |
| `whiston-josephus-the-wars-of-the-jews` | Flavius Josephus | The Wars of the Jews; Or, The History of the Destruction of Jerusalem | William Whiston | 1737 (see the Gutenberg header) | have | PG 2850 |

## Kisari Mohan Ganguli (the complete prose Mahabharata, 4 vols)

Shelf: `pipeline/ganguli_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ganguli` · titles `python3 pipeline/split_shelf_titles.py ganguli`.
Round 34 (2026-10-10), vetoable. Gutenberg's single-parva files are left out as duplicates. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ganguli-vyasa-the-mahabharata-vol-1` | Vyasa (attributed) | The Mahabharata of Krishna-Dwaipayana Vyasa, Volume 1 Books 1, 2 and 3 | Kisari Mohan Ganguli | 1883-1896 (see the Gutenberg header) | have | PG 15474 |
| `ganguli-vyasa-the-mahabharata-vol-2` | Vyasa (attributed) | The Mahabharata of Krishna-Dwaipayana Vyasa, Volume 2 Books 4, 5, 6 and 7 | Kisari Mohan Ganguli | 1883-1896 (see the Gutenberg header) | have | PG 15475 |
| `ganguli-vyasa-the-mahabharata-vol-3` | Vyasa (attributed) | The Mahabharata of Krishna-Dwaipayana Vyasa, Volume 3 Books 8, 9, 10, 11 and 12 | Kisari Mohan Ganguli | 1883-1896 (see the Gutenberg header) | have | PG 15476 |
| `ganguli-vyasa-the-mahabharata-vol-4` | Vyasa (attributed) | The Mahabharata of Krishna-Dwaipayana Vyasa, Volume 4 Books 13, 14, 15, 16, 17 and 18 | Kisari Mohan Ganguli | 1883-1896 (see the Gutenberg header) | have | PG 15477 |
| — | — | pg-7864: A single parva of the same translation; the four volumes on this shelf hold all eighteen books. | — | — | excluded | — |
| — | — | pg-7965: A single parva of the same translation; the four volumes on this shelf hold all eighteen books. | — | — | excluded | — |
| — | — | pg-11894: A single parva of the same translation; the four volumes on this shelf hold all eighteen books. | — | — | excluded | — |
| — | — | pg-12058: A single parva of the same translation; the four volumes on this shelf hold all eighteen books. | — | — | excluded | — |
| — | — | pg-12333: A single parva of the same translation; the four volumes on this shelf hold all eighteen books. | — | — | excluded | — |

## Manmatha Nath Dutt (prose Ramayana, 4 vols; Harivamsha; Vishnupuranam)

Shelf: `pipeline/mn-dutt_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mn-dutt` · titles `python3 pipeline/split_shelf_titles.py mn-dutt`.
Round 34 (2026-10-10), vetoable. Not R. C. Dutt (Lane D's dutt shelf). Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mn-dutt-harivamsha` | Anonymous (the Harivamsha, the appendix to the Mahabharata) | A Prose English Translation of Harivamsha | Manmatha Nath Dutt | 1891-1897 (see the Gutenberg header) | have | PG 61937 |
| `mn-dutt-valmiki-the-ramayana-vol-1` | Valmiki (attributed) | The Rāmāyana, Volume 1. Bālakāndam and Ayodhyākāndam | Manmatha Nath Dutt | 1891-1897 (see the Gutenberg header) | have | PG 57265 |
| `mn-dutt-valmiki-the-ramayana-vol-2` | Valmiki (attributed) | The Rāmāyana, Volume 2. Āranya, Kishkindhā, and Sundara Kāndam | Manmatha Nath Dutt | 1891-1897 (see the Gutenberg header) | have | PG 57826 |
| `mn-dutt-valmiki-the-ramayana-vol-3` | Valmiki (attributed) | The Rāmāyana, Volume 3. Yuddhakāndam | Manmatha Nath Dutt | 1891-1897 (see the Gutenberg header) | have | PG 60188 |
| `mn-dutt-valmiki-the-ramayana-vol-4` | Valmiki (attributed) | The Rāmāyana, Volume 4. Uttara Kānda | Manmatha Nath Dutt | 1891-1897 (see the Gutenberg header) | have | PG 62496 |
| `mn-dutt-vishnupuranam` | Anonymous (the Vishnu Purana) | A Prose English Translation of Vishnupuranam (Based on Professor H. H. Wilson's translation.) | Manmatha Nath Dutt (after H. H. Wilson) | 1891-1897 (see the Gutenberg header) | have | PG 66208 |

## George Saintsbury (Marguerite of Navarre's Heptameron, 5 vols)

Shelf: `pipeline/saintsbury-heptameron_shelf.json` · fetch `python3 pipeline/fetch_shelf.py saintsbury-heptameron` · titles `python3 pipeline/split_shelf_titles.py saintsbury-heptameron`.
Round 34 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `saintsbury-heptameron-marguerite-the-heptameron-vol-1` | Marguerite of Navarre | The Tales of the Heptameron, Vol. 1 (of 5) | George Saintsbury | 1894 (see the Gutenberg header) | have | PG 17701 |
| `saintsbury-heptameron-marguerite-the-heptameron-vol-2` | Marguerite of Navarre | The Tales of the Heptameron, Vol. 2 (of 5) | George Saintsbury | 1894 (see the Gutenberg header) | have | PG 17702 |
| `saintsbury-heptameron-marguerite-the-heptameron-vol-3` | Marguerite of Navarre | The Tales of the Heptameron, Vol. 3 (of 5) | George Saintsbury | 1894 (see the Gutenberg header) | have | PG 17703 |
| `saintsbury-heptameron-marguerite-the-heptameron-vol-4` | Marguerite of Navarre | The Tales of the Heptameron, Vol. 4 (of 5) | George Saintsbury | 1894 (see the Gutenberg header) | have | PG 17704 |
| `saintsbury-heptameron-marguerite-the-heptameron-vol-5` | Marguerite of Navarre | The Tales of the Heptameron, Vol. 5 (of 5) | George Saintsbury | 1894 (see the Gutenberg header) | have | PG 17705 |
| — | — | pg-28858: A linked index to the same Heptameron volumes, not a text. | — | — | excluded | — |

## Vihari-Lala Mitra (The Yoga-Vasishtha, 7 parts)

Shelf: `pipeline/viharilala-mitra_shelf.json` · fetch `python3 pipeline/fetch_shelf.py viharilala-mitra` · titles `python3 pipeline/split_shelf_titles.py viharilala-mitra`.
Round 34 (2026-10-10), vetoable. Keyed from modern photo-reprints: flagged. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `viharilala-mitra-yoga-vasishtha-vol-1` | Valmiki (attributed) | The Yoga-Vasishtha Maharamayana of Valmiki, Vol. 1 (of 4) | Vihari-Lala Mitra | 1891-1899 (see the Gutenberg header) | have | PG 71326 |
| `viharilala-mitra-yoga-vasishtha-vol-2-part-1` | Valmiki (attributed) | The Yoga-Vasishtha Maharamayana of Valmiki, Vol. 2 (of 4), Part 1 (of 2) | Vihari-Lala Mitra | 1891-1899 (see the Gutenberg header) | have | PG 71063 |
| `viharilala-mitra-yoga-vasishtha-vol-2-part-2` | Valmiki (attributed) | The Yoga-Vasishtha Maharamayana of Valmiki, Vol. 2 (of 4), Part 2 (of 2) | Vihari-Lala Mitra | 1891-1899 (see the Gutenberg header) | have | PG 71064 |
| `viharilala-mitra-yoga-vasishtha-vol-3-part-1` | Valmiki (attributed) | The Yoga-Vasishtha Maharamayana of Valmiki, Vol. 3 (of 4), Part 1 (of 2) | Vihari-Lala Mitra | 1891-1899 (see the Gutenberg header) | have | PG 71095 |
| `viharilala-mitra-yoga-vasishtha-vol-3-part-2` | Valmiki (attributed) | The Yoga-Vasishtha Maharamayana of Valmiki, Vol. 3 (of 4), Part 2 (of 2) | Vihari-Lala Mitra | 1891-1899 (see the Gutenberg header) | have | PG 46531 |
| `viharilala-mitra-yoga-vasishtha-vol-4-part-1` | Valmiki (attributed) | The Yoga-Vasishtha Maharamayana of Valmiki, Vol 4 (of 4), Part 1 (of 2) | Vihari-Lala Mitra | 1891-1899 (see the Gutenberg header) | have | PG 71248 |
| `viharilala-mitra-yoga-vasishtha-vol-4-part-2` | Valmiki (attributed) | The Yoga-Vasishtha Maharamayana of Valmiki, Vol. 4 (of 4), Part 2 (of 2) | Vihari-Lala Mitra | 1891-1899 (see the Gutenberg header) | have | PG 71249 |

## Tobias Smollett as translator (Gil Blas, 3 vols; Don Quixote; Voltaire's Peter the Great)

Shelf: `pipeline/smollett-translations_shelf.json` · fetch `python3 pipeline/fetch_shelf.py smollett-translations` · titles `python3 pipeline/split_shelf_titles.py smollett-translations`.
Round 34 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `smollett-translations-cervantes-don-quixote` | Miguel de Cervantes | The history and adventures of the renowned Don Quixote | Tobias Smollett | 1749-1761 (see the Gutenberg header) | have | PG 77095 |
| `smollett-translations-le-sage-gil-blas-vol-1` | Alain-René Le Sage | The Adventures of Gil Blas of Santillane, Volume 1 (of 3) | Tobias Smollett | 1749-1761 (see the Gutenberg header) | have | PG 66677 |
| `smollett-translations-le-sage-gil-blas-vol-2` | Alain-René Le Sage | The Adventures of Gil Blas of Santillane, Volume 2 (of 3) | Tobias Smollett | 1749-1761 (see the Gutenberg header) | have | PG 66678 |
| `smollett-translations-le-sage-gil-blas-vol-3` | Alain-René Le Sage | The Adventures of Gil Blas of Santillane, Volume 3 (of 3) | Tobias Smollett | 1749-1761 (see the Gutenberg header) | have | PG 66679 |
| `smollett-translations-voltaire-the-history-of-peter-the-great` | Voltaire | The History of Peter the Great, Emperor of Russia | Tobias Smollett | 1749-1761 (see the Gutenberg header) | have | PG 42540 |

## Rasmus B. Anderson (Bjørnson; Rydberg's Teutonic Mythology, 3 vols; Brandes; Lumholtz)

Shelf: `pipeline/rasmus-anderson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rasmus-anderson` · titles `python3 pipeline/split_shelf_titles.py rasmus-anderson`.
Round 35 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rasmus-anderson-bjornson-a-happy-boy` | Bjørnstjerne Bjørnson | A Happy Boy | Rasmus B. Anderson | 1881-1889 (see the Gutenberg header) | have | PG 12633 |
| `rasmus-anderson-bjornson-arne` | Bjørnstjerne Bjørnson | Arne; Early Tales and Sketches Patriots Edition | Rasmus B. Anderson | 1881-1889 (see the Gutenberg header) | have | PG 39744 |
| `rasmus-anderson-bjornson-magnhild-dust` | Bjørnstjerne Bjørnson | Magnhild; Dust | Rasmus B. Anderson | 1881-1889 (see the Gutenberg header) | have | PG 33683 |
| `rasmus-anderson-brandes-eminent-authors-of-the-nineteenth-century` | Georg Brandes | Eminent Authors of the Nineteenth Century: Literary Portraits | Rasmus B. Anderson | 1881-1889 (see the Gutenberg header) | have | PG 49999 |
| `rasmus-anderson-lumholtz-among-cannibals` | Carl Lumholtz | Among Cannibals: An Account of Four Years' Travels in Australia and of Camp Life With the Aborigines of Queensland | Rasmus B. Anderson | 1881-1889 (see the Gutenberg header) | have | PG 66299 |
| `rasmus-anderson-rydberg-teutonic-mythology-vol-1` | Viktor Rydberg | Teutonic Mythology: Gods and Goddesses of the Northland, Vol. 1 | Rasmus B. Anderson | 1881-1889 (see the Gutenberg header) | have | PG 37876 |
| `rasmus-anderson-rydberg-teutonic-mythology-vol-2` | Viktor Rydberg | Teutonic Mythology: Gods and Goddesses of the Northland, Vol. 2 | Rasmus B. Anderson | 1881-1889 (see the Gutenberg header) | have | PG 58829 |
| `rasmus-anderson-rydberg-teutonic-mythology-vol-3` | Viktor Rydberg | Teutonic Mythology: Gods and Goddesses of the Northland, Vol. 3 | Rasmus B. Anderson | 1881-1889 (see the Gutenberg header) | have | PG 58830 |

## William Archer beyond Ibsen (Nansen's Eskimo Life; Kielland)

Shelf: `pipeline/archer-other_shelf.json` · fetch `python3 pipeline/fetch_shelf.py archer-other` · titles `python3 pipeline/split_shelf_titles.py archer-other`.
Round 35 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `archer-other-kielland-tales-of-two-countries` | Alexander Lange Kielland | Tales of Two Countries | William Archer | 1891-1893 (see the Gutenberg header) | have | PG 8663 |
| `archer-other-nansen-eskimo-life` | Fridtjof Nansen | Eskimo Life | William Archer | 1891-1893 (see the Gutenberg header) | have | PG 46972 |
| — | — | single-play-ibsen: Gutenberg's single Ibsen plays (4070, 4093, 4782, 7942, 8121, 18428, 18792) are excluded on archer-ibsen_shelf.json as duplicates of the collected set. | — | — | excluded | — |

## George Borrow as translator (Romantic Ballads; The Sleeping Bard; Faustus; Welsh Poems; the Wise ballad pamphlets)

Shelf: `pipeline/borrow-translations_shelf.json` · fetch `python3 pipeline/fetch_shelf.py borrow-translations` · titles `python3 pipeline/split_shelf_titles.py borrow-translations`.
Round 35 (2026-10-10), vetoable. Lane D's borrow shelf keeps the Turkish Jester. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `borrow-translations-alf-the-freebooter-little-danneved-and-s` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Alf the Freebooter, Little Danneved and Swayne Trost, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26787 |
| `borrow-translations-axel-thordson-and-fair-valborg-a-ballad` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Axel Thordson and Fair Valborg: a ballad | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 27406 |
| `borrow-translations-brown-william-the-power-of-the-harp-and` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Brown William, The Power of the Harp, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26788 |
| `borrow-translations-child-maidelvold-and-other-ballads` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Child Maidelvold, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 28771 |
| `borrow-translations-ellen-of-villenskov-and-other-ballads` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Ellen of Villenskov, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 28772 |
| `borrow-translations-embeo-e-majaro-lucas` | The Gospel of Luke (Borrow's Romani version) | Embéo e Majaró Lucas | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 29470 |
| `borrow-translations-emelian-the-fool-a-tale` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Emelian the Fool: a tale | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26789 |
| `borrow-translations-ermeline` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Ermeline | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26791 |
| `borrow-translations-finnish-arts-or-sir-thor-and-damsel-thur` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Finnish Arts; Or, Sir Thor and Damsel Thure, a Ballad | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 28774 |
| `borrow-translations-grimmer-and-kamper-the-end-of-sivard-sna` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Grimmer and Kamper, The End of Sivard Snarenswayne, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26792 |
| `borrow-translations-hafbur-and-signe-a-ballad` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Hafbur and Signe: a ballad | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 27473 |
| `borrow-translations-king-diderik-and-the-fight-between-the-l` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | King Diderik and the fight between the Lion and Dragon, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26802 |
| `borrow-translations-king-hacon-s-death-and-bran-and-the-blac` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | King Hacon's Death, and Bran and the Black Dog: Two Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26803 |
| `borrow-translations-klinger-faustus` | Friedrich Maximilian Klinger | Faustus | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 25468 |
| `borrow-translations-little-engel-a-ballad-with-a-series-of-e` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Little Engel: a ballad; with a series of epigrams from the Persian | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26805 |
| `borrow-translations-marsk-stig-a-ballad` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Marsk Stig: a ballad | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26831 |
| `borrow-translations-marsk-stig-s-daughters-and-other-songs-a` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Marsk Stig's Daughters, and Other Songs and Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26832 |
| `borrow-translations-mollie-charane-and-other-ballads` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Mollie Charane, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 27408 |
| `borrow-translations-niels-ebbesen-and-germand-gladenswayne-t` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Niels Ebbesen, and Germand Gladenswayne: Two Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26833 |
| `borrow-translations-oehlenschlager-the-gold-horns` | Adam Oehlenschläger | The Gold Horns | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 29124 |
| `borrow-translations-proud-signild-and-other-ballads` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Proud Signild, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 27396 |
| `borrow-translations-queen-berngerd-the-bard-and-the-dreams-a` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Queen Berngerd, The Bard and the Dreams, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 27474 |
| `borrow-translations-romantic-ballads-translated-from-the-dan` | Danish ballads and Oehlenschläger, Ewald and others | Romantic Ballads, Translated from the Danish; and Miscellaneous Pieces | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 2430 |
| `borrow-translations-the-brother-avenged-and-other-ballads` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | The Brother Avenged, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26790 |
| `borrow-translations-the-expedition-to-birting-s-land-and-oth` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | The Expedition to Birting's Land, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26793 |
| `borrow-translations-the-nightingale-the-valkyrie-and-raven-a` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | The Nightingale, the Valkyrie and Raven, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 26834 |
| `borrow-translations-the-return-of-the-dead-and-other-ballads` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | The Return of the Dead, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 27407 |
| `borrow-translations-the-story-of-tim` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | The Story of Tim | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 28770 |
| `borrow-translations-ulf-van-yern-and-other-ballads` | Anonymous (Danish and other ballads; from Borrow's manuscripts) | Ulf Van Yern, and Other Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 27405 |
| `borrow-translations-welsh-poems-and-ballads` | Welsh poets (Dafydd ap Gwilym and others) | Welsh Poems and Ballads | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 54851 |
| `borrow-translations-wynne-the-sleeping-bard-or-visions-of-the-worl` | Ellis Wynne | The Sleeping Bard; Or, Visions of the World, Death, and Hell | George Borrow | 1825-1915 (see the Gutenberg header) | have | PG 20634 |
| — | — | pg-13879: Ewald's The Death of Balder (Borrow, 1889): Ewald has his own shelf on lane D (ewald_shelf.json); left for its owner. | — | — | excluded | — |

## Adele Szold Seltzer (Hauptmann's Atlantis; Rashi; Sudermann; Maya the Bee)

Shelf: `pipeline/adele-seltzer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py adele-seltzer` · titles `python3 pipeline/split_shelf_titles.py adele-seltzer`.
Round 35 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `adele-seltzer-bonsels-the-adventures-of-maya-the-bee` | Waldemar Bonsels | The Adventures of Maya the Bee | Adele Szold Seltzer (verses by Arthur Guiterman) | 1922 | have | PG 22354 |
| `adele-seltzer-hauptmann-atlantis` | Gerhart Hauptmann | Atlantis | Adele Szold Seltzer | 1912 | have | PG 17241 |
| `adele-seltzer-liber-rashi` | Maurice Liber | Rashi | Adele Szold Seltzer | 1906 | have | PG 3165 |
| `adele-seltzer-magdeleine-marx-woman` | Magdeleine Marx | Woman | Adele Szold Seltzer | 1920 | have | PG 33943 |
| `adele-seltzer-sudermann-iolanthes-wedding` | Hermann Sudermann | Iolanthe's Wedding | Adele Szold Seltzer | 1918 | have | PG 34358 |

## Claud Field beyond Strindberg (Gogol; Al Ghazzali; Gunnarsson; Russian peasant tales)

Shelf: `pipeline/claud-field_shelf.json` · fetch `python3 pipeline/fetch_shelf.py claud-field` · titles `python3 pipeline/split_shelf_titles.py claud-field`.
Round 36 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `claud-field-ghazzali-the-confessions-of-al-ghazzali` | Al-Ghazali | The Confessions of Al Ghazzali | Claud Field | 1909-1920 (see the Gutenberg header) | have | PG 58977 |
| `claud-field-gogol-the-mantle-and-other-stories` | Nikolai Gogol | The Mantle, and Other Stories | Claud Field | 1909-1920 (see the Gutenberg header) | have | PG 36238 |
| `claud-field-gunnarsson-the-sworn-brothers` | Gunnar Gunnarsson | The Sworn Brothers: A Tale of the Early Days of Iceland | Claud Field (with William Emmé) | 1909-1920 (see the Gutenberg header) | have | PG 62123 |
| `claud-field-nemirovich-danchenko-peasant-tales-of-russia` | Vasilii Ivanovich Nemirovich-Danchenko | Peasant Tales of Russia | Claud Field | 1909-1920 (see the Gutenberg header) | have | PG 32755 |
| — | — | pg-44107: The Growth of a Soul is Strindberg: on strindberg-english_shelf.json. | — | — | excluded | — |

## Edwin Björkman beyond Strindberg (Schnitzler's Three Plays)

Shelf: `pipeline/edwin-bjorkman_shelf.json` · fetch `python3 pipeline/fetch_shelf.py edwin-bjorkman` · titles `python3 pipeline/split_shelf_titles.py edwin-bjorkman`.
Round 36 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `edwin-bjorkman-schnitzler-the-lonely-way-intermezzo-countess-mizzie` | Arthur Schnitzler | The Lonely Way—Intermezzo—Countess Mizzie Three Plays | Edwin Björkman | 1915 (see the Gutenberg header) | have | PG 29745 |
| — | — | pg-45375: Strindberg: on strindberg-english_shelf.json. | — | — | excluded | — |

## Ellie Schleussner beyond Strindberg (Lucka's Evolution of Love)

Shelf: `pipeline/ellie-schleussner_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ellie-schleussner` · titles `python3 pipeline/split_shelf_titles.py ellie-schleussner`.
Round 36 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ellie-schleussner-lucka-the-evolution-of-love` | Emil Lucka | The Evolution of Love | Ellie Schleussner | 1922 (see the Gutenberg header) | have | PG 17699 |

## Helen Zimmern beyond Nietzsche (Carmen Sylva's Pilgrim Sorrow)

Shelf: `pipeline/helen-zimmern_shelf.json` · fetch `python3 pipeline/fetch_shelf.py helen-zimmern` · titles `python3 pipeline/split_shelf_titles.py helen-zimmern`.
Round 36 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `helen-zimmern-sylva-pilgrim-sorrow-a-cycle-of-tales` | Carmen Sylva | Pilgrim Sorrow: A Cycle of Tales | Helen Zimmern | 1884 (see the Gutenberg header) | have | PG 46262 |
| — | — | pg-27799: De Amicis's Holland vol. 1: De Amicis has his own shelf (de-amicis_shelf.json, another lane); left for its owner. | — | — | excluded | — |

## Paul V. Cohn beyond Nietzsche (Bordeaux's Fort Vaux; Beyens)

Shelf: `pipeline/paul-cohn_shelf.json` · fetch `python3 pipeline/fetch_shelf.py paul-cohn` · titles `python3 pipeline/split_shelf_titles.py paul-cohn`.
Round 36 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `paul-cohn-beyens-germany-before-the-war` | Baron Eugène Beyens | Germany before the war | Paul V. Cohn | 1916-1917 (see the Gutenberg header) | have | PG 48572 |
| `paul-cohn-bordeaux-the-last-days-of-fort-vaux` | Henry Bordeaux | The Last Days of Fort Vaux, March 9-June 7, 1916 | Paul V. Cohn | 1916-1917 (see the Gutenberg header) | have | PG 48532 |

## Horace B. Samuel beyond Nietzsche (Stendhal's The Red and the Black; Schnitzler)

Shelf: `pipeline/horace-samuel_shelf.json` · fetch `python3 pipeline/fetch_shelf.py horace-samuel` · titles `python3 pipeline/split_shelf_titles.py horace-samuel`.
Round 36 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `horace-samuel-schnitzler-the-road-to-the-open` | Arthur Schnitzler | The Road to the Open | Horace B. Samuel | 1913-1923 (see the Gutenberg header) | have | PG 45895 |
| `horace-samuel-stendhal-the-red-and-the-black` | Stendhal | The Red and the Black: A Chronicle of 1830 | Horace B. Samuel | 1913-1923 (see the Gutenberg header) | have | PG 44747 |

## Gaston du C. de Vere: the complete Vasari, Lives of the Painters (10 vols, 1912-1915)

Shelf: `pipeline/gaston-de-vere_shelf.json` · fetch `python3 pipeline/fetch_shelf.py gaston-de-vere` · titles `python3 pipeline/split_shelf_titles.py gaston-de-vere`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `gaston-de-vere-vasari-lives-of-the-most-eminent-painters-sculp-vol-01` | Giorgio Vasari | Lives of the Most Eminent Painters Sculptors and Architects, Vol. 01 (of 10) Cimabue to Agnolo Gaddi | Gaston du C. de Vere | 1912-1915 (see the Gutenberg header) | have | PG 25326 |
| `gaston-de-vere-vasari-lives-of-the-most-eminent-painters-sculp-vol-02` | Giorgio Vasari | Lives of the Most Eminent Painters Sculptors and Architects, Vol. 02 (of 10) Berna to Michelozzo Michelozzi | Gaston du C. de Vere | 1912-1915 (see the Gutenberg header) | have | PG 25759 |
| `gaston-de-vere-vasari-lives-of-the-most-eminent-painters-sculp-vol-03` | Giorgio Vasari | Lives of the Most Eminent Painters Sculptors and Architects, Vol. 03 (of 10) Filarete and Simone to Mantegna | Gaston du C. de Vere | 1912-1915 (see the Gutenberg header) | have | PG 26860 |
| `gaston-de-vere-vasari-lives-of-the-most-eminent-painters-sculp-vol-04` | Giorgio Vasari | Lives of the Most Eminent Painters Sculptors and Architects, Vol. 04 (of 10) Filippino Lippi to Domenico Puligo | Gaston du C. de Vere | 1912-1915 (see the Gutenberg header) | have | PG 28420 |
| `gaston-de-vere-vasari-lives-of-the-most-eminent-painters-sculp-vol-05` | Giorgio Vasari | Lives of the Most Eminent Painters Sculptors and Architects, Vol. 05 (of 10) Andrea da Fiesole to Lorenzo Lotto | Gaston du C. de Vere | 1912-1915 (see the Gutenberg header) | have | PG 28421 |
| `gaston-de-vere-vasari-lives-of-the-most-eminent-painters-sculp-vol-06` | Giorgio Vasari | Lives of the most Eminent Painters Sculptors and Architects, Vol. 06 (of 10) Fra Giocondo to Niccolo Soggi | Gaston du C. de Vere | 1912-1915 (see the Gutenberg header) | have | PG 28422 |
| `gaston-de-vere-vasari-lives-of-the-most-eminent-painters-sculp-vol-07` | Giorgio Vasari | Lives of the most Eminent Painters Sculptors and Architects, Vol. 07 (of 10) Tribolo to Il Sodoma | Gaston du C. de Vere | 1912-1915 (see the Gutenberg header) | have | PG 31845 |
| `gaston-de-vere-vasari-lives-of-the-most-eminent-painters-sculp-vol-08` | Giorgio Vasari | Lives of the most Eminent Painters Sculptors and Architects, Vol. 08 (of 10) Bastiano to Taddeo Zucchero | Gaston du C. de Vere | 1912-1915 (see the Gutenberg header) | have | PG 31938 |
| `gaston-de-vere-vasari-lives-of-the-most-eminent-painters-sculp-vol-09` | Giorgio Vasari | Lives of the Most Eminent Painters, Sculptors and Architects, Vol. 09 (of 10) Michelagnolo to the Flemings | Gaston du C. de Vere | 1912-1915 (see the Gutenberg header) | have | PG 32362 |
| `gaston-de-vere-vasari-lives-of-the-most-eminent-painters-sculp-vol-10` | Giorgio Vasari | Lives of the most Eminent Painters Sculptors and Architects, Vol. 10 (of 10) Bronzino to Vasari, & General Index. | Gaston du C. de Vere | 1912-1915 (see the Gutenberg header) | have | PG 33203 |

## Alfred Sutro's Maeterlinck (Treasure of the Humble; Wisdom and Destiny; Life of the Bee; Buried Temple)

Shelf: `pipeline/sutro_shelf.json` · fetch `python3 pipeline/fetch_shelf.py sutro` · titles `python3 pipeline/split_shelf_titles.py sutro`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `sutro-maeterlinck-the-buried-temple` | Maurice Maeterlinck | The Buried Temple | Alfred Sutro | 1897-1902 (see the Gutenberg header) | have | PG 19711 |
| `sutro-maeterlinck-the-life-of-the-bee` | Maurice Maeterlinck | The Life of the Bee | Alfred Sutro | 1897-1902 (see the Gutenberg header) | have | PG 4511 |
| `sutro-maeterlinck-the-treasure-of-the-humble` | Maurice Maeterlinck | The Treasure of the Humble | Alfred Sutro | 1897-1902 (see the Gutenberg header) | have | PG 48217 |
| `sutro-maeterlinck-wisdom-and-destiny` | Maurice Maeterlinck | Wisdom and Destiny | Alfred Sutro | 1897-1902 (see the Gutenberg header) | have | PG 4349 |

## 'Monk' Lewis as translator (Zschokke's Bravo of Venice; Naubert's Feudal Tyrants)

Shelf: `pipeline/mg-lewis_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mg-lewis` · titles `python3 pipeline/split_shelf_titles.py mg-lewis`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mg-lewis-naubert-feudal-tyrants-or-the-counts-of-carlshei-vol-1` | Benedikte Naubert | Feudal tyrants; or, The Counts of Carlsheim and Sargans, volume 1 (of 4) | Matthew Gregory Lewis | 1805-1806 (see the Gutenberg header) | have | PG 69553 |
| `mg-lewis-naubert-feudal-tyrants-or-the-counts-of-carlshei-vol-2` | Benedikte Naubert | Feudal tyrants; or, The Counts of Carlsheim and Sargans, volume 2 (of 4) | Matthew Gregory Lewis | 1805-1806 (see the Gutenberg header) | have | PG 69623 |
| `mg-lewis-naubert-feudal-tyrants-or-the-counts-of-carlshei-vol-3` | Benedikte Naubert | Feudal tyrants; or, The Counts of Carlsheim and Sargans, volume 3 (of 4) | Matthew Gregory Lewis | 1805-1806 (see the Gutenberg header) | have | PG 69624 |
| `mg-lewis-naubert-feudal-tyrants-or-the-counts-of-carlshei-vol-4` | Benedikte Naubert | Feudal tyrants; or, The Counts of Carlsheim and Sargans, volume 4 (of 4) | Matthew Gregory Lewis | 1805-1806 (see the Gutenberg header) | have | PG 69625 |
| `mg-lewis-zschokke-the-bravo-of-venice-a-romance` | Heinrich Zschokke | The Bravo of Venice: A Romance | Matthew Gregory Lewis | 1805-1806 (see the Gutenberg header) | have | PG 2706 |

## A. B. Lindsay: the Russo-Japanese War from the Russian (Semenov; Nozhin; Kuropatkin)

Shelf: `pipeline/ab-lindsay_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ab-lindsay` · titles `python3 pipeline/split_shelf_titles.py ab-lindsay`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ab-lindsay-kuropatkin-the-russian-army-and-the-japanese-war-vol-1` | A. N. Kuropatkin | The Russian Army and the Japanese War, Vol. 1 (of 2) Being Historical and Critical Comments on the Military Policy and Power of Russia and on the Campaign in the Far East | A. B. Lindsay | 1906-1909 (see the Gutenberg header) | have | PG 58256 |
| `ab-lindsay-kuropatkin-the-russian-army-and-the-japanese-war-vol-2` | A. N. Kuropatkin | The Russian Army and the Japanese War, Vol. 2 (of 2) Being Historical and Critical Comments on the Military Policy and Power of Russia and on the Campaign in the Far East | A. B. Lindsay | 1906-1909 (see the Gutenberg header) | have | PG 60975 |
| `ab-lindsay-nozhin-the-truth-about-port-arthur` | E. K. Nozhin | The Truth About Port Arthur | A. B. Lindsay | 1906-1909 (see the Gutenberg header) | have | PG 59972 |
| `ab-lindsay-semenov-the-battle-of-tsu-shima-between-the-japa` | Vladimir Semenov | The Battle of Tsu-shima between the Japanese and Russian fleets, fought on 27th May 1905 | A. B. Lindsay | 1906-1909 (see the Gutenberg header) | have | PG 57324 |

## Thomas Rymer Jones: Brehm's Cassell's Book of Birds (4 vols)

Shelf: `pipeline/rymer-jones_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rymer-jones` · titles `python3 pipeline/split_shelf_titles.py rymer-jones`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rymer-jones-brehm-cassell-s-book-of-birds-vol-1` | Alfred Edmund Brehm | Cassell's book of birds; vol. 1 | Thomas Rymer Jones | 1869-1873 (see the Gutenberg header) | have | PG 48675 |
| `rymer-jones-brehm-cassell-s-book-of-birds-vol-2` | Alfred Edmund Brehm | Cassell's book of birds; vol. 2 | Thomas Rymer Jones | 1869-1873 (see the Gutenberg header) | have | PG 57450 |
| `rymer-jones-brehm-cassell-s-book-of-birds-vol-3` | Alfred Edmund Brehm | Cassell's book of birds; vol. 3 | Thomas Rymer Jones | 1869-1873 (see the Gutenberg header) | have | PG 60254 |
| `rymer-jones-brehm-cassell-s-book-of-birds-vol-4` | Alfred Edmund Brehm | Cassell's book of birds; vol. 4 | Thomas Rymer Jones | 1869-1873 (see the Gutenberg header) | have | PG 68801 |

## George Hayward: Bichat's General Anatomy (3 vols) and Physiological Researches

Shelf: `pipeline/hayward-bichat_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hayward-bichat` · titles `python3 pipeline/split_shelf_titles.py hayward-bichat`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hayward-bichat-bichat-general-anatomy-applied-to-physiology-an-vol-1` | Xavier Bichat | General Anatomy, Applied to Physiology and Medicine, Vol. 1 (of 3) | George Hayward | 1822-1827 (see the Gutenberg header) | have | PG 56118 |
| `hayward-bichat-bichat-general-anatomy-applied-to-physiology-an-vol-2` | Xavier Bichat | General Anatomy, Applied to Physiology and Medicine, Vol. 2 (of 3) | George Hayward | 1822-1827 (see the Gutenberg header) | have | PG 56147 |
| `hayward-bichat-bichat-general-anatomy-applied-to-physiology-an-vol-3` | Xavier Bichat | General Anatomy, Applied to Physiology and Medicine, Vol. 3 (of 3) | George Hayward | 1822-1827 (see the Gutenberg header) | have | PG 56328 |
| `hayward-bichat-bichat-physiological-researches-on-life-and-dea` | Xavier Bichat | Physiological Researches on Life and Death | George Hayward (with F. [Translator] Gold) | 1822-1827 (see the Gutenberg header) | have | PG 56440 |

## Johann Reinhold Forster: Kalm's Travels into North America; Bougainville's Voyage

Shelf: `pipeline/jr-forster_shelf.json` · fetch `python3 pipeline/fetch_shelf.py jr-forster` · titles `python3 pipeline/split_shelf_titles.py jr-forster`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `jr-forster-bougainville-a-voyage-round-the-world` | Louis-Antoine de Bougainville | A voyage round the world | Johann Reinhold Forster | 1770-1772 (see the Gutenberg header) | have | PG 73429 |
| `jr-forster-kalm-travels-into-north-america-volume-1-of-3` | Pehr Kalm | Travels into North America, Volume 1 (of 3) | Johann Reinhold Forster | 1770-1772 (see the Gutenberg header) | have | PG 71849 |
| `jr-forster-kalm-travels-into-north-america-volume-2-of-3` | Pehr Kalm | Travels into North America, Volume 2 (of 3) | Johann Reinhold Forster | 1770-1772 (see the Gutenberg header) | have | PG 72103 |
| `jr-forster-kalm-travels-into-north-america-volume-3-of-3` | Pehr Kalm | Travels into North America, Volume 3 (of 3) | Johann Reinhold Forster | 1770-1772 (see the Gutenberg header) | have | PG 72737 |

## John Brett: Feijoo's Essays, or Discourses (4 vols)

Shelf: `pipeline/brett-feijoo_shelf.json` · fetch `python3 pipeline/fetch_shelf.py brett-feijoo` · titles `python3 pipeline/split_shelf_titles.py brett-feijoo`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `brett-feijoo-feijoo-essays-or-discourses-vol-1-of-4` | Benito Jerónimo Feijoo | Essays, or discourses, vol. 1 (of 4) | John Brett | 1777-1780 (see the Gutenberg header) | have | PG 71277 |
| `brett-feijoo-feijoo-essays-or-discourses-vol-2-of-4` | Benito Jerónimo Feijoo | Essays, or discourses, vol. 2 (of 4) | John Brett | 1777-1780 (see the Gutenberg header) | have | PG 71278 |
| `brett-feijoo-feijoo-essays-or-discourses-vol-3-of-4` | Benito Jerónimo Feijoo | Essays, or discourses, vol. 3 (of 4) | John Brett | 1777-1780 (see the Gutenberg header) | have | PG 76228 |
| `brett-feijoo-feijoo-essays-or-discourses-vol-4-of-4` | Benito Jerónimo Feijoo | Essays, or discourses, vol. 4 (of 4) | John Brett | 1777-1780 (see the Gutenberg header) | have | PG 76229 |

## Frederic Whyte (Filon's The English Stage; Schillings's In Wildest Africa)

Shelf: `pipeline/frederic-whyte_shelf.json` · fetch `python3 pipeline/fetch_shelf.py frederic-whyte` · titles `python3 pipeline/split_shelf_titles.py frederic-whyte`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `frederic-whyte-filon-the-english-stage-being-an-account-of-th` | Augustin Filon | The English Stage: Being an Account of the Victorian Drama | Frederic Whyte | 1897-1907 (see the Gutenberg header) | have | PG 36590 |
| `frederic-whyte-schillings-in-wildest-africa-vol-1` | C. G. Schillings | In Wildest Africa, Vol. 1 | Frederic Whyte | 1897-1907 (see the Gutenberg header) | have | PG 54922 |
| `frederic-whyte-schillings-in-wildest-africa-vol-2` | C. G. Schillings | In Wildest Africa, Vol. 2 | Frederic Whyte | 1897-1907 (see the Gutenberg header) | have | PG 54923 |

## Emilie Poulsson's Zwilgmeyer (Inger Johanne; Johnny Blossom)

Shelf: `pipeline/poulsson-zwilgmeyer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py poulsson-zwilgmeyer` · titles `python3 pipeline/split_shelf_titles.py poulsson-zwilgmeyer`.
Round 37 (2026-10-10), vetoable. Lane D's poulsson shelf holds her Top-of-the-World Stories. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `poulsson-zwilgmeyer-zwilgmeyer-inger-johanne-s-lively-doings` | Dikken Zwilgmeyer | Inger Johanne's lively doings | Emilie Poulsson | 1912-1920 (see the Gutenberg header) | have | PG 70274 |
| `poulsson-zwilgmeyer-zwilgmeyer-johnny-blossom` | Dikken Zwilgmeyer | Johnny Blossom | Emilie Poulsson | 1912-1920 (see the Gutenberg header) | have | PG 64005 |
| `poulsson-zwilgmeyer-zwilgmeyer-what-happened-to-inger-johanne-as-told-b` | Dikken Zwilgmeyer | What happened to Inger Johanne, as told by herself | Emilie Poulsson | 1912-1920 (see the Gutenberg header) | have | PG 32502 |

## Elizabeth Gilbert Martin: Imbert de Saint-Amand's French court histories

Shelf: `pipeline/eg-martin_shelf.json` · fetch `python3 pipeline/fetch_shelf.py eg-martin` · titles `python3 pipeline/split_shelf_titles.py eg-martin`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `eg-martin-saint-amand-last-years-of-louis-xv` | Imbert de Saint-Amand | Last years of Louis XV | Elizabeth Gilbert Martin | 1891-1893 (see the Gutenberg header) | have | PG 79712 |
| `eg-martin-saint-amand-marie-antoinette-and-the-downfall-of-roy` | Imbert de Saint-Amand | Marie Antoinette and the Downfall of Royalty | Elizabeth Gilbert Martin | 1891-1893 (see the Gutenberg header) | have | PG 32408 |
| `eg-martin-saint-amand-the-court-of-louis-xv` | Imbert de Saint-Amand | The court of Louis XV | Elizabeth Gilbert Martin | 1891-1893 (see the Gutenberg header) | have | PG 73192 |

## Elizabeth Lee (Jusserand; Maspero; Rosegger)

Shelf: `pipeline/elizabeth-lee_shelf.json` · fetch `python3 pipeline/fetch_shelf.py elizabeth-lee` · titles `python3 pipeline/split_shelf_titles.py elizabeth-lee`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `elizabeth-lee-jusserand-the-english-novel-in-the-time-of-shakesp` | J. J. Jusserand | The English Novel in the Time of Shakespeare | Elizabeth Lee | 1890-1913 (see the Gutenberg header) | have | PG 31151 |
| `elizabeth-lee-maspero-egyptian-art-studies` | Gaston Maspero | Egyptian Art: Studies | Elizabeth Lee | 1890-1913 (see the Gutenberg header) | have | PG 64387 |
| `elizabeth-lee-rosegger-i-n-r-i-a-prisoner-s-story-of-the-cross` | Peter Rosegger | I.N.R.I.: A prisoner's Story of the Cross | Elizabeth Lee | 1890-1913 (see the Gutenberg header) | have | PG 17011 |

## William Johnston (Beckmann's History of Inventions; Paulinus's Voyage to the East Indies)

Shelf: `pipeline/w-johnston_shelf.json` · fetch `python3 pipeline/fetch_shelf.py w-johnston` · titles `python3 pipeline/split_shelf_titles.py w-johnston`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `w-johnston-beckmann-a-history-of-inventions-discoveries-and-vol-1` | Johann Beckmann | A History of Inventions, Discoveries, and Origins, Volume 1 (of 2) | William Johnston | 1797-1846 (see the Gutenberg header) | have | PG 48151 |
| `w-johnston-beckmann-a-history-of-inventions-discoveries-and-vol-2` | Johann Beckmann | A History of Inventions, Discoveries, and Origins, Volume 2 (of 2) | William Johnston | 1797-1846 (see the Gutenberg header) | have | PG 48152 |
| `w-johnston-paulinus-voyage-to-the-east-indies` | Paulinus a S. Bartholomaeo | Voyage to the East Indies | William Johnston | 1797-1846 (see the Gutenberg header) | have | PG 76461 |

## Louise Seymour Houghton (Sabatier's St Francis; Bordeaux; Boylesve)

Shelf: `pipeline/houghton-translations_shelf.json` · fetch `python3 pipeline/fetch_shelf.py houghton-translations` · titles `python3 pipeline/split_shelf_titles.py houghton-translations`.
Round 37 (2026-10-10), vetoable. Lane D's louise-houghton shelf holds her Russian Grandmother's Wonder Tales. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `houghton-translations-bordeaux-the-house` | Henry Bordeaux | The house | Louise Seymour Houghton | 1894-1918 (see the Gutenberg header) | have | PG 72388 |
| `houghton-translations-boylesve-you-no-longer-count-tu-n-es-plus-rien` | René Boylesve | You no longer count (Tu n'es plus rien!) | Louise Seymour Houghton | 1894-1918 (see the Gutenberg header) | have | PG 68557 |
| `houghton-translations-sabatier-life-of-st-francis-of-assisi` | Paul Sabatier | Life of St. Francis of Assisi | Louise Seymour Houghton | 1894-1918 (see the Gutenberg header) | have | PG 18787 |

## Helena Frank (Yiddish Tales; Peretz; Rosenfeld)

Shelf: `pipeline/helena-frank_shelf.json` · fetch `python3 pipeline/fetch_shelf.py helena-frank` · titles `python3 pipeline/split_shelf_titles.py helena-frank`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `helena-frank-peretz-stories-and-pictures` | Isaac Loeb Peretz | Stories and Pictures | Helena Frank | 1906-1914 (see the Gutenberg header) | have | PG 37242 |
| `helena-frank-rosenfeld-songs-of-labor-and-other-poems` | Morris Rosenfeld | Songs of Labor, and Other Poems | Helena Frank (with Rose Pastor Stokes) | 1906-1914 (see the Gutenberg header) | have | PG 6859 |
| `helena-frank-yiddish-tales` | various authors (anthology) | Yiddish Tales | Helena Frank | 1906-1914 (see the Gutenberg header) | have | PG 33707 |

## Alexander Ewing (Hoffmann's Serapion Brethren; Jean Paul)

Shelf: `pipeline/alexander-ewing_shelf.json` · fetch `python3 pipeline/fetch_shelf.py alexander-ewing` · titles `python3 pipeline/split_shelf_titles.py alexander-ewing`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `alexander-ewing-hoffmann-the-serapion-brethren-vol-i` | E. T. A. Hoffmann | The Serapion Brethren, Vol. I. | Alexander Ewing | 1877-1892 (see the Gutenberg header) | have | PG 31820 |
| `alexander-ewing-hoffmann-the-serapion-brethren-vol-ii` | E. T. A. Hoffmann | The Serapion Brethren, Vol. II | Alexander Ewing | 1877-1892 (see the Gutenberg header) | have | PG 31668 |
| `alexander-ewing-jean-paul-flower-fruit-and-thorn-pieces-or-the-wed` | Jean Paul | Flower, Fruit, and Thorn Pieces; or, the Wedded Life, Death, and Marriage of Firmian Stanislaus Siebenkaes, Parish Advocate in the Burgh of Kuhschnappel. | Alexander Ewing | 1877-1892 (see the Gutenberg header) | have | PG 36164 |

## Samuel A. Eliot Jr.'s Wedekind

Shelf: `pipeline/sa-eliot_shelf.json` · fetch `python3 pipeline/fetch_shelf.py sa-eliot` · titles `python3 pipeline/split_shelf_titles.py sa-eliot`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `sa-eliot-wedekind-erdgeist-earth-spirit-a-tragedy-in-four` | Frank Wedekind | Erdgeist (Earth-Spirit): A Tragedy in Four Acts | Samuel A. Eliot Jr. | 1914-1923 (see the Gutenberg header) | have | PG 29682 |
| `sa-eliot-wedekind-pandora-s-box-a-tragedy-in-three-acts` | Frank Wedekind | Pandora's Box: A Tragedy in Three Acts | Samuel A. Eliot Jr. | 1914-1923 (see the Gutenberg header) | have | PG 33415 |
| `sa-eliot-wedekind-tragedies-of-sex` | Frank Wedekind | Tragedies of sex | Samuel A. Eliot Jr. | 1914-1923 (see the Gutenberg header) | have | PG 76872 |

## Frances Douglas's Blasco Ibáñez

Shelf: `pipeline/frances-douglas_shelf.json` · fetch `python3 pipeline/fetch_shelf.py frances-douglas` · titles `python3 pipeline/split_shelf_titles.py frances-douglas`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `frances-douglas-ibanez-sonnica` | Vicente Blasco Ibáñez | Sónnica | Frances Douglas | 1911-1919 (see the Gutenberg header) | have | PG 31821 |
| `frances-douglas-ibanez-the-blood-of-the-arena` | Vicente Blasco Ibáñez | The Blood of the Arena | Frances Douglas | 1911-1919 (see the Gutenberg header) | have | PG 33799 |
| `frances-douglas-ibanez-the-dead-command-from-the-spanish-los-mu` | Vicente Blasco Ibáñez | The Dead Command From the Spanish Los Muertos Mandan | Frances Douglas | 1911-1919 (see the Gutenberg header) | have | PG 27068 |

## Henry L. Brose: relativity from the German (Moszkowski; Weyl and Freundlich pending)

Shelf: `pipeline/brose_shelf.json` · fetch `python3 pipeline/fetch_shelf.py brose` · titles `python3 pipeline/split_shelf_titles.py brose`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `brose-moszkowski-einstein-the-searcher` | Alexander Moszkowski | Einstein, the searcher | Henry L. Brose | 1920-1922 (see the Gutenberg header) | have | PG 70678 |
| `pg-43006` | — | Weyl's Space-Time-Matter: Gutenberg publishes this physics book only as PDF/LaTeX, with no plain-text file to fetch. Left for a later pass that finds a period scan on the Internet Archive. | — | — | pending | — |
| `pg-70793` | — | Freundlich's The Foundations of Einstein's Theory of Gravitation: Gutenberg has only an HTML edition, no plain-text file. Left for a later pass that finds a period scan on the Internet Archive. | — | — | pending | — |

## Mary Wilson's Heyse tales

Shelf: `pipeline/mary-wilson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mary-wilson` · titles `python3 pipeline/split_shelf_titles.py mary-wilson`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mary-wilson-heyse-l-arrabiata-and-other-tales` | Paul Heyse | L'Arrabiata and Other Tales | Mary Wilson | 1867-1870 (see the Gutenberg header) | have | PG 33583 |
| `mary-wilson-heyse-the-dead-lake-and-other-tales` | Paul Heyse | The Dead Lake, and Other Tales | Mary Wilson | 1867-1870 (see the Gutenberg header) | have | PG 33916 |

## Robert Willis's Harvey

Shelf: `pipeline/robert-willis_shelf.json` · fetch `python3 pipeline/fetch_shelf.py robert-willis` · titles `python3 pipeline/split_shelf_titles.py robert-willis`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `robert-willis-harvey-an-anatomical-disquisition-on-the-motion` | William Harvey | An anatomical disquisition on the motion of the heart & blood in animals | Robert Willis | 1847 (see the Gutenberg header) | have | PG 67065 |
| `robert-willis-harvey-the-works-of-william-harvey-m-d-translat` | William Harvey | The Works of William Harvey M.D. Translated from the Latin with a life of the author | Robert Willis | 1847 (see the Gutenberg header) | have | PG 58857 |

## L. Williams: Bruno's Heroic Enthusiasts

Shelf: `pipeline/l-williams_shelf.json` · fetch `python3 pipeline/fetch_shelf.py l-williams` · titles `python3 pipeline/split_shelf_titles.py l-williams`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `l-williams-bruno-the-heroic-enthusiasts-part-1` | Giordano Bruno | The Heroic Enthusiasts (Gli Eroici Furori) Part the First An Ethical Poem | L. Williams | 1887-1889 (see the Gutenberg header) | have | PG 19817 |
| `l-williams-bruno-the-heroic-enthusiasts-part-2` | Giordano Bruno | The Heroic Enthusiasts (Gli Eroici Furori) Part the Second An Ethical Poem | L. Williams | 1887-1889 (see the Gutenberg header) | have | PG 19833 |

## Alice Werner (Weule's Native Life in East Africa; The Humour of Holland)

Shelf: `pipeline/alice-werner_shelf.json` · fetch `python3 pipeline/fetch_shelf.py alice-werner` · titles `python3 pipeline/split_shelf_titles.py alice-werner`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `alice-werner-dircks-the-humour-of-holland` | various authors (anthology, ed. W. H. Dircks) | The humour of Holland | Alice Werner | 1894-1909 (see the Gutenberg header) | have | PG 64761 |
| `alice-werner-weule-native-life-in-east-africa` | Karl Weule | Native life in East Africa | Alice Werner | 1894-1909 (see the Gutenberg header) | have | PG 71496 |

## Herbert Trench's Merezhkovsky

Shelf: `pipeline/herbert-trench_shelf.json` · fetch `python3 pipeline/fetch_shelf.py herbert-trench` · titles `python3 pipeline/split_shelf_titles.py herbert-trench`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `herbert-trench-merezhkovsky-the-death-of-the-gods-christ-and-antichr` | Dmitry Sergeyevich Merezhkovsky | The Death of the Gods (Christ and Antichrist, 1 of 3) | Herbert Trench | 1901-1902 (see the Gutenberg header) | have | PG 46492 |
| `herbert-trench-merezhkovsky-the-romance-of-leonardo-da-vinci-the-for` | Dmitry Sergeyevich Merezhkovsky | The Romance of Leonardo da Vinci, the Forerunner | Herbert Trench | 1901-1902 (see the Gutenberg header) | have | PG 47902 |

## Frederic Taber Cooper (French painter monographs; Montessori)

Shelf: `pipeline/ft-cooper_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ft-cooper` · titles `python3 pipeline/split_shelf_titles.py ft-cooper`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ft-cooper-barbusse-meissonier` | Henri Barbusse | Meissonier | Frederic Taber Cooper | 1912-1914 (see the Gutenberg header) | have | PG 43085 |
| `ft-cooper-beaume-fromentin` | Georges Beaume | Fromentin | Frederic Taber Cooper | 1912-1914 (see the Gutenberg header) | have | PG 42838 |
| `ft-cooper-crastre-bastien-lepage` | François Crastre | Bastien Lepage | Frederic Taber Cooper | 1912-1914 (see the Gutenberg header) | have | PG 36533 |
| `ft-cooper-crastre-goya` | François Crastre | Goya | Frederic Taber Cooper | 1912-1914 (see the Gutenberg header) | have | PG 42425 |
| `ft-cooper-crastre-henner` | François Crastre | Henner | Frederic Taber Cooper | 1912-1914 (see the Gutenberg header) | have | PG 47443 |
| `ft-cooper-crastre-rosa-bonheur` | François Crastre | Rosa Bonheur | Frederic Taber Cooper | 1912-1914 (see the Gutenberg header) | have | PG 41939 |
| `ft-cooper-crastre-veronese` | François Crastre | Veronese | Frederic Taber Cooper | 1912-1914 (see the Gutenberg header) | have | PG 41974 |
| `ft-cooper-keim-gerome` | Albert Keim | Gérôme | Frederic Taber Cooper | 1912-1914 (see the Gutenberg header) | have | PG 44340 |
| `ft-cooper-keim-honore-de-balzac` | Albert Keim and Louis Lumet | Honoré de Balzac | Frederic Taber Cooper | 1912-1914 (see the Gutenberg header) | have | PG 3625 |
| `ft-cooper-montessori-pedagogical-anthropology` | Maria Montessori | Pedagogical Anthropology | Frederic Taber Cooper | 1912-1914 (see the Gutenberg header) | have | PG 46643 |

## Ruth Helen Davis (Gautier and Loti; Bordeaux)

Shelf: `pipeline/ruth-davis_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ruth-davis` · titles `python3 pipeline/split_shelf_titles.py ruth-davis`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ruth-davis-bordeaux-the-awakening` | Henry Bordeaux | The awakening | Ruth Helen Davis | 1912-1914 (see the Gutenberg header) | have | PG 70440 |
| `ruth-davis-bordeaux-the-fear-of-living` | Henry Bordeaux | The fear of living | Ruth Helen Davis | 1912-1914 (see the Gutenberg header) | have | PG 73031 |
| `ruth-davis-bordeaux-the-woollen-dress` | Henry Bordeaux | The woollen dress | Ruth Helen Davis | 1912-1914 (see the Gutenberg header) | have | PG 71410 |
| `ruth-davis-gautier-the-daughter-of-heaven` | Judith Gautier and Pierre Loti | The Daughter of Heaven | Ruth Helen Davis | 1912-1914 (see the Gutenberg header) | have | PG 47218 |

## D. B. Stewart: Anatole France's Seven Wives of Bluebeard (3 files)

Shelf: `pipeline/db-stewart_shelf.json` · fetch `python3 pipeline/fetch_shelf.py db-stewart` · titles `python3 pipeline/split_shelf_titles.py db-stewart`.
Round 37 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `db-stewart-france-the-miracle-of-the-great-st-nicolas` | Anatole France | The Miracle of the Great St. Nicolas | D. B. Stewart | 1920 (see the Gutenberg header) | have | PG 25410 |
| `db-stewart-france-the-seven-wives-of-bluebeard` | Anatole France | The Seven Wives of Bluebeard | D. B. Stewart | 1920 (see the Gutenberg header) | have | PG 25411 |
| `db-stewart-france-the-story-of-the-duchess-of-cicogne-and` | Anatole France | The Story of the Duchess of Cicogne and of Monsieur de Boulingrin | D. B. Stewart | 1920 (see the Gutenberg header) | have | PG 25409 |

## Charles R. Murphy's Verhaeren (the three books of love poems)

Shelf: `pipeline/cr-murphy_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cr-murphy` · titles `python3 pipeline/split_shelf_titles.py cr-murphy`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cr-murphy-verhaeren-afternoon` | Emile Verhaeren | Afternoon | Charles R. Murphy | 1916-1917 (see the Gutenberg header) | have | PG 45466 |
| `cr-murphy-verhaeren-the-evening-hours` | Emile Verhaeren | The Evening Hours | Charles R. Murphy | 1916-1917 (see the Gutenberg header) | have | PG 45467 |
| `cr-murphy-verhaeren-the-sunlit-hours` | Emile Verhaeren | The Sunlit Hours | Charles R. Murphy | 1916-1917 (see the Gutenberg header) | have | PG 45465 |

## John Henry Brady: Alemán's Guzman d'Alfarache via Le Sage (3 vols)

Shelf: `pipeline/brady-guzman_shelf.json` · fetch `python3 pipeline/fetch_shelf.py brady-guzman` · titles `python3 pipeline/split_shelf_titles.py brady-guzman`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `brady-guzman-aleman-the-life-and-adventures-of-guzman-d-alfa-vol-1` | Mateo Alemán | The Life and Adventures of Guzman D'Alfarache, or the Spanish Rogue, vol. 1/3 | John Henry Brady (with Alain René Le Sage) | 1821 (see the Gutenberg header) | have | PG 52806 |
| `brady-guzman-aleman-the-life-and-adventures-of-guzman-d-alfa-vol-2` | Mateo Alemán | The Life and Adventures of Guzman D'Alfarache, or the Spanish Rogue, vol. 2/3 | John Henry Brady (with Alain René Le Sage) | 1821 (see the Gutenberg header) | have | PG 52938 |
| `brady-guzman-aleman-the-life-and-adventures-of-guzman-d-alfa-vol-3` | Mateo Alemán | The Life and Adventures of Guzman D'Alfarache, or the Spanish Rogue, vol. 3/3 | John Henry Brady (with Alain René Le Sage) | 1821 (see the Gutenberg header) | have | PG 53081 |

## A. J. W. Morrison for Bohn (Schiller's histories; Schlegel; Goethe's Swiss letters)

Shelf: `pipeline/ajw-morrison_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ajw-morrison` · titles `python3 pipeline/split_shelf_titles.py ajw-morrison`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ajw-morrison-goethe-letters-from-switzerland-and-travels-in` | Johann Wolfgang von Goethe | Letters from Switzerland and Travels in Italy | A. J. W. Morrison | 1846-1849 (see the Gutenberg header) | have | PG 53205 |
| `ajw-morrison-schiller-history-of-the-revolt-of-the-netherlands` | Friedrich Schiller | History of the Revolt of the Netherlands — Complete | A. J. W. Morrison (with Edward Backhouse Eastwick) | 1846-1849 (see the Gutenberg header) | have | PG 6780 |
| `ajw-morrison-schiller-the-history-of-the-thirty-years-war` | Friedrich Schiller | The History of the Thirty Years' War | A. J. W. Morrison | 1846-1849 (see the Gutenberg header) | have | PG 566 |
| `ajw-morrison-schlegel-the-philosophy-of-life-and-philosophy-of` | Friedrich von Schlegel | The philosophy of life, and philosophy of language, in a course of lectures | A. J. W. Morrison | 1846-1849 (see the Gutenberg header) | have | PG 43544 |
| — | — | pg-6775: Another Gutenberg file of The History of the Thirty Years' War (566): duplicate, not shelved. | — | — | excluded | — |

## M. P. Willcocks's Anatole France (Contemporary History)

Shelf: `pipeline/willcocks_shelf.json` · fetch `python3 pipeline/fetch_shelf.py willcocks` · titles `python3 pipeline/split_shelf_titles.py willcocks`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `willcocks-france-the-elm-tree-on-the-mall` | Anatole France | The Elm-tree on the Mall | M. P. Willcocks | 1910 (see the Gutenberg header) | have | PG 49924 |
| `willcocks-france-the-wicker-work-woman-a-chronicle-of-our` | Anatole France | The Wicker Work Woman: A Chronicle of Our Own Times | M. P. Willcocks | 1910 (see the Gutenberg header) | have | PG 50286 |

## Ellen Waugh (Jókai; Ebner-Eschenbach)

Shelf: `pipeline/ellen-waugh_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ellen-waugh` · titles `python3 pipeline/split_shelf_titles.py ellen-waugh`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ellen-waugh-ebner-eschenbach-the-two-countesses` | Marie von Ebner-Eschenbach | The two countesses | Ellen Waugh | 1893-1897 (see the Gutenberg header) | have | PG 76750 |
| `ellen-waugh-jokai-the-green-book-or-freedom-under-the-snow` | Mór Jókai | The Green Book; Or, Freedom Under the Snow: A Novel | Ellen Waugh | 1893-1897 (see the Gutenberg header) | have | PG 34503 |

## Margaret P. Waterman (Heimburg; Archag)

Shelf: `pipeline/mp-waterman_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mp-waterman` · titles `python3 pipeline/split_shelf_titles.py mp-waterman`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mp-waterman-heimburg-a-sister-s-love-a-novel` | W. Heimburg | A Sister's Love: A Novel | Margaret P. Waterman | 1890-1898 (see the Gutenberg header) | have | PG 33958 |
| `mp-waterman-schnapps-archag-the-little-armenian` | Charles H. Schnapps | Archag, the Little Armenian | Margaret P. Waterman | 1890-1898 (see the Gutenberg header) | have | PG 52638 |

## Charles Troilius: Linnaeus's Tour in Lapland (2 vols)

Shelf: `pipeline/troilius_shelf.json` · fetch `python3 pipeline/fetch_shelf.py troilius` · titles `python3 pipeline/split_shelf_titles.py troilius`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `troilius-linne-lachesis-lapponica-or-a-tour-in-lapland-vol-1` | Carl Linnaeus | Lachesis Lapponica; Or, A Tour in Lapland, Volume 1 | Charles Troilius | 1811 (see the Gutenberg header) | have | PG 34779 |
| `troilius-linne-lachesis-lapponica-or-a-tour-in-lapland-vol-2` | Carl Linnaeus | Lachesis Lapponica; Or, A Tour in Lapland, Volume 2 | Charles Troilius | 1811 (see the Gutenberg header) | have | PG 36059 |

## Minna Caroline Smith (Palacio Valdés; Pérez Galdós)

Shelf: `pipeline/minna-smith_shelf.json` · fetch `python3 pipeline/fetch_shelf.py minna-smith` · titles `python3 pipeline/split_shelf_titles.py minna-smith`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `minna-smith-galdos-saragossa-a-story-of-spanish-valor` | Benito Pérez Galdós | Saragossa: A Story of Spanish Valor | Minna Caroline Smith | 1899-1900 (see the Gutenberg header) | have | PG 47769 |
| `minna-smith-valdes-the-joy-of-captain-ribot` | Armando Palacio Valdés | The Joy of Captain Ribot | Minna Caroline Smith | 1899-1900 (see the Gutenberg header) | have | PG 38293 |

## Leon Simon (Ahad Ha'am; Einstein's About Zionism, 1930)

Shelf: `pipeline/leon-simon_shelf.json` · fetch `python3 pipeline/fetch_shelf.py leon-simon` · titles `python3 pipeline/split_shelf_titles.py leon-simon`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `leon-simon-ahad-ha-am-ten-essays-on-zionism-and-judaism` | Ahad Ha'am | Ten Essays on Zionism and Judaism | Leon Simon | 1922-1930 (see the Gutenberg header) | have | PG 67667 |
| `leon-simon-einstein-about-zionism` | Albert Einstein | About Zionism | Leon Simon | 1922-1930 (see the Gutenberg header) | have | PG 79647 |

## Jane Minot Sedgwick's George Sand

Shelf: `pipeline/sedgwick-sand_shelf.json` · fetch `python3 pipeline/fetch_shelf.py sedgwick-sand` · titles `python3 pipeline/split_shelf_titles.py sedgwick-sand`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `sedgwick-sand-francois-the-waif` | George Sand | François the waif | Jane Minot Sedgwick | 1894 (see the Gutenberg header) | have | PG 69153 |
| `sedgwick-sand-the-devil-s-pool` | George Sand | The Devil's Pool | Jane Minot Sedgwick (with Ellery Sedgwick) | 1894 (see the Gutenberg header) | have | PG 21993 |

## Fayette Robinson (Brillat-Savarin's Physiology of Taste; Sand)

Shelf: `pipeline/fayette-robinson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fayette-robinson` · titles `python3 pipeline/split_shelf_titles.py fayette-robinson`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fayette-robinson-brillat-savarin-the-physiology-of-taste-or-transcendenta` | Jean Anthelme Brillat-Savarin | The Physiology of Taste; Or, Transcendental Gastronomy | Fayette Robinson | 1851-1854 (see the Gutenberg header) | have | PG 5434 |
| `fayette-robinson-sand-the-countess-of-rudolstadt-a-sequel-to-c` | George Sand | The Countess of Rudolstadt A Sequel to "Consuelo" | Fayette Robinson | 1851-1854 (see the Gutenberg header) | have | PG 62338 |

## James Burton Robertson: Schlegel's Philosophy of History (2 vols)

Shelf: `pipeline/jb-robertson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py jb-robertson` · titles `python3 pipeline/split_shelf_titles.py jb-robertson`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `jb-robertson-schlegel-the-philosophy-of-history-vol-1-of-2` | Friedrich von Schlegel | The Philosophy of History, Vol. 1 of 2 | James Burton Robertson | 1835 (see the Gutenberg header) | have | PG 38365 |
| `jb-robertson-schlegel-the-philosophy-of-history-vol-2-of-2` | Friedrich von Schlegel | The Philosophy of History, Vol. 2 of 2 | James Burton Robertson | 1835 (see the Gutenberg header) | have | PG 48275 |

## Edwin Gile Rich (Saint-Saëns; Lafond)

Shelf: `pipeline/eg-rich_shelf.json` · fetch `python3 pipeline/fetch_shelf.py eg-rich` · titles `python3 pipeline/split_shelf_titles.py eg-rich`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `eg-rich-lafond-covered-with-mud-and-glory` | Georges Lafond | Covered with mud and glory | Edwin Gile Rich | 1918-1919 (see the Gutenberg header) | have | PG 60268 |
| `eg-rich-saint-saens-musical-memories` | Camille Saint-Saëns | Musical Memories | Edwin Gile Rich | 1918-1919 (see the Gutenberg header) | have | PG 16459 |

## H. Raahauge's Clara Viebig

Shelf: `pipeline/raahauge_shelf.json` · fetch `python3 pipeline/fetch_shelf.py raahauge` · titles `python3 pipeline/split_shelf_titles.py raahauge`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `raahauge-viebig-absolution` | Clara Viebig | Absolution | H. Raahauge | 1908-1913 (see the Gutenberg header) | have | PG 30724 |
| `raahauge-viebig-the-son-of-his-mother` | Clara Viebig | The Son of His Mother | H. Raahauge | 1908-1913 (see the Gutenberg header) | have | PG 30732 |

## E. C. Otté's Humboldt (Cosmos vol. 1; Views of Nature)

Shelf: `pipeline/otte_shelf.json` · fetch `python3 pipeline/fetch_shelf.py otte` · titles `python3 pipeline/split_shelf_titles.py otte`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `otte-humboldt-cosmos-a-sketch-of-the-physical-descript` | Alexander von Humboldt | Cosmos: A Sketch of the Physical Description of the Universe, Vol. 1 | E. C. Otté | 1849-1850 (see the Gutenberg header) | have | PG 14565 |
| `otte-humboldt-views-of-nature-or-contemplations-on-the` | Alexander von Humboldt | Views of nature: or Contemplations on the sublime phenomena of creation with scientific illustrations | E. C. Otté (with Henry G. Bohn) | 1849-1850 (see the Gutenberg header) | have | PG 67684 |

## Charles William O'Reilly: Werne's White Nile expedition (2 vols)

Shelf: `pipeline/co-reilly_shelf.json` · fetch `python3 pipeline/fetch_shelf.py co-reilly` · titles `python3 pipeline/split_shelf_titles.py co-reilly`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `co-reilly-werne-expedition-to-discover-the-sources-of-th-vol-1` | Ferdinand Werne | Expedition to discover the sources of the White Nile, in the years 1840, 1841, Vol. 1 (of 2) | Charles William O'Reilly | 1849 (see the Gutenberg header) | have | PG 73465 |
| `co-reilly-werne-expedition-to-discover-the-sources-of-th-vol-2` | Ferdinand Werne | Expedition to discover the sources of the White Nile, in the years 1840, 1841, Vol. 2 (of 2) | Charles William O'Reilly | 1849 (see the Gutenberg header) | have | PG 73466 |

## Mary Pickering Nichols (Gudrun; Wieck)

Shelf: `pipeline/mp-nichols_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mp-nichols` · titles `python3 pipeline/split_shelf_titles.py mp-nichols`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mp-nichols-gudrun-a-mediaeval-epic` | anonymous (Middle High German epic) | Gudrun: A Mediaeval Epic | Mary Pickering Nichols | 1875-1889 (see the Gutenberg header) | have | PG 46109 |
| `mp-nichols-wieck-piano-and-song` | Friedrich Wieck | Piano and song | Mary Pickering Nichols | 1875-1889 (see the Gutenberg header) | have | PG 16658 |

## W. Montgomery's Schweitzer (The Quest of the Historical Jesus; Paul and His Interpreters)

Shelf: `pipeline/w-montgomery_shelf.json` · fetch `python3 pipeline/fetch_shelf.py w-montgomery` · titles `python3 pipeline/split_shelf_titles.py w-montgomery`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `w-montgomery-schweitzer-paul-and-his-interpreters` | Albert Schweitzer | Paul and his interpreters | W. Montgomery | 1910-1912 (see the Gutenberg header) | have | PG 76284 |
| `w-montgomery-schweitzer-the-quest-of-the-historical-jesus` | Albert Schweitzer | The quest of the historical Jesus | W. Montgomery | 1910-1912 (see the Gutenberg header) | have | PG 45422 |

## G. F. Monkshood (Louÿs; Bourget)

Shelf: `pipeline/monkshood_shelf.json` · fetch `python3 pipeline/fetch_shelf.py monkshood` · titles `python3 pipeline/split_shelf_titles.py monkshood`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `monkshood-bourget-the-story-of-andre-cornelis` | Paul Bourget | The Story of André Cornélis | G. F. Monkshood | 1908-1909 (see the Gutenberg header) | have | PG 66636 |
| `monkshood-louys-woman-and-puppet-etc` | Pierre Louÿs | Woman and Puppet, Etc. | G. F. Monkshood | 1908-1909 (see the Gutenberg header) | have | PG 51107 |

## P. Chalmers Mitchell (Hertwig; Metchnikoff)

Shelf: `pipeline/chalmers-mitchell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py chalmers-mitchell` · titles `python3 pipeline/split_shelf_titles.py chalmers-mitchell`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `chalmers-mitchell-hertwig-the-biological-problem-of-to-day-preform` | Oscar Hertwig | The Biological Problem of To-day: Preformation Or Epigenesis? The Basis of a Theory of Organic Development | P. Chalmers Mitchell | 1896-1903 (see the Gutenberg header) | have | PG 37221 |
| `chalmers-mitchell-metchnikoff-the-nature-of-man` | Elie Metchnikoff | The nature of man | P. Chalmers Mitchell | 1896-1903 (see the Gutenberg header) | have | PG 75505 |

## Katherine Miller's Romain Rolland

Shelf: `pipeline/katherine-miller_shelf.json` · fetch `python3 pipeline/fetch_shelf.py katherine-miller` · titles `python3 pipeline/split_shelf_titles.py katherine-miller`.
Round 38 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `katherine-miller-rolland-clerambault-the-story-of-an-independent` | Romain Rolland | Clerambault: The Story of an Independent Spirit During the War | Katherine Miller | 1919-1921 (see the Gutenberg header) | have | PG 10868 |
| `katherine-miller-rolland-colas-breugnon` | Romain Rolland | Colas Breugnon | Katherine Miller | 1919-1921 (see the Gutenberg header) | have | PG 70371 |

## Anthony C. Middleton: d'Holbach's Letters to Eugenia

Shelf: `pipeline/ac-middleton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ac-middleton` · titles `python3 pipeline/split_shelf_titles.py ac-middleton`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ac-middleton-holbach-letters-to-eugenia-or-a-preservative-aga` | Paul-Henri Thiry, baron d'Holbach | Letters to Eugenia; Or, A Preservative Against Religious Prejudices | Anthony C. Middleton | 1870 (see the Gutenberg header) | have | PG 31275 |
| — | — | pg-38094: Another Gutenberg file of the same translation: duplicate, not shelved. | — | — | excluded | — |

## L. G. Meyer (Huysmans; Zola)

Shelf: `pipeline/lg-meyer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lg-meyer` · titles `python3 pipeline/split_shelf_titles.py lg-meyer`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lg-meyer-huysmans-sac-au-dos` | J.-K. Huysmans | Sac-Au-Dos | L. G. Meyer | 1907 (see the Gutenberg header) | have | PG 23216 |
| `lg-meyer-zola-the-fete-at-coqueville` | Émile Zola | The Fête At Coqueville | L. G. Meyer | 1907 (see the Gutenberg header) | have | PG 23222 |

## Ella McMahon (Caussade's Abandonment; St Francis de Sales)

Shelf: `pipeline/ella-mcmahon_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ella-mcmahon` · titles `python3 pipeline/split_shelf_titles.py ella-mcmahon`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ella-mcmahon-caussade-abandonment-or-absolute-surrender-to-div` | Jean Pierre de Caussade | Abandonment; or, Absolute Surrender to Divine Providence | Ella McMahon | 1884-1887 (see the Gutenberg header) | have | PG 52057 |
| `ella-mcmahon-francis-maxims-and-counsels-of-st-francis-de-sal` | St. Francis de Sales | Maxims and counsels of St. Francis de Sales for every day of the year | Ella McMahon | 1884-1887 (see the Gutenberg header) | have | PG 73661 |

## John Maver: Zúñiga's Historical View of the Philippine Islands (2 vols)

Shelf: `pipeline/maver_shelf.json` · fetch `python3 pipeline/fetch_shelf.py maver` · titles `python3 pipeline/split_shelf_titles.py maver`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `maver-zuniga-an-historical-view-of-the-philippine-isl-vol-1` | Joaquín Martínez de Zúñiga | An Historical View of the Philippine Islands, Vol 1 (of 2) Exhibiting their discovery, population, language, government, manners, customs, productions and commerce. | John Maver | 1814 (see the Gutenberg header) | have | PG 39010 |
| `maver-zuniga-an-historical-view-of-the-philippine-isl-vol-2` | Joaquín Martínez de Zúñiga | An Historical View of the Philippine Islands, Vol 2 (of 2) Exhibiting their discovery, population, language, government, manners, customs, productions and commerce. | John Maver | 1814 (see the Gutenberg header) | have | PG 39027 |

## Clarence A. Manning: Korolenko's Birds of Heaven

Shelf: `pipeline/ca-manning_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ca-manning` · titles `python3 pipeline/split_shelf_titles.py ca-manning`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ca-manning-korolenko-birds-of-heaven-and-other-stories` | Vladimir Korolenko | Birds of Heaven, and Other Stories | Clarence A. Manning | 1919 (see the Gutenberg header) | have | PG 60256 |
| — | — | pg-78316: Taras Shevchenko, the Poet of Ukraine (1945): printed after 1930, not public domain on this lane's rule. | — | — | excluded | — |

## George Maidment's Funck-Brentano

Shelf: `pipeline/maidment_shelf.json` · fetch `python3 pipeline/fetch_shelf.py maidment` · titles `python3 pipeline/split_shelf_titles.py maidment`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `maidment-funck-brentano-legends-of-the-bastille` | Frantz Funck-Brentano | Legends of the Bastille | George Maidment | 1899-1901 (see the Gutenberg header) | have | PG 43231 |
| `maidment-funck-brentano-princes-and-poisoners-studies-of-the-cou` | Frantz Funck-Brentano | Princes and Poisoners: Studies of the Court of Louis XIV | George Maidment | 1899-1901 (see the Gutenberg header) | have | PG 43238 |

## Kenneth R. H. Mackenzie (Tyll Owlglass; Hesekiel's Bismarck)

Shelf: `pipeline/krh-mackenzie_shelf.json` · fetch `python3 pipeline/fetch_shelf.py krh-mackenzie` · titles `python3 pipeline/split_shelf_titles.py krh-mackenzie`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `krh-mackenzie-hesekiel-the-life-of-bismarck-private-and-politic` | George Hesekiel | The Life of Bismarck, Private and Political With Descriptive Notices of His Ancestry | Kenneth R. H. Mackenzie | 1860-1870 (see the Gutenberg header) | have | PG 58776 |
| `krh-mackenzie-owlglass-the-marvellous-adventures-and-rare-conce` | anonymous (the Till Eulenspiegel chapbook) | The Marvellous Adventures and Rare Conceits of Master Tyll Owlglass Newly collected, chronicled and set forth, in our English tongue | Kenneth R. H. Mackenzie | 1860-1870 (see the Gutenberg header) | have | PG 55035 |

## Marjorie Laurie's Loti

Shelf: `pipeline/marjorie-laurie_shelf.json` · fetch `python3 pipeline/fetch_shelf.py marjorie-laurie` · titles `python3 pipeline/split_shelf_titles.py marjorie-laurie`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `marjorie-laurie-loti-the-sahara` | Pierre Loti | The Sahara | Marjorie Laurie | 1917-1921 (see the Gutenberg header) | have | PG 59077 |
| `marjorie-laurie-loti-war` | Pierre Loti | War | Marjorie Laurie | 1917-1921 (see the Gutenberg header) | have | PG 35211 |

## Mrs. John Lane's Anatole France

Shelf: `pipeline/mrs-john-lane_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mrs-john-lane` · titles `python3 pipeline/split_shelf_titles.py mrs-john-lane`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mrs-john-lane-france-balthasar-and-other-works` | Anatole France | Balthasar and Other Works - | Mrs. John Lane | 1909-1911 (see the Gutenberg header) | have | PG 22059 |
| `mrs-john-lane-france-honey-bee` | Anatole France | Honey-Bee | Mrs. John Lane | 1909-1911 (see the Gutenberg header) | have | PG 25405 |

## Robert Rives La Monte (Ferri; Deville)

Shelf: `pipeline/la-monte_shelf.json` · fetch `python3 pipeline/fetch_shelf.py la-monte` · titles `python3 pipeline/split_shelf_titles.py la-monte`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `la-monte-deville-socialism-revolution-and-internationalis` | Gabriel Pierre Deville | Socialism, Revolution and Internationalism | Robert Rives La Monte | 1900-1907 (see the Gutenberg header) | have | PG 35962 |
| `la-monte-ferri-socialism-and-modern-science-darwin-spen` | Enrico Ferri | Socialism and Modern Science (Darwin, Spencer, Marx) | Robert Rives La Monte | 1900-1907 (see the Gutenberg header) | have | PG 18397 |

## Mrs. Carlton A. Kingsbury (Claretie; About)

Shelf: `pipeline/kingsbury_shelf.json` · fetch `python3 pipeline/fetch_shelf.py kingsbury` · titles `python3 pipeline/split_shelf_titles.py kingsbury`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `kingsbury-about-the-king-of-the-mountains` | Edmond About | The King of the Mountains | Mrs. Carlton A. Kingsbury | 1897 (see the Gutenberg header) | have | PG 42096 |
| `kingsbury-claretie-the-crime-of-the-boulevard` | Jules Claretie | The Crime of the Boulevard | Mrs. Carlton A. Kingsbury | 1897 (see the Gutenberg header) | have | PG 34058 |

## Charles H. Kerr (Labriola; Lafargue's Right to Be Lazy)

Shelf: `pipeline/ch-kerr_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ch-kerr` · titles `python3 pipeline/split_shelf_titles.py ch-kerr`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ch-kerr-labriola-essays-on-the-materialistic-conception-o` | Antonio Labriola | Essays on the Materialistic Conception of History | Charles H. Kerr | 1904-1907 (see the Gutenberg header) | have | PG 32644 |
| `ch-kerr-lafargue-the-right-to-be-lazy-and-other-studies` | Paul Lafargue | The right to be lazy, and other studies | Charles H. Kerr | 1904-1907 (see the Gutenberg header) | have | PG 52984 |

## John Kenrick: Strauss's Helon's Pilgrimage to Jerusalem (2 vols)

Shelf: `pipeline/kenrick_shelf.json` · fetch `python3 pipeline/fetch_shelf.py kenrick` · titles `python3 pipeline/split_shelf_titles.py kenrick`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `kenrick-strauss-helon-s-pilgrimage-to-jerusalem-volume-1` | Friedrich Strauss | Helon's Pilgrimage to Jerusalem, Volume 1 (of 2) A picture of Judaism, in the century which preceded the advent of our Savior. | John Kenrick | 1824 (see the Gutenberg header) | have | PG 54867 |
| `kenrick-strauss-helon-s-pilgrimage-to-jerusalem-volume-2` | Friedrich Strauss | Helon's Pilgrimage to Jerusalem, Volume 2 (of 2) A picture of Judaism, in the century which preceded the advent of our Savior. | John Kenrick | 1824 (see the Gutenberg header) | have | PG 56891 |

## Charlotte Brewster Jordan's Blasco Ibáñez (The Four Horsemen of the Apocalypse)

Shelf: `pipeline/cb-jordan_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cb-jordan` · titles `python3 pipeline/split_shelf_titles.py cb-jordan`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cb-jordan-ibanez-mare-nostrum-our-sea-a-novel` | Vicente Blasco Ibáñez | Mare Nostrum (Our Sea): A Novel | Charlotte Brewster Jordan | 1918-1919 (see the Gutenberg header) | have | PG 11697 |
| `cb-jordan-ibanez-the-four-horsemen-of-the-apocalypse` | Vicente Blasco Ibáñez | The Four Horsemen of the Apocalypse | Charlotte Brewster Jordan | 1918-1919 (see the Gutenberg header) | have | PG 1484 |

## Smith Ely Jelliffe (Silberer; Rank)

Shelf: `pipeline/jelliffe_shelf.json` · fetch `python3 pipeline/fetch_shelf.py jelliffe` · titles `python3 pipeline/split_shelf_titles.py jelliffe`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `jelliffe-rank-the-myth-of-the-birth-of-the-hero-a-psyc` | Otto Rank | The Myth of the Birth of the Hero: A psychological interpretation of mythology | Smith Ely Jelliffe (with F. Robbins) | 1914-1917 (see the Gutenberg header) | have | PG 66192 |
| `jelliffe-silberer-hidden-symbolism-of-alchemy-and-the-occu` | Herbert Silberer | Hidden Symbolism of Alchemy and the Occult Arts | Smith Ely Jelliffe | 1914-1917 (see the Gutenberg header) | have | PG 27755 |

## J. V. Huntington: Franchère's Voyage to the Northwest Coast

Shelf: `pipeline/jv-huntington_shelf.json` · fetch `python3 pipeline/fetch_shelf.py jv-huntington` · titles `python3 pipeline/split_shelf_titles.py jv-huntington`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `jv-huntington-franchere-narrative-of-a-voyage-to-the-northwest-c` | Gabriel Franchère | Narrative of a Voyage to the Northwest Coast of America in the years 1811, 1812, 1813, and 1814 or the First American Settlement on the Pacific | J. V. Huntington | 1854 (see the Gutenberg header) | have | PG 15911 |
| — | — | pg-76209: Thwaites's Early Western Travels vol. 6 reprints Huntington's Franchère together with Brackenridge's own English journal; the translation is already shelved from PG 15911. | — | — | excluded | — |

## John Howard's Remy de Gourmont

Shelf: `pipeline/john-howard_shelf.json` · fetch `python3 pipeline/fetch_shelf.py john-howard` · titles `python3 pipeline/split_shelf_titles.py john-howard`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `john-howard-gourmont-mr-antiphilos-satyr` | Remy de Gourmont | Mr. Antiphilos, satyr | John Howard (with Louis Lozowick) | 1921-1922 (see the Gutenberg header) | have | PG 78206 |
| `john-howard-gourmont-the-book-of-masks` | Remy de Gourmont | The Book of Masks | John Howard | 1921-1922 (see the Gutenberg header) | have | PG 46247 |

## F. Appleby Holt (Gilliard's Thirteen Years at the Russian Court; Benoît)

Shelf: `pipeline/fa-holt_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fa-holt` · titles `python3 pipeline/split_shelf_titles.py fa-holt`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fa-holt-benoit-the-secret-spring` | Pierre Benoît | The secret spring | F. Appleby Holt (with H. W. Fox) | 1920-1921 (see the Gutenberg header) | have | PG 69281 |
| `fa-holt-gilliard-thirteen-years-at-the-russian-court-a-pe` | Pierre Gilliard | Thirteen years at the Russian court (a personal record of the last years and death of the Czar Nicholas II. and his family) | F. Appleby Holt | 1920-1921 (see the Gutenberg header) | have | PG 60546 |

## Nora Kathleen Hills's Vimar picture books

Shelf: `pipeline/nk-hills_shelf.json` · fetch `python3 pipeline/fetch_shelf.py nk-hills` · titles `python3 pipeline/split_shelf_titles.py nk-hills`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `nk-hills-vimar-clown-the-circus-dog` | Auguste Vimar | Clown, the Circus Dog | Nora Kathleen Hills | 1914 (see the Gutenberg header) | have | PG 46793 |
| `nk-hills-vimar-the-curly-haired-hen` | Auguste Vimar | The Curly-Haired Hen | Nora Kathleen Hills | 1914 (see the Gutenberg header) | have | PG 13302 |

## Emily Hill: Karasowski's Chopin (2 vols)

Shelf: `pipeline/emily-hill_shelf.json` · fetch `python3 pipeline/fetch_shelf.py emily-hill` · titles `python3 pipeline/split_shelf_titles.py emily-hill`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `emily-hill-karasowski-frederic-chopin-his-life-letters-and-wor-vol-1` | Maurycy Karasowski | Frederic Chopin: His Life, Letters, and Works,  v. 1 (of  2) | Emily Hill | 1879 (see the Gutenberg header) | have | PG 46577 |
| `emily-hill-karasowski-frederic-chopin-his-life-letters-and-wor-vol-2` | Maurycy Karasowski | Frederic Chopin: His Life, Letters, and Works,  v. 2 (of  2) | Emily Hill | 1879 (see the Gutenberg header) | have | PG 46573 |

## William Frederick Harvey (Nyrop; Nordau)

Shelf: `pipeline/wf-harvey_shelf.json` · fetch `python3 pipeline/fetch_shelf.py wf-harvey` · titles `python3 pipeline/split_shelf_titles.py wf-harvey`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `wf-harvey-nordau-on-art-and-artists` | Max Nordau | On art and artists | William Frederick Harvey | 1901-1907 (see the Gutenberg header) | have | PG 76748 |
| `wf-harvey-nyrop-the-kiss-and-its-history` | Kristoffer Nyrop | The kiss and its history | William Frederick Harvey | 1901-1907 (see the Gutenberg header) | have | PG 51856 |

## Robert Harrison: Reumont's Lorenzo de' Medici (2 vols)

Shelf: `pipeline/robert-harrison_shelf.json` · fetch `python3 pipeline/fetch_shelf.py robert-harrison` · titles `python3 pipeline/split_shelf_titles.py robert-harrison`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `robert-harrison-reumont-lorenzo-de-medici-the-magnificent-vol-1` | Alfred von Reumont | Lorenzo de' Medici, the Magnificent (vol. 1 of 2) | Robert Harrison | 1876 (see the Gutenberg header) | have | PG 50624 |
| `robert-harrison-reumont-lorenzo-de-medici-the-magnificent-vol-2` | Alfred von Reumont | Lorenzo de' Medici, the Magnificent (vol. 2 of 2) | Robert Harrison | 1876 (see the Gutenberg header) | have | PG 50625 |

## Henry Harland (Feuillet; Serao)

Shelf: `pipeline/henry-harland_shelf.json` · fetch `python3 pipeline/fetch_shelf.py henry-harland` · titles `python3 pipeline/split_shelf_titles.py henry-harland`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `henry-harland-feuillet-the-romance-of-a-poor-young-man` | Octave Feuillet | The Romance of a Poor Young Man | Henry Harland | 1890 (see the Gutenberg header) | have | PG 45200 |
| `henry-harland-serao-fantasy-a-novel` | Matilde Serao | Fantasy: A Novel | Henry Harland (with Paul Sylvester) | 1890 (see the Gutenberg header) | have | PG 67143 |

## Joseph I. Gorfinkle's Pirke Avot

Shelf: `pipeline/gorfinkle_shelf.json` · fetch `python3 pipeline/fetch_shelf.py gorfinkle` · titles `python3 pipeline/split_shelf_titles.py gorfinkle`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `gorfinkle-pirke-avot-the-sayings-of-the-jewish-fat` | the Mishnah (tractate Avot) | Pirke Avot: The Sayings of the Jewish Fathers | Joseph I. Gorfinkle | 1913 (see the Gutenberg header) | have | PG 8547 |
| — | — | pg-8548: Another Gutenberg file of the same translation: duplicate, not shelved. | — | — | excluded | — |

## Sir Home Gordon's Faguet

Shelf: `pipeline/home-gordon_shelf.json` · fetch `python3 pipeline/fetch_shelf.py home-gordon` · titles `python3 pipeline/split_shelf_titles.py home-gordon`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `home-gordon-faguet-initiation-into-literature` | Émile Faguet | Initiation into Literature | Sir Home Gordon | 1913-1914 (see the Gutenberg header) | have | PG 8555 |
| `home-gordon-faguet-initiation-into-philosophy` | Émile Faguet | Initiation into Philosophy | Sir Home Gordon | 1913-1914 (see the Gutenberg header) | have | PG 9304 |

## Mrs. W. A. Gillespie's Blasco Ibáñez

Shelf: `pipeline/mrs-gillespie_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mrs-gillespie` · titles `python3 pipeline/split_shelf_titles.py mrs-gillespie`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mrs-gillespie-ibanez-blood-and-sand` | Vicente Blasco Ibáñez | Blood and Sand | Mrs. W. A. Gillespie | 1909-1913 (see the Gutenberg header) | have | PG 54222 |
| `mrs-gillespie-ibanez-the-shadow-of-the-cathedral` | Vicente Blasco Ibáñez | The Shadow of the Cathedral | Mrs. W. A. Gillespie | 1909-1913 (see the Gutenberg header) | have | PG 12041 |

## J. E. Fries (Arrhenius; Björklund)

Shelf: `pipeline/je-fries_shelf.json` · fetch `python3 pipeline/fetch_shelf.py je-fries` · titles `python3 pipeline/split_shelf_titles.py je-fries`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `je-fries-arrhenius-the-destinies-of-the-stars` | Svante Arrhenius | The Destinies of the Stars | J. E. Fries | 1910-1918 (see the Gutenberg header) | have | PG 58222 |
| `je-fries-bjorklund-death-and-resurrection-from-the-point-of` | Gustaf Björklund | Death and resurrection from the point of view of the cell-theory | J. E. Fries | 1910-1918 (see the Gutenberg header) | have | PG 60750 |

## Frank Roy Fraprie (Hallays; Mayer)

Shelf: `pipeline/fraprie_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fraprie` · titles `python3 pipeline/split_shelf_titles.py fraprie`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fraprie-hallays-the-spell-of-the-heart-of-france-the-tow` | André Hallays | The spell of the heart of France: the towns, villages and châteaux about Paris | Frank Roy Fraprie | 1912-1923 (see the Gutenberg header) | have | PG 46321 |
| `fraprie-mayer-bromoil-printing-and-bromoil-transfer` | Emil Mayer | Bromoil printing and bromoil transfer | Frank Roy Fraprie | 1912-1923 (see the Gutenberg header) | have | PG 69127 |

## Cecil Fairfax: Bjørnson's Heritage of the Kurts (2 vols)

Shelf: `pipeline/cecil-fairfax_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cecil-fairfax` · titles `python3 pipeline/split_shelf_titles.py cecil-fairfax`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cecil-fairfax-bjornson-the-heritage-of-the-kurts-volume-1-of-2` | Bjørnstjerne Bjørnson | The Heritage of the Kurts, Volume 1 (of 2) | Cecil Fairfax | 1892 (see the Gutenberg header) | have | PG 37801 |
| `cecil-fairfax-bjornson-the-heritage-of-the-kurts-volume-2-of-2` | Bjørnstjerne Bjørnson | The Heritage of the Kurts, Volume 2 (of 2) | Cecil Fairfax | 1892 (see the Gutenberg header) | have | PG 37802 |

## George Eliot as translator (Strauss's Life of Jesus; Feuerbach's Essence of Christianity)

Shelf: `pipeline/george-eliot-translations_shelf.json` · fetch `python3 pipeline/fetch_shelf.py george-eliot-translations` · titles `python3 pipeline/split_shelf_titles.py george-eliot-translations`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `george-eliot-translations-feuerbach-the-essence-of-christianity-translated-f` | Ludwig Feuerbach | The Essence of Christianity Translated from the second German edition | George Eliot | 1846-1854 (see the Gutenberg header) | have | PG 47025 |
| `george-eliot-translations-strauss-the-life-of-jesus-critically-examined-4t` | David Friedrich Strauss | The Life of Jesus Critically Examined (4th ed.) | George Eliot | 1846-1854 (see the Gutenberg header) | have | PG 64037 |

## Amelia B. Edwards (Maspero's Egyptian Archaeology; Loviot)

Shelf: `pipeline/amelia-edwards_shelf.json` · fetch `python3 pipeline/fetch_shelf.py amelia-edwards` · titles `python3 pipeline/split_shelf_titles.py amelia-edwards`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `amelia-edwards-loviot-a-lady-s-captivity-among-chinese-pirates` | Fanny Loviot | A lady's captivity among Chinese pirates in the Chinese seas | Amelia B. Edwards | 1858-1887 (see the Gutenberg header) | have | PG 34167 |
| `amelia-edwards-maspero-manual-of-egyptian-archaeology-and-guide` | Gaston Maspero | Manual of Egyptian Archaeology and Guide to the Study of Antiquities in Egypt | Amelia B. Edwards | 1858-1887 (see the Gutenberg header) | have | PG 14400 |

## J. D. Duff (Aksakov; Herzen's Memoirs)

Shelf: `pipeline/jd-duff_shelf.json` · fetch `python3 pipeline/fetch_shelf.py jd-duff` · titles `python3 pipeline/split_shelf_titles.py jd-duff`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `jd-duff-aksakov-a-russian-gentleman` | S. T. Aksakov | A Russian Gentleman | J. D. Duff | 1917-1923 (see the Gutenberg header) | have | PG 38781 |
| `jd-duff-herzen-the-memoirs-of-alexander-herzen-parts-i` | Aleksandr Herzen | The Memoirs of Alexander Herzen, Parts I and II | J. D. Duff | 1917-1923 (see the Gutenberg header) | have | PG 67882 |

## Bérengère Drillien's Anatole France

Shelf: `pipeline/drillien_shelf.json` · fetch `python3 pipeline/fetch_shelf.py drillien` · titles `python3 pipeline/split_shelf_titles.py drillien`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `drillien-france-monsieur-bergeret-in-paris` | Anatole France | Monsieur Bergeret in Paris | Bérengère Drillien | 1919-1921 (see the Gutenberg header) | have | PG 49414 |
| `drillien-france-the-amethyst-ring` | Anatole France | The Amethyst Ring | Bérengère Drillien | 1919-1921 (see the Gutenberg header) | have | PG 49108 |

## Robert B. Douglas (Thaïs; the Cent Nouvelles Nouvelles)

Shelf: `pipeline/rb-douglas_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rb-douglas` · titles `python3 pipeline/split_shelf_titles.py rb-douglas`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rb-douglas-france-thais` | Anatole France | Thais | Robert B. Douglas | 1899-1909 (see the Gutenberg header) | have | PG 2078 |
| `rb-douglas-one-hundred-merrie-and-delightsome-stori` | anonymous (Les Cent Nouvelles Nouvelles) | One Hundred Merrie And Delightsome Stories Right Pleasaunte To Relate In All Goodly Companie By Way Of Joyance And Jollity | Robert B. Douglas | 1899-1909 (see the Gutenberg header) | have | PG 18575 |

## Frances Elizabeth Cox's Hymns from the German

Shelf: `pipeline/fe-cox_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fe-cox` · titles `python3 pipeline/split_shelf_titles.py fe-cox`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fe-cox-hymns-from-the-german-translated-by-fran` | various German hymn writers (anthology) | Hymns from the German Translated by Frances Elizabeth Cox | Frances Elizabeth Cox | 1841-1864 (see the Gutenberg header) | have | PG 39439 |
| `fe-cox-sacred-hymns-from-the-german-translated` | various German hymn writers (anthology) | Sacred Hymns from the German Translated by Frances Elizabeth Cox | Frances Elizabeth Cox | 1841-1864 (see the Gutenberg header) | have | PG 39440 |

## Mrs. L. Burke's Madame Guizot

Shelf: `pipeline/mrs-l-burke_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mrs-l-burke` · titles `python3 pipeline/split_shelf_titles.py mrs-l-burke`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mrs-l-burke-guizot-moral-tales` | Madame Guizot | Moral Tales | Mrs. L. Burke | 1850s (see the Gutenberg header) | have | PG 47485 |
| `mrs-l-burke-guizot-popular-tales` | Madame Guizot | Popular Tales | Mrs. L. Burke | 1850s (see the Gutenberg header) | have | PG 42839 |

## Madame Burette: Tieck's Rebellion in the Cevennes (2 vols)

Shelf: `pipeline/burette_shelf.json` · fetch `python3 pipeline/fetch_shelf.py burette` · titles `python3 pipeline/split_shelf_titles.py burette`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `burette-tieck-the-rebellion-in-the-cevennes-an-histori-vol-1` | Ludwig Tieck | The Rebellion in the Cevennes, an Historical Novel. Vol. I. | Madame Burette | 1845 (see the Gutenberg header) | have | PG 31738 |
| `burette-tieck-the-rebellion-in-the-cevennes-an-histori-vol-2` | Ludwig Tieck | The Rebellion in the Cevennes, an Historical Novel. Vol. II. | Madame Burette | 1845 (see the Gutenberg header) | have | PG 31739 |

## Neil Buchanan: Harnack's History of Dogma (vols 1-2)

Shelf: `pipeline/neil-buchanan_shelf.json` · fetch `python3 pipeline/fetch_shelf.py neil-buchanan` · titles `python3 pipeline/split_shelf_titles.py neil-buchanan`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `neil-buchanan-harnack-history-of-dogma-volume-1` | Adolf von Harnack | History of Dogma, Volume 1 | Neil Buchanan | 1894-1896 (see the Gutenberg header) | have | PG 19612 |
| `neil-buchanan-harnack-history-of-dogma-volume-2` | Adolf von Harnack | History of Dogma, Volume 2 | Neil Buchanan | 1894-1896 (see the Gutenberg header) | have | PG 19613 |

## Eleanor Stimson Brooks (Duhamel; Rolland)

Shelf: `pipeline/eleanor-brooks_shelf.json` · fetch `python3 pipeline/fetch_shelf.py eleanor-brooks` · titles `python3 pipeline/split_shelf_titles.py eleanor-brooks`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `eleanor-brooks-duhamel-the-heart-s-domain` | Georges Duhamel | The Heart's Domain | Eleanor Stimson Brooks | 1919-1925 (see the Gutenberg header) | have | PG 66564 |
| `eleanor-brooks-rolland-summer` | Romain Rolland | Summer | Eleanor Stimson Brooks (with Van Wyck Brooks) | 1919-1925 (see the Gutenberg header) | have | PG 66882 |

## Van Wyck Brooks: Bazalgette's Thoreau

Shelf: `pipeline/van-wyck-brooks_shelf.json` · fetch `python3 pipeline/fetch_shelf.py van-wyck-brooks` · titles `python3 pipeline/split_shelf_titles.py van-wyck-brooks`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `van-wyck-brooks-bazalgette-henry-thoreau-bachelor-of-nature` | Léon Bazalgette | Henry Thoreau, bachelor of nature | Van Wyck Brooks | 1924 (see the Gutenberg header) | have | PG 78810 |
| — | — | pg-66882: Rolland's Summer: on eleanor-brooks_shelf.json (a joint translation). | — | — | excluded | — |

## Percy Favor Bicknell's Jókai

Shelf: `pipeline/pf-bicknell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py pf-bicknell` · titles `python3 pipeline/split_shelf_titles.py pf-bicknell`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `pf-bicknell-jokai-manasseh-a-romance-of-transylvania` | Mór Jókai | Manasseh: A Romance of Transylvania | Percy Favor Bicknell | 1900-1901 (see the Gutenberg header) | have | PG 20892 |
| `pf-bicknell-jokai-the-baron-s-sons-a-romance-of-the-hungar` | Mór Jókai | The Baron's Sons: A Romance of the Hungarian Revolution of 1848 | Percy Favor Bicknell | 1900-1901 (see the Gutenberg header) | have | PG 34674 |

## Ernest Bell's Lessing

Shelf: `pipeline/ernest-bell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ernest-bell` · titles `python3 pipeline/split_shelf_titles.py ernest-bell`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ernest-bell-lessing-minna-von-barnhelm` | Gotthold Ephraim Lessing | Minna Von Barnhelm | Ernest Bell | 1878 (see the Gutenberg header) | have | PG 2663 |
| `ernest-bell-lessing-the-dramatic-works-of-g-e-lessing-miss-s` | Gotthold Ephraim Lessing | The Dramatic Works of G. E. Lessing Miss Sara Sampson, Philotas, Emilia Galotti, Nathan the Wise | Ernest Bell | 1878 (see the Gutenberg header) | have | PG 33435 |

## W. P. Baines's Loti

Shelf: `pipeline/baines_shelf.json` · fetch `python3 pipeline/fetch_shelf.py baines` · titles `python3 pipeline/split_shelf_titles.py baines`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `baines-loti-a-tale-of-brittany-mon-frere-yves` | Pierre Loti | A Tale of Brittany (Mon frère Yves) | W. P. Baines | 1909-1923 (see the Gutenberg header) | have | PG 62667 |
| `baines-loti-egypt-la-mort-de-philae` | Pierre Loti | Egypt (La Mort de Philae) | W. P. Baines | 1909-1923 (see the Gutenberg header) | have | PG 3685 |

## Katharine Babbitt (French war memoirs)

Shelf: `pipeline/katharine-babbitt_shelf.json` · fetch `python3 pipeline/fetch_shelf.py katharine-babbitt` · titles `python3 pipeline/split_shelf_titles.py katharine-babbitt`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `katharine-babbitt-cuvru-magot-beyond-the-marne-quincy-huiry-voisins-be` | Henriette Cuvru-Magot | Beyond the Marne: Quincy, Huiry, Voisins before and during the battle | Katharine Babbitt | 1917-1918 (see the Gutenberg header) | have | PG 44599 |
| `katharine-babbitt-nicolas-campaign-diary-of-a-french-officer` | René Nicolas | Campaign diary of a French officer | Katharine Babbitt | 1917-1918 (see the Gutenberg header) | have | PG 77912 |

## Ingeborg Andersen (Drachmann; Poulsen)

Shelf: `pipeline/ingeborg-andersen_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ingeborg-andersen` · titles `python3 pipeline/split_shelf_titles.py ingeborg-andersen`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ingeborg-andersen-drachmann-atheism-in-pagan-antiquity` | A. B. Drachmann | Atheism in Pagan Antiquity | Ingeborg Andersen | 1922 (see the Gutenberg header) | have | PG 28312 |
| `ingeborg-andersen-poulsen-etruscan-tomb-paintings-their-subjects-a` | Frederik Poulsen | Etruscan Tomb Paintings, Their Subjects and Significance | Ingeborg Andersen | 1922 (see the Gutenberg header) | have | PG 62431 |

## Mary H. Allies (Damascene on Holy Images; Chrysostom)

Shelf: `pipeline/mh-allies_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mh-allies` · titles `python3 pipeline/split_shelf_titles.py mh-allies`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mh-allies-chrysostom-leaves-from-st-john-chrysostom` | Saint John Chrysostom | Leaves from St. John Chrysostom | Mary H. Allies | 1889-1898 (see the Gutenberg header) | have | PG 62447 |
| `mh-allies-damascus-st-john-damascene-on-holy-images-followe` | Saint John of Damascus | St John Damascene on Holy Images (πρὸς τοὺς διαβάλλοντας τᾶς ἁγίας εἰκόνας). Followed by Three Sermons on the Assumption (κοίμησις) | Mary H. Allies | 1889-1898 (see the Gutenberg header) | have | PG 49917 |

## Abby Langdon Alger (Judith Gautier; Delsarte)

Shelf: `pipeline/abby-alger_shelf.json` · fetch `python3 pipeline/fetch_shelf.py abby-alger` · titles `python3 pipeline/split_shelf_titles.py abby-alger`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `abby-alger-delaumosne-delsarte-system-of-oratory` | Delaumosne and Angélique Arnaud (on François Delsarte) | Delsarte System of Oratory | Abby Langdon Alger (with Frances A. Shaw) | 1884-1887 (see the Gutenberg header) | have | PG 12200 |
| `abby-alger-gautier-the-usurper-an-episode-in-japanese-histo` | Judith Gautier | The Usurper: An Episode in Japanese History | Abby Langdon Alger | 1884-1887 (see the Gutenberg header) | have | PG 47002 |

## John C. Ager's Swedenborg

Shelf: `pipeline/ager_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ager` · titles `python3 pipeline/split_shelf_titles.py ager`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ager-swedenborg-angelic-wisdom-concerning-the-divine-lov` | Emanuel Swedenborg | Angelic Wisdom Concerning the Divine Love and the Divine Wisdom | John C. Ager | 1890s (see the Gutenberg header) | have | PG 16627 |
| `ager-swedenborg-heaven-and-its-wonders-and-hell` | Emanuel Swedenborg | Heaven and its Wonders and Hell | John C. Ager | 1890s (see the Gutenberg header) | have | PG 17368 |

## T. K. Abbott's Kant (the ethics)

Shelf: `pipeline/tk-abbott_shelf.json` · fetch `python3 pipeline/fetch_shelf.py tk-abbott` · titles `python3 pipeline/split_shelf_titles.py tk-abbott`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `tk-abbott-kant-fundamental-principles-of-the-metaphysic` | Immanuel Kant | Fundamental Principles of the Metaphysic of Morals | Thomas Kingsmill Abbott | 1873 (see the Gutenberg header) | have | PG 5682 |
| `tk-abbott-kant-the-metaphysical-elements-of-ethics` | Immanuel Kant | The Metaphysical Elements of Ethics | Thomas Kingsmill Abbott | 1873 (see the Gutenberg header) | have | PG 5684 |

## H. Parker: Village Folk-Tales of Ceylon (vols 1-2)

Shelf: `pipeline/h-parker_shelf.json` · fetch `python3 pipeline/fetch_shelf.py h-parker` · titles `python3 pipeline/split_shelf_titles.py h-parker`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `h-parker-village-folk-tales-of-ceylon-volume-1-of` | Sinhalese village storytellers (collected by H. Parker) | Village Folk-Tales of Ceylon, Volume 1 (of 3) | H. Parker | 1910-1914 (see the Gutenberg header) | have | PG 56614 |
| `h-parker-village-folk-tales-of-ceylon-volume-2-of` | Sinhalese village storytellers (collected by H. Parker) | Village Folk-Tales of Ceylon, Volume 2 (of 3) | H. Parker | 1910-1914 (see the Gutenberg header) | have | PG 57399 |

## Robert Parke: Mendoza's History of China (2 vols)

Shelf: `pipeline/robert-parke_shelf.json` · fetch `python3 pipeline/fetch_shelf.py robert-parke` · titles `python3 pipeline/split_shelf_titles.py robert-parke`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `robert-parke-mendoza-the-history-of-the-great-and-mighty-king-vol-1` | Juan González de Mendoza | The History of the Great and Mighty Kingdom of China and the Situation Thereof, Volume 1 (of 2) | Robert Parke | 1588 (Hakluyt Society reprint, 1853-1854) (see the Gutenberg header) | have | PG 39009 |
| `robert-parke-mendoza-the-history-of-the-great-and-mighty-king-vol-2` | Juan González de Mendoza | The History of the Great and Mighty Kingdom of China and the Situation Thereof, Volume 2 (of 2) | Robert Parke | 1588 (Hakluyt Society reprint, 1853-1854) (see the Gutenberg header) | have | PG 42551 |

## Alexander Muir: Gregorovius's Wanderings in Corsica (2 vols)

Shelf: `pipeline/alexander-muir_shelf.json` · fetch `python3 pipeline/fetch_shelf.py alexander-muir` · titles `python3 pipeline/split_shelf_titles.py alexander-muir`.
Round 39 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `alexander-muir-gregorovius-wanderings-in-corsica-its-history-and-it-vol-1` | Ferdinand Gregorovius | Wanderings in Corsica: Its History and Its Heroes. Vol. 1 of 2 | Alexander Muir | 1855 (see the Gutenberg header) | have | PG 44727 |
| `alexander-muir-gregorovius-wanderings-in-corsica-its-history-and-it-vol-2` | Ferdinand Gregorovius | Wanderings in Corsica: Its History and Its Heroes. Vol. 2 of 2 | Alexander Muir | 1855 (see the Gutenberg header) | have | PG 58337 |

## One-off translations: medieval and early texts (Anglo-Saxon Chronicle, Saxo, the Táin, Roland, sagas, Old English poems, Ship of Fools, Lusiad, Hypnerotomachia)

Shelf: `pipeline/singles-medieval-epic_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-medieval-epic` · titles `python3 pipeline/split_shelf_titles.py singles-medieval-epic`.
Round 40 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-medieval-epic-andreas` | anonymous (Old English) | Andreas: The Legend of St. Andrew | Robert K. Root | (see the Gutenberg header) | have | PG 15225 |
| `singles-medieval-epic-bartholomaeus-mediaeval-lore-from-bartholomew-anglicus` | Bartholomaeus Anglicus | Mediaeval Lore from Bartholomew Anglicus | John Trevisa | (see the Gutenberg header) | have | PG 6493 |
| `singles-medieval-epic-bedier-the-romance-of-tristan-and-iseult` | Joseph Bédier | The Romance of Tristan and Iseult | Hilaire Belloc | (see the Gutenberg header) | have | PG 14244 |
| `singles-medieval-epic-benjamin-the-itinerary-of-benjamin-of-tudela` | Benjamin of Tudela | The Itinerary of Benjamin of Tudela | Marcus Nathan Adler | (see the Gutenberg header) | have | PG 14981 |
| `singles-medieval-epic-brant-the-ship-of-fools-volume-1` | Sebastian Brant | The Ship of Fools, Volume 1 | Alexander Barclay | (see the Gutenberg header) | have | PG 20179 |
| `singles-medieval-epic-bury-the-love-of-books` | Richard de Bury | The Love of Books: The Philobiblon of Richard de Bury | Ernest Chester Thomas | (see the Gutenberg header) | have | PG 626 |
| `singles-medieval-epic-camoes-the-lusiad` | Luís de Camões | The Lusiad; Or, The Discovery of India, an Epic Poem | William Julius Mickle | (see the Gutenberg header) | have | PG 32528 |
| `singles-medieval-epic-colonna-hypnerotomachia` | Francesco Colonna | Hypnerotomachia: The Strife of Loue in a Dreame | Robert Dallington | (see the Gutenberg header) | have | PG 18459 |
| `singles-medieval-epic-cynewulf-the-elene-of-cynewulf-translated-into-en` | Cynewulf | The Elene of Cynewulf translated into English prose | Lucius Hudson Holt | (see the Gutenberg header) | have | PG 14781 |
| `singles-medieval-epic-eirik-the-red-s-saga` | anonymous (Icelandic saga) | Eirik the Red's Saga | John Sephton | (see the Gutenberg header) | have | PG 17946 |
| `singles-medieval-epic-elene` | anonymous (Old English) | Elene; Judith; Athelstan, or the Fight at Brunanburh; Byrhtnoth, or the Fight at Maldon; and the Dream of the Rood Anglo-Saxon Poems | James Mercer Garnett | (see the Gutenberg header) | have | PG 15879 |
| `singles-medieval-epic-haleole-the-hawaiian-romance-of-laieikawai` | S. N. Haleole | The Hawaiian Romance Of Laieikawai | Martha Warren Beckwith | (see the Gutenberg header) | have | PG 13603 |
| `singles-medieval-epic-john-damascene-barlaam-and-ioasaph` | attributed to St John of Damascus | Barlaam and Ioasaph | Harold Mattingly and George Ratcliffe Woodward | (see the Gutenberg header) | have | PG 749 |
| `singles-medieval-epic-la-chanson-de-roland` | anonymous (Old French epic) | La Chanson de Roland : Translated from the Seventh Edition of Léon Gautier | Léonce Rabillon | (see the Gutenberg header) | have | PG 23819 |
| `singles-medieval-epic-laxdaela-saga-translated-from-the-icelan` | anonymous (Icelandic saga) | Laxdæla Saga Translated from the Icelandic | Muriel A. C. Press | (see the Gutenberg header) | have | PG 17803 |
| `singles-medieval-epic-old-english-poems-translated-into-the-or` | anonymous (Old English) | Old English Poems Translated into the Original Meter Together with Short Selections from Old English Prose | Cosette Faust Newton and Stith Thompson | (see the Gutenberg header) | have | PG 31172 |
| `singles-medieval-epic-saxo-the-danish-history-books-i-ix` | Saxo Grammaticus | The Danish History, Books I-IX | Oliver Elton | (see the Gutenberg header) | have | PG 1150 |
| `singles-medieval-epic-selections-from-ancient-irish-poetry` | anonymous (Old Irish poets) | Selections from Ancient Irish Poetry | Kuno Meyer | (see the Gutenberg header) | have | PG 32030 |
| `singles-medieval-epic-sturla-the-norwegian-account-of-haco-s-expediti` | Sturla Þórðarson | The Norwegian account of Haco's expedition against Scotland, A.D. MCCLXIII. | James Johnstone | (see the Gutenberg header) | have | PG 18299 |
| `singles-medieval-epic-tegner-fridthjof-s-saga` | Esaias Tegnér | Fridthjof's Saga; a Norse romance | Martha A. Lyon Holcomb and Thomas A. E. Holcomb | (see the Gutenberg header) | have | PG 3759 |
| `singles-medieval-epic-the-ancient-irish-epic-tale-tain-bo-cual` | anonymous (Old Irish) | The Ancient Irish Epic Tale Táin Bó Cúalnge | Joseph Dunn | (see the Gutenberg header) | have | PG 16464 |
| `singles-medieval-epic-the-anglo-saxon-chronicle` | anonymous (Old English annals) | The Anglo-Saxon Chronicle | J. Ingram and J. A. Giles | (see the Gutenberg header) | have | PG 657 |
| `singles-medieval-epic-the-cattle-raid-of-cualnge-tain-bo-cualn` | anonymous (Old Irish) | The Cattle-Raid of Cualnge (Tain Bo Cualnge) : An Old Irish Prose-Epic | Lucy Winifred Faraday | (see the Gutenberg header) | have | PG 14391 |
| `singles-medieval-epic-the-high-history-of-the-holy-graal` | anonymous (Old French romance, Perlesvaus) | The High History of the Holy Graal | Sebastian Evans | (see the Gutenberg header) | have | PG 750 |
| `singles-medieval-epic-the-lay-of-the-cid` | anonymous (Old Spanish epic) | The Lay of the Cid | R. Selden Rose and Leonard Bacon | (see the Gutenberg header) | have | PG 6088 |
| `singles-medieval-epic-villani-villani-s-chronicle-being-selections-fro` | Giovanni Villani | Villani's Chronicle Being Selections from the First Nine Books of the Croniche Fiorentine of Giovanni Villani | Rose E. Selfe | (see the Gutenberg header) | have | PG 33022 |
| `singles-medieval-epic-wynne-the-visions-of-the-sleeping-bard` | Ellis Wynne | The Visions of the Sleeping Bard | Robert Gwyneddon Davies | (see the Gutenberg header) | have | PG 5671 |

## One-off translations: philosophy, history and science (Burckhardt, Bergson, Amiel, Machiavelli's Discourses, Kandinsky, Engels, Planck, Lavoisier, Comenius)

Shelf: `pipeline/singles-ideas_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-ideas` · titles `python3 pipeline/split_shelf_titles.py singles-ideas`.
Round 40 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-ideas-amiel-amiel-s-journal` | Henri Frédéric Amiel | Amiel's Journal: The Journal Intime of Henri-Frédéric Amiel | Humphry Ward | (see the Gutenberg header) | have | PG 8545 |
| `singles-ideas-bastiat-sophisms-of-the-protectionists` | Frédéric Bastiat | Sophisms of the Protectionists | Horace White | (see the Gutenberg header) | have | PG 20161 |
| `singles-ideas-bastiat-what-is-free-trade-an-adaptation-of-fred` | Frédéric Bastiat | What Is Free Trade? An Adaptation of Frederic Bastiat's "Sophismes Éconimiques" Designed for the American Reader | Alexander Del Mar | (see the Gutenberg header) | have | PG 16106 |
| `singles-ideas-bergson-creative-evolution` | Henri Bergson | Creative Evolution | Arthur Mitchell | (see the Gutenberg header) | have | PG 26163 |
| `singles-ideas-bergson-dreams` | Henri Bergson | Dreams | Edwin E. Slosson | (see the Gutenberg header) | have | PG 20842 |
| `singles-ideas-burckhardt-the-civilisation-of-the-renaissance-in-i` | Jacob Burckhardt | The Civilisation of the Renaissance in Italy | S. G. C. Middlemore | (see the Gutenberg header) | have | PG 2074 |
| `singles-ideas-comenius-the-orbis-pictus` | Johann Amos Comenius | The Orbis Pictus | Charles Hoole | (see the Gutenberg header) | have | PG 28299 |
| `singles-ideas-condorcet-the-first-essay-on-the-political-rights` | Condorcet | The first essay on the political rights of women | Alice Drysdale Vickery | (see the Gutenberg header) | have | PG 31550 |
| `singles-ideas-descartes-selections-from-the-principles-of-philos` | René Descartes | Selections from the Principles of Philosophy | John Veitch | (see the Gutenberg header) | have | PG 4391 |
| `singles-ideas-engels-the-condition-of-the-working-class-in-en` | Friedrich Engels | The Condition of the Working-Class in England in 1844 with a Preface written in 1892 | Florence Kelley | (see the Gutenberg header) | have | PG 17306 |
| `singles-ideas-falckenberg-history-of-modern-philosophy-from-nicola` | Richard Falckenberg | History of Modern Philosophy From Nicolas of Cusa to the Present Time | Andrew Campbell Armstrong | (see the Gutenberg header) | have | PG 11100 |
| `singles-ideas-ibn-tufayl-the-awakening-of-the-soul` | Ibn Tufayl | The Awakening of the Soul | Paul Brönnle | (see the Gutenberg header) | have | PG 34572 |
| `singles-ideas-jellinek-the-declaration-of-the-rights-of-man-and` | Georg Jellinek | The Declaration of the Rights of Man and of Citizens | Max Farrand | (see the Gutenberg header) | have | PG 29815 |
| `singles-ideas-kandinsky-concerning-the-spiritual-in-art` | Wassily Kandinsky | Concerning the Spiritual in Art | Michael Sadleir | (see the Gutenberg header) | have | PG 5321 |
| `singles-ideas-kropotkin-the-place-of-anarchism-in-socialistic-ev` | Petr Alekseevich Kropotkin | The place of anarchism in socialistic evolution | Henry Glasse | (see the Gutenberg header) | have | PG 31104 |
| `singles-ideas-lavoisier-elements-of-chemistry-in-a-new-systemati` | Antoine Laurent Lavoisier | Elements of Chemistry, In a New Systematic Order, Containing all the Modern Discoveries | Robert Kerr | (see the Gutenberg header) | have | PG 30775 |
| `singles-ideas-leonardo-thoughts-on-art-and-life` | Leonardo da Vinci | Thoughts on Art and Life | Maurice Baring | (see the Gutenberg header) | have | PG 29904 |
| `singles-ideas-machiavelli-discourses-on-the-first-decade-of-titus` | Niccolò Machiavelli | Discourses on the First Decade of Titus Livius | Ninian Hill Thomson | (see the Gutenberg header) | have | PG 10827 |
| `singles-ideas-michelet-la-sorciere` | Jules Michelet | La Sorcière: The Witch of the Middle Ages | Lionel J. Trotter | (see the Gutenberg header) | have | PG 31420 |
| `singles-ideas-planck-the-origin-and-development-of-the-quantu` | Max Planck | The Origin and Development of the Quantum Theory | Hans Thacher Clarke and Ludwik Silberstein | (see the Gutenberg header) | have | PG 33663 |
| `singles-ideas-ptahhotep-the-instruction-of-ptah-hotep-and-the-in` | Ptahhotep and Kagemna | The Instruction of Ptah-Hotep and the Instruction of Ke'Gemni The Oldest Books in the World | Battiscombe G. Gunn | (see the Gutenberg header) | have | PG 30508 |
| `singles-ideas-ribot-essay-on-the-creative-imagination` | Th. Ribot | Essay on the Creative Imagination | Albert Heyem Nachmen Baron | (see the Gutenberg header) | have | PG 26430 |
| `singles-ideas-rochefoucauld-reflections` | La Rochefoucauld | Reflections; or Sentences and Moral Maxims | J. Hain Friswell and J. W. Willis Bund | (see the Gutenberg header) | have | PG 9105 |
| `singles-ideas-schlegel-lectures-on-dramatic-art-and-literature` | August Wilhelm von Schlegel | Lectures on Dramatic Art and Literature | John Black | (see the Gutenberg header) | have | PG 7148 |
| `singles-ideas-schopenhauer-essays-of-schopenhauer` | Arthur Schopenhauer | Essays of Schopenhauer | Sara Hay Goddard Dircks | (see the Gutenberg header) | have | PG 11945 |
| `singles-ideas-tarde-underground-man` | Gabriel de Tarde | Underground Man | Cloudesley Brereton | (see the Gutenberg header) | have | PG 33549 |
| `pg-17384` | — | Hilbert's The Foundations of Geometry (Townsend, 1902): Gutenberg publishes this mathematics book only as PDF/LaTeX, with no plain-text file to fetch. Left for a later pass that finds a period scan on the Internet Archive. | — | — | pending | — |
| `pg-21016` | — | Dedekind's Essays on the Theory of Numbers (Beman, 1901): Gutenberg publishes this mathematics book only as PDF/LaTeX, with no plain-text file to fetch. Left for a later pass that finds a period scan on the Internet Archive. | — | — | pending | — |
| `pg-26752` | — | Ramus's The Way to Geometry (Bedwell, 1636): Gutenberg's text file is a stub ('a text version was not prepared'; HTML only, for the diagrams). Left for a later pass that finds a period scan. | — | — | pending | — |

## One-off translations: novels, plays and poems (Lermontov, Pushkin, Mickiewicz, Botchan, Maria Chapdelaine, Huysmans, the Noh plays, Cervantes's Exemplary Novels)

Shelf: `pipeline/singles-literature_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-literature` · titles `python3 pipeline/split_shelf_titles.py singles-literature`.
Round 40 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-literature-azuela-the-underdogs` | Mariano Azuela | The Underdogs: A Novel of the Mexican Revolution | E. Munguía | (see the Gutenberg header) | have | PG 549 |
| `singles-literature-boccaccio-la-fiammetta` | Giovanni Boccaccio | La Fiammetta | James C. Brogan | (see the Gutenberg header) | have | PG 10006 |
| `singles-literature-cattopadhyaya-the-poison-tree` | Bankimacandra Cattopadhyaya | The Poison Tree: A Tale of Hindu Life in Bengal | Miriam S. Knight | (see the Gutenberg header) | have | PG 17455 |
| `singles-literature-certain-noble-plays-of-japan` | Zeami and other Noh playwrights | Certain Noble Plays of Japan: From the manuscripts of Ernest Fenollosa | Ernest Fenollosa | (see the Gutenberg header) | have | PG 8094 |
| `singles-literature-cervantes-the-exemplary-novels-of-cervantes` | Miguel de Cervantes | The Exemplary Novels of Cervantes | Walter K. Kelly | (see the Gutenberg header) | have | PG 14420 |
| `singles-literature-corneille-polyeucte` | Pierre Corneille | Polyeucte | Thomas Constable | (see the Gutenberg header) | have | PG 2543 |
| `singles-literature-daudet-the-nabob` | Alphonse Daudet | The Nabob | W. Blaydes | (see the Gutenberg header) | have | PG 2077 |
| `singles-literature-fontaine-fables-of-la-fontaine-a-new-edition-with` | Jean de La Fontaine | Fables of La Fontaine — a New Edition, with Notes | Elizur Wright | (see the Gutenberg header) | have | PG 7241 |
| `singles-literature-gautier-enamels-and-cameos-and-other-poems` | Théophile Gautier | Enamels and Cameos and other Poems | Agnes Lee | (see the Gutenberg header) | have | PG 29521 |
| `singles-literature-gorky-creatures-that-once-were-men` | Maksim Gorky | Creatures That Once Were Men | J. K. M. Shirazi | (see the Gutenberg header) | have | PG 1466 |
| `singles-literature-heine-poems-and-ballads-of-heinrich-heine` | Heinrich Heine | Poems and Ballads of Heinrich Heine | Emma Lazarus | (see the Gutenberg header) | have | PG 31726 |
| `singles-literature-hemon-maria-chapdelaine` | Louis Hémon | Maria Chapdelaine: A Tale of the Lake St. John Country | W. H. Blake | (see the Gutenberg header) | have | PG 4383 |
| `singles-literature-holberg-comedies-by-holberg` | Ludvig Holberg | Comedies by Holberg : Jeppe of the Hill, The Political Tinker, Erasmus Montanus | Oscar James Campbell and Frederic Schenck | (see the Gutenberg header) | have | PG 5749 |
| `singles-literature-holberg-niels-klim-s-journey-under-the-ground-be` | Ludvig Holberg | Niels Klim's journey under the ground being a narrative of his wonderful descent to the subterranean lands; together with an account of the sensible animals and trees inhabiting the planet Nazar and t | John Gierlow | (see the Gutenberg header) | have | PG 27884 |
| `singles-literature-huysmans-against-the-grain` | J.-K. Huysmans | Against the Grain | John Howard | (see the Gutenberg header) | have | PG 12341 |
| `singles-literature-huysmans-la-bas` | J.-K. Huysmans | Là-bas | Keene Wallis | (see the Gutenberg header) | have | PG 14323 |
| `singles-literature-jacobsen-mogens-and-other-stories` | J. P. Jacobsen | Mogens, and Other Stories | Anna Grabow | (see the Gutenberg header) | have | PG 6765 |
| `singles-literature-kalidasa-the-birth-of-the-war-god` | Kālidāsa | The Birth of the War-God: A Poem by Kálidása | Ralph T. H. Griffith | (see the Gutenberg header) | have | PG 31968 |
| `singles-literature-kartini-letters-of-a-javanese-princess` | Raden Adjeng Kartini | Letters of a Javanese Princess | Agnes Louise Symmers | (see the Gutenberg header) | have | PG 34647 |
| `singles-literature-kochanowski-laments` | Jan Kochanowski | Laments | Dorothea Prall | (see the Gutenberg header) | have | PG 27179 |
| `singles-literature-leopardi-the-poems-of-giacomo-leopardi` | Giacomo Leopardi | The Poems of Giacomo Leopardi | Frederick Townsend | (see the Gutenberg header) | have | PG 19315 |
| `singles-literature-lermontov-a-hero-of-our-time` | Mikhail Iurevich Lermontov | A Hero of Our Time | Marr Murray and J. H. Wisdom | (see the Gutenberg header) | have | PG 913 |
| `singles-literature-lessing-nathan-the-wise` | Gotthold Ephraim Lessing | Nathan the Wise; a dramatic poem in five acts | W. Taylor | (see the Gutenberg header) | have | PG 3820 |
| `singles-literature-loti-an-iceland-fisherman` | Pierre Loti | An Iceland Fisherman | Jules Cambon | (see the Gutenberg header) | have | PG 2196 |
| `singles-literature-maeterlinck-pelleas-and-melisande` | Maurice Maeterlinck | Pélléas and Mélisande; Alladine and Palomides; Home | Richard Hovey | (see the Gutenberg header) | have | PG 13329 |
| `singles-literature-mickiewicz-konrad-wallenrod` | Adam Mickiewicz | Konrad Wallenrod: An Historical Poem | Maude Ashurst Biggs | (see the Gutenberg header) | have | PG 34050 |
| `singles-literature-mickiewicz-pan-tadeusz` | Adam Mickiewicz | Pan Tadeusz; or, The last foray in Lithuania a story of life among Polish gentlefolk in the years 1811 and 1812 | George Rapall Noyes | (see the Gutenberg header) | have | PG 28240 |
| `singles-literature-moliere-amphitryon` | Molière | Amphitryon | A. R. Waller | (see the Gutenberg header) | have | PG 2536 |
| `singles-literature-moliere-the-middle-class-gentleman` | Molière | The Middle-Class Gentleman | Philip Dwight Jones | (see the Gutenberg header) | have | PG 2992 |
| `singles-literature-musset-the-confession-of-a-child-of-the-century` | Alfred de Musset | The Confession of a Child of the Century | Kendall Warren | (see the Gutenberg header) | have | PG 9869 |
| `singles-literature-natsume-botchan-master-darling` | Natsume Sōseki | Botchan (Master Darling) | Yasotaro Mori | (see the Gutenberg header) | have | PG 8868 |
| `singles-literature-nekrasov-who-can-be-happy-and-free-in-russia` | Nikolai Alekseevich Nekrasov | Who Can Be Happy and Free in Russia? | Juliet M. Soskice | (see the Gutenberg header) | have | PG 9619 |
| `singles-literature-novalis-henry-of-ofterdingen` | Novalis | Henry of Ofterdingen: A Romance. | Friedrich von Schlegel and Ludwig Tieck | (see the Gutenberg header) | have | PG 31873 |
| `singles-literature-pushkin-boris-godunov` | Aleksandr Sergeevich Pushkin | Boris Godunov: a drama in verse | Alfred Hayes | (see the Gutenberg header) | have | PG 5089 |
| `singles-literature-pushkin-eugene-oneguine-onegin-a-romance-of-russ` | Aleksandr Sergeevich Pushkin | Eugene Oneguine [Onegin] A Romance of Russian Life in Verse | Henry Spalding | (see the Gutenberg header) | have | PG 23997 |
| `singles-literature-rostand-l-aiglon` | Edmond Rostand | L'Aiglon | Louis Napoleon Parker | (see the Gutenberg header) | have | PG 30012 |
| `singles-literature-saint-pierre-paul-and-virginia-from-the-french-of-j-b` | Bernardin de Saint-Pierre | Paul and Virginia from the French of J.B.H. de Saint Pierre | Helen Maria Williams | (see the Gutenberg header) | have | PG 10859 |
| `singles-literature-sand-mauprat` | George Sand | Mauprat | Stanley Young | (see the Gutenberg header) | have | PG 2194 |
| `singles-literature-schiller-mary-stuart` | Friedrich Schiller | Mary Stuart: A Tragedy | Joseph Charles Mellish | (see the Gutenberg header) | have | PG 6791 |
| `singles-literature-sigurjonsson-modern-icelandic-plays-eyvind-of-the-hil` | Jóhann Sigurjónsson | Modern Icelandic Plays Eyvind of the Hills; The Hraun Farm | Henninge Margrethe Krohn Schanche | (see the Gutenberg header) | have | PG 21937 |
| — | — | pg-30442: Daudet's Letters from My Windmill in the Keith Adams and Mireille Harmelin translation: a modern translation, not a printing before 1931. | — | — | excluded | — |
| — | — | pg-17445: Pumpurs's Bearslayer in Arthur Cropley's translation: a modern translation, not a printing before 1931. | — | — | excluded | — |

## One-off translations: history, exploration and memoir (Bābur-nāma, de Soto, Vasco da Gama, Schiltberger, Garibaldi, Moltke, Slatin, Wace, First World War memoirs)

Shelf: `pipeline/singles-history-travel_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-history-travel` · titles `python3 pipeline/split_shelf_titles.py singles-history-travel`.
Round 41 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-history-travel-a-german-deserter-s-war-experience` | anonymous (a German deserter) | A German deserter's war experience | Julius Koettgen | (see the Gutenberg header) | have | PG 42721 |
| `singles-history-travel-allingham-captain-cuellar-s-adventures-in-connaugh` | Francisco de Cuéllar (ed. Hugh Allingham) | Captain Cuellar's Adventures in Connaught & Ulster A.D. 1588. To Which Is Added an Introduction and Complete Translation of Captain Cuellar's Narrative of the Spanish Armada and His Adventures in Irel | Robert Crawford | (see the Gutenberg header) | have | PG 52472 |
| `singles-history-travel-babur-the-babur-nama-in-english-memoirs-of-bab` | Babur | The Bābur-nāma in English (Memoirs of Bābur) | Annette Susannah Beveridge | (see the Gutenberg header) | have | PG 44608 |
| `singles-history-travel-barine-la-grande-mademoiselle-1627-1652` | Arvède Barine | La Grande Mademoiselle, 1627-1652 | Helene Meyer-Franck | (see the Gutenberg header) | have | PG 50717 |
| `singles-history-travel-baudesson-indo-china-and-its-primitive-people` | Henry Baudesson | Indo-China and its primitive people | E. Appleby Holt | (see the Gutenberg header) | have | PG 45958 |
| `singles-history-travel-celesia-the-conspiracy-of-gianluigi-fieschi-or-g` | Emanuele Celesia | The Conspiracy of Gianluigi Fieschi, or, Genoa in the sixteenth century. | David H. Wheeler | (see the Gutenberg header) | have | PG 50656 |
| `singles-history-travel-charnay-the-ancient-cities-of-the-new-world-bein` | Désiré Charnay | The Ancient Cities of the New World Being Travels and Explorations in Mexico and Central America From 1857-1882 | Helen S. Conant and J. Gonino | (see the Gutenberg header) | have | PG 45656 |
| `singles-history-travel-chevalier-society-manners-and-politics-in-the-unit` | Michel Chevalier | Society, Manners and Politics in the United States Being a Series of Letters on North America | T. G. Bradford | (see the Gutenberg header) | have | PG 45761 |
| `singles-history-travel-danilevskii-the-princess-tarakanova` | G. P. Danilevskii | The Princess Tarakanova: A Dark Chapter of Russian History | Ida de Mouchanoff | (see the Gutenberg header) | have | PG 53580 |
| `singles-history-travel-des-niau-the-history-of-the-devils-of-loudun-volu` | Des Niau | The History of the Devils of Loudun, Volumes I-III The Alleged Possession of the Ursuline Nuns, and the Trial and Execution of Urbain Grandier, Told by an Eye-witness | Edmund Goldsmid | (see the Gutenberg header) | have | PG 45282 |
| `singles-history-travel-duras-prison-journals-during-the-french-revolu` | the Duchesse de Duras | Prison Journals During the French Revolution | Martha Ward Carey | (see the Gutenberg header) | have | PG 46750 |
| `singles-history-travel-elvas-a-narrative-of-the-expedition-of-hernand` | a Gentleman of Elvas | A Narrative of the expedition of Hernando de Soto into Florida published at Evora in 1557 | Richard Hakluyt | (see the Gutenberg header) | have | PG 34997 |
| `singles-history-travel-garibaldi-the-life-of-general-garibaldi-translated` | Giuseppe Garibaldi | The Life of General Garibaldi Translated from his private papers; with the history of his splendid exploits in Rome, Lombardy, Sicily and Naples, to the present time. | Theodore Dwight | (see the Gutenberg header) | have | PG 50544 |
| `singles-history-travel-general-staff-the-war-book-of-the-german-general-staff` | the Prussian Great General Staff | The War Book of the German General Staff Being "The Usages of War on Land" Issued by the Great General Staff of the German Army | J. H. Morgan | (see the Gutenberg header) | have | PG 51646 |
| `singles-history-travel-genevoix-neath-verdun-august-october-1914` | Maurice Genevoix | 'Neath Verdun, August-October, 1914 | H. Grahame Richards | (see the Gutenberg header) | have | PG 46770 |
| `singles-history-travel-gomara-the-pleasant-historie-of-the-conquest-of` | Francisco López de Gómara | The pleasant historie of the conquest of the VVeast India, now called new Spayne atchieued by the vvorthy Prince Hernando Cortes, marques of the Valley of Huaxacac, most delectable to reade | Thomas Nicholas | (see the Gutenberg header) | have | PG 46524 |
| `singles-history-travel-katip-celebi-the-history-of-the-maritime-wars-of-the` | Kâtip Çelebi | The History of the Maritime Wars of the Turks. Chapters I. to IV. | James Mitchell | (see the Gutenberg header) | have | PG 53813 |
| `singles-history-travel-klaczko-two-chancellors` | Julian Klaczko | Two Chancellors: Prince Gortchakof and Prince Bismarck | Frank P. Ward | (see the Gutenberg header) | have | PG 39559 |
| `singles-history-travel-konig-the-voyage-of-the-deutschland` | Paul König | The voyage of the "Deutschland" | Vivien Ellis | (see the Gutenberg header) | have | PG 45922 |
| `singles-history-travel-lauridsen-vitus-bering` | Peter Lauridsen | Vitus Bering: the Discoverer of Bering Strait | Julius E. Olsen | (see the Gutenberg header) | have | PG 46032 |
| `singles-history-travel-leti-il-nipotismo-di-roma-or-the-history-of-t` | Gregorio Leti | Il nipotismo di Roma, or, The History of the Popes Nephews from the time of Sixtus IV. to the death of the last Pope, Alexander VII | William Aglionby | (see the Gutenberg header) | have | PG 54001 |
| `singles-history-travel-loher-cyprus` | Franz von Löher | Cyprus: Historical and Descriptive | A. Batson Joyner | (see the Gutenberg header) | have | PG 47056 |
| `singles-history-travel-mardiganian-ravished-armenia-the-story-of-aurora-mar` | Aurora Mardiganian | Ravished Armenia The Story of Aurora Mardiganian, the Christian Girl Who Lived Through the Great Massacres | H. L. Gates | (see the Gutenberg header) | have | PG 53046 |
| `singles-history-travel-mertens-an-account-of-the-plague-which-raged-at` | Charles de Mertens | An account of the plague which raged at Moscow, in 1771 | Richard Pearson | (see the Gutenberg header) | have | PG 49567 |
| `singles-history-travel-mitre-the-emancipation-of-south-america` | Bartolomé Mitre | The Emancipation of South America | William Pilling | (see the Gutenberg header) | have | PG 48856 |
| `singles-history-travel-moltke-the-franco-german-war-of-1870-71` | Helmuth von Moltke | The Franco-German War of 1870-71 | Archibald Forbes | (see the Gutenberg header) | have | PG 36209 |
| `singles-history-travel-mucke-the-ayesha-being-the-adventures-of-the-l` | Hellmuth von Mücke | The "Ayesha," being the adventures of the landing squad of the "Emden" | Helene S. White | (see the Gutenberg header) | have | PG 45878 |
| `singles-history-travel-noldeke-sketches-from-eastern-history` | Theodor Nöldeke | Sketches from Eastern History | J. Sutherland Black | (see the Gutenberg header) | have | PG 54782 |
| `singles-history-travel-pluschow-my-escape-from-donington-hall-preceded-b` | Gunther Plüschow | My Escape from Donington Hall, Preceded by an Account of the Siege of Kiao-Chow in 1915 | Pauline De Chary | (see the Gutenberg header) | have | PG 49264 |
| `singles-history-travel-politovskii-from-libau-to-tsushima-a-narrative-of-th` | Evgenii Politovsky | From Libau to Tsushima A narrative of the voyage of Admiral Rojdestvensky's fleet to eastern seas, including a detailed account of the Dogger Bank incident | Frederick Rowlandson Godfrey | (see the Gutenberg header) | have | PG 49735 |
| `singles-history-travel-reitlinger-a-diplomat-s-memoir-of-1870-being-the-ac` | Frederic Reitlinger | A Diplomat's Memoir of 1870 being the account of a balloon escape from the siege of Paris and a political mission to London and Vienna | Henry Scipio Reitlinger | (see the Gutenberg header) | have | PG 49546 |
| `singles-history-travel-richthofen-the-red-battle-flyer` | Manfred von Richthofen | The Red Battle Flyer | J. Ellis Barker | (see the Gutenberg header) | have | PG 41159 |
| `singles-history-travel-sakurai-human-bullets` | Tadayoshi Sakurai | Human Bullets: A Soldier's Story of Port Arthur | Masujiro Honda | (see the Gutenberg header) | have | PG 47548 |
| `singles-history-travel-schiltberger-the-bondage-and-travels-of-johann-schilt` | Johannes Schiltberger | The Bondage and Travels of Johann Schiltberger, a Native of Bavaria, in Europe, Asia, and Africa, 1396-1427 | J. Buchan Telfer | (see the Gutenberg header) | have | PG 52569 |
| `singles-history-travel-schimmer-the-sieges-of-vienna-by-the-turks` | Karl August Schimmer | The Sieges of Vienna by the Turks | Francis Egerton Ellesmere | (see the Gutenberg header) | have | PG 54731 |
| `singles-history-travel-schwink-ypres-1914` | Otto Schwink | Ypres 1914: An Official Account Published by Order of the German General Staff | G. C. Wynne | (see the Gutenberg header) | have | PG 44234 |
| `singles-history-travel-slatin-fire-and-sword-in-the-sudan-a-personal-n` | Rudolf Slatin | Fire and Sword in the Sudan A Personal Narrative of Fighting and Serving the Dervishes 1879-1895 | F. R. Wingate | (see the Gutenberg header) | have | PG 41035 |
| `singles-history-travel-turpin-history-of-the-kingdom-of-siam-and-of-th` | F. H. Turpin | History of the Kingdom of Siam and of the revolutions that have caused the overthrow of the empire, up to A.D. 1770 | B. O. Cartwright | (see the Gutenberg header) | have | PG 44564 |
| `singles-history-travel-velho-a-journal-of-the-first-voyage-of-vasco-d` | Álvaro Velho (attributed) | A Journal of the First Voyage of Vasco da Gama 1497-1499 | Ernest Georg Ravenstein | (see the Gutenberg header) | have | PG 46440 |
| `singles-history-travel-vertot-the-revolutions-of-portugal` | abbé de Vertot | The Revolutions of Portugal | Gabriel Roussillon | (see the Gutenberg header) | have | PG 43852 |
| `singles-history-travel-villari-the-two-first-centuries-of-florentine-hi` | Pasquale Villari | The Two First Centuries of Florentine History The Republic and Parties at the Time of Dante. Fourth Impression. | Linda Villari | (see the Gutenberg header) | have | PG 45469 |
| `singles-history-travel-wace-master-wace-his-chronicle-of-the-norman` | Wace | Master Wace, His Chronicle of the Norman Conquest From the Roman De Rou | Edgar Taylor | (see the Gutenberg header) | have | PG 41163 |
| `singles-history-travel-wilhelm-ii-the-kaiser-s-memoirs` | Kaiser Wilhelm II | The Kaiser's Memoirs | T. R. Ybarra | (see the Gutenberg header) | have | PG 43522 |
| `singles-history-travel-zwaardecroon-memoir-of-hendrick-zwaardecroon-commande` | Hendrick Zwaardecroon | Memoir of Hendrick Zwaardecroon, commandeur of Jaffnapatam (afterwards Governor-General of Nederlands India) 1697. For the guidance of the council of Jaffnapatam, during his absence at the coast of Ma | Sophia Pieters | (see the Gutenberg header) | have | PG 40579 |

## One-off translations: science, medicine and crafts (De Re Metallica, Galileo, Goethe's Theory of Colours, Petrus Peregrinus, Montessori, Poincaré, lithography, Lavater's ghosts)

Shelf: `pipeline/singles-science-craft_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-science-craft` · titles `python3 pipeline/split_shelf_titles.py singles-science-craft`.
Round 41 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-science-craft-agricola-de-re-metallica-translated-from-the-firs` | Georg Agricola | De Re Metallica, Translated from the First Latin Edition of 1556 | Herbert Hoover and Lou Henry Hoover | (see the Gutenberg header) | have | PG 38015 |
| `singles-science-craft-bazancourt-secrets-of-the-sword` | César de Bazancourt | Secrets of the Sword | Charles Felix Clay | (see the Gutenberg header) | have | PG 46093 |
| `singles-science-craft-bilguer-a-dissertation-on-the-inutility-of-the-a` | Johann Ulrich Bilguer | A dissertation on the inutility of the amputation of limbs | S. A. D. Tissot | (see the Gutenberg header) | have | PG 44089 |
| `singles-science-craft-binet-mentally-defective-children` | Alfred Binet and Théodore Simon | Mentally Defective Children | William Blackley Drummond | (see the Gutenberg header) | have | PG 36458 |
| `singles-science-craft-bouchot-the-printed-book` | Henri Bouchot | The Printed Book: Its History, Illustration and Adornment From the Days of Gutenberg to the Present Time | E. C. Bigmore | (see the Gutenberg header) | have | PG 44890 |
| `singles-science-craft-bourgelat-a-new-system-of-horsemanship` | Claude Bourgelat | A New System of Horsemanship | Richard Berenger | (see the Gutenberg header) | have | PG 46696 |
| `singles-science-craft-braune-a-gothic-grammar-with-selections-for-rea` | Wilhelm Braune | A Gothic Grammar, with selections for reading and a glossary | G. H. Balg | (see the Gutenberg header) | have | PG 50336 |
| `singles-science-craft-calmette-venoms` | A. Calmette | Venoms: Venomous Animals and Antivenomous Serum-therapeutics | E. E. Austen | (see the Gutenberg header) | have | PG 51078 |
| `singles-science-craft-comte-the-philosophy-of-mathematics` | Auguste Comte | The philosophy of mathematics | W. M. Gillespie | (see the Gutenberg header) | have | PG 39702 |
| `singles-science-craft-delaborde-engraving` | Henri Delaborde | Engraving: Its Origin, Processes, and History | Robert Alan Mowbray Stevenson | (see the Gutenberg header) | have | PG 42936 |
| `singles-science-craft-dunant-the-origin-of-the-red-cross` | Henry Dunant | The Origin of the Red Cross: "Un souvenir de Solferino" | Anna B. Heylin Wright | (see the Gutenberg header) | have | PG 50968 |
| `singles-science-craft-ebbinghaus-psychology` | Hermann Ebbinghaus | Psychology: an elementary text-book | Max F. Meyer | (see the Gutenberg header) | have | PG 52823 |
| `singles-science-craft-flammarion-urania` | Camille Flammarion | Urania | Augusta Rice Stetson | (see the Gutenberg header) | have | PG 41941 |
| `singles-science-craft-forel-ants-and-some-other-insects` | Auguste Forel | Ants and Some Other Insects: An Inquiry Into the Psychic Powers of These Animals | William Morton Wheeler | (see the Gutenberg header) | have | PG 52134 |
| `singles-science-craft-galilei-a-discourse-presented-to-the-most-serene` | Galileo Galilei | A Discourse Presented to the Most Serene Don Cosimo II., Great Duke of Tuscany, Concerning the Natation of Bodies Vpon, and Submersion In, the Water. | Thomas Salusbury | (see the Gutenberg header) | have | PG 37729 |
| `singles-science-craft-galilei-the-sidereal-messenger-of-galileo-galile` | Galileo Galilei and Johannes Kepler | The sidereal messenger of Galileo Galilei | Edward Stafford Carlos | (see the Gutenberg header) | have | PG 46036 |
| `singles-science-craft-gannal-history-of-embalming-and-of-preparations` | J.-N. Gannal | History of Embalming and of Preparations in Anatomy, Pathology, and Natural History; Including an Account of a New Process for Embalming | Richard Harlan | (see the Gutenberg header) | have | PG 48078 |
| `singles-science-craft-goethe-goethe-s-theory-of-colours` | Johann Wolfgang von Goethe | Goethe's Theory of Colours | Charles Lock Eastlake | (see the Gutenberg header) | have | PG 50572 |
| `singles-science-craft-halfer-the-progress-of-the-marbling-art-from-te` | Josef Halfer | The progress of the marbling art, from technical scientific principles | Herman Dieck | (see the Gutenberg header) | have | PG 41241 |
| `singles-science-craft-herbart-outlines-of-educational-doctrine` | Johann Friedrich Herbart | Outlines of Educational Doctrine | Alexis Frederick Lange | (see the Gutenberg header) | have | PG 44905 |
| `singles-science-craft-jespersen-how-to-teach-a-foreign-language` | Otto Jespersen | How to teach a foreign language | Sophia Yhlen-Olsen Bertelsen | (see the Gutenberg header) | have | PG 54943 |
| `singles-science-craft-la-mettrie-man-a-machine` | Julien Offray de La Mettrie | Man a Machine | Gertrude Carman Bussey | (see the Gutenberg header) | have | PG 52090 |
| `singles-science-craft-lavater-of-ghostes-and-spirites-walking-by-night` | Ludwig Lavater | Of Ghostes and Spirites, Walking by Night And of Straunge Noyses, Crackes, and Sundrie Forewarnings, Which Commonly Happen Before the Death of Men: Great Slaughters, and Alterations of Kingdoms | Robert Harrison | (see the Gutenberg header) | have | PG 51038 |
| `singles-science-craft-magnus-superstition-in-medicine` | Hugo Magnus | Superstition in Medicine | Julius L. Salinger | (see the Gutenberg header) | have | PG 44744 |
| `singles-science-craft-mathot-gas-engines-and-producer-gas-plants-a-pr` | Rodolphe Edgard Mathot | Gas-Engines and Producer-Gas Plants A Practice Treatise Setting Forth the Principles of Gas-Engines and Producer Design, the Selection and Installation of an Engine, Conditions of Perfect Operation, P | Waldemar Kaempffert | (see the Gutenberg header) | have | PG 38415 |
| `singles-science-craft-meige-tics-and-their-treatment` | Henry Meige and E. Feindel | Tics and Their Treatment | S. A. Kinnier Wilson | (see the Gutenberg header) | have | PG 39822 |
| `singles-science-craft-montessori-the-montessori-method-scientific-pedagog` | Maria Montessori | The Montessori Method Scientific Pedagogy as Applied to Child Education in 'The Children's Houses' with Additions and Revisions by the Author | Anne E. George | (see the Gutenberg header) | have | PG 39863 |
| `singles-science-craft-oken-elements-of-physiophilosophy` | Lorenz Oken | Elements of Physiophilosophy | Alfred Tulk | (see the Gutenberg header) | have | PG 49196 |
| `singles-science-craft-paulli-a-treatise-on-tobacco-tea-coffee-and-cho` | Simon Paulli | A Treatise on Tobacco, Tea, Coffee, and Chocolate | R. James | (see the Gutenberg header) | have | PG 53027 |
| `singles-science-craft-peregrinus-the-letter-of-petrus-peregrinus-on-the-m` | Petrus Peregrinus (Pierre de Maricourt) | The Letter of Petrus Peregrinus on the Magnet, A.D. 1269 | Brother Arnold | (see the Gutenberg header) | have | PG 50524 |
| `singles-science-craft-pfaundler-international-language-and-science-consi` | Leopold Pfaundler and others | International Language and Science Considerations on the Introduction of an International Language into Science | F. G. Donnan | (see the Gutenberg header) | have | PG 54694 |
| `singles-science-craft-poincare-the-foundations-of-science` | Henri Poincaré | The Foundations of Science: Science and Hypothesis, The Value of Science, Science and Method | George Bruce Halsted | (see the Gutenberg header) | have | PG 39713 |
| `singles-science-craft-rathgen-the-preservation-of-antiquities` | Friedrich Rathgen | The preservation of antiquities | George A. Auden and Harold Allden Auden | (see the Gutenberg header) | have | PG 46851 |
| `singles-science-craft-senefelder-the-invention-of-lithography` | Alois Senefelder | The Invention of Lithography | J. W. Muller | (see the Gutenberg header) | have | PG 40924 |
| `singles-science-craft-tissot-advice-to-the-people-in-general-with-reg` | S. A. D. Tissot | Advice to the people in general, with regard to their health | J. Kirkpatrick | (see the Gutenberg header) | have | PG 39044 |
| `singles-science-craft-vallery-radot-louis-pasteur` | René Vallery-Radot | Louis Pasteur: His Life and Labours | Elizabeth Emma Proby Hamilton | (see the Gutenberg header) | have | PG 47505 |
| `singles-science-craft-vigenere-a-discovrse-of-fire-and-salt-discovering` | Blaise de Vigenère | A Discovrse of Fire and Salt Discovering Many Secret Mysteries as well Philosophicall, as Theologicall | Edward Stephens | (see the Gutenberg header) | have | PG 47365 |
| `singles-science-craft-wundt-an-introduction-to-psychology-translated` | Wilhelm Wundt | An Introduction to Psychology Translated from the Second German Edition | Rudolf Pintner | (see the Gutenberg header) | have | PG 46677 |
| `singles-science-craft-wundt-elements-of-folk-psychology-outline-of-a` | Wilhelm Wundt | Elements of Folk Psychology Outline of a Psychological History of the Development of Mankind | Edward L. Schaub | (see the Gutenberg header) | have | PG 44138 |
| `singles-science-craft-einstein` | Albert Einstein | The Meaning of Relativity: Four Lectures Delivered at Princeton University, May 1921 | Edwin Plimpton Adams | 1922 | have-raw | IA `meaningofrelativ00eins` |
| `singles-science-craft-gauss` | Carl Friedrich Gauss | General Investigations of Curved Surfaces of 1827 and 1825 | James Caddall Morehead and Adam Miller Hiltebeitel | 1902 | have-raw | IA `generalinvestiga00gausuoft` |
| `singles-science-craft-klein` | Felix Klein | On Riemann's Theory of Algebraic Functions and their Integrals | Frances Hardcastle | 1893 | have-raw | IA `onriemannstheory00kleiuoft` |
| `singles-science-craft-planck-lectures` | Max Planck | Eight Lectures on Theoretical Physics, Delivered at Columbia University in 1909 | A. P. Wills | 1915 | have-raw | IA `eightlecturesont00planuoft` |
| `singles-science-craft-planck-radiation` | Max Planck | The Theory of Heat Radiation | Morton Masius | 1914 | have-raw | IA `theoryofheatradi00planrich` |
| `singles-science-craft-planck-thermo` | Max Planck | Treatise on Thermodynamics | Alexander Ogg | 1903 | have-raw | IA `treatiseonthermo00planuoft` |

## One-off translations: more philosophy, religion and politics (Durkheim, Engels, Kant, Grotius, Pascal, Schopenhauer, Croce, Trotsky, Petrarch, Galateo)

Shelf: `pipeline/singles-ideas-2_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-ideas-2` · titles `python3 pipeline/split_shelf_titles.py singles-ideas-2`.
Round 41 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-ideas-2-annet-critical-examination-of-the-life-of-st-p` | Peter Annet | Critical Examination of the Life of St. Paul | Paul Henri Thiry Holbach | (see the Gutenberg header) | have | PG 38102 |
| `singles-ideas-2-bebel-woman-and-socialism` | August Bebel | Woman and Socialism | Meta Stern Lilienthal | (see the Gutenberg header) | have | PG 47244 |
| `singles-ideas-2-beer-the-life-and-teaching-of-karl-marx` | Max Beer | The life and teaching of Karl Marx | T. C. Partington and H. J. Stenning | (see the Gutenberg header) | have | PG 37290 |
| `singles-ideas-2-brentano-the-origin-of-the-knowledge-of-right-and` | Franz Brentano | The Origin of the Knowledge of Right and Wrong | Cecil Hague | (see the Gutenberg header) | have | PG 49228 |
| `singles-ideas-2-comte-a-general-view-of-positivism-or-summary` | Auguste Comte | A General View of Positivism Or, Summary exposition of the System of Thought and Life | John Henry Bridges | (see the Gutenberg header) | have | PG 53799 |
| `singles-ideas-2-cousin-lectures-on-the-true-the-beautiful-and-t` | Victor Cousin | Lectures on the true, the beautiful and the good | O. W. Wight | (see the Gutenberg header) | have | PG 36208 |
| `singles-ideas-2-croce-historical-materialism-and-the-economics` | Benedetto Croce | Historical materialism and the economics of Karl Marx | Christabel M. Meredith | (see the Gutenberg header) | have | PG 39653 |
| `singles-ideas-2-croce-the-philosophy-of-giambattista-vico` | Benedetto Croce | The Philosophy of Giambattista Vico | R. G. Collingwood | (see the Gutenberg header) | have | PG 52814 |
| `singles-ideas-2-della-casa-a-renaissance-courtesy-book` | Giovanni Della Casa | A Renaissance Courtesy-book: Galateo of Manners & Behaviours | Robert Peterson | (see the Gutenberg header) | have | PG 47993 |
| `singles-ideas-2-drews-the-christ-myth` | Arthur Drews | The Christ Myth | C. Delisle Burns | (see the Gutenberg header) | have | PG 45540 |
| `singles-ideas-2-durkheim-the-elementary-forms-of-the-religious-li` | Émile Durkheim | The Elementary Forms of the Religious Life | Joseph Ward Swain | (see the Gutenberg header) | have | PG 41360 |
| `singles-ideas-2-engels-socialism-utopian-and-scientific` | Friedrich Engels | Socialism, Utopian and Scientific | Edward B. Aveling | (see the Gutenberg header) | have | PG 39257 |
| `singles-ideas-2-eucken-ethics-and-modern-thought` | Rudolf Eucken | Ethics and Modern Thought: A Theory of Their Relations | Margaret von Seydewitz | (see the Gutenberg header) | have | PG 43405 |
| `singles-ideas-2-eucken-life-s-basis-and-life-s-ideal` | Rudolf Eucken | Life's Basis and Life's Ideal: The Fundamentals of a New Philosophy of Life | Alban G. Widgery | (see the Gutenberg header) | have | PG 43719 |
| `singles-ideas-2-fenelon-fenelon-s-treatise-on-the-education-of-d` | Fénelon | Fenelon's Treatise on the Education of Daughters Translated from the French, and Adapted to English Readers | Thomas Frognall Dibdin | (see the Gutenberg header) | have | PG 47621 |
| `singles-ideas-2-gentile-the-reform-of-education` | Giovanni Gentile | The Reform of Education | Dino Bigongiari | (see the Gutenberg header) | have | PG 36762 |
| `singles-ideas-2-goldziher-mythology-among-the-hebrews-and-its-hist` | Ignác Goldziher | Mythology among the Hebrews and Its Historical Development | R. Martineau | (see the Gutenberg header) | have | PG 48967 |
| `singles-ideas-2-grotius-the-rights-of-war-and-peace` | Hugo Grotius | The Rights of War and Peace | A. C. Campbell | (see the Gutenberg header) | have | PG 46564 |
| `singles-ideas-2-halevy-the-life-of-friedrich-nietzsche` | Daniel Halévy | The life of Friedrich Nietzsche | Joseph M. Hone | (see the Gutenberg header) | have | PG 53620 |
| `singles-ideas-2-holbach-christianity-unveiled-being-an-examinati` | Paul Henri Thiry Holbach | Christianity Unveiled Being an Examination of the Principles and Effects of the Christian Religion | W. M. Johnson | (see the Gutenberg header) | have | PG 40770 |
| `singles-ideas-2-janet-elements-of-morals-with-special-applicat` | Paul Janet | Elements of Morals With Special Application of the Moral Law to the Duties of the Individual and of Society and the State | Caroline Rollin Corson | (see the Gutenberg header) | have | PG 37016 |
| `singles-ideas-2-kant-kant-s-critique-of-judgement` | Immanuel Kant | Kant's Critique of Judgement | J. H. Bernard | (see the Gutenberg header) | have | PG 48433 |
| `singles-ideas-2-kant-perpetual-peace` | Immanuel Kant | Perpetual Peace: A Philosophical Essay | Mary Campbell Smith | (see the Gutenberg header) | have | PG 50922 |
| `singles-ideas-2-leopardi-essays-and-dialogues` | Giacomo Leopardi | Essays and Dialogues | Charles Edwardes | (see the Gutenberg header) | have | PG 52356 |
| `singles-ideas-2-liebknecht-the-future-belongs-to-the-people` | Karl Liebknecht | The Future Belongs to the People | Savel Zimand | (see the Gutenberg header) | have | PG 39023 |
| `singles-ideas-2-maimon-solomon-maimon` | Solomon Maimon | Solomon Maimon: An Autobiography. | John Clark Murray | (see the Gutenberg header) | have | PG 41042 |
| `singles-ideas-2-maniri-letters-from-a-sufi-teacher` | Sharafuddin Maneri | Letters from a Sûfî Teacher | Baijnath Singh | (see the Gutenberg header) | have | PG 47749 |
| `singles-ideas-2-maxwell-metapsychical-phenomena` | J. Maxwell | Metapsychical phenomena | L. I. Finch | (see the Gutenberg header) | have | PG 46942 |
| `singles-ideas-2-nordau-morals-and-the-evolution-of-man` | Max Nordau | Morals and the Evolution of Man | Marie Adèle Lewenz | (see the Gutenberg header) | have | PG 37998 |
| `singles-ideas-2-oppenheimer-the-state` | Franz Oppenheimer | The State: Its History and Development Viewed Sociologically | John M. Gitterman | (see the Gutenberg header) | have | PG 51544 |
| `singles-ideas-2-pascal-the-thoughts-of-blaise-pascal` | Blaise Pascal | The Thoughts of Blaise Pascal | C. Kegan Paul | (see the Gutenberg header) | have | PG 46921 |
| `singles-ideas-2-petrarca-petrarch-s-letters-to-classical-authors` | Francesco Petrarca | Petrarch's Letters to Classical Authors | Mario Emilio Cosenza | (see the Gutenberg header) | have | PG 47859 |
| `singles-ideas-2-petrarca-petrarch-s-secret` | Francesco Petrarca | Petrarch's Secret; or, the Soul's Conflict with Passion Three Dialogues Between Himself and S. Augustine | William H. Draper | (see the Gutenberg header) | have | PG 49450 |
| `singles-ideas-2-reville-lectures-on-the-origin-and-growth-of-rel` | Albert Réville | Lectures on the Origin and Growth of Religion as Illustrated by the Native Religions of Mexico and Peru | Philip H. Wicksteed | (see the Gutenberg header) | have | PG 34804 |
| `singles-ideas-2-schopenhauer-on-the-fourfold-root-of-the-principle-of` | Arthur Schopenhauer | On the Fourfold Root of the Principle of Sufficient Reason, and On the Will in Nature: Two Essays (revised edition) | Karl Hillebrand | (see the Gutenberg header) | have | PG 50966 |
| `singles-ideas-2-schopenhauer-the-basis-of-morality` | Arthur Schopenhauer | The Basis of Morality | Arthur Brodrick Bullock | (see the Gutenberg header) | have | PG 44929 |
| `singles-ideas-2-schwegler-a-history-of-philosophy-in-epitome` | Albert Schwegler | A History of Philosophy in Epitome | Julius H. Seelye | (see the Gutenberg header) | have | PG 41412 |
| `singles-ideas-2-sombart-socialism-and-the-social-movement-in-the` | Werner Sombart | Socialism and the Social Movement in the 19th Century | Anson Phelps Atterbury | (see the Gutenberg header) | have | PG 35210 |
| `singles-ideas-2-steiner-the-way-of-initiation` | Rudolf Steiner | The Way of Initiation; or, How to Attain Knowledge of the Higher Worlds | Max Gysi | (see the Gutenberg header) | have | PG 39986 |
| `singles-ideas-2-stendhal-on-love` | Stendhal | On Love | Cecil N. Sidney Woolf and Philip Sidney Woolf | (see the Gutenberg header) | have | PG 53720 |
| `singles-ideas-2-trotsky-our-revolution` | Leon Trotsky | Our Revolution: Essays on Working-Class and International Revolution, 1904-1917 | Moissaye J. Olgin | (see the Gutenberg header) | have | PG 36303 |

## One-off translations: nineteenth-century continental fiction (Auerbach, Heyse, Spielhagen, E. Werner, Jókai, Bjørnson, De Coster, Mann's Royal Highness, Hugo, Laclos, Gourmont)

Shelf: `pipeline/singles-continental-fiction_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-continental-fiction` · titles `python3 pipeline/split_shelf_titles.py singles-continental-fiction`.
Round 42 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-continental-fiction-aimard-the-missouri-outlaws` | Gustave Aimard | The Missouri Outlaws | Percy B. St. John | (see the Gutenberg header) | have | PG 44574 |
| `singles-continental-fiction-auerbach-black-forest-village-stories` | Berthold Auerbach | Black Forest Village Stories | Charles Goepp | (see the Gutenberg header) | have | PG 32517 |
| `singles-continental-fiction-auerbach-landolin` | Berthold Auerbach | Landolin | Annie B. Irish | (see the Gutenberg header) | have | PG 33008 |
| `singles-continental-fiction-auerbach-villa-eden` | Berthold Auerbach | Villa Eden: The Country-House on the Rhine | Charles C. Shackford | (see the Gutenberg header) | have | PG 32902 |
| `singles-continental-fiction-bazan-the-mystery-of-the-lost-dauphin-louis-xv` | Emilia Pardo Bazán | The Mystery of the Lost Dauphin (Louis XVII) | Annabel Hord Seeger | (see the Gutenberg header) | have | PG 41509 |
| `singles-continental-fiction-bergerac-a-voyage-to-the-moon` | Cyrano de Bergerac | A Voyage to the Moon | Archibald Lovell | (see the Gutenberg header) | have | PG 46547 |
| `singles-continental-fiction-bjornson-arne` | Bjørnstjerne Bjørnson | Arne: A Sketch of Norwegian Country Life | Augusta Plesner and Susan Rugeley-Powers | (see the Gutenberg header) | have | PG 35246 |
| `singles-continental-fiction-bjornson-in-god-s-way` | Bjørnstjerne Bjørnson | In God's Way: A Novel | Elizabeth Carmichael | (see the Gutenberg header) | have | PG 37726 |
| `singles-continental-fiction-brouwer-akbar` | P. A. S. van Limburg Brouwer | Akbar: An Eastern Romance | M. M. | (see the Gutenberg header) | have | PG 40155 |
| `singles-continental-fiction-coster-flemish-legends` | Charles de Coster | Flemish Legends | Harold Taylor | (see the Gutenberg header) | have | PG 37668 |
| `singles-continental-fiction-coster-the-legend-of-the-glorious-adventures-of` | Charles de Coster | The Legend of the Glorious Adventures of Tyl Ulenspiegel in the land of Flanders and elsewhere | Geoffrey Arundel Whitworth | (see the Gutenberg header) | have | PG 37599 |
| `singles-continental-fiction-couperus-psyche` | Louis Couperus | Psyche | Benjamin Shepherd Berrington | (see the Gutenberg header) | have | PG 38005 |
| `singles-continental-fiction-dahn-saga-of-halfred-the-sigskald` | Felix Dahn | Saga of Halfred the Sigskald: A Northern Tale of the Tenth Century | Sophie F. F. Veitch | (see the Gutenberg header) | have | PG 32443 |
| `singles-continental-fiction-dumas-the-prussian-terror` | Alexandre Dumas | The Prussian Terror | R. S. Garnett | (see the Gutenberg header) | have | PG 36016 |
| `singles-continental-fiction-eeden-the-quest-the-authorized-translation-fro` | Frederik van Eeden | The Quest The authorized translation from the Dutch of De kleine Johannes | Laura Ward Cole | (see the Gutenberg header) | have | PG 40657 |
| `singles-continental-fiction-filon-garrick-s-pupil` | Augustin Filon | Garrick's Pupil | J. V. Prichard | (see the Gutenberg header) | have | PG 35023 |
| `singles-continental-fiction-franzos-judith-trachtenberg` | Karl Emil Franzos | Judith Trachtenberg: A Novel | Charlton Thomas Lewis and L. P. Lewis | (see the Gutenberg header) | have | PG 36937 |
| `singles-continental-fiction-franzos-the-chief-justice` | Karl Emil Franzos | The Chief Justice: A Novel | Miles Corbet | (see the Gutenberg header) | have | PG 36854 |
| `singles-continental-fiction-gerstacker-the-wanderings-and-fortunes-of-some-germ` | Friedrich Gerstäcker | The wanderings and fortunes of some German emigrants | David Black | (see the Gutenberg header) | have | PG 42672 |
| `singles-continental-fiction-gourmont-a-virgin-heart` | Remy de Gourmont | A Virgin Heart: A Novel | Aldous Huxley | (see the Gutenberg header) | have | PG 44384 |
| `singles-continental-fiction-gourmont-very-woman-sixtine` | Remy de Gourmont | Very woman (Sixtine) | J. L. Barrets | (see the Gutenberg header) | have | PG 45920 |
| `singles-continental-fiction-guerrazzi-isabella-orsini` | Francesco Domenico Guerrazzi | Isabella Orsini: A Historical Novel of the Fifteenth Century | Luigi Monti | (see the Gutenberg header) | have | PG 46967 |
| `singles-continental-fiction-harting-anno-domini-2071-translated-from-the-dut` | Pieter Harting | Anno Domini 2071 Translated from the Dutch Original | Alexander V. W. Bikkers | (see the Gutenberg header) | have | PG 45350 |
| `singles-continental-fiction-hausrath-klytia` | Adolf Hausrath | Klytia: A Story of Heidelberg Castle | Sutton Fraser Corkran | (see the Gutenberg header) | have | PG 33133 |
| `singles-continental-fiction-heimburg-gertrude-s-marriage` | W. Heimburg | Gertrude's Marriage | J. W. Davis | (see the Gutenberg header) | have | PG 32442 |
| `singles-continental-fiction-heyse-a-divided-heart-and-other-stories` | Paul Heyse | A divided heart, and other stories | Constance Stewart Copeland | (see the Gutenberg header) | have | PG 34102 |
| `singles-continental-fiction-heyse-at-the-ghost-hour-the-house-of-the-unbel` | Paul Heyse | At the Ghost Hour. The House of the Unbelieving Thomas | Frances A. Van Santford | (see the Gutenberg header) | have | PG 33878 |
| `singles-continental-fiction-heyse-barbarossa-and-other-tales` | Paul Heyse | Barbarossa, and Other Tales | L. C. S. | (see the Gutenberg header) | have | PG 33789 |
| `singles-continental-fiction-heyse-four-phases-of-love` | Paul Heyse | Four Phases of Love | G. H. Kingsley | (see the Gutenberg header) | have | PG 34104 |
| `singles-continental-fiction-hugo-toilers-of-the-sea` | Victor Hugo | Toilers of the sea | W. Moy Thomas | (see the Gutenberg header) | have | PG 32338 |
| `singles-continental-fiction-ibanez-the-cabin-la-barraca` | Vicente Blasco Ibáñez | The Cabin [La barraca] | Beatrice M. Mekota and Francis Haffkine Snow | (see the Gutenberg header) | have | PG 38165 |
| `singles-continental-fiction-ibanez-the-enemies-of-women-los-enemigos-de-la` | Vicente Blasco Ibáñez | The Enemies of Women (Los enemigos de la mujer) | Irving Brown | (see the Gutenberg header) | have | PG 38458 |
| `singles-continental-fiction-ingemann-the-childhood-of-king-erik-menved` | Bernhard Severin Ingemann | The Childhood of King Erik Menved: An Historical Romance | John Kesson | (see the Gutenberg header) | have | PG 36626 |
| `singles-continental-fiction-jokai-black-diamonds` | Mór Jókai | Black Diamonds: A Novel | Frances A. Gerard | (see the Gutenberg header) | have | PG 32668 |
| `singles-continental-fiction-jokai-in-love-with-the-czarina-and-other-stori` | Mór Jókai | In Love With the Czarina, and Other Stories | Louis Felbermann | (see the Gutenberg header) | have | PG 34574 |
| `singles-continental-fiction-jokai-the-strange-story-of-rab-raby` | Mór Jókai | The Strange Story of Rab Ráby | Emil Reich | (see the Gutenberg header) | have | PG 36739 |
| `singles-continental-fiction-jokai-the-yellow-rose` | Mór Jókai | The yellow rose | Beatrice Danford | (see the Gutenberg header) | have | PG 34911 |
| `singles-continental-fiction-keller-seven-legends` | Gottfried Keller | Seven Legends | Martin Wyness | (see the Gutenberg header) | have | PG 34504 |
| `singles-continental-fiction-kock-the-barber-of-paris` | Paul de Kock | The Barber of Paris | Edith Mary Norris | (see the Gutenberg header) | have | PG 37453 |
| `singles-continental-fiction-kohn-gabriel` | S. Kohn | Gabriel: A Story of the Jews in Prague | Arthur Milman | (see the Gutenberg header) | have | PG 36855 |
| `singles-continental-fiction-kraszewski-the-jew` | Józef Ignacy Kraszewski | The Jew | Linda Da Kowalewska | (see the Gutenberg header) | have | PG 37621 |
| `singles-continental-fiction-laclos-dangerous-connections-v-1-2-3-4-a-series` | Choderlos de Laclos | Dangerous Connections, v. 1, 2, 3, 4 A Series of Letters, selected from the Correspondence of a Private Circle; and Published for the Instruction of Society. | Thomas Moore | (see the Gutenberg header) | have | PG 45512 |
| `singles-continental-fiction-leblanc-arsene-lupin-versus-herlock-sholmes` | Maurice Leblanc | Arsène Lupin versus Herlock Sholmes | George Morehead | (see the Gutenberg header) | have | PG 40203 |
| `singles-continental-fiction-mamin-siberiak-verotchka-s-tales` | D. N. Mamin-Siberiak | Verotchka's Tales | Ray Davidson | (see the Gutenberg header) | have | PG 35036 |
| `singles-continental-fiction-mann-royal-highness` | Thomas Mann | Royal Highness | A. Cecil Curtis | (see the Gutenberg header) | have | PG 36028 |
| `singles-continental-fiction-mary-lafon-jaufry-the-knight-and-the-fair-brunissen` | Jean Bernard Lafon Mary-Lafon | Jaufry the Knight and the Fair Brunissende: A Tale of the Times of King Arthur | Alfred Elwes | (see the Gutenberg header) | have | PG 44433 |
| `singles-continental-fiction-patot-the-travels-and-adventures-of-james-mass` | Simon Tyssot de Patot | The Travels and Adventures of James Massey | Stephen Whatley | (see the Gutenberg header) | have | PG 37400 |
| `singles-continental-fiction-quatrelles-the-days-of-chivalry` | Quatrelles | The Days of Chivalry; Or, The Legend of Croquemitaine | Tom Hood | (see the Gutenberg header) | have | PG 44428 |
| `singles-continental-fiction-reuter-in-the-year-13` | Fritz Reuter | In the Year '13: A Tale of Mecklenburg Life | Charles Lee Lewes | (see the Gutenberg header) | have | PG 35852 |
| `singles-continental-fiction-schubin-blanche` | Ossip Schubin | Blanche: The Maid of Lille | Sarah Holland Adams | (see the Gutenberg header) | have | PG 35385 |
| `singles-continental-fiction-schubin-gloria-victis-a-romance` | Ossip Schubin | 'Gloria Victis!' A Romance | Mary Maxwell | (see the Gutenberg header) | have | PG 35672 |
| `singles-continental-fiction-schubin-the-story-of-a-genius` | Ossip Schubin | The Story of a Genius | E. H. Lockwood | (see the Gutenberg header) | have | PG 35590 |
| `singles-continental-fiction-sparre-the-black-tortoise` | Christian Sparre | The Black Tortoise: Being the Strange Story of Old Frick's Diamond | Gertrude Hughes Brækstad | (see the Gutenberg header) | have | PG 46006 |
| `singles-continental-fiction-spielhagen-hammer-and-anvil` | Friedrich Spielhagen | Hammer and Anvil: A Novel | William Hand Browne | (see the Gutenberg header) | have | PG 34868 |
| `singles-continental-fiction-spielhagen-quisisana` | Friedrich Spielhagen | Quisisana; or, Rest at Last | H. E. Goldschmidt | (see the Gutenberg header) | have | PG 34764 |
| `singles-continental-fiction-spielhagen-the-german-pioneers` | Friedrich Spielhagen | The German Pioneers: A Tale of the Mohawk | Levi Sternberg | (see the Gutenberg header) | have | PG 34583 |
| `singles-continental-fiction-strindberg-on-the-seaboard` | August Strindberg | On the Seaboard: A Novel of the Baltic Islands | Elizabeth Clarke Westergren | (see the Gutenberg header) | have | PG 44184 |
| `singles-continental-fiction-sudermann-the-wish` | Hermann Sudermann | The Wish: A Novel | Lily Henkel | (see the Gutenberg header) | have | PG 33886 |
| `singles-continental-fiction-trueba-the-cid-campeador` | Antonio de Trueba | The Cid Campeador: A Historical Romance | Henry Joseph Gill | (see the Gutenberg header) | have | PG 41990 |
| `singles-continental-fiction-turgenev-annouchka` | Ivan Sergeevich Turgenev | Annouchka: A Tale | Franklin Pierce Abbott | (see the Gutenberg header) | have | PG 39427 |
| `singles-continental-fiction-vanderem-two-banks-of-the-seine-les-deux-rives` | Fernand Vandérem | Two banks of the Seine (Les Deux Rives) | George Raffalovich | (see the Gutenberg header) | have | PG 45857 |
| `singles-continental-fiction-werner-hermann` | E. Werner | Hermann: A Novel | Helen Keer Brown | (see the Gutenberg header) | have | PG 35142 |
| `singles-continental-fiction-werner-partners` | E. Werner | Partners: A Novel. | H. G. Godwin | (see the Gutenberg header) | have | PG 35135 |
| `singles-continental-fiction-werner-the-sign-of-flame` | E. Werner | The Sign of Flame | Eva Freeman Hart and E. Van Gerpen | (see the Gutenberg header) | have | PG 35069 |

## One-off translations: plays, verse and tale collections (Sudermann's plays incl. Edith Wharton's, Vondel's Lucifer, Cyrano, Salomé, the Noh, Baudelaire, Christine de Pisan, Kathá Sarit Ságara, Kādambarī, Old Celtic Romances)

Shelf: `pipeline/singles-verse-drama-tales_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-verse-drama-tales` · titles `python3 pipeline/split_shelf_titles.py singles-verse-drama-tales`.
Round 42 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-verse-drama-tales-alighieri-the-divine-comedy-of-dante-alighieri` | Dante Alighieri | The Divine Comedy of Dante Alighieri: The Inferno | James Romanes Sibbald | (see the Gutenberg header) | have | PG 41537 |
| `singles-verse-drama-tales-anon-chinese-mother-goose-rhymes` | traditional Chinese nursery rhymes | Chinese Mother Goose Rhymes | Isaac Taylor Headland | (see the Gutenberg header) | have | PG 40425 |
| `singles-verse-drama-tales-anon-martha` | Friedrich von Flotow (music) and W. Friedrich (libretto) | Martha; or, The Fair at Richmond | M. Louise Baum | (see the Gutenberg header) | have | PG 38597 |
| `singles-verse-drama-tales-anon-old-celtic-romances` | anonymous Old Irish tales | Old Celtic Romances | P. W. Joyce | (see the Gutenberg header) | have | PG 38041 |
| `singles-verse-drama-tales-anon-plays-of-old-japan` | Zeami and other Noh playwrights | Plays of Old Japan: The 'No' | Marie Carmichael Stopes and Joji Sakurai | (see the Gutenberg header) | have | PG 44092 |
| `singles-verse-drama-tales-anon-roumanian-stories-translated-from-the-or` | various Romanian authors | Roumanian Stories, Translated from the Original Roumanian | Lucy Byng | (see the Gutenberg header) | have | PG 38991 |
| `singles-verse-drama-tales-anon-tales-from-the-old-french` | anonymous Old French tales | Tales from the Old French | Isabel Butler | (see the Gutenberg header) | have | PG 36658 |
| `singles-verse-drama-tales-anon-zanzibar-tales` | Swahili oral tales | Zanzibar Tales: Told by Natives of the East Coast of Africa | George W. Bateman | (see the Gutenberg header) | have | PG 37472 |
| `singles-verse-drama-tales-aryasura-the-gatakamala` | Aryasura | The Gâtakamâlâ; Or, Garland of Birth-Stories | J. S. Speyer | (see the Gutenberg header) | have | PG 46984 |
| `singles-verse-drama-tales-bana-the-kadambari-of-bana` | Bāṇa and Bhūṣaṇabhaṭṭa | The Kādambarī of Bāṇa | C. M. Ridding | (see the Gutenberg header) | have | PG 41128 |
| `singles-verse-drama-tales-baudelaire-the-flowers-of-evil` | Charles Baudelaire | The Flowers of Evil | Cyril Scott | (see the Gutenberg header) | have | PG 36098 |
| `singles-verse-drama-tales-bhatta-the-katha-sarit-sagara` | Somadeva Bhatta | The Kathá Sarit Ságara; or, Ocean of the Streams of Story | C. H. Tawney | (see the Gutenberg header) | have | PG 40588 |
| `singles-verse-drama-tales-christine-the-book-of-the-duke-of-true-lovers` | Christine de Pisan | The Book of the Duke of True Lovers | Laurence Binyon and Eric Robert Dalrymple Maclagan | (see the Gutenberg header) | have | PG 36737 |
| `singles-verse-drama-tales-gosvami-chaitanya-s-life-and-teachings-from-his` | Kṛṣṇadāsa Kavirāja Gosvāmi | Chaitanya's Life And Teachings From his contemporary Begali biography the Chaitanya-charit-amrita | Jadunath Sarkar | (see the Gutenberg header) | have | PG 38016 |
| `singles-verse-drama-tales-gul-bat-caucasian-legends` | Abraam Abraamovich Gul'bat | Caucasian Legends | Sergiei Veselitskii-Bozhidarovich | (see the Gutenberg header) | have | PG 35577 |
| `singles-verse-drama-tales-heijermans-the-ghetto` | Herman Heijermans | The Ghetto: A Drama in Four Acts | Chester Bailey Fernald | (see the Gutenberg header) | have | PG 36307 |
| `singles-verse-drama-tales-holberg-jeppe-on-the-hill` | Ludvig Holberg | Jeppe on the Hill; Or, The Transformed Peasant: A Comedy in Five Acts | Martin B. Ruud and Waldemar Westergaard | (see the Gutenberg header) | have | PG 42022 |
| `singles-verse-drama-tales-iriarte-literary-fables-of-yriarte` | Tomás de Iriarte | Literary Fables of Yriarte | George H. Devereux | (see the Gutenberg header) | have | PG 39640 |
| `singles-verse-drama-tales-lloyd-aw-aw-tam-indian-nights` | Comalk-Hawk-Kih (as told to J. Wm. Lloyd) | Aw-Aw-Tam Indian Nights: Being the Myths and Legends of the Pimas of Arizona | Edward Hubert Wood | (see the Gutenberg header) | have | PG 38064 |
| `singles-verse-drama-tales-llull-the-buke-of-the-order-of-knyghthood-tran` | Ramon Llull | The Buke of the Order of Knyghthood Translated from the French by Sir Gilbert Hay, Knight | Gilbert Hay | (see the Gutenberg header) | have | PG 43365 |
| `singles-verse-drama-tales-quevedo-the-visions-of-dom-francisco-de-quevedo` | Francisco de Quevedo | The Visions of Dom Francisco de Quevedo Villegas | Roger L'Estrange | (see the Gutenberg header) | have | PG 41908 |
| `singles-verse-drama-tales-quevedo-the-visions-of-quevedo` | Francisco de Quevedo | The Visions of Quevedo | William Elliot | (see the Gutenberg header) | have | PG 41950 |
| `singles-verse-drama-tales-rostand-cyrano-de-bergerac` | Edmond Rostand | Cyrano de Bergerac: An Heroic Comedy in Five Acts | Charles Renauld | (see the Gutenberg header) | have | PG 41949 |
| `singles-verse-drama-tales-sudermann-fires-of-st-john` | Hermann Sudermann | Fires of St. John: A Drama in Four Acts | Charles Swickard | (see the Gutenberg header) | have | PG 34356 |
| `singles-verse-drama-tales-sudermann-honor` | Hermann Sudermann | Honor: A Play in Four Acts | Hilmar R. Baukhage | (see the Gutenberg header) | have | PG 34357 |
| `singles-verse-drama-tales-sudermann-magda` | Hermann Sudermann | Magda: A Play in Four Acts | Charles Edward Amory Winslow | (see the Gutenberg header) | have | PG 34184 |
| `singles-verse-drama-tales-sudermann-morituri` | Hermann Sudermann | Morituri: Three One-Act Plays Teja—Fritzchen—The Eternal Masculine | Archibald Alexander | (see the Gutenberg header) | have | PG 34359 |
| `singles-verse-drama-tales-sudermann-roses` | Hermann Sudermann | Roses: Four One-Act Plays Streaks of Light—The Last Visit—Margot—The Far-away Princess | Grace Frank | (see the Gutenberg header) | have | PG 34360 |
| `singles-verse-drama-tales-sudermann-the-joy-of-living-es-lebe-das-leben` | Hermann Sudermann | The Joy of Living (Es lebe das Leben): A Play in Five Acts | Edith Wharton | (see the Gutenberg header) | have | PG 34207 |
| `singles-verse-drama-tales-thakura-vidyapati` | Vidyāpati Thākura | Vidyāpati: Bangīya padābali; songs of the love of Rādhā and Krishna | Ananda K. Coomaraswamy | (see the Gutenberg header) | have | PG 38174 |
| `singles-verse-drama-tales-vondel-vondel-s-lucifer` | Joost van den Vondel | Vondel's Lucifer | Leonard Charles Van Noppen | (see the Gutenberg header) | have | PG 37659 |
| `singles-verse-drama-tales-wilde-salome` | Oscar Wilde | Salomé: A Tragedy in One Act | Alfred Bruce Douglas | (see the Gutenberg header) | have | PG 42704 |

## One-off translations: more continental and world fiction (Pushkin's prose tales, Gogol, Andreyev, La Gaviota, Corinne, Persiles, Galatea, Undset's Jenny, T. E. Lawrence's The Forest Giant)

Shelf: `pipeline/singles-fiction-2_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-fiction-2` · titles `python3 pipeline/split_shelf_titles.py singles-fiction-2`.
Round 43 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-fiction-2-alarcon-the-strange-friend-of-tito-gil` | Pedro Antonio de Alarcón | The Strange Friend of Tito Gil | Elizabeth Townsend Darr | (see the Gutenberg header) | have | PG 64456 |
| `singles-fiction-2-andreyev-the-dark` | Leonid Andreyev | The dark | Leonard A. Magnus and K. Walter | (see the Gutenberg header) | have | PG 49594 |
| `singles-fiction-2-andreyev-the-little-angel-and-other-stories` | Leonid Andreyev | The Little Angel, and Other Stories | W. H. Lowe | (see the Gutenberg header) | have | PG 49598 |
| `singles-fiction-2-andreyev-the-red-laugh` | Leonid Andreyev | The red laugh: fragments of a discovered manuscript | A. Linden | (see the Gutenberg header) | have | PG 62460 |
| `singles-fiction-2-andreyev-when-the-king-loses-his-head-and-other-s` | Leonid Andreyev | When the King Loses His Head, and Other Stories | Archibald J. Wolfe | (see the Gutenberg header) | have | PG 49595 |
| `singles-fiction-2-anon-christmas-stories-from-french-and-spanis` | various French and Spanish writers | Christmas Stories from French and Spanish Writers | Antoinette Ogden | (see the Gutenberg header) | have | PG 47333 |
| `singles-fiction-2-anon-christmas-tales-of-flanders` | various Flemish writers (compiled by André de Ridder) | Christmas tales of Flanders | M. C. O. Morris | (see the Gutenberg header) | have | PG 64134 |
| `singles-fiction-2-apollinaire-the-poet-assassinated` | Guillaume Apollinaire | The Poet Assassinated | Matthew Josephson | (see the Gutenberg header) | have | PG 60771 |
| `singles-fiction-2-balzac-love-in-a-mask` | Honoré de Balzac | Love in a Mask; Or, Imprudence and Happiness | Alice M. Ivimy | (see the Gutenberg header) | have | PG 48884 |
| `singles-fiction-2-barzini-the-little-match-man` | Luigi Barzini | The Little Match Man | S. F. Woodruff | (see the Gutenberg header) | have | PG 54678 |
| `singles-fiction-2-bazan-a-christian-woman` | Emilia Pardo Bazán | A Christian Woman | Mary Springer | (see the Gutenberg header) | have | PG 54796 |
| `singles-fiction-2-becquer-romantic-legends-of-spain` | Gustavo Adolfo Bécquer | Romantic legends of Spain | Cornelia Frances Bates and Katharine Lee Bates | (see the Gutenberg header) | have | PG 50044 |
| `singles-fiction-2-berger-the-ordeal-by-fire-by-a-sergeant-in-the` | Marcel Berger | The Ordeal by Fire By a Sergeant in the French Army | Cecil Curtis | (see the Gutenberg header) | have | PG 60166 |
| `singles-fiction-2-bourget-a-cruel-enigma` | Paul Bourget | A Cruel Enigma | Julian Cray | (see the Gutenberg header) | have | PG 65620 |
| `singles-fiction-2-bourget-the-blue-duchess` | Paul Bourget | The Blue Duchess | Ernest Tristan | (see the Gutenberg header) | have | PG 55726 |
| `singles-fiction-2-caballero-la-gaviota` | Fernán Caballero | La Gaviota: A Spanish novel | J. Leander Starr | (see the Gutenberg header) | have | PG 48698 |
| `singles-fiction-2-carove-the-story-without-an-end` | Friedrich Wilhelm Carové | The Story Without an End | Sarah Austin | (see the Gutenberg header) | have | PG 62229 |
| `singles-fiction-2-chekhov-the-black-monk-and-other-stories` | Anton Pavlovich Chekhov | The Black Monk, and Other Stories | R. E. C. Long | (see the Gutenberg header) | have | PG 55307 |
| `singles-fiction-2-corbeau-the-forest-giant` | Adrien Le Corbeau | The Forest Giant | T. E. Lawrence | (see the Gutenberg header) | have | PG 65161 |
| `singles-fiction-2-d-annunzio-tales-of-my-native-town` | Gabriele D'Annunzio | Tales of My Native Town | Gaetano Ettore Raffaele Mantellini | (see the Gutenberg header) | have | PG 55742 |
| `singles-fiction-2-delpit-odette-s-marriage-a-novel-from-the-frenc` | Albert Delpit | Odette's Marriage A Novel, from the French of Albert Delpit, Translated from the "Revue des Deux Mondes," by Emily Prescott | Emily Prescott | (see the Gutenberg header) | have | PG 47697 |
| `singles-fiction-2-erckmann-chatrian-brigadier-frederick` | Erckmann-Chatrian | Brigadier Frederick; and, The Dean's Watch | Richard Burton | (see the Gutenberg header) | have | PG 50186 |
| `singles-fiction-2-eschenbach-molly-and-kitty-or-peasant-life-in-irela` | Olga Eschenbach and Maria Burg | Molly and Kitty, or Peasant Life in Ireland; with Other Tales | Trauermantel | (see the Gutenberg header) | have | PG 48379 |
| `singles-fiction-2-fonhus-the-trail-of-the-elk` | Mikkjel Fønhus | The Trail of the Elk | Sara Helene Petersen Weedon | (see the Gutenberg header) | have | PG 51771 |
| `singles-fiction-2-france-bee` | Anatole France | Bee: The Princess of the Dwarfs | Peter Wright | (see the Gutenberg header) | have | PG 53771 |
| `singles-fiction-2-france-mother-of-pearl` | Anatole France | Mother of Pearl | Frederic Chapman | (see the Gutenberg header) | have | PG 58099 |
| `singles-fiction-2-gaspe-cameron-of-lochiel` | Philippe Aubert de Gaspé | Cameron of Lochiel | Charles G. D. Roberts | (see the Gutenberg header) | have | PG 53154 |
| `singles-fiction-2-gautier-the-memoirs-of-a-white-elephant` | Judith Gautier | The Memoirs of a White Elephant | S. A. B. Harvey | (see the Gutenberg header) | have | PG 46983 |
| `singles-fiction-2-gide-prometheus-illbound` | André Gide | Prometheus Illbound | Mary Lilian Share Harmsworth Rothermere | (see the Gutenberg header) | have | PG 60914 |
| `singles-fiction-2-gogol-cossack-tales` | Nikolai Vasilevich Gogol | Cossack Tales | Jurij V. Tolstoj | (see the Gutenberg header) | have | PG 58409 |
| `singles-fiction-2-gogol-home-life-in-russia-volumes-1-and-2-dead` | Nikolai Vasilevich Gogol | Home Life in Russia, Volumes 1 and 2 [Dead Souls] | Krystin Lach-Szyrma | (see the Gutenberg header) | have | PG 58070 |
| `singles-fiction-2-gorky-three-men` | Maksim Gorky | Three Men: A Novel | Charles Horne | (see the Gutenberg header) | have | PG 56456 |
| `singles-fiction-2-hugo-under-sentence-of-death` | Victor Hugo | Under Sentence of Death; Or, a Criminal's Last Hours | Gilbert Campbell | (see the Gutenberg header) | have | PG 50010 |
| `singles-fiction-2-kuprin-a-slav-soul-and-other-stories` | A. I. Kuprin | A Slav Soul, and Other Stories | Rosa Savary Graham and Stephen Graham | (see the Gutenberg header) | have | PG 57036 |
| `singles-fiction-2-lie-the-family-at-gilje` | Jonas Lie | The Family at Gilje: A Domestic Story of the Forties | Samuel Coffin Eastman | (see the Gutenberg header) | have | PG 55646 |
| `singles-fiction-2-loti-the-last-days-of-pekin` | Pierre Loti | The Last Days of Pekin | Myrta Leonora Jones | (see the Gutenberg header) | have | PG 49121 |
| `singles-fiction-2-maistre-a-journey-round-my-room` | Xavier de Maistre | A journey round my room | Henry Attwell | (see the Gutenberg header) | have | PG 62519 |
| `singles-fiction-2-maupassant-the-sisters-rondoli-and-other-stories` | Guy de Maupassant | The Sisters Rondoli, and Other Stories | Ernest Augustus Boyd | (see the Gutenberg header) | have | PG 60136 |
| `singles-fiction-2-maurois-ariel` | André Maurois | Ariel: A Shelley Romance | Ella D'Arcy | (see the Gutenberg header) | have | PG 64118 |
| `singles-fiction-2-mirbeau-calvary` | Octave Mirbeau | Calvary: A Novel | Louis Rich | (see the Gutenberg header) | have | PG 48773 |
| `singles-fiction-2-murai-kibun-daizin` | Gensai Murai | Kibun Daizin; Or, From Shark-Boy to Merchant Prince | Masao Yoshida | (see the Gutenberg header) | have | PG 65320 |
| `singles-fiction-2-noriac-human-follies-la-betise-humaine` | Jules Noriac | Human Follies (La Bêtise Humaine.) | George Marlow | (see the Gutenberg header) | have | PG 50179 |
| `singles-fiction-2-ortoli-evening-tales` | Jean-Baptiste Frédéric Ortoli | Evening Tales | Joel Chandler Harris | (see the Gutenberg header) | have | PG 56153 |
| `singles-fiction-2-perelaer-baboe-dalima` | M. T. H. Perelaer | Baboe Dalima; or, The Opium Fiend | Edwin James Venning | (see the Gutenberg header) | have | PG 60751 |
| `singles-fiction-2-pushkin-the-prose-tales-of-alexander-pushkin` | Aleksandr Sergeevich Pushkin | The Prose Tales of Alexander Pushkin | T. Keane | (see the Gutenberg header) | have | PG 55219 |
| `singles-fiction-2-pushkin-the-queen-of-spades-and-other-stories` | Aleksandr Sergeevich Pushkin | The Queen of Spades, and other stories | H. Sutherland Edwards | (see the Gutenberg header) | have | PG 55024 |
| `singles-fiction-2-rosegger-the-forest-schoolmaster` | Peter Rosegger | The Forest Schoolmaster | Frances E. Skinner | (see the Gutenberg header) | have | PG 47168 |
| `singles-fiction-2-saavedra-galatea` | Miguel de Cervantes Saavedra | Galatea | Herman Oelsner and A. B. Welford | (see the Gutenberg header) | have | PG 63404 |
| `singles-fiction-2-saavedra-the-wanderings-of-persiles-and-sigismund` | Miguel de Cervantes Saavedra | The Wanderings of Persiles and Sigismunda: A Northern Story | Louisa Dorothea Stanley | (see the Gutenberg header) | have | PG 61561 |
| `singles-fiction-2-sage-asmodeus` | Alain René Le Sage | Asmodeus; or, The Devil on Two Sticks | Joseph Thomas | (see the Gutenberg header) | have | PG 51145 |
| `singles-fiction-2-sand-the-marquis-de-villemer` | George Sand | The Marquis de Villemer | Ralph Keeler | (see the Gutenberg header) | have | PG 63083 |
| `singles-fiction-2-segur-the-story-of-a-donkey-abridged-from-the` | Sophie Ségur | The Story of a Donkey abridged from the French of Madame la comtesse de Ségur | Charles Welsh | (see the Gutenberg header) | have | PG 55256 |
| `singles-fiction-2-serao-farewell-love-a-novel` | Matilde Serao | Farewell Love! A Novel | Aline Harland | (see the Gutenberg header) | have | PG 54619 |
| `singles-fiction-2-serao-the-desire-of-life` | Matilde Serao | The Desire of Life | William Collinge | (see the Gutenberg header) | have | PG 61109 |
| `singles-fiction-2-sienkiewicz-through-the-desert` | Henryk Sienkiewicz | Through the Desert | Mary W. Artois | (see the Gutenberg header) | have | PG 60177 |
| `singles-fiction-2-siwertz-downstream` | Sigfrid Siwertz | Downstream | E. Classen | (see the Gutenberg header) | have | PG 60685 |
| `singles-fiction-2-stael-corinne` | Madame de Staël | Corinne; or, Italy | Isabel Hill and L. E. L. (Letitia Elizabeth Landon) | (see the Gutenberg header) | have | PG 52077 |
| `singles-fiction-2-sue-paula-monti` | Eugène Sue | Paula Monti; or, The Hôtel Lambert | Charles H. Town | (see the Gutenberg header) | have | PG 64739 |
| `singles-fiction-2-suttner-lay-down-your-arms` | Bertha von Suttner | Lay Down Your Arms: The Autobiography of Martha von Tilling | T. Holmes | (see the Gutenberg header) | have | PG 49294 |
| `singles-fiction-2-tolstoy-sebastopol` | Leo Tolstoy | Sebastopol | Francis Davis Millet | (see the Gutenberg header) | have | PG 61388 |
| `singles-fiction-2-topelius-the-king-s-ring` | Zacharias Topelius | The king's ring | Herbert Arnold and Sophie Öhrwall | (see the Gutenberg header) | have | PG 58838 |
| `singles-fiction-2-undset-jenny` | Sigrid Undset | Jenny: A Novel | William Emmé | (see the Gutenberg header) | have | PG 60741 |
| `singles-fiction-2-vega-the-pilgrim-of-castile` | Lope de Vega | The Pilgrim of Castile; or, El Pelegrino in Su Patria | William Dutton | (see the Gutenberg header) | have | PG 49847 |
| `singles-fiction-2-verga-the-house-by-the-medlar-tree` | Giovanni Verga | The House by the Medlar-Tree | Mary A. Craig | (see the Gutenberg header) | have | PG 54684 |
| `singles-fiction-2-veselitskaia-mimi-s-marriage` | Lidiia Ivanovna Veselitskaia | Mimi's Marriage | C. T. Hagberg Wright | (see the Gutenberg header) | have | PG 56719 |
| `singles-fiction-2-zola-claude-s-confession` | Émile Zola | Claude's Confession | George D. Cox | (see the Gutenberg header) | have | PG 63819 |
| `singles-fiction-2-zola-the-monomaniac-la-bete-humaine` | Émile Zola | The Monomaniac (La bête humaine) | Edward Vizetelly | (see the Gutenberg header) | have | PG 57038 |
| — | — | spyri-65174: Spyri's The New Year's Carol: left for the spyri shelf (Lane D). | — | — | excluded | — |

## One-off translations: more plays and poetry (The Lower Depths, Hands Around, Echegaray, Petrarch, Leopardi, Mirèio, Orlando Innamorato, the Mesnevi, the Orkneyinga Saga, the Jātaka, the Diamond Sutra)

Shelf: `pipeline/singles-plays-poetry-2_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-plays-poetry-2` · titles `python3 pipeline/split_shelf_titles.py singles-plays-poetry-2`.
Round 43 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-plays-poetry-2-al-maarri-the-luzumiyat-of-abu-l-ala-selected-from` | Abu al-Ala al-Maarri | The Luzumiyat of Abu'l-Ala Selected from his Luzum ma la Yalzam and Suct us-Zand | Ameen Fares Rihani | (see the Gutenberg header) | have | PG 50457 |
| `singles-plays-poetry-2-anon-antar` | anonymous (the Sīrat ʿAntar) | Antar: A Bedoueen Romance | Terrick Hamilton | (see the Gutenberg header) | have | PG 57857 |
| `singles-plays-poetry-2-anon-buddhist-birth-stories` | anonymous (the Pali Jātaka, ed. V. Fausbøll) | Buddhist birth stories; or, Jataka tales, Volume 1 | Robert Cæsar Childers and T. W. Rhys Davids | (see the Gutenberg header) | have | PG 51880 |
| `singles-plays-poetry-2-anon-fir-flower-tablets` | various Chinese poets | Fir-Flower Tablets: Poems Translated from the Chinese | Florence Wheelock Ayscough and Amy Lowell | (see the Gutenberg header) | have | PG 48222 |
| `singles-plays-poetry-2-anon-post-biblical-hebrew-literature` | various Hebrew writers | Post-Biblical Hebrew Literature: An Anthology | B. Halper | (see the Gutenberg header) | have | PG 61386 |
| `singles-plays-poetry-2-anon-rustic-chivalry-cavalleria-rusticana` | Pietro Mascagni (music); G. Targioni-Tozzetti and G. Menasci (libretto) | Rustic Chivalry (Cavalleria Rusticana): Melodrama in One Act | James Cartwright Macy | (see the Gutenberg header) | have | PG 48007 |
| `singles-plays-poetry-2-anon-sumerian-hymns-from-cuneiform-texts-in-t` | anonymous Sumerian hymns | Sumerian Hymns from Cuneiform Texts in the British Museum | Frederick Augustus Vanderburgh | (see the Gutenberg header) | have | PG 48094 |
| `singles-plays-poetry-2-anon-the-babees-book` | anonymous medieval courtesy books (from F. J. Furnivall's texts) | The Babees' Book: Medieval Manners for the Young: Done into Modern English | L. J. Naylor | (see the Gutenberg header) | have | PG 58985 |
| `singles-plays-poetry-2-anon-the-dean-of-lismore-s-book` | James MacGregor, Dean of Lismore (compiler) | The Dean of Lismore's Book: A Selection of Ancient Gaelic Poetry | Thomas Maclauchlan | (see the Gutenberg header) | have | PG 48099 |
| `singles-plays-poetry-2-anon-the-king-s-mirror-speculum-regale-konung` | anonymous Norwegian (the Konungs skuggsjá) | The King's Mirror (Speculum regale-Konungs skuggsjá) | Laurence Marcellus Larson | (see the Gutenberg header) | have | PG 61264 |
| `singles-plays-poetry-2-anon-the-lay-of-the-nibelung-men` | anonymous (the Nibelungenlied) | The Lay of the Nibelung Men | Arthur S. Way | (see the Gutenberg header) | have | PG 59831 |
| `singles-plays-poetry-2-anonymous-the-orkneyinga-saga` | anonymous (the Orkneyinga saga) | The Orkneyinga Saga | Gilbert Goudie and Jón A. Hjaltalín (Jón Andrésson Hjaltalín) | (see the Gutenberg header) | have | PG 57723 |
| `singles-plays-poetry-2-boiardo-the-orlando-innamorato` | Matteo Maria Boiardo | The Orlando Innamorato | William Stewart Rose | (see the Gutenberg header) | have | PG 57869 |
| `singles-plays-poetry-2-brieux-three-plays-by-brieux-with-a-preface-by` | Eugène Brieux | Three Plays by Brieux With a Preface by Bernard Shaw | St. John Hankin and John Pollock and Charlotte Frances Shaw | (see the Gutenberg header) | have | PG 46992 |
| `singles-plays-poetry-2-christine-the-epistle-of-othea-to-hector` | de Pisan Christine | The epistle of Othea to Hector; or, The boke of knyghthode | Stephen Scrope | (see the Gutenberg header) | have | PG 60567 |
| `singles-plays-poetry-2-claudel-tete-d-or` | Paul Claudel | Tête-d'Or: A play in three acts | J. S. Newberry | (see the Gutenberg header) | have | PG 52088 |
| `singles-plays-poetry-2-echegaray-the-great-galeoto` | José Echegaray | The great Galeoto; Folly or saintliness two plays done from the verse of José Echegaray into English prose by Hannah Lynch | Hannah Lynch | (see the Gutenberg header) | have | PG 55981 |
| `singles-plays-poetry-2-echegaray-the-son-of-don-juan-an-original-drama-in` | José Echegaray | The son of Don Juan an original drama in 3 acts inspired by the reading of Ibsen's work entitled 'Gengangere' | James Graham | (see the Gutenberg header) | have | PG 56126 |
| `singles-plays-poetry-2-fontaine-the-fables-of-la-fontaine-translated-int` | Jean de La Fontaine | The Fables of La Fontaine Translated into English Verse by Walter Thornbury and Illustrated by Gustave Doré | Walter Thornbury | (see the Gutenberg header) | have | PG 50316 |
| `singles-plays-poetry-2-gorky-the-lower-depths` | Maksim Gorky | The Lower Depths: A Drama in Four Acts | Jenny Covan | (see the Gutenberg header) | have | PG 52468 |
| `singles-plays-poetry-2-heijermans-the-good-hope-in-the-drama` | Herman Heijermans | The Good Hope (In "The Drama: A Quarterly Review of Dramatic Literature") | Harriet Gampert Higgins | (see the Gutenberg header) | have | PG 58473 |
| `singles-plays-poetry-2-hrotsvitha-the-plays-of-roswitha` | Hrotsvitha | The Plays of Roswitha | Christopher St. John | (see the Gutenberg header) | have | PG 59770 |
| `singles-plays-poetry-2-iqbal-the-secrets-of-the-self-asrar-i-khudi-a` | Muhammad Iqbal | The Secrets of the Self (Asrar-i Khudi) — A Philosophical Poem | Reynold Alleyne Nicholson | (see the Gutenberg header) | have | PG 57317 |
| `singles-plays-poetry-2-leclerc-coward-or-hero` | Eugène Leclerc | Coward or Hero? | Sale Barker | (see the Gutenberg header) | have | PG 56369 |
| `singles-plays-poetry-2-leopardi-the-poems-of-leopardi` | Giacomo Leopardi | The poems of Leopardi | Francis Henry Cliffe | (see the Gutenberg header) | have | PG 53020 |
| `singles-plays-poetry-2-mistral-mireio-a-provencal-poem` | Frédéric Mistral | Mirèio, a Provençal Poem | H. W. Preston | (see the Gutenberg header) | have | PG 56008 |
| `singles-plays-poetry-2-mitra-nil-darpan` | Dinabandhu Mitra | Nil Darpan; or, The Indigo Planting Mirror, A Drama. Translated from the Bengali by a Native. | Michael Madhusudan Dutt | (see the Gutenberg header) | have | PG 54027 |
| `singles-plays-poetry-2-oehlenschlager-the-gods-of-the-north` | Adam Oehlenschläger | The Gods of the North: an epic poem | William Edward Frye | (see the Gutenberg header) | have | PG 49696 |
| `singles-plays-poetry-2-petrarca-fifteen-sonnets-of-petrarch` | Francesco Petrarca | Fifteen sonnets of Petrarch | Thomas Wentworth Higginson | (see the Gutenberg header) | have | PG 50307 |
| `singles-plays-poetry-2-pushkin-poems-with-introduction-and-notes` | Aleksandr Sergeevich Pushkin | Poems With Introduction and Notes | Ivan Panin | (see the Gutenberg header) | have | PG 54991 |
| `singles-plays-poetry-2-rumi-the-mesnevi` | Maulana Jalal al-Din Rumi | The Mesnevi | James W. Redhouse | (see the Gutenberg header) | have | PG 61724 |
| `singles-plays-poetry-2-saavedra-numantia` | Miguel de Cervantes Saavedra | Numantia | James Young Gibson | (see the Gutenberg header) | have | PG 53041 |
| `singles-plays-poetry-2-sadi-the-bustan-of-sadi-translated-from-the-p` | Sadi | The Bustān of Sadi Translated from the Persian with an introduction | A. Hart Edwards | (see the Gutenberg header) | have | PG 60471 |
| `singles-plays-poetry-2-sardou-the-sorceress` | Victorien Sardou | The Sorceress: A Drama in Five Acts | Charles A. Weissert | (see the Gutenberg header) | have | PG 54705 |
| `singles-plays-poetry-2-schnitzler-hands-around-reigen` | Arthur Schnitzler | Hands Around [Reigen]: A Cycle of Ten Dialogues | L. D. Edwards and F. L. Glaser | (see the Gutenberg header) | have | PG 53513 |
| `singles-plays-poetry-2-shikibu-diaries-of-court-ladies-of-old-japan` | Murasaki Shikibu, Izumi Shikibu and the Sarashina diarist | Diaries of Court Ladies of Old Japan | Annie Shepley Omori and Kochi Doi | (see the Gutenberg header) | have | PG 47151 |
| `singles-plays-poetry-2-takeda-chushingura` | Izumo Takeda and Shoraku Miyoshi and Senryu Namiki | Chushingura; Or, The Treasury of Loyal Retainers | Jukichi Inouye | (see the Gutenberg header) | have | PG 59421 |
| `singles-plays-poetry-2-unknown-the-diamond-sutra-chin-kang-ching-or-pra` | anonymous (the Vajracchedikā Sūtra) | The Diamond Sutra (Chin-Kang-Ching) or Prajna-Paramita | William Gemmell (from Kumārajīva's Chinese) | (see the Gutenberg header) | have | PG 64623 |
| `singles-plays-poetry-2-vega-the-works-of-garcilasso-de-la-vega-surna` | Garcilaso de la Vega | The Works of Garcilasso de la Vega, Surnamed the Prince of Castilian Poets, Translated into English Verse With a Critical and Historical Essay on Spanish Poetry and a Life of the Author | Jeremiah Holmes Wiffen | (see the Gutenberg header) | have | PG 49410 |
| — | — | various-47036: The Jade Flute: translator unnamed, so the per-title translator gate has nothing to check. | — | — | excluded | — |

## One-off translations: fiction, plays and verse, mostly 1920s (Three Kingdoms, All Quiet on the Western Front, Steppenwolf, Giants in the Earth, Death in Venice, Krakatit, Max Havelaar, Eloisa)

Shelf: `pipeline/singles-fiction-3_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-fiction-3` · titles `python3 pipeline/split_shelf_titles.py singles-fiction-3`.
Round 44 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-fiction-3-andreyev-plays-by-leonid-andreyeff` | Leonid Andreyev | Plays by Leonid Andreyeff | Clarence Linton Meader and Fred Newton Scott | (see the Gutenberg header) | have | PG 78247 |
| `singles-fiction-3-anon-a-marvelous-history-of-mary-of-nimmegen` | anonymous (Mariken van Nieumeghen) | A marvelous history of Mary of Nimmegen Who for more than seven year lived and had ado with the devil | Harry Morgan Ayres | (see the Gutenberg header) | have | PG 68434 |
| `singles-fiction-3-anon-french-fairy-tales` | various French writers | French fairy tales | Martha Ward Carey | (see the Gutenberg header) | have | PG 79327 |
| `singles-fiction-3-anon-rhymes-from-the-russian` | various Russian poets | Rhymes from the Russian | John Pollen | (see the Gutenberg header) | have | PG 71595 |
| `singles-fiction-3-anon-the-humour-of-russia` | various Russian writers | The humour of Russia | E. L. Voynich | (see the Gutenberg header) | have | PG 71756 |
| `singles-fiction-3-anon-the-tain` | anonymous (the Táin Bó Cúailnge) | The Táin | Mary A. Hutton | (see the Gutenberg header) | have | PG 77663 |
| `singles-fiction-3-anon-told-in-the-gardens-of-araby-untranslate` | anonymous Arabic tales | Told in the gardens of Araby (untranslated until now) | Izora C. Chandler and Mary Williams Montgomery | (see the Gutenberg header) | have | PG 73256 |
| `singles-fiction-3-auerbach-the-little-barefoot` | Berthold Auerbach | The little Barefoot | Eliza Buckminster Lee | (see the Gutenberg header) | have | PG 70159 |
| `singles-fiction-3-bettauer-the-city-without-jews` | Hugo Bettauer | The city without Jews | Salomea Neumark Brainin | (see the Gutenberg header) | have | PG 76288 |
| `singles-fiction-3-bezruc-songs-of-the-slav` | various Czech and Slovak poets (Bezruč, Čech, Hálek, Kollár and others) | Songs of the Slav | Otto Kotouč | (see the Gutenberg header) | have | PG 70309 |
| `singles-fiction-3-bordeaux-the-will-to-live-les-roquevillard` | Henry Bordeaux | The will to live (Les Roquevillard) | Pitts Duffield | (see the Gutenberg header) | have | PG 71923 |
| `singles-fiction-3-bourget-a-living-lie` | Paul Bourget | A Living Lie | J. A. J. De Villiers | (see the Gutenberg header) | have | PG 65887 |
| `singles-fiction-3-buonarroti-sonnets-and-madrigals-of-michelangelo-bu` | Michelangelo Buonarroti | Sonnets and madrigals of Michelangelo Buonarroti | William Wells Newell | (see the Gutenberg header) | have | PG 73109 |
| `singles-fiction-3-capek-krakatit` | Karel Čapek | Krakatit | Lawrence Hyde | (see the Gutenberg header) | have | PG 79127 |
| `singles-fiction-3-caturbhujamisra-the-prem-sagur` | Caturbhujamisra | The Prem sagur | W. Hollings and Lallu Lal | (see the Gutenberg header) | have | PG 74050 |
| `singles-fiction-3-chekhov-the-shooting-party` | Anton Pavlovich Chekhov | The shooting party | A. E. Chamot | (see the Gutenberg header) | have | PG 73729 |
| `singles-fiction-3-couperus-eline-vere` | Louis Couperus | Eline Vere | Jack Thomas Grein | (see the Gutenberg header) | have | PG 66911 |
| `singles-fiction-3-d-annunzio-the-daughter-of-jorio` | Gabriele D'Annunzio | The daughter of Jorio | Alice Henry and Pietro Isola and Charlotte Porter | (see the Gutenberg header) | have | PG 76655 |
| `singles-fiction-3-d-annunzio-the-virgins-of-the-rocks` | Gabriele D'Annunzio | The Virgins of the Rocks | Agatha Hughes | (see the Gutenberg header) | have | PG 67313 |
| `singles-fiction-3-debans-catherine-s-coquetries` | Camille Debans | Catherine's coquetries | Leon Mead | (see the Gutenberg header) | have | PG 70172 |
| `singles-fiction-3-dods-tales-of-the-wild-and-the-wonderful-1867` | Mary Diana Dods | Tales of the Wild and the Wonderful [1867] | Sarah Elizabeth Utterson | (see the Gutenberg header) | have | PG 66106 |
| `singles-fiction-3-esme-the-red-gods` | Jean d' Esme | The Red Gods | Moreby Acklom | (see the Gutenberg header) | have | PG 79053 |
| `singles-fiction-3-fitinghoff-children-of-the-moor` | Laura Fitinghoff | Children of the moor | Siri Andrews | (see the Gutenberg header) | have | PG 76142 |
| `singles-fiction-3-fleuron-kittens` | Svend Fleuron | Kittens | David Pritchard | (see the Gutenberg header) | have | PG 74356 |
| `singles-fiction-3-gnudtzmann-eyes-that-cannot-see` | Albert Theodor Gnudtzmann | Eyes that cannot see | Arvid Paulson | (see the Gutenberg header) | have | PG 79218 |
| `singles-fiction-3-goethe-goethe-and-schiller-s-xenions` | Johann Wolfgang von Goethe and Friedrich Schiller | Goethe and Schiller's Xenions | Paul Carus | (see the Gutenberg header) | have | PG 76691 |
| `singles-fiction-3-guardia-costa-rican-tales` | Ricardo Fernández Guardia | Costa Rican tales | Gray Casement | (see the Gutenberg header) | have | PG 79583 |
| `singles-fiction-3-halek-evening-songs` | Vítězslav Hálek | Evening songs | Josef Štýbr | (see the Gutenberg header) | have | PG 77623 |
| `singles-fiction-3-hauptmann-the-coming-of-peace-a-family-catastrophe` | Gerhart Hauptmann | The coming of peace (A family catastrophe) | Janet Achurch and C. E. Wheeler | (see the Gutenberg header) | have | PG 75247 |
| `singles-fiction-3-hebbel-three-plays-by-frederic-hebbel` | Friedrich Hebbel | Three plays by Frederic Hebbel | Leslie Holdsworth Allen and Barker Fairley | (see the Gutenberg header) | have | PG 71187 |
| `singles-fiction-3-hesse-steppenwolf` | Hermann Hesse | Steppenwolf | Basil Creighton | (see the Gutenberg header) | have | PG 75756 |
| `singles-fiction-3-hofberg-swedish-fairy-tales` | Herman Hofberg | Swedish fairy tales | Willard Henry Myers | (see the Gutenberg header) | have | PG 73093 |
| `singles-fiction-3-jacques-dr-mabuse-master-of-mystery` | Norbert Jacques | Dr. Mabuse, master of mystery | Lilian A. Clare | (see the Gutenberg header) | have | PG 75967 |
| `singles-fiction-3-kielland-elsie` | Alexander Lange Kielland | Elsie | Miles Menander Dawson | (see the Gutenberg header) | have | PG 74860 |
| `singles-fiction-3-kivi-seven-brothers` | Aleksis Kivi | Seven brothers | Alex Matson | (see the Gutenberg header) | have | PG 79566 |
| `singles-fiction-3-kotzebue-the-virgin-of-the-sun` | August von Kotzebue | The virgin of the sun | Anne Plumptre | (see the Gutenberg header) | have | PG 69962 |
| `singles-fiction-3-larrouy-vagabonds-of-the-sea` | Maurice Larrouy | Vagabonds of the sea | Randolph Silliman Bourne | (see the Gutenberg header) | have | PG 70982 |
| `singles-fiction-3-leroux-the-new-terror` | Gaston Leroux | The new terror | Hannaford Bennett | (see the Gutenberg header) | have | PG 76493 |
| `singles-fiction-3-lion-the-black-pearl` | Marie Lion | The black pearl | Maude Wholohan | (see the Gutenberg header) | have | PG 78087 |
| `singles-fiction-3-loti-lives-of-two-cats` | Pierre Loti | Lives of Two Cats | Mary B. Richards | (see the Gutenberg header) | have | PG 67061 |
| `singles-fiction-3-louys-the-songs-of-bilitis` | Pierre Louÿs | The songs of Bilitis | Mitchell S. Buck | (see the Gutenberg header) | have | PG 76646 |
| `singles-fiction-3-luo-san-kuo` | Guanzhong Luo | San kuo; or, Romance of the three kingdoms (volume 1 of 2) | C. H. Brewitt-Taylor | (see the Gutenberg header) | have | PG 77416 |
| `singles-fiction-3-mann-death-in-venice` | Thomas Mann | Death in Venice | Kenneth Burke | (see the Gutenberg header) | have | PG 66073 |
| `singles-fiction-3-mauriac-the-kiss-to-the-leper` | François Mauriac | The kiss to the leper | James Whitall | (see the Gutenberg header) | have | PG 69443 |
| `singles-fiction-3-mauriac-therese` | François Mauriac | Thérèse | Eric Sutton | (see the Gutenberg header) | have | PG 73670 |
| `singles-fiction-3-merezhkovsky-akhnaton-king-of-egypt` | Dmitry Sergeyevich Merezhkovsky | Akhnaton, King of Egypt | Natalie Duddington | (see the Gutenberg header) | have | PG 73364 |
| `singles-fiction-3-mitra-the-spoilt-child` | Peary Chand Mitra | The Spoilt Child: A Tale of Hindu Domestic Life | G. D. Oswell | (see the Gutenberg header) | have | PG 69173 |
| `singles-fiction-3-mongiardini-rembadi-pinocchio-under-the-sea` | Gemma Mongiardini-Rembadi | Pinocchio under the sea | Carol Della Chiesa | (see the Gutenberg header) | have | PG 71880 |
| `singles-fiction-3-morand-lewis-and-irene` | Paul Morand | Lewis and Irene | Vyvyan Beresford Holland | (see the Gutenberg header) | have | PG 71047 |
| `singles-fiction-3-multatuli-max-havelaar` | Multatuli | Max Havelaar; | Alphonse Nahuys | (see the Gutenberg header) | have | PG 70128 |
| `singles-fiction-3-natsume-unhuman-tour` | Soseki Natsume | Unhuman tour | Kazutomo Takahashi | (see the Gutenberg header) | have | PG 73131 |
| `singles-fiction-3-nodier-the-bibliomaniac` | Charles Nodier | The Bibliomaniac | Mabel Osgood Wright | (see the Gutenberg header) | have | PG 66552 |
| `singles-fiction-3-pearse-collected-works-of-padraic-h-pearse` | Padraic Pearse | Collected works of Padraic H. Pearse | Joseph Campbell | (see the Gutenberg header) | have | PG 78495 |
| `singles-fiction-3-petrarca-love-s-crucifix` | Francesco Petrarca | Love's crucifix | Agnes Tobin | (see the Gutenberg header) | have | PG 78533 |
| `singles-fiction-3-pont-jest-shadowed-by-a-detective` | René de Pont-Jest | Shadowed by a detective | Virginia Champlin | (see the Gutenberg header) | have | PG 78812 |
| `singles-fiction-3-przyjemski-wanda` | Juliusz Rawicz Przyjemski | Wanda | Anna Maria May | (see the Gutenberg header) | have | PG 77708 |
| `singles-fiction-3-remarque-all-quiet-on-the-western-front` | Erich Maria Remarque | All quiet on the Western Front | A. W. Wheen | (see the Gutenberg header) | have | PG 75011 |
| `singles-fiction-3-rolland-annette-and-sylvie` | Romain Rolland | Annette and Sylvie: Being Volume One of The Soul Enchanted | Ben Ray Redman | (see the Gutenberg header) | have | PG 66405 |
| `singles-fiction-3-rolvaag-giants-in-the-earth` | O. E. Rølvaag | Giants in the earth | Lincoln Colcord | (see the Gutenberg header) | have | PG 75491 |
| `singles-fiction-3-rousseau-eloisa` | Jean-Jacques Rousseau | Eloisa | W. Kenrick | (see the Gutenberg header) | have | PG 76639 |
| `singles-fiction-3-sand-the-naiad` | George Sand | The Naiad: A ghost story | Katherine Berry di Zérèga | (see the Gutenberg header) | have | PG 69312 |
| `singles-fiction-3-shevchenko-the-kobzar-of-the-ukraine-being-select-p` | Taras Shevchenko | The Kobzar of the Ukraine Being select poems of Taras Shevchenko done into English verse with biographical fragments by Alexander Jardine Hunter | Alexander J. Hunter | (see the Gutenberg header) | have | PG 68486 |
| `singles-fiction-3-tanizaki-a-spring-time-case` | Jun'ichiro Tanizaki | A spring-time case | Z. Tamotsu Iwado | (see the Gutenberg header) | have | PG 73132 |
| `singles-fiction-3-terrasson-the-life-of-sethos-vol-1-of-2` | Jean Terrasson | The life of Sethos, Vol. 1 (of 2) | Thomas Lediard | (see the Gutenberg header) | have | PG 79675 |
| `singles-fiction-3-tormay-the-old-house` | Cécile Tormay | The Old House: A Novel | Emil Torday | (see the Gutenberg header) | have | PG 66344 |
| `singles-fiction-3-undset-the-bridal-wreath` | Sigrid Undset | The Bridal Wreath | Charles Archer and J. S. Scott | (see the Gutenberg header) | have | PG 67929 |
| `singles-fiction-3-vega-the-new-art-of-writing-plays` | Lope de Vega | The new art of writing plays | W. T. Brewster | (see the Gutenberg header) | have | PG 76719 |
| `singles-fiction-3-vollmar-sibylla` | A. Vollmar | Sibylla | Cornelia McFadden | (see the Gutenberg header) | have | PG 77545 |
| `pg-79102` | — | Erich Kästner, Emil and the detectives (May Massee): first published in English in 1930. US public domain since 1 January 2026, but fetch_shelf.py's gate still treats 1930 as in copyright, so it waits on the same override Adam is being asked about for Pickthall's Quran. | — | — | pending | — |
| `pg-79453` | — | Italo Svevo, Confessions of Zeno (Beryl De Zoete): first published in English in 1930. US public domain since 1 January 2026, but fetch_shelf.py's gate still treats 1930 as in copyright, so it waits on the same override Adam is being asked about for Pickthall's Quran. | — | — | pending | — |
| `pg-78105` | — | Ryūnosuke Akutagawa, Tales grotesque and curious (Glenn W. Shaw): first published in English in 1930. US public domain since 1 January 2026, but fetch_shelf.py's gate still treats 1930 as in copyright, so it waits on the same override Adam is being asked about for Pickthall's Quran. | — | — | pending | — |

## One-off translations: more history, travel and memoir (Gregory of Tours, Alberuni's India, Columbus's letters, Timur, Omar ibn Said, Jusserand, the Dreyfus letters, lives of Wagner, Berlioz and Chopin)

Shelf: `pipeline/singles-history-2_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-history-2` · titles `python3 pipeline/split_shelf_titles.py singles-history-2`.
Round 45 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-history-2-adam-the-romance-of-my-childhood-and-youth` | Juliette Adam | The romance of my childhood and youth | Helen Stanley | (see the Gutenberg header) | have | PG 70563 |
| `singles-history-2-amicis-morocco-its-people-and-places` | Edmondo De Amicis | Morocco, Its People and Places | Caroline Tilton | (see the Gutenberg header) | have | PG 57206 |
| `singles-history-2-amt-the-german-army-in-belgium-the-white-boo` | the German Foreign Office (Auswärtiges Amt) | The German Army in Belgium, the White Book of May 1915 | E. N. Bennett | (see the Gutenberg header) | have | PG 54296 |
| `singles-history-2-anon-the-unwritten-history-of-old-st-augustin` | Spanish colonial records (compiled by A. M. Brooks) | The unwritten history of old St. Augustine | Annie Averette | (see the Gutenberg header) | have | PG 54804 |
| `singles-history-2-barbaro-travels-to-tana-and-persia` | Giosofat Barbaro and Ambrogio Contarini | Travels to Tana and Persia | Eugene Armand Roy and William Thomas | (see the Gutenberg header) | have | PG 75292 |
| `singles-history-2-barine-bernardin-de-st-pierre` | Arvède Barine | Bernardin de St. Pierre | James Edward Gordon | (see the Gutenberg header) | have | PG 58723 |
| `singles-history-2-bedier-german-atrocities-from-german-evidence` | Joseph Bédier | German Atrocities from German Evidence | Bernhard Harrison | (see the Gutenberg header) | have | PG 47088 |
| `singles-history-2-berlioz-the-life-of-hector-berlioz-as-written-by` | Hector Berlioz | The life of Hector Berlioz as written by himself in his letters and memoirs | Katharine F. Boult | (see the Gutenberg header) | have | PG 62668 |
| `singles-history-2-biruni-alberuni-s-india-volume-1-of-2` | Muḥammad ibn Aḥmad Bīrūnī | Alberuni's India (Volume 1 of 2) | Eduard Sachau | (see the Gutenberg header) | have | PG 79672 |
| `singles-history-2-bourcier-under-the-german-shells` | Emmanuel Bourcier | Under the German shells | George Nelson Holt and Mary Roxy Wilkins Holt | (see the Gutenberg header) | have | PG 68301 |
| `singles-history-2-brunet-the-new-german-constitution` | René Brunet | The New German Constitution | Joseph Gollomb | (see the Gutenberg header) | have | PG 54957 |
| `singles-history-2-capart-a-blue-devil-of-france` | G.-P. Capart | A Blue Devil of France: Epic figures and stories of the Great War, 1914-1918 | J. C. Drouillard | (see the Gutenberg header) | have | PG 48229 |
| `singles-history-2-columbus-select-letters-of-christopher-columbus` | Christopher Columbus | Select letters of Christopher Columbus | Richard Henry Major | (see the Gutenberg header) | have | PG 77820 |
| `singles-history-2-cousin-the-youth-of-madame-de-longueville-or-ne` | Victor Cousin | The youth of Madame de Longueville, or new revelations of court and convent in the seventeenth century | Frederick W. Ricord | (see the Gutenberg header) | have | PG 77579 |
| `singles-history-2-deich-sixteen-years-in-siberia` | L. G. Deich | Sixteen years in Siberia: Some experiences of a Russian revolutionist | Helen Chisholm | (see the Gutenberg header) | have | PG 54129 |
| `singles-history-2-dieterich-hellenism-in-asia-minor` | Karl Dieterich | Hellenism in Asia Minor | Carroll N. Brown | (see the Gutenberg header) | have | PG 55728 |
| `singles-history-2-dingelstedt-john-gutenberg-first-master-printer-his` | Franz von Dingelstedt | John Gutenberg, First Master Printer His Acts and Most Remarkable Discourses and his Death | Caroline Wintour | (see the Gutenberg header) | have | PG 50000 |
| `singles-history-2-dreyfus-lettres-d-un-innocent` | Alfred Dreyfus | Lettres d'un Innocent: The Letters of Captain Dreyfus to His Wife | L. G. Moreau | (see the Gutenberg header) | have | PG 64720 |
| `singles-history-2-ebers-richard-lepsius-a-biography` | Georg Ebers | Richard Lepsius, a biography | Zoe Dana Underhill | (see the Gutenberg header) | have | PG 74815 |
| `singles-history-2-engelmann-pompeii` | Richard Engelmann | Pompeii | Talfourd Ely | (see the Gutenberg header) | have | PG 78658 |
| `singles-history-2-friis-the-monastery-of-petschenga` | J. A. Friis | The monastery of Petschenga | Hill Repp | (see the Gutenberg header) | have | PG 72118 |
| `singles-history-2-ganz-the-land-of-riddles-russia-of-to-day` | Hugo Ganz | The Land of Riddles (Russia of To-day) | Herman Rosenthal | (see the Gutenberg header) | have | PG 56772 |
| `singles-history-2-garo-why-armenia-should-be-free` | Armen Garo | Why Armenia Should Be Free: Armenia's Rôle in the Present War | Aram Torossian | (see the Gutenberg header) | have | PG 53976 |
| `singles-history-2-gautier-charles-baudelaire-his-life` | Théophile Gautier and Charles Baudelaire | Charles Baudelaire, His Life | Guy Thorne | (see the Gutenberg header) | have | PG 47075 |
| `singles-history-2-gautier-richard-wagner-and-his-poetical-work-fro` | Judith Gautier | Richard Wagner and His Poetical Work, from "Rienzi" to "Parsifal" | L. S. J. | (see the Gutenberg header) | have | PG 46982 |
| `singles-history-2-gautier-wagner-at-home` | Judith Gautier | Wagner at Home | Effie Dunreith Massie | (see the Gutenberg header) | have | PG 47080 |
| `singles-history-2-gebler-galileo-galilei-and-the-roman-curia-from` | Karl von Gebler | Galileo Galilei and the Roman Curia From Authentic Sources | G. Sturge | (see the Gutenberg header) | have | PG 60215 |
| `singles-history-2-gregory-history-of-the-franks` | Bishop of Tours Gregory | History of the Franks | Ernest Brehaut | (see the Gutenberg header) | have | PG 74955 |
| `singles-history-2-grellmann-dissertation-on-the-gipseys-representing` | Heinrich Moritz Gottlieb Grellmann | Dissertation on the Gipseys Representing their manner of life, family economy, occupations & trades, marriages & education, sickness, death, & burial, religion, language, sciences & arts, &c. &c. &c.; | Matthew Raper | (see the Gutenberg header) | have | PG 62745 |
| `singles-history-2-guizot-essay-on-the-character-and-influence-of` | François Guizot | Essay on the Character and Influence of Washington in the Revolution of the United States of America | George Stillman Hillard | (see the Gutenberg header) | have | PG 60668 |
| `singles-history-2-guizot-history-of-the-origin-of-representative` | François Guizot | History of the Origin of Representative Government in Europe | Andrew R. Scoble | (see the Gutenberg header) | have | PG 61250 |
| `singles-history-2-hedin-with-the-german-armies-in-the-west` | Sven Anders Hedin | With the German armies in the West | H. G. De Walterstorff | (see the Gutenberg header) | have | PG 79238 |
| `singles-history-2-homberg-d-eon-de-beaumont-his-life-and-times` | Octave Homberg and Fernand Jousselin | D'Eon de Beaumont, his life and times | Alfred Rieu | (see the Gutenberg header) | have | PG 75490 |
| `singles-history-2-houssaye-cleopatra` | Henry Houssaye | Cleopatra: A Study | A. F. D. | (see the Gutenberg header) | have | PG 56049 |
| `singles-history-2-hugo-oration-on-voltaire` | Victor Hugo | Oration on Voltaire | James Parton | (see the Gutenberg header) | have | PG 76789 |
| `singles-history-2-humboldt-letters-of-alexander-von-humboldt-to-var` | Alexander von Humboldt | Letters of Alexander von Humboldt to Varnhagen von Ense. From 1827 to 1858. With extracts from Varnhagen's diaries, and letters of Varnhagen and others to Humboldt | Friedrich Kapp | (see the Gutenberg header) | have | PG 67420 |
| `singles-history-2-huret-sarah-bernhardt` | Jules Huret | Sarah Bernhardt | George A. Raper | (see the Gutenberg header) | have | PG 57583 |
| `singles-history-2-husen-the-confessions-of-the-celebrated-counte` | Heinrich Husen | The Confessions of the Celebrated Countess of Lichtenau, Late Mrs. Rietz Now Confined in the Fortress of Gloglau as a State-prisoner | Richard B--t--n | (see the Gutenberg header) | have | PG 67532 |
| `singles-history-2-josephus-selections-from-josephus` | Flavius Josephus | Selections From Josephus | H. St. J. Thackeray | (see the Gutenberg header) | have | PG 64837 |
| `singles-history-2-jusserand-english-wayfaring-life-in-the-middle-age` | J. J. Jusserand | English Wayfaring Life in the Middle Ages (XIVth Century) | Lucy Toulmin Smith | (see the Gutenberg header) | have | PG 58530 |
| `singles-history-2-koldewey-the-german-arctic-expedition-of-1869-70` | Karl Koldewey | The German Arctic expedition of 1869-70, and narrative of the wreck of the "Hansa" in the ice | Lewis Page Mercier | (see the Gutenberg header) | have | PG 79056 |
| `singles-history-2-kolff-voyages-of-the-dutch-brig-of-war-dourga` | D. H. Kolff | Voyages of the Dutch brig of war Dourga | George Windsor Earl | (see the Gutenberg header) | have | PG 73305 |
| `singles-history-2-laurin-sweden` | Carl G. Laurin | Sweden | Grenville Grove | (see the Gutenberg header) | have | PG 78746 |
| `singles-history-2-lederer-the-discoveries-of-john-lederer-in-three` | John Lederer | The Discoveries of John Lederer In three several Marches from Virginia to the East of Carolina, and other parts of the Continent | William Talbot | (see the Gutenberg header) | have | PG 65160 |
| `singles-history-2-lepsius-letters-from-egypt-ethiopia-and-the-peni` | Richard Lepsius | Letters from Egypt, Ethiopia, and the peninsula of Sinai | Joanna B. Horner and Leonora Horner | (see the Gutenberg header) | have | PG 78968 |
| `singles-history-2-leroy-beaulieu-the-awakening-of-the-east` | Pierre Leroy-Beaulieu | The Awakening of the East: Siberia—Japan—China | Richard Davey | (see the Gutenberg header) | have | PG 61310 |
| `singles-history-2-malsagov-an-island-hell` | S. A. Malʹsagov | An island hell: A Soviet prison in the far north | F. H. Lyon | (see the Gutenberg header) | have | PG 68923 |
| `singles-history-2-martin-captivity-and-escape` | Jean Martin | Captivity and Escape | V. A. Randell | (see the Gutenberg header) | have | PG 49347 |
| `singles-history-2-maulde-la-claviere-the-women-of-the-renaissance` | R. de Maulde-La-Clavière | The women of the Renaissance | George Herbert Ely | (see the Gutenberg header) | have | PG 77508 |
| `singles-history-2-mirza-the-baz-nama-yi-nasiri` | Prince Taymur Mirza | The Baz-nama-yi Nasiri | D. C. Phillott | (see the Gutenberg header) | have | PG 74303 |
| `singles-history-2-mokveld-the-german-fury-in-belgium-experiences-o` | L. Mokveld | The German Fury in Belgium Experiences of a Netherland Journalist during four months with the German Army in Belgium | Carel Thieme | (see the Gutenberg header) | have | PG 60364 |
| `singles-history-2-naima-annals-of-the-turkish-empire-from-1591-t` | Mustafa Naima | Annals of the Turkish Empire, from 1591 to 1659 | Charles Fraser | (see the Gutenberg header) | have | PG 60151 |
| `singles-history-2-nicolaus-nicolaus-of-damascus-life-of-augustus` | of Damascus Nicolaus | Nicolaus of Damascus' life of Augustus | Clayton Morris Hall | (see the Gutenberg header) | have | PG 74423 |
| `singles-history-2-pourtales-frederick-chopin` | Guy de Pourtalès | Frederick Chopin | Charles Bayly | (see the Gutenberg header) | have | PG 76904 |
| `singles-history-2-rey-a-woman-s-wanderings-and-trials-during-t` | Jacoba Elizabeth De la Rey | A woman's wanderings and trials during the Anglo-Boer War | Lucy Hotz | (see the Gutenberg header) | have | PG 72195 |
| `singles-history-2-rolland-mahatma-gandhi` | Romain Rolland | Mahatma Gandhi: The Man Who Became One With the Universal Being | Catherine Dase Groth | (see the Gutenberg header) | have | PG 61575 |
| `singles-history-2-said-translation-of-the-life-of-omar-ibn-said` | Omar ibn Said | Translation of the Life of Omar ibn Said: Manuscript No. 1 | Isaac Bird | (see the Gutenberg header) | have | PG 63635 |
| `singles-history-2-schultze-the-sultanate-of-bornu` | Arnold Schultze | The Sultanate of Bornu | Philip Askell Benton | (see the Gutenberg header) | have | PG 77463 |
| `singles-history-2-stackelberg-the-life-of-carmen-sylva-queen-of-rouman` | Natalie Stackelberg | The Life of Carmen Sylva (Queen of Roumania) | Hilda Elizabeth Deichmann | (see the Gutenberg header) | have | PG 49139 |
| `singles-history-2-sturmer-two-war-years-in-constantinople` | Harry Stürmer | Two war years in Constantinople | E. Allen | (see the Gutenberg header) | have | PG 60638 |
| `singles-history-2-stutterheim-a-detailed-account-of-the-battle-of-aust` | Karl von Stutterheim | A Detailed Account of the Battle of Austerlitz | John Pine Coffin | (see the Gutenberg header) | have | PG 66641 |
| `singles-history-2-sukloff-the-life-story-of-a-russian-exile` | Marie Sukloff | The life-story of a Russian exile | Gregory Yarros | (see the Gutenberg header) | have | PG 79182 |
| `singles-history-2-sylva-from-memory-s-shrine` | Carmen Sylva | From Memory's Shrine: The Reminscences of Carmen Sylva | Edith Hopkirk | (see the Gutenberg header) | have | PG 51674 |
| `singles-history-2-symington-pen-and-pencil-sketches-of-faroe-and-ice` | Andrew James Symington | Pen and pencil sketches of Faröe and Iceland | Ólafur Pálsson | (see the Gutenberg header) | have | PG 71936 |
| `singles-history-2-timur-the-mulfuzat-timury` | Timur | The Mulfuzāt Timūry = | Abū Ṭālib al-Ḥusaynī and Charles Stewart | (see the Gutenberg header) | have | PG 76195 |
| `singles-history-2-topin-the-man-with-the-iron-mask` | Marius Topin | The man with the iron mask | Henry Vizetelly | (see the Gutenberg header) | have | PG 70207 |
| `singles-history-2-tret-iakov-my-experiences-at-nan-shan-and-port-arth` | Nikolaĭ Aleksandrovich Tret'iakov | My Experiences at Nan Shan and Port Arthur with the Fifth East Siberian Rifles | Arthur Cameron Rimington Alford | (see the Gutenberg header) | have | PG 59741 |
| `singles-history-2-tschudi-ludwig-the-second-king-of-bavaria` | Clara Tschudi | Ludwig the Second, King of Bavaria | Ethel Harriet Hearn | (see the Gutenberg header) | have | PG 48578 |
| `singles-history-2-tunisi-travels-of-an-arab-merchant-in-soudan-th` | Muḥammad ibn ʻUmar Tūnisī | Travels of an Arab merchant in Soudan (the Black Kingdoms of Central Africa) | Dr. Perron and Bayle St. John | (see the Gutenberg header) | have | PG 70889 |
| `singles-history-2-ungern-sternberg-the-memoirs-of-maria-stella-lady-newboro` | Maria Stella Petronilla Ungern-Sternberg | The Memoirs of Maria Stella (Lady Newborough) | M. Harriet M. Capes | (see the Gutenberg header) | have | PG 56643 |
| `singles-history-2-vogue-the-russian-novelists` | Eugène-Melchior Vogüé | The Russian novelists | Jane Loring Edmands | (see the Gutenberg header) | have | PG 72271 |
| `singles-history-2-werne-african-wanderings` | Ferdinand Werne | African wanderings | J. R. Johnston | (see the Gutenberg header) | have | PG 78507 |

## One-off translations: philosophy, law, religion and politics (Machiavelli's Prince, the Courtier, Maimonides's Guide, Bergson's Time and Free Will, Laplace, Valla's Donation, Descartes, Avicenna, Averroes)

Shelf: `pipeline/singles-ideas-3_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-ideas-3` · titles `python3 pipeline/split_shelf_titles.py singles-ideas-3`.
Round 46 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-ideas-3-anon-the-visigothic-code` | the Visigothic kings (the Forum Judicum) | The Visigothic code | S. P. Scott | (see the Gutenberg header) | have | PG 72551 |
| `singles-ideas-3-averroes-the-philosophy-and-theology-of-averroes` | Averroës | The Philosophy and Theology of Averroes | Muhammad Jamil al-Rahman | (see the Gutenberg header) | have | PG 65708 |
| `singles-ideas-3-avicenna-a-compendium-on-the-soul` | Avicenna | A Compendium on the Soul | Edward Abbott Van Dyck | (see the Gutenberg header) | have | PG 58186 |
| `singles-ideas-3-bergson-time-and-free-will` | Henri Bergson | Time and Free Will: An Essay on the Immediate Data of Consciousness | Frank Lubecki Pogson | (see the Gutenberg header) | have | PG 56852 |
| `singles-ideas-3-boer-the-history-of-philosophy-in-islam` | T. J. de Boer | The History of Philosophy in Islam | Edward R. Jones | (see the Gutenberg header) | have | PG 66566 |
| `singles-ideas-3-bonger-criminality-and-economic-conditions` | Willem Adriaan Bonger | Criminality and economic conditions | Henry P. Horton | (see the Gutenberg header) | have | PG 71282 |
| `singles-ideas-3-callieres-on-the-manner-of-negotiating-with-prince` | Monsieur de Callières | On the manner of negotiating with princes On the uses of diplomacy; the choice of ministers and envoys; and the personal qualities necessary for success in missions abroad | Alexander Frederick Whyte | (see the Gutenberg header) | have | PG 68987 |
| `singles-ideas-3-casaux-thoughts-on-the-mechanism-of-societies` | Charles Casaux | Thoughts on the mechanism of societies | Joseph Parkyns Macmahon | (see the Gutenberg header) | have | PG 73958 |
| `singles-ideas-3-castiglione-the-book-of-the-courtier` | Baldassarre Castiglione | The Book of the Courtier | Leonard Eckstein Opdycke | (see the Gutenberg header) | have | PG 67799 |
| `singles-ideas-3-chamfort-the-cynic-s-breviary` | Sébastien-Roch-Nicolas Chamfort | The cynic's breviary: Maxims and anecdotes from Nicolas de Chamfort | William G. Hutchison | (see the Gutenberg header) | have | PG 69632 |
| `singles-ideas-3-chatelier-how-to-become-mentally-superior` | Henri Le Chatelier | How to become mentally superior | Ralph E. Oesper | (see the Gutenberg header) | have | PG 78988 |
| `singles-ideas-3-compayre-the-history-of-pedagogy` | Gabriel Compayré | The History of Pedagogy | William Harold Payne | (see the Gutenberg header) | have | PG 62376 |
| `singles-ideas-3-confucius-the-book-of-filial-duty` | Confucius and Zengzi | The book of filial duty | Ivan Chên | (see the Gutenberg header) | have | PG 75878 |
| `singles-ideas-3-coulanges-the-origin-of-property-in-land-with-an-i` | Fustel de Coulanges | The Origin of Property in Land With an introductory chapter on the English manor by W. J. Ashley | Margaret Ashley | (see the Gutenberg header) | have | PG 67558 |
| `singles-ideas-3-d-olivet-the-golden-verses-of-pythagoras` | Antoine Fabre d'Olivet and Pythagoras | The golden verses of Pythagoras | Nayán Louise Redfield | (see the Gutenberg header) | have | PG 69174 |
| `singles-ideas-3-dahlke-buddhism-science` | Paul Dahlke | Buddhism & science | Bhikkhu Sīlāchāra | (see the Gutenberg header) | have | PG 77146 |
| `singles-ideas-3-descartes-six-metaphysical-meditations` | René Descartes | Six metaphysical meditations | William Molyneux | (see the Gutenberg header) | have | PG 70091 |
| `singles-ideas-3-droz-the-art-of-being-happy-in-a-series-of-le` | Joseph Droz | The Art of Being Happy In a Series of Letters from a Father to His Children: with Observations and Comments | Timothy Flint | (see the Gutenberg header) | have | PG 56869 |
| `singles-ideas-3-fechner-the-little-book-of-life-after-death` | Gustav Theodor Fechner | The little book of life after death | Mary C. Wadsworth | (see the Gutenberg header) | have | PG 74480 |
| `singles-ideas-3-flournoy-from-india-to-the-planet-mars` | Théodore Flournoy | From India to the planet Mars: A study of a case of somnambulism with glossolalia | Daniel B. Vermilye | (see the Gutenberg header) | have | PG 63092 |
| `singles-ideas-3-fontenelle-conversations-on-the-plurality-of-worlds` | M. de Fontenelle | Conversations on the Plurality of Worlds | Miss Gunning | (see the Gutenberg header) | have | PG 66559 |
| `singles-ideas-3-ghazzali-some-religious-and-moral-teachings-of-al` | Ghazzali | Some religious and moral teachings of Al-Ghazzali | Syed Nawab Ali | (see the Gutenberg header) | have | PG 73140 |
| `singles-ideas-3-gide-a-history-of-economic-doctrines` | Charles Gide and Charles Rist | A history of economic doctrines | R. Richards and William Smart | (see the Gutenberg header) | have | PG 57500 |
| `singles-ideas-3-glanville-a-translation-of-glanville` | Ranulf de Glanville | A translation of Glanville | John Beames | (see the Gutenberg header) | have | PG 71142 |
| `singles-ideas-3-grotius-the-freedom-of-the-seas` | Hugo Grotius | The freedom of the seas | Ralph Van Deman Magoffin | (see the Gutenberg header) | have | PG 75962 |
| `singles-ideas-3-hilty-happiness` | Karl Hilty | Happiness: Essays on the meaning of life | Francis Greenwood Peabody | (see the Gutenberg header) | have | PG 68817 |
| `singles-ideas-3-hilty-the-steps-of-life` | Karl Hilty | The steps of life: further essays on happiness | Melvin Brandow | (see the Gutenberg header) | have | PG 71785 |
| `singles-ideas-3-i-the-officer-s-manual` | Emperor of the French Napoleon I | The Officer's Manual: Napoleon's Maxims of War | G. C. D'Aguilar | (see the Gutenberg header) | have | PG 50750 |
| `singles-ideas-3-key-the-century-of-the-child` | Ellen Key | The Century of the Child | Francis Maro | (see the Gutenberg header) | have | PG 57283 |
| `singles-ideas-3-laplace-a-philosophical-essay-on-probabilities` | Pierre Simon Laplace | A Philosophical Essay on Probabilities | Frederick Lincoln Emory and Frederick Wilson Truscott | (see the Gutenberg header) | have | PG 58881 |
| `singles-ideas-3-levi-the-history-of-magic` | Éliphas Lévi | The history of magic | Arthur Edward Waite | (see the Gutenberg header) | have | PG 70033 |
| `singles-ideas-3-levy-bruhl-the-philosophy-of-auguste-comte` | Lucien Lévy-Bruhl | The Philosophy of Auguste Comte | Kathleen Mary de Beaumont Klein | (see the Gutenberg header) | have | PG 56517 |
| `singles-ideas-3-lipsius-a-brief-outline-of-the-history-of-librar` | Justus Lipsius | A brief outline of the history of libraries | John Cotton Dana | (see the Gutenberg header) | have | PG 78256 |
| `singles-ideas-3-machiavelli-the-prince` | Niccolò Machiavelli | The Prince | Luigi Ricci | (see the Gutenberg header) | have | PG 57037 |
| `singles-ideas-3-maimonides-the-guide-for-the-perplexed` | Moses Maimonides | The guide for the perplexed | M. Friedländer | (see the Gutenberg header) | have | PG 73584 |
| `singles-ideas-3-nostradamus-the-true-prophecies-or-prognostications` | Nostradamus | The true prophecies or prognostications of Michael Nostradamus, physician to Henry II. Francis II. and Charles IX. Kings of France, and one of the best astronomers that ever were. A work full of curio | Theophilus Garencières | (see the Gutenberg header) | have | PG 68907 |
| `singles-ideas-3-palacios-islam-and-the-divine-comedy` | Miguel Asín Palacios | Islam and the Divine comedy | Harold Sunderland | (see the Gutenberg header) | have | PG 77789 |
| `singles-ideas-3-pannekoek-marxism-and-darwinism` | Anton Pannekoek | Marxism and Darwinism | Nathan Weiser | (see the Gutenberg header) | have | PG 72095 |
| `singles-ideas-3-petrarca-petrarch-the-first-modern-scholar-and-ma` | Francesco Petrarca | Petrarch, the First Modern Scholar and Man of Letters A Selection from His Correspondence with Boccaccio and Other Friends, Designed to Illustrate the Beginnings of the Renaissance | James Harvey Robinson and Henry Winchester Rolfe | (see the Gutenberg header) | have | PG 48776 |
| `singles-ideas-3-rhyn-mysteria` | Otto Henne am Rhyn | Mysteria | J. Fitzgerald | (see the Gutenberg header) | have | PG 77541 |
| `singles-ideas-3-richter-pictures-of-the-socialistic-future-freel` | Eugen Richter | Pictures of the Socialistic Future (freely adapted from Bebel) | Henry Wright | (see the Gutenberg header) | have | PG 66123 |
| `singles-ideas-3-rohde-psyche` | Erwin Rohde | Psyche: The Cult of Souls and Belief in Immortality among the Greeks | W. B. Hillis | (see the Gutenberg header) | have | PG 66555 |
| `singles-ideas-3-solovyof-the-justification-of-the-good` | Vladimir Solovyof | The justification of the good | Nathalie A. Duddington | (see the Gutenberg header) | have | PG 79715 |
| `singles-ideas-3-stekel-the-depths-of-the-soul` | Wilhelm Stekel | The Depths of the Soul: Psycho-Analytical Studies | Samuel A. Tannenbaum | (see the Gutenberg header) | have | PG 57272 |
| `singles-ideas-3-valla-the-treatise-of-lorenzo-valla-on-the-don` | Lorenzo Valla | The treatise of Lorenzo Valla on the Donation of Constantine | Christopher Bush Coleman | (see the Gutenberg header) | have | PG 70092 |
| `singles-ideas-3-vives-tudor-school-boy-life` | Juan Luis Vives | Tudor school-boy life: the dialogues of Juan Luis Vives | Foster Watson | (see the Gutenberg header) | have | PG 56286 |
| `singles-ideas-3-winckelmann-reflections-on-the-painting-and-sculptur` | Johann Joachim Winckelmann | Reflections on the painting and sculpture of the Greeks | Henry Fuseli | (see the Gutenberg header) | have | PG 61317 |
| `singles-ideas-3-zetkin-social-democracy-and-woman-suffrage-a-pa` | Klara Zetkin | Social-Democracy and Woman Suffrage A Paper Read by Clara Zetkin to the Conference of Women Belonging to the Social-Democratic Party Held at Mannheim, Before the Opening of the Annual Congress of the  | A. Blaize | (see the Gutenberg header) | have | PG 57474 |

## One-off translations: science, medicine, art and crafts (Carnot, Huygens, Pasteur, Sachs, Helmholtz, Cellini's treatises, Koldewey's Babylon, Robert-Houdin)

Shelf: `pipeline/singles-science-2_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-science-2` · titles `python3 pipeline/split_shelf_titles.py singles-science-2`.
Round 46 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-science-2-arrhenius-worlds-in-the-making` | Svante Arrhenius | Worlds in the making: The evolution of the universe | H. Borns | (see the Gutenberg header) | have | PG 69022 |
| `singles-science-2-askinson-perfumes-and-their-preparation` | George William Askinson | Perfumes and their preparation | Isidor Furst | (see the Gutenberg header) | have | PG 55735 |
| `singles-science-2-balck-tactics-volume-1-of-2-introduction-and-f` | W. Balck | Tactics, Volume 1 (of 2). Introduction and Formal Tactics of Infantry | Walter Krueger | (see the Gutenberg header) | have | PG 64927 |
| `singles-science-2-behring-the-suppression-of-tuberculosis` | Emil von Behring | The suppression of tuberculosis | Charles Bolduan | (see the Gutenberg header) | have | PG 70133 |
| `singles-science-2-bergman-outlines-of-mineralogy` | Torbern Bergman | Outlines of mineralogy | William Withering | (see the Gutenberg header) | have | PG 74532 |
| `singles-science-2-bernhardi-cavalry-a-popular-edition-of-cavalry-in` | Friedrich von Bernhardi | Cavalry A Popular Edition of "Cavalry in War and Peace" | Tom Bridges | (see the Gutenberg header) | have | PG 58635 |
| `singles-science-2-bersch-the-manufacture-of-earth-colours` | Josef Bersch | The manufacture of earth colours | Chas. Salter | (see the Gutenberg header) | have | PG 71219 |
| `singles-science-2-bersch-the-manufacture-of-mineral-and-lake-pigm` | Josef Bersch | The manufacture of mineral and lake pigments | A. C. Wright | (see the Gutenberg header) | have | PG 72143 |
| `singles-science-2-bichat-treatise-on-the-anatomy-and-physiology-o` | Xavier Bichat | Treatise on the Anatomy and Physiology of the Mucous Membranes With Illustrative Pathological Observations | Joseph Houlton | (see the Gutenberg header) | have | PG 52987 |
| `singles-science-2-bie-history-of-the-pianoforte-and-pianoforte` | Oskar Bie | History of the pianoforte and pianoforte players | E. E. Kellett and Edward W. Naylor | (see the Gutenberg header) | have | PG 71333 |
| `singles-science-2-bloem-the-soul-of-the-moving-picture` | Walter Julius Bloem | The soul of the moving picture | Allen Wilson Porterfield | (see the Gutenberg header) | have | PG 73028 |
| `singles-science-2-bos-agricultural-zoology` | J. Ritzema Bos | Agricultural zoology | J. R. Ainsworth Davis | (see the Gutenberg header) | have | PG 77045 |
| `singles-science-2-broca-artificial-limbs` | Auguste Broca and Charles Ducroquet | Artificial Limbs | Reginald Cheyne Elmslie | (see the Gutenberg header) | have | PG 55739 |
| `singles-science-2-bruun-the-cave-dwellers-of-southern-tunisia` | Daniel Bruun | The cave dwellers of Southern Tunisia | L. A. E. B. | (see the Gutenberg header) | have | PG 71585 |
| `singles-science-2-buschor-greek-vase-painting-griechische-vasenmal` | Ernst Buschor | Greek vase-painting (Griechische Vasenmalerei) | G. C. Richards | (see the Gutenberg header) | have | PG 61986 |
| `singles-science-2-carnot-reflections-on-the-motive-power-of-heat` | Sadi Carnot and William Thomson Kelvin | Reflections on the motive power of heat | Robert Henry Thurston | (see the Gutenberg header) | have | PG 78610 |
| `singles-science-2-cellini-the-treatises-of-benvenuto-cellini-on-go` | Benvenuto Cellini | The treatises of Benvenuto Cellini on goldsmithing and sculpture | C. R. Ashbee | (see the Gutenberg header) | have | PG 72995 |
| `singles-science-2-chevreul-the-laws-of-contrast-of-colour` | M. E. Chevreul | The laws of contrast of colour | John Spanton | (see the Gutenberg header) | have | PG 76939 |
| `singles-science-2-curie-pierre-curie` | Marie Curie | Pierre Curie | Charlotte Kellogg and Vernon L. Kellogg | (see the Gutenberg header) | have | PG 69617 |
| `singles-science-2-dancel-obesity-or-excessive-corpulence` | J.-F. Dancel | Obesity, or Excessive Corpulence: The Various Causes and the Rational Means of Cure | M. Barrett | (see the Gutenberg header) | have | PG 57069 |
| `singles-science-2-daumas-the-horses-of-the-sahara-and-the-manners` | E.‏ Daumas | The Horses of the Sahara and the Manners of the Desert | James Hutton | (see the Gutenberg header) | have | PG 51041 |
| `singles-science-2-deite-a-practical-treatise-on-the-manufacture` | C. Deite | A practical treatise on the manufacture of perfumery | William T. Brannt | (see the Gutenberg header) | have | PG 50139 |
| `singles-science-2-desault-a-treatise-on-fractures-luxations-and-ot` | P.-J. Desault | A Treatise on Fractures, Luxations, and Other Affections of the Bones | Charles Caldwell | (see the Gutenberg header) | have | PG 58602 |
| `singles-science-2-dupouy-medicine-in-the-middle-ages-extracts-fro` | Edmond Dupouy | Medicine in the Middle Ages Extracts from "Le Moyen Age Medical" by Dr. Edmond Dupouy; translated by T. C. Minor | Thomas C. Minor | (see the Gutenberg header) | have | PG 63938 |
| `singles-science-2-ecker-the-anatomy-of-the-frog` | Alexander Ecker | The anatomy of the frog | George Haslam | (see the Gutenberg header) | have | PG 77560 |
| `singles-science-2-fabre-insect-life` | Jean-Henri Fabre | Insect life: Souvenirs of a naturalist | Margaret Roberts | (see the Gutenberg header) | have | PG 68186 |
| `singles-science-2-faucher-remarks-on-the-production-of-the-preciou` | Léon Faucher | Remarks on the production of the precious metals and on the demonetization of gold in several countries in Europe | Thomson Hankey | (see the Gutenberg header) | have | PG 50581 |
| `singles-science-2-flammarion-dreams-of-an-astronomer` | Camille Flammarion | Dreams of an astronomer | E. E. Fournier d'Albe | (see the Gutenberg header) | have | PG 74239 |
| `singles-science-2-flourens-phrenology-examined` | P. Flourens | Phrenology Examined | Charles D. Meigs | (see the Gutenberg header) | have | PG 65041 |
| `singles-science-2-fritz-photo-lithography` | Georg Fritz | Photo-Lithography | E. J. Wall | (see the Gutenberg header) | have | PG 55971 |
| `singles-science-2-gelieu-the-bee-preserver` | Jonas de Gélieu | The Bee Preserver; or, Practical Directions for the Management and Preservation of Hives | Clementina Stirling Graham | (see the Gutenberg header) | have | PG 67816 |
| `singles-science-2-glauber-the-works-of-the-highly-experienced-and` | Johann Rudolf Glauber | The works of the highly experienced and famous chymist, John Rudolph Glauber | Christopher Packe | (see the Gutenberg header) | have | PG 74240 |
| `singles-science-2-graffigny-gas-and-petroleum-engines` | H. de Graffigny | Gas and Petroleum Engines | Athol Garnet Elliott | (see the Gutenberg header) | have | PG 59311 |
| `singles-science-2-groneman-ruins-of-buddhistic-temples-in-praga-val` | I. Groneman | Ruins of Buddhistic Temples in Prågå Valley—Tyandis Båråbudur, Mendut and Pawon | J. H. | (see the Gutenberg header) | have | PG 63057 |
| `singles-science-2-groos-the-play-of-man` | Karl Groos | The Play of Man | Elizabeth L. Baldwin | (see the Gutenberg header) | have | PG 58411 |
| `singles-science-2-hansen-leprosy` | G. Armauer Hansen and Carl Looft | Leprosy | Norman Walker | (see the Gutenberg header) | have | PG 71312 |
| `singles-science-2-helmholtz-popular-lectures-on-scientific-subjects` | Hermann von Helmholtz | Popular lectures on scientific subjects | E. Atkinson | (see the Gutenberg header) | have | PG 77725 |
| `singles-science-2-holst-the-atom-and-the-bohr-theory-of-its-stru` | Helge Holst and Hendrik Anthony Kramers | The atom and the Bohr theory of its structure | Rachel T. Lindsay and Robert Bruce Lindsay | (see the Gutenberg header) | have | PG 70708 |
| `singles-science-2-huber-the-natural-history-of-ants` | P. Huber | The natural history of ants | James Rawlins Johnson | (see the Gutenberg header) | have | PG 79213 |
| `singles-science-2-huygens-the-celestial-worlds-discover-d` | Christiaan Huygens | The celestial worlds discover'd | John Clarke | (see the Gutenberg header) | have | PG 71191 |
| `singles-science-2-jacob-the-arts-in-the-middle-ages-and-at-the-p` | P. L. Jacob | The Arts in the Middle Ages and at the Period of the Renaissance | James Dafforne | (see the Gutenberg header) | have | PG 59924 |
| `singles-science-2-koldewey-the-excavations-at-babylon` | Robert Koldewey | The excavations at Babylon | A. S. Johns | (see the Gutenberg header) | have | PG 71398 |
| `singles-science-2-koppen-the-armies-of-europe` | Fedor von Köppen | The Armies of Europe | Edward Gleichen | (see the Gutenberg header) | have | PG 61365 |
| `singles-science-2-lungwitz-a-text-book-of-horseshoeing-for-horsesho` | A. Lungwitz | A Text-Book of Horseshoeing, for Horseshoers and Veterinarians | John W. Adams | (see the Gutenberg header) | have | PG 66786 |
| `singles-science-2-marion-the-wonders-of-optics` | Fulgence Marion | The Wonders of Optics | Charles W. Quin | (see the Gutenberg header) | have | PG 65114 |
| `singles-science-2-metchnikoff-immunity-in-infective-diseases` | Elie Metchnikoff | Immunity in infective diseases | Francis G. Binnie | (see the Gutenberg header) | have | PG 77523 |
| `singles-science-2-moncalm-the-origin-of-thought-and-speech` | M. Moncalm | The Origin of Thought and Speech | G. S. Whitmarsh | (see the Gutenberg header) | have | PG 64834 |
| `singles-science-2-moret-spanish-painting` | A. de Beruete y Moret | Spanish Painting | Lewis Spence | (see the Gutenberg header) | have | PG 64796 |
| `singles-science-2-mosso-fear` | A. Mosso | Fear | Federico Kiesow and E. Lough | (see the Gutenberg header) | have | PG 59901 |
| `singles-science-2-mure-dr-b-mure-s-materia-medica` | Benoît Mure | Dr. B. Mure's materia medica | Charles J. Hempel | (see the Gutenberg header) | have | PG 70350 |
| `singles-science-2-nilsson-primitive-time-reckoning` | Martin P. Nilsson | Primitive time-reckoning | F. J. Fielden | (see the Gutenberg header) | have | PG 64768 |
| `singles-science-2-pasteur-studies-on-fermentation` | Louis Pasteur | Studies on fermentation | Frank Faulkner and D. Constable Robb | (see the Gutenberg header) | have | PG 63355 |
| `singles-science-2-pirro-johann-sebastian-bach` | André Pirro | Johann Sebastian Bach: The Organist and His Works for the Organ | Wallace Goodrich | (see the Gutenberg header) | have | PG 59085 |
| `singles-science-2-pottier-douris-and-the-painters-of-greek-vases` | Edmond Pottier | Douris and the Painters of Greek Vases | Bettina Kahnweiler | (see the Gutenberg header) | have | PG 61034 |
| `singles-science-2-pozzi-escot-the-toxins-and-venoms-and-their-antibodi` | M. Emm. Pozzi-Escot | The Toxins and Venoms and Their Antibodies | Alfred I. Cohn | (see the Gutenberg header) | have | PG 50458 |
| `singles-science-2-radiguet-the-making-of-a-modern-army-and-its-oper` | René-Louis-Jules Radiguet | The Making of a Modern Army and its Operations in the Field A study based on the experience of three years on the French front (1914-1917) | Henry P. Du Bellet | (see the Gutenberg header) | have | PG 59804 |
| `singles-science-2-rambousek-industrial-poisoning-from-fumes-gases-an` | Josef Rambousek | Industrial Poisoning from Fumes, Gases and Poisons of Manufacturing Processes | Thomas Morison Legge | (see the Gutenberg header) | have | PG 60605 |
| `singles-science-2-ritter-comparative-geography` | Carl Ritter | Comparative geography | William Leonard Gage | (see the Gutenberg header) | have | PG 73615 |
| `singles-science-2-robert-houdin-the-secrets-of-stage-conjuring` | Jean-Eugène Robert-Houdin | The secrets of stage conjuring | Professor Hoffmann | (see the Gutenberg header) | have | PG 77917 |
| `singles-science-2-rodin-art` | Auguste Rodin | Art | Katharine Waldo Douglas Fedden | (see the Gutenberg header) | have | PG 59799 |
| `singles-science-2-rodin-venus-to-the-venus-of-melos` | Auguste Rodin | Venus. To the Venus of Melos | Dorothy Dudley | (see the Gutenberg header) | have | PG 59680 |
| `singles-science-2-sachs-history-of-botany-1530-1860` | Julius Sachs | History of Botany (1530-1860) | Henry E. F. Garnsey | (see the Gutenberg header) | have | PG 61240 |
| `singles-science-2-schnauss-collotype-and-photo-lithography` | Julius Schnauss | Collotype and Photo-lithography | Edwin C. Middleton | (see the Gutenberg header) | have | PG 49866 |
| `singles-science-2-schroeder-handbook-of-violin-playing` | Carl Schroeder | Handbook of violin playing | John Matthews | (see the Gutenberg header) | have | PG 73023 |
| `singles-science-2-sedziwoj-a-new-light-of-alchymie-taken-out-of-the` | Michal Sedziwój and Paracelsus | A New Light of Alchymie Taken out of the Fountaine of Nature, and Manuall Experience. Etc. | John French | (see the Gutenberg header) | have | PG 61112 |
| `singles-science-2-sernin-healthful-sports-for-young-ladies` | Mademoiselle St. Sernin | Healthful Sports for Young Ladies | William Combe | (see the Gutenberg header) | have | PG 57057 |
| `singles-science-2-smith-soren-hjorth` | Sigurd Smith | Søren Hjorth: Inventor of the Dynamo-electric Principle | F. Sodemann | (see the Gutenberg header) | have | PG 66046 |
| `singles-science-2-tramerye-the-world-struggle-for-oil` | Pierre Paul Ernest L'Espagnol de la Tramerye | The World-Struggle for Oil | Charles Leonard Leese | (see the Gutenberg header) | have | PG 61894 |
| `singles-science-2-valentini-mexican-copper-tools` | Philipp J. J. Valentini | Mexican Copper Tools: The Use of Copper by the Mexicans Before the Conquest; and the Katunes of Maya History, a Chapter in the Early History of Central America, With Special Reference to the Pio Perez | Stephen Salisbury | (see the Gutenberg header) | have | PG 57961 |
| `singles-science-2-vasari-vasari-on-technique` | Giorgio Vasari | Vasari on technique | Louisa S. Maclehose | (see the Gutenberg header) | have | PG 73397 |
| `singles-science-2-warming-a-handbook-of-systematic-botany` | Eugenius Warming | A handbook of systematic botany | Michael Cresse Potter | (see the Gutenberg header) | have | PG 68580 |
| `singles-science-2-principia` | Isaac Newton | The Mathematical Principles of Natural Philosophy (Principia), with the System of the World | Andrew Motte (revised, with a life of Newton, by N. W. Chittenden) | 1729 | have-raw | IA `newtonspmathema00newtrich` |
| `singles-science-2-menabrea` | Luigi Federico Menabrea | Sketch of the Analytical Engine invented by Charles Babbage, with Notes by the Translator (Notes A to G) | Ada Lovelace (signs her notes A. A. L.) | 1843 | have-raw | IA `india.history.resource.53369` (cut from the volume) |

## One-off translations: art, music, memoir and miscellany (Leonardo's Treatise on Painting, Hegel's Fine Art, Forkel's Bach, Rimsky-Korsakov, Dürer, King Alfred's Soliloquies, the Dhammapada, Platter)

Shelf: `pipeline/singles-arts-miscellany_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-arts-miscellany` · titles `python3 pipeline/split_shelf_titles.py singles-arts-miscellany`.
Round 47 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-arts-miscellany-adam-practical-bookbinding` | Paul Adam | Practical Bookbinding | Thomas E. Maw | (see the Gutenberg header) | have | PG 39318 |
| `singles-arts-miscellany-anon-the-book-of-vagabonds-and-beggars-with-a` | anonymous (the Liber Vagatorum, with Martin Luther's preface) | The Book of Vagabonds and Beggars, with a Vocabulary of Their Language | John Camden Hotten | (see the Gutenberg header) | have | PG 46287 |
| `singles-arts-miscellany-anon-the-buddha-s-path-of-virtue` | anonymous (the Dhammapada) | The Buddha's Path of Virtue: A Translation of the Dhammapada | F. L. Woodward | (see the Gutenberg header) | have | PG 35185 |
| `singles-arts-miscellany-anon-the-pan-german-programme-the-petition-of` | six German industrial and agrarian associations (the 1915 petition) | The Pan-German Programme The Petition of the Six Associations and the Manifesto of the Intellectuals | Edwyn Robert Bevan | (see the Gutenberg header) | have | PG 46192 |
| `singles-arts-miscellany-augustine-king-alfred-s-old-english-version-of-st` | of Hippo Augustine | King Alfred's Old English Version of St. Augustine's Soliloquies Turned into Modern English | King Alfred (into Old English) and Henry Lee Hargrove (into modern English) | (see the Gutenberg header) | have | PG 40341 |
| `singles-arts-miscellany-barue-domestic-french-cookery-4th-ed` | Sulpice Barué | Domestic French Cookery, 4th ed. | Eliza Leslie | (see the Gutenberg header) | have | PG 34837 |
| `singles-arts-miscellany-bouton-and-the-kaiser-abdicates` | S. Miles Bouton | And the Kaiser abdicates: The German Revolution November 1918-August 1919 | Arthur N. Holcombe and William Bennett Munro | (see the Gutenberg header) | have | PG 39563 |
| `singles-arts-miscellany-cain-nooks-corners-of-old-paris` | Georges Cain | Nooks & Corners of Old Paris | Frederick Lawton | (see the Gutenberg header) | have | PG 40306 |
| `singles-arts-miscellany-carlo-the-flying-spy` | Camillo De Carlo | The flying spy | Maria Sermolino | (see the Gutenberg header) | have | PG 46567 |
| `singles-arts-miscellany-caron-french-dishes-for-american-tables` | Pierre Caron | French Dishes for American Tables | Frederic Sherman | (see the Gutenberg header) | have | PG 45348 |
| `singles-arts-miscellany-chaikovskii-the-life-letters-of-peter-ilich-tchaikov` | Modest Chaikovskii | The Life & Letters of Peter Ilich Tchaikovsky | Rosa Newmarch | (see the Gutenberg header) | have | PG 45259 |
| `singles-arts-miscellany-church-dante-an-essay-to-which-is-added-a-trans` | Dante Alighieri (De Monarchia), with an essay by R. W. Church | Dante. An essay. To which is added a translation of De Monarchia. | F. J. Church | (see the Gutenberg header) | have | PG 33896 |
| `singles-arts-miscellany-cladel-rodin` | Judith Cladel | Rodin: The Man and His Art, with Leaves from His Note-book | S. K. Star | (see the Gutenberg header) | have | PG 43327 |
| `singles-arts-miscellany-clemenceau-the-surprises-of-life` | Georges Clemenceau | The surprises of life | Grace Hall | (see the Gutenberg header) | have | PG 40618 |
| `singles-arts-miscellany-drouet-juliette-drouet-s-love-letters-to-victor` | Juliette Drouet and Louis Guimbaud | Juliette Drouet's Love-Letters to Victor Hugo Edited with a Biography of Juliette Drouet | Theodora Davidson | (see the Gutenberg header) | have | PG 44034 |
| `singles-arts-miscellany-dupre-thoughts-on-art-and-autobiographical-mem` | Giovanni Duprè | Thoughts on Art and Autobiographical Memoirs of Giovanni Duprè | E. M. Peruzzi | (see the Gutenberg header) | have | PG 40870 |
| `singles-arts-miscellany-durer-of-the-just-shaping-of-letters` | Albrecht Dürer | Of the Just Shaping of Letters | R. T. Nichol | (see the Gutenberg header) | have | PG 37103 |
| `singles-arts-miscellany-forkel-johann-sebastian-bach` | Johann Nikolaus Forkel | Johann Sebastian Bach: His Life, Art, and Work | Charles Sanford Terry | (see the Gutenberg header) | have | PG 35041 |
| `singles-arts-miscellany-gandhi-a-guide-to-health` | Mahatma Gandhi | A Guide to Health | A. Rama Iyer | (see the Gutenberg header) | have | PG 40373 |
| `singles-arts-miscellany-gounod-charles-gounod-autobiographical-reminisc` | Charles Gounod | Charles Gounod Autobiographical Reminiscences with Family Letters and Notes on Music | W. Hely Hutchinson | (see the Gutenberg header) | have | PG 35812 |
| `singles-arts-miscellany-heeren-a-manual-of-ancient-history-particularly` | A. H. L. Heeren | A Manual of Ancient History Particularly with Regard to the Constitutions, the Commerce, and the Colonies, of the States of Antiquity | D. A. Talboys | (see the Gutenberg header) | have | PG 39747 |
| `singles-arts-miscellany-hegel-the-introduction-to-hegel-s-philosophy-o` | Georg Wilhelm Friedrich Hegel | The Introduction to Hegel's Philosophy of Fine Arts Translated from the German with Notes and Prefatory Essay | Bernard Bosanquet | (see the Gutenberg header) | have | PG 46330 |
| `singles-arts-miscellany-huldermann-albert-ballin` | Bernhard Huldermann | Albert Ballin | Wilhelm Johann Eggers | (see the Gutenberg header) | have | PG 44135 |
| `singles-arts-miscellany-lalanne-a-treatise-on-etching` | Maxime Lalanne | A Treatise on Etching | S. R. Koehler | (see the Gutenberg header) | have | PG 33751 |
| `singles-arts-miscellany-lamszus-the-human-slaughter-house` | Wilhelm Lamszus | The Human Slaughter-House: Scenes from the War that is Sure to Come | Oakley Williams | (see the Gutenberg header) | have | PG 39588 |
| `singles-arts-miscellany-leduc-the-mechanism-of-life` | Stéphane Leduc | The Mechanism of Life | William Deane Butcher | (see the Gutenberg header) | have | PG 33862 |
| `singles-arts-miscellany-leonardo-a-treatise-on-painting` | da Vinci Leonardo | A Treatise on Painting | J. F. Rigaud | (see the Gutenberg header) | have | PG 46915 |
| `singles-arts-miscellany-louise-my-own-affairs` | Princess of Belgium Louise | My Own Affairs | Maude M. C. Ffoulkes | (see the Gutenberg header) | have | PG 43086 |
| `singles-arts-miscellany-mangin-the-desert-world` | Arthur Mangin | The Desert World | W. H. Davenport Adams | (see the Gutenberg header) | have | PG 43396 |
| `singles-arts-miscellany-massenet-my-recollections` | Jules Massenet | My Recollections | H. Villiers Barnett | (see the Gutenberg header) | have | PG 36728 |
| `singles-arts-miscellany-merezhkovsky-the-life-work-of-flaubert-from-the-russi` | Dmitry Sergeyevich Merezhkovsky | The Life-Work of Flaubert, from the Russian of Merejowski | G. A. Mounsey | (see the Gutenberg header) | have | PG 33933 |
| `singles-arts-miscellany-naquet-legal-chemistry-a-guide-to-the-detection` | Alfred Naquet | Legal Chemistry A Guide to the Detection of Poisons, Examination of Tea, Stains, Etc., as Applied to Chemical Jurisprudence | Jesse P. Battershall | (see the Gutenberg header) | have | PG 44048 |
| `singles-arts-miscellany-palmieri-the-eruption-of-vesuvius-in-1872` | Luigi Palmieri | The Eruption of Vesuvius in 1872 | Robert Mallet | (see the Gutenberg header) | have | PG 33483 |
| `singles-arts-miscellany-pena-the-oriental-republic-of-uruguay-at-the` | Carlos María de Pena and Honore Roustan | The Oriental Republic of Uruguay at the World's Columbian Exhibition, Chicago, 1893 | Jean-Jacques Réthoré | (see the Gutenberg header) | have | PG 42879 |
| `singles-arts-miscellany-pfungst-clever-hans-the-horse-of-mr-von-osten-a` | Oskar Pfungst | Clever Hans (The Horse of Mr. Von Osten) A contribution to experimental animal and human psychology | Carl Leo Rahn | (see the Gutenberg header) | have | PG 33936 |
| `singles-arts-miscellany-platter-the-autobiography-of-thomas-platter-a-sc` | Thomas Platter | The Autobiography of Thomas Platter, a schoolmaster of the sixteenth century. | Elizabeth Anne McCaul Finn | (see the Gutenberg header) | have | PG 33860 |
| `singles-arts-miscellany-quesada-the-social-evolution-of-the-argentine-re` | Ernesto Quesada | The Social Evolution of the Argentine Republic | Enrique Gil and Layton B. Register | (see the Gutenberg header) | have | PG 38086 |
| `singles-arts-miscellany-reber-history-of-ancient-art` | Franz von Reber | History of Ancient Art | Joseph Thacher Clarke | (see the Gutenberg header) | have | PG 42082 |
| `singles-arts-miscellany-recy-the-decoration-of-leather-from-the-frenc` | Georges de Récy | The Decoration of Leather From the French of Georges de Récy | Maude Nathan | (see the Gutenberg header) | have | PG 40286 |
| `singles-arts-miscellany-renan-english-conferences-of-ernest-renan` | Ernest Renan | English Conferences of Ernest Renan: Rome and Christianity. Marcus Aurelius | Clara Erskine Clement Waters | (see the Gutenberg header) | have | PG 42865 |
| `singles-arts-miscellany-renard-guilds-in-the-middle-ages` | Georges François Renard | Guilds in the Middle Ages | Dorothy Terry | (see the Gutenberg header) | have | PG 45425 |
| `singles-arts-miscellany-rimsky-korsakov-principles-of-orchestration-with-musical` | Nikolay Rimsky-Korsakov | Principles of Orchestration, with Musical Examples Drawn from His Own Works | Edward Agate | (see the Gutenberg header) | have | PG 33900 |
| `singles-arts-miscellany-rolland-handel` | Romain Rolland | Handel | A. Eaglefield Hull | (see the Gutenberg header) | have | PG 39671 |
| `singles-arts-miscellany-roux-acrobats-and-mountebanks` | Hugues Le Roux and Jules Garnier | Acrobats and Mountebanks | A. P. Morton | (see the Gutenberg header) | have | PG 45587 |
| `singles-arts-miscellany-rydberg-the-magic-of-the-middle-ages` | Viktor Rydberg | The Magic of the Middle Ages | August Hjalmar Edgren | (see the Gutenberg header) | have | PG 39608 |
| `singles-arts-miscellany-schirmacher-the-modern-woman-s-rights-movement` | Käthe Schirmacher | The Modern Woman's Rights Movement: A Historical Survey | Carl Conrad Eckhardt | (see the Gutenberg header) | have | PG 33700 |
| `singles-arts-miscellany-schweigger-clinical-investigations-on-squint` | C. Schweigger | Clinical Investigations on Squint | Emily J. Robinson | (see the Gutenberg header) | have | PG 35639 |
| `singles-arts-miscellany-seiler-the-voice-in-singing` | Emma Seiler | The Voice in Singing | William Henry Furness | (see the Gutenberg header) | have | PG 42080 |
| `singles-arts-miscellany-taine-a-tour-through-the-pyrenees` | Hippolyte Taine | A Tour Through the Pyrenees | John Safford Fiske | (see the Gutenberg header) | have | PG 44429 |
| `singles-arts-miscellany-tanska-hoffmanowa-the-journal-of-countess-francoise-krasin` | Klementyna Tańska-Hoffmanowa | The Journal of Countess Françoise Krasinska, Great Grandmother of Victor Emmanuel | Kasimir Dziekonska | (see the Gutenberg header) | have | PG 36660 |
| `singles-arts-miscellany-wasielewski-the-violoncello-and-its-history` | Wilhelm Joseph von Wasielewski | The Violoncello and Its History | Isobella S. E. Stigand | (see the Gutenberg header) | have | PG 42629 |
| `singles-arts-miscellany-van-gogh` | Vincent van Gogh | The Letters of a Post-Impressionist, being the Familiar Correspondence of Vincent van Gogh | Anthony M. Ludovici | 1912 | have-raw | IA `lettersofpostimp00goghuoft` |
| — | — | busch-38902: Buzz a Buzz: no plain-text file at Gutenberg (as the wilhelm-busch shelf also notes). | — | — | excluded | — |

## One-off translations: fiction, plays and verse from the first stretch of the list (Mühlbach, Pushkin, Blavatsky's Grand Inquisitor, Sienkiewicz, Hamsun, Ibsen's early plays, Dante's Banquet, the Pembroke Antonius)

Shelf: `pipeline/singles-fiction-4_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-fiction-4` · titles `python3 pipeline/split_shelf_titles.py singles-fiction-4`.
Round 48 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-fiction-4-about-the-man-with-the-broken-ear` | Edmond About | The man with the broken ear | Henry Holt | (see the Gutenberg header) | have | PG 20724 |
| `singles-fiction-4-aleichem-jewish-children` | Sholem Aleichem | Jewish children | Hannah Berman | (see the Gutenberg header) | have | PG 27001 |
| `singles-fiction-4-alighieri-the-banquet-il-convito` | Dante Alighieri | The Banquet (Il Convito) | Elizabeth Price Sayer | (see the Gutenberg header) | have | PG 12867 |
| `singles-fiction-4-amfiteatrov-folk-tales-of-napoleon-napoleonder-from` | Aleksandr Amfiteatrov, with a tale by Balzac | Folk-Tales of Napoleon Napoleonder from the Russian; The Napoleon of the People from the French of Honoré De Balzac | George Kennan | (see the Gutenberg header) | have | PG 11278 |
| `singles-fiction-4-anon-after-long-years-and-other-stories` | various writers | After Long Years and Other Stories | Sophie Antoinette Miller and Agnes Mary Dunne | (see the Gutenberg header) | have | PG 8111 |
| `singles-fiction-4-anon-armenian-literature` | various Armenian writers | Armenian Literature: Comprising Poetry, Drama, Folk-lore and Classic Traditions; Translated into English for the First Time | Robert Arnot and F. B. Collins | (see the Gutenberg header) | have | PG 11461 |
| `singles-fiction-4-anon-hindustani-lyrics` | various Hindustani poets | Hindustani Lyrics | Inayat Khan and Jessie Duncan Westbrook | (see the Gutenberg header) | have | PG 17711 |
| `singles-fiction-4-anon-malayan-literature` | various Malay writers | Malayan Literature: Comprising Romantic Tales, Epic Poetry and Royal Chronicles | Chauncey C. Starkweather | (see the Gutenberg header) | have | PG 7095 |
| `singles-fiction-4-anon-markandeya-purana-books-vii-and-viii` | anonymous (the Mārkaṇḍeya Purāṇa) | Mârkandeya Purâna, Books VII and VIII | B. Hale Wortham | (see the Gutenberg header) | have | PG 7169 |
| `singles-fiction-4-anon-russian-lyrics` | various Russian poets | Russian Lyrics | Martha Dickinson Bianchi | (see the Gutenberg header) | have | PG 11985 |
| `singles-fiction-4-anon-the-departing-soul-s-address-to-the-body` | anonymous (Old English poem) | The Departing Soul's Address to the Body: A Fragment of a Semi-Saxon Poem Discovered Among the Archives of Worcester Cathedral | Samuel Weller Singer | (see the Gutenberg header) | have | PG 19937 |
| `singles-fiction-4-anon-the-garden-of-bright-waters-one-hundred` | various Asian poets | The Garden of Bright Waters One Hundred and Twenty Asiatic Love Poems | E. Powys Mathers | (see the Gutenberg header) | have | PG 9920 |
| `singles-fiction-4-anon-the-matsuyama-mirror` | anonymous Japanese tale | The Matsuyama Mirror | T. H. James | (see the Gutenberg header) | have | PG 30020 |
| `singles-fiction-4-anon-welsh-lyrics-of-the-nineteenth-century` | various Welsh poets | Welsh Lyrics of the Nineteenth Century | Edmund O. Jones | (see the Gutenberg header) | have | PG 15165 |
| `singles-fiction-4-anonymous-battle-of-the-monkey-the-crab` | anonymous Japanese tale | Battle of the Monkey & the Crab | David Thompson | (see the Gutenberg header) | have | PG 25021 |
| `singles-fiction-4-asbjornsen-round-the-yule-log` | Peter Christen Asbjørnsen | 'Round the yule-log: Christmas in Norway | H. L. Broekstad | (see the Gutenberg header) | have | PG 31993 |
| `singles-fiction-4-audoux-marie-claire` | Marguerite Audoux | Marie Claire | John N. Raphael | (see the Gutenberg header) | have | PG 20572 |
| `singles-fiction-4-balzac-a-street-of-paris-and-its-inhabitant` | Honoré de Balzac | A Street of Paris and Its Inhabitant | Henri Pène du Bois | (see the Gutenberg header) | have | PG 8150 |
| `singles-fiction-4-barbusse-the-inferno` | Henri Barbusse | The Inferno | Edward J. O'Brien | (see the Gutenberg header) | have | PG 12414 |
| `singles-fiction-4-baroja-caesar-or-nothing` | Pío Baroja | Cæsar or Nothing | Louis How | (see the Gutenberg header) | have | PG 8444 |
| `singles-fiction-4-benoit-atlantida` | Pierre Benoît | Atlantida | Mary Ross and Mary Van Arsdale Tongue | (see the Gutenberg header) | have | PG 14301 |
| `singles-fiction-4-bjornson-the-bridal-march` | Bjørnstjerne Bjørnson | The Bridal March; One Day | Edmund Gosse | (see the Gutenberg header) | have | PG 18110 |
| `singles-fiction-4-bosboom-toussaint-major-frank` | A. L. G. Bosboom-Toussaint | Major Frank | James Akeroyd | (see the Gutenberg header) | have | PG 27425 |
| `singles-fiction-4-cherubini-pinocchio-in-africa` | Eugenio Cherubini | Pinocchio in Africa | Angelo Patri | (see the Gutenberg header) | have | PG 5327 |
| `singles-fiction-4-claretie-his-excellency-the-minister` | Jules Claretie | His Excellency the Minister | Henri Roberts | (see the Gutenberg header) | have | PG 15934 |
| `singles-fiction-4-colette-barks-and-purrs` | Colette | Barks and Purrs | Maire Monica Kelly | (see the Gutenberg header) | have | PG 11737 |
| `singles-fiction-4-coppee-ten-tales` | François Coppée | Ten Tales | Walter Learned | (see the Gutenberg header) | have | PG 20380 |
| `singles-fiction-4-coppee-the-lost-child` | François Coppée | The Lost Child | J. Matthewman | (see the Gutenberg header) | have | PG 23063 |
| `singles-fiction-4-corneille-the-cid` | Pierre Corneille | The Cid | Roscoe Mongan | (see the Gutenberg header) | have | PG 14954 |
| `singles-fiction-4-dandin-hindoo-tales` | Dandin | Hindoo Tales; Or, the Adventures of Ten Princes | Philip Whittington Jacob | (see the Gutenberg header) | have | PG 11738 |
| `singles-fiction-4-daudet-jack-1877` | Alphonse Daudet | Jack 1877 | Mary Neal Sherwood | (see the Gutenberg header) | have | PG 25302 |
| `singles-fiction-4-daudet-the-immortal` | Alphonse Daudet | The Immortal; Or, One of the "Forty." (L'immortel) - 1877 | A. W. Verrall and Margaret de Gaudrion Merrifield Verrall | (see the Gutenberg header) | have | PG 25766 |
| `singles-fiction-4-dostoyevsky-the-grand-inquisitor` | Fyodor Dostoyevsky | The Grand Inquisitor | H. P. Blavatsky | (see the Gutenberg header) | have | PG 8578 |
| `singles-fiction-4-eeden-the-bride-of-dreams` | Frederik van Eeden | The Bride of Dreams | Mellie von Auw | (see the Gutenberg header) | have | PG 9111 |
| `singles-fiction-4-erckmann-chatrian-the-dean-s-watch` | Erckmann-Chatrian | The Dean's Watch | Ralph Browning Fiske | (see the Gutenberg header) | have | PG 23054 |
| `singles-fiction-4-flygare-carlen-the-home-in-the-valley` | Emilie Flygare-Carlén | The Home in the Valley | Elbert Perce | (see the Gutenberg header) | have | PG 16422 |
| `singles-fiction-4-fontaine-fables-in-rhyme-for-little-folks-from-th` | Jean de La Fontaine | Fables in Rhyme for Little Folks From the French of La Fontaine | W. T. Larned | (see the Gutenberg header) | have | PG 24108 |
| `singles-fiction-4-fontaine-the-original-fables-of-la-fontaine-rende` | Jean de La Fontaine | The Original Fables of La Fontaine Rendered into English Prose by Fredk. Colin Tilney | F. C. Tilney | (see the Gutenberg header) | have | PG 15946 |
| `singles-fiction-4-france-the-queen-pedauque` | Anatole France | The Queen Pedauque | Jos. A. V. Stritzko | (see the Gutenberg header) | have | PG 6571 |
| `singles-fiction-4-girardin-the-cross-of-berny` | Delphine de Girardin, Théophile Gautier, Joseph Méry and Jules Sandeau | The Cross of Berny; Or, Irene's Lovers | Florence Fendall and Florence Holcomb | (see the Gutenberg header) | have | PG 13191 |
| `singles-fiction-4-halevy-parisian-points-of-view` | Ludovic Halévy | Parisian Points of View | Edith Virginia Brander Matthews | (see the Gutenberg header) | have | PG 15465 |
| `singles-fiction-4-hamsun-look-back-on-happiness` | Knut Hamsun | Look Back on Happiness | Paula Wiking | (see the Gutenberg header) | have | PG 8445 |
| `singles-fiction-4-hamsun-shallow-soil` | Knut Hamsun | Shallow Soil | Carl Christian Hyllested | (see the Gutenberg header) | have | PG 7537 |
| `singles-fiction-4-ibanez-woman-triumphant-la-maja-desnuda` | Vicente Blasco Ibáñez | Woman Triumphant (La Maja Desnuda) | Hayward Keniston | (see the Gutenberg header) | have | PG 18876 |
| `singles-fiction-4-ibsen-early-plays-catiline-the-warrior-s-barro` | Henrik Ibsen | Early Plays — Catiline, the Warrior's Barrow, Olaf Liljekrans | Anders Orbeck | (see the Gutenberg header) | have | PG 7172 |
| `singles-fiction-4-iffland-the-lawyers-a-drama-in-five-acts` | August Wilhelm Iffland | The Lawyers, A Drama in Five Acts | C. Lüdger | (see the Gutenberg header) | have | PG 31567 |
| `singles-fiction-4-jammes-romance-of-the-rabbit` | Francis Jammes | Romance of the Rabbit | Gladys Edgerton | (see the Gutenberg header) | have | PG 12909 |
| `singles-fiction-4-jokai-debts-of-honor` | Mór Jókai | Debts of Honor | Arthur B. Yolland | (see the Gutenberg header) | have | PG 22757 |
| `singles-fiction-4-jokai-timar-s-two-worlds` | Mór Jókai | Timar's Two Worlds | Hegan Kennard | (see the Gutenberg header) | have | PG 31409 |
| `singles-fiction-4-karrik-more-russian-picture-tales` | Valerian Viliamovich Karrik | More Russian Picture Tales | Nevill Forbes | (see the Gutenberg header) | have | PG 23462 |
| `singles-fiction-4-kielland-garman-and-worse` | Alexander Lange Kielland | Garman and Worse: A Norwegian Novel | W. W. Kettlewell | (see the Gutenberg header) | have | PG 15864 |
| `singles-fiction-4-kielland-norse-tales-and-sketches` | Alexander Lange Kielland | Norse Tales and Sketches | R. L. Cassie | (see the Gutenberg header) | have | PG 14593 |
| `singles-fiction-4-kindermann-lola` | Henny Kindermann | Lola | Agnes Blake | (see the Gutenberg header) | have | PG 25887 |
| `singles-fiction-4-kompert-a-ghetto-violet-from-christian-and-leah` | Leopold Kompert | A Ghetto Violet From "Christian and Leah" | Alfred S. Arnold | (see the Gutenberg header) | have | PG 22663 |
| `singles-fiction-4-kotzebue-the-stranger` | August von Kotzebue | The Stranger: A Drama, in Five Acts | Benjamin Thompson | (see the Gutenberg header) | have | PG 20217 |
| `singles-fiction-4-lang-pixy-s-holiday-journey` | George Lang | Pixy's Holiday Journey | Mary E. Ireland | (see the Gutenberg header) | have | PG 15426 |
| `singles-fiction-4-lenotre-the-house-of-the-combrays` | G. Lenotre | The House of the Combrays | Gwendolen Jackson Gilder | (see the Gutenberg header) | have | PG 17067 |
| `singles-fiction-4-lie-the-pilot-and-his-wife` | Jonas Lie | The Pilot and His Wife | G. L. Tottenham | (see the Gutenberg header) | have | PG 15588 |
| `singles-fiction-4-maurois-general-bramble` | André Maurois | General Bramble | Ronald Boswell and Jules Castier | (see the Gutenberg header) | have | PG 30596 |
| `singles-fiction-4-mikszath-heathen-master-filcsik` | Kálmán Mikszáth | Heathen Master Filcsik | William N. Loew | (see the Gutenberg header) | have | PG 31676 |
| `singles-fiction-4-mikszath-st-peter-s-umbrella` | Kálmán Mikszáth | St. Peter's Umbrella: A Novel | B. W. Worswick | (see the Gutenberg header) | have | PG 31945 |
| `singles-fiction-4-milton-poemata` | John Milton | Poemata : Latin, Greek and Italian Poems by John Milton | William Cowper | (see the Gutenberg header) | have | PG 6929 |
| `singles-fiction-4-montgolfier-piccolissima` | Adélaïde de Montgolfier | Piccolissima | Eliza Lee Cabot Follen | (see the Gutenberg header) | have | PG 4049 |
| `singles-fiction-4-mornay-a-discourse-of-life-and-death-by-mornay` | Philippe de Mornay and Robert Garnier | A Discourse of Life and Death, by Mornay; and Antonius by Garnier | Mary Sidney Herbert, Countess of Pembroke | (see the Gutenberg header) | have | PG 21789 |
| `singles-fiction-4-muhlbach-henry-viii-and-his-court` | L. Mühlbach | Henry VIII and His Court: A Historical Novel | Henry Niles Pierce | (see the Gutenberg header) | have | PG 3476 |
| `singles-fiction-4-muhlbach-joseph-ii-and-his-court` | L. Mühlbach | Joseph II. and His Court: An Historical Novel | A. de V. Chaudron | (see the Gutenberg header) | have | PG 3793 |
| `singles-fiction-4-muhlbach-napoleon-and-the-queen-of-prussia` | L. Mühlbach | Napoleon and the Queen of Prussia | F. Jordan | (see the Gutenberg header) | have | PG 19562 |
| `singles-fiction-4-muhlbach-old-fritz-and-the-new-era` | L. Mühlbach | Old Fritz and the New Era | Peter Langley | (see the Gutenberg header) | have | PG 3460 |
| `singles-fiction-4-muhlbach-the-merchant-of-berlin` | L. Mühlbach | The Merchant of Berlin: An Historical Novel | Amory Coffin | (see the Gutenberg header) | have | PG 12016 |
| `singles-fiction-4-multatuli-walter-pieterse` | Multatuli | Walter Pieterse: A Story of Holland | Hubert Evans | (see the Gutenberg header) | have | PG 30135 |
| `singles-fiction-4-niese-the-story-of-the-little-mamsell` | Charlotte Niese | The Story of the Little Mamsell | E. C. Emerson | (see the Gutenberg header) | have | PG 23221 |
| `singles-fiction-4-palamas-life-immovable-first-part` | Kostes Palamas | Life Immovable. First Part | Aristides E. Phoutrides | (see the Gutenberg header) | have | PG 24191 |
| `singles-fiction-4-pushkin-marie` | Aleksandr Sergeevich Pushkin | Marie; a story of Russian love | Marie H. de Zielinska | (see the Gutenberg header) | have | PG 4344 |
| `singles-fiction-4-pushkin-the-daughter-of-the-commandant` | Aleksandr Sergeevich Pushkin | The Daughter of the Commandant | Mary Pamela Milne-Home | (see the Gutenberg header) | have | PG 13511 |
| `singles-fiction-4-pushkin-the-queen-of-spades` | Aleksandr Sergeevich Pushkin | The Queen Of Spades | H. Twitchell | (see the Gutenberg header) | have | PG 23058 |
| `singles-fiction-4-reymont-the-comedienne` | Władysław Stanisław Reymont | The Comedienne | Edmund Obecny | (see the Gutenberg header) | have | PG 25760 |
| `singles-fiction-4-rizal-friars-and-filipinos-an-abridged-transla` | José Rizal | Friars and Filipinos An Abridged Translation of Dr. Jose Rizal's Tagalog Novel, 'Noli Me Tangere.' | Frank E. Gannett | (see the Gutenberg header) | have | PG 30278 |
| `singles-fiction-4-sacher-masoch-venus-in-furs` | Leopold Sacher-Masoch | Venus in Furs | Fernanda Savage | (see the Gutenberg header) | have | PG 6852 |
| `singles-fiction-4-sadi-the-persian-literature-comprising-the-sh` | Sadi | The Persian Literature, Comprising The Shah Nameh, The Rubaiyat, The Divan, and The Gulistan, Volume 2 | James Ross | (see the Gutenberg header) | have | PG 13060 |
| `singles-fiction-4-sallengre-ebrietatis-encomium-or-the-praise-of-dru` | Albert-Henri de Sallengre | Ebrietatis Encomium or, the Praise of Drunkenness | Robert Samber | (see the Gutenberg header) | have | PG 29188 |
| `singles-fiction-4-scheffel-the-trumpeter-of-sakkingen` | Joseph Victor von Scheffel | The Trumpeter of Säkkingen: A Song from the Upper Rhine. | Rebecca Brünnow | (see the Gutenberg header) | have | PG 31314 |
| `singles-fiction-4-schiller-turandot` | Friedrich Schiller | Turandot: The Chinese Sphinx | Sabilla Novello | (see the Gutenberg header) | have | PG 26553 |
| `singles-fiction-4-shinran-buddhist-psalms-translated-from-the-japa` | Shinran | Buddhist Psalms translated from the Japanese of Shinran Shonin | L. Adams Beck and S. Yamabe | (see the Gutenberg header) | have | PG 7015 |
| `singles-fiction-4-sienkiewicz-sielanka` | Henryk Sienkiewicz | Sielanka: An Idyll | Thomas H. Bullick and Vatslaf A. Hlasko | (see the Gutenberg header) | have | PG 29305 |
| `singles-fiction-4-sienkiewicz-without-dogma` | Henryk Sienkiewicz | Without Dogma: A Novel of Modern Poland | Iza Young | (see the Gutenberg header) | have | PG 11686 |
| `singles-fiction-4-spillman-the-shipwreck-a-story-for-the-young` | Joseph Spillman | The Shipwreck A Story for the Young | Mary Richards Gray | (see the Gutenberg header) | have | PG 18399 |
| `singles-fiction-4-steinberg-in-those-days` | Judah Steinberg | In Those Days: The Story of an Old Man | George Jeshurun | (see the Gutenberg header) | have | PG 8539 |
| `singles-fiction-4-sudermann-dame-care` | Hermann Sudermann | Dame Care | Bertha Overbeck | (see the Gutenberg header) | have | PG 8487 |
| `singles-fiction-4-sue-a-cardinal-sin` | Eugène Sue | A Cardinal Sin | Alexina Loranger Donovan | (see the Gutenberg header) | have | PG 18832 |
| `singles-fiction-4-sue-a-romance-of-the-west-indies` | Eugène Sue | A Romance of the West Indies | Marian Longfellow | (see the Gutenberg header) | have | PG 29894 |
| `singles-fiction-4-sue-the-brass-bell` | Eugène Sue | The Brass Bell; or, The Chariot of Death | Solon De Leon | (see the Gutenberg header) | have | PG 26623 |
| `singles-fiction-4-thoma-moral` | Ludwig Thoma | Moral | Charles Recht | (see the Gutenberg header) | have | PG 4963 |
| `singles-fiction-4-tieck-the-pictures` | Ludwig Tieck | The Pictures; The Betrothing: Novels | Connop Thirlwall | (see the Gutenberg header) | have | PG 31912 |
| `singles-fiction-4-valdes-the-grandee` | Armando Palacio Valdés | The Grandee | Rachel Challice | (see the Gutenberg header) | have | PG 31056 |
| `singles-fiction-4-werner-the-northern-light` | E. Werner | The Northern Light | D. M. Lowrey | (see the Gutenberg header) | have | PG 16095 |
| `singles-fiction-4-zamacois-their-son` | Eduardo Zamacois | Their Son; The Necklace | George Allan England | (see the Gutenberg header) | have | PG 31662 |
| `singles-fiction-4-zola-a-love-episode` | Émile Zola | A Love Episode | C. C. Starkweather | (see the Gutenberg header) | have | PG 13695 |
| `singles-fiction-4-zola-the-dream` | Émile Zola | The Dream | Eliza E. Chase | (see the Gutenberg header) | have | PG 9499 |
| `singles-fiction-4-zschokke-the-broken-cup` | Heinrich Zschokke | The Broken Cup | Parke Godwin | (see the Gutenberg header) | have | PG 23062 |
| — | — | orgegan-28277: Mickiewicz's My First Battle: the translation was made for Project Gutenberg in 2009 and is not public domain. | — | — | excluded | — |
| — | — | poulsson-26348: Aanrud's Lisbeth Longfrock (tr. Laura E. Poulsson): left for Lane D's poulsson shelf, which covers both Poulsson sisters. | — | — | excluded | — |
| — | — | may-25729: Karl May's Travel Tales in the Promised Land (tr. Schoonover): the Gutenberg header marks it a COPYRIGHTED Project Gutenberg eBook, and the rights gate refuses it. | — | — | excluded | — |

## One-off translations: history, travel, ideas and music from the first stretch of the list (De Orbe Novo, Morga's Philippines, Lobo's Abyssinia by Samuel Johnson, the Tudor Machiavelli, Lamartine's Girondists, Arago, Wagner On Conducting)

Shelf: `pipeline/singles-nonfiction-2_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-nonfiction-2` · titles `python3 pipeline/split_shelf_titles.py singles-nonfiction-2`.
Round 49 (2026-10-10), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-nonfiction-2-achenwall-achenwall-s-observations-on-north-americ` | Gottfried Achenwall | Achenwall's Observations on North America | J. G. Rosengarten | (see the Gutenberg header) | have | PG 24752 |
| `singles-nonfiction-2-adam-the-schemes-of-the-kaiser` | Juliette Adam | The Schemes of the Kaiser | J. O. P. Bland | (see the Gutenberg header) | have | PG 17737 |
| `singles-nonfiction-2-amman-the-talking-deaf-man-a-method-proposed-w` | Johann Conrad Amman | The Talking Deaf Man A Method Proposed, Whereby He Who is Born Deaf, May Learn to Speak | Daniel Foot | (see the Gutenberg header) | have | PG 13014 |
| `singles-nonfiction-2-anghiera-de-orbe-novo-volume-1-of-2-the-eight-dec` | Pietro Martire d' Anghiera | De Orbe Novo, Volume 1 (of 2) The Eight Decades of Peter Martyr D'Anghera | Francis Augustus MacNutt | (see the Gutenberg header) | have | PG 12425 |
| `singles-nonfiction-2-anon-how-to-write-a-play-letters-from-augier` | Augier, Banville, Dennery, Dumas, Gondinet, Labiche, Legouvé, Pailleron, Sardou, Zola | How to Write a Play Letters from Augier, Banville, Dennery, Dumas, Gondinet, Labiche, Legouvé, Pailleron, Sardou and Zola | Dudley H. Miles | (see the Gutenberg header) | have | PG 18230 |
| `singles-nonfiction-2-arago-biographies-of-distinguished-scientific` | F. Arago | Biographies of distinguished scientific men. First series | Robert Grant and Baden Powell and W. H. Smyth | (see the Gutenberg header) | have | PG 16775 |
| `singles-nonfiction-2-becker-christianity-and-islam` | Carl Heinrich Becker | Christianity and Islam | H. J. Chaytor | (see the Gutenberg header) | have | PG 11198 |
| `singles-nonfiction-2-bernhardi-cavalry-in-future-wars` | Friedrich von Bernhardi | Cavalry in Future Wars | Charles Sydney Goldman | (see the Gutenberg header) | have | PG 28298 |
| `singles-nonfiction-2-birnbaum-prof-koch-s-method-to-cure-tuberculosis` | Max Birnbaum | Prof. Koch's Method to Cure Tuberculosis Popularly Treated | Fr. Brendecke | (see the Gutenberg header) | have | PG 27181 |
| `singles-nonfiction-2-blakman-henry-the-sixth` | John Blakman | Henry the Sixth | M. R. James | (see the Gutenberg header) | have | PG 29689 |
| `singles-nonfiction-2-boelcke-an-aviator-s-field-book-being-the-field` | Oswald Boelcke | An Aviator's Field Book Being the field reports of Oswald Bölcke, from August 1, 1914 to October 28, 1916 | Robert Reynold Hirsch | (see the Gutenberg header) | have | PG 30011 |
| `singles-nonfiction-2-bordeaux-georges-guynemer` | Henry Bordeaux | Georges Guynemer: Knight of the Air | Louise Morgan Sill | (see the Gutenberg header) | have | PG 18117 |
| `singles-nonfiction-2-busoni-sketch-of-a-new-esthetic-of-music` | Ferruccio Busoni | Sketch of a New Esthetic of Music | Theodore Baker | (see the Gutenberg header) | have | PG 31799 |
| `singles-nonfiction-2-cerruti-my-friends-the-savages-notes-and-observa` | Giovanni Battista Cerruti | My Friends the Savages Notes and Observations of a Perak settler (Malay Peninsula) | I. Stone Sanpietro | (see the Gutenberg header) | have | PG 28189 |
| `singles-nonfiction-2-cramer-bremen-cotton-exchange-1872-1922` | Andreas Wilhelm Cramer | Bremen Cotton Exchange, 1872/1922 | Ch. F. C. Uhte | (see the Gutenberg header) | have | PG 29065 |
| `singles-nonfiction-2-crignelle-le-morvan-a-district-of-france-its-wild` | Henri de Crignelle | Le Morvan, [A District of France,] Its Wild Sports, Vineyards and Forests; with Legends, Antiquities, Rural and Local Sketches | William Jesse | (see the Gutenberg header) | have | PG 28573 |
| `singles-nonfiction-2-dard-perils-and-captivity-comprising-the-suff` | Charlotte-Adélaïde Dard, Pierre-Raymond de Brisson and Jean Godin des Odonais | Perils and Captivity Comprising The sufferings of the Picard family after the shipwreck of the Medusa, in the year 1816; Narrative of the captivity of M. de Brisson, in the year 1785; Voyage of Madame | Patrick Maxwell | (see the Gutenberg header) | have | PG 22792 |
| `singles-nonfiction-2-decelles-the-patriotes-of-37` | Alfred D. DeCelles | The 'Patriotes' of '37: A Chronicle of the Lower Canada Rebellion | W. Stewart Wallace | (see the Gutenberg header) | have | PG 29973 |
| `singles-nonfiction-2-dennert-at-the-deathbed-of-darwinism` | Eberhard Dennert | At the Deathbed of Darwinism: A Series of Papers | Edwin V. O'Harra and John H. Peschges | (see the Gutenberg header) | have | PG 21019 |
| `singles-nonfiction-2-durer-records-of-journeys-to-venice-and-the-lo` | Albrecht Dürer | Records of Journeys to Venice and the Low Countries | Rudolf Tombo | (see the Gutenberg header) | have | PG 3226 |
| `singles-nonfiction-2-ehrlich-histology-of-the-blood-normal-and-pathol` | Paul Ehrlich and Adolf Lazarus | Histology of the Blood, Normal and Pathological | W. Myers | (see the Gutenberg header) | have | PG 29842 |
| `singles-nonfiction-2-faguet-the-cult-of-incompetence` | Émile Faguet | The cult of incompetence | Beatrice Barstow | (see the Gutenberg header) | have | PG 27368 |
| `singles-nonfiction-2-feuillet-orchesography-or-the-art-of-dancing-the` | Raoul-Auger Feuillet | Orchesography, or, the Art of Dancing The Art of Dancing by Characters and Demonstrative Figures | John Weaver | (see the Gutenberg header) | have | PG 9454 |
| `singles-nonfiction-2-finot-modern-saints-and-seers` | Jean Finot | Modern Saints and Seers | Evan Marrett | (see the Gutenberg header) | have | PG 25126 |
| `singles-nonfiction-2-forstner-the-journal-of-submarine-commander-von-f` | Georg-Günther Forstner | The Journal of Submarine Commander von Forstner | Russell Codman | (see the Gutenberg header) | have | PG 30114 |
| `singles-nonfiction-2-frobel-autobiography-of-friedrich-froebel` | Friedrich Fröbel | Autobiography of Friedrich Froebel | Emilie Michaelis and Henry Keatley Moore | (see the Gutenberg header) | have | PG 16434 |
| `singles-nonfiction-2-gasparin-the-uprising-of-a-great-people-the-unite` | Agénor Gasparin | The Uprising of a Great People The United States in 1861. to Which is Added a Word of Peace on the Difference Between England the United States. | Mary L. Booth | (see the Gutenberg header) | have | PG 10637 |
| `singles-nonfiction-2-goudemetz-historical-epochs-of-the-french-revoluti` | Henry Goudemetz | Historical Epochs of the French Revolution With The Judgment And Execution Of Louis XVI., King Of France And A List Of The Members Of The National Convention, Who Voted For And Against His Death | Francis Randolph | (see the Gutenberg header) | have | PG 16962 |
| `singles-nonfiction-2-grasser-synthetic-tannins-their-synthesis-indust` | Georg Grasser | Synthetic Tannins, Their Synthesis, Industrial Production and Application | Fini Georges Alexander Enna | (see the Gutenberg header) | have | PG 7981 |
| `singles-nonfiction-2-gregorovius-lucretia-borgia-according-to-original-do` | Ferdinand Gregorovius | Lucretia Borgia According to Original Documents and Correspondence of Her Day | John Leslie Garner | (see the Gutenberg header) | have | PG 20804 |
| `singles-nonfiction-2-gross-criminal-psychology` | Hans Gross | Criminal Psychology: A Manual for Judges, Practitioners, and Students | Horace Meyer Kallen | (see the Gutenberg header) | have | PG 1320 |
| `singles-nonfiction-2-guizot-memoirs-to-illustrate-the-history-of-my` | François Guizot | Memoirs to Illustrate the History of My Time, Volume 1 | John William Cole | (see the Gutenberg header) | have | PG 28169 |
| `singles-nonfiction-2-hertzka-freeland` | Theodor Hertzka | Freeland: A Social Anticipation | Arthur Ransom | (see the Gutenberg header) | have | PG 9866 |
| `singles-nonfiction-2-holbach-superstition-in-all-ages` | Paul Henri Thiry Holbach | Superstition in all ages | Anna Knoop | (see the Gutenberg header) | have | PG 17607 |
| `singles-nonfiction-2-hugo-the-history-of-a-crime-the-testimony-of` | Victor Hugo | The History of a Crime The Testimony of an Eye-Witness | T. H. Joyce and Arthur Locker | (see the Gutenberg header) | have | PG 10381 |
| `singles-nonfiction-2-inostrantzev-iranian-influence-on-moslem-literature-p` | Konstantin Aleksandrovich Inostrantzev | Iranian Influence on Moslem Literature, Part I | G. K. Nariman | (see the Gutenberg header) | have | PG 12918 |
| `singles-nonfiction-2-kestell-the-peace-negotiations-between-the-gover` | J. D. Kestell and D. E. van Velden | The peace negotiations between the governments of the South African Republic and the Orange Free State, and the representatives of the British government, which terminated in the peace concluded at Ve | D. E. van Velden | (see the Gutenberg header) | have | PG 27529 |
| `singles-nonfiction-2-labat-the-art-of-fencing` | maître d'armes Labat | The Art of Fencing; Or, The Use of the Small Sword | Andrew Mahon | (see the Gutenberg header) | have | PG 12135 |
| `singles-nonfiction-2-lamartine-atheism-among-the-people` | Alphonse de Lamartine | Atheism Among the People | Edward Everett Hale and Francis Le Baron | (see the Gutenberg header) | have | PG 25339 |
| `singles-nonfiction-2-lamartine-history-of-the-girondists-volume-i-perso` | Alphonse de Lamartine | History of the Girondists, Volume I Personal Memoirs of the Patriots of the French Revolution | H. T. Ryde | (see the Gutenberg header) | have | PG 18094 |
| `singles-nonfiction-2-lasker-chess-strategy` | Edward Lasker | Chess Strategy | J. Du Mont | (see the Gutenberg header) | have | PG 5614 |
| `singles-nonfiction-2-lauzanne-fighting-france` | Stéphane Lauzanne | Fighting France | John Lauris Blake Williams | (see the Gutenberg header) | have | PG 18483 |
| `singles-nonfiction-2-ledesma-chocolate` | Antonio Colmenero de Ledesma | Chocolate: or, An Indian Drinke By the wise and Moderate use whereof, Health is preserved, Sicknesse Diverted, and Cured, especially the Plague of the Guts; vulgarly called The New Disease | James Wadsworth | (see the Gutenberg header) | have | PG 21271 |
| `singles-nonfiction-2-lehmann-how-to-sing-meine-gesangskunst` | Lilli Lehmann | How to sing [Meine Gesangskunst] | Richard Aldrich | (see the Gutenberg header) | have | PG 19116 |
| `singles-nonfiction-2-lenclos-life-letters-and-epicurean-philosophy-of` | Ninon de Lenclos | Life, letters, and Epicurean philosophy of Ninon de L'Enclos, the celebrated beauty of the seventeenth century | William Hassell Overton and Charles Henry Robinson | (see the Gutenberg header) | have | PG 10665 |
| `singles-nonfiction-2-liszt-life-of-chopin` | Franz Liszt | Life of Chopin | Martha Walker Cook | (see the Gutenberg header) | have | PG 4386 |
| `singles-nonfiction-2-lobo-a-voyage-to-abyssinia` | Jerónimo Lobo | A Voyage to Abyssinia | Samuel Johnson | (see the Gutenberg header) | have | PG 1436 |
| `singles-nonfiction-2-machiavelli-machiavelli-volume-i` | Niccolò Machiavelli | Machiavelli, Volume I | Edward Dacres and Peter Whitehorne | (see the Gutenberg header) | have | PG 15772 |
| `singles-nonfiction-2-mauclair-the-french-impressionists-1860-1900` | Camille Mauclair | The French Impressionists (1860-1900) | Paul G. Konody | (see the Gutenberg header) | have | PG 14056 |
| `singles-nonfiction-2-mead-medica-sacra-or-a-commentary-on-the-most` | Richard Mead | Medica Sacra Or, A Commentary on the Most Remarkable Diseases Mentioned in the Holy Scriptures | Thomas Stack | (see the Gutenberg header) | have | PG 31203 |
| `singles-nonfiction-2-menant-les-parsis` | Delphine Menant | Les Parsis | Ratanbai Ardeshir Vakil | (see the Gutenberg header) | have | PG 29109 |
| `singles-nonfiction-2-menzel-germany-from-the-earliest-period-volume` | Wolfgang Menzel | Germany from the Earliest Period, Volume 4 | George Horrocks | (see the Gutenberg header) | have | PG 8401 |
| `singles-nonfiction-2-morga-history-of-the-philippine-islands` | Antonio de Morga | History of the Philippine Islands | Emma Helen Blair and James Alexander Robertson | (see the Gutenberg header) | have | PG 7001 |
| `singles-nonfiction-2-muller-facts-and-arguments-for-darwin` | Fritz Müller | Facts and Arguments for Darwin | W. S. Dallas | (see the Gutenberg header) | have | PG 6475 |
| `singles-nonfiction-2-niebuhr-the-tell-el-amarna-period` | Carl Niebuhr | The Tell El Amarna Period | J. Hutchison | (see the Gutenberg header) | have | PG 26145 |
| `singles-nonfiction-2-nordenskiold-the-voyage-of-the-vega-round-asia-and-eu` | A. E. Nordenskiöld | The Voyage of the Vega round Asia and Europe, Volume I and Volume II | Alexander Leslie | (see the Gutenberg header) | have | PG 24365 |
| `singles-nonfiction-2-persky-contemporary-russian-novelists` | Serge Persky | Contemporary Russian Novelists | Frederick Eisemann | (see the Gutenberg header) | have | PG 31503 |
| `singles-nonfiction-2-petrucci-chinese-painters` | Raphaël Petrucci | Chinese Painters: A Critical Study | Frances Seaver | (see the Gutenberg header) | have | PG 22288 |
| `singles-nonfiction-2-picq-battle-studies` | Charles Ardant du Picq | Battle Studies; Ancient and Modern Battle | Robert Christie Cotton and John N. Greely | (see the Gutenberg header) | have | PG 7294 |
| `singles-nonfiction-2-preyer-the-mind-of-the-child-part-ii-the-develo` | William T. Preyer | The Mind of the Child, Part II The Development of the Intellect, International Education Series Edited By William T. Harris, Volume IX. | Henry W. Brown | (see the Gutenberg header) | have | PG 19549 |
| `singles-nonfiction-2-quelus-the-natural-history-of-chocolate-being-a` | D. Quélus | The Natural History of Chocolate Being a Distinct and Particular Account of the Cocoa-Tree, its Growth and Culture, and the Preparation, Excellent Properties, and Medicinal Vertues of its Fruit | R. Brookes | (see the Gutenberg header) | have | PG 24588 |
| `singles-nonfiction-2-rapin-de-carmine-pastorali-prefixed-to-thomas` | René Rapin | De Carmine Pastorali Prefixed to Thomas Creech's translation of the Idylliums of Theocritus (1684) | Thomas Creech | (see the Gutenberg header) | have | PG 14495 |
| `singles-nonfiction-2-rathenau-the-new-society` | Walther Rathenau | The New Society | Arthur Windham | (see the Gutenberg header) | have | PG 20936 |
| `singles-nonfiction-2-reggio-a-guide-for-the-religious-instruction-of` | Isaac Samuel Reggio | A Guide for the Religious Instruction of Jewish Youth | M. H. Picciotto | (see the Gutenberg header) | have | PG 21905 |
| `singles-nonfiction-2-rolland-musicians-of-to-day` | Romain Rolland | Musicians of to-day | Mary Blaiklock | (see the Gutenberg header) | have | PG 16467 |
| `singles-nonfiction-2-rosenkranz-pedagogics-as-a-system` | Karl Rosenkranz | Pedagogics as a System | Anna C. Brackett | (see the Gutenberg header) | have | PG 30661 |
| `singles-nonfiction-2-roy-a-new-philosophy` | Edouard Le Roy | A New Philosophy | Vincent Benson | (see the Gutenberg header) | have | PG 1347 |
| `singles-nonfiction-2-sadger-sleep-walking-and-moon-walking` | J. Sadger | Sleep Walking and Moon Walking: A Medico-Literary Study | Louise Brink | (see the Gutenberg header) | have | PG 30556 |
| `singles-nonfiction-2-saint-saens-on-the-execution-of-music-and-principall` | Camille Saint-Saëns | On the Execution of Music, and Principally of Ancient Music | Henry P. Bowie | (see the Gutenberg header) | have | PG 30412 |
| `singles-nonfiction-2-salvator-the-caravan-route-between-egypt-and-syri` | Archduke of Austria Ludwig Salvator | The Caravan Route between Egypt and Syria | Ernst von Hesse-Wartegg | (see the Gutenberg header) | have | PG 26705 |
| `singles-nonfiction-2-sancho-an-account-of-the-conquest-of-peru` | Pedro Sancho | An Account of the Conquest of Peru | Philip Ainsworth Means | (see the Gutenberg header) | have | PG 26602 |
| `singles-nonfiction-2-sand-the-george-sand-gustave-flaubert-letters` | George Sand and Gustave Flaubert | The George Sand-Gustave Flaubert Letters | Aimée L. McKenzie | (see the Gutenberg header) | have | PG 5115 |
| `singles-nonfiction-2-schmid-the-theories-of-darwin-and-their-relatio` | Rudolf Schmid | The Theories of Darwin and Their Relation to Philosophy, Religion, and Morality | G. A. Zimmermann | (see the Gutenberg header) | have | PG 22150 |
| `singles-nonfiction-2-scholten-a-comparative-view-of-religions` | Johannes Henricus Scholten | A Comparative View of Religions | Francis T. Washburn | (see the Gutenberg header) | have | PG 20137 |
| `singles-nonfiction-2-starke-poise` | D. Starke | Poise | Francis Medhurst | (see the Gutenberg header) | have | PG 13877 |
| `singles-nonfiction-2-supino-fra-angelico` | I. B. Supino | Fra Angelico | Leader Scott | (see the Gutenberg header) | have | PG 21561 |
| `singles-nonfiction-2-tavera-the-medicinal-plants-of-the-philippines` | T. H. Pardo de Tavera | The Medicinal Plants of the Philippines | Jerome Beers Thomas | (see the Gutenberg header) | have | PG 26393 |
| `singles-nonfiction-2-tolstoy-tolstoy-on-shakespeare` | Leo Tolstoy | Tolstoy on Shakespeare: A Critical Essay on Shakespeare | V. G. Chertkov and Isabella Fyvie Mayo | (see the Gutenberg header) | have | PG 27726 |
| `singles-nonfiction-2-tosi-observations-on-the-florid-song` | Pier Francesco Tosi | Observations on the Florid Song; Or, Sentiments on the Ancient and Modern Singers | John Ernest Galliard | (see the Gutenberg header) | have | PG 26477 |
| `singles-nonfiction-2-valentinus-of-natural-and-supernatural-things-also` | Basilius Valentinus | Of Natural and Supernatural Things Also of the first Tincture, Root, and Spirit of Metals and Minerals, how the same are Conceived, Generated, Brought forth, Changed, and Augmented. | Daniel Cable | (see the Gutenberg header) | have | PG 26340 |
| `singles-nonfiction-2-wagner-on-conducting-ueber-das-dirigiren` | Richard Wagner | On Conducting (Üeber Das Dirigiren) : A Treatise on Style in the Execution of Classical Music | Edward Dannreuther | (see the Gutenberg header) | have | PG 4523 |
| `singles-nonfiction-2-wagner-the-simple-life` | Charles Wagner | The Simple Life | Mary Louise Hendee | (see the Gutenberg header) | have | PG 23092 |
| `singles-nonfiction-2-yajnavalkya-hindu-law-and-judicature-from-the-dharma` | Yajñavalkya | Hindu Law and Judicature from the Dharma-Sástra of Yájnavalkya | W. A. Montriou and Edward Röer | (see the Gutenberg header) | have | PG 21918 |
| `singles-nonfiction-2-yoritomo-tashi-common-sense-how-to-exercise-it` | Yoritomo-Tashi | Common sense, how to exercise it | Lily Kendall Beers Berthelot de la Boileverie | (see the Gutenberg header) | have | PG 13072 |
| — | — | ferrer-30174: Fernández Bolívar's Mathematical-Historical Principles: author born 1923, so a modern work. | — | — | excluded | — |
| — | — | cunningham-28921: Nicole's Essay on True and Apparent Beauty: J. V. Cunningham translated it for the Augustan Reprint Society in 1950, so it is not a pre-1931 printing. | — | — | excluded | — |

## One-off translations: the last of the single-translator list (Calthrop's Sun Tzu, Bose and Saha's Principle of Relativity, Renouf's Book of the Dead, Tocqueville's Old Regime, Life of Pasteur, Gautier, Rolland, Duhamel, Claudel)

Shelf: `pipeline/singles-remainder_shelf.json` · fetch `python3 pipeline/fetch_shelf.py singles-remainder` · titles `python3 pipeline/split_shelf_titles.py singles-remainder`.
Round 52 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `singles-remainder-anon-the-egyptian-book-of-the-dead` | Ancient Egyptian funerary texts (anonymous) | The Egyptian Book of the dead | P. Le Page Renouf and Edouard Naville | (see the Gutenberg header) | have | PG 69566 |
| `singles-remainder-anon-the-taleef-shereef` | anonymous (an Indian materia medica in Persian) | The Taleef Shereef; Or, Indian Materia Medica | George Playfair | (see the Gutenberg header) | have | PG 53755 |
| `singles-remainder-boschere-the-city-curious` | Jean de Boschère | The City Curious | F. Tennyson Jesse | (see the Gutenberg header) | have | PG 32406 |
| `singles-remainder-bull-fridtjof-nansen` | Jacob B. Bull | Fridtjof Nansen: A Book for the Young | M. R. Barnard | (see the Gutenberg header) | have | PG 38026 |
| `singles-remainder-claudel-the-east-i-know` | Paul Claudel | The East I know | Teresa Frances Benét and William Rose Benét | (see the Gutenberg header) | have | PG 70971 |
| `singles-remainder-duhamel-civilisation-1914-1918` | Georges Duhamel | Civilisation 1914-1918 | T. P. Conwell-Evans | (see the Gutenberg header) | have | PG 68774 |
| `singles-remainder-einstein-the-principle-of-relativity` | Albert Einstein and H. Minkowski | The Principle of Relativity | Satyendranath Bose and Meghnad Saha | (see the Gutenberg header) | have | PG 66944 |
| `singles-remainder-gautier-my-household-of-pets` | Théophile Gautier | My household of pets | Susan Coolidge | (see the Gutenberg header) | have | PG 65665 |
| `singles-remainder-gautier-wanderings-in-spain` | Théophile Gautier | Wanderings in Spain | Thomas Robert McQuoid | (see the Gutenberg header) | have | PG 52763 |
| `singles-remainder-guiccioli-my-recollections-of-lord-byron` | Teresa Guiccioli | My Recollections of Lord Byron | Hubert E. H. Jerningham | (see the Gutenberg header) | have | PG 25977 |
| `singles-remainder-guizot-meditations-and-moral-sketches` | François Guizot | Meditations and Moral Sketches | John Butler Ormonde | (see the Gutenberg header) | have | PG 60705 |
| `singles-remainder-hammer-purgstall-the-history-of-the-assassins-derived-fro` | Joseph Hammer-Purgstall | The History of the Assassins, Derived from Oriental Sources | Oswald Charles Wood | (see the Gutenberg header) | have | PG 53023 |
| `singles-remainder-hurgronje-the-holy-war-made-in-germany` | C. Snouck Hurgronje | The holy war "made in Germany" | Joseph E. Gillet | (see the Gutenberg header) | have | PG 69537 |
| `singles-remainder-khayyam-the-sufism-of-the-rubaiyat-or-the-secret` | Omar Khayyam | The Sufism of the Rubáiyát, or, the Secret of the Great Paradox | Norton F. W. Hazeldine | (see the Gutenberg header) | have | PG 50619 |
| `singles-remainder-mauclair-auguste-rodin` | Camille Mauclair | Auguste Rodin: The Man - His Ideas - His Works | Clementina Black | (see the Gutenberg header) | have | PG 50665 |
| `singles-remainder-muhlen-fairy-tales-for-workers-children` | Hermynia Zur Mühlen | Fairy Tales for Workers' Children | Ida Dailes | (see the Gutenberg header) | have | PG 66687 |
| `singles-remainder-o-rell-jonathan-and-his-continent` | Max O'Rell and Jack Allyn | Jonathan and His Continent: Rambles Through American Society | Mary Bartlett Blouët | (see the Gutenberg header) | have | PG 34679 |
| `singles-remainder-perelaer-ran-away-from-the-dutch` | M. T. H. Perelaer | Ran away from the Dutch | Maurice Blok | (see the Gutenberg header) | have | PG 71401 |
| `singles-remainder-reventlow-the-vampire-of-the-continent` | E. Reventlow | The Vampire of the Continent | Georges Chatterton-Hill | (see the Gutenberg header) | have | PG 66468 |
| `singles-remainder-rolland-above-the-battle` | Romain Rolland | Above the Battle | C. K. Ogden | (see the Gutenberg header) | have | PG 32779 |
| `singles-remainder-saintine-the-solitary-of-juan-fernandez-or-the-re` | X.-B. Saintine | The Solitary of Juan Fernandez, or the Real Robinson Crusoe | Anne Topan Wilbur Wood | (see the Gutenberg header) | have | PG 11441 |
| `singles-remainder-sunzi-the-book-of-war` | Sunzi and Qi Wu | The Book of War: The Military Classic of the Far East The Articles of Suntzu; The Sayings of Wutzu | Everard Ferguson Calthrop | (see the Gutenberg header) | have | PG 44024 |
| `singles-remainder-tcheng-chin-chin` | Ki-tong Tcheng | Chin-Chin; Or, The Chinaman at Home | Robert Harborough Sherard | (see the Gutenberg header) | have | PG 58371 |
| `singles-remainder-tocqueville-the-state-of-society-in-france-before-th` | Alexis de Tocqueville | The State of Society in France Before the Revolution of 1789 And the Causes Which Led to That Event | Henry Reeve | (see the Gutenberg header) | have | PG 54187 |
| `singles-remainder-unknown-the-descent-of-the-sun` | F. W. Bain (presented as from a Sanskrit manuscript) | The descent of the sun: A cycle of birth | F. W. Bain | (see the Gutenberg header) | have | PG 68641 |
| `singles-remainder-vallery-radot-the-life-of-pasteur` | René Vallery-Radot | The life of Pasteur | R. L. Devonshire | (see the Gutenberg header) | have | PG 60956 |

## Series shelf: the Broadway Library of XVIII Century French Literature (Routledge, ed. Aldington, 1927): Diderot's Dialogues, Crébillon's The Sofa, the Prince de Ligne, Richelieu, the Memoirs of the Bastille

Shelf: `pipeline/broadway-library_shelf.json` · fetch `python3 pipeline/fetch_shelf.py broadway-library` · titles `python3 pipeline/split_shelf_titles.py broadway-library`.
Round 55 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `broadway-diderot-dialogues` | Denis Diderot | Dialogues | Francis Birrell | 1927 | have-raw | IA `in.ernet.dli.2015.84138` |
| `broadway-crebillon-the-sofa` | Claude-Prosper Jolyot de Crébillon (Crébillon fils) | The Sofa: A Moral Tale | Bonamy Dobrée | 1927 | have-raw | IA `in.ernet.dli.2015.186140` |
| `broadway-ligne-letters-and-memoirs` | Charles-Joseph, Prince de Ligne | Letters and Memoirs of the Prince de Ligne | Leigh Ashton | 1927 | have-raw | IA `lettersmemoirsof0000leig` |
| `broadway-private-life-of-richelieu` | anonymous (La Vie privée du maréchal de Richelieu, 1791) | The Private Life of the Marshal Duke of Richelieu | F. S. Flint | 1927 | have-raw | IA `privatelifeofmar0000fsfl` |
| `broadway-memoirs-of-the-bastille` | Jean Henri Latude and Simon-Nicolas-Henri Linguet | Memoirs of the Bastille | J. and S. F. Mills Whitham | 1927 | have-raw | IA `memoirsofbastill0000latu` |
| `broadway-lespinasse-love-letters` | Julie de Lespinasse and the Comte de Guibert | Love Letters of Mlle de Lespinasse to and from the Comte de Guibert | E. H. F. Mills | 1929 | have-raw | IA `lovelettersofmll0000dele` |
| `broadway-marmontel` | — | Memoirs of Marmontel, tr. Brigit Patmore (Routledge, 1930; archive.org memoirsofmarmont00marm): a 1930 printing, so it waits on the 1930 ruling. | — | — | pending | — |
| `broadway-rousseau-reveries` | — | The Reveries of a Solitary, tr. John Gould Fletcher (Routledge, 1927; archive.org dli.ministry.22007, undated scan): Rousseau has another lane's shelf (rousseau), so it is left for that lane. | — | — | pending | — |
| `broadway-not-found` | — | No open scan found (searched 2026-10-17): Diderot's Memoirs of a Nun (Birrell, 1928), Madame du Hausset's Memoirs of Madame de Pompadour (Flint, 1928), Crébillon/Voisenon/Montesquieu short stories (Jackson), Joubert (H. P. Collins), Madame de Staal-Delaunay (Raymond Mortimer), the September Massacres (Partridge), Paradis de Moncrif's Zeloide (Scott Moncrieff), Madame d'Epinay (Allingham), Voltaire and du Deffand. | — | — | pending | — |

## Series shelf: The Broadway Travellers (Routledge, ed. Denison Ross and Eileen Power, 1926-29): Tafur, Clavijo, Ibn Battuta, Bontekoe, Cortés, Mornay, Don Juan of Persia, Akbar and the Jesuits, Bernal Díaz

Shelf: `pipeline/broadway-travellers_shelf.json` · fetch `python3 pipeline/fetch_shelf.py broadway-travellers` · titles `python3 pipeline/split_shelf_titles.py broadway-travellers`.
Round 56 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `broadway-travellers-tafur` | Pero Tafur | Travels and Adventures, 1435-1439 | Malcolm Letts | 1926 | have-raw | IA `ldpd_6352599_000` |
| `broadway-travellers-clavijo` | Ruy González de Clavijo | Embassy to Tamerlane, 1403-1406 | Guy Le Strange | 1928 | have-raw | IA `b31354932` |
| `broadway-travellers-ibn-battuta` | Ibn Battuta | Travels in Asia and Africa, 1325-1354 (selections) | H. A. R. Gibb | 1929 | have-raw | IA `pli.kerala.rare.27987` |
| `broadway-travellers-bontekoe` | Willem Ysbrandsz. Bontekoe | Memorable Description of the East Indian Voyage, 1618-25 | C. B. Bodde-Hodgkinson and Pieter Geyl | 1929 | have-raw | IA `memorabledescrip0000bont` |
| `broadway-travellers-cortes-five-letters` | Hernán Cortés | Five Letters, 1519-1526 | J. Bayard Morris | 1928 | have-raw | IA `dli.ministry.13876` |
| `broadway-travellers-huguenot-family` | Charlotte Arbaleste, Madame de Mornay | A Huguenot Family in the XVI Century: the Memoirs of Philippe de Mornay, Sieur du Plessis Marly, written by his wife | Lucy Crump | 1926 | have-raw | IA `huguenotfamilyin0000morn` |
| `broadway-travellers-don-juan-of-persia` | Don Juan of Persia (Uruch Beg) | Don Juan of Persia, a Shi'ah Catholic, 1560-1604 | Guy Le Strange | 1926 | have-raw | IA `donjuanofpersias00juan` |
| `broadway-travellers-akbar-and-the-jesuits` | Pierre du Jarric | Akbar and the Jesuits: an account of the Jesuit missions to the court of Akbar | C. H. Payne | 1926 | have-raw | IA `akbarjesuitsacco00duja` |
| `broadway-travellers-bernal-diaz` | Bernal Díaz del Castillo | The Discovery and Conquest of Mexico, 1517-1521 | A. P. Maudslay | 1928 | have-raw | IA `bernaldiazdelcas002605mbp` |
| `broadway-travellers-1930` | — | Printed in 1930, so waiting on the 1930 ruling: Jahangir and the Jesuits (C. H. Payne; dli.ministry.03303), Jewish Travellers (Elkan Nathan Adler; McGillLibrary-108936-464), Madame d'Aulnoy's Travels into Spain (dli.ministry.04080) and Boxer's Commentaries of Ruy Freyre de Andrada. | — | — | pending | — |
| `broadway-travellers-1931` | — | The Travels of an Alchemist (Arthur Waley, 1931) is too late. | — | — | pending | — |
| — | — | huc-gabet: Huc and Gabet's Travels in Tartary (1928 reissue) is Hazlitt's 1852 translation, already on the hazlitt-huc shelf. | — | — | excluded | — |
| — | — | ia-travelsinasiaafr0000muha: A later reprint of Gibb's Ibn Battuta (front matter lists years to 1969). | — | — | excluded | — |

## Series shelf: Routledge's Broadway Translations and Broadway Medieval Library (1920s): Lunacharsky's Three Plays, Paton's Sir Lancelot of the Lake, Mabbe's Celestina, the English Faust Book

Shelf: `pipeline/broadway-translations_shelf.json` · fetch `python3 pipeline/fetch_shelf.py broadway-translations` · titles `python3 pipeline/split_shelf_titles.py broadway-translations`.
Round 57 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `broadway-translations-lunacharski-three-plays` | Anatoly Lunacharsky | Three Plays: Faust and the City, Vasilisa the Wise, The Magi | L. A. Magnus and K. Walter | 1923 | have-raw | IA `bwb_KU-774-607` |
| `broadway-translations-sir-lancelot-of-the-lake` | anonymous (the Old French prose Lancelot) | Sir Lancelot of the Lake: a French prose romance of the thirteenth century | Lucy Allen Paton | 1929 | have-raw | IA `sirlancelotofthelakelapatton` |
| `broadway-translations-celestina-mabbe` | Fernando de Rojas | Celestina, or The Tragi-Comedy of Calisto and Melibea | James Mabbe | 1631 | have-raw | IA `celestinaortragi00roja` |
| `broadway-translations-english-faust-book` | anonymous (the German Faustbuch, 1587) | The History of the Damnable Life and Deserved Death of Doctor John Faustus (1592), with The Second Report of Faustus (1594) | P. F., Gent. (the English Faust Book; the Second Report is anonymous) | 1592 | have-raw | IA `historyofdamnabl0000unse_o0d7` |
| `broadway-translations-guibert-autobiography` | Guibert of Nogent | The Autobiography of Guibert, Abbot of Nogent-sous-Coucy (De vita sua) | C. C. Swinton Bland | 1925 | have-raw | IA `autobiographyofg00guib` |
| `broadway-translations-1930` | — | Letters of George Sand, selected and translated by Veronica Lucas (Routledge, 1930; lettersofgeorges0000geor): a 1930 printing, waiting on the 1930 ruling. | — | — | pending | — |
| `broadway-medieval-lane-a` | — | Left for Lane A as devotional collections: Caesarius of Heisterbach's Dialogue on Miracles (H. von E. Scott and C. C. Swinton Bland, 1929, 2 vols; caesariusthedialogueonmiraclesvol.1/.2) and Johannes Herolt's Miracles of the Blessed Virgin Mary (Bland, 1928; miraclesoftheblessedvirginherolt), both Broadway Medieval Library. | — | — | pending | — |
| — | — | esquemeling: Esquemeling's Buccaneers of America (1684 translation, Broadway 1926): the same text is already held inside pyle's Buccaneers and Marooners of America (PG 73564). | — | — | excluded | — |
| — | — | classical: Petronius (Mitchell, 1923), Alciphron (Wright, 1922), Lucretius (1920) and The Mirror of Venus (Wright, 1925) are classical, so left for Lane B. | — | — | excluded | — |

## Eileen Power as translator: The Goodman of Paris (1928) and Boissonnade's Life and Work in Medieval Europe (1927)

Shelf: `pipeline/eileen-power_shelf.json` · fetch `python3 pipeline/fetch_shelf.py eileen-power` · titles `python3 pipeline/split_shelf_titles.py eileen-power`.
Round 58 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `eileen-power-goodman-of-paris` | anonymous (Le Ménagier de Paris, c. 1393) | The Goodman of Paris: a treatise on moral and domestic economy by a citizen of Paris | Eileen Power | 1928 | have-raw | IA `in.ernet.dli.2015.166239` |
| `eileen-power-boissonnade-life-and-work` | Prosper Boissonnade | Life and Work in Medieval Europe (Fifth to Fifteenth Centuries) | Eileen Power | 1927 | have-raw | IA `dli.ministry.16291` |
| — | — | later-reprints: Life and Work in Medieval Europe also survives as Harper Torchbooks (1964), Dover (2002) and Dorset (1987) reprints; only the 1927 printing is used. | — | — | excluded | — |

## Series shelf: Kegan Paul's History of Civilization (ed. C. K. Ogden, 1925-27): Febvre, Moret and Davy, Delaporte (V. Gordon Childe), Huart, Moret's Nile (M. R. Dobie), Pittard, Renard, Perrier

Shelf: `pipeline/history-of-civilization_shelf.json` · fetch `python3 pipeline/fetch_shelf.py history-of-civilization` · titles `python3 pipeline/split_shelf_titles.py history-of-civilization`.
Round 59 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `history-of-civilization-febvre` | Lucien Febvre (with Lionel Bataillon) | A Geographical Introduction to History | E. G. Mountford and J. H. Paxton | 1925 | have-raw | IA `geographicalintr0000luci_e9f4` |
| `history-of-civilization-from-tribe-to-empire` | Alexandre Moret and Georges Davy | From Tribe to Empire: social organization among primitives and in the ancient East | V. Gordon Childe | 1926 | have-raw | IA `fromtribetoempir00more` |
| `history-of-civilization-delaporte-mesopotamia` | Louis Delaporte | Mesopotamia: the Babylonian and Assyrian Civilization | V. Gordon Childe | 1925 | have-raw | IA `mesopotamiababyl00dela` |
| `history-of-civilization-huart-ancient-persia` | Clément Huart | Ancient Persia and Iranian Civilization | M. R. Dobie | 1927 | have-raw | IA `in.ernet.dli.2015.73398` |
| `history-of-civilization-moret-nile` | Alexandre Moret | The Nile and Egyptian Civilization | M. R. Dobie | 1927 | have-raw | IA `nileegyptiancivi00more` |
| `history-of-civilization-pittard-race-and-history` | Eugène Pittard | Race and History: an Ethnological Introduction to History | V. C. C. Collum | 1926 | have-raw | IA `dli.ministry.19521` |
| `history-of-civilization-renard-life-and-work-modern` | Georges Renard and Georges Weulersse | Life and Work in Modern Europe (Fifteenth to Eighteenth Centuries) | Margaret Richards | 1926 | have-raw | IA `lifeworkinmodern0000rena` |
| `history-of-civilization-perrier-earth-before-history` | Edmond Perrier | The Earth before History: Man's Origin and the Origin of Life | Paul Radin | 1925 | have-raw | IA `earthbeforehisto00perr` |
| `history-of-civilization-1930` | — | Granet's Chinese Civilization (1930) and later volumes wait on the 1930 ruling or are too late. | — | — | pending | — |
| — | — | classical: Glotz (The Aegean Civilization, Ancient Greece at Work, The Greek City), Jardé (The Formation of the Greek People) and Homo (Primitive Italy) are Greek and Roman scholarship, left for Lane B. | — | — | excluded | — |
| — | — | ia-in.ernet.dli.2015.107710: The Nile and Egyptian Civilization: 'Reissued 1972'; used only as evidence of the translator's name. | — | — | excluded | — |

## Series shelf: the Wisdom of the East (Orient Press and John Murray, 1904-): Lionel Giles's Lieh Tzu and Lao Tzu, Forke's Yang Chu, Cranmer-Byng's Lute of Jade, Feast of Lanterns, Odes, Hafiz and Sa'di, Walsh, Hoshino, Morrison, Field's al-Ghazali, E. J. Thomas's Buddhist Scriptures and Vedic Hymns, Barnett's Santideva, the Dhammapada, Lederer's Shabistari, Wollaston, Zeb-un-Nissa, Baerlein's Abu'l-Ala, Wortabet, Collins's Bahya, Cohen, Dennis's Burden of Isis, Gorn Old's Shu King, Ku Hung-Ming

Shelf: `pipeline/wisdom-of-the-east_shelf.json` · fetch `python3 pipeline/fetch_shelf.py wisdom-of-the-east` · titles `python3 pipeline/split_shelf_titles.py wisdom-of-the-east`.
Round 60 (2026-10-17), vetoable: East Asian volumes. Round 61 (2026-10-17), vetoable: Indian, Persian, Arabic, Hebrew and Egyptian volumes. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `wisdom-of-the-east-lieh-tzu` | Liezi (Lieh Tzu) | Taoist Teachings from the Book of Lieh Tzu | Lionel Giles | 1912 | have-raw | IA `taoistteachingsf00liezrich` |
| `wisdom-of-the-east-lao-tzu` | Laozi (Lao Tzu) | The Sayings of Lao Tzu | Lionel Giles | 1904 | have-raw | IA `sayingslaotz00gilegoog` |
| `wisdom-of-the-east-yang-chu` | Yang Zhu (Yang Chu), from the Liezi | Yang Chu's Garden of Pleasure | Anton Forke | 1912 | have-raw | IA `yangchusgardenof00yanguoft` |
| `wisdom-of-the-east-lute-of-jade` | Classical Chinese poets (Li Po, Tu Fu and others) | A Lute of Jade | L. Cranmer-Byng | 1909 | have | PG 390 |
| `wisdom-of-the-east-feast-of-lanterns` | Classical Chinese poets | A Feast of Lanterns | L. Cranmer-Byng | 1916 | have-raw | IA `feastoflanterns00cran` |
| `wisdom-of-the-east-odes` | The Shijing (Book of Odes) | The Odes of Confucius | L. Cranmer-Byng | 1905 | have-raw | IA `odesofconfucius00craniala` |
| `wisdom-of-the-east-master-singers` | Japanese poets from the Manyoshu onward | The Master-Singers of Japan | Clara A. Walsh | 1910 | have-raw | IA `india.history.resource.91749` |
| `wisdom-of-the-east-way-of-contentment` | Kaibara Ekiken | The Way of Contentment | Ken Hoshino | 1913 | have-raw | IA `wayofcontentment00kaibrich` |
| `wisdom-of-the-east-ti-me-kun-dan` | Anonymous Tibetan mystery play | Ti-Me-Kun-Dan, Prince of Buddhist Benevolence | Millicent H. Morrison | 1925 | have-raw | IA `in.ernet.dli.2015.106823` |
| `wisdom-of-the-east-alchemy-of-happiness` | Al-Ghazali | The Alchemy of Happiness | Claud Field | 1910 | have-raw | IA `in.ernet.dli.2015.106793` |
| `wisdom-of-the-east-buddhist-scriptures` | The Pali Canon (selections) | Buddhist Scriptures | E. J. Thomas | 1913 | have-raw | IA `india.history.resource.112174` |
| `wisdom-of-the-east-vedic-hymns` | The Rigveda (selections) | Vedic Hymns | Edward J. Thomas | 1923 | have-raw | IA `bwb_W9-DJJ-947` |
| `wisdom-of-the-east-path-of-light` | Śāntideva | The Path of Light (the Bodhicaryāvatāra) | L. D. Barnett | 1909 | have-raw | IA `pathoflight00sant` |
| `wisdom-of-the-east-way-of-virtue` | The Dhammapada | The Buddha's 'Way of Virtue' | W. D. C. Wagiswara and K. J. Saunders | 1912 | have-raw | IA `thebuddhaswayof00unknuoft` |
| `wisdom-of-the-east-rubaiyat-of-hafiz` | Hafiz | The Ruba'iyat of Hafiz | Syed Abdul Majid and L. Cranmer-Byng | 1910 | have-raw | IA `rubaiyatofhafiz00hafi` |
| `wisdom-of-the-east-secret-rose-garden` | Mahmud Shabistari | The Secret Rose Garden (Gulshan-i Raz) | Florence Lederer | 1920 | have-raw | IA `secretrosegarden00shabiala-2` |
| `wisdom-of-the-east-rose-garden-of-sadi` | Sa'di | The Rose-Garden of Sa'di (from the Gulistan) | L. Cranmer-Byng | 1910 | have-raw | IA `in.ernet.dli.2015.460102` |
| `wisdom-of-the-east-scroll-of-wisdom` | Sa'di (attributed) | Sadi's Scroll of Wisdom (Pand-nama) | Arthur N. Wollaston | 1906 | have-raw | IA `scrollofwisdomwi00sadiuoft` |
| `wisdom-of-the-east-diwan-of-zeb-un-nissa` | Zeb-un-Nissa | The Diwan of Zeb-un-Nissa | Magan Lal and Jessie Duncan Westbrook | 1913 | have-raw | IA `diwanofzebunniss00zebuuoft` |
| `wisdom-of-the-east-diwan-of-abul-ala` | Abu'l-Ala al-Ma'arri | The Diwan of Abu'l-Ala | Henry Baerlein | 1909 | have | PG 13086 |
| `wisdom-of-the-east-arabian-wisdom` | Arabic proverbs and sayings | Arabian Wisdom | John Wortabet | 1916 | have | PG 33109 |
| `wisdom-of-the-east-duties-of-the-heart` | Bahya ibn Paquda | The Duties of the Heart (selections) | Edwin Collins | 1904 | have-raw | IA `india.history.resource.111766` |
| `wisdom-of-the-east-jewish-proverbs` | Talmud and Midrash (proverbs) | Ancient Jewish Proverbs | A. Cohen | 1911 | have-raw | IA `ancientjewishpro0000cohe` |
| `wisdom-of-the-east-burden-of-isis` | Ancient Egyptian (the Lamentations of Isis and Nephthys) | The Burden of Isis | James Teackle Dennis | 1910 | have-raw | IA `burdenofisis00isisiala` |
| `wisdom-of-the-east-book-of-history` | The Shujing (Book of History) | The Classics of Confucius: Book of History | W. Gorn Old | 1906 | have-raw | IA `classicsconfuci00sephgoog` |
| `wisdom-of-the-east-conduct-of-life` | The Zhongyong (Doctrine of the Mean) | The Conduct of Life, or the Universal Order of Confucius | Ku Hung-Ming | 1906 | have-raw | IA `conductoflifeoru0000unse` |
| `women-and-wisdom-of-japan` | — | Women and Wisdom of Japan (Murray, 1905; india.history.resource.91283): the Onna Daigaku and its sequel in English, but the title page names only Shingoro Takaishi as writer of the introduction, and the text read so far never says who translated. Held back until the translator is established. | — | — | pending | — |
| `legends-of-indian-buddhism` | — | Legends of Indian Buddhism (Murray, 1911; india.history.resource.112118): six legends translated from Burnouf's French, but the title page names Winifred Stephens only for the introduction and the text read never says who translated. Held back with Women and Wisdom of Japan until the translator is established. | — | — | pending | — |
| — | — | musings-of-a-chinese-mystic: Musings of a Chinese Mystic (Lionel Giles, 1906; musingschinesem00zhua): selections from H. A. Giles's 1889 Chuang Tzu translation, which its own note credits and which the giles shelf already holds whole. | — | — | excluded | — |
| — | — | sayings-of-confucius: Lionel Giles's Sayings of Confucius (1907) is already on the giles shelf (PG 46389). | — | — | excluded | — |
| — | — | held-in-singles: Already held on lane C's singles shelves: Gunn's Instruction of Ptah-hotep (PG 30508, singles-ideas), Bronnle's Awakening of the Soul (PG 34572, singles-ideas) and Ivan Chen's Book of Filial Duty (PG 75878, singles-ideas-3), and A. Hart Edwards's Bustan of Sadi (1911; PG 60471, singles-plays-poetry-2). | — | — | excluded | — |
| — | — | confessions-of-al-ghazzali: Claud Field's Confessions of Al Ghazzali (1909) is already on the claud-field shelf. | — | — | excluded | — |
| — | — | not-translations: Studies rather than translations, so off a translators' shelf: Yone Noguchi's Spirit of Japanese Poetry (1914, his lectures), E. V. Gatenby's Cloud-Men of Yamato (1929, 'an outline of mysticism in Japanese literature'), and M. A. Murray's Ancient Egyptian Legends (1913), which she says she 'retold ... in my own way'. | — | — | excluded | — |
| — | — | wisdom-of-the-apocrypha: The Wisdom of the Apocrypha (1910) uses the Revised Version text (its prefatory note says so), so it is not a new translation. | — | — | excluded | — |
| — | — | religion-of-the-koran: Wollaston's Religion of the Koran (1904): its Koran passages are 'taken from the Translation by the late Professor E. H. Palmer' (Sacred Books of the East, 1880), which the palmer shelf holds. | — | — | excluded | — |
| — | — | persian-mystics-davis: F. Hadland Davis's Persian Mystics: Rumi (1907) and Jami (1908) (PG 45159, 45158): anthologies of other men's translations by permission (Whinfield and Nicholson in the Rumi volume, FitzGerald and others in the Jami), not new translations. | — | — | excluded | — |
| — | — | studies: Authored studies rather than translations: Herbert Baynes's Way of the Buddha (1906, 'the treatise'), L. D. Barnett's Brahma-Knowledge (1907, 'an outline of the philosophy of the Vedanta') and Heart of India (1908, 'sketches'), and S. A. Kapadia's Teachings of Zoroaster (1905, 'by S. A. Kapadia'). Eric Hammond's Splendour of God (1911) is a compilation of Baha'i extracts whose front matter names no translator. | — | — | excluded | — |

## Series shelf: the Sacred Books of the East (Clarendon Press, 1879-1910), the volumes not on muller, palmer or legge: Rhys Davids's Buddhist Suttas and Milinda, the Vinaya Texts, Beal, Kern's Lotus Sutra, Jacobi's Jaina Sutras, Buddhist Mahayana Texts, Darmesteter's and Mills's Zend-Avesta, West's Pahlavi Texts, Bühler's Sacred Laws and Manu, Jolly, Telang's Bhagavadgita, Oldenberg's Grihya-sutras and Vedic Hymns, Eggeling's Satapatha-Brahmana, Müller's Vedic Hymns, Bloomfield's Atharva-Veda, Thibaut's Vedanta-Sutras

Shelf: `pipeline/sacred-books-of-the-east_shelf.json` · fetch `python3 pipeline/fetch_shelf.py sacred-books-of-the-east` · titles `python3 pipeline/split_shelf_titles.py sacred-books-of-the-east`.
Round 62 (2026-10-17), vetoable: Buddhist and Jain volumes. Round 63: Zoroastrian and Hindu law volumes. Round 64: Vedic and Vedanta volumes. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `sacred-books-of-the-east-buddhist-suttas` | The Pali Canon (seven suttas, the Maha-parinibbana Suttanta first) | Buddhist Suttas | T. W. Rhys Davids | 1881 | have-raw | IA `in.ernet.dli.2015.217508` |
| `sacred-books-of-the-east-vinaya-1` | The Vinaya Pitaka | Vinaya Texts, part I (the Patimokkha; Mahavagga I-IV) | T. W. Rhys Davids and Hermann Oldenberg | 1881 | have-raw | IA `in.ernet.dli.2015.217507` |
| `sacred-books-of-the-east-vinaya-2` | The Vinaya Pitaka | Vinaya Texts, part II (Mahavagga V-X and more) | T. W. Rhys Davids and Hermann Oldenberg | 1882 | have-raw | IA `in.ernet.dli.2015.217606` |
| `sacred-books-of-the-east-vinaya-3` | The Vinaya Pitaka | Vinaya Texts, part III | T. W. Rhys Davids and Hermann Oldenberg | 1885 | have-raw | IA `in.ernet.dli.2015.283711` |
| `sacred-books-of-the-east-fo-sho-hing-tsan-king` | Asvaghosa, in Dharmaraksha's Chinese version | The Fo-sho-hing-tsan-king, a Life of Buddha | Samuel Beal | 1883 | have-raw | IA `in.ernet.dli.2015.217599` |
| `sacred-books-of-the-east-saddharma-pundarika` | The Saddharmapundarika Sutra | The Saddharma-pundarika, or the Lotus of the True Law | H. Kern | 1884 | have-raw | IA `sacredbooksofthe014253mbp` |
| `sacred-books-of-the-east-jaina-sutras-1` | The Jain Agamas | Jaina Sutras, part I (with the Kalpa Sutra) | Hermann Jacobi | 1884 | have-raw | IA `in.ernet.dli.2015.168707` |
| `sacred-books-of-the-east-jaina-sutras-2` | The Jain Agamas | Jaina Sutras, part II (with the Uttaradhyayana Sutra) | Hermann Jacobi | 1895 | have-raw | IA `in.ernet.dli.2015.188663` |
| `sacred-books-of-the-east-milinda-1` | The Milindapanha | The Questions of King Milinda, part I | T. W. Rhys Davids | 1890 | have-raw | IA `in.ernet.dli.2015.217506` |
| `sacred-books-of-the-east-milinda-2` | The Milindapanha | The Questions of King Milinda, part II | T. W. Rhys Davids | 1894 | have-raw | IA `in.ernet.dli.2015.175350` |
| `sacred-books-of-the-east-mahayana-texts` | Asvaghosa's Buddhacarita and the Sukhavati, Vajracchedika and Prajnaparamita sutras | Buddhist Mahayana Texts | E. B. Cowell, F. Max Müller and J. Takakusu | 1894 | have-raw | IA `in.ernet.dli.2015.175347` |
| `sacred-books-of-the-east-zend-avesta-1` | The Avesta | The Zend-Avesta, part I (the Vendidad) | James Darmesteter | 1880 | have-raw | IA `in.ernet.dli.2015.205057` |
| `sacred-books-of-the-east-pahlavi-1` | Zoroastrian Pahlavi literature | Pahlavi Texts, part I | E. W. West | 1880 | have-raw | IA `in.ernet.dli.2015.175343` |
| `sacred-books-of-the-east-pahlavi-2` | Zoroastrian Pahlavi literature | Pahlavi Texts, part II | E. W. West | 1882 | have-raw | IA `in.ernet.dli.2015.215926` |
| `sacred-books-of-the-east-zend-avesta-2` | The Avesta | The Zend-Avesta, part II | James Darmesteter | 1883 | have-raw | IA `in.ernet.dli.2015.215924` |
| `sacred-books-of-the-east-pahlavi-3` | Zoroastrian Pahlavi literature | Pahlavi Texts, part III | E. W. West | 1885 | have-raw | IA `in.ernet.dli.2015.215927` |
| `sacred-books-of-the-east-zend-avesta-3` | The Avesta | The Zend-Avesta, part III | L. H. Mills | 1887 | have-raw | IA `in.ernet.dli.2015.152855` |
| `sacred-books-of-the-east-pahlavi-4` | Zoroastrian Pahlavi literature | Pahlavi Texts, part IV | E. W. West | 1892 | have-raw | IA `in.ernet.dli.2015.88823` |
| `sacred-books-of-the-east-pahlavi-5` | Zoroastrian Pahlavi literature | Pahlavi Texts, part V | E. W. West | 1897 | have-raw | IA `in.ernet.dli.2015.220646` |
| `sacred-books-of-the-east-sacred-laws-1` | The Dharmasutras of Apastamba and Gautama | The Sacred Laws of the Aryas, part I | Georg Bühler | 1879 | have-raw | IA `in.ernet.dli.2015.283698` |
| `sacred-books-of-the-east-institutes-of-vishnu` | The Vishnu Smriti | The Institutes of Vishnu | Julius Jolly | 1880 | have-raw | IA `india.history.resource.85789` |
| `sacred-books-of-the-east-bhagavadgita` | The Bhagavadgita, Sanatsugatiya and Anugita | The Bhagavadgita with the Sanatsugatiya and the Anugita | Kashinath Trimbak Telang | 1882 | have-raw | IA `sacredbooksofthe015782mbp` |
| `sacred-books-of-the-east-sacred-laws-2` | The Dharmasutras of Vasishtha and Baudhayana | The Sacred Laws of the Aryas, part II | Georg Bühler | 1882 | have-raw | IA `in.ernet.dli.2015.189031` |
| `sacred-books-of-the-east-laws-of-manu` | The Manusmriti | The Laws of Manu | Georg Bühler | 1886 | have-raw | IA `dli.ernet.237984` |
| `sacred-books-of-the-east-grihya-sutras-1` | The Grihyasutras | The Grihya-sutras, part I | Hermann Oldenberg | 1886 | have-raw | IA `in.ernet.dli.2015.215928` |
| `sacred-books-of-the-east-grihya-sutras-2` | The Grihyasutras and the Yajna-paribhasha-sutras | The Grihya-sutras, part II | Hermann Oldenberg and F. Max Müller | 1892 | have-raw | IA `in.ernet.dli.2015.189030` |
| `sacred-books-of-the-east-minor-law-books` | Narada and Brihaspati | The Minor Law-Books, part I | Julius Jolly | 1889 | have-raw | IA `in.ernet.dli.2015.283710` |
| `sacred-books-of-the-east-satapatha-1` | The Satapatha Brahmana | The Satapatha-Brahmana, part I | Julius Eggeling | 1882 | have-raw | IA `dli.ernet.5376` |
| `sacred-books-of-the-east-satapatha-2` | The Satapatha Brahmana | The Satapatha-Brahmana, part II | Julius Eggeling | 1885 | have-raw | IA `in.ernet.dli.2015.175348` |
| `sacred-books-of-the-east-satapatha-3` | The Satapatha Brahmana | The Satapatha-Brahmana, part III | Julius Eggeling | 1894 | have-raw | IA `in.ernet.dli.2015.264301` |
| `sacred-books-of-the-east-satapatha-4` | The Satapatha Brahmana | The Satapatha-Brahmana, part IV | Julius Eggeling | 1897 | have-raw | IA `sacredbooksofthe014167mbp` |
| `sacred-books-of-the-east-satapatha-5` | The Satapatha Brahmana | The Satapatha-Brahmana, part V | Julius Eggeling | 1900 | have-raw | IA `in.ernet.dli.2015.265` |
| `sacred-books-of-the-east-vedic-hymns-1` | The Rigveda (hymns to the Maruts and others) | Vedic Hymns, part I | F. Max Müller | 1891 | have-raw | IA `in.ernet.dli.2015.188666` |
| `sacred-books-of-the-east-vedic-hymns-2` | The Rigveda (hymns to Agni) | Vedic Hymns, part II | Hermann Oldenberg | 1897 | have-raw | IA `in.ernet.dli.2015.169473` |
| `sacred-books-of-the-east-atharva-veda` | The Atharvaveda (selections, with extracts from the ritual books and commentaries) | Hymns of the Atharva-Veda | Maurice Bloomfield | 1897 | have-raw | IA `in.ernet.dli.2015.152526` |
| `sacred-books-of-the-east-vedanta-sutras-1` | Badarayana, with Sankara's commentary | The Vedanta-Sutras, part I | George Thibaut | 1890 | have-raw | IA `in.ernet.dli.2015.169472` |
| `sacred-books-of-the-east-vedanta-sutras-2` | Badarayana, with Sankara's commentary | The Vedanta-Sutras, part II | George Thibaut | 1896 | have-raw | IA `in.ernet.dli.2015.88889` |
| `sacred-books-of-the-east-vedanta-sutras-3` | Badarayana, with Ramanuja's commentary | The Vedanta-Sutras, part III | George Thibaut | 1904 | have-raw | IA `vedntasutrastr03bdar` |
| — | — | motilal-reprints: Motilal Banarsidass reprints (Delhi, 1960s on) of the same volumes, e.g. in.ernet.dli.2015.224726 (vol. 11), 224728 (vol. 13) and 226564 (vol. 49), 273506 (vol. 37), 224722 (vol. 7), 224729 (vol. 14), 92889 (vol. 12), 45311 (vol. 48), whose front matter says 'First published by the Oxford University Press ... Reprinted by Motilal Banarsidass': post-1930 printings, refused in favour of the Clarendon originals. | — | — | excluded | — |
| — | — | held-elsewhere: Vols 1 and 15 (Müller's Upanishads) and vol. 10's Dhammapada are on muller; vols 6 and 9 (Palmer's Qur'an) on palmer; Legge's vols 3, 16, 27, 28, 39 and 40 are on legge (round 64). | — | — | excluded | — |

## Series shelf: the Pali canon in English before 1931: the Cambridge Jataka (Chalmers, Rouse, Francis, Neil, Cowell), Rhys Davids's Dialogues of the Buddha, Chalmers's Further Dialogues, Mrs Rhys Davids's Psalms of the Early Buddhists, Geiger and Bode's Mahavamsa, Burlingame's Buddhist Legends, Warren's Buddhism in Translations

Shelf: `pipeline/pali-buddhist-translations_shelf.json` · fetch `python3 pipeline/fetch_shelf.py pali-buddhist-translations` · titles `python3 pipeline/split_shelf_titles.py pali-buddhist-translations`.
Round 65 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `pali-buddhist-translations-jataka-1` | The Jataka (Pali birth stories) | The Jataka, vol. I | Robert Chalmers | 1895 | have-raw | IA `jatakaorstorieso01cowe` |
| `pali-buddhist-translations-jataka-2` | The Jataka (Pali birth stories) | The Jataka, vol. II | W. H. D. Rouse | 1895 | have-raw | IA `jatakaorstorieso02cowe` |
| `pali-buddhist-translations-jataka-3` | The Jataka (Pali birth stories) | The Jataka, vol. III | H. T. Francis and R. A. Neil | 1897 | have-raw | IA `jatakaorstorieso03cowe` |
| `pali-buddhist-translations-jataka-4` | The Jataka (Pali birth stories) | The Jataka, vol. IV | W. H. D. Rouse | 1901 | have-raw | IA `dli.ernet.18111` |
| `pali-buddhist-translations-jataka-5` | The Jataka (Pali birth stories) | The Jataka, vol. V | H. T. Francis | 1905 | have-raw | IA `jatakaorstorieso0000htfr` |
| `pali-buddhist-translations-jataka-6` | The Jataka (Pali birth stories) | The Jataka, vol. VI | E. B. Cowell and W. H. D. Rouse | 1907 | have-raw | IA `jatakaorstorieso06cowe` |
| `pali-buddhist-translations-dialogues-1` | The Digha Nikaya, suttas 1-13 | Dialogues of the Buddha, part I | T. W. Rhys Davids | 1899 | have-raw | IA `dialoguesofbuddh01davi` |
| `pali-buddhist-translations-dialogues-2` | The Digha Nikaya | Dialogues of the Buddha, part II | T. W. and C. A. F. Rhys Davids | 1910 | have-raw | IA `dialoguesofbuddh02davi` |
| `pali-buddhist-translations-dialogues-3` | The Digha Nikaya | Dialogues of the Buddha, part III | T. W. and C. A. F. Rhys Davids | 1921 | have-raw | IA `dialoguesofbuddh03davi` |
| `pali-buddhist-translations-further-dialogues-2` | The Majjhima Nikaya | Further Dialogues of the Buddha, vol. II | Lord Chalmers (Robert Chalmers) | 1927 | have-raw | IA `in.ernet.dli.2015.529132` |
| `pali-buddhist-translations-psalms-of-the-sisters` | The Therigatha | Psalms of the Early Buddhists, I: Psalms of the Sisters | C. A. F. Rhys Davids | 1909 | have-raw | IA `psalmsofearlybud01davi` |
| `pali-buddhist-translations-psalms-of-the-brethren` | The Theragatha | Psalms of the Early Buddhists, II: Psalms of the Brethren | C. A. F. Rhys Davids | 1913 | have-raw | IA `psalmsofearlybud02davi` |
| `pali-buddhist-translations-mahavamsa` | The Mahavamsa (chronicle of Ceylon) | The Mahavamsa, or the Great Chronicle of Ceylon | Wilhelm Geiger, assisted by Mabel Haynes Bode | 1912 | have-raw | IA `mahavamsagreatch00geigrich` |
| `pali-buddhist-translations-buddhist-legends-1` | The Dhammapada commentary (attributed to Buddhaghosa) | Buddhist Legends, part 1 | Eugene Watson Burlingame | 1921 | have-raw | IA `buddhistlegends01burluoft` |
| `pali-buddhist-translations-buddhist-legends-2` | The Dhammapada commentary (attributed to Buddhaghosa) | Buddhist Legends, part 2 | Eugene Watson Burlingame | 1921 | have-raw | IA `buddhistlegends02burluoft` |
| `pali-buddhist-translations-buddhist-legends-3` | The Dhammapada commentary (attributed to Buddhaghosa) | Buddhist Legends, part 3 | Eugene Watson Burlingame | 1921 | have-raw | IA `buddhistlegends03burluoft` |
| `pali-buddhist-translations-buddhism-in-translations` | The Pali Canon and its commentaries (selected passages) | Buddhism in Translations | Henry Clarke Warren | 1896 | have-raw | IA `buddhismintransl00warr` |
| `kindred-sayings` | — | The Book of the Kindred Sayings (Samyutta Nikaya; Pali Text Society, 1917-30, Mrs Rhys Davids and F. L. Woodward): the archive.org copies found are Luzac reprints of the 1950s-60s or undated, and part V is 1930. Waiting for period scans and the 1930 ruling. | — | — | pending | — |
| `further-dialogues-1` | — | Lord Chalmers's Further Dialogues of the Buddha, vol. I (Oxford, 1926): the only scan found (in.gov.ignca.9135) has the German map supplement of Filchner's Tibet expedition (Berlin, 1913) bound or scanned into it, thousands of lines of it, so it is not used. Vol. II (1927) is on the shelf. | — | — | pending | — |
| — | — | buddhist-birth-stories: Rhys Davids's Buddhist Birth Stories (1880, the first Jataka in English) is already on singles-plays-poetry-2 (PG 51880). | — | — | excluded | — |
| — | — | jataka-luzac: Luzac & Co. reissues of the Jataka (e.g. in.ernet.dli.2015.283272): later reprints for the Pali Text Society, not used. | — | — | excluded | — |

## Series shelf: the Harvard Oriental Series translations before 1931: Whitney's Atharva-Veda, Keith's Black Yajus and Rigveda Brahmanas, Macdonell's Brhad-Devata, Woods's Yoga-System of Patanjali, Lanman's Karpura-manjari, Belvalkar's Uttara-Rama-Charita

Shelf: `pipeline/harvard-oriental-series_shelf.json` · fetch `python3 pipeline/fetch_shelf.py harvard-oriental-series` · titles `python3 pipeline/split_shelf_titles.py harvard-oriental-series`.
Round 66 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `harvard-oriental-series-atharva-veda-1` | The Atharva-Veda Samhita, books I-VII | Atharva-Veda Samhita, first half | William Dwight Whitney, revised and edited by Charles Rockwell Lanman | 1905 | have-raw | IA `atharvavedasainh01whit` |
| `harvard-oriental-series-atharva-veda-2` | The Atharva-Veda Samhita, books VIII-XIX | Atharva-Veda Samhita, second half | William Dwight Whitney, revised and edited by Charles Rockwell Lanman | 1905 | have-raw | IA `atharvavedasainh02whit` |
| `harvard-oriental-series-black-yajus-1` | The Taittiriya Samhita, kandas I-III | The Veda of the Black Yajus School, part 1 | Arthur Berriedale Keith | 1914 | have-raw | IA `in.ernet.dli.2015.501797` |
| `harvard-oriental-series-black-yajus-2` | The Taittiriya Samhita, kandas IV-VII | The Veda of the Black Yajus School, part 2 | Arthur Berriedale Keith | 1914 | have-raw | IA `in.ernet.dli.2015.500424` |
| `harvard-oriental-series-rig-veda-brahmanas` | The Aitareya and Kausitaki Brahmanas | Rigveda Brahmanas | Arthur Berriedale Keith | 1920 | have-raw | IA `in.ernet.dli.2015.188962` |
| `harvard-oriental-series-brhad-devata` | The Brhad-Devata attributed to Saunaka | The Brhad-Devata, part II: translation and notes | Arthur Anthony Macdonell | 1904 | have-raw | IA `dli.ministry.10567` |
| `harvard-oriental-series-yoga-system` | The Yoga-sutras of Patanjali, with Veda-Vyasa's commentary and Vachaspati-Misra's gloss | The Yoga-System of Patanjali | James Haughton Woods | 1914 | have-raw | IA `in.ernet.dli.2015.109808` |
| `harvard-oriental-series-karpura-manjari` | Rajasekhara's Karpura-manjari (Prakrit drama) | Rajasekhara's Karpura-manjari | Charles Rockwell Lanman (translation), Sten Konow (edition) | 1901 | have-raw | IA `in.ernet.dli.2015.280338` |
| `harvard-oriental-series-uttara-rama-charita` | Bhavabhuti's Uttara-Rama-Charita | Rama's Later History, part 1: introduction and translation | Shripad Krishna Belvalkar | 1915 | have-raw | IA `in.ernet.dli.2015.281456` |
| `vikramas-adventures` | — | Edgerton's Vikrama's Adventures (HOS 26-27, 1926): the only archive.org scans (vikramasadventur01unse, 02unse) were OCR'd as Hindi, so their text layer is garbage. Waiting for a usable text. | — | — | pending | — |
| — | — | kiratarjuniya: Cappeller's Bharavi's Kiratarjuniya (HOS 15, 1912) is a translation into German, not English. | — | — | excluded | — |
| — | — | little-clay-cart: Ryder's Little Clay Cart (HOS 9) is already on the ryder shelf. | — | — | excluded | — |
| — | — | pali-volumes: Warren (HOS 3) and Burlingame (HOS 28-30) are on pali-buddhist-translations. | — | — | excluded | — |
| — | — | motilal-reprints: Motilal Banarsidass reprints of HOS volumes (in.ernet.dli.2015.263106, in.ernet.dli.2015.263108, dli.ernet.233919): 1960s-70s reprints, not used. | — | — | excluded | — |

## Shelf: Chinese, Tibetan and Japanese classics in English before 1931: Beal's Si-yu-ki and Life of Hiuen-Tsiang, Takakusu's I-tsing, Giles's Fa-hsien, Rockhill's Life of the Buddha and Udanavarga, Dawa-Samdup and Evans-Wentz's Tibetan Book of the Dead, Chamberlain's Kojiki, Aston's Nihongi

Shelf: `pipeline/east-asian-classics_shelf.json` · fetch `python3 pipeline/fetch_shelf.py east-asian-classics` · titles `python3 pipeline/split_shelf_titles.py east-asian-classics`.
Round 67 (2026-10-17), vetoable. Round 82 (2026-10-17), vetoable: two Tibetan titles added. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `east-asian-classics-si-yu-ki-1` | Xuanzang (Hiuen-Tsiang), Da Tang Xiyu ji | Si-yu-ki: Buddhist Records of the Western World, vol. I | Samuel Beal | 1884 | have-raw | IA `siyukibuddhistre01hsuoft` |
| `east-asian-classics-si-yu-ki-2` | Xuanzang (Hiuen-Tsiang), Da Tang Xiyu ji | Si-yu-ki: Buddhist Records of the Western World, vol. II | Samuel Beal | 1884 | have-raw | IA `siyukibuddhistre02hsuoft` |
| `east-asian-classics-life-of-hiuen-tsiang` | Huili, the life of Xuanzang | The Life of Hiuen-Tsiang | Samuel Beal | 1888 | have-raw | IA `lifeofhiuentsian030569mbp` |
| `east-asian-classics-i-tsing` | Yijing (I-tsing), Nanhai jigui neifa zhuan | A Record of the Buddhist Religion as Practised in India and the Malay Archipelago | J. Takakusu | 1896 | have-raw | IA `recordofbuddhist00ichi` |
| `east-asian-classics-fa-hsien-giles` | Faxian (Fa-hsien), Foguo ji | The Travels of Fa-hsien (399-414 A.D.), or Record of the Buddhistic Kingdoms | H. A. Giles | 1923 | have-raw | IA `in.ernet.dli.2015.172773` |
| `east-asian-classics-life-of-the-buddha-tibetan` | The Tibetan Kanjur and Tanjur (lives of the Buddha and early history of his order) | The Life of the Buddha and the Early History of his Order, derived from Tibetan Works | W. Woodville Rockhill | 1884 | have-raw | IA `dli.pahar.1054` |
| `east-asian-classics-kojiki` | The Kojiki (Records of Ancient Matters, 712) | Ko-ji-ki, or Records of Ancient Matters | Basil Hall Chamberlain | 1882 | have-raw | IA `transactionsasi27japagoog` |
| `east-asian-classics-nihongi-1` | The Nihon shoki (Chronicles of Japan, 720) | Nihongi: Chronicles of Japan from the Earliest Times to A.D. 697, vol. I | W. G. Aston | 1896 | have-raw | IA `nihongi1asto` |
| `east-asian-classics-nihongi-2` | The Nihon shoki (Chronicles of Japan, 720) | Nihongi: Chronicles of Japan from the Earliest Times to A.D. 697, vol. II | W. G. Aston | 1896 | have-raw | IA `nihongi2asto` |
| `east-asian-classics-udanavarga` | Dharmatrata, the Udanavarga (the Tibetan Dhammapada, from the Kanjur) | Udanavarga: a Collection of Verses from the Buddhist Canon | W. Woodville Rockhill | 1883 | have-raw | IA `udnavargacolle00bkah` |
| `east-asian-classics-tibetan-book-of-the-dead` | The Bardo Thodol (Karma Lingpa's terma) | The Tibetan Book of the Dead, or the After-Death Experiences on the Bardo Plane, according to Lama Kazi Dawa-Samdup's English Rendering | Lama Kazi Dawa-Samdup, edited by W. Y. Evans-Wentz | 1927 | have-raw | IA `tibetanbookofdea0000unse_w2j5` |
| — | — | legge-fa-hien: Legge's Record of Buddhistic Kingdoms (1886, PG 2124) is already on the legge shelf. | — | — | excluded | — |
| — | — | later-reprints: Asian Educational Services, Paragon, Munshiram Manoharlal and Orientalia Indica reprints of these titles on archive.org (e.g. lifeofhuuentsian00sham, recordofbuddhist0000faxi, dli.ernet.233945): later reprints, not used. | — | — | excluded | — |
| — | — | milarepa-1928: Evans-Wentz's Tibet's Great Yogi Milarepa (1928): the only open scan (tibetsgreatyogim0000wyev) is a 1971 reprint of the 1951 second edition. Not used. | — | — | excluded | — |
| — | — | bardo-thodol-upload: the-tibetan-book-of-the-dead_202401 is a private upload of the same 1927 book; the Internet Archive's own scan was used. | — | — | excluded | — |

## Shelf: Persian, Tamil and Sanskrit classics in English before 1931: the Warners' complete verse Shahnama of Firdausi (9 vols), G. U. Pope's Kural, Naladiyar and Tiruvacagam, H. H. Wilson's Vishnu Purana

Shelf: `pipeline/oriental-classics_shelf.json` · fetch `python3 pipeline/fetch_shelf.py oriental-classics` · titles `python3 pipeline/split_shelf_titles.py oriental-classics`.
Round 68 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `oriental-classics-shahnama-1` | Firdausi, the Shahnama | The Shahnama of Firdausi, vol. I | Arthur George Warner and Edmond Warner | 1905 | have-raw | IA `shahnama01firduoft` |
| `oriental-classics-shahnama-2` | Firdausi, the Shahnama | The Shahnama of Firdausi, vol. II | Arthur George Warner and Edmond Warner | 1906 | have-raw | IA `shahnama02firduoft` |
| `oriental-classics-shahnama-3` | Firdausi, the Shahnama | The Shahnama of Firdausi, vol. III | Arthur George Warner and Edmond Warner | 1908 | have-raw | IA `shahnama03firduoft` |
| `oriental-classics-shahnama-4` | Firdausi, the Shahnama | The Shahnama of Firdausi, vol. IV | Arthur George Warner and Edmond Warner | 1909 | have-raw | IA `shahnama04firduoft` |
| `oriental-classics-shahnama-5` | Firdausi, the Shahnama | The Shahnama of Firdausi, vol. V | Arthur George Warner and Edmond Warner | 1910 | have-raw | IA `shahnama05firduoft` |
| `oriental-classics-shahnama-6` | Firdausi, the Shahnama | The Shahnama of Firdausi, vol. VI | Arthur George Warner and Edmond Warner | 1912 | have-raw | IA `shahnama06firduoft` |
| `oriental-classics-shahnama-7` | Firdausi, the Shahnama | The Shahnama of Firdausi, vol. VII | Arthur George Warner and Edmond Warner | 1915 | have-raw | IA `shahnama07firduoft` |
| `oriental-classics-shahnama-8` | Firdausi, the Shahnama | The Shahnama of Firdausi, vol. VIII | Arthur George Warner and Edmond Warner | 1923 | have-raw | IA `shahnama08firduoft` |
| `oriental-classics-shahnama-9` | Firdausi, the Shahnama | The Shahnama of Firdausi, vol. IX | Arthur George Warner and Edmond Warner | 1925 | have-raw | IA `shahnama09firduoft` |
| `oriental-classics-sacred-kurral` | Tiruvalluvar, the Tirukkural | The 'Sacred' Kurral of Tiruvalluva-Nayanar | G. U. Pope | 1886 | have-raw | IA `tiruvalluvanayan00tiruuoft` |
| `oriental-classics-naladiyar` | The Naladiyar (Jain Tamil quatrains) | The Naladiyar, or Four Hundred Quatrains in Tamil | G. U. Pope | 1893 | have-raw | IA `munivararuliccey00poperich` |
| `oriental-classics-tiruvacagam` | Manikkavacakar, the Tiruvacagam | The Tiruvacagam, or 'Sacred Utterances' of the Tamil Poet, Saint and Sage Manikka-vacagar | G. U. Pope | 1900 | have-raw | IA `tiruvaagamorsa00manirich` |
| `oriental-classics-vishnu-purana` | The Vishnu Purana | The Vishnu Purana: a System of Hindu Mythology and Tradition | H. H. Wilson | 1840 | have-raw | IA `in.ernet.dli.2015.283854` |
| — | — | later-reprints: Asian Educational Services and South India Saiva Siddhanta reprints of Pope's Kural and Naladiyar (sacredkurralofti00revg, naladiyarorfourh00gupo, the 1958 Naladiyar): later reprints, not used. | — | — | excluded | — |
| — | — | wilson-hall-edition: Fitzedward Hall's enlarged edition of Wilson's Vishnu Purana (Trübner, 1864-77) is not added alongside the 1840 original, to avoid two copies of one translation. | — | — | excluded | — |

## Shelf: the Mughal histories in English before 1931: Beveridge's Akbarnama (vols I-II), Blochmann and Jarrett's Ain-i-Akbari, Rogers and Beveridge's Tuzuk-i-Jahangiri, Annette Beveridge's Humayun-nama

Shelf: `pipeline/mughal-histories_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mughal-histories` · titles `python3 pipeline/split_shelf_titles.py mughal-histories`.
Round 69 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mughal-histories-akbarnama-1` | Abu'l-Fazl, the Akbarnama | The Akbarnama of Abu-l-Fazl, vol. I | H. Beveridge | 1907 | have-raw | IA `in.ernet.dli.2015.469729` |
| `mughal-histories-akbarnama-2` | Abu'l-Fazl, the Akbarnama | The Akbarnama of Abu-l-Fazl, vol. II | H. Beveridge | 1912 | have-raw | IA `india.history.resource.107685` |
| `mughal-histories-ain-i-akbari-1` | Abu'l-Fazl, the Ain-i-Akbari | The Ain i Akbari, vol. I | H. Blochmann | 1873 | have-raw | IA `in.ernet.dli.2015.279471` |
| `mughal-histories-ain-i-akbari-2` | Abu'l-Fazl, the Ain-i-Akbari | The Ain i Akbari, vol. II | H. S. Jarrett | 1891 | have-raw | IA `in.ernet.dli.2015.32527` |
| `mughal-histories-ain-i-akbari-3` | Abu'l-Fazl, the Ain-i-Akbari | The Ain i Akbari, vol. III | H. S. Jarrett | 1894 | have-raw | IA `in.ernet.dli.2015.32529` |
| `mughal-histories-tuzuk-i-jahangiri-1` | Jahangir, the Tuzuk-i-Jahangiri (memoirs) | The Tuzuk-i-Jahangiri, or Memoirs of Jahangir, vol. I | Alexander Rogers, edited by Henry Beveridge | 1909 | have-raw | IA `tuzukijahangirio00jahauoft` |
| `mughal-histories-tuzuk-i-jahangiri-2` | Jahangir, the Tuzuk-i-Jahangiri (memoirs) | The Tuzuk-i-Jahangiri, or Memoirs of Jahangir, vol. II | Alexander Rogers, edited by Henry Beveridge | 1914 | have-raw | IA `in.ernet.dli.2015.116012` |
| `mughal-histories-humayun-nama` | Gulbadan Begam, the Humayun-nama | The History of Humayun (Humayun-nama) | Annette S. Beveridge | 1902 | have-raw | IA `historyofhumayun00gulbrich` |
| `akbarnama-3` | — | Beveridge's Akbarnama vol. III: issued in fascicles from 1907, but the volume was completed only in 1939, so it is after the cutoff as a whole. The scans found are the 1939 volume or its 2000 reprint. | — | — | pending | — |
| — | — | akbarnama-2000-reprints: Asiatic Society reprints of March and February 2000 (in.ernet.dli.2015.189288, 189290, 189291, 55648, 55649, 55650): not used. | — | — | excluded | — |
| — | — | ain-i-akbari-1927: Phillott's 1927 second edition of Blochmann's vol. I is not added alongside the 1873 first edition. | — | — | excluded | — |

## Shelf: the historians of Muslim India in English before 1931: Elliot and Dowson's History of India as Told by its Own Historians (8 vols), Briggs's complete Ferishta (4 vols)

Shelf: `pipeline/india-historians_shelf.json` · fetch `python3 pipeline/fetch_shelf.py india-historians` · titles `python3 pipeline/split_shelf_titles.py india-historians`.
Round 70 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `india-historians-elliot-dowson-1` | The Persian and Arabic historians of Muslim India (extracts) | The History of India, as Told by its Own Historians: the Muhammadan Period, vol. I | Sir H. M. Elliot, edited and continued by John Dowson | 1867 | have-raw | IA `cu31924024066593` |
| `india-historians-elliot-dowson-2` | The Persian and Arabic historians of Muslim India (extracts) | The History of India, as Told by its Own Historians: the Muhammadan Period, vol. II | Sir H. M. Elliot, edited and continued by John Dowson | 1869 | have-raw | IA `cu31924073036729` |
| `india-historians-elliot-dowson-3` | The Persian and Arabic historians of Muslim India (extracts) | The History of India, as Told by its Own Historians: the Muhammadan Period, vol. III | Sir H. M. Elliot, edited and continued by John Dowson | 1871 | have-raw | IA `cu31924073036737` |
| `india-historians-elliot-dowson-4` | The Persian and Arabic historians of Muslim India (extracts) | The History of India, as Told by its Own Historians: the Muhammadan Period, vol. IV | Sir H. M. Elliot, edited and continued by John Dowson | 1872 | have-raw | IA `cu31924073036745` |
| `india-historians-elliot-dowson-5` | The Persian and Arabic historians of Muslim India (extracts) | The History of India, as Told by its Own Historians: the Muhammadan Period, vol. V | Sir H. M. Elliot, edited and continued by John Dowson | 1873 | have-raw | IA `cu31924073036752` |
| `india-historians-elliot-dowson-6` | The Persian and Arabic historians of Muslim India (extracts) | The History of India, as Told by its Own Historians: the Muhammadan Period, vol. VI | Sir H. M. Elliot, edited and continued by John Dowson | 1875 | have-raw | IA `india.history.resource.372` |
| `india-historians-elliot-dowson-7` | The Persian and Arabic historians of Muslim India (extracts) | The History of India, as Told by its Own Historians: the Muhammadan Period, vol. VII | Sir H. M. Elliot, edited and continued by John Dowson | 1877 | have-raw | IA `cu31924073036778` |
| `india-historians-elliot-dowson-8` | The Persian and Arabic historians of Muslim India (extracts) | The History of India, as Told by its Own Historians: the Muhammadan Period, vol. VIII | Sir H. M. Elliot, edited and continued by John Dowson | 1877 | have-raw | IA `cu31924073036786` |
| `india-historians-ferishta-1` | Muhammad Qasim Ferishta, Tarikh-i Firishta | History of the Rise of the Mahomedan Power in India till the Year A.D. 1612, vol. I | John Briggs | 1829 | have-raw | IA `india.history.resource.349` |
| `india-historians-ferishta-2` | Muhammad Qasim Ferishta, Tarikh-i Firishta | History of the Rise of the Mahomedan Power in India till the Year A.D. 1612, vol. II | John Briggs | 1829 | have-raw | IA `india.history.resource.107661` |
| `india-historians-ferishta-3` | Muhammad Qasim Ferishta, Tarikh-i Firishta | History of the Rise of the Mahomedan Power in India till the Year A.D. 1612, vol. III | John Briggs | 1829 | have-raw | IA `india.history.resource.376` |
| `india-historians-ferishta-4` | Muhammad Qasim Ferishta, Tarikh-i Firishta | History of the Rise of the Mahomedan Power in India till the Year A.D. 1612, vol. IV | John Briggs | 1829 | have-raw | IA `in.ernet.dli.2015.45583` |
| — | — | briggs-late-reprints: Reprints of Briggs's Ferishta from 1971 and 1981 (in.ernet.dli.2015.499221, in.ernet.dli.2015.189198): not used. | — | — | excluded | — |

## Shelf: classical Arabic prose and poetry in English before 1931: de Slane's Ibn Khallikan (4 vols), Sprenger's Mas'udi, Hitti's Usamah and Baladhuri (with Murgotten), Chenery and Steingass's Assemblies of al-Hariri, Sir William Jones's Moallakat, Ockley's Hai Ebn Yokdhan, Lyall's Mufaddaliyat

Shelf: `pipeline/arabic-classics_shelf.json` · fetch `python3 pipeline/fetch_shelf.py arabic-classics` · titles `python3 pipeline/split_shelf_titles.py arabic-classics`.
Round 71 (2026-10-17), vetoable. Round 85 (2026-10-17), vetoable: three titles added. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `arabic-classics-ibn-khallikan-1` | Ibn Khallikan, Wafayat al-a'yan | Ibn Khallikan's Biographical Dictionary, vol. I | Baron Mac Guckin de Slane | 1843 | have-raw | IA `india.history.resource.41158` |
| `arabic-classics-ibn-khallikan-2` | Ibn Khallikan, Wafayat al-a'yan | Ibn Khallikan's Biographical Dictionary, vol. II | Baron Mac Guckin de Slane | 1843 | have-raw | IA `india.history.resource.40984` |
| `arabic-classics-ibn-khallikan-3` | Ibn Khallikan, Wafayat al-a'yan | Ibn Khallikan's Biographical Dictionary, vol. III | Baron Mac Guckin de Slane | 1868 | have-raw | IA `india.history.resource.53346` |
| `arabic-classics-ibn-khallikan-4` | Ibn Khallikan, Wafayat al-a'yan | Ibn Khallikan's Biographical Dictionary, vol. IV | Baron Mac Guckin de Slane | 1871 | have-raw | IA `india.history.resource.53344` |
| `arabic-classics-masudi-meadows-of-gold` | Al-Mas'udi, Muruj al-dhahab | El-Mas'udi's Historical Encyclopaedia, entitled 'Meadows of Gold and Mines of Gems', vol. I | Aloys Sprenger | 1841 | have-raw | IA `historicalencycl00masrich` |
| `arabic-classics-usamah` | Usamah ibn Munqidh, Kitab al-I'tibar (memoirs) | An Arab-Syrian Gentleman and Warrior in the Period of the Crusades | Philip K. Hitti | 1929 | have-raw | IA `arabsyriangentle00usma` |
| `arabic-classics-baladhuri-1` | Al-Baladhuri, Kitab futuh al-buldan | The Origins of the Islamic State, part I | Philip Khuri Hitti | 1916 | have-raw | IA `originsofislamic01bald` |
| `arabic-classics-baladhuri-2` | Al-Baladhuri, Kitab futuh al-buldan | The Origins of the Islamic State, part II | Francis Clark Murgotten | 1924 | have-raw | IA `originsofislamic02bald` |
| `arabic-classics-hariri-1` | Al-Hariri, the Maqamat | The Assemblies of al-Hariri, vol. I (assemblies 1-26) | Thomas Chenery | 1867 | have-raw | IA `in.ernet.dli.2015.282995` |
| `arabic-classics-hariri-2` | Al-Hariri, the Maqamat | The Assemblies of al-Hariri, vol. II (assemblies 27-50) | F. Steingass | 1898 | have-raw | IA `in.ernet.dli.2015.282996` |
| `arabic-classics-mufaddaliyat-2` | al-Mufaddal al-Dabbi's anthology of pre-Islamic odes | The Mufaddaliyat: an Anthology of Ancient Arabian Odes, vol. II: Translation and Notes | Charles James Lyall | 1918 | have-raw | IA `mufaddaliyatanth00mufauoft` |
| `arabic-classics-moallakat-jones` | The Mu'allaqat (the seven suspended odes) | The Moallakat, or Seven Arabian Poems, which were suspended on the Temple at Mecca | William Jones | 1782 | have-raw | IA `bim_eighteenth-century_the-moallakt-or-seven-_1782` |
| `arabic-classics-hai-ebn-yokdhan` | Ibn Tufail | The Improvement of Human Reason, exhibited in the Life of Hai Ebn Yokdhan | Simon Ockley | 1708 | have | PG 16831 |
| `arc-lyall-translations` | — | Lyall's Translations of Ancient Arabian Poetry (1885): the only open scan (in.ernet.dli.2015.50391) is the 1930 reprint, which waits on the 1930 ruling. | — | — | pending | — |
| — | — | beirut-reprints: Librairie du Liban (1970) and Khayats (1964-66) reprints of Ibn Khallikan, Usamah and Baladhuri (ibnkhallikansbio0001ibnk-0004ibnk, memoirsofarabsyr0000tran, originsofislamic0000bald): not used. | — | — | excluded | — |
| — | — | arc-lyall-diwans-1913: Lyall's Diwans of Abid ibn al-Abras and Amir ibn at-Tufail (Gibb Memorial, 1913; diwansofabidibna21abiduoft): the OCR is almost all Arabic and Lyall's name was not found in it, so the English could not be checked. | — | — | excluded | — |

## Translator shelf: E. A. Wallis Budge's Egyptian, Ethiopic and Syriac translations before 1931: the Book of the Dead, the Egyptian Heaven and Hell, the Liturgy of Funerary Offerings, Amen-em-apt, the Kebra Nagast, the Alexander romances, Bar Hebraeus's Laughable Stories, the Monks of Kublai Khan, the Book of Medicines

Shelf: `pipeline/budge_shelf.json` · fetch `python3 pipeline/fetch_shelf.py budge` · titles `python3 pipeline/split_shelf_titles.py budge`.
Round 72 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `budge-book-of-the-dead` | The Egyptian Book of the Dead (Theban recension) | The Book of the Dead: an English Translation of the Chapters, Hymns, etc., of the Theban Recension | E. A. Wallis Budge | 1898 | have-raw | IA `dli.ministry.10397` |
| `budge-egyptian-heaven-and-hell-1` | The Book Am-Tuat (Egyptian funerary book) | The Egyptian Heaven and Hell, vol. I: the Book Am-Tuat | E. A. Wallis Budge | 1905 | have-raw | IA `india.history.resource.92915` |
| `budge-egyptian-heaven-and-hell-2` | The short form of the Book Am-Tuat and the Book of Gates | The Egyptian Heaven and Hell, vol. II: the Short Form of the Book Am-Tuat and the Book of Gates | E. A. Wallis Budge | 1905 | have-raw | IA `india.history.resource.92916` |
| `budge-liturgy-of-funerary-offerings` | The Egyptian Liturgy of Funerary Offerings | The Liturgy of Funerary Offerings: the Egyptian Texts with English Translations | E. A. Wallis Budge | 1909 | have-raw | IA `liturgyoffunerar00budg` |
| `budge-teaching-of-amen-em-apt` | The Instruction of Amenemope | The Teaching of Amen-em-apt, Son of Kanekht | E. A. Wallis Budge | 1924 | have-raw | IA `teachingofamenem0000eawa` |
| `budge-queen-of-sheba` | The Kebra Nagast (Ethiopian national epic) | The Queen of Sheba and her only Son Menyelek (the Kebra Nagast) | E. A. Wallis Budge | 1922 | have-raw | IA `queenofshebahero00budgrich` |
| `budge-alexander-ethiopic` | The Ethiopic histories of Alexander (Pseudo-Callisthenes and others) | The Life and Exploits of Alexander the Great, being a Series of Translations of the Ethiopic Histories of Alexander | E. A. Wallis Budge | 1896 | have-raw | IA `cu31924091208573` |
| `budge-alexander-syriac` | The Syriac Pseudo-Callisthenes | The History of Alexander the Great, being the Syriac Version of the Pseudo-Callisthenes | E. A. Wallis Budge | 1889 | have-raw | IA `BudgeSyriacAlexander` |
| `budge-laughable-stories` | Bar Hebraeus, the Laughable Stories | The Laughable Stories collected by Mar Gregory John Bar-Hebraeus | E. A. Wallis Budge | 1897 | have-raw | IA `laughablestories00barhrich` |
| `budge-monks-of-kublai-khan` | The history of Rabban Sawma and Mar Yahballaha III (Syriac) | The Monks of Kublai Khan, Emperor of China | E. A. Wallis Budge | 1928 | have-raw | IA `monksofkublaikha0000unse` |
| `budge-book-of-medicines` | The Syriac Book of Medicines | Syrian Anatomy, Pathology and Therapeutics, or 'The Book of Medicines', vol. II: English translation | E. A. Wallis Budge | 1913 | have-raw | IA `syriananatomypat02budgiala` |
| `amulets-and-superstitions` | — | Amulets and Superstitions (Oxford, 1930): waits on the 1930 ruling. | — | — | pending | — |
| — | — | christian-texts: Budge's Christian translations are left for lane A: The Contendings of the Apostles (1899-1901), The Paradise or Garden of the Holy Fathers (1907), Saint Michael the Archangel (1894), the Life of Takla Haymanot (1906), the Book of the Saints of the Ethiopian Church (1928) and the Book of the Cave of Treasures (1927). | — | — | excluded | — |
| — | — | book-of-the-dead-reissues: The 1901 three-volume Books on Egypt and Chaldaea reissue of the Book of the Dead translation and the 1913 Papyrus of Ani are not added alongside the 1898 translation. | — | — | excluded | — |
| — | — | book-of-the-dead-other-volumes: The Egyptian text and vocabulary volumes of the 1898 Book of the Dead (e.g. bookdeadanengli00budggoog, the vocabulary) are not shelved. | — | — | excluded | — |
| — | — | book-of-medicines-1: Vol. I of the Book of Medicines (1913) is the Syriac text. | — | — | excluded | — |

## Shelf: Babylonian, Assyrian and Sumerian texts in English before 1931: the Epic of Gilgamesh (Thompson, Jastrow and Clay, Langdon, the British Museum), Langdon's Sumerian epics, liturgies and Epic of Creation, Thompson's Devils and Evil Spirits, Harper's Code of Hammurabi and Assyrian and Babylonian Literature

Shelf: `pipeline/babylonian-assyrian_shelf.json` · fetch `python3 pipeline/fetch_shelf.py babylonian-assyrian` · titles `python3 pipeline/split_shelf_titles.py babylonian-assyrian`.
Round 73 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `babylonian-assyrian-gilgamish-thompson` | The Epic of Gilgamesh (Standard Babylonian version) | The Epic of Gilgamish: a New Translation ... rendered literally into English Hexameters | R. Campbell Thompson | 1928 | have-raw | IA `thompson-1928-gilgamesh` |
| `babylonian-assyrian-gilgamesh-old-babylonian` | The Old Babylonian Gilgamesh (the Yale tablet) | An Old Babylonian Version of the Gilgamesh Epic | Morris Jastrow and Albert T. Clay | 1920 | have-raw | IA `anoldbabylonianv00jastuoft` |
| `babylonian-assyrian-gilgamish-langdon` | The Old Babylonian Gilgamesh (the Pennsylvania tablet) | The Epic of Gilgamish | Stephen Langdon | 1917 | have-raw | IA `epicofgilgamish00unse` |
| `babylonian-assyrian-deluge-and-gilgamish` | The Babylonian flood story and the Epic of Gilgamesh (summary and extracts) | The Babylonian Story of the Deluge and the Epic of Gilgamish | E. A. Wallis Budge (British Museum) | 1920 | have-raw | IA `babylonianstoryo00brituoft` |
| `babylonian-assyrian-sumerian-epic-of-paradise` | The Sumerian Eridu and flood texts | Sumerian Epic of Paradise, the Flood and the Fall of Man | Stephen Langdon | 1915 | have-raw | IA `sumerianepicofpa00lang_0` |
| `babylonian-assyrian-sumerian-liturgies` | Sumerian liturgies and psalms | Sumerian Liturgies and Psalms | Stephen Langdon | 1919 | have-raw | IA `in.ernet.dli.2015.166777` |
| `babylonian-assyrian-epic-of-creation` | The Enuma Elish | The Babylonian Epic of Creation | Stephen Langdon | 1923 | have-raw | IA `in.gov.ignca.33817` |
| `babylonian-assyrian-devils-and-evil-spirits-1` | Babylonian and Assyrian incantations against demons | The Devils and Evil Spirits of Babylonia, vol. I | R. Campbell Thompson | 1903 | have-raw | IA `devilsevilspirit01thomuoft` |
| `babylonian-assyrian-devils-and-evil-spirits-2` | Babylonian and Assyrian incantations against demons | The Devils and Evil Spirits of Babylonia, vol. II | R. Campbell Thompson | 1904 | have-raw | IA `devilsevilspirit02thomuoft` |
| `babylonian-assyrian-code-of-hammurabi-harper` | The Code of Hammurabi | The Code of Hammurabi, King of Babylon, about 2250 B.C. | Robert Francis Harper | 1904 | have-raw | IA `codeofhammurabik00harpuoft` |
| `babylonian-assyrian-assyrian-and-babylonian-literature` | Assyrian and Babylonian inscriptions, epics, laws and letters (anthology) | Assyrian and Babylonian Literature: Selected Translations | various translators, with a critical introduction by Robert Francis Harper | 1901 | have-raw | IA `assyrianbabylon00harp` |
| `thompson-gilgamish-1930` | — | Thompson's Oxford edition of the Gilgamesh text (1930): waits on the 1930 ruling, and is mostly cuneiform. | — | — | pending | — |
| — | — | held-on-reading-lists: King's Seven Tablets of Creation (1902) and Johns's Code of Hammurabi (1903) are on the reading-lists branch. | — | — | excluded | — |
| — | — | late-reprints: The AMS Press 1976 reprint of the Devils and Evil Spirits and the 2002-07 reprints of Harper's Hammurabi: not used. | — | — | excluded | — |

## Shelf: ancient Egyptian texts in English before 1931: Breasted's Ancient Records of Egypt (5 vols), Petrie's Egyptian Tales (2 series), Griffith's High Priests of Memphis, Maspero's Popular Stories (Mrs. Johns), Erman's Literature of the Ancient Egyptians (Blackman)

Shelf: `pipeline/egyptian-texts_shelf.json` · fetch `python3 pipeline/fetch_shelf.py egyptian-texts` · titles `python3 pipeline/split_shelf_titles.py egyptian-texts`.
Round 74 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `egyptian-texts-ancient-records-1` | Egyptian historical inscriptions and documents | Ancient Records of Egypt, vol. I: The First to the Seventeenth Dynasties | James Henry Breasted | 1906 | have-raw | IA `ancientrecordsof01brea` |
| `egyptian-texts-ancient-records-2` | Egyptian historical inscriptions and documents | Ancient Records of Egypt, vol. II: The Eighteenth Dynasty | James Henry Breasted | 1906 | have-raw | IA `ancientrecordsof02brea` |
| `egyptian-texts-ancient-records-3` | Egyptian historical inscriptions and documents | Ancient Records of Egypt, vol. III: The Nineteenth Dynasty | James Henry Breasted | 1906 | have-raw | IA `ancientrecordsof03brea` |
| `egyptian-texts-ancient-records-4` | Egyptian historical inscriptions and documents | Ancient Records of Egypt, vol. IV: The Twentieth to the Twenty-Sixth Dynasties | James Henry Breasted | 1906 | have-raw | IA `in.ernet.dli.2015.231361` |
| `egyptian-texts-ancient-records-5` | Egyptian historical inscriptions and documents | Ancient Records of Egypt, vol. V: Indices | James Henry Breasted | 1907 | have-raw | IA `ancientrecordsof05brea` |
| `egyptian-texts-egyptian-tales-1` | Egyptian tales from the papyri, 4th to 12th dynasty | Egyptian Tales, Translated from the Papyri: First Series | W. M. Flinders Petrie | 1895 | have | PG 7386 |
| `egyptian-texts-egyptian-tales-2` | Egyptian tales from the papyri, 18th to 19th dynasty | Egyptian Tales, Translated from the Papyri: Second Series | W. M. Flinders Petrie | 1895 | have | PG 7413 |
| `egyptian-texts-high-priests-of-memphis` | The demotic Setne Khamwas tales | Stories of the High Priests of Memphis: the Sethon of Herodotus and the Demotic Tales of Khamuas | F. Ll. Griffith | 1900 | have-raw | IA `storiesofhighpri00grifuoft` |
| `egyptian-texts-popular-stories` | Ancient Egyptian popular tales (from Maspero's Contes populaires, 4th ed.) | Popular Stories of Ancient Egypt | Mrs. C. H. W. Johns, from the French of Gaston Maspero | 1915 | have-raw | IA `cu31924091207393` |
| `egyptian-texts-literature-of-the-ancient-egyptians` | Egyptian poems, narratives and instructions (from Erman's Die Literatur der Aegypter, 1923) | The Literature of the Ancient Egyptians | Aylward M. Blackman, from the German of Adolf Erman | 1927 | have-raw | IA `literatureofanci0000unse_q0r2` |
| — | — | breasted-vol-4-wrong-scan: ancientrecordsof04brea is mislabelled: its text is Caroline Pichler's Sämmtliche Werke, so vol. IV comes from the Digital Library of India. | — | — | excluded | — |
| — | — | egyptian-literature-1901: The Colonial Press anthology Egyptian Literature (1901) reprints other translators' work and is not added. | — | — | excluded | — |
| — | — | late-reprints: Blom (1971) reprints of Petrie and the Zeller (1985) reprint of Griffith: not used. | — | — | excluded | — |

## Shelf: classical Japanese literature in English before 1931: Dickins's Primitive & Mediaeval Japanese Texts, Chamberlain's Classical Poetry of the Japanese, Pierson's Manyosu book I, Porter's Hundred Verses and Kenko, Sansom's Tsuredzure Gusa

Shelf: `pipeline/japanese-classics_shelf.json` · fetch `python3 pipeline/fetch_shelf.py japanese-classics` · titles `python3 pipeline/split_shelf_titles.py japanese-classics`.
Round 76 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `japanese-classics-primitive-and-mediaeval-texts` | Selections from the Manyoshu, the Taketori monogatari and other early Japanese texts | Primitive & Mediaeval Japanese Texts, translated into English | F. Victor Dickins | 1906 | have-raw | IA `primitivemediaev00dickuoft` |
| `japanese-classics-classical-poetry` | Classical Japanese poems and lyric dramas | The Classical Poetry of the Japanese | Basil Hall Chamberlain | 1880 | have-raw | IA `classicalpoetryo00chamuoft` |
| `japanese-classics-manyosu-book-1` | The Manyoshu, book I | The Manyôśû, Book I | J. L. Pierson | 1929 | have-raw | IA `manyosubooki0000unse` |
| `japanese-classics-hundred-verses` | The Hyakunin isshu, compiled by Fujiwara no Sadaie | A Hundred Verses from Old Japan, being a Translation of the Hyaku-nin-isshiu | William N. Porter | 1909 | have-raw | IA `hundredversesfro00fujiuoft` |
| `japanese-classics-miscellany-of-a-japanese-priest` | Yoshida Kenko, the Tsurezuregusa | The Miscellany of a Japanese Priest, being a Translation of Tsure-zure Gusa | William N. Porter | 1914 | have-raw | IA `miscellanyofjapa00yosh` |
| `japanese-classics-tsuredzure-gusa` | Yoshida Kenko, the Tsurezuregusa | The Tsuredzure Gusa of Yoshida no Kaneyoshi | G. B. Sansom | 1911 | have-raw | IA `in.ernet.dli.2015.69047` |
| `ten-foot-square-hut` | — | A. L. Sadler's The Ten Foot Square Hut and Tales of the Heike (Sydney, 1928): only the Tuttle reprint of 1972 is on archive.org. Waiting for a period scan. | — | — | pending | — |
| — | — | held-elsewhere: The Diaries of Court Ladies of Old Japan (PG 47151) is on singles-plays-poetry-2; Waley's Tale of Genji and Pillow-Book are on the waley shelf; Mitford's Tales of Old Japan on mitford; the Chushingura on singles-plays-poetry-2. | — | — | excluded | — |
| — | — | dickins-romanised-texts: The romanised-text volume of Dickins's Primitive & Mediaeval Japanese Texts (primitivemediaev00dickiala) is not a translation. | — | — | excluded | — |

## Shelf: the Fables of Bidpai in English before 1931: Keith-Falconer's Syriac Kalilah and Dimnah, North's Morall Philosophie of Doni (1570), Eastwick's and Wollaston's Anvar-i Suhaili

Shelf: `pipeline/bidpai_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bidpai` · titles `python3 pipeline/split_shelf_titles.py bidpai`.
Round 77 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bidpai-kalilah-and-dimnah-syriac` | The Old Syriac Kalilah and Dimnah (the Bidpai fables) | Kalilah and Dimnah, or the Fables of Bidpai, being an Account of their Literary History, with an English Translation of the later Syriac Version | I. G. N. Keith-Falconer | 1885 | have-raw | IA `kalilahdimnahorf00bdpkuoft` |
| `bidpai-morall-philosophie-of-doni` | Doni's Italian Bidpai (La moral filosophia, 1552) | The Earliest English Version of the Fables of Bidpai: The Morall Philosophie of Doni | Sir Thomas North, edited by Joseph Jacobs | 1570 | have-raw | IA `earliestenglishv00doniuoft` |
| `bidpai-anvar-i-suhaili-eastwick` | Husain Vaiz Kashifi, the Anvar-i Suhaili (Persian Bidpai) | The Anvar-i Suhaili, or the Lights of Canopus | Edward B. Eastwick | 1854 | have-raw | IA `india.history.resource.70987` |
| `bidpai-anwar-i-suhaili-wollaston` | Husain Vaiz Kashifi, the Anvar-i Suhaili (Persian Bidpai) | The Anwar-i-Suhaili, or Lights of Canopus, commonly known as Kalilah and Damnah | Arthur N. Wollaston | 1877 | have-raw | IA `anwarisuhailiorl00woll` |
| — | — | wright-syriac-text: William Wright's Book of Kalilah and Dimnah (Clarendon, 1884) is the Syriac text, not a translation. | — | — | excluded | — |
| — | — | children's-retellings: Maude Barrows Dutton's The Tortoise and the Geese (1908) and similar retellings for children are not translations. | — | — | excluded | — |

## Shelf: Persian poetry and Sufi prose in English before 1931: Wilberforce Clarke's Hafiz, Bustan, Sikandar Nama and Awarif, Atkinson's Laili and Majnun, C. E. Wilson's Haft Paikar and Masnavi Book II, Le Gallienne's free Hafiz

Shelf: `pipeline/persian-poets_shelf.json` · fetch `python3 pipeline/fetch_shelf.py persian-poets` · titles `python3 pipeline/split_shelf_titles.py persian-poets`.
Round 80 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `persian-poets-sikandar-nama` | Nizami Ganjavi | The Sikandar Nama, e Bara, or Book of Alexander the Great | H. Wilberforce Clarke | 1881 | have-raw | IA `sikandarnmaebara00nimg` |
| `persian-poets-hafiz-divan-1` | Hafiz | The Divan, written in the fourteenth century by Khwaja Shamsu-d-Din Muhammad-i-Hafiz-i-Shirazi, vol. I | H. Wilberforce Clarke | 1891 | have-raw | IA `thedivan01hafiuoft` |
| `persian-poets-hafiz-divan-2` | Hafiz | The Divan of Hafiz, vol. II | H. Wilberforce Clarke | 1891 | have-raw | IA `thedivan02hafiuoft` |
| `persian-poets-bustan-clarke` | Sa'di | The Bustan | H. Wilberforce Clarke | 1879 | have-raw | IA `bstnbyshaikh00sadiuoft` |
| `persian-poets-awarif-ul-maarif` | Shihab al-Din Umar al-Suhrawardi | The 'Awarifu-l-Ma'arif | H. Wilberforce Clarke | 1891 | have-raw | IA `awarifulmaarif00suhr` |
| `persian-poets-laili-and-majnun` | Nizami Ganjavi | Laili and Majnun: a Poem from the Original Persian of Nazami | James Atkinson | 1836 | have-raw | IA `lailandmajnnapo00atkigoog` |
| `persian-poets-haft-paikar` | Nizami Ganjavi | The Haft Paikar (The Seven Beauties), vol. I: translation | C. E. Wilson | 1924 | have-raw | IA `in.ernet.dli.2015.81011` |
| `persian-poets-masnavi-book-2` | Rumi | The Masnavi, Book II, vol. I: translation | C. E. Wilson | 1910 | have-raw | IA `in.ernet.dli.2015.93748` |
| `persian-poets-hafiz-odes-le-gallienne` | Hafiz | Odes from the Divan of Hafiz, freely rendered from literal translations | Richard Le Gallienne | 1905 | have-raw | IA `odesfromdivanofh00hafiuoft` |
| — | — | laili-1968-reprint: lailimajnunpoem0000jame is a 1968 reprint of Atkinson's Laili and Majnun; the 1836 Valpy scan is used. | — | — | excluded | — |
| — | — | awarif-1979: bwb_S0-AVT-190 is a 1979 Lahore printing of Clarke's Awarif; the 1891 Calcutta scan is used. | — | — | excluded | — |
| — | — | haft-paikar-commentary: Vol. II of Wilson's Haft Paikar (1924) is his commentary, not the translation. | — | — | excluded | — |
| — | — | masnavi-commentary: Vol. II of Wilson's Masnavi Book II (1910) is his commentary, not the translation. | — | — | excluded | — |

## Shelf: Sanskrit and Hindi classics in English before 1931: Wilson's Theatre of the Hindus and Megha Duta, Boyd's Nagananda, Tawney's Bhartrihari, Growse's Ramayana of Tulsi Das, Arthur Avalon's Tantra of the Great Liberation and Serpent Power

Shelf: `pipeline/indian-literature_shelf.json` · fetch `python3 pipeline/fetch_shelf.py indian-literature` · titles `python3 pipeline/split_shelf_titles.py indian-literature`.
Round 83 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `indian-literature-theatre-of-the-hindus-1` | Sanskrit drama (Sudraka's Mricchakatika, Kalidasa's Vikramorvasi, Bhavabhuti's Uttara Rama Charitra) | Select Specimens of the Theatre of the Hindus, vol. I | Horace Hayman Wilson | 1835 | have-raw | IA `selectspecimenso01wils_0` |
| `indian-literature-theatre-of-the-hindus-2` | Sanskrit drama (Bhavabhuti's Malati and Madhava, Visakhadatta's Mudra Rakshasa, Harsha's Ratnavali, and accounts of other plays) | Select Specimens of the Theatre of the Hindus, vol. II | Horace Hayman Wilson | 1835 | have-raw | IA `selectspecimenso02wils_0` |
| `indian-literature-megha-duta` | Kalidasa | The Megha Duta, or Cloud Messenger, translated into English verse | Horace Hayman Wilson | 1813 | have-raw | IA `mghadta00kali` |
| `indian-literature-nagananda` | Harsha | Nagananda, or the Joy of the Snake-World: a Buddhist Drama in Five Acts | Palmer Boyd | 1872 | have-raw | IA `bub_gb_2JfomcFOiEIC` |
| `indian-literature-bhartrihari` | Bhartrihari | Two Centuries of Bhartrihari, translated into English verse | C. H. Tawney | 1877 | have-raw | IA `twocenturiesofbh00bhar` |
| `indian-literature-tulsi-das-ramayana` | Tulsidas | The Ramayana of Tulsi Das (the Ramcharitmanas) | F. S. Growse | 1883 | have-raw | IA `in.ernet.dli.2015.43864` |
| `indian-literature-great-liberation` | The Mahanirvana Tantra | Tantra of the Great Liberation (Mahanirvana Tantra) | Arthur Avalon (Sir John Woodroffe) | 1913 | have-raw | IA `india.history.resource.110781` |
| `indian-literature-serpent-power` | Purnananda's Sat-Cakra-Nirupana and the Paduka-Pancaka | The Serpent Power, being the Shat-Chakra-Nirupana and Paduka-Panchaka | Arthur Avalon (Sir John Woodroffe) | 1924 | have-raw | IA `in.ernet.dli.2015.283748` |
| — | — | theatre-1955: theatreofhindus00wils is a 1955 reprint of Wilson's Theatre of the Hindus; the 1835 second edition is used. | — | — | excluded | — |
| — | — | tulsi-das-later-editions: Growse's Tulsi Das in later editions (1891, 1914, 1922) and a 1966 reprint were passed over for the 1883 edition. | — | — | excluded | — |

## E. J. W. Gibb (Ottoman Poems; A History of Ottoman Poetry, vols I-V)

Shelf: `pipeline/gibb_shelf.json` · fetch `python3 pipeline/fetch_shelf.py gibb` · titles `python3 pipeline/split_shelf_titles.py gibb`.
Round 84 (2026-10-17), vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `gibb-ottoman-poems` | Ottoman Turkish poets | Ottoman Poems, translated into English verse in the original forms | E. J. W. Gibb | 1882 | have-raw | IA `ottomanpoemstran00gibb` |
| `gibb-history-1` | Ottoman Turkish poets | A History of Ottoman Poetry, vol. I | E. J. W. Gibb | 1900 | have-raw | IA `historyofottoman01gibbuoft` |
| `gibb-history-2` | Ottoman Turkish poets | A History of Ottoman Poetry, vol. II | E. J. W. Gibb (edited by Edward G. Browne) | 1902 | have-raw | IA `historyofottoman02gibb` |
| `gibb-history-3` | Ottoman Turkish poets | A History of Ottoman Poetry, vol. III | E. J. W. Gibb (edited by Edward G. Browne) | 1904 | have-raw | IA `historyofottoman03gibbuoft` |
| `gibb-history-4` | Ottoman Turkish poets | A History of Ottoman Poetry, vol. IV | E. J. W. Gibb (edited by Edward G. Browne) | 1905 | have-raw | IA `historyofottoman04gibbuoft` |
| `gibb-history-5` | Ottoman Turkish poets | A History of Ottoman Poetry, vol. V | E. J. W. Gibb (edited by Edward G. Browne) | 1907 | have-raw | IA `historyofottoman05gibbuoft` |
| — | — | gibb-history-6: Vol. VI of A History of Ottoman Poetry (1909, historyofottoman06gibbuoft) contains the Turkish originals, not translations. | — | — | excluded | — |
| — | — | gibb-ottoman-literature-1901: Ottoman Literature: the Poets and Poetry of Turkey (M. Walter Dunne, 1901) was not taken: not checked against the Colonial Press Turkish Literature of the same year (Gutenberg 56464, on hammer-purgstall). | — | — | excluded | — |

## Arthur Ransome as translator (Gourmont; Old Peter's Russian Tales)

Shelf: `pipeline/ransome-translations_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ransome-translations` · titles `python3 pipeline/split_shelf_titles.py ransome-translations`.
2026-10-10, vetoable. His Swallows and Amazons is on Lane B's `ransome_shelf.json`, not here. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ransome-old-peters-russian-tales` | Russian folk tales, retold | Old Peter's Russian Tales | Arthur Ransome | 1916 | have | PG 16981 |
| `ransome-gourmont-night-in-the-luxembourg` | Remy de Gourmont | A Night in the Luxembourg | Arthur Ransome | 1912 | have | PG 46766 |
| — | — | ransome-own-books: Swallows and Amazons and the rest of the series: Ransome's own books, on Lane B's ransome_shelf.json. | — | — | excluded | — |
