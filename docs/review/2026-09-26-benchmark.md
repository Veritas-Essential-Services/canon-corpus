---
model_log:
  - 2026-09-26 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
  - 2026-09-26 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
fable_review: pending
---
# The WORDS port against the Clementine Vulgate (2026-09-26)

*How much of a real ecclesiastical Latin text the lemma spine's analyzer
(`pipeline/whitaker.py`, `pipeline/whitaker_tricks.py`) can read, and by what
rule. Produced by `pipeline/benchmark_whitaker.py`. Numbers and single forms
only; no running text is quoted.*

```
python pipeline/build_lemma_spine.py --fetch     # the Whitaker files and pinned Ada
python pipeline/proper_names.py --fetch          # Hitchcock's Bible Names (states F, G)
python pipeline/benchmark_whitaker.py --fetch    # the text, then the measurement
```

## Source

| | |
|---|---|
| text | the Clementine Vulgate, 73 books, one verse per line |
| from | the Clementine Vulgate Project's source files, mirrored at github.com/BibleGet-I-O/Clementine-Vulgate, commit `d57e2cde0cceda0d073ea9efc1fee616bcfeb2c1`, `src/iso-encoded/*.lat` (codepage 1252) |
| sha256 | `8002776ae05d72fcec447dac1b890728423096ffd22970771cbb419b0536b990`, taken over the sorted list of (file name, file sha256). A changed, added or missing book is a hard stop. |
| licence | **public domain**. The project's own words: "The text has been released into the public domain." It asks, without a licence, for acknowledgment, for error reports, and that changes be made clear. Evidence: vulsearch.sourceforge.net as archived by the Wayback Machine on 2022-11-21 (`web.archive.org/web/20221121145231/https://vulsearch.sourceforge.net/index.html`, sha256 `3fb9ee61…a368`). |
| kept at | `data/corpus/benchmark/` (gitignored). Only the script and this summary are committed. |
| modified | nothing on disk. In memory the script drops the verse numbers and the markup (`\` `[` `]` `/` and `<speaker>` labels), splits on non-letters, lower-cases, strips diacritics (ë) and opens the ligatures æ and œ. |

The mirror's `src/utf8` copies were converted as if they were Latin-1, so every
œ in them is a C1 control character. The benchmark reads the codepage-1252
originals instead.

**Size: 612,029 running words, 46,316 distinct forms.**

## Seven states of the port, all from today

| state | what it adds |
|---|---|
| **A** | stem + ending, uniques, enclitics: the port as it was this morning |
| **B** | + SYNCOPE, SLURY, FIXES, TRICKS: the port by noon |
| **C** | + Roman numerals and the non-enclitic TACKONs (task 1) |
| **D** | + what this benchmark sent back to the Ada for (task 3): stem keys as `makedict_main.adb` writes them, and the PACKONs and TICKONs of Word's Qu block |
| **E** | + WORDS's capitalisation rule (`parse.adb`, Is_Capitalized): no TRICKS on a word written capitalised (afternoon) |
| **F** | + the house proper-names table, consulted for a capitalised form (`pipeline/proper_names.py`) |
| **G** | + the house supplement (`data/lemmas/house-supplement.jsonl`) |

A, B and C key stems by slot, as the port did before D. The fix that folds
the enclitic *-ve* is in all of them, because it cannot be switched off.
From E on, a form is read as it is written each time: a form written both
capitalised and not is analysed both ways, and each token counts under its
own spelling. The "forms" columns take the spelling a form is written in
most (lower-case on a tie).

## Coverage

*"Read"* means at least one analysis that is not WORDS's two-words guess.
*"Guess only"* means nothing but that guess, which WORDS itself labels "If not
obvious, probably incorrect" and which the lemma spine never takes.

| | unknown forms | unknown tokens | guess only (forms / tokens) | read forms | read tokens |
|---|---|---|---|---|---|
| A | 5,142 (11.10%) | 24,340 (3.98%) | 0 / 0 | 41,174 (88.90%) | 587,689 (96.02%) |
| B | 3,152 (6.81%) | 16,157 (2.64%) | 367 / 2,589 | 42,797 (92.40%) | 593,283 (96.94%) |
| C | 3,136 (6.77%) | 16,025 (2.62%) | 360 / 2,205 | 42,820 (92.45%) | 593,799 (97.02%) |
| **D** | **3,120 (6.74%)** | **15,910 (2.60%)** | 324 / 1,569 | **42,872 (92.56%)** | **594,550 (97.14%)** |
| E | 3,569 (7.71%) | 17,990 (2.94%) | 74 / 309 | 42,673 (92.13%) | 593,730 (97.01%) |
| F | 188 (0.41%) | 353 (0.06%) | 74 / 309 | 46,054 (99.43%) | 611,367 (99.89%) |
| **G** | **162 (0.35%)** | **196 (0.03%)** | 67 / 276 | **46,087 (99.51%)** | **611,557 (99.92%)** |

E to G are explained below, under "After".

From A to D, 1,698 forms go from unknown to read (1,679 by a rule, 19 plainly,
the latter all from the stem-key fix). 324 go from unknown to guess only. **No
form that A read plainly lost its plain reading.**

**Unknown or guess only in D: 3,444 forms, 17,479 tokens (2.86%).** 3,334 of
those forms (16,986 tokens) are never written lower-case in the text. That
means they are proper names, which WORDS mostly lacks. Only **110 forms (493
tokens, 0.08% of the text)** are ever written lower-case.

## One candidate or several

A candidate is a distinct dictionary form (lemma). Two-words guesses are left
out.

| | read forms: one / several | share one | read tokens: one / several | share one |
|---|---|---|---|---|
| A | 30,393 / 10,781 | 73.82% | 354,857 / 232,832 | 60.38% |
| B | 31,631 / 11,166 | 73.91% | 358,751 / 234,532 | 60.47% |
| C | 31,653 / 11,167 | 73.92% | 359,254 / 234,545 | 60.50% |
| D | 31,630 / 11,242 | 73.78% | 358,983 / 235,567 | 60.38% |
| E | 31,488 / 11,185 | 73.79% | 358,402 / 235,328 | 60.36% |
| F | 34,929 / 11,125 | 75.84% | 376,309 / 235,058 | 61.55% |
| G | 34,961 / 11,126 | 75.86% | 376,495 / 235,062 | 61.56% |

About three forms in four have one lemma, but only three running words in five.
The commonest words are the ambiguous ones (*qui* and *quod* have four lemmas each; *in* and *est* have two). D adds
candidates to a few forms that already had one, because WORDS reads *quoque*
and *quemque* as PACKON pronouns too.

## Needing a rule

These are forms read only by a rule, with no plain reading. They are counted
by the first rule in `via`. A form whose analyses reach it by different rules
counts under each, so the kinds can add up to more than the total.

| | forms needing a rule | tokens |
|---|---|---|
| B | 1,623 (3.50%) | 5,594 (0.91%) |
| C | 1,646 (3.55%) | 6,110 (1.00%) |
| D | 1,679 (3.63%) | 6,753 (1.10%) |
| E | 1,480 (3.20%) | 5,933 (0.97%) |
| F, G | 1,280 (2.76%) | 5,056 (0.83%) |

By kind (forms / tokens):

| kind | B | C | D | E | F, G |
|---|---|---|---|---|---|
| SYNCOPE | 641 / 2,437 | 641 / 2,437 | 641 / 2,437 | 641 / 2,437 | 640 / 2,435 |
| PREFIX | 282 / 895 | 281 / 894 | 280 / 892 | 280 / 892 | 204 / 456 |
| SUFFIX | 418 / 783 | 418 / 783 | 415 / 774 | 415 / 774 | 292 / 335 |
| TRICK | 286 / 1,488 | 284 / 1,279 | 283 / 1,093 | 84 / 273 | 84 / 273 |
| SLURY | 20 / 49 | 20 / 49 | 20 / 49 | 20 / 49 | 15 / 33 |
| TACKON | – | 26 / 726 | 25 / 725 | 25 / 725 | 25 / 725 |
| PACKON | – | – | 38 / 839 | 38 / 839 | 38 / 839 |
| TICKON | – | – | 1 / 2 | 1 / 2 | 1 / 2 |
| ROMAN | – | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |

TRICK falls from B to D because forms that a trick used to reach, often
wrongly, are now read by a TACKON or PACKON. The Vulgate has no Roman numerals
as such. Four forms (*mi*, *dii*, *vi*, *ii*; 248 tokens) get a numeral
reading beside their real ones, as they do in WORDS.

The rules that matter most in D, by tokens:

| rule (`via`) | forms | tokens |
|---|---|---|
| SYNCOPE `s => vis` (*audisset*, *nosti*) | 433 | 1,128 |
| SYNCOPE `ier => iver` (*audierunt*, *abierunt*) | 155 | 863 |
| TACKON `-cum` (*tecum*, *mecum*, *vobiscum*, *nobiscum*) | 6 | 563 |
| SYNCOPE `ii => ivi` | 43 | 430 |
| TRICK Any_Tricks `internal h/` | 99 | 366 |
| PACKON `-dam` (*quidam*) | 13 | 317 |
| PACKON `-cumque` (*quicumque*); `-cum` finds the same 9 forms, through the prefix quirk the Ada has | 9 | 285 |
| PACKON `-quam` (*quisquam*) | 5 | 184 |
| PREFIX `as-` (*assumo*) | 37 | 184 |
| TRICK Any_Tricks `internal ae/e` | 34 | 152 |
| PREFIX `am-` | 18 | 134 |
| TRICK Mediaeval `internal s/ns` (*vigesimo* read as *vigensimo*; *Aser*) | 7 | 114 |
| TACKON `-modi` (*hujusmodi*, *hujuscemodi*) | 2 | 81 |

**A caution the numbers make plain.** Of the 1,679 rule-read forms, 435 (1,731
tokens) are never written lower-case, so they are names. Nearly all of those
readings are wrong:

- *Amalec* and *Amnon* are read as *am-* + a word;
- *Absalom* is read as *abs-* + a word;
- *Libanus* is read with the suffix *-an*;
- *Emath* and *Hiram* are read by dropping an *h*;
- *Aser* is read by *s/ns*.

WORDS guards against this by trying no tricks on a capitalised word it takes
for a name (Ignore_Unknown_Names). The port does not, because search keys are
lower-case; this is a departure recorded in `whitaker_tricks.py`. The lemma
spine is safe: it takes a rule's lemma only when the draft's headword agrees.
A concordance over raw text would not be safe. The next step is to carry
capitalisation into the analyzer. *(Done the same afternoon: states E to G,
below. In G, 36 never-lower-case forms, 43 tokens, are still read only by a
rule.)*

## The 30 commonest unknowns (state D)

All 30 are proper names, never written lower-case. "(guess)" marks a
two-words guess only.

| form | count | form | count | form | count |
|---|---|---|---|---|---|
| aaron | 322 | galaad | 130 | esau | 83 |
| joseph | 186 | jordanem | 128 | simon | 81 |
| josue (guess) | 183 | jonathas | 122 | ruben | 74 |
| abraham | 182 | isaac | 115 | gad | 72 |
| ephraim | 180 | nabuchodonosor | 110 | ezechias | 72 |
| sion | 180 | samuel | 109 | hebron | 70 |
| benjamin | 163 | ammon | 105 | dan | 69 |
| moab | 154 | jeroboam | 99 | jeremiam | 68 |
| philisthiim | 147 | achab | 87 | bethel | 67 |
| joab | 142 | josaphat | 85 | jericho | 67 |

## What the unknowns pointed to

### Ported, because WORDS has it (task 3)

The lower-case unknowns in state C pointed to three things WORDS does that the
port did not. Together they read **52 more forms, 751 tokens**.

1. **PACKONs** (`Process_Packons`): *quidquam* 109, *quaecumque* 102,
   *quicumque* 99, *quisquam* 38, *quaedam* 35, *quemquam* 25, *quispiam* 22,
   *quosdam* 21, *quemdam* 20, and the rest of the *quidam*, *quicumque*,
   *quisquam*, *quilibet* and *quinam* families.
2. **TICKONs**: *siqua* 2 (*si* + *qua*).
3. **Stem keys** (`makedict_main.adb`): *pessimum* 14, *pessimis* 13, *summus*
   12, *interiora* 12, *proximam* 2 and other forms of one-stem comparatives
   and superlatives. With them came the adverb's own comparison table
   (*pejus* COMP, *pessime* SUPER), which was a wrong parse rather than an
   unknown.

### WORDS's own limits: WORDS would not read these either

- **Syncope inside an enclitic**: *sepelieruntque* 8, *abieruntque* 6,
  *servieruntque* 6, *abiitque* 3, *dormieritque*, *quaesieritque*,
  *audissetque*, *exieruntque*. WORDS's Enclitic runs syncope on the whole
  form, not on the form less *-que*.
- **Words written together** (a two-words guess at best):
  - *teipsum* 27, *meipsum* 13, *vosmetipsos* 15, *temetipsum* 12, *meipso*
    12, *nosmetipsos* 9, *vobismetipsis* 8 and similar;
  - *unumquemque* 17, *unumquodque* 8, *unaquaeque* 4, *unamquamque* 3,
    *unoquoque* 3;
  - compound ordinals: *tertiadecima* 9, *tertiodecimo* 6, *quintodecimo* 6,
    *quartodecimo* 5, *septimodecimo*, *nonusdecimus*, *decimoquinto*;
  - *sartatecta* 7, *paulominus* 3, *plusquam*, *nudiusquarta*,
    *reipublicae*.
- **Spellings that no WORDS trick reaches**, of words WORDS has:
  - *m* for *n* before *-dem*: *eamdem* 16, *eumdem* 13, *eorumdem*,
    *earumdem*, *eamdemque*, *tantumdem*;
  - a doubled consonant for a single one (WORDS only tries single for
    double): *squallentes* 2, *redditibus* 3, *braccis*;
  - an internal *y* for *i*: *tyrones* 2;
  - *ti* for *ci* (the medieval table has only *ci* for *ti*): *natalitius*,
    *nutritios*;
  - two changes at once: *rhedarum*.
- **Comparison WORDS does not generate**: *necessariora*; and *nequissima* 6,
  *nequius* 5, *nequissimi* 3, *nequissimis* 2, *nequissimum*, because WORDS
  files *nequior* and *nequissimus* as undeclined.

### Missing from WORDS's vocabulary (listed, not fixed)

These forms, spellings or inflections are not in DICTLINE at the pinned
commit. A later session could supply them from a house supplement:

- *pharisaeus* (*pharisaei* 55, *-orum* 17, *-is* 13, *-us* 9, *-os* 6)
- *sadducaeus* (*-orum* 7, *-i* 5, *-is*, *-os*)
- *setim* 30, *theraphim* 4
- *basis*, accusative in *-im* and *-em* (*basim* 10, *basem*)
- *prophetis*, *-idis* (*prophetidem* 2)
- *emptitius* (*emptitius* 2, *emptitii*)
- *sardonycho*, *mygale*, *psaltem*, *myro*, *smigmata*, *bahem*,
  *querulosi*, *nerviceis*, *onustati*
- *pyrorum* 4
- *quaesumus* 2 (*quaeso*, which WORDS lists without this form)
- *ruituri* (future participle of *ruo*), *sancitum* (supine of *sancio* in
  *-itum*), *circumlinisti*, *plexueris*, *fasciaretur*
- the place names written lower-case: *carmel* 6, *horon* 2, *ixion*
- *ejicicetur*: this looks like a misprint in the source. It may be worth
  reporting to the Clementine project, as it asks.

The proper names, about 3,300 forms and 17,000 tokens, are the largest gap by
far. WORDS was never meant to hold them. A names table (biblical names,
indeclinable or Latinised, from a PD onomasticon) is its own piece of work.

## After: capitalisation, proper names, house supplement (states E to G)

*Added the same afternoon. The first two items below are what the benchmark
asked for above; the third fills the vocabulary gaps it listed.*

### Before and after

| | unknown forms | unknown tokens | guess only (forms / tokens) | read tokens | never lower-case, read only by a rule (forms / tokens) |
|---|---|---|---|---|---|
| **before (D)** | 3,120 (6.74%) | 15,910 (2.60%) | 324 / 1,569 | 97.14% | 435 / 1,731 |
| **after (G)** | **162 (0.35%)** | **196 (0.03%)** | 67 / 276 | **99.92%** | **36 / 43** |

What WORDS and the house cannot read in G, unknown or guess only, is 229 forms
and 472 tokens: **0.08% of the text**. No form that A read plainly lost its
plain reading, and the supplement adds no reading to any form a Whitaker entry
already reads (the benchmark checks both).

### E: WORDS's capitalisation rule

Ported from `parse.adb`. Parse_Latin_Word skips Try_Tricks, and TRICKS on the
form less an enclitic, when Ignore_Unknown_Names is on (its default, Y, in
`word_parameters.adb`) and the word is Capitalized: first letter A-Z, second
a-z. (The option's help text says "longer than three letters"; the code tests
only that the word has two letters, and the code is ported.) The analyzer reads
the test from the form as written; with only a search key, as the hymn build
calls it, nothing is capitalised and nothing changes.

**One correction to what was asked.** WORDS skips *only* the TRICKS on a
capitalised word. SLURY, SYNCOPE and the prefixes and suffixes (FIXES) all run
inside Pass, before the test, so WORDS itself reads *Absalom* as *abs-* + a
word and *Libanus* with the suffix *-an*. The port does exactly that and no
more. Those readings are replaced in F, because a name found in the names
table stops the FIXES the way a name in DICTLINE would.

From D to E, 199 forms (811 tokens) lose their only reading, a trick, and 250
forms (1,247 tokens) lose their two-words guess. Never-lower-case forms read
only by a rule fall from 435 to 236: every TRICK is gone, and PREFIX 83,
SUFFIX 156, SYNCOPE 14, SLURY 5 and TACKON 1 remain. The cost to ordinary
words is small: after G, 14 forms that the text also writes lower-case lose a
reading when they open a sentence (18 tokens), and only 9 of those tokens had a
real reading rather than a guess (*Vigesima* 5, *Vigesimum*, *Foenerabis*,
*Foeneratur*, *Gazophylacia*). That is WORDS's behaviour too.

### F: the proper-names table

`data/lemmas/proper-names/names.jsonl`, built by `pipeline/proper_names.py`,
method in its docstring, figures in its manifest. It is derived mechanically:

1. **Candidates**: forms never written lower-case, capitalised at least once
   in mid-sentence (not at a verse start or after `. : ? !`, where any word is
   capitalised), and with no plain WORDS reading in D. **3,574 forms, 18,507
   tokens** (2,956 unknown in D, 233 guess only, 385 read only by a rule). Five
   more are a candidate plus *-que* and are left to the lookup, which takes the
   enclitic off. **Held back**: 190 forms (205 tokens) that are never
   lower-case but capitalised only at a sentence start. Most are names met once
   (*Balaan*, *Corneli*, *Dositheus*), but some are ordinary words there
   (*assumensque*, *arastis*, *thymiateria*), so the rule does not take them.
   They are listed in the manifest for Adam.
2. **Lemmas from the Vulgate's own forms.** A candidate with a Latin
   nominative ending heads the attested forms of its stem: *Jonathas* heads
   *Jonathae*, *Jonatha*; *Samuel* heads *Samuelem*, *Samuelis*, *Samuele*,
   *Samueli*. No nominative the text does not write is ever supplied.
   **3,004 lemmas**: 2,686 of one form (*Aaron*, 322 tokens), 318 with a
   paradigm (6,019 tokens). By class: 1st declension *-a* 81, *-as* 79; 2nd
   *-us* 56; 3rd consonant stem 45; *-es* 28; plural *-i* 11; 3rd *-is* 10;
   plural *-ae* 4; *-am/-ae* 3 (*Abraham*, *Abrahae*); Greek *-e* 1.
   12 forms belong to two lemmas and keep both (*Michae*: *Micha*, *Michas*;
   *Sarae*: *Sara*, *Sares*).
3. **Hitchcock's Bible Names Dictionary** (1869, public domain; CCEL's
   ThML, pinned by sha256). Its headwords are the King James spellings, so a
   lemma is matched exactly, then after the regular spelling correspondences
   (*Sadoc* ~ *Zadok*, *Basan* ~ *Bashan*), then less a Latin *-s*/*-us*
   (*Jeremias* ~ *Jeremiah*). 1,017 lemmas match: 567 exact, 407 by
   spelling, 43 by ending. The row carries Hitchcock's headword, entry id and
   gloss verbatim; nothing is added. 1,987 lemmas have no match (*Josue*,
   *Galaad*, *Nabuchodonosor*: the Vulgate's and the King James's spellings
   differ too much); they are names by step 1 all the same.

From E to F, 3,381 forms (17,637 tokens) go from unknown to a name, and 200
(877 tokens) from a rule's reading to a name. The commonest names now read:
*Aaron* 322, *Abraham* 221 (with *Abrahae*), *Jordanis* 198 (with
*Jordanem*, *Jordane*), *Joseph* 186, *Josue* 183, *Ephraim* 180, *Sion*
180, *Jonathas* 165, *Benjamin* 163, *Jeremias* 159.

**Known limits, for review.** The classes are tried in a fixed order, so where
both *X-a* and *X-as* are written the *-as* name wins the *-a* form (*Idumaea*
is filed under *Idumaeas*). The `ending` tier of Hitchcock is the weakest and
gives a few wrong identities (*Jacobus* ~ *Jacob*, *Antiochus* ~
*Antioch*); the lemma never depends on it. A name's case is not given. Names
WORDS already has (*Israel*, *David*, *Moyses*, *Jesus*, *Aegyptus*) are not
in the table: WORDS reads them plainly.

### G: the house supplement

`data/lemmas/house-supplement.jsonl`: 24 rows, 33 distinct forms, 190 tokens,
exactly the gaps listed above under "Missing from WORDS's vocabulary". Every
row has provenance `house`, its attestation (each count is checked against the
text) and a justification from the Vulgate's forms and, where it has the word,
Lewis & Short (1879, public domain). A row is either an entry in DICTLINE's
terms, read by WORDS's own endings (with `only_forms`, just the forms it
cites), or forms with their parse given outright. "Of Whitaker's lemma" means
the forms are read as DICTLINE's own lemma, so they join it.

| lemma | kind | Vulgate forms |
|---|---|---|
| pharisaeus, pharisaei | entry | *pharisaei* 55, *pharisaeorum* 17, *pharisaeis* 13, *pharisaeus* 9, *pharisaeos* 6, *pharisaee* 1 |
| sadducaeus, sadducaei | entry | *sadducaeorum* 7, *sadducaei* 5, *sadducaeis* 1, *sadducaeos* 1 |
| setim, undeclined | entry | *setim* 30 |
| theraphim, undeclined | entry | *theraphim* 4 |
| carmel, undeclined | entry | *carmel* 6 (the common noun, in Isaiah; *Carmel* the mountain is a name) |
| bas, baseos/is (of Whitaker's lemma) | forms | *basim* 10, *basem* 1 |
| prophetis, prophetidis | entry, only its forms | *prophetidem* 2 |
| empticius, empticia, empticium (of Whitaker's lemma) | entry, only its forms | *emptitius* 2, *emptitii* 1 |
| sardonychus, sardonycha, sardonychum | entry, only its forms | *sardonycho* 1 |
| mygale, mygales | entry, only its forms | *mygale* 1 |
| psaltes, psaltae (of Whitaker's lemma) | forms | *psaltem* 1 |
| myrum, myri | entry, only its forms | *myro* 1 |
| smegma, smegmatis (of Whitaker's lemma) | entry, only its forms | *smigmata* 1 |
| querulosus, querulosa, querulosum | entry, only its forms | *querulosi* 1 |
| nerviceus, nervicea, nerviceum | entry, only its forms | *nerviceis* 1 |
| onusto, onustare, -, onustatus | entry, only its forms | *onustati* 1 |
| pirus, piri (of Whitaker's lemma) | entry, only its forms | *pyrorum* 4 |
| pirum, piri (of Whitaker's lemma) | entry, only its forms | *pyrorum* 4 |
| quaeso, quaesere, -, - (of Whitaker's lemma) | forms | *quaesumus* 2 |
| ruo, ruere, rui, rutus (of Whitaker's lemma) | entry, only its forms | *ruituri* 1 |
| sancio, sancire, sanxi, sanctus (of Whitaker's lemma) | entry, only its forms | *sancitum* 1 |
| circumlino, circumlinere, circumlevi, circumlitus (of Whitaker's lemma) | entry, only its forms | *circumlinisti* 1 |
| plecto, plectere, plexi, plectus (of Whitaker's lemma) | entry, only its forms | *plexueris* 1 |
| fascio, fasciare, -, fasciatus | entry, only its forms | *fasciaretur* 1 |

Two headings rest on the house rather than on a source, and say so in their
rows: *sadducaeus* is headed in the singular like *pharisaeus* (Lewis & Short
heads it *Sadducaei*, and the Vulgate writes only plurals), and the gender of
the undeclined *setim*, *theraphim* and *carmel* is not evidenced (filed
neuter, as DICTLINE files *ephod* and *manna*). *Onusto* and *fascio* are given
no perfect, because none is attested.

Not supplied: *bahem* (one form; no public-domain lemma to hang it on),
*ixion* (a bird here; Lewis & Short has only the mythical Ixion; one token),
*horon* (a fragment: the benchmark splits *Beth-horon* at the hyphen), and
*ejicicetur* (the misprint).

From F to G, 26 forms (153 tokens) go from unknown to read and 7 (37 tokens)
from a guess to read.

### Both switches are off in the lemma spine

The supplement (`Whitaker(house_supplement=True)`) and the names table
(`X.names = proper_names.load()`) are loaded only when asked for, and the hymn
build asks for neither, so `build_lemma_spine.py --check` and
`build_hymn_corpus.py --check` are byte-identical. The capitalisation rule is
on, but the hymn build passes search keys, which are never capitalised. Whether
the spine should load the supplement and the names is Adam's call.

## PACK headings: two options for Adam

WORDS prints no dictionary form for a qu-pronoun + PACKON entry. The house
composes one from the pronoun's heading and the tackon (the default, unchanged).
`Whitaker(pack_headings="real")` or `build_lemma_spine.py --pack-headings real`
heads them instead as a dictionary would, following Lewis & Short where it
heads the word. On the hymns the switch changes one form's analyses (*quoque*,
whose PACKON readings are renamed) and no token's lemma or parsing.

| house heading (default) | real heading (`--pack-headings real`) |
|---|---|
| qui, quae, quod + -cumque | quicumque, quaecumque, quodcumque |
| qui, quae, quod + -cunque | quicunque, quaecunque, quodcunque |
| qui, quae, quod + -dam | quidam, quaedam, quoddam |
| qui, quae, quod + -libet | quilibet, quaelibet, quodlibet |
| qui, quae, quod + -lubet | quilubet, quaelubet, quodlubet |
| qui, quae, quod + -nam | quinam, quaenam, quodnam |
| qui, quae, quod + -quam | quisquam, quaequam, quidquam |
| qui, quae, quod + -que | quisque, quaeque, quodque |
| qui, quae, quod + -vis | quivis, quaevis, quodvis |
| quis, quid + -cum | *(kept: WORDS's entry is "only ABL", quocum; there is no nominative to head it)* |
| quis, quid + -dam | quidam, quiddam |
| quis, quid + -libet | quilibet, quidlibet |
| quis, quid + -lubet | quilubet, quidlubet |
| quis, quid + -nam | quisnam, quidnam |
| quis, quid + -piam | quispiam, quidpiam |
| quis, quid + -que | quisque, quidque |
| quis, quid + -vis | quivis, quidvis |

Points for the ruling: under "real", *quidam* and *quisque* each head two
lemmas (WORDS's adjectival and substantival entries stay apart, as their keys
do); *quisquam* is filed by WORDS under the adjectival *qui*, and the real
heading is Lewis & Short's (*quisquam, quaequam, quidquam*); the headword
becomes *quidam* rather than *qui*, so a hymn draft that says *quidam* would
agree with Whitaker instead of disagreeing.
