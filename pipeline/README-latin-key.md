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
| `vulgate-concordance.jsonl` | L&S key the Vulgate uses (9,617) | `sure` verses (the form can only be this word) and `possible` verses (one reading of several). |
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
| `class` | several do, and one has the word class WORDS gives. Also: one prints no class while every other prints a class that does not fit (*qui* the pronoun is `qui1`, because `qui2` is the adverb). | 1,045 |
| `spelling` | no headword matches, but one entry prints this as another spelling before its first sense (*rursum* under `rursus`, *quatuor* under `quattuor`, *revertor* under `reverto`) | 872 |
| `voice` | only the verb's other voice is there (WORDS *domino*, L&S `dominor`) | 99 |
| `ambiguous` | several entries remain. All are listed and none is chosen. | 776 |
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

| status | forms | tokens | share of tokens |
|---|---|---|---|
| `sure`: every reading is the same L&S entry | 32,631 | 416,090 | 68.0% |
| `several`: readings point at different entries, or one reading has none | 9,521 | 176,134 | 28.8% |
| `no-ls`: read by WORDS, but no reading is in L&S | 3,933 | 19,303 | 3.2% |
| `unread`: WORDS has no reading | 231 | 502 | 0.1% |

`several` is real Latin ambiguity, and the build does not settle it.
Examples:

- *est* is `sum1` or `edo2` (he eats);
- *ejus* is `is` or `idem`;
- *sanctus* is the adjective or the participle of `sancio`.

Choosing needs the sentence, and is for a later tagger or for Adam's review
layer. Until then the concordance lists such verses under `possible`, never
under `sure`. The `no-ls` tokens are nearly all biblical names (*Jerusalem*
828, *Jacob* 328).

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
- `possible` is every reading WORDS allows. The build chooses none.
- No uid is proposed or minted for a Latin word. That would follow the Strong's
  pattern (`proposed-uids.jsonl`, `--adopt`) only on Adam's ruling.
- Only the Vulgate is linked so far. The hymns already carry Whitaker lemma
  keys (`data/hymns/tokens.jsonl`), so `whitaker-ls.jsonl` reaches their words
  too.
