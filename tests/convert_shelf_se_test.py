#!/usr/bin/env python3
"""Offline checks for the Standard Ebooks path (2026-10-10): fetch_shelf.se_rights
and convert_shelf_se.convert_se, on a made-up fixture (no book text)."""
import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
from fetch_shelf import se_rights, jobs_for
from convert_shelf_se import convert_se

FIXTURE = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html><html><body>
<section id="imprint" epub:type="frontmatter imprint"><p>Based on a
<a href="https://www.fadedpage.com/showbook.php?pid=1">transcription</a> and
<a href="https://archive.org/details/somescan">page scans</a>.</p></section>
<section id="chapter-1" epub:type="bodymatter chapter"><header><hgroup>
<h2 epub:type="z3998:ordinal">I</h2><p epub:type="title">The First</p></hgroup></header>
<p>One <i>two</i>.</p><p>Three &amp; four.</p>
<figure><img src="x.svg"/><figcaption>A map</figcaption></figure>
<blockquote><p>Five.</p><cite>Six</cite></blockquote><ul><li>Seven</li></ul></section>
<section id="chapter-2" epub:type="bodymatter chapter"><hgroup><h2>II</h2></hgroup><p>Eight.</p></section>
<section id="colophon"><p>Not the book.</p></section>
<section id="uncopyright"><p>believed to be in the United States public domain ... CC0 1.0</p></section>
</body></html>"""

passed = failed = 0
def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print("FAIL", name)

r = se_rights(FIXTURE.encode())
check("rights ok", r["se_rights"].startswith("ok"))
check("sources recorded", r["se_sources"] == ["https://archive.org/details/somescan",
                                              "https://www.fadedpage.com/showbook.php?pid=1"])
check("rights refused without CC0", se_rights(FIXTURE.replace("CC0 1.0", "")).get("se_rights").startswith("CHECK"))
check("rights refused on an error page", se_rights(b"<html>Not found</html>")["se_rights"].startswith("CHECK"))
check("job url", jobs_for({"standard_ebooks": {"s": ["a-b/c-d", "T"]}}, "x")
      == [("s", "T", "https://standardebooks.org/ebooks/a-b/c-d/text/single-page", ".xhtml", "se")])

with tempfile.NamedTemporaryFile("w", suffix=".xhtml", delete=False, encoding="utf-8") as f:
    f.write(FIXTURE)
book = convert_se(f.name, "s", "T", "A", {"jurisdiction": {"us": "pd"}})
os.unlink(f.name)
ids = [u["id"] for u in book["units"]]
check("ids", ids == ["s:1.1", "s:1.2", "s:1.3", "s:1.4", "s:1.5", "s:2.1"])
check("inline markup and entities", book["units"][0]["text"] == "One two." and book["units"][1]["text"] == "Three & four.")
check("figure skipped", all("map" not in u["text"] for u in book["units"]))
check("cite outside p kept", book["units"][3]["text"] == "Six")
check("front/back matter skipped", all("book" not in u["text"] for u in book["units"]))
check("ref carries heading", book["units"][0]["ref"] == "Chapter I. The First, par. 1")
check("ref without title", book["units"][-1]["ref"] == "Chapter II, par. 1")
check("rights block", book["rights"] == {"jurisdiction": {"us": "pd"}})
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
