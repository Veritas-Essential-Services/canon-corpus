# prov: 2026-10-20 claude-opus-5-5 drafted
# fable_review: pending
"""The fix library: what other people learned fighting OCR, held in one place, and a profile that
picks out the fixes actually in play for the typesetting of the book at hand.

Adam, 2026-10-20: "Can we ingest each of these and build a whole system that picks and chooses from a
whole library of fixes and choose the elements that are actually in play with the particular
typesetting that one is working from."

    python3 -m unscanner fixes fetch      # the pinned sources -> data/fixes/src/ (gitignored)
    python3 -m unscanner fixes build      # -> data/fixes/library.jsonl, one rule a line (gitignored)
    python3 -m unscanner fixes profile --book data/unscanner/<slug> [--review R.json --answers A.json ...]
                                          # -> <book>/fixes-profile.json: every rule, in play or not, and why

SOURCES (each rule keeps its source; none of these files is committed: the repo is public, and
Guiguts is GPL-2 and Underwood's rules carry no licence, so they are fetched and used locally only,
as STEPBible is):
  guiguts      Distributed Proofreaders' scanno lists (the volunteers behind most Project Gutenberg
               books): common scannos ("arid" -> "and"), stealth scannos (both words: "bad"/"had"),
               known misspellings, regular expressions, and the GutWrench/GutAxe lists. GPL-2.0.
  underwood    Ted Underwood's OCR normalizer rules for English after 1700 (98,380 measured pairs,
               "tbe" -> "the", "foon" -> "soon"); his syncope, fusing, hyphen and variant-spelling rules
               are NORMALIZATIONS (they modernize) and are never applied to a faithful text. No licence.
  icdar2019    ICDAR 2019 Competition on Post-OCR Text Correction, English part: OCR aligned with a
               corrected text, character by character. Mined here for character confusions
               ("c" read as "e", "h" as "li") and their counts. CC BY 4.0, Rigaud, Doucet, Coustaty and
               Moreux (2019).
  house        The rules learned from Adam's answers on the Proof Desk (learned.py, smallcaps.py,
               layout.py rules 6-7), listed so a profile shows them beside the borrowed ones.

THE PROFILE. A rule is in play for a book only when the book gives it work and the evidence says it
is right there:
  - it fires: the book has the rule's "wrong" form at least once (a long-s rule never fires in a book
    with no long s, so it stays off without anyone deciding so);
  - the book's own words: the corrected form is printed cleanly elsewhere in this book (tesseract
    confidence 90+), or is a dictionary word; the "wrong" form is NOT a dictionary word, and is not
    printed cleanly elsewhere (when it is, the page really says it: "bad", "ball");
  - the desk: where the rule fires on a word that a person or Claude's eyes settled for this book
    (the answers given), how often it gives that answer (its precision on this typesetting). Rules'
    own clears are not used as truth, so no rule grades itself.
  on    : it fires, the desk does not contradict it (precision >= 0.9 where it has 2+ cases), and the
          book's words support it;
  flag  : it fires but the evidence is mixed (a stealth scanno: both forms are words): listed for a
          person, never applied;
  off   : it does not fire, or the desk or the book contradicts it.
Character confusions are profiled the same way, as a class: every word the dictionary does not know
is tried with each confusion; a confusion that turns many of this book's non-words into words it
prints elsewhere, and agrees with the desk, is a trait of this typesetting ("this face's c reads as e").
"""
import gzip
import hashlib
import json
import os
import re
import subprocess
import unicodedata
import urllib.request
import zipfile
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ROOT = os.path.join(REPO, "data", "fixes")
SRC = os.path.join(ROOT, "src")

