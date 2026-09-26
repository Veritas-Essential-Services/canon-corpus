# John 1:1–18 — house drafts for review

*2026-09-26. Branch `wip/john1-drafts`. Built from `data/nt/gloss-overrides.jsonl`
(137 rows, layer `house`, all `draft: true`) and `data/nt/prose-order.jsonl`
(18 verses, source `house-draft`, all draft). Schema: `pipeline/README-nt-jsonl.md`
s.12 and s.14. Until you review them, the reader badges every column these reach
"draft — awaiting Adam's review".*

## What this is

- **Glosses.** A contextual word gloss for each token where Strong's dictionary gloss
  misleads in the verse: all 22 nulls, all 42 `def-head` glosses (*commencement*,
  *luminousness*, *lay forth*, …), tense and mood the dictionary cannot carry (ἦν
  *was*, not *exist*), pronouns by use (αὐτοῦ *him* after a preposition, *his* after
  a noun), and case where English needs a preposition (*of-God*). The dictionary
  gloss is kept under `provenance.gloss.was`; nothing is lost. Word glosses in the
  hymns' hyphenated style, never more than four words. House work: no translation
  or lexicon was copied or consulted.
- **plain_form** (where given) is the word's form in the plain line only, e.g. a verb
  that absorbs its οὐ (*did-not-know*), or an article folded into *who-is*.
- **Plain line.** Each verse's `prose_order` walks the tokens in English order, the
  hymns' convention exactly: numbers are token positions, `[bracketed]` words are
  supplied, `absorbed` positions are carried by a neighbour. The line below is what
  `render_plain()` produces; it is rendered, never stored.

## How to answer

Write in the **Adam:** column: ✓ to accept, or your gloss / order (`draft→` leaves
a row a draft; `gloss: …; plain_form: …` sets both). Then
`python3 pipeline/review.py apply docs/review/2026-09-26-john1-drafts.md` does, per
row: drop `draft` and `drafted_on`, add `"reviewed_on"` (and `"layer":
"adam-reviewed"` for a gloss that is now yours), and rebuild with
`python3 pipeline/build_nt_corpus.py`. It stops on any answer it would have to
guess at, naming the row (README-nt-jsonl.md s.15). A row you reject can simply be
deleted: the dictionary gloss comes back.

## Four choices left for you

| verse | word | draft | the question |
|---|---|---|---|
| 1:5 | κατέλαβεν | *grasped* (*did-not-grasp*) | laid hold of: understood, or overcame? |
| 1:9 | ἐρχόμενον | *coming*, with *every man* | Robinson parses it with *man* (first) or with *the light*; the draft follows his first |
| 1:14 | ἐσκήνωσεν | *dwelt* | or the literal *tented* |
| 1:16 | ἀντί | *in-place-of* | grace in place of grace, or grace following grace? |


## John 1:1

`kjv:John.1.1` · `wh-AGJ6YAF47Q`

> Ἐν ἀρχῇ ἦν ὁ λόγος, καὶ ὁ λόγος ἦν πρὸς τὸν θεόν, καὶ θεὸς ἦν ὁ λόγος.

**Wooden** (draft glosses in Greek order): in beginning was the Word and the Word was with the God and God was the Word

**Plain:** In [the] beginning was the Word and the Word was with God and the Word was God

`prose_order` [1, "the", 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 16, 17, 15, 14] · `absorbed` [11]

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 2 | ἀρχῇ | commencement | beginning |  | arche in 'in the beginning': the beginning, not the ceremonial 'commencement' |  |
| 3 | ἦν | exist | was |  | the imperfect of eimi: 'was', not the timeless dictionary 'exist' |  |
| 5 | λόγος | something said | Word |  | logos here is the Word, the Prologue's title for him, not 'something said' |  |
| 8 | λόγος | something said | Word |  | logos here is the Word, the Prologue's title for him, not 'something said' |  |
| 9 | ἦν | exist | was |  | the imperfect of eimi: 'was', not the timeless dictionary 'exist' |  |
| 10 | πρὸς | — | with |  | pros with the accusative: 'with' (in company with); the dictionary gives no gloss |  |
| 15 | ἦν | exist | was |  | the imperfect of eimi: 'was', not the timeless dictionary 'exist' |  |
| 17 | λόγος | something said | Word |  | logos here is the Word, the Prologue's title for him, not 'something said' |  |


