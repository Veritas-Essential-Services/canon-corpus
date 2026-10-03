#!/usr/bin/env python3
"""
tag_fathers.py -- every word of the Greek and Latin fathers keyed to a
dictionary entry, and every scripture reference in their editors' notes
resolved to a KJV verse. Each tag and each link carries the id of the rule
that made it.

    python3 pipeline/tag_fathers.py            # tag the books built here -> build/fathers/ + data/fathers/
    python3 pipeline/tag_fathers.py --check    # rebuild in memory: = the committed data/fathers/ files
    python3 pipeline/tag_fathers.py <slug>...  # only these books (writes nothing committed)

INPUT. The books structure_texts.py builds (data/books/<slug>.json,
gitignored): the First1KGreek fathers and Cramer's catenae (`-grc`), and the
CSEL and Oehler Latin fathers (`-lat`). Plus, built locally from their pins:
the Greek NT (rebuild_bible.py) for the Greek, and Lewis & Short with
Whitaker's WORDS (build_latin_key.py --fetch, build_lemma_spine.py --fetch)
for the Latin.

GREEK: a Strong's number, by build_apostolic_fathers.tag_word's fixed rules
against the Greek NT (nt-form, nt-form-nu, nt-form-major, nt-key, headword;
else null: ambiguous, unseen, latin). Nothing here is new; the rules are the
Apostolic Fathers' own, so a word gets the same number in Clement of Rome and
in Clement of Alexandria.

LATIN: a Lewis & Short entry key, by build_latin_key's machinery: WORDS reads
the form, its lemma is linked to L&S by headword and word class, and where
WORDS allows several entries the context rules remove readings until one
is left or none can be removed (the rule list is build_latin_key's,
README-latin-key.md s.4b). A token's rule is `sure`
(one reading), the "+"-joined context rules that settled it, or null with
why: `several` (readings left), `no-ls` (WORDS reads it, L&S has no entry),
`unread` (WORDS cannot read it: OCR damage, a Greek word, a name).

SCRIPTURE: fathers_scripture.py (its docstring has the rules). Cramer's
catenae need none: every comment there already sits on its verse
(place_catena.py), and those links are counted, not re-read.

WHAT IS COMMITTED (rule 6). The tokens are the text itself, and the TEI is
CC BY-SA: they go to build/fathers/<slug>.json, gitignored, beside the books
they come from, with build/fathers/scripture-links.jsonl (one row per unit:
its links to KJV verses, each with its rule). Like the Bible shards, these
are rebuilt, not committed. Committed: data/fathers/manifest.json (per book
the sha256 of the book read and of the tags written, the counts by rule; the
links file's sha256), so --check proves a rebuild is the same.
"""
import collections
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fathers_scripture as FS  # noqa: E402
import versification as VM  # noqa: E402

BOOKS = os.path.join(ROOT, "data", "books")
OUT = os.path.join(ROOT, "build", "fathers")
DATA = os.path.join(ROOT, "data", "fathers")
LINKS_FILE = os.path.join(OUT, "scripture-links.jsonl")
MANIFEST_FILE = os.path.join(DATA, "manifest.json")


def slugs():
    with open(os.path.join(BOOKS, "manifest.json"), encoding="utf-8") as f:
        m = json.load(f)
    grc = sorted(s for s in m if s.endswith("-grc"))
    lat = sorted(s for s in m if s.endswith("-lat"))
    return grc, lat


def load_book(slug):
    p = os.path.join(BOOKS, f"{slug}.json")
    with open(p, "rb") as f:
        blob = f.read()
    return json.loads(blob), hashlib.sha256(blob).hexdigest()


