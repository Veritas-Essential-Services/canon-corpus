# Bloom burn tools (Lane B, 2026-10-27 to 2026-11-03)

These are the scripts that built the Bloom checklist, the shelf plans and the Admissions page. They are committed so that nothing lives only in a session's scratchpad. They ran from a scratchpad folder. Paths inside them are absolute (`/home/user/canon-corpus`, the scratchpad); point them at your own checkout before re-running.

| File | What it does |
|---|---|
| `bloom.json` | Bloom's appendix (The Western Canon, 1994), parsed from Robert Teeter's transcription |
| `heldidx.py`, `heldidx2.py` | Index every `*_shelf.json` on every origin branch (the "held" set) |
| `match.py`, `pgmatch.py`, `gpg.py`, `gt.py` | Match Bloom entries to held shelves and to the Gutenberg catalogue |
| `mkbloom.py` | Build the checklist (with Lane C's held and staged maps from `laneC.json`) |
| `research/BRIEF.md` | The brief the research agents followed; their output is `../bloom-research.jsonl` |
| `mkplan.py` | Turn `add` verdicts into per-author shelf plans (`plans/*.json`); skips any id held anywhere |
| `apply.py` | Write or extend `pipeline/<shelf>_shelf.json` from one plan entry, with its `_bloom` case block |
| `runall.sh` | For each shelf in a plan: apply, `fetch_shelf.py`, `--verify --record`; commit only if clean |
| `cases1-3.py`, `mkdata.py` | Written cases for the PR #38 shelves (Admissions tab 1) |
| `mkadds.py` | Collect `_bloom` rows into the additions list (tab 3) and refine checklist statuses |
| `page.tpl.html`, `build.py` | The Admissions page template and its builder |
| `shot3.js` | Playwright smoke test of the built page |

Re-run order: heldidx2 → match/pgmatch → mkbloom → (research) → mkplan → runall.sh plan → mkadds → build.py.