## John 1:2

`kjv:John.1.2` · `wh-N7Z29E6SEG`

> Οὗτος ἦν ἐν ἀρχῇ πρὸς τὸν θεόν.

**Wooden** (draft glosses in Greek order): he was in beginning with the God

**Plain:** He was in [the] beginning with God

`prose_order` [1, 2, 3, "the", 4, 5, 7] · `absorbed` [6]

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 2 | ἦν | exist | was |  | the imperfect of eimi: 'was', not the timeless dictionary 'exist' |  |
| 4 | ἀρχῇ | commencement | beginning |  | arche in 'in the beginning': the beginning, not the ceremonial 'commencement' |  |
| 5 | πρὸς | — | with |  | pros with the accusative: 'with' (in company with); the dictionary gives no gloss |  |


## John 1:3

`kjv:John.1.3` · `wh-1AR8W4B50X`

> Πάντα δι’ αὐτοῦ ἐγένετο, καὶ χωρὶς αὐτοῦ ἐγένετο οὐδὲ ἓν ὃ γέγονεν.

**Wooden** (draft glosses in Greek order): all-things through him came-to-be and without him came-to-be not-even one that has-come-to-be

**Plain:** All-things came-to-be through him and without him not-even one came-to-be that has-come-to-be

`prose_order` [1, 4, 2, 3, 5, 6, 7, 9, 10, 8, 11, 12] · `absorbed` []

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 1 | Πάντα | all | all-things |  | neuter plural panta: all things, not bare 'all' |  |
| 3 | αὐτοῦ | — | him |  | autou/auto after a preposition or as object: 'him' (the dictionary has no standalone him) |  |
| 4 | ἐγένετο | be | came-to-be |  | ginomai here: came into being (aorist); 'be' flattens it into a copula |  |
| 6 | χωρὶς | — | without |  | choris: 'without'; the dictionary gives no gloss |  |
| 7 | αὐτοῦ | — | him |  | autou/auto after a preposition or as object: 'him' (the dictionary has no standalone him) |  |
| 8 | ἐγένετο | be | came-to-be |  | ginomai here: came into being (aorist); 'be' flattens it into a copula |  |
| 9 | οὐδὲ | not | not-even |  | oude before hen: 'not even (one)', stronger than 'not' |  |
| 12 | γέγονεν | be | has-come-to-be |  | perfect of ginomai: 'has come to be' |  |


## John 1:4

`kjv:John.1.4` · `wh-1K68J8T2K7`

> Ἐν αὐτῷ ζωὴ ἦν, καὶ ἡ ζωὴ ἦν τὸ φῶς τῶν ἀνθρώπων,

**Wooden** (draft glosses in Greek order): in him life was and the life was the light of-the men

**Plain:** In him was life and the life was the light of men

`prose_order` [1, 2, 4, 3, 5, 6, 7, 8, 9, 10, 11, 12] · `absorbed` []

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 2 | αὐτῷ | — | him |  | autou/auto after a preposition or as object: 'him' (the dictionary has no standalone him) |  |
| 4 | ἦν | exist | was |  | the imperfect of eimi: 'was', not the timeless dictionary 'exist' |  |
| 8 | ἦν | exist | was |  | the imperfect of eimi: 'was', not the timeless dictionary 'exist' |  |
| 10 | φῶς | luminousness | light |  | phos is light itself; 'luminousness' is the dictionary's abstract sense |  |
| 11 | τῶν | the | of-the | of | genitive plural article: 'of the'; plain drops the article before generic 'men' |  |
| 12 | ἀνθρώπων | man | men |  | genitive plural of anthropos: 'men' (people), not singular 'man' |  |


## John 1:5

`kjv:John.1.5` · `wh-85ADTVKTWW`

> καὶ τὸ φῶς ἐν τῇ σκοτίᾳ φαίνει, καὶ ἡ σκοτία αὐτὸ οὐ κατέλαβεν.

**Wooden** (draft glosses in Greek order): and the light in the darkness shines and the darkness it not grasped

**Plain:** And the light shines in the darkness and the darkness did-not-grasp it

