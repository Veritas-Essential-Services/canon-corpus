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

- 2026-10-10T09:03-05:00: Ransome request reached lanes B and C together; B pushed first, C's duplicate dropped. ransome-translations shelf (Gourmont, Old Peter): 0 mismatched.

- 2026-10-10T09:12-05:00: round 9, scott-moncrieff shelf: 9 titles (PG 5, IA 4), 6 pending. --verify --record 0 mismatched.

- 2026-10-10T09:17-05:00: round 10: ryder (5), gertrude-bell (1), levy-nietzsche (15). --verify --record 0 mismatched on all.

- 2026-10-10T09:26-05:00: round 11: archer-ibsen (11 vols). --verify --record 0 mismatched.

- 2026-10-10T09:38-05:00: round 12: morris-magnusson (3), strindberg-english (14). --verify --record 0 mismatched.

- 2026-10-10T09:45-05:00: round 13: Saga Library + TNLS (morris-magnusson, now 10), Björkman series 1 (strindberg-english, now 15), pickthall (1, 1930 override). --verify --record 0 mismatched.

- 2026-10-10T09:52-05:00: fix: mm-volsunga duplicated Lane D's edda-volsunga-morris; now held_in cross-reference. Re-verified 0 mismatched.

- 2026-10-10T10:05-05:00: round 14: wormeley (41), vizetelly (16); id-clash check over all lane C shelves: none. --verify --record 0 mismatched.

- 2026-10-10T10:18-05:00: round 15: wiener-tolstoy (24 vols). --verify --record 0 mismatched.

- 2026-10-10T10:23-05:00: round 16: leland-heine (8), whishaw (3). --verify --record 0 mismatched.

- 2026-10-10T10:28-05:00: round 17: koteliansky (10), marian-fell (3), seltzer (5), dole (6). --verify --record 0 mismatched.

- 2026-10-10T10:41-05:00: round 18: ellen-marriage (18), clara-bell (43), waring (4, one held_in). --verify --record 0 mismatched.

- 2026-10-10T10:53-05:00: round 19: teixeira-de-mattos (59), serrano (6), mary-howitt (2), duff-gordon (2). --verify --record 0 mismatched.

- 2026-10-10T11:00-05:00: round 20: bernard-miall (10), jessie-muir (4), wraxall (23), dowson (3). --verify --record 0 mismatched.

- 2026-10-10T11:08-05:00: round 21: machen-casanova (1), ives (18), cj-hogarth (10), herman-bernstein (9), eleanor-marx-aveling (5), bain-jokai (12). --verify --record 0 mismatched.

- 2026-10-10T11:18-05:00: round 22: safford (23), wister (14), allinson (9), worster (8), chater (7), de-leon (18). --verify --record 0 mismatched.

- 2026-10-10T11:27-05:00: round 23: upton (35), colbron (5), isaac-goldberg (9), thomas-roscoe (8), durand (7), ct-brooks (6), lady-wallace (8), frewer (6), laura-ensor (6), ranous (2). --verify --record 0 mismatched.

- 2026-10-10T11:31-05:00: round 24: eden-cedar-paul (10), bailey-saunders (8), mccabe (9), farquharson-sharp (7, one held_in), mary-morison (8), diana-white (1), robert-black (1), waller (7), rothwell (5). --verify --record 0 mismatched.

- 2026-10-10T11:36-05:00: round 25: markham (7), thomasina-ross (7), hl-williams (6), beatrice-marshall (5), alys-hallard (4), bertha-ness (5), macdowall (5), gillies (5), christina-tyrrell (6), d-anvers (6), livingston (4), barrett-clark (5), lamond (6). --verify --record 0 mismatched.

- 2026-10-10T11:44-05:00: round 26: archer-ibsen vol 12, marian-fell Plays, julius-west (1), george-calderon (2). --verify --record 0 mismatched.

