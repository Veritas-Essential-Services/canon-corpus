# Lane D — Storytellers: digest (2026-10-02 15:32 CDT)

**Queue: all items done.** Nothing failed to fetch. No uids minted, nothing registered in `data/books/manifest.json`, no converter edited.

## Andrew Lang — `pipeline/lang_shelf.json`
- **Held:** 95 Gutenberg books, clean and converted (102,483 paragraph units): all twelve Coloured Fairy Books, the other story books, his fairy tales and novels, the Odyssey (with Butcher), Iliad (with Leaf and Myers), Homeric Hymns, Theocritus, Aucassin, poetry, essays, myth and folklore, histories.
- **Raw OCR:** 29 Internet Archive volumes (Poetical Works 1923 ×4, History of Scotland ×4, Homer and the Epic, Lockhart ×2, Northcote ×2, Maid of France, Prince Charles Edward, St Andrews and more). OCR is 94-99% clean.
- **Pending:** Tales of a Fairy Court (not online anywhere I could find); clean text for the 29 OCR volumes.
- **Excluded:** duplicate transcriptions, selections, and about 25 books by other authors that Lang only edited or introduced (Scott, Dickens, Stevenson and others). Each exclusion gives its reason in the shelf.

## Charles Lamb — `pipeline/lamb_shelf.json`
- **Held:** all 7 volumes of Lucas's *Works of Charles and Mary Lamb* (1903-05). Six come from Gutenberg, clean and converted (22,015 units). Vol. IV (Dramatic Specimens) is raw OCR from Internet Archive. Tales from Shakespeare, Ulysses and Poetry for Children are also held standalone. Beauty and the Beast (attributed to Lamb, with Lang's introduction) is raw OCR.
- The letters now cite by Lucas's number: `LETTER 263A, par. 4`.
- **Pending:** a clean text of Lucas vol. IV, Ainger's edition as a second witness, and Lucas's 1935 Letters (probably still in copyright).

## Fables
None of the earlier fables work is in canon-corpus. I searched every branch. The map marks it "pending: locate". It may be in armarium, wordhoard or the vault.

## For Adam to decide
1. **Minting:** 135 slugs (`lang-*` ×124, `lamb-*` ×11) are waiting for the attended uid pass and manifest registration.
2. **Mrs. Lang:** Leonora Blanche Lang wrote most of the later story books. They sit on Andrew's shelf with her credited. Should she get her own shelf?
3. **Converter:** the new `pipeline/convert_shelf_gutenberg.py` gives some books per-book heading options in their shelf rows. Before the next burn, decide whether those rules move into structure_texts.py's per-book rules (CLAUDE.md rule 2).
4. **The lane is exhausted.** Unless you add authors to `QUEUE-D.json`, the next Lane D worker has only upkeep to do. Natural next storytellers: Grimm, Perrault, Andersen, Aesop. Only add Aesop once the earlier fables work is found.
