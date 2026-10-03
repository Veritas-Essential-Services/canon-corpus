#!/usr/bin/env python3
"""
build_xrefs.py -- the cross-reference layer: for every KJV verse, the
passages that bear on it, keyed on KJV verse ids (kjv:Book.c.v, the suite's
shared key).

    python3 pipeline/build_xrefs.py --fetch    # the two Treasury scans from archive.org, sha256-pinned (~1.2 GB)
    python3 pipeline/build_xrefs.py            # build everything (resumable; ~10 min the first time)
    python3 pipeline/build_xrefs.py --check    # rebuild data/xrefs/tsk.jsonl in memory: = the committed bytes
    python3 pipeline/build_xrefs.py --train    # relearn the 3/8 glyph model (data/xrefs/glyph-3-8.json)
    python3 pipeline/build_xrefs.py --measure FILE  # score against OpenBible.info's cross_references.txt (CC BY; measuring only)

TWO SOURCES, TWO POSTURES (rule 6):

1. The Treasury of Scripture Knowledge (Bagster; public domain), read from two
   independent archive.org scans (tsk_layout.py, tsk_read.py, tsk_glyphs.py).
   COMMITTED: data/xrefs/tsk.jsonl, one row per verse that has an entry --
   only what both scans attest (README-xrefs.md s.4).
2. Every passage in the built books that cites a verse: the fathers' editors'
   notes (PR #7's build/fathers/scripture-links.jsonl), the catenae placed on
   their verses, and any other book unit whose links name a kjv: verse.
   Those editions are CC BY-SA or carry their own rights, so the index they
   make goes to build/xrefs/cited-by.jsonl (gitignored), like PR #7's links;
   the manifest records its counts and sha256.

Nothing here mints a uid: the layer is keyed on the KJV verse ids that already
exist (data/uids/wordhoard.uids.json is read, never written).
"""
import argparse
import collections
import gzip
import hashlib
import json
import os
import sys
import urllib.request
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tsk_glyphs as G  # noqa: E402
import tsk_layout as L  # noqa: E402
import tsk_read as T  # noqa: E402

CORPUS = os.path.join(ROOT, "data", "corpus", "tsk")
BUILD = os.path.join(ROOT, "build", "xrefs")
DATA = os.path.join(ROOT, "data", "xrefs")
TSK_FILE = os.path.join(DATA, "tsk.jsonl")
MANIFEST = os.path.join(DATA, "manifest.json")
CITED_BY = os.path.join(BUILD, "cited-by.jsonl")
ONE_SCAN = os.path.join(BUILD, "tsk-one-scan.jsonl")

# The two scans. Both are open (not lending-library) archive.org items; the
# other Treasury scans there are lending-only and are not used.
SCANS = {
    "rato": {
        "item": "treasuryofscript0000rato",
        "edition": "Fleming H. Revell / Samuel Bagster (1889 per archive.org), introduction by R. A. Torrey; "
                   "Graduate Theological Union copy",
        "files": {
            "chocr": ("treasuryofscript0000rato_chocr.html.gz",
                      "1f5bca3305f94c9d03d15f0ce621f796a2c3bf8d6114d6f72079e421e59bf5e9"),
            "jp2": ("treasuryofscript0000rato_jp2.zip",
                    "02490bb539e9f53bffe5af0c65e5fa5dbd20d864444974023fbefa75de36fd83"),
        },
    },
    "drra": {
        "item": "treasuryofscript0000drra",
        "edition": "Samuel Bagster and Sons (undated printing of the same plates)",
        "files": {
            "chocr": ("treasuryofscript0000drra_chocr.html.gz",
                      "4aaa77b5e23f1243b61c1ea4764ba94a59da9c9a8ed575127e65eae7bdfdbe70"),
            "jp2": ("treasuryofscript0000drra_jp2.zip",
                    "c781f2ea7d01a07b1656db5ba8d4a0399f5a2fda97e974d781876d69296588a2"),
        },
    },
}
ORDER = ("rato", "drra")      # rato's catchwords and order are used where both have a reference
# PR #7's Old Testament links are under review (2026-10-03: 30 of 64 checked
# were off -- line numbers read as verses, numbering misjudged, "et" and
# dashes misparsed). Until #7 is fixed every fathers-notes citation of an OT
# verse carries "provisional": true; rebuild with the fixed links and drop
# this set.
OT_BOOKS = set(T.ORDER[:39])
NEAR = 6                       # verses apart that a reference may be "the same one, misplaced"