def scripture_context(numbering=False):
    """The KJV ids and the maps; with `numbering`, also each edition's
    measured OT numbering (data/fathers/numbering.json) and what reading a
    mixed edition reference by reference needs (Brenton's English, the
    Strong's glosses)."""
    with open(os.path.join(ROOT, "data", "uids", "wordhoard.uids.json"), encoding="utf-8") as f:
        kjv_ids = {k for k in json.load(f)["uids"] if k.startswith("kjv:")}
    ctx = {"kjv_ids": kjv_ids, "bmap": VM.load(VM.BRENTON_PATH), "vmap": VM.load(VM.VULGATE_PATH),
           "hmap": VM.load(VM.PATH)}
    if numbering:
        import fathers_numbering as FN
        ctx["numbering"] = FN.load()
        ctx["bren"] = FN.Brenton(ctx)
        ctx["glosses"] = FN.glosses()
    return ctx


def scripture(book, family, ctx, tokens=None):
    """{unit id: [links]} from the editors' notes and printed references,
    each OT reference read in the edition's measured numbering."""
    scheme = None
    if "numbering" in ctx:
        import fathers_numbering as FN
        scheme = FN.scheme_for(book, family, ctx["numbering"])
    out = {}
    for u in book["units"]:
        app = u.get("apparatus") or {}
        labels = [("note", n["text"]) for n in app.get("notes") or []] + \
                 [("refs", r) for r in app.get("refs") or []]
        if not labels:
            continue
        uw = None
        if tokens is not None and "glosses" in ctx:
            import fathers_numbering as FN
            uw = FN.unit_words(tokens.get(u["id"], []), ctx["glosses"])
        links = []
        for source, lab in labels:
            links += FS.links_for(lab, family, source, ctx, scheme, uw)
        if links:
            out[u["id"]] = links
    return out


# ---------------------------------------------------------------------------
# Greek: Strong's numbers by the Apostolic Fathers' rules
# ---------------------------------------------------------------------------

def tag_greek(book, tables, cache):
    import build_apostolic_fathers as A
    stats = collections.Counter()
    out = {}
    for u in book["units"]:
        row = []
        for m in A.WORD.finditer(u["text"]):
            w = m.group(0)
            if w not in cache:
                cache[w] = A.tag_word(w, tables)
            num, why = cache[w]
            stats[why] += 1
            row.append([w, num, why])          # why: the rule, or why there is no number
        out[u["id"]] = row
    return out, stats


# ---------------------------------------------------------------------------
# Latin: Lewis & Short keys by the Latin key's rules
# ---------------------------------------------------------------------------

class LatinKey:
    def __init__(self):
        import build_latin_key as L
        import proper_names
        import whitaker as W
        if not os.path.exists(L.LS_FILE) or L.sha256_file(L.LS_FILE) != L.LS["sha256"]:
            raise SystemExit("Lewis & Short missing or changed: python3 pipeline/build_latin_key.py --fetch")
        if not W.have_cache():
            raise SystemExit("WORDS missing: python3 pipeline/build_lemma_spine.py --fetch")
        self.L = L
        self.X = W.Whitaker(house_supplement=True)
        self.X.names = proper_names.load()
        self.links, self.by_head = L.whitaker_links(self.X, L.read_ls())
        self.sources = {"lewis-short": L.LS, "whitaker": W.COMMIT}

    def tag(self, book):
        form_rows, _, _, token_rows, _ = self.L.build_vulgate(self.X, self.links, self.by_head,
                                                              book["units"])
        status = {r["form"]: r["status"] for r in form_rows}
        stats = collections.Counter()
        out = {}
        for u, row in zip(book["units"], token_rows):
            toks = []
            for form, key, rule in row["tokens"]:
                why = ("sure" if key and not rule else rule if key else
                       status[form] if status[form] in ("no-ls", "unread") else "several")
                stats[why] += 1
                toks.append([form, key, why])
            out[u["id"]] = toks
        return out, stats


