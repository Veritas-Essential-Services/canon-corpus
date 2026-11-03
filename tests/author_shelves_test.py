#!/usr/bin/env python3
# prov: 2026-11-03 claude-opus-5-5 drafted (the author shelves: Tolkien, Lewis, Sayers, Chesterton)
"""The author shelves (pipeline/author_shelves.json), offline: the ledger, the Standard Ebooks fetcher's
spine and rights gate, the SE converter and the Middle English Vocabulary converter on inline fixtures,
and the manifest entries the build committed. No network, no corpus."""
import json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import fetch_sources as fs  # noqa: E402
import structure_texts as st  # noqa: E402

fails = passes = 0
def ok(c, m):
    global fails, passes
    print(("ok    " if c else "FAIL  ") + m)
    if c: passes += 1
    else: fails += 1

L = fs.author_shelves()
ok(list(L["shelves"]) == ["tolkien", "lewis", "sayers", "chesterton"], "four shelves, in order")
se = fs.se_books()
ok(len(se) == 10 and all(len(r["commit"]) == 40 and len(r["sha256"]) == 64 and r["year"] <= 1930 for r in se.values()),
   "ten Standard Ebooks books, each pinned to a commit and a sha256, each from 1930 or before")
ok(se["lewis-dymer"]["files"] == "dymer" and se["lewis-spirits-in-bondage"]["repo"] == se["lewis-dymer"]["repo"],
   "C. S. Lewis's Poetry is two books, cut by file prefix")
ag = fs.archive_gutenberg_books()
ok(list(ag) == ["tolkien-middle-english-vocabulary"] and len(ag["tolkien-middle-english-vocabulary"]["sha256"]) == 64, "Tolkien's vocabulary, pinned")
held = L["shelves"]["chesterton"]["held"]["slugs"]
ok(len(held) == 61 and "chesterton-orthodoxy" in held and "chesterton-heretics" in held and not set(held) & set(se), "61 Chesterton books held before, Orthodoxy and Heretics among them; none fetched twice")
ok(all(s["waiting"]["count"] > 0 and s["waiting"]["first"] >= "2027-01-01" and s["waiting"]["posthumous"] for s in L["shelves"].values()),
   "each shelf counts its waiting books and says how its posthumous ones are reckoned")
m20 = json.load(open(os.path.join(HERE, "..", "pipeline", "mysteries-1920s_shelf.json")))
ok("sayers-strong-poison" not in m20["gutenberg"] and "sayers-strong-poison" in m20["_held"], "Strong Poison has one owner")

# --- the fetcher, on a fake repository
OPF = '<item href="text/titlepage.xhtml" id="titlepage.xhtml"/><item href="text/imprint.xhtml" id="imprint.xhtml"/>' \
      '<item href="text/dymer-chapter-1.xhtml" id="dymer-chapter-1.xhtml"/><item href="text/spirits-in-bondage-chapter-1.xhtml" id="spirits-in-bondage-chapter-1.xhtml"/>' \
      '<item href="text/uncopyright.xhtml" id="uncopyright.xhtml"/>' \
      '<itemref idref="titlepage.xhtml"/><itemref idref="imprint.xhtml"/><itemref idref="spirits-in-bondage-chapter-1.xhtml"/><itemref idref="dymer-chapter-1.xhtml"/><itemref idref="uncopyright.xhtml"/>'
ok(fs.se_spine(OPF) == ["titlepage.xhtml", "imprint.xhtml", "spirits-in-bondage-chapter-1.xhtml", "dymer-chapter-1.xhtml", "uncopyright.xhtml"], "the spine, in reading order")
X = '<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><body>{}</body></html>'
IMPRINT = X.format('<section id="imprint"><p>The source text and artwork in this ebook are believed to be in the United States public domain.</p><p>CC0 1.0 Universal</p></section>')
DYMER = X.format('<article id="dymer-chapter-1" epub:type="chapter z3998:poem"><h3><span epub:type="se:label">Canto</span> <span>I</span></h3>'
                 '<section id="dymer-chapter-1-stanza-1"><header><p epub:type="z3998:ordinal">1</p></header><p><span>You stranger, long</span><br/><span>Upon these words</span></p></section>'
                 '<section id="dymer-chapter-1-stanza-2"><header><p epub:type="z3998:ordinal">2</p></header><p><span>This moment</span></p></section></article>')
files = {"content.opf": OPF, "text/imprint.xhtml": IMPRINT, "text/uncopyright.xhtml": X.format('<section id="uncopyright"><p>x</p></section>'),
         "text/dymer-chapter-1.xhtml": DYMER, "text/spirits-in-bondage-chapter-1.xhtml": X.format("<section id='x'/>")}
