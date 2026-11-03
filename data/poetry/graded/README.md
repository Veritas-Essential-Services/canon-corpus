<!-- prov: 2026-11-03 claude-opus-5-5 drafted (Adam: bring the Poetry Hoard to its most complete state; the graded mega book first) -->
<!-- fable_review: pending -->
# The graded volume — the Schoolroom Treasury, one book in five bands

Adam's decision (2026-10-07): **one mega book, graded by band inside it**; split per band later only if each band stands alone. No admission threshold: everything is placed, then Adam culls.

`pipeline/grade_poetry.py` places every poem in the hoard's four poetry layers (AO, heroic addendum, collections, treasury: 7,959 poems, 6,760 printed in full) into one of five bands and writes the book.

| File | What |
|---|---|
| `book-bands.json` | **hand-kept**: the band each of the pool's 55 books places its pieces in, and why (title, preface, stated audience). General anthologies carry `vote: false`. |
| `graded.jsonl` | built: one row per poem — `band`, `why`, `found_in`, `n_books`, `lines`, `length`, `difficulty` (1–3), `flags`, `rank` |
| `graded.csv` | built: the same, flat, with a blank **`keep?`** column — the cull sheet |
| `volume/<band>.md` | built: the reading edition, every poem of the band, in full where hosted, a link where not; parts over 4 MB are numbered |
| `CONTENTS.md` | built: counts per band, the commonest reasons, and the flagged poems |

## How a poem is placed

1. **AO's year**, where AO lists the poem (Years 1–3, 4–6, 7–9, 10–12).
2. Else the **heroic addendum's year**.
3. Else the **books it was found in vote**, each with its band from `book-bands.json`; the band is the lower median of the votes — the earliest band by which at least half the placing books had it (the plan's "earliest year that most of the readers placed it"). McGuffey's readers vote by number (2–3 → Years 1–3, 4 → 4–6, 5 → 7–9, 6 → 10–12).
4. A poem found **only in general anthologies** (Golden Treasury, Oxford Book, World's Best Poetry …) goes to Years 10–12, marked `general anthologies only`. That is the largest group (about 3,000), and the likeliest place for Adam to move poems down.

Order inside a band: AO's own order first (year, term, order), then the most-printed poems first.

`difficulty` is a relative mark (thirds of the hoard on syllables per word, long-word share, archaisms and line length), not a reading age. `flags` marks poems long for a young band (over 100 lines in Nursery or Years 1–3, over 300 in 4–6) for a second look; nothing is moved by a flag.

## Rebuild

    python3 pipeline/grade_poetry.py          # after any build_poetry.py run, or an edit to book-bands.json
    python3 tests/grade_poetry_test.py        # --check, coverage, AO years, the 5 MB cap

Generated text, committed per ADR 0026 exception 3. Never edit the built files by hand; change `book-bands.json` or the script.

## What comes next

- **Adam culls** in `graded.csv` (or the cull page, if published): `keep?` = `y` / `n`, and a band to move a poem to.
- Then: a cull-aware rebuild (only kept poems in `volume/`), stanza portions for the Mnemonicon, and the pictures (pre-1931 Rackham, Wyeth, Pyle) per band.
- Declamations (prose speeches) get their own section once that layer lands.