RIGHTS = {
    "tsk": {
        "license": "public-domain",
        "work": "The Treasury of Scripture Knowledge (Samuel Bagster, c. 1830s; R. A. Torrey's "
                "introduction, 1890s). Public domain in the US: published before 1931.",
        "attribution": "Treasury of Scripture Knowledge; scans by the Internet Archive",
        "source_url": "https://archive.org/details/treasuryofscript0000rato",
        "redistribute_whole": True,
        "note": "Only the references and catchwords are taken; the scans' OCR is the Internet "
                "Archive's (tesseract), re-read here. OpenBible.info's cross-reference set "
                "(CC BY) is never an input; it is used only to measure (README-xrefs.md s.6).",
    },
    "cited_by": {
        "license": "mixed: each citing passage keeps its own book's rights block",
        "redistribute_whole": False,
        "note": "Built from editions that are CC BY-SA (First1KGreek, CSEL TEI) or otherwise "
                "licensed; like PR #7's scripture links, rebuilt locally and never committed.",
    },
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- fetch
def fetch():
    os.makedirs(CORPUS, exist_ok=True)
    for tag, s in SCANS.items():
        for _, (name, want) in s["files"].items():
            path = os.path.join(CORPUS, name)
            if os.path.exists(path) and sha256_file(path) == want:
                print(f"  have {name}")
                continue
            url = f"https://archive.org/download/{s['item']}/{name}"
            print(f"  fetching {url}")
            tmp = path + ".tmp"
            req = urllib.request.Request(url, headers={"User-Agent": "canon-corpus/build_xrefs"})
            with urllib.request.urlopen(req, timeout=600) as r, open(tmp, "wb") as f:
                while True:
                    blk = r.read(1 << 20)
                    if not blk:
                        break
                    f.write(blk)
            got = sha256_file(tmp)
            if got != want:
                os.remove(tmp)
                raise SystemExit(f"{name}: sha256 {got} is not the pinned {want}")
            os.replace(tmp, path)


def src_path(tag, kind):
    name, want = SCANS[tag]["files"][kind]
    p = os.path.join(CORPUS, name)
    if not os.path.exists(p):
        raise SystemExit(f"missing {p}: run build_xrefs.py --fetch")
    return p


# ---------------------------------------------------------------- per scan
def code_key(*mods):
    """A short hash of the modules a cached stage depends on: a cache built by
    other code is never read back (so --check is a rebuild, not a re-read)."""
    h = hashlib.sha256()
    for m in mods:
        with open(m.__file__, "rb") as f:
            h.update(f.read())
    return h.hexdigest()[:12]


def layout_path(tag):
    return os.path.join(BUILD, f"{tag}.layout.{code_key(L)}.jsonl.gz")


def stage_layout(tag):
    out = layout_path(tag)
    if not os.path.exists(out):
        print(f"  {tag}: laying out the OCR")
        os.makedirs(BUILD, exist_ok=True)
        L.build(src_path(tag, "chocr"), out)
    return out


def stage_read(tag, shape):
    """Align and read one scan: [(src verse, catchword, ref)] in printed order.
    Each ref keeps the digits as read and the glyph under each digit."""
    lines, heads, npages = L.load_lines(stage_layout(tag), T.parse_head)
    entries, log = T.align(lines, shape, heads, npages)
    reads = []
    for e in entries:
        b, c, v = e["verse"]
        text, glyphs = T.entry_text(lines, e)
        for kw, rs in T.refs(text):
            for r in rs:
                r["digits"] = {f: text[a:z] for f, (a, z) in r["at"].items()}
                r["glyphs"] = {f: [glyphs[i] for i in range(a, z)] for f, (a, z) in r["at"].items()}
                del r["at"]
                reads.append(((b, c, v), kw, r))
    log["heads"] = len(heads)
    log["pages"] = npages
    return entries, reads, log


def glyphs_of(reads):
    out = set()
    for _, _, r in reads:
        for f, gl in r["glyphs"].items():
            for ch, g in zip(r["digits"][f], gl):
                if ch in "38" and g:
                    out.add(tuple(g))
    return out


def _page_job(args):
    zip_path, member, boxes = args
    return G.page_features(zip_path, member, boxes)


def stage_features(tag, reads):
    """{glyph: feature} for every 3/8 in a reference, cached per scan."""
    import numpy as np
    cache = os.path.join(BUILD, f"{tag}.glyphs.{code_key(L, T, G)}.npz")
    if os.path.exists(cache):
        d = np.load(cache)
        return {tuple(int(x) for x in k): f for k, f in zip(d["keys"], d["feats"])}
    print(f"  {tag}: cropping the 3s and 8s from the page images")
    item = SCANS[tag]["item"]
    zp = src_path(tag, "jp2")
    bypage = collections.defaultdict(list)
    for g in sorted(glyphs_of(reads)):
        bypage[g[0]].append(g)
    jobs = [(zp, f"{item}_jp2/{item}_{p:04d}.jp2", bs) for p, bs in sorted(bypage.items())]
    with Pool(max(1, min(4, os.cpu_count() or 1))) as pool:
        res = pool.map(_page_job, jobs, chunksize=4)
    pairs = sorted((tuple(b), f) for r in res for b, f in r if f is not None)
    keys = np.array([k for k, _ in pairs], dtype=np.int64).reshape(-1, 6)
    arr = np.array([f for _, f in pairs], dtype=np.float32).reshape(len(pairs), -1)
    tmp = cache + ".tmp.npz"
    np.savez_compressed(tmp, keys=keys, feats=arr)
    os.replace(tmp, cache)
    return {tuple(int(x) for x in k): f for k, f in zip(keys, arr)}


def weak_labels(reads, shape):
    """{glyph: "3"|"8"} from references with one 3/8 whose reading as printed
    and swapped differ in whether they name a KJV verse (tsk_glyphs.py)."""
    lab = {}
    for (b, c, _v), _kw, r in reads:
        pos = [(f, i, tuple(g)) for f, gl in r["glyphs"].items()
               for i, (ch, g) in enumerate(zip(r["digits"][f], gl)) if ch in "38" and g]
        if len(pos) != 1:
            continue
        f, i, g = pos[0]
        d = r["digits"][f]
        r2 = dict(r)
        r2[f] = int(d[:i] + G.SWAP[d[i]] + d[i + 1:])
        ok, ok2 = bool(T.resolve(r, b, c, shape)), bool(T.resolve(r2, b, c, shape))
        if ok and not ok2:
            lab[g] = d[i]
        elif ok2 and not ok:
            lab[g] = G.SWAP[d[i]]
    return lab


def corrected(reads, p3):
    """Apply the glyph model: each ref gets its digits re-read and a status:
    "as-read" (no 3/8, or every one confirmed), "fixed" (a digit changed),
    "unsure" (a 3/8 the model could not call; the OCR's reading kept)."""
    out = []
    for src, kw, r in reads:
        r = dict(r)
        unsure = fixed = False
        for f, gl in r["glyphs"].items():
            d = list(r["digits"][f])
            for i, (ch, g) in enumerate(zip(d, gl)):
                if ch in "38" and g:
                    p = p3.get(tuple(g))
                    k = G.decide(p) if p is not None else None
                    if k is None:
                        unsure = True
                    elif k != ch:
                        d[i] = k
                        fixed = True
            nd = "".join(d)
            if nd != r["digits"][f]:
                r[f] = int(nd)
        # one digit the model could not call leaves the whole reference
        # unsure, whatever another digit's fix did
        r["status"] = "unsure" if unsure else ("fixed" if fixed else "as-read")
        out.append((src, kw, r))
    return out


# ---------------------------------------------------------------- combine
def combine(per_scan, entries_of, shape):
    """Two scans' resolved references -> (committed rows, one-scan rows, counts).

    AGREED: both scans read the same reference under the same verse.
    PLACED: both read it, under verses at most NEAR apart, and one scan has no
      entry at the later verse while the other has: that scan missed the
      entry line, so its later references ran on under the verse before
      (measured: the later verse is right 84-90% of the time, README s.4).
    Everything else stays one scan's reading and is not committed."""
    V = T.Verses(shape)
    idx = V.index
    sets = {}
    for tag, items in per_scan.items():
        s = collections.defaultdict(list)
        for src, kw, t, st in items:
            s[(src, t)].append((kw, st))
        sets[tag] = s
    a, b = ORDER
    agreed = set(sets[a]) & set(sets[b])
    placed = {}
    moved_from = set()        # (scan, verse, ref): the run-on copy a placement replaces
    placed_from = {}          # (later, ref) -> (scan, verse) of that run-on copy
    for x, y in ((a, b), (b, a)):
        by_target = collections.defaultdict(list)
        for (src, t) in sets[y]:
            if (src, t) not in agreed:
                by_target[t].append(src)
        for (src, t) in sets[x]:
            if (src, t) in agreed:
                continue
            near = [s for s in by_target.get(t, []) if s != src and abs(idx[s] - idx[src]) <= NEAR]
            if not near:
                continue
            other = min(near, key=lambda s: (abs(idx[s] - idx[src]), idx[s]))
            later, earlier = (src, other) if idx[src] > idx[other] else (other, src)
            who_earlier = x if earlier == src else y
            who_later = y if who_earlier == x else x
            if later not in entries_of[who_earlier] and later in entries_of[who_later]:
                placed[(later, t)] = who_later
                placed_from[(later, t)] = (who_earlier, earlier)
                moved_from.add((who_earlier, earlier, t))
    keep = agreed | set(placed)
    # rows, in printed order (scan a first, then anything only b ordered)
    rows = collections.OrderedDict()
    seen = set()
    unsure = set()
    for (src, t) in agreed:
        if all(st == "unsure" for _, st in sets[a][(src, t)]) and all(st == "unsure" for _, st in sets[b][(src, t)]):
            unsure.add((src, t))
    for (src, t), tag in placed.items():
        # a placed reference whose 3/8 neither scan could call is no surer
        # than an agreed one
        tag_e, src_e = placed_from[(src, t)]
        if all(st == "unsure" for _, st in sets[tag][(src, t)]) and \
                all(st == "unsure" for _, st in sets[tag_e][(src_e, t)]):
            unsure.add((src, t))
    for tag in ORDER:
        for src, kw, t, st in per_scan[tag]:
            key = (src, t)
            if key not in keep or key in seen or (key in placed and placed[key] != tag):
                continue
            seen.add(key)
            rows.setdefault(src, []).append((kw, t))
    placed_at = collections.defaultdict(list)
    for (s, t) in placed:
        placed_at[s].append(t)
    unsure_at = collections.defaultdict(list)
    for (s, t) in unsure:
        unsure_at[s].append(t)
    out = []
    for src in sorted(rows, key=lambda s: idx[s]):
        groups = []
        for kw, t in rows[src]:
            rid = T.ref_id(t)
            if groups and (groups[-1]["kw"] == kw or not kw):
                if rid not in groups[-1]["refs"]:
                    groups[-1]["refs"].append(rid)
            else:
                groups.append({"kw": kw, "refs": [rid]})
        row = {"verse": "kjv:%s.%d.%d" % src, "groups": groups}
        pl = sorted(T.ref_id(t) for t in placed_at.get(src, ()))
        if pl:
            row["placed"] = pl
        un = sorted(T.ref_id(t) for t in unsure_at.get(src, ()))
        if un:
            row["unsure_digit"] = un
        out.append(row)
    one = []
    for tag in ORDER:
        for src, kw, t, st in per_scan[tag]:
            if (src, t) not in keep and (tag, src, t) not in moved_from:
                one.append({"verse": "kjv:%s.%d.%d" % src, "scan": tag, "kw": kw,
                            "ref": T.ref_id(t), "glyphs": st})
    counts = {
        "verses_with_entries": len(out),
        "refs": sum(len(g["refs"]) for r in out for g in r["groups"]),
        "agreed": len(agreed),
        "placed": len(placed),
        "unsure_digit": len(unsure),
        "one_scan_not_committed": len(one),
    }
    return out, one, counts


def dumps_rows(rows):
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
                   for r in rows).encode("utf-8")


