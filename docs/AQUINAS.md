# Aquinas, Latin and English, side by side

Started 2026-10-17 (Adam: "Aquinas in translation and in Latin if we could key
them together somehow"). This file is the ledger for the Aquinas work: what is
held, how the two languages are keyed, and what waits on Adam.

## What was already here (census of all 30 branches, 2026-10-17)

| Held | Where | Notes |
|---|---|---|
| Summa, English, Parts I, I-II, II-II, III | `adler_shelf.json`: `aquinas-summa`, `-1-2`, `-2-2`, `-3` (Gutenberg 17611, 17897, 18755, 19950) | Dominican translation; paragraph ids, kept unchanged |
| Summa, English, Supplement + Appendix | `pipeline/ingest_summa_supplement.py` -> `aquinas-summa-supp` (CCEL) | |
| Latin, anything | nowhere | |
| Contra Gentiles, Catena Aurea, other works | nowhere | Lane A confirmed it holds no Aquinas |

## How the two languages are keyed

The key is **the Thomist citation itself**, which both editions print:

    I.q2.a3          ST I q.2 a.3 (the article; its row carries the English title)
    I.q2.a3.arg1     first objection          I.q2.a3.sc    sed contra
    I.q2.a3.co       the body (respondeo)     I.q2.a3.ad1   reply to the first objection
    I.q2.pr          the question's prologue  I-II.pr       the part's prologue

A second sed contra is `.sc2` (the first is then `.sc1`); a reply to the sed
contra is `.ad-sc`. A question with a single article (I q.71) is keyed `.a1`.
Parts are `I`, `I-II`, `II-II`, `III`, `Suppl`, `App1`, `App2`.

Because the key is the citation, nothing is guessed: two texts either print the
same part of the same article or they don't, and `data/aquinas/st-key.jsonl`
(committed, one row per article) says which:

| status | meaning |
|---|---|
| `both` | the same parts on both sides |
| `parts-differ` | both sides have the article, but divide it differently; the row lists each side's parts |
| `en-only` / `la-only` | one side has no such article |

Each row also carries `pg`: the first and last unit ids of that article in the
existing Gutenberg books (`aquinas-summa:...`), so the Latin can be read beside
the English already held, under its existing ids. `pg_en` in the parallel file
gives the Gutenberg units for every part.

**Built 2026-10-17:** 3,742 rows. 2,867 articles and prologues match part for
part; 314 differ (below); 559 are English-only (the Supplement and its
Appendix, which Corpus Thomisticum does not print, plus two single-article
question prologues); 2 Latin-only (the general prologue to the Summa and the
II-II prologue, which the English folds into II-II q.1).

### Why 314 articles divide differently (real differences, not errors)

- **The translators drop a closing formula.** Where the Latin has *Et per hoc
  patet responsio ad primum* ("and so the first objection is answered") as its
  own reply, the Dominicans often print nothing: 73 articles lack `ad1`, 62 lack
  `ad-sc`, and so on.
- **"On the other hand" read as an objection.** Where the Leonine labels a
  counter-argument *Sed contra, videtur quod...*, the Dominicans call it
  "Objection 4": the Latin row has `sc`, the English `arg4`.
- **Multiple sed contras** printed as one English "On the contrary".

The key records each of these as it is; nothing is forced to line up.

### Repairs to the English (CCEL), made by rule and recorded per row (`en_repairs`)

- A label printed twice ("Reply to Objection 1" for the second reply): the
  occurrence standing where the missing number belongs takes it. 11 articles.
- Two articles printed under one heading (II-II q.64 a.7+8, q.66 a.5+6,
  q.123 a.10+11): split at the second article's first objection.

Every repair was checked against the Latin of the same part.

## Sources and rights (US public domain is the test)

| Text | Source | Rights |
|---|---|---|
| English Summa (keyed) | CCEL `summa.xml` (DC.Rights: Public Domain), the file `ingest_summa_supplement.py` already fetches; no second fetch of the Gutenberg text | Dominican translation 1911-25 (2nd rev. ed. 1920-22): US PD. The digital text was keyed from the Benziger 1947 printing; only the translation is used |
| Latin Summa | Corpus Thomisticum (`pipeline/fetch_corpus_thomisticum.py`): the Leonine text, Rome 1888-1906, ed. Enrique Alarcon | underlying text US PD; **see the Latin question** |

### The Latin question (for Adam)

Corpus Thomisticum is the best Latin text there is (the Leonine, proofread),
and it is cut exactly where the key needs it. But every page says *(c)
Fundacion Tomas de Aquino quoad hanc editionem. Iura omnia asservantur*: the
foundation claims rights in its electronic edition. Under US law a faithful
transcription of a public-domain text is probably not copyrightable (no new
originality), but the claim is there, and the brief said "if its terms allow".

So for now it is handled like the STEPBible lexicons: fetched into the
gitignored corpus, built locally, `redistribute_whole: false` in the manifest,
nothing of its text committed. The committed key holds no Latin text.

### The public-domain Latin: the 1894 Roman edition (built 2026-10-17)

`aquinas-st-la1894`: the *editio altera Romana* (Rome: Forzani, 1894), from the
Internet Archive's OCR of vols. 1-5 (`summatheologicae0001thom`..`0005thom`;
vol. 6 is the index). `pipeline/aquinas_st_1894.py` cuts it by the edition's
own words: *Ad secundum sic proceditur* opens article 2 and names it, so a
misread ARTICULUS heading is overruled and an article 1 after a later article
means a lost QUAESTIO heading. *Praeterea*, *Sed contra*, *Respondeo*, *Ad
primum ergo dicendum* cut the parts. Its Appendix, printed as Suppl. q.100-102,
is renamed to App. II q.1, App. I q.2, App. I q.1 by title.

