---
fable_review: pending
---
# The Hebrew Old Testament in the corpus JSONL (Westminster Leningrad Codex)

*Schema `wordhoard/corpus-jsonl/v1`, the four files the hymns and the Greek NT
use (`README-hymn-jsonl.md`, `README-nt-jsonl.md`), with the differences
written down here. Built by `pipeline/build_ot_corpus.py`, validated by
`tests/ot_corpus_test.py`. 2026-10-02.*

```
data/ot/<Book>/passages.jsonl     one line per verse (the KJV verse that already exists)
data/ot/<Book>/witnesses.jsonl    one line per verse: the Hebrew (hbo.wlc)
data/ot/<Book>/tokens.jsonl       one line per word of it
data/ot/<Book>/alignments.jsonl   one line per verse: hbo.wlc faces kjv.plain
data/ot/manifest.json             one over all 39 books: counts, shards, versification,
                                  sources + licence evidence, rulings, checksums
```

`<Book>` is the OSIS book, in the KJV's order (`Gen` … `Mal`). Read the files
through `build_ot_corpus.load_ot()`, which follows the manifest.

## 1. What is in it, and what is not

| | |
|---|---|
| WLC verses read | 23,213 |
| passages (KJV verses with a Hebrew witness) | 23,142, uids reused, **0 minted** |
| tokens | 305,124 |
| ketiv / with a qere / written-not-read | 1,264 / 1,241 / 6 (and 11 ketiv sharing a two-word qere) |
| qere read but not written | 9, on their witness as `qere_only` |
| lemma, parsing, gloss | **none** (s.2) |
| on disk | 132 MB; about 10.5 MB gzipped; the largest file 7.8 MB |

## 2. The licence gate: the text is public domain, the lemmas are not

The Open Scriptures Hebrew Bible (github.com/openscriptures/morphhb, pinned at
`3d15126`) carries two works in one file:

| | licence | where it says so |
|---|---|---|
| the WLC text | **Public Domain** | each book's `<work osisWork="WLC"><rights>`; README: "The text of the WLC remains in the Public Domain" |
| OSHB's lemmas and morphology (`lemma=`, `morph=`, the `/` morpheme splits, the word ids) | **CC BY 4.0** | README: "Lemma and morphology data are licensed under a Creative Commons Attribution 4.0 International license" |

This repo is public and its gate admits public-domain editions and the house's
own work only (ADR 0001; launch plan D4). CC BY is collected, used, and never
served whole: the STEPBible lexicons and the TVTMS table already live that
way, in gitignored `data/corpus/`. So these files take **the words and nothing
OSHB added**: the text of each `<w>` with its morpheme slashes removed, the
maqqef, sof pasuq, paseq and inverted nun, the pe/samekh section marks, and
each qere. Every token's `lemma`, `lemma_key`, `parsing` and `gloss` is null,
and the manifest says why once (`token_provenance`), not on 305,124 tokens.

This is the biggest difference from the Greek NT, whose lemmas (Strong's 1890
by Robinson's numbers) and parsing (Robinson's) are public domain. A Hebrew
lemma layer needs one of:

- **ADR 0019**, the ruling that would also admit SBLGNT: OSHB's layer as its
  own file keyed by token address, with its rights block and attribution,
  never merged into these PD files; or
- a public-domain route to the lemma. Strong's Hebrew dictionary is PD and
  already in this repo, but assigning a Strong's number to each word is
  exactly OSHB's CC BY work, so it cannot be borrowed.

## 3. Identity

The same rule as the NT (house style s.2): the registry opens frozen, and each
Hebrew verse is a witness of the KJV verse's existing passage. The citation is
`kjv:<OSIS>`; the slug names the versification of record, not the language.

The WLC numbers verses the Hebrew way. `data/versification/bhs-kjv.json`
(PR #5, built from STEPBible's TVTMS, CC BY 4.0, only the 2,037 differing
verses committed) says which KJV verse each Hebrew verse is. A witness whose
Hebrew number differs carries the WLC's own reference as `wlc_ref`, as the
NT's Romans doxology carries `rp_ref`. 2,037 + 4 witnesses do.

## 4. Four house defaults, awaiting Adam

Each is in the manifest with `status: "house default, awaiting Adam's ruling"`.

