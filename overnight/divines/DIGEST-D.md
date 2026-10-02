# Lane D — Storytellers: digest (2026-10-02 15:47 CDT)

**Queue: all 12 items done.** Seven storytellers were added during the burn at the coordinator's relay of your keep-going wish. **Each one can be vetoed** by deleting its shelf file and map section. Nothing failed to fetch. No uids minted, nothing registered in `data/books/manifest.json`, no converter edited.

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


## Added this burn (veto any)
| Shelf | Held | Raw OCR | Units | Notes |
|---|---|---|---|---|
| `macdonald` | 31 CCEL + 27 Gutenberg | 3 | 102,687 | fantasies, fairy tales, novels, Unspoken Sermons (67 scripture links), poetry |
| `grimm` | Hunt's Household Tales (PG) | 1884 2 vols (Lang intro, Grimms' notes) | 1,769 | cites by tale number: exactly 200 tales + 10 legends |
| `andersen` | 9 Gutenberg | 7 | 12,713 | one slug per translation, translator in each title. **PG 27200's translator is unverified** (probably Paull) |
| `kingsley` | 43 Gutenberg | 0 | 42,788 | everything English on Gutenberg, including sermons |
| `hawthorne` | 4 Gutenberg | 0 | 2,887 | children's books only. **Your call:** widen to his novels and tales? |
| `bulfinch` | 4 Gutenberg | 0 | 7,772 | the three Mythology books held separately |
| `pyle` | 19 Gutenberg | 1 | 24,597 | books he wrote; illustrator-only books excluded. **The Arthur books cite badly** (Book > Part > Chapter nesting) |

All 286 shelf URLs re-checked at the end of the run: all resolve. Every slug appears in the map. Nothing failed, and there are 0 Gutenberg copyright markers.

## Added on relay 3 (veto any)
| Shelf | Held | Raw OCR | Units | Notes |
|---|---|---|---|---|
| `carroll` | 16 Gutenberg | 0 | 14,130 | both Alices (+ Under Ground, Nursery), Sylvie and Bruno, verse, Tangled Tale, logic books. 3 maths works pending: no plain text |
| `kipling` | 5 Gutenberg | 0 | 6,452 | the relay's list only: both Jungle Books, Just So, Puck, Rewards and Fairies. **Your call:** Kim, Captains Courageous, Stalky and the rest are listed as pending |
| `stevenson` | 45 Gutenberg | 0 | 34,834 | everything single-book on Gutenberg, collaborations included. Treasure Island already held. **Your call:** the 23-volume Swanston Edition as a second witness |

## For Adam to decide
1. **Minting:** 135 + 151 = 286 slugs (lang 124, lamb 11, macdonald 61, grimm 3, andersen 16, kingsley 43, hawthorne 4, bulfinch 4, pyle 20) are waiting for the attended uid pass and manifest registration.
2. **Mrs. Lang:** Leonora Blanche Lang wrote most of the later story books. They sit on Andrew's shelf with her credited. Should she get her own shelf?
3. **Converter:** the new `pipeline/convert_shelf_gutenberg.py` gives some books per-book heading options in their shelf rows. Before the next burn, decide whether those rules move into structure_texts.py's per-book rules (CLAUDE.md rule 2).
4. **Nesting-aware converter** wanted for Pyle's Arthur books and Helen of Troy.
5. **The lane is exhausted again.** Unless you add authors to `QUEUE-D.json`, the next Lane D worker has only upkeep to do. Natural next storytellers: Grimm, Perrault, Andersen, Aesop. Only add Aesop once the earlier fables work is found.
