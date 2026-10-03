#!/usr/bin/env python3
"""commentaries_test.py -- pipeline/build_commentaries.py: Lightfoot on
Galatians, Philippians, Colossians and Philemon; Westcott on Hebrews and the
Epistles of St John; Hort's Six Lectures. The rules on small inline fixtures
(no corpus needed), then the measures the committed manifest records, then,
when the built books are present, the books against their manifest entries."""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import build_commentaries as B  # noqa: E402

passed = failed = 0


def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}")


def line(text, x0, y0, x1, h, xs=None):
    """An hOCR line as charles_ocr reads it: words are (x0, y0, x1, y1, conf, text)."""
    toks = text.split()
    step = (x1 - x0) / max(len(toks), 1)
    words = [(x0 + i * step, y0, x0 + (i + 1) * step, y0 + h, 95, t) for i, t in enumerate(toks)]
    return {"text": text, "bbox": [x0, y0, x1, y0 + h], "xs": xs or h, "words": words}


# -- a verse number opening a note
check("opener: a verse number", B.opener("12. The word is used") == (None, 12, None, "read"))
check("opener: a chapter printed with it, and a run", B.opener("II. 1, 2. The apostle") == (2, 1, 2, "read"))
check("opener: a run's last number is its end", B.opener("2, 3, 4. These verses")[1:3] == (2, 4))
check("opener: OCR letters for digits undone, and said so", B.opener("to. The next") == (None, 10, None, "read-fix"))
check("opener: a year is not a verse", B.opener("1873. In that year") is None)
check("opener: prose is not a verse", B.opener("the word") is None)
check("opener: a run running backwards keeps only its start", B.opener("5, 3. text")[1:3] == (5, None))

# -- running heads
check("split_head: reference at the right", B.split_head("EPISTLE TO THE GALATIANS. [I. 2, 3")
      == ("I. 2, 3", "EPISTLE TO THE GALATIANS. "))
check("split_head: reference at the left", B.split_head("II. 4] EPISTLE TO THE HEBREWS.")[0] == "II. 4")
check("split_head: a head with no reference", B.split_head("INTRODUCTION.") == (None, "INTRODUCTION."))
check("head_chapter: 'IL. 4' is II", B.head_chapter("IL. 4", 6) == 2)
check("head_chapter: Greek-lookalike 'ΠῚ. 8' is III", B.head_chapter("ΠῚ. 8", 6) == 3)
check("head_chapter: '1. 6' is I", B.head_chapter("1. 6", 6) == 1)
check("head_chapter: a chapter the book lacks is unread", B.head_chapter("VII. 3", 6) is None)
check("head_chapter: no reference, no chapter", B.head_chapter(None, 6) is None)
check("head_verses", B.head_verses("III. 12-14") == [12, 14])

# -- junk lines: the large type's accents read as their own lines
check("is_junk: accents and marks only", B.is_junk(line("‘ “ - ’", 100, 100, 200, 20), 20))
check("is_junk: small type", B.is_junk(line("a b", 100, 100, 200, 10), 20))
check("is_junk: a line of words is kept", not B.is_junk(line("the word which was spoken before", 100, 100, 600, 20), 20))

# -- layout: large-type text above, notes in two columns, indented openers
above = [line("ΠΑΥΛΟΣ ἀπόστολος οὐκ ἀπ᾽ ἀνθρώπων", 100, 100, 900, 40, 30)]
cols = []
for i in range(6):
    y = 300 + i * 30
    lx = 120 if i in (0, 3) else 100
    cols.append(line(("1. " if i == 0 else "2. " if i == 3 else "") + "note words run on in the left col", lx, y, 480, 20, 15))
    cols.append(line("note words run on in the right column here", 520, y, 900, 20, 15))
a = {"body": above + cols}
lay = B.layout(a, 1000, False)
check("layout: two note columns found", lay is not None and len(lay["left"]) == 6 and len(lay["right"]) == 6)
check("layout: the larger type above is the epistle's text", lay and [l["text"] for l in lay["text"]] == [above[0]["text"]])
ind = [ok for l, ok in B.stream(lay)] if lay else []
check("stream: indented lines may open a note, flush ones may not", ind[:6] == [True, False, False, True, False, False])
prose = [line("and the word of the law that was in the beginning", 100, 100 + i * 25, 900, 20, 15) for i in range(3)]
check("layout: body-type prose above two columns is an essay with footnotes, not notes",
      B.layout({"body": prose + cols}, 1000, False) is None)
check("layout: one column is not a commentary page", B.layout({"body": [c for c in cols if c["bbox"][0] < 500]}, 1000, False) is None)

# -- the verse sequence
counts = {1: 24, 2: 21, 3: 29}
d = B.Decoder(counts)
check("decoder: the first verse", d.offer(1, None, 1, []) == (1, 1, None))
check("decoder: forward in the chapter", d.offer(3, None, 1, [1, 5]) == (1, 3, None))
check("decoder: a note on a verse just passed is taken", d.offer(2, None, 1, []) == (1, 2, None))
check("decoder: ... and the sequence stays where it was", (d.c, d.v) == (1, 3))
check("decoder: past the chapter's KJV verse count is refused", d.offer(40, None, 1, []) is None)
d.c, d.v = 1, 5
check("decoder: no turn mid-chapter without the head", d.offer(1, None, None, []) is None)
d.c, d.v = 1, 23
check("decoder: a list item '2.' with a '1.' close behind is not the turn",
      d.offer(2, None, 2, [], ahead=[(None, 1)]) is None)
check("decoder: the chapter turns where the head says", d.offer(1, None, 2, []) == (2, 1, None))
d.c, d.v = 2, 5
check("decoder: a chapter printed with the number", d.offer(1, None, None, [], 3) == (3, 1, None))
d.c, d.v = 1, 3
check("decoder: two agreeing running heads resync the chapter", d.offer(5, None, 3, [], None, True) == (3, 5, None))
d.c, d.v = 1, 3
check("decoder: one unconfirmed head does not: the note stays in its chapter",
      d.offer(5, None, 3, [], None, False) == (1, 5, None) and (d.c, d.v) == (1, 5))
