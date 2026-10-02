---
model_log:
  - 2026-09-26 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
  - 2026-09-26 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
fable_review: pending
---
# The Greek New Testament in the corpus JSONL (the whole NT; pilot John 1:1–18)

*Schema `wordhoard/corpus-jsonl/v1`, the same four files as the hymns
(`README-hymn-jsonl.md`), with the differences written down here. Built by
`pipeline/build_nt_corpus.py`, validated by `tests/nt_corpus_test.py`.
Launch plan D2 (format), D3 (lemma spine), D4 (licence gate) and D5 (reader
datasets), the Greek half. 2026-09-26.*

```
data/nt/<Book>/passages.jsonl     one line per verse (the passage that already exists)
data/nt/<Book>/witnesses.jsonl    one line per Greek rendering of a verse (grc.byz)
data/nt/<Book>/tokens.jsonl       one line per word of that rendering
data/nt/<Book>/alignments.jsonl   one line per verse: grc.byz faces kjv.plain
data/nt/manifest.json             one over all 27 books: counts, shards, checksums,
                                  sources + licence evidence, rulings, future layers
```

`<Book>` is the OSIS book (`Matt` … `Rev`). Since 2026-10-02 the build covers
the whole NT; the John 1:1–18 pilot is now a labelled pericope inside
`data/nt/John/`, its records byte-identical to what the pilot wrote. Read the
files through `build_nt_corpus.load_nt()`, which follows the manifest's
`shards` block, so no consumer needs to know the layout (s.16).

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
| `gloss` | house draft, never null | **Strong's dictionary gloss** by a fixed rule (s.12); null where no rule fires; an override row replaces it with a contextual one |
| `plain_form` | house draft, null where the gloss serves | null unless an override row sets it (s.12) |
| `en.wooden`, `en.plain` | generated witnesses | `en.wooden` absent: wooden is rendered straight from the glosses. `en.plain` as the hymns carry it, from `prose-order.jsonl` (s.14) |
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
`reading_of_record: false`. Beside it, where a prose order exists, the verse's
`<uid>/en.plain`: `lang: "en"`, `role: "plain"`, `text: null`,
`generated: true`, `prose_order`, `absorbed`, `plain_override`, `source`,
`attested: "N"`, and `draft`/`drafted_on` or `reviewed_on` (s.14).

**tokens.jsonl.** `address` (`<uid>/grc.byz.t04`), `passage_uid`, `witness`,
`position` (1-based in the verse), the eight fields, `lemma_key`, `syntax`
(null), `provenance` (`{lemma, parsing, gloss}`), and `review`.

| field | content | null when |
|---|---|---|
| `surface` | the word as RP prints it, edge punctuation and ¶ off, the elision mark `’` kept | never |
| `normalized` | `NFC(surface)` | never |
| `search_key` | NFD, every combining mark dropped, elision mark dropped, lowercased, every sigma `σ` | never |
| `translit` | the house scheme (s.5) on `normalized` | never |
| `lemma` | Strong's headword for `lemma_key` | Strong's has no entry (none in the whole NT) |
| `parsing` | Robinson's code; the first, where he gives two | never, from RP |
| `gloss` | Strong's 1890 dictionary gloss for `lemma_key`, by the rule in `provenance.gloss.rule` (s.12). **Not a contextual translation**, unless an override row replaced it (`provenance.gloss.kind: "contextual"`, the dictionary value under `was`) | no rule fires and no override applies (none in the pilot since the 2026-09-26 house draft; the dictionary left 22) |
| `plain_form` | the gloss's form in the plain line, set only by an override row | no override sets one |

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

## 7. Counts

The whole NT, measured 2026-10-02 (`tests/nt_corpus_test.py`, `EXPECTED_NT`):

