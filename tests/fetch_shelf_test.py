#!/usr/bin/env python3
"""
fetch_shelf_test.py -- the two gate fixes of 2026-10-03, offline.

Run:  python3 tests/fetch_shelf_test.py

1. The identity gate collects every miss. An `_identity_checked` override
   covers only the miss it names (a plain string: the first author-or-title
   miss; a dict: its "author"/"title" keys) and never the translator.
3. A surname that is also a common English word ("hall", "ken") is never
   matched bare; a shelf whose only forms are bare common words stops at load.
2. The IA rights gate fails closed: anything but "ok" is refused unless
   `_rights_checked` names the slug, and the latest year on the record decides.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
import fetch_shelf as fs

ok = 0
def check(cond, what):
    global ok
    if not cond:
        sys.exit(f"FAIL: {what}")
    ok += 1

def run(text, override=None, translator=None, key=("sermons", "preached"), surname=("edwards",)):
    r = {}
    try:
        fs.check_identity(r, text.encode(), list(key), set(), "ia", override, list(surname), None, translator)
        return r, None
    except RuntimeError as e:
        return r, str(e)

GOOD = "sermons preached by jonathan edwards, translated by smith"
r, e = run(GOOD, translator="smith")
check(e is None and "identity_override" not in r, "a clean text passes")

r, e = run("sermons preached at the rolls", override=None)
check(e and "surname" in e, "an author miss with no override is refused")

r, e = run("sermons preached at the rolls", override="title page read by eye")
check(e is None and "kept: title page" in r["identity_override"], "a string override covers the author miss")

r, e = run("sermons preached at the rolls", override="title page read by eye", translator="smith")
check(e and "translator" in e and "surname" not in e,
      "an author override no longer hides a translator miss")

r, e = run("an unrelated pamphlet", override="title page read by eye")
check(e and "title words" in e and "surname" not in e,
      "a string override covers only the first miss; the title miss after it still refuses")

r, e = run("an unrelated pamphlet", override={"author": "seen", "title": "seen"})
check(e is None and r["identity_override"].count("kept:") == 2, "a dict override covers the misses it names")

r, e = run("sermons preached by edwards", override={"author": "x", "title": "y", "translator": "z"}, translator="smith")
check(e and "translator" in e, "no override ever covers the translator")

r, e = run("sermons preached at the rolls", override="read by eye", translator="smith")
check(e and "translator" in e, "a string override never covers the translator either")

# rights: fail closed, latest year decides
def rights(date, fail=False, cols=()):
    real = fs.get
    def fake(url, tries=3):
        if fail:
            raise OSError("offline")
        import json
        return json.dumps({"result": {"date": date, "collection": list(cols)}}).encode()
    fs.get = fake
    try:
        return fs.ia_rights("x")["ia_rights"]
    finally:
        fs.get = real

check(rights("1890").startswith("ok"), "an 1890 record is ok")
check(rights("1965 [c1890]").startswith("CHECK: published 1965"), "a 1965 reprint of an 1890 book is a 1965 printing")
check(rights("", fail=True).startswith("unchecked"), "an unreachable catalogue reads unchecked")
check(not rights("", fail=True).startswith("ok"), "and unchecked is not ok, so the gate refuses it")
check(rights("").startswith("CHECK: no date"), "an undated record is CHECK")
check(rights("1890", cols=["inlibrary"]).startswith("CHECK"), "a lending scan is CHECK")

# common-word surnames
for w in ("hall", "ken", "brown", "gale", "lamb", "church", "palmer", "skinner", "fuller", "barrow"):
    check(w in fs.COMMON_WORD_SURNAMES, f"{w!r} is on the common-word list")
for w in ("edwards", "newman", "wesley", "traherne"):
    check(w not in fs.COMMON_WORD_SURNAMES, f"{w!r} is a usable bare surname")
check(fs.check_surnames({"_surname": ["hall"]}), "a shelf naming only bare 'hall' stops at load")
check(fs.check_surnames({"_surname_by_slug": {"x": ["ken"]}}), "so does a per-item list of bare 'ken'")
check(not fs.check_surnames({"_surname": ["joseph hall", "hall"]}), "a multi-word form beside it loads")
check(not fs.check_surnames({"_surname": ["edwards"]}), "an uncommon bare surname loads")
r, e = run("sermons preached in the hall of the college", surname=("joseph hall", "hall"))
check(e and "surname" in e, "the bare common word never matches: 'the hall' is not Joseph Hall")
r, e = run("sermons preached by joseph hall", surname=("joseph hall", "hall"))
check(e is None and r["author_seen"] == "joseph hall", "the full name does")
r, e = run("sermons preached by the bishop of norwich, joseph\nhall", surname=("joseph hall",))
check(e is None, "a full name broken across an OCR line still matches")

print(f"fetch_shelf_test: {ok} checks passed")
