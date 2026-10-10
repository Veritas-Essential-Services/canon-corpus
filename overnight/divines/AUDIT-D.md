# Lane D — §5 quality audit (2026-10-02, relay 5)

Scope: all 29 Lane D shelves, 497 sources (443 converted Gutenberg/CCEL books,
54 raw Internet Archive OCR volumes). Three checks the relay named, plus the
standing URL and map checks. The method is stated for each check, so a number
here can be re-run rather than trusted. Nothing was minted and no book text is
committed; the audit scripts were scratch and are not in the repo.

## 0. URLs and map

- All 497 source URLs answer. Four failed on the first pass (a 500 from
  archive.org, two connection resets and a TLS EOF from Gutenberg) and all
  four answered on retry.
- Every slug on every Lane D shelf appears in `docs/divines-map/D-storytellers.md`.

## 1. Duplicates across shelves

**Same source twice: none.** No Gutenberg number, IA identifier or CCEL id is
held twice anywhere in `pipeline/*_shelf.json` (all 154 shelves, every lane)
or in the house manifests in `fetch_sources.py` (GUTENBERG_EXTRA,
CHESTERTON_GUTENBERG, CCEL). The title collisions the check found are all
volumes of one multi-volume set (Lang's History of Scotland, Stevenson's
Letters, and so on).

**Same text in two volumes.** This was measured on the text itself, not the
titles: every paragraph of 160 or more letters in the 443 converted books was
hashed, and the pairs of books that share 5 or more identical paragraphs were
counted. Each such pair is a reprint or a collection that contains an earlier
book. All of them are deliberate holdings of distinct published volumes, so
nothing is wrong. But a uid-minting pass must not mint the shared passages
twice: they are one passage with two witnesses (rule 3c). The larger cases
are listed below; "x% of A" is the share of A's long paragraphs that also
appear in B.

| Book A | Contained in B | Shared | Note |
|---|---|---|---|
| `barrie-peter-pan-in-kensington-gardens` | `barrie-little-white-bird` | 89% of A | Kensington Gardens is chapters 13-18 of The Little White Bird |
| `stevenson-father-damien` | `stevenson-lay-morals` | 75% of A | the Lay Morals volume reprints the Damien letter |
| `macdonald-light-princess` (CCEL) | `macdonald-light-princess-other-stories` | 72% of A | |
| `carroll-hunting-of-the-snark` | `carroll-rhyme-and-reason` | 71% of A | Rhyme? and Reason? reprints the Snark and most of Phantasmagoria (47%) |
| `lang-ballades-blue-china` | `lang-ballades-verses-vain` | 65% of A | the American selection reprints the English book |
| `macdonald-day-boy-night-girl` (CCEL) | `macdonald-stephen-archer` | 62% of A | |
| `kingsley-sanitary-and-social-lectures-and-essays` | `kingsley-health-and-education` | 49% of A | Kingsley's collected lectures overlap pairwise, 9-42% |
| `lang-custom-and-myth` | `lang-custom-and-myth-new-ed` | 43% of each | two editions of one book |
| `lamb-adventures-of-ulysses`, `lamb-tales-from-shakespeare` | `lamb-works-lucas-books-for-children` | 42%, 39% of A | Lucas's collected edition reprints both |
| `lang-tales-of-romance` | `lang-book-of-romance` | 32% of A | |
| `pyle-stolen-treasure` | `pyle-book-of-pirates` | 28% of A | |
| `macdonald-adela-cathcart-1..3` | `macdonald-portent`, `-light-princess*`, `-cross-purposes-shadows` | 7-34% | the stories told inside Adela Cathcart were later published on their own |
| `bulfinch-age-of-fable`, `-age-of-chivalry`, `-legends-of-charlemagne` | each other | 6-8% | shared front matter and index |

**Across Lane D's shelves**, the overlaps are tale-level and small. Lang's
colour fairy books reprint other translators' versions.
- `lang-red-fairy-book` shares 41 paragraphs with `ralston-russian-fairy-tales`
  (5% of Ralston). Lang took Ralston's translations.
