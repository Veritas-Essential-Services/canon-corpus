# Merge plan, October 2026: PRs #5 to #10 and the relay branch

Written 2026-10-02 by the Strong's thread (PR #10). Nothing here has been merged
or pushed anywhere. The trial merge below was done on a throwaway local copy of
`main` and thrown away.

## The short version

Merge in this order. Each step has at most a few text conflicts, and all of
them have a mechanical fix (below). On the fully merged tree every test suite
that can run in the cloud passes.

| Step | PR | Branch | What it is | Head tried |
|---|---|---|---|---|
| 1 | #6 | `claude/project-thread-ja8lqz` | upkeep + the Contents-reader title fix | a2d935e |
| 2 | #5 | `claude/project-thread-rcfr2a` | BDB scripture refs resolved to KJV verses | 25fe747 |
| 3 | #9 | `claude/project-thread-xatdhh` | Vulgate, Douay, Brenton + their KJV maps | e7c6dcf |
| 4 | #8 | `claude/project-thread-tskfc3` | whole Greek NT, Hebrew OT text, Apostolic Fathers | 00e8ade |
| 5 | #7 | `claude/project-thread-hxenem` | Perseus / First1KGreek shelf, Thayer's by entry | 1fc2cf7 |
| 6 | #10 | `claude/project-thread-17bo7g` | Strong's as the key for every Hebrew and Greek word | 1753f92 |
| 7 | relay | `claude/armarium-divines` | the four-lane relay's shelves and converters | 605723c |

## Why this order (the dependencies)

- **#5 sits underneath #8, #9 and #10.** Its commits are already inside all
  three. Merge it first and they shrink to their own work.
- **#8 contains #9.** #8's branch merged #9's head (e7c6dcf) to get the
  Septuagint-to-KJV map. So #9 goes before #8. Merging #8 first would drag #9
  in unreviewed.
- **#10 contains #5, #8 (up to 077780f) and #9.** It is stacked on #8. After #8
  merges, change #10's base to `main` on GitHub; its diff then shows only the
  Strong's work.
- **#6 and #7 are independent.** #6 is small and touches the reader, so it goes
  first. #7 goes after the Bible work because its conflicts are all in
  `CLAUDE.md`, the book manifest and one test file, and they are easier to
  settle once.
- **The relay branch is last.** It is 158 new files (shelf lists, converters,
  `overnight/`, `docs/divines-map`) and merged clean at every point. It is
  not a PR yet.

## The trial merge, step by step

Each step merged the branch into the result of the step before.

| Step | Result | Conflicted files |
|---|---|---|
| #6 | clean | none |
| #5 | conflict | `CLAUDE.md` (1 hunk) |
| #9 | conflict | `CLAUDE.md` (1 hunk) |
| #8 | clean | none |
| #7 | conflict | `CLAUDE.md` (2 hunks), `data/books/manifest.json`, `tests/structure_test.py` (2 hunks) |
| #10 | conflict | `data/books/manifest.json` |
| relay | clean | none |

Final tree against `main`: 234 files changed, +195,671 / -699.

### Each conflict and its fix

