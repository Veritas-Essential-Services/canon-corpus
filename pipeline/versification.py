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
"""
import json
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "data", "versification", "bhs-kjv.json")


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
