#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""
build_english_versification.py -- the historic English Bibles -> KJV verse
maps, so a verse cited in a Bible's own numbering (geneva:Num.13.1) lands on
the kjv: unit holding the same text (kjv:Num.12.16).

    python3 pipeline/build_english_versification.py --fetch          # every source, pinned
    python3 pipeline/build_english_versification.py                  # build every map
    python3 pipeline/build_english_versification.py geneva           # build one
    python3 pipeline/build_english_versification.py --check          # rebuild: byte-identical
    python3 pipeline/build_english_versification.py --audit geneva   # verses for reading

THE SOURCES (fetch_sources.ENGLISH): scrollmapper builds them from CrossWire's
SWORD modules, and a module sits on the KJV's verse GRID. So the slot numbers
are the Bible's own wherever it numbers as the KJV does, which for these
Protestant Bibles is almost everywhere. Where one numbers otherwise (the
Geneva follows the Hebrew in Num 13, 1 Sam 24, Dan 4, Hos 14...), its verses
were poured into the KJV's slots in order, and a chapter's overflow merged
into the chapter's last slot. The unit ids are the slots: the Bible's own
numbers, except that a merged last slot holds more than its number says.
The Tudor Bibles scrollmapper lacks come from Bible SuperSearch, on the same
grid (fetch_sources.ENGLISH_BSS); Coverdale and Tyndale printed no verse
numbers, so there the numbers are the transcription's. They are compared in
folded spelling (OLD_SPELLING), and Coverdale's Psalter, which follows the
Latin's division, is where the alignment does most of the work.

THE MAP IS READ OFF THE WORDS. These are English Bibles of the same tradition
as the KJV, so each chapter is aligned against the KJV's English (a monotonic
alignment over content-word overlap, the one the Vulgate and Brenton audits
use: 1-1, 1-2, 2-1, 2-2, 1-3, 3-1, 1-4, gaps), in a window that reaches into
the chapters on either side. A chapter keeps the same numbers unless the
alignment agrees with the KJV clearly better than the same numbers do (mean
Dice gain >= GAIN); then the chapter follows the alignment, and it is listed
under `aligned_chapters` with both scores. HOUSE_ROWS hold what an
order-keeping alignment cannot say (two verses swapped), each read in both
texts, with words that must stand in the Bible's verse.

The build refuses to write unless
  * every verse with text lands on a kjv: unit, or is named with why not;
  * every KJV verse of a book the Bible has is reached, or is named with why
    not (the Bible lacks it: the text-critical omissions, 1 John 5:7).
Not CC BY: this map is the house's own reading, from two PD texts.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_vulgate_versification as BVV  # noqa: E402
import fetch_sources as FS  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, ".."))
CORPUS = os.path.join(ROOT, "data", "corpus", "english")
OUTDIR = os.path.join(ROOT, "data", "versification")
KJV_TSV = BVV.KJV_TSV
GAIN = 0.15        # a chapter follows the alignment only when it reads this much better
VERSE_GAIN = 0.25  # ...and a single verse, outside such a chapter, when this much better
REACH = 8          # verses of the neighbouring chapters the alignment may reach into
BEADS = BVV._BEADS + [(1, 4, .15)]

_TAIL = ("the Bible's verse runs on into the words the KJV numbers as the next verse; read "
         "in both texts")
_EMPTY = ("the slot before it is empty: the transcription puts both verses' words here "
          "(old spelling hides it from the alignment; read in both texts)")
_SHIFT18 = "Young's numbers in Genesis 18:11-14 run one ahead of the KJV's"
_PHIL = ("Phil 1:16-17 in the order of the Greek the revisers followed: the KJV's two "
         "verses swapped")
_HOLDS = ("the verse holds the words of both KJV verses (the slot after or before it is "
          "empty or holds other words); read in both texts")
_COVPS = ("Coverdale's Psalter (from the Latin) divides the psalm otherwise; read in both "
          "texts")
