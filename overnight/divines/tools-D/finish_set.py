#!/usr/bin/env python3
"""Lane D bookkeeping for a children's-set shelf (Gutenberg and Internet
Archive rows mixed), the counterpart of catalog_shelf.py finish.

    python3 overnight/divines/tools-D/finish_set.py <shelf> "<one-line blurb>"

Run after fetch_shelf.py <shelf>, --verify --record and, if the shelf has
Gutenberg rows, convert_shelf_gutenberg.py <shelf>. Appends the shelf's table
to docs/divines-map/D-storytellers.md, regenerates the master map, and adds a
QUEUE-D item, a REPORT-D entry and a DIGEST-D row. Internet Archive items stay
raw OCR (fetch_shelf.py's rule) and are counted as texts, not units.
"""
import json, os, sys, datetime

def now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).isoformat(timespec="seconds")

name, blurb = sys.argv[1], sys.argv[2]
path = f"pipeline/{name}_shelf.json"
shelf = json.load(open(path, encoding="utf-8"))
cdir = f"data/corpus/{name}"
crp = f"{cdir}/{name}_convert_report.json"
conv = json.load(open(crp)) if os.path.exists(crp) else {}
fetch = json.load(open(f"{cdir}/{name}_fetch_report.json"))
checks = shelf.get("_checks", {})
pg, ia = shelf.get("gutenberg", {}), shelf.get("internet_archive", {})
failed = [s for s in list(pg) + list(ia) if fetch.get(s, {}).get("status") == "FAILED"]
mism = [s for s, c in checks.items() if c.get("identity") not in (None, "ok", "title_weak")]
rights = [s for s, c in checks.items() if c.get("pg_copyrighted") or str(c.get("ia_rights", "ok")).startswith(("CHECK", "unchecked"))]
built = {s: conv[s] for s in conv if conv[s].get("status") == "built"}
units = sum(c.get("units", 0) for c in built.values())
day = now()[:10]
lines = [f"## {shelf['_author']}", "",
         f"Shelf: `{path}` ({day}; at Adam's ask for old children's sets). {blurb} "
         f"{len(pg)} Gutenberg texts, {len(ia)} Internet Archive scans (raw OCR). Not in the manifest; no uids minted.",
         "", "| Work | Status | Where |", "|---|---|---|"]
for slug, row in pg.items():
    u = f" ({built[slug]['units']} units)" if slug in built else ""
    lines.append(f"| {row[1].replace('|', '/')} | {'have' if slug in built else 'pending'} | PG {row[0]}, `{slug}`{u} |")
for slug, row in ia.items():
    ok = slug not in failed
    lines.append(f"| {row[1].replace('|', '/')} | {'have (raw OCR)' if ok else 'pending'} | IA `{row[0]}`, `{slug}` |")
for k, v in shelf.get("_excluded", {}).items():
    lines.append(f"| {k} | excluded | {v.replace('|', '/')} |")
for k, v in shelf.get("_held", {}).items():
    lines.append(f"| {k} | pending | {v.replace('|', '/')} |")
with open("docs/divines-map/D-storytellers.md", "a", encoding="utf-8") as f:
    f.write("\n" + "\n".join(lines) + "\n")
os.system("cat docs/divines-map/*.md > docs/DIVINES-MASTER-MAP.md")
note = (f"{name}: new shelf, {len(built)} Gutenberg books ({units:,} units) and {len(ia) - len([s for s in failed if s in ia])} "
        f"Internet Archive scans; verify {len(mism)} mismatches, {len(rights)} rights flags"
        + (f"; {len(failed)} failed to fetch" if failed else "") + ".")
qp = "overnight/divines/QUEUE-D.json"
q = json.load(open(qp, encoding="utf-8")); t = now()
q["items"].append({"id": name, "scope": f"CHILDREN'S SETS (Adam's ask, {day}) — {shelf['_author']}; no minting",
                   "status": "done" if not (failed or mism or rights) else "done-with-defects",
                   "started": t, "finished": t, "notes": note})
json.dump(q, open(qp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(qp, "a").write("\n")
with open("overnight/divines/REPORT-D.md", "a", encoding="utf-8") as f:
    f.write(f"\n## {t[:10]} {t[11:16]} CDT — {name}: done\n- {note}\n")
row = f"| `{name}` | {len(built)} Gutenberg + {len(ia)} IA | 0 | {units:,} | {blurb} Added {day} (children's sets). |"
dp = "overnight/divines/DIGEST-D.md"
d = open(dp, encoding="utf-8").read()
d = d.replace("\n\n## For Adam to decide", "\n" + row + "\n\n## For Adam to decide", 1)
open(dp, "w", encoding="utf-8").write(d)
print(note)
