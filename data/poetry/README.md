---
model_log:
  - 2026-10-06 claude-opus-5-5 drafted
fable_review: pending
---
# data/poetry — the Word Hoard poetry section

Three layers of poems, one shape, and Mnemonicon memory packs built from them.
Build: `pipeline/build_poetry.py`. Validator: `tests/poetry_test.py`.

| Layer | Tag | What it is |
|---|---|---|
| **AO** | `ao` | AmblesideOnline's poetry selections, Years 1–12 and the Canadian supplement, as AO schedules them (year, term, order). |
| **Heroic addendum** | `addendum-heroic` | The house's own proposals: heroic, adventurous and vocational verse, plus a few songs. Same year/term slots so it sits **beside** the AO list, never inside it. Every row is `status: proposed` until Adam rules on it. |
| **Treasury** | `treasury` | The Schoolroom Treasury's candidate pool: every verse candidate from the 55 old anthologies, readers and speakers in `pool/`, for Adam to cull. No year or term yet; every row is `status: candidate` and carries its `pool_id`. Selections are written by `pipeline/select_treasury.py`. |

A poem in two layers is one poem: one citation (`poetry:<poet>.<title>`),
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

Every hosted text is cut from a Project Gutenberg book pinned by sha256 in
`sources.json`. The first 120 books came from the GITenberg mirror on GitHub
(`raw.githubusercontent.com/GITenberg/…`), because gutenberg.org was not
reachable from the build sandbox when this section was built. From
2026-10-13 books come straight from `gutenberg.org/cache/epub/<n>/pg<n>.txt`
(Sing-Song, Frost's *Collected Poems* 1930, Meynell's Blake, and the books
that supplied a printing for poems no source had been pinned for).

### Finding a printing for a linked poem (2026-10-13)

A poem with no `pd_source` was matched by title, first against the poet's own
books on Project Gutenberg and then against the anthologies already in the
pool, and cut with this script's own `extract()`. A cut was kept only if:

- it carries no editorial prose, transcriber's note or bracketed headnote,
  and a trailing signature or source line is cut off by an `end` rule the
  build replays;
- for an anthology, the poet's name stands beside the poem;
- for an AmblesideOnline Year 1 poem, its first line matches AO's own
  transcription;
- no other printing gives a longer text of the same poem, unless AO's
  transcription confirms the shorter one.

Each such row says in `notes` how it was checked ("N printings agree on
it", "its length matches AO's transcription", or "found in one printing
only; not cross-checked"). Poems whose AO title is a generic one (*Song*,
*Epitaph*), excerpts ("from …"), and anonymous verse were left linked.

Two extract rules matter here: the existing `parts` (a poem whose stanzas are
numbered I., II., … across double blank lines, as in Lear) and `fix`, a
list of `[typo, mending]` pairs (new) for a printer's or transcriber's slip
(*Sing-Song*'s "Jives" for "lives"), applied to the cut text, never to the
book.

## The treasury layer (2026-10-17)

Adam asked for every poem in the candidate pool to be in the hoard. `pipeline/select_treasury.py` turns `pool/pool.jsonl` into `selections/treasury.jsonl`:

- **Which poems:** every verse candidate. The 667 prose pieces (speeches from the readers and speakers) wait for a declamation layer. A candidate already in the AO list or the addendum is not repeated.
- **Where the cut begins:** at the poem's first line as its book prints it, at the occurrence with the poem's title just above it, so a contents page or an index of first lines never wins. Books whose year was read from the book itself are tried first. The rule is stored in the row (`extract.first_line`, `occurrence`, and an `end` for a signature line at the foot) and the build replays it.
- **What is refused:** a cut that runs into the next poem of the book, a single line, more than 900 lines, prose, or an editor's bracketed note. Such a candidate stays in the layer, linked out, with the reasons.
- **Packs:** one per source book, `treasury-pg<n>.json`.

Order of a rebuild: `build_poetry.py --fetch`, `select_treasury.py --fetch` (fetches and pins the pool's books), `build_poetry.py`, then `build_poetry.py --check`.