def blob_of(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")


def write_atomic(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "wb") as f:
        f.write(data)
    os.replace(path + ".tmp", path)


def link_rows(slug, sc):
    """One row per unit: its links, kjv: prefixes dropped (every target is a
    KJV verse); a link with no target is unresolved and says why."""
    rows = []
    for uid, links in sc.items():
        out = []
        for ln in links:
            d = {k: ln[k] for k in ("ref", "target", "through", "spans", "alt_target", "numbering",
                                    "read_as", "rule") if k in ln}
            for k in ("target", "through", "alt_target"):
                if k in d:
                    d[k] = d[k][4:]
            if "spans" in d:
                d["spans"] = [t[4:] for t in d["spans"]]
            if not ln.get("resolved"):
                d.pop("target", None)
                d["why"] = ln.get("why", "?")
            out.append(d)
        rows.append({"unit": uid, "links": out})
    return rows


def run(only=None):
    grc, lat = slugs()
    if only:
        grc = [s for s in grc if s in only]
        lat = [s for s in lat if s in only]
    ctx = scripture_context(numbering=True)
    entries, rows = {}, []
    if grc:
        import build_apostolic_fathers as A
        tables = A.tag_tables()
        cache = {}
        for slug in grc:
            book, sha = load_book(slug)
            tokens, stats = tag_greek(book, tables, cache)
            catena = slug.startswith("catena-")
            sc = {} if catena else scripture(book, "grc", ctx, tokens)
            entries[slug] = summarise(slug, sha, tokens, stats, sc, book, "strongs")
            rows += link_rows(slug, sc)
            data = blob_of({"slug": slug, "book_sha256": sha, "key": "strongs",
                            "tokens": tokens, "scripture": sc})
            write_atomic(os.path.join(OUT, f"{slug}.json"), data)
            entries[slug]["tags_sha256"] = hashlib.sha256(data).hexdigest()
            print(f"  {slug:52} {sum(stats.values()):>8} words  {entries[slug]['tagged_share']:6.1%} "
                  f"tagged  {entries[slug]['scripture']['resolved']:>6} refs")
    if lat:
        K = LatinKey()
        for slug in lat:
            book, sha = load_book(slug)
            tokens, stats = K.tag(book)
            sc = scripture(book, "lat", ctx)
            entries[slug] = summarise(slug, sha, tokens, stats, sc, book, "lewis-short")
            rows += link_rows(slug, sc)
            data = blob_of({"slug": slug, "book_sha256": sha, "key": "lewis-short",
                            "tokens": tokens, "scripture": sc})
            write_atomic(os.path.join(OUT, f"{slug}.json"), data)
            entries[slug]["tags_sha256"] = hashlib.sha256(data).hexdigest()
            print(f"  {slug:52} {sum(stats.values()):>8} words  {entries[slug]['tagged_share']:6.1%} "
                  f"tagged  {entries[slug]['scripture']['resolved']:>6} refs")
    return entries, rows


TAGGED_GREEK = ("nt-form", "nt-form-nu", "nt-form-major", "nt-key", "headword")


def summarise(slug, sha, tokens, stats, sc, book, key):
    words = sum(stats.values())
    if key == "strongs":
        tagged = sum(stats[r] for r in TAGGED_GREEK)
    else:
        tagged = sum(v for r, v in stats.items() if r not in ("several", "no-ls", "unread"))
    links = [ln for v in sc.values() for ln in v]
    sres = collections.Counter(ln["rule"] for ln in links if ln.get("resolved"))
    catena = sum(1 for u in book["units"] for ln in u.get("links") or []
                 if ln.get("kind") == "scripture" and ln.get("target", "").startswith("kjv:"))
    e = {"key": key, "book_sha256": sha, "words": words, "tagged": tagged,
         "tagged_share": round(tagged / words, 4) if words else 0.0,
         "by_rule": dict(sorted(stats.items(), key=lambda kv: -kv[1])),
         "scripture": {"read": len(links), "resolved": sum(sres.values()),
                       "resolved_by_rule": dict(sorted(sres.items())),
                       "unresolved_by_why": dict(sorted(collections.Counter(
                           ln.get("why", "?") for ln in links if not ln.get("resolved")).items())),
                       "alt_target": sum(1 for ln in links if "alt_target" in ln),
                       "ot_by_numbering": dict(sorted(collections.Counter(
                           ln["numbering"] for ln in links if ln.get("resolved") and "numbering" in ln).items()))}}
    if catena:
        e["scripture"]["placed_on_verse"] = catena
    return e


def manifest(entries):
    grc = {k: v for k, v in entries.items() if v["key"] == "strongs"}
    lat = {k: v for k, v in entries.items() if v["key"] == "lewis-short"}

    def tot(es):
        w = sum(e["words"] for e in es.values())
        t = sum(e["tagged"] for e in es.values())
        r = collections.Counter()
        for e in es.values():
            r.update(e["by_rule"])
        return {"books": len(es), "words": w, "tagged": t, "tagged_share": round(t / w, 4) if w else 0,
                "by_rule": dict(sorted(r.items(), key=lambda kv: -kv[1])),
                "scripture_read": sum(e["scripture"]["read"] for e in es.values()),
                "scripture_resolved": sum(e["scripture"]["resolved"] for e in es.values())}
    return {
        "schema": "canon-corpus/fathers-tags/v1",
        "built_by": "pipeline/tag_fathers.py",
        "greek": {"key": "Strong's number (data/nt, Robinson's lemma numbers)",
                  "rules": "build_apostolic_fathers.tag_word: nt-form, nt-form-nu, nt-form-major, "
                           "nt-key, headword; null: ambiguous, unseen, latin",
                  **tot(grc)},
        "latin": {"key": "Lewis & Short entry key (lewis-short:<key>)",
                  "rules": "build_latin_key: sure, or the '+'-joined context rules that settled "
                           "it (README-latin-key.md s.4b, by_rule below); null: several, no-ls, "
                           "unread",
                  **tot(lat)},
        "scripture": {"rules": "fathers_scripture.py: note/<map> from a footnote, refs/<map> from a "
                               "printed bracketed reference; map = the edition's measured OT "
                               "numbering (fathers_numbering.py, data/fathers/numbering.json): "
                               "vulgate, brenton (the Septuagint's), bhs (the Hebrew's) or kjv (the English), and nt; "
                               "+content where an edition that mixes numberings was read by the "
                               "father's own words; +ocr-twin where Job/John was "
                               "read as its twin",
                      "file": "build/fathers/scripture-links.jsonl (gitignored; rebuilt)"},
        "not_claimed": [
            "A Greek word's number is the NT's reading of the same written form; the fathers' "
            "own senses are not read.",
            "A Latin key is settled only by WORDS's readings and the context rules; what they "
            "leave open stays null.",
            "The OT numbering is measured per editor and class of book (Psalms, Jeremiah, the "
            "rest), from the notes themselves (fathers_numbering.py); only in a Greek edition "
            "that mixes numberings is a note's quotation read on its own, by the father's words, "
            "and only where the numberings differ by chapter, where that vote is right 89% of "
            "the time. Where the other numbering names another verse it is kept as alt_target.",
            "The texts are OCR (CSEL, many First1KGreek files): a misread word is tagged as read.",
        ],
        "books": dict(sorted(entries.items())),
    }


def jsonl(rows):
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
                   for r in rows)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    entries, rows = run(set(args) if args else None)
    rows.sort(key=lambda r: r["unit"])
    links_text = jsonl(rows).encode("utf-8")
    m = manifest(entries)
    m["scripture"]["rows"] = len(rows)
    with open(os.path.join(DATA, "numbering.json"), "rb") as f:
        m["scripture"]["numbering_sha256"] = hashlib.sha256(f.read()).hexdigest()
    m["scripture"]["sha256"] = hashlib.sha256(links_text).hexdigest()
    man = (json.dumps(m, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    for fam in ("greek", "latin"):
        f = m[fam]
        print(f"  {fam}: {f['books']} books, {f['words']:,} words, {f['tagged_share']:.1%} tagged; "
              f"scripture {f['scripture_resolved']:,} resolved of {f['scripture_read']:,} read")
    if args:
        return
    if "--check" in sys.argv:
        same = [os.path.exists(MANIFEST_FILE) and open(MANIFEST_FILE, "rb").read() == man]
        print("  CHECK", "PASSED: byte-identical" if all(same) else "FAILED: differs")
        if not all(same):
            raise SystemExit(1)
        return
    write_atomic(LINKS_FILE, links_text)
    write_atomic(MANIFEST_FILE, man)


if __name__ == "__main__":
    main()
