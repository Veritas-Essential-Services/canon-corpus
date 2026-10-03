#!/usr/bin/env python3
"""
build_commentary.py -- the whole-Bible commentaries keyed to KJV verse ids:
which verses each comment is on, and which verses it cites.

    python3 pipeline/build_commentary.py --fetch   # CCEL's texts + the scans' OCR, sha256-pinned
    python3 pipeline/build_commentary.py           # -> data/commentary/*.jsonl + manifest.json, build/commentary/
    python3 pipeline/build_commentary.py --check   # rebuild in memory: byte-identical to the committed files
    python3 pipeline/build_commentary.py --collate # CCEL's wording vs the period scans -> collation.json

THE BOOKS (CCEL ThML; each CCEL print source recorded and checked: a print
source dated 1930 or later is flagged `ccel_print_source_check`, as
fetch_shelf.py does):
  henry   Matthew Henry, Exposition of the Old and New Testaments (1706-21;
          Acts to Revelation finished by other ministers), six volumes
  jfb     Jamieson, Fausset and Brown, Commentary Critical and Explanatory
          on the Whole Bible (1871)
  barnes  Albert Barnes, Notes on the New Testament (CCEL keyed it from
          Baker's 1949 reprint: flagged)
  wesley  John Wesley, Explanatory Notes upon the Old and New Testaments
          (CCEL marks chapters only: split_verses cuts at each note's number)
  calvin  John Calvin, Commentaries, Calvin Translation Society, 45 volumes
          (the translators' footnotes dropped: drop_notes)
and one from EEBO-TCP (hand-keyed from the first edition, CC0):
  poole   Matthew Poole, Annotations upon the Holy Bible (1683-85): read by
          build_tcp_work, one comment per verse with a note (below)
and one read from scans, there being no keyed text:
  clarke  Adam Clarke, Commentary (1810-26): archive.org OCR of two
          printings of each Testament (1843 and 1846 OT, 1846 and 1835 NT),
          read by clarke_read.py; build_scan_work commits a citation only
          when both printings read it in their notes on the same verse

A COMMENT. CCEL marks each comment's passage with an empty
<scripCom osisRef=.../>. A comment runs from its mark to the next one, or to
the next division; marks with no comment text between them are one comment,
on the most precise passage named (Henry marks the chapter, then its first
section; Barnes the verse, then its chapter). Text before a chapter's first
mark is that chapter's introduction.

TWO READINGS OF WHERE A COMMENT IS. The mark is one. The other is read from
the comment itself, never from the mark:
  henry   the verse numbers printed in the passage Henry quotes ("1 In the
          beginning ... 2 And the earth"): first and last;
  jfb     the verse number that opens the first lemma ("<b>13. pitieth</b>"),
          in the chapter of the enclosing "Chapter N" division;
  barnes  the division's title ("Matthew 2:14").
Each row says whether they agree (`anchor`: agrees / differs / unread).

WHAT A COMMENT CITES is voted as in build_topical.py: CCEL's scripRef tags
and topical_read.refs() read independently (with "ver. 31" and "ch. 3:5"
taken in the comment's own book and chapter); a citation is committed when
both read it, or when one does and print does too.

Committed: anchors and citations (kjv: ids). The prose, public domain but
CCEL's keyed text, is written to build/commentary/ only.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import topical_read as R  # noqa: E402
import tsk_read as T  # noqa: E402
import build_topical as BT  # noqa: E402
import clarke_read as CR  # noqa: E402
import spurgeon_read as SR  # noqa: E402

CORPUS = os.path.join(ROOT, "data", "corpus", "commentary")
OUT = os.path.join(ROOT, "data", "commentary")
BUILD = os.path.join(ROOT, "build", "commentary")
CCEL = "https://ccel.org/ccel/"
IA = "https://archive.org/download/"
TCP = "https://raw.githubusercontent.com/textcreationpartnership/"

WORKS = {
    "henry": {
        "title": "An Exposition of the Old and New Testaments (Commentary on the Whole Bible)",
        "author": "Matthew Henry (1662-1714); Acts to Revelation completed by other ministers after his death",
        "files": [
            ("henry1", "h/henry/mhc1.xml", "6eb946647f806f46129001f83013d65c51e40ac59b939ac1c51404aa50375971"),
            ("henry2", "h/henry/mhc2.xml", "673fcb4168ad946ab1e6923c0e331cc61e4adca4498fc0ee34cf1507285aa2f7"),
            ("henry3", "h/henry/mhc3.xml", "8ba9779eba5d326acbfc9acaccf2ea1fa2d6b5c48b03ab86fc5e80b0bfa5b17e"),
            ("henry4", "h/henry/mhc4.xml", "7b6ea0800caa1daab6b0c807f5b95c7567fb5d880290bbe91d848048a80486b2"),
            ("henry5", "h/henry/mhc5.xml", "8b0853b116e9a68215a594bafe29f45502d4c766e1f128cbf5fb050f45cf2518"),
            ("henry6", "h/henry/mhc6.xml", "296195d09d4fbb1e7516ea77c100dbc87ce37542c3109f9f570c3cf155b594c1"),
        ],
        "scans": [
            ("London, 1828, six volumes (NOT_IN_COPYRIGHT)", [
                ("expositionofoldn01henr", "636a85f8a1a4eed5d03052928afe4276a92374379044d9f5ff0e3b5c401ce1f1"),
                ("expositionofoldn02henr", "20a13bb63b858af42d8fb48853765a19eaba3ffd5e32c45e6e271b08f1c3de49"),
                ("expositionofoldn03henr", "afd16953a6d5ab8b9ed8b8888ece4927a29be93d095552072ef7ac0448af9857"),
                ("expositionofoldn04henr", "6b31c0416194905e0ce93ec4d2779720a22c0c759a621c5a85b15e6de4ba61e2"),
                ("expositionofoldn05henr", "7e840d9172f37cfc1ff625042d042d254f55bb242cfcc00dd85af4cd36ecc053"),
                ("expositionofoldn06henr", "faab8cbebfceb2bdb5152768566e3fbcf678dd4a2841fc03f113e18cdcc52b24"),
            ]),
        ],
    },
    "jfb": {
        "title": "A Commentary, Critical and Explanatory, on the Old and New Testaments",
        "author": "Robert Jamieson, A. R. Fausset, David Brown",
        "files": [("jfb", "j/jamieson/jfb.xml", "ce16900c4795d9bd3dc7f7aaec3fccd395c166d4d9593a14b9aae06869aab9af")],
        "scans": [
            ("1873 one-volume printing (NOT_IN_COPYRIGHT)", [
                ("commentarycritic00jami", "eb90ea6bcf888c0ae1cff1cf6467cd781dbff74469c2ec7ae253471c45518066")]),
            ("1879 one-volume printing", [
                ("commentarycritic00jami_0", "004ffabd4c3f1ab0ecc45346383eb51341a0ffa8098ac32a8e33b972a637fd53")]),
        ],
    },
    "poole": {
        "kind": "tcp",
        "title": "Annotations upon the Holy Bible",
        "author": "Matthew Poole (1624-1679); from Isaiah 59 on, finished after his death by other ministers (Vol. II)",
        "files": [
            ("poole1", TCP + "A55363/master/A55363.xml", "fc494999def0b470be3e1d826d1bb310fe2e627da7d9946067485ddc92fbe6b5"),
            ("poole2", TCP + "A55368/master/A55368.xml", "88e15a73286b932440edfa76936b374ba63360ffea2d62d0d3ba514c5cf9a6e6"),
        ],
        "scans": [],
    },
    "barnes": {
        "title": "Notes, Explanatory and Practical, on the New Testament",
        "author": "Albert Barnes (1798-1870)",
        "files": [("barnes", "b/barnes/ntnotes.xml", "88fdc365052dd5e037ce7e6d5d797b1a5b3ba8591f62b6b3755a706feb853e05")],
        "print_books": {"Matt", "Mark", "Luke", "John"},     # all the open 1840 scans cover
        "scans": [
            ("the Gospels only, 1840, two volumes (the rest of the New Testament is not checked)", [
                ("notesexplanatory01inbarn", "6ece4e6dc4f095e90d7addd5d4f6af7f67af23db74c7fba31df019a974d8a869"),
                ("notesexplanatory02barn_0", "c920932b4ae56677b20916478b75764e059a4118a066c0c90f49e4cde2cab19a")]),
        ],
    },
    "wesley": {
        "title": "Explanatory Notes upon the Old and New Testaments",
        "author": "John Wesley (1703-1791)",
        "files": [("wesley", "w/wesley/notes.xml", "c4534a8964bb8900256ade116209e2bb114caab6100b098b20bf68b682e3fdce")],
        "split_verses": True,       # CCEL marks the chapter; each note opens with its verse number
        "roman_comma": True,        # "Luke iii, 31"
        "scans": [],
    },
    "calvin": {
        "title": "Commentaries (Calvin Translation Society, Edinburgh, 1843-55)",
        "author": "John Calvin (1509-1564); translated and annotated by the Calvin Translation Society's editors",
        "files": [
            ("calvin01", "c/calvin/calcom01.xml", "4b700a5aa4f799f9363cc232cde85409a4f2ff58ebba6c82d9c4830ba83c7b33"),
            ("calvin02", "c/calvin/calcom02.xml", "fa675fccdbe4d1ad0e555069e0c00c46d732974cc1989b1ca3df87bb073f0663"),
            ("calvin03", "c/calvin/calcom03.xml", "5f153f44091059eff0d75451785cee7e3d0d9e63edecee645fe7b1b7c1dcaf53"),
            ("calvin04", "c/calvin/calcom04.xml", "d0af9b325ea95e6fec6cd69e7cb67e660379868cfed63006424e147e086db721"),
            ("calvin05", "c/calvin/calcom05.xml", "228608eda64658283ba7672b84267f0a62615eec37abe72c2128ede9fce9ee7c"),
            ("calvin06", "c/calvin/calcom06.xml", "de96d1361801c31a76db343b05fe227664184aeefeb365b895d1ecf3e7592ad6"),
            ("calvin07", "c/calvin/calcom07.xml", "98657e5ee3b1564e7d16729a8fd4fc73b1f46439f02e750fdbe700488fc33879"),
            ("calvin08", "c/calvin/calcom08.xml", "d536c3aef54fbece4f8411ee9e76279333c97cd321ce1fc99241da17ea917586"),
            ("calvin09", "c/calvin/calcom09.xml", "ed4df1781f8f4fcc5c192adae0702a198f19176e2ae5e4790b34b5780971a591"),
            ("calvin10", "c/calvin/calcom10.xml", "7663f8e936be7b2f896a01e146ac30e03884f6edc04f3fc65d2b97bb51f99070"),
            ("calvin11", "c/calvin/calcom11.xml", "ba8b446e8df7599db0e8088704f5c108fab17a873f34df75f7449eb79b13d6ea"),
            ("calvin12", "c/calvin/calcom12.xml", "53e9f7cb53092c67c71ed3f6b0bf6f625f0fcdc4b4f4272327c8939fb9e4b3de"),
            ("calvin13", "c/calvin/calcom13.xml", "f87ca5809cf9d52d8a4dd90bca1453254f8d6518a1668f7af1418865cfd80043"),
            ("calvin14", "c/calvin/calcom14.xml", "d4875806cb10179dd4ec51d38260c8d85150ac3272c38916858b06c25905c00d"),
            ("calvin15", "c/calvin/calcom15.xml", "5470801c8e4f73adb79bc425d586298c79ec45ddb1f4ee69bebff0b2163a76dc"),
            ("calvin16", "c/calvin/calcom16.xml", "14f5e0b5fb890e04a18d0907e3d9303d3bc7a5f91bc6958d13ee7fbe5dcb683c"),
            ("calvin17", "c/calvin/calcom17.xml", "798e2868501737dbad1257ada4cc88415384bd0513dc89f5c3bd662108435b78"),
            ("calvin18", "c/calvin/calcom18.xml", "2c7989b0bef3b1d9b5a8d5c977eb409d1ba7f515643f4f01a52a7bc0bb3dd5f9"),
            ("calvin19", "c/calvin/calcom19.xml", "bdde519e98338ce70f1ebf26efc3040e57b716ef15ecb88af529095df0ae6249"),
            ("calvin20", "c/calvin/calcom20.xml", "1fb1279732e1ec3820a9458094b74074c4146c8bb0f72ad4b775fd9cad1a3b00"),
            ("calvin21", "c/calvin/calcom21.xml", "2cf559a316f8dd267805ea332e66c62300a45baf5c579bb105cd1ecc6fa8727b"),
            ("calvin22", "c/calvin/calcom22.xml", "e1f87bee30d0c44206811f55508b83e30df6b4738c665c3e3e473646bcd4a8a0"),
            ("calvin23", "c/calvin/calcom23.xml", "545b547bdaea2b48492da3530a4e369806c20dc734d13691014cac24e44970e9"),
            ("calvin24", "c/calvin/calcom24.xml", "852e065780ef1969630ce55d7310c8df1029ab4e303d3b7efbf05626b84a2496"),
            ("calvin25", "c/calvin/calcom25.xml", "a0d0e8a8afc1027bbd960a5ee6a6dfbefee08a5cb60fbcc74b1a1780bb0041e0"),
            ("calvin26", "c/calvin/calcom26.xml", "fa11e0f55eb5228fb048abc3a79c93c03d877604274bf7a137ed68149dcb4ee5"),
            ("calvin27", "c/calvin/calcom27.xml", "706711217a3b7e0bf3698bf855f5675371e41faf82bd6369874ff5051c94c171"),
            ("calvin28", "c/calvin/calcom28.xml", "b88752f77e187112a3f920aa82e9aaa125f32765a9843daf3c94290f3dd44a67"),
            ("calvin29", "c/calvin/calcom29.xml", "11295fba3e70f79968a46a1a499e7daef96d51e20552a517f1ae919d630d2054"),
            ("calvin30", "c/calvin/calcom30.xml", "90e826641081bd15d455a799da7f60574d4394d884de75d6f351ade0d1763ab8"),
            ("calvin31", "c/calvin/calcom31.xml", "4989da59aa4b29fd076d95bae451def22de137db54bd7c52eb070f544913b428"),
            ("calvin32", "c/calvin/calcom32.xml", "a6a0045ee9a75603a35142bdcfa2fdeac79a9d867ea32b1e16cbc47a8c0d6681"),
            ("calvin33", "c/calvin/calcom33.xml", "28cecf1fe7cdf9837f6760f8febb9bea5cee08ead5950596fa4dac1dfb4a98af"),
            ("calvin34", "c/calvin/calcom34.xml", "69f6362ccb18d6e09c8c4aae165179b8dc4838ae19b268b3a3787fb6ed37c39a"),
            ("calvin35", "c/calvin/calcom35.xml", "d4681c28a63055fa04fcd4883f8f9acf0e2614086bdfe40c0fd303bf26ddd035"),
            ("calvin36", "c/calvin/calcom36.xml", "b48725d5eb77240b1bc4e5918d7141387811e9e2916e19f210a3cc75e6886af1"),
            ("calvin37", "c/calvin/calcom37.xml", "a1ca28543d1700c301dfb9e72e9fa8646febd1575e76ae0bc91ddb95a871bf34"),
            ("calvin38", "c/calvin/calcom38.xml", "83f148d977bb0e02928d209dd4cb2b19ebea440dd9c5e85fe3e73131fb53289c"),
            ("calvin39", "c/calvin/calcom39.xml", "176ef9aa57b3973664dcf65d4ca12c1b7b319e51e8df7c270d237d6ad1aed012"),
            ("calvin40", "c/calvin/calcom40.xml", "62b7b8c27c058d259cc4dc63564970ead43d516beeb9225b83a01c6d02fa1db2"),
            ("calvin41", "c/calvin/calcom41.xml", "fac8c754eb4291391a28e94f9e285c40f9a5dfc43326f63a3438f65f9aa9aefd"),
            ("calvin42", "c/calvin/calcom42.xml", "51096062bcf518040d5384f2597331b6e96dece4d0aaf2e5dda64c262dd921d2"),
            ("calvin43", "c/calvin/calcom43.xml", "b5cdb241085c0eea44aa29388d88a53d2940ee0910cd43c39182f4a0c581528b"),
            ("calvin44", "c/calvin/calcom44.xml", "b3bc9df38e418bc26ec525e01e9a4f59a41ca0b8f9c52ede49d880f0eac59827"),
            ("calvin45", "c/calvin/calcom45.xml", "61ee8f73bf8a3f274bdf599c20631874a1070d489edf9fd659d572bfb20b1d1f")],
        "drop_notes": True,         # the translators' footnotes are the editors', not Calvin's
        "scans": [],
    },
    "hodge": {
        "title": "A Commentary on the Epistle to the Ephesians",
        "author": "Charles Hodge (1797-1878)",
        "files": [("hodge-ephesians", "h/hodge/ephesians.xml", "a25226498c8646bb3b062d0b3e58ccbea7ed9f4b14a04ef9b3728757301c21dc")],
        "verse_head": True,         # "V. 2. Contains the usual apostolic benediction"
        "comma": True,              # "Heb. 13, 9"
        "scans": [],
    },
    "manton": {
        "title": "A Practical Commentary, or an Exposition with Notes on the Epistles of James and Jude",
        "author": "Thomas Manton (1620-1677)",
        "files": [("manton04", "m/manton/manton04.xml", "2755b7879c26e006e4238d5b23784d5a815e3f4baa9dab5177742a1f556188b3"),
                  ("manton05", "m/manton/manton05.xml", "435d3dba30709b6ed959fd9367116cff3e24d5821b2f31ab5390834ae3a2eb77")],
        "verse_head": True,         # "Ver. 2. My brethren, count it all joy"
        "scans": [],
    },
    "trapp": {
        "kind": "tcp-verse",
        "title": "A Commentary or Exposition upon ... (five volumes of the first editions)",
        "author": "John Trapp (1601-1669)",
        # (file, url, sha256, the books its commentary divisions hold, in order)
        "files": [
            ("trapp-A63067", TCP + "A63067/master/A63067.xml", "63d2f9a9e54439cce653aa8e3bac1bc5a6f622ef0d4fd74321dd8d02d7957c1f"),
            ("trapp-A63065", TCP + "A63065/master/A63065.xml", "440b7caa1fc282bccd576ad0559dd29ac2fe6d788dcce7d9fbbf00756834dcf0"),
            ("trapp-A63066", TCP + "A63066/master/A63066.xml", "8899d8ef3b1af3be79b96feba3a19857f2c485854e98ab5e5789f22d0e991d4f"),
            ("trapp-A63068", TCP + "A63068/master/A63068.xml", "1433f8113cb45b34400e1effacb259cdc15ff4789993ddff9348699457cab69b"),
            ("trapp-A63069", TCP + "A63069/master/A63069.xml", "0622c547e10058daae32da35e8cedef3e9cd5cc5e8eecf8c65315b8973248744"),
        ],
        "books": {
            "trapp-A63067": "Matt Mark Luke",
            "trapp-A63065": "Rom 1Cor 2Cor Gal Eph Phil Col 1Thess 2Thess 1Tim 2Tim Titus Phlm Heb Jas 1Pet 2Pet 1John 2John 3John Jude Rev",
            "trapp-A63066": "Ezra Neh Esth Job Ps",
            "trapp-A63068": "Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal",
            "trapp-A63069": "Prov Eccl Song Isa Jer Lam Ezek Dan",
        },
        "scans": [],
    },
    "clarke": {
        "kind": "scan",
        "title": "The Holy Bible ... with a Commentary and Critical Notes",
        "author": "Adam Clarke (1760?-1832)",
        "files": [],
        "scans": [],
        # two printings of each Testament; (archive.org id, sha256 of its OCR, first book, last book, bare heads)
        "testaments": [
            ("Old Testament", [
                ("New York: G. Lane & P. P. Sandford, 1843, four volumes", [
                    ("holybiblecontai01clar", "60e08d6933e937eac95bfeb74d25d1fc61be7450a5e257a242fbe93f23288071", "Gen", "Deut", False),
                    ("holybiblecontai02clar", "aea6d2bdda8180c511590d0a09d0626ce237c44ef651457e3d96a7641e42c654", "Josh", "Esth", False),
                    ("holybiblecontai03clar", "5015e2244eca20e1662f57ec8e7e10236015f64f1bf189d47728eed565433d3e", "Job", "Song", False),
                    ("holybiblecontai04clar", "f9c1b82d279c7ce60017c3505777b15b5a7ee2274e0c5173c0df0be98ebaf602", "Isa", "Mal", False)]),
                ("New York: G. Lane & C. B. Tippett, 1846, four volumes", [
                    ("holybiblecontain184601clar", "3b4897ca1f376c4424834051d3b0db912b9418066f46ee0dce38b17b3d6772f0", "Gen", "Deut", False),
                    ("holybiblecontai184602clar", "a15b62dcb0b05d48fd9fd7b96dd498c2d4c9713de45437f5db7c8b38a2fdc994", "Josh", "Esth", False),
                    ("holybiblecontai184603clar", "2eda5c108dd51938657a1b3ec1c0061c5a856b4f9d9a9e6a60fd61816d769f3b", "Job", "Song", False),
                    ("holybiblecontain184604clar", "d328ce5cc6469ca85306948d758d9c74bd9475bd2ce2f4a9cd6fd3efa1aec956", "Isa", "Mal", False)]),
            ]),
            ("New Testament", [
                ("New York: G. Lane & C. B. Tippett, 1846, two volumes", [
                    ("newtestamentofou01clar", "9c3f5f4207ef5f3ca8b5588561425bc10a3a835461f16e57d69153b58ff3bb18", "Matt", "Acts", False),
                    ("newtestamentofo02clar", "3fd1c33abe18d1727af8d7f1018ae15bf1fb4b96e449e4c7549ecc8b065e3fbe", "Rom", "Rev", False)]),
                ("New York: P. D. Myers, 1835, one volume", [
                    ("newtestamentofou00clar", "1e719f547663439a17079e35fa360e5ad3a0fe9988a2d86a8d0bdc64ec21531d", "Matt", "Rev", True)]),
            ]),
        ],
    },
    "spurgeon": {
        "kind": "scan",
        "reader": "spurgeon",
        "title": "The Treasury of David (the Exposition)",
        "author": "C. H. Spurgeon (1834-1892)",
        "edition": "archive.org OCR of two printings (London and New York)",
        "files": [],
        "scans": [],
        # two printings; (archive.org id, sha256 of its OCR, first psalm, last psalm, unused)
        "testaments": [
            ("Psalms", [
                ("London: Marshall Brothers, six volumes", [
                    ("thetreasuryofdav01spuruoft", "38d558e4d70a4bf6d903114f85a49a4e82091728eca06a903aa99aa65ceed6d8", 1, 26, False),
                    ("thetreasuryofdav02spuruoft", "913881bd61b061876a10a9c3ea2568c0eec1ef7e6b3b19ffb3514d9ec3fefd9b", 27, 57, False),
                    ("thetreasuryofdav03spuruoft", "99e6a259c619971ee1ca4bdf8c82cc6aba378fd229a600651d7c9cae3627cb46", 58, 87, False),
                    ("treasuryofdavid04spuruoft", "a1e2108006f8f0f2aed78681934b27fad10ab41ccde4af0b9f8746463c8472b9", 88, 110, False),
                    ("thetreasuryofdav00spuruoft", "77747209b100cbbc55699dcda810797672df60d6df81e70902005c487f06f921", 111, 119, False),
                    ("treasuryofdavid06spuruoft", "be4272ba2a15637655748f6bf06c0e20b7a75ec9deba7de1ba27b6a33f3e880f", 120, 150, False)]),
                ("New York: Funk & Wagnalls, seven volumes", [
                    ("treasuryofdavid0001chsp", "c96158a94e65d2e427d1e13afa9739f50e29e5a72d574abefa47129214b05161", 1, 26, False),
                    ("treasuryofdavidc0002spur", "bed622796127c5bd9e445206bb12be8ef70541741f99c70b68ee566a3f667a9b", 27, 52, False),
                    ("treasuryofdavidc0000spur", "4e1bb0d6da9eafe326f756c5e64ca476d43ddb4eeb797088848027417c4bd4d8", 53, 78, False),
                    ("treasuryofdavidv0004unse", "082bf25ee943056fe0506b70a5cbdf00d9e4a4d84905733701950ee62010078f", 79, 103, False),
                    ("treasuryofdavidc0005spur", "fa06a48a8b185040837e9121cc861e9389233363701d6b0bfd73428232fac0ab", 104, 118, False),
                    ("treasuryofdavidc0006spur", "72b9095c9d4b0585c40522953c5a3a4bfeec3a433b39786ba7abb24542245e7f", 119, 124, False),
                    ("treasuryofdavidc0007spur", "c179791fd17e58fc5e4ad5a4a06509b50bf49a94da9db4af0652c447b017cc88", 125, 150, False)]),
            ]),
        ],
    },
}

RIGHTS = {
    "license": "public-domain",
    "basis": "Henry 1706-21, Jamieson-Fausset-Brown 1871, Barnes 1832-53, Poole 1683-85, Wesley 1755-66, Hodge 1856,"
             " Manton 1651-58 (Nisbet 1871), Calvin in the"
             " Calvin Translation Society's English 1843-55, Clarke 1810-26 (read from archive.org scans of the 1835-46"
             " New York printings), Spurgeon's Treasury of David 1869-85 (read from archive.org scans of the London"
             " and New York printings); every author and translator died before 1931."
             " Poole's transcription is EEBO-TCP's (Phase I), CC0 1.0",
    "committed": "which verses each comment is on and which verses it cites; the prose stays in build/",
    "redistribute_whole": True,
}

_FULL = {"Genesis": "Gen", "Exodus": "Exod", "Leviticus": "Lev", "Numbers": "Num", "Deuteronomy": "Deut",
         "Joshua": "Josh", "Judges": "Judg", "Ruth": "Ruth", "Ezra": "Ezra", "Nehemiah": "Neh", "Esther": "Esth",
         "Job": "Job", "Psalms": "Ps", "Proverbs": "Prov", "Ecclesiastes": "Eccl", "Song of Solomon": "Song",
         "Isaiah": "Isa", "Jeremiah": "Jer", "Lamentations": "Lam", "Ezekiel": "Ezek", "Daniel": "Dan",
         "Hosea": "Hos", "Joel": "Joel", "Amos": "Amos", "Obadiah": "Obad", "Jonah": "Jonah", "Micah": "Mic",
         "Nahum": "Nah", "Habakkuk": "Hab", "Zephaniah": "Zeph", "Haggai": "Hag", "Zechariah": "Zech",
         "Malachi": "Mal", "Matthew": "Matt", "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts",
         "Romans": "Rom", "Galatians": "Gal", "Ephesians": "Eph", "Philippians": "Phil", "Colossians": "Col",
         "Titus": "Titus", "Philemon": "Phlm", "Hebrews": "Heb", "James": "Jas", "Jude": "Jude",
         "Revelation": "Rev"}
for _n, _o in (("Samuel", "Sam"), ("Kings", "Kgs"), ("Chronicles", "Chr"), ("Corinthians", "Cor"),
               ("Thessalonians", "Thess"), ("Timothy", "Tim"), ("Peter", "Pet"), ("John", "John")):
    for _i, _w in ((1, "1"), (2, "2"), (3, "3")):
        _FULL[f"{_w} {_n}"] = f"{_i}{_o}"
        _FULL[f"{['', 'First', 'Second', 'Third'][_i]} {_n}"] = f"{_i}{_o}"
_FULL["Acts of the Apostles"] = "Acts"


KJV_TXT = os.path.join(ROOT, "data", "corpus", "kjv_bible.txt")
KJV_SHA = "0204adaed1f25700aa854218cae63c7172228c41088f335e99167a071eed83c0"


def path(name):
    return os.path.join(CORPUS, name + ".xml")


def fetch():
    for w, d in WORKS.items():
        for name, rel, want in d["files"]:
            BT._get(rel if rel.startswith("https:") else CCEL + rel, path(name), want)
        for _, idents in d["scans"]:
            for ident, want in idents:
                BT._get(f"{IA}{ident}/{ident}_djvu.txt", scan_path(ident), want)
        for _, printings in d.get("testaments", []):
            for _, vols in printings:
                for ident, want, *_ in vols:
                    BT._get(f"{IA}{ident}/{ident}_djvu.txt", scan_path(ident), want)


def verify():
    for w, d in WORKS.items():
        for name, rel, want in d["files"]:
            p = path(name)
            if not os.path.exists(p):
                raise SystemExit(f"{p} missing: run build_commentary.py --fetch")
            if BT.sha(p) != want:
                raise SystemExit(f"HARD STOP: {p} changed upstream (sha256 mismatch)")
        for _, printings in d.get("testaments", []):
            for _, vols in printings:
                for ident, want, *_ in vols:
                    p = scan_path(ident)
                    if not os.path.exists(p):
                        raise SystemExit(f"{p} missing: run build_commentary.py --fetch")
                    if BT.sha(p) != want:
                        raise SystemExit(f"HARD STOP: {p} changed upstream (sha256 mismatch)")
    if any(d.get("kind") == "scan" for d in WORKS.values()):
        if not os.path.exists(KJV_TXT) or BT.sha(KJV_TXT) != KJV_SHA:
            raise SystemExit(f"{KJV_TXT} missing or changed: run fetch_sources.py (Project Gutenberg 10)")


def print_source(s):
    """CCEL's printSourceInfo, and whether a person must look (a year >= 1930)."""
    m = re.search(r"<printSourceInfo>(.*?)</printSourceInfo>", s[:40000], re.S)
    src = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip() if m else None
    years = [int(y) for y in re.findall(r"(?<!\d)(1[5-9]\d\d|20\d\d)(?!\d)", src or "")]
    rights = [x.strip() for x in re.findall(r"<DC\.Rights[^>]*>(.*?)</DC\.Rights>", s[:40000], re.S) if x.strip()]
    return {"ccel_print_source": src, "ccel_print_source_check": bool(years) and max(years) >= 1930,
            "ccel_dc_rights": " / ".join(rights) or None}