_ROM3 = ("the Latin Psalter's longer Ps 14:3 (13:3 in the Vulgate), the words of Rom "
         "3:13-18, which Coverdale translates and the Hebrew and the KJV lack")
HOUSE_ROWS = {     # {slug: {verse: ([KJV verses], words in the verse, why)}}
    "geneva": {
        "Num.13.33": (["Num.13.32", "Num.13.33"], "For there we sawe gyant",
                      "the last slot of a chapter numbered as the Hebrew: it holds the "
                      "Geneva's 13:33 and 13:34"),
        "2Sam.1.26": (["2Sam.1.26", "2Sam.1.27"], "howe are the migh", _TAIL),
        "Job.6.29": (["Job.6.29", "Job.6.30"], "Is there iniquitie in my tongu", _TAIL),
        "Ps.72.19": (["Ps.72.19", "Ps.72.20"], "HERE END THE prayers", _TAIL),
        "Jer.49.38": (["Jer.49.38", "Jer.49.39"], "in the latter daies", _TAIL),
        "Rom.1.30": (["Rom.1.30", "Rom.1.31"], "without vnderstanding", _TAIL),
        "Heb.13.6": (["Heb.13.5"], "I will not faile thee, neither forsake thee",
                     "the end of the KJV's 13:5, which the Geneva numbers as 13:6"),
        "Rev.12.18": (["Rev.13.1"], "And I stood on the sea sand",
                      "the first words of the KJV's 13:1, which the Geneva ends chapter 12 with"),
    },
    "tyndale": {
        "Rom.1.23": (["Rom.1.22", "Rom.1.23"], "When they couted them selves wyse", _EMPTY),
        "1Cor.3.22": (["1Cor.3.21", "1Cor.3.22"], "Therfore let no ma reioyce in men", _EMPTY),
    },
    "ylt": {
        "Gen.18.11": (["Gen.18.10"], "Sarah is hearkening at the opening of the tent",
                      "Young ends the KJV's 18:10 as a verse of its own, and numbers on one "
                      "ahead to 18:14"),
        "Gen.18.12": (["Gen.18.11"], "Abraham and Sarah are aged", _SHIFT18),
        "Gen.18.13": (["Gen.18.12"], "Sarah laugheth in her heart", _SHIFT18),
        "Gen.18.14": (["Gen.18.13", "Gen.18.14"], "Is any thing too wonderful for Jehovah",
                      _SHIFT18),
        "Song.2.1": (["Song.2.2"], "As a lily among the thorns",
                     "Young's 1:17 ends with the KJV's 2:1; his 2:1-2 are the KJV's 2:2"),
        "Zech.7.6": (["Zech.7.5", "Zech.7.6"], "When ye fasted with mourning",
                     "Young's 7:6 opens with the second half of the KJV's 7:5"),
    },
    "coverdale": {
        "Exod.38.14": (["Exod.38.14", "Exod.38.15"], "vpon either syde of the courte dore",
                       _HOLDS),
        "Deut.14.19": (["Deut.14.19"], "And all foules yt crepe",
                       "the KJV's 14:19 only: the words of 14:20 ('of all clean fowls ye may "
                       "eat') are in no verse of this transcription"),
        "1Kgs.6.32": (["1Kgs.6.31", "1Kgs.6.32"], "he made two dores of olyue", _HOLDS),
        "Ps.14.2": (["Ps.14.2", "Ps.14.3"], "But they are all gone out of the waye", _COVPS),
        "Ps.14.3": ([], "Their throte is an open sepulcre", _ROM3),
        "Ps.14.4": ([], "their fete are swift to shed bloude", _ROM3),
        "Ps.18.46": (["Ps.18.45"], "The straunge children are waxe olde", _COVPS),
        "Ps.40.14": (["Ps.40.15"], "that crie ouer me: there there", _COVPS),
        "Ps.40.16": (["Ps.40.17"], "As for me, I am poore", _COVPS),
        "Ps.79.13": (["Ps.79.12", "Ps.79.13"], "rewarde the (o LORDE) seuefolde", _COVPS),
        "Ps.93.2": (["Ps.93.1"], "he hath made the rounde worlde so sure", _COVPS),
        "Ps.93.4": (["Ps.93.3"], "The floudes aryse", _COVPS),
        "Ps.93.5": (["Ps.93.4", "Ps.93.5"], "The wawes of the see are mightie", _COVPS),
        "Ps.130.1": (["Ps.130.1", "Ps.130.2"], "LORDE heare my voyce", _COVPS),
        "Hab.3.4": (["Hab.3.3", "Hab.3.4"], "His glory couereth the heauens",
                    "the second half of the KJV's 3:3 opens Coverdale's 3:4"),
    },
    "darby": {
        "Phil.1.16": (["Phil.1.17"], "These indeed out of love", _PHIL),
        "Phil.1.17": (["Phil.1.16"], "but those out of contention", _PHIL),
    },
    "asv": {
        "Phil.1.16": (["Phil.1.17"], "the one do it of love", _PHIL),
        "Phil.1.17": (["Phil.1.16"], "but the other proclaim Christ of faction", _PHIL),
        "1John.5.7": (["1John.5.6"], "it is the Spirit that beareth witness",
                      "the second half of the KJV's 5:6; the ASV prints no heavenly "
                      "witnesses, and numbers its 5:6 in two"),
    },
}


