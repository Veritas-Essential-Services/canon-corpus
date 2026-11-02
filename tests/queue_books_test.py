"""The illustrated-classics queue converter (structure_texts.convert_divided, 2026-11-01).

Synthetic sources only (no book text): each case builds a tiny file shaped like the real one and checks
the ids, refs, rubrics and cuts the config promises. Run: python tests/queue_books_test.py
"""
import os, sys, tempfile, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(HERE, "..", "pipeline")
sys.path.insert(0, PIPE)
spec = importlib.util.spec_from_file_location("structure_texts", os.path.join(PIPE, "structure_texts.py"))
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

passed = failed = 0
def check(name, cond):
    global passed, failed
    print(("ok    " if cond else "FAIL  ") + name)
    passed, failed = passed + bool(cond), failed + (not cond)

def build(slug, *texts):
    d = tempfile.mkdtemp()
    ps = []
    for i, t in enumerate(texts):
        p = os.path.join(d, f"{slug}.{i}.txt")
        open(p, "w", encoding="utf-8").write("*** START OF THIS PROJECT GUTENBERG EBOOK X ***\n" + t +
                                              "\n*** END OF THIS PROJECT GUTENBERG EBOOK X ***\n")
        ps.append(p)
    b = S.convert_divided(ps, slug, S.QUEUE_BOOKS[slug])
    return b, {u["id"]: u for u in b["units"]}

# Malory: the Contents' preface is skipped by start_min_line; a rubric is unit .0; a bare CHAPTER takes the
# next paragraph as its rubric once Pollard's note is scrubbed; the split "CHAP TER" heading is mended.
contents = "PREFACE OF WILLIAM CAXTON\n\n" + "filler\n" * 420
v1 = (contents + "PREFACE OF WILLIAM CAXTON\n\nAlpha beta.\n\nBOOK I\n\n\n"
      "CHAPTER I. How one thing\nbefell.\n\nGamma delta.\n\nEpsilon.\n\n"
      "CHAPTER II[*1]\n\n\n[*1] Misnumbered by the printer.\n\n\nHow another thing befell.\n\nZeta.\n\n"
      "BOOK II.\n\nCHAP TER I. How a third befell.\n\nEta.\n\nGLOSSARY\n\nword, gloss\n")
v2 = "BOOK X\n\nCHAPTER I. How the tenth began.\n\nTheta.\n\nGLOSSARY\n\nmore\n"
b, u = build("malory-morte", v1, v2)
check("malory: preface kept once, contents copy cut", list(u)[0] == "malory-morte:preface.1" and
      sum(1 for k in u if k.startswith("malory-morte:preface")) == 1)
check("malory: rubric is .0, marked heading", u["malory-morte:1.1.0"].get("heading") and
      u["malory-morte:1.1.0"]["text"].startswith("CHAPTER I. How one thing befell"))
check("malory: paragraphs count from 1 under the rubric", u["malory-morte:1.1.2"]["text"] == "Epsilon.")
check("malory: bare chapter takes the next paragraph as rubric", u["malory-morte:1.2.0"]["text"] ==
      "How another thing befell." and u["malory-morte:1.2.1"]["text"] == "Zeta.")
check("malory: Pollard's note scrubbed", not any("Misnumbered" in x["text"] for x in u.values()))
check("malory: CHAP TER mended", "malory-morte:2.1.1" in u)
check("malory: second volume continues the books", u["malory-morte:10.1.1"]["text"] == "Theta.")
check("malory: glossary cut", not any("gloss" in x["text"] or "more" == x["text"] for x in u.values()))

# Ovid: BOOK THE <ordinal>, fables keyed by number with the Latin range in the ref, footnotes and the
# EXPLANATION commentary gone, Riley's braces dropped (words kept).
ov = ("BOOK THE FIRST.\n\n\nTHE ARGUMENT. [I.1-4]\n\nOne {more} line.[1]\n\n"
      "    [Footnote 1: _One._--Ver. 1. A note\n    over two lines.]\n\n\n"
      "FABLE I. [I.5-31]\n\n  A summary.\n\nBody text.\n\nEXPLANATION.\n\nCommentary.\n\n"
      "FABLES II. AND III. [I.32-88]\n\nMore.\n\nTranscriber's Note on the Text:\n\nnotes\n")
