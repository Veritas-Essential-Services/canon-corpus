---
model_log:
  - 2026-07-22 claude-fable-5 drafted (from git trailer; backfilled 2026-09-30)
  - 2026-09-06 claude-opus-5 edited (from git trailer; backfilled 2026-09-30)
  - 2026-09-07 claude-opus-5 edited (from git trailer; backfilled 2026-09-30)
  - 2026-09-26 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
  - 2026-09-27 claude-opus-5-5 edited (from git trailer; backfilled 2026-09-30)
  - 2026-10-19 claude-opus-5-5 edited
  - 2026-10-20 claude-opus-5-5 edited (Aphthonius commands)
fable_review: pending
---
# canon-corpus — rules for AI sessions

<!-- board-protocol -->
## 🔴 Before working this repo — read the board

This repo is one project in a larger estate, and work here has been duplicated
elsewhere before. **Read these in order, before writing code:**

1. **`MindCastleintheCloud/4 - Indexes/MOC — Project Status.md`** — every project's
   declared state against its observed activity, plus the cross-project overlap
   section. **If this project appears in that overlap section, read the project it
   collides with first.**
2. **This project's `_STATUS` note** in the vault, if it has one.
3. **The rest of this file.**

The board is generated from `Claude/Projects/overwatch/seed.yml`. To change what it
says about this project, edit the seed and run:

```
cd ../overwatch && python bin/verify_disk.py --write && python bin/build.py
```

**Before ending a session:** commit here, then update the project's `_STATUS` note
and **bump its `updated:` date** — the board compares that date against what git
actually saw, and an unbumped date surfaces as a contradiction within a fortnight.

## What this is
The shared source + structure layer of the Canon OS (Rings 1–2): manifest-
driven fetchers and the structure_texts converters that turn public-domain
texts into unit-id JSON. Extracted from `patrimonium` 2026-07-22 (its
history up to commit `d33503e` is the pre-extraction acquisitions ledger).
Consumers: **armarium** (sibling repo), patrimonium, and later Memoria and
the Resolver. Owner: Adam — hobbyist; beginner-friendly explanations
appreciated.

The living truth for project state is the Obsidian vault:
`9 - Projects/Armarium/_STATUS — Armarium.md`. Read it first.

## Golden rules
1. **Manifests ARE the collection.** PERSEUS/CCEL/GUTENBERG_EXTRA dicts in
   `pipeline/fetch_sources.py` + `data/books/manifest.json` are committed;
   corpus texts and built JSON are gitignored and rebuildable. Commit
   history is the acquisitions ledger — one commit per acquisition wave.
2. **Never hand-edit a source text.** Fixes live in per-book rules in
   `structure_texts.py` so they rerun on refetch.
3. **The unit id is the CITATION spine** of the whole suite: canonical
   citation ↔ unit id ↔ any edition's page. Do not change existing id
   schemes without a vault ruling; CTS-URN alignment is pending (ids stay
   short, manifest records the URN per edition).