- 3,109 articles carry it, **including the whole Supplement and Appendix**:
  every English article now has a Latin beside it except 2.
- Each part is checked against the Leonine part of the same key (word
  overlap; median 0.97). The 192 parts under 0.5 are listed in the key row as
  `la1894_doubtful` and flagged in the parallel file. Most sit in I q.12-14,
  where a lost heading shifts a run of articles.
- It is unproofread OCR and a pre-Leonine text; the manifest says both.
- Key rows: `la1894` (its parts), `status_1894` (against the English).

## Summa contra Gentiles (built 2026-10-17)

`pipeline/build_aquinas_scg.py`. The key is book and chapter, as Thomists cite
it: `SCG.3.95` = *Contra Gentiles* III, 95; paragraphs are numbered within the
chapter. `data/aquinas/scg-key.jsonl` (committed, one row per Leonine chapter,
455 rows) says which witnesses print each chapter and how many paragraphs each
has. It holds no text but the English chapter titles.

| witness | text | chapters | rights |
|---|---|---|---|
| `la` | Corpus Thomisticum (the Leonine, 1918-30) | 455 | local only, as for the Summa |
| `la1894` | the *editio Romana* (Rome: Forzani, 1894), IA `summaecontragent00thom`, raw OCR | 443 | US PD: **the Latin that can be shared** |
| `dominican` | English Dominican Fathers, literal, "from the latest Leonine edition" (1923-28), IA OCR | 354 (Books I-III) | US PD |
| `rickaby` | Joseph Rickaby, *Of God and His Creatures* (1905), abridged and annotated, CCEL | 383 (all four books) | US PD |

297 chapters have all four witnesses. Only 12 Leonine chapters lack the PD
Latin, and each one is a heading the 1894 OCR lost: its text is there, run
into the chapter before (the manifest lists them).

**Two numberings.** The Leonine renumbered the work. The editions before it,
the 1894 included, number differently: Book III runs to 164, and a chapter of
objections often stands apart from the chapter that answers them. Rickaby
translates that older numbering. So:

- The 1894 Latin is placed on the Leonine **by its text**. The opening of each
  1894 chapter is matched against every three-paragraph window of each
  Leonine chapter, so the second half of a joint chapter is found too. Nearly
  every chapter matches at 0.6 or better (Dice of the words), and the five
  below 0.4 were checked by title and are right. Its own number is kept as
  `la1894_numbered` wherever it differs (42 chapters).
