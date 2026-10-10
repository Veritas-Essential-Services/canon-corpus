#!/usr/bin/env python3
"""Convert the STANDARD EBOOKS items of pipeline/<shelf>_shelf.json (2026-10-10).

    python3 pipeline/convert_shelf_se.py <shelf>   # after fetch_shelf.py <shelf>

The companion of convert_shelf_gutenberg.py for the single-page XHTML that
fetch_shelf.py saves for a "standard_ebooks" row. SE marks its structure, so
nothing is detected: each bodymatter <section id="chapter-N"> is a chapter,
its <hgroup> (or <h2>) gives the ordinal and title, and every <p> or <li> after it (or a
quotation's <cite> standing outside one) is a
paragraph unit. Front and back matter (SE's title page, imprint, colophon,
uncopyright) are not the book and are skipped; so are figures.

Also taken: the author's own front and back matter (preface, appendix,
endnotes...; AUTHOR_MATTER), keyed by SE's section id. Endnote markers are
dropped from the paragraph text.

Unit ids: <slug>:<N>.<par>, N = SE's chapter number (exact) or the section id
(`preface`, `endnotes`), par = running
paragraph within the chapter as SE sets it. Same {id, ref, text, links[]}
contract as every other converter.

Reads data/corpus/<shelf>/<slug>.xhtml; writes data/books/<slug>.json
(gitignored) atomically (temp + rename) and skips books already built (rule
5). The shelf's `_jurisdiction` is copied into the book's `rights` block, so a
consumer sees a US-only status without opening the shelf. Stats only to
data/corpus/<shelf>/<shelf>_convert_report.json. Does NOT write
data/books/manifest.json and does NOT touch data/uids/ (attended steps).
"""
import hashlib, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "data", "corpus")

RE_SECTION = re.compile(r'<section[^>]*\bid="([^"]+)"[^>]*\bepub:type="([^"]*)"[^>]*>(.*?)</section>', re.S)
# the author's own matter outside the chapters (Racundra's preface, appendix
# and endnotes); SE's own pages (titlepage, imprint, colophon...) never match
AUTHOR_MATTER = {"preface", "foreword", "introduction", "prologue", "epilogue", "afterword",
                 "appendix", "endnotes", "glossary", "conclusion"}
RE_HGROUP = re.compile(r"<hgroup>(.*?)</hgroup>", re.S)
RE_BLOCK = re.compile(r"<(p|li|cite)(?:\s[^>]*)?>(.*?)</\1>", re.S)

def flat(fragment):
    """Inline markup off, entities decoded, whitespace collapsed."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()

def convert_se(path, slug, title, author, rights=None):
    raw = open(path, encoding="utf-8").read()
    # endnote markers would glue a number onto the word they follow
    raw = re.sub(r'<a[^>]*epub:type="noteref"[^>]*>.*?</a>', "", raw, flags=re.S)
    raw = re.sub(r'<a[^>]*epub:type="backlink"[^>]*>.*?</a>', "", raw, flags=re.S)
    units = []
    for m in RE_SECTION.finditer(raw):
        sid, types, body = m.group(1), set(m.group(2).split()), m.group(3)
        ch = re.fullmatch(r"chapter-(\d+)", sid)
        if ch and "chapter" in types:
            n = int(ch.group(1))
        elif types & AUTHOR_MATTER:
            n = sid
        else:
            continue
        hg = RE_HGROUP.search(body) or re.search(r"<h2[^>]*>.*?</h2>", body, re.S)
        head = ""
        if hg:
            inner = hg.group(1) if hg.re is RE_HGROUP else hg.group(0)
            ordinal = re.search(r"<h2[^>]*>(.*?)</h2>", inner, re.S)
            name = re.search(r"<p[^>]*>(.*?)</p>", inner, re.S)
            head = ". ".join(x for x in (flat(ordinal.group(1)) if ordinal else "",
                                          flat(name.group(1)) if name else "") if x)
            body = body[:hg.start()] + body[hg.end():]
        body = re.sub(r"<figure.*?</figure>", "", body, flags=re.S)
        pnum = 0
        for b in RE_BLOCK.finditer(body):
            text = flat(b.group(2))
            if not text:
                continue
            pnum += 1
            ref = (f"Chapter {head or n}" if isinstance(n, int) else (head or sid.title())) + f", par. {pnum}"
            units.append({"id": f"{slug}:{n}.{pnum}", "ref": ref, "text": text, "links": []})
    book = {"slug": slug, "title": title, "author": author,
            "source": {"path": os.path.relpath(path, CORPUS), "format": "standard-ebooks-xhtml",
                       "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest()},
            "scheme": {"citation": "chapter + paragraph", "resolution": "paragraph",
                       "honesty": "chapters exact (SE's marked sections); paragraph = running paragraph "
                                  "within the chapter as SE sets it; SE's text, spelling modernized, "
                                  "not a transcription of the first edition"},
            "units": units}
    if rights:
        book["rights"] = rights
    return book

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: convert_shelf_se.py <shelf>")
    name = sys.argv[1]
    shelf = json.load(open(os.path.join(HERE, f"{name}_shelf.json"), encoding="utf-8"))
    author = shelf.get("_author", name)
    rights = None
    if shelf.get("_jurisdiction"):
        rights = {"source_license": "Standard Ebooks production, CC0 1.0",
                  "jurisdiction": shelf["_jurisdiction"]}
    src = os.path.join(CORPUS, name)
    out = os.path.join(HERE, "..", "data", "books")
    os.makedirs(out, exist_ok=True)
    stats = {}
    for slug, row in shelf.get("standard_ebooks", {}).items():
        path, dest = os.path.join(src, slug + ".xhtml"), os.path.join(out, slug + ".json")
        if not os.path.exists(path):
            stats[slug] = {"status": "not fetched"}; print(slug, "not fetched"); continue
        if os.path.exists(dest):
            book = json.load(open(dest, encoding="utf-8"))
        else:
            book = convert_se(path, slug, row[1], author, rights)
            with open(dest + ".tmp", "w", encoding="utf-8") as f:
                json.dump(book, f, ensure_ascii=False)
            os.replace(dest + ".tmp", dest)
        units = book.get("units", [])
        ids = [u["id"] for u in units]
        s = {"status": "built", "units": len(units),
             "chapters": len({i.split(":", 1)[1].split(".")[0] for i in ids}),
             "duplicate_ids": len(ids) - len(set(ids)),
             "chars": sum(len(u["text"]) for u in units)}
        stats[slug] = s
        print(slug, s, flush=True)
    rep = os.path.join(src, f"{name}_convert_report.json")
    if os.path.isdir(src):
        json.dump(stats, open(rep + ".tmp", "w"), indent=1)
        os.replace(rep + ".tmp", rep)
    built = [s for s in stats.values() if s["status"] == "built"]
    print(f"{len(built)} built, {sum(s['units'] for s in built)} units")
    return stats

if __name__ == "__main__":
    main()
