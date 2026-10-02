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
         "concordance.jsonl", "kjv-tags.jsonl", "kjv-renderings.jsonl", "parallels.jsonl",
         "concordance-view.jsonl", "manifest.json")

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

# Original-language corpora, read ONLY through their own loaders (their shards
# are rebuilt by pipeline/rebuild_bible.py, not committed): name -> (dir, loader).
CORPORA = {"nt": "data/nt", "ot": "data/ot"}


def load_corpus(name):
    """The corpus's tokens via build_nt_corpus.load_nt / build_ot_corpus.load_ot,
    or None when its shards are not built here."""
    try:
        if name == "nt":
            import build_nt_corpus as M
            return M.load_nt(ROOT)["tokens"]
        import build_ot_corpus as M
        return M.load_ot(ROOT)["tokens"]
    except (SystemExit, FileNotFoundError):
        return None

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

def build_concordance(table, prior_rows, prior_manifest, kjv_rows=None):
    keys = {t["strongs"] for t in table}
    occ = {}                                   # key -> {corpus: [uids in canon order]}
    tokens = {}
    stats = {}
    # The KJV's own tagging: every verse of both testaments, by the English.
    if kjv_rows is None:
        for r in prior_rows:
            if "kjv" in r["passages"]:
                occ.setdefault(r["strongs"], {})["kjv"] = r["passages"]["kjv"]
                tokens.setdefault(r["strongs"], {})["kjv"] = r["tokens"]["kjv"]
        if (prior_manifest.get("concordance") or {}).get("kjv"):
            stats["kjv"] = prior_manifest["concordance"]["kjv"]   # unchanged: see kstats
    else:
        for r in kjv_rows:
            for _, k in r["tags"] + r.get("title_tags", []):
                if k in keys:
                    occ.setdefault(k, {}).setdefault("kjv", {})[r["passage_uid"]] = None
                    tc = tokens.setdefault(k, {})
                    tc["kjv"] = tc.get("kjv", 0) + 1
        for k in occ:
            if isinstance(occ[k].get("kjv"), dict):
                occ[k]["kjv"] = list(occ[k]["kjv"])
        stats["kjv"] = {"dir": "data/strongs/kjv-tags.jsonl",
                        "tokens": sum(len(r["tags"]) + len(r.get("title_tags", [])) for r in kjv_rows),
                        "numbers_occurring": sum(1 for k in occ if "kjv" in occ[k]),
                        "note": "tagged KJV words, not original-language tokens"}
    for name, rel in CORPORA.items():
        toks = load_corpus(name)
        if toks is None:
            for r in prior_rows:              # carry a corpus we cannot see forward
                if name in r["passages"]:
                    occ.setdefault(r["strongs"], {})[name] = r["passages"][name]
                    tokens.setdefault(r["strongs"], {})[name] = r["tokens"][name]
            if (prior_manifest.get("concordance") or {}).get(name):
                stats[name] = prior_manifest["concordance"][name]     # unchanged: --check holds
            continue
        n_tok, no_key, unknown, suffixed = 0, 0, {}, 0
        for t in toks:
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
# The English half: KJV words tagged with Strong's numbers (README s.6)
# ---------------------------------------------------------------------------

KJV_SRC = {
    "url": "https://ebible.org/Scriptures/eng-kjv2006_usfm.zip",
    "dir": os.path.join(S.CORPUS, "strongs-kjv", "eng-kjv2006_usfm"),
    # sha256 of the 66 .usfm files, concatenated in file-name order. Not the
    # zip's: eBible rebuilds the zip (and its dated copr.htm) on its own schedule.
    "usfm_sha256": "6c4d66ade2f4d44c43f8652374b5a3952fb9b2e42fb821711d4bc5724141a9f4",
    "edition": ("King James (Authorized) Version, 1769 standard text, protocanon, \"with "
                "Strong's numbers added\" -- eBible.org eng-kjv2006, USFM"),
    "rights_line": ("eBible.org, the edition's own page and copr.htm: \"Public Domain\" ... "
                    "\"You may copy the King James Version of the Holy Bible freely.\" "
                    "(Crown letters patent: UK printing only.)"),
    "lineage": ("The tagging is CrossWire's KJV module: OT Strong's from The Bible Foundation "
                "(bf.org), NT from CrossWire's KJV2003 project. CrossWire's kjv.conf: "
                "\"CrossWire Bible Society hereby grants a general public license to use this "
                "text for any purpose\"; DistributionLicense=GPL."),
    "status": "rights ruling for Adam: labelled public domain on the exact edition, see README s.6",
}