| | |
|---|---|
| verses | 7,953 in 27 shards (uids reused 7,953, minted 0) |
| tokens | 140,149; 5,380 distinct lemmas |
| tokens with lemma / parsing / gloss | 140,149 / 140,149 / 131,631 (93.9%; 124,516 before s.17) |
| dictionary glosses by rule | kjv-form 27,855; paradigm 7,103; kjv-sole 20,489; kjv-in-def 52,792; def-head 23,255 |
| no gloss | 8,518: 7,642 function words, 871 with no usable head, 5 pronouns in crasis |
| finite verbs | 19,571 |
| tokens flagged for review | 28 (Robinson's double parsings) |
| largest file | `Luke/tokens.jsonl`, 13 MB |
| KJV verses with no Greek witness | 4: Luke 17:36, Acts 8:37, 15:34, 24:7 (Textus Receptus only) |

The pilot, John 1:1–18 (`load_nt(pericope="John.1.1-18")`), unchanged:

| | |
|---|---|
| verses | 18 (uids reused 18, minted 0) |
| tokens | 253; 83 distinct lemmas |
| tokens with lemma / parsing / gloss | 253 / 253 / 253; the dictionary alone 246, 231 before s.17 (s.12) |
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

*Done 2026-10-02: s.16 says how, and which two answers are still house
defaults. Kept as the record of what was measured first.*

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
python3 pipeline/review.py status              # the John 1 drafts: answered / open (s.15)
python3 pipeline/review.py apply docs/review/2026-09-26-john1-drafts.md
```

## 12. Glosses: Strong's dictionary glosses, by a fixed rule

*Added 2026-09-26. Code: `pipeline/strongs_gloss.py`. Tests: `tests/nt_corpus_test.py`
("glosses", "the gloss rule, on fixtures", and against the pins).*

**What they are.** Each gloss is the sense Strong's 1890 dictionary gives
for the token's Strong's number (`lemma_key`), chosen by the rule below.
**They are dictionary glosses, not a contextual translation.** One number
gets one gloss in every verse, whatever the verse means (an article or
pronoun varies only with its person, number, gender and case). The manifest's
`gloss` block says so, and the reader says so under the wooden column.

**What a Strong's entry gives.** A short definition, and the KJV renderings
after `:--`. Petersen's XML splits Strong's paragraph between
`<strongs_derivation>` and `<strongs_def>` at its first semicolon, often
mid-sense, so the rule reads the two as one paragraph. The KJV renderings are
printed **alphabetically**, not by frequency, so "the first rendering" means
nothing by itself: λόγος's first is *account*, λαμβάνω's *accept*. The rule
lets Strong's own definition choose among them.

**The rule.** The first step that fires sets the gloss, and its id goes on
the token as `provenance.gloss.rule`.

| id | tokens | what it does |
|---|---|---|
| `kjv-form` | 49 | Articles and personal, demonstrative and relative pronouns (Robinson T, P, D, R): the first KJV rendering, in Strong's order, that is an English form agreeing in person, number, gender and case (the table `FORMS`). None agrees: null. Strong's defines these by their grammar, not a sense, so there is no fallback. |
| `paradigm` | 15 | *Added 2026-10-02 (s.17).* Personal pronouns (Robinson P, not crasis) whose entry Strong's calls a pronoun, when `kjv-form` finds no agreeing rendering: the AV form for the token's person, number, gender and case, from the house table `PARADIGM` (I/me/my, we/us/our, thou/thee/thy, ye/you/your, he/him/his, she/her/her, it/it/its, they/them/their). In the pilot all 15 sit under house drafts, so the pilot's visible glosses do not move. |
| `kjv-sole` | 24 | The entry has exactly one usable KJV rendering. |
| `kjv-in-def` | 116 | The usable KJV rendering that occurs earliest, as a whole word, in the definition. Clauses about derivation ("from G…", "a primary verb") or grammar ("the first person singular…") are set aside, and text outside parentheses is searched before text inside. A pronoun form never glosses a non-pronoun. A rendering of one or two letters ("of", "to") counts only as the first word of a clause, or for a verb after "to". |
| `def-head` | 42 | Nouns, adjectives and verbs only: the head of the first sense clause. Parentheses come off; it is cut at the first comma, "i.e." or " or "; a leading "properly," etc., "a"/"an", and for a verb "to"/"I" are dropped. More than four words is not taken. |
| (none) | 7 (22 before s.17) | null, with the reason in `provenance.gloss.why`. Before s.17 that was 15 pronouns with no agreeing KJV form (13 masculine αὐτός, whose entry has no standalone *him*/*his*; 2 plural forms Robinson files under ἐγώ, whose entry lists only *I*, *me*), and 7 function words with no KJV rendering in the definition (πρός ×2, ἀλλά ×2, χωρίς, ἔμπροσθεν, ἀντί). |

"Usable" rendering: Strong's marks with **X** a rendering that comes from a
Greek idiom and with **+** one that needs other words; both are skipped.
Parenthesised parts are Strong's optional additions, so the base is taken
without them. There is one part-of-speech adjustment: a noun takes the noun
variant Strong's prints, so σκοτία's `dark(-ness)` gives *darkness*.

**Never invented.** The test re-derives every gloss from the pinned XML. It
checks that each KJV-rule gloss is one of the entry's usable renderings (or
its printed variant), and that each `def-head` gloss is words of Strong's
definition. Coverage in the pilot: **246 of 253 tokens (97.2%)**, 231 (91.3%) before the paradigm rule (s.17).

**What the dictionary gets wrong, as expected.** Some glosses are etymological
or odd in context: ἀρχή *commencement*, φῶς *luminousness*, λέγω
*lay forth*, ἀποστέλλω *set*, περί *with*. The rule is not tuned to rescue
them. That is the override layer's job.

**The override layer (contextual glosses).**
`data/nt/gloss-overrides.jsonl` (committed, LF) has the shape of
`data/lemmas/adam-reviewed.jsonl` (README-lemma-spine.md s.8):

```
{"address": "wh-…/grc.byz.t05",   # the token's address
 "surface": "λόγος",               # must equal the token's surface: a guard
 "gloss": "…",                     # and/or "plain_form"
 "layer": "adam-reviewed",         # or "house"
 "reviewed_on": "2026-09-27",
 "note": "…"}                      # optional
```

The build applies a row after the dictionary rule. The token's
`provenance.gloss` becomes `{source: <layer>, kind: "contextual",
reviewed_on, note, was: {value: <the dictionary gloss>, source:
"strongs-1890", rule, …}}`, so the dictionary value is never lost. The
manifest declares the layer as a source (licence `own`) and the file's
sha256 once a row is applied, and counts rows in `gloss.by_override`. A
malformed row, a surface that no longer matches, or a row for a token that
does not exist stops the build.

**Draft rows (added 2026-09-26).** A house proposal awaiting Adam's review
carries `"draft": true` and `"drafted_on"` in place of `reviewed_on`, and
only layer `house` may be a draft. Its provenance says `draft: true,
drafted_on` (no `reviewed_on`), the manifest counts it in
`gloss.overrides.draft` and `drafts`, and the reader badges every column it
reaches. To accept a row, drop `draft`/`drafted_on`, date it `reviewed_on`
(layer `adam-reviewed` if it is now his), and rebuild.

**The first house draft (2026-09-26): 137 rows, all draft.** Every token
where the dictionary gloss misleads in context, and the 22 nulls: the
`def-head` glosses (all 42), tense and mood the dictionary cannot carry (ἦν
*was*, not *exist*), pronouns by use (αὐτοῦ *him* after a preposition, *his*
after a noun), case where English needs a preposition (*of-God*), and the
words the plain line needs a finite form for (`plain_form`, e.g. a verb
absorbing its οὐ as *did-not-know*). Word glosses in the hymns' hyphenated
style, at most four words; each row has a one-line reason in `note`. House
work, not copied from any translation or lexicon. Reviewed per verse in
`docs/review/2026-09-26-john1-drafts.md`.

## 13. The reader: Greek columns and the KJV witness

`pipeline/render_reader.py` renders the Greek through the hymns' own renderers:

- **wooden** is `build_hymn_corpus.render_wooden()` over the verse's tokens in
  Greek order. A word with no gloss is shown as a marked gap (—), never as a
  made-up word. The column is labelled "dictionary glosses, not a translation",
  and says how many of its words are contextual house glosses instead.
- **plain** is `build_nt_corpus.render_plain()`, which is the hymns'
  `render_plain()` with the Prologue's names (John, Moses, Father) added to
  the capital-keeping list, over the verse's `en.plain` witness (s.14). A
  verse with no `en.plain` shows **"not yet ordered"**.
- **Drafts are marked.** A wooden column that uses a draft gloss, and a plain
  column whose prose order is a draft, carry the badge **"draft — awaiting
  Adam's review"**, and the popover says "draft" beside the gloss's source and
  shows the dictionary gloss it replaced.
- **KJV** is a fifth, separately labelled column. It is not one of the four,
  and it is not `elegant`. It is the verse's `kjv.plain` witness under the same
  uid, read from `data/books/kjv.witnesses.json`, a gitignored build
  (`structure_texts.py`, then `build_witnesses.py`). Where that build is absent,
  the column says so. The KJV translates the Textus Receptus, not this Greek,
  and the column says that too.
- **Rights.** The KJV is public domain in the US. In the UK it is under the
  Crown patent (rights review 2026-09-26, s.6). The manifest's `facing_witness`
  block records the basis and `rights_note: "Crown patent: KJV print not for
  UK"`, and the reader prints both under Sources & rights.

## 14. The plain line: a house prose_order (draft)

*Added 2026-09-26. File: `data/nt/prose-order.jsonl` (committed, LF). Built into
`en.plain` witnesses by `build_nt_corpus.py`; validated by `tests/nt_corpus_test.py`.*

**The convention is the hymns', exactly** (README-hymn-jsonl.md s.5):

- an **integer** is a token position of the verse's `grc.byz`; that token's
  `plain_form`, or else its `gloss`, is emitted;
- a **string** is a word English needs and the Greek lacks, shown
  `[bracketed]` (the 0:1 alignment);
- **`absorbed`** lists positions carried by a neighbour's form (many:1): an
  article folded into its noun (τὸν θεόν *God*), οὐ folded into its verb's
  `plain_form` (*did-not-know*);
- **`plain_override`** is a whole-line string for a verse no permutation
  reaches. Null everywhere; the loader refuses one until it is needed.

Every token is used exactly once, by the order or by absorption
(`permutation_problems()`, the hymns' rule). A walked token must have a gloss
or a `plain_form`: the build stops rather than render a gap. The plain line is
rendered, never stored.

**A row:**

```
{"passage_uid": "wh-…", "citation": "kjv:John.1.2",   # the citation is a guard
 "prose_order": [1, 2, 3, "the", 4, 5, 7], "absorbed": [6],
 "plain_override": null,
 "source": "house-draft",                             # a key of PROSE_SOURCES
 "draft": true, "drafted_on": "2026-09-26"}           # or reviewed_on, once Adam has
```

`house-draft` is declared in the manifest's `sources` (licence `own`,
`status: "draft"`), so the licence gate admits it as the house's own work. The
manifest's `prose_order` block states the convention and counts, and its
`drafts` block counts every draft row of both files and names the review doc.
A malformed row, a citation that does not match its uid, or an order that is
not a permutation stops the build.

**The first draft: all 18 verses, all draft.** Four choices in it are
flagged for Adam in the review doc rather than settled: 1:5 κατέλαβεν
(*grasped*: understood or overcame), 1:9 ἐρχόμενον (with *every man*,
following Robinson's first parse, or with *the light*), 1:14 ἐσκήνωσεν
(*dwelt*, or the literal *tented*) and 1:16 ἀντί (*in place of*). The supplied words are
few and bracketed: articles English needs, a subject pronoun where the Greek
verb carries it, *was* in 1:6, *came* in 1:8, and *him* in 1:18.

## 15. Answering the review doc: `pipeline/review.py`

*Added 2026-09-26. Tests: `tests/review_test.py` (on a temp copy of the repo).*

Adam answers `docs/review/2026-09-26-john1-drafts.md` in its **Adam:** cells
(one per gloss row) and its **Adam (plain line):** line (one per verse), then:

```
python3 pipeline/review.py apply docs/review/2026-09-26-john1-drafts.md --dry-run
python3 pipeline/review.py apply docs/review/2026-09-26-john1-drafts.md
```

| answer | a gloss row | a plain line |
|---|---|---|
| `✓` or `ok` | accepted: layer `adam-reviewed`, `draft`/`drafted_on` dropped, `reviewed_on` added; gloss, plain_form and note kept | accepted: source `adam-reviewed`, dated the same way |
| a string | the gloss, now Adam's. On a row that also has a `plain_form`, the run stops: say which | a prose_order, `[1, "the", 2, …]`, optionally followed by `absorbed [11]` (the sheet's own `` `prose_order` … · `absorbed` … `` line pastes back as is) |
| `gloss: …; plain_form: …` | those fields (`plain_form: none` removes it) | — |
| `draft→` | nothing: the draft stands | nothing |
| `draft→ <value>` | the draft revised, still `draft: true`, `drafted_on` today | the order revised, still a draft |
| blank | nothing, ever | nothing, ever |

A gloss must be a word gloss (at most four words, no markup), and a
prose_order must be a permutation of the verse's tokens. An order that leaves
positions out without saying `absorbed […]` stops, naming them. So does an
English sentence in place of an order, `x or y`, a question mark, or `ok but …`.
Every stop names the verse and the word, and nothing is written until every
answer reads cleanly. Rows are rewritten in place, in the file's order and key
order. `build_nt_corpus.py` then rebuilds, and its `--check` runs. If the build
refuses, the files are put back. A second apply writes nothing.

To reject a draft outright, delete its row from `gloss-overrides.jsonl`: the
dictionary gloss comes back. The tool does not delete. A replaced gloss's
house draft survives only in git history (`provenance.gloss.was` holds the
dictionary value, as before).

`adam-reviewed` is one source for both files, licence own, declared in the
manifest once a row uses it. A reviewed row is never a draft. The manifest's
`drafts` block counts what is still open, and says `none open` at zero.
`render` rebuilds the doc from `data/nt/` and
`docs/review/2026-09-26-john1-drafts.notes.json` (its prose, with the row
counts filled in). It is byte-identical while nothing has changed. An accepted
row shows `✓`, and a revised draft shows its new value with the cell open again.

## 16. The full run (2026-10-02): two house defaults, each one edit

The build now reads every book (`SCOPE` in `build_nt_corpus.py`). A narrowed
`SCOPE` is for tests and `--report` only: the build refuses to write or
`--check` one, because the manifest would lose the other books (the
partial-build trap in CLAUDE.md). It needed the two answers s.10 named. Both
are still **Adam's rulings**. Until he makes them, the build uses the
defaults below, the manifest records each under `rulings`-style blocks with
`status: "house default, awaiting Adam's ruling"`, and changing either is one
edit and a rebuild. Nothing downstream hard-codes either answer.

**Ruling 1: the Romans doxology.** Default: the doxology is one passage whose
position differs (s.10's recommendation). RP Rom 14:24–26 are `grc.byz`
witnesses of the KJV uids of Rom 16:25–27, and each such witness carries
`rp_ref` (`"Rom.14.24"` …), RP's own reference. Rows keep RP's reading order,
so in `data/nt/Rom/` they follow 14:23. The manifest's `versification` block
lists `placed_elsewhere`, `left_out` and `kjv_verses_without_grc`.

- *To rule the other way:* set the values of `VERSIFICATION_MAP` to `None`.
  The three RP verses are then left out and counted (`left_out`), KJV Rom
  16:25–27 join the TR-only verses with no Greek witness, and nothing is
  minted. The validator builds Romans that way to prove it.

**Ruling 2: sharding.** Default: one folder per book, the four files in
each, one `manifest.json` over all of them (its `shards` block: `layout`,
`order` in canon order, per-book `dir`, `verses`, `tokens`). Token records are
unchanged: provenance stays on every token. The whole is 97 MB on disk and
about 7 MB gzipped; the largest file is 13 MB, under GitHub's 50 MB warning
(the validator checks this).

- *To change it:* `SHARD = None` writes the four flat files (tokens ~76 MB,
  over the warning); the other options in s.10 (provenance moved to the
  manifest, or tokens gitignored and rebuilt from the pins) are larger
  changes and would want their own PR.

**What else changed.**

- **Pins.** The 108 book files (27 × 4) are pinned in
  `pipeline/nt_pins.json`, measured at `BYZ_COMMIT`. A mismatch stops the
  build as before. (raw.githubusercontent.com rate-limits a bulk `--fetch`;
  a clone of byztxt at that commit, copied into `data/corpus/byztxt/27a45ff1b7be/`,
  gives byte-identical files.)
- **`pericope`** is `"John.1.1-18"` on the pilot verses and `null` on every
  other. The reader and the John 1 review sheet read just the pilot through
  `load_nt(pericope=…)`, whose manifest is a view with the pilot's own counts.
- **Overrides and prose orders** still cover John 1:1–18 only. Every other
  verse has dictionary glosses and no `en.plain`. A row for a book outside a
  narrowed `SCOPE` is skipped, not stale.
- **`--check`** also fails on an output file the build would not write (the
  pilot's old flat files), and a write removes such files. Shards are written
  before the manifest, each by temp file and rename.
- **The validator's def-head check** now asks that every word of the gloss be
  a word of Strong's definition (his parentheses come out, so a head like
  *lead under*, from "to lead (oneself) under", is not one substring).

**Seen in the full run:** a handful of `def-head` glosses read oddly once the
parentheses come out, and 7,214 pronouns, mostly masculine αὐτός, got no
gloss because Strong's entry has no standalone *him*/*his*. Both are fixed
by the gloss-rule changes in s.17.

## 17. Gloss-rule changes after the full run (2026-10-02)

Coverage went from 124,516 to **131,631 of 140,149 (93.9%)**. The rule is
still a fixed function of (parsing, Strong's entry), and the validator still
re-derives every gloss and checks it is never invented.

- **`paradigm` (new, 7,103 tokens).** See s.12. Strong's lists only some
  forms of the personal pronouns (σύ: *thou*; ἐγώ: *I, me*; αὐτός: no
  standalone *him*/*his*), and the rest are English grammar, not sense. The
  form comes from a house table, and the rule id says so. It is a dictionary
  gloss like the rest: αὐτοῦ is *his* in every verse, even where context
  wants *him* (after a preposition), and an intensive αὐτός (*himself*, *the
  same*) is still *he*. Fixing that by use is the override layer's job, as
  before. Crasis (κἀμοί, `-K`) stays null, because *and me* is not *me*:
  5 tokens.
- **A demonstrative or relative with no agreeing form** now goes on to the
  sense rules instead of stopping null; articles and personal pronouns
  still stop. In the NT this gives one more gloss (ἕως ὅτου's *whiles*).
  τοιοῦτος and τοσοῦτος still find no rendering in their definitions and stay
  null as function words.
- **def-head.** A parenthesis that opens "or" and holds two or more words is
  a whole alternative reading, so the head stops before it: G2507
  `lower demolish` becomes *lower*. A one-word "(or esteem)" still alternates
  with the word before it (*render glorious*). A head cut at " or " that
  leaves a dangling "in a X" drops it: G2745 `boast in a good` becomes *boast*.
- **Two broken entries in the XML.** Petersen's conversion lost the `:--`
  before the KJV rendering in G259 and G3372, so the rendering read as the
  end of the definition (`length length`). `strongs_gloss.XML_REPAIRS`
  restores them at load time; the source file is not edited. They are the
  only two of the 104 entries with no `<kjv_def>` that carry definition text.
- **The pilot.** The 15 pronouns the dictionary left null in John 1:1–18 now
  have a paradigm gloss under their house drafts (`provenance.gloss.was`), so
  the review sheet's *dictionary* column shows it. The drafts themselves are
  unchanged, and what the reader shows does not move.

Left alone deliberately: `under contrary to` (G5227, 2 tokens) and similar
heads where Strong's parenthesis glosses a prefix. A rule for them would be
fitted to one entry.
