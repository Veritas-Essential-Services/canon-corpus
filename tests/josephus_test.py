#!/usr/bin/env python3
"""
josephus_test.py -- the validator for the Josephus books
(pipeline/build_josephus.py; Niese's Greek and Whiston's English, from PerseusDL).

    python3 tests/josephus_test.py

OFFLINE (always): the committed manifest entries (rights block, CC BY-SA
label, alignment counts), the pins, and the numbering rules on fixtures.

AGAINST THE PINNED TEI (when data/corpus/perseus-josephus/ holds it and
data/nt/ is built): a rebuild equals every manifest entry, every Whiston unit
has its counterpart, both files begin each unit at the same Niese section
(two known exceptions, named), and the famous passages are where they belong.
"""
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "pipeline"))
import build_josephus as J  # noqa: E402

PASS = FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"ok   {label}")
    else:
        FAIL += 1
        print(f"FAIL {label}  {detail}")


EXPECTED = {"ant": (1444, 20), "war": (707, 0), "life": (76, 0), "apion": (77, 0)}  # Whiston units, Greek-only .arg
# Niese section where a Whiston unit begins, Greek vs English: the two places they
# differ, both read. Ant. 12.3.1: the Greek's milestone sits one section later.
# Ant. 17.13.1: the English keys its piece "17.13", a slip for 17.339.
NIESE_START_EXCEPTIONS = {("12", "3", "1"), ("17", "13", "1")}

print("--- manifest")
man = json.load(open(J.MANIFEST, encoding="utf-8"))
slugs = [f"josephus-{w}-{ed}" for w, *_ in J.WORKS for ed in J.EDITIONS]
check("eight books: four works, Greek and English", len(slugs) == 8 and all(s in man for s in slugs),
      [s for s in slugs if s not in man])
check("every entry carries the rights block: CC BY-SA 4.0, PD text, not served whole",
      all(man[s]["rights"]["redistribute_whole"] is False and "CC BY-SA 4.0" in man[s]["rights"]["license"]
          and J.COMMIT in man[s]["rights"]["source_url"] for s in slugs if s in man))
for w, (n, arg) in EXPECTED.items():
    g, e = man.get(f"josephus-{w}-niese", {}), man.get(f"josephus-{w}-whiston", {})
    check(f"{w}: {n} Whiston units in each language, all aligned (+{arg} Greek-only summaries)",
          e.get("units") == n and e["alignment"]["matched"] == n and not e["alignment"]["unmatched"]
          and g.get("units") == n + arg and g["alignment"]["matched"] == n
          and all(x.endswith(".arg") for x in g["alignment"]["unmatched"]),
          (g.get("units"), e.get("units")))
check("the Greek books carry Strong's tagging counts; the English do not",
      all("tagging" in man[f"josephus-{w}-niese"] and "tagging" not in man[f"josephus-{w}-whiston"]
          for w in EXPECTED))
check("books are gitignored (CC BY-SA, rule 6)",
      "data/books/*.json" in open(os.path.join(REPO, ".gitignore"), encoding="utf-8").read())
pins = J.pins()
check("all eight TEI files are pinned by sha256",
      len(pins) == 8 and all(re.fullmatch(r"[0-9a-f]{64}", v) for v in pins.values()))

print("--- numbering rules, on fixtures")
check("Whiston order: sections run on, chapters restart at 1",
      J.check_order("t", "t", [("1", "pr", "1"), ("1", "pr", "2"), ("1", "1", "1"), ("1", "1", "2"),
                               ("1", "2", "1"), ("2", "arg"), ("2", "1", "1")]) is None)
try:
    J.check_order("t", "t", [("5", "6", "7"), ("5", "8", "1")])
    stopped = False
except SystemExit:
    stopped = True
check("a skipped chapter (Ant. 5: 6, 8, 8 as Perseus keyed the English) stops the build", stopped)
check("every FIXES row names its file", all(k[1] in J.EDITIONS and k[0] in EXPECTED for k in J.FIXES))

# Lengths of a plausible run of sections; the English ~1.3x the Greek, with noise.
_g = [400, 1200, 300, 2500, 700, 150, 1800, 900, 350, 2200, 600, 1300, 500, 1600, 250, 1000]
_e = [int(x * 1.3 * f) for x, f in zip(_g, [1, .9, 1.1, 1, .95, 1.2, 1, 1.05, .9, 1, 1.1, .95, 1, 1, 1.15, 1])]
_k = [("1", "1", str(i + 1)) for i in range(len(_g))]
check("shift check: an aligned run reports nothing",
      J.shift_runs([(k, "x" * g, "x" * e) for k, g, e in zip(_k, _g, _e)]) == [])
