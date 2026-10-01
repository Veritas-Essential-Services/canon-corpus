#!/usr/bin/env python3
# prov: 2026-10-01 claude drafted (Claude Code web session; model name withheld by session policy)
# fable_review: pending
"""
lemma_bridge_test.py -- the English lemma bridge (ADR 0012): archaic KJV forms
found by their modern words.

Run:  python3 tests/lemma_bridge_test.py

WHAT IT ASSERTS
    1. THE BUG. KJV Psalms + Proverbs (data/greppable/kjv.tsv) in a real SQLite
       FTS5 index with the stock porter stemmer: "show" finds 0 verses while
       "shew" finds 37; "help" misses Ps 86:17 ("hast holpen me"); "ordain"
       misses Ps 7:13 ("he ordaineth his arrows").
    2. THE FIX. pipeline/lemma_bridge.py expand_query() closes each one, and
       the two directions agree (show == shew, help == holpen).
    3. The forms named in the task, the homograph rule (bear finds bare, bare
       does not pull in bear), archaic_only, and FTS5 query syntax passing
       through (phrases, OR, brackets, prefix*).
    4. The committed table: every form has a lemma, a rule/source and a quote;
       review rows stay out of search.
    5. PARITY. exports/lemma-bridge/lemma-bridge.js gives the same MATCH string
       as the Python twin for every query here (needs Node; without it the test
       says so and that block does not run).
    6. With a Vocabularium checkout beside this repo, the build reproduces the
       committed files byte for byte (build_lemma_bridge.py --check).
"""
import json
import os
import shutil
import sqlite3
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "pipeline"))
import lemma_bridge as LB  # noqa: E402

PASS, FAIL = 0, []


def check(label, cond, detail=""):
    global PASS
    if cond:
        PASS += 1
        print("  PASS  " + label)
    else:
        FAIL.append(label)
        print("  FAIL  " + label + (("  -- " + str(detail)) if detail else ""))


# ---- the text, indexed the way the concordance indexes it
with open(os.path.join(REPO, "data", "greppable", "kjv.tsv"), encoding="utf-8") as f:
    next(f)
    verses = [l.rstrip("\n").split("\t", 1) for l in f]
verses = [v for v in verses if v[0].startswith(("kjv:Ps.", "kjv:Prov."))]
TEXT = dict(verses)
db = sqlite3.connect(":memory:")
db.execute("CREATE VIRTUAL TABLE v USING fts5(id UNINDEXED, text, tokenize='porter unicode61')")
db.executemany("INSERT INTO v VALUES (?, ?)", verses)


def refs(match):
    return [r[0] for r in db.execute("SELECT id FROM v WHERE v MATCH ? ORDER BY rowid", (match,))]


bridge = LB.load_bridge()


def search(q, **kw):
    return refs(LB.expand_query(q, bridge, **kw)[0])


print("\n--- the text ---")
check("Psalms (2,461) + Proverbs (915) = 3,376 verses", len(verses) == 3376, len(verses))

print("\n--- the bug, without the bridge ---")
check('plain FTS: "show" finds 0 verses', refs("show") == [], len(refs("show")))
check('plain FTS: "shew" finds 37 verses', len(refs("shew")) == 37, len(refs("shew")))
check('plain FTS: "help" misses Ps 86:17 ("hast holpen me")', "kjv:Ps.86.17" not in refs("help"))
check('plain FTS: "ordain" misses Ps 7:13 ("he ordaineth his arrows")', "kjv:Ps.7.13" not in refs("ordain"))

print("\n--- the fix ---")
show = search("show")
check('"show" finds all 37 "shew" verses', set(refs("shew")) <= set(show))
check('"show" finds Ps 19:1 ("the firmament sheweth his handywork")', "kjv:Ps.19.1" in show)
check('"shew" and "show" return the same verses', search("shew") == show)
check('a modern inflection ("showed") reaches the same family', search("showed") == show)
help_ = search("help")
check('"help" finds both "holpen" verses (Ps 86:17, 83:8)', {"kjv:Ps.86.17", "kjv:Ps.83.8"} <= set(help_))
check('"help" keeps every plain "help" verse', set(refs("help")) <= set(help_))
check('"holpen" returns the same verses as "help"', search("holpen") == help_)
ordain = search("ordain")
check('"ordain" finds Ps 7:13 ("ordaineth")', "kjv:Ps.7.13" in ordain)
check('"ordain" keeps its plain hits', set(refs("ordain")) <= set(ordain))

print("\n--- the forms named in the task ---")
for form, lemma in [("shew", "show"), ("shewn", "show"), ("holpen", "help"), ("spake", "speak"),
                    ("wist", "know"), ("wot", "know"), ("clave", "cleave"), ("gat", "get"),
                    ("brake", "break"), ("ordaineth", "ordain"), ("sayest", "say"), ("lovedst", "love"),
                    ("thee", "you"), ("thou", "you"), ("ye", "you"), ("thy", "your"), ("thine", "your")]:
    check("%s -> %s" % (form, lemma), form in LB.expand_word(lemma, bridge))