- 2026-10-10T11:50-05:00: round 27: johnes (12), elwes (6, one held_in), fleming (11), mcclure (1), ainslie (6), derbyshire (4), gilbert-cannan (4), lewisohn (4), van-laun (4), eugene-mason (4), eleanor-grove (1). --verify --record 0 mismatched.

- 2026-10-10T11:55-05:00: round 28: mary-loyd (4), krehbiel (4), frances-hoey (4), dulcken (2), prestage (4), dorothy-bussy (4), dziewicki (4), swanwick (3), oxenford (2), monier-williams (2), lalor (4), walter-armstrong (4). --verify --record 0 mismatched.

- 2026-10-10T12:01-05:00: round 29: ww-waters (3), edna-underwood (4), ellen-frothingham (3), boylan (2), holcroft (3), margaret-armour (3), florence-simmonds (3), guerney (3), benecke (3), lowe-porter (3), aldington (3), dora-schmitz (2), welby (3), emilie-jackson (3), metcalfe (3), wollstonecraft (3), bicknell (4). --verify --record 0 mismatched; benecke 8378 flagged (1944 reprint of a 1921 text).

- 2026-10-10T12:14-05:00: round 30: chapman-coleman (5), soissons (4), mccormack (2), georgina-malcolm (4), denis-maccarthy (4), hannibal-lloyd (4), cournos (2), lily-wolffsohn (3), shea-troyer (3), pauline-townsend (3), thomson-weismann (4), ssa-stephenson (3), robson-michaud (3), painter (3), campion (3), friedlaender (3), aline-delano (3). --verify --record 0 mismatched. Flagged late reprints: campion 50015 (1937), friedlaender 15729 (1946). mccormack 25387/36640 pending (PDF only).

- 2026-10-10T12:20-05:00: round 31: zilboorg (2), yarmolinsky (2), katharine-wylde (2), winifred-stephens (2), selver (2), rigg (2), hornblow (2), hanna-larsen (2), flitch (2), glazer (2), bunnett (2), constance-bache (2), hueffer (2), atkinson-lepper (2), cf-atkinson (2), joly (2), byington (2), bealby (2), hazlitt-huc (2), lockhart-diaz (2), crewe-jones (2), greenstreet (1), stirling-bastiat (2), delffs (2), egerton (1). --verify --record 0 mismatched. Flagged late reprint: flitch 14636 (Dover 1954). greenstreet 37157 pending (PDF only); egerton 8387 excluded (duplicate).

- 2026-10-10T12:27-05:00: round 32: elise-lathrop (3), hammer-purgstall (2), nathaniel-greene (3), dunstan (3), de-quincey-walladmor (2), jane-chapman (3), bushby (3), babington (2), meldola (2), jp-richter (2), lord-stanley (3), ziegler (2), fitzwater-wray (2), wenckstern (2), vandam (2), untermann (2), strettell (2), lionel-strachey (2), storer (2), scheffauer (2), pinkerton (2), ongley (2), jessie-lemont (2), hollander (2), gertrude-hall (2), bithell (2), agnetti (2), borthwick (2), kamensky (2), bucknall (2). --verify --record 0 mismatched. Flagged: lord-stanley 38253 (1970 facsimile), storer 42148 (post-1934 printing).

- 2026-10-10T12:36-05:00: round 33: laura-kendall (3), rs-townsend (2), silvanus-thompson (2), surendranath-tagore (2), rabindranath-tagore (2), arthur-symons (2), sumichrast (2), rose-strunsky (2), cw-stork (2), adler-stern (2), steegmann (2), schierbrand (2), schele-de-vere (2), elizabeth-sabine (2), ramsden (2), ts-perry (2), neumann (2), lady-moreton (2), jakowleff-montefiore (2), jepson (2), hjerleid (2), godman (2), selina-gaye (2), freese (2), duncan-forbes (2), fassett (2), de-kay (2), fanny-copeland (2), oliver-colt (2), burnham-maupin (2), hf-brownson (2), wa-bradley (2), bonney (1), se-boggs (2), drezmal (2), cowell (2). --verify --record 0 mismatched. Flagged: lady-moreton 29447 (1935 reprint). cw-stork 78363 is a 1930 first edition (PD 2026).