- `lang-blue-fairy-book` shares 16 paragraphs with `perrault-fairy-tales-samber-mansion`
  (Samber's Perrault).
- `jacobs-english-fairy-tales` shares 7 paragraphs with `lang-green-fairy-book`.

These are the same witnesses of the same tales. A minting pass should treat
them as one passage each.

**Raw OCR volumes that duplicate a converted book.** Fifteen hundred random
8-word phrases were sampled from each IA volume and looked up in all 443
converted books. OCR errors break phrases, so about 50% here means most of the
volume.
- `macdonald-threefold-cord`: 72% found in `macdonald-poetical-works-2`.
- `lang-story-of-the-golden-fleece`: 65% in `lang-tales-of-troy-and-greece`.
- `lang-new-and-old-letters-dead-authors`: 61% in `lang-letters-to-dead-authors`.
  This is the enlarged edition.
- `grimm-hunt-1884-01` and `-02`: 54% and 49% in `grimm-hunt-household-tales`.
  **This is the one real duplicate.** It is the same Hunt translation twice:
  once as clean Gutenberg text, once as raw OCR. What the IA set adds is Lang's
  introduction and Grimm's notes.
- `macdonald-dealings-with-the-fairies`: 49% in `-light-princess-other-stories`.
- `macdonald-scotch-songs-ballads`: 46% in `-poetical-works-2`.
- `lang-poetical-works-04`: 45% in `lang-helen-of-troy`.
- `lang-origins-of-religion`: 35% in `lang-custom-and-myth*`.
- `andersen-stories-household-dulcken`: 28% in `andersen-what-the-moon-saw-dulcken`.
  This is the same translator, Dulcken.

## 2. OCR quality, per raw volume

The method has two measures, scored per volume.

- **Word hit.** This is the share of the volume's alphabetic words that are
  real words. A word counts as real if it occurs at least 3 times in the 443
  clean converted books, which gives a 72,112-word vocabulary.
- **Fused tokens.** This is the share of tokens where letters are fused with
  digits or symbols (`tlie`, `wor1d`, `pp.12a`).

Grades:

| Grade | Word hit | Fused tokens |
|---|---|---|
| A | 95% or more | under 2% |
| B | 92% to 95%, or 95% and up with 2% or more fused | any |
| C | 85% to 92% | any |
| D | under 85% | any |

This is a coarse screen. It catches a bad scan. It does not prove a good one,
because names, archaic spellings and verse all lower the hit rate without
being errors.

**Result:** 43 A and 11 B, with no C or D. Every raw volume is readable OCR. The
B grades come from three causes:
- Verse and songs: Lang's Poetical Works, Scotch Songs, Lays and Legends.
- Running heads and page numbers fused into words: Lucas's Dramatic Specimens,
  Lofting's Caravan.
- Short picture books, where captions weigh heavily: Pigling Bland, and
  Beauty and the Beast.

The lowest-scoring volume is `macdonald-scotch-songs-ballads` (93.1%, in
Scots).

| Grade | Volume | Shelf | Size | Word hit | Fused tokens | Text also held as |
|---|---|---|---|---|---|---|
| A | `lang-miracles-st-katherine` | lang | 93 KB | 95.0% | 0.9% | — |
| A | `lang-origins-of-religion` | lang | 463 KB | 96.4% | 1.6% | `lang-custom-and-myth-new-ed` (36%); `lang-custom-and-myth` (35%) |
| A | `lang-st-andrews` | lang | 623 KB | 96.5% | 1.6% | — |
| A | `lang-politics-of-aristotle-essays` | lang | 200 KB | 96.5% | 1.4% | — |
| A | `lang-homer-and-the-epic` | lang | 996 KB | 96.8% | 1.7% | — |
| A | `lang-portraits-jewels-mary-stuart` | lang | 168 KB | 97.2% | 1.2% | — |
| A | `grimm-hunt-1884-02` | grimm | 1,742 KB | 97.3% | 1.6% | `grimm-hunt-household-tales` (49%) |
| A | `lang-devil-dancers` | lang | 175 KB | 97.5% | 1.6% | — |
| A | `lang-northcote-02` | lang | 704 KB | 97.7% | 1.3% | — |
| A | `lang-history-scotland-01` | lang | 1,558 KB | 97.9% | 1.4% | — |
| A | `lang-prince-charles-edward` | lang | 965 KB | 97.9% | 1.7% | — |
| A | `lang-dead-leman` | lang | 321 KB | 97.9% | 1.3% | — |
| A | `andersen-improvisatore-howitt` | andersen | 865 KB | 98.0% | 1.2% | — |
| A | `chesterton-generally-speaking` | chesterton-gaps | 446 KB | 98.0% | 0.7% | — |
| A | `lang-northcote-01` | lang | 710 KB | 98.1% | 1.1% | — |
| A | `lang-sir-george-mackenzie` | lang | 849 KB | 98.1% | 1.3% | — |
| A | `andersen-danish-fairy-legends-peachey` | andersen | 1,114 KB | 98.1% | 1.7% | — |
| A | `chesterton-return-of-don-quixote` | chesterton-gaps | 484 KB | 98.1% | 1.6% | — |
| A | `lang-history-scotland-04` | lang | 1,894 KB | 98.2% | 1.4% | — |
| A | `lang-king-over-the-water` | lang | 1,359 KB | 98.2% | 1.6% | — |
| A | `lang-new-and-old-letters-dead-authors` | lang | 313 KB | 98.2% | 0.9% | `lang-letters-to-dead-authors` (61%) |
| A | `grimm-hunt-1884-01` | grimm | 1,384 KB | 98.2% | 1.5% | `grimm-hunt-household-tales` (54%) |
| A | `chesterton-outline-of-sanity` | chesterton-gaps | 411 KB | 98.2% | 0.5% | — |
| A | `lang-lockhart-01` | lang | 706 KB | 98.3% | 1.6% | — |
| A | `lang-maid-of-france` | lang | 961 KB | 98.3% | 1.1% | — |
| A | `potter-little-pig-robinson` | potter | 66 KB | 98.3% | 1.5% | — |
| A | `lang-lockhart-02` | lang | 773 KB | 98.4% | 1.8% | — |
| A | `andersen-picture-book-without-pictures` | andersen | 171 KB | 98.4% | 1.7% | — |
| A | `chesterton-incredulity-of-father-brown` | chesterton-gaps | 468 KB | 98.5% | 1.9% | — |
| A | `lang-history-scotland-02` | lang | 1,690 KB | 98.6% | 1.3% | — |
| A | `chesterton-robert-louis-stevenson` | chesterton-gaps | 286 KB | 98.7% | 0.6% | — |
| A | `lang-history-scotland-03` | lang | 1,216 KB | 98.8% | 1.1% | — |
| A | `macdonald-dealings-with-the-fairies` | macdonald | 330 KB | 98.8% | 1.6% | `macdonald-light-princess-other-stories` (49%); `macdonald-cross-purposes-shadows` (26%) |
| A | `andersen-fairy-tales-braekstad` | andersen | 950 KB | 98.8% | 1.4% | — |
| A | `lang-book-of-saints-and-heroes` | lang | 657 KB | 98.9% | 0.7% | — |
| A | `lang-red-book-of-animal-stories` | lang | 626 KB | 98.9% | 0.9% | — |
| A | `lang-all-sorts-of-stories-book` | lang | 684 KB | 99.0% | 1.0% | — |
| A | `andersen-stories-household-dulcken` | andersen | 2,770 KB | 99.2% | 1.2% | `andersen-what-the-moon-saw-dulcken` (28%); `andersen-fairy-tales-paull` (20%) |
| A | `macdonald-threefold-cord` | macdonald | 243 KB | 99.3% | 1.8% | `macdonald-poetical-works-2` (72%); `macdonald-robert-falconer` (6%) |
| A | `lang-story-of-the-golden-fleece` | lang | 58 KB | 99.4% | 0.8% | `lang-tales-of-troy-and-greece` (65%) |
| A | `andersen-faery-tales-lucas` | andersen | 950 KB | 99.6% | 1.3% | — |
| A | `collodi-pinocchio-murray` | collodi | 288 KB | 99.6% | 0.9% | — |
| A | `andersen-fairy-tales-craigie` | andersen | 2,700 KB | 99.7% | 1.4% | `andersen-what-the-moon-saw-dulcken` (26%); `andersen-fairy-tales-paull` (13%) |
| B | `macdonald-scotch-songs-ballads` | macdonald | 80 KB | 93.1% | 4.8% | `macdonald-poetical-works-2` (46%) |
| B | `potter-pigling-bland` | potter | 26 KB | 95.6% | 2.5% | — |
| B | `nesbit-lays-and-legends-1` | nesbit | 196 KB | 96.5% | 3.3% | — |
| B | `lang-poetical-works-02` | lang | 168 KB | 97.6% | 2.3% | `lang-ballads-lyrics-old-france` (21%); `lang-ballades-verses-vain` (18%) |
| B | `lang-poetical-works-04` | lang | 192 KB | 97.7% | 2.9% | `lang-helen-of-troy` (45%) |
| B | `lamb-works-lucas-dramatic-specimens` | lamb | 1,432 KB | 97.8% | 3.0% | — |
| B | `pyle-garden-behind-the-moon` | pyle | 171 KB | 97.8% | 2.0% | — |
| B | `lamb-beauty-and-the-beast` | lamb | 54 KB | 98.2% | 3.9% | — |
| B | `lang-poetical-works-03` | lang | 174 KB | 98.4% | 2.0% | `lang-rhymes-a-la-mode` (11%); `lang-ballads-lyrics-old-france` (11%) |
| B | `lofting-doctor-dolittles-caravan` | lofting | 350 KB | 98.4% | 3.1% | — |
| B | `lang-poetical-works-01` | lang | 170 KB | 98.8% | 2.3% | `lang-ballades-verses-vain` (22%); `lang-ballades-blue-china` (15%) |

## 3. Translator credits

**Method.**
- Every Gutenberg row was checked against Gutenberg's own catalogue
  (`pg_catalog.csv`, its `[Translator]` roles) and against the `Translator:`
  line captured from each file's header at fetch.
- A row was flagged if a translator is named there but not in the row's title.
- A row was also flagged if the book's main author is not the shelf's author.
- Every IA title was read by hand.
- No Lane D book carries Gutenberg's COPYRIGHTED marker.

**Fixed now: `macdonald-for-the-right` (PG 36904) was not MacDonald's book.**
- It is *For the Right*, a novel by Karl Emil Franzos, translated by Julie
  Sutter.
- MacDonald wrote only its preface.
- It sat on the MacDonald shelf, with no translator recorded, from when the shelf was built
  until this audit.
- It is removed to `_excluded` (`macdonald-introduction-only`), and the map
  row now reads "not taken".

**For Adam: five Andersen translations name no translator.** These Andersen
rows say so in their titles, but they entered the shelf anyway. That is looser
than the rule since applied to Collodi (PG 16865) and Perrault (PG 33511),
which were held back for the same gap.
- `andersen-fairy-tales-paull` (PG 27200). The wording matches Mrs H. B.
  Paull's, but this is unverified.
- `andersen-christmas-greeting` (PG 31103).
- `andersen-o-t` (PG 7513).
- `andersen-pictures-of-sweden` (PG 12313).
- `andersen-picture-book-without-pictures` (IA). IA credits Mary Howitt, but
  this is unverified.

All five are 19th-century translations, and US public domain whoever made
them. But the 2026-07-26 rule says a translation enters a shelf only with its
translator recorded. **Your call:**
- (a) Hold the five back, like Collodi and Perrault.
- (b) Keep them, with the gap stated, as now.
- (c) Someone identifies each translator from the printed edition.

Recommended: (a) until (c) is done. Nothing was removed: they were admitted on
an earlier relay and are already listed for your veto.

**Clean otherwise.** Every other translated book names its translator in its
title. That covers the Grimm (Hunt), Andersen (Dulcken,
Craigie, Peachey, Brækstad, Lucas, Howitt), Collodi, Perrault, Dasent and
Ralston rows, and Lang's own translations (Homer, Theocritus, The Dead Leman,
Saint Katherine). The rows whose main author differs from the shelf author are
all co-written books, and their titles say so:
- Lang with Haggard, Mason, Pollock and Kendall.
- Stevenson with Osbourne and Henley.
- Nesbit with Bland and Brooke.

