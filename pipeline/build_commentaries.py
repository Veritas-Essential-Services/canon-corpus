#!/usr/bin/env python3
"""
build_commentaries.py -- six public-domain commentaries and lectures, shelved
as drafts, keyed where they can be by the verse they comment on.

    python3 pipeline/build_commentaries.py --fetch    # pinned sources -> data/corpus/commentaries/ (gitignored, ~170 MB)
    python3 pipeline/build_commentaries.py            # build data/books/<slug>.json + manifest entries
    python3 pipeline/build_commentaries.py --check    # rebuild in memory: = the committed manifest entries
    python3 pipeline/build_commentaries.py --report   # per-book measures, writes nothing
    python3 tests/commentaries_test.py

THE BOOKS, AND WHICH PRINTING (every one printed before 1929: US public domain)

  lightfoot-galatians     J. B. Lightfoot, St Paul's Epistle to the Galatians,
                          10th ed. (1890), the Macmillan reprint of 1910.
                          Internet Archive saintpaulsepistl00lighrich (UC copy).
  lightfoot-philippians   J. B. Lightfoot, St Paul's Epistle to the Philippians,
                          3rd ed. (Macmillan, 1873). stpaulsepistleto00lighuoft (Toronto copy).
  lightfoot-colossians    J. B. Lightfoot, St Paul's Epistles to the Colossians
                          and to Philemon (Macmillan, 1875, the first edition):
                          Project Gutenberg #50857, a proofread transcription.
  westcott-hebrews        B. F. Westcott, The Epistle to the Hebrews, 2nd ed.
                          (Macmillan, 1892). epistletohebrew00westgoog (Harvard copy).
  westcott-john           B. F. Westcott, The Epistles of St John, 3rd ed.
                          (Macmillan, 1892). cu31924074296629 (Cornell copy).
  hort-ante-nicene        F. J. A. Hort, Six Lectures on the Ante-Nicene Fathers
                          (Macmillan, 1895). sixlecturesonant00hortrich (UC copy): by page,
                          each page carrying its lecture (`lecture`).

  Wave 2a (2026-10-03), the same machinery, scan sets of several volumes allowed
  (`volumes`: page ids then lead with the volume, `v2.leaf.15`):
  westcott-gospel-john    B. F. Westcott, The Gospel according to St John: the Greek
                          text with introduction and notes (London: Murray, 1908, 2 vols).
                          gospelaccordingt01west (Princeton), gospelaccordingt02west (Toronto).
  lightfoot-horae         John Lightfoot (1602-1675), Horae Hebraicae et Talmudicae, ed.
                          R. Gandell (Oxford, 1859, 4 vols): Matthew to 1 Corinthians, notes
                          headed "Ver. 5:" in one column. horaehebraicaeet000{1-4}ligh (the
                          Internet Archive's own scans: the only copies whose OCR kept Hebrew).
  ellicott-galatians      C. J. Ellicott, St Paul's Epistle to the Galatians, 4th ed.
                          (Longmans, 1867). stpaulsepistleto00elli (Princeton).
  ellicott-ephesians      C. J. Ellicott, St Paul's Epistle to the Ephesians, 5th ed.
                          (Longmans, 1884). cu31924029294240 (Cornell).
  ellicott-philippians    C. J. Ellicott, Philippians, Colossians and Philemon (Parker,
                          1857, the first edition). criticalgrammati00elli (Princeton).
  ellicott-thessalonians  C. J. Ellicott, St Paul's Epistles to the Thessalonians, 4th ed.
                          (Longmans, 1880). cu31924029294539 (Cornell).
  ellicott-pastorals      C. J. Ellicott, The Pastoral Epistles of St Paul, 5th ed.
                          (Longmans, 1883). pastoralepistles00elli (Princeton).

Project Gutenberg has only the Colossians (searched 2026-10-03 by author and
title); its Greek is real Unicode and its markup gives the verse anchors of
Lightfoot's Greek text and every note paragraph, so that book is exact. The
other five are read from the Internet Archive's OCR (hOCR, word boxes),
chosen by measuring every candidate scan's text layer (the comment above
CANDIDATES lists the numbers): the other Toronto scans of Lightfoot (and the 1879
Colossians) have NO Greek codepoints at all, every Greek word turned into
Latin letters, as Thayer's and Abbott-Smith's scans were; the John scan from
Toronto was OCR'd as Greek throughout, its English unreadable. The scans
chosen keep the notes' Greek as Greek.

THE CITATION SPINE. A commentary is cited by the verse it comments on. On a
commentary page the epistle's text stands at the top in large type and the
notes run below in two columns; a note on a new verse opens an indented
paragraph with the verse number ("6. οὕτως ταχέως] ..."), a paraphrase of a
run of verses with the run ("6—9. ..."), and every other note opens with its
lemma alone. So each indented number is a candidate verse opener, and it is
accepted only if the sequence allows it: the same chapter at or after the
current verse (within the KJV's verse count and a bounded gap), or the next
chapter's first verses where the page's running head (OCR, read fuzzily) or
the end of the chapter says so. An accepted opener starts (or continues) the
unit `<slug>:<chapter>.<verse>` (`lightfoot-galatians:2.20`; a run is
`1.6-9`; in a volume of several epistles the book leads: `westcott-john:
2John.1.6`, `lightfoot-colossians:Phlm.1.4-7`), and every line after it,
in reading order (left column, then right), belongs to it until the next
accepted opener. A rejected candidate stays in the text where it stands and
is counted. Each note unit links to the KJV verse(s) it comments on
(`type: comments-on`). Notes before the first opener are the unit `title`.

What a commentary page holds besides the notes is kept, never dropped: the
epistle's text block (and, in Westcott, the critical apparatus printed under
it) is the unit `leaf.N.text`; a single-column passage that begins on a
commentary page after the notes (a detached note) is the page unit `leaf.N`.
Every page that is not laid out in note columns (introductions, detached
notes, Westcott's additional notes, dissertations, essays, index) is a page
unit, `leaf.N` (the scan leaf, as the Charles books), the printed folio in
`scan.printed_page` where the running head gives it (or its neighbours do:
`scan.printed_page_from`). Lines the OCR made of accents alone (the
diacritics of the large Greek type, read as a line of their own) are
dropped and counted.

The Colossians from Gutenberg: notes by the same rule, but read off the
transcription's paragraphs and its verse anchors (no OCR, no guessing of
chapters: a note's verse number is matched to the latest Greek verse anchor
with that number). Lightfoot's Greek text is kept per verse
(`text.Col.1.3`), the introduction, dissertations and index by printed page
(`p.17`, the transcription marks every page break), footnotes on the unit
whose text carries their reference mark (`notes`), marginal summaries in
`sidenotes`.

SCRIPTURE. Every unit's English references ("Rom. ix. 16", "1 Cor. i. 1")
are read by fathers_scripture.parse (the same reader as the fathers' English
editors) and resolved in the KJV's own numbering, which these English
editors use; a reference to a verse the KJV lacks, to a whole chapter, or to
a book outside the KJV stays `resolved: false` with its reason. "ver. 8"
and "vv. 8, 9" in a note mean the verse of the same chapter, and Westcott's
"c. x. 11" the same epistle (`rule: self/...`).

HONESTY. The five scanned books are unproofread OCR and every honesty field
says so; their notes' boundaries rest on verse numbers read off the page and
checked only against the sequence. Nothing is minted: ids are citations.
"""
import argparse
import collections
import hashlib
import html
import json
import os
import re
import statistics as st
import sys
import unicodedata
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import charles_ocr as C  # noqa: E402
import fathers_scripture as FS  # noqa: E402

BOOKS_DIR = os.path.join(ROOT, "data", "books")
MANIFEST = os.path.join(BOOKS_DIR, "manifest.json")
CACHE = os.path.join(ROOT, "data", "corpus", "commentaries")
UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")
STRONGS = os.path.join(ROOT, "data", "strongs", "strongs.jsonl")
NT_JOHN = os.path.join(ROOT, "data", "nt", "John", "passages.jsonl")

# The candidate scans, measured 2026-10-03 on each item's _djvu.txt: Greek
# letters as a share of all letters; Greek tokens (3+ letters) found among
# Strong's Greek lemmas, the forms of data/nt/John and the Greek of PG
# #50857; English tokens found in the dwyl word list (data/corpus/proof).
#   Galatians   saintpaulsepistl00lighrich 1910  6.8%  65.9%  92.6%   <- chosen (IA: NOT_IN_COPYRIGHT)
#               cu31924075537088 (a 1921 reprint) 6.8% 66.5% 92.7%
#               saintpaulepistle00lighuoft 1914, saintpaulsepistl00lighuoft 1890,
#               sa590770400lighuoft 1880, stpaulsepistleto00ligh 1870: 0.0% Greek
#   Philippians stpaulsepistleto00lighuoft 1873  7.3%  65.6%  92.4%   <- chosen
#               saintpaulsepistl00ligh 1878      7.3%  65.1%  92.1%
#               epistlephilippia00lighuoft 1903, a590773100lighuoft 1898: 0.0% Greek
#   Colossians  PG #50857 (1875)                11.5%  (transcribed)   93.3%   <- chosen
#               saintpaulsepistl00unknuoft 1879: 0.0% Greek, English 82.6%
#   Hebrews     epistletohebrew00westgoog 1892 13.6%  64.2%  88.9%   <- chosen
#               epistletohebrews0000broo_a4f0 1889: 0.0% Greek
#   John        cu31924074296629 1892           9.2%  74.0%  92.2%   <- chosen
#               epistlesstjohn00dclgoog 1892     9.2%  73.7%  92.2%
#               epistlesstjohng00westgoog 1886   9.0%  69.0%  91.7%
#               epistlesofstjohn00westuoft 1886, TheEpistlesOfStJohnTheGreekText:
#               ~100% Greek letters (the English OCR'd as Greek)
#   Hort        sixlecturesonant00hortrich 1895  (no Greek)  96.3%   <- chosen
#               sixlecturesonan00hortgoog 95.3%, sixlecturesonant00hortuoft 94.9%
# Wave 2a, measured 2026-10-03 the same way, except that the Greek column here
# is greek_measure()'s own yardstick (Strong's lemmas and data/nt/John only,
# the figure the manifest records), so it reads lower than the column above.
#   Westcott, John (Greek text, 1908)
#               gospelaccordingt01west vol. 1     7.3%  40.8%  94.5%   <- chosen (also Lane A's vol. 1)
#               gospelaccordingt02west vol. 2    10.3%  41.9%  93.5%   <- chosen
#               gospelaccordingt02west_0 (Lane A's vol. 2), gtu_32400003017666_2, gospelaccordingt0002broo,
#               bwb_S0-ASP-656_1, gospelaccordingt0001broo: 0.0% Greek
#               gospelaccording01westgoog vol. 1: 99.9% Greek letters (the English OCR'd as Greek)
#               The Authorised Version edition (gospelaccordingt00westuoft 1892, gospelaccording00westgoog 1882,
#               gospelaccording13unkngoog 1896) was not needed: the Greek-text edition kept its Greek.
#   Westcott, Ephesians (1906): REJECTED, no scan keeps its Greek. saintpaulsepistl00westuoft: 100% Greek
#               letters (English OCR'd as Greek); cu31924029294209, saintpaulsepistl0009broo, bwb_S0-BLY-035:
#               0.0% Greek; saintpaulsepistl0000west, saintpaulsepistl0000broo_v8b1: 1952 (Eerdmans) reprints.
#   Lightfoot, Horae Hebraicae (Gandell, 1859): Greek 2.4-3.4%, Hebrew letters
#               horaehebraicaeet000{1,2,3,4}ligh   Hebrew 2.0/2.3/1.9/1.5% of letters   <- chosen
#               (their Hebrew words 3+ letters: 23-26% a Strong's lemma, 44-47% with one prefix letter off)
#               horaehebraicaeet0{1,2,4}lighuoft, horaehebraicaeet00lighuoft (Toronto), horhebraicet0{1-4}ligh
#               (Princeton), horhebraicettal00gandgoog: no Hebrew codepoints; horhebraicet02ligh,
#               horhebraicettal00unkngoog: no Greek either; commentaryonnewt000*: 1979/1989 reprints.
#   Ellicott    Galatians stpaulsepistleto00elli 1867 (4th ed.) 10.7%  39.9%  87.4%   <- chosen
#               cu31924029294118 1867 10.7% 39.7%; criticalgrammat00elli 1854 11.0%; criticalgrammati59elli 1859;
#               criticalgrammel00elli 1867 (Boston); commentarycritic00elli 1860: 99.9% Greek letters;
#               acommentarycrit00elligoog, commentarycritic00ellirich/-iala 1860, acriticalandgra00elligoog 1859,
#               bwb_P9-DVB-553 1876: 0.0% Greek
#               Ephesians cu31924029294240 1884 (5th ed.)   11.6%  39.0%  86.2%   <- chosen
#               commentarycrit00elli 1863 (Andover) 11.0%; stpaulsepistletoephe00elli 1864,
#               stpaulsepistlet00elligoog 1868, stpaulsepistlet01elligoog 1884: 0.0% Greek;
#               acriticalandgra04elligoog 1855, stpaulsepistleto01elli 1868: ~100% Greek letters
#               Phil./Col./Philem. criticalgrammati00elli 1857 (1st ed.) 11.1%  39.7%  86.4%   <- chosen
#               criticalgramma00elli 1865 (Andover) 10.6%; cu31924029292856 1888, stpaulsepistles00elligoog
#               1865, criticalgrammati00elliuoft 1872: 0.0% Greek; acriticalandgra05elligoog: a 1998 reprint
#               Thessalonians cu31924029294539 1880 (4th ed.) 12.2%  41.5%  86.9%   <- chosen
#               stpaulsepistles00elliuoft 1866 12.3% 41.2%; acriticalandgra0{1,3,7}elligoog 1858,
#               stpaulsepistles0{1,2}elligoog 1866: 0.0% Greek
#               Pastorals pastoralepistles00elli 1883 (5th ed.)  12.3%  34.5%  85.3%   <- chosen
#               criticalgrammati1856elli 1856 12.7%; acriticalandgra06elligoog, pastorialepistl00elligoog
#               1865 (Andover); cu31924029294570 1883, pastoralepistles1869elli: ~100% Greek letters;
#               criticalgrammtic0000rtre: 0.0% Greek
#   Project Gutenberg has none of these (searched 2026-10-03: Westcott, Ellicott, Lightfoot).
CANDIDATES = None

