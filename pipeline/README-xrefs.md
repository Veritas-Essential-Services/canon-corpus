# The cross-reference layer (`data/xrefs/`)

<!-- prov: 2026-10-03 drafted (Claude Code) · fable_review: pending -->

For every KJV verse, the passages that bear on it, keyed on the KJV verse unit
ids (`kjv:Gen.1.1`), the key the whole suite already shares. Nothing is minted:
the ids are the ones in `data/uids/wordhoard.uids.json`, read and never written.

| layer | what | where | committed? |
|---|---|---|---|
| **tsk** | the *Treasury of Scripture Knowledge*, verse by verse | `data/xrefs/tsk.jsonl` | yes: public domain |
| **cited_by** | every verse's citers: the Treasury both ways, the fathers' editors' notes (PR #7), the catenae, every built book's links to a verse | `build/xrefs/cited-by.jsonl` | no: built from CC BY-SA editions, like PR #7's links; counts + sha256 in the manifest |

```
python3 pipeline/build_xrefs.py --fetch     # the two scans, sha256-pinned (~1.2 GB into data/corpus/tsk/)
python3 pipeline/build_xrefs.py             # build (~15 min first time; stages cached in build/xrefs/, keyed by the code that made them)
python3 pipeline/build_xrefs.py --check     # rebuild tsk.jsonl in memory: byte-identical to the committed file
python3 pipeline/xrefs.py kjv:John.1.1      # look a verse up
python3 tests/xrefs_test.py                 # offline: the reader rule by rule, then the committed files
```

For the fathers: build PR #7's `build/fathers/scripture-links.jsonl` and the
books first (`tag_fathers.py`), or point `--fathers-links` / `--books` at a
checkout that has them.

## 1. Rows

```json
{"verse":"kjv:Gen.1.1",
 "groups":[{"kw":"beginning","refs":["kjv:Prov.8.22-24","kjv:Prov.16.4","kjv:Mark.13.19", "..."]},
           {"kw":"God","refs":["kjv:Exod.20.11","..."]}],
 "placed":["..."], "unsure_digit":["..."]}
```

A reference is `kjv:Book.c.v`, `kjv:Book.c.v-v2` (same chapter) or
`kjv:Book.c.v-c2.v2`; a whole chapter is written as its first to last verse.
`kw` is the Treasury's catchword (the word of the verse the references
gloss) as the OCR read it, uncorrected. `placed` and `unsure_digit` mark
references that are in `groups` but stand on less (section 4).

## 2. Reading a scan (`tsk_layout.py`, `tsk_read.py`)

The source is the Internet Archive's own character OCR (`_chocr.html.gz`,
tesseract 5) of two scans. Not the plain-text OCR: that reads some lines
straight across the gutter. Each page's gutter is found from the ink, every
line is cut at it, and the left column is read before the right.

**Which verse an entry belongs to is an alignment, not a walk.** A walk (keep
the current chapter, take the next number) loses its place at the first
misread verse number and never finds it again. Instead every line that opens
with a number, and every `CHAP. XII.` / `PSALM XXIII.`, is offered every
verse that number (or a confused reading of it: 8/3, 9/2, 1/4/7, 6/5) could
be, inside the window its page's running head allows (the head's chapter,
less three, to the next head's, plus one); the best chain through the KJV
order wins. A number read as printed scores 4, a confused one 2.5, a line
like `1 Ki. 4. 33.` (a book, not a verse) 1; each verse passed over costs
0.35 and a jump of more than 40 verses 8. A misread number then costs one
entry, not every entry after it.

**References**: an abbreviation (the Treasury's own: `Ge. Ex. … Jno. … Re.`,
plus the forms the OCR makes of them: `Hx.` for Ex., `Ee.` for Ec.), `ch.`
(this book) or `ver.` (this chapter); then chapter.verse, verse lists with
commas, ranges with a dash, more chapters after a semicolon. The OCR's comma
for the point (`Ex. 20, 11`) is read as the point. `Heb.` before a word is
"Hebrew" (a marginal reading), not Hebrews. The chronology (`A.M. 2093.
B.C. 1911.`) is not a reference. An abbreviation two books share in the OCR
(`Jo.`: Josh. or Je.) gives a reference only if exactly one of them has the
verse.

## 3. The 3 that reads as 8 (`tsk_glyphs.py`)

The face's 3 has a round, nearly closed top, and tesseract reads it as 8 most
of the time; two scans of the same plates make the same mistake. Every 3 and 8
inside a reference is cropped from the page image again and a small network
calls it. **Its labels come from the Bible's shape alone:** in a reference
with one 3/8, if the reading as printed names no KJV verse (`Ps. 184.3`) and
the swapped one does, the swap is the label; if the swap names none and the
reading does, the reading is. OpenBible.info is never a label.

76,900 glyphs are labelled that way across the two scans (70,525 of them 3s).
Held out (one in five), the network agrees with 99.1% of the labels; it is
sure (p >= 0.9 either way) of 97.8% of glyphs and right on 99.5% of those.
A glyph it is not sure of keeps the OCR's reading, and the reference is
marked `unsure` in that scan.

What it changed, measured against OpenBible (section 6), on the Revell scan:

