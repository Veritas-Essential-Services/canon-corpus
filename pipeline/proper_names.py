#!/usr/bin/env python3
# prov: 2026-09-26 claude-opus-5-5 drafted (from git trailer; backfilled 2026-09-30)
# fable_review: pending
"""
proper_names.py -- the house table of proper names for the Latin lemma
spine: the biblical names of the Clementine Vulgate, each form the text
writes mapped to its name lemma, part of speech `proper`.

    python3 pipeline/benchmark_whitaker.py --fetch  # the Vulgate (once; gitignored)
    python3 pipeline/proper_names.py --fetch        # Hitchcock's dictionary (once; gitignored)
    python3 pipeline/proper_names.py                # build and write the table
    python3 pipeline/proper_names.py --check        # rebuild; committed files byte-identical

    In:   data/corpus/benchmark/clementine/<commit[:12]>/*.lat  (pinned by benchmark_whitaker)
          data/corpus/hitchcock/bible_names.xml                (pinned below)
          the Whitaker files (build_lemma_spine.py --fetch)
    Out:  data/lemmas/proper-names/names.jsonl   COMMITTED. One row per name lemma.
          data/lemmas/proper-names/manifest.json COMMITTED. Sources, licences,
                                                 method, counts, checksum.

WHY
    WORDS was never meant to hold proper names, and the Vulgate benchmark
    (docs/review/2026-09-26-benchmark.md) found that nearly all it cannot
    read are names: about 3,300 forms, 17,000 tokens. The analyzer consults
    this table for a capitalised form, beside WORDS's own dictionary lookup
    (whitaker_tricks.parse_latin_word); it is loaded only when asked for.

HOW THE TABLE IS MADE (mechanically; nothing here is typed by hand)
    1. Candidates. A form (lower-cased, as benchmark_whitaker counts it) is
       a candidate when the Vulgate
         * never writes it lower-case, and
         * writes it capitalised at least once in mid-sentence, i.e. after a
           word, comma or semicolon of the same verse, not at the start of a
           verse or after . : ? ! ( ) / \\ [ ] or a speaker label, where a
           common word would be capitalised too; and
       WORDS (the port with every rule, state D of the benchmark, no
       capitalisation rule) has no plain reading of it. A form that is a
       candidate plus -que, when that candidate is in the table, is left
       out: the lookup takes the enclitic off, as WORDS does.
    2. Lemmas, from the Vulgate's own inflected forms. A candidate n that
       ends in a nominative ending N of the house table ENDINGS (standard
       Latin endings, e.g. -as with -ae, -am, -an, -a) heads a paradigm when
       another candidate is n's stem plus one of N's other endings
       (Jonathas: Jonathae, Jonatham, Jonatha). Nominative classes are
       tried in ENDINGS's order, and a form already taken as another
       name's oblique form never heads a later class (Jonatha is Jonathas's
       ablative, not a first-declension nominative). A form that is itself a
       headword in Hitchcock, letter for letter (the EXACT tier below), is
       never taken as another name's oblique form (Elam is not Ela's accusative;
       Gadi is not Gad's genitive). A form claimed by two nominatives keeps
       both (Michae: Michas and Micha). A candidate no nominative claims is its
       own lemma, "one form" (Aaron, 322 tokens, always so written).
       The lemma is the nominative as the text most often writes it,
       diacritics off and ligatures opened, j and v kept (Jonathas, Israel).
       No nominative is ever supplied that the text does not write.
    3. Hitchcock. Each lemma is looked up in Hitchcock's Bible Names
       Dictionary (1869), whose headwords are the King James spellings:
         exact     the same letters, case and hyphens aside;
         spelling  the same after the regular Latin/English correspondences
                   (j=i=y, v=u, ae=oe=e, ph=f, th=t, sh=s, ch=c, k=c, z=s,
                   doubled letters single, a final h dropped);
         ending    the same after a Latin nominative -s or -us, -um is taken
                   off (Ezechias ~ Hezekiah is NOT reached: e/he differ);
       the first tier that finds anything is kept, with every headword it
       finds. The row carries Hitchcock's headword, his entry id and his
       own gloss of the name, verbatim; nothing is added to it. A lemma
       with no match has `hitchcock: []`; it is still a name by step 1.

SOURCES AND LICENCES (recorded in the manifest)
    * The Clementine Vulgate: public domain (benchmark_whitaker.LICENCE).
      Forms and counts only; no running text is copied.
    * Hitchcock's Bible Names Dictionary, from Hitchcock's New and Complete
      Analysis of the Holy Bible (New York: A. J. Johnson, 1874, c1869), as
      the Christian Classics Ethereal Library publishes it (ThML), pinned by
      sha256. Public domain: the file's own DC.Rights says so, and the book
      is from 1869/1874.
"""

