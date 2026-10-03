#!/usr/bin/env python3
"""Offline checks for pipeline/split_shelf_titles.py (lane C's title cutter).
No network, no corpus: each check runs the real script on a throwaway copy
of the repo layout in a temp directory. Run:
    python3 tests/split_shelf_titles_test.py

The one that matters most: a title that fails after an earlier good cut
must not leave the old titles/<slug>.txt behind (coordinator review,
2026-10-03), because a stale file on disk reads as a good title."""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "pipeline", "split_shelf_titles.py")

PASS = 0
FAIL = []
def check(label, cond):
    global PASS
    if cond: PASS += 1
    else: FAIL.append(label)

BODY = ("*** START OF THE PROJECT GUTENBERG EBOOK TEST ***\n"
        "FIRST POEM\n" + "a line of the first poem\n" * 40 +
        "SECOND POEM\n" + "a line of the second poem\n" * 40 +
        "*** END OF THE PROJECT GUTENBERG EBOOK TEST ***\nlicence text\n")

def setup(titles):
    root = tempfile.mkdtemp()
    os.makedirs(os.path.join(root, "pipeline"))
    shutil.copy(SCRIPT, os.path.join(root, "pipeline"))
    src = os.path.join(root, "data", "corpus", "t")
    os.makedirs(src)
    open(os.path.join(src, "vol.txt"), "w").write(BODY)
    write_shelf(root, titles)
    return root

def write_shelf(root, titles):
    json.dump({"titles": titles}, open(os.path.join(root, "pipeline", "t_shelf.json"), "w"))

def run(root):
    r = subprocess.run([sys.executable, os.path.join(root, "pipeline", "split_shelf_titles.py"), "t"],
                       capture_output=True, text=True)
    out = os.path.join(root, "data", "corpus", "t", "titles")
    rep = json.load(open(os.path.join(out, "titles_report.json")))
    return r.returncode, out, rep

GOOD = {"source": "vol", "start": ["FIRST POEM", 1], "end": ["SECOND POEM", 1]}

root = setup({"t-first": GOOD})
code, out, rep = run(root)
cut = os.path.join(out, "t-first.txt")
check("a good title is cut and exits 0", code == 0 and os.path.exists(cut))
check("the cut stops before the end marker", "second poem" not in open(cut).read())
check("the Gutenberg licence is never part of a cut", "licence" not in open(cut).read())

write_shelf(root, {"t-first": {**GOOD, "end": ["NO SUCH HEADING", 1]}})
code, out, rep = run(root)
check("a failed marker exits 1", code == 1)
check("a failed marker deletes the earlier cut", not os.path.exists(cut))
check("the report says the stale cut was removed",
      rep["t-first"]["status"] == "MARKER-FAILED" and rep["t-first"].get("stale_removed"))

write_shelf(root, {"t-first": GOOD})
run(root)
write_shelf(root, {"t-first": {**GOOD, "source": "missing-volume"}})
code, out, rep = run(root)
check("a missing source deletes the earlier cut", code == 1 and not os.path.exists(cut))

write_shelf(root, {"t-first": GOOD})
run(root)
write_shelf(root, {"t-first": {**GOOD, "start": ["SECOND POEM", 1], "end": None,
                               "source": "vol"}})
open(os.path.join(root, "data", "corpus", "t", "vol.txt"), "w").write(
    BODY.replace("a line of the second poem\n" * 40, "short\n"))
code, out, rep = run(root)
check("a too-short cut deletes the earlier cut", code == 1 and not os.path.exists(cut))

write_shelf(root, {"t-first": {"of": "X", "held_in": {"file": "pipeline/adler_shelf.json", "slug": "x"}}})
open(cut, "w").write("left over from an earlier run\n")
code, out, rep = run(root)
check("a title held elsewhere exits 0 and leaves no file of its own",
      code == 0 and not os.path.exists(cut) and rep["t-first"]["status"] == "held-elsewhere")
check("no temp file is left behind", not any(f.endswith(".tmp") for f in os.listdir(out)))
shutil.rmtree(root)

print(f"\n{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
