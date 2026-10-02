---
model_log:
  - 2026-10-02 claude-opus-5-5 drafted
fable_review: pending
---
# The Latin key: Lewis & Short, linked to the Vulgate's words

*Built by `pipeline/build_latin_key.py`, tested by `tests/latin_key_test.py`.
This is the Latin twin of `README-strongs.md`.*

```
python3 pipeline/build_lemma_spine.py --fetch   # once: Whitaker's WORDS, pinned
python3 pipeline/fetch_sources.py               # once: the Clementine Vulgate
python3 pipeline/build_latin_key.py --fetch     # once: Lewis & Short, pinned
python3 pipeline/build_latin_key.py             # build data/lemmas/latin-key/
python3 pipeline/build_latin_key.py --check     # byte-identical
python3 tests/latin_key_test.py
```

## 1. Why this key

Hebrew and Greek words key on Strong's number, and BDB, Thayer and LSJ hang
off that number as witnesses. Latin has no numbered concordance, so the key is
the entry **Lewis & Short** (1879) gives the word. It is cited as
`lewis-short:<key>`, using Perseus's own entry key: `adoro`, `verbum`. A
homograph carries L&S's printed number: `malus1` is the adjective, `malus3` the
apple tree. L&S is the dictionary the field cites, and the one Perseus and
Logeion key on.

Getting there takes two steps:

1. **Form to lemma.** Whitaker's WORDS reads a form as written, *Verbum*, and
   gives its dictionary lemma, `verbum, verbi N (2nd) N`. This is the house
   analyzer, with its proper-names table and house supplement
   (`README-lemma-spine.md`).
2. **Lemma to L&S entry.** This build matches that lemma to its L&S entry, by
   the rules in s.3.

## 2. The files (`data/lemmas/latin-key/`, all committed, about 33 MB)

| file | one row per | what it holds |
|---|---|---|
| `lewis-short.jsonl` | L&S entry (51,645) | See below. No definition text. |
| `whitaker-ls.jsonl` | Whitaker lemma (40,827) | The L&S key(s) it links to, and the `status` saying how. |
| `vulgate-forms.jsonl` | Vulgate form as written, lower-cased (46,316) | Token count, Whitaker lemmas, L&S keys, `status`. |
| `strongs-latin.jsonl` | Strong's number with a Latin equivalent (4,057) | The L&S entries the Vulgate uses where the KJV has that number, scored (s.4c). |
| `vulgate-concordance.jsonl` | L&S key the Vulgate uses (8,609) | `sure` verses (the form alone decides), `resolved` verses by rule id (s.4b), and `possible` verses (left null). |
| `manifest.json` | — | Pins, rights, counts, what is not claimed. |

Each `lewis-short.jsonl` row holds:

- `key` and `citation`;
- the Perseus entry id (`n981`);
- the homograph number;
- the entry type;
- the folded headword and other printed spellings;
- the word class, and where it came from (`class_by`);
- `pointer`.

Verses are cited in the Vulgate's own numbering: `Ps.22.1` is
`vulgate:Ps.22.1`, "Dominus regit me". Its KJV verse (Ps 23:1) and that
verse's uid are on the Vulgate unit (`convert_vulgate`, field `kjv`) and are
not repeated here. **Nothing is minted.**

## 3. How a Whitaker lemma finds its L&S entry

Matching is by spelling and word class, never by meaning. Both sides are
folded alike:

- lower case;
- no macrons;
- j read as i, v read as u;
- hyphens and Perseus's quantity marks (`a^credula`) dropped.

**The L&S headword is the first spelling L&S prints, not the key.** Perseus
keys some compounds by their prefix: `super10` is *super-fio*.

Some entries are excluded:

- An entry printed as an affix (`sum-`, "for sub before m") keeps its hyphen,
  so it never takes a whole word.
- An entry L&S marks spurious (`type="spur"`) never takes a word.
- A **pointer** entry is short, has no class, and is nothing but "v. …"
  (`sum2`: "= eum, v. is"). It loses to a real entry with the same headword.

The tries run in order:

