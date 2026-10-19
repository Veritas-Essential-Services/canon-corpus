<!-- prov: 2026-10-19 claude-opus-5-5 drafted -->
# Brewer's *Character Sketches* — the plates

The full-page pictures in E. Cobham Brewer's *Character Sketches of Romance,
Fiction and the Drama* (the revised American edition, ed. Marion Harland,
Selmar Hess, New York, 1892, 8 volumes), catalogued for the Pinacotheca and for
a later publishing project. Adam, 2026-10-19: link to the pictures, and give
each one a unique uid, "for when we want to build out these books for a later
publishing project".

**Facts and links only.** As with the rest of `data/art/`, no image is stored
here. Each plate links to its page image on the holder's own IIIF server [the
standard libraries use to serve an image at any size]: archive.org, from the
University of Toronto's scans (`charactersketche0Nbrewuoft`, marked
NOT_IN_COPYRIGHT). Published 1892, so US public domain whoever drew it.

## Files

- `plates.jsonl`: **283 plates**, one row each, sorted by volume and leaf.
- `listed-not-found.jsonl`: 31 entries in a volume's own List of Illustrations
  that no found plate could be matched to with confidence. **Some are found
  plates whose OCR titles didn't match** (vols 3 and 5 especially); others are
  missing from the Toronto scan (vol 6's *Pygmalion and Galatea*: its tissue
  guard is scanned, the plate itself is not). The Cornell scans of the 1896
  printing (`cu31924026991xxx`) are the place to fill a real gap.

| Vol | Plates | Notes |
|---|---|---|
| 1 | 42 | |
| 2 | 38 | |
| 3 | 51 | |
| 4 | 21 | |
| 5 | 41 | |
| 6 | 28 | 28 of the 29 listed; the 29th is not in the scan |
| 7 | 39 | this scan has no List of Illustrations, so no list matching |
| 8 | 23 | the list read only partly |

## A row

- `uid`: the plate's identity (`wh-…`), minted once in `data/uids/wordhoard.uids.json` and never changed.
- `citation`: its address, `brewer-sketches:v6.leaf114`, volume plus **scan leaf**. The leaf is a fact about the scan that no later fix can move. A running "plate 12" would renumber every plate after one that a better rule finds.
- `volume`, `leaf`, `tissue_leaf`: where it is. Each plate is bound with a printed tissue guard (caption, artist, engraver, a short passage); `tissue_leaf` is that leaf, or `null` when the plate was found from the list alone.
- `caption_ocr`, `artist_ocr`, `engraver_ocr`: read from the tissue guard's OCR. **Unproofread**: "Dor6" for Doré, "Fiiger" for Füger.
- `plate_title_ocr`: the plate's own printed title, in capitals, when the OCR caught it.
- `list`: the matching entry in the volume's List of Illustrations (`n`, `title`, `artist`, `faces` = the printed page it faces), when one matched. This is the cleanest title and artist available, but still OCR.
- `found_by`: `title` (the leaf's own title matched the tissue caption), `ink` (the strongest-contrast leaf beside the tissue), `list` / `list+ink` (found from the list's facing-page number).
- `px`, `page`, `iiif_canvas`, `iiif_image`: the scan page, and its IIIF image service. A display copy is `{iiif_image}/full/!1280,1280/0/default.jpg`; the full size is `{iiif_image}/full/max/0/default.jpg`.
- `rights`: `pd_us: true` with its basis.

## How it was checked

Every one of the 283 was looked at on contact sheets rendered from the scan
PDFs (2026-10-19). Four pale pages that slipped in on the first run (tissues
and blanks) were removed by a contrast rule: real plates score 51–90 in
grey-level spread, the strays 9–15, and the cutoff is 30. A few landscape
plates are bound sideways (vol 6 leaves 178, 188 and 226, among others):
**rotation is not recorded yet**. Do that in a review pass before printing.

## Rebuild

    python3 pipeline/brewer_plates.py --fetch    # manifests, OCR, PDFs (~190 MB) -> data/corpus/art/ (gitignored)
    python3 pipeline/brewer_plates.py            # -> these files; mints a uid only for a new leaf
    python3 pipeline/brewer_plates.py --check    # mint 0, byte-identical
    python3 tests/brewer_plates_test.py          # offline checks of these files
