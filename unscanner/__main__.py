"""python3 -m unscanner run <slug> [--archive ID | --pdf PATH] [--pages 1-40] [--title T --author A]

Phase A of the Unscanner (vault: 9 - Projects/Unscanner): one user, public-domain books only.

The rights gate comes first and is not optional. An archive.org item must carry the Archive's own
`possible-copyright-status: NOT_IN_COPYRIGHT`, or the run must say why the book is public domain with
`--rights "..."` (a local PDF always needs it). The reason is written into every output.
"""
import argparse
import datetime
import hashlib
import json
import os
import sys
import urllib.request

from . import book as BK
from . import emit as E
from . import scan as S

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DEFAULT_WORK = os.path.join(REPO, "data", "unscanner")


def known(slug):
    """Defaults for a book the corpus already declares (fetch_sources.ARCHIVE_OCR)."""
    sys.path.insert(0, os.path.join(REPO, "pipeline"))
    try:
        import fetch_sources as fs
        import structure_texts as st
    except Exception:
        return {}
    out = {}
    if slug in getattr(fs, "ARCHIVE_OCR", {}):
        ident, _fn, note = fs.ARCHIVE_OCR[slug]
        out.update(ident=ident, note=note)
    if slug in getattr(st, "ARCHIVE_PROSE", {}):
        out.update(title=st.ARCHIVE_PROSE[slug][0], author=st.ARCHIVE_PROSE[slug][1],
                   extra_heads=tuple(st.ARCHIVE_PROSE[slug][2]),
                   heading_fixes=dict(st.ARCHIVE_PROSE[slug][3]) if len(st.ARCHIVE_PROSE[slug]) > 3 else {})
    return out


def archive_rights(ident):
    with urllib.request.urlopen(f"https://archive.org/metadata/{ident}", timeout=60) as r:
        md = json.load(r).get("metadata", {})
    return md.get("possible-copyright-status"), md


