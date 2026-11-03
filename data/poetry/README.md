---
model_log:
  - 2026-10-06 claude-opus-5-5 drafted
  - 2026-11-03 claude-opus-5-5 added the declamations layer
fable_review: pending
---
# data/poetry — the Word Hoard poetry section

Four layers of poems and a layer of declamations, one shape, and Mnemonicon memory packs built from them.
Build: `pipeline/build_poetry.py`. Validator: `tests/poetry_test.py`.

| Layer | Tag | What it is |
|---|---|---|
| **AO** | `ao` | AmblesideOnline's poetry selections, Years 1–12 and the Canadian supplement, as AO schedules them (year, term, order). |
| **Heroic addendum** | `addendum-heroic` | The house's own proposals: heroic, adventurous and vocational verse, plus a few songs. Same year/term slots so it sits **beside** the AO list, never inside it. Every row is `status: proposed` until Adam rules on it. |
| **Treasury** | `treasury` | The Schoolroom Treasury's candidate pool: every verse candidate from the 55 old anthologies, readers and speakers in `pool/`, for Adam to cull. No year or term yet; every row is `status: candidate` and carries its `pool_id`. Selections are written by `pipeline/select_treasury.py`. |
| **Collections** | `collections` | A whole book or set of one poet's, taken entire at Adam's ask. Each row names its `collection` (its tag and its pack) and keeps the book's order. The first is `cowper-guyon`: all 37 of Cowper's translations of Madame Guyon. |
| **Declamations** | `declamations` | The prose half of the pool: the speeches, orations and reader lessons that schoolboys learned to declaim. Every row is `status: candidate`. Citations are `declamations:<speaker>.<title>`. Selections are written by `pipeline/select_declamations.py`; see *The declamations layer* below. |

A poem in two layers is one poem: one citation (`poetry:<poet>.<title>`),
one `wh-` uid, one Mnemonicon piece id.

## Files

| File | Committed | Made by |
|---|---|---|
| `selections/ao.jsonl` | yes | curated: AO's schedule (read from amblesideonline.org poet pages and year booklists, 2026-10-06) |
| `selections/addendum-heroic.jsonl` | yes | curated: the house's proposals |
| `poets.json` | yes | curated: names, aliases, birth/death years (death year drives only the life+70 note) |
| `sources.json` | yes | the Project Gutenberg books texts are cut from, with mirror URL and sha256 |
| `selections/treasury.jsonl` | yes | **built** by `select_treasury.py`: every verse candidate in the pool, with its cut |
| `selections/collections.jsonl` | yes | curated: whole collections, one row per poem in the book's order |
| `catalog-ao.jsonl`, `catalog-addendum-heroic.jsonl`, `catalog-treasury-N.jsonl` | yes | **built**: one row per selection, with uid, rights and hosting decision |
| `texts-N.jsonl` | yes | **built**: the hosted texts, public domain only, cut from the pinned books |
| `selections/declamations.jsonl` | yes | **built** by `select_declamations.py`: every prose piece in the pool, with its cut |
| `catalog-declamations.jsonl` | yes | **built**: one row per declamation, with uid, rights and hosting decision |
| `declamations-texts.jsonl` | yes | **built**: the hosted declamations, paragraphs one to a line |

A built JSONL over 4 MB is cut into numbered parts of whole rows (`texts-1.jsonl`, `texts-2.jsonl`, …) so no committed file passes the 5 MB cap; one that fits keeps its plain name. Read them with `read_parts()` in `build_poetry.py`, which takes either form.
| `../../exports/mnemonicon/poetry/*.json` | yes | **built**: import files, one per year and term (`ao-y02-t1.json`, `heroic-y05-t1.json`, …), one per source book for the treasury and the declamations (`treasury-pg<n>.json`, `declamation-pg<n>.json`) |
| `../corpus/gitenberg/<n>.txt`, `<n>.mirror.txt` | no (gitignored) | `--fetch` |

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

## The collections layer (2026-10-23)

When Adam wants a poet's book whole, it goes in `selections/collections.jsonl`. Every poem gets a row, in the book's order, and each row names its `collection` and `collection_title`. Each collection's poems are banked in one pack, `collection-<collection>.json`, and tagged with the collection's name.

