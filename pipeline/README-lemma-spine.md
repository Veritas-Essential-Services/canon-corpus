# The Latin lemma spine — Whitaker's WORDS

*Schema `wordhoard/lemma-table/v1`. Launch plan D3. Built by
`pipeline/build_lemma_spine.py` (library: `pipeline/whitaker.py` and
`pipeline/whitaker_tricks.py`), applied to tokens by `pipeline/lemma_spine.py`,
validated by `tests/lemma_spine_test.py` and `tests/whitaker_tricks_test.py`.*

A lemma spine means every Latin token points at one dictionary headword from a
named, licensed source. Glosses, decks and a concordance can then join on the
lemma rather than on spelling. For Latin, the source is William Whitaker's
WORDS.

```
python pipeline/build_lemma_spine.py --fetch   # once: the pinned Whitaker files (+ Ada source)
python pipeline/build_lemma_spine.py           # the table + the hymn analyses
python pipeline/build_hymn_corpus.py           # tokens take lemma/parsing from them
python tests/lemma_spine_test.py               # 64 checks
python tests/whitaker_tricks_test.py           # 63 checks: one or more per ported rule
python pipeline/build_lemma_spine.py --check   # committed lemma files byte-identical
```

---

## 1. Source and licence

| | |
|---|---|
| program | WORDS 1.97F, William A. Whitaker (1936–2010) |
| files | `DICTLINE.GEN`, `INFLECTS.LAT`, `UNIQUES.LAT`, `ADDONS.LAT`, `LICENCE.txt` |
| from | github.com/mk270/whitakers-words, commit `1f2f0fb0867a896d7b9284a03d615ed635d6f992` |
| pinned | sha256 of every file, in `whitaker.PINS` and the manifest; a mismatch is a hard stop |
| cached at | `data/corpus/whitaker/<commit[:12]>/` (gitignored, like every fetched corpus) |

**Licence: not public domain.** WORDS is copyright Whitaker, with an
unconditional grant. His own documentation says:

> Permission is hereby freely given for any and all use of program and data.

It also says all parts of WORDS, source code and data files, are "made freely
available to anyone who wishes to use them, for whatever purpose". The evidence
is the author's WORDSDOC (Wayback snapshot 2010-12-27 of users.erols.com, sha256
recorded) and `LICENCE.txt` at the pinned commit. The full grant is quoted
verbatim in `manifest.source.grant_verbatim`.

The house gate was PD-or-own (launch plan D4, ADR 0001). This grant is neither,
so it goes in as its own class, **`free-grant`**, admitted for Whitaker only. It
is marked `open` for Adam's ruling. The validator fails any other source that
claims it. Two further notes: a headword such as *adoro* is a fact, not an
expression, and the grant's courtesy ("at least tell me") can no longer be
honoured, because the author died in 2010.

## 2. The files

`data/lemmas/whitaker-la/`

