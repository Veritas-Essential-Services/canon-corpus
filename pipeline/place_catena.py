#!/usr/bin/env python3
"""
place_catena.py -- which of Cramer's verse marks are verses, and in which
chapter. Writes data/catenae/<slug>.json (COMMITTED); convert_catena in
structure_texts.py only reads it.

    python3 pipeline/place_catena.py --fetch   # the Robinson-Pierpont books, pinned
    python3 pipeline/place_catena.py           # place every catena, write the JSON
    python3 pipeline/place_catena.py --check   # recompute; the JSON must be byte-identical
    python3 pipeline/place_catena.py <slug>... # only these

WHY THIS EXISTS. Cramer's catenae (Oxford, 1838-44; data/corpus/first1k/)
are divided only by the ancient kephalaia. He printed the VERSE number
beside each lemma, but never the chapter, and in the epistles the verse
numbers are bare <lb n="12"/> marks between paragraphs, mixed with his
page-line numbers (5, 10, 15...). So "which mark is a verse, and which
chapter is it in" is not in the source. It is measured here, and the
measurement is committed so a reader can review it.

THE RULE. Every candidate mark (structure_texts.catena_marks) has a lemma:
the paragraph beside it. Its score against a verse is the share of words
(Greek, accents stripped, over two letters) the two have in common, taken
both ways (lemma in verse; verse in lemma -- a lemma may be quoted inside a
comment), the larger. A path through the marks then picks, for each mark,
either a verse or "not a verse", maximizing total score, under:
    - chapters only advance (a skipped chapter costs 0.05 each);
    - inside a chapter a verse may step back (Cramer is not strictly in
      order), at a cost of 0.35, more than a skip: a step back must be
      earned by the lemma;
    - "not a verse" costs 0.3 -- a page-line number is skipped this way;
    - a margin number is a printed verse number, and so is a bare <lb n>
      that is not a multiple of 5, since Cramer numbers his page lines in
      fives only: leaving one out costs 0.3. A bare multiple of 5 is as likely
      a page line, so placing it must earn 0.5 (it is placed only where its
      lemma shares half its words with the verse);
    - a printed number that is wrong may be placed at another verse of the
      same or next chapter only when the lemma matches the printed verse
      under 0.3 and that other verse at 0.6 or more, at a cost of 0.35 (11:23
      printed "33"). The printed number is kept. (A comment often quotes the
      NEXT verse; a printed number its lemma matches at 0.3 or more stays put.)
    - a lemma of under three words is scored as if it had three, so two
      common words cannot make a 100% match.
The verse text is Robinson-Pierpont 2018 (PD), the NT pilot's pinned
source, commit 27a45ff. A placement scoring under 0.1 is dropped (no
evidence, no link); one under 0.3 is kept and called weak in the book; the
honesty field states the measured counts.
"""
import hashlib, json, os, re, sys, unicodedata, urllib.request, csv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import structure_texts as st                                  # noqa: E402

BYZ_COMMIT = "27a45ff1b7be6c17ccbfeac414f3f55732ae8e28"
BYZ_RAW = ("https://raw.githubusercontent.com/byztxt/byzantine-majority-text/"
           + BYZ_COMMIT + "/csv-unicode/ccat/no-variants/{stem}.csv")
