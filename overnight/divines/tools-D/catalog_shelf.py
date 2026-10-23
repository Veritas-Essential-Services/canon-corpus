#!/usr/bin/env python3
"""Lane D's shelf helper: an author's English Gutenberg texts -> a shelf, and the
lane's records for it. Written 2026-10-23 to replace the session-scratch helpers
lost at the 10/18 pause; kept on the branch so the next worker has it.

    held      <out.json>                         every Gutenberg id and shelf name on every origin branch
    make      <shelf> --author "Surname, First, 1800-1900" [--author ...] --prefix p
              --surname "first surname" [--surname ...] --about "..."  (needs held.json, catalog)
    scan      <shelf>     after fetch_shelf.py: move texts with a 1931+ copyright line to _held
    finish    <shelf> --blurb "..."   map section, master map, queue, report, digest rows

Paths: --catalog (pg_catalog.csv.gz from gutenberg.org/cache/epub/feeds/) and
--held (held.json) default to $LANE_D_SCRATCH. Run from the canon-corpus root.
Stats only: no book text is printed or written to any committed file.
"""
import argparse, csv, gzip, json, os, re, subprocess, sys, datetime

SCR = os.environ.get("LANE_D_SCRATCH", ".")
ap = argparse.ArgumentParser()
ap.add_argument("cmd"); ap.add_argument("shelf")
ap.add_argument("--author", action="append", default=[])
ap.add_argument("--prefix"); ap.add_argument("--surname", action="append", default=[])
ap.add_argument("--about", default=""); ap.add_argument("--blurb", default="Novels and other writing.")
ap.add_argument("--catalog", default=os.path.join(SCR, "pg_catalog.csv.gz"))
ap.add_argument("--held", default=os.path.join(SCR, "held.json"))
a = ap.parse_args()

def git(*args, inp=None):
    return subprocess.run(["git", *args], capture_output=True, input=inp).stdout

def now():
    return subprocess.run(["date", "+%Y-%m-%dT%H:%M:%S%:z"], capture_output=True, text=True,
                          env={**os.environ, "TZ": "America/Chicago"}).stdout.strip()

def held(out):
    refs = [r for r in git("for-each-ref", "--format=%(refname)", "refs/remotes/origin").decode().split()
            if not r.endswith("/HEAD")]
    blobs = {}
    for ref in refs:
        for line in git("ls-tree", "-r", ref, "--", "pipeline/").decode().splitlines():
            meta, path = line.split("\t", 1)
            if path.endswith((".json", ".py")):
                blobs.setdefault(meta.split()[2], (ref, path))
    ids, shelves = {}, {}
    def add(i, where):
        try: ids.setdefault(int(i), where)
        except (TypeError, ValueError): pass
    raw = git("cat-file", "--batch", inp="".join(s + "\n" for s in blobs).encode())
    pos = 0
    while pos < len(raw):
        nl = raw.index(b"\n", pos); hdr = raw[pos:nl].split(); size = int(hdr[2])
        body = raw[nl + 1: nl + 1 + size]; pos = nl + size + 2
        ref, path = blobs[hdr[0].decode()]; name = path.split("/")[-1]
        if name.endswith("_shelf.json"):
            shelves.setdefault(name[:-11], set()).add(ref.split("origin/", 1)[1])
            try: d = json.loads(body)
            except ValueError: continue
            for slug, row in (d.get("gutenberg") or {}).items():
                add(row[0] if isinstance(row, list) and row else row, f"{name}:{slug}")
            for sec in ("_excluded", "_held"):
                v = d.get(sec) or {}
                txt = json.dumps(v)
                lists = re.findall(r"\bPG ((?:\d+(?:, (?:and )?|,? and ))*\d+)", txt)  # "PG 545, 29405 and 69338"
                for m in re.findall(r"\bpg-(\d+)", txt, re.I) + [i for l in lists for i in re.findall(r"\d+", l)]:
                    add(m, f"{name}:{sec}")
        elif name.endswith(".py"):
            t = body.decode("utf-8", "replace")
            if "gutenberg" in t.lower():
                for m in re.finditer(r'"[a-z0-9_\-]+"\s*:\s*\(?\s*(\d{1,5})\s*[,)]', t):
                    add(m.group(1), name)
        else:
            s = body.decode("utf-8", "replace")
            if "gutenberg" in s.lower():
                for m in re.finditer(r'"(?:pg|gutenberg|pg_id|id)"\s*:\s*(\d{1,5})\b', s):
                    add(m.group(1), name)
    json.dump({"ids": {str(k): v for k, v in sorted(ids.items())},
               "shelves": {k: sorted(v) for k, v in sorted(shelves.items())}}, open(out, "w"))
    print(len(refs), "branches,", len(ids), "Gutenberg ids,", len(shelves), "shelf names")

