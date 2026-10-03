# Lane C — Translator shelves: digest (read first)
Totals 2026-10-03T05:42-05:00: 47 shelves, 179 titles (rounds 1-3: 108; round 4: 13; round 5: 27; round 6: 11; round 7: 12; round 8: 8 — Symonds 3, Blackie 2, Theodore Martin 1, Hearn 2). **11 of them are cross-references to works the repo already holds, not new copies.** No uids minted.
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