USFM_OSIS = dict(zip(
    "GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO ECC SNG "
    "ISA JER LAM EZK DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL "
    "MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE 2PE "
    "1JN 2JN 3JN JUD REV".split(),
    "Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps "
    "Prov Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal "
    "Matt Mark Luke John Acts Rom 1Cor 2Cor Gal Eph Phil Col 1Thess 2Thess 1Tim 2Tim Titus Phlm "
    "Heb Jas 1Pet 2Pet 1John 2John 3John Jude Rev".split()))

USFM_ORDER = {o: i for i, o in enumerate(USFM_OSIS.values())}
RE_KJV_W = re.compile(r'\\\+?w ([^|\\]+)\|strong="([HG]\d+)"\\\+?w\*')
RE_FOOTNOTE = re.compile(r"\\f .*?\\f\*", re.S)


def fetch_kjv():
    import io
    import urllib.request
    import zipfile
    req = urllib.request.Request(KJV_SRC["url"], headers={"User-Agent": "canon-corpus"})
    with urllib.request.urlopen(req, timeout=120) as r:
        zf = zipfile.ZipFile(io.BytesIO(r.read()))
    os.makedirs(KJV_SRC["dir"], exist_ok=True)
    for m in zf.infolist():
        if m.filename.endswith((".usfm", ".htm")):
            with open(os.path.join(KJV_SRC["dir"], os.path.basename(m.filename)), "wb") as f:
                f.write(zf.read(m))
    print(f"fetched {KJV_SRC['url']} -> {os.path.relpath(KJV_SRC['dir'], ROOT)}")


def _usfm_files():
    d = KJV_SRC["dir"]
    if not os.path.isdir(d):
        return None
    fs = sorted(f for f in os.listdir(d) if f.endswith(".usfm"))
    return [os.path.join(d, f) for f in fs] if len(fs) == 66 else None


def read_kjv_tags(table):
    """-> ([{passage_uid, citation, tags: [[english, key], ...]}], stats), or
    (None, None) when the source is not here. `english` is the KJV word or
    phrase exactly as tagged, in verse order; untagged words (the italics the
    translators supplied, most articles) are not listed."""
    files = _usfm_files()
    if not files:
        return None, None
    h = hashlib.sha256()
    for f in files:
        with open(f, "rb") as fh:
            h.update(fh.read())
    got = h.hexdigest()
    if got != KJV_SRC["usfm_sha256"]:
        raise SystemExit(f"eBible KJV USFM sha256 {got[:12]} is not the pinned "
                         f"{KJV_SRC['usfm_sha256'][:12]}: read the diff before re-pinning.")
    reg = wh_uid.WhUidRegistry(REGISTRY)
    keys = {t["strongs"] for t in table}
    rows, missing, unknown, n_tags, n_title = [], [], {}, 0, 0

    def tag(chunk):
        nonlocal n_tags
        out = []
        for word, raw in RE_KJV_W.findall(chunk):
            k, _ = normalize(raw)
            n_tags += 1
            if k not in keys:
                unknown[k] = unknown.get(k, 0) + 1
            out.append([word, k])
        return out

    for f in files:
        code = os.path.basename(f)[3:6]
        osis = USFM_OSIS[code]
        text = RE_FOOTNOTE.sub("", open(f, encoding="utf-8-sig").read())
        ch, title = None, []
        for line in re.split(r"(?=\\[cv] )", text):
            m = re.match(r"\\c (\d+)", line)
            if m:
                ch = int(m.group(1))
                title = tag(line)        # a psalm title (\\d) sits before verse 1
                n_title += len(title)
                continue
            m = re.match(r"\\v (\d+)", line)
            if not m:
                continue
            cit = f"kjv:{osis}.{ch}.{int(m.group(1))}"
            uid = reg.map.get(cit)
            if uid is None:
                missing.append(cit)
                continue
            row = {"passage_uid": uid, "citation": cit, "tags": tag(line)}
            if title:
                row["title_tags"] = title    # the KJV numbers no title: kept beside verse 1
                title = []
            rows.append(row)
    stats = {"source": dict(KJV_SRC, usfm_sha256=got, dir=os.path.relpath(KJV_SRC["dir"], ROOT)),
             "verses": len(rows), "tags": n_tags, "psalm_title_tags": n_title,
             "verses_without_tags": sum(1 for r in rows if not r["tags"]),
             "citations_without_uid": missing,
             "keys_not_in_1890": dict(sorted(unknown.items(), key=lambda kv: sort_key(kv[0])))}
    return rows, stats


