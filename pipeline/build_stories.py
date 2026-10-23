#!/usr/bin/env python3
# prov: 2026-10-23 claude-opus-5-5 drafted
# fable_review: pending
"""build_stories.py -- the story layer of the Illustrated Classics.

    python3 pipeline/build_stories.py            # give every story, figure and scene its uid; validate
    python3 pipeline/build_stories.py --check    # mint 0, files byte-identical

Adam, 2026-10-23: tag a picture to the STORY, SCENE and FIGURES it shows,
never to one book, so the same Minotaur serves Bulfinch, Hawthorne and Ovid.
So a story lives here, apart from any edition:

    data/stories/<story>/story.json     settings, and each telling's chapter table
    data/stories/<story>/figures.jsonl  who appears; `looks` = what the text says
                                        they look like, in the house's words, cited
    data/stories/<story>/scenes.jsonl   what happens, in the house's words, pinned
                                        to a paragraph of a telling

The jsonl files are the source: edit them by hand, then run this script, which
adds the uid to any row that lacks one and checks every reference. No book text
is stored -- titles and looks are paraphrase, anchors are unit ids and counts.

Citations (the mutable layer, pipeline/wh_uid.py): `story-<id>:story`,
`story-<id>:figure.<figure>`, `story-<id>:scene.<scene>`. Renaming a scene id
mints a new uid, so don't; change its title instead.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import wh_uid as U  # noqa: E402

UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")
STORIES = os.path.join(ROOT, "data", "stories")
BOOKS = os.path.join(ROOT, "data", "books")


def read_jsonl(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def dump_jsonl(rows):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def with_uid(row, uid):
    return {"uid": uid, **{k: v for k, v in row.items() if k != "uid"}}


def validate(sid, story, figures, scenes, problems):
    def bad(msg):
        problems.append(f"{sid}: {msg}")
    tellings = {t["id"]: t for t in story.get("tellings", [])}
    fids = [f["id"] for f in figures]
    if len(set(fids)) != len(fids):
        bad("duplicate figure id")
    scids = [s["id"] for s in scenes]
    if len(set(scids)) != len(scids):
        bad("duplicate scene id")
    known_units = {}
    for t in tellings.values():
        p = os.path.join(BOOKS, f"{t.get('book')}.json")
        if os.path.exists(p):   # gitignored build; checked when present
            known_units[t["id"]] = {u["id"] for u in json.load(open(p, encoding="utf-8"))["units"]}

    def anchor(where, tid, ch, para, at):
        t = tellings.get(tid)
        if not t:
            return bad(f"{where}: no telling {tid!r}")
        chs = {c["n"]: c for c in t["chapters"]}
        if ch not in chs or not 1 <= para <= chs[ch]["paras"]:
            bad(f"{where}: chapter {ch} para {para} is outside {tid}")
        if not at.startswith(t["book"] + ":"):
            bad(f"{where}: {at!r} is not a unit of {t['book']}")
        if tid in known_units and at not in known_units[tid]:
            bad(f"{where}: {at!r} is not in data/books/{t['book']}.json")
    first = next(iter(tellings), None)
    for f in figures:
        for lk in f.get("looks", []):
            anchor(f"figure {f['id']}", lk.get("telling", first), lk["chapter"], lk["para"], lk["at"])
    order = []
    for s in scenes:
        anchor(f"scene {s['id']}", s["telling"], s["chapter"], s["para"], s["at"])
        for fid in s["figures"]:
            if fid not in fids:
                bad(f"scene {s['id']}: unknown figure {fid!r}")
        if s["setting"] not in story.get("settings", {}):
            bad(f"scene {s['id']}: unknown setting {s['setting']!r}")
        if s["telling"] == first:
            order.append((s["chapter"], s["para"]))
    if order != sorted(order):
        bad("scenes are not in story order")


def build(check=False):
    reg = U.WhUidRegistry(UIDS)
    problems, changed = [], []
    for sid in sorted(os.listdir(STORIES)):
        d = os.path.join(STORIES, sid)
        if not os.path.isfile(os.path.join(d, "story.json")):
            continue
        sp, fp, cp = (os.path.join(d, n) for n in ("story.json", "figures.jsonl", "scenes.jsonl"))
        story = json.load(open(sp, encoding="utf-8"))
        figures, scenes = read_jsonl(fp), read_jsonl(cp)
        if story.get("id") != sid:
            problems.append(f"{sid}: story.json id is {story.get('id')!r}")
        validate(sid, story, figures, scenes, problems)
        cite = f"story-{sid}"
        story = with_uid(story, reg.uid_for(f"{cite}:story"))
        figures = [with_uid(f, reg.uid_for(f"{cite}:figure.{f['id']}")) for f in figures]
        scenes = [with_uid(s, reg.uid_for(f"{cite}:scene.{s['id']}")) for s in scenes]
        for path, text in ((sp, json.dumps(story, ensure_ascii=False, indent=1) + "\n"),
                           (fp, dump_jsonl(figures)), (cp, dump_jsonl(scenes))):
            if open(path, encoding="utf-8").read() != text:
                changed.append(os.path.relpath(path, ROOT))
                if not check:
                    tmp = path + ".tmp"
                    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                        f.write(text)
                    os.replace(tmp, path)
        print(f"{sid}: {len(figures)} figures, {len(scenes)} scenes")
    if problems:
        print("\n".join("PROBLEM " + p for p in problems))
        sys.exit(1)
    if check:
        reg.assert_no_mint()
        if changed:
            sys.exit("CHECK FAILED: would rewrite " + ", ".join(changed))
        print("check: mint 0, byte-identical")
    else:
        reg.save()
        print(f"minted {reg.minted}; rewrote {len(changed)} file(s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    build(ap.parse_args().check)
