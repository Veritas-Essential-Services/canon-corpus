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
                          R. Gandell (Oxford, 4 vols, the sheets of 1859; these copies possibly
                          a later issue): Matthew to 1 Corinthians, notes
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
"c. x. 11" the same epistle (`rule: self/...`), unless another work's
abbreviation, a Latin title word or a capitalised name stands just before it
(self_c_refused); "Gal. c. iv. 3" and "Gal. C. iv. 3" are Gal 4:3 (book_c). A
range FS.parse reads only the start of ("viii. 28-ix. 3", "8. 28-9. 3",
"iii. 12-8", "iii. 6, 7-iv. 2") is found by cross_ranges and applied only to
the reference under its own book.

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
#               cu31924075537088 (a 1921 reprint) 6.8% 66.5% 92.7%   (Lane A's item, lightfoot-galatians-1890)
#               saintpaulepistle00lighuoft 1914, saintpaulsepistl00lighuoft 1890,
#               sa590770400lighuoft 1880, stpaulsepistleto00ligh 1870: 0.0% Greek
#   Philippians stpaulsepistleto00lighuoft 1873  7.3%  65.6%  92.4%   <- chosen
#               saintpaulsepistl00ligh 1878      7.3%  65.1%  92.1%   (4th ed.; Lane A's item, lightfoot-philippians-1878)
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
#               gospelaccordingt02west vol. 2    10.3%  41.9%  93.5%   <- chosen (also Lane A's vol. 2, since 2026-10-03)
#               gospelaccordingt02west_0 (Lane A's first vol. 2, replaced), gtu_32400003017666_2, gospelaccordingt0002broo,
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
        "note": ("Lane A (branch claude/armarium-divines, pipeline/j-b-lightfoot_shelf.json, lightfoot-galatians-1890) "
                 "shelves another copy of the same 10th edition, cu31924075537088 (its reprint list ends 1921): "
                 "Greek 6.8% of letters, Greek tokens known 66.5%, English 92.7%, against 6.8%, 65.9% and 92.6% "
                 "here (measured 2026-10-03 on each _djvu.txt): not clearly better"),
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
        "note": ("Lane A (branch claude/armarium-divines, pipeline/j-b-lightfoot_shelf.json, "
                 "lightfoot-philippians-1878) shelves another edition, the 4th (London: Macmillan, 1878), "
                 "saintpaulsepistl00ligh: Greek 7.3% of letters, Greek tokens known 65.1%, English 92.1%, "
                 "against 7.3%, 65.6% and 92.4% here (measured 2026-10-03 on each _djvu.txt)"),
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
                    "unit of that verse (scan.leaves and scan.printed_pages are then the first volume's, and "
                    "a unit taken up again in the other volume lists every leaf and page with its volume in "
                    "scan.volume_leaves and scan.volume_printed_pages)"),
        "note": ("Lane A (branch claude/armarium-divines, pipeline/b-f-westcott_shelf.json) shelves the raw OCR of "
                 "the same two scans, gospelaccordingt01west and gospelaccordingt02west, as westcott-john-greek-1/-2, "
                 "and gospelaccordingt00westuoft (the 1892 Authorised Version edition) as westcott-john-av-1892; "
                 "its vol. 2 was first gospelaccordingt02west_0, replaced 2026-10-03 because that copy's text "
                 "layer has no Greek codepoints (0.0% of letters, measured 2026-10-03 on its _djvu.txt) against "
                 "10.3% in gospelaccordingt02west"),
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
                    "the Corinthians, a new edition by Robert Gandell, 4 vols (Oxford: University Press, the "
                    "sheets of 1859); "
                    "the title pages print no date (Gandell's preface is dated 1 April 1859) and vol. 4 ends with "
                    "a Macmillan advertisement, so these copies may be a later issue of the 1859 sheets"),
        "printed": 1859,
        "printed_label": "1859 (the sheets; this copy possibly a later issue)",
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
SELF_C_OK = {"cf.", "comp.", "conf.", "cp.", "see", "so", "also", "esp.", "and", "in", "on", "with", "as", "e.g.",
             "i.e.", "above", "below", "ver.", "vv.", "(", "[", ";", ",", "compare", "comp", "cf", "again", "here"}
# ... and a work named without an abbreviation is another work too: a Latin title
# word among the three words before ('Tertullian de Baptismo c. iv. 3', 'Pro
# Cluentio, c. v. 12'), or a capitalised name just before and not one of these English
# words ('this Epistle c. iii. 17' is the epistle's own), opening a sentence too ('Irenaeus
# c. iv. 3' is refused; 'Oompare c. x. 12' and 'Boo c. v. 11', OCR of 'Compare' and 'See', are
# read by SELF_C_OCR below)
SELF_C_TITLE = {"de", "adv", "adv.", "adversus", "contra", "pro", "apud"}
SELF_C_ENGLISH = {"epistle", "chapter", "compare", "contrast", "see", "comp", "cf", "note", "so", "also"}
# '<Book>. c. iv. 3' ('Chrys. on Gal. c. iv. 3', 'Gal. C. iv. 3'): that book's chapter and verse, the
# 'c.' or 'C.' a word ('chapter'), never Roman C; it is dropped before FS.parse reads it
BOOK_C = re.compile(r'(?<![\w])((?:(IV|III|II|I|[1-4])\.?\s?)?([A-Z][a-zA-Z]{0,11})\.?,?\s*)(?<![A-Za-z])[cC]\.\s*'
                    r'(?=[ivxlIVXL]{1,7}\.\s*\d)')
# a range crossing a chapter: 'viii. 28-ix. 3', '8:28-9:3' or '8. 28-9. 3' (FS.parse reads its start
# only); with the chapter repeated ('iii. 28-iii. 3') it may also run backwards in one chapter
CROSS_RANGE = re.compile(r'\b([ivxlc]{1,7})\.\s*(\d{1,3})\s*[–—-]+\s*([ivxlc]{1,7})\.\s*(\d{1,3})\b'
                         r'|\b(\d{1,3})[:.]\s*(\d{1,3})\s*[–—-]+\s*(\d{1,3})[:.]\s*(\d{1,3})\b')
# a range closing a comma list and running into the next chapter ('iii. 6, 7-iv. 2'): FS.parse
# reads the list's verses and drops the range's end; the key is the list's last verse. Only
# the next chapter: Bengel's translators also set a dash between references ('1 Cor. ii. 8,
# 11—viii. 1', 'viii. 1, 2, 13—ix. 27'), and a list does not open a range of chapters
LIST_RANGE = re.compile(r'\b([ivxlc]{1,7})\.\s*\d{1,3}(?:\s*,\s*\d{1,3})*\s*,\s*(\d{1,3})\s*[–—-]+\s*'
                        r'([ivxlc]{1,7})\.\s*(\d{1,3})\b'
                        r'|\b(\d{1,3})[:.]\s*\d{1,3}(?:\s*,\s*\d{1,3})*\s*,\s*(\d{1,3})\s*[–—-]+\s*'
                        r'(\d{1,3})[:.]\s*(\d{1,3})\b')
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


def book_c(text):
    """'Gal. c. iv. 3' -> 'Gal. iv. 3' where the name is a KJV book: FS.parse
    would read the 'c.' as Roman 100 ('Gal 100')."""
    def f(m):
        b, kind = FS.book_of(m.group(2), m.group(3), "eng")
        return m.group(1) if b and kind == "kjv" else m.group(0)
    return BOOK_C.sub(f, text)


ROMAN_NAME = re.compile(r'[IVXLC]+')


def book_before(text, pos):
    """The book a reference at `pos` is read under: the last name before it
    that FS.parse would take as a book (a name that is no book, or another
    work's title, ends the book before it). Roman chapter numerals are not names."""
    book = None
    for m in FS.BOOK_RE.finditer(text):
        if m.start() >= pos:
            break
        if ROMAN_NAME.fullmatch(m.group("name")) and not m.group("pre"):
            continue
        b, kind = FS.book_of(m.group("pre"), m.group("name"), "eng")
        book = b if b and kind == "kjv" and not FS.NOT_AFTER.search(text, 0, m.start()) else None
    return book


def cross_ranges(text):
    """(book, chapter, verse) -> (chapter, verse) for every range in the text
    that crosses into a later chapter, runs backwards in one, or repeats its
    chapter ('iii. 28-iii. 3'). Keyed by the book it is read under, so a range
    applies only to its own reference, never to another book cited at the same
    chapter and verse ('Phil. iii. 20-iv. 1; comp. Col. iii. 20')."""
    out = {}
    s = text.replace("—", "-").replace("–", "-").replace("‒", "-")
    for m in CROSS_RANGE.finditer(s):
        if m.group(1):
            a, b = FS.roman(m.group(1)), FS.roman(m.group(3))
            v, w = int(m.group(2)), int(m.group(4))
        else:
            a, v, b, w = (int(m.group(k)) for k in (5, 6, 7, 8))
        if a and b and (b > a or (b == a and w != v)):
            out.setdefault((book_before(s, m.start()), a, v), (b, w))
    for m in LIST_RANGE.finditer(s):
        if m.group(1):
            a, b = FS.roman(m.group(1)), FS.roman(m.group(3))
            v, w = int(m.group(2)), int(m.group(4))
        else:
            a, v, b, w = (int(m.group(k)) for k in (5, 6, 7, 8))
        if a and b == a + 1:
            out.setdefault((book_before(s, m.start()), a, v), (b, w))
    for m in BACK_RANGE.finditer(s):
        a = FS.roman(m.group(1)) if m.group(1) else int(m.group(4))
        v, w = (int(m.group(2)), int(m.group(3))) if m.group(1) else (int(m.group(5)), int(m.group(6)))
        if a and w < v:
            out.setdefault((book_before(s, m.start()), a, v), (a, w))
    return out


# (review c11) a comma list of verses after an English chapter ('Rom. viii. 1, 2, 13', 'Rom. 8:1, 2,
# 13'): FS.parse reads ', 2, 13' as the apparatus's 'chapter, verse' (Rom 2:13), so for FS.parse
# alone the list's commas become '.' (more verses of the chapter) and a comma after it ';' (a new
# reference). Only after a Roman chapter or 'N:': an arabic 'N. M, ...' stays FS.parse's
VERSE_LIST = re.compile(r'(?P<list>(?<![\w])(?:[ivxlcIVXLC]{1,7}\.|\d{1,3}:)\s*\d{1,3}'
                        r'(?:\s*[-–—]\s*\d{1,3}(?!\d)(?!\s*[.:]\s*\d))?'
                        r'(?:\s*,\s*\d{1,3}(?!\d)(?!\s*[.:]\s*\d)(?:\s*[-–—]\s*\d{1,3}(?!\d)(?!\s*[.:]\s*\d))?)+)'
                        r'(?P<tail>\s*,(?=\s*(?:[ivxlcIVXLC]{1,7}\.|\d{1,3}[.:])\s*\d))?')


def verse_lists(text):
    """The text as FS.parse should read it: each English verse list's commas '.', and a comma
    after the list before another chapter ';'. Only for FS.parse: the other patterns read
    the text as printed."""
    text = VERSE_LIST.sub(lambda m: m.group("list").replace(",", ".") + (m.group("tail") or "").replace(",", ";"),
                          text)
    # (review c12) 'Rom. 8:1, 12:3': a comma between two 'N:M' is a new reference, not a verse 12
    return CHAPTER_COMMA.sub(r"\1;", text)


CHAPTER_COMMA = re.compile(r'(?<![\w:])(\d{1,3}:\d{1,3})\s*,(?=\s*\d{1,3}:\d)')


# (review c11) the OCR misreadings of SELF_C_OK / SELF_C_ENGLISH words actually found before a
# self 'c.' in these scans (measured over all 43 volumes), read as the word they misread. An
# explicit list, not 'one letter off': that let names through ('Hero', 'Hera', 'Leo c. v. 11')
SELF_C_OCR = {"oompare": "compare", "oomp.": "comp.", "boo": "see", "seo": "see"}


def self_c_refused(text, start):
    """A bare 'c. iv. 3' is another work's chapter when the word before it is
    an abbreviation ('Euseb. H.E. c. iv. 3'), when a Latin title word stands
    among the three words before it ('Tertullian de Baptismo c. iv. 3'), or when
    the word before is a capitalised name (opening a sentence too, unless it is
    one of the English words above or an observed OCR misreading of one,
    SELF_C_OCR); 'cf. c. iv. 3', 'comp. c. iv. 3', 'Compare c. x. 12' and
    'Faith: c. ix. 15' are read."""
    ws = text[max(0, start - 60):start].split()
    if not ws:
        return False
    w = ws[-1]
    lw = w.lower().lstrip("([") or w      # '(comp. c. iv. 3' is 'comp.'
    if lw in SELF_C_OK or lw in SELF_C_OCR or re.fullmatch(r'[\d.]+', w):
        return False
    if w.endswith("."):
        return True
    if any(x.lower().strip(",;:(") in SELF_C_TITLE for x in ws[-3:]):
        return True
    if w[-1] in ",;:":
        return False            # a clause ends before the reference ('Faith: c. ix. 15')
    bare = w.lstrip("([") or w   # (review c12) '(Irenaeus c. iv. 3' is a name too
    if bare[:1].isupper() and bare.lower() not in SELF_C_ENGLISH:
        return True             # a name, mid-sentence or opening one ('Irenaeus c. iv. 3', 'Leo c. v. 11')
    return False


