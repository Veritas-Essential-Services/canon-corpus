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
python3 -c "import sys; sys.path.insert(0,'pipeline'); import fetch_sources as F; F.fetch_vulgate(); F.fetch_douay()"
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
| `concordance.jsonl` | number that occurs | Every passage uid it occurs in, from the Greek NT's own tokens (`nt`), and how many tokens. |
| `parallels.jsonl` | KJV verse numbered differently elsewhere (5,423) | Its verse ids in the Clementine Vulgate, the Douay-Rheims and Brenton's Septuagint. |
| `manifest.json` | — | Sources and their sha256, counts, what is not claimed, and the local files' sha256 (`local`). |

Those are committed. **Everything drawn from the KJV's Strong's tags is built
locally to the gitignored `build/strongs/`**, because whether those tags are public
domain or GPL is still Adam's call (s.6):

| file (local) | one row per | what it says |
|---|---|---|
| `kjv-tags.jsonl` | KJV verse (31,102) | Each tagged English word or phrase, in verse order, with its Strong's key. |
| `kjv-renderings.jsonl` | number the KJV tags | Every English rendering of it and how often: the index of Strong's Exhaustive Concordance. |
| `concordance-kjv.jsonl` | number the KJV tags | Every KJV passage uid it occurs in: the `kjv` half of the concordance. |
| `concordance-view.jsonl` | used number (14,197) | **The concordance view**: everything above about one number, in one row (s.9). |

`manifest.local` records their sha256, row counts and the rights block
(`redistribute_whole: false`); a rebuild with `--fetch`ed tags proves itself against
it. On 2026-10-02 these files were removed from the branch tip. They are still in
the branch's earlier commits (and in #7's and #11's branches, which carry it), so
they stay visible on GitHub until those branches are squash-merged and deleted,
or rewritten; that is Adam's call (PR #10, decision 7). The dictionaries themselves stay
in the gitignored `data/corpus/`.

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
  1. **Verse level, local:** the KJV's own tagging (s.6) gives every OT verse its
     Strong's numbers, so `build/strongs/concordance-kjv.jsonl` covers the OT. Like
     every file from those tags it waits on Adam's rights call before it is committed.
  2. **Word level, local only:** every build where the pinned WLC is in `data/corpus/`
     writes `build/strongs/oshb-ot/<Book>.jsonl`, one row per `data/ot` token address
     with OSHB's Strong's keys as plain `H<n>`, any augment letter (`1254a`) in its own
     `augment` field, keyed by address, passage uid and position, plus a `rights.json`.
     `build/` is gitignored, so it is never committed. Drop it by deleting the folder.
     It walks the OSHB files with `build_ot_corpus.read_book()`'s own word rules and
     stops if any verse's word count differs; `tests/strongs_test.py` checks that
     every surface matches the data/ot token it keys. 299,162 tokens get one
     key, 12 get two, and 5,950 get none: OSHB gives no number for those words.
