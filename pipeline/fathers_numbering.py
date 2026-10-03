#!/usr/bin/env python3
"""
fathers_numbering.py -- how each edition of the fathers numbers the Old
Testament, MEASURED, so fathers_scripture.py reads each editor's references
in that editor's numbering instead of assuming the family's.

    python3 pipeline/fathers_numbering.py           # measure -> data/fathers/numbering.json
    python3 pipeline/fathers_numbering.py --check   # re-measure: byte-identical

WHY. A Greek editor cites the Old Testament as the Septuagint numbers it, or
as the Hebrew and English Bibles do, and editors differ: most cite the Psalms
by the Greek count (Ps. 71 for the KJV's Ps 72), but Heikel's Laus
Constantini cites "Psal. 72, 8 ... 72, 7" beside Isa 2:4 for the peace psalm,
the KJV's Ps 72. Read through the Septuagint's map, that lands on Ps 73
("they are corrupt"). An editor can also
number the Psalms one way and the rest of the Bible the other (Cohn-Wendland's
Philo, PR #8). So the reading is decided per EDITOR and per CLASS of book:
the Psalms, Jeremiah (whose Greek order of chapters is not the Hebrew's),
and the rest.

HOW. Every OT reference in an edition's notes is read in both numberings: the
family's (Brenton's Septuagint for a Greek edition, the Clementine Vulgate for
a Latin one) and the English (the KJV's chapter and verse as printed). Where
the two name different KJV verses, the reference is evidence:

  existence   only one numbering has such a verse (LXX Ps 132 has 3 verses,
              so "Ps. 132, 7" is the English count).
  content     Greek only: both exist, and the father's own words decide.
              Each Greek word's Strong's number (tag_fathers.py) gives its
              English glosses (data/strongs/strongs.jsonl: KJV usage and
              definition); each candidate verse is read in Brenton's English,
              the Septuagint's own translation (the KJV verse the English
              reading names is read as the Brenton verse(s) that map to it).
              The share of the verse's words, weighted by rarity, found among
              the unit's glosses is its score; a vote needs the winner ahead
              by MARGIN and sharing at least MIN_SHARED words. The glosses of the COMMON words (NT count over
              COMMON: the article, particles, prepositions, θεός, κύριος)
              are left out: "pass", "over", "end" match any verse.
              CALIBRATED on the same notes where both numberings name the
              same verse (so which verse the editor meant is not in doubt),
              against the same verse number in the next chapter and against
              the next verse: 89% of votes are right between chapters and 75%
              between neighbouring verses (numbering.json "calibration").

DECISION, per editor and class (numbering.json "rule"): log-odds. The prior
is the share of all the family's votes for the class that say English (the
Greek editions number the Psalms as the Septuagint, 89%, and the rest as the
English, 62%; Jeremiah is near even, so a thinly attested edition's Jeremiah
is close to a coin flip, and its log-odds say so). Each vote adds the
log-odds of a vote of its kind being right: content from the calibration,
existence from the Latin editions' Psalms, where the Vulgate numbering is not
in doubt and 5% of existence votes still say otherwise (OCR digits, slips).
So a thinly attested edition leans on the pool and a well attested one
decides for itself: Heikel's Psalms (Ps 132:7, which the Septuagint does not
have, and the peace psalm) come out English against the pool. A Greek class
with at least MIN_VOTES votes of which neither side has SHARE is MIXED
(Dindorf's Demonstratio cites the Psalms both ways): there each note's run of
references to one chapter is read as one quotation, by one content vote over
all its verses, where the two numberings put it in different chapters (rule
suffix +content); else as the edition leans. The evidence is committed beside
each decision. Latin editions have no content votes (no English for their
words), so existence alone decides them, and it says Vulgate throughout.

INPUT: data/books/<slug>.json (the notes), build/fathers/<slug>.json (the
Greek tags, tag_fathers.py), data/strongs/strongs.jsonl (committed),
Brenton's USFM (build_brenton_versification.py --fetch, pinned), the maps in
data/versification/ and the KJV ids in data/uids/ (committed).
"""
import collections
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fathers_scripture as FS  # noqa: E402
import versification as VM  # noqa: E402

