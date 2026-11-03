# Bloom-only review (2026-10-27)

Adam's ruling, 2026-10-27: no more indiscriminate additions. New acquisitions are
works on the appendix list of Harold Bloom's *The Western Canon* (1994) that are US
public domain. Everything Lane B added in PR #38 (rounds cq-ec) is held back, unmerged,
until Adam has judged it shelf by shelf.

- `2026-10-27-pr38-admissions.json`: the 582 shelves PR #38 adds or extends, each with
  a tier, a lean (keep / Adam's call / cut) and a written case. Adam marks them on the
  Armarium Admissions page (claude.ai artifact); his marks live in that page's
  database, not here.
- `2026-10-27-bloom-checklist.json`: all 1,518 entries of Bloom's list, from Robert
  Teeter's transcription (http://sonic.net/~rteeter/grtbloom.html), checked against
  every `*_shelf.json` and `data/books/manifest.json` on every origin branch, and
  against Project Gutenberg's English catalogue for the gaps.

Matching is by author surname and title words, then corrected by hand for the
Theocratic Age. "Author shelved, title not found by name" is a hint, not a verdict:
many such titles sit inside a collected-works volume. A gap with an English Gutenberg
match is US public domain. A 20th-century gap with no match is probably still in
copyright in the US, where the line is publication before 1931.
