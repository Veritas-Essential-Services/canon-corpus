#!/usr/bin/env python3
"""Fetch the Latin of Aquinas from the Corpus Thomisticum (Enrique Alarcon,
University of Navarre), page by page, into data/corpus/corpus-thomisticum/.

    python3 pipeline/fetch_corpus_thomisticum.py            # everything listed in WORKS
    python3 pipeline/fetch_corpus_thomisticum.py sth        # one work (prefix)

Resumable: a page already on disk is kept. Polite: one request a second.

RIGHTS (read before republishing). The text is the Leonine edition (Summa
Theologiae, Rome 1888-1906; Summa contra Gentiles 1918-30), public domain in
the US. The site's pages say "(c) Fundacion Tomas de Aquino quoad hanc
editionem. Iura omnia asservantur": the foundation claims rights in its
electronic edition. So, like the STEPBible lexicons, these files are fetched
into the gitignored corpus and used locally; nothing built from them is
committed until Adam rules (docs/AQUINAS.md, "The Latin question").
"""
import os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "corpus", "corpus-thomisticum")
BASE = "https://www.corpusthomisticum.org/"
UA = {"User-Agent": "Canon-Corpus/0.1 (personal library research)"}
INDEX = BASE + "iopera.html"
# work prefix -> what it is; the page list is read from the site's own index
WORKS = {
    "sth": "Summa Theologiae (Leonine, 1888-1906)",
    "scg": "Summa contra Gentiles (Leonine, 1918-1930)",
    "cmt": "Catena aurea in Matthaeum",
    "cmc": "Catena aurea in Marcum",
    "clc": "Catena aurea in Lucam",
    "cjo": "Catena aurea in Ioannem",
}

def get(url):
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read()
        except Exception as e:
            err = e
            time.sleep(2 ** i)
    raise RuntimeError(f"{url}: {err}")

def main(argv):
    want = argv or list(WORKS)
    os.makedirs(OUT, exist_ok=True)
    idx_path = os.path.join(OUT, "iopera.html")
    if not os.path.exists(idx_path):
        open(idx_path, "wb").write(get(INDEX))
    idx = open(idx_path, "rb").read().decode("latin-1")
    pages = []
    for p in re.findall(r'corpusthomisticum\.org/([a-z]+[0-9a-z]*)\.html', idx):
        w = re.match(r"[a-z]+", p).group(0)
        if any(w == x for x in want) and p not in pages:
            pages.append(p)
    got = 0
    for p in pages:
        dest = os.path.join(OUT, p + ".html")
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            continue
        data = get(BASE + p + ".html")
        if not data:
            print(f"EMPTY {p}", file=sys.stderr)
            continue
        with open(dest + ".tmp", "wb") as f:
            f.write(data)
        os.replace(dest + ".tmp", dest)
        got += 1
        time.sleep(1)
    print(f"{len(pages)} pages listed for {', '.join(want)}; fetched {got} new")

if __name__ == "__main__":
    main(sys.argv[1:])
