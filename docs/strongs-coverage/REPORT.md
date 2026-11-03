# Strong's numbers against BDB and Thayer

Built by `pipeline/strongs_coverage.py` from the committed `data/strongs/` and the
dictionaries' sources. Rerun it after any rebuild; `--check` fails if this page is stale.
Each list below is a TSV beside this file.

## Hebrew and Aramaic: Strong's against BDB

- 8,674 Hebrew and Aramaic numbers. 8,262 have a BDB entry of their own.
- 374 appear only in an entry for another word (`bdb-shared`):
  BDB files them under a related word, a spelling or a root.
- 38 appear in no BDB entry at all (4 arc, 34 hbo),
  14 of them proper names. List: `hebrew-numbers-no-bdb-entry.tsv`.

- 10,022 BDB entries; 847 carry no Strong's number. 621 of those are roots
  or unpointed headings (Strong's numbers words, not roots); 226 are pointed words,
  42 of them cross-references ("see ..."). List: `bdb-entries-no-strongs.tsv`.
- 61 entries in BDB's Aramaic part list only Hebrew numbers
  (the Hebrew cognate). They count as `bdb-shared` unless an override row says otherwise:
  45 root, 9 the word's Hebrew number, shared, 7 override. A root heading ("√ of following")
  is no word, so no Aramaic number is its own. The rest list the Hebrew number of the same word
  (Strong's numbers a name once, and כֹּר "Aramaic the same"); they stay shared, except where
  BDB has no Hebrew entry for the word (H8674 Tattenai): there the override table makes
  the Aramaic entry its own. Slips are in the override table too.
  List: `bdb-aramaic-entries-hebrew-numbers-only.tsv`, with each row's kind.
- 437 pointed entries list numbers none of whose Strong's lemmas spells the
  entry's headword, even with plene and defective spellings, -yahu/-yah, and final letters folded.
  By kind: 223 related form, 80 cross-reference, 66 word the entry names, 36 override, 32 compound name.
  `suspect_kind()` tries compound name, cross-reference, related form, then word the entry
  names, and the first that fits is the row's kind. All but `override` stand
  as the source keys them: plurals, variants and derivatives (`תְּאֻנִים` under H8383),
  compound names, cross-references, and words the entry names (a reading it corrects, the
  word its lemma field also prints). `override` rows are slips in the source's key, e.g.
  BDB7322 קֹדֶשׁ keyed to H6994 (קָטֹן), not H6944. Every entry here for which some Strong's
  lemma spells the headword was read by hand; the slips found are
  `data/strongs/bdb-key-overrides.jsonl` (44 rows, each with its reason, the source
  untouched). List: `bdb-keys-not-spelling-headword.tsv`, with each row's kind.

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
  (The counts in these first two items were measured against that commit; those below are
  read from the data on every run.)
- **Slips in BDB's key, overridden.** 44 rows. 39 entries (37 Hebrew, 2 Aramaic) are keyed to a word
  they are not about, most by one digit (BDB7322 קֹדֶשׁ H6994 for H6944, BDB578 H8396 Tabor
  for H8386). `data/strongs/bdb-key-overrides.jsonl` gives each its own number and why;
  37 slipped keys are dropped, and a related word the source also lists stays shared.
  1 more Aramaic entry only drops a slip (BDB9800 עֲשַׂב keyed H6611 Pethahiah), and 4
  names that occur only in the Aramaic of Ezra (Achmetha, Asnappar, Shethar-bozenai,
  Tattenai), which Strong's numbers once, as Hebrew, now have their BDB entry as their own.
- **Aramaic words tagged Hebrew.** 25 numbers whose printed derivation opens "(Aramaic)" read as
  Hebrew: the markup tags proper names (and H426 "God", H576 "I") `x-pn` in place of a
  language (H1841 Daniel, H3567 Cyrus). The printed note now wins (`lang_from: derivation` on the row), so BDB's Aramaic
  entries for them are their own entries. Of the 87 Aramaic entries counted above as listing
  only Hebrew numbers, 26 were these words (counted before this rule).

## Greek: Strong's against Thayer

- 5,624 Greek numbers, 5,523 in use (101 are "Not Used").
- In the committed links: TBESG 5,523, LSJ 5,523, Thayer 0 (Thayer's links are filled in by a build where its entries exist).

- **Thayer's split entries are not in this build.** `thayer-entries` (PR #7) is built only on
  Adam's PC, where the OCR is. Its manifest records 5,486 entries, 5,092 linked to one Strong's
  number by headword and 14 matching more than one (left unlinked), so about 394 entries carry
  no number. Run `python3 pipeline/strongs_coverage.py` there to fill in both Thayer lists.
- Meanwhile `greek-numbers-no-tbesg-or-lsj.tsv` lists the Greek numbers in use that neither
  STEPBible lexicon keys (0).

