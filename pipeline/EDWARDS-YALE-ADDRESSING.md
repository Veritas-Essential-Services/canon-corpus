---
model_log:
  - 2026-09-27 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
fable_review: pending
---
# Putting Yale numbering on the public-domain Edwards

Goal: every public-domain Edwards passage in the Word Hoard should carry its
Yale address, **WJE vol:page**, the way scholars cite him (e.g. *WJE 2:305*).

This follows the GBWW ruling of 2026-09-07. The Yale edition becomes a
ground truth for ADDRESSING, built as an anchor table. It is not a source of
TEXT. The public-domain text is what we serve, and the Yale page is a label
laid over it.

## Three layers

| layer | what it gives | needs | status |
|---|---|---|---|
| 1. work → Yale volume | "Freedom of the Will is WJE 1" | the Yale volume titles | `edwards_yale_map.json`, candidate |
| 2. public-domain pages | "Dwight 2:95": each IA leaf with its own printed page number | IA's `page_numbers.json` + `djvu.xml` | `edwards_pages.py` → `data/corpus/edwards-pages/` |
| 3. Yale page anchors | "Dwight 2:95 ≈ WJE 1:180" | the Yale text with its page breaks (Adam's Logos) | waiting on the Logos export |

### Layer 2 check

For three Dwight volumes, 1,113 page numbers read from the running heads
agree with IA's table and 73 disagree. The disagreements are OCR misreads of
the running head: 14 for 44, 110 for 116, 106 for 166.

### Layer 3 method

Once the Yale text is exported page by page:

1. Match Yale pages to public-domain pages by shared word sequences (8-word
   shingles), within the work that layer 1 says to search.
2. Keep a match only when it is unique and in order: Yale page n+1 must land
   after Yale page n.
3. Store every match as an **anchor**: {WJE vol:page ↔ PD slug:page, score}.
4. Between anchors, a PD passage takes the Yale page by interpolation, marked
   `honesty: "interpolated"`. At an anchor it is `honesty: "exact"`.

### What Yale numbers that no public-domain edition has

- **The Miscellanies entry numbers (a–1360).** Hickman prints a selection
  without them. They have to be matched by text.
- **Sermons by date.** Yale arranges sermons by date preached (WJE 10, 14,
  17, 19, 22, 25). The public-domain collections rarely date them. The match
  is by text, then the date comes with it.
- **Everything Yale printed for the first time.** That includes most of the
  1,200 sermons and the Blank Bible. There is no public-domain text to label;
  it exists only on the private shelf.

## Rights

The Yale text is copyrighted and lives only on Adam's private shelf, outside
every git repo. Anchors (page-number pairs) are facts about the book, not its
text, and can live with the corpus. That is the same posture as the GBWW
anchor table.