There is one edited text: MacDonald's Hamlet, the Folio text with his study.

## 4. Second pass (2026-10-02 evening, after Lane D's own batches 7 and 8)

Rerun of §0-§3 over all 55 Lane D shelves (598 slugs), including the twenty added under the standing relay.

- **URLs.** 598 checked: 594 answered first time. Three Gutenberg files reset the connection and all three answered on retry (PG 5654, 137, 2788). One Internet Archive file, `lifelettersofjoh01langiala_djvu.txt` (Lang's Lockhart, vol. 1), returns HTTP 500 three times running although the item's metadata still lists it; vol. 2 answers. This looks like an Archive storage node being down, not a missing file, and the local copy fetched on the second run is intact. Recheck before relying on a refetch. Every slug is in the map.
- **Same source held twice.** None.
- **Text held twice, new this pass.** One case, settled before commit: Ewing's *The Brownies and Other Tales* (PG 16052) and *The Land of Lost Toys* (PG 33880) measured 84% and 93% contained in *Lob Lie-by-the-Fire, The Brownies and Other Tales* (PG 62783). Only PG 62783 is held, and the other two are in `ewing_shelf.json` `_excluded` with the figures. Other new overlaps are small borrowings between collectors, which is expected: Jacobs's *Celtic Fairy Tales* draws on Hyde and on Yeats's anthology (17 and 31 paragraphs), Jacobs's *Indian Fairy Tales* draws on Steel's *Tales of the Punjab* (24), and Steel's *English Fairy Tales* retells Jacobs (32 + 11). Mint those passages once with two witnesses, as in §1. *Sara Crewe* (1888) and *A Little Princess* (1905) share only 23 paragraphs, because Burnett rewrote the story, so they are two works.
- **Translators.** Every translated row in batches 7-8 names its translator in the title, and the catalog agrees. The rows are Spyri (Edwards, Stork, Dole, Brooks), Wyss (Kingston), Ozaki, Mitford, Crane, Hyde and Gregory. The catalog check (`TR-NOT-IN-TITLE`) is empty for all 55 shelves. One `COPYRIGHTED` header was found and kept out: PG 3836 *Swiss Family Robinson*.
- **OCR.** 63 raw volumes graded: 46 A, 12 B, 3 C, 1 D. The new C is Hyde's *Beside the Fire* (0.917). Its Irish texts were printed in Gaelic type, which the Archive OCR turns into strings like `pijín 1 muic, nÁ b]\oc`. The English pages read cleanly. The Irish is unusable as OCR and would need re-OCR with an Irish model or a clean source. Campbell vols. 1-3 (C, D, C) fall for the same reason, the facing Gaelic, and his English was spot-checked as readable.

## 5. Third pass (2026-10-02 late evening, after batches 9 and 10)

All 80 shelves (652 slugs).

- **URLs.** Every URL was checked. On the first sweep, 16 calls failed with connection resets or TLS hiccups. Every one answered on retry except Lang's Lockhart vol. 1 on the Internet Archive, which still returns HTTP 500 (see §4).
- **Same source held twice.** None.
- **Translators.** The catalog check is clean. Every translated row on the new shelves names its translator in the title, and the catalog agrees: Bain, Giles, Mijatovich, Bleek, Webster, Thorpe and Blackwell, Magnússon and Morris, and Kirby.
- **Text held twice, new this pass:**
  - *Mijatovich, Serbian Fairy Tales* (1918) is 91% contained in her *Serbian Folk-lore*. Only the larger book is held, and the other is excluded with the figure.
  - *Petrovitch* shares about 200 paragraphs (13%) with Mijatovich. Mint those once.
  - Church's *Stories from Virgil* is 42% the same text as his *Stories of the Old World*, which reuses it. Both are held, as two witnesses.
  - Guerber's *Myths of Northern Lands* and *Myths of the Norsemen* share about 12%. The later book reworks the earlier one. Both are held.
- **OCR.** The Golden Legend's seven volumes all grade A (0.974-0.985), even with Caxton's spelling. The totals are now 53 A, 12 B, 3 C and 1 D.
- **Editions.** Wherever a title gives a year, it was checked against the fetched text's title page or Gutenberg header. Where the text is a later printing, the title says so: Frere 1870, Mijatovich 2nd ed. 1899, Webster 2nd ed. 1879, Crooke 1922 reprint, Kúnos/Bain 1901, Church's Iliad 1920, Milne's *Once on a Time* 1922. Where the text carries no date (Grace James, Petrovitch, Zitkala-Ša, Bain's Cossack tales), the title gives none.

