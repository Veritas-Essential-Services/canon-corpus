#!/usr/bin/env python3
"""
xrefs.py -- look up the cross-reference layer by KJV verse.

    python3 pipeline/xrefs.py kjv:John.1.1      # its Treasury references, and what cites it

    import xrefs
    x = xrefs.Xrefs()
    x.treasury("kjv:Gen.1.1")    # [{"kw": "beginning", "refs": ["kjv:Prov.8.22-24", ...]}, ...]
    x.cited_by("kjv:John.1.1")   # [{"by": "kjv:Gen.1.1", "source": "tsk", "kw": ...},
                                 #  {"by": "<father's unit>", "source": "fathers-notes", ...}, ...]

cited_by() reads build/xrefs/cited-by.jsonl when it has been built (the
Treasury both ways, the fathers' notes, every book link to a verse); without
it, the Treasury's own references, reversed, from the committed data.
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tsk_read as T  # noqa: E402

TSK_FILE = os.path.join(ROOT, "data", "xrefs", "tsk.jsonl")
CITED_BY = os.path.join(ROOT, "build", "xrefs", "cited-by.jsonl")


class Xrefs:
    def __init__(self, tsk_file=TSK_FILE, cited_by_file=CITED_BY):
        self.rows = {}
        with open(tsk_file, encoding="utf-8") as f:
            for raw in f:
                r = json.loads(raw)
                self.rows[r["verse"]] = r
        self._cb_file = cited_by_file if os.path.exists(cited_by_file) else None
        self._cb = None

    def treasury(self, verse):
        r = self.rows.get(verse)
        return r["groups"] if r else []

    def _load_cited_by(self):
        if self._cb is not None:
            return
        self._cb = collections.defaultdict(list)
        if self._cb_file:
            with open(self._cb_file, encoding="utf-8") as f:
                for raw in f:
                    r = json.loads(raw)
                    self._cb[r["verse"]] = r["by"]
            return
        V = T.Verses(T.kjv_shape())
        for v, r in self.rows.items():
            for g in r["groups"]:
                for rid in g["refs"]:
                    b, c, vv, c2, v2 = T.parse_ref_id(rid)
                    for k in range(V.index[(b, c, vv)], V.index[(b, c2, v2)] + 1):
                        self._cb["kjv:%s.%d.%d" % V.seq[k]].append({"by": v, "source": "tsk", "kw": g["kw"]})

    def cited_by(self, verse):
        self._load_cited_by()
        return self._cb.get(verse, [])


if __name__ == "__main__":
    x = Xrefs()
    for v in sys.argv[1:]:
        print(v)
        for g in x.treasury(v):
            print(f"  {g['kw'] or '-'}: {', '.join(g['refs'])}")
        cb = x.cited_by(v)
        by = collections.Counter(c["source"] for c in cb)
        print(f"  cited by {len(cb)}: {dict(by)}")
        for c in cb[:12]:
            print("   ", c["source"], c["by"])