- 2026-10-10T12:41-05:00: round 34: whiston (5), ganguli (4), mn-dutt (6), saintsbury-heptameron (5), viharilala-mitra (7), smollett-translations (5). --verify --record 0 mismatched. Large translations: Whiston's Josephus, Ganguli's Mahabharata, M. N. Dutt's Ramayana, Saintsbury's Heptameron, Mitra's Yoga-Vasishtha (facsimile flag), Smollett.

- 2026-10-10T12:59-05:00: round 35: rasmus-anderson (8), archer-other (2), borrow-translations (31), adele-seltzer (5). --verify --record 0 mismatched. Gap audit: +24 titles on curtin (8), hapgood (6), wormeley (4), clara-bell (3), levy-nietzsche (2), payne (1); burton Kama Sutra excluded by judgment; adele-seltzer split from seltzer.

- 2026-10-10T13:05-05:00: round 36: claud-field (4), edwin-bjorkman (1), ellie-schleussner (1), helen-zimmern (1), paul-cohn (2), horace-samuel (2). --verify --record 0 mismatched. Audit part 2: +8 titles on vizetelly, de-leon, dole, koteliansky, leland-heine, prestage, morris-magnusson, strindberg-english; 3 duplicates excluded; Gobineau left off by judgment.

- 2026-10-10T13:22-05:00: round 37: gaston-de-vere (10), sutro (4), mg-lewis (5), ab-lindsay (4), rymer-jones (4), hayward-bichat (4), jr-forster (4), brett-feijoo (4), frederic-whyte (3), poulsson-zwilgmeyer (3), eg-martin (3), elizabeth-lee (3), w-johnston (3), houghton-translations (3), helena-frank (3), alexander-ewing (3), sa-eliot (3), frances-douglas (3), brose (1), mary-wilson (2), robert-willis (2), l-williams (2), alice-werner (2), herbert-trench (2), ft-cooper (10), ruth-davis (4), db-stewart (3). --verify --record 0 mismatched. Gap-fill: +4 bowring, +2 symonds. brose: Weyl and Freundlich to _pending (no plain text).

- 2026-10-10T13:29-05:00: round 38: cr-murphy (3), brady-guzman (3), ajw-morrison (4), willcocks (2), ellen-waugh (2), mp-waterman (2), troilius (2), minna-smith (2), leon-simon (2), sedgwick-sand (2), fayette-robinson (2), jb-robertson (2), eg-rich (2), raahauge (2), otte (2), co-reilly (2), mp-nichols (2), w-montgomery (2), monkshood (2), chalmers-mitchell (2), katherine-miller (2). --verify --record 0 mismatched. Gap-fill: +1 strindberg-english (Lucky Pehr). Flags: About Zionism 1930 printing; Cosmos vol. 1 a 1997 facsimile of 1858.

- 2026-10-10T13:40-05:00: round 39: ac-middleton (1), lg-meyer (2), ella-mcmahon (2), maver (2), ca-manning (1), maidment (2), krh-mackenzie (2), marjorie-laurie (2), mrs-john-lane (2), la-monte (2), kingsbury (2), ch-kerr (2), kenrick (2), cb-jordan (2), jelliffe (2), jv-huntington (1), john-howard (2), fa-holt (2), nk-hills (2), emily-hill (2), wf-harvey (2), robert-harrison (2), henry-harland (2), gorfinkle (1), home-gordon (2), mrs-gillespie (2), je-fries (2), fraprie (2), cecil-fairfax (2), george-eliot-translations (2), amelia-edwards (2), jd-duff (2), drillien (2), rb-douglas (2), fe-cox (2), mrs-l-burke (2), burette (2), neil-buchanan (2), eleanor-brooks (2), van-wyck-brooks (1), pf-bicknell (2), ernest-bell (2), baines (2), katharine-babbitt (2), ingeborg-andersen (2), mh-allies (2), abby-alger (2), ager (2), tk-abbott (2), h-parker (2), robert-parke (2), alexander-muir (2). --verify --record 0 mismatched. giles: Art of War extra files excluded. Dropped rw-lawson (no plain text). Flags: Silberer Dover 1971; Swedenborg 1988 printing; Mendoza 1970 facsimile.

