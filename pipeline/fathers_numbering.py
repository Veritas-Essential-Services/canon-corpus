#!/usr/bin/env python3
"""
fathers_numbering.py -- how each edition of the fathers numbers the Old
Testament, MEASURED, so fathers_scripture.py reads each editor's references
in that editor's numbering instead of assuming the family's.

    python3 pipeline/fathers_numbering.py           # measure -> data/fathers/numbering.json
    python3 pipeline/fathers_numbering.py --check   # re-measure: byte-identical

WHY. An editor cites the Old Testament in one of three numberings, and
editors differ:
  lxx / vulgate   the Septuagint's (Brenton's map) or the Clementine's: the
                  Greek count of the Psalms, a long title counted as verse 1;
  hebrew          the Hebrew Bible's chapter and verse (BHS, the German
                  Bibles), a psalm's title counted as verse 1
                  (data/versification/bhs-kjv.json);
  english         the KJV's chapter and verse as printed.
Most Greek editors cite the Psalms by the Greek count (Ps. 71 for the KJV's
Ps 72), but Heikel's Eusebius cites "Psal. 72, 8 ... 72, 7" beside Isa 2:4
for the peace psalm, the KJV's Ps 72: not the Greek count. Whether it is the
Hebrew count or the English is another question, and his notes do not settle
it (his "Psal. 7, 16ff." for the pit is the KJV's 7:15 in the Hebrew count
and 7:16 in the English, and the father quotes both verses); so the measure
says so rather than choosing. An editor can also number the Psalms one way
and the rest of the Bible another (Cohn-Wendland's Philo, PR #8). So the
reading is decided per EDITOR and per CLASS of book: the Psalms, Jeremiah
(whose Greek order of chapters is not the Hebrew's), and the rest.

HOW. Every OT reference in an edition's notes is read in all three of its
family's numberings. Where they name different KJV verses, the reference is a
vote for the numberings it supports:

  existence   only some numberings have such a verse (LXX Ps 132 has 3
              verses, so "Ps. 132, 7" is the Hebrew or English count).
  content     Greek only: all exist, and the father's own words decide.
              Each Greek word's Strong's number (tag_fathers.py) gives its
              English glosses (data/strongs/strongs.jsonl: KJV usage and
              definition); each candidate verse is read in Brenton's English,
              the Septuagint's own translation (as the Brenton verse(s) that
              map to that KJV verse). The share of the verse's words,
              weighted by rarity, found among the unit's glosses is its
              score; a vote needs the winner ahead of the next by MARGIN and
              sharing at least MIN_SHARED words. The glosses of the COMMON
              words (NT count over COMMON: the article, particles,
              prepositions, θεός, κύριος) are left out: "pass", "over",
              "end" match any verse. CALIBRATED on the same notes where every
              numbering names the same verse (so which verse the editor
              meant is not in doubt), against the same verse number in the
              next chapter and against the next verse: 89% of votes are right
              between chapters and 75% between neighbouring verses
              (numbering.json "calibration").

DECISION, per editor and class (numbering.json "rule"): each numbering scores
the log of its share of the whole family's votes for the class (the prior,
shares(): a mixture estimate, in which a vote two numberings share is split
between them by their shares, so an LXX editor's "lxx+hebrew" votes, which
only show a psalm's title counted as verse 1, lend the Hebrew count nothing
against the English), plus, for every vote supporting it, the log-odds of a
vote of that kind being right: content from the calibration, existence from
the Latin editions' Psalms, where the Vulgate numbering is not in doubt and
5% of existence votes still say otherwise (OCR digits, slips). The highest
score wins, under two guards. An edition leaves the pool's numbering only on
at least MIN_OWN votes of its own that tell the two apart (one OCR digit
moves nothing: Halm's one Hebrew-only reference outside the Psalms). And a
rival numbering is ruled out only by MIN_OWN of the edition's own votes
netting against it, or, for the pool's numbering, by a pooled share of
SHARE with no vote of the edition's against it. A rival not ruled out is
UNDECIDED: the class reads as it leans, and every link a rival would read as
another verse says so (numbering_undecided, with that verse as alt_target).
Heikel's Psalms: Ps 132:7 and the peace psalm rule out the Greek count, but
both fit the Hebrew and the English alike, so they read as the pool leans
(English) and Ps 7:16 carries the Hebrew's 7:15 beside it, undecided.
A Greek class with at least MIN_VOTES votes of which no numbering has
SHARE is MIXED (Dindorf's Demonstratio cites the Psalms both ways): there each
note's run of references to one chapter is read as one quotation, by one
content vote over all its verses, where the winning and runner-up readings
put it in different chapters (rule suffix +content); else as the edition
leans. The evidence is committed beside each decision. Latin editions have no
content votes (no English for their words), so existence alone decides them:
Vulgate, except where an edition's existence votes say otherwise
(Reifferscheid-Wissowa's Tertullian, Psalms: Hebrew or English, undecided).

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
MIN_OWN = 2
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
SCHEMES = {"grc": ("lxx", "hebrew", "english"), "lat": ("vulgate", "hebrew", "english")}


def readings(book, ch, v, family, ctx):
    """{numbering: KJV target} for one reference read in each numbering the
    family's editors might use: None where that numbering has no such verse,
    NO_KJV where it has the verse but the KJV numbers none for it (a psalm
    title in the Hebrew count, Dan 3:24-90 in the Vulgate's: still evidence
    that the verse exists in that numbering)."""
    out = {}
    for scheme in SCHEMES[family]:
        r = FS.read_in(scheme, book, ch, v, ctx)
        out[scheme] = r["target"] if r.get("resolved") else (NO_KJV if r.get("exists") else None)
    return out


def candidates(R):
    """{KJV target: [numberings naming it]}, real targets only, in scheme order."""
    out = {}
    for scheme, t in R.items():
        if t and t != NO_KJV:
            out.setdefault(t, []).append(scheme)
    return out


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

    def pick(self, unit_words, sets):
        """The index of the verse word set the father's words favour, by
        MARGIN over the next and with at least MIN_SHARED words in common;
        None if none does."""
        scores = sorted(((self.score(unit_words, x), i) for i, x in enumerate(sets)), reverse=True)
        (s1, i1), (s2, _i2) = scores[0], scores[1]
        if s1 - s2 < MARGIN or len(sets[i1] & unit_words) < MIN_SHARED:
            return None
        return i1

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


def chapter_of(t):
    return t.rsplit(".", 1)[0]


def content_vote(bren, uw, cands):
    """(numberings, kind) the father's words favour among the candidate
    verses of one reference, or None; kind is 'chapter' when the winner and
    the runner-up lie in different chapters, else 'verse'."""
    ts = [t for t in cands if bren.verse(kjv=t)]
    if len(ts) < 2:
        return None
    sets = [bren.verse(kjv=t) for t in ts]
    i = bren.pick(uw, sets)
    if i is None:
        return None
    rest = sorted(((bren.score(uw, sets[j]), ts[j]) for j in range(len(ts)) if j != i), reverse=True)
    kind = "chapter" if chapter_of(ts[i]) != chapter_of(rest[0][1]) else "verse"
    return cands[ts[i]], kind


def group_vote(bren, uw, items, ctx, family="grc"):
    """The numberings the father's words favour for the references one note
    prints together in one chapter ("Jerem. 9, 23. 24"): one quotation, so
    one numbering, judged by the words of all its verses at once. Only where
    the winning and the runner-up readings put the passage in different
    CHAPTERS (the better-calibrated case); a shift of a verse or two within
    the chapter is left to the edition's numbering. None if undecided."""
    per = collections.defaultdict(list)    # numbering -> its targets
    for book, ch, v in items:
        for scheme, t in readings(book, ch, v, family, ctx).items():
            per[scheme].append(t)
    groups = {}
    for scheme, ts in per.items():
        if all(t and t != NO_KJV for t in ts):
            groups.setdefault(tuple(ts), []).append(scheme)
    keys = [k for k in groups if all(bren.verse(kjv=t) for t in k)]
    if len(keys) < 2:
        return None
    sets = [set().union(*(bren.verse(kjv=t) for t in k)) for k in keys]
    i = bren.pick(uw, sets)
    if i is None:
        return None
    rest = sorted(((bren.score(uw, sets[j]), j) for j in range(len(keys)) if j != i), reverse=True)
    if chapter_of(keys[i][0]) == chapter_of(keys[rest[0][1]][0]):
        return None
    return set(groups[keys[i]])


