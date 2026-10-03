---
model_log:
  - 2026-07-22 claude-fable-5 drafted (from git trailer; backfilled 2026-09-30)
  - 2026-09-26 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
  - 2026-09-27 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
fable_review: pending
---
# canon-corpus

The shared source + structure layer of the Canon OS: manifest-driven
fetchers for public-domain texts (Perseus TEI, CCEL ThML, Project
Gutenberg) and converters that turn them into unit-id JSON with canonical
citations, scripture keylinks, and honest resolution metadata.

*Commit the manifest and the recipe; the texts refetch.* Corpus and built
JSON are gitignored — `data/books/manifest.json` (checksums, schemes,
provenance) is the committed record of the collection.

## Build the library

    python3 pipeline/fetch_sources.py       # fetch sources -> data/corpus/
    python3 pipeline/structure_texts.py     # convert       -> data/books/*.json

## Consumers

- [armarium](../armarium) — the personal Libronix (search, reverse
  concordance, reader). Expects this repo as a sibling checkout.
- patrimonium — the Nomenclator's card backs.
- Memoria / the Resolver — future.

## Tests

    python3 tests/structure_test.py         # 95 offline checks, no corpus needed
    python3 tests/versification_test.py     # the Hebrew->KJV verse map (BDB's citations)
    python3 tests/vulgate_versification_test.py  # the Clementine Vulgate->KJV verse map
    python3 tests/brenton_versification_test.py  # Brenton's Septuagint->KJV verse map
    python3 tests/english_versification_test.py  # Geneva, Tyndale, Young's, Darby, ASV->KJV maps
    python3 tests/parallel_index_test.py    # the parallel-Bible index (data/parallel/)
    python3 tests/deuterocanon_test.py      # the deuterocanon's shared key (KJV Apocrypha)
    python3 tests/hymn_corpus_test.py       # the hymn JSONL validator (D1-D2)
    python3 tests/lemma_spine_test.py       # the Latin lemma spine (D3)
    python3 tests/nt_corpus_test.py         # the Greek NT JSONL validator (D2-D5 pilot)
    python3 tests/ot_corpus_test.py         # the Hebrew OT JSONL validator
    python3 tests/reader_test.py            # the reader: deterministic, self-contained, every token (D5)
    python3 tests/review_test.py            # review.py end to end, on a temp copy of the repo
    python3 tests/lemma_bridge_test.py      # English lemma bridge (ADR 0012): shew/show, holpen/help in real FTS5
    python3 tests/remint_maxims_test.py     # remint_maxims.py end to end, on a temp copy

## Adam's review sheets

    python3 pipeline/review.py status               # answered vs open, per sheet
    python3 pipeline/review.py apply <sheet.md>     # his answers -> override rows, rebuild, --check
    python3 pipeline/review.py render [--check]     # the sheets, regenerated from the data

`docs/review/2026-09-26-lemma-flags.md` (24 Latin tokens -> `data/lemmas/adam-reviewed.jsonl`)
and `docs/review/2026-09-26-john1-drafts.md` (137 house glosses and 18 plain lines ->
`data/nt/gloss-overrides.jsonl`, `data/nt/prose-order.jsonl`). The answers `ok`/`✓`,
`draft→` and a value are explained in `pipeline/README-lemma-spine.md` s.8b and
`pipeline/README-nt-jsonl.md` s.15. Anything ambiguous stops the run and names the row.

## Adam's maxims: re-mint to house uids (prepared, not run)

    python3 pipeline/remint_maxims.py            # dry run (the default): writes nothing
    python3 pipeline/remint_maxims.py --write    # mint maxims:AK-00n in the registry; write the Hoard records
    python3 pipeline/remint_maxims.py --check    # the written records match the source and the registry

**The maxims are private, and this repo is public.** Since 2026-09-27 the
source and its records live in the Word Hoard house repo, cloned beside this
one (or set `WORDHOARD_HOUSE`): `wordhoard/data/maxims/maxims-original.jsonl`
stays as filed, and `--write` adds `wordhoard/data/maxims/maxims-original.hoard.jsonl`,
one `passage/maxim` Hoard record per maxim, `ak-maxim-000n` kept in `legacy[]`.
That file is what the Florilegium's Propria imports. Their `maxims:` citations
go in the house's private registry; only the bare uids come back here, as
`reserved` (see `data/uids/`).

