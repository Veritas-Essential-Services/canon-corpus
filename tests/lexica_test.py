#!/usr/bin/env python3
"""Offline checks for pipeline/betacode.py and pipeline/lexica.py: the
shareable lexicons (Perseus LSJ, Abbott-Smith, Lewis & Short) and the
STEPBible supplement's selection rule. Fixtures inline; with the real sources
fetched (data/corpus/lexicons/), also checks them.

    python3 tests/lexica_test.py"""
import glob, os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import betacode, lexica

PASS = 0
FAIL = []
def check(label, cond):
    global PASS
    if cond: PASS += 1
    else: FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label)

def skip(label):
    print("skip " + label)

# ---------------------------------------------------------------- Beta Code
B = betacode.to_unicode
check("lo/gos -> λόγος (final sigma)", B("lo/gos") == "λόγος")
check("*)ihsou=s -> Ἰησοῦς (capital with its marks before the letter)", B("*)ihsou=s") == "Ἰησοῦς")
check("tw=| -> τῷ (circumflex + iota subscript compose)", B("tw=|") == "τῷ")
check("h(me/ra -> ἡμέρα (rough breathing then acute)", B("h(me/ra") == "ἡμέρα")
check("e)kklhsi/a -> ἐκκλησία", B("e)kklhsi/a") == "ἐκκλησία")
check("a medial sigma stays medial", B("sw/zw") == "σώζω")
check("a sigma before punctuation is final", B("lo/gos,") == "λόγος,")
check("headword_key drops marks and case and unifies sigma",
      betacode.headword_key("Λόγος") == betacode.headword_key("λογος") == "λογοσ")
check("an LSJ homograph key a)1 becomes an id with ~h1", lexica._lsj_id("a)1") == "ἀ~h1")
check("a capital's marks written AFTER its letter still attach (*)a/ploun -> Ἄπλουν)", B("*)a/ploun") == "Ἄπλουν")
check("body_agrees: ἆ's TFLSJ body opening on ἔᾱ is caught", not lexica.body_agrees("ἆ", "ἔᾱ , Epic dialect"))
check("body_agrees: LSJ's hyphenated stem ἀγάπ-η is the same word", lexica.body_agrees("ἀγάπη", "<b>ἀγάπ-η</b>, ἡ, love"))
check("body_agrees: a comma list of forms matches any of them", lexica.body_agrees("α, Ἀλφα", "ἄλφα , τό"))

tmp = tempfile.mkdtemp()
def write(name, s):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)
    return p

# ---------------------------------------------------------------- Perseus LSJ
LSJ = write("grc.lsj.perseus-eng1.xml", """<TEI.2><text><body><div0>
<entryFree id="n1" key="lo/gos" type="main"><orth lang="greek">lo/gos</orth>, <gen lang="greek">o(</gen>,
 <sense n="A">computation, cf. <foreign lang="greek">le/gw</foreign>
 <bibl n="urn:cts:greekLit:tlg0059.tlg030.perseus-grc1:340d">Pl.<title>R.</title>340d</bibl>.</sense></entryFree>
<entryFree id="n2" key="a)1" type="main"><orth lang="greek">a)</orth> privative</entryFree>
</div0></body></text></TEI.2>""")
b = lexica.convert_lsj_perseus([LSJ])
u = {x["id"]: x for x in b["units"]}
check("LSJ: ids are the Unicode headword", "lsj-perseus:λόγος" in u and "lsj-perseus:ἀ~h1" in u)
check("LSJ: Greek runs are converted, English is left alone",
      u["lsj-perseus:λόγος"]["text"].startswith("λόγος, ὁ, computation, cf. λέγω"))
check("LSJ: a tail inside a Greek run's parent stays English", "privative" in u["lsj-perseus:ἀ~h1"]["text"])
c = u["lsj-perseus:λόγος"]["links"]
check("LSJ: a quotation's CTS URN becomes a cites link, unresolved and labelled",
      c == [{"kind": "cites", "urn": "urn:cts:greekLit:tlg0059.tlg030.perseus-grc1", "passage": "340d",
             "label": "Pl.R.340d", "resolved": False}])
check("LSJ: the ref names the homograph", u["lsj-perseus:ἀ~h1"]["ref"] == "LSJ s.v. ἀ (1)")
check("LSJ: CC BY-SA, share-alike, shareable whole",
      b["rights"]["license"] == "CC BY-SA 4.0" and b["rights"]["share_alike"] and "redistribute_whole" not in b["rights"])

