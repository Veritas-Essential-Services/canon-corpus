#!/usr/bin/env python3
# prov: 2026-10-03 drafted (Claude Code)
# fable_review: pending
"""The cross-reference layer: the Treasury reader rule by rule on lines as
the scans print them (offline, no corpus needed), then the committed
data/xrefs/ files against the KJV ids and their manifest."""
import hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import tsk_read as T
import tsk_glyphs as G
import build_xrefs as B

fails = passed = 0
def check(m, c):
    global fails, passed
    print(("ok    " if c else "FAIL  ") + m)
    if c: passed += 1
    else: fails += 1

shape = T.kjv_shape()
def R(text):
    return [(kw, [(r["abbr"], r["c"], r["v"], r["c2"], r["v2"]) for r in rs]) for kw, rs in T.refs(text)]

# ---- numerals and running heads
check("roman: XVII, and the OCR's l for I", T.roman("XVII") == 17 and T.roman("XIl") == 12)
check("roman: CXIX", T.roman("CXIX") == 119)
check("head: 'B.C. 1913. GENESIS, XVII. A.M. 2091.'", T.parse_head("B.C. 1913. GENESIS, XVII. A.M. 2091.") == ("Gen", 17))
check("head: a misspelt name still matches (2SAMURL)", T.parse_head("8.0. 1035, 2SAMURL, XII. A.M, 2969,") == ("2Sam", 12))
check("head: THE ACTS", T.parse_head("A.D. 34. THE ACTS, IX. A.M. 4038.") == ("Acts", 9))
check("head: a psalm range gives its first psalm", T.parse_head("PSALMS, XVI—-XVIII.") == ("Ps", 16))
check("head: no book, no head", T.parse_head("THE CHRONOLOGICAL ORDER") is None)

# ---- references, as the Treasury prints them
r = R("beginning. Pr. 8. 22-24; 16.4. Mar. 13. 19. Jno. 1. 1-3. He. 1.10. 1 Jno. 1.1.")
check("Gen 1:1 'beginning': six references in one run", r == [("beginning", [
    ("Pr", 8, 22, None, 24), ("Pr", 16, 4, None, None), ("Mar", 13, 19, None, None),
    ("Jno", 1, 1, None, 3), ("He", 1, 10, None, None), ("1Jno", 1, 1, None, None)])])
r = R("God. Ps. 33. 6, 9; 148. 5. Mat. 8. 8.")
check("verse lists with commas, chapters after semicolons",
      r[0][1] == [("Ps", 33, 6, None, None), ("Ps", 33, 9, None, None), ("Ps", 148, 5, None, None), ("Mat", 8, 8, None, None)])
r = R("that. ver. 10, 12, 18. ch. 46. Ex. 20, 11.")
check("'ver.' keeps the entry's chapter; 'ch. 46.' is a whole chapter; 'Ex. 20, 11' reads the comma as the point",
      r[0][1] == [("ver", None, 10, None, None), ("ver", None, 12, None, None), ("ver", None, 18, None, None),
                  ("ch", 46, None, None, None), ("Ex", 20, 11, None, None)])
r = R("Joseph. Ge. 49.33-50.3.")
check("a range across chapters", r[0][1] == [("Ge", 49, 33, 50, 3)])
r = R("slew. Jude 14, 15. Ob. 3.")
check("a one-chapter book is cited by verse", r[0][1] == [("Jude", 1, 14, None, None), ("Jude", 1, 15, None, None), ("Ob", 1, 3, None, None)])
r = R("souls. Heb. souls. lift. Ex. 6.8.")
check("'Heb.' before a word is Hebrew, not Hebrews", r == [("souls Heb souls lift", [("Ex", 6, 8, None, None)])])
r = R("1 A.M. 2093. B.C. 1911. in. ch.46.2.")
check("the chronology (A.M., B.C.) is not a reference", [x for _, rs in r for x in rs] == [("ch", 46, 2, None, None)])
r = R("a. Ps.33.6. b. Is.40.12.")
check("two catchwords, two runs", [kw for kw, _ in r] == ["a", "b"])
check("a span indexes the text as read",
      (lambda t: [t[a:z] for a, z in T.refs(t)[0][1][0]["at"].values()])("x. Ps. 104. 24") == ["104", "24"])

