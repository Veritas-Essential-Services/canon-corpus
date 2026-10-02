<!-- prov: 2026-10-02 claude-opus-5-5 drafted -->
<!-- fable_review: pending -->
# data/strongs/ — Strong's numbers as the key for every biblical word

Adam, 2026-10-02: *"ingest Strong's Concordance and use that as the source of truth
for those words and use the strongs numbering and save those beside the UID somehow
that makes sense. I want to use that for all biblical language references."*

Built by `pipeline/build_strongs.py`; checked by `tests/strongs_test.py`.

```
python3 pipeline/fetch_sources.py            # the dictionaries, into data/corpus/lexicons/
python3 pipeline/build_strongs.py --fetch    # the Strong's-tagged KJV (eBible), into data/corpus/
python3 pipeline/build_versification.py --fetch   # the pinned WLC, for the local OSHB layer
python3 pipeline/build_strongs.py            # build data/strongs/
python3 pipeline/build_strongs.py --check    # THE GATE: byte-identical, 0 newly proposed
python3 tests/strongs_test.py
python3 pipeline/build_strongs.py --adopt    # ONLY on Adam's ruling (s.4)
```

## 1. What is here

| file | one row per | what it says |
|---|---|---|
| `strongs.jsonl` | Strong's number (14,298) | **The table.** Lemma, transliteration, pronunciation, derivation, definition and KJV renderings, from Strong's own 1890 dictionaries. |
| `proposed-uids.jsonl` | word (14,197) | The Word Hoard uid each word **would** get. Not in the registry. |
| `witnesses.jsonl` | Strong's number | Which entries in BDB, TBESG, LSJ and Thayer write that word up. Citations only. |
| `concordance.jsonl` | number that occurs | Every passage uid it occurs in, per corpus (`kjv`, `nt`), and how many tokens. |
| `kjv-tags.jsonl` | KJV verse (31,102) | Each tagged English word or phrase, in verse order, with its Strong's key. |
| `kjv-renderings.jsonl` | number the KJV tags | Every English rendering of it and how often: the index of Strong's Exhaustive Concordance. |
| `manifest.json` | — | Sources and their sha256, counts, and what is not claimed. |

All committed. The dictionaries themselves stay in the gitignored `data/corpus/`.

## 2. The key, and the two citations

**Key:** `H` or `G` and the number, no leading zeros: `H2617`, `G26`. It is the form
`data/nt/` tokens already carry in `lemma_key`, and what `structure_texts.strongs_id()`
emits. `build_strongs.normalize()` reads every other spelling in the house into it:

| written | key | suffix |
|---|---|---|
| `G0026`, `26` (Greek) | `G26` | — |
| `G0001G` (STEPBible extended) | `G1` | `G` |
| `H1254a` (OSHB augmented) | `H1254` | `a` |

A suffix is a finer split *inside* one Strong's number (G1 is both the letter alpha and
the interjection ἆ). It rides beside the key and is never part of it.

**Two citations, deliberately different:**

- `strongs:G26` names the **word**. It is the natural key the uid hangs on.
- `strongs-greek:G26` names **Strong's 1890 dictionary entry** for it. That is one
  witness of the word, alongside BDB, Thayer, LSJ and TBESG.

That is the house's passage/witness split (CLAUDE.md 3c) applied to words: a word has
one identity and many write-ups, and Strong's own entry is one of them, the one the
numbering comes from.

## 3. Why Strong's is the key, and where it is honest to say so

Strong's numbering is the one public-domain key that every source in this repo already
speaks: the Greek NT tokens (Robinson's numbers), BDB (9,164 of 10,022 entries carry
one), the STEPBible lexicons (extended Strong's), PR #7's Thayer entries, and OSHB's
Hebrew tagging for the Old Testament.

What it is not (rule 4, honesty): it is not a perfect inventory of words.

- **Strong's lumps.** One number can cover two words (G1 above; H2617 is witnessed by
  two BDB entries, BDB2965 and BDB2970). The witness lists keep both.
- **Strong's skips.** 101 Greek numbers, G2717 and G3203 to G3302, are "Not Used". They
  stay in the table flagged `not_used`, and get no uid, because they name no word.
- **Robinson's numbers are not always Strong's choice.** The NT tokens carry the number
  Robinson assigned; where he and Strong would differ, the token's number wins and the
  NT README says so.

## 4. The uids: proposed, not minted

Identity is the uid, and the registry is `data/uids/wordhoard.uids.json` (CLAUDE.md 3b).
Adding 14,197 words to it is Adam's call, so this build writes them to
`proposed-uids.jsonl` and leaves the registry alone.

- Each proposal is minted against everything the registry holds (mapped, tombstoned
  and `reserved`), and the test re-checks that nothing collides.
- Proposals are seeded from the committed file, exactly as the registry is, so a
  rebuild proposes nothing new (`--check`).
- `kind` is `lexeme`, on the record, never in the uid.
- `--adopt` copies them into the registry **verbatim**, so the uid in this file is the
  one the word will have. It refuses if any citation or uid is already taken. After
  adopting, rebuild, and every row says `registered`. Adoption should also add
  `lexeme` to `wh_uid.KINDS`.