def calibrate(bren, uw, target, cal):
    """How often a content vote is right: where every numbering names the
    same verse (no doubt which one the editor meant), score it against the
    same verse number in the next chapter and against the next verse, as the
    measure would."""
    true = bren.verse(kjv=target)
    if not true:
        return
    book, ch, v = target[4:].split(".")
    for kind, decoy in (("chapter", f"kjv:{book}.{int(ch) + 1}.{v}"), ("verse", f"kjv:{book}.{ch}.{int(v) + 1}")):
        d = bren.verse(kjv=decoy)
        if not d:
            continue
        i = bren.pick(uw, [true, d])
        cal[kind][{None: "unclear", 0: "right", 1: "wrong"}[i]] += 1


def measure(ctx, slugs, bren=None, gl=None, cal=None):
    """{family: {editor: {class: Counter}}} of votes, and the books behind each
    editor; `cal` collects the content vote's calibration. A vote's key is
    its kind and the numberings it supports: 'existence:lxx+english' (the
    Hebrew count has no such verse), 'content_chapter:hebrew'."""
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
                    R = readings(book_, ch, v, family, ctx)
                    have = [x for x in SCHEMES[family] if R[x] is not None]
                    if not have:
                        continue
                    cands = candidates(R)
                    if len(have) == len(R) and len(cands) == 1 and NO_KJV not in R.values():
                        if family == "grc":
                            if uw is None:
                                uw = unit_words(tokens.get(u["id"], []), gl)
                            calibrate(bren, uw, next(iter(cands)), cal)
                        continue
                    c = votes[family][ed][numbering_class(book_)]
                    books_of[(family, ed)].add(slug)
                    if len(have) < len(R):
                        c["existence:" + "+".join(have)] += 1
                        continue
                    if family != "grc" or len(cands) < 2:
                        continue
                    if uw is None:
                        uw = unit_words(tokens.get(u["id"], []), gl)
                    cv = content_vote(bren, uw, cands)
                    if cv:
                        c[f"content_{cv[1]}:" + "+".join(cv[0])] += 1
    return votes, books_of