3b. **Identity is separate from the citation, and is the `uid`.**
   `pipeline/wh_uid.py`; the map is `data/uids/wordhoard.uids.json` and is
   COMMITTED — losing it silently renames every identifier in the Word
   Hoard. 🔴 **This repo is PUBLIC.** Private citations (vault note paths,
   Adam's own maxims) never go in it: they live in the house's private
   registry, `wordhoard/data/uids/house.uids.json`, which shares this one id
   space (`WhUidRegistry(..., shared_space=<this file>)`) and lists its uids
   here, bare, under `reserved`. Never delete a `reserved` entry, and never
   save this file with a `wh_uid.py` older than 2026-09-27 — an old one drops
   `reserved` on save. Ruled 2026-09-27. A citation says where to look; a uid says what you will find.
   Citations are unchanged and are not deprecated. A rebuild of existing
   content must mint ZERO (`build_witnesses.py --check`).
   🔴 Normative rules, all of them, in the vault:
   `9 - Projects/Canon OS/HOUSE STYLE — Addressing and Identity (2026-09-18).md`
3c. **A passage may have many WITNESSES; a witness has no identity of its
   own.** `<uid>/<witness>`, e.g. `wh-FXPPV85VPA/kjv.italic`. Two editions
   of one verse are two witnesses, never two passages. Every book declares
   its `reading_of_record`.
4. **Honesty fields are load-bearing.** Every book's `scheme.honesty`
   states its real citation resolution; never pretend precision.
5. **Builds are resumable + atomic** (temp-file + rename; skip finished
   books). Keep it that way — a killed run must never corrupt output.
6. IP posture: host/structure/publish public-domain freely; map facts
   about copyrighted translations, never copy. CCEL asks non-commercial
   use of some prepared editions — check per work before republishing.

## Commands
    python3 pipeline/fetch_sources.py        # fetch everything missing (resumable)
    python3 pipeline/fetch_sources.py --list # show the manifests
    python3 pipeline/structure_texts.py      # build data/books/*.json + manifest
    python3 tests/structure_test.py          # 147 offline checks (no corpus needed)
    python3 tests/json_duplicate_keys_test.py # no committed JSON repeats a key (a git merge can)
    python3 pipeline/extract_brewer.py --pdf P   # Brewer's 1894, from Adam's pinned PDF -> corpus
    python3 tests/wh_uid_test.py             # 67 identity-layer checks
    python3 tests/latin_shelf_uid_test.py    # wave-1 Latin shelf uids (vault; skips when unreachable)
    python3 pipeline/build_versification.py --fetch    # TVTMS + WLC, pinned
    python3 pipeline/build_versification.py --check    # Hebrew->KJV map byte-identical; WLC invariants
    python3 pipeline/build_versification.py --measure  # BDB cites in Hebrew numbering: the evidence
    python3 tests/versification_test.py      # the map, offline
    python3 pipeline/build_vulgate_versification.py --fetch    # TVTMS + the Clementine, pinned
    python3 pipeline/build_vulgate_versification.py --check    # Vulgate->KJV map byte-identical; invariants
    python3 pipeline/build_vulgate_versification.py --measure  # the map vs proper names in both texts
    python3 pipeline/build_vulgate_versification.py --audit-douay  # the map vs the Douay's English
    python3 tests/vulgate_versification_test.py  # the Vulgate map, offline
    python3 pipeline/build_brenton_versification.py --fetch  # TVTMS + Brenton's USFM, pinned
    python3 pipeline/build_brenton_versification.py --check  # Brenton->KJV map byte-identical; invariants
    python3 pipeline/build_brenton_versification.py --audit  # the map vs Brenton's English aligned to the KJV's
    python3 tests/brenton_versification_test.py  # the Brenton map, offline
    python3 pipeline/build_english_versification.py --fetch  # Geneva, Tyndale, YLT, Darby, ASV, pinned
    python3 pipeline/build_english_versification.py --check  # their KJV maps byte-identical; invariants
    python3 pipeline/build_english_versification.py --audit geneva  # verses a nearby KJV verse fits better
    python3 tests/english_versification_test.py  # the five maps, offline
    python3 pipeline/build_parallel_index.py          # data/parallel/kjv-parallel.tsv (needs the built books)
    python3 pipeline/build_parallel_index.py --check  # the index byte-identical
    python3 tests/parallel_index_test.py      # the index vs the committed maps, offline
    python3 pipeline/build_deuterocanon.py          # the deuterocanon's shared key (needs the built books)
    python3 pipeline/build_deuterocanon.py --check  # map + index byte-identical
    python3 pipeline/build_deuterocanon.py --audit  # the weakest pairings, to read
    python3 tests/deuterocanon_test.py        # the deuterocanon map and index, offline
    python3 pipeline/adjudicate_kjv.py       # KJV census + disagreement classes
    python3 pipeline/build_kjv_italic.py     # kjv.complete.json (kjv.italic) from the committed kjv.tsv
    python3 pipeline/build_witnesses.py --check   # THE GATE: must mint 0
    python3 pipeline/build_progym.py --check      # Aphthonius, 3 editions: must mint 0
    python3 pipeline/build_hymn_corpus.py --check # hymns JSONL: mint 0, byte-identical
    python3 tests/hymn_corpus_test.py        # validator for data/hymns/*.jsonl
    python3 pipeline/build_lemma_spine.py --fetch  # Whitaker's WORDS, pinned (D3)
    python3 pipeline/build_lemma_spine.py --check  # lemma files byte-identical
    python3 tests/lemma_spine_test.py        # the Latin lemma spine
    python3 tests/whitaker_tricks_test.py    # WORDS syncope/slury/fixes/tricks/roman/tackons/packons, rule by rule
    python3 pipeline/benchmark_whitaker.py --fetch  # WORDS vs the Clementine Vulgate (text gitignored)
    python3 pipeline/proper_names.py --fetch  # the house proper-names table (Vulgate + Hitchcock, PD)
    python3 pipeline/proper_names.py --check  # names table byte-identical
    python3 tests/proper_names_test.py        # the names table; the house supplement's attestation
    python3 pipeline/build_nt_corpus.py --fetch   # Greek NT pilot: RP2018 + Strong's, pinned
    python3 pipeline/build_nt_corpus.py --check   # NT JSONL: mint 0, byte-identical
    python3 tests/nt_corpus_test.py          # validator for data/nt/*.jsonl
    python3 pipeline/build_nt_corpus.py --survey  # the whole NT measured; writes nothing
    python3 pipeline/export_mnemonicon_pack.py         # hymns -> Mnemonicon import files (C5)
    python3 pipeline/export_mnemonicon_pack.py --check # packs byte-identical
    python3 tests/mnemonicon_pack_test.py              # the packs vs the app's import; the PD gate
    node tests/mnemonicon_pack_browser_test.js         # import into the real page (Playwright, temp copy)
    python3 pipeline/build_poetry.py --fetch           # poetry: fetch the pinned Gutenberg books (GITenberg mirror)
    python3 pipeline/select_treasury.py --fetch        # poetry: the candidate pool -> selections/treasury.jsonl (run before the build)
    python3 pipeline/build_poetry.py                   # AO + heroic addendum + treasury -> catalogs, texts, Mnemonicon packs
    python3 pipeline/build_poetry.py --check           # poetry: mint 0, byte-identical
    python3 tests/poetry_test.py                       # the poetry section: rights gate, ids, packs, cutter
    python3 pipeline/review.py status                  # Adam's review sheets: answered / open
    python3 pipeline/review.py apply docs/review/<sheet>.md   # answers -> override rows, rebuild, --check
    python3 pipeline/review.py render --check          # the sheets are what the data renders
    python3 tests/review_test.py                       # review.py end to end, on a temp copy
    python3 -m unscanner run <slug> [--archive ID | --pdf P --rights WHY]  # a scan re-set (unscanner/README.md)
    python3 -m unscanner run church-odyssey-boys --to-corpus  # ...and structure_texts.py builds from it
    python3 tests/unscanner_test.py                    # 36 offline checks (tesseract optional)
    python3 -m unscanner.restore page*.jp2 --out DIR [--pdf book.pdf]   # paper to white, pictures kept, text layer (pilot)
    python3 -m unscanner.gutenberg HOCR_DIR pg.txt OUT [decisions.json]  # Gutenberg's proofread words onto the OCR boxes
    python3 tests/restore_test.py                      # 14 offline checks (PDF part needs tesseract + pikepdf)
    python3 tests/gutenberg_layer_test.py              # 13 offline checks
    python3 -m unscanner editions collate --scan a=DIR --scan b=DIR --djvu a=XML --djvu b=XML --base a --volume N --out OUT  # several scans -> Proof Desk
    python3 -m unscanner editions merge --collation OUT/collation.json --base-dir DIR --base a --volume N --answers R.json C.json A.json --out OUT  # -> merged text
    python3 tests/editions_test.py                     # columns, running heads, signature marks, margin breaks, dashes (28)
    python3 tests/smallcaps_test.py                    # small caps reread, abbreviations, ll/U, æ (21)
    python3 -m unscanner fixes fetch && python3 -m unscanner fixes build   # the fix library (Guiguts GPL-2, Underwood unlicensed, ICDAR CC BY): local only, gitignored
    python3 -m unscanner fixes profile --book data/unscanner/<slug>      # which fixes this typesetting has in play
    python3 tests/fixes_test.py                        # the fix library's profile on a made-up book (13)
    python3 pipeline/brewer_plates.py --fetch          # Brewer's Character Sketches: 8 vols' manifests, OCR, PDFs (gitignored)
    python3 pipeline/brewer_plates.py [--check]        # -> data/art/brewer-sketches/plates.jsonl, 283 plates with uids (mint 0)
    python3 tests/brewer_plates_test.py                # the plates catalog, offline
    python3 pipeline/build_stories.py [--check]        # Illustrated Classics story layer: scenes + figures -> uids (mint 0)
    python3 tests/stories_test.py                      # data/stories/ and data/art/illustrated-classics/, offline
    python3 pipeline/build_dictionary_links.py --fetch # the dictionaries' edges (+ Character Sketches scans)
    python3 pipeline/build_dictionary_links.py --check # data/dictionaries/ byte-identical
    python3 tests/dictionary_links_test.py             # the edge parsers, offline

## Layout
- pipeline/fetch_sources.py — PERSEUS (TEI) + CCEL (ThML) + GUTENBERG (.txt)
  manifests and fetcher; downloads land in data/corpus/ (gitignored)
- pipeline/structure_texts.py — the converters: TEI / ThML / KJV /
  Gutenberg verse–prose–drama → data/books/<slug>.json (gitignored) +
  data/books/manifest.json (committed: checksums, schemes, provenance)
- tests/structure_test.py — offline converter checks, fixtures inline
- The Clementine Vulgate (1592, PD) — `VULGATE` in fetch_sources.py, pinned
  to a commit of github.com/BibleGet-I-O/Clementine-Vulgate (73 books, one
  sha256 over the files); `convert_vulgate` -> data/books/vulgate.json,
  35,809 verses. Ids are `vulgate:Ps.50.3` in the VULGATE's own numbering
  (Greek Psalm count, titles in verse 1, Greek additions in Dan/Esth): not
  linked to kjv: units, no uids minted. Each verse keeps the project's
  marked-up line as `marked` beside the plain `text`.
- pipeline/build_hymn_corpus.py — Latin hymns → data/hymns/{passages,
  witnesses,tokens,alignments}.jsonl (COMMITTED: the JSONL is the source of
  truth). One row per CLAUSE, joined by uid. Schema:
  pipeline/README-hymn-jsonl.md
- data/hymn-sources/ -- hymns from a printed PD edition (Lauda Sion, Sacris
  solemniis, Verbum supernum, from Britt 1922, every line checked against the
  scan image). No house draft: no prose_order, lemmas only where
  Whitaker leaves no choice, and glosses are Whitaker DICTIONARY glosses by a
  fixed rule (pipeline/whitaker_gloss.py, README s.11; override layer
  data/hymns/gloss-overrides.jsonl). README-hymn-jsonl.md s.9; their cuts and
  lemma flags await Adam in docs/review/2026-09-26-thomas-{cuts,lemma-flags}.md.
  Also here: britt-1922-adoro-te.json, Britt's Adoro te, which the build
  COLLATES against the received text (never replaces it); every difference
  awaits Adam in docs/review/2026-09-26-adoro-collation.md (README s.10)
- pipeline/whitaker.py (+ whitaker_tricks.py) + build_lemma_spine.py — Whitaker's WORDS (Latin
  lemmas, licence `free-grant`, NOT PD) → data/lemmas/whitaker-la/ (hymn
  slice committed; full table gitignored). Rules:
  pipeline/README-lemma-spine.md
