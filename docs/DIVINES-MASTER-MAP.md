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
| Grosart's Selections (1865); Charity and Its Fruits (1852); Observations on the Trinity (Smyth, 1880) | have-raw | IA |
| An Unpublished Essay on the Trinity (Fisher, 1903), IA scan | alternate | the same essay CCEL serves clean (`edwards-trinity`); it was listed twice until 2026-10-02 |
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
| Matthew Henry's Concise Commentary on the Bible | have, rights question | CCEL `mhcc` (`mhenry-concise`): an anonymous one-volume abridgement; CCEL names no abridger or date, so its PD status is not established (see the shelf's `_rights_question`) |
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

## Isaac Watts (round 5, my pick, 2026-10-02)

Prose only; the hymns and psalms are for the hymn manifest.

| Work | Status | Where |
|---|---|---|
| The Works, Leeds edition (Baines), vol. 1 of 9 | have | Gutenberg 77103 (`watts-works-leeds-1`) |
| A Short Essay Toward the Improvement of Psalmody | have | Gutenberg 30409 (`watts-essay-psalmody`) |
| The Works (London: Barfield, 1810, ed. Burder), vols. I-VI | have-raw | IA `worksofreverendl01watt`..`06watt` |
| The Leeds Works, vols. 2-9 | pending | not yet released on Gutenberg |
| Hymns and Spiritual Songs; The Psalms of David; Divine Songs | excluded here | hymn manifest |

## Archibald Alexander (round 5, my pick, 2026-10-02)

| Work | Status | Where |
|---|---|---|
| The Canon of the Old and New Testaments Ascertained | have | CCEL `canon` (`aalexander-canon`) |
| The Evidences of the Christian Religion | have | CCEL `evidences` (`aalexander-evidences`) |
| Outlines of Moral Science | have | CCEL `outlines` (`aalexander-moral-science`) |
| Thoughts on Religious Experience (1844) | have-raw | IA `thoughtsonreligi00alexuoft` |
| Biographical Sketches of the Log College (1851) | have-raw | IA `biographicalsketcheso00alex` |
| Practical Sermons (1850) | have-raw | IA `practicalsermons00alexuoft` |
| A History of the Israelitish Nation (1853) | have-raw | IA `historyofisraeli00alex` |
| A History of Colonization on the Western Coast of Africa (1846) | have-raw | IA `historyofcoloniz00alex` |
| J. W. and J. A. Alexander's books | excluded here | his sons |

## Thomas Chalmers (round 5, my pick, 2026-10-02)

No CCEL or Gutenberg text. The Works (Glasgow: William Collins, 1836-1842, 25 vols), one IA series (Princeton Seminary scans), raw OCR.

| Work | Status | Where |
|---|---|---|
| The Works, vols. I-XXV | have-raw | IA `worksofthomas01chal`..`03chal`, `worksofthomascha04chal`..`25chal` (`chalmers-works-01`..`25`) |
| Posthumous Works, ed. William Hanna (1847-52, 9 vols) | pending | scans found, set not yet checked |
| The 1840 printing; Select Works (1848-56) | alternate | the 1836-42 set is held |

## Ebenezer and Ralph Erskine (round 5, my pick, 2026-10-02)

The two brothers on one shelf. No CCEL or Gutenberg text; raw IA OCR.

| Work | Status | Where |
|---|---|---|
| Ebenezer Erskine, The Whole Works (Edinburgh: Ogle & Murray, 1871), vols. I-III | have-raw | IA `wholeworksoflate01ersk`..`03ersk` (`eerskine-works-01`..`03`) |
| Ralph Erskine, The Sermons and Other Practical Works (London: Tegg, 1865), vols. I-VII | have-raw | IA `sermonsotherpr01ersk`..`07ersk` (`rerskine-works-01`..`07`); the Gospel Sonnets are in it |
| Earlier editions (1763-1836) and single sermons (ECCO) | alternate | the 1865 and 1871 sets are held |

## Thomas Halyburton (round 5, my pick, 2026-10-02)

| Work | Status | Where |
|---|---|---|
| The Works (Glasgow: Blackie, 1833, ed. Robert Burns): The Great Concern of Salvation; Natural Religion Insufficient; communion sermons; Memoirs | have-raw | IA `worksofrevthomas00haly` (`halyburton-works-1833`) |
| Separate printings (1751-1865) | alternate | the 1833 Works are held |

## Hugh Binning (round 5, my pick, 2026-10-02)

| Work | Status | Where |
|---|---|---|
| The Works (Edinburgh: Fullarton, 1851, ed. Matthew Leishman) | have-raw | IA `worksofrevhughbi00binn` (`binning-works-1851`) |
| Works (1735; Edinburgh 1839, 3 vols) | alternate | the 1851 edition is held |

## James Durham (round 5, my pick, 2026-10-02)

No CCEL, Gutenberg or 19th-century collected edition on IA. Early printings, raw IA OCR, rough (77-85%).

| Work | Status | Where |
|---|---|---|
| Christ Crucified: 72 sermons on Isaiah 53 (1792), 2 vols | have-raw | IA `christcrucifiedo01durh`, `02durh` |
| The Law Unsealed (1777) | have-raw | IA `lawunsorp00durh` |
| A Commentarie upon the Book of the Revelation (1680) | have-raw | IA `commentarieuponb00durh` |
| Clavis Cantici: an Exposition of the Song of Solomon (1723) | have-raw | IA `claviscant00durh` |
| The Dying Man's Testament, a Treatise concerning Scandal (1659) | pending | the scan's OCR never names Durham |

## Octavius Winslow (round 5, my pick, 2026-10-02)

No CCEL or Gutenberg text. Fifteen books from library scans, raw IA OCR; slugs `owinslow-*`.

