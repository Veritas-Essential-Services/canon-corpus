# The corpus JSONL — passages, witnesses, tokens, alignments

*Schema `wordhoard/corpus-jsonl/v1`. First instance: `data/hymns/` (Adoro te and
Pange lingua), built by `pipeline/build_hymn_corpus.py`, validated by
`tests/hymn_corpus_test.py`. Launch plan D1–D2.*

This is the Corpus Architecture's four levels (vault: *Word Hoard — Corpus
Architecture* §2 and §8) written down as files, with the house identity rules
(*HOUSE STYLE — Addressing and Identity*) applied. Nothing here is new doctrine;
where a choice had to be made, it is marked **Choice** and can be overruled.

```
passages.jsonl     one line per passage (the idea; language-neutral)
witnesses.jsonl    one line per rendering of a passage
tokens.jsonl       one line per word of a tokenized witness
alignments.jsonl   one line per link between witnesses
manifest.json      counts, checksums, sources + licences, the legacy join
```

Records are flat and joined by **uid**, never nested and never joined by a
legacy `unit_id` or by position.

---

## 1. The row unit for verse is the clause

Ruling #10 (2026-09-16): verse is stored by clause, not by line. A line
that leans on a verb in another line renders wrongly on its own, and a hymn
enjambs most of the time.

**The rule used to cut.** A hymn row is a clause: a finite verb and every word
it governs.

- Lines **must** be joined when a word on one line depends on a finite verb on
  another: a participle agreeing with that verb's subject, an infinitive it
  governs, a conjunction whose verb is on the next line.
- A clause with its own finite verb (relative, causal, coordinate) **may**
  stand as its own row. Pange lingua's cut keeps one conditional with its main
  clause (st4 ll.4–6); that cut predates this rule and is kept as made.
- A vocative, or a complete verbless exclamation, governs nothing and is
  governed by nothing, so it stays a row of its own.

Every joined clause records its grammatical reason in `cut.why`. The validator
fails a join with no reason.

*Adoro te* went from 27 line rows to **23 clauses**, with five joins (st3, st4,
st5 and st7 ll.3–4, and the existing st6 ll.3–4). *Pange lingua* keeps its
**12 clauses** from the 2026-09-16 retrofit.

### The stanza stays, as the container

**Choice.** The stanza keeps its existing uid and becomes a `unit: "stanza"`
passage that lists its clauses. It holds no Latin and no tokens, because the
text is stored once, on the clauses. It survives because it is still a real
unit: Hopkins and Caswall render stanzas, the Oratorium sings stanzas, and a
deck card pointing at a stanza uid should keep resolving to something that
says where its text went.

This is **not** recorded as a registry `split`. A split moves the parent uid
onto its largest child, which would make a stanza uid mean one clause, and
that stops being true the moment Hopkins' stanza hangs off it.

---

## 2. passages.jsonl

| field | clause | stanza | notes |
|---|---|---|---|
| `uid` | ✓ | ✓ | `wh-XXXXXXXXXX`, from `wh_uid.WhUidRegistry`, never by hand |
| `citation` | `hymns:adoro-te.st3.c3` | `hymns:adoro-te.st3` | house grammar `<slug>:<path>` |
| `kind` | `passage` | `passage` | kind is a field, never in the uid (R6) |
| `unit` | `clause` | `stanza` | |
| `work` | `hymns:adoro-te` | same | |
| `stanza`, `clause` | ints | `stanza` only | |
| `lines` | `[first, last]` in the stanza | `[1, n]` | a clause may span lines |
| `stanza_uid` | ✓ | — | the container |
| `clauses` | — | `[uid, …]` in order | must partition the stanza exactly |
| `grade`, `memorize` | ✓ | ✓ | per the Battle Plan |
| `reading_of_record` | `la.1` | — | the witness a bare citation resolves to |
| `cut` | `{by, why}` | — | `why` required when `lines` spans more than one line |
| `notes` / `teacher_notes` | ✓ | ✓ | house teaching notes |
| `status` | ✓ | ✓ | `machine-draft, unchecked` until Adam checks |
| `legacy` | `{unit_ids: […]}` | `{id}` | the old keys; read once by the build, never joined on |

