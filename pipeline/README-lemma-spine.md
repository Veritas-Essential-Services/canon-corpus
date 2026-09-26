# The Latin lemma spine — Whitaker's WORDS

*Schema `wordhoard/lemma-table/v1`. Launch plan D3. Built by
`pipeline/build_lemma_spine.py` (library: `pipeline/whitaker.py`), applied to
tokens by `pipeline/lemma_spine.py`, validated by `tests/lemma_spine_test.py`.*

A lemma spine means every Latin token points at one dictionary headword from a
named, licensed source. Glosses, decks and a concordance can then join on the
lemma rather than on spelling. For Latin, the source is William Whitaker's
WORDS.

```
python pipeline/build_lemma_spine.py --fetch   # once: the pinned Whitaker files
python pipeline/build_lemma_spine.py           # the table + the hymn analyses
python pipeline/build_hymn_corpus.py           # tokens take lemma/parsing from them
python tests/lemma_spine_test.py               # 44 checks
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
 "sources": ["DICTLINE.GEN:1291", ...]}
```

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
- the dictionary form, character for character (`dictionary_form.adb`).

**Not ported:** TRICKS, SLURY, SYNCOPE and FIXES (prefix and suffix
composition), and frequency trimming. An `unknown` may therefore still be
reachable by the full program. Today there is one: *pellicane* (WORDS spells
it *pelicanus*).

**Filled by the house, and marked `form_by: "house"`.** WORDS prints no
dictionary form for pronouns of declension 1 (*qui*, *quis*) or 5 (*ego*,
*tu*, *nos*, *vos*, *sui*). `whitaker.HOUSE_PRONOUN_FORMS` supplies the
conventional headings for 9 lemmas.

## 5. Measured 2026-09-26 (the 263 hymn tokens)

| | |
|---|---|
| distinct forms | 222; 221 analysed, 1 unknown |
| lemma from Whitaker | **244** (162 sole candidate, 82 chosen by the draft among several) |
| lemma kept from the draft | 19: 9 disagree, 9 ambiguous, 1 unknown |
| parsing from Whitaker | 84; plus 10 confirmed with the draft's note kept |
| parsing: draft consistent, Whitaker ambiguous | 145 |
| parsing disagreements | 5 |
| **flagged for review** | **24 tokens** |

Most disagreements are convention rather than error. WORDS files *se* under
*sui*, *nobis* under *nos*, *supremus* under *superus*, *duodeni* under
*duodecim*, and spells *subjicio* where the text has *subiicit*. The parse
conflicts are real questions for Adam: *et* and *ergo* (adv or conj), and
*Thomas* (Greek 1st declension, or indeclinable as WORDS has it).

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