d = B.Decoder(counts)
check("decoder: a run's end beyond the chapter is dropped, and counted",
      d._take(1, 20, 30) == (1, 20, None) and d.runs_cut == 1)
check("decoder: a run over 15 verses keeps its start, and is counted",
      d._take(2, 1, 20) == (2, 1, None) and d.runs_cut == 2)
check("decoder: a run within the chapter is kept, not counted", d._take(3, 1, 5) == (3, 1, 5) and d.runs_cut == 2)
check("opener: a run running backwards says so (openers_run_cut)",
      B.opener("5, 3. text").run_cut and not B.opener("2, 3, 4. These verses").run_cut)
check("CROSS_OPEN: a run into the next chapter ('28—V. 1.') is recognised, a plain opener is not",
      B.CROSS_OPEN.match("28—V. 1. ‘So then") and not B.CROSS_OPEN.match("28. So then"))

# -- scripture
ids = B.kjv_ids()
check("kjv ids: read from the committed registry", "kjv:Gal.2.20" in ids and len(ids) > 30000)
r = B.scripture("compare ver. 20 above", ids, own="Gal", chapter=2)
check("scripture: 'ver. 20' is the note's own chapter", any(x.get("target") == "kjv:Gal.2.20" and x["rule"] == "self/ver" for x in r))
r = B.scripture("as in c. iii. 13", ids, own="Gal", chapter=2)
check("scripture: 'c. iii. 13' is the epistle's own", any(x.get("target") == "kjv:Gal.3.13" and x["rule"] == "self/c" for x in r))
r = B.scripture("see Rom. viii. 28", ids)
check("scripture: another book, KJV numbering", any(x.get("target") == "kjv:Rom.8.28" for x in r))
r = B.scripture("see Rom. viii. 99", ids)
check("scripture: a verse the KJV lacks stays unresolved, with why", r and not r[0]["resolved"] and r[0].get("why"))
check("scripture: without its own book, 'ver. 20' is not read", not B.scripture("ver. 20", ids))
r = B.scripture("Euseb. H.E. c. iv. 3", ids, own="Gal", chapter=2)
check("scripture: 'Euseb. H.E. c. iv. 3' is Eusebius's chapter, not Gal 4.3", not r)
check("scripture: 'ib. c. iii. 13' (another work) is refused, 'cf. c. iii. 13' is read",
      not B.scripture("ib. c. iii. 13", ids, own="Gal", chapter=2)
      and [x.get("target") for x in B.scripture("cf. c. iii. 13", ids, own="Gal", chapter=2)] == ["kjv:Gal.3.13"])
units = [{"id": "x:leaf.9", "kind": "page", "text": "Euseb. H.E. c. iv. 3; and ver. 20", "links": []},
         {"id": "x:2.20", "kind": "note", "book": "Gal", "text": "as in c. iii. 13", "links": []}]
B.SCANS["_t"] = {"ia": "t", "epistles": [("Gal", 1, 2)]}
B.harvest("_t", units, ids)
del B.SCANS["_t"]
check("harvest: an introduction page reads no 'c.'/'ver.' as the epistle's own", units[0]["links"] == [])
check("harvest: a note unit does", [x.get("target") for x in units[1]["links"]] == ["kjv:Gal.3.13"])
r = B.scripture("see vv. 8-12", ids, own="Gal", chapter=2)
check("scripture: 'vv. 8-12' is one link, a range with `through`",
      [(x["target"], x.get("through"), x["ref"]) for x in r] == [("kjv:Gal.2.8", "kjv:Gal.2.12", "Gal 2:8-12")])
r = B.scripture("see ver. 3, 4", ids, own="Gal", chapter=2)
check("scripture: 'ver. 3, 4' is two verses", [x["target"] for x in r] == ["kjv:Gal.2.3", "kjv:Gal.2.4"])
r = B.scripture("See Rom. viii. 28-ix. 3", ids)
check("scripture: a range crossing chapters keeps its end",
      [(x["target"], x.get("through")) for x in r] == [("kjv:Rom.8.28", "kjv:Rom.9.3")])
r = B.scripture("Rom. 8:28-9:3.", ids)
check("scripture: ... in arabic numbering too", [x.get("through") for x in r] == ["kjv:Rom.9.3"])
r = B.scripture("cf. Gal. iii. 12-8", ids)
check("scripture: a range running backwards keeps its start and says so",
      [(x["target"], "through" in x, x.get("through_unread")) for x in r] == [("kjv:Gal.3.12", False, "3:8: backwards")])
r = B.scripture("cf. Gal. iii. 8-40", ids)
check("scripture: a range past the chapter keeps its start and says so",
      [(x["target"], "through" in x, x.get("through_unread")) for x in r] == [("kjv:Gal.3.8", False, "3:40: past the chapter")])
# (review c9) a range applies only to its own book's reference
r = B.scripture("Phil. iii. 20-iv. 1; comp. Col. iii. 20", ids)
check("scripture: 'Phil. iii. 20-iv. 1' does not spill onto 'Col. iii. 20'",
      [(x["target"], x.get("through")) for x in r] == [("kjv:Phil.3.20", "kjv:Phil.4.1"), ("kjv:Col.3.20", None)])
r = B.scripture("Phil. iii. 12-8 and Col. iii. 12", ids)
check("scripture: 'Phil. iii. 12-8' is backwards, 'Col. iii. 12' is not",
      [(x["target"], x.get("through_unread")) for x in r] == [("kjv:Phil.3.12", "3:8: backwards"), ("kjv:Col.3.12", None)])