Until adoption, a consumer joins on the **Strong's key**, which is stable, and treats
the uid column as provisional.

## 5. How the rest of the corpus links to it

- **The Greek NT** (`data/nt/`): every token's `lemma_key` is a key in the table (all
  140,149 tokens resolve; tested).
- **The Hebrew OT** (`data/ot/`, PR #8): its tokens carry **no** Strong's key, because
  OSHB's lemma tagging is CC BY 4.0 and the licence gate (ADR 0001) keeps it out of
  the committed files. Two things stand in for it:
  1. **Verse level, committed:** the KJV's own tagging (s.6) gives every OT verse its
     Strong's numbers, so the concordance's `kjv` corpus covers the OT.
  2. **Word level, local only:** every build where the pinned WLC is in `data/corpus/`
     writes `build/strongs/oshb-ot/<Book>.jsonl`, one row per `data/ot` token address
     with OSHB's Strong's keys (augment letter kept: `H1254a`) and a `rights.json`.
     `build/` is gitignored, so it is never committed. Drop it by deleting the folder.
     It walks the OSHB files with `build_ot_corpus.read_book()`'s own word rules and
     checks every surface, so it cannot drift from the tokens. 299,162 tokens get one
     key, 12 get two, and 5,950 get none: OSHB gives no number for those words.
- **BDB, TBESG, LSJ:** `witnesses.jsonl`, built from the sources in `data/corpus/`.
- **Thayer:** PR #7's `thayer-entries` book already links each entry to `strongs-greek`.
  It is built only on Adam's machine (the OCR lives there), so a cloud build carries
  Thayer's committed links forward untouched. A local build fills them in.

**A partial build never deletes.** A witness or corpus whose source is absent is
carried forward from the committed files, and the manifest says `carried_forward`.
That is the 2026-09-06 manifest lesson, applied here from the start.

## 6. The English half: the KJV's words, tagged

Strong's *Exhaustive Concordance* lists every KJV English word with the number behind
it. `kjv-tags.jsonl` is that link, verse by verse, and `kjv-renderings.jsonl` is its
index. 349,308 tags across all 31,102 verses, every one a used number in the table.

**The sources, and the rights line of each exact edition (read 2026-10-02):**

| source | rights line | used? |
|---|---|---|
| **eBible.org `eng-kjv2006`** (USFM), "with Strong's numbers added" | Its own page and `copr.htm`: **"Public Domain"** ... "You may copy the King James Version of the Holy Bible freely." Crown letters patent apply in the UK only. | **Yes**, pinned by the sha256 of its 66 USFM files. |
| CrossWire SWORD `KJV` module v3.1 (where eBible's tags come from) | `kjv.conf`: "CrossWire Bible Society hereby grants a general public license to use this text for any purpose"; `DistributionLicense=GPL`. OT tags from The Bible Foundation (bf.org), NT from CrossWire's KJV2003 project. | Lineage only. |
| STEPBible TAHOT / TAGNT | Repo README: **CC BY 4.0**. They tag the Hebrew and Greek with Strong's and carry STEP's own English glosses, not the KJV's words. | No. Not the KJV, and not PD. |

**The rights call is Adam's.** The tags are labelled public domain on the exact
edition, the standard CLAUDE.md sets. The thing to weigh is that CrossWire's own
conf for the same tagging says GPL, though its prose grants use "for any purpose".

How it reads:
- A tagged entry is the KJV word or phrase exactly as tagged (`"man’s hand"` is one
  entry) with the key of the Hebrew or Greek word it translates. Untagged words, such as
  the translators' italics and most articles, are not listed.
- Psalm titles carry tags too (424 of them). The KJV numbers no title, so they sit beside
  verse 1 as `title_tags`, never inside it.
- The tagging is CrossWire's, not checked here against the Hebrew or Greek. Known
  quirk: H853, the untranslatable object marker, appears where the tagger attached it
  to the neighbouring English word.

## 7. What is not claimed yet

- **OSHB's word-level tags in the committed files.** OSHB's lemma and Strong's tagging is
  CC BY 4.0, so it stays local (s.5). Committing it as its own labelled layer, the way
  the OT README's `alternative` describes, is a rights ruling for Adam (rule 6, ADR 0019).
- **The KJV tags are not proofread.** They are CrossWire's, as published.
- **Lemma spelling.** Lemmas are as the OpenScriptures transcriptions give them, not
  Unicode-normalised. Compare with NFC.

## 8. Rights

Strong's 1890 dictionaries are public domain. The Hebrew transcription's XML markup is
CC BY 4.0 (OpenScriptures HebrewLexicon). Only the PD text fields are carried, with
attribution in the manifest. The STEPBible lexicons (CC BY, `redistribute_whole: false`)
contribute **citations only**, never text, so nothing of theirs is redistributed. The
KJV tags: s.6. OSHB's tags: s.5, never committed.
