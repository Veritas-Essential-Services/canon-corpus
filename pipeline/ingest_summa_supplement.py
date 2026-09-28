#!/usr/bin/env python3
"""Summa Theologica — the SUPPLEMENT to the Third Part (and its Appendix).

Aquinas died in 1274 partway through the treatise on Penance (Part III ends
at Q. 90). The Supplement, compiled from his commentary on the Sentences,
finishes the plan. Project Gutenberg carries Parts I, I-II, II-II and III
(adler_shelf.json: aquinas-summa, -1-2, -2-2, -3) but not the Supplement,
so this one comes from CCEL's complete Summa, cut down to the SUPPLEMENT and
Appendix divisions and run through the same ThML converter as every CCEL book.

    python3 pipeline/ingest_summa_supplement.py
Writes data/corpus/ccel/aquinas-summa-supp.xml and data/books/aquinas-summa-supp.json.
"""
import json, os, re, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import structure_texts as st

URL = "https://ccel.org/ccel/a/aquinas/summa.xml"
SRC = os.path.join(HERE, "..", "data", "corpus", "ccel", "aquinas-summa-full.xml")
CUT = os.path.join(HERE, "..", "data", "corpus", "ccel", "aquinas-summa-supp.xml")
OUT = os.path.join(HERE, "..", "data", "books", "aquinas-summa-supp.json")

if not os.path.exists(SRC):
    os.makedirs(os.path.dirname(SRC), exist_ok=True)
    req = urllib.request.Request(URL, headers={"User-Agent": "Canon-Corpus/0.1 (personal library research)"})
    open(SRC, "wb").write(urllib.request.urlopen(req, timeout=300).read())
s = open(SRC, encoding="utf-8").read()
starts = [m.start() for m in re.finditer(r"<div1[\s>]", s)]
titles = [re.search(r'title="([^"]*)"', s[p:p + 400]).group(1) for p in starts]
end = s.find("</ThML.body>")
bounds = starts + [end]
keep = [i for i, t in enumerate(titles) if t.startswith("SUPPLEMENT") or t == "Appendix"]
assert keep, "no SUPPLEMENT division found -- CCEL changed the file"
cut = s[:starts[0]] + "".join(s[bounds[i]:bounds[i + 1]] for i in keep) + s[end:]
cut = re.sub(r"<DC.Title[^>]*>.*?</DC.Title>",
             "<DC.Title>Summa Theologica, Supplement to the Third Part</DC.Title>", cut, count=1, flags=re.S)
open(CUT, "w", encoding="utf-8").write(cut)
book = st.convert_thml(CUT, "aquinas-summa-supp")
with open(OUT + ".tmp", "w", encoding="utf-8") as f:
    json.dump(book, f, ensure_ascii=False)
os.replace(OUT + ".tmp", OUT)
print(f"aquinas-summa-supp: {len(book['units'])} units — {book['title']}")