def _stop(msg):
    raise SystemExit(f"HARD STOP: {msg}")


def out_path(slug):
    return os.path.join(OUTDIR, f"{slug}-kjv.json")


# ---------------------------------------------------------------- inputs

_KJV = {}


def kjv():
    """{ref: text}, in the KJV's order."""
    if not _KJV:
        with open(KJV_TSV, encoding="utf-8") as f:
            for line in f:
                i, _, t = line.rstrip("\n").partition("\t")
                if i.startswith("kjv:"):
                    _KJV[i[4:]] = t
    return _KJV


def kjv_books():
    return list(dict.fromkeys(k.split(".")[0] for k in kjv()))


def verses(slug):
    """[(ref, text)] of the Bible's slots that have text, in order, with OSIS
    book ids (the file holds the 66 books in the KJV's order)."""
    out = []
    for ref, raw in slots(slug):
        t = re.sub(r"\s+", " ", raw).strip()
        if t:
            out.append((ref, t))
    return out


def slots(slug):
    """[(ref, text as the source has it)] of every slot in the file, in order."""
    e = FS.ENGLISH[slug]
    p = os.path.join(CORPUS, e["file"])
    if not os.path.exists(p) or BVV.BV.sha256(p) != e["sha256"]:
        _stop(f"{e['file']} missing or changed. Run --fetch.")
    books = kjv_books()
    try:
        rows = FS.english_slots(slug, p, len(books))
    except (ValueError, RuntimeError) as x:
        _stop(str(x))
    return [(f"{books[n - 1]}.{c}.{v}", t) for n, _name, c, v, t in rows]


def empty_slots(slug):
    return [r for r, t in slots(slug) if not t.strip()]


# ---------------------------------------------------------------- alignment

# Tudor spelling hides agreement from the plain tokens (Coverdale agrees with
# the KJV's same-numbered verse at a mean Dice of 0.31 with them; 0.53 with
# these). Both sides are folded the same way: v->u, j->i, y->i, ck->k,
# doubled letters single, a final -e dropped ("heauen"/"heaven" -> "heauen",
# "fete"/"feet" -> "fet"). Only the Bibles named here read this way, so the
# five maps built before it are unchanged.
OLD_SPELLING = {"coverdale"}


def _fold(w):
    w = w.replace("v", "u").replace("j", "i").replace("y", "i").replace("ck", "k")
    w = re.sub(r"(.)\1+", r"\1", w)
    return w[:-1] if len(w) > 3 and w.endswith("e") else w


_OSTOP = {_fold(w) for w in BVV._STOP}


def _otoks(t):
    return {w[:5] for w in (_fold(x) for x in re.findall(r"[a-z]+", t.lower()))
            if w not in _OSTOP and len(w) > 2}


