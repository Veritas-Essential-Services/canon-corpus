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
python tests/whitaker_tricks_test.py           # 167 checks: one or more per ported rule
python pipeline/build_lemma_spine.py --check   # committed lemma files byte-identical
python pipeline/proper_names.py --fetch        # once: Hitchcock's Bible Names (s.10)
python pipeline/proper_names.py --check        # the names table byte-identical (needs the Vulgate)
python tests/proper_names_test.py              # 46 checks
python pipeline/review.py status               # Adam's review sheet: answered / open (s.8b)
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
`PREFIX`, `SUFFIX`, `TWO_WORDS`, `TACKON`, `PACKON`, `TICKON` or `ROMAN`;
`as` is the form WORDS
actually looked up; `explain` is WORDS's own explanation line. A plain
analysis has no `via`. A Roman numeral is its own lemma (`form_by:
"whitaker-roman"`, e.g. `MCMXCIX  NUM  (ROMAN)`, `value` 1999); an ill-formed
one, read leniently, is a `TRICK` from table `Bad_Roman_Number`.

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

## 3b. A token with no draft: `lemma_spine.resolve_undrafted`

*Added 2026-09-26, for the three hymns printed from Britt 1922
(README-hymn-jsonl.md s.9).* Those tokens have no house draft, so there is
nothing to choose among Whitaker's entries with, and nothing to fall back on.
The rule takes Whitaker only where it leaves no choice. It never guesses.

**Lemma.** Two-words guesses are set aside first, as above.

| WORDS gives | `lemma` / `lemma_key` | status | flagged |
|---|---|---|---|
| one entry | its principal parts / its key | `sole` | no |
| several entries, all with the same lemma (*in* +acc, +abl) | that lemma / null (the entry is a parse question) | `same-lemma` | no |
| several words (*panis*: *panis*, *pane*, *Pan*) | null / null, candidates in `provenance.lemma.whitaker` | `ambiguous` | **yes** |
| only a prefix/suffix formation | null / null | `disagree` | **yes** |
| nothing | null / null | `unknown` | **yes** |

**Parsing** is taken only when the lemma is taken from one entry, and that
entry gives exactly one parse (`whitaker`). If it gives several (*te*: acc or
abl), the parsing is null with status `ambiguous`, and it is **not** flagged.
Several parses is ordinary Latin, and choosing one means reading the line,
which is house work.

`provenance.*.draft` is null on every such token, and `source` is null where
nothing was taken. The overrides file (s.8) answers them the same way. A
`lemma_key` must still be one of Whitaker's analyses of the form. The sheet
is `docs/review/2026-09-26-thomas-lemma-flags.md` (s.8b).

**Measured 2026-09-26 (505 tokens).**

| | tokens |
|---|---|
| lemma `sole` | 273 |
| lemma `same-lemma` | 34 |
| lemma `ambiguous` | 193 |
| lemma `disagree` | 3 (*sumptionis*, *præsignatur*, *solemniis*: suffix and prefix readings) |
| lemma `unknown` | 2 (*Sion*, *Isaac*: proper names; the names table of s.10 has them, but the spine does not load it) |
| parsing `whitaker` | 140 |
| parsing `ambiguous` | 133 |
| parsing `unchecked` (no lemma taken) | 232 |
| **flagged** | **198** tokens, 152 distinct forms |

The forms grew from 222 to 547, with 2 unknown. The medieval-respelling
measure of s.5 on all 547 forms is 80 respellings: 9 recovered before the
rules, and 53 after.

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
- **Roman numerals** (`roman_numerals_package.adb`): Roman_Number rule for
  rule (*XIV* = 14, *IIII* = 4; *IIX*, *VL*, *XCL* refused), tried first and
  kept beside any other reading (*vi* is 6 and a form of *vis*); an
  ill-formed numeral is read by Bad_Roman_Number at the very end of TRICKS
  (*IIX* = 8), replacing any two-words guess, as in the Ada;
- **the non-enclitic TACKONs** (`word_package.adb`, Try_Tackons): *-cumque*,
  *-cunque*, *-cine*, *-pte*, *-ce*, *-modi*, *-dem*, *-cum*, *-vis*, *-met*,
  *-familias*, in `ADDONS.LAT` order, when Word finds nothing else (so inside
  every rule too): *egomet*, *mecum*, *nobiscum*, *quantuscumque*, *suapte*,
  *huiusmodi*, *paterfamilias*. A tackon keeps only readings of its own part
  of speech (a pronoun only of a declension it fits), and the first that hits
  wins;
