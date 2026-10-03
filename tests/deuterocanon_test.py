#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""data/versification/deuterocanon.json and data/parallel/deuterocanon-parallel.tsv:
the deuterocanon's shared key (the KJV's Apocrypha verse) for the Vulgate, the
Douay and Brenton. Offline, no corpus needed. The rebuild is
build_deuterocanon.py --check (it needs the built books)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import versification as V

fails = passed = 0
def check(m, c):
    global fails, passed
    print(("ok    " if c else "FAIL  ") + m)
    if c: passed += 1
    else: fails += 1

ROOT = os.path.join(HERE, "..")
m = json.load(open(os.path.join(ROOT, "data", "versification", "deuterocanon.json"), encoding="utf-8"))
with open(os.path.join(ROOT, "data", "parallel", "deuterocanon-parallel.tsv"), encoding="utf-8") as f:
    lines = f.read().split("\n")
head = lines[0].split("\t")
rows = {}
for line in lines[1:]:
    if line:
        cells = line.split("\t")
        rows[cells[0]] = {c: (cells[i].split(" ") if cells[i] else []) for i, c in enumerate(head)}
C = lambda k, col: rows[k][col]
R = lambda ref, w: V.resolve_dc(ref, w, m)
W = m["witnesses"]

check("columns: the KJV Apocrypha key, then the Vulgate, the Douay and Brenton",
      head == ["kjva", "vulgate", "douay", "brenton"])
check("one row per KJV Apocrypha verse, 5,722, as the key's book counts say",
      len(rows) == 5722 == sum(m["key"]["books"].values()))
check("the key is public domain and pinned by sha256",
      m["rights"]["license"] == "public-domain" and len(m["key"]["sha256"]) == 64)
check("every witness is one of the three, each with counts that add up",
      set(W) == {"vulgate", "douay", "brenton"}
      and all(w["counts"]["keyed"] + w["counts"]["no_key"] == w["counts"]["verses"] for w in W.values()))

# Known pairs, each read in both texts.
def is_(ref, w, *ks):
    r = R(ref, w)
    return bool(r) and r["resolved"] and r.get("spans", [r["target"]]) == [f"kjva:{k}" for k in ks]
check("Brenton's Sirach 33:12 is the KJV's 30:25 (the Greek's displaced block)",
      is_("Sir.33.12", "brenton", "Sir.30.25"))
check("Brenton's Epistle of Jeremy 1:5 is the KJV's Baruch 6:5", is_("EpJer.1.5", "brenton", "Bar.6.5"))
check("the Vulgate's Daniel 3:24 opens the Song of the Three (PrAzar 1)",
      is_("Dan.3.24", "vulgate", "PrAzar.1.1"))
check("the Douay's Daniel 13:1 is Susanna 1", is_("Dan.13.1", "douay", "Sus.1.1"))
check("the Douay's Esther 11:2 is the KJV's Rest of Esther 11:2",
      is_("Esth.11.2", "douay", "AddEsth.11.2"))
check("Brenton's Esther 1:1 is Mordecai's dream, the KJV's Rest of Esther 11:2",
      is_("Esth.1.1", "brenton", "AddEsth.11.2"))
check("a verse outside the deuterocanon is not covered (it is keyed to the KJV instead)",
      R("Esth.1.2", "brenton") is None and R("Gen.1.1", "vulgate") is None)
r = R("3Macc.1.1", "brenton")
check("3 Maccabees has no key and says why", r and not r["resolved"] and "3 Maccabees" in r["why"])
r = R("Ps.151.1", "brenton")
check("Psalm 151 has no key and says why", r and not r["resolved"] and "151" in r["why"])

# The Vulgate is keyed through the Douay.
vk = {k: r["vulgate"] for k, r in rows.items()}
dk = {k: r["douay"] for k, r in rows.items()}
diff = {k for k in rows if vk[k] != dk[k]}
check("the Vulgate's and the Douay's keys agree verse for verse, except where the Douay file "
      "prints the Epistle of Jeremy's 6:37 in the slot of 6:7",
      diff == {"Bar.6.8", "Bar.6.38"} and C("Bar.6.38", "vulgate") == ["Bar.6.37"]
      and C("Bar.6.38", "douay") == ["Bar.6.7"] and C("Bar.6.8", "vulgate") == ["Bar.6.7"]
      and C("Bar.6.8", "douay") == [])
vg = V.load(V.VULGATE_PATH)
def expand(runs):
    out = set()
    for x in runs:
        b, c, v = x.split(".")
        if "-" in v:
            a, z = v.split("-")
            out |= {f"{b}.{c}.{n}" for n in range(int(a), int(z) + 1)}
        else:
            out.add(x)
    return out
