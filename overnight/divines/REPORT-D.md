# Lane D (Storytellers) — append-only log

## 2026-10-02 15:25 CDT — lang: done
- Vault (CLAUDE.md's board, _STATUS notes) is not reachable from the cloud; worked from the repo only.
- Baseline `tests/structure_test.py`: 64 passed, 0 failed (before and after).
- Sources: Gutenberg catalogue CSV filtered on "Lang, Andrew"; Internet Archive author search (980 records) for books Gutenberg lacks, each id checked (metadata title, date, djvu text present). CCEL: no Lang.
- Shelf `pipeline/lang_shelf.json`: 95 Gutenberg + 29 IA = 124 items; all fetched (60.5 MB), 0 failed, 0 Gutenberg copyright markers.
- Converted the 95 Gutenberg books with the new `pipeline/convert_shelf_gutenberg.py` (imports structure_texts' convert_gutenberg_prose + contents_chapre, modifies nothing): 102,165 units; every book found at least one heading. Verse books go through the prose path (a unit is a stanza). IA OCR left raw.
- Not registered in data/books/manifest.json and NO uids minted: all 124 `lang-*` slugs await the attended minting pass.
- Excluded with reasons in the shelf: duplicate transcriptions, selections, others' books Lang only edited/introduced (Scott, Dickens, Stevenson, Perrault...), multi-author volumes.
- For Adam: "Mrs. Lang" wrote most of the later story books; they sit on this shelf under Lang's editorship with her credited in the title. Decide whether she gets her own shelf.
