# Lemma review: the 24 flagged hymn tokens (2026-09-26)

**For:** Adam. **From:** the lemma spine (launch plan D3,
`pipeline/README-lemma-spine.md`). **Built from:** `data/hymns/tokens.jsonl` at
the commit that added this sheet, after WORDS's tricks, syncope and
prefix/suffix rules were ported.

A token is flagged when Whitaker's WORDS and the house draft disagree, when
WORDS offers several entries the draft cannot choose between, or when WORDS
has nothing. Until you answer, the **draft stands** on every flagged token.
Nothing here was overwritten.

**How to answer.** Write in the *Adam* column: `ok` to take the
recommendation, `keep` to keep the draft as it is, or your own answer. I turn
each answer into one row of `data/lemmas/adam-reviewed.jsonl` (README s.8).
The build then applies it with provenance `adam-reviewed`, and the draft and
the value it replaced stay on record. A row can set any of these:

- `lemma_key`: one of Whitaker's entries, by the name in the *Whitaker* column.
- `lemma`: a lemma as you want it written.
- `parsing`: a parsing as you want it written.

Most flags come in five kinds, so one ruling per kind would settle most of
the sheet:

| kind | rows | the question |
|---|---|---|
| **A.** Same word, WORDS heads it differently (*sē* under *sui*, *nōbīs* under *nōs*, *suprēmus* under *superus*, *duodēnī* under *duodecim*, *subiiciō* spelled *subjicio*) | 1, 2, 4, 6, 13, 16, 17, 18, 23 | Keep the house headword, and join to Whitaker through `lemma_key`? (Recommended.) |
| **B.** WORDS has two entries for one verb, transitive and intransitive | 3, 15, 19 | Pick by the sense in the line. |
| **C.** WORDS has two principal-part sets (*praestitī* / *praestāvī*) | 8, 21 | Take *praestitī*, the classical one. |
| **D.** Part of speech (*et*, *ergo*, *Amen*, *Thomas*) | 5, 7, 12, 20, 24 | Is the draft's class or WORDS's the house convention? |
| **E.** Real homographs (*fidēs* faith / *fidēs* lyre-string, *mundus* world / clean, *beātus* two entries, *ūnus* NUM / ADJ) | 10, 11, 14, 22 | Pick by sense. |

Row 9 (*pellicane*) is the odd one: WORDS has no pelican.

---