- 2026-10-10T13:53-05:00: round 40: singles-medieval-epic (27), singles-ideas (26), singles-literature (40). --verify --record 0 mismatched. New single-translation shelf form (_surname_by_slug per title). Flags: Hypnerotomachia 1969 facsimile; Underdogs post-1952 printing. _pending: Hilbert, Dedekind, Ramus.

- 2026-10-10T14:21-05:00: round 41: singles-history-travel (44), singles-science-craft (39), singles-ideas-2 (41). --verify --record 0 mismatched. Flags: De Re Metallica Dover 1950; Durkheim 1964 impression. _pending: six PDF-only physics/maths books.

- 2026-10-10T14:40-05:00: round 42: singles-continental-fiction (64), singles-verse-drama-tales (32). --verify --record 0 mismatched. No late printings found in the year check. Left for owners: Lagerlöf's From a Swedish Homestead (lagerlof, Lane D) and two Tudor Erasmus translations (erasmus shelf).

- 2026-10-10T14:51-05:00: round 43: singles-fiction-2 (67), singles-plays-poetry-2 (39). --verify --record 0 mismatched. No late printings found. Left for owners: Spyri's New Year's Carol (spyri, Lane D). Excluded: The Jade Flute (translator unnamed).

- 2026-10-10T14:52-05:00: round 44: singles-fiction-3 (68). --verify --record 0 mismatched. Three 1930 translations in _pending (Emil and the Detectives, Confessions of Zeno, Akutagawa) await the 1930 override. Hutton's Táin carries a 1948 presentation inscription (not a printing). Left for owners: Lagerlöf's Liliecrona's Home.

- 2026-10-10T14:55-05:00: round 45: singles-history-2 (72). --verify --record 0 mismatched. No late printings found.

- 2026-10-10T15:02-05:00: round 46: singles-ideas-3 (48), singles-science-2 (71). --verify --record 0 mismatched. No late printings found. _pending: Newton's Principia (Motte) and Menabrea/Lovelace, HTML-only at Gutenberg.

- 2026-10-10T15:03-05:00: round 47: singles-arts-miscellany (51). --verify --record 0 mismatched. Flag: Rimsky-Korsakov's Principles of Orchestration keyed from the 1964 Dover reprint. _pending: Van Gogh letters (HTML only). Excluded: Buzz a Buzz (no plain text).

- 2026-10-10T15:12-05:00: round 48: singles-fiction-4 (99). --verify --record 0 mismatched. Flag: Maurois's General Bramble keyed from a 1931 reprint. Excluded: Karl May's Travel Tales (COPYRIGHTED PG header), My First Battle (2009 translation). Left for owner: Lisbeth Longfrock (poulsson, Lane D).

- 2026-10-10T15:15-05:00: round 49: singles-nonfiction-2 (84). --verify --record 0 mismatched. Facsimiles flagged: Rapin/Creech (ARS 1947), Gregorovius's Lucretia Borgia (Blom 1968), Tosi/Galliard (Reeves 1967). Excluded: Nicole/Cunningham (a 1950 translation) and Fernández Bolívar (modern).

- 2026-10-17T16:47-05:00: round 51: period scans for 9 HTML-only pending titles (singles-science-2 +2, singles-science-craft +6, singles-arts-miscellany +1). --verify --record 0 mismatched. adler newton-principia is the Latin 1687, not Motte (flagged in DIGEST-C).