# ---------------------------------------------------------------- Abbott-Smith
AS = write("abbott-smith.tei.xml", """<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>
<entry n="λόγος|G3056"><form><orth>λόγος</orth></form><sense><gloss>a word</gloss></sense></entry>
<entry n="ἀβαρής|G4"><form><orth>ἀβαρής</orth></form><sense><gloss>not burdensome</gloss></sense></entry>
<entry n="Ἀβιληνή"><form><orth>Ἀβιληνή</orth></form></entry>
</body></text></TEI>""")
a = lexica.convert_abbott_smith(AS)
au = {x["id"]: x for x in a["units"]}
check("Abbott-Smith: one unit per entry, id by lemma", set(au) == {"abbott-smith:λόγος", "abbott-smith:ἀβαρής", "abbott-smith:Ἀβιληνή"})
check("Abbott-Smith: the Strong's number becomes a link to strongs-greek",
      au["abbott-smith:λόγος"]["links"] == [{"kind": "lexical", "relation": "Strong's number", "target": "strongs-greek:G3056"}])
check("Abbott-Smith: an entry without a number has no link, and no invented number",
      au["abbott-smith:Ἀβιληνή"]["links"] == [] and au["abbott-smith:Ἀβιληνή"]["lex"]["strongs"] == "")
check("Abbott-Smith: public domain", a["rights"]["license"] == "Public domain")
AS_PLAIN = write("abbott-smith-plain.tei.xml", """<TEI><text><body>
<entry n="λόγος|G3056"><form><orth>λόγος</orth></form></entry></body></text></TEI>""")
check("Abbott-Smith: the real file's un-namespaced TEI reads the same (it built 0 entries once)",
      [x["id"] for x in lexica.convert_abbott_smith(AS_PLAIN)["units"]] == ["abbott-smith:λόγος"])

# ---------------------------------------------------------------- Lewis & Short
LS = write("lewis-short.xml", """<TEI.2><text><body><div0>
<entryFree id="n1" key="verbum" type="main"><orth lang="la">verbum</orth>, i, n. a word,
 <bibl n="urn:cts:latinLit:phi0474.phi053.perseus-lat2:1:13:23">Cic. Div. 1, 13, 23</bibl></entryFree>
</div0></body></text></TEI.2>""")
l = lexica.convert_lewis_short(LS)
check("L&S: id by key, text kept, colon passage becomes dots",
      l["units"][0]["id"] == "lewis-short:verbum" and l["units"][0]["links"][0]["passage"] == "1.13.23"
      and l["units"][0]["text"].startswith("verbum, i, n. a word"))

# ---------------------------------------------------------------- the supplement's rule
have = {betacode.headword_key(w) for w in ("λόγος", "ἄλφα", "ἆ")}
sel = lexica.select_supplement({"G3056": "λόγος",          # in Perseus: excluded
                                "G0001G": "ἄλφα", "G0001H": "ἆ",  # a split: both kept
                                "G6011": "λόγος",          # beyond Strong's: kept though LSJ has it
                                "G0078": "Ἀδδί"}, have)    # nobody has it: kept
check("supplement: an entry Perseus/Abbott-Smith already has is NOT taken", "G3056" not in sel)
check("supplement: both halves of a split are taken, and say why",
      sel.get("G0001G") == ["split"] and sel.get("G0001H") == ["split"])
check("supplement: a G6000+ entry is taken even when LSJ has the word", sel.get("G6011") == ["beyond-strongs"])
check("supplement: a word nobody else has is taken", sel.get("G0078") == ["not-in-perseus-or-abbott-smith"])
check("supplement: a word counts as missing only when NEITHER STEP spelling is in Perseus",
      lexica.select_supplement({"G0100": ["λογοςς", "λόγος"]}, have) == {})

STEP_HDR = "\t".join(["G0000", "G0000 =", "", "lemma", "translit", "pos", "gloss", "body"]) + "\n"
def row(k, lemma, gloss, body, rel="", tgt=""):
    return "\t".join([k[:5], f"{k} = {rel}", tgt, lemma, "tr", "N", gloss, body]) + "\n"
TB = write("tbesg.txt", row("G0001G", "ἄλφα", "alpha", "brief-a") + row("G0001H", "ἆ", "ah!", "brief-ah")
           + row("G3056", "λόγος", "word", "brief-logos") + row("G0078", "Ἀδδί", "Addi", "brief-addi"))
FL = write("tflsj.txt", row("G0001G", "ἄλφα", "alpha", "ἄλφα FULL-alpha") + row("G6011", "λόγος", "word", "FULL-lxx", "a Form of", "G3056")
           + row("G0001H", "ἆ", "ah!", "ἔᾱ FULL-wrong-word"))
