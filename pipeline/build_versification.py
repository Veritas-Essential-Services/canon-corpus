#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""
build_versification.py -- the Hebrew (BHS) -> KJV verse map for the Old
Testament, so a citation made in Hebrew numbering can land on a kjv: unit id.

    python3 pipeline/build_versification.py --fetch     # pinned inputs -> data/corpus/ (sha256-checked)
    python3 pipeline/build_versification.py             # build, write data/versification/bhs-kjv.json
    python3 pipeline/build_versification.py --check     # rebuild; byte-identical, every invariant holds
    python3 pipeline/build_versification.py --measure   # which numbering does BDB really cite in?

WHY THIS EXISTS
    BDB cites scripture in Hebrew versification (structure_texts.py, "WHAT IS
    NOT CLAIMED HERE"). Most of the time Hebrew and KJV numbers agree; where
    they don't, a naive reading of "Ps.51.3" opens the wrong verse. Its
    139k citations were recorded as stated and left unresolved until a map
    existed. This is that map.

THE MAP'S SOURCE: STEPBible TVTMS (CC BY 4.0)
    "Translators Versification Traditions with Methodology for
    Standardisation", Tyndale House / STEPBible.org, pinned at commit
    b99716b. Its condensed section aligns, row by row, the English KJV column
    with the traditional Hebrew column. Only those two columns are read, only
    for the 39 OT books, and only the rows where they differ are kept.
    Correspondences between verse numbers are facts, but the licence asks
    for attribution and that the data not be redistributed whole: the TVTMS
    file stays in data/corpus/ (gitignored, like every fetched source) and
    only this derived OT Hebrew->KJV subset, about 2,000 rows, is committed,
    with the attribution and `redistribute_whole: false` in its rights block.
    The changes made to the data (TVTMS asks for a note of them) are stated
    in the output's `source.changes`.

THE CHECK: THE WESTMINSTER LENINGRAD CODEX (PD text)
    The Open Scriptures Hebrew Bible (github.com/openscriptures/morphhb),
    pinned at commit 3d15126, gives the real list of Hebrew verses (WLC 4.20,
    23,213 of them). The build refuses to write unless:
      * every WLC verse lands on a KJV verse in the uid registry (or on a
        psalm title, which the KJV prints with no verse number);
      * every KJV OT verse is reached from some Hebrew verse, except those the
        map itself names as having no Hebrew verse of their own;
      * no Hebrew verse is given two different targets by TVTMS.
    The WLC lemmas (CC BY 4.0, OSHB) are read only by --measure and never
    written anywhere.

WHAT THE MAP SAYS, AND WHAT IT DOES NOT
    `map` lists only the Hebrew verses whose KJV number differs. A Hebrew
    verse not in it has the same number in the KJV. A value is one KJV
    reference, or a list when one Hebrew verse holds the text of two KJV
    verses (Isa 63:19 = KJV 63:19 + 64:1). `hebrew_chapters` gives the WLC's
    verse count per chapter, so a reference that is no Hebrew verse at all is
    caught rather than passed through. A target "Ps.51.title" means the
    KJV's unnumbered superscription: the KJV has no unit id for it, so a
    citation that lands there is NOT resolved, and says why.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(ROOT, "data", "corpus")
OUT = os.path.join(ROOT, "data", "versification", "bhs-kjv.json")
REGISTRY = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")

TVTMS_COMMIT = "b99716b0cddb648ddb95cc786a197180f2f97d48"
TVTMS_NAME = ("TVTMS - Translators Versification Traditions with Methodology for "
              "Standardisation for Eng+Heb+Lat+Grk+Others - STEPBible.org CC BY.txt")
TVTMS_URL = ("https://raw.githubusercontent.com/STEPBible/STEPBible-Data/"
             f"{TVTMS_COMMIT}/Versification/" + urllib.request.quote(TVTMS_NAME))
TVTMS_SHA256 = "63058e0f20201af4bdaa7d830da5be8f493455d947c5f147d84840b33db9ddf8"
TVTMS_PATH = os.path.join(CORPUS, "versification", "tvtms.txt")

WLC_COMMIT = "3d15126fb1ef74867fc1434be1942e837932691f"
WLC_URL = "https://raw.githubusercontent.com/openscriptures/morphhb/{commit}/wlc/{book}.xml"
WLC_DIR = os.path.join(CORPUS, "wlc", WLC_COMMIT[:7])
# sha256 measured 2026-10-02; a mismatch is a hard stop.
WLC_PINS = {
    "Gen": "0526e5c9a5fb4d907847645f954ed3d1268fa69decbd872056cedd2668d86449",
    "Exod": "04868367cdacb6ccdc61488e923e20f918172042e6437842a0621f63ac5b847f",
    "Lev": "e21e70265c9ef500182f8ccb4f4e1186e5a79e1169d24cef23cc479baf07b191",
    "Num": "02e4febfcc027d10b3e35e4f091eae67a40d26f37b6254faac6b4af053fe4896",
    "Deut": "04f8087442a1e67a631cd70f2ac4e42fe0a780ae132edb165a3a29f3f290358f",
    "Josh": "a066200ab2269c0a86a2e9ba119a3d0fce8c5f7ecc44bb53ec134b83dffc6006",
    "Judg": "3b3a909f04041dbd52dc6b7293a96ce75d94db8a90fdeda878943db7b8fac57f",
    "Ruth": "fb6a2660383c7176941cb87b2be182ef634b66d49d057635869f4d9cb1f0a11e",
    "1Sam": "960432732c22286b82d80b6b25af8d10dc5f2e82a4e5e48b2e3a1b1eea17f3cb",
    "2Sam": "e7793e141ed94eadbd2dfb23936abbb4062e81a7dcd41114a6e36644f50b8333",
    "1Kgs": "832ba10f605dce34c4888ee0a795d91edc2b293391d6ae9c36c36c6350761a3e",
    "2Kgs": "056db5393beaef0a1159d9bcaac7dfd865df9bab2eb240ea90e9fa3f0c0e7449",
    "1Chr": "8b59992b6607c6ca0fc423813be8cc244f011c1da32bc8485c0c0f581a897ed4",
    "2Chr": "507294e8ca0fcf31ec25fe62fa24a7f2581f53116519bf08cfe96ff85e9c99fb",
    "Ezra": "fb28ff697d0ee17eba5b4db47fb7261ee1870cea0d5701bfc77c9e28d4138129",
    "Neh": "be082e95c206469122455b9849d4dd08da50c817732d8198c1beece90402801a",
    "Esth": "f9b5b8adaf504dcac409bb6a27c9328967f47eeb4e920070cd53ef5301299019",
    "Job": "7db3311184122f37a8fd52f3c7c0c4a6d2da7b77ee82f4fdb26bcba9171d297f",
    "Ps": "fe55eef316a65fb0f46d833d526ca2fd722e86ff7339f1a39f0c5b7f9062ced2",
    "Prov": "964f99c00239b53b854c4686c99490c8d1ac7664784a30afdfc23781a3abb161",
    "Eccl": "2dfc858d19048f6479eca33b9fe781c2d7e9059e9ae3ab0b37b802d3afec02bb",
    "Song": "5cd6ae36d32c059aaf794af5a5eaed914ac643486db3e412eb0b969760db82ca",
    "Isa": "0807678de609bdef284bed5400b94ddab570d101b593c7f59ae1939015572fa2",
    "Jer": "1a7ad7bc26a2cae1d3964230e8eb73043bc1f32505cb86cd69a25261dc39f493",
    "Lam": "be68fc6a913313367280c2596e28733ee8cf877c12a65227237733b40d0248c4",
    "Ezek": "90bf8adfa66b2f6695c702263fe668755c99c6afc386202c12de4f704f5d4e46",
    "Dan": "bc69d0fa9708dacb11ea6d587509250bf1bcc1b4343eac2d6e97f8b41518fc0d",
    "Hos": "f38ae44a3a97d142768bd5f4d40e77b69265184f9a5aec9e6af1b9b226e8daae",
    "Joel": "c0fefc6881afe949b023968106cdccc05a690734b8bb6e9aa48914d77e5369af",
    "Amos": "6ad94c6a18076762f1a458720c62156d354e5111ee25719b7792b70792d0084d",
    "Obad": "1e893e552a7ed7e2e6d4048637ff5da8a2853a9e4432f4095cede80b959d850c",
    "Jonah": "1e1afcc3aaba1399d5c884ee106894c6bfca87c8c81fa57783ab75a923eee17d",
    "Mic": "267e111adc1b941e32444816af07aa136ecde02cb315cd42597f78b393e67a01",
    "Nah": "5993b28bdbee3c922e3e93002d343a655493e8bd45e3472f3b62d77beadcb62c",
    "Hab": "2592b212d816775adc8dac46bd0c46263982c308a186dde64dfb8239c57bd2d1",
    "Zeph": "eb5bd2a745fba1ffeed31dfafd834ce7c290929c992390be1a2b9451d22dea2e",
    "Hag": "26ebbae4fe491cf89ce70e1264cbcbf66a562b497cb214b677e67a9a43ad545c",
    "Zech": "2e287c8d0e0abd3bf601eb8ef9b4ee6ca3ae12cf36c0ed1612a7dcca54a2e777",
    "Mal": "1583e6a701406dce7b8c2bf85e3522ec31383756de130685fc7c2eb6df8964b2",
}

# TVTMS book codes (SIL/Paratext) -> the OSIS codes the KJV unit ids use.
TV2OSIS = {
    "Gen": "Gen", "Exo": "Exod", "Lev": "Lev", "Num": "Num", "Deu": "Deut",
    "Jos": "Josh", "Jdg": "Judg", "Rut": "Ruth", "1Sa": "1Sam", "2Sa": "2Sam",
    "1Ki": "1Kgs", "2Ki": "2Kgs", "1Ch": "1Chr", "2Ch": "2Chr", "Ezr": "Ezra",
    "Neh": "Neh", "Est": "Esth", "Job": "Job", "Psa": "Ps", "Pro": "Prov",
    "Ecc": "Eccl", "Sng": "Song", "Isa": "Isa", "Jer": "Jer", "Lam": "Lam",
    "Ezk": "Ezek", "Dan": "Dan", "Hos": "Hos", "Jol": "Joel", "Amo": "Amos",
    "Oba": "Obad", "Jon": "Jonah", "Mic": "Mic", "Nam": "Nah", "Hab": "Hab",
    "Zep": "Zeph", "Hag": "Hag", "Zec": "Zech", "Mal": "Mal",
}
OT = list(TV2OSIS.values())
BOOK_ORDER = {b: i for i, b in enumerate(OT)}

RE_REF = re.compile(r"^([1-3]?[A-Za-z]+)\.(\d+):(\d+|Title)(?:-(\d+))?$")
RE_ABSENT = re.compile(r"^Absent \[=([1-3]?[A-Za-z]+\.\d+:\d+)\]$")


def _stop(msg):
    raise SystemExit(f"HARD STOP: {msg}")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def fetch():
    """Every pinned file not already cached with the right sha256
    (pipeline/pinned_fetch.py: the 39 WLC books come in one shallow git fetch,
    which raw.githubusercontent.com's rate limit does not touch)."""
    import pinned_fetch as F
    ua = "canon-corpus/versification"
    F.fetch("STEPBible/STEPBible-Data", TVTMS_COMMIT,
            [("Versification/" + TVTMS_NAME, TVTMS_PATH, TVTMS_SHA256)], ua=ua)
    F.fetch("openscriptures/morphhb", WLC_COMMIT,
            [(f"wlc/{b}.xml", os.path.join(WLC_DIR, b + ".xml"), want)
             for b, want in WLC_PINS.items()], ua=ua)


def _require_pins():
    bad = [p for p, w in [(TVTMS_PATH, TVTMS_SHA256)] +
           [(os.path.join(WLC_DIR, b + ".xml"), w) for b, w in WLC_PINS.items()]
           if not os.path.exists(p) or sha256(p) != w]
    if bad:
        _stop(f"{len(bad)} pinned input(s) missing or changed, first "
              f"{os.path.relpath(bad[0], ROOT)}. Run --fetch.")


# ---------------------------------------------------------------- TVTMS

def tvtms_rows(path=TVTMS_PATH):
    """(line, type, english_kjv, hebrew) for every live row of the condensed
    section whose block has both an 'English KJV' and a 'Hebrew' column.
    A block names its columns either on its `$Section` line or on a `BIBLES`
    row; lines opening with # are commented out in the source and skipped."""
    lines = open(path, encoding="utf-8-sig").read().split("\n")
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("#DataStart(Condensed)"))
        end = next(i for i, l in enumerate(lines) if i > start and l.startswith("#DataEnd(Condensed)"))
    except StopIteration:
        _stop("TVTMS has no #DataStart(Condensed) ... #DataEnd(Condensed) section")
    cols, out = None, []
    for n, line in enumerate(lines[start + 1:end], start + 2):
        c = [x.strip() for x in line.split("\t")]
        t = c[0]
        if t.startswith("$"):
            cols = [x for x in c[1:] if x] or None
            continue
        if t == "BIBLES":
            cols = [x for x in c[1:] if x]
            continue
        if cols is None or not t or t[0] in "#',>" or "TEST" in t:
            continue
        if "English KJV" not in cols or "Hebrew" not in cols:
            continue
        ie, ih = 1 + cols.index("English KJV"), 1 + cols.index("Hebrew")
        if ih >= len(c) or ie >= len(c):
            continue
        out.append((n, t, c[ie], c[ih]))
    return out