GUTENBERG = {
    "lightfoot-colossians": {
        "pg": 50857,
        "url": "https://www.gutenberg.org/cache/epub/50857/pg50857-images.html",
        "file": "pg50857-images.html",
        "sha256": "5d62c4f3b025f31c71d724c26b143cebec11636983e9be797d9fcab090b688d3",
        "title": "St Paul's Epistles to the Colossians and to Philemon",
        "short": "Lightfoot, Col.",
        "author": "J. B. Lightfoot",
        "edition": ("J. B. Lightfoot, Saint Paul's Epistles to the Colossians and to Philemon: a revised "
                    "text with introductions, notes, and dissertations (London: Macmillan, 1875), the first "
                    "edition (title page as transcribed)"),
        "printed": 1875,
        "regions": {"ΠΡΟΣ ΚΟΛΑΣΣΑΕΙΣ": "Col", "ΠΡΟΣ ΦΙΛΗΜΟΝΑ": "Phlm"},
        "anchor": {"Col": re.compile(r'^(I|II|III|IV)_(\d+)$'), "Phlm": re.compile(r'^(ph)_(\d+)$')},
    },
}

SCANS = {
    "lightfoot-galatians": {
        "ia": "saintpaulsepistl00lighrich",
        "sha256": "fc65644766c7e56822907235645bcecfc878521f804f4c7870320057e05f282c",
        "title": "St Paul's Epistle to the Galatians",
        "short": "Lightfoot, Gal.",
        "author": "J. B. Lightfoot",
        "edition": ("J. B. Lightfoot, Saint Paul's Epistle to the Galatians: a revised text with introduction, "
                    "notes, and dissertations, 10th ed. (1890); this copy the reprint of 1910 (London: "
                    "Macmillan, 1910), as its title page and imprint read"),
        "printed": 1910,
        "copy": "University of California Libraries",
        "ia_rights": "NOT_IN_COPYRIGHT",
        "leaves": (8, 403),
        "epistles": [("Gal", 90, 244)],
        "apparatus": False,
    },
    "lightfoot-philippians": {
        "ia": "stpaulsepistleto00lighuoft",
        "sha256": "c7829cd1fd0666dbc339c4702c3e1b34165b573b83c4cf41b38a6407f5539d66",
        "title": "St Paul's Epistle to the Philippians",
        "short": "Lightfoot, Phil.",
        "author": "J. B. Lightfoot",
        "edition": ("J. B. Lightfoot, Saint Paul's Epistle to the Philippians: a revised text with "
                    "introduction, notes, and dissertations, 3rd ed. (London and Cambridge: Macmillan, 1873), "
                    "as its title page reads"),
        "printed": 1873,
        "copy": "University of Toronto (Robarts)",
        "ia_rights": "NOT_IN_COPYRIGHT",
        "leaves": (9, 362),
        "epistles": [("Phil", 95, 181)],
        "apparatus": False,
    },
    "westcott-hebrews": {
        "ia": "epistletohebrew00westgoog",
        "sha256": "2785db294c9077843e33c9305b30a8467fff12583f9c903675e8dcc22e0b33d3",
        "title": "The Epistle to the Hebrews",
        "short": "Westcott, Heb.",
        "author": "B. F. Westcott",
        "edition": ("B. F. Westcott, The Epistle to the Hebrews: the Greek text with notes and essays, 2nd ed. "
                    "(London and New York: Macmillan, 1892), as its title page reads (first ed. 1889)"),
        "printed": 1892,
        "copy": "Harvard University (Google scan)",
        "ia_rights": "NOT_IN_COPYRIGHT",
        "leaves": (9, 594),
        "epistles": [("Heb", 94, 542)],
        "apparatus": True,
    },
    "westcott-john": {
        "ia": "cu31924074296629",
        "sha256": "06dfd59ea42ff4aa504f0cc6089848ec92cf70da4f0fa909e5a1b6e9e6833134",
        "title": "The Epistles of St John",
        "short": "Westcott, Epp. John",
        "author": "B. F. Westcott",
        "edition": ("B. F. Westcott, The Epistles of St John: the Greek text with notes and essays, 3rd ed. "
                    "(Cambridge and London: Macmillan, 1892), as its title page reads (first ed. 1883)"),
        "printed": 1892,
        "copy": "Cornell University Library",
        "ia_rights": None,
        "leaves": (9, 441),
        "epistles": [("1John", 64, 281), ("2John", 284, 293), ("3John", 296, 306)],
        "apparatus": True,
    },
    "hort-ante-nicene": {
        "ia": "sixlecturesonant00hortrich",
        "sha256": "acffe34d110c2a486981e1510b618a7dd9b282181724e346de710e7cd31dfb93",
        "title": "Six Lectures on the Ante-Nicene Fathers",
        "short": "Hort, Ante-Nicene Fathers",
        "author": "F. J. A. Hort",
        "edition": ("F. J. A. Hort, Six Lectures on the Ante-Nicene Fathers (London and New York: Macmillan, "
                    "1895), as its title page reads; delivered 1890, published after his death by his son"),
        "printed": 1895,
        "copy": "University of California Libraries",
        "ia_rights": "NOT_IN_COPYRIGHT",
        "leaves": None,           # measured: the leaves that carry text, title page to the printer's imprint
        "epistles": [],
        "apparatus": False,
    },
}
# Wave 2a (2026-10-03). `volumes`: one book from several scans (page ids lead
# with the volume: v2.leaf.15); `head`: how the running head names the verse
# ("cu": Westcott's "[Cu. VII" on the left page, "Ver. 4-7]" on the right;
# "plain": Ellicott's "I. 20." with no bracket; "ch": Lightfoot's "[Ch. i. 23.");
# `style` "ver": notes in one column opened by "Ver. 5:" (the Horae); an
# epistle's fourth field is the chapter its notes resume at.
SCANS.update({
    "westcott-gospel-john": {
        "title": "The Gospel according to St John",
        "short": "Westcott, John",
        "author": "B. F. Westcott",
        "edition": ("B. F. Westcott, The Gospel according to St John: the Greek text with introduction and notes, "
                    "2 vols (London: John Murray, 1908), as the title pages read; published after his death"),
        "printed": 1908,
        "apparatus": True,
        "head": "cu",
        "lookahead": True,
        "honesty": ("the chapter is printed in the left page's running head only ('[Cu. VII'), the verses in "
                    "the right's ('Ver. 4-7]'); Westcott's additional notes after a chapter, where they are laid "
                    "out in columns, run into the note of the verse they open with; the pericope of the "
                    "adulteress (7.53-8.11), printed as an appendix to vol. 2, is by page only; "
                    "openers_against_running_head counts notes whose page head reads another chapter, "
                    "and notes_reopened the verses taken up again further on, whose text joins the first "
                    "unit of that verse"),
        "note": ("Lane A (branch claude/armarium-divines, pipeline/b-f-westcott_shelf.json) shelves the raw OCR of "
                 "gospelaccordingt01west (vol. 1, used here too), gospelaccordingt02west_0 (vol. 2) and "
                 "gospelaccordingt00westuoft (the 1892 Authorised Version edition) as westcott-john-greek-1/-2 "
                 "and westcott-john-av-1892; vol. 2 here is gospelaccordingt02west (Toronto) instead, because "
                 "gospelaccordingt02west_0's text layer has no Greek codepoints (0.0% of letters, measured "
                 "2026-10-03 on its _djvu.txt) against 10.3% here"),
        "volumes": [
            {"ia": "gospelaccordingt01west",
             "sha256": "ec341318718254bee14e7b664297519746defaf373a783b57128cdb29f04fc44",
             "copy": "Princeton Theological Seminary Library", "ia_rights": None,
             "leaves": (5, 483), "epistles": [("John", 202, 483)]},
            {"ia": "gospelaccordingt02west",
             "sha256": "9c921a390547f8350b9cf7fabfb33a46b33968ad0bec9ed79a455550376f9d75",
             "copy": "University of Toronto (Robarts)", "ia_rights": None,
             "leaves": (5, 404), "epistles": [("John", 12, 387, 8)]},
        ],
    },
    "lightfoot-horae": {
        "title": "Horae Hebraicae et Talmudicae",
        "short": "Lightfoot, Hor. Hebr.",
        "author": "John Lightfoot (1602-1675)",
        "edition": ("John Lightfoot, Horae Hebraicae et Talmudicae: Hebrew and Talmudical exercitations upon the "
                    "Gospels, the Acts, some chapters of St Paul's Epistle to the Romans, and the First Epistle to "
                    "the Corinthians, a new edition by Robert Gandell, 4 vols (Oxford: University Press, 1859); "
                    "the title pages print no date (Gandell's preface is dated 1 April 1859) and vol. 4 ends with "
                    "a Macmillan advertisement, so these copies may be a later issue of the 1859 sheets"),
        "printed": 1859,
        "apparatus": False,
        "head": "ch",
        "style": "ver",
        "note": ("the Internet Archive's own scans of the four volumes, chosen because their OCR kept the Hebrew "
                 "(about 2% of letters, real Hebrew codepoints); the Toronto (horaehebraicaeet0{1,2,4}lighuoft, "
                 "horaehebraicaeet00lighuoft) and Princeton (horhebraicet0{1-4}ligh) scans of the same edition "
                 "have no Hebrew codepoints at all; measured 2026-10-03 on each item's _djvu.txt; the raw-OCR "
                 "john-lightfoot shelf (branch claude/project-thread-c4l3cp) lists the Horae in Pitman's Whole "
                 "Works (1822-25) as pending, another edition, not shelved there"),
        "volumes": [
            {"ia": "horaehebraicaeet0001ligh",
             "sha256": "1ba4063fdbc1c09f0a721e4c489f77fe8534d5ecb1fb8c7fcf1b863fa81ef4d6",
             "copy": "Internet Archive scan", "ia_rights": None, "leaves": (5, 394), "epistles": []},
            {"ia": "horaehebraicaeet0002ligh",
             "sha256": "e54b581870ba3818113c255170311583fbae9fe887d3ce66a5d6f7e26e5adebb",
             "copy": "Internet Archive scan", "ia_rights": None, "leaves": (5, 486),
             "epistles": [("Matt", 13, 390), ("Mark", 399, 486)]},
            {"ia": "horaehebraicaeet0003ligh",
             "sha256": "8ffc3f7c8498da9a72af76b4e7c284a30474db48349cdcf2970dbbcc01a02e7c",
             "copy": "Internet Archive scan", "ia_rights": None, "leaves": (5, 462),
             "epistles": [("Luke", 11, 237), ("John", 243, 461)]},
            {"ia": "horaehebraicaeet0004ligh",
             "sha256": "d373363ad662c0e272c3e220015a793b7ee23c8e79a4e3d1cdb8be08d1e1d373",
             "copy": "Internet Archive scan", "ia_rights": None, "leaves": (5, 354),
             "epistles": [("Acts", 11, 159), ("Rom", 161, 170), ("1Cor", 177, 291)]},
        ],
    },
    "ellicott-galatians": {
        "ia": "stpaulsepistleto00elli",
        "sha256": "b8fe27d024d63d0d78ba12a90ddcffe5cd9aaed6b445a8b3116051bae40572a9",
        "title": "St Paul's Epistle to the Galatians",
        "short": "Ellicott, Gal.",
        "author": "C. J. Ellicott",
        "edition": ("C. J. Ellicott, St Paul's Epistle to the Galatians: with a critical and grammatical commentary, "
                    "and a revised translation, 4th ed., corrected (London: Longmans, Green, Reader, & Dyer, "
                    "1867), as its title page reads (first ed. 1854)"),
        "printed": 1867,
        "copy": "Princeton Theological Seminary Library",
        "ia_rights": "NOT_IN_COPYRIGHT",
        "leaves": (7, 205),
        "epistles": [("Gal", 37, 176)],
        "apparatus": False,
        "head": "plain",
        "prose_above": True,
        "lookahead": True,
        "honesty": ("Ellicott's textual notes, printed full width above the two columns, are read with the "
                    "notes (a textual note opening with its verse number opens that verse's unit); his revised "
                    "translation at the end of the volume is by page; openers_against_running_head counts notes "
                    "whose page head (rarely legible in these scans) reads another chapter, "
                    "and notes_reopened the verses taken up again further on, whose text joins the first "
                    "unit of that verse"),
    },
    "ellicott-ephesians": {
        "ia": "cu31924029294240",
        "sha256": "5acf89fdcb93b47401c7126f0d5097757b86b95fdaf9981214c6f96c82aa07ac",
        "title": "St Paul's Epistle to the Ephesians",
        "short": "Ellicott, Eph.",
        "author": "C. J. Ellicott",
        "edition": ("C. J. Ellicott, St Paul's Epistle to the Ephesians: with a critical and grammatical commentary, "
                    "and a revised translation, 5th ed., corrected (London: Longmans, Green & Co., 1884), as its "
                    "title page reads (first ed. 1855)"),
        "printed": 1884,
        "copy": "Cornell University Library",
        "ia_rights": None,
        "leaves": (6, 213),
        "epistles": [("Eph", 22, 181)],
        "apparatus": False,
        "head": "plain",
        "prose_above": True,
        "lookahead": True,
        "honesty": ("Ellicott's textual notes, printed full width above the two columns, are read with the "
                    "notes (a textual note opening with its verse number opens that verse's unit); his revised "
                    "translation at the end of the volume is by page; openers_against_running_head counts notes "
                    "whose page head (rarely legible in these scans) reads another chapter, "
                    "and notes_reopened the verses taken up again further on, whose text joins the first "
                    "unit of that verse"),
    },
    "ellicott-philippians": {
        "ia": "criticalgrammati00elli",
        "sha256": "d48f012284e787f2bd8bae2fbe09a5a466a5c15473117bf8d7dc040210b76f9d",
        "title": "St Paul's Epistles to the Philippians, the Colossians, and Philemon",
        "short": "Ellicott, Phil. Col. Philem.",
        "author": "C. J. Ellicott",
        "edition": ("C. J. Ellicott, A critical and grammatical commentary on St Paul's Epistles to the Philippians, "
                    "Colossians, and to Philemon, with a revised translation (London: John W. Parker and Son, "
                    "1857), the first edition, as its title page reads (MDCCCLVII)"),
        "printed": 1857,
        "copy": "Princeton Theological Seminary Library",
        "ia_rights": "NOT_IN_COPYRIGHT",
        "leaves": (7, 290),
        "epistles": [("Phil", 23, 127), ("Col", 131, 225), ("Phlm", 229, 244)],
        "apparatus": False,
        "head": "plain",
        "prose_above": True,
        "lookahead": True,
        "honesty": ("Ellicott's textual notes, printed full width above the two columns, are read with the "
                    "notes (a textual note opening with its verse number opens that verse's unit); his revised "
                    "translation at the end of the volume is by page; openers_against_running_head counts notes "
                    "whose page head (rarely legible in these scans) reads another chapter, "
                    "and notes_reopened the verses taken up again further on, whose text joins the first "
                    "unit of that verse"),
    },
    "ellicott-thessalonians": {
        "ia": "cu31924029294539",
        "sha256": "9d94507cc9e47f7a1019162cc6ae0a7845fd2e56d06798c04b084ee3a0b88d77",
        "title": "St Paul's Epistles to the Thessalonians",
        "short": "Ellicott, Thess.",
        "author": "C. J. Ellicott",
        "edition": ("C. J. Ellicott, St Paul's Epistles to the Thessalonians: with a critical and grammatical "
                    "commentary, and a revised translation, 4th ed. (London: Longman, Green, Longman, Roberts & "
                    "Green, 1880), as its title page reads (first ed. 1858)"),
        "printed": 1880,
        "copy": "Cornell University Library",
        "ia_rights": None,
        "leaves": (2, 184),
        "epistles": [("1Thess", 14, 105), ("2Thess", 110, 153)],
        "apparatus": False,
        "head": "plain",
        "prose_above": True,
        "lookahead": True,
        "honesty": ("Ellicott's textual notes, printed full width above the two columns, are read with the "
                    "notes (a textual note opening with its verse number opens that verse's unit); his revised "
                    "translation at the end of the volume is by page; openers_against_running_head counts notes "
                    "whose page head (rarely legible in these scans) reads another chapter, "
                    "and notes_reopened the verses taken up again further on, whose text joins the first "
                    "unit of that verse"),
    },
    "ellicott-pastorals": {
        "ia": "pastoralepistles00elli",
        "sha256": "f9140c24e65007ef2f80c3070b3fa20585913e13b898f91d215a18287154945e",
        "title": "The Pastoral Epistles of St Paul",
        "short": "Ellicott, Past.",
        "author": "C. J. Ellicott",
        "edition": ("C. J. Ellicott, The Pastoral Epistles of St Paul: with a critical and grammatical commentary, "
                    "and a revised translation, 5th ed., corrected (London: Longmans, Green & Co., 1883), as its "
                    "title page reads (first ed. 1856)"),
        "printed": 1883,
        "copy": "Princeton Theological Seminary Library",
        "ia_rights": "NOT_IN_COPYRIGHT",
        "leaves": (7, 290),
        "epistles": [("1Tim", 23, 130), ("2Tim", 135, 200), ("Titus", 205, 241)],
        "apparatus": False,
        "head": "plain",
        "prose_above": True,
        "lookahead": True,
        "honesty": ("Ellicott's textual notes, printed full width above the two columns, are read with the "
                    "notes (a textual note opening with its verse number opens that verse's unit); his revised "
                    "translation at the end of the volume is by page; openers_against_running_head counts notes "
                    "whose page head (rarely legible in these scans) reads another chapter, "
                    "and notes_reopened the verses taken up again further on, whose text joins the first "
                    "unit of that verse"),
    },
})
ORDER = ["lightfoot-galatians", "lightfoot-philippians", "lightfoot-colossians",
         "westcott-hebrews", "westcott-john", "hort-ante-nicene",
         "westcott-gospel-john", "lightfoot-horae", "ellicott-galatians", "ellicott-ephesians",
         "ellicott-philippians", "ellicott-thessalonians", "ellicott-pastorals"]
