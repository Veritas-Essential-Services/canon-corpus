"""
fingerprint.py -- the OTHER kind of distinctive phrase.

signature.py finds phrases a work uses ONCE, unpredictably: coinages.
This finds the opposite -- phrases a work uses CONSTANTLY that nobody else uses
at all. Not a coinage, a habit. "The shadow of death" is not surprising inside
the KJV (it appears in seven books) but it is nearly absent from English prose
that is not quoting it.

Coinages are what a work invented. Fingerprints are what it sounds like -- and
for cross-corpus probing a fingerprint is the better instrument, because a
phrase used twenty times gives twenty chances to be echoed instead of one.
"""
import json, math, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, "/root/echo")
from signature import sentences, bg_grams, book_of, NUMERAL, STOP_ONLY, NMIN, NMAX

MIN_COUNT = 5
MIN_BOOKS_USED = 2     # used in more than one book of the work: a habit, not a set piece

def run(book_path, bg_paths, out_path, top=200):
    units = json.load(open(book_path, encoding="utf-8"))["units"]
    raw, sents = [], []
    for u in units:
        for w in sentences(u["text"]):
            raw.extend(w); sents.append(([x.lower() for x in w], u["id"]))
    cap, low = Counter(), Counter()
    for w in raw: (cap if w[0].isupper() else low)[w.lower()] += 1
    props = {w for w,n in cap.items() if low.get(w,0)==0}

    count, books, where = Counter(), defaultdict(set), {}
    for lw, uid in sents:
        b = book_of(uid)
        for n in range(NMIN, NMAX+1):
            for i in range(len(lw)-n+1):
                g = lw[i:i+n]
                if any(x in props or x in NUMERAL for x in g): continue
                if sum(1 for x in g if x not in STOP_ONLY) < 2: continue
                k = " ".join(g)
                count[k] += 1; books[k].add(b); where.setdefault(k, uid)

    bg = bg_grams(bg_paths)
    rows = []
    for g, c in count.items():
        if c < MIN_COUNT or len(books[g]) < MIN_BOOKS_USED or g in bg: continue
        rows.append({"phrase": g, "n": len(g.split()), "count": c,
                     "books_used": len(books[g]), "first_at": where[g],
                     "score": round(math.log(c) * math.log(len(books[g])+1) * len(g.split()), 2)})
    rows.sort(key=lambda r: -r["score"])
    kept, seen = [], []
    for r in rows:
        if any(r["phrase"] in s for s in seen): continue
        kept.append(r); seen.append(r["phrase"])
        if len(kept) >= top: break
    with open(out_path,"w",encoding="utf-8") as f:
        for r in kept: f.write(json.dumps(r, ensure_ascii=False)+"\n")
    return kept

if __name__ == "__main__":
    kept = run(sys.argv[1], sys.argv[3].split(","), sys.argv[2])
    print(f"=== FINGERPRINT PHRASES — used repeatedly here, absent from ordinary prose ===")
    for r in kept[:40]:
        print(f"  x{r['count']:<4} {r['books_used']:>2} books  {r['phrase']:<44} [{r['first_at']}]")
