# canon-corpus — rules for AI sessions

## What this is
The shared source + structure layer of the Canon OS (Rings 1–2): manifest-
driven fetchers and the structure_texts converters that turn public-domain
texts into unit-id JSON. Extracted from `patrimonium` 2026-07-22 (its
history up to commit `d33503e` is the pre-extraction acquisitions ledger).
Consumers: **armarium** (sibling repo), patrimonium, and later Memoria and
the Resolver. Owner: Adam — hobbyist; beginner-friendly explanations
appreciated.

The living truth for project state is the Obsidian vault:
`9 - Projects/Armarium/_STATUS — Armarium.md`. Read it first.

## Golden rules
1. **Manifests ARE the collection.** PERSEUS/CCEL/GUTENBERG_EXTRA dicts in
   `pipeline/fetch_sources.py` + `data/books/manifest.json` are committed;
   corpus texts and built JSON are gitignored and rebuildable. Commit
   history is the acquisitions ledger — one commit per acquisition wave.
2. **Never hand-edit a source text.** Fixes live in per-book rules in
   `structure_texts.py` so they rerun on refetch.
3. **The unit id is the spine** of the whole suite: canonical citation ↔
   unit id ↔ any edition's page. Do not change existing id schemes without
   a vault ruling; CTS-URN alignment is pending (ids stay short, manifest
   records the URN per edition).
4. **Honesty fields are load-bearing.** Every book's `scheme.honesty`
   states its real citation resolution; never pretend precision.
5. **Builds are resumable + atomic** (temp-file + rename; skip finished
   books). Keep it that way — a killed run must never corrupt output.
6. IP posture: host/structure/publish public-domain freely; map facts
   about copyrighted translations, never copy. CCEL asks non-commercial
   use of some prepared editions — check per work before republishing.

## Commands
    python3 pipeline/fetch_sources.py        # fetch everything missing (resumable)
    python3 pipeline/fetch_sources.py --list # show the manifests
    python3 pipeline/structure_texts.py      # build data/books/*.json + manifest
    python3 tests/structure_test.py          # 18 offline checks (no corpus needed)

## Layout
- pipeline/fetch_sources.py — PERSEUS (TEI) + CCEL (ThML) + GUTENBERG (.txt)
  manifests and fetcher; downloads land in data/corpus/ (gitignored)
- pipeline/structure_texts.py — the converters: TEI / ThML / KJV /
  Gutenberg verse–prose–drama → data/books/<slug>.json (gitignored) +
  data/books/manifest.json (committed: checksums, schemes, provenance)
- tests/structure_test.py — offline converter checks, fixtures inline

## Sandbox mechanics (inherited from patrimonium — they apply here)
- Do NOT run live git in a mounted/synced folder — copy to /tmp, run git
  there, copy the .git back. `git config core.fileMode false` in fresh copies.
- No detached background jobs; chunk long work into <45 s foreground calls;
  keep scripts resumable.
- Big builds: build to /tmp then copy in (mounted disks are slow; Adam's
  native Windows disk is fast).

## Scaling (decided, don't re-litigate — see vault "Armarium at scale")
Before thousands of books: manifests become CSV, parallel structure
conversion, throttled bulk fetch. The data model itself already scales.

## End every working session
Update the vault _STATUS note (state, one dated log line, next actions)
and commit. A session that doesn't update the status note didn't happen.
