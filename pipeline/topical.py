#!/usr/bin/env python3
"""
topical.py -- look up the topical and dictionary layer by KJV verse.

    python3 pipeline/topical.py kjv:John.3.16     # every Nave / Torrey / Easton / Smith place that cites it

    import topical
    t = topical.Topical()
    t.by_verse("kjv:Gen.1.1")   # [{"work": "nave", "id": "nave:creation", "term": "CREATION", "path": [...]}, ...]
    t.entry("easton:abdon")     # the committed row
    t.text("easton:abdon")      # the dictionary's prose, when build/topical/ has been built

A reference that is a range or a whole chapter cites every verse in it.
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tsk_read as T  # noqa: E402

DATA = os.path.join(ROOT, "data", "topical")
BUILD = os.path.join(ROOT, "build", "topical")
WORKS = ("nave", "torrey", "easton", "smith")


class Topical:
    def __init__(self, data=DATA, build=BUILD):
        self.rows = {}
        self._build = build
        self._text = None
        V = T.Verses(T.kjv_shape())
        self._by = collections.defaultdict(list)
        for w in WORKS:
            with open(os.path.join(data, w + ".jsonl"), encoding="utf-8") as f:
                for raw in f:
                    r = json.loads(raw)
                    self.rows[r["id"]] = r
                    places = r["topics"] if "topics" in r else [{"path": [], "refs": r["refs"]}]
                    for t in places:
                        for rid in t["refs"]:
                            b, c, v, c2, v2 = T.parse_ref_id(rid)
                            for k in range(V.index[(b, c, v)], V.index[(b, c2, v2)] + 1):
                                self._by["kjv:%s.%d.%d" % V.seq[k]].append(
                                    {"work": w, "id": r["id"], "term": r["term"], "path": t["path"], "ref": rid})

    def by_verse(self, verse):
        return self._by.get(verse, [])

    def entry(self, uid):
        return self.rows.get(uid)

    def text(self, uid):
        if self._text is None:
            self._text = {}
            for w in ("easton", "smith"):
                p = os.path.join(self._build, w + ".text.jsonl")
                if os.path.exists(p):
                    with open(p, encoding="utf-8") as f:
                        for raw in f:
                            r = json.loads(raw)
                            self._text[r["id"]] = r["text"]
        return self._text.get(uid)


if __name__ == "__main__":
    t = Topical()
    for v in sys.argv[1:]:
        hits = t.by_verse(v)
        print(f"{v}: {len(hits)} places")
        for h in hits:
            print(f"  {h['work']:7} {h['term']}" + (" > " + " > ".join(h["path"]) if h["path"] else "") + f"  ({h['ref']})")
