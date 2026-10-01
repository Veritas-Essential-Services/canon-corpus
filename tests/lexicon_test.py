#!/usr/bin/env python3
# prov: 2026-10-01 claude-opus-5-5 drafted
"""data/lexicons/webster1913.json.gz: present, the documented hash, and sane entries."""
import gzip, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "data", "lexicons", "webster1913.json.gz")
fails = 0
def ok(c, m):
    global fails
    print(("ok    " if c else "FAIL  ") + m)
    if not c: fails += 1
raw = gzip.open(P).read()
d = json.loads(raw)
ok(hashlib.sha256(raw).hexdigest() == "bbcce71688ef05aaa75fbeee65176c2db778426a2732b7e653197d8b26a52861",
   "uncompressed JSON matches the sha256 in data/lexicons/README.md")
ok(len(d) == 90143, "90,143 headwords")
ok(all(k == k.lower() for k in d), "every headword is lowercase")
ok(all(isinstance(v, list) and v and all("d" in s for s in v) for v in d.values()), "every entry has at least one sense")
ok(d["corybantic"][0]["p"] == "adj.", "corybantic is there (Heretics ch. VI)")
ok("pulchritude" in d, "pulchritude is there")
sys.exit(1 if fails else 0)
