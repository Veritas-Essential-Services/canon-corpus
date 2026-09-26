# Adoro te: the received Latin collated against Britt 1922 (2026-09-26)

**For:** Adam. **From:** `pipeline/build_hymn_corpus.py` (`collate()`), which
compares the corpus's *Adoro te* (`la.1`, source `roman-missal-received`, "not
yet checked against a named PD printing") word by word with Matthew Britt, *The
Hymns of the Breviary and Missal* (1922), no. 79, pp. 190-191. Britt's Latin was
read from the page images (scan `hymnsofbreviarym00britrich`, n199-n200, each
image's sha256 recorded) into `data/hymn-sources/britt-1922-adoro-te.json`, by
the conventions of the other three Britt hymns. The OCR layer was not used.

**Result:** 149 received words, 148 printed; 148 paired, 124 identical to the character. **25 differences**: 12 punctuation, 10 orthography, 1 capital, 1 spelling, 1 word. **Nothing in the text has
changed**, and no uid has: this sheet only lists them.

**Worth a look first** (the two that change a `search_key`):

- **st3 l.4** *paenitens* (received) against Britt's *pœnitens*. Both spellings
  are attested, and `search_key` does not fold *ae* into *oe*, so a search
  for one misses the other.
- **st7 l.4** the closing *Amen*: Britt prints none, as for *Pange lingua*.

The rest are Britt's orthography (æ, œ, consonantal j, which `search_key`
already folds), one capital (*Veritatis* / *veritatis*, st2 l.4), and
punctuation. The canonical orthography is still your call (Latin Hymns doc
s.7, decision 2); these rows let you make it word by word or all at once.

**How to answer.** In the *Adam* column write `ok` (the received reading
stands), `britt` (you prefer Britt's), or `draft→` to leave it open; add
`; note: …` if you like. Then
`python pipeline/review.py apply docs/review/2026-09-26-adoro-collation.md`
writes one row per answer to `data/hymn-sources/collation-reviewed.jsonl`,
rebuilds and runs `build_hymn_corpus.py --check`.

**What an answer does.** The build counts the answers in the manifest
(`sources["roman-missal-received"].collation`). When every row says `ok`,
the source becomes `verified: true`, dated by your latest answer. A `britt`
answer is recorded, **not applied**: the Latin comes from the batch note, and a
change to it is made there (then remove that answer row: the difference it
answered no longer exists, and the build stops on an answer to nothing).

**Hopkins.** His *Adoro te* is not in the 1918 *Poems*: Bridges's note says the
edition prints no translations, and the Project Gutenberg transcription of it
has none. No public-domain printing of the translation was reachable, so it
stays unverified (`sources["hopkins-1918"].finding`).

| # | St · line | Difference id | Received (the corpus) | Britt 1922 | Kind | Adam: |
|---|---|---|---|---|---|---|
| 1 | 1 · l.2 (p. 190) | `wh-XS0K64RXX7/la.1.t01:orthography` | *Quae* | *Quæ* | orthography | |
| 2 | 1 · l.3 (p. 190) | `wh-54JF0Y5SAS/la.1.t06:orthography` | *subiicit* | *subjicit* | orthography | |
| 3 | 1 · l.4 (p. 190) | `wh-Q7RW8M6N3G/la.1.t03:punctuation` | *contemplans* | *contemplans,* | punctuation | |
| 4 | 2 · l.3 (p. 190) | `wh-ZAQ3WCX1ZT/la.1.t05:punctuation` | *Filius:* | *Filius,* | punctuation | |
| 5 | 2 · l.4 (p. 190) | `wh-AY5MTJ16HN/la.1.t04:capital` | *Veritatis* | *veritatis* | capital | |
| 6 | 3 · l.2 (p. 190) | `wh-0861J9FP9P/la.1.t06:punctuation` | *humanitas;* | *humanitas:* | punctuation | |
| 7 | 3 · l.3 (p. 190) | `wh-9VBD834SNY/la.1.t03:punctuation` | *credens* | *credens,* | punctuation | |
| 8 | 3 · l.4 (p. 190) | `wh-9VBD834SNY/la.1.t10:spelling` | *paenitens* | *pœnitens* | spelling | |
| 9 | 4 · l.1 (p. 190) | `wh-DYSVH9E243/la.1.t05:punctuation` | *intueor;* | *intueor:* | punctuation | |
| 10 | 5 · l.1 (p. 191) | `wh-C6XJ8HY910/la.1.t04:punctuation` | *Domini!* | *Domini,* | punctuation | |
| 11 | 5 · l.2 (p. 191) | `wh-RG74QS4K4B/la.1.t02:punctuation` | *vivus,* | *vivus* | punctuation | |
| 12 | 5 · l.2 (p. 191) | `wh-RG74QS4K4B/la.1.t04:orthography` | *praestans* | *præstans* | orthography | |
| 13 | 5 · l.2 (p. 191) | `wh-RG74QS4K4B/la.1.t05:punctuation` | *homini!* | *homini,* | punctuation | |
| 14 | 5 · l.3 (p. 191) | `wh-0Y016CRD3W/la.1.t01:orthography` | *Praesta* | *Præsta* | orthography | |
| 15 | 5 · l.3 (p. 191) | `wh-0Y016CRD3W/la.1.t02:orthography` | *meae* | *meæ* | orthography | |
| 16 | 6 · l.1 (p. 191) | `wh-DZFZPFNWFA/la.1.t02:punctuation` | *pellicane,* | *pellicane* | punctuation | |
| 17 | 6 · l.1 (p. 191) | `wh-DZFZPFNWFA/la.1.t03:orthography` | *Iesu* | *Jesu* | orthography | |
| 18 | 6 · l.3 (p. 191) | `wh-04J0BZVQGS/la.1.t01:orthography` | *Cuius* | *Cujus* | orthography | |
| 19 | 7 · l.1 (p. 191) | `wh-J5EPARGG3B/la.1.t01:orthography` | *Iesu* | *Jesu* | orthography | |
| 20 | 7 · l.1 (p. 191) | `wh-J5EPARGG3B/la.1.t05:punctuation` | *aspicio,* | *aspicio:* | punctuation | |
| 21 | 7 · l.2 (p. 191) | `wh-ZX5Y8TQ8K1/la.1.t03:punctuation` | *illud* | *illud,* | punctuation | |
| 22 | 7 · l.2 (p. 191) | `wh-ZX5Y8TQ8K1/la.1.t06:punctuation` | *sitio;* | *sitio:* | punctuation | |
| 23 | 7 · l.4 (p. 191) | `wh-CGTXCH3Y9B/la.1.t09:orthography` | *tuae* | *tuæ* | orthography | |
| 24 | 7 · l.4 (p. 191) | `wh-CGTXCH3Y9B/la.1.t10:orthography` | *gloriae* | *gloriæ* | orthography | |
| 25 | 7 · l.4 (p. 191) | `wh-CGTXCH3Y9B/la.1.t11:word` | *Amen.* | — (absent) | word | |

Row numbers are for talking about the sheet only; each answer is keyed by its
difference id (the received token's address and the kind of difference).

## What an answer looks like in the file

```
{"id": "wh-…/la.1.t10:spelling", "reading": "received", "reviewed_on": "2026-09-27"}
{"id": "wh-…/la.1.t11:word", "reading": "britt", "reviewed_on": "2026-09-27", "note": "no Amen, as Britt"}
```