def tokens_for(slug):
    return _otoks if slug in OLD_SPELLING else BVV._etoks


def align(D, K):
    """Monotonic alignment of token sets D (the Bible's verses) against K (the
    KJV's), free to start and end anywhere in K. Returns
    ({i: [j...]}, total score)."""
    n, M = len(D), len(K)
    best = {(0, j): (0.0, None) for j in range(0, M + 1)}
    for i in range(n + 1):
        for j in range(M + 1):
            if (i, j) not in best:
                continue
            sc = best[(i, j)][0]
            for a, b, pen in BEADS:
                ni, nj = i + a, j + b
                if ni > n or nj > M:
                    continue
                A = set().union(*D[i:ni]) if a else set()
                B = set().union(*K[j:nj]) if b else set()
                s2 = sc + (BVV._dice(A, B) if a and b else 0) - pen
                if (ni, nj) not in best or best[(ni, nj)][0] < s2 - 1e-12:
                    best[(ni, nj)] = (s2, (i, j))
    ends = sorted((k for k in best if k[0] == n), key=lambda k: (-best[k][0], k[1]))
    end = ends[0]
    total = best[end][0]
    al = {}
    while best[end][1]:
        pi, pj = best[end][1]
        for x in range(pi, end[0]):
            al[x] = list(range(pj, end[1]))
        end = (pi, pj)
    return al, total