## 6. Fourth pass (2026-10-02 night, after batches 11 and 12)

All 97 shelves (719 slugs).

- **URLs.** 719 checked. Five Gutenberg files reset the connection or dropped TLS on the first sweep (PG 28804, 45264, 14814, 78504, 13015), and all five answered on retry. Lang's Lockhart vol. 1 on the Internet Archive still returns HTTP 500 (see §4). Every slug is in the map.
- **Same source held twice: one, now settled.** Lane D's `giles-liaozhai` shelf and Lane C's Giles translator shelf (`giles_shelf.json`, row `giles-strange-stories`) both held PG 43629, Giles's *Strange Stories from a Chinese Studio*. Both were added within minutes of each other on the night of 2026-10-02/03, and Lane C queued it first. Lane D's row moved to `_excluded` with a pointer to Lane C's row. Lane D's heading rules for the book (story numbers as headings, the footnotes kept under each story) are copied into that note in case Lane C's row wants them. The shelf file keeps only the exclusions and can be deleted if you prefer. Minting total drops by one, to 719.
- **Translators.** The catalog check is clean. The one translation in batch 12 is Weston's (Wolfram's *Parzival*, the Marie de France lais), and her name is in the titles. The other batch-12 books are retellings (Baldwin, Macgregor, Gilbert, Knowles, Rolleston, Hull), and the catalog lists the reteller as author. Knowles's *Legends of King Arthur* is catalogued with Malory as co-author because it retells him, but its text is Knowles's own, and it shares no measured paragraph with the Malory shelf.
- **Text held twice, new this pass:**
  - Craik's *Little Lame Prince* (PG file) shares 190 long paragraphs with her *Fairy Book*. The Gutenberg file bundles fairy tales from the *Fairy Book* (Prince Leander and others) after the title story. Both are held: mint the shared tales once, with two witnesses.
  - Stockton's *Fanciful Tales* (1922) reprints stories from *The Bee-Man of Orn* (101 paragraphs; already noted in the DIGEST).
  - Baldwin's *Hero Tales* draws on his own *Story of Siegfried* (43 paragraphs) and *Story of the Golden Age* (30). Mint those once.
  - Rolleston's two Celtic books share 12 paragraphs. That is too small to matter, but they should still be minted once.