# ---- resolving
g = lambda **k: dict({"abbr": "Ps", "c": None, "v": None, "c2": None, "v2": None}, **k)
check("Ps 33:6 resolves", T.resolve(g(c=33, v=6), "Gen", 1, shape) == [("Ps", 33, 6, 33, 6)])
check("Ps 184 is no psalm", T.resolve(g(c=184, v=3), "Gen", 1, shape) == [])
check("'ver. 5' is the entry's chapter", T.resolve(g(abbr="ver", v=5), "Gen", 2, shape) == [("Gen", 2, 5, 2, 5)])
check("'ch. 3. 15' is the entry's book", T.resolve(g(abbr="ch", c=3, v=15), "Gen", 1, shape) == [("Gen", 3, 15, 3, 15)])
check("a whole chapter is its first to last verse", T.resolve(g(c=23), "Gen", 1, shape) == [("Ps", 23, 1, 23, 6)])
check("a range past the chapter keeps its first verse", T.resolve(g(c=23, v=5, v2=9), "Gen", 1, shape) == [("Ps", 23, 5, 23, 5)])
check("an OCR form of two books: one candidate per book that has the verse",
      sorted(b for b, *_ in T.resolve(g(abbr="Jo", c=1, v=1), "Gen", 1, shape)) == ["Jer", "Josh"])
for t in [("Gen", 1, 1, 1, 1), ("Prov", 8, 22, 8, 24), ("Gen", 49, 33, 50, 3)]:
    check(f"ref id round trip {T.ref_id(t)}", T.parse_ref_id(T.ref_id(t)) == t)

# ---- the alignment
check("digit alternatives: 8 may be 3, 9 may be 2", set(T.digit_alternatives("8")) == {3} and 2 in T.digit_alternatives("9"))
lines = [("CHAP. I.", (0, 0, 0)), ("GOD creates heaven and earth, 1; the light, 3;", (0, 0, 1)),
         ("1 beginning. Pr. 8. 22-24.", (0, 0, 2)), ("2 without. Job 26.7.", (0, 0, 3)),
         ("8 God. Ps. 33. 6.", (0, 0, 4)), ("1 Ki. 4. 33. Is. 45. 7.", (0, 0, 5)),
         ("4 that. ver. 10.", (0, 0, 6)), ("CHAP. II.", (0, 0, 7)), ("1 Thus. Ex. 20.11.", (0, 0, 8))]
ents, log = T.align(lines, shape)
got = [(e["verse"], e["rule"]) for e in ents]
check("align: Gen 1:1, 1:2, a misread '8' taken as 1:3, then 1:4, then 2:1",
      got == [(("Gen", 1, 1), "read"), (("Gen", 1, 2), "read"), (("Gen", 1, 3), "digit"),
              (("Gen", 1, 4), "read"), (("Gen", 2, 1), "read")])
check("align: '1 Ki. 4. 33.' is a continuation of 1:3, not an entry",
      ents[2]["lines"] == [4, 5])
check("align: a chapter's summary belongs to no entry", all(1 not in e["lines"] for e in ents))

# ---- the glyph model
if os.path.exists(G.MODEL):
    rep = json.load(open(G.MODEL, encoding="utf-8")).get("report", {})   # no numpy needed to read it
    check("glyph model: held-out agreement >= 98%", rep.get("held_out_agreement", 0) >= 0.98)
    check("glyph model: decide() calls only sure glyphs", G.decide(0.95) == "3" and G.decide(0.05) == "8" and G.decide(0.5) is None)
else:
    check("glyph model present (data/xrefs/glyph-3-8.json)", False)
try:
    import numpy as np
    import PIL  # noqa: F401
except ImportError:
    np = None
    print("skip  feature(): numpy and Pillow are not installed (python3 -m pip install numpy pillow)")
if np is not None:
    blob = np.zeros((20, 14), dtype=np.uint8) + 255
    check("feature(): a blank crop is no glyph", G.feature(blob) is None)

# corrected(): the model's calls, and a reference's status
gA, gB = (5, 10, 20, 0, 30, 90), (5, 30, 40, 0, 30, 90)
rd = [(("Gen", 1, 1), "x", {"abbr": "Ps", "c": 88, "v": 8, "c2": None, "v2": None,
                            "digits": {"c": "88", "v": "8"}, "glyphs": {"c": [gA, None], "v": [gB]}})]
fx = B.corrected(rd, {gA: 0.99, gB: 0.01})[0][2]
check("corrected(): a sure 3 read as 8 is fixed", (fx["c"], fx["v"], fx["status"]) == (38, 8, "fixed"))
fx = B.corrected(rd, {gA: 0.99, gB: 0.5})[0][2]
check("corrected(): one digit fixed and one unsure leaves the reference unsure", fx["status"] == "unsure")
fx = B.corrected(rd, {gB: 0.01})[0][2]
check("corrected(): a glyph with no crop keeps the OCR's reading, unsure", (fx["c"], fx["status"]) == (88, "unsure"))

