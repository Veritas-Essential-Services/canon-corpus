<!-- prov: 2026-11-03 claude-opus-5-5 drafted -->
# Page art: draft catalogs

What `pipeline/art_harvest.py` found in the illustrated Gutenberg editions on
the storyteller shelves (2026-11-03): every picture, headpiece, tailpiece,
ornament and decorated initial, in reading order, with where it sits. The plan
behind this, and the rules these drafts will become, are in `docs/ART-PLAN.md`.

**These are drafts.** No uid is minted (that waits for Adam's word, ART-PLAN
section 8). Each `kind` is a guess made by rule. Gutenberg's copies of the art
are reduced, so whether a picture is a full-page plate waits for the scan.

## The numbers (2026-11-03)

53 shelves read, 1,029 Gutenberg books. 510, on 41 of those shelves, have an illustrated HTML edition
(at least 3 pieces), and those hold 17,612 placements:

| kind | placements | where it goes (ART-PLAN s.1) |
|---|---|---|
| picture | 14,098 | Pinacotheca |
| initial | 1,841 | ornament library if drawn; anchor only if Gutenberg sets a plain letter |
| ornament | 782 | ornament library |
| cover | 285 | Pinacotheca (the cover of *that* edition) |
| glyph | 293 | neither: a symbol set in the line (a cattle brand, a nursery-rhyme mark) |
| tailpiece | 258 | ornament library, or Pinacotheca if it shows a scene |
| headpiece | 55 | the same |

334 books keep Gutenberg's printed page numbers, so their pieces have a page.
3,680 pieces have a caption. The other 519 books have no pictures in their
Gutenberg HTML (`_index.json`, `skipped`).

## Files

- `<book-slug>.jsonl`: one row per placement, in reading order.
- `_index.json`: per book, its counts and its **rights** answer; and the books skipped, with the reason.
- `_ornament-candidates.jsonl`: ornaments that may be one block printed in several books (below).

## A row

| field | what it is |
|---|---|
| `citation` | its address: `pg503:images/i012.jpg#2` = the second time that file is placed in ebook 503. A plain letter Gutenberg sets as a drop cap is `pg503:type-initial#4`. Both are facts about the Gutenberg file that no later fix can move |
| `n` | its place in reading order |
| `kind`, `kind_by` | the guess and the rule that made it: `default` (it shows something), `repeat:N` (placed N times in the book), `band` (4x as wide as tall), `small-before-heading`, `tiny` (32 px or less), `alt-letter` (alt text is one letter), `class-or-name`, `class:<css class>`, `label:<word>` (Gutenberg's own alt text says headpiece, tailpiece, ornament...), `name` (the cover) |
| `printed_page` | the page Gutenberg marked last before it, when the edition kept page numbers |
| `heading` | the last heading before it |
| `place` | `in-heading`, `before-heading`, `after-heading`, `paragraph-start` (initials), `end-of-section` (tailpieces), `in-text` |
| `before_quote` | the 70 characters that follow it: how an anchor finds its spot in the house text (ART-PLAN s.3) |
| `caption`, `alt`, `title` | as Gutenberg has them (a placeholder alt like "[Illustration]" is dropped) |
| `letter`, `word`, `html_has_letter` | initials: the letter, the word it opens, and whether Gutenberg's HTML spells that word with it |
| `px`, `sha256`, `dhash` | the Gutenberg copy's pixel size, the first 16 hex of its sha256, and its dHash (a 64-bit sketch of its shape that survives resizing) |
| `src` | the file inside the Gutenberg zip; the image is at `https://www.gutenberg.org/cache/epub/<pg>/<src>` |
| `pd_us` | `true`, or `"check"`: the reason is in `_index.json` |

## Rights (US public domain is the only test)

A Gutenberg file marked COPYRIGHTED is refused. A book is `pd_us: true` when the
shelf dates its edition before 1931 and nothing on the file's title page or
copyright lines is later, or, with no shelf date, when the latest year on those
lines is before 1931. Years in a transcriber's or scanner's note do not count.
**88 books say `check`**: most have no date anywhere in the file; 17 show a
later year on the title page (Potter's *Benjamin Bunny* 1932, Lofting's
*Voyages* 1933, Lang's *Orange Fairy Book* 1937). That year may be only a
reprint of art published earlier, but someone has to read the title page
before any of that art is hosted.

## Initials that lose their letter

**314 picture initials in 27 books**: Gutenberg's HTML text lacks the letter
the picture carries ("nce upon a time", "HE sun had set"). The letter lives in
the picture. The house text is built from Gutenberg's `.txt`, which keeps the
whole word: 67 of 69 on three books checked (Jacobs's *Indian Fairy Tales*,
*Paddy the Beaver*, *Kidnapped*). So nothing is wrong in the corpus today. But
a page rebuilt from the HTML must put the letter back in the text and draw the
picture over it (ART-PLAN s.3a). `html_has_letter: false` marks every case.

## Ornaments shared between books

`_ornament-candidates.jsonl` groups ornaments, tailpieces, headpieces and
picture initials from different books whose dHash differs by 10 bits or less
and whose shape (width to height) agrees within 25%. 14 groups. A look by eye
on 2026-11-03:

- **real:** Pyle's four Arthur volumes share tailpieces and chapter bands
  (groups 1, 2, 6, 14). The Scribner Press colophon appears in six books by
  Barrie, Seton, Stockton and Burnett (groups 4, 5). Both MacGregor volumes
  share one vignette (11), and both Molesworth volumes share one rule (12).
- **not one block:** plain type capitals of one face (3, 7, 8); two different
  triangles of the same layout (13); two different O's (10); a pirate band
  beside some bells (9).

Group numbers change on a rebuild, so this list is a note, not data.

## Rebuild

    python3 pipeline/art_harvest.py --fetch <shelf> ...   # zips to data/corpus/art/pg/ (gitignored), 2 s apart
    python3 pipeline/art_harvest.py <shelf> ...           # these files
    python3 pipeline/art_harvest.py --check <shelf> ...   # byte-identical
    python3 pipeline/art_harvest.py --candidates
    python3 pipeline/art_gallery.py                       # the review page, build/art-gallery/
    python3 tests/art_harvest_test.py                     # 26 offline checks

The 53 shelves of 2026-11-03: potter burgess grahame aesop andersen grimm
jacobs-fairy collodi lofting kate-greenaway ruskin-golden-river
wilde-fairy-tales langloh-parker crane pyle katharine-pyle carroll seton bunyan
henty lang baum nesbit kipling kingsley macdonald barrie alcott stevenson garis
gruelle palmer-cox burnett lfperkins perkins molesworth ewing macgregor baldwin
baldwin-more bulfinch church church-aeneid dodge eggleston guerber
guerber-histories harris-remus hawthorne hawthorne-works eva-march-tappan
stockton arthur-scott-bailey.
