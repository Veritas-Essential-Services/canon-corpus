---
model_log:
  - 2026-11-03 claude-opus-5-5 drafted (Church's Homers: collation note)
fable_review: pending
---
# data/unscanned/

Working texts the Unscanner made from scans, shipped gzipped (`SHIPPED_WORKING_TEXT` in
`pipeline/fetch_sources.py`), and what was built on them.

## Church's Iliad and Odyssey for Boys and Girls: the collated text (2026-11-03)

Both books have been in the corpus since 2026-10-16 as the Unscanner's re-OCR of one scan each. This
layer does not acquire anything new: it reads that working text against the Archive's OCR of the same
scan and of other printings, word by word, and settles every disagreement by vote or by looking at the
page image. `pipeline/collate_church_homer.py` holds every rule; nothing is typed into a text by hand.
`structure_texts.py` builds the corpus books from the collated units when they are present (same ids;
only units holding a heading, a footnote or plate junk are gone, and no Armarium plate points at one).

| file | what |
|---|---|
| `<slug>.unscanned.json.gz` | the base: the Unscanner's working text (unchanged) |
| `<slug>.collation-reads.json` | what was read on the page images: places the witnesses could not settle, footnotes, the List of Illustrations; each read names its leaf |
| `<slug>.collated.json` | the result: chapters (titles in the book's order), paragraphs, footnotes, List of Illustrations, and the corpus units |
| `<slug>.collation.json` | every place where the readings differ, with each witness's words and who decided it |
| `<slug>.md` | the reading text |

Rebuild: `python3 pipeline/collate_church_homer.py --fetch` (the witnesses' OCR, gitignored), then
`python3 pipeline/collate_church_homer.py --check` (byte-identical).

### Sources (all printings dated before 1931; first published 1906 and 1907, US public domain)

**The Iliad for Boys and Girls** (New York: Macmillan, September 1907)

| siglum | archive.org | printing | file | sha256 |
|---|---|---|---|---|
| base | iliadforboysgirl00chur_0 | 1923 (Library of Congress) | `church-iliad-boys.unscanned.json.gz` (unpacks to d48108d4…50e4e) | 7f80e3c19522a348d984aaa3c3e25896a0be3eb37e8168696215f0dea39d45e4 |
| A | iliadforboysgirl00chur_0 | the same paper, the Archive's own OCR | `iliadforboysgirl00chur_0_djvu.xml` | 249a06995024c7f5ee3380c13a8854e7ce5453e5ac997c7edb1bb25f0db89d51 |
| B | iliadforboysand00homegoog | **1907, first printing** (Harvard, scanned by Google) | `iliadforboysand00homegoog_djvu.xml` | 023fa2a936d62199d64dff2576345e29055ea359dcab365ebf50eb677f531d89 |
| C | bwb_Y0-BOA-876 | 1927 | `bwb_Y0-BOA-876_djvu.xml` | 67179c567c0869e776bc348462556c1476cb3bbcbbb8168324c64192c1bbbce9 |

**The Odyssey for Boys and Girls** (New York: Macmillan, September 1906)

| siglum | archive.org | printing | file | sha256 |
|---|---|---|---|---|
| base | odysseyforboysgi00chur | 1906 (New York Public Library) | `church-odyssey-boys.unscanned.json.gz` (unpacks to 0ff9026e…f786) | 99bdc5a8b6074c8aafecacf52fef6e53d21b956a82cbdab7b21eb8279486af79 |
| A | odysseyforboysgi00chur | the same paper, the Archive's own OCR | `odysseyforboysgi00chur_djvu.xml` | 15155b6ef7cbb1b8d69bbcbda9d34ad333ae4b7a89b15a265357f6126daad642 |
| B | odysseyforboysa00unkngoog | 1906 (Harvard, scanned by Google) | `odysseyforboysa00unkngoog_djvu.xml` | 9146cb7cd96ff47e00137f10249ec6764a00b4d2a08d48f3c18feb1c6af83284 |

Left out because they are after 1930: iliadforboysgirl0000reva (1932 printing) and bwb_Y0-BOC-827
(Odyssey, copyright 1934).

### Rules (in the script's docstring, in full)

1. Witness furniture goes: Google's notices, running heads and other lines that are mostly capitals,
   folios, signature marks. Line-end hyphens are rejoined, and the hyphen is kept only where the book
   prints the word with a hyphen elsewhere.
2. Base dirt is cleaned: underline specks, stray marks standing alone, tesseract's doubled quotation
   marks, brackets and specks touching a word, and spaced `; : ? !`.
3. Names take their printed marked forms (Telemăchus, Menelaüs, Ænēas, Briseïs). Every form was read
   on the page image.
4. Each witness is aligned with the base on letters only.
5. The vote. The base stands when a witness supports it and no other reading has as many votes. A
   reading two witnesses share, with the most votes, replaces it. Anything else is open and is read on
   the page image. Case and quotation marks are voted too; stops and commas are not.
6. Words the base dropped (mostly last lines at page breaks) are put back when two witnesses agree.
7. Structure:
   - empty units and the colophon are dropped;
   - each chapter's opening word is set in capitals, as printed in small capitals;
   - a unit that begins in lower case continues the paragraph before it;
   - footnotes are taken out of the running text and attached to their paragraph.

### Result

| | Iliad | Odyssey |
|---|---|---|
| chapters | 26 (I–XXV + The End of Troy) | 23 |
| paragraphs | 365 | 418 |
| words | 43,706 (base 43,798) | 42,489 (base 42,643) |
| corpus units | 371 of 374 | 428 of 436 |
| places where the readings differ | 360 | 365 |
| – base kept | 247 | 288 |
| – witnesses' shared reading adopted | 93 | 60 |
| – read on the page image | 20 | 17 |
| names set in their printed form | 182 | 172 |
| quotation marks from the witnesses | 79 | 11 |
| footnotes | 2 (Artemis; two talents) | 2 (Cyprus; the wooden horse) |
| List of Illustrations | 16 plates after Flaxman (the 1923 list) | 12 coloured plates |

Every change a witness made and every open place was checked against crops of the page image.

### What was checked against the 1907 first printing

The base Iliad is a 1923 printing, so the oddities in its text were looked up on the page images of B
(the 1907 first printing).

- **The plates' own misprints are in 1907 too, and are kept as printed:** *Alatanta* (for Atalanta;
  the Harvard copy has a reader's pencil correction), *Nector's* (for Hector's), *Scæn Gates* (for
  Scæan), *Sarēpdon* and *Sarpdoēn* (for Sarpēdon).
- **The List of Illustrations differs between the printings.**
  - The 1907 list has twelve plates and the 1923 list has sixteen.
  - Only 1923 has: Hector Chiding Paris; The Meeting of Hector and Andromaché; The Embassy of
    Achilles; Thetis Bringing the Armour; The Gods Descending to Battle.
  - Only 1907 has: Hera commanding the Sun to Set (facing p. 240).
  - 1907 prints "Polydamas" where 1923 prints "Polydamus".
  - The collated text gives the 1923 list, the one in the base scan. The 1907 list is recorded beside
    it (`illustrations_first_printing`).
  - Not checked: whether the 1923 printing has plates the 1907 one lacks, which is what its list
    suggests.

### Remaining doubts

- **Stops and commas are not voted.** Apart from the cleanup rules and the page reads, they are the
  base OCR's. In the Odyssey, only A votes on quotation marks and case, because B's OCR mangles
  quotation marks.
- **A misreading that every witness shares stands.** The witnesses are mostly the same paper or the
  same plates, so a broken letter can fool them all. This is collated OCR, not a line-by-line
  proofread.
- **Single-witness disagreements stay with the base.** Where only one witness differs (the Odyssey
  has two witnesses), the base wins.
- **Five Odyssey paragraph-end words were restored together with their quotation marks.** The words
  were missing from the base and both witnesses have them. The quotation marks were set from context
  and the page image.
- **Chapter titles follow the Contents in words.** The Contents is set in small capitals. The titles
  are given in title case, with the names in their marked text forms (Andromaché, Menelaüs).

### Stories from Homer (1878)

Checked for a Gutenberg text. None was found in the GITenberg mirror or in archive.org's gutenberg
collection. gutenberg.org itself was not reachable from this session. Scans are listed in
`data/poetry/pool/sources.json`. Nothing was fetched.