def kjv_renderings(rows):
    """key -> {english: count}: the index at the back of Strong's Exhaustive
    Concordance. Case folded, except words the KJV prints in capitals (LORD)."""
    out = {}
    for r in rows:
        for word, k in r["tags"] + r.get("title_tags", []):
            w = word if word.isupper() and len(word) > 1 else word.lower()
            d = out.setdefault(k, {})
            d[w] = d.get(w, 0) + 1
    return [{"strongs": k, "renderings": dict(sorted(out[k].items(), key=lambda kv: (-kv[1], kv[0])))}
            for k in sorted(out, key=sort_key)]


# ---------------------------------------------------------------------------
# OSHB's Strong's tags on the Hebrew OT tokens: CC BY 4.0, BUILT, NEVER COMMITTED
# ---------------------------------------------------------------------------

OSHB_OUT = os.path.join(ROOT, "build", "strongs", "oshb-ot")     # gitignored (build/)
OSHB_RIGHTS = {
    "license": "CC BY 4.0",
    "attribution": ("Open Scriptures Hebrew Bible (OSHB), lemma and morphology tagging, "
                    "openscriptures/morphhb; Westminster Leningrad Codex text public domain"),
    "source_url": "https://github.com/openscriptures/morphhb",
    "redistribute_whole": False,
    "note": ("Not committed: data/ot/ withholds OSHB's CC BY layer under ADR 0001, and this "
             "layer follows the same gate (as the STEPBible lexicons do). Built locally into "
             "build/, gitignored. Drop it by deleting build/strongs/oshb-ot/."),
}
RE_OSHB_NUM = re.compile(r"(\d+)(?:\s*([a-z]))?")


def oshb_keys(lemma):
    """OSHB lemma attribute -> [(key, augment letter or None)]: 'c/d/776' ->
    [('H776', None)]; '1254 a' -> [('H1254', 'a')]. Prefixes (b/, c/, l/ ...)
    carry no number and are not returned."""
    out = []
    for part in (lemma or "").split("/"):
        m = RE_OSHB_NUM.search(part)
        if m:
            out.append((f"H{int(m.group(1))}", m.group(2)))
    return out


