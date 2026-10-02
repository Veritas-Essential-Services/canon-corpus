#!/usr/bin/env python3
# prov: 2026-10-02 claude-opus-5-5 drafted
# fable_review: pending
"""
build_strongs.py -- Strong's numbers as the shared key for biblical words.

    python3 pipeline/build_strongs.py            # build data/strongs/
    python3 pipeline/build_strongs.py --check    # rebuild in memory: byte-identical, 0 proposed
    python3 pipeline/build_strongs.py --adopt    # ONLY on Adam's ruling: proposals -> registry

Adam, 2026-10-02: "use Strong's ... as the source of truth for those words and
use the strongs numbering and save those beside the UID". Rules and the
reasoning behind each choice: pipeline/README-strongs.md.

WHAT IT WRITES (data/strongs/, all committed)
    strongs.jsonl         THE TABLE. One row per Strong's number, H1-H8674 and
                          G1-G5624, from Strong's own 1890 dictionaries (PD).
                          Every other file here, and every corpus that names a
                          Hebrew or Greek word, keys on its `strongs` field.
    proposed-uids.jsonl   One PROPOSED Word Hoard uid per Strong's word, its
                          citation `strongs:G26`. NOT in data/uids/: minting
                          ~14,000 identities is Adam's call (CLAUDE.md 3b).
                          `--adopt` copies them into the registry verbatim, so
                          a uid seen here is the uid he will get.
    witnesses.jsonl       Where each number is written up: Strong's own entry,
                          BDB, TBESG, LSJ, Thayer. Citations only, never text,
                          so the CC BY lexicons are pointed at, not copied.
    concordance.jsonl     Every passage uid each number occurs in, read from
                          the committed original-language corpora (data/nt/,
                          and data/ot/ once it lands).
    manifest.json         Sources, sha256s, counts, and what is not claimed.

THE KEY
    "G26", "H2617": prefix and the number with no leading zeros, exactly the
    form data/nt/ tokens already carry in `lemma_key` and structure_texts'
    strongs_id() emits. normalize() reads every spelling in the house
    (G0026, 26 with a language, G0001G extended, H1254a augmented) into it.

A PARTIAL RUN NEVER DELETES (the 2026-09-06 manifest lesson)
    A witness or corpus whose source is missing here is carried forward from
    the committed files, not dropped. The lexicon sources live in the
    gitignored data/corpus/; `python3 pipeline/fetch_sources.py` fetches them.
"""

import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import structure_texts as S  # noqa: E402
import wh_uid  # noqa: E402

OUT = os.path.join(ROOT, "data", "strongs")
REGISTRY = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")
LEX = os.path.join(S.CORPUS, "lexicons")
BOOKS = os.path.join(ROOT, "data", "books")

FILES = ("strongs.jsonl", "proposed-uids.jsonl", "witnesses.jsonl",
         "concordance.jsonl", "manifest.json")

CITATION_SLUG = "strongs"      # strongs:G26 -- the WORD; strongs-greek:G26 is its 1890 entry
KIND = "lexeme"
GREEK_MAX = S.GREEK_MAX
HEBREW_MAX = S.HEBREW_MAX

# The two dictionaries, pinned by the sha256 already recorded for them in
# data/books/manifest.json (fetched 2026-09-06; re-verified 2026-10-02).
SOURCES = {
    "strongs-hebrew": {
        "file": "strongs-hebrew.xml",
        "sha256": "a628f4f89f8bdaf2483fd3faf1abc8653cc6717758dfc9f24beb7571d9bdd0c4",
        "what": "Strong's Hebrew and Chaldee Dictionary (James Strong, 1890)",
        "transcription": "OpenScriptures HebrewLexicon, HebrewStrong.xml",
        "url": "https://github.com/openscriptures/HebrewLexicon",
        "rights": ("Dictionary text public domain (1890). The XML markup is CC BY 4.0 "
                   "(OpenScriptures); only the PD text fields are carried here, with "
                   "attribution."),
    },
    "strongs-greek": {
        "file": "strongs-greek.xml",
        "sha256": "df928f01b37632f8af9f16289ce58d10b958014cb5dbd1e1ea715a8d311a0625",
        "what": "Strong's Greek Dictionary of the New Testament (James Strong, 1890)",
        "transcription": "OpenScriptures strongs, StrongsGreekDictionaryXML_1.4 (Ulrik Petersen)",
        "url": "https://github.com/openscriptures/strongs",
        "rights": "Public domain; the file's own prologue: \"Public Domain -- Copy Freely\".",
    },
}