# (review c9) a work named without an abbreviation is another work
check("scripture: 'Tertullian de Baptismo c. iv. 3' is not Gal 4.3",
      not B.scripture("Tertullian de Baptismo c. iv. 3", ids, own="Gal", chapter=2))
check("scripture: 'cf. c. iv. 3' and 'comp. c. iv. 3' are still Gal 4.3",
      all([x.get("target") for x in B.scripture(t, ids, own="Gal", chapter=2)] == ["kjv:Gal.4.3"]
          for t in ("cf. c. iv. 3", "comp. c. iv. 3")))
check("scripture: a clause before 'c.' or a sentence opening it is the epistle's own ('Faith: c. ix. 15', "
      "'thoughts. Compare c. x. 12', 'this Epistle c. iii. 17'); 'Pro Cluentio, c. v. 12' is not",
      [x.get("target") for t in ("the Faith: c. iv. 15", "thoughts. Compare c. iv. 12", "this Epistle c. iii. 17")
       for x in B.scripture(t, ids, own="Gal", chapter=2)] == ["kjv:Gal.4.15", "kjv:Gal.4.12", "kjv:Gal.3.17"]
      and not B.scripture("Pro Cluentio, c. v. 12", ids, own="Gal", chapter=2))
# (review c9) '<Book>. c. <roman>. <n>' is the book's chapter, never Roman C
r = B.scripture("Chrys. on Gal. c. iv. 3", ids, own="Gal", chapter=2)
check("scripture: 'Chrys. on Gal. c. iv. 3' is Gal 4.3, not 'Gal 100'",
      [(x["ref"], x.get("target")) for x in r] == [("Gal 4:3", "kjv:Gal.4.3")])
check("scripture: 'Mic. v. 2' keeps its 'c' (not read as 'Mi' + 'c.')",
      [x.get("target") for x in B.scripture("Mic. v. 2", ids)] == ["kjv:Mic.5.2"])
# (review c9) an arabic range into the next chapter; a backward range with the chapter repeated
r = B.scripture("Rom. 8. 28-9. 3", ids)
check("scripture: 'Rom. 8. 28-9. 3' keeps its end",
      [(x["target"], x.get("through")) for x in r] == [("kjv:Rom.8.28", "kjv:Rom.9.3")])
r = B.scripture("Gal. iii. 28-iii. 3", ids)
check("scripture: 'Gal. iii. 28-iii. 3' keeps its start and says it runs backwards",
      [(x["target"], "through" in x, x.get("through_unread")) for x in r] == [("kjv:Gal.3.28", False, "3:3: backwards")])
r = B.scripture("Gal. iii. 3-iii. 5", ids)
check("scripture: 'Gal. iii. 3-iii. 5' (chapter repeated, forwards) keeps its end",
      [(x["target"], x.get("through")) for x in r] == [("kjv:Gal.3.3", "kjv:Gal.3.5")])

# -- refs, rights, folios
s = {"short": "Lightfoot, Gal."}
check("note_ref", B.note_ref(s, "Gal", 2, 20) == "Lightfoot on Gal 2.20" and B.note_ref(s, "Gal", 2, 3, 5) == "Lightfoot on Gal 2.3-5")
hdr = ("The Project Gutenberg eBook\n\nThis eBook is for the use of anyone anywhere in the United States and most "
       "other parts of the world at no cost\n\n*** START OF THE PROJECT")
check("gutenberg_rights: the rights line as read", B.gutenberg_rights(hdr).startswith("This eBook is for the use of anyone"))
try:
    B.gutenberg_rights("*** This is a COPYRIGHTED Project Gutenberg eBook ***\n" + hdr)
    check("gutenberg_rights: a COPYRIGHTED header stops the build", False)
except SystemExit:
    check("gutenberg_rights: a COPYRIGHTED header stops the build", True)
m = B.NOTE_OPEN.match("IV. 1. Masters")
check("NOTE_OPEN: a roman chapter with the verse", m and (m.group(1), m.group(2)) == ("IV", "1"))
pp = B.printed_pages({10: [1], 11: [2], 12: [], 13: [4], 14: [5], 15: [99]})
check("printed_pages: folios agreeing with their neighbours are read", pp.get(11) == (2, "read"))
check("printed_pages: a leaf with no folio takes its neighbours' offset", pp.get(12) == (3, "neighbours"))
check("printed_pages: a stray number is not a folio", pp.get(15, (None,))[0] != 99)

# -- the pins
check("pins: every scan pinned by sha256", all(re.fullmatch(r"[0-9a-f]{64}", v["sha256"]) for s in B.SCANS.values() for v in B.volumes(s)))
check("pins: the Gutenberg file pinned by sha256", all(re.fullmatch(r"[0-9a-f]{64}", g["sha256"]) for g in B.GUTENBERG.values()))
check("pins: the Horae's printed year is 1859, labelled as the sheets, the copies possibly a later issue",
      B.SCANS["lightfoot-horae"]["printed"] == 1859
      and B.SCANS["lightfoot-horae"]["printed_label"] == "1859 (the sheets; this copy possibly a later issue)")
check("pins: every edition printed before 1929", all(s["printed"] < 1929 for s in list(B.SCANS.values()) + list(B.GUTENBERG.values())))
check("pins: every scan's Internet Archive date (pinned from its metadata; fetch() stops if it changes) is "
      "before 1929 and is the edition's printed year, or a note says why not",
      all(re.match(r"\d{4}", v.get("ia_date", "")) and int(v["ia_date"][:4]) < 1929 and v["printed"] < 1929
          and (int(v["ia_date"][:4]) == v["printed"] or v.get("ia_date_note"))
          for s in B.SCANS.values() for v in B.volumes(s)))

# -- the second shelf's ranges (Keil & Delitzsch)
check("K&D: 'vv. 8-12' is one span, 'vv. 3-5, 9' a span and a verse",
      B._ver_spans(B.SELF_VER.search("vv. 8-12")) == [(8, 12)]
      and B._ver_spans(B.SELF_VER.search("vv. 3-5, 9")) == [(3, 5), (9, None)])