- pipeline/build_nt_corpus.py — the Greek NT (Robinson-Pierpont 2018, PD;
  lemmas = Strong's 1890 headword by Robinson's number) → data/nt/ (COMMITTED).
  One row per VERSE on the KJV verse's EXISTING uid: registry opened frozen,
  mints 0. Pilot John 1:1-18. Schema + differences from the hymns:
  pipeline/README-nt-jsonl.md. Glosses: Strong's DICTIONARY glosses by a
  fixed rule (pipeline/strongs_gloss.py, README s.12), not a translation;
  data/nt/gloss-overrides.jsonl is the contextual layer and
  data/nt/prose-order.jsonl the plain line's word order (README s.14). Both
  hold a house DRAFT awaiting Adam's review (docs/review/2026-09-26-john1-drafts.md);
  the reader badges every column built on one.
- pipeline/build_versification.py + versification.py — the OT Hebrew (BHS/WLC)
  -> KJV verse map → data/versification/bhs-kjv.json (COMMITTED; TVTMS CC BY
  4.0, derived subset, checked against the pinned WLC). convert_bdb resolves
  BDB's scripture citations through it.
- pipeline/build_vulgate_versification.py — the Clementine Vulgate -> KJV verse
  map → data/versification/vulgate-kjv.json (COMMITTED; same TVTMS file and
  rights block). TVTMS's tests are RUN against the Clementine to pick the
  column each block follows; HOUSE_ROWS holds the 55 verses no column fits,
  each checked against the Latin (most found by --audit-douay). convert_vulgate
  gives every unit `kjv` (resolved target, or why not); ids stay in Vulgate
  numbering.
