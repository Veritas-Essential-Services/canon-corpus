# Lane C (Translator shelves) — append-only log

## 2026-10-02T15:17-05:00 — shelf-dryden: done-with-defects
- Vault unreachable from the cloud; worked from the repo only (CLAUDE.md asks for vault notes).
- pipeline/fetch_shelf.py already existed (lane B); used as is. New: pipeline/split_shelf_titles.py (cuts titles from multi-work volumes by exact heading-line markers; writes only gitignored data/corpus/<shelf>/titles/).
- Sources: PG 228 + Scott's Works vols 11-17 (PG 44050, 54361, 47383, 64337, 47641, 14947, 76952); IA ovidsmetamorphos00ovid (Garth 1826), historyofleague00maim (1684). 10 fetched, 0 failed, ~7.5 MB. No COPYRIGHTED markers.
- 21 titles cut, 0 failed: aeneid, aeneid-dedication, georgics, eclogues, metamorphoses (Garth), ovid-metamorphoses, ovid-epistles, ovid-art-of-love, ovid-amores, theocritus, lucretius, horace, iliad, juvenal, persius, fables-chaucer, fables-boccaccio, veni-creator, xavier, art-of-painting, history-of-the-league.
- OCR check (share of tokens found in a clean Scott vocabulary): Garth 1826 0.949, League 1684 0.783 (long s), Scott vol 13 clean baseline 0.938.
- tests/structure_test.py: 64 passed, 0 failed (run after; only new files added, none imported by the tests).
- Not converted to unit-id JSON (needs fetch_sources.py entry: forbidden in the relay). Awaiting uid minting: all 21 titles.
- Excluded: "Dryden's Plutarch" (Dryden translated none of the Lives), Polybius/Lucian prefaces, PG 24901 (wrong Dryden), Gilfillan and PG 7490 duplicates.
- Lane B pointers dryden-aeneid / -georgics / -eclogues / -metamorphoses now resolve.

## 2026-10-02T15:30-05:00 — shelf-garnett: done-with-defects
- Shelf pipeline/garnett_shelf.json: 60 sources (40 Gutenberg, 20 Internet Archive), 40.3 MB, 0 failed. All 40 PG headers: Translator = Constance Garnett; no COPYRIGHTED markers.
- 52 titles cut (split_shelf_titles.py now joins multi-volume titles: Sportsman's Sketches, Virgin Soil, Dead Souls, Herzen's My Past and Thoughts 6 vols). Dostoevsky 12, Tolstoy 5, Chekhov 16 (13 Tales vols, letters, 2 plays vols), Turgenev 15, Gogol 1, Ostrovsky 1, Goncharov 1, Herzen 1.
- Dating: every title first published 1894-1927 (US PD, pre-1931). Later printings scanned are recorded per title as scan_edition (War and Peace IA-dated 1910, House of the Dead 1923, plays 1923 Phoenix reprint). Undatable Carlton House War and Peace excluded.
- IA OCR quality (tokens in a clean-text vocabulary): 0.921 (plays vol 1) to 0.974 (Insulted and Injured); clean PG baseline 0.962.
- Excluded: PG 600/6536 (duplicate of Notes inside White Nights), PG 4602 (older transcription), PG 1944 (no translator named in file), non-Garnett PG versions (Martin, Hogarth), IA 1911 House of the Dead (not Garnett), DLI scans (txt 404).
- Pending: Gogol vols 3-6, Poor Folk / Uncle's Dream, Notes from Underground as its own cut title, 1904 War and Peace first printing.
- tests/structure_test.py: 64 passed, 0 failed.

## 2026-10-02T15:31-05:00 — overflow-garnett-gaps: done-with-defects
- +2 Gogol (IA overcoatothersto0000niko, 1923; IA Dikanka, Knopf 1926), both title pages name Garnett. Fetched 2/2.
- +1 cut title: garnett-notes-from-underground (from inside garnett-white-nights; overlap flagged so minting gives one uid per passage).
- Not found: Government Inspector (1926), Mirgorod (1928). IA mirgorodgogol is a Russian edition (excluded). Poor Folk / Uncle's Dream: no Garnett version located; the 1915 IA copies are Hogarth's (excluded).
- Garnett shelf now 62 sources, 55 titles, all cut.

