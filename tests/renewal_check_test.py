#!/usr/bin/env python3
"""renewal_check.py's matching rules, on made-up renewal rows (no download needed).

    python3 tests/renewal_check_test.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
import renewal_check as rc

ROWS = [
    ("1962-1.tsv", "BURROUGHS, EDGAR RICE.", "Lost on Venus; illustrated by J. Allen St. John.", "A80914", "1935-02-15", "R305497", "1962-11-26", ""),
    ("1977-1.tsv", "Edgar Rice Burroughs.", "Triumphant. (Tarzan, no. 3485) (In United feature comics, Oct. 6, 1950)", "B5-15797", "1950-10-06", "R676470", "1977-11-01", ""),
    ("1990-from-db.tsv", "Soeren Aabye Kierkegaard, translated by Howard Hong and Edna Hong.", "Works of love.", "A560757", "1962-03-28", "RE484468", "1990-07-17", ""),
    ("1960-1.tsv", "TRAIN, ARTHUR C.", "Puritan's progress.", "A34699", "1931-02-13", "R210517", "1958-03-19", ""),
]
rc._ROWS = [(r, " " + rc.norm(r[1] + " " + r[2] + " " + r[7]) + " ", set(rc.words(r[2] + " " + r[7]))) for r in ROWS]

n = 0
def check(cond, what):
    global n
    n += 1
    if not cond:
        sys.exit(f"FAIL: {what}")

h = rc.full_hits(rc.search(author="Edgar Rice Burroughs", title="Lost on Venus"))
check(len(h) == 1 and h[0][1][5] == "R305497", "a renewed title is found in full")
check(rc.search(author="Arthur Train", title="The Moon Maker") == [], "an unrenewed title finds nothing")
h = rc.search(author="Edgar Rice Burroughs", title="Tarzan the Invincible")
check(len(h) == 1 and h[0][0] == "title 1/2", "a one-word overlap is a loose candidate only")
check(rc.full_hits(rc.search(author="Kierkegaard", title="Works of Love")), "the surname is found inside a translator's credit")
check(rc.search(author="Walter Lowrie", title="Works of Love") == [], "another surname does not match")
check(rc.search(reg="A-34699")[0][0] == "reg", "a registration number matches, punctuation ignored")
check(rc.surname_of("Roy J. Snell (tr. nobody)") == "snell", "the surname is the last name word")
check(rc.surname_of("Lewis Sperry Chafer, Jr.") == "chafer", "Jr. is not a surname")
check([h[1][5] for h in rc.title_only("Works of Love")] == ["RE484468"], "a title-only search ignores the name")
print(f"renewal_check_test: {n} checks passed")