def support(c, family):
    """{numbering: votes that support it} (a vote may support several)."""
    out = {x: 0 for x in SCHEMES[family]}
    for k, n in c.items():
        for x in k.split(":")[1].split("+"):
            out[x] += n
    return out


def shares(c, family, rounds=200):
    """{numbering: its share of the pool}: a mixture estimate in which a vote
    two numberings share is split between them in proportion to their
    shares, repeated to a fixed point. So an LXX-numbered editor's
    'lxx+hebrew' votes (a psalm's title counted as verse 1) go almost wholly
    to the LXX and lend the Hebrew count nothing against the English, while
    a 'hebrew+english' vote still counts against the LXX."""
    xs = SCHEMES[family]
    votes = [(k.split(":")[1].split("+"), n) for k, n in c.items()]
    tot = sum(n for _, n in votes)
    if not tot:
        return {x: round(1 / len(xs), 4) for x in xs}
    p = {x: 1 / len(xs) for x in xs}
    for _ in range(rounds):
        got = {x: 0.0 for x in xs}
        for sup, n in votes:
            z = sum(p[x] for x in sup)
            for x in sup:
                got[x] += n * (p[x] / z if z else 1 / len(sup))
        p = {x: got[x] / tot for x in xs}
    return {x: round(v, 4) for x, v in p.items()}


def is_mixed(c, family):
    """Enough votes, and no numbering has SHARE of them."""
    n = sum(c.values())
    return n >= MIN_VOTES and max(support(c, family).values()) / n < SHARE


def logit(p):
    p = min(max(p, CLIP), 1 - CLIP)
    return math.log(p / (1 - p))


