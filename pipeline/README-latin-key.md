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
python3 pipeline/build_latin_key.py             # build build/latin-key/ + the manifest
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

## 2. The files (`build/latin-key/`, gitignored, about 49 MB)

**Only `data/lemmas/latin-key/manifest.json` is committed.** Every other file
is drawn from Perseus's CC BY-SA text of L&S, so it is built locally to
`build/latin-key/`, and the manifest records each file's sha256 and row count
(`files`) beside the rights block (s.5). A rebuild proves itself against those
hashes (`--check`). Until Adam rules on s.5 nothing derived from L&S goes into
this public repository; on 2026-10-02 the files were also removed from the
branch's history.

| file | one row per | what it holds |
|---|---|---|
| `lewis-short.jsonl` | L&S entry (51,645) | See below. No definition text. |
| `whitaker-ls.jsonl` | Whitaker lemma (40,827) | The L&S key(s) it links to, and the `status` saying how. |
| `vulgate-forms.jsonl` | Vulgate form as written, lower-cased (46,316) | Token count, Whitaker lemmas, L&S keys, `status`. |
| `strongs-latin.jsonl` | Strong's number with a Latin equivalent (3,950) | The L&S entries the Vulgate uses where the KJV has that number, scored (s.4c). |
| `vulgate-concordance.jsonl` | L&S key the Vulgate uses (9,364) | `sure` verses (the form alone decides), `resolved` verses by rule id (s.4b), and `possible` verses (left null). |
| `manifest.json` (committed) | — | Pins, rights, counts, each file's sha256, what is not claimed. |

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
| `headword` | exactly one entry prints this headword | 24,581 |
| `class` | several do, and one has the word class WORDS gives. Also: one prints no class while every other prints a class that does not fit (*qui* the pronoun is `qui1`, because `qui2` is the adverb). WORDS's adverb *cum* ("when") may be L&S's conjunction. | 1,045 |
| `case` | ... and exactly one is capitalised as the lemma is (*rex* is `rex1`, not the name `Rex2`) | 305 |
| `gender` | ... and exactly one noun has the lemma's gender (*populus* m. is `populus1`, the people; f. is `populus2`, the poplar) | 59 |
| `spelling` | no headword matches, but one entry prints this as another spelling before its first sense (*rursum* under `rursus`, *quatuor* under `quattuor`, *revertor* under `reverto`) | 878 |
| `voice` | only the verb's other voice is there (WORDS *domino*, L&S `dominor`) | 90 |
| `ambiguous` | several entries remain. All are listed and none is chosen. | 410 |
| `clash` | the only entry is a noun where WORDS has a verb (or the reverse), or an adverb where WORDS has a pronoun (*eadem*, *eodem*). Those are never one entry, so it is another word, left unlinked: WORDS's *vis* "you want" (from volo) is not L&S's `vis` "force"; *canto, cantonis* is not `canto` "to sing"; WORDS's *audito* is not L&S's noun `auditor`. | 32 |
| `none` | L&S has none of these | 13,427 |

The class L&S prints is its `<pos>` tag, or a gender (meaning a noun). A
verb class wins over a gender found further on (*comitio*, "v. n. and a.").
**Perseus tags L&S's "v. n."** (verbum neutrum, an intransitive verb) **as a
gender**, `<gen>n.</gen>`, so *miror*, *vereor* and *abstineo* would read as
neuter nouns. The n. is taken as the verb's when the entry prints a verb
class, a conjugation number in its inflection (*miror* "ātus, 1"), or "v. a.
and" just before it. That moved 41 entries, all verbs, from noun to verb. Where it
tags neither, the class is the italic word at the head of the first sense
(`cum2`: *conj.*), and `class_by` says `sense`. That is a hint and is labelled
as one.

Most `none` lemmas are words L&S never had:

- WORDS's medieval and Church Latin (*sabbataria*, *levifico*);
- many biblical names (*Josue*, *Joab*, *Nabuchodonosor*);
- variant spellings L&S does not print (*adtestatio*).

They keep their Whitaker lemma; this build does not invent a key for them.

**Numbers.** WORDS keeps a number's four words in one entry ("septem, septimus
-a -um, septeni -ae -a, septie(n)s") and tells them apart in each reading
(CARD, ORD, DIST, ADVERB). L&S gives each its own entry, so an ordinal,
distributive or number-adverb reading is linked by its own word: *septimo* is
`septimus`, *tertio* `tertius`, never `septem` or `tres`.

