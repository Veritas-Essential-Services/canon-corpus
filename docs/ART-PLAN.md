<!-- prov: 2026-10-23 claude-opus-5-5 drafted -->
# Page art: a plan for cataloguing pictures, ornaments and initials

Adam, 2026-10-23: *"I want to have a plan and a storage scheme to save all
illustrations, decorative flourishes and illuminated letters or elements on
the pages. Can we catalog all of these and have anchors in the books for where
they would go if we wanted to reconstruct the book with the remastered
flourishes and ornate first letters of chapters?"* Later the same morning he
added that full-page illustrations go to the Pinacotheca, and asked where the
smaller elements should go.

This is the plan. It is a design only. **No uids have been minted and nothing
has been extracted in bulk.** A worked example on one book is in
`docs/art-plan/example/` (section 7).

---

## 1. The short answer

Every piece of page art gets **one record**, saved as a line of text in this
repo. The record says what the piece is, which scan it came from, which leaf
of that scan, and the exact rectangle on that leaf. That is enough to get the
picture back at any time, because the Internet Archive will cut any rectangle
out of any page on request (section 4).

Records go in one of two places, by a simple test: **does it show something?**

| It is... | It goes to | Examples |
|---|---|---|
| a picture | the **Pinacotheca** (`data/art/`), the picture gallery | full-page plates, frontispieces, pictures in the text, picture headpieces drawn for one chapter, maps |
| decoration | the **ornament library** (`data/art/ornaments/`) | stock headpieces and tailpieces, decorated and pictorial initials, borders, rules, fleurons, printer's devices |

**The book's text is never changed.** Each book gets a small **anchors** file
beside it that says "this piece goes here", so a book can be rebuilt with its
art in place.

**Images are not stored in git.** The repo keeps the records. The pixels live
at the Archive (always recoverable from the record), on your drive as a backup,
and, for your remastered versions, in one storage bucket (section 5).

---

## 2. What a record holds

Each record follows the rule the repo already uses for verses (CLAUDE.md rules
3b and 3c): **one thing gets one identity (a `uid`), and each copy of it is a
witness.**

- The **thing** is the artwork: Pyle's drawing of Uther-Pendragon, or one
  carved headpiece block.
- A **witness** is one printed impression of it: *this* scan, *this* leaf,
  *this* rectangle. The same drawing in a second printing, Gutenberg's copy of
  it, and your remastered version are all witnesses of the same uid.

So a remastered headpiece is not a new item. It is one more witness of the
design, written `wh-XXXXXXXXXX/remaster.1`. That is what lets a rebuilt book
pick the best witness of each piece.

A record (the full shape is in `docs/art-plan/example/`):

| Field | What it is |
|---|---|
| `uid` | the identity, `wh-…`, minted once and never changed |
| `citation` | its address: `art:<scan-id>:leaf23.1`, meaning the first piece on leaf 23 of that scan, top to bottom. A scan leaf is a fact no later fix can move (the Brewer plates rule, `data/art/brewer-sketches/README.md`) |
| `kind` | `plate`, `frontispiece`, `illustration`, `headpiece`, `tailpiece`, `initial`, `vignette`, `border`, `rule`, `fleuron`, `device`, `map`, `title-lettering`, `cover`, `endpaper` |
| `style` | for initials: `plain`, `decorated` (ornament around the letter), `pictorial` (a scene inside it), `historiated` (a scene that tells part of the story) |
| `depicts`, `title`, `artist` | what it shows; the title and artist as printed, with where each came from |
| `witnesses[]` | each impression: `archive_id`, `leaf`, `printed_page`, `box` `[x0, y0, x1, y1]` in the scan's own pixels, `box_by` (how it was measured), and a ready `crop` link |
| `parts[]` | a piece inside a piece, such as the pictorial initial in a plate's hand-lettered title |
| `remasters[]` | your cleaned or redrawn versions: file name, sha256 (a fingerprint of the exact file), who made it, when |
| `rights` | `pd_us` and its basis. **US public domain is the only test** (your rule, 2026-10-10) |
| `review` | what is still unchecked, said plainly (rule 4) |

---

## 3. Anchors: where each piece sits in the book

An anchor is one line in `data/art/anchors/<book-slug>.jsonl`. It says, for
one place in one book, "this piece goes here".