# Witness lexicons: slug -> (label, how to build it from data/corpus, or None
# when it can only be read from a built data/books/<slug>.json).
WITNESSES = {
    "bdb": ("bdb-hebrew", lambda: S.convert_bdb(os.path.join(LEX, "bdb-hebrew.tsv")),
            [os.path.join(LEX, "bdb-hebrew.tsv")]),
    "tbesg": ("tbesg-greek", lambda: S.convert_stepbible_greek(
                  [os.path.join(LEX, "tbesg-greek.txt")], "tbesg-greek", "", "", ""),
              [os.path.join(LEX, "tbesg-greek.txt")]),
    "lsj": ("lsj-greek", lambda: S.convert_stepbible_greek(
                [os.path.join(LEX, f) for f in ("tflsj-greek-0-5624.txt", "tflsj-greek-extra.txt")],
                "lsj-greek", "", "", ""),
            [os.path.join(LEX, f) for f in ("tflsj-greek-0-5624.txt", "tflsj-greek-extra.txt")]),
    # Thayer's entries (PR #7) come only from Adam's local OCR; read the built
    # book when it exists, else carry the committed links forward.
    "thayer": ("thayer-entries", None, [os.path.join(BOOKS, "thayer-entries.json")]),
}

# Original-language corpora: dir -> witness label. Each is one folder per book
# of <Book>/tokens.jsonl with `passage_uid` and `lemma_key`, books in the
# order its manifest.json lists them.
CORPORA = {"nt": "data/nt", "ot": "data/ot"}

KEY_RE = re.compile(r"^\s*([HGhg])?0*(\d+)\s*([A-Za-z])?\s*$")


def normalize(raw, lang=None):
    """Any house spelling of a Strong's number -> ("G26", suffix or None).

    `lang` ("greek"/"hebrew") supplies the prefix for a bare number. The
    suffix is an extended (STEPBible G0001G) or augmented (OSHB 1254a) letter:
    a finer split INSIDE one Strong's number, kept beside the key, never in it.
    Returns (None, None) for anything else."""
    m = KEY_RE.match(str(raw or ""))
    if not m:
        return None, None
    pre = (m.group(1) or {"greek": "G", "hebrew": "H"}.get(lang or "", "")).upper()
    if not pre or int(m.group(2)) == 0:
        return None, None
    return f"{pre}{int(m.group(2))}", m.group(3)


def sort_key(k):
    return (0 if k[0] == "H" else 1, int(k[1:]))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def dump_jsonl(rows):
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)


# ---------------------------------------------------------------------------
# The table
# ---------------------------------------------------------------------------

def build_table():
    rows = []
    for slug, conv, lang in (("strongs-hebrew", S.convert_strongs_hebrew, "hebrew"),
                             ("strongs-greek", S.convert_strongs_greek, "greek")):
        src = SOURCES[slug]
        path = os.path.join(LEX, src["file"])
        if not os.path.exists(path):
            raise SystemExit(f"missing {path}: run python3 pipeline/fetch_sources.py")
        got = sha256(path)
        if got != src["sha256"]:
            raise SystemExit(f"{src['file']}: sha256 {got[:12]} is not the pinned "
                             f"{src['sha256'][:12]}. The source changed upstream; read the "
                             f"diff before re-pinning.")
        for u in conv(path)["units"]:
            key = u["id"].split(":", 1)[1]
            lx = u["lex"]
            if lang == "hebrew":
                tongue = "arc" if lx.get("lang") == "arc" else "hbo"
            else:
                tongue = "grc"
            see = []
            for ln in u["links"]:
                t, _ = normalize(ln["target"].split(":", 1)[1])
                if t and t != key and t not in see:
                    see.append(t)
            row = {"strongs": key, "lang": tongue,
                   "citation": f"{CITATION_SLUG}:{key}", "entry": u["id"],
                   "lemma": lx.get("lemma", ""), "translit": lx.get("translit", ""),
                   "pron": lx.get("pron", ""),
                   "derivation": lx.get("derivation", ""),
                   "definition": lx.get("meaning", ""),
                   "kjv_usage": lx.get("kjv_usage", ""), "see": see}
            if lang == "hebrew":
                row["pos"] = lx.get("pos", "")
                row["proper_name"] = lx.get("lang") == "x-pn"
            else:
                row["beta"] = lx.get("beta", "")
            if lx.get("not_used"):
                row["not_used"] = True
                row["note"] = u["text"]
            rows.append(row)
    rows.sort(key=lambda r: sort_key(r["strongs"]))
    return rows


