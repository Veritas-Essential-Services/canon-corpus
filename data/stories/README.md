# Stories: the scene and figure layer of the Illustrated Classics

Adam's ruling (2026-10-23): tag a picture to the **story, scene and figures** it shows, never to a book's pages. Then one Minotaur picture serves Bulfinch, Hawthorne and Ovid alike, and a Wyeth plate of Silver can sit in any edition of *Treasure Island*.

Each story has its own folder:

| File | What it holds |
|---|---|
| `story.json` | the settings, and for each **telling** (an edition's text) its chapter table: title, paragraph count, first house unit id |
| `figures.jsonl` | who appears. `looks` lists what the text says each figure looks like, in the house's own words, cited by chapter and paragraph. This is the brief for keeping a character consistent across artists |
| `scenes.jsonl` | what happens, in the house's own words, pinned to a paragraph: `at` is the unit id from `structure_texts.py`, and `chapter`/`para` count within the author's chapters |

**No book text is stored here.** Titles and looks are paraphrase; anchors are ids and counts.

The jsonl files are hand-edited sources. `python3 pipeline/build_stories.py` adds a uid to any new row (citations `story-<id>:story`, `story-<id>:figure.<id>`, `story-<id>:scene.<id>`) and checks every reference; `--check` must mint 0. Don't rename a scene id: that would mint a new uid. Change the title instead.

Pictures live beside the other art in `data/art/illustrated-classics/<story>/`: `editions.json` (every illustrated edition, with its rights answer and role: anchor, fill or hold), and the plate and ornament catalogue to come.

## Treasure Island (2026-10-23)

- **Chapters:** 34, from the house text (`treasure_island`, Project Gutenberg #120, 1,424 units).
- **Scenes:** 55. Not every paragraph has a scene: a scene is a moment an illustrator has drawn, or could draw.
- **Figures:** 20, with looks cited for the eight whom Stevenson describes.
- **House units:** they run by PART, not by chapter (`treasure_island:PART_ONE--The_Old_Buccaneer.2`). This is because the converter's chapter pattern doesn't match this file's roman-numeral headings. The chapter table bridges the two.
