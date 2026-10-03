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

THE SECOND SHELF (Alford, Bengel, Keil & Delitzsch: one book per volume) is
the table SECOND and its own reader, build_book_2b: see the comment above
SECOND for the scans measured and chosen, and harvest_2b for how Keil &
Delitzsch's Old Testament numbering is measured and mapped.
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
        "ia": "saintpaulsepistl00lighrich", "ia_date": "1910",
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
        "ia": "stpaulsepistleto00lighuoft", "ia_date": "1873",
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
        "ia": "epistletohebrew00westgoog", "ia_date": "1892",
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
        "ia": "cu31924074296629", "ia_date": "1892",
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
        "ia": "sixlecturesonant00hortrich", "ia_date": "1895",
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
            {"ia": "gospelaccordingt01west", "ia_date": "1908",
             "sha256": "ec341318718254bee14e7b664297519746defaf373a783b57128cdb29f04fc44",
             "copy": "Princeton Theological Seminary Library", "ia_rights": None,
             "leaves": (5, 483), "epistles": [("John", 202, 483)]},
            {"ia": "gospelaccordingt02west", "ia_date": "1908",
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
            {"ia": "horaehebraicaeet0001ligh", "ia_date": "1859",
             "sha256": "1ba4063fdbc1c09f0a721e4c489f77fe8534d5ecb1fb8c7fcf1b863fa81ef4d6",
             "copy": "Internet Archive scan", "ia_rights": None, "leaves": (5, 394), "epistles": []},
            {"ia": "horaehebraicaeet0002ligh", "ia_date": "1859",
             "sha256": "e54b581870ba3818113c255170311583fbae9fe887d3ce66a5d6f7e26e5adebb",
             "copy": "Internet Archive scan", "ia_rights": None, "leaves": (5, 486),
             "epistles": [("Matt", 13, 390), ("Mark", 399, 486)]},
            {"ia": "horaehebraicaeet0003ligh", "ia_date": "1859",
             "sha256": "8ffc3f7c8498da9a72af76b4e7c284a30474db48349cdcf2970dbbcc01a02e7c",
             "copy": "Internet Archive scan", "ia_rights": None, "leaves": (5, 462),
             "epistles": [("Luke", 11, 237), ("John", 243, 461)]},
            {"ia": "horaehebraicaeet0004ligh", "ia_date": "1859",
             "sha256": "d373363ad662c0e272c3e220015a793b7ee23c8e79a4e3d1cdb8be08d1e1d373",
             "copy": "Internet Archive scan", "ia_rights": None, "leaves": (5, 354),
             "epistles": [("Acts", 11, 159), ("Rom", 161, 170), ("1Cor", 177, 291)]},
        ],
    },
    "ellicott-galatians": {
        "ia": "stpaulsepistleto00elli", "ia_date": "1867",
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
        "ia": "cu31924029294240", "ia_date": "1884",
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
        "ia": "criticalgrammati00elli", "ia_date": "1857",
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
        "ia": "cu31924029294539", "ia_date": "1880",
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
        "ia": "pastoralepistles00elli", "ia_date": "1883",
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
            date = meta.get("metadata", {}).get("date")
            if date != s["ia_date"]:
                raise SystemExit(f"{s['ia']}: metadata date {date!r} != recorded {s['ia_date']!r}")
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
    cut = e is not None and e <= n
    if cut:
        e = None
    return Read((cp, n, e, "read-fix" if fix else "read"), cut)


class Read(tuple):
    """An opener as read; `run_cut` is true when its run ran backwards and
    only its first verse was kept (counted in openers_run_cut)."""
    def __new__(cls, t, run_cut=False):
        x = super().__new__(cls, t)
        x.run_cut = run_cut
        return x


# a run opener that crosses into the next chapter ('28—V. 1.'): not read as
# a run (a note id names one chapter); counted in openers_crossing_chapter
CROSS_OPEN = re.compile(r'^\W{0,2}\d{1,2}\s*[—–-]+\s*[IVX]{1,4}\.\s*\d{1,2}\s*\.')


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
        self.runs_cut = 0          # runs longer than 15 verses or past the chapter: first verse kept

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
            return c, n, self._run(c, n, e)
        return None

    def _run(self, c, n, e):
        if e is not None and (e > self.counts.get(c, 0) or e - n > 15):
            self.runs_cut += 1
            return None
        return e

    def _take(self, c, n, e):
        e = self._run(c, n, e)
        self.c, self.v = c, n
        return c, n, e

# ------------------------------------------------------------------ scripture

FS.FAMILY.setdefault("eng", {}).update({
    "judg": "Judg", "judges": "Judg", "jude": "Jude", "jud": "Jude", "james": "Jas",
    "apoc": "Rev", "hebr": "Heb", "philem": "Phlm", "lk": "Luke", "mk": "Mark", "jn": "John",
})
SELF_VER = re.compile(r'\b(?:ver|vv|vers)\.\s*(\d{1,2})((?:\s*[,–—-]\s*\d{1,2}(?!\s*[a-zA-Z]{2,}\.))*)')
SELF_C = re.compile(r'\bc\.\s*([ivxl]{1,6})\.\s*(\d{1,2})\b')
# the word before a bare 'c. iv. 3': an abbreviation ending in '.' names
# another work ('Euseb. H.E. c. iv. 3', 'ib. c. 3'), unless it is one of these
SELF_C_BEFORE = re.compile(r'(\S+)\s*$')
SELF_C_OK = {"cf.", "comp.", "conf.", "cp.", "see", "so", "also", "esp.", "and", "in", "on", "with", "as", "e.g.",
             "i.e.", "above", "below", "ver.", "vv.", "(", "[", ";", ","}
# a range crossing a chapter: 'viii. 28-ix. 3' or '8:28-9:3' (FS.parse reads its start only)
CROSS_RANGE = re.compile(r'\b([ivxlc]{1,7})\.\s*(\d{1,3})\s*[–—-]+\s*([ivxlc]{1,7})\.\s*(\d{1,3})\b'
                         r'|\b(\d{1,3}):(\d{1,3})\s*[–—-]+\s*(\d{1,3}):(\d{1,3})\b')
# a range running backwards in one chapter ('iii. 12-8'): FS.parse drops its end
BACK_RANGE = re.compile(r'\b([ivxlc]{1,7})\.\s*(\d{1,3})\s*[–—-]+\s*(\d{1,3})\b(?!\s*[.:]\s*\d)'
                        r'|\b(\d{1,3}):(\d{1,3})\s*[–—-]+\s*(\d{1,3})\b(?!\s*[.:]\s*\d)')


_CHAPTERS = {}


def chapters(ids):
    if not _CHAPTERS:
        for k in ids:
            b, c, _ = k[4:].rsplit(".", 2)
            _CHAPTERS[b] = max(_CHAPTERS.get(b, 0), int(c))
    return _CHAPTERS


def cross_ranges(text):
    """(chapter, verse) -> (chapter, verse) for every range in the text that
    crosses into a later chapter, or runs backwards in one."""
    out = {}
    for m in CROSS_RANGE.finditer(text):
        if m.group(1):
            a, b = FS.roman(m.group(1)), FS.roman(m.group(3))
            v, w = int(m.group(2)), int(m.group(4))
        else:
            a, v, b, w = (int(m.group(k)) for k in (5, 6, 7, 8))
        if a and b and b > a:
            out.setdefault((a, v), (b, w))
    for m in BACK_RANGE.finditer(text):
        a = FS.roman(m.group(1)) if m.group(1) else int(m.group(4))
        v, w = (int(m.group(2)), int(m.group(3))) if m.group(1) else (int(m.group(5)), int(m.group(6)))
        if a and w < v:
            out.setdefault((a, v), (a, w))
    return out


def self_c_refused(text, start):
    """A bare 'c. iv. 3' is another work's chapter when the word before it is
    an abbreviation ('Euseb. H.E. c. iv. 3')."""
    m = SELF_C_BEFORE.search(text[max(0, start - 40):start])
    if not m:
        return False
    w = m.group(1)
    return w.endswith(".") and w.lower() not in SELF_C_OK and not re.fullmatch(r'[\d.]+', w)


def scripture(text, ids, own=None, chapter=None):
    """English references in a unit's text, resolved in the KJV's numbering.
    `own` (a note unit's epistle) also reads 'ver. 20' (with `chapter`) and a
    bare 'c. iii. 13' as the commentary's own epistle, unless an abbreviation
    of another work stands just before it. A range keeps its end in `through`;
    a range the KJV cannot end (past the chapter, or backwards) keeps its
    start only and says so in `through_unread`."""
    out, seen = [], set()
    xr = cross_ranges(text)
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
        if end:
            if end > v and f"kjv:{book}.{ch}.{end}" in ids:
                x["through"] = f"kjv:{book}.{ch}.{end}"
            else:
                x["through_unread"] = f"{ch}:{end}: " + ("backwards" if end <= v else "past the chapter")
        elif (ch, v) in xr:
            c2, v2 = xr[(ch, v)]
            if c2 == ch:
                x["through_unread"] = f"{ch}:{v2}: backwards"
            elif f"kjv:{book}.{c2}.{v2}" in ids:
                x["through"] = f"kjv:{book}.{c2}.{v2}"
                x["ref"] = p = f"{p}-{c2}:{v2}"
            else:
                x["through_unread"] = f"{c2}:{v2}: no such verse"
        out.append(x)
    if own:
        hits = []
        if chapter:
            for m in SELF_VER.finditer(text):
                # '8-12' a range, '8, 9' two verses
                parts = re.findall(r'([,–—-])?\s*(\d{1,2})', m.group(1) + m.group(2))
                runs = []
                for sep, d in parts:
                    if sep and sep != "," and runs:
                        runs[-1][1] = int(d)
                    else:
                        runs.append([int(d), None])
                hits += [("self/ver", chapter, a, b) for a, b in runs]
        for m in SELF_C.finditer(text):
            c = FS.roman(m.group(1))
            if c and not self_c_refused(text, m.start()):
                hits.append(("self/c", c, int(m.group(2)), None))
        for rule, c, v, e in hits:
            t = f"kjv:{own}.{c}.{v}"
            p = f"{own} {c}:{v}" + (f"-{e}" if e else "")
            if p in seen:
                continue
            seen.add(p)
            if t in ids:
                x = {"ref": p, "target": t, "resolved": True, "numbering": "english", "rule": rule}
                if e:
                    if e > v and f"kjv:{own}.{c}.{e}" in ids:
                        x["through"] = f"kjv:{own}.{c}.{e}"
                    else:
                        x["through_unread"] = f"{c}:{e}: " + ("backwards" if e <= v else "past the chapter")
                out.append(x)
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
    return Read((None, n, (e if e and e > n else None), "read-fix" if fix else "read"), bool(e and e <= n))


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
        self.runs_cut = 0

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
            self.runs_cut += 1
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
            if took and o.run_cut:
                m["openers_run_cut"] += 1
        elif indented and CROSS_OPEN.match(l["text"]):
            m["openers_crossing_chapter"] += 1
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
    if books:
        # runs kept only at their first verse: backwards, over 15 verses, past
        # the chapter; and run openers into the next chapter, not read at all
        m["openers_run_cut"] += sum(d.runs_cut for d in decoders.values())
        m["openers_crossing_chapter"] += 0
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
    m = collections.Counter(openers_run_cut=0, openers_crossing_chapter=0)
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
                if not mo and tag == "p" and i == 0 and CROSS_OPEN.match(t):
                    m["openers_crossing_chapter"] += 1
                if mo:
                    n = int(mo.group(2))
                    e = int(mo.group(3)) if mo.group(3) and int(mo.group(3)) > n else None
                    m["openers_run_cut"] += bool(mo.group(3)) and e is None     # a run backwards: its start kept
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


# ================================================================== the second shelf (2026-10-03)
#
# Henry Alford's Greek Testament (vols II-IV), J. A. Bengel's Gnomon in the
# T. & T. Clark English (vols II-IV), and Keil & Delitzsch's Biblical
# Commentary on the Old Testament (the Pentateuch and Delitzsch on the Psalms;
# Isaiah measured but not shelved), all from Internet Archive hOCR, every scan chosen by measuring
# its text layer (2026-10-03, on each item's _djvu.txt: Greek letters as a share
# of all letters; Greek tokens of 3+ letters found in the Strong's/John
# vocabulary above; English tokens found in the dwyl word list; Hebrew letters
# as a share of all letters):
#
#   Alford I (Gospels)  greektestamentwi01alfo 1849-cat. (Lane A's item), greektestamentwidv01alfo 1874,
#                       greektestamentwi189801alfo 1897: 0.0% Greek (every Greek word in Latin letters);
#                       greektestament00alfogoog 1849, greektestamentw00unkngoog 1863: ~100% Greek letters
#                       (the English OCR'd as Greek). bub_gb_YOY2AAAAMAAJ (Michigan): its text layer would
#                       not download (HTTP 500, 2026-10-03). NOT SHELVED: no scan keeps both languages.
#   Alford II           greektestamentwi02alfo 3rd ed. 1857  17.3%  34.1%  84.1%   <- chosen (Lane A's item)
#                       greektestamentwiptsl02alfo 1899 (7th ed., new impr.) 17.1% 34.8% 84.0% (not clearly better)
#                       greektestamentw02alfo 1849-cat., greektestamentwidvr02alfo 1874, greektestamentwi0002alfo
#                       1859: 0.0% Greek; greektestament02alfo 1868: ~100% Greek letters
#   Alford III          greektestamentwi00alfo 4th ed. 1865  15.4%  35.5%  86.8%   <- chosen (Lane A has no vol. III)
#                       greektestamentw03alfo 1849-cat. 15.8% 35.5% 86.5%; greektestamentwi0003alfo 1859: 0.0%;
#                       greektestament03alfo 1868: ~100% Greek letters; greektestamentwi03alfo 1856: no text layer (HTTP 500)
#   Alford IV           greektestamentwi04alfo 4th ed., Boston (Lee & Shepard) 14.0% 35.7% 87.6%  <- chosen (Lane A's item)
#                       greektestamentwi5604alfo 3rd ed. 1866 13.6% 35.5% 87.4%; greektestamentwiptsl04alfo 1897 14.0% 35.3%
#   Bengel I, V         every scan of the English Gnomon's vols I and V (gnomonofthenewte01benguoft 1857,
#                       gnomonofnewt01beng 1873, gnomonofnewtest01beng 1873, cu31924092350515 1877,
#                       cu31924092350531 1866, gnomonofnewtesta05beng 1859, the Philadelphia 2-vol. translation
#                       gnomonnewtestam00benggoog 1864 and johnalbertbenge00benggoog 1860...): 0.0% Greek. NOT SHELVED.
#   Bengel II + III     gnomonofnewtesta23beng 1873 (7th ed., vols II and III bound as one) 6.3% 34.4% 95.8%  <- chosen
#                       cu31924092350523 1877 (vol. II only) 5.9% 33.1% 95.7%; cu31924092350499 1877 (vol. III): 0.0%
#   Bengel IV           cu31924092350507 1877 (7th ed.) 7.5% 32.4% 95.3%   <- chosen
#                       gnomonofnewtesta03benguoft 1873: 0.0% Greek
#   (Neither CCEL nor Project Gutenberg has Bengel's Gnomon or Keil & Delitzsch: searched 2026-10-03.)
#   K&D: no scan of any volume keeps its Hebrew (0.00% Hebrew letters in all 40 measured: the pointed
#   Hebrew is OCR'd as Latin-letter debris). Chosen by English share:
#   Pentateuch I        thepentateuch01keiluoft 1878 95.2%  <- (pentateuch01keil 1866 95.1%, biblicalcomm01keiluoft 1869 94.8%)
#   Pentateuch II       biblicalcomm02keiluoft 1872 95.3%   <- (pentateuch02keiluoft 1872 95.2%)
#   Pentateuch III      pentateuch03keiluoft 1871 95.2%     <- (biblicalcommenta03keiluoft 1867 94.9%, pentateuch03keil 94.7%)
#   Psalms I            commentarypsalm01deliuoft 1880 91.6% <- (biblicalcommenta187101deli 1871 91.2%, ...188001 1877 91.2%)
#   Psalms II           biblicalcommenta187102deli 1871 91.3% <- (biblicalcommenta188002deli 1877 91.1%)
#   Psalms III          commentarypsalm03deliuoft 1880 92.0% <- (biblicalcommenta03deli 1877 91.2%, biblicalcomment02unkngoog no hOCR)
#   Isaiah I, II        biblicalcommenta1deliuoft / biblicalcoisaiah02deliuoft 1890 (4th ed.) 93.3% / 93.0%
#                       (isaiahsprophecie01/02deliuoft 1884 93.3/93.1%; the 1867 Indian-library scans 92.8/93.1%).
#                       NOT SHELVED YET: Delitzsch's Isaiah does not open its sections 'Ver. 3.' as the Pentateuch
#                       and the Psalms do (39 such openers in vol. I's 400 pages, against ~600 verses; the 1867
#                       translation measures the same on its text layer). It needs a reader keyed by the running
#                       heads ('CHAPTER V. 11, 12.', recto only) instead. Their hOCR, measured 2026-10-03:
#                       f05085fa5e015134f3b67c6bca38f35b539d0b4debfbad6b8eba09f4c7ccbb6a (vol. I),
#                       349c3a341f55971b7307b9f8dd95d91d0dc39e95925547968a97f36e988a0858 (vol. II).

def _alford(vol, ia, sha, edition, printed, copy, rights, leaves, books, lane_a):
    return {"ia": ia, "sha256": sha, "title": f"The Greek Testament, vol. {vol}", "short": f"Alford, Gk Test. {vol}",
            "author": "Henry Alford", "edition": edition, "printed": printed, "copy": copy, "ia_rights": rights,
            "leaves": leaves, "epistles": books, "apparatus": True, "reader": "alford", "lane_a": lane_a}


def _bengel(vol, ia, sha, edition, printed, copy, rights, leaves, books):
    return {"ia": ia, "sha256": sha, "title": f"Gnomon of the New Testament, vol. {vol}", "short": f"Bengel, Gnomon {vol}",
            "author": "J. A. Bengel", "edition": edition, "printed": printed, "copy": copy, "ia_rights": rights,
            "leaves": leaves, "epistles": books, "apparatus": False, "reader": "bengel"}


def _kd(title, short, author, ia, sha, edition, printed, copy, rights, leaves, books):
    return {"ia": ia, "sha256": sha, "title": title, "short": short, "author": author, "edition": edition,
            "printed": printed, "copy": copy, "ia_rights": rights, "leaves": leaves, "epistles": books,
            "apparatus": False, "reader": "kd"}


_ALF = ("Henry Alford, The Greek Testament: with a critically revised text, a digest of various readings, "
        "marginal references to verbal and idiomatic usage, prolegomena, and a critical and exegetical commentary")
_BEN = ("John Albert Bengel, Gnomon of the New Testament, now first translated into English, revised and edited "
        "by Andrew R. Fausset (Edinburgh: T. & T. Clark)")
_KD = "C. F. Keil and F. Delitzsch, Biblical Commentary on the Old Testament (Edinburgh: T. & T. Clark, Clark's Foreign Theological Library)"
_KDP = "C. F. Keil and F. Delitzsch"
SECOND = {
    "alford-commentary-2": _alford(
        "II", "greektestamentwi02alfo", "d19889cfbb6cf820564721633a48e0e26204a10bdf4a56211648400d56853a7e",
        f"{_ALF}, vol. II (Acts, Romans, Corinthians), 3rd ed. (London: Rivingtons; Cambridge: Deighton, Bell, 1857), "
        "as its title page reads", 1857, "University of California Libraries", "NOT_IN_COPYRIGHT", (5, 794),
        [("Acts", 105, 392), ("Rom", 393, 549), ("1Cor", 550, 698), ("2Cor", 699, 794)], True),
    "alford-commentary-3": _alford(
        "III", "greektestamentwi00alfo", "0d6492f87b3e3ce6a6adee9a61d5ff9832fd6f4ed83f1f5c5601511e5a7d26fd",
        f"{_ALF}, vol. III (Galatians to Philemon), 4th ed. (London: Rivingtons; Cambridge: Deighton, Bell, 1865), "
        "as its title page reads", 1865, "Boston University School of Theology", None, (7, 579),
        [("Gal", 145, 211), ("Eph", 212, 295), ("Phil", 296, 339), ("Col", 340, 391), ("1Thess", 392, 427),
         ("2Thess", 428, 443), ("1Tim", 444, 510), ("2Tim", 511, 551), ("Titus", 552, 572), ("Phlm", 573, 579)],
        False),
    "alford-commentary-4": _alford(
        "IV", "greektestamentwi04alfo", "770fee70202d9a1a3ccd92aacc00072cda2496ed124f984993dd70879ea544d5",
        f"{_ALF}, vol. IV (Hebrews to the Revelation), 4th ed. (Boston: Lee and Shepard; New York: Lee, Shepard and "
        "Dillingham), the American issue of Rivingtons' London edition; the title page is undated, the item's "
        "catalogue date is 1874", 1874, "Princeton Theological Seminary Library", "NOT_IN_COPYRIGHT", (5, 1057),
        [("Heb", 307, 579), ("Jas", 580, 636), ("1Pet", 637, 694), ("2Pet", 695, 726), ("1John", 727, 821),
         ("2John", 822, 827), ("3John", 828, 834), ("Jude", 835, 849), ("Rev", 850, 1057)], True),
    "bengel-gnomon-2": _bengel(
        "II", "gnomonofnewtesta23beng", "174e4034973d12427eea4bd705a47342e3be3274e9b03996b1d1027b5e593478",
        f"{_BEN}, vol. II (Luke, John, Acts), tr. Andrew R. Fausset, seventh edition (1873), as its title page "
        "reads; bound with vol. III", 1873,
        "Princeton Theological Seminary Library", "NOT_IN_COPYRIGHT", (9, 754),
        [("Luke", 13, 237), ("John", 238, 527), ("Acts", 528, 754)]),
    "bengel-gnomon-3": _bengel(
        "III", "gnomonofnewtesta23beng", "174e4034973d12427eea4bd705a47342e3be3274e9b03996b1d1027b5e593478",
        f"{_BEN}, vol. III (Romans, Corinthians), tr. James Bryce, seventh edition (1873), as its own title "
        "page (leaf 755) reads; bound after vol. II",
        1873, "Princeton Theological Seminary Library", "NOT_IN_COPYRIGHT", (755, 1199),
        [("Rom", 757, 960), ("1Cor", 961, 1110), ("2Cor", 1111, 1199)]),
    "bengel-gnomon-4": _bengel(
        "IV", "cu31924092350507", "ac11e9768744c1f7d7b1b98a7b0acfb3a17aefa66b3d63c178fa5dd66a385e1c",
        f"{_BEN}, vol. IV (Galatians to Hebrews), tr. James Bryce, seventh edition (1877), as its title page reads", 1877,
        "Cornell University Library", None, (4, 509),
        [("Gal", 8, 66), ("Eph", 67, 125), ("Phil", 126, 163), ("Col", 164, 195), ("1Thess", 196, 218),
         ("2Thess", 219, 244), ("1Tim", 245, 295), ("2Tim", 296, 323), ("Titus", 324, 333), ("Phlm", 334, 338),
         ("Heb", 339, 509)]),
    "keil-delitzsch-pentateuch-1": _kd(
        "Biblical Commentary on the Old Testament: The Pentateuch, vol. I", "Keil, Pent. I", _KDP,
        "thepentateuch01keiluoft", "39ee9f3f185433552ab2069c3dc4e4049ad032fdb961337303c229b162291d06",
        f"{_KD}, vol. I: The Pentateuch (Genesis; Exodus i.-xi.), by C. F. Keil, tr. James Martin (1878 issue), "
        "as its title page reads", 1878, "University of Toronto (Robarts)", "NOT_IN_COPYRIGHT", (7, 507),
        [("Gen", 37, 420), ("Exod", 421, 507)]),
    "keil-delitzsch-pentateuch-2": _kd(
        "Biblical Commentary on the Old Testament: The Pentateuch, vol. II", "Keil, Pent. II", _KDP,
        "biblicalcomm02keiluoft", "314975d9d073558e6a5382f4f48d5b26273e101c5b6a76fb9559775efc4583de",
        f"{_KD}, vol. II: The Pentateuch (Exodus xii.-xl.; Leviticus), by C. F. Keil, tr. James Martin (1872), "
        "as its title page reads", 1872, "University of Toronto (Emmanuel College)", "NOT_IN_COPYRIGHT", (8, 489),
        [("Exod", 12, 263), ("Lev", 264, 489)]),
    "keil-delitzsch-pentateuch-3": _kd(
        "Biblical Commentary on the Old Testament: The Pentateuch, vol. III", "Keil, Pent. III", _KDP,
        "pentateuch03keiluoft", "9e0b0189d5a0806fabbaa733a673c6888e49ec00c8da01f442ca260225b59f04",
        f"{_KD}, vol. III: The Pentateuch (Numbers; Deuteronomy), by C. F. Keil, tr. James Martin (1871), "
        "as its title page reads", 1871, "University of Toronto (Robarts)", "NOT_IN_COPYRIGHT", (8, 544),
        [("Num", 14, 281), ("Deut", 282, 529)]),
    "delitzsch-psalms-1": _kd(
        "Biblical Commentary on the Psalms, vol. I", "Delitzsch, Ps. I", "Franz Delitzsch",
        "commentarypsalm01deliuoft", "dcd1104005b32e8a3ac96a84b400719f55a7848bac5dbaa39a55b25aa805c787",
        f"{_KD}: Franz Delitzsch, Biblical Commentary on the Psalms, vol. I (Ps. i.-xxxv.), tr. Francis Bolton "
        "(1880 issue), as its title page reads", 1880, "Trinity College, Toronto", "NOT_IN_COPYRIGHT", (8, 447),
        [("Ps", 100, 447)]),
    "delitzsch-psalms-2": _kd(
        "Biblical Commentary on the Psalms, vol. II", "Delitzsch, Ps. II", "Franz Delitzsch",
        "biblicalcommenta187102deli", "f453ad2a67b60934f86336d9ce461d039cf407245d29e5abb902805211a29f3a",
        f"{_KD}: Franz Delitzsch, Biblical Commentary on the Psalms, vol. II (Ps. xxxvi.-lxxxiii.), tr. Francis "
        "Bolton (1871), as its title page reads", 1871, "Princeton Theological Seminary Library", "NOT_IN_COPYRIGHT",
        (7, 432), [("Ps", 13, 423)]),
    "delitzsch-psalms-3": _kd(
        "Biblical Commentary on the Psalms, vol. III", "Delitzsch, Ps. III", "Franz Delitzsch",
        "commentarypsalm03deliuoft", "ce83fe38fb61611a348f998a612776e990e62e5f015082fdcffb0a5787f0d8f9",
        f"{_KD}: Franz Delitzsch, Biblical Commentary on the Psalms, vol. III (Ps. lxxxiv.-cl.), tr. Francis Bolton "
        "(second edition of the translation, 1881), as its title page reads", 1881, "Trinity College, Toronto", "NOT_IN_COPYRIGHT", (4, 431),
        [("Ps", 12, 427)]),
}
# How each scan was chosen, carried into the manifest (scheme.scan_choice), so a reader of the manifest
# sees the other witnesses without opening this file.
SCAN_CHOICE = {
    "alford-commentary-2": "Lane A's item (same scan); measured against greektestamentwiptsl02alfo (1899): "
                           "Greek 17.3% vs 17.1% of letters, Greek tokens known 34.1% vs 34.8%: not clearly better",
    "alford-commentary-3": "greektestamentwi00alfo (4th ed., 1865; Lane A has no vol. III): Greek 15.4%, known 35.5%; "
                           "greektestamentw03alfo 15.8%/35.5% is a catalogue-1849 copy of unstated edition",
    "alford-commentary-4": "Lane A's item (same scan); measured against greektestamentwi5604alfo (3rd ed., 1866): "
                           "Greek 14.0% vs 13.6%, known 35.7% vs 35.5%",
    "bengel-gnomon-2": "gnomonofnewtesta23beng (vols. II and III bound as one): Greek 6.3%, known 34.4%; "
                       "cu31924092350523 (1877, vol. II) 5.9%/33.1%",
    "bengel-gnomon-3": "gnomonofnewtesta23beng (vols. II and III bound as one); cu31924092350499 (1877, vol. III): "
                       "0.0% Greek",
    "bengel-gnomon-4": "cu31924092350507 (1877): Greek 7.5%, known 32.4%; gnomonofnewtesta03benguoft (1873): 0.0% Greek",
}
# the chapter a volume's notes on a book begin at, where an earlier volume holds the book's start
FIRST_CHAPTER = {"keil-delitzsch-pentateuch-2": {"Exod": 12}, "delitzsch-psalms-2": {"Ps": 36},
                 "delitzsch-psalms-3": {"Ps": 84}}
for _k in SECOND:
    if _k in SCAN_CHOICE:
        SECOND[_k]["scan_choice"] = SCAN_CHOICE[_k]
    if _k in FIRST_CHAPTER:
        SECOND[_k]["first_chapter"] = FIRST_CHAPTER[_k]
SCANS.update(SECOND)
# Each scan's Internet Archive `date`, as its metadata gives it (fetch()
# stops if it changes), and why it differs from the year the title page
# prints, where it does.
IA_DATES_2B = {
    "greektestamentwi02alfo": ("1856", "IA catalogues it 1856; the title page reads 1857"),
    "greektestamentwi00alfo": ("1865", None),
    "greektestamentwi04alfo": ("1874", None),
    "gnomonofnewtesta23beng": ("1873", None),
    "cu31924092350507": ("1877", None),
    "thepentateuch01keiluoft": ("1871-1878", "IA dates the whole set; this volume's title page reads 1878"),
    "biblicalcomm02keiluoft": ("1869-", "IA dates the set from 1869; this volume's title page reads 1872"),
    "pentateuch03keiluoft": ("1871-1878", "IA dates the whole set; this volume's title page reads 1871"),
    "commentarypsalm01deliuoft": ("1880-1881", "IA dates the set; this volume's title page reads 1880"),
    "biblicalcommenta187102deli": ("1871", None),
    "commentarypsalm03deliuoft": ("1880-1881", "IA dates the set; this volume's title page reads 1881"),
}
for _s in SECOND.values():
    _d, _why = IA_DATES_2B[_s["ia"]]
    _s["ia_date"] = _d
    if _why:
        _s["ia_date_note"] = _why
ORDER.extend(SECOND)
MULTI.update(k for k, s in SECOND.items() if len(s["epistles"]) > 1)

# ================================================================== Keil & Delitzsch: the rest of the set (4c)
#
# The other volumes of T. & T. Clark's Biblical Commentary on the Old Testament, read by the same `kd`
# reader.
# Every candidate scan measured 2026-10-03 on its _djvu.txt (Hebrew / Greek letters as a share of all
# letters; English tokens of 3+ letters found in the dwyl word list; 'Ver.' openers as kd_cands reads
# them, line by line; hOCR present or not). No scan of any volume keeps its Hebrew (0.00% in every one).
# The Brigham Young set (biblicalcommenta00keil01 ... 07keil07, IA date '1900') is Eerdmans' photographic
# reprint (its own leaves read "Reprinted, November 1986"): refused, not printed before 1929. The
# india.history.resource.* items carry no rights field, no contributor and no page count: used only
# as measures. Cornell's 1878 set (cu3192407068xxxx) has hOCR for only some volumes; where it has none,
# it is a measure only.
#   Joshua, Judges, Ruth  joshuajudgesruth04keil 1875 (Robarts) 94.2%  789 Ver.   <- chosen
#               biblicalcommenta04keiluoft 1882 (Emmanuel; IA titles it Job) 94.0% 783; biblicalcomm04keiluoft
#               1869- (Robarts) 93.6% 745; joshuajudgesruth1872keil 94.2% 783, joshuajudgesrut00keilgoog 1865
#               94.1% 783, joshuajudgesruth1880keil 93.2% 759; cu31924070685734 93.0% 704; india...72625 94.0% 750
#   Samuel      biblicalcomment00keiluoft 1880 (Trinity) 95.0%  915 Ver.   <- chosen
#               commentarysamuel00keiluoft 1880 (Trinity) 94.9% 907; biblicalcommen00keil 1876 (Robarts) 94.9% 912;
#               biblicalcomment00keil 1872 94.4% 902; biblicalcommenta68keil 1868 94.2% 898; cu31924052268087
#               1891 94.3% 894; cu31924070685742 94.6% 884; india...72628 94.5% 888
#   Kings       thebooksofthekin00keiluoft 1883 (Emmanuel; 2nd ed.) 93.6%  841 Ver.   <- chosen
#               booksofkings00bhuoft 1872 (Robarts) 93.1% 649; booksofkings00keil 1872 93.4% 778;
#               bookskingstrbyj00keilgoog 1872 91.2% 347
#   Chronicles  booksofchronicle00keiluoft 1878 (Robarts) 93.1%  772 Ver.   <- chosen
#               booksofchronicle00keiliala 1872 93.5% 783 (not clearly better; not Toronto); booksofchronicle00keil
#               1872 93.2% 770; bookschronicles00keilgoog 1872 91.7% 416; cu31924070685767 92.9% 758; india...72634
#   Ezra, Nehemiah, Esther  booksofezranehem00keil 1873 (Princeton) 93.3%  521 Ver.   <- chosen (no Toronto scan)
#               booksofezranehem1888keil 1888 92.6% 515; booksezranehemi00keilgoog, cu31924058517529,
#               cu31924070685775: no hOCR; india...72636 93.5% 508
KD4C = {
    "keil-delitzsch-joshua-judges-ruth": _kd(
        "Biblical Commentary on the Old Testament: Joshua, Judges, Ruth", "Keil, Josh.-Ruth", _KDP,
        "joshuajudgesruth04keil", "4b0cb6d3360799a7228cd3fac29245621530e78e4c9f60e8829d39d48f2f295f",
        f"{_KD}, vol. IV: Joshua, Judges, Ruth, by C. F. Keil and F. Delitzsch, tr. James Martin (1875 issue), "
        "as its title page reads", 1875, "University of Toronto (Robarts)", None, (7, 508),
        [("Josh", 39, 248), ("Judg", 261, 478), ("Ruth", 484, 508)]),
    "keil-delitzsch-samuel": _kd(
        "Biblical Commentary on the Books of Samuel", "Keil, Sam.", _KDP,
        "biblicalcomment00keiluoft", "1560a2ea753736b564e2f5bc7e9fbe87e392865cab9eb780512ee86eee6c2679",
        f"{_KD}: C. F. Keil, Biblical Commentary on the Books of Samuel, tr. James Martin (1880 issue), "
        "as its title page reads", 1880, "University of Toronto (Trinity College)", "NOT_IN_COPYRIGHT", (6, 523),
        [("1Sam", 24, 293), ("2Sam", 294, 523)]),
    "keil-delitzsch-kings": _kd(
        "Biblical Commentary on the Books of the Kings", "Keil, Kings", _KDP,
        "thebooksofthekin00keiluoft", "6097e3f6bd3c190d18773c479b7fc86e9883e6647423e771af77869409b462d0",
        f"{_KD}: C. F. Keil, The Books of the Kings, tr. James Martin, second edition (1883), as its title page "
        "reads", 1883, "University of Toronto (Emmanuel College)", "NOT_IN_COPYRIGHT", (6, 534),
        [("1Kgs", 26, 294), ("2Kgs", 295, 534)]),
    "keil-delitzsch-chronicles": _kd(
        "Biblical Commentary on the Books of the Chronicles", "Keil, Chron.", _KDP,
        "booksofchronicle00keiluoft", "2beebc8ca2a4d11ef5ad17946c43a6a7ec938bffacaaf2363fcb5670a3d835c5",
        f"{_KD}: C. F. Keil, The Books of the Chronicles, tr. Andrew Harper (1878), as its title page reads",
        1878, "University of Toronto (Robarts)", "NOT_IN_COPYRIGHT", (6, 527),
        [("1Chr", 58, 313), ("2Chr", 314, 527)]),
    "keil-delitzsch-ezra-nehemiah-esther": _kd(
        "Biblical Commentary on the Books of Ezra, Nehemiah, and Esther", "Keil, Ezra-Esth.", _KDP,
        "booksofezranehem00keil", "8ceaeab881449655839e75e65844b072bc4f370896968dc07cae8f5ad5ad4d05",
        f"{_KD}: C. F. Keil, The Books of Ezra, Nehemiah, and Esther, tr. Sophia Taylor (1873), as its title page "
        "reads", 1873, "Princeton Theological Seminary Library", "NOT_IN_COPYRIGHT", (11, 396),
        [("Ezra", 35, 152), ("Neh", 170, 314), ("Esth", 335, 396)]),
}
# how each was chosen (scheme.scan_choice), and each item's IA `date` (fetch() stops if it changes)
KD4C_CHOICE = {
    "keil-delitzsch-joshua-judges-ruth": "joshuajudgesruth04keil (Toronto, 1875): English 94.2%, 789 'Ver.' openers; "
                                         "biblicalcommenta04keiluoft (Toronto, 1882) 94.0%/783 and "
                                         "biblicalcomm04keiluoft (Toronto, 1869) 93.6%/745",
    "keil-delitzsch-samuel": "biblicalcomment00keiluoft (Toronto, 1880): English 95.0%, 915 'Ver.' openers; "
                             "commentarysamuel00keiluoft (the same issue) 94.9%/907, biblicalcommen00keil (Toronto, "
                             "1876) 94.9%/912",
    "keil-delitzsch-kings": "thebooksofthekin00keiluoft (Toronto, 1883, 2nd ed.): English 93.6%, 841 'Ver.' openers; "
                            "booksofkings00bhuoft (Toronto, 1872) 93.1%/649, booksofkings00keil (1872) 93.4%/778",
    "keil-delitzsch-chronicles": "booksofchronicle00keiluoft (Toronto, 1878): English 93.1%, 772 'Ver.' openers; "
                                 "booksofchronicle00keiliala (1872) 93.5%/783 is not clearly better",
    "keil-delitzsch-ezra-nehemiah-esther": "booksofezranehem00keil (Princeton, 1873; no Toronto scan): English 93.3%, "
                                           "521 'Ver.' openers; booksofezranehem1888keil 92.6%/515; the Oxford and "
                                           "Cornell scans have no hOCR",
}
KD4C_IA_DATES = {
    "joshuajudgesruth04keil": ("1875", None),
    "biblicalcomment00keiluoft": ("1880", None),
    "thebooksofthekin00keiluoft": ("1883", None),
    "booksofchronicle00keiluoft": ("1878", None),
    "booksofezranehem00keil": ("1873", None),
}
# The prophets: Jeremiah and Lamentations (2 vols), Ezekiel (2 vols), Daniel, the Minor Prophets (2 vols);
# the candidates measured are in KD4C_CHOICE. The Ezekiel scans bind Andrews' Life of Christ after the
# commentary: those leaves are outside the volume's range.
KD4C.update({
    "keil-delitzsch-jeremiah-1": _kd(
        "Biblical Commentary on the Prophecies of Jeremiah, vol. I", "Keil, Jer. I", _KDP,
        "propheciesofjere01keil", "e609bff9112327710351175b3308258e17b7e06ac6094e8aff100a25badc18a3",
        f"{_KD}: C. F. Keil, The Prophecies of Jeremiah, vol. I (chap. i.-xxix.), tr. David Patrick (1880 issue), "
        "as its title page reads", 1880, "Princeton Theological Seminary Library", "NOT_IN_COPYRIGHT", (9, 433),
        [("Jer", 51, 433)]),
    "keil-delitzsch-jeremiah-2": _kd(
        "Biblical Commentary on the Prophecies of Jeremiah, vol. II", "Keil, Jer. II", _KDP,
        "propheciesofjere02keil", "8e714e17e98bb401fe5621a55a38ecd5310adb81efb8ade970e071878423a342",
        f"{_KD}: C. F. Keil, The Prophecies of Jeremiah, vol. II (chap. xxx.-lii.; Lamentations), tr. James "
        "Kennedy (1874), as its title page reads", 1874, "Princeton Theological Seminary Library", "NOT_IN_COPYRIGHT",
        (7, 467), [("Jer", 13, 343), ("Lam", 367, 467)]),
    "keil-delitzsch-ezekiel-1": _kd(
        "Biblical Commentary on the Prophecies of Ezekiel, vol. I", "Keil, Ezek. I", _KDP,
        "biblicalcommenta01keiluoft", "ecec4e81ffab2306a5f2eb729290db4f3c3891d5f8218a940b403e032af07f6d",
        f"{_KD}: C. F. Keil, Biblical Commentary on the Prophecies of Ezekiel, vol. I (chap. i.-xxviii.), tr. "
        "James Martin (1876), as its title page reads", 1876, "University of Toronto (Robarts)", "NOT_IN_COPYRIGHT",
        (8, 443), [("Ezek", 32, 443)]),
    "keil-delitzsch-ezekiel-2": _kd(
        "Biblical Commentary on the Prophecies of Ezekiel, vol. II", "Keil, Ezek. II", _KDP,
        "biblicalcommenta02keiluoft", "c20737e357a7f3f1647ab1a79fc7131e3be1ea5d1becaf09e56dd14743bf3f7d",
        f"{_KD}: C. F. Keil, Biblical Commentary on the Prophecies of Ezekiel, vol. II (chap. xxix.-xlviii.), tr. "
        "James Martin (1876), as its title page reads", 1876, "University of Toronto (Emmanuel College)", None,
        (6, 459), [("Ezek", 14, 459)]),
    "keil-delitzsch-daniel": _kd(
        "Biblical Commentary on the Book of Daniel", "Keil, Dan.", _KDP,
        "bookofprophetdan00keil", "51ab5c80ff5a5c6c39f20cb3928c0f0b30001aec7fb0ff7dafc86a664826df62",
        f"{_KD}: C. F. Keil, The Book of the Prophet Daniel, tr. M. G. Easton (1872), as its title page reads",
        1872, "Princeton Theological Seminary Library", "NOT_IN_COPYRIGHT", (7, 526), [("Dan", 76, 526)]),
    "keil-delitzsch-minor-prophets-1": _kd(
        "Biblical Commentary on the Twelve Minor Prophets, vol. I", "Keil, Min. Proph. I", _KDP,
        "thetwelveminorp01keiluoft", "f781e60b1c64f5c28c7684983c2b2469bdbc20a6fdbcb12e471fbbaa3e79b971",
        f"{_KD}: C. F. Keil, The Twelve Minor Prophets, vol. I (Hosea to Micah), tr. James Martin (1878 issue), "
        "as its title page reads", 1878, "University of Toronto (Robarts)", "NOT_IN_COPYRIGHT", (4, 526),
        [("Hos", 38, 178), ("Joel", 190, 243), ("Amos", 251, 347), ("Obad", 361, 389), ("Jonah", 400, 428),
         ("Mic", 436, 526)]),
    "keil-delitzsch-minor-prophets-2": _kd(
        "Biblical Commentary on the Twelve Minor Prophets, vol. II", "Keil, Min. Proph. II", _KDP,
        "thetwelveminorpr02keiluoft", "44995dcbef39e0e8ca4548baa1551cc211dd5634897dfeb85b3ef06367667092",
        f"{_KD}: C. F. Keil, The Twelve Minor Prophets, vol. II (Nahum to Malachi), tr. James Martin (1878 issue), "
        "as its title page reads", 1878, "University of Toronto (Robarts)", "NOT_IN_COPYRIGHT", (4, 486),
        [("Nah", 19, 59), ("Hab", 66, 127), ("Zeph", 137, 176), ("Hag", 185, 226), ("Zech", 234, 432),
         ("Mal", 440, 486)]),
})
KD4C_CHOICE.update({
    "keil-delitzsch-jeremiah-1": "propheciesofjere01keil (Princeton, 1880; no Toronto scan): English 94.8%, 895 'Ver.' "
                                 "openers; cu31924070685882 (Cornell) 93.9%/881 has no hOCR",
    "keil-delitzsch-jeremiah-2": "propheciesofjere02keil (Princeton, 1874; no Toronto scan): English 93.7%, 763 'Ver.' "
                                 "openers; cu31924070685890 (Cornell) 93.6%/750 has no hOCR; prophesiesofjere0002unse "
                                 "is a lending-library item (its text refused, HTTP 401)",
    "keil-delitzsch-ezekiel-1": "biblicalcommenta01keiluoft (Toronto, 1876): English 95.8%, 794 'Ver.' openers; "
                                "biblicalcommenta00keiluoft (Toronto) 95.4%/808, biblicalcommenta01keil (Princeton) "
                                "94.4%/794",
    "keil-delitzsch-ezekiel-2": "biblicalcommenta02keiluoft (Toronto, 1876): English 96.0%, 619 'Ver.' openers; "
                                "india.history.resource.78885 95.6%/613; cu31924070685908/-916 (Cornell): no hOCR",
    "keil-delitzsch-daniel": "bookofprophetdan00keil (Princeton, 1872; no Toronto scan): English 93.6%, 280 'Ver.' "
                             "openers; cu31924070689447 (Cornell, 1878) 93.6%/284 is not clearly better",
    "keil-delitzsch-minor-prophets-1": "thetwelveminorp01keiluoft (Toronto, 1878): English 95.5%, 610 'Ver.' openers; "
                                       "cu31924070689454 (Cornell) 94.4%/595, india.history.resource.78876 (1868) "
                                       "94.7%/580",
    "keil-delitzsch-minor-prophets-2": "thetwelveminorpr02keiluoft (Toronto, 1878): English 95.2%, 508 'Ver.' openers; "
                                       "cu31924070689462 (Cornell) 94.0%/493, india.history.resource.72629 (1868) "
                                       "94.4%/487",
})
KD4C_IA_DATES.update({
    "propheciesofjere01keil": ("1874-1880 [v. 1, 1880]", "IA dates the set; this volume's title page reads 1880"),
    "propheciesofjere02keil": ("1874-1880 [v. 1, 1880]", "IA dates the set, naming vol. I's 1880; this volume's "
                                                         "title page reads 1874"),
    "biblicalcommenta01keiluoft": ("1876", None),
    "biblicalcommenta02keiluoft": ("1876", None),
    "bookofprophetdan00keil": ("1872", None),
    "thetwelveminorp01keiluoft": ("1878", None),
    "thetwelveminorpr02keiluoft": ("1878", None),
})
KD4C_HONESTY = (
    "a running head naming a chapter below the median of the five headed leaves before it or above the median "
    "of the five after it is dropped as misread (measure.running_heads_out_of_order); an opener the sequence "
    "refuses for a verse already passed inside the section the chapter's latest run opened ('Ver. 20.' "
    "after 'Ver. 25.' under 'Vers. 20-25.', where a section's translation is followed by its exposition) reopens that verse's unit, its text joining that unit, which "
    "is then not contiguous in the print (measure.notes_reopened), or, where the verse has none yet, opens it "
    "without moving the sequence (measure.notes_opened_behind)")
# a volume continuing a book starts its notes where the volume before left off
KD4C_FIRST_CHAPTER = {"keil-delitzsch-jeremiah-2": {"Jer": 30}, "keil-delitzsch-ezekiel-2": {"Ezek": 29}}
for _k, _s in KD4C.items():
    _s["scan_choice"] = KD4C_CHOICE[_k]
    _s["monotone_heads"] = True     # a misread head ('XL' for 'XI') must not carry the notes 29 chapters on
    _s["reopen"] = True             # 'Ver. 20.' after 'Ver. 25.': the exposition after the translation
    _s["honesty"] = KD4C_HONESTY
    if _k in KD4C_FIRST_CHAPTER:
        _s["first_chapter"] = KD4C_FIRST_CHAPTER[_k]
    _s["ia_date"], _why = KD4C_IA_DATES[_s["ia"]]
    if _why:
        _s["ia_date_note"] = _why
SECOND.update(KD4C)
SCANS.update(KD4C)
ORDER.extend(KD4C)
MULTI.update(k for k, s in KD4C.items() if len(s["epistles"]) > 1)

# ------------------------------------------------------------------ second shelf: Alford's page

ALF_APP = {"rec", "om", "ins", "txt", "bef", "aft", "rel", "latt", "vss", "syrr", "copt", "arm", "eth", "aeth",
           "vulg", "al", "chr", "thdrt", "lat-ff", "goth", "syr", "it", "elz", "lachm", "tischdf"}


def alford_layout(a, W):
    """Alford's page: the Greek text (with its marginal references), the
    digest of readings under it, then the notes in two columns. The columns
    are the largest cluster of side-by-side line pairs; everything above them
    is text or digest; the digest begins at the first line that reads like it
    (a verse number, or the digest's sigla: rec, om, txt, ins...)."""
    body = a["body"]
    box = text_box(body)
    if not box:
        return None
    x0, x1 = box
    cx, tw = (x0 + x1) / 2, x1 - x0
    slack = 0.02 * W
    left = [l for l in body if l["bbox"][2] < cx + slack]
    right = [l for l in body if l["bbox"][0] > cx - slack]
    wide = lambda l: l["bbox"][2] - l["bbox"][0] > 0.3 * tw  # noqa: E731
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
    lh = st.median([l["bbox"][3] - l["bbox"][1] for pr in pairs for l in pr])
    pairs.sort(key=lambda pr: pr[0]["bbox"][1])
    clusters = [[pairs[0]]]
    for pr in pairs[1:]:
        if pr[0]["bbox"][1] - clusters[-1][-1][0]["bbox"][1] > 3.5 * lh:
            clusters.append([])
        clusters[-1].append(pr)
    zone = max(reversed(clusters), key=len)
    if len(zone) < 4:
        return None
    note_xs = st.median([l["xs"] for pr in zone for l in pr])
    y_tc = min(min(l["bbox"][1], r["bbox"][1]) for l, r in zone)
    cols = [l for l in left + right if l["bbox"][1] >= y_tc - 0.3 * note_xs]
    zone_end = max(l["bbox"][3] for l in cols)
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
            cols_l.append(l)
    prose = [l for l in above if sum(w[5].lower().strip(".,;:") in STOP for w in l["words"]) >= 3]
    if len(prose) >= 4:
        return None                     # prose above two columns: a prolegomena page with footnotes
    above.sort(key=lambda l: l["bbox"][1])
    start = None
    for l in above:
        toks = [w[5].lower().strip(".,;:()[]") for w in l["words"]]
        sig = sum(t in ALF_APP for t in toks)
        if l["bbox"][2] - l["bbox"][0] > 0.5 * tw and (sig >= 2 or (re.match(r'\s*\d{1,2}\.\s', l["text"]) and sig >= 1)):
            start = l["bbox"][1]
            break
    text = [l for l in above if start is None or l["bbox"][1] < start]
    app = [l for l in above if start is not None and l["bbox"][1] >= start]
    return {"text": text, "apparatus": app, "left": C.merge_rows(cols_l), "right": C.merge_rows(cols_r),
            "tail": tail, "note_xs": note_xs}


ALF_OPEN = re.compile(r'(?<![\w.,;:\-])(?:([IVX]{1,5})\.\s*)?(\d{1,2})((?:\s*[,—–\-]+\s*\d{1,2}){0,3})\s?\.\s?'
                      r'(?:[\]\)\}\|]|[17J]{1,2}(?=\s)|(?=\s?[Ͱ-Ͽἀ-῿]))')
ALF_ABBR = {"ver", "vv", "vers", "ch", "chap", "c", "p", "pp", "cf", "see", "comp", "ib", "ibid", "l", "ll", "sect",
            "§", "v", "ff", "art", "no", "fol", "col", "bk", "lib", "ed", "vol", "n", "note", "and", "&"}


def alford_cands(text, prev):
    """Inline verse openers in a line of Alford's notes ('9.] As we said',
    '5. ᾧ ἡ δόξα', '6—10.| ANNOUNCEMENT'): [(pos, (chapter or None, n, end, how))].
    A number counts only after the end of a clause and not after a numeral or
    a reference's abbreviation ('Rom. ix. 3.' 'ver. 8.' are references)."""
    out = []
    for m in ALF_OPEN.finditer(text):
        before = (prev + " " + text[:m.start()]).rstrip()
        if before:
            if before[-1] not in ".)]};:!?’”\"'—|·":
                continue
            w = before.split()[-1].strip(".,;:()[]{}’‘'\"")
            if re.fullmatch(r'[ivxlcIVXLC]+|\d+', w) or w.lower() in ALF_ABBR:
                continue
        n = int(m.group(2))
        run = re.findall(r'\d{1,2}', m.group(3) or "")
        e = int(run[-1]) if run and int(run[-1]) > n else None
        cp = FS.roman(m.group(1)) if m.group(1) else None
        if n == 0 or (m.group(1) and not cp):
            continue
        out.append((m.start(), (cp, n, e, "read")))
    return out


ALF_ROMAN = str.maketrans({"Ι": "I", "Χ": "X", "Υ": "V", "l": "I", "1": "I", "|": "I"})


def alford_head(a, nch):
    """(chapter, verse numbers) of an Alford running head: its roman chapter
    stands alone or before the verses ('IV. 15—18.'), read only from the
    letters a roman numeral can have."""
    if nch == 1:
        return 1, head_verses(a["head"])
    for piece in re.split(r'\s*\|\s*|\s{2,}', a["head"]):
        for m in re.finditer(r'(?<![\w])([IVXΙΧΥl1|]{1,6})(?![A-Za-zͰ-Ͽἀ-῿])[.,:]?\s*((?:\d{1,2}\s*[—–\-,.]*\s*){0,3})', piece):
            tok = m.group(1).translate(ALF_ROMAN)
            if not re.fullmatch(r'[IVX]+', tok) or (tok == "I" and not m.group(1) in ("I", "Ι")):
                continue
            c = FS.roman(tok)
            if c and 1 <= c <= nch:
                return c, [int(x) for x in re.findall(r'\d{1,2}', m.group(2) or "")]
    return None, []

# ------------------------------------------------------------------ second shelf: the single-column page


def sc_page(p):
    """A single-column page (Bengel, Keil & Delitzsch): its running head,
    folio, body lines with whether each opens a paragraph, and the footnote
    block at the foot (smaller type), as (head, nums, body, foot, junk)."""
    L = [l for l in p["lines"] if l["words"] and l["text"].strip()]
    if not L:
        return "", [], [], [], 0
    many = [l for l in L if len(l["words"]) >= 4]
    med = st.median([l["xs"] for l in many]) if many else None
    medh = st.median([l["bbox"][3] - l["bbox"][1] for l in many]) if many else None
    L.sort(key=lambda l: l["bbox"][1])
    head = []
    if len(L) > 1 and len(L[0]["words"]) <= 10 and L[0]["bbox"][1] < 0.12 * p["h"]:
        t = L[0]
        letters = [c for c in t["text"] if c.isalpha()]
        if letters and sum(c.isupper() for c in letters) >= 0.5 * len(letters):
            head = [l for l in L if l["bbox"][1] < t["bbox"][3] - 0.3 * (t["bbox"][3] - t["bbox"][1])]
    rest = [l for l in L if l not in head]
    nums = []
    for l in head:
        for tok in l["text"].split():
            if re.fullmatch(r'\d{1,3}', tok) and (tok is l["text"].split()[0] or tok is l["text"].split()[-1]):
                nums.append(int(tok))
    # signature marks and a lone folio at the foot
    sig = [l for l in rest if l["bbox"][1] > 0.9 * p["h"] and len(l["words"]) <= 6
           and (re.fullmatch(r'[\W\d]*\d{1,3}[\W]*', l["text"].strip()) or re.search(r'VOL\.', l["text"]))]
    for l in sig:
        if re.fullmatch(r'\d{1,3}', l["text"].strip()):
            nums.append(int(l["text"].strip()))
    rest = [l for l in rest if l not in sig]
    junk = [l for l in rest if not any(c.isalnum() for c in l["text"])]
    rest = [l for l in rest if l not in junk]
    foot = []
    wh = lambda l: st.median([w[3] - w[1] for w in l["words"]])  # noqa: E731  (the type's height, per line)
    medw = st.median([wh(l) for l in many]) if many else None
    if medh:
        small = lambda l: wh(l) < 0.9 * medw or (med and l["xs"] < 0.88 * med)  # noqa: E731
        for l in reversed(rest):
            if small(l) or (foot and len(l["words"]) < 4):
                foot.insert(0, l)
            else:
                break
        while foot and not small(foot[0]):
            foot.pop(0)
        if len(foot) == len(rest):
            foot = []                   # a page all in small type is text, not footnotes
    body = [l for l in rest if l not in foot]
    xs0 = sorted(l["bbox"][0] for l in body if len(l["words"]) >= 4)
    mg = xs0[len(xs0) // 5] if xs0 else 0
    em = med or 40
    out = [(l, 0.6 * em <= l["bbox"][0] - mg <= 4.5 * em) for l in body]
    return " | ".join(l["text"] for l in sorted(head, key=lambda l: l["bbox"][0])), nums, out, foot, len(junk)


HEAD_ROMAN = str.maketrans({"Ι": "I", "Χ": "X", "Υ": "V", "l": "I", "|": "I"})


def sc_head(head, nch):
    """(chapter, verse numbers) of a single-column running head: 'CHAP. L.
    15-21.', 'PSALM XXXV. 1—3.', 'ST JOHN IV. 7-10.', 'EPHESIANS IV. 14, 15.'"""
    t = head.translate(HEAD_ROMAN)
    for m in re.finditer(r'(?<![A-Za-z])([IVXLC]{1,8})(?![A-Za-z])[.,:]?((?:\s*\d{1,3}\s*[—–\-,.]*){0,4})', t):
        c = FS.roman(m.group(1))
        if c and 1 <= c <= nch:
            vs = [int(x) for x in re.findall(r'\d{1,3}', m.group(2) or "") if int(x) <= 180]
            return c, vs
    if nch == 1:
        return 1, [int(x) for x in re.findall(r'\b\d{1,2}\b', t)]
    return None, []


BENGEL_OPEN = re.compile(r'^[‘“"\'(]?(?:([IVX]{1,5})\.\s*)?(\d{1,2})((?:\s*(?:[,—–\-]+|\s+and)\s*\d{1,2}){0,4})'
                         r'\s*[.,]\s*\d?\s*(?=[^\d\s])')
KD_OPEN = re.compile(r'[‘“"\'(]?(?:[VY][eco]r?s?|Ver)\s?[.,]\s*(\d{1,3})'
                     r'((?:\s*(?:[,—–\-]+|\s+and)\s*\d{1,3}){0,6})(?:\s*sqq?\.?)?(?:\s*[.,:;]|\s+(?=[a-z]))')


def sc_cand(text, reader):
    """A verse number opening a paragraph (Bengel): '14. μηκέτι)', '7.1 °Ex
    τῆς'."""
    m = BENGEL_OPEN.match(text)
    if not m:
        return None
    cp = FS.roman(m.group(1)) if m.group(1) else None
    if m.group(1) and not cp:
        return None
    n, run = int(m.group(2)), m.group(3)
    nums = [int(x) for x in re.findall(r'\d{1,2}', run or "")]
    e = nums[-1] if nums and nums[-1] > n else None
    return (cp, n, e, "read") if n else None


def kd_cands(text):
    """Keil & Delitzsch's section openers: 'Ver. 3.', 'Vers. 14-19.', 'Vers.
    9-12 contain', with a capital V (a reference inside a sentence is 'ver.
    3'), at the start of a line or after a dash or a sentence's end, where they
    run on inside a paragraph ('... rooted there. — Ver. 3. As Adam ...'):
    [(pos, (None, n, end, how))]."""
    out = []
    for m in KD_OPEN.finditer(text):
        before = text[:m.start()].rstrip()
        if before and before[-1] not in "—–-.;:!?)”\"'":
            continue
        n = int(m.group(1))
        nums = [int(x) for x in re.findall(r'\d{1,3}', m.group(2) or "")]
        e = nums[-1] if nums and nums[-1] > n else None
        if n:
            out.append((m.start(), (None, n, e, "read")))
    return out

PSALM_TITLE = re.compile(r'^\W{0,3}[PFr][SB]A[LI]M\s+([IVXLCl1]{1,9})[.,]?(?:\s*[-—–]\s*([IVXLCl1]{1,9})[.,]?)?\s*$')


def psalm_title(l, W, last):
    """Delitzsch's title line over each psalm ('PSALM XXXVI.', 'PSALM
    XLII.-XLIII.'), centred in the column: the psalm's number, read where it
    is the next psalm or a near one after the last read (a final I is often
    OCR'd as L: 'PSALM XLL'), else None."""
    m = PSALM_TITLE.match(l["text"])
    if not m or l["bbox"][0] < 0.15 * W:
        return None
    raw = m.group(1).replace("l", "I").replace("1", "I")
    for tok in (raw, raw[:-1] + "I" if raw.endswith("L") else None):
        n = FS.roman(tok) if tok else None
        if n and 1 <= n <= 150 and (last is None or last < n <= last + 3):
            return n
    return None

# ------------------------------------------------------------------ second shelf: numbering (Keil & Delitzsch)


_VMAP = None


def vmap():
    global _VMAP
    if _VMAP is None:
        import versification as V
        _VMAP = V.load()
    return _VMAP


def heb_counts(book):
    out = {}
    for k, n in vmap()["hebrew_chapters"].items():
        b, c = k.rsplit(".", 1)
        if b == book:
            out[int(c)] = n
    return out


def numbering_votes(pairs, ids):
    """Existence votes over (book, chapter, verse) as printed: a verse only the
    Hebrew (WLC) has is a vote for the Hebrew numbering, a verse only the KJV
    has a vote for the KJV's; a verse both have (or neither) says nothing."""
    heb = only_heb = only_kjv = 0
    for b, c, v in pairs:
        h = 1 <= v <= vmap()["hebrew_chapters"].get(f"{b}.{c}", 0)
        k = f"kjv:{b}.{c}.{v}" in ids
        if h and not k:
            only_heb += 1
        elif k and not h:
            only_kjv += 1
        heb += 1
    return {"read": heb, "only_hebrew": only_heb, "only_kjv": only_kjv}


def decide(v):
    """hebrew / kjv when one side has at least 5 votes and twice the other's;
    otherwise undecided (and then each reference is read where it exists)."""
    if v["only_hebrew"] >= 5 and v["only_hebrew"] >= 2 * v["only_kjv"]:
        return "hebrew"
    if v["only_kjv"] >= 5 and v["only_kjv"] >= 2 * v["only_hebrew"]:
        return "kjv"
    return "undecided"


def ot_link(b, c, v, numbering, ids, rule):
    """A link to an OT verse printed in `numbering` (hebrew / kjv / undecided).
    Undecided: a verse only one numbering has is read in it; a verse both have
    is resolved only where the two read it alike, else it stays unresolved with
    both candidates (never silently the KJV's)."""
    import versification as V
    osis = f"{b}.{c}.{v}"
    if numbering == "undecided":
        h = 1 <= v <= vmap()["hebrew_chapters"].get(f"{b}.{c}", 0)
        k = f"kjv:{osis}" in ids
        rule += "/undecided"
        if h and k:
            r = V.resolve(osis, vmap(), ids)
            if r.get("resolved") and r["target"] == f"kjv:{osis}" and "spans" not in r:
                return {"printed": osis, "target": f"kjv:{osis}", "resolved": True, "numbering": "either",
                        "rule": rule}
            heb = {"numbering": "hebrew", **({"target": r["target"]} if r.get("resolved") else {"why": r["why"]})}
            return {"printed": osis, "resolved": False, "numbering": "undecided",
                    "why": "the numbering is not measured here, and the Hebrew and the KJV read this verse differently",
                    "candidates": [{"numbering": "kjv", "target": f"kjv:{osis}"}, heb], "rule": rule}
        numbering = "hebrew" if (h and not k) else "kjv"
    if numbering == "hebrew":
        r = V.resolve(osis, vmap(), ids)
        out = {"printed": osis, "numbering": "hebrew", "rule": rule}
        out.update(r)
        return out
    t = f"kjv:{osis}"
    if t in ids:
        return {"printed": osis, "target": t, "resolved": True, "numbering": "kjv", "rule": rule}
    return {"printed": osis, "resolved": False, "numbering": "kjv", "why": "no such verse in the KJV", "rule": rule}


_OWN, _WORK = {}, {}


def work_numbering(book, ids):
    """How Keil & Delitzsch's commentary numbers `book`, measured from its own
    note ids: the existence votes of every `kd` volume holding the book,
    pooled (one volume rarely has enough differing verses; the set does).
    Undecided where no volume holds the book."""
    if book not in _WORK:
        tot = {"read": 0, "only_hebrew": 0, "only_kjv": 0}
        vols = []
        for k, s in SCANS.items():
            if s.get("reader") != "kd" or book not in [e[0] for e in s.get("epistles", [])]:
                continue
            if k not in _OWN:
                _OWN[k] = build_scan_2b(k, ids, votes_only=True)
            for f in tot:
                tot[f] += _OWN[k][book][f]
            vols.append(k)
        _WORK[book] = dict(tot, decision=decide(tot), volumes=vols)
    return _WORK[book]


def effective(decision, book, ids, rule, used=None):
    """A measured decision, or, where it is undecided, the work's own."""
    if decision != "undecided":
        return decision, rule
    if used is not None:
        used.add(book)
    return work_numbering(book, ids)["decision"], rule + "/work"

# ------------------------------------------------------------------ second shelf: the build


def build_scan_2b(slug, ids, votes_only=False):
    s = SCANS[slug]
    reader = s["reader"]
    P = pages(slug)
    a0, b0 = s["leaves"]
    seg = {}
    for book, x, y in s["epistles"]:
        for leaf in range(x, y + 1):
            seg[leaf] = book
    m = collections.Counter()
    units = []
    A = {leaf: analyse(P[leaf]) for leaf in range(a0, b0 + 1)}
    nums = {leaf: list(a["nums"]) for leaf, a in A.items()}
    SC = {}
    if reader != "alford":
        for leaf in range(a0, b0 + 1):
            SC[leaf] = sc_page(P[leaf])
            nums[leaf] = sorted(set(nums[leaf]) | set(SC[leaf][1]))
    pp = printed_pages(nums)
    kjv_counts = {book: verse_counts(ids, book) for book, _, _ in s["epistles"]}
    nch = {book: max(c) for book, c in kjv_counts.items()}
    items = []
    last_psalm = None
    for leaf in range(a0, b0 + 1):
        a = A[leaf]
        book = seg.get(leaf)
        if reader == "alford":
            m["junk_lines_dropped"] += a["junk"]
            lay = alford_layout(a, P[leaf]["w"]) if book else None
            if lay is None:
                if a["body"]:
                    units.append(page_unit(slug, s, leaf, a["body"], a, pp))
                    m["leaves_page"] += 1
                continue
            m["leaves_commentary"] += 1
            hc, hv = alford_head(a, nch[book])
            if lay["text"] or lay["apparatus"]:
                t = ""
                for l in lay["text"]:
                    t = C.join(t, l["text"])
                u = {"id": f"{slug}:leaf.{leaf}.text",
                     "ref": f"{s['short']}, " + (f"p. {pp[leaf][0]}" if leaf in pp else f"leaf {leaf}") + ", text",
                     "kind": "epistle-text", "book": book, "text": t, "links": [], "scan": {"leaves": [leaf]}}
                if lay["apparatus"]:
                    u["apparatus"] = " ".join(l["text"] for l in lay["apparatus"])
                if a["head"]:
                    u["scan"]["running_head"] = a["head"]
                if leaf in pp:
                    u["scan"]["printed_page"] = pp[leaf][0]
                units.append(u)
            prev = ""
            for col in (lay["left"], lay["right"]):
                for l in col:
                    items.append({"book": book, "leaf": leaf, "text": l["text"], "para": False,
                                  "cands": alford_cands(l["text"], prev), "hc": hc, "hv": hv})
                    prev = l["text"]
            if lay["tail"]:
                units.append(page_unit(slug, s, leaf, lay["tail"], a, pp, {"after_notes": True}))
                m["leaves_with_tail"] += 1
        else:
            head, _, body, foot, junk = SC[leaf]
            m["junk_lines_dropped"] += junk
            if not book:
                lines = [l for l, _ in body] + foot
                if lines:
                    aa = dict(a, head=head or a["head"])
                    units.append(page_unit(slug, s, leaf, lines, aa, pp))
                    m["leaves_page"] += 1
                continue
            m["leaves_commentary"] += 1
            hc, hv = sc_head(head, 150 if book == "Ps" else nch[book])
            hv = [v for v in hv if v not in SC[leaf][1]]          # not the folio
            prev = ""
            for l, para in body:
                ps = psalm_title(l, P[leaf]["w"], last_psalm) if book == "Ps" else None
                if ps:
                    last_psalm = ps
                    items.append({"book": book, "leaf": leaf, "text": l["text"], "para": True, "psalm": ps,
                                  "cands": [], "hc": hc, "hv": hv, "head": head})
                    m["psalm_titles_read"] += 1
                    continue
                if reader == "kd":
                    cands = kd_cands(l["text"])
                else:
                    c = sc_cand(l["text"], reader) if para else None
                    cands = [(0, c)] if c else []
                items.append({"book": book, "leaf": leaf, "text": l["text"], "para": para,
                              "cands": cands, "hc": hc, "hv": hv, "head": head})
                prev = l["text"]
            if foot:
                m["footnote_lines"] += len(foot)
                t = ""
                for l in foot:
                    t = C.join(t, l["text"])
                items.append({"book": book, "leaf": leaf, "text": t, "foot": True, "cands": [], "hc": hc, "hv": hv})
    if s.get("monotone_heads"):
        monotone_heads(items, m)
    # heads confirmed by the nearest headed leaves (a verso head may name only
    # the book): sure when a neighbour agrees, or the chapter lies between them
    headed = {}
    for it in items:
        if it["hc"] is not None:
            headed.setdefault(it["leaf"], (it["book"], it["hc"]))

    def near(leaf, book, step):
        for k in range(1, 4):
            h = headed.get(leaf + step * k)
            if h:
                return h[1] if h[0] == book else None
        return None
    for it in items:
        hn, hp = near(it["leaf"], it["book"], 1), near(it["leaf"], it["book"], -1)
        it["hc_next"] = hn
        it["hsure"] = it["hc"] is not None and (it["hc"] in (hn, hp) or (
            hn is not None and hp is not None and hp <= it["hc"] <= hn))
    # which numbering the volume's own verses are in (Keil & Delitzsch only)
    numbering = {}
    if reader == "kd":
        for book in kjv_counts:
            pairs = []
            seen_heads = set()
            for it in items:
                if it["book"] != book or it["hc"] is None:
                    continue
                if it["leaf"] not in seen_heads:
                    seen_heads.add(it["leaf"])
                    pairs += [(book, it["hc"], v) for v in it["hv"]]
                pairs += [(book, it["hc"], o[1]) for _, o in it["cands"]]
                pairs += [(book, it["hc"], o[2]) for _, o in it["cands"] if o[2]]
            v = numbering_votes(pairs, ids)
            v["decision"] = decide(v)
            numbering[book] = v
        if votes_only:
            return numbering
        _OWN[slug] = {b: dict(v) for b, v in numbering.items()}
        m["numbering_own"] = numbering
    counts = {}
    for book in kjv_counts:
        if numbering.get(book, {}).get("decision") == "hebrew":
            counts[book] = heb_counts(book)
        elif numbering.get(book, {}).get("decision") == "undecided":
            hc_ = heb_counts(book)
            counts[book] = {c: max(n, hc_.get(c, 0)) for c, n in kjv_counts[book].items()}
        else:
            counts[book] = kjv_counts[book]
    decoders = {}
    for book in counts:
        d = HeadDecoder(counts[book])
        if reader == "kd":
            d.GAP, d.USE_HV = 30, False     # K&D's heads give the page's verses, not a bound on the notes
        d.c = s.get("first_chapter", {}).get(book, 1)     # a volume continuing a book starts where it does
        decoders[book] = d
    notes = decode_2b(slug, items, decoders, pp, m)
    for key, nu in notes.items():
        book = nu["book"]
        if nu["c"] is None:
            ref, links = f"{note_ref(s, book)}, before the first note", []
        elif nu.get("intro"):
            ref, links = f"{note_ref(s, book)} {nu['c']}, introduction", []
        else:
            vs = range(nu["n"], (nu["e"] or nu["n"]) + 1)
            nb = numbering.get(book, {}).get("decision")
            if nb:                  # an OT volume: its numbering measured, the Hebrew mapped
                nb = effective(nb, book, ids, "")[0]
                links = [dict(ot_link(book, nu["c"], v, nb, ids, "comments-on"), type="comments-on") for v in vs]
                for lk in links:
                    lk.pop("rule", None)
            else:
                links = [{"target": f"kjv:{book}.{nu['c']}.{v}", "type": "comments-on",
                          "resolved": f"kjv:{book}.{nu['c']}.{v}" in ids} for v in vs]
            ref = note_ref(s, book, nu["c"], nu["n"], nu["e"])
        u = {"id": f"{slug}:{key}", "ref": ref, "kind": "intro" if nu.get("intro") else "note", "book": book,
             "text": nu["text"], "links": links, "scan": {"leaves": nu["leaves"]}}
        if nu["pages"]:
            u["scan"]["printed_pages"] = nu["pages"]
        if nu["notes"]:
            u["notes"] = nu["notes"]
        units.append(u)
    order = {"page": 0, "epistle-text": 0, "intro": 1, "note": 1}
    units.sort(key=lambda u: (min(u["scan"]["leaves"]), order[u["kind"]]))
    return units, m, (a0, b0), pp


def monotone_heads(items, m, w=5):
    """(4c) A commentary's chapters only move forward, so a running head
    naming a chapter below the median of the five headed leaves before it, or
    above the median of the five after it (same book), is a misreading ('XL'
    for 'XI', 'XXV' for 'XXVIII'): its chapter is dropped, and counted."""
    seq, seen = [], set()
    for it in items:
        if it["hc"] is not None and it["leaf"] not in seen:
            seen.add(it["leaf"])
            seq.append((it["leaf"], it["book"], it["hc"]))
    bad = set()
    for i, (leaf, book, hc) in enumerate(seq):
        prev = [x[2] for x in seq[max(0, i - w):i] if x[1] == book]
        nxt = [x[2] for x in seq[i + 1:i + 1 + w] if x[1] == book]
        if (prev and hc < st.median_low(prev)) or (nxt and hc > st.median_high(nxt)):
            bad.add(leaf)
    for it in items:
        if it["leaf"] in bad:
            it["hc"] = None
    m["running_heads_out_of_order"] = len(bad)


class HeadDecoder(Decoder):
    """The base sequence, with three ways out of a missed chapter turn, each
    only where the base sequence refuses the number and only FORWARD:
    (1) a running head confirmed by its neighbours (hsure) names a later
    chapter that has the verse (K&D open a chapter's notes wherever its first
    section starts, 'Vers. 7-17', not at verse 1-4); (2) a chapter printed
    with the number ('VII. 1-40.', Alford's section heads) names a later
    chapter, at its verse 1-3, the page's running head names the same
    chapter, and the next numbers read go on from there;
    (3) three refusals running, each under a running head naming the same
    later chapter, which has the verse: the sequence was lost, the heads
    agree, follow them."""

    USE_HV = True

    def __init__(self, counts):
        super().__init__(counts)
        self.stuck = []

    def offer(self, n, e, hc, hv, cp=None, hsure=False, ahead=()):
        if not self.USE_HV:
            hv = ()
        nxt = [a for a in list(ahead)[:2]]
        if cp is not None and cp > self.c and len(nxt) == 2 and all(
                a[0] is None and self.v < a[1] <= self.counts.get(self.c, 0) and a[1] > n + 3 for a in nxt):
            return None         # 'IV. 1' while the numbers after it go on in this chapter: a reference
        r = super().offer(n, e, hc, hv, cp, hsure, ahead)
        if r is not None:
            self.stuck = []
            return r
        later = lambda c: c is not None and self.c < c <= self.nch and n <= self.counts.get(c, 0)  # noqa: E731
        if cp is None and hsure and later(hc) and (not hv or n <= max(hv) + 2):
            r = self._take(hc, n, e)
        elif cp is not None and later(cp) and cp == hc and n <= 3 \
                and all(a[0] is None and n <= a[1] <= n + 12 for a in list(ahead)[:2]):
            r = self._take(cp, n, e)
        elif cp is None and later(hc):
            self.stuck.append(hc)
            if len(self.stuck) >= 3 and len(set(self.stuck[-3:])) == 1:
                r = self._take(hc, n, e)
        else:
            self.stuck = []
        if r is not None:
            self.stuck = []
        return r


def decode_2b(slug, items, decoders, pp, m):
    """The verse sequence over the reading-order lines: each candidate opener
    is offered to its book's Decoder (seeing the next few candidates); a
    number far ahead of the sequence while a nearer one follows close behind
    is a misreading and is refused."""
    notes = collections.OrderedDict()
    current = {}
    flat = [(i, j) for i, it in enumerate(items) for j in range(len(it["cands"]))]
    seg, k = [], 0
    for it in items:
        k += 1 if it.get("psalm") else 0
        seg.append((it["book"], k))       # a psalm's title closes the look-ahead
    ahead = {}
    for k, (i, j) in enumerate(flat):
        ahead[(i, j)] = [items[i2]["cands"][j2][1][:2] for i2, j2 in flat[k + 1:k + 7] if seg[i2] == seg[i]]

    def unit(key, book, c=None, n=None, e=None):
        return notes.setdefault(key, {"book": book, "c": c, "n": n, "e": e, "text": "", "leaves": [], "pages": [],
                                      "notes": []})

    def put(key, text, leaf, para):
        nu = notes[key]
        if text:
            nu["text"] = nu["text"] + "\n" + text if (para and nu["text"]) else C.join(nu["text"], text)
        if leaf not in nu["leaves"]:
            nu["leaves"].append(leaf)
            if leaf in pp and pp[leaf][0] not in nu["pages"]:
                nu["pages"].append(pp[leaf][0])

    for i, it in enumerate(items):
        book, leaf = it["book"], it["leaf"]
        dec = decoders[book]
        pre = ids_prefix(slug, book)
        if current.get(book) is None:
            current[book] = f"{pre}title"
            unit(current[book], book)
        if it.get("foot"):
            unit(current[book], book)["notes"].append(it["text"])
            put(current[book], "", leaf, False)
            continue
        if it.get("psalm"):
            # a psalm's title line: the sequence moves to it, and what precedes its first verse note
            # (Delitzsch's introduction to the psalm) is the unit <c>.intro
            dec.c, dec.v = it["psalm"], 0
            current[book] = f"{pre}{it['psalm']}.intro"
            unit(current[book], book, it["psalm"])["intro"] = True
            put(current[book], it["text"], leaf, True)
            continue
        hc = it["hc"]
        if hc is None and it.get("hc_next") is not None and it["hc_next"] > dec.c:
            hc = it["hc_next"]
        pos, para = 0, it["para"]
        for j, (p, o) in enumerate(it["cands"]):
            cp, n, e, how = o
            nxt = ahead[(i, j)]
            if cp is None and n > dec.v + 1 and any(a[0] is None and dec.v < a[1] < n for a in nxt[:3]):
                m["openers_out_of_sequence"] += 1
                continue
            took = dec.offer(n, e, hc, it["hv"], cp, it["hsure"], nxt)
            back = reopen(slug, notes, pre, dec, n, cp) if not took else None
            if back:
                # (4c) a verse of this section taken up again (Keil's Jeremiah: the section's
                # translation verse by verse, then the exposition verse by verse): its text joins
                # that verse's unit, and the sequence stays where it was
                m["notes_reopened" if back in notes else "notes_opened_behind"] += 1
                put(current[book], it["text"][pos:p].strip(), leaf, para)
                unit(back, book, dec.c, n)
                current[book] = back
                pos, para = p, True
                continue
            m["openers_accepted" if took else "openers_rejected"] += 1
            if not took:
                continue
            c, n2, _ = took
            e2 = e if (e and n2 < e <= dec.counts.get(c, 0) and e - n2 <= 60) else None
            put(current[book], it["text"][pos:p].strip(), leaf, para)
            key = f"{pre}{c}.{n2}" + (f"-{e2}" if e2 else "")
            unit(key, book, c, n2, e2)
            current[book] = key
            pos, para = p, True
        put(current[book], it["text"][pos:].strip(), leaf, para)
    return notes


def reopen(slug, notes, pre, dec, n, cp):
    """(4c) The unit of a verse already passed in the current chapter, for an
    opener the sequence refused ('Ver. 20.' after 'Ver. 25.') inside the
    section the chapter's latest run opened ('Vers. 20-25.'): the verse's own
    unit, else the latest run that opens at it, else a new unit for that verse
    (the exposition after a translation printed without verse numbers); None
    elsewhere, or where the volume does not reopen."""
    if not SCANS[slug].get("reopen") or cp is not None or n >= dec.v:
        return None
    run = next((k for k in reversed(notes) if k.startswith(f"{pre}{dec.c}.") and "-" in k), None)
    if not run:
        return None
    a, b = (int(x) for x in run.rsplit(".", 1)[1].split("-"))
    if not a <= n <= b:
        return None         # only inside the section the latest run opened ('Vers. 20-25.')
    key = f"{pre}{dec.c}.{n}"
    if key in notes:
        return key
    return next((k for k in reversed(notes) if k.startswith(key + "-")), None) or key


def harvest_2b(slug, units, ids):
    """Scripture in the second shelf's units. Alford and Bengel: the English
    references in the KJV's numbering, as the first shelf. Keil & Delitzsch:
    which numbering the volume cites the OT in is MEASURED (existence votes,
    Psalms and the other OT books apart), and each OT reference is resolved in
    it, the Hebrew through data/versification/bhs-kjv.json."""
    s = SCANS[slug]
    if s["reader"] != "kd":
        n = r = 0
        own_single = s["epistles"][0][0] if len(s["epistles"]) == 1 else None
        for u in units:
            book = u.get("book") or own_single
            ch = None
            if u["kind"] == "note":
                mm = re.match(r'(?:[1-3]?[A-Za-z]+\.)?(\d+)\.\d', u["id"].split(":", 1)[1])
                ch = int(mm.group(1)) if mm else None
            text = u["text"] + " " + " ".join(u.get("notes", []))
            found = scripture(text, ids, own=book if u["kind"] == "note" else None, chapter=ch)
            u["links"] += found
            n += len(found)
            r += sum(1 for x in found if x["resolved"])
        return n, r, {}
    import versification as V
    parsed = []
    votes = {"Ps": [], "other": []}
    for u in units:
        text = u["text"] + " " + " ".join(u.get("notes", []))
        refs = FS.parse("¶ " + text, "eng")
        parsed.append(refs)
        for book, kind, ch, v, end, alt in refs:
            if kind == "kjv" and v is not None and book in V.BOOKS:
                votes["Ps" if book == "Ps" else "other"].append((book, ch, v))
    measure = {}
    for k, pairs in votes.items():
        vv = numbering_votes(pairs, ids)
        vv["decision"] = decide(vv)
        measure[k] = vv
    own_num, used = {}, set()
    n = r = 0
    for u, refs in zip(units, parsed):
        found, seen = [], set()
        for ref in refs:
            book, kind, ch, v, end, alt = ref
            p = FS.printed(ref)
            if p in seen:
                continue
            seen.add(p)
            if kind != "kjv":
                found.append({"ref": p, "resolved": False, "why": "a book outside the KJV", "rule": "text/kjv"})
                continue
            if v is None:
                found.append({"ref": p, "resolved": False, "why": "cites a whole chapter, not a verse", "rule": "text"})
                continue
            if book in V.BOOKS:
                cls = "Ps" if book == "Ps" else "other"
                dec, rl = effective(measure[cls]["decision"], book, ids, f"text/{cls}", used)
                x = dict(ref=p, **ot_link(book, ch, v, dec, ids, rl))
                y = ot_link(book, ch, end, dec, ids, rl) if end and end > v else None
            else:
                t = f"kjv:{book}.{ch}.{v}"
                x = ({"ref": p, "target": t, "resolved": True, "numbering": "kjv", "rule": "text/nt"} if t in ids else
                     {"ref": p, "resolved": False, "why": "no such verse in the KJV", "rule": "text/nt"})
                y = ({"target": f"kjv:{book}.{ch}.{end}", "resolved": True}
                     if end and end > v and f"kjv:{book}.{ch}.{end}" in ids else None)
            _kd_through(x, ch, v, end, y)
            found.append(x)
        if u["kind"] == "note" and u.get("book"):
            mm = re.match(r'(?:[1-3]?[A-Za-z]+\.)?(\d+)\.\d', u["id"].split(":", 1)[1])
            if mm:
                b, c = u["book"], int(mm.group(1))
                nb, srl = own_num.setdefault(b, effective(s["_numbering"].get(b, {}).get("decision", "kjv"), b, ids,
                                                          "self", used))
                for mt in SELF_VER.finditer(u["text"]):
                    for v, end in _ver_spans(mt):
                        p = f"{b} {c}:{v}" + (f"-{end}" if end else "")
                        if p not in seen:
                            seen.add(p)
                            x = dict(ref=p, **ot_link(b, c, v, nb, ids, srl.replace("self", "self/ver", 1)))
                            _kd_through(x, c, v, end, ot_link(b, c, end, nb, ids, "self/ver")
                                        if end and end > v else None)
                            found.append(x)
                for mt in KD_CHAP.finditer(u["text"]):
                    c2 = FS.roman(mt.group(1))
                    p = f"{b} {c2}:{mt.group(2)}"
                    if c2 and p not in seen and c2 <= max(heb_counts(b)):
                        seen.add(p)
                        found.append(dict(ref=p, **ot_link(b, c2, int(mt.group(2)), nb, ids,
                                                           srl.replace("self", "self/chap", 1))))
        u["links"] += found
        n += len(found)
        r += sum(1 for x in found if x.get("resolved"))
    return n, r, {"numbering_references": measure,
                  "numbering_work": {b: work_numbering(b, ids) for b in sorted(used)}}


def _ver_spans(mt):
    """A SELF_VER match as (verse, end or None) pairs: 'vv. 8-12' is one span,
    'vv. 8, 12' two verses."""
    out = [[int(mt.group(1)), None]]
    for sep, n in re.findall(r'\s*([,–—-])\s*(\d{1,2})', mt.group(2)):
        if sep == ",":
            out.append([int(n), None])
        else:
            out[-1][1] = int(n)
    return [tuple(x) for x in out]


def _kd_through(x, ch, v, end, y):
    """A range's end on a Keil & Delitzsch link: `through` where it resolves
    after the start, else `through_unread`, as the first shelf's scripture()."""
    if not end or not x.get("resolved"):
        return
    if end > v and y and y.get("resolved") and y["target"] != x["target"]:
        x["through"] = y["target"]
    else:
        x["through_unread"] = f"{ch}:{end}: " + ("backwards" if end <= v else "no such verse")


KD_CHAP = re.compile(r'\b(?:chap|ch)\.\s*([ivxlc]{1,8})\.\s*(\d{1,3})\b')   # 'chap. ii. 4': the same book
HEBREW_CHAR = re.compile(r'[֐-׿]')


def honesty_2b(slug):
    s = SCANS[slug]
    if s["reader"] == "alford":
        return ("notes keyed by verse where the OCR'd page lets them be: Alford runs his verse notes on inline "
                "('9.] As we said', '5. ᾧ ἡ δόξα'), so a verse number after the end of a clause, followed by a "
                "bracket or by Greek, and not after a reference's numeral or abbreviation, is a candidate, "
                "accepted when the verse sequence (and the fuzzily read running head) allows it; every following "
                "line, left column then right, belongs to it; boundaries are only as good as the numbers read off "
                "the page, and a misread or rejected number merges a verse's notes into the verse before (counts in "
                "measure); the Greek text block per leaf (leaf.N.text) with the digest of readings under it "
                "(apparatus) and the marginal references run into the text; every other page by scan leaf "
                "(leaf.N, the folio in scan.printed_page where read); unproofread OCR")
    if s["reader"] == "bengel":
        return ("notes keyed by verse where the OCR'd page lets them be: an indented paragraph opening with a verse "
                "number ('14. μηκέτι)') is a candidate, accepted when the verse sequence and the running head "
                "allow it; following paragraphs belong to it until the next; the translator's footnotes (the "
                "smaller type at a page's foot) go in `notes` of the unit open at that point; boundaries are only "
                "as good as the numbers read off the page (counts in measure); every other page by scan leaf "
                "(leaf.N); unproofread OCR")
    return ("notes keyed by verse where the OCR'd page lets them be: an indented paragraph opening 'Ver. 3.' or "
            "'Vers. 14-19.' is a candidate, accepted when the verse sequence and the running head ('CHAP. I. "
            "14-19.', 'PSALM V. 5—7.') allow it; following paragraphs, including the introduction to the next "
            "section, belong to it until the next accepted opener; ids are in the numbering the volume prints, "
            "MEASURED per book (measure.numbering_own) and linked to the KJV through bhs-kjv.json where it is the "
            "Hebrew's; the OT references in the text are resolved in the numbering measured for them "
            "(measure.numbering_references); where either measure is undecided, the commentary's own numbering of "
            "that book decides, measured from the note ids of every Keil & Delitzsch volume holding it, pooled "
            "(measure.numbering_work); where that too is undecided, a verse both numberings have is resolved only "
            "where the two read it alike, else it stays unresolved with both candidates; footnotes in `notes`; every other page by scan leaf (leaf.N); the "
            "Hebrew words are lost: the OCR read the pointed Hebrew as Latin-letter debris, which stays in the "
            "text as printed by the OCR, unremoved" + (f"; {s['honesty']}" if s.get("honesty") else "")
            + "; unproofread OCR")


def citation_2b(slug):
    lead = "book.chapter.verse" if slug in MULTI else "chapter.verse"
    extra = ", in the numbering the volume prints (scheme.numbering)" if SCANS[slug]["reader"] == "kd" else ""
    text = "leaf.N.text; " if SCANS[slug]["reader"] == "alford" else ""
    return (f"note: {lead} of the verse commented on{extra} (a run of verses: {lead}-end); {text}everything else: "
            "scan leaf (leaf.N; folio in scan.printed_page)")


def build_book_2b(slug, ids):
    """build_book for the second shelf: the same book shape, with the reader,
    the numbering measured, and Hebrew retention in measure."""
    s = SCANS[slug]
    units, m, (a0, b0), pp = build_scan_2b(slug, ids)
    s["_numbering"] = m.get("numbering_own", {})
    rights = {"license": f"public domain in the US (printed {s['printed']}); the scan and its OCR are the "
                         "Internet Archive's",
              "ia_possible_copyright_status": s["ia_rights"] or "(the item's metadata carries no rights field)",
              "attribution": f"Internet Archive, {s['ia']} ({s['copy']} copy)",
              "source_url": f"https://archive.org/details/{s['ia']}",
              "redistribute_whole": True}
    m["printed_page_read"] = sum(1 for x in pp.values() if x[1] == "read")
    m["printed_page_from_neighbours"] = sum(1 for x in pp.values() if x[1] != "read")
    n_links, n_resolved, extra = harvest_2b(slug, units, ids)
    numbering_own = m.pop("numbering_own", None)
    kinds = collections.Counter(u["kind"] for u in units)
    measure = {"units": dict(sorted(kinds.items())), **dict(sorted(m.items()))}
    cov = {}
    for b, _, _ in s["epistles"]:
        allv = {k for k in ids if k.startswith(f"kjv:{b}.")}
        cl = lambda u: [x for x in u["links"] if x.get("type") == "comments-on"]  # noqa: E731
        have = {x["target"] for u in units if u["kind"] == "note" and u.get("book") == b
                for x in cl(u) if x.get("resolved")}
        single = {x["target"] for u in units if u["kind"] == "note" and u.get("book") == b
                  for x in cl(u) if x.get("resolved") and len(cl(u)) == 1}
        chs = sorted({int(t.rsplit(".", 2)[1]) for t in have})
        cov[b] = {"kjv_verses": len(allv), "commented": len(have), "with_own_note": len(single)}
        if chs and (chs[0] > 1 or chs[-1] < max(verse_counts(ids, b))):
            # a volume holding part of a book: the verses of the chapters its notes reach
            cov[b]["chapters"] = [chs[0], chs[-1]]
            cov[b]["kjv_verses_in_chapters"] = sum(1 for k in allv if chs[0] <= int(k.rsplit(".", 2)[1]) <= chs[-1])
    measure["kjv_coverage"] = cov
    measure["scripture_links"] = {"read": n_links, "resolved": n_resolved,
                                  "ranges": sum(1 for u in units for x in u["links"] if "through" in x),
                                  "ranges_start_only": sum(1 for u in units for x in u["links"]
                                                           if "through_unread" in x)}
    if numbering_own is not None:
        measure["numbering_own"] = numbering_own
    measure.update(extra)
    measure["greek"] = greek_measure(u["text"] for u in units)
    letters = heb = 0
    for u in units:
        letters += sum(c.isalpha() for c in u["text"])
        heb += len(HEBREW_CHAR.findall(u["text"]))
    measure["hebrew"] = {"hebrew_letters": heb, "hebrew_share_of_letters": round(heb / letters, 4) if letters else 0}
    scheme = {"citation": citation_2b(slug), "resolution": "verse-note",
              "honesty": honesty_2b(slug) + RANGES_HONESTY_2B, "status": "draft"}
    if numbering_own is not None:
        scheme["numbering"] = {b: v["decision"] for b, v in numbering_own.items()}
    if s.get("lane_a"):
        scheme["same_scan_as"] = "Lane A's raw-OCR shelf of this IA item (pipeline/henry-alford_shelf.json, branch claude/armarium-divines)"
    if s.get("scan_choice"):
        scheme["scan_choice"] = s["scan_choice"]
    source = {"format": "ia-hocr", "sha256": s["sha256"], "ia": s["ia"], "leaves": [a0, b0]}
    s.pop("_numbering", None)
    return {"slug": slug, "title": s["title"], "author": s["author"], "edition": s["edition"], "source": source,
            "scheme": scheme, "rights": rights, "measure": measure, "units": units}


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
        # 'ver. 20' and a bare 'c. iii. 13' are the epistle's own only in its
        # notes: in an introduction or dissertation 'c.' is as often another
        # work's chapter (Eusebius, Irenaeus)
        found = scripture(text, ids, own=book if u["kind"] == "note" else None, chapter=ch)
        u["links"] += found
        n += len(found)
        r += sum(1 for x in found if x["resolved"])
    return n, r


RUNS_HONESTY = (
    "; a run of verses opening a note is kept at its first verse when it runs backwards, past the chapter or "
    "over 15 verses (measure.openers_run_cut), and a run into the next chapter ('28—V. 1.') is not read as an "
    "opener at all, its text joining the note before (openers_crossing_chapter); in the scripture references "
    "a range keeps its end in `through` (one crossing chapters, 'viii. 28-ix. 3', included) and a range the "
    "KJV cannot end keeps its start only, marked through_unread (scripture_links.ranges_start_only); 'ver. 20' "
    "and a bare 'c. iii. 13' are read as the commentary's own epistle in note units only, and never after "
    "another work's abbreviation ('Euseb. H.E. c. iv. 3')")


RANGES_HONESTY_2B = (
    "; in the scripture references a range keeps its end in `through` (one crossing chapters included), and a "
    "range the KJV cannot end keeps its start only, marked through_unread (scripture_links.ranges_start_only)")


def honesty(slug, ocr):
    h = _honesty(slug, ocr)
    if slug == "hort-ante-nicene":
        return h
    tail = "; unproofread OCR"
    return h[:-len(tail)] + RUNS_HONESTY + tail if h.endswith(tail) else h + RUNS_HONESTY


def _honesty(slug, ocr):
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
    if slug in SECOND:
        return build_book_2b(slug, ids)      # the second shelf's reader
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
    measure["scripture_links"] = {"read": n_links, "resolved": n_resolved,
                                  "ranges": sum(1 for u in units for x in u["links"] if "through" in x),
                                  "ranges_start_only": sum(1 for u in units for x in u["links"]
                                                           if "through_unread" in x)}
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