x = {"target": "kjv:Ps.51.3", "resolved": True}
B._kd_through(x, 51, 5, 6, {"target": "kjv:Ps.51.4", "resolved": True})
check("K&D: a range keeps its end in `through`", x.get("through") == "kjv:Ps.51.4")
x = {"target": "kjv:Ps.51.3", "resolved": True}
B._kd_through(x, 51, 5, 3, None)
check("K&D: a backward range keeps its start only and says so", x.get("through_unread") == "51:3: backwards"
      and "through" not in x)

# -- the manifest's measures
with open(os.path.join(ROOT, "data", "books", "manifest.json"), encoding="utf-8") as f:
    man = json.load(f)
ents = {k: man[k] for k in B.ORDER if k in man}
check("manifest: one entry per book", len(ents) == len(B.ORDER) >= 6 + len(B.SECOND))
check("manifest: honesty, rights and draft status on every entry",
      all(e["scheme"].get("honesty") and e.get("rights") and e["scheme"].get("status") == "draft" for e in ents.values()))
check("manifest: every OCR'd book says it is unproofread",
      all("unproofread OCR" in e["scheme"]["honesty"] for e in ents.values() if e["format"] == "ia-hocr"))
check("manifest: the OCR'd books' rights record the item's status field",
      all("ia_possible_copyright_status" in e["rights"] for e in ents.values() if e["format"] == "ia-hocr"))
cov = lambda k, b: ents[k]["measure"]["kjv_coverage"][b]  # noqa: E731
check("manifest: Colossians and Philemon, every verse commented",
      cov("lightfoot-colossians", "Col")["commented"] == 95 and cov("lightfoot-colossians", "Phlm")["commented"] == 25)
check("manifest: Galatians, 95% of verses", cov("lightfoot-galatians", "Gal")["commented"] >= 0.95 * 149)
check("manifest: Philippians, 90% of verses", cov("lightfoot-philippians", "Phil")["commented"] >= 0.9 * 104)
check("manifest: Hebrews, 90% of verses", cov("westcott-hebrews", "Heb")["commented"] >= 0.9 * 303)
check("manifest: 1 John, 95% of verses", cov("westcott-john", "1John")["commented"] >= 0.95 * 105)
LOW_GREEK = {"hort-ante-nicene", "lightfoot-horae"}     # lectures; and the Horae, whose quotations are Hebrew
check("manifest: the commentaries' Greek survived as Greek (over 5% of letters)",
      all(ents[k]["measure"]["greek"]["greek_share_of_letters"] > 0.05 for k in B.ORDER
          if k not in LOW_GREEK and B.SCANS.get(k, {}).get("reader") != "kd"))
check("manifest: most scripture references resolve",
      all(e["measure"]["scripture_links"]["resolved"] >= 0.8 * e["measure"]["scripture_links"]["read"]
          for k, e in ents.items() if k not in LOW_GREEK))
check("manifest: Hort is by page, six lectures found",
      ents["hort-ante-nicene"]["scheme"]["resolution"] == "page" and ents["hort-ante-nicene"]["measure"]["lecture_headings"] == 6)
check("manifest: every Gutenberg footnote placed",
      ents["lightfoot-colossians"]["measure"]["footnotes_placed"] == ents["lightfoot-colossians"]["measure"]["footnotes"])

# -- wave 2a: several volumes, other running heads, the Horae's 'Ver. 5:'
vs = B.volumes({"title": "T", "volumes": [{"ia": "a", "leaves": (1, 2)}, {"ia": "b", "leaves": (3, 4)}]})
check("volumes: each volume carries the book's settings and its number",
      [(v["ia"], v["title"], v["vol"]) for v in vs] == [("a", "T", 1), ("b", "T", 2)] and "volumes" not in vs[0])
check("volumes: a one-scan book is its own volume, numbered None", B.volumes({"ia": "x"}) == [{"ia": "x", "vol": None}])
hd = lambda h, ref=None: {"head": h, "ref": ref}  # noqa: E731
check("head_ref cu: Westcott's left page names the chapter",
      B.head_ref(hd("264 GOSPEL ACCORDING TO ST. JOHN [Cu. VII"), {"head": "cu"}, 21) == (7, []))
check("head_ref cu: the right page names the verses only",
      B.head_ref(hd("VER. 4—7] GOSPEL ACCORDING TO ST. JOHN 263", "VER. 4—7"), {"head": "cu"}, 21) == (None, [4, 7]))
check("head_ref plain: Ellicott's 'PHILIPPIANS II. 9.'",
      B.head_ref(hd("46 | PHILIPPIANS II. 9."), {"head": "plain"}, 4) == (2, [9]))
check("head_ref plain: a folio after a bar is not a chapter", B.head_ref(hd("Bt F. | 29"), {"head": "plain"}, 6)[0] is None)
check("head_ref ch: Lightfoot's '[Ch. xxviii. 19.'",
      B.head_ref(hd("382 Hebrew and Talmudical [Ch. xxviii. 19."), {"head": "ch"}, 28) == (28, [19]))