s = lexica.convert_step_supplement(TB, [FL], [LSJ], AS)
su = {x["id"].split(":")[1]: x for x in s["units"]}
check("supplement: exactly the selected keys become units", set(su) == {"G0001G", "G0001H", "G6011", "G0078"})
check("supplement: ONE text per entry -- the full (TFLSJ) body where both exist, never both",
      "FULL-alpha" in su["G0001G"]["text"] and "brief-a" not in su["G0001G"]["text"])
check("supplement: TBESG where TFLSJ has none", "brief-addi" in su["G0078"]["text"])
check("supplement: a TFLSJ text that opens on another headword is set aside for the brief text, and says so",
      "brief-ah" in su["G0001H"]["text"] and "FULL-wrong-word" not in su["G0001H"]["text"]
      and su["G0001H"]["lex"]["step_edition"].startswith("TBESG (the TFLSJ text opens on another headword)"))
check("supplement: a relation to an entry left out points at the public Strong's entry",
      {"kind": "lexical", "relation": "a Form of", "target": "strongs-greek:G3056"} in su["G6011"]["links"])
check("supplement: links to the matching Perseus LSJ entry",
      {"kind": "lexical", "relation": "LSJ entry", "target": "lsj-perseus:λόγος"} in su["G6011"]["links"])
sp = lexica.convert_step_supplement(TB, [FL], [LSJ], AS, preferences={"G3056": "step", "G0078": "perseus"})
spu = {x["id"].split(":")[1]: x for x in sp["units"]}
check("review: a `step` answer takes an entry Perseus already has, marked preferred-by-review",
      spu.get("G3056", {}).get("lex", {}).get("why") == ["preferred-by-review"])
check("review: a `perseus` answer never removes an entry the rules take", "G0078" in spu)
check("betacode.accented_key keeps accents: ἁγνῶς and ἀγνώς differ, headword_key does not",
      betacode.accented_key("ἁγνῶς") != betacode.accented_key("ἀγνώς")
      and betacode.headword_key("ἁγνῶς") == betacode.headword_key("ἀγνώς"))
check("supplement: rights name STEPBible, CC BY 4.0, subset, shareable",
      s["rights"]["license"] == "CC BY 4.0" and "STEPBible" in s["rights"]["attribution"]
      and s["rights"]["shareable"] and s["rights"]["subset_of"] == ["tbesg-greek", "lsj-greek"])

# ---------------------------------------------------------------- enrichment (facts, not STEP's text)
LSJE = write("grc.lsj.perseus-eng5.xml", """<TEI.2><text><body><div0>
<entryFree id="e1" key="a)ga/ph" type="main"><orth lang="greek">a)ga/ph</orth>, love,
 <bibl n="urn:cts:greekLit:tlg0031.tlg006.perseus-grc1:5:8">Ep.Rom. 5.8</bibl>,
 <bibl n="urn:cts:greekLit:tlg0031.tlg126:1:12">Ep.Jud. 12</bibl>,
 <bibl n="urn:cts:greekLit:tlg0527.tlg027:22:1">LXX Ps. 22.1</bibl>,
 <bibl>Ev.Matt. 5.3</bibl>, <bibl>Ge. 1.1</bibl>,
 <bibl n="urn:cts:greekLit:tlg0059.tlg030.perseus-grc1:327a">Pl. R. 327a</bibl></entryFree>
<entryFree id="e2" key="ku/wn1" type="main"><orth lang="greek">ku/wn</orth>, dog, <foreign lang="greek">ku/wn fu/lac</foreign></entryFree>
<entryFree id="e3" key="ku/wn2" type="main"><orth lang="greek">ku/wn</orth>, a throw at dice</entryFree>
</div0></body></text></TEI.2>""")
eb = lexica.convert_lsj_perseus([LSJE])
kjv_ids = {"kjv:Rom.5.8", "kjv:Matt.5.3", "kjv:Jude.1.12"}
full_e = {"G0026": ("ἀγάπη", "", "", "love", "ἀγάπη love NT.Rom.5.8", "", ""),
          "G2965": ("κύων", "", "", "dog", "κύων dog φύλαξ", "", "")}
est = lexica.enrich_lsj(eb, {"0059": "Plato Phil.", "0031": "Novum Testamentum", "0527": "Septuaginta"},
                        {"5-4 B.C.": ["0059"]}, kjv_ids, full_e, {})