| file | committed | one row per |
|---|---|---|
| `lemmas.jsonl` | **no** (about 16 MB; rebuildable; sha256 in the manifest) | Whitaker lemma |
| `hymns.analyses.jsonl` | yes | distinct hymn form (`search_key`) |
| `hymns.lemmas.jsonl` | yes | lemma the hymn analyses name (the hymns' slice of the table) |
| `manifest.json` | yes | source, pins, licence, counts, checksums, `unknown_forms` |

**A lemma** is one WORDS *dictionary form*, the string WORDS prints above
its meanings. For example: `adoro, adorare, adoravi, adoratus  V (1st) TRANS`.
That string is the row's `key`. Dictionary lines that share a form, such as the
thirty `qu` lines that head `qui, quae, quod`, are one lemma with several
`entries`. Each entry keeps its DICTLINE line number, four stems, part of
speech, flags (age, area, geography, frequency, source) and English meaning.

```
{"key", "lemma" (principal parts), "headword" (folded), "pos",
 "form_by": "whitaker" | "house" | "none", "entries": [{"source": "DICTLINE.GEN:1291", ...}]}
```

**An analysis** is one way WORDS reads a form:

```
{"key", "lemma", "headword", "pos", "form_by",
 "parse": {"pos": "V", "decl": [1,1], "tense": "PRES", ...},
 "whitaker": "V 1 1 PRES ACTIVE IND 1 S",       # as WORDS prints it
 "enclitic": null | "que" | "ne" | "ve" | "est",
 "via": [...],                                  # only when a rule was needed (s.4)
 "sources": ["DICTLINE.GEN:1291", ...]}
```

`via` lists the rules WORDS needed to read the form, outermost first, e.g.
`[{"kind": "TRICK", "table": "Mediaeval_Tricks", "rule": "internal e/ae",
"as": "cenae", "explain": ...}]`. `kind` is `SYNCOPE`, `SLURY`, `TRICK`,
`PREFIX`, `SUFFIX` or `TWO_WORDS`; `as` is the form WORDS actually looked up;
`explain` is WORDS's own explanation line. A plain analysis has no `via`.

## 3. How a token gets its lemma and parsing

The hymn build (`build_hymn_corpus.py`) reads **only** the committed
`hymns.analyses.jsonl`, so it runs offline. The rule is in `lemma_spine.resolve`.

**Lemma.**

1. Keep only the Whitaker analyses whose headword is the draft's headword
   (folded: no macrons, lowercase, j→i, v→u).
2. Prefer those consistent with the draft's parsing.
3. If several entries remain, the draft's own lemma can choose among them.
   These filters are soft, applied in this order:
   - its part of speech: a gender tag means a noun, `-a, -um` an adjective;
   - its other principal parts: `-stitī` picks *praestiti* over *praestavi*;
   - its case: `spēs` over the proper noun `Spes`.
4. If exactly one entry is left, take Whitaker's principal parts as `lemma`
   and the dictionary form as `lemma_key`.
5. Otherwise **keep the draft** and flag the token: `disagree` (another
   headword), `ambiguous` (several entries the draft cannot choose between)
   or `unknown` (no analysis).

Readings WORDS reaches only by a rule (s.4) take part like any other, with
two limits. A lemma taken from one records the rule in `provenance.lemma.via`.
A reading only by prefix or suffix formation names the base word, never the
compound, so it can only `disagree`; it is listed as e.g. `pellex, pellicis
(by suffix -an)` and gets its own review reason. And WORDS's two-words guesses
are **never taken**: WORDS itself prints "If not obvious, probably incorrect".
A form with nothing else stays `unknown`, the guess kept in
`provenance.lemma.whitaker_guess`.

**Parsing** (only once the lemma is Whitaker's).

- **`whitaker`**: Whitaker gives exactly one parse for that entry, the draft
  is consistent with it, and the draft commits to one value per feature it
  names. `parsing` becomes Whitaker's parse, written in the house's
  abbreviations.
- **`confirmed`**: as above, but the draft carries a teaching note Whitaker
  cannot express (`impersonal`, `(-iō)`, `postpos`, `conj + subj`). The
  draft is kept verbatim.
- **`draft-consistent`**: Whitaker gives several parses and the draft fits
  at least one. The draft is kept. This is normal for Latin (*te* is acc or
  abl) and is not flagged.
- **`disagree`**: no Whitaker parse fits the draft. The draft is kept, and the
  token is flagged.

"Consistent" means every feature the draft names (case, number, gender,
person, tense, mood, voice, degree, declension/conjugation, part of speech)
is present in Whitaker's parse and agrees with it. Whitaker's `X` matches
anything, and `C` (common gender) matches m or f. Features the draft does not
mention constrain nothing.

**Every token records both values, whichever wins.** New token fields:

| field | content |
|---|---|
| `lemma_key` | the Whitaker dictionary form; null where the draft stands |
| `provenance.lemma` | `{source, status, draft, candidates, ...}`, plus `sources` (DICTLINE lines) or `whitaker` (what Whitaker said instead) |
| `provenance.parsing` | `{source, status, draft, whitaker_parses, whitaker, ...}` |
| `review` | null, or a list of reasons for Adam |

Putting `provenance.*.draft` back reproduces the pre-D3 lemma and parsing
exactly. The test checks every draft against the vault batch files.

## 4. What is ported from WORDS, and what is not

The code is ported from the Ada source at the same commit, rule for rule:

- stem + ending matching with u=v and i=j (`word_package.adb`,
  `inflections_package.adb`);
- the verb filters (`list_sweep.adb`);
- uniques;
- the enclitics (`parse.adb`);
- `sum`, which `makedict_main.adb` inserts rather than listing in DICTLINE;
- the dictionary form, character for character (`dictionary_form.adb`);
- **SYNCOPE** (`tricks.adb`): *audiit* = *audivit*, *amasti* = *amavisti*,
  *amarunt* = *amaverunt*, *audierunt* = *audiverunt*, *dixti* = *dixisti*;
- **SLURY** (`trick_tables.adb`): assimilated prefixes, *obpono* = *oppono*,
  *comloco* = *conloco*;
- **FIXES** (`word_package.adb`, Prune_Stems / Apply_Prefix / Apply_Suffix /
  Reduce_Stem_List): the 129 prefixes and 179 suffixes of `ADDONS.LAT`, one
  of each at most, e.g. *super-* + *laudabilis* + *-iter*;
- **TRICKS** (`tricks.adb`, `trick_tables.ads/.adb`): the first-letter tables,
  `Any_Tricks` (*ae*/*e*, *oe*/*e*, *ph*/*f*, *h*/-), `Mediaeval_Tricks`
  (Harrington/Elliott: *e*/*ae*, *ci*/*ti*, *t*/*th*, ...), a terminal
  *-iis* on adjectives, *is*/*iis* for *eo*, doubled consonants written
  single, and two words run together;
- the order WORDS tries all of this in (`parse.adb`, Pass and
  Parse_Latin_Word): plain; SLURY if nothing; SYNCOPE unless a form of *esse*
  is there; the enclitics; FIXES if still nothing; TRICKS last, then TRICKS on
  the form less an enclitic.

The tables are copied row for row, and `whitaker_tricks_test.py` compares
them with the Ada (pinned by sha256 in `whitaker.ADA_SOURCES`, fetched by
`--fetch`). Where the port departs from the Ada it says so at the top of
`whitaker_tricks.py`. In short: the forms are already folded (v→u, j→i), so
the tables are folded too and cannot tell consonantal *v* from *u*; WORDS's
"is this the perfect system?" looks only at the last record of an internally
sorted array, here any record counts; one branch of SLUR can never fire in
the Ada (it compares strings of different lengths) and is not ported; and
Roman numerals, the non-enclitic TACKONs and PACKONs are still not ported.
Frequency trimming is not ported either: every analysis is kept.

WORDS assumes at most one trick per word ("the chances are 1/1000", its
comment says). So *leticia* (needs both *ae* and *ti*) stays out of reach, as
it is in WORDS.

**Filled by the house, and marked `form_by: "house"`.** WORDS prints no
dictionary form for pronouns of declension 1 (*qui*, *quis*) or 5 (*ego*,
*tu*, *nos*, *vos*, *sui*). `whitaker.HOUSE_PRONOUN_FORMS` supplies the
conventional headings for 9 lemmas.

## 5. Measured 2026-09-26 (the 263 hymn tokens)

| | |
|---|---|
| distinct forms | 222; 222 analysed, 0 unknown |
| lemma from Whitaker | **244** (161 sole candidate, 83 chosen by the draft among several) |
| lemma kept from the draft | 19: 10 disagree, 9 ambiguous |
| parsing from Whitaker | 84; plus 10 confirmed with the draft's note kept |
| parsing: draft consistent, Whitaker ambiguous | 145 |
| parsing disagreements | 5 |
| **flagged for review** | **24 tokens** |

Most disagreements are convention rather than error. WORDS files *se* under
*sui*, *nobis* under *nos*, *supremus* under *superus*, *duodeni* under
*duodecim*, and spells *subjicio* where the text has *subiicit*. The parse
conflicts are real questions for Adam: *et* and *ergo* (adv or conj), and
*Thomas* (Greek 1st declension, or indeclinable as WORDS has it).

**Before and after the rules (same day).** On these hymns the rules change
little, because the hymn forms are already dictionary spellings and TRICKS
and FIXES only run when nothing plain is found:

| | before | after |
|---|---|---|
| forms unknown | 1 (*pellicane*) | 0 |
| lemma status | 162 agree, 82 agree-selected, 9 disagree, 9 ambiguous, 1 unknown | 161, 83, 10, 9, 0 |
| lemma from Whitaker / flagged | 244 / 24 | 244 / 24 |

*Pellicane* is no longer unknown, but not because WORDS knows the pelican.
DICTLINE at the pinned commit has no *pelicanus* in any spelling. WORDS now
reads the form as *pellex, pellicis* ("concubine") plus the adjective suffix
*-an-*: a mis-analysis. The token is still flagged, now as `disagree`, and the
draft's lemma stands. SYNCOPE adds a second reading to *moras* (*moveras*)
and *caro* (*cavero*). The draft's headword still picks the right lemma for
both, so only the candidate counts change.

Where the rules matter is medieval spelling. Every hymn form was respelled
the medieval way (*ae*→*e*, *oe*→*e*, *ti*→*ci*, a doubled consonant
single), 30 respellings in all. WORDS without the rules found the right
lemma for 3 of them. With the rules it finds 22. The test measures this
figure.

## 6. Not here

- **ADR 0012's lemma bridge (archaic English: shew→show, holpen→help)** is not
  built. The ADR requires one ("without the bridge a concordance is silently
  wrong") but does not specify its table, source or format. It needs a
  specification before it can be built, and it is English, not this Latin
  spine.
- **Greek** (Morpheus, treebanks) is out of scope for D3's first pass.
  Licences as read on 2026-09-26:
  - Morpheus: MPL-2.0 (perseids-tools/morpheus);
  - the Perseus AGLDT treebank: CC BY-SA 3.0 US, so under ADR 0001 it is
    referenced by CTS URN and never merged in;
  - PROIEL: CC BY-NC-SA 3.0;
  - Gorman's treebanks: CC BY-NC-SA 4.0.

## 7. Adding forms

A new hymn adds forms, and the hymn build hard-stops on any `search_key` that
has no analysis row. `build_lemma_spine.py` therefore reads its forms from two
places: the committed tokens, and every stanza in the vault batch files that
`build_hymn_corpus.HYMNS` names, when the vault is reachable. So the order is:

1. add the hymn to `HYMNS`;
2. run `build_lemma_spine.py`;
3. run `build_hymn_corpus.py`;
4. commit `data/lemmas/` and `data/hymns/` together;
5. bump `EXPECTED` in `tests/lemma_spine_test.py`.

## 8. Adam's answers: the overrides file

The flagged tokens are listed for review in `docs/review/2026-09-26-lemma-flags.md`.
His answers go in `data/lemmas/adam-reviewed.jsonl` (committed, LF, empty until
then). There is one JSON row per answered token:

```
{"address": "wh-0Y016CRD3W/la.1.t01",   # the token's address (tokens.jsonl)
 "surface": "Praesta",                   # must equal the token's surface: a guard
 "lemma_key": "praesto, praestare, praestiti, praestitus  V (1st)",
 "lemma": "...",                         # optional: a lemma of his own
 "parsing": "...",                       # optional
 "reviewed_on": "2026-09-27",
 "note": "..."}                          # optional
```

- **`lemma_key` alone** takes that Whitaker entry. It must be one of
  Whitaker's analyses of the form, and its principal parts become the lemma.
- **`lemma`** sets a lemma as written (with `lemma_key`, or with none when no
  Whitaker entry fits).
- **`parsing`** sets the parsing as written. A lemma answer does not re-run
  the parsing check, so answer both if both matter.

`build_hymn_corpus.py` applies each row after `lemma_spine.resolve`, through
`lemma_spine.apply_override`. The overridden field's provenance becomes
`{"source": "adam-reviewed", "status": "adam-reviewed", "reviewed_on", "note",
"draft", "was": {...what it replaced...}}`. The review reasons he answered
are cleared, and any others stand. The hymn manifest declares the
`adam-reviewed` source (license `own`) and the file's sha256 once a row is
applied. A malformed row, a key Whitaker does not have, a surface that no
longer matches, or a row for a token that does not exist stops the build. An
answer is never dropped silently.