- 2026-10-17T16:54-05:00: round 52: singles-remainder (26). --verify --record 0 mismatched. Single-translator list closed.

- 2026-10-17T16:58-05:00: round 53: maude +8 (Anna Karenina, Essays and Letters, Sevastopol, Confession, Hadji Murad, First Step, Pamphlets). --verify --record 0 mismatched.

- 2026-10-17T17:02-05:00: round 54: scott-moncrieff +2 (The Captive, Lauzun). --verify --record 0 mismatched.

- 2026-10-17T17:09-05:00: round 55: broadway-library (5). --verify --record 0 mismatched. Also +1 aldington (Voltaire and Frederick), +1 emilie-jackson (Mercier).

- 2026-10-17T17:12-05:00: round 56: broadway-travellers (9). --verify --record 0 mismatched.

- 2026-10-17T17:16-05:00: round 57: broadway-translations (4). --verify --record 0 mismatched. Also +1 broadway-library (Lespinasse).

- 2026-10-17T17:19-05:00: round 58: eileen-power (2). --verify --record 0 mismatched. Also +1 broadway-translations (Guibert), +1 storer (Poggio).

- 2026-10-17T17:24-05:00: round 59: history-of-civilization (8). --verify --record 0 mismatched.

- 2026-10-17T17:36-05:00: round 60: wisdom-of-the-east (10). --verify --record 0 mismatched. Wisdom of the East, East Asian volumes.

- 2026-10-17T17:46-05:00: round 61: wisdom-of-the-east +16 (26). --verify --record 0 mismatched. Wisdom of the East, Indian/Persian/Arabic/Hebrew/Egyptian volumes.

- 2026-10-17T17:53-05:00: round 62: sacred-books-of-the-east (11). --verify --record 0 mismatched. Sacred Books of the East, Buddhist and Jain volumes.

- 2026-10-17T17:58-05:00: round 63: sacred-books-of-the-east +16 (27). --verify --record 0 mismatched. SBE Zoroastrian and Hindu law volumes.

- 2026-10-17T18:06-05:00: round 64: sacred-books-of-the-east +11 (38), legge +6 (9). --verify --record 0 mismatched. SBE Vedic/Vedanta volumes; Legge's SBE.

- 2026-10-17T18:14-05:00: round 65: pali-buddhist-translations (17). --verify --record 0 mismatched. Pali canon in English (Jataka, Dialogues, Psalms, Mahavamsa, Buddhist Legends, Warren).

- 2026-10-17T18:21-05:00: round 66: harvard-oriental-series (9). --verify --record 0 mismatched. Vikrama's Adventures pending (Hindi OCR); Kiratarjuniya excluded (German).

- 2026-10-17T18:27-05:00: round 67: east-asian-classics (9). --verify --record 0 mismatched.

- 2026-10-17T18:30-05:00: round 68: oriental-classics (13). --verify --record 0 mismatched. occ-tiruvacagam title_weak (OCR ç as 9), checked by eye.

- 2026-10-17T18:34-05:00: round 69: mughal-histories (8). --verify --record 0 mismatched.

- 2026-10-17T18:41-05:00: round 70: india-historians (12). --verify --record 0 mismatched. ih-ferishta-4 identity override (OCR 'HRKiCiS' for Briggs), checked by eye.

- 2026-10-17T18:45-05:00: round 71: arabic-classics (10). --verify --record 0 mismatched. arc-hariri-1 identity override (OCR 'CHEKEEY' for Chenery), checked by eye.

- 2026-10-17T18:52-05:00: round 72: budge (11). --verify --record 0 mismatched. bdg-alexander-syriac rights override (undated record; title page 1889).