check("ver_opener: 'Ver. 5:'", B.ver_opener("Ver. 5: Ἐν ἐκείναις") == (None, 5, None, "read"))
check("ver_opener: a run, the footnote mark after it ignored", B.ver_opener("Ver. 9,10*: text")[1:3] == (9, 10))
check("ver_opener: 'g' for 9, and said so", B.ver_opener("Ver. g: text") == (None, 9, None, "read-fix"))
check("ver_opener: prose is not a verse", B.ver_opener("Very many of them") is None)
check("chap_heading: 'CHAP. XI.' is 11", B.chap_heading("CHAP. XI.", 28) == 11)
check("chap_heading: an unread number is -1", B.chap_heading("CHAP. ונרא", 28) == -1)
check("chap_heading: a line of prose is no heading", B.chap_heading("CHAP. I. of the book, which he wrote", 28) is None)
vd = B.VerDecoder({1: 25, 2: 23, 3: 17, 5: 48})
check("VerDecoder: the first note takes the agreeing head ahead", vd.offer(1, None, None, 1, None) == (1, 1, None))
check("VerDecoder: a heading moves the chapter on, skipping chapters", vd.offer(3, None, None, None, 5) == (5, 3, None))
check("VerDecoder: an earlier head does not move it back", vd.offer(9, None, 2, None, None) == (5, 9, None))
check("VerDecoder: a verse past the chapter's count is refused", vd.offer(60, None, None, None, None) is None)
check("chapter_word: Ellicott's 'CHAPTER II. 1.' opens 2.1",
      B.opener(B.chapter_word("CHapTeR II. 1. διά] after")) == (2, 1, None, "read"))
check("chapter_word: the old-style 1 read as 'τ' after it is 1",
      B.opener(B.chapter_word("Cuapter II. τ. Αὐτοὶ γὰρ")) == (2, 1, None, "read"))
dl = B.Decoder({1: 10, 6: 18}, lookahead=True)
dl.c, dl.v = 6, 3
check("decoder lookahead: a number with two of the next four openers before it is a misreading",
      dl.offer(11, None, None, [12], ahead=[(None, 5), (None, 6), (None, 7)]) is None)
d0 = B.Decoder({1: 10, 6: 18})
d0.c, d0.v = 6, 3
check("decoder lookahead: ... the six original books keep the old rule (byte-identical rebuilds)",
      d0.offer(11, None, None, [12], ahead=[(None, 5), (None, 6), (None, 7)]) == (6, 11, None))
dl = B.Decoder({1: 25, 2: 25}, lookahead=True)
dl.c, dl.v = 1, 22
check("decoder lookahead: a list '1.' is not the turn while this chapter's later verses are ahead",
      dl.offer(1, None, None, [], ahead=[(None, 2), (None, 3), (None, 23)]) is None)
# (review c9) a note taken up again in another volume: (volume, leaf) pairs
nu = {"vol": 1, "leaves": [], "pages": [], "vleaves": [], "vpages": []}
B.note_leaf(nu, 1, 400, (790, "read"))
B.note_leaf(nu, 2, 15, (3, "read"))
B.note_leaf(nu, 2, 400, (788, "read"))       # the same leaf number in vol. 2: not the vol. 1 leaf
B.note_leaf(nu, 1, 400, (790, "read"))
sc = B.note_scan(nu)
check("westcott multi-volume: a unit running into vol. 2 keeps vol. 1's leaves and lists every (volume, leaf)",
      sc["volume"] == 1 and sc["leaves"] == [400] and sc["printed_pages"] == [790]
      and sc["volume_leaves"] == [[1, 400], [2, 15], [2, 400]]
      and sc["volume_printed_pages"] == [[1, 790], [2, 3], [2, 788]])
nu = {"vol": 2, "leaves": [], "pages": [], "vleaves": [], "vpages": []}
B.note_leaf(nu, 2, 15, None)
check("westcott multi-volume: a unit in one volume carries no volume_leaves",
      B.note_scan(nu) == {"leaves": [15], "volume": 2})
# (review c9) the Hebrew word order: the hOCR's, measured, never reordered
heb = [{"words": [(300, 0, 340, 10, 90, "בראשית"), (250, 0, 290, 10, 90, "ברא"), (200, 0, 240, 10, 90, "אלהים"),
                  (100, 0, 140, 10, 90, "God")]},
       {"words": [(100, 0, 140, 10, 90, "ברא"), (150, 0, 190, 10, 90, "אלהים")]}]
check("hebrew_pairs: right-to-left word boxes (reading order) and left-to-right ones counted apart",
      B.hebrew_pairs(heb) == {"pairs_right_to_left": 2, "pairs_left_to_right": 1})
hm = B.hebrew_measure(["the word בראשית and ובראשית here"])
check("hebrew_measure: letters counted, a prefixed lemma found",
      hm["hebrew_letters"] == 13 and hm["hebrew_tokens_3plus"] == 2 and hm["hebrew_tokens_strongs_lemma_or_prefixed"] >= 0.5)
if "westcott-gospel-john" in ents:
    e = ents["westcott-gospel-john"]
    check("manifest: Westcott's John, 70% of verses, two volumes",
          e["measure"]["kjv_coverage"]["John"]["commented"] >= 0.7 * 879 and len(man["westcott-gospel-john"]
                                                                                   ["rights"]["attribution"].split(";")) == 2)
    check("manifest: Westcott's John, under 5% of notes against the running head",
          e["measure"]["openers_against_running_head"] <= 0.05 * e["measure"]["openers_on_headed_pages"])
    check("manifest: Westcott's John names Lane A's scans and why vol. 2 differs",
          "gospelaccordingt02west_0" in e["scheme"]["note"] and "no Greek" in e["scheme"]["note"])
