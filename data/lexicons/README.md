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

## brewer-1894.paras.json.gz

<!-- prov: 2026-10-19 claude-opus-5-5 drafted -->
**Brewer's Dictionary of Phrase and Fable, New and Enlarged Edition of 1894.** Public
domain (Brewer d. 1897). Not a finished dictionary but the WORKING TEXT the converter
reads: the paragraphs `pipeline/extract_brewer.py` takes from Adam's PDF (pinned by its
sha256 in `fetch_sources.py`, `LOCAL_SOURCES`), page by page, furniture dropped.

- Why it is committed: the PDF cannot be fetched, so without this a fresh clone (the
  hosted Armarium's rebuild) could not build Brewer's. Adam's ruling, 2026-10-19: commit
  the working text of public-domain books built from his own files.
- `fetch_sources.py` unpacks it into `data/corpus/lexicons/` and refuses it unless the
  unpacked bytes match the pinned sha256
  `fb9e705796fd0f5dbb0725a6d0c2c74a754d05004a1ec871952152dfecd9ea6a`.
- Reproducible: `extract_brewer.py` writes compact JSON and gzips with `mtime=0`, so the
  same PDF gives the same bytes. 2.8 MB compressed, 8.0 MB unpacked; 60,071 paragraphs.
- Shape: `{source_sha256, pages, toc: [[letter, page]], furniture_lines, paras: [{p, top, lines}]}`.