## Latin hymns (JSONL)

`data/hymns/` holds *Adoro te* and *Pange lingua* as four flat JSONL files
(passages, witnesses, tokens, alignments), one row per clause, every record
keyed by uid. Schema and rules: `pipeline/README-hymn-jsonl.md`.
Each token's lemma comes from Whitaker's WORDS where it agrees with the house
draft (launch plan D3): `pipeline/README-lemma-spine.md`.

## Greek New Testament (JSONL)

`data/nt/` holds the whole New Testament from the Robinson-Pierpont
Byzantine text (public domain): 7,953 verses, 140,149 words, one folder per
book with the same four files, one row per verse, and one manifest over all
of them. John 1:1-18 is the pilot the house drafts and the reader cover. Each verse is a
witness of the KJV verse's existing uid, so nothing is minted. Parsing is
Robinson's; lemmas are Strong's headwords. Schema, licence evidence,
transliteration scheme and the two rulings still open (the Romans doxology,
the sharding): `pipeline/README-nt-jsonl.md` s.16.

## Hebrew Old Testament (JSONL)

`data/ot/` holds the whole Old Testament from the Westminster Leningrad Codex
(public domain): 23,142 KJV verses, 305,124 words, laid out like the NT. Each
Hebrew verse is mapped to its KJV verse through `data/versification/bhs-kjv.json`
and is a witness of that verse's existing uid, so nothing is minted. Ketiv and
qere are both kept. The OSHB lemmas and morphology are CC BY 4.0, so they are
left out of this public repo. Schema, licence evidence and the open rulings
(psalm titles, spans, joined verses): `pipeline/README-ot-jsonl.md`.

Both testaments rebuild from pinned sources in under a minute:
`python3 pipeline/rebuild_bible.py` fetches the pinned inputs (one shallow git
fetch per source repo, sha256-checked), builds, and checks the result is
byte-identical. `--verify` does the same in memory and writes nothing.

## Apostolic Fathers (Greek)

Nine books from Kirsopp Lake's Loeb edition (1912-13, public domain), built
from the First1KGreek TEI: 1 and 2 Clement, the seven letters of Ignatius,
Polycarp to the Philippians, the Martyrdom of Polycarp, the Didache, Barnabas,
Hermas and Diognetus. That is 1,941 sections and 64,890 words, cited the
standard way (`1 Clem. 1.1`, `Ign. Eph. 1.1`, `Herm. Sim. 9.1.1`). The TEI
is CC BY-SA 4.0, so the books are built locally and only their manifest
entries are committed, each labelled. 85% of the Greek words carry a Strong's
number by fixed rules against the Greek NT; the rest are left blank, never
guessed. Lake's scripture references resolve to KJV verses, the Old Testament
through Brenton's Septuagint map, and the ones First1KGreek keyed to the wrong
book are flagged. `python3 pipeline/build_apostolic_fathers.py --fetch`. Lightfoot's
English is aligned to it (next section).

## Apostolic Fathers (English, Lightfoot)

