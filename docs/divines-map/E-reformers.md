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
| Sacred Dissertations on the Apostles' Creed, tr. Fraser (2 vols, 1823); on the Lord's Prayer, tr. Pringle (1839); Irenical Animadversions, tr. Bell (1807) | have-raw | `witsius_shelf.json`; translators checked |

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
| Wodrow's Correspondence, ed. Thomas M'Crie (3 vols, 1842-43) | have-raw | `robert-wodrow_shelf.json` |
| Bruce's Sermons on the Sacrament, tr. Laidlaw (1901); Andrew Melville | pending | not yet searched |

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
| James Fergusson, Brief Exposition of Galatians to Thessalonians (reprint, Ward, 1841) | have-raw | `james-fergusson_shelf.json` |
| George Hutcheson, Brief Exposition on the XII Small Prophets (1657); Forty-Five Sermons on Psalm 130 (1691) | have-raw | `george-hutcheson_shelf.json`, EEBO scans |
| George Hutcheson, Exposition of John (1657); of Job (1669) | pending | no pre-1930 scan on IA |
| Andrew Gray, Works, pref. Tweedie (Aberdeen, 1839) | have-raw | `andrew-gray_shelf.json` |
| Alexander Henderson, Sermons, Prayers and Pulpit Addresses, ed. Martin (1867) | have-raw | `alexander-henderson_shelf.json` |
| Alexander Shields, A Hind Let Loose (Glasgow, 1797) | have | `alexander-shields_shelf.json`, Gutenberg transcription |
| Willison, Practical Works, with Hetherington's essay (Blackie, undated) | have-raw | `willison_shelf.json` |
| Witherspoon, Works (Edinburgh, 1804-05, 9 vols) | have-raw | `witherspoon_shelf.json`; vol. VIII pending on an archive server error |

## Scottish church histories

The narrative histories of the Kirk from the Reformation to the Revolution, in their 19th-century club editions. Calderwood, Row and Blair are in the Wodrow Society section above; Knox's History is in his Works.

