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