def expand(cell):
    """'Psa.3:2-8' -> [(Ps,3,2)...(Ps,3,8)]; 'Num.25:19; 26:1' -> two refs;
    'Psa.3:Title' -> [(Ps,3,'title')]. None for anything else (NoVerse,
    Absent, LXX subverses): those rows say nothing about Hebrew -> KJV."""
    out, book = [], None
    for part in (p.strip() for p in cell.split(";")):
        if book and re.match(r"^\d+:", part):
            part = f"{book}.{part}"
        m = RE_REF.match(part)
        if not m:
            return None
        b, ch, a, z = m.groups()
        book = b
        if b not in TV2OSIS:
            return None
        if a == "Title":
            out.append(f"{TV2OSIS[b]}.{ch}.title")
            continue
        out += [f"{TV2OSIS[b]}.{ch}.{v}" for v in range(int(a), int(z or a) + 1)]
    return out


def osis_key(ref):
    b, ch, v = ref.split(".")
    return (BOOK_ORDER[b], int(ch), -1 if v == "title" else int(v))


def build_map(rows):
    """Hebrew verse -> KJV verse(s), for every Hebrew verse TVTMS aligns.
    Returns (h2e, kjv_absent): h2e values are lists; kjv_absent holds the
    KJV verses TVTMS marks as having no Hebrew verse of their own."""
    h2e, kjv_absent = {}, {}

    def put(h, e):
        got = h2e.setdefault(h, [])
        if e not in got:
            got.append(e)

    for n, typ, e_cell, h_cell in rows:
        E = expand(e_cell)
        if not E:
            continue
        m = RE_ABSENT.match(h_cell)
        if m:
            # The KJV verse has no Hebrew verse number of its own. For
            # MergedPrevVerse TVTMS names the Hebrew verse that carries its
            # text; that Hebrew verse then spans two KJV verses.
            for e in E:
                kjv_absent[e] = {"tvtms": f"{typ}: Hebrew {h_cell}", "line": n}
            if typ == "MergedPrevVerse":
                (h,) = expand(m.group(1)) or [None]
                if h:
                    for e in E:
                        put(h, e)
                        kjv_absent[e]["text_in_hebrew"] = h
            continue
        H = expand(h_cell)
        if not H:
            continue
        if len(E) == len(H):
            pairs = zip(H, E)
        elif len(E) == 1:
            pairs = [(h, E[0]) for h in H]     # several Hebrew verses, one KJV verse
        else:
            _stop(f"TVTMS line {n}: {e_cell!r} vs {h_cell!r} do not align")
        for h, e in pairs:
            put(h, e)
    for h, es in h2e.items():
        es.sort(key=osis_key)
        # Two targets are allowed only where one is a MergedPrevVerse the
        # Hebrew verse also carries; anything else is a contradiction.
        own = [e for e in es if e not in kjv_absent]
        if len(own) > 1:
            _stop(f"Hebrew {h} has two KJV targets in TVTMS: {own}")
    return h2e, kjv_absent


