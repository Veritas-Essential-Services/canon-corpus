# The Press — Puritan classics, set for publishing

The Press turns a public-domain text the library already knows about into a
book: one Pandoc Markdown master per title, built to EPUB and HTML, with the
original title page, clean headings, footnotes, every scripture reference
tagged with its KJV verse id, an Index of Scripture References, and a Note on
the Text that names the source edition and lists every change. It is the
"small step from publish-ready" layer on top of the corpus.

## Which books

`pipeline/press_catalog.json` lists the best-selling Puritan sets and maps
each title to its **original public-domain edition**:

| Tier | Set | Titles |
|---|---|---|
| 1 | Banner of Truth, *Puritan Classics* box set (Banner's own best-of the series) | 15 |
| 2 | Banner of Truth, *Puritan Paperbacks* (the rest of the 62-volume set) | 50 |
| 3 | Reformation Heritage Books, *Puritan Treasures for Today* | 22 |

The modern edition is only the pointer. Banner's and RHB's abridgements,
updated wording, selections, introductions and notes are in copyright and are
never copied; the Press sets the author's full text from the edition named in
the catalog (Goold's Owen, Grosart's Sibbes and Brooks, Offor's Bunyan, Bonar's
Rutherford, and so on). Where Banner's volume is itself a modern selection
(*Smooth Stones*, *Gospel Life*, *The Golden Treasury*), the catalog marks it
excluded and says why.

"Best-selling" was read from the publishers' own lists (Banner's box set is
its curated best-of the series), not from Amazon: Amazon refuses automated
reads, and the per-edition sales ranks a search returned were scattered across
dozens of reprints of the same title.

## Commands

    python3 pipeline/press_build.py --list              # every title and its state
    python3 pipeline/press_build.py <slug>              # set one book -> data/press/<slug>/
    python3 pipeline/press_build.py --ready             # every title with a usable source
    python3 pipeline/press_proof.py <slug>              # proof against the scan (see below)
    python3 pipeline/press_ocr.py --heads <ia-id>       # find a treatise's leaves in a Works volume
    python3 tests/press_test.py                         # offline checks

Output (`data/press/<slug>/`, gitignored, rebuildable): `<slug>.md` (the
master), `<slug>.epub`, `<slug>.html` (preview), `qa.json`, `proof.json`.
Committed: the code, the catalog, `pipeline/press_rules/<slug>.json` (each
book's corrections, each with its evidence), `docs/press/QA.md` and
`docs/press/proof/<slug>.md` (numbers and the words a person must look at).

## Sources, in order of preference

1. **CCEL ThML** (`press_thml.py`): a proofread transcription with real
   structure (divisions, italics, footnotes, osisRef-tagged scripture). Each
   CCEL file's print source is checked first: `boston/crook` is a 2000
   modernised rewrite and is refused; `rutherford/letters` looks like Banner's
   1973 selection and is refused in favour of Bonar's complete edition.
2. **Project Gutenberg** (`press_text.py`): Offor's Bunyan and similar. One
   treatise is cut from a Works volume by its title line. PG dropped many of
   Offor's footnote marks; such notes print under "Further Notes" rather than
   being guessed into place, and the QA counts them.
3. **Internet Archive scans** (`press_abbyy.py` + `press_ocr.py`): the volume's
   ABBYY FineReader XML, which keeps italics, font sizes and line positions.
   Running heads and page numbers are dropped (the page number becomes an
   anchor), smaller type at the foot of a page becomes that page's footnotes,
   line-end hyphens are resolved against the volume's own usage.

## Proofing: word-perfect against the scan

`press_proof.py` aligns the set text word by word with an independent OCR of a
scan of the same edition (archive.org's hOCR text, which also says which page
each word is on). Where they disagree on a real word, it fetches that page's
image and reads it again with Tesseract. Two readings of the scan agreeing
against the transcription, on a word the dictionary knows, is a confirmed
error: it becomes a correction rule with the archive.org id, leaf and printed
page as evidence, and the build applies it and lists it in the book's Note on
the Text. Anything less certain goes on the book's proof sheet for a person.

First result, Owen's *Mortification of Sin* (CCEL, Goold vol. 6): 42,945
words, 98.4% aligned to the 1862 printing; 3 transcription errors confirmed
and corrected ("judgement" ×2 where Goold prints "judgment", "the evidence"
for "the evidences"); 65 OCR misreads upheld; 18 spots left for a person.

## What is not done yet

- Books set from OCR (tier-1 Brooks, Sibbes, Flavel, Bridge, Alleine) still
  carry OCR errors until the two-engine proof (ABBYY vs Tesseract over every
  page) is run over them. The QA's "rare unknown words" column is that
  worklist.
- Rights: CCEL asks that some prepared editions not be used commercially
  (CLAUDE.md rule 6). The words are public domain; whether to publish from a
  CCEL base or re-derive from the scan is Adam's ruling.
- No uid minting: the Press writes nothing to `data/uids/`.
