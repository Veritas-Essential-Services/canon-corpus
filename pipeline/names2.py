"""
names2.py -- the onomastic channel, done by evidence rather than by capital letters.

Capitalisation cannot identify a name in verse: Shakespeare capitalises the
first word of every line, so "Howl" and "Wormwood" look exactly like "Jephthah".
The test that does work: a proper noun is a word that is NEVER seen lowercase.
"""
import json, re, sys
from collections import defaultdict, Counter

WORD = re.compile(r"\b([A-Za-z]{3,})\b")

def cases(text, cap, low):
    for m in WORD.finditer(text):
        w = m.group(1)
        (cap if w[0].isupper() else low)[w.lower()] += 1

def main(kjv_path, tgt_path, bg_paths, out_path, max_verses=40, max_uses=20):
    kjv = json.load(open(kjv_path, encoding="utf-8"))["units"]
    tgt = json.load(open(tgt_path, encoding="utf-8"))["units"]

    kcap, klow = Counter(), Counter()
    where = defaultdict(set)
    for u in kjv:
        cases(u["text"], kcap, klow)
        for m in WORD.finditer(u["text"]):
            if m.group(1)[0].isupper():
                where[m.group(1).lower()].add(u["id"])

    # a KJV proper noun: always capitalised in the KJV, never lowercase
    names = {w for w, n in kcap.items() if n >= 1 and klow.get(w, 0) == 0}
    names = {w for w in names if 1 <= len(where[w]) <= max_verses}
    sys.stderr.write(f"kjv proper nouns (rare): {len(names):,}\n")

    # and unknown to ordinary English: drop anything the background ever uses
    bcap, blow = Counter(), Counter()
    for p in bg_paths:
        cases(open(p, encoding="utf-8", errors="ignore").read(), bcap, blow)
    names = {w for w in names if (bcap.get(w,0) + blow.get(w,0)) == 0}
    sys.stderr.write(f"after background: {len(names):,}\n")

    # and not an ordinary word in the target either (kills line-start capitals)
    tcap, tlow = Counter(), Counter()
    for u in tgt: cases(u["text"], tcap, tlow)
    names = {w for w in names if tlow.get(w,0) == 0}
    sys.stderr.write(f"after target-lowercase test: {len(names):,}\n")

    rows, tally = [], Counter()
    for u in tgt:
        for m in {x.group(1) for x in WORD.finditer(u["text"]) if x.group(1)[0].isupper()}:
            w = m.lower()
            if w in names:
                tally[w] += 1
                rows.append({"target_id": u["id"], "target_ref": u.get("ref",""),
                             "name": m, "kjv_verses": sorted(where[w])[:8],
                             "kjv_verse_count": len(where[w]),
                             "text": " ".join(u["text"].split())[:200]})
    rows = [r for r in rows if tally[r["name"].lower()] <= max_uses]
    rows.sort(key=lambda r: (tally[r["name"].lower()], r["kjv_verse_count"]))
    with open(out_path,"w",encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False)+"\n")
    sys.stderr.write(f"{len(rows)} hits, {len({r['name'] for r in rows})} distinct names\n")
    return rows, tally

if __name__ == "__main__":
    rows, tally = main(sys.argv[1], sys.argv[2], sys.argv[3].split(","), sys.argv[4])
    seen=set()
    print("\ndistinct biblical names found in Shakespeare (rarest first):")
    for r in rows:
        if r["name"] in seen: continue
        seen.add(r["name"])
        print(f"  {r['name']:<13} {tally[r['name'].lower()]}x in Shakespeare, "
              f"{r['kjv_verse_count']} KJV verses -> {r['kjv_verses'][0]}  [{r['target_id']}]")
