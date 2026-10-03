# Pending sources: historic English Bibles not yet on the shelf

<!-- prov: 2026-10-02 drafted (Claude Code); candidates found by web search, none opened -->
<!-- prov: 2026-10-03 edited (Claude Code): Coverdale, the Bishops' and full Tyndale landed from Bible SuperSearch -->
<!-- prov: 2026-10-03 merged (Claude Code): PR #9's Charles section, updated for build_charles.py -->

## On the shelf since 2026-10-02: Coverdale, the Bishops', Tyndale in full

All three come from Bible SuperSearch's download API
(`https://api.biblesupersearch.com/api/download?bible=<module>&format=json`,
`fetch_sources.ENGLISH_BSS`), module_version 6.2.0, retrieved 2026-10-02.
The API is not versioned, so each file is pinned by sha256 and the reader
stops on another hash or module_version.

| Bible | Module | Verses | Books | Map |
|---|---|---|---|---|
| Coverdale (1535) | `coverdale` | 31,088 | 66 (no Apocrypha) | `data/versification/coverdale-kjv.json` |
| Bishops' (1568) | `bishops` | 31,096 | 66 (no Apocrypha) | `data/versification/bishops-kjv.json` |
| Tyndale | `tyndale` | 13,852 | 33: Gen-Deut, Jonah, the NT | `data/versification/tyndale-kjv.json` (replaces the ten-book scrollmapper source) |

### Rights findings, for Adam

- **Rights line, as read:** each file's own `metadata.copyright_statement`:
  "This Bible is in the Public Domain."
- **Where the text came from is not stated.** BSS names no transcription or
  editor for any of the three.
- **The same Coverdale and Bishops' text is on textusreceptusbibles.com**
  (Gen 1:1-2 compared, word for word). That site's terms restrict reuse.
  Those are website terms of service, not a copyright: the 16th-century
  texts are public domain, and a verbatim transcription adds no new US
  copyright. Whether to honour the site's wishes anyway (as the house does
  STEPBible's request) is Adam's call. Nothing is redistributed whole: the
  corpus files are gitignored, and only pins, manifest entries and the
  verse maps are committed.
- **Tyndale cross-check:** eBible.org's `engtnt` (the 1534 NT, copr.htm:
  "Public Domain") was compared verse by verse against BSS's NT: of 7,954
  verses, 55% are identical and 96% agree at a character ratio of 0.95 or
  more. Most of the rest are spelling variants or a chapter divided
  otherwise (John 18). All three of Mark 11:26, Luke 17:36 and Rev 21:26 are
  empty in both. eBible was used only to check; it is not a second source.
- **Bishops' italics:** the metadata says `italics: 1`, but the text has no
  italic markup at all, so the printed italics are not recoverable from this
  source.

### What the transcriptions lack (named in each map's `kjv_without_verse`)

- Coverdale: 13 KJV verses. Most are slots BSS marks "(Omitted Text)". Also
  KJV Ps 72:20 and 136:24.
- Bishops': six empty slots (Gen 11:10, 46:9, Exod 6:14, 36:8, Deut 16:4,
  Esth 1:1). Each looks like a lost first verse of a section.
- Tyndale: Mark 11:26, Luke 17:36, Rev 21:26, Exod 40:14, Num 7:22.

A better transcription of any of these would fill the gaps. The Apocrypha
of Coverdale and the Bishops' are still wanted.

## Wycliffe: read from the 1850 scans (2026-10-03, branch `wycliffe-fm`)

<!-- prov: 2026-10-03 edited (Claude Code): Wycliffe sources checked; Forshall and Madden built from the scans -->

What the reachable copies hold:

- **eBible `engWycliffe`** (`https://ebible.org/Scriptures/engWycliffe_usfm.zip`,
  419,866 bytes, sha256 `d3bca9a2304c1c2d...`, copr.htm "Public Domain"): nine
  books only (Gen-Deut and the four Gospels), the LATER version, numbered as
  the KJV. The BibleNLP vref extract is made from it.
- **Bible SuperSearch:** no Wycliffe module.
- **CrossWire `Wycliffe` v2.4.1:** complete, with the Apocrypha, but CC BY-SA
  4.0, and the printed edition it was transcribed from is not named.
  **Awaiting Adam's ruling; not used.**
- **Forshall and Madden, Oxford 1850, 4 vols** (both versions in parallel
  columns: earlier on the left, later on the right). Public domain. Scanned
  from the University of Toronto (Robarts) copy. Every item's
  `possible-copyright-status` field reads `NOT_IN_COPYRIGHT`. There is no
  `rights` or `licenseurl` field.

  | Vol. | Books | archive.org item | Leaves |
  |---|---|---|---|
  | I | Genesis - Ruth | `holybiblecontain01wycluoft` | 770 |
  | II | 1 Kings - Psalms (with 3 Esdras) | `holybiblecontain02wycluoft` | 908 |
  | III | Proverbs - 2 Maccabees | `holybiblecontain03wycluoft` | 916 |
  | IV | the New Testament (with Laodiceans) | `holybiblecontain04wycluoft` | 786 |

  There is also a second scan, `ENGW850_DBS_HS` (the Digital Bible Society).
  It is one 215 MB PDF with its own OCR. Its rights field reads "The Digital
  Bible Society is unaware of any copyright restrictions". It was not opened.

