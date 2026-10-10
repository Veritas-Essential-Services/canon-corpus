# Classical reading lists → public-domain ingest

<!-- model: claude-opus-5-5 drafted 2026-10-10 (project thread) -->

Every work on the published reading lists of eight classical-Christian schools and publishers, deduplicated, checked against everything canon-corpus holds on **any** branch, and the missing public-domain titles ingested in batches.

| List | Evidence | How complete |
|---|---|---|
| Classical Conversations (Foundations, Essentials, Challenge A–IV) | CC bookstore bundles + CC's "117 must-read books" | Challenge levels complete; Foundations/Essentials have no literature list |
| Canon Press (Moscow, ID) | the shop catalogue (Canon Classics, Christian Heritage Series, reprints) | complete for pre-1930 titles |
| New Saint Andrews College | 2027 undergraduate catalog; graduate CCS courses | catalog often names authors, not works |
| Logos School | elementary literature list; grade 1–8 reading guides; secondary overview | high-school lists are not public |
| Logos Online School | Integrated Humanities course pages (Omnibus I–VI) + electives | good |
| Bethlehem College & Seminary | 2012–13 and 2026–27 catalogs; faculty posts | partial: no published great-books list exists |
| Memoria Press | grade curriculum sets 1–12, Memoria Academy, Highlands Latin School | good |
| CiRCE Institute | site blocked automated reading; titles came from search summaries of CiRCE pages | weakest: check in a browser before relying on a row |

## Files

- `READING-LISTS.tsv`: one row per work: lists it appears on, status, what is held or where to get it, public-domain note, ingest batch.
- `sources/*.tsv`: the raw rows per list, each with the URL it was read from.

Status values: `held` (on some branch), `ingested` (fetched by this work), `partial`, `missing` (PD, not held), `short` (a story or speech whose source is still to find), `lane` (claimed by a relay lane or another thread), `notpd`, `modern`.

Public domain here means US: published 1930 or earlier (as of 2026). UK terms are noted where an author died after 1955. A translation needs its own PD translator; the modern translations several lists assign (Fagles, Fitzgerald, West) are not PD, and the held PD translations stand in for them.

## Batches

Shelves follow the relay convention (`pipeline/<name>_shelf.json`, `fetch_shelf.py <shelf> --verify --record`, `convert_shelf_gutenberg.py <shelf>`); corpus text and built JSON stay gitignored, and nothing is minted. Shelf names are checked against every branch before each batch; where a relay lane already owns an author's shelf, this work uses a distinct name (`hawthorne-rl`, `stephen-crane`, `rwemerson`).

### Batch 1 (2026-10-10): English and American novels

12 shelves, 27 Gutenberg texts, 51,135 units. Every item passed the identity, rights-line and translator checks (`_checks` recorded in each shelf).

| Shelf | Works |
|---|---|
| `austen` | Pride and Prejudice, Sense and Sensibility, Mansfield Park, Northanger Abbey, Persuasion (Emma already held: `austen-emma`) |
| `defoe` | Robinson Crusoe |
| `dickens` | A Tale of Two Cities, Great Expectations, Oliver Twist, David Copperfield, Bleak House, Hard Times |
| `bronte` | Jane Eyre, Wuthering Heights |
| `hawthorne-rl` | The Scarlet Letter |
| `mshelley` | Frankenstein |
| `douglass` | Narrative of the Life of Frederick Douglass |
| `stephen-crane` | The Red Badge of Courage |
| `thoreau` | Walden, with Civil Disobedience |
| `rwemerson` | Essays, First and Second Series |
| `poe` | Works, Raven Edition, vols 1–5 |
| `marlowe` | Doctor Faustus |

Three books needed a chapter rule because their Contents and body headings differ in case: Great Expectations, The Red Badge of Courage, Frankenstein (Letters and Chapters).

### Batch 2 (2026-10-10): novels and adventure

23 shelves, 43 Gutenberg texts, 75,708 units, all checks passed.

