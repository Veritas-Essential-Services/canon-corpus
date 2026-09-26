# The Greek New Testament in the corpus JSONL (pilot: John 1:1–18)

*Schema `wordhoard/corpus-jsonl/v1`, the same four files as the hymns
(`README-hymn-jsonl.md`), with the differences written down here. Built by
`pipeline/build_nt_corpus.py`, validated by `tests/nt_corpus_test.py`.
Launch plan D2 (format), D3 (lemma spine), D4 (licence gate) and D5 (reader
datasets), the Greek half. 2026-09-26.*

```
data/nt/passages.jsonl     one line per verse (the passage that already exists)
data/nt/witnesses.jsonl    one line per Greek rendering of a verse (grc.byz)
data/nt/tokens.jsonl       one line per word of that rendering
data/nt/alignments.jsonl   one line per verse: grc.byz faces kjv.plain
data/nt/manifest.json      counts, checksums, sources + licence evidence, future layers
```

Nothing here is new doctrine except where marked **Choice**. The clause rule
for Greek (s.8) is a **proposal**, and nothing in the files depends on it.

---

## 1. Identity: the verse already has a uid

House style s.2: *two editions are still two witnesses of one passage.* A
Greek verse and a KJV verse are that relation. John 1:1 has carried its uid
since the KJV witness build (2026-09-17), so this build **mints nothing**.
It opens the registry frozen and asks it for `kjv:John.1.1`. The pilot reuses
18 uids and mints 0.

- **The citation stays `kjv:John.1.1`.** The slug names the **versification of
  record**, not the language. Every passage now carries `versification: "kjv"`
  to say so. A neutral alias (`bible:` or `nt:`) would be a registry
  ruling for Adam, and it could not be a second uid.
- **A Greek verse with no KJV uid is a hard stop**, never a fresh uid.
  Across the whole NT that happens three times (s.10).
- **The reading of record is not moved.** `build_witnesses.py` declares
  `kjv.plain`. This build leaves it and sets `grc.byz` to
  `reading_of_record: false`. Making the Greek the default would be a ruling,
  not a build.
- **No pericope container is minted.** `pericope: "John.1.1-18"` is a label.
  If the reader or a deck needs to point at the Prologue as one thing, that
  wants a range citation grammar, and a uid once minted can never be taken
  back (R5). Decide the grammar first.

## 2. What differs from the Latin hymns

