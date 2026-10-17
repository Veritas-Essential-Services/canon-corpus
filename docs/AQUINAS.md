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

## Commands

    python3 pipeline/fetch_corpus_thomisticum.py      # Latin pages (resumable, 1 req/s)
    python3 pipeline/ingest_summa_supplement.py       # fetches CCEL summa.xml if missing
    python3 pipeline/ingest_adler.py                  # the Gutenberg Summa the key points into
    python3 pipeline/aquinas_st_1894.py --fetch       # the 1894 OCR volumes
    python3 pipeline/build_aquinas_st.py              # books + parallel file + key
    python3 pipeline/build_aquinas_st.py --check      # key byte-identical
    python3 tests/aquinas_test.py                     # offline checks