## 4. The Vulgate's words

Every running word of the Clementine Vulgate is read: 612,029, the
benchmark's own count (README-lemma-spine s.5b). WORDS's two-word guesses are
never taken, as in the lemma spine. Neither are its abbreviations (*Non.*,
*A.*), since the text is cut into words at every full stop and so has none.

The first pass looks at a form alone:

| status | forms | tokens | share of tokens |
|---|---|---|---|
| `sure`: every reading is the same L&S entry | 32,954 | 422,340 | 69.0% |
| `several`: readings point at different entries, or one reading has none | 9,195 | 169,880 | 27.8% |
| `no-ls`: read by WORDS, but no reading is in L&S | 3,936 | 19,307 | 3.2% |
| `unread`: WORDS has no reading | 231 | 502 | 0.1% |

The `no-ls` tokens are nearly all biblical names (*Jerusalem* 828, *Jacob* 328).

## 4b. One word in its verse: the context rules

A `several` word is then looked at in its verse. Each rule only **removes**
readings, and only if at least one is left. A word is resolved when one L&S
entry remains, and it is tagged with every rule that removed something. Any
word still open stays **null**. No rule reads meaning.

**Two kinds of rule.** Most read the grammar of the verse. Three are
**priors**: `rare-entry` and `rare-inflection` use WORDS's own frequency
grades, and `whole-word` follows the dictionary's convention. A prior says
which reading is usual, not which one this verse has, so the manifest counts
words settled by priors alone apart from words a grammar rule helped settle
(`vulgate_tokens_resolved_by_kind`).

| rule id | what it removes | why it holds | tokens it settles (alone or with others) |
|---|---|---|---|
| `idem-dem` | an *idem* reading of a form without *-dem* (*ejus*, *eos*, *eis*) | WORDS's own entry for idem says "w/-dem ONLY" | 8,957 |
| `proper-lower` | a reading that is a name, for a word written lower-case: a capitalised L&S key (*panes* not `Pan`, *principes* not `Princeps2`); where L&S has no entry, a WORDS name | the Clementine capitalises names | 2,190 |
| `possessive-agrees` | beside a word that can only be a possessive (*meus*, *tuus*, *suus*, *noster*, *vester*), every reading that is not a noun, adjective, pronoun or numeral agreeing with it in case, number and gender. It runs before `rare-entry`, which would otherwise take *salutare tuum*, "thy salvation", as the verb saluto, because WORDS grades the noun by classical use. | a possessive needs something to agree with | 2,289 |
| `whole-word` (prior) | a reading that splits off an enclitic (-que, -ne, -ve), when another reads the word whole: *absque* is the preposition "without", not *abs* + -que | the dictionary prints the whole word | 3,058 |
| `rare-inflection` (prior) | a reading by an ending WORDS grades less than common (C or rarer in INFLECTS.LAT: *dominum* as domina's genitive plural) | WORDS's own grade on the ending | 3,015 |
| `rare-entry` (prior) | a reading whose dictionary entry is two or more of WORDS's frequency grades below the commonest reading, when that one is A or B (*est* as edo, "eats", grade C, against sum, A). **Only between readings of one word class.** A noun never loses to a verb or participle by frequency: before 2026-10-02 it did, and every *peccata* went to `pecco`, every *tribus* to `tres`, *praeceptum* to `praecipio`. | WORDS's own grade on the entry. **This is a frequency prior, not proof**; it is the rule most likely to be wrong in a given verse. | 21,928 |
| `prep-object` | the non-preposition readings, when the next word in the clause can be in the case the preposition takes (*cum eo*, *a facie*) | a preposition needs an object | 6,870 |
| `no-prep-object` | the preposition reading, when the clause ends after it (*a, a, a*) or the next word is lower-case, read, and has no case and no adverb reading (*cum autem*) | there is nothing for it to govern | 1,822 |
| `si-quis` | every reading but the indefinite `quis2`, after *si*, *ne*, *num* | the grammar-book rule: after si, nisi, num, ne, ali- drops away. *nisi* is left out because *nisi qui* is usually relative (Isa 42:19). | 192 |

Two cases look like no-object but are not, so `no-prep-object` stands aside
for them:

- **A capitalised next word** may be a name WORDS misreads. In *a Sidone*,
  WORDS reads *Sidone* as the verb sido.
- **An adverb** can be a preposition's object in the Vulgate. *a longe* means
  "from afar".

`no-prep-object` also fires when the next word is a particle that stands
second in its clause (*vero*, *autem*, *enim*, *itaque*, *igitur*, *quoque*,
*quidem*): *cum vero* is "but when", since no such particle comes between a
preposition and its object.

`prep-object` stands aside once too: a name with no case followed by a verb
(*Quod cum David rescisset*, 1 Sam 23:9) may be the subject of a cum-clause,
so *cum* stays null there.

The result over all 612,029 words, in `manifest.counts`:

| outcome | tokens | share |
|---|---|---|
| sure (the form alone decides) | 422,339 | 69.0% |
| resolved, a grammar rule taking part | 21,843 | 3.6% |
| resolved by priors alone | 27,679 | 4.5% |
| **unresolved, null** | 120,359 | **19.7%** (from 27.8%) |
| no L&S entry / unread | 19,809 | 3.2% |

What stays null is real ambiguity that no rule here can see:

- *qui*, *quae*, *quod*: relative, interrogative or indefinite;
- *sanctus*: the adjective, or the participle of `sancio`;
- *mea*: meus, or meo "go!", which WORDS grades only one step apart;
- *peccata*, *principio*, *tribus*: a noun, or a verb or number of the same
  spelling. Only the verse's sense tells them apart.

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
- The KJV side brings its Strong's tags (`build/strongs/kjv-tags.jsonl`, also
  local, README-strongs). Without them the build keeps the committed manifest's
  counts for this file and does not rebuild it. The
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