def build_oshb_layer():
    """Strong's keys for every data/ot/ token, from the same pinned OSHB files
    build_ot_corpus.py reads, segmented by ITS rules: its read_book() is
    wrapped, and each verse re-walked in parallel to collect lemma attributes
    per word, then zipped against its tokens with the surfaces checked."""
    try:
        import build_ot_corpus as O
        import xml.etree.ElementTree as ET
    except ImportError:
        return None
    import build_versification as V
    if not all(os.path.exists(os.path.join(V.WLC_DIR, b + ".xml")) for b in O.SCOPE):
        return None
    NS = O.NS
    log = []                                   # (wlc ref, [[keys] per word]) in plan order
    orig = O.read_book

    def lemmas_of(osis):
        root = ET.parse(os.path.join(V.WLC_DIR, osis + ".xml")).getroot()
        per = {}
        for v in root.iter(NS + "verse"):
            words, prev = [], None
            for el in v:
                if el.tag == NS + "w" and prev is not None and prev.tag == NS + "w" \
                        and not (prev.tail or "").strip(" \n\t") and not re.search(r"\s", prev.tail or ""):
                    words[-1] += oshb_keys(el.get("lemma"))      # one WLC word OSHB divided
                    prev = el
                    continue
                prev = el
                if el.tag == NS + "w":
                    words.append(oshb_keys(el.get("lemma")))
            per[v.get("osisID")] = words
        return per

    def wrapped(osis):
        out = orig(osis)
        per = lemmas_of(osis)
        for ref, verse in out:
            if len(per[ref]) != len(verse["words"]):
                raise SystemExit(f"OSHB layer: {ref} has {len(verse['words'])} words, "
                                 f"lemma walk found {len(per[ref])}")
            log.append((ref, per[ref]))
        return out

    O.read_book = wrapped
    try:
        data, manifest = O.build(wh_uid.WhUidRegistry(REGISTRY, frozen=True))
    finally:
        O.read_book = orig
    skipped = {x["wlc"] for x in manifest["versification"]["left_out"]}
    flat = [ks for ref, words in log if ref not in skipped for ks in words]
    toks = data["tokens"]
    if len(flat) != len(toks):
        raise SystemExit(f"OSHB layer: {len(flat)} words vs {len(toks)} tokens")
    book = {p["uid"]: p["book"] for p in data["passages"]}
    per_book = {}
    for t, ks in zip(toks, flat):
        row = {"address": t["address"], "passage_uid": t["passage_uid"], "witness": t["witness"],
               "position": t["position"], "surface": t["surface"], "strongs": [k for k, _ in ks]}
        if any(a for _, a in ks):
            row["augment"] = [a for _, a in ks]
        per_book.setdefault(book[t["passage_uid"]], []).append(row)
    return per_book


# ---------------------------------------------------------------------------
# The concordance VIEW: one row per number, everything about it in one place
# ---------------------------------------------------------------------------

# Parallel Bibles, each reached from the KJV verse through a committed verse
# map: name -> (slug, how to build its units from data/corpus, inputs).
def _vulgate_units():
    import fetch_sources as F
    return S.convert_vulgate(os.path.join(S.CORPUS, "vulgate"), F.VULGATE["books"],
                             F.VULGATE["pin"])["units"]


def _douay_units():
    import fetch_sources as F
    p = os.path.join(S.CORPUS, "douay", "DRC.json")
    return S.convert_douay(p, F.VULGATE["books"], sha256(p))["units"]


PARALLELS = {
    "vulgate": (_vulgate_units, [os.path.join(S.CORPUS, "vulgate")],
                "Clementine Vulgate (1592, PD), through data/versification/vulgate-kjv.json"),
    "douay": (_douay_units, [os.path.join(S.CORPUS, "douay", "DRC.json")],
              "Douay-Rheims, Challoner (PD), in the Vulgate's numbering, through the same map"),
}
PARALLELS_NOT_YET = {
    "brenton": ("Brenton's Septuagint is not in this repo. A Septuagint->KJV map exists on "
                "branch claude/happy-carson-m9ajwl (data/versification/lxx-kjv.tsv, CC BY-SA), "
                "which is not a PR in this project; it wires in here once it lands."),
}