if "lightfoot-horae" in ents:
    e = ents["lightfoot-horae"]
    check("manifest: the Horae, 1,000 notes from Matthew to 1 Corinthians",
          e["measure"]["units"]["note"] >= 1000 and list(e["measure"]["kjv_coverage"]) ==
          ["Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor"])
    check("manifest: the Horae's Hebrew survived (over 1% of letters, a third of words biblical lemmas)",
          e["measure"]["hebrew"]["hebrew_share_of_letters"] > 0.01
          and e["measure"]["hebrew"]["hebrew_tokens_strongs_lemma_or_prefixed"] > 0.33)
    check("manifest: the Horae, under 5% of notes against the running head",
          e["measure"]["openers_against_running_head"] <= 0.05 * e["measure"]["openers_on_headed_pages"])
    check("manifest: the Horae's scripture references mostly resolve (75%: it cites the Talmud's books too)",
          e["measure"]["scripture_links"]["resolved"] >= 0.75 * e["measure"]["scripture_links"]["read"])
    wo = e["measure"]["hebrew"]["word_order"]
    check("manifest: the Horae's Hebrew word order is measured (nearly all right to left) and the honesty says "
          "it is the hOCR's, not reordered",
          wo["pairs_right_to_left"] > 50 * wo["pairs_left_to_right"]
          and "never reordered" in e["scheme"]["honesty"] and "word_order" in e["scheme"]["honesty"])
    check("manifest: the Horae's printed date says the copies may be a later issue",
          "1859 (the sheets; this copy possibly a later issue)" in e["rights"]["license"]
          and "may be a later issue" in e["scheme"]["note"])
ELL = {"ellicott-galatians": ["Gal"], "ellicott-ephesians": ["Eph"], "ellicott-philippians": ["Phil", "Col", "Phlm"],
       "ellicott-thessalonians": ["1Thess", "2Thess"], "ellicott-pastorals": ["1Tim", "2Tim", "Titus"]}
for k, bks in ELL.items():
    if k in ents:
        cv = ents[k]["measure"]["kjv_coverage"]
        check(f"manifest: {k}, 75% of verses", list(cv) == bks and all(
            cv[b]["commented"] >= 0.75 * cv[b]["kjv_verses"] for b in bks))

# -- the built books, when present
for k in B.ORDER:
    p = os.path.join(ROOT, "data", "books", f"{k}.json")
    if not os.path.exists(p):
        print(f"SKIPPED built: {k} (data/books/{k}.json not built here)")
        continue
    with open(p, "rb") as f:
        blob = f.read()
    check(f"built: {k} = its manifest entry", hashlib.sha256(blob).hexdigest() == ents[k]["built_sha256"])
    units = json.loads(blob)["units"]
    check(f"built: {k} ids unique", len({u["id"] for u in units}) == len(units))
    check(f"built: {k} comments-on links name KJV verses that exist (or say why not: a psalm's title)",
          all(lk["resolved"] or lk.get("why") for u in units for lk in u["links"] if lk.get("type") == "comments-on"))

# -- the second shelf (Alford, Bengel, Keil & Delitzsch)
check("second shelf: slugs not Lane A's (alford-greek-testament-*)",
      B.SECOND and not any(k.startswith("alford-greek-testament") for k in B.SECOND))
check("second shelf: every volume pinned, printed before 1929, and in ORDER",
      all(re.fullmatch(r"[0-9a-f]{64}", v["sha256"]) and v["printed"] < 1929 and k in B.ORDER for k, v in B.SECOND.items()))
check("second shelf: Alford vol. I is not shelved (no scan keeps its Greek)", "alford-commentary-1" not in B.SECOND)
check("second shelf: a volume of several books leads its ids with the book",
      all((k in B.MULTI) == (len(v["epistles"]) > 1) for k, v in B.SECOND.items()))

# Alford's inline openers
c = B.alford_cands("9.] As we said before", "of the whole matter.")
check("alford: '9.]' after a sentence is an opener", [x[1][1] for x in c] == [9])
c = B.alford_cands("And so ver. 8.] is not", "")
check("alford: after 'ver.' a number is a reference", c == [])
c = B.alford_cands("see Rom. ix. 3.] the same", "")
check("alford: after a roman numeral a number is a reference", c == [])
c = B.alford_cands("these things). 6—10.| ANNOUNCEMENT of", "")
check("alford: a run '6—10.|' opens 6 and ends 10", [x[1][1:3] for x in c] == [(6, 10)])
c = B.alford_cands("5. ᾧ ἡ δόξα", "")
check("alford: a number before Greek opens", [x[1][1] for x in c] == [5])
check("alford_head: 'IIETPOT A. II.' (ΠΕΤΡΟΥ OCR'd) is chapter II, not the title's II",
      B.alford_head({"head": "IIETPOT A. | II."}, 5)[0] == 2 and B.alford_head({"head": "IIETPOT A."}, 5)[0] is None)

# the single-column books
check("bengel: '14. μηκέτι)' opens 14", B.sc_cand("14. μηκέτι) no longer", "bengel") == (None, 14, None, "read"))
check("bengel: 'IV. 1. ' opens chapter IV", B.sc_cand("IV. 1. Παρακαλῶ) I beseech", "bengel")[:2] == (4, 1))
check("bengel: prose is not an opener", B.sc_cand("the word", "bengel") is None)
check("kd: 'Vers. 14-19.' opens a run", B.kd_cands("Vers. 14-19. The account") == [(0, (None, 14, 19, "read"))])
check("kd: 'Vers. 9-12 contain' opens a run", [x[1][1:3] for x in B.kd_cands("Vers. 9-12 contain a description")] == [(9, 12)])
check("kd: '— Ver. 3.' inside a paragraph opens", [x[1][1] for x in B.kd_cands("rooted there. — Ver. 3. As Adam")] == [3])
check("kd: 'ver. 3' (lower case) is a reference", B.kd_cands("The heading in ver. 1 runs thus") == [])
check("kd: a capital 'Ver.' mid-sentence is not an opener", B.kd_cands("as shown in Ver. 3. here") == [])
check("sc_head: 'CHAP. X. 8-12.'", B.sc_head("CHAP. X. 8-12. 165", 50)[0] == 10)
check("sc_head: 'PSALM XXXVII. 7'", B.sc_head("PSALM XXXVII. 7", 150)[0] == 37)
W = 2000
check("psalm_title: the next psalm's title line is read",
      B.psalm_title(line("PSALM XLI.", 600, 100, 1100, 40), W, 40) == 41)