| Work | Status | Where |
|---|---|---|
| Experimental and Practical Views of the Atonement (1838); The Silver Trumpet (1844); The Work of the Holy Spirit (1846); Personal Declension and Revival (1847); The Inner Life (1853); The Glory of the Redeemer (1855); Glimpses of the Truth (1856); Midnight Harmonies (1856); Life in Jesus (his mother's memoir, 1860); Christ Ever With You (1863); The Sympathy of Christ (1863); The Precious Things of God (1867); The Ministry of Home (1867); None Like Christ (1868); Go and Tell Jesus (1869) | have-raw | IA (identifiers in the shelf) |
| Bare uploads of None Like Christ, Consider Jesus, The Inquirer Directed | excluded | no library provenance |
| 1961-2010 reprints | excluded | modern editions |

## B. B. Warfield (round 5, my pick, 2026-10-02)

No CCEL or Gutenberg text. Nineteen books he published in his lifetime, from library scans, raw IA OCR; slugs `warfield-*`.

| Work | Status | Where |
|---|---|---|
| Textual Criticism of the NT (1886); Revision of the Confession (1890); Two Studies in the History of Doctrine (1897); Right of Systematic Theology (1897); Present Day Conception of Evolution (1900); Predestination in the Reformed Confessions (1901); Making of the Westminster Confession (1901); Power of God unto Salvation (1903); Millennium and the Apocalypse (1904); Lord of Glory (1907); Africa and Christian Latin Literature (1907); Westminster Assembly and its Work (1908); Literary History of Calvin's Institutes (1909); Is Jesus God? (1912); Saviour of the World (1913); Plan of Salvation (1915); Faith and Life (1916); Counterfeit Miracles (1918); John Humphrey Noyes (1921) | have-raw | IA (identifiers in the shelf) |
| Oxford Works, 10 vols (1927-1932) | excluded | posthumous; lending scans; later volumes fail the rights gate |
| Four Hymns (1910) | excluded | verse, for the hymn manifest |
| Reprints 1935-1997; books by others with his contribution | excluded | modern or not his |

## James Henley Thornwell (round 5, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton and Library of Congress scans; slugs `thornwell-*`. He was a leading clerical defender of slavery and secession; the shelf waits on Adam's veto (DIGEST-A).

| Work | Status | Where |
|---|---|---|
| Collected Writings, vol. 1 Theological (1871), vol. 2 Theological and Ethical (1871), vol. 3 Theological and Controversial (1873), vol. 4 Ecclesiastical (1873) | have-raw | IA (identifiers in the shelf) |
| Discourses on Truth (1855); The Arguments of Romanists (1845) | have-raw | IA |
| Pamphlets on slavery and secession (1850-1862) | excluded | for Adam's call |
| Palmer, Life and Letters (1875) | excluded | biography by another author |

## Robert Lewis Dabney (round 5, my pick, 2026-10-02)

No CCEL text; Gutenberg holds only A Defence of Virginia, which is excluded. Raw IA OCR, mostly Princeton scans; slugs `dabney-*`. He defended slavery and, after the war, white supremacy; the shelf waits on Adam's veto (DIGEST-A).

| Work | Status | Where |
|---|---|---|
| Syllabus and Notes of Systematic and Polemic Theology, 2nd ed. (1878); Sacred Rhetoric (1870); The Sensualistic Philosophy (1875); The Christian Sabbath (1882); Christ Our Penal Substitute (1898) | have-raw | IA (identifiers in the shelf) |
| Discussions, vol. 1 Theological and Evangelical (1890), vol. 2 Evangelical (1891), vol. 3 Philosophical (1892), vol. 4 Secular (1897) | have-raw | IA |
| A Defence of Virginia (1867); political tracts | excluded | for Adam's call |
| Life of Stonewall Jackson; war memorials | excluded | military biography |

## Samuel Davies (round 5, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `sdavies-*`.

| Work | Status | Where |
|---|---|---|
| Sermons on Important Subjects, 3 vols (New York: Carter, 1845, with an essay by Albert Barnes) | have-raw | IA (identifiers in the shelf) |
| The Philadelphia edition (c1864, 3 vols) | alternate | its vol. 1 text file returned server errors |
| Letters from the Rev. Samuel Davies and others (1761) | excluded | short pamphlet, not his alone |

## George Swinnock (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `swinnock-*`.

| Work | Status | Where |
|---|---|---|
| Works, 5 vols (Edinburgh: Nichol, 1868): The Christian Man's Calling, The Door of Salvation Opened, Heaven and Hell Epitomized, The Incomparableness of God, The Fading of the Flesh and the rest | have-raw | IA (identifiers in the shelf) |
| First editions, 1659-1679 | alternate | IA (EEBO) |

## Thomas Adams (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `tadams-*`.

| Work | Status | Where |
|---|---|---|
| Works, 3 vols (Edinburgh: Nichol, 1861-62, memoir by Joseph Angus): his sermons, meditations and discourses | have-raw | IA (identifiers in the shelf) |

## David Clarkson (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `clarkson-*`.

| Work | Status | Where |
|---|---|---|
| Practical Works, 3 vols (Edinburgh: Nichol, 1864-65) | have-raw | IA (identifiers in the shelf) |

## Andrew Fuller (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from a Trinity College, Toronto scan; slug `afuller-*`.

| Work | Status | Where |
|---|---|---|
| Complete Works with a Memoir by A. G. Fuller (London: Dyer, 1846, one volume): The Gospel Worthy of All Acceptation, the Calvinistic and Socinian Systems, Strictures on Sandemanianism, Discourses on Genesis and on the Apocalypse, The Backslider and the rest | have-raw | IA (identifier in the shelf) |
| Philadelphia Works (1820-25, 8 vols) and later American editions | alternate | IA |
| Memoir of Samuel Pearce; Ryland's Life of Fuller | excluded | mostly others' words |

## Augustus Toplady (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `toplady-*`.

| Work | Status | Where |
|---|---|---|
| Works, 6 vols (London: Baynes, 1825, with a memoir): Historic Proof of the Doctrinal Calvinism of the Church of England, sermons, essays, letters, hymns and poems | have-raw | IA (identifiers in the shelf) |
| One-volume London editions (1837, 1844, 1857); the 1794 Works | alternate | IA |

## William Romaine (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from a Princeton scan; slug `romaine-*`.

| Work | Status | Where |
|---|---|---|
| Whole Works (London: Blake, 1837, one volume): Cadogan's Life, Discourses on the Law and Gospel, the Life, Walk and Triumph of Faith, Psalm 107, Letters, Sermons, Essay on Psalmody | have-raw | IA (identifier in the shelf) |
| Works, 8 vols (London, 1801) | alternate | IA; long-s print OCRs at 85-88% |

## Isaac Ambrose (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from a Princeton scan; slug `ambrose-*`.

| Work | Status | Where |
|---|---|---|
| Works (London: Tegg, 1829, one volume): Prima, Media and Ultima (Regeneration, the Means, the Last Things), Looking unto Jesus, War with Devils, Communion with Angels, with a memoir | have-raw | IA (identifier in the shelf) |
| Earlier Works (1799-1811) and separate printings (1737-1856) | alternate | IA |

## Charles Bridges (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `bridges-*`.

| Work | Status | Where |
|---|---|---|
| Works (New York: Carter, 1849): vol. 1 Proverbs, vol. 2 The Christian Ministry, vol. 3 Psalm 119 with the Memoir of Mary Jane Graham | have-raw | IA (identifiers in the shelf) |
| An Exposition of the Book of Ecclesiastes (1860) | have-raw | IA |
| Separate editions (1832-1865) | alternate | IA |

## Charles Simeon (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `simeon-horae-*`.

| Work | Status | Where |
|---|---|---|
| Horae Homileticae, 21 vols (London: Holdsworth and Ball, 1832-33): 2,536 sermon outlines, Genesis to Revelation, with Claude's Essay on the Composition of a Sermon and an index | have-raw | IA (identifiers in the shelf) |
| Toronto scan of the same set; the 1819 and 1855 editions | alternate | IA |

## Robert Haldane (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `haldane-*`.

| Work | Status | Where |
|---|---|---|
| Exposition of the Epistle to the Romans, 3 vols (Edinburgh: Whyte, 1838) | have-raw | IA (identifiers in the shelf) |
| The Evidence and Authority of Divine Revelation, 2 vols (1839) | have-raw | IA |
| The Books of the Old and New Testaments Proved to be Canonical (1832) | have-raw | IA |
| One-volume Romans (1847-1874) | alternate | IA |
| Pamphlets (1824-1840) | excluded | controversy |

## James Buchanan (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `jbuchanan-*`.

| Work | Status | Where |
|---|---|---|
| The Doctrine of Justification (1867); The Office and Work of the Holy Spirit (1842); Comfort in Affliction (1844); Faith in God and Modern Atheism, 2 vols (1855); Analogy Considered as a Guide to Truth (1864) | have-raw | IA (identifiers in the shelf) |
| Later and American editions | alternate | IA |
| Lectures on church establishments (1835); Essays and Reviews articles (1861) | excluded | church politics; attribution not checked |

## William Cunningham (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton and Toronto scans; slugs `wcunningham-*`.

| Work | Status | Where |
|---|---|---|
| The Reformers and the Theology of the Reformation (1862); Historical Theology, 2 vols (1862-63); Discussions on Church Principles (1863), all ed. Buchanan and Bannerman | have-raw | IA (identifiers in the shelf) |
| Theological Lectures (1878) | have-raw | IA |
| Works (1870) issue; other scans | alternate | IA |

## Patrick Fairbairn (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Toronto, Princeton, Library of Congress, California and Google scans; slugs `fairbairn-*`.

| Work | Status | Where |
|---|---|---|
| The Typology of Scripture, 4th ed., 2 vols (1864); Jonah (1849); Hermeneutical Manual (1858); Prophecy (1866); The Revelation of Law in Scripture (1869); The Pastoral Epistles (1874); Pastoral Theology, with Dodds's memoir (1875); Ezekiel (1876) | have-raw | IA (identifiers in the shelf) |
| Other editions and scans | alternate | IA |
| His translations from the German | excluded | other men's books |

## John Angell James (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `jajames-works-*`.

| Work | Status | Where |
|---|---|---|
| Works, ed. T. S. James, vols 1-14, 16-17 (London: Hamilton, Adams, from 1860): The Anxious Inquirer, Christian Charity, the Family Monitor, addresses, sermons and the rest | have-raw | IA (identifiers in the shelf) |
| Works, vol. 15 | pending | no scan with a text layer |

## William Jay (round 6, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Trinity College, Toronto and Princeton scans; slugs `wjay-*`.

| Work | Status | Where |
|---|---|---|
| Works, 3 vols (New York: Harper, 1861): vol. 1 the daily exercises for the closet, vol. 2 short discourses for families and more, vol. 3 sermons | have-raw | IA (identifiers in the shelf) |
| Autobiography, ed. Redford and J. A. James (1855) | have-raw | IA |
| Earlier collected editions (1832, 1844); separate printings | alternate | IA |

## William Bridge (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from California scans; slugs `wbridge-*`.

| Work | Status | Where |
|---|---|---|
| Works, now first collected, 5 vols (London: Tegg, 1845): A Lifting up for the Downcast, Christ and the Covenant, sermons and treatises | have-raw | IA (identifiers in the shelf) |
| Toronto scan; his 1654 and 1657 collections | alternate | IA |

## Edward Reynolds (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `ereynolds-*`.

| Work | Status | Where |
|---|---|---|
| Whole Works, 6 vols (London: Holdsworth, 1826, memoir by Alexander Chalmers): the Passions and Faculties of the Soul, Psalm 110, Hosea 14, sermons | have-raw | IA (identifiers in the shelf) |
| Explication of Psalm 110 (1837) | alternate | IA |

## William Bates (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Google and Princeton scans; slugs `wbates-*`.

| Work | Status | Where |
|---|---|---|
| Whole Works (London: Black, 1815), vols 2-4: sermons on forgiveness, the Everlasting Rest of the Saints, miscellaneous sermons | have-raw | IA (Google scans) |
| The Harmony of the Divine Attributes (1831); The Four Last Things (1826); Spiritual Perfection (1834, with Pye Smith's essay) | have-raw | IA |
| Whole Works, vol. 1 | pending | no scan found |

## Ezekiel Hopkins (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `ehopkins-*`.

| Work | Status | Where |
|---|---|---|
| Works, 3 vols (Philadelphia: Leighton, ed. C. W. Quick from Pratt's London edition, 1867-74): the Ten Commandments, the Lord's Prayer, the Two Covenants, Death Disarmed, sermons | have-raw | IA (identifiers in the shelf) |
| Pratt's London Works (1809); separate printings (1701-1860) | alternate | IA |

## Robert Traill (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Google scans; slugs `rtraill-*`.

| Work | Status | Where |
|---|---|---|
| Works, 4 vols in 2 (Edinburgh: Ogle, 1810): the Throne of Grace, sixteen sermons on the Lord's Prayer in John 17, the Steadfast Adherence to the Profession of our Faith, eleven sermons, the Vindication of the Protestant Doctrine of Justification | have-raw | IA (identifiers in the shelf) |
| Glasgow (1775) and 1796 editions; Select Practical Writings (1845) | alternate | IA |

## George Gillespie (round 7, my pick, 2026-10-02)

Slugs `gillespie-*`.

| Work | Status | Where |
|---|---|---|
| Works, vol. 1 (Edinburgh: Ogle, 1846, ed. Hetherington): Dispute against the English Popish Ceremonies, Assertion of the Government of the Church of Scotland and more | have-clean | Gutenberg 26849 |
| Aaron's Rod Blossoming (1844) | have-raw | IA |
| Works, vol. 2; A Treatise of Miscellany Questions | pending | no usable scan (the 1649 one OCRs at 75%) |

## David Dickson (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `ddickson-*`. A thin shelf: his commentaries survive on IA only in 17th-century printings.

| Work | Status | Where |
|---|---|---|
| Select Practical Writings, vol. 1 (1845) | have-raw | IA |
| The Sum of Saving Knowledge, with Durham (1886, Macpherson's notes) | have-raw | IA |
| Psalms (1653-54), Hebrews (1635), Matthew; Therapeutica Sacra (1697) | pending | only 17th-century printings |

## John Brown of Haddington (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Library of Congress, Cornell and Princeton scans; slugs `jbrown-*`.

| Work | Status | Where |
|---|---|---|
| A Compendious View of Natural and Revealed Religion (1819); A Dictionary of the Holy Bible (1839); Explication of the Shorter Catechism (1845); Compendious History of the British Churches, 2 vols (1820); A Brief View of the Figures of Scripture (1812) | have-raw | IA (identifiers in the shelf) |
| Concordance | alternate | a word list, left for later |
| Jamieson-Fausset-Brown; John Brown of Edinburgh's Romans | excluded | other authors |

## Timothy Dwight (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text of the Theology. Raw IA OCR from California scans; slugs `tdwight-*`.

| Work | Status | Where |
|---|---|---|
| Theology Explained and Defended in a Series of Sermons, 4 vols (New York: Harper, 1846, with a memoir) | have-raw | IA (identifiers in the shelf) |
| Editions of 1818-1837 | alternate | IA |

## Samuel Hopkins (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `shopkins-*`.

| Work | Status | Where |
|---|---|---|
| Works, 3 vols (Boston: Doctrinal Tract and Book Society, 1854, with a memoir): the System of Doctrines, the Inquiry into True Holiness, the Dialogue concerning the Slavery of the Africans and more | have-raw | IA (identifiers in the shelf) |
| Separate printings (1765-1815), including his Life of Edwards | alternate | IA |
| Sketches of his life (1805) | excluded | autobiographical, edited by Stephen West; for Adam to add if wanted |

## Joseph Bellamy (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from New York Public Library scans; slugs `jbellamy-*`.

| Work | Status | Where |
|---|---|---|
| Works, 2 vols (Boston: Doctrinal Tract and Book Society, 1853, with a memoir): True Religion Delineated, the Wisdom of God in the Permission of Sin, the Theron, Paulinus and Aspasio dialogues, sermons | have-raw | IA (identifiers in the shelf) |
| New York Works (1811); 18th-century printings | alternate | IA |

## Thomas Vincent (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR; slugs `tvincent-*`.

| Work | Status | Where |
|---|---|---|
| An Explanation of the Assembly's Shorter Catechism (1854); Christ's Sudden and Certain Appearance to Judgment (1823); God's Terrible Voice in the City (1811); The True Christian's Love of the Unseen Christ (1701) | have-raw | IA (identifiers in the shelf) |
| Other editions (1668-1840) | alternate | IA |

## Henry Smith (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR from Princeton scans; slugs `hsmith-*`.

| Work | Status | Where |
|---|---|---|
| Works, 2 vols (Edinburgh: Nichol, 1866): sermons, treatises, prayers and poems | have-raw | IA (identifiers in the shelf) |

## Lewis Bayly (round 7, my pick, 2026-10-02)

No CCEL or Gutenberg text. Raw IA OCR of an Eighteenth Century Collections Online scan; slug `bayly-*`.

| Work | Status | Where |
|---|---|---|
| The Practice of Piety (London, 1754) | have-raw | IA |
| Editions of 1623-1734; the French (1661) and Massachusett (1665, 1685) translations | alternate | IA |

## John Preston (round 7, my pick, 2026-10-02)

Nothing shelved. IA holds only 17th-century printings, and their OCR scored 79-81%.

| Work | Status | Where |
|---|---|---|
| The Breast-Plate of Faith and Love; The New Covenant; Life Eternal; Four Godly Treatises; The Golden Sceptre; Mount Ebal; Sin's Overthrow (1630-1641) | pending | IA identifiers in the shelf's `_pending` |

## John Wesley (round 8, my pick, 2026-10-02)

Slugs `wesley-*`.

| Work | Status | Where |
|---|---|---|
| Sermons on Several Occasions; Explanatory Notes on the Bible; A Plain Account of Christian Perfection; the Journal (Parker's abridgement) | have-clean | CCEL |
| Works, 10 vols (New York: J. & J. Harper, 1826-30) | have-raw | IA (identifiers in the shelf) |
| Hymns and poems | see hymn manifest | |
| Jackson's 1872 Works | alternate | on IA only as 1958-65 reprints, except vols 10 and 14 |

## Richard Hooker (round 8, my pick, 2026-10-02)

Slugs `hooker-*`.

| Work | Status | Where |
|---|---|---|
| A Learned Discourse of Justification | have-clean | CCEL |
| Works, ed. John Keble, 3 vols (Oxford, 1836): Of the Laws of Ecclesiastical Polity, sermons, tractates, Walton's Life | have-raw | IA (identifiers in the shelf) |
| The Church Defended (CCEL) | excluded | stubs |


## Jeremy Taylor (round 8, my pick, 2026-10-02)

Slugs `jtaylor-*`.

| Work | Status | Where |
|---|---|---|
| The Rule and Exercises of Holy Living | have-clean | CCEL |
| The Rule and Exercises of Holy Dying | have-clean | CCEL |
| Whole Works, ed. Reginald Heber, rev. Charles Page Eden, 10 vols (London, 1847-54) | have-raw | IA (identifiers in the shelf) |


## Lancelot Andrewes (round 8, my pick, 2026-10-02)

Slugs `andrewes-*`.

| Work | Status | Where |
|---|---|---|
| Private Devotions (the Greek), tr. J. H. Newman | have-clean | CCEL |
| Ninety-Six Sermons, 5 vols (Oxford: Parker, 1841-43, Library of Anglo-Catholic Theology) | have-raw | IA (identifiers in the shelf) |
| A Pattern of Catechistical Doctrine, and Other Minor Works (Oxford, 1846) | have-raw | IA |
| Private Devotions (the Latin), tr. J. M. Neale | pending | not yet looked for |


## Joseph Butler (round 8, my pick, 2026-10-02)

Slugs `butler-*`.

| Work | Status | Where |
|---|---|---|
| The Analogy of Religion, with Two Brief Dissertations | have-clean | CCEL |
| Fifteen Sermons Preached at the Rolls Chapel | have-clean | CCEL |
| Works, ed. W. E. Gladstone, 2 vols (Oxford: Clarendon Press, 1896) | have-raw | IA (identifiers in the shelf) |


## Thomas Fuller (round 8, my pick, 2026-10-02)

Slugs `fuller-*`.

| Work | Status | Where |
|---|---|---|
| Good Thoughts in Bad Times and Other Papers | have-clean | CCEL |
| David's Heinous Sin, Hearty Repentance, Heavy Punishment (verse) | have-clean | CCEL |
| The Church History of Britain, 3 vols (London: Tegg, 1837) | have-raw | IA (identifiers in the shelf) |
| The Holy State and the Profane State (London: Pickering, 1840) | have-raw | IA |
| The History of the Worthies of England | not looked for | |


## John Donne (round 8, my pick, 2026-10-02)

Slugs `donne-*`.

| Work | Status | Where |
|---|---|---|
| Devotions upon Emergent Occasions | have-clean | CCEL |
| Death's Duel | have-clean | CCEL |
| Sermon Preached to the Lords upon Easter-day | have-clean | CCEL |
| Works, ed. Henry Alford, 6 vols (London: Parker, 1839) | have-raw | IA (identifiers in the shelf) |
| Sermon at the Spital (CCEL) | excluded | a fragment |


## Thomas Traherne (round 8, my pick, 2026-10-02)

Slugs `traherne-*`.

| Work | Status | Where |
|---|---|---|
| Centuries of Meditations | have-clean | CCEL |
| Poetical Works, ed. Bertram Dobell (London, 1903) | have-raw | IA (identifier in the shelf) |
| Christian Ethicks (1675) | pending | long-s OCR, 79.8% |


## John Henry Newman (round 8, my pick, 2026-10-02)

Slugs `newman-*`.

| Work | Status | Where |
|---|---|---|
| The Dream of Gerontius (verse) | have-clean | CCEL |
| Apologia pro Vita Sua (1890 printing) | have-clean | Gutenberg 22088 |
| An Essay on the Development of Christian Doctrine | have-clean | Gutenberg 35110 |
| An Essay in Aid of a Grammar of Assent | have-clean | Gutenberg 34022 |
| The Idea of a University | have-clean | Gutenberg 24526 |
| Historical Sketches, vol. 1 | have-clean | Gutenberg 21859 |
| Parochial and Plain Sermons, 8 vols (London: Longmans, 1891) | have-raw | IA (identifiers in the shelf) |
| Tracts for the Times (CCEL) | excluded | several authors |
| Callista; Loss and Gain | excluded | novels |


## George Herbert (round 8, my pick, 2026-10-02)

Slugs `herbert-*`.

| Work | Status | Where |
|---|---|---|
| A Priest to the Temple, or The Country Parson | have-clean | CCEL |
| English Works, ed. George Herbert Palmer, 3 vols (Boston: Houghton Mifflin, 1905; vol. 1 a 1915 printing), including The Temple | have-raw | IA (identifiers in the shelf) |


## Thomas Ken (round 8, my pick, 2026-10-02)

Slugs `ken-*`.

| Work | Status | Where |
|---|---|---|
| Prose Works, ed. J. T. Round (London, 1838) | have-raw | IA (identifiers in the shelf) |
| A Manual of Prayers for Winchester College (1857 printing) | have-raw | IA |
| The Christian Year, or Hymns and Poems (London: Pickering, 1868) | have-raw | IA |


## Joseph Hall (round 8, my pick, 2026-10-02)

Slugs `hall-*`.

| Work | Status | Where |
|---|---|---|
| Works, ed. Philip Wynter (Oxford: University Press, 1863), vols 1-9 | have-raw | IA (identifiers in the shelf) |
| Works, vol. 10 | pending | no correct scan found yet |


## Isaac Barrow (round 8, my pick, 2026-10-03)

Slugs `barrow-*`.

| Work | Status | Where |
|---|---|---|
| Theological Works, ed. Alexander Napier, 9 vols (Cambridge: University Press, 1859) | have-raw | IA (identifiers in the shelf) |


## Henry Martyn (round 8, my pick, 2026-10-03)

Slugs `martyn-*`.

| Work | Status | Where |
|---|---|---|
| Journals and Letters, ed. Samuel Wilberforce, 2 vols (London, 1837) | have-raw | IA (identifiers in the shelf) |
| Sermons (Boston, 1822) | have-raw | IA |


## James Hervey (round 9, my pick, 2026-10-03)

Slugs `hervey-*`.

| Work | Status | Where |
|---|---|---|
| Whole Works, 1 vol. (Edinburgh: Brown and Nelson, 1834), incl. Meditations and Contemplations, Theron and Aspasio | have-raw | IA (identifier in the shelf) |


## Henry Venn (round 9, my pick, 2026-10-03)

Slugs `venn-*`.

| Work | Status | Where |
|---|---|---|
| The Complete Duty of Man (New York, 1838 printing) | have-raw | IA (identifier in the shelf) |


## John Fletcher of Madeley (round 9, my pick, 2026-10-03)

Slugs `fletcher-*`.

| Work | Status | Where |
|---|---|---|
| Works, 4 vols (New York: Carlton and Porter / Carlton and Lanahan, undated; catalogued 1833), incl. the Checks to Antinomianism | have-raw | IA (identifiers in the shelf) |


## Robert Hall (round 9, my pick, 2026-10-03)

Slugs `rhall-*` (not `hall-*`, which is Joseph Hall's).

| Work | Status | Where |
|---|---|---|
| Works, ed. Olinthus Gregory, 6 vols (London: Bohn; catalogued 1846) | have-raw | IA (identifiers in the shelf) |
| Miscellaneous Works and Remains (London: Bohn; catalogued 1846) | have-raw | IA |


## Edward Payson (round 9, my pick, 2026-10-03)

Slugs `payson-*`.

| Work | Status | Where |
|---|---|---|
| Complete Works, 3 vols (Philadelphia: Gihon, 1851) | have-raw | IA (identifiers in the shelf) |


## Cotton Mather (round 9, my pick, 2026-10-03)

Slugs `cmather-*`.

| Work | Status | Where |
|---|---|---|
| Magnalia Christi Americana, 2 vols (Hartford: Silas Andrus and Son; copyright 1852) | have-raw | IA (identifiers in the shelf) |
| Essays to Do Good (Bonifacius) (Boston, 1808) | have-raw | IA |
| The Wonders of the Invisible World | excluded | bundled with Increase Mather; Salem trials; Adam's call |


## John Pearson (round 9, my pick, 2026-10-03)

Slugs `pearson-*`.

| Work | Status | Where |
|---|---|---|
| An Exposition of the Creed, with Edward Walford's analysis (London: George Bell; catalogued 1902) | have-raw | IA (identifier in the shelf) |


## William Paley (round 9, my pick, 2026-10-03)

Slugs `paley-*`.

| Work | Status | Where |
|---|---|---|
| A View of the Evidences of Christianity | have-clean | CCEL |
| Natural Theology, with illustrative notes | have-clean | CCEL |
| Works, 1 vol. (Philadelphia: Crissy and Markley; catalogued 1853), incl. Horae Paulinae, Moral and Political Philosophy, sermons | have-raw | IA (identifier in the shelf) |


## Robert South (round 9, my pick, 2026-10-03)

Slugs `south-*`.

| Work | Status | Where |
|---|---|---|
| Sermons Preached upon Several Occasions, 7 vols (Oxford: Clarendon Press, 1823) | have-raw | IA (identifiers in the shelf) |


## Thomas Scott (round 9, my pick, 2026-10-03)

Slugs `tscott-*`.

| Work | Status | Where |
|---|---|---|
| Essays on the Most Important Subjects in Religion; The Force of Truth (Edinburgh, 1825) | have-raw | IA (identifier in the shelf) |
| The Holy Bible with Explanatory Notes (the Family Bible) | not looked for | |


## William Beveridge (round 9, my pick, 2026-10-03)

Slugs `beveridge-*`.

| Work | Status | Where |
|---|---|---|
| Theological Works, 12 vols (Oxford: Parker, 1842-48, Library of Anglo-Catholic Theology); vols 11-12 in Latin | have-raw | IA (identifiers in the shelf) |


## W. G. T. Shedd (round 9, my pick, 2026-10-03)

Slugs `shedd-*`.

| Work | Status | Where |
|---|---|---|
| Dogmatic Theology, 2 vols (New York: Scribner, 1888) and vol. 3, supplement (1894) | have-raw | IA (identifiers in the shelf) |
| A History of Christian Doctrine, 2 vols (New York: Scribner, 1863; vol. 2 an 1868 printing) | have-raw | IA |


## J. B. Lightfoot (round 10, my pick, 2026-10-03)

Slugs `lightfoot-*`.

| Work | Status | Where |
|---|---|---|
| The Apostolic Fathers (tr. Lightfoot) | have-clean | CCEL |
| St. Paul's Epistles to the Colossians and to Philemon | have-clean | Gutenberg 50857 |
| Essays on the Work Entitled Supernatural Religion | have-clean | Gutenberg 18191 |
| Sermons | have-clean | Gutenberg 37527 |
| Saint Paul's Epistle to the Galatians (London: Macmillan, 1890) | have-raw | IA (identifier in the shelf) |
| Saint Paul's Epistle to the Philippians (London: Macmillan, 1898) | have-raw | IA |


## B. F. Westcott (round 10, my pick, 2026-10-03)

Slugs `westcott-*`.

| Work | Status | Where |
|---|---|---|
| The Gospel according to St. John: the Greek text, 2 vols (London: Murray, 1908) | have-raw | IA (identifiers in the shelf) |
| The Gospel according to St. John: the Authorised Version (London: Murray, 1892) | have-raw | IA |
| The Epistles of St. John: the Greek text (London: Macmillan, 1883) | have-raw | IA |
| The Epistle to the Hebrews: the Greek text (London: Macmillan, 1889) | have-raw | IA |
| A General Survey of the History of the Canon of the New Testament (London: Macmillan, 1896) | have-raw | IA |


## R. C. Trench (round 10, my pick, 2026-10-03)

Slugs `trench-*`.

| Work | Status | Where |
|---|---|---|
| On the Study of Words | have-clean | Gutenberg 6480 |
| English Past and Present | have-clean | Gutenberg 20900 |
| A Select Glossary of English Words Used Formerly in Senses Different from Their Present | have-clean | Gutenberg 70210 |
| Proverbs and Their Lessons | have-clean | Gutenberg 56504 |
| Synonyms of the New Testament (London: Kegan Paul, 1901) | have-raw | IA (identifier in the shelf) |
| Notes on the Parables of Our Lord (New York: Appleton; catalogued 1855) | have-raw | IA |
| Notes on the Miracles of Our Lord (New York: Appleton, 1883) | have-raw | IA |


## John Brown of Edinburgh (round 10, my pick, 2026-10-03)

Slugs `jbrowne-*` (John Brown of Haddington, his grandfather, is `brown-*` on his own shelf).

| Work | Status | Where |
|---|---|---|
| Discourses and Sayings of Our Lord Jesus Christ, 2 vols (New York: Carter, 1854) | have-raw | IA (identifiers in the shelf) |
| Analytical Exposition of the Epistle to the Romans (New York: Carter, 1857) | have-raw | IA |
| Expository Discourses on the First Epistle of Peter (New York: Carter; catalogued 1855) | have-raw | IA |


## F. W. Robertson (round 10, my pick, 2026-10-03)

Slugs `fwrobertson-*`.

| Work | Status | Where |
|---|---|---|
| Sermons Preached at Brighton, third series | have-clean | Gutenberg 16645 |
| Sermons Preached at Brighton, 4 vols (London: H. S. King, 1875) | have-raw | IA (identifiers in the shelf) |


## John Eadie (round 10, my pick, 2026-10-03)

Slugs `eadie-*`.

| Work | Status | Where |
|---|---|---|
| Commentary on the Greek Text of Ephesians (Edinburgh: T. and T. Clark, 1883) | have-raw | IA (identifier in the shelf) |
| Commentary on the Greek Text of Galatians (Edinburgh: T. and T. Clark, 1869) | have-raw | IA |
| Commentary on the Greek Text of Thessalonians (London: Macmillan, 1877) | pending | archive.org errors |
| Commentary on the Greek Text of Philippians | excluded | only copy found is a 1977 reprint |


## Henry Alford (round 10, my pick, 2026-10-03)

Slugs `alford-*`.

| Work | Status | Where |
|---|---|---|
| The Greek Testament, vols 1-2 (London: Rivington; catalogued 1849-56) | have-raw | IA (identifiers in the shelf) |
| The Greek Testament, vol. 4 (Boston: Lee and Shepard; catalogued 1874) | have-raw | IA |
| The Greek Testament, vol. 3 | pending | archive.org errors |


## John Keble (round 10, my pick, 2026-10-03)

Slugs `keble-*`.

| Work | Status | Where |
|---|---|---|
| The Christian Year (verse) | have-clean | CCEL |
| National Apostasy (the Assize Sermon, 1833) | have-clean | Gutenberg 49112 |
| Sermons, Academical and Occasional (Oxford: Parker, 1847) | have-raw | IA (identifier in the shelf) |
| Occasional Papers and Reviews (Oxford: Parker, 1877) | have-raw | IA |
| Sermons for the Christian Year (1875-80, 11 vols) | not shelved yet | |


## E. B. Pusey (round 10, my pick, 2026-10-03)

Slugs `pusey-*`.

| Work | Status | Where |
|---|---|---|
| The Minor Prophets, with a Commentary (Oxford: Parker; catalogued 1860) | have-raw | IA (identifier and text file name in the shelf) |
| Daniel the Prophet: Nine Lectures (Oxford: Parker, 1868) | have-raw | IA |
| Lenten Sermons (Oxford: Parker, 1874) | have-raw | IA |
| Nine Sermons Preached before the University of Oxford (1879) | pending | no text file |


## H. P. Liddon (round 10, my pick, 2026-10-03)

Slugs `liddon-*`.

| Work | Status | Where |
|---|---|---|
| The Divinity of Our Lord and Saviour Jesus Christ (Bampton Lectures) (London: Rivingtons, 1867) | have-raw | IA (identifiers in the shelf) |
| Easter in St. Paul's (Longmans, 1897 printing) | have-raw | IA |
| Advent in St. Paul's (Longmans, 1906 printing) | have-raw | IA |
| Passiontide Sermons (Longmans, 1891) | have-raw | IA |
| Clerical Life and Work (Longmans, 1895) | have-raw | IA |
| Christmastide in St. Paul's | not shelved | the copy tried was refused |


## A. A. Hodge (round 10, my pick, 2026-10-03)

Slugs `aa-hodge-*`.

| Work | Status | Where |
|---|---|---|
| Outlines of Theology, rewritten and enlarged (New York: Carter, 1879) | have-raw | IA (identifiers in the shelf) |
| A Commentary on the Confession of Faith (1885 new edition of the 1869 book) | have-raw | IA |
| The Atonement (Presbyterian Board, 1867) | have-raw | IA |
| Popular Lectures on Theological Themes (Presbyterian Board, 1887) | have-raw | IA |
| The Life of Charles Hodge (Scribner, 1880) | have-raw | IA |
| Outlines of Theology, first edition (1860) | alternate | IA |


## J. A. Alexander (round 10, my pick, 2026-10-03)

Slugs `ja-alexander-*`. The text layers carry no Hebrew or Greek characters at all.

| Work | Status | Where |
|---|---|---|
| The Earlier Prophecies of Isaiah (Wiley and Putnam, 1846) | have-raw | IA (identifiers in the shelf) |
| The Later Prophecies of Isaiah (Wiley and Putnam, 1847) | have-raw | IA |
| The Psalms Translated and Explained (Baker and Scribner, 1850), vols 1-3 | have-raw | IA |
| The Acts of the Apostles Explained (Scribner, 1857), vols 1-2 | have-raw | IA |
| The Gospel according to Mark Explained (Scribner, 1858) | have-raw | IA |
| The Gospel according to Matthew Explained (Scribner, title page 1861, preface December 1860) | have-raw | IA |
| Notes on New Testament Literature and Ecclesiastical History (Scribner, 1861) | have-raw | IA |
| Sermons (Scribner, 1860), vols 1-2 | have-raw | IA |
| Essays on the Primitive Church Offices (1851) | pending | the copy tried was refused |
| Isaiah Translated and Explained, the abridgement (1851) | alternate | IA |
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
| The Works of Plato, vol. 1 of 6 (Bohn, 1848) | Henry Cary | `plato-bohn-cary-v1-pg` | have (PG 78618) |
| The Works of Plato, vol. 2 of 6 (Bohn, 1849) | Henry Davis | `plato-bohn-davis-v2-pg` | have (PG 79398) |
| The Works of Plato, a new and literal version, vol. 1: Apology, Crito, Phaedo, Gorgias, Protagoras, Phaedrus, Theaetetus, Euthyphron, Lysis (Bohn, 1848) | Henry Cary | `plato-bohn-v1` | have-raw (IA `theworksofplato01platiala`) |
| The Works of Plato, a new and literal version, vol. 2: Republic, Timaeus, Critias (Bohn, 1849) | Henry Davis | `plato-bohn-v2` | have-raw (IA `worksofplatonewl02platiala`) |
| The Works of Plato, a new and literal version, vol. 3: Meno, Euthydemus, Sophist, Statesman, Cratylus, Parmenides, Banquet (Bohn, 1850) | George Burges | `plato-bohn-v3` | have-raw (IA `theworksofplato03platiala`) |
| The Works of Plato, a new and literal version, vol. 4: Philebus, Hippias Minor, Rivals, Charmides, Ion, Hipparchus, Laches, Alcibiades I-II, Minos, Menexenus, Clitopho, Hippias Major, Theages, Epistles (Bohn, 1851) | George Burges | `plato-bohn-v4` | have-raw (IA `b29340986_0004`) |
| The Works of Plato, a new and literal version, vol. 5: The Laws (Bohn, 1852) | George Burges | `plato-bohn-v5` | have-raw (IA `worksofplatonew05platiala`) |
| The Works of Plato, a new and literal version, vol. 6: the doubtful works, with lives and introductions (Bohn, 1854) | George Burges | `plato-bohn-v6` | have-raw (IA `worksofplatonewl06platiala`) |
| The Works of Plato, viz. his Fifty-Five Dialogues and Twelve Epistles, vol. 1 (London, 1804) | Thomas Taylor (nine dialogues by Floyer Sydenham) | `plato-taylor-1804-v1` | have-raw (IA `vol1worksofplato00plat`) |
| The Works of Plato, viz. his Fifty-Five Dialogues and Twelve Epistles, vol. 2 (London, 1804) | Thomas Taylor (nine dialogues by Floyer Sydenham) | `plato-taylor-1804-v2` | have-raw (IA `vol2worksofplato00plat`) |
| The Works of Plato, viz. his Fifty-Five Dialogues and Twelve Epistles, vol. 3 (London, 1804) | Thomas Taylor (nine dialogues by Floyer Sydenham) | `plato-taylor-1804-v3` | have-raw (IA `vol3worksofplato00plat`) |
| The Works of Plato, viz. his Fifty-Five Dialogues and Twelve Epistles, vol. 4 (London, 1804) | Thomas Taylor (nine dialogues by Floyer Sydenham) | `plato-taylor-1804-v4` | have-raw (IA `vol4worksofplato00plat`) |
| The Works of Plato, viz. his Fifty-Five Dialogues and Twelve Epistles, vol. 5 (London, 1804) | Thomas Taylor (nine dialogues by Floyer Sydenham) | `plato-taylor-1804-v5` | have-raw (IA `vol5worksofplato00plat`) |
| The Prose Works of Percy Bysshe Shelley, vol. 2 (ed. R. H. Shepherd, 1888): The Banquet, Ion, Menexenus, with Shelley's essay On the Symposium | Percy Bysshe Shelley | `plato-shelley-prose-works-v2` | have (PG 67926) |
| Euthyphro | Harold North Fowler (Loeb, 1914) | `plato-perseus-fowler-euthyphro` | have (Perseus TEI `tlg0059.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |
| Apology | Harold North Fowler (Loeb, 1914) | `plato-perseus-fowler-apology` | have (Perseus TEI `tlg0059.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |
| Crito | Harold North Fowler (Loeb, 1914) | `plato-perseus-fowler-crito` | have (Perseus TEI `tlg0059.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |
| Phaedo | Harold North Fowler (Loeb, 1914) | `plato-perseus-fowler-phaedo` | have (Perseus TEI `tlg0059.tlg004.perseus-eng2`; markup CC BY-SA 4.0) |
| Cratylus | Harold North Fowler (Loeb, 1926) | `plato-perseus-fowler-cratylus` | have (Perseus TEI `tlg0059.tlg005.perseus-eng2`; markup CC BY-SA 4.0) |
| Theaetetus | Harold North Fowler (Loeb, 1921) | `plato-perseus-fowler-theaetetus` | have (Perseus TEI `tlg0059.tlg006.perseus-eng2`; markup CC BY-SA 4.0) |
| Sophist | Harold North Fowler (Loeb, 1921) | `plato-perseus-fowler-sophist` | have (Perseus TEI `tlg0059.tlg007.perseus-eng2`; markup CC BY-SA 4.0) |
| Statesman | Harold North Fowler (Loeb, 1925) | `plato-perseus-fowler-statesman` | have (Perseus TEI `tlg0059.tlg008.perseus-eng2`; markup CC BY-SA 4.0) |
| Parmenides | Harold North Fowler (Loeb, 1926) | `plato-perseus-fowler-parmenides` | have (Perseus TEI `tlg0059.tlg009.perseus-eng2`; markup CC BY-SA 4.0) |
| Philebus | Harold North Fowler (Loeb, 1925) | `plato-perseus-fowler-philebus` | have (Perseus TEI `tlg0059.tlg010.perseus-eng2`; markup CC BY-SA 4.0) |
| Symposium | W. R. M. Lamb (Loeb, 1925) | `plato-perseus-lamb-symposium` | have (Perseus TEI `tlg0059.tlg011.perseus-eng2`; markup CC BY-SA 4.0) |
| Phaedrus | Harold North Fowler (Loeb, 1914) | `plato-perseus-fowler-phaedrus` | have (Perseus TEI `tlg0059.tlg012.perseus-eng2`; markup CC BY-SA 4.0) |
| Alcibiades I | W. R. M. Lamb (Loeb, 1927) | `plato-perseus-lamb-alcibiades-i` | have (Perseus TEI `tlg0059.tlg013.perseus-eng2`; markup CC BY-SA 4.0) |
| Alcibiades II | W. R. M. Lamb (Loeb, 1927) | `plato-perseus-lamb-alcibiades-ii` | have (Perseus TEI `tlg0059.tlg014.perseus-eng2`; markup CC BY-SA 4.0) |
| Hipparchus | W. R. M. Lamb (Loeb, 1927) | `plato-perseus-lamb-hipparchus` | have (Perseus TEI `tlg0059.tlg015.perseus-eng2`; markup CC BY-SA 4.0) |
| Lovers | W. R. M. Lamb (Loeb, 1927) | `plato-perseus-lamb-lovers` | have (Perseus TEI `tlg0059.tlg016.perseus-eng2`; markup CC BY-SA 4.0) |
| Theages | W. R. M. Lamb (Loeb, 1927) | `plato-perseus-lamb-theages` | have (Perseus TEI `tlg0059.tlg017.perseus-eng2`; markup CC BY-SA 4.0) |
| Charmides | W. R. M. Lamb (Loeb, 1927) | `plato-perseus-lamb-charmides` | have (Perseus TEI `tlg0059.tlg018.perseus-eng2`; markup CC BY-SA 4.0) |
| Laches | W. R. M. Lamb (Loeb, 1924) | `plato-perseus-lamb-laches` | have (Perseus TEI `tlg0059.tlg019.perseus-eng2`; markup CC BY-SA 4.0) |
| Lysis | W. R. M. Lamb (Loeb, 1925) | `plato-perseus-lamb-lysis` | have (Perseus TEI `tlg0059.tlg020.perseus-eng2`; markup CC BY-SA 4.0) |
| Euthydemus | W. R. M. Lamb (Loeb, 1924) | `plato-perseus-lamb-euthydemus` | have (Perseus TEI `tlg0059.tlg021.perseus-eng2`; markup CC BY-SA 4.0) |
| Protagoras | W. R. M. Lamb (Loeb, 1924) | `plato-perseus-lamb-protagoras` | have (Perseus TEI `tlg0059.tlg022.perseus-eng2`; markup CC BY-SA 4.0) |
| Gorgias | W. R. M. Lamb (Loeb, 1925) | `plato-perseus-lamb-gorgias` | have (Perseus TEI `tlg0059.tlg023.perseus-eng2`; markup CC BY-SA 4.0) |
| Meno | W. R. M. Lamb (Loeb, 1924) | `plato-perseus-lamb-meno` | have (Perseus TEI `tlg0059.tlg024.perseus-eng2`; markup CC BY-SA 4.0) |
| Greater Hippias | Harold North Fowler (Loeb, 1926) | `plato-perseus-fowler-greater-hippias` | have (Perseus TEI `tlg0059.tlg025.perseus-eng2`; markup CC BY-SA 4.0) |
| Lesser Hippias | Harold North Fowler (Loeb, 1926) | `plato-perseus-fowler-lesser-hippias` | have (Perseus TEI `tlg0059.tlg026.perseus-eng2`; markup CC BY-SA 4.0) |
| Ion | W. R. M. Lamb (Loeb, 1925) | `plato-perseus-lamb-ion` | have (Perseus TEI `tlg0059.tlg027.perseus-eng2`; markup CC BY-SA 4.0) |
| Menexenus | R. G. Bury (Loeb, 1929) | `plato-perseus-bury-menexenus` | have (Perseus TEI `tlg0059.tlg028.perseus-eng2`; markup CC BY-SA 4.0) |
| Cleitophon | R. G. Bury (Loeb, 1929) | `plato-perseus-bury-cleitophon` | have (Perseus TEI `tlg0059.tlg029.perseus-eng2`; markup CC BY-SA 4.0) |
| Timaeus | R. G. Bury (Loeb, 1929) | `plato-perseus-bury-timaeus` | have (Perseus TEI `tlg0059.tlg031.perseus-eng2`; markup CC BY-SA 4.0) |
| Critias | R. G. Bury (Loeb, 1929) | `plato-perseus-bury-critias` | have (Perseus TEI `tlg0059.tlg032.perseus-eng2`; markup CC BY-SA 4.0) |
| Minos | W. R. M. Lamb (Loeb, 1927) | `plato-perseus-lamb-minos` | have (Perseus TEI `tlg0059.tlg033.perseus-eng2`; markup CC BY-SA 4.0) |
| Laws | R. G. Bury (Loeb, 1926) | `plato-perseus-bury-laws` | have (Perseus TEI `tlg0059.tlg034.perseus-eng2`; markup CC BY-SA 4.0) |
| Epinomis | W. R. M. Lamb (Loeb, 1927) | `plato-perseus-lamb-epinomis` | have (Perseus TEI `tlg0059.tlg035.perseus-eng2`; markup CC BY-SA 4.0) |
| Letters | R. G. Bury (Loeb, 1929) | `plato-perseus-bury-letters` | have (Perseus TEI `tlg0059.tlg036.perseus-eng2`; markup CC BY-SA 4.0) |
| The Republic of Plato, translated into English with an analysis and notes (Golden Treasury Series; Macmillan, 1892 printing; first printed 1852) | John Llewelyn Davies and David James Vaughan | `plato-davies-vaughan-republic-1892` | have-raw (IA `republicofplato13plat`) |
| The Platonic Dialogues for English Readers, vol. I: Dialogues of the Socratic School and those referring to the Trial and Death of Socrates, second edition (Macmillan, 1860; abridged in parts, by the translator's own preface) | William Whewell | `plato-whewell-v1-1860` | have-raw (IA `in.ernet.dli.2015.100023`) |
| The Platonic Dialogues for English Readers, vol. II: Antisophist Dialogues (Macmillan, 1860; abridged in parts) | William Whewell | `plato-whewell-v2-1860` | have-raw (IA `platonicdialogu04whewgoog`) |
| The Platonic Dialogues for English Readers, vol. III: The Republic and the Timaeus (Macmillan, 1861; abridged in parts) | William Whewell | `plato-whewell-v3-1861` | have-raw (IA `platonicdialogu05whewgoog`) |
| The Republic of Plato in Ten Books, translated from the Greek (Everyman's Library; first issue of this edition 1906, this scan the 1919 reprint; Spens's translation first published 1763) | Harry Spens | `plato-spens-republic-everyman` | have-raw (IA `republicofplatoi00platuoft`) |

Pending (wishlist):

- Held now (2026-10-02): the complete Bohn *Works of Plato* (Cary, Davis, Burges, 6 vols., 1848-54), which carries the dialogues Jowett left out (Greater Hippias, Hipparchus, Minos, Rivals, Theages, Clitophon, Epinomis, the Epistles, Definitions and the other doubtful works). Vols. 1-2 are clean from Gutenberg as well. Whether a second translator belongs on this shelf or its own is still Adam's call; moving the rows is cheap.
- The Republic, Jowett's separate 3rd ed. with marginal analysis and index (PG 55201): an alternate witness of the Republic.
- The Dialogues of Plato, 1892, vol. 2 as a clean Gutenberg transcription (PG 76464, 2025): the other four volumes are not on Gutenberg yet; when they are, that is the cleanest collected edition.
- Shelley's Banquet (Symposium), Ion and Menexenus are held above (Prose Works vol. 2, PG 67926). Thomas Taylor's complete Plato (1804, with Sydenham's nine dialogues) is held above, 5 vols.
- Perseus serves 36 English Plato texts (Loeb: Fowler, Lamb, Shorey, Bury). The 35 by Fowler, Lamb and Bury (1914-29) are held above as alternate witnesses; Shorey's Republic (1935-37 file) is excluded.

Excluded: PG 150 (duplicate Republic, shorter introduction), PG 19840 (Euthyphro; serves a 404), PG 29441 (an index page), PG 13726 (Cary, not Jowett).; Shorey's Loeb Republic (Perseus file dated 1935-37)

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
| De Mundo (Oxford, Clarendon Press, 1914; the separate issue later bound into vol. III) | E. S. Forster | `aristotle-forster-de-mundo-1914` | have-raw (IA `demundoarisrich`) |
| The Poetics of Aristotle | S. H. Butcher | `aristotle-butcher-poetics-pg` | have (PG 1974) |
| Aristotle on the Art of Poetry (Oxford, 1920), preface by Gilbert Murray | Ingram Bywater | `aristotle-bywater-poetics-pg` | have (PG 6763) |
| Politics: A Treatise on Government | William Ellis (1776) | `aristotle-ellis-politics-pg` | held elsewhere: PG 6762 is already held on pipeline/adler_shelf.json as aristotle-politics |
| The Nicomachean Ethics of Aristotle (Everyman), introduction by J. A. Smith | D. P. Chase; PG names no translator, identified by collating against the 1915 Everyman printing titled 'Translated by D. P. Chase' (IA nicomacheanethic00arisuoft): 167 of 200 sampled 8-word runs match | `aristotle-chase-ethics-pg` | held elsewhere: PG 8438 is already held on pipeline/adler_shelf.json as aristotle-ethics (labelled 'tr. Chase', which the collation agre |
| The Athenian Constitution | Sir Frederic G. Kenyon (1891) | `aristotle-kenyon-athenian-constitution-pg` | have (PG 26095) |
| Aristotle's History of Animals, in ten books (Bohn, 1862) | Richard Cresswell | `aristotle-cresswell-history-of-animals-pg` | have (PG 59058) |
| The Categories (the Oxford translation, also in vol. I above) | E. M. Edghill | `aristotle-edghill-categories-pg` | held elsewhere: PG 2412 is Edghill's Categories, the same Oxford translation held in aristotle-ross-v01 (Works vol. I, 1928) |
| The Nicomachean Ethics of Aristotle (Everyman's Library, introduction by J. A. Smith) | unnamed in the Gutenberg file | `aristotle-everyman-ethics-pg` | held (PG 8438 is aristotle-ethics on the Adler shelf; not refetched) |
| The Nicomachean Ethics of Aristotle, translated with notes, analytical introduction and questions (Bohn's Classical Library; London: Henry G. Bohn, 1850) | R. W. Browne | `aristotle-browne-ethics-1850` | have-raw (IA `nicomacheanethi12arisgoog`) |
| Aristotle's Treatise on Rhetoric, literally translated, with Hobbes's analysis; and The Poetic of Aristotle, literally translated (Bohn's Classical Library; London: Henry G. Bohn, new edition, 1857) | anonymous literal translation of the Rhetoric, edited by Theodore Alois Buckley; the Poetic by Theodore Buckley | `aristotle-bohn-rhetoric-poetic-1857` | have-raw (IA `treatiseonrheto00aris`) |
| The Organon, or Logical Treatises, of Aristotle, with the Introduction of Porphyry, literally translated, vol. I (Bohn; London: Henry G. Bohn, 1853) | Octavius Freire Owen | `aristotle-owen-organon-1853-v1` | have-raw (IA `organonorlogicalt01aris`) |
| The Organon, or Logical Treatises, of Aristotle, with the Introduction of Porphyry, literally translated, vol. II (Bohn; London: Henry G. Bohn, MDCCCLIII) | Octavius Freire Owen | `aristotle-owen-organon-1853-v2` | have-raw (IA `organonorlogica04porpgoog`) |
| The Metaphysics of Aristotle, translated from the Greek, with copious notes (London: printed for the author, 1801) | Thomas Taylor | `aristotle-taylor-metaphysics-1801` | have-raw (IA `metaphysicsofari00aris`) |
| The Nicomachean Ethics of Aristotle, translated with an analysis and critical notes (London: Macmillan, 1892) | J. E. C. Welldon | `aristotle-welldon-ethics-1892` | have-raw (IA `nicomacheanethic1892aris`) |
| The Rhetoric of Aristotle, translated with an analysis and critical notes (London: Macmillan, 1886) | J. E. C. Welldon | `aristotle-welldon-rhetoric-1886` | have-raw (IA `rhetoricofaristo00aristot`) |
| The Politics of Aristotle, translated with an analysis and critical notes (London: Macmillan, 1901 printing; first published 1883) | J. E. C. Welldon | `aristotle-welldon-politics-1901` | have-raw (IA `bwb_KU-767-069`) |
| The Nicomachean Ethics of Aristotle (London: C. Kegan Paul, 1881) | F. H. Peters | `aristotle-peters-ethics-1881` | have-raw (IA `nicomacheanethi00petegoog`) |
| Nicomachean Ethics | Harris Rackham (1926) | `aristotle-perseus-rackham-nicomachean-ethics` | have (Perseus TEI `tlg0086.tlg010.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): genuine pre-1931 separate issues of Meteorologica (1923) and Parva Naturalia (1908), which are PD now (no scan found yet; De Mundo, 1914, is held above); R. D. Hicks's De Anima (1907, Greek facing); a clean proofread Nicomachean Ethics (Ross) from Gutenberg if one appears.

Aristotle cross-ref: the Adler shelf already holds `aristotle-ethics` (Chase, PG 8438) and `aristotle-politics` (Jowett, PG 6762, the same translation as the Politics in Oxford vol. X).

Excluded: `meteorologica00aris` (catalogued as the 1923 separate issue, but the scan is all of vol. III and carries the 1931 De Anima); duplicate Toronto scans of vols. X–XII; Perseus English (Loeb) not used; `worksofaristotle00unse` (*Aristotle's Masterpiece*, falsely ascribed).

## Hesiod

Shelf: `pipeline/hesiod_shelf.json`. Hugh G. Evelyn-White, prose (Loeb, 1914), PD. Gutenberg, English only. Evelyn-White prints the line references in the prose, "(ll. 1-25)", 510 of them, so a line-level citation scheme is possible later; the trial conversion gives paragraph units only.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Works and Days; Theogony; Shield of Heracles; Catalogues of Women and other fragments; with the Homeric Hymns, Epigrams, Contest of Homer and Hesiod, and Homerica (one volume) | Evelyn-White | `hesiod-evelyn-white` | have (PG 348) |
| The Remains of Hesiod the Ascraean, Including the Shield of Hercules | Charles Abraham Elton (with George Chapman's Works and Days) | `hesiod-elton` | have (PG 66350) |
| The Works of Hesiod, translated from the Greek (London: N. Blandford, 1728), vol. 1 | Thomas Cooke ('Mr. Cooke' on the title page) | `hesiod-cooke-1728-v1` | have-raw (IA `bim_eighteenth-century_the-works-of-hesiod-tran_hesiod_1728_1`) |
| The Works of Hesiod, translated from the Greek (London: N. Blandford, 1728), vol. 2 | Thomas Cooke ('Mr. Cooke' on the title page) | `hesiod-cooke-1728-v2` | have-raw (IA `bim_eighteenth-century_the-works-of-hesiod-tran_hesiod_1728_2`) |
| Hesiod: the Poems and Fragments done into English Prose (Oxford: Clarendon Press, 1908) | A. W. Mair | `hesiod-mair-1908` | have-raw (IA `hesiodpoemsandf01mairgoog`) |
| The Works of Hesiod, Callimachus, and Theognis, literally translated into English prose, with the metrical translations of Elton, Tytler and Frere appended (Bohn's Classical Library, MDCCCLVI) | J. Banks (prose); verse by Charles Abraham Elton, James Tytler and John Hookham Frere | `hesiod-banks-bohn-1856` | have-raw (IA `workshesiodcall01frergoog`) |

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
| Metamorphoses, vol. 1: Books I-VIII (Loeb, 1916) | Frank Justus Miller | `ovid-miller-metamorphoses-v1` | held: the scan is a 1970s reprint of the 1921 second edition carrying an added bibliography (items of 1963 to the 1970s), which is not public domain; not fetched (see `_held`) |
| Metamorphoses, vol. 2: Books IX-XV (Loeb, 1916) | Frank Justus Miller | `ovid-miller-metamorphoses-v2` | have-raw (IA `metamorphoseswit02oviduoft`) |
| Heroides and Amores (Loeb, 1914) | Grant Showerman | `ovid-showerman-heroides-amores` | have-raw (IA `heroidesamores00ovid`) |
| Tristia, Ex Ponto (Loeb, 1924) | Arthur Leslie Wheeler | `ovid-wheeler-tristia-ponto` | have-raw (IA `bwb_W9-CQC-386`) |
| Ovid's Metamorphosis Englished, mythologized and represented in figures (Oxford, 1632) | George Sandys (verse, 1632) | `ovid-sandys-1632` | have-raw (IA `ovidsmetamorphos00ovid_0`) |
| Metamorphoses | Brookes More (blank verse, 1922) | `ovid-perseus-more-metamorphoses` | have (Perseus TEI `phi0959.phi006.perseus-eng3`; markup CC BY-SA 4.0) |
| Amours | translators not named (1855) | `ovid-perseus-1855-amours` | have (Perseus TEI `phi0959.phi001.perseus-eng2`; markup CC BY-SA 4.0) |
| The Art of Beauty | translators not named (1855) | `ovid-perseus-1855-art-of-beauty` | have (Perseus TEI `phi0959.phi003.perseus-eng2`; markup CC BY-SA 4.0) |
| The Art of Love | translators not named (1855) | `ovid-perseus-1855-art-of-love` | have (Perseus TEI `phi0959.phi004.perseus-eng2`; markup CC BY-SA 4.0) |
| The Remedy of Love | translators not named (1855) | `ovid-perseus-1855-remedy-of-love` | have (Perseus TEI `phi0959.phi005.perseus-eng2`; markup CC BY-SA 4.0) |
| The Epistles (Heroides) | translators not named (1813) | `ovid-perseus-1813-epistles` | have (Perseus TEI `phi0959.phi002.perseus-eng2`; markup CC BY-SA 4.0) |
| The Art of Love, and Other Poems: On Painting the Face, Ars Amatoria, Remedia Amoris, Nux, Ibis, Halieuticon, Consolatio ad Liviam (Loeb; London: Heinemann, New York: Putnam, MCMXXIX; Latin facing) | J. H. Mozley | `ovid-mozley-art-of-love-1929` | have-raw (IA `ovidartofloveoth0000unse`) |

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
| The Aeneid of Virgil, translated into Scottish verse (Eneados, 1513), vol. 1 (Bannatyne Club, Edinburgh, 1839) | Gavin Douglas | `virgil-douglas-eneados-v1` | have-raw (IA `aeneidofvirgiltr01virguoft`) |
| The Aeneid of Virgil, translated into Scottish verse (Eneados, 1513), vol. 2 (Bannatyne Club, Edinburgh, 1839) | Gavin Douglas | `virgil-douglas-eneados-v2` | have-raw (IA `aeneidofvirgil6402virguoft`) |
| The First Four Books of the Aeneid of Virgil, in English heroic verse (1582; Edinburgh reprint, 1836) | Richard Stanyhurst | `virgil-stanyhurst-1836` | have-raw (IA `firstfourbooksn00maidgoog`) |
| The Works of Virgil, literally translated into English prose by Davidson, new edition revised by Theodore Alois Buckley (New York: Harper, 1874) | Joseph Davidson, revised by Theodore Alois Buckley | `virgil-davidson-buckley-1874` | have-raw (IA `worksvirgil03virggoog`) |
| The Works of Virgil rendered into English Prose (Globe Edition; Macmillan, 1871) | James Lonsdale and Samuel Lee | `virgil-lonsdale-lee-1871` | have-raw (IA `worksofvirgilren00virg`) |
| The Works of Virgil, translated, vol. I (London, MDCCCXLIX): first four Pastorals, Georgics and first four Aeneids by Rann Kennedy; the rest by Charles Rann Kennedy | Rann Kennedy and Charles Rann Kennedy | `virgil-kennedy-1849-v1` | have-raw (IA `worksofvirgiltra0001char`) |
| The Works of Virgil, translated, vol. II (London, MDCCCXLIX) | Rann Kennedy and Charles Rann Kennedy | `virgil-kennedy-1849-v2` | have-raw (IA `worksofvirgiltra0002char`) |
| The Works of Virgil in English Verse, vol. I of four: the Eclogues and Georgics by Joseph Warton, with the Life and two essays (London: R. and J. Dodsley, MDCCLXIII) | Joseph Warton | `virgil-pitt-warton-1763-v1` | have-raw (IA `worksvirgilinen01attegoog`) |
| The Works of Virgil in English Verse, vol. III of four: the Aeneid, Books V-VIII, by Christopher Pitt, with Warburton's dissertation on the sixth book (Dodsley, MDCCLXIII) | Christopher Pitt | `virgil-pitt-warton-1763-v3` | have-raw (IA `worksvirgilinen00attegoog`) |

Pending (wishlist): none known. Gavin Douglas's Eneados (1513, Scots) is held above in the Bannatyne Club edition (1839).

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
| The Odyssey of Homer done into English Verse (London: Reeves & Turner, 1887) | William Morris | `homer-morris-odyssey-1887` | have-raw (IA `odysseyofhomer00homeuoft`) |
| The Odyssey of Homer, translated into English prose (preface dated Cambridge, February 1891) | George Herbert Palmer | `homer-palmer-odyssey-1891` | have-raw (IA `odysseyhomer02palmgoog`) |
| The Odyssey of Homer translated into English Verse in the Spenserian Stanza, vol. I, books I-XII (Blackwood, 1861) | Philip Stanhope Worsley | `homer-worsley-odyssey-1861-v1` | have-raw (IA `odysseyhomer04worsgoog`) |
| The Odyssey of Homer translated into English Verse in the Spenserian Stanza, vol. II, books XIII-XXIV (Blackwood, 1862) | Philip Stanhope Worsley | `homer-worsley-odyssey-1862-v2` | have-raw (IA `odysseyhomer01worsgoog`) |
| The Odyssey of Homer in English Verse, third edition (Macmillan, 1904) | Arthur S. Way | `homer-way-odyssey-1904` | have-raw (IA `odysseyofhomerin00homerich`) |
| The Iliad of Homer faithfully translated into unrhymed English metre (London: Walton and Maberly, 1856; the title-page date OCRs poorly) | Francis William Newman | `homer-newman-iliad-1856` | have-raw (IA `iliadhomerfaith00newmgoog`) |
| The Iliad of Homer translated into English Verse in the Spenserian Stanza, vol. I, books I-XII (Blackwood, 1865) | Philip Stanhope Worsley | `homer-worsley-iliad-1865-v1` | have-raw (IA `iliadhomertrans00conigoog`) |
| The Iliad of Homer translated into English Verse in the Spenserian Stanza, vol. II, books XIII-XXIV (Blackwood, 1868) | John Conington | `homer-conington-iliad-1868-v2` | have-raw (IA `iliadhomertrans01conigoog`) |
| The Iliad of Homer done into English Verse, vol. I, books I-XII (Sampson Low, 1886) | Arthur S. Way | `homer-way-iliad-1886-v1` | have-raw (IA `iliadhomer01home`) |
| The Iliad of Homer done into English Verse, vol. II, books XIII-XXIV (Sampson Low, 1888) | Arthur S. Way | `homer-way-iliad-1888-v2` | have-raw (IA `iliaddoneintoen02homegoog`) |

Pending (wishlist): none known beyond the rows above.

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
| Aeschylus in English Verse, Part I: The Seven against Thebes, The Persians (London, 1906) | Arthur S. Way | `aeschylus-way-1906-part1` | have-raw (IA `cu31924087947051`) |
| Aeschylus in English Verse, Part II: Prometheus Bound, The Suppliant Maidens (London, 1907) | Arthur S. Way | `aeschylus-way-1907-part2` | have-raw (IA `cu31924087947069`) |
| Aeschylus in English Verse, Part III: Agamemnon, Choephoroe, Eumenides (London, 1908) | Arthur S. Way | `aeschylus-way-1908-part3` | have-raw (IA `aeschylusinengl04aescgoog`) |
| The Oresteia of Aeschylus translated into English Prose (London, 18 Bury Street, 1893) | Lewis Campbell | `aeschylus-campbell-oresteia-prose-1893` | have-raw (IA `oresteiaofaeschy00aescrich`) |
| The Plays of Aeschylus translated from a revised text (prose; London: George Bell, 1909) | Walter Headlam and C. E. S. Headlam | `aeschylus-headlam-plays-1909` | have-raw (IA `aeschylusplays00aesciala`) |
| The Oresteia of Aeschylus translated and explained (London: George Allen, 1900) | George C. W. Warr | `aeschylus-warr-oresteia-1900` | have-raw (IA `oresteiatranslat00aescuoft`) |
| Agamemnon | Herbert Weir Smyth (1926) | `aeschylus-perseus-smyth-agamemnon` | have (Perseus TEI `tlg0085.tlg005.perseus-eng3`; markup CC BY-SA 4.0) |
| Eumenides | Herbert Weir Smyth (1926) | `aeschylus-perseus-smyth-eumenides` | have (Perseus TEI `tlg0085.tlg007.perseus-eng2`; markup CC BY-SA 4.0) |
| Libation Bearers | Herbert Weir Smyth (1926) | `aeschylus-perseus-smyth-libation-bearers` | have (Perseus TEI `tlg0085.tlg006.perseus-eng2`; markup CC BY-SA 4.0) |
| Persians | Herbert Weir Smyth (1922) | `aeschylus-perseus-smyth-persians` | have (Perseus TEI `tlg0085.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |
| Prometheus Bound | Herbert Weir Smyth (1922) | `aeschylus-perseus-smyth-prometheus-bound` | have (Perseus TEI `tlg0085.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |
| Seven Against Thebes | Herbert Weir Smyth (1922) | `aeschylus-perseus-smyth-seven-against-thebes` | have (Perseus TEI `tlg0085.tlg004.perseus-eng2`; markup CC BY-SA 4.0) |
| Suppliant Maidens | Herbert Weir Smyth (1922) | `aeschylus-perseus-smyth-suppliant-maidens` | have (Perseus TEI `tlg0085.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): none here: Smyth's Loeb (1922-26) is on PR #7 as Perseus TEI.

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
| Rhesus | Gilbert Murray | `euripides-perseus-murray-rhesus` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Euripides, translated by R. Potter, vol. 1 (Valpy, 1832) | Robert Potter | `euripides-potter-v1` | have-raw (IA `euripides00pottgoog`) |
| Euripides, translated by R. Potter, vol. 2 (Valpy, 1832) | Robert Potter | `euripides-potter-v2` | have-raw (IA `euripides01pottgoog`) |
| Euripides, translated by R. Potter, vol. 3 (Valpy, 1832) | Robert Potter | `euripides-potter-v3` | have-raw (IA `euripides02pottgoog`) |
| The Tragedies of Euripides, vol. 2 (prose, Bohn, 1850) | Theodore Alois Buckley | `euripides-buckley-v2` | have-raw (IA `tragedieseuripi01eurigoog`) |

Pending (wishlist): Way's 1912 Loeb (Greek facing). Potter's Euripides is held complete in the 1832 Valpy reprint (3 vols.). Wodhull's Euripides is held complete from the 1809 Greek Tragic Theatre (vols. 3-5).

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
| Sophocles in English Verse, Part I: Oedipus the King, Oedipus at Kolonus, Antigone (London, 1909) | Arthur S. Way | `sophocles-way-1909-part1` | have-raw (IA `cu31924026676365`) |
| The Tragedies of Sophocles, translated into English prose (Cambridge, 1904) | Sir Richard C. Jebb | `sophocles-jebb-prose-1904` | have-raw (IA `tragediessophoc00jebbgoog`) |
| Sophocles translated into English Verse (London: Rivingtons, MDCCCLXXXIII) | Robert Whitelaw | `sophocles-whitelaw-1883` | have-raw (IA `sophoclestransla00sophuoft`) |
| The Tragedies of Sophocles translated into English Verse, vol. I (London: J. M. Richardson, 1824) | Thomas Dale | `sophocles-dale-1824-v1` | have-raw (IA `tragediesofsopho01soph_0`) |
| The Tragedies of Sophocles translated into English Verse, vol. II (London: J. M. Richardson, 1824) | Thomas Dale | `sophocles-dale-1824-v2` | have-raw (IA `tragediesofsopho02soph`) |

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
| Aristophanes: a Metrical Version of the Acharnians, the Knights and the Birds (Morley's Universal Library; 2nd ed., Routledge, 1887) | John Hookham Frere | `aristophanes-frere-morley` | have-raw (IA `aristophanesmetr00arisiala`) |
| The Comedies of Aristophanes, a new and literal translation, vol. I: Acharnians, Knights, Clouds, Wasps, Peace, Birds (Bohn; London: George Bell, 1887) | William James Hickie | `aristophanes-hickie-1887-v1` | have-raw (IA `comediesofaristo0001will`) |
| The Comedies of Aristophanes, vol. II: The Clouds, The Wasps (London: John Murray, 1822) | Thomas Mitchell | `aristophanes-mitchell-1822-v2` | have-raw (IA `comediesaristop00mitcgoog`) |
| The Comedies of Aristophanes, translated into familiar blank verse, vol. I (Oxford: D. A. Talboys; IA records 1837) | C. A. Wheelwright | `aristophanes-wheelwright-1837-v1` | have-raw (IA `comediesaristop01arisgoog`) |
| The Comedies of Aristophanes, translated into familiar blank verse, vol. II (Oxford: D. A. Talboys; IA records 1837) | C. A. Wheelwright | `aristophanes-wheelwright-1837-v2` | have-raw (IA `comediesofaristo02aris`) |

Pending (wishlist): B. B. Rogers's complete verse Aristophanes (1902-16; Greek facing). Frere's Frogs (the fourth play of his 1840 set) is not in the 1887 Morley volume held above. Hickie's Bohn vol. II (no IA text file) and Mitchell's vol. I (1820; no scan found).

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
| The History of Herodotus, translated from the Greek (London, 1737), vol. 1 (John Adams's copy) | Isaac Littlebury | `herodotus-littlebury-1737-v1` | have-raw (IA `historyofherodot01hero`) |
| The History of Herodotus, translated from the Greek (London, 1737), vol. 2 (John Adams's copy) | Isaac Littlebury | `herodotus-littlebury-1737-v2` | have-raw (IA `historyofherodot02hero`) |
| Herodotus, translated from the Greek, with notes, 4th ed., in four volumes (London: Rivington and others, 1821), vol. I | William Beloe | `herodotus-beloe-1821-v1` | have-raw (IA `india.history.resource.86416`) |
| Herodotus, translated from the Greek, with notes, 4th ed., in four volumes (London: Rivington and others, 1821), vol. II | William Beloe | `herodotus-beloe-1821-v2` | have-raw (IA `india.history.resource.86417`) |
| Herodotus, translated from the Greek, with notes, 4th ed., in four volumes (London: Rivington and others, 1821), vol. III | William Beloe | `herodotus-beloe-1821-v3` | have-raw (IA `india.history.resource.86418`) |
| Herodotus, translated from the Greek, with notes, 4th ed., in four volumes (London: Rivington and others, 1821), vol. IV | William Beloe | `herodotus-beloe-1821-v4` | have-raw (IA `india.history.resource.86419`) |
| Histories | A. D. Godley (1920-25; modernized by Perseus) | `herodotus-perseus-godley-histories` | have (Perseus TEI `tlg0016.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): none here: Godley's Loeb (1920-25) is on PR #7 as Perseus TEI.

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

Pending (wishlist): none known beyond the rows above.

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
| The Anabasis, or Expedition of Cyrus, and the Memorabilia of Socrates, literally translated (Bohn, 1875 printing) | J. S. Watson (geographical commentary by W. F. Ainsworth) | `xenophon-watson-anabasis-memorabilia` | have-raw (IA `anabasisorexped00xeno`) |
| The Cyropaedia, or Institution of Cyrus, and the Hellenics, literally translated (Bohn, 1855) | J. S. Watson and Henry Dale | `xenophon-watson-dale-cyropaedia-hellenics` | have-raw (IA `cyropaediaorins00xeno`) |
| Xenophon's Minor Works, literally translated (Bohn; 1914 stereotype reprint) | J. S. Watson | `xenophon-watson-minor-works` | have-raw (IA `xenophonsminorwo00xeno`) |
| Xenophon, vol. I: The Anabasis (Valpy's Family Classical Library, 1830) | Edward Spelman | `xenophon-spelman-anabasis-1830` | have-raw (IA `anabasis00coopgoog`) |
| Cyropaedia, or the Institution of Cyrus (London: Vernor and Hood, 1803) | Maurice Ashley | `xenophon-ashley-cyropaedia-1803` | have-raw (IA `cyropaediaorinst00xeno`) |
| Memorabilia | Edgar Carew Marchant (Loeb, 1923) | `xenophon-perseus-marchant-memorabilia` | have (Perseus TEI `tlg0032.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |
| Economics (Oeconomicus) | Edgar Carew Marchant (Loeb, 1923) | `xenophon-perseus-marchant-economics` | have (Perseus TEI `tlg0032.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |
| Banquet (Symposium) | Otis Johnson Todd (Loeb, 1923) | `xenophon-perseus-todd-banquet` | have (Perseus TEI `tlg0032.tlg004.perseus-eng2`; markup CC BY-SA 4.0) |
| Apology | Otis Johnson Todd (Loeb, 1923) | `xenophon-perseus-todd-apology` | have (Perseus TEI `tlg0032.tlg005.perseus-eng2`; markup CC BY-SA 4.0) |
| Hiero | Edgar Carew Marchant (Loeb, 1925) | `xenophon-perseus-marchant-hiero` | have (Perseus TEI `tlg0032.tlg008.perseus-eng2`; markup CC BY-SA 4.0) |
| Agesilaus | Edgar Carew Marchant (Loeb, 1925) | `xenophon-perseus-marchant-agesilaus` | have (Perseus TEI `tlg0032.tlg009.perseus-eng2`; markup CC BY-SA 4.0) |
| Constitution of the Lacedaemonians | Edgar Carew Marchant (Loeb, 1925) | `xenophon-perseus-marchant-constitution-of-the-lacedaemonians` | have (Perseus TEI `tlg0032.tlg010.perseus-eng2`; markup CC BY-SA 4.0) |
| Ways and Means | Edgar Carew Marchant (Loeb, 1925) | `xenophon-perseus-marchant-ways-and-means` | have (Perseus TEI `tlg0032.tlg011.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Cavalry Commander | Edgar Carew Marchant (Loeb, 1925) | `xenophon-perseus-marchant-on-the-cavalry-commander` | have (Perseus TEI `tlg0032.tlg012.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Art of Horsemanship | Edgar Carew Marchant (Loeb, 1925) | `xenophon-perseus-marchant-on-the-art-of-horsemanship` | have (Perseus TEI `tlg0032.tlg013.perseus-eng2`; markup CC BY-SA 4.0) |
| On Hunting | Edgar Carew Marchant (Loeb, 1925) | `xenophon-perseus-marchant-on-hunting` | have (Perseus TEI `tlg0032.tlg014.perseus-eng2`; markup CC BY-SA 4.0) |
| The Minor Works of Xenophon: Memoirs of Socrates, The Banquet, Hiero, Economics, translated from the Greek by several hands (London: Walker and others, 1813) | several hands: the Banquet by James Welwood, the Economics by R. Bradley; the Memoirs and Hiero unnamed in the volume | `xenophon-several-hands-minor-works-1813` | have-raw (IA `minorworksofxeno00xenouoft`) |
| Cyropaedia | Walter Miller (Loeb 1914) | `xenophon-perseus-miller-cyropaedia` | have (Perseus TEI `tlg0032.tlg007.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): none here. Marchant's and Todd's Loebs (1923-25) are held above as Perseus TEI; Brownson's Hellenica and Anabasis and Miller's Cyropaedia are on PR #7 as Perseus TEI.

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

Pending (wishlist): Paton's Loeb (1922-27) is on PR #7 as Perseus TEI; 

## Arrian

Shelf: `pipeline/arrian_shelf.json`. Chinnock's Anabasis (1884) and Dansey's On Coursing (1831), clean Gutenberg. Epictetus's Discourses, which Arrian recorded, are shelved under Epictetus. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Anabasis of Alexander | E. J. Chinnock (1884) | `arrian-chinnock-anabasis` | have (PG 46976) |
| Arrian on Coursing (Cynegeticus) | William Dansey (1831) | `arrian-dansey-coursing` | have (PG 78013) |
| The Commerce and Navigation of the Erythraean Sea, with Arrian's Account of the Voyage of Nearkhos (Indica, chs. 18-43; 1879) | J. W. McCrindle | `arrian-mccrindle-nearkhos` | have (PG 55054) |
| Ancient India as described by Megasthenes and Arrian: the fragments of Megasthenes and the first part of Arrian's Indika (chs. 1-17; 1877) | J. W. McCrindle | `arrian-mccrindle-ancient-india` | have-raw (IA `b29352290`) |
| Arrian's History of Alexander's Expedition, with notes (London, 1729), vol. 1 (Books I-IV) | John Rooke | `arrian-rooke-1729-v1` | have-raw (IA `arrianshistorya00rookgoog`) |

Pending (wishlist): Chinnock's Indica (Bohn, 1893) as a second witness; vol. 2 of Rooke's 1729 Arrian (vol. 1 is held above; no scan of vol. 2 found). The whole Indica is held in McCrindle's two books above (chs. 1-17 in Ancient India, 18-43 in the Voyage of Nearkhos).

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
| A discourse to an unlearned prince | John Kersey | `plutarch-perseus-kersey-a-discourse-to-an-unlearned-prince` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Against Colotes, the Disciple and Favorite of Epicurus. | A. G. | `plutarch-perseus-g-against-colotes-the-disciple-and-favorit` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Five Tragical Histories of Love | A.I. | `plutarch-perseus-ai-five-tragical-histories-of-love` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Love. | John Philips | `plutarch-perseus-philips-of-love` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Whether 'Twere Rightly Said, Live Concealed. | Charles Whitaker | `plutarch-perseus-whitaker-whether-twere-rightly-said-live-conceale` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| That Virtue May Be Taught | John Patrick | `plutarch-perseus-patrick-that-virtue-may-be-taught` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Whether an Aged Man Ought to Meddle in State Affairs. | F. Fetherston | `plutarch-perseus-fetherston-whether-an-aged-man-ought-to-meddle-in-s` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Whether vice is sufficient to render a man unhappy | Samuel White | `plutarch-perseus-white-whether-vice-is-sufficient-to-render-a-m` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Whether the Passions of the Soul or Diseases of the Body Are Worse | Samuel White | `plutarch-perseus-white-whether-the-passions-of-the-soul-or-dise` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Laconic Apophthegms; or Remarkable Sayings of the Spartans. | unnamed (as in the Perseus header) | `plutarch-perseus-anon-laconic-apophthegms-or-remarkable-saying` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Whether water or fire be most useful. | F. Fetherston | `plutarch-perseus-fetherston-whether-water-or-fire-be-most-useful` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| That brute beasts make use of reason | Sir A. J. | `plutarch-perseus-j-that-brute-beasts-make-use-of-reason` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| An Abstract of a Comparison Betwixt Aristophanes and Menander | William Baxter | `plutarch-perseus-baxter-an-abstract-of-a-comparison-betwixt-aris` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| A breviate of a discourse, showing that the Stoics speak greater improbabilities than the poets. | William Baxter | `plutarch-perseus-baxter-a-breviate-of-a-discourse-showing-that-t` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Advice to Bride and Groom | Frank Cole Babbitt | `plutarch-perseus-babbitt-advice-to-bride-and-groom` | have (Perseus TEI `tlg0007.tlg078.perseus-eng3`; markup CC BY-SA 4.0) |
| Conjugal Precepts | John Philips | `plutarch-perseus-philips-conjugal-precepts` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Plutarch's Consolatory Letter to His Wife | Thomas Creech | `plutarch-perseus-creech-plutarch-s-consolatory-letter-to-his-wif` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| A Letter of Condolence to Apollonius | Frank Cole Babbitt | `plutarch-perseus-babbitt-a-letter-of-condolence-to-apollonius` | have (Perseus TEI `tlg0007.tlg076.perseus-eng3`; markup CC BY-SA 4.0) |
| Consolation to Apollonius | Matthew Morgan | `plutarch-perseus-morgan-consolation-to-apollonius` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Concerning the fortune or virtue of Alexander the Great. | John Phillips | `plutarch-perseus-phillips-concerning-the-fortune-or-virtue-of-alex` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Natural Affection Towards One's Offspring | R. Brown | `plutarch-perseus-brown-of-natural-affection-towards-one-s-offsp` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of the Love of Wealth | John Patrick | `plutarch-perseus-patrick-of-the-love-of-wealth` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Why the Oracles Cease to Give Answers | Robert Midgley | `plutarch-perseus-midgley-why-the-oracles-cease-to-give-answers` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of the word ΕΙ engraven over the gate of Apollo's temple at Delphi | R. Kippax | `plutarch-perseus-kippax-of-the-word-engraven-over-the-gate-of-ap` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of the Face Appearing Within the Orb Of the Moon | A.G. | `plutarch-perseus-ag-of-the-face-appearing-within-the-orb-of` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Fate. | A. G. | `plutarch-perseus-g-of-fate` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Garrulity, or Talkativeness | John Philips | `plutarch-perseus-philips-of-garrulity-or-talkativeness` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| A Discourse Concerning Socrates's Daemon | Thomas Creech | `plutarch-perseus-creech-a-discourse-concerning-socrates-s-daemon` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Herodotus's Malice. | A. G. | `plutarch-perseus-g-of-herodotus-s-malice` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Envy and Hatred | P. Lancaster | `plutarch-perseus-lancaster-of-envy-and-hatred` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Isis and Osiris, or of the Ancient Religion and Philosophy of Egypt. | William Baxter | `plutarch-perseus-baxter-of-isis-and-osiris-or-of-the-ancient-rel` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Wherefore the Pythian Priestess now Ceases to Deliver her Oracles in Verse | John Philips | `plutarch-perseus-philips-wherefore-the-pythian-priestess-now-ceas` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| How a Man May Inoffensively Praise Himself Without Being Liable to Envy | P. Lancaster | `plutarch-perseus-lancaster-how-a-man-may-inoffensively-praise-himse` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Concerning Such Whom God is Slow to Punish | John Philips | `plutarch-perseus-philips-concerning-such-whom-god-is-slow-to-puni` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The contradictions of the Stoics | E. Smith | `plutarch-perseus-smith-the-contradictions-of-the-stoics` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Superstition | Frank Cole Babbitt | `plutarch-perseus-babbitt-superstition` | have (Perseus TEI `tlg0007.tlg080.perseus-eng3`; markup CC BY-SA 4.0) |
| Of Superstition, or Indiscreet Devotion | William Baxter | `plutarch-perseus-baxter-of-superstition-or-indiscreet-devotion` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of the Tranquillity of the Mind. | Matthew Morgan | `plutarch-perseus-morgan-of-the-tranquillity-of-the-mind` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Moral Virtue | Matthew Morgan | `plutarch-perseus-morgan-of-moral-virtue` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Bashfulness | Thomas Hoy | `plutarch-perseus-hoy-of-bashfulness` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On Having Many Friends | Frank Cole Babbitt | `plutarch-perseus-babbitt-on-having-many-friends` | have (Perseus TEI `tlg0007.tlg073.perseus-eng3`; markup CC BY-SA 4.0) |
| Of Large Acquaintance: or, an Essay to Prove the Folly of Seeking Many Friends | William W. Goodwin | `plutarch-perseus-goodwin-of-large-acquaintance-or-an-essay-to-pro` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Concerning the procreation of the soul as discoursed in Timaeus | John Philips | `plutarch-perseus-philips-concerning-the-procreation-of-the-soul-a` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| How To Profit By One's Enemies | Frank Cole Babbitt | `plutarch-perseus-babbitt-how-to-profit-by-one-s-enemies` | have (Perseus TEI `tlg0007.tlg072.perseus-eng3`; markup CC BY-SA 4.0) |
| How a man may receive advantage and profit from his enemies. | John Hartcliffe | `plutarch-perseus-hartcliffe-how-a-man-may-receive-advantage-and-prof` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Concerning the cure of anger: a dialogue | William Dillingham | `plutarch-perseus-dillingham-concerning-the-cure-of-anger-a-dialogue` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of common conceptions, against the Stoics. | Samuel White | `plutarch-perseus-white-of-common-conceptions-against-the-stoics` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Curiosity, or an Over-Busy Inquisitiveness into Things Impertinent. | Maurice Wheeler | `plutarch-perseus-wheeler-of-curiosity-or-an-over-busy-inquisitive` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of eating of flesh: Tract I. | William Baxter | `plutarch-perseus-baxter-of-eating-of-flesh-tract-i` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of eating of flesh: Tract II. | William Baxter | `plutarch-perseus-baxter-of-eating-of-flesh-tract-ii` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Banishment, or Flying One's Country. | John Patrick | `plutarch-perseus-patrick-of-banishment-or-flying-one-s-country` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Chance | Frank Cole Babbitt | `plutarch-perseus-babbitt-chance` | have (Perseus TEI `tlg0007.tlg074.perseus-eng3`; markup CC BY-SA 4.0) |
| Of Fortune | William Baxter | `plutarch-perseus-baxter-of-fortune` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Concerning the fortune of the Romans | John Oswald | `plutarch-perseus-oswald-concerning-the-fortune-of-the-romans` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Brotherly Love | John Thomson | `plutarch-perseus-thomson-of-brotherly-love` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Whether the Athenians Were More Renowned For Their Warlike Achievements or For Their Learning | R. Smith | `plutarch-perseus-smith-whether-the-athenians-were-more-renowned` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The Education of Children | Frank Cole Babbitt | `plutarch-perseus-babbitt-the-education-of-children` | have (Perseus TEI `tlg0007.tlg067.perseus-eng3`; markup CC BY-SA 4.0) |
| A Discourse Touching the Training of Children | Simon Ford | `plutarch-perseus-ford-a-discourse-touching-the-training-of-chi` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Concerning the First Principle of Cold | F. Fetherston | `plutarch-perseus-fetherston-concerning-the-first-principle-of-cold` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On Listening to Lectures | Frank Cole Babbitt | `plutarch-perseus-babbitt-on-listening-to-lectures` | have (Perseus TEI `tlg0007.tlg069.perseus-eng3`; markup CC BY-SA 4.0) |
| Of Hearing | Thomas Hoy | `plutarch-perseus-hoy-of-hearing` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Which are the most crafty, water-animals or those creatures that breed upon the land? | John Philips | `plutarch-perseus-philips-which-are-the-most-crafty-water-animals` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Advice About Keeping Well | Frank Cole Babbitt | `plutarch-perseus-babbitt-advice-about-keeping-well` | have (Perseus TEI `tlg0007.tlg077.perseus-eng3`; markup CC BY-SA 4.0) |
| Plutarch's Rules for the Preservation of Health | Matthew Poole | `plutarch-perseus-poole-plutarch-s-rules-for-the-preservation-of` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of the Three Sorts of Government, Monarchy, Democracy, and Oligarchy. | R. Smith | `plutarch-perseus-smith-of-the-three-sorts-of-government-monarch` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Virtue and Vice | Frank Cole Babbitt | `plutarch-perseus-babbitt-virtue-and-vice` | have (Perseus TEI `tlg0007.tlg075.perseus-eng3`; markup CC BY-SA 4.0) |
| Of Virtue and Vice | William Baxter | `plutarch-perseus-baxter-of-virtue-and-vice` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Against Running in Debt, or Taking up Money Upon Usury | R. Smith | `plutarch-perseus-smith-against-running-in-debt-or-taking-up-mon` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| That a Philosopher Ought Chiefly to Converse with Great Men | Knightly Chetwood | `plutarch-perseus-chetwood-that-a-philosopher-ought-chiefly-to-conv` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Concerning the Virtues of Women | Isaac Chauncy | `plutarch-perseus-chauncy-concerning-the-virtues-of-women` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| That it is Not Possible to Live Pleasurably According to the Doctrine of Epicurus | William Baxter | `plutarch-perseus-baxter-that-it-is-not-possible-to-live-pleasura` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Parallels, or a comparison between the Greek and Roman Histories. | John Oswald | `plutarch-perseus-oswald-parallels-or-a-comparison-between-the-gr` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Plutarch's Platonic questions | R. Brown | `plutarch-perseus-brown-plutarch-s-platonic-questions` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Political Precepts | Samuel White | `plutarch-perseus-white-political-precepts` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Symposiacs | Thomas Creech | `plutarch-perseus-creech-symposiacs` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Greek Questions | Isaac Chauncy | `plutarch-perseus-chauncy-greek-questions` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Plutarch's Natural Questions | R. Brown | `plutarch-perseus-brown-plutarch-s-natural-questions` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Roman Questions | Isaac Chauncy | `plutarch-perseus-chauncy-roman-questions` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| How the Young Man Should Study Poetry | Frank Cole Babbitt | `plutarch-perseus-babbitt-how-the-young-man-should-study-poetry` | have (Perseus TEI `tlg0007.tlg068.perseus-eng3`; markup CC BY-SA 4.0) |
| How a Young Man Ought to Hear Poems | Simon Ford | `plutarch-perseus-ford-how-a-young-man-ought-to-hear-poems` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| How to Tell a Flatterer from a Friend | Frank Cole Babbitt | `plutarch-perseus-babbitt-how-to-tell-a-flatterer-from-a-friend` | have (Perseus TEI `tlg0007.tlg070.perseus-eng3`; markup CC BY-SA 4.0) |
| How to Know a Flatterer from a Friend | George Tullie | `plutarch-perseus-tullie-how-to-know-a-flatterer-from-a-friend` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| How a Man May Become Aware of His Progress in Virtue | Frank Cole Babbitt | `plutarch-perseus-babbitt-how-a-man-may-become-aware-of-his-progre` | have (Perseus TEI `tlg0007.tlg071.perseus-eng3`; markup CC BY-SA 4.0) |
| How a Man May Be Sensible of His Progress in Virtue. | Hugh Tod(d) | `plutarch-perseus-todd-how-a-man-may-be-sensible-of-his-progres` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The apophthegms or remarkable sayings of kings and great commanders. | Edward Hinton | `plutarch-perseus-hinton-the-apophthegms-or-remarkable-sayings-of` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The Dinner of the Seven Wise Men | Frank Cole Babbitt | `plutarch-perseus-babbitt-the-dinner-of-the-seven-wise-men` | have (Perseus TEI `tlg0007.tlg079.perseus-eng3`; markup CC BY-SA 4.0) |
| The Banquet of the Seven Wise Men | Roger Davis | `plutarch-perseus-davis-the-banquet-of-the-seven-wise-men` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Lives of the Ten Orators | Charles Barcroft | `plutarch-perseus-barcroft-lives-of-the-ten-orators` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of the Names of Rivers and Mountains, and of Such Things as are to be Found Therein | R. White | `plutarch-perseus-white-of-the-names-of-rivers-and-mountains-and` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Concerning music | John Philips | `plutarch-perseus-philips-concerning-music` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Of Those Sentiments Concerning Nature with which Philosophers were Delighted | John Dowell | `plutarch-perseus-dowell-of-those-sentiments-concerning-nature-wi` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The Philosophie, commonlie called, The Morals (London, 1603), first part of the scan | Philemon Holland | `plutarch-holland-morals-1603-part1` | have-raw (IA `plutarchhollandmorals01`) |
| The Philosophie, commonlie called, The Morals (London, 1603), second part of the scan (from the Symposiaques) | Philemon Holland | `plutarch-holland-morals-1603-part2` | have-raw (IA `plutarchhollandmorals02`) |
| Aemilius Paulus | Bernadotte Perrin (1918) | `plutarch-perseus-perrin-aemilius-paulus` | have (Perseus TEI `tlg0007.tlg019.perseus-eng2`; markup CC BY-SA 4.0) |
| Agesilaus | Bernadotte Perrin (1917) | `plutarch-perseus-perrin-agesilaus` | have (Perseus TEI `tlg0007.tlg044.perseus-eng2`; markup CC BY-SA 4.0) |
| Agis and Cleomenes | Bernadotte Perrin (1921) | `plutarch-perseus-perrin-agis-and-cleomenes` | have (Perseus TEI `tlg0007.tlg051.perseus-eng1`; markup CC BY-SA 4.0) |
| Alcibiades | Bernadotte Perrin (1916) | `plutarch-perseus-perrin-alcibiades` | have (Perseus TEI `tlg0007.tlg015.perseus-eng2`; markup CC BY-SA 4.0) |
| Alexander | Bernadotte Perrin (1919) | `plutarch-perseus-perrin-alexander` | have (Perseus TEI `tlg0007.tlg047.perseus-eng2`; markup CC BY-SA 4.0) |
| Antony | Bernadotte Perrin (1920) | `plutarch-perseus-perrin-antony` | have (Perseus TEI `tlg0007.tlg058.perseus-eng2`; markup CC BY-SA 4.0) |
| Aratus | Bernadotte Perrin (1926) | `plutarch-perseus-perrin-aratus` | have (Perseus TEI `tlg0007.tlg063.perseus-eng2`; markup CC BY-SA 4.0) |
| Aristides | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-aristides` | have (Perseus TEI `tlg0007.tlg024.perseus-eng2`; markup CC BY-SA 4.0) |
| Artaxerxes | Bernadotte Perrin (1926) | `plutarch-perseus-perrin-artaxerxes` | have (Perseus TEI `tlg0007.tlg064.perseus-eng2`; markup CC BY-SA 4.0) |
| Brutus | Bernadotte Perrin (1918) | `plutarch-perseus-perrin-brutus` | have (Perseus TEI `tlg0007.tlg061.perseus-eng2`; markup CC BY-SA 4.0) |
| Caesar | Bernadotte Perrin (1919) | `plutarch-perseus-perrin-caesar` | have (Perseus TEI `tlg0007.tlg048.perseus-eng2`; markup CC BY-SA 4.0) |
| Caius Marcius Coriolanus | Bernadotte Perrin (1916) | `plutarch-perseus-perrin-caius-marcius-coriolanus` | have (Perseus TEI `tlg0007.tlg016.perseus-eng2`; markup CC BY-SA 4.0) |
| Caius Marius | Bernadotte Perrin (1920) | `plutarch-perseus-perrin-caius-marius` | have (Perseus TEI `tlg0007.tlg031.perseus-eng2`; markup CC BY-SA 4.0) |
| Camillus | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-camillus` | have (Perseus TEI `tlg0007.tlg011.perseus-eng2`; markup CC BY-SA 4.0) |
| Cato the Younger | Bernadotte Perrin (1919) | `plutarch-perseus-perrin-cato-the-younger` | have (Perseus TEI `tlg0007.tlg050.perseus-eng2`; markup CC BY-SA 4.0) |
| Cicero | Bernadotte Perrin (1919) | `plutarch-perseus-perrin-cicero` | have (Perseus TEI `tlg0007.tlg055.perseus-eng2`; markup CC BY-SA 4.0) |
| Cimon | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-cimon` | have (Perseus TEI `tlg0007.tlg035.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Agesilaus and Pompey | Bernadotte Perrin (1917) | `plutarch-perseus-perrin-comparison-of-agesilaus-and-pompey` | have (Perseus TEI `tlg0007.tlg046.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Agis and Cleomenes and the Gracchi | Bernadotte Perrin (1921) | `plutarch-perseus-perrin-comparison-of-agis-and-cleomenes-and` | have (Perseus TEI `tlg0007.tlg053.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Alcibiades and Coriolanus | Bernadotte Perrin (1916) | `plutarch-perseus-perrin-comparison-of-alcibiades-and-coriola` | have (Perseus TEI `tlg0007.tlg017.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Aristides and Marcus Cato | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-comparison-of-aristides-and-marcus-c` | have (Perseus TEI `tlg0007.tlg026.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Demetrius and Antony | Bernadotte Perrin (1920) | `plutarch-perseus-perrin-comparison-of-demetrius-and-antony` | have (Perseus TEI `tlg0007.tlg059.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Demosthenes and Cicero | Bernadotte Perrin (1919) | `plutarch-perseus-perrin-comparison-of-demosthenes-and-cicero` | have (Perseus TEI `tlg0007.tlg056.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Dion and Brutus | Bernadotte Perrin (1918) | `plutarch-perseus-perrin-comparison-of-dion-and-brutus` | have (Perseus TEI `tlg0007.tlg062.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Lucullus and Cimon | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-comparison-of-lucullus-and-cimon` | have (Perseus TEI `tlg0007.tlg037.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Lycurgus and Numa | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-comparison-of-lycurgus-and-numa` | have (Perseus TEI `tlg0007.tlg006.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Lysander and Sulla | Bernadotte Perrin (1916) | `plutarch-perseus-perrin-comparison-of-lysander-and-sulla` | have (Perseus TEI `tlg0007.tlg034.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Nicias and Crassus | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-comparison-of-nicias-and-crassus` | have (Perseus TEI `tlg0007.tlg040.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Pelopidas and Marcellus | Bernadotte Perrin (1917) | `plutarch-perseus-perrin-comparison-of-pelopidas-and-marcellu` | have (Perseus TEI `tlg0007.tlg023.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Pericles and Fabius Maximus | Bernadotte Perrin (1916) | `plutarch-perseus-perrin-comparison-of-pericles-and-fabius-ma` | have (Perseus TEI `tlg0007.tlg014.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Philopoemen and Titus | Bernadotte Perrin (1921) | `plutarch-perseus-perrin-comparison-of-philopoemen-and-titus` | have (Perseus TEI `tlg0007.tlg029.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Sertorius and Eumenes | Bernadotte Perrin (1919) | `plutarch-perseus-perrin-comparison-of-sertorius-and-eumenes` | have (Perseus TEI `tlg0007.tlg043.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Solon and Publicola | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-comparison-of-solon-and-publicola` | have (Perseus TEI `tlg0007.tlg009.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Theseus and Romulus | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-comparison-of-theseus-and-romulus` | have (Perseus TEI `tlg0007.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |
| Comparison of Timoleon and Aemilius | Bernadotte Perrin (1918) | `plutarch-perseus-perrin-comparison-of-timoleon-and-aemilius` | have (Perseus TEI `tlg0007.tlg020.perseus-eng2`; markup CC BY-SA 4.0) |
| Crassus | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-crassus` | have (Perseus TEI `tlg0007.tlg039.perseus-eng2`; markup CC BY-SA 4.0) |
| Demetrius | Bernadotte Perrin (1920) | `plutarch-perseus-perrin-demetrius` | have (Perseus TEI `tlg0007.tlg057.perseus-eng2`; markup CC BY-SA 4.0) |
| Demosthenes | Bernadotte Perrin (1919) | `plutarch-perseus-perrin-demosthenes` | have (Perseus TEI `tlg0007.tlg054.perseus-eng2`; markup CC BY-SA 4.0) |
| Dion | Bernadotte Perrin (1918) | `plutarch-perseus-perrin-dion` | have (Perseus TEI `tlg0007.tlg060.perseus-eng2`; markup CC BY-SA 4.0) |
| Eumenes | Bernadotte Perrin (1919) | `plutarch-perseus-perrin-eumenes` | have (Perseus TEI `tlg0007.tlg041.perseus-eng2`; markup CC BY-SA 4.0) |
| Fabius Maximus | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-fabius-maximus` | have (Perseus TEI `tlg0007.tlg013.perseus-eng2`; markup CC BY-SA 4.0) |
| Galba | Bernadotte Perrin (1926) | `plutarch-perseus-perrin-galba` | have (Perseus TEI `tlg0007.tlg065.perseus-eng2`; markup CC BY-SA 4.0) |
| Lucullus | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-lucullus` | have (Perseus TEI `tlg0007.tlg036.perseus-eng2`; markup CC BY-SA 4.0) |
| Lycurgus | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-lycurgus` | have (Perseus TEI `tlg0007.tlg004.perseus-eng2`; markup CC BY-SA 4.0) |
| Lysander | Bernadotte Perrin (1916) | `plutarch-perseus-perrin-lysander` | have (Perseus TEI `tlg0007.tlg032.perseus-eng2`; markup CC BY-SA 4.0) |
| Marcellus | Bernadotte Perrin (1917) | `plutarch-perseus-perrin-marcellus` | have (Perseus TEI `tlg0007.tlg022.perseus-eng2`; markup CC BY-SA 4.0) |
| Marcus Cato | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-marcus-cato` | have (Perseus TEI `tlg0007.tlg025.perseus-eng2`; markup CC BY-SA 4.0) |
| Nicias | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-nicias` | have (Perseus TEI `tlg0007.tlg038.perseus-eng2`; markup CC BY-SA 4.0) |
| Numa | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-numa` | have (Perseus TEI `tlg0007.tlg005.perseus-eng2`; markup CC BY-SA 4.0) |
| Otho | Bernadotte Perrin (1926) | `plutarch-perseus-perrin-otho` | have (Perseus TEI `tlg0007.tlg066.perseus-eng2`; markup CC BY-SA 4.0) |
| Pelopidas | Bernadotte Perrin (1917) | `plutarch-perseus-perrin-pelopidas` | have (Perseus TEI `tlg0007.tlg021.perseus-eng2`; markup CC BY-SA 4.0) |
| Pericles | Bernadotte Perrin (1916) | `plutarch-perseus-perrin-pericles` | have (Perseus TEI `tlg0007.tlg012.perseus-eng2`; markup CC BY-SA 4.0) |
| Philopoemen | Bernadotte Perrin (1921) | `plutarch-perseus-perrin-philopoemen` | have (Perseus TEI `tlg0007.tlg027.perseus-eng2`; markup CC BY-SA 4.0) |
| Phocion | Bernadotte Perrin (1919) | `plutarch-perseus-perrin-phocion` | have (Perseus TEI `tlg0007.tlg049.perseus-eng2`; markup CC BY-SA 4.0) |
| Pompey | Bernadotte Perrin (1917) | `plutarch-perseus-perrin-pompey` | have (Perseus TEI `tlg0007.tlg045.perseus-eng2`; markup CC BY-SA 4.0) |
| Publicola | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-publicola` | have (Perseus TEI `tlg0007.tlg008.perseus-eng2`; markup CC BY-SA 4.0) |
| Pyrrhus | Bernadotte Perrin (1920) | `plutarch-perseus-perrin-pyrrhus` | have (Perseus TEI `tlg0007.tlg030.perseus-eng2`; markup CC BY-SA 4.0) |
| Romulus | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-romulus` | have (Perseus TEI `tlg0007.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |
| Sertorius | Bernadotte Perrin (1919) | `plutarch-perseus-perrin-sertorius` | have (Perseus TEI `tlg0007.tlg042.perseus-eng2`; markup CC BY-SA 4.0) |
| Solon | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-solon` | have (Perseus TEI `tlg0007.tlg007.perseus-eng2`; markup CC BY-SA 4.0) |
| Sulla | Bernadotte Perrin (1916) | `plutarch-perseus-perrin-sulla` | have (Perseus TEI `tlg0007.tlg033.perseus-eng2`; markup CC BY-SA 4.0) |
| Themistocles | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-themistocles` | have (Perseus TEI `tlg0007.tlg010.perseus-eng2`; markup CC BY-SA 4.0) |
| Theseus | Bernadotte Perrin (1914) | `plutarch-perseus-perrin-theseus` | have (Perseus TEI `tlg0007.tlg001.perseus-eng3`; markup CC BY-SA 4.0) |
| Tiberius and Caius Gracchus | Bernadotte Perrin (1921) | `plutarch-perseus-perrin-tiberius-and-caius-gracchus` | have (Perseus TEI `tlg0007.tlg052.perseus-eng1`; markup CC BY-SA 4.0) |
| Timoleon | Bernadotte Perrin (1918) | `plutarch-perseus-perrin-timoleon` | have (Perseus TEI `tlg0007.tlg018.perseus-eng2`; markup CC BY-SA 4.0) |
| Titus Flamininus | Bernadotte Perrin (1921) | `plutarch-perseus-perrin-titus-flamininus` | have (Perseus TEI `tlg0007.tlg028.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): Philemon Holland's Morals (1603) is held above from the UC San Diego copy (OCR 0.90-0.92, old spelling); Babbitt's Moralia vols. 3 on (1931-) are after the 1930 line. Perrin's Lives are on PR #7 as Perseus TEI.

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
| The Meditations of Marcus Aurelius Antoninus (Oxford, Frowde, 1906; introduction by Charles Bigg) | John Jackson (from the catalogue; the scan's title page names no translator) | `marcus-aurelius-jackson-1906` | have-raw (IA `meditationsmarc00jackgoog`) |
| The Meditations of Marcus Aurelius (Everyman's Library no. 9, intro. W. H. D. Rouse; first issue of this edition 1906, this scan the 1948 reprint) | Meric Casaubon | `marcus-aurelius-casaubon-everyman` | have-raw (IA `meditations00marcuoft`) |
| The Emperor Marcus Antoninus his Conversation with Himself, with Gataker's preliminary discourse and Dacier's Life (London: Richard Sare, 1701) | Jeremy Collier | `marcus-aurelius-collier-1701` | have-raw (IA `emperormarcusant01marc`) |
| The Meditations of Marcus Aurelius (Camelot Series; London: Walter Scott, 1887) | Jeremy Collier, revised by Alice Zimmern | `marcus-aurelius-collier-zimmern-1887` | have-raw (IA `meditationsmarc02collgoog`) |

Pending (wishlist): Haines's Loeb (1916; Greek facing).

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
| Arrian's Discourses of Epictetus | George Long | `epictetus-perseus-long-arrian-s-discourses-of-epictetus` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Fragments | George Long | `epictetus-perseus-long-fragments` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Fragments | Thomas Wentworth Higginson | `epictetus-perseus-higginson-fragments` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The Encheiridion, or Manual | George Long | `epictetus-perseus-long-the-encheiridion-or-manual` | held: same translation as another row on this shelf, not a second witness (see `_held`) |

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
| The Workes of Lucius Annaeus Seneca, both Morrall and Naturall (London, 1614) | Thomas Lodge | `seneca-lodge-workes-1614` | have-raw (IA `bim_early-english-books-1475-1640_the-workes-of-lucius-ann_seneca-lucius-annus_1614`) |
| The Epistles of Lucius Annaeus Seneca, with large annotations, vol. I (London: Woodfall for Robinson, MDCCLXXXVI) | Thomas Morell | `seneca-morell-epistles-1786-v1` | have-raw (IA `epistlesluciusa01senegoog`) |
| The Epistles of Lucius Annaeus Seneca, with large annotations, vol. II (London: Woodfall for Robinson, MDCCLXXXVI) | Thomas Morell | `seneca-morell-epistles-1786-v2` | have-raw (IA `epistlesluciusa00senegoog`) |

Pending (wishlist): Basore's Moral Essays vols. 2-3 (1932-35, not PD).

Excluded: PG 59025 (index), PG 55705 (another Seneca, wrong author). Held back for Adam: Seneca his Tenne Tragedies in the 1927 Tudor Translations printing, which carries T. S. Eliot's introduction (US public domain by date, not life+70); the 1581 and 1887 printings are the alternatives.

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
| Tacitus, The Histories, vol. I: Books I-III, with an English translation (Loeb; London: Heinemann, New York: Putnam, MCMXXV; Latin facing) | Clifford H. Moore | `tacitus-moore-histories-v1` | have-raw (IA `tacitus-in-5-volumes.-v.-2-loeb-111`) |

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
| The History of Rome by Titus Livius, translated from the original with notes and illustrations (first American from the last London edition; New York: Peter A. Mesier and others, 1823), vols. I-VI in one file | George Baker | `livy-baker-1823` | have-raw (IA `the-history-of-rome-by-titus-livius-volumes-1-6-translated-by-george-baker-1823`) |
| Livy, Books XXI-XXV: The Second Punic War (Macmillan, 1883) | Alfred John Church and William Jackson Brodribb | `livy-church-brodribb-21-25-1883` | have-raw (IA `livybook2125seco00livy`) |

Pending (wishlist): Foster's Loeb vol. 2 (1922; only a 1939 revised printing found, refused).

## Julius Caesar

Shelf: `pipeline/caesar_shelf.json`. McDevitte and Bohn (1869), all five commentaries, clean Gutenberg. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| 'De Bello Gallico' and Other Commentaries | W. A. McDevitte and W. S. Bohn | `caesar-mcdevitte-bohn` | have (PG 10657) |
| The Gallic War (Loeb, 1917) | H. J. Edwards | `caesar-edwards-gallic-war` | have-raw (IA `gallicwar00caes`) |
| The Civil Wars (Loeb, 1914) | A. G. Peskett | `caesar-peskett-civil-wars` | have-raw (IA `civilwarswitheng00caesuoft`) |
| The Eyght Bookes of Caius Julius Caesar, conteyning his Martiall Exploytes in the Realme of Gallia (London, Willyam Seres, 1565) | Arthur Golding | `caesar-golding-1565` | have-raw (IA `bim_early-english-books-1475-1640_the-eyght-bookes-of-caiu_caesar-caino-julius_1565`) |
| The Commentaries of Caesar, translated into English, with a discourse concerning the Roman art of war (1753; Philadelphia stereotype, 1837) | William Duncan | `caesar-duncan-1837` | have-raw (IA `commentariesofc00caes`) |

Pending (wishlist): none known (Golding's Caesar, 1565, is held above).

## Suetonius

Shelf: `pipeline/suetonius_shelf.json`. Thomson rev. Forester (Bohn), complete. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Lives of the Twelve Caesars, complete | Alexander Thomson, rev. T. Forester | `suetonius-thomson-forester` | have (PG 6400) |
| Suetonius, vol. 1 (Loeb, 1913) | J. C. Rolfe | `suetonius-rolfe-v1` | held: the scan is the 1951 revised printing ('Revised and Reprinted 1951') with an 'Editor's Note (1979)': the text is not the 1913 one; not fetched (see `_held`) |
| Suetonius, vol. 2 (Loeb, 1914) | J. C. Rolfe | `suetonius-rolfe-v2` | have-raw (IA `suetonius02suetuoft`) |
| The Deified Julius | John C. Rolfe | `suetonius-perseus-rolfe-the-deified-julius` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The Historie of Twelve Caesars, Emperours of Rome (London, 1606) | Philemon Holland | `suetonius-holland-1606` | have-raw (IA `suetoniushollandtwelvecaesars`) |

Pending (wishlist): none known.

Excluded: PG 6386-6399 (the same text split into 14 files).

## Sallust

Shelf: `pipeline/sallust_shelf.json`. Watson (Bohn). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Conspiracy of Catiline and the Jugurthine War | J. S. Watson (Bohn) | `sallust-watson` | have (PG 7990) |
| Sallust (Loeb, 1921) | J. C. Rolfe | `sallust-rolfe` | have-raw (IA `sallustsa00sall`) |
| The Works of Sallust, translated into English, with political discourses, and Cicero's four orations against Catiline (London: R. Ware, 1744) | Thomas Gordon | `sallust-gordon-1744` | have-raw (IA `worksofsallusttr00sall`) |
| Sallust, translated by W. Rose, with improvements and notes (Valpy's Family Classical Library, 1830) | William Rose (revised) | `sallust-rose-1830` | have-raw (IA `sallusttrbywros00crisgoog`) |


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
| The Letters of the Younger Pliny, literally translated (Kegan Paul, Trench, 1890) | John Delaware Lewis | `pliny-younger-lewis-letters` | have-raw (IA `lettersyoungerp00plingoog`) |
| The Letters of the Younger Pliny, Second Series: Books VI-X (London and Felling-on-Tyne: Walter Scott Publishing Co.; no printed date, see _rights_checked) | John B. Firth | `pliny-younger-firth-letters-2` | have-raw (IA `in.ernet.dli.2015.38111`) |

Pending (wishlist): a printed date for Firth's Second Series (the DLI scan has none).

Excluded: PG 58589 (adaptation).

## Lucretius

Shelf: `pipeline/lucretius_shelf.json`. Munro (prose, vol. 3 of his edition) and Bailey (1910), raw IA; Creech (1714 ed.) and Good (1805, with the Latin), raw IA; Trevelyan's selections, clean. Leonard's verse is on the Adler shelf (mislabelled Munro there). Not minted.

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
| The Nature of Things: a didactic poem, vol. I (London 1805) | John Mason Good | `lucretius-good-1805-v1` | have-raw (IA `natureofthingsdi01lucr`) |
| The Nature of Things: a didactic poem, vol. II (London 1805) | John Mason Good | `lucretius-good-1805-v2` | have-raw (IA `natureofthingsdi02lucr`) |
| Lucretius, De Rerum Natura, with an English translation (Loeb Classical Library; London: Heinemann, New York: Putnam, 1924; Latin facing) | W. H. D. Rouse | `lucretius-rouse-loeb-1924` | have-raw (IA `text-lucretius-rouse`) |

Pending (wishlist): none. Rouse's Loeb is held above from a 1924 first printing (IA `text-lucretius-rouse`); the 1953 and 1959 printings follow the 1937 revision and were not taken.

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
| Odes | John Conington | `horace-perseus-conington-odes` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The Works of Horace, translated literally into English prose (new edition revised by T. A. Buckley; Harper, 1869) | Christopher Smart, revised by Theodore Alois Buckley | `horace-smart-buckley-1869` | have-raw (IA `workshorace00smargoog`) |
| The Works of Horace rendered into English Prose (Globe Edition; Macmillan, 1874) | James Lonsdale and Samuel Lee | `horace-lonsdale-lee-1874` | have-raw (IA `worksofhoraceren00hora`) |
| The Odes of Horace translated into English Verse, with a life and notes (Boston: Ticknor and Fields, 1866) | Theodore Martin | `horace-martin-odes-1866` | have-raw (IA `odesofhoracetran00horarich`) |
| The Odes and Epodes of Horace, a metrical translation into English, with Latin text (Blackwood, 1869) | Edward Bulwer-Lytton, Lord Lytton | `horace-lytton-1869` | have-raw (IA `odes00epodesofhorahorarich`) |
| The Odes of Horace translated into English (London: John Murray; preface dated 1894) | William Ewart Gladstone | `horace-gladstone-1894` | have-raw (IA `odeshorace01gladgoog`) |
| Horace, The Odes and Epodes, with an English translation (Loeb Classical Library; 1914 translation, Latin facing; this scan is a later impression, see _rights_checked) | C. E. Bennett | `horace-bennett-loeb-odes` | have-raw (IA `in.ernet.dli.2015.98705`) |
| The Works of Horace, translated into English verse, with a life and notes, vol. I: Life, Odes (Blackwood, MDCCCLXXXI) | Theodore Martin | `horace-martin-works-1881-v1` | have-raw (IA `worksofhorace01horauoft`) |
| The Works of Horace, translated into English verse, vol. II: Epodes, Secular Hymn, Satires, Epistles (Blackwood, 1881) | Theodore Martin | `horace-martin-works-1881-v2` | have-raw (IA `worksofhorace02horauoft`) |

Pending (wishlist): Smart's prose in its first, unrevised form (1756) from a cleaner scan than the ECCO OCR (0.74-0.76), which was refused.

## Catullus

Shelf: `pipeline/catullus_shelf.json`. Ellis (1871) and Burton-Smithers (1894), clean Gutenberg. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Poems and Fragments of Catullus translated in the metres of the original | Robinson Ellis (1871) | `catullus-ellis` | have (PG 18867) |
| The Carmina of Caius Valerius Catullus | Sir Richard Burton (verse) and Leonard C. Smithers (prose) | `catullus-burton-smithers` | have (PG 20732) |
| Catullus, Tibullus and Pervigilium Veneris (Loeb, 1913) | F. W. Cornish (Catullus), J. P. Postgate (Tibullus), J. W. Mackail (Pervigilium) | `catullus-tibullus-pervigilium-loeb` | have-raw (IA `catullustibullus00catu`) |
| Carmina | Sir Richard Francis Burton | `catullus-perseus-burton-carmina` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Carmina | Leonard C. Smithers | `catullus-perseus-smithers-carmina` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The Poems of Valerius Catullus, translated into English verse (Edinburgh, 1867) | James Cranstoun | `catullus-cranstoun-1867` | have-raw (IA `poemsofvaleriusc00caturich`) |
| The Poems of Caius Valerius Catullus translated, with a preface and notes, vol. I (London: John Murray, 1821) | George Lamb | `catullus-lamb-1821-v1` | have-raw (IA `poemscaiusvaler01catugoog`) |
| Erotica: the Poems of Catullus and Tibullus, the Vigil of Venus, a literal prose translation with notes, with the metrical versions of Lamb and Grainger and others (Bohn, MDCCCLIV) | Walter K. Kelly | `catullus-tibullus-kelly-erotica-1854` | have-raw (IA `cu31924031218211`) |


Excluded: PG 23720 (serves a 404).

## Tibullus

Shelf: `pipeline/tibullus_shelf.json`. Theodore C. Williams (1905), clean Gutenberg. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Elegies of Tibullus | Theodore Chickering Williams (verse) | `tibullus-williams` | have (PG 9610) |
| A Poetical Translation of the Elegies of Tibullus, and of the poems of Sulpicia (London, 1759; Latin text facing), 2 vols. in one scan | James Grainger | `tibullus-grainger-1759` | have-raw (IA `apoeticaltransl00graigoog`) |

Pending (wishlist): none known. Postgate's Loeb Tibullus (1913) is held in the Catullus shelf's Loeb volume (`catullus-tibullus-pervigilium-loeb`).

## Juvenal and Persius

Shelf: `pipeline/juvenal_shelf.json`. Evans's literal prose with Gifford's verse (Bohn), clean Gutenberg. Dryden's on lane C. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Satires of Juvenal, Persius, Sulpicia, and Lucilius | Lewis Evans (prose), with William Gifford's verse translation | `juvenal-persius-evans-gifford` | have (PG 50657) |
| — | — | `dryden-juvenal` | cross-ref → Dryden shelf, lane C |
| — | — | `dryden-persius` | cross-ref → Dryden shelf, lane C |
| Juvenal and Persius (Loeb, 1918) | G. G. Ramsay | `juvenal-persius-ramsay` | have-raw (IA `juvenalpersiuswi00juveuoft`) |
| The Satires of A. Persius Flaccus, with a translation and commentary (2nd ed., ed. H. Nettleship, Oxford, 1874; Latin facing) | John Conington | `persius-conington-1874` | have-raw (IA `satireswithtrans00persuoft`) |
| The Satires of Persius, translated, with notes (London: W. Bulmer for J. Wright, 1799) | William Drummond | `persius-drummond-1799` | have-raw (IA `bim_eighteenth-century_the-satires-of-persius-t_persius_1799`) |
| A New and Literal Translation of Juvenal and Persius, with explanatory notes, 2 vols. bound as one (London: William Baynes, 1814) | Martin Madan | `juvenal-persius-madan-1814` | have-raw (IA `newliteraltransl00juveiala`) |
| The Satires of Juvenal translated into English Verse (London: Longman and others, 1814) | Charles Badham | `juvenal-badham-1814` | have-raw (IA `satiresofjuvenal00ju`) |
| The Satires of Juvenal, translated and illustrated (London: Payne and Mackinlay, 1807) | Francis Hodgson | `juvenal-hodgson-1807` | have-raw (IA `b28269743`) |


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
| Plautus, vol. 3: The Merchant, The Braggart Warrior, Mostellaria, The Persian (Loeb, 1924) | Paul Nixon | `plautus-nixon-v3` | held: the only scan (IA plautus03plau) is a 1980 reprint of the 1924 translation carrying a 'Bibliographical Note (1979)', which is not public domain; not fetched (see `_held`) |
| Terence, vol. 1 (Loeb, 1912) | John Sargeaunt | `terence-sargeaunt-v1` | have-raw (IA `terence000ijohn`) |
| Terence, vol. 2 (Loeb, 1912) | John Sargeaunt | `terence-sargeaunt-v2` | have-raw (IA `terence00iijohn`) |

Pending (wishlist): Thornton's verse Plautus (1767-74), from a cleaner scan than the ECCO OCR (0.65-0.70), which was refused.

## Lucan

Shelf: `pipeline/lucan_shelf.json`. Ridley's blank-verse Pharsalia (1896); PG names no translator, identified by collation with Ridley's 1905 printing. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Pharsalia; Dramatic Episodes of the Civil Wars | Sir Edward Ridley (blank verse, 1896); PG names no translator, identified by collation | `lucan-ridley-pharsalia` | have (PG 602) |
| Lucan: The Civil War, Books I-X (Pharsalia) (Loeb, 1928) | J. D. Duff | `lucan-duff` | have-raw (IA `lucancivilwarboo00lucauoft`) |
| Lucan's Pharsalia, vol. 1 | Nicholas Rowe | `lucan-rowe-v1` | have-raw (IA `bub_gb_AnxKHS45tH8C`) |
| Lucan's Pharsalia, vol. 2 (1812; with Vida's Art of Poetry) | Nicholas Rowe | `lucan-rowe-v2` | have-raw (IA `bub_gb_GEsNZ2BDG1QC`) |
| The Pharsalia of Lucan, translated into blank verse (Longmans, 1896) | Edward Ridley | `lucan-ridley-1896` | have-raw (IA `cu31924026485809`) |
| The Pharsalia of Lucan, translated into blank verse, second edition, revised and corrected (Longmans, 1905) | Edward Ridley | `lucan-ridley-1905` | have-raw (IA `pharsaliatransla00lucauoft`) |

Pending (wishlist): Marlowe's First Book (Marlowe shelf).

## Apuleius

Shelf: `pipeline/apuleius_shelf.json`. Adlington's Golden Asse (1566) and Butler's Apologia and Florida (1909), clean Gutenberg. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Golden Asse | William Adlington (1566) | `apuleius-adlington-golden-asse` | have (PG 1666) |
| The Apologia and Florida of Apuleius of Madaura | H. E. Butler (1909) | `apuleius-butler-apologia-florida` | have (PG 26294) |
| The Golden Ass, being the Metamorphoses of Lucius Apuleius (Loeb, 1915) | William Adlington (1566), revised by S. Gaselee | `apuleius-adlington-gaselee` | have-raw (IA `goldenassbeingme00apuliala`) |
| The Metamorphoses or Golden Ass of Apuleius of Madaura, vol. 1 (Oxford, 1910) | H. E. Butler | `apuleius-butler-v1` | have-raw (IA `metamorphosesorg01apuluoft`) |
| The Metamorphoses or Golden Ass of Apuleius of Madaura, vol. 2 (Oxford, 1910) | H. E. Butler | `apuleius-butler-v2` | have-raw (IA `metamorphosesorg02apuluoft`) |
| The Metamorphosis, or Golden Ass, and Philosophical Works, of Apuleius, translated from the original Latin (London: Triphook and Rodd, 1822) | Thomas Taylor | `apuleius-taylor-1822` | have-raw (IA `metamorphosisor00apulgoog`) |

Pending (wishlist): none known.

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
| The Cynic | Henry Watson Fowler and Francis George Fowler | `lucian-perseus-fowler-the-cynic` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Demosthenes: an Encomium | Henry Watson Fowler and Francis George Fowler | `lucian-perseus-fowler-demosthenes-an-encomium` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The Halcyon | Emily James Smith | `lucian-perseus-smith-the-halcyon` | have (Perseus TEI `tlg0061.tlg004.perseus-eng1`; markup CC BY-SA 4.0) |
| The Works of Lucian, from the Greek (London: T. Cadell, 1780), vol. 1 | Thomas Francklin | `lucian-francklin-1780-v1` | have-raw (IA `worksoflucian01luci`) |
| The Works of Lucian, from the Greek (London: T. Cadell, 1780), vol. 2 | Thomas Francklin | `lucian-francklin-1780-v2` | have-raw (IA `worksoflucian02luci`) |
| Lucian of Samosata, from the Greek, with the comments and illustrations of Wieland and others, vol. I (London, 1820) | William Tooke | `lucian-tooke-1820-v1` | have-raw (IA `lucianofsamosata01luciuoft`) |
| Lucian of Samosata, from the Greek, with the comments and illustrations of Wieland and others, vol. II (London, 1820) | William Tooke | `lucian-tooke-1820-v2` | have-raw (IA `lucianofsamosata02luciuoft`) |

Pending (wishlist): none for Francklin: his Works of Lucian (1780, 2 vols.) is held above. Harmon's Loeb vols. 5 on (1936-) are after the 1930 line.

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
| The Letters to his Friends, vol. 3 (Loeb, 1929) | W. Glynn Williams | `cicero-williams-friends-v3` | held: the scan is the 1954 printing ('Revised and with additions 1954'): the text is not the 1929 one; not fetched (see `_held`) |
| De Finibus Bonorum et Malorum (Loeb, 1914) | H. Rackham | `cicero-rackham-de-finibus` | have-raw (IA `definibusbonoru02cicegoog`) |
| De Senectute, De Amicitia, De Divinatione (Loeb, 1923) | W. A. Falconer | `cicero-falconer-senectute-amicitia-divinatione` | have-raw (IA `cicerodesenectut0000will_n8p4`) |
| Philippics (Loeb, 1926) | Walter C. A. Ker | `cicero-ker-philippics` | have-raw (IA `philippics00ciceuoft`) |
| The Verrine Orations, vol. 1 (Loeb, 1928) | L. H. G. Greenwood | `cicero-greenwood-verrines-v1` | have-raw (IA `ciceroverrineora0001unse`) |
| De Re Publica, De Legibus (Loeb, 1928) | Clinton Walker Keyes | `cicero-keyes-de-re-publica-de-legibus` | have-raw (IA `derepublicadeleg0000cice_k7o1`) |
| Cicero: the Offices; Cato, or an Essay on Old Age; Laelius, or an Essay on Friendship (Harper, 1838, vol. 3) | Thomas Cockman (Offices); William Melmoth (Cato, Laelius) | `cicero-cockman-offices-melmoth-cato-laelius` | have-raw (IA `bub_gb_IGgRfydq6YwC`) |
| Cicero on Oratory and Orators, with his Letters to Quintus and Brutus (Bohn; Bell & Daldy, 1871 printing) | J. S. Watson | `cicero-watson-on-oratory` | have-raw (IA `ciceroonoratory00cice`) |
| Cicero's Three Books of Offices, or Moral Duties; also Cato Major, Laelius, Paradoxes, Scipio's Dream and the Letter to Quintus (Harper, 1860) | Cyrus R. Edmonds | `cicero-edmonds-offices` | have-raw (IA `cicerosthreebook00ciceuoft`) |
| Cicero, The Speeches: Pro Archia, Post Reditum in Senatu, Post Reditum ad Quirites, De Domo Sua, De Haruspicum Responsis, Pro Plancio (Loeb, first printed 1923; this scan a 1965 reprint; Latin facing) | N. H. Watts | `cicero-watts-pro-archia-etc` | have-raw (IA `cicero-in-28-volumes.-vol.-11-loeb-158`) |
| Cicero, The Speeches: Pro Lege Manilia, Pro Caecina, Pro Cluentio, Pro Rabirio Perduellionis (Loeb, first printed 1927; this scan a 1966 reprint; Latin facing) | H. Grose Hodge | `cicero-grose-hodge-pro-lege-manilia-etc` | have-raw (IA `cicero-in-28-volumes.-vol.-9-loeb-198`) |
| Cicero, Pro Quinctio, Pro Roscio Amerino, Pro Roscio Comoedo, De Lege Agraria I-III (Loeb, first printed 1930; this scan a 1967 reprint; Latin facing) | John Henry Freese | `cicero-freese-pro-quinctio-etc` | have-raw (IA `cicero-in-28-volumes.-vol.-6-loeb-240`) |

Pending (wishlist): King's Tusculans (Loeb 1927; only the 1945 revised printing has text, refused).

Excluded: none. (Winstedt's Atticus, once held back as Latin facing, is now held: Latin-facing Loebs are taken.)

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
| The Orations of Demosthenes, pronounced to excite the Athenians against Philip, King of Macedon, a new edition, vol. I (London: Bensley, 1806) | Thomas Leland | `demosthenes-leland-1806-v1` | have-raw (IA `orationsofdemost01demouoft`) |
| The Orations of Demosthenes, pronounced to excite the Athenians against Philip, King of Macedon, a new edition, vol. II (London: Bensley, 1806) | Thomas Leland | `demosthenes-leland-1806-v2` | have-raw (IA `orationsofdemost02demouoft`) |

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

Pending (wishlist): none: Lamb's Loeb (1930) is held above as Perseus TEI

## Isocrates

Shelf: `pipeline/isocrates_shelf.json`. J. H. Freese, The Orations of Isocrates vol. 1 (Bohn, 1894), raw IA OCR.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Orations of Isocrates, vol. 1 (Bohn, 1894) | J. H. Freese | `isocrates-freese-v1` | have-raw (IA `orationsofisocra0000isoc`) |
| Against the Sophists | George Norlin (1929) | `isocrates-perseus-norlin-against-the-sophists` | have (Perseus TEI `tlg0010.tlg008.perseus-eng2`; markup CC BY-SA 4.0) |
| Antidosis | George Norlin (1929) | `isocrates-perseus-norlin-antidosis` | have (Perseus TEI `tlg0010.tlg019.perseus-eng2`; markup CC BY-SA 4.0) |
| To Archidamus | George Norlin (1928) | `isocrates-perseus-norlin-to-archidamus` | have (Perseus TEI `tlg0010.tlg016.perseus-eng2`; markup CC BY-SA 4.0) |
| Areopagiticus | George Norlin (1929) | `isocrates-perseus-norlin-areopagiticus` | have (Perseus TEI `tlg0010.tlg018.perseus-eng2`; markup CC BY-SA 4.0) |
| Nicocles or the Cyprians | George Norlin (1928) | `isocrates-perseus-norlin-nicocles-or-the-cyprians` | have (Perseus TEI `tlg0010.tlg014.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Peace | George Norlin (1929) | `isocrates-perseus-norlin-on-the-peace` | have (Perseus TEI `tlg0010.tlg017.perseus-eng2`; markup CC BY-SA 4.0) |
| Panathenaicus | George Norlin (1929) | `isocrates-perseus-norlin-panathenaicus` | have (Perseus TEI `tlg0010.tlg021.perseus-eng2`; markup CC BY-SA 4.0) |
| Panegyricus | George Norlin (1928) | `isocrates-perseus-norlin-panegyricus` | have (Perseus TEI `tlg0010.tlg011.perseus-eng2`; markup CC BY-SA 4.0) |
| To Demonicus | George Norlin (1928) | `isocrates-perseus-norlin-to-demonicus` | have (Perseus TEI `tlg0010.tlg007.perseus-eng2`; markup CC BY-SA 4.0) |
| To Nicocles | George Norlin (1928) | `isocrates-perseus-norlin-to-nicocles` | have (Perseus TEI `tlg0010.tlg013.perseus-eng2`; markup CC BY-SA 4.0) |
| To Philip | George Norlin (1928) | `isocrates-perseus-norlin-to-philip` | have (Perseus TEI `tlg0010.tlg020.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): Freese never published vol. 2; Norlin/Van Hook Loeb (1928-45) only vols. 1-2 PD by date

## Pindar

Shelf: `pipeline/pindar_shelf.json`. Myers (Gutenberg) and the Turner/Moore Bohn (raw IA OCR, clean-word 0.87).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Extant Odes of Pindar | Ernest Myers | `pindar-myers` | have (PG 10717) |
| The Odes of Pindar, literally translated into English prose (Bohn; 1872 printing) | Dawson W. Turner (prose) and Abraham Moore (verse) | `pindar-turner-moore` | have-raw (IA `odespindarliter00moorgoog`) |
| — | — | `cary-pindar` | cross-ref → lane C, pipeline/cary_shelf.json (Cary, 1833) |
| Pindar in English Verse (London: Edward Moxon, 1833) | Henry Francis Cary | `pindar-cary-1833` | held elsewhere: IA pindarinenglish00carygoog is already held on pipeline/cary_shelf.json (lane C) as cary-pindar |
| Odes of Pindar, with several other pieces in prose and verse, with a dissertation on the Olympick games (London, 1749) | Gilbert West (verse; selected odes) | `pindar-west-1749` | have-raw (IA `bim_eighteenth-century_odes-of-pindar-with-sev_pindar_1749`) |
| The Odes of Pindar in English Prose, with West's Dissertation on the Olympic Games (Oxford: Munday and Slatter, 1824), 2 vols. in one scan | Peter Edmund Laurent per the catalogue (not named on the title page) | `pindar-laurent-prose-1824` | have-raw (IA `odespindarineng01pindgoog`) |
| The Odes of Pindar translated into English Prose, with brief explanatory notes and a preface (London: Williams and Norgate, 1868) | F. A. Paley | `pindar-paley-1868` | have-raw (IA `bub_gb_z9lUAAAAcAAJ`) |
| Pindar, translated (London: A. J. Valpy for Colburn and Bentley, 1830) | C. A. Wheelwright | `pindar-wheelwright-1830` | have-raw (IA `pindartrbycawhe00pindgoog`) |

Pending (wishlist): Sandys Loeb (1915; Greek facing)

## Theocritus, Bion, Moschus

Shelf: `pipeline/theocritus_shelf.json`. Calverley's verse (Gutenberg) and the Banks/Chapman Bohn (raw IA OCR, clean-word 0.86).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Theocritus, translated into English Verse | Charles Stuart Calverley | `theocritus-calverley` | have (PG 11533) |
| The Idylls of Theocritus, Bion, and Moschus, and the War-Songs of Tyrtaeus (Bohn, 1853) | J. Banks (prose), J. M. Chapman (verse); Tyrtaeus R. Polwhele | `theocritus-bion-moschus-banks` | have-raw (IA `idyllstheocritu00biongoog`) |
| — | — | `lang theocritus-bion-moschus (PG 4775)` | cross-ref → lane D, pipeline/lang_shelf.json |
| The Idylliums of Theocritus, translated from the Greek, with notes (London, 1767) | Francis Fawkes | `theocritus-fawkes-1767` | have-raw (IA `idylliumsoftheoc00theo`) |
| The Idylls of Theocritus translated into English Verse (London: Rivingtons, 1901; revised from 1894) | James Henry Hallard | `theocritus-hallard-1901` | have-raw (IA `idyllsoftheocrit00theo`) |

Pending (wishlist): Edmonds Loeb (1912; Greek facing)

## Apollonius Rhodius

Shelf: `pipeline/apollonius_shelf.json`. Seaton, Way (Gutenberg) and Coleridge 1889 (raw IA OCR, clean-word 0.92).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Argonautica | R. C. Seaton | `apollonius-seaton` | have (PG 13977) |
| The Tale of the Argonauts | Arthur S. Way | `apollonius-way` | have (PG 64235) |
| The Argonautica of Apollonius Rhodius (Bell, 1889) | Edward P. Coleridge | `apollonius-coleridge` | have-raw (IA `B-001-014-458`) |
| The Argonautics of Apollonius Rhodius, in four books (London, 1780) | Francis Fawkes (finished after his death by Henry Meen) | `apollonius-fawkes-1780` | have-raw (IA `argonauticsofapo00apoliala`) |
| The Argonautics of Apollonius Rhodius, translated into English verse, with notes (Dublin, 1803), vol. 1 (holds all four books of the poem) | William Preston | `apollonius-preston-1803-v1` | have-raw (IA `argonauticstrin00apolgoog`) |
| The Argonautics of Apollonius Rhodius, translated into English verse, with notes (Dublin, 1803), vol. 3 (notes and dissertations; vol. 2 not found on archive.org) | William Preston | `apollonius-preston-1803-v3` | have-raw (IA `argonauticstrin01apolgoog`) |

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
| The Greek Anthology, as selected for the use of Westminster, Eton and other public schools, literally translated into English prose, with metrical versions by Bland, Merivale and others (Bohn, MDCCCLIV) | George Burges | `greek-anthology-burges-1854` | have-raw (IA `greekanthology0000geor`) |

Pending (wishlist): Paton's Anthology, Edmonds's Lyra Graeca, Mair's Callimachus/Aratus/Oppian (all Loebs, Greek facing). Callimachus, Aratus, Tryphiodorus and Musaeus in older translations are on the late-greek-poets shelf.

Excluded: modern free Sappho recreations (Carman, O'Hara, Stacpoole)

## Diogenes Laertius

Shelf: `pipeline/diogenes-laertius_shelf.json`. Yonge (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Lives and Opinions of Eminent Philosophers | Charles Duke Yonge | `diogenes-laertius-yonge` | have (PG 57342) |
| Lives of Eminent Philosophers | R. D. Hicks (1925) | `diogenes-laertius-perseus-hicks-lives-of-eminent-philosopher` | have (Perseus TEI `tlg0004.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |

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
| Political Fragments of Archytas, Charondas, Zaleucus and other ancient Pythagoreans, preserved by Stobaeus; and Ethical Fragments of Hierocles (London: for the translator, 1822) | Thomas Taylor | `pythagoreans-taylor-political-fragments-1822` | have-raw (IA `politicalfragmen00taylrich`) |

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
| The Works of the Emperor Julian, vol. 1 | Wilmer Cave Wright | `julian-wright-v1` | held: Gutenberg's transcription (PG 48664) includes a 'Bibliographical Addendum (1980)' from the reprint it was made from, which is not public domain by date; not fetched (see `_held`) |
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
| Heliodorus, An Aethiopian Romance (Broadway Translations; 1923 per the catalogue) | Thomas Underdowne (1587), revised and partly rewritten by F. A. Wright | `heliodorus-underdowne-wright` | have-raw (IA `thiopianromanc00heliuoft`) |
| The Loves of Chaereas and Callirrhoe, written originally in Greek by Chariton of Aphrodisios, vol. 1 (London: Becket and De Hondt, 1764) | unnamed ('made by two young persons', per the dedication) | `chariton-1764-v1` | have-raw (IA `loveschrcasandc01chargoog`) |
| The Loves of Chaereas and Callirrhoe, vol. 2: Books V-VIII (London: Becket and De Hondt, 1764) | unnamed ('made by two young persons', per the dedication in vol. 1) | `chariton-1764-v2` | have-raw (IA `loveschrcasandc00chargoog`) |
| Xenophon's Ephesian History: or the Love-Adventures of Abrocomas and Anthia, in five books (London, 1727) | unnamed in the OCR ('By Mr. ...', name illegible); attributed elsewhere to John Rooke, not verified here | `xenophon-ephesius-1727` | have-raw (IA `gpl_1772898`) |

Excluded: the 1733 Daphnis and Chloe (ECCO OCR 0.69)

## Euclid

Shelf: `pipeline/euclid_shelf.json`. Heath's Thirteen Books 1908, 3 vols. (IA, clean-word 0.77-0.83; mathematical OCR).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Thirteen Books of Euclid's Elements, vol. 1 (1908) | T. L. Heath | `euclid-heath-v1` | have-raw (IA `thirteenbookseu02heibgoog`) |
| The Thirteen Books of Euclid's Elements, vol. 2 (1908) | T. L. Heath | `euclid-heath-v2` | have-raw (IA `thirteenbookseu00heibgoog`) |
| The Thirteen Books of Euclid's Elements, vol. 3 (1908) | T. L. Heath | `euclid-heath-v3` | have-raw (IA `thirteenbookseu01heibgoog`) |
| The Thirteen Books of Euclid's Elements | Thomas Little Heath | `euclid-perseus-heath-the-thirteen-books-of-euclid-s-elements` | held: same translation as another row on this shelf, not a second witness (see `_held`) |

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
| Aphorisms | Francis Adams | `hippocrates-perseus-adams-aphorisms` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Airs, Waters, and Places | Francis Adams | `hippocrates-perseus-adams-airs-waters-and-places` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Airs Waters Places | William Henry Samuel Jones | `hippocrates-perseus-jones-airs-waters-places` | have (Perseus TEI `tlg0627.tlg002.perseus-eng4`; markup CC BY-SA 4.0) |
| Nutriment | William Henry Samuel Jones | `hippocrates-perseus-jones-nutriment` | have (Perseus TEI `tlg0627.tlg046.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Articulations | Francis Adams | `hippocrates-perseus-adams-on-the-articulations` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On Injuries of the Head | Francis Adams | `hippocrates-perseus-adams-on-injuries-of-the-head` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On Regimen in Acute Diseases | Francis Adams | `hippocrates-perseus-adams-on-regimen-in-acute-diseases` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On Fistulae | Francis Adams | `hippocrates-perseus-adams-on-fistulae` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On Fractures | Francis Adams | `hippocrates-perseus-adams-on-fractures` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On Hemorrhoids | Francis Adams | `hippocrates-perseus-adams-on-hemorrhoids` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On the Sacred Disease | Francis Adams | `hippocrates-perseus-adams-on-the-sacred-disease` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On the Surgery | Francis Adams | `hippocrates-perseus-adams-on-the-surgery` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On Ancient Medicine | Francis Adams | `hippocrates-perseus-adams-on-ancient-medicine` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Ancient Medicine | William Henry Samuel Jones | `hippocrates-perseus-jones-ancient-medicine` | have (Perseus TEI `tlg0627.tlg001.perseus-eng4`; markup CC BY-SA 4.0) |
| On Ulcers | Francis Adams | `hippocrates-perseus-adams-on-ulcers` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The Epidemics | Francis Adams | `hippocrates-perseus-adams-the-epidemics` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| The Oath | Francis Adams | `hippocrates-perseus-adams-the-oath` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Oath | William Henry Samuel Jones | `hippocrates-perseus-jones-oath` | have (Perseus TEI `tlg0627.tlg013.perseus-eng5`; markup CC BY-SA 4.0) |
| The Law | Francis Adams | `hippocrates-perseus-adams-the-law` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Precepts | William Henry Samuel Jones | `hippocrates-perseus-jones-precepts` | have (Perseus TEI `tlg0627.tlg051.perseus-eng2`; markup CC BY-SA 4.0) |
| Of the Prognostics | Francis Adams | `hippocrates-perseus-adams-of-the-prognostics` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Mochlicus | Francis Adams | `hippocrates-perseus-adams-mochlicus` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| Epidemics I and III | W. H. S. Jones (Loeb, 1923) | `hippocrates-perseus-jones-epidemics-1-3` | have (Perseus TEI `tlg0627.tlg006.perseus-eng4`; markup CC BY-SA 4.0) |

Pending (wishlist): the Jones/Withington Loeb beyond the six 1923 pieces held as Perseus TEI (Greek facing: OCR not taken)

## Galen

Shelf: `pipeline/galen_shelf.json`. Brock's Natural Faculties 1916 (Gutenberg; facing Greek kept).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Galen: On the Natural Faculties | Arthur John Brock | `galen-brock-natural-faculties` | have (PG 43383) |
| On the Natural Faculties | Arthur John Brock | `galen-perseus-brock-on-the-natural-faculties` | held: same translation as another row on this shelf, not a second witness (see `_held`) |

## Aretaeus

Shelf: `pipeline/aretaeus_shelf.json`. Adams 1856, Greek and English (IA, 0.83).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Extant Works of Aretaeus, the Cappadocian (1856) | ed. and Francis Adams | `aretaeus-adams` | have-raw (IA `extantworksaret00adamgoog`) |
| On the Causes and Symptoms of Acute Diseases | Francis Adams | `aretaeus-perseus-adams-on-the-causes-and-symptoms-of-acute-dise` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On the Causes and Symptoms of Chronic Diseases | Francis Adams | `aretaeus-perseus-adams-on-the-causes-and-symptoms-of-chronic-di` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On the Therapeutics of Acute Diseases | Francis Adams | `aretaeus-perseus-adams-on-the-therapeutics-of-acute-diseases` | held: same translation as another row on this shelf, not a second witness (see `_held`) |
| On the Cure of Chronic Diseases | Francis Adams | `aretaeus-perseus-adams-on-the-cure-of-chronic-diseases` | held: same translation as another row on this shelf, not a second witness (see `_held`) |

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
| The Epigrams of Martial, translated into English prose, each accompanied by one or more verse translations from the works of English poets (Bohn's Classical Library; George Bell, 1877) | unnamed (Bohn prose), with verse versions by various hands | `martial-bohn-1877` | have-raw (IA `epigramsmartial01bohngoog`) |

## Statius

Shelf: `pipeline/statius_shelf.json`. Mozley Loeb 1928, 2 vols. (IA, 0.91-0.92; Latin facing).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Statius, vol. 1: Silvae, Thebaid I-IV (Loeb, 1928) | J. H. Mozley | `statius-mozley-v1` | have-raw (IA `statius01stat`) |
| Statius, vol. 2: Thebaid V-XII, Achilleid (Loeb, 1928) | J. H. Mozley | `statius-mozley-v2` | have-raw (IA `statius02stat`) |
| The Thebaid of Statius, translated into English verse, with notes and observations (Oxford, 1767), both volumes in one scan | William Lillington Lewis (not named on the title page; attributed in catalogues) | `statius-lewis-thebaid-1767` | have-raw (IA `thebaidstatius00conggoog`) |
| The Silvae of Statius, translated with introduction and notes (Oxford, 1908) | D. A. Slater | `statius-slater-silvae-1908` | have-raw (IA `silvaetranslated00statuoft`) |
| The Thebaid of Statius, translated into English verse, with notes and observations, vol. I, second edition corrected (London: T. Becket; the year OCRs as 'MDCCLXm'; IA records 1767) | William Lillington Lewis | `statius-lewis-thebaid-v1` | have-raw (IA `thebaidstatiust01lewigoog`) |
| The Thebaid of Statius, vol. II (Books VII-XII), second edition corrected (London: T. Becket; no year in the OCR; IA records 1773) | William Lillington Lewis | `statius-lewis-thebaid-v2` | have-raw (IA `thebaidstatiust00lewigoog`) |

## Claudian

Shelf: `pipeline/claudian_shelf.json`. Platnauer Loeb 1922 (Gutenberg); Hawkins 1817 vol. 1 (IA, 0.85).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Claudian, vol. 1 | Maurice Platnauer | `claudian-platnauer-v1` | have (PG 51443) |
| Claudian, vol. 2 | Maurice Platnauer | `claudian-platnauer-v2` | have (PG 51444) |
| The Works of Claudian, vol. 1 (1817) | A. Hawkins | `claudian-hawkins-v1` | have-raw (IA `worksclaudian00hawkgoog`) |
| The Rape of Proserpine, with other poems, from Claudian, translated into English Verse (London: Valpy, 1814) | Jacob George Strutt | `claudian-strutt-1814` | have-raw (IA `rapeofproserpi00clau`) |
| Translations from Claudian (London: John Murray, 1823) | Henry Howard | `claudian-howard-1823` | have-raw (IA `translationsfrom00clauuoft`) |

Pending (wishlist): Hawkins vol. 2 (no text layer)

## Quintilian

Shelf: `pipeline/quintilian_shelf.json`. Butler Loeb 1920-22, 4 vols. (IA, 0.87-0.92; Latin facing).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Institutio Oratoria of Quintilian, vol. 1: Books I-III | H. E. Butler | `quintilian-butler-v1` | held: the scan is a reprint of the 1920 translation carrying a 'Bibliographical Addendum (1980)', which is not public domain; not fetched (see `_held`) |
| The Institutio Oratoria of Quintilian, vol. 2: Books IV-VI | H. E. Butler | `quintilian-butler-v2` | have-raw (IA `institutioorator02quin`) |
| The Institutio Oratoria of Quintilian, vol. 3: Books VII-IX | H. E. Butler | `quintilian-butler-v3` | have-raw (IA `institutioorator03quinuoft`) |
| The Institutio Oratoria of Quintilian, vol. 4: Books X-XII | H. E. Butler | `quintilian-butler-v4` | have-raw (IA `institutioorator04quinuoft`) |
| The Institutio Oratoria of Quintilian, vol. 1: Books I-III (Loeb; imprint 'First printed 1921' [vol. I appeared 1920]; Latin facing) | H. E. Butler | `quintilian-butler-v1-1921` | have-raw (IA `in.ernet.dli.2015.99822`) |
| Quintilian's Institutes of Oratory, vol. I (Bohn's Classical Library; London: George Bell, 1903, reprinted from stereotype plates of the 1856 edition) | John Selby Watson | `quintilian-watson-v1-1903` | have-raw (IA `cu31924075437685`) |
| Quintilian's Institutes of Oratory, vol. II (Bohn, 1856) | John Selby Watson | `quintilian-watson-v2-1856` | have-raw (IA `cu31924075437677`) |

Pending (wishlist): Watson's Bohn (no scan located)

## Vitruvius

Shelf: `pipeline/vitruvius_shelf.json`. Morgan 1914 (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Ten Books on Architecture | Morris Hicky Morgan | `vitruvius-morgan` | have (PG 20239) |
| The Architecture of Marcus Vitruvius Pollio, in Ten Books (London, Priestley and Weale, 1826) | Joseph Gwilt | `vitruvius-gwilt-1826` | have-raw (IA `architectureofma00vitruoft`) |

Pending (wishlist): none known

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

Pending (wishlist): none known.

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
| The Two Books on the Water Supply of the City of Rome (Boston, 1899) | Clemens Herschel | `frontinus-herschel-1899` | have-raw (IA `twobooksonwater01frongoog`) |

## Celsus

Shelf: `pipeline/celsus_shelf.json`. Greive, 1814 edition (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Of Medicine, in Eight Books | James Greive | `celsus-greive` | have (PG 64207) |

## Cato and Varro

Shelf: `pipeline/roman-farming_shelf.json`. Harrison, Roman Farm Management 1918 (Gutenberg); Columella, 1745 (IA, translator unnamed); Palladius in Middle English verse, c. 1420 (EETS, 1873).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Roman Farm Management: The Treatises of Cato and Varro | Fairfax Harrison | `cato-varro-harrison` | have (PG 12140) |
| L. Junius Moderatus Columella Of Husbandry, in twelve books, and his book concerning trees (London: A. Millar, 1745) | unnamed (not on the title page) | `columella-1745` | have-raw (IA `ljuniusmoderatus00colu`) |
| Palladius on Husbondrie, from the unique MS. of about 1420, Part I: the text (EETS o.s. 52, 1873), ed. Barton Lodge; Part II (o.s. 72, 1879: notes, glossary, rhyme index) is not held | anonymous Middle English verse translator (c. 1420) | `palladius-husbondrie-1873` | have-raw (IA `palladiusonhusbo00palluoft`) |

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
| The History of Justin, taken out of the Four and Forty Books of Trogus Pompeius, 5th ed. (London, 1688) | Robert Codrington | `justin-codrington-1688` | have-raw (IA `historyjustinta00codrgoog`) |
| Velleius Paterculus, Compendium of Roman History; Res Gestae Divi Augusti (Loeb, first printed 1924; this scan a 1961 reprint; Latin facing) | Frederick W. Shipley | `velleius-shipley-res-gestae` | have-raw (IA `compendiumofroma00velluoft`) |

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
| The Roman Antiquities of Dionysius Halicarnassensis, vol. 1 (London, 1758) | Edward Spelman | `dionysius-spelman-v1` | have-raw (IA `romanantiquities01dion`) |
| The Roman Antiquities of Dionysius Halicarnassensis, vol. 2 (London, 1758) | Edward Spelman | `dionysius-spelman-v2` | have-raw (IA `romanantiquities02dion`) |
| The Roman Antiquities of Dionysius Halicarnassensis, vol. 3 (London, 1758) | Edward Spelman | `dionysius-spelman-v3` | have-raw (IA `romanantiquities03dion`) |
| The Roman Antiquities of Dionysius Halicarnassensis, vol. 4 (London, 1758) | Edward Spelman | `dionysius-spelman-v4` | have-raw (IA `romanantiquities04dion`) |

Pending (wishlist): none known (Spelman's Roman Antiquities, 1758, is held above)

## Augustus, Res Gestae

Shelf: `pipeline/augustus_shelf.json`. Fairley 1898 (Gutenberg).

| Work | Translator | Slug | Status |
|---|---|---|---|
| Monumentum Ancyranum: The Deeds of Augustus | ed. and William Fairley | `augustus-res-gestae-fairley` | have (PG 66595) |

## Longinus

Shelf: `pipeline/longinus_shelf.json`. Havell (1890), William Smith (1739; 1752 printing) and Prickard (1906). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| On the Sublime (1890) | H. L. Havell | `longinus-havell-sublime` | have (PG 17957) |
| Dionysius Longinus on the Sublime, translated from the Greek, with notes and observations (1752 printing) | William Smith | `longinus-smith-sublime` | have-raw (IA `dionysiuslongin00smitgoog`) |
| Longinus on the Sublime (Oxford, Clarendon Press, 1906) | A. O. Prickard | `longinus-prickard-sublime` | have-raw (IA `longinusonsublim0000aopr`) |

Pending (wishlist): Fyfe's Loeb (1927; Greek facing); the earlier English versions Smith's preface names (London, 1650s; Oxford, 1698), not located.

Excluded: Rhys Roberts's Demetrius On Style, 1902 (Greek facing, OCR 0.59-0.72)

## Cassiodorus

Shelf: `pipeline/cassiodorus_shelf.json`. Hodgkin's condensed Variae (1886). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Letters of Cassiodorus, being a condensed translation of the Variae Epistolae (1886) | Thomas Hodgkin | `cassiodorus-hodgkin-letters` | have (PG 18590) |

Pending (wishlist): a complete Variae in English (none PD known); the Institutiones and the Psalm commentary are lane A's if wanted.

## Maximus of Tyre

Shelf: `pipeline/maximus-tyrius_shelf.json`. Thomas Taylor's Dissertations (1804). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Dissertations of Maximus Tyrius, vols. 1-2 in one scan (London, 1804) | Thomas Taylor | `maximus-tyrius-taylor-dissertations` | have-raw (IA `bub_gb_YcYfAAAAMAAJ`) |

Pending (wishlist): none known

## Philostratus

Shelf: `pipeline/philostratus_shelf.json`. Berwick's Life of Apollonius (1809) and Phillimore's vol. 1 (1912). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Life of Apollonius of Tyana, translated from the Greek of Philostratus (London, 1809) | Edward Berwick | `philostratus-berwick-apollonius` | have-raw (IA `lifeofapollonius00phil`) |
| Philostratus, In Honour of Apollonius of Tyana, vol. 1 (Oxford, 1912) | J. S. Phillimore | `philostratus-phillimore-apollonius-v1` | have-raw (IA `philostratusinho00philuoft`) |

Pending (wishlist): Phillimore vol. 2 (1912; no scan found); the Lives of the Sophists and Imagines in a PD English version; Conybeare's Loeb (Greek facing).

## Manilius

Shelf: `pipeline/manilius_shelf.json`. Creech's verse Astronomicon (1697; translator attributed, not named in the scan). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Five Books of M. Manilius, done into English verse with notes (London, 1697) | Thomas Creech (attributed; not named in the scan) | `manilius-creech-1697` | have-raw (IA `bim_early-english-books-1641-1700_the-five-books-of-m-man_manilius-marcus_1697`) |

Pending (wishlist): a cleaner copy of Creech (1697 or 1700 printing)

## Valerius Maximus

Shelf: `pipeline/valerius-maximus_shelf.json`. The 1684 Memorable Acts and Sayings (dedication signed by Samuel Speed). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Q. Valerius Maximus, his Collections of the Memorable Acts and Sayings (London, 1684) | unnamed on the title page (dedication signed by Samuel Speed) | `valerius-maximus-speed-1684` | have-raw (IA `Q.ValeriusMaximusMemorableActsAndSayings`) |

Pending (wishlist): none known

## Late Greek poets (Callimachus, Aratus, Tryphiodorus, Musaeus)

Shelf: `pipeline/late-greek-poets_shelf.json`. Dodd's Callimachus (1755), three Aratus translators (1848, 1880, 1885), Merrick's Tryphiodorus (1739), Arnold's Musaeus. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Hymns of Callimachus, translated from the Greek into English verse, with select epigrams and the Coma Berenices (London; 1755 per the catalogue, the imprint date is lost in the OCR) | William Dodd | `callimachus-dodd-hymns` | have-raw (IA `hymnsofcallimach00call`) |
| The Phenomena and Diosemeia of Aratus, translated into English verse (London, Parker, 1848) | John Lamb | `aratus-lamb-phenomena` | have-raw (IA `phenomenadioseme00arat`) |
| The Skies and Weather-Forecasts of Aratus (London, Macmillan, 1880) | Edward Poste | `aratus-poste-skies` | have-raw (IA `skiesandweather01aratgoog`) |
| The Phainomena, or Heavenly Displays, of Aratus, done into English verse (1885) | Robert Brown Jr. | `aratus-brown-phainomena` | have-raw (IA `phainomenaorhea00aratgoog`) |
| The Destruction of Troy, being the sequel of the Iliad, translated from the Greek of Tryphiodorus (Oxford, 1739) | James Merrick | `tryphiodorus-merrick-destruction-of-troy` | have-raw (IA `bim_eighteenth-century_the-destruction-of-troy_tryphiodorus_1739`) |
| Hero and Leander, from the Greek of Musaeus (Cassell, Petter and Galpin) | Edwin Arnold | `musaeus-arnold-hero-leander` | have-raw (IA `heroleanderfromg00musaiala`) |
| Oppian's Halieuticks, of the Nature of Fishes and Fishing of the Ancients, in V Books (Oxford, 1722) | William Diaper and John Jones (attributed; the title page names no translator) | `oppian-diaper-jones-halieuticks` | have-raw (IA `bim_eighteenth-century_halieutica-english-o_oppian-of-cilicia_1722`) |
| Cassandra, translated from the original Greek of Lycophron, with notes (Cambridge, 1806) | Philip Yorke, Viscount Royston | `lycophron-royston-1806` | have-raw (IA `cassandra00lyco`) |

Pending (wishlist): Tytler's Callimachus (1793; a scan exists, date and edition not confirmed); Mair's Loebs (Greek facing).

Excluded: Mawer's Cynegeticks, 1736 (ECCO OCR 0.76)

## Vegetius

Shelf: `pipeline/vegetius_shelf.json`. Clarke's 1767 translation of the Epitoma rei militaris; translator from the catalogue title. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Military Institutions of Vegetius, in five books, translated from the original Latin, with a preface and notes (London, 1767) | John Clarke | `vegetius-clarke-1767` | have-raw (IA `bim_eighteenth-century_de-re-militari-english_vegetius-renatus-flaviu_1767`) |

Pending (wishlist): Milner's 1993 translation is in copyright, so it is not wanted.

## Propertius

Shelf: `pipeline/propertius_shelf.json`. Butler's Loeb (1912, Latin facing; the scan is the 1929 reprint) and Gantillon's Bohn prose (1895 reprint). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Propertius, with an English translation (Loeb, 1912; 1929 reprint) | H. E. Butler | `propertius-butler-loeb` | have-raw (IA `propertiuswithen00propuoft`) |
| The Elegies of Propertius, with notes, literally translated (Bohn, 1895 reprint) | P. J. F. Gantillon (select elegies in verse by Nott and Elton) | `propertius-gantillon-bohn` | have-raw (IA `elegiesofpropert00propiala`) |
| The Elegies of Sextus Propertius, translated into English verse (Edinburgh, 1875) | James Cranstoun | `propertius-cranstoun-1875` | have-raw (IA `elegiessextuspr00unkngoog`) |

Pending (wishlist): Phillimore's 1906 prose translation (Oxford), if a scan turns up.

## Zosimus

Shelf: `pipeline/zosimus_shelf.json`. The anonymous 1814 London translation of the New History. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The History of Count Zosimus, translated from the original Greek (London: J. Davis, 1814) | unnamed (not on the title page) | `zosimus-1814` | have-raw (IA `historyofcountzo00zosiuoft`) |

## Herodian

Shelf: `pipeline/herodian_shelf.json`. The 1629 English Herodian (attributed to James Maxwell; not named in the scan). EEBO OCR, noisy. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Herodian of Alexandria his History of Twenty Roman Caesars and Emperors, interpreted out of the Greek original (London, 1629) | attributed to James Maxwell (not named in the scan) | `herodian-1629` | have-raw (IA `bim_early-english-books-1475-1640_herodian-of-alexandria-h_herodian_1629`) |

Pending (wishlist): A cleaner eighteenth-century translation, if a scan turns up. The 1635 reissue (IA bim_early-english-books-1475-1640_herodian-of-alexandria-h_herodian_1635) is the same translation and was not added.

## Polyaenus

Shelf: `pipeline/polyaenus_shelf.json`. Shepherd's Stratagems of War (1793). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Polyaenus's Stratagems of War, translated from the original Greek (London: George Nicol, 1793) | R. Shepherd | `polyaenus-shepherd-1793` | have-raw (IA `bim_eighteenth-century_polynuss-stratagems-of_polyaenus-of-lampsacus_1793`) |

## Quintus Curtius

Shelf: `pipeline/curtius_shelf.json`. Brende's 1553 Historie (first edition) and Digby's 1714 History of the Wars of Alexander. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Historie of Quintus Curcius, conteyning the Actes of the greate Alexander (London, 1553) | John Brende | `curtius-brende-1553` | have-raw (IA `bim_early-english-books-1475-1640_the-historie-of-quintus-_curtius-rufus-q_1553`) |
| Quintus Curtius his History of the Wars of Alexander, with Freinshemius's supplement (London, 1714), vol. 1 | John Digby | `curtius-digby-1714-v1` | have-raw (IA `bim_eighteenth-century_quintus-curtius-his-hist_curtius-rufus-quintus_1714_1`) |
| Wars of Alexander, vol. 2 of Quintus Curtius his History of the Wars of Alexander (London, 1714) | John Digby | `curtius-digby-1714-v2` | have-raw (IA `bim_eighteenth-century_quintus-curtius-his-hist_curtius-rufus-quintus_1714_2`) |

Pending (wishlist): Later printings of Brende (1561, 1570, 1584, 1592, 1602) are the same translation and were not added; the 1747 'History of the wars of Alexander' (2 vols.) has not been identified.

## Jordanes

Shelf: `pipeline/jordanes_shelf.json`. Mierow's English Getica, twice: the clean 1908 thesis text and the 1915 Princeton book with commentary (raw IA). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Origin and Deeds of the Goths (Princeton, 1908) | Charles Christopher Mierow | `jordanes-mierow-getica-1908` | have (PG 14809) |
| The Gothic History of Jordanes in English Version, with an introduction and a commentary (Princeton, 1915) | Charles Christopher Mierow | `jordanes-mierow-gothic-history-1915` | have-raw (IA `gothichistoryofj00jorduoft`) |

Pending (wishlist): none known

## Sidonius Apollinaris

Shelf: `pipeline/sidonius_shelf.json`. O. M. Dalton's complete Letters (Oxford, 1915, 2 vols.), raw IA; the first English translation of the whole. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Letters of Sidonius, vol. 1 (Oxford, 1915) | O. M. Dalton | `sidonius-dalton-v1` | have-raw (IA `lettersofsidoniu01sido`) |
| The Letters of Sidonius, vol. 2 (Oxford, 1915) | O. M. Dalton | `sidonius-dalton-v2` | have-raw (IA `lettersofsidoniu02sido`) |

Pending (wishlist): none known

## Isaeus

Shelf: `pipeline/isaeus_shelf.json`. Sir William Jones's Speeches of Isaeus (1779), raw IA. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Speeches of Isaeus in Causes concerning the Law of Succession to Property at Athens (London, 1779) | William Jones | `isaeus-jones-1779` | have-raw (IA `speechesofisaeus00isae`) |
| On Behalf of Euphiletus | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-behalf-of-euphiletus` | have (Perseus TEI `tlg0017.tlg012.perseus-eng2`; markup CC BY-SA 4.0) |
| On The Estate Of Pyrrhus | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-the-estate-of-pyrrhus` | have (Perseus TEI `tlg0017.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |
| On The Estate of Apollodorus | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-the-estate-of-apollodorus` | have (Perseus TEI `tlg0017.tlg007.perseus-eng2`; markup CC BY-SA 4.0) |
| On The Estate of Aristarchus | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-the-estate-of-aristarchus` | have (Perseus TEI `tlg0017.tlg010.perseus-eng2`; markup CC BY-SA 4.0) |
| On The Estate of Ciron | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-the-estate-of-ciron` | have (Perseus TEI `tlg0017.tlg008.perseus-eng2`; markup CC BY-SA 4.0) |
| On The Estate of Cleonymus | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-the-estate-of-cleonymus` | have (Perseus TEI `tlg0017.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Estate of Astyphilus | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-the-estate-of-astyphilus` | have (Perseus TEI `tlg0017.tlg009.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Estate of Dicaeogenes | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-the-estate-of-dicaeogenes` | have (Perseus TEI `tlg0017.tlg005.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Estate of Hagnias | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-the-estate-of-hagnias` | have (Perseus TEI `tlg0017.tlg011.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Estate of Menecles | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-the-estate-of-menecles` | have (Perseus TEI `tlg0017.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Estate of Nicostratus | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-the-estate-of-nicostratus` | have (Perseus TEI `tlg0017.tlg004.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Estate of Philoctemon | Edward Seymour Forster (1962) | `isaeus-perseus-forster-on-the-estate-of-philoctemon` | have (Perseus TEI `tlg0017.tlg006.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): Forster's Loeb (1927; Greek facing)

Excluded: the ECCO copy (IA bim_eighteenth-century_the-speeches-of-isus-in_isaeus_1779): OCR 0.68, a worse scan of the same edition

## Herodas

Shelf: `pipeline/herodas_shelf.json`. Hugo Sharpley's verse Mimes, A Realist of the Aegean (1906), raw IA. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| A Realist of the Aegean: a verse-translation of the Mimes of Herodas (London, 1906) | Hugo Sharpley | `herodas-sharpley-1906` | have-raw (IA `cu31924026669642`) |

Pending (wishlist): Headlam and Knox (1922; Greek facing)

Excluded: realistofaegeanb00herorich (a second scan of the same 1906 book, slightly worse OCR)

## Rutilius Namatianus

Shelf: `pipeline/rutilius_shelf.json`. Keene's edition with George F. Savage-Armstrong's English verse (London, 1907; Latin facing), raw IA. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| De reditu suo libri duo: the Home-Coming of Rutilius Claudius Namatianus, ed. Charles Haines Keene (London, 1907) | George F. Savage-Armstrong (verse); ed. Charles Haines Keene | `rutilius-savage-armstrong-1907` | have-raw (IA `cu31924026546386`) |

Pending (wishlist): none known

## Solinus

Shelf: `pipeline/solinus_shelf.json`. Arthur Golding's Worthie Worke of Julius Solinus Polyhistor (London, 1587), raw IA (EEBO OCR, old spelling). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Worthie Worke of Julius Solinus Polyhistor (London, 1587) | Arthur Golding | `solinus-golding-1587` | have-raw (IA `bim_early-english-books-1475-1640_the-worthie-worke-of-jul_solinus-caius-julius_1587`) |

Pending (wishlist): none known

Excluded: the other EEBO copy (bim_early-english-books-1475-1640_the-excellent-worke-o_solinus-caius-jul_1587): OCR 0.66, a worse scan of the same edition

## Greek voyages (Periplus, Hanno)

Shelf: `pipeline/periploi_shelf.json`. Schoff's Periplus of the Erythraean Sea (1912) and Falconer's Voyage of Hanno (1797, with the Greek text), raw IA. McCrindle's Periplus (1879) is on the Arrian shelf. Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Periplus of the Erythraean Sea: Travel and Trade in the Indian Ocean by a Merchant of the First Century (New York, 1912) | Wilfred H. Schoff | `periplus-schoff-1912` | have-raw (IA `peripluserythra00schogoog`) |
| The Voyage of Hanno, translated and accompanied with the Greek text (London, 1797) | Thomas Falconer | `hanno-falconer-1797` | have-raw (IA `voyagehannotran00hanngoog`) |

Pending (wishlist): none known

## Historia Augusta

Shelf: `pipeline/historia-augusta_shelf.json`. Magie's Loeb vols. I-II from first printings (1921, 1924; IA, OCR 0.89-0.90; Latin facing). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Scriptores Historiae Augustae, with an English translation, vol. I (Loeb; London: Heinemann, New York: Putnam, MCMXXI; Latin facing) | David Magie | `historia-augusta-magie-v1` | have-raw (IA `scriptoreshistor0000unse`) |
| The Scriptores Historiae Augustae, with an English translation, vol. II (Loeb; London: Heinemann, New York: Putnam, MCMXXIV; Latin facing) | David Magie | `historia-augusta-magie-v2` | have-raw (IA `scriptores0000unse`) |

Pending (wishlist): vol. III (1932) is after the 1930 line.

## Fronto

Shelf: `pipeline/fronto_shelf.json`. Haines's Loeb, the first English Fronto, vols. I-II from first printings (1919, 1920; IA, OCR 0.82-0.83; Latin facing, some letters in Greek). Not minted.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Correspondence of Marcus Cornelius Fronto with Marcus Aurelius Antoninus, Lucius Verus, Antoninus Pius and various friends, vol. I (Loeb; London: Heinemann, New York: Putnam, MCMXIX) | C. R. Haines | `fronto-haines-v1` | have-raw (IA `correspondenceof01fronuoft`) |
| The Correspondence of Marcus Cornelius Fronto with Marcus Aurelius Antoninus, Lucius Verus, Antoninus Pius and various friends, vol. II (Loeb; London: Heinemann, New York: Putnam, MCMXX) | C. R. Haines | `fronto-haines-v2` | have-raw (IA `correspondenceof0002crha_r5s5`) |

Pending (wishlist): none: vol. II's 1929 revision (seen only in a 1988 reprint) was not taken; the 1920 first printing is held.

## Aeschines

Shelf: `pipeline/aeschines_shelf.json`. New shelf 2026-10-03: the three speeches in Adams's Loeb translation (1919), English-only Perseus TEI.

| Work | Translator | Slug | Status |
|---|---|---|---|
| Against Timarchus | Charles Darwin Adams (Loeb 1919) | `aeschines-perseus-adams-against-timarchus` | have (Perseus TEI `tlg0026.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |
| On the Embassy | Charles Darwin Adams (Loeb 1919) | `aeschines-perseus-adams-on-the-embassy` | have (Perseus TEI `tlg0026.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |
| Against Ctesiphon | Charles Darwin Adams (Loeb 1919) | `aeschines-perseus-adams-against-ctesiphon` | have (Perseus TEI `tlg0026.tlg003.perseus-eng2`; markup CC BY-SA 4.0) |

Pending (wishlist): an older English Aeschines (pre-1900), if a clean scan turns up.

## Apollodorus

Shelf: `pipeline/apollodorus_shelf.json`. New shelf 2026-10-03: Frazer's Loeb Library (1921), English-only Perseus TEI with Frazer's notes.

| Work | Translator | Slug | Status |
|---|---|---|---|
| The Library | Sir James George Frazer (Loeb 1921) | `apollodorus-perseus-frazer-library` | have (Perseus TEI `tlg0548.tlg001.perseus-eng2`; markup CC BY-SA 4.0) |
| Epitome | James George Frazer (1921) | `apollodorus-perseus-frazer-epitome` | have (Perseus TEI `tlg0548.tlg002.perseus-eng2`; markup CC BY-SA 4.0) |

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

## Rossetti (Vita Nuova, Early Italian Poets)

Shelf: `pipeline/rossetti_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rossetti` · titles `python3 pipeline/split_shelf_titles.py rossetti`.
Round 4, lane C's choice under the coordinator's standing instruction; vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rossetti-vita-nuova` | Dante | La Vita Nuova (The New Life) | Dante Gabriel Rossetti | 1861 | have | PG 41085 |
| `rossetti-early-italian-poets` | Ciullo d'Alcamo, Guido Guinizelli, Guido Cavalcanti, Cino da Pistoia, Dante and others | The Early Italian Poets (Part I: poets before Dante; Part II: Dante and his circle, incl. the Vita Nuova) | Dante Gabriel Rossetti | 1861 | have-raw | IA `earlyitalianpo00rossuoft` |
| `rossetti-dante-and-his-circle-1874` | — | The 1874 rearranged edition (Ellis & White): a second witness of the same translations; not fetched. | — | — | pending | — |
| — | — | original-poems: Rossetti's own poems (House of Life etc.): not translations. | — | — | excluded | — |

## Fairfax (Tasso)

Shelf: `pipeline/fairfax_shelf.json` · fetch `python3 pipeline/fetch_shelf.py fairfax` · titles `python3 pipeline/split_shelf_titles.py fairfax`.
Round 4, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `fairfax-jerusalem-delivered` | Tasso | Jerusalem Delivered (Gerusalemme Liberata), 20 books | Edward Fairfax | 1600 | have | PG 392 |

## W. S. Rose (Ariosto)

Shelf: `pipeline/rose_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rose` · titles `python3 pipeline/split_shelf_titles.py rose`.
Round 4, vetoable. Gutenberg text placed by hand (its cache URL 404s); the URL is in the shelf's `_manual_fetch`. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rose-orlando-furioso` | Ariosto | Orlando Furioso, 46 cantos | William Stewart Rose | 1831 | have | PG 615 |

## Shelton (Don Quixote)

Shelf: `pipeline/shelton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py shelton` · titles `python3 pipeline/split_shelf_titles.py shelton`.
Round 4, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `shelton-don-quixote` | Cervantes | Don Quixote, Parts I-II | Thomas Shelton | 1612-1620 | have-raw | IA `historyofvalorou00cerv` + IA `historyofvalorou02cerviala` + IA `historyofvalorou03cerviala` |
| `shelton-1612-1620-originals` | — | The 1612 and 1620 first editions are on IA (cervantessheltondonquixote01/02): early-modern OCR; not fetched. | — | — | pending | — |

## C. E. Norton (Dante, prose)

Shelf: `pipeline/norton_shelf.json` · fetch `python3 pipeline/fetch_shelf.py norton` · titles `python3 pipeline/split_shelf_titles.py norton`.
Round 4, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `norton-hell` | Dante | Inferno (Hell), prose | Charles Eliot Norton | 1891 | have-raw | IA `divinecomedyofda01dantiala` |
| `norton-purgatory` | Dante | Purgatorio, prose | Charles Eliot Norton | 1892 | have-raw | IA `divinecomedyofda02dantiala` |
| `norton-paradise` | Dante | Paradiso, prose | Charles Eliot Norton | 1892 | have-raw | IA `divinecomedyofda03dantiala` |
| `norton-new-life` | Dante | La Vita Nuova (The New Life) | Charles Eliot Norton | 1867 | have-raw | IA `newlifeofdanteal00dant_1` |

## John Payne (Villon, Decameron)

Shelf: `pipeline/payne_shelf.json` · fetch `python3 pipeline/fetch_shelf.py payne` · titles `python3 pipeline/split_shelf_titles.py payne`.
Round 4, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `payne-decameron` | Boccaccio | The Decameron | John Payne | 1886 | have | PG 23700 |
| `payne-villon` | Villon | Poems (Lesser and Greater Testament, Ballades) | John Payne | 1878 | have-raw | IA `poemsofmasterfra00villiala` |
| `payne-thousand-nights` | — | Payne's Book of the Thousand Nights and One Night (Villon Society 1882-84, 9 vols): Burton's and Lane's are already shelved; the IA set is incomplete and not fetched. Your call. | — | — | pending | — |
| `payne-bandello` | — | Novels of Matteo Bandello (1890, 6 vols): on IA; not fetched this run. | — | — | pending | — |

## Carlyle as translator (Goethe, German tales)

Shelf: `pipeline/carlyle_shelf.json` · fetch `python3 pipeline/fetch_shelf.py carlyle` · titles `python3 pipeline/split_shelf_titles.py carlyle`.
Round 4, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `carlyle-wilhelm-meister` | Goethe | Wilhelm Meister's Apprenticeship and Travels | Thomas Carlyle | 1824-1827 | have | PG 36483 + PG 78139 |
| `carlyle-german-tales` | Musaeus, Tieck, Richter | German Romance tales | Thomas Carlyle | 1827 | have | PG 38779 |
| — | — | carlyle-own-works: Sartor Resartus, The French Revolution etc.: Carlyle's own works, not translations. | — | — | excluded | — |

## Jeremiah Curtin (Sienkiewicz)

Shelf: `pipeline/curtin_shelf.json` · fetch `python3 pipeline/fetch_shelf.py curtin` · titles `python3 pipeline/split_shelf_titles.py curtin`.
Round 5, lane C's choice; vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `curtin-quo-vadis` | Sienkiewicz | Quo Vadis | Jeremiah Curtin | 1896 | have | PG 2853 |
| `curtin-with-fire-and-sword` | Sienkiewicz | With Fire and Sword (Trilogy I) | Jeremiah Curtin | 1890 | have | PG 37027 |
| `curtin-the-deluge` | Sienkiewicz | The Deluge (Trilogy II) | Jeremiah Curtin | 1891 | have | PG 37198 + PG 37308 |
| `curtin-pan-michael` | Sienkiewicz | Pan Michael (Trilogy III) | Jeremiah Curtin | 1893 | have | PG 37361 |
| `curtin-on-the-field-of-glory` | Sienkiewicz | On the Field of Glory | Jeremiah Curtin | 1906 | have | PG 37406 |
| `curtin-knights-of-the-cross` | — | The Knights of the Cross (1900): Gutenberg's edition is not Curtin's; no Curtin scan checked this run. | — | — | pending | — |
| `curtin-myths` | — | Curtin's own collections of Irish, Russian and Native American myths: his own fieldwork rather than translations of a work; left out. | — | — | pending | — |

## Isabel Hapgood (Hugo, Gorky, Turgenev, Bunin)

Shelf: `pipeline/hapgood_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hapgood` · titles `python3 pipeline/split_shelf_titles.py hapgood`.
Round 5, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hapgood-les-miserables` | Hugo | Les Misérables | Isabel F. Hapgood | 1887 | have | PG 135 |
| `hapgood-gorky-orloff` | Gorky | Orlóff and His Wife: Tales of the Barefoot Brigade | Isabel F. Hapgood | 1901 | have | PG 55636 |
| `hapgood-bunin-village` | Bunin | The Village | Isabel F. Hapgood | 1923 | have | PG 59981 |
| `hapgood-turgenev-first-love` | Turgenev | First Love, and Other Stories | Isabel F. Hapgood | 1904 | have | PG 56878 |
| `hapgood-turgenev-superfluous-man` | Turgenev | The Diary of a Superfluous Man, and Other Stories | Isabel F. Hapgood | 1904 | have | PG 41201 |
| `hapgood-turgenev-reckless-character` | Turgenev | A Reckless Character, and Other Stories | Isabel F. Hapgood | 1904 | have | PG 15994 |
| `hapgood-turgenev-nobleman` | Turgenev | A Nobleman's Nest | Isabel F. Hapgood | 1903 | have | PG 25771 |
| `hapgood-tolstoy` | — | Hapgood's Tolstoy (Childhood, Boyhood, Youth 1886; Sevastopol 1888): not on Gutenberg in her version; IA not checked this run. | — | — | pending | — |

## James Legge (Chinese classics)

Shelf: `pipeline/legge_shelf.json` · fetch `python3 pipeline/fetch_shelf.py legge` · titles `python3 pipeline/split_shelf_titles.py legge`.
Round 5, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `legge-tao-teh-king` | Laozi | Tao Te Ching | James Legge | 1891 | have | PG 216 |
| `legge-analects` | Confucius | Analects | James Legge | 1861 | have | PG 3330 |
| `legge-faxian` | Faxian | A Record of Buddhistic Kingdoms | James Legge | 1886 | have | PG 2124 |
| `legge-sacred-books` | — | The rest of Legge's Sacred Books of the East (Shu King, Shih King, Yi King, Li Ki, Zhuangzi: SBE 3, 16, 27-28, 39-40): on IA, not fetched this run. | — | — | pending | — |
| — | — | pg-3100-4094: Gutenberg 3100 and 4094 are the Chinese-language text of the Chinese Classics, not the translation. | — | — | excluded | — |

## H. A. and Lionel Giles (Chinese)

Shelf: `pipeline/giles_shelf.json` · fetch `python3 pipeline/fetch_shelf.py giles` · titles `python3 pipeline/split_shelf_titles.py giles`.
Round 5, vetoable. Lionel Giles is US PD only (UK until end-2028). Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `giles-chuang-tzu` | Zhuangzi | Chuang Tzu | Herbert A. Giles | 1889 | have | PG 59709 |
| `giles-strange-stories` | Pu Songling | Strange Stories from a Chinese Studio | Herbert A. Giles | 1880 | have | PG 43629 |
| `giles-art-of-war` | Sunzi | The Art of War | Lionel Giles | 1910 | have | PG 132 |
| `giles-sayings-of-confucius` | Confucius | The Sayings of Confucius | Lionel Giles | 1907 | have | PG 46389 |
| — | — | giles-own-works: H. A. Giles's History of Chinese Literature and China and the Chinese: his own works. | — | — | excluded | — |

## Arthur Waley (pre-1931 only)

Shelf: `pipeline/waley_shelf.json` · fetch `python3 pipeline/fetch_shelf.py waley` · titles `python3 pipeline/split_shelf_titles.py waley`.
Round 5, vetoable. 🔴 US PD only: UK copyright runs to the end of 2036. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `waley-170-chinese-poems` | Chinese poets | A Hundred and Seventy Chinese Poems | Arthur Waley | 1918 | have | PG 42290 |
| `waley-more-translations` | Chinese poets | More Translations from the Chinese | Arthur Waley | 1919 | have | PG 16500 |
| `waley-li-po` | Li Bai | The Poet Li Po | Arthur Waley | 1919 | have | PG 43274 |
| `waley-no-plays` | Zeami and others | The No Plays of Japan | Arthur Waley | 1921 | have | PG 43304 |
| `waley-genji-1-3` | Murasaki Shikibu | The Tale of Genji, parts 1-3 (The Tale of Genji; The Sacred Tree; A Wreath of Cloud) | Arthur Waley | 1925-1927 | have | PG 66057 + PG 67111 + PG 75852 |
| `waley-pillow-book` | Sei Shonagon | The Pillow-Book of Sei Shonagon | Arthur Waley | 1928 | have | PG 76016 |
| `waley-genji-4-6` | — | Genji parts 4-6 (Blue Trousers 1928, The Lady of the Boat 1932, The Bridge of Dreams 1933): part 4 is US PD but not on Gutenberg; parts 5-6 are after 1930 and are refused. | — | — | pending | — |
| — | — | waley-after-1930: The Way and its Power (1934), the Analects (1938), Monkey (1942): still in copyright. | — | — | excluded | — |

## John Hoole (Tasso)

Shelf: `pipeline/hoole_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hoole` · titles `python3 pipeline/split_shelf_titles.py hoole`.
Round 5, vetoable. 1803 printing still uses the long s (OCR reads s as f). Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hoole-jerusalem-delivered` | Tasso | Jerusalem Delivered, 20 books | John Hoole | 1763 | have-raw | IA `jerusalemdeliver01tassiala` + IA `jerusalemdeliver02tassiala` |
| `hoole-orlando-furioso` | — | Hoole's Ariosto (1783): only 18th-century long-s printings and incomplete Google sets of the 1807 edition found. Not fetched. | — | — | pending | — |

## Sir John Harington (Ariosto, 1591)

Shelf: `pipeline/harington_shelf.json` · fetch `python3 pipeline/fetch_shelf.py harington` · titles `python3 pipeline/split_shelf_titles.py harington`.
Round 5, vetoable. Early-modern OCR, 66% of tokens in a modern vocabulary: a defect. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `harington-orlando-furioso` | Ariosto | Orlando Furioso, 46 books | Sir John Harington | 1591 | have-raw | IA `orlandofuriosoin00ario_0` |

## F. Max Müller (Upanishads, Dhammapada)

Shelf: `pipeline/muller_shelf.json` · fetch `python3 pipeline/fetch_shelf.py muller` · titles `python3 pipeline/split_shelf_titles.py muller`.
Round 6, lane C's choice; vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `muller-upanishads` | Upanishads | The Upanishads (twelve principal Upanishads) | F. Max Müller | 1879-1884 | have-raw | IA `upanishads01mluoft` + IA `p2upanishads00mluoft` |
| `muller-dhammapada` | Dhammapada | Dhammapada | F. Max Müller | 1881 | have | PG 2017 |
| `muller-rig-veda-1869` | — | Müller's Rig-Veda-Sanhita vol. 1 (hymns to the Maruts, 1869): only that volume was ever published; not fetched. | — | — | pending | — |

## Sir Edwin Arnold (Bhagavad Gita)

Shelf: `pipeline/edwin-arnold_shelf.json` · fetch `python3 pipeline/fetch_shelf.py edwin-arnold` · titles `python3 pipeline/split_shelf_titles.py edwin-arnold`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `edwin-arnold-bhagavad-gita` | Bhagavad Gita | The Song Celestial (Bhagavad Gita) | Sir Edwin Arnold | 1885 | have | PG 2388 |
| `edwin-arnold-indian-idylls` | — | Indian Idylls (1883, episodes of the Mahabharata): not on Gutenberg; IA not checked this run. | — | — | pending | — |
| — | — | light-of-asia: The Light of Asia (1879): Arnold's own poem. | — | — | excluded | — |

## R. T. H. Griffith (Ramayana, Rigveda)

Shelf: `pipeline/griffith_shelf.json` · fetch `python3 pipeline/fetch_shelf.py griffith` · titles `python3 pipeline/split_shelf_titles.py griffith`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `griffith-ramayana` | Valmiki | The Ramayana | Ralph T. H. Griffith | 1870 | have | PG 24869 |
| `griffith-rigveda` | Rigveda | The Hymns of the Rigveda, 10 mandalas | Ralph T. H. Griffith | 1889 | have-raw | IA `in.ernet.dli.2015.195721` + IA `in.ernet.dli.2015.195722` |
| `griffith-atharvaveda` | — | Hymns of the Atharva-veda (1895-96), the Samaveda (1893), the White Yajurveda (1899): on IA; not fetched this run. | — | — | pending | — |

## J. M. Rodwell (Koran)

Shelf: `pipeline/rodwell_shelf.json` · fetch `python3 pipeline/fetch_shelf.py rodwell` · titles `python3 pipeline/split_shelf_titles.py rodwell`.
Round 6, vetoable. Suras in his chronological order. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `rodwell-koran` | The Qur'an | The Koran | J. M. Rodwell | 1861 | have | PG 2800 |
| — | — | pg-3434: Gutenberg 3434 is the same Rodwell translation (an older file); not fetched twice. | — | — | excluded | — |

## George Sale (Koran)

Shelf: `pipeline/sale_shelf.json` · fetch `python3 pipeline/fetch_shelf.py sale` · titles `python3 pipeline/split_shelf_titles.py sale`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `sale-koran` | The Qur'an | The Koran | George Sale | 1734 | have | PG 7440 |
| `sale-preliminary-discourse` | — | Sale's Preliminary Discourse (his long introduction): check whether PG 7440 carries it; if not, a scan of an 1825+ edition. | — | — | pending | — |

## E. H. Palmer (Qur'an)

Shelf: `pipeline/palmer_shelf.json` · fetch `python3 pipeline/fetch_shelf.py palmer` · titles `python3 pipeline/split_shelf_titles.py palmer`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `palmer-quran` | The Qur'an | The Qur'an | E. H. Palmer | 1880 | have-raw | IA `1922707.0006.001.umich.edu` + IA `thequraan09unknuoft` |
| — | — | qurn01unkngoog: Google copy of part II, a duplicate of the Toronto copy (both hold chapters XVII-CXIV; found in the second review round 2026-10-03). Toronto kept for its better OCR. | — | — | excluded | — |

## E. H. Whinfield (Rumi's Masnavi)

Shelf: `pipeline/whinfield_shelf.json` · fetch `python3 pipeline/fetch_shelf.py whinfield` · titles `python3 pipeline/split_shelf_titles.py whinfield`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `whinfield-masnavi` | Rumi | Masnavi (abridged) | E. H. Whinfield | 1887 | have-raw | IA `cu31924026910251` |
| `whinfield-omar` | — | Whinfield's Omar Khayyam quatrains are inside Gutenberg 38511, a 1903 compilation with FitzGerald's and Nicolas's versions; it would need cutting by marker. Not fetched. | — | — | pending | — |

## R. A. Nicholson (Rumi, Hujwiri)

Shelf: `pipeline/nicholson_shelf.json` · fetch `python3 pipeline/fetch_shelf.py nicholson` · titles `python3 pipeline/split_shelf_titles.py nicholson`.
Round 6, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `nicholson-kashf-al-mahjub` | Hujwiri | Kashf al-Mahjub | Reynold A. Nicholson | 1911 | have | PG 64786 |
| `nicholson-divani-shamsi-tabriz` | Rumi | Selected Poems from the Divani Shamsi Tabriz | Reynold A. Nicholson | 1898 | have-raw | IA `india.history.resource.111025` |
| `nicholson-mathnawi` | — | The Mathnawi translation (Gibb series, 1925-40): vols 1-2 (1926, 1930) are US PD; the rest are not. Not fetched. | — | — | pending | — |

## Southey as translator (Amadis, the Cid)

Shelf: `pipeline/southey_shelf.json` · fetch `python3 pipeline/fetch_shelf.py southey` · titles `python3 pipeline/split_shelf_titles.py southey`.
Round 7, lane C's choice; vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `southey-chronicle-of-the-cid` | Chronicle of the Cid (Crónica del Cid and others) | Chronicle of the Cid | Robert Southey | 1808 | have | PG 8491 |
| `southey-amadis-of-gaul` | Lobeira / Montalvo | Amadis of Gaul, 4 vols | Robert Southey | 1803 | have-raw | IA `amadisofgaul01lobeuoft` + PG 51099 + PG 52941 + PG 55005 |
| — | — | southey-own-poems: Thalaba, Madoc, the Life of Nelson etc.: Southey's own works. | — | — | excluded | — |

## Coleridge as translator (Wallenstein)

Shelf: `pipeline/coleridge_shelf.json` · fetch `python3 pipeline/fetch_shelf.py coleridge` · titles `python3 pipeline/split_shelf_titles.py coleridge`.
Round 7, vetoable. Gutenberg text placed by hand (cache URL 404s), see `_manual_fetch`. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `coleridge-piccolomini` | Schiller | The Piccolomini (Wallenstein, part 2) | Samuel Taylor Coleridge | 1800 | have | PG 6786 |
| `coleridge-death-of-wallenstein` | Schiller | The Death of Wallenstein (Wallenstein, part 3) | Samuel Taylor Coleridge | 1800 | have | PG 6787 |
| — | — | wallensteins-lager: Wallenstein's Camp (part 1) was not translated by Coleridge. | — | — | excluded | — |

## John and E. A. Bowring (Chamisso, Goethe, Heine)

Shelf: `pipeline/bowring_shelf.json` · fetch `python3 pipeline/fetch_shelf.py bowring` · titles `python3 pipeline/split_shelf_titles.py bowring`.
Round 7, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `bowring-peter-schlemihl` | Chamisso | Peter Schlemihl | John Bowring | 1824 | have | PG 21943 |
| `bowring-goethe-poems` | Goethe | Poems, in the original metres | Edgar Alfred Bowring | 1853 | have | PG 1287 |
| `bowring-heine-poems` | Heine | Poems, complete | Edgar Alfred Bowring | 1859 | have | PG 52882 |
| `john-bowring-anthologies` | — | Sir John Bowring's Specimens of the Russian Poets (1821-23), Servian Popular Poetry (1827), Poetry of the Magyars (1830): on IA; not fetched this run. | — | — | pending | — |

## John Anster (Faust I)

Shelf: `pipeline/anster_shelf.json` · fetch `python3 pipeline/fetch_shelf.py anster` · titles `python3 pipeline/split_shelf_titles.py anster`.
Round 7, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `anster-faust-part-1` | Goethe | Faust, Part I (verse) | John Anster | 1835 | have-raw | IA `firstpartgoethe00anstgoog` |
| `anster-faust-part-2` | — | Anster's Part II (1864): not fetched this run. | — | — | pending | — |
| — | — | fausttransanster00goetuoft: IA catalogues it as Anster's (Harper 1886), but its title page reads 'translated into English verse ... by John Stuart Blackie', Macmillan 1880: a different translation. Refused by the identity gate 2026-10-03. | — | — | excluded | — |

## Abraham Hayward (Faust I, prose)

Shelf: `pipeline/hayward_shelf.json` · fetch `python3 pipeline/fetch_shelf.py hayward` · titles `python3 pipeline/split_shelf_titles.py hayward`.
Round 7, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `hayward-faust-part-1` | Goethe | Faust, Part I (prose) | Abraham Hayward | 1833 | have-raw | IA `faustdramatichay00goetuoft` |

## P. H. Wicksteed (Paradiso, Convivio)

Shelf: `pipeline/wicksteed_shelf.json` · fetch `python3 pipeline/fetch_shelf.py wicksteed` · titles `python3 pipeline/split_shelf_titles.py wicksteed`.
Round 7, vetoable. Paradiso has the Italian facing: OCR mixes both. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `wicksteed-paradiso` | Dante | Paradiso (prose, Italian facing) | Philip H. Wicksteed | 1899 | have-raw | IA `paradisoofdantea00dantuoft` |
| `wicksteed-convivio` | Dante | Convivio | Philip H. Wicksteed | 1903 | have-raw | IA `convivioofdantea00dant` |
| `wicksteed-latin-works` | — | The Latin Works of Dante (Temple Classics 1904): Wicksteed did the letters and eclogues, A. G. Ferrers Howell the rest; translator per piece needed. Not fetched. | — | — | pending | — |
| — | — | six-sermons: Dante: Six Sermons (PG 36479): Wicksteed's own work. | — | — | excluded | — |

## J. C. Mangan (German Anthology)

Shelf: `pipeline/mangan_shelf.json` · fetch `python3 pipeline/fetch_shelf.py mangan` · titles `python3 pipeline/split_shelf_titles.py mangan`.
Round 7, vetoable. Not converted to unit-id JSON; **no uids minted**.

| Title slug | Author | Work | Translator | Tr. | Status | Source |
|---|---|---|---|---|---|---|
| `mangan-german-anthology` | Goethe, Schiller, Uhland, Rückert and others | Anthologia Germanica (German Anthology) | James Clarence Mangan | 1845 | have-raw | IA `anthologiagerma02manggoog` + IA `anthologiagerma03manggoog` |
| `mangan-irish` | — | Mangan's translations from the Irish (The Poets and Poetry of Munster, 1849): not fetched. | — | — | pending | — |
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
| Devil-Dancers, Witch-Finders, Rain-Makers, and Medicine-Men (1896) | held (not his: "compiled from Lang, Caldwell, Conway, Tylor, … and others") | IA `devildancerswitc00lang` |
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

## W. R. S. Ralston (Russian and Tibetan tales)

Shelf: `pipeline/ralston_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Russian Fairy Tales (1873), and Tibetan Tales (1906), Ralston's English of Schiefner's German from the Kah-gyur, cut by numbered tale. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Russian Fairy Tales: A Choice Collection of Muscovite Folk-lore, tr. W. R. S. Ralston (1873) | have | PG 22373, `ralston-russian-fairy-tales` (3485 units) |
| Tibetan Tales, Derived from Indian Sources, tr. Ralston from Schiefner's German (1906) | have | PG 66870, `ralston-tibetan-tales` (1848 units) |
| ralston-other-translations | excluded | Turgenev's Liza (PG 12194), tr. Ralston: outside the relay's ask (Russian tales) |
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
| Beowulf: An Anglo-Saxon Epic Poem, tr. J. Lesslie Hall (1892) | held on main | PG 16328 is slug `beowulf` in fetch_sources.py; not fetched twice (was `beowulf-hall`) |
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
| The Elder Eddas of Saemund Sigfusson, tr. Benjamin Thorpe, and the Younger Eddas of Snorre Sturleson, tr. I. A. Blackwell (Norrœna Society, 1906) | have | PG 14726, `edda-thorpe-blackwell` (3027 units) |
| The Story of the Volsungs (Volsunga Saga), with Excerpts from the Poetic Edda, tr. Eiríkr Magnússon and William Morris | have | PG 1152, `edda-volsunga-morris` (1288 units) |
| edda-retellings | excluded | Faraday's The Edda (PG 13007-13008), Wilmot-Buxton (29551): studies and retellings; Guerber's Myths of the Norsemen (28497) is held on guerber_shelf.json |
| edda-prose | excluded | Snorri's Prose (Younger) Edda is on the Sturluson shelf |

## The Kalevala (Crawford)

Shelf: `pipeline/kalevala_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). John Martin Crawford's 1888 translation, the complete Gutenberg file, cut by its fifty runes. The two-volume Gutenberg split of the same text and Kirby's later translation are not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Kalevala: The Epic Poem of Finland, tr. John Martin Crawford (1888) | have | PG 5186, `kalevala-crawford` (1534 units) |
| Kalevala, The Land of the Heroes, tr. W. F. Kirby (1907), vol. 1 | have | PG 25953, `kalevala-kirby-1` (1627 units) |
| Kalevala, The Land of the Heroes, tr. W. F. Kirby (1907), vol. 2 | have | PG 33089, `kalevala-kirby-2` (1561 units) |
| kalevala-duplicates | excluded | Crawford's Kalevala volumes 1 and 2 (PG 5184, 5185): the same text as the complete file |

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
| Stories of Red Hanrahan (1904) | have | PG 5793, `yeats-stories-of-red-hanrahan` (140 units) |
| The Secret Rose (1897) | have | PG 5795, `yeats-secret-rose` (160 units) |
| yeats-poems-plays | excluded | Yeats's poems, plays, essays and autobiographies: outside a storytellers shelf (a poets' lane would hold them) |
| yeats-stories | excluded | Rosa Alchemica (PG 5794) and John Sherman and Dhoya (49109): his other fiction; Rosa Alchemica is an occult story, John Sherman a novel. Red Hanrahan and The Secret Rose are held: tales built on Irish folk material |

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

## Mary Mapes Dodge

Shelf: `pipeline/dodge_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Hans Brinker, cut by its own Contents. The St. Nicholas issues she edited are not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Hans Brinker; or, The Silver Skates (1865) | have | PG 764, `dodge-hans-brinker` (2093 units) |
| dodge-duplicate | excluded | Hans Brinker (PG 34378): a later illustrated printing |
| dodge-st-nicholas | excluded | the St. Nicholas magazine issues she edited: many authors, not hers |

## L. M. Montgomery

Shelf: `pipeline/montgomery_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her Prince Edward Island books published before 1931, cut by their own chapter lines. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Anne of Green Gables (1908) | have | PG 45, `montgomery-anne-of-green-gables` (1793 units) |
| Anne of Avonlea (1909) | have | PG 47, `montgomery-anne-of-avonlea` (1712 units) |
| Anne of the Island (1915) | have | PG 51, `montgomery-anne-of-the-island` (1766 units) |
| Anne's House of Dreams (1917) | have | PG 544, `montgomery-annes-house-of-dreams` (1612 units) |
| Rainbow Valley (1919) | have | PG 5343, `montgomery-rainbow-valley` (1639 units) |
| Rilla of Ingleside (1921) | have | PG 3796, `montgomery-rilla-of-ingleside` (1771 units) |
| Chronicles of Avonlea (1912) | have | PG 1354, `montgomery-chronicles-of-avonlea` (1302 units) |
| Further Chronicles of Avonlea (1920) | have | PG 5340, `montgomery-further-chronicles-of-avonlea` (1457 units) |
| The Story Girl (1911) | have | PG 5342, `montgomery-story-girl` (2145 units) |
| The Golden Road (1913) | have | PG 316, `montgomery-golden-road` (1952 units) |
| Kilmeny of the Orchard (1910) | have | PG 5341, `montgomery-kilmeny-of-the-orchard` (763 units) |
| Emily of New Moon (1923) | have | PG 61236, `montgomery-emily-of-new-moon` (2422 units) |
| The Blue Castle (1926) | have | PG 67979, `montgomery-blue-castle` (1530 units) |
| montgomery-duplicate | excluded | Anne of Green Gables (PG 64365): a later illustrated printing |
| montgomery-short-stories | excluded | the six magazine short-story gatherings (PG 24873-24878): candidates for a later batch |

## Kate Douglas Wiggin

Shelf: `pipeline/wiggin_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her children's books; New Chronicles of Rebecca nested chronicle > part. The anthologies she edited are not taken (other people's texts). Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Rebecca of Sunnybrook Farm (1903) | have | PG 498, `wiggin-rebecca-of-sunnybrook-farm` (1292 units) |
| New Chronicles of Rebecca (1907) | have | PG 1375, `wiggin-new-chronicles-of-rebecca` (1195 units) |
| The Birds' Christmas Carol (1887) | have | PG 721, `wiggin-birds-christmas-carol` (215 units) |
| Mother Carey's Chickens (1911) | have | PG 10540, `wiggin-mother-careys-chickens` (1342 units) |
| Timothy's Quest (1890) | have | PG 18531, `wiggin-timothys-quest` (560 units) |
| Polly Oliver's Problem (1893) | have | PG 15630, `wiggin-polly-olivers-problem` (783 units) |
| wiggin-duplicate | excluded | The Birds' Christmas Carol (PG 24286): a second transcription |
| wiggin-anthologies | excluded | the anthologies she edited with Nora Archibald Smith (The Fairy Ring, Tales of Laughter, Tales of Wonder, The Arabian Nights, Pinafore Palace, The Posy Ring, Golden Numbers): other people's texts, which other shelves hold at source |
| wiggin-adult | excluded | Penelope books, A Cathedral Courtship and her other adult fiction, and her kindergarten writings: not children's classics |

## Juliana Horatia Ewing

Shelf: `pipeline/ewing_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her stories for children; the Jackanapes volume nested story > chapter or scene. Two volumes measured as contained in Lob Lie-by-the-Fire are excluded, not held twice. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Jackanapes, Daddy Darwin's Dovecot and Other Stories | have | PG 7865, `ewing-jackanapes-and-other-stories` (745 units) |
| Old-Fashioned Fairy Tales (1882) | have | PG 15592, `ewing-old-fashioned-fairy-tales` (878 units) |
| Lob Lie-by-the-Fire, The Brownies and Other Tales | have | PG 62783, `ewing-lob-lie-by-the-fire` (2156 units) |
| Jan of the Windmill (1876) | have | PG 5601, `ewing-jan-of-the-windmill` (1542 units) |
| Mrs. Overtheway's Remembrances (1869) | have | PG 17772, `ewing-mrs-overtheways-remembrances` (1029 units) |
| Six to Sixteen (1875) | have | PG 19360, `ewing-six-to-sixteen` (1287 units) |
| A Flat Iron for a Farthing (1872) | have | PG 19859, `ewing-flat-iron-for-a-farthing` (1205 units) |
| ewing-jackanapes-single | excluded | Jackanapes alone (PG 20351): contained in PG 7865 |
| ewing-other | excluded | Melchior's Dream, A Great Emergency, Brothers of Pity, Mary's Meadow, The Peace Egg, We and the World, Last Words, verses and miscellanea: candidates for a later batch |
| ewing-contained | excluded | The Brownies and Other Tales (PG 16052) and The Land of Lost Toys (PG 33880): measured 84% and 93% contained in Lob Lie-by-the-Fire, The Brownies and Other Tales (PG 62783), which is held |

## Mrs. Molesworth

Shelf: `pipeline/molesworth_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Eight of her best-known children's books, cut by their own Contents or chapter lines; some fifty others on Gutenberg are left for later. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Cuckoo Clock (1877) | have | PG 15569, `molesworth-cuckoo-clock` (1082 units) |
| The Tapestry Room (1879) | have | PG 17175, `molesworth-tapestry-room` (1095 units) |
| "Carrots": Just a Little Boy (1876) | have | PG 33544, `molesworth-carrots` (1054 units) |
| Christmas-Tree Land (1884) | have | PG 39375, `molesworth-christmas-tree-land` (1125 units) |
| The Adventures of Herr Baby (1881) | have | PG 29380, `molesworth-herr-baby` (852 units) |
| Four Winds Farm (1887) | have | PG 39748, `molesworth-four-winds-farm` (1005 units) |
| An Enchanted Garden: Fairy Stories (1892) | have | PG 43127, `molesworth-enchanted-garden` (795 units) |
| Rosy (1882) | have | PG 6676, `molesworth-rosy` (1034 units) |
| molesworth-duplicate | excluded | The Cuckoo Clock (PG 28619): a later illustrated printing |
| molesworth-other | excluded | her many other children's books and novels on Gutenberg (some fifty titles): candidates for a later batch |

## Johann David Wyss (The Swiss Family Robinson)

Shelf: `pipeline/wyss_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Kingston's translation only: the edition whose header names its translator. One other Gutenberg edition is marked COPYRIGHTED and is excluded; the first English version names no translator and waits for Adam. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Swiss Family Robinson, tr. W. H. G. Kingston | have | PG 41659, `wyss-swiss-family-robinson-kingston` (2544 units) |
| wyss-copyrighted | excluded | Swiss Family Robinson (PG 3836): its Gutenberg header reads 'This is a COPYRIGHTED Project Gutenberg eBook' (the 2026-07-26 rights rule) |
| wyss-godwin | excluded | The Family Robinson Crusoe (PG 72813): the first English version, published by M. J. Godwin and Co.; the edition names no translator (usually attributed to the Godwins), so it waits for Adam |
| wyss-unnamed | excluded | The Swiss Family Robinson (PG 11703) and the Milo Winter and T. H. Robinson printings (PG 34808, 78017): no translator named in the catalog; Words of One Syllable (PG 6692): Lucy Aikin's adaptation |

## Alfred J. Church

Shelf: `pipeline/church_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). His retellings of Homer, Virgil, the tragedians, Livy, Herodotus, Spenser and the Charlemagne romances; nested story > chapter where a book holds several stories. His novels are not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Story of the Iliad, edited for school use (Macmillan, 1905; 1920 printing) | have | PG 74231, `church-story-of-the-iliad` (700 units) |
| The Story of the Odyssey | have | PG 6370, `church-story-of-the-odyssey` (705 units) |
| Stories from Virgil | have | PG 40622, `church-stories-from-virgil` (382 units) |
| Stories from the Greek Tragedians | have | PG 14994, `church-stories-from-the-greek-tragedians` (873 units) |
| Stories from Livy | have | PG 24030, `church-stories-from-livy` (217 units) |
| Stories of the Old World | have | PG 43982, `church-stories-of-the-old-world` (1210 units) |
| Stories of the Persian Wars, from Herodotus | have | PG 78980, `church-stories-of-the-persian-wars` (327 units) |
| The Faery Queen and Her Knights: Stories Retold from Edmund Spenser | have | PG 55765, `church-faery-queen-and-her-knights` (667 units) |
| Stories of Charlemagne and the Twelve Peers of France | have | PG 75339, `church-stories-of-charlemagne` (689 units) |
| church-novels | excluded | his historical novels (Callias, Lords of the World, The Count of the Saxon Shore, The Hammer, With the King at Oxford, A Young Macedonian, Helmet and Spear, Henry the Fifth): fiction of his own; candidates for a later batch |
| church-history | excluded | Roman Life in the Days of Cicero (PG 13481): history, not story |
| church-tacitus | excluded | Tacitus, tr. Church and Brodribb: held by Lane B on tacitus_shelf.json |
| church-iliad-audio | excluded | The Iliad for Boys and Girls (PG 21584): on Gutenberg only as a LibriVox audiobook, with no text file |

## H. A. Guerber

Shelf: `pipeline/guerber_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her handbooks of myth and legend, cut by their own chapter lines or Contents. Her school histories are not taken. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Myths of Greece and Rome, Narrated with Special Reference to Literature and Art | have | PG 39250, `guerber-myths-of-greece-and-rome` (3455 units) |
| Myths of Northern Lands | have | PG 73021, `guerber-myths-of-northern-lands` (2779 units) |
| Myths of the Norsemen, from the Eddas and Sagas | have | PG 28497, `guerber-myths-of-the-norsemen` (1893 units) |
| Legends of the Middle Ages, Narrated with Special Reference to Literature and Art | have | PG 12455, `guerber-legends-of-the-middle-ages` (1472 units) |
| The Book of the Epic: The World's Great Epics Told in Story | have | PG 13983, `guerber-book-of-the-epic` (1770 units) |
| Legends of Switzerland | have | PG 64163, `guerber-legends-of-switzerland` (1549 units) |
| Stories of the Wagner Opera | have | PG 16840, `guerber-stories-of-the-wagner-opera` (448 units) |
| guerber-histories | excluded | The Story of the Greeks (PG 23495), The Story of the Thirteen Colonies (48051) and her other school histories: history, not myth |

## Josephine Preston Peabody

Shelf: `pipeline/peabody_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Greek myths retold for children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Old Greek Folk Stories Told Anew | have | PG 9313, `peabody-old-greek-folk-stories` (436 units) |
| peabody-poems-plays | excluded | The Piper (PG 11661), The Singing Man (14531), The Singing Leaves (75847), The Book of the Little Past (39131): verse and drama |

## The Golden Legend (Jacobus de Voragine, tr. Caxton)

Shelf: `pipeline/golden-legend_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The whole Temple Classics set, seven volumes, raw Internet Archive OCR of Google scans. Every title page was read: all seven are Ellis's 1900 edition. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Golden Legend, or Lives of the Saints, as englished by William Caxton, ed. F. S. Ellis (Temple Classics, 1900), vol. 1 | have-raw | IA `TheGoldenLegendV1`, `golden-legend-vol-1` |
| The Golden Legend, or Lives of the Saints, as englished by William Caxton, ed. F. S. Ellis (Temple Classics, 1900), vol. 2 | have-raw | IA `TheGoldenLegendV2`, `golden-legend-vol-2` |
| The Golden Legend, or Lives of the Saints, as englished by William Caxton, ed. F. S. Ellis (Temple Classics, 1900), vol. 3 | have-raw | IA `TheGoldenLegendV3`, `golden-legend-vol-3` |
| The Golden Legend, or Lives of the Saints, as englished by William Caxton, ed. F. S. Ellis (Temple Classics, 1900), vol. 4 | have-raw | IA `TheGoldenLegendV4`, `golden-legend-vol-4` |
| The Golden Legend, or Lives of the Saints, as englished by William Caxton, ed. F. S. Ellis (Temple Classics, 1900), vol. 5 | have-raw | IA `TheGoldenLegendV5`, `golden-legend-vol-5` |
| The Golden Legend, or Lives of the Saints, as englished by William Caxton, ed. F. S. Ellis (Temple Classics, 1900), vol. 6 | have-raw | IA `TheGoldenLegendV6`, `golden-legend-vol-6` |
| The Golden Legend, or Lives of the Saints, as englished by William Caxton, ed. F. S. Ellis (Temple Classics, 1900), vol. 7 | have-raw | IA `TheGoldenLegendV7`, `golden-legend-vol-7` |
| golden-legend-longfellow | excluded | Longfellow's The Golden Legend (PG 10490): a dramatic poem of the same name, not this book |
| golden-legend-other-printings | excluded | later Dent reprints of the same Temple Classics edition (1922-1935) and the Wellesley scans of vols. 3 and 5 (goldenlegendorli03jaco, goldenlegendorli05jaco): the 1900 set is held |
| golden-legend-ryan | excluded | Ryan and Ripperger's translation (Longmans, 1941) and the Princeton translation (1993): in copyright |

## William Canton

Shelf: `pipeline/canton_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Saints' legends retold for children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| A Child's Book of Saints | have | PG 22112, `canton-childs-book-of-saints` (934 units) |

## Abbie Farwell Brown

Shelf: `pipeline/abbie-brown_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Saints' legends and their animals, Norse myths and bird legends, retold for children; cut by legend or tale. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Book of Saints and Friendly Beasts | have | PG 28990, `abbie-brown-book-of-saints-and-friendly-beasts` (656 units) |
| In the Days of Giants: A Book of Norse Tales | have | PG 44622, `abbie-brown-in-the-days-of-giants` (760 units) |
| The Curious Book of Birds | have | PG 16140, `abbie-brown-curious-book-of-birds` (728 units) |

## Amy Steedman

Shelf: `pipeline/steedman_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Saints' lives retold for young children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| In God's Garden: Stories of the Saints for Little Children | have | PG 36674, `steedman-in-gods-garden` (732 units) |

## Grace James

Shelf: `pipeline/grace-james_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Japanese tales retold, cut by her own Contents. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Japanese Fairy Tales, retold by Grace James | have | PG 35853, `grace-james-japanese-fairy-tales` (1870 units) |

## William Elliot Griffis

Shelf: `pipeline/griffis_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Fairy tales from Japan, the Netherlands, Wales, Switzerland, Korea and Belgium, retold in his own English, cut by tale. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Japanese Fairy World: Stories from the Wonder-Lore of Japan (1880) | have | PG 29337, `griffis-japanese-fairy-world` (741 units) |
| Dutch Fairy Tales for Young Folks | have | PG 7871, `griffis-dutch-fairy-tales` (694 units) |
| Welsh Fairy Tales | have | PG 9368, `griffis-welsh-fairy-tales` (1081 units) |
| Swiss Fairy Tales | have | PG 69739, `griffis-swiss-fairy-tales` (856 units) |
| Korean Fairy Tales | have | PG 67180, `griffis-korean-fairy-tales` (772 units) |
| Belgian Fairy Tales | have | PG 67256, `griffis-belgian-fairy-tales` (939 units) |

## Elphinstone Dayrell

Shelf: `pipeline/dayrell_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). West African tales from Southern Nigeria, set down by a colonial officer; numbered stories. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Folk Stories from Southern Nigeria, West Africa (1910), introduction by Andrew Lang | have | PG 34655, `dayrell-folk-stories-southern-nigeria` (548 units) |
| Ikom Folk Stories from Southern Nigeria (1913) | have | PG 70959, `dayrell-ikom-folk-stories` (739 units) |

## Florence Cronise and Henry Ward

Shelf: `pipeline/cronise-ward_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Sierra Leone tales. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Cunnie Rabbit, Mr. Spider and the Other Beef: West African Folk Tales (1903) | have | PG 48828, `cronise-cunnie-rabbit` (1366 units) |

## W. H. I. Bleek

Shelf: `pipeline/bleek_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Khoekhoe fables and tales, numbered as Bleek numbers them. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Reynard the Fox in South Africa; or, Hottentot Fables and Tales, tr. W. H. I. Bleek (1864) | have | PG 73413, `bleek-reynard-in-south-africa` (420 units) |

## Parker Fillmore

Shelf: `pipeline/fillmore_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Czech and Slovak tales retold. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Czechoslovak Fairy Tales, retold by Parker Fillmore (1919) | have | PG 32217, `fillmore-czechoslovak-fairy-tales` (1342 units) |
| The Shoemaker's Apron: A Second Book of Czechoslovak Fairy Tales and Folk Tales (1920) | have | PG 33002, `fillmore-shoemakers-apron` (1654 units) |

## Elodie Lawton Mijatovich

Shelf: `pipeline/mijatovich_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Serbian folk tales in her translation; her later selection is excluded as contained. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Serbian Folk-lore, tr. Elodie Lawton Mijatovich, ed. W. Denton (second edition, 1899) | have | PG 45321, `mijatovich-serbian-folk-lore` (963 units) |
| mijatovich-fairy-tales-contained | excluded | Serbian Fairy Tales (PG 67191; New York: McBride, 1918): measured 91% contained in Serbian Folk-lore (PG 45321), which is held |

## Woislav M. Petrovitch

Shelf: `pipeline/petrovitch_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Serbian hero tales and legends, cut by chapter. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Hero Tales and Legends of the Serbians | have | PG 38571, `petrovitch-hero-tales-serbians` (2057 units) |

## Mary Frere

Shelf: `pipeline/frere_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Deccan tales as told by Anna Liberata de Souza, cut by the book's Contents. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Old Deccan Days; or, Hindoo Fairy Legends Current in Southern India, collected by Mary Frere from the telling of Anna Liberata de Souza (Philadelphia: Lippincott, 1870 printing) | have | PG 36696, `frere-old-deccan-days` (1120 units) |

## Lal Behari Day

Shelf: `pipeline/lal-behari-day_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Bengali tales in his English. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Folk-Tales of Bengal (1883) | have | PG 38488, `day-folk-tales-of-bengal` (387 units) |

## William Crooke and W. H. D. Rouse

Shelf: `pipeline/crooke-rouse_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Indian tales collected by Crooke, retold by Rouse. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Talking Thrush, and Other Tales from India, collected by William Crooke, retold by W. H. D. Rouse (1899; 1922 reprint) | have | PG 30635, `crooke-talking-thrush` (1395 units) |

## Natesa Sastri and Mrs. Howard Kingscote

Shelf: `pipeline/natesa-sastri_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). South Indian tales. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Tales of the Sun; or, Folklore of Southern India, by Mrs. Howard Kingscote and Pandit Natesa Sastri (1890) | have | PG 37002, `sastri-tales-of-the-sun` (950 units) |

## R. Nisbet Bain (translator)

Shelf: `pipeline/bain_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Cossack and Turkish tales in his translation. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Cossack Fairy Tales and Folk Tales, ed. and tr. R. Nisbet Bain (Harrap printing, undated in the Gutenberg text) | have | PG 29672, `bain-cossack-fairy-tales` (439 units) |
| Turkish Fairy Tales and Folk Tales, collected by Ignácz Kúnos, tr. R. Nisbet Bain (1901 printing) | have | PG 64807, `bain-turkish-fairy-tales` (896 units) |

## Pu Songling, tr. Herbert A. Giles

Shelf: `pipeline/giles-liaozhai_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Liaozhai's strange stories, numbered as Giles numbers them, with his footnotes under each. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| liaozhai-volumes | excluded | vols. 1 and 2 as separate files (PG 43627, 43628): the same text as the combined file |
| liaozhai-strange-stories-chinese-studio | excluded | PG 43629: the same file Lane C holds as giles-strange-stories on giles_shelf.json (queued first, 2026-10-03 00:43 UTC); not fetched twice. If that row needs heading rules, Lane D's were: {"levels": [{"re": "[IVXLC]+\\.$", "title_next": true}, {"re": "FOOTNOTES:$"}], "start": "STRANGE STORIES$", "front": true} |

## Zitkala-Ša

Shelf: `pipeline/zitkala-sa_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Dakota legends retold by a Yankton Dakota writer. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Old Indian Legends, retold by Zitkala-Ša (1901) | have | PG 338, `zitkala-sa-old-indian-legends` (439 units) |

## Charles A. Eastman and Elaine Goodale Eastman

Shelf: `pipeline/eastman_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Sioux tales retold, cut by evenings. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Wigwam Evenings: Sioux Folk Tales Retold (1909) | have | PG 28099, `eastman-wigwam-evenings` (600 units) |

## Rachel Harriette Busk

Shelf: `pipeline/busk_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Spanish legends and traditional tales. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Patrañas; or, Spanish Stories, Legendary and Traditional (London: Griffith and Farran, 1870) | have | PG 45859, `busk-patranas` (1411 units) |

## Wentworth Webster

Shelf: `pipeline/webster-basque_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Basque legends he collected and translated. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Basque Legends, collected and tr. Wentworth Webster, with an essay by Julien Vinson (second edition, 1879) | have | PG 34902, `webster-basque-legends` (2404 units) |

## A. A. Milne

Shelf: `pipeline/milne_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Pooh, the two verse books and Once on a Time, cut by chapter or poem. US public domain only; still in copyright in the UK until 2027. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Winnie-the-Pooh (1926) | have | PG 67098, `milne-winnie-the-pooh` (1089 units) |
| The House at Pooh Corner (1928) | have | PG 73011, `milne-house-at-pooh-corner` (1262 units) |
| When We Were Very Young (1924) | have | PG 70271, `milne-when-we-were-very-young` (349 units) |
| Now We Are Six (1927) | have | PG 70516, `milne-now-we-are-six` (227 units) |
| Once on a Time (1917; the Gutenberg text is a printing with a 1922 copyright) | have | PG 27771, `milne-once-on-a-time` (2031 units) |
| milne-adult | excluded | his plays, essays, humour collections and The Red House Mystery: not children's books |

## Dinah Maria Mulock Craik

Shelf: `pipeline/craik_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her children's books, cut by chapter or story. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Little Lame Prince and His Travelling-Cloak | have | PG 496, `craik-little-lame-prince` (810 units) |
| The Adventures of a Brownie, as Told to My Child | have | PG 30494, `craik-adventures-of-a-brownie` (634 units) |
| The Fairy Book: The Best Popular Stories Selected and Rendered Anew | have | PG 19734, `craik-fairy-book` (1828 units) |
| craik-duplicates | excluded | The Little Lame Prince (PG 23977, 45975): other printings; the Margaret Waters rewriting (24053): an adaptation |
| craik-novels | excluded | John Halifax, Gentleman and her other novels: not children's books |

## Jean Ingelow

Shelf: `pipeline/ingelow_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her fairy tales. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Mopsa the Fairy | have | PG 32867, `ingelow-mopsa-the-fairy` (1080 units) |
| Wonder-Box Tales | have | PG 21014, `ingelow-wonder-box-tales` (559 units) |
| ingelow-duplicate | excluded | Mopsa the Fairy (PG 67087): a later illustrated printing |
| ingelow-other | excluded | her Poems (PG 13223-13224) and Fated to Be Free (12303) |

## Frank R. Stockton

Shelf: `pipeline/stockton_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). His fairy tales; the 1922 school selection is nested section > tale. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Bee-Man of Orn and Other Fanciful Tales | have | PG 12067, `stockton-bee-man-of-orn` (1070 units) |
| Ting-a-ling | have | PG 20836, `stockton-ting-a-ling` (484 units) |
| Fanciful Tales, ed. Mary E. Burt (school edition, 1922 copyright) | have | PG 71032, `stockton-fanciful-tales` (650 units) |
| stockton-adult | excluded | The Lady, or the Tiger?, Rudder Grange and his other fiction: not fairy tales; candidates for a later batch |

## Thornton W. Burgess

Shelf: `pipeline/burgess_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The Mother West Wind books and the twenty Bedtime Story-Books, all before 1929, cut by chapter. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Old Mother West Wind | have | PG 2557, `burgess-old-mother-west-wind` (427 units) |
| Mother West Wind's Children | have | PG 20877, `burgess-mother-west-winds-children` (697 units) |
| Mother West Wind's Animal Friends | have | PG 39706, `burgess-mother-west-winds-animal-friends` (654 units) |
| Mother West Wind "Why" Stories | have | PG 14958, `burgess-mother-west-wind-why` (523 units) |
| Mother West Wind "How" Stories | have | PG 21286, `burgess-mother-west-wind-how` (433 units) |
| Mother West Wind "When" Stories | have | PG 46988, `burgess-mother-west-wind-when` (376 units) |
| Mother West Wind "Where" Stories | have | PG 17250, `burgess-mother-west-wind-where` (419 units) |
| The Adventures of Reddy Fox | have | PG 1825, `burgess-reddy-fox` (347 units) |
| The Adventures of Johnny Chuck | have | PG 5844, `burgess-johnny-chuck` (317 units) |
| The Adventures of Peter Cottontail | have | PG 46866, `burgess-peter-cottontail` (402 units) |
| The Adventures of Unc' Billy Possum | have | PG 14732, `burgess-unc-billy-possum` (346 units) |
| The Adventures of Mr. Mocker | have | PG 11915, `burgess-mr-mocker` (304 units) |
| The Adventures of Jerry Muskrat | have | PG 5110, `burgess-jerry-muskrat` (314 units) |
| The Adventures of Danny Meadow Mouse | have | PG 25301, `burgess-danny-meadow-mouse` (293 units) |
| The Adventures of Grandfather Frog | have | PG 14375, `burgess-grandfather-frog` (311 units) |
| The Adventures of Chatterer the Red Squirrel | have | PG 37952, `burgess-chatterer` (268 units) |
| The Adventures of Sammy Jay | have | PG 43596, `burgess-sammy-jay` (262 units) |
| The Adventures of Buster Bear | have | PG 22816, `burgess-buster-bear` (308 units) |
| The Adventures of Old Mr. Toad | have | PG 12630, `burgess-old-mr-toad` (334 units) |
| The Adventures of Prickly Porky | have | PG 15521, `burgess-prickly-porky` (297 units) |
| The Adventures of Old Man Coyote | have | PG 46952, `burgess-old-man-coyote` (360 units) |
| The Adventures of Paddy the Beaver | have | PG 19092, `burgess-paddy-beaver` (267 units) |
| The Adventures of Poor Mrs. Quack | have | PG 5846, `burgess-poor-mrs-quack` (274 units) |
| The Adventures of Bobby Coon | have | PG 46951, `burgess-bobby-coon` (241 units) |
| The Adventures of Jimmy Skunk | have | PG 21015, `burgess-jimmy-skunk` (283 units) |
| The Adventures of Bob White | have | PG 46950, `burgess-bob-white` (296 units) |
| burgess-duplicates | excluded | Paddy the Beaver (PG 2493), Danny Meadow Mouse (25529), Lightfoot the Deer (4670): other transcriptions or later titles |
| burgess-later | excluded | Lightfoot, Whitefoot, Blacky, Old Granny Fox, Bowser, Happy Jack, Mrs. Peter Rabbit, Buster Bear's Twins, Billy Mink, Little Joe Otter, Wishing-Stone Stories, The Christmas Reindeer and the Boy Scout books: candidates for a later batch, each to be checked against the 1929 line |
| burgess-handbooks | excluded | the Burgess Animal and Bird Books (PG 2441, 3074, 23708, 23709): natural history, not story |

## Selma Lagerlöf

Shelf: `pipeline/lagerlof_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Two books in Velma Swanston Howard's translation. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Wonderful Adventures of Nils, tr. Velma Swanston Howard | have | PG 10935, `lagerlof-wonderful-adventures-of-nils` (3053 units) |
| Christ Legends, tr. Velma Swanston Howard | have | PG 44818, `lagerlof-christ-legends` (1332 units) |
| lagerlof-novels | excluded | Gösta Berling, Jerusalem, The Emperor of Portugallia and her other novels and stories, translators named in the catalog: candidates for a later batch |

## Édouard Laboulaye

Shelf: `pipeline/laboulaye_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). His fairy tales in Mary L. Booth's translation. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Laboulaye's Fairy Book, tr. Mary L. Booth | have | PG 26386, `laboulaye-fairy-book` (1111 units) |

## Wilhelm Hauff

Shelf: `pipeline/hauff_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). His fairy tales in two named translations. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Tales of the Caravan, Inn, and Palace, tr. Edward L. Stowell | have | PG 32109, `hauff-tales-of-the-caravan-inn-palace` (1613 units) |
| Fairy Tales, tr. L. L. Weedon | have | PG 74947, `hauff-fairy-tales-weedon` (1513 units) |
| hauff-unnamed | excluded | The Little Glass Man and Other Stories (PG 45606): the Gutenberg header names Lina Eckenstein only as contributor; held back until the translator is confirmed |
| hauff-other | excluded | The Oriental Story Book (24593), The Severed Hand (22664), The Wine-Ghosts of Bremen (32064), The Banished (32071): translator to be checked; candidates for a later batch |

## Margaret Gatty

Shelf: `pipeline/gatty_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her stories for children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Aunt Judy's Tales | have | PG 5074, `gatty-aunt-judys-tales` (1045 units) |
| The Fairy Godmothers and Other Tales | have | PG 11319, `gatty-fairy-godmothers` (581 units) |
| gatty-translation | excluded | The History of a Mouthful of Bread (PG 6970): her translation of Jean Macé's science book, not story |

## Maria Edgeworth

Shelf: `pipeline/edgeworth_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her stories for children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Parent's Assistant; or, Stories for Children | have | PG 3655, `edgeworth-parents-assistant` (3828 units) |
| edgeworth-duplicate | excluded | The Parent's Assistant (PG 36132, Macmillan, with Anne Thackeray Ritchie's introduction): another printing; candidate as a second witness |
| edgeworth-other | excluded | Castle Rackrent, The Absentee, Belinda and the Tales and Novels volumes: not children's books |

## James Baldwin (1841-1925)

Shelf: `pipeline/baldwin_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). His retellings of myth, epic and legend for young readers. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Story of Siegfried | have | PG 6866, `baldwin-story-of-siegfried` (1198 units) |
| Old Greek Stories | have | PG 11582, `baldwin-old-greek-stories` (830 units) |
| Hero Tales | have | PG 15616, `baldwin-hero-tales` (660 units) |
| Fifty Famous Stories Retold | have | PG 18442, `baldwin-fifty-famous-stories` (1038 units) |
| A Story of the Golden Age | have | PG 54214, `baldwin-story-of-the-golden-age` (1123 units) |
| The Sampo: A Wonder Tale of the Old North | have | PG 66819, `baldwin-sampo` (1414 units) |
| baldwin-other | excluded | Fifty Famous People (PG 6168), Four Great Americans (11174), the readers and the Book-Lover: history, schoolbooks and criticism |

## Mary Macgregor

Shelf: `pipeline/macgregor_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Three of her 'Told to the Children' retellings. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Stories of King Arthur's Knights, Told to the Children | have | PG 25654, `macgregor-stories-of-king-arthurs-knights` (614 units) |
| Stories of Siegfried, Told to the Children | have | PG 26181, `macgregor-stories-of-siegfried` (597 units) |
| Stories from the Ballads, Told to the Children | have | PG 22175, `macgregor-stories-from-the-ballads` (580 units) |
| macgregor-histories | excluded | The Story of Greece (PG 66070), The Story of Rome (66147): history |
| macgregor-undine | excluded | Undine (PG 18752): her adaptation of La Motte-Fouqué; a candidate for a later batch |

## Henry Gilbert

Shelf: `pipeline/gilbert_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Arthurian tales retold for children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| King Arthur's Knights: The Tales Re-told for Boys and Girls | have | PG 22396, `gilbert-king-arthurs-knights` (2573 units) |

## Sir James Knowles

Shelf: `pipeline/knowles_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Arthurian legends compiled from Malory and others. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Legends of King Arthur and His Knights | have | PG 12753, `knowles-legends-of-king-arthur` (1702 units) |

## T. W. Rolleston

Shelf: `pipeline/rolleston_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Irish and Celtic legend retold. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The High Deeds of Finn, and Other Bardic Romances of Ancient Ireland | have | PG 14749, `rolleston-high-deeds-of-finn` (938 units) |
| Myths and Legends of the Celtic Race | have | PG 34081, `rolleston-myths-legends-celtic-race` (2512 units) |
| rolleston-epictetus | excluded | The Teaching of Epictetus (PG 39855): on Lane B's epictetus_shelf.json |
| rolleston-other | excluded | Sea Spray, Parallel Paths, Ireland and Poland, his Thomas Davis selection: verse and essays |

## Eleanor Hull

Shelf: `pipeline/hull_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Irish legend and Norse-British saga history retold. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Cuchulain, the Hound of Ulster | have | PG 52963, `hull-cuchulain-hound-of-ulster` (845 units) |
| The Northmen in Britain | have | PG 69131, `hull-northmen-in-britain` (1014 units) |
| hull-poem-book | excluded | The Poem-Book of the Gael (PG 46917): an anthology of other hands' translations |

## Jessie L. Weston (translator)

Shelf: `pipeline/weston_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her English versions of medieval romance; Parzival nested book > argument. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Parzival: A Knightly Epic, Wolfram von Eschenbach, tr. Jessie L. Weston, vol. 1 | have | PG 47297, `weston-parzival-1` (1205 units) |
| Parzival: A Knightly Epic, Wolfram von Eschenbach, tr. Jessie L. Weston, vol. 2 | have | PG 47298, `weston-parzival-2` (804 units) |
| Morien, rendered into English prose from the medieval Dutch by Jessie L. Weston | have | PG 8447, `weston-morien` (273 units) |
| Sir Gawain and the Lady of Lys, tr. Jessie L. Weston | have | PG 45514, `weston-gawain-and-the-lady-of-lys` (309 units) |
| Sir Gawain and the Green Knight, retold by Jessie L. Weston | have | PG 66084, `weston-gawain-and-the-green-knight` (249 units) |
| Guingamor, Lanval, Tyolet, Bisclaveret: Four Lais, rendered into English prose by Jessie L. Weston | have | PG 46234, `weston-four-lais` (303 units) |
| weston-studies | excluded | From Ritual to Romance (PG 4090), The Legend of Sir Lancelot du Lac (46497), The Three Days' Tournament (46636): scholarship, not story |

## Mary De Morgan (1850-1907)

Shelf: `pipeline/de-morgan_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her literary fairy tales. The Windfairies prints each story's title only on its headpiece plate, so a new convert_nested option ("caption") reads those plates as headings. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Necklace of Princess Fiorimonde, and Other Stories | have | PG 38976, `de-morgan-necklace-of-princess-fiorimonde` (738 units) |
| The Windfairies, and Other Tales | have | PG 69875, `de-morgan-windfairies` (719 units) |

## Frances Browne (1816-1879)

Shelf: `pipeline/frances-browne_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Granny's Wonderful Chair, a frame of fairy tales. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Granny's Wonderful Chair | have | PG 26018, `frances-browne-grannys-wonderful-chair` (421 units) |
| grannys-wonderful-chair-curtis | excluded | PG 35820, a later illustrated edition of the same book with Dollie Radford's introduction; held once |

## Klara Stroebe, ed., tr. Frederick H. Martens

Shelf: `pipeline/stroebe_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Swedish and Norwegian folk tales with Stroebe's source notes after each tale. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Swedish Fairy Book, ed. Klara Stroebe, tr. Frederick H. Martens | have | PG 37193, `stroebe-swedish-fairy-book` (570 units) |
| The Norwegian Fairy Book, ed. Klara Stroebe, tr. Frederick H. Martens | have | PG 38070, `stroebe-norwegian-fairy-book` (945 units) |

## Lucy Fitch Perkins (1865-1937)

Shelf: `pipeline/lfperkins_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her Twins series: children's stories of other lands and times. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Japanese Twins | have | PG 3496, `lfperkins-japanese-twins` (766 units) |
| The Swiss Twins | have | PG 3497, `lfperkins-swiss-twins` (387 units) |
| The Belgian Twins | have | PG 3642, `lfperkins-belgian-twins` (458 units) |
| The Eskimo Twins | have | PG 3774, `lfperkins-eskimo-twins` (663 units) |
| The Dutch Twins | have | PG 4012, `lfperkins-dutch-twins` (778 units) |
| The Scotch Twins | have | PG 4086, `lfperkins-scotch-twins` (674 units) |
| The French Twins | have | PG 4091, `lfperkins-french-twins` (453 units) |
| The Spartan Twins | have | PG 9966, `lfperkins-spartan-twins` (531 units) |
| The Puritan Twins | have | PG 16644, `lfperkins-puritan-twins` (461 units) |
| The Cave Twins | have | PG 28425, `lfperkins-cave-twins` (554 units) |
| The Italian Twins | have | PG 28426, `lfperkins-italian-twins` (328 units) |
| The Irish Twins | have | PG 28431, `lfperkins-irish-twins` (621 units) |
| The Mexican Twins | have | PG 28889, `lfperkins-mexican-twins` (606 units) |
| lfperkins-folk-tales-from-the-russian | excluded | PG 12851: by Verra de Blumenthal; Perkins only illustrated it |
| lfperkins-summers-readers | excluded | PG 67302, 68453: school primers, not stories |
| lfperkins-moon-princess | excluded | PG 60042, The Moon Princess (1905): written by Edith Ogden Harrison; Perkins only illustrated it (title page read) |

## Laura E. Richards (1850-1943)

Shelf: `pipeline/richards_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her fables and stories for children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Captain January | have | PG 7790, `richards-captain-january` (285 units) |
| Melody: The Story of a Child | have | PG 7824, `richards-melody` (351 units) |
| The Silver Crown: Another Book of Fables | have | PG 19892, `richards-silver-crown` (516 units) |
| The Pig Brother, and Other Fables and Stories | have | PG 43336, `richards-pig-brother` (647 units) |
| Five Minute Stories | have | PG 49748, `richards-five-minute-stories` (1211 units) |
| Three Minute Stories | have | PG 49751, `richards-three-minute-stories` (693 units) |
| The Joyous Story of Toto | have | PG 35281, `richards-joyous-story-of-toto` (875 units) |
| Toto's Merry Winter | have | PG 41603, `richards-totos-merry-winter` (1080 units) |
| Snow-White; or, The House in the Wood | have | PG 49724, `richards-snow-white` (524 units) |
| richards-golden-breasted-kootoo | excluded | PG 49750, The Golden-Breasted Kootoo, and Other Stories (1899 reissue; copyright 1885): the stories told inside The Joyous Story of Toto, reprinted; 72% of its long paragraphs are in richards-joyous-story-of-toto |

## Charlotte M. Yonge (1823-1901)

Shelf: `pipeline/yonge_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her historical tales and story books for the young; the domestic novels are left for now. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Little Duke: Richard the Fearless | have | PG 3048, `yonge-little-duke` (794 units) |
| The Prince and the Page: A Story of the Last Crusade | have | PG 3696, `yonge-prince-and-the-page` (1166 units) |
| The Lances of Lynwood | have | PG 4364, `yonge-lances-of-lynwood` (1030 units) |
| The Herd Boy and His Hermit | have | PG 5313, `yonge-herd-boy-and-his-hermit` (896 units) |
| A Book of Golden Deeds | have | PG 6489, `yonge-book-of-golden-deeds` (878 units) |
| Little Lucy's Wonderful Globe | have | PG 4538, `yonge-little-lucys-wonderful-globe` (300 units) |
| yonge-little-lucys-wonderful-globe-2 | excluded | PG 26487, a second transcription of Little Lucy's Wonderful Globe; held once |

## Lady Wilde (Speranza)

Shelf: `pipeline/lady-wilde_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Irish legends, charms and superstitions she gathered from the people. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Ancient Legends, Mystic Charms, and Superstitions of Ireland | have | PG 61436, `lady-wilde-ancient-legends-of-ireland` (2552 units) |

## T. Crofton Croker

Shelf: `pipeline/croker_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The first collection of Irish fairy legends taken down from country people. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Fairy Legends and Traditions of the South of Ireland | have | PG 39752, `croker-fairy-legends-south-of-ireland` (1213 units) |

## Thomas Keightley

Shelf: `pipeline/keightley_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Fairy belief and fairy tales surveyed across Europe and Asia. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Fairy Mythology | have | PG 41006, `keightley-fairy-mythology` (3358 units) |

## Sophia Morrison

Shelf: `pipeline/morrison_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Tales collected on the Isle of Man. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Manx Fairy Tales | have | PG 51762, `morrison-manx-fairy-tales` (686 units) |

## Robert Hunt

Shelf: `pipeline/robert-hunt_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Cornish drolls and traditions. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Popular Romances of the West of England, Second Series | have | PG 59033, `robert-hunt-popular-romances-west-of-england-2` (1907 units) |

## Sabine Baring-Gould

Shelf: `pipeline/baring-gould_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). His books of legend and lore. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Curious Myths of the Middle Ages | have | PG 36127, `baring-gould-curious-myths-of-the-middle-ages` (740 units) |
| The Book of Were-Wolves | have | PG 5324, `baring-gould-book-of-were-wolves` (882 units) |
| A Book of Ghosts | have | PG 36638, `baring-gould-book-of-ghosts` (3105 units) |
| Legends of the Patriarchs and Prophets | have | PG 48736, `baring-gould-legends-of-the-patriarchs-and-prophets` (3580 units) |
| Grettir the Outlaw: A Story of Iceland | have | PG 48622, `baring-gould-grettir-the-outlaw` (1204 units) |
| baring-gould-lives-of-the-saints | excluded | The Lives of the Saints (16 vols; Gutenberg holds some months): a saints' calendar on the scale of Lane A's divines; left for Adam to place |

## Charles Godfrey Leland

Shelf: `pipeline/leland_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Tales he took down from the people: Wabanaki legends of Glooskap, Florentine legends, the folk legends of Virgil the magician, and the Algonkin legends in verse. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Algonquin Legends of New England | have | PG 6803, `leland-algonquin-legends-of-new-england` (1319 units) |
| Legends of Florence, First Series | have | PG 32786, `leland-legends-of-florence-1` (1611 units) |
| The Unpublished Legends of Virgil | have | PG 62335, `leland-unpublished-legends-of-virgil` (1682 units) |
| Kulóskap the Master, and Other Algonkin Poems, tr. Charles Godfrey Leland and John Dyneley Prince (1902) | have | PG 78673, `leland-kuloskap-the-master` (991 units) |

## Henry Rowe Schoolcraft

Shelf: `pipeline/schoolcraft_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). His records of Ojibwe and other Great Lakes oral legends, the source Longfellow drew on; a collector's versions, framed by him. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Myth of Hiawatha, and Other Oral Legends | have | PG 21620, `schoolcraft-myth-of-hiawatha` (968 units) |
| Algic Researches, vol. 1 | have | PG 35152, `schoolcraft-algic-researches-1` (465 units) |
| Algic Researches, vol. 2 | have | PG 35175, `schoolcraft-algic-researches-2` (435 units) |
| The Indian Fairy Book, from the Original Legends (Stokes, 1916; a reprint of the 1856 collection) | have | PG 48469, `schoolcraft-indian-fairy-book` (1716 units) |

## Frank Hamilton Cushing

Shelf: `pipeline/cushing_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Zuñi tales and creation myths recorded while he lived at Zuñi Pueblo. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Zuñi Folk Tales | have | PG 54682, `cushing-zuni-folk-tales` (2469 units) |
| Outlines of Zuñi Creation Myths | have | PG 48342, `cushing-outlines-of-zuni-creation-myths` (504 units) |

## James Mooney

Shelf: `pipeline/mooney_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Cherokee myths recorded among the Eastern Cherokee. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Myths of the Cherokee | have | PG 45634, `mooney-myths-of-the-cherokee` (3565 units) |

## Katharine Berry Judson, ed.

Shelf: `pipeline/judson_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Regional anthologies of Native American myths, drawn from earlier printed sources and credited to them. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Myths and Legends of California and the Old Southwest | have | PG 2503, `judson-california-and-the-old-southwest` (653 units) |
| Myths and Legends of the Great Plains | have | PG 22083, `judson-great-plains` (1038 units) |
| Myths and Legends of the Mississippi Valley and the Great Lakes | have | PG 44935, `judson-mississippi-valley-and-great-lakes` (1242 units) |
| Myths and Legends of Alaska | have | PG 47146, `judson-alaska` (747 units) |
| Myths and Legends of British North America | have | PG 48409, `judson-british-north-america` (913 units) |

## Robert Hamill Nassau

Shelf: `pipeline/nassau_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). West African animal tales heard in Gabon, with his notes; cited by part, tale and note. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Where Animals Talk: West African Folk Lore Tales | have | PG 58900, `nassau-where-animals-talk` (1528 units) |

## Susan Coolidge (Sarah Chauncey Woolsey)

Shelf: `pipeline/coolidge_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The Katy books and her other girls' stories, written for the young. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| What Katy Did | have | PG 8994, `coolidge-what-katy-did` (1132 units) |
| What Katy Did at School | have | PG 5141, `coolidge-what-katy-did-at-school` (1117 units) |
| What Katy Did Next | have | PG 8995, `coolidge-what-katy-did-next` (825 units) |
| Clover | have | PG 15798, `coolidge-clover` (951 units) |
| In the High Valley | have | PG 28724, `coolidge-in-the-high-valley` (926 units) |
| Nine Little Goslings | have | PG 27678, `coolidge-nine-little-goslings` (940 units) |
| Eyebright | have | PG 27223, `coolidge-eyebright` (857 units) |
| A Round Dozen | have | PG 35186, `coolidge-round-dozen` (1030 units) |
| The New-Year's Bargain | have | PG 58762, `coolidge-new-years-bargain` (730 units) |

## Lucretia P. Hale

Shelf: `pipeline/lucretia-hale_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The comic Peterkin family stories. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Peterkin Papers | have | PG 3028, `lucretia-hale-peterkin-papers` (1288 units) |
| The Last of the Peterkins, with Others of Their Kin | have | PG 15546, `lucretia-hale-last-of-the-peterkins` (847 units) |
| lucretia-hale-peterkin-papers-2 | excluded | PG 25648, a second transcription of The Peterkin Papers. Paragraph-start containment against PG 3028 measured 82% both ways, so it is the same text; held once (PG 3028). |

## Margaret Sidney (Harriett Mulford Stone Lothrop)

Shelf: `pipeline/margaret-sidney_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The Five Little Peppers series, the family saga of the Pepper children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Five Little Peppers and How They Grew | have | PG 2770, `margaret-sidney-five-little-peppers` (2426 units) |
| Five Little Peppers Midway | have | PG 5632, `margaret-sidney-peppers-midway` (2333 units) |
| Five Little Peppers and their Friends | have | PG 6418, `margaret-sidney-peppers-and-their-friends` (3063 units) |
| Five Little Peppers Abroad | have | PG 6987, `margaret-sidney-peppers-abroad` (2412 units) |
| Five Little Peppers Grown Up | have | PG 7498, `margaret-sidney-peppers-grown-up` (2754 units) |
| Five Little Peppers at School | have | PG 26122, `margaret-sidney-peppers-at-school` (2867 units) |
| Five Little Peppers in the Little Brown House | have | PG 71128, `margaret-sidney-peppers-little-brown-house` (2586 units) |
| The Adventures of Joel Pepper | have | PG 7434, `margaret-sidney-joel-pepper` (2408 units) |
| Ben Pepper | have | PG 35178, `margaret-sidney-ben-pepper` (2999 units) |
| Phronsie Pepper | have | PG 71146, `margaret-sidney-phronsie-pepper` (2186 units) |
| Our Davie Pepper | have | PG 71215, `margaret-sidney-our-davie-pepper` (3360 units) |
| The Stories Polly Pepper Told | have | PG 49471, `margaret-sidney-stories-polly-pepper-told` (2507 units) |

## Eleanor H. Porter

Shelf: `pipeline/eleanor-porter_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Pollyanna and its sequel, and Just David. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Pollyanna | have | PG 1450, `eleanor-porter-pollyanna` (1927 units) |
| Pollyanna Grows Up | have | PG 6100, `eleanor-porter-pollyanna-grows-up` (2113 units) |
| Just David | have | PG 440, `eleanor-porter-just-david` (1809 units) |

## Jean Webster

Shelf: `pipeline/jean-webster_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Daddy-Long-Legs and Dear Enemy, novels in letters, and the two Patty books. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Daddy-Long-Legs | have | PG 157, `jean-webster-daddy-long-legs` (1014 units) |
| Dear Enemy | have | PG 238, `jean-webster-dear-enemy` (1610 units) |
| Just Patty | have | PG 21048, `jean-webster-just-patty` (1716 units) |
| When Patty Went to College | have | PG 21639, `jean-webster-when-patty-went-to-college` (1280 units) |
| jean-webster-daddy-long-legs-40426 | excluded | PG 40426, a second transcription of the novel Daddy-Long-Legs (2012, PGDP). Not a copy of PG 157: paragraph-start containment measured 58% one way, 68% the other, so the two differ in paragraphing or text. Held once here (PG 157); if both are wanted, they are two witnesses of one work, never two books. |
| jean-webster-daddy-long-legs-play-75857 | excluded | PG 75857 is a DIFFERENT work: Daddy Long-Legs, a comedy in four acts. PG's header says New York: Samuel French, 1914; the title page's copyright lines read 1912 (novel form), 1914 (Jean Webster) and 1922 (Samuel French), so this printing is 1922 or later and is public domain in the US. Not added this batch: it carries production notes after Act IV, and the acts would need their own heading rule. A candidate for Adam. |

## Johnny Gruelle

Shelf: `pipeline/gruelle_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The Raggedy Ann and Andy stories and his other fairy tales. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Raggedy Ann Stories | have | PG 18190, `gruelle-raggedy-ann-stories` (653 units) |
| Raggedy Andy Stories | have | PG 17371, `gruelle-raggedy-andy-stories` (645 units) |
| Friendly Fairies | have | PG 11315, `gruelle-friendly-fairies` (539 units) |
| The Magical Land of Noom | have | PG 62440, `gruelle-magical-land-of-noom` (1219 units) |
| The Paper Dragon | have | PG 78535, `gruelle-paper-dragon` (736 units) |

## Albert Bigelow Paine

Shelf: `pipeline/albert-paine_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The Hollow Tree animal tales and his other children's books. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Hollow Tree Nights and Days | have | PG 24410, `albert-paine-hollow-tree-nights-and-days` (702 units) |
| Mr. Turtle's Flying Adventure | held once | PG 28192: a reprint; 91% of it is in Hollow Tree Nights and Days (sixth audit pass) |
| Mr. Rabbit's Wedding | held once | PG 28193: a reprint; 96% of it is in Hollow Tree Nights and Days (sixth audit pass) |
| How Mr. Rabbit Lost His Tail | have | PG 28204, `albert-paine-how-mr-rabbit-lost-his-tail` (232 units) |
| The Arkansaw Bear | have | PG 28302, `albert-paine-arkansaw-bear` (722 units) |

## Aubrey de Vere

Shelf: `pipeline/de-vere_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Saints' legends and Irish heroic legends retold in verse. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Legends of Saint Patrick | have | PG 7165, `de-vere-legends-of-saint-patrick` (309 units) |
| Legends of the Saxon Saints | have | PG 29121, `de-vere-legends-of-the-saxon-saints` (1270 units) |
| The Foray of Queen Meave, and Other Legends of Ireland's Heroic Age | have | PG 78491, `de-vere-foray-of-queen-meave` (572 units) |

## W. D. Westervelt

Shelf: `pipeline/westervelt_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Hawaiian legends he collected and translated from the Hawaiian himself: Maui, Pele, the gods and ghosts, old Honolulu, and the historical legends. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Legends of Ma-ui, a Demi God of Polynesia, and of His Mother Hina | have | PG 32601, `westervelt-legends-of-maui` (862 units) |
| Legends of Gods and Ghosts (Hawaiian Mythology) | have | PG 39195, `westervelt-gods-and-ghosts` (1040 units) |
| Hawaiian Legends of Volcanoes | have | PG 66516, `westervelt-legends-of-volcanoes` (819 units) |
| Legends of Old Honolulu | have | PG 66547, `westervelt-legends-of-old-honolulu` (1033 units) |
| Hawaiian Historical Legends | have | PG 66357, `westervelt-historical-legends` (748 units) |

## Dean S. Fansler, ed.

Shelf: `pipeline/fansler_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Filipino folk tales collected by him and his students, each credited to its narrator, with comparative notes. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Filipino Popular Tales | have | PG 8299, `fansler-filipino-popular-tales` (3379 units) |

## Mite Kremnitz, collector; J. M. Percival, adapter

Shelf: `pipeline/kremnitz_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Romanian fairy tales from Ispirescu, Creanga and others, in Percival's English. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Roumanian Fairy Tales | have | PG 20552, `kremnitz-roumanian-fairy-tales` (1443 units) |

## Elsie Spicer Eells

Shelf: `pipeline/eells_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Brazilian and Azorean folk tales retold for children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Fairy Tales from Brazil | have | PG 24714, `eells-fairy-tales-from-brazil` (480 units) |
| Tales of Giants from Brazil | have | PG 21678, `eells-tales-of-giants-from-brazil` (431 units) |
| The Islands of Magic | have | PG 34431, `eells-islands-of-magic` (1346 units) |

## Knud Rasmussen, ed.; tr. W. J. Alexander Worster

Shelf: `pipeline/rasmussen_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Greenlandic tales collected by Rasmussen, in Worster's English. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Eskimo Folk-Tales | have | PG 28932, `rasmussen-eskimo-folk-tales` (1435 units) |

## Horace Newton Allen

Shelf: `pipeline/horace-allen_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Korean folk tales he translated, with his chapters describing Korea. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Korean Tales | have | PG 55539, `horace-allen-korean-tales` (416 units) |

## E. M. Berens

Shelf: `pipeline/berens_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). A school handbook retelling the Greek and Roman myths and heroic legends. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Myths and Legends of Ancient Greece and Rome | have | PG 22381, `berens-myths-and-legends-greece-rome` (1428 units) |

## Sara Cone Bryant

Shelf: `pipeline/sara-bryant_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Folk tales, fables and stories retold for telling aloud, with her advice to story-tellers. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| How to Tell Stories to Children | have | PG 474, `sara-bryant-how-to-tell-stories` (1097 units) |
| Stories to Tell Children | have | PG 16693, `sara-bryant-stories-to-tell-children` (1301 units) |
| sara-bryant-stories-to-tell-to-children-473 | excluded | PG 473, an undated transcription (1996) of Stories to Tell to Children. PG 16693 is the same work from the London: Harrap 1918 printing, proofread. Paragraph-start containment 68% one way, 65% the other, so the two differ in text or paragraphing (the opening stories differ, e.g. The Little Pink Rose against The Little Yellow Tulip). Held once (PG 16693, the dated printing); if both are wanted, they are two witnesses of one work. |

## Howard R. Garis

Shelf: `pipeline/garis_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The Uncle Wiggily books and the Bed Time Stories animal series, from his newspaper bedtime stories, and the small Uncle Wiggily picture pamphlets. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Curly and Floppy Twistytail (The Funny Piggie Boys) | have | PG 5262, `garis-curly-and-floppy-twistytail` (1207 units) |
| Umboo, the Elephant | have | PG 5900, `garis-umboo-the-elephant` (886 units) |
| Buddy and Brighteyes Pigg: Bed Time Stories | have | PG 11156, `garis-buddy-and-brighteyes-pigg` (970 units) |
| Sammie and Susie Littletail | have | PG 13087, `garis-sammie-and-susie-littletail` (865 units) |
| Lulu, Alice and Jimmie Wibblewobble | have | PG 15280, `garis-lulu-alice-and-jimmie-wibblewobble` (1024 units) |
| Uncle Wiggily's Adventures | have | PG 15281, `garis-uncle-wiggilys-adventures` (1084 units) |
| Uncle Wiggily's Travels | have | PG 15282, `garis-uncle-wiggilys-travels` (1321 units) |
| Uncle Wiggily in the Woods | have | PG 17807, `garis-uncle-wiggily-in-the-woods` (1266 units) |
| Bully and Bawly No-Tail (the Jumping Frogs) | have | PG 18599, `garis-bully-and-bawly-no-tail` (1140 units) |
| Jacko and Jumpo Kinkytail (The Funny Monkey Boys) | have | PG 32334, `garis-jacko-and-jumpo-kinkytail` (1235 units) |
| Uncle Wiggily in Wonderland | have | PG 42574, `garis-uncle-wiggily-in-wonderland` (1185 units) |
| Uncle Wiggily's Fortune | have | PG 54995, `garis-uncle-wiggilys-fortune` (1185 units) |
| Uncle Wiggily's Automobile | have | PG 60017, `garis-uncle-wiggilys-automobile` (748 units) |
| Neddie and Beckie Stubtail (Two Nice Bears) Bedtime Stories | have | PG 61082, `garis-neddie-and-beckie-stubtail` (1613 units) |
| Toodle and Noodle Flat-tail: The Jolly Beaver Boys | have | PG 67990, `garis-toodle-and-noodle-flat-tail` (1451 units) |
| Uncle Wiggily and Mother Goose Complete in two parts; fifty-two stories—one for each week of the year | have | PG 69458, `garis-uncle-wiggily-and-mother-goose` (2138 units) |
| Uncle Wiggily's Airship | have | PG 70295, `garis-uncle-wiggilys-airship` (1324 units) |
| Adventures of the runaway rocking chair | have | PG 71213, `garis-adventures-of-the-runaway-rocking-chair` (732 units) |
| Uncle Wiggily and Baby Bunty | have | PG 73603, `garis-uncle-wiggily-and-baby-bunty` (810 units) |
| Three little Trippertrots on their travels | have | PG 75192, `garis-three-little-trippertrots-on-their-travels` (1376 units) |
| Three little Trippertrots | have | PG 75474, `garis-three-little-trippertrots` (1452 units) |
| Uncle Wiggily's Auto Sled or, How Mr. Hedgehog Helped Him Get Up the Slippery Hill; and, How Uncle Wiggily Made a Snow Pudding. Also, What Happened in the Snow Fort | have | PG 50405, `garis-uncle-wiggilys-auto-sled` (97 units) |
| Uncle Wiggily's Squirt Gun; Or, Jack Frost Icicle Maker And, Uncle Wiggily's Queer Umbrellas, also, Uncle Wiggily's Lemonade Stand | have | PG 56950, `garis-uncle-wiggilys-squirt-gun` (90 units) |
| Uncle Wiggily on The Flying Rug; Or, The Great Adventure on a Windy March Day | have | PG 61671, `garis-uncle-wiggily-on-the-flying-rug` (66 units) |
| Uncle Wiggily and the Pirates; Or, How the Enemy Craft of Pirate Fox was Sunk | have | PG 61695, `garis-uncle-wiggily-and-the-pirates` (61 units) |
| Uncle Wiggily Goes Swimming; Or, How the Frog Boys Surprised the Fox | have | PG 61735, `garis-uncle-wiggily-goes-swimming` (61 units) |
| Uncle Wiggily on roller skates | have | PG 70017, `garis-uncle-wiggily-on-roller-skates` (87 units) |
| Uncle Wiggily's June Bug friends | have | PG 70627, `garis-uncle-wiggilys-june-bug-friends` (87 units) |
| Uncle Wiggily's funny auto | have | PG 70783, `garis-uncle-wiggilys-funny-auto` (89 units) |
| The adventures of Uncle Wiggily, the bunny rabbit gentleman with the twinkling pink nose | have | PG 71185, `garis-adventures-of-uncle-wiggily` (72 units) |
| The second adventures of Uncle Wiggily | have | PG 71515, `garis-second-adventures-of-uncle-wiggily` (75 units) |
| Uncle Wiggily on the farm | have | PG 71594, `garis-uncle-wiggily-on-the-farm` (90 units) |
| Uncle Wiggily's silk hat | have | PG 72607, `garis-uncle-wiggilys-silk-hat` (105 units) |
| Uncle Wiggily's fishing trip | have | PG 72612, `garis-uncle-wiggilys-fishing-trip` (114 units) |
| Uncle Wiggily's rolling hoop | have | PG 72746, `garis-uncle-wiggilys-rolling-hoop` (120 units) |
| garis-uncle-wiggilys-story-book | excluded | PG 60625, Uncle Wiggily's Story Book: its copyright line reads MCMXXI and MCMXXXIX (1921 and 1939). The 1939 printing may carry material first published that year, so it is held back for Adam rather than added on Gutenberg's clearance alone. |
| garis-series-fiction | excluded | Dick Hamilton, the Curlytops, Larry Dexter, Rick and Ruddy, Teddy, the Smith Boys, the Camp Fire Girls and the Daddy books are series fiction, not story-telling; left out of this shelf. |
| garis-uncle-wiggily-and-old-mother-hubbard | excluded | PG 23213, Uncle Wiggily and Old Mother Hubbard Adventures of the Rabbit Gentleman with the Mother Goose Characters (1922): 97% of its long paragraphs are in Uncle Wiggily and Mother Goose (PG 69458, Fenno 1916), held here. Held once. |

## Annie and Eliza Keary

Shelf: `pipeline/keary_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Tales from Norse mythology retold for children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Heroes of Asgard: Tales from Scandinavian Mythology | have | PG 41283, `keary-heroes-of-asgard` (1075 units) |

## Jean Lang

Shelf: `pipeline/jean-lang_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Greek myths, the Iliad, Spenser and Border legends retold for young readers. Not Andrew Lang. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| A Book of Myths | have | PG 22693, `jean-lang-book-of-myths` (1969 units) |
| Stories from the Iliad; Or, the Siege of Troy | have | PG 68127, `jean-lang-stories-from-the-iliad` (595 units) |
| Stories from the Faerie Queen, Told to the Children | have | PG 41350, `jean-lang-stories-from-the-faerie-queen` (629 units) |
| Stories of the Border Marches | have | PG 14416, `jean-lang-stories-of-the-border-marches` (824 units) |
| jean-lang-story-of-general-gordon | excluded | PG 24756, a biography, not a story-telling book; left out |

## R. E. Francillon

Shelf: `pipeline/francillon_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The Greek myths retold for young readers. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Gods and Heroes; or, The Kingdom of Jupiter | have | PG 45416, `francillon-gods-and-heroes` (1159 units) |

## Ouida (Maria Louise Ramé)

Shelf: `pipeline/ouida_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her stories for children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Bimbi: Stories for Children | have | PG 5834, `ouida-bimbi` (740 units) |
| Moufflou, and Other Stories | have | PG 75655, `ouida-moufflou` (333 units) |
| A Dog of Flanders, The Nürnberg Stove, and Other Stories | have | PG 50032, `ouida-dog-of-flanders-and-other-stories` (1150 units) |
| ouida-dog-of-flanders | excluded | PG 7766, A Dog of Flanders on its own: 91% of its long paragraphs are in PG 50032 (A Dog of Flanders, The Nürnberg Stove, and Other Stories), held here. Held once. |
| ouida-nurnberg-stove | excluded | PG 20997, The Nürnberg Stove on its own (Lippincott, eighth edition): 87% of it is in PG 50032, held here. Held once. |
| ouida-findelkind | excluded | PG 1367, Findelkind on its own: Bimbi (PG 5834), held here, prints the same story, and 78% of the long paragraphs match exactly. Held once. |

## Gene Stratton-Porter

Shelf: `pipeline/stratton-porter_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The Limberlost novels, her other fiction, and The Fire Bird, a story in verse. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Freckles | have | PG 111, `stratton-porter-freckles` (1742 units) |
| A Girl of the Limberlost | have | PG 125, `stratton-porter-girl-of-the-limberlost` (3041 units) |
| Laddie: A True Blue Story | have | PG 286, `stratton-porter-laddie` (2869 units) |
| The Harvester | have | PG 349, `stratton-porter-harvester` (3222 units) |
| At the Foot of the Rainbow | have | PG 532, `stratton-porter-at-the-foot-of-the-rainbow` (1139 units) |
| The Song of the Cardinal | have | PG 533, `stratton-porter-song-of-the-cardinal` (303 units) |
| Michael O'Halloran | have | PG 9489, `stratton-porter-michael-ohalloran` (3989 units) |
| A Daughter of the Land | have | PG 3722, `stratton-porter-daughter-of-the-land` (2367 units) |
| Her Father's Daughter | have | PG 904, `stratton-porter-her-fathers-daughter` (2307 units) |
| The White Flag | have | PG 59823, `stratton-porter-white-flag` (1798 units) |
| The Fire Bird | have | PG 35188, `stratton-porter-fire-bird` (244 units) |
| stratton-porter-second-transcriptions | excluded | PG 26220 (A Girl of the Limberlost), 26465 (The Harvester) and 26582 (Michael O'Halloran) have no plain-text file at Gutenberg (404); the plain-text transcriptions 125, 349 and 9489 are held. |
| stratton-porter-moths-of-the-limberlost | excluded | PG 4907, natural history, not story-telling; left out |
| stratton-porter-wild-heart | excluded | PG 77766, The Wild Heart (1922), is by Emma-Lindsay Squier; Stratton-Porter only wrote its introduction (title page and Gutenberg header). Not hers; left out. |

## Giambattista Basile, tr. John Edward Taylor

Shelf: `pipeline/basile_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Neapolitan fairy tales of the 1630s (Cinderella's and Rapunzel's early cousins) in Taylor's translation, as selected by E. F. Strange. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Stories from the Pentamerone | have | PG 2198, `basile-stories-from-the-pentamerone` (683 units) |

## Giovanni Francesco Straparola, tr. W. G. Waters

Shelf: `pipeline/straparola_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Italian Renaissance tales told over thirteen nights, where several fairy-tale types first appear in print; some are bawdy. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Nights of Straparola, volume 1 | have | PG 75257, `straparola-nights-vol-1` (795 units) |

## Gesta Romanorum, tr. Charles Swan

Shelf: `pipeline/gesta-romanorum_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). The medieval Latin collection of tales with morals that Chaucer, Gower and Shakespeare drew on. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Tales from the Gesta Romanorum | have | PG 58655, `gesta-romanorum-tales` (1470 units) |

## Ellen C. Babbitt

Shelf: `pipeline/babbitt_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Buddhist birth stories retold for young children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Jataka Tales | have | PG 62514, `babbitt-jataka-tales` (464 units) |
| More Jataka Tales | have | PG 7518, `babbitt-more-jataka-tales` (429 units) |

## Abby Morton Diaz

Shelf: `pipeline/abby-diaz_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Her comic and fairy stories for children. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Cats' Arabian Nights, or, King Grimalkum | have | PG 69482, `abby-diaz-cats-arabian-nights` (520 units) |
| The Entertaining Story of King Brondé, His Lily and His Rosebud | have | PG 68833, `abby-diaz-king-bronde` (732 units) |
| The Jimmyjohns, and Other Stories | have | PG 70939, `abby-diaz-jimmyjohns` (1589 units) |
| The William Henry Letters | have | PG 34335, `abby-diaz-william-henry-letters` (1555 units) |
| abby-diaz-essays | excluded | PG 6704 (A Domestic Problem) and 68812 (The Schoolmaster's Trunk) are essays, not stories; left out |

## Beatrice E. Clay

Shelf: `pipeline/beatrice-clay_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Arthurian and Welsh tales retold for young readers. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Stories from Le Morte D'Arthur and the Mabinogion | have | PG 15551, `beatrice-clay-stories-from-morte-darthur-and-mabinogion` (309 units) |

## Emilie and Laura E. Poulsson, trs.

Shelf: `pipeline/poulsson_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Scandinavian children's stories by Topelius, Nyblom and others, in the Poulssons' English. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Top-of-the-World Stories for Boys and Girls | have | PG 36465, `poulsson-top-of-the-world-stories` (797 units) |

## Gudrun Thorne-Thomsen

Shelf: `pipeline/thorne-thomsen_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Stories by Jørgen Moe and Zacharias Topelius in her English. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Birch and the Star, and Other Stories | have | PG 49201, `thorne-thomsen-birch-and-the-star` (324 units) |

## Charles M. Skinner

Shelf: `pipeline/skinner_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). American legends gathered place by place, from the Hudson to the Pacific slope, and from Puerto Rico, Hawaii and the Philippines. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Myths and Legends of Our Own Land (complete) | have | PG 6615, `skinner-myths-and-legends-of-our-own-land` (1183 units) |
| Myths and Legends of Our New Possessions and Protectorate | have | PG 24732, `skinner-myths-and-legends-of-our-new-possessions` (627 units) |
| skinner-own-land-parts | excluded | PG 6606-6614, the nine parts of Myths and Legends of Our Own Land issued separately; the complete file PG 6615 is held, so the parts are held once inside it |

## Richard Wilhelm, ed.; tr. Frederick H. Martens

Shelf: `pipeline/wilhelm_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Chinese fairy tales and legends, in Martens's English after Wilhelm's German. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Chinese Fairy Book | have | PG 29939, `wilhelm-chinese-fairy-book` (1526 units) |

## Im Bang and Yi Ryuk, tr. James S. Gale

Shelf: `pipeline/gale-korean_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Korean tales of imps, ghosts and fairies from two old Korean collections. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Korean Folk Tales | have | PG 51002, `gale-korean-korean-folk-tales` (776 units) |

## Cecil Henry Bompas, tr.

Shelf: `pipeline/bompas_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Santal tales collected by P. O. Bodding and written out in Santali, in Bompas's English. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Folklore of the Santal Parganas | have | PG 11938, `bompas-folklore-of-the-santal-parganas` (1409 units) |

## W. H. Barker and Cecilia Sinclair

Shelf: `pipeline/barker-sinclair_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Anansi stories and other Gold Coast tales. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| West African Folk-Tales | have | PG 66923, `barker-sinclair-west-african-folk-tales` (425 units) |

## Mrs. Rafy

Shelf: `pipeline/rafy_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Tales of the Khasi Hills. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Folk-Tales of the Khasis | have | PG 37884, `rafy-folk-tales-of-the-khasis` (505 units) |

## A. J. Gliński, tr. Maude Ashurst Biggs

Shelf: `pipeline/glinski_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Polish fairy tales from Gliński's collection, with the translator's notes. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Polish Fairy Tales | have | PG 36668, `glinski-polish-fairy-tales` (635 units) |

## Josef Baudiš, tr.

Shelf: `pipeline/baudis_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Czech folk tales. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Czech Folk Tales | have | PG 52596, `baudis-czech-folk-tales` (796 units) |
| baudis-key-of-gold | excluded | PG 20680, The Key of Gold: 23 Czech Folk Tales, has no plain-text file at Gutenberg (404); not fetched |

## Marjory Wardrop, tr.

Shelf: `pipeline/wardrop_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Georgian, Mingrelian and Gurian folk tales. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Georgian Folk Tales | have | PG 44536, `wardrop-georgian-folk-tales` (773 units) |

## W. Henry Jones and Lewis L. Kropf, trs.

Shelf: `pipeline/jones-kropf_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Hungarian tales from Kriza, Erdélyi, Pap and others, with the translators' long introduction and comparative notes; cut introduction > section, tales and notes > tale. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Folk-Tales of the Magyars | have | PG 42981, `jones-kropf-folk-tales-of-the-magyars` (3152 units) |

## P. H. Emerson

Shelf: `pipeline/emerson_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Tales he took down in Anglesey in 1891-2, cut by story with numbered sections and his notes. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Welsh Fairy-Tales and Other Stories | have | PG 8675, `emerson-welsh-fairy-tales` (490 units) |

## Thomas G. Thrum, ed.

Shelf: `pipeline/thrum_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Hawaiian legends gathered from several writers and translators, cut by numbered chapter and section. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Hawaiian Folk Tales | have | PG 18450, `thrum-hawaiian-folk-tales` (1216 units) |

## Charles Sellers

Shelf: `pipeline/sellers_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Spanish and Portuguese folk tales. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Tales from the Lands of Nuts and Grapes | have | PG 31481, `sellers-tales-from-the-lands-of-nuts-and-grapes` (867 units) |

## Elizabeth W. Grierson

Shelf: `pipeline/grierson_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Scottish fairy tales retold, with a glossary. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| The Scottish Fairy Book | have | PG 37532, `grierson-scottish-fairy-book` (1661 units) |

## Mrs. A. W. Hall, tr.

Shelf: `pipeline/angus-hall_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Icelandic fairy tales, cut by tale and chapter. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Icelandic Fairy Tales | have | PG 67085, `angus-hall-icelandic-fairy-tales` (1386 units) |

## W. F. O'Connor, tr.

Shelf: `pipeline/oconnor_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Tibetan tales he collected and translated, with verses from Tibetan love-songs. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Folk Tales from Tibet | have | PG 75000, `oconnor-folk-tales-from-tibet` (827 units) |

## Nellie N. Russell

Shelf: `pipeline/russell_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Chinese folklore and stories, with memorial pieces gathered by the compiler, Mary H. Porter. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Gleanings from Chinese Folklore | have | PG 75089, `russell-gleanings-from-chinese-folklore` (471 units) |

## Anna Jameson

Shelf: `pipeline/jameson_shelf.json` (2026-10-02; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). Saints' and Marian legends told through the pictures made of them; cut by part, section and saint or subject. Not in the manifest; no uids minted.

| Work | Status | Where |
|---|---|---|
| Sacred and Legendary Art, volume 1 | have | PG 69581, `jameson-sacred-and-legendary-art-1` (1911 units) |
| Legends of the Madonna as Represented in the Fine Arts | have | PG 12047, `jameson-legends-of-the-madonna` (1575 units) |

## Fables (existing repo work — cross-referenced, located by search not assumption)

Searched 2026-10-02 (`git grep -il -E 'fable|aesop'` over the whole tree, then every remote branch): **no fables shelf, section or ingest exists in canon-corpus.** The only hits are KJV verses containing "fables", the `fable_review` provenance field, and a note in `pipeline/fetch_sources.py` that Chesterton-introduced Aesop was excluded from his shelf. Nothing is duplicated and no uids are touched.

| Work | Status | Where |
|---|---|---|
| Earlier fables work | pending | locate it: it may live in a sibling repo (armarium, wordhoard) or the vault, which this run cannot reach. Reconcile it with the Aesop shelf above before anything is minted |