def build_parallels(prior_rows):
    """KJV verse -> the unit ids in each parallel Bible holding its text.
    Only verses where that is NOT simply the same number are listed; a verse
    absent here has `<slug>:<same osis>` in each. Returns (rows, stats, carried)."""
    by_kjv, stats, carried = {}, {}, []
    have = {}
    for name, (units_fn, paths, what) in PARALLELS.items():
        if not all(os.path.exists(p) for p in paths) or not os.path.exists(
                os.path.join(ROOT, "data", "versification", "vulgate-kjv.json")):
            carried.append(name)
            continue
        units = units_fn()
        have[name] = {u["id"] for u in units}
        unresolved = 0
        for u in units:
            k = u.get("kjv") or {}
            if not k.get("resolved"):
                unresolved += 1
                continue
            ts = [t for t in (k.get("spans") or [k["target"]]) if t.startswith("kjv:")]
            for t in ts:
                by_kjv.setdefault(t[4:], {}).setdefault(name, []).append(u["id"])
        stats[name] = {"what": what, "units": len(units), "units_without_kjv_verse": unresolved}
    rows = []
    for r in prior_rows:                      # a Bible not buildable here: keep its rows
        for name in carried:
            if name in r["parallels"]:
                by_kjv.setdefault(r["kjv"], {})[name] = r["parallels"][name]
    reg = wh_uid.WhUidRegistry(REGISTRY)
    kjv_osis = sorted((c[4:] for c in reg.map if c.startswith("kjv:")),
                      key=lambda o: (USFM_ORDER.get(o.split(".")[0], 99),
                                     int(o.split(".")[1]), int(o.split(".")[2])))
    for osis in kjv_osis:
        par = by_kjv.get(osis, {})
        out = {}
        for name in PARALLELS:
            if name in carried and name not in par:
                continue                   # carried, and the committed file had it same-numbered
            ids = par.get(name, [])
            if ids != [f"{name}:{osis}"]:
                out[name] = ids            # [] = no verse of that Bible holds it
        if out:
            rows.append({"kjv": osis, "parallels": out})
    for name in PARALLELS:
        if name in stats:
            stats[name]["kjv_verses_renumbered_or_split"] = sum(1 for r in rows if r["parallels"].get(name))
            stats[name]["kjv_verses_with_none"] = sum(1 for r in rows if r["parallels"].get(name) == [])
    return rows, stats, carried


