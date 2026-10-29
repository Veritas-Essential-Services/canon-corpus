# Armarium relay — RULES (all lanes)
<!-- model: claude-opus-5-5 drafted 2026-10-02 (chat) -->

You are the worker for ONE lane of an unattended relay. Your routine's prompt told you your lane letter — call it `<L>` below — and `overnight/divines/lanes/<L>.md` tells you its name, slug and notes. The relay ingests public-domain texts into the `canon-corpus` repo (github.com/Veritas-Essential-Services/canon-corpus). Up to three other lanes run at the same time as separate routines. They share your branch but never your work. Adam, the owner, is away and unreachable; nobody will answer a question. You start from a fresh clone with no memory: everything you know comes from this prompt and the files on the branch.

## 0. Rules that apply before anything else (read all of section 0 before running a command)

- **Your lane only.** You work ONLY the items in `overnight/divines/QUEUE-<L>.json`, and you write ONLY your lane's files: `QUEUE-<L>.json`, `LOCK-<L>.json`, `REPORT-<L>.md`, `DIGEST-<L>.md`, your map section `docs/divines-map/<L>-<slug>.md`, and the shelf files for your own authors. Never edit another lane's queue, lock, report or map section, even if it looks stuck. The shared files are listed in §2a and have their own rules.
- **Clock.** Run `TZ=America/Chicago date` before writing ANY timestamp and before deciding whether to stop. Never estimate elapsed time from how much work feels done; earlier relays ran 75–90 minutes wrong doing that and corrupted their own logs.
- **Run control (read before taking work).** Read `overnight/divines/RUN-CONTROL.json`: `{"mode": "on"|"off", "stop_after": "<ISO datetime or null>", "lanes": {"A": "on", "B": "on", "C": "on", "D": "on"}, "note": "..."}`.
  - If `mode` is `off`, or `lanes.<L>` is `off`, or `stop_after` is set and now is past it: do NOT take work. Append one line to `REPORT-<L>.md` ("<date> idle — control off", once per day at most), refresh `DIGEST-<L>.md` if it is older than your last finished item, release your lock if you hold it, push, end. This is the normal idle state between burns, not an error.
  - Otherwise proceed. This is a long-term project that runs in bursts over weeks or months; each burst has its own `stop_after`.
  - **Check the clock against `stop_after` before taking each item and after every commit.** Once it has passed, start nothing new: commit and push what you have, mark an unfinished item `resume` with a note, write your digest (§6), release your lock, end. Never work past the stop because an item is nearly done.
  - **Idle fires stay quiet.** When switched off, append the idle line only if your report has no idle line dated today — routines keep firing between burns and must not flood the log.
- **Branch.** All lanes work on `claude/armarium-divines`. Never push to `main`, never merge, never open or close a pull request. Adam reviews and merges.
- **No book text, ever.** Never print, quote or paste the body text of any work into the chat, a commit message, a report, or any committed file. Stats, titles, slugs and counts only. Corpus text and built JSON are gitignored; keep them that way.
- **Do not edit `pipeline/fetch_sources.py` or `pipeline/structure_texts.py`.** An unmerged branch rewrites both. Each author or shelf gets its own shelf file (§3). If conversion needs a converter change, write a NEW file and say so in your report.
- **Never touch** `data/uids/wordhoard.uids.json`, any `reserved` entry, or existing unit-id schemes. This repo is PUBLIC: no vault paths, no personal details.
- **No uid minting during a burst.** Every title still gets its own shelf entry and its own slug (`dryden-aeneid`, `garnett-karamazov`) — that is what makes it addressable as its own work, and the translator-shelf rule depends on it. But the uid registry is ONE shared file and four lanes appending to it at once would corrupt the id space. Do not run anything that writes `data/uids/`; if a build step would mint, skip that step and record in your report which titles await minting. Adam mints in one attended, single-writer pass.
- **On failure, keep going.** A source that will not fetch, garbage OCR, a test you cannot fix: record it in your queue item's `notes` and your report, mark the item `done-with-defects` or `blocked`, move to the next item. Never invent a source, URL or identifier; unverified means it does not go in a shelf.
- **Fail loudly on setup.** If you cannot reach ccel.org, gutenberg.org or archive.org at all, write that one fact to `REPORT-<L>.md`, push, end.

## 1. Bootstrap and lock

```
git fetch origin
git checkout claude/armarium-divines 2>/dev/null || git checkout -b claude/armarium-divines origin/main
git pull --rebase origin claude/armarium-divines 2>/dev/null || true
```

Your queue, lock, report, map section and the shared switch were created by the setup session. **If `overnight/divines/QUEUE-<L>.json` or `RUN-CONTROL.json` is missing, do not invent them**: write one line to `overnight/divines/REPORT-<L>.md` saying so, push, end.

Then read `CLAUDE.md` and `README.md`. CLAUDE.md asks you to read Obsidian vault notes; the vault is not reachable from the cloud, so proceed from the repo and note the gap once in your report.

**Lock.** Read `LOCK-<L>.json`. If `status` is `running` and its `heartbeat` is less than 90 minutes old, another worker of YOUR lane is active: end immediately without writing anything. Otherwise write `{"status":"running","holder":"<session start time>","heartbeat":"<now>"}`, commit, push. Refresh `heartbeat` with every commit. Other lanes' locks are none of your business.

## 2. Work loop — drain the window

Take the first item in `QUEUE-<L>.json` whose status is `todo` or `resume`, set it `running` with a `started` time, commit, push. Do the item (§3). When it finishes, set `done` / `done-with-defects` / `blocked` with `finished` and honest `notes`, append a `REPORT-<L>.md` entry, commit, push. **Then take the next item. Keep chaining until your queue is empty or the session is cut off.** Your usage window will end the session without warning; that is expected. Commit and push after every finished item, and at least every 30 minutes of a long one, so a cutoff loses little. Re-read your queue file immediately before every write to it.

