#!/usr/bin/env python3
"""
build_josephus.py -- Josephus in Greek (Niese, 1885-95) and in English
(Whiston, 1737), both from the PerseusDL TEI, aligned unit for unit by
Whiston's book.chapter.section.

    python3 pipeline/build_josephus.py --fetch   # pinned TEI -> data/corpus/perseus-josephus/ (gitignored)
    python3 pipeline/build_josephus.py           # build data/books/josephus-*.json + manifest entries
    python3 pipeline/build_josephus.py --check   # rebuild in memory: = the committed manifest entries
    python3 tests/josephus_test.py

WORKS. The Antiquities, the Jewish War, the Life and Against Apion: eight
books, a Greek and an English for each work.

LICENCE (rule 6). Niese's Greek and Whiston's English are public domain. The
Perseus TEI of each is "Available under a Creative Commons Attribution-
ShareAlike 4.0 International License", so these books are handled like the
Apostolic Fathers: built locally, gitignored, and only the manifest entries
committed, each with a `rights` block and `redistribute_whole: false`.

ALIGNMENT. Two numberings are in use for Josephus. Niese's sections
(Ant. 18.63) are the modern scholarly standard; Whiston's book.chapter.section
(Ant. 18.3.3) is what readers of Whiston know. Perseus marks Whiston's
chapters and sections as milestones in BOTH files, at the same points (1,702
milestones in each Antiquities file, 818 in each War). So a unit here is one
Whiston section, `josephus-ant-niese:18.3.3` and `josephus-ant-whiston:18.3.3`,
and each Greek unit also records the Niese sections it spans (`lex.niese`),
so either citation finds it. Each unit links to its counterpart. The Life is
cited by Whiston's section alone, Against Apion by book.section.

Text before a book's first Whiston milestone (Niese's table of contents, the
ancient summary at the head of each book of the Antiquities) has no Whiston
number. It becomes a unit `<book>.arg`, in the Greek only.

What Niese brackets as suspect (<del>, e.g. the Testimonium Flavianum, Ant.
18.63-64) is kept and printed in square brackets, as Niese prints it. Notes,
heads and Whiston's chapter titles are left out of `text`.

STRONG'S TAGS on the Greek, by the same fixed rules as the Apostolic Fathers
(build_apostolic_fathers.tag_word), never guessed.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_apostolic_fathers as A  # noqa: E402

BOOKS = A.BOOKS
MANIFEST = A.MANIFEST
T = "{http://www.tei-c.org/ns/1.0}"

REPO = "PerseusDL/canonical-greekLit"
COMMIT = "bcc5df0602f3b3fe6fefe1e1d575602a25ab1db6"
CACHE = os.path.join(ROOT, "data", "corpus", "perseus-josephus", COMMIT[:12])
SOURCE_URL = f"https://github.com/{REPO}/tree/{COMMIT}/data/tlg0526"
PINS_PATH = os.path.join(HERE, "josephus_pins.json")

# key, TLG work, title, SBL abbreviation, citation levels (Whiston)
WORKS = [
    ("ant", "tlg001", "Antiquities of the Jews", "Ant.", "book.chapter.section"),
    ("war", "tlg004", "The Jewish War", "J.W.", "book.chapter.section"),
    ("life", "tlg002", "The Life of Flavius Josephus", "Life", "section"),
    ("apion", "tlg003", "Against Apion", "Ag. Ap.", "book.section"),
]
EDITIONS = {
    "niese": {"file": "perseus-grc2", "lang": "grc",
              "edition": "B. Niese, Flavii Iosephi opera (Berlin: Weidmann, 1885-95)",
              "author": "Flavius Josephus"},
    "whiston": {"file": "perseus-eng2", "lang": "en",
                "edition": "W. Whiston, The Works of Flavius Josephus (1737; Auburn and "
                           "Rochester: Alden and Beardsley, 1856)",
                "author": "Flavius Josephus, tr. William Whiston"},
}
RIGHTS = {
    "license": "CC BY-SA 4.0 (the Perseus Digital Library TEI); the underlying text "
               "(Niese 1885-95, Whiston 1737) is public domain",
    "attribution": "Perseus Digital Library, Tufts University (PerseusDL/canonical-greekLit)",
    "source_url": SOURCE_URL,
    "redistribute_whole": False,
}
SKIP = {T + "note", T + "head", T + "label"}

# Per-file corrections to Perseus's Whiston milestones (rule 2: the TEI is never
# edited; these rerun on refetch). Each was found by the two checks read() and
# the validator run: Whiston's numbers must run 1, 2, 3 ... in every file, and
# each Whiston unit must begin at the same Niese section in the Greek and the
# English. The other file of the pair is the witness for each fix.
#   renumber: (book, milestone unit, n as keyed, which occurrence in the book, n as it should be)
#   insert:   (book, Niese section) -- a Whiston section the file lacks begins
#             there, and every later section of that book counts one higher
FIXES = {
    ("ant", "whiston"): {"renumber": [
        ("2", "Whiston_section", "10", 1, "9"),    # 2.6 runs 1-8, 10, 10: the Greek has 9
        ("5", "Whiston_chapter", "8", 1, "7"),     # chapters 6, 8, 8: the Greek has 7
        ("13", "Whiston_chapter", "7", 1, "4"),    # chapters 3, 7, 5: the Greek has 4
    ]},
    ("apion", "niese"): {"insert": [
        ("2", "2.109"),   # the Greek lacks Whiston 2.9 (77 sections in the English, 76 here);
                          # the English begins it at Niese 2.109, and every later one agrees
    ]},
}


def rel_path(work, ed):
    tlg = dict((k, w) for k, w, *_ in WORKS)[work]
    return f"data/tlg0526/{tlg}/tlg0526.{tlg}.{EDITIONS[ed]['file']}.xml"


def local(rel):
    return os.path.join(CACHE, *rel.split("/"))


def pins():
    with open(PINS_PATH, encoding="utf-8") as f:
        return json.load(f)


def fetch():
    import pinned_fetch as F
    p = pins()
    F.fetch(REPO, COMMIT, [(rel, local(rel), p[rel]) for rel in p], ua="canon-corpus/josephus")


def verify_pins():
    p = pins()
    bad = [r for r, w in p.items() if not os.path.exists(local(r)) or A.sha256_file(local(r)) != w]
    if bad:
        raise SystemExit(f"pinned inputs missing or changed: {bad[:3]}\n"
                         f"  run: python3 pipeline/build_josephus.py --fetch")


class Stream:
    """Walks a TEI body in document order and files its text under the current
    Whiston number, noting the Niese section each piece came from."""

    def __init__(self, levels, fixes=None):
        self.levels = levels
        self.fixes = fixes or {}
        self.seen = {}
        self.shift = 0
        self.book = None
        self.chapter = None
        self.section = None
        self.niese = None
        self.order, self.text, self.spans = [], {}, {}

    def key(self):
        if self.section is None:
            return (self.book, "arg") if self.book else ("arg",)
        if self.levels == "section":
            return (self.section,)
        if self.levels == "book.section":
            return (self.book, self.section)
        return (self.book, self.chapter, self.section)

    def put(self, s):
        if not s:
            return
        k = self.key()
        if k not in self.text and not s.strip():
            return                    # whitespace between milestones opens no unit
        if k not in self.text:
            self.order.append(k)
            self.text[k], self.spans[k] = [], []
        self.text[k].append(s)
        if self.niese and s.strip() and self.niese not in self.spans[k]:
            self.spans[k].append(self.niese)

    def walk(self, el):
        tag = el.tag
        if tag == T + "div" and el.get("type") == "textpart":
            if el.get("subtype") == "book":
                self.book, self.chapter, self.section = el.get("n"), None, None
                self.seen, self.shift = {}, 0
            elif el.get("subtype") == "section":
                self.niese = f"{self.book}.{el.get('n')}" if self.book else el.get("n")
                if (self.book, self.niese) in self.fixes.get("insert", []):
                    self.shift += 1
                    self.section = str(int(self.section) + 1)
        elif tag == T + "milestone":
            unit, n = el.get("unit"), el.get("n").rstrip(".")
            k = (unit, n)
            self.seen[k] = self.seen.get(k, 0) + 1
            for b, u, was, nth, now in self.fixes.get("renumber", []):
                if (b, u, was, nth) == (self.book, unit, n, self.seen[k]):
                    n = now
            if unit == "Whiston_chapter":
                self.chapter = n
                self.section = "0"    # text before the chapter's first section shows as .0
            elif unit == "Whiston_section":
                self.section = str(int(n) + self.shift)
        if tag in SKIP:
            self.put(" ")
            return
        if tag == T + "del":
            self.put("[")
        if tag == T + "lb":
            self.put(" ")
        self.put(el.text)
        for c in el:
            self.walk(c)
            self.put(c.tail)
        if tag == T + "del":
            self.put("]")
        if tag == T + "p":
            self.put(" ")


def clean(s):
    s = re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip()
    return re.sub(r"\[\s+", "[", re.sub(r"\s+\]", "]", s))


def read(work, ed):
    levels = dict((k, lv) for k, *_, lv in WORKS)[work]
    root = ET.parse(local(rel_path(work, ed))).getroot()
    lic = root.find(f".//{T}availability/{T}licence")
    licence = clean("".join(lic.itertext())) if lic is not None else \
        clean("".join(root.find(f".//{T}availability").itertext()))
    if "Attribution-ShareAlike 4.0" not in licence:
        raise SystemExit(f"HARD STOP: {rel_path(work, ed)}: licence line is not the CC BY-SA 4.0 "
                         f"recorded ({licence!r}); re-read the rights before building")
    st = Stream(levels, FIXES.get((work, ed)))
    st.walk(root.find(f".//{T}body"))
    check_order(work, ed, st.order)
    return [(k, clean("".join(st.text[k])), st.spans[k]) for k in st.order]


def check_order(work, ed, keys):
    """Whiston's numbers run 1, 2, 3 ... (a chapter after its book's last, a
    section after its chapter's last). A break means a keying error the FIXES
    do not cover yet, and text would be filed under the wrong number: stop."""
    prev = None
    for k in keys:
        if k[-1] == "arg":
            prev = None
            continue
        if prev is not None and prev[:-1] == k[:-1]:
            ok = int(k[-1]) == int(prev[-1]) + 1
        elif prev is not None and len(k) == 3 and prev[0] == k[0]:
            ok = k[2] == "1" and (prev[1] == "pr" and k[1] == "1" or
                                  prev[1] != "pr" and int(k[1]) == int(prev[1]) + 1)
        else:
            ok = k[-1] == "1" and (len(k) < 3 or k[1] in ("pr", "1"))
        if not ok:
            raise SystemExit(f"HARD STOP: {work}/{ed}: Whiston number {'.'.join(prev or ())} "
                             f"is followed by {'.'.join(k)}; add a FIXES row, or read why")
        prev = k


def build_work(work, title, abbrev, levels):
    """Two books (Greek, English) for one work, aligned by Whiston number."""
    out = {}
    read_ = {ed: read(work, ed) for ed in EDITIONS}
    keys = {ed: {k for k, t, _ in rows if t} for ed, rows in read_.items()}
    for ed, rows in read_.items():
        other = "whiston" if ed == "niese" else "niese"
        slug, oslug = f"josephus-{work}-{ed}", f"josephus-{work}-{other}"
        units = []
        for k, text, spans in rows:
            if not text:
                continue
            cid = ".".join(k)
            u = {"id": f"{slug}:{cid}", "ref": f"{abbrev} {cid}", "text": text, "links": []}
            if k in keys[other]:
                u["links"].append({"target": f"{oslug}:{cid}", "type": "translation" if ed == "niese"
                                   else "original", "resolved": True})
            u["lex"] = {"niese": spans}
            units.append(u)
        e = EDITIONS[ed]
        rel = rel_path(work, ed)
        out[slug] = {
            "slug": slug, "title": title + (" (Greek)" if ed == "niese" else " (English)"),
            "author": e["author"],
            "source": {"path": os.path.relpath(local(rel), os.path.join(ROOT, "data", "corpus")),
                       "format": "tei-perseus", "edition": e["edition"], "lang": e["lang"],
                       "sha256": A.sha256_file(local(rel))},
            "scheme": {"citation": f"{abbrev} {levels} (Whiston)",
                       "resolution": "Whiston section",
                       "honesty": "exact to Whiston's sections, which Perseus marks in both "
                                  "files at the same points; each unit's Niese sections are "
                                  "in lex.niese" + ("" if ed == "niese" else
                                                    " (the Niese section where the English "
                                                    "piece begins, as Perseus keyed it)"),
                       "note": "Notes, heads and chapter titles are left out of `text`"
                               + ("; Niese's brackets (<del>) are printed as [ ]" if ed == "niese" else "")},
            "rights": dict(RIGHTS),
            "alignment": {"counterpart": f"josephus-{work}-{'whiston' if ed == 'niese' else 'niese'}",
                          "units": len(units),
                          "matched": sum(1 for u in units if u["links"]),
                          "unmatched": [u["id"].split(":", 1)[1] for u in units if not u["links"]]},
            "units": units,
        }
    return out


def entry(book, blob):
    e = {"title": book["title"], "author": book["author"], "format": book["source"]["format"],
         "sha256": book["source"]["sha256"], "units": len(book["units"]),
         "scheme": book["scheme"], "rights": book["rights"], "alignment": book["alignment"]}
    if "tagging" in book:
        e["tagging"] = {k: v for k, v in book["tagging"].items() if k != "scheme"}
    e["built_sha256"] = hashlib.sha256(blob).hexdigest()
    return e


def build():
    verify_pins()
    tables = A.tag_tables()
    out = {}
    for work, _, title, abbrev, levels in WORKS:
        for slug, book in build_work(work, title, abbrev, levels).items():
            if slug.endswith("-niese"):
                book = A.tag(book, tables)
            blob = json.dumps(book, ensure_ascii=False).encode("utf-8")
            out[slug] = (book, blob, entry(book, blob))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    built = build()
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    for slug, (book, _, e) in built.items():
        al = e["alignment"]
        t = e.get("tagging")
        tag = (f" {100 * sum(t[r] for r in A.RULES) / t['words']:5.1f}% of {t['words']:,} words tagged"
               if t else "")
        print(f"  {slug:<26}{e['units']:>5} units {al['matched']:>5} aligned "
              f"{len(al['unmatched']):>3} unaligned{tag}")
    if a.report:
        return
    if a.check:
        bad = [s for s, (_, blob, e) in built.items() if manifest.get(s) != e
               or (os.path.exists(os.path.join(BOOKS, s + ".json"))
                   and open(os.path.join(BOOKS, s + ".json"), "rb").read() != blob)]
        if bad:
            raise SystemExit(f"CHECK FAILED: rebuilt books differ from the manifest: {bad}")
        print("  CHECK PASSED: every book = its committed manifest entry (built_sha256).")
        return
    for slug, (_, blob, e) in built.items():
        A.write_atomic(os.path.join(BOOKS, slug + ".json"), blob)
        manifest[slug] = e
    A.write_atomic(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    print(f"  wrote {len(built)} books + {len(manifest)}-entry manifest")


if __name__ == "__main__":
    main()