`prose_order` [1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 13, 11] · `absorbed` [12]

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 3 | φῶς | luminousness | light |  | phos is light itself; 'luminousness' is the dictionary's abstract sense |  |
| 7 | φαίνει | shine | shines |  | present indicative: 'shines' |  |
| 12 | οὐ | no | not |  | ou negates the verb: 'not', not the interjection 'no' |  |
| 13 | κατέλαβεν | take | grasped | did-not-grasp | katalambano: 'laid hold of', which can mean understood or overcame; draft takes 'grasped' -- Adam to rule |  |


## John 1:6

`kjv:John.1.6` · `wh-X6SEVZWDRF`

> Ἐγένετο ἄνθρωπος ἀπεσταλμένος παρὰ θεοῦ, ὄνομα αὐτῷ Ἰωάννης.

**Wooden** (draft glosses in Greek order): came-to-be man sent from God name to-him John

**Plain:** There-came [a] man sent from God his name [was] John

`prose_order` [1, "a", 2, 3, 4, 5, 7, 6, "was", 8] · `absorbed` []

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 1 | Ἐγένετο | be | came-to-be | there-came | egeneto opening a narrative: 'there came' (a man arose) |  |
| 3 | ἀπεσταλμένος | set | sent |  | perfect passive participle of apostello: 'sent', not 'set' |  |
| 7 | αὐτῷ | — | to-him | his | dative of possession: 'to him' (his) name |  |


## John 1:7

`kjv:John.1.7` · `wh-V68AC12DH7`

> Οὗτος ἦλθεν εἰς μαρτυρίαν, ἵνα μαρτυρήσῃ περὶ τοῦ φωτός, ἵνα πάντες πιστεύσωσιν δι’ αὐτοῦ.

**Wooden** (draft glosses in Greek order): he came for witness that might-bear-witness concerning the light that all might-believe through him

**Plain:** He came for witness that [he] might-bear-witness concerning the light that all might-believe through him

`prose_order` [1, 2, 3, 4, 5, "he", 6, 7, 8, 9, 10, 11, 12, 13, 14] · `absorbed` []

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 2 | ἦλθεν | come | came |  | aorist of erchomai: 'came' |  |
| 3 | εἰς | to | for |  | eis of purpose: 'for' |  |
| 4 | μαρτυρίαν | evidence given | witness |  | martyria: witness, testimony; 'evidence given' is the dictionary's paraphrase |  |
| 6 | μαρτυρήσῃ | witness | might-bear-witness |  | aorist subjunctive after hina: 'might bear witness' |  |
| 7 | περὶ | with | concerning |  | peri with the genitive: 'concerning'; 'with' is its accusative sense |  |
| 9 | φωτός | luminousness | light |  | phos is light itself; 'luminousness' is the dictionary's abstract sense |  |
| 12 | πιστεύσωσιν | have faith | might-believe |  | aorist subjunctive of pisteuo: 'might believe' |  |
| 14 | αὐτοῦ | — | him |  | autou/auto after a preposition or as object: 'him' (the dictionary has no standalone him) |  |


## John 1:8

`kjv:John.1.8` · `wh-5NV9W6SVQK`

> Οὐκ ἦν ἐκεῖνος τὸ φῶς, ἀλλ’ ἵνα μαρτυρήσῃ περὶ τοῦ φωτός.

**Wooden** (draft glosses in Greek order): not was he the light but that might-bear-witness concerning the light

**Plain:** He was not the light but [came] that [he] might-bear-witness concerning the light

`prose_order` [3, 2, 1, 4, 5, 6, "came", 7, "he", 8, 9, 10, 11] · `absorbed` []

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 1 | Οὐκ | no | not |  | ou negates the verb: 'not', not the interjection 'no' |  |
| 2 | ἦν | exist | was |  | the imperfect of eimi: 'was', not the timeless dictionary 'exist' |  |
| 5 | φῶς | luminousness | light |  | phos is light itself; 'luminousness' is the dictionary's abstract sense |  |
| 6 | ἀλλ’ | — | but |  | alla: 'but', the contrast; the dictionary gives no gloss |  |
| 8 | μαρτυρήσῃ | witness | might-bear-witness |  | aorist subjunctive after hina: 'might bear witness' |  |
| 9 | περὶ | with | concerning |  | peri with the genitive: 'concerning'; 'with' is its accusative sense |  |
| 11 | φωτός | luminousness | light |  | phos is light itself; 'luminousness' is the dictionary's abstract sense |  |


## John 1:9

`kjv:John.1.9` · `wh-4FCS8SH6DF`