import argparse
import collections
import hashlib
import html
import json
import os
import re
import sys
import unicodedata
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import whitaker as W  # noqa: E402

OUT = os.path.join(ROOT, "data", "lemmas", "proper-names")
NAMES = os.path.join(OUT, "names.jsonl")
SCHEMA = "wordhoard/proper-names/v1"
COMMITTED = ("names.jsonl", "manifest.json")

HITCHCOCK_URL = "https://ccel.org/ccel/h/hitchcock/bible_names.xml"
HITCHCOCK_SHA256 = "43390f72248bb3687cc69598b4dc6fd80dc6e406225eed3cd05e66594386d836"
HITCHCOCK_CACHE = os.path.join(ROOT, "data", "corpus", "hitchcock", "bible_names.xml")
HITCHCOCK_LICENCE = {
    "license": "public-domain",
    "work": "Hitchcock's Bible Names Dictionary",
    "author": "Roswell D. Hitchcock",
    "printed": ("From Hitchcock's New and Complete Analysis of the Holy Bible, New York: "
                "A. J. Johnson, 1874, c1869, pp. 1104-1113 (the file's printSourceInfo)"),
    "edition": "Christian Classics Ethereal Library, ThML, bookID bible_names (digitized by Brad Haugaard)",
    "url": HITCHCOCK_URL,
    "sha256": HITCHCOCK_SHA256,
    "evidence": "the file's own <DC.Rights>Public Domain</DC.Rights>; the book was printed 1869/1874",
    "verified_on": "2026-09-26",
    "used_for": "headword, entry id and the name's gloss, verbatim, as provenance for each lemma",
}

# Sentence boundaries for step 1: after these, a common word is capitalised too.
BOUNDARY = set(".:?!()/\\[]")
TOKEN = re.compile(r"[^\W\d_]+|[.:?!;,()/\\\[\]]")

# Step 2: the house's table of Latin nominative endings and the endings the
# other forms of the same paradigm take. Standard Latin grammar, nothing
# else; the ORDER decides which class a form is claimed by first.
ENDINGS = (
    # (nominative, the other endings, class, what the head must satisfy)
    ("us", ("i", "o", "um", "e", "orum", "is", "os"), "2nd declension, -us", None),
    ("as", ("ae", "am", "an", "a"), "1st declension, -as", None),
    ("", ("is", "i", "em", "e"), "3rd declension, consonant stem", "consonant"),
    ("es", ("is", "i", "em", "en", "e", "ae"), "-es (1st or 3rd declension)", "consonant"),
    ("is", ("i", "em", "im", "e", "idis", "idi", "idem", "ide"), "3rd declension, -is", "consonant"),
    ("a", ("ae", "am", "arum", "is", "as"), "1st declension, -a", None),
    ("am", ("ae",), "-am, genitive/dative -ae (Abraham, Abrahae)", "hitchcock"),
    ("e", ("es", "en"), "1st declension, Greek -e", None),
    ("i", ("orum", "is", "os"), "2nd declension, plural", None),
    ("ae", ("arum", "is", "as"), "1st declension, plural", None),
)
# What a head must satisfy: "consonant", its stem ends in a consonant (so
# Nathinaeis, a dative plural, is never an -is nominative, nor Jojada a
# consonant stem); "hitchcock", it is itself a name in Hitchcock (so
# Jerosolymam, an accusative, never heads the -am class; Abraham does).
VOWELS = set("aeiouy")
ENCLITICS = ("que",)


# ---------------------------------------------------------------------------
# Hitchcock
# ---------------------------------------------------------------------------

def fetch_hitchcock(path=HITCHCOCK_CACHE):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print(f"  fetch {HITCHCOCK_URL}")
        with urllib.request.urlopen(HITCHCOCK_URL, timeout=120) as r:
            blob = r.read()
        with open(path + ".tmp", "wb") as f:
            f.write(blob)
        os.replace(path + ".tmp", path)
    verify_hitchcock(path)