check("shewed reaches show through shew (porter does the -ed)", "shew" in LB.expand_word("show", bridge))

print("\n--- search behaviour ---")
check('"you" also finds thee / thou / ye', len(search("you")) > 5 * len(refs("you")),
      (len(search("you")), len(refs("you"))))
check('"bear" reaches "bare" (she bare a son)', "bare" in LB.expand_word("bear", bridge))
check('"bare" is a homograph: it does NOT pull in every "bear"', "bear" not in LB.expand_word("bare", bridge))
check('"see" does not pull in "say" (a 1913-only old sense, left in review)', "say" not in LB.expand_word("see", bridge))
check('"smite" reaches "smote"', "smote" in LB.expand_word("smite", bridge))
check("archaic_only drops went but keeps goeth",
      "went" not in LB.expand_word("go", bridge, archaic_only=True)
      and "went" in LB.expand_word("go", bridge)
      and "goeth" in LB.expand_word("go", bridge, archaic_only=True))
m, _ = LB.expand_query('"the LORD" show* OR mercy', bridge)
check("phrases, OR and prefix* pass through: " + m, m == '"the LORD" AND show* OR "mercy"')
check("that query runs in FTS5", len(refs(m)) > 0)
two = search("shew mercy")
check("two words are ANDed (every hit has a show/shew form and mercy/merciful)",
      two and all("merc" in TEXT[r].lower() and ("show" in TEXT[r].lower() or "shew" in TEXT[r].lower()) for r in two),
      len(two))
check("brackets and OR the user typed are kept: (help OR ordain)",
      len(search("(help OR ordain)")) == len(set(help_) | set(ordain)))
check("an empty query gives an empty match", LB.expand_query("", bridge)[0] == "")

print("\n--- the committed table ---")
forms = bridge["forms"]
check("%d forms" % len(forms), len(forms) > 1000)
check("every form has at least one lemma", all(e["lemmas"] for e in forms.values()))
check("every form names its rule and source and quotes it", all(e["rule"] and e["source"] and e["quote"] for e in forms.values()))
check("no form maps to itself", all(f not in e["lemmas"] for f, e in forms.items()))
with open(os.path.join(REPO, "data", "lemma_bridge", "needs_review.csv"), encoding="utf-8") as f:
    review = [l.split(",")[0] for l in f.read().splitlines()[1:]]
check('review rows stay out of search (seeth: the bridge keeps "see"; review holds Webster\'s "seethe")',
      [r for r in review if r in forms and r != "seeth"] == [])

print("\n--- parity: the browser function gives the same MATCH strings ---")
QUERIES = ["show", "shew", "showed", "help", "holpen", "helped", "ordain", "you", "bear", "bare", "see",
           "smite", "go", "shew mercy", '"the LORD" show* OR mercy', "(help OR ordain)", "", "Thou art"]
node = shutil.which("node")
if not node:
    print("  (Node not found: the JavaScript twin was not compared)")
else:
    js = """
const LB = require(%s); const b = JSON.parse(require('fs').readFileSync(%s, 'utf8'));
const qs = %s; const out = {};
for (const q of qs) { out[q] = [LB.expandQuery(q, b).match, LB.expandQuery(q, b, {archaicOnly: true}).match]; }
process.stdout.write(JSON.stringify(out));
""" % (json.dumps(os.path.join(REPO, "exports", "lemma-bridge", "lemma-bridge.js")),
       json.dumps(str(LB.TABLE)), json.dumps(QUERIES))
    got = json.loads(subprocess.run([node, "-e", js], capture_output=True, text=True, check=True).stdout)
    for q in QUERIES:
        py = [LB.expand_query(q, bridge)[0], LB.expand_query(q, bridge, archaic_only=True)[0]]
        check("same MATCH, default and archaic-only: %r" % q, got[q] == py, (got[q], py))

print("\n--- rebuild ---")
vocab = [d for d in (os.environ.get("VOCABULARIUM_DIR"), os.path.join(os.path.dirname(REPO), "vocabularium"),
                     os.path.join(os.path.dirname(REPO), "Vocabularium Website"))
         if d and os.path.exists(os.path.join(d, "data", "sources", "webster1913.json.gz"))]
if not vocab:
    print("  (no Vocabularium checkout beside this repo: the byte-identical rebuild was not run)")
else:
    r = subprocess.run([sys.executable, os.path.join(REPO, "pipeline", "build_lemma_bridge.py"),
                        "--check", "--vocabularium", vocab[0]], capture_output=True, text=True)
    check("build_lemma_bridge.py --check: the committed files rebuild byte for byte", r.returncode == 0,
          r.stdout[-200:] + r.stderr[-200:])

print()
if FAIL:
    print(f"{PASS} passed, {len(FAIL)} FAILED: {FAIL}")
    sys.exit(1)
print(f"{PASS} passed, 0 failed")
