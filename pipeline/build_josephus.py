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
so either citation finds it. Each unit links to its counterpart. Where
Perseus's milestones slip, FIXES corrects them, and the build stops on a new
slip: on numbers out of order (check_order), and on a run of units whose
English fits its neighbour's Greek better than its own (shift_runs, by length). The Life is
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
# edited; these rerun on refetch). Each was found by the checks read() and the
# validator run: Whiston's numbers must run 1, 2, 3 ... in every file, each
# Whiston unit must begin at the same Niese section in the Greek and the
# English, and no run of units may fit its neighbour's text better than its own
# (shift_runs). The other file of the pair is the witness for each fix.
#   renumber: (book, milestone unit, n as keyed, which occurrence in the book, n as it should be)
#   insert:   (book, Niese section) -- a Whiston section the file lacks begins
#             there, and every later section of that book counts one higher
#   slide:    (book, dropped point, anchored point, phrase) -- a run of Whiston
#             milestones each sits one section off. The milestone keyed at the
#             dropped point ("chapter.section") is not a boundary; the run's real
#             boundary that has no milestone begins at `phrase` (Greek words,
#             spaces match any whitespace) in the text after the point keyed as
#             the anchored point; every milestone keyed between the two takes
#             the number of its neighbour on the anchored side. Chapter
#             milestones in the run travel with their sections.
#   niese:    (book, first, last, step) -- the English carries the Niese numbers
#             Perseus copied from a slid Greek run: each Niese section keyed
#             first..last takes the number of the one `step` sections along
#   niese_set: (book, Niese as keyed, as it should be)
# The Whiston English is the witness for both slides: its paragraphs are
# Whiston's printed sections (in the Antiquities every milestone opens a <p>,
# and only 11 of 1,455 <p>s have none), and both runs end at a capitalised
# chapter opening or a one-sentence paragraph that only a section number explains.
FIXES = {
    ("ant", "whiston"): {
        "renumber": [
            ("2", "Whiston_section", "10", 1, "9"),    # 2.6 runs 1-8, 10, 10: the Greek has 9
            ("5", "Whiston_chapter", "8", 1, "7"),     # chapters 6, 8, 8: the Greek has 7
            ("13", "Whiston_chapter", "7", 1, "4"),    # chapters 3, 7, 5: the Greek has 4
        ],
        "niese": [
            ("4", "277", "294", -1),   # Ant. 4.8.32-41: the Greek slide below, copied
            ("8", "144", "246", +1),   # Ant. 8.6.1-8.10.2: likewise
        ],
        "niese_set": [
            ("8", "251", "255"),       # Ant. 8.10.3 begins inside Niese 8.255
        ],
    },
    ("ant", "niese"): {"slide": [
        # Ant. 4.8.32 is one sentence, "In like manner, let no one revile a person
        # blind or dumb" (its own paragraph in Whiston, and in Niese): Perseus put
        # the Greek's 32 at the next section, Niese 4.277 "If men strive", and so
        # on to 41, which it put at Niese 4.294; Whiston's 41 begins at 4.292
        # "Let this be the constitution".
        ("4", "8.41", "8.31", "Ὁμοίως μηδὲ βλασφημείτω"),
        # Ant. 8.6.1 is "Now when the king saw that the walls of Jerusalem" (Niese
        # 8.150), not Menander on Hiram (8.144, the end of Whiston's 8.5.3); every
        # Greek milestone to 8.10.3 sits one section early, and Whiston's 8.10.3,
        # "Now when Rehoboam ... were shut up in Jerusalem", begins inside 8.255.
        ("8", "6.1", "10.3", "ἐγκεκλεισμένου τοῦ Ῥοβοάμου"),
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
        self.before = self.kchapter = None    # kchapter: the chapter as the file keys it
        self.niese = None
        self.armed = None
        self.slide, self.anchor, self.niese_map = {}, {}, {}
        self.order, self.text, self.spans = [], {}, {}

    def renumber(self, seen, unit, n):
        k = (unit, n)
        seen[k] = seen.get(k, 0) + 1
        for b, u, was, nth, now in self.fixes.get("renumber", []):
            if (b, u, was, nth) == (self.book, unit, n, seen[k]):
                return now
        return n

    def plan(self, body):
        """Resolve the slide and niese rows against the file's own sequence of
        Whiston points and Niese sections (a first pass over the body)."""
        if not (self.fixes.get("slide") or self.fixes.get("niese") or self.fixes.get("niese_set")):
            return
        points, divs, seen, chapter = {}, {}, {}, None
        for el in body.iter():
            if el.tag == T + "div" and el.get("type") == "textpart":
                if el.get("subtype") == "book":
                    self.book, chapter, seen = el.get("n"), None, {}
                elif el.get("subtype") == "section":
                    divs.setdefault(self.book, []).append(el.get("n"))
            elif el.tag == T + "milestone":
                unit = el.get("unit")
                n = self.renumber(seen, unit, el.get("n").rstrip("."))
                if unit == "Whiston_chapter":
                    chapter = n
                elif unit == "Whiston_section":
                    points.setdefault(self.book, []).append(f"{chapter}.{n}" if chapter else n)
        self.book = None
        for book, drop, after, phrase in self.fixes.get("slide", []):
            P = points[book]
            d, a = P.index(drop), P.index(after)
            self.slide[(book, drop)] = None
            step = 1 if a < d else -1
            for i in range(min(a, d) + 1, max(a, d)) if a < d else range(d + 1, a + 1):
                self.slide[(book, P[i])] = P[i + step]
            label = P[a + 1] if a < d else P[a]
            self.anchor[(book, after)] = (re.compile(r"\s+".join(map(re.escape, phrase.split()))), label)
        for book, first, last, step in self.fixes.get("niese", []):
            D = divs[book]
            for i in range(D.index(first), D.index(last) + 1):
                self.niese_map[(book, D[i])] = D[i + step]
        for book, was, now in self.fixes.get("niese_set", []):
            self.niese_map[(book, was)] = now

    def set_label(self, label):
        self.chapter, self.section = label.split(".") if "." in label else (self.chapter, label)

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
        if self.armed:
            m = self.armed[0].search(s)
            if m:
                label = self.armed[1]
                self.armed = None
                self.put(s[:m.start()])
                self.set_label(label)
                self.put(s[m.start():])
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
                self.seen, self.shift, self.kchapter = {}, 0, None
            elif el.get("subtype") == "section":
                n = self.niese_map.get((self.book, el.get("n")), el.get("n"))
                self.niese = f"{self.book}.{n}" if self.book else n
                if (self.book, self.niese) in self.fixes.get("insert", []):
                    self.shift += 1
                    self.section = str(int(self.section) + 1)
        elif tag == T + "milestone":
            unit = el.get("unit")
            n = self.renumber(self.seen, unit, el.get("n").rstrip("."))
            if unit == "Whiston_chapter":
                self.before = (self.chapter, self.section)
                self.chapter = self.kchapter = n
                self.section = "0"    # text before the chapter's first section shows as .0
            elif unit == "Whiston_section":
                if self.armed:
                    raise SystemExit(f"HARD STOP: a FIXES slide anchor was not found before "
                                     f"Whiston {self.book}.{self.chapter}.{n}: read why")
                keyed = f"{self.kchapter}.{n}" if self.levels == "book.chapter.section" else n
                if (self.book, keyed) in self.slide:
                    label = self.slide[(self.book, keyed)]
                    if label is not None:
                        self.set_label(label)
                    elif self.section == "0":
                        self.chapter, self.section = self.before   # a dropped chapter opening
                else:
                    self.section = str(int(n) + self.shift)
                self.armed = self.anchor.get((self.book, keyed))
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
    body = root.find(f".//{T}body")
    st.plan(body)
    st.walk(body)
    if st.armed:
        raise SystemExit(f"HARD STOP: {work}/{ed}: a FIXES slide anchor was never found: read why")
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


SHIFT_WINDOW, SHIFT_RATIO, SHIFT_FLOOR = 6, 0.5, 0.25


def shift_runs(pairs):
    """Runs of units whose text fits a neighbour's better than its own.

    pairs: [(key, greek, english)] in Whiston order. A Greek section and its
    English differ in length by a near-constant ratio (the median, in logs); a
    run where every unit's milestone sits one section off keeps all the
    numbers, the Niese starts and the counts in agreement, but pairs each
    English with its neighbour's Greek. For every window of SHIFT_WINDOW units,
    compare the mean distance from the median ratio as paired against the same
    with the English moved one unit either way: a window that fits at least
    twice as well shifted (and is poorly fitted as paired) is reported as
    (step, first key, last key). Measured on the four works before the 2026-10-03
    fix: shifted windows fit at 0.04-0.13, aligned ones at 0.3-1.1; the
    nearest aligned stretch elsewhere (the decrees, Ant. 14.10) needs a
    window of 4 to trip."""
    import math
    import statistics
    if len(pairs) < SHIFT_WINDOW:
        return []
    a = [math.log(max(len(g), 1)) for _, g, _ in pairs]
    b = [math.log(max(len(e), 1)) for _, _, e in pairs]
    c = statistics.median(x - y for x, y in zip(a, b))
    n, w = len(pairs), SHIFT_WINDOW
    d0 = [abs(a[i] - b[i] - c) for i in range(n)]
    found = []
    for step in (+1, -1):
        ds = [abs(a[i + step] - b[i] - c) if 0 <= i + step < n else 9.0 for i in range(n)]
        for i in range(n - w + 1):
            x, y = sum(d0[i:i + w]), sum(ds[i:i + w])
            if y < SHIFT_RATIO * x and x / w > SHIFT_FLOOR:
                if found and found[-1][0] == step and found[-1][3] + w > i:   # overlapping windows
                    found[-1] = (step, found[-1][1], pairs[i + w - 1][0], i)
                else:
                    found.append((step, pairs[i][0], pairs[i + w - 1][0], i))
    return [(step, first, last) for step, first, last, _ in found]


def build_work(work, title, abbrev, levels):
    """Two books (Greek, English) for one work, aligned by Whiston number."""
    out = {}
    read_ = {ed: read(work, ed) for ed in EDITIONS}
    greek = {k: t for k, t, _ in read_["niese"]}
    runs = shift_runs([(k, greek[k], t) for k, t, _ in read_["whiston"]
                       if t and greek.get(k) and k[-1] != "arg"])
    if runs:
        raise SystemExit(f"HARD STOP: {work}: Greek and English sit one unit apart in "
                         + "; ".join(f"{'.'.join(f)}-{'.'.join(l)} (English n fits Greek n{s:+d})"
                                     for s, f, l in runs)
                         + ": read both, find the slipped milestones, add a FIXES slide row")
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
                                                    "piece begins, as Perseus keyed it, "
                                                    "corrected by FIXES)"),
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
