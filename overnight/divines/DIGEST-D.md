# Lane D — Storytellers: digest (2026-10-02 20:08 CDT)

**Queue: all 100 items done.** Eighty-eight storytellers were added during the burn at the coordinator's relays of your keep-going wish: seven on the second run, seven on the third (Carroll, Kipling, Stevenson, Chesterton's 1926-1928 gaps, Aesop, Nesbit, Potter) and eight on the fourth (Grahame, Barrie, Baum's Oz, Ruskin's Golden River, Wilde's fairy tales, Dickens's Christmas books, Collodi's Pinocchio, Lofting) and five folk-tale shelves on the fifth (Joseph Jacobs, Dasent, Ralston, Perrault, Colum), and the great legends on the sixth (Malory, Beowulf, the Poetic Edda, the Kalevala, Dasent's sagas, Sturluson, Dutt's epics; the Mabinogion was already held by lane C on `guest_shelf.json` and is not duplicated), then twenty in Lane D's own batches under the standing relay: ten folk-tale shelves (Yeats, Hyde, Lady Gregory, Campbell of Islay, Ozaki, Mitford, Steel, Crane, Grinnell, Uncle Remus) and ten children's classics (Burnett, Alcott, Spyri, Sewell, Dodge, Montgomery, Wiggin, Ewing, Molesworth, The Swiss Family Robinson), then seven myth and saints shelves (Alfred J. Church, Guerber, Peabody, the Golden Legend in Caxton's English, Canton, Abbie Farwell Brown, Steedman), then eighteen world folk-tale shelves (Grace James, Griffis, Dayrell, Cronise and Ward, Bleek, Fillmore, Mijatovich, Petrovitch, Frere, Lal Behari Day, Crooke and Rouse, Natesa Sastri, Bain, Pu Songling in Giles's English, Zitkala-Ša, the Eastmans, Busk, Webster) and three pending translations promoted (Thorpe's Eddas, Morris's Volsunga, Kirby's Kalevala) with Yeats's own tales, then ten more children's classics shelves (Milne, Craik, Ingelow, Stockton, Burgess, Lagerlöf, Laboulaye, Hauff, Gatty, Edgeworth). **Each one can be vetoed** by deleting its shelf file and map section. Nothing failed to fetch except three Carroll maths works with no plain-text file. All 512 Lane D shelf URLs (35 shelves) resolve at the end of the sixth run. No uids minted, nothing registered in `data/books/manifest.json`, and `structure_texts.py` / `fetch_sources.py` were not edited (the new options live in `convert_shelf_gutenberg.py` and the new `convert_nested.py`).

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
| `macdonald` | 31 CCEL + 27 Gutenberg | 3 | 102,658 | fantasies, fairy tales, novels, Unspoken Sermons (67 scripture links), poetry |
| `grimm` | Hunt's Household Tales (PG) | 1884 2 vols (Lang intro, Grimms' notes) | 1,769 | cites by tale number: exactly 200 tales + 10 legends |
| `andersen` | 9 Gutenberg | 7 | 12,703 | one slug per translation, translator in each title. **PG 27200's translator is unverified** (probably Paull) |
| `kingsley` | 43 Gutenberg | 0 | 42,788 | everything English on Gutenberg, including sermons |
| `hawthorne` | 4 Gutenberg | 0 | 2,887 | children's books only. **Your call:** widen to his novels and tales? |
| `bulfinch` | 4 Gutenberg | 0 | 7,770 | the three Mythology books held separately |
| `pyle` | 19 Gutenberg | 1 | 24,252 | books he wrote; illustrator-only books excluded. The four Arthur books now cite Book / Part / Chapter (`convert_nested.py`, relay 3), with 0 duplicate ids |

All 286 shelf URLs re-checked at the end of the second run: all resolve. Every slug appears in the map. Nothing failed, and there are 0 Gutenberg copyright markers.