- convert_douay — the Douay-Rheims (Challoner; fetch_sources.DOUAY, PD, pinned
  GitHub mirror) → data/books/douay.json (gitignored): the Vulgate's English,
  in its numbering; each unit's `vulgate` and `kjv`. DOUAY_ROWS holds the 49
  verses where this edition breaks verses off the Clementine's (Bar 6:7: it
  prints 6:37 in that slot; Sir 29:16-34 run one behind; Isa 46:11, 2 Sam
  13:38, Ps 150:5 hold the next verse's words); empty padding
  verses in the file are dropped, never given ids.
- Brenton's English Septuagint (1851, PD; fetch_sources.BRENTON: eBible.org's
  USFM zip, pinned in a GitHub mirror) → convert_brenton → data/books/brenton.json
  (gitignored), 28,617 verses in the Greek's OWN numbering: Psalms by the Greek
  count (title = v.1), Jeremiah's chapters in the Greek's order, Nehemiah as
  Ezra 11-23, the Greek's additions lettered (1Kgs.12.24a), text before v.1 as
  v.0. eBible's KJV-numbered NEH duplicate is skipped.
  pipeline/build_brenton_versification.py → data/versification/brenton-kjv.json
  (COMMITTED; same TVTMS file and rights block). Columns are picked by TVTMS's
  hard tests, then by how well Brenton's English agrees with the KJV's (word
  counts are only approximate on a translation). HOUSE_ROWS holds what no
  column fits, each read in both texts (most found by --audit). A lettered
  verse standing in a gap of Brenton's numbers is the KJV verse there only if
  the words agree (Jer 10:9a is NOT 10:10). versification.resolve_brenton.
  No Greek LXX: Rahlfs and CATSS are restricted; Swete awaits a ruling (its
  only machine-readable text is CC BY-SA markup over the PD edition).
