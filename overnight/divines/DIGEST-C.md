# Lane C — Translator shelves: digest (read first)
Totals 2026-10-10T11:18-05:00: 88 shelves, 672 titles. By round: 1-3: 108; 4: 13; 5: 27; 6: 11; 7: 12; 8: 8; Ransome translations: 2; 9 (Scott Moncrieff): 9; 10 (Ryder 5, Gertrude Bell 1, Levy Nietzsche 15): 21; 11 (Archer's Ibsen): 11; 12 (Magnússon-Morris 3, Strindberg 14): 17; 13 (Saga Library 6, Three Northern Love Stories 1, Björkman 1, Pickthall 1): 9; 14 (Wormeley 41, Vizetelly 16): 57; 15 (Wiener's Tolstoy): 24; 16 (Leland's Heine 8, Whishaw 3): 11; 17 (Koteliansky 10, Marian Fell 3, Seltzer 5, Dole 6): 24; 18 (Ellen Marriage 18, Clara Bell 43, Waring 4): 65; 19 (Teixeira de Mattos 59, Serrano 6, Howitt 2, Duff Gordon 2): 69; 20 (Miall 10, Muir 4, Wraxall 23, Dowson 3): 40; 21 (Machen 1, Ives 18, Hogarth 10, Bernstein 9, Marx Aveling 5, Bain 12): 55; 22 (Safford 23, Wister 14, Allinson 9, Worster 8, Chater 7, De Leon 18): 79. **13 of the titles are cross-references to works the repo already holds (the Volsunga Saga became one on 2026-10-10), not new copies.** No uids minted.
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