## Added on relay 3 (veto any)
| Shelf | Held | Raw OCR | Units | Notes |
|---|---|---|---|---|
| `carroll` | 16 Gutenberg | 0 | 14,130 | both Alices (+ Under Ground, Nursery), Sylvie and Bruno, verse, Tangled Tale, logic books. 3 maths works pending: no plain text |
| `kipling` | 5 Gutenberg | 0 | 6,451 | the relay's list only: both Jungle Books, Just So, Puck, Rewards and Fairies. **Your call:** Kim, Captains Courageous, Stalky and the rest are listed as pending |
| `stevenson` | 45 Gutenberg | 0 | 34,834 | everything single-book on Gutenberg, collaborations included. Treasure Island already held. **Your call:** the 23-volume Swanston Edition as a second witness |
| `chesterton-gaps` | 0 | 5 | raw OCR | the five 1926-1928 books fetch_sources.py deferred. The 61 already held are untouched. **Your call:** The Thing, Poet and the Lunatics (1929) and the 1930 books are US public domain too |
| `aesop` | 2 Gutenberg | 0 | 768 | Townsend (1867) and Jacobs (1894), one slug each. **Before minting:** reconcile with the earlier fables work, which is not in this repo |
| `nesbit` | 33 Gutenberg | 1 | 48,200 | children's books, retellings, adult novels and verse, all pre-1930; Lays and Legends (1886) as raw OCR |
| `potter` | 21 Gutenberg | 2 | 2,337 | 20 little books plus The Fairy Caravan (US 1929); Pigling Bland and Little Pig Robinson (1930) as raw OCR. Text only, no pictures. US status only: she died in 1943 |

All 413 Lane D shelf URLs (16 shelves) re-checked at the end of the third run: all resolve. Three gap-fill scans added after that check (Potter 2, Nesbit 1) fetched cleanly. Every slug appears in the map. 0 Gutenberg copyright markers. Unit counts for macdonald, andersen, bulfinch and lang moved by a few after the Contents-reader fix (item 4 below).