# ---------------------------------------------------------------- comments
_EVENT = re.compile(r"<scripCom\b([^>]*)/?>|<div(\d)\b([^>]*)>")
_ATTR = re.compile(r'(\w+)="([^"]*)"')
_DROP = re.compile(r"<h\d\b[^>]*>.*?</h\d>|<p\b[^>]*class=\"(?:Center|t8|passage)\"[^>]*>.*?</p>", re.S)
_VERSE_HEAD = re.compile(r"\s*(?:Verses?|Vers|Ver|Vv|V)\.?\s*(\d{1,3})(?:\s*[,\-\u2013]\s*(\d{1,3}))?\.")
_NOTE = re.compile(r"<note\b.*?</note>", re.S)
_WESLEY_V = re.compile(r"<p\b[^>]*>\s*(\d{1,3})(?:\s*[,\-\u2013]\s*(\d{1,3}))?\.\s+")
_PASSAGE = re.compile(r"<p\b[^>]*class=\"passage\"[^>]*>(.*?)</p>", re.S)


def comments(s, work):
    """[{"anchor": (b, c, v, c2, v2), "raw": html, "title": div title, "chapter": n or None}]"""
    body = s[s.find("<ThML.body"):]
    out = []
    cur = None
    title = chapter = None

    def close():
        if cur and cur["anchor"] and R.plain(_DROP.sub("", cur["raw"])):
            out.append(cur)

    pos = 0
    for m in _EVENT.finditer(body):
        if cur is not None:
            cur["raw"] += body[pos:m.start()]
        pos = m.end()
        if m.group(2):                                   # a division starts
            a = dict(_ATTR.findall(m.group(3)))
            if (WORKS.get(work, {}).get("split_verses") and cur is not None and cur["anchor"]
                    and re.match(r"(?:Introduction to|Commentary on) Chapter", a.get("title", ""))):
                continue                                 # Wesley's OT: a chapter's parts, after its mark
            close()
            title = a.get("title", "")
            cm = re.match(r"(?:Chapter|CHAPTER|Psalm) (\d+)$", title)
            if cm:
                chapter = int(cm.group(1))
            elif m.group(2) in ("1", "2"):
                chapter = None
            cur = {"anchor": None, "raw": "", "title": title, "chapter": chapter}
            continue
        a = dict(_ATTR.findall(m.group(1)))
        q = R.osis_parts(re.sub(r"^Bible[^:]*:", "", a.get("osisRef", "")).split(" ")[0])
        if q is None:
            continue
        substantive = cur is not None and R.plain(_DROP.sub("", cur["raw"]))
        if cur is None:
            cur = {"anchor": q, "raw": "", "title": title, "chapter": chapter}
        elif cur["anchor"] is None:
            cur["anchor"] = q
            if substantive and q[2] is None:             # a chapter's introduction, before its mark
                close()
                cur = {"anchor": q, "raw": "", "title": title, "chapter": chapter}
        elif not substantive:
            old = cur["anchor"]
            # keep the more precise of two marks on one place (Barnes: verse, then chapter)
            if not (q[2] is None and old[2] is not None and old[:2] == q[:2]):
                cur["anchor"] = q
        else:
            close()
            cur = {"anchor": q, "raw": "", "title": title, "chapter": chapter}
    if cur is not None:
        cur["raw"] += body[pos:]
        close()
    return out


