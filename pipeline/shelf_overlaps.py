#!/usr/bin/env python3
"""Find shelves that fetch the same source: one Gutenberg number, Internet
Archive identifier, CCEL work or Perseus URN named by two shelf entries.

    python3 pipeline/shelf_overlaps.py                      # pipeline/*_shelf.json here
    python3 pipeline/shelf_overlaps.py --ref origin/claude/armarium-divines
    python3 pipeline/shelf_overlaps.py --ref <ref> --json   # machine-readable
    python3 pipeline/shelf_overlaps.py --ref <ref> --check  # exit 1 if a lane owns an overlap
    python3 pipeline/shelf_overlaps.py --all                # also list what main already holds twice

The relay (overnight/divines/RULES.md) runs four lanes that each write their
own pipeline/<author>_shelf.json. Nothing stops two lanes shelving the same
book from the same file: a translator's lane and an author's lane, say, both
naming PG 2600. Each shelf then fetches it, the library holds it under two
slugs, and the uid pass would mint it twice. This reads every shelf and
reports each source named more than once.

Only the fetch dicts count (`ccel`, `gutenberg`, `internet_archive`,
`perseus`). `_held`, `_cross_ref`, `_pending`, `_excluded` and `_alternates`
are pointers or wishlists by design and are ignored.

Lanes: with --ref (or in a git checkout), each shelf's lane is read from the
subject of the commit that added it ("Lane A: ...", "relay C: ..."). Shelves
already on main, and fetch_sources.py's own lists (read as one more shelf),
are "main". A shelf whose lane can't be read is "?". An overlap is `cross-lane` when its shelves
belong to two lanes (or a lane is unknown), `same-lane` when one lane named
the source twice, `on-main` when every shelf involved is already merged.

It also reports SLUG clashes: one slug on two rows. The built book is
data/books/<slug>.json and the manifest is keyed by slug, so two texts under
one slug would overwrite each other. Reads only; writes nothing.
"""
import argparse, ast, json, os, re, subprocess, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SHELF_RE = re.compile(r"^pipeline/([^/]+)_shelf\.json$")
LANE_RE = re.compile(r"^\s*(?:lane|relay)\s+([A-D])\b", re.I)
KINDS = ("gutenberg", "internet_archive", "ccel", "perseus")


def _git(*args):
    return subprocess.check_output(["git", "-C", ROOT, *args], stderr=subprocess.DEVNULL)


def load_shelves(ref=None):
    """{shelf name: parsed json} from pipeline/ at `ref`, or the working tree."""
    out = {}
    if ref:
        names = _git("ls-tree", "--name-only", ref, "pipeline/").decode().split("\n")
        for p in names:
            m = SHELF_RE.match(p)
            if m:
                out[m.group(1)] = json.loads(_git("show", f"{ref}:{p}").decode("utf-8"))
    else:
        d = os.path.join(ROOT, "pipeline")
        for f in sorted(os.listdir(d)):
            m = SHELF_RE.match("pipeline/" + f)
            if m:
                with open(os.path.join(d, f), encoding="utf-8") as fh:
                    out[m.group(1)] = json.load(fh)
    return out


def manifest_shelf(ref=None):
    """pipeline/fetch_sources.py's own lists, as one more shelf ("fetch_sources").

    The dicts are read with ast, never imported, so nothing is executed."""
    path = "pipeline/fetch_sources.py"
    try:
        text = _git("show", f"{ref}:{path}").decode("utf-8") if ref else \
            open(os.path.join(ROOT, path), encoding="utf-8").read()
    except (OSError, subprocess.CalledProcessError):
        return {}
    d = {}
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            try:
                d[node.targets[0].id] = ast.literal_eval(node.value)
            except ValueError:
                pass
    shelf = {"gutenberg": {}, "ccel": {}, "perseus": {}}
    for slug, v in (d.get("GUTENBERG_EXTRA") or {}).items():
        shelf["gutenberg"][slug] = [v, slug]
    for slug, v in (d.get("CHESTERTON_GUTENBERG") or {}).items():
        shelf["gutenberg"][slug] = [v[0], v[1]]
    for slug, v in (d.get("CCEL") or {}).items():          # (author, work, note)
        shelf["ccel"][slug] = [f"{v[0][0]}/{v[0]}/{v[1]}", v[2]]
    for slug, v in (d.get("CHESTERTON_CCEL") or {}).items():
        shelf["ccel"][slug] = [f"c/chesterton/{v[0]}", v[1]]
    for slug, v in (d.get("PERSEUS") or {}).items():       # (repo, path, note)
        shelf["perseus"][slug] = [os.path.basename(v[1]).rsplit(".", 1)[0], v[2]]
    return shelf


def shelf_lanes(names, ref=None, base="origin/main"):
    """{shelf name: lane letter, "main" or "?"}.

    A shelf already on `base` belongs to "main" (merged work, no lane); the
    rest take the lane named by the commit that added the file."""
    lanes = {}
    try:
        on_base = set(_git("ls-tree", "--name-only", base, "pipeline/").decode().split("\n"))
    except (OSError, subprocess.CalledProcessError):
        on_base = set()
    for n in names:
        if n == "fetch_sources" or f"pipeline/{n}_shelf.json" in on_base:
            lanes[n] = "main"
            continue
        try:
            args = ["log", "--diff-filter=A", "--format=%s"]
            if ref:
                args.append(ref)
            subj = _git(*args, "--", f"pipeline/{n}_shelf.json").decode().strip().split("\n")
        except (OSError, subprocess.CalledProcessError):
            subj = []
        m = next((LANE_RE.match(s) for s in reversed(subj) if LANE_RE.match(s)), None)
        lanes[n] = m.group(1).upper() if m else "?"
    return lanes


