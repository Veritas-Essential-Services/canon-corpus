#!/usr/bin/env python3
"""press_abbyy.py -- an Internet Archive ABBYY FineReader XML file -> pages of
styled paragraphs, cached.

archive.org keeps, for most scanned books, the full ABBYY output
(<id>_abbyy.gz): every character with its box, confidence and font, and every
run's size, bold and ITALIC flags. The plain OCR text throws all of that away;
the Press needs it: italics are meaning in a Puritan book (the scripture they
quote is set in italic), font size is how a footnote is told from the text,
and the per-word confidence is where the proofing starts.

    load(ident) -> [page, ...]           (cached as data/corpus/press/ia/<id>.pages.json.gz)
    page  = {"i": leaf, "w": width, "h": height, "pars": [par, ...]}
    par   = {"lines": [line, ...], "box": [l, t, r, b]}
    line  = {"runs": [[text, italic, bold, fs], ...], "box": [...], "weak": [[word, conf], ...]}

Page i is the i-th <page> of the file; for archive.org's own scans that is
the image served as /page/n{i}.jpg (checked per volume by press_ocr, which
compares its printed page numbers).
"""
import gzip, json, os, sys
import xml.etree.ElementTree as ET
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import press_build

IA_DIR = os.path.join(press_build.ROOT, "data", "corpus", "press", "ia")
NS = "{http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml}"

def _fetch(ident):
    dest = os.path.join(IA_DIR, f"{ident}_abbyy.gz")
    return press_build.fetch(f"https://archive.org/download/{ident}/{ident}_abbyy.gz", dest)

def parse(path):
    pages = []
    page = par = line = None
    with gzip.open(path, "rb") as f:
        for ev, el in ET.iterparse(f, events=("start", "end")):
            tag = el.tag.replace(NS, "")
            if ev == "start":
                if tag == "page":
                    page = {"i": len(pages), "w": int(el.get("width", 0)), "h": int(el.get("height", 0)), "pars": []}
                elif tag == "block":
                    btype = el.get("blockType")
                    page and page.setdefault("_bt", []).append(btype)
                elif tag == "par":
                    par = {"lines": []}
                elif tag == "line":
                    line = {"runs": [], "box": [int(el.get(k, 0)) for k in "ltrb"], "weak": []}
                continue
            # end events
            if tag == "formatting" and line is not None:
                chars = el.findall(NS + "charParams")
                text = "".join((c.text or "") for c in chars)
                fs = float((el.get("fs") or "0").rstrip(".") or 0)
                line["runs"].append([text, el.get("italic") == "true", el.get("bold") == "true", fs])
                # words that ABBYY itself doubts: lowest char confidence per word
                word, low, sus = "", 255, False
                for c in chars:
                    ch = c.text or ""
                    if c.get("wordStart") == "true" and word.strip():
                        if sus or low < 50:
                            line["weak"].append([word.strip(), low])
                        word, low, sus = "", 255, False
                    word += ch
                    if ch.strip():
                        low = min(low, int(c.get("charConfidence", 255)))
                        sus = sus or c.get("suspicious") == "true"
                if word.strip() and (sus or low < 50):
                    line["weak"].append([word.strip(), low])
                el.clear()
            elif tag == "line" and par is not None:
                if line["runs"]:
                    par["lines"].append(line)
                line = None
                el.clear()
            elif tag == "par" and page is not None:
                if par["lines"]:
                    bs = [l["box"] for l in par["lines"]]
                    par["box"] = [min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)]
                    page["pars"].append(par)
                par = None
            elif tag == "page":
                page.pop("_bt", None)
                pages.append(page)
                page = None
                el.clear()
    return pages

def load(ident):
    cache = os.path.join(IA_DIR, f"{ident}.pages.json.gz")
    if os.path.exists(cache):
        return json.load(gzip.open(cache, "rt", encoding="utf-8"))
    pages = parse(_fetch(ident))
    tmp = cache + ".tmp"
    with gzip.open(tmp, "wt", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, cache)
    return pages

def page_text(page):
    return "\n\n".join("\n".join("".join(r[0] for r in l["runs"]) for l in p["lines"]) for p in page["pars"])

if __name__ == "__main__":
    pages = load(sys.argv[1])
    print(len(pages), "pages")
    for i in sys.argv[2:]:
        print(f"--- page {i}\n" + page_text(pages[int(i)]))