- 2026-10-17T18:55-05:00: round 73: babylonian-assyrian (11). --verify --record 0 mismatched. bab-gilgamish-thompson rights override (undated record; title page 1928).

- 2026-10-17T18:59-05:00: round 74: egyptian-texts (10). --verify --record 0 mismatched.

- 2026-10-17T19:03-05:00: round 75: legge +8 (17). --verify --record 0 mismatched. Legge's Chinese Classics, first edition 1861-72.

- 2026-10-17T19:06-05:00: round 76: japanese-classics (6). --verify --record 0 mismatched.

- 2026-10-17T19:13-05:00: round 77: bidpai (4). --verify --record 0 mismatched. bid-anwar-i-suhaili-wollaston identity override (OCR 'WOLLASTUN').

- 2026-10-17T19:15-05:00: round 78: edwin-arnold +4 (5). --verify --record 0 mismatched. Indian Poetry is an undated impression (flagged).

- 2026-10-17T19:25-05:00: round 79: griffith +6 (8), whinfield +3 (4), nicholson +3 (5). --verify --record 0 mismatched.

- 2026-10-17T19:30-05:00: round 80: persian-poets (9). --verify --record 0 mismatched. pers-bustan-clarke identity override (OCR 'WILBERTORCE').

- 2026-10-17T19:36-05:00: round 81: payne +8 (12). --verify --record 0 mismatched. Six identity overrides (blackletter or unreadable title pages).

- 2026-10-17T19:39-05:00: round 82: east-asian-classics +2 (11). --verify --record 0 mismatched.

- 2026-10-17T19:43-05:00: round 83: indian-literature (8). --verify --record 0 mismatched.

- 2026-10-17T19:47-05:00: round 84: gibb (6). --verify --record 0 mismatched. gibb-ottoman-poems identity override (OCR).

- 2026-10-17T19:51-05:00: round 85: arabic-classics +3 (13). --verify --record 0 mismatched.

- 2026-10-17T19:56-05:00: round 86: rodkinson (18). --verify --record 0 mismatched.

- 2026-10-17T19:59-05:00: round 87: hebrew-classics (4). --verify --record 0 mismatched.

- 2026-10-17T20:03-05:00: round 88: norse-sagas (7). --verify --record 0 mismatched.

- 2026-10-17T20:08-05:00: round 89: scandinavian-classics (5). --verify --record 0 mismatched.

- 2026-10-17T20:11-05:00: round 90: gap-fills cw-stork (+2), hollander (+1), edwin-bjorkman (+1). --verify --record 0 mismatched.

- 2026-10-17T20:15-05:00: round 91: gap-fill scandinavian-classics (+3, now 8). --verify --record 0 mismatched.

- 2026-10-17T20:35-05:00: round 92: italian-classics (15). --verify --record 0 mismatched.
- 2026-10-17T20:35-05:00: round 92 gap-fills: hoole (+1), aldington (+1), bowring (+1). --verify --record 0 mismatched. Identity overrides: itc-carducci-holland, hoole-metastasio-1/2.

- 2026-10-17T20:41-05:00: round 93: hispanic-classics (10). --verify --record 0 mismatched. serrano gap-fill +3.

- 2026-10-17T20:55-05:00: round 94: german-classics (20). --verify --record 0 mismatched.

- 2026-10-17T21:01-05:00: round 95: german-literature (8). --verify --record 0 mismatched. ellen-frothingham +0 (Sappho to _pending, 1972 facsimile); upton +0 (Immensee excluded, name not in scan).

- 2026-10-17T21:14-05:00: round 96: french-classics (13), johnes +2 (14). --verify --record 0 mismatched. johnes +2 (Froissart 1848, 2 vols); only the two new _checks recorded, older check dates kept.

- 2026-10-17T21:24-05:00: round 97: wormeley +16 (61), ives +1 (19). --verify --record 0 mismatched; only new _checks recorded, older check dates kept.

