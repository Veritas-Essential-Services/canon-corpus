# prov: 2026-10-02 drafted (Claude Code)
# fable_review: pending
"""
versification.py -- read data/versification/bhs-kjv.json (built by
build_versification.py) and turn a Hebrew-numbered OT reference into the
KJV reference(s) it names.

    m = load()
    targets("Ps.51.3", m)   -> ["Ps.51.1"]
    targets("Ps.51.1", m)   -> ["Ps.51.title"]     (the KJV's unnumbered superscription)
    targets("Isa.63.19", m) -> ["Isa.63.19", "Isa.64.1"]
    targets("Gen.1.1", m)   -> ["Gen.1.1"]         (not in the map: same number)

The Clementine Vulgate's map (data/versification/vulgate-kjv.json, built by
build_vulgate_versification.py) reads the same way:

    v = load(VULGATE_PATH)
    targets("Ps.50.3", v)   -> ["Ps.51.1"]
    resolve_vulgate("Jonah.2.1", v, kjv_ids) -> {"resolved": True, "target": "kjv:Jonah.1.17"}

So does Brenton's English Septuagint's (data/versification/brenton-kjv.json,
built by build_brenton_versification.py), whose verse labels may be lettered
('1Kgs.12.24a', the Greek's additions) and whose Nehemiah is Ezra 11-23:

    g = load(BRENTON_PATH)
    resolve_brenton("Ps.50.3", g, kjv_ids)   -> {"resolved": True, "target": "kjv:Ps.51.1"}
    resolve_brenton("Ezra.11.1", g, kjv_ids) -> {"resolved": True, "target": "kjv:Neh.1.1"}

And the historic English Bibles' (data/versification/<slug>-kjv.json):

    e = load(english_path("geneva"))
    resolve_english("Num.13.1", e, kjv_ids) -> {"resolved": True, "target": "kjv:Num.12.16"}

The deuterocanon has its own key, the KJV's Apocrypha verse (kjva:), one map
for every witness (data/versification/deuterocanon.json, built by
build_deuterocanon.py):

    d = load(DC_PATH)
    resolve_dc("Sir.33.12", "brenton", d) -> {"resolved": True, "target": "kjva:Sir.30.25"}
    resolve_dc("Gen.1.1", "brenton", d)   -> None   (not a deuterocanonical verse)
"""
import json
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "data", "versification", "bhs-kjv.json")
VULGATE_PATH = os.path.join(os.path.dirname(PATH), "vulgate-kjv.json")
BRENTON_PATH = os.path.join(os.path.dirname(PATH), "brenton-kjv.json")
DC_PATH = os.path.join(os.path.dirname(PATH), "deuterocanon.json")


def english_path(slug):
    """The map of one of the historic English Bibles (build_english_versification.py)."""
    return os.path.join(os.path.dirname(PATH), f"{slug}-kjv.json")


BOOKS = {"Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam", "2Sam",
         "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov",
         "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos",
         "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal"}


