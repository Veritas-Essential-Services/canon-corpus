import json, os, sys, time, glob
sys.path.insert(0, "/root/batch")
from phrasekit import background, extract

B   = "/mnt/user-data/uploads/Projects/canon-corpus/data/books"
C   = "/mnt/user-data/uploads/Projects/canon-corpus/data/corpus"
OUT = "/root/batch/out"
os.makedirs(OUT, exist_ok=True)

BG_ALL = ["burke_reflections.txt","gibbon_v1.txt","federalist.txt",
          "tocqueville_v1.txt","treasure_island.txt","plutarch.txt"]

def background_for(slug):
    """A work must never be its own background.

    treasure_island is both an ingested work and one of the six background
    texts. Left alone it returns ZERO fingerprints -- correctly, since every
    phrase in it is by definition in the background -- and the zero looks
    exactly like a finding about Stevenson. Any slug whose name matches a
    background file is dropped from its own comparison set."""
    return [f"{C}/{x}" for x in BG_ALL if os.path.splitext(x)[0] != slug]
SKIP = {"manifest","lsj-greek","tbesg-greek","thayer","kjv"}   # lexicons; kjv.complete replaces kjv

works = []
for f in sorted(glob.glob(f"{B}/*.json")):
    s = os.path.basename(f)[:-5]
    if s in SKIP: continue
    works.append((s.replace("kjv.complete","kjv"), f))
works.append(("kjv", "/root/kjv/kjv.complete.json"))
works = {s: f for s, f in works}

t0 = time.time()
print(f"building background from {len(BG_ALL)} texts...", flush=True)
bg_cache = {}
def bg_for(slug):
    key = tuple(background_for(slug))
    if key not in bg_cache:
        bg_cache[key] = background(list(key))
    return bg_cache[key]
bg_full = bg_for("__none__")
print(f"  background: {len(bg_full):,} phrases  ({time.time()-t0:.0f}s)", flush=True)

rows = []
for i, (slug, path) in enumerate(sorted(works.items()), 1):
    t = time.time()
    bg = bg_for(slug)
    try:
        r = extract(path, bg)
    except Exception as e:
        print(f"[{i}/{len(works)}] {slug}: FAILED {type(e).__name__}: {e}", flush=True)
        continue
    if r is None:
        print(f"[{i}/{len(works)}] {slug}: too small, skipped", flush=True)
        continue
    with open(f"{OUT}/{slug}-signature.jsonl","w",encoding="utf-8") as f:
        for x in r["coinages"]: f.write(json.dumps(x, ensure_ascii=False)+"\n")
    with open(f"{OUT}/{slug}-fingerprint.jsonl","w",encoding="utf-8") as f:
        for x in r["fingerprints"]: f.write(json.dumps(x, ensure_ascii=False)+"\n")
    rows.append({"slug": slug, "title": r["title"], "author": r["author"],
                 "words": r["words"], "units": r["units"],
                 "coinages": len(r["coinages"]), "fingerprints": len(r["fingerprints"]),
                 "top_coinage": r["coinages"][0]["phrase"] if r["coinages"] else None,
                 "top_fingerprint": r["fingerprints"][0]["phrase"] if r["fingerprints"] else None,
                 "top_fingerprint_count": r["fingerprints"][0]["count"] if r["fingerprints"] else 0,
                 "seconds": round(time.time()-t,1)})
    print(f"[{i}/{len(works)}] {slug:<22} {r['words']:>8,}w  "
          f"{len(r['coinages']):>3}c {len(r['fingerprints']):>3}f  "
          f"{time.time()-t:.0f}s", flush=True)

json.dump(rows, open(f"{OUT}/_index.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\nDONE {len(rows)} works in {time.time()-t0:.0f}s", flush=True)
