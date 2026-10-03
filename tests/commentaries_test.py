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
check("decoder: one unconfirmed head does not", d.offer(5, None, 3, [], None, False) != (3, 5, None))
check("decoder: a run's end beyond the chapter is dropped", B.Decoder(counts)._take(1, 20, 30) == (1, 20, None))

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
check("pins: every edition printed before 1929", all(s["printed"] < 1929 for s in list(B.SCANS.values()) + list(B.GUTENBERG.values())))

# -- the manifest's measures
with open(os.path.join(ROOT, "data", "books", "manifest.json"), encoding="utf-8") as f:
    man = json.load(f)
ents = {k: man[k] for k in B.ORDER if k in man}
check("manifest: one entry per book", len(ents) == len(B.ORDER) >= 6)
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
      all(ents[k]["measure"]["greek"]["greek_share_of_letters"] > 0.05 for k in B.ORDER if k not in LOW_GREEK))
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
        continue
    with open(p, "rb") as f:
        blob = f.read()
    check(f"built: {k} = its manifest entry", hashlib.sha256(blob).hexdigest() == ents[k]["built_sha256"])
    units = json.loads(blob)["units"]
    check(f"built: {k} ids unique", len({u["id"] for u in units}) == len(units))
    check(f"built: {k} comments-on links name KJV verses that exist",
          all(lk["resolved"] for u in units for lk in u["links"] if lk.get("type") == "comments-on"))

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