- The historic English Bibles: Geneva 1599, Tyndale, Young's (1898), Darby
  (1889), ASV (1901) — fetch_sources.ENGLISH, scrollmapper's JSON of CrossWire
  modules at the Douay's pin, each README read ("License: Public Domain") →
  convert_english → data/books/<slug>.json (gitignored). A CrossWire module sits
  on the KJV's verse GRID: ids are its slots, the Bible's own numbers except
  where it numbers otherwise (the Geneva follows the Hebrew in Num 13, Dan 4,
  Job 39-41...) and the chapter's overflow is merged into its last slot.
  build_english_versification.py → data/versification/<slug>-kjv.json
  (COMMITTED; the house's own reading, PD): each chapter aligned against the
  KJV's English, followed only where it reads clearly better; HOUSE_ROWS for
  swaps (Phil 1:16-17) and what old spelling hides. This Tyndale holds ten
  books only; Darby's "beginningGod" is mended by a per-book rule
  (ENGLISH_RULES). versification.resolve_english. NOT here: Wycliffe (the
  one reachable PD copy, BibleNLP's eBible extract, drops verses where the
  Vulgate's chapters run longer than the Hebrew's), Coverdale and the
  Bishops' (no reachable machine-readable PD source found).
  Candidates for a full-network lane: docs/pending-sources.md.
- pipeline/build_parallel_index.py → data/parallel/kjv-parallel.tsv (COMMITTED,
  generated): one row per KJV verse (with its uid), naming the verse(s) that
  hold its text in the Hebrew (bhs-kjv), the Greek NT (data/nt; the John 1
  pilot on this branch), and each shelf version, in that version's own
  numbering. Read off the committed maps and the built books' `kjv`; no new
  judgement. A version's verse with no KJV verse is in no row. Its rights
  note is data/parallel/README.md: the hebrew, vulgate, douay and brenton
  columns are TVTMS-derived (CC BY 4.0), and so is every Vulgate, Douay and
  Brenton unit's `kjv` (the manifest's `rights.kjv_field` says so). A built
  Bible records its map's sha256 (`scheme.kjv_map_sha256`); structure_texts.py
  rebuilds it when the map changes, so `kjv` never goes stale.
- The deuterocanon's shared key: the KJV's own Apocrypha (fetch_sources.KJVA,
  eBible's Cambridge Paragraph Bible USFM, pinned in a GitHub mirror, rights
  line "Public Domain") → convert_kjva → data/books/kjva.json (gitignored),
  `kjva:Book.c.v`, 5,722 verses; the Rest of Esther renumbered into the KJV's
  10:4-16:24 from eBible's Greek order. pipeline/build_deuterocanon.py aligns
  Brenton and the Douay to it by their English (the Vulgate keyed through the
  Douay, which keeps its numbers) → data/versification/deuterocanon.json +
  data/parallel/deuterocanon-parallel.tsv (COMMITTED; PD, the house's
  reading). HOUSE_ROWS for what the alignment misses (found by --audit
  and by scanning for keys far from their neighbours'). Each unit of those
  books carries `kjva` (versification.resolve_dc). Jerome's Tobit and Judith
  are another recension: keyed only where the words agree. R. H. Charles's
  1913 Apocrypha has a reserved slot (WITNESSES, TSV_COLUMNS): see
  docs/pending-sources.md.
- pipeline/render_reader.py — the reverse-interlinear reader (D5) →
  build/reader/reader.html; test tests/reader_test.py. John's KJV column
  reads the gitignored data/books/kjv.witnesses.json (README-nt-jsonl s.13).
- pipeline/export_mnemonicon_pack.py — the hymn JSONL as Mnemonicon import
  files, one per hymn → exports/mnemonicon/ (COMMITTED; PD only, the gate
  refuses anything else). One piece per stanza, a line per clause; ids are
  uuid5 of the passage uid, so a re-import adds nothing. Launch plan C5.
- pipeline/build_poetry.py — the poetry section (2026-10-06): AmblesideOnline's
  poetry schedule (tag `ao`) and the house's heroic/adventurous/vocational
  addendum (tag `addendum-heroic`, proposals), one row shape, in
  data/poetry/ (COMMITTED: selections, catalogs, texts). Texts are CUT by the
  script from pinned Gutenberg books, never typed; hosted only when US public
  domain, with the reason per poem; everything else links out. Packs in
  exports/mnemonicon/poetry/, ids uuid5 of the poem's wh-uid. Rules and
  schema: data/poetry/README.md.

- unscanner/ — the Unscanner, Phase A (2026-10-16): a scanned PD book -> tesseract hOCR -> layout
  (indent = paragraph, folios and running heads by position, plates from the ink) -> reflowed HTML,
  faithful page HTML in the closest open typeface, EPUB, corpus units, and a review sheet. Rights
  gate first. Working files in data/unscanner/ (gitignored). `--to-corpus` writes
  data/corpus/archive/<slug>.unscanned.json, which structure_texts.py PREFERS over the Archive's djvu
  text for ARCHIVE_PROSE books. Both Church Homers are built from it. Rules: unscanner/README.md.
  Their working text SHIPS (2026-10-19, Adam: commit the working text of PD books built from
  his own files): data/unscanned/<slug>.unscanned.json.gz, declared in SHIPPED_WORKING_TEXT in
  fetch_sources.py, unpacked into data/corpus/archive/ after a sha256 check, so the hosted
  rebuild reads the Unscanner's text, not the djvu. Regenerated 2026-10-19 byte-identical to the
  2026-10-17 build. A new Unscanner book that should reach the host needs an entry there too.

## Sandbox mechanics (inherited from patrimonium — they apply here)
- Do NOT run live git in a mounted/synced folder — copy to /tmp, run git
  there, copy the .git back. `git config core.fileMode false` in fresh copies.
- No detached background jobs; chunk long work into <45 s foreground calls;
  keep scripts resumable.
- Big builds: build to /tmp then copy in (mounted disks are slow; Adam's
  native Windows disk is fast).

## Scaling (decided, don't re-litigate — see vault "Armarium at scale")
Before thousands of books: manifests become CSV, parallel structure
conversion, throttled bulk fetch. The data model itself already scales.

## End every working session
Update the vault _STATUS note (state, one dated log line, next actions)
and commit. A session that doesn't update the status note didn't happen.

## Lexicons — a fourth door (2026-09-06)

Three reference works now ingest through the same converters and the same
output shape: **Strong's Hebrew** (H1–H8674), **Strong's Greek** (G1–G5624),
and the **unabridged Brown-Driver-Briggs** (10,022 entries). Sources are in
`LEXICONS` in `fetch_sources.py`; converters are `convert_strongs_hebrew`,
`convert_strongs_greek`, `convert_bdb`.

**Why they needed no schema change.** A lexicon is not a linear text, but the
unit id was always the citation hub, and for a lexicon the canonical citation
IS the entry number — `strongs-hebrew:H2617`. Cross-references go in
`links[]`, the field the ThML scripRef harvest already fills. Result:
**25,609 cross-references, zero dangling**, and the three books are one
connected graph. Extra lexical fields (lemma, translit, pos, KJV usage) hang
off each unit under `lex` so the `{id, ref, text, links[]}` contract every
other converter emits is untouched.

**Rights (rule 6 / the 2026-07-26 gate).** All three underlying works are
public domain and the rights line of each exact edition was read, not assumed.
The OpenScriptures markup is CC BY 4.0 over PD dictionary text; the BDB repo
states "Public domain document". Recorded per entry in `LEXICONS`.

**What is deliberately NOT claimed (rule 4).** BDB cites scripture in Hebrew
versification, which parts company with the KJV's — most visibly in Psalms,
where a superscription counts as verse 1 and shifts every later verse. So its
**139,125 scripture citations are recorded as the source stated them**
(`{osis, ref, versification: "bhs"}`), and since 2026-10-02 each is resolved
through a Hebrew->KJV map, `data/versification/bhs-kjv.json`
(`pipeline/build_versification.py`): **137,780 carry `target: "kjv:..."`**;
1,345 stay `resolved: false` with a `why` (psalm titles, which the KJV does
not number; references that name no Hebrew verse; NT references). The map is
STEPBible's TVTMS (CC BY 4.0; only the derived OT Hebrew/KJV subset is
committed, `redistribute_whole: false`), and the build refuses to write
unless every one of the WLC's 23,213 verses lands on a KJV unit id. That BDB
really numbers in Hebrew is measured, not assumed (`--measure`): where the
schemes differ, the entry's own word is in the cited Hebrew verse 72% of the
time and in the same-numbered KJV verse 5.5%.

