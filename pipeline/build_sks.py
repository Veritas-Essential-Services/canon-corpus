#!/usr/bin/env python3
"""Kierkegaard in Danish: Søren Kierkegaards Skrifter (SKS), vols 1-16, from
the Royal Danish Library's TEI (github.com/kb-dk/SKS_tei, CC0 1.0), pinned to
a commit and to each file's sha256 (pipeline/sks_pins.json).

    python3 pipeline/build_sks.py --fetch   # the pinned txt.xml files -> data/corpus/sks/
    python3 pipeline/build_sks.py           # -> data/books/sks-<code>.json + manifest entries
    python3 pipeline/build_sks.py --check   # rebuild = the committed manifest entries
    python3 pipeline/build_sks.py --pin     # (maintainer) record sha256 of the fetched files

What is taken: each work's main text (txt.xml). Kierkegaard's own footnotes
ride on the unit that anchors them (`notes`), never in `text`. Not taken: the
SKS editors' commentary (kom.xml) and textual account (txr.xml); the journals
and papers (SKS 17-27) and letters (SKS 28), a later wave.

Reading of record: the SKS text as its editors print it. In the TEI that means
<app> -> <lem> (variants dropped, counted), <choice> -> the printed form
(<reg> over the first edition's misprint <orig>, kept as `sic`; <abbr> over the
editors' <expan>; <corr> over <sic>), <add> kept and <del> dropped (the
posthumous manuscripts in SKS 15-16).

Unit: one paragraph (or verse group), cited by the SKS page it begins on:
`sks-kg:23.2` is the second paragraph that begins on SKS 9, page 23; ref
"SKS 9, 23 (KG)". The first edition's page (SV1, which the Hong translations
print in their margins) and the 3rd collected edition's (SV3) ride under
`pages` where the TEI marks them. Kierkegaard scholars cite SKS by volume,
page and line; the TEI carries no line numbers, so the id stops at the
paragraph and the honesty field says so. Mints nothing.
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, "data", "corpus", "sks")
BOOKS = os.path.join(ROOT, "data", "books")
MANIFEST = os.path.join(BOOKS, "manifest.json")
PINS = os.path.join(ROOT, "pipeline", "sks_pins.json")
T = "{http://www.tei-c.org/ns/1.0}"
XID = "{http://www.w3.org/XML/1998/namespace}id"

RIGHTS = {
    "license": "CC0 1.0 (the Royal Danish Library's TEI of Søren Kierkegaards Skrifter); "
               "Kierkegaard's text (d. 1855) is public domain",
    "attribution": "Søren Kierkegaards Skrifter, ed. N. J. Cappelørn, J. Garff, J. Kondrup et al., "
                   "Søren Kierkegaard Forskningscenteret 1997-2013; TEI by Karsten Kynde, "
                   "Det Kgl. Bibliotek (kb-dk/SKS_tei)",
    "source_url": None,  # filled from the pin
    "redistribute_whole": True,
    "note": "The repository's LICENSE is CC0 1.0 and the Royal Library's text portal "
            "(tekster.kb.dk) labels every SKS text 'dedikeret til public domain' with a CC0 "
            "link, asking only that the editors be credited. Each file's own teiHeader still "
            "reads availability status='restricted', 'copyright' (written 2004, before the "
            "CC0 release): recorded here so it is not a surprise. Only the main text is "
            "built; the editors' commentary is not taken.",
}


def load_pins():
    with open(PINS, encoding="utf-8") as f:
        return json.load(f)


def raw_url(pins, code):
    return f"https://raw.githubusercontent.com/{pins['repo']}/{pins['commit']}/data/v1.9/{code}/txt.xml"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_atomic(path, data):
    with open(path + ".tmp", "wb") as f:
        f.write(data)
    os.replace(path + ".tmp", path)


def local(code):
    return os.path.join(CORPUS, code + ".txt.xml")


def fetch(pins):
    os.makedirs(CORPUS, exist_ok=True)
    for code in pins["works"]:
        p = local(code)
        want = pins["sha256"].get(code)
        if os.path.exists(p) and want and sha256_file(p) == want:
            continue
        with urllib.request.urlopen(raw_url(pins, code), timeout=120) as r:
            data = r.read()
        got = hashlib.sha256(data).hexdigest()
        if want and got != want:
            write_atomic(p + ".refused", data)
            raise SystemExit(f"REFUSED {code}: sha256 {got} != pinned {want}")
        write_atomic(p, data)
        print(f"  fetched {code} ({len(data):,} bytes)")


def verify_pins(pins):
    bad = [c for c in pins["works"] if not os.path.exists(local(c))
           or sha256_file(local(c)) != pins["sha256"].get(c)]
    if bad:
        raise SystemExit(f"missing or changed sources (run --fetch): {bad}")


# ---------------------------------------------------------------- text

SKIP = {"note", "rdg", "rdgGrp", "witDetail", "expan", "orig", "sic", "del", "figure",
        "figDesc", "graphic", "ptr", "witStart", "witEnd"}


class Walker:
    """Walks the body in document order, tracking the editions' pages."""

    def __init__(self, notes=None):
        self.notes = notes or {}
        self.page = {"sks": None, "sv1": None, "sv2": None, "sv3": None}
        self.stats = {"variants_dropped": 0, "misprints_emended": 0, "deletions_dropped": 0,
                      "notes": 0}

    def pb(self, e):
        ed = (e.get("edRef") or "").lstrip("#").lower()
        if ed in ("sks", "sv1", "sv2", "sv3"):
            self.page[ed] = e.get("n")

    def text(self, e, out, notes, start):
        """Append e's printed text to out; Kierkegaard's notes go to notes.
        start[0] is set to a snapshot of the pages at the first character."""
        tag = e.tag.replace(T, "")
        if tag == "pb":
            self.pb(e)
        elif tag == "ptr" and e.get("type") == "author":
            nid = (e.get("target") or "").lstrip("#")
            if nid in self.notes:
                notes.append({"id": nid, "text": self.notes[nid]})
                self.stats["notes"] += 1
            else:
                self.stats["notes_unresolved"] = self.stats.get("notes_unresolved", 0) + 1
        elif tag == "choice":
            kids = {k.tag.replace(T, ""): k for k in e}
            for pref in ("reg", "corr", "abbr", "lem", "seg"):
                if pref in kids:
                    if pref in ("reg", "corr") and ("orig" in kids or "sic" in kids):
                        self.stats["misprints_emended"] += 1
                    self.inner(kids[pref], out, notes, start)
                    break
            else:
                if len(e):
                    self.inner(e[0], out, notes, start)
        elif tag == "app":
            for k in e:
                kt = k.tag.replace(T, "")
                if kt == "lem":
                    self.inner(k, out, notes, start)
                elif kt in ("rdg", "rdgGrp"):
                    self.stats["variants_dropped"] += 1
                    self.skip_pbs(k)
        elif tag in SKIP:
            if tag == "del":
                self.stats["deletions_dropped"] += 1
            self.skip_pbs(e)
        elif tag == "head" and e.get("type") == "topText":
            pass
        else:
            if tag == "l" and out and not out[-1].endswith(" / "):
                if "".join(out).strip():
                    out.append(" / ")
            if tag == "cell" and out and "".join(out).strip():
                out.append(" | ")
            self.inner(e, out, notes, start)
            if tag in ("row",):
                out.append(" ")
        if e.tail:
            self.emit(e.tail, out, start)

    def inner(self, e, out, notes, start):
        if e.text:
            self.emit(e.text, out, start)
        for k in e:
            self.text(k, out, notes, start)

    def emit(self, s, out, start):
        if start[0] is None and s.strip():
            start[0] = dict(self.page)
        out.append(s)

    def skip_pbs(self, e):
        # a page break inside dropped matter still turns the page
        for k in e.iter(T + "pb"):
            self.pb(k)


