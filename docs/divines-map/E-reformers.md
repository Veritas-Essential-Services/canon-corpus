# English and Scottish Reformers, Ursinus, Witsius

Built 2026-10-03 on its own branch (not a relay lane), with the relay's `pipeline/fetch_shelf.py` unchanged. Every shelf passed `fetch_shelf.py <shelf> --verify --record` (identity, surname, rights line; results in each shelf's `_checks`). Internet Archive volumes are raw OCR (the Edwards precedent); each title page was read before listing. Nothing minted into `data/uids/`; every slug below awaits Adam's minting pass.

## The Parker Society reformers

| Work | Status | Where |
|---|---|---|
| Cranmer, Writings and Disputations on the Lord's Supper (1844); Miscellaneous Writings and Letters (1846), ed. Cox | have-raw | `cranmer_shelf.json`, IA `writingsanddispu01cranuoft`, `writingscranmer02cranuoft` |
| Cranmer, Remains, ed. Jenkyns (Oxford 1833) | pending | not yet located |
| Cranmer, A Necessary Doctrine | excluded | CCEL serves a 922-word fragment with no source line |
| Latimer, Sermons (1844); Sermons and Remains (1845), ed. Corrie | have-raw | `latimer_shelf.json`, IA `sermonsedforpark31latiuoft`, `sermonsedforthep32latiuoft` |
| Latimer, Sermons (CCEL); Sermons on the Card, ed. Morley (1883) | have | CCEL `latimer/sermons` (608 units), PG 2458 (145 units) |
| Ridley, Works, ed. Christmas (1841) | have-raw | `ridley_shelf.json`, IA `ridleysworks00ridluoft` |
| Hooper, Early Writings (1843); Later Writings (1852) | have-raw | `john-hooper_shelf.json`, IA `earlywritingsofj0026hoop` (Toronto copy's text file returns HTTP 500), `laterwritingsofb25hoopuoft` |
| Bradford, Writings, ed. Townsend (2 vols, 1848, 1853) | have-raw | `john-bradford_shelf.json`, IA `writingsofjohnbr01braduoft`, `02braduoft` |
| Bradford, Godly Meditations; Sermons and Tracts | have | CCEL (205 and 229 units) |
| Jewel, Works, ed. Ayre (4 portions, 1845-1850) | have-raw | `jewel_shelf.json`, IA Toronto vols 1, 2, 4 + Princeton vol 3 |
| Jewel, Works, ed. Jelf (8 vols, Oxford 1848) | pending | Toronto scans found; a possible second witness |
| Becon, Early Works (1843); Catechism (1844); Prayers and Other Pieces (1844), ed. Ayre | have-raw | `becon_shelf.json`, IA Toronto |
| Bullinger, Decades I-V, tr. H. I., ed. Harding (4 vols, 1849-1852) | have-raw | `heinrich-bullinger_shelf.json`, IA Toronto (its volume numbers differ from the set's) |
| Bullinger's letters (Zurich Letters, Original Letters) | pending | a Parker Society miscellany shelf |
| Tyndale, Doctrinal Treatises (1848); Expositions and Practice of Prelates (1849); Answer to More (1850), ed. Walter | have-raw | `william-tyndale_shelf.json` (prose works; his Bible is a witness on PR #11) |
| Whitaker, Disputation on Holy Scripture (1849) | have-raw | `william-whitaker_shelf.json` |
| Fulke, Defence of the Translations (1843); Answers to Stapleton, Martiall, Sanders (1848) | have-raw | `william-fulke_shelf.json` |
| Coverdale, Writings and Translations (1844); Remains (1846) | have-raw | `myles-coverdale_shelf.json` (his Bible is a witness on PR #11) |
| Grindal, Remains (1843) | have-raw | `grindal_shelf.json` |
| Sandys, Sermons (1841) | have-raw | `edwin-sandys_shelf.json` |
| Pilkington, Works (1842) | have-raw | `james-pilkington_shelf.json` |
| Philpot, Examinations and Writings (1842) | have-raw | `john-philpot_shelf.json` |
| Hutchinson, Works (1842) | have-raw | `roger-hutchinson_shelf.json` |
| Rogers, Catholic Doctrine of the Church of England (1854) | have-raw | `thomas-rogers_shelf.json` |
| Nowell, Catechism, Latin with Norton's English (1853) | have-raw | `nowell_shelf.json`; Norton checked as translator |
| Whitgift, Works (3 portions, 1851-1853) | have-raw | `whitgift_shelf.json` |
| Calfhill, Answer to Martiall (1846); Bale, Select Works (1849); Cooper, Answer in Defence (1850); Woolton, Christian Manual (1851) | have-raw | `calfhill`, `john-bale`, `thomas-cooper`, `woolton` shelves |
| Liturgies of Edward VI (1844); Liturgical Services of Elizabeth (1847); Private Prayers of Elizabeth (1851); Bull's Christian Prayers (1842) | have-raw | `parker-society_shelf.json` |
| Zurich Letters, first series (1842) and its Latin originals; second series (1845); Original Letters (2 portions, 1846-1847); Epistolae Tigurinae (1848) | have-raw | `parker-society_shelf.json` |
| Correspondence of Matthew Parker (1853); Select Poetry of Elizabeth's reign (2 parts, 1845); General Index (1855) | have-raw | `parker-society_shelf.json` |
| Zurich Letters, second series, Latin originals | pending | not yet identified among the scans |

## John Knox

| Work | Status | Where |
|---|---|---|
| Works, ed. Laing, vols 1-2 (History of the Reformation) | have | PG 21938, 40886 (8,165 units) |
| Works, ed. Laing, vols 3-6 | have-raw | `john-knox_shelf.json`, IA (vol 3 1854, vol 4 1895 reissue, vols 5-6) |
| First Blast of the Trumpet | have | CCEL (141 units), keyed from Southgate, London (1878) |
| Treatise on Prayer (CCEL) | pending | CCEL keyed it from a 1995 modern-spelling reprint; the original is in Laing vol. 3 (Confession or Prayer on the Death of Edward VI) |
| History, ed. Lennox (1905, modernised) | pending | PG 48250; a possible second witness |

## Zacharias Ursinus

| Work | Status | Where |
|---|---|---|
| Commentary on the Heidelberg Catechism, tr. G. W. Williard, 2nd American ed. (Columbus 1852) | have-raw | `ursinus_shelf.json`, IA `commdrza00ursi`; translator checked |
| The Summe of Christian Religion, tr. Parry (1587) | pending | earlier translation |
| CCEL essays (What is Catechism?, What is the Gospel) | excluded | no source or rights line |

## Herman Witsius

| Work | Status | Where |
|---|---|---|
| The Oeconomy of the Covenants (3 vols, New York 1798) | have-raw | `witsius_shelf.json`, IA Princeton; translator not named in the text |
| Sacred Dissertations on the Apostles' Creed (1823); on the Lord's Prayer (1839); Irenical Animadversions (1807) | pending | Princeton scans, not yet title-checked |

## John Calvin: gaps beside lane A's shelf

Lane A's `calvin_shelf.json` already holds the Calvin Translation Society set (45 commentary volumes through `fetch_sources.py`, Beveridge's Institutes, the Tracts and Bonnet's Letters). This separate shelf adds what it lists as not searched, and leaves lane A's file untouched.

| Work | Status | Where |
|---|---|---|
| Institutes, tr. John Allen (London 1813; first American ed., Philadelphia 1816, 3 vols) | have-raw | `calvin-gaps_shelf.json`, IA Princeton 1816 set; translator checked |
| Calvin's Calvinism (Eternal Predestination; Secret Providence), tr. Henry Cole (1856-57) | have-raw | `calvin-gaps_shelf.json`, 1927 SGU reprint with both parts; translator checked |
| Institutes, tr. Norton (1561); Golding's sermon translations | pending | early-print scans only |

## The Wodrow Society

| Work | Status | Where |
|---|---|---|
| Calderwood, History of the Kirk of Scotland, ed. Thomson (8 vols, 1842-1849) | have-raw | `calderwood_shelf.json` |
| James Melville, Autobiography and Diary, ed. Pitcairn (1842) | have-raw | `james-melville_shelf.json` |
| Rollock, Select Works, ed. Gunn (2 vols, 1844-1849) | have-raw | `rollock_shelf.json` |
| Robert Bruce, Sermons, ed. Cunningham (1843) | have-raw | `robert-bruce_shelf.json` |
| Miscellany of the Wodrow Society, vol. 1 (1844) | have-raw | `wodrow-society_shelf.json` |
| Select Biographies, ed. Tweedie (2 vols, 1845-1847): Welsh, Simson, Livingstone, Dickson, Guthrie, Fraser of Brea, Nisbet | have-raw | `wodrow-society_shelf.json` |
| Knox's Works, ed. Laing (Wodrow Society vols) | have | `john-knox_shelf.json` |
| Row, History of the Kirk, ed. Laing (1842) | have-raw | `john-row_shelf.json` |
| Blair, Life and Autobiography, ed. M'Crie (1848) | have-raw | `robert-blair_shelf.json` |
| Bruce's Sermons on the Sacrament, tr. Laidlaw (1901); Andrew Melville; Wodrow's Correspondence (3 vols, 1842-43) | pending | not yet searched |

## Scottish divines: gaps beside lane A's shelves

Lane A already holds Boston's Complete Works (`boston_shelf.json`), Ebenezer and Ralph Erskine (`erskines_shelf.json`), Gillespie's Works vol. 1 and Aaron's Rod (`george-gillespie_shelf.json`), Durham's Christ Crucified, Law Unsealed, Revelation and Clavis Cantici (`durham_shelf.json`), and Rutherford's Letters, Lex Rex and major treatises (`rutherford_shelf.json`, with Bonar's editions on `andrew-bonar_shelf.json`). These separate shelves add only what those files list as pending or lack, and leave them untouched.

| Work | Status | Where |
|---|---|---|
| Rutherford, Christ Dying and Drawing Sinners to Himself (1647) | have-raw | `rutherford-gaps_shelf.json`, the second Princeton scan, which names him |
| Rutherford, A Survey of the Spiritual Antichrist (1648) | have-raw | `rutherford-gaps_shelf.json`, EEBO scan |
| Rutherford, A Peaceable and Temperate Plea for Paul's Presbyterie (1642) | have-raw | `rutherford-gaps_shelf.json` |
| Rutherford, Divine Right of Church-Government (1646); Influences of the Life of Grace (1659) | pending | the 1646 scan lacks its title page; no 1659 scan found |
| Durham, The Dying Man's Testament, or a Treatise concerning Scandal (1659) | have-raw | `durham-gaps_shelf.json`, identity read by eye ('DVRHAM') |
| Durham, The Blessedness of the Death of those that die in the Lord (1682) | have-raw | `durham-gaps_shelf.json`, EEBO scan |
| Durham, The Unsearchable Riches of Christ (1764) | have-raw | `durham-gaps_shelf.json`, ECCO scan |
| Durham, Heaven upon Earth (1685, 1732); The Great Corruption of Subtile Self (1686) | pending | name unreadable in the OCR; OCR too poor |
| Boston; the Erskines | have | lane A, complete; no gaps found |
| Gillespie, Works vol. 2 (1846); Miscellany Questions (1649) | pending | no usable scan; his Parliament sermons are already in Works vol. 1 |
| Patrick Gillespie, The Ark of the Covenant Opened (1677) | pending | anonymous on its title page |

## Scottish church histories

The narrative histories of the Kirk from the Reformation to the Revolution, in their 19th-century club editions. Calderwood, Row and Blair are in the Wodrow Society section above; Knox's History is in his Works.

| Work | Status | Where |
|---|---|---|
| Spottiswoode, History of the Church of Scotland, ed. Russell and Napier (Spottiswoode Society, 3 vols, 1847-1851) | have-raw | `spottiswoode_shelf.json`, NLS set |
| Baillie, Letters and Journals 1637-1662, ed. Laing (Bannatyne Club, 3 vols, 1841-1842) | have-raw | `robert-baillie_shelf.json` |
| Wodrow, History of the Sufferings of the Church of Scotland, ed. Burns (4 vols, 1828-1830) | have-raw | `robert-wodrow_shelf.json` |
| Kirkton, Secret and True History of the Church of Scotland, ed. Sharpe (1817) | have-raw | `kirkton_shelf.json` |
| M'Crie, Life of John Knox (ed. by his son, 1873); Life of Andrew Melville (2 vols, 1819) | have-raw | `thomas-mccrie_shelf.json` |
| Howie, The Scots Worthies, rev. Carslaw (1870) | have-raw | `howie_shelf.json` |
| A Cloud of Witnesses, ed. J. H. Thomson (1871) | have-raw | `cloud-of-witnesses_shelf.json`; name check on the editor |
| Wodrow's Analecta (Maitland Club, 1842-43); Kirkton's Life of John Welsh | pending | not yet searched |

## The Westminster Assembly

Lane A holds Warfield's Westminster studies and the Assembly divines Reynolds and Bridge; Baillie's Letters are above. These shelves add the Assembly's own record and its 19th-century historians.

| Work | Status | Where |
|---|---|---|
| Minutes of the Sessions, Nov 1644 to Mar 1649, ed. Mitchell and Struthers (1874) | have-raw | `westminster-assembly_shelf.json` |
| The Confession, Larger and Shorter Catechisms, Directories, Form of Church Government, Covenants (Nelson, 1877) | have-raw | `westminster-assembly_shelf.json` |
| Gillespie, Notes of Debates and Proceedings, 1644-1645, ed. Meek (1846) | have-raw | `gillespie-gaps_shelf.json`; Google scan |
| Mitchell, The Westminster Assembly: its History and Standards (1883); Catechisms of the Second Reformation (1886) | have-raw | `alexander-mitchell_shelf.json` |
| Hetherington, History of the Westminster Assembly (1843; New York 1868 printing) | have-raw | `hetherington_shelf.json` |
| Shaw, Exposition of the Confession of Faith (2nd ed., 1846) | have-raw | `robert-shaw_shelf.json` |
| Lightfoot's Journal of the Assembly (Works vol. 13, 1824) | pending | not yet searched |

## Free Church of Scotland divines

Other lanes already hold William Cunningham, Thomas Chalmers and James Buchanan. These shelves add their New College colleagues and two Highland ministers.

| Work | Status | Where |
|---|---|---|
| Bannerman, The Church of Christ (2 vols, 1868) | have-raw (vol. 1) | `james-bannerman_shelf.json`; vol. 2 pending on an Internet Archive server error |
| Bannerman, Inspiration: the Infallible Truth and Divine Authority of the Holy Scriptures (1865) | have-raw | `james-bannerman_shelf.json` |
| Smeaton, The Doctrine of the Atonement as taught by Christ Himself (1868); as taught by the Apostles (1870); The Doctrine of the Holy Spirit (1882) | have-raw | `george-smeaton_shelf.json` |
| Kennedy, The Days of the Fathers in Ross-shire (4th ed., 1867) | have-raw | `john-kennedy-dingwall_shelf.json` |
| Hugh Martin, The Atonement (1877); The Prophet Jonah (3rd ed., 1880) | have-raw | `hugh-martin_shelf.json` |
| Hugh Martin, The Shadow of Calvary | pending | no pre-1930 scan found |

## English Reformation histories

| Work | Status | Where |
|---|---|---|
| Foxe, The Acts and Monuments, ed. Cattley, with Townsend's dissertation (8 vols, 1837-1841) | have-raw | `john-foxe_shelf.json`; the full text, not the abridged Book of Martyrs |
| Burnet, History of the Reformation of the Church of England, ed. Pocock (7 vols, Oxford, 1865) | have-raw | `gilbert-burnet_shelf.json` |
| Strype's Memorials, Annals and Lives (Oxford, 1812-1840) | pending | not yet searched |
