#!/usr/bin/env python3
"""
build_topical.py -- four public-domain topical and dictionary books keyed to
KJV verse ids, and Hitchcock's names joined to their entries.

    python3 pipeline/build_topical.py --fetch    # CCEL's four texts + the scans' OCR, sha256-pinned (~60 MB)
    python3 pipeline/build_topical.py            # -> data/topical/*.jsonl + manifest.json, build/topical/
    python3 pipeline/build_topical.py --check    # rebuild in memory: byte-identical to the committed files

THE BOOKS. Nave's Topical Bible (1896), Torrey's New Topical Text Book
(1897), Easton's Bible Dictionary (1893/1897) and Smith's Bible Dictionary
(Peloubet's 1884 one-volume revision), all from CCEL's ThML, which tags
every scripture reference with an osisRef.

THREE READINGS OF EVERY REFERENCE. CCEL's tag is one. topical_read.refs(),
which reads the displayed text with no help from the tag, is the second. The
third is print: the archive.org OCR of an open scan of each book (two for
Nave, Torrey and Smith, one for Easton), its references read by the same
reader and ALIGNED in order against the book's (GNU diff), so a reference
counts as printed only where it falls in the same run of the same entry.

A reference is committed when two of the three agree: CCEL's tag and the
reader both (the common case), or either one and print. One alone is not
committed; it is listed in build/topical/<work>.rejected.jsonl. Then it
must name a KJV verse or chapter (data/uids' kjv: ids); one that does not
is dropped and counted. A reference to the Apocrypha is kept as the source
gave it, under `apocrypha`, never as a kjv: id.

WHAT IS COMMITTED. Headings and references: an entry's term, Nave's and
Torrey's subtopic outline, and the kjv: ids. The dictionaries' prose
(Easton, Smith) and the scans are not committed; build/topical/ holds the
prose for local use. Nothing is minted.

HITCHCOCK has no scripture references (0 in CCEL's file); his 2,623 names
are already pinned by proper_names.py. Each entry here whose term is a
Hitchcock headword, letter for letter, carries his entry id, so a verse
reaches a name's meaning through the entry that cites it.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import topical_read as R  # noqa: E402
import tsk_read as T  # noqa: E402

CORPUS = os.path.join(ROOT, "data", "corpus", "topical")
OUT = os.path.join(ROOT, "data", "topical")
BUILD = os.path.join(ROOT, "build", "topical")
MANIFEST = os.path.join(OUT, "manifest.json")
CCEL = "https://ccel.org/ccel/"
IA = "https://archive.org/download/"

WORKS = {
    "nave": {
        "title": "Nave's Topical Bible",
        "author": "Orville J. Nave",
        "printed": "Nave's Topical Bible: a digest of the Holy Scriptures (Lincoln, Neb.: Topical Bible Pub. Co., 1896/97)",
        "kind": "topical",
        "ccel": ("n/nave/bible.xml", "dc58dd4e37d5af639f508a4c64657b40f5ccbe727f523b219ffaa70d661f619d"),
        "ccel_rights": "CCEL's file names no rights (DC.Rights empty); Nave died 1917 and the book was printed 1896/97. "
                       "Its header's comment '(tr. William Whiston)' is a stray CCEL template line, not about this book.",
        "scans": [
            ("navestopicalbibl0000orvi_h3u8", "b55be0680b2c73efef3b55736a8699d8a2ec2098fcfc914b71ae4e0e493e53b0", "1897, tesseract 5.3"),
            ("navestopicalbibl00nave", "bbeb8e55db8f637248350720c9b4658aefaf2b1f52ed93e67dcdd46b58feb7ee", "1903, ABBYY 8; NOT_IN_COPYRIGHT"),
        ],
    },
    "torrey": {
        "title": "Torrey's New Topical Textbook",
        "author": "R. A. Torrey",
        "printed": "The New Topical Text Book (New York, Chicago: Fleming H. Revell, 1897)",
        "kind": "topical",
        "ccel": ("t/torrey/ttt.xml", "e49a064b857b186c7250084a43b58afd5972c2dcba5869738e515d001968064b"),
        "ccel_rights": "CCEL's file names no rights (DC.Rights empty); the book was printed 1897.",
        "scans": [
            ("newtopicaltextbo00torr", "4cca7862ec3678c18277a2730d9f8337b41eeb298bc668e4c41c03b7eac86fb5", "1897 Revell; NOT_IN_COPYRIGHT"),
            ("newtopicaltextbo0000revr", "31555240fb82c51b046deca0f30b7848103b32fb1d6887347bd146dfdd0ca369", "1897 Revell, tesseract 5.3"),
        ],
    },
    "easton": {
        "title": "Easton's Bible Dictionary",
        "author": "M. G. Easton",
        "printed": "Illustrated Bible Dictionary (London: T. Nelson, 1893; 3rd ed. 1897), per CCEL's printSourceInfo 1897",
        "kind": "dictionary",
        "ccel": ("e/easton/ebd2.xml", "10e3f432e38ee8197c30a613576dc363af3f29fa4aa90ebd0782533df906e5f1"),
        "ccel_rights": "CCEL's file: DC.Rights 'Public Domain'; printSourceInfo 1897.",
        "scans": [
            ("illustratedbible00east", "d4d476abd109ffe86ad318e33f26201f21591ade74643968c41ad49424e1870f",
             "1893 first edition (N.Y.), ABBYY 8; the only open scan, and an earlier edition than CCEL's 1897"),
        ],
    },
    "smith": {
        "title": "Smith's Bible Dictionary",
        "author": "William Smith; revised and edited by F. N. and M. A. Peloubet",
        "printed": "A Dictionary of the Bible ... revised and edited by F. N. and M. A. Peloubet (Philadelphia: "
                   "Porter and Coates, 1884): the one-volume Sunday-school revision, NOT the 1860-63 three-volume work",
        "kind": "dictionary",
        "ccel": ("s/smith_w/bibledict.xml", "f0aa85b544f70384e24715dcb172ea0b687f8d5646994335e84c8dc44e5aca43"),
        "ccel_rights": "CCEL's file: DC.Rights 'Public Domain'; printSourceInfo 1884.",
        "scans": [
            ("dictionaryofbibl00smit_0", "2b5790a3b6d0ddbd0c5433eb5b4e448adcc28d1dc63aa3857cded37b5d1a29df",
             "1884 Porter and Coates (Peloubet), ABBYY 9; the edition CCEL's text is"),
        ],
    },
}
# Tried and not used: dictionaryofbibl0000smit_e6o5 (1880, the larger Smith):
# it cites in Roman chapters ("Gen. iv. 2"), and 179 references read from it,
# so it is not the edition CCEL keyed and cannot check it.

RIGHTS = {
    "license": "public-domain",
    "basis": "printed 1884-1897 in the United States; every author died before 1931",
    "committed": "headings, the subtopic outline and verse references only; the dictionaries' prose stays in build/",
    "redistribute_whole": True,
}


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _get(url, path, want):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print(f"  fetch {url}")
        with urllib.request.urlopen(url, timeout=300) as r:
            blob = r.read()
        with open(path + ".tmp", "wb") as f:
            f.write(blob)
        os.replace(path + ".tmp", path)
    got = sha(path)
    if got != want:
        raise SystemExit(f"HARD STOP: {path} sha256 {got} != pinned {want}")


def ccel_path(work):
    return os.path.join(CORPUS, work + ".xml")


def scan_path(ident):
    return os.path.join(CORPUS, "scans", ident + ".txt")


def fetch():
    for w, d in WORKS.items():
        rel, want = d["ccel"]
        _get(CCEL + rel, ccel_path(w), want)
        for ident, want_s, _ in d["scans"]:
            _get(f"{IA}{ident}/{ident}_djvu.txt", scan_path(ident), want_s)


def verify():
    for w, d in WORKS.items():
        p = ccel_path(w)
        if not os.path.exists(p):
            raise SystemExit(f"{p} missing: run build_topical.py --fetch")
        if sha(p) != d["ccel"][1]:
            raise SystemExit(f"HARD STOP: {p} changed upstream (sha256 mismatch)")
        for ident, want, _ in d["scans"]:
            if not os.path.exists(scan_path(ident)) or sha(scan_path(ident)) != want:
                raise SystemExit(f"{scan_path(ident)} missing or changed: run build_topical.py --fetch")


# ---------------------------------------------------------------- the vote
def key(t):
    return "%s %s %s" % (t[0], t[1], t[2])


def aligned(a, b):
    """Indices of a that GNU diff matches against b, in order."""
    with tempfile.TemporaryDirectory() as d:
        pa, pb = os.path.join(d, "a"), os.path.join(d, "b")
        with open(pa, "w") as f:
            f.write("\n".join(a) + "\n")
        with open(pb, "w") as f:
            f.write("\n".join(b) + "\n")
        out = subprocess.run(["diff", "-d", "--unchanged-line-format=S%dn\n", "--old-line-format=O%dn\n",
                              "--new-line-format=", pa, pb], capture_output=True, text=True).stdout
    return {int(x[1:]) - 1 for x in out.split() if x.startswith("S")}


def candidates(para, here=None):
    """One paragraph's references, each with who read it:
    [{"t": (book, c, v, c2, v2), "ccel": bool, "reader": bool}] in reading order."""
    tags = []
    for t in para["tagged"]:
        for o in t["osis"].split(" Bible:"):
            q = R.osis_parts(o)
            tags.append(q if q else ("?", o, None, None, None))
    mine = [(r["book"], r["c"], r["v"], r["c2"], r["v2"]) for r in R.refs(para["text"], here=here)]
    out = []
    left = collections.Counter(x[:3] for x in tags)
    first = {}
    for q in tags:
        first.setdefault(q[:3], q)
    for q in mine:
        if left[q[:3]] > 0:
            left[q[:3]] -= 1
            out.append({"t": first[q[:3]], "ccel": True, "reader": True})
        else:
            out.append({"t": q, "ccel": False, "reader": True})
    for q in tags:
        if left[q[:3]] > 0:
            left[q[:3]] -= 1
            out.append({"t": q, "ccel": True, "reader": False})
    return out


def kjv_id(t, shape, books):
    """(book, c, v, c2, v2) -> "kjv:..." or (None, why)."""
    b, c, v, c2, v2 = t
    if (b == "Esth" and (c > 10 or (c == 10 and (v or 0) > 3))) or (b == "Dan" and c in (13, 14)):
        return None, "apocrypha"      # the Greek additions, in the Vulgate's numbering
    if b not in shape:
        return None, ("apocrypha" if b in books else "not a book")
    ch = shape[b]
    if c not in ch or c2 not in ch or (c2, v2 or 0) < (c, v or 0):
        return None, "no such chapter"
    if v is None:
        v = 1
    if v2 is None:
        v2 = ch[c2]
    if v < 1 or v2 < 1 or v > ch[c] or v2 > ch[c2] or (c2, v2) < (c, v):
        return None, "no such verse"
    return T.ref_id((b, c, v, c2, v2)), None


APOCRYPHA = {"Tob", "Jdt", "Wis", "Sir", "Bar", "1Macc", "2Macc", "3Macc", "4Macc", "1Esd", "2Esd",
             "PrAzar", "PrMan", "Sus", "Bel", "AddEsth", "EpJer", "3Esd", "4Esd"}


WORD = re.compile(r"[a-z]{3,}")


def slug(term):
    s = re.sub(r"[^a-z0-9]+", "-", R.plain(term).lower().replace("’", "").replace("'", "")).strip("-")
    return s or "x"


def heading(text):
    """A subtopic's own words: the text before its first reference, less Nave's
    "–"/"." outline marks and Torrey's " — "."""
    rs = R.refs(text)
    h = text[:rs[0]["at"]] if rs else text
    h = h.strip().lstrip("–-.").strip()
    h = re.sub(r"\s*[—\-:,;]+\s*$", "", h).strip()
    return h.rstrip(".").strip() if h.endswith(". ") else h