SOURCES = {
    "guiguts": {"git": "https://github.com/DistributedProofreaders/guiguts.git",
                "commit": "5e32afdf024b384325b8bd3db2de9126b375de1e", "license": "GPL-2.0",
                "redistribute": False, "credit": "Distributed Proofreaders, Guiguts"},
    "guiguts-py": {"git": "https://github.com/DistributedProofreaders/guiguts-py.git",
                   "commit": "c31b3f9e3c0c08b253ca97813bc4a7df0acb4b8f", "license": "GPL-2.0",
                   "redistribute": False, "credit": "Distributed Proofreaders, Guiguts 2"},
    "underwood": {"git": "https://github.com/tedunderwood/DataMunging.git",
                  "commit": "a8c5c93d399be36ebdc666cdc27f659527150f24",
                  "license": "none stated (all rights reserved by default): fetched and used locally, never redistributed",
                  "redistribute": False, "credit": "Ted Underwood, DataMunging / OCRnormalizer"},
    "icdar2019": {"url": "https://zenodo.org/records/3515403/files/ICDAR2019-POCR-ground-truth.zip?download=1",
                  "sha256": "519fd9ae3e8457504e8995b7b0cc71e3b92e64a1e8c9ac2e5695e10977e32c2e",
                  "license": "CC-BY-4.0", "redistribute": True,
                  "credit": "Rigaud, Doucet, Coustaty, Moreux, ICDAR 2019 Competition on Post-OCR Text Correction"},
}

# ---------------------------------------------------------------- fetch