## 2026-10-02T15:32-05:00 — queue empty: finding (§5d) and session end
- Finding — two witnesses of Dryden's Aeneid differ systematically. PG 228 vs Scott vols 14-15, verse lines aligned (difflib): 13,802 vs 13,824 lines; 8,255 identical after normalising case and punctuation; 5,127 differ in spelling only (same word count); 340 differ in length; 64 inserted/deleted. Top differences: th'→the (309), thro'→through (193), heav'n→heaven (143), ev'ry→every (94), pow'r→power (63), -'d→-ed (fix'd, rais'd, call'd ...). PG 228 keeps Dryden's metrical elisions (the 1697 habit); Scott expands them. So they are two witnesses of one text, not duplicates — choosing the reading_of_record is Adam's call (PG 228 for the poet's metre, Scott for the notes and Dedication).
- Map audit: Dryden map rows match the 21 titles in dryden_shelf.json; Garnett section is generated from garnett_shelf.json. Lane B's six Dryden pointers all resolve.
- All shelf identifiers resolved at fetch time this session (72 sources, 0 failed).
- Next worker of lane C: nothing queued. Real leftovers are in DIGEST-C.md (Gogol Government Inspector + Mirgorod scans; Dryden 1700 Fables order). Do not refetch: everything is on the branch as shelves; corpus files are not.

## 2026-10-02T15:43-05:00 — round 2 (coordinator relay): five translator shelves
- Pope and Chapman NOT taken: lane B's running `homer` item shelves them translator-per-work. Plutarch skipped (another thread).
- shelf-cary: done. 4 titles (Dante 3 canticles, Pindar 1833 raw OCR).
- shelf-longfellow: done. 4 titles (Dante 3 canticles + Translations section cut from PG 1365, ending before his Virgil/Ovid pieces).
- shelf-florio: done-with-defects. Montaigne 1603 via the 1906 Gibbings reprint (6 vols raw OCR) + 1620 Decameron (attribution only).
- shelf-burton: done. Arabian Nights 10 vols, Supplemental Nights 6, Lusiads, Camoens Lyricks. Explicit-content titles (Catullus, Kama Sutra, Pentamerone) pending, Adam's call.
- shelf-maude: done-with-defects. 10 titles; PG 26472 404 and PG 26660 front-matter-only worked around; dating evidence recorded per title.
- 52 sources fetched in all, 0 failed after fixes; 24 titles cut, 0 failed. structure_test: 64 passed.

## 2026-10-02T15:48-05:00 — round 3 (lane C's own additions under the keep-going relay): seven shelves
- cotton, ormsby, urquhart-motteux, fitzgerald, taylor, lane, guest: 12 sources fetched (0 failed after one title fix), 9 titles cut, 0 failed. Translator lines verified in every PG header; IA scans checked for the translator's name on the title page.
- Note for lanes: lane B's newer fetch_shelf.py title-word check fails on accented titles (Rubáiyát); worked around in the shelf title, no change to the fetcher.
- structure_test: 64 passed.

## 2026-10-02T15:48-05:00 — session end: lock released. Queue empty again (14 shelves, 109 titles). Next worker: more translator shelves only with a clear source; see DIGEST-C pending lists (Gogol plays/Mirgorod, Maude Anna Karenina, Cary's Birds, Burton's held-back titles await Adam).

## 2026-10-02T17:27-05:00 — review-fixes (from the review thread, relayed by the coordinator)
- 10 titles marked `held_in` and cross-referenced (adler ×7, fetch_sources ×3 incl. Cary/8800); their duplicate sources dropped. split_shelf_titles.py reports them "held-elsewhere" and never re-cuts them.
- Translator field on every title; `_name_words` translator-only; `_verified` evidence per source in every shelf (PG Translator: line + COPYRIGHTED marker; IA translator-named + front-matter years).
- Late printings replaced: Raw Youth, Gambler, Friend of the Family, Honest Thief, Chekhov Plays 1. Garnett War and Peace moved to pending (no pre-1931 scan). Maude UK note and Chekhov dates fixed.
- fetch_shelf --verify: 0 mismatched on all 14 shelves. split: 108 titles, 0 not cut. structure_test: 64 passed.

## 2026-10-02T17:37-05:00 — lane A surname check adopted
- `_surname` (translator surnames, whole words) added to all 14 lane C shelves; `fetch_shelf.py --verify --record` run on each: `_checks` committed, 0 mismatched, 0 rights flags.

## 2026-10-02T19:41-05:00 — round 4: seven translator shelves (rossetti, fairfax, rose, shelton, norton, payne, carlyle)
- 18 sources fetched, 0 failed (Rose's Gutenberg 615 placed by hand: the cache URL 404s, see `_manual_fetch`). 13 titles cut, 0 failed. `--verify --record`: 0 mismatched, 0 rights flags. Front-matter scan: 0 post-1930 years.
- The coordinator's suggested Jowett, Church & Brodribb, Butler and Lang-Leaf-Myers are lane B/D's already; none taken.
- Note for lane B: fetch_shelf.py could fall back to https://www.gutenberg.org/ebooks/<n>.txt.utf-8 when cache/epub 404s (PG 615).

## 2026-10-02T19:47-05:00 — round 5: seven translator shelves (curtin, hapgood, legge, giles, waley, hoole, harington)
- 31 sources fetched (one IA HTTP 500 retried), 0 failed. 27 titles cut, 0 failed. `--verify --record`: 0 mismatched, 0 rights flags; one identity override (Hoole vol. 2, split OCR name), one title_weak (Harington).
- Defects: Harington 1591 OCR (0.66), Hoole 1803 long s (0.82). Rights notes: Waley UK to end-2036, Lionel Giles UK to end-2028 (US PD).

## 2026-10-02T19:53-05:00 — round 6: eight translator shelves (muller, edwin-arnold, griffith, rodwell, sale, palmer, whinfield, nicholson)
- 14 sources fetched, 0 failed after one identity override (Nicholson Divani, OCR "Nichqlson"). 11 titles cut, 0 failed. `--verify --record`: 0 mismatched, 0 rights flags. Front-matter scan over rounds 5-6: one flag, a 2019 digitisation credit (examined, recorded).

## 2026-10-02T19:56-05:00 — second review round
- 11 shelves: full-name `_surname`; Shelton vol. 2 title page recorded; Palmer part I fetched (part II had been fetched twice). `--verify --record` re-run on 13 shelves: 0 mismatched, 0 rights flags.

## 2026-10-02T21:49-05:00 — split_shelf_titles.py stale-cut fix (coordinator finding)
- A title that fails (missing marker, missing source, too short) or is held elsewhere now has any earlier titles/<slug>.txt (and .tmp) deleted; the report records "stale_removed". Good cuts were already temp-file + rename.
- New test: `python3 tests/split_shelf_titles_test.py` (10 checks, offline, runs the real script on a temp copy). Fails 5 of 10 on the old code, passes 10 on the fix. All lane C shelves re-cut clean; structure_test 64 passed. (CLAUDE.md's command list is not a lane file: the new test command is for Adam to add.)

## 2026-10-02T21:52-05:00 — lane A gate fix (815a082) re-verified
- `fetch_shelf.py --verify --record` re-run on all 36 lane C shelves under the fail-closed rights gate, per-miss overrides and max(years) date gate: 0 mismatched, 0 rights flags; the 6 identity overrides still cover only the miss each names. sturluson and lang are not lane C shelves.

## 2026-10-03T00:51-05:00 — round 7: seven shelves (southey, coleridge, bowring, anster, hayward, wicksteed, mangan) + lane A guard
- 15 sources, 0 failed after fixes (one IA mislabel, Blackie as Anster, replaced; three recorded identity overrides). 12 titles cut. `--verify --record` across all 43 lane C shelves under e1ef08b: 0 mismatched, 0 rights flags. Coordinator's suggested list was entirely held already (lanes B, C, D).

## 2026-10-03T01:20-05:00 — split_shelf_titles.py --help (reviewer finding)
- `-h`/`--help` now print the docstring and exit 0 instead of being read as a shelf name (FileNotFoundError). Two checks added: tests/split_shelf_titles_test.py 12 passed.

## 2026-10-03T05:42-05:00 — round 8: four shelves (symonds, blackie, theodore-martin, hearn)
- 7 Gutenberg sources, 0 failed; 7 titles cut + 1 cross-reference (Blackie's Aeschylus → lane B aeschylus). `--verify --record`: 0 mismatched, 0 rights flags.

- 2026-10-03 ~07:00 CDT: name-audit relay done. Full-name `_surname` on 11 shelves (maude, hearn, southey, symonds, blackie, rossetti, coleridge, garnett, griffith, nicholson, muller); --verify --record 0 mismatched, 0 rights flags on all.
