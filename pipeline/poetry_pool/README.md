# pipeline/poetry_pool — how the candidate pool was built (2026-10-07)

The scripts that turned 55 Gutenberg anthologies into `data/poetry/pool/`.
They are kept as they were run, for the record and for adding books later;
several carry the scratch paths of the session that wrote them, so read a
script before rerunning it.

- `tools/p_<pg id>.py`, `chscripts/*.py`: one parser per book (or per book
  family), each writing `rows/<pg id>.jsonl`; `tools/lib.py` and
  `chscripts/common.py` hold the shared cutting code.
- `tools/church.py`: the Alfred J. Church shelf.
- `merge.py`: an earlier copy of `pipeline/merge_poetry_pool.py`, which is
  the one to use.
- `fetch_texts.py`: fetches the books themselves into
  `data/corpus/pool-texts/` (gitignored), by Gutenberg id from
  `data/poetry/pool/sources.json`.

The per-book rows are committed in `data/poetry/pool/rows/`, and
`data/poetry/pool/pool.csv` is the sheet Adam culls from (its `keep?`
column starts blank). Moved here from the project's shared folder on
2026-10-13 so they live in git.
