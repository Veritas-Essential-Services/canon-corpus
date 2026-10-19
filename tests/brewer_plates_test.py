#!/usr/bin/env python3
# prov: 2026-10-19 claude-opus-5-5 drafted
# fable_review: pending
"""Offline checks for data/art/brewer-sketches/ (Brewer's Character Sketches plates).
No network, no scans needed.   python3 tests/brewer_plates_test.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import brewer_plates as B  # noqa: E402
import wh_uid as U  # noqa: E402

PASS, FAIL = 0, []


def check(label, cond):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
    print(("ok   " if cond else "FAIL ") + label)


rows = [json.loads(l) for l in open(B.OUT, encoding="utf-8")]
reg = json.load(open(B.UIDS, encoding="utf-8"))["uids"]

check("283 plates across all eight volumes", len(rows) == 283 and {r["volume"] for r in rows} == set(range(1, 9)))
check("every uid is well formed and unique", all(U.is_uid(r["uid"]) for r in rows)
      and len({r["uid"] for r in rows}) == len(rows))
check("every citation is volume + scan leaf, and unique",
      all(r["citation"] == f"brewer-sketches:v{r['volume']}.leaf{r['leaf']}" for r in rows)
      and len({r["citation"] for r in rows}) == len(rows))
check("the registry holds each citation -> uid exactly as the row says",
      all(reg.get(r["citation"]) == r["uid"] for r in rows))
check("every plate links to an archive.org IIIF image service and page",
      all(r["iiif_image"].startswith("https://iiif.archive.org/image/iiif/3/") and
          r["page"].startswith("https://archive.org/details/") for r in rows))
check("every plate is US public domain with its basis stated",
      all(r["rights"]["pd_us"] is True and "1892" in r["rights"]["basis"] for r in rows))
check("rows are sorted by volume then leaf", rows == sorted(rows, key=lambda r: (r["volume"], r["leaf"])))
check("the four strays the contrast rule removed stay out",
      not {(2, 163), (3, 23), (5, 4), (7, 81)} & {(r["volume"], r["leaf"]) for r in rows})
check("vol 6 is exact: 28 plates, only Pygmalion (not in the scan) listed-not-found",
      sum(r["volume"] == 6 for r in rows) == 28 and
      [m["title"] for m in map(json.loads, open(B.MISSING, encoding="utf-8")) if m["volume"] == 6]
      == ["PYGMALION AND GALATEA"])

# the parsers, on lines as this OCR prints them
check("credit line: artist and engraver split", B.split_credit("Gustave Dore, Artist Pannemaker, Engraver")
      == ("Gustave Dore", "Pannemaker"))
check("credit line: misread 'ylrtist' still read as the artist credit",
      B.split_credit("H. Kauihack, ylrtist")[0] == "H. Kauihack")
t = B.tissue(["Charney examining Picciola.", "Barrios, Artist Ch. Geoffrey, Engraver",
              "rHE Count Charney, in prison for political offenses, devotes himself"])
check("tissue guard: caption above the credit line", t and t["caption_ocr"] == "Charney examining Picciola."
      and t["artist_ocr"] == "Barrios" and t["engraver_ocr"] == "Ch. Geoffrey")
check("a List of Illustrations page is never taken for a tissue",
      B.tissue(["LIST OF ILLUSTRATIONS.", "VOLUME VI.", "Illustration Artist To face"]) is None)
check("plate title: the plate leaf's capitals; the copyright page refused",
      B.plate_title(["PUSS-IN-BOOTS."]) == "PUSS-IN-BOOTS"
      and B.plate_title(["Copyright by", "Selmar Hess.", "PHOTOGRAVURES PRINTED ON THE", "HESS PRESS"]) is None)
L = B.parse_list([["LIST OF ILLUSTRATIONS.", "VOLUME VI.", "Illustration Artist To face", "page",
                   "PIED PIPER OF HAMELIN (THE) H. Kaulbach Frontispiece",
                   "REINIKE FOX BEFORE KING LION - • - - W. von Kaulbach 284",
                   "ROB ROY ^PARTING RASHLEIGH AND FRANCIS", "OSBALDISTONE J. B. McDonald 300"]])
check("list: frontispiece, dot leaders, and a title wrapped onto two lines",
      [(e["faces"]) for e in L] == ["frontispiece", 284, 300]
      and L[1]["artist"] == "W. von Kaulbach" and "OSBALDISTONE" in L[2]["title"] and "FRANCIS" in L[2]["title"])

print(f"\n{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