# ---------------------------------------------------------------- cited by
def cited_by(tsk_rows, shape, books_dir, links_file):
    """{verse: [citation]} from the Treasury (both ways) and the built books."""
    V = T.Verses(shape)
    out = collections.defaultdict(list)
    counts = collections.Counter()

    def verses(rid):
        b, c, v, c2, v2 = T.parse_ref_id(rid)
        i, j = V.index[(b, c, v)], V.index[(b, c2, v2)]
        return ["kjv:%s.%d.%d" % V.seq[k] for k in range(i, j + 1)]

    for row in tsk_rows:
        for g in row["groups"]:
            for rid in g["refs"]:
                for tv in verses(rid):
                    out[tv].append({"by": row["verse"], "source": "tsk", "kw": g["kw"]})
                    counts["tsk"] += 1
    if links_file and os.path.exists(links_file):
        with open(links_file, encoding="utf-8") as f:
            for raw in f:
                row = json.loads(raw)
                for ln in row["links"]:
                    if "target" in ln:
                        c = {"by": row["unit"], "source": "fathers-notes", "rule": ln["rule"], "ref": ln["ref"]}
                        if ln["target"].split(".")[0] in OT_BOOKS:
                            c["provisional"] = True
                            counts["fathers-notes-ot-provisional"] += 1
                        out["kjv:" + ln["target"]].append(c)
                        counts["fathers-notes"] += 1
    if books_dir and os.path.isdir(books_dir):
        for name in sorted(os.listdir(books_dir)):
            if not name.endswith(".json") or name == "manifest.json" or name.startswith("kjv"):
                continue
            with open(os.path.join(books_dir, name), encoding="utf-8") as f:
                book = json.load(f)
            for u in book.get("units", []):
                for ln in u.get("links") or []:
                    t = ln.get("target", "")
                    if ln.get("kind") == "scripture" and t.startswith("kjv:") and t.count(".") == 2:
                        out[t].append({"by": u["id"], "source": "book-links",
                                       "match": ln.get("match")})
                        counts["book-links"] += 1
    return out, counts


