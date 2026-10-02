# Lane C — Translator shelves: digest (read first)
Totals 2026-10-02T15:43-05:00: 7 shelves, 100 titles (Dryden 21, Garnett 55, Cary 4, Longfellow 4, Florio 2, Burton 4, Maude 10). No uids minted.
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
- 1923 printings scanned for War and Peace (scan IA-dated 1910), House of the Dead, Honest Thief and the plays (their text is her translation; the printing date is recorded).

## Shelves added after the first queue (vetoable — Adam's call)
Added 2026-10-02T15:33-05:00 at the coordinator's relay ("keep going, more translator shelves"): Cary (Dante), Longfellow (Dante and others), Florio (Montaigne), Burton (Arabian Nights), the Maudes (Tolstoy, PD editions only). **Not taken: Pope and Chapman (Homer)** — lane B's running `homer` item already shelves them translator-per-work, and the relay forbids taking another lane's titles. Plutarch skipped (another thread has it). Veto any of these and the shelf file plus its map rows can simply be deleted; nothing was minted.

### What those five shelves hold (each vetoable on its own; delete the shelf file and its map rows)
- **Cary:** Inferno, Purgatorio, Paradiso (Gutenberg), Pindar 1833 (raw OCR).
- **Longfellow:** the three canticles, plus his Translations section (Manrique, Spanish, German, Scandinavian, Beowulf passage, French, Michelangelo, Portuguese). His Virgil and Ovid pieces were left for lane B.
- **Florio:** Montaigne's Essayes 1603, using the 1906 reprint (6 volumes of raw OCR, Elizabethan spelling); the 1620 Decameron (anonymous; the Florio attribution is a scholarly one).
- **Burton:** the Arabian Nights (10 vols), Supplemental Nights (6), the Lusiads, and the Camoens Lyricks. **Your call:** Catullus, Kama Sutra and Pentamerone are public domain but explicit, so they are listed and not fetched.
- **Maude:** War and Peace, Resurrection, the Cossacks, Father Sergius, Master and Man, What Men Live By, the six Plays, What Is Art?, The Devil, Three Days in the Village. **Your call:** five of these files print no edition year, so they rest on Gutenberg's US clearance (published before 1931).
