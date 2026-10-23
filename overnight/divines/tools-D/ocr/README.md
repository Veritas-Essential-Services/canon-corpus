# OCR collation (Lane D)

These tools turn a rough Internet Archive OCR into a corrected witness. The scan itself is never
edited. Each step is a rule or a recorded reading that reruns on refetch (CLAUDE.md rule 2).

    overnight/divines/tools-D/ocr/run.sh <ia_id> [workdir]

The script reads `data/ocr-fixes/<ia_id>.json` and writes
`data/corpus/<shelf>/<witness>.corrected.txt`, which is gitignored like all corpus text.

It needs `tesseract` (eng), `/usr/share/dict/words`, Python 3 with Pillow (for `crops.py` only),
and network access to archive.org.

## The passes, in order

1. **Majority vote** (`collate.py`). The scan is token-aligned with the other scans of the *same
   printing*, listed in `collated_with`. Where the primary has a non-word and the others agree on a
   word, the vote wins.
2. **Re-OCR** (`reocr.py`). Tesseract is run on the pages that are still garbled. A tesseract word
   replaces a garbled token only when the alignment is one-for-one and the result is a real word.
   Set `OMP_THREAD_LIMIT=1`.
3. **Hand readings** (`replay.py`, again in `final.py`). The rows in the fix list come from
   reading cropped page images (`crops.py <id> <maxpage> <minpage> <outdir>` makes the contact
   sheets).
4. **Scanner habits** (`pass2.py`, `garble.py`):
   - `*s` / `^s` becomes `’s`.
   - `t123` becomes `†123`.
   - Old-style figures are fixed (`i8` becomes `18`).
   - Stray carets are removed.
   - Small caps are uppercased.
   - Picture and ornament noise is dropped.
5. **Index** (`idxrules.py`), for pages from `index_from_page` on:
   - Roman volume numbers read as digits are fixed (`11:` becomes `II:`).
   - The edition marks are **kept**. In My Book House, `*` marks a first-edition page and `†` a
     second-edition page. Either can print before or after the number, so never strip a `*` as a
     leader dot.

## The fix lists are the one place book words are committed

Adam ruled on 2026-10-23 that a word-level fix list may be committed: each row is
`[page, OCR token(s), reading]`. RULES.md's "no book text" rule still holds for everything else:
- no passages,
- no corrected text files,
- nothing quoted in chat, commits or reports.

## Limits

- An OCR error that happens to be a real word is caught only by the vote. For example, a drop
  cap read as "HE" for "THE".
- Index lines whose reference numbers fell out of reading order are only partly repaired.