check("the Vulgate's deuterocanon is as many verses as its KJV map names as having no KJV verse",
      W["vulgate"]["counts"]["verses"] == sum(r["count"] for r in vg["no_kjv_verse"]))
check("Jerome's Tobit and Judith: the Douay's unkeyed verses there say so",
      any(("Tob" in r["verses"][0] or "Jdt" in r["verses"][0]) and "Jerome" in r["why"]
          for r in W["douay"]["no_key"]))

# The house rows, each read in both texts.
hr = W["brenton"]["house_rows"]
check("Brenton's house rows are all present and in the index",
      set(hr) == {"Esth.4.17o", "Esth.8.12c", "Esth.8.12d", "Dan.3.72a", "Esth.5.1", "Esth.5.2",
                  "Sir.30.13b", "Sir.36.16", "Sir.1.1", "Sir.1.1a", "Sir.1.1b", "Sir.1.1c",
                  "Sir.1.1g"}
      and all(v in C(k, "brenton") for v, h in hr.items() for k in h["kjva"]))
check("Brenton's Dan 3:72a is the KJV's Song of the Three 45 (winter and summer)",
      C("PrAzar.1.45", "brenton") == ["Dan.3.72a"])

# Found by reading the weakest pairings and every far-flung key (2026-10-03).
check("review: Brenton's Sir 1:1-1:1g is the translator's prologue, the KJV's Sir 0.2; "
      "Brenton has no other prologue, so the KJV's first (0.1) is empty in its column",
      all(is_(v, "brenton", "Sir.0.2") for v in ("Sir.1.1", "Sir.1.1a", "Sir.1.1d", "Sir.1.1g"))
      and C("Sir.0.1", "brenton") == [] and is_("Sir.1.1h", "brenton", "Sir.1.1"))
check("review: Brenton's Sir 30:13b is the KJV's 30:12, not 7:23", is_("Sir.30.13b", "brenton", "Sir.30.12"))
check("review: the Douay's Sir 9:21 is 9:14, not 29:20; 20:14 is 20:14, not 18:18",
      is_("Sir.9.21", "douay", "Sir.9.14") and is_("Sir.20.14", "douay", "Sir.20.14"))
check("review: the Douay's Tob 9:3-8 sit in the KJV's 9:2-6, not chapters 7 and 10",
      is_("Tob.9.3", "douay", "Tob.9.2") and is_("Tob.9.4", "douay", "Tob.9.4")
      and is_("Tob.9.5", "douay", "Tob.9.3") and is_("Tob.9.8", "douay", "Tob.9.6"))
check("review: Jdt 13:31 (Douay) is the KJV's 14:7; Jdt 14:11 is 14:12-13",
      is_("Jdt.13.31", "douay", "Jdt.14.7") and is_("Jdt.14.11", "douay", "Jdt.14.12", "Jdt.14.13"))
r = R("Esth.15.3", "douay")
check("review: Mordecai's charge (Vulgate Esth 15:3) has no key and says why",
      r and not r["resolved"] and "4:8" in r["why"])
check("review: Latin-only verses (Sir 3:1, 23:31; Tob 1:15) have no key",
      all(not R(x, "douay")["resolved"] and "the Vulgate's Latin has this" in R(x, "douay")["why"]
          for x in ("Sir.3.1", "Sir.23.31", "Tob.1.15")))
check("every Douay house row is listed with its why", len(W["douay"]["house_rows"]) >= 30
      and all(h["why"] for h in W["douay"]["house_rows"].values()))

# The map and the index agree.
ok = True
for name, w in W.items():
    for k, r in rows.items():
        for ref in r[name]:
            res = R(ref, name)
            if not res or not res["resolved"] or f"kjva:{k}" not in res.get("spans", [res["target"]]):
                if not (name in hr and ref in hr):
                    ok = False
check("every ref in the index resolves through resolve_dc to that row's key", ok)
check("in the books each witness has, its empty index cells are exactly the KJV verses its map names",
      all({k for k, r in rows.items() if not r[n] and k.split(".")[0] in W[n]["kjva_books_read"]}
          == expand(W[n]["kjva_without_verse"]) for n in W))
check("weak pairings are few in Brenton (both Englished from the Greek) and flagged",
      W["brenton"]["counts"]["weak"] <= 5 and R("Sir.33.12", "brenton").get("weak") is None)

print(f"\n{passed} passed, {fails} failed")
sys.exit(1 if fails else 0)
