# The commentary layer (`data/commentary/`)

<!-- prov: 2026-10-03 drafted (Claude Code) · fable_review: pending -->

Ten commentaries keyed to the KJV verse unit ids (`kjv:Gen.1.1`):
which verses each comment is on, and which verses it cites. Nothing is minted.
The ids are read from `data/uids/wordhoard.uids.json` and never written.

| work | comments | verses covered | citations | source |
|---|---|---|---|---|
| Matthew Henry, *Exposition* (1706-21) | 5,417 | 31,065 | 64,108 | CCEL |
| Jamieson, Fausset and Brown (1871) | 19,776 | 19,776 | 59,019 | CCEL |
| Matthew Poole, *Annotations* (1683-85) | 26,208 | 26,208 | 55,433 (+16,020 margin parallels) | EEBO-TCP, hand-keyed first edition |
| Albert Barnes, *Notes on the New Testament* | 7,947 | 7,947 | 39,586 | CCEL (keyed from Baker's 1949 reprint) |
| John Wesley, *Explanatory Notes* (1755-66) | 19,073 | 28,160 | 3,151 | CCEL |
| John Calvin, *Commentaries* (CTS English, 1843-55) | 14,041 | 16,363 | 17,102 | CCEL, 45 volumes |
| Charles Hodge, *Ephesians* (1856) | 146 | 154 | 676 | CCEL |
| Thomas Manton, *James* and *Jude* (1651-58) | 122 | 132 | 5,344 | CCEL (Nisbet, 1871) |
| John Trapp, *Commentary* (1647-60), five volumes | 14,699 | 14,662 | 34,557 (+3,776 margin) | EEBO-TCP, hand-keyed first editions |
| Adam Clarke, *Commentary* (1810-26) | 18,129 | 18,129 | 9,163 | archive.org OCR of two printings of each Testament |
| C. H. Spurgeon, *Treasury of David*, the Exposition (1869-85) | 2,324 | 2,324 | 132 | archive.org OCR of two printings |
| Charles Hodge, *Romans* (revised, 1864) | 336 | 336 | 1,743 | archive.org OCR of two printings |
| Charles Hodge, *1 and 2 Corinthians* (1857, 1860) | 470 | 470 | 1,198 | archive.org OCR of two printings of each |
| Robert Haldane, *Romans* | 407 | 407 | 470 | archive.org OCR of two printings |
| John Brown of Edinburgh, *Hebrews* (1862) | 37 | 37 | 451 | archive.org OCR of two copies of one printing |
| John Brown of Edinburgh, *1 Peter* (discourses) | 26 | 26 | 1,060 | archive.org OCR of two printings |

```
python3 pipeline/build_commentary.py --fetch    # CCEL's texts, Poole's TCP files, the scans' OCR, all sha256-pinned
python3 pipeline/build_commentary.py            # build (~2 min; Clarke also needs data/corpus/kjv_bible.txt)
python3 pipeline/build_commentary.py --check    # rebuild in memory: byte-identical to the committed files
python3 pipeline/build_commentary.py --collate  # CCEL's wording against the period printings -> collation.json
python3 pipeline/commentary.py kjv:John.3.16    # the comments on a verse, and the comments that cite it
python3 tests/commentary_test.py                # the reader's commentary rules, fixtures, the committed layer
```

Not taken here: Alford, Ellicott, Bengel and Keil-Delitzsch (the
archive.org pickups thread, PR #11, has them). **Gill is not taken.** No keyed
text exists. The open scans are scattered 18th-century volumes in long-s type
(1758-65 Old Testament, an 1811 New Testament volume) with no second
printing to vote against, and the complete uploads are modern retypings with
no library provenance. Lane A's `gill_shelf.json` reached the same finding.

## 1. Rows

```json
{"id":"jfb:Gen.1.1","on":"kjv:Gen.1.1","anchor":"agrees","cites":["kjv:Ps.33.6","..."],"in_print":2}
{"id":"poole:Gen.1.1","on":"kjv:Gen.1.1","anchor":"agrees","cites":["kjv:Gen.2.1","..."],"parallels":[]}
{"id":"clarke:Acts.7.42","on":"kjv:Acts.7.42","anchor":"both printings","cites":["kjv:Amos.5.25"]}
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
- Calvin: the verse number that opens the comment (`<b>12.</b> <i>And Jesus
  entered</i>`), in the mark's chapter.
- Hodge and Manton: the verse number that opens the comment ("V. 2.", "Ver.
  2."), in the mark's chapter.
- Wesley: CCEL marks only the chapter. Each note opens with its verse number
  ("5. And he opened his mouth - A phrase ..."), so the notes are split there.
  The second reading is the lemma, the words before " - ", looked for in the
  KJV verse the number names (`agrees` when half its words are there).

| work | agrees | differs | unread |
|---|---|---|---|
| Henry | 4,232 | 19 | 1,166 |
| JFB | 16,604 | 4 | 3,168 |
| Barnes | 7,569 | 0 | 378 |
| Wesley | 9,870 | 213 | 8,990 |
| Calvin | 10,334 | 134 | 3,573 |
| Hodge | 132 | 0 | 14 |
| Manton | 117 | 0 | 5 |

"Unread" is mostly a comment with no quoted passage or lemma to read. Wesley's
New Testament notes quote his own revision of the text, so many lemmas there
do not match the KJV's words and are unread.

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

Wesley and Calvin have no print check yet, so only citations both readings
agree on are committed. Wesley loses most: CCEL's tagger reads none of his
"ver. 3" references and only the first of "Acts xviii, 1, 2". 5,593
references only the reader found go to `build/commentary/wesley.rejected.jsonl`
(5,313 of them in the note's own chapter). Wesley prints "Luke iii, 31", a
comma after the Roman chapter, which the reader takes only for him
(`roman_comma`).

Hodge writes "Heb. 13, 9", a comma for the colon. The reader takes that only
for him (`comma`), since elsewhere "Ps. 23, 24" is two psalms.

Calvin's CTS volumes carry the translators' footnotes (French readings,
cross-references). They are the editors' words, not Calvin's, so they are
cut before his citations are read and are not in his prose.

| work | both read it | found in print | CCEL only | found in print | reader only | found in print |
|---|---|---|---|---|---|---|
| Henry | 33,686 | 71.0% | 1,644 | 3.6% | 4,140 | 53.7% |
| JFB | 50,207 | 66.6% | 58 | 5.2% | 174 | 59.8% |
| Barnes (Gospels) | 11,890 | 48.1% | 78 | 11.5% | 84 | 29.8% |

The print figures count only citations that name their own book. "ver. 31"
has no book in print to align with. The figures are capped by OCR quality.
Barnes's are lower because CCEL rewrote his references ("Joh 3:16" for "John
iii. 16"), and the OCR reads the Roman chapters less well.

**Poole.** TCP transcribed the folio by hand, twice, from page images, and
marked every word it could not read (`<gap>`). There is no second text to vote
against. A citation is committed when it names a KJV verse and no unread word
touches it. 2,667 were dropped for touching one, and 697 name no KJV verse.
The reader handles his forms:

- 17th-century book names (`Psal.`, `Ioh.`, `Iob`, `Ier.`, `Matth.`).
  These are read only for Poole.
- A point for the colon ("Gen. 2. 1").
- "Chap. 3. 4" and "ver. 31" are read in the book named just before them
  ("as Luke tells us, ch. 1. 26"). Failing that, they take the chapter of a
  reference that ended within 40 characters in the same sentence ("Exod. 30.
  25. to verse 31"). Failing both, they take the comment's own place. A
  "Chap." never borrows the last reference's book: "Gal. 6. 5. Chap. 20. 12"
  in a note on Revelation is Revelation 20:12. Only a spelled-out name
  counts without its point, so "as Philip had done" names no book.
- A point closes each reference ("chap. 7. 34. & 25. 10."), and the book
  carries over it.
- A psalm's title ("Psal. 18. title") is no reference, as in the topical layer.

**Trapp.** TCP keyed five volumes of the first editions (1647-60) by hand:
the Gospels to Luke, the Epistles and Revelation, Ezra to Psalms, the Minor
Prophets, and Proverbs to Daniel. TCP's copy lacks John, Acts, the Pentateuch
and the histories. Trapp does not print the Bible text. Each note opens a
paragraph with its verse and lemma ("Verse 3. Concerning his Son] Here's a
lofty ..."), and verse 1 stands in the chapter head. So a note's place is read
twice: the printed number, and the lemma looked for in the KJV verse it names,
with the spelling levelled (long s, u/v, i/j, a final e). 14,190 agree, 32
differ and 477 are unread. A number that runs backwards is not read (110),
and a head printed twice is read as one (31). Citations are read once, as
Poole's are, and dropped next to an unread word (654). The margin, mostly his
sources ("Chemnit. Exam."), is kept apart as `parallels`.

**An outside check.** The Treasury of Scripture Knowledge
(`data/xrefs/tsk.jsonl`, read from its own 1830s scans) is compared with each
work's citations. How many does the Treasury also list at the same verse, and
how many at an unrelated verse, 1,000 verses on?

| work | in the Treasury at that verse | at an unrelated verse |
|---|---|---|
| Henry | 29.2% | 1.6% |
| JFB | 28.1% | 0.2% |
| Barnes | 34.3% | 0.2% |
| Poole, notes | 24.9% | 0.2% |
| Poole, margin parallels | 68.0% | 0.2% |
| Wesley | 45.1% | 0.1% |
| Calvin | 14.2% | 0.2% |
| Hodge | 10.6% | 0.4% |
| Manton | 6.2% | 0.1% |
| Trapp, notes | 15.0% | 0.2% |
| Clarke | 23.0% | 0.23% |
| Spurgeon | 5.5% | 0.0% (of 55) |
| Hodge, Romans | 12.1% | 0.1% |
| Hodge, Corinthians | 23.2% | 0.7% |
| Haldane | 11.6% | 0.0% |
| Brown, Hebrews | 4.9% | 0.5% |
| Brown, 1 Peter | 4.4% | 0.1% |

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

## 6. Adam Clarke (`clarke_read.py`)

Clarke is on no keyed site: CCEL has no Clarke (404), and sacred-texts
refuses (403). So both readings come from the OCR of open archive.org scans,
two printings of each Testament:

| | first printing | second printing |
|---|---|---|
| Old Testament | New York, Lane & Sandford, 1843, four volumes | New York, Lane & Tippett, 1846, four volumes |
| New Testament | New York, Lane & Tippett, 1846, two volumes | New York, P. D. Myers, 1835, one volume |

The 1843 and 1846 Old Testaments are very likely the same stereotype plates.
Their agreement mostly removes OCR error, not editorial difference. The two
New Testaments are set differently.

Not taken: the 1883-84 Phillips & Hunt New Testament. It is Daniel Curry's
revision, not Clarke's words.

**The page.** The KJV text, its margin and its chronology are at the top,
and Clarke's notes are below. The OCR runs them together, so a note's text is
interleaved with Bible text and margin. Each chapter's notes open with
"NOTES ON CHAP. IV." (or "NOTES ON PSALM XXIII.", or "NOTES.--" in 1835).

**Where a note is.** A note opens with a head: "Verse 17. The priests--stood
firm on dry ground]" (in 1835, the bare number). The note headings cut the
notes into runs. A run is cut again where its verse numbers fall back to 1-3,
which marks a heading the OCR lost. The runs are then aligned in order to the
volume's chapters by dynamic programming. A run scores, for a chapter, how
far its lemmas' words are in the KJV verses its heads name. It gains a bonus
when the heading's Roman numeral, read through its OCR confusions (H for II),
names that chapter.

A head is placed when at least half of its lemma's words (two or more, of 3+
letters) are in the KJV verse it names:

| | heads | placed | chapters found |
|---|---|---|---|
| OT 1843 | 11,534 | 10,695 | 927 of 929 |
| OT 1846 | 11,047 | 10,133 | 924 of 929 |
| NT 1846 | 6,232 | 5,645 | 260 of 260 |
| NT 1835 | 5,633 | 4,803 | 255 of 260 |

A row is written for every verse either printing places: 13,065 placed in
both (`anchor: "both printings"`) and 5,064 in one (`"one printing"`).

**What a note cites.** The text runs from the head to the next head, cut at
the next chapter, and is read paragraph by paragraph. These paragraphs are
dropped:

- the chronology margin and page feet (11,496);
- the Bible text, where half of its word pairs are in this chapter's KJV or
  the next one's (63,405);
- the margin's references (34,276). These are letter-marked references,
  "Or," and "Heb." glosses, or a run of references with no prose in it.

`topical_read.refs()` reads what is left, with Clarke's forms: lower-case
Roman chapters, and "ver. 10" and "chap. iii. 17" read in the note's own book
and chapter. Two kinds of reading are not kept:

- "ver. 407" just after a classical work ("Iliad i., ver. 407"). That is
  Homer's line, not a verse.
- A citation of the note's own verse (471).

**A citation is committed only when both printings read it in their notes on
the same verse.** 9,163 are. 14,992 are read in one printing only. They go to
`build/commentary/clarke.rejected.jsonl`, with the printing that read them.

The Treasury check (section 3) puts Clarke's citations near Poole's notes:
23.0% at that verse, 0.23% at an unrelated one.

**What it is not.** The head placement and the citations are only as good as
the OCR and these rules. A Bible-text or margin paragraph the rules miss is
read as the note's. The two-printing vote catches that in the New Testament,
where the pages are set differently. In the Old Testament it catches it less
well, because the plates are the same. The prose in
`build/commentary/clarke.text.jsonl` is unproofread OCR of the printing
named, and its rows say so.

## 7. Spurgeon's Treasury of David (`spurgeon_read.py`)

CCEL's *Treasury of David* is page images only: its XML holds no text. So,
as with Clarke, both readings come from the OCR of open archive.org scans,
of two printings set apart:

- London, Marshall Brothers, six volumes (`thetreasuryofdav01spuruoft` and
  on);
- New York, Funk & Wagnalls, seven volumes (`treasuryofdavid0001chsp` and
  on).

**Only the Exposition is read.** Each psalm has Spurgeon's own Exposition,
then "Explanatory Notes and Quaint Sayings" (other writers, quoted, each
headed "Verse 1.--"), then "Hints to the Village Preacher". The notes are
other authors' words and are left for a later pass. An Exposition runs from
its heading ("EXPOSITION.", "EXPOSITION,", or Psalm 119's "EXPOSITION OF
VERSES i TO 8.") to the first notes heading, "Verse N.--" line, hints
heading, next psalm, or next Exposition.

**Where a comment is.**

1. The Expositions are aligned in order to the volume's psalms by dynamic
   programming. An Exposition scores, for a psalm, how far its printed verse
   lines ("2 He maketh me to lie down ...") are in the KJV verses their
   numbers name. Psalm 119 may take one Exposition per section. London places
   all 150 psalms; New York 145 (its OCR loses the heading of Psalms 15, 96,
   105, 130 and 144).
2. The printed verse lines are grouped. Of the candidate lines, the chain
   with rising numbers that scores highest is kept, so one stray numbered
   line cannot shut out the rest.
3. The comment after a group is on the group. Where Spurgeon numbers his
   comments ("2. “He maketh me to lie down ...”"), each number opens a
   comment on that verse (or "4, 5." on both). A number is read as a head
   only when it is past every verse already commented on and not past the
   group's last verse. So a page or footnote number is never a head.

A row is written for every verse either printing places: 1,986 placed in
both (`anchor: "both printings"`) and 338 in one.

**What a comment cites.** The Exposition quotes Scripture far more than it
cites it by chapter and verse, so citations are few. `topical_read.refs()`
reads them with Roman chapters and "ver. 5" in the psalm. A citation is
committed only when both printings read it on the same verse: 132 are, and
101 are read in one printing only (`build/commentary/spurgeon.rejected.jsonl`).
Spurgeon's citations are mostly other verses of the same psalm, which the
Treasury of Scripture Knowledge rarely lists: hence its low Treasury figure.

**What it is not.** The prose in `build/commentary/spurgeon.text.jsonl` is
unproofread OCR of the printing named.

## 8. Hodge, Haldane and John Brown (`single_read.py`)

These are commentaries on one book that no library has keyed. CCEL has only
Hodge's *Ephesians*, which section 2 reads. So, as with Clarke and Spurgeon,
both readings come from the OCR of open archive.org scans, and a citation is
committed only when both read it on the same verse:

| work | first printing | second printing |
|---|---|---|
| Hodge, *Romans* | Philadelphia, Martien, 1864 | New York, Armstrong, 1896 |
| Hodge, *1 Corinthians* | New York, Carter, 1857 | New York, Carter, 1874 |
| Hodge, *2 Corinthians* | New York, Carter, 1860 | New York, Carter, 1872 |
| Haldane, *Romans* | New York, Carter, 1858 | London, Oliphant, 1874 |
| Brown, *Hebrews* | Edinburgh, Oliphant, 1862 (archive.org's copy) | the same printing (Google's copy) |
| Brown, *1 Peter* | New York, Carter, 1855 | New York, Carter, 1866 |

Hodge's *Romans* is the 1864 revision; the 1835 first edition is a
different text and is not used. Carter's Hodge printings may share plates,
and Brown's *Hebrews* has only the one printing open, in two copies. There
the vote removes OCR error only, as in Clarke's Old Testament. Google's copy
is only read: nothing of its file is committed, only the verse places and
citations both copies agree on.

**Hodge and Haldane: verse heads.** These books open each comment with a
head: "VERSE 1. Paul, a servant ...", "V. 2.--Which he had promised ...",
or, in Hodge's *Corinthians*, the bare "11. For it hath been declared".
`read_volume` cuts the heads into runs at the "CHAPTER IV." headings ("CHAPTER
I. PART II." goes on with chapter I). It aligns the runs to the book's
chapters with Clarke's dynamic programming. A head is placed when half of
its lemma's words are in the KJV verse it names, so a numbered point
("5. God is the ultimate end") is never a head.

| | heads placed | not placed |
|---|---|---|
| Hodge, *Romans*, 1864 / 1896 | 316 / 318 | 62 / 78 |
| Hodge, *1 Corinthians*, 1857 / 1874 | 240 / 239 | 225 / 216 |
| Hodge, *2 Corinthians*, 1860 / 1872 | 195 / 190 | 66 / 71 |
| Haldane, 1858 / 1874 | 299 / 345 | 37 / 2 |

The New York Haldane writes "Eph. ii., 15". The reader reads that form
(`roman_comma`) along with the London "Eph. ii. 15".

**Brown on 1 Peter: discourses.** Each discourse is on a passage, printed
under its head: "1 PET. ii. 1-3.--Wherefore, laying aside ...". The 1855
printing prints that head. It is read when the words after it are that
verse's KJV words. The 1866 printing prints the passage without a head. There
the passage is found by windows of ten words: it starts at the first window
with 80% of its words in one KJV verse, and runs while each window has 60%
in that verse or a few past it. A discourse is one comment on its passage
(26 rows, 20 placed alike in both printings).

**Brown on Hebrews: no chapter headings to align.** His CHAPTERs are the
divisions of his argument, not the Bible's chapters. So a verse head ("Ver.
5.", "Verses 1-3.--") is placed by its lemma alone, in the nearest chapter at
or after the last one placed. The printed passages that open his sections
are read as in 1 Peter. Brown heads few verses, so this gives 37 comments,
26 placed alike in both copies. Most of his comment runs on without heads,
inside the comment before.

**What these are not.** Brown's comments are whole sections and discourses,
so the Treasury check at their first verse is weak (4-5% against 0.1-0.5%).
The prose in `build/commentary/` is unproofread OCR of the printing named.

## 9. Not committed, not claimed

- **The prose.** It goes to `build/commentary/<work>.text.jsonl`, and
  `commentary.py`'s `text()` reads it there. All four are public domain;
  Poole's transcription is CC0. Committing prose is Adam's call.
- **A comment that differs** keeps its CCEL mark (or Poole's order) as `on`.
  The `anchor` field says so.
- **No citation comes from a scan alone.** For the CCEL and TCP works the
  scans are a check; Clarke, Spurgeon, Hodge's Romans and Corinthians,
  Haldane and John Brown are read from two printings, and a citation needs both.
