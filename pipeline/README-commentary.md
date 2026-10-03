# The commentary layer (`data/commentary/`)

<!-- prov: 2026-10-03 drafted (Claude Code) · fable_review: pending -->

Four whole-Bible commentaries keyed to the KJV verse unit ids (`kjv:Gen.1.1`):
which verses each comment is on, and which verses it cites. Nothing is minted.
The ids are read from `data/uids/wordhoard.uids.json` and never written.

| work | comments | verses covered | citations | source |
|---|---|---|---|---|
| Matthew Henry, *Exposition* (1706-21) | 5,417 | 31,065 | 63,877 | CCEL |
| Jamieson, Fausset and Brown (1871) | 19,776 | 19,776 | 59,013 | CCEL |
| Matthew Poole, *Annotations* (1683-85) | 26,208 | 26,208 | 50,684 (+14,181 margin parallels) | EEBO-TCP, hand-keyed first edition |
| Albert Barnes, *Notes on the New Testament* | 7,947 | 7,947 | 39,573 | CCEL (keyed from Baker's 1949 reprint) |

```
python3 pipeline/build_commentary.py --fetch    # CCEL's texts, Poole's TCP files, the scans' OCR, all sha256-pinned
python3 pipeline/build_commentary.py            # build (~1 min)
python3 pipeline/build_commentary.py --check    # rebuild in memory: byte-identical to the committed files
python3 pipeline/build_commentary.py --collate  # CCEL's wording against the period printings -> collation.json
python3 pipeline/commentary.py kjv:John.3.16    # the comments on a verse, and the comments that cite it
python3 tests/commentary_test.py                # the reader's commentary rules, fixtures, the committed layer
```

Not taken here: Gill, Alford, Ellicott, Bengel and Keil-Delitzsch (the
archive.org pickups thread has them; Gill is on lane A's shelves). Adam
Clarke is not on CCEL; see section 6.

## 1. Rows

```json
{"id":"jfb:Gen.1.1","on":"kjv:Gen.1.1","anchor":"agrees","cites":["kjv:Ps.33.6","..."],"in_print":2}
{"id":"poole:Gen.1.1","on":"kjv:Gen.1.1","anchor":"agrees","cites":["kjv:Gen.2.1","..."],"parallels":[]}
```

- `id` is the work plus the passage the comment is on. A second comment on
  the same passage gets `~2`. These are citations, not uids.
- `on` is that passage: one verse, or a run (Henry comments on sections,
  `henry:Gen.1.1-2`; a chapter's introduction is on the whole chapter).
- `anchor` says whether a second reading of where the comment is agrees
  with the first (section 2).
- `cites` are the verses the comment cites, in the order it cites them.
- `parallels` (Poole only) are the parallel places printed in his margin.
- `in_print` counts the citations also found in a period printing (section 3).

## 2. Where a comment is: two readings

**CCEL (Henry, JFB, Barnes).** CCEL marks each comment with an empty
`<scripCom osisRef=.../>`. A comment runs from its mark to the next mark or
division. The second reading comes from the comment's own text, never the mark:

- Henry: the verse numbers printed in the passage he quotes, first and last.
- JFB: the verse number that opens the first lemma (`<b>13. pitieth</b>`).
- Barnes: the division's title ("Matthew 2:14").

| work | agrees | differs | unread |
|---|---|---|---|
| Henry | 4,232 | 19 | 1,166 |
| JFB | 16,604 | 4 | 3,168 |
| Barnes | 7,569 | 0 | 378 |

"Unread" is mostly a comment with no quoted passage or lemma to read.

**Poole.** His folio prints the KJV text with its verse numbers inline ("2. And
the Earth", "33 And every"). His notes sit at the foot of the page, each keyed
to a word of the verse. The parallel places are in the margin. A note belongs
to the verse whose number came before it. A chapter's numbers must read
2, 3, ... up to the KJV's last verse, in order:

- 1,119 chapters read in order.
- 20 are read **by order**. A misprinted number between two right ones is
  taken as the one between (Exodus 29 prints 36 twice). One chapter number is
  read the same way: Psalm 45 is headed "PSAL. LXV."
- 49 **differ**. A number is lost (1 Kings 17 has no "3"), so a few notes sit
  on the verse before. Their rows say `differs`.
- Leviticus 10-11: two pages are missing from the images TCP keyed. Nothing
  after the gap is placed, and 24 notes are dropped.

## 3. What a comment cites

**CCEL.** Each citation is voted as in `build_topical.py`. CCEL's own
`<scripRef>` tag is one reading. `topical_read.refs()` reading the displayed
text is the other. A citation is committed when both read it, or when one
does and a period printing does too.

The print check reads the archive.org OCR of open scans:

- Henry: the London 1828 edition, six volumes.
- JFB: the 1873 and 1879 one-volume printings.
- Barnes: the 1840 Gospels, two volumes. These are the only open volumes
  found, so only the Gospels are checked.

A citation counts as printed only where it falls in the same run, aligned in
order with GNU diff.

| work | both read it | found in print | CCEL only | found in print | reader only | found in print |
|---|---|---|---|---|---|---|
| Henry | 33,658 | 71.1% | 1,672 | 3.6% | 4,165 | 53.2% |
| JFB | 50,206 | 66.6% | 59 | 22.0% | 164 | 53.7% |
| Barnes (Gospels) | 11,890 | 48.1% | 78 | 11.5% | 80 | 31.3% |

The print figures count only citations that name their own book. "ver. 31"
has no book in print to align with. The figures are capped by OCR quality.
Barnes's are lower because CCEL rewrote his references ("Joh 3:16" for "John
iii. 16"), and the OCR reads the Roman chapters less well.

**Poole.** TCP transcribed the folio by hand, twice, from page images, and
marked every word it could not read (`<gap>`). There is no second text to vote
against. A citation is committed when it names a KJV verse and no unread word
touches it. 2,516 were dropped for touching one, and 671 name no KJV verse.
The reader handles his forms:

- 17th-century book names (`Psal.`, `Ioh.`, `Iob`, `Ier.`, `Matth.`).
  These are read only for Poole.
- A point for the colon ("Gen. 2. 1").
- "Chap. 3. 4" and "ver. 31" are read in the book named just before them
  ("as Luke tells us, ch. 1. 26"). Failing that, they take the chapter of a
  reference that ended within 40 characters in the same sentence ("Exod. 30.
  25. to verse 31"). Failing both, they take the comment's own place.

**An outside check for all four.** The Treasury of Scripture Knowledge
(`data/xrefs/tsk.jsonl`, read from its own 1830s scans) is compared with each
work's citations. How many does the Treasury also list at the same verse, and
how many at an unrelated verse, 1,000 verses on?

| work | in the Treasury at that verse | at an unrelated verse |
|---|---|---|
| Henry | 29.2% | 1.6% |
| JFB | 28.1% | 0.2% |
| Barnes | 34.3% | 0.2% |
| Poole, notes | 25.4% | 0.2% |
| Poole, margin parallels | 66.6% | 0.2% |

The check is a measure only. Nothing is kept or dropped by it. Henry's
unrelated-verse figure is higher because his comments span whole sections.

## 4. CCEL's print sources (the `ccel_print_source` rule)

Each CCEL file's `<printSourceInfo>` is recorded in the manifest. A year of
1930 or later sets `ccel_print_source_check`, as `fetch_shelf.py` does.

- **Barnes is flagged: "Grand Rapids, Mich.: Baker Book House, 1949."**
- Henry: "1706-1721. This version may be from the Revell edition."
- JFB: "1871".

## 5. Is CCEL's wording the period wording? (`--collate`, `collation.json`)

A fixed sample of 400 comments per work is found in the period scans, and 80
words of each are aligned word by word.

- **Barnes** agrees with the 1840 American printing word for word (91.4%,
  the rest OCR noise). There is no hath-to-has modernising. But CCEL
  spells -our where 1840 has -or (52 in the sample: honour, favour,
  neighbourhood). So Baker's 1949 reprint, and CCEL's text, follow a British
  edition, not the 1840 American one. CCEL also rewrote the references in
  modern abbreviations.
- **JFB** is edited. CCEL writes "namely" for "viz." (15), "that is" for
  "i.e.", "manuscripts" for "MSS", "while" for "whilst" and "among" for
  "amongst". It has American -or spellings where 1873 has -our (32). The
  words of the comments otherwise agree (90.7%).
- **Henry** is lightly modernised against the 1828 London edition (93.7%
  agreement). CCEL has towards for toward, you for ye, spoke for spake,
  afterwards for afterward, and show for shew. Most old forms are kept.

What this means for the layer: the committed rows hold places, not wording.
The prose in `build/commentary/` is CCEL's text, with the edits above. Before
anyone publishes that prose as Henry's, JFB's or Barnes's own words, it should
be collated against a period printing, or taken from one.

Poole's text is the first edition itself, in 17th-century spelling.

## 6. Adam Clarke

Clarke is not on CCEL: its paths return 404. sacred-texts refuses
(403). Open archive.org scans exist: the 1843 four-volume set
(`holybiblecontai01clar` to `04clar`), the 1846 set, and Google scans of
1836-37. Taking Clarke means OCR alignment like the Treasury's: verse heads
read from the scans, with two printings agreeing. It is not in this layer yet.

## 7. Not committed, not claimed

- **The prose.** It goes to `build/commentary/<work>.text.jsonl`, and
  `commentary.py`'s `text()` reads it there. All four are public domain;
  Poole's transcription is CC0. Committing prose is Adam's call.
- **A comment that differs** keeps its CCEL mark (or Poole's order) as `on`.
  The `anchor` field says so.
- **No citation comes from a scan alone.** The scans are a check.