def normalize(kind, ident, shelf_name, shelf):
    """The comparable form of one source id, or None if it names nothing."""
    if ident is None:
        return None
    s = str(ident).strip()
    if not s:
        return None
    if kind == "gutenberg":
        m = re.fullmatch(r"(?:pg|ebook\s*#?)?\s*0*(\d+)", s, re.I)
        return m.group(1) if m else s.lower()
    if kind == "internet_archive":
        return s.lower()  # IA lookups are case-insensitive; two cases are one item
    if kind == "ccel":
        if s.count("/") >= 2:
            return s.strip("/").lower()
        author = shelf.get("_ccel_author") or f"{shelf_name[0]}/{shelf_name}"
        return f"{author.strip('/')}/{s}".lower()
    return s.lower()  # perseus URN


def entries(shelves):
    """(kind, key, shelf, slug, title) for every fetch-dict row of every shelf."""
    for name, shelf in sorted(shelves.items()):
        for kind in KINDS:
            rows = shelf.get(kind)
            if not isinstance(rows, dict):
                continue
            for slug, row in rows.items():
                if isinstance(row, list) and row:
                    ident, title = row[0], (row[1] if len(row) > 1 else "")
                elif isinstance(row, dict):
                    ident = row.get("id") or row.get("identifier")
                    title = row.get("title", "")
                else:
                    continue
                key = normalize(kind, ident, name, shelf)
                if key:
                    yield kind, key, name, slug, str(title)


def _scope(rows):
    ls = {r["lane"] for r in rows}
    if ls == {"main"}:
        return "on-main"      # both already merged: not a relay lane's to fix
    if len(ls) > 1 or "?" in ls:
        return "cross-lane"
    return "same-lane"


ORDER = {"cross-lane": 0, "same-lane": 1, "on-main": 2}


def _group(pairs):
    out = []
    for (kind, key), rows in pairs.items():
        if len(rows) < 2:
            continue
        out.append({"kind": kind, "id": key, "scope": _scope(rows),
                    "same_shelf": len({r["shelf"] for r in rows}) == 1, "rows": rows})
    out.sort(key=lambda o: (ORDER[o["scope"]], o["kind"], o["id"]))
    return out


def overlaps(shelves, lanes=None):
    """Every source named by two or more rows, cross-lane first."""
    lanes = lanes or {}
    seen = defaultdict(list)
    for kind, key, name, slug, title in entries(shelves):
        seen[(kind, key)].append({"shelf": name, "slug": slug, "title": title,
                                  "lane": lanes.get(name, "?")})
    return _group(seen)


def slug_clashes(shelves, lanes=None):
    """Every slug used by two rows. The built book is data/books/<slug>.json and
    the manifest is keyed by slug, so two different texts under one slug would
    overwrite each other."""
    lanes = lanes or {}
    seen = defaultdict(list)
    for kind, key, name, slug, title in entries(shelves):
        seen[("slug", slug)].append({"shelf": name, "slug": slug, "title": title,
                                     "lane": lanes.get(name, "?"), "source": f"{kind} {key}"})
    clashes = _group(seen)
    for c in clashes:
        c["same_source"] = len({r["source"] for r in c["rows"]}) == 1
    return clashes


def _label(shelf):
    return "fetch_sources.py" if shelf == "fetch_sources" else f"{shelf}_shelf.json"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--ref", help="read shelves at this git ref instead of the working tree")
    ap.add_argument("--base", default="origin/main", help="shelves on this ref count as merged (default origin/main)")
    ap.add_argument("--json", action="store_true", help="print the findings as JSON")
    ap.add_argument("--all", action="store_true", help="also list overlaps that are already on main")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 on any cross- or same-lane overlap or slug clash")
    a = ap.parse_args(argv)
    shelves = load_shelves(a.ref)
    shelves["fetch_sources"] = manifest_shelf(a.ref)
    lanes = shelf_lanes(shelves, a.ref, a.base)
    found = {"sources": overlaps(shelves, lanes), "slugs": slug_clashes(shelves, lanes)}
    if a.json:
        print(json.dumps(found, ensure_ascii=False, indent=1))
    else:
        n_rows = sum(1 for _ in entries(shelves))
        print(f"{len(shelves) - 1} shelves + fetch_sources.py, {n_rows} fetch rows: "
              f"{len(found['sources'])} sources named twice or more, "
              f"{len(found['slugs'])} slugs used twice or more")
        hidden = sum(o["scope"] == "on-main" for k in found for o in found[k])
        if hidden and not a.all:
            print(f"({hidden} already on main, not a lane's to fix; --all lists them)")
        for what, items in (("SOURCE", found["sources"]), ("SLUG", found["slugs"])):
            for o in items:
                if o["scope"] == "on-main" and not a.all:
                    continue
                extra = ", one shelf" if o["same_shelf"] else ""
                if o.get("same_source"):
                    extra += ", same source"
                print(f"\n{what} [{o['scope']}{extra}] {o['kind']} {o['id']}")
                for r in o["rows"]:
                    src = f"  ({r['source']})" if "source" in r else ""
                    print(f"  lane {r['lane']:<4} {_label(r['shelf'])}  {r['slug']}{src}  -- {r['title'][:60]}")
    bad = sum(o["scope"] != "on-main" for k in found for o in found[k])
    if a.check and bad:
        raise SystemExit(f"{bad} overlap(s) or clash(es) a relay lane owns")


if __name__ == "__main__":
    main()