def build_view(table, wit, kjv_rows, parallels):
    """One row per number the KJV tags or the NT uses."""
    by = {t["strongs"]: t for t in table}
    w = {r["strongs"]: r["witnesses"] for r in wit}
    par = {r["kjv"]: r["parallels"] for r in parallels}
    verses, words = {}, {}
    for r in kjv_rows:
        osis = r["citation"][4:]
        for word, k in r["tags"] + r.get("title_tags", []):
            vs = verses.setdefault(k, {})
            vs[osis] = vs.get(osis, 0) + 1
            d = words.setdefault(k, {})
            ww = word if word.isupper() and len(word) > 1 else word.lower()
            d[ww] = d.get(ww, 0) + 1
    rows = []
    for k in sorted(set(verses) | {t["strongs"] for t in table if not t.get("not_used")}, key=sort_key):
        t = by[k]
        vs = verses.get(k, {})
        lex = {name: cits for name, cits in w.get(k, {}).items()}
        row = {"strongs": k, "lemma": t["lemma"], "translit": t["translit"], "lang": t["lang"],
               "definition": t["definition"], "lexicons": lex,
               "kjv": {"occurrences": sum(vs.values()), "verses": list(vs),
                       "renderings": dict(sorted(words.get(k, {}).items(), key=lambda kv: (-kv[1], kv[0])))},
               "parallels": {o: par[o] for o in vs if o in par}}
        rows.append(row)
    return rows


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
    kjv_rows, kstats = read_kjv_tags(table)
    if kjv_rows is None:                     # source not here: the committed layer stands
        kjv_text = {n: open(os.path.join(OUT, n), encoding="utf-8").read()
                    for n in ("kjv-tags.jsonl", "kjv-renderings.jsonl")
                    if os.path.exists(os.path.join(OUT, n))}
        kstats = prior_manifest.get("kjv") or {}     # unchanged, so --check holds without the source
        carried.append("kjv")
    else:
        kjv_text = {"kjv-tags.jsonl": dump_jsonl(kjv_rows),
                    "kjv-renderings.jsonl": dump_jsonl(kjv_renderings(kjv_rows))}
    conc, cstats = build_concordance(table, read_jsonl(os.path.join(OUT, "concordance.jsonl")),
                                     prior_manifest, kjv_rows)
    par, pstats, pcarried = build_parallels(read_jsonl(os.path.join(OUT, "parallels.jsonl")))
    for name in pcarried:
        pstats[name] = (prior_manifest.get("parallels") or {}).get(name, {})
    carried += [f"parallels:{n}" for n in pcarried]
    if kjv_rows is not None:
        view = dump_jsonl(build_view(table, wit, kjv_rows, par))
    else:                                     # the view needs the KJV tags: keep the committed one
        vp = os.path.join(OUT, "concordance-view.jsonl")
        view = open(vp, encoding="utf-8").read() if os.path.exists(vp) else ""
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
        "kjv": kstats,
        "parallels": dict(pstats, rule=("parallels.jsonl lists a KJV verse only where a parallel "
                                        "Bible does not hold it under the same number; [] = none "
                                        "of its verses does"), not_yet=PARALLELS_NOT_YET),
        "view": {"file": "concordance-view.jsonl",
                 "row": ("one per used Strong's number: lemma, definition, every lexicon entry "
                         "(citations), every KJV verse and English rendering, and for each "
                         "verse whose number differs, its Vulgate and Douay verse ids")},
        "oshb_layer": dict(OSHB_RIGHTS, built_to="build/strongs/oshb-ot/<Book>.jsonl",
                           how="python3 pipeline/build_strongs.py (when the pinned WLC is in data/corpus/)"),
        "not_claimed": [
            "The KJV tags are CrossWire's, as eBible.org publishes them; they are not checked "
            "here against the Hebrew or Greek, and the rights call on them is Adam's (README s.6).",
            "A KJV tag links an English word to the number of the word it translates; untagged "
            "words (italics the translators supplied, most articles) are not listed.",
            "The ot corpus carries no keys of its own: data/ot/ withholds OSHB's CC BY tags. "
            "Old Testament occurrences come from the KJV's tagging (corpus kjv), by verse.",
            "Strong's numbering is the key, not a claim that each number is one word: Strong's "
            "lumps some homographs and splits some forms (README s.3).",
        ],
    }
    return {
        "strongs.jsonl": dump_jsonl(table),
        "proposed-uids.jsonl": dump_jsonl(proposals),
        "witnesses.jsonl": dump_jsonl(wit),
        "concordance.jsonl": dump_jsonl(conc),
        **kjv_text,
        "parallels.jsonl": dump_jsonl(par),
        "concordance-view.jsonl": view,
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
    if "--fetch" in sys.argv:
        return fetch_kjv()
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
    layer = build_oshb_layer()
    if layer:
        os.makedirs(OSHB_OUT, exist_ok=True)
        for book, recs in layer.items():
            with open(os.path.join(OSHB_OUT, book + ".jsonl"), "w", encoding="utf-8", newline="\n") as f:
                f.write(dump_jsonl(recs))
        with open(os.path.join(OSHB_OUT, "rights.json"), "w", encoding="utf-8") as f:
            json.dump(OSHB_RIGHTS, f, ensure_ascii=False, indent=1)
        n = sum(len(v) for v in layer.values())
        print(f"oshb layer (CC BY, not committed): {n} tokens -> {os.path.relpath(OSHB_OUT, ROOT)}")
    else:
        print("oshb layer: skipped (pinned WLC not in data/corpus; build_versification.py --fetch)")
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