# Ant. 8's shape: English 4 also holds Greek 5, English 5-11 hold Greek 6-12, and
# English 12-13 split Greek 13 between them; aligned again from 14.
_slid = _e[:3] + [_e[3] + _e[4]] + _e[5:12] + [_e[12] // 2, _e[12] // 2] + _e[13:]
check("shift check: a run where each English holds the next Greek is found (Ant. 8.6.1-8.10.3, 2026-10-03)",
      [s for s, *_ in J.shift_runs([(k, "x" * g, "x" * e) for k, g, e in zip(_k, _g, _slid)])] == [+1],
      J.shift_runs([(k, "x" * g, "x" * e) for k, g, e in zip(_k, _g, _slid)]))

have = all(os.path.exists(J.local(r)) for r in pins)
nt_built = os.path.exists(os.path.join(REPO, "data", "nt", "Rev", "tokens.jsonl"))
if not (have and nt_built):
    print("\nskip  the pinned TEI or the built NT is missing "
          "(build_josephus.py --fetch; rebuild_bible.py); the rebuild checks did not run")
else:
    print("--- rebuild")
    built = J.build()
    check("a rebuild equals every committed manifest entry",
          all(man.get(s) == e for s, (_, _, e) in built.items()),
          [s for s, (_, _, e) in built.items() if man.get(s) != e])
    for w in EXPECTED:
        g = {k: sp[0] if sp else None for k, _, sp in J.read(w, "niese")}
        e = {k: sp[0] if sp else None for k, _, sp in J.read(w, "whiston")}
        diff = {k for k in g if k[-1] != "arg" and g[k] != e.get(k)}
        check(f"{w}: each Whiston unit begins at the same Niese section in both files",
              diff <= NIESE_START_EXCEPTIONS, sorted(diff - NIESE_START_EXCEPTIONS)[:5])
    for w in EXPECTED:
        g = {k: t for k, t, _ in J.read(w, "niese")}
        runs = J.shift_runs([(k, g[k], t) for k, t, _ in J.read(w, "whiston") if t and g.get(k)
                             and k[-1] != "arg"])
        check(f"{w}: no run of units fits its neighbour's text better than its own", not runs, runs)
    u = {x["id"]: x for b, _, _ in built.values() for x in b["units"]}
    for cid, gr, en in [("4.8.32", "Ὁμοίως μηδὲ βλασφημείτω", "In like manner, let no one revile"),
                        ("4.8.33", "Ἐν μάχῃ", "If men strive together"),
                        ("4.8.41", "Αὕτη μὲν οὖν ὑμῖν", "Let this be the constitution"),
                        ("8.6.1", "Ἐπεὶ δʼ ἑώρα τὰ τῶν Ἱεροσολύμων τείχη", "Now when the king saw that the walls"),
                        ("8.7.1", "Κατὰ δὲ τὸν αὐτὸν καιρὸν", "ABOUT the same time"),
                        ("8.10.3", "ἐγκεκλεισμένου τοῦ Ῥοβοάμου", "Now when Rehoboam, and the multitude")]:
        check(f"Ant. {cid}: the slid runs (FIXES slide) pair the right Greek and English",
              u[f"josephus-ant-niese:{cid}"]["text"].startswith(gr)
              and u[f"josephus-ant-whiston:{cid}"]["text"].startswith(en))
    check("... and Menander on Hiram stays in Ant. 8.5.3, after Dius",
          "Μένανδρος" in u["josephus-ant-niese:8.5.3"]["text"]
          and u["josephus-ant-niese:8.5.3"]["lex"]["niese"][-1] == "8.149")
    t = u["josephus-ant-niese:18.3.3"]
    check("Ant. 18.3.3 is the Testimonium, Niese 18.63-64, in Niese's brackets",
          t["lex"]["niese"] == ["18.63", "18.64"] and t["text"].startswith("[Γίνεται δὲ κατὰ τοῦτον")
          and "ὁ χριστὸς" in t["text"])
    check("... and its English is Whiston's 'He was [the] Christ'",
          "He was [the] Christ" in u["josephus-ant-whiston:18.3.3"]["text"])
    j = u["josephus-ant-niese:20.9.1"]
    check("Ant. 20.9.1 names James, the brother of Jesus (Niese 20.200)",
          "20.200" in j["lex"]["niese"] and "τὸν ἀδελφὸν Ἰησοῦ τοῦ λεγομένου Χριστοῦ" in j["text"])
    check("Ant. 18.5.2 is John the Baptist (Niese 18.116-119)",
          "Ἰωάννου τοῦ ἐπικαλουμένου βαπτιστοῦ" in u["josephus-ant-niese:18.5.2"]["text"])
    check("Ag. Ap. 2.9 exists in the Greek (the inserted milestone) and begins at Niese 2.109",
          u["josephus-apion-niese:2.9"]["lex"]["niese"][0] == "2.109")
    check("every unit links to its counterpart, both ways",
          all(l["target"] in u and any(m["target"] == x["id"] for m in u[l["target"]]["links"])
              for x in u.values() for l in x["links"]))
    check("no notes or chapter heads in the English text (Whiston's notes are long)",
          not any("CHAPTER" in x["text"] for i, x in u.items() if i.startswith("josephus-ant-whiston")))

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