- **Word's Qu block** (`word_package.adb`): the PACKONs of Process_Packons,
  a qu-pronoun with a tackon (*quidam*, *quicumque*, *quisquam*, *quispiam*,
  *quilibet*, *quendam* with its *n* turned back to *m*), tried when the form
  reads as at most one qu-pronoun record; and the TICKONs, a particle before
  a qu-pronoun (*siqua* = *si* + *qua*, *nescioquis*);
- **stem keys** as `makedict_main.adb` writes them: a one-stem comparative or
  superlative adjective (*interior*, *pessimus*, *summus*, *proximus*), a
  one-stem comparative or superlative adverb, and a numeral of one sort
  (*vicesimus*, ordinal) get the key of what they stand for, not slot 1; and
  an adverb's comparison comes from its own key table (*pejus* COMP,
  *pessime* SUPER). Both were found by the Vulgate benchmark
  (`docs/review/2026-09-26-benchmark.md`): before them *pessimus*, *summus*
  and *vicesimo* were unknown, and *verius* was read as a positive adverb;
- the order WORDS tries all of this in (`parse.adb`, Pass and
  Parse_Latin_Word): plain; SLURY if nothing; SYNCOPE unless a form of *esse*
  is there; the enclitics; FIXES if still nothing; TRICKS last, then TRICKS on
  the form less an enclitic;
- **capitalisation** (`parse.adb`, Is_Capitalized, with Ignore_Unknown_Names
  on, its default in `word_parameters.adb`): a word written with A-Z then a-z
  is taken for a name and gets **no TRICKS**. Nothing else is skipped: SLURY,
  SYNCOPE and the FIXES run inside Pass, before the test, so WORDS reads
  *Absalom* as *abs-* + a word too. The test reads the form as written
  (`raw`); called with only a search key, as the hymn build calls it, nothing
  is capitalised and nothing changes. Found by the Vulgate benchmark, where
  tricks had given *Hiram*, *Emath* and *Aser* wrong readings.

The tables are copied row for row, and `whitaker_tricks_test.py` compares
them with the Ada (pinned by sha256 in `whitaker.ADA_SOURCES`, fetched by
`--fetch`). Where the port departs from the Ada it says so at the top of
`whitaker_tricks.py`. In short: the forms are already folded (v→u, j→i), so
the tables are folded too and cannot tell consonantal *v* from *u*; WORDS's
"is this the perfect system?" looks only at the last record of an internally
sorted array, here any record counts; one branch of SLUR can never fire in
the Ada (it compares strings of different lengths) and is not ported;
Roman numerals are read from the form as written, because the search key has
already turned every *v* into *u*, which is not a Roman digit; and
Process_Qu_Pronouns is not ported as such, because ordinary stem + ending
matching already reads the qu-pronouns. Frequency trimming is not ported
either: every analysis is kept.

One bug fixed with this port (2026-09-26): the enclitic list was read
unfolded, so *-ve* was compared as `ve` against search keys where it is
always `ue`, and never stripped. It is folded now. No hymn form changed.

WORDS assumes at most one trick per word ("the chances are 1/1000", its
comment says). So *leticia* (needs both *ae* and *ti*) stays out of reach, as
it is in WORDS.

**Filled by the house, and marked `form_by: "house"`.** WORDS prints no
dictionary form for pronouns of declension 1 (*qui*, *quis*) or 5 (*ego*,
*tu*, *nos*, *vos*, *sui*). `whitaker.HOUSE_PRONOUN_FORMS` supplies the
conventional headings for 9 lemmas. It prints none for a qu-pronoun + PACKON
entry either; the house heads those `qui, quae, quod + -dam  PACK`, composed
rather than spelt out, because WORDS files *quisquam* under the adjectival
*qui*, and spelling the parts out would invent *quiquam*. Their headword is
the pronoun's (*qui*, *quis*): 17 more house lemmas.
`whitaker.HOUSE_PACK_HEADWORDS` offers real headings instead (*quidam, quaedam,
quoddam*; *quisquam, quaequam, quidquam*), from Lewis & Short where it heads
the word, behind a switch: `Whitaker(pack_headings="real")`,
`build_lemma_spine.py --pack-headings real`. The default stays the composed
heading until Adam chooses; both are listed in
`docs/review/2026-09-26-benchmark.md`. On the hymns the switch changes one
form's analyses (*quoque*'s PACKON readings) and no token.

