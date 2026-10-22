# prov: 2026-10-20 claude-opus-5-5 drafted
"""Offline checks for the small-capitals reread and the abbreviation rule (no scans needed)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from unscanner import smallcaps as S
from unscanner.learned import abbrev_rule, ll_rule, lig_garble_rule

ok = bad = 0
def check(name, cond):
    global ok, bad
    print(("PASS " if cond else "FAIL ") + name); ok += bool(cond); bad += (not cond)

check("jumbled tesseract reading is small caps", S.looks_smallcaps({"toronto.tess": "KateErFELTo", "toronto.djvu": "Katekfelto"}))
check("all-caps tesseract reading is small caps", S.looks_smallcaps({"cornell.tess": "PYROCLES"}))
check("the Archive's ll-as-U is not small caps", not S.looks_smallcaps({"toronto.tess": "Rolla", "toronto.djvu": "RoUa"}))
check("a plain word is not small caps", not S.looks_smallcaps({"toronto.tess": "doctor", "cornell.tess": "doctor"}))
check("a dropped letter is no objection", S._drops("CAGLITRO", "CAGLIOSTRO"))
check("a changed letter is an objection", not S._drops("CAGLIOSTBO", "CAGLIOSTRO"))
check("etc. beats ctc.", abbrev_rule(["ctc.", "etc."]) == "etc.")
check("etc., keeps its comma", abbrev_rule(["ete.,", "etc.,"]) == "etc.,")
check("i.e. beats ze.", abbrev_rule(["ze.", "i.e."]) == "i.e.")
check("no abbreviation, no pick", abbrev_rule(["Rome", "Romc"]) is None)
check("U inside a lowercase word is ll", ll_rule(["Rolla", "RoUa "]) == "Rolla")
check("...or li", ll_rule(["LilUa-Bianca,", "Lillia-Bianca,"]) == "Lillia-Bianca,")
check("...at the word's end", ll_rule(["ball,", "baU,"]) == "ball,")
check("quote marks are not the question", ll_rule(['MotaUeb,"', "Motalleb,\u201d"]) == "Motalleb,\u201d")
check("a capital U starting a word is left alone", ll_rule(["Use", "Uae"]) is None)
check("AngUae / AngHse / Angliz -> Angliæ", lig_garble_rule({"Angliew,": ["toronto.tess"], "AngUae,": ["toronto.djvu"], "Angliz,": ["cornell.tess"], "AngHse,": ["cornell.djvu"]}) == "Angliæ,")
check("house in both scans stays house", lig_garble_rule({"house": ["toronto.tess", "cornell.tess"]}) is None)
check("one scan alone is not enough", lig_garble_rule({"AngUae,": ["toronto.djvu"], "Angle,": ["cornell.tess"]}) is None)
check("a headword before its bracket is small caps", S.heads_entry({"base": "Lone", "line": "Lone (St. John), born at Neweastle, began"}))
check("a word mid-line is not a headword", not S.heads_entry({"base": "doctor", "line": "the influenza doctor (see above)"}))
check("Cormae / Cormac is not a ligature", lig_garble_rule({"Cormae": ["toronto.tess", "toronto.djvu"], "Cormac": ["cornell.tess", "cornell.djvu"]}) is None)
print(f"{ok} passed, {bad} failed"); sys.exit(1 if bad else 0)
