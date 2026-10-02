<!-- prov: 2026-10-02 claude-opus-5-5 drafted -->
<!-- fable_review: pending -->
# data/strongs/ — Strong's numbers as the key for every biblical word

Adam, 2026-10-02: *"ingest Strong's Concordance and use that as the source of truth
for those words and use the strongs numbering and save those beside the UID somehow
that makes sense. I want to use that for all biblical language references."*

Built by `pipeline/build_strongs.py`; checked by `tests/strongs_test.py`.

```
python3 pipeline/fetch_sources.py            # the dictionaries, into data/corpus/lexicons/
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
| `concordance.jsonl` | number that occurs | Every passage uid it occurs in, per corpus, and how many tokens. |
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
- **The Hebrew OT** (`data/ot/`, being built from OSHB in the Greek NT thread): read
  the same way the day it lands. `lemma_key` should be the plain key, with any OSHB
  augment letter in its own field; `normalize()` copes either way and the manifest
  counts suffixed tokens.
- **BDB, TBESG, LSJ:** `witnesses.jsonl`, built from the sources in `data/corpus/`.
- **Thayer:** PR #7's `thayer-entries` book already links each entry to `strongs-greek`.
  It is built only on Adam's machine (the OCR lives there), so a cloud build carries
  Thayer's committed links forward untouched. A local build fills them in.

**A partial build never deletes.** A witness or corpus whose source is absent is
carried forward from the committed files, and the manifest says `carried_forward`.
That is the 2026-09-06 manifest lesson, applied here from the start.

## 6. What is not claimed yet

- **The English half of Strong's Concordance.** Strong's *Exhaustive Concordance* lists
  every KJV English word with the number behind it. That needs a KJV whose words are
  tagged with Strong's numbers, and no tagged KJV has had its rights line read here.
  The concordance in this folder is the original-language half: number to passage, from
  the Greek and Hebrew texts themselves.
- **OSHB's tagging is CC BY 4.0.** The WLC text is public domain, but OSHB's lemma and
  Strong's tagging carry CC BY. The OT concordance rows would be facts derived from
  that tagging (which number is in which verse), with attribution in the manifest. That
  is a rights ruling for Adam (CLAUDE.md rule 6).
- **Lemma spelling.** Lemmas are as the OpenScriptures transcriptions give them, not
  Unicode-normalised. Compare with NFC.

## 7. Rights

Strong's 1890 dictionaries are public domain. The Hebrew transcription's XML markup is
CC BY 4.0 (OpenScriptures HebrewLexicon). Only the PD text fields are carried, with
attribution in the manifest. The STEPBible lexicons (CC BY, `redistribute_whole: false`)
contribute **citations only**, never text, so nothing of theirs is redistributed.
