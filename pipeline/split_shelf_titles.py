#!/usr/bin/env python3
"""Cut each TITLE of a translator shelf out of the volume it was fetched in.

    python3 pipeline/split_shelf_titles.py <shelf>     # e.g. dryden, from canon-corpus root

A translator shelf (dryden, garnett) lists two things: SOURCES (whole files,
fetched by fetch_shelf.py into data/corpus/<shelf>/) and TITLES (the works a
reader cites: dryden-georgics, dryden-juvenal). Several titles often live in
one source volume (Scott's Dryden vol. 12 holds his Ovid, Theocritus,
Lucretius, Horace and Homer), so each title names its source and a pair of
heading markers:

    "titles": {"dryden-juvenal": {"source": "dryden-scott-13",
                                  "start": ["TRANSLATIONS", 1],
                                  "end":   ["TRANSLATIONS", 2], ...}}

A marker is [exact heading line, stripped; which occurrence, 1-based]. "end"
null = to the end of the source's body. No "start" = the whole body. The
Gutenberg header and licence are always cut off first. "source" may be a
LIST of source slugs (a title in several volumes): their bodies are joined
in order, then cut. A title with "held_in" ({file, slug, gutenberg_id}) is
already held elsewhere in the repo (adler_shelf.json, fetch_sources.py):
it is cross-referenced, not fetched or cut again.

Writes data/corpus/<shelf>/titles/<slug>.txt (gitignored, atomic temp+rename)
and titles_report.json (lines, bytes, marker line numbers). A missing marker
or a source not on disk is REPORTED, never guessed and never written as an
empty file. A title that fails (or is held elsewhere) has any earlier
titles/<slug>.txt deleted, so a stale cut never outlives the failure that
replaced it (the report says "stale_removed"). Writes nothing under data/uids/: no minting (relay rule).
Converter files (fetch_sources.py, structure_texts.py) are untouched.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

def body(text):
    """Strip a Project Gutenberg header/footer if present."""
    s = re.search(r"^\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG.*$", text, re.M)
    e = re.search(r"^\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG.*$", text, re.M)
    return text[s.end() if s else 0: e.start() if e else len(text)]

def find(lines, marker, after=0):
    want, occ = marker
    n = 0
    for i, ln in enumerate(lines):
        if ln.strip() == want:
            n += 1
            if n == occ:
                if i < after:
                    raise ValueError(f"marker {marker} at line {i+1} precedes start")
                return i
    raise ValueError(f"marker {marker} not found ({n} occurrences)")

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: split_shelf_titles.py <shelf>")
    if sys.argv[1] in ("-h", "--help"):      # not a shelf name (reviewer, 2026-10-03)
        print(__doc__)
        sys.exit(0)
    name = sys.argv[1]
    shelf = json.load(open(os.path.join(HERE, f"{name}_shelf.json"), encoding="utf-8"))
    src_dir = os.path.join(ROOT, "data", "corpus", name)
    out = os.path.join(src_dir, "titles")
    os.makedirs(out, exist_ok=True)
    report = {}

    def fail(slug, rec):
        """Record a failed title and delete any earlier cut of it: a stale file
        on disk would read as a good title (coordinator review, 2026-10-03)."""
        dest = os.path.join(out, slug + ".txt")
        for p in (dest, dest + ".tmp"):
            if os.path.exists(p):
                os.remove(p)
                rec["stale_removed"] = True
        report[slug] = rec

    for slug, t in shelf.get("titles", {}).items():
        if t.get("held_in"):     # already held by another shelf/manifest: cross-reference, never re-cut
            fail(slug, {"status": "held-elsewhere", "held_in": t["held_in"]})
            print(slug, "held-elsewhere", t["held_in"].get("file"), t["held_in"].get("slug")); continue
        src = t["source"]
        srcs = src if isinstance(src, list) else [src]   # a list = volumes, joined in order
        paths = [next((os.path.join(src_dir, s + x) for x in (".txt", ".xml")
                       if os.path.exists(os.path.join(src_dir, s + x))), None) for s in srcs]
        if not all(paths):
            fail(slug, {"status": "NO-SOURCE", "source": src})
            print(slug, "NO-SOURCE", src); continue
        lines = []
        for path in paths:
            lines += body(open(path, encoding="utf-8", errors="replace").read()).splitlines()
        try:
            a = find(lines, t["start"]) if t.get("start") else 0
            b = find(lines, t["end"], after=a + 1) if t.get("end") else len(lines)
        except ValueError as e:
            fail(slug, {"status": "MARKER-FAILED", "source": src, "error": str(e)})
            print(slug, "MARKER-FAILED", e); continue
        chunk = "\n".join(lines[a:b]).strip() + "\n"
        if len(chunk) < 500:
            fail(slug, {"status": "TOO-SHORT", "source": src, "bytes": len(chunk)})
            print(slug, "TOO-SHORT", len(chunk)); continue
        dest = os.path.join(out, slug + ".txt")
        with open(dest + ".tmp", "w", encoding="utf-8") as f:
            f.write(chunk)
        os.replace(dest + ".tmp", dest)
        report[slug] = {"status": "cut", "source": src, "body_lines": [a + 1, b],
                        "lines": b - a, "bytes": len(chunk.encode("utf-8"))}
        print(slug, "cut", b - a, "lines", report[slug]["bytes"], "bytes")
    rp = os.path.join(out, "titles_report.json")
    json.dump(report, open(rp + ".tmp", "w"), indent=1)
    os.replace(rp + ".tmp", rp)
    bad = [s for s, r in report.items() if r["status"] not in ("cut", "held-elsewhere")]
    print(f"{len(report)} titles, {len(bad)} not cut: {bad}")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
