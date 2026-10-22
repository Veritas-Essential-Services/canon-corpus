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

## Several scans of one book (2026-10-20, Character Sketches vol. 6)

Two printings of the same volume (Toronto 1892, Cornell 1896), each read by two engines (tesseract,
and the Archive's own), are one text. Adam: *"run each of the different editions of the same volume
against each other and merge them intelligently,"* then *"build all this into the unscanner."*

    python3 -m unscanner run <slug-a> --archive <id-a>        # each scan first, as any book
    python3 -m unscanner run <slug-b> --archive <id-b>
    python3 -m unscanner editions collate --scan a=data/unscanner/<slug-a> --scan b=data/unscanner/<slug-b> \
        --djvu a=<id-a>_djvu.xml --djvu b=<id-b>_djvu.xml --base a --volume 6 \
        [--brewer data/lexicons/brewer-1894.paras.json.gz] --out <dir>
    #   -> collation.json, review.json, rule-clears.json, proof-desk.html (publish it; Adam answers)
    python3 -m unscanner editions merge --collation <dir>/collation.json --base-dir data/unscanner/<slug-a> \
        --base a --volume 6 --answers <dir>/rule-clears.json <claude-reads.json> <adam.json> --out <dir>
    #   -> merged.json (paragraphs, each with its pages) and merged.txt

Answer files rank lowest first: a rule's clear, then Claude's read of the image, then Adam's pick.
Review ids are `v<vol>-p<page>-i<index>`, the word's place among the base scan's words: so a rebuild of
the base scan must keep its line order (it does: columns and paragraphs live in `blocks`).

### What the engines get wrong, and the rule for each (all agree with Adam's 120 answers)

Each was learned from Adam's answers or his notes on the desk; `unscanner/learned.py` and
`unscanner/smallcaps.py` hold them, `tests/smallcaps_test.py` and `tests/editions_test.py` check them.

- **Roman numerals** garble ("Ill", "lU", "HI", "1.") -> the roman reading; digits never beat one.
- **The æ ligature** reads as "e", "se", "ce", "ae", "ee" -> æ. Adam: Caesar and Cæsar are one word
  (the Armarium's search folds æ to ae, wordhoard PR #120).
- **Small capitals** (a full capital, then capitals at x-height) read as lower case or a jumble
  (KateErFELTo). Signs: the jumble, or a **headword before its bracket** (LONG (St. John), MORISON
  (Dr.)), which the engines read as a plain word. The word is cut from each scan, enlarged, and
  reread capitals-only at four crop sizes; taken when both printings give the same word.
- **c read as e** -> c, unless only the e-form is a word. But a **stock abbreviation** wins first
  (etc., &c., viz., i.e., e.g., cf., ib., ibid., sc., q.v.): Adam, "etc. is more likely than ctc."
- **ll read as U** inside a lower-case word (RoUa, baU,) -> ll, or li/il (LilUa -> Lillia).
- **A capital U or H inside a word is "li", and a final se/ae/z is æ** (AngUae, AngHse -> Angliæ),
  only when both scans arrive at it (Cormae/Cormac is Cormac).
- **R read as E/B, b as h** -> our engine's reading. **Both engines on one scan agree** -> that pair.
- **Pronunciation marks are kept as printed** (Socrătês, Korân); Adam, 2026-10-20: "keep the marks you
  collected and replace the ones I skipped."
- **Claude's eyes**: tested blind on Adam's 120 answers, 111 exact, 6 more differing only in mark or
  ligature style, 1 misread (italic æ read as œ). So Claude reads every crop still open; a reading that
  agrees with an engine clears ("Claude's read"), one no engine had is flagged ("no engine had it").
- **Look up a strange word's neighbours before calling it wrong**: "fey expand" is the end of the
  name "Cuf- / fey", broken at the margin; "fiared" is the fl ligature read as fi (flared).

### Page and line rules this book added to the Unscanner (layout.py)

- **Two columns** (`find_columns`): 8+ lines wholly each side of the middle, few across it. Blocks
  are built per column, left then right; `p["lines"]` keeps its order. 200 of 330 pages.
- **A running head over each column**, at up to 16% down the page, often one or two capitalised words
  ("PIPCHIN", "214 PIPPA"), sometimes two lines of one row ("217", "PLAIDS"): dropped. Found 4 -> 191.
- **A printer's signature mark** ("III", "lll", "pats": a scrap at a column's foot, set small) is not
  text: dropped. Twenty "III"s had reached the review sheet as words.
- **Margin breaks, rule 6b** (`more=True`): a range ("1630-" / "1706"), small capitals across the
  margin ("Dia-" / "MONDS.)" -> DIAMONDS.)), a name's hyphen ("Fitz-" / "James"). **6c**
  (`dictionary=load_dictionary(repo)`): with no evidence in the book itself, Webster 1913 decides,
  hyphened (first-rate, knight-errant, to-day) or solid with its endings (pasture, conditions,
  perverted); a name broken mid-word is joined (Copper- / field); a prefix is joined (con- / gress);
  two words with no headword keep it (knife-grinder). **6d**: the OCR's dirt round a break ("be- -",
  "con--", "ex- -ploits", "Decem- ‘ber", "_tention"). A paragraph begun in lower case after a broken
  word continues it (verse running on into the next column). Never across a paragraph start: there a
  capital after a hyphen is a new entry ("Pari-" / "Schamir (The)").
