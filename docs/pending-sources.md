# Pending sources: historic English Bibles not yet on the shelf

<!-- prov: 2026-10-02 drafted (Claude Code); candidates found by web search, none opened -->

Sessions without archive.org access cannot fetch these Bibles. This file lists
them for a lane with full network access. **None of the candidates below has
been opened or checked.** Each still needs the standing rights check: read the
rights line of the exact edition before anything is fetched. Each also needs
a check that the text is a transcription, not page images.

| Bible | Why it is pending | Candidate archive.org items (unverified) |
|---|---|---|
| Coverdale (1535) | No machine-readable PD source was reachable from a cloud thread | `ENGCVD_DBS_HS` (Digital Bible Society, "English (1535) Coverdale Bible", likely text: **try first**); `CoverdaleBible1535_838`; `1535-coverdale-bible`; `coverdale-bible-1535`; `holyscriptures00cove` (a 19th-century reprint) |
| Bishops' Bible (1568) | Same as Coverdale | `ENGBSB_DBS_HS` ("Bishops Bible - NT (text)", NT only, likely text: **try first**); `1568TheBishopsBible`; `1568-bishops-bible`; `BibleBishops1568.ropt` |
| Tyndale, in full | The shelf's Tyndale (`fetch_sources.ENGLISH["tyndale"]`) holds ten books only | `1534-tyndale-nt`; `0410Tyndale1534NT` (1534 NT); `ThePentateuch` (Tyndale's Pentateuch); `tyndale-rogers-coverdale-bible-1526-1535-tyndale-translation-holy-scriptures` |
| Wycliffe (c.1395) | The one reachable PD copy (BibleNLP/ebible `eng-engWycliffe.txt`) holds the Pentateuch and Gospels only, in vref slots, and drops verses wherever the Vulgate's chapters run longer than the Hebrew's (Lev 6:24-30, Num 16:36-50) | eBible's own `engWycliffe` USFM zip (ebible.org, which carries its own numbering), or Forshall and Madden's 1850 edition on archive.org (no identifier found yet) |

## When one is fetched

1. Pin it: commit or item identifier, file name, and sha256, in
   `fetch_sources.ENGLISH` or its own dict.
2. Record the rights line as read.
3. If it is USFM, read it with `brenton_verses` and `brenton_text` (eBible's
   markup). If it is plain text, write a converter in the same pattern.
4. Add its map with `build_english_versification.py`. Note that this builder
   assumes the KJV verse grid. A source with its own numbering (eBible USFM)
   keeps that numbering. Then the alignment carries the whole map, as it does
   for the Geneva's Hebrew-numbered chapters.
5. Add its column to `build_parallel_index.py`.

Search results that led here:
- [Coverdale Bible, 1535 (CoverdaleBible1535_838)](https://archive.org/details/CoverdaleBible1535_838)
- [1535 Coverdale Bible](https://archive.org/details/1535-coverdale-bible)
- [English (1535) Coverdale Bible](https://archive.org/details/ENGCVD_DBS_HS)
- [Coverdale Bible (1535)](https://archive.org/details/coverdale-bible-1535)
- [Tyndale Rogers Coverdale Bible 1526-1535](https://archive.org/details/tyndale-rogers-coverdale-bible-1526-1535-tyndale-translation-holy-scriptures)
- [The Holy Scriptures (Coverdale)](https://archive.org/details/holyscriptures00cove)
- [1534 Tyndale New Testament](https://archive.org/details/1534-tyndale-nt)
- [1534 Tyndale New Testament (0410Tyndale1534NT)](https://archive.org/details/0410Tyndale1534NT)
- [The Pentateuch (Tyndale)](https://archive.org/details/ThePentateuch)
- [1568 The Bishop's Bible](https://archive.org/details/1568TheBishopsBible)
- [English (1568) Bishops Bible - NT (text)](https://archive.org/details/ENGBSB_DBS_HS)
- [1568 Bishop's Bible](https://archive.org/details/1568-bishops-bible)
- [Bible Bishop's 1568](https://archive.org/details/BibleBishops1568.ropt)