- **BDB, TBESG, LSJ:** `witnesses.jsonl`, built from the sources in `data/corpus/`.
  BDB files several numbers under 1,204 of its entries (H6_H8: two forms of one
  word; but also words it only mentions, like H430 under the entry for YHWH).
  Only one is the entry's own and counts as a witness (`bdb`): of the numbers in the
  entry's own language (Aramaic from BDB9264, where BDB's Aramaic part opens; it often
  lists the Hebrew cognate first), the one whose Strong's lemma spells the headword, else
  the first. The rest are listed apart as `bdb-shared`, never as witnesses.
  Where the source's key is a slip (BDB7322 קֹדֶשׁ "holiness" keyed H6994 קָטֹן, for
  H6944), `data/strongs/bdb-key-overrides.jsonl` names the entry, the keys the source
  gives, the number that is its own, the keys that are slips and are dropped, and why:
  44 rows, each read in both books: 39 slips given their own number, 4 names found only
  in the Aramaic of Ezra that Strong's numbers once, as Hebrew (`own_lang_differs` says
  why), and one row that only drops a slip. The source is never edited. The build stops if a
  row's entry or number is unknown, if the source's keys are no longer what the row was
  written for, or if a row matches nothing; the manifest records the file's sha256.
  A number is Aramaic where the markup tags it so or where Strong's printed derivation
  opens "(Aramaic)". The markup tags proper names `x-pn` in place of a language, so 25
  Aramaic words tagged `x-pn` would read as Hebrew; those rows carry
  `lang_from: "derivation"`. Most are names (H1841 Daniel, H3567 Cyrus); two are not
  (H426 אֱלָהּ "God", H576 אֲנָא "I").
  `proper_name` is that same `x-pn` tag, read as the markup gives it. It is not the
  same as Strong's own part of speech: 255 tagged `x-pn` have no `n-pr` part of speech
  (mostly gentilics such as H91 "Agagite", which are names in all but form, plus a few
  plain words like H426 and H576), and 50 with an `n-pr` part of speech are not tagged
  (H11 Abaddon). Neither field alone is the list of names; both are kept as given.
  `pipeline/strongs_coverage.py` reports what no entry covers: `docs/strongs-coverage/`.
- **Thayer:** PR #7's `thayer-entries` book already links each entry to `strongs-greek`.
  It is built only on Adam's machine (the OCR lives there), so a cloud build carries
  Thayer's committed links forward untouched. A local build fills them in.

**The corpora are read through their own loaders** (`load_nt()`, `load_ot()`), never
by path. Since PR #8's 44cb57d their shards are rebuilt by `pipeline/rebuild_bible.py`,
not committed. When they are absent, the committed concordance rows stand.

**A partial build never deletes.** A witness or corpus whose source is absent is
carried forward from the committed files, with the committed manifest's stats
unchanged (so `--check` still passes); the build says so on stdout.
That is the 2026-09-06 manifest lesson, applied here from the start.

## 6. The English half: the KJV's words, tagged

Strong's *Exhaustive Concordance* lists every KJV English word with the number behind
it. `build/strongs/kjv-tags.jsonl` is that link, verse by verse, and
`kjv-renderings.jsonl` is its index. Both are local until the rights call below. 349,308 tags across all 31,102 verses, every one a used number in the table.

**The sources, and the rights line of each exact edition (read 2026-10-02):**

