---
model_log:
  - 2026-09-26 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
fable_review: pending
---
# Agreement marks in the reader: two candidate forms

*2026-09-26. Launch plan D5. For Adam's choice; nothing is decided here.*

**Settled already.** Ruling #9 (2026-09-15, "The Column Question", s.4 and s.6):
the wooden column in verse carries agreement marks. Only the *form* was left
open, "to be chosen when the reader is built". The reader is now built
(`pipeline/render_reader.py`), and it has a toggle that shows both forms on the
real hymns.

**Where the marks come from.** From no new data. They are drawn at render time
from the house draft's `syntax` notes on each token: *modifies X*, *agrees with
X*, *refers to X*, *antecedent X*, *ablative absolute with X*. A note ties a word
to the one token in its clause whose `search_key` matches X, with an enclitic
*-que* allowed. Failing that, it ties to the one such token elsewhere in the
stanza. Groups are numbered per stanza, and the same number is used on the Latin
word and on its wooden gloss.

On the two hymns, 39 notes give 35 ties, 4 of them across a clause break.
*Adoro* st1: *contemplans* in c4 agrees with *cor* in c3, which is the Column
Question's own example. The 4 notes that are not drawn name no word in the
stanza (for example, "agrees with the 'I' of peto" or "modifies understood
subject"). An undrawn tie is honest, and a wrong one would be the lie the marks
exist to prevent. The most groups in one stanza is 4. The Greek has no
`syntax` notes yet, so it has no marks.

## Option A: superscript indices

`Tibi se³ cor³ meum³ totum³ subiicit`, and the same indices on
`To-you itself³ [my]-heart³ my³ whole³ submits`.

- **For it:** it prints. Ad Summum is print-first and already uses it: "agreement
  marks become superscript numbers on the page" (2026-09-17). Ad Summum's
  FINISH LINE recommends it suite-wide for prose that is taught. It survives
  photocopying, greyscale and colour-blindness, and a teacher can read it aloud
  ("the threes go together").
- **Against it:** it clutters. A dense stanza carries several numbers per line,
  and a child may read them as footnotes. The numbers only mean something inside
  one stanza.

## Option B: colour pairs

The words of a group share a colour and a thick underline of that colour, from
six colours, with a light and a dark set.

- **For it:** it reads at a glance, with no clutter in the words themselves.
  It is closest to how a teacher marks up a board.
- **Against it:** it does not print in greyscale or photocopy. About one boy in
  twelve is red-green colour-blind. The underline shows that a word is marked,
  but only the hue says which group it is in. A stanza with more than six groups would reuse a colour (none does today).

## Not built: the tie-bar

The note also named a tie-bar, an arc linking agreeing words. It is the clearest
form for adjacent pairs. It fails exactly where marks matter most: across a
line, and across a clause break.

## Recommendation, for what it is worth

**A as the default, with B as a screen-only toggle**, which is what the reader
does now. A is the form that serves Ad Summum's print, the Oratorium's handouts
and the screen alike. Either way it is a rendering rule, so changing it later
costs one CSS rule and no data.