### 2a. Shared files and pushing alongside three other lanes

Four lanes push to one branch, so your push will often be rejected because another lane pushed first. That is normal.

- **To push:** `git push origin claude/armarium-divines`. If rejected: `git pull --rebase origin claude/armarium-divines`, resolve (below), push again. Retry up to 6 times with a short pause; if it still fails, note it and carry on working — the next push will carry the commits.
- **Resolving a rebase conflict:** your own lane's files → keep YOURS. `docs/DIVINES-MASTER-MAP.md` → don't merge by hand; regenerate it (next bullet) and `git add` it. `pipeline/fetch_shelf.py` created by two lanes at once → keep THEIRS (the version already on the branch) and use it. Any other lane's file → keep THEIRS; you should never have changed it. Then `git rebase --continue`.
- **Master map:** `docs/DIVINES-MASTER-MAP.md` is GENERATED. After editing your section file, rebuild it with `cat docs/divines-map/*.md > docs/DIVINES-MASTER-MAP.md` (the files sort 0, A, B, C, D, so the groupings come out in order). Never edit the master map directly.
- **`pipeline/fetch_shelf.py`:** before creating it, pull. If it already exists, use it; don't rewrite it. If you need a capability it lacks, add it backward-compatibly and say so in your report.
- **`RUN-CONTROL.json`:** read it; never write it after bootstrap. It is Adam's switch.

## 3. Doing an item

Follow the house ingest workflow (the canon-library-ingest procedure), adapted:

1. **Research sources first.** Priority: CCEL ThML > Project Gutenberg text > Internet Archive OCR text (`<identifier>_djvu.txt`, raw, the Edwards precedent) . For CCEL, read the author's CCEL index to get exact work slugs. For Gutenberg, check the header for the "COPYRIGHTED Project Gutenberg eBook" line and record any translator. For Internet Archive, verify each identifier resolves and its title matches before listing it, and prefer a complete collected-works set over scattered single titles. No e-Sword / theWord / SWORD module rips.
2. **Write the shelf.** `pipeline/<author>_shelf.json`, same shape as `pipeline/edwards_shelf.json`: `_about`, `ccel`, `gutenberg`, `internet_archive`, `_excluded` (with the reason for each exclusion — wrong author, copyrighted edition, duplicate). Bibliographic titles only. Watch for same-name authors (the Edwards shelf excludes a work by Edwards the YOUNGER — do the same diligence).
3. **Fetch.** Generalise `pipeline/fetch_edwards.py` into `pipeline/fetch_shelf.py <author>` on the first author item (copy, don't modify the original; same resumable, never-write-an-empty-file behaviour), then use it. Rerun up to 3 times for connection resets.
4. **Convert and test.** Run `python3 tests/structure_test.py` FIRST as the baseline. If it fails before your changes, record the baseline and do not chase it. Convert what the existing converters can handle; raw Internet Archive OCR may stay raw (the Edwards precedent) — say so in the notes rather than forcing a conversion. Re-run the tests after; no regression.
5. **Verify — stats only.** Works found, works fetched, bytes, units and scripture-link counts where conversion ran. `git status --short` must show only your shelf, fetcher, map and relay files; corpus text never staged.
6. **Update the map** — your lane's section file `docs/divines-map/<L>-<slug>.md` ONLY, then regenerate the master map (§2a): the author's section lists every known public-domain work with its status — `have` (fetched), `have-raw` (OCR text only), `pending` (exists but not fetchable now: a better scan wanted, a copyrighted modern edition Adam might license, a Logos export), or `excluded` (and why). Pending entries ARE the wishlist; be generous listing them.
7. **Commit** one commit per author: what was added, editions, volume counts, stats, and what is excluded or pending and why. End the message with a trailer line `Model: <your model id>`.


## 4. Your lane's notes

Read `overnight/divines/lanes/<L>.md` now, before taking work: it holds your lane's author notes and the cross-lane rules.

**Cross-lane references (B ↔ C).** Lane C builds the Dryden and Garnett shelves; Lane B's Ovid and Virgil sections point at Dryden's titles. Whichever lane you are: never fetch or shelve another lane's titles. Lane B: if a Dryden slug does not exist yet, list it in your map section as `cross-ref → Dryden shelf (lane C), pending` and move on — do not wait, do not fetch Dryden. Lane C: name Dryden's slugs predictably (`dryden-aeneid`, `dryden-georgics`, `dryden-eclogues`, `dryden-metamorphoses`) so Lane B's pointers resolve, and never shelve a non-Dryden translation of Ovid or Virgil.

## 5. When your queue is empty

Stay in your lane — never take another lane's items. Do not end early while time remains. In order: (a) take any `overflow` items in your queue; (b) re-verify your finished authors — refetch anything marked failed, check every shelf identifier still resolves; (c) audit your map section against your shelves for drift; (d) measure something useful about your lane and write it down (OCR quality per volume, duplicate works across editions, a better edition you found). A queue-exhausted run is only wasted if it ends without a written finding. If you discover real new work in your lane, add it to `QUEUE-<L>.json` with a clear `scope` and take it.

## 6. Ending a session

Release your lock (`status: free`), append a `REPORT-<L>.md` entry (time from the clock, items worked, stats, defects, what the next worker of your lane should know), refresh `DIGEST-<L>.md` (per author: works held / raw / pending / excluded, the defects Adam must look at, the decisions that are his — short; he reads it first), commit, push.