**The probe.** Each item has a `_djvu.txt` and an ABBYY `_hocr.html` (word
boxes). The measures:

- **OCR quality.** Genesis was sampled, both columns, 54,796 alphabetic
  tokens. 92.1% are words in eBible's Wycliffe, once the OCR's `3` is read
  as the yogh (eBible's `y`). 95.2% are, if one trailing letter may be
  dropped. That letter is one of F&M's collation sigla, printed superscript
  and run into the word by the OCR (`li3tb`). Junk tokens: 3.0%.
- **The columns** separate cleanly by x position. The gutter is a 50-75 px
  empty strip, and it moves between versos and rectos. Two exceptions:
  - The later version's marginal glosses and the Psalter's Latin incipits
    stand in the outer margin, in smaller type. They are told apart by
    position and dropped.
  - On some leaves ABBYY ran a left-column line into the right column's,
    and stretched the joining word across the gutter. The reader assigns
    that word to the left column.
- **Verse numbers.** Most are legible digits in the outer margin of each
  column. The rest are misread in a few regular ways (`s` for 5 or 8, `e`
  for 6, `IG` for 16, `u` for 11). Each chapter opens with a heading in
  each column (`CAP. VI.`, `PSALM VII.`). Each page has a running head with
  its chapter and verse range.

**Built.** `pipeline/build_wycliffe.py` follows the Charles pattern, with
tests in `tests/wycliffe_test.py`. It produces two books, `wycliffe-earlier`
and `wycliffe-later`. Their ids are in the Clementine's numbering
(`wycliffe-later:Ps.50.3`), and each unit's `kjv` is resolved through
`vulgate-kjv.json`. The coverage of the Clementine's 35,809 verses:

| | Verses present | Numbers read / with a fix / inferred | Books by verse / by leaf |
|---|---|---|---|
| earlier | 33,797 (94.4%) | 20,664 / 5,077 / 6,949 | 73 / 0 |
| later | 30,625 (85.5%) | 16,376 / 5,643 / 7,972 | 69 / 4 (Prov, Sir, 2 John, Jude) |

The later version was also compared with eBible's transcription of the
same verses (nine books, 8,526 verses):

- 81.7% agree (word-sequence ratio 0.6 or more).
- 6.8% agree in part.
- 11.5% disagree. Most of these are runs where a missed margin number
  shifts the division by one verse until the next number read
  (Deuteronomy 4 is the worst).

The text itself is unproofread OCR, and each book says so.

## Still pending

| Bible | Why it is pending | Candidates (unverified) |
|---|---|---|
| Wycliffe (c.1395) | Built from the F&M scans (above), but the text is unproofread OCR and 6-15% of verses are missing or misdivided. A clean complete transcription is still wanted | CrossWire `Wycliffe` v2.4.1 (CC BY-SA 4.0, base edition unnamed: Adam's ruling); proofreading F&M against the scans; the DBS scan `ENGW850_DBS_HS` as a second OCR to vote with |
| Coverdale / Bishops' Apocrypha | BSS has the 66 books only | archive.org `ENGCVD_DBS_HS`, `1568TheBishopsBible` (unopened) |

## When one is fetched

1. Pin it with its commit or item identifier, file name and sha256, in
   `fetch_sources.ENGLISH` (a scrollmapper or BSS file) or in its own dict.
2. Record the rights line as read.
3. For USFM, read it with `brenton_verses` and `brenton_text` (eBible's
   markup). For another format, extend `fetch_sources.english_slots`.
4. Add its map with `build_english_versification.py`. Old spelling belongs in
   `OLD_SPELLING`. Read the `--audit` output, and read the multi-verse spans,
   in both texts.
5. Add its column to `build_parallel_index.py`.

## R. H. Charles, *The Apocrypha and Pseudepigrapha of the Old Testament* (1913)

It is the slot the deuterocanon index left open
(`pipeline/build_deuterocanon.py`). Charles is now fetched, OCR'd and built
by `pipeline/build_charles.py`, one book per work (`data/books/charles-<key>.json`,
in Charles's own numbering). What remains, to plug it in:

1. (Done: pinned, rights read, converted; see `build_charles.py`.)
2. (Done: one book per work, Charles's own numbering.)
3. Uncomment the `charles` row in `WITNESSES`, with a `passages` function
   that groups his verses by the KJV Apocrypha book they belong to, and add
   `charles` to `TSV_COLUMNS`.
4. Run `build_deuterocanon.py --audit` and read Charles's weak pairings.
   Add `HOUSE_ROWS` for what the alignment misses.
5. Charles prints 3 and 4 Maccabees, which the KJV's Apocrypha does not. They
   stay without a key (`NO_KEY_BOOKS`) until a ruling picks one, probably
   Charles's own numbering.
