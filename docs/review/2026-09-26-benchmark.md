# The WORDS port against the Clementine Vulgate (2026-09-26)

*How much of a real ecclesiastical Latin text the lemma spine's analyzer
(`pipeline/whitaker.py`, `pipeline/whitaker_tricks.py`) can read, and by what
rule. Produced by `pipeline/benchmark_whitaker.py`. Numbers and single forms
only; no running text is quoted.*

```
python pipeline/build_lemma_spine.py --fetch     # the Whitaker files and pinned Ada
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

## Four states of the port, all from today

| state | what it adds |
|---|---|
| **A** | stem + ending, uniques, enclitics: the port as it was this morning |
| **B** | + SYNCOPE, SLURY, FIXES, TRICKS: the port by noon |
| **C** | + Roman numerals and the non-enclitic TACKONs (task 1) |
| **D** | + what this benchmark sent back to the Ada for (task 3): stem keys as `makedict_main.adb` writes them, and the PACKONs and TICKONs of Word's Qu block |

A, B and C key stems by slot, as the port did before D. The fix that folds
the enclitic *-ve* is in all four, because it cannot be switched off.

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

By kind (forms / tokens):

| kind | B | C | D |
|---|---|---|---|
| SYNCOPE | 641 / 2,437 | 641 / 2,437 | 641 / 2,437 |
| PREFIX | 282 / 895 | 281 / 894 | 280 / 892 |
| SUFFIX | 418 / 783 | 418 / 783 | 415 / 774 |
| TRICK | 286 / 1,488 | 284 / 1,279 | 283 / 1,093 |
| SLURY | 20 / 49 | 20 / 49 | 20 / 49 |
| TACKON | – | 26 / 726 | 25 / 725 |
| PACKON | – | – | 38 / 839 |
| TICKON | – | – | 1 / 2 |
| ROMAN | – | 0 / 0 | 0 / 0 |

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
capitalisation into the analyzer.

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
