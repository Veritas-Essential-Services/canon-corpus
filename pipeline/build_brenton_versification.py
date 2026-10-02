#!/usr/bin/env python3
# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""
build_brenton_versification.py -- Brenton's English Septuagint -> KJV verse
map, so a verse cited in Brenton's (the Greek's) numbering (brenton:Ps.50.3)
lands on the kjv: unit holding the same text (kjv:Ps.51.1).

    python3 pipeline/build_brenton_versification.py --fetch   # TVTMS + Brenton, pinned
    python3 pipeline/build_brenton_versification.py           # build data/versification/brenton-kjv.json
    python3 pipeline/build_brenton_versification.py --check   # rebuild: byte-identical, every invariant holds
    python3 pipeline/build_brenton_versification.py --audit   # Brenton's English against the KJV's

THE SAME METHOD AS THE VULGATE'S MAP (build_vulgate_versification.py, whose
TVTMS reader this uses): STEPBible's TVTMS (CC BY 4.0, the pinned file) gives
block by block the numbering of each tradition, with TESTS that tell a Bible
which column it follows. The build RUNS those tests on Brenton's own verse
list. Its tests of verse EXISTENCE decide which columns can apply; its
word-count tests are only approximate on a translation, so among the columns
left the one whose pairs agree best with the KJV's English is followed (ties:
fewer word-count failures, then a column TVTMS names for Brenton, then the
Greek family). eBible's Brenton keeps the KJV's or the Hebrew's numbers in
places, so a non-Greek column may pass; where its pairs clash with a Greek
block's, the block is re-read by its Greek column. Where nothing passes, the
nearest Greek column is followed and its failed tests recorded.

    TVTMS writes the Greek's additions as SUBVERSES (Est.1:1.1-17); Brenton
    LETTERS them (Esth.1.1b). The build reads Brenton's n-th lettered verse
    after verse V as TVTMS's V.n. Brenton's Nehemiah is chapters 11-23 of
    his "Ezra and Nehemiah" (the Greek's 2 Esdras): its ids keep that
    numbering (Ezra.11.1) and TVTMS reads it as Neh 1-13.

THE CHECK: Brenton is English, so the map is tested against the KJV's words
directly. --audit aligns Brenton's English with the KJV's, verse by verse
(the alignment --audit-douay runs for the Vulgate), and lists every verse
whose aligned KJV verses share nothing with the map's. What reading those
found went into HOUSE_ROWS, each with words that must stand in Brenton's
verse, so a changed source fails loudly. The build refuses to write unless
  * every Brenton verse lands on a kjv: unit or a KJV psalm title, or is
    named as having no KJV verse, with why;
  * every KJV verse is reached from a Brenton verse, or the followed column
    says Brenton has none, or Brenton prints no verse of its number (said
    so, and not read verse by verse: the text may be in a neighbour).

WHAT THE MAP SAYS: `map` lists the Brenton verses whose KJV reference
differs (a list value: several KJV verses). `no_kjv_verse` names, by run,
every Brenton verse with no KJV verse, and why. `kjv_without_brenton_verse`
names the KJV verses Brenton has no verse for. `brenton_verses` is Brenton's
verse list per chapter, so a reference that is no Brenton verse is caught.
Rights: the derived subset carries TVTMS's attribution and
`redistribute_whole: false`, as the other maps do.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_versification as BV            # noqa: E402  (the pinned TVTMS)
import build_vulgate_versification as BVV   # noqa: E402  (its TVTMS block reader)
import fetch_sources as FS                  # noqa: E402  (the pinned Brenton)
import structure_texts as S                 # noqa: E402  (the Brenton reader)

ROOT = BV.ROOT
OUT = os.path.join(ROOT, "data", "versification", "brenton-kjv.json")
ZIP = os.path.join(BV.CORPUS, "brenton", "eng-Brenton_usfm.zip")
KJV_TSV = BVV.KJV_TSV

# Column preference inside a block, when several pass (after any column
# TVTMS names for Brenton).
def _rank(col):
    if "Brenton" in col:
        return 0
    if col.startswith(("Greek", "Grk")):
        return 1
    if col.startswith("English"):
        return 2
    return 3


NOT_IN_KJV_BOOKS = {
    "Tob": "Tobit: not in the KJV's canon (printed as Apocrypha)",
    "Jdt": "Judith: not in the KJV's canon (printed as Apocrypha)",
    "Wis": "Wisdom: not in the KJV's canon (printed as Apocrypha)",
    "Sir": "Sirach: not in the KJV's canon (printed as Apocrypha, Ecclesiasticus)",
    "Bar": "Baruch: not in the KJV's canon (printed as Apocrypha)",
    "EpJer": "the Epistle of Jeremy: not in the KJV's canon (printed as Apocrypha, Baruch 6)",
    "Sus": "Susanna: not in the KJV's canon (printed as Apocrypha)",
    "Bel": "Bel and the Dragon: not in the KJV's canon (printed as Apocrypha)",
    "1Macc": "1 Maccabees: not in the KJV's canon (printed as Apocrypha)",
    "2Macc": "2 Maccabees: not in the KJV's canon (printed as Apocrypha)",
    "1Esd": "1 Esdras: not in the KJV's canon (printed as Apocrypha)",
    "PrMan": "the Prayer of Manasses: not in the KJV's canon (printed as Apocrypha)",
    "3Macc": "3 Maccabees: not in the KJV's canon or its Apocrypha",
    "4Macc": "4 Maccabees: not in the KJV's canon or its Apocrypha",
}
NOT_IN_KJV_RANGES = [   # (book, chapter, first verse, last verse, why), Brenton's numbering
    ("Ps", 151, 0, 999, "Psalm 151, which the Greek has and the Hebrew does not"),
    ("Dan", 3, 24, 90, "the Song of the Three Children, a Greek addition; the KJV prints it "
                       "as Apocrypha"),
]
WHY_LETTERED = ("a passage the Greek has here and the Hebrew does not, lettered by Brenton; "
                "the KJV has no verse for it (some such passages repeat text the KJV has "
                "elsewhere)")
WHY_ESTHER = "the Greek additions to Esther; the KJV prints them as Apocrypha (the Rest of Esther)"
WHY_PROLOGUE = "text Brenton prints before verse 1 (the Greek's own prologue); the KJV has none"

# Where reading Brenton against the KJV found a correspondence TVTMS does not
# give. {Brenton verse: ([KJV verses], words in Brenton's verse, why)}; an
# empty list: no KJV verse, for the stated reason. `words` must stand in
# Brenton's verse (the build checks it), so a changed source fails loudly.
_PROV24 = ("Proverbs 24-31 in the Greek's order: Brenton numbers the Greek's 24:1-22, then "
           "the KJV's 30:1-14 (his 24:22f-t), the KJV's 24:23-34 (his 24:23-34), the KJV's "
           "30:15-33 (his 24:35-53) and 31:1-9 (his 24:54-62); his 25-29 are the KJV's, and "
           "his 31:10-31 the KJV's 31:10-31. TVTMS has no row for it; read verse by verse")
_REDIV = ("Brenton divides the passage differently from the KJV (the Greek's own verse "
          "breaks); read in both texts")
_JER49 = ("Jeremiah's oracles on the nations stand in the Greek's order: Brenton's 25:14-20 "
          "is the KJV's 49:34-39 (Elam), his 30:1-16 the KJV's 49:7-22 (Edom), 30:17-21 "
          "49:1-5 (Ammon), 30:23-28 49:28-33 (Kedar), 30:29-33 49:23-27 (Damascus). No "
          "TVTMS column has Brenton's order; read verse by verse")
_EXOD39 = ("the Greek's account of the finished work names the tabernacle's furnishings in "
           "its own order, and its 39:12 (the gold left over) is in no KJV verse; read item "
           "by item")
SKIP_BLOCKS = {"$Jer.49:1-49:39": _JER49}
# KJV verses no Brenton verse holds, where a skipped block would have said so.
KJV_ABSENT = {"Jer.49.6": "the Greek has no verse for it (TVTMS: Jer.30:22 [Empty]); "
                          "Brenton prints 30:22 empty"}
_REVIEW = ("found in review, reading Brenton's English against the KJV's: the KJV verse(s) "
           "named hold this verse's text, and TVTMS's row (or its silence, the same number) "
           "does not. Ps 97/98: TVTMS's title cell for the KJV's Ps 98 reads [=Psa.98:1], "
           "which in the Greek's numbering is the KJV's Ps 99, a psalm with no title. "
           "1 Kgs 2:46c (Lebanon) has no KJV verse; 2:46d's Thermae is the KJV's Tadmor (9:18)")
HOUSE_ROWS = {
    **{v: (es, w, _PROV24) for v, (es, w) in {
        "Prov.24.22f": (["Prov.30.1"], "My son, reverence my words"),
        "Prov.24.22g": (["Prov.30.2"], "the most simple of all men"),
        "Prov.24.22h": (["Prov.30.3"], "God has taught me wisdom"),
        "Prov.24.22i": (["Prov.30.4"], "Who has gone up to heaven"),
        "Prov.24.22k": (["Prov.30.5"], "the words of God are tried"),
        "Prov.24.22l": (["Prov.30.6"], "Add not unto his words"),
        "Prov.24.22m": (["Prov.30.7"], "Two things I ask of thee"),
        "Prov.24.22n": (["Prov.30.8"], "Remove far from me vanity"),
        "Prov.24.22o": (["Prov.30.9"], "lest I be filled"),
        "Prov.24.22p": (["Prov.30.10"], "Deliver not a servant"),
        "Prov.24.22q": (["Prov.30.11"], "curse their father"),
        "Prov.24.22r": (["Prov.30.12"], "judge themselves to be just"),
        "Prov.24.22s": (["Prov.30.13"], "have lofty eyes"),
        "Prov.24.22t": (["Prov.30.14"], "have swords for teeth"),
        "Prov.24.35": (["Prov.30.15"], "The horse-leech had three"),
        "Prov.24.36": (["Prov.30.16"], "The grave, and the love of a woman"),
        "Prov.24.37": (["Prov.30.17"], "The eye that laughs to scorn a father"),
        "Prov.24.38": (["Prov.30.18"], "three things impossible for me"),
        "Prov.24.39": (["Prov.30.19"], "the track of a flying eagle"),
        "Prov.24.40": (["Prov.30.20"], "the way of an adulterous woman"),
        "Prov.24.41": (["Prov.30.21"], "By three things the earth is troubled"),
        "Prov.24.42": (["Prov.30.22"], "if a servant reign"),
        "Prov.24.43": (["Prov.30.23"], "cast out her own mistress"),
        "Prov.24.44": (["Prov.30.24"], "four very little things"),
        "Prov.24.45": (["Prov.30.25"], "the ants which are weak"),
        "Prov.24.46": (["Prov.30.26"], "the rabbits also"),
        "Prov.24.47": (["Prov.30.27"], "The locusts have no king"),
        "Prov.24.48": (["Prov.30.28"], "And the eft"),
        "Prov.24.49": (["Prov.30.29"], "three things which go well"),
        "Prov.24.50": (["Prov.30.30"], "A lion's whelp"),
        "Prov.24.51": (["Prov.30.31"], "a cock walking in boldly"),
        "Prov.24.52": (["Prov.30.32"], "If thou abandon thyself to mirth"),
        "Prov.24.53": (["Prov.30.33"], "Milk out milk"),
        "Prov.24.54": (["Prov.31.1"], "the oracular answer of a king"),
        "Prov.24.55": (["Prov.31.2"], "What wilt thou keep, my son"),
        "Prov.24.56": (["Prov.31.3"], "Give not thy wealth to women"),
        "Prov.24.57": (["Prov.31.4"], "let them then not drink wine"),
        "Prov.24.58": (["Prov.31.5"], "lest they drink, and forget wisdom"),
        "Prov.24.59": (["Prov.31.6"], "Give strong drink to those that are in sorrow"),
        "Prov.24.60": (["Prov.31.7"], "that they may forget their poverty"),
        "Prov.24.61": (["Prov.31.8"], "Open thy mouth with the word of God"),
        "Prov.24.62": (["Prov.31.9"], "Open thy mouth and judge justly"),
    }.items()},
    **{v: (es, w, _REDIV) for v, (es, w) in {
        "Gen.8.3": (["Gen.8.3", "Gen.8.4"], "and the ark rested"),
        "Gen.8.4": (["Gen.8.5"], "And the water continued to"),
        "Lev.8.18": (["Lev.8.18", "Lev.8.19"], "And Moses brought near the"),
        "Lev.8.19": (["Lev.8.20", "Lev.8.21"], "And he divided the ram"),
        "Lev.8.20": (["Lev.8.21"], "And Moses offered up the"),
        "Lev.8.21": (["Lev.8.22"], "And Moses brought the second"),
        "Lev.8.22": (["Lev.8.23"], "and Moses took of his"),
        "Lev.8.23": (["Lev.8.24"], "And Moses brought near the"),
        "Lev.8.24": (["Lev.8.25"], "And he took the fat"),
        "Lev.8.25": (["Lev.8.26"], "And from the basket of"),
        "Lev.8.26": (["Lev.8.27"], "and put them all on"),
        "Lev.8.27": (["Lev.8.28"], "And Moses took them at"),
        "Lev.8.28": (["Lev.8.29"], "And Moses took the breast"),
        "Lev.8.29": (["Lev.8.30"], "And Moses took of the"),
        "Num.21.19": (["Num.21.19", "Num.21.20"], "and from Manthanain to Naaliel"),
        "Num.21.20": (["Num.21.21"], "And Moses sent ambassadors to"),
        "Num.21.21": (["Num.21.22"], "We will pass through thy"),
        "Num.27.3": (["Num.27.3", "Num.27.4"], "Our father died in the"),
        "Num.27.4": (["Num.27.5"], "And Moses brought their case"),
        "Num.27.5": (["Num.27.6"], "And the Lord spoke to"),
        "Num.27.6": (["Num.27.7"], "The daughters of Salpaad have"),
        "Num.27.7": (["Num.27.8"], "And thou shalt speak to"),
        "Deut.5.17": (["Deut.5.17"], "Thou shalt not commit murder"),
        "Deut.5.18": (["Deut.5.18"], "Thou shalt not commit adultery"),
        "Exod.28.29a": (["Exod.28.24"], "thou shalt put the wreaths on both sides"),
        "Exod.28.30": (["Exod.28.25", "Exod.28.30"], "the two circlets on both the shoulders"),
        "1Kgs.5.32": (["1Kgs.5.18"], "And they prepared the stones"),
        "1Kgs.2.35i": (["1Kgs.9.15", "1Kgs.9.17", "1Kgs.9.18"], "And he built Assur"),
        "Prov.7.6": (["Prov.7.6", "Prov.7.7"], "For she looks from a"),
        "Prov.7.7": (["Prov.7.8"], "passing by the corner in"),
        "Prov.7.8": (["Prov.7.9"], "and speaking, in the dark"),
        "Prov.15.27a": (["Prov.16.6"], "By alms and by faithful"),
        "Prov.15.28a": (["Prov.16.7"], "The ways of righteous men"),
        "Prov.15.29a": (["Prov.16.8"], "Better are small receipts with"),
        "Prov.15.29b": (["Prov.16.9"], "Let the heart of a"),
        "Prov.16.9": (["Prov.16.4"], "All the works of the"),
        "Obad.1.2": (["Obad.1.1"], "Arise ye, and let us"),
        "Obad.1.3": (["Obad.1.2", "Obad.1.3"], "Behold, I have made thee"),
    }.items()},
    **{v: (es, w, _REVIEW) for v, (es, w) in {
        "Ps.97.1": (["Ps.98.title", "Ps.98.1"], "A Psalm of David. Sing to the Lord a new song"),
        "Ps.98.1": (["Ps.99.1"], "A Psalm of David. The Lord reigns"),
        "Josh.19.47": (["Josh.19.48"], "This is the inheritance of the tribe"),
        "Josh.19.48": (["Josh.19.47"], "fought against Lachis"),
        "Deut.23.25": (["Deut.23.25"], "the corn field of thy neighbour"),
        "Deut.23.26": (["Deut.23.24"], "the vineyard of thy neighbour"),
        "Prov.31.26": (["Prov.31.27"], "The ways of her household"),
        "Prov.31.27": (["Prov.31.26"], "she opens her mouth wisely"),
        "Gen.35.16": (["Gen.35.16", "Gen.35.21"], "beyond the tower of Gader"),
        "2Sam.23.29": (["2Sam.23.29", "2Sam.23.31", "2Sam.23.32"], "Asmoth the Bardiamite"),
        "1Kgs.2.46b": (["1Kgs.4.21"], "they brought gifts, and served Solomon"),
        "1Kgs.2.46c": ([], "open the domains of Libanus"),
        "1Kgs.2.46d": (["1Kgs.9.18"], "built Therm"),
        "1Kgs.2.46e": (["1Kgs.4.22", "1Kgs.4.23"], "the daily provision of Solomon"),
        "1Kgs.2.46f": (["1Kgs.4.24"], "from Raphi unto Gaza"),
        "1Kgs.2.46g": (["1Kgs.4.24", "1Kgs.4.25"], "at peace on all sides"),
        "1Kgs.2.46h": (["1Kgs.4.2", "1Kgs.4.3", "1Kgs.4.4", "1Kgs.4.5", "1Kgs.4.6"],
                       "these were the princes of Solomon"),
    }.items()},
    "Jer.10.9a": (["Jer.10.5"], "They must certainly be borne",
                  "the second half of the KJV's Jer 10:5, which the Greek has after 10:9"),
    **{v: (es, w, "the KJV's Jer 23:7-8, which the Greek has after 23:40") for v, (es, w) in {
        "Jer.23.40a": (["Jer.23.7"], "behold, the days come, saith the Lord"),
        "Jer.23.40b": (["Jer.23.8"], "who has gathered the whole seed of Israel"),
    }.items()},
    "1Kgs.2.35k": (["1Kgs.9.15"], "only after he had built the house of the Lord", _REDIV),
    "Exod.38.27": (["Exod.40.31", "Exod.40.32"], "that at it Moses and Aaron and his sons",
                   "the laver's washing, which the KJV has at 40:31-32; the Greek has it here "
                   "and has no 40:30-32"),
    **{v: (es, w, _EXOD39) for v, (es, w) in {
        "Exod.38.22": (["Exod.38.1", "Exod.38.2"], "He made the brazen altar"),
        "Exod.39.10": (["Exod.38.30"], "the brazen appendage of the altar"),
        "Exod.39.11": (["Exod.39.32"], "did as the Lord commanded Moses"),
        "Exod.39.12": ([], "of the gold that remained of the offering"),
        "Exod.39.13": (["Exod.39.1"], "the blue that was left"),
        "Exod.39.14": (["Exod.39.33"], "they brought the garments to Moses"),
        "Exod.39.15": (["Exod.39.35", "Exod.39.39"], "the ark of the covenant"),
        "Exod.39.16": (["Exod.39.37", "Exod.39.38"], "the anointing oil"),
        "Exod.39.17": (["Exod.39.37"], "oil for the light"),
        "Exod.39.18": (["Exod.39.36"], "the table of shewbread"),
        "Exod.39.19": (["Exod.39.41"], "the garments of the sanctuary"),
        "Exod.39.20": (["Exod.39.38", "Exod.39.40"], "the curtains of the court"),
        "Exod.39.21": (["Exod.39.34", "Exod.39.40"], "rams' skins dyed red"),
    }.items()},
    "Prov.16.7": ([], "The beginning of a good", WHY_LETTERED.replace(
        "lettered by Brenton", "numbered by Brenton (16:1-3, 16:7-8)")),
    "Prov.16.8": ([], "He that seeks the Lord", WHY_LETTERED.replace(
        "lettered by Brenton", "numbered by Brenton (16:1-3, 16:7-8)")),
    "Esth.1.1": ([], "In the second year of the reign of Artaxerxes", WHY_ESTHER +
                 " (Brenton numbers addition A from 1:1 and the KJV's 1:1 as 1:1s)"),
    "Esth.1.1s": (["Esth.1.1"], "And it came to pass after these things",
                  "the KJV's Esther 1:1, which Brenton letters after addition A"),
    **{v: (es, w, _JER49) for v, (es, w) in {
        "Jer.25.14": ([], "The Prophecies of Jeremias against the Nations"),
        **{f"Jer.25.{15 + i}": ([f"Jer.49.{35 + i}"], None) for i in range(5)},
        "Jer.25.20": (["Jer.49.34"], "concerning \u00c6lam"),
        **{f"Jer.30.{1 + i}": ([f"Jer.49.{7 + i}"], None) for i in range(16)},
        **{f"Jer.30.{17 + i}": ([f"Jer.49.{1 + i}"], None) for i in range(5)},
        **{f"Jer.30.{23 + i}": ([f"Jer.49.{28 + i}"], None) for i in range(6)},
        **{f"Jer.30.{29 + i}": ([f"Jer.49.{23 + i}"], None) for i in range(5)},
    }.items()},
}


def _stop(msg):
    raise SystemExit(f"HARD STOP: {msg}")


# ---------------------------------------------------------------- inputs

def fetch():
    BV.fetch()
    print(f"brenton: {FS.fetch_brenton()}")


def _require_pins():
    if not os.path.exists(BV.TVTMS_PATH) or BV.sha256(BV.TVTMS_PATH) != BV.TVTMS_SHA256:
        _stop("TVTMS missing or changed. Run --fetch.")
    if not os.path.exists(ZIP) or BV.sha256(ZIP) != FS.BRENTON["sha256"]:
        _stop("Brenton is not fetched, or differs from its pin. Run --fetch.")


def brenton():
    """[(ref, text)] in Brenton's order, refs in his numbering ('Ezra.11.1',
    '1Kgs.12.24a'); verses with no text (eBible's placeholders) left out."""
    out = []
    for osis, _t, c, v, marked in S.brenton_verses(ZIP):
        text, _n = S.brenton_text(marked)
        if text:
            out.append((f"{osis}.{c}.{v}", text))
    return out


def kjv_verses():
    uids = json.load(open(BV.REGISTRY, encoding="utf-8"))["uids"]
    ot = set(BV.TV2OSIS.values())
    return {k[4:] for k in uids if k.startswith("kjv:") and k[4:].split(".")[0] in ot}


RE_LABEL = re.compile(r"^(\d+)([a-z]?)$")


def view(refs):
    """{Brenton ref: TVTMS-view key}. The view is how TVTMS writes the same
    verse: Brenton's Nehemiah (Ezra 11-23) as Neh 1-13, and a lettered verse
    as the n-th subverse of the verse it follows ('Esth.1.1.1')."""
    out, nth = {}, {}
    for r in refs:
        b, c, v = r.split(".")
        n, letter = RE_LABEL.match(v).groups()
        c = int(c)
        if b == "Ezra" and c > 10:
            b, c = "Neh", c - 10
        if letter:
            k = nth[(b, c, n)] = nth.get((b, c, n), 0) + 1
            out[r] = f"{b}.{c}.{n}.{k}"
        else:
            out[r] = f"{b}.{c}.{n}"
    return out


def osis_key(ref, order={}):
    if not order:
        for i, b in enumerate(list(BV.TV2OSIS.values()) + list(S.BRENTON_BOOKS.values())):
            order.setdefault(b, i)
    p = ref.split(".")
    v = p[2]
    m = RE_LABEL.match(v)
    return (order.get(p[0], 99), int(p[1]),
            -1 if v == "title" else int(m.group(1)), m.group(2) if m else "",
            int(p[3]) if len(p) > 3 else 0)


def sizes_of(keys):
    """{'Book.ch': highest whole verse number} over view keys."""
    out = {}
    for k in keys:
        p = k.split(".")
        if len(p) == 3:
            out[f"{p[0]}.{p[1]}"] = max(out.get(f"{p[0]}.{p[1]}", 0), int(p[2]))
    return out


# ---------------------------------------------------------------- the tests

def _words(side, vw):
    total = 0
    for term in side.split("+"):
        osis, ch, v, sub, mul = BVV._tref(term)
        if v == "TextBeforeV1":
            raise BVV.Undecidable(term)
        key = f"{osis}.{ch}.{v}" + (f".{sub}" if sub not in (None, "0") else "")
        total += mul * len(vw.get(key, "").split())
    return total


def holds(cond, vw, sizes):
    """Does TVTMS condition `cond` hold for Brenton (`vw`: view key -> text)?"""
    cond = cond.replace(" ", "")
    m = BVV.RE_COND.match(cond)
    if not m:
        raise BVV.Undecidable(cond)
    lhs, op, rhs = m.groups()
    if op == "=":
        osis, ch, v, sub, _ = BVV._tref(lhs)
        what = rhs.lower()
        if v == "TextBeforeV1":
            # Brenton prints a psalm's title in its verse 1; text before
            # verse 1 is his verse "0" (Lamentations' prologue).
            there = bool(vw.get(f"{osis}.{ch}.0"))
        elif what == "last":
            if sub is not None:
                raise BVV.Undecidable(cond)
            return sizes.get(f"{osis}.{ch}") == int(v)
        else:
            key = f"{osis}.{ch}.{v}" + (f".{sub}" if sub not in (None, "0") else "")
            there = bool(vw.get(key, "").strip())
        if what == "exist":
            return there
        if what == "notexist":
            return not there
        raise BVV.Undecidable(cond)
    a, b = _words(lhs, vw), _words(rhs, vw)
    return a < b if op == "<" else a > b


def choose_column(block, vw, sizes, tally, greek_only=False):
    """(column, how, failed tests) for `block`. TVTMS's tests are of two
    kinds. Whether a verse exists, which is a chapter's last, whether text
    stands before verse 1: Brenton answers these exactly. Which of two verses
    has more words: Brenton answers these only roughly, being a translation
    (Ps 13's Latin and Greek columns differ only there). So a column must
    pass every existence test it can be asked; among those that do, the one
    whose pairs agree best with the KJV's words is followed (the word-count
    tests break a tie, then the preference order). Where no column passes,
    the Greek column failing fewest is followed, chosen the same way, and its
    failures recorded."""
    cols, tests = block["cols"], block["tests"]
    cands = sorted((c for c in cols if not c.startswith("English KJV")), key=_rank)
    cands.append(next(c for c in cols if c.startswith("English KJV")))
    if greek_only:
        cands = [c for c in cands if _rank(c) <= 1]
    score = {}
    for col in cands:
        hard, soft, decided = [], [], 0
        for cond in tests.get(col, []):
            try:
                r = holds(cond, vw, sizes)
            except BVV.Undecidable:
                tally["undecidable"] += 1
                continue
            decided += 1
            if not r:
                (soft if re.search(r"[<>]", cond) else hard).append(cond)
        score[col] = (hard, soft, decided)

    def pick(cs):
        if len(cs) == 1:
            return cs[0]
        return min(cs, key=lambda c: (-_agreement(block, c, vw, sizes), len(score[c][1]),
                                      _unprinted(block, c, vw, sizes), _rank(c)))
    passing = [c for c in cands if score[c][2] and not score[c][0]]
    if passing:
        best = pick(passing)
        if not score[best][1]:
            return best, "tests", []
        return best, "tests (a word-count test aside)", score[best][1]
    greek = [c for c in cands if _rank(c) <= 1]
    if not greek:
        return None, "no column passes; no Greek column", []
    if not any(tests.get(c) for c in greek):
        return greek[0], "no tests for the Greek columns", []
    fewest = min(len(score[c][0]) for c in greek)
    best = pick([c for c in greek if len(score[c][0]) == fewest])
    return best, "fallback: nearest Greek column", score[best][0] + score[best][1]


_KJV_TEXT = {}


def _kjv_toks(e):
    if not _KJV_TEXT:
        with open(KJV_TSV, encoding="utf-8") as f:
            for line in f:
                i, _, t = line.rstrip("\n").partition("\t")
                if i.startswith("kjv:"):
                    _KJV_TEXT[i[4:]] = BVV._etoks(t)
    return _KJV_TEXT[e]


def _agreement(block, col, vw, sizes):
    """Between Greek columns that fail the same number of tests: how well the
    words of the Brenton verses the column pairs agree with the KJV verses
    they are paired with (mean Dice overlap of content-word stems)."""
    _kjv_toks("Gen.1.1")
    kcol = next(c for c in block["cols"] if c.startswith("English KJV"))
    ks = BVV.chapters_of(_KJV_TEXT)
    got = [BVV._dice(BVV._etoks(vw[k]), _KJV_TEXT[e])
           for k, e in block_pairs(block, col, kcol, sizes, ks, vw)[0]
           if k in vw and e in _KJV_TEXT]
    return round(sum(got) / len(got), 6) if got else 0.0


def _unprinted(block, col, vw, sizes):
    """How many whole verses the column names that Brenton does not print: the
    tie-break between columns that fail the same number of tests."""
    i = block["cols"].index(col)
    n, named = 0, {}
    for _l, _t, cells in block["rows"]:
        if i < len(cells) and not cells[i].startswith("Absent"):
            for x in (expand(cells[i], sizes) or []):
                if x[3] in (None, 0) and x[2] != "title":
                    n += _key(x) not in vw
                    named.setdefault(f"{x[0]}.{x[1]}", set()).add(x[2])
    # ... and how many Brenton verses inside (or just past) the run it names
    # it leaves unnamed.
    for ch, vs in named.items():
        n += sum(1 for v in range(min(vs), max(vs) + 2) if v not in vs and f"{ch}.{v}" in vw)
    return n


# ---------------------------------------------------------------- build

def _key(x):
    """An expanded TVTMS cell item -> a view key (subverse 0 is the verse)."""
    b, ch, v, sub = x
    return f"{b}.{ch}.{v}" + (f".{sub}" if sub not in (None, 0) else "")


def expand(cell, sizes):
    """BVV.expand, and also a list after a book and chapter ("Exo.38:14, 15,
    17.2"): each item a verse (or verse.subverse) of that chapter."""
    m = re.match(r"^((?:[1-4]?[A-Za-z]{2,3}\.)?\d+:\d+)\.(\d+)-(\d+)$", cell.strip())
    if m:   # "Jos.9:2.1-6": subverses 1-6 of 9:2 (BVV.expand reads one)
        first = BVV.expand(f"{m.group(1)}.{m.group(2)}", sizes)
        if first:
            b, ch, v, _s = first[0]
            return [(b, ch, v, s) for s in range(int(m.group(2)), int(m.group(3)) + 1)]
    out = BVV.expand(cell, sizes)
    if out is not None or "," not in cell:
        return out
    cell = re.sub(r"\s*\[[^\]]*\]|\s*\([^)]*\)", "", cell).strip()
    m = re.match(r"^([1-4]?[A-Za-z]{2,3})\.(\d+):(.+)$", cell)
    if not m:
        return None
    out = []
    for item in (x.strip() for x in m.group(3).split(",")):
        got = BVV.expand(f"{m.group(1)}.{m.group(2)}:{item}", sizes)
        if got is None:
            return None
        out += got
    return out


def block_pairs(blk, col, kcol, vsizes, ksizes, vw):
    """(pairs, absent): pairs [(view key, KJV verse)]; absent {KJV verse:
    note}. A KJV subverse past .0 is text the KJV does not print: '+'."""
    cols = blk["cols"]
    ik, il = cols.index(kcol), cols.index(col)
    pairs, absent = [], {}
    for n, typ, cells in blk["rows"]:
        if max(ik, il) >= len(cells):
            continue
        kc, lc = cells[ik], cells[il]
        E = expand(kc, ksizes)
        if not E:
            continue
        Ek = []
        for e in E:
            k = BVV._ref(e) + ("+" if e[3] not in (None, 0) else "")
            if k not in Ek:
                Ek.append(k)
        if any(k.endswith("+") for k in Ek) and any(not k.endswith("+") for k in Ek):
            Ek = [k for k in Ek if not k.endswith("+")]
        m = re.match(r"^Absent(?:\s*\[(=?)(.+)\])?$", lc)
        if m or lc in ("NoVerse", "Empty") or "[Empty]" in lc:
            # No verse for the KJV verse; "[=X]": its text is inside verse X.
            held = (sorted({_key(x) for x in (expand(m.group(2), vsizes) or [])})
                    if m and m.group(1) else [])
            for e in Ek:
                if not e.endswith("+"):
                    absent[e] = f"{typ}: {col} {lc} (TVTMS line {n})"
                    for h in held:
                        pairs.append((h, e))
            continue
        L = expand(lc, vsizes)
        if not L:
            continue
        Lv = []
        for x in L:
            if _key(x) not in Lv:
                Lv.append(_key(x))
        if not any(x in vw for x in Lv):
            # The followed column names a verse Brenton does not print.
            for e in Ek:
                if not e.endswith("+"):
                    absent[e] = f"{typ}: {col} {lc}, which Brenton does not print (TVTMS line {n})"
            continue
        if len(Ek) == len(Lv):
            pairs += list(zip(Lv, Ek))
        elif len(Lv) == 1:
            pairs += [(Lv[0], e) for e in Ek]
        elif len(Ek) == 1:
            pairs += [(x, Ek[0]) for x in Lv]
        else:
            _stop(f"TVTMS line {n}: {kc!r} vs {col} {lc!r} do not align")
    return pairs, absent


def _why_no_kjv(ref, vkey):
    b, c, v = ref.split(".")
    n, letter = RE_LABEL.match(v).groups()
    if b in NOT_IN_KJV_BOOKS:
        return NOT_IN_KJV_BOOKS[b]
    for book, ch, lo, hi, why in NOT_IN_KJV_RANGES:
        if b == book and int(c) == ch and lo <= int(n) <= hi:
            return why
    if n == "0":
        return WHY_PROLOGUE
    if letter:
        return WHY_ESTHER if b == "Esth" else WHY_LETTERED
    return None


def compute():
    _require_pins()
    br = brenton()
    text = dict(br)
    refs = [r for r, _ in br]
    vw_of = view(refs)
    of_vw = {k: r for r, k in vw_of.items()}
    vw = {vw_of[r]: t for r, t in br}
    kjv = kjv_verses()
    vsizes, ksizes = sizes_of(vw), BVV.chapters_of(kjv)
    tally = {"undecidable": 0}
    v2e, kjv_absent, followed, left_alone, paired_from = {}, {}, {}, [], {}
    staged = []
    for blk in BVV.tvtms_blocks():
        kcol = next((c for c in blk["cols"] if c.startswith("English KJV")), None)
        if kcol is None:
            continue
        code = re.match(r"^\$([1-4]?[A-Za-z]{2,3})\.", blk["title"])
        book = BVV.TV_UPPER.get(code.group(1).upper()) if code else None
        if book is None or book not in BV.TV2OSIS.values():
            continue    # the NT, the deuterocanon, 1-4 Esdras: nothing to map to the KJV's OT
        if blk["title"] in SKIP_BLOCKS:
            left_alone.append(f"line {blk['line']} {blk['title']}: house rows ({SKIP_BLOCKS[blk['title']][:60]}...)")
            continue
        col, how, failed = choose_column(blk, vw, vsizes, tally)
        if col is None:
            left_alone.append(f"line {blk['line']} {blk['title']}: {how}")
            continue
        staged.append([blk, kcol, col, how, failed])
    # A block followed by a non-Greek column (its tests passed: Brenton keeps
    # the KJV's or the Hebrew's numbers there) passed only on verse NUMBERS.
    # Where its pairs would move a Brenton verse a Greek block already
    # placed, the numbers passed by accident (Exod 36, whose 38 verses hold
    # the KJV's chapter 39): the block is re-read by its nearest Greek column.
    greek_placed = {}
    for blk, kcol, col, how, failed in staged:
        if _rank(col) <= 1:
            for k, e in block_pairs(blk, col, kcol, vsizes, ksizes, vw)[0]:
                greek_placed.setdefault(k, set()).add(e)
    for st in staged:
        blk, kcol, col, how, failed = st
        if _rank(col) <= 1:
            continue
        pairs = block_pairs(blk, col, kcol, vsizes, ksizes, vw)[0]
        if any(k in greek_placed and e not in greek_placed[k] for k, e in pairs):
            g, ghow, gfailed = choose_column(blk, vw, vsizes, tally, greek_only=True)
            if g:
                st[2:] = [g, f"{ghow} (the passing {col} column clashes with a Greek block)",
                          gfailed]
    for blk, kcol, col, how, failed in staged:
        f = {"line": blk["line"], "column": col, "how": how}
        if failed:
            f["failed_tests"] = failed
        followed[blk["title"]] = f
        pairs, absent = block_pairs(blk, col, kcol, vsizes, ksizes, vw)
        for k, e in pairs:
            got = v2e.setdefault(k, [])
            if e not in got:
                got.append(e)
            paired_from.setdefault(e, []).append(k)
        for e, note in absent.items():
            kjv_absent[e] = note

    # Brenton ref -> KJV targets; lettered verses and view keys TVTMS never
    # names fall back to the same number (a lettered verse: none).
    target, no_kjv, nowhere = {}, {}, []
    for r in refs:
        k = vw_of[r]
        why = _why_no_kjv(r, k)
        es = [e for e in v2e.get(k, []) if not e.endswith("+")
              and e.split(".")[0] not in BVV.KJV_APOCRYPHA]
        if r in HOUSE_ROWS:
            es, words, hwhy = HOUSE_ROWS[r]
            if words is not None and words not in text[r]:
                _stop(f"HOUSE_ROWS {r}: {words!r} is not in Brenton's verse")
            if not es:
                no_kjv[r] = hwhy
                continue
            es = list(es)
        elif b_in_no_kjv(r):
            no_kjv[r] = why
            continue
        elif k in v2e and not es:
            no_kjv[r] = why or ("text the Greek adds, which TVTMS reads as a subverse the "
                                "KJV does not print")
            continue
        elif k not in v2e and why:
            no_kjv[r] = why     # a lettered verse or a prologue TVTMS does not name
            continue
        elif k not in v2e:
            es = [k]            # TVTMS is silent: the same number
        bad = [e for e in es if not e.endswith(".title") and e not in kjv]
        if not es or bad:
            nowhere.append((r, k, es))
            continue
        target[r] = sorted(es, key=osis_key)
    if nowhere and os.environ.get("BRENTON_EXPLORE"):
        print(f"EXPLORE: {len(nowhere)} Brenton verses unplaced: {[n[0] for n in nowhere[:80]]}")
    if nowhere and not os.environ.get("BRENTON_EXPLORE"):
        _stop(f"{len(nowhere)} Brenton verse(s) land on no KJV verse and are in no stated "
              f"exception, first {[n[0] for n in nowhere[:40]]}")
    # Lettered verses that fill a gap in Brenton's numbers. eBible letters
    # some KJV verses whose number Brenton's sequence skips (Gen 31:50a is the
    # KJV's 31:51; Brenton has no 31:51). Where the n letters after verse V
    # stand exactly where n numbers are skipped, the k-th letter is the KJV
    # verse k after V's last target, if no other Brenton verse reaches it and
    # the English of the two agrees.
    reached = {e for es in target.values() for e in es}
    nums = {}
    for r in refs:
        b, c, v = r.rsplit(".", 2)[0], r.rsplit(".", 2)[1], r.rsplit(".", 1)[1]
        m = RE_LABEL.match(v)
        if m:
            nums.setdefault((b, c), []).append((int(m.group(1)), m.group(2), r))
    gap_filled = {}
    for (b, c), vs in nums.items():
        plain = sorted(n for n, l, _ in vs if not l)
        for n in sorted({n for n, l, _ in vs if l}):
            letters = [r for m_, l, r in vs if m_ == n and l]
            after = [p for p in plain if p > n]
            if not after or after[0] - n - 1 != len(letters) or f"{b}.{c}.{n}" not in target:
                continue
            last = target[f"{b}.{c}.{n}"][-1]
            lb, lc, lv = last.rsplit(".", 2)[0], last.split(".")[-2], last.split(".")[-1]
            if not lv.isdigit():
                continue
            cands = [f"{lb}.{lc}.{int(lv) + k}" for k in range(1, len(letters) + 1)]
            if any(r not in no_kjv or r in HOUSE_ROWS for r in letters) or \
                    any(e not in kjv or e in reached for e in cands) or \
                    any(BVV._dice(BVV._etoks(text[r]), _kjv_toks(e)) < 0.3
                        for r, e in zip(letters, cands)):
                continue    # the words must agree too (Jer 10:9a is the KJV's 10:5b, not 10:10)
            for r, e in zip(letters, cands):
                del no_kjv[r]
                target[r] = [e]
                gap_filled[r] = e
                reached.add(e)
    missing = sorted(kjv - reached, key=osis_key)
    unexplained, without = [], {}
    for e in missing:
        if e in KJV_ABSENT:
            without[e] = KJV_ABSENT[e]
        elif e in kjv_absent:
            without[e] = kjv_absent[e]
        elif e in paired_from and not any(k in vw for k in paired_from[e]):
            without[e] = (f"TVTMS's followed column puts it at {', '.join(paired_from[e])}, "
                          f"which Brenton does not print")
        elif e not in vw:
            without[e] = ("Brenton prints no verse of this number and TVTMS does not say "
                          "why; not read verse by verse, so the text may stand in a "
                          "neighbouring verse of his (review found Gen 35:21 in his 35:16 "
                          "and 2 Sam 23:31 in his 23:29)")
        else:
            unexplained.append(e)
    if unexplained and os.environ.get("BRENTON_EXPLORE"):
        print(f"EXPLORE: {len(unexplained)} KJV verses unreached: {unexplained[:80]}")
    if unexplained and not os.environ.get("BRENTON_EXPLORE"):
        _stop(f"{len(unexplained)} KJV verse(s) reached from no Brenton verse, first "
              f"{unexplained[:60]}")
    return {"target": target, "no_kjv": no_kjv, "without": without, "followed": followed,
            "left_alone": left_alone, "tally": tally, "text": text, "refs": refs,
            "view": vw_of, "kjv": kjv, "gap_filled": gap_filled}


def b_in_no_kjv(r):
    """A verse in a book or range the KJV does not hold is never mapped, even
    where TVTMS's English column names an apocryphal verse for it."""
    b, c, v = r.split(".")
    n = RE_LABEL.match(v).group(1)
    return b in NOT_IN_KJV_BOOKS or any(
        b == book and int(c) == ch and lo <= int(n) <= hi for book, ch, lo, hi, _ in NOT_IN_KJV_RANGES)


def _runs(refs):
    """Consecutive verses of one chapter as 'Book.ch.a-b' runs (Brenton's
    order: a lettered verse continues a run from its verse)."""
    out, cur = [], None
    for r in refs:
        b, ch, v = r.split(".")
        if cur and cur[0] == (b, ch) and cur[3] is not None and r == cur[3]:
            cur[2] = v
        else:
            if cur:
                out.append(cur)
            cur = [(b, ch), v, v, None]
        cur[3] = _next.get(r)
    if cur:
        out.append(cur)
    return [f"{b}.{ch}.{a}" + (f"-{z}" if z != a else "") for (b, ch), a, z, _n in out]


_next = {}


def _compact(labels):
    """Brenton's verse labels of one chapter, in order, as '1-24,24a-24i,24k-24z,25-38'.
    A lettered run holds every letter between its ends (Brenton skips some
    letters, j and v most often, so a skipped letter breaks the run)."""
    out, run = [], None
    for v in labels:
        n, letter = RE_LABEL.match(v).groups()
        if run and not letter and not run[2] and n.isdigit() and int(n) == int(run[1]) + 1:
            run[1] = n
        elif run and letter and run[2] and run[3] == n and ord(letter) == ord(run[2]) + 1:
            run[1], run[2] = v, letter
        else:
            if run:
                out.append(run)
            run = [v, v, letter, n]
    if run:
        out.append(run)
    return ",".join(a if a == z else f"{a}-{z}" for a, z, _l, _n in out)


def build():
    r = compute()
    refs, target = r["refs"], r["target"]
    _next.clear()
    _next.update({a: b for a, b in zip(refs, refs[1:])})
    diff = {}
    for v in refs:
        if v in target:
            es = target[v]
            if es != [v]:
                diff[v] = es[0] if len(es) == 1 else es
    by_why = {}
    for v in refs:
        if v in r["no_kjv"]:
            by_why.setdefault(r["no_kjv"][v], []).append(v)
    whole = {why: b for b, why in NOT_IN_KJV_BOOKS.items()}
    no_kjv = [{"verses": [f"{whole[why]} (the whole book)"] if why in whole else _runs(vs),
               "count": len(vs), "why": why} for why, vs in by_why.items()]
    chapters = {}
    for v in refs:
        b, c, x = v.split(".")
        chapters.setdefault(f"{b}.{c}", []).append(x)
    unusual = {t: f for t, f in r["followed"].items() if f["how"] != "tests" or _rank(f["column"]) > 1}
    many = {}
    for v, es in target.items():
        for e in es:
            many.setdefault(e, []).append(v)
    return {
        "note": ("Brenton's English Septuagint -> KJV verse numbers. Only the Brenton verses "
                 "whose KJV reference differs are in `map`; any other Brenton verse not named in "
                 "`no_kjv_verse` has the same reference in the KJV. Brenton's Nehemiah is "
                 "Ezra 11-23 (the Greek's 2 Esdras), and his lettered verses (1Kgs.12.24a) are "
                 "the Greek's additions. A list value is one Brenton verse holding text of "
                 "several KJV verses; several Brenton verses may share one KJV verse. A "
                 "'.title' target is the KJV's unnumbered psalm superscription. "
                 "`brenton_verses` lists Brenton's verses per chapter. Built by "
                 "pipeline/build_brenton_versification.py; do not hand-edit."),
        "from": "brenton", "to": "kjv",
        "source": {
            "name": "TVTMS - Translators Versification Traditions with Methodology for "
                    "Standardisation (STEPBible.org)",
            "url": "https://github.com/STEPBible/STEPBible-Data",
            "commit": BV.TVTMS_COMMIT, "sha256": BV.TVTMS_SHA256,
            "columns_read": ["English KJV", "the column whose tests Brenton passes, block by "
                             "block (usually a Greek one); see blocks_not_greek"],
            "changes": ("Reformatted: only the condensed section is read, for the 39 books of "
                        "the KJV's Old Testament; in each block one column is followed, chosen "
                        "by running TVTMS's own tests on Brenton; subverses are read as "
                        "Brenton's lettered verses; rows where the two agree are dropped; book "
                        "codes become OSIS; ranges are expanded to single verses. house_rows "
                        "adds the correspondences TVTMS does not have; nothing of TVTMS's is "
                        "altered."),
        },
        "rights": {
            "license": "CC BY 4.0",
            "attribution": ("Data created by www.STEPBible.org based on work at Tyndale "
                            "House Cambridge (CC BY 4.0)"),
            "source_url": "https://github.com/STEPBible/STEPBible-Data",
            "redistribute_whole": False,
        },
        "checked_against": {
            "name": "Brenton's English Septuagint (PD), eBible.org's USFM, as "
                    "fetch_sources.BRENTON pins it",
            "url": f"https://github.com/{FS.BRENTON['repo']}", "commit": FS.BRENTON["commit"],
            "sha256": FS.BRENTON["sha256"],
            "brenton_verses": len(refs), "kjv_verses": len(r["kjv"]),
            "brenton_verses_landing_on_no_kjv_verse_unexplained": 0,
            "kjv_verses_reached_from_no_brenton_verse": len(r["without"]),
            "tvtms_blocks_followed": len(r["followed"]),
            "tvtms_tests_brenton_cannot_answer": r["tally"]["undecidable"],
        },
        "counts": {"differing_brenton_verses": len(diff),
                   "to_psalm_titles": sum(1 for es in target.values() for e in es
                                          if e.endswith(".title")),
                   "spanning_several_kjv_verses": sum(isinstance(x, list) for x in diff.values()),
                   "kjv_verses_shared_by_several_brenton_verses":
                       sum(len(vs) > 1 for vs in many.values()),
                   "brenton_verses_with_no_kjv_verse": len(r["no_kjv"]),
                   "house_rows": len(HOUSE_ROWS)},
        "blocks_not_greek": unusual,
        "house_rows": {v: {"kjv": es, "why": why} for v, (es, _w, why) in HOUSE_ROWS.items()},
        "lettered_gap_fills": {
            "why": ("a lettered verse standing where Brenton's numbers skip as many verses "
                    "as it has letters: eBible letters a KJV verse whose number Brenton's "
                    "sequence lacks (Gen.31.50a is the KJV's 31:51)"),
            "verses": {v: r["gap_filled"][v] for v in refs if v in r["gap_filled"]}},
        "brenton_verses": {c: _compact(vs) for c, vs in chapters.items()},
        "no_kjv_verse": no_kjv,
        "kjv_without_brenton_verse": r["without"],
        "map": diff,
    }


# ---------------------------------------------------------------- audit

def audit(show=120, r=None):
    """Brenton's English against the KJV's: a monotonic alignment (1-1, 1-2,
    2-1, 2-2, 1-3, 3-1 and gaps; Dice overlap of content-word stems) of each
    run of Brenton verses whose map targets move forward, against the KJV
    verses around them. A verse whose aligned KJV verses share nothing with
    the map's is listed for reading. Not a gate: the Greek and the Hebrew
    differ, and loose stretches make honest noise."""
    r = r or compute()
    kj = {}
    with open(KJV_TSV, encoding="utf-8") as f:
        for line in f:
            i, _, t = line.rstrip("\n").partition("\t")
            if i.startswith("kjv:"):
                kj[i[4:]] = t
    kord = list(kj)
    kidx = {k: i for i, k in enumerate(kord)}
    KT = [BVV._etoks(kj[k]) for k in kord]
    units = [(v, [e for e in r["target"][v] if e in kidx]) for v in r["refs"] if v in r["target"]]
    units = [(v, es) for v, es in units if es]
    # runs whose first target moves forward (a reordered book, Jeremiah, breaks into runs)
    segs, cur = [], []
    for v, es in units:
        g = kidx[es[0]]
        if cur and (v.split(".")[0] != cur[-1][0].split(".")[0] or g < kidx[cur[-1][1][0]] - 3
                    or g > kidx[cur[-1][1][0]] + 12):
            segs.append(cur)
            cur = []
        cur.append((v, es))
    if cur:
        segs.append(cur)
    flagged, aligned, unaligned = [], {}, 0
    for seg in segs:
        books = {e.split(".")[0] for _v, es in seg for e in es}
        lo = max(0, kidx[seg[0][1][0]] - 10)
        hi = min(len(kord), max(kidx[es[-1]] for _v, es in seg) + 11)
        while kord[lo].split(".")[0] not in books:
            lo += 1
        while kord[hi - 1].split(".")[0] not in books:
            hi -= 1
        M, n = hi - lo, len(seg)
        DT = [BVV._etoks(r["text"][v]) for v, _ in seg]
        guess = [kidx[es[0]] - lo for _v, es in seg]
        # the alignment may start anywhere near the first guess, and end anywhere
        best = {(0, j): (0.0, None) for j in range(0, min(M, guess[0] + 10) + 1)}
        for i in range(n + 1):
            c = guess[min(i, n - 1)]
            for j in range(max(0, c - 10), min(M, c + 10) + 1):
                if (i, j) not in best:
                    continue
                sc = best[(i, j)][0]
                for a, b, pen in BVV._BEADS:
                    ni, nj = i + a, j + b
                    if ni > n or nj > M:
                        continue
                    A = set().union(*DT[i:ni]) if a else set()
                    B_ = set().union(*KT[lo + j:lo + nj]) if b else set()
                    s2 = sc + (BVV._dice(A, B_) if a and b else 0) - pen
                    if (ni, nj) not in best or best[(ni, nj)][0] < s2:
                        best[(ni, nj)] = (s2, (i, j))
        ends = [k for k in best if k[0] == n]
        if not ends:
            unaligned += n
            continue
        end = max(ends, key=lambda k: best[k][0])
        al = {}
        while best[end][1]:
            pi, pj = best[end][1]
            for x in range(pi, end[0]):
                al[x] = [kord[lo + y] for y in range(pj, end[1])]
            end = (pi, pj)
        for x, (v, es) in enumerate(seg):
            aligned[v] = al.get(x, [])
            if al.get(x) and not set(es) & set(al[x]):
                flagged.append((v, es, al[x]))
    # The verses said to have NO KJV verse (lettered additions, prologues):
    # does one read like a KJV verse near where its neighbours land?
    nearest, last = {}, None
    for v in r["refs"]:
        if v in r["target"] and r["target"][v][0] in kidx:
            last = kidx[r["target"][v][0]]
        elif v in r["no_kjv"] and last is not None and not b_in_no_kjv(v):
            T = BVV._etoks(r["text"][v])
            got = max(((BVV._dice(T, KT[j]), kord[j]) for j in range(max(0, last - 30),
                                                                     min(len(kord), last + 31))),
                      default=(0, None))
            if got[0] >= 0.5:
                nearest[v] = got
    chapters = {}
    for f in flagged:
        chapters.setdefault(f[0].rsplit(".", 1)[0], []).append(f)
    print(f"Brenton verses said to have no KJV verse that read like one nearby (Dice >= 0.5): "
          f"{len(nearest)}")
    for v, (d, k) in nearest.items():
        print(f"  {v} ~ {k} ({d:.2f})")
    print(f"Brenton verses aligned to the KJV by their English: {len(units) - unaligned:,} "
          f"(not aligned: {unaligned})")
    print(f"  where the alignment shares no KJV verse with the map: {len(flagged)} verses "
          f"in {len(chapters)} chapters")
    for c, fs in sorted(chapters.items(), key=lambda kv: -len(kv[1]))[:show]:
        print(f"  {c} ({len(fs)}): " + "; ".join(f"{v} map {m} / English {e}" for v, m, e in fs[:3]))
    return flagged, aligned


def render(doc):
    return (json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--audit", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
        return
    if a.audit:
        audit()
        return
    blob = render(build())
    if os.environ.get("BRENTON_EXPLORE"):
        _stop("BRENTON_EXPLORE is set: the invariants are not enforced, so nothing is "
              "written or checked")
    rel = os.path.relpath(OUT, ROOT)
    if a.check:
        if not os.path.exists(OUT):
            _stop(f"{rel} missing")
        if open(OUT, "rb").read() != blob:
            _stop(f"{rel} differs from a rebuild")
        print(f"OK: {rel} byte-identical; every invariant holds")
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT + ".tmp", "wb") as f:
        f.write(blob)
    os.replace(OUT + ".tmp", OUT)
    print(f"wrote {rel}: {json.loads(blob)['counts']}")


if __name__ == "__main__":
    main()
