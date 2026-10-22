#!/usr/bin/env python3
# prov: 2026-10-03 claude-opus-5-5 drafted
# fable_review: pending
"""No committed JSON file repeats a key in the same object.

json.load keeps the LAST of two equal keys and says nothing, so a manifest
with a catalogue id written twice loads, builds and passes every other test.
That is how a textual git merge of two branches that both added
josephus-life-whiston left data/books/manifest.json holding it twice
(merge rehearsal, 2026-10-03, docs/MERGE-REHEARSAL.md problem 1): no conflict
was reported, and one of the two entries was silently thrown away on load.
This test reads every committed .json with a hook that sees every key."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
fails = passes = 0
def ok(c, m):
    global fails, passes
    print(("ok    " if c else "FAIL  ") + m)
    if c: passes += 1
    else: fails += 1


def duplicates(text):
    """Every key repeated within one object, in document order."""
    found = []
    def hook(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                found.append(k)
            seen.add(k)
        return dict(pairs)
    json.loads(text, object_pairs_hook=hook)
    return found


def committed_json():
    """The .json files git tracks; a plain walk when there is no git."""
    try:
        out = subprocess.check_output(["git", "-C", ROOT, "ls-files", "-z", "*.json"],
                                      stderr=subprocess.DEVNULL)
        return [p for p in out.decode("utf-8").split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        paths = []
        for d, dirs, files in os.walk(ROOT):
            dirs[:] = [x for x in dirs if x not in (".git", "corpus", "build")]
            paths += [os.path.relpath(os.path.join(d, f), ROOT) for f in files if f.endswith(".json")]
        return sorted(paths)


print("--- the checker itself")
ok(duplicates('{"a": 1, "b": 2}') == [], "a clean object has no duplicates")
ok(duplicates('{"josephus-life-whiston": {"format": "tei"}, "x": 0, '
              '"josephus-life-whiston": {"format": "tei-perseus"}}') == ["josephus-life-whiston"],
   "a top-level id written twice is caught (the 2026-10-03 case)")
ok(duplicates('{"book": {"scheme": {"note": "a", "note": "b"}}}') == ["note"],
   "a key repeated deep inside an entry is caught")
ok(duplicates('[{"id": 1}, {"id": 2}]') == [], "the same key in two different objects is fine")

print("--- the committed files")
paths = committed_json()
ok(len(paths) > 0, f"{len(paths)} committed .json files found")
bad = 0
for rel in paths:
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        continue
    with open(p, encoding="utf-8") as f:
        text = f.read()
    try:
        d = duplicates(text)
    except json.JSONDecodeError as e:
        ok(False, f"{rel}: not valid JSON ({e})")
        bad += 1
        continue
    if d:
        shown = ", ".join(sorted(set(d))[:5])
        ok(False, f"{rel}: {len(d)} repeated key(s): {shown}")
        bad += 1
ok(bad == 0, "no committed .json repeats a key in the same object")

print(f"\n{passes} passed, {fails} failed")
sys.exit(1 if fails else 0)
