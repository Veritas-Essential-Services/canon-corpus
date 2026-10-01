<!-- prov: 2026-10-01 claude-opus-5-5 drafted -->
# data/lexicons — dictionaries the rooms look words up in

## webster1913.json.gz

**Webster's Revised Unabridged Dictionary, 1913.** Public domain (US, published 1913).
Source text: Project Gutenberg #29765. Parsed by
`vocabularium/wordbook/dictionaries/parse_webster1913.py` (vocabularium `99d2ff0`) to
headword / part of speech / short sense; copied here unchanged in content on 2026-10-01
so the Armarium can serve word lookups (ADR 0020, the recording gate) the same way it
reads books: from the sibling canon-corpus checkout, never from its own repo (armarium
rule 2).

- Shape: `{ "<lowercase headword>": [ { "p": "<part of speech>", "d": "<short sense>" }, … ] }`
- 90,143 headwords.
- sha256 of the uncompressed JSON (sorted keys, compact separators, UTF-8):
  `bbcce71688ef05aaa75fbeee65176c2db778426a2732b7e653197d8b26a52861`
- Committed, not gitignored: like the hymn JSONL it is the source the rooms read. It is
  2.2 MB compressed. To refresh it, re-run the parser above and re-compress with sorted
  keys and `mtime=0` so the bytes are reproducible.
- Honesty: senses are the parser's SHORT sense (the first `Defn:` or numbered sense),
  not the whole entry. Quotations, etymologies and notes are left out by design.
