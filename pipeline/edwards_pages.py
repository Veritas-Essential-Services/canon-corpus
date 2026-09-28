#!/usr/bin/env python3
"""Page-address every Internet Archive Edwards volume by its OWN printed pages.

For each IA item in edwards_shelf.json this reads two files IA publishes
beside every scan:
  <id>_djvu.xml          the OCR text, one <OBJECT> per scanned leaf
  <id>_page_numbers.json IA's own leaf -> printed page number table, with a
                          confidence for each page it read off the scan
and writes data/corpus/edwards-pages/<slug>.jsonl, one line per leaf:
  {"slug", "leaf", "page", "page_conf", "text"}
so any passage can be cited as e.g. "Dwight 2:95" -- the first half of
putting Yale numbering on the public-domain works (the second half aligns
these pages to the Yale text; see EDWARDS-YALE-ADDRESSING.md).

page is "" where IA could not read a number (plates, blanks, front matter);
page_conf is IA's confidence (None where it inferred the number from its
neighbours). Nothing is guessed here. Resumable: finished volumes are kept.
"""
import gzip, json, os, re, sys, time, urllib.request, xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "corpus", "edwards-pages")
UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}
SHELF = json.load(open(os.path.join(HERE, "edwards_shelf.json"), encoding="utf-8"))

def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
                return r.read()
        except Exception as e:
            err = e; time.sleep(2 ** i)
    raise RuntimeError(f"{url}: {err}")

def leaf_texts(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = []
    for obj in root.iter("OBJECT"):
        usemap = obj.get("usemap", "")
        m = re.search(r"_(\d{4})\.djvu", usemap)
        leaf = int(m.group(1)) if m else None
        lines = []
        for line in obj.iter("LINE"):
            words = [w.text or "" for w in line.iter("WORD")]
            if words:
                lines.append(" ".join(words))
        out.append((leaf, "\n".join(lines)))
    return out

def main():
    os.makedirs(OUT, exist_ok=True)
    report = {}
    for slug, (ident, title) in SHELF["internet_archive"].items():
        dest = os.path.join(OUT, slug + ".jsonl")
        if os.path.exists(dest):
            report[slug] = "kept"; continue
        try:
            try:
                pn = json.loads(get(f"https://archive.org/download/{ident}/{ident}_page_numbers.json", tries=2))
            except RuntimeError:
                pn = {"pages": [], "confidence": "no IA page table for this scan -- leaves only"}
            pages = {p["leafNum"]: p for p in pn.get("pages", [])}
            leaves = leaf_texts(get(f"https://archive.org/download/{ident}/{ident}_djvu.xml"))
        except Exception as e:
            report[slug] = f"FAILED {e}"; print(slug, report[slug], flush=True); continue
        n_num = 0
        with open(dest + ".tmp", "w", encoding="utf-8") as f:
            for i, (leaf, text) in enumerate(leaves):
                # djvu.xml leaves are numbered from 0 in their image names; IA's
                # page table counts leaves from the same scan sequence.
                key = leaf if leaf in pages else i
                p = pages.get(key, {})
                if p.get("pageNumber"): n_num += 1
                f.write(json.dumps({"slug": slug, "leaf": key, "page": p.get("pageNumber", ""),
                                    "page_conf": p.get("confidence"), "text": text}, ensure_ascii=False) + "\n")
        os.replace(dest + ".tmp", dest)
        report[slug] = f"{len(leaves)} leaves, {n_num} with a printed page number (IA volume confidence {pn.get('confidence')})"
        print(slug, report[slug], flush=True)
    json.dump(report, open(os.path.join(OUT, "_report.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
