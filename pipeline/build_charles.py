#!/usr/bin/env python3
"""
build_charles.py -- R. H. Charles (ed.), *The Apocrypha and Pseudepigrapha
of the Old Testament in English* (Oxford: Clarendon Press, 1913), 2 vols,
read verse by verse out of the Internet Archive's OCR of the scans.

    python3 pipeline/build_charles.py --fetch    # pinned hOCR -> data/corpus/charles/ (gitignored, ~200 MB)
    python3 pipeline/build_charles.py            # build data/books/charles-*.json + manifest entries
    python3 pipeline/build_charles.py --check    # rebuild in memory: = the committed manifest entries
    python3 pipeline/build_charles.py --report   # per-book measures, writes nothing
    python3 tests/charles_test.py

SOURCE. No machine-readable Charles exists. Wikisource has the front matter
and the Sibyllines only; the transcriptions on the web are unattributed. So
the text is the OCR the Internet Archive made of two scans (both University
of Toronto copies, both marked NOT_IN_COPYRIGHT):

    vol. I  (Apocrypha)       theapocryphaandp01unknuoft   708 leaves, 500 ppi
    vol. II (Pseudepigrapha)  apocryphapseudep02charuoft   902 leaves, 300 ppi

The BYU scans the request named (apocryphapseudep01char / 02char) were
OCR'd as Greek: their English is unreadable, so they are not used. The hOCR
(word boxes) is pinned by sha256; the archive can re-derive its OCR, and a
changed file stops the build rather than silently changing the text.

WHAT IS READ, AND HOW WELL. charles_ocr.py reads the layout: the translation
(large type) is separated from the notes and apparatus (small type), verse
numbers are read from the margin and decoded against the page's running
head. Every unit records how its number was got (`scan.number`: read as
printed / read with an OCR letter-for-digit fix / inferred from the
sequence) and where its first words were placed (`scan.start`). Charles
numbers the margin LINE on which a verse begins, so where a verse begins
mid-line the split is at the first sentence break in that line: a guess,
and flagged as one. The text is unproofread OCR and says so.

Verification is measured, not claimed: for every book with a KJV
counterpart the build counts how many of the KJV Apocrypha's verse numbers
it has a unit for (Charles's numbering mostly follows it), and for every
book how many pages' running heads agree with the decoded chapters. Both go
into the manifest. A book is built verse by verse only if its decoding
clears the bar in MODE_BAR; otherwise (and for the books Charles prints in
parallel columns: Adam and Eve, 2 Enoch's two recensions, Ahikar's versions)
its unit is the printed page, which is exact and checkable against the scan.

TWO COLUMNS ON A PROSE PAGE. Where a verse book prints two witnesses side by
side (the LXX and Theodotion in Susanna and Bel; the alpha and beta texts in
places in the Testaments; I Esdras beside its Hebrew parallel), only the left
column is read: the right one is numbered in its right margin, which this
reader does not read, and taking it would splice the two texts together. The
number of such leaves is in each book's measure
(`two_column_leaves_left_kept`), so the loss is labelled rather than hidden.

RIGHTS. Published 1913: public domain in the United States. Outside it, life
+ 70 runs from each contributor's death, and one contributor outlived 1955:
J. A. F. Gregg (the Additions to Esther) died in 1961 (date from general
reference, not checked against a source this session), so that book is still
in copyright in life+70 countries until the end of 2031; it is flagged in its
rights block. The built books are gitignored like every other book; only
manifest entries are committed.

Nothing is minted: unit ids are citations (`charles-tob:5.10`), not uids.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import charles_ocr as C  # noqa: E402

BOOKS_DIR = os.path.join(ROOT, "data", "books")
MANIFEST = os.path.join(BOOKS_DIR, "manifest.json")
CACHE = os.path.join(ROOT, "data", "corpus", "charles")

VOLUMES = {
    "v1": {"ia": "theapocryphaandp01unknuoft", "title": "Vol. I: Apocrypha",
           "file": "theapocryphaandp01unknuoft_hocr.html",
           "sha256": "1b02f9fae2b863617a1caf74a23ef55c4b78c98c4bc20489a97da8afa7452c08",
           "T": 50},
    "v2": {"ia": "apocryphapseudep02charuoft", "title": "Vol. II: Pseudepigrapha",
           "file": "apocryphapseudep02charuoft_hocr.html",
           "sha256": "cca43ccaf0ed41bebaf96adfe50c0a49b09150ec4b541e572866eefcb6782d24",
           "T": 38},
}
# the KJV Apocrypha, used only to MEASURE the verse decoding (eBible.org, PD)
KJV_CHECK = {"url": "https://ebible.org/Scriptures/eng-kjv_usfm.zip", "file": "eng-kjv_usfm.zip",
             "sha256": "1bab5d4d030439831fc0b39d7f11001dd8527fc6277405e7f6512273c200c3a4"}

# key, vol, title, contributor(s) as the volume lists them, first and last
# text leaf, layout, options. Leaves are the scan's page index (0-based, as in
# https://archive.org/details/<ia>/page/n<leaf>).
#   layout: prose | poetry | left-column (I Esdras: the right column is its
#           canonical parallel) | columns (parallel versions: page units) | lines
#   opts:   kjv (USFM code of the KJV counterpart), start (first chapter),
#           max (last chapter), chapterless, parts
BOOKS = [
    ("1esd", "v1", "I Esdras", "S. A. Cook", 36, 73, "left-column", {"kjv": "1ES", "max": 9}),
    ("1macc", "v1", "I Maccabees", "W. O. E. Oesterley", 82, 139, "prose", {"kjv": "1MA", "max": 16}),
    ("2macc", "v1", "II Maccabees", "James Moffatt", 147, 169, "prose", {"kjv": "2MA", "max": 15}),
    ("3macc", "v1", "III Maccabees", "Cyril W. Emmet", 178, 188, "prose", {"max": 7}),
    ("tob", "v1", "The Book of Tobit", "D. C. Simpson", 217, 256, "prose", {"kjv": "TOB", "max": 14}),
    ("jdt", "v1", "The Book of Judith", "A. E. Cowley", 263, 282, "prose", {"kjv": "JDT", "max": 16}),
    ("sir", "v1", "Sirach", "G. H. Box and W. O. E. Oesterley", 331, 533, "poetry", {"kjv": "SIR", "max": 51}),
    ("wis", "v1", "The Wisdom of Solomon", "Samuel Holmes", 550, 583, "poetry", {"kjv": "WIS", "max": 19}),
    ("bar", "v1", "The Book of Baruch", "O. C. Whitehouse", 598, 611, "prose", {"kjv": "BAR", "max": 5}),
    ("epjer", "v1", "The Epistle of Jeremy", "C. J. Ball", 614, 626, "prose", {"chapterless": True}),
    ("prman", "v1", "The Prayer of Manasses", "Herbert E. Ryle", 635, 639, "prose", {"chapterless": True}),
    ("azar", "v1", "The Prayer of Azariah and the Song of the Three Children", "W. H. Bennett",
     647, 652, "prose", {"chapterless": True}),
    ("sus", "v1", "Susanna", "D. M. Kay", 662, 666, "prose", {"chapterless": True}),
    ("bel", "v1", "Bel and the Dragon", "T. Witton Davies", 673, 679, "prose", {"chapterless": True}),
    ("addesth", "v1", "The Additions to Esther", "J. A. F. Gregg", 687, 698, "prose", {"letters": "ABCDEF"}),
    ("jub", "v2", "The Book of Jubilees", "R. H. Charles", 30, 101, "prose", {"max": 50}),
    ("arist", "v2", "The Letter of Aristeas", "Herbert T. Andrews", 113, 141, "prose", {"chapterless": True}),
    ("adam", "v2", "The Books of Adam and Eve", "L. S. A. Wells", 153, 173, "columns", {}),
    ("mart", "v2", "The Martyrdom of Isaiah", "R. H. Charles", 178, 181, "prose", {"max": 5}),
    ("1en", "v2", "The Book of Enoch (1 Enoch)", "R. H. Charles", 207, 300, "prose", {"max": 108}),
    ("testxii", "v2", "The Testaments of the Twelve Patriarchs", "R. H. Charles", 315, 379, "prose",
     {"parts": ["Reu.", "Sim.", "Levi", "Jud.", "Iss.", "Zeb.", "Dan", "Naph.", "Gad", "Ash.", "Jos.", "Benj."]}),
    ("sib", "v2", "The Sibylline Oracles", "H. C. O. Lanchester", 396, 425, "lines",
     {"parts": ["frag1", "frag2", "frag3", "3", "4", "5"]}),
    ("asmos", "v2", "The Assumption of Moses", "R. H. Charles", 433, 443, "prose", {"max": 12}),
    ("2en", "v2", "The Book of the Secrets of Enoch (2 Enoch)", "Nevill Forbes and R. H. Charles",
     450, 488, "columns", {}),
    ("2bar", "v2", "II Baruch (the Syriac Apocalypse)", "R. H. Charles", 500, 545, "prose", {"max": 87}),
    ("3bar", "v2", "III Baruch (the Greek Apocalypse)", "H. Maldwyn Hughes", 552, 560, "prose", {"max": 17}),
    ("4ezra", "v2", "IV Ezra", "G. H. Box", 580, 643, "prose", {"kjv": "2ES", "start": 3, "max": 14}),
    ("pssol", "v2", "The Psalms of Solomon", "G. Buchanan Gray", 650, 671, "poetry", {"max": 18}),
    ("4macc", "v2", "The Fourth Book of Maccabees", "R. B. Townshend", 685, 704, "prose", {"max": 18}),
    ("aboth", "v2", "Pirke Aboth: The Sayings of the Fathers", "R. Travers Herford", 710, 733, "prose",
     {"max": 6}),
    ("ahikar", "v2", "The Story of Ahikar", "F. C. Conybeare, J. Rendel Harris and Agnes Smith Lewis",
     743, 803, "columns", {}),
    ("zad", "v2", "Fragments of a Zadokite Work", "R. H. Charles", 817, 853, "prose", {"max": 20}),
]
TESTAMENT_HEADS = ["REUBEN", "SIMEON", "LEVI", "JUDAH", "ISSACHAR", "ZEBULUN", "DAN",
                   "NAPHTALI", "GAD", "ASHER", "JOSEPH", "BENJAMIN"]
# a book is read verse by verse only if at least this share of its verse
# numbers were read off the page (as printed or with a letter-for-digit fix)
# and at least this share of its readable running heads agree with it
MODE_BAR = {"read": 0.6, "heads": 0.75}
EDITION = ("R. H. Charles (ed.), The Apocrypha and Pseudepigrapha of the Old Testament in English, "
           "2 vols (Oxford: Clarendon Press, 1913)")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_atomic(path, data):
    with open(path + ".tmp", "wb") as f:
        f.write(data)
    os.replace(path + ".tmp", path)


def download(url, dest, sha):
    if os.path.exists(dest) and sha256_file(dest) == sha:
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "canon-corpus/charles"})
    with urllib.request.urlopen(req, timeout=600) as r, open(dest + ".tmp", "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    got = sha256_file(dest + ".tmp")
    if got != sha:
        os.remove(dest + ".tmp")
        raise SystemExit(f"{url}: sha256 {got} != pinned {sha}")
    os.replace(dest + ".tmp", dest)


def fetch():
    for v in VOLUMES.values():
        download(f"https://archive.org/download/{v['ia']}/{v['file']}",
                 os.path.join(CACHE, v["file"]), v["sha256"])
        print(f"  {v['ia']}: hOCR present, sha256 pinned")
    download(KJV_CHECK["url"], os.path.join(CACHE, KJV_CHECK["file"]), KJV_CHECK["sha256"])
    print("  eng-kjv_usfm.zip (verse lists for the measure): present, sha256 pinned")


def pages(vol):
    """The volume's leaves, parsed once and cached (gzipped JSON) beside the hOCR."""
    v = VOLUMES[vol]
    src = os.path.join(CACHE, v["file"])
    cache = os.path.join(CACHE, f"{v['ia']}.{v['sha256'][:12]}.pages.json.gz")
    if os.path.exists(cache):
        return C.load_pages(cache)
    if not os.path.exists(src) or sha256_file(src) != v["sha256"]:
        raise SystemExit(f"pinned hOCR missing or changed: {src}\n  run: python3 pipeline/build_charles.py --fetch")
    P = C.read_hocr(src)
    C.save_pages(P, cache)
    return C.load_pages(cache)