MULTI = {"lightfoot-colossians", "westcott-john",    # volumes of several epistles: ids lead with the book
         "lightfoot-horae", "ellicott-philippians", "ellicott-thessalonians", "ellicott-pastorals"}

# ------------------------------------------------------------------ files


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_atomic(path, data):
    with open(path + ".tmp", "wb") as f:
        f.write(data)
    os.replace(path + ".tmp", path)


def download(url, dest, sha):
    if os.path.exists(dest) and sha256_file(dest) == sha:
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "canon-corpus/commentaries"})
    with urllib.request.urlopen(req, timeout=600) as r, open(dest + ".tmp", "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    got = sha256_file(dest + ".tmp")
    if got != sha:
        os.remove(dest + ".tmp")
        raise SystemExit(f"{url}: sha256 {got} != pinned {sha}")
    os.replace(dest + ".tmp", dest)


def fetch():
    for slug, g in GUTENBERG.items():
        download(g["url"], os.path.join(CACHE, g["file"]), g["sha256"])
        print(f"  {slug}: PG #{g['pg']} present, sha256 pinned")
    for slug, s0 in SCANS.items():
        for s in volumes(s0):
            # the item's rights field, read live: a changed status stops the fetch
            meta = json.load(urllib.request.urlopen(f"https://archive.org/metadata/{s['ia']}", timeout=120))
            got = meta.get("metadata", {}).get("possible-copyright-status")
            if got != s["ia_rights"]:
                raise SystemExit(f"{s['ia']}: possible-copyright-status {got!r} != recorded {s['ia_rights']!r}")
            f = f"{s['ia']}_hocr.html"
            download(f"https://archive.org/download/{s['ia']}/{f}", os.path.join(CACHE, f), s["sha256"])
            print(f"  {slug}: {s['ia']} hOCR present, sha256 pinned; rights field {got!r}")


def volumes(s):
    """The scans of a book: one, or each of its `volumes` with the book's
    settings under it (`vol` its number, None for a one-scan book)."""
    if "volumes" not in s:
        return [dict(s, vol=None)]
    return [dict({k: x for k, x in s.items() if k != "volumes"}, **v, vol=i + 1) for i, v in enumerate(s["volumes"])]

# ------------------------------------------------------------------ hOCR

LINE = re.compile(r'<span class="(?:ocr_line|ocr_caption|ocr_header|ocr_textfloat)"([^>]*)>')
WORD = re.compile(r'<span class="ocrx_word"([^>]*)>(.*?)</span>', re.S)
TITLE = re.compile(r'title="([^"]*)"')


def _title(attrs):
    m = TITLE.search(attrs)
    t = m.group(1) if m else ""
    bb = re.search(r'bbox (\d+) (\d+) (\d+) (\d+)', t)
    xs = re.search(r'x_size ([\d.]+)', t)
    cf = re.search(r'x_wconf (\d+)', t)
    return (tuple(map(int, bb.groups())) if bb else (0, 0, 0, 0),
            float(xs.group(1)) if xs else 0.0, int(cf.group(1)) if cf else 0)


def read_hocr(path):
    """charles_ocr.read_hocr's output, from either attribute order (the
    Hort file puts lang before title)."""
    with open(path, encoding="utf-8") as f:
        s = f.read()
    out = []
    for p in s.split('<div class="ocr_page"')[1:]:
        ms = list(LINE.finditer(p))
        lines = []
        for i, m in enumerate(ms):
            seg = p[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(p)]
            bbox, xs, _ = _title(m.group(1))
            words = []
            for w in WORD.finditer(seg):
                wb, _, conf = _title(w.group(1))
                t = html.unescape(re.sub('<[^>]+>', '', w.group(2))).strip()
                if t:
                    words.append(wb + (conf, t))
            if words:
                lines.append({"bbox": bbox, "xs": xs, "words": words, "text": " ".join(w[5] for w in words)})
        bb = re.search(r'bbox 0 0 (\d+) (\d+)', p)
        out.append({"w": int(bb.group(1)), "h": int(bb.group(2)), "lines": lines})
    return out


def pages(slug, s=None):
    s = s or SCANS[slug]
    src = os.path.join(CACHE, f"{s['ia']}_hocr.html")
    cache = os.path.join(CACHE, f"{s['ia']}.{s['sha256'][:12]}.pages.json.gz")
    if os.path.exists(cache):
        return C.load_pages(cache)
    if not os.path.exists(src) or sha256_file(src) != s["sha256"]:
        raise SystemExit(f"pinned hOCR missing or changed: {src}\n  run: python3 pipeline/build_commentaries.py --fetch")
    C.save_pages(read_hocr(src), cache)
    return C.load_pages(cache)

# ------------------------------------------------------------------ the page


def is_junk(l, med):
    """A line the OCR made of the large Greek type's accents and breathings
    alone ('U / 4 ‘ “-'), or nothing legible: small type, or short tokens."""
    t = l["text"]
    if not any(c.isalnum() for c in t):
        return True
    toks = [w[5] for w in l["words"]]
    longw = sum(1 for x in toks if sum(c.isalpha() for c in x) >= 3)
    if longw >= 4:
        return False
    if med and l["xs"] < 0.62 * med:
        return True
    lens = [sum(c.isalpha() for c in x) for x in toks]
    return len(toks) >= 3 and sum(lens) / len(toks) < 2.0


def headlike(l):
    t = l["text"].strip()
    if not t or len(l["words"]) > 9:
        return False
    if re.search(r'[\[\]\(\)\{\}]', t) and re.search(r'\d', t):
        return True
    if re.fullmatch(r'[^\w]*\d{1,3}[^\w]*', t):
        return True
    letters = [c for c in t if c.isalpha()]
    return bool(letters) and sum(c.isupper() for c in letters) >= 0.6 * len(letters)


REF_OPEN = re.compile(r'[\[\(\{]\s*([^\[\]\(\)\{\}]{1,18})$')
REF_CLOSE = re.compile(r'^\s*([^\[\]\(\)\{\}]{1,18}?)\s*[\]\)\}]')


def split_head(text):
    """(verse reference or None, rest) of a running-head line: 'EPISTLE TO THE
    GALATIANS. [I. 2, 3' -> ('I. 2, 3', 'EPISTLE TO THE GALATIANS.')."""
    m = REF_OPEN.search(text)
    if m and re.search(r'\d', m.group(1)):
        return m.group(1).strip(), text[:m.start()]
    m = REF_CLOSE.match(text)
    if m and re.search(r'\d', m.group(1)):
        return m.group(1).strip(), text[m.end():]
    return None, text


ROMANISH = str.maketrans({"Ι": "I", "ι": "I", "l": "I", "L": "I", "1": "I", "|": "I", "!": "I", "T": "I",
                          "t": "I", "i": "I", "Ί": "I", "Π": "II", "Η": "II", "H": "II", "Υ": "V", "v": "V",
                          "Χ": "X", "x": "X", "E": "I"})


def head_chapter(ref, nch):
    """The chapter of a running head's reference, read fuzzily ('IL. 4' is
    II, 'ΠῚ. 8' is III, '1. 6' is I), or None."""
    if not ref:
        return None
    r = "".join(c for c in unicodedata.normalize("NFD", ref) if not unicodedata.combining(c))
    m = re.match(r'\s*([^\W\d_]{1,5}|[|!]{1,4})\s*[.,:;]?\s*\d', r)
    if m:
        n = FS.roman(m.group(1).translate(ROMANISH))
        return n if n and 1 <= n <= nch else None
    m = re.match(r'\s*(\d)\s*\.\s*\d', r)
    if m and 1 <= int(m.group(1)) <= nch:
        return int(m.group(1))
    return None


def head_verses(ref):
    return [int(x) for x in re.findall(r'\d{1,2}', ref or "")]


def analyse(p):
    """Head, page number, verse reference, body lines and junk count of a leaf."""
    L = [l for l in p["lines"] if l["words"] and l["text"].strip()]
    many = [l["xs"] for l in L if len(l["words"]) >= 4]
    med = st.median(many) if many else None
    junk = [l for l in L if is_junk(l, med)]
    L = sorted([l for l in L if l not in junk], key=lambda l: l["bbox"][1])
    head = []
    if L:
        top = L[0]
        band = [l for l in L if l["bbox"][1] <= top["bbox"][3] - 0.3 * (top["bbox"][3] - top["bbox"][1])]
        head = [l for l in band if headlike(l)]
    ref, nums, rests = None, [], []
    for l in sorted(head, key=lambda l: l["bbox"][0]):
        r, rest = split_head(l["text"])
        if r and ref is None:
            ref = r
        rests.append(rest)
        nums += [int(t) for t in re.findall(r'(?<![\w.])(\d{1,3})(?![\w])', rest)]
    body = [l for l in L if l not in head]
    # a lone folio at the foot (chapter-opening pages print it there)
    foot = [l for l in body if l["bbox"][1] > 0.88 * p["h"] and re.fullmatch(r'\d{1,3}', l["text"].strip())]
    for l in foot:
        nums.append(int(l["text"].strip()))
    body = [l for l in body if l not in foot]
    title = " ".join(re.sub(r'[\d\W_]+', ' ', r).strip() for r in rests).strip()
    return {"head": " | ".join(l["text"] for l in sorted(head, key=lambda l: l["bbox"][0])),
            "ref": ref, "nums": nums, "title": title, "body": body, "junk": len(junk), "med": med}


def text_box(lines):
    xs0 = sorted(l["bbox"][0] for l in lines if len(l["words"]) >= 3)
    xs1 = sorted(l["bbox"][2] for l in lines if len(l["words"]) >= 3)
    if not xs0:
        return None
    return xs0[len(xs0) // 10], xs1[(9 * len(xs1)) // 10]


STOP = set("the and of to in is that which as be it by with for this not was his he are an on from but "
           "or have has its their they we our".split())


def layout(a, W, apparatus, prose_ok=False):
    """Split a leaf's body into: the epistle text above the notes, the
    apparatus under it, the notes in reading order (left column, then right),
    and a single-column tail. None if the leaf is not laid out in note columns."""
    body = a["body"]
    box = text_box(body)
    if not box:
        return None
    x0, x1 = box
    cx, tw = (x0 + x1) / 2, x1 - x0
    slack = 0.02 * W
    left = [l for l in body if l["bbox"][2] < cx + slack]
    right = [l for l in body if l["bbox"][0] > cx - slack]
    wide = lambda l: l["bbox"][2] - l["bbox"][0] > 0.28 * tw  # noqa: E731
    pairs = []
    for l in left:
        if not wide(l):
            continue
        for r in right:
            if wide(r) and abs(r["bbox"][1] - l["bbox"][1]) < 0.7 * max(l["xs"], 10):
                pairs.append((l, r))
                break
    if len(pairs) < 4:
        return None
    note_xs = st.median([l["xs"] for pr in pairs for l in pr])
    y_tc = min(min(l["bbox"][1], r["bbox"][1]) for l, r in pairs)
    in_cols = [l for l in left + right]
    zone_end = max(l["bbox"][3] for l in in_cols if l["bbox"][1] >= y_tc - 0.3 * note_xs)
    above, cols_l, cols_r, tail = [], [], [], []
    for l in body:
        y0 = l["bbox"][1]
        if y0 < y_tc - 0.3 * note_xs:
            above.append(l)
        elif l in left:
            cols_l.append(l)
        elif l in right:
            cols_r.append(l)
        elif y0 > zone_end - 0.3 * note_xs:
            tail.append(l)
        else:
            cols_l.append(l)          # a line across the gutter inside the notes: read with the left
    # The epistle's text is set in a larger type than the notes. A page whose
    # matter above the columns is in body type is an essay or a detached note
    # with its footnotes in two columns, not a commentary page.
    note_h = st.median([l["bbox"][3] - l["bbox"][1] for pr in pairs for l in pr])
    large = [l for l in above if l["bbox"][3] - l["bbox"][1] >= 1.25 * note_h or l["xs"] >= 1.25 * note_xs]
    small = [l for l in above if l not in large]
    prose = [l for l in small if sum(w[5].lower().strip(".,;:") in STOP for w in l["words"]) >= 2]
    if len(prose) >= 3 and not prose_ok:     # (Ellicott prints his textual notes full width above the notes)
        return None
    app, pre = [], []
    for l in small:
        (app if apparatus and l["xs"] < 0.92 * note_xs else pre).append(l)
    return {"text": large, "apparatus": app, "pre": pre, "left": C.merge_rows(cols_l),
            "right": C.merge_rows(cols_r), "tail": tail, "note_xs": note_xs}


def margin(col):
    xs = sorted(l["bbox"][0] for l in col if len(l["words"]) >= 3)
    return xs[len(xs) // 4] if xs else (min(l["bbox"][0] for l in col) if col else 0)


OPENER = re.compile(r'^[‘“"\'(]?(?:([IVXΙΠ][IVXLlΙΠ]{0,3})\.\s*)?([0-9IlOoSτt]{1,2})'
                    r'((?:\s*(?:[,—–\-]+|\s+and)\s*[0-9IlOoSτt]{1,2}){1,4})?\s*[.,]\s+(?=\D)')
RUN_LAST = re.compile(r'([0-9IlOoSτt]{1,2})\s*$')


def opener(text):
    """A verse number opening a note: (chapter printed with it or None, n,
    end of a run or None, 'read'|'read-fix') or None. 'II. 1, 2. ...' names
    its chapter; 'to.' is 10 with the OCR's letters undone."""
    m = OPENER.match(text)
    if not m:
        return None
    n = C.num(m.group(2))
    last = RUN_LAST.search(m.group(3)).group(1) if m.group(3) else None
    e = C.num(last) if last else None
    if n is None or n == 0 or (last and e is None):
        return None
    cp = FS.roman(m.group(1).translate(ROMANISH)) if m.group(1) else None
    if m.group(1) and not cp:
        return None
    fix = not m.group(2).isdigit() or bool(last and not last.isdigit())
    if e is not None and e <= n:
        e = None
    return cp, n, e, "read-fix" if fix else "read"


CHAPTER_WORD = re.compile(r'^\W{0,2}C[A-Za-z]{1,4}[Tt][Ee][Rr]\s*(?=[IVXΙΠ])')


def chapter_word(text):
    """Ellicott opens a chapter's first note 'CHAPTER II. 1. διά]': the word
    dropped so the chapter and verse read as an opener; an old-style figure 1
    read as 'τ' there is 1."""
    t = CHAPTER_WORD.sub("", text)
    if t is not text and t != text:
        t = re.sub(r'^([IVXΙΠ][IVXLlΙΠ]{0,3}\.\s*)[τt]\.', r'\g<1>1.', t)
    return t


def stream(lay):
    """Note lines in reading order, each with whether it is indented."""
    out = [(l, True) for l in lay["pre"]]     # full-width matter above the columns: may open a verse
    for col in (lay["left"], lay["right"]):
        mg = margin(col)
        for l in col:
            ind = l["bbox"][0] - mg
            out.append((l, 0.45 * lay["note_xs"] <= ind <= 2.6 * lay["note_xs"]))
    return out

# ------------------------------------------------------------------ verses


def kjv_ids():
    with open(UIDS, encoding="utf-8") as f:
        return {k for k in json.load(f)["uids"] if k.startswith("kjv:")}


def verse_counts(ids, book):
    out = collections.defaultdict(int)
    for k in ids:
        b, c, v = k[4:].rsplit(".", 2)
        if b == book:
            out[int(c)] = max(out[int(c)], int(v))
    return dict(out)


class Decoder:
    """The verse sequence of one epistle's notes. An opener is accepted in
    the current chapter at or after the current verse (within the chapter's
    KJV verse count, and no further ahead than the page's running head allows),
    or as the opening verses of the next chapter where the running head or
    the end of the chapter says the chapter has turned."""
    GAP = 10

    def __init__(self, counts, lookahead=False):
        self.counts = counts
        self.nch = max(counts)
        self.c, self.v = 1, 0
        self.lookahead = lookahead

    def offer(self, n, e, hc, hv, cp=None, hsure=False, ahead=()):
        """hc: the chapter of the page's running head (None if unread); hsure:
        the next or previous leaf's head agrees with it; hv: the verse numbers
        the heads print; cp: a chapter printed with the opener itself."""
        c, v, cnt = self.c, self.v, self.counts
        if self.lookahead and cp is None and n > v + 1 \
                and sum(1 for a in ahead[:4] if a[0] in (None, c) and v < a[1] < n) >= 2:
            # (wave 2a books) two of the next four openers fall between: this
            # number is a misreading ('11' for '4' at Ellicott's Gal 6.4)
            return None
        if cp is not None:
            # a chapter printed with the number: taken if it is this one or the next
            if cp == c + 1 and n <= 4:
                return self._take(cp, n, e)
            if cp != c:
                if hsure and cp == hc and n <= cnt.get(cp, 0):
                    return self._take(cp, n, e)
                return None
        if hsure and hc is not None and hc not in ((c,) if self.lookahead else (c, c + 1)) and n <= cnt.get(hc, 0):
            return self._take(hc, n, e)      # two agreeing running heads put the notes elsewhere: follow them
        limit = max(hv) + 2 if hv else v + self.GAP
        if v <= n <= cnt.get(c, 0) and n <= max(limit, v + 3) and n - v <= self.GAP + 6:
            if not (hc == c + 1 and n <= 3 and v >= 3):
                return self._take(c, n, e)
        if c + 1 <= self.nch and n <= 4 and n < max(v, 1) \
                and (hc == c + 1 or (hc is None and v >= cnt.get(c, 0) - 3)):
            # a new chapter opens at its first verse: a later number with a '1.'
            # close behind is a list inside a note (or an additional note), not the turn
            if n > 1 and any(a[1] == 1 and a[0] in (None, c + 1) for a in ahead):
                return None
            if self.lookahead and hc != c + 1 \
                    and any(a[0] in (None, c) and max(v, 4) < a[1] <= cnt.get(c, 0) for a in ahead):
                return None    # (wave 2a) this chapter's later verses are still to come: a list, not the turn
            return self._take(c + 1, n, e)
        if v - 2 <= n < v and n >= 1 and hc in (None, c):
            # a note on a verse just passed (Lightfoot takes 3 after 4 at Gal 1.3):
            # taken, and the sequence stays where it was
            return c, n, (e if e and e <= cnt.get(c, 0) and e - n <= 15 else None)
        return None

    def _take(self, c, n, e):
        if e is not None and (e > self.counts.get(c, 0) or e - n > 15):
            e = None
        self.c, self.v = c, n
        return c, n, e

# ------------------------------------------------------------------ scripture

FS.FAMILY.setdefault("eng", {}).update({
    "judg": "Judg", "judges": "Judg", "jude": "Jude", "jud": "Jude", "james": "Jas",
    "apoc": "Rev", "hebr": "Heb", "philem": "Phlm", "lk": "Luke", "mk": "Mark", "jn": "John",
})
SELF_VER = re.compile(r'\b(?:ver|vv|vers)\.\s*(\d{1,2})((?:\s*[,–—-]\s*\d{1,2}(?!\s*[a-zA-Z]{2,}\.))*)')
SELF_C = re.compile(r'\bc\.\s*([ivxl]{1,6})\.\s*(\d{1,2})\b')


_CHAPTERS = {}


def chapters(ids):
    if not _CHAPTERS:
        for k in ids:
            b, c, _ = k[4:].rsplit(".", 2)
            _CHAPTERS[b] = max(_CHAPTERS.get(b, 0), int(c))
    return _CHAPTERS


def scripture(text, ids, own=None, chapter=None):
    """English references in a unit's text, resolved in the KJV's numbering."""
    out, seen = [], set()
    for r in FS.parse("¶ " + text, "eng"):
        book, kind, ch, v, end, alt = r
        p = FS.printed(r)
        if p in seen:
            continue
        seen.add(p)
        if kind != "kjv":
            out.append({"ref": p, "resolved": False, "why": "a book outside the KJV", "rule": "text/kjv"})
            continue
        if v is None:
            why = ("cites a whole chapter, not a verse" if ch <= chapters(ids).get(book, 0) else
                   "no such chapter: another work cited by the same abbreviation (Ignatius's Ephesians...), "
                   "or an OCR misreading")
            out.append({"ref": p, "resolved": False, "why": why, "rule": "text/kjv"})
            continue
        t = f"kjv:{book}.{ch}.{v}"
        if t not in ids:
            out.append({"ref": p, "resolved": False, "why": "no such verse in the KJV (an OCR misreading, or "
                        "another numbering)", "rule": "text/kjv"})
            continue
        x = {"ref": p, "target": t, "resolved": True, "numbering": "english", "rule": "text/kjv"}
        if end and f"kjv:{book}.{ch}.{end}" in ids:
            x["through"] = f"kjv:{book}.{ch}.{end}"
        out.append(x)
    if own:
        hits = []
        if chapter:
            for m in SELF_VER.finditer(text):
                vs = [int(m.group(1))] + [int(x) for x in re.findall(r'\d{1,2}', m.group(2))]
                hits += [("self/ver", chapter, x) for x in vs]
        for m in SELF_C.finditer(text):
            c = FS.roman(m.group(1))
            if c:
                hits.append(("self/c", c, int(m.group(2))))
        for rule, c, v in hits:
            t = f"kjv:{own}.{c}.{v}"
            p = f"{own} {c}:{v}"
            if p in seen:
                continue
            seen.add(p)
            if t in ids:
                out.append({"ref": p, "target": t, "resolved": True, "numbering": "english", "rule": rule})
            else:
                out.append({"ref": p, "resolved": False, "why": "no such verse in the KJV", "rule": rule})
    return out

# ------------------------------------------------------------------ Greek


def _fold(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if not unicodedata.combining(c)).replace("ς", "σ").replace("ϲ", "σ")


GREEK_WORD = re.compile(r'[Ͱ-Ͽἀ-῿]+')
_VOCAB = None


def greek_vocab():
    """Strong's Greek lemmas and the forms of John in data/nt (both committed):
    a fixed yardstick for how much OCR'd Greek is Greek words."""
    global _VOCAB
    if _VOCAB is None:
        v = set()
        with open(STRONGS, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                if d["strongs"].startswith("G"):
                    v |= {_fold(w) for w in GREEK_WORD.findall(d.get("lemma") or "")}
        with open(NT_JOHN, encoding="utf-8") as f:
            for line in f:
                v |= {_fold(w) for w in GREEK_WORD.findall(line)}
        _VOCAB = v
    return _VOCAB


def greek_measure(texts):
    letters = greek = mixed = 0
    toks = known = 0
    vocab = greek_vocab()
    for t in texts:
        for c in t:
            if c.isalpha():
                letters += 1
                if 'Ͱ' <= c <= 'Ͽ' or 'ἀ' <= c <= '῿':
                    greek += 1
        for w in re.findall(r'\w+', t):
            g = any('Ͱ' <= c <= 'Ͽ' or 'ἀ' <= c <= '῿' for c in w)
            if g and any('a' <= c.lower() <= 'z' for c in w):
                mixed += 1
        for w in GREEK_WORD.findall(t):
            if len(w) >= 3:
                toks += 1
                known += _fold(w) in vocab
    return {"greek_letters": greek, "greek_share_of_letters": round(greek / letters, 4) if letters else 0,
            "greek_tokens_3plus": toks, "greek_tokens_in_reference_vocab": round(known / toks, 4) if toks else 0,
            "mixed_script_tokens": mixed}

HEBREW = {"lightfoot-horae"}           # books measured for Hebrew too
HEBREW_WORD = re.compile(r'[\u05d0-\u05ea\u05f0-\u05f2\u0591-\u05c7]+')
_HVOCAB = None


def _hfold(w):
    w = "".join(c for c in unicodedata.normalize("NFD", w) if '\u05d0' <= c <= '\u05ea')
    return w.translate(str.maketrans("ךםןףץ", "כמנפצ"))


def hebrew_measure(texts):
    """Hebrew letters as a share of all letters, and how many Hebrew words
    (3+ letters) are a Strong's Hebrew lemma, as written or after one
    prefixed letter (ו ב ל כ מ ש ה ד): a fixed yardstick of biblical words,
    so the Talmud's Hebrew and Aramaic score lower than its OCR deserves."""
    global _HVOCAB
    if _HVOCAB is None:
        _HVOCAB = set()
        with open(STRONGS, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                if d["strongs"].startswith("H"):
                    _HVOCAB |= {_hfold(w) for w in HEBREW_WORD.findall(d.get("lemma") or "")}
    letters = heb = toks = known = known_p = 0
    for t in texts:
        for c in t:
            if c.isalpha():
                letters += 1
                heb += '\u05d0' <= c <= '\u05ea'
        for w in HEBREW_WORD.findall(t):
            w = _hfold(w)
            if len(w) >= 3:
                toks += 1
                known += w in _HVOCAB
                known_p += w in _HVOCAB or (w[0] in "ובלכמשהד" and w[1:] in _HVOCAB)
    return {"hebrew_letters": heb, "hebrew_share_of_letters": round(heb / letters, 4) if letters else 0,
            "hebrew_tokens_3plus": toks,
            "hebrew_tokens_strongs_lemma": round(known / toks, 4) if toks else 0,
            "hebrew_tokens_strongs_lemma_or_prefixed": round(known_p / toks, 4) if toks else 0}

# ------------------------------------------------------------------ printed pages


def printed_pages(nums_by_leaf):
    """{leaf: (page, 'read'|'neighbours')}. A folio read in the head is
    trusted when the leaves around it agree on the offset (leaf -> page);
    a leaf whose folio was not read takes the offset its nearest read
    neighbours on both sides agree on."""
    offs = {}
    for leaf, nums in nums_by_leaf.items():
        for n in nums:
            offs.setdefault(leaf, []).append(n - leaf)
    leaves = sorted(nums_by_leaf)
    good = {}
    for leaf in leaves:
        win = collections.Counter(o for q in leaves if abs(q - leaf) <= 12 and q != leaf for o in offs.get(q, []))
        for o in offs.get(leaf, []):
            if win[o] >= 2:
                good[leaf] = o
                break
    out = {leaf: (leaf + o, "read") for leaf, o in good.items()}
    gl = sorted(good)
    for leaf in leaves:
        if leaf in out:
            continue
        before = [q for q in gl if q < leaf and leaf - q <= 6]
        after = [q for q in gl if q > leaf and q - leaf <= 6]
        if before and after and good[before[-1]] == good[after[0]]:
            out[leaf] = (leaf + good[before[-1]], "neighbours")
    return out

# ------------------------------------------------------------------ scanned books


def ids_prefix(slug, book):
    return f"{book}." if slug in MULTI else ""


def vol_id(vol):
    return f"v{vol}." if vol else ""


def vol_ref(vol):
    return f"vol. {vol}, " if vol else ""


def page_unit(slug, s, leaf, lines, a, pp, extra=None, vol=None):
    cols = C.columns(lines, max(l["bbox"][2] for l in lines) + 1) if lines else [lines]
    text = ""
    for col in cols:
        for l in col:
            text = C.join(text, l["text"])
        if len(cols) > 1 and col is not cols[-1]:
            text += " |"
    scan = {"leaves": [leaf]}
    if leaf in pp:
        scan["printed_page"] = pp[leaf][0]
        if pp[leaf][1] != "read":
            scan["printed_page_from"] = pp[leaf][1]
    if a["head"]:
        scan["running_head"] = a["head"]
    if len(cols) > 1:
        scan["columns"] = len(cols)
    if vol:
        scan["volume"] = vol
    u = {"id": f"{slug}:{vol_id(vol)}leaf.{leaf}",
         "ref": f"{s['short']}, {vol_ref(vol)}" + (f"p. {pp[leaf][0]}" if leaf in pp else f"leaf {leaf}"),
         "kind": "page", "text": text, "links": [], "scan": scan}
    if a["title"]:
        u["section"] = a["title"]
    if extra:
        u["scan"].update(extra)
    return u


LECTURE = re.compile(r'LECTURE\s+([IVX]{1,4})\.')


def note_ref(s, book, c=None, n=None, e=None):
    """'Lightfoot on Gal 2.20': the commentator, then the verse his note is on."""
    who = s["short"].split(",")[0]
    if c is None:
        return f"{who} on {book}"
    return f"{who} on {book} {c}.{n}" + (f"-{e}" if e else "")


def hort_leaves(P):
    """Title page to the printer's imprint: the leaves with the book's text."""
    first = next(i for i, p in enumerate(P)
                 if any("LECTURES" in l["text"] for l in p["lines"]))
    # the imprint is printed twice, on the title verso and after the last page: the text ends at the last
    last = max(i for i, p in enumerate(P)
               if any("PRINTED BY" in l["text"].upper() and "CLAY" in l["text"].upper() for l in p["lines"]))
    return first, last


HEAD_CU = re.compile(r'[\[\(\{]\s*[CcO06][HhUuXxNnaΗ][.,]?\s*([IVXLΙΠΗΥΧlLiE1|!TtΊ]{1,7})(?![\w.])')
HEAD_PLAIN = re.compile(r'(?<![^\W\d_])([IVXΙΠΗ][IVXLΙΠΗl]{0,4})\s*[.,]\s*(\d{1,2}(?:\s*[,—–-]+\s*\d{1,2})*)')
HEAD_CH = re.compile(r'C\s*[hH]\w{0,2}\s*[.,]?\s*([ivxlIVXL1Ι|]{1,7})\s*[.,]\s*(\d{1,2})')


def head_ref(a, s, nch):
    """(chapter or None, verse numbers) of a leaf's running head, read as the
    book's `head` style says; without one, as the Lightfoot and Westcott
    epistles print it ('[I. 2, 3')."""
    style = s.get("head")
    if style == "cu":
        m = HEAD_CU.search(a["head"])
        n = FS.roman(m.group(1).translate(ROMANISH)) if m else None
        c = n if n and 1 <= n <= nch else None
        vs = head_verses(a["ref"]) if a["ref"] and re.match(r'\W*V', a["ref"]) else []
    elif style == "plain":
        m = HEAD_PLAIN.search(a["head"])
        c = head_chapter(f"{m.group(1)}. {m.group(2)}", nch) if m else None
        vs = head_verses(m.group(2)) if m and c else []
    elif style == "ch":
        m = HEAD_CH.search(a["head"])
        n = FS.roman(m.group(1).translate(ROMANISH)) if m else None
        c = n if n and 1 <= n <= nch else None
        vs = [int(m.group(2))] if m and c else []
    else:
        return (1 if nch == 1 else head_chapter(a["ref"], nch)), head_verses(a["ref"])
    return (1 if nch == 1 else c), vs


VER = re.compile(r'^[\W_]{0,2}V[Ee][Rr][Ss]?\s*[.,]?\s*([0-9IlOoSτtg]{1,2})((?:\s*[,.—–-]+\s*[0-9IlOoSτtg]{1,2})*)'
                 r'[^\s\w]{0,2}\w?[^\s\w]{0,2}\s*[:;.,](?!\d)')
CHAP = re.compile(r'^[\W_]{0,2}CHAP[S.,:]*\s*(\S{1,8})')


def ver_opener(text):
    """'Ver. 5:' (or 'Ver. 9, 10*:', the footnote mark read as a letter):
    (None, n, end or None, 'read'|'read-fix') or None."""
    m = VER.match(text)
    if not m:
        return None
    n = C.num(m.group(1))
    rest = re.findall(r'[0-9IlOoSτtg]{1,2}', m.group(2) or "")
    e = C.num(rest[-1]) if rest else None
    if not n or (rest and e is None):
        return None
    fix = not m.group(1).isdigit() or bool(rest and not rest[-1].isdigit())
    return None, n, (e if e and e > n else None), "read-fix" if fix else "read"


def chap_heading(text, nch):
    """A 'CHAP. XI.' heading line: its chapter, -1 if the number is unread, else None."""
    if len(text.split()) > 4:
        return None
    m = CHAP.match(text)
    if not m:
        return None
    r = re.sub(r'[^\w|!]', '', m.group(1))
    r = re.sub(r'[a-z]$', '', r) if len(r) > 1 else r     # a footnote letter after the numeral
    n = FS.roman(r.translate(ROMANISH)) if r else None
    return n if n and 1 <= n <= nch else -1


class VerDecoder:
    """Lightfoot's Horae: each note opens 'Ver. 5:', so the number is a verse
    without guessing; only its chapter is read, from a 'CHAP. XI.' heading
    in the body, or from a running head ('[Ch. xi. 4.') that a head within
    three leaves agrees with. Chapters only go forward (he skips many); when
    a heading is unread, or the verse goes back, the next agreeing head
    names the chapter. A verse past the chapter's KJV count is refused."""

    def __init__(self, counts):
        self.counts = counts
        self.nch = max(counts)
        self.c, self.v = 0, 0

    def offer(self, n, e, hc, ahead, heading):
        c = self.c
        if heading and heading > 0 and c < heading <= self.nch:
            c = heading
        elif hc and hc > c:
            c = hc
        elif (heading == -1 or n < self.v) and ahead and ahead > c:
            c = ahead
        if c == 0:
            c = ahead or 1
        if not 1 <= n <= self.counts.get(c, 0):
            return None
        if e is not None and (e > self.counts[c] or e - n > 15):
            e = None
        self.c, self.v = c, n
        return c, n, e


def build_scan(slug, ids):
    s0 = SCANS[slug]
    vols = volumes(s0)
    multi = len(vols) > 1
    ver = s0.get("style") == "ver"
    books = []
    for s in vols:
        for e in s["epistles"]:
            if e[0] not in books:
                books.append(e[0])
    units, notes = [], collections.OrderedDict()
    m = collections.Counter()
    decoders = {book: VerDecoder(verse_counts(ids, book)) if ver else
                Decoder(verse_counts(ids, book), s0.get("lookahead", False)) for book in books}
    spans, pps = [], {}
    # pass 1: every leaf read; note lines collected with their page's evidence
    lines = []
    for s in vols:
        vol = s["vol"] if multi else None
        P = pages(slug, s)
        a0, b0 = s["leaves"] if s["leaves"] else hort_leaves(P)
        spans.append((a0, b0))
        A = {leaf: analyse(P[leaf]) for leaf in range(a0, b0 + 1)}
        pp = printed_pages({leaf: a["nums"] for leaf, a in A.items()})
        pps[vol] = pp
        seg, start = {}, {}
        for e in s["epistles"]:
            for leaf in range(e[1], e[2] + 1):
                seg[leaf] = e[0]
            if len(e) > 3:
                start[e[1]] = e[3]
        heads = {leaf: head_ref(A[leaf], s, decoders[seg[leaf]].nch) for leaf in seg if leaf in A}
        where = lambda leaf: (f"{s['short']}, {vol_ref(vol)}"  # noqa: E731
                              + (f"p. {pp[leaf][0]}" if leaf in pp else f"leaf {leaf}"))
        for leaf in range(a0, b0 + 1):
            a = A[leaf]
            m["junk_lines_dropped"] += a["junk"]
            if leaf in start:
                lines.append({"restart": (seg[leaf], start[leaf])})
            if ver and leaf in seg:
                book = seg[leaf]
                nch = decoders[book].nch
                m["leaves_commentary"] += 1
                hc = heads[leaf][0]
                near = [heads[q][0] for q in range(leaf - 3, leaf + 4) if q != leaf and seg.get(q) == book]
                hok = hc if hc is not None and hc in near else None
                ahead = next((heads[q][0] for q in range(leaf, leaf + 7) if seg.get(q) == book
                              and heads[q][0] is not None
                              and heads[q][0] in [heads[r][0] for r in range(q - 3, q + 4)
                                                  if r != q and seg.get(r) == book]), None)
                body = C.merge_rows(a["body"])
                mg = margin(body)
                xs = a["med"] or 40
                for l in body:
                    ind = l["bbox"][0] - mg
                    lines.append({"book": book, "leaf": leaf, "vol": vol, "pp": pp.get(leaf), "line": l,
                                  "indented": 0.45 * xs <= ind <= 2.6 * xs, "o": ver_opener(l["text"]),
                                  "heading": chap_heading(l["text"], nch), "hc": hok, "ahead": ahead})
                continue
            lay = layout(a, P[leaf]["w"], s["apparatus"], s.get("prose_above", False)) if leaf in seg else None
            if lay is None:
                if a["body"]:
                    units.append(page_unit(slug, s, leaf, a["body"], a, pp, vol=vol))
                    m["leaves_page"] += 1
                continue
            book = seg[leaf]
            m["leaves_commentary"] += 1
            hc, hv = heads[leaf]
            nch = decoders[book].nch
            nxt = head_ref(A[leaf + 1], s, nch) if leaf + 1 in A else None
            prv = head_ref(A[leaf - 1], s, nch) if leaf - 1 in A else None
            hc_next = nxt[0] if nxt else None
            hc_prev = prv[0] if prv else None
            near = (hc_next, hc_prev)
            if s.get("head") == "cu":       # the chapter is printed on every other page only
                near += tuple(heads[q][0] for q in (leaf - 2, leaf + 2) if q in heads)
            hsure = hc is not None and hc in near
            hv = hv + (nxt[1] if nxt and hc_next == hc else [])
            if lay["text"] or lay["apparatus"]:
                t = ""
                for l in lay["text"]:
                    t = C.join(t, l["text"])
                u = {"id": f"{slug}:{vol_id(vol)}leaf.{leaf}.text", "ref": where(leaf) + ", text",
                     "kind": "epistle-text", "book": book, "text": t, "links": [],
                     "scan": {"leaves": [leaf]}}
                if lay["apparatus"]:
                    u["apparatus"] = " ".join(l["text"] for l in lay["apparatus"])
                if a["head"]:
                    u["scan"]["running_head"] = a["head"]
                if leaf in pp:
                    u["scan"]["printed_page"] = pp[leaf][0]
                if vol:
                    u["scan"]["volume"] = vol
                units.append(u)
            for l, indented in stream(lay):
                o = opener(chapter_word(l["text"]) if s.get("head") else l["text"]) if indented else None
                lines.append({"book": book, "leaf": leaf, "vol": vol, "pp": pp.get(leaf), "line": l,
                              "indented": indented, "o": o,
                              "hc": hc, "hc_next": hc_next, "hv": hv, "hsure": hsure})
            if lay["tail"]:
                units.append(page_unit(slug, s, leaf, lay["tail"], a, pp, {"after_notes": True}, vol=vol))
                m["leaves_with_tail"] += 1
    # pass 2: the verse sequence, each candidate seeing the next few candidates
    current, heading = {}, {}
    cand = [i for i, x in enumerate(lines) if x.get("o")]
    nxt_cand = {i: [(lines[j]["o"][0], lines[j]["o"][1]) for j in cand[k + 1:k + 7] if lines[j]["book"] == lines[i]["book"]]
                for k, i in enumerate(cand)}
    for i, x in enumerate(lines):
        if "restart" in x:
            book, c = x["restart"]
            decoders[book].c, decoders[book].v = c, 0
            current[book] = None
            continue
        book, leaf, l, indented, o = x["book"], x["leaf"], x["line"], x["indented"], x["o"]
        dec = decoders[book]
        took = None
        if ver:
            if x["heading"] is not None:
                heading[book] = x["heading"]
                m["chapter_headings" if x["heading"] > 0 else "chapter_headings_unread"] += 1
            if o:
                took = dec.offer(o[1], o[2], x["hc"], x["ahead"], heading.pop(book, None))
        else:
            hc = x["hc"]
            if hc is None and x["hc_next"] is not None and x["hc_next"] > dec.c:
                hc = x["hc_next"]
            if o:
                took = dec.offer(o[1], o[2], hc, x["hv"], o[0], x["hsure"], nxt_cand[i])
        if took and (ver or dec.lookahead) and x["hc"] is not None:
            # (wave 2a) a check, not a rule: the page's running head read a chapter
            m["openers_on_headed_pages"] += 1
            m["openers_against_running_head"] += took[0] != x["hc"]
        if o:
            m["openers_accepted" if took else "openers_rejected"] += 1
            if took and o[3] == "read-fix":
                m["openers_read_with_fix"] += 1
        cur = current.get(book)
        if took:
            c, n, e = took
            key = f"{ids_prefix(slug, book)}{c}.{n}" + (f"-{e}" if e else "")
            if key in notes and key != cur and (ver or dec.lookahead):
                m["notes_reopened"] += 1      # (wave 2a) the verse taken again later: its text joins the first
            if key not in notes:
                notes[key] = {"book": book, "c": c, "n": n, "e": e, "text": "", "leaves": [], "pages": [],
                              "vol": x["vol"]}
            cur = current[book] = key
        if cur is None:
            cur = current[book] = f"{vol_id(x['vol'])}{ids_prefix(slug, book)}title"
            notes.setdefault(cur, {"book": book, "c": None, "n": None, "e": None, "text": "",
                                   "leaves": [], "pages": [], "vol": x["vol"]})
        nu = notes[cur]
        nu["text"] = nu["text"] + "\n" + l["text"] if (indented and nu["text"]) else C.join(nu["text"], l["text"])
        if leaf not in nu["leaves"]:
            nu["leaves"].append(leaf)
            if x["pp"] and x["pp"][0] not in nu["pages"]:
                nu["pages"].append(x["pp"][0])
    for key, nu in notes.items():
        book = nu["book"]
        s = s0
        if nu["c"] is None:
            ref, links = f"{note_ref(s, book)}, before the first note", []
        else:
            vs = range(nu["n"], (nu["e"] or nu["n"]) + 1)
            links = [{"target": f"kjv:{book}.{nu['c']}.{v}", "type": "comments-on",
                      "resolved": f"kjv:{book}.{nu['c']}.{v}" in ids} for v in vs]
            ref = note_ref(s, book, nu["c"], nu["n"], nu["e"])
        u = {"id": f"{slug}:{key}", "ref": ref, "kind": "note", "book": book, "text": nu["text"], "links": links,
             "scan": {"leaves": nu["leaves"]}}
        if nu["pages"]:
            u["scan"]["printed_pages"] = nu["pages"]
        if nu["vol"]:
            u["scan"]["volume"] = nu["vol"]
        units.append(u)
    order = {"page": 0, "epistle-text": 0, "note": 1}
    units.sort(key=lambda u: (u["scan"].get("volume", 0), min(u["scan"]["leaves"]), order[u["kind"]]))
    if not books:
        # a book of lectures: each page says which lecture it is in, from the
        # 'LECTURE I.' heading that opens it (the ids stay the leaves)
        lect = None
        for u in units:
            mm = LECTURE.match(u["scan"].get("running_head", ""))
            if mm:
                lect = FS.roman(mm.group(1)) or lect
                m["lecture_headings"] += 1
            if lect:
                u["lecture"] = lect
    pp = pps[None] if not multi else pps
    return units, m, (spans[0] if not multi else spans), pp


# ------------------------------------------------------------------ Gutenberg

BLOCK = re.compile(r'<(h[1-6]|p|li|td)\b([^>]*)>(.*?)</\1>'
                   r'|<div class="(sidenote[^"]*)">(.*?)</div>'
                   r'|<div(?: class="([^"]*)")?>((?:(?!<div)(?!</div>)(?!<h[1-6])(?!<p\b)(?!<li\b)(?!<td\b).)*?)</div>',
                   re.S)
PAGENO = re.compile(r'<span class="pageno" id="Page_([0-9ivxlc]+)">[^<]*</span>')
ARROW = re.compile(r'<a href="#Page_[0-9ivxlc]+" class="pginternal">\s*(?:→|←|&gt;|&lt;|>|<)?\s*</a>')
ANCHOR = re.compile(r'<a id="([A-Za-z]+_\d+)"></a>(?:<sup>\d+</sup>)?')
FNREF = re.compile(r'<a id="(r\d+)"></a>')


def clean(x):
    x = ARROW.sub("", x)
    x = re.sub(r'<br\s*/?>', ' ', x)
    x = re.sub(r'<[^>]+>', '', x)
    return re.sub(r'\s+', ' ', html.unescape(x)).strip()


NOTE_OPEN = re.compile(r'^(?:([IV]{1,3})\.\s*)?(\d{1,2})(?:\s*[,–—-]\s*(\d{1,2}))?\.\s')


def gutenberg_rights(raw):
    head = raw[:raw.find("*** START")]
    if "COPYRIGHTED Project Gutenberg" in raw[:raw.find("*** START") + 2000] or "COPYRIGHTED" in head:
        raise SystemExit("the Gutenberg header says COPYRIGHTED: not shelved")
    m = re.search(r'This eBook is for the use of anyone anywhere in the United States[^<]*?(?=<|\n\n)', head)
    return re.sub(r'\s+', ' ', m.group(0)).strip() if m else None


def build_gutenberg(slug, ids):
    g = GUTENBERG[slug]
    src = os.path.join(CACHE, g["file"])
    if not os.path.exists(src) or sha256_file(src) != g["sha256"]:
        raise SystemExit(f"pinned file missing or changed: {src}\n  run: python3 pipeline/build_commentaries.py --fetch")
    with open(src, encoding="utf-8") as f:
        raw = f.read()
    rights_line = gutenberg_rights(raw)
    body = raw[raw.find("*** START"):raw.find("*** END")]
    fn_at = body.find('<div class="footnote"')
    main, fns = body[:fn_at], body[fn_at:]
    footnotes = {m.group(1): clean(m.group(2))
                 for m in re.finditer(r'<div class="footnote" id="(f\d+)">(.*?)</div>', fns, re.S)}
    m = collections.Counter()
    pages = collections.OrderedDict()      # page -> unit
    notes = collections.OrderedDict()
    greek = collections.OrderedDict()      # (book, c, v) -> text
    seen_anchor = []                       # (book, c, v) in order
    page, section, region = "front", None, None
    cur_note, cur_verse = None, None
    fn_home = {}
    roman_ch = {"I": 1, "II": 2, "III": 3, "IV": 4, "ph": 1}
    covered = 0
    for b in BLOCK.finditer(main):
        tag, inner = b.group(1), b.group(3)
        cm = re.search(r'class="([^"]*)"', b.group(2) or "")
        cls = cm.group(1) if cm else ""
        if tag is None and b.group(4):
            tag, cls, inner = "sidenote", b.group(4), b.group(5)
        elif tag is None:
            tag, cls, inner = "div", b.group(6) or "", b.group(7)
        if tag in ("h2", "h3"):
            t = clean(inner)
            region = next((bk for k, bk in g["regions"].items() if t.startswith(k)), None)
            section = t
            cur_note = None
        # split the block at page breaks
        parts = PAGENO.split(inner)
        segs = [(None, parts[0])] + [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]
        for i, (pg, frag) in enumerate(segs):
            if pg is not None:
                page = pg
            t = clean(frag)
            covered += len(t)
            if not t:
                continue
            refs = FNREF.findall(frag)
            if tag in ("h2", "h3"):
                hp = _page(pages, slug, page, section, g)
                hp.setdefault("headings", []).append(t)
                for r in refs:
                    fn_home[r] = ("page", page)
                continue
            if region:
                book = region
                if tag == "p" and "c000" in cls.split() and t.endswith("]"):
                    continue                                  # the running head ("I. 3]")
                if tag == "p" and "c032" in cls.split():       # Lightfoot's Greek text
                    pieces = re.split(r'<a id="([A-Za-z]+_\d+)"></a>', frag)
                    for j, piece in enumerate(pieces):
                        if j % 2 == 1:
                            mm = g["anchor"][book].match(piece)
                            if mm:
                                cur_verse = (book, roman_ch[mm.group(1)], int(mm.group(2)))
                                seen_anchor.append(cur_verse)
                            continue
                        x = clean(re.sub(r'<sup>\d+</sup>', '', piece))
                        if x and cur_verse:
                            greek[cur_verse] = (greek.get(cur_verse, "") + " " + x).strip()
                    continue
                mo = NOTE_OPEN.match(t) if (tag == "p" and i == 0) else None
                if mo:
                    n = int(mo.group(2))
                    e = int(mo.group(3)) if mo.group(3) and int(mo.group(3)) > n else None
                    c0 = cur_verse[1] if cur_verse and cur_verse[0] == book else 1
                    seen = {(x[1], x[2]) for x in seen_anchor if x[0] == book}
                    # the chapter of the latest Greek verse, unless the number is
                    # well past it and was printed in the chapter before (a note
                    # on 1.29 after the text has turned to 2.1)
                    if mo.group(1):
                        c = FS.roman(mo.group(1))           # 'IV. 1.' names its chapter
                    elif (c0, n) not in seen and (c0 - 1, n) in seen and n > cur_verse[2] + 2:
                        c = c0 - 1
                    else:
                        c = c0
                    m["openers"] += 1
                    if (c, n) not in seen:
                        m["openers_before_their_verse_anchor"] += 1
                    cur_note = f"{book}.{c}.{n}" + (f"-{e}" if e else "")
                    notes.setdefault(cur_note, {"book": book, "c": c, "n": n, "e": e, "paras": [], "pages": []})
                if cur_note is None:
                    cur_note = f"{book}.title"
                    notes.setdefault(cur_note, {"book": book, "c": None, "n": None, "e": None,
                                                "paras": [], "pages": []})
                nu = notes[cur_note]
                if i > 0 and nu["paras"]:
                    nu["paras"][-1] += " " + t              # the paragraph runs on over a page break
                else:
                    nu["paras"].append(t)
                if page not in nu["pages"]:
                    nu["pages"].append(page)
                for r in refs:
                    fn_home[r] = ("note", cur_note)
                continue
            u = _page(pages, slug, page, section, g)
            if tag == "sidenote":
                u.setdefault("sidenotes", []).append(t)
            else:
                u["_paras"].append(t)       # a paragraph cut by a page break: its second half opens the new page
            for r in refs:
                fn_home[r] = ("page", page)
    units = []
    for key, nu in notes.items():
        book = nu["book"]
        u = {"id": f"{slug}:{key}", "ref": note_ref(g, book, nu["c"], nu["n"], nu["e"]), "kind": "note",
             "book": book, "text": "\n".join(nu["paras"]), "links": [], "pages": nu["pages"]}
        if nu["c"] is not None:
            vs = range(nu["n"], (nu["e"] or nu["n"]) + 1)
            u["links"] = [{"target": f"kjv:{book}.{nu['c']}.{v}", "type": "comments-on",
                           "resolved": f"kjv:{book}.{nu['c']}.{v}" in ids} for v in vs]
        units.append(u)
    for (book, c, v), t in greek.items():
        units.append({"id": f"{slug}:text.{book}.{c}.{v}", "ref": f"{g['short']} {book} {c}.{v}, text",
                      "kind": "epistle-text", "book": book, "text": t,
                      "links": [{"target": f"kjv:{book}.{c}.{v}", "type": "text-of",
                                 "resolved": f"kjv:{book}.{c}.{v}" in ids}]})
    for pg, u in pages.items():
        u["text"] = "\n".join(u.pop("_paras"))
        units.append(u)
    byid = {u["id"]: u for u in units}
    for r, (kind, where) in fn_home.items():
        f = footnotes.get("f" + r[1:])
        if f is None:
            continue
        uid = f"{slug}:{where}" if kind == "note" else f"{slug}:p.{where}"
        byid[uid].setdefault("notes", []).append(f)
    m["footnotes"] = len(footnotes)
    m["footnotes_placed"] = sum(1 for r in fn_home if "f" + r[1:] in footnotes)
    total = len(clean(main))
    m["text_chars_captured"] = round(covered / total, 4) if total else 0
    return units, m, rights_line


def _page(pages, slug, page, section, g):
    if page not in pages:
        pages[page] = {"id": f"{slug}:p.{page}", "ref": f"{g['short']}, p. {page}", "kind": "page",
                       "text": "", "links": [], "_paras": []}
        if section:
            pages[page]["section"] = section
    return pages[page]


# ------------------------------------------------------------------ books


def scan_books(slug):
    out = []
    for v in volumes(SCANS[slug]):
        out += [e[0] for e in v["epistles"] if e[0] not in out]
    return out


def harvest(slug, units, ids):
    own = None
    if slug in SCANS and len(scan_books(slug)) == 1:
        own = scan_books(slug)[0]
    n = r = 0
    for u in units:
        book = u.get("book") or own
        ch = None
        if u["kind"] == "note":
            k = u["id"].split(":", 1)[1]
            mm = re.match(r'(?:[1-3]?[A-Za-z]+\.)?(\d+)\.\d', k)
            ch = int(mm.group(1)) if mm else None
        text = u["text"] + " " + " ".join(u.get("notes", []))
        found = scripture(text, ids, own=book if u["kind"] in ("note", "page") else None, chapter=ch)
        u["links"] += found
        n += len(found)
        r += sum(1 for x in found if x["resolved"])
    return n, r


def honesty(slug, ocr):
    if not ocr:
        return ("notes keyed by verse exactly as the Project Gutenberg transcription marks them: a note "
                "paragraph opening with a verse number (or a run, '3-8.') starts that verse's unit, its chapter "
                "the latest verse anchor in Lightfoot's Greek text with that number; following lemma notes "
                "belong to it; Lightfoot's Greek text per verse (text.<book>.<c>.<v>); introductions, "
                "dissertations and index by printed page (p.N) as the transcription marks page breaks, "
                "footnotes on the unit holding their reference mark, marginal summaries in 'sidenotes'; the "
                "transcription is proofread (Distributed Proofreaders), not checked here against the print")
    if slug == "hort-ante-nicene":
        return ("page-exact: one unit per scan leaf (leaf.N), the printed folio in scan.printed_page where the "
                "running head gives it or its neighbours agree on it (scan.printed_page_from); each page"
                " carries the lecture it falls in (`lecture`, from the LECTURE headings), but lectures and paragraphs are NOT units; unproofread OCR")
    sc = SCANS.get(slug, {})
    if sc.get("style") == "ver":
        return ("notes keyed by verse as Lightfoot heads them, 'Ver. 5:' at the start of a line (the number read "
                "as printed, a footnote mark after it ignored), in one column; the CHAPTER is not printed with "
                "the verse and is read from a 'CHAP. XI.' heading in the body or from the running heads "
                "('[Ch. xi. 4.'), a head counting only where a head within three leaves agrees, chapters only "
                "moving forward (he comments on chosen verses and skips whole chapters), so a misread head can "
                "put a run of notes in the wrong chapter (openers_against_running_head counts the notes whose "
                "page head reads another chapter; notes_reopened, the verses taken up again further on, whose "
                "text joins the first unit of that verse); every following line belongs to the note, the page's "
                "footnotes (Gandell's references) included where they stand; vol. 1 (the chorographical "
                "century and inquiries) and the dedications, prefaces, addenda and indexes by scan leaf "
                "(v<N>.leaf.<M>, the folio in scan.printed_page where read); lines of bare accents dropped and "
                "counted; the Hebrew and Aramaic quotations are the OCR's Hebrew script, unpointed and often "
                "misread (measure.hebrew); unproofread OCR")
    tail = f"; {sc['honesty']}" if sc.get("honesty") else ""
    return ("notes keyed by verse where the OCR'd page lets them be: an indented verse number opening a note "
            "paragraph is accepted when the verse sequence (and the fuzzily read running head) allows it, "
            "and every following line, left column then right, belongs to it; boundaries are therefore only "
            "as good as the numbers read off the page, and a misread or rejected number merges a verse's notes "
            "into the verse before (counts in measure); the epistle's text block per leaf (leaf.N.text, with "
            "the critical apparatus under it where printed); every other page (introduction, detached and "
            "additional notes, dissertations, essays, index) by scan leaf (leaf.N, the folio in "
            "scan.printed_page where read); lines of bare accents dropped and counted; marginal summaries "
            f"may be run into their lines{tail}; unproofread OCR")


def citation(slug, ocr):
    if slug == "hort-ante-nicene":
        return "scan leaf (leaf.N), one per printed page; the folio, where read, in scan.printed_page"
    lead = "book.chapter.verse" if slug in MULTI else "chapter.verse"
    pages = "printed page (p.N)" if not ocr else "scan leaf (leaf.N; folio in scan.printed_page)"
    if "volumes" in SCANS.get(slug, {}):
        pages = "volume and scan leaf (v<N>.leaf.<M>; folio in scan.printed_page)"
        if SCANS[slug].get("style") == "ver":
            return (f"note: {lead} of the verse commented on (a run of verses: {lead}-end); notes before a "
                    f"book's first: v<N>.book.title; everything else: {pages}")
        return (f"note: {lead} of the verse commented on (a run of verses: {lead}-end); epistle text: "
                f"v<N>.leaf.<M>.text; everything else: {pages}")
    return (f"note: {lead} of the verse commented on (a run of verses: {lead}-end); epistle text: "
            + ("text.book.chapter.verse" if not ocr else "leaf.N.text") + f"; everything else: {pages}")


def build_book(slug, ids):
    ocr = slug in SCANS
    if ocr:
        s = SCANS[slug]
        units, m, spans, pp = build_scan(slug, ids)
        if "volumes" not in s:
            a0, b0 = spans
            source = {"format": "ia-hocr", "sha256": s["sha256"], "ia": s["ia"], "leaves": [a0, b0]}
            rights = {"license": f"public domain in the US (printed {s['printed']}); the scan and its OCR are the "
                                 "Internet Archive's",
                      "ia_possible_copyright_status": s["ia_rights"] or "(the item's metadata carries no rights field)",
                      "attribution": f"Internet Archive, {s['ia']} ({s['copy']} copy)",
                      "source_url": f"https://archive.org/details/{s['ia']}",
                      "redistribute_whole": True}
            pv = list(pp.values())
        else:
            vs = volumes(s)
            # one sha256 for the set: of the volumes' pinned sha256s, in order
            source = {"format": "ia-hocr",
                      "sha256": hashlib.sha256(" ".join(v["sha256"] for v in vs).encode()).hexdigest(),
                      "volumes": [{"vol": v["vol"], "ia": v["ia"], "sha256": v["sha256"], "leaves": list(sp)}
                                  for v, sp in zip(vs, spans)]}
            rights = {"license": f"public domain in the US (printed {s['printed']}); the scans and their OCR are "
                                 "the Internet Archive's",
                      "ia_possible_copyright_status": "; ".join(
                          f"vol. {v['vol']} {v['ia']}: " + (v["ia_rights"] or "(the item's metadata carries no "
                                                             "rights field)") for v in vs),
                      "attribution": "Internet Archive, " + "; ".join(f"{v['ia']} ({v['copy']} copy)" for v in vs),
                      "source_url": " ".join(f"https://archive.org/details/{v['ia']}" for v in vs),
                      "redistribute_whole": True}
            pv = [x for d in pp.values() for x in d.values()]
        meta = s
        m["printed_page_read"] = sum(1 for x in pv if x[1] == "read")
        m["printed_page_from_neighbours"] = sum(1 for x in pv if x[1] != "read")
    else:
        g = GUTENBERG[slug]
        units, m, line = build_gutenberg(slug, ids)
        source = {"format": "gutenberg-html", "sha256": g["sha256"], "pg": g["pg"], "url": g["url"]}
        rights = {"license": f"public domain in the US (printed {g['printed']}); Project Gutenberg's header is "
                             "not marked COPYRIGHTED",
                  "gutenberg_header": line,
                  "attribution": f"Project Gutenberg eBook #{g['pg']} (KD Weeks, Colin Bell and the Online "
                                 "Distributed Proofreading Team)",
                  "source_url": f"https://www.gutenberg.org/ebooks/{g['pg']}",
                  "redistribute_whole": True}
        meta = g
    n_links, n_resolved = harvest(slug, units, ids)
    kinds = collections.Counter(u["kind"] for u in units)
    measure = {"units": dict(sorted(kinds.items())), **dict(sorted(m.items()))}
    eps = scan_books(slug) if ocr else list(GUTENBERG[slug]["regions"].values())
    if eps:
        cov = {}
        for b in eps:
            allv = {k for k in ids if k.startswith(f"kjv:{b}.")}
            have = {x["target"] for u in units if u["kind"] == "note" and u.get("book") == b
                    for x in u["links"] if x.get("type") == "comments-on" and x["resolved"]}
            single = {x["target"] for u in units if u["kind"] == "note" and u.get("book") == b
                      for x in u["links"] if x.get("type") == "comments-on" and x["resolved"]
                      and len([y for y in u["links"] if y.get("type") == "comments-on"]) == 1}
            cov[b] = {"kjv_verses": len(allv), "commented": len(have), "with_own_note": len(single)}
        measure["kjv_coverage"] = cov
    measure["scripture_links"] = {"read": n_links, "resolved": n_resolved}
    measure["greek"] = greek_measure(u["text"] for u in units)
    if slug in HEBREW:
        measure["hebrew"] = hebrew_measure(u["text"] for u in units)
    book = {"slug": slug, "title": meta["title"], "author": meta["author"], "edition": meta["edition"],
            "source": source,
            "scheme": {"citation": citation(slug, ocr), "resolution": "verse-note" if eps else "page",
                       "honesty": honesty(slug, ocr), "status": "draft"},
            "rights": rights, "measure": measure, "units": units}
    return book


def entry(book, blob):
    src = book["source"]
    if "pg" in src:
        where = f"PG #{src['pg']}"
    elif "volumes" in src:
        where = "; ".join(f"vol. {v['vol']}: scan leaves {v['leaves'][0]}-{v['leaves'][1]} of {v['ia']}"
                          for v in src["volumes"])
    else:
        where = f"scan leaves {src['leaves'][0]}-{src['leaves'][1]} of {src['ia']}"
    return {"title": book["title"], "author": book["author"], "format": src["format"], "sha256": src["sha256"],
            "units": len(book["units"]),
            "scheme": dict(book["scheme"], note=f"{book['edition']}; {where}"
                           + (f"; {SCANS[book['slug']]['note']}" if SCANS.get(book["slug"], {}).get("note") else "")),
            "rights": book["rights"], "measure": book["measure"],
            "built_sha256": hashlib.sha256(blob).hexdigest()}


def build(slugs=None):
    ids = kjv_ids()
    out = {}
    for slug in ORDER:
        if slugs and slug not in slugs:
            continue
        book = build_book(slug, ids)
        blob = json.dumps(book, ensure_ascii=False).encode("utf-8")
        out[slug] = (book, blob, entry(book, blob))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("books", nargs="*")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    built = build(a.books)
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    for slug, (book, _, e) in built.items():
        m = e["measure"]
        cov = " ".join(f"{b} {c['commented']}/{c['kjv_verses']}" for b, c in m.get("kjv_coverage", {}).items())
        print(f"  {slug:<22}{e['units']:>5} units  {dict(m['units'])}  {cov}  "
              f"scripture {m['scripture_links']['resolved']}/{m['scripture_links']['read']}  "
              f"greek {m['greek']['greek_share_of_letters']:.1%} known {m['greek']['greek_tokens_in_reference_vocab']:.1%}")
        if a.report:
            print("      " + json.dumps({k: v for k, v in m.items() if k not in ("units", "greek")},
                                        ensure_ascii=False))
    if a.report:
        return
    if a.check:
        bad = [s for s, (_, blob, e) in built.items() if manifest.get(s) != e]
        if bad:
            raise SystemExit(f"CHECK FAILED: rebuilt books differ from the manifest: {bad}")
        print("  CHECK PASSED: every book = its committed manifest entry (built_sha256).")
        return
    for slug, (_, blob, e) in built.items():
        write_atomic(os.path.join(BOOKS_DIR, slug + ".json"), blob)
        manifest[slug] = e
    write_atomic(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    print(f"  wrote {len(built)} books + {len(manifest)}-entry manifest")


if __name__ == "__main__":
    main()
