"""
phrasekit.py -- one pass over a work, producing both phrase lists.

COINAGES (signature): rare as a whole, common in their parts, far rarer than
those parts predict. What the work invented.

FINGERPRINTS: used repeatedly here, absent from ordinary English prose, spread
across the work rather than clumped. What the work sounds like.

Dispersion is measured POSITIONALLY -- each work is cut into 20 equal slices by
unit order -- rather than by the work's declared divisions. The corpus does not
declare them consistently (Gilgamesh claims one division; Bunyan's Holy War
claims one per unit), so anything keyed on them silently misbehaves. Position is
always available and measures the same thing: does this word range across the
whole work, or clump in one technical passage?
"""
import json, math, re, unicodedata
from collections import Counter, defaultdict

NMIN, NMAX   = 3, 6
SLICES       = 20
MIN_SLICE_FR = 0.25    # a word must appear in this fraction of the work's slices
MIN_WORD     = 25      # ...and be at least this common, to count as "ordinary"
MAX_COINAGE  = 4       # more occurrences than this and it is a formula
MIN_FINGER   = 5       # fewer than this and it is not a habit
MIN_FP_SLICES= 3       # a fingerprint must recur across the work, not in one scene

STOP_ONLY = set("""a an and are as at be but by for from had has have in is it its of on
or that the to was were with which who not so then there this these those he she they
them his her their you your i me my we us our shall will did do does been being am""".split())

NUMERAL = set("""one two three four five six seven eight nine ten eleven twelve thirteen
fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty
seventy eighty ninety hundred thousand million score first second third fourth fifth
sixth seventh eighth ninth tenth eleventh twelfth twentieth cubit cubits shekel shekels
ephah omer hin measures""".split())

SENT    = re.compile(r"[.!?;:]+")
SPEAKER = re.compile(r"^[A-Z][A-Z' .-]{1,30}\.\s*$", re.M)

def sentences(text):
    t = unicodedata.normalize("NFKD", text).replace("’","'").replace("‘","'")
    t = SPEAKER.sub(" ", t)
    for s in SENT.split(t):
        w = [x for x in re.sub(r"[^A-Za-z']+", " ", s).split() if x and x != "'"]
        if w: yield w

def background(paths):
    bg = set()
    for p in paths:
        for w in sentences(open(p, encoding="utf-8", errors="ignore").read()):
            lw = [x.lower() for x in w]
            for n in range(NMIN, NMAX+1):
                for i in range(len(lw)-n+1):
                    bg.add(" ".join(lw[i:i+n]))
    return bg

def extract(book_path, bg, top_coin=300, top_fp=100000):
    d = json.load(open(book_path, encoding="utf-8"))
    units = d["units"]
    nslice = max(1, len(units) // SLICES)

    raw, sents = [], []
    for idx, u in enumerate(units):
        sl = min(SLICES-1, idx // nslice)
        for w in sentences(u["text"]):
            raw.extend(w)
            sents.append(([x.lower() for x in w], u["id"], sl))

    cap, low = Counter(), Counter()
    for w in raw: (cap if w[0].isupper() else low)[w.lower()] += 1
    props = {w for w, n in cap.items() if low.get(w, 0) == 0}

    uni, wslices = Counter(), defaultdict(set)
    for lw, _, sl in sents:
        uni.update(lw)
        for x in lw: wslices[x].add(sl)
    total = sum(uni.values())
    if total < 2000:
        return None
    need = max(2, int(SLICES * MIN_SLICE_FR))

    ordinary = {w: (uni[w] >= MIN_WORD and w not in props and w not in NUMERAL
                    and len(wslices[w]) >= need) for w in uni}
    loose    = {w: (w not in props and w not in NUMERAL) for w in uni}

    cnt, strict, gslices, where = Counter(), {}, defaultdict(set), {}
    for lw, uid, sl in sents:
        for n in range(NMIN, NMAX+1):
            for i in range(len(lw)-n+1):
                g = lw[i:i+n]
                if not all(loose[x] for x in g): continue
                if sum(1 for x in g if x not in STOP_ONLY) < 2: continue
                k = " ".join(g)
                cnt[k] += 1; gslices[k].add(sl); where.setdefault(k, uid)
                if k not in strict: strict[k] = all(ordinary[x] for x in g)

    coin, fing = [], []
    for g, c in cnt.items():
        w = g.split(); n = len(w)
        if strict[g] and c <= MAX_COINAGE:
            exp = math.prod(uni[x]/total for x in w)
            if exp > 0:
                npmi = math.log((c/total)/exp + 1e-30) / (n - 1)
                coin.append({"phrase": g, "n": n, "count": c,
                             "surprise_per_join": round(npmi, 2),
                             "in_background": g in bg, "first_at": where[g],
                             "score": round(npmi + 0.5*math.log(n), 2)})
        if c >= MIN_FINGER and len(gslices[g]) >= MIN_FP_SLICES and g not in bg:
            fing.append({"phrase": g, "n": n, "count": c,
                         "slices": len(gslices[g]), "first_at": where[g],
                         "score": round(math.log(c)*math.log(len(gslices[g])+1)*n, 2)})

    def maximal(rows, top):
        rows.sort(key=lambda r: -r["score"])
        kept, seen = [], []
        for r in rows:
            if any(r["phrase"] in s for s in seen): continue
            kept.append(r); seen.append(r["phrase"])
            if len(kept) >= top: break
        return kept

    return {"slug": d.get("slug"), "title": d.get("title"), "author": d.get("author"),
            "words": total, "units": len(units),
            "coinages": maximal(coin, top_coin), "fingerprints": maximal(fing, top_fp)}