| Shelf | Works |
|---|---|
| `stoker` | Dracula |
| `hardy` | Far from the Madding Crowd |
| `wilkie-collins` | The Woman in White |
| `wilde-novels` | The Picture of Dorian Gray (the fairy tales are Lane D's `wilde-fairy-tales`) |
| `conan-doyle` | A Study in Scarlet, The Sign of the Four, Adventures, Memoirs, The Hound of the Baskervilles, The Return of Sherlock Holmes, The Lost World, The White Company |
| `hgwells` | The Time Machine, The Invisible Man, The War of the Worlds |
| `verne` | Twenty Thousand Leagues under the Sea (the 1872 translation; F. P. Walter's modern one is excluded) |
| `walter-scott` | Ivanhoe, The Talisman |
| `george-eliot` | Silas Marner (Middlemarch already held) |
| `kipling-novels` | Kim, The Man Who Would Be King, Stalky & Co. (children's books are Lane D's `kipling`) |
| `henty` | The Cat of Bubastes, The Dragon and the Raven, Winning His Spurs, By Right of Conquest, In the Reign of Terror, With Lee in Virginia, In the Heart of the Rockies, Redskin and Cow-Boy |
| `orczy` | The Scarlet Pimpernel |
| `john-buchan` | The Thirty-Nine Steps |
| `tennyson` | Idylls of the King |
| `twain-rl` | A Connecticut Yankee, Sketches New and Old (boys' books are the `mark-twain` shelf) |
| `cather` | My Ántonia |
| `tarkington` | Penrod |
| `sabatini` | Scaramouche |
| `terhune` | Lad: A Dog |
| `allen-french` | The Story of Rolf and the Viking's Bow |
| `jane-porter` | The Scottish Chiefs |
| `margery-williams` | The Velveteen Rabbit |
| `dcfisher` | Understood Betsy (US PD; UK until 2029) |

Held back: Conan Doyle's Case-Book (1927) pending a per-story date check.

### Batch 3 (2026-10-10): medieval and church

15 shelves, 18 texts, all checks passed. Fourteen Gutenberg texts are converted (about 31,800 units); the four Internet Archive scans stay raw OCR until someone structures them.

| Shelf | Works |
|---|---|
| `bede` | Ecclesiastical History of England (Sellar, 1907) |
| `kempis` | The Imitation of Christ (Benham) |
| `erasmus` | The Praise of Folly (Wilson, 1668) |
| `marco-polo` | The Travels of Marco Polo, vols 1–2 (Yule, rev. Cordier) |
| `einhard` | Einhard's Life of Charlemagne (Grant, 1905) |
| `old-english-chronicles` | Six Old English Chronicles (Giles), with Geoffrey of Monmouth's History of the Kings of Britain |
| `chretien` | Four Arthurian Romances (Comfort) |
| `petrarch` | The Sonnets, Triumphs, and Other Poems (Bohn) |
| `spenser` | The Faerie Queene, Books I–VII in two volumes (J. C. Smith). PG 6930 is excluded: its header is COPYRIGHTED |
| `hammurabi` | The Oldest Code of Laws in the World (Johns, 1903) |
| `enuma-elish` | The Seven Tablets of Creation, vols 1–2 (L. W. King, 1902; IA) |
| `anselm` | Proslogium, Monologium, Cur Deus Homo (Deane, 1903; IA) |
| `hegel` | Philosophy of Right (Dyde, 1896; IA) |
| `benedict-rule` | The Rule of St. Benedict, Latin and English (Fort Augustus, 1906; IA). PG 50040 (Doyle) is excluded: copyright 1948 |
| `abelard` | Historia Calamitatum (Bellows). The Letters are Lane C's `moncrieff-abelard` |

The Song of Roland is already held on Lane C's `scott-moncrieff` shelf.

### Batch 4 (2026-10-10): American documents and essays

15 shelves, 28 texts, all checks passed. 26 Gutenberg texts are converted (about 25,600 units); Gentz and Bradstreet are Internet Archive scans and stay raw OCR.

| Shelf | Works |
|---|---|
| `american-founding` | The Mayflower Compact, Patrick Henry's Liberty or Death, the Declaration of Independence, the Constitution, the Bill of Rights (The Federalist is already held) |
| `lincoln` | The Papers and Writings of Abraham Lincoln, vols 1–7 (Lapsley, 1905) |
| `franklin` | Autobiography (Pine, 1916) |
| `thomas-paine` | Common Sense; Writings vol. 2, The Rights of Man (Conway). Distinct from Lane D's `albert-paine` |
| `edmund-burke` | Works vol. 3: Reflections on the Revolution in France |
| `gentz` | The Origin and Principles of the American Revolution (J. Q. Adams tr., 1800; IA) |
| `wheatley` | Poems on Various Subjects (1773) |
| `bradstreet` | Works in Prose and Verse (Ellis, 1867; IA) |
| `tocqueville` | Democracy in America, vols 1–2 (Reeve) |
| `stowe` | Uncle Tom's Cabin |
| `whitman` | Leaves of Grass |
| `booker-washington` | Up from Slavery |
| `du-bois` | The Souls of Black Folk |
| `william-james` | The Varieties of Religious Experience; Pragmatism |
| `upton-sinclair` | The Jungle (US PD; UK until 2038) |

Beyond Good and Evil is already held on Lane C's `levy-nietzsche`. Still to find for the founding-documents row: the Articles of Confederation, the Northwest Ordinance, Washington's Farewell Address, and the Clay, Calhoun and Garrison speeches.

### Batch 5 (2026-10-10): poets, philosophy and the 1920s

15 shelves, 29 texts, all checks passed. 27 Gutenberg texts are converted (about 45,000 units); Galileo and Mencken are Internet Archive scans and stay raw OCR. The 1920s books are US public domain only; each shelf's `_about` gives the year its UK copyright ends.

| Shelf | Works |
|---|---|
| `donne-poems` | The Poems of John Donne, vols 1–2 (Grierson, 1912). Lane A's `john-donne` holds the prose and left the poems out |
| `gibbon-rl` | Decline and Fall, vols 2–6 (vol. 1 already held) |
| `rousseau-emile` | Emile (Foxley, 1911). The Discourses are already held with Cole's Social Contract |
| `romantic-poets` | Lyrical Ballads (1798); Keats's Poems 1817, Endymion, Poems 1820; Shelley's Complete Poetical Works; Byron's Childe Harold and Don Juan |
| `freud` | The Interpretation of Dreams (Brill, 1913) |
| `ts-eliot` | Prufrock and Other Observations; The Waste Land |
| `scott-fitzgerald` | The Great Gatsby; Tales of the Jazz Age (with Benjamin Button) |
| `hemingway` | The Sun Also Rises |
| `robert-frost` | New Hampshire (with Stopping by Woods) |
| `thornton-wilder` | The Bridge of San Luis Rey |
| `em-forster` | A Passage to India |
| `war-poets` | Rupert Brooke, Collected Poems; Wilfred Owen, Poems (1920) |
| `macaulay-lays` | Lays of Ancient Rome |
| `galileo` | Dialogues concerning Two New Sciences (Crew and de Salvio, 1914; IA) |
| `mencken` | The American Language (1919; IA) |

Gibbon vols 2–6 needed a chapter rule: their headings are indented and repeat once per chapter part.

### Batch 6 (2026-10-10): children's history and Old English

15 shelves, 23 texts, all checks passed. Seven Gutenberg texts are converted (about 8,000 units); the other 16 are Internet Archive scans and stay raw OCR.

| Shelf | Works |
|---|---|
| `haaren` | Famous Men of the Middle Ages (PG); Famous Men of Greece and of Rome (IA). The 1904 originals, not Memoria's revisions |
| `eggleston` | Stories of Great Americans for Little Americans |
| `guerber-histories` | The Story of the Thirteen Colonies (PG); The Story of the Great Republic (IA). Lane D's `guerber` holds the myth books |
| `church-aeneid` | The Æneid for Boys and Girls (1908; IA). Lane D's `church` holds his other retellings |
| `burt` | Poems Every Child Should Know |
| `lear` | Nonsense Books |
| `eugene-field` | Poems of Childhood |
| `abbott-makers-of-history` | Alexander the Great. Lane D's `jacob-abbott` holds the Rollo books |
| `gregory-seven-laws` | The Seven Laws of Teaching (1886; IA) |
| `dorothy-mills` | The Book of the Ancient World (1923), Greeks (1925), Romans (1927); IA; US PD, UK until 2029 |
| `melville-billy-budd` | Billy Budd, Sailor (Constable, 1924; IA) |
| `malmesbury` | Chronicle of the Kings of England (Giles, 1847; IA) |
| `old-english-poetry` | The Exeter Book, part 1 (Gollancz, 1895); The Riddles of the Exeter Book (Tupper, 1910); The Caedmon Poems (Kennedy, 1916); all IA |
| `old-english-prose` | King Alfred's Boethius (Sedgefield, 1900); Aelfric's Catholic Homilies, part 1 (Thorpe, 1844); IA |
| `basil-padelford` | Plutarch and Basil on poetry, with Basil's Address to Young Men (Padelford, 1902; IA) |

Left to Lane A, whose author shelves they belong on: Finney's Memoirs, Dabney's Stonewall Jackson, Ryle's Thoughts for Young Men, Spurgeon's Lectures to My Students, Perkins's A Reformed Catholic, Beza on the plague.

### Batch 7 (2026-10-10): the last gaps

4 shelves, 6 texts, all checks passed. Chaucer's three volumes are converted (11,501 units); the rest are Internet Archive scans and stay raw OCR.

| Shelf | Works |
|---|---|
| `chaucer-skeat` | Chaucer's Works, ed. Skeat, vols 1–3: Romaunt of the Rose and minor poems; Boethius and Troilus; the House of Fame, Legend of Good Women and Astrolabe |
| `vindiciae` | A Defence of Liberty against Tyrants (Vindiciae contra Tyrannos), the 1689 translation with Laski's introduction (1924) |
| `wanda-gag` | Millions of Cats (1928). A picture book: the scan is the work, and its text is only a pointer |
| `macdonald-documents` | Select Documents Illustrative of the History of the United States, 1776–1861: the Articles of Confederation, the Ordinance of 1787 and more |

Found already held while checking: the Three Forms of Unity (Schaff's Creeds, vol. 3) and the English Lactantius (ANF 7, on PR #11). Whitefield's sermons are left to Lane A with his journals.

What the lists still lack: Bonaventure's Mind's Road to God has no PD English translation found; Augustine's De Ordine and De Quantitate Animae have no PD English found; Washington's Farewell Address and the Clay, Calhoun and Garrison speeches; Bandello's novella and the CC anthology pieces, which need a source per story.