def second_reading(c, work):
    """Where the comment's own text says it is, (b, c, v, c2, v2) or None."""
    b, ch = c["anchor"][0], c["anchor"][1]
    if work == "henry":
        nums = []
        for p in _PASSAGE.findall(c["raw"]):
            nums += [int(x) for x in re.findall(r"(?:^|\s)(\d{1,3})\s(?=[A-Z(])", R.plain(p))]
        if not nums:
            return None
        return (b, ch, nums[0], ch, nums[-1])
    if work == "jfb":
        m = re.search(r"<b>\s*(\d{1,3})\.", c["raw"])
        if not m or c["chapter"] is None:
            return None
        return (b, c["chapter"], int(m.group(1)), c["chapter"], int(m.group(1)))
    if work == "calvin":           # "<b>12.</b> <i>And Jesus entered</i>", in the mark's chapter
        m = re.search(r"<b>\s*(\d{1,3})\.", _NOTE.sub("", c["raw"]))
        if not m or c["anchor"][2] is None:
            return None
        return (b, ch, int(m.group(1)), ch, int(m.group(1)))
    if WORKS[work].get("verse_head"):     # "Ver. 2." / "V. 2." opening the comment, in the mark's chapter
        m = _VERSE_HEAD.match(R.plain(_DROP.sub("", c["raw"])))
        if not m or c["anchor"][2] is None:
            return None
        v = int(m.group(1))
        return (b, ch, v, ch, int(m.group(2)) if m.group(2) else v)
    if work == "barnes":
        m = re.match(r"(.+?) (\d+):(\d+)$", c["title"] or "")
        if not m or m.group(1) not in _FULL:
            return None
        return (_FULL[m.group(1)], int(m.group(2)), int(m.group(3)), int(m.group(2)), int(m.group(3)))
    return None