| status | rule | lemmas |
|---|---|---|
| `headword` | exactly one entry prints this headword | 24,608 |
| `class` | several do, and one has the word class WORDS gives. Also: one prints no class while every other prints a class that does not fit (*qui* the pronoun is `qui1`, because `qui2` is the adverb). WORDS's adverb *cum* ("when") may be L&S's conjunction. | 1,046 |
| `case` | ... and exactly one is capitalised as the lemma is (*rex* is `rex1`, not the name `Rex2`) | 305 |
| `gender` | ... and exactly one noun has the lemma's gender (*populus* m. is `populus1`, the people; f. is `populus2`, the poplar) | 59 |
| `spelling` | no headword matches, but one entry prints this as another spelling before its first sense (*rursum* under `rursus`, *quatuor* under `quattuor`, *revertor* under `reverto`) | 873 |
| `voice` | only the verb's other voice is there (WORDS *domino*, L&S `dominor`) | 100 |
| `ambiguous` | several entries remain. All are listed and none is chosen. | 409 |
| `none` | L&S has none of these | 13,427 |

The class L&S prints is its `<pos>` tag, or a gender (meaning a noun). Where it
tags neither, the class is the italic word at the head of the first sense
(`cum2`: *conj.*), and `class_by` says `sense`. That is a hint and is labelled
as one.

Most `none` lemmas are words L&S never had:

- WORDS's medieval and Church Latin (*sabbataria*, *levifico*);
- many biblical names (*Josue*, *Joab*, *Nabuchodonosor*);
- variant spellings L&S does not print (*adtestatio*).

They keep their Whitaker lemma; this build does not invent a key for them.

## 4. The Vulgate's words

Every running word of the Clementine Vulgate is read: 612,029, the
benchmark's own count (README-lemma-spine s.5b). WORDS's two-word guesses are
never taken, as in the lemma spine. Neither are its abbreviations (*Non.*,
*A.*), since the text is cut into words at every full stop and so has none.

The first pass looks at a form alone:

| status | forms | tokens | share of tokens |
|---|---|---|---|
| `sure`: every reading is the same L&S entry | 32,940 | 422,301 | 69.0% |
| `several`: readings point at different entries, or one reading has none | 9,212 | 169,923 | 27.8% |
| `no-ls`: read by WORDS, but no reading is in L&S | 3,933 | 19,303 | 3.2% |
| `unread`: WORDS has no reading | 231 | 502 | 0.1% |

The `no-ls` tokens are nearly all biblical names (*Jerusalem* 828, *Jacob* 328).

## 4b. One word in its verse: the context rules

A `several` word is then looked at in its verse. Each rule only **removes**
readings, and only if at least one is left. A word is resolved when one L&S
entry remains, and it is tagged with every rule that removed something. Any
word still open stays **null**. No rule reads meaning.

