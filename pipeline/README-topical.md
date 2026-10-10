# The topical and dictionary layer (`data/topical/`)

<!-- prov: 2026-10-03 drafted (Claude Code) · fable_review: pending -->

Four public-domain reference books keyed to the KJV verse unit ids
(`kjv:Gen.1.1`). Hitchcock's names are joined to their entries. Nothing is
minted: the ids are read from `data/uids/wordhoard.uids.json` and never written.

| book | entries | references committed | also found in print |
|---|---|---|---|
| Nave's Topical Bible (1896/97) | 5,322 (22,259 subtopics) | 77,848 | 83.5% |
| Torrey's New Topical Text Book (1897) | 623 (21,544 subtopics) | 38,543 | 94.4% |
| Easton's Bible Dictionary (1893/1897) | 3,964 | 23,414 | 93.5% |
| Smith's Bible Dictionary (Peloubet, 1884) | 4,561 | 10,415 | 87.0% |

```
python3 pipeline/build_topical.py --fetch   # CCEL's four texts + five scans' OCR, sha256-pinned (~60 MB into data/corpus/topical/)
python3 pipeline/build_topical.py           # build (~2 min)
python3 pipeline/build_topical.py --check   # rebuild in memory: byte-identical to the committed files
python3 pipeline/topical.py kjv:John.3.16   # every place in the four books that cites a verse
python3 tests/topical_test.py               # the reader rule by rule; the committed layer
```

## 1. Rows

Nave's and Torrey's keep their outline:

```json
{"id":"nave:adoption","term":"ADOPTION","see":["GOD, FATHERHOOD OF", "..."],
 "topics":[{"path":["OF CHILDREN. INSTANCES OF","Of Moses"],
            "refs":["kjv:Exod.2.5-10","kjv:Acts.7.21","kjv:Heb.11.24"],"in_print":3}, "..."]}
```

The dictionaries give an entry's references in the order the article cites them:

```json
{"id":"easton:abdon","term":"Abdon","refs":["kjv:Judg.12.13-15","kjv:1Sam.12.11","..."],
 "in_print":9,"hitchcock":"a-p0.22"}
```

The fields:

- `id` is the book plus a slug of the headword. A repeated headword gets `~2`,
  and so on. These are citations, not uids.
- References use the same forms as `data/xrefs/`. A whole chapter is written
  as its first to its last verse.
- `in_print` counts how many of a place's references the printed scans were
  found to carry (section 3).
- `apocrypha` holds Apocrypha references as the source gave them. Esther 10:4
  and on, and Daniel 13-14, are the Greek additions in the Vulgate's
  numbering, so they go here and are never turned into `kjv:` ids.
- `hitchcock` is the entry id in Hitchcock's Bible Names. It is set only where
  the headword is a Hitchcock headword, letter for letter.

## 2. Sources

All four come from the Christian Classics Ethereal Library's ThML. Each file
is pinned by sha256, and its rights line is copied into the manifest:

- Easton's and Smith's files say "Public Domain".
- Nave's and Torrey's files leave the rights field empty. Both books were
  printed in 1896-97, and both authors died before 1931.
- Nave's header carries a stray template line, "(tr. William Whiston)". It is
  not about this book.

**Smith's is the 1884 one-volume revision by F. N. and M. A. Peloubet, not
the 1860-63 three-volume dictionary.** The two editions have to be told apart
because their references are written differently. Peloubet's references are
arabic, and they match CCEL's text 82% of the time. The 1880 large edition
writes chapters in Roman numerals ("Gen. iv. 2"): this reader got 179
references from its whole scan, so it cannot be used to check CCEL. The full
1863 dictionary would be a separate book to OCR, from open archive.org scans
such as `dictionaryofbibl1863smit`.

**CCEL's Nave is not the 1897 wording, word for word.** A modern digital
editor added glosses and modernized some words:

- `ASS (DONKEY)`, "bronze" for "brass", "yeast", "Malta", and Greek words
  ("ekklesia", "diakonos", "monogenes").

CCEL's Torrey is in British spelling ("honour", "characterised"). The rows
mark this where it can be seen:

- A heading with a word that appears in neither printed scan carries
  `wording_not_in_print` with those words. That is 877 of 27,581 Nave
  headings, and 562 of 22,167 for Torrey, nearly all spellings.
- The references are what counts. In Nave, only 394 of 22,259 subtopics have
  no reference at all that is also found in print.

## 3. Three readings of every reference

