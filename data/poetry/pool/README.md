# The candidate pool (Schoolroom Treasury)

Every poem found in 55 pre-1931 anthologies, school readers and recitation books on Project Gutenberg, merged into one list for Adam to cull. Built 2026-10-07. See `docs/context/schoolroom-treasury-poetry-plan.md`.

- `pool.jsonl`: 7,391 candidates from 9,953 rows. One line per poem: `pool_id`, `title`, `author`, `first_line`, `kind` (verse or prose speech), `n_books` (how many of the books carry it), `books` (Gutenberg ids), `audiences`, `also_in` (`ao`, `addendum-heroic`). Sorted by `n_books`, highest first.
- `sources.json`: 121 books checked (children's, general and recitation shelves, plus Alfred J. Church), 75 fetched. Each records its year, how the year was checked, audience, and whether its Gutenberg header says COPYRIGHTED (none do).

**How rows were matched:** by the first eight words of the first line, or by title plus the author's surname. A poem printed with a different first line or title in two books can still show as two rows.

**Known gaps:** authors are left as each book prints them, or null; first lines and verse or prose were found by heuristics; several well-known anthologies (Stedman, Heart Throbs, Stevenson's Home Book of Verse for Young Folks) are not on Gutenberg and are not counted.

Rebuild: `pipeline/merge_poetry_pool.py <dir>`, where `<dir>` holds `rows/*.jsonl` and `src/*.json`; the per-book rows, texts and parsers are in the project's shared folder under `poetry-pool/`.
