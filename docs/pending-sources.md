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

## Still pending

| Bible | Why it is pending | Candidates (unverified) |
|---|---|---|
| Wycliffe (c.1395) | The one reachable PD copy (BibleNLP/ebible `eng-engWycliffe.txt`) holds only the Pentateuch and Gospels, in vref slots. It also drops verses wherever the Vulgate's chapters run longer than the Hebrew's (Lev 6:24-30, Num 16:36-50) | eBible's own `engWycliffe` USFM zip (ebible.org, which carries its own numbering); Forshall and Madden's 1850 edition on archive.org (no identifier found yet); check whether Bible SuperSearch has a module |
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