# ---------------------------------------------------------------- main
def build(train=False, books_dir=None, links_file=None, write=True):
    import numpy as np
    shape = T.kjv_shape()
    per_reads, per_entries, logs = {}, {}, {}
    for tag in ORDER:
        print(f"{tag}: reading")
        entries, reads, log = stage_read(tag, shape)
        per_reads[tag], logs[tag] = reads, log
        per_entries[tag] = {e["verse"] for e in entries}
        print(f"  {log['entries']} entries, {len(reads)} references")
    feats = {tag: stage_features(tag, per_reads[tag]) for tag in ORDER}
    if train or not os.path.exists(G.MODEL):
        X, Y = [], []
        for tag in ORDER:
            lab = weak_labels(per_reads[tag], shape)
            for g in sorted(lab):
                if g in feats[tag]:
                    X.append(feats[tag][g])
                    Y.append(1.0 if lab[g] == "3" else 0.0)
        d, rep = G.train(X, Y)
        print("  glyph model:", rep)
        os.makedirs(DATA, exist_ok=True)
        tmp = G.MODEL + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(d, f, separators=(",", ":"))
            f.write("\n")
        os.replace(tmp, G.MODEL)
    model = G.Model.load()
    per_scan, scan_counts = {}, {}
    for tag in ORDER:
        keys = list(feats[tag])
        p = dict(zip(keys, model.p3(np.array([feats[tag][k] for k in keys])))) if keys else {}
        reads = corrected(per_reads[tag], p)
        items = []
        c = collections.Counter()
        for src, kw, r in reads:
            cs = T.resolve(r, src[0], src[1], shape)
            c["refs"] += 1
            c["glyphs_" + r["status"]] += 1
            if len(cs) == 1:
                items.append((src, kw, cs[0], r["status"]))
                c["resolved"] += 1
            else:
                c["unresolved" if not cs else "ambiguous_book"] += 1
        per_scan[tag] = items
        scan_counts[tag] = dict(c, **{k: logs[tag][k] for k in ("entries", "headings", "heads", "pages")},
                                entries_by_rule=logs[tag]["by_rule"])
        print(f"  {tag}: {dict(c)}")
    rows, one, counts = combine(per_scan, per_entries, shape)
    blob = dumps_rows(rows)
    print("tsk:", counts)
    if not write:
        return blob, counts
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(BUILD, exist_ok=True)
    for path, data in ((TSK_FILE, blob), (ONE_SCAN, dumps_rows(one))):
        tmp = path + ".tmp"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    cb, cb_counts = cited_by(rows, shape, books_dir, links_file)
    V = T.Verses(shape)
    cb_rows = [{"verse": v, "by": cb[v]}
               for v in sorted(cb, key=lambda s: (V.index.get(T.parse_ref_id(s)[:3], -1), s))]
    cb_blob = dumps_rows(cb_rows)
    tmp = CITED_BY + ".tmp"
    with open(tmp, "wb") as f:
        f.write(cb_blob)
    os.replace(tmp, CITED_BY)
    with open(G.MODEL, "rb") as f:
        model_sha = sha256_bytes(f.read())
    manifest = {
        "schema": "canon-corpus/xrefs/v1",
        "built_by": "pipeline/build_xrefs.py",
        "key": "KJV verse unit ids (kjv:Book.c.v), the ids already in data/uids/wordhoard.uids.json; nothing minted",
        "layers": {
            "tsk": {
                "file": "data/xrefs/tsk.jsonl",
                "sha256": sha256_bytes(blob),
                "rows": len(rows),
                "counts": counts,
                "rights": RIGHTS["tsk"],
                "scans": {t: {"item": SCANS[t]["item"], "edition": SCANS[t]["edition"],
                              "files": {k: {"name": n, "sha256": h} for k, (n, h) in SCANS[t]["files"].items()},
                              "read": scan_counts[t]} for t in ORDER},
                "glyph_model": {"file": "data/xrefs/glyph-3-8.json", "sha256": model_sha,
                                "report": model.d.get("report")},
                "not_claimed": [
                    "Only references both scans attest are committed (agreed, or placed by the "
                    "entry one scan missed); a reference only one scan reads is in "
                    "build/xrefs/tsk-one-scan.jsonl, counted, not committed.",
                    "A catchword is the OCR's text of it, uncorrected.",
                    "unsure_digit: both scans kept the OCR's 3 or 8 because the glyph model "
                    "could not call it; the two scans agreeing is then weak evidence.",
                    "The Treasury's notes (marginal readings, 'Heb.' renderings, chronology) "
                    "are not taken; only references.",
                    "Verses the Treasury has no entry for, or whose entry neither alignment "
                    "found, have no row.",
                ],
            },
            "cited_by": {
                "file": "build/xrefs/cited-by.jsonl (gitignored; rebuilt)",
                "sha256": sha256_bytes(cb_blob),
                "verses": len(cb_rows),
                "counts": dict(cb_counts),
                "inputs": {
                    "fathers_links": "build/fathers/scripture-links.jsonl (pipeline/tag_fathers.py, PR #7)"
                    if links_file and os.path.exists(links_file) else None,
                    "fathers_links_sha256": sha256_file(links_file) if links_file and os.path.exists(links_file) else None,
                    "books": "data/books/*.json (structure_texts.py): unit links of kind scripture to a kjv: verse"
                    if books_dir and os.path.isdir(books_dir) else None,
                },
                "rights": RIGHTS["cited_by"],
                "provisional": "fathers-notes citations of Old Testament verses: PR #7's OT links are "
                               "under review (30 of 64 checked were off); rebuild when #7 is fixed",
            },
        },
    }
    tmp = MANIFEST + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")
    os.replace(tmp, MANIFEST)
    print(f"wrote {TSK_FILE} ({len(rows)} rows), {CITED_BY} ({len(cb_rows)} verses), {MANIFEST}")
    return blob, counts