1. **CCEL's tag.** CCEL wraps each reference in `<scripRef osisRef=...>`.
2. **The reader.** `topical_read.refs()` reads the displayed text with no
   help from the tag. It handles the forms these books use:
   - abbreviations, and the OCR's variants of them;
   - a book that carries over a `;` or a `,`;
   - whole chapters (`Jer 21; 22`);
   - chapter ranges and ranges across chapters;
   - the single-chapter books (`Jude 9`, `Jude 1:9`, `Jude 6; 14`);
   - lists of chapters (`Ps. 23, 24`);
   - ordinals (`1Jo`, `II Sam.`, `3 Macc.`), and Susanna and Bel;
   - a psalm's title (`Ps. 18, title`, `Ps. 51:title`) is no reference:
     the KJV does not number titles;
   - a number with a book after it is that book's ordinal, not a chapter of
     the book before: "Eph. 2:15; 2 Tim. 1:10", and in the old Roman form
     "1 Chr. 25:1, 2 Chr. 20:14" (read wrongly as 1 Chronicles 2 before
     2026-10-10; fixing it raised every book's share found in print);
   - `Is`, `Am`, `So`, `Ex` and `Re` before a bare number and then a word
     (`Is 40 days`) are prose, not books. Nave's `Ex 32;` still reads.
3. **Print.** The archive.org OCR of open scans of the printed books is read
   by the same reader:
   - Nave's: the 1897 and 1903 printings.
   - Torrey's: two copies of the 1897 Revell printing.
   - Easton's: the 1893 first edition, the only open scan.
   - Smith's: the 1884 Peloubet.

   The print readings are then **aligned** in order against the book's with
   GNU diff. So a reference counts as printed only where it falls in the same
   run, not merely somewhere in the book.

A reference is committed when two of the three readings agree. That means CCEL
and the reader together, or either one of them together with print. A
reference only one reading has goes to `build/topical/<book>.rejected.jsonl`.

What the vote catches (the manifest's `by_reading`):

| book | both | found in print | CCEL only | found in print | reader only | found in print |
|---|---|---|---|---|---|---|
| Nave | 77,643 | 83.4% | 291 | 2.4% | 371 | 84.4% |
| Torrey | 38,436 | 94.3% | 136 | 0% | 142 | 77.5% |
| Easton | 23,491 | 93.3% | 152 | 2.6% | 695 | 90.7% |
| Smith | 10,865 | 85.7% | 151 | 46.4% | 112 | 68.8% |

References that only CCEL tagged are mostly tagger errors, and print says so.
The commonest is `Jude 1:9` tagged as `Jude 1` (verse 1), with the `:9` left
untagged. References only the reader found are mostly real references CCEL
missed, and print confirms them. Smith's CCEL-only references are the
exception: half are in print, so there the reader still misses forms Smith
uses (the vote keeps those only where print has them).

The "found in print" figures are not a measure of error. They are capped by
OCR quality: the OCR writes `Ley.` for Lev. and `18:138` for 18:13. Nave's
1897 printing also quotes many verses in full, and the OCR breaks some of
those references up. Two scans of one book help here: Torrey's two copies
together reach 94%.

Last, every reference must name a KJV verse or chapter:

- 108 do not and are dropped (`names no KJV verse`). Most are typos in the
  source, such as Smith's "1 Chronicles 7:88" and Easton's "Jer. 38:60".
- 178 are the Apocrypha, kept under `apocrypha`.

## 4. Hitchcock

Hitchcock's Bible Names has no scripture references: CCEL's file has none.
Its 2,623 names are already pinned by `proper_names.py`, so this layer adds no
copy of them. Instead, each entry here whose headword is a Hitchcock headword
carries his entry id:

- 2,326 Nave entries;
- 1,768 Easton entries;
- 2,239 Smith entries;
- 12 Torrey entries.

A verse therefore reaches a name's meaning through the entry that cites the
verse.

## 5. Not committed, not claimed

- **The dictionaries' prose** (Easton's and Smith's articles) is not
  committed. `build_topical.py` writes it to `build/topical/<book>.text.jsonl`,
  and `topical.py`'s `text()` reads it there. The text is public domain, and
  CCEL's files say so. Committing it is Adam's call.
- **Headings are CCEL's.** Nave's carry its modern glosses, as section 2 says.
- **`see` is a cross-reference to another topic,** given as the heading names
  it. It is not resolved to a row id.
- **The scans are only a check.** No reference comes from the scans alone.
