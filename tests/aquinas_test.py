#!/usr/bin/env python3
"""Offline checks for the Aquinas Latin-English key (pipeline/build_aquinas_st.py).
No corpus needed: fixtures are inline. Run: python3 tests/aquinas_test.py"""
import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import build_aquinas_st as b

FAILS = []
def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)

# --- Latin citations (Corpus Thomisticum <P TITLE>) -> key
for title, want in [
    ("I q. 2 a. 3 co.", "I.q2.a3.co"),
    ("I-II q. 90 a. 1 arg. 2", "I-II.q90.a1.arg2"),
    ("II-II q. 1 a. 1 s. c.", "II-II.q1.a1.sc"),
    ("II-II q. 1 a. 1 s. c. 2", "II-II.q1.a1.sc2"),
    ("III q. 60 a. 1 ad 3", "III.q60.a1.ad3"),
    ("I q. 1 a. 4 ad arg.", "I.q1.a4.ad-sc"),
    ("I q. 2 pr.", "I.q2.pr"),
    ("Iª q. 2 pr.", "I.q2.pr"),
    ("I q. 71 arg. 1", "I.q71.a1.arg1"),          # a question of one article
    ("I-II pr.", "I-II.pr"),
    ("Summa theologiae, pr.", "ST.pr"),
]:
    check(f"la_key({title!r}) = {want}", b.la_key(title) == want)
check("la_key refuses what it cannot read", b.la_key("I q. 2 a. 3 xyz") is None)

# --- the key prints as Thomists cite
check("ref_of co", b.ref_of("I.q2.a3.co") == "ST I q.2 a.3 co.")
check("ref_of ad", b.ref_of("I-II.q90.a1.ad2") == "ST I-II q.90 a.1 ad 2")
check("ref_of sc2", b.ref_of("II-II.q1.a1.sc2") == "ST II-II q.1 a.1 s.c. 2")

# --- order inside an article
segs = ["ad2", "co", "arg2", "sc", "", "arg1", "ad1", "ad-sc"]
check("seg order", sorted(segs, key=b.seg_sort) == ["", "arg1", "arg2", "sc", "co", "ad1", "ad2", "ad-sc"])

# --- English: one CCEL article, with a continuation paragraph and an unbolded label
THML = """<ThML><ThML.body>
<div3 title="Question. 2 - The Existence of God" id="FP_Q2">
<h3>THE EXISTENCE OF GOD</h3>
<p id="a"> Because the chief aim of sacred doctrine is to teach the knowledge of God.</p>
<div4 title="Article. 3 - Whether God exists?" id="FP_Q2_A3">
<h4 id="h">Whether God exists?</h4>
<p id="p1"><b>Objection 1:</b> It seems that God does not exist.</p>
<p id="p2"><b>Objection 2:</b> Further, it is superfluous.</p>
<p id="p3"><b>On the contrary,</b> It is said in the person of God: "I am Who am."</p>
<p id="p4"><b>I answer that,</b> The existence of God can be proved in five ways.</p>
<p id="p5"> The first and more manifest way is the argument from motion.</p>
<p id="p6"><b>Reply to Objection 1:</b> As Augustine says (<scripRef osisRef="Bible.vul:Ex.3.14">Ex. 3:14</scripRef>).</p>
<p id="p7"><b>Reply to Objection 1:</b> Since nature works for a determinate end.</p>
</div4>
</div3>
</ThML.body></ThML>"""
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(THML)
b.REPAIRS.clear()
units, titles = b.parse_en(f.name)
os.unlink(f.name)
by = {u["key"]: u for u in units}
check("question prologue keyed .pr", by.get("I.q2.pr", {}).get("text", "").startswith("Because the chief aim"))
check("article title row", by.get("I.q2.a3", {}).get("text") == "Whether God exists?")
check("labels stripped", by.get("I.q2.a3.arg1", {}).get("text") == "It seems that God does not exist.")
check("continuation paragraph stays with the body",
      by.get("I.q2.a3.co", {}).get("text", "").endswith("argument from motion."))
check("a repeated reply label is renumbered by position", "I.q2.a3.ad2" in by
      and by["I.q2.a3.ad2"]["text"].startswith("Since nature"))
check("...and the repair is recorded", any(r["key"] == "I.q2.a3" for r in b.REPAIRS))
check("scripture link kept as the source tagged it, unresolved",
      by["I.q2.a3.ad1"]["links"] == [{"osis": "Ex.3.14", "versification": "vul", "resolved": False}])

# --- the key: same parts both sides -> both; a missing reply -> parts-differ, never forced
en = [{"key": k} for k in ["I.q2.a3", "I.q2.a3.arg1", "I.q2.a3.co", "I.q2.a4", "I.q2.a4.co"]]
la = [{"key": k} for k in ["I.q2.a3.arg1", "I.q2.a3.co", "I.q2.a4.co", "I.q2.a4.ad1", "I.q2.a5.co"]]
rows = {r["key"]: r for r in b.build_key(en, la, {"I.q2.a3": "t"})}
check("key: both", rows["I.q2.a3"]["status"] == "both")
check("key: parts-differ", rows["I.q2.a4"]["status"] == "parts-differ")
check("key: la-only", rows["I.q2.a5"]["status"] == "la-only")

