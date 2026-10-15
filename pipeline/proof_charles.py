#!/usr/bin/env python3
"""
proof_charles.py -- an OCR flag list over the Charles 1913 text, word by
word (pipeline/build_charles.py). It FLAGS likely OCR errors for a person to
check against the scan; it never changes the text (golden rule 2: a fix,
once confirmed, is a per-book rule in the reader, so it reruns on rebuild).

    python3 pipeline/proof_charles.py --fetch   # the pinned word list -> data/corpus/proof/
    python3 pipeline/proof_charles.py           # write docs/review/charles-ocr-flags.{tsv,md}
    python3 pipeline/proof_charles.py --check   # the committed flags = a fresh pass

Needs the built books (python3 pipeline/build_charles.py).

WHAT IS FLAGGED, per token of every verse/page unit:
  glyph    a character no English page of Charles prints (™ ¢ | « ©, Greek
           or Hebrew letters inside the translation, stray control marks)
  mixed    letters and digits in one word ('l0rd', 'tbe5e'): a misread
           letter, or a verse number run into its word
  unknown  a lower-case word in no vocabulary below
  rare-name  a capitalised word (not opening a sentence) seen only once in
           all 32 books and in no vocabulary: a name the OCR may have bent
  hyphen   'a-b' where neither half is a word but 'ab' is: a line-end
           hyphen the reader did not join
  apparatus-dropped  a line build_charles.py left out as notes or apparatus
           (charles_ocr.is_apparatus_text), listed so it can be checked

VOCABULARY: the dwyl/english-words list (Unlicense, public domain; pinned by
commit and sha256), every word of the KJV with Apocrypha (eBible's USFM, the
file build_charles.py already pins), and every word Charles's own text uses
three times or more (an OCR error is rarely repeated letter for letter).

SUGGESTION: where one OCR-typical edit (rn/m, cl/d, li/h, ii/u, 1/l, 0/o,
c/e, f/t, h/b, ...; or one deleted, inserted or substituted letter) turns the
flagged word into a vocabulary word, the most frequent such word is offered.
It is a hint for the reviewer, never applied.

The flags are a list to read against the scan, with the unit id and leaf
for each. False positives are expected (Charles's rare transliterations);
recall is not measured, because no proofread Charles exists to measure it
against.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_charles as B  # noqa: E402

WORDS = {
    "url": "https://raw.githubusercontent.com/dwyl/english-words/"
           "20f5cc9b3f0ccc8ce45d814c532b7c2031bba31c/words_alpha.txt",
    "path": os.path.join(ROOT, "data", "corpus", "proof", "words_alpha.txt"),
    "sha256": "3ed0c94610d8bcf7c11bbb49c56aa49c7234d32b66824df91f554169e572da48",
    "rights": "The Unlicense (public domain dedication), github.com/dwyl/english-words",
}
OUT_TSV = os.path.join(ROOT, "docs", "review", "charles-ocr-flags.tsv")
OUT_MD = os.path.join(ROOT, "docs", "review", "charles-ocr-flags.md")

TOKEN = re.compile(r"\S+")
EDGE = "\"'‘’“”()[]{}.,;:!?—–-*_†‡§"
OK_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
               ".,;:!?'\"‘’“”()[]-—–*/&ÆæŒœéèêëàâäïîôöüûç⌜⌝⸢⸣ ")
CONFUSIONS = [("rn", "m"), ("m", "rn"), ("cl", "d"), ("d", "cl"), ("li", "h"), ("h", "li"),
              ("ii", "u"), ("u", "ii"), ("in", "m"), ("m", "in"), ("vv", "w"), ("tl", "d"),
              ("1", "l"), ("l", "1"), ("1", "i"), ("0", "o"), ("o", "0"), ("5", "s"), ("8", "s"),
              ("c", "e"), ("e", "c"), ("f", "t"), ("t", "f"), ("h", "b"), ("b", "h"), ("n", "u"),
              ("u", "n"), ("I", "l"), ("l", "I"), ("i", "l"), ("l", "i"), ("a", "o"), ("o", "a"),
              ("fi", "h"), ("ri", "n"), ("tb", "th"), ("tli", "th"), ("ct", "d")]
ALPHA = "abcdefghijklmnopqrstuvwxyz"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch():
    p = WORDS["path"]
    if os.path.exists(p) and sha256(p) == WORDS["sha256"]:
        print(f"  {os.path.basename(p)}: present, sha256 pinned")
        return
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with urllib.request.urlopen(WORDS["url"], timeout=120) as r:
        blob = r.read()
    if hashlib.sha256(blob).hexdigest() != WORDS["sha256"]:
        sys.exit(f"word list changed upstream: sha256 {hashlib.sha256(blob).hexdigest()}")
    tmp = p + ".tmp"
    with open(tmp, "wb") as f:
        f.write(blob)
    os.replace(tmp, p)
    print(f"  {os.path.basename(p)}: fetched")


def kjv_words():
    path = os.path.join(B.CACHE, B.KJV_CHECK["file"])
    c = collections.Counter()
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if not n.endswith(".usfm"):
                continue
            t = z.read(n).decode("utf-8", "replace")
            t = re.sub(r"\\[a-z0-9]+\*?", " ", t)
            t = re.sub(r"\|[^\\ ]*", " ", t)
            for w in re.findall(r"[A-Za-z]+", t):
                c[w.lower()] += 1
    return c


def books():
    for b in B.BOOKS:
        p = os.path.join(B.BOOKS_DIR, f"charles-{b[0]}.json")
        if not os.path.exists(p):
            sys.exit(f"{p} is not built: run python3 pipeline/build_charles.py")
        with open(p, encoding="utf-8") as f:
            yield b[0], json.load(f)


def core(tok):
    return tok.strip(EDGE)


def candidates(w, vocab):
    out = set()
    for a, b in CONFUSIONS:
        i = w.find(a)
        while i >= 0:
            out.add(w[:i] + b + w[i + len(a):])
            i = w.find(a, i + 1)
    for i in range(len(w) + 1):
        if i < len(w):
            out.add(w[:i] + w[i + 1:])
            for ch in ALPHA:
                out.add(w[:i] + ch + w[i + 1:])
        for ch in ALPHA:
            out.add(w[:i] + ch + w[i:])
    return [c for c in out if c in vocab and c != w]


def run():
    if not (os.path.exists(WORDS["path"]) and sha256(WORDS["path"]) == WORDS["sha256"]):
        sys.exit("pinned word list missing: run python3 pipeline/proof_charles.py --fetch")
    with open(WORDS["path"], encoding="utf-8") as f:
        dwyl = {w.strip().lower() for w in f if w.strip()}
    kjv = kjv_words()
    data = list(books())
    own = collections.Counter()
    caps = collections.Counter()
    for _, bk in data:
        for u in bk["units"]:
            for t in TOKEN.findall(u["text"]):
                w = core(t)
                if w.isalpha():
                    own[w.lower()] += 1
                    if w[0].isupper():
                        caps[w] += 1
    vocab = dwyl | set(kjv) | {w for w, n in own.items() if n >= 3}
    freq = collections.Counter(kjv)
    freq.update(own)

    rows = []
    words = collections.Counter()
    per = collections.defaultdict(collections.Counter)
    for key, bk in data:
        for u in bk["units"]:
            toks = TOKEN.findall(u["text"])
            for i, t in enumerate(toks):
                words[key] += 1
                w = core(t)
                if not w:
                    continue
                kind = None
                if any(ch not in OK_CHARS for ch in t):
                    kind = "glyph"
                elif any(ch.isdigit() for ch in w) and any(ch.isalpha() for ch in w):
                    kind = "mixed"
                elif "-" in w and w.replace("-", "").isalpha():
                    parts = [p.lower() for p in w.split("-") if p]
                    joined = "".join(parts)
                    if joined in vocab and not all(p in vocab for p in parts):
                        kind = "hyphen"
                elif w.isalpha() and w.lower() not in vocab:
                    prev = toks[i - 1] if i else "."
                    opens = prev[-1:] in ".?!:" or i == 0
                    if w[0].islower():
                        kind = "unknown"
                    elif not opens and caps[w] == 1:
                        kind = "rare-name"
                    elif opens and w.lower() not in own:
                        kind = "unknown"
                if not kind:
                    continue
                sug = ""
                if kind == "hyphen":
                    sug = w.replace("-", "")
                elif kind in ("unknown", "rare-name", "mixed"):
                    lw = w.lower()
                    cs = candidates(lw, vocab)
                    if cs:
                        best = max(cs, key=lambda c: (freq[c], c))
                        sug = best if w[0].islower() else best[:1].upper() + best[1:]
                ctx = " ".join(toks[max(0, i - 4):i] + ["⟦" + t + "⟧"] + toks[i + 1:i + 5])
                leaf = u.get("scan", {}).get("leaves", [""])[0]
                rows.append((u["id"], str(leaf), kind, w, sug, ctx.replace("\t", " ")))
                per[key][kind] += 1
        for d in bk.get("apparatus_dropped", []):
            rows.append((f"charles-{key}", str(d["leaf"]), "apparatus-dropped", "", "",
                         d["text"].replace("\t", " ")))
            per[key]["apparatus-dropped"] += 1
    return rows, words, per


def render(rows, words, per):
    tsv = "unit\tleaf\tkind\ttoken\tsuggestion\tcontext\n" + "".join("\t".join(r) + "\n" for r in rows)
    kinds = ["glyph", "mixed", "unknown", "rare-name", "hyphen", "apparatus-dropped"]
    lines = [
        "# Charles 1913: OCR flag list, for review against the scans",
        "",
        "Generated by `python3 pipeline/proof_charles.py` from the built `charles-*` books;",
        "nothing in the text was changed. Every flag is in `charles-ocr-flags.tsv`: the unit",
        "id, the scan leaf to open, the kind of flag, the token, a suggested reading where",
        "one OCR-typical edit gives a known word, and the words around it. A suggestion is",
        "a hint, never applied; a confirmed fix becomes a rule in the reader so it reruns.",
        "",
        "Kinds: `glyph` a character Charles's English does not print; `mixed` letters and",
        "digits in one word; `unknown` a word in no vocabulary (an English word list, the",
        "KJV with Apocrypha, and any word Charles's text uses three or more times);",
        "`rare-name` a capitalised word used once and known nowhere; `hyphen` a line-end",
        "hyphen left in a word; `apparatus-dropped` a whole line the reader took for notes",
        "or apparatus and left out of the verses (book and leaf, its text in `context`), to",
        "check that nothing of Charles's English was lost. False positives are expected",
        "(transliterated names); how many errors the pass misses is not measured. This is a",
        "list of places to look, not a proofreading: the text is unchanged and unproofread.",
        "",
        "| book | words | " + " | ".join(kinds) + " | word flags per 1,000 words |",
        "|---|---:|" + "---:|" * len(kinds) + "---:|",
    ]
    tot = collections.Counter()
    for b in B.BOOKS:
        k = b[0]
        n = sum(per[k][x] for x in kinds[:-1])     # word flags; dropped lines are not words
        tot.update(per[k])
        lines.append(f"| {k} | {words[k]:,} | " + " | ".join(f"{per[k][x]:,}" for x in kinds)
                     + f" | {1000 * n / words[k]:.1f} |" if words[k] else f"| {k} | 0 |")
    W = sum(words.values())
    lines.append(f"| **all** | {W:,} | " + " | ".join(f"{tot[x]:,}" for x in kinds)
                 + f" | {1000 * sum(tot[x] for x in kinds[:-1]) / W:.1f} |")
    lines.append("")
    return tsv, "\n".join(lines)


def write_atomic(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
        return
    tsv, md = render(*run())
    if a.check:
        bad = [p for p, t in ((OUT_TSV, tsv), (OUT_MD, md))
               if not os.path.exists(p) or open(p, encoding="utf-8").read() != t]
        if bad:
            sys.exit(f"CHECK FAILED: {bad} differ from a fresh pass")
        print("  CHECK PASSED: the committed flags = a fresh pass")
        return
    write_atomic(OUT_TSV, tsv)
    write_atomic(OUT_MD, md)
    print(f"  wrote {tsv.count(chr(10)) - 1:,} flags -> {os.path.relpath(OUT_TSV, ROOT)}")


if __name__ == "__main__":
    main()
