#!/usr/bin/env python3
"""
place_catena.py -- which of Cramer's verse marks are verses, and in which
chapter. Writes data/catenae/<slug>.json (COMMITTED); convert_catena in
structure_texts.py only reads it.

    python3 pipeline/place_catena.py --fetch   # the Robinson-Pierpont books, pinned
    python3 pipeline/place_catena.py           # place every catena, write the JSON
    python3 pipeline/place_catena.py --check   # recompute; the JSON must be byte-identical

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
      order), at a cost of 0.25;
    - "not a verse" costs 0.3 -- a page-line number is skipped this way;
    - a margin number is a printed verse number, so leaving it out costs 0.3;
      a bare <lb n> is as likely a page line, so placing it must earn 0.5
      (it is placed only where its lemma shares half its words with the verse);
    - a margin number that is wrong may be placed at another verse of the
      same or next chapter only when the lemma matches that verse at 0.6 or
      more, at a cost of 0.35 (11:23 printed "33"). The printed number is kept.
    - a lemma of under three words is scored as if it had three, so two
      common words cannot make a 100% match.
The verse text is Robinson-Pierpont 2018 (PD), the NT pilot's pinned
source, commit 27a45ff. A placement scoring under 0.3 is kept and called
weak in the book; the honesty field states the measured counts.
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
}

SKIP, BACK, GAP, JUMP0, FIX, FIX_MIN, LB, SHORT = 0.3, 0.25, 0.05, 0.02, 0.35, 0.6, 0.5, 3
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
        margin = src == "margin"
        # A margin number IS a printed verse number: leaving it out costs.
        # A bare <lb n> is as likely a page line: placing it must earn LB.
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
                if margin and c2 in (c, c + 1):
                    for vv, vw in verses.items():
                        if vv == n:
                            continue
                        s = score(lem, vw)
                        if s >= FIX_MIN:
                            put((c2, vv), v + s - cost - FIX - (BACK if c2 == c and vv < lv else 0),
                                path + ((o, c2, vv, s),))
        states = dict(sorted(new.items(), key=lambda kv: (-kv[1][0], kv[0]))[:BEAM])
    best = max(states.values(), key=lambda x: (x[0], x[1]))[1]
    return {o: (c, vv, s) for o, c, vv, s in best}


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
    n_lb = sum(p["src"] == "lb" for p in placed)
    honesty = (f"The chapter of every verse is MEASURED, not printed: of {n_all} numbered "
               f"marks, {n_pl} were placed at a verse by pipeline/place_catena.py "
               f"({n_pl - n_lb} printed margin numbers, {n_lb} bare line numbers whose lemma "
               f"matched the verse at half its words or more); the rest read as page-line "
               f"numbers or unplaceable. Of the placed, {half} have a lemma sharing at least "
               f"half its words with the Robinson-Pierpont verse, {third} at least 30% (the "
               f"others are linked as weak); {fixed} printed number(s) were read as another "
               f"verse on the lemma's evidence, the printed number kept. Placed marks fall in "
               f"chapters {chapters[0] if chapters else '-'}-{chapters[-1] if chapters else '-'}; "
               f"a kephalaion with no placed mark is one unlinked unit.")
    doc = {"slug": slug, "source_sha256": st.sha256(path),
           "rp2018": {"commit": BYZ_COMMIT, "file": stem + ".csv"},
           "rule": {"skip": SKIP, "back": BACK, "gap": GAP, "jump": JUMP0, "fix": FIX,
                    "fix_min": FIX_MIN, "lb": LB, "short": SHORT},
           "honesty": honesty, "placed": placed}
    return json.dumps(doc, ensure_ascii=False, indent=1) + "\n"


def main():
    if "--fetch" in sys.argv:
        fetch(); return
    os.makedirs(st.CATENA_DIR, exist_ok=True)
    bad = []
    for slug in st.CATENA:
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
