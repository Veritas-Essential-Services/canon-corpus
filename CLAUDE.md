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
    python3 tests/structure_test.py          # 60 offline checks (no corpus needed)
    python3 tests/wh_uid_test.py             # 54 identity-layer checks
    python3 pipeline/adjudicate_kjv.py       # KJV census + disagreement classes
    python3 pipeline/build_witnesses.py --check   # THE GATE: must mint 0
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
    python3 pipeline/perseus_catalog.py --fetch        # Perseus Greek+Latin+lexica, shallow clones (~1.1 GB, gitignored)
    python3 pipeline/perseus_survey.py [--check]       # every Perseus edition measured by its own citation scheme; shelves NOTHING
    python3 tests/cts_test.py                          # the CapiTainS reader (pipeline/cts.py)
    python3 tests/lexica_test.py                       # Beta Code, the shareable lexicons, the STEP supplement's rules
    python3 pipeline/lexica.py --candidates [--check]   # the STEP-or-Perseus review candidates (needs the lexicon sources)
    python3 pipeline/versification.py [--fetch|--check] # Septuagint -> KJV map (TVTMS tested against Swete)
    python3 tests/versification_test.py                # the map against known facts of the Greek numbering
    python3 pipeline/review.py status                  # Adam's review sheets: answered / open
    python3 pipeline/review.py apply docs/review/<sheet>.md   # answers -> override rows, rebuild, --check
    python3 pipeline/review.py render --check          # the sheets are what the data renders
    python3 tests/review_test.py                       # review.py end to end, on a temp copy

## Layout
- pipeline/fetch_sources.py — PERSEUS (TEI) + CCEL (ThML) + GUTENBERG (.txt)
  manifests and fetcher; downloads land in data/corpus/ (gitignored)
- pipeline/structure_texts.py — the converters: TEI / ThML / KJV /
  Gutenberg verse–prose–drama → data/books/<slug>.json (gitignored) +
  data/books/manifest.json (committed: checksums, schemes, provenance)
- tests/structure_test.py — offline converter checks, fixtures inline
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
- pipeline/render_reader.py — the reverse-interlinear reader (D5) →
  build/reader/reader.html; test tests/reader_test.py. John's KJV column
  reads the gitignored data/books/kjv.witnesses.json (README-nt-jsonl s.13).
- pipeline/cts.py — reads ANY Perseus (CapiTainS) TEI file by the citation
  scheme it declares (refsDecl), so one converter covers the collection;
  convert_cts() emits the usual {id, ref, text, links[]} with the CTS URN
  in the source block and a CC BY-SA rights block. NOT wired into any shelf:
  data/perseus/survey.jsonl (COMMITTED, facts only, no text) measures all
  2,097 editions for Adam's scope + rights decision (perseus_survey.py).
  convert_tei stays as it is: the three existing Perseus books keep their ids.
- pipeline/export_mnemonicon_pack.py — the hymn JSONL as Mnemonicon import
  files, one per hymn → exports/mnemonicon/ (COMMITTED; PD only, the gate
  refuses anything else). One piece per stanza, a line per clause; ids are
  uuid5 of the passage uid, so a re-import adds nothing. Launch plan C5.

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
(`{osis, ref, versification: "bhs", resolved: false}`) and are NOT resolved to
`kjv:` unit ids. Resolving them needs a versification map; that is its own
piece of work. A labelled hole beats a confident wrong label.

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

### The shareable lexicons, and STEP only for what they lack (Adam, 2026-09-29)

**Ruling:** the public Greek and Latin lexicons are ones that may be shared
whole, and STEPBible is used **only** for entries they lack plus the two
things STEP did that nobody else has: its Septuagint / beyond-Strong's
vocabulary (G6000+) and its splits of one Strong's number into the words it
covers (G0001G α / G0001H ἆ). `pipeline/lexica.py`; sources pinned in
`LEXICONS` (fetch_sources.py); `tests/lexica_test.py`.

| book | source | licence | entries |
|---|---|---|---|
| `lsj-perseus` | Perseus LSJ TEI (Greek in Beta Code → `betacode.py`) | CC BY-SA 4.0 | 116,497; 422,262 quotations kept as CTS-URN links, `resolved: false` |
| `abbott-smith` | translatable-exegetical-tools TEI, carries Strong's numbers | public domain (text and markup, per its README) | 6,153 |
| `lewis-short` | Perseus L&S TEI, the eng2 file (Unicode Greek) | CC BY-SA 4.0 | 51,645; 289,309 CTS-URN links |
| `step-greek-supplement` | STEP TBESG + TFLSJ, a **selection** | CC BY 4.0, `shareable: true`, `subset_of` both | 4,329 of 9,550 keys |

