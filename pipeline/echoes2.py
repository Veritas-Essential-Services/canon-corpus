"""
echoes2.py — rarity-weighted text-reuse detection with a background control.

The whole difficulty: a shared phrase is only evidence of borrowing if it is
rare in ORDINARY ENGLISH. Rarity inside the source alone is not enough --
"God save the King" occurs in few Bible verses but in a great deal of English,
so it is a formula, not a quotation. So three filters, not one:

  1. rare in the SOURCE      -> the phrase can locate a passage
  2. absent from BACKGROUND  -> the phrase is not just period idiom
  3. rare in the TARGET      -> the phrase is not the author's own habit
"""
import json, re, sys, unicodedata
from collections import defaultdict

N = 4
MAX_SRC = 6        # in at most this many source units
MAX_BG  = 0        # must not appear in the background corpora at all
MAX_TGT = 3        # in at most this many target windows (else it's the author's own tic)
WINDOW  = 3

STOP = set("""a about after all also am an and any are as at be been before being but by can
did do does down for from had has have he her here him his how i if in into is it its me
more most my no nor not now of off on one only or other our out over own said say see shall
she so some such than that the thee thy their them then there these they thine this those
thou to too unto up upon us was we were what when where which while who whom why will with
would ye yea yet you your are art hath doth let make made man men come came go went know
good great god lord king day time thing let'""".split())

SPEAKER = re.compile(r"^[A-Z][A-Z' .ÆŒ-]{1,30}\.\s*$", re.M)

def norm_words(s):
    s = unicodedata.normalize("NFKD", s).replace("’","'").replace("‘","'")
    s = SPEAKER.sub(" ", s).lower()
    return [w for w in re.sub(r"[^a-z']+", " ", s).split() if w and w != "'"]

def grams(w, n=N):
    return [tuple(w[i:i+n]) for i in range(len(w)-n+1)]

def informative(g):
    return sum(1 for w in g if w not in STOP) >= 2

def longest_run(a, b):
    pos = defaultdict(list)
    for j, w in enumerate(b): pos[w].append(j)
    best, prev = 0, {}
    for w in a:
        cur = {}
        for j in pos.get(w, ()):
            cur[j] = prev.get(j-1, 0) + 1
            best = max(best, cur[j])
        prev = cur
    return best

def background_grams(paths):
    bg = set()
    for p in paths:
        w = norm_words(open(p, encoding="utf-8", errors="ignore").read())
        bg |= set(grams(w))
        sys.stderr.write(f"  bg {p.split('/')[-1]}: {len(w):,} words, running set {len(bg):,}\n")
    return bg

def run(src_path, tgt_path, bg_paths, out_path, min_hits=2, min_run=5):
    src = json.load(open(src_path, encoding="utf-8"))["units"]
    tgt = json.load(open(tgt_path, encoding="utf-8"))["units"]

    sys.stderr.write("background:\n")
    bg = background_grams(bg_paths)

    src_idx, src_txt = defaultdict(list), {}
    for u in src:
        w = norm_words(u["text"]); src_txt[u["id"]] = w
        for g in set(grams(w)):
            if informative(g) and g not in bg:
                src_idx[g].append(u["id"])
    rare = {g: v for g, v in src_idx.items() if len(v) <= MAX_SRC}
    sys.stderr.write(f"source: {len(src_idx):,} informative non-background {N}-grams, "
                     f"{len(rare):,} locating\n")

    wins = []
    for i in range(len(tgt)):
        c = tgt[i:i+WINDOW]
        wins.append((c[0]["id"], c[-1]["id"], " ".join(x["text"] for x in c), c[0].get("ref","")))

    tgt_df = defaultdict(int)
    win_words = []
    for _, _, text, _ in wins:
        w = norm_words(text); win_words.append(w)
        for g in set(grams(w)):
            if g in rare: tgt_df[g] += 1

    results, seen_phrase = [], {}
    for (a, b, text, ref), w in zip(wins, win_words):
        hits = defaultdict(set)
        for g in grams(w):
            if g in rare and tgt_df[g] <= MAX_TGT:
                for vid in rare[g]: hits[vid].add(g)
        for vid, gs in hits.items():
            r = longest_run(w, src_txt[vid])
            if len(gs) < min_hits or r < min_run: continue
            key = (vid, tuple(sorted(gs)))
            score = len(gs) + r * 0.6
            if key in seen_phrase and seen_phrase[key]["score"] >= score: continue
            seen_phrase[key] = {"target_id": a, "target_through": b, "target_ref": ref,
                                "source_id": vid, "shared_ngrams": len(gs),
                                "longest_run": r, "score": round(score,2),
                                "shared": [" ".join(g) for g in sorted(gs)][:6],
                                "target_text": " ".join(text.split())[:320]}
    results = sorted(seen_phrase.values(), key=lambda x: -x["score"])
    with open(out_path,"w",encoding="utf-8") as f:
        for r in results: f.write(json.dumps(r, ensure_ascii=False)+"\n")
    sys.stderr.write(f"{len(results)} candidate echoes -> {out_path}\n")

if __name__ == "__main__":
    src, tgt, out = sys.argv[1], sys.argv[2], sys.argv[3]
    bgs = sys.argv[4].split(",")
    run(src, tgt, bgs, out,
        int(sys.argv[5]) if len(sys.argv)>5 else 2,
        int(sys.argv[6]) if len(sys.argv)>6 else 5)