# ---------------------------------------------------------------------------
# Proposed uids (nothing touches data/uids/)
# ---------------------------------------------------------------------------

def build_proposals(table, prior):
    """Seed from the committed proposals; mint a concept only for a word that
    has none. Never reuse a concept the registry (mapped or reserved) holds."""
    reg = wh_uid.WhUidRegistry(REGISTRY)
    taken = set(reg._concepts)
    held = {p["citation"]: p["uid"] for p in prior}
    for u in held.values():
        taken.add(wh_uid.parse_uid(u)["concept"])
    rows, minted = [], 0
    for t in table:
        if t.get("not_used"):
            continue                       # Strong's placeholder: a number, not a word
        c = t["citation"]
        uid = reg.map.get(c) or held.get(c)
        if uid is None:
            concept = wh_uid.new_concept(taken)
            taken.add(concept)
            uid = wh_uid.format_uid(concept)
            minted += 1
        rows.append({"strongs": t["strongs"], "citation": c, "uid": uid, "kind": KIND,
                     "lemma": t["lemma"],
                     "status": "registered" if reg.map.get(c) == uid else "proposed"})
    return rows, minted


# ---------------------------------------------------------------------------
# Witnesses: where each number is written up
# ---------------------------------------------------------------------------

def _units_for(label, conv, paths):
    if conv and all(os.path.exists(p) for p in paths):
        return conv()["units"], {os.path.relpath(p, ROOT): sha256(p) for p in paths}
    if conv is None and all(os.path.exists(p) for p in paths):
        with open(paths[0], encoding="utf-8") as f:
            return json.load(f)["units"], {os.path.relpath(paths[0], ROOT): sha256(paths[0])}
    return None, None


def build_witnesses(table, prior_rows, prior_manifest):
    keys = {t["strongs"] for t in table}
    out = {t["strongs"]: {"strongs-1890": t["entry"]} for t in table}
    stats, carried = {}, []
    prior = {r["strongs"]: r["witnesses"] for r in prior_rows}
    for name, (label, conv, paths) in WITNESSES.items():
        units, shas = _units_for(label, conv, paths)
        if units is None:
            # Not buildable here: carry the committed links forward untouched.
            n = 0
            for k, w in prior.items():
                if name in w and k in out:
                    out[k][name] = w[name]
                    n += 1
            carried.append(name)
            stats[name] = dict((prior_manifest.get("witnesses") or {}).get(name, {}),
                               book=label, carried_forward=True,
                               numbers_covered=n,
                               note="source not present in this build; committed links kept as they were")
            continue
        linked, beyond, unkeyed = 0, 0, 0
        for u in units:
            targets = []
            for ln in u.get("links", []):
                if ln.get("kind") == "strongs":
                    k, _ = normalize(ln["target"].split(":", 1)[1])
                    if k:
                        targets.append(k)
            if not targets and (u.get("lex") or {}).get("strongs"):
                k, _ = normalize(u["lex"]["strongs"])
                if k:
                    targets.append(k)
            if not targets:
                unkeyed += 1
                continue
            hit = False
            for k in dict.fromkeys(targets):
                if k in keys:
                    out[k].setdefault(name, []).append(u["id"])
                    hit = True
                else:
                    beyond += 1
            linked += hit
        stats[name] = {"book": label, "entries": len(units), "linked": linked,
                       "no_strongs": unkeyed, "beyond_1890": beyond,
                       "numbers_covered": sum(1 for k in out if name in out[k]),
                       "inputs": shas}
    rows = [{"strongs": k, "witnesses": out[k]} for k in sorted(out, key=sort_key)]
    return rows, stats, carried


