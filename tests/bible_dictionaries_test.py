#!/usr/bin/env python3
# prov: 2026-11-03 claude-opus-5-5 drafted (Easton's, Nave's, Hurlbut's atlas)
# fable_review: pending
"""Offline checks for the Bible dictionaries (2026-11-03): Easton's Bible
Dictionary and Nave's Topical Bible (CCEL ThML), and Hurlbut's Bible Atlas
(Gutenberg text + its printed indexes). Fixtures inline; no corpus needed.
When the fetched files are present, a few whole-book invariants are checked
too. Run:  python3 tests/bible_dictionaries_test.py"""
import os, sys, json, tempfile, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
PIPE = os.path.join(ROOT, "pipeline")
sys.path.insert(0, PIPE)


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(PIPE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


st = load("structure_texts")
fs = load("fetch_sources")

PASS, FAIL = 0, []


def check(label, cond):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label)


def tmp(text, suffix):
    f = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, encoding="utf-8")
    f.write(text)
    f.close()
    return f.name


# A KJV verse list in the shape of data/parallel/kjv-parallel.tsv: Gen 1 has 3
# verses, Gen 2 has 2, Exod 4 has 31, Col 1 has 2.
KJV = tmp("kjv\tuid\n" + "".join(f"{k}\twh-X\n" for k in
          ["Gen.1.1", "Gen.1.2", "Gen.1.3", "Gen.2.1", "Gen.2.2", "Col.1.1", "Col.1.2"]
          + [f"Exod.4.{v}" for v in range(1, 32)]), ".tsv")
verses, last = st.kjv_verse_index(KJV)
check("kjv index: every verse, and each chapter's last verse",
      "Gen.2.2" in verses and last[("Gen", 1)] == 3 and last[("Exod", 4)] == 31)
L = lambda *a: st.kjv_link(*a, "ref", (verses, last))
check("kjv_link: a verse the KJV has links to its unit",
      L("Gen", 1, 2, 0, 0) == {"kind": "scripture", "ref": "ref", "versification": "kjv",
                               "osis": "Gen.1.2", "target": "kjv:Gen.1.2", "resolved": True})
check("kjv_link: a range keeps its end; a chapter range ends on the last verse",
      L("Exod", 4, 27, 4, 30)["end"] == "Exod.4.30" and L("Gen", 1, 2, 2, 0)["end"] == "Gen.2.2")
check("kjv_link: a whole chapter links its first verse, end its last, flagged",
      L("Gen", 1, 0, 0, 0)["target"] == "kjv:Gen.1.1" and L("Gen", 1, 0, 0, 0)["end"] == "Gen.1.3"
      and L("Gen", 1, 0, 0, 0)["chapter"] is True)
check("kjv_link: a verse or chapter the KJV lacks is kept unresolved, with why",
      L("Gen", 1, 9, 0, 0) == {"kind": "scripture", "ref": "ref", "versification": "kjv",
                               "osis": "Gen.1.9", "resolved": False, "why": "no such verse in the KJV"}
      and L("Gen", 7, 0, 0, 0)["why"] == "no such chapter in the KJV")
check("kjv_link: an Apocrypha book is not guessed into the KJV",
      L("1Macc", 1, 57, 0, 0)["resolved"] is False and "Apocrypha" in L("1Macc", 1, 57, 0, 0)["why"])

# ---------------------------------------------------------------- Easton's (ThML)
THML_HEAD = ('<?xml version="1.0" encoding="UTF-8"?>\n<ThML><ThML.head><DC>'
             '<DC.Rights>Public Domain</DC.Rights></DC></ThML.head><ThML.body>\n')