ov2 = "BOOK THE EIGHTH.\n\nFABLE I. [VIII.1-151]\n\nEighth.\n\nTHE END.\n\nafter\n"
b, u = build("ovid-riley", ov, ov2)
check("ovid: argument keyed and ranged", u["ovid-riley:1.arg.1"]["ref"] == "Book I, The Argument [I.1-4], par. 1")
check("ovid: braces dropped, footnote mark and block gone", u["ovid-riley:1.arg.1"]["text"] == "One more line.")
check("ovid: summary is paragraph 1", u["ovid-riley:1.f1.1"]["text"] == "A summary.")
check("ovid: EXPLANATION muted", not any(x["text"] == "Commentary." for x in u.values()))
check("ovid: joint fables keyed f2-3", u["ovid-riley:1.f2-3.1"]["ref"].startswith("Book I, Fables II and III"))
check("ovid: second file, book VIII", "ovid-riley:8.f1.1" in u and not any(x["text"] == "after" for x in u.values()))

# Bulfinch: "Chapter I" then the title paragraph; the title goes into the label, not a unit.
aof = ("Contents\n\nChapter I\n\nStories of Gods and Heroes.\n\n\nChapter I\n\nIntroduction\n\nFirst para.\n\n"
       "CHAPTER II\n\nPrometheus and Pandora\n\nSecond.\n\nSKETCH OF THE HISTORY OF GREEK SCULPTURE\n\nx\n")
b, u = build("bulfinch-age-of-fable", aof)
check("bulfinch: title paragraph joins the label", u["bulfinch-age-of-fable:ch1.1"]["ref"] ==
      "Chapter I: Introduction, par. 1")
check("bulfinch: capital CHAPTER too", u["bulfinch-age-of-fable:ch2.1"]["text"] == "Second.")
check("bulfinch: sculpture sketch cut", len(u) == 2)

# Hesiod: section headings to keys; (ll. a-b) carried to later paragraphs; [nnnn] note marks scrubbed.
hes = ("THE WORKS OF HESIOD\n\n\nWORKS AND DAYS (832 lines)\n\n(ll. 1-10) Muses [1301].\n\nAttend.\n\n"
       "THE ASTRONOMY (fragments)\n\nFragment #1--Athenaeus: stars.\n\n"
       "THE CATALOGUES OF WOMEN AND EOIAE (fragments) [1701]\n\nFragment #1--x.\n\nII. [1745]\n\n(ll. 1-2) y.\n\n"
       "WORKS ATTRIBUTED TO HOMER\n\nhymns\n")
b, u = build("hesiod-evelyn-white", hes)
check("hesiod: works and days is wd, line range in ref", u["hesiod-evelyn-white:wd.1"]["ref"] == "Works and Days, ll. 1-10")
check("hesiod: range carried to the next paragraph", u["hesiod-evelyn-white:wd.2"]["ref"] == "Works and Days, ll. 1-10")
check("hesiod: note mark scrubbed", u["hesiod-evelyn-white:wd.1"]["text"] == "(ll. 1-10) Muses.")
check("hesiod: fragment group keyed, fr. in ref", u["hesiod-evelyn-white:astronomy.1"]["ref"] == "Astronomy (fragments), fr. 1")
check("hesiod: Catalogues book II", "hesiod-evelyn-white:catalogues-of-women-and-eoiae2.1" in u)
check("hesiod: Homerica cut", not any(x["text"] == "hymns" for x in u.values()))

# Robin Hood: chapters numbered by the book's own Contents, matched however the heading is cased.
rh = ("PREFACE\n\nFROM THE AUTHOR TO THE READER\n\nWelcome.\n\nCONTENTS\n\n How Robin Hood Came To Be An Outlaw\n"
      " Robin Hood And The Tinker\n Epilogue\n\n\nPROLOGUE\n\nGiving an account.\n\n"
      "How Robin Hood Came to Be an Outlaw\n\nOne.\n\nPART FIRST\nTelling how.\n\n\nRobin Hood and the Tinker\n\n"
      "Two.[1]\n\n  [1] A footnote\n  of two lines.\n\nEpilogue\n\nEnd.\n\nEnd of Project Gutenberg's book\n")
b, u = build("pyle-robin-hood", rh)
check("robin hood: preface kept, its subtitle dropped", u["pyle-robin-hood:preface.1"]["text"] == "Welcome.")
check("robin hood: contents scrubbed", not any("Tinker" in x["text"] for x in u.values()))
check("robin hood: chapters by contents order", u["pyle-robin-hood:ch1.1"]["text"] == "One." and
      u["pyle-robin-hood:ch2.1"]["text"] == "Two.")
check("robin hood: part summary split from its heading", u["pyle-robin-hood:part1.1"]["text"] == "Telling how.")
check("robin hood: footnote gone", len([k for k in u if k.startswith("pyle-robin-hood:ch2")]) == 1)
check("robin hood: epilogue, no licence line", u["pyle-robin-hood:epilogue.1"]["text"] == "End." and
      "pyle-robin-hood:epilogue.2" not in u)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