- 2026-10-17T21:29-05:00: round 98: wormeley +11 (72), incl. PG 43283 moved out of _excluded after reading its title page. --verify --record 0 mismatched; only new _checks recorded.

- 2026-10-17T21:37-05:00: round 99: michelet-in-english (11). --verify --record 0 mismatched. mic-history-of-france-vol-1/2 identity overrides (OCR 'G, II SMITH', 'G, H, SMITH').

- 2026-10-17T21:43-05:00: round 100: french-classics +7 (20). --verify --record 0 mismatched; only new _checks recorded. Butler's Select Essays dropped (undated).

- 2026-10-17T21:47-05:00: round 101: durand +3 (10), french-classics +1 (21). --verify --record 0 mismatched; only new _checks recorded.

- 2026-10-17T21:51-05:00: round 102: lusiads-in-english (8). --verify --record 0 mismatched.

- 2026-10-17T21:58-05:00: round 103: hispanic-classics +4 (14). Pinto (cu31924077183410) to _pending: Cornell 1996 replacement photocopy. Audit: budge, burton, edwin-arnold, egyptian-texts, cw-stork each moved one title to _pending for the same reason. --verify --record 0 mismatched.

- 2026-10-17T22:07-05:00: round 104: lady-wallace +11 (now 19). --verify --record 0 mismatched. lwa-nohl-life-of-mozart-vol-2 identity override (OCR 'WALLACK').

- 2026-10-17T22:17-05:00: round 105: italian-classics +17 (now 32). --verify --record 0 mismatched. Identity overrides: Guicciardini vols 2, 3, 5 (Goddard OCR), Magenis vol 1.

- 2026-10-17T22:22-05:00: round 106: ww-waters +4 (now 7), benecke +1 (now 4), steegmann +1 (now 3). --verify --record 0 mismatched.

- 2026-10-17T22:26-05:00: round 107: singles-nonfiction-2 +2 (Girondists II-III, identity overrides for Ryde OCR), singles-literature +1 (Huard's Vigny), italian-classics +1 (Garrow's Niccolini). --verify --record 0 mismatched.

- 2026-10-17T22:32-05:00: round 108: german-poets-in-english (9). --verify --record 0 mismatched. New shelf german-poets-in-english (gpe-).

- 2026-10-17T22:37-05:00: round 109: pinkerton +3, seltzer +1, singles-fiction-3 +2 (Garshin; Voynich identity override). Coxwell's Kriloff to _pending (undated scan). --verify --record 0 mismatched.

- 2026-10-17T22:44-05:00: round 110: new loew (4); bowring +1, singles-plays-poetry-2 +1, singles-fiction-3 +2. Identity overrides: Bowring Petofi (OCR), Ashes vol 1 (no title page). --verify --record 0 mismatched.

- 2026-10-17T22:51-05:00: round 111: hispanic-classics +5 (Espinel x2, Gracian x2, Guevara), singles-nonfiction-2 +1 (Krasinski). Identity override: Saldkeld (letter-spaced OCR). --verify --record 0 mismatched.

- 2026-10-17T22:59-05:00: round 112: selver +7, singles-fiction-3 +1 (Makropoulos), singles-arts-miscellany +1 (How a Play). Czechoslovak anthology to _pending (undated). --verify --record 0 mismatched.

- 2026-10-17T23:05-05:00: round 113: french-classics +4 (Ellis Rose x3, Gundry Manon), ts-perry +2 (Princess of Cleves). Identity overrides: Gundry (OCR), Cleves vol 2 (no title page). --verify --record 0 mismatched.

- 2026-10-17T23:11-05:00: round 114: french-classics +3 (Way's Fabliaux), italian-classics +2 (Tassoni: Ozell, Atkinson). --verify --record 0 mismatched.

- 2026-10-17T23:17-05:00: round 115: broadway-translations +1 (Simplicissimus), singles-fiction-3 +1 (Kleist). --verify --record 0 mismatched.
