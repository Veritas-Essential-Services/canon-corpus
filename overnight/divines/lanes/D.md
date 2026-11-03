# Lane D — Storytellers

slug: `storytellers` · queue: `overnight/divines/QUEUE-D.json` · map section: `docs/divines-map/D-storytellers.md`

## Notes for this lane's authors

- **Andrew Lang** (storytellers): English original, public domain — the twelve Coloured Fairy Books (Blue, Red, Green, etc.), his poetry, folklore/myth scholarship, histories. His Homer translations (with Butcher and Leaf) can cross-reference a Homer section later; keep them on his shelf with their own uids.
- **Charles Lamb** (storytellers): English original, public domain — Essays of Elia, the letters, Tales from Shakespeare (with Mary Lamb). Credit Mary on Tales from Shakespeare.
- **The STORYTELLERS grouping also gathers the fables work already in this repo.** Do NOT assume a path — SEARCH the repo first (`git grep -il -E 'fable|aesop|a_?fable' -- '*.py' '*.json' '*.md' docs pipeline`, list what you find in the report, and fold the existing fable shelf/section into the Storytellers map by cross-reference). If you find nothing, say so in the report and leave a `pending: locate earlier fables work` note rather than creating a duplicate. Never re-ingest or re-mint uids for fables already held.

## Cross-lane rules

**Cross-lane references (B ↔ C).** Lane C builds the Dryden and Garnett shelves; Lane B's Ovid and Virgil sections point at Dryden's titles. Whichever lane you are: never fetch or shelve another lane's titles. Lane B: if a Dryden slug does not exist yet, list it in your map section as `cross-ref → Dryden shelf (lane C), pending` and move on — do not wait, do not fetch Dryden. Lane C: name Dryden's slugs predictably (`dryden-aeneid`, `dryden-georgics`, `dryden-eclogues`, `dryden-metamorphoses`) so Lane B's pointers resolve, and never shelve a non-Dryden translation of Ovid or Virgil.
