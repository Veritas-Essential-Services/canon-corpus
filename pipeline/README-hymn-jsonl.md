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
| `lemma` | dictionary headword | no licensed or house source yet |
| `parsing` | morphology | no licensed or house source yet; **a build never invents one** |
| `gloss` | the wooden gloss: Latin order, one hyphenated chunk per word, `[brackets]` for words on no peg | never |
| `plain_form` | the gloss's finite/idiomatic English form for the plain line | the gloss serves as-is |
| `syntax` | a teacher's note on the word's function | not drafted |
| `legacy_address` | the token's address before the re-cut | |

Null means "no source yet". It never means "lost". The empty string is not
allowed. Where each field comes from is in `manifest.token_fields`. Today's
`lemma` and `parsing` are the house machine draft (unchecked); D3 re-derives
lemmas from Whitaker.

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