# weak labels from the KJV's shape
gl = (5, 10, 20, 0, 30, 90)
reads = [(("Gen", 1, 1), "x", {"abbr": "Ps", "c": 184, "v": 3, "c2": None, "v2": None,
                               "digits": {"c": "184", "v": "3"}, "glyphs": {"c": [None, gl, None], "v": [None]}})]
check("weak label: Ps 184 cannot be, Ps 134 can: that 8 is a 3", B.weak_labels(reads, shape) == {gl: "3"})

# ---- combining two scans
s = lambda b, c, v: (b, c, v)
t1, t2, t3 = ("Prov", 8, 22, 8, 24), ("Ps", 33, 6, 33, 6), ("Isa", 45, 7, 45, 7)
per = {"rato": [(s("Gen", 1, 1), "beginning", t1, "as-read"), (s("Gen", 1, 2), "without", t3, "as-read"),
                (s("Gen", 1, 3), "God", t2, "fixed")],
       "drra": [(s("Gen", 1, 1), "beginning", t1, "as-read"), (s("Gen", 1, 1), "beginning", t3, "as-read")]}
entries_of = {"rato": {s("Gen", 1, 1), s("Gen", 1, 2), s("Gen", 1, 3)}, "drra": {s("Gen", 1, 1)}}
rows, one, counts = B.combine(per, entries_of, shape)
byv = {r["verse"]: r for r in rows}
check("combine: a reference both scans read under one verse is kept", "kjv:Prov.8.22-24" in byv["kjv:Gen.1.1"]["groups"][0]["refs"])
check("combine: one scan missed the 1:2 entry, so its Isa 45:7 ran on under 1:1: placed at 1:2",
      byv.get("kjv:Gen.1.2", {}).get("placed") == ["kjv:Isa.45.7"] and "kjv:Isa.45.7" not in str(byv["kjv:Gen.1.1"]))
check("combine: a reference only one scan reads is not committed",
      "kjv:Gen.1.3" not in byv and [o["ref"] for o in one] == ["kjv:Ps.33.6"])
check("combine: counts", counts["agreed"] == 1 and counts["placed"] == 1 and counts["one_scan_not_committed"] == 1)

# the earlier scan HAS an entry at the later verse: the two readings are two
# verses' references, not one run-on, and nothing is placed
entries_both = {"rato": {s("Gen", 1, 1), s("Gen", 1, 2), s("Gen", 1, 3)}, "drra": {s("Gen", 1, 1), s("Gen", 1, 2)}}
rows2, one2, counts2 = B.combine(per, entries_both, shape)
check("combine: no placement when both scans have the later entry", counts2["placed"] == 0
      and not any(r.get("placed") for r in rows2))
# the run-on is in the FIRST scan (rato missed the entry): placed from drra's side
per3 = {"rato": [(s("Gen", 1, 1), "beginning", t3, "unsure")],
        "drra": [(s("Gen", 1, 2), "without", t3, "unsure")]}
rows3, one3, counts3 = B.combine(per3, {"rato": {s("Gen", 1, 1)}, "drra": {s("Gen", 1, 1), s("Gen", 1, 2)}}, shape)
byv3 = {r["verse"]: r for r in rows3}
check("combine: a run-on in either scan is placed at the later verse, with the later scan's catchword",
      byv3.get("kjv:Gen.1.2", {}).get("placed") == ["kjv:Isa.45.7"]
      and byv3["kjv:Gen.1.2"]["groups"][0]["kw"] == "without" and one3 == [])
check("combine: a placed reference neither scan could read the 3/8 of is marked unsure_digit",
      byv3["kjv:Gen.1.2"].get("unsure_digit") == ["kjv:Isa.45.7"])

# --measure's digit classes
check("digit class: Ps 33:6 is shape-blind (Ps 38:6, 33:6... 83:6 all exist)",
      B.digit_class("kjv:Ps.33.6", shape) == "3/8, shape blind")
check("digit class: Prov 8:22-24 is shape-blind (Prov 3:22 exists)", B.digit_class("kjv:Prov.8.22-24", shape) == "3/8, shape blind")
check("digit class: Ps 134:3 is told by shape (Ps 184 is no psalm, 134:8 no verse)",
      B.digit_class("kjv:Ps.134.3", shape) == "3/8, shape tells")
