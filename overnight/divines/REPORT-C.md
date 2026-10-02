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