def kjv_verses():
    p = os.path.join(CACHE, KJV_CHECK["file"])
    if not os.path.exists(p):
        return None
    out = collections.defaultdict(set)
    with zipfile.ZipFile(p) as z:
        for n in z.namelist():
            m = re.match(r'\d+-([0-9A-Z]{3})eng-kjv\.usfm$', n)
            if not m:
                continue
            c = 0
            for line in z.read(n).decode("utf-8").splitlines():
                mc = re.match(r'\\c (\d+)', line)
                if mc:
                    c = int(mc.group(1))
                for mv in re.finditer(r'\\v (\d+)', line):
                    out[m.group(1)].add((c, int(mv.group(1))))
    return out


def letter_head(t):
    """Additions to Esther: 'ESTHER. B5—C 5' -> (2, 5, 3, 5)."""
    m = re.search(r'ESTHER\.?\s*([A-F])\s*([0-9IlO]{1,3})\s*(?:[-—–]+\s*(?:([A-F])\s*)?([0-9IlO]{1,3}))?', t)
    if not m:
        return None
    a = "ABCDEF".index(m.group(1)) + 1
    c = "ABCDEF".index(m.group(3)) + 1 if m.group(3) else a
    return (a, C.num(m.group(2)), c, C.num(m.group(4)) if m.group(4) else None)