# --- the 1894 OCR witness: headings, formulas, a lost QUAESTIO heading, a running head
import aquinas_st_1894 as o
OCR = """QUAESTIO  I.

DE  SACRA  DOCTRINA.

1.  Utrum  sit  necessarium.

ARTICULUS  I.

UTRUM  SIT  NECESSARIUM.

(22.  q.  2.  art.  3.
Et  ver.  q.  14.  art.  11.).

Ad  primum  sic  proceditur.  Videtur,  quod  non  sit  neces¬
sarium.

2.  Praeterea.  Doctrina  non  potest  esse  nisi  de  ente.

Sed  contra  est,  quod  dicitur.

28  QUAESTIO  I.  ARTICULUS  I.

Respondeo  dicendum,  quod  necessarium  fuit.

Ad  primum  ergo  dicendum,  quod  licet.

Ad  secundum  dicendum,  quod  diversa.

ARTICULUS  II.

UTRUM  SACRA  DOCTRINA  SIT  SCIENTIA.

Ad  secundum  sic  proceditur.  Videtur,  quod  non.

Respondeo  dicendum,  sacram  doctrinam  esse  scientiam.

Et  per  hoc  patet  responsio  ad  objecta.

ARTICULUS  I.

UTRUM  DEUS  SIT.

Ad  primum  sic  proceditur.  Videtur,  quod  Deus  non  sit.

Respondeo  dicendum,  quod  Deum  esse  quinque  modis  probari  potest.
"""
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write(OCR)
ou = {u["key"]: u["text"] for u in o.parse_volume("I", f.name)}
os.unlink(f.name)
check("1894: title and cross-references stay on the title row", "Et ver. q. 14" in ou.get("I.q1.a1", ""))
check("1894: hyphenation sign rejoined", ou.get("I.q1.a1.arg1", "").endswith("non sit necessarium."))
check("1894: Praeterea is the next objection", "I.q1.a1.arg2" in ou)
check("1894: running head dropped", "QUAESTIO" not in ou.get("I.q1.a1.co", "") and "I.q1.a1.co" in ou)
check("1894: replies by their ordinal", "I.q1.a1.ad2" in ou)
check("1894: 'responsio ad objecta' is ad-sc", "I.q1.a2.ad-sc" in ou)
check("1894: article 1 after article 2 means a lost QUAESTIO heading", "I.q2.a1.co" in ou)
check("overlap of near-identical Latin is high", o.overlap("Respondeo dicendum quod Deum esse", "Respondeo dicendum, quod Deum esse") > 0.9)

# --- Contra Gentiles (pipeline/build_aquinas_scg.py)
import build_aquinas_scg as g
check("scg: OCR numerals (n for II, l for I)", g.ocr_roman("XLn") == 42 and g.ocr_roman("XXl") == 21)
check("scg: a heading followed by its title", g.chapter_heading("CHAPTER XLII", "THAT GOD IS ONE")[:2] == (42, 42)
      and g.chapter_heading("CHAPTER XLII", "THAT GOD IS ONE")[2])
check("scg: a running head with its page number is not a heading", g.chapter_heading("CHAPTER XLII 87", "the text") is None)
check("scg: a running head followed by a bare page number is not taken", not g.chapter_heading("CHAPTER CXXX", "129")[2])
check("scg: a joint heading covers two chapters", g.chapter_heading("CHAPTERS VIII AND IX", "ARGUMENTS")[:2] == (8, 9))
check("scg: a joint running head is not a heading", g.chapter_heading("CHAPTERS VIII AND IX 19", "x") is None)
check("scg: a title with a lower-cased word is still capitals", g.capitals("THAT god's power IS HIS SUBSTANCE"))
check("scg: a table of contents line is recognised", bool(g.RE_TOC.search("THAT GOD IS NOT IN ANY GENUS - - - - 60 XXVI.")))
check("scg: Latin cited as Thomists cite", g.ref_of("SCG.3.95") == "SCG III, 95")

DOM = """CONTENTS

CHAPTER I

THAT GOD IS - - - 1 II. THAT GOD IS ONE - - 3

CHAPTER I

THAT GOD IS

The first chapter's text runs on
over a line.

CHAPTER I 2

the page broke this paragraph.

CHAPTERS II AND III

OF TWO THINGS

Joint text.
"""
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write(DOM)
dd = g.parse_dominican(f.name, 1, 1)
os.unlink(f.name)
check("scg dominican: the table of contents is skipped", dd.get("SCG.1.1", {}).get("title") == "THAT GOD IS")
check("scg dominican: a paragraph broken by a page is rejoined", dd["SCG.1.1"]["paras"] ==
      ["The first chapter's text runs on over a line. the page broke this paragraph."])
check("scg dominican: CHAPTERS II AND III is one chapter covering two", dd.get("SCG.1.2", {}).get("covers") == [2, 3])
check("scg dominican: no repair reported for a clean run", "_repairs" not in dd)

