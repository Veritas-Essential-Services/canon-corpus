#!/usr/bin/env python3
"""Offline checks for pipeline/build_sks.py (the SKS TEI reader), on a fixture."""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
import build_sks as S  # noqa: E402

FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt>
<title level="s">Søren Kierkegaards Skrifter</title><title>Prøve</title><title type="short">PR</title>
</titleStmt><seriesStmt><biblScope unit="volume">4</biblScope></seriesStmt></fileDesc></teiHeader>
<text><body><div type="chapter"><head type="topText" n="x"/>
<p rend="decoration"><pb edRef="#SKS" n="7"/><figure type="blank"/></p>
<head>Forord</head>
<p><pb edRef="#SV1" n="3"/>En <choice><orig>dialeltisk</orig><reg>dialektisk</reg></choice> Tvivl
<choice><abbr>o. s. v.</abbr><expan>og saa videre</expan></choice>
<app><lem>Lem</lem><rdg>Rdg</rdg></app> <del>bort</del><add>til</add>
fortsat <pb edRef="#SKS" n="8"/>paa næste Side<ptr type="author" target="#pr.1"/>.</p>
<p>Anden paa side otte.</p>
<lg><l>Første Linie</l><l>Anden Linie</l></lg>
</div>
<note type="author" place="bottom" xml:id="pr.1"><p>Forfatterens <pb edRef="#SKS" n="99"/>Note.</p></note>
</body></text></TEI>
"""

fails = 0


def check(name, ok):
    global fails
    print(("ok   " if ok else "FAIL ") + name)
    fails += not ok


with tempfile.TemporaryDirectory() as d:
    S.CORPUS = d
    with open(os.path.join(d, "pr.txt.xml"), "w", encoding="utf-8") as f:
        f.write(FIXTURE)
    pins = {"repo": "kb-dk/SKS_tei", "commit": "c0ffee", "sha256": {"pr": "x"}}
    book = S.convert("pr", pins)
    u = book["units"]
    check("three units (decoration paragraph skipped)", len(u) == 3)
    check("id is the SKS page the paragraph begins on", u[0]["id"] == "sks-pr:7.1")
    check("ref names volume, page, work", u[0]["ref"] == "SKS 4, 7 (PR)")
    check("reg over the misprint; abbr over the expansion; lem over rdg; del dropped, add kept",
          u[0]["text"] == "En dialektisk Tvivl o. s. v. Lem til fortsat paa næste Side.")
    check("page turn inside the paragraph recorded", u[0]["pages"].get("sks_end") == "8")
    check("SV1 page carried", u[0]["pages"].get("sv1") == "3")
    check("author's note attached by its ptr, not in text",
          u[0].get("notes") == [{"id": "pr.1", "text": "Forfatterens Note."}])
    check("a note's page break does not move the text's pages", u[1]["id"] == "sks-pr:8.1")
    check("heading carried", u[0].get("head") == ["Forord"])
    check("verse lines joined with ' / '", u[2]["text"] == "Første Linie / Anden Linie")
    st = book["scheme"]["stats"]
    check("stats counted", st["misprints_emended"] == 1 and st["variants_dropped"] == 1
          and st["deletions_dropped"] == 1 and st["notes"] == 1)
    check("rights: CC0 and redistributable", book["rights"]["license"].startswith("CC0")
          and book["rights"]["redistribute_whole"] is True)

# the committed pins cover SKS 1-16 and every work has a sha256
pins = json.load(open(S.PINS, encoding="utf-8"))
check("pins: 87 works, each with a sha256",
      len(pins["works"]) == 87 and all(len(pins["sha256"].get(c, "")) == 64 for c in pins["works"]))

print(f"\n{'ALL PASSED' if not fails else str(fails) + ' FAILED'}")
sys.exit(1 if fails else 0)