def clean(parts):
    s = " ".join("".join(parts).split())
    return s.replace(" / / ", " / ").strip(" /|")


def header(root):
    ts = root.find(f".//{T}titleStmt")
    title = short = None
    for t in ts.findall(T + "title"):
        if t.get("type") == "short":
            short = (t.text or "").strip()
        elif t.get("level") is None and title is None:
            title = (t.text or "").strip()
    vol = root.find(f".//{T}seriesStmt/{T}biblScope[@unit='volume']")
    return title, short, int(vol.text)


def convert(code, pins):
    root = ET.parse(local(code)).getroot()
    title, short, vol = header(root)
    body = root.find(f".//{T}body")
    # Kierkegaard's footnotes stand after the text (<note type="author">), anchored
    # by <ptr type="author" target="#id"/>; read them with their own walker so
    # their page breaks do not move the text's pages.
    nw, notes_by_id = Walker(), {}
    for n in body.iter(T + "note"):
        if n.get("type") == "author":
            buf = []
            nw.inner(n, buf, [], [None])
            notes_by_id[n.get(XID)] = clean(buf)
    w = Walker(notes_by_id)
    units, heads, per_page = [], [], {}
    seen = set()

    def visit(e, depth):
        tag = e.tag.replace(T, "")
        if tag == "pb":
            w.pb(e)
            return
        if tag == "note":
            return
        if tag == "div":
            heads.append(None)
            for k in e:
                visit(k, depth + 1)
            heads.pop()
            return
        if tag == "head":
            if e.get("type") == "topText":
                return
            buf = []
            w.inner(e, buf, [], [None])
            h = clean(buf)
            if h and heads:
                heads[-1] = h if heads[-1] is None else heads[-1] + " " + h
            return
        if tag in ("p", "lg", "table"):
            if e.get("rend") == "decoration":
                w.skip_pbs(e)
                return
            buf, notes, start = [], [], [None]
            w.inner(e, buf, notes, start)
            text = clean(buf)
            if not text:
                return
            pg = start[0] or dict(w.page)
            sks = pg["sks"] or "0"
            per_page[sks] = per_page.get(sks, 0) + 1
            uid = f"sks-{code}:{sks}.{per_page[sks]}"
            assert uid not in seen, uid
            seen.add(uid)
            u = {"id": uid, "ref": f"SKS {vol}, {sks} ({short})", "text": text, "links": [],
                 "pages": {k: v for k, v in pg.items() if v}}
            if w.page["sks"] and w.page["sks"] != sks:
                u["pages"]["sks_end"] = w.page["sks"]
            h = [x for x in heads if x]
            if h:
                u["head"] = h
            if notes:
                u["notes"] = notes
            units.append(u)
            return
        # anything else at block level (milestone, figure, l outside p ...)
        for k in e:
            visit(k, depth)

    for k in body:
        visit(k, 0)
    no_sks = sum(1 for u in units if not u["pages"].get("sks"))
    slug = f"sks-{code}"
    rights = dict(RIGHTS)
    rights["source_url"] = f"https://github.com/{pins['repo']}/tree/{pins['commit']}/data/v1.9/{code}"
    book = {
        "slug": slug,
        "title": f"{title} (Danish, SKS {vol})",
        "author": "Søren Kierkegaard",
        "source": {"path": f"sks/{code}.txt.xml", "format": "tei-sks", "lang": "da",
                   "edition": f"Søren Kierkegaards Skrifter, vol. {vol} (Søren Kierkegaard "
                              "Forskningscenteret, 1997-2013), TEI v1.9",
                   "sha256": pins["sha256"][code]},
        "scheme": {
            "citation": f"SKS {vol}, page (paragraph): sks-{code}:<SKS page>.<nth paragraph beginning on it>",
            "resolution": "paragraph",
            "honesty": "exact to the SKS page each paragraph begins on (the TEI's own page "
                       "breaks); the paragraph number within the page is counted here, not "
                       "printed in SKS. SKS line numbers are not in the TEI, so a line "
                       "citation (SKS 9, 23,12) resolves only to its paragraph."
                       + (f" {no_sks} unit(s) precede the first SKS page mark and are filed "
                          "under page 0." if no_sks else ""),
            "note": "Kierkegaard's footnotes ride in `notes`, never in `text`. Variant "
                    "readings, the editors' expansions and the first edition's misprints are "
                    "left out of `text` (counted in `stats`). `pages.sv1` is the first "
                    "edition's page where the TEI marks it (the Hongs' margins).",
            "stats": dict(w.stats, notes_in_file=len(notes_by_id)),
        },
        "rights": rights,
        "units": units,
    }
    return book