| # | Hymn · stanza · clause uid | Form, in its line | Draft lemma · parse | Whitaker's candidates | Why flagged | Recommend | Adam: |
|---|---|---|---|---|---|---|---|
| 1 | Adoro te · 1 · `wh-54JF0Y5SAS` (t02) | **se** · *Tibi se cor meum totum subiicit,* | sē · reflexive acc | `-, sui  PRON` (acc/abl, any number) | A: WORDS heads the reflexive under *sui* | `lemma_key` = `-, sui  PRON`; keep lemma *sē*; parsing stays | |
| 2 | Adoro te · 1 · `wh-54JF0Y5SAS` (t06) | **subiicit** · *Tibi se cor meum totum subiicit,* | subiciō, -ere, -iēcī, -iectum · 3 sg pres ind act, 3 conj (-iō) | `subjicio, subjicere, subjeci, subjectus  V (3rd) TRANS` (3 sg pres ind act) | A: WORDS spells it with *j* (so its headword folds to *subiicio*, not *subicio*) | `lemma_key` = WORDS's *subjicio* entry; keep the house lemma *subiciō* | |
| 3 | Adoro te · 1 · `wh-Q7RW8M6N3G` (t05) | **deficit** · *Quia te contemplans totum deficit.* | dēficiō, -ere, -fēcī, -fectum · 3 sg pres ind act, 3 conj (-iō) | `deficio … V (3rd) INTRANS` ("fail, grow faint"); `deficio … V (3rd) TRANS` ("fail, let down") | B: two entries, same parse | `lemma_key` = the **INTRANS** entry (the heart "fails", "faints") | |
| 4 | Adoro te · 2 · `wh-ZAQ3WCX1ZT` (t02) | **quidquid** · *Credo quidquid dixit Dei Filius:* | quisquis, quidquid · indef rel pron, n acc sg | `quidquid  PRON  (UNIQUES)` (nom/acc sg n) | A: WORDS lists *quidquid* as an irregular form with no dictionary heading | `keep`: the draft's *quisquis, quidquid* is the heading learners look up. A UNIQUES key would join only this one form. | |
| 5 | Adoro te · 3 · `wh-0861J9FP9P` (t05) | **et** · *At hic latet simul et humanitas;* | et · adv | `et  CONJ` | D: WORDS has only the conjunction | `keep` "adv". Here *et* = *etiam*, "also", which the grammars class as adverbial. | |
| 6 | Adoro te · 3 · `wh-9VBD834SNY` (t01) | **Ambo** · *Ambo tamen credens atque confitens,* | ambō, ambae, ambō · adj/pron, acc pl (dual-form) | `amb  NUM` ("both"; acc pl m/n and others) | A: WORDS's entry has one stem, so its printed heading is the bare stem *amb* | `lemma_key` = `amb  NUM`; keep lemma *ambō, ambae, ambō* | |
| 7 | Adoro te · 4 · `wh-DYSVH9E243` (t03) | **Thomas** · *Plagas, sicut Thomas, non intueor;* | Thōmās, -ae m. · nom sg (Greek 1st decl) | `Thomas, undeclined  N M` (N 9 9, eccl.) | D: WORDS treats the name as indeclinable. The lemma is already Whitaker's ("Thomas, undeclined"). | lemma *Thōmās, -ae m.* with WORDS's `lemma_key`; `keep` the parsing. The Vulgate declines it (*Thomae*). | |
| 8 | Adoro te · 5 · `wh-0Y016CRD3W` (t01) | **Praesta** · *Praesta meae menti de te vivere,* | praestō · 2 sg pres impv act | `praesto … praestiti, praestitus  V (1st)` (freq A); `praesto … praestavi, praestatus  V (1st)` (freq C) | C: two principal-part sets | `lemma_key` = the **praestiti** entry | |
| 9 | Adoro te · 6 · `wh-DZFZPFNWFA` (t02) | **pellicane** · *Pie pellicane, Iesu Domine,* | pellicānus, -ī m. · voc sg | `pellex, pellicis  N (3rd) F` + suffix *-an-*, read as ADJ voc sg m, "concubine-ish": wrong | WORDS has no *pelicanus* in any spelling. Before the port this token was `unknown`; now WORDS's own suffix rule mis-reads it. | `keep` the draft lemma and parse, no `lemma_key` | |
| 10 | Adoro te · 6 · `wh-04J0BZVQGS` (t02) | **una** · *Cuius una stilla salvum facere* | ūnus · f nom sg | `unus -a -um, primus … NUM` ("one", freq A); `unus, una, unum (gen -ius)  ADJ` ("alone, a single", freq E) | E: two entries | `lemma_key` = the **NUM** entry: "one drop", the cardinal | |
| 11 | Adoro te · 7 · `wh-CGTXCH3Y9B` (t08) | **beatus** · *Visu sim beatus tuae gloriae. Amen.* | beātus, -a, -um · m nom sg | `beatus, beata -um, beatior …  ADJ` ("happy, fortunate", classical); `beatus, beata, beatum  ADJ` ("blessed, blissful", medieval/eccl.); also *beo* ptc and noun *beatus* | E: two ADJ entries with the draft's parts | `lemma_key` = the classical **beatus, beata -um, beatior …** entry, which has the comparison forms. The eccl. entry is the closer sense, so this one is your call. | |
| 12 | Adoro te · 7 · `wh-CGTXCH3Y9B` (t11) | **Amen** · *Visu sim beatus tuae gloriae. Amen.* | āmēn · Hebrew, indecl | `amen  ADV` | D: WORDS parses it as an adverb | parsing "adv (Hebrew, indecl)": takes WORDS's class and keeps the note | |
| 13 | Pange lingua · 2 · `wh-G1VG74Z7Q5` (t01) | **Nobis** · *Nobis datus, nobis natus* | ego (pl nōs) · dat pl | `nos, nostrum  PRON` (dat/abl pl) | A: WORDS heads *nos* separately from *ego* | `lemma_key` = `nos, nostrum  PRON`; take its lemma. The second *nobis* in this line was drafted as *nōs* and already takes this entry, so this makes the pair match. | |
| 14 | Pange lingua · 2 · `wh-G1VG74Z7Q5` (t10) | **mundo** · *Et in mundo conversatus,* | mundus · abl sg | `mundus, mundi  N (2nd) M` ("world"); `mundus, munda -um …  ADJ` ("clean"); *mundo, mundare* V | E: the draft's lemma names no part of speech | `lemma_key` = `mundus, mundi  N (2nd) M` | |
| 15 | Pange lingua · 2 · `wh-G1VG74Z7Q5` (t19) | **clausit** · *Miro clausit ordine.* | claudō, -ere, clausī, clausum · 3 sg perf ind act | `claudo … V (3rd) TRANS` ("close, conclude"); `claudo … V (3rd) INTRANS` ("limp"); *claudeo* | B: two entries | `lemma_key` = the **TRANS** entry: he "closed" (*moras* is its object) | |
| 16 | Pange lingua · 3 · `wh-6BK80FRWKN` (t02) | **supremae** · *In supremae nocte cenae* | suprēmus, -a, -um · f gen sg | `superus, supera -um, superior …, supremus -a -um  ADJ` (gen sg f SUPER) | A: WORDS files *suprēmus* as the superlative of *superus* | `lemma_key` = the *superus* entry; keep lemma *suprēmus* | |
| 17 | Pange lingua · 3 · `wh-6BK80FRWKN` (t16) | **duodenae** · *Cibum turbae duodenae* | duodēnī, -ae, -a · f dat sg | `duodecim, duodecimus …, duodeni -ae -a …  NUM` (DIST, nom/voc **pl** f only) | A: one WORDS entry covers the whole numeral family. The parse was not checked. WORDS has no dat sg: distributives are plural. | `lemma_key` = the *duodecim* entry; keep lemma *duodēnī*; `keep` parsing "f dat sg" (a distributive used as a singular adjective with *turbae*) | |
| 18 | Pange lingua · 3 · `wh-6BK80FRWKN` (t17) | **Se** · *Se dat suis manibus.* | sē · reflexive acc | `-, sui  PRON` | A: as row 1 | as row 1 | |
| 19 | Pange lingua · 4 · `wh-VX7C0X53T0` (t04) | **deficit** · *Et si sensus deficit,* | dēficiō · 3 sg pres ind act | `deficio … INTRANS`; `deficio … TRANS` | B: as row 3 | `lemma_key` = the **INTRANS** entry ("if the senses fail") | |
| 20 | Pange lingua · 5 · `wh-CJ4HZ9V2X8` (t02) | **ergo** · *Tantum ergo Sacramentum* | ergō · conj | `ergo  ADV` | D: WORDS classes *ergo* as an adverb | parsing "adv (inferential: therefore)", since the dictionaries class it so. `keep` if the house teaches it as a conjunction. | |
| 21 | Pange lingua · 5 · `wh-KJD6FQ9548` (t01) | **Praestet** · *Praestet fides supplementum* | praestō, -āre · 3 sg pres subj act | *praestiti* and *praestavi* entries (as row 8); also impersonal *praestat* | C: as row 8 | `lemma_key` = the **praestiti** entry | |
| 22 | Pange lingua · 5 · `wh-KJD6FQ9548` (t02) | **fides** · *Praestet fides supplementum* | fidēs · nom sg | `fides, fidei  N (5th) F` ("faith"); `fides, fidis  N (3rd) F` ("lyre string"); *fidis*; *fido* | E: the draft's lemma names no declension | `lemma_key` = `fides, fidei  N (5th) F` | |
| 23 | Pange lingua · 6 · `wh-2YZEYPB0HE` (t03) | **utroque** · *Procedenti ab utroque* | uterque, utraque, utrumque · m abl sg | `uter, utra, utrum  ADJ` + *-que* (abl sg m/n); `utroque  ADV`; `utro  ADV` + *-que* | A: WORDS builds *uterque* as *uter* + *-que* and has no *uterque* heading | lemma *uterque, utraque, utrumque* with `lemma_key` = `uter, utra, utrum  ADJ`; parsing stays | |
| 24 | Pange lingua · 6 · `wh-2YZEYPB0HE` (t07) | **Amen** · *Compar sit laudatio. Amen.* | āmēn · Hebrew, indecl | `amen  ADV` | D: as row 12 | as row 12 | |