def testament_of_page(P, leaves):
    out = {}
    for pg in leaves:
        p = P[pg]
        t = " ".join(l["text"] for l in p["lines"] if l["bbox"][3] < p["h"] * 0.065).upper()
        for i, n in enumerate(TESTAMENT_HEADS):
            if "TESTAMENT OF " + n in t:
                out[pg] = i
    return out


def page_units(P, leaves, T):
    """One unit per printed page: the body text, columns in order."""
    out = []
    for pg in leaves:
        _, body, _ = C.split_body(P[pg], T)
        cols = C.columns(body, P[pg]["w"])
        text = " | ".join(" ".join(l["text"] for l in col) for col in cols if col)
        if text.strip():
            out.append({"leaf": pg, "page": C.printed_page(P[pg]), "text": text, "columns": len(cols)})
    return out


def decode_book(P, key, vol, a, b, layout, o):
    leaves = range(a, b + 1)
    T = VOLUMES[vol]["T"]
    if layout == "lines":
        units, stats = C.sibyl_units(P, leaves, T, o["parts"])
        return units, stats, {}, [], []
    head_fn = letter_head if "letters" in o else C.head_range
    rows, heads, twocol = C.collect(P, leaves, T, layout, head_fn)
    chapters = not o.get("chapterless")
    if not chapters:
        heads = {}
    parts = pop = None
    if "parts" in o:
        parts, pop = len(o["parts"]), testament_of_page(P, leaves)
        heads = {}
    heads = C.smooth_heads(heads)
    assign = C.decode(rows, heads, chapters, o.get("start", 1), o.get("max") or (len(o["letters"]) if "letters" in o else None),
                      parts, pop)
    units, stats = C.build_units(rows, assign)
    dropped = [{"leaf": pg, "text": text} for pg, kind, _, text in rows if kind == 'a']
    return units, stats, heads, twocol, dropped