# ---------------------------------------------------------------- WLC

OSIS_NS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"


def wlc_verses(with_lemmas=False):
    """{osisID: set(Strong's numbers) or None} for every verse of the WLC."""
    out = {}
    for b in OT:
        root = ET.parse(os.path.join(WLC_DIR, b + ".xml")).getroot()
        for v in root.iter(OSIS_NS + "verse"):
            if not with_lemmas:
                out[v.get("osisID")] = None
                continue
            s = set()
            for w in v.iter(OSIS_NS + "w"):
                for part in (w.get("lemma") or "").split("/"):
                    m = re.search(r"(\d+)", part)
                    if m:
                        s.add(int(m.group(1)))
            out[v.get("osisID")] = s
    return out


def kjv_ot_verses():
    uids = json.load(open(REGISTRY, encoding="utf-8"))["uids"]
    return {k[4:] for k in uids if k.startswith("kjv:") and k[4:].split(".")[0] in BOOK_ORDER}


# ---------------------------------------------------------------- build

def build():
    _require_pins()
    h2e, kjv_absent = build_map(tvtms_rows())
    wlc = wlc_verses()
    kjv = kjv_ot_verses()

    # Invariant 1: every Hebrew verse lands on a real KJV verse (or a title).
    reached, nowhere = set(), []
    for h in wlc:
        for e in h2e.get(h, [h]):
            if e.endswith(".title"):
                continue
            if e not in kjv:
                nowhere.append((h, e))
            reached.add(e)
    if nowhere:
        _stop(f"{len(nowhere)} Hebrew verse(s) land on no KJV verse, first {nowhere[:5]}")
    # Invariant 2: every KJV verse is reached, or TVTMS says why not.
    orphans = sorted(kjv - reached - set(kjv_absent), key=osis_key)
    if orphans:
        _stop(f"{len(orphans)} KJV verse(s) reached from no Hebrew verse, first {orphans[:5]}")
    # Invariant 3: the map speaks only of verses the WLC has.
    ghosts = sorted(set(h2e) - set(wlc), key=osis_key)

    diff = {}
    for h in sorted(h2e, key=osis_key):
        if h not in wlc:
            continue
        es = h2e[h]
        if es == [h]:
            continue
        diff[h] = es[0] if len(es) == 1 else es
    absent = {e: kjv_absent[e] for e in sorted(kjv_absent, key=osis_key)
              if e in kjv and e not in reached}
    split = {e: kjv_absent[e]["text_in_hebrew"] for e in sorted(kjv_absent, key=osis_key)
             if "text_in_hebrew" in kjv_absent[e]}
    # The Hebrew verse count of every chapter (PD WLC facts): a reference
    # outside these is not a Hebrew verse at all, whatever the KJV has there.
    chapters = {}
    for h in sorted(wlc, key=osis_key):
        b, ch, v = h.split(".")
        chapters[f"{b}.{ch}"] = max(chapters.get(f"{b}.{ch}", 0), int(v))
    if sum(chapters.values()) != len(wlc):
        _stop("WLC verse numbers are not 1..n in every chapter")
    titles = sum(1 for v in diff.values() for e in ([v] if isinstance(v, str) else v)
                 if e.endswith(".title"))

    return {
        "note": ("Hebrew (BHS/WLC) -> KJV verse numbers for the Old Testament. Only the "
                 "Hebrew verses whose KJV number differs are listed; any other Hebrew "
                 "verse has the same number in the KJV. A list value is one Hebrew verse "
                 "holding the text of two KJV verses. A '.title' target is the KJV's "
                 "unnumbered psalm superscription, which has no kjv: unit id. "
                 "hebrew_chapters is the WLC's verse count per chapter. Built by "
                 "pipeline/build_versification.py; do not hand-edit."),
        "from": "bhs", "to": "kjv",
        "source": {
            "name": "TVTMS - Translators Versification Traditions with Methodology for "
                    "Standardisation (STEPBible.org)",
            "url": "https://github.com/STEPBible/STEPBible-Data",
            "commit": TVTMS_COMMIT, "sha256": TVTMS_SHA256,
            "columns_read": ["English KJV", "Hebrew"],
            "changes": ("Reformatted: only the condensed section's 'English KJV' and "
                        "'Hebrew' columns are read, for the 39 OT books; rows where the "
                        "two agree are dropped; TVTMS book codes become OSIS; verse "
                        "ranges are expanded to single verses. No correspondence is "
                        "added or altered."),
        },
        "rights": {
            "license": "CC BY 4.0",
            "attribution": ("Data created by www.STEPBible.org based on work at Tyndale "
                            "House Cambridge (CC BY 4.0)"),
            "source_url": "https://github.com/STEPBible/STEPBible-Data",
            "redistribute_whole": False,
        },
        "checked_against": {
            "name": "Westminster Leningrad Codex 4.20, via the Open Scriptures Hebrew Bible",
            "url": "https://github.com/openscriptures/morphhb", "commit": WLC_COMMIT,
            "text_license": "Public Domain (WLC); lemmas and morphology CC BY 4.0 (OSHB)",
            "wlc_verses": len(wlc), "kjv_ot_verses": len(kjv),
            "wlc_verses_landing_on_no_kjv_verse": 0,
            "kjv_verses_reached_from_no_hebrew_verse": len(absent),
            "map_rows_for_verses_the_wlc_lacks": len(ghosts),
        },
        "counts": {"differing_hebrew_verses": len(diff), "to_psalm_titles": titles,
                   "spanning_two_kjv_verses": sum(isinstance(v, list) for v in diff.values())},
        "hebrew_chapters": chapters,
        "kjv_split_from_previous_hebrew_verse": split,
        "kjv_without_hebrew_verse": {e: v["tvtms"] for e, v in absent.items()},
        "map": diff,
    }