def build_work(work, shape, hitch):
    d = WORKS[work]
    entries = R.ccel_entries(ccel_path(work))
    cands = []          # (entry index, para index, cand)
    for ei, e in enumerate(entries):
        for pi, p in enumerate(e["paras"]):
            for c in candidates(p):
                cands.append((ei, pi, c))
    seq = [key(c["t"]) for _, _, c in cands]
    printed = collections.Counter()
    scan_stats = []
    vocab = set()
    for ident, _, what in d["scans"]:
        with open(scan_path(ident), encoding="utf-8", errors="replace") as f:
            stext = f.read()
        vocab |= set(WORD.findall(stext.lower()))
        srefs = [key((r["book"], r["c"], r["v"])) for r in R.refs(stext)]
        m = aligned(seq, srefs)
        for i in m:
            printed[i] += 1
        scan_stats.append({"scan": ident, "what": what, "refs_read": len(srefs), "aligned": len(m)})

    counts = collections.Counter()
    by_class = collections.defaultdict(lambda: [0, 0])     # class -> [n, printed]
    kept = collections.defaultdict(list)                    # (ei, pi) -> [kjv ids]
    shown = collections.defaultdict(set)                    # (ei, pi) -> kjv ids found in print
    apoc = collections.defaultdict(list)
    rejected = []
    for i, (ei, pi, c) in enumerate(cands):
        cls = "both" if c["ccel"] and c["reader"] else ("ccel-only" if c["ccel"] else "reader-only")
        by_class[cls][0] += 1
        by_class[cls][1] += bool(printed[i])
        if not (cls == "both" or printed[i]):
            counts["one reading, not printed"] += 1
            rejected.append({"term": entries[ei]["term"], "ref": list(c["t"]), "class": cls,
                             "text": entries[ei]["paras"][pi]["text"][:300]})
            continue
        if c["t"][0] == "?":
            counts["unreadable tag"] += 1
            continue
        rid, why = kjv_id(c["t"], shape, APOCRYPHA)
        if rid is None:
            if why == "apocrypha":
                b0, c0, v0 = c["t"][:3]
                if b0 in ("Esth", "Dan"):
                    b0 = {"Esth": "AddEsth", "Dan": "AddDan"}[b0] + "(vulgate:" + c["t"][0]
                    a_id = "%s.%s%s)" % (b0, c0, ".%s" % v0 if v0 else "")
                else:
                    a_id = "%s.%s%s" % (b0, c0, ".%s" % v0 if v0 else "")
                if a_id not in apoc[(ei, pi)]:
                    apoc[(ei, pi)].append(a_id)
                counts["apocrypha"] += 1
            else:
                counts["names no KJV verse"] += 1
                rejected.append({"term": entries[ei]["term"], "ref": list(c["t"]), "class": cls, "why": why,
                                 "text": entries[ei]["paras"][pi]["text"][:300]})
            continue
        if printed[i]:
            shown[(ei, pi)].add(rid)
        if rid not in kept[(ei, pi)]:
            kept[(ei, pi)].append(rid)
            counts["committed"] += 1
            counts["committed, printed"] += bool(printed[i])
        else:
            counts["repeat in one paragraph"] += 1

    rows, prose = [], []
    seen = collections.Counter()
    for ei, e in enumerate(entries):
        base = slug(e["term"])
        seen[base] += 1
        uid = f"{work}:{base}" if seen[base] == 1 else f"{work}:{base}~{seen[base]}"
        row = {"id": uid, "term": e["term"]}
        hk = hitch.get(re.sub(r"[^a-z]", "", e["term"].lower()))
        if d["kind"] == "topical":
            odd = sorted({x for x in WORD.findall(e["term"].lower()) if x not in vocab})
            if odd:
                row["wording_not_in_print"] = odd
            topics, stack = [], []
            for pi, p in enumerate(e["paras"]):
                h = heading(p["text"])
                stack = (stack + [""] * p["depth"])[:p["depth"]] + [h]
                if kept[(ei, pi)] or apoc[(ei, pi)]:
                    t = {"path": [x for x in stack[1:] if x] if work == "nave" else [x for x in stack if x],
                         "refs": kept[(ei, pi)], "in_print": len(shown[(ei, pi)])}
                    odd = sorted({x for h in t["path"] for x in WORD.findall(h.lower()) if x not in vocab})
                    if odd:
                        t["wording_not_in_print"] = odd
                    if apoc[(ei, pi)]:
                        t["apocrypha"] = apoc[(ei, pi)]
                    topics.append(t)
                see = re.match(r"^[–.\s]*See\s+(.+)$", p["text"])
                if see and not kept[(ei, pi)]:
                    row.setdefault("see", []).append(see.group(1).strip())
            row["topics"] = topics
        else:
            refs, ap, pr = [], [], set()
            for pi in range(len(e["paras"])):
                pr |= shown[(ei, pi)]
                refs += [r for r in kept[(ei, pi)] if r not in refs]
                ap += [r for r in apoc[(ei, pi)] if r not in ap]
            row["refs"] = refs
            row["in_print"] = len(pr & set(refs))
            if ap:
                row["apocrypha"] = ap
            prose.append({"id": uid, "term": e["term"], "text": "\n\n".join(p["text"] for p in e["paras"])})
        if hk:
            row["hitchcock"] = hk
        rows.append(row)
    counts["refs_in_rows"] = sum(len(t["refs"]) for r in rows for t in (r["topics"] if "topics" in r else [r]))
    counts["entries"] = len(entries)
    counts["entries_with_refs"] = sum(1 for r in rows if r.get("refs") or any(t["refs"] for t in r.get("topics", [])))
    counts["hitchcock_joined"] = sum(1 for r in rows if "hitchcock" in r)
    if d["kind"] == "topical":
        tops = [t for r in rows for t in r["topics"]]
        counts["topics"] = len(tops)
        counts["topics_none_in_print"] = sum(1 for t in tops if t["in_print"] == 0)
        counts["headings_with_wording_not_in_print"] = sum(1 for t in tops if "wording_not_in_print" in t) + \
            sum(1 for r in rows if "wording_not_in_print" in r)
    measure = {cls: {"refs": n, "printed": p, "share_printed": round(p / n, 4) if n else None}
               for cls, (n, p) in sorted(by_class.items())}
    return rows, prose, rejected, dict(sorted(counts.items())), measure, scan_stats