def anchor_check(c, work):
    s = second_reading(c, work)
    if s is None:
        return "unread"
    a = c["anchor"]
    if a[2] is None:
        return "unread"
    if work in ("jfb", "calvin"):          # a lemma opens the comment on its first verse
        return "agrees" if s[:3] == a[:3] else "differs"
    return "agrees" if (s[0], s[1], s[2], s[4]) == (a[0], a[1], a[2], a[4] if a[4] is not None else a[2]) else "differs"


def body(c, work):
    """The comment's own markup: headings dropped, and the translators' footnotes where they are the editors'."""
    raw = _DROP.sub("", c["raw"])
    return _NOTE.sub(" ", raw) if WORKS[work].get("drop_notes") else raw


_KJV = {}


def kjv_words(shape):
    if "k" not in _KJV:
        import structure_texts as S
        _KJV["k"] = CR.Kjv({u["id"]: u["text"] for u in S.convert_kjv(KJV_TXT)["units"]}, shape)
    return _KJV["k"]


def split_verses(c, shape):
    """Wesley: CCEL marks only the chapter, and each note opens with its verse
    number ("5. And he opened his mouth - A phrase ..."). One comment per note;
    the text before the first number is the chapter's introduction. The second
    reading of each place is its lemma (the words before " - "), looked for in
    the KJV verse it names."""
    b, ch = c["anchor"][0], c["anchor"][1]
    if c["anchor"][2] is not None or ch is None or b not in shape or ch not in shape[b]:
        return [dict(c, check="unread")]
    ms = list(_WESLEY_V.finditer(c["raw"]))
    out = []
    head = c["raw"][:ms[0].start()] if ms else c["raw"]
    if R.plain(_DROP.sub("", head)):
        out.append(dict(c, raw=head, check="unread"))
    kjv = kjv_words(shape)
    for i, m in enumerate(ms):
        raw = c["raw"][m.start():ms[i + 1].start() if i + 1 < len(ms) else len(c["raw"])]
        v, v2 = int(m.group(1)), int(m.group(2)) if m.group(2) else None
        lemma = R.plain(raw[m.end() - m.start():]).split(" - ")[0][:160]
        if CR.words(lemma) and len(CR.words(lemma)) >= 2 and 1 <= v <= shape[b][ch]:
            here = kjv.sim(lemma, b, ch, v)
            best = max(range(1, shape[b][ch] + 1), key=lambda x: (kjv.sim(lemma, b, ch, x), -abs(x - v)))
            check = "agrees" if here >= CR.NEED else ("differs" if kjv.sim(lemma, b, ch, best) >= here + 0.5 else "unread")
        else:
            check = "unread"
        out.append(dict(c, raw=raw, anchor=(b, ch, v, ch, v2 if v2 and v2 > v else v), check=check))
    return out


