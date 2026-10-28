#!/usr/bin/env python3
# prov: 2026-10-28 claude-opus-5-5 drafted
# fable_review: pending
"""Offline checks for unscanner/gutenberg.py: Gutenberg's proofread words laid onto OCR word boxes.
The OCR side is built here as word pieces (no hOCR, no scan), the Gutenberg side as a small .txt.
Run: python3 tests/gutenberg_layer_test.py
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from unscanner import gutenberg as G                    # noqa: E402

PASS, FAIL = 0, []


def check(name, ok):
    global PASS
    if ok:
        PASS += 1
    else:
        FAIL.append(name)
        print("FAIL", name)


PG = """header
*** START OF THE PROJECT GUTENBERG EBOOK TEST ***
[Illustration] Chapter First.

It happened that among those worthies who were summoned unto London Town
by the mandate of the Archbishop there was a certain knight, very honorable
and of high estate, and he was running to the anvil of the Archbishop.

[Sidenote: _Of Sir Ector, the trustworthy Knight._]

How a Young Knight of the King's Court was wounded, and if he lived
nobody knoweth; and the King descended the stair with great sorrow.
So it was, and so it is.
*** END OF THE PROJECT GUTENBERG EBOOK TEST ***
footer
"""

# what the OCR read, line by line: the drop initial lost, a misread, a word broken over a line,
# a running head and folio in the middle of the text, a sidenote read between the lines, and two
# compositor's slips that the print really has (Kinght, decended)
OCR_LINES = [
    (["Chapter", "First."], 96),
    (["T", "happened", "that", "among", "those", "worthies", "who", "were", "summoned", "unto", "London", "Town"], 95),
    (["by", "the", "mandate", "ot", "the", "Archbishop", "there", "was", "a", "certain", "knight,", "very", "honorable"], 94),
    (["and", "of", "high", "estate,", "and", "he", "was", "run-"], 95),
    (["12", "THE", "WINNING", "OF", "KINGHOOD"], 95),
    (["ning", "to", "the", "anvil", "of", "the", "Archbishop."], 95),
    (["Of", "Sir", "Ector,", "the", "trustwor-", "thy", "Knight."], 70),
    (["How", "a", "Young", "Kinght", "of", "the", "King's", "Court", "was", "wounded,", "and", "it", "he", "lived"], 92),
    (["nobody", "knoweth;", "and", "the", "King", "decended", "the", "stair", "with", "great", "sorrow."], 92),
]


def ocr_pieces():
    out = []
    for li, (words, conf) in enumerate(OCR_LINES):
        head = li == 4
        for wi, t in enumerate(words):
            parts = [x for x in G.SPLIT.split(t) if G.norm(x)]
            for k, x in enumerate(parts):
                out.append({"page": "p1" if li < 4 else "p2", "line": li, "word": wi, "part": k,
                            "parts": len(parts), "t": x, "n": G.norm(x), "bbox": [wi * 50, li * 40, wi * 50 + 40, li * 40 + 30],
                            "conf": conf, "full": t, "furniture": head})
    return out


def main():
    tmp = tempfile.mkdtemp()
    pg = os.path.join(tmp, "pg.txt")
    open(pg, "w").write(PG)
    body, notes = G.pg_body(pg)
    check("header and footer cut", body[0] == "Chapter" and body[-1] == "is.")
    check("sidenote taken out of the body", "trustworthy" not in body
          and [t for k, t, _ in notes if k == "sidenote"][-1] == "Knight.")
    check("italic marks dropped", all("_" not in t for _, t, _ in notes))

    check("typo shapes", G._typo("kinght", "knight") == "swap" and G._typo("decended", "descended") == "drop"
          and G._typo("of", "ot") is None)

    ocr = ocr_pieces()
    vocab = {}
    for t in body + [t for _, t, _ in notes]:
        vocab[G.norm(t)] = vocab.get(G.norm(t), 0) + 1
    assign, rows = G.classify(ocr, body, vocab)
    G.moved_pass(ocr, body, rows, assign)
    G.second_pass(ocr, notes, rows, assign)
    cls = {}
    for r in rows:
        cls.setdefault(r["class"], []).append(r)
    find = lambda t: [i for i, w in enumerate(ocr) if w["t"] == t]

    check("drop initial mended", assign.get(find("T")[0]) == "It" and "initial" in cls)
    check("misread mended", assign.get(find("ot")[0]) == "of")
    check("broken word: both halves carry Gutenberg's letters",
          assign.get(find("run")[0], "") + assign.get(find("ning")[0], "") == "running")
    check("running head kept as furniture", "furniture" in cls and find("WINNING")[0] not in assign)
    check("sidenote placed", assign.get(find("Ector,")[0]) == "Ector,")
    check("compositor's slips held for a person, not mended",
          sorted(r["ocr"][0] for r in cls.get("print_typo", [])) == ["Kinght", "decended"]
          and find("Kinght")[0] not in assign)
    check("two real words: a dispute", [r["ocr"] for r in cls.get("dispute", [])] == [["it"]])

    dec = [{"page": "p2", "ocr": ["it"], "pg": ["if"], "choice": "pg"},
           {"page": "p2", "ocr": ["Kinght"], "pg": ["Knight"], "choice": "ocr"}]
    n = G.apply_decisions(ocr, rows, assign, dec)
    check("decisions applied", n == 2 and assign.get(find("it")[0]) == "if" and find("Kinght")[0] not in assign)

    words = G.page_words(ocr, assign)
    texts = [t for t, _ in words["p2"]]
    check("page words: one per printed word, Gutenberg's spelling", "if" in texts and "Kinght" in texts
          and "Archbishop." in texts)
    print(f"{PASS} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