> Ἦν τὸ φῶς τὸ ἀληθινόν, ὃ φωτίζει πάντα ἄνθρωπον ἐρχόμενον εἰς τὸν κόσμον.

**Wooden** (draft glosses in Greek order): was the light the true that gives-light-to every man coming into the world

**Plain:** [It] was the true light that gives-light-to every man coming into the world

`prose_order` ["it", 1, 2, 5, 3, 6, 7, 8, 9, 10, 11, 12, 13] · `absorbed` [4]

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 1 | Ἦν | exist | was |  | the imperfect of eimi: 'was', not the timeless dictionary 'exist' |  |
| 3 | φῶς | luminousness | light |  | phos is light itself; 'luminousness' is the dictionary's abstract sense |  |
| 7 | φωτίζει | shed rays | gives-light-to |  | photizo: to give light to, from phos; 'shed rays' is the dictionary's literal |  |
| 8 | πάντα | all | every |  | pas with a singular noun and no article: 'every' |  |
| 10 | ἐρχόμενον | come | coming |  | present participle: 'coming'. Robinson parses it with 'man' or with 'light'; the draft follows his first parse -- Adam to rule |  |
| 11 | εἰς | to | into |  | eis with motion: 'into' |  |


## John 1:10

`kjv:John.1.10` · `wh-H3QSAJKTMQ`

> Ἐν τῷ κόσμῳ ἦν, καὶ ὁ κόσμος δι’ αὐτοῦ ἐγένετο, καὶ ὁ κόσμος αὐτὸν οὐκ ἔγνω.

**Wooden** (draft glosses in Greek order): in the world was and the world through him came-to-be and the world him not knew

**Plain:** [He] was in the world and the world came-to-be through him and the world did-not-know him

`prose_order` ["he", 4, 1, 2, 3, 5, 6, 7, 10, 8, 9, 11, 12, 13, 16, 14] · `absorbed` [15]

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 4 | ἦν | exist | was |  | the imperfect of eimi: 'was', not the timeless dictionary 'exist' |  |
| 9 | αὐτοῦ | — | him |  | autou/auto after a preposition or as object: 'him' (the dictionary has no standalone him) |  |
| 10 | ἐγένετο | be | came-to-be |  | ginomai here: came into being (aorist); 'be' flattens it into a copula |  |
| 14 | αὐτὸν | — | him |  | autou/auto after a preposition or as object: 'him' (the dictionary has no standalone him) |  |
| 15 | οὐκ | no | not |  | ou negates the verb: 'not', not the interjection 'no' |  |
| 16 | ἔγνω | know | knew | did-not-know | aorist of ginosko: 'knew' (recognised) |  |


## John 1:11

`kjv:John.1.11` · `wh-N7G5893KY9`

> Εἰς τὰ ἴδια ἦλθεν, καὶ οἱ ἴδιοι αὐτὸν οὐ παρέλαβον.

**Wooden** (draft glosses in Greek order): to the own-things came and the own-people him not received

**Plain:** [He] came to his-own and his-own-people did-not-receive him

`prose_order` ["he", 4, 1, 3, 5, 7, 10, 8] · `absorbed` [2, 6, 9]

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 3 | ἴδια | own | own-things | his-own | ta idia, neuter: his own things (his own home), not bare 'own' |  |
| 4 | ἦλθεν | come | came |  | aorist of erchomai: 'came' |  |
| 7 | ἴδιοι | own | own-people | his-own-people | hoi idioi, masculine: his own people |  |
| 8 | αὐτὸν | — | him |  | autou/auto after a preposition or as object: 'him' (the dictionary has no standalone him) |  |
| 9 | οὐ | no | not |  | ou negates the verb: 'not', not the interjection 'no' |  |
| 10 | παρέλαβον | receive | received | did-not-receive | paralambano: to receive (take to oneself), aorist |  |


## John 1:12

`kjv:John.1.12` · `wh-9W1VV098C1`

> Ὅσοι δὲ ἔλαβον αὐτόν, ἔδωκεν αὐτοῖς ἐξουσίαν τέκνα θεοῦ γενέσθαι, τοῖς πιστεύουσιν εἰς τὸ ὄνομα αὐτοῦ·

**Wooden** (draft glosses in Greek order): as-many-as but received him he-gave them authority children of-God to-become to-those believing in the name his

**Plain:** But as-many-as received him he-gave them authority to-become children of-God to-those-who believe in his name