Supplement rules, each frozen as a test: a word counts as missing only when
**neither** STEP spelling is in lsj-perseus or abbott-smith; **one text per
entry**, the TFLSJ body where STEP has both, **unless that body opens on
another headword** (71 do; G0001H ἆ carries ἔα's body), when the brief TBESG
text is used and `lex.step_edition` says so; a relation whose target is left
out points at the public `strongs-greek` entry; each entry links its LSJ and
Abbott-Smith matches. The whole STEP books (`tbesg-greek`, `lsj-greek`) are
unchanged and stay `redistribute_whole: false`.

**Which STEP entries beat ours (2026-09-29).** STEP's TFLSJ is the same LSJ as
`lsj-perseus`, edited: over the 8,331 entries both hold, the median keeps 100% of the
Perseus Greek. `lexica.py --candidates [--check]` finds the 296 where STEP's may be better
(Perseus copy damaged `<*>`, the two texts under 60% overlap, or Perseus has the word only
accent-blind: `betacode.accented_key` tells ἁγνῶς from ἀγνώς, `headword_key` cannot) into
the COMMITTED `data/lexicons/step-preference-candidates.jsonl`; Adam answers
`docs/review/2026-09-29-step-preference.md`; a `step` answer joins the supplement as
`preferred-by-review`, a `perseus` answer never removes what the rules take.

**Enrichment: STEP's usability, built on the open text (2026-09-29).** `lexica.enrich_lsj`
adds to `lsj-perseus` the facts that make STEP's edition easier, using none of STEP's
text: author name and century on 417,383 of 422,751 citations (CLTK TLG canon tables, MIT,
pinned); 4,356 of 4,387 NT citations resolved to their KJV verse id (`kjv:Rom.5.8`); 6,042
Septuagint citations labelled `LXX.Ps.22.1`, versification `lxx`, NOT resolved (LXX
numbering is not the KJV's); Strong's numbers on 8,077 entries from STEP's
number-to-word mapping, matched on the ACCENTED headword and, between homographs, by the
Greek of STEP's text. LSJ cites Jude as `tlg0031.tlg126` and Judges as `tlg0527.tlg009`. An
untagged citation is read from its label only when unmistakable (`Ev.Matt.`, `LXX Ge.`;
never a bare `Ge.`). STEP's own NT references are the answer key, counted every build in
`scheme.enrichment`: 93.5% of ours are also STEP's, and we have 94.3% of STEP's.

**Septuagint -> KJV, verse by verse (2026-09-29).** `pipeline/versification.py` puts
every verse of Swete's Septuagint (First1KGreek TEI, the edition LSJ cites) on its KJV
number using STEPBible's **TVTMS**, the published standard for versification traditions,
the way TVTMS is designed to be used: each row carries TESTS (`Dan.3:97=Last`,
`Gen.6:1>Gen.6:2`) and they are run against Swete itself, then against the KJV. The map is
COMMITTED (`data/versification/lxx-kjv.tsv`, 29,169 rows; `lxx_to_kjv('Ps.22.1')` ->
`Ps.23.1`) so consumers need no sources; `--check` rebuilds it byte-for-byte. Rules learned:
subverse tests are unobservable in an edition printing whole verses and are set aside;
word-count tests only break ties (`soft`); the tests pick the pattern WHATEVER its label
(Swete's Daniel 3 runs to v.100, which TVTMS files under Latin); First1K and LSJ number the
Septuagint's books differently (First1K tlg035 = Psalms of Solomon, LSJ tlg035 = Wisdom), so
Swete's books are matched by title. Checked independently by proper names: where the map
moves a verse, the KJV verse it names shares more names 757 times, the same-number verse 4
(each of the 4 read: known Greek order changes, the map right). `tests/versification_test.py`.
LSJ's Septuagint citations now resolve through it (4,297 of 6,042; 1,480 are to books the
KJV lacks), and every resolved scripture link carries `osis`, the field Armarium indexes.

⚠️ **Armarium does not read `rights` yet.** Its per-book download serves any
book whole, the two STEP books included. The fix belongs in armarium
(refuse `/download/<slug>` when `redistribute_whole` is false).

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
