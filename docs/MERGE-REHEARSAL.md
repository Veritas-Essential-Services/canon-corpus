---
model_log:
  - 2026-10-03 claude-opus-5-5 drafted
fable_review: pending
---
# Merge rehearsal: the open drafts, in merge-plan order (2026-10-03)

**What this is.** A report from merging every open draft onto `main` in the
planned order on a scratch tree, running the test suites after each merge, to
find conflicts and breakage *before* anything lands on `main`. The scratch
tree itself was not kept on GitHub (it held every draft at once); this file is
the record. Once the real merges are done, this report can be deleted.

**Base:** `main` @ `97b7b5e`. **Heads as fetched** (a branch that moved after
this may behave differently):

| order | PR | head | merge | tests after |
|---|---|---|---|---|
| 1 | #6 upkeep, Contents-reader fix | `356ed3a` | clean | green |
| 2 | #5 BDB -> KJV map | `25fe747` | conflict: CLAUDE.md | green |
| 3 | #9 Vulgate, Douay, Brenton, English Bibles | `a85df25` | conflict: CLAUDE.md | green |
| 4 | #8 whole Bible, Apostolic Fathers, Josephus, Philo | `f42632b` | clean | green (once the NT/OT pins were fetched) |
| 5 | #10 Strong's as the word key | `29c55c8` | conflict: data/books/manifest.json | green |
| 6 | #7 Thayer's, Perseus, fathers, catenae | `232ae6d` | conflict: CLAUDE.md, **plus a silent duplicate key** (problem 1) | green |
| 7 | #11 Lightfoot, Charles, Tudor Bibles, Schaff | `0b231ed` | conflict: fetch_sources.py, manifest.json | green |
| 8 | claude/armarium-divines | `beff42f` | clean | green |

"Green" here means every `tests/*.py` exits 0 (25 to 32 suites, depending on
the step). `latin_shelf_uid_test` and `remint_maxims_test` skip because the
private Latin shelf and wordhoard aren't in the cloud box. That isn't caused
by any merge.

## Problems found

### 1. The Josephus *Life* has two builders, and git doubled its manifest entry without saying so (#7 and #8)

#7 adds `josephus-life-whiston` to `PERSEUS` in `fetch_sources.py`, so
`structure_texts.py` builds it as a generic Perseus book (`format: "tei"`).
#8 builds the same slug in `build_josephus.py` (`format: "tei-perseus"`,
aligned to Niese). Merging #7 after #8 **reported no conflict in
`manifest.json`**, but the merged file held the key `josephus-life-whiston`
**twice**. Python's `json` silently keeps the last one, which is why every
test still passed. The #11 resolution below rewrote the manifest from parsed
JSON, and that removed the duplicate, keeping #8's entry.
`tests/json_duplicate_keys_test.py` now fails on any committed JSON that
repeats a key, so a merge like this one can't pass silently again.

What's still open: on a full `fetch_sources.py` + `structure_texts.py` run,
#7's generic converter will rebuild that slug and overwrite #8's entry. One
pipeline has to own the slug. My guess, not checked: drop it from `PERSEUS`,
because `build_josephus.py` is the aligned build.

### 2. `build_parallel_index.py --check` crashes: it reads a file the NT re-layout removed (#9 and #11, from #8's layout)

`build_parallel_index.py` (added on #9's line) opens
`data/nt/witnesses.jsonl`. Commit `3969ff0` ("Greek NT: the whole New
Testament, one folder per book", on #8's line) moved the NT into
`data/nt/<Book>/`, and that file is gone. On the merged tree, **and on #11's
own head**, the gate fails with:

    FileNotFoundError: .../data/nt/witnesses.jsonl

`tests/parallel_index_test.py` still passes, so only the gate catches it.
The parallel index needs to read the per-book layout.

### 3. Stale Apostolic Fathers entries on #10 and #7 (resolved here, nothing to do if merged in order)

#10 and #7 carry an older build of the nine `*-lake` entries
(`scripture_refs` 239 for 1 Clement, from `077780f`). #8 and #11 carry the
newer one (268, from `00e8ade`, scripture refs resolved). I kept the newer
one. `build_apostolic_fathers.py --check` passes on the result.

### 4. CLAUDE.md's command list conflicts on every PR

Every PR edits the same few lines of the Commands block: each adds its own
commands and changes the `structure_test.py` count. I resolved each one by
keeping both sides' new commands. The count now reads 204, which is what
the merged tree actually runs. It had drifted from 64 through 68, 69, 95 and
191 across the branches. Whoever does the real merges should expect to fix
this block by hand each time.

### 5. #11's Lightfoot source and #9's KJVA source were added at the same spot in fetch_sources.py

Both are new, independent blocks, so the fix is to keep both. #11's patch,
applied on top of the merged file, puts `LIGHTFOOT` and `fetch_lightfoot()`
right after `fetch_kjva()`, plus its `--list` line. The file parses and
`fetch_sources.py --list` runs.

## Gates on the fully merged tree

Passing: lemma_spine, nt_corpus (mint 0), ot_corpus (mint 0), nt_variants,
apostolic_fathers, josephus, philo, versification, vulgate_versification,
brenton_versification, english_versification, deuterocanon, latin_key,
mnemonicon packs, `review.py render --check`.

**Failing:** `build_parallel_index.py --check` (problem 2).

**Could not run here** (not caused by the merges):
- `build_lightfoot`, `proper_names`, and the KJV witness gate. The network
  policy blocks ccel.org and gutenberg.org.
- `build_hymn_corpus`. It needs the private Latin shelf.
- `build_lemma_bridge`. It needs a Vocabularium checkout.
- `build_strongs`, `place_catena`. Their lexicon inputs aren't fetched here.

## Unrelated: Perseus upstream drift

`structure_texts.py` on freshly fetched sources gives new `sha256` values
for `iliad-butler`, `odyssey-eng4` and `aeneid-williams`. Those three
Perseus fetches aren't pinned to a commit, so upstream has changed since
`main` recorded them. `main` has the same drift. I didn't commit the new
values.
