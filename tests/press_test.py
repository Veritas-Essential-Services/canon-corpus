#!/usr/bin/env python3
"""Offline checks for the Press (pipeline/press_*.py). No network, no corpus.

    python3 tests/press_test.py
"""
import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import press_scripture as S
import press_thml, press_render, press_build, press_text

fails = 0
def check(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(("ok  " if ok else "FAIL"), name, "" if ok else f"\n     got  {got!r}\n     want {want!r}")

# --- scripture: printed references -> KJV ids, never clamped
check("roman chapter", S.parse("Rom. viii. 13"), ["Rom.8.13"])
check("verse list", S.parse("Ps. cxix. 5, 6"), ["Ps.119.5", "Ps.119.6"])
check("numbered book", S.parse("1 John iii. 2"), ["1John.3.2"])
check("roman book number", S.parse("I Cor. xv. 3"), ["1Cor.15.3"])
check("range", S.parse("Gal. v. 17–19"), ["Gal.5.17", "Gal.5.18", "Gal.5.19"])
check("arabic", S.parse("Rom. 8:13"), ["Rom.8.13"])
check("chapter only", S.parse("Heb. xii."), ["Heb.12"])
check("second chapter in one ref", S.parse("Isa. liii. 5; lv. 1"), ["Isa.53.5", "Isa.55.1"])
check("no such verse is refused", S.parse("Ps. cxx. 9"), [])
check("printers' j for i", S.parse("Gen. xiij. 2"), ["Gen.13.2"])
check("osisRef range", S.check_osis("Rom.8.13-Rom.8.15")[0], ["Rom.8.13", "Rom.8.14", "Rom.8.15"])
check("osisRef bad verse", S.check_osis("Ps.120.9")[0], [])
ctx = {}
S.parse_context("Rom. viii. 13", ctx)
check("context: bare verse", S.parse_context("verse 9", ctx)[:3:2], (["Rom.8.9"], True))
check("context: chap.", S.parse_context("chap. xii. 1", ctx)[0], ["Rom.12.1"])
check("context: 'Book, chap.'", S.parse_context("Hebrews, chap. iii. 12", {})[0], ["Heb.3.12"])
check("versification total", sum(sum(v) for v in S.VERSES.values()), 31102)

# --- markdown safety: a paragraph must never turn into a list or heading
check("guard number", press_thml.guard_start("1. First, it is"), "1\\. First, it is")
check("guard paren", press_thml.guard_start("(2.) Secondly"), "(2.\\) Secondly")
check("guard roman", press_thml.guard_start("IV. The fourth"), "IV\\. The fourth")
check("guard hash", press_thml.guard_start("# not a heading"), "\\# not a heading")
check("escape", press_thml.esc("a*b_c[d]"), "a\\*b\\_c\\[d\\]")
check("emphasis keeps spaces outside", press_thml.wrap(" word ", "*", "*"), " *word* ")

# --- ThML -> Press document -> book
THML = """<ThML><ThML.head><DC><DC.Title>Test</DC.Title></DC></ThML.head>
<ThML.body>
<div1 type="Work" title="A Treatise" id="i">
<div2 type="Titlepage" title="Title page." id="i.i"><p class="h1"><span style="text-transform:uppercase">a treatise</span></p></div2>
<div2 type="Chapter" title="Chapter I." id="i.ii">
<pb n="7" id="x"/>
<h1>Chapter I.</h1>
<argument>The text opened.</argument>
<p class="Body"><span style="font-variant:small-caps">The</span> words, <scripRef passage="Rom. viii. 13" osisRef="Bible:Rom.8.13">Rom. viii. 13</scripRef>, and <scripRef passage="verse 9">verse 9</scripRef> are <i>plain</i>.<note place="foot" n="1"><p>A note.</p></note></p>
<p class="Body">1. First, a numbered head.</p>
</div2>
<div1 title="Indexes" id="ii"><p>dropped</p></div1>
</div1></ThML.body></ThML>"""
with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False, encoding="utf-8") as f:
    f.write(THML)
doc = press_thml.convert(f.name, "t")
kinds = [b["k"] for b in doc["blocks"]]
check("title page kept as its own block", kinds[:3], ["titlepage_start", "tp", "titlepage_end"])
check("uppercase transform applied", doc["blocks"][1]["md"], "A TREATISE")
check("osisRef + context refs", [r["ids"] for r in doc["refs"]], [["Rom.8.13"], ["Rom.8.9"]])
check("context ref flagged inferred", doc["refs"][1].get("inferred"), True)
check("footnote captured", doc["notes"], {"n1": "A note."})
check("indexes dropped", any("dropped" in (b.get("md") or "") for b in doc["blocks"]), False)
md = press_render.render(doc, {"slug": "t", "title": "A Treatise", "author": "X", "note_on_text": ["n."]})
check("heading loses its full stop", "# Chapter I {#t-s-i-ii .unnumbered}" in md, True)
check("page anchor rides on the next paragraph", "[]{#t-p7 .pb n=\"7\"}" in md, True)
check("argument block", "::: {.argument}\nThe text opened.\n:::" in md, True)
check("index of scripture", "## Romans {.unnumbered .unlisted}" in md and "8:13" in md and "8:9" in md, True)
check("numbered paragraph escaped", "1\\. First, a numbered head." in md, True)
check("YAML booleans", "toc: true" in md, True)
os.unlink(f.name)

# --- rules: a correction must match exactly as often as it says
d2 = {"blocks": [{"k": "para", "md": "the evidence of it"}], "notes": {}}
press_build.apply_rules(d2, {"corrections": [{"find": "the evidence", "replace": "the evidences"}]})
check("rule applied", d2["blocks"][0]["md"], "the evidences of it")
try:
    press_build.apply_rules(d2, {"corrections": [{"find": "absent words", "replace": "x"}]})
    check("rule that no longer matches stops the build", False, True)
except RuntimeError:
    check("rule that no longer matches stops the build", True, True)

# --- old and British words are not proofing work
W = {"cometh", "come", "favor", "endeavor", "honor"}
check("eth verb", press_build.known("cometh", W), True)
check("our spelling", press_build.known("favour", W), True)
check("unknown stays unknown", press_build.known("aflaiction", W), False)

# --- plain-text references (Gutenberg / OCR)
class C:  # minimal converter context
    section, ctx, refs, problems = "s1", {}, [], []
out = press_text.tag_refs("as in (Psa 66:17,18) and Rom. viii. 13.", C)
check("text refs tagged", [r["ids"] for r in C.refs], [["Ps.66.17", "Ps.66.18"], ["Rom.8.13"]])

print("\n%d failure(s)" % fails)
sys.exit(1 if fails else 0)