**Thayer's (added 2026-09-06) is the one book here that was OCR'd, not
fetched.** It is PD and scanned (archive.org `greekenglishlexi00grimuoft`,
760pp), but **no machine-readable edition exists** — that scan's own text layer
has **zero Greek codepoints**, every Greek word mangled into Latin (`édris` for
ἐλπίς). Abbott-Smith 1922 fails the same way. Re-OCR'd with `tesseract grc+eng`
at 300 dpi: **552,594 Greek characters recovered**. 744 of 760 pages carry text;
the other 16 were each checked and are the two cloth covers plus 14 blank leaves.

Recipe, if it ever needs redoing (~70 min on 2 cores):

```bash
curl -sL -o thayer.pdf https://archive.org/download/greekenglishlexi00grimuoft/greekenglishlexi00grimuoft.pdf
# grc.traineddata from tesseract-ocr/tessdata_best into your tessdata dir, then per page:
OMP_THREAD_LIMIT=1 tesseract page.png out -l grc+eng --psm 3
```

🔴 **`OMP_THREAD_LIMIT=1` is not optional.** Without it, tesseract's OpenMP
oversubscribes a 2-core box and the same page takes **62 s instead of 10 s** —
for byte-identical output. That one variable is the difference between a
70-minute job and a 4.5-hour one.

**Its unit is the printed page, and that is a deliberate refusal.** Entry
boundaries have to be inferred from OCR and cannot be inferred reliably:
requiring a paragraph break before a Greek headword finds 4,532 entries,
dropping that requirement finds 7,983, and Thayer's really has about 5,600.
Neither is the entry list. So `thayer:p.300` is the unit — exact, checkable
against the scan — with detected headwords carried under `lex.headwords`,
flagged heuristic. Entry segmentation can be refined later against a stable
page-anchored base without re-running the OCR. The text is unproofread OCR and
says so in its honesty field; Greek diacritics are where it errs most.