One hymn form changed with these (2026-09-26), and no hymn token's lemma or
parsing: *quoque* gains WORDS's PACKON readings (*quo* + *-que*, from
*quisque*/*quique*: 5 candidates to 7), and *verius*, the adverb, is now
COMP where it was POS.

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

## 5b. Measured on a real text: the Clementine Vulgate

`pipeline/benchmark_whitaker.py` runs the analyzer over the whole Clementine
Vulgate: 612,029 running words, a public-domain text pinned by sha256 and kept
gitignored. It measures seven states of the port. The summary is
`docs/review/2026-09-26-benchmark.md`.

| | before the rules | with every rule and fix |
|---|---|---|
| forms unknown | 11.10% | 6.74% (plus 0.70% two-words guess only) |
| tokens unknown | 3.98% | 2.60% (plus 0.26% guess only) |

Nearly all that is left is proper names. Only 0.08% of the text is an unknown
that is ever written lower-case.

Three later states (same day) close that gap:

| | E: + capitalisation | F: + proper names (s.10) | G: + house supplement (s.9) |
|---|---|---|---|
| forms unknown | 7.71% | 0.41% | 0.35% (plus 0.14% guess only) |
| tokens unknown | 2.94% | 0.06% | 0.03% (plus 0.05% guess only) |
| tokens read | 97.01% | 99.89% | 99.92% |

E is WORDS's own rule, so it reads *less* than D: the trick readings it drops
were, on names, nearly all wrong. The prefix and suffix readings of names
stay in E, as they do in WORDS; the names table in F replaces them.

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

## 8b. Answering the sheet: `pipeline/review.py`

Nobody needs to write those rows by hand. Adam fills the sheet's **Adam:**
column, and the tool writes them:

```
python pipeline/review.py status                                  # answered / open, per sheet
python pipeline/review.py apply docs/review/2026-09-26-lemma-flags.md --dry-run
python pipeline/review.py apply docs/review/2026-09-26-lemma-flags.md
python pipeline/review.py render                                  # the sheet again, from the data
python pipeline/review.py render --check                          # is the sheet what the data says?
python tests/review_test.py                                       # 50 checks, on a temp copy
```

| in the Adam: column | what is written |
|---|---|
| `ok` or `✓` | the row's recommendation, exactly (kept in the notes file as `ok`) |
| `keep` | the draft value for what was flagged: `lemma` for a lemma flag, `parsing` for a parsing flag |
| a Whitaker key, e.g. `mundus, mundi  N (2nd) M` | `lemma_key` (matched with spacing folded, since markdown loses a double space) |
| any other string, on a lemma flag | `lemma`, as written |
| `lemma_key: …; lemma: …; parsing: …; note: …` | those fields, any of them |
| `as row 1` | row 1's answer |
| `draft→` | nothing: the draft stands and the token stays flagged |
| blank | nothing, ever |

Anything else stops the run **before anything is written**, and each stop
names the row: a bare string on a row flagged only for its parsing (say
`parsing: …` or `lemma: …`), `ok?` or `x or y`, `ok but …`, a `lemma_key`
Whitaker does not have for that form, `draft→ something` (a lemma answer has no
draft state). Each answer is checked with `apply_override` against the
token's own analyses before the file is touched.

An answered row is dated `reviewed_on` from the machine's clock (`--today`
overrides it, for tests), written in token order, and then
`build_hymn_corpus.py` rebuilds and its `--check` runs. If the build refuses,
the overrides file is put back. Applying the same sheet again writes nothing:
a row that already says what the answer says keeps its `reviewed_on`.

**The sheet is rendered, not hand-kept.** What the data cannot say (the prose
above and below the table, and each row's *Whitaker's candidates*, *Why
flagged* and *Recommend* cells, and the row `ok` writes) lives in
`docs/review/2026-09-26-lemma-flags.notes.json`. Everything else comes from
`data/hymns/` and the provenance's `draft`. `render` is byte-identical to the
sheet while the data is unchanged. After an apply, it shows each answered row
as `ok`, `keep` or its fields, so the rendered sheet applies as a no-op.
`render` refuses to overwrite answers that have not been applied yet
(`--force` drops them). The rows are the tokens in the notes file plus any
token flagged since, so a new flag appears with `—` in the hand-written cells
until the notes file gains them.

## 9. The house supplement

`data/lemmas/house-supplement.jsonl` (committed, LF) fills the gaps the Vulgate
benchmark found in DICTLINE's vocabulary, and nothing else: 24 rows, 34 forms.
It is **off unless asked for** (`Whitaker(house_supplement=True)`), so the
lemma spine's committed files do not change; the benchmark's state G turns it
on.

Every row has `"provenance": "house"`, an `id`, `attested` (form: count in the
Clementine Vulgate, checked against the text by the benchmark and by
`proper_names_test.py`) and a `justification` from public-domain attestation:
the Vulgate's own forms and, where it has the word, Lewis & Short (1879). A row
is one of two kinds:

- **an entry** in DICTLINE's terms: `stems` and `part` (e.g. `N 2 1 M P`), read
  by WORDS's own endings. With `only_forms` it reads just the forms it cites,
  so it can add nothing to any other form (*prophetidem*, but not *prophetis*,
  which is *propheta*'s dative plural);
- **forms** with their parse outright, as UNIQUES gives them (*basim*,
  `N 3 9 ACC S F`).

`of` names the Whitaker lemma the forms belong to (its dictionary form,
exactly: *emptitius* is DICTLINE's *empticius*); without it the row is a lemma
of its own, headed by `dictionary_form` and marked `form_by: "house"`. Either
way a reading's `source` is the row (`house-supplement.jsonl:7`), never a
DICTLINE line, and it carries `house: <id>`. A row without provenance,
justification or attestation, an `of` that is not a Whitaker form, or stems
that do not read the form stop the build.

Not supplied: *bahem* (one form; no public-domain lemma to hang it on),
*ixion* (a bird here; Lewis & Short has only the mythical Ixion), *horon* (a
fragment: the benchmark splits *Beth-horon* at the hyphen), *ejicicetur* (a
misprint).

## 10. Proper names

`data/lemmas/proper-names/names.jsonl` (committed, LF; built by
`pipeline/proper_names.py`, its manifest beside it) maps the Vulgate's proper
names, form by form, to a name lemma with part of speech **`proper`**. It is
consulted by `whitaker_tricks.parse_latin_word` for a **capitalised** form
only, beside WORDS's own dictionary lookup, as a name in DICTLINE would be. It
is loaded only when asked for (`X.names = proper_names.load()`); the lemma
spine does not load it.

Everything in it is derived mechanically; the method is in the module's
docstring and the manifest. In short:

1. **Candidates**: forms the Vulgate never writes lower-case, writes
   capitalised at least once in mid-sentence (not at a verse start or after
   `. : ? !`), and WORDS cannot read plainly: 3,574 forms, 18,507 tokens.
   190 forms (205 tokens) capitalised only where any word would be are held
   back and listed in the manifest.
2. **Lemmas** from the Vulgate's own inflected forms: a candidate ending in a
   Latin nominative ending heads the attested forms of its stem (*Jonathas*:
   *Jonathae*, *Jonatha*). No nominative the text does not write is ever
   supplied; a form with no paradigm is its own lemma ("one form": *Aaron*,
   322 tokens).
3. **Hitchcock's Bible Names Dictionary** (1869, public domain, CCEL's ThML,
   pinned by sha256): each lemma carries the headwords it matches, their entry
   ids and Hitchcock's gloss, verbatim, with the tier that matched (`exact`,
   `spelling`, `ending`). Nothing is added to what Hitchcock gives. The
   `ending` tier is the weakest (*Jacobus* ~ *Jacob*, *Antiochus* ~ *Antioch*
   are wrong identities; the lemma itself does not depend on it).

3,004 lemmas: 2,686 of one form, 318 with a paradigm; 1,017 matched in
Hitchcock (567 exact, 407 spelling, 43 ending).

A reading from the table: `{"key": "Jonathas  proper", "lemma": "Jonathas",
"form_by": "house-names", "parse": {"pos": "proper"}, "source":
"proper-names/names.jsonl:<line>"}`. The case of a name form is not given.