def compute(slug):
    tok = tokens_for(slug)
    kj = kjv()
    kord = list(kj)
    kidx = {k: i for i, k in enumerate(kord)}
    KT = [tok(kj[k]) for k in kord]
    vs = verses(slug)
    text = dict(vs)
    house = HOUSE_ROWS.get(slug, {})
    chapters = {}
    for r, _t in vs:
        chapters.setdefault(r.rsplit(".", 1)[0], []).append(r)
    target, no_kjv, aligned_chapters, widened, filled = {}, {}, {}, [], {}
    for ch, refs in chapters.items():
        book = ch.split(".")[0]
        same = [kidx.get(r) for r in refs]
        D = [tok(text[r]) for r in refs]
        id_score = sum(BVV._dice(D[i], KT[same[i]]) if same[i] is not None else 0
                       for i in range(len(refs))) / len(refs)
        ks = [i for i, k in enumerate(kord) if k.rsplit(".", 1)[0] == ch]
        if ks:
            lo, hi = ks[0], ks[-1] + 1
        else:
            lo = hi = min((s for s in same if s is not None), default=0)
        lo, hi = max(0, lo - REACH), min(len(kord), hi + REACH)
        while kord[lo].split(".")[0] != book:
            lo += 1
        while kord[hi - 1].split(".")[0] != book:
            hi -= 1
        al, _tot = align(D, KT[lo:hi])
        al_score = sum(BVV._dice(D[i], set().union(*(KT[lo + j] for j in al[i])))
                       if al.get(i) else 0 for i in range(len(refs))) / len(refs)
        follow = (al_score - id_score >= GAIN
                  and any([kord[lo + j] for j in al.get(i, [])] != [refs[i]]
                          for i in range(len(refs))))
        if follow:
            aligned_chapters[ch] = {"same_numbers": round(id_score, 3),
                                    "aligned": round(al_score, 3)}
        for i, r in enumerate(refs):
            if r in house:
                es, words, why = house[r]
                if words not in text[r]:
                    _stop(f"HOUSE_ROWS {slug} {r}: {words!r} is not in the verse")
                if es:
                    target[r] = list(es)
                else:
                    no_kjv[r] = why
            elif follow:
                es = [kord[lo + j] for j in al.get(i, [])]
                if es:
                    target[r] = es
                else:
                    no_kjv[r] = ("the alignment pairs it with no KJV verse in a chapter that "
                                 "numbers otherwise")
            elif r in kidx:
                # Same numbers, but a merged slot holds the next verse(s) too
                # (Luke 15:31 holding 15:31-32): take the alignment's wider
                # reading of this one verse when it contains the same number
                # and reads clearly better.
                # Likewise a stretch inside the chapter numbered otherwise (Gal
                # 1:22-23 holding the KJV's 1:23-24): a verse the alignment
                # moves, where it reads much better there.
                es = [kord[lo + j] for j in al.get(i, [])]
                gain = (BVV._dice(D[i], set().union(*(KT[kidx[e]] for e in es)))
                        - BVV._dice(D[i], KT[kidx[r]])) if es else 0
                if es != [r] and (gain >= VERSE_GAIN or (r in es and gain >= 0.1)):
                    target[r] = es
                    widened.append(r)
                else:
                    target[r] = [r]
            else:
                no_kjv[r] = "no KJV verse of this number"
    # A KJV verse no verse reached, standing between what one verse and the
    # next reach, belongs to the first of them when that verse closes its
    # chapter (CrossWire merges a chapter's overflow into its last slot:
    # Dan 3:30 holds the KJV's 3:30 and 4:1-3), or when the verse reads
    # better with it; to the second when that one reads better with it (an
    # empty slot whose words the module put in the next one).
    reached = {e for es in target.values() for e in es}
    placed = [r for r in (x for x, _ in vs) if r in target]
    last_of = {refs[-1] for refs in chapters.values()}
    for a, b in zip(placed, placed[1:]):
        i, j = kidx[target[a][-1]], kidx[target[b][0]]
        gap = [kord[x] for x in range(i + 1, j) if kord[x] not in reached
               and kord[x].split(".")[0] == a.split(".")[0]]
        if not gap:
            continue

        def gain(x):
            T = tok(text[x])
            return (BVV._dice(T, set().union(*(KT[kidx[e]] for e in target[x] + gap)))
                    - BVV._dice(T, set().union(*(KT[kidx[e]] for e in target[x]))))
        ga = gain(a) if a not in house else -1
        gb = gain(b) if b not in house else -1
        if gb >= 0.05 and gb > ga:      # an empty slot, its words in the next (Tyndale Matt 5:48)
            target[b] = sorted(gap + target[b], key=kidx.get)
            filled[b] = gap
        elif (a in last_of and a not in house) or ga >= 0.05:
            target[a] = target[a] + gap
            filled[a] = gap
        else:
            continue
        reached.update(gap)
    bad = [(r, es) for r, es in target.items() if any(e not in kidx for e in es)]
    if bad:
        _stop(f"{slug}: targets not in the KJV: {bad[:10]}")
    reached = {e for es in target.values() for e in es}
    books = {r.split(".")[0] for r in text}
    missing = [k for k in kord if k.split(".")[0] in books and k not in reached]
    why_missing = HOUSE_MISSING.get(slug, {})
    unexplained = [k for k in missing if k not in why_missing]
    report = os.environ.get("ENGLISH_EXPLORE")
    if unexplained and report:
        print(f"EXPLORE {slug}: {len(unexplained)} KJV verses unreached: {unexplained[:60]}")
    elif unexplained:
        _stop(f"{slug}: {len(unexplained)} KJV verse(s) reached from no verse, first "
              f"{unexplained[:40]}")
    if no_kjv and report:
        print(f"EXPLORE {slug}: no KJV verse: {list(no_kjv.items())[:40]}")
    return {"slug": slug, "refs": [r for r, _ in vs], "text": text, "target": target,
            "no_kjv": no_kjv, "aligned_chapters": aligned_chapters,
            "without": {k: why_missing.get(k, "?") for k in missing}, "widened": widened, "filled": filled,
            "books": [b for b in kjv_books() if b in books], "kord": kord}


