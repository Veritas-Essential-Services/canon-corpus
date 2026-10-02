# Lane C — Translator shelves: digest (read first)
Totals 2026-10-02T17:27-05:00: 14 shelves, 108 titles (Dryden 21, Garnett 54, Cary 4, Longfellow 4, Florio 2, Burton 4, Maude 10, Cotton 1, Ormsby 1, Urquhart-Motteux 2, FitzGerald 2, Taylor 2, Lane 1, Guest 1). **10 of them are cross-references to works the repo already holds, not new copies** (see Review fixes). No uids minted.
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
