# The Unscanner (Phase A)

A scanned public-domain book in; the book re-set out. Built 2026-10-16 to the design in the vault
(`9 - Projects/Unscanner/`): Phase A is one user, public domain only, faithful re-typesetting.
Phase B (submissions, accounts, a review queue) is deferred and is not here.

```
python3 -m unscanner run church-odyssey-boys                     # a slug fetch_sources.ARCHIVE_OCR declares
python3 -m unscanner run my-book --archive <identifier>          # any archive.org scan
python3 -m unscanner run my-book --pdf scan.pdf --rights "why it is PD" --title T --author A
python3 -m unscanner run church-odyssey-boys --pages 1-45        # a trial on part of a book
python3 -m unscanner run church-odyssey-boys --to-corpus         # and hand the result to structure_texts.py
python3 tests/unscanner_test.py                                  # 36 offline checks
```

Needs `tesseract` (eng), `pdftoppm`/`pdfinfo` (poppler), Python with Pillow and numpy (OpenCV
optional), and `npm` for the font candidates. A 320-page book takes about 4 minutes of OCR on two
cores (`--jobs 2`, each tesseract on one thread) and a minute of analysis; OCR is cached per page, so
re-runs and changes to the rules cost only the minute.

## The rights gate comes first

An archive.org item must carry the Archive's `possible-copyright-status: NOT_IN_COPYRIGHT`, or the run
must state why the edition is public domain with `--rights "..."`. A local PDF always needs it. The run
refuses otherwise. The reason is written into the colophon, the EPUB's `dc:rights`, and the report.

## What it does, in order

| step | module | what is measured, and the rule |
|---|---|---|
| scan in | `scan.py` | PDF -> 300 dpi grey page -> tesseract hOCR (words, boxes, confidences). Resumable, atomic. |
| binding | `scandata.py` | the Archive's leaf record: covers and everything before the title page leave the reading editions |
| furniture | `layout.py` | folios and running heads by position and recurrence; an unreadable or misread folio is set from the neighbours when both sides agree |
| page kind | `images.py`, `layout.py` | plate / blank / text from the ink no word accounts for |
| style | `style.py` | italic from the slant that sharpens the stems; small capitals from x-height vs cap height |
| blocks | `layout.py` | paragraph = printed indent; heading = size, centring, capitals; verse = deep indent; a page's unindented first line continues the last page's paragraph |
| second witness | `collate.py` | the Archive's own OCR, consulted only where ours is unsure AND unattested AND theirs is a word the book prints elsewhere |
| structure | `book.py` | chapters from CHAPTER headings, numbered in sequence when the numeral is misread; titles from the best-read printing; declared unnumbered sections |
| typeface | `fonts.py` | 14 OFL candidates (Fontsource, pinned 5.3.0) set word by word against the scan; ranked by shape and set width |
| editions | `emit.py` | reflowed HTML, faithful page HTML, EPUB 3, corpus units, review sheet |

Every rule's count goes into `out/report.json` and onto the review sheet, which shows each page's scan
beside its reading with low-confidence words marked, and lists every word mended from the second
witness and every margin hyphen decided without evidence.

## Outputs (all under `data/unscanner/<slug>/`, gitignored, rebuildable)

- `out/reflow/index.html` the book to read, in the matched face, plates in place
- `out/pages/index.html` the faithful edition: each page at its printed proportions, each word where it was printed
- `out/book.epub` EPUB 3, font and plates inside
- `out/units.json` the corpus shape; each unit names its scan pages and printed page labels
- `out/review/index.html` the proofing sheet

## What it does not claim

- It is **unproofread OCR**. Misreadings stand, and the honesty field says so with the mean confidence.
- The typeface is **the closest open candidate**, not the original face. When the top two score within
  0.01 the report says *inconclusive* (it did for the Iliad). The point size assumes the PDF states the
  page's real size, which library scans often do not.
- Italic and small capitals are measurements and can be wrong on a dirty page; they are counted.
- Plates are cut from the scan, never redrawn. The cut is the ink's bounding box.

## Proven on

| book | pages | mean conf | chapters | units | folios vs the Archive's record | mended from 2nd witness |
|---|---|---|---|---|---|---|
| Church, *The Odyssey for Boys and Girls* | 318 | 93.3 | 23 of 23 | 436 | 212 of 212 agree | 51 |
| Church, *The Iliad for Boys and Girls* | 344 | 93.7 | 25 of 25 + *The End of Troy* | 374 | 217 of 217 agree | 23 |

Against the Archive's own text of the Odyssey, the two readings agree on 99.1% of words; the Unscanner
keeps the book's accents (*Athené*, *Circé*) that the Archive's text drops, and its paragraphs come from
the printed indentation rather than a guess (436 paragraphs against the djvu ingest's 331).
