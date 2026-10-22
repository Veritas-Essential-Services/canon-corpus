#!/usr/bin/env python3
"""Offline checks for pipeline/build_dictionary_links.py: fixtures inline, no corpus needed."""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pipeline"))
import build_dictionary_links as dl  # noqa: E402

PASS, FAIL = 0, []


def check(label, cond):
    global PASS
    if cond:
        PASS += 1; print("ok  ", label)
    else:
        FAIL.append(label); print("FAIL", label)


def u(i, text="", **lex):
    return {"id": i, "text": text, "lex": lex, "links": lex.pop("links", [])}


books = {
    "smith-dgrbm": {"units": [
        u("smith-dgrbm:ajax-bio-1", lemma="Ajax", links=[
            {"kind": "classical", "cite": "Hom. Il. 2.557"},
            {"kind": "classical", "cite": "Apollod. 3.10.8"},
            {"kind": "classical", "cite": "Just. 7.1"},
            {"kind": "classical", "cite": "Apollod. fr. a"}]),
        u("smith-dgrbm:ajax-bio-2", lemma="Ajax")]},
    "brewer-character-sketches": {"units": [
        u("brewer-character-sketches:ajax", "AJAX, a Greek. (_Gen._ i. 1-3) 2 _Sam._ xvii. "
          "Shakespeare, _Troilus and Cressida_ (1602), act ii. sc. 3. King John, iii. 1. "
          "Gen. lx. 2; Sam. iv. 1; Act i. 5.", headword="AJAX"),
        u("brewer-character-sketches:app1:x", "", headword="Ajax", appendix="app1")]},
    "brewer": {"units": [
        u("brewer:ajax", "Prov. xxx. 8. Shakespeare: 1 Henry IV., iii. 1. Shakespeare: Hamlet, ix. 1",
          headword="Ajax", links=[{"kind": "scripture", "ref": "Prov. xxx. 8", "target": "kjv:Prov.30.8",
                                   "resolved": True}]),
        u("brewer:air", "Air", headword="Air")]},
    "kjv": {"units": [u(f"kjv:{b}") for b in ("Gen.1.1", "Gen.1.3", "Prov.30.8", "2Sam.17.1", "John.3.1")]},
    "shakespeare": {"units": [u(f"shakespeare:{s}.1") for s in
                              ("troilus-and-cressida.2.3", "henry-iv-1.3.1", "hamlet.1.1", "king-john.3.1")]},
}

names = dl.build_names(books)
check("names: a headword in all three dictionaries is one row; an appendix item is not a headword",
      len(names) == 1 and names[0]["key"] == "ajax" and len(names[0]["members"]) == 3
      and names[0]["members"]["brewer-character-sketches"] == ["brewer-character-sketches:ajax"])
check("names: two Smith homonyms make the row not one-each", names[0]["one_each"] is False)

scr, miss = dl.build_scripture(books)
t = {r["cite"]: r for r in scr}
check("scripture: italic abbreviation, roman chapter, verse range",
      t["_Gen._ i. 1-3"]["target"] == "kjv:Gen.1.1" and t["_Gen._ i. 1-3"]["to"] == "kjv:Gen.1.3")
check("scripture: a numbered book at chapter level", t["2 _Sam._ xvii."]["target"] == "kjv:2Sam.17"
      and t["2 _Sam._ xvii."]["level"] == "chapter")
check("scripture: Phrase and Fable's own parsed links are carried over, not re-parsed",
      {"from": "brewer:ajax", "cite": "Prov. xxx. 8", "target": "kjv:Prov.30.8", "level": "verse",
       "how": "in-book"} in scr)
check("scripture: a verse the KJV lacks is dropped and counted; `Sam.` without its number is not guessed",
      "Gen. lx. 2" not in t and miss == {"no such verse in the KJV": 1, "no book number": 1})
check("scripture: `King John, iii.` and a play's `Act i. 5` are not the Bible",
      not any(r["target"].startswith("kjv:John") or r["target"].startswith("kjv:Acts") for r in scr))