OUT = os.path.join(ROOT, "data", "fathers", "numbering.json")
BOOKS = os.path.join(ROOT, "data", "books")
TAGS = os.path.join(ROOT, "build", "fathers")
STRONGS = os.path.join(ROOT, "data", "strongs", "strongs.jsonl")
CONCORDANCE = os.path.join(ROOT, "data", "strongs", "concordance.jsonl")

MARGIN = 0.2
MIN_VOTES = 4
COMMON = 100  # calibrated: see numbering.json "calibration" (500: 83%/69%, 100: 89%/75%, 25: 92%/75% on far fewer votes)
SHARE = 0.7
CLIP = 0.05
MIN_SHARED = 2
FAMILY_MAP = {"grc": "lxx", "lat": "vulgate"}

STOP = set("""the and of to in that for is he it with as his be was they on not by are this
unto all shall him them which from but have will thou thy thee my me their your our
were one out into also when there then who what hath upon even any every let yea
""".split())


def numbering_class(book):
    return "Ps" if book == "Ps" else ("Jer" if book == "Jer" else "rest")


def words(s):
    """Content words, cut to five letters so 'flourish' meets 'flourisheth'."""
    return {w[:5] for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2}


NO_KJV = "no-kjv-verse"


def readings(book, ch, v, family, ctx):
    """(family-numbered KJV target, English-numbered KJV target); None where
    that numbering has no such verse, NO_KJV where the family's Bible has it
    but the KJV has no verse for it (an addition: still evidence that the
    verse exists in that numbering)."""
    osis = f"{book}.{ch}.{v}"
    try:
        if family == "lat":
            r = (VM.resolve_vulgate(osis, ctx["vmap"], ctx["kjv_ids"])
                 if f"{book}.{ch}" in ctx["vmap"]["vulgate_chapters"] else {})
        else:
            r = VM.resolve_brenton(osis, ctx["bmap"], ctx["kjv_ids"])
    except (ValueError, KeyError):
        r = {}
    if r.get("resolved"):
        fam = r["target"]
    elif r and not r.get("why", "").startswith("no such"):
        fam = NO_KJV  # the family's Bible has the verse; the KJV does not (Dan 3:24-90 Vulg.)
    else:
        fam = None
    direct = f"kjv:{osis}"
    return fam, (direct if direct in ctx["kjv_ids"] else None)


class Brenton:
    """Brenton's English by his own verse ids, and the Brenton verses behind
    each KJV verse, with word rarities over his verses."""

    def __init__(self, ctx):
        import build_brenton_versification as BB
        self.text, self.inv = {}, collections.defaultdict(list)
        df = collections.Counter()
        for osis, txt in BB.brenton():
            self.text[osis] = words(txt)
            df.update(self.text[osis])
            r = VM.resolve_brenton(osis, ctx["bmap"], ctx["kjv_ids"])
            if r.get("resolved"):
                self.inv[r["target"]].append(osis)
        n = len(self.text)
        self.idf = {w: math.log(n / c) for w, c in df.items()}
        self.top = math.log(n)

    def verse(self, osis=None, kjv=None):
        if osis is not None:
            return self.text.get(osis)
        got = [self.text[o] for o in self.inv.get(kjv, []) if o in self.text]
        return set().union(*got) if got else None

    def pick(self, unit_words, a, b):
        """0 or 1: the verse word set the father's words favour, by MARGIN and
        with at least MIN_SHARED words in common; None if neither."""
        sa, sb = self.score(unit_words, a), self.score(unit_words, b)
        if abs(sa - sb) < MARGIN:
            return None
        win = a if sa > sb else b
        if len(win & unit_words) < MIN_SHARED:
            return None
        return 0 if sa > sb else 1

    def score(self, unit_words, vw):
        w = lambda x: self.idf.get(x, self.top)  # noqa: E731
        return sum(w(x) for x in vw & unit_words) / sum(w(x) for x in vw)