def load(path=PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def targets(osis, m):
    """KJV reference(s) for Hebrew reference `osis` ('Book.ch.v')."""
    v = m["map"].get(osis, osis)
    return [v] if isinstance(v, str) else list(v)


def resolve(osis, m, kjv_ids):
    """Fields to merge into a scripture link stated in Hebrew numbering.
    `kjv_ids` is the set of existing kjv: unit ids ('kjv:Ps.51.1'). A link is
    resolved only when every KJV verse it lands on has a unit id; otherwise
    it stays unresolved and says why, so nothing points at a verse that is
    not there."""
    b, ch, v = osis.split(".")
    if b not in BOOKS:
        return {"resolved": False, "why": "not an Old Testament reference; the map is OT only"}
    if not 1 <= int(v) <= m["hebrew_chapters"].get(f"{b}.{ch}", 0):
        return {"resolved": False, "why": "no such verse in the Hebrew Bible (WLC)"}
    ts = targets(osis, m)
    ids = [f"kjv:{t}" for t in ts]
    if any(t.endswith(".title") for t in ts):
        return {"resolved": False, "kjv": ts,
                "why": "psalm title: the KJV prints it before v.1, with no verse number"}
    if not all(i in kjv_ids for i in ids):
        return {"resolved": False, "why": "no such verse in the KJV"}  # unreachable while --check holds
    out = {"resolved": True, "target": ids[0]}
    if len(ids) > 1:
        out["spans"] = ids
    return out


def _no_kjv(osis, m):
    """Why Clementine verse `osis` has no KJV verse, or None."""
    b, ch, v = osis.split(".")
    for row in m["no_kjv_verse"]:
        for run in row["verses"]:
            if run.endswith(" (the whole book)"):
                if run == f"{b} (the whole book)":
                    return row["why"]
                continue
            rb, rch, rv = run.split(".")
            lo, _, hi = rv.partition("-")
            if (rb, rch) == (b, ch) and int(lo) <= int(v) <= int(hi or lo):
                return row["why"]
    return None


def resolve_vulgate(osis, m, kjv_ids):
    """What a verse in the Clementine's numbering ('Ps.50.3') names in the
    KJV, as fields for a unit or a link. Resolved only when every KJV verse it
    lands on has a unit id. A verse holding a psalm title and verse 1 is
    resolved to verse 1, and its `spans` keep the title as a bare 'Ps.13.title'
    (no kjv: prefix: a KJV title is no unit). The Hebrew `resolve` marks the
    same case unresolved, since a BDB citation of it means the title."""
    b, ch, v = osis.split(".")
    if not 1 <= int(v) <= m["vulgate_chapters"].get(f"{b}.{ch}", 0):
        return {"resolved": False, "why": "no such verse in the Clementine Vulgate"}
    why = _no_kjv(osis, m)
    if why:
        return {"resolved": False, "why": why}
    ts = targets(osis, m)
    ids = [f"kjv:{t}" for t in ts if not t.endswith(".title")]
    if not ids:
        return {"resolved": False, "kjv": ts,
                "why": "psalm title: the KJV prints it before v.1, with no verse number"}
    if not all(i in kjv_ids for i in ids):
        return {"resolved": False, "why": "no such verse in the KJV"}  # unreachable while --check holds
    out = {"resolved": True, "target": ids[0]}
    if len(ts) > 1:
        out["spans"] = [f"kjv:{t}" if not t.endswith(".title") else t for t in ts]
    return out


def brenton_labels(chapter, m):
    """Brenton's verse labels of one chapter ('1Kgs.12'), in his order, from
    the map's compact `brenton_verses` ('1-24,24a-24i,24k-24z,25-33')."""
    out = []
    for run in m["brenton_verses"].get(chapter, "").split(","):
        if not run:
            continue
        a, _, z = run.partition("-")
        z = z or a
        if a.isdigit():
            out += [str(i) for i in range(int(a), int(z) + 1)]
        else:
            out += [a[:-1] + chr(c) for c in range(ord(a[-1]), ord(z[-1]) + 1)]
    return out


def _no_kjv_brenton(osis, m):
    """Why Brenton verse `osis` has no KJV verse, or None. A run
    ('1Kgs.12.24o-24z') is in Brenton's order, so it is read by position."""
    b, ch, v = osis.split(".")
    labels = brenton_labels(f"{b}.{ch}", m)
    for row in m["no_kjv_verse"]:
        for run in row["verses"]:
            if run.endswith(" (the whole book)"):
                if run == f"{b} (the whole book)":
                    return row["why"]
                continue
            rb, rch, rv = run.split(".")
            if (rb, rch) != (b, ch):
                continue
            lo, _, hi = rv.partition("-")
            if labels.index(lo) <= labels.index(v) <= labels.index(hi or lo):
                return row["why"]
    return None


def resolve_brenton(osis, m, kjv_ids):
    """What a verse in Brenton's numbering ('Ps.50.3', '1Kgs.12.24a',
    'Ezra.11.1') names in the KJV, as fields for a unit or a link. Resolved
    only when every KJV verse it lands on has a unit id. `spans` keeps a psalm
    title bare, as resolve_vulgate does."""
    b, ch, v = osis.split(".")
    if v not in brenton_labels(f"{b}.{ch}", m):
        return {"resolved": False, "why": "no such verse in Brenton's Septuagint"}
    why = _no_kjv_brenton(osis, m)
    if why:
        return {"resolved": False, "why": why}
    ts = targets(osis, m)
    ids = [f"kjv:{t}" for t in ts if not t.endswith(".title")]
    if not ids:
        return {"resolved": False, "kjv": ts,
                "why": "psalm title: the KJV prints it before v.1, with no verse number"}
    if not all(i in kjv_ids for i in ids):
        return {"resolved": False, "why": "no such verse in the KJV"}  # unreachable while --check holds
    out = {"resolved": True, "target": ids[0]}
    if len(ts) > 1:
        out["spans"] = [f"kjv:{t}" if not t.endswith(".title") else t for t in ts]
    return out


def resolve_english(osis, m, kjv_ids):
    """What a verse in one historic English Bible's numbering names in the
    KJV, by that Bible's map. Resolved only when every KJV verse it lands on
    has a unit id."""
    b, ch, v = osis.split(".")
    have = m["chapters"].get(f"{b}.{ch}", 0)
    if not v.isdigit():
        return {"resolved": False, "why": f"no such verse in {m['source']['name']}"}
    if not (int(v) <= have if isinstance(have, int) else v in have.split(",")) or int(v) < 1:
        return {"resolved": False, "why": f"no such verse in {m['source']['name']}"}
    for row in m["no_kjv_verse"]:
        for run in row["verses"]:
            rb, rch, rv = run.split(".")
            lo, _, hi = rv.partition("-")
            if (rb, rch) == (b, ch) and int(lo) <= int(v) <= int(hi or lo):
                return {"resolved": False, "why": row["why"]}
    ts = targets(osis, m)
    ids = [f"kjv:{t}" for t in ts]
    if not all(i in kjv_ids for i in ids):
        return {"resolved": False, "why": "no such verse in the KJV"}  # unreachable while --check holds
    out = {"resolved": True, "target": ids[0]}
    if len(ids) > 1:
        out["spans"] = ids
    return out



_DC_RUNS = {}


def _in_runs(osis, runs):
    """Is `osis` in a list of runs ('Sir.1.1-30', 'Esth.1.1a')?"""
    b, ch, v = osis.split(".")
    for run in runs:
        rb, rch, rv = run.split(".")
        if (rb, rch) != (b, ch):
            continue
        lo, _, hi = rv.partition("-")
        if rv == v or (lo.isdigit() and v.isdigit() and int(lo) <= int(v) <= int(hi or lo)):
            return True
    return False


def resolve_dc(osis, witness, m):
    """The shared deuterocanon key(s) of a verse in `witness`'s own numbering
    ('vulgate', 'douay', 'brenton'): {"resolved": True, "target": "kjva:...",
    "spans": [...]} or {"resolved": False, "why": ...}; None for a verse the
    map does not cover (the protocanonical books, keyed to the KJV instead)."""
    w = m["witnesses"][witness]
    if not _in_runs(osis, w["verses"]):
        return None
    if osis in w["map"]:
        ks = w["map"][osis]
        ks = [ks] if isinstance(ks, str) else ks
    else:
        for row in w["no_key"]:
            if _in_runs(osis, row["verses"]):
                return {"resolved": False, "why": row["why"]}
        b, ch, v = osis.split(".")
        ks = [f"kjva:{'Bar' if b == 'EpJer' else b}.{'6' if b == 'EpJer' else ch}.{v}"]
    out = {"resolved": True, "target": ks[0]}
    if len(ks) > 1:
        out["spans"] = ks
    if _in_runs(osis, w.get("weak", [])):
        out["weak"] = True
    return out