- Rickaby goes with the 1894 chapter of his number (370 chapters). Where the
  1894 OCR lost that heading, his title is matched against the Dominican's
  instead (9 chapters); 1 keeps his own number. His own numbers are
  `rickaby_numbered`. Where he joins a chapter of objections to its answer
  ("Chapters XXXII, XXXV"), the answering chapter's row says `rickaby_in`.
- The Leonine prints eight pairs as one chapter (I, 51-52; III, 95-96 ...).
  The row has `la_covers`, and the covered number's row, if any, has `la_in`.

**The Dominican English is raw OCR.** Its chapters are found by their
headings, in sequence. A running head (CHAPTER XLII 87) and a table of
contents are told apart from a heading, and a joint heading (CHAPTERS VIII AND
IX) covers two chapters. Four headings are lost in the scan (I, 13; II, 78;
III, 63, 81), and each chapter's text runs into the next; the manifest lists
them. Paragraph counts agree with the Leonine in 104 of 354 chapters, because
the OCR's paragraphs are not the Leonine's numbered ones. **Book IV (1929) is
on no Archive scan we could find**, so Book IV has Rickaby's abridgement only
in English.

## Catena Aurea (built 2026-10-17)

`pipeline/build_aquinas_catena.py`. The key is the Latin's own division:
`CA.Mt.5.3` = *Catena in Matthaeum*, cap. 5, lectio 3. A lectio is a few verses
and the Fathers' comments on them, quoted one after another.
`data/aquinas/catena-key.jsonl` (committed, one row per lectio, 827 rows)
gives the verses, the Fathers in order on each side, and the fit. It holds
no text.

| gospel | Latin lectiones | English sections | one to one | median fit |
|---|---|---|---|---|
| Matthew | 285 | 285 (CCEL, clean) | 282 | 1.0 |
| Mark | 105 | 105 (CCEL, clean) | 105 | 1.0 |
| Luke | 246 | 287 (IA OCR) | 206 | 0.94 |
| John | 191 | 223 (IA OCR) | 147 | 0.95 |

Every lectio has its English.

**How a section finds its lectio.** The English (the Oxford translation, ed.
J. H. Newman, 1841-45, US PD) prints no lectio numbers. It opens each section
with the verses it comments on. The sections are placed on the lectiones by
**the order of the Fathers quoted**: Gloss, Augustine, Augustine, Chrysostom,
Gregory. That order survives translation, so it works as a fingerprint.
`fit` is how closely the two orders agree (0 to 1). The lowest is 0.57, and
the lowest few were read and are right.

- Where the OCR splits one lectio's verses into two or three sections, they
  are joined into that lectio (`en_sections`). This happens 74 times, all in
  Luke and John.
- Where one English section spans two lectiones, the second lectio's row
  points to the first with `en_in`.
- The Latin keeps the medieval chapter breaks in a few places. Its Mt 5,
  lectiones 22-23, are Mt 6:1-4. Those rows say `en_chapter: 6`, and their
  verses are in that chapter.

Matthew and Mark come from clean CCEL text. Luke and John are unproofread
OCR: the margin notes (the sources of the quotations) stay in the text.

## Commands

    python3 pipeline/fetch_corpus_thomisticum.py      # Latin pages (resumable, 1 req/s)
    python3 pipeline/ingest_summa_supplement.py       # fetches CCEL summa.xml if missing
    python3 pipeline/ingest_adler.py                  # the Gutenberg Summa the key points into
    python3 pipeline/aquinas_st_1894.py --fetch       # the 1894 OCR volumes
    python3 pipeline/build_aquinas_st.py              # books + parallel file + key
    python3 pipeline/build_aquinas_st.py --check      # key byte-identical
    python3 pipeline/fetch_shelf.py aquinas           # the English shelf (Dominican SCG OCR, Rickaby, Catena ...)
    python3 pipeline/build_aquinas_scg.py --fetch     # Contra Gentiles: the 1894 Latin OCR
    python3 pipeline/build_aquinas_scg.py             # Contra Gentiles books + parallel file + key
    python3 pipeline/build_aquinas_scg.py --check     # its key byte-identical
    python3 pipeline/build_aquinas_catena.py          # Catena Aurea books + parallel file + key
    python3 pipeline/build_aquinas_catena.py --check  # its key byte-identical
    python3 tests/aquinas_test.py                     # offline checks
