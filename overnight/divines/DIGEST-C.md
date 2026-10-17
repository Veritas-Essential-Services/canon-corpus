# Lane C — Translator shelves: digest (read first)
Totals 2026-10-17T16:47-05:00: 403 shelves, 2579 titles. By round: 1-3: 108; 4: 13; 5: 27; 6: 11; 7: 12; 8: 8; Ransome translations: 2; 9 (Scott Moncrieff): 9; 10 (Ryder 5, Gertrude Bell 1, Levy Nietzsche 15): 21; 11 (Archer's Ibsen): 11; 12 (Magnússon-Morris 3, Strindberg 14): 17; 13 (Saga Library 6, Three Northern Love Stories 1, Björkman 1, Pickthall 1): 9; 14 (Wormeley 41, Vizetelly 16): 57; 15 (Wiener's Tolstoy): 24; 16 (Leland's Heine 8, Whishaw 3): 11; 17 (Koteliansky 10, Marian Fell 3, Seltzer 5, Dole 6): 24; 18 (Ellen Marriage 18, Clara Bell 43, Waring 4): 65; 19 (Teixeira de Mattos 59, Serrano 6, Howitt 2, Duff Gordon 2): 69; 20 (Miall 10, Muir 4, Wraxall 23, Dowson 3): 40; 21 (Machen 1, Ives 18, Hogarth 10, Bernstein 9, Marx Aveling 5, Bain 12): 55; 22 (Safford 23, Wister 14, Allinson 9, Worster 8, Chater 7, De Leon 18): 79; 23 (Upton 35, Colbron 5, Goldberg 9, Roscoe 8, Durand 7, Brooks 6, Lady Wallace 8, Frewer 6, Ensor 6, Ranous 2): 92; 24 (Paul 10, Saunders 8, McCabe 9, Farquharson Sharp 7, Morison 8, White 1, Black 1, Waller 7, Rothwell 5): 56; 25 (thirteen shelves): 71; 26 (pending items and Chekhov): 5; 27 (eleven shelves): 57; 28 (twelve shelves): 41; 29 (seventeen shelves): 51; 30 (seventeen shelves): 56; 31 (twenty-five shelves): 48; 32 (thirty shelves): 66; 33 (thirty-six shelves): 72; 34 (six shelves): 32; 35 (gap audit: four new shelves 46, plus 24 on seven older shelves): 70; 36 (audit +8, six new shelves 11): 19; 37 (gap-fill +6, twenty-seven shelves 97): 103; 38 (gap-fill +1, twenty-one shelves 46): 47; 39 (fifty-two shelves): 99; 40 (three shelves): 93; 41 (three shelves): 124; 42 (two shelves): 96; 43 (two shelves): 106; 44 (one shelves): 68; 45 (one shelves): 72; 46 (two shelves): 119; 47 (one shelves): 51; 48 (one shelves): 99; 49 (one shelves): 84; 50 (Garnett gap-fill +1): 1; 51 (period scans for HTML-only titles, +9 on three older shelves): 9. **15 of the titles are cross-references to works the repo already holds (the Volsunga Saga became one on 2026-10-10), not new copies.** No uids minted.
**RESUMED 2026-10-17T16:40-05:00 in burn mode (Adam, relayed 2026-10-17 21:33Z): every Garnett translation first, then the resume plan.** Paused 2026-10-10 after round 49. Plato/Aristotle are Lane B's, Aquinas a new thread's, Lang/Lamb Lane D's: skipped here. Resume plan: (1) re-check the ~149 unshelved single-translator ids; (2) look for period Internet Archive scans of the HTML-only items in _pending (Principia, Menabrea/Lovelace, Van Gogh, six physics books); (3) apply Adam's rulings on the 1930 override, facsimiles and late reprints once given.
Updated 2026-10-02T15:32-05:00. No uids minted anywhere in this lane: every title below awaits your single-writer minting pass. Nothing is converted to unit-id JSON yet (that needs entries in fetch_sources.py, which the relay may not touch).

## Dryden — `pipeline/dryden_shelf.json`
- **21 titles held** (19 clean, 2 raw OCR) from 10 sources: Scott's Works vols 11-17 via Gutenberg + PG 228 + two Internet Archive scans.
- Virgil: aeneid, aeneid-dedication, georgics, eclogues · Ovid: metamorphoses (Garth composite), ovid-metamorphoses (Dryden's own share), ovid-epistles, ovid-art-of-love, ovid-amores · theocritus, lucretius, horace, iliad, juvenal, persius · fables-chaucer, fables-boccaccio, veni-creator · xavier (Bouhours), art-of-painting (Du Fresnoy), history-of-the-league (Maimbourg, raw).
- Pending (wishlist): 1700 Fables first edition (to restore Dryden's order), 1693 Juvenal whole book, 1697 Virgil, 1717 Garth, 1688 Xavier.
- Excluded: "Dryden's Plutarch" (he translated none of the Lives), Polybius/Lucian prefaces, a different John Dryden, duplicates.

## Garnett — `pipeline/garnett_shelf.json`
- **55 titles held** from 62 sources (40 Gutenberg, 22 Internet Archive scans, OCR quality 0.92-0.97): Dostoevsky 13, Tolstoy 5, Chekhov 16, Turgenev 15, Gogol 3, Ostrovsky, Goncharov, Herzen. All first published 1894-1927 (US PD); later printings recorded per title.
- Pending: Gogol's Government Inspector (1926) and Mirgorod (1928): no verified scan found. Poor Folk / Uncle's Dream: no Garnett version found.
- **Round 50 (2026-10-17), Garnett gap-fill:** `garnett-war-and-peace-vol3` added: War and Peace vol. III (Parts XI to the Epilogue), Heinemann Library Edition, London 1904, from a Digital Library of India scan (archive.org `in.ernet.dli.2015.170286`). Raw OCR; the title page reads "Constance Garnett ... Volume III ... London ... 1904"; no post-1930 year in the front matter. Volumes I and II: no pre-1931 scan found (every other IA War and Peace checked was Dole, Wiener, Maude, the Kropotkin revision, or the 1931+ Modern Library), so they stay in _pending. Excluded `warpeace0000coun_g3a9` (Modern Library, post-1930). Knipper letters (1925): only a 1966 Blom facsimile reprint exists, so pending. Gogol plays and Mirgorod re-searched: still nothing pre-1931. The rest of Garnett (Tolstoy, Dostoevsky, Turgenev, Chekhov, Gogol, Herzen, Goncharov, Ostrovsky) was already complete; no other branch holds a Garnett shelf. **Your call:** whether a lone third volume is worth holding until I and II turn up (it stays unless you veto).

## Your decisions
1. **Dryden's Aeneid reading of record:** PG 228 keeps Dryden's elisions (th', heav'n, fix'd); Scott expands them in about 5,100 of 13,800 lines but carries the Dedication and notes. Two witnesses, one uid per passage.
2. **dryden-metamorphoses** is the Garth edition, translated by many hands (lane B points at it). Should the uid name it as Garth's book, with Dryden's own share (dryden-ovid-metamorphoses) as the Dryden title?
3. **Overlapping titles:** garnett-notes-from-underground sits inside garnett-white-nights, and dryden-aeneid-dedication sits inside Scott vol 14. The minting pass must give one uid per passage.
4. Is a converter worth writing for these cut titles (verse for Dryden, prose chapters for Garnett), as a NEW file outside structure_texts.py?

## Defects
- dryden-history-of-the-league: long-s OCR (78% of tokens in a clean vocabulary).
- Pre-1931 printings only. Garnett's War and Peace was removed (only a 1931+ scan exists); Raw Youth, Gambler, Friend of the Family, Honest Thief and Chekhov Plays 1 were swapped to earlier printings (see Review fixes).

## Shelves added after the first queue (vetoable — Adam's call)
Added 2026-10-02T15:33-05:00 at the coordinator's relay ("keep going, more translator shelves"): Cary (Dante), Longfellow (Dante and others), Florio (Montaigne), Burton (Arabian Nights), the Maudes (Tolstoy, PD editions only). **Not taken: Pope and Chapman (Homer)** — lane B's running `homer` item already shelves them translator-per-work, and the relay forbids taking another lane's titles. Plutarch skipped (another thread has it). Veto any of these and the shelf file plus its map rows can simply be deleted; nothing was minted.

### What those five shelves hold (each vetoable on its own; delete the shelf file and its map rows)
- **Cary:** Inferno, Purgatorio, Paradiso (Gutenberg), Pindar 1833 (raw OCR).
- **Longfellow:** the three canticles, plus his Translations section (Manrique, Spanish, German, Scandinavian, Beowulf passage, French, Michelangelo, Portuguese). His Virgil and Ovid pieces were left for lane B.
- **Florio:** Montaigne's Essayes 1603, using the 1906 reprint (6 volumes of raw OCR, Elizabethan spelling); the 1620 Decameron (anonymous; the Florio attribution is a scholarly one).
- **Burton:** the Arabian Nights (10 vols), Supplemental Nights (6), the Lusiads, and the Camoens Lyricks. **Your call:** Catullus, Kama Sutra and Pentamerone are public domain but explicit, so they are listed and not fetched.
- **Maude:** War and Peace, Resurrection, the Cossacks, Father Sergius, Master and Man, What Men Live By, the six Plays, What Is Art?, The Devil, Three Days in the Village. **Your call:** five of these files print no edition year, so they rest on Gutenberg's US clearance (published before 1931).

### Round 3, added by lane C itself under the same keep-going relay (each vetoable)
Cotton (Montaigne), Ormsby (Don Quixote), Urquhart and Motteux (Rabelais; Motteux's Quixote), FitzGerald (Rubaiyat, Salaman and Absal, Calderón), Bayard Taylor (Faust I and II), E. W. Lane (Thousand and One Nights), and Lady Charlotte Guest (Mabinogion). They pair with the earlier shelves: Montaigne now has Florio and Cotton, and the Nights have Burton and Lane, which makes them witnesses for comparison. **Your call:** Lane's Selections from the Kur-an is listed but not fetched.

## Review fixes — 2026-10-02T17:27-05:00 (from the review thread)
- **Already held, now cross-referenced, not copied (10 titles).** Each carries `held_in` {file, slug, gutenberg_id}, and its duplicate source was removed: dryden-aeneid → adler `virgil-eclogues` (PG 228); garnett-karamazov → adler `dostoevsky-karamazov` (28054); maude-war-and-peace → adler `tolstoy-warpeace` (2600); cotton → adler `montaigne-essays` (3600); ormsby → adler `cervantes-quixote` (996); urquhart-motteux-rabelais → adler `rabelais-gargantua` (1200); taylor-faust-part-1 → fetch_sources `faust` (14591); the three Cary canticles → fetch_sources `divine_comedy` (8800).
- **Your fix (not a lane C file):** adler_shelf.json titles PG 228 "Eclogues, Georgics, Aeneid" under slug `virgil-eclogues`. PG 228 is the Aeneid only. Dryden's Eclogues and Georgics are lane C's dryden-eclogues and dryden-georgics, from Scott. Also, adler credits Rabelais 1200 to Urquhart alone; Books IV–V are Motteux.
- **Dryden/Garth overlap:** dryden-metamorphoses (Garth 1826, many translators) contains dryden-ovid-metamorphoses (Scott 12, Dryden's own share). They are two witnesses of Dryden's lines and must get one uid per passage.
- **Translator field** on every lane C title. `_name_words` is now the translator only (no original authors, no common words), so the identity check really tests the translator.
- **Committed evidence that rights lines were read:** each shelf has a `_verified` block per source. For PG it records the header's Translator: line and the COPYRIGHTED marker (false everywhere). For IA it records whether the translator is named in the first 30 KB and the years printed in the front matter. Five IA overrides are recorded in `_identity_checked` with the evidence: Pindar's name is only in IA metadata, Florio vol. 2 has no title page (vol. 1 names him), and three cases are OCR spacing or misspelling (Lane ×2, Gogol "Garnet").
- **The front-matter year scan caught four more post-1930 printings that IA had labelled early.** Raw Youth (1956 and 1970 impressions) is now Macmillan 1923. Gambler (1957) is now Heinemann 1914, first impression. Friend of the Family (1974) is now a Heinemann scan with no imprint date (**your call:** its inside publisher's list is the 1920s one). Garnett War and Peace (Modern Library Giant, 1931+) is removed to pending. Earlier in the review: Chekhov Plays 1 was a 1935/1940 Phoenix printing (now Chatto 1925), and Honest Thief was a 1957 reset (now the earlier Heinemann). Chekhov dates fixed: Plays 2 Chatto 1923, House of the Dead Macmillan 1928.
- **Checked and a false alarm:** archive.org `christianitypatr00tols` IS Garnett. Its title page reads "translated by Constance Garnett", Cape 1922.
- **Maude UK note corrected:** UK copyright ran to the end of 2008 (Aylmer, d. 1938) and the end of 2009 (Louise, d. 1939).

## Round 4 — 2026-10-02T19:41-05:00, lane C's own choice under the coordinator's standing instruction (each shelf vetoable: delete the shelf file and its map rows)
The coordinator suggested Jowett, Church & Brodribb, Butler and Lang-Leaf-Myers. **All four are already shelved by other lanes, so none was taken**: Jowett's Thucydides and Politics (lane B, thucydides and aristotle), Church & Brodribb (lane B, tacitus), Butler's Odyssey (lane B, homer; his Iliad is in the build), and Lang-Leaf-Myers (lane D, lang). Taken instead, after grepping every shelf, fetch_sources.py and the other queues for each name:
- **Rossetti:** Vita Nuova (Gutenberg 41085) and The Early Italian Poets (1861 first edition, raw OCR). The 1861 book also contains the Vita Nuova, so there are two witnesses and it needs one uid per passage.
- **Fairfax:** Tasso's Jerusalem Delivered (Gutenberg 392).
- **W. S. Rose:** Ariosto's Orlando Furioso (Gutenberg 615). Gutenberg's cache URL for 615 returns 404, and it's the only URL fetch_shelf.py builds, so I fetched the file by hand from the ebooks URL, which is recorded in `_manual_fetch`. The surname check on "rose" is weak (the word is also a flower), so the Gutenberg header's Translator line is the real evidence.
- **Shelton:** Don Quixote, the first English translation, from Macmillan 1900 (3 vols, raw OCR). It is a third Quixote alongside Motteux and Ormsby.
- **C. E. Norton:** the Divine Comedy in prose (Houghton 1895-98 printing of 1891-92, one title per canticle, matching Cary's) and the New Life (1892).
- **John Payne:** the Decameron (Gutenberg 23700) and Villon (Villon Society 1878). **Your call:** his Thousand Nights and his Bandello are listed and not fetched, because the Nights already has Burton and Lane.
- **Carlyle as translator:** Wilhelm Meister's Apprenticeship and Travels (Gutenberg 36483 + 78139), and the German tales of Musaeus, Tieck and Richter (Gutenberg 38779).
- All of them passed the new surname check and the rights check (`_checks` recorded) and the front-matter year scan (`_verified`); no post-1930 year turned up. OCR quality on the scans is 0.93-0.96.

## Round 5 — 2026-10-02T19:47-05:00, lane C's own choice (each shelf vetoable: delete the shelf file and its map rows)
Each name was grepped across every shelf, fetch_sources.py and all four queues first, and none of them was held anywhere.
- **Curtin:** Sienkiewicz's Quo Vadis, the Trilogy (With Fire and Sword, The Deluge, Pan Michael) and On the Field of Glory (6 Gutenberg files).
- **Hapgood:** Hugo's Les Misérables (Gutenberg 135), Gorky's Orlóff, Bunin's The Village, and four Turgenev volumes. Her Turgenev is a second witness beside Garnett's.
- **Legge:** the Tao Te Ching, the Analects, and Faxian. The rest of his Sacred Books of the East is pending.
- **Giles:** H. A. Giles's Zhuangzi and Strange Stories from a Chinese Studio; Lionel Giles's Art of War and Sayings of Confucius. **Your call:** Lionel Giles died in 1958, so his work is US PD (published before 1931) but stays in UK copyright until the end of 2028.
- **Waley:** only work published before 1931: 170 Chinese Poems, More Translations, Li Po, the Nō Plays, Genji parts 1-3, and the Pillow-Book. **Your call:** this is US PD only, because the UK term runs to the end of 2036. Drop the shelf if Armarium may ever serve outside the US.
- **Hoole:** Tasso's Jerusalem Delivered (1803, 2 vols, raw OCR). Defect: the long s is still in use, so the OCR reads s as f (82% vocabulary). Vol. 2's title page names him, but the OCR splits the name; that is recorded in `_identity_checked`.
- **Harington:** Orlando Furioso, 1591 first edition. Defect: Elizabethan spelling plus scan errors leave 66% of tokens in a modern vocabulary. **Your call:** keep it as a raw witness, or veto it until a transcription exists (EEBO-TCP may have one).
- Every Gutenberg header names the expected translator; none is marked copyrighted (`_checks`). The archive.org rights gate raised no flags. Hoole's Ariosto is pending (only long-s printings or incomplete sets were found).

## Round 6 — 2026-10-02T19:53-05:00, lane C's own choice: scriptures and classics of the East (each shelf vetoable)
I grepped each name across every shelf, fetch_sources.py and the four queues first. Lane D's dutt shelf holds Romesh Dutt's condensed epics; Griffith's Ramayana is a different translation, so it is a second witness, not a duplicate.
- **Max Müller:** the Upanishads (SBE 1 and 15, raw OCR) and the Dhammapada (Gutenberg 2017).
- **Edwin Arnold:** the Bhagavad Gita, as "The Song Celestial" (Gutenberg 2388).
- **Griffith:** the Ramayana (Gutenberg 24869) and the Hymns of the Rigveda (2nd ed. 1896-97, Digital Library of India scans, raw OCR 0.88-0.90).
- **Three Korans, three witnesses:** Rodwell (1861, Gutenberg 2800, suras in his chronological order, so ids must carry the sura number), Sale (1734, Gutenberg 7440), and Palmer (SBE 1880, raw OCR).
- **Whinfield:** Rumi's Masnavi, abridged (1887).
- **Nicholson:** Hujwiri's Kashf al-Mahjub (Gutenberg 64786) and Selected Poems from the Divani Shamsi Tabriz (1898). The Divani is raw OCR at 0.79 because the Persian text faces the English. Its OCR spells the name "Nichqlson", so that file is in `_identity_checked`.
- The surname checks for "sale" and "arnold" are weak (a common word, and another Arnold), so the Gutenberg header's Translator line is the evidence for those two (`_checks`).
- **Your call:** scripture of living religions. These are 19th-century scholarly translations, all PD. Veto any you would rather not host.

## Second review round — 2026-10-02T19:56-05:00 (the roving reviewer)
- **Bare surnames tightened.** "rose" matches "the sun rose", so the identity check passed on almost any text. Eleven shelves now require the full name: Rose, Sale, Edwin Arnold, Bayard Taylor, Charles Cotton, Charlotte Guest, E. W. Lane, John Payne, the Gileses, Eliot Norton and Richard Burton. Every source still passes.
- **Shelton vol. 2** passed only because of a publisher's ad at the back; its title page is OCR'd as "Thomas Sbelton". That title page was read by eye, and the reading is recorded in the shelf.
- **Found while checking: Palmer's Qur'an had part II twice and no part I.** Both IA copies held chapters XVII-CXIV. Part I (SBE 6, Michigan copy) now replaces the duplicate, and its title page reads "translated by E. H. Palmer, part I, chapters I to XVI".

## Round 7 — 2026-10-03T00:51-05:00, Romantic-era translators (each shelf vetoable)
The new coordinator listed Chapman, Pope, Cowper, Butcher and Lang, Jowett's Thucydides, Rawlinson's Herodotus, North's Plutarch, Florio and Urquhart. **All of them are already shelved:** the first seven by lanes B and D (homer, lang, thucydides, herodotus, plutarch), and Florio and Urquhart by lane C. Nothing was duplicated. Lane C's own picks instead:
- **Southey:** the Chronicle of the Cid, and Amadis of Gaul (vols 2-4 from Gutenberg, vol. 1 from the Toronto 1803 scan). The vol. 1 copy has lost the half-title that names him; the Toronto catalogue records it, and that is noted in `_identity_checked`.
- **Coleridge:** Schiller's The Piccolomini and The Death of Wallenstein (Gutenberg 6786-6787, placed by hand because the cache URL returns 404).
- **The Bowrings:** Sir John Bowring's Peter Schlemihl, and his son E. A. Bowring's Goethe Poems and Heine Poems (two translators, one per title).
- **Anster and Hayward:** Faust Part I in verse (1835) and in prose (1833), new witnesses beside Bayard Taylor's. **Caught by the gate:** IA's "Anster" item (fausttransanster00goetuoft) is actually John Stuart Blackie's Faust (Macmillan 1880), so it was excluded and replaced with Routledge's Anster.
- **Wicksteed:** Dante's Paradiso (Temple Classics; the OCR mixes in the Italian, 0.71) and the Convivio (1903).
- **Mangan:** German Anthology (Dublin 1845, 2 vols). Vol. II has no title leaf, which is recorded.
- **Lane A's common-word surname guard (e1ef08b):** Palmer now uses "e. h. palmer". Part II's OCR mangles the name, which is recorded with the IA catalogue evidence. All 43 lane C shelves pass.

## Round 8 — 2026-10-03T05:42-05:00 (each shelf vetoable)
The coordinator re-sent the Chapman/Pope/Cowper/Butcher-Lang/Jowett/Rawlinson/North/Florio/Urquhart list. All of it is already shelved (see round 7), and I told the coordinator so. My own picks, after grepping all shelves and queues (Howitt's Andersen is lane D's; Blackie's Aeschylus is lane B's):
- **Symonds:** Cellini's Autobiography, the Sonnets of Michelangelo and Campanella, and Wine, Women, and Song (goliard songs). All from Gutenberg.
- **Blackie:** Faust Part I (Gutenberg 63203). His Aeschylus is a cross-reference to lane B's aeschylus shelf, not a copy.
- **Theodore Martin:** Schiller's Wilhelm Tell (Gutenberg 6788). His Faust, Vita Nuova, Catullus and Heine are pending.
- **Hearn:** Gautier's One of Cleopatra's Nights, and Flaubert's Temptation of St. Anthony (1910, US PD).
- All Gutenberg headers name the translator; none is marked copyrighted. `--verify --record` is clean.

## Name audit fix (2026-10-03, from Lane D's audit)

Lane D found that `maude` and a bare `hearn` would also pass other authors' texts (Maude Ashurst Biggs, for one). Eleven shelves now gate on the full printed name only: maude (Aylmer/Louise Maude), hearn (Lafcadio Hearn), southey, symonds, blackie, rossetti, coleridge, garnett, griffith, nicholson, muller. Each was tested against every source on its shelf; the only three misses (southey-amadis-1, garnett-gogol-dikanka, nicholson-divani-1898) already carry `_identity_checked` overrides. All eleven re-verified and re-recorded: 0 mismatched, 0 rights flags. **Your call:** none.

## Ransome as translator (2026-10-10)

Your Swallows and Amazons request reached two lanes at once; Lane B shelved it first (`pipeline/ransome_shelf.json`, its questions are in DIGEST-B), so lane C dropped its own copy before pushing. Lane C's shelf `ransome-translations` holds only what is a translation or retelling: Gourmont's *A Night in the Luxembourg* (1912, PG 46766, translator line reads Arthur Ransome) and *Old Peter's Russian Tales* (1916, PG 16981). Verified and recorded: 0 mismatched, 0 rights flags. No uids minted. **Your call:** none beyond the usual veto.

Two notes on Lane B's shelf, passed to it through the coordinator: its `_surname` is a bare `ransome` (Lane D's audit asks for the full printed name), and Standard Ebooks' proofed CC0 edition (2026-01-01) is a cleaner text than the 1946 OCR if you want a reading copy.

## Round 9: C. K. Scott Moncrieff (2026-10-10)

New shelf `scott-moncrieff`, 9 titles. Nobody else shelves him; checked across every branch. From Gutenberg: Proust's *Swann's Way* (1922), *Within a Budding Grove* (1924) and *The Guermantes Way* (1925), *The Song of Roland* (1919), and Stendhal's *Charterhouse of Parma* (1925, two volumes joined). From archive.org, raw OCR, each title page read: *Widsith, Beowulf* (1921), and *The Abbess of Castro* (1926), *Armance* (1928) and *The Letters of Abelard and Heloise* (Knopf, 1926). Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** Gutenberg's *Guermantes Way* was made from a Modern Library printing of 1932 or later. The text is the 1925 translation. Keep it, or move it to `_pending`?

Pending, because every open scan is a later printing: *Cities of the Plain*, *The Captive*, *The Sweet Cheat Gone*, *The Red and the Black* (only volume one of the 1926 printing is open), and Pirandello's *Shoot!*. *The Old and the Young* has only volume two open.


## Round 10: Ryder, Gertrude Bell, the Levy Nietzsche (2026-10-10)

Three new shelves, 21 titles; none was on any other lane's shelf.

- **`ryder`** (5 titles): Arthur W. Ryder's Sanskrit. *Shakuntala and Other Works* (Kalidasa, 1912), *The Little Clay Cart* (1905) and *Twenty-Two Goblins* (1917) come from Gutenberg. *The Panchatantra* (Chicago, 1925) and *The Bhagavad-gita* (1929) are raw OCR. In the Panchatantra scan the printed year is garbled, so it rests on the catalogue's 1925 date. Pending: *Dandin's Ten Princes*, whose only open scan is from 1960.
- **`gertrude-bell`** (1 title): *Poems from the Divan of Hafiz* (1897).
- **`levy-nietzsche`** (15 titles): the first complete English Nietzsche, Oscar Levy's edition of 1909 to 1913, all from Gutenberg. It was a team of translators, so each title checks for its own translator's name rather than a shelf-wide one. Mencken's *Antichrist* and Harvey's *Human, All Too Human* are other translators and are excluded.

Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** none beyond the veto. One note: Ludovici lived until 1971, so the UK status of the Levy volumes varies by translator. In the US they are all public domain.

## Round 11: William Archer's Ibsen (2026-10-10)

New shelf `archer-ibsen`: the Heinemann/Scribner Collected Works of Henrik Ibsen (1906-1912), which was the standard English Ibsen. It is shelved one title per volume, vols 1 to 11, with the plays in each listed. Eight volumes come from Gutenberg's clean texts of that edition. Vols 6, 9 and 10 are archive.org OCR with their title pages read: 1906, 1907, and a 1913 impression of 1907. Vol 12 (*From Ibsen's Workshop*) is pending because archive.org returned errors all day. Gutenberg's single plays from the same edition are excluded so nothing is held twice. Sharp's *A Doll's House* stays on Adler's shelf, since it is a different translation. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** none beyond the veto. One note on the UK: Gosse died in 1928 and Herford in 1931, so the volumes they co-translated (*Hedda*, *Master Builder*, *Love's Comedy*, *Brand*) have been UK public domain only since 2002. The US is unaffected.

## Round 12: Magnússon and Morris; Strindberg in English (2026-10-10)

- **`morris-magnusson`** (3 titles, all from Gutenberg): *The Volsunga Saga* (1870), *Grettir the Strong* (1869) and *Frithiof the Bold* (1875). Morris's Homer, Virgil and Beowulf stay on their author shelves. Pending for next round: the six-volume Saga Library (1891-1905) and *Three Northern Love Stories*, both from archive.org. The Volsunga file opens with a modern e-text editor's bibliography, which must be stripped before the text is published.
- **`strindberg-english`** (14 titles, all from Gutenberg): four Björkman volumes (Scribner, 1913-16), two volumes by Edith and Warner Oland (1912), five by Claud Field (1912-15) and three by Ellie Schleussner (1912-13). Each title checks for its own translator's name. Excluded: Graham Rawson's *Road to Damascus* (a 1939 translation; Gutenberg has it, but it is too late for this lane), two Gutenberg single plays already inside Björkman's second series, and two books with no translator named.

Verified and recorded: 0 mismatched, 0 rights flags. No uids minted. **Your call:** none beyond the veto.

## Round 13: pending items cleared, and Pickthall's Quran (2026-10-10)

- **`morris-magnusson`** gains 7 titles: the six-volume Saga Library (Quaritch, 1891-1905), which includes their Heimskringla, and *Three Northern Love Stories* (1875). These are raw OCR with every title page read. Archive.org labels one copy "vol. 1" when it is actually vol. III, so the right copy is used and the note is recorded. Laing's Heimskringla stays on the Sturluson shelf as a separate translation.
- **`strindberg-english`** gains Björkman's first series (Scribner, 1912).
- **`pickthall`** (new, 1 title): Marmaduke Pickthall, *The Meaning of the Glorious Koran* (Knopf, London, 1930), the first English Quran by an English Muslim. It is US public domain since January 2026 and UK public domain since 2007. It sits beside the Sale, Rodwell and Palmer Quran shelves.

Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** Pickthall passes only through a `_rights_checked` override, the same one Swallows and Amazons needed, because fetch_shelf still treats 1930 as in copyright (Lane A's file; I flagged this to the coordinator). Unlike Swallows and Amazons, this scan is a 1930 printing, so there is no later-printing question. Still pending: Archer's Ibsen vol. 12, because archive.org keeps returning errors for that file.

## Fix: Volsunga Saga overlap (2026-10-10)

In round 12 I shelved Magnússon and Morris's *Volsunga Saga* (PG 1152), which Lane D has held on `poetic-edda_shelf.json` since October 3. I missed it in my overlap check. It is now a cross-reference (`held_in`) on `morris-magnusson`, and the duplicate source is gone. Re-verified: 0 mismatched.

## Round 14: Wormeley's Balzac and Vizetelly's Zola (2026-10-10)

From this round on, every Gutenberg and archive.org id is checked against every shelf on every branch before anything is shelved. A re-run over all of lane C's shelves found no clash other than the Volsunga one, which is now fixed.

- **`wormeley`** (41 titles, Gutenberg): Katharine Prescott Wormeley's Balzac (Roberts Brothers, Boston, 1885-1900), plus Daudet's *Tartarin on the Alps*, Sand's *The Bagpipers* and Balzac's *Letters to Madame Hanska*. Five texts had no Gutenberg cache copy, so they were fetched by hand and are noted in `_manual_fetch`. *The Celibates* is excluded because two of its three novels are already shelved singly. Waring's *Cousin Bette* stays on Adler's shelf.
- **`vizetelly`** (16 titles, Gutenberg): Ernest Alfred Vizetelly's Zola (Chatto and Windus, 1886-1906), including the Three Cities as complete single novels rather than Gutenberg's split volumes. Gutenberg names him as editor rather than translator for *The Fortune of the Rougons* and *His Masterpiece*. Those two say they revise an earlier version, so their titles say so.

The `translated` field gives the series' date range, not each book's first year. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted. **Your call:** none beyond the veto.

## Round 15: Leo Wiener's Complete Tolstoy (2026-10-10)

New shelf `wiener-tolstoy`: the first complete English Tolstoy, translated by Leo Wiener (Dana Estes, Boston, 1904-05). It is shelved as one title per volume, all 24 volumes, raw OCR with each title page read ("Translated from the Original Russian and Edited by Leo Wiener"). For two volumes the first copy was unusable: one lacked its title page and one would not download. Florida's copies are used for those and the swaps are noted. It is a second witness beside the Maudes', Garnett's and Hapgood's Tolstoy; ids were checked across all branches and nothing is held twice. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted. **Your call:** none beyond the veto.

## Round 16: Leland's Heine; Whishaw's Dostoevsky (2026-10-10)

- **`leland-heine`** (8 titles): Charles Godfrey Leland's Heine, vols 1-8 of Heinemann's Works of Heinrich Heine (1891-93; two are 1906 reprints). This is the prose: Pictures of Travel, The Salon, Germany, French Affairs and the Florentine Nights volume. It is raw OCR with every title page read. Vols 9-12 (the poems) are by Brooksbank and Armour and are not shelved. Leland's folklore stays on the other lane's `leland_shelf.json`.
- **`whishaw`** (3 titles): Frederick Whishaw's Dostoevsky for Vizetelly (London, 1887-88): *The Idiot*, *The Friend of the Family and The Gambler*, and *Uncle's Dream and The Permanent Husband* (from Gutenberg). In the Friend of the Family scan the OCR reads "WH1SHAW", so the name check cannot see him; the title page was read and the override is recorded.

Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** Whishaw's *Injury and Insult* (1887) survives open only as a mid-century Micro Photo photographic facsimile of the 1887 edition. Does a photo-facsimile count as the 1887 printing? It is pending until you decide.

## Round 17: Russian into English, 1886-1923 (2026-10-10)

Four new shelves, 24 titles, all from Gutenberg, each translator line read in the text:

- **`koteliansky`** (10): S. S. Koteliansky and his Bloomsbury collaborators. With Leonard Woolf: Chekhov's *Note-Book*, Gorky's *Reminiscences* of Chekhov and of Tolstoy, Countess Tolstoy's *Autobiography* and Bunin's *Gentleman from San Francisco*, whose title story is co-credited to D. H. Lawrence. With Virginia Woolf: *Talks with Tolstoi*. With J. M. Murry: Chekhov's *The Bet*, Kuprin and Shestov. Also *All Things are Possible*, with Lawrence's foreword.
- **`marian-fell`** (3): Chekhov's *Swan Song* and *Russian Silhouettes*, and Korolenko's *Makar's Dream*. Her Scribner *Plays* volume is pending for next round.
- **`seltzer`** (5): Thomas Seltzer's Gorky (*The Spy*), Andreyev, Gogol (*The Inspector-General*), Sudermann (*The Song of Songs*, in a 1926 printing) and Ostwald.
- **`dole`** (6): Nathan Haskell Dole's Tolstoy (Crowell, 1887), Palacio Valdés, Verga and Dupuy's *Great Masters of Russian Literature*.

All of these are US public domain. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** nothing for the US. If the library is ever published in the UK, the Koteliansky volumes have been UK public domain only since 2026, and the three he did with Murry not until 2028.

## Round 18: the Dent Balzac translators, and Clara Bell (2026-10-10)

Three new shelves, 65 titles, all from Gutenberg, with the translator line read in every header:

- **`ellen-marriage`** (18): Ellen Marriage's Balzac for Dent's Comédie Humaine (ed. Saintsbury, 1895-99). Left out: the Gutenberg extracts and series titles that would duplicate whole novels.
- **`clara-bell`** (43): Clara Bell (d. 1927), the most prolific Victorian translator. 23 Balzac titles for the same Dent set, plus Georg Ebers (8 complete novels, not Gutenberg's per-volume splits), Eckstein's *Quintus Claudius* (2 volumes), Galdós (3), Hillern (2), Couperus, Huysmans, Maupassant, Palacio Valdés and Karadjordjević. *Leon Roch* and *Quintus Claudius* have no complete Gutenberg text, so each volume is its own title.
- **`waring`** (4): James Waring's Balzac (Dent). His *Cousin Betty* is already on adler_shelf.json, so it is a cross-reference here, not a second copy.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** none beyond the veto.


## Round 19: Teixeira de Mattos, and three Victorian women translators (2026-10-10)

Four new shelves, 69 titles, all from Gutenberg, with the translator read in every header or title page:

- **`teixeira-de-mattos`** (59): Alexander Teixeira de Mattos (d. 1921). Fabre's insect books (16), Maeterlinck's essays and plays (15), Couperus's novels (11, including the four-part *Small Souls* sequence), Leblanc's Arsène Lupin and others (8), Chateaubriand's *Memoirs* (6 volumes), plus Tocqueville's *Recollections*, Streuvels and Paoli. Two Fabre volumes share chapters with Bernard Miall, and two Maeterlinck essays are Sutro's; each is noted. Left out: three retellings for children and Carl Ewald, who has his own shelf on another lane.
- **`serrano`** (6): Mary J. Serrano's Galdós (*Doña Perfecta*), Pardo Bazán (3), Zola's *Doctor Pascal* and Eça de Queirós.
- **`mary-howitt`** (2): Mary Howitt's Fredrika Bremer. Her Andersen is already on andersen_shelf.json.
- **`duff-gordon`** (2): Lady Duff Gordon's *The Amber Witch* and *The French in Algiers*.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** none beyond the veto. Note for the Ewald shelf's owner: Teixeira de Mattos's *My Little Boy* (PG 35543) and *The Old Room* (PG 62883) are not on it yet.


## Round 20: Scandinavian, French frontier tales, the first Les Misérables (2026-10-10)

Four new shelves, 40 titles, all from Gutenberg, with the translator line read in every header:

- **`bernard-miall`** (10): Bernard Miall's translations printed before 1931: Nexø's *Pelle the Conqueror* (the complete text; vols 1 and 4 are Jessie Muir's), Rolland's *Tolstoy*, Maeterlinck's *Poems*, Fabre's *Social Life in the Insect World* and two Fabre biographies, Brieux's three plays (one each by Miall, J. B. Fagan and Charlotte Shaw), and three history books.
- **`jessie-muir`** (4): Jessie Muir's Jonas Lie (2), Bojer's *The Power of a Lie* and Fleuron's *Grim* (with J. Alexander, 1921).
- **`wraxall`** (23): Sir Lascelles Wraxall's 18 Gustave Aimard frontier novels and the first English *Les Misérables* (1862, 5 volumes). That is a second witness beside Hapgood's translation, not a duplicate.
- **`dowson`** (3): Ernest Dowson's *Les liaisons dangereuses* (2 volumes) and Balzac's *A Passion in the Desert*.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** none beyond the veto. Aimard's frontier novels are period adventure fiction with the racial attitudes of the 1860s; they are shelved as period documents, the way the rest of the lane is. Veto them if that is not what the Armarium wants.


## Round 21: Casanova, George Sand, and the Russians again (2026-10-10)

Six new shelves, 55 titles, all from Gutenberg, with the translator line read in every header. No post-1930 year appears in any front matter:

- **`machen-casanova`** (1): Arthur Machen's Casanova *Memoirs* (1894), as Gutenberg's one complete text rather than its 30 part-files.
- **`ives`** (18): George Burnham Ives (d. 1930): ten George Sand novels for Barrie (1900-02), Daudet's *The Nabob*, Mérimée's stories, Paul de Kock, Bourget, Aicard, a Balzac selection, and Bernard's life of the printer Geofroy Tory.
- **`cj-hogarth`** (10): C. J. Hogarth's Tolstoy (*Childhood*, *Boyhood*, *Youth*), Dostoevsky (*Poor Folk*, *The Gambler*), Goncharov's *Oblomov*, Turgenev's *Fathers and Sons*, Gorky, Andreyev and Melgunov's *Red Terror in Russia* (1926).
- **`herman-bernstein`** (9): Herman Bernstein's Andreyev (6, including *The Seven Who Were Hanged*), Gorky, Chekhov and Turgenev.
- **`eleanor-marx-aveling`** (5): Eleanor Marx Aveling's *Madame Bovary* (1886), Ibsen's *The Lady from the Sea* and *The Wild Duck*, Lissagaray's *History of the Commune* and Plekhanov.
- **`bain-jokai`** (12): R. Nisbet Bain's fiction: ten Jókai books, Jonas Lie's *Weird Tales from Northern Seas* and *Tales from Gorky*. His three folk-tale books stay on lane D's `bain_shelf.json`; this shelf uses the name form "nisbet bain" only.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** none beyond the veto. Casanova's *Memoirs* are frank about his love affairs; veto if that is not wanted on the shelf.


## Round 22: German romances, Scandinavians, Sue (2026-10-10)

Six new shelves, 79 titles, all from Gutenberg, with the translator line read in every header:

- **`safford`** (23): Mary J. Safford's Ebers (nine complete novels, *A Question*, and his autobiography), Felix Dahn (3), Mühlbach, Heyse, Hamerling's *Aspasia*, Eckstein, Hillern, Jókai, Mariager, Nordau (2) and Marie Bashkirtseff. Gutenberg's per-volume Ebers files and its mixed-translator *Complete Short Works* are left out.
- **`wister`** (14): Annis Lee Wister's German popular novels for Lippincott: Marlitt, E. Werner, Streckfuss, Ossip Schubin and others.
- **`allinson`** (9): A. R. Allinson's Anatole France (4), Brantôme's *Lives of Fair and Gallant Ladies* (2 volumes), Dumas's *The Wolf-Leader*, Lemonnier and *Fantômas*.
- **`worster`** (8): W. W. Worster's Hamsun (*Growth of the Soil*, *Pan*, *Wanderers*, *Mothwise*), Bojer's *The Great Hunger* (with Charles Archer), Gunnarsson, Buchholtz and Nilsen. His Rasmussen is on the rasmussen shelf, and his Lagerlöf (*The Outcast*, PG 71086) is left for the lagerlof shelf's owner.
- **`chater`** (7): Arthur G. Chater's Amundsen (*The South Pole*), Nansen (*In Northern Mists*, 2 volumes), Brandes's *Nietzsche*, Ellen Key, Hamsun's *Victoria* and Duun's *The Trough of the Wave*. Duun is a 1930 Knopf printing; its copyright line was read, and a 1930 book has been US public domain since January 2026.
- **`de-leon`** (18): Daniel De Leon's Eugène Sue, 17 tales of *The Mysteries of the People*, and Bebel's *Woman under Socialism*.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** none beyond the veto.


## Round 23: ten smaller translators (2026-10-10)

Ten new shelves, 92 titles, all from Gutenberg, with the translator line read in every header:

- **`upton`** (35): George P. Upton's *Life Stories for Young People* (McClurg, 1904-11), short German biographies and legends for children (Charlemagne, Columbus, Beethoven, the Nibelungs, Frithiof and others), plus Nohl's lives of Wagner, Haydn and Liszt and Max Müller's *Memories*.
- **`colbron`** (5): Grace Isabel Colbron's Auguste Groner detective stories (1910).
- **`isaac-goldberg`** (9): Isaac Goldberg's Baroja, Blasco Ibáñez, *Brazilian Tales*, Pinski, and Remy de Gourmont (two 1920s Little Blue Books).
- **`thomas-roscoe`** (8): Thomas Roscoe's Lanzi, *History of Painting in Italy* (6 volumes), Pellico's *My Ten Years' Imprisonment*, and *Tales of Humour, Gallantry and Romance*.
- **`durand`** (7): John Durand's Taine: *The Origins of Contemporary France* (6 volumes) and *The Philosophy of Art*. Gutenberg's text adds a short modern preface and notes by its volunteer annotator, which is why 1988 shows up in the front matter. The translation itself is from 1876-94.
- **`ct-brooks`** (6): Charles Timothy Brooks's Goethe *Faust*, Part I, and Jean Paul (*Titan*, *Hesperus*, *The Invisible Lodge*). His Busch stays on the wilhelm-busch shelf.
- **`lady-wallace`** (8): Lady Wallace's Mozart, Beethoven and Mendelssohn letters and Auerbach's *Joseph in the Snow* (3 volumes).
- **`frewer`** (6): Ellen Frewer's Verne (*Dick Sands*), Cahun, Schweinfurth's *The Heart of Africa* and Holub's *Seven Years in South Africa*.
- **`laura-ensor`** (6): Laura Ensor's Loti (*Madame Chrysanthème*), Daudet (2), Maupassant's *Afloat* and the *Memoirs of the Princesse de Ligne*.
- **`ranous`** (2): Dora Knowlton Ranous's D'Annunzio (*The Flame*) and *Zibeline*.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** none beyond the veto. For the wilhelm-busch shelf's owner: Brooks's *Plish and Plum* (PG 37188) is not on it yet.


## Round 24: philosophers, critics, historians (2026-10-10)

Nine new shelves, 56 titles, all from Gutenberg, with the translator line read in every header. No post-1930 year appears in any front matter:

- **`eden-cedar-paul`** (10): Eden and Cedar Paul's Zweig (2), Rolland, Schnitzler's *Casanova's Homecoming*, Emil Ludwig's *Napoleon* and *Diana*, Loria's *Karl Marx*, a French private's war diary, and two books by Eden alone.
- **`bailey-saunders`** (8): T. Bailey Saunders's seven volumes of Schopenhauer's essays and Goethe's *Maxims and Reflections*.
- **`mccabe`** (9): Joseph McCabe's Haeckel (5 titles, including *The Riddle of the Universe*), Bölsche's life of Haeckel, Voltaire's *Toleration*, Ferrer and Nordmann's *Einstein and the Universe*.
- **`farquharson-sharp`** (7): R. Farquharson Sharp's Everyman Ibsen (5) and Bjørnson (2). His *A Doll's House* is already on adler_shelf.json, so it is a cross-reference here.
- **`mary-morison`** (8): Brandes's *Main Currents in Nineteenth Century Literature* (6 volumes, with Diana White) and *William Shakespeare* (with Archer and White), and Bjørnson's *Mary*. **`diana-white`** (1): Dubois's *Timbuctoo the Mysterious*.
- **`robert-black`** (1): Guizot's *Popular History of France*, as Gutenberg's one complete text.
- **`waller`** (7): E. M. Waller's Dumas, *My Memoirs* (6 volumes), and Mérimée.
- **`rothwell`** (5): Fred Rothwell's Bergson (*Laughter*, with Brereton), Schuré, Pascal, Ohnet and Roujon.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** I left four of the Pauls' translations off, by judgment rather than rights: *A Young Girl's Diary* and three sexology books from the 1910s-20s (Moll, Bloch, Kisch). They are listed in the shelf's `_excluded`. Say if you want them in.


## Round 25: thirteen smaller translators (2026-10-10)

Thirteen new shelves, 71 titles, all from Gutenberg, with the translator line read in every header. The only post-1930 years in any front matter are Gutenberg transcribers' notes:

- **`markham`** (7): Sir Clements Markham's Hakluyt Society Spanish chronicles (Cieza de León 4, Quirós, Vespucci's letters with Columbus and Las Casas documents) and *Lazarillo de Tormes*.
- **`thomasina-ross`** (7): Humboldt's *Personal Narrative* (3 volumes), Tschudi's *Travels in Peru*, Bouterwek's *History of Spanish and Portuguese Literature* (2 volumes) and *El Buscapié*.
- **`hl-williams`** (6): Henry Llewellyn Williams's Dumas (five Marie Antoinette romances) and Aimard.
- **`beatrice-marshall`** (5): Sudermann (4) and Michaëlis. **`alys-hallard`** (4): the Goncourts, Gyp, Doumic's *George Sand*, *Brave Belgians*.
- **`bertha-ness`** (5) and **`christina-tyrrell`** (6): E. Werner and Gottschall, Bentley three-deckers of the 1870s and 80s.
- **`macdowall`** (5): Fritz Reuter's *An Old Story of My Farming Days* (3 volumes), Franzos's *The Jews of Barnow* and Wägner's *Epics and Romances of the Middle Ages*.
- **`gillies`** (5): R. P. Gillies's Hoffmann, *The Devil's Elixir* (2 volumes, 1824), and Fouqué's *The Magic Ring* (3 volumes, 1825).
- **`d-anvers`** (6): N. D'Anvers (Nancy Bell): Verne (3), Nadaillac, Plauchut and Hourst.
- **`livingston`** (4): Arthur Livingston's Blasco Ibáñez, Quiroga, Farrère and Montessori. **`barrett-clark`** (5): Rostand's *The Romancers*, Rolland and other French plays.
- **`lamond`** (6): E. M. Lamond's translation of Hartmann Grisar's *Luther* (6 volumes, 1913-17), the Jesuit historian's critical life.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** none beyond the veto. Grisar's *Luther* is a Catholic polemical biography. It is shelved as a translation, not as divinity; veto it if lane A's Reformation shelves should not sit beside it.


## Round 26: two pending items cleared, and Chekhov's first English translators (2026-10-10)

- **`archer-ibsen`** vol. 12, *From Ibsen's Workshop* (A. G. Chater, introduction by Archer). It had been pending because of archive.org errors; a Toronto copy works. It is a 1923 Scribner printing of the 1911 Copyright Edition. The Archer set is now complete, 12 of 12.
- **`marian-fell`**: her *Plays* (Scribner, 1912: *Uncle Vanya*, *Ivanoff*, *The Sea-Gull*, *The Swan Song*), from Cornell's copy with its title page. Adler's shelf already has *Uncle Vanya* from Gutenberg (PG 1756), whose text names no translator; this is the book it came from.
- New **`julius-west`** (1): Chekhov's *Plays, Second Series* (1916), including *The Three Sisters* and *The Cherry Orchard*.
- New **`george-calderon`** (2): *Two Plays by Tchekhof*, *The Seagull* and *The Cherry Orchard* (1912), and Ilya Tolstoy's *Reminiscences of Tolstoy*.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Still pending:** Ryder's *Dandin* (only a 1960 scan), Scott Moncrieff's later Proust volumes (only post-1931 printings are open), and Whishaw's *Crime and Punishment* (no open scan). Whishaw's *Injury and Insult* still waits on your facsimile ruling.


## Round 27: chronicles, philosophy, history, novels (2026-10-10)

Eleven new shelves, 57 titles, all from Gutenberg, with the translator line read in every header. No post-1930 year appears in any front matter:

- **`johnes`** (12): Thomas Johnes's *Chronicles of Enguerrand de Monstrelet* (1809), volumes 1-12 (Gutenberg lacks volume 13).
- **`elwes`** (6): R. H. M. Elwes's Spinoza: the *Theologico-Political Treatise* (4 parts) and *On the Improvement of the Understanding*. His *Ethics* is on adler_shelf.json, so it is a cross-reference here.
- **`fleming`** (11): William F. Fleming's Voltaire, the *Philosophical Dictionary* (10 volumes) and one more volume of the 1901 Works.
- **`mcclure`** (1): Maspero's *History of Egypt, Chaldæa, Syria, Babylonia and Assyria*, as Gutenberg's one complete text.
- **`ainslie`** (6): Douglas Ainslie's Croce, including both his 1909 and his revised 1922 *Aesthetic*.
- **`derbyshire`** (4): Charles Derbyshire's Rizal: *Noli Me Tangere* (as *The Social Cancer*), *El Filibusterismo* (as *The Reign of Greed*) and two essays.
- **`gilbert-cannan`** (4): Rolland's *Jean-Christophe* (3 volumes) and Chekhov (with Koteliansky). **`lewisohn`** (4): Wassermann (3) and Sudermann.
- **`van-laun`** (4): Taine's *History of English Literature* (3 volumes) and La Bruyère. **`eugene-mason`** (4): Wace, Layamon, Marie de France and *Aucassin and Nicolette* for Everyman.
- **`eleanor-grove`** (1): Ebers's *An Egyptian Princess*, the complete text.

Skipped because they are already shelved on other branches: Brill's Freud (freud_shelf.json) and Henderson, McMaster and Quesada's Maupassant (maupassant_shelf.json).

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Your call:** none beyond the veto.


## Round 28: twelve more translators (2026-10-10)

Twelve new shelves, 41 titles, all from Gutenberg, with the translator line read in every header:

- **`mary-loyd`** (4): Lady Mary Loyd's Mérimée (*Carmen*, *Colomba*), Stendhal's *The Chartreuse of Parma* and the Prince de Joinville's *Memoirs*.
- **`krehbiel`** (4): H. E. Krehbiel's edition of Thayer's *Life of Beethoven* (3 volumes, 1921) and Kerst's *Mozart*.
- **`frances-hoey`** (4): Madame de Rémusat's *Memoirs* (2 volumes) and Challamel's *History of Fashion* (both with John Lillie), and Verne's *An Antarctic Mystery*.
- **`dulcken`** (2): Ida Pfeiffer's travels. His Andersen stays on the andersen shelf.
- **`prestage`** (4): Azurara's *Chronicle of the Discovery and Conquest of Guinea* (2 volumes, with Beazley) and Eça de Queirós (2).
- **`dorothy-bussy`** (4): Dorothy Bussy's Gide: *Strait is the Gate*, *The Vatican Swindle*, *The Counterfeiters*, and *The Immoralist*. *The Immoralist* is a 1930 Knopf printing, US public domain since January 2026.
- **`dziewicki`** (4): Reymont's *The Peasants* (4 volumes, 1924-25).
- **`swanwick`** (3): Goethe's *Egmont* and *Iphigenia in Tauris*, and Schiller's *The Maid of Orleans*.
- **`oxenford`** (2): Goethe's *Autobiography* (the full Bohn text; Gutenberg's half-length copy is left out) and *Tales from the German*.
- **`monier-williams`** (2): *Sakoontala* and the *Siksha-Patri*. **`lalor`** (4): Roscher (2) and Nohl's *Mozart* and *Beethoven*. **`walter-armstrong`** (4): Perrot and Chipiez on the art of Egypt and of Chaldæa and Assyria.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Merge note (not a decision):** the reading-lists thread's `chekhov-bet_shelf.json` (on its own branch, added today) holds PG 55283, Koteliansky and Murry's *The Bet*, which is also on this lane's `koteliansky` shelf. Whichever merges second should turn its copy into a cross-reference.

## Round 29: seventeen more translators (2026-10-10)

Seventeen new shelves, 51 titles, all from Gutenberg, with the translator line read in every header:

- **`ww-waters`** (3): W. G. Waters's *Journal of Montaigne's Travels in Italy* (3 volumes). His Straparola is left out (it stays with the Straparola shelf).
- **`edna-underwood`** (4): Hafiz, Mickiewicz's *Sonnets from the Crimea*, and two story collections (foreign countries; the Balkans).
- **`ellen-frothingham`** (3): Lessing's *Laocoon*, Goethe's *Hermann and Dorothea*, Auerbach's *Edelweiss*.
- **`boylan`** (2): Goethe's *Werther* and Schiller's *Don Carlos* (Bohn). A Little Blue Book extract of his Goethe (PG 78269) is left out.
- **`holcroft`** (3): Beaumarchais's *The Follies of a Day* (*The Marriage of Figaro*, 1785) and Trenck's *Life* (2 volumes).
- **`margaret-armour`** (3): *The Fall of the Nibelungs* and Wagner's *Ring* in two volumes (Rackham's illustrations).
- **`florence-simmonds`** (3): Corroyer's *Gothic Architecture*, Duhamel's *The New Book of Martyrs*, Le Goffic's *Dixmude*.
- **`guerney`** (3): Bunin's *The Dreams of Chang* and Kuprin's *Sulamith* and *Yama* (all 1920s printings).
- **`benecke`** (3): three volumes of Polish tales (Sienkiewicz, Prus, Żeromski and others). **Flag:** Gutenberg keyed *Selected Polish Tales* from the 1944 World's Classics reprint of the 1921 selection. The text is the 1921 public-domain text reprinted, but the copy itself is not a pre-1931 printing. Veto it if you want only pre-1931 copies.
- **`lowe-porter`** (3): Mann's *Buddenbrooks* (2 volumes, 1924) and *Three Essays* (1929).
- **`aldington`** (3): Benda's *The Great Betrayal* (1928), Cyrano de Bergerac's *Voyages to the Moon and the Sun*, Sologub's *The Little Demon*.
- **`dora-schmitz`** (2): Haeckel's *History of Creation* (2 volumes). Her Schliemann stays on the schliemann shelf.
- **`welby`** (3): Flammarion's *Astronomy for Amateurs*, Ostwald's *Maxim Gorki*, Ribot's *The Evolution of General Ideas*.
- **`emilie-jackson`** (3): Mrs. Wilfrid Jackson's Anatole France: *The Gods are Athirst*, *The Opinions of Jérôme Coignard*, *The Revolt of the Angels*.
- **`metcalfe`** (3): *Fantômas* and two Verne novels.
- **`wollstonecraft`** (3): Mary Wollstonecraft as translator: Madame de Cambon's *Young Grandison* (2 volumes) and Necker's *Of the Importance of Religious Opinions*.
- **`bicknell`** (4): four of Fabre's books for young readers.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 30: seventeen more translators (2026-10-10)

Seventeen new shelves, 56 titles, all from Gutenberg, with the translator line read in every header:

- **`chapman-coleman`** (5): Mrs. Chapman Coleman's Luise Mühlbach (Appleton, 1867-69): *Frederick the Great and His Family*, *Berlin and Sans-Souci*, *Goethe and Schiller*, *Queen Hortense*, *Mohammed Ali and His House*.
- **`soissons`** (4): Sienkiewicz's *So Runs the World*, Orzeszkowa's *An Obscure Apostle*, and Kraszewski's *The Countess Cosel* and *Count Brühl*.
- **`mccormack`** (2): Mach's *Popular Scientific Lectures* and Weismann's *On Germinal Selection* (Open Court). His Lagrange and Schubert are in `_pending`: Gutenberg has them only as PDF/LaTeX, with no text file.
- **`georgina-malcolm`** (4): Freytag's *Pictures of German Life* (1862-63, 4 volumes).
- **`denis-maccarthy`** (4): Calderón's *Life Is a Dream*, *The Wonder-Working Magician*, *The Purgatory of St. Patrick*, *The Two Lovers of Heaven*.
- **`hannibal-lloyd`** (4): Prince Maximilian of Wied's *Travels in the Interior of North America* (Thwaites's Early Western Travels, 3 parts) and Iffland's *The Nephews*.
- **`cournos`** (2): Sologub's *The Created Legend* and *The Old House*. *The Little Demon* is already on `aldington`; two Esenwein anthologies he only contributed to are left out.
- **`lily-wolffsohn`** (3): Dahn's *A Struggle for Rome* (1878, 3 volumes).
- **`shea-troyer`** (3): *The Dabistán, or School of Manners* (Oriental Translation Fund, 1843, 3 volumes).
- **`pauline-townsend`** (3): Otto Jahn's *Life of Mozart* (1882, 3 volumes).
- **`thomson-weismann`** (4): Weismann's *The Evolution Theory* (2 volumes), Rudolf Otto's *Naturalism and Religion*, and Brehm's *From North Pole to Equator*.
- **`ssa-stephenson`** (3): Spielhagen's *The Breaking of the Storm* (1877, 3 volumes).
- **`robson-michaud`** (3): Michaud's *History of the Crusades* (3 volumes).
- **`painter`** (3): William Painter's *The Palace of Pleasure* (1566-67), the Elizabethan collection of novelle that Shakespeare drew on, in Jacobs's 1890 edition.
- **`campion`** (3): Schweitzer's *On the Edge of the Primeval Forest* (1922) and the two volumes of *The Philosophy of Civilization* (1923).
- **`friedlaender`** (3): Dubnow's *History of the Jews in Russia and Poland* (JPS, 1916-20, 3 volumes).
- **`aline-delano`** (3): Tolstoy's *The Kingdom of God is Within You* and *What is Art?*, Hugo's *Ninety-Three*, Korolenko's *The Blind Musician*.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Flags (same question as Benecke in round 29):** two Gutenberg copies were keyed from reprints made after 1930 of translations first printed before it. Campion's *On the Edge of the Primeval Forest* comes from a 1937 reprint of the 1922 text, and Friedlaender's Dubnow volume 2 from the JPS's 1946 reprint of the 1918 text. The words are the public-domain text, but the copies are not pre-1931 printings. Veto them if you want only pre-1931 copies.

## Round 31: twenty-five more translators (2026-10-10)

Twenty-five new shelves, 48 titles, all from Gutenberg, with the translator line read in every header:

- **`zilboorg`** (2): Zamyatin's *We* (Dutton, 1924), the book's first publication in any language, and Andreyev's *He Who Gets Slapped*.
- **`yarmolinsky`** (2): Saltykov-Shchedrin's *A Family of Noblemen* (*The Golovlyov Family*) and *The Shield*, the 1917 anthology edited by Gorky, Andreyev and Sologub.
- **`katharine-wylde`** (2): Grazia Deledda's *Ashes* and *Nostalgia*.
- **`winifred-stephens`** (2): Anatole France's *The Life of Joan of Arc* and *Clio*.
- **`selver`** (2): Karel Čapek's *R.U.R.* (the play that gave English the word "robot") and *The Insect Play*, both 1923.
- **`rigg`** (2): Rigg's *Decameron* (1903, 2 volumes), a separate translation from Payne's on the `payne` shelf.
- **`hornblow`** (2): D'Annunzio's *The Intruder* and *The Triumph of Death*.
- **`hanna-larsen`** (2): J. P. Jacobsen's *Marie Grubbe* and *Niels Lyhne*.
- **`flitch`** (2): Unamuno's *The Tragic Sense of Life* and *Essays and Soliloquies*.
- **`glazer`** (2): Molnár's *Liliom*, and *Fashions for Men* with *The Swan*.
- **`bunnett`** (2): Fouqué's *Undine* and the *Memoirs of Leonora Christina*.
- **`constance-bache`** (2) and **`hueffer`** (2): the *Letters of Franz Liszt* and the *Correspondence of Wagner and Liszt*.
- **`atkinson-lepper`** (2): De Coster's *The Legend of Ulenspiegel* (1918).
- **`cf-atkinson`** (2): Spengler's *The Decline of the West* (Knopf, 1926 and 1928).
- **`joly`** (2): the first two books of *Hung Lou Meng, or The Dream of the Red Chamber* (1892-93).
- **`byington`** (2): Stirner's *The Ego and His Own* and Eltzbacher's *Anarchism*.
- **`bealby`** (2): Hoffmann's *Weird Tales*.
- **`hazlitt-huc`** (2): Huc's *Travels in Tartary, Thibet, and China*.
- **`lockhart-diaz`** (2): *The Memoirs of the Conquistador Bernal Díaz del Castillo* (1844).
- **`crewe-jones`** (2): Malot's *Nobody's Boy* and *Nobody's Girl*.
- **`greenstreet`** (1): Dastre's *Life and Death*. His Poincaré is in `_pending` because Gutenberg has it only as PDF/LaTeX.
- **`stirling-bastiat`** (2): Bastiat's *Economic Sophisms* and *Harmonies of Political Economy*.
- **`delffs`** (2): Scheffel's *Ekkehard*.
- **`egerton`** (1): Hamsun's *Hunger*, from Knopf's 1920 printing. Gutenberg's own note says the Knopf text bowdlerises Egerton's 1899 translation. The unexpurgated 1899 edition is not on Gutenberg. A second Gutenberg copy of the same Knopf text is left out.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Flag (same question as rounds 29 and 30):** Flitch's *The Tragic Sense of Life* comes from the 1954 Dover reprint, which calls itself an unaltered republication of the 1921 Macmillan text. Veto it if you want only pre-1931 copies.

## Round 32: thirty more translators (2026-10-10)

Thirty new shelves, 66 titles, all from Gutenberg, with the translator line read in every header:

- **`elise-lathrop`** (3): three novels by Ossip Schubin.
- **`hammer-purgstall`** (2): Evliya Çelebi's *Narrative of Travels in Europe, Asia, and Africa* (Oriental Translation Fund). An anthology he only contributed to is left out.
- **`nathaniel-greene`** (3): Van der Velde's *Tales from the German* (2 volumes) and Mühlbach's *The Daughter of an Empress*.
- **`dunstan`** (3): Belot's *A Parisian Sultana* (1879). It is a racy French society novel of its day: veto it if it doesn't belong.
- **`de-quincey-walladmor`** (2): *Walladmor* (1825), the German fake Scott novel that De Quincey "freely translated" back into English. A Jean Paul miscellany with several translators is left out.
- **`jane-chapman`** (3): Ingemann's *King Eric and the Outlaws*. **`bushby`** (3): *The Danes, Sketched by Themselves*. Her Andersen is already shelved elsewhere.
- **`babington`** (2): Hecker's *The Black Death in the Fourteenth Century* (1833) and *The Epidemics of the Middle Ages* (1844). Morley's 1888 reprint of part of it is left out.
- **`meldola`** (2): Weismann's *Studies in the Theory of Descent*, with Darwin's preface. **`jp-richter`** (2): *The Notebooks of Leonardo da Vinci* (1883). For both, the combined one-file copy is left out.
- **`lord-stanley`** (3): Hakluyt Society volumes: Barbosa's coasts of East Africa and Malabar, Pigafetta's account of Magellan's voyage, and Alvares's Portuguese embassy to Abyssinia.
- **`ziegler`** (2): Wedekind's *The Awakening of Spring* and *Such is Life*. **`fitzwater-wray`** (2): Barbusse's *Under Fire* and *Light*.
- **`wenckstern`** (2): Eötvös's *The Village Notary* and Schlesinger's *Saunterings in and about London*. **`vandam`** (2): Sastrow's *Memoirs of a German Burgomaster* and the *Recollections of the Congress of Vienna*.
- **`untermann`** (2): Engels's *The Origin of the Family, Private Property and the State* (Kerr, 1902) and Dietzgen.
- **`strettell`** (2): Verhaeren's *Poems* and the *Memoirs of Mistral*. **`lionel-strachey`** (2): the *Memoirs of Madame Vigée Lebrun* and *The Gray Nun*.
- **`storer`** (2): *Il Novellino* (1925) and Pirandello's *Three Plays*. **`scheffauer`** (2): Heine's *Atta Troll* and Mann's *Bashan and I*.
- **`pinkerton`** (2): Artsybashev's *Sanine* and the *La Bohème* libretto. **`ongley`** (2): Blasco Ibáñez's *The Temptress* and Gálvez's *Nacha Regules*.
- **`jessie-lemont`** (2): Rilke's *Poems* (1918) and *Auguste Rodin*. **`hollander`** (2): *Selections from the Writings of Kierkegaard* (1923), the first Kierkegaard in English, and Einarsson's *Sword and Crozier*.
- **`gertrude-hall`** (2): Verlaine's *Poems* and Rostand's *Chantecler*. **`bithell`** (2): Zweig's *Émile Verhaeren* and Vollmöller's *Turandot*.
- **`agnetti`** (2): Fogazzaro's *The Patriot* and *Leila*. **`borthwick`** (2): Ellen Key's *The Morality of Woman* and *The Woman Movement*.
- **`kamensky`** (2): Mendeleyev's *The Principles of Chemistry* (1891). **`bucknall`** (2): Viollet-le-Duc's *Annals of a Fortress* and *How to Build a House*.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Flags (same questions as earlier rounds):** Barbosa's *Description of the Coasts of East Africa and Malabar* on `lord-stanley` comes from a 1970 photo-reprint of the 1866 Hakluyt volume (the same question as Whishaw's facsimile). Storer's Pirandello *Three Plays* comes from a printing after 1934 of the 1922 text. Veto either if you want only pre-1931 copies.

## Round 33: thirty-six more translators (2026-10-10)

Thirty-six new shelves, 72 titles, all from Gutenberg, with the translator line read in every header:

- **`laura-kendall`** (3): Verne's *Ticket No. "9672"*, Ernest Daudet's *Which?*, and Gaboriau's *A Thousand Francs Reward*.
- **`rs-townsend`** (2): Turgenev's *Virgin Soil* (Everyman) and *Tolstoi for the Young*.
- **`silvanus-thompson`** (2): Huygens's *Treatise on Light* (1912) and William Gilbert's *De Magnete* (1900).
- **`surendranath-tagore`** (2): *The Home and the World* and *My Reminiscences*. **`rabindranath-tagore`** (2): *Songs of Kabir* (with Evelyn Underhill) and *The Crescent Moon*, his own Bengali poems in his own English.
- **`arthur-symons`** (2): Baudelaire's *Poems in Prose*, and D'Annunzio's *The Child of Pleasure* (Georgina Harding's prose, Symons's verse).
- **`sumichrast`** (2): Gautier's *The Romance of a Mummy* and *My Private Menagerie*. **`burnham-maupin`** (2): Gautier's *Mademoiselle de Maupin*.
- **`rose-strunsky`** (2): *The Journal of Leo Tolstoi, 1895-1899* and Gorky's *The Confession*. **`jakowleff-montefiore`** (2): two volumes of early Gorky stories.
- **`cw-stork`** (2): *Modern Swedish Masterpieces* (1923) and Söderberg's *Martin Birck's Youth*, a 1930 first edition, US public domain since January 2026.
- **`adler-stern`** (2): Auerbach's *On the Heights* and *Waldfried*. **`schele-de-vere`** (2): Spielhagen's *Problematic Characters* and *Through Night to Light*. His Saintine is already shelved elsewhere.
- **`steegmann`** (2): Deledda's *The Woman and the Priest* and *The Mother*. **`schierbrand`** (2): Keller's *Seldwyla Folks* and Bilse's *A Little Garrison*.
- **`elizabeth-sabine`** (2): Humboldt's *Aspects of Nature*. **`ramsden`** (2): Laura Marholm's *Six Modern Women* and *We Women and Our Authors*.
- **`ts-perry`** (2): Imbert de Saint-Amand on the empresses Josephine and Marie Louise. **`oliver-colt`** (2): *The Memoirs of General Baron de Marbot* and Daudet's *Tartarin de Tarascon*.
- **`neumann`** (2): the *History of the Pirates who Infested the China Sea* and *Vahram's Chronicle of the Armenian Kingdom in Cilicia* (Oriental Translation Fund, 1831).
- **`lady-moreton`** (2): Coloma's *The Story of Don John of Austria* and *Perez the Mouse*.
- **`jepson`** (2): Leblanc's *Arsène Lupin* and Leroux's *The Man with the Black Feather*. **`hjerleid`** (2): Bjørnson's *The Fisher Girl* and *Ovind*.
- **`godman`** (2): Levasseur's *Lafayette in America in 1824 and 1825*. **`selina-gaye`** (2) and **`se-boggs`** (2): Hungarian novels by Jósika and Jókai.
- **`freese`** (2): *The Library of Photius*, vol. 1 (1920), and Niemann's *The Coming Conquest of England*. A Livy he only edited is left out.
- **`duncan-forbes`** (2): *The Adventures of Hatim Taï* and the *Bagh o Bahar*. **`cowell`** (2): the *Sarva-Darsana-Samgraha* and the *Tattva-Muktavali*.
- **`fassett`** (2): Pío Baroja's *Youth and Egolatry* and *The City of the Discreet*. **`de-kay`** (2): Rolland's *Pierre and Luce* and Daudet's *Numa Roumestan*.
- **`fanny-copeland`** (2): *Croatian Tales of Long Ago* (1924) and *The Slav Nations*. **`drezmal`** (2): Sienkiewicz's *In Desert and Wilderness* and *Whirlpools*.
- **`hf-brownson`** (2): Balmes's *Fundamental Philosophy*. **`wa-bradley`** (2): Gourmont's *Decadence* and *The Story of Flamenca*.
- **`bonney`** (1): Pierotti's *Jerusalem Explored*, the text volume. The plates volume is left out.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Flag (same question as earlier rounds):** Lady Moreton's *Perez the Mouse* comes from a 1935 reprint of the 1914 book. Veto it if you want only pre-1931 copies.

## Round 34: six more translators (2026-10-10)

Six new shelves, 32 titles, all from Gutenberg, with the translator line read in every header:

This round took the large translations that the rank of smaller translators kept passing over:

- **`whiston`** (5): William Whiston's Josephus (1737): *The Antiquities of the Jews*, *The Wars of the Jews*, *Against Apion*, the *Life*, and the *Discourse to the Greeks concerning Hades*. DIGEST-B records that Lane B left Josephus unassigned in case it belonged to lane A. No lane has shelved it since, and it is a translation, so it is here. If lane A wants it, this shelf can become a cross-reference.
- **`ganguli`** (4): Kisari Mohan Ganguli's complete prose *Mahabharata* (1883-96), all eighteen books in Gutenberg's four-volume edition. Gutenberg's five single-parva files are left out as duplicates. Lane D's `dutt` shelf names this as another translator's and leaves it alone.
- **`mn-dutt`** (6): Manmatha Nath Dutt's prose *Rāmāyana* (4 volumes), the *Harivamsha* and the *Vishnupuranam*. He is not R. C. Dutt, whose verse epics are on Lane D's `dutt` shelf.
- **`saintsbury-heptameron`** (5): Saintsbury's *Heptameron* of Marguerite of Navarre (1894). Gutenberg's linked index to it is left out.
- **`viharilala-mitra`** (7): *The Yoga-Vasishtha Maharamayana* (Calcutta, 1891-99), complete in seven parts.
- **`smollett-translations`** (5): Smollett's *Gil Blas* (3 volumes), his *Don Quixote*, and Voltaire's *History of Peter the Great*. The other Quixotes on this lane (`ormsby`, `shelton`) are separate translations.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

**Flag (the facsimile question again):** the Yoga-Vasishtha was scanned from modern Indian photo-reprints (Delhi, 1978 and 1999) of the 1890s Calcutta edition. The words are the 1890s text, but the copy is a facsimile. It is the same question as Whishaw's *Injury and Insult* and Stanley's Barbosa.

## Round 35: gap audit of older shelves, and four new translators (2026-10-10)

70 titles, all from Gutenberg, with the translator line read in every header:

**Part 1: titles missing from shelves this lane already had.** A sweep of the Gutenberg catalogue found 24 titles by translators already shelved here that had never been added or ruled out:

- **`curtin`** (+8): Sienkiewicz's *Children of the Soil*, *Hania*, *In Vain*, *Let Us Follow Him*, *Life and Death* and *Lillian Morris*, Prus's *The Pharaoh and the Priest*, and Orzeszkowa's *The Argonauts*. A second transcription of the Prus is left out.
- **`hapgood`** (+6): Hugo's *Notre-Dame de Paris*, Leskov's *The Steel Flea*, and four Tolstoy titles, including *Sevastopol*. That one was in `_pending` as "not on Gutenberg in her version" and is there now. A duplicate *What to Do?* is left out.
- **`wormeley`** (+4): Balzac's *The Chouans*, *César Birotteau*, *Pierrette* and *An Historical Mystery*.
- **`clara-bell`** (+3): Balzac's *A Man of Business*, Schubin's *Our Own Set*, and van Eeden's *Little Johannes*.
- **`levy-nietzsche`** (+2): *Thoughts Out of Season* I (Ludovici) and vol. 3, *The Future of our Educational Institutions* (Kennedy). Both were on the shelf's missing-volumes list. Five part-files and duplicate files are recorded as excluded.
- **`payne`** (+1): *Alaeddin and the Enchanted Lamp*. His *Thousand Nights* stays a pending decision for you (Gutenberg has only 4 of the 9 volumes).
- **`burton`**: the *Kama Sutra* (Burton and Bhide) is recorded as left off by judgment, like the Pauls' sexology titles.

**Part 2: four new shelves (46 titles).**

- **`rasmus-anderson`** (8): Bjørnson's *Arne*, *A Happy Boy* and *Magnhild*, Rydberg's *Teutonic Mythology* (3 volumes), Brandes's *Eminent Authors*, and Lumholtz's *Among Cannibals*. His *Younger Edda* is already on the `sturluson` shelf.
- **`archer-other`** (2): Nansen's *Eskimo Life* and Kielland's *Tales of Two Countries*.
- **`borrow-translations`** (31): *Romantic Ballads from the Danish* (1826), *The Sleeping Bard*, Klinger's *Faustus*, Oehlenschläger's *The Gold Horns*, *Welsh Poems and Ballads*, Borrow's Romani *Gospel of Luke* (*Embeo e Majaro Lucas*), and 24 ballad and tale pamphlets from his manuscripts that T. J. Wise printed in 1913-14. Wise is the bibliographer later exposed for forging "first editions". These pamphlets are genuine Borrow texts, but the editions are Wise's. Lane D's `borrow` shelf keeps the *Turkish Jester*. Ewald's *The Death of Balder* is left for Lane D's `ewald` shelf.
- **`adele-seltzer`** (5): Hauptmann's *Atlantis*, Liber's *Rashi* (credited to "Adele Szold", 1906), Sudermann's *Iolanthe's Wedding*, Magdeleine Marx's *Woman*, and *The Adventures of Maya the Bee*. Her husband Thomas Seltzer's shelf now records these five as hers.

Not added: Ludovici's van Gogh letters (Gutenberg has no text file for it).

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 36: the rest of the audit, and six team translators (2026-10-10)

19 titles, all from Gutenberg, with the translator line read in every header:

**Part 1: the rest of the audit of older shelves (+8 titles).** Zola's *Money* (`vizetelly`), Marx's *The Eighteenth Brumaire* (`de-leon`), Suttner's *When Thoughts Will Soar* (`dole`), Dostoevsky's *Stavrogin's Confession* (Koteliansky and Virginia Woolf, 1922; `koteliansky`), Scheffel's *Gaudeamus!* (`leland-heine`), *The Letters of a Portuguese Nun* (`prestage`), *The Story of Gunnlaug the Worm-Tongue* (`morris-magnusson`), and Strindberg's *The Growth of a Soul* (`strindberg-english`). Three duplicates are recorded as excluded: another *Wilhelm Tell* on `theodore-martin`, three single Gautier stories on `hearn` that are already held whole, and a Gutenberg copy of Björkman's first series that `strindberg-english` already holds from archive.org.

**Part 2: six new shelves (11 titles)**, for team translators whose other work was outside the Strindberg and Nietzsche shelves:

- **`claud-field`** (4): Gogol's *The Mantle and Other Stories*, *Peasant Tales of Russia*, *The Confessions of Al Ghazzali*, and Gunnarsson's *The Sworn Brothers*.
- **`edwin-bjorkman`** (1): Schnitzler's *The Lonely Way*, *Intermezzo* and *Countess Mizzie*. **`ellie-schleussner`** (1): Lucka's *The Evolution of Love*.
- **`helen-zimmern`** (1): Carmen Sylva's *Pilgrim Sorrow*. Her De Amicis is left for the `de-amicis` shelf.
- **`paul-cohn`** (2): Bordeaux's *The Last Days of Fort Vaux* and Beyens's *Germany before the War*.
- **`horace-samuel`** (2): Stendhal's *The Red and the Black* (1913) and Schnitzler's *The Road to the Open*.

**Left off by judgment:** Adrian Collins's translation of Gobineau's *The Inequality of Human Races* (1915), the founding text of "scientific" racism. Ask if you want it shelved as a historical document.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 37: twenty-seven more translators (2026-10-10)

Twenty-seven new shelves, 97 titles, all from Gutenberg, with the translator line read in every header:

**Part 1: gap-fill on two older shelves (+6 titles).** `bowring` gains Sir John Bowring's *Specimens of the Russian Poets* (2 vols, 1821-1823), *Servian Popular Poetry* (1827) and the 1920 *Anthology of Jugoslav Poetry*, which is built mostly on his versions but credits a few other translators per poem. `symonds` gains his *Memoirs of Count Carlo Gozzi* (2 vols, 1890).

**Part 2: twenty-seven new shelves**, mostly working translators with three or more books:

- **Art and science:** `gaston-de-vere` (the complete Vasari, 10 vols), `ft-cooper` (8 French painter monographs, a Balzac life, Montessori's *Pedagogical Anthropology*), `rymer-jones` (Brehm's birds, 4 vols), `hayward-bichat` (Bichat, 4), `robert-willis` (Harvey, 2), `brose` (Moszkowski's *Einstein the Searcher*; Weyl and Freundlich wait in `_pending` because Gutenberg has no plain text for them), `w-johnston` (Beckmann's *History of Inventions*, Paulinus).
- **Travel and war:** `jr-forster` (Kalm's *Travels into North America*, Bougainville), `ab-lindsay` (Semenov's *Tsu-shima*, Nozhin's *Port Arthur*, Kuropatkin, 2 vols), `frederic-whyte` (Schillings's *In Wildest Africa*, Filon's *English Stage*), `alice-werner` (Weule's *Native Life in East Africa*, *The Humour of Holland*).
- **Essays and history:** `brett-feijoo` (Feijoo's *Essays*, 4 vols), `eg-martin` (Imbert de Saint-Amand, 3), `elizabeth-lee` (Jusserand, Maspero, Rosegger's *I.N.R.I.*), `l-williams` (Bruno's *Heroic Enthusiasts*, 2 parts), `sutro` (Maeterlinck, 4).
- **Fiction and drama:** `mg-lewis` ('Monk' Lewis's *Bravo of Venice* and Naubert's *Feudal Tyrants*, 4 vols), `alexander-ewing` (Hoffmann's *Serapion Brethren*, Jean Paul), `herbert-trench` (Merezhkovsky, 2), `mary-wilson` (Heyse, 2), `frances-douglas` (Blasco Ibáñez, 3), `ruth-davis` (Gautier and Loti, Bordeaux), `houghton-translations` (Sabatier's *St Francis*, Bordeaux, Boylesve), `helena-frank` (*Yiddish Tales*, Peretz, Rosenfeld), `poulsson-zwilgmeyer` (Zwilgmeyer, 3), `db-stewart` (Anatole France, 3 files of one book), `sa-eliot` (Wedekind's *Erdgeist*, *Pandora's Box* and *Tragedies of Sex*).

**Merge notes:** Lane D already has `poulsson` and `louise-houghton` shelves, each holding one other book by the same translator. Mine are named `poulsson-zwilgmeyer` and `houghton-translations` so they don't collide; either pair could be merged into one shelf. Lane D's `de-vere` (Aubrey de Vere) and `ewing` (Juliana Horatia Ewing) are different people, so mine are `gaston-de-vere` and `alexander-ewing`.

**Skipped:** Agnes Kinloch Kingston's three Verne translations (Verne has an author shelf from the reading lists) and the Paulus Aegineta and E. Werner translators, whose authors already have shelves.

**Vetoable content:** Wedekind's sex tragedies (`sa-eliot`) are frank for their time; they were famous stage plays and are standard repertory.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 38: twenty-one more translators (2026-10-10)

Twenty-one new shelves, 46 titles, all from Gutenberg, with the translator line read in every header:

**Twenty-one new shelves for translators with two or three books each**, plus one gap-fill: Velma Swanston Howard's translation of Strindberg's *Lucky Pehr* (1912) now sits on `strindberg-english`. Her four Lagerlöf translations are left for the `lagerlof` shelf.

- **Ideas and history:** `w-montgomery` (Schweitzer's *The Quest of the Historical Jesus*, 1910, and *Paul and His Interpreters*), `jb-robertson` (Schlegel's *Philosophy of History*, 2 vols), `ajw-morrison` (Schiller's *Thirty Years' War* and *Revolt of the Netherlands*, Schlegel's *Philosophy of Life*, Goethe's *Letters from Switzerland*), `leon-simon` (Ahad Ha'am's *Ten Essays on Zionism and Judaism*, Einstein's *About Zionism*), `chalmers-mitchell` (Hertwig, Metchnikoff's *The Nature of Man*).
- **Science and travel:** `otte` (Humboldt's *Cosmos* vol. 1 and *Views of Nature*), `troilius` (Linnaeus's *Tour in Lapland*, 2 vols), `co-reilly` (Werne's White Nile expedition, 2 vols), `fayette-robinson` (Brillat-Savarin's *Physiology of Taste*, Sand's *Countess of Rudolstadt*).
- **Fiction and poetry:** `brady-guzman` (Alemán's *Guzman d'Alfarache*, 3 vols), `cr-murphy` (Verhaeren, 3), `willcocks` (Anatole France, 2), `katherine-miller` (Rolland's *Clerambault* and *Colas Breugnon*), `sedgwick-sand` (Sand, 2), `minna-smith` (Palacio Valdés, Pérez Galdós), `ellen-waugh` (Jókai, Ebner-Eschenbach), `mp-waterman` (Heimburg, *Archag*), `raahauge` (Viebig, 2), `monkshood` (Louÿs's *Woman and Puppet*, Bourget), `mp-nichols` (*Gudrun*, Wieck's *Piano and Song*), `eg-rich` (Saint-Saëns's *Musical Memories*, Lafond).

**Two printings to know about:** Einstein's *About Zionism* is a 1930 Soncino Press printing with no copyright line, so it is US public domain since January 2026, the same footing as Pickthall's Quran. Gutenberg's *Cosmos* vol. 1 was keyed from a 1997 Johns Hopkins facsimile of the 1858 Harper printing, without the 1997 introduction. That is the facsimile question again.

**Skipped:** Pauline Flach's and most of Velma Swanston Howard's titles (Lagerlöf has a shelf), Louise Brooks's (Spyri has a shelf), Lansdale's and Varnall's De Amicis, the Doric Race translators (`k-o-muller` exists), and Gutenberg's second file of Schiller's *Thirty Years' War* (a duplicate).

**Vetoable content:** Louÿs's *Woman and Puppet* is a sensual novel, not an explicit one.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 39: fifty-two more translators (2026-10-10)

Fifty-two new shelves, 99 titles, all from Gutenberg, with the translator line read in every header:

**Fifty-two new shelves for translators with one or two books each.** All are from Gutenberg, and the translator line was read in every header.

- **Religion and ideas:** `george-eliot-translations` (Strauss's *The Life of Jesus Critically Examined* and Feuerbach's *The Essence of Christianity*, the two books that carried German higher criticism into English), `tk-abbott` (Kant's *Fundamental Principles of the Metaphysic of Morals* and *Metaphysical Elements of Ethics*), `neil-buchanan` (Harnack's *History of Dogma*, vols 1-2), `ager` (Swedenborg's *Heaven and Hell* and *Divine Love and Wisdom*), `mh-allies` (John of Damascus on holy images; Chrysostom), `ella-mcmahon` (Caussade's *Abandonment*; St Francis de Sales), `fe-cox` (*Hymns from the German*, 2 books), `gorfinkle` (*Pirke Avot*), `kenrick` (Strauss's *Helon's Pilgrimage to Jerusalem*), `ac-middleton` (d'Holbach's *Letters to Eugenia*, an atheist polemic), `ingeborg-andersen` (Drachmann's *Atheism in Pagan Antiquity*).
- **Socialism and psychology:** `ch-kerr` (Labriola, Lafargue's *The Right to Be Lazy*), `la-monte` (Ferri, Deville), `jelliffe` (Silberer's *Hidden Symbolism of Alchemy*, Rank's *The Myth of the Birth of the Hero*).
- **History and travel:** `robert-parke` (Mendoza's *History of China*, 1588, 2 vols), `maver` (Zúñiga's *Philippine Islands*, 2 vols), `jv-huntington` (Franchère's *Voyage to the Northwest Coast*), `alexander-muir` (Gregorovius's *Corsica*), `robert-harrison` (Reumont's *Lorenzo de' Medici*), `maidment` (Funck-Brentano, 2), `fa-holt` (Gilliard's *Thirteen Years at the Russian Court*), `amelia-edwards` (Maspero's *Egyptian Archaeology*), `katharine-babbitt` (two French war memoirs), `h-parker` (*Village Folk-Tales of Ceylon*, vols 1-2), `emily-hill` (Karasowski's *Chopin*), `krh-mackenzie` (*Tyll Owlglass*, Hesekiel's *Bismarck*).
- **Fiction, essays and drama:** `jd-duff` (Aksakov, Herzen's *Memoirs*), `cb-jordan` (*The Four Horsemen of the Apocalypse*, *Mare Nostrum*), `mrs-gillespie` (*The Shadow of the Cathedral*, *Blood and Sand*), `rb-douglas` (*Thaïs*, the *Cent Nouvelles Nouvelles*), `ernest-bell` (Lessing), `cecil-fairfax` (Bjørnson), `pf-bicknell` (Jókai), `burette` (Tieck), `henry-harland` (Feuillet, Serao), `home-gordon` (Faguet), `john-howard` (Gourmont), `eleanor-brooks` and `van-wyck-brooks` (Duhamel, Rolland, Bazalgette's *Thoreau*), Anatole France from `mrs-john-lane` and `drillien`, Loti from `marjorie-laurie` and `baines`, and smaller shelves: `lg-meyer`, `ca-manning`, `kingsbury`, `nk-hills`, `wf-harvey`, `je-fries`, `fraprie`, `mrs-l-burke`, `abby-alger`.

**Three more post-1930 printings:** Gutenberg keyed Silberer from the Dover 1971 reprint, which says it is "unabridged and unaltered" from 1917. Swedenborg's *Divine Love and Wisdom* is from a 1988 Swedenborg Foundation printing of Ager's pre-1931 revised translation. Mendoza's *China* is from Burt Franklin's 1970 facsimile of the 1853-1854 Hakluyt edition. Each carries a note, and the first two join the late-reprint question and the third the facsimile question.

**Dropped or merged:** Lionel Giles's *Art of War* is already on my `giles` shelf; Gutenberg's two further files of it are recorded there as excluded. Lawson's translation of Einstein's *Relativity* has no plain-text file on Gutenberg, so that shelf was dropped. Manning's *Shevchenko* (1945) is excluded as post-1930. Lane D's `babbitt` and `bicknell` shelves and the reading lists' `george-eliot` are other people, so mine are named `katharine-babbitt`, `pf-bicknell` and `george-eliot-translations`.

**Lane A may want some of these:** `mh-allies`, `ella-mcmahon`, `neil-buchanan`, `ager` and `fe-cox` are devotional or theological. No other lane shelves them yet. They can move if Lane A claims them.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 40: three more translators (2026-10-10)

Three new shelves, 93 titles, all from Gutenberg, with the translator line read in every header:

**A new kind of shelf.** Every translator with two or more books on Gutenberg now has a shelf. What remains is about a thousand translators with a single book each, and many of those books are classics. One shelf per translator would mean a thousand tiny shelves, so this round starts **single-translation shelves**. Each is grouped by subject and holds many translators, and each title still gates on its own translator's name (`_surname_by_slug`), the same way `strindberg-english` works. Say if you would rather have one shelf per translator.

- **`singles-medieval-epic`** (27): *The Anglo-Saxon Chronicle* (Ingram and Giles), Saxo Grammaticus's *Danish History* (Elton), the *Táin* twice (Faraday, Dunn), *La Chanson de Roland* (Rabillon), Bédier's *Tristan and Iseult* (Belloc), *The High History of the Holy Graal* (Evans), *Barlaam and Ioasaph* (Woodward and Mattingly), *Laxdæla Saga* and *Eirik the Red's Saga*, Old English poems (Andreas, Elene, Judith, Brunanburh), Kuno Meyer's *Ancient Irish Poetry*, *The Lay of the Cid*, Tegnér's *Fridthjof's Saga*, Barclay's *Ship of Fools* (1509), Mickle's *Lusiad*, Villani, the *Philobiblon*, Trevisa's Bartholomew Anglicus, Benjamin of Tudela, the Hawaiian *Laieikawai*, *The Visions of the Sleeping Bard*, and Dallington's *Hypnerotomachia* (1592).
- **`singles-ideas`** (26): Burckhardt's *Civilisation of the Renaissance in Italy* (Middlemore), Bergson's *Creative Evolution* and *Dreams*, *Amiel's Journal* (Mrs Humphry Ward), Machiavelli's *Discourses* (Thomson), Kandinsky's *Concerning the Spiritual in Art* (Sadleir), Engels's *Condition of the Working-Class in England* (Kelley), Planck's quantum lectures, Lavoisier's *Elements of Chemistry* (Kerr, 1790), Comenius's *Orbis Pictus* (Hoole), Descartes, A. W. Schlegel's *Lectures on Dramatic Art*, La Rochefoucauld, Schopenhauer (Dircks), Condorcet on women's rights, Jellinek, Kropotkin, Michelet's *La Sorcière*, Leonardo's *Thoughts on Art and Life* (Baring), Ptah-Hotep, Ibn Tufayl, Bastiat (2), Falckenberg, Ribot and Tarde. Hilbert, Dedekind and Ramus wait in `_pending` because Gutenberg has no plain text for them.
- **`singles-literature`** (40): Lermontov's *A Hero of Our Time*, Pushkin's *Eugene Onegin* (Spalding, 1881) and *Boris Godunov*, Mickiewicz's *Pan Tadeusz* (Noyes) and *Konrad Wallenrod*, Sōseki's *Botchan*, Hémon's *Maria Chapdelaine*, Azuela's *The Underdogs*, Huysmans's *Against the Grain* and *Là-bas*, *Certain Noble Plays of Japan* (Fenollosa's manuscripts, finished by Pound), Cervantes's *Exemplary Novels*, Novalis's *Henry of Ofterdingen*, Holberg (2), Kalidasa (Griffith), Leopardi, Emma Lazarus's *Heine*, Nekrasov, Musset, Boccaccio's *Fiammetta*, *Paul and Virginia* (Helen Maria Williams), Lessing's *Nathan the Wise*, Schiller's *Mary Stuart*, Corneille's *Polyeucte*, Molière (2), Maeterlinck (Hovey), Rostand's *L'Aiglon*, Kochanowski's *Laments*, Kartini's letters and others.

**Printings to know about:** Gutenberg's *Hypnerotomachia* is from a 1969 facsimile of the 1592 printing (the facsimile question). *The Underdogs* is Munguía's 1929 translation, but Gutenberg's copy comes from a printing after 1952: its unsigned biographical preface mentions Azuela's death (the late-reprint question, plus a preface that may itself be in copyright).

**Left for their owners:** Samuel Butler's *Iliad* (the `homer` shelf holds Homer by translator), Gardiner's *Cligés* (`chretien`) and Worthington's *Émile* extracts (`rousseau-emile`). Two modern translations, Adams and Harmelin's Daudet and Cropley's *Bearslayer*, are excluded.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 41: three more translators (2026-10-10)

Three new shelves, 124 titles, all from Gutenberg, with the translator line read in every header:

**Three more single-translation shelves** (124 titles), built the same way as round 40's, where each title gates on its own translator.

- **`singles-history-travel`** (44): *The Bābur-nāma* (Annette Beveridge), the Gentleman of Elvas on de Soto (Hakluyt, 1609), the journal of Vasco da Gama's first voyage and Schiltberger's *Bondage and Travels* (both Hakluyt Society), Gómara's *Conquest of the West India* (1578), Garibaldi's memoirs (1859), Moltke's *Franco-German War*, Slatin's *Fire and Sword in the Sudan*, Wace's chronicle of the Norman Conquest, Villari's Florence, Charnay's *Ancient Cities of the New World*, Leti's *Il Nipotismo di Roma* (1669), Kâtip Çelebi's *Maritime Wars of the Turks*, *The Devils of Loudun*, Vertot's *Revolutions of Portugal*, Turpin's *Siam*, the Moscow plague of 1771, Mardiganian's *Ravished Armenia*, and First World War memoirs and records (Richthofen, Genevoix's *'Neath Verdun*, Plüschow, the *Ayesha*, the *Deutschland*, the Kaiser's memoirs, the German General Staff's *War Book*, *Ypres 1914*).
- **`singles-science-craft`** (39): Agricola's *De Re Metallica* (Herbert and Lou Hoover), Galileo's *Sidereal Messenger* and *Discourse* on floating bodies (Salusbury, 1663), Goethe's *Theory of Colours* (Eastlake), Petrus Peregrinus on the magnet, Poincaré's *Foundations of Science*, La Mettrie's *Man a Machine*, *The Montessori Method*, Forel's *Ants*, Flammarion's *Urania*, Comte's *Philosophy of Mathematics*, Vallery-Radot's *Pasteur*, Dunant's *Origin of the Red Cross*, Senefelder's *Invention of Lithography*, bookmaking and engraving, Lavater's *Of Ghostes and Spirites* (1572), Vigenère's *Fire and Salt* (1649), Paulli on tobacco, tea, coffee and chocolate, Bourgelat's horsemanship, Bazancourt's *Secrets of the Sword*, Wundt (2), Ebbinghaus, Binet, Herbart and Jespersen. Six physics and mathematics books (Einstein's *Meaning of Relativity*, Planck ×3, Gauss, Klein) wait in `_pending` because Gutenberg has them only as PDF, LaTeX or HTML.
- **`singles-ideas-2`** (41): Durkheim's *Elementary Forms of the Religious Life* (Swain), Engels's *Socialism, Utopian and Scientific* (Aveling), Kant's *Critique of Judgement* (Bernard) and *Perpetual Peace*, Grotius's *Rights of War and Peace*, Pascal's *Thoughts* (Kegan Paul), Schopenhauer's *Basis of Morality* and *Fourfold Root*, Croce on Vico (Collingwood) and on Marx, Trotsky's *Our Revolution* (1918), Bebel's *Woman and Socialism*, Liebknecht, Sombart, Oppenheimer's *The State*, Stendhal's *On Love* (the Woolfs), Comte's *General View of Positivism*, Petrarch's *Letters to Classical Authors* and *Secret*, Della Casa's *Galateo* (Peterson, 1576), Maimon's autobiography, Halévy's *Nietzsche*, Drews's *The Christ Myth*, d'Holbach (2), Eucken (2), Cousin, Gentile, Goldziher, Leopardi's *Essays and Dialogues*, Steiner and others.

**Two more post-1930 printings (late-reprint question):** Gutenberg keyed *De Re Metallica* from the Dover 1950 edition, which calls itself "a complete and unchanged reprint" of 1912. Durkheim comes from the fifth impression (1964) of the 1915 setting.

**Left for their owners:** Hammer-Purgstall's *Assassins* (`hammer-purgstall`), Tocqueville's *State of Society in France* (`tocqueville`), and three Freud translations (`freud`).

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 42: two more translators (2026-10-10)

Two new shelves, 96 titles, all from Gutenberg, with the translator line read in every header:

**Two more single-translation shelves** (96 titles), built like rounds 40-41: each title gates on its own translator.

- **`singles-continental-fiction`** (64): the German novel and novella of the 1870s-90s in American and British translations (Auerbach ×3, Heyse ×4, Spielhagen ×3, E. Werner ×3, Ossip Schubin ×3, Franzos ×2, Heimburg, Dahn, Reuter, Hausrath, Kohn, Gerstäcker, Keller's *Seven Legends*, Sudermann's *The Wish*), Thomas Mann's *Royal Highness* (Curtis, 1916), Jókai by four translators other than Bain, Bjørnson's *Arne* and *In God's Way*, Ingemann, Kraszewski's *The Jew*, Couperus's *Psyche*, Van Eeden's *The Quest*, De Coster's *Ulenspiegel* (Whitworth) and *Flemish Legends*, Blasco Ibáñez ×2, Turgenev's *Annouchka*, Hugo's *Toilers of the Sea* (W. Moy Thomas), Dumas's *Prussian Terror* (R. S. Garnett), Paul de Kock, Laclos's *Dangerous Connections* (1812), Gourmont ×2 (one is Aldous Huxley's *A Virgin Heart*, 1921), Leblanc's *Arsène Lupin versus Herlock Sholmes*, Aimard, Pardo Bazán, Trueba's *Cid Campeador*, Guerrazzi, Strindberg's *On the Seaboard*, Cyrano de Bergerac's *Voyage to the Moon* (Lovell, 1687) and Tyssot de Patot's *James Massey* (Whatley, 1733).
- **`singles-verse-drama-tales`** (32): six Sudermann plays (among them Edith Wharton's *The Joy of Living*, 1902, and *Magda*), Heijermans's *The Ghetto*, Vondel's *Lucifer* (Van Noppen), Rostand's *Cyrano* (Renauld), Wilde's *Salomé* (Lord Alfred Douglas), Holberg's *Jeppe on the Hill*, Marie Stopes's *Plays of Old Japan: The Nō*, the libretto of Flotow's *Martha*; Baudelaire's *Flowers of Evil* (Cyril Scott), Christine de Pisan's *Duke of True Lovers* (Binyon), Quevedo's *Visions* in two translations (L'Estrange, Elliot), Iriarte's *Literary Fables*, Sibbald's *Inferno*, Gilbert Hay's Scots *Buke of the Order of Knyghthood* from Llull; the *Kathá Sarit Ságara* (Tawney), the *Kādambarī* (Ridding), Vidyāpati (Coomaraswamy), *Chaitanya's Life and Teachings* (Sarkar), the *Jātakamālā* (Speyer); and *Old Celtic Romances* (Joyce), *Tales from the Old French* (Isabel Butler), *Zanzibar Tales*, *Roumanian Stories*, *Caucasian Legends*, *Aw-Aw-Tam Indian Nights* and *Chinese Mother Goose Rhymes*.
- **Left for their owners:** Lagerlöf's *From a Swedish Homestead* (the `lagerlof` shelf, Lane D) and two Tudor Erasmus translations, Hake's *Diversoria* and Leigh's *Modest Meane to Mariage* (the `erasmus` shelf).
- **For Adam:** *Salomé* and *Cyrano* sit here because Wilde's and Rostand's own shelves (if any) don't hold these translations; move them if you'd rather keep a writer's works together. No late printings turned up in the year check.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 43: two more translators (2026-10-10)

Two new shelves, 106 titles, all from Gutenberg, with the translator line read in every header:

**Two more single-translation shelves** (106 titles), built the same way: each title gates on its own translator.

- **`singles-fiction-2`** (67): Pushkin's prose tales (Keane) and *The Queen of Spades* (Sutherland Edwards), Gogol's *Cossack Tales* and *Home Life in Russia*, Andreyev ×4 (*The Red Laugh*, *The Dark*, *The Little Angel*, *When the King Loses His Head*), Gorky's *Three Men*, Kuprin's *A Slav Soul*, Chekhov's *Black Monk* (R. E. C. Long), Tolstoy's *Sebastopol* (Frank Millet), Fernán Caballero's *La Gaviota*, Madame de Staël's *Corinne* (Isabel Hill), Le Sage's *Asmodeus*, Cervantes's *Persiles and Sigismunda* and *Galatea*, Lope de Vega's *Pilgrim of Castile* (1621), Bécquer's *Romantic Legends of Spain*, Alarcón, Pardo Bazán, Verga's *House by the Medlar-Tree*, Serao ×2, D'Annunzio, Hugo's *Last Day of a Condemned*, Balzac's *Love in a Mask*, George Sand's *Marquis de Villemer*, Zola ×2, Mirbeau's *Calvary*, Loti's *Last Days of Pekin*, Bourget ×2, Anatole France ×2, Apollinaire's *The Poet Assassinated* (Matthew Josephson, 1923), Gide's *Prometheus Illbound* (1919), Maurois's *Ariel* (Ella D'Arcy, 1924), Le Corbeau's *The Forest Giant* (T. E. Lawrence, 1924), Xavier de Maistre's *Journey Round My Room*, Carové's *Story Without an End* (Sarah Austin), Suttner's *Lay Down Your Arms*, Sienkiewicz's *Through the Desert*, Undset's *Jenny* (1921), Jonas Lie, Topelius, Siwertz, Rosegger, the Comtesse de Ségur, Erckmann-Chatrian, Eugène Sue, Aubert de Gaspé's *Cameron of Lochiel* (Charles G. D. Roberts), Perelaer's *Baboe Dalima*, Murai's *Kibun Daizin* and Maupassant (Ernest Boyd).
- **`singles-plays-poetry-2`** (39): Gorky's *The Lower Depths*, Schnitzler's *Hands Around* (1920), Claudel's *Tête-d'Or*, Brieux's *Three Plays* (with Shaw's preface), Echegaray ×2, Sardou's *The Sorceress*, Heijermans's *The Good Hope*, Cervantes's *Numantia*, Mitra's *Nil Darpan* (Madhusudan Dutt, 1861), the *Chushingura*, Roswitha's plays (Christopher St. John), *Cavalleria Rusticana*; Petrarch's sonnets (Higginson), Garcilaso (Wiffen, 1823), Leopardi, Mistral's *Mirèio* (Harriet Preston), Boiardo's *Orlando Innamorato* (W. S. Rose), La Fontaine (Thornbury), Oehlenschläger's *Gods of the North*, Pushkin's poems (Panin), Arthur Way's *Lay of the Nibelung Men*, the *Orkneyinga Saga*, *The King's Mirror*, the *Dean of Lismore's Book*, *Antar*, Abu'l-Ala's *Luzumiyat* (Rihani), Rumi's *Mesnevi* (Redhouse), Sadi's *Bustān*, Iqbal's *Secrets of the Self* (Nicholson, 1920), the Childers *Jātaka*, the *Diamond Sutra*, *Sumerian Hymns*, *Fir-Flower Tablets* (Ayscough and Amy Lowell), *Diaries of Court Ladies of Old Japan*, Halper's *Post-Biblical Hebrew Literature*, Christine de Pisan's *Othea* (Scrope) and *The Babees' Book*.
- **Left out:** Spyri's *The New Year's Carol* (for the `spyri` shelf, Lane D) and *The Jade Flute*, whose translator is unnamed, so the per-title gate has nothing to check. Devotional titles in this stretch of the list (Chantal's letters, Challoner's *Following of Christ*, Ann Griffiths's hymns, Kurtz's *Church History* and others) are left for Lane A.
- **For Adam:** *Hands Around* is Schnitzler's *Reigen*, a cycle of seduction scenes; veto it if you'd rather not have it. No late printings turned up in the year check.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 44: one more translators (2026-10-10)

One new shelves, 68 titles, all from Gutenberg, with the translator line read in every header:

**A third fiction shelf** (68 titles), built the same way.

- **`singles-fiction-3`** (68): Luo Guanzhong's *Romance of the Three Kingdoms* (Brewitt-Taylor, 1925), Remarque's *All Quiet on the Western Front* (A. W. Wheen, 1929), Hesse's *Steppenwolf* (Basil Creighton, 1929), Rølvaag's *Giants in the Earth* (1927), Thomas Mann's *Death in Venice* (Kenneth Burke, 1925), Čapek's *Krakatit*, Kivi's *Seven Brothers* (1929), Mauriac's *Thérèse* and *The Kiss to the Leper*, Undset's *The Bridal Wreath*, Couperus's *Eline Vere*, Multatuli's *Max Havelaar*, Rolland's *Annette and Sylvie*, Merezhkovsky's *Akhnaton*, Morand's *Lewis and Irene*, Natsume's *Unhuman Tour*, Tanizaki's *A Spring-time Case*, Bettauer's *The City Without Jews*, Norbert Jacques's *Dr. Mabuse*, Leroux's *The New Terror*, Rousseau's *Eloisa* (Kenrick, 1761), Kotzebue's *Virgin of the Sun* (Anne Plumptre), Nodier's *The Bibliomaniac*, George Sand's *The Naiad*, Auerbach's *Little Barefoot*, Chekhov's *Shooting Party* (Chamot), Andreyev's plays, Hauptmann's *Coming of Peace*, Hebbel's *Three Plays*, D'Annunzio ×2, Lope de Vega's *New Art of Writing Plays*, Goethe and Schiller's *Xenions*, Michelangelo's sonnets (Newell), Petrarch (*Love's Crucifix*, Agnes Tobin), Shevchenko's *Kobzar*, Hálek's *Evening Songs*, the *Prem Sagur*, *Mary of Nimmegen*, the *Táin* in Mary Hutton's verse, Pearse's collected works, Louÿs's *Songs of Bilitis*, Terrasson's *Sethos* (1732), Swedish, French, Costa Rican and Arabian tales, Pollen's *Rhymes from the Russian*, *Songs of the Slav* and Voynich's *The Humour of Russia*.
- **Waiting in `_pending`:** three translations first published in 1930: Kästner's *Emil and the Detectives* (May Massee), Svevo's *Confessions of Zeno* (Beryl de Zoete) and Akutagawa's *Tales Grotesque and Curious*. They became US public domain on 1 January 2026, but the gate still treats 1930 as in copyright, so they wait on the same override as Pickthall's Quran.
- **Left for the owner:** Lagerlöf's *Liliecrona's Home* (the `lagerlof` shelf, Lane D).
- **For Adam:** Louÿs's *Songs of Bilitis* (1923) is frankly erotic verse; veto it if you'd rather not have it. Hutton's *Táin* scan carries her 1948 presentation inscription; the text itself was first printed in 1907.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 45: one more translators (2026-10-10)

One new shelves, 72 titles, all from Gutenberg, with the translator line read in every header:

**A second history shelf** (72 titles), built the same way.

- **`singles-history-2`** (72): Gregory of Tours's *History of the Franks* (Ernest Brehaut, 1916), Alberuni's *India* (Sachau), Columbus's *Select Letters* (R. H. Major, Hakluyt Society), Barbaro and Contarini's *Travels to Tana and Persia* (Hakluyt Society), the *Mulfuzāt Timūry*, Nicolaus of Damascus's *Life of Augustus*, Naima's *Annals of the Turkish Empire*, the *Baz-nama-yi Nasiri*, al-Tūnisī's *Travels of an Arab Merchant in Soudan*, the *Life of Omar ibn Said* (written in Arabic in North Carolina by an enslaved man), Jusserand's *English Wayfaring Life in the Middle Ages* (Lucy Toulmin Smith), Maulde-La-Clavière's *Women of the Renaissance*, Guizot on Washington and on representative government, Grellmann's *Dissertation on the Gipseys* (1787), *The Discoveries of John Lederer* (1672), Stutterheim's *Austerlitz*, the Dreyfus letters, Lepsius's *Letters from Egypt*, the German Arctic expedition of 1869-70, De Amicis's *Morocco*, Vogüé's *The Russian Novelists*, lives and memoirs of Wagner, Baudelaire, Berlioz, Chopin, Sarah Bernhardt, Ludwig II, Carmen Sylva, Gandhi (Rolland, 1924), D'Eon, Maria Stella and the Countess of Lichtenau, Russian exile and Siberian memoirs, and First World War records (Bédier's *German Atrocities*, the German White Book, Hedin's *With the German Armies in the West*).
- **Left for others:** devotional and church titles in this stretch (Kurtz, Hippolytus's *Apostolic Tradition*, Huss's letters, Pusey's *Confessions*, the *Martyrs Mirror* and others) stay for Lane A. Mussolini's 1923 speeches are left off by judgment; say if you want them as a primary source.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 46: two more translators (2026-10-10)

Two new shelves, 119 titles, all from Gutenberg, with the translator line read in every header:

**Two more single-translation shelves** (119 titles), built the same way.

- **`singles-ideas-3`** (48): Machiavelli's *The Prince* (Luigi Ricci, 1903), Castiglione's *Book of the Courtier* (Opdycke, 1901), Maimonides's *Guide for the Perplexed* (Friedländer), Bergson's *Time and Free Will* (Pogson, 1910), Laplace's *Philosophical Essay on Probabilities*, Valla's *Donation of Constantine* (Coleman, 1922), Descartes's *Six Metaphysical Meditations* (Molyneux, 1680), Avicenna's *Compendium on the Soul*, Averroes, al-Ghazzali, de Boer's *History of Philosophy in Islam*, Asín Palacios's *Islam and the Divine Comedy*, Glanville on English law (Beames), Scott's *Visigothic Code*, Grotius's *Freedom of the Seas*, Callières on negotiating, Napoleon's *Maxims of War*, Vives's school dialogues, Petrarch's letters, Winckelmann (Fuseli, 1765), Fontenelle's *Plurality of Worlds*, Rohde's *Psyche*, Fustel de Coulanges, Solovyov's *Justification of the Good*, Chamfort, Nostradamus (Garencières, 1672), Éliphas Lévi's *History of Magic* (Waite), the *Book of Filial Duty*, Fechner, Hilty ×2, Ellen Key, Stekel, Flournoy, Compayré, Gide and Rist, Zetkin, Pannekoek and Bonger.
- **`singles-science-2`** (71): Carnot's *Reflections on the Motive Power of Heat* (Thurston), Huygens's *Celestial Worlds Discover'd* (1698), Pasteur's *Studies on Fermentation*, Sachs's *History of Botany*, Helmholtz's *Popular Lectures*, Metchnikoff, Behring, Hansen on leprosy, Bichat (Houlton) and Desault, Marie Curie's *Pierre Curie*, Arrhenius, Holst and Kramers on the Bohr atom, Warming, Huber's ants, Fabre's *Insect Life* (Margaret Roberts), Bergman's mineralogy (Withering), Glauber and Sendivogius on alchemy, Chevreul on colour, Cellini's treatises on goldsmithing and sculpture (Ashbee), Vasari on technique, Koldewey's *Excavations at Babylon*, Rodin on art, Robert-Houdin's *Secrets of Stage Conjuring*, Groos's *Play of Man*, Mosso's *Fear*, Ritter's *Comparative Geography*, Flammarion, and handbooks on lithography, pigments, perfumes, horseshoeing, bees, music, warfare and engines.
- **Waiting in `_pending`:** Newton's *Principia* (Andrew Motte) and Menabrea's *Sketch of the Analytical Engine* with Ada Lovelace's Notes. Gutenberg has both only as HTML, because of the mathematics. They are worth a later pass from period scans.
- **Left out by judgment:** Pouchet's *Plurality of the Human Race* (1864 polygenist race science, the same call as Gobineau), Krafft-Ebing, Forel's *Sexual Ethics* and Fehlinger (the same call as the other sexology titles), the *Protocols* (a forgery), and the Freud titles (left for the owner of the Freud translations). Pascal's *Provincial Letters* (M'Crie) stays for Lane A.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 47: one more translators (2026-10-10)

One new shelves, 51 titles, all from Gutenberg, with the translator line read in every header:

**A miscellany shelf** (51 titles) from the earlier stretch of the single-translator list, built the same way.

- **`singles-arts-miscellany`** (51): Leonardo's *Treatise on Painting* (Rigaud), Bosanquet's translation of Hegel's *Introduction to the Philosophy of Fine Art* (1886), Dürer's *Of the Just Shaping of Letters*, Forkel's *Bach* (C. S. Terry, 1920), Rimsky-Korsakov's *Principles of Orchestration*, Rolland's *Handel*, Rosa Newmarch's *Tchaikovsky*, the recollections of Gounod and Massenet, Duprè, Rodin, Reber's *History of Ancient Art*, Lalanne on etching, bookbinding, leather, the violoncello, singing; Thomas Platter's autobiography, the Countess Krasinska's journal, Juliette Drouet's letters to Hugo, Princess Louise of Belgium's *My Own Affairs*; King Alfred's Old English *Soliloquies* of Augustine, R. W. Church's *Dante* with F. J. Church's *De Monarchia*, the *Dhammapada* (Woodward), Gandhi's *Guide to Health*, Merezhkovsky's *Flaubert*, Rydberg's *Magic of the Middle Ages*, Heeren's *Ancient History*, Renan's English conferences, Pfungst's *Clever Hans*, Taine's *Pyrenees*, *Nooks and Corners of Old Paris*, *Guilds in the Middle Ages*, *Acrobats and Mountebanks*, *The Book of Vagabonds and Beggars* (Luther's *Liber Vagatorum*), French cookery, Vesuvius in 1872, and a few First World War and Weimar documents.
- **For Adam:** Gutenberg's *Principles of Orchestration* was keyed from the 1964 Dover reprint of Agate's 1922 translation. That makes twelve late reprints; the words are public domain.
- **Waiting / left out:** Van Gogh's *Letters of a Post-Impressionist* is in `_pending` (Gutenberg has HTML only); Busch's *Buzz a Buzz* has no plain text either and is excluded, as the `wilhelm-busch` shelf already notes.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 48: one more translators (2026-10-10)

One new shelves, 99 titles, all from Gutenberg, with the translator line read in every header:

**A fourth fiction shelf** (99 titles), from titles the earlier single-translation rounds had passed over.

- **`singles-fiction-4`** (99): Luise Mühlbach's historical novels by five translators, Pushkin ×3, Dostoevsky's *Grand Inquisitor* (translated by H. P. Blavatsky, 1881), Sienkiewicz's *Without Dogma* and *Sielanka*, Hamsun ×2, Ibsen's *Early Plays* (Orbeck, 1921), Sudermann's *Dame Care*, Zola ×2, Daudet ×2, Balzac, Anatole France's *Queen Pedauque*, Coppée ×2, About's *The Man with the Broken Ear*, Erckmann-Chatrian, Eugène Sue ×3 (one by Solon De Leon), Jókai ×2, Mikszáth ×2, Kielland ×2, Jonas Lie, Bjørnson (Gosse), Reymont's *The Comedienne*, Multatuli's *Walter Pieterse*, Rizal's *Friars and Filipinos* (Gannett's abridgement), Baroja's *Caesar or Nothing*, Blasco Ibáñez's *Woman Triumphant*, Palacio Valdés, Audoux's *Marie Claire*, Colette's *Barks and Purrs*, Benoît's *Atlantida*, Barbusse's *The Inferno*, Maurois's *General Bramble*, Jammes, Tieck (Connop Thirlwall), Zschokke, Scheffel's *Trumpeter of Säkkingen*, Schiller's *Turandot*, Kotzebue's *The Stranger*, Iffland's *The Lawyers*, Corneille's *The Cid*, Thoma's *Moral*, Sacher-Masoch's *Venus in Furs*, Sholem Aleichem's *Jewish Children*, Kompert, Steinberg, Dante's *Banquet*, Milton's Latin and Italian poems (Cowper), Palamas, the *Mārkaṇḍeya Purāṇa*, Dandin's *Ten Princes*, Shinran's *Buddhist Psalms*, Mathers's *Garden of Bright Waters*, the Countess of Pembroke's Mornay and Garnier's *Antonius* (1592), and anthologies of Malayan, Armenian, Persian, Welsh, Hindustani and Russian verse and tale.
- **For Adam:** *Venus in Furs* (1870; Savage's translation, 1921) is the novel masochism is named after; veto it if you'd rather not have it. Gutenberg's *General Bramble* was keyed from a 1931 reprint of the 1921 translation, which makes thirteen late reprints.
- **Left out:** Karl May's *Travel Tales in the Promised Land* (Gutenberg's header says COPYRIGHTED, and the gate refused it), Mickiewicz's *My First Battle* (translated for Gutenberg in 2009), and Aanrud's *Lisbeth Longfrock* (for Lane D's `poulsson` shelf). Verne's translations stay with the `verne` shelf's owner; Butler's *Iliad*, *Cligès* and the Erasmus *Colloquies* likewise.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 49: one more translators (2026-10-10)

One new shelves, 84 titles, all from Gutenberg, with the translator line read in every header:

**A second non-fiction shelf** (84 titles) from titles the earlier single-translation rounds had passed over.

- **`singles-nonfiction-2`** (84): Peter Martyr's *De Orbe Novo* (MacNutt, 1912), Morga's *History of the Philippine Islands*, Pedro Sancho's *Account of the Conquest of Peru* (Means, 1917), Lobo's *Voyage to Abyssinia* in Samuel Johnson's 1735 translation (his first book), the Tudor Translations Machiavelli (Dacres's *Discourses* and *Prince*, 1636, with Whitehorne's *Art of War*), Dürer's journeys to Venice and the Low Countries, Hugo's *History of a Crime*, Lamartine's *History of the Girondists*, Gregorovius's *Lucretia Borgia*, Guizot's *Memoirs*, Blakman's *Henry the Sixth* (M. R. James, 1919), Nordenskiöld's *Voyage of the Vega*, Arago's *Biographies of Distinguished Scientific Men*, the Sand-Flaubert letters, Liszt's *Chopin*, Wagner's *On Conducting*, Tosi on florid song (Galliard, 1743), Feuillet's *Orchesography* (Weaver, 1706), Busoni, Saint-Saëns, Lilli Lehmann's *How to Sing*, Rolland's *Musicians of To-day*, Ardant du Picq's *Battle Studies*, Bernhardi, Boelcke and von Forstner, Froebel's autobiography, Preyer's *Mind of the Child*, Hans Gross's *Criminal Psychology*, Fritz Müller's *Facts and Arguments for Darwin*, Ehrlich, Koch, Basil Valentine, two old treatises on chocolate (1652 and 1730), Holbach's *Superstition in All Ages*, Hertzka's *Freeland*, Charles Wagner's *The Simple Life*, Tolstoy on Shakespeare, Faguet, Le Roy, Rathenau, Edward Lasker's *Chess Strategy*, fencing and Hindu law.
- **For Adam:** three more works survive on Gutenberg only as later facsimiles or reissues: Rapin's *De Carmine Pastorali* in Creech's 1684 translation (Augustan Reprint Society, 1947, with a short modern introduction), Gregorovius's *Lucretia Borgia* (1904 translation, Blom reissue 1968) and Tosi's *Observations on the Florid Song* (Galliard, 1743; Reeves reprint 1967). That makes nine facsimiles.
- **Left out:** Nicole's *Essay on True and Apparent Beauty*, because J. V. Cunningham translated it in 1950, and Fernández Bolívar's *Mathematical-Historical Principles* (a modern author). Devotional titles in this stretch stay for Lane A: the Smalcald Articles, Luther's *Table Talk*, Jewel's *Apology*, Catherine of Siena's letters, the lives of St Teresa, St Declan and Ciaran, Thomas à Kempis's chronicle, Aquinas on prayer, Rolle, Swedenborg and the hymn books.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. No uids minted.

## Round 51: period scans for the HTML-only titles (2026-10-17)

Nine titles that waited in `_pending` because Gutenberg has them only as HTML (mathematics) now come from period Internet Archive scans, each with the translator's name and the imprint year read in the OCR. All are raw OCR: the prose reads, the formulas and diagrams do not.

- **`singles-science-2`** (+2): Newton's *Principia* in Andrew Motte's translation, Daniel Adee's New York edition of 1846 (the one Gutenberg 76404 transcribed), with the System of the World; and Menabrea's *Sketch of the Analytical Engine* with Ada Lovelace's Notes A to G, cut from *Scientific Memoirs* vol. III (London, 1843), the first printing. That printing names her only as "A. A. L.", so its name check is excused by eye (`_identity_checked`).
- **`singles-science-craft`** (+6): Einstein's *The Meaning of Relativity* (Adams; Princeton 1923), Gauss's *General Investigations of Curved Surfaces* (Morehead and Hiltebeitel; Princeton 1902), Klein's *On Riemann's Theory of Algebraic Functions* (Frances Hardcastle; 1893), and three Planck volumes: *Eight Lectures on Theoretical Physics* (Wills; Columbia 1915), *The Theory of Heat Radiation* (Masius; 1914) and *Treatise on Thermodynamics* (Ogg; Longmans 1903).
- **`singles-arts-miscellany`** (+1): Van Gogh's *Letters of a Post-Impressionist* (Ludovici; Constable 1912).
- **Still pending:** Ramus's *Way to Geometry* (Bedwell, 1636): no scan found outside Gutenberg's own.
- 🔴 **For whoever owns `adler_shelf.json` (found 2026-10-17):** its `newton-principia` entry says "tr. Motte", but Gutenberg 28233 is the **1687 Latin first edition** (*Philosophiae Naturalis Principia Mathematica*, "Jussu Societatis Regiae ac Typis Josephi Streater"). The label is wrong; the text is a real treasure. With Motte's English now on `singles-science-2`, the repo holds the Latin and the English of the Principia, which is the pairing Adam asked for with Aquinas and Aristotle. Lane C may not edit that file, so the label stays wrong until its owner fixes it.

Ids were checked across all branches: no clashes. Verified and recorded: 0 mismatched, 0 rights flags. The only post-1930 year in any front matter is the 2016 digitisation date on the Scientific Memoirs scan. No uids minted.