get = lambda url: files[url.split("/src/epub/", 1)[1]]
row = {"repo": "r", "commit": "c" * 40, "files": "dymer", "title": "Dymer", "year": 1926, "sha256": "0" * 64}
with tempfile.TemporaryDirectory() as d:
    try:
        fs.fetch_se("t", row, corpus=d, get=get); ok(False, "a wrong pin is refused")
    except RuntimeError as e:
        ok("refused" in str(e) and not os.listdir(d), "a wrong pin is refused, and nothing is written")
    import hashlib
    joined = "".join(f"<!-- se-file: {f} -->\n" + files["text/" + f] + "\n" for f in ("imprint.xhtml", "dymer-chapter-1.xhtml", "uncopyright.xhtml"))
    row["sha256"] = hashlib.sha256(joined.encode()).hexdigest()
    r = fs.fetch_se("t", row, corpus=d, get=get)
    path = os.path.join(d, "standardebooks", "t.xhtml")
    ok("3 files" in r and "spirits" not in open(path).read(), "the prefix takes Dymer's files and the imprint pages, not the other book's")
    files["text/imprint.xhtml"] = X.format('<section id="imprint"><p>All rights reserved.</p></section>')
    try:
        fs.fetch_se("t2", row, corpus=d, get=get); ok(False, "no rights line: refused")
    except RuntimeError as e:
        ok("rights gate" in str(e), "an imprint without SE's public-domain and CC0 lines is refused before the pin is read")
    st.CORPUS = d
    b = st.convert_se_book(path, "lewis-dymer", "Dymer", "C. S. Lewis", row)
    ok([u["id"] for u in b["units"]] == ["lewis-dymer:1.1", "lewis-dymer:1.2"], "a numbered stanza is one unit at its own number")
    ok(b["units"][0]["text"] == "You stranger, long / Upon these words" and b["units"][0]["ref"] == "Dymer, Canto I, stanza 1",
       "verse lines kept as lines; the stanza number and the heading are not text")
    ok(b["rights"]["redistribute_whole"] is True and "CC0" in b["rights"]["license"] and b["title"] == "Dymer (1926)", "the rights block and the dated title")
    LETTER = X.format('<section id="chapter-1" epub:type="chapter z3998:letter"><header><hgroup><h3>1</h3><p epub:type="title">Agatha to Olive</p></hgroup>'
                      '<p>15, Whittington Terrace</p></header><p>Thank you<a epub:type="noteref" href="#n">1</a> very much.</p>'
                      '<footer><p><span>Your loving sister,</span><br/><b>Aggie</b></p></footer></section>')
    p2 = os.path.join(d, "l.xhtml"); open(p2, "w").write("<!-- se-file: chapter-1.xhtml -->\n" + LETTER + "\n")
    b = st.convert_se_book(p2, "s", "Docs", "D", {"year": 1930})
    ok([u["text"] for u in b["units"]] == ["15, Whittington Terrace", "Thank you very much.", "Your loving sister, / Aggie"] and b["units"][0]["id"] == "s:1.1"
       and b["units"][0]["ref"] == "Docs, 1. Agatha to Olive, par. 1", "a letter's dateline and signature are text, its heading is not, a note marker is dropped")
    MEV = ("*** START OF THIS PROJECT GUTENBERG EBOOK X ***\n\nPREFACE\n\nThis vocabulary.\n\n[Transcriber's Note: x]\n\n"
           "#A#, _pron._ he, XIII _a_ 27.\n\n#Abate#, _v._ to lessen.\n\nreduce, VIII.\n\n#Uncouþe#, _adj._ strange.\n\n#Þat#, _conj._ that.\n\n*** END OF THIS PROJECT GUTENBERG EBOOK X ***\n")
    p3 = os.path.join(d, "m.txt"); open(p3, "w").write(MEV)
    b = st.convert_middle_english_vocabulary(p3, "t", "T", "J. R. R. Tolkien")
    ok([u["id"] for u in b["units"]] == ["t:front.1", "t:front.2", "t:A.1", "t:A.2", "t:V.1", "t:Þ.1"], "front matter, then entries by letter (U filed with V, as printed); the transcriber's note dropped")
    ok(b["units"][3]["text"].endswith("reduce, VIII.") and b["units"][3]["lex"]["headword"] == "Abate", "a sense after a blank line stays in its entry")

man = json.load(open(os.path.join(HERE, "..", "data", "books", "manifest.json"), encoding="utf-8"))
built = list(se) + list(ag)
ok(all(s in man and man[s]["units"] > 100 for s in built), "all eleven books are in the manifest")
ok(man["lewis-dymer"]["units"] == 295 and man["tolkien-middle-english-vocabulary"]["units"] == 4640 and man["chesterton-incredulity"]["units"] == 1143,
   "the counts the build measured (Dymer 295 units: 9 cantos' stanzas and the epigraph)")
print(f"{passes} passed, {fails} failed")
sys.exit(1 if fails else 0)
