---
model_log:
  - 2026-10-06 claude-opus-5-5 drafted
fable_review: pending
---
# data/poetry — the Word Hoard poetry section

Two layers of poems, one shape, and Mnemonicon memory packs built from them.
Build: `pipeline/build_poetry.py`. Validator: `tests/poetry_test.py`.

| Layer | Tag | What it is |
|---|---|---|
| **AO** | `ao` | AmblesideOnline's poetry selections, Years 1–12 and the Canadian supplement, as AO schedules them (year, term, order). |
| **Heroic addendum** | `addendum-heroic` | The house's own proposals: heroic, adventurous and vocational verse, plus a few songs. Same year/term slots so it sits **beside** the AO list, never inside it. Every row is `status: proposed` until Adam rules on it. |

A poem in both layers is one poem: one citation (`poetry:<poet>.<title>`),
one `wh-` uid, one Mnemonicon piece id.

## Files

| File | Committed | Made by |
|---|---|---|
| `selections/ao.jsonl` | yes | curated: AO's schedule (read from amblesideonline.org poet pages and year booklists, 2026-10-06) |
| `selections/addendum-heroic.jsonl` | yes | curated: the house's proposals |
| `poets.json` | yes | curated: names, aliases, birth/death years (death year drives only the life+70 note) |
| `sources.json` | yes | the Project Gutenberg books texts are cut from, with mirror URL and sha256 |
| `catalog-ao.jsonl`, `catalog-addendum-heroic.jsonl` | yes | **built**: one row per selection, with uid, rights and hosting decision |
| `texts.jsonl` | yes | **built**: the hosted texts, public domain only, cut from the pinned books |
| `../../exports/mnemonicon/poetry/*.json` | yes | **built**: import files, one per year and term (`ao-y02-t1.json`, `heroic-y05-t1.json`, …) |
| `../corpus/gitenberg/<n>.txt` | no (gitignored) | `--fetch` |

## A catalog row

```json
{"uid": "wh-…", "citation": "poetry:walter-de-la-mare.silver", "layer": "ao",
 "tags": ["poetry", "ao", "ao-y2", "ao-y2-t1", "walter-de-la-mare"],
 "year": 2, "term": 1, "order": 12, "poet": "Walter de la Mare", "poet_died": 1956,
 "title": "Silver", "first_pub": {"work": "Peacock Pie", "year": 1913},
 "pd_source": {"gutenberg": 3753, "work": "Peacock Pie, a Book of Rhymes", "edition_year": null},
 "rights": {"us": "pd", "basis": "US public domain: first published 1913 …", "elsewhere": "… life + 70 …"},
 "host": "full", "link": "https://www.gutenberg.org/ebooks/3753", "pack": "ao-y02-t1",
 "ao_page": "https://www.amblesideonline.org/poet-delamare", "kind": null, "notes": "…"}
```

`year` is a number, or `"canada"` for AO's Canadian poets. `term` is null
where AO gives none (the Year 6 anthology, Year 12, the Canadian poets).
Addendum rows also carry `kind` (`heroic` · `adventurous` · `vocational` ·
`song`) and `status: "proposed"`.

## The rights rule (US, as of 1 January 2026)

Copyright follows the **edition**, not the poet (ADR 0001). The test is the
text we host:

- **`pd` → hosted in full** when the text is cut from a Gutenberg book whose
  header carries no copyright notice, and either the printing is dated before
  1931, or the poem was first published before 1931, or the poet died before
  1931. The reason is written into `rights.basis` in words, per poem.
- **`in-copyright` → linked out** when the poem was first published in 1931
  or later.
- **`uncertain` → linked out** when no first publication or pre-1931 printing
  could be established.
- A `pd` poem whose text has not been cut yet (its book is not on the mirror,
  the cut failed proofing, it is an excerpt or a book-length work, or no
  public-domain printing is pinned) is **linked out** and says why.

`rights.elsewhere` adds the life + 70 position for readers outside the US:
Frost, Milne, de la Mare, Sandburg, Millay and others who died after 1955
are still in copyright in the UK, EU, Canada and Australia.

The house's posture is notice and takedown, not pre-screening; this gate is
only the line between hosting a text and linking to it.

## Long poems

A hosted poem over 120 lines is banked in parts of whole stanzas (about 40
lines each; a long verse paragraph breaks after a sentence). Part ids are
uuid5 of `<uid>#part<k>`, so they are as stable as a whole poem's.

## Where the texts come from

gutenberg.org is not reachable from the build sandbox, so books are fetched
from the GITenberg mirror on GitHub (`raw.githubusercontent.com/GITenberg/…`),
which mirrors Gutenberg's files up to about 2015, and pinned by sha256. Books
released later (Milne's two, Frost's *Collected Poems* 1930, the 1893
*Sing-Song*, Meynell's Blake) are not on the mirror; their poems stay linked
until they are fetched from gutenberg.org on a machine that can reach it.
