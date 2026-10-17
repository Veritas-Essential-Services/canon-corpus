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
| `locator` | `heading:<words>`, which takes the units under the one heading of a converted book whose id contains those words; or `lines:<start>\|<end>`, which takes the raw text from the first line matching regex `<start>` up to the next line matching `<end>` |
| `status` | `ok` (cut), `held` (the collection is held elsewhere), `lane` (belongs to a relay lane), `notpd`, `nosource` (no PD source found yet), `todo` |
| `note` | translator, edition, or why a piece is not cut |

Prefer `lines:` when a piece has numbered parts, because the converter turns each part into its own heading. A cut from an Internet Archive scan is unproofread OCR and says so in its `honesty` field.

    python3 pipeline/extract_short_pieces.py --check   # every ok row resolves exactly once
    python3 pipeline/extract_short_pieces.py           # writes data/shorts/
    python3 tests/short_pieces_test.py