eu = {x["id"]: x for x in eb["units"]}
el = {l["label"]: l for l in eu["lsj-perseus:ἀγάπη"]["links"] if l["kind"] == "cites"}
check("enrich: an NT citation resolves to its KJV verse id",
      el["Ep.Rom. 5.8"]["target"] == "kjv:Rom.5.8" and el["Ep.Rom. 5.8"]["resolved"] is True)
check("enrich: LSJ's Jude (tlg126, not tlg026) resolves", el["Ep.Jud. 12"].get("target") == "kjv:Jude.1.12")
check("enrich: a Septuagint citation is labelled LXX, never resolved to the KJV",
      el["LXX Ps. 22.1"]["scripture"] == "LXX.Ps.22.1" and el["LXX Ps. 22.1"]["versification"] == "lxx"
      and el["LXX Ps. 22.1"]["resolved"] is False and "target" not in el["LXX Ps. 22.1"])
check("enrich: an untagged NT label is read and resolved", el["Ev.Matt. 5.3"].get("target") == "kjv:Matt.5.3")
check("enrich: a bare 'Ge.' with no URN is not taken for scripture", "Ge. 1.1" not in el)
check("enrich: a classical citation names its author and century",
      el["Pl. R. 327a"]["author"] == "Plato Phil." and el["Pl. R. 327a"]["date"] == "5-4 B.C.")
check("enrich: STEP's number-to-word mapping gives the entry its Strong's number and a link",
      eu["lsj-perseus:ἀγάπη"]["lex"]["strongs"] == ["G26"]
      and {"kind": "lexical", "relation": "Strong's number (STEPBible's mapping)", "target": "strongs-greek:G26"}
      in eu["lsj-perseus:ἀγάπη"]["links"])
check("enrich: between LSJ homographs, the Greek of STEP's text picks the one it describes",
      eu["lsj-perseus:κύων~h1"]["lex"].get("strongs") == ["G2965"] and "strongs" not in eu["lsj-perseus:κύων~h2"]["lex"])
check("enrich: no STEP text goes into the entry", "NT.Rom" not in eu["lsj-perseus:ἀγάπη"]["text"])
check("enrich: STEP's own references are the answer key, counted in the stats",
      est["check: NT refs, both"] == 1 and est["check: NT refs, STEP's"] == 1)
check("enrich: the rights name the CLTK tables and STEP's mapping",
      [e["license"] for e in eb["rights"]["enrichment"]] == ["MIT", "CC BY 4.0"])

# ---------------------------------------------------------------- the real sources, if here
L = os.path.join(HERE, "..", "data", "corpus", "lexicons")
lsjp = glob.glob(os.path.join(L, "perseus-lsj", "*.xml"))
if len(lsjp) == 27 and os.path.exists(os.path.join(L, "abbott-smith.tei.xml")) and os.path.exists(os.path.join(L, "tbesg-greek.txt")):
    rb = lexica.convert_lsj_perseus(lsjp)
    ids = [x["id"] for x in rb["units"]]
    check("real LSJ: 116,497 entries, ids unique", len(ids) == 116497 and len(set(ids)) == len(ids))
    lg = next(x for x in rb["units"] if x["id"] == "lsj-perseus:λόγος")
    check("real LSJ: λόγος is Unicode and cites Plato", lg["text"].startswith("λόγος") and any("tlg0059" in c["urn"] for c in lg["links"]))
    rs = lexica.convert_step_supplement(os.path.join(L, "tbesg-greek.txt"),
                                        [os.path.join(L, "tflsj-greek-0-5624.txt"), os.path.join(L, "tflsj-greek-extra.txt")],
                                        lsjp, os.path.join(L, "abbott-smith.tei.xml"))
    n = len(rs["units"])
    ra = lexica.convert_abbott_smith(os.path.join(L, "abbott-smith.tei.xml"))
    check("real Abbott-Smith: 6,153 entries", len(ra["units"]) == 6153)
    check(f"real supplement: a selection, not the lexicon ({n:,} of 9,550 keys)", 4000 < n < 5000)
    check("real supplement: G0001G and G0001H (α and ἆ) both present",
          {"step-greek-supplement:G0001G", "step-greek-supplement:G0001H"} <= {x["id"] for x in rs["units"]})
else:
    skip("the real lexicon sources are not fetched (python3 pipeline/fetch_sources.py)")

print(f"\n{PASS} passed, {len(FAIL)} failed")
for f in FAIL:
    print("  FAIL", f)
sys.exit(1 if FAIL else 0)