def fetch(log=print):
    os.makedirs(SRC, exist_ok=True)
    for sid, s in SOURCES.items():
        dest = os.path.join(SRC, sid)
        if "git" in s:
            if not os.path.isdir(os.path.join(dest, ".git")):
                subprocess.run(["git", "init", "-q", dest], check=True)
                subprocess.run(["git", "-C", dest, "remote", "add", "origin", s["git"]], check=True)
            have = subprocess.run(["git", "-C", dest, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            if have != s["commit"]:
                subprocess.run(["git", "-C", dest, "fetch", "-q", "--depth", "1", "origin", s["commit"]], check=True)
                subprocess.run(["git", "-C", dest, "checkout", "-q", s["commit"]], check=True)
            log(f"  {sid}: {s['commit'][:12]} ({s['license']})")
        else:
            path = dest + ".zip"
            if not os.path.exists(path) or _sha(path) != s["sha256"]:
                with urllib.request.urlopen(s["url"], timeout=300) as r, open(path + ".part", "wb") as f:
                    f.write(r.read())
                os.replace(path + ".part", path)
            assert _sha(path) == s["sha256"], f"{sid}: sha256 differs from the pinned one"
            log(f"  {sid}: sha256 {s['sha256'][:12]} ({s['license']})")


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

# ---------------------------------------------------------------- ingest


PERL_PAIR = re.compile(r"^\s*'((?:[^'\\]|\\.)*)'\s*=>\s*'((?:[^'\\]|\\.)*)'", re.M)
# a regular expression about markup (HTML, footnote brackets, spacing, line ends) is not about the
# words the OCR read: kept out of the library
MARKUP = re.compile(r"html|<|footnote|sidenote|illustration|bracket|space|blank line|line end|\\n|tab|"
                    r"page ?break|markup|tag|asterisk|ellips|dash|hyphen at|quote mark", re.I)


def _rule(kind, match, source, file, replace=None, **kw):
    r = {"kind": kind, "match": match, "source": source, "file": file}
    if replace is not None:
        r["replace"] = replace
    r.update(kw)
    r["id"] = f"{source}:{kind}:{hashlib.md5((kind + match + (replace or '')).encode()).hexdigest()[:10]}"
    return r


def _perl_hash(path, source, file, kind="word"):
    out = []
    for m in PERL_PAIR.finditer(open(path, encoding="utf-8", errors="replace").read()):
        a, b = m.group(1).replace("\\'", "'"), m.group(2).replace("\\'", "'")
        if kind == "word" and not b:
            out.append(_rule("suspect", a, source, file))
        else:
            out.append(_rule(kind, a, source, file, b))
    return out


def ingest_guiguts():
    base = os.path.join(SRC, "guiguts", "src", "scannos")
    out = []
    out += _perl_hash(os.path.join(base, "en-commn.rc"), "guiguts", "en-commn.rc")
    out += _perl_hash(os.path.join(base, "misspelled.rc"), "guiguts", "misspelled.rc")
    out += [r for r in _perl_hash(os.path.join(base, "regex.rc"), "guiguts", "regex.rc", kind="regex")
            if not MARKUP.search(r["match"] + r.get("replace", ""))]
    gw = os.path.join(base, "GutWrenchGutAxe")
    out += _perl_hash(os.path.join(gw, "scanno_w.rc"), "guiguts", "GutWrench scanno_w.rc")
    for line in open(os.path.join(gw, "GAscanno.txt"), encoding="utf-8", errors="replace"):
        s = line.strip()
        if len(s) < 4 or s[0].lower() not in "swr":
            continue
        d = s[1]
        parts = s[2:].split(d)
        if len(parts) < 3:
            continue
        err, cor, desc = parts[0], parts[1], parts[2]
        if MARKUP.search(desc + err):
            continue
        kind = {"s": "string", "w": "word", "r": "regex"}[s[0].lower()]
        stealth = "stealth" in desc.lower()
        out.append(_rule("stealth" if (stealth and kind == "word") else kind, err, "guiguts", "GutAxe GAscanno.txt",
                         cor.replace("$", "\\"), note=desc))
    return out


def ingest_underwood():
    base = os.path.join(SRC, "underwood", "rulesets")
    out = []
    for line in open(os.path.join(base, "CorrectionRules.txt"), encoding="utf-8", errors="replace"):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 2 and p[0] and p[1]:
            w = int(p[2]) if len(p) > 2 and p[2].strip().isdigit() else None
            out.append(_rule("word", p[0], "underwood", "CorrectionRules.txt", p[1], weight=w))
    for line in open(os.path.join(base, "AmbiguousPairs.txt"), encoding="utf-8", errors="replace"):
        p = line.split()
        if len(p) == 2:
            out.append(_rule("stealth", p[1], "underwood", "AmbiguousPairs.txt", p[0], note="long-s pair"))
    for f in ("SyncopeRules.txt", "FusingRules.txt", "HyphenRules.txt", "VariantSpellings.txt"):
        for line in open(os.path.join(base, f), encoding="utf-8", errors="replace"):
            p = line.rstrip("\n").split("\t")
            if len(p) >= 2 and p[0] and p[1]:
                out.append(_rule("normalize", p[0], "underwood", f, p[1],
                                 note="modernizes: never applied to a faithful text"))
    return out


def _confusions(ocr, gs):
    """Aligned OCR and gold strings ('@' fills gaps) -> character confusions (wrong -> right), one to
    three characters each side, inside words only."""
    out = []
    i, n = 0, min(len(ocr), len(gs))
    while i < n:
        if ocr[i] == gs[i]:
            i += 1
            continue
        j = i
        while j < n and ocr[j] != gs[j] and j - i < 3:
            j += 1
        a, b = ocr[i:j].replace("@", ""), gs[i:j].replace("@", "")
        left, right = ocr[i - 1:i], ocr[j:j + 1]
        if a != b and (a + b).isalpha() and left.isalpha() and (right.isalpha() or right == ""):
            out.append((a, b))
        i = j
    return out


def ingest_icdar(lang="EN"):
    path = os.path.join(SRC, "icdar2019.zip")
    c = Counter()
    words = Counter()
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.startswith("full_22M_without_Finnish/" + lang + "/") and n.endswith(".txt")]
        for n in names:
            t = z.read(n).decode("utf-8", errors="replace")
            m1 = re.search(r"\[OCR_aligned\] (.*)", t)
            m2 = re.search(r"\[ GS_aligned\] (.*)", t)
            if not (m1 and m2):
                continue
            o, g = m1.group(1), m2.group(1)
            c.update(_confusions(o, g))
            # word pairs: aligned tokens by the gold's spaces
            for ow, gw in zip(re.split(r"(?<=\S) (?=\S)", o), re.split(r"(?<=\S) (?=\S)", g)):
                ow, gw = ow.replace("@", ""), gw.replace("@", "")
                if ow != gw and ow.isalpha() and gw.isalpha() and 2 <= len(gw) <= 20:
                    words[(ow, gw)] += 1
    out = [_rule("char", a, "icdar2019", f"{lang} aligned", b, weight=k) for (a, b), k in c.items() if k >= 3]
    out += [_rule("word", a, "icdar2019", f"{lang} aligned", b, weight=k) for (a, b), k in words.items() if k >= 2]
    return out


HOUSE = [
    ("roman", "a garbled roman numeral (Ill, lU, HI, 1.) -> the roman reading", "learned.py"),
    ("ligature", "e / se / ce / ae / ee where æ is printed -> æ", "learned.py"),
    ("smallcaps", "a word in small capitals read as a jumble -> capitals", "learned.py, smallcaps.py"),
    ("smallcaps-reread", "a jumbled word or a headword before its bracket, reread capitals-only from each scan", "smallcaps.py"),
    ("abbrev", "a stock abbreviation wins (etc., &c., viz., i.e.)", "learned.py"),
    ("c-for-e", "two readings differ only by c/e -> c, unless only the e form is a word", "learned.py"),
    ("ll-in-word", "a capital U inside a lower-case word -> ll / li / il", "learned.py"),
    ("lig-garble", "a capital U/H inside a word -> li, a final se/ae/z -> æ, both scans agreeing", "learned.py"),
    ("R-E-B-h", "R read as E/B/P, b as h -> tesseract's reading", "learned.py"),
    ("same-scan", "both engines on one scan agree -> that pair", "learned.py"),
    ("margin-6b-6d", "margin breaks: ranges, small capitals, names, Webster, OCR dirt", "layout.py"),
    ("dashes-7", "en dash ranges, close em dashes, attribution dashes", "layout.py"),
    ("furniture", "two columns, a running head over each, signature marks", "layout.py"),
]


def build(log=print):
    rules = []
    for name, fn in (("guiguts", ingest_guiguts), ("underwood", ingest_underwood), ("icdar2019", ingest_icdar)):
        got = fn()
        log(f"  {name}: {len(got)} rules  {dict(Counter(r['kind'] for r in got))}")
        rules += got
    rules += [_rule("house", k, "house", f, note=d) for k, d, f in HOUSE]
    seen, out = set(), []
    for r in rules:
        if r["id"] not in seen:
            seen.add(r["id"])
            out.append(r)
    os.makedirs(ROOT, exist_ok=True)
    tmp = os.path.join(ROOT, "library.jsonl.part")
    with open(tmp, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, os.path.join(ROOT, "library.jsonl"))
    json.dump({k: {x: v for x, v in s.items() if x not in ("git", "url")} | {"from": s.get("git") or s.get("url")}
               for k, s in SOURCES.items()}, open(os.path.join(ROOT, "sources.json"), "w"), indent=1)
    log(f"  library: {len(out)} rules -> {os.path.join(ROOT, 'library.jsonl')}")
    return out


def load_library():
    return [json.loads(l) for l in open(os.path.join(ROOT, "library.jsonl"), encoding="utf-8")]

# ---------------------------------------------------------------- profile


def letters(t):
    t = unicodedata.normalize("NFC", t)
    m = re.search(r"[^\W\d_](?:[\w’'\-]*[^\W\d_])?", t)
    return m.group(0) if m else ""


def book_words(book):
    """Every word of a book.json: (page n, line index, word index, text, confidence)."""
    for p in book["pages"]:
        if p.get("kind") != "text":
            continue
        drop = set(p.get("drop") or [])
        for li, ln in enumerate(p["lines"]):
            if li in drop:
                continue
            for wi, w in enumerate(ln["words"]):
                yield p["n"], li, wi, w.get("was") or w["t"], w.get("conf") or 0


def _recase(src, rep):
    if src.isupper() and len(src) > 1:
        return rep.upper()
    if src[:1].isupper():
        return rep[:1].upper() + rep[1:]
    return rep


class Evidence:
    """What a book says about its own words, and what its desk settled."""

    def __init__(self, book, lexicon, truth=None, texts=None):
        """texts: the book's words after margin breaks are rejoined (merged paragraphs, or the
        Unscanner's units). Without it the scan's own words are counted, skipping both halves of a
        word broken at a line's end ("pro-" / "fessions" is no word "fessions")."""
        self.lexicon = lexicon
        self.clean = Counter()
        self.all = Counter()
        prev_broken = False
        for _, _, wi, t, conf in book_words(book):
            w = letters(t).lower()
            broken = t.endswith("-")
            frag = broken or (prev_broken and wi == 0)
            prev_broken = broken if broken else (prev_broken and wi != 0 and False)
            if not w or frag:
                continue
            if texts is None:
                self.all[w] += 1
            if conf >= 90:
                self.clean[w] += 1
        if texts is not None:
            for t in texts:
                for tok in t.split():
                    w = letters(tok).lower()
                    if w:
                        self.all[w] += 1
        self.truth = truth or {}            # base reading (lower letters) -> Counter(settled answer)

    def known(self, w):
        """A dictionary word, or one with a common ending ("contends"), or one this book prints
        cleanly twice."""
        from .layout import in_dictionary
        return in_dictionary(w, self.lexicon) or self.clean[w] >= 2

    def good_target(self, w):
        """What a correction may produce: a dictionary word (with its endings) printed cleanly in this
        book, or a name or foreign word the book prints cleanly three times."""
        from .layout import in_dictionary
        return (in_dictionary(w, self.lexicon) and self.clean[w] >= 1) or self.clean[w] >= 3


def desk_truth(review, answers):
    """review.json items + answers (person or Claude's eyes) -> {base reading: Counter(answer)}."""
    t = defaultdict(Counter)
    for it in review["items"]:
        a = answers.get(it["id"])
        if a is None:
            continue
        b = letters(it["base"]).lower()
        if b:
            t[b][letters(a).lower()] += 1
    return t


def edits(a, b):
    """The character confusions that turn a into b ("chureh" -> "church": [("e", "c")])."""
    import difflib
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op != "equal":
            out.append((a[i1:i2], b[j1:j2]))
    return out


def profile_word_rule(r, ev, traits=None):
    m = r["match"]
    rep = r.get("replace", "")
    ml = m.lower()
    if rep and rep.lower() == ml:
        return "off", {"why": "changes only the case"}
    if r["source"] == "icdar2019" and (r.get("weight") or 0) < 5:
        return "off", {"why": "seen fewer than five times in the ICDAR alignment"}
    hits = ev.all.get(ml, 0)
    if not hits:
        return "off", {"hits": 0, "why": "does not fire in this book"}
    tp = fp = 0
    for ans, k in ev.truth.get(ml, {}).items():
        if ans == rep.lower():
            tp += k
        else:
            fp += k
    st = {"hits": hits, "desk_right": tp, "desk_wrong": fp}
    if r["kind"] == "suspect":
        return ("flag", st | {"why": "a known misspelling; no correction given"})
    if tp + fp >= 2 and tp / (tp + fp) < 0.9:
        return "off", st | {"why": "the desk contradicts it"}
    match_real = ml in ev.lexicon or ev.clean[ml] >= 3
    rep_ok = rep.lower() in ev.lexicon or ev.clean[rep.lower()] >= 1
    if r["kind"] == "stealth" or match_real:
        if tp >= 2 and fp == 0:
            return "on", st | {"why": "both forms are words, but the desk settles it"}
        return "flag", st | {"why": "both forms are words (a stealth scanno): for a person"}
    if not rep_ok:
        return "off", st | {"why": "the correction is not a word of this book or the dictionary"}
    if traits is not None and not tp:
        # a borrowed rule is only as good as the confusion under it: on only when every edit it makes
        # is a confusion this typeface is seen to make ("chureh" -> "church" rests on c read as e,
        # in play here; "foundly" -> "soundly" rests on the long s, which this book does not have)
        missing = [e for e in edits(ml, rep.lower()) if traits.get(e) != "on"]
        if missing:
            return "flag", st | {"why": "rests on a confusion not seen in this typeface: " +
                                 ", ".join(f"{a or '∅'}->{b or '∅'}" for a, b in missing)}
    return "on", st | {"why": "the wrong form is no word; the right one is" + (", and the desk agrees" if tp else "") +
                       ("" if traits is None else "; its confusions are this typeface's")}


def misread(w, conf, ev, ratio=3):
    """Is w a misreading, one confusion from a word? Two ways:
      - it is no word, the OCR never read it cleanly, and exactly one confusion makes a good word;
      - it is no dictionary word, but the OCR read it confidently by habit ("ealled" 38 times, 14 of
        them at 90+): one confusion makes a dictionary word this book prints `ratio` times as often
        ("called", 182).
    -> the corrected word, or None."""
    from .layout import in_dictionary
    if len(w) < 4 or in_dictionary(w, ev.lexicon):
        return None
    c = {cand for _, cand in char_candidates(w, conf, ev)}
    if len(c) != 1:
        return None
    cand = c.pop()
    # a short word has too many neighbours ("loue" is love, not lone): four letters need the corrected
    # word to be the book's habit, not merely a word
    if len(w) <= 4 and ev.all[cand] < ratio * 3 * max(1, ev.all[w]):
        return None
    if ev.clean[w] == 0 and not ev.known(w):
        return cand
    if in_dictionary(cand, ev.lexicon) and ev.all[cand] >= ratio * max(1, ev.all[w]):
        return cand
    return None


def char_candidates(word, conf, ev, limit=40):
    """Every word one character confusion away from a non-word, that THIS BOOK prints cleanly
    (tesseract 90+) somewhere: a dictionary word alone is not enough ("rumored" -> "tumored")."""
    out = []
    for a, b in conf[:limit]:
        start = 0
        while True:
            i = word.find(a, start)
            if i < 0:
                break
            cand = word[:i] + b + word[i + len(a):]
            if ev.good_target(cand):
                out.append(((a, b), cand))
            start = i + 1
    return out


def profile(book, lexicon, library, truth=None, texts=None, log=print):
    """Traits are learned from the scan's own words (all of them, before any vote or answer); the
    rules' hits are counted on `texts` when given (what is left to fix after the vote and the desk)."""
    raw = Evidence(book, lexicon, truth)
    ev = Evidence(book, lexicon, truth, texts) if texts is not None else raw
    res = {"rules": {}, "summary": Counter(), "traits": []}
    # 1. the typeface's confusions, measured on its non-words
    weights = {(r["match"], r["replace"]): r.get("weight") or 0 for r in library if r["kind"] == "char"}
    chars = sorted(weights, key=lambda ab: -weights[ab])
    house = [("e", "c"), ("li", "h"), ("U", "ll"), ("rn", "m"), ("c", "e"), ("ii", "u"), ("tl", "d"),
             ("f", "s"), ("n", "u"), ("u", "n")]
    for h in house:
        if h not in weights:
            chars.insert(0, h)
    per = defaultdict(lambda: {"words": 0, "desk_right": 0, "desk_wrong": 0, "examples": []})
    for w, n in raw.all.items():
        # a word printed cleanly in the book is what the page says ("enfants", "valeur"), unless it is
        # a confident habit of the OCR's (misread: "ealled" beside "called")
        cand = misread(w, chars, raw)
        if not cand:
            continue
        ab = next(ab for ab, c in char_candidates(w, chars, raw) if c == cand)
        st = per[ab]
        st["words"] += n
        if len(st["examples"]) < 6:
            st["examples"].append(f"{w}->{cand}")
        for ans, k in raw.truth.get(w, {}).items():
            if ans == cand:
                st["desk_right"] += k
            else:
                st["desk_wrong"] += k
    traits = {}
    for ab, st in sorted(per.items(), key=lambda kv: -kv[1]["words"]):
        tot = st["desk_right"] + st["desk_wrong"]
        prec = st["desk_right"] / tot if tot else None
        # a confusion that adds or drops a letter ("enfants" -> "enfans") needs the desk's proof;
        # any other needs ten words in this book, and the desk not against it
        indel = not ab[0] or not ab[1]
        if prec is not None and tot >= 3 and prec < 0.9:
            state = "off"
        elif indel:
            state = "on" if prec is not None and tot >= 5 and prec >= 0.95 else "off"
        elif st["words"] >= 10 and (prec is None or tot < 3 or prec >= 0.9):
            state = "on"
        elif st["words"] >= 3:
            state = "flag"
        else:
            state = "off"
        traits[ab] = state
        res["traits"].append({"wrong": ab[0], "right": ab[1], "state": state, "precision": prec, **st})
    # 2. every rule of the library, gated by those traits
    for r in library:
        if r["kind"] in ("word", "stealth", "suspect"):
            state, st = profile_word_rule(r, ev, traits)
        elif r["kind"] == "normalize":
            state, st = "off", {"why": "a normalization: never applied to a faithful text"}
        elif r["kind"] == "house":
            state, st = "on", {"why": "the house's own rule, measured on Adam's answers"}
        else:
            continue
        res["summary"][(r["source"], r["kind"], state)] += 1
        if state != "off" or r["source"] == "house":
            res["rules"][r["id"]] = {"state": state, **{k: r[k] for k in ("kind", "match", "source", "file") if k in r},
                                    "replace": r.get("replace"), **st}
    res["summary"] = {f"{a}/{b}/{c}": v for (a, b, c), v in sorted(res["summary"].items())}
    return res


def fixer(prof, ev):
    """The profile as a function: word -> (fixed word, rule) or None. Only rules `on`; a character
    confusion only when the word is no word and the confusion gives exactly one word."""
    words = {}
    for rid, r in prof["rules"].items():
        if r["state"] == "on" and r["kind"] in ("word", "stealth") and r.get("replace"):
            words.setdefault(r["match"].lower(), (r["replace"], rid))
    active = [(t["wrong"], t["right"]) for t in prof["traits"] if t["state"] == "on"]

    def fix(token):
        # half a word broken at the margin is no word to fix ("Anto-" is Anto-nio); a word whose
        # trouble is the æ ("Ccsar" is Cæsar) is the ligature rule's, not a confusion's
        if token.rstrip(".,;:)]”’'\"").endswith("-") or re.search(r"(?i)\bc[cs]?sar|\bc[ce]sar", token):
            return None
        core = letters(token)
        if not core:
            return None
        lw = core.lower()
        if lw in words:
            cand, rid = words[lw]
        else:
            cand, rid = misread(lw, active, ev), "char"
        if not cand:
            return None
        # a name the book prints cleanly ("Hugo", which a borrowed rule turns into "huge") is left
        # alone, unless the correction is the book's habit ("Chureh" beside a hundred "Church")
        if core[:1].isupper() and ev.clean[lw] >= 2 and ev.all[cand.lower()] < 3 * ev.all[lw]:
            return None
        return token.replace(core, _recase(core, cand), 1), rid
    return fix


# ---------------------------------------------------------------- command line


def add_parser(sub):
    f = sub.add_parser("fixes", help="the fix library: fetch, build, profile a book")
    fs = f.add_subparsers(dest="fcmd", required=True)
    fs.add_parser("fetch", help="the pinned sources -> data/fixes/src/")
    fs.add_parser("build", help="-> data/fixes/library.jsonl")
    p = fs.add_parser("profile", help="which fixes are in play for a book's typesetting")
    p.add_argument("--book", required=True, help="an unscanner work dir (its book.json)")
    p.add_argument("--review", help="review.json from editions collate (the desk)")
    p.add_argument("--answers", nargs="*", default=[], help="answers settled by a person or Claude's eyes")
    p.add_argument("--brewer", help="Brewer's Dictionary paragraphs, added to the lexicon")
    p.add_argument("--text", help="merged.json from editions merge: count words after rejoining")
    p.add_argument("--out", help="default: <book>/fixes-profile.json")


def dispatch(a):
    if a.fcmd == "fetch":
        fetch()
    elif a.fcmd == "build":
        build()
    elif a.fcmd == "profile":
        from . import editions as E
        from .editions_cli import _answers
        book = json.load(open(os.path.join(a.book, "book.json"), encoding="utf-8"))
        lexicon = {w.lower() for w in E.load_lexicon(REPO, a.brewer)}
        truth = None
        if a.review:
            ans = {}
            for path in a.answers:
                ans.update(_answers(path))
            truth = desk_truth(json.load(open(a.review, encoding="utf-8")), ans)
        texts = None
        if a.text:
            texts = [g["text"] for g in json.load(open(a.text, encoding="utf-8"))["paragraphs"]]
        prof = profile(book, lexicon, load_library(), truth, texts)
        out = a.out or os.path.join(a.book, "fixes-profile.json")
        json.dump(prof, open(out, "w"), ensure_ascii=False, indent=0)
        on = sum(1 for r in prof["rules"].values() if r["state"] == "on")
        fl = sum(1 for r in prof["rules"].values() if r["state"] == "flag")
        print(f"{on} rules in play, {fl} flagged for a person; traits of this typeface:")
        for t in prof["traits"][:15]:
            pr = "" if t["precision"] is None else f", desk {t['precision']:.0%}"
            print(f"  {t['state']:4} {t['wrong']!r} read for {t['right']!r}: {t['words']} words{pr}  e.g. {', '.join(t['examples'][:3])}")
        print("->", out)