def cite(key, o, u):
    if "parts" in o:
        p = o["parts"][u["part"]].rstrip(".")
        return f"{p}.{u['v']}" if key == "sib" else f"{p}.{u['ch']}.{u['v']}"
    if "letters" in o:
        return f"{o['letters'][u['ch'] - 1]}.{u['v']}"
    if o.get("chapterless"):
        return str(u["v"])
    return f"{u['ch']}.{u['v']}"


def build_book(key, vol, title, editor, a, b, layout, o, kjv):
    P = pages(vol)
    v = VOLUMES[vol]
    slug = f"charles-{key}"
    measure = {}
    mode = "page"
    units = []
    if layout != "columns":
        vu, stats, heads, twocol, dropped = decode_book(P, key, vol, a, b, layout, o)
        n = len(vu)
        read = (stats["read"] + stats["fuzzy"]) / n if n else 0
        ok, tot = C.head_agreement(vu, heads)
        measure = {"verses": n, "number_read": stats["read"], "number_read_with_fix": stats["fuzzy"],
                   "number_inferred": stats["inferred"],
                   "start": {k[6:]: c for k, c in sorted(stats.items()) if k.startswith("start:")},
                   "headings_dropped": stats["heading-dropped"],
                   "apparatus_lines_dropped": stats["apparatus-dropped"]}
        if twocol:
            measure["two_column_leaves_left_kept"] = len(twocol)
        if heads:
            measure["running_heads_agree"] = [ok, tot]
        if kjv is not None and o.get("kjv"):
            ref = kjv[o["kjv"]]
            if o["kjv"] == "2ES":
                ref = {x for x in ref if 3 <= x[0] <= 14}
            if o["kjv"] == "BAR":
                ref = {x for x in ref if x[0] <= 5}     # the KJV's Baruch 6 is the Epistle of Jeremy
            have = {(u["ch"], u["v"]) for u in vu}
            measure["kjv_verse_numbers"] = {"kjv": len(ref), "present": len(ref & have),
                                            "beyond_kjv": len(have - ref)}
        good = read >= MODE_BAR["read"] and (not heads or ok >= MODE_BAR["heads"] * tot)
        if good:
            mode = "verse"
            for u in vu:
                c = cite(key, o, u)
                units.append({"id": f"{slug}:{c}", "ref": f"{title} {c}", "text": u["text"].strip(),
                              "links": [],
                              "scan": {"leaves": u["leaves"], "number": u["num"], "start": u["start"]}})
            # a number decoded twice (an OCR slip the decoder could not undo) keeps both, told apart
            seen = collections.Counter()
            for u in units:
                seen[u["id"]] += 1
                if seen[u["id"]] > 1:
                    u["id"] += f"~{seen[u['id']]}"
                    u["scan"]["duplicate_number"] = True
        else:
            measure["refused"] = (f"verse decoding below the bar (numbers read {read:.0%}; "
                                  f"heads {ok}/{tot}): built by printed page instead")
    if mode == "page":
        for pu in page_units(P, range(a, b + 1), v["T"]):
            # one id scheme per book: the scan leaf, always present; the printed folio,
            # where the OCR read one, rides along (a misread folio must not become an id)
            pid = f"leaf.{pu['leaf']}"
            scan = {"leaves": [pu["leaf"]], "columns": pu["columns"]}
            if pu["page"]:
                scan["printed_page"] = pu["page"]
            units.append({"id": f"{slug}:{pid}",
                          "ref": f"{title}, " + (f"p. {pu['page']}" if pu["page"] else pid),
                          "text": pu["text"], "links": [], "scan": scan})
        seen = collections.Counter()
        for u in units:
            seen[u["id"]] += 1
            if seen[u["id"]] > 1:
                u["id"] = f"{slug}:leaf.{u['scan']['leaves'][0]}"
    if mode == "verse":
        if o.get("chapterless"):
            citation = "verse"
        elif "letters" in o:
            citation = "section letter.verse (Charles's A-F)"
        elif key == "sib":
            citation = "book or fragment.line (the Greek line numbers Charles prints inline)"
        elif "parts" in o:
            citation = "testament.chapter.verse"
        else:
            citation = "chapter.verse (Charles's numbering)"
        honesty = ("verse numbers decoded from the scan's margin OCR; each unit says whether its number was "
                   "read as printed, read with a letter-for-digit fix, or inferred from the sequence; a verse "
                   "that begins mid-line is split at the line's first sentence break (scan.start='sentence'), "
                   "a guess; the text is unproofread OCR")
        if key == "sib":
            honesty = ("line numbers read from the inline '(n)' markers; text is unproofread OCR")
    else:
        citation = "scan leaf (leaf.N), one per printed page of the 1913 edition; the folio, where read, in scan.printed_page"
        honesty = ("page-exact; verses NOT segmented (Charles prints parallel versions in columns here, or "
                   "the verse numbers could not be decoded reliably); columns joined with ' | '; "
                   "the text is unproofread OCR")
    rights = {
        "license": "public domain in the US (published 1913); the scan and its OCR are the Internet "
                   "Archive's, marked NOT_IN_COPYRIGHT",
        "attribution": f"Internet Archive, {v['ia']} (University of Toronto copy)",
        "source_url": f"https://archive.org/details/{v['ia']}",
        "redistribute_whole": True,
    }
    if key == "addesth":
        rights["note"] = ("J. A. F. Gregg died 1961 (general reference, unchecked): in copyright in life+70 "
                          "countries until the end of 2031; public domain in the US")
        rights["redistribute_whole"] = False
    book = {"slug": slug, "title": title, "author": f"tr. and ed. {editor}, in Charles (1913)",
            "edition": EDITION, "volume": v["title"],
            "source": {"format": "ia-hocr", "sha256": v["sha256"], "ia": v["ia"], "leaves": [a, b]},
            "scheme": {"citation": citation, "resolution": mode, "honesty": honesty},
            "rights": rights, "measure": measure, "units": units}
    if layout != "columns" and dropped:
        book["apparatus_dropped"] = dropped     # read against the scans: docs/review/charles-ocr-flags.tsv
    return slug, book