EASTON = THML_HEAD + """<div1 title="Easton's Bible Dictionary" id="EBD"><div2 title="A" id="a">
<glossary id="a-p0.1">
<term id="t1">Aaron</term>
<def id="d1">
<p id="p1">The eldest son of Amram <scripRef passage="Ex. 6:20" id="s1" parsed="|Exod|6|20|0|0" osisRef="Bible:Exod.6.20">Ex. 6:20</scripRef>; spokesman for
<a href="/ccel/easton/ebd2.m.html?term=moses" id="a1">Moses</a> <scripRef passage="Ex. 4:27-30" id="s2" parsed="|Exod|4|27|4|30" osisRef="Bible:Exod.4.27-Exod.4.30">Ex. 4:27-30</scripRef>.</p>
<p id="p2">Again <scripRef passage="Gen 1" id="s3" parsed="|Gen|1|0|0|0" osisRef="Bible:Gen.1">Gen 1</scripRef>, twice
<scripRef passage="Gen. 1:2" id="s4" parsed="|Gen|1|2|0|0" osisRef="Bible:Gen.1.2">Gen. 1:2</scripRef> and
<scripRef passage="Gen 1:2" id="s5" parsed="|Gen|1|2|0|0" osisRef="Bible:Gen.1.2">1:2</scripRef>; not the KJV:
<scripRef passage="1 Macc. 1:57" id="s6" parsed="|1Macc|1|57|0|0" osisRef="Bible:1Macc.1.57">1 Macc. 1:57</scripRef>,
<scripRef passage="Gen 1:24" id="s7" parsed="|Gen|1|24|0|0" osisRef="Bible:Gen.1.24">Gen 1:24</scripRef>; see
<a href="/ccel/easton/ebd2.z.html?term=zion" id="a2">Zion</a> and <a href="/ccel/easton/ebd2.c.html?term=courts" id="a3">Courts</a>.</p>
</def>
<term id="t2">Court</term>
<def id="d2"><p id="p3">An enclosure &amp; a yard.</p></def>
<term id="t3">Moses</term>
<def id="d3"><p id="p4">Drawn out.</p></def>
</glossary></div2></div1>
<div1 title="Indexes"><p class="bref"><a class="TOC" href="?scrBook=Gen&amp;scrCh=1&amp;scrV=1#a-p1">1:1</a></p></div1>
</ThML.body></ThML>
"""
_ep = tmp(EASTON, ".xml")
eb = st.convert_easton(_ep, kjv_path=KJV)
eu = {u["id"]: u for u in eb["units"]}
aaron = eu["easton:aaron"]
check("easton: one unit per <term>, keyed by headword slug, ref the headword as printed",
      list(eu) == ["easton:aaron", "easton:court", "easton:moses"] and aaron["ref"] == "Aaron"
      and aaron["lex"]["headword"] == "Aaron")
check("easton: text is the definition's paragraphs, tags gone, entities read",
      aaron["text"].count("\n\n") == 1 and "<" not in aaron["text"]
      and eu["easton:court"]["text"] == "An enclosure & a yard.")
sc = [l for l in aaron["links"] if l["kind"] == "scripture"]
check("easton: CCEL's parsed scripRef becomes a kjv: link; repeats within an entry merge",
      [l["osis"] for l in sc] == ["Exod.6.20", "Exod.4.27", "Gen.1.1", "Gen.1.2", "1Macc.1.57", "Gen.1.24"]
      and sc[1]["end"] == "Exod.4.30" and sc[2].get("chapter") is True)
check("easton: Exod 6:20 is not in the fixture KJV, so it stays unresolved (checked, not trusted)",
      sc[0]["resolved"] is False and sc[3]["resolved"] is True and sc[5]["resolved"] is False)
see = [l for l in aaron["links"] if l["kind"] == "see"]
check("easton: <a href ...?term=> cross-references resolve to entries; plural to singular is marked",
      see[0] == {"kind": "see", "label": "Moses", "target": "easton:moses"}
      and see[2] == {"kind": "see", "label": "Courts", "target": "easton:court", "match": "number"})
check("easton: a reference to no entry is kept, unresolved",
      see[1]["resolved"] is False and "target" not in see[1])
check("easton: the scripture index after the glossary is not read as entries",
      len(eb["units"]) == 3)
s = eb["scheme"]["stats"]
check("easton: the scheme counts what it did",
      s["scripture_refs"] == 7 and s["scripture_resolved"] == 4 and s["scripture_unresolved"] == 3
      and s["see_resolved"] == 2 and s["see_unresolved"] == 1 and s["unresolved_why"] ==
      {"book not in the KJV build (Apocrypha)": 1, "no such verse in the KJV": 2})
check("easton: rights: the file's own DC.Rights line, whole redistribution allowed",
      eb["rights"]["rights_line"] == "Public Domain" and eb["rights"]["redistribute_whole"] is True
      and eb["source"]["format"] == "dictionary-thml")
os.unlink(_ep)