# ---------------------------------------------------------------------------
# Concordance: number -> passage uids, from the committed corpora
# ---------------------------------------------------------------------------

def _books(base):
    man = os.path.join(base, "manifest.json")
    if os.path.exists(man):
        with open(man, encoding="utf-8") as f:
            books = (json.load(f).get("selection") or {}).get("books")
        if books:
            return books
    return sorted(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)))


def build_concordance(table, prior_rows, prior_manifest):
    keys = {t["strongs"] for t in table}
    occ = {}                                   # key -> {corpus: [uids in canon order]}
    tokens = {}
    stats = {}
    for name, rel in CORPORA.items():
        base = os.path.join(ROOT, rel)
        if not os.path.isdir(base):
            for r in prior_rows:              # carry a corpus we cannot see forward
                if name in r["passages"]:
                    occ.setdefault(r["strongs"], {})[name] = r["passages"][name]
                    tokens.setdefault(r["strongs"], {})[name] = r["tokens"][name]
            if (prior_manifest.get("concordance") or {}).get(name):
                stats[name] = dict(prior_manifest["concordance"][name], carried_forward=True)
            continue
        n_tok, no_key, unknown, suffixed = 0, 0, {}, 0
        for book in _books(base):
            path = os.path.join(base, book, "tokens.jsonl")
            for t in read_jsonl(path):
                n_tok += 1
                k, suf = normalize(t.get("lemma_key"))
                if not k:
                    no_key += 1
                    continue
                suffixed += bool(suf)
                if k not in keys:
                    unknown[k] = unknown.get(k, 0) + 1
                    continue
                # dict as an ordered set: canon order, a verse listed once
                occ.setdefault(k, {}).setdefault(name, {})[t["passage_uid"]] = None
                tc = tokens.setdefault(k, {})
                tc[name] = tc.get(name, 0) + 1
        for k in occ:
            if isinstance(occ[k].get(name), dict):
                occ[k][name] = list(occ[k][name])
        stats[name] = {"dir": rel, "tokens": n_tok, "tokens_without_key": no_key,
                       "tokens_with_suffix": suffixed,
                       "tokens_key_not_in_1890": sum(unknown.values()),
                       "keys_not_in_1890": dict(sorted(unknown.items(), key=lambda kv: sort_key(kv[0]))),
                       "numbers_occurring": sum(1 for k in occ if name in occ[k])}
    rows = [{"strongs": k, "tokens": tokens[k], "passages": occ[k]}
            for k in sorted(occ, key=sort_key)]
    return rows, stats


# ---------------------------------------------------------------------------