def verify_hitchcock(path=HITCHCOCK_CACHE):
    if not os.path.exists(path):
        raise SystemExit(f"Hitchcock is not fetched ({path}); run proper_names.py --fetch")
    with open(path, "rb") as f:
        d = hashlib.sha256(f.read()).hexdigest()
    if d != HITCHCOCK_SHA256:
        raise SystemExit(f"HARD STOP: Hitchcock sha256 {d} != pinned {HITCHCOCK_SHA256}")


def read_hitchcock(path=HITCHCOCK_CACHE):
    """[{id, term, meaning}], in the file's order."""
    verify_hitchcock(path)
    with open(path, encoding="utf-8") as f:
        x = f.read()
    out = []
    for i, term, meaning in re.findall(r'<term id="([^"]+)">(.*?)</term>\s*<def id="[^"]+">(.*?)</def>', x, re.S):
        out.append({"id": i, "term": html.unescape(" ".join(term.split())),
                    "meaning": html.unescape(" ".join(re.sub(r"<[^>]+>", "", meaning).split()))})
    return out


def _plain(s):
    s = "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()
    return s.replace("æ", "ae").replace("œ", "oe")


def exact_key(s):
    return re.sub(r"[^a-z]", "", _plain(s))


def spelling_key(s):
    """The regular Latin/English correspondences of biblical names."""
    s = exact_key(s)
    for a, b in (("ae", "e"), ("oe", "e"), ("ph", "f"), ("th", "t"), ("sh", "s"), ("ch", "c")):
        s = s.replace(a, b)
    s = s.translate(str.maketrans("jyvkz", "iiucs"))
    s = re.sub(r"(.)\1+", r"\1", s)
    return s[:-1] if s.endswith("h") and len(s) > 2 else s


def ending_keys(s):
    k = spelling_key(s)
    return [k[:-len(e)] for e in ("us", "um", "s") if k.endswith(e) and len(k) > len(e) + 1]


class Hitchcock:
    def __init__(self, entries):
        self.entries = entries
        self.by = {"exact": collections.defaultdict(list), "spelling": collections.defaultdict(list)}
        for e in entries:
            self.by["exact"][exact_key(e["term"])].append(e)
            self.by["spelling"][spelling_key(e["term"])].append(e)

    def is_name(self, form):
        """Hitchcock has this very spelling as a headword (exact tier only:
        at the spelling tier Jeremia, Jeremias's ablative, would be
        Jeremiah)."""
        return bool(self.by["exact"].get(exact_key(form)))

    def match(self, lemma):
        """(tier, [entries]) for the first tier that finds anything."""
        for tier, key in (("exact", exact_key(lemma)), ("spelling", spelling_key(lemma))):
            got = self.by[tier].get(key)
            if got:
                return tier, got
        got = []
        for k in ending_keys(lemma):
            got += [e for e in self.by["spelling"].get(k, ()) if e not in got]
        return ("ending", got) if got else (None, [])


# ---------------------------------------------------------------------------
# The Vulgate census (step 1)
# ---------------------------------------------------------------------------

def census(B):
    """Per form: tokens, whether ever lower-case, capitalised mid-sentence
    tokens, and the written spellings of its capitalised tokens."""
    counts, lower = collections.Counter(), set()
    mid, written = collections.Counter(), collections.defaultdict(collections.Counter)
    for b in B.BOOKS:
        with open(os.path.join(B.CACHE, b + ".lat"), encoding="cp1252") as f:
            for line in f:
                line = B.SPEAKER.sub(" . ", B.REF.sub("", line))
                prev = "."
                for t in TOKEN.findall(line):
                    if not t[0].isalpha():
                        prev = t
                        continue
                    form = B.raw_form(t)
                    counts[form] += 1
                    if t[:1].islower():
                        lower.add(form)
                    else:
                        written[form][t] += 1
                        if prev not in BOUNDARY:
                            mid[form] += 1
                    prev = t
    return counts, lower, mid, written