Row numbers are for talking about the sheet only. Each answer is keyed by
the token's address: the clause uid plus the token number in brackets, e.g.
`wh-54JF0Y5SAS/la.1.t02`.

## What an answer looks like in the file

Row 8, taken as recommended:

```
{"address": "wh-0Y016CRD3W/la.1.t01", "surface": "Praesta",
 "lemma_key": "praesto, praestare, praestiti, praestitus  V (1st)",
 "reviewed_on": "2026-09-27"}
```

Row 2, keeping the house spelling but joining to Whitaker:

```
{"address": "wh-54JF0Y5SAS/la.1.t06", "surface": "subiicit",
 "lemma": "subiciō, -ere, -iēcī, -iectum",
 "lemma_key": "subjicio, subjicere, subjeci, subjectus  V (3rd) TRANS",
 "reviewed_on": "2026-09-27", "note": "house spelling; WORDS spells with j"}
```

Row 5, keeping the draft's parsing:

```
{"address": "wh-0861J9FP9P/la.1.t05", "surface": "et", "parsing": "adv",
 "reviewed_on": "2026-09-27", "note": "et = etiam"}
```

The build refuses a `lemma_key` that is not one of Whitaker's analyses of
that form. It also refuses a row whose surface no longer matches its token.
Then run `python pipeline/build_hymn_corpus.py` and
`python tests/lemma_spine_test.py`, and commit `data/lemmas/adam-reviewed.jsonl`
with `data/hymns/`.