check("digit class: Gen 1:1 has no 3/8", B.digit_class("kjv:Gen.1.1", shape) == "no-3/8")

# ---- cited-by: the fathers' OT links are provisional until PR #7 is fixed
import tempfile
with tempfile.TemporaryDirectory() as d:
    lf = os.path.join(d, "links.jsonl")
    with open(lf, "w") as f:
        f.write(json.dumps({"unit": "x-lat:1", "links": [
            {"ref": "Ps 22:1", "rule": "note/vulgate", "target": "Ps.22.1"},
            {"ref": "Matt 27:46", "rule": "note/nt", "target": "Matt.27.46"},
            {"ref": "Mark 18:6", "rule": "note/nt", "why": "no such verse"}]}) + "\n")
    cb, cnt = B.cited_by([], shape, None, lf)
    check("cited-by: a father's OT citation is provisional", cb["kjv:Ps.22.1"][0].get("provisional") is True)
    check("cited-by: a father's NT citation is not", "provisional" not in cb["kjv:Matt.27.46"][0])
    check("cited-by: an unresolved note is not a citation", cnt["fathers-notes"] == 2)

# ---- the committed data
if os.path.exists(B.TSK_FILE) and os.path.exists(B.MANIFEST):
    blob = open(B.TSK_FILE, "rb").read()
    man = json.load(open(B.MANIFEST, encoding="utf-8"))
    tsk = man["layers"]["tsk"]
    check("manifest: tsk.jsonl's sha256", hashlib.sha256(blob).hexdigest() == tsk["sha256"])
    rows = [json.loads(x) for x in blob.decode("utf-8").splitlines()]
    check("manifest: row count", len(rows) == tsk["rows"])
    kjv = {k for k in json.load(open(os.path.join(ROOT, "data", "uids", "wordhoard.uids.json"), encoding="utf-8"))["uids"]
           if k.startswith("kjv:")}
    V = T.Verses(shape)
    check("every row's verse is a KJV unit id", all(r["verse"] in kjv for r in rows))
    ok = True
    for r in rows:
        for gg in r["groups"]:
            for rid in gg["refs"]:
                b, c, v, c2, v2 = T.parse_ref_id(rid)
                if f"kjv:{b}.{c}.{v}" not in kjv or f"kjv:{b}.{c2}.{v2}" not in kjv or V.index[(b, c2, v2)] < V.index[(b, c, v)]:
                    ok = False
    check("every reference names KJV unit ids, first verse before last", ok)
    check("rows are in Bible order, one per verse",
          [V.index[T.parse_ref_id(r["verse"])[:3]] for r in rows] == sorted({V.index[T.parse_ref_id(r["verse"])[:3]] for r in rows}))
    check("placed / unsure_digit references are references of their row",
          all(set(r.get("placed", [])) | set(r.get("unsure_digit", [])) <= {x for gg in r["groups"] for x in gg["refs"]} for r in rows))
    check("the Treasury is labelled public domain, redistributable", tsk["rights"]["license"] == "public-domain"
          and tsk["rights"]["redistribute_whole"] is True)
    check("cited-by is labelled not to be redistributed whole (CC BY-SA inputs)",
          man["layers"]["cited_by"]["rights"]["redistribute_whole"] is False)
    check("the scans are pinned by sha256", all(len(f["sha256"]) == 64 for sc in tsk["scans"].values() for f in sc["files"].values()))
    check("the layer covers most of the Bible (>= 25,000 verses)", len(rows) >= 25000)
    check("Gen 1:1 cites Prov 8:22-24 ('beginning')",
          any("kjv:Prov.8.22-24" in gg["refs"] for gg in rows[0]["groups"]) and rows[0]["verse"] == "kjv:Gen.1.1")
    gm = hashlib.sha256(open(G.MODEL, "rb").read()).hexdigest()
    check("manifest: the glyph model's sha256", gm == tsk["glyph_model"]["sha256"])
uids = json.load(open(os.path.join(ROOT, "data", "uids", "wordhoard.uids.json"), encoding="utf-8"))["uids"]
check("nothing minted: no xref or tsk key in the uid registry", not any(k.startswith(("tsk:", "xref")) for k in uids))
check(".gitignore keeps build/ out (cited-by and the one-scan reads)", "build/" in open(os.path.join(ROOT, ".gitignore")).read().split())

print(f"\n{passed} passed, {fails} failed")
sys.exit(1 if fails else 0)
