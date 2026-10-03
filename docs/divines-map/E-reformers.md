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
| Remaining Parker Society authors (Coverdale, Tyndale, Whitgift, Pilkington, Fulke, Grindal, Sandys, Nowell, Hutchinson, Whitaker, Philpot, Rogers, Parker...) | pending | IA Toronto and California scans seen; not in this ask |

## John Knox

| Work | Status | Where |
|---|---|---|
| Works, ed. Laing, vols 1-2 (History of the Reformation) | have | PG 21938, 40886 (8,165 units) |
| Works, ed. Laing, vols 3-6 | have-raw | `john-knox_shelf.json`, IA (vol 3 1854, vol 4 1895 reissue, vols 5-6) |
| First Blast of the Trumpet; Treatise on Prayer | have | CCEL (141 and 71 units) |
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
