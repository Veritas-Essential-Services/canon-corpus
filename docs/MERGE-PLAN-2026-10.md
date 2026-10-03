# Merge plan, October 2026: PRs #5 to #10 and the relay branch

Written 2026-10-02 by the Strong's thread (PR #10), revised 2026-10-03 after
#7 merged #10. Nothing has been merged. The trial merges below were done on a
throwaway local copy of `main` and thrown away.

**What changed on 2026-10-03:** #7's branch merged #10 (at 232ae6d), so **#10
must now go before #7**. Merging #7 first would bring in an old copy of #10
unreviewed, including files #10 has since taken out for rights reasons
(PR #10 body). Merged in the order below, those files stay out of `main`
(checked on the trial tree).

## The short version

Merge in this order. Each step has at most a few text conflicts, and all of
them have a mechanical fix (below). On the fully merged tree every test suite
that can run in the cloud passes.

| Step | PR | Branch | What it is | Head tried |
|---|---|---|---|---|
| 1 | #6 | `claude/project-thread-ja8lqz` | upkeep + the Contents-reader title fix | 356ed3a |
| 2 | #5 | `claude/project-thread-rcfr2a` | BDB scripture refs resolved to KJV verses | 25fe747 |
| 3 | #9 | `claude/project-thread-xatdhh` | Vulgate, Douay, Brenton + their KJV maps | db5f5a9 |
| 4 | #8 | `claude/project-thread-tskfc3` | whole Greek NT, Hebrew OT text, Apostolic Fathers | f42632b |
| 4b | — | — | **after #8: rerun `python3 pipeline/build_parallel_index.py` and commit the result.** It fills the Greek NT column; #9's build reads #8's one-folder-per-book layout. | — |
| 5 | #10 | `claude/project-thread-17bo7g` | Strong's as the key for every Hebrew and Greek word (**squash-merge**) | 97dc4c0 |
| 6 | #7 | `claude/project-thread-hxenem` | Perseus / First1KGreek shelf, Thayer's by entry (**squash-merge**) | 0281061 |
| 7 | #11 | `claude/project-thread-y4capw` | Archive.org/CCEL pickups: Lightfoot's English Apostolic Fathers, Charles, Tudor Bibles, Schaff (**squash-merge**) | ff633ad |
| 8 | relay | `claude/armarium-divines` | the four-lane relay's shelves and converters | 4aa2994 |

Heads move. Before merging, check each branch's head against this table; if
one moved, repeat the trial (last section).

## Why this order (the dependencies)

- **#5 sits underneath #8, #9 and #10.** Its commits are already inside all
  three. Merge it first and they shrink to their own work.
- **#8 contains an older #9.** #8's branch merged #9 (e7c6dcf) for the
  Septuagint-to-KJV map; #9 has moved on since. So #9 goes before #8.
- **#10 contains #5, an older #8 (077780f) and an older #9.** It is stacked on
  #8. After #8 merges, change #10's base to `main` on GitHub; its diff then
  shows only the Strong's work.
- **#7 contains an older #10** (merged at 232ae6d, for its tooling). So #10
  goes before #7.
- **#11 contains #7, #8 and #9** (it merges schaff-fathers, which carries
  #7), so it goes after all three. Its trial row below was taken at 0b231ed,
  before it merged #7 and the Tudor Bibles; repeat the trial before merging.
- **#6 is independent.** It is small and touches the reader, so it goes first.
  It now carries two commits that need your ruling (below).
- **The relay branch is last.** It is 158 new files (shelf lists, converters,
  `overnight/`, `docs/divines-map`) and merged clean at every point. It is
  not a PR yet.

## The trial merge, step by step

Each step merged the branch into the result of the step before.

Trial of 2026-10-03 01:00 UTC, at the heads in the table above:

| Step | Result | Conflicted files |
|---|---|---|
| #6 | clean | none |
| #5 | conflict | `CLAUDE.md` |
| #9 | conflict | `CLAUDE.md` |
| #8 | conflict | `CLAUDE.md` |
| #10 | conflict | `CLAUDE.md`, `data/books/manifest.json` (fix 5) |
| #7 | conflict | `CLAUDE.md`, `tests/structure_test.py` (fix 4) |
| #11 | conflict | `CLAUDE.md`, `data/books/manifest.json` (fix 3), `pipeline/fetch_sources.py` |
| relay | clean | none |

Final tree against `main`: 420 files changed, +249,677 / -701. The
`CLAUDE.md` conflicts are all fixes 1 and 2. #11's `fetch_sources.py` conflict
is new: #11 and the branches before it each added source dicts at the same
place, so keep both sides. A full merge rehearsal is running on
`claude/merge-rehearsal` (the build-check thread), which will report anything
this quick trial missed. The 2026-10-02
trial (#7 before #10) also conflicted in `tests/structure_test.py` and the
book manifest at #7; with #10 first, #7's only conflict is `CLAUDE.md`. Fixes
3 and 4 below are kept in case #7 moves again.

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
   Rechecked 2026-10-03 key by key: every entry #10 has is identical to #8's
   head (f42632b), and #8 has more (Philo, Josephus, the Apostolic Fathers,
   TAGNT variants). So when merging #10, **keep `main`'s side** of this file
   (`git checkout --ours data/books/manifest.json`). Merging #8's head into
   #10 first does not avoid the conflict (a reviewer tried it).

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
- Beowulf (PG 16328) is J. Lesslie Hall's translation, not Gummere's (4819839).
- PG 228 is Dryden's Aeneid only (356ed3a).

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
- **Squash-merge #10, #7 and #11** (or purge first). #11 carries #7, so it
  carries the same old commits. The files #10 took out for
  rights reasons are still in both branches' earlier commits (b35ad03,
  39ffc1e, 4620d48, 692ad17). An ordinary merge would carry those commits,
  and the files with them, into `main`'s history; a squash merge does not.
  The alternative is to purge both branches' history first (force-push).
- The KJV Strong's tags: eBible labels them Public Domain, while CrossWire's
  module says GPL. Decide which. Until you do, everything built from them
  (`kjv-tags`, `kjv-renderings`, the KJV half of the concordance, the
  concordance view) is built locally to `build/strongs/` and was removed from
  the branch's history on 2026-10-02.
- The OSHB OT layer is CC BY. Commit it, or keep building it locally.
- The Latin key (added after the trial merge): may an index of Lewis & Short's entry keys, taken from Perseus's CC BY-SA text, be committed? Until you say yes, only its manifest is committed; the files build to `build/latin-key/` and were removed from the branch's history on 2026-10-02. It adds no conflicts.

**#11**
- The #11 review's Lightfoot fix has landed (ff633ad): all 9 rows now carry
  the house token `rights.license: public-domain`, CCEL's rights lines moved
  unchanged to `rights.note`. The same commit restores the manifest's indent=1.
- Lightfoot: should `redistribute_whole` be true? The text is PD; CCEL claims
  copyright on its prepared file.
- #8's `build_apostolic_fathers.py` still lists Lightfoot as pending; that fix
  belongs in #8 (or a follow-up after #11).

**Across #9 and #11**
- Does the "no SWORD rips" rule cover the scrollmapper English Bibles and the
  Douay?

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
