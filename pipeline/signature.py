"""
signature.py -- extract a work's SIGNATURE PHRASES: the ones that carry an idea.

Not rare strings, not keywords, not proper nouns. The target is the phrase built
entirely out of ordinary words whose COMBINATION is unique -- "the valley of the
shadow of death," "a still small voice," "faith, hope, charity."

Five conditions. The last two are the ones that do the real work:

  1. rare as a whole       -- occurs a handful of times, not a formula
  2. common in its parts   -- every component word is ordinary in this work
  3. surprising            -- far rarer than its own words predict (normalised PMI,
                              so an 8-gram cannot outscore a 4-gram by length alone)
  4. not a proper noun     -- names are a separate channel
  5. WIDELY DISPERSED words -- every component word appears across many books.

Condition 5 is what separates an idea from a procedure. "Mercy," "death" and
"light" turn up all over a corpus; "scall," "ephah" and "bright spot" live in one
technical chapter. Dispersion is abstractness, measured rather than guessed --
no hand-written list of "idea words," and no thumb on the scale for the books we
happen to find interesting.
"""
import json, math, re, sys, unicodedata
from collections import Counter, defaultdict

NMIN, NMAX = 3, 6
MAX_COUNT  = 4      # more often than this and it is a formula, not a coinage
MIN_WORD   = 25     # a component word rarer than this is not "ordinary"
MIN_BOOKS  = 12     # a component word must range across at least this many books

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

def book_of(uid):
    """kjv:Gen.1.1 -> Gen ; shakespeare:hamlet.2.2.1 -> hamlet"""
    tail = uid.split(":", 1)[-1]
    return tail.split(".", 1)[0]

def bg_grams(paths):
    seen = set()
    for p in paths:
        for w in sentences(open(p, encoding="utf-8", errors="ignore").read()):
            lw = [x.lower() for x in w]
            for n in range(NMIN, NMAX+1):
                for i in range(len(lw)-n+1):
                    seen.add(" ".join(lw[i:i+n]))
    return seen

def run(book_path, bg_paths, out_path):
    units = json.load(open(book_path, encoding="utf-8"))["units"]

    raw, sents = [], []
    for u in units:
        for w in sentences(u["text"]):
            raw.extend(w)
            sents.append(([x.lower() for x in w], u["id"]))

    cap, low = Counter(), Counter()
    for w in raw: (cap if w[0].isupper() else low)[w.lower()] += 1
    props = {w for w, n in cap.items() if low.get(w, 0) == 0}

    uni, spread = Counter(), defaultdict(set)
    for lw, uid in sents:
        b = book_of(uid)
        uni.update(lw)
        for x in lw: spread[x].add(b)
    total = sum(uni.values())

    def ordinary(x):
        return (uni[x] >= MIN_WORD and x not in props
                and x not in NUMERAL and len(spread[x]) >= MIN_BOOKS)

    count, where = Counter(), {}
    for lw, uid in sents:
        ok = [ordinary(x) for x in lw]
        for n in range(NMIN, NMAX+1):
            for i in range(len(lw)-n+1):
                if not all(ok[i:i+n]): continue
                g = lw[i:i+n]
                if sum(1 for x in g if x not in STOP_ONLY) < 2: continue
                k = " ".join(g)
                count[k] += 1
                where.setdefault(k, uid)
    sys.stderr.write(f"candidate phrases: {len(count):,}\n")

    bg = bg_grams(bg_paths)
    sys.stderr.write(f"background phrases: {len(bg):,}\n")

    scored = []
    for g, c in count.items():
        if c > MAX_COUNT: continue
        w = g.split(); n = len(w)
        exp = math.prod(uni[x]/total for x in w)
        if exp <= 0: continue
        npmi = math.log((c/total)/exp + 1e-30) / (n - 1)
        scored.append({"phrase": g, "n": n, "count": c,
                       "surprise_per_join": round(npmi, 2),
                       "rarest_word": min(w, key=lambda x: uni[x]),
                       "rarest_word_freq": min(uni[x] for x in w),
                       "in_background": g in bg,
                       "first_at": where[g],
                       "score": round(npmi + 0.5*math.log(n), 2)})
    scored.sort(key=lambda r: -r["score"])

    def maximal(rows, top):
        kept, seen = [], []
        for r in rows:
            if any(r["phrase"] in s for s in seen): continue
            kept.append(r); seen.append(r["phrase"])
            if len(kept) >= top: break
        return kept

    native  = maximal([r for r in scored if not r["in_background"]], 300)
    entered = maximal([r for r in scored if r["in_background"]], 150)

    with open(out_path, "w", encoding="utf-8") as f:
        for r in native + entered: f.write(json.dumps(r, ensure_ascii=False)+"\n")
    sys.stderr.write(f"{len(native)} distinctive + {len(entered)} entered-the-language "
                     f"-> {out_path}\n")
    return native, entered

if __name__ == "__main__":
    native, entered = run(sys.argv[1], sys.argv[3].split(","), sys.argv[2])
    print(f"\n=== SIGNATURE PHRASES — absent from ordinary English prose ===")
    for r in native[:45]:
        print(f"  {r['score']:>5} x{r['count']}  {r['phrase']:<46} [{r['first_at']}]")
    print(f"\n=== PHRASES THAT ENTERED THE LANGUAGE — also found in the background prose ===")
    for r in entered[:30]:
        print(f"  {r['score']:>5} x{r['count']}  {r['phrase']:<46} [{r['first_at']}]")