sh, miss = dl.build_shakespeare(books)
check("shakespeare: Character Sketches' `Title (1602), act ii. sc. 3` and DPF's `1 Henry IV., iii. 1`",
      {r["target"] for r in sh} == {"shakespeare:troilus-and-cressida.2.3", "shakespeare:henry-iv-1.3.1"})
check("shakespeare: a scene the text lacks is dropped and counted", miss == {"no such scene": 1})

cl, miss = dl.build_classical(books)
check("classical: a known work's passage becomes a CTS URN",
      {"from": "smith-dgrbm:ajax-bio-1", "cite": "Apollod. 3.10.8",
       "urn": "urn:cts:greekLit:tlg0548.tlg001:3.10.8"} in cl)
check("classical: an unknown abbreviation and a non-numeric passage stay unresolved, counted",
      miss["unresolved"] >= 2 and "Just." in miss["top_unresolved_abbreviations"]
      and not any("fr." in r["cite"] for r in cl))

pm, read = dl._page_map([["x"], ["1 HEAD"], ["PLATE"], ["2 HEAD"], ["nothing"], ["HEAD 4"], ["5 x"]])
check("pages: folios chain through a plate; a leaf between read folios is counted only when they agree",
      pm[1] == 1 and pm[3] == 2 and pm[4] == 3 and pm[5] == 4 and 2 not in pm and 4 not in read)

import json as _json, tempfile as _tf
_pb = {"brewer-character-sketches": {"units": [
    u("brewer-character-sketches:circe", headword="Circe"),
    u("brewer-character-sketches:deans-douce-davie", headword="Deans", qualifier="Douce Davie"),
    u("brewer-character-sketches:moses-rod", headword="Moses' Rod"),
    u("brewer-character-sketches:far-away", headword="Faraway")]}}
_pp = [{"id": "brewer-character-sketches:circe", "volume": 2, "leaf": 70},
       {"id": "brewer-character-sketches:deans-douce-davie", "volume": 2, "leaf": 194},
       {"id": "brewer-character-sketches:moses-rod", "volume": 2, "leaf": 300},
       {"id": "brewer-character-sketches:far-away", "volume": 2, "leaf": 400}]
with _tf.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as _f:
    for c, leaf in (("Circe and her Swine", 72), ("Ejffie Deans in the Prison", 196),
                    ("Preparing Moses for the Fair", 302), ("Faraway", 300)):
        _f.write(_json.dumps({"citation": f"brewer-sketches:v2.leaf{leaf}", "uid": "wh-X", "volume": 2,
                              "leaf": leaf, "caption_ocr": c}) + "\n")
_saved, dl.PLATES = dl.PLATES, _f.name
_pr = {r["plate"]: r for r in dl.build_plates(_pb, _pp)}
dl.PLATES = _saved; os.unlink(_f.name)
check("plates: a caption naming a nearby headword links the plate to that entry",
      _pr["brewer-sketches:v2.leaf72"]["target"] == "brewer-character-sketches:circe")
check("plates: a headword whose qualifier is not in the caption stays a candidate",
      _pr["brewer-sketches:v2.leaf196"]["resolved"] is False)
check("plates: every word of the headword must be in the caption; distance is capped",
      "brewer-sketches:v2.leaf302" not in _pr and "brewer-sketches:v2.leaf300" not in _pr)

_nb = {"smith-dgrbm": {"units": [u("smith-dgrbm:admetus-bio-1", "Admetus, king of Pherae in Thessaly, "
                                   "husband of Alcestis, served by Apollo.", lemma="Admetus")]},
       "brewer-character-sketches": {"units": [u("brewer-character-sketches:admetus",
                                     "ADMETUS, whom Apollo served; Alcestis died for him.", headword="ADMETUS")]},
       "brewer": {"units": [u("brewer:admetus", "Admetus. A king. See the Greek tale.", headword="Admetus")]}}
_nr = dl.build_names(_nb)[0]
check("names: a pair naming two of the same people is corroborated, with the names; one that names none is not",
      _nr["corroborated"] == [{"a": "smith-dgrbm:admetus-bio-1", "b": "brewer-character-sketches:admetus",
                               "shared": ["Alcestis", "Apollo"], "shared_n": 2}])

print(f"\n{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