def check():
    blob, _ = build(write=False)
    with open(TSK_FILE, "rb") as f:
        have = f.read()
    with open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    ok = blob == have and sha256_bytes(blob) == man["layers"]["tsk"]["sha256"]
    print("check:", "byte-identical" if ok else "DIFFERS")
    return ok


def digit_class(rid, shape):
    """Which glyph evidence a committed reference stands on:
    "no-3/8"           no 3 or 8 in its numbers;
    "3/8, shape tells" every 3/8 in it, swapped, names no verse, so the
                       Bible's shape alone confirms the reading;
    "3/8, shape blind" some 3/8, swapped, also names a verse: only the glyph
                       model chose, and two scans agreeing adds little (both
                       go through the same model). Where a model error would
                       hide, so it is measured on its own."""
    b, c, v, c2, v2 = T.parse_ref_id(rid)
    nums = {"c": c, "v": v, "c2": c2, "v2": v2}
    if not any(ch in "38" for x in nums.values() for ch in str(x)):
        return "no-3/8"

    def names(n):
        cc, vv, cc2, vv2 = n["c"], n["v"], n["c2"], n["v2"]
        return all(x in shape[b] for x in (cc, cc2)) and 1 <= vv <= shape[b][cc] and 1 <= vv2 <= shape[b][cc2]
    for f, x in nums.items():
        if (f == "c2" and c2 == c) or (f == "v2" and (c2, v2) == (c, v)):
            continue                      # not printed: the id repeats c / v
        sx = str(x)
        for i, ch in enumerate(sx):
            if ch in "38":
                n = dict(nums)
                n[f] = int(sx[:i] + G.SWAP[ch] + sx[i + 1:])
                if f == "c" and c2 == c:
                    n["c2"] = n["c"]
                if f == "v" and (c2, v2) == (c, v):
                    n["v2"] = n["v"]
                if names(n):
                    return "3/8, shape blind"
    return "3/8, shape tells"