check("psalm_title: 'XLL' (a final I read as L) is XLI", B.psalm_title(line("PSALM XLL", 600, 100, 1100, 40), W, 40) == 41)
check("psalm_title: a psalm far from the last read is not a title",
      B.psalm_title(line("PSALM LX.", 600, 100, 1100, 40), W, 40) is None)
check("psalm_title: flush left is a sentence, not the title", B.psalm_title(line("PSALM XLI.", 100, 100, 600, 40), W, 40) is None)

# numbering: existence votes
v = B.numbering_votes([("Ps", 51, 21), ("Ps", 51, 20), ("Ps", 3, 9), ("Ps", 18, 51), ("Ps", 60, 14), ("Ps", 34, 23)], ids)
check("numbering_votes: verses only the Hebrew has are Hebrew votes", v["only_hebrew"] == 6 and v["only_kjv"] == 0)
check("decide: six Hebrew votes and none against is hebrew", B.decide(v) == "hebrew")
check("decide: too few votes is undecided", B.decide({"only_hebrew": 3, "only_kjv": 0}) == "undecided")
check("decide: a split is undecided", B.decide({"only_hebrew": 6, "only_kjv": 4}) == "undecided")
check("decide: KJV votes", B.decide({"only_hebrew": 2, "only_kjv": 5}) == "kjv")
x = B.ot_link("Ps", 51, 3, "hebrew", ids, "t")
check("ot_link: Hebrew Ps 51:3 is the KJV's 51:1", x["resolved"] and x["target"] == "kjv:Ps.51.1")
x = B.ot_link("Ps", 51, 1, "hebrew", ids, "t")
check("ot_link: a psalm's title is unresolved, with why", not x["resolved"] and "title" in x["why"])
x = B.ot_link("Ps", 51, 1, "kjv", ids, "t")
check("ot_link: in the KJV's numbering, Ps 51:1 is itself", x["target"] == "kjv:Ps.51.1")
x = B.ot_link("Gen", 32, 33, "undecided", ids, "t")
check("ot_link: undecided reads a verse only the Hebrew has as Hebrew", x["resolved"] and x["target"] == "kjv:Gen.32.32")

# the decoder's ways out of a missed chapter turn
d = B.HeadDecoder({1: 30, 2: 30, 3: 30, 4: 30})
d.c, d.v = 1, 20
check("HeadDecoder: a confirmed later head takes a section opening mid-chapter", d.offer(7, None, 2, [], None, True) == (2, 7, None))
d = B.HeadDecoder({1: 30, 2: 30, 3: 30, 4: 30})
d.c, d.v = 1, 20
check("HeadDecoder: 'IV. 1' with this chapter's numbers after it is a reference",
      d.offer(1, None, None, [], 4, False, [(None, 21), (None, 22)]) is None and (d.c, d.v) == (1, 20))
d = B.HeadDecoder({1: 30, 2: 30, 3: 30, 4: 30})
d.c, d.v = 1, 28
r = [d.offer(n, None, 3, []) for n in (5, 6, 8)]
check("HeadDecoder: three refusals under one later head follow the head", r[:2] == [None, None] and r[2] == (3, 8, None))

# the manifest's measures for the second shelf
for k in B.SECOND:
    e = ents.get(k)
    if not e:
        continue
    cv = e["measure"]["kjv_coverage"]
    tot = sum(c.get("kjv_verses_in_chapters", c["kjv_verses"]) for c in cv.values())
    got = sum(c["commented"] for c in cv.values())
    floor = 0.5 if k.startswith("alford") else 0.7
    check(f"manifest: {k} notes reach {floor:.0%} of its verses", got >= floor * tot)
    if B.SECOND[k]["reader"] == "kd":
        check(f"manifest: {k} records the numbering measured", set(e["scheme"]["numbering"]) == set(cv)
              and "numbering_references" in e["measure"])
        check(f"manifest: {k} says its Hebrew is lost", e["measure"]["hebrew"]["hebrew_letters"] == 0
              and "Hebrew words are lost" in e["scheme"]["honesty"])
    else:
        check(f"manifest: {k} kept its Greek", e["measure"]["greek"]["greek_share_of_letters"] > 0.05)
check("manifest: Delitzsch's Psalms are measured as numbered in the Hebrew",
      all(ents[k]["scheme"]["numbering"]["Ps"] == "hebrew" for k in ("delitzsch-psalms-1", "delitzsch-psalms-2", "delitzsch-psalms-3")
          if k in ents))
check("manifest: Lane A's same scans are named", all("same_scan_as" in ents[k]["scheme"]
                                                     for k in ("alford-commentary-2", "alford-commentary-4") if k in ents))

# -- the third shelf: Meyer (T&T Clark translation), and Godet not shelved
check("meyer: every volume pinned, printed before 1929, IA date recorded, in SECOND and ORDER",
      B.MEYER and all(re.fullmatch(r"[0-9a-f]{64}", v["sha256"]) and v["printed"] < 1929 and v.get("ia_date")
                      and k in B.SECOND and k in B.ORDER and v["reader"] == "meyer" for k, v in B.MEYER.items()))
check("meyer: the Gospels, Acts, Romans and Corinthians are shelved",
      {b for v in B.MEYER.values() for b, _, _ in v["epistles"]} >= {"Matt", "Mark", "Luke", "John", "Acts", "Rom",
                                                                    "1Cor", "2Cor"})
check("meyer: Corinthians vol. II holds 1 Cor 14-16 and 2 Cor, so its ids name the book",
      "meyer-corinthians-2" in B.MULTI and B.MEYER["meyer-corinthians-2"]["first_chapter"] == {"1Cor": 14})
check("meyer: an IA date that is not the title page's year says why",
      all(v.get("ia_date_note") for v in B.MEYER.values() if not v["ia_date"].startswith(str(v["printed"]))))
check("meyer: no Godet volume is shelved (no scan keeps its Greek)", not any("godet" in k for k in B.ORDER))
check("meyer: the Funk & Wagnalls issues name their American editor",
      all(v.get("american") for v in B.MEYER.values() if "Funk" in v["edition"]))