def scripture(text, ids, own=None, chapter=None):
    """English references in a unit's text, resolved in the KJV's numbering.
    `own` (a note unit's epistle) also reads 'ver. 20' (with `chapter`) and a
    bare 'c. iii. 13' as the commentary's own epistle, unless an abbreviation
    of another work stands just before it. A range keeps its end in `through`;
    a range the KJV cannot end (past the chapter, or backwards) keeps its
    start only and says so in `through_unread`."""
    out, seen = [], set()
    read = book_c(text)
    xr = cross_ranges(read)
    for r in FS.parse("¶ " + verse_lists(read), "eng"):
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
        elif (book, ch, v) in xr:
            c2, v2 = xr[(book, ch, v)]
            if c2 < ch or (c2 == ch and v2 <= v):
                x["through_unread"] = f"{c2}:{v2}: backwards"
            elif c2 == ch and f"kjv:{book}.{ch}.{v2}" in ids:
                x["through"] = f"kjv:{book}.{ch}.{v2}"
                x["ref"] = p = f"{p}-{v2}"
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


def hebrew_pairs(lines):
    """Adjacent Hebrew words in a line, in the order the line holds them (the
    hOCR's, or left to right where merge_rows joined two OCR rows): how many
    pairs run right to left on the page (the second word's box left of the
    first: Hebrew's reading order) and how many left to right (word-reversed)."""
    rtl = ltr = 0
    for l in lines:
        ws = l["words"]
        for a, b in zip(ws, ws[1:]):
            if HEBREW_WORD.match(a[5].lstrip("([‘“'\"")) and HEBREW_WORD.match(b[5].lstrip("([‘“'\"")):
                if b[0] < a[0]:
                    rtl += 1
                else:
                    ltr += 1
    return {"pairs_right_to_left": rtl, "pairs_left_to_right": ltr}


def hebrew_word_order(slug):
    """hebrew_pairs over every line as the build keeps it: the hOCR's word
    order, which the build never reorders; a note leaf's lines after
    merge_rows, which sorts the words of two joined OCR rows left to right."""
    s0 = SCANS[slug]
    tot = collections.Counter()
    for s in volumes(s0):
        P = pages(slug, s)
        seg = {leaf for e in s["epistles"] for leaf in range(e[1], e[2] + 1)}
        a0, b0 = s["leaves"]
        for leaf in range(a0, b0 + 1):
            body = analyse(P[leaf])["body"]
            if leaf in seg and s0.get("style") == "ver":
                body = C.merge_rows(body)
            tot.update(hebrew_pairs(body))
    return {k: tot[k] for k in ("pairs_right_to_left", "pairs_left_to_right")}

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


def note_leaf(nu, vol, leaf, pp):
    """A note unit's leaves as (volume, leaf): a verse taken up again in a later
    volume (Westcott's John) joins its first unit, and leaf numbers (and
    folios) repeat from one volume to the next. `leaves` and `pages` keep the
    unit's own (first) volume's only."""
    if (vol, leaf) in nu["vleaves"]:
        return
    nu["vleaves"].append((vol, leaf))
    if vol == nu["vol"]:
        nu["leaves"].append(leaf)
    if pp and (vol, pp[0]) not in nu["vpages"]:
        nu["vpages"].append((vol, pp[0]))
        if vol == nu["vol"]:
            nu["pages"].append(pp[0])


