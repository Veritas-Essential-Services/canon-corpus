# Short pieces

The stories, poems, fables, speeches and excerpts that classical and Christian curricula assign, kept as their own section of the corpus.

A short piece is rarely a book of its own. The Ransom of Red Chief lives in O. Henry's *Whirligigs*, and The Necklace lives in a Maupassant volume. So each collection is fetched as an ordinary shelf item (`pipeline/<shelf>_shelf.json`). `SHORT-PIECES.tsv` then says where each piece sits inside its collection. `pipeline/extract_short_pieces.py` cuts every piece out into `data/shorts/<piece>.json`, which is gitignored and rebuildable like `data/books/`.

## Columns

| Column | Meaning |
|---|---|
| `piece` | the piece's id, unique (used as the file name in `data/shorts/`) |
| `title`, `author`, `date`, `kind` | the piece itself. `kind` is one of short_story, poem, fable, fairy_tale, speech, essay, letter, document, sermon, hymn, excerpt |
| `lists` | the curricula that assign it, `;`-separated |
| `shelf`, `source` | the shelf and the item slug that hold it |
| `locator` | `heading:<words>`, which takes the units under the one heading of a converted book whose id contains those words; or `lines:<start>\|<end>[\|<n>]`, which takes the raw text from the first line matching regex `<start>` (the `<n>`th, when a contents page repeats the heading) up to the next line matching `<end>` |
| `status` | `ok` (cut), `held` (held as a whole work, or the same text as another row), `lane` (belongs to a relay lane), `notpd` (published after 1930), `nosource` (no PD source found yet), `todo` (PD or undated, not yet found in a shelved collection) |
| `note` | translator, edition, or why a piece is not cut |

Prefer `lines:` when a piece has numbered parts, because the converter turns each part into its own heading. A cut from an Internet Archive scan is unproofread OCR and says so in its `honesty` field.

    python3 pipeline/extract_short_pieces.py --check   # every ok row resolves exactly once
    python3 pipeline/extract_short_pieces.py           # writes data/shorts/
    python3 tests/short_pieces_test.py

## What is in it (2026-10-17)

1,568 rows from nine curricula: Classical Conversations, the Veritas Omnibus volumes, Wes Callihan, Andrew Kern, Andrew Pudewa, Heidi White, Angelina Stanford, Ambleside Online, Memoria Press, and the pieces inside the McGuffey, Elson and Baldwin readers those curricula use. The raw list rows, each with the URL it was read from, are in `docs/reading-lists/sources/` (`omnibus.tsv`, `callihan-kern.tsv`, `pudewa-white-stanford.tsv`, `readers.tsv`).

| Status | Rows |
|---|---|
| `ok`, cut and checked | 722 |
| `held` as a whole work | 137 |
| `todo` | 669 (135 of them hymns, which need a PD hymnal shelf) |
| `notpd` | 40 |

By kind, the cut pieces are 361 poems, 164 short stories, 77 essays, 53 excerpts, 43 speeches, 7 fables, 7 fairy tales, 6 plays, 2 sermons, a letter and a hymn.

How the locators were made: a scratch script looked for each title as a standalone heading (capitals, a numbered lesson heading, or a centred title) in every fetched collection, required the author's name near the heading or in the collection, skipped contents pages, took the cut up to the next heading of the same style, and threw out cuts too small or too large for their kind. Every `ok` row was then cut with `--check`, the outliers were read by hand, and six bad cuts were turned back to `held` or `todo` (each says why in `note`). The script is not committed: the TSV is the record, and every locator in it is plain text a person can read and fix.

Caveats:

- **A reader's cut is the reader's lesson.** McGuffey and Elson print a biographical note before the piece and vocabulary or study questions after it; those rows say so in `note`.
- **Readers sometimes abridge.** Elson and McGuffey print excerpts of long poems (The Vision of Sir Launfal, Snow-Bound) under the full title.
- **Most Internet Archive cuts are OCR** (the Elson grammar-school readers and Baldwin's Thirty More Famous Stories and Old Stories of the East) and keep their page numbers and running heads.
- **`held` from title matching is a pointer, not a proof.** It names the shelf whose title matched; open it before relying on it.
- **Undated rows** come from lists that gave no date. They are only `ok` where the collection that holds them is itself public domain.