## 3. witnesses.jsonl

A witness is a rendering of a passage and has no identity of its own. Its
address is `<uid>/<name>`.

| field | notes |
|---|---|
| `address`, `passage_uid`, `name` | `name` is what the rendering *is*: `la.1`, `en.wooden`, `en.plain`, `en.elegant`, `en.singable`, `en.literal` |
| `lang`, `role`, `register` | language lives here and nowhere else: never in a uid, citation, file or folder name |
| `text` | the rendering, lines separated by `\n`; **null when `generated`** |
| `generated` | true for `en.wooden` and `en.plain` |
| `prose_order`, `absorbed`, `plain_override` | `en.plain` only; see §5 |
| `source` | a key into `manifest.sources`, which carries the licence |
| `attested` | `Y`/`N`; composed text is flagged, never quarantined |
| `reading_of_record` | exactly one `true` per clause (`la.1`) |
| `cut_from` / `legacy_address` | where the text sat before the re-cut |

Stanza-level renderings (`en.singable`: Hopkins for Adoro te, Caswall for
Pange lingua; `en.literal`: Britt's 1922 prose) hang on the **stanza**,
because they render a stanza and not a clause. Hopkins moved from `en.elegant`
to `en.singable` under ruling #9, which lists Hopkins as a singable, not a
translation.

## 4. tokens.jsonl

One line per word of a tokenized witness (today, `la.1` only).

| field | content | null when |
|---|---|---|
| `address` | `<uid>/la.1.t04` | never |
| `passage_uid`, `witness`, `position`, `line` | position is 1-based within the clause; `line` is the stanza line, for verse display | never |
| `surface` | exactly as the reading of record has it; never cleaned | never |
| `normalized` | `NFC(surface)`; NFC only, never NFKC | never |
| `search_key` | NFD, combining marks dropped, lowercased, æ→ae, œ→oe, **j→i, v→u** | never |
| `translit` | romanization | **always null on a Latin-script witness**; filled for grc/he |
| `lemma` | dictionary headword: Whitaker's where it agrees with the draft, else the draft (D3) | no licensed or house source yet |
| `lemma_key` | the Whitaker dictionary form naming the lemma: the spine's join key | the draft stands (see `provenance`) |
| `parsing` | morphology: Whitaker's where it gives one parse the draft agrees with, else the draft | no licensed or house source yet; **a build never invents one** |
| `gloss` | the wooden gloss: Latin order, one hyphenated chunk per word, `[brackets]` for words on no peg | never |
| `plain_form` | the gloss's finite/idiomatic English form for the plain line | the gloss serves as-is |
| `syntax` | a teacher's note on the word's function | not drafted |
| `legacy_address` | the token's address before the re-cut | |
| `provenance` | `{lemma: {...}, parsing: {...}}`: the source, status, and the draft value, whichever won | never |
| `review` | reasons for Adam: Whitaker disagrees, is ambiguous, or has nothing | nothing to review |

Null means "no source yet". It never means "lost". The empty string is not
allowed. Where each field comes from is in `manifest.token_fields`. Since D3, `lemma` and
`parsing` come from Whitaker's WORDS where it agrees with the house draft, and
from the draft otherwise, never silently. The rules and counts are in
`pipeline/README-lemma-spine.md`.

## 5. `plain` is generated, never stored

The plain line is the tokens walked in `prose_order`:

- **an integer** is a token position; that token's `plain_form`, or else its
  `gloss`, is emitted.
- **a string** is a *supplied* word English needs and Latin lacks. It is shown
  `[bracketed]`: the 0:1 alignment.
- **`absorbed`** lists positions carried by a neighbour's form (many:1). The
  commonest case is `non` absorbed into the verb it negates.
- **`plain_override`** is a whole-line string for the rare line no permutation
  reaches. It is null everywhere today.

Every token is used exactly once, either by the order or by absorption. The
first word is capitalised, and other capitals are recomputed (the PROPER list
keeps *God*, *Lord* and so on). The pronoun *I* is never lower-cased.

The renderer is `render_plain()` in `build_hymn_corpus.py`. The wooden line is
`render_wooden()`: the glosses in Latin order. **No file contains a `plain` or
`wooden` key**, and the validator greps every record for one.

For a clause built from joined lines, `prose_order` is the line orders
concatenated. No word crossed a line break that had not already crossed it in
the retrofit.

## 6. alignments.jsonl

| field | notes |
|---|---|
| `alignment_id` | `<a address>~<b witness name>` |
| `level` | `section` (a rendering ↔ the clauses it faces) or `token` |
| `a`, `b` | lists of `{address, tokens}`; `tokens: null` means the whole witness |
| `type` | `1:1`, `1:many`, `many:1`, `many:many`, from the list lengths |
| `confidence` | `high` / `medium` / `low`, with a `note` when not high |

**Choice.** Today every alignment is `section`-level: a stanza rendering is
aligned to the `la.1` of each clause it faces. That relation is derivable from
stanza membership, and the validator checks that the two agree. It is stored
anyway, because the facing-page reader looks here and because `confidence`
says something membership can't: Hopkins' Adoro st6 opens with a clause that
has no Latin behind it, so it is `medium`.

Token-level rows arrive with the first independent tokenized second witness,
such as a Greek text, or the Vulgate against the Septuagint. The `la.1 → en.plain`
relation is *not* stored here: `prose_order` is its one home.

## 7. The manifest and the licence gate

Launch plan D4 and ADR 0001: only public-domain editions, or the house's own
work. Every `source` records `license` (`PD` | `own`), `license_basis`,
`edition`, `verified` and anything still `open`. The validator fails any other
licence.

**Perseus (CC BY-SA) is never merged in.** Enrichment from it is a separate
layer keyed by CTS URN and joined at read time. `manifest.perseus.cts_urn`
records the URN per work. Both hymns have none, so it is null, not guessed.

The manifest also carries `legacy_join` (every legacy `unit_id` → its clause
uid, read once), the sha256 of every input and output, and `cut_on`.

## 8. Adding the next hymn (mechanical)

1. Put its batch JSON and permutations JSON beside the others, or point
   `$WORDHOARD_LATIN_DIR` at them.
2. Add an entry to `HYMNS` in `build_hymn_corpus.py`: the legacy prefix, both
   files, where its stanza-level renderings come from, and the `clauses` table.
   Each clause is `(first line, last line, [legacy unit_ids], why)`.
3. Add any new source to `SOURCES`, with its licence read from the exact
   edition. Translations carry their own copyright.
4. `python pipeline/build_hymn_corpus.py`. It mints once, one uid per new
   clause. **Commit `data/uids/wordhoard.uids.json` with the data.**
5. Bump the counts in `tests/hymn_corpus_test.py`, then run it.
   `python pipeline/build_hymn_corpus.py --check` must mint 0.

The build refuses to guess. A legacy row that lands in no clause, tokens that
don't match surface for surface, a join with no reason, or a stanza uid that
disagrees with the registry are all hard stops.

---

## 9. Hymns from a printed edition (no vault batch, no house draft)

*Added 2026-09-26: Lauda Sion, Sacris solemniis, Verbum supernum prodiens
(launch plan Ring 3, "the hymns of Thomas").*

*Adoro te* and *Pange lingua* came to the corpus as vault batch notes: the
Latin, a house draft of every token (gloss, lemma, parsing, syntax) and a
house plain order. These three hymns have none of that. Their text comes
straight from one public-domain printing:

**Matthew Britt, *The Hymns of the Breviary and Missal* (1922)**, the same
printing Caswall's *Pange lingua* was verified against: Latin, a verse
translation and a literal prose translation for each. The scan is
`archive.org/details/hymnsofbreviarym00britrich`.

### 9a. The source file

`data/hymn-sources/britt-1922-corpus-christi.json` (committed; PD) holds, per
stanza: the Latin lines, the verse English, Britt's literal prose, and the
printed page of each. It also records the edition (title page and copyright
page), every scan page read with its image's sha256, and the transcription's
conventions. `HYMNS[slug]["source_file"]` points the build at it.

**Verified means read against the page image.** The scan's OCR text layer
was the starting point only, and it is wrong in ways that matter: *Nee* for
*Nec*, *Quern* for *Quem*, no ligatures, and *Vetera* where the page has
*vetera*. Every line was checked against the image.

**Conventions:**

- The Latin is exactly as printed: *æ*, *œ*, consonantal *j*.
- The display capital (LAUDA) is title case.
- A turned-over verse line is rejoined, and each word broken at a turnover is
  listed in the file.
- The English uses the house typography (straight quotes, `--`) and keeps
  Britt's metrical *-èd*.
- The literal prose is the quoted translation only, without Britt's commentary.

### 9b. What is stored

The same four files and records as the batch hymns, with these differences:

- **Passages.** No `legacy` block (there were no legacy ids). `grade` and
  `memorize` are null. `status` reads "text verified against Britt 1922; cut
  and lemmas unchecked". The stanza records its printed `page`.
- **Clause witnesses: `la.1` only**, source `britt-1922-latin`, with its
  `page`. There is **no `en.wooden`, `en.plain` or `en.elegant`**, and
  `manifest.works[..].not_stored` says why. A gloss and a plain order are house
  work, and none is invented, as for the Greek before its draft (README-nt-jsonl
  s.13). The reader shows those columns empty with that reason.
- **Stanza witnesses**: `en.singable` and `en.literal`, both from Britt, with
  their pages.
  - Lauda Sion is sung in Hugh T. Henry's translation.
  - Sacris solemniis is sung in "a cento based on the translation by J. D.
    Chambers".
  - Verbum supernum is sung in Neale's translation (st. 1-4) and Caswall's
    (st. 5-6).
  - Each witness is aligned to its clauses, as the batch hymns' are.
- **Tokens**: `gloss`, `plain_form` and `syntax` are null. `lemma` and `parsing`
  come from `lemma_spine.resolve_undrafted` (README-lemma-spine.md s.3b):
  Whitaker only where it leaves no choice, else null and flagged.

**Counts:**

| | stanzas | clauses | tokens |
|---|---|---|---|
| Lauda Sion | 12 | 45 | 286 |
| Sacris solemniis | 7 | 17 | 132 |
| Verbum supernum | 6 | 12 | 87 |

That is 99 uids minted, and nothing about *Adoro te* or *Pange lingua*
changed. Their records are the first lines of each file, byte-identical to
e9ed7f0, and the test pins that.

### 9c. The cut

The cut follows the s.1 rule, as *Adoro te*'s re-cut did. For these hymns
**every** clause records its reason in `cut.why`, one-line clauses included,
because every cut goes to Adam. The table is `HYMNS[slug]["clauses"]` as
`(first line, last line, why)`. Each clause's `cut.review` is `open` until
Adam answers.

### 9d. Adam's answers: `docs/review/2026-09-26-thomas-cuts.md`

`review.py` renders one row per stanza, showing the clauses with their lines
and reasons. The answers are:

- `ok` accepts the cut;
- `draft→` defers it;
- `cut: 1, 2-3, 4-6; note: …` re-cuts it. The note is required for any join the
  draft did not have.

`review.py apply` writes `data/hymn-sources/cut-reviewed.jsonl` rows
(`{stanza, cut, reviewed_on, note?}`), rebuilds, and runs `--check`. The build
applies them, and the clause's `cut` then says `review: adam-reviewed` with the
date.

**Identity under a re-cut.** A clause citation is positional (`st10.c2`). If a
reviewed re-cut puts different lines under a citation the draft already
minted, the build does three things:

1. It gives that citation a fresh uid (`wh_uid.mint_free`).
2. It records the old uid as superseded by the new one in the registry.
3. It writes `cut.supersedes` on the clause.

So an old address never silently means new words, and no uid is reused. A
citation the re-cut drops keeps its uid in the registry, as every vanished
citation does. A second, different re-cut of the same stanza is refused,
because it is a hand decision.

Lemma answers are keyed by clause uid, so the cut sheet comes first. A lemma
answer left on a re-issued clause stops the build rather than being dropped.
Their flagged tokens have their own sheet,
`docs/review/2026-09-26-thomas-lemma-flags.md`, answered into the same
`adam-reviewed.jsonl`.

### 9e. Adding the next printed hymn

1. Transcribe it into a source file under `data/hymn-sources/` from a named PD
   printing. Record the page and scan for every stanza, and check every line
   against the image, not the OCR.
2. Add a `HYMNS` entry with `source_file`, `latin_source`, `stanza_singable`,
   `stanza_literal` and the clause table, with every cut's reason. Add any new
   source to `PRINTED_SOURCES` with its licence basis.
3. Run `build_lemma_spine.py`, which reads the new forms from the source file,
   then `build_hymn_corpus.py`, then `build_lemma_spine.py` again (its
   manifest counts the tokens).
4. Run `review.py render` to add the stanzas and the flags to the sheets.
5. Bump the counts in `tests/hymn_corpus_test.py` and `tests/lemma_spine_test.py`.
   Add the hymn to `render_reader.WORKS` and to `export_mnemonicon_pack.HYMNS`.

---

## 10. Collating a batch hymn against a PD printing

*Added 2026-09-26: Adoro te against Britt 1922.*

*Adoro te*'s Latin came from the vault batch note as "received liturgical
text", with `verified: false` and an open item: check it against a named PD
printing. Britt 1922 prints it (no. 79, pp. 190-191). The collation measures the
corpus text against that printing and changes nothing in it.

**The printed text.** `data/hymn-sources/britt-1922-adoro-te.json` holds
Britt's Latin as printed, read from the page images (scan n199-n200, each
image's sha256 recorded) by the s.9a conventions. It is not an input of the
text, so it is not in `inputs_sha256`. `build_hymn_corpus.COLLATIONS` names it.

**The comparison.** `collate()` pairs the words of each stanza line, after
aligning on `search_key`. A word one side lacks does not shift the rest. Each
difference gets a kind:

| kind | meaning | search_key |
|---|---|---|
| `orthography` | æ/ae, œ/oe, j/i | same |
| `capital` | *Veritatis* / *veritatis* | same |
| `punctuation` | the marks around the word | same |
| `spelling` | *paenitens* / *pœnitens* | differs |
| `word` | a word only one side has | differs |

Its id is the received token's address and the kind
(`wh-…/la.1.t10:spelling`).

**The result (2026-09-26).** 149 received words and 148 printed; every
printed word pairs, and 124 are identical to the character. There are 25
differences: 12 punctuation, 10 orthography, 1 capital, 1 spelling (*paenitens*)
and 1 word (the closing *Amen*, which Britt does not print, as for *Pange
lingua*). The build writes this into `manifest.sources["roman-missal-received"]
.collation["hymns:adoro-te"]`. Those are verification fields only: a rebuild
changes no JSONL file and no uid.

**Adam's answers.** `docs/review/2026-09-26-adoro-collation.md` has one row
per difference. `ok` means the received reading stands, `britt` means Britt's
is preferred, and `draft→` leaves the row open. `review.py apply` writes
`data/hymn-sources/collation-reviewed.jsonl` (`{id, reading, reviewed_on,
note?}`), and the manifest counts the rows. The source becomes `verified:
true` only when every row is answered `ok`. A `britt` answer is recorded, not
applied, because the text is the batch note's and a change to it is made
there. After such a change, remove the answer row: its difference is gone, and
an answer to a difference that does not exist stops the build.

**Hopkins.** The singable is recorded as from the 1918 *Poems*, but that
edition prints no translations (Bridges's note, and the Project Gutenberg
transcription of it, ebook 22403). No PD printing of Hopkins's *Adoro te* was
reachable, so `hopkins-1918` stays unverified, with a `finding` saying why.