RIC = """<ThML><div1 title="Book III. Providence">
<div2 title="Chapter XCV, XCVI. That the Immutability of Divine Providence does not bar the Utility of Prayer"><p>a</p></div2>
<div2 title="Chapter XCVI. That God does not hear all Prayers"><p>b</p></div2>
<div2 title="Chapter Chapter XCVIII. How Providence follows a Plan"><p>c</p></div2>
<div2 title="Chapters CXXXII, CXXXV. Arguments against Voluntary Poverty, with Replies"><p>d</p></div2>
<div2 title="Chapters XLI–XLV."><p>e</p></div2>
</div1></ThML>"""
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(RIC)
rr = g.parse_rickaby(f.name)
os.unlink(f.name)
check("rickaby: 'XCV, XCVI' is two chapters", rr["SCG.3.95"]["own_covers"] == [95, 96])
check("rickaby: his own XCVI after it is kept", rr["SCG.3.96"]["title"] == "That God does not hear all Prayers")
check("rickaby: 'Chapter Chapter' read", "SCG.3.98" in rr)
check("rickaby: a comma joins a chapter to its answer, not a range", rr["SCG.3.132"]["own_covers"] == [132, 135])

# alignment: his numbers are offset by one, and his second chapter is the second half of a joint chapter
dom = {"SCG.3.94": {"title": "OF THE CERTAINTY OF DIVINE PROVIDENCE", "paras": []},
       "SCG.3.95": {"title": "THAT THE UNCHANGEABLENESS OF DIVINE PROVIDENCE DOES NOT EXCLUDE THE USEFULNESS OF PRAYER",
                    "paras": [], "covers": [95, 96]},
       "SCG.3.97": {"title": "HOW THERE IS A REASON FOR DIVINE PROVIDENCE", "paras": []}}
ric = {"SCG.3.95": {"title": "Of the Certainty of Divine Providence", "paras": ["x"], "own": 95, "own_covers": [95]},
       "SCG.3.96": {"title": "That the Immutability of Divine Providence does not bar the Utility of Prayer", "paras": ["y"], "own": 96, "own_covers": [96]},
       "SCG.3.97": {"title": "That God does not hear all Prayers", "paras": ["z"], "own": 97, "own_covers": [97]},
       "SCG.3.98": {"title": "How the Arrangements of Divine Providence follow a Reason", "paras": ["w"], "own": 98, "own_covers": [98]}}
al, routes = g.align_rickaby(ric, dom, {})
check("rickaby aligned: offset numbering placed by title", al["SCG.3.94"]["own"] == 95)
check("rickaby aligned: two of his chapters joined in one joint Leonine chapter",
      al["SCG.3.95"]["own_covers"] == [96, 97] and al["SCG.3.95"]["paras"] == ["y", "z"])
check("rickaby aligned: and the next falls in place", al["SCG.3.97"]["own"] == 98)
al, routes = g.align_rickaby(ric, dom, {(3, 95): "SCG.3.94", (3, 97): "SCG.3.95"})
check("rickaby: the 1894 Latin's placement wins where it has his number, titles elsewhere",
      al["SCG.3.94"]["own"] == 95 and routes == {"latin": 2, "title": 2})

# the 1894 Latin: own numbering, a misread numeral, a running head, then placed by its text
OLD = """LIBER PRIMUS

CAPUT PRIMUM.

QUOD SIT OFFICIUM SAPIENTIS.

Veritatem meditabitur guttur meum, et labia mea detestabuntur impium.

CAPUT vni.

DE DEO TRINO ET UNO.

Multitudinis usus quem in rebus nominandis sequendum Philosophus cen-
set, communiter obtinuit.

LIBER I. CAP. II. 3

ut sapientes dicantur qui res ordinant.

CAPUT III.

QUOD DEUS SIT ACTUS PURUS.

Deus est actus purus absque potentia.

INDEX CAPITULORUM
"""
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
    f.write(OLD)
oc, orep = g.parse_la1894(f.name)
os.unlink(f.name)
check("1894: a misread numeral is read from the sequence", sorted(oc) == ["SCG.1.1", "SCG.1.2", "SCG.1.3"])
check("1894: hyphenation rejoined, running head dropped, a page-broken paragraph rejoined",
      oc["SCG.1.2"]["paras"] == ["Multitudinis usus quem in rebus nominandis sequendum Philosophus censet, communiter obtinuit. "
                                 "ut sapientes dicantur qui res ordinant."])
check("1894: the index ends the text", "INDEX" not in " ".join(oc["SCG.1.3"]["paras"]))
leo = {"SCG.1.1": {"paras": ["Veritatem meditabitur guttur meum labia detestabuntur impium"], "title": "", "covers": [1]},
       "SCG.1.2": {"paras": ["Deus actus purus absque potentia"], "title": "", "covers": [2]}}
o94, where = g.align_1894(oc, leo)
check("1894: placed on the Leonine by its Latin, not its number", where[(1, 3)] == "SCG.1.2" and where[(1, 1)] == "SCG.1.1")

print(f"\n{len(FAILS)} failed" if FAILS else "\nall passed")
sys.exit(1 if FAILS else 0)