# ---------------------------------------------------------------- Nave's (ThML)
NAVE = THML_HEAD + """<glossary id="a-p0.1">
<term id="t1">PRIEST</term>
<def type="Scripture References" id="d1">
<p class="index2" id="p1">Of Melchizedek <scripRef id="s1" passage="Ge 1:1" parsed="|Gen|1|1|0|0" osisRef="Bible:Gen.1.1">Ge 1:1</scripRef></p>
<p class="index3" id="p2">Consecrated <scripRef id="s2" passage="Ex 4:1-3" parsed="|Exod|4|1|0|3" osisRef="Bible:Exod.4.1-Exod.4.3">Ex 4:1-3</scripRef></p>
<p class="index2" id="p3">See <a href="bible.l.html?term=levites" id="a1">LEVITES</a></p>
</def>
<term id="t2">HIGH PRIEST</term>
<def type="Scripture References" id="d2">
<p class="index2" id="p4">See <a href="bible.p.html?term=priest,+high" id="a2">PRIEST, HIGH</a>; <a href="bible.a.html?term=abstinence" id="a3">ABSTINENCE</a></p>
</def>
<term id="t3">ABSTINENCE, TOTAL</term>
<def type="Scripture References" id="d3"><p class="index2" id="p5"><scripRef id="s3" passage="Col 9:9" parsed="|Col|9|9|0|0" osisRef="Bible:Col.9.9">Co 9:9</scripRef></p></def>
</glossary></ThML.body></ThML>
"""
_np = tmp(NAVE, ".xml")
nb = st.convert_nave(_np, kjv_path=KJV)
nu = {u["id"]: u for u in nb["units"]}
check("nave: topics keyed by slug, printed in capitals as the source has them",
      list(nu) == ["nave:priest", "nave:high-priest", "nave:abstinence-total"]
      and nu["nave:priest"]["ref"] == "PRIEST")
check("nave: sub-topic depth rides in lex.levels, one per paragraph",
      nu["nave:priest"]["lex"]["levels"] == [2, 3, 2] and nu["nave:priest"]["text"].count("\n\n") == 2)
check("nave: a verse range within a chapter keeps its end",
      nu["nave:priest"]["links"][1]["end"] == "Exod.4.3")
hs = nu["nave:high-priest"]["links"]
check("nave: 'PRIEST, HIGH' (a sub-topic) links the topic it sits under, marked match=topic",
      hs[0] == {"kind": "see", "label": "PRIEST, HIGH", "target": "nave:priest", "match": "topic"})
check("nave: a name that begins exactly one topic links it, marked match=prefix",
      hs[1]["target"] == "nave:abstinence-total" and hs[1]["match"] == "prefix")
check("nave: an abbreviation CCEL misparsed (Co -> Col 9) names no KJV chapter and stays unresolved",
      nu["nave:abstinence-total"]["links"][0]["resolved"] is False)
check("nave: rights held (DC.Rights empty in the file): redistribute_whole false",
      nb["rights"]["redistribute_whole"] is False)
os.unlink(_np)

# ---------------------------------------------------------------- the manifest
SLUGS = [x for x in ("easton", "nave", "hurlbut-bible-atlas") if x in fs.LEXICONS]
PINS = {"easton": "b8e82aa7ca847f4d97fb432cd965e398a111333c",
        "nave": "eeb9b7418be4d02c497d142da3b9890fad356252",
        "hurlbut-bible-atlas": "https://archive.org/download/bibleatlasamanua41140gut/"}
check("fetch: each is pinned (a commit in the URL, or an archive.org item) and by sha256",
      SLUGS and all(len(fs.LEXICON_SHA256[x]) == 64 and PINS[x] in fs.LEXICONS[x][0] for x in SLUGS))
man = json.load(open(os.path.join(ROOT, "data", "books", "manifest.json"), encoding="utf-8"))
check("manifest: each committed entry carries the pinned sha256 and its rights block",
      all(x in man and man[x]["sha256"] == fs.LEXICON_SHA256[x] and "rights" in man[x] for x in SLUGS))

# ---------------------------------------------------------------- the real books, when fetched
LEX = os.path.join(ROOT, "data", "corpus", "lexicons")
BOOKS = {"easton": ("easton-ebd.xml", "convert_easton"), "nave": ("nave-bible.xml", "convert_nave"),
         "hurlbut-bible-atlas": ("hurlbut-bible-atlas.txt", "convert_hurlbut_atlas")}
real = [(x, BOOKS[x][0], getattr(st, BOOKS[x][1])) for x in SLUGS
        if os.path.exists(os.path.join(LEX, BOOKS[x][0])) and os.path.exists(st.KJV_PARALLEL)]
for slug, fn, conv in real:
    b = conv(os.path.join(LEX, fn))
    links = [l for u in b["units"] for l in u["links"] if l["kind"] == "scripture"]
    check(f"{slug} (fetched): unit count is the manifest's, every unit has text, "
          f"every resolved link names a KJV verse",
          len(b["units"]) == man[slug]["units"] and all(u["text"] for u in b["units"])
          and all(l["target"][4:] in st.kjv_verse_index()[0] for l in links if l["resolved"]))
if not real:
    print("(fetched books absent: whole-book checks skipped)")

os.unlink(KJV)
print(f"\n{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