def note_scan(nu):
    """A note unit's `scan`: its volume's leaves and folios; where it runs into
    another volume, every leaf and folio with its volume as well."""
    sc = {"leaves": nu["leaves"]}
    if nu["pages"]:
        sc["printed_pages"] = nu["pages"]
    if nu["vol"]:
        sc["volume"] = nu["vol"]
    if any(v != nu["vol"] for v, _ in nu["vleaves"]):
        sc["volume_leaves"] = [list(t) for t in nu["vleaves"]]
        sc["volume_printed_pages"] = [list(t) for t in nu["vpages"]]
    return sc


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
                              "vol": x["vol"], "vleaves": [], "vpages": []}
            cur = current[book] = key
        if cur is None:
            cur = current[book] = f"{vol_id(x['vol'])}{ids_prefix(slug, book)}title"
            notes.setdefault(cur, {"book": book, "c": None, "n": None, "e": None, "text": "",
                                   "leaves": [], "pages": [], "vol": x["vol"], "vleaves": [], "vpages": []})
        nu = notes[cur]
        nu["text"] = nu["text"] + "\n" + l["text"] if (indented and nu["text"]) else C.join(nu["text"], l["text"])
        note_leaf(nu, x["vol"], leaf, x["pp"])
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
             "scan": note_scan(nu)}
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
#   Alford III          greektestamentwi00alfo 4th ed. 1865  15.4%  35.5%  86.8%   <- chosen
#                       greektestamentwi03alfo 1856 (Lane A's item; its text layer would not download at first,
#                       HTTP 500): re-measured 2026-10-03 beside 00alfo with greek_measure(): 16.3% vs 15.3%,
#                       known 21.3% vs 35.5%, English 85.1% vs 86.8%, mixed-script tokens 378 vs 0: not better
#                       greektestamentw03alfo 1849-cat. 15.8% 35.5% 86.5%; greektestamentwi0003alfo 1859: 0.0%;
#                       greektestament03alfo 1868: ~100% Greek letters
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
        "(leaf 11) reads, naming no other translator; bound with vol. III", 1873,
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
    "alford-commentary-3": "greektestamentwi00alfo (4th ed., 1865): Greek 15.3% of letters, Greek tokens known 35.5%, "
                           "English 86.8%, mixed-script tokens 0; Lane A's item (pipeline/henry-alford_shelf.json, "
                           "alford-greek-testament-3) is greektestamentwi03alfo (title page dated 1856, no edition "
                           "statement): Greek 16.3% (273,536 letters), known 21.3%, English 85.1%, mixed-script "
                           "tokens 378 (both measured 2026-10-03 on each _djvu.txt with greek_measure()): more Greek "
                           "letters, far fewer of them Greek words, so not better; greektestamentw03alfo 15.8%/35.5% "
                           "is a catalogue-1849 copy of unstated edition",
    "alford-commentary-4": "Lane A's item (same scan); measured against greektestamentwi5604alfo (3rd ed., 1866): "
                           "Greek 14.0% vs 13.6%, known 35.7% vs 35.5%",
    "bengel-gnomon-2": "gnomonofnewtesta23beng (vols. II and III bound as one): Greek 6.3%, known 34.4%; "
                       "cu31924092350523 (1877, vol. II) 5.9%/33.1%",
    "bengel-gnomon-3": "gnomonofnewtesta23beng (vols. II and III bound as one); cu31924092350499 (1877, vol. III): "
                       "0.0% Greek",
    "bengel-gnomon-4": "cu31924092350507 (1877): Greek 7.5%, known 32.4%; gnomonofnewtesta03benguoft (1873): 0.0% Greek",
}
# books whose scans are exactly the IA items Lane A shelves as raw OCR (checked 2026-10-03 against
# origin/claude/armarium-divines:pipeline/<name>_shelf.json): scheme.same_scan_as
_LANE_A = "branch claude/armarium-divines"
SAME_SCAN_AS = {
    "westcott-hebrews": f"same scan as Lane A: westcott-hebrews-1892 (pipeline/b-f-westcott_shelf.json, {_LANE_A})",
    "westcott-john": f"same scan as Lane A: westcott-epistles-john-1892 (pipeline/b-f-westcott_shelf.json, {_LANE_A})",
    "westcott-gospel-john": ("same scans as Lane A: westcott-john-greek-1 and westcott-john-greek-2 "
                             f"(pipeline/b-f-westcott_shelf.json, {_LANE_A})"),
    "alford-commentary-2": f"same scan as Lane A: alford-greek-testament-2 (pipeline/henry-alford_shelf.json, {_LANE_A})",
    "alford-commentary-4": f"same scan as Lane A: alford-greek-testament-4 (pipeline/henry-alford_shelf.json, {_LANE_A})",
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
            if s.get("reader") not in KD_READERS or book not in [e[0] for e in s.get("epistles", [])]:
                continue                                # KD4D: was != "kd"
            if k not in _OWN:
                _OWN[k] = (KD_VOTES.get(s["reader"], build_scan_2b)(k, ids, votes_only=True)   # KD4D: KD_VOTES
                           if scan_present(k) else committed_votes(k))
            for f in tot:
                tot[f] += _OWN[k][book][f]
            vols.append(k)
        _WORK[book] = dict(tot, decision=decide(tot), volumes=vols)
    return _WORK[book]


def scan_present(slug):
    """Its pages can be read here: the pages cache, or the hOCR (which pages() checks against its pin)."""
    s = SCANS[slug]
    return (os.path.exists(os.path.join(CACHE, f"{s['ia']}.{s['sha256'][:12]}.pages.json.gz"))
            or os.path.exists(os.path.join(CACHE, f"{s['ia']}_hocr.html")))


def committed_votes(slug):
    """(review c11) A volume whose scan is not here lends work_numbering its own-id votes as the
    committed manifest records them (measure.numbering_own: the same votes its build makes), so
    one volume builds or checks with only its own scan. Neither: stop, and say which."""
    with open(MANIFEST, encoding="utf-8") as f:
        e = json.load(f).get(slug)
    own = (e or {}).get("measure", {}).get("numbering_own")
    if own is None:
        raise SystemExit(f"work_numbering needs {slug}: its scan is absent and the manifest has no "
                         f"numbering_own for it\n  run: python3 pipeline/build_commentaries.py --fetch")
    print(f"  ({slug}: scan absent, its numbering votes read from the committed manifest)", file=sys.stderr)
    return {b: {f: v[f] for f in ("read", "only_hebrew", "only_kjv")} for b, v in own.items()}


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
    if s["reader"] not in KD_READERS:          # KD4D: was != "kd"
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
    if s["reader"] in READER_TEXTS:
        return READER_TEXTS[s["reader"]]["honesty"]
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
    if SCANS[slug]["reader"] in READER_TEXTS:
        return READER_TEXTS[SCANS[slug]["reader"]]["citation"](slug)
    lead = "book.chapter.verse" if slug in MULTI else "chapter.verse"
    extra = ", in the numbering the volume prints (scheme.numbering)" if SCANS[slug]["reader"] == "kd" else ""
    text = "leaf.N.text; " if SCANS[slug]["reader"] == "alford" else ""
    return (f"note: {lead} of the verse commented on{extra} (a run of verses: {lead}-end); {text}everything else: "
            "scan leaf (leaf.N; folio in scan.printed_page)")


def build_book_2b(slug, ids):
    """build_book for the second shelf: the same book shape, with the reader,
    the numbering measured, and Hebrew retention in measure."""
    s = SCANS[slug]
    units, m, (a0, b0), pp = SCAN_READERS.get(s["reader"], build_scan_2b)(slug, ids)
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
    if slug in SAME_SCAN_AS:
        scheme["same_scan_as"] = SAME_SCAN_AS[slug]
    if s.get("scan_choice"):
        scheme["scan_choice"] = s["scan_choice"]
    source = {"format": "ia-hocr", "sha256": s["sha256"], "ia": s["ia"], "leaves": [a0, b0]}
    s.pop("_numbering", None)
    return {"slug": slug, "title": s["title"], "author": s["author"], "edition": s["edition"], "source": source,
            "scheme": scheme, "rights": rights, "measure": measure, "units": units}


# ================================================================== the third shelf: Meyer (2026-10-03)
#
# H. A. W. Meyer, Critical and Exegetical Commentary (Handbook) on the New
# Testament, in the T. & T. Clark translation (Edinburgh, 1873-1882; Clark's
# Foreign Theological Library). One book per volume, read from Internet
# Archive hOCR. Every scan of each volume was measured on its _djvu.txt
# (2026-10-03): Greek letters as a share of all letters, and Greek tokens of 3+
# letters found in the Strong's/John yardstick (greek_vocab), the manifest's
# figure; then the chosen ones again on their commentary leaves (hOCR):
#
#   Matthew I       criticalexeget01meyeiala (T&T Clark, 1880 issue) 5.1% / 34.9%  <- the only scan with Greek
#                   Funk & Wagnalls 1884 (one volume): criticalexegetic01meye, criticalandexeg02meyegoog,
#                   criticalexegetic0000meye_y5k0: 0.0% Greek (every Greek word in Latin letters)
#   Matthew II      criticalexegetic12meye (T&T Clark, 1879) 6.2% / 37.1% on its commentary leaves  <- chosen
#                   criticalexegetic02meyeiala (1881 issue) 6.3% / 36.1%: not clearly better;
#                   criticalexeg02meye (1877 cat.): 0.0%
#   Mark & Luke I   criticalexegetic21meye (1880) 8.4% / 35.3%  <- chosen: the same Princeton set as vol. II
#                   criticalexeget01meye (1880, another Princeton copy) 8.4% / 35.3%: the same;
#                   Funk 1884/1893 (one volume): criticalexegetic00meye 7.0%/36.2%, criticalexegetic02meye
#                   7.0%/36.8% (the American issue: the T&T Clark text with the American editor's notes);
#                   criticalandexeg00riddgoog, criticalexegetic0000meye, handbooktogospel0000hein: 0.0%
#   Mark & Luke II  criticalexegetic22meye (1880) 7.9% / 36.8%  <- chosen; criticalexeget02meye (1880): 0.0%
#   John            every T&T Clark scan has 0.0% Greek: criticalexegeticjohn01meye, criticalexegeticjohn02meye
#                   (1874-75), criticalexegetic188101meye (1881), bwb_P9-EDR-284_1 (1883). The Funk & Wagnalls
#                   issue (New York, 1884: the T&T Clark translation, with A. C. Kendrick's notes for the
#                   American edition) keeps it: criticalexegetic04meye 5.1% / 42.1%  <- chosen;
#                   criticalandexeg01meyegoog 5.0% / 42.0%, commentaryonnew01unkngoog (1883) 5.1% / 42.0%:
#                   the same printing, not better; bwb_S0-ATB-610: 0.0%
#   Romans          every T&T Clark scan has 0.0% Greek: criticalandexeg00dickgoog (1873), criticalexegetic62meye
#                   (1874, vol. II), criticalexeg00meye (1881, vol. I). The Funk & Wagnalls issue (New York,
#                   1884, with Timothy Dwight's notes for the American edition): criticalexegetic06meye
#                   6.5% / 40.5%  <- chosen; criticalandexeg03meyegoog, criticalandexege05meyeuoft: 0.0%
#   Acts I, II      criticalexegetic51meye / 52meye (Princeton, 1877) 6.2% / 33.8% and 7.4% / 31.0%  <- chosen;
#                   criticalexegetic01meyeiala 6.1% / 33.4%, criticalexeget00meye 5.7% / 33.3% (vol. I): not better
#   Corinthians I   criticalexegetic71meye (Princeton, 1877) 7.3% / 40.3%  <- chosen; criticalexege01meye
#                   6.9% / 40.6%, Funk & Wagnalls criticalexegetme00meye (1884) 7.3% / 41.0%: not clearly better;
#                   criticalhandbook01meyeuoft: catalogued 1906-
#   Corinthians II  criticalexegetic72meye (Princeton, title page 1879) 8.3% / 41.0%  <- chosen
#   Galatians ... Jude: each volume's chosen scan and the others measured are in its scan_choice below.
#   Thessalonians (Lünemann, 1880) is NOT SHELVED: its only scan, criticalexegetic00ln, has 0.0% Greek.
#   (CriticalExegeticalHandbookNewTestament11Volumes, a modern compilation of no stated edition, and
#   in.ernet.dli.2015.350526: 0.0%.)
#
# F. Godet's commentaries in the T. & T. Clark translation (John, 3 vols, 1876-77 and later issues; Luke,
# 2 vols, 1875 and later; Romans, 2 vols, 1880-81; 1 Corinthians, 2 vols, 1886-87) are NOT SHELVED: all 50
# scans of them with a text layer (the Edinburgh issues and the Funk & Wagnalls reprints) have 0.0% Greek
# letters; dli.ernet.73313 and commentaryonstp00godegoog would not give their text (2026-10-03), and the
# Zondervan/Kregel reprints (1956-91: commentaryonepis0000fgod, commentaryonfirs0000fgod, ...) are after 1928. Godet quotes the Greek in the body of his notes ('the pron. αὐτός'), and
# the OCR turned every such word into Latin-letter debris ('auTo^;'). Neither CCEL nor Project Gutenberg
# holds them (searched 2026-10-03). The candidates and their measures are in the README.
#
# THE PAGE. One column. Each chapter opens with a heading 'CHAPTER IV.' and Meyer's critical notes on its
# readings, a paragraph running its verses on inline ('Ver. 4. ὁ ἄνθρωπ.] Elz. Scholz omit ... — Ver. 6.
# ...'); the exegesis follows, a paragraph per verse or run, opening 'Ver. 1. Βίβλος γενέσεως] ...' or
# 'Vv. 2-6.'. So the chapter heading opens the unit <chapter>.intro (the critical notes); only an
# INDENTED paragraph that opens 'Ver. N.' (or 'Vv.', 'Vers.') is a candidate verse opener, and never the
# first line after a heading; a candidate whose first two lines read like the critical apparatus (two or
# more of Lachm., Tisch., Elz., Recepta, Curss., Codd., vss...) is critical notes, not exegesis. A heading
# the OCR lost or garbled is found as a short centred line followed by such a critical paragraph; its
# number, if unread, is the next chapter (Meyer comments on every chapter in order). A critical paragraph
# with no heading at all, where the running heads say the chapter has turned (or the last chapter's
# verses are done), is taken as the heading (chapter_headings_implied). The Funk & Wagnalls issues print
# the American editor's 'Notes by American Editor' at the end of a chapter or a group of chapters: the
# unit <chapter>.american (kind editor-notes), never mixed into Meyer's notes.


def _meyer(ia, sha, title, short, edition, printed, copy, leaves, books, ia_date, ia_date_note=None,
           first_chapter=None, american=None, scan_choice=None, inline=True, author="H. A. W. Meyer", *,
           ia_rights):
    # ia_rights: the item's possible-copyright-status as IA's metadata gives it (None when absent), read
    # 2026-10-03 and checked again live by --fetch, which stops on any change
    s = {"ia": ia, "sha256": sha, "title": title, "short": short, "author": author, "edition": edition,
         "printed": printed, "copy": copy, "ia_rights": ia_rights, "leaves": leaves, "epistles": books,
         "apparatus": False, "reader": "meyer", "ia_date": ia_date}
    for k, v in (("ia_date_note", ia_date_note), ("first_chapter", first_chapter), ("american", american),
                 ("scan_choice", scan_choice)):
        if v:
            s[k] = v
    if not inline:
        s["inline"] = False          # measured: Romans keeps more verses with paragraph openers only
    return s


_MEY = ("H. A. W. Meyer, Critical and Exegetical Commentary on the New Testament, translated from the German "
        "(Edinburgh: T. & T. Clark, Clark's Foreign Theological Library)")
_MEY_FUNK = ("H. A. W. Meyer, Critical and Exegetical Hand-book, the T. & T. Clark translation reissued "
             "with supplementary notes for the American edition (New York: Funk & Wagnalls, 1884)")
MEYER = {
    "meyer-matthew-1": _meyer(
        "criticalexeget01meyeiala", "fe4a4957a2ae1fae7aac1338aeedda5672a0bf6d54171d4315fd9020c344b601",
        "Critical and Exegetical Handbook to the Gospel of Matthew, vol. I", "Meyer, Matt. I",
        f"{_MEY}: the Gospel of Matthew, vol. I (chapters i.-xvii.), tr. from the sixth German edition by Peter "
        "Christie, revised and edited by Frederick Crombie (MDCCCLXXX: the 1880 issue), as its title page reads",
        1880, "University of California Libraries", (4, 499), [("Matt", 94, 498)], "1880",
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="the only scan of vol. I whose OCR kept the Greek (5.1% of letters, 34.9% known); the Funk & "
                    "Wagnalls scans (1884) have 0.0% Greek"),
    "meyer-matthew-2": _meyer(
        "criticalexegetic12meye", "ebff2f82b306d0fd53c73b1c18f8a7eecfa8018e995f13826183194e27ee00ef",
        "Critical and Exegetical Handbook to the Gospel of Matthew, vol. II", "Meyer, Matt. II",
        f"{_MEY}: the Gospel of Matthew, vol. II (chapters xviii.-xxviii.), tr. Peter Christie, revised and "
        "edited by Frederick Crombie (MDCCCLXXIX: 1879), as its title page reads", 1879,
        "Princeton Theological Seminary Library", (9, 322), [("Matt", 15, 322)], "1877",
        ia_date_note="IA catalogues it 1877 (the set's first date); this volume's title page reads 1879",
        first_chapter={"Matt": 18},
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexegetic12meye (1879): Greek 6.2%, known 37.1% on the commentary leaves; "
                    "criticalexegetic02meyeiala (1881 issue) 6.3% / 36.1%: not clearly better; "
                    "criticalexeg02meye: 0.0% Greek"),
    "meyer-mark-luke-1": _meyer(
        "criticalexegetic21meye", "0b07ab24a5e2d534672d113ece616db303f7f42762cee74e4177025c61c78615",
        "Critical and Exegetical Handbook to the Gospels of Mark and Luke, vol. I", "Meyer, Mark-Luke I",
        f"{_MEY}: the Gospels of Mark and Luke, vol. I (Mark; Luke i.-ii.), tr. from the fifth German edition "
        "by Robert Ernest Wallis, revised and edited by William P. Dickson (MDCCCLXXX: 1880), as its title "
        "page reads", 1880, "Princeton Theological Seminary Library", (7, 372),
        [("Mark", 36, 279), ("Luke", 293, 371)], "1880",
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexegetic21meye, the same Princeton set as vol. II: Greek 8.4%, known 35.3%; "
                    "criticalexeget01meye (another copy, 1880) measures the same; the Funk & Wagnalls one-volume "
                    "issue criticalexegetic00meye 7.0% / 36.2%"),
    "meyer-mark-luke-2": _meyer(
        "criticalexegetic22meye", "6ac63a270d1f958035c6dbab864e8680a4ae175b40d926a9f24aa3ac901e6ad9",
        "Critical and Exegetical Handbook to the Gospels of Mark and Luke, vol. II", "Meyer, Mark-Luke II",
        f"{_MEY}: the Gospels of Mark and Luke, vol. II (Luke iii.-xxiv.), tr. Robert Ernest Wallis, revised "
        "and edited by William P. Dickson (MDCCCLXXX: 1880), as its title page reads", 1880,
        "Princeton Theological Seminary Library", (9, 381), [("Luke", 11, 381)], "1880",
        first_chapter={"Luke": 3},
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexegetic22meye: Greek 7.9%, known 36.8%; criticalexeget02meye (1880): 0.0% Greek"),
    "meyer-john": _meyer(
        "criticalexegetic04meye", "fe47adc8baa7f50621c494c909b567a86a5a4cea2ebaad78872bf6dd0b78f9d8",
        "Critical and Exegetical Hand-book to the Gospel of John", "Meyer, John",
        f"{_MEY_FUNK}: the Gospel of John, tr. from the fifth German edition by William Urwick, revised and "
        "edited by Frederick Crombie, with a preface and supplementary notes by A. C. Kendrick (New York: Funk "
        "& Wagnalls, 1884), as its title page reads", 1884, "Princeton Theological Seminary Library",
        (5, 596), [("John", 63, 579)], "1884", american="A. C. Kendrick",
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="every T&T Clark scan of John (1874-75, 1881, 1883) has 0.0% Greek; this Funk & Wagnalls "
                    "issue of the same translation keeps it: Greek 5.1%, known 42.1%; criticalandexeg01meyegoog "
                    "5.0% / 42.0% and commentaryonnew01unkngoog 5.1% / 42.0% are the same printing"),
    "meyer-romans": _meyer(
        "criticalexegetic06meye", "86abbfce229a86115080899b968073cbfa2eaf235a2526f69421b986b7e73055",
        "Critical and Exegetical Hand-book to the Epistle to the Romans", "Meyer, Romans",
        f"{_MEY_FUNK}: the Epistle to the Romans, tr. from the fifth German edition by John C. Moore and Edwin "
        "Johnson, revised and edited by William P. Dickson, with a preface and supplementary notes by Timothy "
        "Dwight (New York: Funk & Wagnalls, 1884), as its title page reads", 1884,
        "Princeton Theological Seminary Library", (7, 628), [("Rom", 58, 612)], "1884",
        american="Timothy Dwight", inline=False,
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="every T&T Clark scan of Romans (1873, 1874, 1881) has 0.0% Greek; this Funk & Wagnalls issue "
                    "keeps it: Greek 6.5%, known 40.5%; criticalandexeg03meyegoog and criticalandexege05meyeuoft "
                    "(the same issue): 0.0%"),
    "meyer-acts-1": _meyer(
        "criticalexegetic51meye", "32b16af1c81832fd678e4195b6a0a18872d580a3f9f20d286a2d622a7d29a27f",
        "Critical and Exegetical Handbook to the Acts of the Apostles, vol. I", "Meyer, Acts I",
        f"{_MEY}: the Acts of the Apostles, vol. I (chapters i.-xii.), tr. from the fourth German edition by "
        "Paton J. Gloag, revised and edited by William P. Dickson (MDCCCLXXVII: 1877), as its title page reads",
        1877, "Princeton Theological Seminary Library", (7, 340), [("Acts", 53, 338)], "1877",
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexegetic51meye (the Princeton set): Greek 6.2%, known 33.8%; criticalexegetic01meyeiala "
                    "6.1% / 33.4% and criticalexeget00meye 5.7% / 33.3%: not better"),
    "meyer-acts-2": _meyer(
        "criticalexegetic52meye", "5240ce3b1d0e3cb5178b8e1d4efa339920d1481d6cac87636840498564cd041d",
        "Critical and Exegetical Handbook to the Acts of the Apostles, vol. II", "Meyer, Acts II",
        f"{_MEY}: the Acts of the Apostles, vol. II (chapters xiii.-xxviii.), tr. Paton J. Gloag, revised and "
        "edited by William P. Dickson (MDCCCLXXVII: 1877), as its title page reads", 1877,
        "Princeton Theological Seminary Library", (9, 338), [("Acts", 13, 337)], "1877",
        first_chapter={"Acts": 13},
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexegetic52meye, the same Princeton set as vol. I: Greek 7.4%, known 31.0%"),
    "meyer-corinthians-1": _meyer(
        "criticalexegetic71meye", "fcaf4b22a50fb767972384cc029e1e53ae34a366397bf728c9d6ed4dbf1ac334",
        "Critical and Exegetical Handbook to the Epistles to the Corinthians, vol. I", "Meyer, Cor. I",
        f"{_MEY}: the Epistles to the Corinthians, vol. I (First Epistle, chapters i.-xiii.), tr. from the fifth "
        "German edition by D. Douglas Bannerman, revised and edited by William P. Dickson (MDCCCLXXVII: 1877), "
        "as its title page reads", 1877, "Princeton Theological Seminary Library", (9, 425),
        [("1Cor", 34, 424)], "1877",
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexegetic71meye (the Princeton set): Greek 7.3%, known 40.3%; criticalexege01meye "
                    "6.9% / 40.6% and the Funk & Wagnalls issue criticalexegetme00meye (1884) 7.3% / 41.0%: not "
                    "clearly better; criticalhandbook01meyeuoft is catalogued 1906-"),
    "meyer-corinthians-2": _meyer(
        "criticalexegetic72meye", "688cdcce28c09942f9e291efd9a6a1af23b4f8c19b4b1a4dfec3173932f06943",
        "Critical and Exegetical Handbook to the Epistles to the Corinthians, vol. II", "Meyer, Cor. II",
        f"{_MEY}: the Epistles to the Corinthians, vol. II (First Epistle, chapters xiv.-xvi., tr. D. Douglas "
        "Bannerman; Second Epistle, tr. from the fifth German edition by David Hunter; revised and edited by "
        "William P. Dickson) (MDCCCLXXIX: 1879), as its title page reads", 1879,
        "Princeton Theological Seminary Library", (13, 540), [("1Cor", 19, 142), ("2Cor", 151, 534)], "1877",
        ia_date_note="IA catalogues it 1877 (the set's first date); this volume's title page reads 1879",
        first_chapter={"1Cor": 14},
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexegetic72meye, the same Princeton set as vol. I: Greek 8.3%, known 41.0%"),
    "meyer-galatians": _meyer(
        "criticalexeget09meye", "411892e95302cbb1f492cbdffd0de25bcf2963465966c4dc6fb4153346dc707c",
        "Critical and Exegetical Handbook to the Epistle to the Galatians", "Meyer, Gal.",
        f"{_MEY}: the Epistle to the Galatians, tr. from the fifth German edition by "
        "\"Mr. Venables\", as the editor's preface names him (the title page's translator line is illegible "
        "in the scan's OCR) (MDCCCLXXIII: 1873), as its title page reads", 1873,
        "Princeton Theological Seminary Library", (13, 383), [("Gal", 39, 382)], "1873",
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexeget09meye (1873): Greek 6.3%, known 40.0%; the Funk & Wagnalls issue (1884: "
                    "criticalexegetic09meye, criticalexegetic0000hein_g2k4, criticalexegetic0000unse_b7h8): 0.0%"),
    "meyer-ephesians-philemon": _meyer(
        "criticalexegetic1880meye", "0bf00dc4bd21ea3933b778564ce4562be68397c054c6ce9fc47e26986ea856b3",
        "Critical and Exegetical Handbook to the Epistles to the Ephesians and to Philemon", "Meyer, Eph.-Philem.",
        f"{_MEY}: the Epistle to the Ephesians and the Epistle to Philemon, tr. from the fourth German edition by "
        "Maurice J. Evans, revised and edited by William P. Dickson (MDCCCLXXX: 1880), as its title page reads",
        1880, "Princeton Theological Seminary Library", (7, 405), [("Eph", 51, 374), ("Phlm", 379, 405)], "1880",
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexegetic1880meye: Greek 7.7%, known 37.5%; criticalexegetic10meye (another copy, 1880) "
                    "would not give its text (HTTP 500, 2026-10-03); the Funk & Wagnalls Ephesians "
                    "criticalandexeg05meyegoog (1884): 0.0%"),
    "meyer-philippians-colossians": _meyer(
        "criticalexeget11meye", "2b2efbc2833f053410fdd6974bfcf6644e2c358b81705d72c96daf27fee9f0e2",
        "Critical and Exegetical Handbook to the Epistles to the Philippians and Colossians", "Meyer, Phil.-Col.",
        f"{_MEY}: the Epistles to the Philippians and Colossians, tr. from the fourth German edition by John C. "
        "Moore, revised and edited by William P. Dickson (MDCCCLXXV: 1875), as its title page reads (the "
        "prefatory note: Philippians first translated by G. H. Venables)", 1875,
        "Princeton Theological Seminary Library", (9, 504), [("Phil", 27, 253), ("Col", 270, 503)], "1875",
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexeget11meye (1875): Greek 8.3%, known 37.6%; the Funk & Wagnalls issue (1885) "
                    "criticalexegetic11meye 7.5% / 38.9% and criticalexegeticphilcolphile00meye 7.5% / 38.9%: not "
                    "clearly better; criticalandexeg00unkngoog (1875), criticalexegetic0000hein_r9x0: 0.0%"),
    "huther-pastorals": _meyer(
        "criticalexeget15huth", "a2fd725f637a849b8f82fd9e0dca9c3102c976e8a3488a767be8eaa7699f1826",
        "Critical and Exegetical Handbook to the Epistles of St. Paul to Timothy and Titus", "Huther, Past.",
        f"{_MEY}: the Epistles to Timothy and Titus, by J. E. Huther, tr. from the fourth German edition by "
        "David Hunter (MDCCCLXXXI: 1881), as its title page reads", 1881,
        "Princeton Theological Seminary Library", (9, 394),
        [("1Tim", 87, 254), ("2Tim", 255, 345), ("Titus", 346, 393)], "1881", author="J. E. Huther",
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexeget15huth (1881): Greek 11.0%, known 35.9%; criticalexeget1881huth (another copy, "
                    "1881, IA rights unstated) 11.7% / 36.0%: not clearly better; the Funk & Wagnalls issue (1885) "
                    "criticalexegetic15huth 9.7% / 34.7%; criticalexegetictimtitu00huth, "
                    "criticalexegetic0000johe_z2x1, criticalexegetic0000johe_f5s9: 0.0%"),
    "lunemann-hebrews": _meyer(
        "criticalexegetic19ln", "db17601c5036be4a349a3577984ccb62e347acd05e9bfb6a510fc1e9bb1fb061",
        "Critical and Exegetical Handbook to the Epistle to the Hebrews", "Lünemann, Heb.",
        f"{_MEY}: the Epistle to the Hebrews, by Gottlieb Lünemann, tr. from the fourth German edition by "
        "Maurice J. Evans (MDCCCLXXXII: 1882), as its title page reads", 1882,
        "Princeton Theological Seminary Library", (9, 514), [("Heb", 87, 513)], "1882", author="Gottlieb Lünemann",
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexegetic19ln (1882): Greek 11.2%, known 34.0%; criticalexegeticheb00ln (1882): 0.0%"),
    "huther-james-john": _meyer(
        "criticalexeget20huth", "21c7b5d43162490d6d46c7ee2b2cdcf219ee83391a8c6edf782c6fb9afbed8d9",
        "Critical and Exegetical Handbook to the General Epistles of James and John", "Huther, Jas.-John",
        f"{_MEY}: the General Epistles of James and John, by J. E. Huther, James tr. Paton J. Gloag, John tr. "
        "Clarke H. Irwin (MDCCCLXXXII: 1882), as its title pages read", 1882,
        "Princeton Theological Seminary Library", (7, 542),
        [("Jas", 52, 241), ("1John", 278, 501), ("2John", 513, 528), ("3John", 529, 542)], "1882",
        author="J. E. Huther",
        ia_rights="NOT_IN_COPYRIGHT",
        scan_choice="criticalexeget20huth (1882): Greek 8.9%, known 42.3%; the Funk & Wagnalls issue (1887, with "
                    "Peter and Jude) criticalexegetic20huth 7.8% / 40.2%; criticalexegetic00huth (1882), "
                    "criticalexegetic0000johe_d6k9, criticalexegetic0000johe_g5m5: 0.0%"),
    "huther-peter-jude": _meyer(
        "criticalexegetichand1881huth", "a3c229ebd8f670fed6819808ba757879a35879aa7b690d1e4488901524c49e7a",
        "Critical and Exegetical Handbook to the General Epistles of Peter and Jude", "Huther, Pet.-Jude",
        f"{_MEY}: the General Epistles of Peter and Jude, by J. E. Huther, Peter tr. D. B. Croom, Jude tr. Paton "
        "J. Gloag (MDCCCLXXXI: 1881), as its title page reads", 1881,
        "Princeton Theological Seminary Library", (7, 452),
        [("1Pet", 53, 261), ("2Pet", 299, 391), ("Jude", 401, 452)], "1881", author="J. E. Huther",
        ia_rights=None,
        scan_choice="criticalexegetichand1881huth (1881, IA rights unstated; printed 1881): Greek 9.0%, known "
                    "36.8%; criticalexegetic21huth (1881) would not give its text (HTTP 500, 2026-10-03); "
                    "criticalexegetic0000johe, bwb_P9-AFQ-241_d0g5: 0.0%"),
}
SCANS.update(MEYER)
SECOND.update(MEYER)
ORDER.extend(MEYER)
MULTI.update(k for k, s in MEYER.items() if len(s["epistles"]) > 1)

MEYER_OPEN = re.compile(r'^[\W_]{0,2}(?:\[[^\]]{0,40}\]\s*)?V(?:[EeIi][RrNn][Ss]?|[vVy])\s?[.,:]?\s*(\d{1,3})'
                        r'((?:\s*(?:[,—–\-]+|\s+and)\s*\d{1,3}){0,6})'
                        r'(?:\s*f{1,2}\.|\s*[.,:;\]]|\s+ἢ\s|\s+(?=[Ͱ-Ͽἀ-῿]))')
# ('Ver. 7 ἢ Ἀδ.': the period read as ἢ; '[See Note LVII. p. 476.] Vv. 1, 2.': the American editor's pointer)
MEYER_SIGLA = re.compile(r'\b(?:Lachm|Tisch|Elz|Griesb|Scholz|Recepta|Rec|Curss?|Cursives|min|Codd|vss|Verss|'
                         r'Vulg|Copt|Sahid|Aeth|Arm|Goth|Syr|It)\b')
MEYER_CHAPTER = re.compile(r'^\W{0,3}[CGO0]\s?H\s?A\s?P\s?T\s?[EF]\s?[RBK]\w{0,2}[\W_]*\s*([^\d]{0,10})$')
MEYER_AMERICAN = re.compile(r'AMERICAN\s+E[a-zA-Z]{3,5}')
MEYER_ROMAN = str.maketrans({"l": "I", "1": "I", "|": "I", "!": "I", "Y": "V", "Ι": "I", "Χ": "X", "Υ": "V",
                             "v": "V", "i": "I", "x": "X"})


def meyer_open(text):
    """'Ver. 4.', 'VER. 1.', 'Vv. 2-6.', 'Vers. 14-19.': (None, n, end, 'read') or None."""
    m = MEYER_OPEN.match(text)
    if not m:
        return None
    n = int(m.group(1))
    nums = [int(x) for x in re.findall(r'\d{1,3}', m.group(2) or "")]
    e = nums[-1] if nums and nums[-1] > n else None
    return (None, n, e, "read") if n else None


def meyer_heading(l, nxt, after, W, H, mg):
    """A chapter heading: a short line set in from the margin, reading CHAPTER (fuzzily), or a short centred
    line followed by a paragraph of critical notes. The numbers its roman may be read as (() if none), or False."""
    words = l["text"].split()
    if not 1 <= len(words) <= 4 or l["bbox"][0] - mg < 0.12 * W or l["bbox"][1] < 0.08 * H:
        return False                    # (not a running head the page reader left in the body)
    m = MEYER_CHAPTER.match(l["text"])
    letters = [c for c in l["text"] if c.isalpha()]
    if not letters or sum(c.isupper() for c in letters) < 0.6 * len(letters):
        return False                    # a heading is in capitals
    o = meyer_open(nxt["text"]) if nxt is not None else None
    crit = o and (meyer_critical(nxt["text"], after) >= 2 or (
        o[1] <= 3 and len(words) <= 4 and l["bbox"][0] - mg > 0.25 * W))   # 'CELA DER Τ ΤΥ.' over 'Ver. 1.'
    if not m and not crit:
        return False
    tok = re.sub(r'[^A-Za-z|!1ΙΧΥ]', '', m.group(1) if m else words[-1]).translate(MEYER_ROMAN)
    out = []
    for t in (tok, tok[:-1] + "I" if tok.endswith("L") else None, tok[:-1] if tok.endswith("L") else None,
              tok.replace("L", "I")):       # a final L is an I, or the period
        if t and ROMAN_STRICT.fullmatch(t) and FS.roman(t) not in out:
            out.append(FS.roman(t))
    return tuple(out)                   # the readings (the caller takes the one that comes next), () if none


ROMAN_STRICT = re.compile(r'(?=[IVXL])L?X{0,3}(?:IX|IV|V?I{0,3})')


MEYER_DASH = re.compile(r'(?:[—–]|--+|-\s)\s*-?\s*(?=[VY])')


def meyer_inline(text, prev):
    """Openers run on inside a paragraph (Mark, Luke: 'Vv. 13-17. See on Matt. ix. 9-13. ... — Ver. 14.
    παράγων]'): 'Ver. N.' after a dash, or at the start of a line when the line before ends with one:
    [(pos, (None, n, end, 'read'))]."""
    out = []
    if prev.rstrip().endswith(("—", "–", "-")):
        o = meyer_open(text)
        if o:
            out.append((0, o))
    for d in MEYER_DASH.finditer(text):
        o = meyer_open(text[d.end():])
        if o and d.end() > 0:
            out.append((d.end(), o))
    return out


MEYER_UNCIALS = re.compile(r'(?<![\w.])(?!LXX\b)[ABCDEFGHKLMNPSUWXYZΓΔΘΛΞΠΨ]{2,7}\b|(?<![\w.])[A-Z]\*{1,2}')


def meyer_critical(text, nxt):
    """How much a paragraph's first lines read like Meyer's critical notes rather than his exegesis: the
    apparatus's sigla named (Lachm., Tisch., Elz., Recepta, min., vss....), a run of uncials ('BCLΔ', 'D*')
    counting as one. Two make a critical paragraph after a chapter's heading; in the exegesis it takes three."""
    t = text + " " + (nxt or "")
    return len(set(MEYER_SIGLA.findall(t))) + (1 if MEYER_UNCIALS.search(t) else 0)


def build_scan_meyer(slug, ids):
    s = SCANS[slug]
    P = pages(slug)
    a0, b0 = s["leaves"]
    seg = {}
    for book, x, y in s["epistles"]:
        for leaf in range(x, y + 1):
            seg[leaf] = book
    m = collections.Counter()
    units = []
    A = {leaf: analyse(P[leaf]) for leaf in range(a0, b0 + 1)}
    SC = {leaf: sc_page(P[leaf]) for leaf in range(a0, b0 + 1)}
    pp = printed_pages({leaf: sorted(set(A[leaf]["nums"]) | set(SC[leaf][1])) for leaf in A})
    kjv_counts = {book: verse_counts(ids, book) for book, _, _ in s["epistles"]}
    nch = {book: max(c) for book, c in kjv_counts.items()}
    items = []
    for leaf in range(a0, b0 + 1):
        a, book = A[leaf], seg.get(leaf)
        head, nums, body, foot, junk = SC[leaf]
        m["junk_lines_dropped"] += junk
        if not book:
            lines = [l for l, _ in body] + foot
            if lines:
                units.append(page_unit(slug, s, leaf, lines, dict(a, head=head or a["head"]), pp))
                m["leaves_page"] += 1
            continue
        m["leaves_commentary"] += 1
        # 'CHAP. XXVL 4, 5.': a final L after a roman is its I and the period (no NT book reaches chapter L)
        hc, hv = sc_head(re.sub(r'(?<=[IVX])L(?=[\s.,:;]|$)', 'I', head or ""), nch[book])
        hv = [v for v in hv if v not in nums]
        xs0 = sorted(l["bbox"][0] for l, _ in body if len(l["words"]) >= 4)
        mg = xs0[len(xs0) // 5] if xs0 else 0
        xs1 = sorted(l["bbox"][2] for l, _ in body if len(l["words"]) >= 4)
        right = xs1[len(xs1) // 2] if xs1 else P[leaf]["w"]
        for i, (l, para) in enumerate(body):
            nxt = body[i + 1][0] if i + 1 < len(body) else None
            after = " ".join(x["text"] for x, _ in body[i + 1:i + 4])     # the next three lines
            it = {"book": book, "leaf": leaf, "text": l["text"], "para": para, "cands": [], "hc": hc, "hv": hv}
            if s.get("american") and MEYER_AMERICAN.search(l["text"]) and len(l["text"].split()) <= 5:
                it["american"] = True
            else:
                h = meyer_heading(l, nxt, " ".join(x["text"] for x, _ in body[i + 2:i + 4]), P[leaf]["w"], P[leaf]["h"], mg)
                if h is not False:
                    it["heading"] = h
                else:
                    o = meyer_open(l["text"]) if para else None
                    # a paragraph of critical notes, indented or not (after a heading the OCR lost, the line
                    # before it ends a paragraph short of the measure)
                    starts = para or i == 0 or body[i - 1][0]["bbox"][2] < right - 0.15 * (right - mg)
                    score = meyer_critical(l["text"], after) if starts and meyer_open(l["text"]) else 0
                    if score >= 2:
                        it["critical"] = score
                    it["crit_score"] = score
                    if score < 2 or para:
                        it["cands"] = meyer_inline(l["text"], body[i - 1][0]["text"] if i else "") \
                            if s.get("inline", True) else []
                        if o:
                            it["cands"] = [(0, o)] + [c for c in it["cands"] if c[0] > 0]
            items.append(it)
        if foot:
            m["footnote_lines"] += len(foot)
            t = ""
            mid = (min(l["bbox"][0] for l in foot) + max(l["bbox"][2] for l in foot)) / 2
            cols = C.columns(foot, 2 * mid)       # Funk & Wagnalls set the footnotes in two columns
            m["footnote_blocks_two_columns"] += len(cols) == 2
            for col in cols:
                for l in col:
                    t = C.join(t, l["text"])
            items.append({"book": book, "leaf": leaf, "text": t, "foot": True, "cands": [], "hc": hc, "hv": hv})
    # running heads confirmed by a neighbour, as build_scan_2b
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
    decoders = {}
    for book in kjv_counts:
        d = HeadDecoder(kjv_counts[book])
        d.c = s.get("first_chapter", {}).get(book, 1)
        decoders[book] = d
    notes = decode_meyer(slug, items, decoders, pp, m)
    for key, nu in notes.items():
        book, kind = nu["book"], nu["kind"]
        links = []
        if nu["c"] is None:
            ref = f"{note_ref(s, book)}, before the first chapter"
        elif kind == "intro":
            ref = f"{note_ref(s, book)} {nu['c']}, chapter heading and critical notes"
        elif kind == "editor-notes":
            ref = f"{note_ref(s, book)} {nu['c']}, notes by the American editor ({s['american']})"
        else:
            vs = range(nu["n"], (nu["e"] or nu["n"]) + 1)
            links = [{"target": f"kjv:{book}.{nu['c']}.{v}", "type": "comments-on",
                      "resolved": f"kjv:{book}.{nu['c']}.{v}" in ids} for v in vs]
            ref = note_ref(s, book, nu["c"], nu["n"], nu["e"])
        u = {"id": f"{slug}:{key}", "ref": ref, "kind": kind, "book": book, "text": nu["text"], "links": links,
             "scan": {"leaves": nu["leaves"]}}
        if kind == "editor-notes":
            u["by"] = s["american"]
        if nu["pages"]:
            u["scan"]["printed_pages"] = nu["pages"]
        if nu["notes"]:
            u["notes"] = nu["notes"]
        units.append(u)
    order = {"page": 0, "intro": 1, "note": 1, "editor-notes": 1}
    units.sort(key=lambda u: (min(u["scan"]["leaves"]), order[u["kind"]]))
    return units, m, (a0, b0), pp


def decode_meyer(slug, items, decoders, pp, m):
    """decode_2b's verse sequence, with Meyer's chapter headings (each opens <c>.intro, the critical notes,
    and sets the sequence to that chapter) and the American editor's notes (<c>.american) between."""
    notes = collections.OrderedDict()
    current, last_ch, in_crit, crit_v = {}, {}, {}, {}
    flat = [(i, j) for i, it in enumerate(items) for j in range(len(it["cands"]))]
    seg, k = [], 0
    for it in items:
        k += 1 if ("heading" in it or it.get("critical")) else 0
        seg.append((it["book"], k))       # a chapter's heading closes the look-ahead
    ahead = {}
    for k, (i, j) in enumerate(flat):
        ahead[(i, j)] = [items[i2]["cands"][j2][1][:2] for i2, j2 in flat[k + 1:k + 7] if seg[i2] == seg[i]]

    def unit(key, book, kind, c=None, n=None, e=None):
        return notes.setdefault(key, {"book": book, "kind": kind, "c": c, "n": n, "e": e, "text": "", "leaves": [],
                                      "pages": [], "notes": []})

    def put(key, text, leaf, para):
        nu = notes[key]
        if text:
            nu["text"] = nu["text"] + "\n" + text if (para and nu["text"]) else C.join(nu["text"], text)
        if leaf not in nu["leaves"]:
            nu["leaves"].append(leaf)
            if leaf in pp and pp[leaf][0] not in nu["pages"]:
                nu["pages"].append(pp[leaf][0])

    def chapter(book, ch, it, how):
        dec = decoders[book]
        pre = ids_prefix(slug, book)
        dec.c, dec.v = ch, 0
        last_ch[book] = ch
        crit_v[book] = max([o[1] for _, o in it["cands"]] or [0])
        current[book] = f"{pre}{ch}.intro"
        m[how] += 1
        unit(current[book], book, "intro", ch)
        put(current[book], it["text"], it["leaf"], True)

    for i, it in enumerate(items):
        book, leaf = it["book"], it["leaf"]
        dec = decoders[book]
        pre = ids_prefix(slug, book)
        if book not in last_ch:
            last_ch[book] = dec.c - 1
        if current.get(book) is None:
            current[book] = f"{pre}title"
            unit(current[book], book, "intro")
        if it.get("foot"):
            unit(current[book], book, "intro")["notes"].append(it["text"])
            put(current[book], "", leaf, False)
            continue
        if "heading" in it:
            nxt_c = last_ch[book] + 1
            # of the readings ('IIL' is II or III), the next chapter first, else one skipped
            h = next((x for x in sorted(it["heading"]) if last_ch[book] < x <= last_ch[book] + 2 and x <= dec.nch), None)
            if h == nxt_c + 1 and nxt_c in (it["hc"], it["hc_next"]):
                h = nxt_c               # a heading that skips a chapter the running heads print ('XX.' for XIX.)
                m["chapter_headings_skip_refused"] += 1
            if h is not None:
                chapter(book, h, it, "chapter_headings_read")
            elif nxt_c <= dec.nch:
                chapter(book, nxt_c, it, "chapter_headings_unread_next")
            else:
                put(current[book], it["text"], leaf, True)
                m["chapter_headings_refused"] += 1
            continue
        crit = it.get("critical", 0)
        intro = current[book] == f"{pre}{last_ch[book]}.intro"
        if crit and (intro or current[book] == f"{pre}title"):
            put(current[book], it["text"], leaf, it["para"])      # more of the chapter's critical notes
            continue
        if intro:
            n0 = it["cands"][0][1][1] if it["cands"] and it["cands"][0][0] == 0 and it["para"] else 0
            if n0 and n0 > crit_v.get(book, 0) and (crit_v.get(book, 0) or (
                    it.get("crit_score") and notes[current[book]]["text"].count("\n") == 0 and len(
                        notes[current[book]]["text"]) < 40)):
                # (the first paragraph under a bare heading, naming the apparatus, opens them)
                # Huther gives a verse's readings a paragraph of its own ('Ver. 5. Instead of the Rec. ...'):
                # the critical notes run on through the verses; the exegesis starts again from a lower one
                put(current[book], it["text"], leaf, it["para"])
                crit_v[book] = max([o[1] for _, o in it["cands"]])
                m["critical_paragraphs_by_verse"] += 1
                continue
            crit_v[book] = max([crit_v.get(book, 0)] + [o[1] for p, o in it["cands"] if p > 0 or not it["para"]])
        if crit == 2 and it["para"] and it["cands"]:
            crit = 0                    # in the exegesis two sigla are not enough: an opener (see meyer_critical)
            m["openers_naming_sigla"] += 1
        if crit:
            hn = it["hc_next"]
            nxt_c = last_ch[book] + 1
            if nxt_c <= dec.nch and current[book] != f"{pre}{last_ch[book]}.intro" and (
                    it["hc"] == nxt_c or hn == nxt_c or dec.v >= dec.counts.get(dec.c, 0) - 3):
                # a critical paragraph whose heading the OCR lost: the chapter turns here
                chapter(book, nxt_c, it, "chapter_headings_implied")
                continue
            m["critical_paragraphs_in_text"] += 1
        if it.get("american"):
            current[book] = f"{pre}{dec.c}.american"
            unit(current[book], book, "editor-notes", dec.c)
            put(current[book], it["text"], leaf, True)
            m["american_blocks"] += 1
            continue
        if current[book].endswith(".american") and not it["cands"]:
            put(current[book], it["text"], leaf, it["para"])
            continue
        if current[book].endswith(".american"):
            m["openers_in_american_notes"] += 1
            put(current[book], it["text"], leaf, it["para"])
            continue
        if crit:
            in_crit[book] = True        # a critical paragraph left in the text: its 'Ver.'s are readings
            it = dict(it, cands=[])
        elif it["para"]:
            in_crit[book] = False
        hc, hsure = it["hc"], it["hsure"]
        if hc is None and it.get("hc_next") is not None and it["hc_next"] > dec.c:
            hc = it["hc_next"]
        if hc is not None and hc < dec.c:
            hc, hsure = None, False     # the headings set the chapter: a running head never takes it back
        pos, para = 0, it["para"]
        for j, (p, o) in enumerate(it["cands"]):
            cp, n, e, how = o
            nxt = ahead[(i, j)]
            if not (p == 0 and it["para"]) and (in_crit.get(book) or not notes[current[book]]["kind"] == "note"):
                m["inline_openers_outside_notes"] += 1     # the critical notes run their verses on inline too
                continue
            if n > dec.v + 1 and any(a[0] is None and dec.v < a[1] < n for a in nxt[:3]):
                m["openers_out_of_sequence"] += 1
                continue
            took = dec.offer(n, e, hc, it["hv"], cp, hsure, nxt)
            m["openers_accepted" if took else "openers_rejected"] += 1
            if not took:
                continue
            c, n2, _ = took
            if it["hsure"] and it["hc"] != c:
                m["openers_against_running_head"] += 1
            if c != last_ch[book]:
                m["chapter_turns_without_heading"] += 1
                last_ch[book] = c
            e2 = e if (e and n2 < e <= dec.counts.get(c, 0) and e - n2 <= 60) else None
            put(current[book], it["text"][pos:p].strip(), leaf, para)
            key = f"{pre}{c}.{n2}" + (f"-{e2}" if e2 else "")
            if key in notes:
                m["notes_reopened"] += 1
            unit(key, book, "note", c, n2, e2)
            current[book] = key
            pos, para = p, True
        put(current[book], it["text"][pos:].strip(), leaf, para)
    return notes


def citation_meyer(slug):
    lead = "book.chapter.verse" if slug in MULTI else "chapter.verse"
    am = "; the American editor's notes: <chapter>.american" if SCANS[slug].get("american") else ""
    return (f"note: {lead} of the verse commented on (a run of verses: {lead}-end); a chapter's heading and "
            f"critical notes: {lead.rsplit('.', 1)[0]}.intro{am}; everything else: scan leaf (leaf.N; folio in "
            "scan.printed_page)")


MEYER_HONESTY = (
    "notes keyed by verse where the OCR'd page lets them be: the exegesis (Meyer's, or Huther's or "
    "Lünemann's in the volumes they wrote for his series) opens each verse's paragraph 'Ver. 4.' or "
    "'Vv. 2-6.', and an indented paragraph so opening is a candidate, accepted when the verse sequence and "
    "the running head ('CHAP. XVII. 4-8.') allow it; following paragraphs belong to it until the "
    "next accepted opener; the chapter is set by the 'CHAPTER IV.' headings, read fuzzily (a heading whose "
    "number is unread is taken as the next chapter: measure.chapter_headings_unread_next; one the OCR lost, "
    "from a critical paragraph where the running heads turn: chapter_headings_implied; a heading whose number "
    "would skip a chapter the running heads print is read as that chapter: chapter_headings_skip_refused), and "
    "each heading with the critical notes on the chapter's readings that follow it is the unit "
    "<chapter>.intro (where a verse's readings take a paragraph of their own, as in Huther, the critical notes "
    "run on until the exegesis starts again from a lower verse: critical_paragraphs_by_verse), a paragraph "
    "of critical notes found elsewhere staying in the text where it stands (critical_paragraphs_in_text); "
    "the American editor's notes (Funk & Wagnalls issues) are <chapter>.american, the chapter they follow; "
    "the translators' footnotes (the smaller type at a page's foot) go in `notes` of the unit open at that "
    "point; boundaries are only as good as the numbers read off the page, and a misread or rejected number "
    "merges a verse's notes into the verse before (counts in measure); introductions, prefaces and index by "
    "scan leaf (leaf.N, the folio in scan.printed_page where read); the Hebrew words are lost (no Hebrew "
    "script survives: measure.hebrew; the OCR gave Latin- or Greek-letter debris, left as it stands); "
    "unproofread OCR")

SCAN_READERS = {"meyer": build_scan_meyer}
READER_TEXTS = {"meyer": {"honesty": MEYER_HONESTY, "citation": citation_meyer}}


# ================================================================== Keil & Delitzsch: Job, Proverbs, Isaiah (4d)
#
# Franz Delitzsch on Job (2 vols), on Proverbs (2 vols) and on Isaiah (2 vols), in the T. & T. Clark
# translation (Clark's Foreign Theological Library), read by their own reader, `kdh`: these volumes print
# few 'Ver. 3.' openers (Job 40-63 a volume, Isaiah 113-340), so the `kd` reader would leave most verses
# unkeyed. What they all print is a RUNNING HEAD on every recto naming the chapter and the verses the page
# treats ('CHAP. III. 10-12. 79', 'CHAPTER XL. 9. 139'; the verso prints only the book's name), and Job
# and Proverbs print the translation of each strophe or proverb with its verse numbers at the line starts
# ('6 That night! let darkness ...'). The reader (build_scan_kdh):
#   1. reads each recto's head into candidate readings (kdh_head: the chapter's roman numeral with the
#      usual OCR confusions undone, the verse or run after it, a run crossing into the next chapter
#      'IX. 34-X. 2', the folio dropped where it is the expected one; old-style figures the OCR swaps,
#      3/8, 1/7, 5/6, 0/9, offered as costlier readings), and decodes them AS A SEQUENCE (kdh_decode,
#      a shortest path: a head's verse may not run backwards, nor leap further ahead than the leaves
#      between allow; a head that fits no path is dropped and counted, running_heads_out_of_order);
#   2. keys each commentary leaf by its decoded head ('running-head'), or a leaf without one (a verso,
#      a head unread or dropped) by the run between the heads around it, from the verse the last head
#      ends at to the verse the next one starts at ('inferred'); a run may cross a chapter
#      ('3.24-4.2'); a leaf whose run would exceed KDH_MAX_RUN verses is a page unit, unkeyed;
#   3. inside the leaves, an opener ('Ver. 8:', 'Vers. 9-11.') or a translation block (indented lines
#      opening with a verse number: the block's first number to its last) that falls inside the leaf's
#      run (two verses' slack) opens its own unit ('opener', 'translation'), which runs on into the next
#      leaf while that leaf's run still reaches its verses;
#   4. units with the same key (a run printed on two rectos, an opener's unit and a head's) are one unit.
# Every unit says how its key was got (`keyed_by`). The numbering is measured as the `kd` volumes'
# (numbering_votes over the decoded heads and the accepted openers; work_numbering pools them with any
# `kd` volume of the same book).
# Scans: see KD4D_CHOICE (every candidate measured with this reader, 2026-10-03).

KD_READERS = {"kd", "kdh"}          # readers whose numbering is measured (harvest_2b, work_numbering)
KDH_MAX_RUN = 40                     # a leaf inferred to span more verses than this is a page unit
KDH_SKIP = 2.0                       # the cost of dropping a running head from the sequence

KDH_ROMAN_FIX = str.maketrans({"1": "I", "|": "I", "!": "I", "Ι": "I", "Χ": "X", "Υ": "V", "'": "", "’": "",
                               "‘": "", "`": ""})
KDH_ROMAN = re.compile(r'(?=[IVXLC])(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})')   # I to LXXXIX
KDH_DIG = str.maketrans({"I": "1", "l": "1", "i": "1", "|": "1", "O": "0", "o": "0", "S": "5", "s": "5",
                         "G": "6", "b": "6", "g": "9", "Z": "2", "z": "2", "B": "8", "T": "7", "J": "1"})
KDH_CHAPWORD = re.compile(r'^[^\w]*[CcGOe][a-zA-Z\'’]{0,4}[AaPpRr][a-zA-Z\'’]{0,5}[.,:]*$|^[CcGO][HhUu]?\.?$|^AP\.?$')
KDH_VERLINE = re.compile(r'^[\W_]{0,2}Vers?\.\s*(\d{1,2})(?:\s*[-—–,]\s*(\d{1,2}))?\s+(?=[A-Z“"‘\'(])')   # 'Ver. 22 Jahve's ...'
KDH_NUMLINE = re.compile(r'^[\W_]{0,2}([0-9IlOoSGgZB]{1,2})[.,]?\s+(?=[A-Z“"‘\'(])')


def kdh_romans(tok):
    """[(chapter, cost)] that a running head's chapter token may be: as read (0), with T/Y/R read as
    I/V/I (0.3), a final L as I ('XVIL', 'IIL': 0.5), every L as I (0.8)."""
    t = tok.translate(KDH_ROMAN_FIX).strip(".,:;")
    if not t or not t.isalpha() or len(t) > 9:
        return []
    out, seen = [], set()
    v0 = t.replace("l", "I").upper()
    v1 = v0.replace("T", "I").replace("Y", "V").replace("R", "I")
    v2 = v1[:-1] + "I" if v1.endswith("L") and len(v1) > 1 else None
    v3 = v1.replace("L", "I")
    v4 = v1 + "I"                                  # a final I lost ('XXXII' for 'XXXIII')
    for v, cost in ((v0, 0.0), (v1, 0.3), (v2, 0.5), (v3, 0.8), (v4, 0.9)):
        if v and v not in seen and KDH_ROMAN.fullmatch(v):
            seen.add(v)
            n = FS.roman(v)
            if n and n not in [x[0] for x in out]:
                out.append((n, cost))
    return out


def kdh_num(tok):
    t = tok.strip(".,:;’‘'\"_()[]*")
    if not t or len(t) > 3 or not (any(ch.isdigit() for ch in t) or (len(t) <= 2 and set(t) <= set("IlOoSG"))):
        return None
    u = t.translate(KDH_DIG)
    return int(u) if u.isdigit() else None


def kdh_head(text, folio=None, vmax=60):
    """Candidate readings (c1, v1, c2, v2, cost) of a recto running head: 'CHAP. III. 10-12. 79' ->
    (3, 10, 3, 12); 'CHAP. IX. 84-X. 2.' -> (9, 34, 10, 2) among others; 'CHAPTER LX. 381' -> (60, 0, 60, 0)
    (a chapter, no verse). [] where the head names no chapter (a verso's 'THE BOOK OF JOB.', an
    introduction's). The folio is dropped where it reads as `folio` (or, unknown, where it is past any
    verse the book has, `vmax`)."""
    t = re.sub(r'[—–~]', '-', text.replace("|", " "))
    toks = t.split()
    if not toks:
        return []
    # the folio: last token (recto) or first (verso)
    for idx in (-1, 0):
        if len(toks) < 2:
            break
        d = toks[idx].strip(".,:;’‘'\"_()[]*-").translate(KDH_DIG)
        if d.isdigit() and ((folio is not None and (d == str(folio) or (d.endswith(str(folio)) and len(d) <= len(str(folio)) + 1)))
                            or (idx == -1 and int(d) > vmax)):
            toks = toks[:-1] if idx == -1 else toks[1:]
    chap_word = False
    for i, tok in enumerate(toks[:4]):
        if KDH_CHAPWORD.match(tok):
            chap_word = True
            continue
        rs = kdh_romans(tok)
        if not rs:
            continue
        rest = " ".join(toks[i + 1:])
        if not chap_word and not re.match(r'^\s*[\dIlOoSGgZB]', rest):
            return []
        return kdh_verses(rs, rest)
    return []


def kdh_verses(rs, rest):
    """The verse part of a running head after its chapter: '10-12.', '4, 5.', '84-X. 2.', '32, XI. 1.',
    '611' (a hyphen lost: 6-11)."""
    parts = re.findall(r'[IVXLC]{1,7}\.|[A-Za-z0-9]+|[-,;]', rest)
    nums, c2at = [], None
    for k, p in enumerate(parts):
        if p in "-,;":
            continue
        if p.endswith(".") and re.fullmatch(r'[IVXLC]{1,7}\.', p) and k + 1 < len(parts) \
                and kdh_num(parts[k + 1]) is not None and nums and c2at is None and FS.roman(p[:-1]):
            c2at = (len(nums), FS.roman(p[:-1]))
            continue
        n = kdh_num(p)
        if n is not None:
            nums.append(n)
    out = []
    for c, rc in rs:
        if not nums:
            out.append((c, 0, c, 0, rc))
            continue
        if c2at:
            k, c2 = c2at
            if k < len(nums):
                v1s, v2s = nums[0], nums[k]
                out += [(c, a, c2, b, rc + 0.6 * ((a != v1s) + (b != v2s)))
                        for a in C.alts(v1s) for b in C.alts(v2s)]
                continue
        v1, v2 = nums[0], nums[-1]
        reads = [(v1, v2, 0.0)] if v2 >= v1 else [(v1, v2, 0.0), (v1, v1, 0.4)]
        if v1 >= 100:
            s = str(v1)                        # '611': 6-11 with its hyphen lost
            reads = [(int(s[:j]), int(s[j:]), 0.6) for j in range(1, len(s)) if s[j] != "0"]
        for a0, b0, rr in reads:
            for a in C.alts(a0):
                for b in C.alts(b0):
                    out.append((c, a, c, b, rc + rr + 0.6 * ((a != a0) + (b != b0))))
    return out


def kdh_page(p):
    """sc_page, with the running head found where sc_page missed it (OCR debris above it at the scan's
    edge): a short line, mostly capitals, with a number, in the top sixth of the page among the first
    body lines; the debris above it is dropped and counted with the junk."""
    head, nums, body, foot, junk = sc_page(p)
    if head and re.search(r'\d', head):
        return head, nums, body, foot, junk
    for i, (l, _) in enumerate(body[:6]):
        if l["bbox"][1] > 0.16 * p["h"]:
            break
        letters = [c for c in l["text"] if c.isalpha()]
        if len(l["words"]) <= 10 and letters and sum(c.isupper() for c in letters) >= 0.5 * len(letters) \
                and re.search(r'\d', l["text"]) and len(letters) >= 3:
            top = l["bbox"][1]
            above = [x for x, _ in body[:i] if x["bbox"][3] <= top + 0.3 * (l["bbox"][3] - top)]
            if len(above) < i:
                break
            toks = l["text"].split()
            nums = [int(x) for x in (toks[0], toks[-1]) if re.fullmatch(r'\d{1,3}', x)]
            return l["text"], nums, body[i + 1:], foot, junk + len(above)
    return head, nums, body, foot, junk


def kdh_decode(heads, counts, fc, start_leaf):
    """The running heads as a sequence: a shortest path over each head's readings (heads in leaf
    order), where a head's first verse may not come before the last head's, nor leap further ahead
    than the leaves between allow; dropping a head costs KDH_SKIP. -> ({leaf: reading}, [dropped leaf])."""
    cum, tot = {}, 0
    for c in range(1, max(counts) + 1):
        cum[c] = tot
        tot += counts.get(c, 0)
    P = lambda c, v: cum[c] + v  # noqa: E731

    def ok(r):
        c1, v1, c2, v2, _ = r
        return c1 in cum and c2 in cum and 0 <= v1 <= counts.get(c1, 0) and v2 <= counts.get(c2, 0) \
            and (v1 > 0 or v2 == 0) and P(c1, v1) <= P(c2, v2) <= P(c1, v1) + 40 and (v1 > 0 or c1 == c2)
    H = [(leaf, [r for r in rs if ok(r)]) for leaf, rs in heads]
    H = [(leaf, rs) for leaf, rs in H if rs]

    def trans(prev, pl, r, leaf):
        s0, e0, s1 = P(prev[0], prev[1]), P(prev[2], prev[3]), P(r[0], r[1])
        if s1 < s0:
            return None
        pages = max(1, (leaf - pl + 1) // 2)
        gap = s1 - e0
        if gap > 25 + 8 * pages:
            return None
        return 0.08 * max(0, gap - 4 * pages)
    start = (fc, 0, fc, 0, 0.0)
    best = []
    W = 30
    for i, (leaf, rs) in enumerate(H):
        row = []
        for r in rs:
            cand = []
            t = trans(start, start_leaf, r, leaf)
            if t is not None:
                cand.append((KDH_SKIP * i + t + r[4], None))
            for j in range(max(0, i - W), i):
                for kk, (cj, _) in enumerate(best[j]):
                    t = trans(H[j][1][kk], H[j][0], r, leaf)
                    if t is not None:
                        cand.append((cj + KDH_SKIP * (i - j - 1) + t + r[4], (j, kk)))
            row.append(min(cand, key=lambda x: x[0]) if cand else (float("inf"), None))
        best.append(row)
    n = len(H)
    end = (KDH_SKIP * n, None)
    for i in range(n):
        for k, (c, _) in enumerate(best[i]):
            if c + KDH_SKIP * (n - 1 - i) < end[0]:
                end = (c + KDH_SKIP * (n - 1 - i), (i, k))
    chosen = {}
    at = end[1]
    while at is not None:
        i, k = at
        chosen[H[i][0]] = H[i][1][k]
        at = best[i][k][1]
    dropped = [leaf for leaf, _ in H if leaf not in chosen]
    return chosen, dropped, [leaf for leaf, rs in heads if rs and leaf not in dict(H)]


def kdh_span_key(c1, v1, c2, v2):
    if c1 == c2:
        return f"{c1}.{v1}" + (f"-{v2}" if v2 != v1 else "")
    return f"{c1}.{v1}-{c2}.{v2}"


def kdh_verses_of(c1, v1, c2, v2, counts):
    out = []
    for c in range(c1, c2 + 1):
        a = v1 if c == c1 else 1
        b = v2 if c == c2 else counts.get(c, 0)
        out += [(c, v) for v in range(a, b + 1)]
    return out


def build_scan_kdh(slug, ids, votes_only=False):
    s = SCANS[slug]
    P = pages(slug)
    a0, b0 = s["leaves"]
    seg = {}
    for book, x, y in s["epistles"]:
        for leaf in range(x, y + 1):
            seg[leaf] = book
    m = collections.Counter()
    units = []
    A = {leaf: analyse(P[leaf]) for leaf in range(a0, b0 + 1)}
    SC = {leaf: kdh_page(P[leaf]) for leaf in range(a0, b0 + 1)}
    pp = printed_pages({leaf: sorted(set(A[leaf]["nums"]) | set(SC[leaf][1])) for leaf in A})
    kjv_counts = {book: verse_counts(ids, book) for book, _, _ in s["epistles"]}
    counts = {}
    for book, kc in kjv_counts.items():
        hc_ = heb_counts(book)
        counts[book] = {c: max(n, hc_.get(c, 0)) for c, n in set(kc.items()) | set(hc_.items())}
    vmax = {book: max(c.values()) for book, c in counts.items()}
    # 1. the running heads, decoded as a sequence per book
    decoded, how = {}, {}
    for book, x, y in s["epistles"]:
        heads = []
        for leaf in range(x, y + 1):
            rs = kdh_head(SC[leaf][0], pp.get(leaf, (None,))[0], vmax[book])
            if rs:
                heads.append((leaf, rs))
        fc = s.get("first_chapter", {}).get(book, 1)
        got, dropped, unread = kdh_decode(heads, counts[book], fc, x - 1)
        m["running_heads_read"] += len(got)
        m["running_heads_out_of_order"] += len(dropped)
        m["running_heads_unreadable"] += len(unread)
        m["running_heads_fixed"] += sum(1 for r in got.values() if r[4] > 0)
        for leaf, r in got.items():
            if r[1] == 0:
                m["running_heads_chapter_only"] += 1
            else:
                decoded[leaf] = r[:4]
                how[leaf] = "running-head"
    # 2. each commentary leaf's run
    span = {}
    for book, x, y in s["epistles"]:
        fc = s.get("first_chapter", {}).get(book, 1)
        hl = sorted(leaf for leaf in decoded if x <= leaf <= y)
        cnt = counts[book]
        for leaf in range(x, y + 1):
            if leaf in decoded:
                span[leaf] = decoded[leaf]
                continue
            prev = [q for q in hl if q < leaf]
            nxt = [q for q in hl if q > leaf]
            a = decoded[prev[-1]][2:4] if prev else (fc, 1)
            b = decoded[nxt[0]][0:2] if nxt else (a[0], cnt.get(a[0], a[1]))
            if (a[0], a[1]) > (b[0], b[1]):
                a, b = b, a
            span[leaf] = (a[0], a[1], b[0], b[1])
            how[leaf] = "inferred"
            if len(kdh_verses_of(*span[leaf], cnt)) > KDH_MAX_RUN:
                span[leaf] = None
    # 3. the stream: openers and translation blocks inside each leaf's run
    segs = []            # {book, c1, v1, c2, v2, how, text, leaves, pages, notes}
    pairs = collections.defaultdict(list)
    for leaf, r in decoded.items():
        pairs[seg[leaf]] += [(seg[leaf], r[0], r[1]), (seg[leaf], r[2], r[3])]
    cur = {}

    def P_(book, c, v):
        return sum(counts[book].get(k, 0) for k in range(1, c)) + v

    def new(book, c1, v1, c2, v2, kind, leaf):
        sg = {"book": book, "c1": c1, "v1": v1, "c2": c2, "v2": v2, "how": kind, "text": "", "leaves": [],
              "pages": [], "notes": [], "open": kind == "translation", "own_end": (c2, v2)}
        segs.append(sg)
        cur[book] = sg
        add(sg, "", leaf, False)
        return sg

    def add(sg, text, leaf, para):
        if text:
            sg["text"] = sg["text"] + "\n" + text if (para and sg["text"]) else C.join(sg["text"], text)
        if leaf not in sg["leaves"]:
            sg["leaves"].append(leaf)
            if leaf in pp and pp[leaf][0] not in sg["pages"]:
                sg["pages"].append(pp[leaf][0])

    def fit(book, n, sp, after):
        """The chapter an opener's verse n belongs to inside the leaf's run sp (two verses' slack), at or
        after `after`; None where it lies outside."""
        c1, v1, c2, v2 = sp
        rng = [(c1, v1 - 2, (v2 if c1 == c2 else counts[book].get(c1, 0)) + 2)]
        if c2 != c1:
            rng.append((c2, 1, v2 + 2))
        for c, lo, hi in rng:
            if lo <= n <= hi and 1 <= n <= counts[book].get(c, 0) and (after is None or P_(book, c, n) >= after):
                return c
        return None

    for leaf in range(a0, b0 + 1):
        a = A[leaf]
        book = seg.get(leaf)
        head, _, body, foot, junk = SC[leaf]
        m["junk_lines_dropped"] += junk
        if not book or span.get(leaf) is None:
            lines = [l for l, _ in body] + foot
            if lines:
                u = page_unit(slug, s, leaf, lines, dict(a, head=head or a["head"]), pp)
                if book:
                    u["book"] = book
                    u["scan"]["between_running_heads"] = "the run inferred here exceeds " + str(KDH_MAX_RUN) + " verses"
                    m["leaves_unkeyed"] += 1
                else:
                    m["leaves_page"] += 1
                units.append(u)
            cur.pop(book, None)
            continue
        m["leaves_commentary"] += 1
        sp = span[leaf]
        c = cur.get(book)
        floor, carried = None, None
        if c and c["how"].split("-")[0] in ("opener", "translation") and \
                P_(book, *c["own_end"]) >= P_(book, sp[0], sp[1]) - 1 and P_(book, c["c1"], c["v1"]) <= P_(book, sp[2], sp[3]):
            add(c, "", leaf, False)            # an opener's note running on into this leaf
            floor = P_(book, c["c1"], c["v1"])
            carried = c
        else:
            c = new(book, *sp, how[leaf], leaf)
        for l, para in body:
            text = l["text"]
            cands = []
            mt = KDH_NUMLINE.match(text)
            mv = KDH_VERLINE.match(text) if para else None
            cc = cur[book]
            if mt and kdh_num(mt.group(1)) and (para or (cc["how"].startswith("translation") and cc["open"])):
                # a translation line; one set flush (its number's box read short) only continuing a block
                cands.append((0, kdh_num(mt.group(1)), None, "translation" if para else "translation-cont"))
            elif mv and not kd_cands(text):
                cands.append((0, int(mv.group(1)), int(mv.group(2)) if mv.group(2) else None, "opener"))
            else:
                cands += [(p, o[1], o[2], "opener") for p, o in kd_cands(text)]
            pos = 0
            for p, n, e, kind in cands:
                cc = cur[book]
                if kind.startswith("translation") and cc["how"].startswith("translation") and cc["open"] \
                        and cc["c2"] == cc["c1"] and cc["v2"] < n <= cc["v2"] + 3 and n <= counts[book].get(cc["c2"], 0):
                    cc["v2"] = n                 # the next verse of the same translation block
                    cc["own_end"] = (cc["c2"], n)
                    m["translation_lines"] += 1
                    continue
                if kind == "translation-cont":
                    continue
                ch = fit(book, n, sp, floor)
                if ch is None:
                    m[f"{kind}s_rejected"] += 1
                    continue
                if e and not (n < e <= counts[book].get(ch, 0) and e - n <= 15):
                    e = None
                add(cc, text[pos:p].strip(), leaf, para)
                new(book, ch, n, ch, e or n, kind, leaf)
                m[f"{kind}s_accepted"] += 1
                if kind == "translation":
                    m["translation_lines"] += 1
                pairs[book] += [(book, ch, n)] + ([(book, ch, e)] if e else [])
                floor = P_(book, ch, n)
                pos, para = p, True
            if not para and cur[book]["open"] and pos == 0 and not mt:
                cur[book]["open"] = False       # a flush line: the translation block has ended
            add(cur[book], text[pos:].strip(), leaf, para)
        if carried is not None and cur[book] is carried and P_(book, sp[2], sp[3]) > P_(book, carried["c2"], carried["v2"]) \
                and len(kdh_verses_of(carried["c1"], carried["v1"], sp[2], sp[3], counts[book])) <= 15:
            # an opener's note filling a leaf with no opener of its own: it runs to the verse the leaf's
            # run ends at (its head's, or the next head's start)
            carried["c2"], carried["v2"] = sp[2], sp[3]
            if not carried["how"].endswith("-to-head"):
                carried["how"] += "-to-head"
                m["openers_run_to_head"] += 1
        if foot:
            m["footnote_lines"] += len(foot)
            t = ""
            for l in foot:
                t = C.join(t, l["text"])
            cur[book]["notes"].append(t)
    # the numbering the volume's own verses are in, measured as the `kd` volumes'
    numbering = {}
    for book in kjv_counts:
        v = numbering_votes(pairs[book], ids)
        v["decision"] = decide(v)
        numbering[book] = v
    if votes_only:
        return numbering
    _OWN[slug] = {b: dict(v) for b, v in numbering.items()}
    m["numbering_own"] = numbering
    # 4. units: one per key
    notes = collections.OrderedDict()
    for sg in segs:
        if not sg["text"].strip() and not sg["notes"]:
            m["empty_segments_dropped"] += 1
            continue
        key = ids_prefix(slug, sg["book"]) + kdh_span_key(sg["c1"], sg["v1"], sg["c2"], sg["v2"])
        if key in notes:
            nu = notes[key]
            if nu["leaves"][-1] < sg["leaves"][0] - 1 or nu is not next(reversed(notes.values())):
                m["notes_rejoined"] += 1
            nu["text"] = nu["text"] + "\n" + sg["text"] if nu["text"] else sg["text"]
            for leaf in sg["leaves"]:
                if leaf not in nu["leaves"]:
                    nu["leaves"].append(leaf)
            nu["pages"] += [x for x in sg["pages"] if x not in nu["pages"]]
            nu["notes"] += sg["notes"]
            continue
        notes[key] = dict(sg)
    for key, nu in notes.items():
        book = nu["book"]
        nb = effective(numbering[book]["decision"], book, ids, "")[0]
        links = []
        for c, v in kdh_verses_of(nu["c1"], nu["v1"], nu["c2"], nu["v2"], counts[book]):
            lk = dict(ot_link(book, c, v, nb, ids, "comments-on"), type="comments-on")
            lk.pop("rule", None)
            links.append(lk)
        who = s["short"].split(",")[0]
        ref = f"{who} on {book} " + kdh_span_key(nu["c1"], nu["v1"], nu["c2"], nu["v2"])
        u = {"id": f"{slug}:{key}", "ref": ref, "kind": "note", "book": book, "text": nu["text"].strip(),
             "keyed_by": nu["how"], "links": links, "scan": {"leaves": nu["leaves"]}}
        if nu["pages"]:
            u["scan"]["printed_pages"] = nu["pages"]
        if nu["notes"]:
            u["notes"] = nu["notes"]
        units.append(u)
        m[f"notes_keyed_by_{nu['how'].replace('-', '_')}"] += 1
    order = {"page": 0, "note": 1}
    units.sort(key=lambda u: (min(u["scan"]["leaves"]), order[u["kind"]]))
    return units, m, (a0, b0), pp


def citation_kdh(slug):
    lead = "book.chapter.verse" if slug in MULTI else "chapter.verse"
    return (f"note: {lead} of the verse commented on, in the numbering the volume prints (scheme.numbering); a run "
            f"of verses: {lead}-end, a run crossing a chapter: chapter.verse-chapter.verse (each unit's keyed_by "
            "says how: opener, translation, running-head, inferred); everything else: scan leaf (leaf.N; folio in "
            "scan.printed_page)")


KDH_HONESTY = (
    "notes keyed by the RUNNING HEADS where the OCR'd page has no better mark: each recto's head ('CHAP. III. "
    "10-12.') read with the OCR's usual confusions undone and decoded as a sequence (a head that does not fit "
    "the sequence is dropped: measure.running_heads_out_of_order; one read only with a figure or numeral "
    "changed: running_heads_fixed); a leaf with a decoded head is the unit of the verses it names "
    "(keyed_by running-head), a leaf without one (every verso, and a head unread or dropped) the run between "
    "the heads around it, from the verse the last head ends at to the verse the next begins at (keyed_by "
    "inferred), a run that may cross a chapter; so a unit's verses are the verses the PAGES print in their "
    "heads, not a note's own boundaries, and a page's text about a verse outside its head's run (the end of "
    "one section, the opening of the next) sits under that run; a leaf whose inferred run would exceed "
    f"{KDH_MAX_RUN} verses is a page unit (leaves_unkeyed); inside a leaf's run, an opener ('Ver. 8:', "
    "'Vers. 9-11.') or a block of translation lines opening with verse numbers ('6 That night ...', the "
    "block's first verse to its last) opens its own unit (keyed_by opener, translation) where its verse lies "
    "inside the run, two verses' slack, and not behind an opener already taken on the leaf (else it stays in "
    "the text, counted rejected); that unit runs on into the next leaf while that leaf's run reaches its "
    "verses, and where that leaf opens no unit of its own, the unit is widened to the end of the leaf's run "
    "(at most 15 verses; keyed_by opener-to-head, translation-to-head: measure.openers_run_to_head), since "
    "the page's text then reaches verses the opener did not name; units of one key are one unit, a key met again later joining its text (notes_rejoined); ids are "
    "in the numbering the volume prints, MEASURED per book (measure.numbering_own) and linked to the KJV "
    "through bhs-kjv.json where it is the Hebrew's; the OT references in the text are resolved in the "
    "numbering measured for them (measure.numbering_references); where either measure is undecided, the "
    "commentary's own numbering of that book decides, pooled over every Keil & Delitzsch volume holding it "
    "(measure.numbering_work); where that too is undecided, a verse both numberings have is resolved only "
    "where the two read it alike, else it stays unresolved with both candidates; footnotes in `notes` of the "
    "unit open at the foot of the page; prefaces, introductions, appendices and indexes by scan leaf "
    "(leaf.N); the Hebrew words are lost: the OCR read the pointed Hebrew as Latin-letter debris, which stays "
    "in the text as printed by the OCR, unremoved; unproofread OCR")

SCAN_READERS["kdh"] = build_scan_kdh
READER_TEXTS["kdh"] = {"honesty": KDH_HONESTY, "citation": citation_kdh}
KD_VOTES = {"kdh": build_scan_kdh}

# KD4D volumes: Delitzsch's Job (2 vols, tr. Bolton 1866), Proverbs (2 vols, tr. Easton 1874-75) and Isaiah
# (2 vols, the fourth edition's translation, 1890). Every candidate scan was MEASURED with the kdh reader:
# KJV verses keyed of the verses in the chapters reached, running heads decoded, heads dropped out of order.
# Refused: anything printed after 1928 (the Eerdmans reprints, 1949-1986, and the Hendrickson 1996 set);
# biblicalcommenta02deliuoft (Proverbs II) for its imprint (undated, the Simpkin Marshall Hamilton Kent
# issue, 1889 or later); biblicalco2ndjob01deliuoft (its hOCR refused, HTTP 500, twice). Lane A
# (claude/armarium-divines, pipeline/*_shelf.json) holds no Delitzsch item, so no same_scan_as.
_DEL = "Franz Delitzsch"
KD4D = {
    "delitzsch-job-1": _kd(
        "Biblical Commentary on the Book of Job, vol. I", "Delitzsch, Job I", _DEL,
        "biblicalcommejob01deliuoft", "a685a4a5d717e9556f68b3c6acb150f3255e4bfcfcccfa0644a36d563ddc4fde",
        f"{_KD}: Franz Delitzsch, Biblical Commentary on the Book of Job, vol. I (chap. i.-xxii.), tr. Francis "
        "Bolton (1866), as its title page reads", 1866, "University of Toronto (Robarts)", "NOT_IN_COPYRIGHT",
        (6, 465), [("Job", 56, 465)]),
    "delitzsch-job-2": _kd(
        "Biblical Commentary on the Book of Job, vol. II", "Delitzsch, Job II", _DEL,
        "biblicalcommejob02deliuoft", "9ebd46aac655acb312add994f35b5eaa1bf7c111419b2c1f919235b918072cf9",
        f"{_KD}: Franz Delitzsch, Biblical Commentary on the Book of Job, vol. II (chap. xxiii.-xlii., with "
        "Wetzstein's appendix), tr. Francis Bolton (1866), as its title page reads", 1866,
        "University of Toronto (Robarts)", "NOT_IN_COPYRIGHT", (10, 470), [("Job", 20, 413)]),
    "delitzsch-proverbs-1": _kd(
        "Biblical Commentary on the Proverbs of Solomon, vol. I", "Delitzsch, Prov. I", _DEL,
        "biblicalcommentary01deli", "dfe4b27b5cb2736a62e46232d1d74cfa4513a6a57c577a798cd2937b09bceb6d",
        f"{_KD}: Franz Delitzsch, Biblical Commentary on the Proverbs of Solomon, vol. I (chap. i.-xvii.), tr. "
        "M. G. Easton (1874), as its title page reads", 1874, "Princeton Theological Seminary Library",
        "NOT_IN_COPYRIGHT", (9, 390), [("Prov", 70, 390)]),
    "delitzsch-proverbs-2": _kd(
        "Biblical Commentary on the Proverbs of Solomon, vol. II", "Delitzsch, Prov. II", _DEL,
        "biblicalcommentary02deli", "22327865dac4aa5538d277f926758bbb46e4ed54fa35af8f50079e322f7aab05",
        f"{_KD}: Franz Delitzsch, Biblical Commentary on the Proverbs of Solomon, vol. II (chap. xviii.-xxxi.), "
        "tr. M. G. Easton (1875), as its title page reads", 1875, "Princeton Theological Seminary Library",
        "NOT_IN_COPYRIGHT", (11, 365), [("Prov", 19, 360)]),
    "delitzsch-isaiah-1": _kd(
        "Biblical Commentary on the Prophecies of Isaiah, vol. I", "Delitzsch, Isa. I", _DEL,
        "biblicalcommenta1deliuoft", "f05085fa5e015134f3b67c6bca38f35b539d0b4debfbad6b8eba09f4c7ccbb6a",
        f"{_KD}, New Series: Franz Delitzsch, Biblical Commentary on the Prophecies of Isaiah, vol. I (chap. "
        "i.-xxvii.), translated from the fourth edition, with an introduction by S. R. Driver (1890), as its "
        "title page reads (it names no translator)", 1890, "University of Toronto (Robarts)", "NOT_IN_COPYRIGHT",
        (5, 478), [("Isa", 69, 478)]),
    "delitzsch-isaiah-2": _kd(
        "Biblical Commentary on the Prophecies of Isaiah, vol. II", "Delitzsch, Isa. II", _DEL,
        "biblicalcoisaiah02deliuoft", "349c3a341f55971b7307b9f8dd95d91d0dc39e95925547968a97f36e988a0858",
        f"{_KD}, New Series: Franz Delitzsch, Biblical Commentary on the Prophecies of Isaiah, vol. II (chap. "
        "xxviii.-lxvi.), translated from the fourth edition (1890), as its title page reads (it names no "
        "translator)", 1890, "University of Toronto (Robarts)", "NOT_IN_COPYRIGHT", (9, 501), [("Isa", 13, 501)]),
}
KD4D_CHOICE = {
    "delitzsch-job-1": "biblicalcommejob01deliuoft (Toronto, 1866): 537 of 550 KJV verses keyed, 201 running heads "
                       "decoded, 0 out of order; biblicalcommenta00deli 535/550 (3 out of order), "
                       "bookofjob00deliuoft 531/550 (1)",
    "delitzsch-job-2": "biblicalcommejob02deliuoft (Toronto, 1866): 503 of 520 KJV verses keyed, 185 heads, 3 out of "
                       "order; biblicalcommenta02deli 505/520 (4 out of order), biblicalcommenta01deli (vol. II, "
                       "though IA catalogues it vol. 1) 502/520 (4), thebookofjob02deliuoft 502/520 (8), "
                       "biblicalco2ndjob02deliuoft 494/520; fewest heads dropped among the near-equal",
    "delitzsch-proverbs-1": "biblicalcommentary01deli (Princeton, 1874): 462 of 501 KJV verses keyed, 154 heads, 2 "
                            "out of order; biblicalcommenta01deliuoft (IA: 1880) 461/501 (4)",
    "delitzsch-proverbs-2": "biblicalcommentary02deli (Princeton, 1875): 378 of 414 KJV verses keyed, 155 heads, 5 out "
                            "of order; biblicalcommenta02deliuoft 383/414 refused: IA dates it 1880, but its title page "
                            "prints no date and its imprint (Simpkin, Marshall, Hamilton, Kent) is of 1889 or later, "
                            "so the issue cannot be dated",
    "delitzsch-isaiah-1": "biblicalcommenta1deliuoft (Toronto, 1890, 4th ed.): 479 of 510 KJV verses keyed, 189 heads, "
                          "3 out of order; biblicalcommenta1894deli (1894) 478/510 (4), isaiahsprophecie01deliuoft (1884, 3rd ed.) 463/510 "
                          "(7), biblicalcomment03deligoog 464/510 (27), biblicalcommenta00delirich 22 out of order",
    "delitzsch-isaiah-2": "biblicalcoisaiah02deliuoft (Toronto, 1890, 4th ed.): 757 of 782 KJV verses keyed, 220 heads, "
                          "5 out of order; isaiahsprophecie02deliuoft (1884, 3rd ed.) 735/782 (6), biblicalcomment04deligoog (1877) 432/782 "
                          "(49)",
}
KD4D_IA_DATES = {
    "biblicalcommejob01deliuoft": ("1866", None),
    "biblicalcommejob02deliuoft": ("1866", None),
    "biblicalcommentary01deli": ("1874", None),
    "biblicalcommentary02deli": ("1874", "IA dates the set; this volume's title page reads 1875"),
    "biblicalcommenta1deliuoft": ("1890", None),
    "biblicalcoisaiah02deliuoft": ("1890", None),
}
# a volume continuing a book starts its notes where the volume before left off
KD4D_FIRST_CHAPTER = {"delitzsch-job-2": {"Job": 23}, "delitzsch-proverbs-2": {"Prov": 18},
                      "delitzsch-isaiah-2": {"Isa": 28}}
for _k, _s in KD4D.items():
    _s["reader"] = "kdh"
    _s["scan_choice"] = KD4D_CHOICE[_k]
    if _k in KD4D_FIRST_CHAPTER:
        _s["first_chapter"] = KD4D_FIRST_CHAPTER[_k]
    _s["ia_date"], _why = KD4D_IA_DATES[_s["ia"]]
    if _why:
        _s["ia_date_note"] = _why
SECOND.update(KD4D)
SCANS.update(KD4D)
ORDER.extend(KD4D)


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
    "a range keeps its end in `through` (one crossing chapters, 'viii. 28-ix. 3' or '8. 28-9. 3', included; "
    "a range is applied only to a reference under its own book) and a range the KJV cannot end keeps its "
    "start only, marked through_unread (scripture_links.ranges_start_only); 'Gal. c. iv. 3' and 'Gal. C. iv. 3' are Gal 4:3, "
    "a comma list of verses stays in its chapter ('viii. 1, 2, 13' is 8:1, 8:2 and 8:13), "
    "and a range closing a list into the next chapter ('iii. 6, 7-iv. 2') keeps its end; "
    "'ver. 20' and a bare 'c. iii. 13' are read as the commentary's own epistle in note units only, and never "
    "after another work's abbreviation ('Euseb. H.E. c. iv. 3'), a Latin title word ('Tertullian de Baptismo "
    "c. iv. 3') or a capitalised name, at a sentence's opening too ('Irenaeus c. iv. 3'), unless it is an "
    "English word or one of the OCR misreadings of one found in these scans ('Oompare', 'Oomp.', 'Boo')")


RANGES_HONESTY_2B = (
    "; in the scripture references a range keeps its end in `through` (one crossing chapters included; a "
    "range is applied only to a reference under its own book), and a range the KJV cannot end keeps its start "
    "only, marked through_unread (scripture_links.ranges_start_only)")


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
                "misread (measure.hebrew), each line's words kept in the order the hOCR gives them, never "
                "reordered: of adjacent Hebrew words in a line, measure.hebrew.word_order counts the pairs the "
                "OCR gave right to left on the page (Hebrew's reading order: nearly all) and left to right "
                "(word-reversed: where two OCR rows were joined, words sorted left to right, or the OCR erred); "
                "unproofread OCR")
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
            rights = {"license": f"public domain in the US (printed {s.get('printed_label', s['printed'])}); the "
                                 "scans and their OCR are "
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
        measure["hebrew"] = dict(hebrew_measure(u["text"] for u in units), word_order=hebrew_word_order(slug))
    book = {"slug": slug, "title": meta["title"], "author": meta["author"], "edition": meta["edition"],
            "source": source,
            "scheme": {"citation": citation(slug, ocr), "resolution": "verse-note" if eps else "page",
                       "honesty": honesty(slug, ocr), "status": "draft"},
            "rights": rights, "measure": measure, "units": units}
    if slug in SAME_SCAN_AS:
        book["scheme"]["same_scan_as"] = SAME_SCAN_AS[slug]
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