## Added on relay 4 (veto any)
| Shelf | Held | Raw OCR | Units | Notes |
|---|---|---|---|---|
| `grahame` | 5 Gutenberg | 0 | 2,115 | Wind in the Willows, Golden Age, Dream Days (with The Reluctant Dragon), Pagan Papers, The Headswoman |
| `barrie` | 26 Gutenberg | 0 | 29,025 | Peter Pan (novel, 1928 play, Kensington Gardens), Thrums, Tommy, sketches, plays. UK has a perpetual Peter Pan royalty right; US status only |
| `baum` | 15 Gutenberg | 0 | 18,663 | the 14 Oz novels and Little Wizard Stories, by chapter. **Your call:** his other fantasies and series books are listed as pending |
| `ruskin-golden-river` | 1 Gutenberg | 0 | 248 | The King of the Golden River only (Ginn 1885 with Doyle's pictures), by chapter |
| `wilde-fairy-tales` | 2 Gutenberg | 0 | 1,006 | The Happy Prince and A House of Pomegranates, all nine tales by title |
| `dickens-christmas` | 5 Gutenberg | 0 | 3,689 | the five Christmas books, cited by stave, quarter, chirp, part or Gift |
| `collodi` | 1 Gutenberg | 1 | 1,757 | Pinocchio tr. Della Chiesa (1914) and tr. Murray (1892, raw OCR). A 1916 edition with no named translator is held back |
| `lofting` | 6 Gutenberg | 1 | 5,086 | Dolittle books 1920-1928, Mrs Tubbs, Porridge Poetry; Caravan as raw OCR. Original texts, including the passages revised in 1988 for racist caricature. Circus, Zoo and Garden are pending |

## Added on relay 5 (veto any)
| Shelf | Held | Raw OCR | Units | Notes |
|---|---|---|---|---|
| `jacobs-fairy` | 6 Gutenberg | 0 | 8,226 | English, More English, Celtic, More Celtic and Indian Fairy Tales, plus Europa's Fairy Book (1916). **Your call:** Europa's was not named by the relay; Celtic Folk and Fairy Tales (PG 35862) held back pending a compare |
| `dasent` | 2 Gutenberg | 0 | 5,716 | Popular Tales from the Norse, Tales from the Fjeld, tr. Dasent. The children's selection (PG 64189) and Burnt Njal left out |
| `ralston` | 1 Gutenberg | 0 | 3,465 | Russian Fairy Tales (1873, the US edition of Russian Folk-Tales), tr. Ralston, by chapter and tale. Tibetan Tales (also his) noted for a later batch |
| `perrault` | 3 Gutenberg | 0 | 1,894 | tr. Charles Welsh (1901), Samber rev. Mansion (1922), A. E. Johnson (1921). **Your call:** Lang's Perrault's Popular Tales (PG 33931) is French text, held back; Tales of Passed Times (PG 33511) names no translator, pending |
| `colum` | 7 Gutenberg | 0 | 6,414 | King of Ireland's Son, Odysseus and Tales of Troy, Boy Who Knew What the Birds Said, Boy Apprenticed to an Enchanter, Children of Odin, Golden Fleece, At the Gateways of the Day (all 1916-1924). Three Plays left out as drama |

## §5 lane-wide audit (relay 5) — full write-up in `overnight/divines/AUDIT-D.md`
- **Duplicates:** no source is held twice anywhere in the repo (all 154 shelves and the house manifests checked by Gutenberg number, IA identifier and CCEL id). Measured on the text, about a dozen converted books are reprinted inside another Lane D volume (Kensington Gardens is 89% of The Little White Bird; Rhyme? and Reason? holds the Snark; Lucas's Lamb reprints Tales from Shakespeare; and so on). These are distinct published volumes, so no change was needed. **One real duplicate:** the raw-OCR Hunt Grimm of 1884 (`grimm-hunt-1884-01/02`) is the same translation as the clean `grimm-hunt-household-tales`; it adds only Lang's introduction and Grimm's notes.
- **OCR:** all 54 raw IA volumes scored: 43 A, 11 B, no C or D (word-hit 93-100% against a vocabulary from the clean books). The B grades are verse, Scots, or running heads fused into words. A coarse screen: it finds bad scans, not proofreading.
- **Translators:** **fixed now:** `macdonald-for-the-right` was Franzos's novel, translated by Julie Sutter, with only a MacDonald preface. It has been removed to `_excluded`. **For you:** five Andersen rows (four Gutenberg, one IA) name no translator but were admitted, looser than the hold applied to Collodi and Perrault. Every other translated row names its translator, and no Lane D file carries the COPYRIGHTED marker.

## Added on relay 6 (veto any)
| Shelf | Held | Raw OCR | Units | Notes |
|---|---|---|---|---|
| `malory` | 3 Gutenberg | 0 | 4,737 | Caxton's text (2 vols) and Strachey's Globe edition, by Book and Chapter. Sommer's critical edition not taken. **Your call:** Strachey expurgates; keep both or Caxton only |
| `beowulf` | 4 Gutenberg | 0 | 2,181 | tr. Hall (1892), Morris and Wyatt (1895), Kirtlan (1914), Gummere (1910). Earle and Tinker exist as scans, not taken |
| `poetic-edda` | 1 Gutenberg | 0 | 4,703 | Bellows (1923), each poem's introduction, text and notes apart. Thorpe's 1866 Eddas and Morris's Volsunga Saga noted for a later batch |
| `kalevala` | 1 Gutenberg | 0 | 1,534 | tr. Crawford (1888), by rune. Kirby (1907) noted for a later batch |
| `dasent` (extended) | +1 Gutenberg | +1 | +4,096 | Burnt Njal (1861; 1900 one-volume reprint) by chapter; Gisli the Outlaw (1866) raw OCR |
| `sturluson` | 2 Gutenberg | 0 | 3,554 | Heimskringla (tr. Laing, rev. Anderson 1889; translator identified by collation, the file names none) by saga and chapter; Prose Edda tr. Anderson (1880). **Your call:** accept the collation as the translator record |
| `dutt` | 1 Gutenberg | 1 | 2,072 | Maha-bharata (1898) by book and canto; Ramayana (1899) raw OCR from a Google scan (non-commercial request, as with CCEL) |

## Added in Lane D's own batches (veto any)
| Shelf | Held | Raw OCR | Units | Notes |
|---|---|---|---|---|
| `yeats-folk` | 3 Gutenberg | 0 | 2,829 | Fairy and Folk Tales of the Irish Peasantry, Irish Fairy Tales, The Celtic Twilight. His own stories (Red Hanrahan, The Secret Rose) noted for later |
| `hyde` | 1 Gutenberg | 1 | 1,803 | Legends of Saints and Sinners (1915); Beside the Fire (1890), raw OCR with facing Irish |
| `gregory` | 4 Gutenberg | 1 | 4,694 | Cuchulain of Muirthemne (raw OCR), Gods and Fighting Men, Kiltartan Wonder Book, Visions and Beliefs I-II |
| `campbell-highlands` | 0 | 4 | raw OCR | Popular Tales of the West Highlands (1890 ed.), 4 vols, Gaelic with Campbell's English |
| `ozaki` | 3 Gutenberg | 0 | 3,587 | Japanese Fairy Tales, Warriors of Old Japan, Romances of Old Japan |
| `mitford` | 1 Gutenberg | 0 | 1,630 | Tales of Old Japan (1871), tr. Mitford |
| `steel` | 2 Gutenberg | 0 | 3,888 | Tales of the Punjab (1894), English Fairy Tales (1918) |
| `crane` | 1 Gutenberg | 0 | 1,963 | Italian Popular Tales (1885), tr. Crane, by chapter and tale |
| `grinnell` | 4 Gutenberg | 0 | 3,491 | Pawnee Hero Stories, Blackfoot Lodge Tales, The Punishment of the Stingy, Blackfeet Indian Stories |
| `harris-remus` | 4 Gutenberg | 0 | 5,087 | the Uncle Remus books 1880-1907. **Your call:** real folk tales inside a racist frame and dialect; keep, keep with a reader's note, or drop |
| `burnett` | 7 Gutenberg | 0 | 8,539 | The Secret Garden, A Little Princess and Sara Crewe, Little Lord Fauntleroy, The Lost Prince, Racketty-Packetty House, Little Saint Elizabeth and Other Stories. |
| `alcott` | 9 Gutenberg | 0 | 17,897 | Little Women, Little Men, Jo's Boys, Eight Cousins, Rose in Bloom, An Old-Fashioned Girl, Under the Lilacs, Jack and Jill, Flower Fables. |
| `spyri` | 4 Gutenberg | 0 | 4,227 | Heidi (tr. Marion Edwards, as Gutenberg spells it; and tr. Stork 1915), Moni the Goat-Boy (tr. Dole), Rico and Wiseli (tr. Brooks). Two witnesses of Heidi; Abbott's 1927 translation held back. |
| `sewell` | 1 Gutenberg | 0 | 925 | Black Beauty. |
| `dodge` | 1 Gutenberg | 0 | 2,093 | Hans Brinker. |
| `montgomery` | 13 Gutenberg | 0 | 21,864 | the Anne books through Rilla of Ingleside, both Chronicles of Avonlea, The Story Girl, The Golden Road, Kilmeny, Emily of New Moon, The Blue Castle. Canadian author d. 1942; all 13 published before 1931, so US public domain. |
| `wiggin` | 6 Gutenberg | 0 | 5,387 | Rebecca of Sunnybrook Farm, New Chronicles of Rebecca, The Birds' Christmas Carol, Mother Carey's Chickens, Timothy's Quest, Polly Oliver's Problem. 6 `~2` ids in Timothy's Quest (scene lines repeat). |
| `ewing` | 7 Gutenberg | 0 | 8,842 | Jackanapes and Other Stories, Lob Lie-by-the-Fire with The Brownies, Old-Fashioned Fairy Tales, Jan of the Windmill, Mrs. Overtheway's Remembrances, Six to Sixteen, A Flat Iron for a Farthing. Brownies (16052) and Land of Lost Toys (33880) excluded as contained (84%, 93%) in Lob (62783). |
| `molesworth` | 8 Gutenberg | 0 | 8,042 | The Cuckoo Clock, The Tapestry Room, Carrots, Christmas-Tree Land, Herr Baby, Four Winds Farm, An Enchanted Garden, Rosy. |
| `wyss` | 1 Gutenberg | 0 | 2,544 | The Swiss Family Robinson, tr. W. H. G. Kingston. **Your call:** The Family Robinson Crusoe (PG 72813, the 1814/1816 Godwin English version) names no translator; PG 3836 is marked COPYRIGHTED and is out. |
| `church` | 9 Gutenberg | 0 | 5,770 | The Story of the Iliad, The Story of the Odyssey, Stories from Virgil, Stories from the Greek Tragedians, Stories from Livy, Stories of the Old World, Stories of the Persian Wars, The Faery Queen and Her Knights, Stories of Charlemagne. The Iliad for Boys and Girls (PG 21584) is audio only on Gutenberg. convert_nested.py now applies a level's strip to a folded title_next title too (Odyssey footnotes); the regression check over every nested book shows 0 changed. |
| `guerber` | 7 Gutenberg | 0 | 13,366 | Myths of Greece and Rome, Myths of Northern Lands, Myths of the Norsemen, Legends of the Middle Ages, The Book of the Epic, Legends of Switzerland, Stories of the Wagner Opera. Myths of the Norsemen moves here from the Edda shelf's exclusions. |
| `peabody` | 1 Gutenberg | 0 | 436 | Old Greek Folk Stories Told Anew. |
| `golden-legend` | 0 Gutenberg | 7 | 0 | The Golden Legend in Caxton's English, ed. F. S. Ellis (1900), 7 vols., raw OCR. The saints' lives on this shelf may belong with Lane A; veto or move. |
| `canton` | 1 Gutenberg | 0 | 934 | A Child's Book of Saints. |
| `abbie-brown` | 1 Gutenberg | 0 | 656 | The Book of Saints and Friendly Beasts. |
| `steedman` | 1 Gutenberg | 0 | 732 | In God's Garden. |
| `poetic-edda` | 3 Gutenberg | 0 | 9,018 | Thorpe and Blackwell's Eddas (1906 Norrœna printing) and Magnússon and Morris's Volsunga Saga, added beside Bellows. Two pending translations promoted from the shelf's own exclusions. |
| `kalevala` | 3 Gutenberg | 0 | 4,722 | Kirby's Kalevala (1907, 2 vols.), a second witness beside Crawford. |
| `yeats-folk` | 5 Gutenberg | 0 | 3,129 | The Secret Rose and Stories of Red Hanrahan added: Yeats's own tales on Irish folk material. |
| `grace-james` | 1 Gutenberg | 0 | 1,870 | Japanese Fairy Tales. |
| `griffis` | 1 Gutenberg | 0 | 741 | Japanese Fairy World. |
| `dayrell` | 2 Gutenberg | 0 | 1,287 | Folk Stories from Southern Nigeria, Ikom Folk Stories. |
| `cronise-ward` | 1 Gutenberg | 0 | 1,366 | Cunnie Rabbit, Mr. Spider and the Other Beef. |
| `bleek` | 1 Gutenberg | 0 | 420 | Reynard the Fox in South Africa. |
| `fillmore` | 2 Gutenberg | 0 | 2,996 | Czechoslovak Fairy Tales, The Shoemaker's Apron. |
| `mijatovich` | 1 Gutenberg | 0 | 963 | Serbian Folk-lore (2nd ed. 1899). Serbian Fairy Tales (PG 67191) excluded: 91% contained. |
| `petrovitch` | 1 Gutenberg | 0 | 2,057 | Hero Tales and Legends of the Serbians. 13% shares text with Mijatovich: mint once, two witnesses. |
| `frere` | 1 Gutenberg | 0 | 1,120 | Old Deccan Days (1870 printing). |
| `lal-behari-day` | 1 Gutenberg | 0 | 387 | Folk-Tales of Bengal. |
| `crooke-rouse` | 1 Gutenberg | 0 | 1,395 | The Talking Thrush (1922 reprint). |
| `natesa-sastri` | 1 Gutenberg | 0 | 950 | Tales of the Sun. |
| `bain` | 2 Gutenberg | 0 | 1,335 | Cossack Fairy Tales, Kúnos's Turkish Fairy Tales (1901, with four Roumanian tales). |
| `giles-liaozhai` | 1 Gutenberg | 0 | 1,894 | Strange Stories from a Chinese Studio. |
| `zitkala-sa` | 1 Gutenberg | 0 | 439 | Old Indian Legends. |
| `eastman` | 1 Gutenberg | 0 | 600 | Wigwam Evenings. |
| `busk` | 1 Gutenberg | 0 | 1,411 | Patrañas (1870). |
| `webster-basque` | 1 Gutenberg | 0 | 2,404 | Basque Legends (2nd ed. 1879). |
| `milne` | 5 Gutenberg | 0 | 4,958 | Winnie-the-Pooh, The House at Pooh Corner, When We Were Very Young, Now We Are Six, Once on a Time. **Your call:** US public domain, but in copyright in the UK and EU until 2027; keep, or hold until 2027? |
| `craik` | 3 Gutenberg | 0 | 3,272 | The Little Lame Prince, The Adventures of a Brownie, The Fairy Book. |
| `ingelow` | 2 Gutenberg | 0 | 1,639 | Mopsa the Fairy, Wonder-Box Tales. |
| `stockton` | 3 Gutenberg | 0 | 2,204 | The Bee-Man of Orn, Ting-a-ling, Fanciful Tales (1922). Fanciful Tales is 42% the same text as Bee-Man: mint once. |
| `burgess` | 26 Gutenberg | 0 | 9,353 | 7 Mother West Wind books and 19 Adventures books. |
| `lagerlof` | 2 Gutenberg | 0 | 4,385 | The Wonderful Adventures of Nils, Christ Legends (tr. Howard). |
| `laboulaye` | 1 Gutenberg | 0 | 1,111 | Laboulaye's Fairy Book (tr. Booth). |
| `hauff` | 2 Gutenberg | 0 | 3,126 | Tales of the Caravan, Inn, and Palace (tr. Stowell), Fairy Tales (tr. Weedon). |
| `gatty` | 2 Gutenberg | 0 | 1,626 | Aunt Judy's Tales, The Fairy Godmothers. |
| `edgeworth` | 1 Gutenberg | 0 | 3,828 | The Parent's Assistant. |
| `baldwin` | 6 Gutenberg | 0 | 6,263 | The Story of Siegfried, Old Greek Stories, Hero Tales, Fifty Famous Stories Retold, A Story of the Golden Age, The Sampo. |

## For Adam to decide
1. **Minting:** 699 slugs are waiting for the attended uid pass and manifest registration: 285 from the second run (lang 124, lamb 11, macdonald 60, grimm 3, andersen 16, kingsley 43, hawthorne 4, bulfinch 4, pyle 20), 130 from the third (carroll 16, kipling 5, stevenson 45, chesterton-gaps 5, aesop 2, nesbit 34, potter 23) and 63 from the fourth (grahame 5, barrie 26, baum 15, ruskin-golden-river 1, wilde-fairy-tales 2, dickens-christmas 5, collodi 2, lofting 7) and 19 from the fifth (jacobs-fairy 6, dasent 2, ralston 1, perrault 3, colum 7) and 15 from the sixth (malory 3, beowulf 4, poetic-edda 1, kalevala 1, dasent +2, sturluson 2, dutt 2), 29 from Lane D's folk-tale batch (yeats-folk 3, hyde 2, gregory 5, campbell-highlands 4, ozaki 3, mitford 1, steel 2, crane 1, grinnell 4, harris-remus 4) and 57 from its children's classics batch (burnett 7, alcott 9, spyri 4, sewell 1, dodge 1, montgomery 13, wiggin 6, ewing 7, molesworth 8, wyss 1) and 27 from its myth and saints batch (church 9, guerber 7, peabody 1, golden-legend 7 raw OCR, canton 1, abbie-brown 1, steedman 1) and 27 from its world folk-tale batch (poetic-edda +2, kalevala +2, yeats-folk +2, and one or two on each of the eighteen new shelves) and 47 from its second children's classics batch (milne 5, craik 3, ingelow 2, stockton 3, burgess 26, lagerlof 2, laboulaye 1, hauff 2, gatty 2, edgeworth 1). Petrovitch shares about 200 paragraphs with Mijatovich: mint those once. The audit found passages held in two volumes (reprints, collected editions, Lang's borrowings from Ralston and Samber): mint those once, with two witnesses; the list is in `AUDIT-D.md` §1.
2. **A bug in `structure_texts.py` (not fixed there; that file is not the lane's to edit).** `_contents_key` strips a lower-case roman page number even when nothing separates it from the title, so a Contents title ending in c, i, l, v or x loses those letters ("The Mice in Council" becomes "The Mice in Coun", "The Cock and the Jewel" becomes "...Jewe"), and the body heading is then never matched. Measured over the Lane D texts that have a Contents (266): 99 Contents titles that are real body headings get truncated, and the house rule misses 68 of them in 21 books (for example Alice ch. IV, Pyle's Book of Sir Percival, Grahame's Romance of the Rail). This is a text heuristic. An earlier figure here (1,229 titles in 224 files) wrongly counted prose lines the Contents reader runs on into; it was corrected 2026-10-02. Headings set in capitals are still caught by the ALL-CAPS fallback; title-case ones are lost. `convert_shelf_gutenberg.py`'s lenient reader now has a separator-aware rule; the house rule, which also builds the committed Chesterton and Gutenberg prose books, still has the bug. Fixing it could change those books' unit ids, so it needs your ruling (CLAUDE.md rule 3). The upkeep thread has drafted the fix; run against all 36 CHESTERTON_GUTENBERG books it moves 0 ids (measured here 2026-10-02 at the coordinator's request). A spot-check confirmed the zero: the old and new rules differ in 12 of those books, but 148 of the 149 Chesterton lines they truncate differently are prose run-off, not titles, and the one real title is matched under both rules.
3. **Widen or not:** Kipling beyond the five named books (Kim, Captains Courageous, Stalky and the rest are listed as pending); Hawthorne's novels and tales (still pending your answer); Chesterton's 1929-1930 books (US public domain now, outside the relay's pre-1929 line); the Stevenson Swanston Edition as a second witness; other Aesop versions (Vernon Jones with Chesterton's introduction, Croxall, L'Estrange); Baum's books beyond Oz; Wilde, Ruskin and Dickens beyond the named books; a translator for the 1916 Whitman Pinocchio (PG 16865, held back because it names none); first-printing scans for Lofting's Circus, Zoo and Garden.
4. **Aesop and the earlier fables work:** the earlier work is still not found in this repo. Reconcile before minting the `aesop` slugs.
5. **Mrs. Lang:** Leonora Blanche Lang wrote most of the later story books. They sit on Andrew's shelf with her credited. Should she get her own shelf?
6. **Converter options:** books now carry heading rules in their shelf rows (`chapre`, `chapre_only`, `contents_only`, `levels`, `sub`, `repeat_continues`; on relay 5 `convert_nested.py` levels also took opt-in `strip` and `max`). Decide whether these move into structure_texts.py's per-book rules (CLAUDE.md rule 2) before minting, since the rules decide the unit ids.
7. **Known citation gaps:** Stevenson's Letters cite by recipient plus place-and-date line (Colvin did not number them; 38 still take `~n`); Townsend's Aesop has ten repeated fable titles (`~2`); Helen of Troy (Lang) still needs stanza-aware conversion; Andersen PG 27200's translator is unverified.
8. **The queue is empty again** (after relay 5's folk tales and audit). Unless you add authors to `QUEUE-D.json`, the next Lane D worker has only upkeep to do.
9. **Andersen without translators (audit):** hold back `andersen-fairy-tales-paull`, `-christmas-greeting`, `-o-t`, `-pictures-of-sweden` and `-picture-book-without-pictures` like Collodi's PG 16865 (recommended), keep them with the gap stated, or have each translator identified from the printed edition.
10. **The 1884 Hunt Grimm:** keep the raw-OCR two-volume set for Lang's introduction and the notes (it would be a second witness of the same tales), or drop it as a duplicate of the clean Gutenberg Hunt.
11. **Malory's two texts:** keep Strachey's Globe edition beside Caxton's (it modernises and expurgates; a second witness of the same chapters), or Caxton only.
12. **Heimskringla's translator:** the Gutenberg file names none; it was identified as Laing, revised by Anderson (1889), by collating its preface word for word with IA's scan of that edition and by its notes signed --L. and --Ed. Accept that as the translator record (rights rule, 2026-07-26), or hold the book back until someone reads the printed title page.