def entry(book, blob):
    return {"title": book["title"], "author": book["author"], "format": book["source"]["format"],
            "sha256": book["source"]["sha256"], "units": len(book["units"]),
            "scheme": dict(book["scheme"], note=f"{book['edition']}; {book['volume']}, scan leaves "
                                                 f"{book['source']['leaves'][0]}-{book['source']['leaves'][1]} "
                                                 f"of {book['source']['ia']}"),
            "rights": book["rights"], "measure": book["measure"],
            "built_sha256": hashlib.sha256(blob).hexdigest()}


def build(keys=None):
    kjv = kjv_verses()
    out = {}
    for key, vol, title, editor, a, b, layout, o in BOOKS:
        if keys and key not in keys:
            continue
        slug, book = build_book(key, vol, title, editor, a, b, layout, o, kjv)
        blob = json.dumps(book, ensure_ascii=False).encode("utf-8")
        out[slug] = (book, blob, entry(book, blob))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("books", nargs="*")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    built = build(a.books)
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    for slug, (book, _, e) in built.items():
        m = e["measure"]
        k = m.get("kjv_verse_numbers")
        kj = f" kjv {k['present']}/{k['kjv']}" if k else ""
        hd = f" heads {m['running_heads_agree'][0]}/{m['running_heads_agree'][1]}" if "running_heads_agree" in m else ""
        rd = (f" read {m['number_read'] + m['number_read_with_fix']}/{m['verses']}" if m.get("verses") else "")
        print(f"  {slug:<16}{e['units']:>5} units  {e['scheme']['resolution']:<6}{rd}{hd}{kj}")
    if a.report:
        return
    if a.check:
        bad = [s for s, (_, blob, e) in built.items() if manifest.get(s) != e]
        if bad:
            raise SystemExit(f"CHECK FAILED: rebuilt books differ from the manifest: {bad}")
        print("  CHECK PASSED: every book = its committed manifest entry (built_sha256).")
        return
    for slug, (_, blob, e) in built.items():
        write_atomic(os.path.join(BOOKS_DIR, slug + ".json"), blob)
        manifest[slug] = e
    write_atomic(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    print(f"  wrote {len(built)} books + {len(manifest)}-entry manifest")


if __name__ == "__main__":
    main()
