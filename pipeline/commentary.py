#!/usr/bin/env python3
"""
commentary.py -- look up the commentary layer by KJV verse.

    python3 pipeline/commentary.py kjv:John.3.16     # the comments on it, and the comments that cite it

    import commentary
    c = commentary.Commentary()
    c.on("kjv:Gen.1.1")       # [{"work": "henry", "id": "henry:Gen.1.1-2", ...}, ...]  comments on the verse
    c.citing("kjv:Gen.1.1")   # comments elsewhere that cite it (or list it in Poole's margin)
    c.text("jfb:Gen.1.1")     # the prose, when build/commentary/ has been built

A comment on a passage is on every verse of it; a citation of a range cites
every verse in it.
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tsk_read as T  # noqa: E402

DATA = os.path.join(ROOT, "data", "commentary")
BUILD = os.path.join(ROOT, "build", "commentary")
WORKS = ("henry", "jfb", "poole", "barnes", "wesley", "calvin", "hodge", "manton", "trapp", "clarke")


class Commentary:
    def __init__(self, data=DATA, build=BUILD):
        self.rows = {}
        self._build = build
        self._text = {}
        V = T.Verses(T.kjv_shape())

        def verses(rid):
            b, c, v, c2, v2 = T.parse_ref_id(rid)
            return ("kjv:%s.%d.%d" % V.seq[k] for k in range(V.index[(b, c, v)], V.index[(b, c2, v2)] + 1))
        self._on = collections.defaultdict(list)
        self._citing = collections.defaultdict(list)
        for w in WORKS:
            with open(os.path.join(data, w + ".jsonl"), encoding="utf-8") as f:
                for raw in f:
                    r = json.loads(raw)
                    r["work"] = w
                    self.rows[r["id"]] = r
                    for v in verses(r["on"]):
                        self._on[v].append(r)
                    for kind in ("cites", "parallels"):
                        for rid in r.get(kind, []):
                            for v in verses(rid):
                                self._citing[v].append({"work": w, "id": r["id"], "on": r["on"], "as": kind, "ref": rid})

    def on(self, verse):
        return self._on.get(verse, [])

    def citing(self, verse):
        return self._citing.get(verse, [])

    def entry(self, uid):
        return self.rows.get(uid)

    def text(self, uid):
        w = uid.split(":")[0]
        if w not in self._text:
            self._text[w] = {}
            p = os.path.join(self._build, w + ".text.jsonl")
            if os.path.exists(p):
                with open(p, encoding="utf-8") as f:
                    for raw in f:
                        r = json.loads(raw)
                        self._text[w][r["id"]] = r.get("text") or "\n".join(r.get("notes", []))
        return self._text[w].get(uid)


if __name__ == "__main__":
    c = Commentary()
    for v in sys.argv[1:]:
        on, cit = c.on(v), c.citing(v)
        print(f"{v}: {len(on)} comments on it, {len(cit)} citing it")
        for r in on:
            print(f"  on      {r['id']}  ({len(r['cites'])} citations)")
        for h in cit[:40]:
            print(f"  cited   {h['id']}  ({h['as']}: {h['ref']})")
        if len(cit) > 40:
            print(f"  ... and {len(cit) - 40} more")
