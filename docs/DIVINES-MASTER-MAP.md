# Armarium master map

The HOME OF RECORD for the whole collection: one checklist, four groupings — Divines, Classical (English translations), Translator shelves, Storytellers. Author sections list works; a translator shelf lists titles each with its own uid, which author sections cross-reference (never duplicated).
Status: have · have-raw (OCR text only) · pending (wanted, not fetchable yet — this is the wishlist) · excluded (with reason) · see hymn manifest.
Shelves: pipeline/<author>_shelf.json. Relay files: overnight/divines/. This file is GENERATED from docs/divines-map/*.md — edit the lane section files, never this file by hand.

# Divines

## Jonathan Edwards

Shelf: `pipeline/edwards_shelf.json` (built 2026-09-28; gap audit 2026-10-02). Before the audit it held all of CCEL (7), 2 Gutenberg and 31 Internet Archive items: the Dwight (1829-30, 10 vols) and Worcester (1808-09, 8 vols) Works and early printings. The Yale edition (1957-2008) is in copyright and private only.

| Work | Status | Where |
|---|---|---|
| Works, Hickman ed. (1834), vols 1-2; Religious Affections; Freedom of the Will; Sermons; Treatise on Grace; Essay on the Trinity | have | CCEL |
| Selected Sermons (Gardiner, 1904); Life of David Brainerd | have | Gutenberg 34632, 65066 |
| Works, Dwight ed. (10 vols) and Worcester ed. (8 vols) | have-raw | IA |
| Grosart's Selections (1865); Charity and Its Fruits (1852); Observations on the Trinity (Smyth, 1880); Essay on the Trinity (Fisher, 1903) | have-raw | IA |
| Early printings: Some Thoughts (1742); Humble Inquiry (1749); Original Sin (1758); Two Dissertations (1765); History of Redemption (1774); sermon volumes (1780, 1788, 1789, 1795) | have-raw | IA |
| **Added by the gap audit:** Religious Affections, first edition (1746) | have-raw | IA `treatiseconcerni1746edwa` |
| **Added:** An Account of the Life of David Brainerd, Edwards's own edition (1749) | have-raw | IA `accountoflaterev00edwa` |
| **Added:** Freedom of the Will, London 1762 (earliest printing found) | have-raw | IA `carefulstrictenq1762edwa` |
| **Added:** Miscellaneous Observations (ed. Erskine, 1793); Remarks on Important Theological Controversies (ed. Erskine, 1796) | have-raw | IA (ECCO scans; long-s OCR is poor) |
| **Added:** Samuel Hopkins, Life and Character of Jonathan Edwards (1804 printing) | have-raw | IA, about Edwards |
| Distinguishing Marks (1742 printing); Humble Attempt, first edition (1747) | have-raw | IA scans that name Edwards (`edwards-distinguishing-marks-1742`, `edwards-humble-attempt-1747`) |
| Distinguishing Marks, first edition (1741) | pending | ECCO scan found; its OCR never yields Edwards's name, so the fetcher refuses it until checked by eye |
| Freedom of the Will, first edition (Boston, 1754) | pending | not found on IA |
| Works, 4 vols (New York, 1868, "with valuable additions") | pending | vols 2-4 on IA, vol. 1 not found; the additions not yet identified |
| Clean text of everything held raw | pending | wishlist |
| Images or Shadows of Divine Things; the Miscellanies; full Notes on Scripture | excluded | first printed by Yale from 1948: in copyright, private shelf only |
| Observations on the Language of the Muhhekaneew Indians | excluded | by Jonathan Edwards the YOUNGER |

## John Flavel

Shelf: `pipeline/flavel_shelf.json` (2026-10-02). Base edition: *The Whole Works of John Flavel*, London: Baynes, 1820, 6 vols, Internet Archive OCR (raw). Placement of works in volumes below is from running-title counts in the OCR, not a printed contents page.

| Work | Status | Where |
|---|---|---|
| The Whole Works (1820), vols 1-6 | have-raw | IA `wholeworksofjohn01flav`..`06flav`, slugs `flavel-works-1820-01`..`06` (1.8 million words) |
| The Fountain of Life Opened | have | CCEL `flavel-fountain` (fetch_sources.py); also 1820 vol. 1 |
| Christ Altogether Lovely (sermon from the Fountain) | have | CCEL `flavel-lovely` |
| The Method of Grace | have | CCEL `flavel-grace`; also 1820 vol. 2 |
| Pneumatologia: A Treatise of the Soul of Man | have | CCEL `flavel-pneumatologia`; also 1820 vols 2-3 |
| A Saint Indeed (Keeping the Heart) | have | CCEL `flavel-saint-indeed`; also 1820 vol. 5 |
| The Life of the late Rev. Mr. John Flavel (anon. memoir) | have | CCEL `flavel-life`; also 1820 vol. 1 |
| The Righteous Man's Refuge; A Blow at the Root; Gospel Unity | have-raw | 1820 vol. 3 |
| England's Duty (Christ Knocking at the Door); Divine Conduct, or the Mystery of Providence; Antipharmacum Saluberrimum; Mount Pisgah; Tidings from Rome | have-raw | 1820 vol. 4 |
| A Token for Mourners; The Touchstone of Sincerity; Husbandry Spiritualized; Navigation Spiritualized; The Seaman's Catechism | have-raw | 1820 vol. 5 |
| Exposition of the Assembly's Shorter Catechism; Sacramental Meditations; The Balm of the Covenant; The Reasonableness of Personal Reformation; Preparation for Sufferings; the Coronation sermon | have-raw | 1820 vol. 6 |
| Planelogia (A Succinct and Seasonable Discourse); Vindiciae Legis et Foederis | have-raw | 1820 vol. 3 (located 2026-10-02 by running-title counts) |
| Clean text of the works held only as raw OCR | pending | wishlist: a proofread transcription or a CCEL edition of each |
| Second scan of the 1820 Works (U. Toronto) | pending | IA `wholeworkstowhic01flavuoft`..`06`, for repairing bad OCR pages |
| Whole Works, 1701 / 1716 / 1762 / 1770 / 1799 editions | pending | IA (ECCO and Google scans), listed under `_alternates` in the shelf |
| Mineachadh air Suipeir an Tighearna (Gaelic, 1879) | pending | IA `mineachadhairsui1879flav`; PD, not English |
| Modern reprints (1930-2017: Banner of Truth, etc.) | excluded | editorial matter may be in copyright; the texts are in the 1820 set |
| Same-name authors (Flavel Shurtleff, Flavel S. Mines, J. F. Mines, D. F. Jamison, F. B. Tiffany, J. F. Curwen, J. F. Bliss) | excluded | not John Flavel the divine |

## John Bunyan

Shelf: `pipeline/bunyan_shelf.json` (2026-10-02). Base edition: *The Works of John Bunyan*, ed. George Offor (Glasgow: Blackie, 1854), 3 vols, as Project Gutenberg clean text (PG 6046-6048; 12.3 MB, 2.2 million words). Offor is the fullest pre-modern collected edition. Vol. 1-2: experimental, doctrinal and practical works; vol. 3: allegorical, figurative and symbolical works. Placements below come from title counts in the text, not a printed contents page.

| Work | Status | Where |
|---|---|---|
| The Works, ed. Offor (1854), vols 1-3 | have | PG 6046-6048, slugs `bunyan-offor-01`..`03` (clean text, not yet structured) |
| The Pilgrim's Progress | have | CCEL `bunyan-pilgrim` (fetch_sources.py); also Offor vol. 3 |
| The Holy War | have | CCEL `bunyan-holy_war` (fetch_sources.py); also Offor vol. 3 |
| Grace Abounding to the Chief of Sinners | have | CCEL `bunyan-grace-abounding`; also Offor vol. 1 |
| The Life and Death of Mr. Badman | have | CCEL `bunyan-badman`; also Offor vol. 3 |
| Miscellaneous Pieces | have | CCEL `bunyan-miscellaneous` and PG 3613 `bunyan-miscellaneous-pieces-pg` (likely the same pieces twice; compare before minting) |
| The Jerusalem Sinner Saved | have | PG 3270 `bunyan-jerusalem-sinner`; also Offor vol. 1 |
| The Pharisee and the Publican | have | PG 3548 `bunyan-pharisee-publican`; also Offor vol. 2 |
| The Heavenly Footman | have | PG 13750 `bunyan-heavenly-footman`; also Offor |
| An Exhortation to Peace and Unity | have | PG 3614 `bunyan-exhortation-peace`. Attribution to Bunyan is doubted by modern scholars; Offor printed it. Adam's call whether it is shelved as Bunyan |
| Doctrinal and practical treatises: The Work of Jesus Christ as an Advocate; The Intercession of Christ; Come and Welcome to Jesus Christ; The Greatness of the Soul; The Strait Gate; The Doctrine of the Law and Grace Unfolded; I Will Pray with the Spirit; Christian Behaviour; A Treatise of the Fear of God; Justification by an Imputed Righteousness; Light for Them That Sit in Darkness; Christ a Complete Saviour; The Acceptable Sacrifice; A Few Sighs from Hell; Israel's Hope Encouraged; The Desire of the Righteous Granted; Saints' Privilege and Profit; Paul's Departure and Crown | have (in Offor) | Offor vols 1-2 |
| Controversial and confessional pieces: The Resurrection of the Dead; A Confession of My Faith; Differences in Judgment about Water Baptism; Peaceable Principles and True; A Defence of the Doctrine of Justification; Some Gospel Truths Opened; Instruction for the Ignorant; A Holy Life the Beauty of Christianity; Seasonable Counsel; Of Antichrist and His Ruin; Exposition of Genesis 1-10; Of the Law and a Christian; The Trinity and a Christian | have (in Offor) | Offor vol. 2 |
| Allegorical and symbolic works: Solomon's Temple Spiritualized; The House of the Forest of Lebanon; The Holy City; The Water of Life; The Barren Fig Tree; A Book for Boys and Girls (Divine Emblems); One Thing Is Needful; Ebal and Gerizzim; Prison Meditations | have (in Offor) | Offor vol. 3 (some in vol. 1) |
| A Relation of the Imprisonment of Mr. John Bunyan | have (in Offor, to confirm) | Offor vol. 1 has one reference under the wording 'relation of my imprisonment' |
| Profitable Meditations (1661); A Vindication of Some Gospel Truths Opened; A Map Shewing the Order and Causes of Salvation | pending | not found under these titles in the Offor text (rechecked 2026-10-02); the Map is a broadsheet diagram |
| Each Offor work as its own structured unit | pending | wishlist: a converter that splits Offor at its treatise headings |
| The Entire Works, ed. Stebbing (1862, 4 vols) | pending | IA `entireworksofjoh01buny`..`04buny`, second collected edition |
| Works, 1692 first collected (Doe) and 1771 sixth ed. (8 vols) | pending | IA scans of early printings, listed in shelf `_alternates` |
| The Riches of Bunyan (Chaplin, 1850) | excluded | an anthology of extracts, not a Bunyan work |
| Pilgrim's Progress in words of one syllable; children's versions | excluded | not Bunyan's text |
| Oxford *Miscellaneous Works* (1976-94); 1968 and 2006 reprints | excluded | in copyright or carrying modern matter |
| German, Dutch, Finnish translations on Gutenberg | excluded | not English |

## J.C. Ryle

Shelf: `pipeline/ryle_shelf.json` (2026-10-02). Ryle died 1900: works printed in his lifetime are public domain; posthumous printings before 1931 are marked. No single collected edition exists, so the shelf is title by title. *Expository Thoughts on the Gospels* (7 vols) is assembled from single volumes of lifetime printings, each identified by the chapter range of its own section headings.

| Work | Status | Where |
|---|---|---|
| Holiness | have | CCEL `ryle-holiness` |
| The Upper Room | have | CCEL `ryle-upper-room` |
| Expository Thoughts: Matthew | have | CCEL `ryle-et-matthew` |
| Expository Thoughts: Mark (1863) | have-raw | IA `saintmark0000ryle` |
| Expository Thoughts: Luke 1-10 / Luke 11-24 (1862) | have-raw | IA `expositorythoug06rylegoog`, `saintluke0002ryle` |
| Expository Thoughts: John 1-6 (1866) / 7-12 / 13-21 | have-raw | IA `saintjohn0000ryle`, `expositorythough06ryle`, `expositorythough07ryle` |
| Practical Religion | have | Gutenberg 38162 |
| The Cross: A Tract for the Times | have | Gutenberg 62001 |
| A Sketch of the Life and Labors of George Whitefield | have | Gutenberg 34727 |
| Knots Untied (1885); Old Paths (1878) | have-raw | IA |
| The Christian Leaders of the Last Century (1869); Bishops and Clergy of Other Days (1868); Facts and Men (1882); Light from Old Times (1902 printing of 1890); The Priest, the Puritan, and the Preacher (1856) | have-raw | IA |
| Principles for Churchmen (1900 printing of 1884); The Lessons of English Church History (1903-04 printing); What Good Will It Do? (1872) | have-raw | IA |
| Home Truths, three series (1854, 1857, 1859 printings; which series each is awaits confirmation) | have-raw | IA |
| Living or Dead? (1852); Startling Questions (1853) | have-raw | IA (collections of tracts; overlap with Home Truths likely) |
| The Christian Race (1900, posthumous); The Two Bears (1869); How Should a Child Be Trained? (1910s printing) | have-raw | IA |
| Bible Inspiration (1877); Thoughts on Immortality (1883); Simplicity in Preaching (1882) | have-raw | IA |
| Tracts: What Time Is It?; Have You the Spirit?; Rich and Poor; What Is Your Hope?; No More Crying; Only One Way; Are You Forgiven?; Occupy Till I Come; Do You Pray? | have-raw | IA, one slug each |
| A Call to Prayer (1860) | have-raw | IA `a-call-to-prayer` (a second scan that does name Ryle) |
| Worldly Conformity (1878) | pending | IA scan found, but the text never names Ryle (title page lost); held back under `_pending` until checked by eye |
| Coming Events and Present Duties; Shall We Know One Another?; Thoughts for Young Men; Duties of Parents; Charges and Addresses | pending | lifetime works not yet found as a verified PD scan (some are inside the Home Truths series) |
| Clean text of everything held raw | pending | wishlist: proofread transcriptions |
| Hymns for the Church on Earth; Spiritual Songs for a Month | see hymn manifest | hymnals Ryle compiled |
| The Sabbath (Gutenberg 48182) | excluded | by Andrew Thomson; Ryle only contributes |
| Modern reprints and 'modernised' editions (1927 on: Banner of Truth, Evangelical Press, Daily Readings, etc.) | excluded | possibly in copyright |
| French, Spanish, Italian, Swedish translations | excluded | not English |
| Same-name authors (John A. Ryle MD, James Ryle, Gilbert Ryle, John Ryle Wood and others) | excluded | not J.C. Ryle |

## Horatius Bonar

Shelf: `pipeline/horatius-bonar_shelf.json` (2026-10-02). Prose only: his hymns and poems belong to the hymn manifest. All lifetime printings (he died 1889). Internet Archive OCR is raw.

| Work | Status | Where |
|---|---|---|
| God's Way of Peace | have | CCEL `hbonar-gods-way-of-peace` |
| The Rent Veil | have | CCEL `hbonar-rent-veil` |
| Follow the Lamb (1874); Words to Winners of Souls (1860); Words of Peace and Welcome (1860) | have-raw | IA |
| The Everlasting Righteousness (1873); The Christ of God (1874); The Blood of the Cross (1858) | have-raw | IA |
| The Night of Weeping (1852); The Morning of Joy (1856) | have-raw | IA |
| Family Sermons (1863); Truth and Error (1851) | have-raw | IA |
| Prophetical Landmarks (1847); The Coming and Kingdom of the Lord Jesus Christ (1849) | have-raw | IA |
| The Desert of Sinai (1857); The Land of Promise (1858); Days and Nights in the East (1866) | have-raw | IA |
| Earth's Morning (1875) | have-raw | IA |
| Life of John Milne of Perth (1870); Life and Work of G. Theophilus Dodds (1884); The White Fields of France (1879) | have-raw | IA |
| Light and Truth: The Gospels (1871); The Acts and the Larger Epistles (1870); The Lesser Epistles (1883) | have-raw | IA |
| Light and Truth: The Old Testament (1869) | have-raw | IA |
| Light and Truth: Revelation | pending | no scan found |
| God's Way of Holiness; Kelso Tracts; Redeem the Time | pending | scans found but their OCR never names Bonar, so the fetcher refused them (`_pending`) |
| How Shall I Go to God? | pending | listed on CCEL but its text is not served; no IA scan found yet |
| A Stranger Here (1853) | have-raw | IA `dli.ministry.06530` |
| Hymns of Faith and Hope (3 series), Communion Hymns, Lyra Consolationis, Hymns of the Nativity, The Song of the New Creation, Until the Day Break, The Bible Hymn-Book, The New Jerusalem, My Old Letters | see hymn manifest | hymns and poems |
| Words Old and New; Catechisms of the Scottish Reformation; Gillies' Historical Collections | excluded | others' texts that Bonar selected or edited |
| Gaelic and Welsh translations | excluded | not English |

## Andrew Bonar

Shelf: `pipeline/andrew-bonar_shelf.json` (2026-10-02). Andrew Alexander Bonar (1810-1892). Includes editions he made of Samuel Rutherford (marked "ed. Bonar": the text is Rutherford's, the sketch and notes are Bonar's). Posthumous diary, reminiscences and selections before 1931 are PD and marked.

| Work | Status | Where |
|---|---|---|
| Memoir and Remains of Robert Murray M'Cheyne | have | Gutenberg 15251 `abonar-mcheyne-memoir` (clean); IA 1844 first edition and 1878 enlarged edition (raw) |
| Narrative of a Mission of Inquiry to the Jews (with M'Cheyne, 1843) | have-raw | IA |
| A Commentary on Leviticus (1851) | have-raw | IA |
| Christ and His Church in the Book of Psalms (1859) | have-raw | IA |
| Memoir of David Sandeman (1862) | have-raw | IA |
| The Brook Besor (1879); Victory over Sin (186-); The Gospel Pointing to the Person of Christ (1888) | have-raw | IA |
| Presbyterian Liturgies (1858) | have-raw | IA |
| Diary and Letters (1894); Reminiscences (1895); Heavenly Springs (1904) | have-raw | IA, posthumous, ed. Marjory Bonar |
| Letters of Samuel Rutherford, ed. Bonar | have | Gutenberg 42557 |
| Quaint Sermons of Samuel Rutherford (1885); Fourteen Communion Sermons (1876), ed. Bonar | have-raw | IA |
| Redemption Drawing Nigh (1847) | have-raw | IA |
| The Visitor's Book of Texts | pending | only a 1982 reprint found |
| Narrative of a Visit to the Holy Land (1878) and other printings | pending | alternates listed in the shelf |
| Andrew Redman Bonar, Andrew J. Bonar, Andrew Bonar Law | excluded | different people |
| Gaelic Memoir of M'Cheyne, French Juifs d'Europe | excluded | not English |
| Modern reprints (1947-1982) | excluded | possibly in copyright |

## Adolph Saphir

Shelf: `pipeline/saphir_shelf.json` (2026-10-02). Adolph Saphir (1831-1891), Hebrew Christian expositor, born at Pesth, Presbyterian minister in London. No CCEL or Gutenberg Saphir exists; everything is Internet Archive OCR, raw.

| Work | Status | Where |
|---|---|---|
| Expository Lectures on Hebrews, first series ch. 1-7 (1875) and second series ch. 8-13 (1874) | have-raw | IA |
| Christ Crucified: Lectures on 1 Corinthians 2 (1873) | have-raw | IA |
| Christ and the Church (1874) | have-raw | IA |
| The Lord's Prayer (1872) | have-raw | IA |
| The Hidden Life (1877) | have-raw | IA |
| Our Life-Day (1878) | have-raw | IA |
| The Divine Unity of Scripture (1892, posthumous) | have-raw | IA |
| Christ and Israel (ed. David Baron, 1911, posthumous) | have-raw | IA |
| Auberlen, The Prophecies of Daniel and the Revelation, tr. Saphir (1856) | have-raw | IA (Saphir as translator) |
| Gavin Carlyle, "Mighty in the Scriptures": A Memoir of Adolph Saphir (1893) | have-raw | IA (about Saphir) |
| Christ and the Scriptures (1867) | pending | IA scan found, but its OCR never names Saphir, so the fetcher refused it; check by eye |
| Jesus and the Sinner (1851) / Found by the Good Shepherd | pending | IA credits Saphir; authorship to confirm |
| Conversion Illustrated; The Compassion of Jesus; other titles in bibliographies | pending | no verified scan found yet |
| The Epistle to the Hebrews: An Exposition (1902 one-work edition) | pending | same lectures as held; alternate edition |
| Christus und die Schrift (German, 1894) | excluded | not English |
| Modern reprints (1942-1984) | excluded | possibly in copyright |
| Moritz Gottlieb, Jacob, Philipp, Marie, Elijah Saphir and others | excluded | different people |


## Thomas Aquinas — Summa Theologiae census (lane A overflow, 2026-10-02)

The whole Summa is already covered by public-domain English text: the Fathers of the English Dominican Province translation (2nd revised ed., 1920-22). Nothing needed a new shelf.

| Part | Status | Where | Census |
|---|---|---|---|
| First Part (I), QQ. 1-119 | have | Gutenberg 17611, `aquinas-summa` in `pipeline/adler_shelf.json` | 119/119 questions present |
| First Part of the Second Part (I-II), QQ. 1-114 | have | Gutenberg 17897, `aquinas-summa-1-2` | 114/114 |
| Second Part of the Second Part (II-II), QQ. 1-189 | have | Gutenberg 18755, `aquinas-summa-2-2` | 189/189 |
| Third Part (III), QQ. 1-90 (Aquinas died at Q. 90) | have | Gutenberg 19950, `aquinas-summa-3` | 90/90 |
| Supplement, QQ. 1-99, and Appendix (2 questions + two articles on Purgatory) | have | CCEL `summa.xml`, cut by `pipeline/ingest_summa_supplement.py` into `aquinas-summa-supp` | 99/99 + appendix |
| Latin text | pending | out of scope for this census; a PD Latin edition (Leonine or Piana) is a wishlist item |

Defects found: in the Gutenberg files the first question of three treatises has no `QUESTION n` heading line (I Q. 116 "On Fate", I-II Q. 1 "Of Man's Last End", II-II Q. 183): the text is there, so a future question-level splitter must key on the question title too. `aquinas-summa-supp` is built by a standalone script and is not yet a row in `adler_shelf.json`, so a shelf-driven rebuild would miss it.


## John Owen (round 2, 2026-10-02)

Target: the Goold edition, *The Works of John Owen* (Edinburgh: Johnstone & Hunter, 1850-1855), 24 volumes, vols. 18-24 the Exposition of Hebrews. All 24 are held as raw IA OCR; each volume number was read off the title-page OCR. Every CCEL Owen title is held as clean ThML. No Gutenberg Owen exists.

| Work | Status | Where |
|---|---|---|
| `owen-mort` | have | already in `fetch_sources.py` (CCEL) |
| `owen-temptation` | have | already in `fetch_sources.py` (CCEL) |
| `owen-communion` | have | already in `fetch_sources.py` (CCEL) |
| `owen-glory` | have | already in `fetch_sources.py` (CCEL) |
| Nature and Causes of Apostasy from the Gospel | have | CCEL `apostasy` (`owen-apostasy`) |
| Two Short Catechisms | have | CCEL `catechisms` (`owen-catechisms`) |
| A Discourse concerning Evangelical Love, Church Peace, and Unity | have | CCEL `churchlove` (`owen-churchlove`) |
| Several Practical Cases of Conscience Resolved | have | CCEL `conscience` (`owen-conscience`) |
| The Death of Death in the Death of Christ | have | CCEL `deathofdeath` (`owen-deathofdeath`) |
| Sacramental Discourses | have | CCEL `discourses` (`owen-discourses`) |
| A Display of Arminianism | have | CCEL `display` (`owen-display`) |
| Eshcol; A Cluster of the Fruit of Canaan | have | CCEL `eshcol` (`owen-eshcol`) |
| An Inquiry into the Original, Nature, Institution, Power, Order, and Communion of Evangelical Churches | have | CCEL `evangelicalchurches` (`owen-evangelicalchurches`) |
| Gospel Grounds and Evidences of the Faith of God's Elect | have | CCEL `faith` (`owen-faith`) |
| A Review of the Annotations of Hugo Grotius | have | CCEL `grotius` (`owen-grotius`) |
| The Nature, Power, Deceit, and Prevelancy of the Remainders of Indwelling Sin in Believers | have | CCEL `indwellingsin` (`owen-indwellingsin`) |
| The Doctrine of Justification by Faith | have | CCEL `just` (`owen-just`) |
| A Dissertation on Divine Justice | have | CCEL `justice` (`owen-justice`) |
| A Discourse Concerning Liturgies, and their Imposition | have | CCEL `liturgies` (`owen-liturgies`) |
| The Doctrine of the Saints' Perseverance Explained and Confirmed | have | CCEL `perseverance` (`owen-perseverance`) |
| Pneumatologia | have | CCEL `pneum` (`owen-pneum`) |
| Poema | have | CCEL `poema` (`owen-poema`) |
| A Practical Exposition upon Psalm CXXX | have | CCEL `psalm130` (`owen-psalm130`) |
| Of Schism | have | CCEL `schism` (`owen-schism`) |
| The Sermons of John Owen | have | CCEL `sermons` (`owen-sermons`) |
| A Treatise of the Dominion of Sin and Grace | have | CCEL `sin_grace` (`owen-sin-grace`) |
| The Grace and Duty of being Spiritually Minded | have | CCEL `spirituallyminded` (`owen-spirituallyminded`) |
| A Brief Declaration and Vindication of The Doctrine of the Trinity | have | CCEL `trinity` (`owen-trinity`) |
| Truth and Innocence Vindicated | have | CCEL `truthinnocence` (`owen-truthinnocence`) |
| Vindiciæ Evangelicæ or, the Mystery of the Gospel Vindicated and Socinianism Examined | have | CCEL `vindicevang` (`owen-vindicevang`) |
| A Brief Instruction in the Worship of God | have | CCEL `worship` (`owen-worship`) |
| Goold vol. 1 | have-raw | IA `worksofjohnowe185001owen` |
| Goold vol. 2 | have-raw | IA `worksofjohnowe185002owen` |
| Goold vol. 3 | have-raw | IA `worksofjohnowe185003owen` |
| Goold vol. 4 | have-raw | IA `worksofjohnowen04owen` |
| Goold vol. 5 | have-raw | IA `worksofjohnowe185005owen` |
| Goold vol. 6 | have-raw | IA `worksofjohnowen06owen` |
| Goold vol. 7 | have-raw | IA `worksofjohnowen185007owen` |
| Goold vol. 8 | have-raw | IA `theworksofowen08owenuoft` |
| Goold vol. 9 | have-raw | IA `worksofjohnowe185009owen` |
| Goold vol. 10 | have-raw | IA `worksofjohnowe185010owen` |
| Goold vol. 11 | have-raw | IA `worksofjohnowend0011owen` |
| Goold vol. 12 | have-raw | IA `theworksofowen12owenuoft` |
| Goold vol. 13 | have-raw | IA `worksofjohnowe185013owen` |
| Goold vol. 14 | have-raw | IA `worksofjohnowen14owen` |
| Goold vol. 15 | have-raw | IA `worksofjohnowen15owen` |
| Goold vol. 16 | have-raw | IA `worksofjohnowe185016owen` |
| Goold vol. 17 (much of it Latin) | have-raw | IA `worksofjohnowend0017owen` |
| Goold vol. 18 (Hebrews) | have-raw | IA `worksofjohnowend0018owen` |
| Goold vol. 19 (Hebrews) | have-raw | IA `owensworks19owenuoft` |
| Goold vol. 20 (Hebrews) | have-raw | IA `owensworks20owenuoft` |
| Goold vol. 21 (Hebrews) | have-raw | IA `owensworks04owenuoft` |
| Goold vol. 22 (Hebrews) | have-raw | IA `owensworks05owenuoft` |
| Goold vol. 23 (Hebrews) | have-raw | IA `worksofjohnowend0023owen` |
| Goold vol. 24 (Hebrews) | have-raw | IA `owensworks07owenuoft` |
| Russell edition 1826; separate Hebrews editions 1811/1839/1840; Goold reprints 1862/1869 | alternate | not fetched: Goold supersedes them |
| Banner of Truth reprints (1965 onward); 1953/1954/1991 editions | excluded | possibly in copyright |


## Richard Sibbes (round 2, 2026-10-02)

Target: Grosart's *Complete Works of Richard Sibbes* (Edinburgh: James Nichol, 1862-1864), 7 volumes, all held as raw IA OCR (Toronto scans). No CCEL ThML could be found (the author page does not resolve) and no Gutenberg Sibbes exists, so there is no clean text yet.

| Work | Status | Where |
|---|---|---|
| Grosart vol. 1 | have-raw | IA `completeworksofr01sibbuoft` |
| Grosart vol. 2 | have-raw | IA `completeworksofr02sibbuoft` |
| Grosart vol. 3 | have-raw | IA `completeworksofr03sibbuoft` |
| Grosart vol. 4 | have-raw | IA `completeworksofr04sibbuoft` |
| Grosart vol. 5 | have-raw | IA `completeworksofr05sibbuoft` |
| Grosart vol. 6 | have-raw | IA `completeworksofr06sibbuoft` |
| Grosart vol. 7 | have-raw | IA `completeworksofr07sibbuoft` |
| Second scan of Grosart (`completeworkso01sibb`..`07`) | alternate | verified, not fetched |
| The Works (Aberdeen, 1809); EEBO quartos 1629-1658; single-work printings 1638-1842 | alternate | texts are in Grosart |
| Clean text of The Bruised Reed / The Soul's Conflict | wishlist | no PD machine-readable edition found |
| Modern editions (1973 onward) | excluded | possibly in copyright |


## Thomas Watson (round 2, 2026-10-02)

Watson (c.1620-1686) has no collected Works. The six CCEL titles are held as clean ThML; the Select Works (1855) and The Saints' Spiritual Delight (1830) as raw IA OCR. No Gutenberg Watson exists.

| Work | Status | Where |
|---|---|---|
| A Body of Divinity | have | CCEL `divinity` (`watson-body-divinity`) |
| The Ten Commandments | have | CCEL `commandments` (`watson-ten-commandments`) |
| The Lord's Prayer | have | CCEL `prayer` (`watson-lords-prayer`) |
| The Beatitudes: An Exposition of Matthew 5:1-12 | have | CCEL `beatitudes` (`watson-beatitudes`) |
| The Art of Divine Contentment | have | CCEL `contentment` (`watson-contentment`) |
| A Divine Cordial | have | CCEL `cordial` (`watson-divine-cordial`) |
| The Select Works of the Rev. Thomas Watson (New York: Robert Carter, 1855) | have-raw | IA `selectworksofrev00wats` |
| The Saints' Spiritual Delight (1830) | have-raw | IA `saintsspiritual00watsgoog` |
| The Godly Man's Picture; The Doctrine of Repentance; Heaven Taken by Storm; A Plea for the Godly | pending | only 1660s-1780s printings found (long-s OCR); first check whether the Select Works carries them |
| A Body of Practical Divinity, printings 1741-1859 | alternate | CCEL Body of Divinity held |
| Thomas Watson of Lincoln (1513-1584), Richard Watson (1781-1833), Thomas E. Watson | excluded | different people |


## Richard Baxter (round 2, 2026-10-02)

Target: Orme's *Practical Works of the Rev. Richard Baxter* (London: James Duncan, 1830), 23 volumes, vol. 1 being Orme's Life of Baxter. All 23 are held as raw IA OCR; no one scan series is complete, so the set mixes Toronto, other library and Google/BSB scans, every volume number read off the title page. Clean text: four CCEL titles and Gutenberg's four-part Christian Directory.

| Work | Status | Where |
|---|---|---|
| The Causes and Danger of Slighting Christ and His Gospel | have | CCEL `causes` (`baxter-causes`) |
| The Reformed Pastor | have | CCEL `pastor` (`baxter-reformed-pastor`) |
| The Saints' Everlasting Rest | have | CCEL `saints_rest` (`baxter-saints-rest`) |
| A Call to the Unconverted to Turn and Live | have | CCEL `unconverted` (`baxter-call-unconverted`) |
| A Christian Directory, Part 1: Christian Ethics | have | Gutenberg 41633 (`baxter-directory-1`) |
| A Christian Directory, Part 2: Christian Economics | have | Gutenberg 43800 (`baxter-directory-2`) |
| A Christian Directory, Part 3: Christian Ecclesiastics | have | Gutenberg 44655 (`baxter-directory-3`) |
| A Christian Directory, Part 4: Christian Politics | have | Gutenberg 43967 (`baxter-directory-4`) |
| Orme vol. 1 (Life) | have-raw | IA `practicalworksof01baxtuoft` |
| Orme vol. 2 | have-raw | IA `practicalworksof02baxtuoft` |
| Orme vol. 3 | have-raw | IA `practicalworksof03baxt` |
| Orme vol. 4 | have-raw | IA `10785346bsb` |
| Orme vol. 5 | have-raw | IA `10785347bsb` |
| Orme vol. 6 | have-raw | IA `practicalworksof06baxtuoft` |
| Orme vol. 7 | have-raw | IA `practicalworksof07baxtuoft` |
| Orme vol. 8 | have-raw | IA `practicalworksof08baxtuoft` |
| Orme vol. 9 | have-raw | IA `practicalworksof09baxt` |
| Orme vol. 10 | have-raw | IA `practicalworksof10baxt` |
| Orme vol. 11 | have-raw | IA `practicalworksof11baxtuoft` |
| Orme vol. 12 | have-raw | IA `practicalworksof12baxtuoft` |
| Orme vol. 13 | have-raw | IA `practicalworksof13baxtuoft` |
| Orme vol. 14 | have-raw | IA `practicalworksof14baxt` |
| Orme vol. 15 | have-raw | IA `practicalworksof15baxtuoft` |
| Orme vol. 16 | have-raw | IA `practicalworksof16baxtuoft` |
| Orme vol. 17 | have-raw | IA `practicalworksof17baxt` |
| Orme vol. 18 | have-raw | IA `practicalworksof18baxtuoft` |
| Orme vol. 19 | have-raw | IA `practicalworksof19baxtuoft` |
| Orme vol. 20 | have-raw | IA `practicalworksr00ormegoog` |
| Orme vol. 21 | have-raw | IA `practicalworksof21baxtuoft` |
| Orme vol. 22 | have-raw | IA `practicalworksof22baxtuoft` |
| Orme vol. 23 | have-raw | IA `practicalworksof23baxtuoft` |
| Reliquiae Baxterianae (1696); Methodus Theologiae, Catholick Theology and the controversial works | pending | not in the Practical Works; no scan verified yet |
| Practical Works 1707 (4 folio vols); 1838/1845 four-volume edition; Select Practical Writings (Bacon) | alternate | not fetched |
| CCEL `practical` | excluded | a stub with almost no text |
| Wesley's abridged Saints' Rest | excluded | not Baxter's text |


## Thomas Brooks (round 2, 2026-10-02)

Target: Grosart's *Complete Works of Thomas Brooks* (Edinburgh: James Nichol, 1866-1867), 6 volumes, all held as raw IA OCR (Toronto scans). No CCEL or Gutenberg Brooks exists, so there is no clean text yet.

| Work | Status | Where |
|---|---|---|
| Grosart vol. 1 | have-raw | IA `completeworksoft01broouoft` |
| Grosart vol. 2 | have-raw | IA `completeworksoft02broouoft` |
| Grosart vol. 3 | have-raw | IA `completeworksoft03broouoft` |
| Grosart vol. 4 | have-raw | IA `completeworksoft04broouoft` |
| Grosart vol. 5 | have-raw | IA `completeworksoft05broouoft` |
| Grosart vol. 6 | have-raw | IA `completeworksoft06broouoft` |
| Other scans of Grosart; Apples of Gold 1814/1859; London's Lamentations 1670; 18th-century printings | alternate | texts are in Grosart |
| Clean text of Precious Remedies against Satan's Devices | wishlist | no PD machine-readable edition found |
| Welsh Privie Key (1845); Great Gain (1869 anthology); other Thomas Brookses | excluded | not English / not Brooks's text / different people |


## Thomas Goodwin (round 2, 2026-10-02)

Target: Nichol's *Works of Thomas Goodwin, D.D.* (Edinburgh, 1861-1866), 12 volumes, all held as raw IA OCR from one complete scan series, each volume number read off its title page. No CCEL or Gutenberg text of this Thomas Goodwin exists.

| Work | Status | Where |
|---|---|---|
| Nichol vol. 1 | have-raw | IA `worksofthomasgoo01good` |
| Nichol vol. 2 | have-raw | IA `worksofthomasgoo02good` |
| Nichol vol. 3 | have-raw | IA `worksofthomasgoo03good` |
| Nichol vol. 4 | have-raw | IA `worksofthomasgoo04good` |
| Nichol vol. 5 | have-raw | IA `worksofthomasgoo05good` |
| Nichol vol. 6 | have-raw | IA `worksofthomasgoo06good` |
| Nichol vol. 7 | have-raw | IA `worksofthomasgoo07good` |
| Nichol vol. 8 | have-raw | IA `worksofthomasgoo08good` |
| Nichol vol. 9 | have-raw | IA `worksofthomasgoo09good` |
| Nichol vol. 10 | have-raw | IA `worksofthomasgoo10good` |
| Nichol vol. 11 | have-raw | IA `worksofthomasgoo11good` |
| Nichol vol. 12 | have-raw | IA `worksofthomasgoo12good` |
| Other scans of Nichol; the 1681-1704 folio Works | alternate | not fetched |
| Clean text of The Heart of Christ in Heaven towards Sinners on Earth | wishlist | no PD machine-readable edition found |
| PG 52639 Moses and Aaron; CCEL goodwin/greekgrammar | excluded | different Goodwins (d. 1642; W. W. Goodwin) |


## Samuel Rutherford (round 2, 2026-10-02)

There is no collected Works. Bonar's editions of the Letters and of two sermon books are already held on the Andrew Bonar shelf and are not refetched. New here: two CCEL titles (clean) and IA OCR of Lex, Rex and the 1640s-1650s treatises.

| Work | Status | Where |
|---|---|---|
| Letters of Samuel Rutherford, ed. Bonar | have | `abonar-ed-rutherford-letters` on `andrew-bonar_shelf.json` |
| Quaint Sermons (1885) | have | `abonar-ed-rutherford-quaint-sermons` on `andrew-bonar_shelf.json` |
| Fourteen Communion Sermons (1876) | have | `abonar-ed-rutherford-communion-sermons` on `andrew-bonar_shelf.json` |
| A Selection from his Letters (CCEL) | have | CCEL `letters` (`rutherford-letters-selection`) |
| The Trial and Triumph of Faith (London: John Field, 1645) | have | CCEL `triumph` (`rutherford-trial-triumph`) |
| Lex, Rex, or The Law and the Prince (Edinburgh, 1843 reprint) | have-raw | IA `lexrexorlawprinc00ruth` |
| A Free Disputation against Pretended Liberty of Conscience (London, 1649) | have-raw | IA `freedisputationa00ruth` (title words partly unread: long s) |
| The Covenant of Life Opened (Edinburgh, 1655) | have-raw | IA `covenli00ruth` |
| The Due Right of Presbyteries (London, 1644) | have-raw | IA EEBO scan (`rutherford-due-right-1644`); the library scan was refused |
| Christ Dying and Drawing Sinners (1647); The Divine Right of Church-Government (1646) | pending | scans found, but their OCR never names Rutherford, so the fetcher refused them; no passing scan found; check by eye |
| A Survey of the Spiritual Antichrist (1648); The Influences of the Life of Grace (1659); the Latin works | pending | not yet found or searched |
| Joshua Redivivus (1796, 1818) and other Letters editions | alternate | Bonar's Letters held |
| S. R. Crockett's novels | excluded | different person |


## Robert Murray M'Cheyne, prose (round 2, 2026-10-02)

His hymns and poems are not shelved here: see the hymn manifest. Bonar's Memoir and Remains and the Mission of Inquiry are already on the Andrew Bonar shelf. New here: four prose collections as raw IA OCR. No CCEL M'Cheyne exists; Gutenberg has only Bonar's Memoir.

| Work | Status | Where |
|---|---|---|
| `abonar-mcheyne-memoir` | have | Gutenberg 15251, on andrew-bonar_shelf.json |
| `abonar-mcheyne-memoir-1844` | have | on andrew-bonar_shelf.json |
| `abonar-mcheyne-memoir-1878` | have | on andrew-bonar_shelf.json |
| `Narrative of a Mission of Inquiry (with Bonar)` | have | on andrew-bonar_shelf.json |
| The Works of the Late Rev. Robert Murray McCheyne (New York: Robert Carter, 1847), vol. 1 | have-raw | IA `worksoflaterevro01mche` |
| The Works of the Late Rev. Robert Murray McCheyne (New York: Robert Carter, 1847), vol. 2 | have-raw | IA `worksoflaterevro02mche` |
| Familiar Letters by the Rev. Robert Murray M'Cheyne, ed. Adam M'Cheyne (1848) | have-raw | IA `familiarletters00mchgoog` |
| The Sermons of the Rev. Robert Murray McCheyne (1863) | have-raw | IA `sermonsofrevrobe00mche` |
| Additional Remains of the Rev. Robert Murray M'Cheyne (1849 printing, microform scan) | have-raw | IA `MN5152ucmf_2` |
| Hymns and poems | see hymn manifest | not shelved here |
| Gaelic translations (1879, 1916); Coventry's abridged Memoir (1865) | excluded | not English / not the full text |


## Matthew Henry (round 2, 2026-10-02)

The Exposition ('Commentary on the Whole Bible') is held whole from CCEL as clean ThML, six volumes plus the Concise Commentary; CCEL's rights line on each reads public domain. Vol. VI (Acts to Revelation) was completed after Henry's death by other ministers. The treatises and sermons come from the 1830 Miscellaneous Works (raw IA OCR).

| Work | Status | Where |
|---|---|---|
| Commentary on the Whole Bible, vol. I (Genesis to Deuteronomy) | have | CCEL `mhc1` (`mhenry-commentary-1`) |
| Commentary on the Whole Bible, vol. II (Joshua to Esther) | have | CCEL `mhc2` (`mhenry-commentary-2`) |
| Commentary on the Whole Bible, vol. III (Job to Song of Solomon) | have | CCEL `mhc3` (`mhenry-commentary-3`) |
| Commentary on the Whole Bible, vol. IV (Isaiah to Malachi) | have | CCEL `mhc4` (`mhenry-commentary-4`) |
| Commentary on the Whole Bible, vol. V (Matthew to John) | have | CCEL `mhc5` (`mhenry-commentary-5`) |
| Commentary on the Whole Bible, vol. VI (Acts to Revelation; completed by other ministers after Henry's death) | have | CCEL `mhc6` (`mhenry-commentary-6`) |
| Matthew Henry's Concise Commentary on the Bible | have | CCEL `mhcc` (`mhenry-concise`) |
| The Miscellaneous Works of the Rev. Matthew Henry, ed. J. B. Williams (London, 1830) | have-raw | IA `miscellaneouswor00henr` |
| The Life and Times of the Rev. Philip Henry, by Matthew Henry (1849 printing) | have-raw | IA `lifetimesofrevph00henr` |
| Method for Prayer, Communicant's Companion, Daily Communion with God and other single treatises | alternate | single printings on IA; most are inside the Miscellaneous Works (not checked title by title) |
| Complete Works (1847) | pending | only vol. 1 found on IA |
| German Psalms translation (1770); Philip Henry's own sermons | excluded | not English / a different author |


## John Calvin, English (round 2, 2026-10-02)

Census first: the 45 Calvin Translation Society commentary volumes are already held through `CALVIN_COMMENTARIES` in `fetch_sources.py`, and the set is complete (Genesis to the Catholic Epistles; Calvin wrote nothing on Revelation and his Ezekiel ends at ch. 20). Added as verified gaps: the Institutes (Beveridge, CTS 1845) and A Treatise on Relics, clean from CCEL; the Letters (Bonnet, 1858, 4 vols), vols 1-2 clean from Gutenberg and 3-4 as IA OCR; the CTS Tracts (3 vols) as IA OCR.

| Work | Status | Where |
|---|---|---|
| Commentaries, CTS, 45 vols (`calvin-com01`..`45`) | have | already in `fetch_sources.py` |
| Institutes of the Christian Religion, tr. Henry Beveridge (Calvin Translation Society, 1845) | have | CCEL `institutes` (`calvin-institutes-beveridge`) |
| A Treatise on Relics, tr. Valerian Krasinski (1854) | have | CCEL `treatise_relics` (`calvin-treatise-relics`) |
| Letters of John Calvin, ed. Jules Bonnet (Philadelphia, 1858), vol. 1 | have | Gutenberg 45423 (`calvin-letters-1`) |
| Letters of John Calvin, ed. Jules Bonnet (Philadelphia, 1858), vol. 2 | have | Gutenberg 45463 (`calvin-letters-2`) |
| Letters of John Calvin, ed. Jules Bonnet (Philadelphia, 1858), vol. 3 | have-raw | IA `lettersc03calv` |
| Letters of John Calvin, ed. Jules Bonnet (Philadelphia, 1858), vol. 4 | have-raw | IA `lettersofjohncal04calv` |
| Tracts Relating to the Reformation, tr. Henry Beveridge (Calvin Translation Society, 1844), vol. 1 | have-raw | IA `tractsrelatingto01calv` |
| Tracts Relating to the Reformation, tr. Henry Beveridge (Calvin Translation Society, 1850), vol. 2 | have-raw | IA `tractsrelatingto02calv` |
| Tracts Relating to the Reformation, tr. Henry Beveridge (Calvin Translation Society, 1851), vol. 3 | have-raw | IA `tractsrelatingto03calv` |
| Institutes in John Allen's (1813) or Norton's (1561) translation | pending | not searched |
| French sermons (Corpus Reformatorum 61-63, on CCEL); Latin Institutio | excluded here | not English; CCEL's Institutio files are stubs |
| On the Christian Life; Of Prayer (CCEL) | alternate | extracts from the Institutes held |


## Stephen Charnock (round 3, my pick, 2026-10-02)

Target: Nichol's *Complete Works of Stephen Charnock* (1864-1866), 5 volumes, raw IA OCR; vols 1-2 hold the Existence and Attributes of God. Six CCEL discourses held clean. No Gutenberg Charnock.

| Work | Status | Where |
|---|---|---|
| A Discourse on the Cleansing Virtue of Christ's Blood | have | CCEL `cleansing` (`charnock-cleansing`) |
| A Discourse of the Efficient of Regeneration | have | CCEL `efficient_regeneration` (`charnock-efficient-regeneration`) |
| A Discourse of the Word, the Instrument of Regeneration | have | CCEL `instr_regen` (`charnock-instrument-regeneration`) |
| A Discourse of the Nature of Regeneration | have | CCEL `nat_regen` (`charnock-nature-regeneration`) |
| The Necessity of Regeneration | have | CCEL `nec_regen` (`charnock-necessity-regeneration`) |
| A Discourse of God's being the Author of Reconciliation | have | CCEL `reconcil` (`charnock-reconciliation`) |
| Nichol vol. 1 | have-raw | IA `completeworksofs01char` |
| Nichol vol. 2 | have-raw | IA `completeworksofs02char` |
| Nichol vol. 3 | have-raw | IA `completeworksofs03char` |
| Nichol vol. 4 | have-raw | IA `completeworksofs04char` |
| Nichol vol. 5 | have-raw | IA `completeworksofs05char` |
| Parsons edition (1815, 9 vols); separate printings of the Attributes (1800-1874) | alternate | Nichol supersedes them |
| Richard Stephen Charnock, etymologist | excluded | different person |


## Thomas Manton (round 3, my pick, 2026-10-02)

Target: the Nisbet *Complete Works of Thomas Manton* (22 vols, 1870-1875). CCEL has nine volumes as clean ThML (1-8, 20); the other thirteen are raw IA OCR. One slug per volume.

| Volume | Status | Where |
|---|---|---|
| Nisbet vol. 1 | have | CCEL `manton01` |
| Nisbet vol. 2 | have | CCEL `manton02` |
| Nisbet vol. 3 | have | CCEL `manton03` |
| Nisbet vol. 4 | have | CCEL `manton04` |
| Nisbet vol. 5 | have | CCEL `manton05` |
| Nisbet vol. 6 | have | CCEL `manton06` |
| Nisbet vol. 7 | have | CCEL `manton07` |
| Nisbet vol. 8 | have | CCEL `manton08` |
| Nisbet vol. 9 | have-raw | IA `completeworksoft09mant` |
| Nisbet vol. 10 | have-raw | IA `completeworksoft10mant` |
| Nisbet vol. 11 | have-raw | IA `completeworksoft11mant` |
| Nisbet vol. 12 | have-raw | IA `completeworksoft12mant` |
| Nisbet vol. 13 | have-raw | IA `completeworksoft13mant` |
| Nisbet vol. 14 | have-raw | IA `completeworksoft14mant` |
| Nisbet vol. 15 | have-raw | IA `completeworksoft15mant` |
| Nisbet vol. 16 | have-raw | IA `completeworksoft16mant` |
| Nisbet vol. 17 | have-raw | IA `completeworksoft17mant` |
| Nisbet vol. 18 | have-raw | IA `completeworksoft18mant` |
| Nisbet vol. 19 | have-raw | IA `completeworksoft19mant` |
| Nisbet vol. 20 | have | CCEL `manton20` |
| Nisbet vol. 21 | have-raw | IA `completeworksoft21mant` |
| Nisbet vol. 22 | have-raw | IA `completeworksoft22mant` |
| IA scans of the CCEL volumes; Toronto scans | alternate | not fetched |


## C. H. Spurgeon (round 2, 2026-10-02)

The sermons, 63 volumes (1855-1917), and seven other works are held clean from CCEL. The Treasury of David is not usable from CCEL (its files are contents-only stubs), so it is held as raw IA OCR of the seven-volume American printing (Funk & Wagnalls, 1882-1886), each volume identified by the psalm range on its title page.

| Work | Status | Where |
|---|---|---|
| Spurgeon's Sermons, vols 1-63 (1855-1917) | have | CCEL `sermons01`..`sermons63` (`spurgeon-sermons-01`..`63`) |
| Morning and Evening: Daily Readings | have | CCEL `morneve` (`spurgeon-morning-evening`) |
| All of Grace | have | CCEL `grace` (`spurgeon-all-of-grace`) |
| Faith's Checkbook | have | CCEL `checkbook` (`spurgeon-faiths-checkbook`) |
| A Puritan Catechism | have | CCEL `catechism` (`spurgeon-puritan-catechism`) |
| Commenting and Commentaries | have | CCEL `comment` (`spurgeon-commenting`) |
| Sermons on Proverbs | have | CCEL `proverbs` (`spurgeon-sermons-proverbs`) |
| Till He Come | have | CCEL `till_he_come` (`spurgeon-till-he-come`) |
| The Treasury of David (New York: Funk & Wagnalls, 1882-1886 printing), vol. 1: Psalms 1-26 | have-raw | IA `treasurydavidco08spurgoog` |
| The Treasury of David (New York: Funk & Wagnalls, 1882-1886 printing), vol. 2: Psalms 27-52 | have-raw | IA `treasuryofdavidc0002spur` |
| The Treasury of David (New York: Funk & Wagnalls, 1882-1886 printing), vol. 3: Psalms 53-78 | have-raw | IA `treasuryofdavidc0000spur` |
| The Treasury of David (New York: Funk & Wagnalls, 1882-1886 printing), vol. 4: Psalms 79-103 | have-raw | IA `treasurydavidco06spurgoog` |
| The Treasury of David (New York: Funk & Wagnalls, 1882-1886 printing), vol. 5: Psalms 104-118 | have-raw | IA `treasuryofdavidc0005spur` |
| The Treasury of David (New York: Funk & Wagnalls, 1882-1886 printing), vol. 6: Psalms 119-124 | have-raw | IA `treasuryofdavidc0006spur` |
| The Treasury of David (New York: Funk & Wagnalls, 1882-1886 printing), vol. 7: Psalms 125-150 | have-raw | IA `treasuryofdavidc0007spur` |
| Lectures to My Students; John Ploughman's Talk; The Soul Winner; Gutenberg Spurgeon | pending | not searched this burn |
| CCEL Treasury of David (treasury1-6) | excluded | stubs |


## Thomas Boston (round 3, my pick, 2026-10-02)

Target: M'Millan's *Whole Works of Thomas Boston* (12 vols, 1848-1852, including his Memoirs), raw IA OCR, each volume read off its title page. The Crook in the Lot is held clean from CCEL.

| Work | Status | Where |
|---|---|---|
| The Crook in the Lot | have | CCEL `crook` (`boston-crook-in-lot`) |
| Whole Works vol. 1 | have-raw | IA `wholeworksoflate01bost` |
| Whole Works vol. 2 | have-raw | IA `wholeworksoflate02bost` |
| Whole Works vol. 3 | have-raw | IA `wholeworksoflate03bost` |
| Whole Works vol. 4 | have-raw | IA `wholeworksoflate04bost` |
| Whole Works vol. 5 | have-raw | IA `wholeworksoflate05bost` |
| Whole Works vol. 6 | have-raw | IA `wholeworksoflate06bost` |
| Whole Works vol. 7 | have-raw | IA `wholeworksoflate07bost` |
| Whole Works vol. 8 | have-raw | IA `wholeworksoflate08bost` |
| Whole Works vol. 9 | have-raw | IA `wholeworkslater02bostgoog` |
| Whole Works vol. 10 | have-raw | IA `wholeworksoflate10bost` |
| Whole Works vol. 11 | have-raw | IA `wholeworksoflate11bost` |
| Whole Works vol. 12 | have-raw | IA `wholeworksoflate12bost` |
| Human Nature in its Fourfold State, Memoirs, Crook in the Lot: separate printings 1775-1899 | alternate | in the Whole Works |
| A clean Fourfold State | wishlist | no PD machine-readable edition found |


## William Gurnall (round 3, my pick, 2026-10-02)

| Work | Status | Where |
|---|---|---|
| The Christian in Complete Armour, intro. John Campbell (London, 1862) | have-raw | IA `ChristianInCompleteArmourOr` |
| Editions of 1803, 1821, 1845; second 1862 scan | alternate | not fetched |
| CCEL `gurnall/armour` | excluded | a stub |
| A clean text of the Complete Armour | wishlist | no PD machine-readable edition found |


## Jeremiah Burroughs (round 3, my pick, 2026-10-02)

No collected Works, no CCEL, no Gutenberg. Two Nichol reprints (Hosea 1863, Saints' Happiness 1867) plus two 1650s printings that passed the identity check, all raw IA OCR.

| Work | Status | Where |
|---|---|---|
| An Exposition of the Prophecy of Hosea, with continuations by Thomas Hall and Edward Reynolds (Edinburgh: James Nichol, 1863) | have-raw | IA `expositionofprop00burr` |
| The Saints' Happiness: Lectures on the Beatitudes (Edinburgh: James Nichol, 1867) | have-raw | IA `saintshappinesst00burr` |
| Moses his Choice, with his Eye Fixed upon Heaven (London, 1650) | have-raw | IA `moseshischoicewi00burr` |
| Four Books on the Eleventh of Matthew (London, 1659) | have-raw | IA `fourbooksonelev00burrgoog` |
| The Rare Jewel of Christian Contentment (London, 1649); Irenicum (1653); The Saints' Treasury (1656); The Glorious Name of God (1643) | have-raw | IA EEBO scans that name Burroughs (`burroughs-rare-jewel-1649`, `-irenicum-1653`, `-saints-treasury-1656`, `-glorious-name-1643`); the Google/library scans were refused; Irenicum flagged `title_weak` |
| Gospel Worship; Gospel Conversation; Gospel Fear; The Evil of Evils | pending | no scan verified yet |
| A clean Rare Jewel | wishlist | no PD machine-readable edition found |


## John Newton, prose (round 3, my pick, 2026-10-02)

His hymns (Olney Hymns) are not shelved here: see the hymn manifest. The six-volume Works (1810) and Bull's 1869 Letters are raw IA OCR; Messiah is clean from CCEL.

| Work | Status | Where |
|---|---|---|
| Messiah: Fifty Expository Discourses, vol. 1 | have | CCEL `messiah1` (`newton-messiah-1`) |
| Messiah: Fifty Expository Discourses, vol. 2 | have | CCEL `messiah2` (`newton-messiah-2`) |
| The Works of the Rev. John Newton (1810), vol. 1 | have-raw | IA `worksrevjohnne01newt` |
| The Works of the Rev. John Newton (1810), vol. 2 | have-raw | IA `worksrevjohnne02newt` |
| The Works of the Rev. John Newton (1810), vol. 3 | have-raw | IA `worksrevjohnne03newt` |
| The Works of the Rev. John Newton (1810), vol. 4 | have-raw | IA `worksrevjohnne04newt` |
| The Works of the Rev. John Newton (1810), vol. 5 | have-raw | IA `worksrevjohnne05newt` |
| The Works of the Rev. John Newton (1810), vol. 6 | have-raw | IA `worksrevjohnne06newt` |
| Letters by the Rev. John Newton of Olney and St. Mary Woolnoth, ed. Josiah Bull (1869) | have-raw | IA `lettersbynewton00newtuoft` |
| Olney Hymns | see hymn manifest | not shelved here |
| Cardiphonia, Authentic Narrative, other letter collections: separate printings | alternate | mostly in the Works |


## George Whitefield (round 3, my pick, 2026-10-02)

The Works (1771-72, 6 vols: sermons, tracts, letters) are clean from Gutenberg; CCEL's Selected Sermons (1904) clean; the Journals as raw IA OCR of their first printings (18th-century type).

| Work | Status | Where |
|---|---|---|
| The Works of the Reverend George Whitefield (London, 1771-1772), vol. 1 | have | Gutenberg 68976 (`whitefield-works-1`) |
| The Works of the Reverend George Whitefield (London, 1771-1772), vol. 2 | have | Gutenberg 71140 (`whitefield-works-2`) |
| The Works of the Reverend George Whitefield (London, 1771-1772), vol. 3 | have | Gutenberg 73012 (`whitefield-works-3`) |
| The Works of the Reverend George Whitefield (London, 1771-1772), vol. 4 | have | Gutenberg 73267 (`whitefield-works-4`) |
| The Works of the Reverend George Whitefield (London, 1771-1772), vol. 5 | have | Gutenberg 77034 (`whitefield-works-5`) |
| The Works of the Reverend George Whitefield (London, 1771-1772), vol. 6 | have | Gutenberg 77041 (`whitefield-works-6`) |
| Selected Sermons of George Whitefield, ed. A. R. Buckland (1904) | have | CCEL `sermons` (`whitefield-selected-sermons`) |
| A Journal of a Voyage from London to Savannah in Georgia (1743 printing) | have-raw | IA `journalofvoyagef00whit` |
| A Continuation of the Reverend Mr. Whitefield's Journal, from his arrival at London to his departure for Georgia (1739) | have-raw | IA `continuationofre03whit` |
| A Continuation of the Reverend Mr. Whitefield's Journal, during the time he was detained in England by the embargo (1739) | have-raw | IA `continuationofre04whit` |
| A Continuation of the Reverend Mr. Whitefield's Journal, from his embarking after the embargo to his arrival at Savannah (1740) | have-raw | IA `continuationofre05whit` |
| A Continuation of the Reverend Mr. Whitefield's Journal, after his arrival at Georgia (1741) | have-raw | IA `continuationofre06whit` |
| A Continuation of the Reverend Mr. Whitefield's Journal: the seventh journal (1744 printing) | have-raw | IA `continuationofre07whit` |
| The Two First Parts of his Life, with his Journals, revised and abridged by himself (1756) | have-raw | IA `twofirst00whit` (title words partly unread) |
| The second journal (Savannah to London, 1739) | pending | only ECCO long-s scans found |
| Tyerman's Life; Belcher's biography | excluded here | by other hands |


## Charles Hodge (round 3, my pick, 2026-10-02)

Systematic Theology (3 vols + index), Ephesians and What is Darwinism? clean from CCEL; the other commentaries and collections as raw IA OCR.

| Work | Status | Where |
|---|---|---|
| Systematic Theology, vol. I (1871-1873) | have | CCEL `theology1` (`hodge-systematic-theology-1`) |
| Systematic Theology, vol. II | have | CCEL `theology2` (`hodge-systematic-theology-2`) |
| Systematic Theology, vol. III | have | CCEL `theology3` (`hodge-systematic-theology-3`) |
| Systematic Theology, Index | have | CCEL `theology4` (`hodge-systematic-theology-index`) |
| A Commentary on the Epistle to the Ephesians (1856) | have | CCEL `ephesians` (`hodge-ephesians`) |
| What is Darwinism? (1874) | have | CCEL `darwinism` (`hodge-what-is-darwinism`) |
| Commentary on the Epistle to the Romans (revised edition, 1864) | have-raw | IA `commentaryonepis00hodgiala` |
| An Exposition of the First Epistle to the Corinthians (1857) | have-raw | IA `expositionoffirs00hodg` |
| The Way of Life (Philadelphia: American Sunday-School Union, 1841) | have-raw | IA `wayoflife00hodg` |
| Essays and Reviews, selected from the Princeton Review (1857) | have-raw | IA `essaysreviews00hodg` |
| Discussions in Church Polity (1878) | have-raw | IA `discussionsinchu00hodg` |
| Conference Papers: Analyses of Discourses, Doctrinal and Practical (1879) | have-raw | IA `conferencepapers00hodg` |
| The Constitutional History of the Presbyterian Church in the United States of America (1851 edition) | have-raw | IA `constitutionalhi1851hodg` |
| An Exposition of the Second Epistle to the Corinthians (1860) | have-raw | IA `expositionofseco00hodg` |
| Princeton Sermons (1879); England and America (1862) | pending | not fetched this burn |
| Romans, first edition (1835) | alternate | the 1864 revision is held |
| A. A. Hodge's books | excluded here | his son |

## John Howe (round 4, my pick, 2026-10-02)

The Whole Works (London: F. Westley, 1822, ed. John Hunt, 8 vols): vols. V-VIII clean from CCEL, vols. I-IV raw IA OCR (title pages read).

| Work | Status | Where |
|---|---|---|
| The Whole Works, vols. V-VIII (1822) | have | CCEL `howe05`-`howe08` (`howe-whole-works-05`..`08`) |
| The Whole Works, vols. I-IV (1822) | have-raw | IA `wholeworksofrevj01howeuoft`..`04howeuoft` |
| Posthumous Works (1832, ed. Hunt) | pending | two Google scans whose title pages give no clear volume order |
| Works (1724, 2 vols); (1835); (1838, 2 vols); (1862-63, 6 vols, pref. Rogers) | alternate | the 1822 Whole Works is held |

## Philip Doddridge (round 4, my pick, 2026-10-02)

Three titles clean from CCEL, one from Gutenberg; the Leeds Works (Edward Baines, 1802-1805, 10 vols) as raw IA OCR. Hymns are for the hymn manifest.

| Work | Status | Where |
|---|---|---|
| The Rise and Progress of Religion in the Soul (1745) | have | CCEL `rise` (`doddridge-rise-progress`) |
| Practical Discourses on Regeneration (1742) | have | CCEL `regen` (`doddridge-regeneration`) |
| The Evidences of Christianity Briefly Stated | have | CCEL `evidences` (`doddridge-evidences`) |
| The Life of Col. James Gardiner | have | Gutenberg 11253 (`doddridge-life-gardiner`) |
| The Works, vols. I-IX (Leeds, 1802-1805) | have-raw | IA `worksofrevpdoddr01dodd`..`09dodd` |
| The Works, vol. X | have-raw | IA `worksrevpdoddri01doddgoog` (the Princeton vol. X scan never names Doddridge and was refused) |
| Miscellaneous Works (1830, 1839) | alternate | the Leeds Works are held |

## Thomas Shepard (round 4, my pick, 2026-10-02)

The Works (Boston, 1853, ed. Albro, 3 vols): vol. I clean from CCEL, vols. II-III raw IA OCR; three further items.

| Work | Status | Where |
|---|---|---|
| The Works, vol. I (1853): Life; The Sincere Convert; The Sound Believer; The Saint's Jewel; Certain Select Cases Resolved; First Principles; The Sum of Christian Religion | have | CCEL `worksthomas` (`shepard-works-01`) |
| The Change of the Sabbath | have | CCEL `sabbath` (`shepard-change-sabbath`) |
| The Works, vols. II-III (1853) | have-raw | IA `worksofthomasshe02shep`, `worksofthomasshe03shep` |
| The Autobiography of Thomas Shepard (1832, ed. N. Adams) | have-raw | IA `autobiographyth00adamgoog` (the library scan has only 38 of 129 pages) |
| The Clear Sun-shine of the Gospel (1648; 1865 reprint) | have-raw | IA `cu31924028652349` |
| First printings (1645-1658) and ECCO reprints | alternate | the 1853 Works are held |

## Henry Scougal (round 4, my pick, 2026-10-02)

| Work | Status | Where |
|---|---|---|
| The Life of God in the Soul of Man | have | CCEL `life` (`scougal-life-of-god`) |
| The Works (Pittsburgh: J. I. Kay, 1830) | have-raw | IA `worksofrevhenrys00scou` |
| Works and Life of God, printings of 1691-1839 | alternate | the 1830 Works are held |
| A New Academy of Compliments (1748) | excluded | catalogued under Scougal on IA; a letter-writing manual, not his |

## William Law (round 4, my pick, 2026-10-02)

Ten titles clean from CCEL; the Works (Brockenhurst: privately reprinted for G. Moreton, 1892-93, 9 vols) as raw IA OCR.

| Work | Status | Where |
|---|---|---|
| A Serious Call to a Devout and Holy Life (1729) | have | CCEL `serious_call` (`law-serious-call`) |
| A Practical Treatise upon Christian Perfection (1726) | have | CCEL `apracticaltreat` (`law-christian-perfection`) |
| The Spirit of Prayer; The Spirit of Love | have | CCEL `prayer`, `love2` |
| The Way to Divine Knowledge; The Grounds and Reasons of Christian Regeneration | have | CCEL `waytodivine`, `grounds` |
| A Demonstration of the Gross and Fundamental Errors; An Appeal to All that Doubt | have | CCEL `errors`, `doubt` |
| An Address to the Clergy; A Collection of Letters | have | CCEL `clergy`, `collection` (also together as CCEL `humbleearnest`, not held twice) |
| The Works, vols. I-IX (1892-93 reprint) | have-raw | IA `worksofreverendl01lawuoft`..`04lawuoft`, `worksoflaw05lawuoft`..`08lawuoft`, `worksofreverendw09laww` |
| The Works (1762), 9 vols | alternate | the 1892-93 reprint is held |
| Jacob Boehme's Works (1764-81) | excluded | Boehme's text |

## John Gill (round 4, my pick, 2026-10-02)

| Work | Status | Where |
|---|---|---|
| A Body of Doctrinal Divinity | have | CCEL `doctrinal` (`gill-doctrinal-divinity`) |
| A Body of Practical Divinity | have | CCEL `practical` (`gill-practical-divinity`) |
| An Exposition of the Book of Solomon's Song | have | CCEL `song` (`gill-solomons-song`) |
| The Cause of God and Truth (London: Tegg, 1838) | have-raw | IA `causeofgodtruthi00gill` |
| A Collection of Sermons and Tracts (London: G. Keith, 1773), 2 vols | have-raw | IA `collectionofserm01gill`, `collectionofserm02gill` |
| An Exposition of the Old Testament; of the New Testament (9 vols) | pending | only scattered 18th-century volumes on IA; no complete set verified |
| Modern retypings (Parisis uploads, 2016 compilation) and 1970s-80s reprints | excluded | no library provenance, or not PD scans |

## William Guthrie (round 4, my pick, 2026-10-02)

| Work | Status | Where |
|---|---|---|
| The Christian's Great Interest, in two parts | have | CCEL `interest2` (`guthrie-christians-great-interest`) |
| Printings of 1750, 1763, 1825, 1833 | alternate | CCEL's clean text is held |
| A Collection of Lectures and Sermons (ed. John Howie, 1779, 1809) | excluded here | many Covenanting preachers, Guthrie among them; would suit a Covenanters shelf |

## Robert Leighton (round 4, my pick, 2026-10-02)

No CCEL or Gutenberg text. The Whole Works (London: James Duncan, 1830, ed. Pearson, 4 vols) as raw IA OCR; the Commentary on 1 Peter falls in vols. I-II by name counts.

| Work | Status | Where |
|---|---|---|
| The Whole Works, vols. I-IV (1830) | have-raw | IA `wholeworksofmost01leig`..`04leig` |
| Works of 1805 (6 vols), 1822, 1825, 1828, 1846, 1853, 1862; separate Commentaries on 1 Peter | alternate | the 1830 edition is held |
| Robert Leighton (1858-1934), novelist | excluded | another man |

## Joseph Alleine (round 4, my pick, 2026-10-02)

No CCEL or Gutenberg text; all raw IA OCR.

| Work | Status | Where |
|---|---|---|
| An Alarm to Unconverted Sinners (American Tract Society, 1834) | have-raw | IA `alarmtounconver00alle` |
| Alleine on the Promises (Baltimore, 1828) | have-raw | IA `alleineonpromis00nichgoog` |
| The Life and Death of Joseph Alleine (Baxter, Theodosia Alleine and others) with his Christian Letters (1815) | have-raw | IA `anaccountoftheli00baxtuoft`; the Life is by others, the Letters are his |
| Other printings of the Alarm (1689-1855, under several titles) | alternate | the 1834 printing is held |
| Heaven Opened | excluded | chiefly Richard Alleine's |

## William Perkins (round 4, my pick, 2026-10-02)

No CCEL, Gutenberg or later collected edition. The Workes (printed by John Legatt, 1616-1618, 3 vols) from EEBO scans, raw IA OCR, rough (71-77%).

| Work | Status | Where |
|---|---|---|
| The Workes, vols. 1-3 (1616, 1617, 1618) | have-raw | IA `bim_early-english-books-1475-1640_the-workes-of-that-famou_perkins-william_1616_1`, `_1617_2`, `_1618_3` |
| Workes of 1603-1635, broken sets; separate treatises | alternate | the 1616-18 set is held |
| Sir William Perkins (d. 1696); Francis Perkins's almanacs | excluded | other men |

## Andrew Murray (round 4, my pick, 2026-10-02)

Devotional books, all published before his death in 1917: eleven clean from CCEL, five from Gutenberg.

| Work | Status | Where |
|---|---|---|
| The Two Covenants; The Deeper Christian Life; The Master's Indwelling; The Lord's Table; The New Life; The School of Obedience; With Christ in the School of Prayer; Absolute Surrender; The True Vine; Waiting on God; Working for God | have | CCEL `m/murray` (`amurray-*`) |
| Holy in Christ; Humility; The Ministry of Intercession; 'Jesus Himself' (1893); Money | have | Gutenberg 26990, 57121, 29296, 26003, 41994 |
| Lord, Teach Us To Pray (1896) | alternate | 71% of it is in the School of Prayer, which is held |
| The Spirit-Filled Life (Gutenberg 33247) | excluded | by John MacNeil; Murray's introduction only |
# Classical (English translations)

## Plato (tr. Jowett)

Shelf: `pipeline/plato_shelf.json`. Jowett, *The Dialogues of Plato*, 3rd ed. (Oxford, 1892), PD. Gutenberg per-dialogue texts (clean, with Jowett's introductions and analyses) plus the 1892 Clarendon five-volume set as raw OCR. Units are paragraphs: the Gutenberg texts carry no Stephanus numbers, so no unit claims Stephanus precision. Not yet minted (no uid minting during a burst).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Charmides (1892 vol. 1) | Benjamin Jowett | `plato-charmides` | have (PG 1580) |
| Lysis (1892 vol. 1) | Benjamin Jowett | `plato-lysis` | have (PG 1579) |
| Laches (1892 vol. 1) | Benjamin Jowett | `plato-laches` | have (PG 1584) |
| Protagoras (1892 vol. 1) | Benjamin Jowett | `plato-protagoras` | have (PG 1591) |
| Euthydemus (1892 vol. 1) | Benjamin Jowett | `plato-euthydemus` | have (PG 1598) |
| Cratylus (1892 vol. 1) | Benjamin Jowett | `plato-cratylus` | have (PG 1616) |
| Phaedrus (1892 vol. 1) | Benjamin Jowett | `plato-phaedrus` | have (PG 1636) |
| Ion (1892 vol. 1) | Benjamin Jowett | `plato-ion` | have (PG 1635) |
| Symposium (1892 vol. 1) | Benjamin Jowett | `plato-symposium` | have (PG 1600) |
| Meno (1892 vol. 2) | Benjamin Jowett | `plato-meno` | have (PG 1643) |
| Euthyphro (1892 vol. 2) | Benjamin Jowett | `plato-euthyphro` | have (PG 1642) |
| Apology (1892 vol. 2) | Benjamin Jowett | `plato-dialogues` | cross-ref → Adler shelf (PG 1656; its shelf title over-claims Crito and Phaedo, which are here) |
| Crito (1892 vol. 2) | Benjamin Jowett | `plato-crito` | have (PG 1657) |
| Phaedo (1892 vol. 2) | Benjamin Jowett | `plato-phaedo` | have (PG 1658) |
| Gorgias (1892 vol. 2) | Benjamin Jowett | `plato-gorgias` | have (PG 1672) |
| Lesser Hippias (1892 vol. 2) | Benjamin Jowett (dubious; Jowett's Appendix I) | `plato-lesser-hippias` | have (PG 1673) |
| Alcibiades I (1892 vol. 2) | Benjamin Jowett (dubious; Appendix I) | `plato-alcibiades-1` | have (PG 1676) |
| Menexenus (1892 vol. 2) | Benjamin Jowett (Appendix I) | `plato-menexenus` | have (PG 1682) |
| Alcibiades II (1892 vol. 2) | Matthew Knight for Jowett's edition (spurious; Appendix II) | `plato-alcibiades-2` | have (PG 1677) |
| Eryxias (1892 vol. 2) | Matthew Knight for Jowett's edition (spurious; Appendix II) | `plato-eryxias` | have (PG 1681) |
| The Republic (1892 vol. 3) | Benjamin Jowett | `plato-republic` | cross-ref → Adler shelf (PG 1497, same text) |
| Timaeus (1892 vol. 3) | Benjamin Jowett | `plato-timaeus` | have (PG 1572) |
| Critias (1892 vol. 3) | Benjamin Jowett | `plato-critias` | have (PG 1571) |
| Parmenides (1892 vol. 4) | Benjamin Jowett | `plato-parmenides` | have (PG 1687) |
| Theaetetus (1892 vol. 4) | Benjamin Jowett | `plato-theaetetus` | have (PG 1726) |
| Sophist (1892 vol. 4) | Benjamin Jowett | `plato-sophist` | have (PG 1735) |
| Statesman (1892 vol. 4) | Benjamin Jowett | `plato-statesman` | have (PG 1738) |
| Philebus (1892 vol. 4) | Benjamin Jowett | `plato-philebus` | have (PG 1744) |
| Laws (1892 vol. 5) | Benjamin Jowett | `plato-laws` | have (PG 1750) |
| The Dialogues of Plato, 3rd ed. (Oxford: Clarendon, 1892), vol. 1 | Jowett | `plato-jowett-1892-v1` | have-raw (IA `b24750189_0001`) |
| The Dialogues of Plato, 3rd ed. (Oxford: Clarendon, 1892), vol. 2 | Jowett | `plato-jowett-1892-v2` | have-raw (IA `b24750189_0002`) |
| The Dialogues of Plato, 3rd ed. (Oxford: Clarendon, 1892), vol. 3 | Jowett | `plato-jowett-1892-v3` | have-raw (IA `b24750189_0003`) |
| The Dialogues of Plato, 3rd ed. (Oxford: Clarendon, 1892), vol. 4 | Jowett | `plato-jowett-1892-v4` | have-raw (IA `b24750189_0004`) |
| The Dialogues of Plato, 3rd ed. (Oxford: Clarendon, 1892), vol. 5 | Jowett | `plato-jowett-1892-v5` | have-raw (IA `b24750189_0005`) |

Pending (wishlist):

- Greater Hippias, Hipparchus, Minos, Lovers (Rivals), Theages, Clitophon, Epinomis, the Epistles, Definitions: not in Jowett's edition. PD English exists in the Bohn *Works of Plato* (Cary, Davis, Burges, 6 vols., 1848–54), of which PG has vols. 1–2 (78618, 79398); the rest want an Internet Archive set. A second-translator shelf, Adam's call.
- The Republic, Jowett's separate 3rd ed. with marginal analysis and index (PG 55201): an alternate witness of the Republic.
- The Dialogues of Plato, 1892, vol. 2 as a clean Gutenberg transcription (PG 76464, 2025): the other four volumes are not on Gutenberg yet; when they are, that is the cleanest collected edition.
- Shelley's Symposium and Ion; Thomas Taylor's complete Plato (1804): PD, other translators, not fetched.
- Perseus serves 36 English Plato texts (Loeb: Fowler, Lamb, Shorey, Bury); alternate witnesses, see `docs/perseus-census.md`.

Excluded: PG 150 (duplicate Republic, shorter introduction), PG 19840 (Euthyphro; serves a 404), PG 29441 (an index page), PG 13726 (Cary, not Jowett).

## Aristotle (tr. Ross, Oxford)

Shelf: `pipeline/aristotle_shelf.json`. The Oxford translation, ed. J. A. Smith and W. D. Ross, 12 vols. (1908–1952). Raw Internet Archive OCR, one file per volume (Edwards precedent); translator per work in the shelf. US public domain for vols. published 1930 or earlier. Not PD in the UK (several translators died after 1956). Not converted, not minted.

| Volume | Works (translator) | Slug | Status |
|---|---|---|---|
| Works of Aristotle, vol. I (1928) | Categoriae, De Interpretatione (E. M. Edghill); Analytica Priora (A. J. Jenkinson); Analytica Posteriora (G. R. G. Mure); Topica, De Sophisticis Elenchis (W. A. Pickard-Cambridge) | `aristotle-ross-v01` | have-raw (IA `worksofaristotle01arisuoft`) |
| Works of Aristotle, vol. II (1930; this copy a lithographic reprint from sheets of the first edition) | Physica (R. P. Hardie and R. K. Gaye); De Caelo (J. L. Stocks); De Generatione et Corruptione (H. H. Joachim) | `aristotle-ross-v02` | have-raw (IA `worksofaristotle0002wdro`) |
| Works of Aristotle, vol. IV (1910) | Historia Animalium (D'Arcy Wentworth Thompson) | `aristotle-ross-v04` | have-raw (IA `worksofaristotle04arisuoft`) |
| Works of Aristotle, vol. V (1912) | De Partibus Animalium (W. Ogle); De Motu and De Incessu Animalium (A. S. L. Farquharson); De Generatione Animalium (A. Platt) | `aristotle-ross-v05` | have-raw (IA `worksofaristotle05arisuoft`) |
| Works of Aristotle, vol. VI (1913) | Opuscula: De Coloribus, De Audibilibus, Physiognomonica, De Plantis, De Mirabilibus Auscultationibus, Mechanica, De Lineis Insecabilibus, Ventorum Situs, De Melisso Xenophane Gorgia (T. Loveday, E. S. Forster, L. D. Dowdall, H. H. Joachim) | `aristotle-ross-v06` | have-raw (IA `worksofaristotle06arisuoft`) |
| Works of Aristotle, vol. VII (1927) | Problemata (E. S. Forster) | `aristotle-ross-v07` | have-raw (IA `worksofaristotle07arisuoft`) |
| Works of Aristotle, vol. VIII, 2nd ed. (1928) | Metaphysica (W. D. Ross) | `aristotle-ross-v08` | have-raw (IA `theworksofaristo08arisuoft`) |
| Works of Aristotle, vol. IX (1925) | Ethica Nicomachea (W. D. Ross); Magna Moralia (St. George Stock); Ethica Eudemia, De Virtutibus et Vitiis (J. Solomon) | `aristotle-ross-v09` | have-raw (IA `theworksofaristo09arisuoft`) |
| Works of Aristotle, vol. X (1921) | Politica (Benjamin Jowett); Oeconomica (E. S. Forster); Atheniensium Respublica (Frederic G. Kenyon) | `aristotle-ross-v10` | have-raw (IA `theworksofaristo10arisuoft`) |
| Works of Aristotle, vol. XI (1924) | Rhetorica (W. Rhys Roberts); De Rhetorica ad Alexandrum (E. S. Forster); De Poetica (Ingram Bywater) | `aristotle-ross-v11` | have-raw (IA `theworksofaristo11arisuoft`) |
| Aristotle's Psychology | Aristotle's Psychology: De Anima and Parva Naturalia (William Alexander Hammond, 1902), gap-fill for vol. III, NOT the Oxford translation | `aristotle-hammond-psychology` | have-raw (IA `aristotlespsycho00arisuoft`) |
| Works of Aristotle, vol. III (1931) | Meteorologica (Webster), De Mundo (Forster), De Anima (J. A. Smith), Parva Naturalia (Beare and Ross), De Spiritu (Dobson) | — | pending: US public domain from 2027-01-01; IA `worksofaristotle03arisuoft` ready |
| Works of Aristotle, vol. XII (1952) | Select Fragments (Ross) | — | pending: 1952, renewal not checked |

Pending (wishlist): genuine pre-1931 separate issues of Meteorologica (1923), De Mundo (1914) and Parva Naturalia (1908), which are PD now; R. D. Hicks's De Anima (1907, Greek facing); a clean proofread Nicomachean Ethics (Ross) from Gutenberg if one appears.

Aristotle cross-ref: the Adler shelf already holds `aristotle-ethics` (Chase, PG 8438) and `aristotle-politics` (Jowett, PG 6762, the same translation as the Politics in Oxford vol. X).

Excluded: `meteorologica00aris` (catalogued as the 1923 separate issue, but the scan is all of vol. III and carries the 1931 De Anima); duplicate Toronto scans of vols. X–XII; Perseus English (Loeb) not used; `worksofaristotle00unse` (*Aristotle's Masterpiece*, falsely ascribed).

## Hesiod

Shelf: `pipeline/hesiod_shelf.json`. Hugh G. Evelyn-White, prose (Loeb, 1914), PD. Gutenberg, English only. Evelyn-White prints the line references in the prose, "(ll. 1-25)", 510 of them, so a line-level citation scheme is possible later; the trial conversion gives paragraph units only.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Works and Days; Theogony; Shield of Heracles; Catalogues of Women and other fragments; with the Homeric Hymns, Epigrams, Contest of Homer and Hesiod, and Homerica (one volume) | Evelyn-White | `hesiod-evelyn-white` | have (PG 348) |
| The Remains of Hesiod the Ascraean, Including the Shield of Hercules | Charles Abraham Elton (with George Chapman's Works and Days) | `hesiod-elton` | have (PG 66350) |

Pending (wishlist): When a Homer section exists, the Homeric Hymns in this volume should be cross-referenced from it, not refetched.

## Ovid

Shelf: `pipeline/ovid_shelf.json`. No single PD translator covers all of Ovid, so the translator is named per row. Henry T. Riley's literal prose (Bohn, 1851–52) is the only one that covers the whole corpus. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Metamorphoses I–VII | Riley (prose, 1851) | `ovid-riley-metamorphoses-1` | have (PG 21765) |
| Metamorphoses VIII–XV | Riley (prose, 1851) | `ovid-riley-metamorphoses-2` | have (PG 26073) |
| Metamorphoses I–XV | J. J. Howard (blank verse, 1807) | `ovid-howard-metamorphoses` | have (PG 28621) |
| Metamorphoses I–XV | Arthur Golding (verse, 1567; ed. Rouse 1904) | `ovid-golding-metamorphoses` | have-raw (IA `cu31924026559777`) |
| Metamorphoses (Garth composite, 1717) | Dryden, Garth and others | `dryden-metamorphoses` | cross-ref → Dryden shelf (lane C) |
| Metamorphoses, Dryden's own parts | Dryden | `dryden-ovid-metamorphoses` | cross-ref → Dryden shelf (lane C) |
| Amores | Riley (prose, 1852) | `ovid-riley-amores` | have (PG 47676) |
| Ars Amatoria | Riley (prose, 1852) | `ovid-riley-ars-amatoria` | have (PG 47677) |
| Remedia Amoris | Riley (prose, 1852) | `ovid-riley-remedia-amoris` | have (PG 47678) |
| Heroides, Sabinus's Responsive Epistles, Medicamina, Nux, Consolatio ad Liviam (with Amores, Ars, Remedia) | Riley (Bohn, 1852) | `ovid-riley-heroides-1852` | have-raw (IA `herodesorepistle00ovid`) |
| Fasti, Tristia, Epistulae ex Ponto, Ibis, Halieuticon | Riley (Bohn, 1851) | `ovid-riley-fasti-tristia-1851` | have-raw (IA `fastitristiapont00ovid`) |
| Heroides (Canace, Helen, Dido); Ars I; Amores I.1, I.4 | Dryden | `dryden-ovid-epistles`, `dryden-ovid-art-of-love`, `dryden-ovid-amores` | cross-ref → Dryden shelf (lane C) |
| Amores (All Ovid's Elegies) | Christopher Marlowe | — | pending: inside Marlowe's Works vol. 3 (PG 21262); belongs on a Marlowe shelf |
| Metamorphoses | Brookes More (1922–33) | — | pending: only Book I (1922) is on IA; the complete text is not cleared |
| Metamorphoses, vol. 1: Books I-VIII (Loeb, 1916) | Frank Justus Miller | `ovid-miller-metamorphoses-v1` | have-raw (IA `metamorphoses01ovid`) |
| Metamorphoses, vol. 2: Books IX-XV (Loeb, 1916) | Frank Justus Miller | `ovid-miller-metamorphoses-v2` | have-raw (IA `metamorphoseswit02oviduoft`) |
| Heroides and Amores (Loeb, 1914) | Grant Showerman | `ovid-showerman-heroides-amores` | have-raw (IA `heroidesamores00ovid`) |
| Tristia, Ex Ponto (Loeb, 1924) | Arthur Leslie Wheeler | `ovid-wheeler-tristia-ponto` | have-raw (IA `bwb_W9-CQC-386`) |

Excluded: PG 21920, *The Last Poems of Ovid* (Akrigg, 2006), a COPYRIGHTED Gutenberg eBook. Later reprints of the two Riley Bohn volumes. Modern translations (Kline and others).

## Virgil

Shelf: `pipeline/virgil_shelf.json`. Translator per row. Rhoades (verse) and Conington (prose) each cover all three works. Verse texts convert cleanly with the existing verse converter (book-level, 12-line blocks); the divisions used are recorded in the shelf. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Aeneid, Georgics, Eclogues (Poems of Virgil, Oxford 1921) | James Rhoades (verse) | `virgil-rhoades-poems-1921` | have-raw (IA `poemsofvirgi00virguoft`) |
| Eclogues | James Rhoades (verse) | `virgil-rhoades-eclogues` | have (PG 230; PG names no translator, identified by collation with Rhoades 1921) |
| Georgics | James Rhoades (verse, 1881) | `virgil-rhoades-georgics` | have (PG 232) |
| Eclogues, Georgics, Aeneid (Works of Virgil, 1880) | John Conington (prose), ed. Symonds | `virgil-conington-works-1880` | have-raw (IA `worksofvirgilvirg00rich`) |
| Aeneid | John Conington (prose), ed. Shumway 1910 | `virgil-conington-aeneid` | have (PG 73488) |
| Aeneid | J. W. Mackail (prose, 1885) | `virgil-mackail-aeneid` | have (PG 22456) |
| Eclogues and Georgics | J. W. Mackail (prose, 1889; 1910 printing) | `virgil-mackail-eclogues-georgics` | have-raw (IA `ecloguesgeorgics00virgrich`) |
| Aeneid | William Morris (verse, 1876) | `virgil-morris-aeneid` | have (PG 29358) |
| Aeneid | E. Fairfax Taylor (Spenserian stanza, 1903–07) | `virgil-taylor-aeneid` | have (PG 18466) |
| Aeneid | Rolfe Humphries (verse, 1951) | `virgil-humphries-aeneid` | have (PG 61596; US PD per Gutenberg, not PD elsewhere) |
| Aeneid | Theodore C. Williams (verse, 1910) | `aeneid-williams` | have (already in the build manifest: Perseus `phi0690.phi003.perseus-eng2`) |
| Aeneid | Dryden | `dryden-aeneid` | cross-ref → Dryden shelf (lane C) |
| Georgics | Dryden | `dryden-georgics` | cross-ref → Dryden shelf (lane C) |
| Eclogues | Dryden | `dryden-eclogues` | cross-ref → Dryden shelf (lane C) |
| Virgil, vol. 1: Eclogues, Georgics, Aeneid I-VI (Loeb, 1916) | H. Rushton Fairclough | `virgil-fairclough-v1` | have-raw (IA `virgilwithenglis01virg`) |
| Virgil, vol. 2: Aeneid VII-XII, Minor Poems (Loeb, 1918) | H. Rushton Fairclough | `virgil-fairclough-v2` | have-raw (IA `virgil0002hrus`) |
| The Georgics and Eclogues of Virgil (1915) | Theodore Chickering Williams | `virgil-williams-georgics-eclogues` | have-raw (IA `georgicseclogues1915virg`) |
| The Æneid of Virgil (1872) | Christopher Pearse Cranch | `virgil-cranch-aeneid` | have-raw (IA `cu31924026565428`) |

Pending (wishlist): Gavin Douglas's Eneados (1513, Scots), a landmark witness.

Excluded: PG 228 (Dryden; lane C), PG 20144 (a single book alongside Voltaire), PG 54717 (stage adaptations), PG 66399 (excerpts), `poemsvirgil00magoog` (no text layer).

## Homer

Shelf: `pipeline/homer_shelf.json`. Translator per title; verse and prose. Butler's Iliad is already built from Perseus; the build's Butler Odyssey is a modern revision (Power and Nagy), so the unrevised 1900 text is held here. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Iliads of Homer Translated according to the Greek | George Chapman (verse, 1611) | `homer-chapman-iliad` | have (PG 51355) |
| The Odysseys of Homer, together with the shorter poems | George Chapman (verse, 1614-16; Hymns, Batrachomyomachia, Epigrams) | `homer-chapman-odyssey` | have (PG 48895) |
| The Iliad | Alexander Pope (verse, 1715-20), notes by T. A. Buckley | `homer-pope-iliad` | have (PG 6130) |
| The Odyssey | Alexander Pope, with William Broome and Elijah Fenton (verse, 1725-26) | `homer-pope-odyssey` | have (PG 3160) |
| The Iliad of Homer Translated into English Blank Verse | William Cowper (1791), ed. Robert Southey | `homer-cowper-iliad` | have (PG 16452) |
| The Odyssey of Homer | William Cowper (blank verse, 1791) | `homer-cowper-odyssey` | have (PG 24269) |
| The Iliad | Edward Stanley, Earl of Derby (blank verse, 1864) | `homer-derby-iliad` | have (PG 6150) |
| The Iliad | Theodore Alois Buckley (prose, Bohn, 1851) | `homer-buckley-iliad` | have (PG 22382) |
| The Odyssey Rendered into English prose | Samuel Butler (prose, 1900), unrevised | `homer-butler-odyssey` | have (PG 1727) |
| The Iliad of Homer, translated into English blank verse, vol. 1 (1875 printing) | William Cullen Bryant | `homer-bryant-iliad-v1` | have-raw (IA `iliadofhomertran01homeuoft`) |
| The Iliad of Homer, translated into English blank verse, vol. 2 (1875 printing) | William Cullen Bryant | `homer-bryant-iliad-v2` | have-raw (IA `iliadofhomertran02homeuoft`) |
| The Odyssey of Homer, translated into English blank verse, vol. 1 (1873 printing) | William Cullen Bryant | `homer-bryant-odyssey-v1` | have-raw (IA `odysseyofhomertr11homeuoft`) |
| The Odyssey of Homer, translated into English blank verse, vol. 2 (1873 printing) | William Cullen Bryant | `homer-bryant-odyssey-v2` | have-raw (IA `odysseyofhomertr22homeuoft`) |
| — | — | `iliad-butler` | cross-ref → build manifest (fetch_sources.PERSEUS), Butler's Iliad 1898; PG 2199 is the same translation, not fetched |
| — | — | `odyssey-eng4` | cross-ref → build manifest (fetch_sources.PERSEUS): Butler's Odyssey revised by Timothy Power and Gregory Nagy, a modern revision; homer-butler-odyssey here is the unrevised 1900 text |
| — | — | `lang-iliad` | cross-ref → Lang shelf, lane D (PG 3059, Lang, Leaf and Myers) |
| — | — | `lang-odyssey` | cross-ref → Lang shelf, lane D (PG 1728, Butcher and Lang) |
| — | — | `lang-homeric-hymns` | cross-ref → Lang shelf, lane D (PG 16338) |
| — | — | `dryden-iliad` | cross-ref → Dryden shelf, lane C (Iliad I and the Last Parting of Hector and Andromache) |
| — | — | `hesiod-evelyn-white` | cross-ref → Hesiod shelf: Evelyn-White's Homeric Hymns, Epigrams, Contest of Homer and Hesiod (1914) |
| Homer, The Iliad, or Achilles' Wrath at the Siege of Ilion, in English blank verse (1864) | T. S. Norgate (attributed by catalogue) | `homer-norgate-iliad` | have-raw (IA `iliadorachillesw00homeuoft`) |
| The English Works of Thomas Hobbes, vol. 10: Homer's Iliads and Odysses (ed. Molesworth) | Thomas Hobbes | `homer-hobbes-iliad-odyssey` | have-raw (IA `englishworksofth0010hobb_d2j3`) |
| Iliad | Augustus Taber Murray | `homer-perseus-murray-iliad` | have (Perseus TEI `tlg0012.tlg001.perseus-eng3`; markup CC BY-SA 4.0) |
| Odyssey | Augustus Taber Murray | `homer-perseus-murray-odyssey` | have (Perseus TEI `tlg0012.tlg002.perseus-eng3`; markup CC BY-SA 4.0) |

Pending (wishlist): A. T. Murray's Loeb Iliad (1924-25) and Odyssey (1919), on Perseus, US PD by date; 

Excluded: PG 2199 (Butler Iliad, already built), PG 28797 (duplicate Butler Odyssey), PG 24856 (schoolbook adaptation).

## Aeschylus

Shelf: `pipeline/aeschylus_shelf.json`. Translator per title; complete in Plumptre and in Blackie. Clean Gutenberg throughout. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Aeschylos: Tragedies and Fragments | E. H. Plumptre (verse), all seven plays and the fragments | `aeschylus-plumptre` | have (PG 53174) |
| The Lyrical Dramas of Aeschylus | John Stuart Blackie (verse, 1850) | `aeschylus-blackie` | have (PG 59225) |
| The House of Atreus: Agamemnon, Libation-Bearers, Furies | E. D. A. Morshead (verse, 1881) | `aeschylus-morshead-atreus` | have (PG 8604) |
| Four Plays of Aeschylus: Suppliant Maidens, Persians, Seven against Thebes, Prometheus Bound | E. D. A. Morshead (verse) | `aeschylus-morshead-four` | have (PG 8714) |
| Prometheus Bound and the Seven Against Thebes | Theodore Alois Buckley (prose, Bohn) | `aeschylus-buckley-prometheus-seven` | have (PG 27458) |
| The Agamemnon of Aeschylus, translated into English rhyming verse | Gilbert Murray; US PD per Gutenberg | `aeschylus-murray-agamemnon` | have (PG 14417) |
| The Greek Tragic Theatre, vol. 1: Aeschylus (new ed., 1809) | Robert Potter | `aeschylus-potter-greek-tragic-theatre` | have-raw (IA `greektragicthea01wodhgoog`) |
| The Dramas of Aeschylus (4th ed., revised, 1899) | Anna Swanwick | `aeschylus-swanwick` | have-raw (IA `dramasofaeschylu0000unse`) |
| Agamemnon | Robert Browning | `aeschylus-perseus-browning-agamemnon` | have (Perseus TEI `tlg0085.tlg005.perseus-eng4`; markup CC BY-SA 4.0) |

Pending (wishlist): H. W. Smyth's Loeb (1922-26), on Perseus, US PD by date; Robert Browning's Agamemnon (1877).

Excluded: PG 7073 (Goldwin Smith's Specimens: excerpts).

## Euripides

Shelf: `pipeline/euripides_shelf.json`. Translator per title; complete in Way (verse, 1894-98) and in Coleridge (prose, 1891), both raw IA OCR (clean-word 0.88-0.92). Murray's plays: US PD per Gutenberg, not PD in life+70 countries. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Tragedies of Euripides, Volume I: Hecuba, Orestes, Phoenissae, Medea, Hippolytus, Alcestis, Andromache, Suppliants, Iphigenia in Aulis, Iphigenia in Tauris | Theodore Alois Buckley (prose, Bohn, 1850) | `euripides-buckley-v1` | have (PG 15081) |
| Hecuba and other plays (Morley's Universal Library, 1888) | Michael Wodhull (verse, 1782) | `euripides-wodhull-hecuba` | have (PG 77336) |
| Hippolytus; The Bacchae | Gilbert Murray (verse) | `euripides-murray-hippolytus-bacchae` | have (PG 8418) |
| The Trojan Women of Euripides | Gilbert Murray (verse) | `euripides-murray-trojan-women` | have (PG 10096) |
| The Electra of Euripides | Gilbert Murray (verse) | `euripides-murray-electra` | have (PG 14322) |
| Medea of Euripides | Gilbert Murray (verse) | `euripides-murray-medea` | have (PG 35451) |
| The Iphigenia in Tauris of Euripides | Gilbert Murray (verse) | `euripides-murray-iphigenia-tauris` | have (PG 5063) |
| The Rhesus of Euripides | Gilbert Murray (verse) | `euripides-murray-rhesus` | have (PG 35170) |
| Alcestis | Gilbert Murray (verse) | `euripides-murray-alcestis` | have (PG 10523) |
| The Tragedies of Euripides in English Verse, vol. 1 (1894) | Arthur S. Way | `euripides-way-1894-v1` | have-raw (IA `tragediesofeurip01euriuoft`) |
| The Tragedies of Euripides in English Verse, vol. 2 (1896) | Arthur S. Way | `euripides-way-1894-v2` | have-raw (IA `tragediesofeurip02euriuoft`) |
| The Tragedies of Euripides in English Verse, vol. 3 (1898) | Arthur S. Way | `euripides-way-1894-v3` | have-raw (IA `tragediesofeurip03euriuoft`) |
| The Plays of Euripides, translated into English prose, vol. 1 (1891) | Edward P. Coleridge | `euripides-coleridge-1891-v1` | have-raw (IA `playseuripides01colegoog`) |
| The Plays of Euripides, translated into English prose, vol. 2 (1891) | Edward P. Coleridge | `euripides-coleridge-1891-v2` | have-raw (IA `playseuripides00colegoog`) |
| The Greek Tragic Theatre, vol. 3: Euripides (new ed., 1809) | Michael Wodhull | `euripides-wodhull-v3` | have-raw (IA `greektragictheat03pott`) |
| The Greek Tragic Theatre, vol. 4: Euripides (new ed., 1809) | Michael Wodhull | `euripides-wodhull-v4` | have-raw (IA `greektragictheat04pott`) |
| The Greek Tragic Theatre, vol. 5: Euripides (new ed., 1809) | Michael Wodhull | `euripides-wodhull-v5` | have-raw (IA `greektragicthea02wodhgoog`) |
| Rhesus | Gilbert Murray | `euripides-perseus-murray-rhesus` | have (Perseus TEI `tlg0006.tlg019.perseus-eng4`; markup CC BY-SA 4.0) |

Pending (wishlist): Buckley vol. II; Way's 1912 Loeb (Greek facing); Robert Potter's Euripides (1781-83). Wodhull's Euripides is held complete from the 1809 Greek Tragic Theatre (vols. 3-5).

Excluded: PG 35171 and 35173 (duplicate Murray Trojan Women and Bacchae).

## Sophocles

Shelf: `pipeline/sophocles_shelf.json`. Translator per title. Jebb's seven prose plays come from Perseus in the unmerged Thayer/Sophocles PR and are cross-referenced. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Seven Plays in English Verse | Lewis Campbell (verse, 1883) | `sophocles-campbell-seven` | have (PG 14484) |
| Plays of Sophocles: Oedipus the King; Oedipus at Colonus; Antigone | Francis Storr (verse, Loeb 1912) | `sophocles-storr-theban` | have (PG 31) |
| Oedipus King of Thebes | Gilbert Murray (rhyming verse) | `sophocles-murray-oedipus` | have (PG 27673) |
| The Philoctetes of Sophocles | Thomas Sheridan (1725) | `sophocles-sheridan-philoctetes` | have (PG 77548) |
| — | — | `sophocles-trachiniae-jebb` | cross-ref → Jebb prose (Perseus), in the unmerged Thayer/Sophocles PR |
| — | — | `sophocles-antigone-jebb` | cross-ref → Jebb prose (Perseus), in the unmerged Thayer/Sophocles PR |
| — | — | `sophocles-ajax-jebb` | cross-ref → Jebb prose (Perseus), in the unmerged Thayer/Sophocles PR |
| — | — | `sophocles-oedipus-tyrannus-jebb` | cross-ref → Jebb prose (Perseus), in the unmerged Thayer/Sophocles PR |
| — | — | `sophocles-electra-jebb` | cross-ref → Jebb prose (Perseus), in the unmerged Thayer/Sophocles PR |
| — | — | `sophocles-philoctetes-jebb` | cross-ref → Jebb prose (Perseus), in the unmerged Thayer/Sophocles PR |
| — | — | `sophocles-oedipus-colonus-jebb` | cross-ref → Jebb prose (Perseus), in the unmerged Thayer/Sophocles PR |
| The Tragedies of Sophocles, a new translation (1865) | E. H. Plumptre | `sophocles-plumptre` | have-raw (IA `tragediesofsopho1865soph`) |
| The Tragedies of Sophocles, from the Greek (London, 1759; all seven plays in this scan) | Thomas Francklin | `sophocles-francklin-1759` | have-raw (IA `tragediesofsopho00soph`) |

Pending (wishlist): vol. 2 of the 1809 Greek Tragic Theatre (Francklin's Sophocles in Potter's set; archive.org answers 503), wanted only to complete that set; Storr's Loeb vol. 2 (Ajax, Electra, Trachiniae, Philoctetes).

Excluded: PG 806 (McNamee, a COPYRIGHTED Gutenberg eBook), PG 7073 (excerpts).

## Aristophanes

Shelf: `pipeline/aristophanes_shelf.json`. Translator per title; complete in the Athenian Society's anonymous literal translation (1912). Duplicates among Gutenberg's single plays were found by shingle overlap. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Eleven Comedies, vol. 1: Knights, Acharnians, Peace, Lysistrata, The Clouds | anonymous (The Athenian Society, 1912) | `aristophanes-athenian-v1` | have (PG 8688) |
| The Eleven Comedies, vol. 2: Wasps, Birds, Frogs, Thesmophoriazusae, Ecclesiazusae, Plutus | anonymous (The Athenian Society, 1912) | `aristophanes-athenian-v2` | have (PG 8689) |
| The Clouds | W. J. Hickie (prose, Bohn) | `aristophanes-hickie-clouds` | have (PG 2562) |
| The Frogs | Benjamin Bickley Rogers (verse) | `aristophanes-rogers-frogs` | have (PG 7998) |
| Lysistrata | Jack Lindsay (1926); US PD per Gutenberg | `aristophanes-lindsay-lysistrata` | have (PG 7700) |

Pending (wishlist): B. B. Rogers's complete verse Aristophanes (1902-16); J. Hookham Frere's four plays (1840).

Excluded: PG 3012, 2571, 3013 (the Athenian Society translation split into single plays).

## Herodotus

Shelf: `pipeline/herodotus_shelf.json`. Macaulay complete across two shelves (vol. 1 on Adler, vol. 2 here); Rawlinson complete, raw IA (clean-word 0.85-0.88). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The History of Herodotus, vol. 2 (Books V-IX) | G. C. Macaulay (prose, 1890) | `herodotus-macaulay-v2` | have (PG 2456) |
| History of Herodotus: a new English version, vol. 1 (1861 printing) | George Rawlinson | `herodotus-rawlinson-v1` | have-raw (IA `historyofherodot01herouoft`) |
| History of Herodotus: a new English version, vol. 2 (1861 printing) | George Rawlinson | `herodotus-rawlinson-v2` | have-raw (IA `historyofherod02hero`) |
| History of Herodotus: a new English version, vol. 3 (1861 printing) | George Rawlinson | `herodotus-rawlinson-v3` | have-raw (IA `c2historyofherod03hero`) |
| History of Herodotus: a new English version, vol. 4 (1861 printing) | George Rawlinson | `herodotus-rawlinson-v4` | have-raw (IA `historyofherod04hero`) |
| — | — | `herodotus-history` | cross-ref → Adler shelf (pipeline/adler_shelf.json): PG 2707, Macaulay vol. 1 (Books I-IV) only, although that shelf's title reads as the whole History |
| Herodotus: a New and Literal Version from the Text of Baehr (Harper, 1873) | Henry Cary | `herodotus-cary` | have-raw (IA `herodotusnewlite0000hero`) |

Pending (wishlist): A. D. Godley's Loeb (1920-25), on Perseus.

Excluded: PG 2131 (an extract of Book II), PG 55758 (adaptation).

## Thucydides

Shelf: `pipeline/thucydides_shelf.json`. Jowett's own Thucydides (1881) and Hobbes's (1629, Oxford 1841 corrected edition), raw IA. Crawley is on the Adler shelf. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Thucydides translated into English, vol. 1 (Oxford, 1881) | Benjamin Jowett | `thucydides-jowett-1881-v1` | have-raw (IA `a609583001thucuoft`) |
| Thucydides translated into English, vol. 2: notes (Oxford, 1881) | Benjamin Jowett | `thucydides-jowett-1881-v2` | have-raw (IA `a609583002thucuoft`) |
| Thucydides, chiefly from the translation of Hobbes of Malmesbury (Oxford, 1841) | Thomas Hobbes (1629), corrected | `thucydides-hobbes-1841` | have-raw (IA `thucydides00thucuoft`) |
| — | — | `thucydides-pelo` | cross-ref → Adler shelf: PG 7142, which is Richard CRAWLEY's translation; the Adler shelf labels it 'tr. Jowett', which is wrong (PG 7142's own header names Crawley) |
| Thucydides, tr. by W. Smith, vol. 1 (1831) | William Smith | `thucydides-smith-v1` | have-raw (IA `thucydidestrbyw01thucgoog`) |
| Thucydides, tr. by W. Smith, vol. 2 (1831) | William Smith | `thucydides-smith-v2` | have-raw (IA `thucydides01smitgoog`) |
| Thucydides, tr. by W. Smith, vol. 3 (1831) | William Smith | `thucydides-smith-v3` | have-raw (IA `thucydidestrbyw02thucgoog`) |
| History of the Peloponnesian War | Charles Foster Smith | `thucydides-perseus-smith-history-of-the-peloponnesian-war` | have (Perseus TEI `tlg0003.tlg001.1st1K-eng1`; markup CC BY-SA 4.0) |
| History of the Peloponnesian War | Henry Dale | `thucydides-perseus-dale-history-of-the-peloponnesian-war` | have (Perseus TEI `tlg0003.tlg001.1st1K-eng2`; markup CC BY-SA 4.0) |
| The History of the Grecian War | Thomas Hobbes | `thucydides-perseus-hobbes-the-history-of-the-grecian-war` | have (Perseus TEI `tlg0003.tlg001.perseus-eng4`; markup CC BY-SA 4.0) |

Pending (wishlist): C. F. Smith's Loeb (1919-23), on Perseus; 

Excluded: PG 26245 (duplicate Crawley), PG 9074 (adaptation).

## Xenophon

Shelf: `pipeline/xenophon_shelf.json`. Dakyns's complete Works of Xenophon (1890-97), one clean Gutenberg text per work. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Anabasis | H. G. Dakyns | `xenophon-anabasis` | have (PG 1170) |
| Hellenica | H. G. Dakyns | `xenophon-hellenica` | have (PG 1174) |
| Cyropaedia: The Education of Cyrus | H. G. Dakyns | `xenophon-cyropaedia` | have (PG 2085) |
| The Memorabilia | H. G. Dakyns | `xenophon-memorabilia` | have (PG 1177) |
| The Symposium | H. G. Dakyns | `xenophon-symposium` | have (PG 1181) |
| The Apology | H. G. Dakyns | `xenophon-apology` | have (PG 1171) |
| The Economist (Oeconomicus) | H. G. Dakyns | `xenophon-economist` | have (PG 1173) |
| Agesilaus | H. G. Dakyns | `xenophon-agesilaus` | have (PG 1169) |
| Hiero | H. G. Dakyns | `xenophon-hiero` | have (PG 1175) |
| The Polity of the Athenians and the Lacedaemonians | H. G. Dakyns | `xenophon-polity` | have (PG 1178) |
| On Revenues | H. G. Dakyns | `xenophon-revenues` | have (PG 1179) |
| The Cavalry General | H. G. Dakyns | `xenophon-cavalry-general` | have (PG 1172) |
| On Horsemanship | H. G. Dakyns | `xenophon-horsemanship` | have (PG 1176) |
| The Sportsman (Cynegeticus) | H. G. Dakyns | `xenophon-sportsman` | have (PG 1180) |
| The Memorable Thoughts of Socrates | Edward Bysshe (1712) | `xenophon-bysshe-memorabilia` | have (PG 17490) |

Pending (wishlist): E. C. Marchant's and Carleton Brownson's Loebs, on Perseus.

Excluded: PG 29459 (index), PG 22003 (Anabasis I-IV only).

## Polybius

Shelf: `pipeline/polybius_shelf.json`. Shuckburgh (1889), complete, clean Gutenberg. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Histories of Polybius, vol. 1 | Evelyn S. Shuckburgh (1889) | `polybius-shuckburgh-v1` | have (PG 44125) |
| The Histories of Polybius, vol. 2 | Evelyn S. Shuckburgh (1889) | `polybius-shuckburgh-v2` | have (PG 44126) |
| — | — | `dryden-polybius-lucian` | cross-ref → Dryden shelf (lane C): Dryden's character of Polybius |
| The General History of Polybius, vol. 1 (1772) | James Hampton | `polybius-hampton-v1` | have-raw (IA `bim_eighteenth-century_the-general-history-of-p_polybius_1772_1`) |
| The General History of Polybius, vol. 2 (1772) | James Hampton | `polybius-hampton-v2` | have-raw (IA `generalhistoryof02poly`) |
| The General History of Polybius, vol. 3 (1773; volume per catalogue) | James Hampton | `polybius-hampton-v3` | have-raw (IA `generalhistoryof03poly`) |
| The General History of Polybius, vol. 4 (1773) | James Hampton | `polybius-hampton-v4` | have-raw (IA `generalhistoryof04poly`) |

Pending (wishlist): W. R. Paton's Loeb (1922-27), on Perseus; 

## Arrian

Shelf: `pipeline/arrian_shelf.json`. Chinnock's Anabasis (1884) and Dansey's On Coursing (1831), clean Gutenberg. Epictetus's Discourses, which Arrian recorded, are shelved under Epictetus. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Anabasis of Alexander | E. J. Chinnock (1884) | `arrian-chinnock-anabasis` | have (PG 46976) |
| Arrian on Coursing (Cynegeticus) | William Dansey (1831) | `arrian-dansey-coursing` | have (PG 78013) |

Pending (wishlist): Chinnock's Indica; Hooke's 1729 Arrian.

## Plutarch

Shelf: `pipeline/plutarch_shelf.json`. Translator per title. Lives complete three times over: North (1579, Tudor Translations 1895-96, raw), Langhorne (1770, raw), Stewart and Long (Bohn, clean); the Dryden-Clough Lives is on the Adler shelf. Moralia: the Goodwin edition (several hands, 1870, 5 vols.) and Bohn's Shilleto, clean. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Plutarch's Lives, vol. 1 (of 4) | Aubrey Stewart and George Long (Bohn, 1880-82) | `plutarch-stewart-long-lives-v1` | have (PG 14033) |
| Plutarch's Lives, vol. 2 (of 4) | Aubrey Stewart and George Long (Bohn, 1880-82) | `plutarch-stewart-long-lives-v2` | have (PG 14114) |
| Plutarch's Lives, vol. 3 (of 4) | Aubrey Stewart and George Long (Bohn, 1880-82) | `plutarch-stewart-long-lives-v3` | have (PG 14140) |
| Plutarch's Lives, vol. 4 (of 4) | Aubrey Stewart and George Long (Bohn, 1880-82) | `plutarch-stewart-long-lives-v4` | have (PG 44315) |
| Plutarch's Essays and Miscellanies, vol. 1 (of 5) | several hands, ed. William W. Goodwin (1870) | `plutarch-goodwin-moralia-v1` | have (PG 78134) |
| Plutarch's Essays and Miscellanies, vol. 2 (of 5) | several hands, ed. William W. Goodwin (1870) | `plutarch-goodwin-moralia-v2` | have (PG 78147) |
| Plutarch's Essays and Miscellanies, vol. 3 (of 5) | several hands, ed. William W. Goodwin (1870) | `plutarch-goodwin-moralia-v3` | have (PG 78851) |
| Plutarch's Essays and Miscellanies, vol. 4 (of 5) | several hands, ed. William W. Goodwin (1870) | `plutarch-goodwin-moralia-v4` | have (PG 79588) |
| Plutarch's Essays and Miscellanies, vol. 5 (of 5) | several hands, ed. William W. Goodwin (1870) | `plutarch-goodwin-moralia-v5` | have (PG 78000) |
| Plutarch's Morals | A. R. Shilleto (Bohn) | `plutarch-shilleto-morals` | have (PG 23639) |
| Plutarch's Romane Questions | Philemon Holland (1603), ed. F. B. Jevons (1892) | `plutarch-holland-roman-questions` | have (PG 57513) |
| Plutarch on the Delay of the Divine Justice | Andrew P. Peabody | `plutarch-peabody-delay` | have (PG 58567) |
| Selected Essays of Plutarch, vol. I | T. G. Tucker | `plutarch-tucker-essays` | have (PG 62618) |
| Selected Essays of Plutarch, vol. II | A. O. Prickard | `plutarch-prickard-essays` | have (PG 62858) |
| Lives of the Noble Grecians and Romans, vol. 1 (Tudor Translations, 1895-96) | Sir Thomas North (1579) | `plutarch-north-lives-v1` | have-raw (IA `plutarchslivesn03accigoog`) |
| Lives of the Noble Grecians and Romans, vol. 2 (Tudor Translations, 1895-96) | Sir Thomas North (1579) | `plutarch-north-lives-v2` | have-raw (IA `plutarchslivesn01accigoog`) |
| Lives of the Noble Grecians and Romans, vol. 3 (Tudor Translations, 1895-96) | Sir Thomas North (1579) | `plutarch-north-lives-v3` | have-raw (IA `plutarchslivesn04accigoog`) |
| Lives of the Noble Grecians and Romans, vol. 4 (Tudor Translations, 1895-96) | Sir Thomas North (1579) | `plutarch-north-lives-v4` | have-raw (IA `plutarchslivesn00accigoog`) |
| Lives of the Noble Grecians and Romans, vol. 5 (Tudor Translations, 1895-96) | Sir Thomas North (1579) | `plutarch-north-lives-v5` | have-raw (IA `plutarchslivesn06accigoog`) |
| Lives of the Noble Grecians and Romans, vol. 6 (Tudor Translations, 1895-96) | Sir Thomas North (1579) | `plutarch-north-lives-v6` | have-raw (IA `plutarchslivesn02accigoog`) |
| Plutarch's Lives, translated from the original Greek, vol. 1 (1813 printing) | John and William Langhorne (1770) | `plutarch-langhorne-lives-v1` | have-raw (IA `livestranslatedf01plutuoft`) |
| Plutarch's Lives, translated from the original Greek, vol. 2 (1813 printing) | John and William Langhorne (1770) | `plutarch-langhorne-lives-v2` | have-raw (IA `livestranslatedf02plutuoft`) |
| Plutarch's Lives, translated from the original Greek, vol. 3 (1813 printing) | John and William Langhorne (1770) | `plutarch-langhorne-lives-v3` | have-raw (IA `livestranslatedf03plutuoft`) |
| Plutarch's Lives, translated from the original Greek, vol. 4 (1844-46 printing) | John and William Langhorne (1770) | `plutarch-langhorne-lives-v4` | have-raw (IA `livestranslatedf04plutuoft`) |
| Plutarch's Lives, translated from the original Greek, vol. 5 (1813 printing) | John and William Langhorne (1770) | `plutarch-langhorne-lives-v5` | have-raw (IA `livestranslatedf05plutuoft`) |
| Plutarch's Lives, translated from the original Greek, vol. 6 (1813 printing) | John and William Langhorne (1770) | `plutarch-langhorne-lives-v6` | have-raw (IA `livestranslatedf06plutuoft`) |
| — | — | `plutarch-lives` | cross-ref → Adler shelf: PG 674, the Dryden-and-others translation revised by A. H. Clough (1859); Adler labels it 'tr. Dryden/Clough' |
| A discourse to an unlearned prince | John Kersey | `plutarch-perseus-kersey-a-discourse-to-an-unlearned-prince` | have (Perseus TEI `tlg0007.tlg116.perseus-eng4`; markup CC BY-SA 4.0) |
| Against Colotes, the Disciple and Favorite of Epicurus. | A. G. | `plutarch-perseus-g-against-colotes-the-disciple-and-favorit` | have (Perseus TEI `tlg0007.tlg140.perseus-eng2`; markup CC BY-SA 4.0) |
| Five Tragical Histories of Love | A.I. | `plutarch-perseus-ai-five-tragical-histories-of-love` | have (Perseus TEI `tlg0007.tlg114.perseus-eng4`; markup CC BY-SA 4.0) |
| Of Love. | John Philips | `plutarch-perseus-philips-of-love` | have (Perseus TEI `tlg0007.tlg113.perseus-eng2`; markup CC BY-SA 4.0) |
| Whether 'Twere Rightly Said, Live Concealed. | Charles Whitaker | `plutarch-perseus-whitaker-whether-twere-rightly-said-live-conceale` | have (Perseus TEI `tlg0007.tlg141.perseus-eng2`; markup CC BY-SA 4.0) |
| That Virtue May Be Taught | John Patrick | `plutarch-perseus-patrick-that-virtue-may-be-taught` | have (Perseus TEI `tlg0007.tlg093.perseus-eng4`; markup CC BY-SA 4.0) |
| Whether an Aged Man Ought to Meddle in State Affairs. | F. Fetherston | `plutarch-perseus-fetherston-whether-an-aged-man-ought-to-meddle-in-s` | have (Perseus TEI `tlg0007.tlg117.perseus-eng4`; markup CC BY-SA 4.0) |
| Whether vice is sufficient to render a man unhappy | Samuel White | `plutarch-perseus-white-whether-vice-is-sufficient-to-render-a-m` | have (Perseus TEI `tlg0007.tlg099.perseus-eng4`; markup CC BY-SA 4.0) |
| Whether the Passions of the Soul or Diseases of the Body Are Worse | Samuel White | `plutarch-perseus-white-whether-the-passions-of-the-soul-or-dise` | have (Perseus TEI `tlg0007.tlg100.perseus-eng4`; markup CC BY-SA 4.0) |
| Laconic Apophthegms; or Remarkable Sayings of the Spartans. | unnamed (as in the Perseus header) | `plutarch-perseus-anon-laconic-apophthegms-or-remarkable-saying` | have (Perseus TEI `tlg0007.tlg082.perseus-eng4`; markup CC BY-SA 4.0) |
| Whether water or fire be most useful. | F. Fetherston | `plutarch-perseus-fetherston-whether-water-or-fire-be-most-useful` | have (Perseus TEI `tlg0007.tlg128.perseus-eng4`; markup CC BY-SA 4.0) |
| That brute beasts make use of reason | Sir A. J. | `plutarch-perseus-j-that-brute-beasts-make-use-of-reason` | have (Perseus TEI `tlg0007.tlg130.perseus-eng4`; markup CC BY-SA 4.0) |
| An Abstract of a Comparison Betwixt Aristophanes and Menander | William Baxter | `plutarch-perseus-baxter-an-abstract-of-a-comparison-betwixt-aris` | have (Perseus TEI `tlg0007.tlg122.perseus-eng4`; markup CC BY-SA 4.0) |
| A breviate of a discourse, showing that the Stoics speak greater improbabilities than the poets. | William Baxter | `plutarch-perseus-baxter-a-breviate-of-a-discourse-showing-that-t` | have (Perseus TEI `tlg0007.tlg137.perseus-eng2`; markup CC BY-SA 4.0) |
| Advice to Bride and Groom | Frank Cole Babbitt | `plutarch-perseus-babbitt-advice-to-bride-and-groom` | have (Perseus TEI `tlg0007.tlg078.perseus-eng3`; markup CC BY-SA 4.0) |
| Conjugal Precepts | John Philips | `plutarch-perseus-philips-conjugal-precepts` | have (Perseus TEI `tlg0007.tlg078.perseus-eng4`; markup CC BY-SA 4.0) |
| Plutarch's Consolatory Letter to His Wife | Thomas Creech | `plutarch-perseus-creech-plutarch-s-consolatory-letter-to-his-wif` | have (Perseus TEI `tlg0007.tlg111.perseus-eng2`; markup CC BY-SA 4.0) |
| A Letter of Condolence to Apollonius | Frank Cole Babbitt | `plutarch-perseus-babbitt-a-letter-of-condolence-to-apollonius` | have (Perseus TEI `tlg0007.tlg076.perseus-eng3`; markup CC BY-SA 4.0) |
| Consolation to Apollonius | Matthew Morgan | `plutarch-perseus-morgan-consolation-to-apollonius` | have (Perseus TEI `tlg0007.tlg076.perseus-eng4`; markup CC BY-SA 4.0) |
| Concerning the fortune or virtue of Alexander the Great. | John Phillips | `plutarch-perseus-phillips-concerning-the-fortune-or-virtue-of-alex` | have (Perseus TEI `tlg0007.tlg087.perseus-eng4`; markup CC BY-SA 4.0) |
| Of Natural Affection Towards One's Offspring | R. Brown | `plutarch-perseus-brown-of-natural-affection-towards-one-s-offsp` | have (Perseus TEI `tlg0007.tlg098.perseus-eng4`; markup CC BY-SA 4.0) |
| Of the Love of Wealth | John Patrick | `plutarch-perseus-patrick-of-the-love-of-wealth` | have (Perseus TEI `tlg0007.tlg103.perseus-eng2`; markup CC BY-SA 4.0) |
| Why the Oracles Cease to Give Answers | Robert Midgley | `plutarch-perseus-midgley-why-the-oracles-cease-to-give-answers` | have (Perseus TEI `tlg0007.tlg092.perseus-eng4`; markup CC BY-SA 4.0) |
| Of the word ΕΙ engraven over the gate of Apollo's temple at Delphi | R. Kippax | `plutarch-perseus-kippax-of-the-word-engraven-over-the-gate-of-ap` | have (Perseus TEI `tlg0007.tlg090.perseus-eng4`; markup CC BY-SA 4.0) |
| Of the Face Appearing Within the Orb Of the Moon | A.G. | `plutarch-perseus-ag-of-the-face-appearing-within-the-orb-of` | have (Perseus TEI `tlg0007.tlg126.perseus-eng4`; markup CC BY-SA 4.0) |
| Of Fate. | A. G. | `plutarch-perseus-g-of-fate` | have (Perseus TEI `tlg0007.tlg108.perseus-eng2`; markup CC BY-SA 4.0) |
| Of Garrulity, or Talkativeness | John Philips | `plutarch-perseus-philips-of-garrulity-or-talkativeness` | have (Perseus TEI `tlg0007.tlg101.perseus-eng4`; markup CC BY-SA 4.0) |
| A Discourse Concerning Socrates's Daemon | Thomas Creech | `plutarch-perseus-creech-a-discourse-concerning-socrates-s-daemon` | have (Perseus TEI `tlg0007.tlg109.perseus-eng2`; markup CC BY-SA 4.0) |
| Of Herodotus's Malice. | A. G. | `plutarch-perseus-g-of-herodotus-s-malice` | have (Perseus TEI `tlg0007.tlg123.perseus-eng2`; markup CC BY-SA 4.0) |
| Of Envy and Hatred | P. Lancaster | `plutarch-perseus-lancaster-of-envy-and-hatred` | have (Perseus TEI `tlg0007.tlg105.perseus-eng2`; markup CC BY-SA 4.0) |
| Of Isis and Osiris, or of the Ancient Religion and Philosophy of Egypt. | William Baxter | `plutarch-perseus-baxter-of-isis-and-osiris-or-of-the-ancient-rel` | have (Perseus TEI `tlg0007.tlg089.perseus-eng4`; markup CC BY-SA 4.0) |
| Wherefore the Pythian Priestess now Ceases to Deliver her Oracles in Verse | John Philips | `plutarch-perseus-philips-wherefore-the-pythian-priestess-now-ceas` | have (Perseus TEI `tlg0007.tlg091.perseus-eng4`; markup CC BY-SA 4.0) |
| How a Man May Inoffensively Praise Himself Without Being Liable to Envy | P. Lancaster | `plutarch-perseus-lancaster-how-a-man-may-inoffensively-praise-himse` | have (Perseus TEI `tlg0007.tlg106.perseus-eng2`; markup CC BY-SA 4.0) |
| Concerning Such Whom God is Slow to Punish | John Philips | `plutarch-perseus-philips-concerning-such-whom-god-is-slow-to-puni` | have (Perseus TEI `tlg0007.tlg107.perseus-eng2`; markup CC BY-SA 4.0) |
| The contradictions of the Stoics | E. Smith | `plutarch-perseus-smith-the-contradictions-of-the-stoics` | have (Perseus TEI `tlg0007.tlg136.perseus-eng2`; markup CC BY-SA 4.0) |
| Superstition | Frank Cole Babbitt | `plutarch-perseus-babbitt-superstition` | have (Perseus TEI `tlg0007.tlg080.perseus-eng3`; markup CC BY-SA 4.0) |
| Of Superstition, or Indiscreet Devotion | William Baxter | `plutarch-perseus-baxter-of-superstition-or-indiscreet-devotion` | have (Perseus TEI `tlg0007.tlg080.perseus-eng4`; markup CC BY-SA 4.0) |
| Of the Tranquillity of the Mind. | Matthew Morgan | `plutarch-perseus-morgan-of-the-tranquillity-of-the-mind` | have (Perseus TEI `tlg0007.tlg096.perseus-eng4`; markup CC BY-SA 4.0) |
| Of Moral Virtue | Matthew Morgan | `plutarch-perseus-morgan-of-moral-virtue` | have (Perseus TEI `tlg0007.tlg094.perseus-eng4`; markup CC BY-SA 4.0) |
| Of Bashfulness | Thomas Hoy | `plutarch-perseus-hoy-of-bashfulness` | have (Perseus TEI `tlg0007.tlg104.perseus-eng2`; markup CC BY-SA 4.0) |
| On Having Many Friends | Frank Cole Babbitt | `plutarch-perseus-babbitt-on-having-many-friends` | have (Perseus TEI `tlg0007.tlg073.perseus-eng3`; markup CC BY-SA 4.0) |
| Of Large Acquaintance: or, an Essay to Prove the Folly of Seeking Many Friends | William W. Goodwin | `plutarch-perseus-goodwin-of-large-acquaintance-or-an-essay-to-pro` | have (Perseus TEI `tlg0007.tlg073.perseus-eng4`; markup CC BY-SA 4.0) |
| Concerning the procreation of the soul as discoursed in Timaeus | John Philips | `plutarch-perseus-philips-concerning-the-procreation-of-the-soul-a` | have (Perseus TEI `tlg0007.tlg134.perseus-eng2`; markup CC BY-SA 4.0) |
| How To Profit By One's Enemies | Frank Cole Babbitt | `plutarch-perseus-babbitt-how-to-profit-by-one-s-enemies` | have (Perseus TEI `tlg0007.tlg072.perseus-eng3`; markup CC BY-SA 4.0) |
| How a man may receive advantage and profit from his enemies. | John Hartcliffe | `plutarch-perseus-hartcliffe-how-a-man-may-receive-advantage-and-prof` | have (Perseus TEI `tlg0007.tlg072.perseus-eng4`; markup CC BY-SA 4.0) |
| Concerning the cure of anger: a dialogue | William Dillingham | `plutarch-perseus-dillingham-concerning-the-cure-of-anger-a-dialogue` | have (Perseus TEI `tlg0007.tlg095.perseus-eng4`; markup CC BY-SA 4.0) |
| Of common conceptions, against the Stoics. | Samuel White | `plutarch-perseus-white-of-common-conceptions-against-the-stoics` | have (Perseus TEI `tlg0007.tlg138.perseus-eng2`; markup CC BY-SA 4.0) |
| Of Curiosity, or an Over-Busy Inquisitiveness into Things Impertinent. | Maurice Wheeler | `plutarch-perseus-wheeler-of-curiosity-or-an-over-busy-inquisitive` | have (Perseus TEI `tlg0007.tlg102.perseus-eng4`; markup CC BY-SA 4.0) |
| Of eating of flesh: Tract I. | William Baxter | `plutarch-perseus-baxter-of-eating-of-flesh-tract-i` | have (Perseus TEI `tlg0007.tlg131.perseus-eng4`; markup CC BY-SA 4.0) |
| Of eating of flesh: Tract II. | William Baxter | `plutarch-perseus-baxter-of-eating-of-flesh-tract-ii` | have (Perseus TEI `tlg0007.tlg132.perseus-eng4`; markup CC BY-SA 4.0) |
| Of Banishment, or Flying One's Country. | John Patrick | `plutarch-perseus-patrick-of-banishment-or-flying-one-s-country` | have (Perseus TEI `tlg0007.tlg110.perseus-eng2`; markup CC BY-SA 4.0) |
| Chance | Frank Cole Babbitt | `plutarch-perseus-babbitt-chance` | have (Perseus TEI `tlg0007.tlg074.perseus-eng3`; markup CC BY-SA 4.0) |
| Of Fortune | William Baxter | `plutarch-perseus-baxter-of-fortune` | have (Perseus TEI `tlg0007.tlg074.perseus-eng4`; markup CC BY-SA 4.0) |
| Concerning the fortune of the Romans | John Oswald | `plutarch-perseus-oswald-concerning-the-fortune-of-the-romans` | have (Perseus TEI `tlg0007.tlg086.perseus-eng4`; markup CC BY-SA 4.0) |
| Of Brotherly Love | John Thomson | `plutarch-perseus-thomson-of-brotherly-love` | have (Perseus TEI `tlg0007.tlg097.perseus-eng4`; markup CC BY-SA 4.0) |
| Whether the Athenians Were More Renowned For Their Warlike Achievements or For Their Learning | R. Smith | `plutarch-perseus-smith-whether-the-athenians-were-more-renowned` | have (Perseus TEI `tlg0007.tlg088.perseus-eng4`; markup CC BY-SA 4.0) |
| The Education of Children | Frank Cole Babbitt | `plutarch-perseus-babbitt-the-education-of-children` | have (Perseus TEI `tlg0007.tlg067.perseus-eng3`; markup CC BY-SA 4.0) |
| A Discourse Touching the Training of Children | Simon Ford | `plutarch-perseus-ford-a-discourse-touching-the-training-of-chi` | have (Perseus TEI `tlg0007.tlg067.perseus-eng4`; markup CC BY-SA 4.0) |
| Concerning the First Principle of Cold | F. Fetherston | `plutarch-perseus-fetherston-concerning-the-first-principle-of-cold` | have (Perseus TEI `tlg0007.tlg127.perseus-eng4`; markup CC BY-SA 4.0) |
| On Listening to Lectures | Frank Cole Babbitt | `plutarch-perseus-babbitt-on-listening-to-lectures` | have (Perseus TEI `tlg0007.tlg069.perseus-eng3`; markup CC BY-SA 4.0) |
| Of Hearing | Thomas Hoy | `plutarch-perseus-hoy-of-hearing` | have (Perseus TEI `tlg0007.tlg069.perseus-eng4`; markup CC BY-SA 4.0) |
| Which are the most crafty, water-animals or those creatures that breed upon the land? | John Philips | `plutarch-perseus-philips-which-are-the-most-crafty-water-animals` | have (Perseus TEI `tlg0007.tlg129.perseus-eng4`; markup CC BY-SA 4.0) |
| Advice About Keeping Well | Frank Cole Babbitt | `plutarch-perseus-babbitt-advice-about-keeping-well` | have (Perseus TEI `tlg0007.tlg077.perseus-eng3`; markup CC BY-SA 4.0) |
| Plutarch's Rules for the Preservation of Health | Matthew Poole | `plutarch-perseus-poole-plutarch-s-rules-for-the-preservation-of` | have (Perseus TEI `tlg0007.tlg077.perseus-eng4`; markup CC BY-SA 4.0) |
| Of the Three Sorts of Government, Monarchy, Democracy, and Oligarchy. | R. Smith | `plutarch-perseus-smith-of-the-three-sorts-of-government-monarch` | have (Perseus TEI `tlg0007.tlg119.perseus-eng4`; markup CC BY-SA 4.0) |
| Virtue and Vice | Frank Cole Babbitt | `plutarch-perseus-babbitt-virtue-and-vice` | have (Perseus TEI `tlg0007.tlg075.perseus-eng3`; markup CC BY-SA 4.0) |
| Of Virtue and Vice | William Baxter | `plutarch-perseus-baxter-of-virtue-and-vice` | have (Perseus TEI `tlg0007.tlg075.perseus-eng4`; markup CC BY-SA 4.0) |
| Against Running in Debt, or Taking up Money Upon Usury | R. Smith | `plutarch-perseus-smith-against-running-in-debt-or-taking-up-mon` | have (Perseus TEI `tlg0007.tlg120.perseus-eng4`; markup CC BY-SA 4.0) |
| That a Philosopher Ought Chiefly to Converse with Great Men | Knightly Chetwood | `plutarch-perseus-chetwood-that-a-philosopher-ought-chiefly-to-conv` | have (Perseus TEI `tlg0007.tlg115.perseus-eng4`; markup CC BY-SA 4.0) |
| Concerning the Virtues of Women | Isaac Chauncy | `plutarch-perseus-chauncy-concerning-the-virtues-of-women` | have (Perseus TEI `tlg0007.tlg083.perseus-eng4`; markup CC BY-SA 4.0) |
| That it is Not Possible to Live Pleasurably According to the Doctrine of Epicurus | William Baxter | `plutarch-perseus-baxter-that-it-is-not-possible-to-live-pleasura` | have (Perseus TEI `tlg0007.tlg139.perseus-eng2`; markup CC BY-SA 4.0) |
| Parallels, or a comparison between the Greek and Roman Histories. | John Oswald | `plutarch-perseus-oswald-parallels-or-a-comparison-between-the-gr` | have (Perseus TEI `tlg0007.tlg085.perseus-eng4`; markup CC BY-SA 4.0) |
| Plutarch's Platonic questions | R. Brown | `plutarch-perseus-brown-plutarch-s-platonic-questions` | have (Perseus TEI `tlg0007.tlg133.perseus-eng2`; markup CC BY-SA 4.0) |
| Political Precepts | Samuel White | `plutarch-perseus-white-political-precepts` | have (Perseus TEI `tlg0007.tlg118.perseus-eng4`; markup CC BY-SA 4.0) |
| Symposiacs | Thomas Creech | `plutarch-perseus-creech-symposiacs` | have (Perseus TEI `tlg0007.tlg112.perseus-eng2`; markup CC BY-SA 4.0) |
| Greek Questions | Isaac Chauncy | `plutarch-perseus-chauncy-greek-questions` | have (Perseus TEI `tlg0007.tlg084b.perseus-eng4`; markup CC BY-SA 4.0) |
| Plutarch's Natural Questions | R. Brown | `plutarch-perseus-brown-plutarch-s-natural-questions` | have (Perseus TEI `tlg0007.tlg125.perseus-eng2`; markup CC BY-SA 4.0) |
| Roman Questions | Isaac Chauncy | `plutarch-perseus-chauncy-roman-questions` | have (Perseus TEI `tlg0007.tlg084a.perseus-eng4`; markup CC BY-SA 4.0) |
| How the Young Man Should Study Poetry | Frank Cole Babbitt | `plutarch-perseus-babbitt-how-the-young-man-should-study-poetry` | have (Perseus TEI `tlg0007.tlg068.perseus-eng3`; markup CC BY-SA 4.0) |
| How a Young Man Ought to Hear Poems | Simon Ford | `plutarch-perseus-ford-how-a-young-man-ought-to-hear-poems` | have (Perseus TEI `tlg0007.tlg068.perseus-eng4`; markup CC BY-SA 4.0) |
| How to Tell a Flatterer from a Friend | Frank Cole Babbitt | `plutarch-perseus-babbitt-how-to-tell-a-flatterer-from-a-friend` | have (Perseus TEI `tlg0007.tlg070.perseus-eng3`; markup CC BY-SA 4.0) |
| How to Know a Flatterer from a Friend | George Tullie | `plutarch-perseus-tullie-how-to-know-a-flatterer-from-a-friend` | have (Perseus TEI `tlg0007.tlg070.perseus-eng4`; markup CC BY-SA 4.0) |
| How a Man May Become Aware of His Progress in Virtue | Frank Cole Babbitt | `plutarch-perseus-babbitt-how-a-man-may-become-aware-of-his-progre` | have (Perseus TEI `tlg0007.tlg071.perseus-eng3`; markup CC BY-SA 4.0) |
| How a Man May Be Sensible of His Progress in Virtue. | Hugh Tod(d) | `plutarch-perseus-todd-how-a-man-may-be-sensible-of-his-progres` | have (Perseus TEI `tlg0007.tlg071.perseus-eng4`; markup CC BY-SA 4.0) |
| The apophthegms or remarkable sayings of kings and great commanders. | Edward Hinton | `plutarch-perseus-hinton-the-apophthegms-or-remarkable-sayings-of` | have (Perseus TEI `tlg0007.tlg081.perseus-eng4`; markup CC BY-SA 4.0) |
| The Dinner of the Seven Wise Men | Frank Cole Babbitt | `plutarch-perseus-babbitt-the-dinner-of-the-seven-wise-men` | have (Perseus TEI `tlg0007.tlg079.perseus-eng3`; markup CC BY-SA 4.0) |
| The Banquet of the Seven Wise Men | Roger Davis | `plutarch-perseus-davis-the-banquet-of-the-seven-wise-men` | have (Perseus TEI `tlg0007.tlg079.perseus-eng4`; markup CC BY-SA 4.0) |
| Lives of the Ten Orators | Charles Barcroft | `plutarch-perseus-barcroft-lives-of-the-ten-orators` | have (Perseus TEI `tlg0007.tlg121.perseus-eng4`; markup CC BY-SA 4.0) |
| Of the Names of Rivers and Mountains, and of Such Things as are to be Found Therein | R. White | `plutarch-perseus-white-of-the-names-of-rivers-and-mountains-and` | have (Perseus TEI `tlg0094.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |
| Concerning music | John Philips | `plutarch-perseus-philips-concerning-music` | have (Perseus TEI `tlg0094.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |
| Of Those Sentiments Concerning Nature with which Philosophers were Delighted | John Dowell | `plutarch-perseus-dowell-of-those-sentiments-concerning-nature-wi` | have (Perseus TEI `tlg0094.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): Philemon Holland's complete Morals (1603) in a cleaner copy; Perrin's and Babbitt's Loebs, on Perseus.

Excluded: PG 3052 (older text of Goodwin), PG 2484 (adaptation), `plutarchslivesn05accigoog` (a worse second scan of North vol. 5), Shakespeare's Plutarch (selections from North).

## Marcus Aurelius

Shelf: `pipeline/marcus-aurelius_shelf.json`. Long (1862) and Chrystal (1902), clean Gutenberg. The Adler shelf's copy is Casaubon by its wording, though labelled Long there (inferred). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Thoughts of Marcus Aurelius Antoninus | George Long (1862) | `marcus-aurelius-long` | have (PG 15877) |
| The Meditations of the Emperor Marcus Aurelius Antoninus: a new rendering | George W. Chrystal (1902) | `marcus-aurelius-chrystal` | have (PG 55317) |
| — | — | `marcus-meditations` | cross-ref → Adler shelf: PG 2680, Casaubon's translation by its wording (inferred); the Adler label 'tr. George Long' looks wrong |
| The Emperor Marcus Antoninus, his Conversation with Himself (1702) | Jeremy Collier | `marcus-aurelius-collier` | have-raw (IA `emperormarcusant00marcrich`) |
| Marcus Aurelius Antoninus to Himself (1898) | Gerald H. Rendall | `marcus-aurelius-rendall` | have-raw (IA `marcusaureliusan00marcrich`) |

Pending (wishlist): Jackson (1906), Haines's Loeb (1916).

Excluded: PG 6920 (serves no text), PG 59784 (index).

## Epictetus

Shelf: `pipeline/epictetus_shelf.json`. Complete in Long (1877), Matheson (1916) and Higginson (1865), raw IA; Long's Selection, Crossley and Rolleston clean. The Adler shelf's 'Discourses, tr. Matheson' is really Higginson's Enchiridion (PG 45109). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| A Selection from the Discourses of Epictetus with the Encheiridion | George Long | `epictetus-long-selection` | have (PG 10661) |
| The Golden Sayings of Epictetus, with the Hymn of Cleanthes | Hastings Crossley | `epictetus-crossley-golden-sayings` | have (PG 871) |
| The Teaching of Epictetus | T. W. Rolleston | `epictetus-rolleston-teaching` | have (PG 39855) |
| The Discourses of Epictetus, with the Encheiridion and Fragments (1877) | George Long | `epictetus-long-discourses-1877` | have-raw (IA `discoursesofepic00epicrich`) |
| Epictetus: the Discourses and Manual, vol. 1 (Oxford, 1916) | P. E. Matheson | `epictetus-matheson-1916-v1` | have-raw (IA `epictetus01epicuoft`) |
| Epictetus: the Discourses and Manual, vol. 2 (Oxford, 1916) | P. E. Matheson | `epictetus-matheson-1916-v2` | have-raw (IA `epictetus02epicuoft`) |
| The Works of Epictetus: Discourses, Enchiridion and Fragments, vol. 1 (1890 printing) | Thomas Wentworth Higginson | `epictetus-higginson-works-v1` | have-raw (IA `worksepictetusc02epicgoog`) |
| The Works of Epictetus, vol. 2 (1890 printing) | Thomas Wentworth Higginson | `epictetus-higginson-works-v2` | have-raw (IA `worksepictetusc00epicgoog`) |
| — | — | `epictetus-discourses` | cross-ref → Adler shelf: PG 45109 is Higginson's ENCHIRIDION only; the Adler label 'The Discourses, tr. P.E. Matheson' is wrong |
| All the Works of Epictetus, which are now Extant (Dublin, 1759) | Elizabeth Carter | `epictetus-carter` | have-raw (IA `allworksofepicte00epic`) |
| Arrian's Discourses of Epictetus | George Long | `epictetus-perseus-long-arrian-s-discourses-of-epictetus` | have (Perseus TEI `tlg0557.tlg001.perseus-eng3`; markup CC BY-SA 4.0) |
| Fragments | George Long | `epictetus-perseus-long-fragments` | have (Perseus TEI `tlg0557.tlg003a.perseus-eng3`; markup CC BY-SA 4.0) |
| Fragments | Thomas Wentworth Higginson | `epictetus-perseus-higginson-fragments` | have (Perseus TEI `tlg0557.tlg003a.perseus-eng4`; markup CC BY-SA 4.0) |
| The Encheiridion, or Manual | George Long | `epictetus-perseus-long-the-encheiridion-or-manual` | have (Perseus TEI `tlg0557.tlg002.perseus-eng3`; markup CC BY-SA 4.0) |

Pending (wishlist): Oldfather's Loeb (1925-28).

## Seneca

Shelf: `pipeline/seneca_shelf.json`. Translator per title, all clean Gutenberg: Stewart, L'Estrange, Clarke, Miller (Tragedies), Harris, Hall (Octavia), Rouse (Apocolocyntosis, US PD per Gutenberg). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| L. Annaeus Seneca on Benefits | Aubrey Stewart | `seneca-stewart-benefits` | have (PG 3794) |
| Minor Dialogues, together with the Dialogue on Clemency | Aubrey Stewart | `seneca-stewart-minor-dialogues` | have (PG 64576) |
| Seneca's Morals of a Happy Life, Benefits, Anger and Clemency | Sir Roger L'Estrange | `seneca-lestrange-morals` | have (PG 56075) |
| Physical Science in the Time of Nero (Quaestiones Naturales) | John Clarke (1910) | `seneca-clarke-natural-questions` | have (PG 76392) |
| The Tragedies of Seneca, translated into English verse | Frank Justus Miller | `seneca-miller-tragedies` | have (PG 57999) |
| Two Tragedies of Seneca: Medea and The Daughters of Troy | Ella Isabel Harris | `seneca-harris-medea-troy` | have (PG 46058) |
| A Translation of Octavia, a Latin Tragedy | Elizabeth Twining Hall (play of doubtful authorship) | `seneca-hall-octavia` | have (PG 54702) |
| Between Heathenism and Christianity: De Providentia (with Plutarch) | Charles W. Super (1899) | `seneca-super-providentia` | have (PG 60831) |
| Apocolocyntosis | W. H. D. Rouse; US PD per Gutenberg | `seneca-rouse-apocolocyntosis` | have (PG 10001) |
| Ad Lucilium Epistulae Morales, vol. 1 (Loeb, 1917) | Richard M. Gummere | `seneca-gummere-epistles-v1` | have-raw (IA `adluciliumepistu01seneuoft`) |
| Ad Lucilium Epistulae Morales, vol. 2 (Loeb, 1920) | Richard M. Gummere | `seneca-gummere-epistles-v2` | have-raw (IA `adluciliumepistu02seneuoft`) |
| Ad Lucilium Epistulae Morales, vol. 3 (Loeb, 1925) | Richard M. Gummere | `seneca-gummere-epistles-v3` | have-raw (IA `adluciliumepistu03seneuoft`) |
| Moral Essays, vol. 1 (Loeb, 1928) | John W. Basore | `seneca-basore-moral-essays-v1` | have-raw (IA `moralessayswithe01seneuoft`) |
| Tragedies, vol. 1 (Loeb, 1917) | Frank Justus Miller | `seneca-miller-loeb-tragedies-v1` | have-raw (IA `tragedieswitheng01seneuoft`) |
| Tragedies, vol. 2 (Loeb, 1917; this printing revised 1929) | Frank Justus Miller | `seneca-miller-loeb-tragedies-v2` | have-raw (IA `tragedieswitheng02seneuoft`) |

Pending (wishlist): Thomas Lodge's Works (1614); Basore's Moral Essays vols. 2-3 (1932-35, not PD).

Excluded: PG 59025 (index), PG 55705 (another Seneca, wrong author).

## Tacitus

Shelf: `pipeline/tacitus_shelf.json`. Church and Brodribb's Annals and Histories (raw IA), the Oxford Germany and Agricola, Fyfe's Histories (US PD per Gutenberg), Gordon's Germany, Murphy's Dialogue. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Germany and the Agricola of Tacitus | the Oxford translation revised (with notes) | `tacitus-oxford-germany-agricola` | have (PG 7524) |
| Tacitus: The Histories, vols. I and II | W. Hamilton Fyfe (1912); US PD per Gutenberg | `tacitus-fyfe-histories` | have (PG 16927) |
| Tacitus on Germany | Thomas Gordon | `tacitus-gordon-germany` | have (PG 2995) |
| A Dialogue Concerning Oratory, or the Causes of Corrupt Eloquence | Arthur Murphy | `tacitus-murphy-dialogue` | have (PG 15017) |
| Annals of Tacitus, translated into English with notes and maps (1906 printing) | A. J. Church and W. J. Brodribb | `tacitus-church-brodribb-annals` | have-raw (IA `annalstacitustr00brodgoog`) |
| The History of Tacitus, translated into English (1894 printing) | A. J. Church and W. J. Brodribb | `tacitus-church-brodribb-histories` | have-raw (IA `historyoftacitus00taci`) |
| — | — | `tacitus-annals` | cross-ref → Adler shelf: PG 7959, which is Thomas GORDON's 'The Reign of Tiberius, out of the First Six Annals' (ed. Galton), not Church and Brodribb's Annals as the Adler label says; the full Church-Brodribb Annals is now on this shelf |
| Dialogus, Agricola, Germania (Loeb, 1914) | W. Peterson (Dialogus), M. Hutton (Agricola, Germania) | `tacitus-hutton-peterson-dialogus-agricola-germania` | have-raw (IA `dialogusagricola0000taci_n3b1`) |
| The Works of Tacitus, with Political Discourses, vol. 1 (1753) | Thomas Gordon | `tacitus-gordon-v1` | have-raw (IA `worksoftacituswi01taci`) |
| The Works of Tacitus, with Political Discourses, vol. 2 (1753) | Thomas Gordon | `tacitus-gordon-v2` | have-raw (IA `worksoftacituswi02taci`) |
| The Works of Tacitus, with Political Discourses, vol. 3 (1753) | Thomas Gordon | `tacitus-gordon-v3` | have-raw (IA `worksoftacituswi03taci`) |
| The Works of Tacitus, with Political Discourses, vol. 4 (1753) | Thomas Gordon | `tacitus-gordon-v4` | have-raw (IA `worksoftacituswi04taci`) |
| The Works of Tacitus, with Political Discourses, vol. 5 (1753) | Thomas Gordon | `tacitus-gordon-v5` | have-raw (IA `worksoftacituswi05taci`) |

Pending (wishlist): Jackson's Loeb Annals (1931-37, not cleared); 

Excluded: PG 59786 (index).

## Livy

Shelf: `pipeline/livy_shelf.json`. Complete in the Bohn translation (Spillan, Edmonds, McDevitte) across four Gutenberg texts; Church and Brodribb Books I-III. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The History of Rome, Books I-VIII | D. Spillan (Bohn) | `livy-bohn-1-8` | have (PG 19725) |
| The History of Rome, Books IX-XXVI | D. Spillan and Cyrus Edmonds (Bohn) | `livy-bohn-9-26` | have (PG 10907) |
| The History of Rome, Books XXVII-XXXVI | Cyrus Edmonds (Bohn) | `livy-bohn-27-36` | have (PG 12582) |
| The History of Rome, Books XXXVII to the end, with the Epitomes and Fragments | W. A. McDevitte (Bohn) | `livy-bohn-37-end` | have (PG 44318) |
| Roman History, Books I-III | A. J. Church and W. J. Brodribb, ed. Duffield Osborne | `livy-church-brodribb-1-3` | have (PG 10828) |
| Livy, vol. 1: Books I-II (Loeb, 1919) | B. O. Foster | `livy-foster-v1` | have-raw (IA `livy0000bofo_o9g8`) |
| Livy, vol. 4: Books VIII-X (Loeb, 1926) | B. O. Foster | `livy-foster-v4` | have-raw (IA `livywithenglisht04livyuoft`) |
| Livy, vol. 5: Books XXI-XXII (Loeb, 1929) | B. O. Foster | `livy-foster-v5` | have-raw (IA `livy05livy`) |
| Livy, vol. 3: Books V-VII (Loeb, 1924) | B. O. Foster | `livy-foster-v3` | have-raw (IA `livywithenglisht0000bofo`) |
| The Romane Historie written by T. Livius of Padua (1659 edition) | Philemon Holland | `livy-holland` | have-raw (IA `romanehistorie00livy`) |
| The History of Rome | Rev. Canon Roberts | `livy-perseus-roberts-the-history-of-rome` | have (Perseus TEI `phi0914.phi001.perseus-eng3`; markup CC BY-SA 4.0) |

Pending (wishlist): Foster's Loeb vol. 2 (1922; only a 1939 revised printing found, refused).

## Julius Caesar

Shelf: `pipeline/caesar_shelf.json`. McDevitte and Bohn (1869), all five commentaries, clean Gutenberg. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| 'De Bello Gallico' and Other Commentaries | W. A. McDevitte and W. S. Bohn | `caesar-mcdevitte-bohn` | have (PG 10657) |
| The Gallic War (Loeb, 1917) | H. J. Edwards | `caesar-edwards-gallic-war` | have-raw (IA `gallicwar00caes`) |
| The Civil Wars (Loeb, 1914) | A. G. Peskett | `caesar-peskett-civil-wars` | have-raw (IA `civilwarswitheng00caesuoft`) |

Pending (wishlist): Arthur Golding's Caesar (1565).

## Suetonius

Shelf: `pipeline/suetonius_shelf.json`. Thomson rev. Forester (Bohn), complete. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Lives of the Twelve Caesars, complete | Alexander Thomson, rev. T. Forester | `suetonius-thomson-forester` | have (PG 6400) |
| Suetonius, vol. 1 (Loeb, 1913) | J. C. Rolfe | `suetonius-rolfe-v1` | have-raw (IA `suetonius01suet`) |
| Suetonius, vol. 2 (Loeb, 1914) | J. C. Rolfe | `suetonius-rolfe-v2` | have-raw (IA `suetonius02suetuoft`) |
| The Deified Julius | John C. Rolfe | `suetonius-perseus-rolfe-the-deified-julius` | have (Perseus TEI `phi1348.abo011.rolfe-eng1`; markup CC BY-SA 4.0) |

Pending (wishlist): Philemon Holland (1606).

Excluded: PG 6386-6399 (the same text split into 14 files).

## Sallust

Shelf: `pipeline/sallust_shelf.json`. Watson (Bohn). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Conspiracy of Catiline and the Jugurthine War | J. S. Watson (Bohn) | `sallust-watson` | have (PG 7990) |
| Sallust (Loeb, 1921) | J. C. Rolfe | `sallust-rolfe` | have-raw (IA `sallustsa00sall`) |


## Pliny the Elder and the Younger

Shelf: `pipeline/pliny_shelf.json`. Bostock and Riley's Natural History, 6 vols.; Melmoth's Letters (rev. Bosanquet); Firth's Letters vol. 1. Clean Gutenberg. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Natural History of Pliny, vol. 1 (of 6) | John Bostock and H. T. Riley (Bohn) | `pliny-elder-bostock-riley-v1` | have (PG 57493) |
| The Natural History of Pliny, vol. 2 (of 6) | John Bostock and H. T. Riley (Bohn) | `pliny-elder-bostock-riley-v2` | have (PG 60230) |
| The Natural History of Pliny, vol. 3 (of 6) | John Bostock and H. T. Riley (Bohn) | `pliny-elder-bostock-riley-v3` | have (PG 59131) |
| The Natural History of Pliny, vol. 4 (of 6) | John Bostock and H. T. Riley (Bohn) | `pliny-elder-bostock-riley-v4` | have (PG 61113) |
| The Natural History of Pliny, vol. 5 (of 6) | John Bostock and H. T. Riley (Bohn) | `pliny-elder-bostock-riley-v5` | have (PG 60688) |
| The Natural History of Pliny, vol. 6 (of 6) | John Bostock and H. T. Riley (Bohn) | `pliny-elder-bostock-riley-v6` | have (PG 62704) |
| Letters of Pliny | William Melmoth, rev. F. C. T. Bosanquet | `pliny-younger-melmoth-letters` | have (PG 2811) |
| The Letters of the Younger Pliny, First Series, vol. 1 | John B. Firth | `pliny-younger-firth-letters-1` | have (PG 3234) |
| Letters, vol. 1 (Loeb, 1915) | William Melmoth, revised by W. M. L. Hutchinson | `pliny-melmoth-hutchinson-letters-v1` | have-raw (IA `letterswithengli01plinuoft`) |
| Letters, vol. 2 (Loeb, 1915) | William Melmoth, revised by W. M. L. Hutchinson | `pliny-melmoth-hutchinson-letters-v2` | have-raw (IA `letterswithengli02plinuoft`) |
| The Historie of the World, commonly called the Naturall Historie of C. Plinius Secundus, tome 1 (1601) | Philemon Holland | `pliny-holland-natural-history-v1` | have-raw (IA `plinyhollandhistorie01`) |
| The Historie of the World, commonly called the Naturall Historie of C. Plinius Secundus, tome 2 (1601) | Philemon Holland | `pliny-holland-natural-history-v2` | have-raw (IA `plinyhollandhistorie02`) |

Pending (wishlist): Firth's remaining volume(s); 

Excluded: PG 58589 (adaptation).

## Lucretius

Shelf: `pipeline/lucretius_shelf.json`. Munro (prose, vol. 3 of his edition) and Bailey (1910), raw IA; Trevelyan's selections, clean. Leonard's verse is on the Adler shelf (mislabelled Munro there). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Translations from Lucretius | R. C. Trevelyan (verse, 1920) | `lucretius-trevelyan-selections` | have (PG 64024) |
| De rerum natura libri sex, ed. with notes and a translation by H. A. J. Munro, vol. 3: the translation (1900 printing) | H. A. J. Munro | `lucretius-munro-translation` | have-raw (IA `lucreticariderer03lucruoft`) |
| Lucretius on the Nature of Things (Oxford, 1910) | Cyril Bailey | `lucretius-bailey-1910` | have-raw (IA `lucretiusonthena00lucruoft`) |
| — | — | `lucretius-nature` | cross-ref → Adler shelf: PG 785 is William Ellery LEONARD's 1916 verse translation, not Munro's as the Adler label says |
| — | — | `dryden-lucretius` | cross-ref → Dryden shelf, lane C (Dryden's passages from Lucretius) |
| T. Lucretius Carus, Of the Nature of Things, vol. 1 (1714) | Thomas Creech | `lucretius-creech-v1` | have-raw (IA `tlucretiuscaruso01lucr`) |
| T. Lucretius Carus, Of the Nature of Things, vol. 2: Books V-VI (1714) | Thomas Creech | `lucretius-creech-v2` | have-raw (IA `tlucretiuscaruso02lucr`) |
| De Rerum Natura | William Ellery Leonard | `lucretius-perseus-leonard-de-rerum-natura` | have (Perseus TEI `phi0550.phi001.perseus-eng1`; markup CC BY-SA 4.0) |

Pending (wishlist): Rouse's Loeb (1924).

Excluded: `in.ernet.dli.2015.96329` (empty text layer).

## Horace

Shelf: `pipeline/horace_shelf.json`. Conington's verse (Odes; Satires, Epistles, Ars Poetica), an unnamed literal prose Works, the Fields' Sabine Farm versions. Clean Gutenberg. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Odes and Carmen Saeculare of Horace | John Conington (verse) | `horace-conington-odes` | have (PG 5432) |
| The Satires, Epistles, and Art of Poetry of Horace | John Conington (verse) | `horace-conington-satires-epistles` | have (PG 5419) |
| The Works of Horace, translated literally into English prose | unnamed ('Handy Literal Translations') | `horace-literal-works` | have (PG 14020) |
| Echoes from the Sabine Farm | Eugene and Roswell Martin Field (free versions) | `horace-field-sabine-farm` | have (PG 13885) |
| — | — | `dryden-horace` | cross-ref → Dryden shelf, lane C |
| Satires, Epistles and Ars Poetica (Loeb, 1926; this printing revised 1929) | H. Rushton Fairclough | `horace-fairclough-satires-epistles` | have-raw (IA `satiresepistlesa00horauoft`) |
| Odes | John Conington | `horace-perseus-conington-odes` | have (Perseus TEI `phi0893.phi001.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): Bennett's Odes and Epodes (Loeb 1914; no readable scan found); Christopher Smart's prose (1756).

## Catullus

Shelf: `pipeline/catullus_shelf.json`. Ellis (1871) and Burton-Smithers (1894), clean Gutenberg. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Poems and Fragments of Catullus translated in the metres of the original | Robinson Ellis (1871) | `catullus-ellis` | have (PG 18867) |
| The Carmina of Caius Valerius Catullus | Sir Richard Burton (verse) and Leonard C. Smithers (prose) | `catullus-burton-smithers` | have (PG 20732) |
| Catullus, Tibullus and Pervigilium Veneris (Loeb, 1913) | F. W. Cornish (Catullus), J. P. Postgate (Tibullus), J. W. Mackail (Pervigilium) | `catullus-tibullus-pervigilium-loeb` | have-raw (IA `catullustibullus00catu`) |
| Carmina | Sir Richard Francis Burton | `catullus-perseus-burton-carmina` | have (Perseus TEI `phi0472.phi001.perseus-eng3`; markup CC BY-SA 4.0) |
| Carmina | Leonard C. Smithers | `catullus-perseus-smithers-carmina` | have (Perseus TEI `phi0472.phi001.perseus-eng4`; markup CC BY-SA 4.0) |


Excluded: PG 23720 (serves a 404).

## Tibullus

Shelf: `pipeline/tibullus_shelf.json`. Theodore C. Williams (1905), clean Gutenberg. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Elegies of Tibullus | Theodore Chickering Williams (verse) | `tibullus-williams` | have (PG 9610) |

Pending (wishlist): Postgate's Loeb (1913).

## Juvenal and Persius

Shelf: `pipeline/juvenal_shelf.json`. Evans's literal prose with Gifford's verse (Bohn), clean Gutenberg. Dryden's on lane C. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Satires of Juvenal, Persius, Sulpicia, and Lucilius | Lewis Evans (prose), with William Gifford's verse translation | `juvenal-persius-evans-gifford` | have (PG 50657) |
| — | — | `dryden-juvenal` | cross-ref → Dryden shelf, lane C |
| — | — | `dryden-persius` | cross-ref → Dryden shelf, lane C |
| Juvenal and Persius (Loeb, 1918) | G. G. Ramsay | `juvenal-persius-ramsay` | have-raw (IA `juvenalpersiuswi00juveuoft`) |


## Plautus and Terence

Shelf: `pipeline/roman-comedy_shelf.json`. Riley's complete Plautus (raw IA, 2 vols.) and Captivi/Mostellaria; Riley's and Colman's Terence; Goodluck's Andrian. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Captivi and the Mostellaria | Henry T. Riley (prose) | `plautus-riley-captivi-mostellaria` | have (PG 7282) |
| Plautus vol. 1: Amphitryo, Asinaria, Aulularia, Bacchides, Captivi | Paul Nixon (Loeb 1916; Latin facing) | `plautus-nixon-v1` | have (PG 16564) |
| The Comedies of Terence, literally translated into English prose | Henry T. Riley (Bohn) | `terence-riley-comedies` | have (PG 22188) |
| The Comedies of Terence | George Colman (verse) | `terence-colman-comedies` | have (PG 22695) |
| Terence's Andrian, a comedy in five acts | W. R. Goodluck | `terence-goodluck-andrian` | have (PG 72921) |
| The Comedies of Plautus, vol. 1 (Bohn; 1913 printing) | Henry T. Riley | `plautus-riley-comedies-v1` | have-raw (IA `comediesofplautu01plauuoft`) |
| The Comedies of Plautus, vol. 2 (Bohn; 1913 printing) | Henry T. Riley | `plautus-riley-comedies-v2` | have-raw (IA `comediesofplautu02plauuoft`) |
| Plautus, vol. 2: Casina, The Casket Comedy, Curculio, Epidicus, Menaechmi (Loeb, 1917) | Paul Nixon | `plautus-nixon-v2` | have-raw (IA `plautusvolume00plaugoog`) |
| Plautus, vol. 3: The Merchant, The Braggart Warrior, Mostellaria, The Persian (Loeb, 1924) | Paul Nixon | `plautus-nixon-v3` | have-raw (IA `plautus03plau`) |
| Terence, vol. 1 (Loeb, 1912) | John Sargeaunt | `terence-sargeaunt-v1` | have-raw (IA `terence000ijohn`) |
| Terence, vol. 2 (Loeb, 1912) | John Sargeaunt | `terence-sargeaunt-v2` | have-raw (IA `terence00iijohn`) |

Pending (wishlist): Thornton's verse Plautus (1767-74).

## Lucan

Shelf: `pipeline/lucan_shelf.json`. Ridley's blank-verse Pharsalia (1896); PG names no translator, identified by collation with Ridley's 1905 printing. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Pharsalia; Dramatic Episodes of the Civil Wars | Sir Edward Ridley (blank verse, 1896); PG names no translator, identified by collation | `lucan-ridley-pharsalia` | have (PG 602) |
| Lucan: The Civil War, Books I-X (Pharsalia) (Loeb, 1928) | J. D. Duff | `lucan-duff` | have-raw (IA `lucancivilwarboo00lucauoft`) |
| Lucan's Pharsalia, vol. 1 | Nicholas Rowe | `lucan-rowe-v1` | have-raw (IA `bub_gb_AnxKHS45tH8C`) |
| Lucan's Pharsalia, vol. 2 (1812; with Vida's Art of Poetry) | Nicholas Rowe | `lucan-rowe-v2` | pending (IA `bub_gb_GEsNZ2BDG1QC`: title page read, vol. II, 1812; the text file answers HTTP 500 intermittently, retrying) |

Pending (wishlist): Marlowe's First Book (Marlowe shelf).

## Apuleius

Shelf: `pipeline/apuleius_shelf.json`. Adlington's Golden Asse (1566) and Butler's Apologia and Florida (1909), clean Gutenberg. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Golden Asse | William Adlington (1566) | `apuleius-adlington-golden-asse` | have (PG 1666) |
| The Apologia and Florida of Apuleius of Madaura | H. E. Butler (1909) | `apuleius-butler-apologia-florida` | have (PG 26294) |
| The Golden Ass, being the Metamorphoses of Lucius Apuleius (Loeb, 1915) | William Adlington (1566), revised by S. Gaselee | `apuleius-adlington-gaselee` | have-raw (IA `goldenassbeingme00apuliala`) |

Pending (wishlist): Butler's Metamorphoses (1910).

## Petronius

Shelf: `pipeline/petronius_shelf.json`. Firebaugh's complete Satyricon (US PD per Gutenberg) and Burnaby's. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Satyricon, complete | W. C. Firebaugh; US PD per Gutenberg | `petronius-firebaugh-satyricon` | have (PG 5225) |
| The Satyricon of Petronius Arbiter | William Burnaby | `petronius-burnaby-satyricon` | have (PG 5611) |
| Petronius (Satyricon); Seneca, Apocolocyntosis (Loeb, 1913) | Michael Heseltine (Petronius), W. H. D. Rouse (Seneca) | `petronius-heseltine-seneca-rouse` | have-raw (IA `petronius00petruoft`) |


Excluded: PG 5218-5224 (Firebaugh split into seven files).

## Lucian

Shelf: `pipeline/lucian_shelf.json`. The Fowlers' Works (1905), 4 vols., complete in Gutenberg; Francklin's Trips to the Moon; Hickes's True History. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Works of Lucian of Samosata, vol. 1 | H. W. and F. G. Fowler | `lucian-fowler-v1` | have (PG 6327) |
| The Works of Lucian of Samosata, vol. 2 | H. W. and F. G. Fowler | `lucian-fowler-v2` | have (PG 6585) |
| The Works of Lucian of Samosata, vol. 3 | H. W. and F. G. Fowler | `lucian-fowler-v3` | have (PG 6829) |
| The Works of Lucian of Samosata, vol. 4 | H. W. and F. G. Fowler | `lucian-fowler-v4` | have (PG 47242) |
| Trips to the Moon | Thomas Francklin | `lucian-francklin-trips-to-the-moon` | have (PG 10430) |
| Lucian's True History | Francis Hickes | `lucian-hickes-true-history` | have (PG 45858) |
| — | — | `dryden-polybius-lucian` | cross-ref → Dryden shelf, lane C (Dryden's Life of Lucian) |
| The Ignorant Book Collector | Austin Morris Harmon | `lucian-perseus-harmon-the-ignorant-book-collector` | have (Perseus TEI `tlg0062.tlg028.perseus-eng2`; markup CC BY-SA 4.0) |
| Alexander the False Prophet | Austin Morris Harmon | `lucian-perseus-harmon-alexander-the-false-prophet` | have (Perseus TEI `tlg0062.tlg038.perseus-eng2`; markup CC BY-SA 4.0) |
| Anacharsis, or Athletics | Austin Morris Harmon | `lucian-perseus-harmon-anacharsis-or-athletics` | have (Perseus TEI `tlg0062.tlg034.perseus-eng2`; markup CC BY-SA 4.0) |
| Dionysus: an Introduction | Austin Morris Harmon | `lucian-perseus-harmon-dionysus-an-introduction` | have (Perseus TEI `tlg0062.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |
| The Double Indictment | Austin Morris Harmon | `lucian-perseus-harmon-the-double-indictment` | have (Perseus TEI `tlg0062.tlg026.perseus-eng2`; markup CC BY-SA 4.0) |
| Slander: on not Being Quick to Put Faith in it | Austin Morris Harmon | `lucian-perseus-harmon-slander-on-not-being-quick-to-put-faith` | have (Perseus TEI `tlg0062.tlg013.perseus-eng2`; markup CC BY-SA 4.0) |
| The Downward Journey, or the Tyrant | Austin Morris Harmon | `lucian-perseus-harmon-the-downward-journey-or-the-tyrant` | have (Perseus TEI `tlg0062.tlg016.perseus-eng2`; markup CC BY-SA 4.0) |
| The Ferry | Emily James Smith | `lucian-perseus-smith-the-ferry` | have (Perseus TEI `tlg0062.tlg016.perseus-eng5`; markup CC BY-SA 4.0) |
| Charon, or the Inspectors | Austin Morris Harmon | `lucian-perseus-harmon-charon-or-the-inspectors` | have (Perseus TEI `tlg0062.tlg023.perseus-eng2`; markup CC BY-SA 4.0) |
| The Hall | Austin Morris Harmon | `lucian-perseus-harmon-the-hall` | have (Perseus TEI `tlg0062.tlg009.perseus-eng2`; markup CC BY-SA 4.0) |
| On Sacrifices | Austin Morris Harmon | `lucian-perseus-harmon-on-sacrifices` | have (Perseus TEI `tlg0062.tlg027.perseus-eng2`; markup CC BY-SA 4.0) |
| The Goddesse of Surrye | Austin Morris Harmon | `lucian-perseus-harmon-the-goddesse-of-surrye` | have (Perseus TEI `tlg0062.tlg041.perseus-eng2`; markup CC BY-SA 4.0) |
| On Funerals | Austin Morris Harmon | `lucian-perseus-harmon-on-funerals` | have (Perseus TEI `tlg0062.tlg036.perseus-eng2`; markup CC BY-SA 4.0) |
| On Salaried Posts in Great Houses | Austin Morris Harmon | `lucian-perseus-harmon-on-salaried-posts-in-great-houses` | have (Perseus TEI `tlg0062.tlg033.perseus-eng2`; markup CC BY-SA 4.0) |
| The Parasite Tychiades | Austin Morris Harmon | `lucian-perseus-harmon-the-parasite-tychiades` | have (Perseus TEI `tlg0062.tlg030.perseus-eng2`; markup CC BY-SA 4.0) |
| The Judgement of the Goddesses | Austin Morris Harmon | `lucian-perseus-harmon-the-judgement-of-the-goddesses` | have (Perseus TEI `tlg0062.tlg032.perseus-eng2`; markup CC BY-SA 4.0) |
| Demonax | Austin Morris Harmon | `lucian-perseus-harmon-demonax` | have (Perseus TEI `tlg0062.tlg008.perseus-eng2`; markup CC BY-SA 4.0) |
| Amber, or the Swan | Austin Morris Harmon | `lucian-perseus-harmon-amber-or-the-swan` | have (Perseus TEI `tlg0062.tlg005.perseus-eng2`; markup CC BY-SA 4.0) |
| The Dream, or the Cock | Austin Morris Harmon | `lucian-perseus-harmon-the-dream-or-the-cock` | have (Perseus TEI `tlg0062.tlg019.perseus-eng2`; markup CC BY-SA 4.0) |
| The Cock | Emily James Smith | `lucian-perseus-smith-the-cock` | have (Perseus TEI `tlg0062.tlg019.perseus-eng5`; markup CC BY-SA 4.0) |
| Heracles: an Introduction | Austin Morris Harmon | `lucian-perseus-harmon-heracles-an-introduction` | have (Perseus TEI `tlg0062.tlg004.perseus-eng2`; markup CC BY-SA 4.0) |
| Hippias, or the Bath | Austin Morris Harmon | `lucian-perseus-harmon-hippias-or-the-bath` | have (Perseus TEI `tlg0062.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |
| Icaromenippus, or the Sky-man | Austin Morris Harmon | `lucian-perseus-harmon-icaromenippus-or-the-sky-man` | have (Perseus TEI `tlg0062.tlg021.perseus-eng2`; markup CC BY-SA 4.0) |
| Essays in Portraiture | Austin Morris Harmon | `lucian-perseus-harmon-essays-in-portraiture` | have (Perseus TEI `tlg0062.tlg039.perseus-eng2`; markup CC BY-SA 4.0) |
| The Consonants at Law Sigma Vs. Tau, in the Court of the Seven Vowels | Austin Morris Harmon | `lucian-perseus-harmon-the-consonants-at-law-sigma-vs-tau-in-th` | have (Perseus TEI `tlg0062.tlg014.perseus-eng2`; markup CC BY-SA 4.0) |
| Zeus Catechized | Austin Morris Harmon | `lucian-perseus-harmon-zeus-catechized` | have (Perseus TEI `tlg0062.tlg017.perseus-eng2`; markup CC BY-SA 4.0) |
| Zeus Rants | Austin Morris Harmon | `lucian-perseus-harmon-zeus-rants` | have (Perseus TEI `tlg0062.tlg018.perseus-eng2`; markup CC BY-SA 4.0) |
| Zeus the Tragedian | Emily James Smith | `lucian-perseus-smith-zeus-the-tragedian` | have (Perseus TEI `tlg0062.tlg018.perseus-eng5`; markup CC BY-SA 4.0) |
| Octogenerians | Austin Morris Harmon | `lucian-perseus-harmon-octogenerians` | have (Perseus TEI `tlg0062.tlg011.perseus-eng2`; markup CC BY-SA 4.0) |
| The Fly | Austin Morris Harmon | `lucian-perseus-harmon-the-fly` | have (Perseus TEI `tlg0062.tlg006.perseus-eng2`; markup CC BY-SA 4.0) |
| Menippus, or the Descent Into Hades | Austin Morris Harmon | `lucian-perseus-harmon-menippus-or-the-descent-into-hades` | have (Perseus TEI `tlg0062.tlg035.perseus-eng2`; markup CC BY-SA 4.0) |
| Nigrinus | Austin Morris Harmon | `lucian-perseus-harmon-nigrinus` | have (Perseus TEI `tlg0062.tlg007.perseus-eng2`; markup CC BY-SA 4.0) |
| My Native Land | Austin Morris Harmon | `lucian-perseus-harmon-my-native-land` | have (Perseus TEI `tlg0062.tlg010.perseus-eng2`; markup CC BY-SA 4.0) |
| Phalaris | Austin Morris Harmon | `lucian-perseus-harmon-phalaris` | have (Perseus TEI `tlg0062.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |
| The Lover of Lies, or the Doubter Tychiades | Austin Morris Harmon | `lucian-perseus-harmon-the-lover-of-lies-or-the-doubter-tychiad` | have (Perseus TEI `tlg0062.tlg031.perseus-eng2`; markup CC BY-SA 4.0) |
| The Dead Come to Life, or the Fisherman | Austin Morris Harmon | `lucian-perseus-harmon-the-dead-come-to-life-or-the-fisherman` | have (Perseus TEI `tlg0062.tlg025.perseus-eng2`; markup CC BY-SA 4.0) |
| Essays in Portraiture Defended | Austin Morris Harmon | `lucian-perseus-harmon-essays-in-portraiture-defended` | have (Perseus TEI `tlg0062.tlg040.perseus-eng2`; markup CC BY-SA 4.0) |
| Prometheus | Austin Morris Harmon | `lucian-perseus-harmon-prometheus` | have (Perseus TEI `tlg0062.tlg020.perseus-eng2`; markup CC BY-SA 4.0) |
| A Professor of Public Speaking | Austin Morris Harmon | `lucian-perseus-harmon-a-professor-of-public-speaking` | have (Perseus TEI `tlg0062.tlg037.perseus-eng2`; markup CC BY-SA 4.0) |
| The Dream or Lucian’s Career | Austin Morris Harmon | `lucian-perseus-harmon-the-dream-or-lucian-s-career` | have (Perseus TEI `tlg0062.tlg029.perseus-eng2`; markup CC BY-SA 4.0) |
| The Dream | Emily James Smith | `lucian-perseus-smith-the-dream` | have (Perseus TEI `tlg0062.tlg029.perseus-eng5`; markup CC BY-SA 4.0) |
| The Carousal, or the Lapiths | Austin Morris Harmon | `lucian-perseus-harmon-the-carousal-or-the-lapiths` | have (Perseus TEI `tlg0062.tlg015.perseus-eng2`; markup CC BY-SA 4.0) |
| Timon, or the Misanthrope | Austin Morris Harmon | `lucian-perseus-harmon-timon-or-the-misanthrope` | have (Perseus TEI `tlg0062.tlg022.perseus-eng2`; markup CC BY-SA 4.0) |
| Toxaris; Or, Friendship | Emily James Smith | `lucian-perseus-smith-toxaris-or-friendship` | have (Perseus TEI `tlg0062.tlg044.perseus-eng5`; markup CC BY-SA 4.0) |
| A True Story | Austin Morris Harmon | `lucian-perseus-harmon-a-true-story` | have (Perseus TEI `tlg0062.tlg012.perseus-eng2`; markup CC BY-SA 4.0) |
| A True History | Emily James Smith | `lucian-perseus-smith-a-true-history` | have (Perseus TEI `tlg0062.tlg012.perseus-eng5`; markup CC BY-SA 4.0) |
| Philosophies for Sale | Austin Morris Harmon | `lucian-perseus-harmon-philosophies-for-sale` | have (Perseus TEI `tlg0062.tlg024.perseus-eng2`; markup CC BY-SA 4.0) |
| The Sale of Lives | Emily James Smith | `lucian-perseus-smith-the-sale-of-lives` | have (Perseus TEI `tlg0062.tlg024.perseus-eng5`; markup CC BY-SA 4.0) |
| Loukios, or the Ass | Emily James Smith | `lucian-perseus-smith-loukios-or-the-ass` | have (Perseus TEI `tlg0061.tlg001.perseus-eng1`; markup CC BY-SA 4.0) |
| The Cynic | Henry Watson Fowler and Francis George Fowler | `lucian-perseus-fowler-the-cynic` | have (Perseus TEI `tlg0061.tlg006.perseus-eng1`; markup CC BY-SA 4.0) |
| Demosthenes: an Encomium | Henry Watson Fowler and Francis George Fowler | `lucian-perseus-fowler-demosthenes-an-encomium` | have (Perseus TEI `tlg0061.tlg003.perseus-eng1`; markup CC BY-SA 4.0) |
| The Halcyon | Emily James Smith | `lucian-perseus-smith-the-halcyon` | have (Perseus TEI `tlg0061.tlg004.perseus-eng1`; markup CC BY-SA 4.0) |

Pending (wishlist): Harmon's Loeb (1913-); Francklin's complete Lucian (1780).

## Cicero

Shelf: `pipeline/cicero_shelf.json`. Yonge's Orations complete (vols. 1-3 raw IA, vol. 4 clean); Yonge, Shuckburgh, Peabody, Featherstonhaugh and Jones for the philosophy and rhetoric; Shuckburgh's whole correspondence (vol. 1 clean, 2-4 raw). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Orations of Marcus Tullius Cicero, vol. 4 | C. D. Yonge (Bohn) | `cicero-yonge-orations-v4` | have (PG 11080) |
| The Academic Questions, Treatise De Finibus, and Tusculan Disputations | C. D. Yonge (Bohn) | `cicero-yonge-academics-finibus-tusculans` | have (PG 29247) |
| Tusculan Disputations; also Treatises on the Nature of the Gods and on the Commonwealth | C. D. Yonge | `cicero-yonge-tusculans-nature-gods` | have (PG 14988) |
| Treatises on Friendship and Old Age | Evelyn S. Shuckburgh | `cicero-shuckburgh-friendship-old-age` | have (PG 2808) |
| De Amicitia, Scipio's Dream | Andrew P. Peabody | `cicero-peabody-amicitia` | have (PG 7491) |
| The Republic of Cicero | George William Featherstonhaugh | `cicero-featherstonhaugh-republic` | have (PG 54161) |
| Cicero's Brutus, or History of Famous Orators; also his Orator | E. Jones | `cicero-jones-brutus-orator` | have (PG 9776) |
| The Letters of Cicero: the whole extant correspondence, vol. 1 | Evelyn S. Shuckburgh | `cicero-shuckburgh-letters-v1` | have (PG 21200) |
| Letters of Marcus Tullius Cicero (selection) | Evelyn S. Shuckburgh | `cicero-shuckburgh-letters-selection` | have (PG 2812) |
| De Officiis | Walter Miller (Loeb; Latin facing) | `cicero-miller-de-officiis` | have (PG 47001) |
| The Orations of Marcus Tullius Cicero, vol. 1 (Bohn) | C. D. Yonge | `cicero-yonge-orations-v1` | have-raw (IA `orationsofmarcus01ciceuoft`) |
| The Orations of Marcus Tullius Cicero, vol. 2 (Bohn) | C. D. Yonge | `cicero-yonge-orations-v2` | have-raw (IA `orationsofmarcus02ciceuoft`) |
| The Orations of Marcus Tullius Cicero, vol. 3 (Bohn) | C. D. Yonge | `cicero-yonge-orations-v3` | have-raw (IA `orationsofmarcus03cice`) |
| The Letters of Cicero: the whole extant correspondence, vol. 2 (1899) | Evelyn S. Shuckburgh | `cicero-shuckburgh-letters-v2` | have-raw (IA `lettersofcicerow02cice`) |
| The Letters of Cicero: the whole extant correspondence, vol. 3 (1899) | Evelyn S. Shuckburgh | `cicero-shuckburgh-letters-v3` | have-raw (IA `lettersofcicero03ciceuoft`) |
| The Letters of Cicero: the whole extant correspondence, vol. 4 (1899) | Evelyn S. Shuckburgh | `cicero-shuckburgh-letters-v4` | have-raw (IA `lettersofcicerow04ciceuoft`) |
| Cicero: Letters to Atticus, vols. 1-3 (Loeb) | E. O. Winstedt (Latin facing kept) | `cicero-winstedt-atticus-v1..v3` | have (PG 58418, 50692, 51403) |
| The Letters to his Friends, vol. 1 (Loeb, 1927) | W. Glynn Williams | `cicero-williams-friends-v1` | have-raw (IA `letterstohisfrie01ciceuoft`) |
| The Letters to his Friends, vol. 2 (Loeb, 1928) | W. Glynn Williams | `cicero-williams-friends-v2` | have-raw (IA `letterstohisfrie02ciceuoft`) |
| The Letters to his Friends, vol. 3 (Loeb, 1929) | W. Glynn Williams | `cicero-williams-friends-v3` | have-raw (IA `letterstohisfrie03ciceuoft`) |
| De Finibus Bonorum et Malorum (Loeb, 1914) | H. Rackham | `cicero-rackham-de-finibus` | have-raw (IA `definibusbonoru02cicegoog`) |
| De Senectute, De Amicitia, De Divinatione (Loeb, 1923) | W. A. Falconer | `cicero-falconer-senectute-amicitia-divinatione` | have-raw (IA `cicerodesenectut0000will_n8p4`) |
| Philippics (Loeb, 1926) | Walter C. A. Ker | `cicero-ker-philippics` | have-raw (IA `philippics00ciceuoft`) |
| The Verrine Orations, vol. 1 (Loeb, 1928) | L. H. G. Greenwood | `cicero-greenwood-verrines-v1` | have-raw (IA `ciceroverrineora0001unse`) |
| De Re Publica, De Legibus (Loeb, 1928) | Clinton Walker Keyes | `cicero-keyes-de-re-publica-de-legibus` | have-raw (IA `derepublicadeleg0000cice_k7o1`) |

Pending (wishlist): De Officiis (Cockman, Edmonds); Watson's Bohn De Oratore; King's Tusculans (Loeb 1927).

Excluded: Winstedt's Atticus (PG 58418, 50692, 51403): Latin facing, pending as a bilingual witness.

## Demosthenes

Shelf: `pipeline/demosthenes_shelf.json`. Kennedy (Bohn) and Pickard-Cambridge (1912).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Olynthiacs and the Philippics of Demosthenes | Charles Rann Kennedy | `demosthenes-kennedy-olynthiacs-philippics` | have (PG 6878) |
| The Public Orations of Demosthenes, vol. 1 | A. W. Pickard-Cambridge (1912) | `demosthenes-pickard-cambridge-v1` | have (PG 9060) |
| The Public Orations of Demosthenes, vol. 2 | A. W. Pickard-Cambridge (1912) | `demosthenes-pickard-cambridge-v2` | have (PG 9061) |
| The Orations of Demosthenes, vol. 1 (Bohn; 1855 printing) | Charles Rann Kennedy | `demosthenes-kennedy-v1` | have-raw (IA `orationsdemosth03kenngoog`) |
| The Orations of Demosthenes, vol. 2 (Bohn; 1880 printing) | Charles Rann Kennedy | `demosthenes-kennedy-v2` | have-raw (IA `orationsofdemost002demo`) |
| The Orations of Demosthenes against Leptines, Midias, Androtion and Aristocrates, vol. 3 (Bohn; 1856) | Charles Rann Kennedy | `demosthenes-kennedy-v3` | have-raw (IA `orationsdemosth01kenngoog`) |
| The Orations of Demosthenes against Timocrates, Aristogiton, Aphobus and others, vol. 4 (Bohn; 1877) | Charles Rann Kennedy | `demosthenes-kennedy-v4` | have-raw (IA `orationsdemosth02kenngoog`) |
| The Orations of Demosthenes against Macartatus, Leochares, Stephanus and others; the Funeral Oration, Exordia and Epistles, vol. 5 (Bohn; 1878) | Charles Rann Kennedy | `demosthenes-kennedy-v5` | have-raw (IA `orationsofdemos05demo`) |
| Against Leptines | James Herbert Vince | `demosthenes-perseus-vince-against-leptines` | have (Perseus TEI `tlg0014.tlg020.perseus-eng2`; markup CC BY-SA 4.0) |
| Answer to Philip’s Letter | James Herbert Vince | `demosthenes-perseus-vince-answer-to-philip-s-letter` | have (Perseus TEI `tlg0014.tlg011.perseus-eng2`; markup CC BY-SA 4.0) |
| First Olynthiac | James Herbert Vince | `demosthenes-perseus-vince-first-olynthiac` | have (Perseus TEI `tlg0014.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |
| For the Liberty of the Rhodians | James Herbert Vince | `demosthenes-perseus-vince-for-the-liberty-of-the-rhodians` | have (Perseus TEI `tlg0014.tlg015.perseus-eng2`; markup CC BY-SA 4.0) |
| For the People of Megalopolis | James Herbert Vince | `demosthenes-perseus-vince-for-the-people-of-megalopolis` | have (Perseus TEI `tlg0014.tlg016.perseus-eng2`; markup CC BY-SA 4.0) |
| Second Olynthiac | James Herbert Vince | `demosthenes-perseus-vince-second-olynthiac` | have (Perseus TEI `tlg0014.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |
| On Halonnesus | James Herbert Vince | `demosthenes-perseus-vince-on-halonnesus` | have (Perseus TEI `tlg0014.tlg007.perseus-eng2`; markup CC BY-SA 4.0) |
| On Organization | James Herbert Vince | `demosthenes-perseus-vince-on-organization` | have (Perseus TEI `tlg0014.tlg013.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Chersonese | James Herbert Vince | `demosthenes-perseus-vince-on-the-chersonese` | have (Perseus TEI `tlg0014.tlg008.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Navy-Boards | James Herbert Vince | `demosthenes-perseus-vince-on-the-navy-boards` | have (Perseus TEI `tlg0014.tlg014.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Peace | James Herbert Vince | `demosthenes-perseus-vince-on-the-peace` | have (Perseus TEI `tlg0014.tlg005.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Treaty with Alexander | James Herbert Vince | `demosthenes-perseus-vince-on-the-treaty-with-alexander` | have (Perseus TEI `tlg0014.tlg017.perseus-eng2`; markup CC BY-SA 4.0) |
| First Philippic | James Herbert Vince | `demosthenes-perseus-vince-first-philippic` | have (Perseus TEI `tlg0014.tlg004.perseus-eng2`; markup CC BY-SA 4.0) |
| Third Philippic | James Herbert Vince | `demosthenes-perseus-vince-third-philippic` | have (Perseus TEI `tlg0014.tlg009.perseus-eng2`; markup CC BY-SA 4.0) |
| Fourth Philippic | James Herbert Vince | `demosthenes-perseus-vince-fourth-philippic` | have (Perseus TEI `tlg0014.tlg010.perseus-eng2`; markup CC BY-SA 4.0) |
| Philip’s Letter | James Herbert Vince | `demosthenes-perseus-vince-philip-s-letter` | have (Perseus TEI `tlg0014.tlg012.perseus-eng2`; markup CC BY-SA 4.0) |
| Second Philippic | James Herbert Vince | `demosthenes-perseus-vince-second-philippic` | have (Perseus TEI `tlg0014.tlg006.perseus-eng2`; markup CC BY-SA 4.0) |
| Third Olynthiac | James Herbert Vince | `demosthenes-perseus-vince-third-olynthiac` | have (Perseus TEI `tlg0014.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Crown | Charles Anthony Vince and James Herbert Vince | `demosthenes-perseus-vince-on-the-crown` | have (Perseus TEI `tlg0014.tlg018.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Embassy | Charles Anthony Vince and James Herbert Vince | `demosthenes-perseus-vince-on-the-embassy` | have (Perseus TEI `tlg0014.tlg019.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): the rest of the early Loeb vols. (Vince, 1926-; Greek facing: OCR not taken). The 1930 Vince volume is held above as Perseus TEI.

## Lysias

Shelf: `pipeline/lysias_shelf.json`. Gutenberg's 'Handy Literal Translations' edition; the translator is not named in the file.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Orations of Lysias (selection) | unnamed ('Handy Literal Translations') | `lysias-literal-orations` | have (PG 6969) |
| Accusation of Calumny | W.R.M. Lamb | `lysias-perseus-lamb-accusation-of-calumny` | have (Perseus TEI `tlg0540.tlg008.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Agoratus | W.R.M. Lamb | `lysias-perseus-lamb-against-agoratus` | have (Perseus TEI `tlg0540.tlg013.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Alcibiades 1 | W.R.M. Lamb | `lysias-perseus-lamb-against-alcibiades-1` | have (Perseus TEI `tlg0540.tlg014.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Alcibiades 2 | W.R.M. Lamb | `lysias-perseus-lamb-against-alcibiades-2` | have (Perseus TEI `tlg0540.tlg015.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Andocides | W.R.M. Lamb | `lysias-perseus-lamb-against-andocides` | have (Perseus TEI `tlg0540.tlg006.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Diogeiton | W.R.M. Lamb | `lysias-perseus-lamb-against-diogeiton` | have (Perseus TEI `tlg0540.tlg032.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Epicrates and his Fellow-envoys | W.R.M. Lamb | `lysias-perseus-lamb-against-epicrates-and-his-fellow-envoys` | have (Perseus TEI `tlg0540.tlg027.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Eratosthenes | W.R.M. Lamb | `lysias-perseus-lamb-against-eratosthenes` | have (Perseus TEI `tlg0540.tlg012.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Ergocles | W.R.M. Lamb | `lysias-perseus-lamb-against-ergocles` | have (Perseus TEI `tlg0540.tlg028.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Nicomachus | W.R.M. Lamb | `lysias-perseus-lamb-against-nicomachus` | have (Perseus TEI `tlg0540.tlg030.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Pancleon | W.R.M. Lamb | `lysias-perseus-lamb-against-pancleon` | have (Perseus TEI `tlg0540.tlg023.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Philocrates | W.R.M. Lamb | `lysias-perseus-lamb-against-philocrates` | have (Perseus TEI `tlg0540.tlg029.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Philon | W.R.M. Lamb | `lysias-perseus-lamb-against-philon` | have (Perseus TEI `tlg0540.tlg031.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Simon | W.R.M. Lamb | `lysias-perseus-lamb-against-simon` | have (Perseus TEI `tlg0540.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |
| Against The Corn-Dealers | W.R.M. Lamb | `lysias-perseus-lamb-against-the-corn-dealers` | have (Perseus TEI `tlg0540.tlg022.perseus-eng2`; markup CC BY-SA 4.0) |
| Against The Subversion of the Ancestral Constitution | W.R.M. Lamb | `lysias-perseus-lamb-against-the-subversion-of-the-ancestral` | have (Perseus TEI `tlg0540.tlg034.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Theomnestus 1 | W.R.M. Lamb | `lysias-perseus-lamb-against-theomnestus-1` | have (Perseus TEI `tlg0540.tlg010.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Theomnestus 2 | W.R.M. Lamb | `lysias-perseus-lamb-against-theomnestus-2` | have (Perseus TEI `tlg0540.tlg011.perseus-eng2`; markup CC BY-SA 4.0) |
| Defense Against A Charge Of Taking Bribes | W.R.M. Lamb | `lysias-perseus-lamb-defense-against-a-charge-of-taking-bribe` | have (Perseus TEI `tlg0540.tlg021.perseus-eng2`; markup CC BY-SA 4.0) |
| Defense Against a Charge of Subverting the Democracy | W.R.M. Lamb | `lysias-perseus-lamb-defense-against-a-charge-of-subverting-t` | have (Perseus TEI `tlg0540.tlg025.perseus-eng2`; markup CC BY-SA 4.0) |
| For Callias | W.R.M. Lamb | `lysias-perseus-lamb-for-callias` | have (Perseus TEI `tlg0540.tlg005.perseus-eng2`; markup CC BY-SA 4.0) |
| For Polystratus | W.R.M. Lamb | `lysias-perseus-lamb-for-polystratus` | have (Perseus TEI `tlg0540.tlg020.perseus-eng2`; markup CC BY-SA 4.0) |
| For The Soldier | W.R.M. Lamb | `lysias-perseus-lamb-for-the-soldier` | have (Perseus TEI `tlg0540.tlg009.perseus-eng2`; markup CC BY-SA 4.0) |
| Funeral Oration | W.R.M. Lamb | `lysias-perseus-lamb-funeral-oration` | have (Perseus TEI `tlg0540.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |
| In Defense of Mantitheus | W.R.M. Lamb | `lysias-perseus-lamb-in-defense-of-mantitheus` | have (Perseus TEI `tlg0540.tlg016.perseus-eng2`; markup CC BY-SA 4.0) |
| Olympic Oration | W.R.M. Lamb | `lysias-perseus-lamb-olympic-oration` | have (Perseus TEI `tlg0540.tlg033.perseus-eng2`; markup CC BY-SA 4.0) |
| On A Wound By Premeditation | W.R.M. Lamb | `lysias-perseus-lamb-on-a-wound-by-premeditation` | have (Perseus TEI `tlg0540.tlg004.perseus-eng2`; markup CC BY-SA 4.0) |
| On The Property Of Eraton | W.R.M. Lamb | `lysias-perseus-lamb-on-the-property-of-eraton` | have (Perseus TEI `tlg0540.tlg017.perseus-eng2`; markup CC BY-SA 4.0) |
| On The Refusal Of A Pension | W.R.M. Lamb | `lysias-perseus-lamb-on-the-refusal-of-a-pension` | have (Perseus TEI `tlg0540.tlg024.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Confiscation of the Property Of The Brother Of Nicias | W.R.M. Lamb | `lysias-perseus-lamb-on-the-confiscation-of-the-property-of-t` | have (Perseus TEI `tlg0540.tlg018.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Murder of Eratosthenes | W.R.M. Lamb | `lysias-perseus-lamb-on-the-murder-of-eratosthenes` | have (Perseus TEI `tlg0540.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Olive Stump | W.R.M. Lamb | `lysias-perseus-lamb-on-the-olive-stump` | have (Perseus TEI `tlg0540.tlg007.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Property of Aristophanes | W.R.M. Lamb | `lysias-perseus-lamb-on-the-property-of-aristophanes` | have (Perseus TEI `tlg0540.tlg019.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Scrutiny of Evandros | W.R.M. Lamb | `lysias-perseus-lamb-on-the-scrutiny-of-evandros` | have (Perseus TEI `tlg0540.tlg026.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): Lamb's Loeb Lysias (1930) if a scan is found

## Isocrates

Shelf: `pipeline/isocrates_shelf.json`. J. H. Freese, The Orations of Isocrates vol. 1 (Bohn, 1894), raw IA OCR.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Orations of Isocrates, vol. 1 (Bohn, 1894) | J. H. Freese | `isocrates-freese-v1` | have-raw (IA `orationsofisocra0000isoc`) |

Pending (wishlist): Freese never published vol. 2; Norlin/Van Hook Loeb (1928-45) only vols. 1-2 PD by date

## Pindar

Shelf: `pipeline/pindar_shelf.json`. Myers (Gutenberg) and the Turner/Moore Bohn (raw IA OCR, clean-word 0.87).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Extant Odes of Pindar | Ernest Myers | `pindar-myers` | have (PG 10717) |
| The Odes of Pindar, literally translated into English prose (Bohn; 1872 printing) | Dawson W. Turner (prose) and Abraham Moore (verse) | `pindar-turner-moore` | have-raw (IA `odespindarliter00moorgoog`) |
| — | — | `cary-pindar` | cross-ref → lane C, pipeline/cary_shelf.json (Cary, 1833) |

Pending (wishlist): Sandys Loeb (1915; Greek facing)

## Theocritus, Bion, Moschus

Shelf: `pipeline/theocritus_shelf.json`. Calverley's verse (Gutenberg) and the Banks/Chapman Bohn (raw IA OCR, clean-word 0.86).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Theocritus, translated into English Verse | Charles Stuart Calverley | `theocritus-calverley` | have (PG 11533) |
| The Idylls of Theocritus, Bion, and Moschus, and the War-Songs of Tyrtaeus (Bohn, 1853) | J. Banks (prose), J. M. Chapman (verse); Tyrtaeus R. Polwhele | `theocritus-bion-moschus-banks` | have-raw (IA `idyllstheocritu00biongoog`) |
| — | — | `lang theocritus-bion-moschus (PG 4775)` | cross-ref → lane D, pipeline/lang_shelf.json |

Pending (wishlist): Edmonds Loeb (1912; Greek facing)

## Apollonius Rhodius

Shelf: `pipeline/apollonius_shelf.json`. Seaton, Way (Gutenberg) and Coleridge 1889 (raw IA OCR, clean-word 0.92).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Argonautica | R. C. Seaton | `apollonius-seaton` | have (PG 13977) |
| The Tale of the Argonauts | Arthur S. Way | `apollonius-way` | have (PG 64235) |
| The Argonautica of Apollonius Rhodius (Bell, 1889) | Edward P. Coleridge | `apollonius-coleridge` | have-raw (IA `B-001-014-458`) |

Excluded: PG 830 (same Seaton text as PG 13977)

## Quintus Smyrnaeus

Shelf: `pipeline/quintus-smyrnaeus_shelf.json`. Way's Fall of Troy (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Fall of Troy | Arthur S. Way | `quintus-smyrnaeus-way` | have (PG 658) |

## Greek lyric and the Anthology

Shelf: `pipeline/greek-lyric_shelf.json`. Mackail, Wharton's Sappho, Moore's Anacreon (Gutenberg) and Poste's Bacchylides (raw IA OCR, clean-word 0.91).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Select Epigrams from the Greek Anthology | J. W. Mackail | `greek-anthology-mackail` | have (PG 2378) |
| Sappho: Memoir, Text, Selected Renderings, and a Literal Translation | ed. and Henry Thornton Wharton; renderings by various hands | `sappho-wharton` | have (PG 57390) |
| The Odes of Anacreon | Thomas Moore | `anacreon-moore` | have (PG 38230) |
| Bacchylides: A Prose Translation (Macmillan, 1898) | Edward Poste | `bacchylides-poste` | have-raw (IA `cu31924026462287`) |

Pending (wishlist): Paton's Anthology, Edmonds's Lyra Graeca, Mair's Callimachus/Aratus/Oppian (all Loebs, Greek facing); Musaeus

Excluded: modern free Sappho recreations (Carman, O'Hara, Stacpoole)

## Diogenes Laertius

Shelf: `pipeline/diogenes-laertius_shelf.json`. Yonge (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Lives and Opinions of Eminent Philosophers | Charles Duke Yonge | `diogenes-laertius-yonge` | have (PG 57342) |

Pending (wishlist): Hicks Loeb (1925; Greek facing)

## Plotinus

Shelf: `pipeline/plotinus_shelf.json`. MacKenna first edition, all 5 vols. 1917-1930 (raw IA OCR, clean-word 0.91-0.94); Guthrie 1918 (Gutenberg); Taylor (Gutenberg essay; Select Works, IA 0.93).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Plotinos: Complete Works, vol. 1 | Kenneth Sylvan Guthrie | `plotinus-guthrie-v1` | have (PG 42930) |
| Plotinos: Complete Works, vol. 2 | Kenneth Sylvan Guthrie | `plotinus-guthrie-v2` | have (PG 42931) |
| Plotinos: Complete Works, vol. 3 | Kenneth Sylvan Guthrie | `plotinus-guthrie-v3` | have (PG 42932) |
| Plotinos: Complete Works, vol. 4 | Kenneth Sylvan Guthrie | `plotinus-guthrie-v4` | have (PG 42933) |
| An Essay on the Beautiful, from the Greek of Plotinus | Thomas Taylor | `plotinus-taylor-beautiful` | have (PG 29510) |
| Plotinus: The Ethical Treatises (First Ennead), vol. 1 (1917) | Stephen MacKenna | `plotinus-mackenna-v1` | have-raw (IA `plotinusethicalt01plotuoft`) |
| Plotinus: Psychic and Physical Treatises (Second and Third Enneads), vol. 2 (1921) | Stephen MacKenna | `plotinus-mackenna-v2` | have-raw (IA `plotinuspsychicp00plotuoft`) |
| Plotinus: On the Nature of the Soul (Fourth Ennead), vol. 3 (1924) | Stephen MacKenna | `plotinus-mackenna-v3` | have-raw (IA `plotinustranslat03burkuoft`) |
| Plotinus: The Divine Mind (Fifth Ennead), vol. 4 (1926) | Stephen MacKenna | `plotinus-mackenna-v4` | have-raw (IA `plotinustranslat04plotuoft`) |
| Plotinus: On the One and Good (Sixth Ennead), vol. 5 (1930) | Stephen MacKenna and B. S. Page | `plotinus-mackenna-v5` | have-raw (IA `plotinusononegoo0005step`) |
| Select Works of Plotinus (Bohn, 1895) | Thomas Taylor; ed. G. R. S. Mead | `plotinus-taylor-select` | have-raw (IA `selectworksofplo00plotuoft`) |

Excluded: a 550-page MacKenna scan of Enneads IV-VI of unknown date; the 1956 revised edition

## Porphyry

Shelf: `pipeline/porphyry_shelf.json`. Taylor's Select Works and Lardner's pagan arguments (Gutenberg); Zimmern's Marcella (IA, 0.94).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Select Works of Porphyry | Thomas Taylor | `porphyry-taylor-select` | have (PG 77014) |
| Arguments of Celsus, Porphyry, and the Emperor Julian, against the Christians | Nathaniel Lardner | `celsus-porphyry-julian-lardner` | have (PG 37696) |
| Porphyry the Philosopher to his Wife Marcella (1896) | Alice Zimmern | `porphyry-marcella-zimmern` | have-raw (IA `porphyryphiloso00garngoog`) |

## Iamblichus

Shelf: `pipeline/iamblichus_shelf.json`. Taylor's Life of Pythagoras and On the Mysteries (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Iamblichus' Life of Pythagoras, or Pythagoric Life | Thomas Taylor | `iamblichus-taylor-pythagoras` | have (PG 63300) |
| Iamblichus on the Mysteries of the Egyptians, Chaldeans, and Assyrians | Thomas Taylor | `iamblichus-taylor-mysteries` | have (PG 72815) |

Pending (wishlist): Wilder's Theurgia (1911; IA text layer empty)

## Proclus

Shelf: `pipeline/proclus_shelf.json`. Taylor's Euclid commentaries and Theology of Plato (Gutenberg, 4 vols.).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Philosophical and Mathematical Commentaries of Proclus on the First Book of Euclid's Elements, vol. 1 | Thomas Taylor | `proclus-taylor-euclid-v1` | have (PG 74253) |
| The Philosophical and Mathematical Commentaries of Proclus on the First Book of Euclid's Elements, vol. 2 | Thomas Taylor | `proclus-taylor-euclid-v2` | have (PG 79455) |
| The Six Books of Proclus on the Theology of Plato, vol. 1 | Thomas Taylor | `proclus-taylor-theology-v1` | have (PG 77393) |
| The Six Books of Proclus on the Theology of Plato, vol. 2 | Thomas Taylor | `proclus-taylor-theology-v2` | have (PG 78800) |

## Ocellus and the minor Pythagoreans

Shelf: `pipeline/pythagoreans_shelf.json`. Taylor (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Ocellus Lucanus on the Nature of the Universe | Thomas Taylor | `ocellus-taylor` | have (PG 75391) |

## Sextus Empiricus

Shelf: `pipeline/sextus-empiricus_shelf.json`. Patrick 1899 (study with a translation of Pyrrhonic Sketches I).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Sextus Empiricus and Greek Scepticism | Mary Mills Patrick (study, with of Pyrrhonic Sketches I) | `sextus-empiricus-patrick` | have (PG 17556) |

Pending (wishlist): no complete PD English Sextus exists

## Julian

Shelf: `pipeline/julian_shelf.json`. Wright's Loeb vols. 1-2 (Gutenberg; facing Greek kept).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Works of the Emperor Julian, vol. 1 | Wilmer Cave Wright | `julian-wright-v1` | have (PG 48664) |
| The Works of the Emperor Julian, vol. 2 | Wilmer Cave Wright | `julian-wright-v2` | have (PG 48768) |

Pending (wishlist): Wright vol. 3 (1923)

## Boethius

Shelf: `pipeline/boethius_shelf.json`. H. R. James 1897 (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Consolation of Philosophy | H. R. James | `boethius-james` | have (PG 14328) |
| The Theological Tractates and The Consolation of Philosophy | Stewart and Rand (Loeb 1918; 'I.T.' 1609 revised) | `boethius-rand-stewart` | have (PG 13316) |

Excluded: Chaucer's Middle English Boece

## Pausanias

Shelf: `pipeline/pausanias_shelf.json`. Shilleto (Gutenberg); Taylor 1824 vols. 1-2 (IA, 0.93; attribution is the catalogue's); Verrall's Attica 1890 (IA, 0.88).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Pausanias' Description of Greece, vol. 1 | A. R. Shilleto | `pausanias-shilleto-v1` | have (PG 68946) |
| Pausanias' Description of Greece, vol. 2 | A. R. Shilleto | `pausanias-shilleto-v2` | have (PG 68680) |
| The Description of Greece by Pausanias, vol. 1 (2nd ed., 1824) | Thomas Taylor (attributed by catalogue) | `pausanias-taylor-v1` | have-raw (IA `descriptiongree07pausgoog`) |
| The Description of Greece by Pausanias, vol. 2 (2nd ed., 1824) | Thomas Taylor (attributed by catalogue) | `pausanias-taylor-v2` | have-raw (IA `descriptiongree06pausgoog`) |
| Mythology and Monuments of Ancient Athens: being a translation of a portion of the Attica of Pausanias (1890) | Margaret de G. Verrall; commentary Jane E. Harrison | `pausanias-attica-verrall` | have-raw (IA `mythologymonume00pausgoog`) |
| The Description of Greece by Pausanias, vol. 3 (2nd ed., 1824) | Thomas Taylor (attributed by catalogue) | `pausanias-taylor-v3` | have-raw (IA `descriptiongree00pausgoog`) |

Pending (wishlist): Frazer 1898 vol. 1 (no usable scan); Jones Loeb (Greek facing)

## Strabo

Shelf: `pipeline/strabo_shelf.json`. Hamilton (Books I-VI) and Falconer (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Geography of Strabo, vol. 1 | H. C. Hamilton and W. Falconer | `strabo-hamilton-falconer-v1` | have (PG 44884) |
| The Geography of Strabo, vol. 2 | H. C. Hamilton and W. Falconer | `strabo-hamilton-falconer-v2` | have (PG 44885) |
| The Geography of Strabo, vol. 3 | H. C. Hamilton and W. Falconer | `strabo-hamilton-falconer-v3` | have (PG 44886) |
| Geography (Books 6-14) | Horace Leonard Jones | `strabo-perseus-jones-geography-books-6-14` | have (Perseus TEI `tlg0099.tlg001.perseus-eng3`; markup CC BY-SA 4.0) |

## Appian

Shelf: `pipeline/appian_shelf.json`. Horace White 1899 (IA, 0.90-0.92).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Roman History of Appian of Alexandria, vol. 1: The Foreign Wars (1899) | Horace White | `appian-white-v1` | have-raw (IA `romanhistoryapp03whitgoog`) |
| The Roman History of Appian of Alexandria, vol. 2: The Civil Wars (1899) | Horace White | `appian-white-v2` | have-raw (IA `romanhistoryapp02whitgoog`) |

## Diodorus Siculus

Shelf: `pipeline/diodorus_shelf.json`. Booth (1814 edition, IA, 0.92-0.93).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Historical Library of Diodorus the Sicilian, vol. 1 (1814) | George Booth | `diodorus-booth-v1` | have-raw (IA `historicallibra01bootgoog`) |
| The Historical Library of Diodorus the Sicilian, vol. 2 (1814) | George Booth | `diodorus-booth-v2` | have-raw (IA `historicallibra00bootgoog`) |

Pending (wishlist): Oldfather Loeb is not PD

## Cassius Dio

Shelf: `pipeline/dio-cassius_shelf.json`. Foster's Dio's Rome 1905-06 (Gutenberg, 6 vols.).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Dio's Rome, vol. 1 | Herbert Baldwin Foster | `dio-foster-v1` | have (PG 18047) |
| Dio's Rome, vol. 2 | Herbert Baldwin Foster | `dio-foster-v2` | have (PG 11607) |
| Dio's Rome, vol. 3 | Herbert Baldwin Foster | `dio-foster-v3` | have (PG 10162) |
| Dio's Rome, vol. 4 | Herbert Baldwin Foster | `dio-foster-v4` | have (PG 10883) |
| Dio's Rome, vol. 5 | Herbert Baldwin Foster | `dio-foster-v5` | have (PG 10890) |
| Dio's Rome, vol. 6 | Herbert Baldwin Foster | `dio-foster-v6` | have (PG 12061) |

Pending (wishlist): Cary Loeb (Greek facing)

## Athenaeus

Shelf: `pipeline/athenaeus_shelf.json`. Yonge (Gutenberg, 3 vols.).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Deipnosophists, or Banquet of the Learned of Athenaeus, vol. 1 | Charles Duke Yonge | `athenaeus-yonge-v1` | have (PG 36921) |
| The Deipnosophists, or Banquet of the Learned of Athenaeus, vol. 2 | Charles Duke Yonge | `athenaeus-yonge-v2` | have (PG 65023) |
| The Deipnosophists, or Banquet of the Learned of Athenaeus, vol. 3 | Charles Duke Yonge | `athenaeus-yonge-v3` | have (PG 66508) |

## Procopius

Shelf: `pipeline/procopius_shelf.json`. Dewing Wars I-VI, the Secret History, Stewart's Buildings (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| History of the Wars, Books I and II: The Persian War | H. B. Dewing | `procopius-dewing-persian` | have (PG 16764) |
| History of the Wars, Books III and IV: The Vandalic War | H. B. Dewing | `procopius-dewing-vandalic` | have (PG 16765) |
| History of the Wars, Books V and VI: The Gothic War | H. B. Dewing | `procopius-dewing-gothic` | have (PG 20298) |
| The Secret History of the Court of Justinian | translator not named in the file | `procopius-secret-history` | have (PG 12916) |
| Of the Buildings of Justinian | Aubrey Stewart | `procopius-stewart-buildings` | have (PG 65404) |

Pending (wishlist): Dewing Wars VII-VIII

## Greek romances

Shelf: `pipeline/greek-romances_shelf.json`. Rowland Smith's Heliodorus, Longus, Achilles Tatius (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Greek Romances of Heliodorus, Longus and Achilles Tatius | Rowland Smith | `greek-romances-smith` | have (PG 55406) |

## Euclid

Shelf: `pipeline/euclid_shelf.json`. Heath's Thirteen Books 1908, 3 vols. (IA, clean-word 0.77-0.83; mathematical OCR).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Thirteen Books of Euclid's Elements, vol. 1 (1908) | T. L. Heath | `euclid-heath-v1` | have-raw (IA `thirteenbookseu02heibgoog`) |
| The Thirteen Books of Euclid's Elements, vol. 2 (1908) | T. L. Heath | `euclid-heath-v2` | have-raw (IA `thirteenbookseu00heibgoog`) |
| The Thirteen Books of Euclid's Elements, vol. 3 (1908) | T. L. Heath | `euclid-heath-v3` | have-raw (IA `thirteenbookseu01heibgoog`) |
| The Thirteen Books of Euclid's Elements | Thomas Little Heath | `euclid-perseus-heath-the-thirteen-books-of-euclid-s-elements` | have (Perseus TEI `tlg1799.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): Heath 2nd ed. (1926)

Excluded: Casey's school adaptation

## Archimedes and Apollonius of Perga

Shelf: `pipeline/archimedes_shelf.json`. Heath's Works (1897), Method (1912), Apollonius's Conics (1896) (IA, 0.73-0.83); Robinson's Method from Heiberg's German (Gutenberg, LaTeX source).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Geometrical Solutions Derived from Mechanics: a Treatise of Archimedes | Lydia G. Robinson from Heiberg's German | `archimedes-method-robinson` | have (PG 7825) |
| The Works of Archimedes (1897) | ed. and T. L. Heath | `archimedes-heath-works` | have-raw (IA `worksofarchimede00arch`) |
| The Method of Archimedes, a supplement to the Works (1912) | ed. and T. L. Heath | `archimedes-heath-method` | have-raw (IA `methodofarchimed00arch`) |
| Apollonius of Perga, Treatise on Conic Sections (1896) | ed. T. L. Heath | `apollonius-perga-heath-conics` | have-raw (IA `treatiseonconics00apolrich`) |

## Hippocrates

Shelf: `pipeline/hippocrates_shelf.json`. Adams: vol. 1 Gutenberg, vol. 2 Sydenham 1849 (IA, 0.93).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Genuine Works of Hippocrates, vol. 1 | Francis Adams | `hippocrates-adams-v1` | have (PG 72583) |
| The Genuine Works of Hippocrates, vol. 2 (Sydenham Society, 1849) | Francis Adams | `hippocrates-adams-v2` | have-raw (IA `b33291408_0004`) |
| Aphorisms | Francis Adams | `hippocrates-perseus-adams-aphorisms` | have (Perseus TEI `tlg0627.tlg012.perseus-eng2`; markup CC BY-SA 4.0) |
| Airs, Waters, and Places | Francis Adams | `hippocrates-perseus-adams-airs-waters-and-places` | have (Perseus TEI `tlg0627.tlg002.perseus-eng3`; markup CC BY-SA 4.0) |
| Airs Waters Places | William Henry Samuel Jones | `hippocrates-perseus-jones-airs-waters-places` | have (Perseus TEI `tlg0627.tlg002.perseus-eng4`; markup CC BY-SA 4.0) |
| Nutriment | William Henry Samuel Jones | `hippocrates-perseus-jones-nutriment` | have (Perseus TEI `tlg0627.tlg046.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Articulations | Francis Adams | `hippocrates-perseus-adams-on-the-articulations` | have (Perseus TEI `tlg0627.tlg010.perseus-eng2`; markup CC BY-SA 4.0) |
| On Injuries of the Head | Francis Adams | `hippocrates-perseus-adams-on-injuries-of-the-head` | have (Perseus TEI `tlg0627.tlg007.perseus-eng2`; markup CC BY-SA 4.0) |
| On Regimen in Acute Diseases | Francis Adams | `hippocrates-perseus-adams-on-regimen-in-acute-diseases` | have (Perseus TEI `tlg0627.tlg004.perseus-eng2`; markup CC BY-SA 4.0) |
| On Fistulae | Francis Adams | `hippocrates-perseus-adams-on-fistulae` | have (Perseus TEI `tlg0627.tlg030.perseus-eng2`; markup CC BY-SA 4.0) |
| On Fractures | Francis Adams | `hippocrates-perseus-adams-on-fractures` | have (Perseus TEI `tlg0627.tlg009.perseus-eng2`; markup CC BY-SA 4.0) |
| On Hemorrhoids | Francis Adams | `hippocrates-perseus-adams-on-hemorrhoids` | have (Perseus TEI `tlg0627.tlg029.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Sacred Disease | Francis Adams | `hippocrates-perseus-adams-on-the-sacred-disease` | have (Perseus TEI `tlg0627.tlg027.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Surgery | Francis Adams | `hippocrates-perseus-adams-on-the-surgery` | have (Perseus TEI `tlg0627.tlg008.perseus-eng2`; markup CC BY-SA 4.0) |
| On Ancient Medicine | Francis Adams | `hippocrates-perseus-adams-on-ancient-medicine` | have (Perseus TEI `tlg0627.tlg001.perseus-eng3`; markup CC BY-SA 4.0) |
| Ancient Medicine | William Henry Samuel Jones | `hippocrates-perseus-jones-ancient-medicine` | have (Perseus TEI `tlg0627.tlg001.perseus-eng4`; markup CC BY-SA 4.0) |
| On Ulcers | Francis Adams | `hippocrates-perseus-adams-on-ulcers` | have (Perseus TEI `tlg0627.tlg028.perseus-eng2`; markup CC BY-SA 4.0) |
| The Epidemics | Francis Adams | `hippocrates-perseus-adams-the-epidemics` | have (Perseus TEI `tlg0627.tlg006.perseus-eng3`; markup CC BY-SA 4.0) |
| The Oath | Francis Adams | `hippocrates-perseus-adams-the-oath` | have (Perseus TEI `tlg0627.tlg013.perseus-eng4`; markup CC BY-SA 4.0) |
| Oath | William Henry Samuel Jones | `hippocrates-perseus-jones-oath` | have (Perseus TEI `tlg0627.tlg013.perseus-eng5`; markup CC BY-SA 4.0) |
| The Law | Francis Adams | `hippocrates-perseus-adams-the-law` | have (Perseus TEI `tlg0627.tlg014.perseus-eng2`; markup CC BY-SA 4.0) |
| Precepts | William Henry Samuel Jones | `hippocrates-perseus-jones-precepts` | have (Perseus TEI `tlg0627.tlg051.perseus-eng2`; markup CC BY-SA 4.0) |
| Of the Prognostics | Francis Adams | `hippocrates-perseus-adams-of-the-prognostics` | have (Perseus TEI `tlg0627.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |
| Mochlicus | Francis Adams | `hippocrates-perseus-adams-mochlicus` | have (Perseus TEI `tlg0627.tlg011.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): Jones/Withington Loeb (Greek facing)

## Galen

Shelf: `pipeline/galen_shelf.json`. Brock's Natural Faculties 1916 (Gutenberg; facing Greek kept).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Galen: On the Natural Faculties | Arthur John Brock | `galen-brock-natural-faculties` | have (PG 43383) |
| On the Natural Faculties | Arthur John Brock | `galen-perseus-brock-on-the-natural-faculties` | have (Perseus TEI `tlg0057.tlg010.perseus-eng2`; markup CC BY-SA 4.0) |

## Aretaeus

Shelf: `pipeline/aretaeus_shelf.json`. Adams 1856, Greek and English (IA, 0.83).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Extant Works of Aretaeus, the Cappadocian (1856) | ed. and Francis Adams | `aretaeus-adams` | have-raw (IA `extantworksaret00adamgoog`) |
| On the Causes and Symptoms of Acute Diseases | Francis Adams | `aretaeus-perseus-adams-on-the-causes-and-symptoms-of-acute-dise` | have (Perseus TEI `tlg0719.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Causes and Symptoms of Chronic Diseases | Francis Adams | `aretaeus-perseus-adams-on-the-causes-and-symptoms-of-chronic-di` | have (Perseus TEI `tlg0719.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Therapeutics of Acute Diseases | Francis Adams | `aretaeus-perseus-adams-on-the-therapeutics-of-acute-diseases` | have (Perseus TEI `tlg0719.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Cure of Chronic Diseases | Francis Adams | `aretaeus-perseus-adams-on-the-cure-of-chronic-diseases` | have (Perseus TEI `tlg0719.tlg004.perseus-eng2`; markup CC BY-SA 4.0) |

## Theophrastus

Shelf: `pipeline/theophrastus_shelf.json`. Bennett & Hammond 1902 (Gutenberg); Jebb 1870 (IA, 0.80; Greek facing).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Characters of Theophrastus | Charles E. Bennett and William A. Hammond | `theophrastus-bennett-hammond` | have (PG 58242) |
| The Characters of Theophrastus (1870) | ed. and R. C. Jebb | `theophrastus-jebb` | have-raw (IA `theophrastoucha02jebbgoog`) |

Pending (wishlist): Hort's Enquiry into Plants (Loeb, Greek facing)

## Hero and Ptolemy

Shelf: `pipeline/greek-mechanics-astronomy_shelf.json`. Greenwood's Hero Pneumatics 1851, Ashmand's Tetrabiblos 1822 (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Pneumatics of Hero of Alexandria | Joseph George Greenwood | `hero-pneumatics-greenwood` | have (PG 77400) |
| Ptolemy's Tetrabiblos | J. M. Ashmand | `ptolemy-tetrabiblos-ashmand` | have (PG 70850) |

## Martial

Shelf: `pipeline/martial_shelf.json`. Bohn prose translation, 1897 printing (IA, 0.88).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Epigrams of Martial, translated into English prose (Bohn; 1897 printing) | Bohn prose translation (anonymous), with verse renderings by various hands | `martial-bohn` | have-raw (IA `epigramsmartial00bohngoog`) |
| Martial, Epigrams, vol. 1: Spectacles, Books I-VII (Loeb, 1919) | Walter C. A. Ker | `martial-ker-v1` | have-raw (IA `martialepigrams01martiala`) |
| Martial, Epigrams, vol. 2: Books VIII-XIV (Loeb, 1920) | Walter C. A. Ker | `martial-ker-v2` | have-raw (IA `martialepigrams02martiala`) |

## Statius

Shelf: `pipeline/statius_shelf.json`. Mozley Loeb 1928, 2 vols. (IA, 0.91-0.92; Latin facing).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Statius, vol. 1: Silvae, Thebaid I-IV (Loeb, 1928) | J. H. Mozley | `statius-mozley-v1` | have-raw (IA `statius01stat`) |
| Statius, vol. 2: Thebaid V-XII, Achilleid (Loeb, 1928) | J. H. Mozley | `statius-mozley-v2` | have-raw (IA `statius02stat`) |

## Claudian

Shelf: `pipeline/claudian_shelf.json`. Platnauer Loeb 1922 (Gutenberg); Hawkins 1817 vol. 1 (IA, 0.85).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Claudian, vol. 1 | Maurice Platnauer | `claudian-platnauer-v1` | have (PG 51443) |
| Claudian, vol. 2 | Maurice Platnauer | `claudian-platnauer-v2` | have (PG 51444) |
| The Works of Claudian, vol. 1 (1817) | A. Hawkins | `claudian-hawkins-v1` | have-raw (IA `worksclaudian00hawkgoog`) |

Pending (wishlist): Hawkins vol. 2 (no text layer)

## Quintilian

Shelf: `pipeline/quintilian_shelf.json`. Butler Loeb 1920-22, 4 vols. (IA, 0.87-0.92; Latin facing).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Institutio Oratoria of Quintilian, vol. 1: Books I-III | H. E. Butler | `quintilian-butler-v1` | have-raw (IA `institutioorator00quin`) |
| The Institutio Oratoria of Quintilian, vol. 2: Books IV-VI | H. E. Butler | `quintilian-butler-v2` | have-raw (IA `institutioorator02quin`) |
| The Institutio Oratoria of Quintilian, vol. 3: Books VII-IX | H. E. Butler | `quintilian-butler-v3` | have-raw (IA `institutioorator03quinuoft`) |
| The Institutio Oratoria of Quintilian, vol. 4: Books X-XII | H. E. Butler | `quintilian-butler-v4` | have-raw (IA `institutioorator04quinuoft`) |

Pending (wishlist): Watson's Bohn (no scan located)

## Vitruvius

Shelf: `pipeline/vitruvius_shelf.json`. Morgan 1914 (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Ten Books on Architecture | Morris Hicky Morgan | `vitruvius-morgan` | have (PG 20239) |

Pending (wishlist): Gwilt (1826)

Excluded: Perrault's abridgment

## Aulus Gellius

Shelf: `pipeline/gellius_shelf.json`. Beloe 1795, vols. 1 and 3 (IA, 0.84-0.86).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Attic Nights of Aulus Gellius, vol. 1 (1795) | William Beloe | `gellius-beloe-v1` | have-raw (IA `bub_gb_j3kBAAAAMAAJ`) |
| The Attic Nights of Aulus Gellius, vol. 2 (1795) | William Beloe | `gellius-beloe-v2` | have-raw (IA `atticnightsofaul02gelliala`) |
| The Attic Nights of Aulus Gellius, vol. 3 (1795) | William Beloe | `gellius-beloe-v3` | have-raw (IA `atticnightsaulu02gellgoog`) |
| The Attic Nights of Aulus Gellius, vol. 1 (Loeb, 1927) | J. C. Rolfe | `gellius-rolfe-v1` | have-raw (IA `bwb_S0-AVN-133`) |
| The Attic Nights of Aulus Gellius, vol. 2 (Loeb, 1927) | J. C. Rolfe | `gellius-rolfe-v2` | have-raw (IA `bwb_S0-AVN-132`) |
| The Attic Nights of Aulus Gellius, vol. 3 (Loeb, 1927) | J. C. Rolfe | `gellius-rolfe-v3` | have-raw (IA `atticnightsofaul0003unse`) |

Pending (wishlist): 

## Ammianus Marcellinus

Shelf: `pipeline/ammianus_shelf.json`. Yonge (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Roman History of Ammianus Marcellinus | Charles Duke Yonge | `ammianus-yonge` | have (PG 28587) |

## Ausonius

Shelf: `pipeline/ausonius_shelf.json`. Evelyn-White Loeb 1919-21, 2 vols. (IA, 0.85-0.87; Latin facing).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Ausonius, with an English translation, vol. 1 | Hugh G. Evelyn-White | `ausonius-evelyn-white-v1` | have-raw (IA `ausonius01evelgoog`) |
| Ausonius, with an English translation, vol. 2 | Hugh G. Evelyn-White | `ausonius-evelyn-white-v2` | have-raw (IA `ausonius02evelgoog`) |

## Frontinus

Shelf: `pipeline/frontinus_shelf.json`. Bennett Loeb 1925 (IA, 0.88; Latin facing).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Frontinus: The Stratagems and The Aqueducts of Rome (Loeb, 1925) | Charles E. Bennett | `frontinus-bennett` | have-raw (IA `frontinus0000unse`) |

## Celsus

Shelf: `pipeline/celsus_shelf.json`. Greive, 1814 edition (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Of Medicine, in Eight Books | James Greive | `celsus-greive` | have (PG 64207) |

## Cato and Varro

Shelf: `pipeline/roman-farming_shelf.json`. Harrison, Roman Farm Management 1918 (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Roman Farm Management: The Treatises of Cato and Varro | Fairfax Harrison | `cato-varro-harrison` | have (PG 12140) |

## Phaedrus

Shelf: `pipeline/phaedrus_shelf.json`. Riley's prose with Smart's verse (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Fables of Phaedrus | Henry T. Riley (prose) and Christopher Smart (verse) | `phaedrus-riley-smart` | have (PG 25512) |

## Justin, Nepos, Eutropius, Florus, Velleius

Shelf: `pipeline/roman-epitomators_shelf.json`. Watson's Bohn volumes 1852-53 (IA, 0.90-0.92).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Justin, Cornelius Nepos, and Eutropius (Bohn, 1853) | John Selby Watson | `justin-nepos-eutropius-watson` | have-raw (IA `justincorneliusn00watsuoft`) |
| Sallust, Florus, and Velleius Paterculus (Bohn, 1852) | John Selby Watson | `sallust-florus-velleius-watson` | have-raw (IA `sallustflorusve00sall`) |
| Lucius Annaeus Florus, Epitome of Roman History; Cornelius Nepos (Loeb, 1929) | E. S. Forster (Florus), J. C. Rolfe (Nepos) | `florus-forster-nepos-rolfe` | have-raw (IA `luciusannaeusflo0000unse`) |

## Justinian

Shelf: `pipeline/justinian_shelf.json`. Moyle's Institutes, 1913 5th ed. (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Institutes of Justinian | John Baron Moyle | `justinian-institutes-moyle` | have (PG 5983) |

## Dionysius of Halicarnassus

Shelf: `pipeline/dionysius-halicarnassus_shelf.json`. Roberts, On Literary Composition 1910 (Gutenberg; Greek facing kept).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Dionysius of Halicarnassus On Literary Composition | ed. and W. Rhys Roberts | `dionysius-roberts-composition` | have (PG 50212) |

Pending (wishlist): Roman Antiquities (Spelman 1758)

## Augustus, Res Gestae

Shelf: `pipeline/augustus_shelf.json`. Fairley 1898 (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Monumentum Ancyranum: The Deeds of Augustus | ed. and William Fairley | `augustus-res-gestae-fairley` | have (PG 66595) |

## Perseus census (overflow)

`docs/perseus-census.md` (generated by `pipeline/perseus_census.py` from the Scaife catalogue): 923 English texts across 82 authors; 3 in the build, 34 already held as the same translation (Evelyn-White's Homeric Hymns), 54 under an author who has a shelf, 832 gaps of which 625 look US public domain by year. Biggest classical gaps: Plutarch (195), Lucian (139), Demosthenes (63), Lysias, Isocrates, Euripides, Plautus, Cicero, Hippocrates, Appian, Suetonius, Aeschylus, Thucydides, Herodotus. These are the wishlist for the next classical burst; Perseus fetching needs a manifest entry or a Perseus mode in `fetch_shelf.py`.
# Translator shelves (each title its own uid; cross-referenced by author sections)

## Dryden

Shelf: `pipeline/dryden_shelf.json` · fetch `python3 pipeline/fetch_shelf.py dryden` · cut titles `python3 pipeline/split_shelf_titles.py dryden`.
Clean text = Project Gutenberg's transcription of Scott's *Works of John Dryden* (18 vols, 1808; PG reprints the 1821 2nd ed.) Titles are cut from those volumes by heading marker; not yet converted to unit-id JSON (the existing converters need a `fetch_sources.py` manifest entry, which the relay may not edit). **No uids minted** — every title awaits Adam's minting pass. Translator for every row: John Dryden (the Garth Metamorphoses is many hands).

Overlap: `dryden-metamorphoses` (Garth 1826, all translators) contains `dryden-ovid-metamorphoses` (Scott 12, Dryden's share). Two witnesses of Dryden's lines, not two passages.

| Title slug | Translates | Work | Status | Source |
|---|---|---|---|---|
| `dryden-aeneid` | Virgil | Aeneid, 12 books (1697) | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `virgil-eclogues` (PG 228; adler's title "Eclogues, Georgics, Aeneid" is wrong, PG 228 is the Aeneid only). Scott 14–15 is a second witness. |
| `dryden-aeneid-dedication` | Virgil | Dedication of the Aeneis (Dryden's essay) | have | Scott 14 |
| `dryden-georgics` | Virgil | Georgics I–IV (1697) | have | Scott 14 |
| `dryden-eclogues` | Virgil | Pastorals I–X (1697) | have | Scott 13 |
| `dryden-metamorphoses` | Ovid | Metamorphoses I–XV, Garth composite ed. (1717; 1826 reprint) — **many hands**, Dryden's share is I, XII and episodes | have-raw | IA `ovidsmetamorphos00ovid` |
| `dryden-ovid-metamorphoses` | Ovid | Metamorphoses: Dryden's own share (I, XII, Ajax & Ulysses, Pythagorean Philosophy, 9 episodes) | have | Scott 12 |
| `dryden-ovid-epistles` | Ovid | Heroides: Canace, Helen, Dido (1680) | have | Scott 12 |
| `dryden-ovid-art-of-love` | Ovid | Ars Amatoria I | have | Scott 12 |
| `dryden-ovid-amores` | Ovid | Amores I.1, I.4 | have | Scott 12 |
| `dryden-theocritus` | Theocritus | Idylls III, XVIII, XXIII, XXVII | have | Scott 12 |
| `dryden-lucretius` | Lucretius | De Rerum Natura, selections I–V | have | Scott 12 |
| `dryden-horace` | Horace | Odes I.3, I.9, I.29; Epode 2 | have | Scott 12 |
| `dryden-iliad` | Homer | Iliad I; Hector and Andromache (VI) | have | Scott 12 |
| `dryden-juvenal` | Juvenal | Satires I, III, VI, X, XVI + Discourse on Satire (1693) | have | Scott 13 |
| `dryden-persius` | Persius | Satires I–VI (1693) | have | Scott 13 |
| `dryden-fables-chaucer` | Chaucer (modernised) | Fables: Palamon & Arcite, Cock & Fox, Flower & Leaf, Wife of Bath, Good Parson (1700) | have | Scott 11 |
| `dryden-fables-boccaccio` | Boccaccio | Fables: Sigismonda, Theodore & Honoria, Cymon & Iphigenia (1700) | have | Scott 11 |
| `dryden-veni-creator` | Latin hymn | Veni Creator Spiritus, paraphrased | have | Scott 11 |
| `dryden-xavier` | Bouhours | Life of St Francis Xavier (1688) | have | Scott 16 |
| `dryden-art-of-painting` | Du Fresnoy | De Arte Graphica (1695) | have | Scott 17 |
| `dryden-history-of-the-league` | Maimbourg | History of the League, complete (1684) | have-raw | IA `historyofleague00maim` (long-s OCR) |
| `dryden-fables-1700` | — | Fables Ancient and Modern, 1st ed. (to restore Dryden's own order) | pending | IA `mdu-rare-075246` |
| `dryden-juvenal-1693` | Juvenal | the whole 1693 book incl. the other translators' satires | pending | IA `juvenaldrydensatires` |
| `dryden-virgil-1697` | Virgil | Works of Virgil as a book (folio or a later reprint) | pending | IA `worksvirgilcont00drydgoog` (1721) |
| `dryden-garth-metamorphoses-1717` | Ovid | Garth 1st ed. | pending | IA, long-s OCR; 1826 reprint preferred |
| `dryden-xavier-1688` | Bouhours | 1st ed. | pending | IA `gpl_1784827` |
| — | Plutarch | "Dryden's Plutarch" | excluded | 41 translators; Malone: "Dryden translated none of the Lives" |
| — | Polybius, Lucian | Dryden's prefaces to others' translations | excluded | not translations |
| — | — | PG 24901, John Fairfield Dryden (US senator) | excluded | wrong Dryden |

## Garnett

Shelf: `pipeline/garnett_shelf.json` · fetch `python3 pipeline/fetch_shelf.py garnett` · titles `python3 pipeline/split_shelf_titles.py garnett`.
All first published 1894–1927: US public domain (pre-1931), UK PD since 2017. Year = first publication of her translation; later printings scanned are recorded in the shelf as `scan_edition`. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `garnett-karamazov` | Dostoevsky | The Brothers Karamazov | Constance Garnett | 1912 | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `dostoevsky-karamazov` (PG 28054) |
| `garnett-idiot` | Dostoevsky | The Idiot | Constance Garnett | 1913 | have-raw | IA `idiotnovelinfour0000fyod` |
| `garnett-possessed` | Dostoevsky | The Possessed | Constance Garnett | 1913 | have | PG 8117 |
| `garnett-crime-and-punishment` | Dostoevsky | Crime and Punishment | Constance Garnett | 1914 | have | PG 2554 |
| `garnett-gambler` | Dostoevsky | The Gambler, and Other Stories | Constance Garnett | 1914 | have-raw | IA `dostoyevsky_fyodor_1821_1881_gambler` |
| `garnett-house-of-the-dead` | Dostoevsky | The House of the Dead | Constance Garnett | 1915 | have-raw | IA `bwb_O4-BDO-591` |
| `garnett-insulted-and-injured` | Dostoevsky | The Insulted and Injured | Constance Garnett | 1915 | have-raw | IA `cu31924026647549` |
| `garnett-raw-youth` | Dostoevsky | A Raw Youth | Constance Garnett | 1916 | have-raw | IA `rawyouth0000fyod` |
| `garnett-eternal-husband` | Dostoevsky | The Eternal Husband, and Other Stories | Constance Garnett | 1917 | have-raw | IA `eternalhusbandot00dost_3` |
| `garnett-white-nights` | Dostoevsky | White Nights, and Other Stories (incl. Notes from Underground) | Constance Garnett | 1918 | have | PG 36034 |
| `garnett-honest-thief` | Dostoevsky | An Honest Thief, and Other Stories | Constance Garnett | 1919 | have-raw | IA `bwb_O8-AOQ-295` |
| `garnett-friend-of-the-family` | Dostoevsky | The Friend of the Family; and Another Story (Novels vol. XII) | Constance Garnett | 1920 | have-raw | IA `friendoffamily0000fyod` |
| `garnett-anna-karenina` | Tolstoy | Anna Karenina | Constance Garnett | 1901 | have | PG 1399 |
| `garnett-death-of-ivan-ilyitch` | Tolstoy | The Death of Ivan Ilyitch, and Other Stories | Constance Garnett | 1902 | have-raw | IA `deathofivanilyit00tols` |
| `garnett-kingdom-of-god` | Tolstoy | "The Kingdom of God Is Within You" | Constance Garnett | 1894 | have | PG 43302 |
| `garnett-christianity-and-patriotism` | Tolstoy | Christianity and Patriotism, with Pertinent Extracts from Other Essays | Constance Garnett | 1922 | have-raw | IA `christianitypatr00tols` |
| `garnett-chekhov-darling` | Chekhov | Tales of Chekhov vol. 1: The Darling, and Other Stories | Constance Garnett | 1916 | have | PG 13416 |
| `garnett-chekhov-duel` | Chekhov | Tales of Chekhov vol. 2: The Duel, and Other Stories | Constance Garnett | 1916 | have | PG 13505 |
| `garnett-chekhov-lady-with-the-dog` | Chekhov | Tales of Chekhov vol. 3: The Lady with the Dog, and Other Stories | Constance Garnett | 1917 | have | PG 13415 |
| `garnett-chekhov-party` | Chekhov | Tales of Chekhov vol. 4: The Party, and Other Stories | Constance Garnett | 1917 | have | PG 13413 |
| `garnett-chekhov-wife` | Chekhov | Tales of Chekhov vol. 5: The Wife, and Other Stories | Constance Garnett | 1918 | have | PG 1883 |
| `garnett-chekhov-bishop` | Chekhov | Tales of Chekhov vol. 7: The Bishop, and Other Stories | Constance Garnett | 1919 | have | PG 13419 |
| `garnett-chekhov-chorus-girl` | Chekhov | Tales of Chekhov vol. 8: The Chorus Girl, and Other Stories | Constance Garnett | 1920 | have | PG 13418 |
| `garnett-chekhov-schoolmistress` | Chekhov | Tales of Chekhov vol. 9: The Schoolmistress, and Other Stories | Constance Garnett | 1920 | have | PG 1732 |
| `garnett-chekhov-horse-stealers` | Chekhov | Tales of Chekhov vol. 10: The Horse-Stealers, and Other Stories | Constance Garnett | 1921 | have | PG 13409 |
| `garnett-chekhov-schoolmaster` | Chekhov | Tales of Chekhov vol. 11: The Schoolmaster, and Other Stories | Constance Garnett | 1921 | have | PG 13412 |
| `garnett-chekhov-cooks-wedding` | Chekhov | Tales of Chekhov vol. 12: The Cook's Wedding, and Other Stories | Constance Garnett | 1922 | have | PG 13417 |
| `garnett-chekhov-love` | Chekhov | Tales of Chekhov vol. 13: Love, and Other Stories | Constance Garnett | 1922 | have | PG 13414 |
| `garnett-chekhov-witch` | Chekhov | Tales of Chekhov vol. 6: The Witch, and Other Stories | Constance Garnett | 1918 | have-raw | IA `witchotherstorie00chek_0` |
| `garnett-chekhov-letters` | Chekhov | Letters of Anton Chekhov to His Family and Friends | Constance Garnett | 1920 | have | PG 6408 |
| `garnett-chekhov-plays-1` | Chekhov | The Plays of Tchehov vol. 1: The Cherry Orchard, and Other Plays | Constance Garnett | 1923 | have-raw | IA `bwb_KU-274-007` |
| `garnett-chekhov-plays-2` | Chekhov | The Plays of Tchehov vol. 2: Three Sisters, and Other Plays | Constance Garnett | 1923 | have-raw | IA `bwb_KU-774-685` |
| `garnett-turgenev-rudin` | Turgenev | Rudin | Constance Garnett | 1894 | have | PG 6900 |
| `garnett-turgenev-house-of-gentlefolk` | Turgenev | A House of Gentlefolk | Constance Garnett | 1894 | have | PG 5721 |
| `garnett-turgenev-on-the-eve` | Turgenev | On the Eve | Constance Garnett | 1895 | have | PG 6902 |
| `garnett-turgenev-fathers-and-children` | Turgenev | Fathers and Children | Constance Garnett | 1895 | have | PG 30723 |
| `garnett-turgenev-smoke` | Turgenev | Smoke | Constance Garnett | 1896 | have | PG 40813 |
| `garnett-turgenev-torrents-of-spring` | Turgenev | The Torrents of Spring | Constance Garnett | 1897 | have | PG 9911 |
| `garnett-turgenev-lear-of-the-steppes` | Turgenev | A Lear of the Steppes, etc. | Constance Garnett | 1898 | have | PG 52642 |
| `garnett-turgenev-dream-tales` | Turgenev | Dream Tales and Prose Poems | Constance Garnett | 1897 | have | PG 8935 |
| `garnett-turgenev-diary-of-a-superfluous-man` | Turgenev | The Diary of a Superfluous Man, and Other Stories | Constance Garnett | 1899 | have | PG 9615 |
| `garnett-turgenev-desperate-character` | Turgenev | A Desperate Character, and Other Stories | Constance Garnett | 1899 | have | PG 8871 |
| `garnett-turgenev-jew` | Turgenev | The Jew, and Other Stories | Constance Garnett | 1899 | have | PG 8696 |
| `garnett-turgenev-knock-knock-knock` | Turgenev | Knock, Knock, Knock, and Other Stories | Constance Garnett | 1921 | have | PG 7120 |
| `garnett-turgenev-sportsmans-sketches` | Turgenev | A Sportsman's Sketches (2 vols) | Constance Garnett | 1895 | have | PG 8597 + PG 8744 |
| `garnett-turgenev-virgin-soil` | Turgenev | Virgin Soil (2 vols) | Constance Garnett | 1896 | have-raw | IA `virginsoil01turguoft` + IA `virginsoil02turguoft` |
| `garnett-turgenev-two-friends` | Turgenev | The Two Friends, and Other Stories | Constance Garnett | 1921 | have-raw | IA `twofriendsothers00turgrich` |
| `garnett-gogol-dead-souls` | Gogol | Dead Souls (Works of Gogol vols 1-2) | Constance Garnett | 1922 | have-raw | IA `p1theworksofniko01gogo` + IA `pt2theworksofnik01gogouoft` |
| `garnett-ostrovsky-storm` | Ostrovsky | The Storm (play) | Constance Garnett | 1899 | have | PG 7991 |
| `garnett-goncharov-common-story` | Goncharov | A Common Story | Constance Garnett | 1894 | have-raw | IA `cu31924026662183` |
| `garnett-herzen-my-past-and-thoughts` | Herzen | My Past and Thoughts (6 vols) | Constance Garnett | 1924-27 | have | PG 76599 … PG 78377 (6 vols) |
| `garnett-gogol-overcoat` | Gogol | The Overcoat, and Other Stories | Constance Garnett | 1923 | have-raw | IA `overcoatothersto0000niko` |
| `garnett-gogol-dikanka` | Gogol | Evenings on a Farm near Dikanka | Constance Garnett | 1926 | have-raw | IA `Dikanka` |
| `garnett-notes-from-underground` | Dostoevsky | Notes from Underground | Constance Garnett | 1918 | have | PG 36034 (cut from the volume) |
| `garnett-gogol-other` | — | Works of Gogol: The Government Inspector and Other Plays (1926) and Mirgorod (1928) - pre-1931, PD; no verified Garnett scan found (IA mirgorodgogol is a 1924 Potsdam Russian edition, not hers). | — | — | pending | — |
| `garnett-dostoevsky-poor-folk` | — | Poor Folk / Uncle's Dream: no Garnett version verified. The 1915 'Poor Folk and The Gambler' scans on IA are the Everyman (C. J. Hogarth) translation. Whether Garnett ever published these is unverified - do not list as hers without a title page. | — | — | pending | — |
| `garnett-war-and-peace-1904` | — | Heinemann 1904 first printing, wanted to replace the later scan. | — | — | pending | — |
| `garnett-turgenev-novels-1894` | — | The rest of the 15-vol Heinemann set as scans (e.g. IA novelsofivanturg02turg ...): only to replace PG texts if they prove defective. | — | — | pending | — |
| `garnett-war-and-peace` | — | Garnett's War and Peace (Heinemann 1904): the only scan found (bwb_P9-DUB-268) is a 1931+ Modern Library Giant. Pre-1931 IA War and Peace scans are other translators (Maude, Dole, Wiener). Removed 2026-10-02; a 1904 Heinemann or McClure scan would restore it. | — | — | pending | — |
| — | — | pg-600, pg-6536: Notes from Underground standalone: duplicates the text inside garnett-white-nights. | — | — | excluded | — |
| — | — | pg-4602: Older transcription of the same Kingdom of God translation; PG 43302 kept. | — | — | excluded | — |
| — | — | pg-1944: The Witch and Other Stories: almost certainly Garnett's Tales vol. 6, but the PG file names no translator; the dated IA scan is used instead. | — | — | excluded | — |
| — | — | pg-2638, pg-2197, pg-2302, pg-1081, pg-47935: The Idiot (Eva Martin), The Gambler and Poor Folk (C. J. Hogarth), Dead Souls (D. J. Hogarth), Fathers and Sons (Hogarth): not Garnett. | — | — | excluded | — |
| — | — | ia-houseofdeadorpri00dostuoft: House of the Dead 1911: predates Garnett's 1915 version; no Garnett on the title page. | — | — | excluded | — |
| — | — | ia-warpeace01tols_0: War and Peace, Carlton House edition, undated: rule - undatable printings excluded. | — | — | excluded | — |
| — | — | ia-dli/in.ernet scans: Digital Library of India copies: their _djvu.txt files 404 at the expected path; Cornell/Toronto/other scans used instead. | — | — | excluded | — |
| — | — | chekhov-plays-1930-modern-library: The Plays of Anton Tchekov (Modern Library, 1929-30): a reprint of the 1923 volumes, which are used. | — | — | excluded | — |
| — | — | ia-mirgorodgogol: Mirgorod, Potsdam 1924 (Kiepenheuer): a Russian-language edition, not Garnett. | — | — | excluded | — |
| — | — | ia-poorfolkgambler00dost: Poor Folk; The Gambler (1915): Everyman edition, C. J. Hogarth's translation. | — | — | excluded | — |
| — | — | ia-honestthief0000fyod: Heinemann printing reset in 1957 (imprint: first published 1919, reprinted 1923, new impression 1950, reprinted (reset) 1957, reprinted 1962): post-1930 resetting, replaced. | — | — | excluded | — |
| — | — | ia-bwb_KR-628-394: Cherry Orchard and Other Plays, Phoenix Library: imprint 'first issued in the Phoenix Library 1935, reprinted 1940' (a review caught the date; the first pick was wrongly dated 1923). Replaced by the 1925 Chatto printing. | — | — | excluded | — |
| — | — | rawyouth00dostuoft: IA dates it Heinemann 1916, but its imprint page reads 'new impression 1956': a post-1930 printing (review 2026-10-02). | — | — | excluded | — |
| — | — | rawyouthnovelint00dost: IA dates it Macmillan 1916; imprint page reads 'reprinted 1923, 1950, 1956, 1964, 1970': a 1970s printing. | — | — | excluded | — |
| — | — | cu31924014422020: Cornell copy IA-dated 1914, but its imprint page lists new impressions to 1957: a 1957 printing (review 2026-10-02). | — | — | excluded | — |
| — | — | novelsoffyodordo12dost: IA-dated 1920; imprint page reads 'new impression 1949, reprinted 1951, 1961, 1969, 1974'. | — | — | excluded | — |
| — | — | friendoffamily0000unse_r7t4: Heinemann 1920 per IA; imprint page reads reprinted to 1969. | — | — | excluded | — |
| — | — | bwb_P9-DUB-268: Modern Library Giant War and Peace (Random House). IA dates it 1910, but the Giants series began in 1931: a post-1930 printing. | — | — | excluded | — |

## Cary (Dante, Pindar)

Shelf: `pipeline/cary_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cary` · titles `python3 pipeline/split_shelf_titles.py cary`.
Added at the coordinator's relay, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cary-inferno` | Dante | Inferno (Hell) | Henry Francis Cary | 1805-06; revised 1814 | held elsewhere (cross-ref) | `pipeline/fetch_sources.py` → `divine_comedy` (PG 8800) |
| `cary-purgatorio` | Dante | Purgatorio | Henry Francis Cary | 1814 | held elsewhere (cross-ref) | `pipeline/fetch_sources.py` → `divine_comedy` (PG 8800) |
| `cary-paradiso` | Dante | Paradiso | Henry Francis Cary | 1814 | held elsewhere (cross-ref) | `pipeline/fetch_sources.py` → `divine_comedy` (PG 8800) |
| `cary-pindar` | Pindar | Odes (Olympian, Pythian, Nemean, Isthmian) | Henry Francis Cary | 1833 | have-raw | IA `pindarinenglish00carygoog` |
| `cary-aristophanes-birds` | — | Cary's Birds of Aristophanes (1824): no scan found this run. | — | — | pending | — |
| `cary-dore-illustrated` | — | PG 8779-8800 Doré-illustrated Cary: same text split into parts (excluded as duplicates; images are the only difference). | — | — | pending | — |
| — | — | pg-1008: Divine Comedy complete: same text as 1005-1007 together. | — | — | excluded | — |
| — | — | pg-10660: Lives of the English Poets: Cary's own prose, not a translation. | — | — | excluded | — |

## Longfellow (Dante and shorter translations)

Shelf: `pipeline/longfellow_shelf.json` · fetch `python3 pipeline/fetch_shelf.py longfellow` · titles `python3 pipeline/split_shelf_titles.py longfellow`.
Added at the coordinator's relay, vetoable. His Virgil and Ovid pieces stay with lane B. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `longfellow-inferno` | Dante | Inferno | Henry Wadsworth Longfellow | 1867 | have | PG 1001 |
| `longfellow-purgatorio` | Dante | Purgatorio | Henry Wadsworth Longfellow | 1867 | have | PG 1002 |
| `longfellow-paradiso` | Dante | Paradiso | Henry Wadsworth Longfellow | 1867 | have | PG 1003 |
| `longfellow-translations` | various | Translations (Complete Poetical Works): Coplas de Manrique, Spanish ballads and sonnets, Frithiof's Saga passages, German lyrics, Beowulf passage, French, Italian (Michelangelo sonnets, Dante passages), Portuguese, Eastern | Henry Wadsworth Longfellow | 1833-1882 | have | PG 1365 (cut from the volume) |
| `longfellow-latin-pieces` | — | Virgil's First Eclogue and Ovid in Exile, inside longfellow-poetical-works: cross-ref -> lane B's Virgil/Ovid sections; not cut here. | — | — | pending | — |
| `longfellow-poets-and-poetry-of-europe` | — | The Poets and Poetry of Europe (1845): an anthology mostly of OTHER translators; only Longfellow's own pieces would belong here. | — | — | pending | — |
| — | — | pg-1004: Divine Comedy complete: same text as 1001-1003. | — | — | excluded | — |
| — | — | original-poems: Hiawatha, Evangeline etc. are his own poems, not translations (an author section would hold them). | — | — | excluded | — |

## Florio (Montaigne, Decameron)

Shelf: `pipeline/florio_shelf.json` · fetch `python3 pipeline/fetch_shelf.py florio` · titles `python3 pipeline/split_shelf_titles.py florio`.
Added at the coordinator's relay, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `florio-montaigne-essays` | Montaigne | Essayes (3 books), 6 vols | John Florio | 1603 | have-raw | IA `essayestranslate01montuoft` … IA `essayestranslate06montuoft` (6 vols) |
| `florio-decameron` | Boccaccio | The Decameron (first complete English, 1620) | attributed to John Florio (published anonymously, 1620) | 1620 | have | PG 52617 + PG 52618 |
| `florio-montaigne-1603-folio` | — | The 1603 first edition (IA MontaigneImages / McGill 1632 folio): only images or long-s OCR; the 1906 reprint is used. | — | — | pending | — |
| `florio-montaigne-everyman` | — | Everyman (1910) or Temple Classics (1897) Florio sets: alternate witnesses if the Gibbings OCR proves weak. | — | — | pending | — |
| — | — | pg-56200: Queen Anna's New World of Words: Florio's dictionary, not a translation (could join a lexicon shelf, Adam's call). | — | — | excluded | — |
| — | — | pg-3600-cotton: PG's Montaigne Essays is Charles Cotton's translation, not Florio. | — | — | excluded | — |

## Burton (Arabian Nights, Camoens)

Shelf: `pipeline/burton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py burton` · titles `python3 pipeline/split_shelf_titles.py burton`.
Added at the coordinator's relay, vetoable. Catullus, Kama Sutra and Pentamerone are listed but not fetched: your call on content. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `burton-arabian-nights` | The Thousand and One Nights (Arabic) | The Book of the Thousand Nights and a Night, 10 vols | Richard Francis Burton | 1885 | have | PG 51252 … PG 58360 (10 vols) |
| `burton-supplemental-nights` | The Thousand and One Nights (Arabic) | Supplemental Nights, 6 vols (vol. 3 in two PG parts) | Richard Francis Burton | 1886-88 | have | PG 59156 … PG 64384 (7 vols) |
| `burton-lusiads` | Camoens | Os Lusiadas | Richard Francis Burton | 1880 | have | PG 77660 + PG 77661 |
| `burton-camoens-lyricks` | Camoens | The Lyricks: sonnets, canzons, odes and sextines | Richard Francis Burton | 1884 | have-raw | IA `cu31924102142985` |
| `burton-catullus` | — | The Carmina of Catullus (1894, with Leonard Smithers; PG 20732): PD; held back for Adam's call on content, not rights. | — | — | pending | — |
| `burton-kama-sutra` | — | Kama Sutra (1883, with Arbuthnot and Bhide; PG 27827): PD; Adam's call on content. | — | — | pending | — |
| `burton-pentamerone` | — | Basile, Il Pentamerone (1893): the IA copy found is a 1927 reprint (ilpentameroneort0000basi); PD as a pre-1931 printing - listed, not fetched, for the same content call. | — | — | pending | — |
| `burton-vikram` | — | Vikram and the Vampire (PG 2400/48511): Burton's free adaptation of the Baital Pachisi, not a translation; PG names no translator. | — | — | pending | — |
| — | — | pg-3435..3450: Older PG transcriptions of the same Nights and Supplemental Nights; the DP proofread editions (51252..64384) are used. | — | — | excluded | — |
| — | — | pg-6036: The Kasidah: Burton's own poem presented as a translation (a literary mask). | — | — | excluded | — |
| — | — | travel-books: Pilgrimage to Al-Madinah, Lake Regions, etc.: his own prose, not translations (an author section would hold them). | — | — | excluded | — |

## Maude (Tolstoy, PD editions only)

Shelf: `pipeline/maude_shelf.json` · fetch `python3 pipeline/fetch_shelf.py maude` · titles `python3 pipeline/split_shelf_titles.py maude`.
Added at the coordinator's relay, vetoable. Only printings before 1931; where the file gives no year, the title rests on Gutenberg's US clearance, which the Tr. column says. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `maude-war-and-peace` | Tolstoy | War and Peace | Aylmer and Louise Maude | pre-1931 printing per Project Gutenberg's US copyright clearance; the file states no edition year | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `tolstoy-warpeace` (PG 2600) |
| `maude-resurrection` | Tolstoy | Resurrection | Louise Maude | 1900 (Dodd, Mead, 'by my authority' note signed by Tolstoy); exact year not printed in the file | have | PG 1938 |
| `maude-father-sergius` | Tolstoy | Father Sergius | Aylmer and Louise Maude | pre-1931 printing per Project Gutenberg's US copyright clearance; the file states no edition year | have | PG 985 |
| `maude-master-and-man` | Tolstoy | Master and Man | Aylmer and Louise Maude | pre-1931 printing per Project Gutenberg's US copyright clearance; the file states no edition year | have | PG 986 |
| `maude-cossacks` | Tolstoy | The Cossacks | Aylmer and Louise Maude | pre-1931 printing per Project Gutenberg's US copyright clearance; the file states no edition year | have | PG 4761 |
| `maude-what-men-live-by` | Tolstoy | What Men Live By, and Other Tales | Aylmer and Louise Maude | pre-1931 printing per Project Gutenberg's US copyright clearance; the file states no edition year | have | PG 6157 |
| `maude-plays` | Tolstoy | Plays, Complete Edition including the Posthumous Plays (6 plays) | Louise and Aylmer Maude | 1914 ed. | have | PG 26661 … PG 26666 (6 vols) |
| `maude-what-is-art` | Tolstoy | What Is Art? | Aylmer Maude | 1904 (Funk & Wagnalls, stated) | have | PG 64908 |
| `maude-the-devil` | Tolstoy | The Devil | Aylmer Maude | 1926 ('First published in 1926', stated) | have | PG 67224 |
| `maude-three-days` | Tolstoy | Three Days in the Village, and Other Sketches | Aylmer and Louise Maude | 1910 (Free Age Press, stated) | have | PG 51018 |
| `maude-anna-karenina` | — | Anna Karenina, tr. L. & A. Maude (World's Classics 1918): not on PG under their names; look for a pre-1931 scan. | — | — | pending | — |
| `maude-centenary` | — | The Centenary Edition (OUP 1928-37, 21 vols): only the volumes printed before 1931 qualify; per-volume dating needed. | — | — | pending | — |
| — | — | pg-28920: War and Peace Book 1 only: part of PG 2600. | — | — | excluded | — |
| — | — | pg-52242, pg-78278: Aylmer Maude's own books (Life of Tolstoy, Life of Marie Stopes): not translations. | — | — | excluded | — |
| — | — | pg-79027: Tolstoy on Art: Maude as editor/compiler; overlaps What Is Art?. | — | — | excluded | — |
| — | — | other-maudes: PG items by Alice Maude Kellogg, Maude Alma, F. N. Maude, Maude Wholohan: different people. | — | — | excluded | — |
| — | — | pg-26472: Newer transcription of What Men Live By: its .txt returns 404 on Gutenberg's cache (2026-10-02); PG 6157 used. | — | — | excluded | — |
| — | — | pg-26660: Plays: Complete Edition, front matter only (the transcriber's note says the plays are posted separately as 26661-26666, which are used). | — | — | excluded | — |

## Cotton (Montaigne)

Shelf: `pipeline/cotton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py cotton` · titles `python3 pipeline/split_shelf_titles.py cotton`.
Added by lane C under the coordinator's keep-going relay, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `cotton-montaigne-essays` | Montaigne | Essays, 3 books (with Hazlitt's notes and the Letters) | Charles Cotton (rev. W. C. Hazlitt) | 1685-86; Hazlitt revision 1877 | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `montaigne-essays` (PG 3600) |
| `cotton-scarron-lucian` | — | Cotton's Scarronides (burlesque Virgil): non-Dryden Virgil belongs to lane B; listed only. | — | — | pending | — |
| — | — | pg-3581..3599: The same Cotton/Hazlitt text in 19 parts; PG 3600 complete used. | — | — | excluded | — |

## Ormsby (Don Quixote)

Shelf: `pipeline/ormsby_shelf.json` · fetch `python3 pipeline/fetch_shelf.py ormsby` · titles `python3 pipeline/split_shelf_titles.py ormsby`.
Added by lane C, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `ormsby-don-quixote` | Cervantes | Don Quixote, Parts I-II | John Ormsby | 1885 | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `cervantes-quixote` (PG 996) |
| — | — | pg-5903..5946, pg-28842: Doré-illustrated or partial Gutenberg copies of the same Ormsby text. | — | — | excluded | — |

## Urquhart & Motteux (Rabelais; Motteux's Quixote)

Shelf: `pipeline/urquhart-motteux_shelf.json` · fetch `python3 pipeline/fetch_shelf.py urquhart-motteux` · titles `python3 pipeline/split_shelf_titles.py urquhart-motteux`.
Added by lane C, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `urquhart-motteux-rabelais` | Rabelais | Gargantua and Pantagruel, Books I-V | Thomas Urquhart (Books I-III), Peter Anthony Motteux (IV-V) | 1653-1694 | held elsewhere (cross-ref) | `pipeline/adler_shelf.json` → `rabelais-gargantua` (PG 1200) |
| `motteux-don-quixote` | Cervantes | The History of Don Quixote | Peter Anthony Motteux | 1700-03 | have | PG 35993 |
| — | — | pg-8166..8170: Doré-illustrated Rabelais, same text in parts. | — | — | excluded | — |

## FitzGerald (Omar, Jami, Calderón)

Shelf: `pipeline/fitzgerald_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fitzgerald` · titles `python3 pipeline/split_shelf_titles.py fitzgerald`.
Added by lane C, vetoable. His Greek plays stay with lane B. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fitzgerald-rubaiyat-salaman` | Omar Khayyam; Jami | Rubáiyát (the editions as printed in this volume) and Salámán and Absál | Edward FitzGerald | 1859-79 / 1856 | have | PG 22535 |
| `fitzgerald-calderon` | Calderon | Eight Dramas of Calderon, freely translated | Edward FitzGerald | 1853/1865 | have | PG 63776 |
| `fitzgerald-agamemnon` | — | FitzGerald's Agamemnon (1865) and Oedipus plays: Greek tragedy is lane B's queued item; cross-ref only. | — | — | pending | — |
| `fitzgerald-bird-parliament` | — | Attar's Bird Parliament (in his Letters and Literary Remains, 1889): needs a scan. | — | — | pending | — |
| — | — | pg-246, pg-35260: Single Rubaiyat editions, contained in PG 22535. | — | — | excluded | — |
| — | — | pg-2587: Life Is a Dream (PG header: tr. FitzGerald): his version is 'Such Stuff as Dreams Are Made Of', which is printed inside PG 63776. Not fetched as a likely duplicate; not compared line by line. | — | — | excluded | — |
| — | — | pg-10315: Persian Literature anthology: mixed translators. | — | — | excluded | — |

## Bayard Taylor (Faust)

Shelf: `pipeline/taylor_shelf.json` · fetch `python3 pipeline/fetch_shelf.py taylor` · titles `python3 pipeline/split_shelf_titles.py taylor`.
Added by lane C, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `taylor-faust-part-1` | Goethe | Faust, Part I | Bayard Taylor | 1870 | held elsewhere (cross-ref) | `pipeline/fetch_sources.py` → `faust` (PG 14591) |
| `taylor-faust-part-2` | Goethe | Faust, Part II | Bayard Taylor | 1871 | have-raw | IA `goethetaylorfaust02` |
| — | — | original-works: Taylor's own travel books, novels and poems: not translations. | — | — | excluded | — |

## E. W. Lane (Thousand and One Nights)

Shelf: `pipeline/lane_shelf.json` · fetch `python3 pipeline/fetch_shelf.py lane` · titles `python3 pipeline/split_shelf_titles.py lane`.
Added by lane C, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `lane-arabian-nights` | The Thousand and One Nights (Arabic) | The Thousand and One Nights, 3 vols | Edward William Lane | 1838-40 (1859 ed.) | have-raw | PG 34206 + IA `thousandonenight02harvuoft` + IA `thousandonenight03laneuoft` |
| `lane-selections-kuran` | — | Selections from the Kur-an (PG 44515): Lane as translator of Quranic passages; Adam's call whether scripture of other faiths belongs on a translator shelf. | — | — | pending | — |
| — | — | pg-41110: Arabian Society in the Middle Ages: Lane's notes, not a translation. | — | — | excluded | — |
| — | — | pg-70796: Modern Egyptians: Lane's own book. | — | — | excluded | — |
| — | — | ia-emory-1883: Chatto 1883 set (emory.edu): its text files are not at the standard path. | — | — | excluded | — |

## Lady Charlotte Guest (Mabinogion)

Shelf: `pipeline/guest_shelf.json` · fetch `python3 pipeline/fetch_shelf.py guest` · titles `python3 pipeline/split_shelf_titles.py guest`.
Added by lane C, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `guest-mabinogion` | Welsh tales (Red Book of Hergest) | The Mabinogion | Lady Charlotte Guest | 1838-49 | have | PG 5160 |
| — | — | pg-19959, 19973, 19976: O. M. Edwards's 3-vol reprint of the same Guest text; PG 5160 used. | — | — | excluded | — |
| — | — | pg-15551, pg-67425: Retellings (Clay; Lanier's Boy's Mabinogion), not translations. | — | — | excluded | — |
# Storytellers

## Andrew Lang

Shelf: `pipeline/lang_shelf.json` (2026-10-02). 95 Gutenberg books (clean text, converted to `data/books/` by `pipeline/convert_shelf_gutenberg.py`: 102,483 paragraph units under headings read from each book's own Contents) and 29 Internet Archive volumes (raw OCR, unconverted). CCEL holds no Lang. Not yet registered in the manifest; no uids minted (attended step). Co-authors and co-translators are credited in each title; "Mrs. Lang" is Leonora Blanche Lang, who wrote much of the later story books. His Homer translations stay here with their own slugs (`lang-odyssey`, `lang-iliad`, `lang-homeric-hymns`) for a future Homer section to cross-reference.

| Work | Status | Where |
|---|---|---|
| The Blue Fairy Book (1889) | have | PG 503, `lang-blue-fairy-book` (1921 units) |
| The Red Fairy Book (1890) | have | PG 540, `lang-red-fairy-book` (3187 units) |
| The Green Fairy Book (1892), ill. H. J. Ford | have | PG 33571, `lang-green-fairy-book` (2028 units) |
| The Yellow Fairy Book (1894), ill. H. J. Ford | have | PG 28314, `lang-yellow-fairy-book` (2150 units) |
| The Pink Fairy Book (1897) | have | PG 5615, `lang-pink-fairy-book` (2141 units) |
| The Grey Fairy Book (1900), ill. H. J. Ford | have | PG 33547, `lang-grey-fairy-book` (2369 units) |
| The Violet Fairy Book (1901) | have | PG 641, `lang-violet-fairy-book` (2321 units) |
| The Crimson Fairy Book (1903) | have | PG 2435, `lang-crimson-fairy-book` (1746 units) |
| The Brown Fairy Book (1904), ill. H. J. Ford | have | PG 31201, `lang-brown-fairy-book` (1875 units) |
| The Orange Fairy Book (1906), ill. H. J. Ford | have | PG 36532, `lang-orange-fairy-book` (2342 units) |
| The Olive Fairy Book (1907), ill. H. J. Ford | have | PG 27826, `lang-olive-fairy-book` (1959 units) |
| The Lilac Fairy Book (1910), ill. H. J. Ford | have | PG 28096, `lang-lilac-fairy-book` (2379 units) |
| The Arabian Nights Entertainments (1898, Lang's selection) | have | PG 128, `lang-arabian-nights` (1836 units) |
| The Blue Poetry Book (anthology ed. Lang, 7th ed.) | have | PG 46515, `lang-blue-poetry-book` (1612 units) |
| The True Story Book (1893) | have | PG 27602, `lang-true-story-book` (961 units) |
| The Red True Story Book (1895) | have | PG 27603, `lang-red-true-story-book` (1732 units) |
| The Animal Story Book (1896) | have | PG 38208, `lang-animal-story-book` (1495 units) |
| The Nursery Rhyme Book (1897) | have | PG 26197, `lang-nursery-rhyme-book` (1503 units) |
| The Book of Romance (1902) | have | PG 26646, `lang-book-of-romance` (1367 units) |
| The Red Romance Book (1905) | have | PG 24624, `lang-red-romance-book` (1923 units) |
| Tales of Romance (based on The Book of Romance) | have | PG 33152, `lang-tales-of-romance` (650 units) |
| The Red Book of Heroes (1909), by Mrs. Lang, ed. Andrew Lang | have | PG 19078, `lang-red-book-of-heroes` (1358 units) |
| The Book of Princes and Princesses (1908), by Mrs. Lang, ed. Andrew Lang | have | PG 46145, `lang-book-of-princes-and-princesses` (942 units) |
| The Strange Story Book (1913), by Mrs. Lang, ed. Andrew Lang | have | PG 37396, `lang-strange-story-book` (1622 units) |
| Prince Prigio (1889) | have | PG 20850, `lang-prince-prigio` (428 units) |
| Prince Ricardo of Pantouflia (1893) | have | PG 21994, `lang-prince-ricardo` (669 units) |
| The Gold of Fairnilee (1888) | have | PG 21934, `lang-gold-of-fairnilee` (324 units) |
| The Princess Nobody: A Tale of Fairyland (1884) | have | PG 52545, `lang-princess-nobody` (178 units) |
| Tales of Troy and Greece (1907) | have | PG 32326, `lang-tales-of-troy-and-greece` (849 units) |
| A Monk of Fife (1895) | have | PG 1631, `lang-monk-of-fife` (1509 units) |
| The Mark of Cain (1886) | have | PG 21821, `lang-mark-of-cain` (1250 units) |
| Much Darker Days (1884) | have | PG 21933, `lang-much-darker-days` (557 units) |
| In the Wrong Paradise, and Other Stories (1886) | have | PG 13984, `lang-in-the-wrong-paradise` (677 units) |
| The Disentanglers (1902) | have | PG 17031, `lang-disentanglers` (3144 units) |
| The World's Desire (1890), with H. Rider Haggard | have | PG 2763, `lang-worlds-desire` (1412 units) |
| Parson Kelly (1899), with A. E. W. Mason | have | PG 38684, `lang-parson-kelly` (2683 units) |
| He (1887 parody), with W. H. Pollock | have | PG 25589, `lang-he` (521 units) |
| 'That Very Mab' (1885), with May Kendall | have | PG 21337, `lang-that-very-mab` (511 units) |
| The Odyssey of Homer, prose tr. S. H. Butcher & Andrew Lang | have | PG 1728, `lang-odyssey` (1372 units) |
| The Iliad, prose tr. Andrew Lang, Walter Leaf & Ernest Myers | have | PG 3059, `lang-iliad` (1101 units) |
| The Homeric Hymns: a new prose translation, and essays (1899) | have | PG 16338, `lang-homeric-hymns` (400 units) |
| Theocritus, Bion and Moschus, rendered into English prose by Andrew Lang | have | PG 4775, `lang-theocritus` (1011 units) |
| Aucassin and Nicolete, tr. Andrew Lang | have | PG 1578, `lang-aucassin` (281 units) |
| Ballads and Lyrics of Old France, with Other Poems (1872) | have | PG 795, `lang-ballads-lyrics-old-france` (358 units) |
| XXXII Ballades in Blue China (1885) | have | PG 51160, `lang-ballades-blue-china` (215 units) |
| Rhymes a la Mode (1884) | have | PG 1645, `lang-rhymes-a-la-mode` (342 units) |
| Grass of Parnassus (1888) | have | PG 1060, `lang-grass-of-parnassus` (304 units) |
| Ban and Arriere Ban: A Rally of Fugitive Rhymes (1894) | have | PG 1855, `lang-ban-and-arriere-ban` (256 units) |
| New Collected Rhymes (1905) | have | PG 1746, `lang-new-collected-rhymes` (272 units) |
| Ballades and Verses Vain (1884) | have | PG 45173, `lang-ballades-verses-vain` (398 units) |
| Helen of Troy (1882) | have | PG 3229, `lang-helen-of-troy` (427 units) |
| A Collection of Ballads (ed. Lang, 1897) | have | PG 1054, `lang-collection-of-ballads` (1622 units) |
| Letters to Dead Authors (1886) | have | PG 3319, `lang-letters-to-dead-authors` (386 units) |
| Letters on Literature (1889) | have | PG 1395, `lang-letters-on-literature` (430 units) |
| Essays in Little (1891) | have | PG 1594, `lang-essays-in-little` (546 units) |
| Books and Bookmen (1886) | have | PG 1961, `lang-books-and-bookmen` (280 units) |
| Adventures Among Books (1905) | have | PG 1994, `lang-adventures-among-books` (663 units) |
| Old Friends: Essays in Epistolary Parody (1890) | have | PG 1991, `lang-old-friends` (432 units) |
| The Library (1881) | have | PG 2018, `lang-library` (228 units) |
| Angling Sketches (1891) | have | PG 2022, `lang-angling-sketches` (303 units) |
| Introduction to the Compleat Angler (Lang's introduction only) | have | PG 2422, `lang-compleat-angler-intro` (106 units) |
| How to Fail in Literature: A Lecture (1890) | have | PG 2566, `lang-how-to-fail-in-literature` (87 units) |
| Lost Leaders (1889), ed. W. Pett Ridge | have | PG 16529, `lang-lost-leaders` (157 units) |
| The Puzzle of Dickens's Last Plot (1905) | have | PG 738, `lang-puzzle-dickens-last-plot` (139 units) |
| Shakespeare, Bacon, and the Great Unknown (1912) | have | PG 5127, `lang-shakespeare-bacon` (933 units) |
| Alfred Tennyson (1901) | have | PG 3654, `lang-alfred-tennyson` (643 units) |
| Sir Walter Scott (1906) | have | PG 61245, `lang-sir-walter-scott` (531 units) |
| Sir Walter Scott and the Border Minstrelsy (1910) | have | PG 4088, `lang-scott-border-minstrelsy` (848 units) |
| History of English Literature from Beowulf to Swinburne (1912) | have | PG 56613, `lang-history-english-literature` (2932 units) |
| Oxford: Brief Historical and Descriptive Notes | have | PG 2444, `lang-oxford` (192 units) |
| Highways and Byways in the Border (1913), with John Lang | have | PG 47800, `lang-highways-byways-border` (2015 units) |
| Custom and Myth (1884) | have | PG 14080, `lang-custom-and-myth` (701 units) |
| Custom and Myth, new edition (1885) — a distinct edition, kept as its own witness | have | PG 33260, `lang-custom-and-myth-new-ed` (1406 units) |
| Myth, Ritual and Religion, vol. 1 | have | PG 2832, `lang-myth-ritual-religion-1` (1136 units) |
| Myth, Ritual and Religion, vol. 2 | have | PG 36794, `lang-myth-ritual-religion-2` (1389 units) |
| The Making of Religion (1898) | have | PG 12353, `lang-making-of-religion` (1960 units) |
| Modern Mythology (1897) | have | PG 14576, `lang-modern-mythology` (832 units) |
| Magic and Religion (1901) | have | PG 46480, `lang-magic-and-religion` (1305 units) |
| The Secret of the Totem (1905) | have | PG 45363, `lang-secret-of-the-totem` (855 units) |
| Method in the Study of Totemism (1911) | have | PG 46546, `lang-method-study-totemism` (242 units) |
| Social Origins (Lang) and Primal Law (J. J. Atkinson), 1903 | have | PG 45724, `lang-social-origins` (1065 units) |
| The Book of Dreams and Ghosts (1897) | have | PG 12621, `lang-book-of-dreams-and-ghosts` (976 units) |
| Cock Lane and Common-Sense (1894) | have | PG 12674, `lang-cock-lane` (768 units) |
| The Clyde Mystery: A Study in Forgeries and Folklore (1905) | have | PG 20902, `lang-clyde-mystery` (479 units) |
| Homer and His Age (1906) | have | PG 7972, `lang-homer-and-his-age` (746 units) |
| The World of Homer (1910) | have | PG 45896, `lang-world-of-homer` (1391 units) |
| A Short History of Scotland (1912) | have | PG 15955, `lang-short-history-scotland` (645 units) |
| John Knox and the Reformation (1905) | have | PG 14016, `lang-john-knox` (1043 units) |
| The Mystery of Mary Stuart (1901) | have | PG 42910, `lang-mystery-of-mary-stuart` (1694 units) |
| James VI and the Gowrie Mystery (1902) | have | PG 31033, `lang-james-vi-gowrie` (982 units) |
| Pickle the Spy (1897) | have | PG 6807, `lang-pickle-the-spy` (1057 units) |
| The Companions of Pickle (1898) | have | PG 68956, `lang-companions-of-pickle` (1302 units) |
| Historical Mysteries (1904) | have | PG 18679, `lang-historical-mysteries` (799 units) |
| The Valet's Tragedy, and Other Studies (1903) | have | PG 2073, `lang-valets-tragedy` (1133 units) |
| The Story of Joan of Arc (1906) | have | PG 48470, `lang-story-of-joan-of-arc` (233 units) |
| Poetical Works, ed. Mrs. Lang (1923), vol. 1 | have-raw | IA `poeticalworks01lang`, `lang-poetical-works-01` |
| Poetical Works (1923), vol. 2 | have-raw | IA `poeticalworks02languoft`, `lang-poetical-works-02` |
| Poetical Works (1923), vol. 3 | have-raw | IA `poeticalworks03languoft`, `lang-poetical-works-03` |
| Poetical Works (1923), vol. 4 | have-raw | IA `poeticalworks04languoft`, `lang-poetical-works-04` |
| A History of Scotland from the Roman Occupation (1900-07), vol. 1 | have-raw | IA `historyofscotlan01languoft`, `lang-history-scotland-01` |
| A History of Scotland, vol. 2 | have-raw | IA `scotlandhisuni02languoft`, `lang-history-scotland-02` |
| A History of Scotland, vol. 3 | have-raw | IA `scotlandhisuni03languoft`, `lang-history-scotland-03` |
| A History of Scotland, vol. 4 | have-raw | IA `scotlandhistuni04languoft`, `lang-history-scotland-04` |
| Homer and the Epic (1893) | have-raw | IA `homerepic00languoft`, `lang-homer-and-the-epic` |
| The Book of Saints and Heroes (1912), by Mrs. Lang, ed. Andrew Lang | have-raw | IA `bookofsaintshe00lang`, `lang-book-of-saints-and-heroes` |
| The All Sorts of Stories Book (1911), by Mrs. Lang, ed. Andrew Lang | have-raw | IA `allsortsofstorie00langiala`, `lang-all-sorts-of-stories-book` |
| The Red Book of Animal Stories (1899) | have-raw | IA `redbookofanimals00languoft`, `lang-red-book-of-animal-stories` |
| The Life and Letters of John Gibson Lockhart (1897), vol. 1 | have-raw | IA `lifelettersofjoh01langiala`, `lang-lockhart-01` |
| The Life and Letters of John Gibson Lockhart (1897), vol. 2 | have-raw | IA `lifelettersofjoh02langiala`, `lang-lockhart-02` |
| Life, Letters, and Diaries of Sir Stafford Northcote (1890), vol. 1 | have-raw | IA `lifelettersdiari0001lang`, `lang-northcote-01` |
| Life, Letters, and Diaries of Sir Stafford Northcote (1890), vol. 2 | have-raw | IA `lifelettersdiari0002lang`, `lang-northcote-02` |
| The Maid of France (1908) | have-raw | IA `maidoffrancebein00languoft`, `lang-maid-of-france` |
| Prince Charles Edward Stuart, the Young Chevalier (1903) | have-raw | IA `princecharlesedw00lang`, `lang-prince-charles-edward` |
| St. Andrews (1893) | have-raw | IA `standrews00langrich`, `lang-st-andrews` |
| Sir George Mackenzie, King's Advocate, of Rosehaugh (1909) | have-raw | IA `sirgeorgemackenz00languoft`, `lang-sir-george-mackenzie` |
| Portraits and Jewels of Mary Stuart (1906) | have-raw | IA `portraitsjewelso00lang`, `lang-portraits-jewels-mary-stuart` |
| The King over the Water (1907), with Alice Shield | have-raw | IA `kingoverwater00shieuoft`, `lang-king-over-the-water` |
| The Story of the Golden Fleece (1903) | have-raw | IA `storyofgoldenfle00lang`, `lang-story-of-the-golden-fleece` |
| New and Old Letters to Dead Authors (1907) | have-raw | IA `newandoldletters00languoft`, `lang-new-and-old-letters-dead-authors` |
| Devil-Dancers, Witch-Finders, Rain-Makers, and Medicine-Men (1896) | have-raw | IA `devildancerswitc00lang`, `lang-devil-dancers` |
| The Politics of Aristotle: Introductory Essays (1886) | have-raw | IA `politicsofaristo00langrich`, `lang-politics-of-aristotle-essays` |
| The Dead Leman, and Other Tales from the French (1889), tr. Lang & Paul Sylvester | have-raw | IA `deadlemanotherta00langiala`, `lang-dead-leman` |
| The Miracles of Madame Saint Katherine of Fierbois (1897), tr. Lang | have-raw | IA `MiraclesOfMadameStKatherineOfFierbois`, `lang-miracles-st-katherine` |
| The Origins of Religion, and Other Essays (1908) | have-raw | IA `originsreligion01assogoog`, `lang-origins-of-religion` |
| Tales of a Fairy Court (1907) | pending | not on Gutenberg; not on Internet Archive (author and title searches, 2026-10-02); wanted |
| La Jeanne d'Arc de M. Anatole France (1909) | pending | IA `lajeannedarcdema00lang`; French; whether Lang wrote it in French or it was translated is unverified |
| Clean text of the 29 OCR-only volumes (History of Scotland, Poetical Works, Lockhart, Northcote, Maid of France, ...) | pending | wishlist: proofread transcriptions |
| Duplicate Gutenberg transcriptions (fairy books PG 640, 3027, 3282, 3454, 6746, 7277; Letters to Dead Authors PG 1491; Prince Prigio PG 21935; Tales of Troy part PG 1973) | excluded | one transcription of each book is held |
| Selections and reissues (Magic Ring, Pretty Goldilocks, Golden Mermaid, Ballades & Rhymes PG 3138, My Own Fairy Book, modern "Rainbow"/"Rose" selections) | excluded | contents already held |
| Tales of King Arthur (PG 49057) | excluded | J. C. Allen's adaptation of The Book of Romance |
| Others' books Lang edited or introduced (Scott's Waverley novels, Dickens, Stevenson Swanston ed., Perrault, Kirk's Secret Commonwealth, Grimm tr. Hunt, Malory ed. Sommer, Longinus tr. Havell, and ~20 more) | excluded | each belongs on its own author's shelf; full list in the shelf's `_excluded` |
| Multi-author volumes with a Lang chapter (Cricket, Anthropology and the Classics, A Batch of Golfing Papers, Poets' Country, ...) | excluded | not Lang's book |
| The Annesley Case (1912); La Pucelle de France (1911) | excluded | trial documents Lang edited; a French translation of The Maid of France by another hand |

## Charles Lamb

Shelf: `pipeline/lamb_shelf.json` (2026-10-02). Spine: *The Works of Charles and Mary Lamb*, ed. E. V. Lucas (Methuen, 1903-05, 7 vols). Gutenberg has six volumes as clean text (its US-issue numbers differ from Methuen's; both are given); vol. IV comes from Internet Archive as raw OCR. Gutenberg books are converted to `data/books/` by `pipeline/convert_shelf_gutenberg.py` (units = paragraphs under headings read from each book's own Contents); not yet registered in the manifest and no uids minted (attended step). Mary Lamb is credited on every work she co-wrote.

| Work | Status | Where |
|---|---|---|
| Tales from Shakespeare (1807), by Charles and Mary Lamb | have | PG 573, `lamb-tales-from-shakespeare` (826 units) |
| The Adventures of Ulysses (1808) | have | PG 7768, `lamb-adventures-of-ulysses` (275 units) |
| Poetry for Children (1809), by Charles and Mary Lamb | have | PG 68359, `lamb-poetry-for-children` (333 units) |
| Works of Charles and Mary Lamb, ed. E. V. Lucas (1903-05) — Miscellaneous Prose (Methuen vol. I; PG 'Volume 1') | have | PG 40988, `lamb-works-lucas-misc-prose` (3453 units) |
| Works, ed. Lucas — Elia and The Last Essays of Elia (Methuen vol. II; PG 'Volume 2') | have | PG 10343, `lamb-works-lucas-elia` (2091 units) |
| Works, ed. Lucas — Books for Children, by Charles and Mary Lamb (Methuen vol. III; PG 'Volume 3') | have | PG 10130, `lamb-works-lucas-books-for-children` (2220 units) |
| Works, ed. Lucas — Poems and Plays (Methuen vol. V; PG labels it 'Volume 4') | have | PG 11576, `lamb-works-lucas-poems-and-plays` (3613 units) |
| Works, ed. Lucas — Letters of Charles and Mary Lamb, 1796-1820 (Methuen vol. VI; PG 'Volume 5') | have | PG 9365, `lamb-works-lucas-letters-1796-1820` (4074 units) |
| Works, ed. Lucas — Letters 1821-1842 (Methuen vol. VII; PG 'Volume 6') | have | PG 10851, `lamb-works-lucas-letters-1821-1842` (5130 units) |
| Works, ed. Lucas (Methuen 1903-05), vol. IV: Dramatic Specimens and the Garrick Plays — the one Lucas volume Gutenberg lacks | have-raw | IA `cu31924016657193`, `lamb-works-lucas-dramatic-specimens` |
| Beauty and the Beast (1811; attributed to Lamb, attribution doubtful), 1887 facsimile reprint with an introduction by Andrew Lang | have-raw | IA `beautyandbeastwi00lambuoft`, `lamb-beauty-and-the-beast` |
| Essays of Elia (1823) and The Last Essays of Elia (1833) | have | Lucas vol. II (`lamb-works-lucas-elia`) |
| Rosamund Gray; the miscellaneous essays, criticism (On the Tragedies of Shakspeare, On the Genius of Hogarth), Table-Talk, uncollected periodical prose | have | Lucas vol. I (`lamb-works-lucas-misc-prose`) |
| Mrs. Leicester's School (with Mary Lamb), The King and Queen of Hearts, Prince Dorus | have | Lucas vol. III (`lamb-works-lucas-books-for-children`) |
| John Woodvil, Mr. H——, The Wife's Trial, Album Verses, Blank Verse (with Lloyd), the poems | have | Lucas vol. V (`lamb-works-lucas-poems-and-plays`) |
| Specimens of English Dramatic Poets (1808) and the Garrick Plays extracts | have-raw | Lucas vol. IV (IA); also many standalone IA scans (1835-1907) |
| The letters of Charles and Mary Lamb | have | Lucas vols. VI-VII |
| Clean text of Lucas vol. IV (OCR 97.2% known words, see Measurements) | pending | wishlist: a proofread transcription; IA has a second Methuen scan and standalone Specimens editions to repair OCR from |
| Ainger's edition (The Life and Works of Charles Lamb, 1899-1900, 12 vols) | pending | IA `lifeworksofcharl10lambuoft` and siblings; a second scholarly witness, not fetched |
| Eliana (1864), Lamb and Hazlitt: Further Letters (1899-1900), Talfourd's Final Memorials (1848) | pending | IA; early gatherings of letters and uncollected pieces, superseded by Lucas but useful as witnesses |
| The Letters of Charles Lamb, ed. Lucas (1935, 3 vols) | pending | likely still in copyright (1935); Adam might license; not fetched |
| Tales from Shakespeare — PG 1286, PG 20657 (Rackham 1909) | excluded | duplicate transcriptions; PG 573 held |
| Best Letters (PG 10125), Roast Pig (PG 43566), Masque of Days (PG 24015), school selections | excluded | selections from works held |
| Works in Four Volumes, vol. 4 (PG 14129) | excluded | one stray volume of an older edition, superseded by Lucas |
| Blue Jar Story Book (PG 34470) | excluded | multi-author anthology |
| Coleridge's Poems (1796, 1797) with early Lamb sonnets | excluded | Coleridge's shelf; Lamb's poems are in Lucas vol. V |
| Books about Lamb (Lucas's Life, Charles Lamb and the Lloyds, Bon-mots) | excluded | not Lamb's text |

### Lane D measurements (2026-10-02)

- **OCR quality of the raw volumes.** Share of OCR words (2+ letters) found in a vocabulary built from the 104 clean Gutenberg texts of these two shelves (words seen twice or more, 56,402 words). All 30 raw volumes score 94.4%-99.1%. Lowest: Miracles of St Katherine 94.4% (much Old French), Politics of Aristotle essays 95.5%, St Andrews 95.7%, Origins of Religion 95.8%, Homer and the Epic 95.8%. Lucas vol. IV 97.2%. Highest: Story of the Golden Fleece 99.1%, All Sorts of Stories Book 98.9%. A rough guide to which volumes most want a clean text, not a proofreading score: the vocabulary is Lang and Lamb's own.
- **Heading detection.** After a per-book chapter rule for four Lang novels (The Mark of Cain, The Gold of Fairnilee, Much Darker Days, Prince Ricardo — their "CHAPTER I.--Title" lines escaped the Contents rule), three books still sit mostly under one heading: The Nursery Rhyme Book (its five sections are italic numbered lines), Aucassin and Nicolete (the chantefable's alternating "Here singeth one / So say they" structure), and Custom and Myth, new edition (46% of its units are the index). Their citations are paragraph-in-book until a structure rule is written.
- **Story and letter boundaries (second pass).** The house rule treats any ALL-CAPS line as a heading, which in these books also catches signatures ("C. LAMB"), addressee lines, plate captions and part numerals, so one story or letter was split across several "headings" and the same heading text recurred (duplicate unit ids). Two shelf-side options in `convert_shelf_gutenberg.py` fix this without touching structure_texts.py: Lucas's letters use `LETTER n` as the only heading (vol. VI: 259 letters, 0 duplicate ids, was 1,748; vol. VII: 354 letters, 0, was 1,932), so a citation reads `LETTER 263A, par. 4`. And 30 books use only their own Contents, read leniently (punctuation and hyphens may differ, Contents may be italic): adopted only where the result lands within 15% of the Contents count with no more duplicate ids than before. The Blue, Red and Green Fairy Books now hold exactly 37, 37 and 42 tales; Tales from Shakespeare exactly its 20 tales plus preface. Still unfixed, recorded: Helen of Troy (Book + numbered stanza wants a stanza-aware converter), the Elia volume and Lucas vol. I (their Contents do not match their body headings), and several poetry books whose Contents list first lines.

## George MacDonald

Shelf: `pipeline/macdonald_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Spine: CCEL ThML (31 works, converted with `convert_shelf.py`); Gutenberg for the 27 books CCEL lacks (converted with `convert_shelf_gutenberg.py`); 3 books as raw Internet Archive OCR. Scripture links appear only in the CCEL ThML (67 links, mostly in the Unspoken Sermons). Known structure gaps: Far Above Rubies, Stephen Archer and the Hamlet study sit mostly under one heading. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Phantastes: A Faerie Romance (1858) | have | CCEL `phantastes_faerie`, `macdonald-phantastes` (515 units) |
| David Elginbrod (1863) | have | CCEL `elginbrod`, `macdonald-david-elginbrod` (3620 units) |
| Adela Cathcart (1864), vol. 1 | have | CCEL `adela1`, `macdonald-adela-cathcart-1` (987 units) |
| Adela Cathcart, vol. 2 | have | CCEL `adela2`, `macdonald-adela-cathcart-2` (697 units) |
| Adela Cathcart, vol. 3 | have | CCEL `adela3`, `macdonald-adela-cathcart-3` (925 units) |
| The Portent and Other Stories | have | CCEL `portent`, `macdonald-portent` (961 units) |
| Annals of a Quiet Neighbourhood (1867) | have | CCEL `neighbourhood`, `macdonald-annals-quiet-neighbourhood` (2446 units) |
| Unspoken Sermons, First Series (1867) | have | CCEL `unspoken1`, `macdonald-unspoken-sermons-1` (332 units) |
| Unspoken Sermons, Second Series (1885) | have | CCEL `unspoken2`, `macdonald-unspoken-sermons-2` (368 units) |
| Unspoken Sermons, Third Series (1889) | have | CCEL `unspoken3`, `macdonald-unspoken-sermons-3` (336 units) |
| The Seaboard Parish (1868) | have | CCEL `seaboardparish`, `macdonald-seaboard-parish` (2636 units) |
| Robert Falconer (1868) | have | CCEL `rfalconer`, `macdonald-robert-falconer` (4280 units) |
| The Miracles of Our Lord (1870) | have | CCEL `miracles`, `macdonald-miracles-of-our-lord` (373 units) |
| At the Back of the North Wind (1871) | have | CCEL `backofnorth`, `macdonald-back-of-north-wind` (2011 units) |
| The Princess and the Goblin (1872) | have | CCEL `princessgoblin`, `macdonald-princess-and-goblin` (1047 units) |
| The Vicar's Daughter (1872) | have | CCEL `vicardaughter`, `macdonald-vicars-daughter` (2379 units) |
| The Light Princess (1864) | have | CCEL `princess`, `macdonald-light-princess` (298 units) |
| Cross Purposes and The Shadows | have | CCEL `purposes_shadows`, `macdonald-cross-purposes-shadows` (292 units) |
| The Day Boy and the Night Girl (1879) | have | CCEL `dayboy`, `macdonald-day-boy-night-girl` (171 units) |
| Thomas Wingfold, Curate (1876) | have | CCEL `thomaswingfold`, `macdonald-thomas-wingfold` (2090 units) |
| Sir Gibbie (1879) | have | CCEL `sirgibbie`, `macdonald-sir-gibbie` (1993 units) |
| A Book of Strife in the Form of the Diary of an Old Soul (1880) | have | CCEL `strife`, `macdonald-diary-of-an-old-soul` |
| The Princess and Curdie (1883) | have | CCEL `princesscurdie`, `macdonald-princess-and-curdie` (879 units) |
| Donal Grant (1883) | have | CCEL `donal_grant`, `macdonald-donal-grant` (3517 units) |
| A Double Story (The Wise Woman, 1875) | have | CCEL `doublestory`, `macdonald-double-story` (546 units) |
| The Elect Lady (1888) | have | CCEL `lady`, `macdonald-elect-lady` (1234 units) |
| The Hope of the Gospel (1892) | have | CCEL `hope`, `macdonald-hope-of-the-gospel` (305 units) |
| Heather and Snow (1893) | have | CCEL `heatherandsnow`, `macdonald-heather-and-snow` (1349 units) |
| There and Back (1891) | have | CCEL `there_back`, `macdonald-there-and-back` (2926 units) |
| Lilith (1895) | have | CCEL `lilith`, `macdonald-lilith` (1964 units) |
| Salted with Fire (1897) | have | CCEL `saltedfire`, `macdonald-salted-with-fire` (1036 units) |
| Alec Forbes of Howglen (1865) | have | PG 18810, `macdonald-alec-forbes` (4127 units) |
| Guild Court: A London Story (1868) | have | PG 56176, `macdonald-guild-court` (3055 units) |
| Ranald Bannerman's Boyhood (1871) | have | PG 9301, `macdonald-ranald-bannerman` (1280 units) |
| Wilfrid Cumbermede (1872) | have | PG 9183, `macdonald-wilfrid-cumbermede` (3797 units) |
| Gutta-Percha Willie (1873) | have | PG 10093, `macdonald-gutta-percha-willie` (956 units) |
| Malcolm (1875) | have | PG 7127, `macdonald-malcolm` (4573 units) |
| St. George and St. Michael (1876) | have | PG 5753, `macdonald-st-george-st-michael` (2974 units) |
| The Marquis of Lossie (1877) | have | PG 7174, `macdonald-marquis-of-lossie` (2999 units) |
| Paul Faber, Surgeon (1879) | have | PG 12387, `macdonald-paul-faber` (2113 units) |
| Mary Marston (1881) | have | PG 8201, `macdonald-mary-marston` (3060 units) |
| Warlock o' Glenwarlock (Castle Warlock, 1882) | have | PG 6364, `macdonald-warlock-o-glenwarlock` (2907 units) |
| Weighed and Wanting (1882) | have | PG 9096, `macdonald-weighed-and-wanting` (2419 units) |
| Stephen Archer, and Other Tales (1883) | have | PG 9191, `macdonald-stephen-archer` (2288 units) |
| What's Mine's Mine (1886) | have | PG 5969, `macdonald-whats-mines-mine` (3140 units) |
| Home Again (1887) | have | PG 8924, `macdonald-home-again` (999 units) |
| The Flight of the Shadow (1891) | have | PG 8902, `macdonald-flight-of-the-shadow` (1236 units) |
| A Rough Shaking (1891) | have | PG 8886, `macdonald-rough-shaking` (2387 units) |
| Far Above Rubies (1898) | have | PG 8955, `macdonald-far-above-rubies` (298 units) |
| For the Right (1888) | not taken | PG 36904: a novel by K. E. Franzos, tr. Julie Sutter, with MacDonald's preface only; removed by the 2026-10-02 audit |
| The Light Princess and Other Fairy Stories (collection) | have | PG 18811, `macdonald-light-princess-other-stories` (839 units) |
| A Dish of Orts: Chiefly Papers on the Imagination, and on Shakespeare (1893) | have | PG 9393, `macdonald-dish-of-orts` (694 units) |
| England's Antiphon (1868), an anthology of English religious verse with MacDonald's commentary | have | PG 10375, `macdonald-englands-antiphon` (1698 units) |
| The Tragedie of Hamlet: A Study with the Text of the Folio of 1623 (1885) | have | PG 10606, `macdonald-hamlet-study` (3340 units) |
| A Hidden Life and Other Poems | have | PG 10578, `macdonald-hidden-life` (1132 units) |
| The Poetical Works of George MacDonald (1893), vol. 1 | have | PG 9543, `macdonald-poetical-works-1` (2670 units) |
| The Poetical Works of George MacDonald (1893), vol. 2 | have | PG 9984, `macdonald-poetical-works-2` (2214 units) |
| Rampolli: Growths from a Long-Planted Root (1897), translations and poems | have | PG 8949, `macdonald-rampolli` (617 units) |
| Dealings with the Fairies (1867), the first fairy-tale collection | have-raw | IA `dealingswithfair00macd_0`, `macdonald-dealings-with-the-fairies` |
| A Threefold Cord: Poems by Three Friends (1883), ed. MacDonald | have-raw | IA `threefoldcordpoe00macd`, `macdonald-threefold-cord` |
| Scotch Songs and Ballads (1893) | have-raw | IA `scotchsongsballa00macduoft`, `macdonald-scotch-songs-ballads` |
| macdonald-pg-duplicates | excluded | Gutenberg copies of works held from CCEL (PG 225, 18614, 325, 697, 708, 34339, 709, 36612, 1640, 1953, 2291, 2370, 2433, 2561, 5676, 5773, 5976 and its vols 5973-5975, 8562 and vols 8551-8553, 8879, 8892, 8913, 8929, 8943, 8944, 9057, 9103, 9154, 9155, 9471, 18859) and per-volume splits of St George (5750-5752) and What's Mine's Mine (5966-5968): CCEL ThML or the complete PG file held instead |
| macdonald-ccel-salted | excluded | CCEL `salted`: a second CCEL copy of Salted with Fire; `saltedfire` held |
| macdonald-ccel-unspoken | excluded | CCEL `unspoken`: a 3.6 KB series index, not a text |
| macdonald-imagination-essays | excluded | The Imagination and Other Essays (Boston, 1883): the essays of A Dish of Orts (held) |
| macdonald-anthologies | excluded | Selections and anthologies by other hands (Beautiful Thoughts, Cheerful Words, Fairy Tales Every Child Should Know, The Golden Key 1906 reprint, The Cruel Painter extract) |


## The Brothers Grimm (tr. Margaret Hunt)

Shelf: `pipeline/grimm_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Margaret Hunt's Household Tales (1884), the translation Andrew Lang introduced. Gutenberg's clean text cites by tale number, using a per-book rule: `53 Little Snow-White, par. 4`. There are exactly 200 tales and 10 Children's Legends. The 1884 two-volume edition, with Lang's introduction and the Grimms' notes, is kept as raw OCR. Cross-reference: the Lang shelf's excluded list points here. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Household Tales by Brothers Grimm, tr. Margaret Hunt (1884), the 200 tales and 10 children's legends | have | PG 5314, `grimm-hunt-household-tales` (1769 units) |
| Grimm's Household Tales, tr. Margaret Hunt, with the author's notes and an introduction by Andrew Lang (1884), vol. 1 | have-raw | IA `grimmshouseholdt01grim`, `grimm-hunt-1884-01` |
| Grimm's Household Tales, tr. Margaret Hunt (1884), vol. 2 | have-raw | IA `grimmshouseholdt2grim`, `grimm-hunt-1884-02` |
| grimm-selections | excluded | selections and retellings: Grimm's Fairy Stories (PG 11027, Owen/Gruelle), Snowdrop & Other Tales (PG 37381, Rackham, a Hunt selection), Grimm's Fairy Tales (PG 52521, ed. Olcott), Household Tales ill. Anning Bell (1912 selection) |
| grimm-widger-index | excluded | PG 59508 is an index of Gutenberg's Grimm files, not a text |
| grimm-same-surname | excluded | other Grimms: Florence M. Grimm (Astronomical Lore in Chaucer), George Grimm (Australian Explorers), Constantin de Grimm (illustrator) |
| grimm-other-languages | excluded | French, Icelandic, Dutch, Polish, Portuguese, Hungarian and Finnish Gutenberg translations: not English |
| grimm-pending-alternates | pending | Edgar Taylor and Marian Edwardes's translation (PG 2591), Lucy Crane's Household Stories (PG 19068, ill. Walter Crane), and the German originals (Deutsche Sagen PG 76558; KHM) — alternate witnesses Adam may want |


## Hans Christian Andersen

Shelf: `pipeline/andersen_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). There is no single canonical English Andersen, so each Victorian translation is held as its own work and its own slug, with the translator in the title. Where a Gutenberg file names no translator, the title says so. PG 27200's translator is inferred from its wording, not verified. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Fairy Tales of Hans Christian Andersen (translator not named in the Gutenberg file; its wording matches the text usually credited to Mrs. H. B. Paull, 1872 — unverified) | have | PG 27200, `andersen-fairy-tales-paull` (4825 units) |
| What the Moon Saw, and Other Tales, tr. H. W. Dulcken (1866) | have | PG 27000, `andersen-what-the-moon-saw-dulcken` (2225 units) |
| Wonderful Stories for Children, tr. Mary Howitt (1846) | have | PG 43600, `andersen-wonderful-stories-howitt` (501 units) |
| The True Story of My Life, tr. Mary Howitt (1847) | have | PG 7007, `andersen-true-story-of-my-life-howitt` (579 units) |
| The Sand-Hills of Jutland, tr. Anna Bushby (1860) | have | PG 26491, `andersen-sand-hills-of-jutland-bushby` (1047 units) |
| The Ice-Maiden, and Other Tales, tr. Fanny Fuller (1863) | have | PG 18604, `andersen-ice-maiden-fuller` (459 units) |
| A Christmas Greeting: A Series of Stories (1847; translator not named in the Gutenberg file) | have | PG 31103, `andersen-christmas-greeting` (587 units) |
| O. T., A Danish Romance (novel; translator not named in the Gutenberg file) | have | PG 7513, `andersen-o-t` (1922 units) |
| Pictures of Sweden (travel; translator not named in the Gutenberg file) | have | PG 12313, `andersen-pictures-of-sweden` (558 units) |
| Stories for the Household, tr. H. W. Dulcken (1889 printing), the fullest Victorian collection | have-raw | IA `storiesforhouseh00ande`, `andersen-stories-household-dulcken` |
| Fairy Tales and Other Stories, revised and in part newly translated by W. A. Craigie (Oxford, 1914) | have-raw | IA `fairytalesandoth00andeuoft`, `andersen-fairy-tales-craigie` |
| Danish Fairy Legends and Tales, tr. Caroline Peachey (1861 ed.) | have-raw | IA `danishfairylege00andegoog`, `andersen-danish-fairy-legends-peachey` |
| Fairy Tales and Stories, tr. H. L. Brækstad, ill. Hans Tegner (1900) | have-raw | IA `fairytalesstorie00ande`, `andersen-fairy-tales-braekstad` |
| Faery Tales from Hans Christian Andersen, tr. Mrs. Edgar Lucas (1910) | have-raw | IA `faerytalesfromha00ande`, `andersen-faery-tales-lucas` |
| The Improvisatore, or, Life in Italy (novel), tr. Mary Howitt (1845) | have-raw | IA `improvisatoreorl00ande`, `andersen-improvisatore-howitt` |
| A Picture-Book without Pictures, and Other Stories (1848; IA credits Mary Howitt, unverified) | have-raw | IA `picturebookwitho00ande`, `andersen-picture-book-without-pictures` |
| andersen-selections | excluded | selections whose texts are held in fuller form: Andersen's Fairy Tales (PG 1597), Stories from Hans Andersen (PG 17860, Dulac), Stickney's First and Second Series (PG 32571-32572), Heath Robinson's Hans Andersen's Fairy Tales (PG 66688), The Nightingale (PG 71096, one tale), Rudy and Babette (PG 40283, the Ice-Maiden) |
| andersen-other-languages | excluded | French, German, Dutch, Catalan, Esperanto, Greek and Finnish Gutenberg translations: not English |
| andersen-hersholt | excluded | Jean Hersholt's Complete Andersen (1942-49): in copyright |
| andersen-pending | pending | Mrs. H. B. Paull's Hans Andersen's Fairy Tales and Stories (1872) as a scan to confirm PG 27200's translator; Under the Willow Tree (Dulcken, 1870); Only a Fiddler and In Spain (Howitt/Bushby); the Danish originals |


## Charles Kingsley

Shelf: `pipeline/kingsley_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). All 43 of his English Gutenberg texts: the children's books, the novels, poems and plays, the sermons, lectures and essays. Single-essay files (Plays and Puritans, Sir Walter Raleigh, Froude's History, Phaethon, Women and Politics) have a single heading, which is correct. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Heroes; Or, Greek Fairy Tales for My Children | have | PG 677, `kingsley-heroes` (860 units) |
| Glaucus; Or, The Wonders of the Shore | have | PG 695, `kingsley-glaucus` (386 units) |
| The Water-Babies | have | PG 1018, `kingsley-water-babies` (1437 units) |
| Alexandria and Her Schools Four Lectures Delivered at the Philosophical Institution, Edinburgh | have | PG 1275, `kingsley-alexandria-and-her-schools` (177 units) |
| The Ancien Régime | have | PG 1335, `kingsley-ancien-regime` (183 units) |
| Historical Lectures and Essays | have | PG 1360, `kingsley-historical-lectures-and-essays` (355 units) |
| Sanitary and Social Lectures and Essays | have | PG 1637, `kingsley-sanitary-and-social-lectures-and-essays` (495 units) |
| Madam How and Lady Why; Or, First Lessons in Earth Lore for Children | have | PG 1697, `kingsley-madam-how-and-lady-why` (1145 units) |
| Westward Ho! Or, The Voyages and Adventures of Sir Amyas Leigh, Knight, of Burrough, in the County of Devon, in the Reig | have | PG 1860, `kingsley-westward-ho` (4993 units) |
| Plays and Puritans | have | PG 3142, `kingsley-plays-and-puritans` (141 units) |
| Sir Walter Raleigh and His Time | have | PG 3143, `kingsley-sir-walter-raleigh-and-his-time` (195 units) |
| Froude's History of England | have | PG 3144, `kingsley-froudes-history-of-england` (75 units) |
| The Roman and the Teuton A Series of Lectures delivered before the University of Cambridge (ed. F. Max Müller) | have | PG 3821, `kingsley-roman-and-the-teuton` (786 units) |
| The Water of Life, and Other Sermons | have | PG 5687, `kingsley-water-of-life-and-other-sermons` (613 units) |
| Hypatia — or New Foes with an Old Face | have | PG 6308, `kingsley-hypatia` (3302 units) |
| Prose Idylls, New and Old | have | PG 7032, `kingsley-prose-idylls-new-and-old` (658 units) |
| Discipline and Other Sermons | have | PG 7042, `kingsley-discipline-and-other-sermons` (541 units) |
| The Good News of God | have | PG 7051, `kingsley-good-news-of-god` (991 units) |
| Hereward, the Last of the English | have | PG 7815, `kingsley-hereward` (4239 units) |
| Twenty-Five Village Sermons | have | PG 7954, `kingsley-twenty-five-village-sermons` (331 units) |
| Sermons on National Subjects | have | PG 8202, `kingsley-sermons-on-national-subjects` (712 units) |
| Alton Locke, Tailor and Poet: An Autobiography | have | PG 8374, `kingsley-alton-locke` (2476 units) |
| The Hermits | have | PG 8733, `kingsley-hermits` (632 units) |
| All Saints' Day and Other Sermons | have | PG 10116, `kingsley-all-saints-day-and-other-sermons` (688 units) |
| Town Geology | have | PG 10251, `kingsley-town-geology` (405 units) |
| The Gospel of the Pentateuch: A Set of Parish Sermons | have | PG 10325, `kingsley-gospel-of-the-pentateuch` (658 units) |
| David: Five Sermons | have | PG 10326, `kingsley-david` (155 units) |
| Yeast: a Problem | have | PG 10364, `kingsley-yeast` (1846 units) |
| Scientific Essays and Lectures | have | PG 10427, `kingsley-scientific-essays-and-lectures` (387 units) |
| At Last: A Christmas in the West Indies | have | PG 10669, `kingsley-at-last` (1209 units) |
| Two Years Ago, Volume I | have | PG 10920, `kingsley-two-years-ago-1` (2261 units) |
| Two Years Ago, Volume II. | have | PG 10995, `kingsley-two-years-ago-2` (2916 units) |
| Phaethon: Loose Thoughts for Loose Thinkers | have | PG 11025, `kingsley-phaethon` (486 units) |
| Literary and General Lectures and Essays | have | PG 11026, `kingsley-literary-and-general-lectures-and-essays` (600 units) |
| Andromeda, and Other Poems | have | PG 11064, `kingsley-andromeda-and-other-poems` (522 units) |
| The Saint's Tragedy | have | PG 11346, `kingsley-saints-tragedy` (1325 units) |
| Sermons for the Times | have | PG 11381, `kingsley-sermons-for-the-times` (455 units) |
| Town and Country Sermons | have | PG 11536, `kingsley-town-and-country-sermons` (699 units) |
| Health and Education | have | PG 17437, `kingsley-health-and-education` (706 units) |
| Westminster Sermons with a Preface | have | PG 18369, `kingsley-westminster-sermons-with-a-preface` (812 units) |
| True Words for Brave Men: A Book for Soldiers' and Sailors' Libraries | have | PG 20138, `kingsley-true-words-for-brave-men` (546 units) |
| Women and Politics | have | PG 20433, `kingsley-women-and-politics` (43 units) |
| Lectures Delivered in America in 1874 | have | PG 30944, `kingsley-lectures-delivered-in-america-in-1874` (346 units) |
| kingsley-illustrated-duplicates | excluded | The Water-Babies, PG 25564 (Goble) and 36309 (J. W. Smith): other transcriptions; PG 1018 held |
| kingsley-selections | excluded | Daily Thoughts (PG 20711) and Out of the Deep (PG 20312): selections by his widow from works held |
| kingsley-finnish | excluded | Finnish translations (PG 49025, 57285, 72487) |
| kingsley-pending | pending | Charles Kingsley: His Letters and Memories of His Life (ed. his widow, 1877), the Life and Works edition (1901-03), and the uncollected Poems volume of 1884 — Internet Archive scans |


## Nathaniel Hawthorne (children's books)

Shelf: `pipeline/hawthorne_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Only the storyteller's shelf: the two Greek-myth books, Grandfather's Chair and the Biographical Stories. His novels and tales are listed as pending for Adam to decide. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| A Wonder-Book for Girls and Boys (1851), ill. Walter Crane | have | PG 32242, `hawthorne-wonder-book` (870 units) |
| Tanglewood Tales (1853) | have | PG 976, `hawthorne-tanglewood-tales` (797 units) |
| The Whole History of Grandfather's Chair (1841) | have | PG 1926, `hawthorne-grandfathers-chair` (857 units) |
| Biographical Stories (1842), from True Stories of History and Biography | have | PG 9254, `hawthorne-biographical-stories` (363 units) |
| hawthorne-duplicates | excluded | A Wonder Book and Tanglewood Tales (PG 35377, Parrish ill., both books in one file), Tanglewood Tales (PG 51995, Sterrett ill.), and the single Wonder-Book tales (PG 9255-9258): texts held |
| hawthorne-not-this-shelf | pending | PENDING, outside this storytellers shelf unless Adam widens it: the novels (Scarlet Letter, Seven Gables, Blithedale, Marble Faun, Fanshawe), Twice-Told Tales, Mosses from an Old Manse, The Snow-Image and the single-story Gutenberg files cut from them (PG 9201-9245), notebooks |


## Thomas Bulfinch

Shelf: `pipeline/bulfinch_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The three books later bound as *Bulfinch's Mythology* are held as three works, plus Oregon and Eldorado. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Age of Fable, or Stories of Gods and Heroes (1855) | have | PG 4925, `bulfinch-age-of-fable` (2605 units) |
| The Age of Chivalry, or Legends of King Arthur (1858) | have | PG 4926, `bulfinch-age-of-chivalry` (2239 units) |
| Legends of Charlemagne, or Romance of the Middle Ages (1863) | have | PG 4927, `bulfinch-legends-of-charlemagne` (2195 units) |
| Oregon and Eldorado; or, Romance of the Rivers (1866) | have | PG 38774, `bulfinch-oregon-and-eldorado` (731 units) |
| bulfinch-combined | excluded | Bulfinch's Mythology in one file (PG 4928, 56644) and a second Age of Fable (PG 3327): the three books are held singly |
| bulfinch-gayley | excluded | The Classic Myths in English Literature (PG 46063): Charles Mills Gayley's book based on Bulfinch, not Bulfinch's text |
| bulfinch-pending | pending | Poetry of the Age of Fable (1863), Shakespeare Adapted for Reading Classes (1865), The Boy Inventor (1860) — Internet Archive scans not yet checked |


## Howard Pyle

Shelf: `pipeline/pyle_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The books Pyle wrote; books by others that he only illustrated are excluded. The four King Arthur books nest Book > Part > Chapter. They are converted by `pipeline/convert_nested.py`, which cites the whole path (`The Book of Three Worthies / PART II ... / Chapter First, par. 3`), with 0 duplicate unit ids (The Champions of the Round Table alone had 990 `~n` suffixes before). Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Merry Adventures of Robin Hood (1883) | have | PG 964, `pyle-robin-hood` (1699 units) |
| Pepper & Salt, or Seasoning for Young Folk (1886) | have | PG 15664, `pyle-pepper-and-salt` (866 units) |
| The Wonder Clock (1888), verses by Katharine Pyle | have | PG 63383, `pyle-wonder-clock` (2167 units) |
| Otto of the Silver Hand (1888) | have | PG 2865, `pyle-otto-of-the-silver-hand` (561 units) |
| Within the Capes (1885) | have | PG 48458, `pyle-within-the-capes` (1471 units) |
| The Rose of Paradise (1888) | have | PG 31673, `pyle-rose-of-paradise` (648 units) |
| Men of Iron (1891) | have | PG 1557, `pyle-men-of-iron` (1213 units) |
| A Modern Aladdin (1892) | have | PG 48444, `pyle-modern-aladdin` (957 units) |
| Twilight Land (1895) | have | PG 47564, `pyle-twilight-land` (1887 units) |
| The Story of Jack Ballister's Fortunes (1895) | have | PG 49985, `pyle-jack-ballister` (2155 units) |
| The Price of Blood (1899) | have | PG 48521, `pyle-price-of-blood` (185 units) |
| Rejected of Men: A Story of To-day (1903) | have | PG 46841, `pyle-rejected-of-men` (1101 units) |
| The Story of King Arthur and His Knights (1903) | have | PG 60184, `pyle-king-arthur` (1799 units) |
| The Story of the Champions of the Round Table (1905) | have | PG 10745, `pyle-champions-round-table` (1657 units) |
| The Story of Sir Launcelot and His Companions (1907) | have | PG 33702, `pyle-sir-launcelot` (2187 units) |
| The Story of the Grail and the Passing of Arthur (1910) | have | PG 60405, `pyle-grail-passing-of-arthur` (1810 units) |
| The Ruby of Kishmoor (1908) | have | PG 3687, `pyle-ruby-of-kishmoor` (157 units) |
| Stolen Treasure (1907) | have | PG 10394, `pyle-stolen-treasure` (688 units) |
| Howard Pyle's Book of Pirates (1921, compiled by Merle Johnson) | have | PG 973, `pyle-book-of-pirates` (1044 units) |
| The Garden Behind the Moon (1895) | have-raw | IA `gardenbehindmoo00pylegoog`, `pyle-garden-behind-the-moon` |
| pyle-duplicates | excluded | Robin Hood PG 10148, Twilight Land PG 1751, Book of Pirates PG 26862: second transcriptions |
| pyle-illustrator-only | excluded | books by others that Pyle illustrated: Dulcibel (Peterson), Grandmother's Story and The One Hoss Shay (Holmes), Chivalry (Cabell), The Island of Enchantment (Forman), Captain Ravenshaw (Stephens), Sir Christopher (Goodwin), A Story of the Golden Age (Baldwin), Hugh Wynne (Mitchell) and others |
| pyle-edited | excluded | The Buccaneers and Marooners of America (PG 73564): Exquemelin and Johnson's texts, Pyle as editor |
| pyle-not-pyle | excluded | That Marvel — The Movie (PG 66368): by Edward S. Van Zile; the catalogue match is a false hit |
| pyle-pending | pending | Yankee Doodle (1881), The Story of the Revolution (Pyle's Book of the American Spirit, 1923 compilation), the magazine stories never collected |

## Lewis Carroll

Shelf: `pipeline/carroll_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The two Alices, with the 1864 manuscript (Under Ground) and the Nursery Alice as separate works; both Sylvie and Bruno books (Furniss edition); the verse; A Tangled Tale; and the logic books. The Alices cite by chapter; Symbolic Logic and The Game of Logic cite by their nested Book > Chapter > Section path (convert_nested.py); A Tangled Tale by Knot. Three mathematical works have no Gutenberg plain text and are pending. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Alice's Adventures in Wonderland (1865) | have | PG 11, `carroll-alice-wonderland` (805 units) |
| Through the Looking-Glass, and What Alice Found There (1871) | have | PG 12, `carroll-looking-glass` (975 units) |
| The Hunting of the Snark: An Agony in Eight Fits (1876) | have | PG 13, `carroll-hunting-of-the-snark` (168 units) |
| Sylvie and Bruno (1889), ill. Harry Furniss | have | PG 48630, `carroll-sylvie-and-bruno` (1942 units) |
| Sylvie and Bruno Concluded (1893), ill. Harry Furniss | have | PG 48795, `carroll-sylvie-and-bruno-concluded` (2028 units) |
| Phantasmagoria and Other Poems (1869) | have | PG 651, `carroll-phantasmagoria` (527 units) |
| Rhyme? and Reason? (1883) | have | PG 33582, `carroll-rhyme-and-reason` (723 units) |
| Three Sunsets and Other Poems (1898) | have | PG 35497, `carroll-three-sunsets` (259 units) |
| A Tangled Tale (1885) | have | PG 29042, `carroll-tangled-tale` (736 units) |
| Alice's Adventures Under Ground (1864 manuscript, facsimile 1886) | have | PG 19002, `carroll-alice-under-ground` (396 units) |
| The Nursery "Alice" (1890) | have | PG 55040, `carroll-nursery-alice` (270 units) |
| The Game of Logic (1886) | have | PG 4763, `carroll-game-of-logic` (801 units) |
| Symbolic Logic, Part I (1896) | have | PG 28696, `carroll-symbolic-logic` (3751 units) |
| Feeding the Mind (1884 lecture, printed 1907) | have | PG 35535, `carroll-feeding-the-mind` (59 units) |
| Eight or Nine Wise Words about Letter-Writing (1890) | have | PG 38065, `carroll-letter-writing` (106 units) |
| Further Nonsense Verse and Prose (1926), ed. Langford Reed | have | PG 77627, `carroll-further-nonsense` (584 units) |
| carroll-duplicates | excluded | Sylvie and Bruno unillustrated (PG 620; the Furniss edition 48630 is held, to match Concluded), Alice HTML edition (928), Alice ill. Gordon Robinson (19033) and ill. Rackham (28885), Snark ill. Holiday (29888): texts held |
| carroll-not-his | excluded | Alice retold in words of one syllable by Mrs. Gorham (19551), Gerstenberg's stage dramatization (35688), Broadwood's song settings (36308), Widger's index of the Gutenberg files (59111) |
| carroll-translations | excluded | Esperanto, German, Italian, Finnish and French translations of Alice (17482, 19778, 28371, 46569, 55456): this shelf is Carroll's English |
| carroll-no-plain-text | pending | PENDING, no Gutenberg plain-text file, so fetch_shelf.py cannot take them: Condensation of Determinants (PG 37354, PDF and LaTeX only), Curiosa Mathematica Parts I and II (PG 78586, 79080, HTML zip only). Mathematics typeset as formulae; needs its own converter if wanted |

## Rudyard Kipling (Jungle Books, Just So, Puck)

Shelf: `pipeline/kipling_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The five children's books the relay named. Kipling sets each Jungle Book story's title twice, once over its verse epigraph and again over the story; the shelf row's `repeat_continues` option keeps that one section, with the paragraph count running on. His other books are pending for Adam to decide. US status only: Kipling died in 1936. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Jungle Book (1894) | have | PG 35997, `kipling-jungle-book` (1072 units) |
| The Second Jungle Book (1895) | have | PG 37364, `kipling-second-jungle-book` (1168 units) |
| Just So Stories (1902) | have | PG 32488, `kipling-just-so-stories` (839 units) |
| Puck of Pook's Hill (1906) | have | PG 15976, `kipling-puck-of-pooks-hill` (1480 units) |
| Rewards and Fairies (1910) | have | PG 32772, `kipling-rewards-and-fairies` (1892 units) |
| kipling-duplicates | excluded | other Gutenberg transcriptions of the same books: Jungle Book (PG 236), Second Jungle Book (1937), Just So Stories (2781), Puck of Pook's Hill (557, 26027), Rewards and Fairies (556): texts held |
| kipling-not-this-shelf | pending | PENDING, outside the relay's list unless Adam widens it: Kim (PG 35555/2226), Captains Courageous (2186/2225), Stalky & Co. (3006), Land and Sea Tales (63619), The Day's Work (2569), Plain Tales from the Hills (1858), Soldiers Three (6120), Life's Handicap (5777), Many Inventions (78240), Traffics and Discoveries (9790), Actions and Reactions (2381), A Diversity of Creatures (13085), Debits and Credits (71002), The Light That Failed (2876), the verse (Departmental Ditties and Barrack-Room Ballads 7846, The Seven Seas 27870, The Five Nations 60260-60261, The Years Between 21777, Songs from Books 15529), travel and war writing (American Notes, From Sea to Sea, Letters of Travel, Sea Warfare, The Irish Guards in the Great War, and others) |
| kipling-not-his | excluded | anthologies with other authors (PG 2035, 2038, 12732, 15466, 21964, 62942, 60482, 30568), selections from his books (16578, 28537, 8649, 2334, 8147, 2163), Widger's index (57538) |
| kipling-translations | excluded | Finnish, French, Esperanto and Spanish translations: this shelf is Kipling's English |

## Robert Louis Stevenson

Shelf: `pipeline/stevenson_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). 45 books, one Gutenberg text each: novels, tales, verse, travel, essays, histories, prayers, letters, and the collaborations (partner named in the title). Treasure Island is already held through fetch_sources.py and is cross-referenced, not refetched. Per-book rules: essay collections cite essay / numbered section (`sub` option); the Colvin Letters cite by recipient plus the place-and-date line (Colvin did not number them; 38 letters sharing recipient and date line still take `~n`); the Henley plays cite play / act / tableau or scene. The 23-volume Swanston Edition is pending as a possible second witness. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Strange Case of Dr Jekyll and Mr Hyde (1886) | have | PG 43, `stevenson-dr-jekyll-and-mr-hyde` (330 units) |
| Kidnapped (1886) | have | PG 421, `stevenson-kidnapped` (1515 units) |
| Catriona (1893; in the US, David Balfour) | have | PG 589, `stevenson-catriona` (1918 units) |
| The Black Arrow: A Tale of the Two Roses (1888) | have | PG 848, `stevenson-black-arrow` (1939 units) |
| The Master of Ballantrae (1889) | have | PG 864, `stevenson-master-of-ballantrae` (1268 units) |
| Prince Otto (1885) | have | PG 372, `stevenson-prince-otto` (1290 units) |
| St. Ives (1897; finished by Arthur Quiller-Couch) | have | PG 322, `stevenson-st-ives` (1734 units) |
| Weir of Hermiston: An Unfinished Romance (1896) | have | PG 380, `stevenson-weir-of-hermiston` (682 units) |
| New Arabian Nights (1882) | have | PG 839, `stevenson-new-arabian-nights` (1989 units) |
| More New Arabian Nights: The Dynamiter (1885), with Fanny Van de Grift Stevenson | have | PG 647, `stevenson-dynamiter` (1071 units) |
| The Merry Men, and Other Tales and Fables (1887) | have | PG 344, `stevenson-merry-men` (990 units) |
| Island Nights' Entertainments (1893) | have | PG 329, `stevenson-island-nights-entertainments` (863 units) |
| Tales and Fantasies (1905) | have | PG 426, `stevenson-tales-and-fantasies` (917 units) |
| Fables (1896) | have | PG 343, `stevenson-fables` (420 units) |
| The Waif Woman (1916) | have | PG 19750, `stevenson-waif-woman` (141 units) |
| The Wrong Box (1889), with Lloyd Osbourne | have | PG 1585, `stevenson-wrong-box` (1318 units) |
| The Wrecker (1892), with Lloyd Osbourne | have | PG 1024, `stevenson-wrecker` (2221 units) |
| The Ebb-Tide (1894), with Lloyd Osbourne | have | PG 1604, `stevenson-ebb-tide` (1084 units) |
| The Plays of W. E. Henley and R. L. Stevenson (Deacon Brodie, Beau Austin, Admiral Guinea, Macaire) | have | PG 719, `stevenson-plays` (2567 units) |
| A Child's Garden of Verses (1885) | have | PG 136, `stevenson-childs-garden-of-verses` (283 units) |
| Underwoods (1887) | have | PG 438, `stevenson-underwoods` (291 units) |
| Ballads (1890) | have | PG 413, `stevenson-ballads` (170 units) |
| Songs of Travel, and Other Verses (1896), ed. Sidney Colvin | have | PG 487, `stevenson-songs-of-travel` (183 units) |
| New Poems, and Variant Readings (1918) | have | PG 441, `stevenson-new-poems` (460 units) |
| Moral Emblems and other Davos booklets (1881-82) | have | PG 772, `stevenson-moral-emblems` (137 units) |
| Prayers Written at Vailima, and A Lowden Sabbath Morn | have | PG 616, `stevenson-prayers-at-vailima` (90 units) |
| An Inland Voyage (1878) | have | PG 534, `stevenson-inland-voyage` (323 units) |
| Travels with a Donkey in the Cevennes (1879) | have | PG 535, `stevenson-travels-with-a-donkey` (342 units) |
| The Silverado Squatters (1883) | have | PG 516, `stevenson-silverado-squatters` (238 units) |
| Edinburgh: Picturesque Notes (1878) | have | PG 382, `stevenson-edinburgh-picturesque-notes` (104 units) |
| In the South Seas (1896) | have | PG 464, `stevenson-in-the-south-seas` (464 units) |
| Essays of Travel (1905) | have | PG 627, `stevenson-essays-of-travel` (393 units) |
| Across the Plains, with Other Memories and Essays (1892) | have | PG 614, `stevenson-across-the-plains` (322 units) |
| Virginibus Puerisque, and Other Papers (1881) | have | PG 386, `stevenson-virginibus-puerisque` (184 units) |
| Familiar Studies of Men and Books (1882) | have | PG 425, `stevenson-familiar-studies` (461 units) |
| Memories and Portraits (1887) | have | PG 381, `stevenson-memories-and-portraits` (200 units) |
| Essays in the Art of Writing (1905) | have | PG 492, `stevenson-essays-in-the-art-of-writing` (146 units) |
| Lay Morals, and Other Papers (1911) | have | PG 373, `stevenson-lay-morals` (773 units) |
| Father Damien: An Open Letter to the Reverend Dr. Hyde of Honolulu (1890) | have | PG 281, `stevenson-father-damien` (47 units) |
| A Footnote to History: Eight Years of Trouble in Samoa (1892) | have | PG 536, `stevenson-footnote-to-history` (221 units) |
| Records of a Family of Engineers (1912) | have | PG 280, `stevenson-records-of-a-family-of-engineers` (494 units) |
| Memoir of Fleeming Jenkin (1887) | have | PG 698, `stevenson-memoir-of-fleeming-jenkin` (393 units) |
| Vailima Letters (1895), to Sidney Colvin | have | PG 387, `stevenson-vailima-letters` (955 units) |
| The Letters of Robert Louis Stevenson, Volume 1 (1899), ed. Sidney Colvin | have | PG 622, `stevenson-letters-1` (1601 units) |
| The Letters of Robert Louis Stevenson, Volume 2 (1899), ed. Sidney Colvin | have | PG 637, `stevenson-letters-2` (1302 units) |
| stevenson-treasure-island | excluded | HELD elsewhere: Treasure Island is fetch_sources.py's `treasure_island` (PG 120); Winter's illustrated text (27780) is a duplicate |
| stevenson-duplicates | excluded | other transcriptions of books held: Jekyll and Hyde (PG 42), David Balfour (14133, the US title of Catriona), Kidnapped ill. Wyeth (56562), Black Arrow ill. Wyeth (32954), A Child's Garden of Verses in seven illustrated editions (19722, 25608-25611, 25617, 28722), A Lowden Sabbath Morn (35546, also in Prayers at Vailima), A Christmas Sermon (14535, in Across the Plains), The Sea Fogs (5272, a chapter of Silverado) |
| stevenson-swanston | pending | the Swanston Edition (23 volumes on Gutenberg, 21686 and 30393-31916), with Andrew Lang's introduction. Its texts duplicate the single books held here; it would be a second witness, for Adam to decide |
| stevenson-selections | excluded | selections from his works: The Pocket R.L.S. (2537), Essays ed. Phelps (10761), An Apology for Idlers and other essays (69825) |
| stevenson-not-his | excluded | anthologies with other authors (PG 2038, 2071, 2359, 2588, 10135, 12732, 21964, 59813), books about him (15547, 53165, 79196), Porto Bello Gold by A. D. H. Smith (70777), Widger's index (58181) |
| stevenson-translations | excluded | non-English editions: this shelf is Stevenson's English |

## G. K. Chesterton (the 1926-1928 gaps)

Shelf: `pipeline/chesterton-gaps_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The five books fetch_sources.py deferred because neither CCEL nor Gutenberg has them, now held as raw Internet Archive OCR. The other 61 Chesterton works are already held through fetch_sources.py and are not refetched. Generally Speaking is the 1929 Dodd, Mead first American printing (copyright 1929), which is US public domain now; the relay's pre-1929 limit is read as first publication (London, 1928). The 1929-1930 books are listed as pending. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Incredulity of Father Brown (1926; New York: Dodd, Mead, 1926) | have-raw | IA `incredulityoffat0000ches`, `chesterton-incredulity-of-father-brown` |
| The Outline of Sanity (1926; New York: Dodd, Mead, 1927) | have-raw | IA `outlineofsanity0000ches`, `chesterton-outline-of-sanity` |
| The Return of Don Quixote (1927; New York: Dodd, Mead, 1927) | have-raw | IA `returnofdonquixo0000ches_i3m2`, `chesterton-return-of-don-quixote` |
| Robert Louis Stevenson (1927; London: Hodder and Stoughton, 1927) | have-raw | IA `robertlouissteve0000ches`, `chesterton-robert-louis-stevenson` |
| Generally Speaking: A Book of Essays (1928; New York: Dodd, Mead, 1929) | have-raw | IA `generallyspeakin00ches`, `chesterton-generally-speaking` |
| chesterton-held | excluded | HELD elsewhere: the 61 works in pipeline/fetch_sources.py (CHESTERTON_CCEL and the Gutenberg Chesterton entries); not refetched |
| chesterton-1929-1930 | pending | PENDING, outside the relay's pre-1929 limit though US public domain since 2025-2026: The Thing (1929), The Poet and the Lunatics (1929), Four Faultless Felons (1930), The Resurrection of Rome (1930), Come to Think of It (1930) |
| chesterton-not-pd | excluded | 1931 and later (Autobiography, The Well and the Shallows, Chaucer, The Scandal of Father Brown, St. Thomas Aquinas and the rest): not yet US public domain |
| chesterton-other-scans | excluded | other scans of the same books (DLI copies 404 on the text file; later reprints of 1937 and 1953; the 1906 Robert Louis Stevenson booklet with W. Robertson Nicoll is a different work) |

## Aesop (Townsend and Jacobs)

Shelf: `pipeline/aesop_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The two English versions the relay named, each its own work: Townsend's literal translation (1867) and Jacobs's retelling (1894). Both cite by fable title, read from each book's own Contents. Townsend gives ten fables a title another fable already has (two called The Two Frogs, for instance) and numbers none of them, so the second of each pair cites with `~2`. Other English versions are listed as pending. Earlier house fables work was not found in this repo (see Fables below). Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Aesop's Fables, tr. George Fyler Townsend (1867) | have | PG 21, `aesop-townsend` (503 units) |
| The Fables of Aesop, selected, told anew and their history traced by Joseph Jacobs (1894) | have | PG 28, `aesop-jacobs` (265 units) |
| aesop-other-versions | pending | PENDING, outside the relay's two translations unless Adam widens it: V. S. Vernon Jones's translation with G. K. Chesterton's introduction and Rackham's pictures (PG 11339, 1912), Croxall (39187), L'Estrange's Fables of Aesop and other mythologists (79038), Bewick's editions (60004, 60874), the 1884 Revised Version (18732), Alfred Caldecott (34588), and the children's versions (Winter 19994, Stickney 49010, C. Robinson 53103, Park's rhymes 21189, Crane's Baby's Own Aesop 25433, Aikin's one-syllable version 76243) |
| aesop-translations | excluded | Finnish (PG 74326): this shelf is English |
| aesop-stevenson | excluded | Stevenson's own Fables (1896) are his, not Aesop's: held on the stevenson shelf |

## E. Nesbit

Shelf: `pipeline/nesbit_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). 33 Gutenberg books: the Bastable and Psammead series, The Railway Children, the Arden books and later fantasies, the dragon and fairy collections, her Shakespeare retellings and Royal Children, and the adult novels, stories and verse; plus her first book of verse, Lays and Legends (1886), as raw Internet Archive OCR. Most chapters are read from the book's own Contents (16 books use the lenient reader). The remaining duplicate ids sit in publishers' back-matter (book lists, THE END), not in her text. Illustrated duplicate transcriptions are excluded. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Story of the Treasure Seekers (1899) | have | PG 770, `nesbit-story-of-the-treasure-seekers` (1245 units) |
| The Wouldbegoods (1901) | have | PG 794, `nesbit-wouldbegoods` (2065 units) |
| The New Treasure Seekers (1904) | have | PG 25496, `nesbit-new-treasure-seekers` (1919 units) |
| Oswald Bastable and Others (1905) | have | PG 28804, `nesbit-oswald-bastable-and-others` (2294 units) |
| Five Children and It (1902) | have | PG 778, `nesbit-five-children-and-it` (1404 units) |
| The Phoenix and the Carpet (1904) | have | PG 836, `nesbit-phoenix-and-the-carpet` (1945 units) |
| The Story of the Amulet (1906) | have | PG 837, `nesbit-story-of-the-amulet` (2394 units) |
| The Railway Children (1906) | have | PG 1874, `nesbit-railway-children` (2149 units) |
| The Enchanted Castle (1907) | have | PG 3536, `nesbit-enchanted-castle` (2271 units) |
| The House of Arden (1908) | have | PG 57799, `nesbit-house-of-arden` (2089 units) |
| Harding's Luck (1909) | have | PG 28725, `nesbit-hardings-luck` (1959 units) |
| The Magic City (1910) | have | PG 20606, `nesbit-magic-city` (1883 units) |
| Wet Magic (1913) | have | PG 50361, `nesbit-wet-magic` (1528 units) |
| The Wonderful Garden; or, The Three Cs (1911) | have | PG 52907, `nesbit-wonderful-garden` (2262 units) |
| The Book of Dragons (1900) | have | PG 23661, `nesbit-book-of-dragons` (1051 units) |
| Nine Unlikely Tales for Children (1901) | have | PG 49913, `nesbit-nine-unlikely-tales` (1221 units) |
| The Magic World (1912) | have | PG 27903, `nesbit-magic-world` (1844 units) |
| Beautiful Stories from Shakespeare (1907) | have | PG 1430, `nesbit-beautiful-stories-from-shakespeare` (1597 units) |
| Royal Children of English History (1897) | have | PG 30167, `nesbit-royal-children` (273 units) |
| Pussy and Doggy Tales (1899) | have | PG 27190, `nesbit-pussy-and-doggy-tales` (409 units) |
| All Round the Year (1888), verses with Caris Brooke | have | PG 20404, `nesbit-all-round-the-year` (85 units) |
| Grim Tales (1893) | have | PG 40321, `nesbit-grim-tales` (667 units) |
| The Literary Sense (1903) | have | PG 39324, `nesbit-literary-sense` (1661 units) |
| In Homespun (1896) | have | PG 4378, `nesbit-in-homespun` (814 units) |
| The Incomplete Amorist (1906) | have | PG 9385, `nesbit-incomplete-amorist` (3284 units) |
| The Incredible Honeymoon (1916) | have | PG 41354, `nesbit-incredible-honeymoon` (1704 units) |
| Man and Maid (1906) | have | PG 33028, `nesbit-man-and-maid` (1739 units) |
| The Prophet's Mantle (1885), with Hubert Bland, as Fabian Bland | have | PG 55244, `nesbit-prophets-mantle` (2340 units) |
| Wings and the Child; or, The Building of Magic Cities (1913) | have | PG 38977, `nesbit-wings-and-the-child` (316 units) |
| Lays and Legends, Second Series (1892) | have | PG 41693, `nesbit-lays-and-legends-2` (497 units) |
| Many Voices: Poems (1922) | have | PG 1924, `nesbit-many-voices` (287 units) |
| Songs of Love and Empire (1898) | have | PG 50162, `nesbit-songs-of-love-and-empire` (627 units) |
| The Rainbow and the Rose (1905) | have | PG 4513, `nesbit-rainbow-and-the-rose` (377 units) |
| Lays and Legends (1886), the first series | have-raw | IA `laysandlegends00nesbgoog`, `nesbit-lays-and-legends-1` |
| nesbit-duplicates | excluded | illustrated transcriptions of books held: Five Children and It ill. Millar (PG 17314), The Wouldbegoods ill. Birch (32466), The Enchanted Castle ill. Millar (34219) |
| nesbit-not-hers | excluded | Landscape and Song (14320), an anthology she edited; Atlantic Narratives (38172), an anthology with other authors |
| nesbit-not-on-gutenberg | pending | her other books on neither Gutenberg nor this shelf; only Lays and Legends (1886) was searched for on Internet Archive this pass |
| nesbit-other-scans | excluded | other scans of Lays and Legends 1886 (laysandlegends01nesbgoog, cu31924013437656, cu31924060442591) and of the 1892 second series (layslegends00nesbrich; the second series is held from Gutenberg) |

## Beatrix Potter

Shelf: `pipeline/potter_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The 20 little books on Gutenberg, one slug each, and The Fairy Caravan (first published in Philadelphia in 1929; US public domain since 2025). Two later little books not on Gutenberg are raw Internet Archive OCR: Pigling Bland (1913, from a 1987 reprint whose new matter is only the colour reproductions) and Little Pig Robinson (1930; US public domain since 2026). The little books have no chapters, so they cite by paragraph; Gutenberg's [Illustration] markers come through as their own units. The words only: the pictures are not in the text files. US status only: Potter died in 1943. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Tale of Peter Rabbit (1902) | have | PG 14838, `potter-peter-rabbit` (69 units) |
| The Tale of Squirrel Nutkin (1903) | have | PG 14872, `potter-squirrel-nutkin` (92 units) |
| The Tailor of Gloucester (1903) | have | PG 14868, `potter-tailor-of-gloucester` (138 units) |
| The Tale of Benjamin Bunny (1904) | have | PG 14407, `potter-benjamin-bunny` (89 units) |
| The Tale of Two Bad Mice (1904) | have | PG 45264, `potter-two-bad-mice` (72 units) |
| The Tale of Mrs. Tiggy-Winkle (1905) | have | PG 15137, `potter-mrs-tiggy-winkle` (99 units) |
| The Tale of the Pie and the Patty-Pan (1905) | have | PG 15234, `potter-pie-and-the-patty-pan` (156 units) |
| The Tale of Mr. Jeremy Fisher (1906) | have | PG 15077, `potter-mr-jeremy-fisher` (35 units) |
| The Story of a Fierce Bad Rabbit (1906) | have | PG 45265, `potter-fierce-bad-rabbit` (35 units) |
| The Story of Miss Moppet (1906) | have | PG 14848, `potter-miss-moppet` (37 units) |
| The Tale of Tom Kitten (1907) | have | PG 14837, `potter-tom-kitten` (71 units) |
| The Tale of Jemima Puddle-Duck (1908) | have | PG 14814, `potter-jemima-puddle-duck` (94 units) |
| The Tale of Samuel Whiskers; or, The Roly-Poly Pudding (1908) | have | PG 15575, `potter-samuel-whiskers` (186 units) |
| The Tale of the Flopsy Bunnies (1909) | have | PG 14220, `potter-flopsy-bunnies` (92 units) |
| The Tale of Ginger and Pickles (1909) | have | PG 14877, `potter-ginger-and-pickles` (98 units) |
| The Tale of Mrs. Tittlemouse (1910) | have | PG 17089, `potter-mrs-tittlemouse` (109 units) |
| The Tale of Timmy Tiptoes (1911) | have | PG 14797, `potter-timmy-tiptoes` (79 units) |
| The Tale of Mr. Tod (1912) | have | PG 19805, `potter-mr-tod` (218 units) |
| The Tale of Johnny Town-Mouse (1918) | have | PG 15284, `potter-johnny-town-mouse` (40 units) |
| Cecily Parsley's Nursery Rhymes (1922) | have | PG 23350, `potter-cecily-parsley` (55 units) |
| The Fairy Caravan (Philadelphia, 1929) | have | PG 78504, `potter-fairy-caravan` (473 units) |
| The Tale of Pigling Bland (1913); scan of a 1987 Warne reprint with new colour reproductions, text as 1913 | have-raw | IA `taleofpiglingbla00beat`, `potter-pigling-bland` |
| The Tale of Little Pig Robinson (1930); undated Warne printing (archive.org's 1920 date is wrong: the book first appeared in 1930) | have-raw | IA `b1111925`, `potter-little-pig-robinson` |
| potter-collections | excluded | Gutenberg's own compilations of books held singly here: The Great Big Treasury of Beatrix Potter (PG 572), A Collection of Beatrix Potter Stories (582) |
| potter-duplicates | excluded | The Tale of Peter Rabbit ill. Virginia Albert (14304, a US edition with another artist's pictures), The Tale of Mrs. Tiggy-Winkle (12103, an earlier transcription) |
| potter-not-on-gutenberg | pending | Appley Dapply's Nursery Rhymes (1917) and other later books found on neither Gutenberg nor Internet Archive in a title search |
| potter-translations | excluded | French Peter Rabbit (29052): this shelf is English |

## Kenneth Grahame

Shelf: `pipeline/grahame_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The Wind in the Willows, The Golden Age, Dream Days, Pagan Papers and The Headswoman, one clean Gutenberg text each, cited by chapter or essay. The Reluctant Dragon is held inside Dream Days, where Grahame put it. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Wind in the Willows (1908) | have | PG 289, `grahame-wind-in-the-willows` (921 units) |
| The Golden Age (1895) | have | PG 291, `grahame-golden-age` (492 units) |
| Dream Days (1898) | have | PG 270, `grahame-dream-days` (459 units) |
| Pagan Papers (1893) | have | PG 5319, `grahame-pagan-papers` (110 units) |
| The Headswoman (1898; 1921 edition ill. Marcia Lane Foster) | have | PG 34243, `grahame-headswoman` (133 units) |
| grahame-duplicates | excluded | other transcriptions of books held: The Wind in the Willows (PG 22340, 22341, 26293, 27805 ill. Bransom), The Golden Age (32501 ill. Parrish, 53250), Dream Days (1288, 35187 ill. Parrish), The Reluctant Dragon (21588, a chapter of Dream Days) |
| grahame-not-his | excluded | anthologies he edited: The Cambridge Book of Poetry for Children (50994), Eugene Field's Lullaby-Land (54874) |

## J. M. Barrie

Shelf: `pipeline/barrie_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). 26 books published before 1930: Peter and Wendy, the Peter Pan play as printed in 1928, Peter Pan in Kensington Gardens and The Little White Bird it came from; the Thrums books and Tommy novels; sketches and addresses; and the plays, which cite by act. US status only: Barrie died in 1937, and the UK grants Great Ormond Street Hospital a perpetual royalty right in Peter Pan. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Peter and Wendy (1911), the Peter Pan novel | have | PG 16, `barrie-peter-and-wendy` (1658 units) |
| Peter Pan; or, The Boy Who Would Not Grow Up (play, first printed New York 1928) | have | PG 78131, `barrie-peter-pan-play` (1119 units) |
| Peter Pan in Kensington Gardens (1906) | have | PG 1332, `barrie-peter-pan-in-kensington-gardens` (207 units) |
| The Little White Bird; or, Adventures in Kensington Gardens (1902) | have | PG 1376, `barrie-little-white-bird` (1156 units) |
| Auld Licht Idylls (1888) | have | PG 8590, `barrie-auld-licht-idylls` (482 units) |
| A Window in Thrums (1889) | have | PG 20914, `barrie-window-in-thrums` (1042 units) |
| The Little Minister (1891) | have | PG 5093, `barrie-little-minister` (3291 units) |
| Sentimental Tommy (1896) | have | PG 14961, `barrie-sentimental-tommy` (2406 units) |
| Tommy and Grizel (1900) | have | PG 11901, `barrie-tommy-and-grizel` (2870 units) |
| Margaret Ogilvy (1896) | have | PG 342, `barrie-margaret-ogilvy` (491 units) |
| Better Dead (1887) | have | PG 20807, `barrie-better-dead` (776 units) |
| When a Man's Single (1888) | have | PG 41031, `barrie-when-a-mans-single` (1932 units) |
| My Lady Nicotine (1890) | have | PG 18934, `barrie-my-lady-nicotine` (529 units) |
| An Edinburgh Eleven (1889) | have | PG 39203, `barrie-edinburgh-eleven` (129 units) |
| A Holiday in Bed, and Other Sketches (1892) | have | PG 39543, `barrie-holiday-in-bed` (348 units) |
| Quality Street (play, 1901; printed 1913) | have | PG 31266, `barrie-quality-street` (1200 units) |
| The Admirable Crichton (play, 1902; printed 1914) | have | PG 3490, `barrie-admirable-crichton` (1318 units) |
| Alice Sit-by-the-Fire (play, 1905) | have | PG 6965, `barrie-alice-sit-by-the-fire` (1266 units) |
| What Every Woman Knows (play, 1908) | have | PG 5654, `barrie-what-every-woman-knows` (1485 units) |
| Der Tag; or, The Tragic Man (play, 1914) | have | PG 39178, `barrie-der-tag` (137 units) |
| Echoes of the War (four plays, 1918) | have | PG 9617, `barrie-echoes-of-the-war` (1502 units) |
| Dear Brutus (play, 1917) | have | PG 4021, `barrie-dear-brutus` (1184 units) |
| A Kiss for Cinderella (play, 1916; printed 1920) | have | PG 69817, `barrie-kiss-for-cinderella` (1218 units) |
| Mary Rose (play, 1920; printed 1924) | have | PG 71067, `barrie-mary-rose` (1198 units) |
| Courage (rectorial address, St Andrews, 1922) | have | PG 10767, `barrie-courage` (61 units) |
| Neither Dorking nor the Abbey (1911), on George Meredith | have | PG 40894, `barrie-neither-dorking-nor-the-abbey` (20 units) |
| barrie-duplicates | excluded | other transcriptions of books held: Peter and Wendy ill. F. D. Bedford (PG 26654), Peter Pan in Kensington Gardens ill. Rackham (26998, 26999), Auld Licht Idyls (20918), The Little Minister ill. Gilbert (33901), The Admirable Crichton ed. Temi Rose (51566, a modern edition with new editorial matter); PG 22984 is an audio recording, not a text; The Old Lady Shows Her Medals (PG 70315) is the Kirriemuir Edition volume of all four Echoes of the War plays, held as 9617 |
| barrie-not-his | excluded | anthologies and books by others he contributed to or introduced (PG 2135, 2588, 21415 Daisy Ashford's Young Visiters, 26146, 37970, 39755 O'Connor's retelling, 43084 Mrs. Oliphant, 62942), Widger's index (58824) |
| barrie-not-on-gutenberg | pending | his books not on Gutenberg (for example The Boy Castaways, Shall We Join the Ladies?); not searched for this pass |

## L. Frank Baum (the Oz books)

Shelf: `pipeline/baum_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Baum's fourteen Oz novels and Little Wizard Stories of Oz, cited by chapter. The Gutenberg transcriptions mark chapters in four different ways, so each book has its own rule in its shelf row. The Marvelous Land of Oz has none in a form a rule can catch, so its 24 chapter titles are listed, and 21 are found. His other books are pending; the Thompson and Snow continuations are not his. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Wonderful Wizard of Oz (1900) | have | PG 55, `baum-wonderful-wizard-of-oz` (1116 units) |
| The Marvelous Land of Oz (1904) | have | PG 54, `baum-marvelous-land-of-oz` (1550 units) |
| Ozma of Oz (1907) | have | PG 486, `baum-ozma-of-oz` (1235 units) |
| Dorothy and the Wizard in Oz (1908) | have | PG 420, `baum-dorothy-and-the-wizard-in-oz` (1308 units) |
| The Road to Oz (1909) | have | PG 485, `baum-road-to-oz` (1249 units) |
| The Emerald City of Oz (1910) | have | PG 517, `baum-emerald-city-of-oz` (1742 units) |
| The Patchwork Girl of Oz (1913) | have | PG 955, `baum-patchwork-girl-of-oz` (1807 units) |
| Little Wizard Stories of Oz (1914), ill. John R. Neill | have | PG 25519, `baum-little-wizard-stories-of-oz` (358 units) |
| Tik-Tok of Oz (1914) | have | PG 956, `baum-tik-tok-of-oz` (1497 units) |
| The Scarecrow of Oz (1915) | have | PG 957, `baum-scarecrow-of-oz` (1250 units) |
| Rinkitink in Oz (1916) | have | PG 958, `baum-rinkitink-in-oz` (1097 units) |
| The Lost Princess of Oz (1917) | have | PG 959, `baum-lost-princess-of-oz` (1150 units) |
| The Tin Woodman of Oz (1918) | have | PG 960, `baum-tin-woodman-of-oz` (1161 units) |
| The Magic of Oz (1919) | have | PG 419, `baum-magic-of-oz` (1138 units) |
| Glinda of Oz (1920) | have | PG 961, `baum-glinda-of-oz` (1005 units) |
| baum-duplicates | excluded | other Gutenberg transcriptions of every Oz book held (illustrated Neill and Denslow editions and re-transcriptions: PG 17426, 19466, 53844, 43936, 21179, 23075, 33361, 19450, 22566, 21174, 26624, 21163, 41667, 32094, 23076, 52176, 51263, 25581, 21169, 24459, 30852, 50194, 39868); PG 19467 (Little Wizard Stories) has no plain-text file, so the Neill transcription 25519 is held |
| baum-not-this-shelf | pending | PENDING, outside the relay's Oz list unless Adam widens it: his other fantasies (The Master Key, The Enchanted Island of Yew, Queen Zixi of Ix, John Dough and the Cherub, The Sea Fairies, Sky Island, Mother Goose in Prose, American Fairy Tales, The Magical Monarch of Mo, Dot and Tot of Merryland, the Santa Claus books, the Twinkle Tales, The Woggle-Bug Book), and the series and adult books (Aunt Jane's Nieces, Mary Louise, the Boy Fortune Hunters, Sam Steele, The Flying Girl, Daring Twins, The Fate of a Crown, The Last Egyptian, Tamawaca Folks, Annabel, Daughters of Destiny, the Hamburgs and window-dressing manuals) |
| baum-not-his | excluded | the Oz books by Ruth Plumly Thompson and Jack Snow (PG 30537, 53765, 55806, 55851, 56073, 56079, 56085, 56555, 56683, 58765, 61681, 65849, 70152, 71273, 73170, 75720, 78637). The Royal Book of Oz (1921, PG 30537) was published under Baum's name but written by Thompson; listed here, not held |
| baum-translations | excluded | non-English editions: this shelf is Baum's English |

## John Ruskin (The King of the Golden River)

Shelf: `pipeline/ruskin-golden-river_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Ruskin's one fairy tale, from Ginn's 1885 Boston edition with Richard Doyle's pictures, cited by chapter. The Contents and the list of illustrations are kept as their own sections so the tale's chapter ids are unique. Ginn's publisher advertisements at the end come through as units. Only this book, as the relay asked. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The King of the Golden River; or, The Black Brothers: A Legend of Stiria (1851); Boston: Ginn, 1885, with Richard Doyle's pictures | have | PG 33673, `ruskin-king-of-the-golden-river` (248 units) |
| ruskin-duplicates | excluded | The King of the Golden River (PG 701), another transcription of the same text |
| ruskin-not-this-shelf | excluded | his other works (Modern Painters, The Stones of Venice, Sesame and Lilies and the rest): outside the storytellers shelf |

## Oscar Wilde (the fairy tales)

Shelf: `pipeline/wilde-fairy-tales_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The Happy Prince and Other Tales and A House of Pomegranates: all nine tales, each cited by its title. Only these two books, as the relay asked. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Happy Prince, and Other Tales (1888) | have | PG 902, `wilde-happy-prince` (428 units) |
| A House of Pomegranates (1891) | have | PG 873, `wilde-house-of-pomegranates` (578 units) |
| wilde-duplicates | excluded | other transcriptions of The Happy Prince (PG 23937, 30120 ill. Charles Robinson) |
| wilde-not-this-shelf | excluded | his plays, The Picture of Dorian Gray, the poems, essays and Lord Arthur Savile's Crime: outside the storytellers shelf unless Adam widens it |

## Charles Dickens (the Christmas books)

Shelf: `pipeline/dickens-christmas_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The five Christmas books, each cited by Dickens's own divisions: staves (Carol), quarters (Chimes), chirps (Cricket), parts (Battle of Life) and the three Gifts (Haunted Man). His novels are on other shelves. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| A Christmas Carol in Prose; Being a Ghost Story of Christmas (1843) | have | PG 46, `dickens-christmas-carol` (717 units) |
| The Chimes: A Goblin Story of Some Bells that Rang an Old Year Out and a New Year In (1844) | have | PG 653, `dickens-chimes` (690 units) |
| The Cricket on the Hearth: A Fairy Tale of Home (1845) | have | PG 678, `dickens-cricket-on-the-hearth` (717 units) |
| The Battle of Life: A Love Story (1846) | have | PG 676, `dickens-battle-of-life` (720 units) |
| The Haunted Man and the Ghost's Bargain: A Fancy for Christmas-Time (1848) | have | PG 644, `dickens-haunted-man` (845 units) |
| dickens-duplicates | excluded | other transcriptions of the five books: A Christmas Carol (PG 9696, 19337, 19505, 20673, 24022 ill. Rackham, 30368 the manuscript facsimile), The Chimes (9738), The Cricket on the Hearth (9739, 20795, 37581), The Battle of Life (9694, 40723), The Haunted Man (9713) |
| dickens-not-his | excluded | stage adaptations by others: C. A. Scott's Old Scrooge (40729), C. Z. Barnett's The Miser's Warning (41739) |
| dickens-not-this-shelf | excluded | his Christmas stories written for Household Words and All the Year Round, and his novels: outside the relay's five Christmas books |

## Carlo Collodi (Pinocchio)

Shelf: `pipeline/collodi_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Two public-domain English Pinocchios, one slug each with the translator in the title: Della Chiesa (1914), clean and cited by chapter, and Murray (1892), the first English translation, as raw OCR. A 1916 Whitman edition that names no translator is held back until someone identifies the translator. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Adventures of Pinocchio, tr. Carol Della Chiesa (1914) | have | PG 500, `collodi-pinocchio-della-chiesa` (1757 units) |
| The Story of a Puppet; or, The Adventures of Pinocchio, tr. M. A. Murray (London: T. Fisher Unwin, 1892) | have-raw | IA `storyofpuppetora00colliala`, `collodi-pinocchio-murray` |
| collodi-duplicates | excluded | The Adventures of Pinocchio (PG 19516, Della Chiesa again) |
| collodi-translator-unrecorded | pending | Pinocchio: The Tale of a Puppet (PG 16865, Whitman 1916, ill. Alice Carsey) names no translator; it does not enter the shelf until the translator is identified (the 2026-07-26 rights rule) |
| collodi-not-pinocchio | excluded | Beppo, tr. W. S. Cramp (PG 78089): not Pinocchio, outside the relay's ask; The Heart of Pinocchio (41446) is by Collodi Nipote, not Collodi |
| collodi-translations | excluded | Italian originals (19517, 52484) and the Finnish translation (53077): this shelf is English |

## Hugh Lofting (before 1929)

Shelf: `pipeline/lofting_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The Doctor Dolittle books of 1920-1928 that Gutenberg has, The Story of Mrs Tubbs and Porridge Poetry, cited by chapter or poem, plus Doctor Dolittle's Caravan as raw OCR of its 1926 first printing. Circus, Zoo and Garden are pending: the only scans found are later printings that carry new, non-public-domain front matter. These are Lofting's original texts, including the passages his publishers revised in 1988 for their racist caricature. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Story of Doctor Dolittle (1920), with Hugh Walpole's introduction | have | PG 501, `lofting-story-of-doctor-dolittle` (815 units) |
| The Voyages of Doctor Dolittle (1922) | have | PG 1154, `lofting-voyages-of-doctor-dolittle` (1743 units) |
| Doctor Dolittle's Post Office (1923) | have | PG 58947, `lofting-doctor-dolittles-post-office` (1600 units) |
| The Story of Mrs Tubbs (1923) | have | PG 64225, `lofting-story-of-mrs-tubbs` (121 units) |
| Porridge Poetry (1924) | have | PG 75663, `lofting-porridge-poetry` (112 units) |
| Doctor Dolittle in the Moon (1928) | have | PG 73411, `lofting-doctor-dolittle-in-the-moon` (695 units) |
| Doctor Dolittle's Caravan (New York: Frederick A. Stokes, October 1926, first printing) | have-raw | IA `bwb_Y0-DVO-085`, `lofting-doctor-dolittles-caravan` |
| lofting-duplicates | excluded | The Story of Doctor Dolittle (PG 26201), another transcription |
| lofting-later-printings-only | pending | Doctor Dolittle's Circus (1924), Doctor Dolittle's Zoo (1925) and Doctor Dolittle's Garden (1927). The Internet Archive scans found are later printings (1950s-1960s, with renewal notices and new front matter about Lofting that is not itself public domain); a first-printing scan should be found before they enter the shelf |
| lofting-1929-and-later | excluded | outside the relay's pre-1929 line: Noisy Nora (1929), The Twilight of Magic (1930), Gub Gub's Book (1932) and the later Dolittle books |

## Joseph Jacobs (the fairy-tale collections)

Shelf: `pipeline/jacobs-fairy_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Jacobs compiled and retold these tales in his own English, so no translator is owed. English Fairy Tales is cut by a title list read from its run-on Contents (the house rule would split Mr Fox at its refrain); More English Fairy Tales by its own Contents. Europa's Fairy Book (1916) is added from the same hand; Celtic Folk and Fairy Tales (PG 35862) is held back as a probable retitling of Celtic Fairy Tales. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| English Fairy Tales (1890) | have | PG 7439, `jacobs-english-fairy-tales` (1259 units) |
| More English Fairy Tales (1894) | have | PG 14241, `jacobs-more-english-fairy-tales` (1331 units) |
| Celtic Fairy Tales (1892) | have | PG 7885, `jacobs-celtic-fairy-tales` (1529 units) |
| More Celtic Fairy Tales (1894) | have | PG 34453, `jacobs-more-celtic-fairy-tales` (1491 units) |
| Indian Fairy Tales (1892) | have | PG 7128, `jacobs-indian-fairy-tales` (1221 units) |
| Europa's Fairy Book (1916) | have | PG 26019, `jacobs-europas-fairy-book` (1395 units) |
| jacobs-aesop | excluded | The Fables of Aesop (PG 28): held on the Aesop shelf as `aesop-jacobs` |
| jacobs-celtic-folk-and-fairy-tales | pending | PENDING CHECK: Celtic Folk and Fairy Tales (PG 35862) is probably Celtic Fairy Tales under an American title; held back until compared |
| jacobs-edited-only | excluded | works Jacobs only edited or introduced: Painter's Palace of Pleasure (PG 20241, 34053, 34840), Morris's Old French Romances (PG 5988) |
| jacobs-not-fairy-tales | excluded | The Story of Geographical Discovery (PG 14291), As Others Saw Him (PG 48974): outside the relay's ask |

## George Webbe Dasent (Norse tales and sagas)

Shelf: `pipeline/dasent_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Asbjørnsen and Moe's Norwegian tales in Dasent's translation, and (relay 6) two of his saga translations: The Story of Burnt Njal, from the proofread transcription of the 1900 one-volume reprint (saga text complete, his introduction abridged), cut by its 158 chapters, and The Story of Gisli the Outlaw (1866), raw IA OCR graded A. The translator is in each title. Tales from the Fjeld prints two different tales called The Haunted Mill and sets The Companion over its frame and again over the tale, so 14 of its ids carry a ~2 suffix; left so rather than merging two tales. The older Gutenberg Njal (PG 597) is the same translation and is not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Popular Tales from the Norse, Asbjørnsen and Moe, tr. George Webbe Dasent (1859) | have | PG 8933, `dasent-popular-tales-from-the-norse` (3348 units) |
| Tales from the Fjeld, Asbjørnsen, tr. George Webbe Dasent (1874) | have | PG 36385, `dasent-tales-from-the-fjeld` (2368 units) |
| The Story of Burnt Njal, from the Icelandic of the Njals Saga, tr. George Webbe Dasent (1861; one-volume reprint, 1900, with Dasent's preface abridged) | have | PG 17919, `dasent-burnt-njal` (4096 units) |
| The Story of Gisli the Outlaw, from the Icelandic, tr. George Webbe Dasent (Edinburgh, 1866) | have-raw | IA `storygislioutla00dasegoog`, `dasent-gisli-the-outlaw` |
| dasent-selection | excluded | A Selection from the Norse Tales for the Use of Children (PG 64189): a selection from Popular Tales from the Norse, a duplicate of its stories |
| dasent-njal-duplicate | excluded | The Story of Burnt Njal (PG 597, 1995 e-text by Douglas Killings): an older transcription of the same translation; the header does not name Dasent as translator. PG 17919 is held instead |
| dasent-orkneyingers | excluded | The Orkneyingers' Saga (Rolls Series, 1894): no usable scan found on this pass |

## W. R. S. Ralston (Russian tales)

Shelf: `pipeline/ralston_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Ralston's translation with his commentary, cut Chapter > tale (51 tales, as his Contents lists them); footnote marks on tale titles are stripped from the citation through a new opt-in 'strip' on convert_nested.py levels. Ten ids carry ~2: the Contents prints each chapter's summary under the same heading as the chapter's opening. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Russian Fairy Tales: A Choice Collection of Muscovite Folk-lore, tr. W. R. S. Ralston (1873) | have | PG 22373, `ralston-russian-fairy-tales` (3465 units) |
| ralston-other-translations | excluded | Turgenev's Liza (PG 12194) and Schiefner's Tibetan Tales (PG 66870), both tr. Ralston: outside the relay's ask (Russian tales); Tibetan Tales would suit a later folk-tale batch |
| ralston-commentary-only | excluded | Stokes's Indian Fairy Tales (PG 31209): Ralston wrote notes only |

## Charles Perrault (English translations before 1929)

Shelf: `pipeline/perrault_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Three translations, each its own work with its translator in the title, as with Andersen. Samber's 1729 version as revised by Mansion (1922) is cut by its own Contents, read leniently; each tale's half-title and body title both register, so a tale's opening caption sits under the half-title. Johnson's Old-Time Stories also carries three tales by Mme de Beaumont and Mme d'Aulnoy, said so in its title. Lang's 1888 Perrault's Popular Tales is the French text and is held back; Tales of Passed Times names no translator and is pending. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Tales of Mother Goose, tr. Charles Welsh (1901) | have | PG 17208, `perrault-mother-goose-welsh` (404 units) |
| The Fairy Tales of Charles Perrault, tr. Robert Samber, rev. J. E. Mansion (1922) | have | PG 29021, `perrault-fairy-tales-samber-mansion` (565 units) |
| Old-Time Stories, tr. A. E. Johnson (1921), with three tales by Mme de Beaumont and Mme d'Aulnoy | have | PG 31431, `perrault-old-time-stories-johnson` (925 units) |
| perrault-lang-french | excluded | Perrault's Popular Tales, ed. Andrew Lang (PG 33931, Oxford 1888): the French text with Lang's English introduction, not an English translation; the Lang shelf points here, so it is noted here, held back for Adam |
| perrault-translator-unrecorded | pending | Tales of Passed Times (PG 33511, ill. Charles Robinson, with d'Aulnoy and Beaumont) names no translator; it does not enter the shelf until one is identified (the 2026-07-26 rights rule) |
| perrault-anthologies | excluded | Planché's Four and Twenty Fairy Tales (PG 52719, 1858) and Quiller-Couch's The Sleeping Beauty (PG 51275): anthologies mostly of other French writers; Perrault is a minority of each |
| perrault-chapbooks | excluded | single-tale Blue Beard chapbooks (PG 43457, 44288, 45381): anonymous retellings, no translator recorded |
| perrault-other | excluded | Vitruvius abridged by Claude Perrault (PG 27877): a different Perrault |

## Padraic Colum (before 1929)

Shelf: `pipeline/colum_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Colum's own retellings, so no translator is owed. The King of Ireland's Son and The Adventures of Odysseus are cut story (or Part) > numbered section, through convert_nested.py; At the Gateways of the Day nests its end-notes under NOTES so a note does not share a tale's id, and takes one 150-character tale title through the new opt-in 'max' key. Three Plays (PG 11878) is left out as drama. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The King of Ireland's Son (1916) | have | PG 3495, `colum-king-of-irelands-son` (1277 units) |
| The Adventures of Odysseus and The Tales of Troy (1918) | have | PG 16867, `colum-adventures-of-odysseus` (778 units) |
| The Boy Who Knew What the Birds Said (1918) | have | PG 24493, `colum-boy-who-knew-what-the-birds-said` (564 units) |
| The Boy Apprenticed to an Enchanter (1920) | have | PG 53252, `colum-boy-apprenticed-to-an-enchanter` (456 units) |
| The Children of Odin (1920) | have | PG 24737, `colum-children-of-odin` (1415 units) |
| The Golden Fleece and the Heroes Who Lived Before Achilles (1921) | have | PG 37881, `colum-golden-fleece` (1197 units) |
| At the Gateways of the Day (1924) | have | PG 69724, `colum-at-the-gateways-of-the-day` (727 units) |
| colum-duplicates | excluded | The Golden Fleece (PG 2395): an older transcription of the same book, without the illustrated edition's apparatus |
| colum-plays | excluded | Three Plays (PG 11878): drama, outside the relay's folk-tale ask |
| colum-commentary-only | excluded | Stephens's Mary, Mary (PG 24742): Colum wrote the introduction only |
| colum-post-1928 | excluded | anything Colum published after 1928 is not taken (the relay's pre-1929 line) |

## Sir Thomas Malory (Le Morte d'Arthur)

Shelf: `pipeline/malory_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Two public-domain texts, each its own work: Caxton's 1485 text in modern spelling (two volumes) and Strachey's Globe edition (1868, rev. 1891). Both are cut Book > Chapter, the citation Caxton's own division (`BOOK III / CHAPTER VI, par. 2`); front matter is cited `front, par. n` so the Contents cannot file it under a chapter. The Caxton volumes keep 22 ~2 ids where a chapter heading is printed in a shape the rule misses. Retellings for children are left out. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Le Morte d'Arthur, Caxton's text (1485) in modern spelling, vol. 1 | have | PG 1251, `malory-morte-darthur-caxton-1` (679 units) |
| Le Morte d'Arthur, Caxton's text (1485) in modern spelling, vol. 2 | have | PG 1252, `malory-morte-darthur-caxton-2` (870 units) |
| Le Morte Darthur, ed. Sir Edward Strachey (Globe edition, 1868, rev. 1891) | have | PG 46853, `malory-morte-darthur-strachey` (3188 units) |
| malory-retellings | excluded | retellings and abridgements: Knowles's Legends of King Arthur (PG 12753), Lanier's Boy's King Arthur (66585), Cutler (22053), Macgregor (25654), Holland (36462), Charles Morris's Historic Tales vols 13-14 (31900, 32292) |
| malory-anthologies | excluded | Harvard Classics vol. 35, Chronicle and Romance (PG 13674): extracts only |
| malory-sommer | excluded | Sommer's critical edition (1889-91, with Lang's essay), named on the Lang shelf: not taken in this batch; IA scans exist if Adam wants the scholarly text |

## Beowulf (translations before 1929)

Shelf: `pipeline/beowulf_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Four translations, each its own work with its translator in the title, as with Andersen. Hall's carries his glossary and notes; Morris and Wyatt's is cut by its fitts; Gummere's and Kirtlan's by their numbered sections. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Beowulf: An Anglo-Saxon Epic Poem, tr. J. Lesslie Hall (1892) | have | PG 16328, `beowulf-hall` (1402 units) |
| The Tale of Beowulf, tr. William Morris and A. J. Wyatt (1895) | have | PG 20431, `beowulf-morris-wyatt` (212 units) |
| The Story of Beowulf, tr. Ernest J. B. Kirtlan (1914) | have | PG 50742, `beowulf-kirtlan` (366 units) |
| Beowulf, tr. Francis B. Gummere (1910) | have | PG 981, `beowulf-gummere` (201 units) |
| beowulf-scholarship | excluded | Chambers's Beowulf: An Introduction (PG 34117), Olson's Hrolfs Saga and Beowulf (14878), Tinker's Translations of Beowulf (25942): about the poem, not the poem |
| beowulf-elsewhere | excluded | Longfellow's Beowulf passage is on the Longfellow translator shelf (lane C) |
| beowulf-ia-candidates | excluded | Earle (1892) and Tinker (1902) translations exist as IA scans; not taken in this batch |

## The Poetic Edda (Bellows, 1923)

Shelf: `pipeline/poetic-edda_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Henry Adams Bellows's translation, cut Poem > INTRODUCTORY NOTE / TEXT / NOTES: a poem's text has no heading of its own, so its stanza 1 (the first numbered paragraph with Bellows's caesura bar) marks where TEXT begins, through convert_nested.py's opt-in label and keep. One fragment (Brot af Sigurtharkvithu) prints its NOTES heading run into the preceding prose, so its notes sit under TEXT and 14 ids take ~2; the source is not hand-edited (rule 2). Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Poetic Edda, tr. Henry Adams Bellows (1923) | have | PG 73533, `edda-bellows` (4703 units) |
| edda-other-translations | excluded | Thorpe and Blackwell's Elder and Younger Eddas (PG 14726, 1866) and Morris and Magnusson's Volsunga Saga with Edda excerpts (PG 1152): other translations, not named by the relay; candidates for a later batch |
| edda-retellings | excluded | Faraday's The Edda (PG 13007-13008), Guerber's Myths of the Norsemen (28497), Wilmot-Buxton (29551): studies and retellings |
| edda-prose | excluded | Snorri's Prose (Younger) Edda is on the Sturluson shelf |

## The Kalevala (Crawford)

Shelf: `pipeline/kalevala_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). John Martin Crawford's 1888 translation, the complete Gutenberg file, cut by its fifty runes. The two-volume Gutenberg split of the same text and Kirby's later translation are not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Kalevala: The Epic Poem of Finland, tr. John Martin Crawford (1888) | have | PG 5186, `kalevala-crawford` (1534 units) |
| kalevala-duplicates | excluded | Crawford's Kalevala volumes 1 and 2 (PG 5184, 5185): the same text as the complete file |
| kalevala-kirby | excluded | W. F. Kirby's Kalevala, The Land of the Heroes (PG 25953, 33089, 1907): another translation, not named by the relay; a candidate for a later batch |

## Snorri Sturluson (Heimskringla, the Prose Edda)

Shelf: `pipeline/sturluson_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Heimskringla in Laing's translation as revised by Anderson (1889), cut Saga > chapter, and the Prose (Younger) Edda in Anderson's translation (1880). The Gutenberg Heimskringla names no translator; it was identified by collating its preface word for word against IA's scan of the 1889 edition, and its notes are signed --L. (Laing) and --Ed. (Anderson). Hearn's second-hand Olaf Tryggvason and Harald saga (PG 22093) is not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Heimskringla, or The Chronicle of the Kings of Norway, tr. Samuel Laing (1844), rev. Rasmus B. Anderson (1889); translator identified by collation, see the shelf note | have | PG 598, `sturluson-heimskringla-laing` (2785 units) |
| The Younger Edda, also called Snorre's Edda, or The Prose Edda, tr. Rasmus B. Anderson (1880) | have | PG 18947, `sturluson-younger-edda-anderson` (769 units) |
| sturluson-selection | excluded | The Sagas of Olaf Tryggvason and of Harald the Tyrant (PG 22093, tr. Ethel Harriet Hearn from Storm's Norwegian): two sagas of Heimskringla, translated at second hand; not taken |
| sturluson-thorpe | excluded | Thorpe and Blackwell's Elder and Younger Eddas (PG 14726): noted on the Poetic Edda shelf |

## Romesh Chunder Dutt (the Indian epics)

Shelf: `pipeline/dutt_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Dutt's condensations into English verse: the Maha-bharata (1898, clean Gutenberg, cut Book > canto) and the Ramayana (1899, raw IA OCR of an undated Google-scanned printing, graded B; IA's file name differs from the item id, so the row names it). Google asks that its scans be used non-commercially; that is a request, not a legal restriction on a public-domain text. Digital Library of India copies return 404. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Maha-bharata, the Epic of Ancient India, condensed into English verse by Romesh C. Dutt (1898) | have | PG 19630, `dutt-mahabharata` (2072 units) |
| Ramayana, the Epic of Rama, Prince of India, condensed into English verse by Romesh C. Dutt (1899; undated printing) | have-raw | IA `RamayanaTheEpicOfRamaPrinceOfIndiaCondensedIntoEnglishVerseBy`, `dutt-ramayana` |
| dutt-other-translators | excluded | Manmatha Nath Dutt's prose Ramayana (1891-94) and Ganguli's prose Mahabharata (PG 7864 and following, 15474-15477): other translators, not named by the relay |
| dutt-dli | excluded | Digital Library of India copies of Dutt (in.ernet.dli.*) return 404 and are not used |

## W. B. Yeats (folk-tale editor)

Shelf: `pipeline/yeats-folk_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Yeats as collector and editor of Irish folk tales; his poems and plays are not taken. Fairy and Folk Tales and Irish Fairy Tales are cut by their own Contents, read leniently (the house rule took each story's byline, BY CROFTON CROKER, for a heading). Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Fairy and Folk Tales of the Irish Peasantry, ed. W. B. Yeats (1888) | have | PG 33887, `yeats-fairy-and-folk-tales-irish-peasantry` (1820 units) |
| Irish Fairy Tales, ed. W. B. Yeats (1892) | have | PG 31763, `yeats-irish-fairy-tales` (756 units) |
| The Celtic Twilight (1893; enlarged 1902) | have | PG 10459, `yeats-celtic-twilight` (253 units) |
| yeats-poems-plays | excluded | Yeats's poems, plays, essays and autobiographies: outside a storytellers shelf (a poets' lane would hold them) |
| yeats-stories | excluded | Stories of Red Hanrahan (PG 5793), The Secret Rose (5795), Rosa Alchemica (5794), John Sherman and Dhoya (49109): his own fiction; a candidate for a later batch |

## Douglas Hyde (Irish folk tales)

Shelf: `pipeline/hyde_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Hyde's tales, collected in Irish and translated by him. Beside the Fire is raw IA OCR graded C: the Irish text faces the English, so the English-vocabulary score is low by design, not a bad scan. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Legends of Saints and Sinners, collected and tr. from the Irish by Douglas Hyde (1915) | have | PG 45910, `hyde-legends-of-saints-and-sinners` (1803 units) |
| Beside the Fire: A Collection of Irish Gaelic Folk Stories, ed. and tr. Douglas Hyde, notes by Alfred Nutt (London: David Nutt, 1890) | have-raw | IA `besidefirecollec00hyde`, `hyde-beside-the-fire` |
| hyde-other | excluded | A Literary History of Ireland (PG 53793) and the Revival of Irish Literature addresses (32746): history and criticism, not tales |

## Lady Gregory (Irish sagas and folklore)

Shelf: `pipeline/gregory_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her retellings of the Ulster and Fenian cycles and her collected folklore, all before 1929. Gods and Fighting Men, The Kiltartan Wonder Book and the first series of Visions and Beliefs are cut by their own Contents; Cuchulain of Muirthemne is raw IA OCR (grade A). Her plays are not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Gods and Fighting Men, tr. and arranged by Lady Gregory, preface by W. B. Yeats (1904) | have | PG 14465, `gregory-gods-and-fighting-men` (2140 units) |
| The Kiltartan Wonder Book (1910) | have | PG 76322, `gregory-kiltartan-wonder-book` (221 units) |
| Visions and Beliefs in the West of Ireland, collected by Lady Gregory, notes by W. B. Yeats, first series (1920) | have | PG 43973, `gregory-visions-and-beliefs-1` (1063 units) |
| Visions and Beliefs in the West of Ireland, second series (1920) | have | PG 43974, `gregory-visions-and-beliefs-2` (1270 units) |
| Cuchulain of Muirthemne, arranged and put into English by Lady Gregory, preface by W. B. Yeats (1902; New York: Scribner, 1903) | have-raw | IA `cuchulainofmuirt00greg_0`, `gregory-cuchulain-of-muirthemne` |
| gregory-plays | excluded | her plays (Seven Short Plays, New Comedies, Three Wonder Plays and others): drama, outside this shelf |
| gregory-other | excluded | The Kiltartan History Book (PG 11260), The Kiltartan Poetry Book (6656), Poets and Dreamers (18070), Our Irish Theatre (65953), Arabi and his Household (74246): candidates for a later batch or another lane |

## J. F. Campbell (Popular Tales of the West Highlands)

Shelf: `pipeline/campbell-highlands_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The 1890 four-volume edition, raw IA OCR. Volumes 1-3 grade C or D and volume 4 grade A on the English-vocabulary screen: the first three print Campbell's Gaelic originals beside his translations (spot-checked: the Gaelic is clean OCR), so the low score is the Gaelic, not the scan. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Popular Tales of the West Highlands, orally collected and tr. J. F. Campbell (1890 ed.), vol. 1 | have-raw | IA `populartalesofwe01campuoft`, `campbell-west-highlands-1` |
| Popular Tales of the West Highlands (1890 ed.), vol. 2 | have-raw | IA `populartalesofw02campuoft`, `campbell-west-highlands-2` |
| Popular Tales of the West Highlands (1890 ed.), vol. 3 | have-raw | IA `populartalesofwe03campuoft`, `campbell-west-highlands-3` |
| Popular Tales of the West Highlands (1890 ed.), vol. 4 | have-raw | IA `populartalesofwe40camp`, `campbell-west-highlands-4` |
| campbell-1860 | excluded | the first edition (Edinburgh, 1860-62), also on IA: the 1890 edition is preferred as the later revision |

## Yei Theodora Ozaki (Japanese tales)

Shelf: `pipeline/ozaki_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her English retellings from Japanese sources. Romances of Old Japan is cut by its own Contents (each romance is printed in parts, and the house rule took the PART lines for headings); the Gutenberg file is Brentano's 1920 printing of the 1919 book. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Japanese Fairy Tales, compiled by Yei Theodora Ozaki (1908) | have | PG 4018, `ozaki-japanese-fairy-tales` (1414 units) |
| Warriors of Old Japan, and Other Stories (1909) | have | PG 41437, `ozaki-warriors-of-old-japan` (787 units) |
| Romances of Old Japan, rendered into English from Japanese sources by Yei Theodora Ozaki (1919; New York: Brentano's, 1920) | have | PG 45933, `ozaki-romances-of-old-japan` (1386 units) |
| ozaki-other-japanese | excluded | Grace James's Japanese Fairy Tales (PG 35853, 1910) and Griffis's Japanese Fairy World (29337, 1880): other hands; candidates for a later batch |

## A. B. Mitford (Tales of Old Japan)

Shelf: `pipeline/mitford_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Mitford's 1871 translations, with his notes on ceremonies, cut by the book's own Contents read leniently. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Tales of Old Japan, tr. A. B. Mitford (1871) | have | PG 13015, `mitford-tales-of-old-japan` (1630 units) |
| mitford-memoirs | excluded | The Attache at Peking (PG 70467) and his Memories (76182-76184): memoir, not tales |

## Flora Annie Steel (folk tales)

Shelf: `pipeline/steel_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Tales of the Punjab with R. C. Temple's notes, the notes nested under NOTES TO TALES so they do not share a tale's id; and her retold English Fairy Tales, whose picture captions the house rule takes for headings in places (24 ~2 ids). Her novels are not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Tales of the Punjab: Folklore of India, told by Flora Annie Steel, notes by R. C. Temple (1894) | have | PG 6145, `steel-tales-of-the-punjab` (1815 units) |
| English Fairy Tales, retold by Flora Annie Steel (1918) | have | PG 17034, `steel-english-fairy-tales` (2073 units) |
| steel-novels | excluded | her novels and Indian stories (On the Face of the Waters and some twenty others, PG 39794-40142): fiction, outside a folk-tale batch |

## T. F. Crane (Italian Popular Tales)

Shelf: `pipeline/crane_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Crane's translations, cut Chapter > numbered tale (the tales are numbered through the book), and his notes nested under NOTES by chapter. The introduction and bibliography are front matter. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Italian Popular Tales, tr. Thomas Frederick Crane (1885) | have | PG 23634, `crane-italian-popular-tales` (1963 units) |

## George Bird Grinnell (Plains Indian tales)

Shelf: `pipeline/grinnell_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Pawnee and Blackfoot stories as told to Grinnell and set down by him in English; three books cut by their own Contents. His hunting, history and boys' books are not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Pawnee Hero Stories and Folk-Tales (1889) | have | PG 36923, `grinnell-pawnee-hero-stories` (1111 units) |
| Blackfoot Lodge Tales: The Story of a Prairie People (1892) | have | PG 11547, `grinnell-blackfoot-lodge-tales` (1208 units) |
| The Punishment of the Stingy, and Other Indian Stories (1901) | have | PG 66596, `grinnell-punishment-of-the-stingy` (468 units) |
| Blackfeet Indian Stories (1913) | have | PG 13833, `grinnell-blackfeet-indian-stories` (704 units) |
| grinnell-other | excluded | When Buffalo Ran (PG 15189), Trails of the Pathfinders (53897), Beyond the Old Frontier (54125), the Jack books and Boone and Crockett volumes: history, fiction and hunting, outside a folk-tale batch |

## Joel Chandler Harris (Uncle Remus)

Shelf: `pipeline/harris-remus_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). African American folk tales of Brer Rabbit in Harris's rendering of plantation dialect, inside a frame that carries the racism of its time and place; the shelf note says so plainly. Four books, two cut by their own Contents. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Uncle Remus, His Songs and His Sayings (1880) | have | PG 2306, `remus-his-songs-and-sayings` (1128 units) |
| Nights with Uncle Remus: Myths and Legends of the Old Plantation (1883) | have | PG 26429, `remus-nights-with-uncle-remus` (3087 units) |
| Told by Uncle Remus: New Stories of the Old Plantation (1905) | have | PG 55676, `remus-told-by-uncle-remus` (702 units) |
| Uncle Remus and Brer Rabbit (1907) | have | PG 22282, `remus-uncle-remus-and-brer-rabbit` (170 units) |
| remus-duplicates | excluded | Uncle Remus, His Songs and His Sayings (PG 21605): a second transcription; Nights with Uncle Remus (PG 24430): the later Milo Winter edition of the same book |
| remus-other | excluded | his other fiction and sketches (Free Joe, Mingo, Thimblefinger books and others): not Uncle Remus; candidates for a later batch |

## Frances Hodgson Burnett

Shelf: `pipeline/burnett_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her children's books, cut by their own Contents or chapter lines; Little Saint Elizabeth is nested story > part. Her adult novels are not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Secret Garden (1911) | have | PG 113, `burnett-secret-garden` (2136 units) |
| A Little Princess (1905) | have | PG 146, `burnett-little-princess` (1730 units) |
| Sara Crewe; or, What Happened at Miss Minchin's (1888) | have | PG 137, `burnett-sara-crewe` (380 units) |
| Little Lord Fauntleroy (1886) | have | PG 479, `burnett-little-lord-fauntleroy` (1234 units) |
| The Lost Prince (1915) | have | PG 384, `burnett-lost-prince` (2153 units) |
| Racketty-Packetty House (1906) | have | PG 8574, `burnett-racketty-packetty-house` (197 units) |
| Little Saint Elizabeth and Other Stories (1890) | have | PG 10466, `burnett-little-saint-elizabeth` (709 units) |
| burnett-duplicates | excluded | second transcriptions: The Secret Garden (PG 17396), A Little Princess (PG 37332), Sara Crewe (PG 24772) |
| burnett-adult | excluded | her adult novels and stories (That Lass o' Lowrie's, A Lady of Quality, T. Tembarom, The Shuttle and others): not children's classics; candidates for a later batch |
| burnett-german-school-edition | excluded | Little Lord Fauntleroy abridged for German schools (PG 49579): an abridgement with German apparatus |

## Louisa May Alcott

Shelf: `pipeline/alcott_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The March family books and her other books for young readers, cut by their own chapter lines. Her thrillers, sketches and story collections are not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Little Women (1868-69) | have | PG 514, `alcott-little-women` (3820 units) |
| Little Men (1871) | have | PG 2788, `alcott-little-men` (2423 units) |
| Jo's Boys (1886) | have | PG 3499, `alcott-jos-boys` (1628 units) |
| Eight Cousins (1875) | have | PG 2726, `alcott-eight-cousins` (1810 units) |
| Rose in Bloom (1876) | have | PG 2804, `alcott-rose-in-bloom` (1890 units) |
| An Old-Fashioned Girl (1870) | have | PG 2787, `alcott-old-fashioned-girl` (2236 units) |
| Under the Lilacs (1878) | have | PG 3795, `alcott-under-the-lilacs` (1774 units) |
| Jack and Jill (1880) | have | PG 2786, `alcott-jack-and-jill` (1739 units) |
| Flower Fables (1855) | have | PG 163, `alcott-flower-fables` (577 units) |
| alcott-duplicates | excluded | second transcriptions: Little Women (PG 37106), Little Men (PG 52900), Eight Cousins (PG 38567), Rose in Bloom (PG 41127) |
| alcott-other | excluded | the Aunt Jo's Scrap-Bag and Lulu's Library volumes, story collections, the thrillers (Behind a Mask and others), Hospital Sketches, Work, Moods: candidates for a later batch |

## Johanna Spyri

Shelf: `pipeline/spyri_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Heidi in two translations, each a witness of one book, and two more stories; every translator named as the Gutenberg header gives it. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Heidi, tr. Marion Edwards | have | PG 1448, `spyri-heidi-edwardes` (1430 units) |
| Heidi, tr. Elisabeth P. Stork (1915) | have | PG 20781, `spyri-heidi-stork` (1355 units) |
| Moni the Goat-Boy, tr. Helen B. Dole | have | PG 9383, `spyri-moni-the-goat-boy` (209 units) |
| Rico and Wiseli, tr. Louise Brooks | have | PG 9075, `spyri-rico-and-wiseli` (1233 units) |
| spyri-heidi-abbott | excluded | Heidi tr. Mabel Abbott (PG 46409, 1927): a third translation of the same book; US public domain, held back only to keep the shelf small |
| spyri-other | excluded | her other translated stories (Toni, Veronica, Gritli's Children, Maezli, Vinzi, Dora and others, each with its translator named in the catalog): candidates for a later batch |

## Anna Sewell

Shelf: `pipeline/sewell_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Black Beauty, cut by its own Contents. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Black Beauty (1877) | have | PG 271, `sewell-black-beauty` (925 units) |
| sewell-young-folks | excluded | Black Beauty, Young Folks' Edition (PG 11860): an adaptation |

## Fables (existing repo work — cross-referenced, located by search not assumption)

Searched 2026-10-02 (`git grep -il -E 'fable|aesop'` over the whole tree, then every remote branch): **no fables shelf, section or ingest exists in canon-corpus.** The only hits are KJV verses containing "fables", the `fable_review` provenance field, and a note in `pipeline/fetch_sources.py` that Chesterton-introduced Aesop was excluded from his shelf. Nothing is duplicated and no uids are touched.

| Work | Status | Where |
|---|---|---|
| Earlier fables work | pending | locate it: it may live in a sibling repo (armarium, wordhoard) or the vault, which this run cannot reach. Reconcile it with the Aesop shelf above before anything is minted |