HOUSE_MISSING = {    # {slug: {KJV verse: why the Bible has no verse for it}}
    "tyndale": {"Mark.11.26": "this transcription of Tyndale has no words for it"},
    "darby": {v: "Darby leaves it out of his text (a verse the oldest manuscripts lack)"
              for v in ["Matt.23.14", "Acts.8.37", "Acts.15.34"]},
    "asv": {**{v: "the ASV leaves it out of its text (a verse the oldest manuscripts lack)"
               for v in ["Matt.17.21", "Matt.18.11", "Matt.23.14", "Mark.7.16", "Mark.9.44",
                         "Mark.9.46", "Mark.11.26", "Mark.15.28", "Luke.17.36", "Luke.23.17",
                         "John.5.4", "Acts.8.37", "Acts.15.34", "Acts.24.7", "Acts.28.29",
                         "Rom.16.24"]},
            "1John.5.7": "the heavenly witnesses (the Comma Johanneum), which the ASV does "
                         "not print; its 5:7-8 are the KJV's 5:6b and 5:8"},
    "geneva": {"Song.1.1": "the title (\"The song of songs, which is Solomon's\"): the "
                           "Geneva prints it as the book's heading, not as a verse"},
    "coverdale": {**{v: "this transcription has no words for it: the source's slot reads "
                        "'(Omitted Text)', and the verses around it do not hold its words"
                     for v in ["Lev.15.23", "Num.7.64", "Josh.15.52", "Josh.15.53",
                               "Josh.15.54", "Neh.13.27", "Mark.6.46", "Mark.11.26",
                               "Luke.17.36", "Rev.21.26"]},
                  "Deut.14.20": "this transcription has no words for it: the source's slot "
                                "reads '(Omitted Text)', and 14:19 holds only the KJV's 14:19",
                  "Ps.136.24": "this transcription has no words for it ('And hath redeemed "
                               "us from our enemies'): its 136:24-25 are the KJV's 136:25-26, "
                               "and its 136:26 reads '(Omitted Text)'"},
}


# ---------------------------------------------------------------- output

def _runs(refs):
    out = []
    for r in refs:
        b, c, v = r.split(".")
        if out and out[-1][0] == (b, c) and int(v) == out[-1][2] + 1:
            out[-1][2] = int(v)
        else:
            out.append([(b, c), int(v), int(v)])
    return [f"{b}.{c}.{a}" + (f"-{z}" if z != a else "") for (b, c), a, z in out]


def build(slug):
    r = compute(slug)
    e = FS.ENGLISH[slug]
    diff = {}
    for v in r["refs"]:
        es = r["target"].get(v)
        if es and es != [v]:
            diff[v] = es[0] if len(es) == 1 else es
    by_why = {}
    for v in r["refs"]:
        if v in r["no_kjv"]:
            by_why.setdefault(r["no_kjv"][v], []).append(v)
    chapters = {}
    for v in r["refs"]:
        b, c, x = v.split(".")
        chapters.setdefault(f"{b}.{c}", []).append(int(x))
    shared = {}
    for v, es in r["target"].items():
        for k in es:
            shared.setdefault(k, []).append(v)
    module = ("the CrossWire module the source was built from" if e.get("source") != "bss"
              else "Bible SuperSearch's module")
    return {
        "note": (f"{e['title']} -> KJV verse numbers. Only the verses whose KJV reference "
                 "differs are in `map`; any other verse not named in `no_kjv_verse` has the "
                 f"same reference in the KJV. The ids are the slots of {module} "
                 "(the KJV's grid): the Bible's own numbers, except "
                 "where it numbers otherwise and a chapter's overflow sits merged in its last "
                 "slot (a list value: one verse holding several KJV verses). "
                 "`aligned_chapters` are the chapters read off the English, with how well "
                 "the same numbers and the alignment agree with the KJV. Built by "
                 "pipeline/build_english_versification.py; do not hand-edit."),
        "from": slug, "to": "kjv",
        "source": FS.english_source(slug),
        "rights": {"license": "public-domain",
                   "note": "the house's own reading of two public-domain texts"},
        **({"tokens": "old spelling folded on both sides before comparing (v/u, j/i, y/i, "
                      "ck/k, doubled letters, final -e): build_english_versification._fold"}
           if slug in OLD_SPELLING else {}),
        **({"coverage": e["coverage"]} if e.get("source") == "bss" and "coverage" in e else {}),
        "checked_against": {"kjv": os.path.relpath(KJV_TSV, ROOT),
                            "verses": len(r["refs"]), "books": len(r["books"]),
                            "verses_landing_on_no_kjv_verse_unexplained": 0,
                            "kjv_verses_reached_from_no_verse": len(r["without"])},
        "counts": {"differing_verses": len(diff),
                   "spanning_several_kjv_verses": sum(isinstance(x, list) for x in diff.values()),
                   "kjv_verses_shared_by_several_verses": sum(len(x) > 1 for x in shared.values()),
                   "verses_with_no_kjv_verse": len(r["no_kjv"]),
                   "aligned_chapters": len(r["aligned_chapters"]),
                   "house_rows": len(HOUSE_ROWS.get(slug, {}))},
        "aligned_chapters": r["aligned_chapters"],
        "house_rows": {v: {"kjv": es, "why": why}
                       for v, (es, _w, why) in HOUSE_ROWS.get(slug, {}).items()},
        "empty_slots": _runs(empty_slots(slug)),
        "chapters": {c: len(xs) if xs == list(range(1, len(xs) + 1)) else
                     ",".join(map(str, xs)) for c, xs in chapters.items()},
        "no_kjv_verse": [{"verses": _runs(vs), "count": len(vs), "why": why}
                         for why, vs in by_why.items()],
        "kjv_without_verse": r["without"],
        "map": diff,
    }


