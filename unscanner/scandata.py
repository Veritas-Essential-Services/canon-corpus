"""The Archive's own page record (`<id>_scandata.xml`): a third witness, to the book's structure.

When the Internet Archive scanned a book, its operator marked each leaf: Cover, Title, Contents,
Chapter, Normal; and keyed in the printed page number where there is one. The PDF holds exactly the
leaves marked `addToAccessFormats`, in order, so PDF page n is the n-th of those. This module uses that
record two ways and no others:

  - the BINDING: covers, and every leaf before the title page (end-papers, a library's bookplate),
    is the copy's, not the book's. Those pages stay in the faithful page view (they are in the scan)
    but leave the reading editions and the units;
  - a CHECK: the Archive's page numbers and chapter marks are compared with what the layout read, and
    the agreement is reported. Nothing the layout read is overwritten by it.
"""
import os
import urllib.request
import xml.etree.ElementTree as ET

URL = "https://archive.org/download/{id}/{id}_scandata.xml"


def fetch(ident, dest):
    if not os.path.exists(dest):
        try:
            with urllib.request.urlopen(URL.format(id=ident), timeout=120) as r:
                data = r.read()
        except Exception:
            return None
        with open(dest + ".part", "wb") as f:
            f.write(data)
        os.replace(dest + ".part", dest)
    return dest


def pages(path):
    """-> {pdf page n: {"type", "number"}} for the leaves the PDF holds."""
    root = ET.parse(path).getroot()
    out, n = {}, 0
    for leaf in root.iter("page"):
        if (leaf.findtext("addToAccessFormats") or "true").strip() != "true":
            continue
        n += 1
        out[n] = {"type": (leaf.findtext("pageType") or "").strip(), "number": (leaf.findtext("pageNumber") or "").strip() or None}
    return out


def binding(sd):
    """PDF pages that are the copy's binding: covers, and everything before the title page."""
    title = min((n for n, v in sd.items() if v["type"] == "Title"), default=None)
    out = {n for n, v in sd.items() if v["type"] in ("Cover", "Color Card", "White Card")}
    if title:
        out |= {n for n in sd if n < title}
    return out


def check(sd, pages_, divisions):
    """Agreement of our page labels and chapter starts with the Archive's record."""
    both = [(p.get("label"), sd[p["n"]]["number"]) for p in pages_ if p["n"] in sd and p.get("label") and sd[p["n"]]["number"]]
    agree = sum(1 for a, b in both if a == b)
    marked = {n for n, v in sd.items() if v["type"] == "Chapter"}
    ours = set()
    for d in divisions:
        for s in d["items"]:
            if s.get("pages"):
                ours.add(s["pages"][0])
                break
    near = sum(1 for n in marked if any(abs(n - o) <= 1 for o in ours))
    return {"labels_compared": len(both), "labels_agree": agree,
            "archive_chapter_marks": len(marked), "our_chapters": len(divisions), "marks_matched": near}
