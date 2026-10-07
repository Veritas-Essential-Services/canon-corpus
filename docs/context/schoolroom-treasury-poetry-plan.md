---
model_log:
  - 2026-10-07 claude-opus-5-5 drafted
fable_review: pending
---
# The Schoolroom Treasury: Poetry and Song

Oct 7, 2026

## Aim

One graded volume of English poems and songs published up to 1930: the pieces schoolchildren actually learned by heart, from nursery verse to Horatius at the bridge. Teachers will use it as the standard book, and children will bank its pieces in the Mnemonicon.

- **Reader:** the teacher or parent who reads it aloud, then the child who memorizes from it.
- **First in the series.** The other volumes (nursery, fables, myth, Arthur, saints, mathematics, riddles, jokes, stories) copy its method.

## Selection rule

A piece earns its place by evidence, not by our taste: how many period school readers and anthologies carried it. That makes "every piece a schoolboy delighted to memorize" countable.

1. Tally every poem in a fixed set of readers and anthologies (next section), matched across sources by first line and author.
2. Rank by the number of sources that carry it, as the hymn manifest ranks hymns by hymnals.
3. Admit everything above a threshold Adam sets, plus the AO list and the heroic addendum by right.
4. Keep a short, named list of editor's additions below the threshold, each with a one-line reason.

## Sources to tally

Only Lyra Heroica is checked so far. Every other row needs its edition and link confirmed before it is counted.

| Source | Year | Kind | Status |
| --- | --- | --- | --- |
| AmblesideOnline poetry rotation | current | curriculum list | in canon-corpus (1,487 rows) |
| Heroic addendum | 2026 | house list | in canon-corpus (58 rows, proposed) |
| Henley, [Lyra Heroica](https://www.gutenberg.org/ebooks/19316) | 1891 | boys' anthology | checked |
| Palgrave, The Golden Treasury | 1861 | anthology | to confirm |
| Quiller-Couch, The Oxford Book of English Verse | 1900 | anthology | to confirm |
| Percy, Reliques; Scott, Minstrelsy | 1765; 1802 | ballads | checked (see the masculine-counterparts file) |
| British school readers and recitation books | 1850s–1930 | readers | to locate |
| McGuffey's Eclectic Readers | 1836–1879 | American readers | to confirm; a check on the British list |

## Grading

Each piece is placed in the earliest year that most of the readers placed it, with AO's year used where AO lists it.

| Band | Ages | What goes here |
| --- | --- | --- |
| Nursery | 3–6 | rhymes, lullabies, singing games (also the Nursery volume) |
| Years 1–3 | 6–9 | short lyrics, fables in verse, simple ballads |
| Years 4–6 | 9–12 | story ballads, Horatius, sea and soldier songs |
| Years 7–9 | 12–15 | Scott, Macaulay, Kipling, Shakespeare speeches |
| Years 10–12 | 15–18 | Milton, Spenser, the long odes and epics in extract |

Every piece also gets a length and a difficulty mark, so the Mnemonicon can portion it out stanza by stanza.

## Rights gate

The 1930 line is exactly the US public-domain line in 2026: anything published through 1930 can be printed in full in the US. canon-corpus already enforces this gate.

- **Print every admitted piece in full.** US law is the only rule this volume follows.
- **Editions, not just poems:** take the text from a pre-1931 printing, never a modern edited text.

## What already exists

Much of the volume's machinery is already built in canon-corpus.

| Piece | Where | Use in the volume |
| --- | --- | --- |
| AO poetry catalog, 1,487 rows by year and term | `data/poetry/selections/ao.jsonl` (PR #17) | the grading backbone |
| Heroic addendum, 58 rows | `addendum-heroic.jsonl` (PR #17) | admitted by right |
| Rights gate and text cutter | `pipeline/build_poetry.py` | full text only from pinned pre-1931 books |
| Mnemonicon packs | `exports/mnemonicon/poetry/` | the memorization edition |
| Masculine-counterpart sources and checked quotes | `docs/context/` (PR #18) | sources to tally, epigraphs |

What is missing is the tally itself: the readers and anthologies, parsed into rows and matched by first line.

## Steps

- [ ] Merge PR #17 (the poetry catalog) and PR #18 (the sources file)
- [ ] Confirm editions and links for every source in the tally table
- [ ] Parse each source into rows: first line, title, author, year printed, grade placed
- [ ] Match rows across sources and rank by count
- [ ] Adam sets the admission threshold and reviews the editor's additions
- [ ] Cut texts through the rights gate and grade them
- [ ] Build the read-aloud edition and the Mnemonicon packs

## Open questions

- Admission threshold: how many sources must carry a piece?
- Should American readers count toward the tally, or serve only as a check?
- One volume, or one book per band?

Living copy (editable): https://claude.ai/code/artifact/8151c654-d39c-4d3e-bc8e-c3cc7f22457a