3,950 of the 14,047 numbers the KJV tags get at least one word. 1,258 of them
are marked `evidence: "thin"`, because the number stands in fewer than 10 KJV
verses. With so few verses, one passage's other words can score as high as the
right one: H4, Aramaic "fruit", comes out as `ramus` and `subter`.

**This is statistical evidence that two words translate each other. It is
not a reading of any verse.** It also inherits the lemma layer's errors, and
it shows where they are. H3444 יְשׁוּעָה paired with `saluto` because the
Vulgate's noun *salutare* ("thy salvation") was read as the verb's infinitive;
`possessive-agrees` (s.4b) was written for it. H2403 and G266 ("sin") paired
with `pecco` until `rare-entry` was kept to one word class; they now give
`peccatum` first.

**Rights.** This file is built from the KJV's Strong's tags as well as from
L&S, so it waits on both rulings (README-strongs s.6 and s.5 below).

## 5. Rights

| source | work | this edition | in the built files (none committed) |
|---|---|---|---|
| Lewis & Short | PD (1879) | Perseus's TEI, **CC BY-SA 4.0**, pinned at PerseusDL/lexica `56061ca`, sha256 in the manifest | Keys, entry ids, homograph numbers, entry types, printed spellings, word class. No definitions. |
| Whitaker's WORDS | copyright, with a free grant | `free-grant` (README-lemma-spine s.1) | Lemma keys (dictionary forms) |
| Clementine Vulgate | PD | BibleGet-I-O mirror, pinned | Forms and counts, verse ids. No running text. |

The rule from ADR 0001 for CC BY-SA material is the one applied to the AGLDT
treebank: point at it, never merge it in. The L&S file stays in the gitignored
`data/corpus/lewis-short/`. The built files (the index of entry keys and the
facts printed in each entry's opening line, and everything linked through it)
stay in the gitignored `build/latin-key/`. Only the manifest is committed,
with Perseus's attribution carried verbatim in
`manifest.sources.lewis-short.rights` (`redistribute_whole: false`).
**Whether that index may be committed is Adam's call.** Until he rules, the
test fails if git tracks anything under `data/lemmas/latin-key/` but the
manifest.

## 6. Not claimed

- A link is a match of spelling and class, not a reading of the entry.
- A context rule chooses only by grammar or by WORDS's frequency grades. `possible` keeps every reading WORDS allows for a word no rule settled.
- No uid is proposed or minted for a Latin word. That would follow the Strong's
  pattern (`proposed-uids.jsonl`, `--adopt`) only on Adam's ruling.
- Only the Vulgate is linked so far. The hymns already carry Whitaker lemma
  keys (`data/hymns/tokens.jsonl`), so `whitaker-ls.jsonl` reaches their words
  too.