1. **`CLAUDE.md`, the test-count lines (#5, #9, #7).** Every branch edited the
   same two lines in the Commands block ("NN offline checks", "NN
   identity-layer checks"). Keeping both sides leaves six lines saying four
   different numbers. **Fix:** keep one line each with the measured numbers on
   the merged tree. `structure_test.py` has **183** checks and `wh_uid_test.py`
   has **67**.
2. **`CLAUDE.md`, the Layout section (#7).** #7 and the Bible branches each
   appended new Layout entries at the same spot. **Fix:** keep both. They
   describe different files.
3. **`data/books/manifest.json` (#7).** Both sides added books at the end of
   the same JSON object. **Fix:** merge key by key against the common ancestor.
   This adds #7's 369 new books. It takes #7's version of `aeneid-williams`,
   `iliad-butler` and `odyssey-eng4`, which only #7 changed: it added their
   rights labels. Nothing clashed.
4. **`tests/structure_test.py` (#7).** Both sides appended new test blocks at
   the end. **Fix:** keep both blocks, #7's after the other.
5. **`data/books/manifest.json` (#10).** This conflict comes from history, not
   content. #10 merged #9 and an older #8 separately, and #8 later merged #9
   too. Git then sees two common ancestors and builds a broken base file.
   **Fix:** take the merged tree's manifest unchanged. Checked key by key
   against the older #8 head, #10 changes nothing in it; the only keys that
   differ are the nine Apostolic Fathers books, where #8 is newer.
   **Cleaner fix:** merge #8's head (00e8ade) into #10 before merging #10.
   That leaves one ancestor and no conflict. I tried to do this on #10's
   branch and the session's permission check stopped it, so it is left for
   you or a later session.

## Tests and gates on the merged tree

Passing: 18 test suites, each with 0 failures:

- apostolic_fathers, brenton_versification, hymn_corpus, lemma_bridge
- lemma_spine, lexicon, mnemonicon_pack, nt_corpus, ot_corpus
- proper_names, reader, review, strongs, structure (183)
- versification, vulgate_versification, wh_uid (67), whitaker_tricks

Two suites can't run in the cloud:

- `latin_shelf_uid_test`: it needs the Latin shelf in the vault, so it skips
  and verifies nothing.
- `remint_maxims_test`: it needs the private `wordhoard` repo beside this one.

Gates that pass:

- `build_strongs.py --check`
- `build_versification.py --check`
- `build_nt_corpus.py --check` (mints 0)
- `build_ot_corpus.py --check` (mints 0)
- `rebuild_bible.py --verify`

Gates that can't run here, so **run them on your PC after merging:**

- `build_witnesses.py --check` is THE gate. It needs both KJV builds, and
  Gutenberg is blocked from this session.
- `build_hymn_corpus.py --check` needs the vault.

## Works on more than one branch

The brief said Lane B and #7 both have Thucydides, Plutarch and Greek tragedy.
That is only partly right. Mostly they hold **different translations of the
same work**. Under rule 3c those are extra witnesses, not duplicates, so both
can stay.

**True duplicates** have the same translation on both sides. Keep one copy of
each:

| Work | Translator | In #7 (Perseus) | In the relay (Gutenberg) |
|---|---|---|---|
| Aristophanes, Clouds | W. J. Hickie | yes | yes |
| Caesar, Gallic War | McDevitte & Bohn | yes | yes |
| Cicero, orations and Academics | C. D. Yonge | yes | yes |
| Cicero, letters and On Friendship | E. S. Shuckburgh | yes | yes |
| Epictetus | T. W. Higginson | yes | yes |
| Euripides | E. P. Coleridge; T. A. Buckley | yes | yes |
| Livy | Bohn (Spillan, Edmonds, McDevitte) | yes | yes |
| Lucian | H. W. & F. G. Fowler, vols 1-4 | yes | yes |
| Plautus; Terence | H. T. Riley | yes | yes |
| Polybius | E. S. Shuckburgh | yes | yes |
| Sallust | J. S. Watson | yes | yes |
| Seneca, Apocolocyntosis | W. H. D. Rouse | yes | yes |
| Suetonius | A. Thomson | rev. Reed | rev. Forester |
| Tacitus, Histories | Church & Brodribb | yes | yes |

**Same work, different translation.** Keep both; they are second witnesses.

| Work | In #7 | In the relay |
|---|---|---|
| Thucydides | Crawley | Jowett, Hobbes |
| Plutarch | Perrin | Holland; Stewart & Long; others |
| Sophocles | Jebb | Storr, Murray, Campbell |
| Aeschylus | Smyth | Morshead, Plumptre, Blackie, Buckley, Murray |
| Herodotus | Godley | Macaulay, Rawlinson |
| Xenophon | Brownson, Miller | Dakyns |
| Horace | Smart | Conington |
| Isocrates | Norlin | Freese |
| Euripides | (above) | also Murray, Way |

#7's newest commit (early Christian apocrypha, M. R. James's English) has no
counterpart on the relay branch.

## Decisions that are yours, one line each

**#5**
- None. It only needs merging first.

**#6**
- Accept the Contents-reader fix that stops cutting letters off titles. It can
  move unit ids under rule 3. The id report says 0 ids move in the 36
  committed books (`docs/review/2026-10-02-contents-key-ids.md`).

**#9**
- Swete's LXX: its markup is CC BY-SA. Ingest it or leave it out.
- 106 KJV verses are treated as wanting in Brenton. This is inferred; accept or
  have them checked.
- The rights notes stand as written: the Douay README says "Public Domain",
  and Brenton asks for error reports.

**#8**
1. The 229 MB of verse files: rebuild on demand (the default, keeps 44cb57d)
   or commit them. If you commit them, squash-merge.
2. The Romans doxology sits at KJV Rom 16:25-27.
3. The NT is stored as one folder per book.
4. The 67 Psalm titles are left out of the OT verse rows.
5. The four joined verses: accept the house default.
6. The 1:2 alignments (Ps 13:6, Isa 63:19): accept the house default.
7. The OT is stored as one folder per book.
8. The Apostolic Fathers get no uids minted.
9. The Apostolic Fathers get Strong's numbers by fixed rule.

**#7**
- Pick one copy of each true duplicate above. There is no default; the
  Perseus copies are proofed and carry standard citations.
- The CC BY-SA rights label on Iliad (Butler), Odyssey and Aeneid (Williams).
  Revert 3d3f902 to reject it.
- Tacitus's marginal headings may come from the 1942 reprint. They are kept in
  the apparatus.
- Demosthenes (Vince) is held back until Vince's death date is checked.
- Confirm the exclusions made for copyright: Birds, Livy (Roberts), Celsus,
  Xenophon's minor works, the Moralia, Pausanias, Isocrates vol. 3, and Lucian
  after 1930.
- Thayer's entry ids are provisional.
- 1 Enoch from Swete 1905 via First1KGreek: check whether its markup carries
  the same CC BY-SA as #9's Swete. This is inferred, not checked.

**#10**
- Adopt the 14,197 proposed word uids (`build_strongs.py --adopt`).
- Use the citation form `strongs:G26`, of kind `lexeme`.
- The 101 Greek "Not Used" numbers get no uid.
- The KJV Strong's tags: eBible labels them Public Domain, while CrossWire's
  module says GPL. Decide which. Until you do, everything built from them
  (`kjv-tags`, `kjv-renderings`, the KJV half of the concordance, the
  concordance view) is built locally to `build/strongs/` and was removed from
  the branch's history on 2026-10-02.
- The OSHB OT layer is CC BY. Commit it, or keep building it locally.
- Merge #8's head into #10 first, to avoid conflict 5.
- The Latin key (added after the trial merge): may an index of Lewis & Short's entry keys, taken from Perseus's CC BY-SA text, be committed? Until you say yes, only its manifest is committed; the files build to `build/latin-key/` and were removed from the branch's history on 2026-10-02. It adds no conflicts.

**Relay branch**
- Decide whether it becomes a PR at all, or which lanes do.
- Pick a copy of each duplicate, as listed under #7.
- Delete the committed `_to_delete/` (about 43 MB).

**Across all of them**
- The 427 open review-sheet rows (hymns, John 1) are unchanged by any merge.

## How to repeat the trial

On a fresh clone:

```
git checkout --detach origin/main
git merge --no-ff origin/<branch>   # once per step, in the order above
```

Resolve conflicts as in the "Each conflict and its fix" section, then:

```
python3 pipeline/rebuild_bible.py
```

After that, run each `tests/*_test.py` and the gates.