def lemma_spelling(written):
    """The commonest written spelling, diacritics off, ligatures opened, case
    and j/v kept (ties: alphabetical)."""
    t = sorted(written.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    t = "".join(c for c in unicodedata.normalize("NFD", t) if not unicodedata.combining(c))
    return t.replace("Æ", "Ae").replace("æ", "ae").replace("Œ", "Oe").replace("œ", "oe")


def candidates(B, X, counts, lower, mid):
    """Step 1. Returns ({form: status in state D}, [forms left out as
    enclitic], {form: status} of the forms held back: never lower-case, not
    read plainly, but capitalised only where any word would be)."""
    X.use_tackons = X.use_roman = X.use_packons = True
    X.use_caps = False
    X.names = {}
    import whitaker_tricks as T
    out, held = {}, {}
    for form in sorted(counts):
        if form in lower:
            continue
        st = B.classify([X._describe(a) for a in T.parse_latin_word(X, W.fold(form), raw=form)])[0]
        if st != "plain":
            (out if mid.get(form) else held)[form] = st
    encl = sorted(f for f in out for t in ENCLITICS if f.endswith(t) and f[:-len(t)] in out)
    for f in encl:
        del out[f]
    return out, encl, held


# ---------------------------------------------------------------------------
# Paradigms (step 2)
# ---------------------------------------------------------------------------

def paradigms(forms, hitchcock):
    """{nominative: (class index, [its other forms])} and {form: [nominatives]}."""
    fs = set(forms)
    heads, claims = {}, collections.defaultdict(list)
    for ci, (nom, others, _, cond) in enumerate(ENDINGS):
        for n in sorted(fs):
            if n in claims or n in heads or not n.endswith(nom) or len(n) <= len(nom) + 1:
                continue
            stem = n[:len(n) - len(nom)] if nom else n
            if cond == "consonant" and stem[-1] in VOWELS:
                continue
            if cond == "hitchcock" and not hitchcock.is_name(n):
                continue
            members = [stem + e for e in others
                       if stem + e in fs and stem + e != n and stem + e not in heads
                       and not hitchcock.is_name(stem + e)]
            if members:
                heads[n] = (ci, members)
                for m in members:
                    claims[m].append(n)
    return heads, claims


def build_rows(counts, mid, written, cands, hitchcock):
    heads, claims = paradigms(cands, hitchcock)
    lemmas = collections.OrderedDict()
    for f in sorted(cands):
        if f in heads:
            lemmas.setdefault(f, set()).add(f)
        elif f in claims:
            for n in claims[f]:
                lemmas.setdefault(n, set()).add(f)
        else:
            lemmas.setdefault(f, set()).add(f)
    rows = []
    for n in sorted(lemmas, key=lambda k: (W.fold(k), k)):
        forms = sorted(lemmas[n] | {n}, key=lambda k: (-counts[k], k))
        lemma = lemma_spelling(written[n])
        tier, hits = hitchcock.match(lemma)
        ci = heads[n][0] if n in heads else None
        nom = ENDINGS[ci][0] if ci is not None else None
        stem = (n[:len(n) - len(nom)] if nom else n) if ci is not None else None
        rows.append({
            "lemma": lemma,
            "headword": W.fold(lemma),
            "pos": "proper",
            "paradigm": ENDINGS[ci][2] if ci is not None else "one form",
            "forms": {f: {"tokens": counts[f], "mid_sentence": mid[f],
                          "ending": (f[len(stem):] if stem is not None and f.startswith(stem) else None),
                          "shared": len(claims.get(f, ())) > 1 or None}
                      for f in forms},
            "tokens": sum(counts[f] for f in forms),
            "hitchcock": [{"term": e["term"], "id": e["id"], "match": tier, "meaning": e["meaning"]} for e in hits],
        })
    for r in rows:
        for v in r["forms"].values():
            if v["shared"] is None:
                del v["shared"]
            if v["ending"] is None:
                del v["ending"]
    return rows, heads, claims


# ---------------------------------------------------------------------------
# Build, check, load
# ---------------------------------------------------------------------------

def serialize(rows):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")


def build():
    import benchmark_whitaker as B
    d = B.digest()
    if d != B.PIN:
        raise SystemExit(f"HARD STOP: Clementine text digest {d} != pinned {B.PIN}")
    hc = Hitchcock(read_hitchcock())
    counts, lower, mid, written = census(B)
    X = W.Whitaker()
    cands, encl, held = candidates(B, X, counts, lower, mid)
    rows, heads, claims = build_rows(counts, mid, written, cands, hc)
    blob = serialize(rows)
    status = collections.Counter(cands.values())
    tiers = collections.Counter((r["hitchcock"][0]["match"] if r["hitchcock"] else "none") for r in rows)
    par = collections.Counter(r["paradigm"] for r in rows)
    never_lower = [f for f in counts if f not in lower]
    manifest = {
        "schema": SCHEMA,
        "doc": "pipeline/README-lemma-spine.md s.10; method in pipeline/proper_names.py",
        "language": "la",
        "provenance": "house",
        "pos": "proper",
        "row_evidence": ("every form of every row: never written lower-case in the Vulgate, capitalised "
                         "there in mid-sentence (`mid_sentence` tokens), and read plainly by no WORDS entry; "
                         "a row's other forms are its nominative's stem plus an ending of its class"),
        "sources": {
            "vulgate": {"repo": B.REPO_URL, "commit": B.COMMIT, "path": "src/iso-encoded/*.lat",
                        "digest_sha256": d, **B.LICENCE,
                        "used_for": "which forms are names (step 1) and their inflected forms (step 2): forms and counts only"},
            "hitchcock": HITCHCOCK_LICENCE,
            "whitaker": {"commit": W.COMMIT, "license": W.LICENCE["license"],
                         "used_for": "only to leave out forms WORDS already reads plainly; nothing of it is copied"},
        },
        "method": {
            "boundary_marks": "".join(sorted(BOUNDARY)),
            "endings": [{"nominative": "-" + n if n else "(bare)", "others": list(o), "class": c,
                         "head_must": cond} for n, o, c, cond in ENDINGS],
            "enclitics_left_to_lookup": list(ENCLITICS),
            "hitchcock_tiers": ["exact", "spelling", "ending"],
        },
        "counts": {
            "vulgate_forms": len(counts),
            "never_lower_case": len(never_lower),
            "candidates": len(cands),
            "candidate_tokens": sum(counts[f] for f in cands),
            "candidates_by_state_D": dict(sorted(status.items())),
            "left_to_the_enclitic_lookup": len(encl),
            "lemmas": len(rows),
            "lemmas_by_paradigm": dict(sorted(par.items(), key=lambda kv: -kv[1])),
            "lemmas_by_hitchcock_match": dict(sorted(tiers.items(), key=lambda kv: -kv[1])),
            "forms_with_two_lemmas": sum(1 for f, n in claims.items() if len(n) > 1),
            "held_back_capitalised_only_at_a_boundary": len(held),
            "held_back_tokens": sum(counts[f] for f in held),
        },
        "held_back": [{"form": f, "tokens": counts[f], "state_D": held[f]}
                      for f in sorted(held, key=lambda f: (-counts[f], f))],
        "left_to_the_enclitic_lookup": encl,
        "files_sha256": {"names.jsonl": hashlib.sha256(blob).hexdigest()},
    }
    blobs = {"names.jsonl": blob,
             "manifest.json": (json.dumps(manifest, ensure_ascii=False, indent=1) + "\n").encode("utf-8")}
    return blobs, manifest


def load(path=NAMES):
    """{search key: [analysis]} for whitaker_tricks.names_lookup: every form
    of every row, as a `proper` reading of its lemma."""
    out = {}
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            r = json.loads(line)
            name = {"lemma": r["lemma"], "headword": r["headword"],
                    "source": f"proper-names/names.jsonl:{n}"}
            for form in r["forms"]:
                out.setdefault(W.fold(form), []).append(
                    {"entry": None, "unique": None, "name": name, "parse": {"pos": "proper"}})
    return out


def write_atomic(path, blob):
    with open(path + ".tmp", "wb") as f:
        f.write(blob)
    os.replace(path + ".tmp", path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="fetch Hitchcock (pinned)")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch_hitchcock()
    blobs, man = build()
    for k, v in man["counts"].items():
        print(f"  {k:<42}{v if not isinstance(v, dict) else json.dumps(v)}")
    if a.check:
        stale = [fn for fn in COMMITTED if not os.path.exists(os.path.join(OUT, fn))
                 or open(os.path.join(OUT, fn), "rb").read() != blobs[fn]]
        if stale:
            raise SystemExit(f"CHECK FAILED: rebuilt output differs from committed: {stale}")
        print("  CHECK PASSED: committed proper-names files byte-identical.")
        return
    os.makedirs(OUT, exist_ok=True)
    for fn, blob in blobs.items():
        write_atomic(os.path.join(OUT, fn), blob)
    print(f"  wrote {OUT}")


if __name__ == "__main__":
    main()