def entry(book, blob):
    return {"title": book["title"], "author": book["author"], "format": book["source"]["format"],
            "sha256": book["source"]["sha256"], "units": len(book["units"]),
            "scheme": book["scheme"], "rights": book["rights"],
            "built_sha256": hashlib.sha256(blob).hexdigest()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--pin", action="store_true")
    a = ap.parse_args()
    pins = load_pins()
    if a.pin:
        pins["sha256"] = {c: sha256_file(local(c)) for c in pins["works"]}
        write_atomic(PINS, (json.dumps(pins, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
        print(f"  pinned {len(pins['sha256'])} files")
        return
    if a.fetch:
        fetch(pins)
    verify_pins(pins)
    built = {}
    for code in pins["works"]:
        book = convert(code, pins)
        blob = json.dumps(book, ensure_ascii=False).encode("utf-8")
        built[book["slug"]] = (blob, entry(book, blob))
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    tot = sum(e["units"] for _, e in built.values())
    for slug, (_, e) in built.items():
        print(f"  {slug:<14}{e['units']:>6} units  {e['title']}")
    print(f"  {len(built)} books, {tot:,} units")
    if a.check:
        bad = [s for s, (blob, e) in built.items() if manifest.get(s) != e
               or (os.path.exists(os.path.join(BOOKS, s + ".json"))
                   and open(os.path.join(BOOKS, s + ".json"), "rb").read() != blob)]
        if bad:
            raise SystemExit(f"CHECK FAILED: rebuilt books differ from the manifest: {bad}")
        print("  CHECK PASSED: every book = its committed manifest entry (built_sha256).")
        return
    for slug, (blob, e) in built.items():
        write_atomic(os.path.join(BOOKS, slug + ".json"), blob)
        manifest[slug] = e
    write_atomic(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    print(f"  wrote {len(built)} books + {len(manifest)}-entry manifest")


if __name__ == "__main__":
    sys.exit(main())
