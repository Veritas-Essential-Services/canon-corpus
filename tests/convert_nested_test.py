"""Offline checks for pipeline/convert_nested.py (Lane D's nested-heading converter).

    python3 tests/convert_nested_test.py

Each case writes a tiny Gutenberg-shaped text to a temp file, converts it, and
checks the ids and refs. No corpus needed.
"""
import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
from convert_nested import convert_nested

PG = "*** START OF THE PROJECT GUTENBERG EBOOK TEST ***\n\n{}\n\n*** END OF THE PROJECT GUTENBERG EBOOK TEST ***\n"
passed = failed = 0

def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print("FAIL", name, detail)

def convert(body, levels, start=None, front=False):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(PG.format(body))
    try:
        return convert_nested(f.name, "t", "T", "A", levels, start, front)["units"]
    finally:
        os.unlink(f.name)

# 1. A Contents whose last line is a title_next heading, then the body start.
#    The start must forget the title the Contents was waiting for: before the
#    fix the first body heading was folded into it and cited "None BOOK ONE".
body = "CONTENTS\n\nBOOK ONE\n\nThe Beginning\n\nBOOK TWO\n\n" \
       "BOOK ONE.\n\nThe Beginning\n\nIt was a dark night.\n\n" \
       "BOOK TWO.\n\nThe End\n\nAnd so it ended."
lv = [{"re": "BOOK [A-Z]+\\.?$", "title_next": True}]
for front in (False, True):
    u = convert(body, lv, start="BOOK ONE\\.$", front=front)
    refs = [x["ref"] for x in u]
    check(f"start resets a pending title (front={front}): no None",
          not any("None" in x["id"] or "None" in x["ref"] for x in u), refs)
    check(f"start resets a pending title (front={front}): first body unit",
          "BOOK ONE The Beginning, par. 1" in refs, refs)
    check(f"start resets a pending title (front={front}): second heading",
          "BOOK TWO The End, par. 1" in refs, refs)

# 2. title_next folds the next short paragraph, and only a short one.
u = convert("CHAPTER I\n\nThe Aesir\n\nIn the beginning.\n\nCHAPTER II\n\n" + "x" * 120,
            [{"re": "CHAPTER [IVX]+$", "title_next": True}])
refs = [x["ref"] for x in u]
check("title_next folds a short title", refs[0] == "CHAPTER I The Aesir, par. 1", refs)
check("title_next leaves a long paragraph as text", refs[-1] == "CHAPTER II, par. 1", refs)

# 3. Two levels: the inner heading restarts paragraphs, the path is joined.
u = convert("NIGHT ONE\n\nTHE FIRST FABLE.\n\nOnce.\n\nTHE SECOND FABLE.\n\nTwice.\n\nNIGHT TWO\n\nTHE FIRST FABLE.\n\nThrice.",
            [{"re": "NIGHT [A-Z]+$"}, {"re": "THE [A-Z]+ FABLE\\.$"}])
ids = [x["id"] for x in u]
check("nested ids are unique", len(ids) == len(set(ids)), ids)
check("nested path in ref", [x["ref"] for x in u][-1] == "NIGHT TWO / THE FIRST FABLE, par. 1", [x["ref"] for x in u])

# 4. A plate caption that matches a level becomes a heading; others vanish.
u = convert("[Illustration:\n\n  The Story of Pinky.\n]\n\nA cat.\n\n[Illustration: a cat]\n\nAnother.",
            [{"re": "The Story of [A-Z][a-z]+\\.?$", "caption": True}])
refs = [x["ref"] for x in u]
check("caption heading", refs == ["The Story of Pinky, par. 1", "The Story of Pinky, par. 2"], refs)

# 5. number_repeats: a second tale under the same title is "(2)", not a run-on or a ~2;
#    a name the Contents used before the start is not counted.
u = convert("CONTENTS\n\nTHE DEAD.\n\nTHE BEAR.\n\nBODY\n\nTHE DEAD.\n\nOne.\n\nTHE DEAD.\n\nTwo.\n\nTHE BEAR.\n\nThree.\n\nTHE DEAD.\n\nFour.",
            [{"re": "(?:CONTENTS|THE [A-Z]+\\.)$", "number_repeats": True}], start="BODY$")
refs = [x["ref"] for x in u if x["ref"].startswith("THE")]
check("number_repeats numbers a repeated title",
      refs == ["THE DEAD, par. 1", "THE DEAD (2), par. 1", "THE BEAR, par. 1", "THE DEAD (3), par. 1"], refs)
check("number_repeats ids unique", len({x["id"] for x in u}) == len(u), [x["id"] for x in u])
u = convert("A\n\nTHE DEAD.\n\nOne.\n\nB\n\nTHE DEAD.\n\nTwo.",
            [{"re": "[AB]$"}, {"re": "THE DEAD\\.$", "number_repeats": True}])
check("number_repeats counts within the parent only",
      [x["ref"] for x in u] == ["A / THE DEAD, par. 1", "B / THE DEAD, par. 1"], [x["ref"] for x in u])

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