def cites(c, work):
    """The comment's citations as candidates (the same vote as build_topical)."""
    raw = body(c, work)
    tags = []
    for m in re.finditer(r"<scripRef\b([^>]*)>", raw):
        o = dict(_ATTR.findall(m.group(1))).get("osisRef", "")
        tags.append({"osis": re.sub(r"^Bible[^:]*:", "", o)})
    para = {"text": R.plain(raw), "tagged": tags, "roman_comma": WORKS[work].get("roman_comma", False),
            "comma": WORKS[work].get("comma", False)}
    return BT.candidates(para, here=c["anchor"][:2])


def build_work(work, shape):
    d = WORKS[work]
    rows, prose, rejected = [], [], []
    counts = collections.Counter()
    sources = []
    items = []                      # (comment, on, anchor check, [candidates])
    for name, rel, want in d["files"]:
        with open(path(name), encoding="utf-8") as f:
            s = f.read()
        ps = print_source(s)
        sources.append({"file": name, "url": CCEL + rel, "sha256": want, **ps})
        cs = comments(s, work)
        if d.get("split_verses"):
            cs = [x for c in cs for x in split_verses(c, shape)]
        for c in cs:
            on, why = BT.kjv_id(c["anchor"], shape, BT.APOCRYPHA)
            if on is None:
                counts["anchor names no KJV verse"] += 1
                rejected.append({"anchor": list(c["anchor"]), "why": why, "text": R.plain(c["raw"])[:300]})
                continue
            items.append((c, on, c["check"] if "check" in c else anchor_check(c, work), cites(c, work)))

    # print: a citation that names its own book and chapter (not "ver. 3",
    # which only the comment's place resolves) is looked for in each printing,
    # aligned in order; the printings' references are read with no context.
    seq, where = [], []
    for k, (c, on, ac, cands) in enumerate(items):
        for j, x in enumerate(cands):
            if x["t"][0] != "?" and x["t"][:2] != c["anchor"][:2] and c["anchor"][0] in d.get("print_books", c["anchor"][:1]):
                seq.append("%s %s %s" % x["t"][:3])
                where.append((k, j))
    printed = collections.Counter()
    scan_stats = []
    for printing, idents in d["scans"]:
        text = ""
        for ident, _ in idents:
            with open(scan_path(ident), encoding="utf-8", errors="replace") as f:
                text += f.read() + "\n"
        # print has no comment place to lend "ch. xi. 4" a book, so only the
        # citations that name one are read there; a key without its book
        # repeats too often for diff to align (and is slow to try)
        srefs = ["%s %s %s" % (r["book"], r["c"], r["v"]) for r in R.refs(text, point=True)]
        m = BT.aligned(seq, srefs)
        for i in m:
            printed[where[i]] += 1
        scan_stats.append({"printing": printing, "scans": [i for i, _ in idents], "refs_read": len(srefs),
                           "aligned": len(m)})
    explicit = {w for w in where}

    seen = collections.Counter()
    by_class = collections.defaultdict(lambda: [0, 0])
    for k, (c, on, ac, cands) in enumerate(items):
        counts["anchor " + ac] += 1
        got, shown = [], set()
        for j, x in enumerate(cands):
            cls = "both" if x["ccel"] and x["reader"] else ("ccel-only" if x["ccel"] else "reader-only")
            counts["cite " + cls] += 1
            if (k, j) in explicit:
                by_class[cls][0] += 1
                by_class[cls][1] += bool(printed[(k, j)])
            if not (cls == "both" or printed[(k, j)]):
                rejected.append({"anchor": list(c["anchor"]), "ref": list(x["t"]), "class": cls,
                                 "text": R.plain(c["raw"])[:300]})
                continue
            rid, why = BT.kjv_id(x["t"], shape, BT.APOCRYPHA)
            if rid is None:
                counts["cite names no KJV verse" if why != "apocrypha" else "cite apocrypha"] += 1
                continue
            if printed[(k, j)]:
                shown.add(rid)
            if rid not in got:
                got.append(rid)
        base = on[4:]
        seen[base] += 1
        uid = f"{work}:{base}" if seen[base] == 1 else f"{work}:{base}~{seen[base]}"
        row = {"id": uid, "on": on, "anchor": ac, "cites": got}
        if d["scans"] and c["anchor"][0] in d.get("print_books", c["anchor"][:1]):
            row["in_print"] = len(shown)
        rows.append(row)
        counts["comments"] += 1
        counts["citations"] += len(got)
        prose.append({"id": uid, "text": R.plain(body(c, work))})
    V = T.Verses(shape)
    covered = set()
    for r in rows:
        b, c, v, c2, v2 = T.parse_ref_id(r["on"])
        covered.update(range(V.index[(b, c, v)], V.index[(b, c2, v2)] + 1))
    counts["verses_covered"] = len(covered)
    measure = {cls: {"refs": n, "printed": p, "share_printed": round(p / n, 4) if n else None}
               for cls, (n, p) in sorted(by_class.items())}
    return rows, prose, rejected, dict(sorted(counts.items())), sources, measure, scan_stats


# ---------------------------------------------------------------- Poole (EEBO-TCP)
# The 1683/85 folio prints the KJV text with its verse numbers inline ("2. And
# the Earth", "33 And every"), Poole's notes at the foot keyed to a word of
# the verse (<note place="bottom">), and the parallel places in the margin
# (<note place="margin">). TCP keyed it by hand from the page images and
# marks what it could not read (<gap>), never guessing.
NS = "{http://www.tei-c.org/ns/1.0}"
# a note's place in the text; a page TCP's images lack; a verse number
_TCP_EV = re.compile(r"\x00(\d+)\x00|\x01|(?<![\w〉◊,.:;\-\x00])(\d{1,3})[.,▪]?(?=\s*[^\s\d.,▪])")
_GAP = " \u25ca "            # an unread word, letter or Greek: never read across