RP_DIR = os.path.join(HERE, "..", "data", "corpus", "byz", "csv-unicode", "ccat", "no-variants")
# sha256 measured 2026-10-02; a mismatch is a hard stop.
PINS = {
    "MAT": "f098a3be6c8a7ecf406189ff41000f7933adf41d522fc6b6484b303314820d5d",
    "MAR": "80e7a72edb34474381c0287b58e2feea1d2495bf8318503dbaee570d4c056550",
    "LUK": "68edd943238ec1cb51fd1ba7f0f59ff0d9b6841fe780ea6812449e9b0debee98",
    "JOH": "06251d70a77f4d17e8dbde054e82ee947ef7834378348e5bcfa938803b42447b",
    "ACT": "922d4e0e618438c2595114346865b322d8599bca76edc62b9ba1811f746d83cb",
    "ROM": "0cda390213ff3782ceeb6a99a2686d541fb298977186ade0f60b024a17b92981",
    "1CO": "3df74494005fbde8705623f9f5c58225dbe53138a3c21d544b175220d3ba455a",
    "2CO": "500e00228db3b04f5eff6de2dc2614ff44dba60b7085a194f96e2c121b2adad9",
    "GAL": "0eb3b8e924e9c7c826b1bc189c272f9020f37b00e305ccc519521ffc4d2b71bb",
    "EPH": "d6d0f6c83d616350e5f78a26af2f6ac5f9836f8b98ef3703526ee90ebad0591d",
    "PHP": "ff818b91ba818894fcf9bf901e93687611307f0c020cba6a5d2308111fee82f6",
    "COL": "2ff3f88b702d59e31192de87ccbf97f8478704c9fffc8be606090d74fa21c7f8",
    "1TH": "06889bdfcaef08c16ecbe65141acbc66c04a5498fb39780b7e3278e25381c814",
    "2TH": "0cfbe3d62e5ba1933608fa1a89566c353264b620f3679e4c8d39b673123f4967",
    "1TI": "09ff4375a477e1836492fc2bb8ff64de460e264db928f709474b211f6be524b4",
    "2TI": "baf93b830c393d9b99d5b924bc223af6580daac150b78a783cfaa3b19fd7984f",
    "TIT": "1e18cf9ac5e168baee75ba9041209ad3fa251cc0a8214a6b253dc463514ef063",
    "PHM": "2af01ed66ab87fc6ba13e5fd5a607db8d223f2b143f8ec7352091ac091a9baf3",
    "HEB": "3fd70fa4077efa736ebb8ac33fdde6bc5d6460ac14b51ae5c4acfea90e6c51ba",
    "JAM": "aedd167524683df076f8a6a0518347a4788f8f7b3130122e0a9ca2ce0d0ab8e0",
    "1PE": "78bced495de92e84be3210e879fdb5d10d0aa0b4d3f68003a33c11e7702667fd",
    "2PE": "28cc901bb641c65d747bc05874f76f7caf325835cb9b043d1c772b74330f9c64",
    "1JO": "4a5837d952c3bdf1b46b25f73aab153af788aba65914165d3e17f3dcdcd03af8",
    "2JO": "ffe5d0b2b96458edc279cbc1197d4cd87fbf843cd20cdf0db22516f17aa7ca85",
    "3JO": "2b19485c09429cbecc20e74a6ba3b01a10781f3c4a736c0c5f95535be6b82e77",
}

SKIP, BACK, GAP, JUMP0, FIX, FIX_MIN, FIX_AT, LB, SHORT = 0.3, 0.35, 0.05, 0.02, 0.35, 0.6, 0.3, 0.5, 3
# A placement whose lemma shares under 10% of its words with the verse has no
# evidence: it is not placed (the mark reads as unplaceable, its text stays
# with the section before), so no KJV link stands on nothing.
MIN_PLACE = 0.1
BEAM = 3000


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def fetch():
    os.makedirs(RP_DIR, exist_ok=True)
    for slug, (_a, _o, stem) in st.CATENA.items():
        p = os.path.join(RP_DIR, stem + ".csv")
        if os.path.exists(p) and sha(p) == PINS.get(stem):
            continue
        blob = urllib.request.urlopen(BYZ_RAW.format(stem=stem), timeout=120).read()
        got = hashlib.sha256(blob).hexdigest()
        if PINS.get(stem) and got != PINS[stem]:
            raise SystemExit(f"HARD STOP: {stem}.csv sha256 {got} != pinned {PINS[stem]}")
        open(p, "wb").write(blob)
        print(f"  fetched {stem}.csv {got}")


def words(s):
    s = unicodedata.normalize("NFD", s.lower().replace("ς", "σ"))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return {w for w in re.findall(r"[α-ω]+", s) if len(w) > 2}


def load_rp(stem):
    p = os.path.join(RP_DIR, stem + ".csv")
    if not os.path.exists(p) or (PINS.get(stem) and sha(p) != PINS[stem]):
        raise SystemExit(f"{stem}.csv missing or changed: run place_catena.py --fetch")
    nt = {}
    for row in csv.DictReader(open(p, encoding="utf-8")):
        nt.setdefault(int(row["chapter"]), {})[int(row["verse"])] = words(row["text"])
    return nt


def score(lem, verse):
    if not lem or not verse:
        return 0.0
    both = len(lem & verse)
    return round(max(both / max(len(lem), SHORT), both / max(len(verse), SHORT)), 4)