1. **Psalm titles (67 Hebrew verses).** The Hebrew numbers a psalm's title as
   verse 1 (sometimes 1–2); the KJV prints it unnumbered, so there is no
   `kjv:` uid to hang it on. Default: left out, each listed under
   `versification.left_out` with its WLC reference. Giving titles a
   citation (`kjv:Ps.51.title`) would mint uids, which can never be taken
   back (R5). That wants a ruling first.
2. **Two Hebrew verses that make one KJV verse (4):** Num 26:1, 1 Sam 20:42,
   1 Kgs 22:43, 1 Chr 12:4. Default: ONE witness, their texts joined in
   codex order, tokens numbered straight through, `wlc_ref` a list and
   `wlc_verse_starts` the token where each Hebrew verse begins.
3. **One Hebrew verse that holds two KJV verses (2):** Ps 13:6 (KJV 13:5–6)
   and Isa 63:19 (KJV 63:19 + 64:1). Default: a witness of the first KJV
   verse; its alignment is `1:2` and names both. KJV Ps 13:6 and Isa 64:1
   then have no Hebrew witness of their own, and are listed with Neh 7:68
   (which the Hebrew lacks) under `kjv_verses_without_hbo`.
4. **Sharding:** one folder per book, as the NT (PR #8).

## 5. The records

**passages.jsonl:** as the NT's; `pericope` is null.

**witnesses.jsonl:** `name: "hbo.wlc"`, `lang: "hbo"`, `register:
"biblical"`, `textform: "masoretic"`, `text` (the verse as the codex prints
it: words, maqqef, paseq, sof pasuq; no section letter), `section_mark`
(`"pe"`, `"samekh"` or null), and where they apply `wlc_ref`,
`wlc_verse_starts`, `qere_only` (`[{after: <token position>, qere}]`).

**tokens.jsonl:** the NT's eight fields, with:

| field | content |
|---|---|
| `surface` | the word as written, the ketiv where there is one; OSHB's `/` removed |
| `normalized` | `NFC(surface)` |
| `search_key` | consonants only: every point and accent dropped, maqqef and signs dropped, final forms folded (ך→כ …) |
| `translit` | null: no house Hebrew scheme yet (s.6) |
| `lemma`, `lemma_key`, `parsing`, `gloss`, `plain_form` | null (s.2) |
| `provenance` | null; the manifest's `token_provenance` holds the one value |
| `ketiv`, `qere` | on a ketiv token: `true`, and the pointed qere (maqqef kept), or null |
| `not_read` | a ketiv with an empty qere (ketiv wela qere) |
| `qere_at` | a ketiv whose qere is read over it and the next word: the position of the token carrying the qere |

**Word division.** A token is a word of the codex. In 12 places OSHB splits
one written word into two `<w>` with no space between, "for exegesis" (its own
note). They are rejoined: the WLC word is the token. OSHB marks 21 exegesis
notes; the other 9 are where the XML already spaces the words, and they are
kept as the XML has them (`wlc_notes_by_n` counts every note kind).

**alignments.jsonl:** `hbo.wlc` ↔ `kjv.plain`, same uid; `type` `1:1`, or `1:2`
for the two spans. It aligns verses, not readings.

## 6. Not done here

- **Transliteration.** The SBL academic scheme for Hebrew needs vowel length,
  vocal or silent shewa and dagesh forte or lene decided per word. That is
  rule work of its own, with fixtures, as the Greek's was. `translit` is null.
- **Glosses and a plain line.** Nothing to gloss from without lemmas (s.2).
- **The reader.** It shows the hymns and John 1. A Hebrew passage would want
  right-to-left layout; nothing here blocks it.

## 7. Commands

```
python3 pipeline/build_versification.py --fetch   # the pinned WLC -> data/corpus/wlc/ (gitignored)
python3 pipeline/build_ot_corpus.py --check       # mint 0, byte-identical
python3 tests/ot_corpus_test.py                   # the validator
```

`raw.githubusercontent.com` rate-limits a bulk fetch. A clone of morphhb at
`3d15126` with its `wlc/` copied into `data/corpus/wlc/3d15126/` gives
byte-identical files (every sha256 matches `build_versification.WLC_PINS`).
