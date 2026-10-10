# Lane C — Translator shelves: digest (read first)
Totals 2026-10-10T12:36-05:00: 270 shelves, 1287 titles. By round: 1-3: 108; 4: 13; 5: 27; 6: 11; 7: 12; 8: 8; Ransome translations: 2; 9 (Scott Moncrieff): 9; 10 (Ryder 5, Gertrude Bell 1, Levy Nietzsche 15): 21; 11 (Archer's Ibsen): 11; 12 (Magnússon-Morris 3, Strindberg 14): 17; 13 (Saga Library 6, Three Northern Love Stories 1, Björkman 1, Pickthall 1): 9; 14 (Wormeley 41, Vizetelly 16): 57; 15 (Wiener's Tolstoy): 24; 16 (Leland's Heine 8, Whishaw 3): 11; 17 (Koteliansky 10, Marian Fell 3, Seltzer 5, Dole 6): 24; 18 (Ellen Marriage 18, Clara Bell 43, Waring 4): 65; 19 (Teixeira de Mattos 59, Serrano 6, Howitt 2, Duff Gordon 2): 69; 20 (Miall 10, Muir 4, Wraxall 23, Dowson 3): 40; 21 (Machen 1, Ives 18, Hogarth 10, Bernstein 9, Marx Aveling 5, Bain 12): 55; 22 (Safford 23, Wister 14, Allinson 9, Worster 8, Chater 7, De Leon 18): 79; 23 (Upton 35, Colbron 5, Goldberg 9, Roscoe 8, Durand 7, Brooks 6, Lady Wallace 8, Frewer 6, Ensor 6, Ranous 2): 92; 24 (Paul 10, Saunders 8, McCabe 9, Farquharson Sharp 7, Morison 8, White 1, Black 1, Waller 7, Rothwell 5): 56; 25 (thirteen shelves): 71; 26 (pending items and Chekhov): 5; 27 (eleven shelves): 57; 28 (twelve shelves): 41; 29 (seventeen shelves): 51; 30 (seventeen shelves): 56; 31 (twenty-five shelves): 48; 32 (thirty shelves): 66; 33 (thirty-six shelves): 72. **15 of the titles are cross-references to works the repo already holds (the Volsunga Saga became one on 2026-10-10), not new copies.** No uids minted.
Updated 2026-10-02T15:32-05:00. No uids minted anywhere in this lane: every title below awaits your single-writer minting pass. Nothing is converted to unit-id JSON yet (that needs entries in fetch_sources.py, which the relay may not touch).

## Dryden — `pipeline/dryden_shelf.json`
- **21 titles held** (19 clean, 2 raw OCR) from 10 sources: Scott's Works vols 11-17 via Gutenberg + PG 228 + two Internet Archive scans.
- Virgil: aeneid, aeneid-dedication, georgics, eclogues · Ovid: metamorphoses (Garth composite), ovid-metamorphoses (Dryden's own share), ovid-epistles, ovid-art-of-love, ovid-amores · theocritus, lucretius, horace, iliad, juvenal, persius · fables-chaucer, fables-boccaccio, veni-creator · xavier (Bouhours), art-of-painting (Du Fresnoy), history-of-the-league (Maimbourg, raw).
- Pending (wishlist): 1700 Fables first edition (to restore Dryden's order), 1693 Juvenal whole book, 1697 Virgil, 1717 Garth, 1688 Xavier.
- Excluded: "Dryden's Plutarch" (he translated none of the Lives), Polybius/Lucian prefaces, a different John Dryden, duplicates.

## Garnett — `pipeline/garnett_shelf.json`
- **55 titles held** from 62 sources (40 Gutenberg, 22 Internet Archive scans, OCR quality 0.92-0.97): Dostoevsky 13, Tolstoy 5, Chekhov 16, Turgenev 15, Gogol 3, Ostrovsky, Goncharov, Herzen. All first published 1894-1927 (US PD); later printings recorded per title.
- Pending: Gogol's Government Inspector (1926) and Mirgorod (1928): no verified scan found. Poor Folk / Uncle's Dream: no Garnett version found.

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