| rule id | what it removes | why it holds | tokens it settles (alone or with others) |
|---|---|---|---|
| `idem-dem` | an *idem* reading of a form without *-dem* (*ejus*, *eos*, *eis*) | WORDS's own entry for idem says "w/-dem ONLY" | 11,282 |
| `proper-lower` | a reading that is a name, for a word written lower-case: a capitalised L&S key (*panes* not `Pan`, *principes* not `Princeps2`); where L&S has no entry, a WORDS name | the Clementine capitalises names | 2,731 |
| `rare-inflection` | a reading by an ending WORDS grades less than common (C or rarer in INFLECTS.LAT: *dominum* as domina's genitive plural) | WORDS's own grade on the ending | 3,717 |
| `rare-entry` | a reading whose dictionary entry is two or more of WORDS's frequency grades below the commonest reading, when that one is A or B (*est* as edo, "eats", grade C, against sum, A) | WORDS's own grade on the entry. **This is a frequency prior, not proof**; it is the rule most likely to be wrong in a given verse. | 55,287 |
| `prep-object` | the non-preposition readings, when the next word in the clause can be in the case the preposition takes (*cum eo*, *a facie*) | a preposition needs an object | 5,477 |
| `no-prep-object` | the preposition reading, when the clause ends after it (*a, a, a*) or the next word is lower-case, read, and has no case and no adverb reading (*cum autem*) | there is nothing for it to govern | 2,246 |
| `si-quis` | every reading but the indefinite `quis2`, after *si*, *ne*, *num* | the grammar-book rule: after si, nisi, num, ne, ali- drops away. *nisi* is left out because *nisi qui* is usually relative (Isa 42:19). | 192 |

Two cases look like no-object but are not, so `no-prep-object` stands aside
for them:

- **A capitalised next word** may be a name WORDS misreads. In *a Sidone*,
  WORDS reads *Sidone* as the verb sido.
- **An adverb** can be a preposition's object in the Vulgate. *a longe* means
  "from afar".

The result over all 612,029 words, in `manifest.counts`:

| outcome | tokens | share |
|---|---|---|
| sure (the form alone decides) | 422,300 | 69.0% |
| resolved by a rule, tagged | 76,264 | 12.5% |
| **unresolved, null** | 93,660 | **15.3%** (from 27.8%) |
| no L&S entry / unread | 19,805 | 3.2% |

What stays null is real ambiguity that no rule here can see:

- *qui*, *quae*, *quod*: relative, interrogative or indefinite;
- *sanctus*: the adjective, or the participle of `sancio`;
- *mea*: meus, or meo "go!", which WORDS grades only one step apart.

`vulgate-concordance.jsonl` gives each key three lists:

- `sure`;
- `resolved`, as `{rule ids: [verses]}`;
- `possible`, for a null reading.

`vulgate-forms.jsonl` gives each `several` form its `resolved` counts by rule
and its `unresolved` count.

Every word, with its key and rule ids, goes to `build/latin-key/vulgate-tokens.jsonl`.
That file is gitignored and the build rebuilds it in about 30 seconds, so a
rule's work can be checked verse by verse.

## 4c. Strong's number to the Vulgate's Latin: `strongs-latin.jsonl`

This bridges the two keys. For each Strong's number, it lists the L&S entries
that stand in the Vulgate where that number stands in the KJV, scored by verse
co-occurrence.

How the pairs are made:

- Each Vulgate verse is paired with the KJV verse(s) its map names (31,057
  pairs; the books outside the KJV's canon have none).
- The KJV side brings its Strong's tags (`data/strongs/kjv-tags.jsonl`). The
  Vulgate side brings the L&S keys of its sure and resolved words. Null words
  bring nothing.
- The score is Dice: 2 × verses together / (verses with the number + verses
  with the word).

A word is kept for a number only if all of these hold:

- it is seen with the number in 3 or more verses;
- it scores 0.10 or more;
- it scores at least 40% of the number's best word;
- the number is among the word's own top 3 numbers in that language.

The last test removes words that merely travel with a number. *Christus*
follows θεός (G2316) but is G5547's word.

| Strong's | Vulgate |
|---|---|
| G26 ἀγάπη | `caritas` 56 verses, `dilectio` 22 |
| H2617 חֶסֶד | `misericordia` 214 |
| G3056 λόγος | `verbum` 198, `sermo` 103 |
| G3870 παρακαλέω | `rogo`, `exhortor`, `obsecro`, `deprecor` |

4,057 of the 14,047 numbers the KJV tags get at least one word. 1,310 of them
are marked `evidence: "thin"`, because the number stands in fewer than 10 KJV
verses. With so few verses, one passage's other words can score as high as the
right one: H4, Aramaic "fruit", comes out as `ramus` and `subter`.

**This is statistical evidence that two words translate each other. It is
not a reading of any verse.** It also inherits the lemma layer's errors, and
it shows where they are. H3444 יְשׁוּעָה pairs with `saluto` because the
Vulgate's noun *salutare* ("thy salvation") is read as the verb's infinitive.

## 5. Rights

| source | work | this edition | committed here |
|---|---|---|---|
| Lewis & Short | PD (1879) | Perseus's TEI, **CC BY-SA 4.0**, pinned at PerseusDL/lexica `56061ca`, sha256 in the manifest | Keys, entry ids, homograph numbers, entry types, printed spellings, word class. No definitions. |
| Whitaker's WORDS | copyright, with a free grant | `free-grant` (README-lemma-spine s.1) | Lemma keys (dictionary forms) |
| Clementine Vulgate | PD | BibleGet-I-O mirror, pinned | Forms and counts, verse ids. No running text. |

The rule from ADR 0001 for CC BY-SA material is the one applied to the AGLDT
treebank: point at it, never merge it in. The L&S file stays in the gitignored
`data/corpus/lewis-short/`. What is committed is the index of entry keys and
the facts printed in each entry's opening line, with Perseus's attribution
carried verbatim in `manifest.sources.lewis-short.rights` (`redistribute_whole:
false`). **Whether that index may be committed is Adam's call.** The answer
there decides whether these files stay.

## 6. Not claimed

- A link is a match of spelling and class, not a reading of the entry.
- A context rule chooses only by grammar or by WORDS's frequency grades. `possible` keeps every reading WORDS allows for a word no rule settled.
- No uid is proposed or minted for a Latin word. That would follow the Strong's
  pattern (`proposed-uids.jsonl`, `--adopt`) only on Adam's ruling.
- Only the Vulgate is linked so far. The hymns already carry Whitaker lemma
  keys (`data/hymns/tokens.jsonl`), so `whitaker-ls.jsonl` reaches their words
  too.