**`cowper-guyon`** holds Cowper's *Translations from the French of Madame de la Mothe Guion*. Cowper made them in 1782, and they were published after his death (Newport Pagnell, 1801). There are 37 poems, cut from Grimshawe's one-volume *Works* (PG #47790, already pinned), which prints them all in its section of that name. Every cut begins after that section's heading (`extract.after`).
- The three night-season poems share a heading, "On the same", so the second and third carry `variant` `night-season-2` and `night-season-3`.
- *The Soul that Loves God finds him everywhere* is printed "every where".
- *A Figurative Description...* has a subtitle printed under its heading. The cut starts at the first line of verse, and the row's notes give the subtitle.

The prose "Brief Account of Madame Guion", which opens the section, is not verse and is left out.

## The declamations layer (2026-11-03)

The plan's prose section: the speeches and lessons the old readers and speakers printed for boys to declaim. `pipeline/select_declamations.py` turns the pool's 667 prose rows into `selections/declamations.jsonl`, and the build gives each one a uid, a rights decision and, where the cut is clean, a hosted text.

- **Which pieces:** every pool row of kind `prose`, plus the plan's Crispin's Day speech (see below). A piece already in another layer is not repeated. Five are skipped this way, for example McGuffey's "Henry V to His Troops", which is "Once more unto the breach" and is already in the treasury. When a speech is printed in two books, the books are matched by their opening ten words, and the speakers must agree. Such a speech is one piece; the second printing is named in the row's notes. "The Same Concluded" goes with its speech.
- **Where the cut begins and ends:** the cut begins at the first line of text under the piece's printed heading. It passes over a byline, a "(_1775_)" date line, an indented headnote or scene line, and McGuffey's life of the author, all of which are kept in the row as `headnote`. The cut stops above the next heading, NOTES, DEFINITIONS or EXERCISES, or the signature line. The signature is kept as `signed`. The rule is stored in the row (`extract`) and the build replays it.
- **Paragraphs:** a prose cut keeps its paragraphs, one to a line in the text. Wrapped lines are joined (`reflow`). McGuffey's paragraph numbers are dropped (`para_numbers`). The Third Reader is printed page by page, so its running heads and signature marks are dropped (`drop`), and its paragraphs are found from its numbers (`join_pages`). Dialogue gives each speaker a line (`speakers`). A verse quotation inside a speech keeps its lines. A transcriber's bracketed note is skipped (`skip_notes`). A piece that is verse (some McGuffey and speaker poems the pool called prose) is cut as verse and marked `form: verse`.
- **What is refused:** a cut is refused if it:
  - runs into the next piece
  - runs past a signature
  - is an editor's or transcriber's note
  - is the reader's introduction (elocution exercises, front matter)
  - is a play in several scenes
  - is under 20 words or over 4000 words, one declamation's cap

  A refused piece stays in the layer, linked out, and its rights note gives the reason.
- **Grade hint:** `grade_hint.audiences` copies the pool's audiences. For a McGuffey cut, it adds `mcguffey_reader` (2–6) and `lesson`, the lesson numeral as printed. A piece in a lesson of short selections takes that lesson's number.
- **Plan pieces:** a row the plan names carries `named_in_plan`. The Gettysburg Address is hosted from *America First* (1916). Patrick Henry's speech is hosted from McGuffey's Sixth (lesson XIX), which prints Wirt's text; the *American Union Speaker* printing is merged into it. Crispin's Day is not in the pool's rows: the pool's parser missed it. It is cut from *Patriotic Song* (PG #52133, 1901), a pool book, which prints it abridged; the row's notes say so. The Man in the Arena is in none of the pool's books, and Wirt's own *Sketches* (1817) is not in the pool. Both wait for a source.
- **Packs:** one per source book, `declamation-pg<n>.json`. A pack holds the category Monologue. A piece over 400 words is split into parts of whole paragraphs, about 250 words each, broken at sentence ends. The packs live in `exports/mnemonicon/poetry/` beside the poems: `build_poetry.py` owns that folder, and `tests/poetry_test.py` checks every pack in it.
- **Texts:** the texts are kept in `declamations-texts.jsonl`, not in `texts-N.jsonl`. Adding 2.7 MB of prose to the poems' shards would reshuffle every shard.

**Mirror pins.** gutenberg.org cannot be reached from the build machine this layer was made on. So each declamation book is pinned a second time, from its GITenberg copy on GitHub: `sources.json` `books[n].mirror` gives `raw_url`, `sha256` and `encoding`. Those copies are byte for byte the files the pool was parsed from. The copy is fetched to `../corpus/gitenberg/<n>.mirror.txt`, and the row's `pd_source.copy` is `mirror`. The Gutenberg pin is left as it was.

**Partial builds.** `build_poetry.py --layer declamations` builds, checks or writes only that layer's catalog, texts and packs. Use it when the other layers' books are not on disk. A full `build_poetry.py --check` still needs every pinned book.

Order of a rebuild: `build_poetry.py --fetch`, `select_declamations.py --fetch` (fetches and checks the mirror pins), `build_poetry.py`, then `build_poetry.py --check`.