## Dictionaries of names — the classical and the literary (2026-10-19)

Adam asked for "a classical dictionary and a literary dictionary that are public
domain". Both ingest through `LEXICONS` and `structure_texts.py`, keyed at ENTRY
level, same `{id, ref, text, links[]}` contract, extras under `lex`:

- **`smith-dgrbm`** — Smith, *Dictionary of Greek and Roman Biography and
  Mythology* (London 1848, 1873 printing), Perseus TEI pinned to commit
  `02768b0`. 19,893 entries + 8 sub-entries. The key is **Perseus's xml:id**
  (`smith-dgrbm:abaris-bio-1`), not the headword: Smith has 19 Apolloniuses,
  and Perseus already encoded Smith's cross-references against those ids, so
  they resolve exactly. Printed `[NAME.]` cross-references are resolved by
  headword only when one entry has it (`[X, No. 2]` picks the homonym); the
  rest keep their candidates, `resolved: false`. 43,867 ancient-author
  citations recorded as Perseus normalised them, NOT resolved to passages.
  Text PD; **markup CC BY-SA 4.0 → `redistribute_whole: false`** like every
  Perseus text here, pending Adam's ruling on CC BY-SA wholes.
  Why not Lemprière: Smith is fuller, and the only machine-readable Lemprière
  (PG 68769) expands the printed abbreviations, which lane B holds for Adam.
- **`brewer-character-sketches`** — Brewer, *Character Sketches of Romance,
  Fiction and the Drama*, the revised American edition of **The Reader's
  Handbook**, ed. Marion Harland (Selmar Hess, 1892), PG 11431/58596/20851/58988.
  ~10,200 entries A–Z plus ~4,200 appendix items (authors' works; foreign poems;
  dramas and operas). Vol. I marks headwords in CAPITALS, II–IV in `=bold=`, and
  vol. IV indents every paragraph two spaces from `=Theresa=` on. Brewer's list
  entries (Dying Sayings, Errors of Authors) print their items like headwords;
  they are told apart by the dictionary's own alphabetical order (a longest
  non-decreasing run) and kept in `lex.list_items`. Brewer's *Dictionary of
  Phrase and Fable* has no Gutenberg edition; it came from Adam's PDF as
  `brewer`, below.

**The edges (`pipeline/build_dictionary_links.py` → `data/dictionaries/`, COMMITTED):**
`names.jsonl` (a headword two or more of the three share — a lead, not an
identity), `scripture.jsonl` (Brewer's Bible refs → `kjv:` ids, each verified
against kjv.json), `shakespeare.jsonl` (→ play.act.scene, verified),
`classical.jsonl` (Smith's citations → CTS URNs through `cts-works.json`, whose
every row was read from Perseus's own `__cts__.xml`; the rest are counted in
`summary.json`, not guessed), `pages-brewer-cs.jsonl` (each Character Sketches
entry → printed page and leaf of the 1892 Hess scans at archive.org,
`charactersketche0{1-8}brewuoft`, by aligning headwords with the scans' text
layer). Needs the built books, so run `structure_texts.py` first.

The lane-B shelves `william-smith` and `anthon` hold Smith's other dictionaries
and Anthon as raw IA OCR books; this is the entry-keyed layer, not a duplicate
acquisition.

**Brewer's Dictionary of Phrase and Fable (1894), added 2026-10-19, is the
first lexicon from a file Adam supplied.** No fetchable machine-readable
edition beat it: the archive.org scans of the 1894-95 printings carry OCR
text, while Adam's PDF is a born-digital typeset (2,971pp, htmldoc 2003) —
exact text, no OCR. So it is declared in `LOCAL_SOURCES` in
`fetch_sources.py`, **pinned by sha256**, and `pipeline/extract_brewer.py`
is the recipe from that one file to `data/corpus/lexicons/brewer-1894.paras.json`.
A different PDF is refused. **Its working text is committed** (Adam's ruling
2026-10-19: commit the working text of public-domain books built from his own
files): `data/lexicons/brewer-1894.paras.json.gz`, reproducible byte for byte,
and `fetch_sources.py` unpacks it into `data/corpus/` after checking its pinned
sha256. So a fresh clone — the hosted Armarium's rebuild — builds Brewer's
without the PDF. The PDF itself is kept in the vault,
`9 - Projects/Armarium/sources/`.

