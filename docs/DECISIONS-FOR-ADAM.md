# Decisions for Adam (updated 2026-10-10)

This is every question the weekend's work left open. They are ordered by what they unblock:

- **Part 1** is what the merges wait on, in the order of `docs/MERGE-PLAN-2026-10.md` (PR #10).
- **Part 2** is what the uid-minting pass waits on.
- **Part 3** is rulings on rights and scope that can wait.

Each line ends with a recommendation. To take every recommendation, answer "yes to all". Otherwise name the items you'd change. ★ marks a merge blocker.

**Where things stand:**
- Nothing has merged since 2026-10-03. PRs #5 to #16 are all open drafts.
- The relay stopped at 12:43 UTC that day.
- One branch has moved since the merge trial: #7, on 2026-10-08.

Items were renumbered on 2026-10-10. Earlier numbers don't carry over.

## Part 1. Before the merges

| # | Decision | Recommend | PR |
|---|---|---|---|
| 1 ★ | Merge order: #6, #5, #9, #8, then rerun `build_parallel_index.py`, then #10, #7, #11, the relay, and #14 to #16 | **Follow the plan.** Repeat its trial merge first, because #7 has moved. | #10 |
| 2 ★ | The Contents-reader fix: titles were losing a trailing c, i, l, v or x. It moves 0 committed ids and recovers about 68 relay headings | **Merge it with #6.** | #6 |
| 3 | PG 228's slug is `virgil-eclogues`, but the file is the Aeneid only | **Rename it now.** No ids exist yet. | #6 |
| 4 | Beowulf PG 16328 is Hall's translation, not Gummere's | **Accept the label and keep the slug `beowulf`.** | #6 |
| 5 ★ | Bible JSONL shards: commit 17 MB of them, or rebuild them from pinned sources? | **Rebuild.** First make `nt_corpus_test` and `ot_corpus_test` skip, not fail, when the shards are absent. | #8, #11 |
| 6 | Bible alignment defaults: the Romans doxology goes at 16:25-27, the 67 psalm titles are left out, and joined Hebrew verses become one witness | **Accept.** | #8 |
| 7 ★ | Adopt the 14,197 Strong's word uids, cited as `strongs:G26`, with no uid for the 101 "Not Used" numbers | **Yes.** | #10 |
| 8 | Commit the KJV Strong's tags? eBible.org says they are public domain; CrossWire says GPL. Commit OSHB's Hebrew tags (CC BY)? | **Build both locally only**, until the GPL question is settled. | #10 |
| 9 | Commit the Lewis & Short index (keys and facts only, no definitions)? | **Yes.** | #10 |
| 10 ★ | Squash-merge #10, #7 and #11, or rewrite their history first? | **Squash.** Each PR keeps its own commit ledger. | #10, #7, #11 |
| 11 ★ | CC BY-SA markup over public-domain text (Perseus, First1KGreek, CSEL, CrossWire's Wycliffe) | **Don't serve it whole for now.** Once Armarium is public, serve the plain text taken out of the markup. | #7, #11 |
| 12 | The Perseus rights block is not copied into the committed manifest, so a reader can't see the limit there | **Fix `structure_texts.py` before #7 merges.** | #7 |
| 13 | Tyndale has two sources: #9 (7,888 verses, from scrollmapper) and #11 (13,852 verses) | **Use #11's**, after checking that it isn't converted from SWORD. | #9, #11 |
| 14 | #9's English Bibles and Douay come from scrollmapper JSON, which is converted from SWORD modules, and the relay's rules ban SWORD | **Swap to a non-SWORD source where one exists.** Otherwise keep, with the provenance recorded. | #9 |
| 15 ★ | CCEL asks for non-commercial use of its prepared texts (198 lane A items, Schaff's Fathers, #15) | **Quote, cite and link only, as now.** Write to CCEL only if Armarium ever charges. | #11, #15, relay |
| 16 | Lightfoot's Apostolic Fathers (1891): set `redistribute_whole` to true? | **True**, if the source states no licence. | #11 |
| 17 | Charles's Additions to Esther: flagged non-free outside the US, on a death date nobody has checked | **Accept for the US.** | #11 |
| 18 | Honour textusreceptusbibles.com's reuse terms for the Tudor Bibles? | **Yes.** | #11 |
| 19 | Wycliffe: collation letters are glued to words | **Strip them with a converter rule.** | #11 |
| 20 | Remove the committed `_to_delete/` folder (43 MB) | **Yes.** History keeps a copy. | main |
| 21 | Keep `docs/MERGE-REHEARSAL.md` on main? | **Drop it** after the merges. | #12 |

## Part 2. Before the minting pass

| # | Decision | Recommend | Where |
|---|---|---|---|
| 22 ★ | When to mint uids for relay slugs (lane D alone has 1,078 slugs on 234 shelves) | **One attended pass**, after the merges and items 2 and 23. Raw OCR volumes get no uids until they are converted. | relay |
| 23 ★ | Move the per-book heading rules (`chapre`, `levels`) from the shelf files into `structure_texts.py` | **Yes.** They decide unit ids. | relay |
| 24 | One text held in two editions or volumes (Dryden and Garth, Garnett, Hunt's Grimm, Malory, Bunyan, Horace and others) | **Keep both as witnesses, one uid per passage.** | relay |
| 25 | Westcott, Lightfoot and Alford commentaries are on #11 (converted) and on lane A (raw OCR) | **#11's text is the reading of record.** | #11, relay |
| 26 | Classical works are on #7 (Perseus) and on lane B (Gutenberg) | **Keep both.** Perseus is the reading of record. | #7, relay |
| 27 | Texts keyed from late reprints: CCEL's Owen (Banner 1965-68), Barnes (Baker 1949), Wesley's Journal, Finney (1944), Torrey (1974), Schaff's Creeds III (1977), MacDonald, and undated CCEL items | **Keep, flagged.** Where an early copy is held (Owen has Goold), make it the reading of record. | relay, #15, #16 |
| 28 | Post-1930 reprints of unrevised translations: Loebs, Ross's Aristotle, Aretaeus (1972) | **Keep the whole class**, and take Freese's *Rhetoric* and Duff's Silius, which are held now. | relay |
| 29 | Undated books dated by a bound-in list (Pott and Wright's Martial, list to 1926) | **Take a book when its list ends before 1930.** | relay |
| 30 | Reconcile lane D's `aesop` with the earlier fables work | **Yes, in the minting pass.** | relay |
| 31 | Fetcher fix: add common-word surnames, and flag CCEL sources with no year or a reprint | **Apply it and re-sweep the CCEL shelves.** | relay |
| 32 | Wrong translator labels on `adler_shelf.json` (Thucydides, Tacitus, Epictetus, Lucretius, Herodotus and others) | **Fix the labels in one upkeep commit.** | relay |

## Part 3. Rulings that can wait

| # | Decision | Recommend | Where |
|---|---|---|---|
| 33 | Public domain in the US only: Murray, the 1913-30 Loebs, MacKenna, Garnett, the Maudes, Radin's Ginzberg vols 3-4, Jewett's Tibet tales and others | **Keep**, noted `pd_scope: US`. | relay |
| 34 | The translator isn't proven by the file: the Andersen rows, the Whitman Pinocchio, the Persian fairy tales, and lane B's unchecked rows | **Accept where a collation or title-page reading is recorded. Hold the rest.** | relay |
| 35 | Six Loebs held because the scans are revised printings or carry later reading lists | **Keep them held.** | relay |
| 36 | *Seneca his Tenne Tragedies* (1927) carries T. S. Eliot's introduction | **Use the 1887 printing.** | relay |
| 37 | Perseus's modernised spelling of Godley's Herodotus and Smyth's Aeschylus | **Keep as witnesses, flagged.** | relay |
| 38 | Greek-facing Loebs fail the OCR bar because their Greek pages score as unclean | **Measure the English pages only.** | relay |
| 39 | Borderline single titles: Babbitt's Moralia 1-2, the stage *Daddy Long-Legs*, *Uncle Wiggily* (1939) | **Yes, yes, hold.** | relay |
| 40 | Shelves the lanes added on their own (lane A rounds 2-14, lane C rounds 3-8, lane D's batches, #14) | **Accept by default.** Veto by deleting a shelf file. | relay, #14 |
| 41 | Veto points: Newman's Catholic works, Finney, Bushnell, the Mathers' witchcraft works (left out), Herbert's *Temple* (verse) | **Keep Newman, Finney and Bushnell, flagged. Leave the Mathers out. Keep Herbert, and also offer him to the hymn side.** | relay |
| 42 | Names and authors: `dryden-metamorphoses` is Garth's book; Mrs. Lang gets her own shelf; Rutherford comes off Bonar's shelf; `lang-devil-dancers` goes to its real author; *The Indian Fairy Book* is filed under Mathews; Theal's printed title, which contains a slur, stays in citations | **Yes to all of these.** | relay |
| 43 | Dryden's Aeneid: which copy is the reading of record? | **PG 228**, with Scott's as a witness. | relay |
| 44 | Widen lane D: Kipling, Hawthorne's novels, Chesterton 1929-30 and more | **Yes to those three; the rest later.** | relay |
| 45 | The Concise Matthew Henry; *An Exhortation to Peace* (doubtful Bunyan) | **Keep both, flagged.** List the *Exhortation* as attributed. | relay |
| 46 | Eight items the identity gate refused; Palgrave's *Fairchild Family*; *The Little Savage* with its "R. B. J." introduction | **Leave them out until someone reads the title pages.** | relay |
| 47 | The Press: is the master text the first edition or a 19th-century one? | **The first edition**, with spelling modernised by rule only in the export. | #15 |
| 48 | The Press: five Reformation Heritage titles are unidentified, and *A Perfect Redeemer* is only inferred | **Leave them out until a title page confirms each.** | #15 |
| 49 | Delitzsch: which Isaiah translation to use (not shelved yet)? How to number the Psalms cross-references? | **The 1890 Isaiah. Record the Psalms references as printed, unresolved.** | #11 |
| 50 | Cross-references: the fathers' Old Testament links are provisional until #7's are fixed | **Accept as is**, and rerun after the fix. | #16 |
| 51 | Schaff follow-ups (OCR of ANF 10, tables for 8 refused works) | **Later.** | #11 |

## Review work only you can do

- **Review sheets.** There are 427 unanswered rows in five sheets on `main` (`python3 pipeline/review.py status`).
- **PR #11.** It also waits on its Charles OCR flags and a Coverdale Psalter sheet.