def render(doc):
    return (json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


# ---------------------------------------------------------------- measure

def measure():
    """BDB's citations in the chapters where Hebrew and KJV numbers differ:
    is the entry's own Strong's number in the WLC verse the citation names
    (Hebrew numbering) or in the verse the same numbers name in the KJV?"""
    sys.path.insert(0, HERE)
    import csv
    import structure_texts as S
    import versification as V
    _require_pins()
    bdb = os.path.join(CORPUS, "lexicons", "bdb-hebrew.tsv")
    if not os.path.exists(bdb):
        _stop("data/corpus/lexicons/bdb-hebrew.tsv missing; run pipeline/fetch_sources.py")
    wlc = wlc_verses(with_lemmas=True)
    m = V.load()
    kjv2heb = {}
    for h in wlc:
        for e in V.targets(h, m):
            kjv2heb.setdefault(e, []).append(h)
    csv.field_size_limit(1 << 27)
    n = with_strongs = bhs_hit = kjv_hit = 0
    for row in csv.reader(open(bdb, encoding="utf-8", errors="replace", newline=""), delimiter="\t"):
        if len(row) < 3:
            continue
        strong = int(re.sub(r"\D", "", row[1]) or 0)
        for b, c, v, _label in S.RE_BDB_REF.findall(row[2]):
            osis = S.BOOKNUM2OSIS.get(int(b))
            key = f"{osis}.{c}.{v}"
            if osis not in BOOK_ORDER or key not in m["map"]:
                continue
            n += 1
            if not strong:
                continue
            with_strongs += 1
            bhs_hit += strong in wlc.get(key, ())
            kjv_hit += any(strong in wlc[h] for h in kjv2heb.get(key, []))
    print(f"BDB citations in verses whose Hebrew and KJV numbers differ: {n:,}")
    print(f"  from entries with a Strong's number: {with_strongs:,}")
    print(f"  the entry's word is in the verse, read as Hebrew numbering: "
          f"{bhs_hit:,} ({bhs_hit / with_strongs:.1%})")
    print(f"  the entry's word is in the verse, read as KJV numbering:    "
          f"{kjv_hit:,} ({kjv_hit / with_strongs:.1%})")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--measure", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
        return
    if a.measure:
        measure()
        return
    blob = render(build())
    if a.check:
        if not os.path.exists(OUT):
            _stop(f"{os.path.relpath(OUT, ROOT)} missing")
        if open(OUT, "rb").read() != blob:
            _stop(f"{os.path.relpath(OUT, ROOT)} differs from a rebuild")
        print(f"OK: {os.path.relpath(OUT, ROOT)} byte-identical; every invariant holds")
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT + ".tmp", "wb") as f:
        f.write(blob)
    os.replace(OUT + ".tmp", OUT)
    doc = json.loads(blob)
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {doc['counts']}")


if __name__ == "__main__":
    main()