**Unlike Thayer's, it is segmented by entry — 17,240 units,
`brewer:<headword-slug>`** (repeats `~2`, `~3` in page order; `ref` is
"Brewer, s.v. X"). The text carries no bold, so a headword is found by rule
(converter docstring): a one-line paragraph, no closing full stop, in its
letter's section, AND on the longest alphabetical run through that section.
The alphabet is what Thayer's OCR could not give: a one-line verse quotation
looks exactly like a headword until it breaks Brewer's order. A line the rule
misses is never dropped — it stays in the entry before it (149 such, counted
in the honesty note). Headwords run into their own first sentence ("Agnus-castus
A shrub…") are split out by `_brewer_run_in` when they fall alphabetically
between their neighbours (490, `lex.run_in`, added 2026-10-22, 17,240 units);
19 that share a found headword's name are left in place so no id moves.

Edges: **2,125 "See" cross-references resolved, zero dangling**; 1,493 more
name nothing that is a headword ("see above", *Notes and Queries*, years) and
are left unlinked. **680 scripture citations** ("Rev. ix. 11") parsed to
`kjv:` ids, ranges kept as `end`, chapters checked against KJV chapter counts
(Psalm 154 and the like refused). Not proofread against the scan; italics
not carried; compound hyphens print as em dashes in this transcription
(first—rate) and are left as printed.

## STEPBible Greek — the one non-PD source, and how the limit is enforced (2026-09-06)

`tbesg-greek` (Abbott-Smith-based brief lexicon, 9,550 entries) and `lsj-greek`
(the **full Liddell-Scott-Jones**, 9,549 entries, 2.8M Greek characters) are
**CC BY 4.0, not public domain** — the only non-PD material in this repo.

**Adam's call, 2026-09-06: collect and use, do not redistribute in whole.** That
is the correct reading of the terms. CC BY *permits* redistribution outright;
STEPBible additionally *asks* that people be pointed at
`github.com/STEPBible` rather than served a mirror, so corrections flow from one
source. The request is not a legal restriction — honoring it is a courtesy that
costs nothing.

**The limit is enforced structurally, not by remembering it.** The source TSVs
land in `data/corpus/` and build to `data/books/*.json`; both are gitignored, so
nothing but the manifest pointer is ever committed. Each built book carries a
`rights` block — `license`, `attribution`, `source_url`,
`redistribute_whole: false` — and `main()` copies it into the committed
manifest, so **a consumer sees the limit without opening the book**. 🔴 Armarium
may quote, cite and link with attribution; it must not serve or ship the whole
lexicon. A test asserts the block survives.

### Three ways to read this file that lose text, and all three are wrong

Measured against the live files; frozen as tests:

- **Column 2 looks like the key. It is a cross-reference TARGET.** Keying on it
  merges Ἀπολλύων (G0623) into Ἀβαδδών (G0003), because Apollyon is "a Name of"
  Abaddon.
- **Column 0 looks like the key. It is not either.** G0001 holds *two different
  words* — the letter α and the interjection ἆ — told apart only by the extended
  suffix (`G0001G` / `G0001H`). Keying on column 0 drops one definition of every
  such pair. The real key is the extended Strong's number opening column 1;
  grouping on it gives one unit per row with zero collisions.
- 🔴 **Stripping HTML tags first throws away 44% of the Greek.** LSJ's hover
  citations live in `title=` attributes and contain the actual quoted ancient
  authors (`ἐπίσταται δ᾽ οὐδ᾽ ἄλφα συλλαβὴν γνῶναι`) — **973,610 Greek
  characters**, the lexicon's evidence base, deleted silently by a one-line
  regex. `_step_body()` pulls them inline first. Retention went 55.9% → 96.1%.

A compound target (`G0473 (G0473+G3739)`) is a key *plus its parts*; reading the
cell as one string manufactured 104 dangling links and lost the parts, which are
the interesting half. 1,318 cross-references now resolve, zero dangling.

### 🔴 A partial build used to delete the ledger

`structure_texts.py`'s `main()` started `manifest = {}` and wrote whatever it
built. A run only sees the sources fetched locally, so **a lexicons-only build
rewrote a 66-book manifest with 3 entries** (caught 2026-09-06 before it was
committed). The manifest IS the collection — rule 1 — so `main()` now seeds
from the committed manifest and updates it. Never let it start empty again.

## Rights check — the gate that was missing (2026-07-26)

`kafka-metamorphosis` (PG 5200) was removed from `pipeline/adler_shelf.json`.
It is the **David Wyllie translation**, whose Gutenberg header reads
`*** This is a COPYRIGHTED Project Gutenberg eBook. ***`. Armarium was serving
it whole and offering it for download with the PG notice stripped.

**Why it got through:** the acquisition run verified AUTHOR and TITLE against the
live PG header. It never read the rights line. An author dead in 1924 tells you
nothing about the person who Englished him in 2002.

**All 68 were re-checked on 2026-07-26** by fetching each PG header and grepping
for the copyright marker. Twelve entries were foreign-language works with no
translator recorded; **eleven are genuinely public domain, and Kafka was the only
copyrighted one.** The translator is now recorded in the `author` field for the
six where PG names one and the shelf did not.

**The standing rule from here:** a title does not enter this shelf until someone
has read the rights line of the exact edition, not the author's dates. Translations
carry their own copyright. When adding a book, check for
`COPYRIGHTED Project Gutenberg` in the header and record the translator in `author`.
