# Strong's numbers against BDB and Thayer

Built by `pipeline/strongs_coverage.py` from the committed `data/strongs/` and the
dictionaries' sources. Rerun it after any rebuild; `--check` fails if this page is stale.
Each list below is a TSV beside this file.

## Hebrew and Aramaic: Strong's against BDB

- 8,674 Hebrew and Aramaic numbers. 8,202 have a BDB entry of their own.
- 410 appear only in an entry for another word (`bdb-shared`):
  BDB files them under a related word, a spelling or a root.
- 62 appear in no BDB entry at all (4 arc, 58 hbo),
  21 of them proper names. List: `hebrew-numbers-no-bdb-entry.tsv`.

- 10,022 BDB entries; 847 carry no Strong's number. 621 of those are roots
  or unpointed headings (Strong's numbers words, not roots); 226 are pointed words,
  42 of them cross-references ("see ..."). List: `bdb-entries-no-strongs.tsv`.
- 87 entries in BDB's Aramaic part list only Hebrew numbers
  (the Hebrew cognate). They count as `bdb-shared`, never as the Aramaic word's entry.
  List: `bdb-aramaic-entries-hebrew-numbers-only.tsv`.
- 437 pointed entries list numbers none of whose Strong's lemmas spells the
  entry's headword, even with plene and defective spellings, -yahu/-yah, and final letters folded.
  Most are plurals, spelling variants and compound names (`תְּאֻנִים` under H8383).
  Some are errors in the source's key, e.g. BDB7322 קֹדֶשׁ keyed to H6994 (קָטֹן) and H6946
  (Kadesh), not H6944. They are listed for review, not changed: the key is the source's.
  List: `bdb-keys-not-spelling-headword.tsv`.

### Fixed in this pass (PR #10)

- **BDB's Aramaic part keyed to the Hebrew word.** It often lists the Hebrew cognate first
  (Aramaic אֶבֶן "stone" is `H68_H69`), and the first number was taken as the entry's own, so
  Aramaic entries counted as witnesses of the Hebrew word. Now an entry's own number is in its
  own language: 180 Aramaic entries are now keyed to the Aramaic number they list, and the 87
  that list only Hebrew numbers no longer count as the Hebrew word's entry. The other way round,
  5 Hebrew entries list only an Aramaic number (BDB734, the Hebrew lion, gives H744, the
  Aramaic word): they no longer count as the Aramaic word's entry.
- **The first number was not always the headword's.** Where another listed number spells the
  headword, that one is the entry's own: BDB842 תְּאַשּׁוּר is H8391, not H839 listed first;
  BDB1292 בּוֺקֵר "herdsman" is H951, not H941 (Buzi). 68 entries changed (58 Hebrew, 10 Aramaic).
- Together 340 BDB entries changed which number they witness, against PR #10 at 0819e9a.

## Greek: Strong's against Thayer

- 5,624 Greek numbers, 5,523 in use (101 are "Not Used").
- In the committed links: TBESG 5,523, LSJ 5,523, Thayer 0 (Thayer's links are filled in by a build where its entries exist).

- **Thayer's split entries are not in this build.** `thayer-entries` (PR #7) is built only on
  Adam's PC, where the OCR is. Its manifest records 5,486 entries, 5,092 linked to one Strong's
  number by headword and 14 matching more than one (left unlinked), so about 394 entries carry
  no number. Run `python3 pipeline/strongs_coverage.py` there to fill in both Thayer lists.
- Meanwhile `greek-numbers-no-tbesg-or-lsj.tsv` lists the Greek numbers in use that neither
  STEPBible lexicon keys (0).

