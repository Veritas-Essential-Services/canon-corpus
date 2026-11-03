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

## Fix-list switches

- `pages_from_twin`: rows of `[page, twin_id, twin_page]`. A page too damaged to repair takes the
  twin scan's reading of the same plate, and this scan's own page then votes on the twin's slips.
  `twinpages.py <id>` suggests rows; check each one against the images, since a reshoot or a
  missing leaf shifts the twin's numbering.
- `reocr_damaged_pages`: also re-OCR every page with three or more garbled tokens.
- `vote_min_ratio` (default 0.6): lower it when damaged pages barely match their twin.
- A hand reading is applied once per row. To fix the same slip twice on a page, give two rows.

## Google scans: habits worth a sweep

These are real words, so the vote and the garble test miss them:
- `li` read as `h` and back (`liis`, `tlie`, `pubhshed`), `lie` for `he`, `bad` for `had`,
  `Avas` for `was`, `iii`/`iu` for `in`;
- a lone `P` or `F` for `?`;
- capital headings in heavy type (`BOBEBT BTTCHAHAK` for ROBERT BUCHANAN);
- italic lines (`Tkanatopsis`, `XIF.` for XIV.);
- old-style figures: `6` read as `0` or `8` (`1810` for 1846). Compare each page's years with
  tesseract's and read the disagreements off the image.

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