| source | rights line | used? |
|---|---|---|
| **eBible.org `eng-kjv2006`** (USFM), "with Strong's numbers added" | Its own page and `copr.htm`: **"Public Domain"** ... "You may copy the King James Version of the Holy Bible freely." Crown letters patent apply in the UK only. | **Yes**, pinned by the sha256 of its 66 USFM files. |
| CrossWire SWORD `KJV` module v3.1 (where eBible's tags come from) | `kjv.conf`: "CrossWire Bible Society hereby grants a general public license to use this text for any purpose"; `DistributionLicense=GPL`. OT tags from The Bible Foundation (bf.org), NT from CrossWire's KJV2003 project. | Lineage only. |
| STEPBible TAHOT / TAGNT | Repo README: **CC BY 4.0**. They tag the Hebrew and Greek with Strong's and carry STEP's own English glosses, not the KJV's words. | No. Not the KJV, and not PD. |

**The rights call is Adam's.** The tags are labelled public domain on the exact
edition, the standard CLAUDE.md sets. The thing to weigh is that CrossWire's own
conf for the same tagging says GPL, though its prose grants use "for any purpose".
Until he rules, nothing built from them is committed: the four files above are
local, and `tests/strongs_test.py` fails if git tracks any of them.

How it reads:
- A tagged entry is the KJV word or phrase exactly as tagged (`"man’s hand"` is one
  entry) with the key of the Hebrew or Greek word it translates. Untagged words, such as
  the translators' italics and most articles, are not listed.
- Psalm titles carry tags too (424 of them). The KJV numbers no title, so they sit beside
  verse 1 as `title_tags`, never inside it. The concordance does not file them
  under verse 1 (the manifest counts them, `psalm_title_tokens_not_filed`); the
  view lists them as `psalm_titles` (`Ps.3`) with their own count. *mizmor*, H4210,
  stands only in titles.
- The tagging is CrossWire's, not checked here against the Hebrew or Greek. Known
  quirk: H853, the untranslatable object marker, appears where the tagger attached it
  to the neighbouring English word.
- Prepositions and particles are rarely tagged: H5921 (*al*) has 48 tags against
  OSHB's 5,757 words, H413 38 against 5,505, H3605 24 against 5,412. Counts for
  such words measure the tagger, not the Bible; the OSHB layer counts the Hebrew.

## 7. What is not claimed yet

- **OSHB's word-level tags in the committed files.** OSHB's lemma and Strong's tagging is
  CC BY 4.0, so it stays local (s.5). Committing it as its own labelled layer, the way
  the OT README's `alternative` describes, is a rights ruling for Adam (rule 6, ADR 0019).
- **The KJV tags are not proofread.** They are CrossWire's, as published.
- **Lemma spelling.** Lemmas are as the OpenScriptures transcriptions give them, not
  Unicode-normalised. Compare with NFC.

## 8. Rights

Strong's 1890 dictionaries are public domain. The Hebrew transcription's XML markup is
CC BY 4.0 (OpenScriptures HebrewLexicon). Carried, with attribution in the manifest:
the PD text fields, and three fields that come from the markup itself, `pos`,
`proper_name` and `lang`, which are CC BY 4.0 (attribution is all CC BY asks). The STEPBible lexicons (CC BY, `redistribute_whole: false`)
contribute **citations only**, never text, so nothing of theirs is redistributed. The
KJV tags: s.6, local until Adam rules. OSHB's tags: s.5, never committed.

## 9. The concordance view

`build/strongs/concordance-view.jsonl` (local, since it carries the KJV tags) is the
page of a printed concordance, one row per used number, built from the other files so
nobody has to join them by hand:

```
{"strongs": "H7462", "lemma": "רָעָה", "translit": "râʻâh", "lang": "hbo",
 "definition": "to tend a flock; i.e. pasture it; ...",
 "lexicons": {"strongs-1890": "strongs-hebrew:H7462", "bdb": ["bdb-hebrew:BDB7994", ...]},
 "kjv": {"occurrences": 172, "verses": ["Gen.4.2", ...],
         "renderings": {"feed": 55, "shepherds": 33, "shepherd": 28, ...}},
 "parallels": {"Ps.23.1": {"vulgate": ["vulgate:Ps.22.1"], "douay": ["douay:Ps.22.1"]}, ...}}
```

- **`kjv.verses`** are the KJV verses whose tagged words carry the number, in canon
  order. Their uids are in `build/strongs/concordance-kjv.jsonl`.
- **`lexicons`** is the number's `witnesses.jsonl` row: citations into Strong's, BDB,
  TBESG, LSJ and Thayer.
- **`parallels`** lists only the verses whose number differs in a parallel Bible. A
  verse not listed is the same verse in each (`vulgate:Gen.1.1`, `douay:Gen.1.1`,
  `brenton:Gen.1.1`). An empty list means that Bible has no verse holding the text
  (Gen 49:32 in the Clementine). The ids come from PR #9's `convert_vulgate`,
  `convert_douay` and `convert_brenton`: each unit's `kjv` target, read backwards,
  through `data/versification/vulgate-kjv.json` and `brenton-kjv.json`. Brenton is the
  Old Testament only, so no New Testament verse lists it.

What the view does not have yet:
- **Thayer.** PR #7's entries (4,940 linked to Strong's) are built from OCR that lives
  only on Adam's machine. The entry links are gitignored, so they are not on any branch.
  The first local build fills the `thayer` lists, and cloud builds keep them after that.