def audit(slug, show=80):
    """For reading: the verses whose mapped KJV verse reads clearly worse than
    a KJV verse within three of it (Dice >= 0.45, and 0.25 better). Old
    spelling makes many verses agree weakly with every KJV verse; this lists
    only the ones some other nearby verse plainly fits."""
    r = compute(slug)
    tok = tokens_for(slug)
    kj = kjv()
    kord = r["kord"]
    kidx = {k: i for i, k in enumerate(kord)}
    toks = {k: tok(t) for k, t in kj.items()}
    print(f"{slug}: aligned chapters {r['aligned_chapters']}")
    flags = []
    for v in r["refs"]:
        es = r["target"].get(v, [])
        if not es:
            continue
        T = tok(r["text"][v])
        s = BVV._dice(T, set().union(*(toks[e] for e in es)))
        i = kidx[es[0]]
        near = max(((BVV._dice(T, toks[kord[x]]), kord[x])
                    for x in range(max(0, i - 3), min(len(kord), i + 4)) if kord[x] not in es),
                   default=(0, None))
        if near[0] >= 0.45 and near[0] >= s + 0.25:
            flags.append((v, es, round(s, 2), near[1], round(near[0], 2)))
    print(f"  verses a nearby KJV verse fits clearly better: {len(flags)}")
    for f in flags[:show]:
        print(f"    {f[0]} -> {f[1]} ({f[2]}); {f[3]} ({f[4]}): {r['text'][f[0]][:60]}")
    print(f"  KJV verses reached from no verse: {sorted(r['without'])}")
    return flags


def render(doc):
    return (json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--audit", action="store_true")
    a = ap.parse_args()
    slugs = a.slugs or list(FS.ENGLISH)
    if a.fetch:
        for s in slugs:
            print(f"{s}: {FS.fetch_english(s)}")
        return
    if a.audit:
        for s in slugs:
            audit(s)
        return
    for s in slugs:
        blob = render(build(s))
        rel = os.path.relpath(out_path(s), ROOT)
        if a.check:
            if not os.path.exists(out_path(s)):
                _stop(f"{rel} missing")
            if open(out_path(s), "rb").read() != blob:
                _stop(f"{rel} differs from a rebuild")
            print(f"OK: {rel} byte-identical; every invariant holds")
            continue
        if os.environ.get("ENGLISH_EXPLORE"):
            _stop("ENGLISH_EXPLORE is set: the invariants were not enforced, so nothing is written")
        with open(out_path(s) + ".tmp", "wb") as f:
            f.write(blob)
        os.replace(out_path(s) + ".tmp", out_path(s))
        print(f"wrote {rel}: {json.loads(blob)['counts']}")


if __name__ == "__main__":
    main()