check("meyer_open: 'Ver. 1. Βίβλος]'", B.meyer_open("Ver. 1. Βίβλος γενέσεως] Book of origin") == (None, 1, None, "read"))
check("meyer_open: 'Vv. 1-17.' is a run", B.meyer_open("Vv. 1-17. In the writing")[1:3] == (1, 17))
check("meyer_open: 'VER. 8.' (small capitals)", B.meyer_open("VER. 8. ἀκριβ. ἐξετάσατε]")[1] == 8)
check("meyer_open: 'Ver. 1 f.'", B.meyer_open("Ver. 1 f. Ἔν ἐκείνῳ")[1] == 1)
check("meyer_open: 'Ver. 7 ἢ' (the period read as ἢ)", B.meyer_open("Ver. 7 ἢ Ἀδ.] Inconsistently")[1] == 7)
check("meyer_open: the American editor's '[See Note LVII. p. 476.]' before 'Vv. 1, 2.'",
      B.meyer_open("[See Note LVII. p. 476.] Vv. 1, 2. The parting")[1:3] == (1, 2))
check("meyer_open: 'ver. 5' (lower case) and prose are not openers",
      B.meyer_open("ver. 5 shows") is None and B.meyer_open("Very well") is None)
check("meyer_inline: '— Ver. 14.' after a dash opens", [c[1][1] for c in B.meyer_inline("p. 335).— Ver. 14.", "")] == [14])
check("meyer_inline: a line opening 'Ver.' after a line ending in a dash opens",
      B.meyer_inline("Ver. 14. παράγων] in passing", "of Mark. —") == [(0, (None, 14, None, "read"))])
check("meyer_inline: 'ver. 14' inside a sentence is a reference", B.meyer_inline("as in ver. 14. and so", "") == [])
check("meyer_critical: a reading's paragraph (Tisch., uncials) scores two",
      B.meyer_critical("Ver. 1. Instead of ἤλθεν, we must read with Tisch., following", "BCLAY, ἔρχεται.") >= 2)
check("meyer_critical: exegesis citing the LXX scores under two",
      B.meyer_critical("Ver. 1. Βίβλος γενέσεως] Book of origin ; Gen.", "ii. 4, v. 1, LXX.; comp. Gen. vi. 9") < 2)
check("meyer_heading: 'CHAPTER XVIL' set in from the margin is read (L for I)",
      17 in B.meyer_heading(line("CHAPTER XVIL", 620, 900, 1000, 40), None, "", 1770, 2800, 100))
check("meyer_heading: a garbled heading over a critical paragraph is a heading, its number unread",
      B.meyer_heading(line("CH APR R Vol", 613, 900, 1000, 40),
                      line("Ver. 1. Instead of ἤλθεν, we must read with Tisch., following", 110, 950, 1700, 40),
                      "BCLAY, ἔρχεται.", 1856, 2800, 110) == ())
check("meyer_heading: a running head 'CHAP. I. 18. 67' is not a heading",
      B.meyer_heading(line("CHAP. I. 18. 67", 745, 60, 1100, 32), None, "", 1770, 2800, 110) is False)
check("meyer_heading: a short line in lower case is not a heading",
      B.meyer_heading(line("and so on", 700, 900, 900, 40), None, "", 1770, 2800, 110) is False)
for k in B.MEYER:
    e = ents.get(k)
    if not e:
        continue
    ms = e["measure"]
    check(f"manifest: {k} has notes, chapter intros, and coverage", ms["units"].get("note", 0) > 100
          and ms["units"].get("intro", 0) >= 2 and ms["kjv_coverage"])
    check(f"manifest: {k} under 2% of notes against a confirmed running head",
          ms.get("openers_against_running_head", 0) <= 0.02 * ms["units"]["note"])
    check(f"manifest: {k} scripture mostly resolves (80%)",
          ms["scripture_links"]["resolved"] >= 0.8 * ms["scripture_links"]["read"])
    check(f"manifest: {k} says its Hebrew is lost", ms["hebrew"]["hebrew_letters"] == 0
          and "Hebrew words are lost" in e["scheme"]["honesty"])
    check(f"manifest: {k} carries its IA date and scan choice",
          e["scheme"].get("scan_choice") and B.MEYER[k]["ia_date"] in json.dumps(B.MEYER[k]))
    if B.MEYER[k].get("american"):
        check(f"manifest: {k} keeps the American editor's notes apart (editor-notes)",
              ms["units"].get("editor-notes", 0) > 0 and ms.get("american_blocks", 0) > 0)
check("manifest: Meyer on Mark and on Romans comment on 95% of their verses",
      all(ents[k]["measure"]["kjv_coverage"][b]["commented"] >= 0.95 * ents[k]["measure"]["kjv_coverage"][b]["kjv_verses"]
          for k, b in (("meyer-mark-luke-1", "Mark"), ("meyer-romans", "Rom")) if k in ents))


def _in_chapters(e, b):
    c = e["measure"]["kjv_coverage"][b]
    return c["commented"] / c.get("kjv_verses_in_chapters", c["kjv_verses"])


check("manifest: Meyer on Acts and Corinthians comments on 93% of the verses in the chapters each volume holds",
      all(_in_chapters(ents[k], b) >= 0.93 for k, b in (
          ("meyer-acts-1", "Acts"), ("meyer-acts-2", "Acts"), ("meyer-corinthians-1", "1Cor"),
          ("meyer-corinthians-2", "1Cor"), ("meyer-corinthians-2", "2Cor")) if k in ents))
check("manifest: Meyer's Acts II read 'XX.' over chapter XIX as XIX (the running heads print it)",
      ents.get("meyer-acts-2", {}).get("measure", {}).get("chapter_headings_skip_refused", 0) >= 1)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