def parse_pages(spec, total):
    if not spec:
        return list(range(1, total + 1))
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out.extend(range(int(a), min(total, int(b or a)) + 1))
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(a):
    k = known(a.slug)
    ident = a.archive or k.get("ident")
    title = a.title or k.get("title") or a.slug
    author = a.author or k.get("author") or ""
    work = BK.Work(a.work, a.slug)
    pdf = work.p("source.pdf")
    if ident and not a.pdf:
        status, md = archive_rights(ident)
        if status != "NOT_IN_COPYRIGHT" and not a.rights:
            sys.exit(f"REFUSED: archive.org {ident} is marked {status!r}, not NOT_IN_COPYRIGHT. "
                     f"Phase A is public domain only; give --rights \"why it is PD\" if you have read the edition's rights.")
        rights = a.rights or f"archive.org possible-copyright-status NOT_IN_COPYRIGHT ({md.get('date', '?')})"
        print(f"fetching {ident} ...")
        S.fetch_pdf(ident, pdf)
        source = f"https://archive.org/details/{ident}"
    elif a.pdf:
        if not a.rights:
            sys.exit("REFUSED: a local PDF needs --rights \"why it is public domain\" (Phase A is PD only).")
        rights = a.rights
        if not os.path.exists(pdf):
            with open(a.pdf, "rb") as src, open(pdf + ".part", "wb") as dst:
                dst.write(src.read())
            os.replace(pdf + ".part", pdf)
        source = os.path.basename(a.pdf)
    else:
        sys.exit("give --archive ID or --pdf PATH (or a slug fetch_sources.ARCHIVE_OCR knows)")
    total = S.page_count(pdf)
    pages = parse_pages(a.pages, total)
    print(f"{title}: {len(pages)} of {total} pages")
    done = BK.ocr_pages(work, pdf, pages, log=(lambda m: None) if a.quiet else print, jobs=a.jobs)
    font_cache = os.path.join(a.work, "_fonts")
    pg, rep = BK.analyse(work, done, font_cache, match_fonts=not a.no_fonts)
    sd = None
    if ident:
        from . import scandata as SD
        sdp = SD.fetch(ident, work.p("scandata.xml"))
        if sdp:
            sd = SD.pages(sdp)
            bind = SD.binding(sd)
            for p in pg:
                if p["n"] in bind:
                    p["kind"] = "binding"
    coll = None
    if ident and not a.no_collate:
        wpath = work.p("witness_djvu.txt")
        local = os.path.join(REPO, "data", "corpus", "archive", a.slug + ".txt")
        if not os.path.exists(wpath):
            if os.path.exists(local):
                open(wpath, "w", encoding="utf-8").write(open(local, encoding="utf-8", errors="replace").read())
            else:
                try:
                    with urllib.request.urlopen(f"https://archive.org/download/{ident}/{ident}_djvu.txt", timeout=120) as r:
                        open(wpath, "wb").write(r.read())
                except Exception as e:
                    print(f"  (no second witness: {e})")
        if os.path.exists(wpath):
            from . import collate as C
            coll = C.collate(pg, open(wpath, encoding="utf-8", errors="replace").read())
    front, divisions, hy = BK.assemble(pg, a.slug, tuple(a.heading or ()) or k.get("extra_heads", ()),
                                     k.get("heading_fixes"))
    units = BK.units(divisions, a.slug)
    archive_check = SD.check(sd, pg, divisions) if sd else None
    kinds = {}
    for p in pg:
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    best = (rep["fonts"] or [None])[0]
    report = {"pages": len(pg), "kinds": kinds, "confidence": BK.confidence(pg), "body_px": rep["body_px"],
              "style": rep["style"], "divisions": len(divisions), "units": len(units),
              "furniture": {"folios": sum(1 for p in pg if p.get("label")),
                            "running_heads": sum(1 for p in pg if p.get("head"))},
              "figures": sum(len(p["figures"]) for p in pg if p["kind"] != "blank"),
              "hyphens": {k: v for k, v in hy.items()}, "fonts": rep["fonts"],
              "collation": coll, "archive_record": archive_check,
              "font_margin": round(rep["fonts"][0]["score"] - rep["fonts"][1]["score"], 4) if len(rep["fonts"]) > 1 else None}
    meta = {"slug": a.slug, "title": title, "author": author, "ident": ident, "source": source, "rights": rights,
            "pdf_sha256": sha256(pdf), "modified": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pt": best["pt"] if best else 12,
            "colophon": f"Re-set by the Unscanner from {source}. {rights}. Typeface: "
                        f"{best['family'] + (' (closest open match' + ('; inconclusive' if (report['font_margin'] or 1) < 0.01 else '') + ')') if best else 'default'}"
                        f". Unproofread OCR."}
    fam = best["family"] if best else "Georgia"
    from . import fonts as F
    finfo = F.fetch_fonts(font_cache, only=[fam]).get(fam) if best else None
    imgs = E.plate_images(work, pdf, pg)
    px_em = (best["pt"] if best else 12) * 300 / 72
    outs = [E.reflow_html(work, meta, front, divisions, imgs, fam, finfo, pg),
            E.pages_html(work, meta, pg, imgs, fam, finfo, px_em),
            E.epub(work, meta, front, divisions, imgs, fam, finfo, pg),
            E.units_json(work, meta, units, pg, report),
            E.review_html(work, meta, pg, report)]
    with open(work.p("out", "report.json"), "w", encoding="utf-8") as f:
        json.dump({k: v for k, v in report.items()}, f, indent=1, ensure_ascii=False)
    with open(work.p("book.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "pages": pg}, f, ensure_ascii=False)
    summary = {k: report[k] for k in ("pages", "kinds", "confidence", "divisions", "units", "furniture", "figures", "style",
                                      "archive_record")}
    summary["font"] = [(r["family"], r["score"], r["pt"]) for r in rep["fonts"][:3]]
    summary["hyphens"] = {k: v for k, v in hy.items() if k != "doubtful"}
    if coll:
        summary["collation"] = {k: v for k, v in coll.items() if k != "mends"}
    print(json.dumps(summary, indent=1))
    for o in outs:
        print("  ->", os.path.relpath(o, REPO))
    if a.to_corpus:
        if not a.pages and k.get("ident"):
            dest = os.path.join(REPO, "data", "corpus", "archive", a.slug + ".unscanned.json")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(outs[3], encoding="utf-8") as src, open(dest + ".part", "w", encoding="utf-8") as dst:
                dst.write(src.read())
            os.replace(dest + ".part", dest)
            print("  -> corpus:", os.path.relpath(dest, REPO), "(structure_texts.py now prefers it)")
        else:
            print("  (--to-corpus needs a whole-book run of a slug fetch_sources.ARCHIVE_OCR declares)")
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(prog="unscanner")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="scan -> re-set book (HTML, EPUB, units, review sheet)")
    r.add_argument("slug")
    r.add_argument("--archive")
    r.add_argument("--pdf")
    r.add_argument("--pages", help="e.g. 1-40 or 12,30-33 (default: all)")
    r.add_argument("--title")
    r.add_argument("--author")
    r.add_argument("--rights", help="why this edition is public domain (required for --pdf)")
    r.add_argument("--heading", action="append", help="an unnumbered section heading (repeatable)")
    r.add_argument("--work", default=DEFAULT_WORK)
    r.add_argument("--no-fonts", action="store_true")
    r.add_argument("--no-collate", action="store_true", help="do not consult the Archive's own OCR")
    r.add_argument("--quiet", action="store_true")
    r.add_argument("--to-corpus", action="store_true",
                   help="copy units.json into data/corpus/archive/ so structure_texts.py builds from it")
    r.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 1)), help="pages OCR'd at once")
    a = ap.parse_args(argv)
    if a.cmd == "run":
        run(a)


if __name__ == "__main__":
    main()
