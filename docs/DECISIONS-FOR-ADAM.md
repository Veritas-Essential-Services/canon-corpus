# Decisions for Adam (2026-10-03)

Every open question from the relay digests (`overnight/divines/DIGEST-A..D.md` on
`claude/armarium-divines`) and the open draft PRs (#4 to #16), merged into one
list. Where several sources ask the same thing, it appears once and the
**Where** column names them all. Each line gives the options and a
recommendation. ★ marks the ones that block a merge or the minting pass.

The sources were last read at 07:42 UTC on 2026-10-03 (relay head `b8e46fd`). The lanes keep writing, so
check the digests for anything newer. Items added after the first pass are numbered from 42, so earlier numbers stay the same.

## Rights and licences

| # | Decision | Options | Recommend | Where |
|---|---|---|---|---|
| 1 ★ | CCEL asks that its prepared editions be used non-commercially. This covers 198 items on lane A's shelves and Schaff's Fathers. | (a) serve whole, (b) quote, cite and link only: `redistribute_whole: false`, as now, (c) write to CCEL | **(b)** now, which is the same line as STEPBible. Ask CCEL (c) only if Armarium ever charges. | DIGEST-A; #11 Schaff; #15; CLAUDE.md rule 6 |
| 2 ★ | CC BY-SA 4.0 markup over public-domain text: Perseus (132 on lane B, 300 in #7, and the Iliad, Odyssey and Aeneid labels), First1KGreek, CSEL, and CrossWire's Wycliffe | (a) serve whole with credit and share-alike, (b) not whole: `redistribute_whole: false`, as now, (c) serve plain text taken out of the markup | **(b)** until Armarium is public, then **(c)**, the usual reading of what is free. Keep #7's revertible commit `3d3f902`. | DIGEST-B; #7 s.3, s.12; #11 Wycliffe |
| 3 | US-only public domain: Murray's Greek plays and Rhesus, Humphries, Fyfe, Lindsay, Rouse, Firebaugh, the 1913-30 Loebs, MacKenna, Garnett, the Maudes, the Oxford Aristotle | keep / drop | **Keep**, with a `pd_scope: US` note. The house is in the US. | DIGEST-B, DIGEST-C; #7 |
| 4 | Charles's Additions to Esther are flagged non-free outside the US, on an unchecked death date (Gregg, 1961) | verify the date / accept / drop | **Accept for the US.** Verify the date before any non-US use. | #11 |
| 5 | Six Loeb volumes held because their scans are revised printings or carry later reading lists (Rolfe's Suetonius 1, Williams's Cicero 3, Nixon's Plautus 3, Butler's Quintilian 1, Miller's Metamorphoses 1, Wright's Julian 1) | release / keep held / write a converter rule that cuts the added matter | **Keep held.** Find pre-1931 scans for the two revised volumes. Release the four only once a cut rule exists. | DIGEST-B |
| 6 | *Seneca his Tenne Tragedies* (1927) carries T. S. Eliot's introduction | take it without the introduction / use the 1581 or 1887 printing / drop | **The 1887 printing**: same translation, no Eliot. | DIGEST-B |
| 7 | English Bibles and the Douay come from scrollmapper's JSON, which is converted from SWORD modules, and the relay's own rules ban SWORD rips | keep / swap where a non-SWORD source exists | **Swap where one exists** (eBible.org, for example). Otherwise keep, with the provenance recorded. | #9; #11 Wycliffe |
| 8 | Commit the KJV Strong's tags? (eBible.org says PD; CrossWire's `kjv.conf` says GPL) | commit / build locally only | **Build locally only** until the GPL line is settled. | #10 decision 4 |
| 9 | Commit OSHB's Hebrew word tags (CC BY 4.0)? | commit / build locally | **Build locally**, the same rule as the STEPBible lexicons. | #10 decision 5 |
| 10 | Commit the Lewis & Short index (keys, ids and opening-line facts only, no definitions)? | yes / no | **Yes.** It holds facts, not CC BY-SA prose. | #10 decision 6 |
| 11 | Honour textusreceptusbibles.com's reuse terms for the Tudor Bibles? | yes / no | **Yes.** It costs nothing. | #11 |
| 12 | Lightfoot's Apostolic Fathers: set `redistribute_whole` to true? | true / pending | **True**, if the source states no licence over the 1891 text. | #11; #8 |
| 13 | Translator not proven by the file: five Andersen rows, Heimskringla (shown to be Laing and Anderson by collation), the Whitman Pinocchio, lane B's `_translator_unchecked` rows, and Lane C's Friend of the Family imprint | one rule for all | **Accept where a collation or title-page reading is recorded. Hold where there is none** (the Andersens and the Pinocchio). | DIGEST-B, DIGEST-C, DIGEST-D 9, 12 |
| 14 | Borderline single titles: Babbitt's Moralia 1-2 (1927-28), Webster's stage *Daddy Long-Legs* (1922), Garis's *Uncle Wiggily's Story Book* (1921 and 1939) | yes / no each | **Yes, yes, hold.** The 1939 printing may add new matter. | DIGEST-B; DIGEST-D 13, 14 |
| 42 | CCEL texts keyed from late reprints, not first printings: Barnes's NT Notes (Baker 1949), 26 Owen titles (Banner 1965-68; *Glory of Christ* is also modernised), Wesley's Journal (Moody 1951), Lightfoot's Apostolic Fathers (Baker 1956), Calvin's *Relics* (2008), four MacDonald titles | keep / swap the reading of record | **Keep, flagged.** Where an early IA or PG copy is held (Owen has Goold), make it the reading of record and keep CCEL as a witness. | DIGEST-A; DIGEST-D 17; #15 |
| 43 | Post-1930 reprint impressions marked "reprinted", not "revised" (Ross's Aristotle vols 2 and 9, Bennett's Horace, several Cicero Loebs) | one rule: keep / hold | **Keep.** A reprint of an unrevised text is the same edition. | DIGEST-B |
| 44 | Perseus texts modernised under CC BY-SA (Godley's Herodotus, Smyth's Aeschylus) | keep as witnesses / drop | **Keep as witnesses, flagged**, under #2's line. | DIGEST-B |
| 45 | Jewett's *Wonder Tales from Tibet* (PG 66443, UK status unclear); the Persian fairy tales (PG 24473, no translator named) | keep / hold | **Keep Jewett under #3. Hold the Persian tales under #13.** | DIGEST-D 15 |

## Identity, ids and minting

| # | Decision | Options | Recommend | Where |
|---|---|---|---|---|
| 15 ★ | The minting pass for relay slugs (lane D alone now has 926 slugs on 163 shelves) | when, and do raw IA volumes get uids? | **One attended pass after the merges and after #17 and #18.** Raw OCR volumes get **no uids** until converted. | DIGEST-A, B, D 1 |
| 16 ★ | Adopt the 14,197 Strong's word uids, citation `strongs:G26` (kind `lexeme`), and no uid for the 101 "Not Used" numbers | yes / no | **Yes** to all three. `--adopt` refuses on any collision. | #10 decisions 1-3 |
| 17 ★ | The Contents-reader fix (titles losing a trailing c, i, l, v or x) | merge #6 / leave | **Merge #6 before any relay minting.** It moves 0 committed ids and recovers about 68 relay headings. | #6 s.2; DIGEST-D 2 |
| 18 ★ | Move the per-book heading rules (`chapre`, `levels` and the rest) into `structure_texts.py` before minting? | yes / keep in the shelves | **Yes.** They decide unit ids (CLAUDE.md rule 2). | DIGEST-D 6; DIGEST-C 4 |
| 19 | One text held in two volumes or editions: Dryden and Garth, Garnett's *Notes* inside *White Nights*, the 1884 Hunt Grimm, Malory's Strachey edition, Petrovitch and Mijatovich, Horace PG 14020 and Smart, Bunyan's CCEL pieces and PG 3613, AUDIT-D s.1 | keep both as witnesses under one uid / drop one | **Keep both, one uid per passage** (CLAUDE.md 3c). Drop only the 1884 Hunt if it adds nothing you want beyond Lang's introduction. | DIGEST-B, C 2-3, D 10, 11; DIGEST-A |
| 20 | Dryden's Aeneid reading of record: PG 228 (Dryden's elisions) or Scott (expanded spellings, with the Dedication) | PG 228 / Scott | **PG 228**, with Scott as the second witness. | DIGEST-C 1 |
| 21 | Name `dryden-metamorphoses` as Garth's book, with Dryden's own share as the Dryden title | yes / no | **Yes.** | DIGEST-C 2 |
| 22 | PG 228's slug is `virgil-eclogues`, but the file is the Aeneid only | rename now / keep | **Rename before it's built.** No ids exist yet. | #6 s.5; DIGEST-C |
| 23 | Beowulf PG 16328 is Hall, not Gummere, and lane D also shelved it as `beowulf-hall` | accept the Hall label and keep one slug | **Accept the label. Keep `beowulf`; lane D points to it under `_held`.** | #6 s.4; #13 |
| 24 | Wrong labels on `adler_shelf.json`: Thucydides, Tacitus, Epictetus, Lucretius, Herodotus, Plato, Marcus, Politics (Ellis), Rabelais (Motteux), and `odyssey-eng4` (a Power and Nagy revision) | fix in one upkeep commit / leave | **Fix**, labels only. Lane B already fetched the right translations. | DIGEST-B 1-2; DIGEST-C |
| 25 | Bible alignment defaults: the Romans doxology goes to 16:25-27, the 67 psalm titles are left out, joined Hebrew verses become one witness | accept / change | **Accept.** | #8 |
| 26 | Tyndale has two sources: #9's scrollmapper (7,888 verses) and #11's biblesupersearch (13,852 verses) | #9 / #11 | **#11's fuller text**, after checking its source isn't SWORD-derived (#7). Keep `tyndale:Luke.17.36` and `Rev.21.26` reachable or retire them on purpose. | MERGE-REHEARSAL; #11 |
| 27 | Wycliffe collation letters glued to words | a strip rule / leave | **A rule**, so the edition stays clean (rule 2). | #11 |
| 28 | Classical works on both #7 (Perseus) and lane B (Gutenberg) | pick one per translation / keep both | **Keep both as witnesses.** Perseus is the reading of record because its citations are built in. | #7 s.7 |
| 46 | Westcott, Lightfoot and Alford commentaries held twice: raw OCR on lane A, converted text in #11 | which is the reading of record | **#11's converted text**, with lane A's scan as a witness. | DIGEST-A; #11 |
| 47 | Delitzsch's Psalms cross-references: follow the volume's own (Hebrew) numbering, or map to KJV? | volume / KJV | **Record them as the volume states**, unresolved, like BDB, until a versification map exists. | #11 |
| 48 | Delitzsch's Isaiah: which English translation is the reader text, the 1890 4th edition or Martin's 1867? | 1890 / 1867 | **1890**, the author's last revision, with 1867 as a witness. | #11 |
| 49 | The Press's master text: a 19th-century edition (nearer modern spelling, but OCR) or the hand-keyed first edition (accurate, 17th-century spelling) | 19th c. / first edition | **The first edition as master**, with spelling modernised by rule only in the export, so the source stays exact. | #15 |
| 50 | The Press's Reformation Heritage titles: *A Perfect Redeemer* traced to Perkins's *True Gain* by inference only; five titles unidentified (Holy Meditation, Special Providence, A Blessed Hope, Prizing Public Worship, Advancing Christian Unity) | confirm / leave out | **Leave out until a title page confirms each.** | #15 |

