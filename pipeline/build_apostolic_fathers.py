#!/usr/bin/env python3
"""
build_apostolic_fathers.py -- the Apostolic Fathers in Greek, Kirsopp Lake's
Loeb text (1912-13), from the First1KGreek TEI, as books in the house shape
({id, ref, text, links[]} per unit, extras under `lex`), cited by the
standard chapter.section.

    python3 pipeline/build_apostolic_fathers.py --fetch   # pinned TEI -> data/corpus/first1k/ (gitignored)
    python3 pipeline/build_apostolic_fathers.py           # build data/books/<slug>.json + manifest entries
    python3 pipeline/build_apostolic_fathers.py --check   # rebuild in memory: = the committed manifest entries
    python3 tests/apostolic_fathers_test.py               # the validator

WHAT IS COMMITTED (rule 6, the licence gate). Lake's Greek is public domain
(published 1912-13). First1KGreek's digital edition of it, the TEI, is
"Available under a Creative Commons Attribution-ShareAlike 4.0 International
License" (each file's <availability><licence>). So the books are built exactly
as the STEPBible lexicons are: the TEI lands in data/corpus/, the built books
in data/books/, both gitignored, and only the manifest entry is committed. Each
entry carries a `rights` block with `redistribute_whole: false`, so a consumer
sees the limit without opening the book.

IDENTITY. Nothing is minted. A unit id here is a CITATION (`1clement-lake:1.1`),
exactly as every other book in data/books/ has; Word Hoard uids for these
passages would be minted only on Adam's ruling (house style s.2).

CITATION. The standard one, from the TEI's own textparts: chapter.section;
Ignatius letter + chapter.section (`Ign. Eph. 1.1`); Hermas Vision, Mandate or
Similitude + chapter.section (`Herm. Sim. 9.1.1`), which is how Lake prints it.
A unit is a textpart with no textpart inside it. Where the source has no
sections (Mart. Pol.'s preface) the chapter is the unit, and the honesty field
says the resolution is "section, where the edition has one".

STRONG'S TAGS (where the existing tooling allows). The Fathers share most of
their vocabulary with the NT, but there is no Greek morphology here. So a word
gets a Strong's number by two fixed rules against the Greek NT already built
(data/nt/, Robinson's lemmas = Strong's numbers), on the NT's own search key
(accents, breathings and case dropped):

  nt-form    the same written form occurs in the NT, always under ONE Strong's number
  headword   the form is a Strong's headword (a dictionary form), under one number

Anything else is null: a form the NT reads under two numbers (ἡ / ἤ, both η)
is ambiguous without accents and morphology, and a word the NT never uses has
no Strong's number at all. Never a guess. The rule id rides with every tag.

SCRIPTURE REFERENCES. Lake's notes cite scripture, and First1KGreek keyed
each as a CTS URN. Both are read (pipeline/af_scripture.py): the note's own
words first, the URN as a cross-check, and every URN that disagrees with the
note kept as a flagged, unresolved link. OT references resolve through
Brenton's LXX -> KJV map (PR #9), NT references to the KJV verse directly.

NOT DONE HERE: Lightfoot & Harmer's English (1891, PD) is on CCEL, which this
environment cannot reach. It is listed under PENDING.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_nt_corpus as N  # noqa: E402
import af_scripture as S  # noqa: E402
import versification as VM  # noqa: E402

BOOKS = os.path.join(ROOT, "data", "books")
MANIFEST = os.path.join(BOOKS, "manifest.json")
T = "{http://www.tei-c.org/ns/1.0}"

F1K_REPO = "OpenGreekAndLatin/First1KGreek"
F1K_COMMIT = "03776b39f4047c5cff06f5296fae4b2bae4b08fb"
CACHE = os.path.join(ROOT, "data", "corpus", "first1k", F1K_COMMIT[:12])
SOURCE_URL = f"https://github.com/{F1K_REPO}/tree/{F1K_COMMIT}"

# slug, path in the repo, title, author, SBL abbreviation. sha256s: apostolic_fathers_pins.json
WORKS = [
    ("1clement-lake", "data/tlg1271/tlg001/tlg1271.tlg001.1st1K-grc1.xml",
     "First Epistle of Clement to the Corinthians", "Clement of Rome", "1 Clem."),
    ("2clement-lake", "data/tlg1271/tlg002/tlg1271.tlg002.1st1K-grc1.xml",
     "Second Epistle of Clement (an ancient homily)", "Anonymous (attributed to Clement of Rome)",
     "2 Clem."),
    ("ignatius-lake", "data/tlg1443/tlg001/tlg1443.tlg001.1st1K-grc1.xml",
     "The Seven Letters of Ignatius (middle recension)", "Ignatius of Antioch", "Ign."),
    ("polycarp-phil-lake", "data/tlg1622/tlg001/tlg1622.tlg001.1st1K-grc1.xml",
     "Epistle of Polycarp to the Philippians", "Polycarp of Smyrna", "Pol. Phil."),
    ("martyrdom-polycarp-lake", "data/tlg1484/tlg001/tlg1484.tlg001.1st1K-grc1.xml",
     "The Martyrdom of Polycarp", "Anonymous (the church at Smyrna)", "Mart. Pol."),
    ("didache-lake", "data/tlg1311/tlg001/tlg1311.tlg001.1st1K-grc1.xml",
     "The Didache (Teaching of the Twelve Apostles)", "Anonymous", "Did."),
    ("barnabas-lake", "data/tlg1216/tlg001/tlg1216.tlg001.opp-grc1.xml",
     "The Epistle of Barnabas", "Anonymous (attributed to Barnabas)", "Barn."),
    ("hermas-lake", "data/tlg1419/tlg001/tlg1419.tlg001.1st1K-grc1.xml",
     "The Shepherd of Hermas", "Hermas", "Herm."),
    ("diognetus-lake", "data/tlg0646/tlg004/tlg0646.tlg004.1st1K-grc1.xml",
     "The Epistle to Diognetus", "Anonymous", "Diogn."),
]
PINS_PATH = os.path.join(HERE, "apostolic_fathers_pins.json")

# Ignatius's letters in Lake's (and the TEI's) order; SBL abbreviations.
IGNATIUS = {"1": "Eph", "2": "Magn", "3": "Trall", "4": "Rom", "5": "Phld", "6": "Smyrn", "7": "Pol"}
# Hermas: the TEI numbers Lake's 27 parts straight through; Lake prints them as
# Visions 1-5, Mandates 1-12, Similitudes 1-10, chapters restarting in each.
HERMAS = {str(i): ("Vis", i) for i in range(1, 6)}
HERMAS.update({str(i): ("Mand", i - 5) for i in range(6, 18)})
HERMAS.update({str(i): ("Sim", i - 17) for i in range(18, 28)})

PENDING = [{
    "what": "Lightfoot & Harmer, The Apostolic Fathers (1891), English (public domain)",
    "where": "CCEL (ccel.org/ccel/lightfoot/fathers)",
    "why": "ccel.org is blocked from the cloud sessions that built this; fetch on Adam's machine",
}]

RIGHTS = {
    "license": "CC BY-SA 4.0 (the First1KGreek digital edition); the Greek text, "
               "Kirsopp Lake's Loeb edition (1912-13), is public domain",
    "attribution": "First1KGreek, Open Greek and Latin (opengreekandlatin.org), "
                   "digitizing K. Lake, The Apostolic Fathers (Loeb Classical Library)",
    "source_url": SOURCE_URL,
    "redistribute_whole": False,
}

SKIP = {T + "note", T + "head", T + "bibl"}
WORD = re.compile(r"[^\W\d_]+(?:[̓᾽᾿’ʼ'][^\W\d_]*)*", re.UNICODE)


def sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def pins():
    with open(PINS_PATH, encoding="utf-8") as f:
        return json.load(f)


def local(rel):
    return os.path.join(CACHE, *rel.split("/"))


def fetch():
    import pinned_fetch as F
    p = pins()
    F.fetch(F1K_REPO, F1K_COMMIT, [(rel, local(rel), p[rel]) for rel in p],
            ua="canon-corpus/apostolic-fathers")


def verify_pins():
    p = pins()
    bad = [rel for rel, want in p.items() if not os.path.exists(local(rel)) or sha256_file(local(rel)) != want]
    if bad:
        raise SystemExit(f"pinned inputs missing or changed: {bad[:3]}\n"
                         f"  run: python3 pipeline/build_apostolic_fathers.py --fetch")


def text_of(el):
    """The running text of a textpart: every child's text and tail, minus notes,
    heads and bibl (the editor's apparatus, not the author's words)."""
    out = [el.text or ""]
    for c in el:
        if c.tag not in SKIP:
            out.append(text_of(c))
        out.append(c.tail or "")
    return "".join(out)


def clean(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip()


# Lake prints Pol. Phil. 10-12 and 14, and Herm. Sim. 9.30.3-10.4.5, in Latin:
# the Greek is lost there. First1KGreek ran that Latin through its Greek
# beta-code converter, so `et in vobis` arrives as `ετ ιν ϝοβις` (and `q` as
# `#3` or θ, capital V as Ω). The map below puts the Latin back. It is a
# per-book rule (rule 2: the source file is never edited), applied only to a
# RUN of words carrying no Greek accent or breathing: Lake's Greek is fully
# accented, while a lone unaccented enclitic (τε, μου) inside Greek is left alone.
DEMANGLE = {"α": "a", "β": "b", "ξ": "c", "δ": "d", "ε": "e", "φ": "f", "γ": "g", "η": "h",
            "ι": "i", "κ": "k", "λ": "l", "μ": "m", "ν": "n", "ο": "o", "π": "p", "θ": "q",
            "ρ": "r", "σ": "s", "ς": "s", "τ": "t", "υ": "u", "ϝ": "v", "χ": "x", "ψ": "y",
            "ζ": "z", "ω": "w", "Ω": "V"}
GREEK_MARKS = {"\u0300", "\u0301", "\u0342", "\u0313", "\u0314", "\u0345"}
LATIN_RUN = 3


def _marked(word):
    return any(c in GREEK_MARKS for c in unicodedata.normalize("NFD", word))


def _latinize(word):
    w = unicodedata.normalize("NFD", word)
    out = "".join(DEMANGLE.get(c.lower() if c != "Ω" else c, c) if c.isalpha() else c for c in w)
    return unicodedata.normalize("NFC", out)


def restore_latin(text):
    """(text, latin word count): runs of >= LATIN_RUN unmarked words, or any word
    that only the converter could have made (ϝ, #3), turned back into Latin."""
    text = text.replace("#3", "θ")
    pieces = re.split(r"(\s+)", text)
    words = [i for i, p in enumerate(pieces) if WORD.search(p)]
    unmarked = [not _marked(pieces[i]) for i in words]
    latin = set()
    run = []
    for k, (i, um) in enumerate(zip(words, unmarked)):
        if um:
            run.append(i)
        if not um or k == len(words) - 1:
            if len(run) >= LATIN_RUN or any("ϝ" in pieces[j] for j in run):
                latin.update(run)
            run = []
    for i in latin:
        pieces[i] = _latinize(pieces[i])
    return "".join(pieces), len(latin)


def harvest_notes(el):
    """Each <bibl> in the textpart as Lake printed it (label) and as
    First1KGreek keyed it (CTS URNs); af_scripture.resolve_note reads them."""
    return [{"label": clean("".join(b.itertext())), "cts": (b.get("corresp") or "").split()}
            for b in el.iter(T + "bibl")]


def cite(slug, abbrev, parts):
    """(unit id, printed ref) from the textpart n's, outermost first."""
    ns = list(parts)
    if slug == "ignatius-lake":
        letter = IGNATIUS[ns[0]]
        return f"{letter}." + ".".join(ns[1:]), f"{abbrev} {letter}. " + ".".join(ns[1:])
    if slug == "hermas-lake":
        kind, num = HERMAS[ns[0]]
        rest = ".".join([str(num)] + ns[1:])
        return f"{kind}.{rest}", f"{abbrev} {kind}. {rest}"
    return ".".join(ns), f"{abbrev} " + ".".join(ns)


def leaves(div, path=()):
    kids = [c for c in div if c.tag == T + "div" and c.get("type") == "textpart"]
    here = path + ((div.get("n"),) if div.get("type") == "textpart" else ())
    if div.get("type") == "textpart" and not kids:
        yield here, div
    for k in kids:
        yield from leaves(k, here)


def convert(slug, rel, title, author, abbrev):
    root = ET.parse(local(rel)).getroot()
    lic = root.find(f".//{T}availability/{T}licence")
    licence = clean("".join(lic.itertext())) if lic is not None else ""
    if "Attribution-ShareAlike 4.0" not in licence:
        raise SystemExit(f"HARD STOP: {rel}: licence line is not the CC BY-SA 4.0 recorded "
                         f"({licence!r}); re-read the rights before building")
    edition = root.find(f".//{T}div[@type='edition']")
    units, seen = [], set()
    for path, div in leaves(edition):
        uid, ref = cite(slug, abbrev, path)
        if uid in seen:
            raise SystemExit(f"HARD STOP: {slug}: two textparts cite as {uid}")
        seen.add(uid)
        text, n_latin = restore_latin(clean(text_of(div)))
        if not text:
            continue
        unit = {"id": f"{slug}:{uid}", "ref": ref, "text": text, "links": harvest_notes(div)}
        if n_latin:
            unit["lang"] = "la" if not any(_marked(w) for w in WORD.findall(text)) else "grc+la"
        units.append(unit)
    return {"slug": slug, "title": title, "author": author,
            "source": {"path": os.path.relpath(local(rel), os.path.join(ROOT, "data", "corpus")),
                       "format": "tei-first1k", "edition": "K. Lake, The Apostolic Fathers "
                       "(Loeb, 1912-13)", "cts": edition.get("n"), "sha256": sha256_file(local(rel))},
            "scheme": {"citation": f"{abbrev} " + ("letter chapter.section" if slug == "ignatius-lake"
                                                   else "Vis./Mand./Sim. book.chapter.section"
                                                   if slug == "hermas-lake" else "chapter.section"),
                       "resolution": "section, where the edition has one",
                       "honesty": "exact to Lake's sections; the Greek is First1KGreek's OCR "
                                  "of the Loeb, corrected but not proofread here, and carries "
                                  "OCR slips (e.g. παῤ for παρ᾽)",
                       "note": "Text only: Lake's notes, heads and apparatus are left out of "
                               "`text`. His scripture references are in links[], resolved to "
                               "kjv: unit ids where the note and the map allow "
                               "(pipeline/af_scripture.py); the rest say why not."},
            "rights": dict(RIGHTS),
            "units": units}


def form_key(w):
    """The written form, compared as written: NFC, lower case, a grave accent read
    as the acute it stands for (Greek writes an acute as grave before another
    word), every elision mark as one, every sigma as σ."""
    w = unicodedata.normalize("NFD", w.lower()).replace("\u0300", "\u0301")
    for e in N.ELISION + "\u1fbd\u1fbf\u0313":
        if w.endswith(e):
            w = w[: -len(e)] + "\u2019"
    return unicodedata.normalize("NFC", w).replace("ς", "σ")


def tag_tables():
    """For each written form, each search key (accents dropped) and each
    headword: how often the NT reads it under each Strong's number."""
    nt = N.load_nt()
    forms, keys, heads = {}, {}, {}
    for t in nt["tokens"]:
        k = t.get("lemma_key")
        if not k:
            continue
        for table, key in ((forms, form_key(t["surface"])), (keys, t["search_key"])):
            table.setdefault(key, {}).setdefault(k, 0)
            table[key][k] += 1
        if t.get("lemma"):
            heads.setdefault(form_key(t["lemma"]), {}).setdefault(k, 0)
            heads[form_key(t["lemma"])][k] += 1
    return forms, keys, heads


RULES = ("nt-form", "nt-form-nu", "nt-form-major", "nt-key", "headword")
MAJOR_SHARE, MAJOR_MIN = 0.97, 20
NT_KEY_MIN = 4


def tag_word(w, tables):
    """(Strong's number or None, rule or why not). Rules in order; the first
    that knows the word decides, and an ambiguous answer is final:

      nt-form        the written form, read in the NT under one number only
      nt-form-nu     the same with a movable nu added (ἐστι -> ἐστιν, φησί -> φησίν)
      nt-form-major  the written form, read under one number at least 97% of at
                     least 20 times (αὐτοῦ: G846 1474, G847 4); the rule id says so
      nt-key         the form without accents, under one number only, for words of
                     4+ letters (in a short word the accent IS the word: ὄν is not ὅν)
      headword       the form is a Strong's headword, of one number only
    """
    if w.isascii():
        return None, "latin"
    forms, keys, heads = tables
    fk = form_key(w)
    seen = forms.get(fk)
    if not seen and N.search_key(w)[-1:] in ("ι", "ε"):
        nu = forms.get(fk + "ν")
        if nu and len(nu) == 1:
            return next(iter(nu)), "nt-form-nu"
    if seen:
        if len(seen) == 1:
            return next(iter(seen)), "nt-form"
        top, n = max(seen.items(), key=lambda kv: kv[1])
        total = sum(seen.values())
        if total >= MAJOR_MIN and n / total >= MAJOR_SHARE:
            return top, "nt-form-major"
        return None, "ambiguous"
    for rule, table, key in (("nt-key", keys, N.search_key(w)), ("headword", heads, fk)):
        if rule == "nt-key" and len(key) < NT_KEY_MIN:
            continue
        hit = table.get(key)
        if hit:
            return (next(iter(hit)), rule) if len(hit) == 1 else (None, "ambiguous")
    return None, "unseen"


def tag(book, tables):
    stats = {"words": 0, **{r: 0 for r in RULES}, "ambiguous": 0, "unseen": 0, "latin": 0}
    for u in book["units"]:
        toks = []
        for m in WORD.finditer(u["text"]):
            num, why = tag_word(m.group(0), tables)
            stats["words"] += 1
            stats[why] += 1
            toks.append([m.group(0), num, why if num else None])
        u.setdefault("lex", {})["tokens"] = toks
    book["tagging"] = {"scheme": "Strong's number by fixed rules against data/nt (tag_word: "
                                 "nt-form, nt-form-nu, nt-form-major, nt-key, headword); null "
                                 "when the answer is ambiguous, unseen, or Latin",
                       **stats}
    return book


def entry(book, blob):
    e = {"title": book["title"], "author": book["author"], "format": book["source"]["format"],
         "sha256": book["source"]["sha256"], "units": len(book["units"]),
         "scheme": book["scheme"], "rights": book["rights"]}
    e["tagging"] = {k: v for k, v in book["tagging"].items() if k != "scheme"}
    links = [x for u in book["units"] for x in u["links"]]
    e["scripture_refs"] = len(links)
    e["scripture_refs_resolved"] = sum(1 for x in links if x["resolved"])
    e["scripture_refs_flagged"] = sum(1 for x in links if x.get("source") == "urn" and not x["resolved"])
    e["built_sha256"] = hashlib.sha256(blob).hexdigest()
    return e


def build():
    verify_pins()
    tables = tag_tables()
    books = {slug: convert(slug, rel, title, author, abbrev) for slug, rel, title, author, abbrev in WORKS}
    ctx = scripture_context(books)
    out = {}
    for slug, book in books.items():
        for u in book["units"]:
            u["links"] = [x for note in u["links"] for x in S.resolve_note(note["label"], note["cts"], ctx, u["id"])]
        book = tag(book, tables)
        blob = json.dumps(book, ensure_ascii=False).encode("utf-8")
        out[slug] = (book, blob, entry(book, blob))
    return out


def scripture_context(books):
    with open(os.path.join(ROOT, "data", "uids", "wordhoard.uids.json"), encoding="utf-8") as f:
        kjv_ids = {k for k in json.load(f)["uids"] if k.startswith("kjv:")}
    return {"kjv_ids": kjv_ids, "bmap": VM.load(VM.BRENTON_PATH),
            "af_ids": {u["id"] for b in books.values() for u in b["units"]}}


def write_atomic(path, data):
    with open(path + ".tmp", "wb") as f:
        f.write(data)
    os.replace(path + ".tmp", path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    built = build()
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    tot = {"units": 0, "words": 0, "tagged": 0, "refs": 0}
    for slug, (book, blob, e) in built.items():
        t = e["tagging"]
        tagged = sum(t[r] for r in RULES)
        tot["units"] += e["units"]; tot["words"] += t["words"]
        tot["tagged"] += tagged; tot["refs"] += e["scripture_refs"]
        print(f"  {slug:<24}{e['units']:>5} units {t['words']:>7,} words "
              f"{100 * tagged / (t['words'] - t['latin']):5.1f}% of Greek tagged "
              f"{t['latin']:>5} Latin {e['scripture_refs']:>4} refs")
        tot["latin"] = tot.get("latin", 0) + t["latin"]
    print(f"  {'all':<24}{tot['units']:>5} units {tot['words']:>7,} words "
          f"{100 * tot['tagged'] / (tot['words'] - tot['latin']):5.1f}% of Greek tagged "
          f"{tot['latin']:>5} Latin {tot['refs']:>4} refs")
    for p in PENDING:
        print(f"  PENDING: {p['what']} -- {p['why']}")
    if a.report:
        return
    if a.check:
        bad = [s for s, (_, blob, e) in built.items() if manifest.get(s) != e
               or (os.path.exists(os.path.join(BOOKS, s + ".json"))
                   and open(os.path.join(BOOKS, s + ".json"), "rb").read() != blob)]
        if bad:
            raise SystemExit(f"CHECK FAILED: rebuilt books differ from the manifest: {bad}")
        print("  CHECK PASSED: every book = its committed manifest entry (built_sha256).")
        return
    for slug, (_, blob, e) in built.items():
        write_atomic(os.path.join(BOOKS, slug + ".json"), blob)
        manifest[slug] = e
    # The same serialization structure_texts.py writes, so other entries do not move.
    write_atomic(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    print(f"  wrote {len(built)} books + {len(manifest)}-entry manifest")


if __name__ == "__main__":
    main()