def tcp_flat(e):
    """A note's text: a gap is a mark nothing is read across; an end-of-line hyphen joins."""
    out = []

    def go(x, top=False):
        tag = x.tag[len(NS):]
        if tag == "gap":
            out.append(_GAP)
        elif tag == "g" and x.get("ref") == "char:EOLhyphen":
            pass
        elif tag == "note" and not top:
            pass
        else:
            if x.text:
                out.append(x.text)
            for c in x:
                go(c)
                out.append(c.tail or "")
    go(e, True)
    return " ".join("".join(out).split())


def _tcp_stream(e, out):
    tag = e.tag[len(NS):]
    if tag == "note":
        out.append(("note", e))
        return
    if tag == "gap":
        out.append(("missing" if e.get("reason") == "missing" else "t", _GAP))
        return
    if tag == "head":
        return
    if not (tag == "g" and e.get("ref") == "char:EOLhyphen") and e.text:
        out.append(("t", e.text))
    for c in e:
        _tcp_stream(c, out)
        if c.tail:
            out.append(("t", c.tail))


def tcp_chapter(b, c, el, n_verses, counts):
    """One chapter -> [(verse, {"notes": [...], "margin": [...]})], and how its
    verse numbers read: "agrees" (2..N in order), "by order" (a misprinted
    number between two right ones, read as the one between), "differs"."""
    seg = []
    _tcp_stream(el, seg)
    notes, parts = [], []
    for k, x in seg:
        if k == "note":
            parts.append(" \x00%d\x00 " % len(notes))
            notes.append(x)
        elif k == "missing":
            parts.append(" \x01 ")
        else:
            parts.append(x)
    ev = list(_TCP_EV.finditer("".join(parts)))
    nums = {i: int(m.group(2)) for i, m in enumerate(ev) if m.group(2)}
    keys = sorted(nums)
    fixed = 0
    for a, i, z in zip(keys, keys[1:], keys[2:]):          # Exod 29 prints 36 twice: the second is 37
        if nums[a] + 2 == nums[z] and nums[i] != nums[a] + 1 and 1 < nums[a] + 1 <= n_verses:
            nums[i] = nums[a] + 1
            fixed += 1
    cur, seen, dead = 1, [1], False
    com = {}
    for i, m in enumerate(ev):
        if m.group(0) == "\x01":                           # pages missing from the images: the rest is unplaced
            dead = True
            counts["chapters with pages missing"] += 1
            continue
        if m.group(1) is not None:
            x = notes[int(m.group(1))]
            if dead:
                counts["notes after missing pages, dropped"] += 1
                continue
            com.setdefault(cur, {"notes": [], "margin": []})["margin" if x.get("place") == "margin" else "notes"].append(tcp_flat(x))
            continue
        if dead:
            continue
        n = nums[i]
        if cur < n <= min(cur + 3, n_verses):
            cur = n
            seen.append(n)
    counts["verse numbers misprinted, read by order"] += fixed
    full = seen == list(range(1, n_verses + 1))
    return sorted(com.items()), ("by order" if fixed else "agrees") if full and not dead else "differs"


def tcp_books(work):
    """The book divisions, in canonical order, of every volume."""
    import xml.etree.ElementTree as ET
    out = []
    for name, _, _ in WORKS[work]["files"]:
        root = ET.parse(path(name)).getroot()
        for d in root.find(".//" + NS + "text").iter(NS + "div"):
            if d.get("type") in ("book", "biblical_commentary"):
                out.append(d)
    return out


def tcp_header(name):
    with open(path(name), encoding="utf-8") as f:
        head = f.read(20000)
    date = re.search(r"<edition>\s*<date>([^<]+)</date>", head)
    cc0 = "publicdomain/zero/1.0" in head
    pd = re.search(r"<availability>.*?\bPublic Domain\b", head, re.S)
    return {"edition_date": date.group(1) if date else None,
            "tcp_licence": "CC0 1.0" if cc0 else "public domain (TCP availability statement)" if pd else "check"}


def build_tcp_work(work, shape):
    """Poole: one comment per verse that has a note. One reading of each
    citation (the transcription is hand-keyed, double-checked by TCP; there is
    no second text): committed when it names a KJV verse and no unread word
    touches it."""
    d = WORKS[work]
    order = list(shape)
    books = tcp_books(work)
    if len(books) != len(order):
        raise SystemExit(f"{work}: {len(books)} book divisions, not {len(order)}")
    rows, prose, rejected = [], [], []
    counts = collections.Counter()
    sources = [{"file": n, "url": u, "sha256": w, **tcp_header(n)} for n, u, w in d["files"]]
    for b, div in zip(order, books):
        chs = [x for x in div.iter(NS + "div") if x.get("type") in ("chapter", "Psalm")] or [div]
        ns = [int(x.get("n") or 1) for x in chs]
        for i in range(1, len(ns) - 1):        # Psalm 45 is headed "PSAL. LXV.": read by its order
            if ns[i] != ns[i - 1] + 1 and ns[i - 1] + 2 == ns[i + 1]:
                ns[i] = ns[i - 1] + 1
                counts["chapter numbers misprinted, read by order"] += 1
        for x, c in zip(chs, ns):
            if c not in shape[b]:
                counts["chapter names no KJV chapter"] += 1
                continue
            verses, ac = tcp_chapter(b, c, x, shape[b][c], counts)
            counts["chapters " + ac] += 1
            for v, got in verses:
                cites, pars = [], []
                for kind, dest in (("notes", cites), ("margin", pars)):
                    for t in got[kind]:
                        for r in R.refs(t, here=(b, c), point=True, old=True):
                            if "\u25ca" in t[max(0, r["at"] - 2):r["at"] + 18]:
                                counts["cite next to an unread word, dropped"] += 1
                                rejected.append({"on": [b, c, v], "ref": [r["book"], r["c"], r["v"]], "why": "unread word",
                                                 "text": t[max(0, r["at"] - 40):r["at"] + 40]})
                                continue
                            rid, why = BT.kjv_id((r["book"], r["c"], r["v"], r["c2"], r["v2"]), shape, BT.APOCRYPHA)
                            if rid is None:
                                counts["cite apocrypha" if why == "apocrypha" else "cite names no KJV verse"] += 1
                                if why != "apocrypha":
                                    rejected.append({"on": [b, c, v], "ref": [r["book"], r["c"], r["v"]], "why": why,
                                                     "text": t[max(0, r["at"] - 40):r["at"] + 40]})
                                continue
                            if rid not in dest:
                                dest.append(rid)
                on = "kjv:%s.%d.%d" % (b, c, v)
                row = {"id": f"{work}:{on[4:]}", "on": on, "anchor": ac, "cites": cites, "parallels": pars}
                rows.append(row)
                counts["comments"] += 1
                counts["notes"] += len(got["notes"])
                counts["citations"] += len(cites)
                counts["parallels"] += len(pars)
                counts["unread words in the notes"] += sum(t.count("\u25ca") for t in got["notes"] + got["margin"])
                prose.append({"id": row["id"], "notes": got["notes"], "margin": got["margin"]})
    counts["verses_covered"] = len(rows)
    return rows, prose, rejected, dict(sorted(counts.items())), sources, None, []


# ---------------------------------------------------------------- Trapp (EEBO-TCP)
# Trapp's commentaries (1647-60) are hand-keyed by TCP from the first
# editions. Unlike Poole's folio they do not print the Bible text: each note
# opens a paragraph with its verse and lemma ("Verse 3. Concerning his Son]
# Here's a lofty ..."), and his sources and parallels stand in the margin.
# So a note's place is read twice: the printed verse number, and its lemma
# looked for in the KJV verse the number names (spelling levelled: long s,
# u/v, i/j, a final e). A citation is read once, as Poole's are, and
# committed when it names a KJV verse and no unread word touches it.
_TRAPP_V = re.compile(r"(?:\x02|\bCHAP\.?\s*[IVXLC1l]+\s*\.)\s*(?:Verses?|Vers|Ver|V)\s*\.?\s*(\d{1,3})(?:\s*[,\-]\s*(\d{1,3}))?\s*[.,:]")


def _trapp_stream(e, out):
    tag = e.tag[len(NS):]
    if tag == "note":
        out.append(("note", e))
        return
    if tag == "gap":
        out.append(("t", _GAP))
        return
    if tag in ("p", "head", "l", "lg"):
        out.append(("t", " \x02 "))
    if not (tag == "g" and e.get("ref") == "char:EOLhyphen") and e.text:
        out.append(("t", e.text))
    for c in e:
        _trapp_stream(c, out)
        if c.tail:
            out.append(("t", c.tail))


def _level(w):
    return w.replace("\u017f", "s").replace("v", "u").replace("j", "i").rstrip("e")