## Repo and merges

| # | Decision | Options | Recommend | Where |
|---|---|---|---|---|
| 29 ★ | Bible JSONL shards: commit 17 MB, or rebuild from pinned sources? | commit / rebuild | **Rebuild**, but first make `nt_corpus_test` and `ot_corpus_test` skip the shards, not fail, on a fresh clone. They fail today. | #8; #11 review |
| 30 ★ | Squash-merge #10, #7 and #11, or force-push to purge history first | squash / purge | **Squash.** The per-acquisition ledger stays on each PR. | #10 decision 7; #7 |
| 31 ★ | Merge order | the plan / other | **Follow `docs/MERGE-PLAN-2026-10.md`**: #6, #5, #9, #8, #10, #7, #11, then the relay. Settle #26 before #11. | #10; #12 |
| 32 | Keep `docs/MERGE-REHEARSAL.md` on main? | keep / drop | **Drop it** once the merges are done. | #12 |
| 33 | Remove the committed `_to_delete/` folder (43 MB of partial downloads and a stale `index.lock`) | yes / no | **Yes.** History keeps a copy. | this thread |
| 51 | PR #4 is a draft that duplicates the merged #3 | close / keep | **Close it.** | #4 |

## Scope and shelves

| # | Decision | Options | Recommend | Where |
|---|---|---|---|---|
| 34 | Shelves the lanes added on their own, for your veto (lane A rounds 2-11, lane C rounds 3-6, lane D's batches) | accept all / veto some | **Accept by default.** Veto by deleting a shelf file and its map rows. | DIGEST-A, C, D |
| 35 | Widen lane D: more Kipling, Hawthorne's novels, Chesterton 1929-30, Stevenson's Swanston edition, other Aesops, more Baum, Wilde, Ruskin and Dickens, Lofting first printings | yes / no each | **Yes to Kipling, Hawthorne and Chesterton 1929-30. The rest later.** | DIGEST-D 3, 8 |
| 36 | Give Mrs. Lang her own shelf; move the Rutherford editions off Andrew Bonar's shelf | yes / no | **Yes to both**, so the author is right. | DIGEST-D 5; DIGEST-A |
| 37 | Concise Matthew Henry (unknown abridger and date); *An Exhortation to Peace and Unity* (doubtful Bunyan) | keep / drop | **Keep both, flagged.** Move the *Exhortation* to `attributed`. | DIGEST-A |
| 38 | Eight items refused by the identity gate (six on lane A, two Ryle tracts) | look at the title pages / leave out | **Leave out until someone looks.** | DIGEST-A |
| 39 | Greek-facing Loebs held back because their Greek OCR is junk | keep the line / take them | **Keep the line.** | DIGEST-B |
| 40 | Reconcile lane D's `aesop` with the earlier fables work before minting | yes | **Yes**, as part of #15. | DIGEST-D 4 |
| 41 | Schaff follow-ups: OCR ANF 10, tables for the 8 refused works, English work books copying their text, Seventh Carthage at 83/87 | now / later | **Later.** None of them blocks the merge. | #11 |
| 52 | Lane A's veto points: Newman's Catholic-period works; the Mathers' witchcraft works (*Wonders of the Invisible World*, *Cases of Conscience*, held); Herbert's *Temple* (verse: here or with the hymns?) | keep / drop each | **Keep Newman and the Mathers as history, flagged. Herbert stays here and is also offered to the hymn side.** | DIGEST-A |
| 53 | `lang-devil-dancers` is held because Lang is not its author | move to the right author / drop | **Move it** to its author's shelf. | DIGEST-D 16 |
| 54 | New shelves from another thread: #14 (88 shelves, 269 Reformation and Scottish volumes, 418 MB) | accept / veto some | **Accept by default**, under #34. Run `shelf_overlaps.py` on it before merging. | #14 |
| 55 | The Bible cross-reference layer: the fathers' Old Testament links stay provisional until #7's OT links are fixed, and 122,369 single-scan Treasury references stay out | accept / wait | **Accept as is.** Rerun the fathers' half after #7's fix. | #16 |

## Review work only you can do

- **Review sheets:** 427 rows across five sheets on `main`, all unanswered (`python3 pipeline/review.py status`). Also on the waiting list: the Charles OCR flags (#11) and a Coverdale Psalter sheet (#11).