def build():
    prior_manifest = {}
    mp = os.path.join(OUT, "manifest.json")
    if os.path.exists(mp):
        with open(mp, encoding="utf-8") as f:
            prior_manifest = json.load(f)
    table = build_table()
    proposals, minted = build_proposals(table, read_jsonl(os.path.join(OUT, "proposed-uids.jsonl")))
    wit, wstats, carried = build_witnesses(table, read_jsonl(os.path.join(OUT, "witnesses.jsonl")),
                                           prior_manifest)
    conc, cstats = build_concordance(table, read_jsonl(os.path.join(OUT, "concordance.jsonl")),
                                     prior_manifest)
    heb = [t for t in table if t["strongs"][0] == "H"]
    grk = [t for t in table if t["strongs"][0] == "G"]
    manifest = {
        "schema": "wordhoard/strongs/v1",
        "doc": "pipeline/README-strongs.md",
        "key": "Strong's number: 'H' or 'G' + the number, no leading zeros (H2617, G26)",
        "citation": f"{CITATION_SLUG}:<key> names the WORD; strongs-hebrew:/strongs-greek:<key> names its 1890 entry",
        "sources": {k: {x: v[x] for x in ("what", "transcription", "url", "sha256", "rights")}
                    for k, v in SOURCES.items()},
        "table": {"rows": len(table), "hebrew": len(heb), "greek": len(grk),
                  "aramaic": sum(t["lang"] == "arc" for t in heb),
                  "hebrew_proper_names": sum(t.get("proper_name", False) for t in heb),
                  "not_used": [t["strongs"] for t in table if t.get("not_used")]},
        "uids": {"status": "PROPOSED -- not in data/uids/; minting awaits Adam (CLAUDE.md 3b)",
                 "kind": KIND, "proposed": sum(p["status"] == "proposed" for p in proposals),
                 "registered": sum(p["status"] == "registered" for p in proposals)},
        "witnesses": wstats,
        "concordance": cstats,
        "not_claimed": [
            "No KJV English word is linked to a Strong's number: that is the English half of "
            "Strong's Exhaustive Concordance, and no public-domain tagged KJV has been verified "
            "here yet (README s.6).",
            "The concordance is by passage uid in the ORIGINAL-LANGUAGE corpora only; a number "
            "absent from them is absent here, not unused in scripture.",
            "Strong's numbering is the key, not a claim that each number is one word: Strong's "
            "lumps some homographs and splits some forms (README s.3).",
        ],
    }
    return {
        "strongs.jsonl": dump_jsonl(table),
        "proposed-uids.jsonl": dump_jsonl(proposals),
        "witnesses.jsonl": dump_jsonl(wit),
        "concordance.jsonl": dump_jsonl(conc),
        "manifest.json": json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
    }, minted, carried


def write(outputs):
    os.makedirs(OUT, exist_ok=True)
    for name, text in outputs.items():
        p = os.path.join(OUT, name)
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, p)                     # atomic: a killed run never truncates


def adopt():
    """Copy every proposed uid into the public registry, verbatim. Run ONLY on
    Adam's ruling. Refuses if any proposed uid is already held by something
    else, or any citation is already mapped to a different uid."""
    reg = wh_uid.WhUidRegistry(REGISTRY)
    held = {u: c for c, u in reg.map.items()}
    rows = read_jsonl(os.path.join(OUT, "proposed-uids.jsonl"))
    added = 0
    for p in rows:
        c, u = p["citation"], p["uid"]
        if reg.map.get(c) == u:
            continue
        if c in reg.map:
            raise SystemExit(f"{c} is already {reg.map[c]}, not {u}: refusing")
        if u in held or u in reg.reserved or u in reg.all_uids():
            raise SystemExit(f"{u} is already held ({held.get(u, 'reserved')}): refusing")
        reg.map[c] = u
        added += 1
    reg.save()
    print(f"adopted {added} uids into {os.path.relpath(REGISTRY, ROOT)}; now rebuild "
          f"(python3 pipeline/build_strongs.py) so proposed-uids.jsonl says 'registered'")


def main():
    if "--adopt" in sys.argv:
        return adopt()
    outputs, minted, carried = build()
    if "--check" in sys.argv:
        bad = []
        for name, text in outputs.items():
            p = os.path.join(OUT, name)
            cur = open(p, encoding="utf-8").read() if os.path.exists(p) else None
            if cur != text:
                bad.append(name)
        print(f"proposed now: {minted} (must be 0)")
        if carried:
            print(f"carried forward, source not here: {', '.join(carried)}")
        for name in FILES:
            print(("DIFF  " if name in bad else "same  ") + name)
        sys.exit(1 if bad or minted else 0)
    write(outputs)
    m = json.loads(outputs["manifest.json"])
    print(f"table: {m['table']['rows']} rows ({m['table']['hebrew']} H, {m['table']['greek']} G)")
    print(f"uids: {minted} newly proposed; {m['uids']['proposed']} proposed, "
          f"{m['uids']['registered']} registered")
    for k, v in m["witnesses"].items():
        print(f"witness {k}: {v.get('numbers_covered')} numbers"
              + (" (carried forward)" if v.get("carried_forward") else ""))
    for k, v in m["concordance"].items():
        print(f"concordance {k}: {v.get('numbers_occurring')} numbers from {v.get('tokens')} tokens")


if __name__ == "__main__":
    main()