def trapp_chapter(b, c, el, kjv, counts):
    """One chapter -> [(verse, last verse, check, notes text, [margin texts])]."""
    seg = []
    _trapp_stream(el, seg)
    notes, parts = [], []
    for k, x in seg:
        if k == "note":
            parts.append(" \x00%d\x00 " % len(notes))
            notes.append(x)
        else:
            parts.append(x)
    text = "".join(parts).replace("\u017f", "s")
    n_verses = kjv.shape[b][c]
    marks = []
    cur = 0
    for m in _TRAPP_V.finditer(text):
        v = int(m.group(1))
        if cur < v <= n_verses:
            marks.append((m, v, int(m.group(2)) if m.group(2) and int(m.group(2)) > v else v))
            cur = v
        elif v == cur:
            counts["a verse head repeated, read as one"] += 1
        else:
            counts["verse heads out of order, not read"] += 1
    out = []
    lev = {}
    for i, (m, v, v2) in enumerate(marks):
        body = text[m.end():marks[i + 1][0].start() if i + 1 < len(marks) else len(text)]
        lemma = re.split(r"\]", body.replace("\x02", " "), 1)[0][:200]
        lw = [_level(w) for w in CR.words(re.sub(r"\x00\d+\x00", " ", lemma))]
        if len(lw) >= 2 and "]" in body[:400]:
            if v not in lev:
                lev[v] = {_level(w) for w in kjv.verse_words(b, c, v)}
            here = sum(w in lev[v] for w in lw) / len(lw)
            check = "agrees" if here >= CR.NEED else "unread"
            if check == "unread":
                for x in range(1, n_verses + 1):
                    if x != v:
                        lev.setdefault(x, {_level(w) for w in kjv.verse_words(b, c, x)})
                        if sum(w in lev[x] for w in lw) / len(lw) >= here + 0.5:
                            check = "differs"
                            break
        else:
            check = "unread"
        margin = [tcp_flat(notes[int(k)]).replace("\u017f", "s") for k in re.findall(r"\x00(\d+)\x00", body)]
        prose = " ".join(re.sub(r"\x00\d+\x00", " ", body).replace("\x02", "\n").split(" "))
        out.append((v, v2, check, " ".join(prose.split()), margin))
    return out


def build_trapp_work(work, shape):
    import xml.etree.ElementTree as ET
    d = WORKS[work]
    kjv = kjv_words(shape)
    rows, prose, rejected, sources = [], [], [], []
    counts = collections.Counter()
    seen = collections.Counter()
    for name, url, want in d["files"]:
        sources.append({"file": name, "url": url, "sha256": want, **tcp_header(name)})
        root = ET.parse(path(name)).getroot()
        divs = [x for x in root.find(".//" + NS + "text").iter(NS + "div") if x.get("type") == "commentary"]
        books = d["books"][name].split()
        if len(divs) != len(books):
            raise SystemExit(f"{name}: {len(divs)} commentary divisions, not {len(books)}")
        for b, div in zip(books, divs):
            chs = [x for x in div if x.tag == NS + "div" and x.get("type") in ("chapter", "Psalm")]
            if not chs:
                chs, ns = [div], [1]
            else:
                ns = [int(x.get("n")) if (x.get("n") or "").isdigit() else None for x in chs]
            for x, c in zip(chs, ns):
                if c is None or c not in shape[b]:
                    counts["chapter names no KJV chapter"] += 1
                    continue
                counts["chapters"] += 1
                for v, v2, check, text, margin in trapp_chapter(b, c, x, kjv, counts):
                    cites, pars = [], []
                    for kind, dest, ts in (("notes", cites, [text]), ("margin", pars, margin)):
                        for t in ts:
                            for r in R.refs(t, here=(b, c), point=True, old=True):
                                if "\u25ca" in t[max(0, r["at"] - 2):r["at"] + 18]:
                                    counts["cite next to an unread word, dropped"] += 1
                                    continue
                                rid, why = BT.kjv_id((r["book"], r["c"], r["v"], r["c2"], r["v2"]), shape, BT.APOCRYPHA)
                                if rid is None:
                                    counts["cite apocrypha" if why == "apocrypha" else "cite names no KJV verse"] += 1
                                    if why != "apocrypha":
                                        rejected.append({"on": [b, c, v], "ref": [r["book"], r["c"], r["v"]], "why": why,
                                                         "text": t[max(0, r["at"] - 40):r["at"] + 40]})
                                    continue
                                if rid not in dest:
                                    dest.append(rid)
                    on = "kjv:%s.%d.%d" % (b, c, v) + ("-%d" % v2 if v2 != v else "")
                    seen[on] += 1
                    uid = f"{work}:{on[4:]}" if seen[on] == 1 else f"{work}:{on[4:]}~{seen[on]}"
                    rows.append({"id": uid, "on": on, "anchor": check, "cites": cites, "parallels": pars})
                    counts["comments"] += 1
                    counts["anchor " + check] += 1
                    counts["citations"] += len(cites)
                    counts["parallels"] += len(pars)
                    prose.append({"id": uid, "text": text, "margin": margin})
    counts["verses_covered"] = len({r["on"] for r in rows})
    return rows, prose, rejected, dict(sorted(counts.items())), sources, None, []


def _scan_volume(d, t, b0, b1, bare, kjv, V, counts, label):
    """One scanned volume's comments: [(book, chapter, verse, last verse, text, [refs])], by the work's reader."""
    out = []
    if d.get("reader") == "spurgeon":
        got, vc = SR.read_volume(t, b0, b1, kjv, V.seq)
        for k, v in vc.items():
            counts[f"{label}: {k}"] += v
        for (c, v), g in got.items():
            out.append(("Ps", c, v, g["last"] if g["last"] > v else None, g["text"], SR.citations(g["text"], c)))
        return out
    hs, vc = CR.read_volume(t, b0, b1, kjv, V.seq, bare)
    for k, v in vc.items():
        counts[f"{label}: {k}"] += v
    for i, h in enumerate(hs):
        if not h["placed"]:
            continue
        b, c = h["chapter"]
        txt, dropped = CR.note_text(t, hs, i, kjv)
        for k, v in dropped.items():
            counts[f"paragraphs dropped: {k}"] += v
        out.append((b, c, h["n"], h["n2"], txt, CR.citations(txt, b, c)))
    return out


def build_scan_work(work, shape):
    """Clarke: both readings from scans (clarke_read.py). A note is placed in
    each of two printings of its Testament; a row is written for every verse
    either printing places, and says which (`anchor`: both printings / one
    printing). A citation is committed only when both printings read it in
    their notes on the same verse."""
    d = WORKS[work]
    kjv = kjv_words(shape)
    V = T.Verses(shape)
    rows, prose, rejected, sources = [], [], [], []
    counts = collections.Counter()
    for testament, printings in d["testaments"]:
        read = []
        for label, vols in printings:
            got = collections.OrderedDict()
            for ident, want, b0, b1, bare in vols:
                sources.append({"testament": testament, "printing": label, "scan": ident,
                                "url": f"{IA}{ident}/{ident}_djvu.txt", "sha256": want})
                with open(scan_path(ident), encoding="utf-8", errors="replace") as f:
                    t = f.read()
                for b, c, n, n2, txt, refs in _scan_volume(d, t, b0, b1, bare, kjv, V, counts, f"{testament}, {label}"):
                    g = got.setdefault((b, c, n), {"n2": set(), "cites": [], "text": []})
                    g["n2"].add(n2)
                    g["text"].append(txt)
                    h = {"n": n}
                    for r in refs:
                        rid, why = BT.kjv_id(r, shape, BT.APOCRYPHA)
                        if rid is None:
                            counts["cite apocrypha" if why == "apocrypha" else "cite names no KJV verse"] += 1
                            continue
                        if rid == "kjv:%s.%d.%d" % (b, c, h["n"]):
                            counts["cite of the note's own verse, not kept"] += 1
                            continue
                        if rid not in g["cites"]:
                            g["cites"].append(rid)
            read.append((label, got))
        (la, a), (lb, b_) = read
        for key in sorted(set(a) | set(b_), key=lambda k: V.index[k]):
            b, c, v = key
            both = key in a and key in b_
            first = a.get(key) or b_[key]
            n2 = first["n2"] if not both else first["n2"] & b_[key]["n2"]
            n2 = max((x for x in n2 if x), default=None)
            on = "kjv:%s.%d.%d" % key
            if n2 and v < n2 <= shape[b][c]:
                on += "-%d" % n2
            if both:
                cites = [x for x in a[key]["cites"] if x in b_[key]["cites"]]
                for lab, mine, other in ((la, a[key], b_[key]), (lb, b_[key], a[key])):
                    for x in mine["cites"]:
                        if x not in other["cites"]:
                            counts["cites one printing reads, not committed"] += 1
                            rejected.append({"on": on, "ref": x, "why": "read in one printing only", "printing": lab})
            else:
                cites = []
                for x in first["cites"]:
                    counts["cites one printing reads, not committed"] += 1
                    rejected.append({"on": on, "ref": x, "why": "the note is placed in one printing only",
                                     "printing": la if key in a else lb})
            row = {"id": f"{work}:{on[4:]}", "on": on, "anchor": "both printings" if both else "one printing",
                   "cites": cites}
            rows.append(row)
            counts["comments"] += 1
            counts["comments placed in both printings" if both else "comments placed in one printing"] += 1
            counts["citations"] += len(cites)
            prose.append({"id": row["id"], "printing": la if key in a else lb,
                          "text": "\n\n".join(first["text"]), "ocr": "unproofread"})
    counts["verses_covered"] = len(rows)
    return rows, prose, rejected, dict(sorted(counts.items())), sources, None, []