def measure(path):
    """Share of committed references OpenBible.info also lists for the verse
    (ranges overlap). OpenBible is CC BY: it is read here, never written anywhere."""
    shape = T.kjv_shape()
    V = T.Verses(shape)
    ob = collections.defaultdict(set)

    def pv(s):
        b, c, v = s.split(".")
        return (b, int(c), int(v))
    with open(path, encoding="utf-8") as f:
        next(f)
        for ln in f:
            a, t, _ = ln.rstrip("\n").split("\t")
            src = pv(a)
            if "-" in t:
                x, y = t.split("-")
                i, j = V.index.get(pv(x)), V.index.get(pv(y))
                if i is not None and j is not None:
                    for k in range(i, min(j, i + 40) + 1):
                        ob[src].add(V.seq[k])
            else:
                ob[src].add(pv(t))
    st = collections.defaultdict(lambda: [0, 0])
    with open(TSK_FILE, encoding="utf-8") as f:
        for raw in f:
            row = json.loads(raw)
            src = T.parse_ref_id(row["verse"])[:3]
            placed = set(row.get("placed", []))
            uns = set(row.get("unsure_digit", []))
            for g in row["groups"]:
                for rid in g["refs"]:
                    b, c, v, c2, v2 = T.parse_ref_id(rid)
                    i, j = V.index[(b, c, v)], V.index[(b, c2, v2)]
                    hit = any(V.seq[k] in ob[src] for k in range(i, min(j, i + 40) + 1))
                    kind = "placed" if rid in placed else ("unsure_digit" if rid in uns else "agreed")
                    for k in ("all", kind, "digits: " + digit_class(rid, shape)):
                        st[k][0] += 1
                        st[k][1] += hit
    if os.path.exists(ONE_SCAN):
        with open(ONE_SCAN, encoding="utf-8") as f:
            for raw in f:
                row = json.loads(raw)
                src = T.parse_ref_id(row["verse"])[:3]
                b, c, v, c2, v2 = T.parse_ref_id(row["ref"])
                i, j = V.index[(b, c, v)], V.index[(b, c2, v2)]
                hit = any(V.seq[k] in ob[src] for k in range(i, min(j, i + 40) + 1))
                st["one-scan (not committed)"][0] += 1
                st["one-scan (not committed)"][1] += hit
    for k, (n, h) in st.items():
        print(f"  {k:28s} {n:7d}  also in OpenBible {h / n:.3f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--train", action="store_true")
    ap.add_argument("--measure", metavar="CROSS_REFERENCES_TXT")
    ap.add_argument("--books", default=os.path.join(ROOT, "data", "books"),
                    help="built books whose unit links feed cited-by (default data/books)")
    ap.add_argument("--fathers-links", default=os.path.join(ROOT, "build", "fathers", "scripture-links.jsonl"),
                    help="PR #7's tag_fathers.py output (default build/fathers/scripture-links.jsonl)")
    a = ap.parse_args()
    if a.fetch:
        fetch()
        return
    if a.measure:
        measure(a.measure)
        return
    if a.check:
        sys.exit(0 if check() else 1)
    build(train=a.train, books_dir=a.books, links_file=a.fathers_links)


if __name__ == "__main__":
    main()