| | Latin hymns (`data/hymns/`) | Greek NT (`data/nt/`) |
|---|---|---|
| row unit | the **clause** (ruling #10) | the **verse**. The clause is proposed as a span layer (s.8) |
| container | the stanza, a `unit: "stanza"` passage | none minted; `pericope` is a label |
| uids | minted by the build, one per clause | **reused**: the KJV verse uids; registry frozen |
| citation | `hymns:adoro-te.st3.c3` | `kjv:John.1.14` (versification of record) |
| original witness | `la.1` | `grc.byz` (Greek, Byzantine textform); a critical text would be `grc.crit` |
| witness text | lines joined by `\n` | one verse string, punctuated as RP prints it |
| extra witness field | — | `paragraph_starts`: RP's ¶ as token positions |
| reading of record | `la.1` | `kjv.plain`, unchanged (see s.1) |
| token `line` | the stanza line | absent: a verse has no lines |
| `translit` | always null (Latin script) | always filled (s.5) |
| `lemma` | Whitaker, else the house draft | Strong's 1890 headword for Robinson's number |
| `lemma_key` | the WORDS dictionary form | `G<n>`: Robinson's Strong's number |
| `parsing` | prose (`1 sg pres ind act`) | Robinson's code verbatim (`V-PAI-1S`); `describe_parsing()` gives the words |
| `gloss`, `plain_form` | house draft, never null | **null**: no public-domain contextual gloss |
| `en.wooden`, `en.plain` | generated witnesses | absent until glosses exist (they are generated *from* glosses) |
| alignments | stanza rendering → its clauses | `grc.byz` → `kjv.plain`, verse to verse, same uid |
| licence classes | PD, own, `free-grant` (Whitaker only) | PD, own. Nothing else |

## 3. The records

**passages.jsonl.** `uid`, `citation`, `kind: "passage"`, `unit: "verse"`,
`book` (OSIS), `osis`, `chapter`, `verse`, `versification`, `pericope`,
`reading_of_record`, `status`.

**witnesses.jsonl.** `address` (`<uid>/grc.byz`), `passage_uid`, `name`,
`lang: "grc"`, `role: "original"`, `register: "koine"`,
`textform: "byzantine"`, `text` (the CCAT csv verse, verbatim),
`paragraph_starts`, `generated: false`, `source`, `attested: "Y"`,
`reading_of_record: false`.

**tokens.jsonl.** `address` (`<uid>/grc.byz.t04`), `passage_uid`, `witness`,
`position` (1-based in the verse), the eight fields, `lemma_key`, `syntax`
(null), `provenance` (`{lemma, parsing}`), and `review`.

| field | content | null when |
|---|---|---|
| `surface` | the word as RP prints it, edge punctuation and ¶ off, the elision mark `’` kept | never |
| `normalized` | `NFC(surface)` | never |
| `search_key` | NFD, every combining mark dropped, elision mark dropped, lowercased, every sigma `σ` | never |
| `translit` | the house scheme (s.5) on `normalized` | never |
| `lemma` | Strong's headword for `lemma_key` | Strong's has no entry (none in the whole NT) |
| `parsing` | Robinson's code; the first, where he gives two | never, from RP |
| `gloss` | — | always, today |
| `plain_form` | — | always, today |

`provenance.parsing.status` is `single` or `alternatives`. Where it is
`alternatives`, the other codes are listed and the token carries a `review`
reason. **The build never chooses.** In the pilot this is one word in John 1:9,
the participle that can agree with "the light" or with "every man". Robinson
parses it both ways, and so do the files.

**alignments.jsonl.** One per verse:
`<uid>/grc.byz` ↔ `<uid>/kjv.plain`, `level: "section"`, `type: "1:1"`,
`confidence: "high"`. The note says what the alignment does not claim: the KJV
translates the Textus Receptus, so this aligns verses, not readings. The KJV
side lives in `data/books/kjv.witnesses.json`, which is rebuildable and
gitignored. The validator checks the name against `build_witnesses.WITNESSES`.

`plain` and `wooden` are never stored, the same as for the hymns.

## 4. The source and its licence

**Robinson–Pierpont, *The New Testament in the Original Greek: Byzantine
Textform* (2018)**, from its official home, `github.com/byztxt/byzantine-majority-text`,
pinned at release `v3.3.2` = commit `27a45ff` (2024-12-31). Read 2026-09-26:

| where | what it says (verbatim) |
|---|---|
| repo `README.md`, "Copyright" | "All the code and text contained in this folder is in the Public Domain." |
| repo `LICENSE.txt` | The Unlicense: "This is free and unencumbered software released into the public domain." |
| `byztxt/robinson-documentation` `README.md` (Robinson's parsing docs) | "Public Domain.  Copy freely." |
| RP2005 printed edition, copyright page (archive.org) | "All rights to this text are released to everyone and no one can reduce these rights at any time." The full paragraph is in the manifest. |
| RP2018 printed edition, copyright page (archive.org, item licence CC0) | The same release, extended to the 2018 edition. The scan's OCR is garbled, so it is **not quoted**. Read it off the page image before quoting it anywhere. |

The editors **request, and do not require,** that their names, the title and
the disclaimer travel with reproductions. The manifest's `attribution` honours
that.

The parsing codes and Strong's numbers are Robinson's own work (his
2009 `PARSING.COD`/`DECLINE.COD`) in the same repo, under the same statement.
**They are public domain.** So `parsing` is his, verbatim.

**Lemmas: Strong's *Dictionary of the Greek Testament* (1890).** The XML's own
prologue says "Public Domain -- Copy Freely". The file (openscriptures/strongs
`0acd2f2`) is byte-identical to the one this repo already ingests as
`strongs-greek`. RP carries **no lemma of its own**, only the Strong's number.
Robinson re-points many numbers to their practical root (every form of εἰμί →
1510, εἶπον → 3004), so the headword looked up through his number is a better
lemma than Strong's own numbering would give. It is still Strong's headword,
not a modern lexicon's (s.9).

## 5. Transliteration: SBL academic, with two house choices

The SBL Handbook of Style, 2nd ed., s.5.3 (table 5.3.1 and notes 5.3.2):

| Greek | Latin | | Greek | Latin |
|---|---|---|---|---|
| α | a | | ν | n |
| β | b | | ξ | x |
| γ | g; **n** before γ κ ξ χ (note 1) | | ο | o |
| δ | d | | π | p |
| ε | e | | ρ | r; **rh** initially and for the second of ρρ (note 3) |
| ζ | z | | σ ς | s |
| η | ē (note 2) | | τ | t |
| θ | th | | υ | y; **u** in αυ ευ ηυ ου υι (note 4) |
| ι | i | | φ | ph |
| κ | k | | χ | ch |
| λ | l | | ψ | ps |
| μ | m | | ω | ō (note 2) |

The rough breathing is **h**, placed before an initial vowel or diphthong
(note 5). Accents are dropped. SBL says it "makes no provision" for iota
subscript and diaeresis, so the house chooses:

- **Choice:** iota subscript is written as a following *i*: ᾳ → ai, ῃ → ēi, ῳ → ōi.
  This matches the transliterations in the Strong's XML.
- **Choice:** the diaeresis is kept (ϊ → ï, ϋ → ÿ). It also blocks the
  diphthong rule, so Μωϋσῆς → Mōÿsēs.
- A capital stays a capital (Ἰησοῦς → Iēsous). The elision mark stays (δι’ → di’).

Checked two ways. First, 14 fixtures taken from the SBL notes' own examples.
Second, the scheme was run against the transliterations in the Strong's
dictionary, with accents set aside: **it agrees on 5,505 of 5,506 one-word
headwords.** The one disagreement is χξϛ, the numeral 666, which Strong's
spells out in words.

## 6. How the build refuses to guess

RP ships each verse twice. The CCAT csv has accents and punctuation. The BP5
csv is unaccented, with Strong's numbers and parsing. The tokens need both.

1. **Pairing.** The CCAT words and the BP5 words are paired in order, and every
   pair must have the same letters (`search_key`). One mismatch is a hard stop.
2. **Against Robinson's own files.** The CSVs are the maintainers' conversion.
   Robinson's Beta-code files are "the ultimate source of truth". The build
   re-reads both `.TXT` (CCAT) and `.BP5` and stops if any word's letters, or
   any number or code, differ. The CCAT apparatus blocks (`{N … > … }`) are
   stripped, not read as text, and counted by siglum in the manifest (3 NA
   notes in 1:16–18).
3. **The parsing grammar.** Every code must match Robinson's documented grammar
   (`PARSING_RE`). All 1,055 distinct codes in the NT do.

What is *not* re-checked: accents and breathings. They come from the maintainers'
Beta→Unicode converter, and the manifest's `open` field says so.

## 7. Counts (pilot)

| | |
|---|---|
| verses | 18 (uids reused 18, minted 0) |
| tokens | 253; 83 distinct lemmas |
| tokens with lemma / parsing / gloss | 253 / 253 / 0 |
| finite verbs | 41 (38 indicative, 3 subjunctive); also 6 participles, 1 infinitive |
| tokens flagged for review | 1 (Robinson's double parsing, 1:9) |
| RP paragraph marks | 0 in this range |

## 8. Proposed, not imposed: a clause rule for Greek

The hymns are cut by clause because a line that leans on a verb in another
line renders wrongly on its own. Prose has the same problem inside a verse.
14 of these 18 verses have two or more finite verbs, and 1:15 has six. The
proposal:

**The rule.** A row is a clause: a finite verb (indicative, subjunctive,
optative or imperative) and every word it governs. This is the hymn rule,
with Greek's own cases:

- a **participle** goes with the clause whose verb it modifies. So does an
  **infinitive** governed by a verb. A **genitive absolute** may stand as its
  own row, since it hangs on no word;
- a clause with its own finite verb **may** stand: relative (ὅς), ὅτι, ἵνα,
  ὡς, καί-coordinate;
- a **verbless clause** with the copula understood counts as a clause
  (1:6b has one);
- **punctuation is not a cut.** RP's commas and raised dots are an
  editor's. Every cut records its `why`, as the hymn joins do.

**The storage (recommended): clauses as spans, not passages.** Give
`grc.byz` a `clauses` list of `{span: [first, last], anchor: <position of the
finite verb>, why}` over its token positions. The reserved span address
(`<uid>/grc.byz@<first>-<last>`, house style s.3) names each one. The verse
stays the identity, because it is the unit every Bible reference, deck and
proof text already uses. The alternative, minting clause passages as the
hymns do, fails in two ways:

- it would mint tens of thousands of uids;
- a sentence routinely crosses a verse boundary (1:12–13 is one sentence, whose
  relative clause in 1:13 has its own verb), so clause passages would not
  partition verses.

Under the proposed rule every clause in 1:1–18 has its finite verb inside its
own verse. That is a first reading and has not been checked. The cut is house
work (licence `own`) and would be drafted by hand, as the hymn cuts were.

## 9. Future enrichment layers (named, never merged)

| layer | licence | where it goes |
|---|---|---|
| MorphGNT (SBLGNT morphology, lemmas) | CC BY-SA 3.0 | never into these files. ShareAlike is a separate layer keyed by address, if ever |
| SBLGNT text | CC BY 4.0 | waits on ADR 0019. If admitted, it is a second witness `grc.crit` on these same uids, in its own file with its own rights block |
| Perseus | CC BY-SA 4.0 | cited by CTS URN, a separate layer (ADR 0001) |

A modern lemma spine for Greek (launch plan D3: "Morpheus/treebanks") would
need a licence read per source. The public-domain options are the ones used
here: Strong's by Robinson's number now, and later Thayer's (1889, already
OCR'd in this repo by page) or Abbott-Smith (1922) re-keyed.

## 10. What a full-NT run takes

Measured with `--survey`, which reads all 27 books at the pinned commit and
writes nothing:

| | |
|---|---|
| RP verses | 7,953 |
| tokens | 140,149 |
| accented ↔ parsed pairing failures | **0**, once ¶ is treated as punctuation (it was 874 verses before) |
| Beta cross-check failures | **0** |
| Robinson codes that fail the grammar | **0** (1,055 distinct) |
| Strong's numbers with no headword | **0** |
| words with alternative parsings | 28 |
| finite verbs | 19,571 |
| RP verses with no KJV uid | 3: Rom 14:24–26, RP's placement of the doxology that the KJV prints as Rom 16:25–27 |
| KJV verses RP lacks | 7: the Textus Receptus verses Luke 17:36, Acts 8:37, 15:34 and 24:7, and Rom 16:25–27 (moved, above) |

So a full run needs:

1. **A versification map with one entry.** RP Rom 14:24–26 ↔ KJV Rom 16:25–27.
   It is a ruling: the doxology is one passage whose position differs, so it
   takes the KJV uids and the witness records where RP places it. The four
   TR-only verses simply have no `grc.byz` witness. Nothing is guessed.
2. **Pins for 108 more files** (27 books × 4). The sha256s come from `--survey`'s
   cache.
3. **Sharding.** The pilot runs about 540 bytes per token. The whole NT would be
   about **76 MB** in one `tokens.jsonl`, over GitHub's 50 MB warning. Options:
   - one file per book under `data/nt/<Book>/` (the largest book is about
     11 MB);
   - moving the constant `provenance` to the manifest, with only the
     exceptions kept per token (provenance is 37% of the pilot's token bytes);
   - leaving tokens gitignored and rebuildable, as `data/books/` is. The pins
     make it reproducible.

   The recommendation is per-book shards plus the provenance change.
4. **Time:** the survey reads and checks the whole NT in a few seconds.
   The build is the same work plus writing. The real cost is review: 28
   double parsings, and Adam's rulings on the doxology and the citation slug.

## 11. Commands

```
python3 pipeline/build_nt_corpus.py --fetch    # pinned inputs -> data/corpus/ (gitignored)
python3 pipeline/build_nt_corpus.py --check    # mint 0, byte-identical
python3 tests/nt_corpus_test.py                # the validator
python3 pipeline/build_nt_corpus.py --survey   # the whole NT, measured; writes nothing
```
