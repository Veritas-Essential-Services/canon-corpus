# Bloom gap research brief (read fully)

Context: canon-corpus is a public-domain library ("the Armarium"). The owner, Adam, ruled that new
acquisitions are ONLY works on Harold Bloom's Western Canon appendix list that are in the US PUBLIC
DOMAIN. We matched Bloom's 1,518 entries against our holdings by machine; your chunk file lists the
entries the machine could NOT confirm as held. Status "author" = the author has a shelf but the title
wasn't found by name (often it's inside a collected-works volume, or held under the translator's
shelf name); "none" = nothing found. The 4th column, when present, is a Project Gutenberg candidate.

## Your job, per entry
Decide one verdict and record evidence. Do NOT edit the git repo. Write ONLY your output file.

verdicts:
- "held": we already hold it (find the shelf + row title). Collected works / complete plays / poetical
  works volumes that contain the title count as held. Say which.
- "add": not held, and a US public-domain ENGLISH edition is available as text: a Project Gutenberg
  ebook (PG only hosts US-PD works, but still check the translator/date), or an Internet Archive scan
  with an OCR text layer (`<id>_djvu.txt`) whose title page you have READ and that was published
  before 1931. Give the best one or two sources (prefer a clean Gutenberg text; prefer complete
  editions; prefer the standard/classic translation).
- "not_pd": the work (or every English translation of it) was first published 1931 or later.
  For foreign works, the TRANSLATION's date governs: a 1920 novel first Englished in 1955 is not_pd.
- "no_source": PD in principle but no usable English text found on PG or IA. Say what you searched.
- "unclear": you can't settle it; say why.

## Rules (Adam's, non-negotiable)
- US public domain is the only rights test: published before 1931 (1930 and earlier is PD as of 2026).
  UK/EU copyright does not matter.
- Translations carry their own copyright: read who translated it and when.
- NEVER fabricate an imprint, year, translator or identifier. Write a year only if you read it on
  a title page / PG header / IA metadata, and say which. If you didn't read it, say "unread".
- For IA items, the scan date is not the publication date; read the title page or printing line in
  the djvu text (first few thousand chars) and check for a later reprint ("copyright 1935", "reprinted
  1946" means the scan is of a later printing, which is fine ONLY if the text is unrevised and the
  first edition is pre-1931; say so). Lending-library (inlibrary/printdisabled) items: skip them.
- Bloom's generic titles ("Poems", "Plays", "Selected Poems", "Stories"): pick ONE good collected edition.
- Do not suggest works Bloom didn't list. Do not suggest commentary about the work.
- For 20th-century authors, screen fast: if the work was first published 1931 or later, it's not_pd;
  one line of evidence (a year you know with confidence, e.g. "Brave New World, 1932") is enough for
  not_pd. Spend effort where the answer could be "add".

## Tools (paths absolute; run from any dir)
B=/tmp/claude-0/-home-user-canon-corpus/e2b3c735-11ff-534b-9d5b-21a3d720dd05/scratchpad/bloom
- Held check (every shelf on every branch + built books): `cd $B && python3 gt.py "REGEX" ["REGEX"..]`
  (case-insensitive regex over row titles and slugs; prints branch, shelf, title). Try title words,
  the author's name, and the translator's name; titles are often stored as e.g. "Works, vol. 3".
- Gutenberg catalogue: `cd $B && python3 gpg.py "REGEX" ["REGEX"..]` (all regexes must match title|authors).
- Gutenberg header (translator, rights): `curl -sL https://www.gutenberg.org/cache/epub/<ID>/pg<ID>.txt | head -80`
- Internet Archive search: `curl -s 'https://archive.org/advancedsearch.php?q=QUERY&fl[]=identifier&fl[]=title&fl[]=date&fl[]=creator&fl[]=language&rows=50&output=json'`
  e.g. q=title:(prison love) AND mediatype:texts AND date:[1500-01-01 TO 1930-12-31]
- IA files (need a *_djvu.txt): `curl -s https://archive.org/metadata/<id>/files | python3 -c "import json,sys;[print(f['name']) for f in json.load(sys.stdin)['result'] if f['name'].endswith('.txt')]"`
- IA text (title page): `curl -sL https://archive.org/download/<id>/<id>_djvu.txt | head -c 4000`
- IA metadata (collection: skip if 'inlibrary' or 'printdisabled' or 'lendinglibrary'): `curl -s https://archive.org/metadata/<id>/metadata`
Network goes through a proxy; if a request fails, retry once after a few seconds.

## Output
Append one JSON object per line (JSONL) to your output file, one line per entry in your chunk, keyed
by the entry number n (first column of the indented lines). Fields:
{"n": 123, "author": "...", "title": "...", "verdict": "held|add|not_pd|no_source|unclear",
 "held_where": "shelf: row title (branch)" or "",
 "sources": [{"kind": "pg"|"ia", "id": "...", "title": "as printed", "translator": "... or ''",
              "year": "1891 (title page)" or "unread", "djvu": "<file name if not <id>_djvu.txt>" or "",
              "evidence": "what you read"}],
 "case": "one or two plain sentences: why this belongs (Bloom lists it) and which edition and why",
 "note": "anything Adam should know (doubts, alternatives, reprints)"}
Write the line as soon as you settle each entry (so partial work survives). When done, reply with
counts per verdict and the 5 most notable findings. Keep going until every entry in your chunk has a line.
