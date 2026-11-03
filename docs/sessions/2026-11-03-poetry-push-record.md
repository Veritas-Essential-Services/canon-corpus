> ⚠️ PARKED — not in the vault.
> Destination: 9 - Projects/<Poetry Hoard or Word Hoard>/_STATUS — <same>.md (whichever note covers the Poetry Hoard / Schoolroom Treasury)
> Parked: 2026-11-03, because the vault was not connected to this cloud session.
> Version: v1. This file is complete on its own; nothing to reconcile.

# Poetry Hoard push, 2026-11-03: record

<!-- model_log: 2026-11-03 claude-opus-5-5 drafted (thread "Complete the Poetry Hoard project") -->

Adam asked for a big push to bring the Poetry Hoard as close to complete as possible, without waiting on him, then to file everything and leave a record. This is that record.

## What I found already done

The coordinator's list of open items was stale. I checked each one against GitHub:

- canon-corpus **#29** (treasury layer) is merged.
- wordhoard **#14, #23, #39, #40, #44, #57, #63, #77** are all merged.
- Migrations **023** (Mnemonicon commons) and **024** (Intake) were **applied by Adam on 2026-10-19**, per the header in each file. **No SQL is owed.**
- The Mnemonicon offline test ("served card is not there") **passes on main**, 37/37, once `WORDHOARD_CORE_DIR` points at `packages/core`.
- The Church Homer books were already in canon-corpus as single-scan OCR (since 2026-10-16); what was missing was collation and proofing.

## What was done (all draft PRs, none merged)

| PR | What | Checks |
|---|---|---|
| [canon-corpus #60](https://github.com/Veritas-Essential-Services/canon-corpus/pull/60) | **The graded mega book.** `pipeline/grade_poetry.py` places all **7,959 poems** (6,760 in full) in five bands: Nursery 819, Years 1–3 1,288, Years 4–6 1,407, Years 7–9 1,064, Years 10–12 3,381. Writes `data/poetry/graded/`: `graded.csv` (blank `keep?` column, the cull sheet), `volume/<band>.md` (reading edition), `graded.jsonl`, `CONTENTS.md`, `book-bands.json` (hand-kept band per source book) | grade_poetry_test 9/9; poetry_test 172/0 |
| [canon-corpus #65](https://github.com/Veritas-Essential-Services/canon-corpus/pull/65) | **Church, Iliad (1907) and Odyssey (1906) for Boys and Girls**, collated against second and third archive.org scans; disputed readings read off page images. Iliad 26 chapters / 43,706 words; Odyssey 23 chapters / 42,489 words. Unit ids unchanged | structure_test 270; build_stories --check mint 0 |
| [canon-corpus #66](https://github.com/Veritas-Essential-Services/canon-corpus/pull/66) | **The declamations layer.** 660 speeches and prose pieces from the old readers and speakers (653 hosted, 7 linked out), 12 Mnemonicon packs (`declamation-pg<n>.json`). Gettysburg Address and Patrick Henry hosted; Crispin's Day cut from Patriotic Song (1901, abridged) | poetry_test 211/0; wh_uid 73/0; mnemonicon_pack 112/0; layer --check mint 0 |
| [wordhoard #271](https://github.com/Veritas-Essential-Services/wordhoard/pull/271) | **Poetry shelf in the Mnemonicon/Promptuarium app** re-synced: 125 packs, 8,013 pieces (was 71 / 1,384). Treasury packs labelled by book; script also ready for the declamation packs | all Mnemonicon suites pass; size check 0 over |

**Cull page (artifact):** https://claude.ai/artifact/NqMBD4t3i6eHx63AwC9429. You can Keep, Cut or Move each poem to another band. Marks save in the page's database (collection `verdicts`, one doc per poem uid), and a later Claude session can read them back into `graded.csv`.

## For Adam's hands

There's no SQL to paste this time.

1. **Review and merge** the four PRs. Order: #60, #65 and #66 in any order, then #271. GitHub wouldn't add you as reviewer because the PRs post under your account, so they're only assigned to you.
2. **Cull** on the cull page, whenever you like. Start with "General anthologies only" in Years 10–12 (about 3,000 poems), because that's where most of the poems that belong in lower bands are.
3. **Run the full rebuild check where gutenberg.org is reachable.** The cloud session couldn't reach it, so the other layers' byte-identical rebuild wasn't run. In PowerShell, adjusting the path if your clone lives elsewhere:

```powershell
cd C:\Users\adamk\Claude\Projects\canon-corpus
git fetch origin
git switch claude/declamations
git pull
python pipeline\build_poetry.py --fetch
python pipeline\build_poetry.py --check
python tests\poetry_test.py
```

4. **After #66 merges, put the declamations on the Poetry shelf.** Or ask Claude to do it:

```powershell
cd C:\Users\adamk\Claude\Projects\canon-corpus
git switch main
git pull
cd ..\wordhoard
git fetch origin
git switch claude/poetry-treasury-shelf
git pull
python apps\mnemonicon\tools\sync_poetry_packs.py ..\canon-corpus
git add apps/mnemonicon/site/poetry
git commit -m "Poetry shelf: the declamation packs"
git push
```

5. **Decisions only you can make:**
   - Should the 33 verse pieces the pool labelled prose move from declamations to the treasury? (#66)
   - Which List of Illustrations should the Iliad show: the 1907 printing (12 plates) or the 1923 printing (16)? (#65)
6. **Optional:** allow `www.gutenberg.org` in this project's cloud environment network settings, so future sessions can run full rebuilds themselves.

## Follow-ups found (not done)

- **Horatius typo:** the canon-corpus text (PG #847) reads "Lars Porsena of **Closium**"; it should be Clusium. It needs a `fix` rule plus a full `--fetch` rebuild. The house Poetry Hoard copy, proofed from the 1851 Tauchnitz, is already correct.
- **17 AO/heroic poems are linked out but could be hosted.** A pre-1931 printing is in the pool for each, including Lochinvar (11 books), Casey at the Bat and The Walrus and the Carpenter. They also need a full rebuild.
- **The Man in the Arena (1910)** is in none of the pool's books, so it needs a pre-1931 printing. Wirt's own 1817 *Sketches* is also missing for Patrick Henry; the McGuffey's Sixth printing of Wirt's text is hosted.
- **Stories from Homer (1878)**: no Gutenberg text was found. gutenberg.org itself couldn't be checked.
- **The graded volume doesn't include the declamations yet.** Add a prose section per band once #66 merges.
- Rooms plan (Odeum, Hymn of the Month, Folk Song Chest, Almanac): left alone this push, because other threads are working in wordhoard's rooms right now and I didn't want to duplicate them.

## Next actions
- [ ] Merge #60, #65, #66, then #271 (with the declamations re-sync)
- [ ] Cull on the cull page
- [ ] Full `build_poetry.py --fetch --check` on the ThinkPad
- [ ] Rule on the 33 verse "declamations" and the Iliad plate list
- [ ] Move this note into the vault.

*Session log line for the _STATUS note:*
`2026-11-03 — Big push: graded mega book (7,959 poems, 5 bands, canon-corpus #60) + cull page; Church Iliad/Odyssey collated (#65); declamations layer 660 pieces (#66); Treasury packs on the Mnemonicon shelf (wordhoard #271). No SQL owed (023/024 applied 10-19).`
