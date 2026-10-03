#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""
build_deuterocanon.py -- one shared key per passage of the deuterocanon
(Tobit, Judith, the Greek Esther, Wisdom, Sirach, Baruch and the Epistle of
Jeremy, the Greek Daniel, 1-2 Maccabees, 1 Esdras, the Prayer of Manasses),
so the Clementine Vulgate, the Douay-Rheims and Brenton's Septuagint, each in
its own numbering, line up verse by verse.

    python3 pipeline/build_deuterocanon.py            # write data/versification/deuterocanon.json
                                                      # and data/parallel/deuterocanon-parallel.tsv
    python3 pipeline/build_deuterocanon.py --check    # rebuild: byte-identical; every invariant holds
    python3 pipeline/build_deuterocanon.py --audit    # the weakest pairings, for reading

THE KEY is the King James Version's Apocrypha verse: kjva:Sir.30.25. The KJV
printed these books (as Apocrypha) in one fixed numbering that the English
tradition kept, and its text is public domain and on the shelf
(data/books/kjva.json, fetch_sources.KJVA). So every key resolves to a real
verse a reader can open, and a later English witness keyed the same way (R.
H. Charles's 1913 Apocrypha follows the RV, which follows these numbers)
plugs in as one more row in WITNESSES. Where the KJV has no Apocrypha book
(3-4 Maccabees, Psalm 151) there is no key, and the map says so.

THE MAP IS READ OFF THE WORDS, not off a versification table. TVTMS has
deuterocanon blocks, but many are commented out in the pinned file (Tob
5-7, 11, 13) and none covers Brenton's own numbering, so it cannot carry the
whole map. The witnesses are all English (the Vulgate through the Douay,
which keeps the Clementine's verses), so each witness chapter is aligned
against the KJV's Apocrypha:

  1. ANCHORS. Each witness verse's closest KJV Apocrypha verse in the same
     passage (Dice overlap of content-word stems, the measure the Vulgate and
     English audits use). Those at ANCHOR or above anchor the chapter.
  2. CANDIDATES. Runs of anchors that move forward together become runs of
     KJV verses (widened by WIDEN on each side), in the witness's order. So a
     chapter the Greek has displaced (Brenton's Sirach 30-36, where the
     Greek manuscripts swap two blocks) still aligns in one pass.
  3. ALIGNMENT. A monotonic alignment of the chapter against its candidates
     (1-1, 1-2, 2-1, 2-2, 1-3, 3-1, 1-4; skipping a candidate is free).
  4. FILTER. A verse keeps its keys only where it shares words with them
     (Dice of at least KEEP over all of them, and some overlap with each). A
     verse that shares too little has no key, with why. This is where
     Jerome's Tobit and Judith show: he translated a different form of the
     story than the Greek the KJV follows, so many of their verses hold
     nothing the KJV's do.

The Vulgate is keyed through the Douay: a Douay verse is the Clementine verse
it reads (the same number, except at structure_texts.DOUAY_ROWS: this file
prints the Epistle of Jeremy's 6:37 in the slot of 6:7). A Clementine verse
the Douay leaves empty has no key, and says so, unless VULGATE_ROWS keys it
from the Latin.

The build refuses to write unless every selected witness verse has keys
that are KJV Apocrypha units or a stated reason for having none. KJV
Apocrypha verses no verse of a witness reaches are listed per witness, not
hidden. Not CC BY: this is the house's own reading of PD texts.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_vulgate_versification as BVV   # noqa: E402  (_etoks, _dice)

ROOT = os.path.normpath(os.path.join(HERE, ".."))
BOOKS = os.path.join(ROOT, "data", "books")
OUT = os.path.join(ROOT, "data", "versification", "deuterocanon.json")
OUT_TSV = os.path.join(ROOT, "data", "parallel", "deuterocanon-parallel.tsv")
TSV_COLUMNS = ["kjva", "vulgate", "douay", "brenton"]   # a new witness: one more column

ANCHOR = 0.3    # a closest-verse match this good anchors the chapter...
STRONG = 0.5    # ...alone; a weaker one only beside another moving the same way
WIDEN = 4       # KJV verses added on each side of an anchor run
KEEP = 0.12     # a verse keeps its keys only at this Dice over all of them
SURE = 0.3      # a pairing this good brackets the weaker ones around it...
SLACK = 2       # ...give or take this many KJV verses
SHARED = 3      # an anchor or a sure pairing shares at least this many word stems
WEAK = 0.2      # a kept pairing below this is listed as weak: read before relying on it
LOCAL = 0.8     # a verse in the chapter nearby wins over a far one this nearly as good
BEADS = [(1, 1, 0), (1, 2, .05), (2, 1, .05), (2, 2, .1), (1, 3, .1), (3, 1, .1), (1, 4, .15)]

KJVA_ORDER = ["Tob", "Jdt", "AddEsth", "Wis", "Sir", "Bar", "PrAzar", "Sus", "Bel",
              "1Macc", "2Macc", "1Esd", "PrMan", "2Esd"]
NO_KEY_BOOKS = {
    "3Macc": "3 Maccabees: the KJV's Apocrypha does not print it, so there is no shared key",
    "4Macc": "4 Maccabees: the KJV's Apocrypha does not print it, so there is no shared key",
}
WHY_WEAK = ("shares too few words with any KJV Apocrypha verse to be keyed (the alignment's "
            "best pairing is below the threshold)")
WHY_JEROME = ("Jerome's Latin of this book follows a different form of the story than the Greek "
              "the KJV translates; this verse shares too few words with any KJV verse to be keyed")
WHY_DOUAY_EMPTY = "the Douay prints no text for this Clementine verse, so its English cannot be read"


def _stop(msg):
    raise SystemExit(f"HARD STOP: {msg}")


def _num(v):
    d = "".join(c for c in v if c.isdigit())
    return int(d) if d else 0


# ---------------------------------------------------------------- witnesses
#
# Each witness: the built book it reads, and `passages(units)`: its verses in
# order, grouped [(KJV Apocrypha books, [(ref, text)])], one group per
# alignment chapter. A later witness (Charles 1913) is one more row.

def _brenton_passages(units):
    groups, why = {}, {}
    pair = {"Tob": ["Tob"], "Jdt": ["Jdt"], "Wis": ["Wis"], "Sir": ["Sir"], "Bar": ["Bar"],
            "EpJer": ["Bar"], "Sus": ["Sus"], "Bel": ["Bel"], "1Macc": ["1Macc"],
            "2Macc": ["2Macc"], "1Esd": ["1Esd"], "PrMan": ["PrMan"]}
    for u in units:
        ref = u["id"].split(":", 1)[1]
        b, c, v = ref.split(".")
        if b in NO_KEY_BOOKS:
            why[ref] = NO_KEY_BOOKS[b]
            continue
        if b == "Ps" and c == "151":
            why[ref] = "Psalm 151: the KJV's Apocrypha does not print it, so there is no shared key"
            continue
        if b in pair:
            groups.setdefault((tuple(pair[b]), f"{b}.{c}"), []).append((ref, u["text"]))
        elif b == "Esth" and not u["kjv"].get("resolved"):
            # The Greek's additions: brenton-kjv.json gives them no KJV verse.
            groups.setdefault((("AddEsth",), f"{b}.{c}"), []).append((ref, u["text"]))
        elif b == "Dan" and c == "3" and 24 <= _num(v) <= 90:
            groups.setdefault((("PrAzar",), f"{b}.{c}"), []).append((ref, u["text"]))
    return list(groups.items()), why


def _douay_passages(units):
    groups = {}
    for u in units:
        ref = u["id"].split(":", 1)[1]
        b, c, v = ref.split(".")
        c, n = int(c), _num(v)
        if b in ("Tob", "Jdt", "Wis", "Sir", "Bar", "1Macc", "2Macc"):
            groups.setdefault(((b,), f"{b}.{c}"), []).append((ref, u["text"]))
        elif b == "Esth" and (c, n) >= (10, 4):
            groups.setdefault((("AddEsth",), f"{b}.{c}"), []).append((ref, u["text"]))
        elif b == "Dan" and c == 3 and 24 <= n <= 90:
            groups.setdefault((("PrAzar",), f"{b}.{c}"), []).append((ref, u["text"]))
        elif b == "Dan" and c in (13, 14):
            groups.setdefault((("Sus", "Bel"), f"{b}.{c}"), []).append((ref, u["text"]))
    return list(groups.items()), {}


WITNESSES = {
    "brenton": {"book": "brenton", "passages": _brenton_passages,
                "title": "Brenton's English Septuagint (1851)"},
    "douay": {"book": "douay", "passages": _douay_passages,
              "title": "the Douay-Rheims (Challoner), the Clementine's English"},
    # "charles": {"book": "charles", "passages": ..., "title": "R. H. Charles (ed.), 1913"},
}
JEROME_BOOKS = {"Tob", "Jdt"}

# What the alignment cannot say, each read in both texts: {witness: {verse:
# ([keys], words that must stand in the verse, why)}}. A row may name a verse
# the witness's selection leaves out (Brenton's Esther 5:1-2 are the Hebrew's
# 5:1-2, keyed to the KJV, and also the Greek's expansion the KJV prints as
# Rest of Esther 15:1, 15:11).
_REREAD = "read in both texts: the alignment's order or overlap misses it"
_FAR = ("read in both texts: the alignment sent it to a verse elsewhere in the book "
        "that shares its words")
_LATIN = ("Jerome's Latin has this and the Greek the KJV translates does not, so there "
          "is no shared key")
HOUSE_ROWS = {
    "brenton": {
        "Esth.4.17o": (["AddEsth.14.8", "AddEsth.14.9"], "not been contented with the bitterness",
                       _REREAD),
        "Esth.8.12c": (["AddEsth.16.2", "AddEsth.16.3"], "Many who have been frequently honoured",
                       _REREAD),
        "Esth.8.12d": (["AddEsth.16.4"], "abolish gratitude from among men", _REREAD),
        "Dan.3.72a": (["PrAzar.1.45"], "O ye frost and heat",
                      "the KJV's 'winter and summer' (the Greek's cold and heat), which Brenton "
                      "prints after 'light and darkness'"),
        "Esth.5.1": (["AddEsth.15.1"], "she put off her mean dress",
                     "the Hebrew's 5:1 in the Greek's fuller wording, which the KJV prints "
                     "again as Rest of Esther 15:1"),
        "Esth.5.2": (["AddEsth.15.11"], "raised the golden sceptre he laid it upon her neck",
                     "the Hebrew's 5:2 in the Greek's fuller wording, which the KJV prints "
                     "again as Rest of Esther 15:11"),
        # The translator's prologue, which Brenton prints as Sir 1:1-1:1g and
        # the KJV as its second prologue (0.2): one KJV verse is more than
        # the alignment pairs with one of Brenton's.
        **{v: (["Sir.0.2"], w, "Brenton prints the translator's prologue as Sir 1:1-1:1g; "
                               "the KJV prints it whole as its second prologue")
           for v, w in [("Sir.1.1", "Whereas many and great things"),
                        ("Sir.1.1a", "my grandfather Jesus"),
                        ("Sir.1.1b", "was drawn on also himself to write"),
                        ("Sir.1.1c", "read it with favour and attention"),
                        ("Sir.1.1g", "prepared before in manners to live after the law")]},
        "Sir.36.16": (["Sir.33.16", "Sir.36.11"], "Though I was the last to wake up",
                      "the Greek's displaced half-line: 'the last to wake up' is the KJV's "
                      "33:16, 'their inheritance as from the beginning' its 36:11"),
        "Sir.30.13b": (["Sir.30.12"], "Bow down his neck in his youth",
                       "the first line of the KJV's 30:12, which Brenton prints after 30:13 "
                       "(the alignment had it at 7:23, which shares the words)"),
    },
    # Found by reading the weakest pairings and every key far from its
    # neighbours' (2026-10-03). _FAR: the alignment sent it to a verse
    # elsewhere that shares its words; _LATIN: Jerome's Latin has it and the
    # Greek the KJV translates does not.
    "douay": {
        "Esth.15.3": ([], "call upon the Lord, and speak to the king",
                      "Mordecai's charge to Esther, which Jerome gives in 15:1-3 and the "
                      "Greek in the Hebrew book's 4:8: the KJV's Apocrypha has no verse for it"),
        "Tob.1.15": ([], "gave them wholesome admonitions", _LATIN),
        "Tob.3.23": (["Tob.3.11"], "Be thy name, O God of Israel, blessed for ever",
                     "Sara's blessing of the Name, which closes her prayer in the Latin and "
                     "opens it in the Greek"),
        "Tob.7.7": (["Tob.7.6", "Tob.7.7"], "kissed him with tears", _REREAD),
        "Tob.7.8": (["Tob.7.8"], "Anna his wife, and Sara their daughter wept", _REREAD),
        "Tob.9.3": (["Tob.9.2"], "go to Gabelus to Rages the city of the Medes", _REREAD),
        "Tob.9.4": (["Tob.9.4"], "my father numbereth the days", _FAR),
        "Tob.9.5": (["Tob.9.3"], "Raguel hath adjured me", _FAR),
        "Tob.9.6": (["Tob.9.5"], "finding Gabelus, gave him his note of hand", _REREAD),
        "Tob.9.7": (["Tob.9.6"], "made him come with him to the wedding", _REREAD),
        "Tob.9.8": (["Tob.9.6"], "he found Tobias sitting at the table", _FAR),
        "Tob.9.9": ([], "The God of Israel bless thee",
                    "Gabelus's blessing of Tobias, which the Greek the KJV translates does "
                    "not give (its 9:6 has Tobias bless his wife)"),
        "Jdt.13.27": (["Jdt.14.6"], "Achior being called for came", _REREAD),
        "Jdt.13.31": (["Jdt.14.7"], "Blessed art thou by thy God in every tabernacle", _REREAD),
        "Jdt.14.11": (["Jdt.14.12", "Jdt.14.13"], "his captains and tribunes were come", _FAR),
        "Wis.6.12": (["Wis.6.11"], "Covet ye, therefore, my words", _FAR),
        "Sir.1.34": (["Sir.1.27"], "the fear of the Lord is wisdom and discipline", _FAR),
        "Sir.1.40": (["Sir.1.30"], "thy heart is full of guile and deceit", _REREAD),
        "Sir.2.23": (["Sir.2.18"], "according to his greatness, so also is his mercy", _FAR),
        "Sir.3.1": ([], "The sons of wisdom are the church of the just", _LATIN),
        "Sir.9.20": (["Sir.9.13"], "thou art going in the midst of snares", _REREAD),
        "Sir.9.21": (["Sir.9.14"], "beware of thy neighbour, and treat with the wise", _FAR),
        "Sir.20.14": (["Sir.20.14"], "The gift of the fool shall do thee no good", _FAR),
        "Sir.20.15": (["Sir.20.15"], "He will give a few things, and upbraid much", _REREAD),
        "Sir.23.31": ([], "he understood not the fear of the Lord", _LATIN),
        "Sir.31.42": (["Sir.31.31"], "press him not in demanding again", _REREAD),
        "Sir.38.1": (["Sir.38.1"], "Honour the physician for the need thou hast of him", _FAR),
        "Sir.39.9": (["Sir.39.6"], "pour forth the words of his wisdom as showers", _FAR),
        "Sir.49.18": (["Sir.49.15"], "his bones were visited", _FAR),
        "1Macc.10.25": (["1Macc.10.25"], "King Demetrius to the nation of the Jews", _FAR),
        "1Macc.14.20": (["1Macc.14.20"], "The princes and the cities of the Spartans", _FAR),
    },
}
# The Clementine verses the Douay has no English for, keyed from the Latin.
VULGATE_ROWS = {
    "Bar.6.7": (["Bar.6.8"], "lingua ipsorum polita a fabro",
                "the idols' tongue polished by the workman: the Douay file prints 6:37 "
                "in this slot (structure_texts.DOUAY_ROWS)"),
}


# ---------------------------------------------------------------- alignment

def align(D, K):
    """Monotonic alignment of witness token sets D against candidate token
    sets K; skipping a candidate is free, a witness verse left unpaired
    scores nothing. Returns {i: [j...]}."""
    n, M = len(D), len(K)
    best = {(0, j): (0.0, None) for j in range(M + 1)}
    for i in range(n + 1):
        for j in range(M + 1):
            if (i, j) not in best:
                continue
            sc = best[(i, j)][0]
            steps = [(a, b, p) for a, b, p in BEADS] + [(1, 0, 0), (0, 1, 0)]
            for a, b, pen in steps:
                ni, nj = i + a, j + b
                if ni > n or nj > M:
                    continue
                s2 = sc - pen
                if a and b:
                    s2 += BVV._dice(set().union(*D[i:ni]), set().union(*K[j:nj]))
                if (ni, nj) not in best or best[(ni, nj)][0] < s2 - 1e-12:
                    best[(ni, nj)] = (s2, (i, j))
    end = max((k for k in best if k[0] == n), key=lambda k: (best[k][0], -k[1]))
    al = {}
    while best[end][1]:
        pi, pj = best[end][1]
        if end[0] > pi and end[1] > pj:
            for x in range(pi, end[0]):
                al[x] = list(range(pj, end[1]))
        end = (pi, pj)
    return al


def _load(slug):
    p = os.path.join(BOOKS, f"{slug}.json")
    if not os.path.exists(p):
        _stop(f"data/books/{slug}.json is missing: fetch its source, then run "
              f"pipeline/structure_texts.py")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def key_witness(units, passages, KT, kbook):
    """{ref: {"keys": [...], "score": s} or {"why": ...}} for one witness."""
    groups, out = passages(units)
    out = {r: {"why": w} for r, w in out.items()}
    for (books, _chap), vs in groups:
        pool = [k for b in books for k in kbook.get(b, [])]
        if not pool:
            _stop(f"{books}: no KJV Apocrypha verses")
        pidx = {k: i for i, k in enumerate(pool)}
        D = [BVV._etoks(t) for _r, t in vs]
        found = []
        wch = int(_chap.split(".")[1])
        for i, d in enumerate(D):
            # Ties (a verse a book repeats: Vulgate Sir 41:18 is also 20:31)
            # go to the chapter nearest the witness's own.
            k = max(pool, key=lambda k: (BVV._dice(d, KT[k]), -abs(int(k.split(".")[1]) - wch),
                                         -pidx[k]))
            near = [x for x in pool if abs(int(x.split(".")[1]) - wch) <= 1]
            kn = max(near, key=lambda x: (BVV._dice(d, KT[x]), -pidx[x])) if near else k
            if kn != k and BVV._dice(d, KT[kn]) >= max(ANCHOR, LOCAL * BVV._dice(d, KT[k])):
                k = kn    # a book repeating itself: the nearby verse, not the far one
            if BVV._dice(d, KT[k]) >= ANCHOR and len(d & KT[k]) >= SHARED:
                found.append((i, pidx[k], BVV._dice(d, KT[k])))
        # An anchor stands if it is strong, or if the next or previous anchor
        # moves on with it (a lone weak match elsewhere in the book is noise).
        anchors = [a for n, (i, a, s) in enumerate(found)
                   if s >= STRONG or any(0 < (a2 - a) * (i2 - i) and abs(a2 - a) <= 3 * abs(i2 - i) + 3
                                         for i2, a2, _s in found[max(0, n - 1):n + 2] if i2 != i)]
        runs = []
        for a in anchors:
            if runs and runs[-1][1] - 2 <= a <= runs[-1][1] + 2 * WIDEN:
                runs[-1][1] = max(runs[-1][1], a)
            else:
                runs.append([a, a])
        cand = []
        for lo, hi in runs:
            for x in range(max(0, lo - WIDEN), min(len(pool), hi + WIDEN + 1)):
                if not cand or cand[-1] != x:
                    if x not in cand[-2 * WIDEN - 2:]:
                        cand.append(x)
        al = align(D, [KT[pool[x]] for x in cand]) if cand else {}
        got = []
        for i in range(len(vs)):
            ks = [pool[cand[j]] for j in al.get(i, [])]
            ks = [k for k in ks if BVV._dice(D[i], KT[k]) > 0]
            got.append((ks, BVV._dice(D[i], set().union(*(KT[k] for k in ks))) if ks else 0.0))
        # A weak pairing must also stand where its neighbours put it: between
        # the nearest surely paired verses before and after it (a little slack).
        sure = [(i, [pidx[k] for k in ks]) for i, (ks, sc) in enumerate(got)
                if sc >= SURE and len(D[i] & set().union(*(KT[k] for k in ks))) >= SHARED]
        for i, (r, _t) in enumerate(vs):
            ks, s = got[i]
            if ks and s < STRONG:
                before = [(j, p) for j, p in sure if j < i][-1:]
                after = [(j, p) for j, p in sure if j > i][:1]
                # With one side only, the verse may run on at most two KJV
                # verses for each of its own from the sure one.
                lo = (min(before[0][1]) - SLACK if before
                      else min(after[0][1]) - 2 * (after[0][0] - i) - SLACK if after else None)
                hi = (max(after[0][1]) + SLACK if after
                      else max(before[0][1]) + 2 * (i - before[0][0]) + SLACK if before else None)
                if before and after and min(after[0][1]) < max(before[0][1]):
                    lo, hi = -1, len(pool)    # a displaced block's edge: no bracket
                if lo is None or not all(lo <= pidx[k] <= hi for k in ks):
                    ks = []
            if ks and s >= KEEP:
                ks = sorted(dict.fromkeys(ks), key=pidx.get)
                out[r] = {"keys": [f"kjva:{k}" for k in ks], "score": round(s, 3)}
            else:
                jerome = passages is _douay_passages and r.split(".")[0] in JEROME_BOOKS
                out[r] = {"why": WHY_JEROME if jerome else WHY_WEAK}
    return out


def _default(ref, books):
    """The key a witness verse gets by its own number in the paired book; the
    map lists a verse only where its keys differ from this."""
    b, c, v = ref.split(".")
    tb = {"EpJer": "Bar"}.get(b, b)
    c = "6" if b == "EpJer" else c
    return [f"kjva:{tb}.{c}.{v}"] if tb in books else None


def _runs(refs, order):
    """Refs in order, consecutive numbered verses of a chapter as one run
    ('Tob.1.3-9'); a lettered verse stands alone."""
    out = []
    for r in sorted(refs, key=order.get):
        b, c, v = r.split(".")
        if out and out[-1][0] == (b, c) and v.isdigit() and isinstance(out[-1][2], int) \
                and int(v) == out[-1][2] + 1:
            out[-1][2] = int(v)
        else:
            n = int(v) if v.isdigit() else v
            out.append([(b, c), n, n])
    return [f"{b}.{c}.{a}" + (f"-{z}" if z != a else "") for (b, c), a, z in out]


def compute():
    kj = _load("kjva")
    kbook, KT, ktext = {}, {}, {}
    for u in kj["units"]:
        k = u["id"].split(":", 1)[1]
        kbook.setdefault(k.split(".")[0], []).append(k)
        KT[k] = BVV._etoks(u["text"])
        ktext[k] = u["text"]
    korder = {k: i for i, k in enumerate(k for b in KJVA_ORDER for k in kbook.get(b, []))}
    res = {}
    for name, w in WITNESSES.items():
        book = _load(w["book"])
        keyed = key_witness(book["units"], w["passages"], KT, kbook)
        bad = [(r, x["keys"]) for r, x in keyed.items() if "keys" in x
               and any(k[5:] not in KT for k in x["keys"])]
        if bad:
            _stop(f"{name}: keys that are no KJV Apocrypha verse: {bad[:5]}")
        text = {u["id"].split(":", 1)[1]: u["text"] for u in book["units"]}
        for r, (ks, words, why) in HOUSE_ROWS.get(name, {}).items():
            if words not in text.get(r, ""):
                _stop(f"HOUSE_ROWS {name} {r}: {words!r} is not in the verse")
            if any(k not in KT for k in ks):
                _stop(f"HOUSE_ROWS {name} {r}: {ks} names no KJV Apocrypha verse")
            keyed[r] = ({"keys": [f"kjva:{k}" for k in ks], "house": why} if ks
                       else {"why": why, "house": why})
        res[name] = {"book": book, "keyed": keyed}
    # The Vulgate, through the Douay: each Douay verse names the Clementine
    # verse(s) it reads (`vulgate`; the same number except at DOUAY_ROWS).
    vul = _load("vulgate")
    dk = res["douay"]["keyed"]
    reads = {}
    for u in res["douay"]["book"]["units"]:
        r = u["id"].split(":", 1)[1]
        if r in dk:
            for v in u.get("vulgate", []):
                reads.setdefault(v.split(":", 1)[1], []).append(dk[r])
    vtext = {u["id"].split(":", 1)[1]: u["text"] for u in vul["units"]}
    vkeyed = {}
    sel = set()
    for u in vul["units"]:
        ref = u["id"].split(":", 1)[1]
        b, c, v = ref.split(".")
        c, n = int(c), _num(v)
        if (b in ("Tob", "Jdt", "Wis", "Sir", "Bar", "1Macc", "2Macc")
                or (b == "Esth" and (c, n) >= (10, 4))
                or (b == "Dan" and ((c == 3 and 24 <= n <= 90) or c in (13, 14)))):
            sel.add(ref)
            got = [x for x in reads.get(ref, []) if "keys" in x]
            if got:
                ks = list(dict.fromkeys(k for x in got for k in x["keys"]))
                x = {"keys": ks}
                if all("score" in g for g in got):
                    x["score"] = min(g["score"] for g in got)
                vkeyed[ref] = x
            else:
                # The Douay's house rows are its own; the Vulgate's are VULGATE_ROWS.
                vkeyed[ref] = ({"why": reads[ref][0]["why"]} if ref in reads
                               else {"why": WHY_DOUAY_EMPTY})
    for ref, (ks, words, why) in VULGATE_ROWS.items():
        if words not in vtext.get(ref, ""):
            _stop(f"VULGATE_ROWS {ref}: {words!r} is not in the verse")
        vkeyed[ref] = {"keys": [f"kjva:{k}" for k in ks], "house": why}
    stray = sorted(u["id"] for u in res["douay"]["book"]["units"]
                   if u["id"].split(":", 1)[1] in dk
                   and not all(v.split(":", 1)[1] in sel for v in u.get("vulgate", [None]) if v))
    if stray:
        _stop(f"Douay verses reading no selected Clementine verse: {stray[:10]}")
    res["vulgate"] = {"book": vul, "keyed": vkeyed}
    return {"res": res, "kbook": kbook, "korder": korder, "ktext": ktext, "KT": KT,
            "kjva": kj}


def build():
    c = compute()
    return _doc(c), _tsv(c)


def _tsv(c):
    """One row per KJV Apocrypha verse: the verse(s) of each witness holding
    its text, in the witness's own numbering, space-separated."""
    rows = {k: {} for k in c["korder"]}
    for name in TSV_COLUMNS[1:]:
        units = c["res"][name]["book"]["units"]
        order = {u["id"].split(":", 1)[1]: i for i, u in enumerate(units)}
        keyed = c["res"][name]["keyed"]
        for r in sorted(keyed, key=order.get):
            for k in keyed[r].get("keys", []):
                cell = rows[k[5:]].setdefault(name, [])
                if r not in cell:
                    cell.append(r)
    lines = ["\t".join(TSV_COLUMNS)]
    for k in sorted(rows, key=c["korder"].get):
        lines.append("\t".join([k] + [" ".join(rows[k].get(n, [])) for n in TSV_COLUMNS[1:]]))
    return ("\n".join(lines) + "\n").encode("utf-8")


def _doc(c):
    res, korder = c["res"], c["korder"]
    doc = {
        "note": ("One shared key per deuterocanonical passage: the KJV Apocrypha verse "
                 "(kjva:Book.c.v, data/books/kjva.json) that holds the same text as each "
                 "witness verse, in the witness's own numbering. Read off the words "
                 "(pipeline/build_deuterocanon.py): each witness chapter aligned against "
                 "the KJV's English. `map` lists only the verses whose keys differ from "
                 "their own number in the paired book (Brenton's Epistle of Jeremy 1:v is "
                 "the KJV's Baruch 6:v by default); every other verse in `verses` that is in "
                 "neither `map` nor `no_key` has that key. "
                 "`no_key` names, by run, the verses with no key and why. `weak` names the "
                 "keyed verses whose words agree least with their key (Dice below "
                 f"{WEAK}): different translations of different texts can share few words, "
                 "so read these before relying on them. "
                 "`kjva_without_verse` names the KJV Apocrypha verses no verse of the "
                 "witness holds."),
        "key": {"scheme": "the KJV's Apocrypha (Cambridge Paragraph Bible, eBible "
                          "engkjvcpb, PD)",
                "from": "data/books/kjva.json",
                "sha256": c["kjva"]["source"]["sha256"],
                "books": {b: len(c["kbook"].get(b, [])) for b in KJVA_ORDER}},
        "rights": {"license": "public-domain",
                   "note": "the house's own reading of public-domain texts; no TVTMS data"},
        "method": {"anchor": ANCHOR, "strong": STRONG, "shared": SHARED, "widen": WIDEN,
                   "local": LOCAL, "keep": KEEP, "sure": SURE, "slack": SLACK, "weak": WEAK,
                   "beads": [[a, b, p] for a, b, p in BEADS]},
        "witnesses": {},
    }
    for name in ["vulgate", "douay", "brenton"]:
        keyed = res[name]["keyed"]
        units = res[name]["book"]["units"]
        order = {u["id"].split(":", 1)[1]: i for i, u in enumerate(units)}
        kb = set(c["kbook"])
        mp, nokey = {}, {}
        for r, x in keyed.items():
            if "keys" in x:
                if x["keys"] != _default(r, kb):
                    mp[r] = x["keys"] if len(x["keys"]) > 1 else x["keys"][0]
            else:
                nokey.setdefault(x["why"], []).append(r)
        reached = {k[5:] for x in keyed.values() for k in x.get("keys", [])}
        books_read = sorted({k[5:].split(".")[0] for x in keyed.values()
                             for k in x.get("keys", [])}, key=KJVA_ORDER.index)
        without = [k for b in books_read for k in c["kbook"][b] if k not in reached]
        scores = [x["score"] for x in keyed.values() if "score" in x]
        nkeyed = sum(1 for x in keyed.values() if "keys" in x)
        weak = [r for r, x in keyed.items() if x.get("score", 1) < WEAK]
        house = {r: x["house"] for r, x in keyed.items() if "house" in x}
        doc["witnesses"][name] = {
            "from": f"data/books/{res[name]['book']['slug']}.json",
            "counts": {"verses": len(keyed), "keyed": nkeyed,
                       "no_key": len(keyed) - nkeyed,
                       "listed_in_map": len(mp),
                       "weak": len(weak),
                       "kjva_verses_reached": len(reached),
                       "kjva_without_verse": len(without),
                       "median_score": sorted(scores)[len(scores) // 2] if scores else None},
            **({"through": "the Douay: a Clementine verse has the keys of the Douay verse(s) "
                           "that read it (its `vulgate`), or VULGATE_ROWS'"} if name == "vulgate" else {}),
            "kjva_books_read": books_read,
            "verses": _runs(keyed, order),
            "map": {r: mp[r] for r in sorted(mp, key=order.get)},
            "no_key": [{"verses": _runs(rs, order), "why": w} for w, rs in sorted(nokey.items())],
            "weak": _runs(weak, order),
            "house_rows": {r: {"kjva": [k[5:] for k in keyed[r].get("keys", [])], "why": w}
                           for r, w in sorted(house.items(), key=lambda x: order[x[0]])},
            "kjva_without_verse": _runs(without, korder),
        }
    return doc


def render(doc):
    return (json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


FAR = 3   # --audit: how far a key may sit from its neighbours' before it is listed


def audit(show=60):
    c = compute()
    for name in ["douay", "brenton"]:
        keyed = c["res"][name]["keyed"]
        text = {u["id"].split(":", 1)[1]: u["text"] for u in c["res"][name]["book"]["units"]}
        weak = sorted(((x["score"], r) for r, x in keyed.items() if "score" in x))[:show]
        print(f"== {name}: the {show} weakest keyed verses")
        for s, r in weak:
            ks = keyed[r]["keys"]
            print(f"{s:.2f} {r} -> {' '.join(ks)}\n   {text[r][:150]}\n   "
                  f"{' / '.join(c['ktext'][k[5:]][:70] for k in ks)}")
        # A key far from every neighbour's: the alignment can send a verse to
        # another chapter that shares its words (Sir 9:21 had gone to 29:20).
        ko = c["korder"]
        refs = [u["id"].split(":", 1)[1] for u in c["res"][name]["book"]["units"]]
        refs = [r for r in refs if "keys" in keyed.get(r, {})]
        pos = {r: ko[keyed[r]["keys"][0][5:]] for r in refs}
        print(f"== {name}: keys more than {FAR} verses from every neighbour's")
        for i, r in enumerate(refs):
            nb = [pos[x] for x in refs[max(0, i - 3):i] + refs[i + 1:i + 4]
                  if x.split(".")[0] == r.split(".")[0]]
            if nb and min(abs(pos[r] - p) for p in nb) > FAR:
                ks = keyed[r]["keys"]
                print(f"{r} -> {' '.join(ks)}{' (house row)' if 'house' in keyed[r] else ''}"
                      f"\n   {text[r][:150]}\n   {c['ktext'][ks[0][5:]][:70]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--audit", action="store_true")
    a = ap.parse_args()
    if a.audit:
        audit()
        return
    doc, tsv = build()
    outs = [(OUT, render(doc)), (OUT_TSV, tsv)]
    if a.check:
        for path, blob in outs:
            rel = os.path.relpath(path, ROOT)
            if not os.path.exists(path) or open(path, "rb").read() != blob:
                _stop(f"{rel} missing or differs from a rebuild")
            print(f"OK: {rel} byte-identical; every invariant holds")
        return
    for path, blob in outs:
        with open(path + ".tmp", "wb") as f:
            f.write(blob)
        os.replace(path + ".tmp", path)
        print(f"wrote {os.path.relpath(path, ROOT)}")
    for n, w in doc["witnesses"].items():
        print(f"{n}: {w['counts']}")


if __name__ == "__main__":
    main()
