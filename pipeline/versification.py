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
"""
import json
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "data", "versification", "bhs-kjv.json")
VULGATE_PATH = os.path.join(os.path.dirname(PATH), "vulgate-kjv.json")


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
    lands on has a unit id."""
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