- **OCR.** Batches 11 and 12 added no Internet Archive volumes, so the grades are unchanged: 53 A, 12 B, 3 C, 1 D.

## 7. Fifth pass (2026-10-02 night, after batches 13-15 and the shelf-ownership fix)

All 115 shelves (779 slugs).

- **Shelf ownership.** Lane D had written over Lane A's `perkins_shelf.json` (William Perkins) with Lucy Fitch Perkins. Lane A's file is restored byte for byte, and the Twins books moved to `lfperkins_shelf.json` (8c69ae2). Every other Lane D shelf file was created by a Lane D commit, and no other lane's commit touches one. `overnight/divines/precommit-D.py` now refuses a commit that changes another lane's shelf.
- **Identity and rights checks recorded.** Every Lane D shelf with rows now carries `_surname` and the `_checks` that `fetch_shelf.py --verify --record` writes (88bc65a, 1015c74, and batch 15's own commits). The final result is 0 identity mismatches and 0 rights flags. The first pass's 7 mismatches and 6 flags are explained in 1015c74. Three were co-translations, where the claim named a different one of the two translators than Gutenberg's header does. Four were raw-OCR title pages that garble the translator's name and were confirmed by reading them. MacDonald's scans print "MAC DONALD". Dutt's Ramayana scan has an undated Archive record, and its title page reads 1899.
- **URLs.** 779 checked. Eight Gutenberg files reset or dropped TLS on the first sweep, and all eight answered on retry; PG 496 took four tries. Lang's Lockhart vol. 1 still returns HTTP 500 (see §4). Every slug is in the map.
- **Same source held twice.** None.
- **Translators.** The catalog check is clean. Kulóskap the Master was published by Leland *and* John Dyneley Prince (title page, 1902), and the row now names both.
- **Text held twice, new this pass.** Mint each of these once, with two witnesses:
  - Richards's *The Pig Brother* (a school reader) reprints 56% of its long paragraphs from her other books held here: Toto, Toto's Merry Winter, Five Minute Stories and The Silver Crown.
  - Schoolcraft's *Myth of Hiawatha* (1856) reprints 46% of its long paragraphs from his *Algic Researches* (1839).
  - Croker's *Fairy Legends* shares 14% with Yeats's *Fairy and Folk Tales of the Irish Peasantry* and 12% of Yeats's *Irish Fairy Tales*, because Yeats reprinted Croker.
  - Lady Wilde shares small amounts with Yeats for the same reason.
- **Excluded before commit** (measured, not guessed): Richards's *Golden-Breasted Kootoo* (72% of it is in *Toto*), and Perkins's *Moon Princess* (written by Edith Ogden Harrison; Perkins only illustrated it).
- **OCR.** Batches 13-15 added no Internet Archive volumes, so the grades are unchanged.

## 8. Sixth pass (2026-10-02 night, after batches 16 and 17)

All 131 shelves (835 slugs after the drop below).

- **URLs.** 837 checked before the drop. Five Gutenberg files reset or dropped TLS on the first sweep, and all five answered on retry. Lang's Lockhart vol. 1, which returned HTTP 500 at the fifth pass, answered this time. Every slug is in the map.
- **Same source held twice.** None. The title collisions are the same multi-volume sets as before.
- **Translators.** The catalog check finds nothing new. Batch 17's translations name their translators in `_translators` (Westervelt for his own Hawaiian translations, Percival for the Kremnitz tales, Worster for Rasmussen, Allen for his Korean tales), and `--verify --record` matched each one.
- **Text held twice, new this pass.**
  - Paine's *Mr. Rabbit's Wedding* (96%) and *Mr. Turtle's Flying Adventure* (91%) are reprints of stories in his *Hollow Tree Nights and Days*. Both were dropped from the shelf and are recorded in its `_excluded`. *How Mr. Rabbit Lost His Tail* shares nothing with it and stays.
  - Westervelt's *Legends of Old Honolulu* and *Hawaiian Legends of Volcanoes* share 15 paragraphs, 3% of each. The Pepper books share a handful of recap paragraphs. Bryant's *How to Tell Stories* shares 5 paragraphs with Richards's *Pig Brother*. All of these are small: mint them once.
- **Excluded before commit** (measured): Hale's second Peterkin Papers transcription (82% both ways), Webster's second Daddy-Long-Legs transcription (58%/68%, held once as the same work), and Bryant's second Stories to Tell to Children transcription (68%/65%, held once). Webster's stage *Daddy Long-Legs* is a different work and waits on Adam (DIGEST decision 13).
- **OCR.** Batches 16 and 17 added no Internet Archive volumes.

## 9. Seventh pass (2026-10-02 night, after batch 18)

All 137 shelves (890 slugs: 790 Gutenberg, 69 Internet Archive, 31 CCEL).

- **Slug count corrected.** The batch 18 DIGEST commit said 892 slugs; batch 18 added 55, not 57, so the total is 890. The DIGEST is fixed.
- **URLs.** 890 checked. Ten Gutenberg files reset on the first sweep, and all ten answered on retry. Every slug is in the map.
- **New check: who the Gutenberg header names.** The surname test can pass a book whose shelf author only wrote its introduction, because the name appears in the text. Batch 18 caught one this way: *The Wild Heart* is by Emma-Lindsay Squier, with an introduction by Stratton-Porter. It was dropped before commit, and that shelf's `_surname` is now "stratton-porter" alone. A new script compares each Gutenberg item's header Author, Editor, Translator and Compiler lines against the shelf's `_surname`, across all 790 Gutenberg items. It flagged three: Burgess's *Sammy Jay*, Baldwin's *Story of the Golden Age* and Baring-Gould's *Grettir the Outlaw*. All three have headers that name only the illustrator, and Gutenberg's catalog and the title pages name the right author. No other book is credited to someone else.
- **Same source held twice.** None new.
- **Translators.** The catalog lists Spenser as an author of Jean Lang's *Stories from the Faerie Queen*. It is her prose retelling, so no translator is involved.
- **Text held twice.** Ouida's *Bimbi* shares stories with her two other collections (Nürnberg Stove, Lampblack, Bandita, The Ambitious Rose Tree): 27% and 13% of it. Mint those once, with two witnesses. The single-story books were held once before commit, as was Garis's *Old Mother Hubbard* (97% inside *Uncle Wiggily and Mother Goose*). Garis's fourteen picture pamphlets share almost nothing with his longer books (5% at most), so they stay.

## 10. Eighth pass (2026-10-03 small hours, after batches 19-21 and review rounds 6-7)

All 163 shelves (926 slugs).

- **URLs.** 926 checked in three chunks (one sweep at higher concurrency tripped the proxy's Gutenberg tunnel and was discarded). Five Gutenberg files reset on the first try and all five answered on retry. Lang's Lockhart vol. 1 returned HTTP 500 again, as at the fifth pass; the Internet Archive record still lists its text file, and the local copy fetched on 2026-10-02 is intact. Every slug is in the map.
- **Author names.** Lane A's load-time gate (e1ef08b) and the reviewer's round 6 led to full-name `_surname` forms on 32 shelves (REPORT-D). Every Lane D shelf passes `check_surnames`, and every re-recorded book matched. The change caught one misattribution: Lang's shelf held a 1896 Christian Literature Society for India pamphlet "compiled from Lang, Caldwell, Conway, Tylor ... and others", now in `_held` (DIGEST decision 16).
- **Header-author check.** Unchanged since the seventh pass: three Gutenberg headers name only an illustrator (Burgess's Sammy Jay, Baldwin's Story of the Golden Age, Baring-Gould's Grettir), and each text names its author.
- **Same source held twice.** None new. The only new title collision is "Welsh Fairy-Tales" (P. H. Emerson, PG 8675) against "Welsh Fairy Tales" (Griffis, PG 9368): different books.
- **Translators.** The catalog check finds nothing new. Batch 21's translations carry `_translators` (Jones for the Magyar tales, Hall, O'Connor, Ralston for Tibetan Tales), and `--verify --record` matched each one; Gutenberg's header for Tibetan Tales names both Schiefner and Ralston.
- **Text held twice.** Batch 21's sixteen new books were compared paragraph by paragraph against every built book. The only overlap above five paragraphs is seven quoted passages Jameson's Sacred and Legendary Art shares with Kingsley's lectures (7 of 1,327). Mint once.
- **CCEL.** Lane A's print-source check (36ca012) flags four MacDonald books keyed from 1934-2001 reprints (DIGEST decision 17).

## 11. Ninth pass (2026-10-03 small hours, after batches 22-24)

All 190 shelves.

- **URLs.** 983 URLs on the 181 shelves of batches 1-23 checked in one sweep. Three Gutenberg files reset the connection and all three answered on retry; Lang's Lockhart vol. 1 returned HTTP 500 again (local copy intact). Batch 24's 16 files were fetched fresh the same hour and every slug is in the map.
- **Jacobs's Celtic Folk and Fairy Tales (PG 35862), held since relay 5 as a probable retitling.** Compared paragraph by paragraph with Celtic Fairy Tales (PG 7885): 81% of each book's long paragraphs are in the other, and the preface is the same. It is Putnam's American title for the same book; it stays in `_excluded`, now with the measurement recorded. Closed.
- **Text held twice.** Batches 22-24 (47 new books) were compared against every built book. Above 10%: van Dyke's Blue Flower repeats three of his separate books (75%, 62%, 50%; mint once, two witnesses), and Irving's Pennell-illustrated Alhambra (PG 49872, 66%) is held once as the same work. Below 10% but real: Ewald's Old Willow Tree (1921) reprints three tales from The Spider (1907) in a revised text, 59 paragraphs alike; mint those once. The Queen Bee is Moore Smith's separate translation of five of the same tales: a different witness, nothing shared word for word.
- **Same tale title twice in one book.** Magnus's three tales called A Tale of the Dead, Curtin's two Koshchéi and two Yahyáhaäs tales, and Dracott's two Sheik Chilli tales used to collide or run together. `convert_nested.py` now takes `number_repeats`, and they cite as "(2)", "(3)". Tests: convert_nested 14 passed, structure_test 64 passed.
- **Translators.** Every batch 23-24 translation carries `_translators`, and `--verify --record` matched each name in its text (Curtin, Larminie, Rehatsek and Ouseley under Clouston, Harding, Magnus, Gaster, Theal, Friedlander, Szold, Teixeira de Mattos, Moore Smith, Wratislaw, Borrow). 0 Gutenberg copyright markers. One translator was refused rather than assumed: Paul Radin's Ginzberg volumes are held (DIGEST decision 18).
- **Retention.** Every new book was checked for prose paragraphs that land in no unit: none lost. The only flagged lines are headings (Clouston's "Gothamite Drolleries (continued)", Howes's "Fairy Tenderheart.").
- **Header-author check.** Two headers word the name differently from the title page (Dracott: "Alice Dracott" against "Alice Elizabeth Dracott"; Wratislaw as compiler). Both texts print the full name, and `_surname` uses it.
- **Name forms (reviewer cycle 9).** Bare "webster", "wilde" and "perkins" each passed two different people's books. Now "jean webster", "wentworth webster", "lady wilde"/"speranza", "oscar wilde" and "lucy fitch perkins", re-recorded clean (0ba7662). The three forms still shared between Lane D shelves name one person on both sides: Joseph Jacobs, William Morris and Martens.
- **number_repeats** now counts a heading once it holds text, so a Contents list cannot use up "(2)" (b8e46fd, two new tests; the eight books using it rebuild with identical ids).

## 12. Tenth pass (2026-10-03 morning, after batches 25-27): name forms

- **Why.** The coordinator found two Lane D shelves gating on a bare surname that another lane's shelf also claims for a different person: kalevala's "crawford" against PR #14's Thomas J. Crawford, and frere's "frere" against W. H. Frere on puritan-manifestoes. A bare surname passes any text that prints it, so a wrong book with the right surname gets through.
- **What was done.** Every Lane D shelf that gated on a one-word form (130 shelves) now gates on the full name its own texts print: "e. nesbit" and "edith nesbit" instead of "nesbit", "lewis carroll" instead of "carroll", and so on. Each form was read from the shelf's texts, not supplied from memory. Every shelf was then rerun with `fetch_shelf --verify --record`, giving 0 mismatches and 0 rights flags on all 130. hearn_shelf.json is left as it was: Lane C has since added to it, the pre-commit gate counts it as theirs, and it already carries "lafcadio hearn" beside the bare "hearn". One shelf failed until a form was added: Dutt's Ramayana scan prints "Romesh Chandra Dutt", not "Romesh C. Dutt".
- **Collisions checked across branches.** The new forms were compared with the shelf files on every remote branch, not only this one. On Lane D's side, the forms still shared between two shelves each name one person: Joseph Jacobs (aesop and jacobs-fairy), William Morris (beowulf and poetic-edda) and Frederick H. Martens (stroebe and wilhelm).
- **One-word forms kept on purpose.** These are names, not English words, and some texts print no fuller form: aesop/æsop, andersen (Lucas's edition prints only "ANDERSEN"), grimm (the 1884 Hunt volumes print no first names), caxton and voragine, dodgson, gummere and kirtlan (beside the full forms), laboulaye, lagerlöf, lönnrot, mijatovich (three spellings), ouida, straparola, sturluson and zitkala.
- **Other lanes' bare forms that pass Lane D authors.** These are their fixes to make, and are reported to the coordinator: "owen" (would pass Elias Owen), "curtin" (Lane C: Jeremiah Curtin on both, so the same person), "horace" and "newton" (would pass Horace N. Allen), "maude" (would pass Maude Ashurst Biggs), "perkins" (would pass Lucy Fitch Perkins) and "preston" (would pass Josephine Preston Peabody).

## 13. Eleventh pass (2026-10-10, after batches 28-31): life-plus-seventy

Every Lane D Gutenberg row was checked against the Gutenberg catalogue's dates for each author, translator, editor and compiler (illustrators left out, since no pictures are in the text). The rule adopted on 2026-10-03, and applied to every batch since, is to hold a book when any of those people died after 1955 or has no recorded death date. Shelves made before that rule were never re-checked against it. This pass does that.

**Died after 1955. All are US public domain by publication date, but still in copyright in the UK and in other life-plus-seventy countries:**
- Padraic Colum (1881-1972): all 7 books on `colum`.
- Thornton W. Burgess (1874-1965): all 28 books on `burgess`.
- Howard R. Garis (1873-1962): all 35 books on `garis`.
- Elsie Spicer Eells (1880-1963): all 3 books on `eells`.
- Sara Cone Bryant (1873-1956): both books on `sara-bryant`.
- A. A. Milne (1882-1956): all 5 books on `milne`. UK copyright ends on 1 January 2027.
- Cecil Henry Bompas (1868-1956): `bompas-folklore-of-the-santal-parganas`.
- Carol Della Chiesa (1887-1972), translator: `collodi-pinocchio-della-chiesa`.

**Birth year only, no death date in the catalogue:** A. E. Johnson (born 1879; Perrault, `perrault-old-time-stories-johnson`), Klara Stroebe (born 1887; both `stroebe` books), Henry Gilbert (born 1868; `gilbert-king-arthurs-knights`), Gudrun Thorne-Thomsen (born 1873; `thorne-thomsen-birch-and-the-star`), Laura E. Poulsson (born 1851; `poulsson`), Lajos Kropf (born 1852; `jones-kropf`), Marie L. McLaughlin (born 1842; `mclaughlin`) and May Kendall (born 1861; `lang-that-very-mab`). Charles Swan (born 1797; `gesta-romanorum`) cannot be living, so he is not listed as a risk.

**No dates at all:** several translators and compilers, among them Mrs. Lang, Fanny Fuller, Marion Edwards (the catalogue's spelling), Elisabeth Stork, Edward L. Stowell, Mary Macgregor, Eliza Keary, E. M. Berens, Ellen C. Babbitt, Beatrice E. Clay, Mrs. Rafy, Charles Sellers, Elizabeth W. Grierson, Mrs. Angus W. Hall, Emily J. Harding, Elias Owen, Yei Theodora Ozaki, Amy Steedman and Grace James. Every one of their books was published before 1931. The catalogue gives no dates for them, and this pass did not look further.

Nothing was removed. Everything above was taken under the US rule in force when it was shelved. Whether Armarium should keep, label or hold these books is Adam's decision (DIGEST-D decision 22).

## 14. Twelfth pass (2026-10-10, after batches 32-34): later reprints

The front and back matter of every Lane D Gutenberg text was searched for copyright, renewal, ISBN or SBN, "all rights reserved" and "printed in" lines, to find books whose Gutenberg file was made from a later reprint rather than the first printing. Two books on the hearn shelf were not checked: their files were not on disk in this session.

**Later reprints of the same text (24 books).** These carry a reprint's printer line, ISBN or SBN, but no editor, introduction or other added text was found: `lang-blue-poetry-book`, `lang-tales-of-romance`, `pyle-sir-launcelot` (Dover, 1991; it says it is an unabridged republication of Scribner's 1907 edition), `nesbit-oswald-bastable-and-others`, `nesbit-nine-unlikely-tales`, `potter-tailor-of-gloucester`, `potter-mr-tod`, `potter-fierce-bad-rabbit`, `grahame-headswoman`, `perrault-old-time-stories-johnson`, `crooke-talking-thrush`, `hull-cuchulain-hound-of-ulster`, `lady-wilde-ancient-legends-of-ireland`, `jean-lang-stories-from-the-iliad`, `jean-lang-stories-from-the-faerie-queen`, `beatrice-clay-stories-from-morte-darthur-and-mabinogion`, `katharine-pyle-wonder-tales-from-many-lands`, `stephens-deirdre`, `macmillan-canadian-fairy-tales`, `ebbutt-hero-myths-and-legends`, `mrjames-five-jars`, `greenaway-under-the-window`, `greenaway-marigold-garden` and `curtin-myths-and-folk-tales-of-ireland`. The reprint's notices sit in the front matter (`front, par. n`), not in the cited text. One gap: the Curtin file was made from Dover's 1975 reprint, which, the transcriber notes, leaves out the 1890 edition's introduction, frontispiece and dedication. So the book on the shelf is the text without its introduction.

**Copyright lines dated 1927 to 1929 (no new problem).** These were published in or before 1929, so they are US public domain now: Potter's The Fairy Caravan (1929), Barrie's Peter Pan play (1928), Lofting's Doctor Dolittle in the Moon (1928, renewed 1956; Lofting died in 1947), Milne's two books, three Garis books and Burgess's Jimmy Skunk (renewed 1946). The Milne, Garis and Burgess books, and Colum's Children of Odin (a modern Macmillan paperback with an ISBN), are already among the 82 in §13.

**False alarms.** Benjamin Bunny's 1932 line is a renewal of 1904. The two Lucy Fitch Perkins hits come from an old Gutenberg header.

Nothing was removed. Before Armarium presents any of these as a particular edition, it should name the reprint, not the first printing.