def treasury_measure(rows, shape):
    """An outside check: the share of a work's citations that the Treasury
    (data/xrefs/tsk.jsonl, read from its own 1830s scans) also lists at the
    same verse, against the share at an unrelated verse (the verse 1,000 on).
    A measure only: nothing is kept or dropped by it."""
    p = os.path.join(ROOT, "data", "xrefs", "tsk.jsonl")
    if not os.path.exists(p):
        return None
    V = T.Verses(shape)

    def verses(rid):
        b, c, v, c2, v2 = T.parse_ref_id(rid)
        return range(V.index[(b, c, v)], V.index[(b, c2, v2)] + 1)
    tsk = {}
    with open(p, encoding="utf-8") as f:
        for raw in f:
            r = json.loads(raw)
            tsk[r["verse"]] = {k for g in r["groups"] for x in g["refs"] for k in verses(x)}
    out = {}
    for kind in ("cites", "parallels"):
        n = hit = base = 0
        for r in rows:
            if kind not in r:
                continue
            on = [V.seq[k] for k in verses(r["on"])]       # a comment on a passage: the Treasury on any verse of it
            mine = set().union(*(tsk.get("kjv:%s.%d.%d" % x, set()) for x in on))
            other = set().union(*(tsk.get("kjv:%s.%d.%d" % V.seq[(V.index[x] + 1000) % len(V.seq)], set()) for x in on))
            if not mine:
                continue
            for x in r[kind]:
                vs = set(verses(x))
                n += 1
                hit += bool(vs & mine)
                base += bool(vs & other)
        if n:
            out[kind] = {"refs": n, "in_treasury_at_that_verse": round(hit / n, 4),
                         "in_treasury_at_an_unrelated_verse": round(base / n, 4)}
    return out


def scan_path(ident):
    return os.path.join(CORPUS, "scans", ident + ".txt")


def build(write=True):
    verify()
    shape = T.kjv_shape()
    files, layers = {}, {}
    for w, d in WORKS.items():
        print(f"{w}: reading")
        if d.get("kind") == "tcp":
            rows, prose, rejected, counts, sources, measure, scans = build_tcp_work(w, shape)
        elif d.get("kind") == "scan":
            rows, prose, rejected, counts, sources, measure, scans = build_scan_work(w, shape)
        elif d.get("kind") == "tcp-verse":
            rows, prose, rejected, counts, sources, measure, scans = build_trapp_work(w, shape)
        else:
            rows, prose, rejected, counts, sources, measure, scans = build_work(w, shape)
        files[f"{w}.jsonl"] = BT.dumps(rows)
        layers[w] = {"file": f"data/commentary/{w}.jsonl",
                     "sha256": hashlib.sha256(files[f"{w}.jsonl"].encode()).hexdigest(),
                     "rows": len(rows), "counts": counts,
                     "explicit_citations_by_reading": measure, "print_check": scans,
                     "treasury_check": treasury_measure(rows, shape),
                     "source": {"title": d["title"], "author": d["author"],
                                "edition": d.get("edition") or {"tcp": "EEBO-TCP TEI (hand-keyed from the first edition)",
                                            "tcp-verse": "EEBO-TCP TEI (hand-keyed from the first editions)",
                                            "scan": "archive.org OCR of two printings of each Testament"}.get(d.get("kind"), "CCEL ThML"),
                                "files": sources}}
        print(f"  {counts}")
        if write:
            os.makedirs(BUILD, exist_ok=True)
            for name, data in ((f"{w}.rejected.jsonl", rejected), (f"{w}.text.jsonl", prose)):
                tmp = os.path.join(BUILD, name + ".tmp")
                with open(tmp, "w", encoding="utf-8") as f:
                    f.write(BT.dumps(data))
                os.replace(tmp, os.path.join(BUILD, name))
    manifest = {"about": "Whole-Bible commentaries keyed to KJV verse ids. pipeline/build_commentary.py; rules in pipeline/README-commentary.md",
                "rights": RIGHTS, "layers": layers}
    files["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    if write:
        os.makedirs(OUT, exist_ok=True)
        for name, data in files.items():
            tmp = os.path.join(OUT, name + ".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(data)
            os.replace(tmp, os.path.join(OUT, name))
        print("wrote " + ", ".join(f"data/commentary/{n}" for n in files))
    return files


# ---------------------------------------------------------------- collation
# Is CCEL's wording the period wording? A fixed sample of comments is found
# in each work's scans (a four-word run that occurs once there) and its next
# 80 words are aligned with the scan's. What differs is counted: the old
# forms print has where CCEL has another word, and -our / -or spellings.
ARCHAIC = {"hath", "doth", "saith", "spake", "shew", "shewed", "shewn", "unto", "toward", "afterward",
           "exceeding", "ye", "thee", "thou", "thy", "hast", "dost", "whilst", "amongst", "betwixt", "viz"}


def collate(work, n=400):
    import difflib
    import random
    d = WORKS[work]
    words = lambda t: [w.lower() for w in re.findall(r"[A-Za-z]+", t)]
    out = {}
    for printing, idents in d["scans"]:
        sc = []
        for ident, _ in idents:
            with open(scan_path(ident), encoding="utf-8", errors="replace") as f:
                sc += words(f.read())
        idx = collections.defaultdict(list)
        for i in range(len(sc) - 3):
            idx[" ".join(sc[i:i + 4])].append(i)
        rows = []
        with open(os.path.join(BUILD, work + ".text.jsonl"), encoding="utf-8") as f:
            for raw in f:
                r = json.loads(raw)
                if r["id"].split(":")[1].split(".")[0] in d.get("print_books", {r["id"].split(":")[1].split(".")[0]}):
                    if len(words(r["text"])) > 120:
                        rows.append(r)
        rnd = random.Random(1)
        sample = rnd.sample(rows, min(n, len(rows)))
        found = tot = same = 0
        old_new, kept, spell = collections.Counter(), collections.Counter(), collections.Counter()
        for r in sample:
            cw = words(r["text"])
            hit = next(((k, idx[g][0]) for k in range(20, len(cw) - 80, 7)
                        for g in [" ".join(cw[k:k + 4])] if len(idx.get(g, ())) == 1), None)
            if not hit:
                continue
            a, b = cw[hit[0]:hit[0] + 80], sc[hit[1]:hit[1] + 90]
            sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
            m = sum(x.size for x in sm.get_matching_blocks())
            if m < 50:
                continue
            found += 1
            tot += len(a)
            same += m
            for op, a1, a2, b1, b2 in sm.get_opcodes():
                if op == "equal":
                    kept.update(w for w in a[a1:a2] if w in ARCHAIC)
                elif op == "replace" and a2 - a1 == 1 and b2 - b1 == 1:
                    x, y = a[a1], b[b1]
                    if y in ARCHAIC and x != y:
                        old_new[f"{y} -> {x}"] += 1
                    if x.replace("our", "or") == y and x != y:
                        spell["CCEL -our, print -or"] += 1
                    if y.replace("our", "or") == x and x != y:
                        spell["CCEL -or, print -our"] += 1
        out[printing] = {"sampled": len(sample), "located": found, "word_agreement": round(same / tot, 4) if tot else None,
                         "print_old_form_ccel_other": dict(old_new.most_common(12)),
                         "old_forms_kept": dict(kept.most_common(8)), "spelling": dict(spell)}
    return out


def collate_all():
    res = {w: collate(w) for w, d in WORKS.items() if d["scans"]}
    p = os.path.join(OUT, "collation.json")
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    os.replace(tmp, p)
    print(json.dumps(res, indent=1))


def check():
    files = build(write=False)
    bad = [n for n, data in files.items()
           if not os.path.exists(os.path.join(OUT, n)) or open(os.path.join(OUT, n), encoding="utf-8").read() != data]
    if bad:
        raise SystemExit("check: differs: " + ", ".join(bad))
    print("check: byte-identical")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--collate", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    elif a.collate:
        collate_all()
    elif a.check:
        check()
    else:
        build()


if __name__ == "__main__":
    main()