| references containing | before | after |
|---|---|---|
| an "8" | 55.5% | 84.9% |
| neither 3 nor 8 | 83.4% | 83.4% |
| all | 75.6% | 83.8% |

So after the re-reading, references with an 8 match as often as references
with no 3 or 8 at all: the digit error is gone, not just reduced.

**Where an error would hide.** The labels come only from references where one
reading names a verse and the other does not, and nine in ten of them are 3s.
In 74,844 committed references (30%), some 3 or 8 swapped names a verse too:
there the Bible's shape cannot tell, only the model chose, and the two scans
agreeing adds little because both go through the same model. `--measure`
scores those ("3/8, shape blind") apart from the ones shape confirms ("3/8,
shape tells") and from "no-3/8". If "shape blind" matches OpenBible as often as
"no-3/8", the model is not hiding errors there. The scan's
OCR read 79,831 printed 3s as 8s; 17 corrections went the other way.

## 4. Two scans, and what is committed

Both scans are read independently, then:

- **agreed**: both read the reference under the same verse. Committed.
- **placed**: both read it, under verses at most 6 apart, and one scan has no
  entry at the later verse while the other has. The first scan missed the
  entry line, so the later verse's references ran on under the verse before.
  Committed at the later verse and listed in `placed`. Measured: where one
  scan lacks the later entry, the later verse is OpenBible's verse 84-90% of
  the time, the earlier 4%.
- **unsure_digit**: agreed, but both scans kept the OCR's 3/8 because the
  model could not call it; committed and listed.
- **one scan only**: not committed. In `build/xrefs/tsk-one-scan.jsonl`,
  counted in the manifest. Most are misreadings of a reference the other scan
  read rightly, or entries one alignment missed.

The first build (2026-10-03):

| | references | also in OpenBible |
|---|---|---|
| **committed** | **248,416** on 25,622 verses | **94.0%** |
| of which agreed (the manifest's `agreed`, 227,774, includes unsure_digit) | 226,736 | 94.6% |
| of which placed | 20,642 | 87.9% |
| of which unsure_digit | 1,038 | 80.4% |
| one scan only (not committed) | 122,369 | 55.9% |

The jump from about 84% for either scan alone to 94.6% for what both read
is the point of reading two scans. Each scan aligned about 26,000 entries
(Revell 25,865; Bagster 26,321) and read about 330,000 references; 5% of
those name no KJV verse (`unresolved` in the manifest) and are dropped.

## 5. The fathers and the books (`cited_by`)

Every link PR #7 resolved from the fathers' editors' notes
(`build/fathers/scripture-links.jsonl`: unit to KJV verse, with its rule,
including `alt_target`'s main reading only), every catena comment
`place_catena.py` placed on its verse, and every other built book unit whose
links name a `kjv:` verse (the CCEL scripRef harvest), reversed into one index
with the Treasury, both ways.

The first build covers 30,920 verses with 507,860 citations:

- 442,557 from the Treasury, both ways, with a range counted once per verse;
- 60,896 from the fathers' notes. That is every link PR #7's head resolves
  (13,393 Greek and 47,503 Latin). PR #7's committed manifest says 60,903
  because it predates the head's three-numbering change;
- 4,407 from book links, almost all the catenae.

The fathers' links were built from PR #7's head (fbb3bd1); their sha256 is in
the manifest. **The fathers' Old Testament citations are provisional:** a
review of #7 found 30 of 64 checked OT links off (footnote line numbers read
as verses, numbering misjudged, "et" and dashes misparsed), so each carries
`"provisional": true` until #7 is fixed. Rerunning is one command once it is:
`tag_fathers.py`, then `build_xrefs.py` (the Treasury stages are cached), then
drop `OT_BOOKS` in build_xrefs.py.

## 6. How it was measured

OpenBible.info's cross-reference set (CC BY, 344,799 rows, seeded from the
Treasury and voted on since) is an independent machine-readable relative of
the Treasury. `--measure` reports the share of committed references it also
lists for the verse. It is not the Treasury and does not contain all of it, so
the ceiling is below 100%; what matters is the comparison between classes.
It is read for measuring only: it is never an input, a label, or a tiebreak,
and nothing from it is written anywhere.

## 7. Not claimed

- Only references both scans attest are committed.
- A catchword is OCR text.
- The Treasury's notes (marginal readings, renderings from the Hebrew,
  chronology) are not taken.
- A verse the Treasury has no entry for, or whose entry neither alignment
  found, has no row.
- The other Treasury scans on archive.org are lending-library items and are
  not used. A third open scan, which would let a reference one scan read
  stand on a 2-of-3 vote, was looked for on 2026-10-03 and not found:
  archive.org's other five copies are all lending-only (1967, 1970, 1982,
  and the 1992 *New Treasury*, a different book); its SwordSearcher plugin
  is a module rip; Bagster's 1843 *Comprehensive Bible* (Google scan) is
  the Treasury's ancestor, not the Treasury, so its references would not
  vote on the same text; HathiTrust holds none of the Treasury's OCLC
  numbers that Open Library lists, and its search refused this network.
  Google Books' API was over its daily quota.