`prose_order` [2, 1, 3, 4, 5, 6, 7, 10, 8, 9, 11, 12, 13, 16, 15] · `absorbed` [14]

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 1 | Ὅσοι | as | as-many-as |  | hosoi: 'as many as'; 'as' alone loses the quantity |  |
| 3 | ἔλαβον | take | received |  | aorist: 'received' (the dictionary's 'take' misses the welcome) |  |
| 4 | αὐτόν | — | him |  | autou/auto after a preposition or as object: 'him' (the dictionary has no standalone him) |  |
| 5 | ἔδωκεν | give | he-gave |  | aorist 3rd singular: 'he gave' |  |
| 7 | ἐξουσίαν | privilege | authority |  | exousia: authority, the right to; 'privilege' is weaker |  |
| 8 | τέκνα | child | children |  | tekna is plural: 'children' |  |
| 9 | θεοῦ | God | of-God |  | genitive: 'of God' |  |
| 10 | γενέσθαι | be | to-become |  | aorist infinitive of ginomai: 'to become' |  |
| 11 | τοῖς | the | to-those | to-those-who | dative plural article with the participle: 'to those (who)' |  |
| 12 | πιστεύουσιν | have faith | believing | believe | present participle of pisteuo: 'believing'; 'have faith' is the dictionary's |  |
| 13 | εἰς | to | in |  | eis after pisteuo: believe 'in' |  |
| 16 | αὐτοῦ | — | his |  | autou after a noun is possessive: 'his' |  |


## John 1:13

`kjv:John.1.13` · `wh-VAYBW6C9NT`

> οἳ οὐκ ἐξ αἱμάτων, οὐδὲ ἐκ θελήματος σαρκός, οὐδὲ ἐκ θελήματος ἀνδρός, ἀλλ’ ἐκ θεοῦ ἐγεννήθησαν.

**Wooden** (draft glosses in Greek order): who not from blood nor from will of-flesh nor from will of-a-man but from God were-born

**Plain:** Who were-born not from blood nor from [the] will of-flesh nor from [the] will of-a-man but from God

`prose_order` [1, 16, 2, 3, 4, 5, 6, "the", 7, 8, 9, 10, "the", 11, 12, 13, 14, 15] · `absorbed` []

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 1 | οἳ | that | who |  | relative pronoun, masculine plural: 'who' |  |
| 2 | οὐκ | no | not |  | ou negates the verb: 'not', not the interjection 'no' |  |
| 5 | οὐδὲ | not | nor |  | oude continuing a negative: 'nor' |  |
| 7 | θελήματος | determination | will |  | thelema: will; 'determination' is the dictionary's |  |
| 8 | σαρκός | flesh | of-flesh |  | genitive: 'of flesh' |  |
| 9 | οὐδὲ | not | nor |  | oude continuing a negative: 'nor' |  |
| 11 | θελήματος | determination | will |  | thelema: will; 'determination' is the dictionary's |  |
| 12 | ἀνδρός | man | of-a-man |  | aner, a man as male (husband), not anthropos: 'of a man' |  |
| 13 | ἀλλ’ | — | but |  | alla: 'but', the contrast; the dictionary gives no gloss |  |
| 16 | ἐγεννήθησαν | procreate | were-born |  | aorist passive of gennao: 'were born', not 'procreate' |  |


## John 1:14

`kjv:John.1.14` · `wh-C3YWSV9ZB6`

> Καὶ ὁ λόγος σὰρξ ἐγένετο, καὶ ἐσκήνωσεν ἐν ἡμῖν- καὶ ἐθεασάμεθα τὴν δόξαν αὐτοῦ, δόξαν ὡς μονογενοῦς παρὰ πατρός- πλήρης χάριτος καὶ ἀληθείας.

**Wooden** (draft glosses in Greek order): and the Word flesh became and dwelt among us and we-looked-upon the glory his glory as of-an-only-begotten from Father full of-grace and of-truth

**Plain:** And the Word became flesh and dwelt among us and we-looked-upon his glory glory as of-an-only-begotten from [the] Father full of-grace and truth

`prose_order` [1, 2, 3, 5, 4, 6, 7, 8, 9, 10, 11, 14, 13, 15, 16, 17, 18, "the", 19, 20, 21, 22, 23] · `absorbed` [12]

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 3 | λόγος | something said | Word |  | logos here is the Word, the Prologue's title for him, not 'something said' |  |
| 5 | ἐγένετο | be | became |  | egeneto with a predicate: 'became' |  |
| 7 | ἐσκήνωσεν | dwell | dwelt |  | skenoo: to live in a tent, aorist; 'dwelt' for now, 'tented' is the literal -- Adam to rule |  |
| 8 | ἐν | in | among |  | en with a plural: 'among' |  |
| 9 | ἡμῖν | — | us |  | hemin, dative plural: 'us'; the dictionary lists only I and me |  |
| 11 | ἐθεασάμεθα | look | we-looked-upon |  | theaomai, aorist 1st plural: 'we looked upon' (gazed at) |  |
| 14 | αὐτοῦ | — | his |  | autou after a noun is possessive: 'his' |  |
| 16 | ὡς | how | as |  | hos: 'as', not 'how' |  |
| 17 | μονογενοῦς | only | of-an-only-begotten |  | monogenes, genitive, no article: 'of an only-begotten' (the only one born) |  |
| 19 | πατρός | father | Father |  | pater here is God the Father |  |
| 21 | χάριτος | graciousness | of-grace |  | charis in the Prologue is grace (the gift), not 'graciousness' (the manner) |  |
| 23 | ἀληθείας | truth | of-truth | truth | genitive after 'full': 'of truth'; plain says 'of' once |  |


## John 1:15

`kjv:John.1.15` · `wh-5SYPF0BZJ7`

> Ἰωάννης μαρτυρεῖ περὶ αὐτοῦ, καὶ κέκραγεν λέγων, Οὗτος ἦν ὃν εἶπον, Ὁ ὀπίσω μου ἐρχόμενος ἔμπροσθέν μου γέγονεν· ὅτι πρῶτός μου ἦν.

**Wooden** (draft glosses in Greek order): John bears-witness concerning him and has-cried-out saying this was whom I-said the-one after me coming before me has-become because before me was

**Plain:** John bears-witness concerning him and has-cried-out saying this was [he] of-whom I-said he-who comes after me has-become before me because [he] was before me

`prose_order` [1, 2, 3, 4, 5, 6, 7, 8, 9, "he", 10, 11, 12, 15, 13, 14, 18, 16, 17, 19, "he", 22, 20, 21] · `absorbed` []

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 2 | μαρτυρεῖ | witness | bears-witness |  | present of martyreo: 'bears witness' |  |
| 3 | περὶ | with | concerning |  | peri with the genitive: 'concerning'; 'with' is its accusative sense |  |
| 4 | αὐτοῦ | — | him |  | autou/auto after a preposition or as object: 'him' (the dictionary has no standalone him) |  |
| 6 | κέκραγεν | cry | has-cried-out |  | perfect of krazo: 'has cried out' |  |
| 7 | λέγων | lay forth | saying |  | present participle of lego: 'saying'; 'lay forth' is the dictionary's root sense |  |
| 8 | Οὗτος | he | this |  | houtos pointing: 'this (one)' |  |
| 9 | ἦν | exist | was |  | the imperfect of eimi: 'was', not the timeless dictionary 'exist' |  |
| 10 | ὃν | that | whom | of-whom | relative, accusative: 'whom'; English says 'of whom I said' |  |
| 11 | εἶπον | lay forth | I-said |  | aorist 1st singular of lego: 'I said' |  |
| 12 | Ὁ | the | the-one | he-who | the article making the participle a noun: 'the one (coming)' |  |
| 13 | ὀπίσω | back | after |  | opiso with the genitive: 'after' (behind) me |  |
| 15 | ἐρχόμενος | come | coming | comes | present participle of erchomai: 'coming' |  |
| 16 | ἔμπροσθέν | — | before |  | emprosthen with the genitive: 'before' (ahead of); the dictionary gives no gloss |  |
| 18 | γέγονεν | be | has-become |  | perfect of ginomai: 'has become' |  |
| 19 | ὅτι | that | because |  | hoti giving the reason: 'because' |  |
| 20 | πρῶτός | foremost | before |  | protos with the genitive: first in relation to, i.e. before (me) |  |
| 22 | ἦν | exist | was |  | the imperfect of eimi: 'was', not the timeless dictionary 'exist' |  |


## John 1:16

`kjv:John.1.16` · `wh-WYER8R4SE6`

> Καὶ ἐκ τοῦ πληρώματος αὐτοῦ ἡμεῖς πάντες ἐλάβομεν, καὶ χάριν ἀντὶ χάριτος.

**Wooden** (draft glosses in Greek order): and from the fullness his we all received and grace in-place-of grace

**Plain:** And we all received from his fullness and grace in-place-of grace

`prose_order` [1, 6, 7, 8, 2, 5, 4, 9, 10, 11, 12] · `absorbed` [3]

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 4 | πληρώματος | repletion | fullness |  | pleroma: fullness; 'repletion' is the dictionary's |  |
| 5 | αὐτοῦ | — | his |  | autou after a noun is possessive: 'his' |  |
| 6 | ἡμεῖς | — | we |  | hemeis, nominative plural: 'we'; the dictionary lists only I and me |  |
| 8 | ἐλάβομεν | take | received |  | aorist: 'received' (the dictionary's 'take' misses the welcome) |  |
| 10 | χάριν | graciousness | grace |  | charis in the Prologue is grace (the gift), not 'graciousness' (the manner) |  |
| 11 | ἀντὶ | — | in-place-of |  | anti: in place of (grace following grace); the dictionary gives no gloss -- Adam to rule on the sense |  |
| 12 | χάριτος | graciousness | grace |  | charis in the Prologue is grace (the gift), not 'graciousness' (the manner) |  |


## John 1:17

`kjv:John.1.17` · `wh-TZFZ7RVT94`

> Ὅτι ὁ νόμος διὰ Μωσέως ἐδόθη, ἡ χάρις καὶ ἡ ἀλήθεια διὰ Ἰησοῦ χριστοῦ ἐγένετο.

**Wooden** (draft glosses in Greek order): because the law through Moses was-given the grace and the truth through Jesus Christ came

**Plain:** Because the law was-given through Moses grace and truth came through Jesus Christ

`prose_order` [1, 2, 3, 6, 4, 5, 8, 9, 11, 15, 12, 13, 14] · `absorbed` [7, 10]

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 1 | Ὅτι | that | because |  | hoti giving the reason: 'because' (for) |  |
| 6 | ἐδόθη | give | was-given |  | aorist passive of didomi: 'was given' |  |
| 8 | χάρις | graciousness | grace |  | charis in the Prologue is grace (the gift), not 'graciousness' (the manner) |  |
| 15 | ἐγένετο | be | came |  | egeneto of an event arriving: 'came' |  |


## John 1:18

`kjv:John.1.18` · `wh-5ZK3CD3S65`

> Θεὸν οὐδεὶς ἑώρακεν πώποτε· ὁ μονογενὴς υἱός, ὁ ὢν εἰς τὸν κόλπον τοῦ πατρός, ἐκεῖνος ἐξηγήσατο.

**Wooden** (draft glosses in Greek order): God no-one has-seen at any time the only-begotten Son the-one being in the bosom of-the Father he made-known

**Plain:** No-one has-seen God at any time the only-begotten Son who-is in the bosom of-the Father he made-known [him]

`prose_order` [2, 3, 1, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, "him"] · `absorbed` [8]

**Adam (plain line):** 

| # | Greek | dictionary | draft gloss | plain_form | why | Adam: |
|---|---|---|---|---|---|---|
| 2 | οὐδεὶς | not | no-one |  | oudeis, masculine: 'no one', not bare 'not' |  |
| 3 | ἑώρακεν | stare at | has-seen |  | perfect of horao: 'has seen'; 'stare at' is the dictionary's |  |
| 6 | μονογενὴς | only | only-begotten |  | monogenes: only-begotten (the only one born), not bare 'only' |  |
| 7 | υἱός | son | Son |  | huios here is the Son |  |
| 8 | ὁ | the | the-one |  | the article with the participle: 'the one (being)'; plain folds it into 'who is' |  |
| 9 | ὢν | exist | being | who-is | present participle of eimi: 'being' |  |
| 10 | εἰς | to | in |  | eis with a verb of being: 'in' (rest, not motion) |  |
| 13 | τοῦ | the | of-the |  | genitive article: 'of the' |  |
| 14 | πατρός | father | Father |  | pater here is God the Father |  |
| 16 | ἐξηγήσατο | consider out | made-known |  | exegeomai: to lead out, unfold, make known; 'consider out' is the dictionary's |  |