Lightfoot and Harmer's translation (1891, public domain), from CCEL's ThML
(pinned by sha256), as nine books matching Lake's nine. Every English unit is
keyed by the Greek it translates (`1clement-lightfoot:4.7` is `1 Clem. 4.7`)
and links to it. Chapters match by rule; inside a chapter CCEL's paragraphs
are placed on Lake's sections by their lengths, and a boundary is drawn only
where every near-best alignment agrees. Of Lake's 1,941 sections, 1,819 have
an English unit of their own, 114 are reached in a run of two or three, and 8
(four Ignatius chapters) only by chapter. Measured: 97.7% of the proper names
in the English are in the linked Greek, against 15.2% in the next unit's, which
is the evidence the alignment is right. A length check agrees (99.1% of the
one-to-one pairs keep the work's own length ratio, 49.6% when shifted by one),
but it is weaker: the ratio is the median of those same pairs, over chapters
whose counts already agree. Range ids (`5.5-6`) are the aligner's; find a
single section through a unit's links. Papias is not in CCEL's file. Built locally;
manifest entries committed. `python3 pipeline/build_lightfoot.py --fetch`.

## Charles's Apocrypha and Pseudepigrapha (1913, read from the scans)

R. H. Charles's two volumes in English, 32 books from I Esdras to the
Zadokite Fragments. No machine-readable edition exists, so the text is the
Internet Archive's OCR of the Toronto scans (hOCR pinned by sha256),
read by `pipeline/charles_ocr.py`: the translation is told from the notes by
type size, verse numbers are read from the margin and decoded as a sequence
checked against each page's running head. Ids are Charles's own citations
(`charles-tob:5.16`, `charles-testxii:Jos.3.7`, `charles-sib:3.101` by line).

Measured, not claimed: 26 books are built verse by verse (12,054 verses;
86% of the numbers read off the page, the rest inferred and flagged as
such); where the KJV Apocrypha has the book, Charles has a unit for 4,662 of
its 4,984 verse numbers. Six books fall below the bar or print versions in
parallel columns and are built by page, one unit per scan leaf
(`charles-adam:leaf.12`), the printed folio kept where the OCR read it. Where a page carries two
witnesses side by side (Susanna and Bel's LXX and Theodotion), only the left
column is read, and the 52 such leaves are counted in the manifest; a line the
OCR read straight across both columns is cut at the gutter first. Each
unit records how its number was got and where its first words were placed;
the text is unproofread OCR. A verse number decoded twice keeps both units, the
second id suffixed `~2` (a house convention awaiting a ruling). Public domain in the US; the Additions to
Esther (Gregg, d. 1961) are flagged `redistribute_whole: false`.
`python3 pipeline/build_charles.py --fetch`, then `--report`. Lines of notes
or apparatus that slip past the type-size split (a third Greek, or thick with
sigla) are dropped, counted, and listed for review. An OCR flag list,
`pipeline/proof_charles.py`, flags likely OCR errors for review against the
scans in `docs/review/charles-ocr-flags.tsv` (unit, leaf, token, a suggested
reading); it changes nothing in the text.

## The Wycliffite Bible (Forshall and Madden 1850, read from the scans)

The earlier and later versions, from F&M's two columns. The source is the
Internet Archive's ABBYY hOCR of the Toronto copy: four items,
`holybiblecontain01`-`04wycluoft`, each pinned by sha256 and marked
`NOT_IN_COPYRIGHT`. The build is `pipeline/build_wycliffe.py`, and it
produces two books, `wycliffe-earlier` and `wycliffe-later`. Ids are in the
Clementine's numbering (`wycliffe-later:Ps.50.3`), and each unit's `kjv` is
resolved through `vulgate-kjv.json`.

What the manifest measures:

- **Coverage of the Clementine's 35,809 verses:** earlier 94.4%, later 85.5%.
- **Books by scan leaf:** four later-version books (Prov, Sir, 2 John,
  Jude) fall below the bar and are built one unit per scan leaf. The
  scheme's `resolution` names them.
- **Check against eBible:** the later version agrees with eBible's
  transcription of the nine books it holds on 81.7% of verses.

The text is unproofread OCR.

A verse number decoded twice keeps both units, the second as `<id>~2`
(then `~3`), with `scan.duplicate_number`. This is a house convention shared
with the Charles books, awaiting Adam's ruling.

`python3 pipeline/build_wycliffe.py --fetch`, then `--check`.

## Commentaries: Lightfoot, Westcott, Hort, Ellicott (drafts)

The build is `pipeline/build_commentaries.py`. It shelves thirteen books, all
printed before 1929:

| Book | Edition | Source |
|---|---|---|
| Lightfoot on Galatians | 10th ed., 1910 reprint | IA scan |
| Lightfoot on Philippians | 3rd ed., 1873 | IA scan |
| Lightfoot on Colossians and Philemon | 1st ed., 1875 | Project Gutenberg #50857 |
| Westcott on Hebrews | 2nd ed., 1892 | IA scan |
| Westcott on the Epistles of St John | 3rd ed., 1892 | IA scan |
| Hort, *Six Lectures on the Ante-Nicene Fathers* | 1895 | IA scan |
| Westcott on St John's Gospel (the Greek text) | 1908, 2 vols | IA scans |
| John Lightfoot, *Horae Hebraicae et Talmudicae* (Matthew to 1 Corinthians) | Gandell's ed., 1859, 4 vols | IA scans |
| Ellicott on Galatians | 4th ed., 1867 | IA scan |
| Ellicott on Ephesians | 5th ed., 1884 | IA scan |
| Ellicott on Philippians, Colossians and Philemon | 1st ed., 1857 | IA scan |
| Ellicott on Thessalonians | 4th ed., 1880 | IA scan |
| Ellicott on the Pastoral Epistles | 5th ed., 1883 | IA scan |

Every source is pinned by sha256. Each scan was picked by measuring its
text layer. Many scans of these books have no Greek at all, because their
OCR turned every Greek word into Latin letters.

**Notes by verse.** A note is cited by the verse it comments on:

- `lightfoot-galatians:2.20` links to `kjv:Gal.2.20`.
- A run of verses is `1.6-9`.
- In a volume of several epistles the book comes first:
  `westcott-john:2John.1.6`.

On the scanned books, a verse number at the start of an indented note is
taken only when it fits the sequence of verses and the page's running head.

**Everything else is kept**, in these units:

- `leaf.N.text`: the epistle's own text block on a page, with Westcott's
  apparatus.
- `leaf.N`: every other page, by scan leaf, with the printed folio in
  `scan.printed_page`.
- Gutenberg's Colossians uses `p.N` for printed pages and `text.Col.1.3`
  for the Greek text.
- Hort is by page only. Each page carries its `lecture`.

**Scripture.** References in the English are resolved in the KJV's
numbering. Some rules:

- "ver. 8" means the same chapter of the note's own epistle.
- A bare "c. iii. 13" means the note's own epistle too. Both readings
  happen in note units only. They never happen after another work's
  abbreviation: "Euseb. H.E. c. iv. 3" is Eusebius, not Galatians 4:3.
- A range keeps its end in `through`. That includes "vv. 8-12" and a range
  that crosses chapters, such as "Rom. viii. 28-ix. 3".
- Sometimes the KJV cannot end a range, because the range runs past the
  chapter or runs backwards. The link then keeps only the start verse and
  says why in `through_unread`. These links are counted in
  `scripture_links.ranges_start_only`.
- A note may open with a run of verses. If the run is backwards, past the
  chapter, or longer than 15 verses, only its first verse is kept
  (`openers_run_cut`).
- A run into the next chapter, such as "28—V. 1.", is not read as an opener
  at all (`openers_crossing_chapter`).

**Two Greek yardsticks.** The candidate table in the script and the
manifest measure Greek against different word lists, so their numbers
differ. For example, Lightfoot's Galatians scores 65.9% in the table and
0.37 in the manifest.

- The table (wave 1, read from each candidate's `_djvu.txt`) also counted
  the Greek of the proofread Gutenberg Colossians. That list holds the
  commentators' own vocabulary, so more words match. The table uses this
  figure only to rank the scans of one book against each other.
- The manifest's `greek.greek_tokens_in_reference_vocab` uses only Strong's
  lemmas and the forms of John in `data/nt`. These lists are committed and
  fixed, so the manifest can compare one book with another, and every
  rebuild gives the same figure. Inflected forms outside John don't count,
  so the figure reads low.
- The wave-2a rows of the table already use the manifest's yardstick.

**The second wave (2a)** uses the same rules, with three additions:

- A book may come from several scans. Its page ids then lead with the
  volume: `westcott-gospel-john:v2.leaf.15`. The notes keep the plain
  citation: `westcott-gospel-john:8.12`, `lightfoot-horae:Matt.5.22`.
- Lightfoot's *Horae* has one column, and each note opens "Ver. 5:". The
  chapter is read from the "CHAP." headings and from running heads that a
  neighbouring page agrees with. Lightfoot skips whole chapters, so the
  chapter only moves forward. Its Hebrew survived the OCR in these scans
  only (about 2% of letters), and `measure.hebrew` says how much of it reads
  as biblical Hebrew.
- For the new books, the measure also counts the notes whose page's
  running head names another chapter (`openers_against_running_head`), and
  the verses that were taken up again later (`notes_reopened`).

Westcott's *Ephesians* (1906) is not shelved. In every scan of it, the
Greek was lost or the English was read as Greek. The other scans that were
measured, and why each was refused, are listed above `CANDIDATES` in the
script.

All the scanned books are unproofread OCR, and their honesty fields say
so. Run `--fetch`, then `--check`. To see each book's coverage and Greek
measures, run `--report`.

### The second shelf: Alford, Bengel, Keil & Delitzsch (drafts)

The same build shelves twelve more volumes, one book per volume, all read
from Internet Archive scans:

| Books | Volumes | Printed |
|---|---|---|
| Alford, *The Greek Testament* | II (Acts-2 Cor), III (Gal-Phlm), IV (Heb-Rev) | 1857, 1865, Boston issue cat. 1874 |
| Bengel, *Gnomon of the New Testament* (T&T Clark English) | II (Luke-Acts), III (Rom-2 Cor), IV (Gal-Heb) | 1873, 1873, 1877 |
| Keil, *The Pentateuch* (Keil & Delitzsch) | I-III | 1878, 1872, 1871 |
| Delitzsch, *The Psalms* (Keil & Delitzsch) | I-III | 1880, 1871, 1881 |

Ids lead with the book in a volume of several books
(`alford-commentary-3:Gal.2.20`, `bengel-gnomon-4:Heb.11.1`). Alford runs
his verse notes on inline ("9.] As we said"), so his openers are read inside
the lines. Keil & Delitzsch open sections "Ver. 3." or "Vers. 14-19.", at a
paragraph or after a dash. Delitzsch's psalm titles start each psalm, and
what comes before the first verse note is the unit `<psalm>.intro`.

**Which numbering.** Keil & Delitzsch number the Old Testament as the
Hebrew does in places. This is measured for each book, not assumed: a verse
only the Hebrew has is a vote for the Hebrew, and a verse only the KJV has
is a vote for the KJV. Delitzsch's Psalms measure as Hebrew, so
`delitzsch-psalms-2:51.5-6` links to the KJV's Ps 51:3-4 through
`data/versification/bhs-kjv.json`, and a psalm's title stays unresolved
with its reason. The Pentateuch mostly measures undecided (the numberings
rarely differ there), and then each verse is read where it exists.

**What is lost.** No scan of Keil & Delitzsch keeps its Hebrew: the OCR
read it as Latin letters, which stay in the text as the OCR gave them.
Every honesty field says so.

**Not shelved.** Alford vol. I and Bengel vols I and V have no scan that
keeps the Greek. Delitzsch's Isaiah does not mark its sections "Ver.", so it
needs a different reader; its scans are measured and listed in the code.

### The third shelf: Meyer (drafts); Godet not shelved

H. A. W. Meyer's *Critical and Exegetical Handbook to the New Testament*, in
the T&T Clark translation, one book per volume, read from Internet Archive
scans:

| Book | Volume | Printed | IA item |
|---|---|---|---|
| `meyer-matthew-1` | Matthew I (ch. 1-17) | Edinburgh, 1880 | criticalexeget01meyeiala |
| `meyer-matthew-2` | Matthew II (ch. 18-28) | Edinburgh, 1879 | criticalexegetic12meye |
| `meyer-mark-luke-1` | Mark; Luke 1-2 | Edinburgh, 1880 | criticalexegetic21meye |
| `meyer-mark-luke-2` | Luke 3-24 | Edinburgh, 1880 | criticalexegetic22meye |
| `meyer-john` | John | New York (Funk & Wagnalls), 1884 | criticalexegetic04meye |
| `meyer-romans` | Romans | New York (Funk & Wagnalls), 1884 | criticalexegetic06meye |

Every T&T Clark scan of John and of Romans lost its Greek, so those two come
from the American issue of the same translation. That issue adds notes by an
American editor (A. C. Kendrick on John, Timothy Dwight on Romans). They are
kept apart, as `<chapter>.american` (kind `editor-notes`, with `by`), and
never mixed into Meyer's notes.

**How a page is read.** Each chapter opens "CHAPTER IV." and then Meyer's
critical notes on its readings. That heading and those notes are the unit
`<chapter>.intro`. The exegesis follows, a paragraph per verse or run,
opening "Ver. 1." or "Vv. 2-6." Only such an indented paragraph opens a
note. In Mark and Luke (and, where it measured better, the other volumes)
Meyer also runs notes on after a dash ("— Ver. 14."), and those are read too.
Romans measured better without them. A heading the OCR garbled or lost is
found by the critical paragraph under it. Its number is checked against the
chapter that should come next. The running heads never move a note back to
an earlier chapter.

**Coverage** (verses with a note, of the verses in the chapters the volume
holds): Matthew I 86%, Matthew II 75%, Mark 97%, Luke 1-2 61%, Luke 3-24
95%, John 91%, Romans 97%. Meyer passes over some verses, and the measure in
each manifest entry counts the openers accepted, refused and taken from the
running heads. The Hebrew is lost in every scan, and every honesty field
says so.

**Not shelved yet:** Meyer on Acts and on Corinthians. Their scans keep the
Greek and are listed in the code.

**Godet is not shelved.** All 50 scans of his John, Luke, Romans and
1 Corinthians in English (the Edinburgh issues and the Funk & Wagnalls
reprints) have no Greek letters at all. Godet quotes the Greek in his notes,
and the OCR turned every such word into Latin letters. CCEL and Project
Gutenberg do not have these books. Shelving them without their Greek, as
Keil & Delitzsch are shelved without their Hebrew, is Adam's call.

## Josephus (Greek and English)

The Antiquities, the Jewish War, the Life and Against Apion: Niese's Greek
(1885-95) and Whiston's English (1737), both public domain, from the Perseus
TEI, which is CC BY-SA (built locally, labelled in the manifest). Each work's
two books are aligned by Whiston's book.chapter.section (`Ant. 18.3.3`), and
every Greek unit also gives its Niese sections (`18.63-64`), so either
citation finds it. 2,304 aligned units; 72% of the Greek words carry a
Strong's number. `python3 pipeline/build_josephus.py --fetch`.

## Philo (Greek and English)

The 31 treatises of Philo of Alexandria that survive in Greek: Cohn-Wendland's
Greek (1896-1915) and Yonge's English (1854-55), both public domain, from the
First1KGreek TEI, which is CC BY-SA (built locally, labelled in the manifest).
62 books, cited by treatise and Cohn-Wendland section (`Spec. 1.177`) and
aligned section for section; only *On the Special Laws* has Greek sections the
English file lacks, 58 of them, listed. The editors' 1,835 scripture
references are moved out of the Greek into links, and 1,826 resolve to a KJV
verse (`--measure` shows how they number). 70% of the Greek words carry a
Strong's number. `python3 pipeline/build_philo.py --fetch`.

## A variant apparatus for the Greek NT

For every KJV verse where eight printed editions disagree (NA28, NA27, the
Tyndale House GNT, SBLGNT, Westcott-Hort, Tregelles, Scrivener's TR and the
Byzantine text), which editions read which words, and what the others print
instead. 4,737 verses carry an apparatus, with 8,198 readings, of which 1,724
change the translation. Each verse is filed on its existing KJV uid. The source
is STEPBible's TAGNT (CC BY 4.0, which STEPBible asks not to be redistributed),
so the book is built locally and only its manifest entry is committed.
MorphGNT/SBLGNT and OpenGNT were read and turned down on their licences.
`python3 pipeline/build_nt_variants.py --fetch`.

## The reader (reverse interlinear, D5)

    python3 pipeline/render_reader.py       # -> build/reader/reader.html (gitignored)

One renderer over both datasets: *Adoro te*, *Pange lingua* and John 1:1-18 in
one self-contained HTML file (inline CSS and JS, no network, no web fonts,
light and dark, readable at 375px). Each passage shows the original, with every
word tappable for lemma, parsing and translit, and then the columns wooden /
plain / elegant / singable. A column the data cannot fill is shown empty with
its reason: the Greek has no glosses yet, so it has no wooden or plain line.
`wooden` and `plain` come from `render_wooden()` / `render_plain()` in
`build_hymn_corpus.py` and are never stored. Each source's licence and
attribution is on the page. The agreement marks are drawn from the draft's
`syntax` notes and toggle between two candidate forms. The choice between them
is Adam's: `docs/reader-agreement-marks.md`.

Extracted from the patrimonium repo 2026-07-22; pre-extraction history
lives there (through commit `d33503e`).