def common_numbers():
    """Strong's numbers the NT uses more than COMMON times: the article,
    pronouns, particles, prepositions, and θεός and κύριος, which every
    verse has. Their glosses ("pass", "over", "end") would match any verse."""
    out = set()
    with open(CONCORDANCE, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("tokens", {}).get("nt", 0) > COMMON:
                out.add(r["strongs"])
    return out


def glosses():
    out = {}
    skip = common_numbers()
    with open(STRONGS, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r["strongs"].startswith("G") and r["strongs"] not in skip:
                out[r["strongs"]] = words(r.get("kjv_usage", "") + " " + r.get("definition", ""))
    return out


def edition_of(book):
    ed = (book.get("source") or {}).get("edition") or {}
    return ed.get("editor") or book.get("author") or "?"


def labels_of(unit):
    app = unit.get("apparatus") or {}
    return [n["text"] for n in app.get("notes") or []] + list(app.get("refs") or [])


def unit_words(tokens, gl):
    """The English glosses of a unit's tagged Greek words."""
    out = set()
    for t in tokens:
        if t[1]:
            out |= gl.get(t[1], set())
    return out


def content_vote(bren, uw, book, ch, v, eng):
    """'lxx', 'english' or None: which reading of one Greek reference the
    father's words favour, by MARGIN."""
    a = bren.verse(osis=f"{book}.{ch}.{v}")
    b = bren.verse(kjv=eng)
    if not a or not b:
        return None
    w = bren.pick(uw, a, b)
    return {0: "lxx", 1: "english"}.get(w)


def group_vote(bren, uw, items, ctx, family="grc"):
    """'lxx', 'english' or None for the references one note prints together
    in one chapter ("Jerem. 9, 23. 24"): they are one quotation, so they are
    read in one numbering, by the words of all their verses at once. Only
    where the two numberings put the passage in different CHAPTERS (the
    measure's better-calibrated case); a shift of a verse or two within the
    chapter is left to the edition's numbering."""
    a, b, chapters = set(), set(), set()
    for book, ch, v in items:
        fam, eng = readings(book, ch, v, family, ctx)
        if not fam or fam == NO_KJV or not eng or fam == eng:
            continue
        chapters.add(fam.rsplit(".", 1)[0] != eng.rsplit(".", 1)[0])
        va, vb = bren.verse(osis=f"{book}.{ch}.{v}"), bren.verse(kjv=eng)
        if va and vb:
            a |= va
            b |= vb
    if chapters != {True} or not a or not b:
        return None
    w = bren.pick(uw, a, b)
    return {0: "lxx", 1: "english"}.get(w)


def calibrate(bren, uw, book, ch, v, cal):
    """How often a content vote is right: where both numberings name the same
    verse (no doubt which one the editor meant), score it against the same
    verse number in the next chapter and against the next verse, as the
    measure would."""
    true = bren.verse(osis=f"{book}.{ch}.{v}")
    if not true:
        return
    for kind, decoy in (("chapter", f"{book}.{ch + 1}.{v}"), ("verse", f"{book}.{ch}.{v + 1}")):
        d = bren.verse(osis=decoy)
        if not d:
            continue
        w = bren.pick(uw, true, d)
        cal[kind][{None: "unclear", 0: "right", 1: "wrong"}[w]] += 1


def measure(ctx, slugs, bren=None, gl=None, cal=None):
    """{family: {editor: {class: Counter}}} of votes, and the books behind each
    editor; `cal` collects the content vote's calibration."""
    cal = cal if cal is not None else collections.defaultdict(collections.Counter)
    bren = bren or Brenton(ctx)
    gl = gl or glosses()
    votes = {"grc": collections.defaultdict(lambda: collections.defaultdict(collections.Counter)),
             "lat": collections.defaultdict(lambda: collections.defaultdict(collections.Counter))}
    books_of = collections.defaultdict(set)
    for family, slug in slugs:
        with open(os.path.join(BOOKS, f"{slug}.json"), encoding="utf-8") as f:
            book = json.load(f)
        ed = edition_of(book)
        tokens = {}
        if family == "grc":
            with open(os.path.join(TAGS, f"{slug}.json"), encoding="utf-8") as f:
                tokens = json.load(f)["tokens"]
        for u in book["units"]:
            labs = labels_of(u)
            if not labs:
                continue
            uw = None
            for lab in labs:
                for ref in FS.parse(lab, family):
                    book_, kind, ch, v, _end, _alt = ref
                    if kind == "deutero" or v is None or book_ in FS.NT:
                        continue
                    fam, eng = readings(book_, ch, v, family, ctx)
                    if fam == eng:
                        if family == "grc" and fam:
                            if uw is None:
                                uw = unit_words(tokens.get(u["id"], []), gl)
                            calibrate(bren, uw, book_, ch, v, cal)
                        continue
                    c = votes[family][ed][numbering_class(book_)]
                    books_of[(family, ed)].add(slug)
                    if fam is None or eng is None:
                        c[f"existence_{'english' if fam is None else FAMILY_MAP[family]}"] += 1
                        continue
                    if family != "grc":
                        continue
                    if uw is None:
                        uw = unit_words(tokens.get(u["id"], []), gl)
                    if fam == NO_KJV:
                        continue
                    cv = content_vote(bren, uw, book_, ch, v, eng)
                    if cv:
                        kind = "chapter" if fam.rsplit(".", 1)[0] != eng.rsplit(".", 1)[0] else "verse"
                        c[f"content_{cv}_{kind}"] += 1
    return votes, books_of


def tally(c, family):
    """(English votes, family votes), every kind counted once."""
    fam = FAMILY_MAP[family]
    e = sum(n for k, n in c.items() if k.split("_")[1] == "english")
    f = sum(n for k, n in c.items() if k.split("_")[1] == fam)
    return e, f


def is_mixed(c, family):
    """Enough votes, and neither numbering has SHARE of them."""
    e, f = tally(c, family)
    n = e + f
    return n >= MIN_VOTES and max(e, f) / n < SHARE


def logit(p):
    p = min(max(p, CLIP), 1 - CLIP)
    return math.log(p / (1 - p))


def lean(c, family, prior, weights):
    """The numbering this edition's votes favour: the pool's English share as
    prior odds, each vote adding its measured weight (the log-odds of being
    right: weights). A thinly attested edition leans on the pool, a well
    attested one decides for itself; ties go to the family's map."""
    odds = logit(prior)
    for k, n in c.items():
        kind, side = k.split("_")[0], k.split("_")[1]
        w = weights["existence"] if kind == "existence" else weights[k.split("_")[2]]
        odds += n * w * (1 if side == "english" else -1)
    return ("english" if odds > 0 else FAMILY_MAP[family]), round(odds, 3)


CLASSES = ("Ps", "Jer", "rest")


def build(ctx, slugs):
    cal = collections.defaultdict(collections.Counter)
    votes, books_of = measure(ctx, slugs, cal=cal)
    out = {"schema": "canon-corpus/fathers-numbering/v1",
           "built_by": "pipeline/fathers_numbering.py",
           "rule": {"margin": MARGIN, "min_shared": MIN_SHARED, "min_votes": MIN_VOTES,
                    "share": SHARE, "clip": CLIP,
                    "common": COMMON,
                    "classes": list(CLASSES),
                    "how": [
                        "votes: existence (only one numbering has the verse) and, in Greek, "
                        "content (the father's glossed words favour one verse by margin)",
                        "an edition's class is read as its log-odds say: the pool's English "
                        "share for the class as prior odds (clipped to clip..1-clip), plus each "
                        "vote's weight (`weights`: the log-odds of a vote of that kind being "
                        "right, from `calibration` and, for existence, the Latin Psalms)",
                        "mixed (Greek): at least min_votes and neither side has `share` of them; "
                        "each note's run of references to one chapter is then read by one content "
                        "vote where the numberings differ by chapter, else as the edition leans"]},
           "calibration": {k: {**dict(sorted(c.items())),
                               "right_share_of_votes": round(c["right"] / (c["right"] + c["wrong"]), 4)
                               if c["right"] + c["wrong"] else None}
                           for k, c in sorted(cal.items())},
           "pooled": {}, "editions": {}}
    pooled = {}
    for family in ("grc", "lat"):
        for cls in CLASSES:
            c = collections.Counter()
            for ed in votes[family].values():
                c.update(ed[cls])
            e, f = tally(c, family)
            pooled[(family, cls)] = round(e / (e + f), 4) if e + f else 0.0
            out["pooled"].setdefault(family, {})[cls] = {"english_share": pooled[(family, cls)],
                                                         "votes": dict(sorted(c.items()))}
    # How far to trust a vote. Content: its calibration. Existence: measured
    # on the Latin editions' Psalms, where the Vulgate numbering is not in
    # doubt; the share of existence votes there that say otherwise is what
    # OCR digits and slips cost (and some editors' real Hebrew references).
    ex = 1 - pooled[("lat", "Ps")]
    weights = {"existence": round(logit(ex), 4)}
    for kind in ("chapter", "verse"):
        r = out["calibration"].get(kind, {}).get("right_share_of_votes")
        weights[kind] = round(logit(r), 4) if r else 0.0
    out["rule"]["weights"] = weights
    for family in ("grc", "lat"):
        eds = {}
        for ed in sorted(votes[family]):
            row = {"books": sorted(books_of[(family, ed)])}
            for cls in CLASSES:
                c = votes[family][ed][cls]
                num, odds = lean(c, family, pooled[(family, cls)], weights)
                r = {"numbering": num, "log_odds_english": odds}
                if family == "grc" and is_mixed(c, family):
                    r["per_reference"] = True
                r["votes"] = dict(sorted(c.items()))
                row[cls] = r
            eds[ed] = row
        out["editions"][family] = eds
    return out


def load(path=OUT):
    """{(family, editor, class): (numbering, per_reference)} and the pooled fallback."""
    with open(path, encoding="utf-8") as f:
        m = json.load(f)
    table = {}
    for family, eds in m["editions"].items():
        for ed, row in eds.items():
            for cls in CLASSES:
                table[(family, ed, cls)] = (row[cls]["numbering"], bool(row[cls].get("per_reference")))
    pooled = {(family, cls): ("english" if v["english_share"] > 0.5 else FAMILY_MAP[family], False)
              for family, p in m["pooled"].items() for cls, v in p.items()}
    return table, pooled


def scheme_for(book, family, numbering):
    """book (an OSIS name) -> (numbering, per_reference) for this edition."""
    table, pooled = numbering
    ed = edition_of(book)
    return lambda b: table.get((family, ed, numbering_class(b)), pooled[(family, numbering_class(b))])


def main():
    import tag_fathers as T
    grc, lat = T.slugs()
    slugs = [("grc", s) for s in grc if not s.startswith("catena-")] + [("lat", s) for s in lat]
    m = build(T.scripture_context(), slugs)
    blob = (json.dumps(m, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    for family, eds in m["editions"].items():
        for ed, row in eds.items():
            print(f"  {family} {ed[:40]:40} " + "  ".join(
                f"{c}={row[c]['numbering']}{'~' if row[c].get('per_reference') else ''}"
                for c in ("Ps", "Jer", "rest")))
    print("  calibration:", m["calibration"])
    print("  pooled english share:", {f: {c: v["english_share"] for c, v in p.items()} for f, p in m["pooled"].items()})
    if "--check" in sys.argv:
        ok = os.path.exists(OUT) and open(OUT, "rb").read() == blob
        print("  CHECK", "PASSED: byte-identical" if ok else "FAILED: differs")
        raise SystemExit(0 if ok else 1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".tmp"
    with open(tmp, "wb") as f:
        f.write(blob)
    os.replace(tmp, OUT)


if __name__ == "__main__":
    main()