| Work | Status | Where |
|---|---|---|
| Spottiswoode, History of the Church of Scotland, ed. Russell and Napier (Spottiswoode Society, 3 vols, 1847-1851) | have-raw | `spottiswoode_shelf.json`, Princeton copies (1851 issue); the NLS copies carry CC BY-NC-SA, so they are alternates |
| Baillie, Letters and Journals 1637-1662, ed. Laing (Bannatyne Club, 3 vols, 1841-1842) | have-raw | `robert-baillie_shelf.json` |
| Wodrow, History of the Sufferings of the Church of Scotland, ed. Burns (4 vols, 1828-1830) | have-raw | `robert-wodrow_shelf.json` |
| Kirkton, Secret and True History of the Church of Scotland, ed. Sharpe (1817) | have-raw | `kirkton_shelf.json` |
| M'Crie, Life of John Knox (ed. by his son, 1873); Life of Andrew Melville (2 vols, 1819); the Reformation in Italy and in Spain (1842 reprints) | have-raw | `thomas-mccrie_shelf.json` |
| Thomas M'Crie the younger, Sketches of Scottish Church History (6th ed., 1849, Google scan); Life of Thomas M'Crie (1842) | have-raw | `thomas-mccrie_shelf.json` |
| Howie, The Scots Worthies, rev. Carslaw (1870) | have-raw | `howie_shelf.json` |
| A Cloud of Witnesses, ed. J. H. Thomson (1871) | have-raw | `cloud-of-witnesses_shelf.json`; name check on the editor |
| Sermons Delivered in Times of Persecution in Scotland, ed. Kerr (1880) | have-raw | `covenanter-sermons_shelf.json`; name check on the editor |
| Michael Shields, Faithful Contendings Displayed, ed. Howie (1780) | have-raw | `michael-shields_shelf.json` |
| Robert Fleming, The Fulfilling of the Scripture (Charlestown, 1806, from Foxcroft's 1743 text) | have-raw | `robert-fleming_shelf.json` |
| Free Church Committee: Memoirs of Veitch, Hog, Henry Erskine and Carstairs (1846); Lives of Henderson and James Guthrie (1846) | have-raw | `free-church-committee_shelf.json` |
| Patrick Walker, Six Saints of the Covenant, ed. D. Hay Fleming (2 vols, 1901) | have-raw | `patrick-walker_shelf.json` |
| Patrick Walker, Biographia Presbyteriana (2 vols, 1827; vol. 2 adds Shields's Life of Renwick) | have-raw | `patrick-walker_shelf.json` |
| Hetherington, History of the Church of Scotland to 1843 (New York, 1856) | have-raw | `hetherington_shelf.json` |
| John Cunningham, The Church History of Scotland, 2nd ed. (2 vols, 1882) | have-raw | `john-cunningham_shelf.json`; not lane A's William Cunningham |
| D. Hay Fleming, The Reformation in Scotland (Stone Lectures, 1910) | have-raw | `hay-fleming_shelf.json` |
| D. Hay Fleming, The Story of the Scottish Covenants in Outline (1904) | have | `hay-fleming_shelf.json`, Gutenberg transcription |
| Wodrow's Analecta (Maitland Club, 4 vols, 1842-43) | have-raw | `robert-wodrow_shelf.json` |
| Wodrow's Collections upon the Lives of the Reformers (Maitland Club, 2 vols, 1834-45) | have-raw | `robert-wodrow_shelf.json`; National Library of Scotland scans, CC BY-NC-SA on the digital copy (noted, not ruled on) |
| Kirkton's Life of John Welsh | pending | not yet searched |
| Acts and Proceedings of the General Assemblies 1560-1618, the 'Booke of the Universall Kirk' (Bannatyne Club, 3 parts, 1839-1845) | have-raw | `general-assembly_shelf.json` |
| Peterkin, Records of the Kirk of Scotland, the Assemblies from 1638 (vol. 1, 1838) | have-raw | `general-assembly_shelf.json` |
| Acts of the General Assembly of the Church of Scotland 1638-1842 (Church Law Society, 1843) | have-raw | `general-assembly_shelf.json` |

## Secession, Disruption and Irish Presbyterian histories

| Work | Status | Where |
|---|---|---|
| M'Kerrow, History of the Secession Church (2 vols, 1839) | have-raw | `john-mckerrow_shelf.json` |
| Robert Buchanan, The Ten Years' Conflict (2 vols, 1849) | have-raw | `robert-buchanan_shelf.json` |
| Thomas Brown, Annals of the Disruption (1884) | have-raw | `thomas-brown-disruption_shelf.json` |
| Reid, History of the Presbyterian Church in Ireland, continued by Killen (3 vols, 1867) | have-raw | `james-seaton-reid_shelf.json` |

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
| Lightfoot, Journal of the Proceedings of the Assembly, 1643-1644 (Whole Works vol. 13, ed. Pitman) | have-raw | `john-lightfoot_shelf.json` |

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
| Strype, Ecclesiastical Memorials (1822, 6 parts), Annals (1824, 7 parts), Lives of Parker, Whitgift (3 vols each), Grindal, Aylmer, Cheke (1821), Sir Thomas Smith (1820) (Clarendon Press); Memorials of Cranmer (EHS, 1848-54, 3 vols) | have-raw | `strype_shelf.json`, 26 volumes |

## Reformed bishops of the Stuart Church

| Work | Status | Where |
|---|---|---|
| Ussher, Whole Works, ed. Elrington (Dublin, 1847-64): the English vols. I-IV, XI, XIII, XV-XVII | have-raw | `ussher_shelf.json` |
| Ussher, Whole Works, the Latin vols. V-X, XII, XIV | pending | Latin; shelve if Latin texts are wanted |
| Davenant, Exposition of Colossians with the Dissertation on the Death of Christ (2 vols, 1831-32); Treatise on Justification (2 vols, 1844-46), tr. Allport | have-raw | `davenant_shelf.json`; translator checked on 3 of 4 |

## English Puritan histories

The lives of the Puritans themselves are on lane A's shelves; these are the histories and biographical dictionaries of the movement. Fuller's Church History is on lane A's `thomas-fuller` shelf.

| Work | Status | Where |
|---|---|---|
| Neal, The History of the Puritans, Toulmin's text (Tegg, 3 vols, 1837) | have-raw | `daniel-neal_shelf.json` |
| Brook, The Lives of the Puritans (3 vols, 1813) | have-raw | `benjamin-brook_shelf.json` |
| Calamy, The Nonconformist's Memorial, ed. Palmer (3 vols, 1802-1803) | have-raw | `edmund-calamy_shelf.json` |
| Calamy, Abridgement of Baxter's Life and Times (1713, 1727) | pending | 18th-century scans only; not yet read |

## Continental Reformed and the Reformation in Europe

| Work | Status | Where |
|---|---|---|
| The Articles of the Synod of Dort, tr. Thomas Scott (Philadelphia, 1831; London 1818) | have-raw | `synod-of-dort_shelf.json`; translator checked |
| Pictet, Christian Theology, tr. Reyroux (London, 1834) | have-raw | `benedict-pictet_shelf.json`; translator checked |
| Merle d'Aubigné, History of the Reformation of the Sixteenth Century, tr. White (ATS, 5 vols) | have-raw | `merle-daubigne_shelf.json`; translator checked |
| Merle d'Aubigné, History of the Reformation in Europe in the Time of Calvin (Longmans, 1863-78, 8 vols) | have-raw | `merle-daubigne_shelf.json`; Cates checked on vols 6-8 |
| Merle d'Aubigné, The Protector: a Vindication (1848) | have-raw | `merle-daubigne_shelf.json` |
| Zanchius, Absolute Predestination, tr. Toplady | have | in lane A's Toplady Works |
| Brandt, History of the Reformation in the Low-Countries (1720-23, 4 vols) | pending | ECCO OCR too broken to read two volumes' numbers |
| Baird, Rise of the Huguenots (2 vols, 1879); Huguenots and Henry of Navarre (2 vols, 1886); Huguenots and the Revocation (1895, vol. 1); Theodore Beza (1899) | have-raw | `henry-baird_shelf.json`; Revocation vol. 2 pending |
| Wylie, The History of Protestantism (Cassell, 3 vols); The Papacy (1852); Daybreak in Spain ([1870]) | have-raw | `james-wylie_shelf.json` |
| Muston, The Israel of the Alps, tr. Montgomery (Blackie, 1875, 2 vols) | have-raw | `alexis-muston_shelf.json` |
| Turretin on the Atonement of Christ, tr. Willson (New York, 1859) | have-raw | `turretin_shelf.json`; translator checked; the full Institutes are in copyright (1992) |

## Confessions and creeds

| Work | Status | Where |
|---|---|---|
| Schaff, The Creeds of Christendom (3 vols; CCEL, proofed) | have | `philip-schaff_shelf.json`; vols I-II from the 1919 sixth edition, vol. III from a reprint of 1889; CCEL's vol. III lacks Part First (Lutheran) |
| The Harmony of Protestant Confessions, ed. Peter Hall (1842) | have-raw | `peter-hall_shelf.json` |
| Dunlop, A Collection of Confessions of Faith (1719-22, 2 vols) | pending | only long-s 18th-century scans, OCR at about a third common words |
| Sprott and Leishman, Book of Common Order (Knox's Liturgy) and the Westminster Directory (1868) | have-raw | `george-sprott_shelf.json` |
| Sprott, Scottish Liturgies of the Reign of James VI (revised, 1901); The Worship and Offices of the Church of Scotland (1882) | have-raw | `george-sprott_shelf.json` |