def weight(kind, weights):
    return weights["existence"] if kind == "existence" else weights[kind.split("_")[1]]


def between(c, x, y, weights):
    """The edition's own votes that tell x from y: (supporting x and not y,
    supporting y and not x, their weighted difference)."""
    nx = ny = 0
    net = 0.0
    for k, n in c.items():
        kind, sup = k.split(":")
        sup = sup.split("+")
        if (x in sup) == (y in sup):
            continue
        if x in sup:
            nx, net = nx + n, net + n * weight(kind, weights)
        else:
            ny, net = ny + n, net - n * weight(kind, weights)
    return nx, ny, net


def decide(c, family, prior, weights, pooled=None, pool_share=0.0):
    """(numbering, scores, undecided): the numbering this edition's votes
    favour, and the rivals its evidence does not rule out.

    Score: each numbering's log prior (its pooled share for the class, from
    shares()), plus the measured weight of every vote
    that supports it (`weights`: the log-odds of a vote of that kind being
    right); ties go by SCHEMES order (the family's own first). Then two
    guards. An edition leaves the pool's numbering (`pooled`) only on at
    least MIN_OWN votes of its own that tell the two apart. And a rival is
    ruled out only by MIN_OWN such votes netting against it, or, for the
    pool's own numbering, by a pool holding `share` of the class with no
    vote of the edition's against it. Any rival left is `undecided`: the
    reading goes by the numbering, and the link says which others remain."""
    score = {x: math.log(min(max(prior[x], CLIP), 1 - CLIP)) for x in SCHEMES[family]}
    for k, n in c.items():
        kind, sup = k.split(":")
        for x in sup.split("+"):
            score[x] += n * weight(kind, weights)
    best = max(SCHEMES[family], key=lambda x: (round(score[x], 9), -SCHEMES[family].index(x)))
    if pooled and best != pooled and between(c, best, pooled, weights)[0] < MIN_OWN:
        best = pooled
    open_ = []
    for y in SCHEMES[family]:
        if y == best:
            continue
        nx, ny, net = between(c, best, y, weights)
        if nx >= MIN_OWN and net > 0:
            continue
        if best == pooled and pool_share >= SHARE and ny == 0:
            continue
        open_.append(y)
    return best, {x: round(v, 3) for x, v in score.items()}, open_


CLASSES = ("Ps", "Jer", "rest")