def hitchcock_index():
    import proper_names as P
    try:
        P.verify_hitchcock()
    except SystemExit:
        P.fetch_hitchcock()
    idx = {}
    for h in P.read_hitchcock():
        idx.setdefault(re.sub(r"[^a-z]", "", h["term"].lower()), h["id"])
    return idx


def dumps(rows):
    return "".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows)


def build(write=True):
    verify()
    shape = T.kjv_shape()
    hitch = hitchcock_index()
    files, manifest_layers = {}, {}
    for w, d in WORKS.items():
        print(f"{w}: reading and voting")
        rows, prose, rejected, counts, measure, scans = build_work(w, shape, hitch)
        files[f"{w}.jsonl"] = dumps(rows)
        manifest_layers[w] = {
            "file": f"data/topical/{w}.jsonl",
            "sha256": hashlib.sha256(files[f"{w}.jsonl"].encode()).hexdigest(),
            "rows": len(rows),
            "counts": counts,
            "by_reading": measure,
            "scans": scans,
            "source": {"title": d["title"], "author": d["author"], "printed": d["printed"],
                       "edition": "Christian Classics Ethereal Library ThML",
                       "url": CCEL + d["ccel"][0], "sha256": d["ccel"][1], "rights_line": d["ccel_rights"]},
        }
        print(f"  {counts}")
        if write:
            os.makedirs(BUILD, exist_ok=True)
            for name, data in ((f"{w}.rejected.jsonl", rejected), (f"{w}.text.jsonl", prose)):
                if not data:
                    continue
                tmp = os.path.join(BUILD, name + ".tmp")
                with open(tmp, "w", encoding="utf-8") as f:
                    f.write(dumps(data))
                os.replace(tmp, os.path.join(BUILD, name))
    manifest = {
        "about": "Topical and dictionary books keyed to KJV verse ids. pipeline/build_topical.py; rules in pipeline/README-topical.md",
        "rights": RIGHTS,
        "hitchcock": "joined by headword, letter for letter; the table is proper_names.py's (pinned there)",
        "layers": manifest_layers,
    }
    files["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    if write:
        os.makedirs(OUT, exist_ok=True)
        for name, data in files.items():
            tmp = os.path.join(OUT, name + ".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(data)
            os.replace(tmp, os.path.join(OUT, name))
        print("wrote " + ", ".join(f"data/topical/{n}" for n in files))
    return files


def check():
    files = build(write=False)
    bad = []
    for name, data in files.items():
        p = os.path.join(OUT, name)
        if not os.path.exists(p) or open(p, encoding="utf-8").read() != data:
            bad.append(name)
    if bad:
        raise SystemExit("check: differs: " + ", ".join(bad))
    print("check: byte-identical")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
        return
    if a.check:
        check()
        return
    build()


if __name__ == "__main__":
    main()
