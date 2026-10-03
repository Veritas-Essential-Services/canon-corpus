#!/usr/bin/env python3
"""
apostolic_fathers_test.py -- the validator for the Apostolic Fathers books
(pipeline/build_apostolic_fathers.py; Lake's Loeb Greek via First1KGreek).

    python3 tests/apostolic_fathers_test.py

OFFLINE (always): the committed manifest entries (rights block, CC BY-SA
label, counts), the pins, and the rules on fixtures: citation (Ignatius's
letters, Hermas's Visions/Mandates/Similitudes), the Latin restoration, and
each Strong's tagging rule, including the ones that must say "don't know".

AGAINST THE PINNED TEI (when data/corpus/first1k/ holds it and data/nt/ is
built): a rebuild equals every committed manifest entry (built_sha256), and the
books hold what Lake prints where it matters.
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
import build_apostolic_fathers as A  # noqa: E402

PASS = FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"ok   {label}")
    else:
        FAIL += 1
        print(f"FAIL {label}  {detail}")


EXPECTED = {  # slug: (units, words, latin words)
    "1clement-lake": (400, 9832, 0), "2clement-lake": (118, 3013, 0),
    "ignatius-lake": (205, 7749, 0), "polycarp-phil-lake": (38, 1582, 450),
    "martyrdom-polycarp-lake": (59, 2641, 0), "didache-lake": (100, 2192, 0),
    "barnabas-lake": (194, 6715, 0), "hermas-lake": (727, 28551, 1265),
    "diognetus-lake": (100, 2615, 0),
}

# ================================================================ OFFLINE
print("--- manifest")
man = json.load(open(A.MANIFEST, encoding="utf-8"))
slugs = [w[0] for w in A.WORKS]
check("the nine works of Lake's Loeb set", sorted(slugs) == sorted(EXPECTED))
check("each has a committed manifest entry", all(s in man for s in slugs), [s for s in slugs if s not in man])
ents = {s: man.get(s, {}) for s in slugs}
check("every entry carries the rights block: CC BY-SA 4.0, PD text, not served whole",
      all(e.get("rights", {}).get("redistribute_whole") is False
          and "CC BY-SA 4.0" in e["rights"]["license"] and "public domain" in e["rights"]["license"]
          and A.F1K_COMMIT in e["rights"]["source_url"] for e in ents.values()))
check("units and word counts are the expected ones",
      all((e.get("units"), e.get("tagging", {}).get("words"), e.get("tagging", {}).get("latin"))
          == EXPECTED[s] for s, e in ents.items()),
      {s: (e.get("units"), e.get("tagging", {}).get("words")) for s, e in ents.items()})
check("every entry records the built book's sha256 (the book itself is gitignored)",
      all(re.fullmatch(r"[0-9a-f]{64}", e.get("built_sha256", "")) for e in ents.values()))
words = sum(e["tagging"]["words"] - e["tagging"]["latin"] for e in ents.values())
tagged = sum(e["tagging"][r] for e in ents.values() for r in A.RULES)
check(f"at least 80% of the Greek words carry a Strong's number ({100 * tagged / words:.1f}%)",
      tagged / words >= 0.80)
check("the books are gitignored, never committed (CC BY-SA, rule 6)",
      "data/books/*.json" in open(os.path.join(REPO, ".gitignore"), encoding="utf-8").read())
pins = A.pins()
check("every work's TEI is pinned by sha256", all(w[1] in pins for w in A.WORKS)
      and all(re.fullmatch(r"[0-9a-f]{64}", v) for v in pins.values()))
check("Lightfoot's English is listed as pending, not silently missing",
      any("Lightfoot" in p["what"] for p in A.PENDING))

print("--- citation")
check("Ignatius: letter, chapter, section", A.cite("ignatius-lake", "Ign.", ("1", "2", "3"))
      == ("Eph.2.3", "Ign. Eph. 2.3"))
check("Ignatius's seventh letter is To Polycarp", A.cite("ignatius-lake", "Ign.", ("7", "1", "1"))[0] == "Pol.1.1")
check("Hermas part 1 is Vision 1", A.cite("hermas-lake", "Herm.", ("1", "1", "1")) == ("Vis.1.1.1", "Herm. Vis. 1.1.1"))
check("Hermas part 6 is Mandate 1, part 17 Mandate 12",
      A.cite("hermas-lake", "Herm.", ("6", "1", "1"))[0] == "Mand.1.1.1"
      and A.cite("hermas-lake", "Herm.", ("17", "2", "1"))[0] == "Mand.12.2.1")
check("Hermas part 18 is Similitude 1, part 27 Similitude 10",
      A.cite("hermas-lake", "Herm.", ("18", "1", "1"))[0] == "Sim.1.1.1"
      and A.cite("hermas-lake", "Herm.", ("27", "4", "5"))[0] == "Sim.10.4.5")
check("everything else is chapter.section", A.cite("didache-lake", "Did.", ("9", "4")) == ("9.4", "Did. 9.4"))

print("--- the Latin")
t, n = A.restore_latin("ιν ηις εργο στατε ετ δομινι εχεμπλαρ σε#3υιμινι, φιρμι ιν φιδε")
check("a garbled Latin run comes back", t == "in his ergo state et domini exemplar sequimini, firmi in fide", t)
t, n = A.restore_latin("Ωαε αυτεμ, περ θυεμ νομεν δομινι")
check("capital V and the θ for q come back", t == "Vae autem, per quem nomen domini", t)
g = "ἐάν τε γάρ τις εἴπῃ μοι τι, καὶ λέγει"
check("Greek with lone unaccented enclitics is left alone", A.restore_latin(g) == (g, 0))
t, n = A.restore_latin("οὐ πιστευθήσονται: ετ εγο συμ παστορ, et")
check("a Latin run inside Greek is restored and the Greek kept",
      t.startswith("οὐ πιστευθήσονται: et ego sum pastor") and n == 5, (t, n))

print("--- scripture labels, on fixtures")
import af_scripture as S  # noqa: E402
check("book, chapter, verses, and a continuation in the same book",
      S.parse_label("Mk. 4, 18; Mt. 13, 20. 22") == [("nt", "Mark", 4, 18, None), ("nt", "Matt", 13, 20, None),
                                                     ("nt", "Matt", 13, 22, None)])
check("a range, and a book with one chapter", S.parse_label("I Cor. 7, 38-40; II Joh. 7")
      == [("nt", "1Cor", 7, 38, 40), ("nt", "2John", 1, 7, None)])
check("OCR spellings: '11 Kings', 'Dent.', 'Is. I, 16'",
      S.parse_label("11 Kings 5, 7") == [("lxx", "2Kgs", 5, 7, None)]
      and S.parse_label("Dent. 4, 2") == [("lxx", "Deut", 4, 2, None)]
      and S.parse_label("Is. I, 16-20") == [("lxx", "Isa", 1, 16, 20)])
check("a parenthesis of verses is read; another numbering in one is not",
      S.parse_label("Is. 5, 26 (11, 12)") == [("lxx", "Isa", 5, 26, None), ("lxx", "Isa", 11, 12, None)]
      and S.parse_label("Ecclus. 32, 9 (*wulg. 35.9)") == [("lxx", "Sir", 32, 9, None)])
check("a chapter alone stays a chapter", S.parse_label("Num. 12") == [("lxx", "Num", 12, None, None)])
check("a range into the next chapter is one range, not an invented verse (1 Clem. 39.2)",
      S.parse_label("Job 4, 16-18; 15, 16; 4, 19-5, 6")
      == [("lxx", "Job", 4, 16, 18), ("lxx", "Job", 15, 16, None), ("lxx", "Job", 4, 19, (5, 6))])
check("a lost semicolon before 'ch, v' starts a new chapter (Herm. Sim. 5.6.3)",
      [r[2:4] for r in S.parse_label("Joh. 10, 18 ; 12, 49. 50 ; 14, 31 15, 10")]
      == [(10, 18), (12, 49), (12, 50), (14, 31), (15, 10)]
      and S.parse_label("Deut 32 8-9") == [("lxx", "Deut", 32, 8, 9)])
check("a word that is no book ends the numbers (Barn. 15.2: 'cf. RL 91, 13-17' is not Jeremiah)",
      S.parse_label("Jer 17. 24. 25, cf. RL 91, 13-17") == [("lxx", "Jer", 17, 24, None), ("lxx", "Jer", 17, 25, None)])
check("OCR 'i', 'I.' and 'Rph' are read (1 John, 1 Peter, Ephesians)",
      [r[1] for r in S.parse_label("Gen. 1, 26. 27 *i Jo. 4, 9")] == ["Gen", "Gen", "1John"]
      and [r[1] for r in S.parse_label("II Tim. 4, 1 (I. Pet. 4, 5)")] == ["2Tim", "1Pet"]
      and [r[1] for r in S.parse_label("I Cor. 6, 9. 10; cf. Rph. 5, 5")] == ["1Cor", "1Cor", "Eph"])
check("a URN: NT, LXX, malformed, not scripture",
      S.parse_urn("urn:cts:greekLit:tlg0031.tlg017:3.1")[0] == ("nt", "Titus", 3, 1, None)
      and S.parse_urn("cts:urn:greekLit:tlg0527.tlg027:33.9")[0] == ("lxx", "Ps", 33, 9, None)
      and S.parse_urn("NN")[0] is None
      and S.parse_urn("urn:cts:greekLit:tlg0098.tlg001:1.50")[0] is None)

print("--- Strong's rules, on fixtures")
fk = A.form_key
forms = {fk("ἐν"): {"G1722": 50}, fk("ἕν"): {"G1520": 9}, fk("αὐτοῦ"): {"G846": 1474, "G847": 4},
         fk("ἄρα"): {"G686": 35, "G687": 16}, fk("ἐστιν"): {"G1510": 539}, fk("ὅν"): {"G3739": 30}}
keys = {"εν": {"G1722", "G1520"}, "ον": {"G3739"}, "φημι": {"G5346"}}
heads = {fk("μετάνοια"): {"G3341"}}
tb = (forms, keys, heads)
check("form_key reads a grave accent as acute", fk("ἐπὶ") == fk("ἐπί"))
check("nt-form: the written form, one number", A.tag_word("ἐν", tb) == ("G1722", "nt-form"))
check("... the accent tells ἕν from ἐν", A.tag_word("ἓν", tb) == ("G1520", "nt-form"))
check("nt-form-major: 97%+ of 20+ readings", A.tag_word("αὐτοῦ", tb) == ("G846", "nt-form-major"))
check("ambiguous below that is null, never guessed", A.tag_word("ἄρα", tb) == (None, "ambiguous"))
check("nt-form-nu: ἐστι is ἐστιν", A.tag_word("ἐστι", tb) == ("G1510", "nt-form-nu"))
check("nt-key for a longer word without its accents", A.tag_word("φημί", tb) == ("G5346", "nt-key"))
check("nt-key refuses a short word: ὄν is not ὅν", A.tag_word("ὄν", tb) == (None, "unseen"))
check("headword", A.tag_word("μετάνοια", tb) == ("G3341", "headword"))
check("Latin is never tagged", A.tag_word("ergo", tb) == (None, "latin"))

# ================================================================ PINNED
have = all(os.path.exists(A.local(r)) for r in pins)
nt_built = os.path.exists(os.path.join(REPO, "data", "nt", "John", "tokens.jsonl")) and \
    os.path.exists(os.path.join(REPO, "data", "nt", "Rev", "tokens.jsonl"))
if not (have and nt_built):
    print("\nskip  the pinned TEI or the built NT is missing "
          "(build_apostolic_fathers.py --fetch; rebuild_bible.py); the rebuild checks did not run")
else:
    print("--- rebuild")
    built = A.build()
    check("a rebuild equals every committed manifest entry", all(man.get(s) == e for s, (_, _, e) in built.items()),
          [s for s, (_, _, e) in built.items() if man.get(s) != e])
    books = {s: b for s, (b, _, _) in built.items()}
    ids = [u["id"] for b in books.values() for u in b["units"]]
    check("unit ids are unique", len(ids) == len(set(ids)))
    check("no unit carries a uid (nothing minted)", not any("uid" in u for b in books.values() for u in b["units"]))
    u = {x["id"]: x for b in books.values() for x in b["units"]}
    check("1 Clem. 1.1 opens as Lake prints it", u["1clement-lake:1.1"]["text"].startswith("Διὰ τὰς αἰφνιδίους"))
    check("Ign. Rom. 4.1 is the wheat of God", "σῖτός εἰμι θεοῦ" in u["ignatius-lake:Rom.4.1"]["text"])
    check("Hermas runs Vis. 1-5, Mand. 1-12, Sim. 1-10",
          {i.split(":")[1].split(".")[0] + i.split(":")[1].split(".")[1]
           for i in ids if i.startswith("hermas-lake:")}
          == {f"Vis{n}" for n in range(1, 6)} | {f"Mand{n}" for n in range(1, 13)} | {f"Sim{n}" for n in range(1, 11)})
    check("Pol. Phil. 10.1 is Latin, restored", u["polycarp-phil-lake:10.1"].get("lang") == "la"
          and u["polycarp-phil-lake:10.1"]["text"].startswith("in his ergo state et domini exemplar"))
    check("no Greek letter left in a Latin-only unit",
          not [x["id"] for x in u.values() if x.get("lang") == "la" and re.search(r"[Ͱ-Ͽἀ-῿]", x["text"])])
    check("Latin only where Lake prints Latin (Pol. Phil. 10-14, Herm. Sim. 9.30-10.4)",
          all(i.startswith(("polycarp-phil-lake:1", "hermas-lake:Sim.9.3", "hermas-lake:Sim.10."))
              for i, x in u.items() if x.get("lang")))
    check("no converter debris (#3) in any text", not [i for i, x in u.items() if "#" in x["text"]])
    check("every token is a word of the unit's text, in order",
          all(" ".join(w for w, _, _ in x["lex"]["tokens"]) == " ".join(A.WORD.findall(x["text"])) for x in u.values()))
    links = [l for x in u.values() for l in x["links"]]
    check("every scripture link is resolved to a KJV unit, or says why not",
          all((l["resolved"] and l["target"].startswith(("kjv:", "1clement-lake:", "2clement-lake:")))
              or (not l["resolved"] and l["why"]) for l in links))
    check(f"most of them resolve ({sum(l['resolved'] for l in links)} of {len(links)})",
          sum(l["resolved"] for l in links) / len(links) >= 0.8)
    pp = [l for l in u["hermas-lake:Sim.9.13.8"]["links"]] + [l for x in u.values() for l in x["links"]
                                                            if l["label"].startswith("Ps. 54, 23")]
    check("Lake's 'Ps. 54, 23' is the KJV's Ps 55:22 (through Brenton)",
          any(l.get("target") == "kjv:Ps.55.22" and l.get("via") == "brenton-kjv" for l in pp))
    def link(uid, ref):
        return next((l for l in u[uid]["links"] if l.get("ref") == ref), {})
    check("where both numberings have the verse, the English is the default and Brenton's is kept "
          "(1 Clem. 36.5 'Pa 110, 1' is 'sit thou at my right hand')",
          link("1clement-lake:36.5", "Ps 110:1").get("target") == "kjv:Ps.110.1"
          and link("1clement-lake:36.5", "Ps 110:1").get("alt_target") == "kjv:Ps.111.1")
    check("... the Septuagint's where it was read so (Did. 3.7, the meek shall inherit the earth)",
          link("didache-lake:3.8", "Ps 36:11").get("target") == "kjv:Ps.37.11"
          and link("didache-lake:3.8", "Ps 36:11").get("numbering") == "lxx")
    check("... and neither where neither verse is the passage (1 Clem. 17.5 'Exod. 8, 11' is 3:11)",
          not link("1clement-lake:17.5", "Exod 8:11").get("resolved", True)
          and link("1clement-lake:17.5", "Exod 8:11").get("candidates"))
    read = {(i, l["ref"]) for i, x in u.items() for l in x["links"]
            if l.get("why_numbering", "").startswith("read") or l.get("candidates")}
    check("every row of the LAKE_OT reading is a link the build makes (none stale)",
          set(S.LAKE_OT) <= read, sorted(set(S.LAKE_OT) - read)[:3])
    check("a range into the next chapter resolves through its last verse (Job 4:19-5:6)",
          link("1clement-lake:39.2", "Job 4:19-5:6").get("through") == "kjv:Job.5.6")
    jon = [l for l in u["1clement-lake:7.6"]["links"] if l.get("cts", "") and "tlg0031.tlg004" in l["cts"]]
    check("the URN that keys Lake's 'Jon. 3' as John 3 is flagged, not followed",
          jon and not jon[0]["resolved"] and "keying error" in jon[0]["why"])

print(f"\n{PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