```json
{"book": "pyle-king-arthur", "art": "wh-…", "witness": "storyofkingarthu00pyle.leaf44",
 "place": "before-heading", "before_quote": "Chapter Second. How Arthur Twice Performed",
 "unit": "pyle-king-arthur:ii.2", "offset": 0}
```

(The unit id here is illustrative; it is filled in when the book is built.)

Why a separate file and not a marker typed into the text:

- **Rule 2: never hand-edit a source text.** A marker in the text would also
  break every search, every word count and every comparison of two editions.
- **The book is rebuilt from source.** A marker added to the built book would
  be wiped by the next rebuild. A separate file survives.
- **One text can carry anchors from several printings** without any clash.

How it finds its place: by the unit id (the citation spine of the whole suite)
plus a character offset, **and** by a short quote of the words that follow
(`before_quote`). If a later fix to the converter shifts the text a few
characters, the quote still finds the spot. The build checks every anchor's
quote and reports any it cannot find. An anchor is never silently dropped.

`place` is one of: `before-heading`, `after-paragraph`, `inline`, `initial`,
`tailpiece`, `page` (a full page of its own, sitting between units, never inside
one), `margin`.

**Plain drop capitals get anchors too.** Most books print the first letter of
a chapter as a plain big capital. There is no art to catalogue there, but the
anchor (`"place": "initial", "style": "plain", "lines": 2, "letter": "I"`)
records that a capital goes there. That is exactly where a rebuilt book would
set an ornate one. This answers the "ornate first letters of chapters" part of
your ask, even for books that never had them.

### 3a. Initials: the letter always lives in the text

Adam, 2026-10-25: *catalog the illuminated letters, and replace the decorative
letter with the correct letter in the body's font, "so we don't start every
chapter with a misspelled word."*

**The rule: the text always spells the whole word, in plain letters.** An
initial is art laid over a letter, never a stand-in for one. "IT happened" is
stored as `IT happened`, never `T happened`, and never with a gap or a marker
where the I was. The catalog says that the I is printed as an ornament and
which one. So:

- **A plain text** (search, the reader without art, copy and paste, a screen
  reader) shows the letter in the body's own font. If a styled drop cap is
  wanted, it is the same font made larger, not a picture.
- **A rebuilt book with art** draws the catalogued initial in the letter's
  place and keeps the real letter underneath, hidden from the eye but there
  for search and screen readers. The word is never broken.

**Why this needs a rule: OCR breaks the first word.** A big or decorated
capital is not a letter to the OCR. It drops it (`T happened` for *IT
happened*, `OW it fell` for *NOW it fell*) or reads it as junk (`J-J^ERE` and
`"LJERE` for *HERE*, `C0,` for *SO,*). In *King Arthur*, 8 of the 37 chapter
openings in the Archive's OCR text start with a broken word, and these are
*plain* capitals. Decorated ones fare worse. Every Archive-only book on the
shelves carries this fault today.

**The repair is a per-book rule built from the catalog, never a hand edit
(rule 2).** Each initial's record carries the `letter` it stands for, the
`word` it opens, `ocr_read` (what the OCR made of that word) and
`ocr_status`: `ok`, `initial dropped`, `initial misread`, or `not located`.
When the status is dropped or misread, the build replaces the OCR's broken
word with the catalogued letter plus the rest of the word as the OCR read it,
so the fix reruns on every refetch. Where a second witness exists (Gutenberg,
another scan), it must agree with the repaired word, or the case goes to the
review sheet instead of being fixed.

**Categories** (`style`), from simplest to richest:

| style | what it is |
|---|---|
| `plain` | a large capital in an ordinary typeface, two or more lines deep |
| `swash` / `calligraphic` | an ordinary letter with flourished strokes |
| `decorated` | a letter set in or on an ornament: vine, scroll, pattern, border |
| `factotum` | a printer's ornamental frame with a space, where any type letter is dropped in (the frame is one design, reused with many letters) |
| `inhabited` | a figure or creature sits inside or around the letter, not telling the story |
| `historiated` | the letter holds a scene from the story itself |
| `illuminated` | coloured and gilt, in manuscripts and their facsimiles |

Each initial also records `where` (chapter opening, plate title, title page,
section) and `lines` (how deep it is set). A decorated letter goes to the
ornament library (it may recur). A `plain` initial is an anchor only.

---

## 4. How the art is found

Three sources, from easiest to hardest:

**(a) Gutenberg HTML.** The fetchers download Gutenberg's plain `.txt`, and
`structure_texts.py` scrubs its `[Illustration]` markers, so today **we throw
the positions away**. Gutenberg's HTML edition keeps every picture in place,
marks drop caps, and keeps the printed page numbers (`{21}`). One pass over
the HTML gives a full anchor list for a book, with printed pages. The
Archive's `page_numbers.json` then turns each printed page into a scan leaf.
That step was tested on *King Arthur* (section 7): Gutenberg says where, and
the scan gives the art at full size.

**(b) Internet Archive scans.** Every item has full-size page images and the
OCR's word boxes (`_hocr.html`, fetched one page at a time). The Unscanner
already finds pictures as "ink no word accounts for" (`unscanner/images.py`)
and draws a rectangle round each one. Today it drops them from the corpus
units. It only needs to write them out as records too.

**(c) Your own PDFs** (Brewer's, the Church Homers): the same route as (b),
run on your PC.

Whatever the source, the **kind** is first guessed by rule (full page = plate,
a wide band before a heading = headpiece, a small block after a chapter's last
line = tailpiece, a square at a paragraph's start = initial). Then it goes on a
review sheet, the way the hymns did (`pipeline/review.py`): a contact sheet of
crops, and you confirm or correct.

**Finding repeated ornaments across books.** Each ornament crop gets a
"perceptual hash", a short fingerprint of what it looks like that survives
small differences in printing and scanning. Two crops with nearly the same
fingerprint are probably the same block. The script proposes "this is the
same headpiece as that one" and you confirm. A confirmed match becomes a
second witness of the existing design, not a new record.

---

## 5. Where the image files live

Three kinds of image, three answers:

| Image | Home | Why |
|---|---|---|
| **Original crops from Archive scans** | **Nowhere new.** The record's `crop` link *is* the image | The Archive's IIIF server (the standard libraries use to serve any part of a page at any size) cuts it on request: `…/<x>,<y>,<w>,<h>/max/0/default.jpg`. Tested; the crop links in the example open |
| **Backup copies of those crops** | **Your drive**, by a download script like `pipeline/download_illustrations.py` | A library can go down or move. Each saved file's sha256 goes in the record, so any copy can be checked |
| **Your remastered versions** | **One storage bucket**, files named `<uid>.<n>.<ext>`, plus your drive | These are new work that exists nowhere else, so they need a real home with backups. Git keeps the record and the sha256, not the file |

**Why not keep the images in git?** One full-size plate from this scan is about
0.6 MB. *King Arthur* alone has about 50 distinct pictures, so about 30 MB of crops.
A thousand illustrated books would be about 30 GB. The whole repo today is
66 MB. Git keeps every version of every file forever, so a picture added and
later replaced still costs space in every copy of the repo, on every machine
and every thread, permanently.

**Why not Git LFS?** LFS ("large file storage") keeps big files outside the
normal history and leaves a pointer behind. It works, but GitHub charges for
LFS storage and for every download past a small free allowance, and this repo
is public, so anyone's clone draws on it. It also makes every fresh clone more
fiddly. For files we can always fetch again from the Archive, it buys nothing.
(Check GitHub's current LFS prices before relying on this paragraph; I did not
look them up today.)

**Which bucket** is your call (section 8). Any plain object store works, since
files are named by uid and checked by sha256. Moving to another store later
just means copying the files.

**Small remasters may be the exception.** A redrawn initial as a vector file
(SVG) is often 20 to 100 KB and is really a drawing written in text. If you
remaster in vector, those could live in git under `data/art/remasters/`. Decide
when the first ones exist.

---

## 6. Layout in the repo

```
data/art/
  catalog.json                    the existing illustrator catalog (unchanged)
  brewer-sketches/plates.jsonl    the existing Brewer plates (unchanged)
  books/<book-slug>.jsonl         Pinacotheca: the pictures from one book, one per line
  ornaments/ornaments.jsonl       the ornament library: one design per line, all its witnesses
  anchors/<book-slug>.jsonl       where each piece sits in that book's text
  README.md                       extended with these rules
```

Brewer's 283 plates already follow most of this (uid, scan, leaf, IIIF link).
They would gain `box` and anchors. Their uids stay as they are.

---

## 7. The worked example: Pyle, *The Story of King Arthur and His Knights* (1903)

Chosen because it is on Lane D's `pyle` shelf (Gutenberg 60184), it is full of
art, and the Archive holds a good scan of the first edition
(`storyofkingarthu00pyle`, New York Public Library copy, NOT_IN_COPYRIGHT;
published 1903, so US public domain).

Files in `docs/art-plan/example/` (examples, **not** catalog data; the uids
read `PILOT-not-minted-n`):

- `pinacotheca.jsonl`: the frontispiece *Uther-Pendragon* (leaf 23), with the
  pictorial initial **U** of its hand-lettered title recorded as a part of it,
  and the Prologue's picture headpiece (leaf 24).
- `ornaments.jsonl`: one stock headpiece (a band of vine with two roundels) and
  its eight placements in the book.
- `anchors.jsonl`: five anchors, including two plain drop capitals.
- `initials.jsonl` (2026-10-25): **all 65 initials in the book.** These are the
  37 chapter-opening capitals (each with its printed page, scan leaf, the word
  it opens, and what the OCR read) and the 28 pictorial initials in the plate
  titles (each tied to its plate). Every plate was found in the scan, and
  every plate-title initial was looked at on a contact sheet.

Every rectangle with a `box` was measured from the ink and checked by eye on
the scan. Each `crop` link opens straight to that piece at full size.

What the example turned up:

1. **Gutenberg HTML is a ready-made anchor list.** One pass found 92 pictures
   and 37 drop caps, each with its printed page, in order. Printed page to
   scan leaf worked through the Archive's page table (page 21 is leaf 44).
2. **Ornaments really do repeat.** Four ornaments account for 36 of the 92
   pictures in this one book: the roundel headpiece 8 times, another headpiece
   8, a third 6, and a tailpiece 14. In an ornament library they are four
   records, not 36.
3. **Two witnesses can disagree, and the record must say so.** Gutenberg puts
   the roundel headpiece before Chapter Sixth (printed page 139). The NYPL
   scan has no headpiece on that page. That is recorded as `ABSENT in this
   scan`, and neither copy is "corrected".
4. **Not every book has ornate initials.** Pyle's chapter openings are plain
   two-line capitals, in print as well as in Gutenberg. His pictorial initials
   are in the hand-lettered plate titles. The plain ones still get anchors
   (section 3).
5. **The OCR breaks one chapter opening in five.** In the Archive's text, 8 of
   the 37 chapter openings start with a broken word: *HERE* read five times as
   `J-J^ERE`, `TJERE` or `"LJERE`, *IT* as `T`, *NOW* as `OW`, *SO* as `C0`.
   Four more could not be located automatically and are marked for checking.
   The catalog's `repair` field holds the fix for each (section 3a). For this
   book the house text comes from Gutenberg, which spells them all correctly.
   But every Archive-only book has the same fault, and this is how it gets
   fixed.
6. **The plate-title initials are all inhabited.** All 28 have a figure or a
   creature inside a framed letter. Most are T's and S's (*The…*, *Sir…*).
   Their subjects are not yet described.

---

## 8. Decisions for you

1. **Go ahead with the scheme?** Two places by the "does it show something?"
   test, records in git, images out of git, anchors beside the text.
2. **Pilot for real on *King Arthur*?** Mint uids for its pictures and
   ornaments (about 60 distinct pieces, placed about 130 times), write its anchors, make a review sheet, and
   build one chapter as HTML with the art restored from the crop links, so you
   can see a rebuilt page. Nothing else gets touched.
3. **Which storage bucket for remasters?** Not needed until the first remaster
   exists. If the Armarium already runs on Supabase, its Storage is the
   simplest. Otherwise Cloudflare R2, which does not charge for downloads.
   Your drive is the backup either way.
4. **Bulk runs, later and only with your yes.** The likely order is the
   illustrated storytellers first (Pyle, Lang's fairy books, Crane, Rackham's
   and Dulac's books), then the Gutenberg HTML harvest across every shelf, then
   Archive-only scans through the Unscanner. Theology scans have little art, so
   they come last.

## 9. Next steps once approved

- `pipeline/art_harvest_gutenberg.py`: Gutenberg HTML to draft records and
  anchors, with printed page to leaf through `page_numbers.json`.
- Unscanner: write its found pictures out as records (`--to-art`).
- `pipeline/art_check.py --check`: every anchor's quote found, every witness's
  box inside its page, every `pd_us` true, a rebuild mints 0 (the house gate).
- A review sheet per book, the way the hymn sheets work.
- Extend `data/art/README.md` with these rules once they are settled.