def place(marks, nt):
    """marks: [(ord, k, n, src, lemma_words)]. Returns {ord: (chapter, verse, score)}."""
    chs = sorted(nt)
    states = {(chs[0], 0): (0.0, ())}
    for o, k, n, src, lem in marks:
        n = int(n)
        # A margin number IS a printed verse number, and so is a bare <lb n>
        # that is not a multiple of 5 (Cramer numbers his page lines only in
        # fives): leaving one out costs. A bare multiple of 5 is as likely a
        # page line: placing it must earn LB.
        margin = src == "margin" or n % 5 != 0
        skip, base = (SKIP, 0.0) if margin else (0.0, LB)
        new = {}

        def put(key, v, path):
            if key not in new or v > new[key][0]:
                new[key] = (v, path)
        for (c, lv), (v, path) in states.items():
            put((c, lv), v - skip, path)
            for c2 in chs:
                if c2 < c:
                    continue
                cost = 0 if c2 == c else JUMP0 + GAP * (c2 - c - 1)
                verses = nt[c2]
                if n in verses:
                    s = score(lem, verses[n])
                    put((c2, n), v + s - base - cost - (BACK if c2 == c and n < lv else 0),
                        path + ((o, c2, n, s),))
                # a misprinted margin: another verse of the chapter, strongly matched
                at = score(lem, verses[n]) if n in verses else 0.0
                if margin and c2 in (c, c + 1) and at < FIX_AT:
                    for vv, vw in verses.items():
                        if vv == n:
                            continue
                        s = score(lem, vw)
                        if s >= FIX_MIN:
                            put((c2, vv), v + s - cost - FIX - (BACK if c2 == c and vv < lv else 0),
                                path + ((o, c2, vv, s),))
        states = dict(sorted(new.items(), key=lambda kv: (-kv[1][0], kv[0]))[:BEAM])
    best = max(states.values(), key=lambda x: (x[0], x[1]))[1]
    return {o: (c, vv, s) for o, c, vv, s in best if s >= MIN_PLACE}


def run(slug):
    abbrev, osis, stem = st.CATENA[slug]
    path = os.path.join(st.CORPUS, "first1k", slug + ".xml")
    root = st.tei_load(path)
    items = st.catena_marks(root.find(f".//{st.TEI_NS}body"))
    marks = [(it["ord"], it["k"], it["n"], it["src"], words(st.catena_lemma(items, i)))
             for i, it in enumerate(items) if it["kind"] == "mark"]
    got = place(marks, load_rp(stem))
    placed = []
    for o, k, n, src, _l in marks:
        if o in got:
            c, v, s = got[o]
            placed.append({"ord": o, "k": k, "n": n, "src": src, "chapter": c, "verse": v,
                           "score": s})
    n_all, n_pl = len(marks), len(placed)
    half = sum(p["score"] >= 0.5 for p in placed)
    third = sum(p["score"] >= 0.3 for p in placed)
    fixed = sum(int(p["n"]) != p["verse"] for p in placed)
    chapters = sorted({p["chapter"] for p in placed})
    n_lb = sum(p["src"] == "lb" and int(p["n"]) % 5 == 0 for p in placed)
    honesty = (f"The chapter of every verse is MEASURED, not printed: of {n_all} numbered "
               f"marks, {n_pl} were placed at a verse by pipeline/place_catena.py "
               f"({n_pl - n_lb} printed verse numbers, {n_lb} bare multiples of 5 -- which "
               f"may be page-line numbers -- whose lemma matched the verse at half its words "
               f"or more); the rest read as page-line numbers or unplaceable. Of the placed, {half} have a lemma sharing at least "
               f"half its words with the Robinson-Pierpont verse, {third} at least 30% (the "
               f"others are linked as weak); {fixed} printed number(s) were read as another "
               f"verse on the lemma's evidence, the printed number kept. Placed marks fall in "
               f"chapters {chapters[0] if chapters else '-'}-{chapters[-1] if chapters else '-'}; "
               f"a kephalaion with no placed mark is one unlinked unit.")
    doc = {"slug": slug, "source_sha256": st.sha256(path),
           "rp2018": {"commit": BYZ_COMMIT, "file": stem + ".csv"},
           "rule": {"skip": SKIP, "back": BACK, "gap": GAP, "jump": JUMP0, "fix": FIX,
                    "fix_min": FIX_MIN, "fix_at": FIX_AT, "lb": LB, "short": SHORT,
                    "min_place": MIN_PLACE},
           "honesty": honesty, "placed": placed}
    return json.dumps(doc, ensure_ascii=False, indent=1) + "\n"


def main():
    if "--fetch" in sys.argv:
        fetch(); return
    os.makedirs(st.CATENA_DIR, exist_ok=True)
    bad = []
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for slug in only or st.CATENA:
        out = run(slug)
        p = os.path.join(st.CATENA_DIR, slug + ".json")
        if "--check" in sys.argv:
            if not os.path.exists(p) or open(p, encoding="utf-8").read() != out:
                bad.append(slug)
            continue
        tmp = p + ".tmp"
        open(tmp, "w", encoding="utf-8").write(out)
        os.replace(tmp, p)
        d = json.loads(out)
        print(f"{slug}: {len(d['placed'])} placed")
    if "--check" in sys.argv:
        print("place_catena --check:", "OK" if not bad else f"DIFFERS: {bad}")
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