- **Dashes, rule 7** (`dashes`): ranges take an en dash (1554–1628); em dashes are set close; a lone
  "-" after a sentence before a name the book prints after ".—" elsewhere is the attribution dash
  (".—Tennyson"); any other lone "-" is dirt.
- 6b-6d and 7 are off unless asked for (`more=True`, `dictionary=`), so the Church Homers, already
  built, rebuild byte-identical until someone turns them on for them and reviews the difference.

Vol. 6 by the numbers: 105,947 words; 715 to the desk; 267 cleared by rule, 326 by Claude's read,
120 by Adam, 2 by context (flared, fey). Merged: 3,021 paragraphs; 2,134 margin breaks rejoined, 119
hyphens kept. Still open (column order the layout cannot see): "(1516-" / PLINY, "qui-" / fit,
"Dra-" / Roland, "Pari-" / Schamir, "Ar-" / Smyrna, "suc-" / Seotch, "SHEP-" / Shepherd. And the base
text outside the desk still carries tesseract's c-for-e misreads (seeretly, Neweastle): the next rule.

## The fix library (2026-10-20)

Adam: *"build a whole system that picks and chooses from a whole library of fixes and choose the
elements that are actually in play with the particular typesetting that one is working from."*

    python3 -m unscanner fixes fetch       # pinned sources -> data/fixes/src/ (gitignored)
    python3 -m unscanner fixes build       # -> data/fixes/library.jsonl: 116,281 rules, each with its source
    python3 -m unscanner fixes profile --book data/unscanner/<slug> [--review R.json --answers A.json ...]
    python3 -m unscanner run <slug> ... --fixes                     # one scan: profile and apply
    python3 -m unscanner editions merge ... --fixes <profile.json>  # several scans: apply to what the vote left

**Sources** (none committed; the repo is public): Distributed Proofreaders' Guiguts scanno lists
(GPL-2.0: 4,377 rules), Ted Underwood's OCR-normalizer rules (no licence stated, so local use only:
98,381 corrections, 401 long-s pairs, 11,308 normalizations), and the ICDAR 2019 post-OCR competition's
English data (CC BY 4.0, Rigaud, Doucet, Coustaty and Moreux), mined for 210 character confusions and
1,658 word pairs. Normalizations (Underwood's syncope, fusing, hyphen and variant rules modernize the
text) are kept and never applied to a faithful transcription.

**How a rule earns its place in a book** (`fixes.profile`):
1. *The typeface's confusions first*, learned from the scan's own words: every word that is no word is
   tried with each known confusion; the confusion that turns many of them into words this book prints
   cleanly is a trait of the face. Vol. 6 Toronto: e read for c (395 words, desk 100%), n for u, c for
   e, e for o, u for n. The Cornell printing adds b for h ("bere", "bowever", "borses").
2. *A borrowed word rule only on a confusion the face makes*: "chureh" -> "church" rests on c read as e,
   in play; "foon" -> "soon" rests on the long s, which an 1892 book has not: it stays off without anyone
   deciding so.
3. *The book's own words decide what is real*: a dictionary word (with its endings) is never changed; a
   word the book prints cleanly is what the page says ("enfants", "valeur") unless one confusion makes a
   dictionary word the book prints three times as often ("ealled", read confidently 14 times, beside
   "called" 182 times: a habit of the OCR, not a word). A name the book prints cleanly stays ("Hugo",
   which a borrowed rule turns into "huge"). A four-letter word needs the corrected word to be the
   book's habit ("loue" is love, not lone). Half a word at the margin is never fixed ("Anto-").
4. *The desk*: where a rule fires on a word a person or Claude's eyes settled, its precision on this
   typesetting; under 90% (3+ cases) it is off. The rules' own clears are never the truth.
5. *States*: `on` (applied), `flag` (for a person: a stealth scanno, where both forms are words; a known
   misspelling with no correction; a rule on a confusion this face does not show), `off`.

**Measured on vol. 6**: against the 1,866 words the four-reading vote mended (independent of the
library), the library alone, from the raw scan word, agrees on 446 and disagrees on none. Over 103,564
undisputed words it changes 56, the misreadings every engine shared ("Chaueer", "Provenee", "vehiele",
"Diekens"). The Cornell scan alone (no desk, no second scan): 105 words.