def build(ctx, slugs):
    cal = collections.defaultdict(collections.Counter)
    votes, books_of = measure(ctx, slugs, cal=cal)
    out = {"schema": "canon-corpus/fathers-numbering/v3",
           "built_by": "pipeline/fathers_numbering.py",
           "rule": {"numberings": {f: list(v) for f, v in SCHEMES.items()},
                    "margin": MARGIN, "min_shared": MIN_SHARED, "min_votes": MIN_VOTES, "min_own": MIN_OWN,
                    "share": SHARE, "clip": CLIP, "common": COMMON,
                    "classes": list(CLASSES),
                    "how": [
                        "each OT reference is read in every numbering of its family: lxx "
                        "(Brenton's map) or vulgate (the Clementine's), hebrew (BHS chapter and "
                        "verse, a psalm's title counted as verse 1: data/versification/bhs-kjv.json) "
                        "and english (the KJV's chapter and verse as printed)",
                        "votes, keyed kind:numberings-supported: existence (only some numberings "
                        "have the verse) and, in Greek, content_chapter / content_verse (the "
                        "father's glossed words favour one candidate verse by margin)",
                        "an edition's class takes the numbering with the highest score: the log of "
                        "its pooled share for the class (a mixture estimate: a vote two numberings "
                        "share is split between them by their shares, to a fixed point, so an "
                        "LXX editor's lxx+hebrew votes lend the Hebrew count nothing against the "
                        "English), clipped to clip..1-clip, plus each supporting vote's weight (`weights`: the "
                        "log-odds of a vote of that kind being right, from `calibration` and, for "
                        "existence, the Latin Psalms)",
                        "an edition leaves the pool's numbering only on at least min_own votes of its "
                        "own that tell the two apart; a rival is ruled out only by min_own such votes "
                        "netting against it, or, for the pool's numbering, by a pooled share of at "
                        "least `share` with no vote of the edition's against it. Rivals not "
                        "ruled out are `undecided`, and every link that would read differently in "
                        "one says so (numbering_undecided)",
                        "mixed (Greek): at least min_votes and no numbering has `share` of them; "
                        "each note's run of references to one chapter is then read by one content "
                        "vote where the candidates differ by chapter, else as the edition leans"]},
           "calibration": {k: {**dict(sorted(c.items())),
                               "right_share_of_votes": round(c["right"] / (c["right"] + c["wrong"]), 4)
                               if c["right"] + c["wrong"] else None}
                           for k, c in sorted(cal.items())},
           "pooled": {}, "editions": {}}
    prior = {}
    for family in ("grc", "lat"):
        for cls in CLASSES:
            c = collections.Counter()
            for ed in votes[family].values():
                c.update(ed[cls])
            prior[(family, cls)] = shares(c, family)
            out["pooled"].setdefault(family, {})[cls] = {"share": prior[(family, cls)],
                                                         "votes": dict(sorted(c.items()))}
    # How far to trust a vote. Content: its calibration. Existence: measured
    # on the Latin editions' Psalms, where the Vulgate numbering is not in
    # doubt: the share of existence votes there that do not support it is
    # what OCR digits and slips cost (and some editors' real Hebrew references).
    lat_ps = collections.Counter({k: n for k, n in out["pooled"]["lat"]["Ps"]["votes"].items()
                                  if k.startswith("existence:")})
    ex = support(lat_ps, "lat")["vulgate"] / sum(lat_ps.values()) if lat_ps else 0.95
    weights = {"existence": round(logit(ex), 4)}
    for kind in ("chapter", "verse"):
        r = out["calibration"].get(kind, {}).get("right_share_of_votes")
        weights[kind] = round(logit(r), 4) if r else 0.0
    out["rule"]["weights"] = weights
    for family in ("grc", "lat"):
        for cls in CLASSES:
            num, _, _ = decide(collections.Counter(), family, prior[(family, cls)], weights)
            out["pooled"][family][cls]["numbering"] = num
        eds = {}
        for ed in sorted(votes[family]):
            row = {"books": sorted(books_of[(family, ed)])}
            for cls in CLASSES:
                c = votes[family][ed][cls]
                pool = out["pooled"][family][cls]
                num, score, undecided = decide(c, family, prior[(family, cls)], weights,
                                               pool["numbering"], pool["share"][pool["numbering"]])
                r = {"numbering": num, "score": score}
                if undecided:
                    r["undecided"] = undecided
                if family == "grc" and is_mixed(c, family):
                    r["per_reference"] = True
                r["votes"] = dict(sorted(c.items()))
                row[cls] = r
            eds[ed] = row
        out["editions"][family] = eds
    return out


def load(path=OUT):
    """{(family, editor, class): (numbering, per_reference, undecided)} and the pooled fallback."""
    with open(path, encoding="utf-8") as f:
        m = json.load(f)
    table = {}
    for family, eds in m["editions"].items():
        for ed, row in eds.items():
            for cls in CLASSES:
                table[(family, ed, cls)] = (row[cls]["numbering"], bool(row[cls].get("per_reference")),
                                            tuple(row[cls].get("undecided", ())))
    pooled = {(family, cls): (v["numbering"], False, ()) for family, p in m["pooled"].items()
              for cls, v in p.items()}
    return table, pooled


def scheme_for(book, family, numbering):
    """book (an OSIS name) -> (numbering, per_reference, undecided) for this edition."""
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
                f"{'?' + '/'.join(row[c]['undecided']) if row[c].get('undecided') else ''}"
                for c in ("Ps", "Jer", "rest")))
    print("  calibration:", m["calibration"])
    print("  weights:", m["rule"]["weights"])
    print("  pooled:", {f: {c: (v["numbering"], v["share"]) for c, v in p.items()} for f, p in m["pooled"].items()})
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