def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()

def slugify(prefix, title, taken, pg):
    t = re.split(r"[:;]|\n", title)[0]
    t = re.sub(r"^(the|a|an)\s+", "", t.strip(), flags=re.I)
    t = re.sub(r"['’]", "", t.lower())
    s = (prefix + "-" + re.sub(r"[^a-z0-9]+", "-", t).strip("-"))[:60].rstrip("-")
    return s if s not in taken else f"{s}-{pg}"

def make():
    H = json.load(open(a.held))
    path = f"pipeline/{a.shelf}_shelf.json"
    if os.path.exists(path) or a.shelf in H["shelves"]:
        sys.exit(f"shelf name {a.shelf!r} already exists on {H['shelves'].get(a.shelf, ['this branch'])}")
    rows = [r for r in csv.DictReader(gzip.open(a.catalog, "rt", encoding="utf-8")) if r["Type"] == "Text"]
    mine = [r for r in rows if any(x in a.author for x in r["Authors"].split("; "))]
    mine.sort(key=lambda r: int(r["Text#"]))
    gut, exc, seen, other_lang = {}, {}, {}, 0
    rep, elsewhere = [], []
    for r in mine:
        pg, title = int(r["Text#"]), " ".join(r["Title"].split())
        if r["Language"] != "en":
            other_lang += 1; continue
        if str(pg) in H["ids"]:
            elsewhere.append(pg); continue
        if re.search(r"\bindex\b", title, re.I) and re.search(r"works|gutenberg", title, re.I):
            exc[f"pg-{pg}"] = f"PG {pg}: Gutenberg's index of the author's works, not a book."; continue
        k = norm(title)
        if k in seen and seen[k][1] != r["Issued"]:
            rep.append(pg); continue
        if k in seen:   # same title, same release day: the volumes of one set
            title += " (a volume of a set Gutenberg lists under one title)"
        seen.setdefault(k, (pg, r["Issued"]))
        slug = slugify(a.prefix, title, gut, pg)
        gut[slug] = [pg, title]
    if rep:
        exc["repeat-editions"] = "PG " + ", ".join(map(str, rep)) + ": second Gutenberg editions of titles already on the shelf."
    if elsewhere:
        exc["held-elsewhere"] = "PG " + ", ".join(map(str, elsewhere)) + ": already on another shelf or in fetch_sources.py on some branch; not taken twice."
    names = sorted({w for s in a.surname for w in s.split() if len(w) > 2 and "." not in w})
    shelf = {"_about": a.about + " Every English text under the name at Gutenberg that no other shelf holds."
                       " Added " + now()[:10] + " at the coordinator's relay of Adam's keep-going message (Adam may veto).",
             "_author": a.author[0].split(",")[1].strip() + " " + a.author[0].split(",")[0].strip()
                        if len(a.author) == 1 else " and ".join(x.split(",")[1].strip() + " " + x.split(",")[0] for x in a.author),
             "_name_words": names, "_surname": a.surname,
             "ccel": {}, "gutenberg": gut, "internet_archive": {}, "_excluded": exc, "_held": {}}
    json.dump(shelf, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{path}: {len(gut)} books, {len(rep)} repeats, {len(elsewhere)} held elsewhere, {other_lang} not English")

COPY = re.compile(r"(?i)(?:copyright(?:ed)?|\(c\)|©)[^\n]{0,60}?\b(193[1-9]|19[4-9]\d|20\d\d)\b")
def scan():
    path = f"pipeline/{a.shelf}_shelf.json"
    shelf = json.load(open(path, encoding="utf-8"))
    moved = []
    for slug, row in list(shelf["gutenberg"].items()):
        f = f"data/corpus/{a.shelf}/{slug}.txt"
        if not os.path.exists(f): continue
        t = open(f, encoding="utf-8", errors="replace").read()
        m = re.search(r"\*\*\* ?START OF[^\n]*", t)
        body = t[m.end():] if m else t
        e = re.search(r"\*\*\* ?END OF", body)
        body = body[:e.start()] if e else body
        front = body[:20000]
        # an old-format file carries Gutenberg's own legal small print after the
        # START line ("Copyright laws are changing", "501(c)(3)"): not a book's line
        front = "\n".join(l for l in front.splitlines()
                          if not re.search(r"(?i)gutenberg|copyright laws|501\(c\)|small print|this header|etext", l))
        hits = sorted({int(y) for y in COPY.findall(front)})
        if hits:
            moved.append((slug, row, hits))
    if moved:
        note = "; ".join(f"PG {row[0]} {row[1][:60]} (copyright line {', '.join(map(str, hits))})" for _, row, hits in moved)
        shelf["_held"]["post-1930"] = ("HELD at the lane's pre-1931 rule (DIGEST-D item 24): " + note +
                                       ". The text names a 1931 or later copyright, so it is not taken until Adam rules.")
        for slug, _, _ in moved:
            del shelf["gutenberg"][slug]
            os.remove(f"data/corpus/{a.shelf}/{slug}.txt")
    json.dump(shelf, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{a.shelf}: {len(moved)} held post-1930: {[m[0] for m in moved]}")

def finish():
    path = f"pipeline/{a.shelf}_shelf.json"
    shelf = json.load(open(path, encoding="utf-8"))
    conv = json.load(open(f"data/corpus/{a.shelf}/{a.shelf}_convert_report.json"))
    fetch = json.load(open(f"data/corpus/{a.shelf}/{a.shelf}_fetch_report.json"))
    checks = shelf.get("_checks", {})
    failed = [s for s in shelf["gutenberg"] if fetch.get(s, {}).get("status") == "FAILED"]
    mism = [s for s, c in checks.items() if c.get("identity") not in (None, "ok")]
    rights = [s for s, c in checks.items() if c.get("pg_copyrighted")]
    units = sum(c.get("units", 0) for c in conv.values() if c.get("status") == "built")
    built = {s: conv[s] for s in conv if conv[s].get("status") == "built"}
    tilde = 0
    for s in built:
        b = f"data/books/{s}.json"
        if os.path.exists(b):
            tilde += sum(1 for u in json.load(open(b, encoding="utf-8"))["units"] if "~" in u["id"])
    n = len(shelf["gutenberg"]); day = now()[:10]
    nexc = len(shelf.get("_excluded", {})); nheld = len(shelf.get("_held", {}))
    lines = [f"## {shelf['_author']}", "",
             f"Shelf: `{path}` ({day}; added at the coordinator's relay of Adam's keep-going wish, Adam may veto). "
             f"{a.blurb} Every English text under the name at Gutenberg that no other shelf holds ({n} books). "
             "Not in the manifest; no uids minted.", "", "| Work | Status | Where |", "|---|---|---|"]
    for slug, row in shelf["gutenberg"].items():
        st = "have" if slug in built else "pending"
        u = f" ({built[slug]['units']} units)" if slug in built else " (fetch failed)"
        lines.append(f"| {row[1].replace('|', '/')} | {st} | PG {row[0]}, `{slug}`{u} |")
    for k, v in shelf.get("_excluded", {}).items():
        lines.append(f"| {k} | excluded | {v.replace('|', '/')} |")
    for k, v in shelf.get("_held", {}).items():
        lines.append(f"| {k} | pending | {v.replace('|', '/')} |")
    with open("docs/divines-map/D-storytellers.md", "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(lines) + "\n")
    os.system("cat docs/divines-map/*.md > docs/DIVINES-MASTER-MAP.md")
    note = (f"{a.shelf}: new shelf, {len(built)} Gutenberg books, {units:,} units, {tilde} ~2 ids; "
            f"verify {len(mism)} mismatches, {len(rights)} rights flags" + (f"; {len(failed)} failed to fetch" if failed else "") + ".")
    qp = "overnight/divines/QUEUE-D.json"
    q = json.load(open(qp, encoding="utf-8")); t = now()
    q["items"].append({"id": a.shelf, "scope": f"STORYTELLERS (added at the coordinator's relay of Adam's keep-going message, {day}; Adam may veto) — {shelf['_author']}; no minting",
                       "status": "done" if not (failed or mism or rights) else "done-with-defects",
                       "started": t, "finished": t, "notes": note})
    json.dump(q, open(qp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    open(qp, "a").write("\n") if not open(qp).read().endswith("\n") else None
    with open("overnight/divines/REPORT-D.md", "a", encoding="utf-8") as f:
        f.write(f"\n## {t[:10]} {t[11:16]} CDT — {a.shelf}: done\n- {note}\n")
    extra = f" {nexc} files listed in _excluded (second copies, anthologies, indexes)." if nexc else ""
    extra += " Post-1930 printings held." if shelf.get("_held") else ""
    row = f"| `{a.shelf}` | {len(built)} Gutenberg | 0 | {units:,} | {a.blurb} Every English text under the name at Gutenberg that no other shelf holds; added {day}.{extra} |"
    dp = "overnight/divines/DIGEST-D.md"
    d = open(dp, encoding="utf-8").read()
    d = d.replace("\n\n## For Adam to decide", "\n" + row + "\n\n## For Adam to decide", 1)
    open(dp, "w", encoding="utf-8").write(d)
    print(note)

{"held": lambda: held(a.shelf), "make": make, "scan": scan, "finish": finish}[a.cmd]()
