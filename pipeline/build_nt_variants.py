#!/usr/bin/env python3
"""
build_nt_variants.py -- a variant apparatus for the Greek NT: for every KJV
verse, which of eight printed editions read which words, from STEPBible's
TAGNT (Translators Amalgamated Greek NT), attached to the verses of data/nt/.

    python3 pipeline/build_nt_variants.py --fetch    # pinned TAGNT -> data/corpus/tagnt/ (gitignored)
    python3 pipeline/build_nt_variants.py            # build data/books/tagnt-variants.json + manifest entry
    python3 pipeline/build_nt_variants.py --check    # rebuild in memory: = the committed manifest entry
    python3 pipeline/build_nt_variants.py --measure  # TAGNT's Byzantine text against our RP2018, verse by verse
    python3 tests/nt_variants_test.py

WHY TAGNT, AND NOT THE OTHERS (rule 6; each rights line read 2026-10-02).
- MorphGNT/SBLGNT: the SBLGNT text is under the SBLGNT EULA, the parsing CC
  BY-SA 3.0 (its README). Not usable here.
- OpenGNT: CC BY-SA 4.0 over a text compiled from the Berean Greek Bible, and
  its tables carry Berean, NET and CSB translations that are "All Rights
  Reserved" or non-commercial (its README, "Other Credits"). Not usable here.
- TAGNT (STEPBible-Data, "Translators Amalgamated OT+NT/TAGNT *.txt"): CC BY
  4.0, with STEPBible's request not to redistribute it ("Refer others to
  github.com/STEPBible as the source of the data. Please do not redistribute
  it yourself."). The house honours that exactly as for the STEPBible
  lexicons: the source and the built book are gitignored, only the manifest
  entry is committed, with `redistribute_whole: false`. TAGNT's English
  column is the Berean Study Bible "with permission" and its Spanish is
  OpenGNT's: neither is read into anything built here.

WHAT IT RECORDS. TAGNT lists every word of NA28, NA27, the Tyndale House GNT
(2017), SBLGNT (2010), Westcott-Hort (1881), Tregelles (1879), Scrivener's TR
(1894) and the Byzantine text (Robinson-Pierpont 2005), each word with the
editions that print it. A unit here is one KJV verse in which the editions
are not unanimous: each run of words read by the same editions is a
`reading`, with the editions that have it, the words other editions print in
its place (`instead`) and the editions that omit it (`omit`), its
Strong's numbers and grammar, and whether TAGNT counts the difference as
significant for translation (an upper-case variant code) or minor (lower
case). Spelling variants, other words in the same slot (TAGNT's "meaning
variants") and word-order displacements ride along. Glosses never do.

VERSES. TAGNT numbers as the NRSV and marks the KJV's number in square
brackets (`2Co.13.13[13.14]`); the KJV's is used, so every unit names an
existing kjv: verse and its uid in data/uids/ (Luke 17:36, Acts 8:37, 15:34
and 24:7 have one but no data/nt row: RP2018 does not print them). Nothing
is minted.

THE BASE TEXT. data/nt/ is RP2018; TAGNT's `Byz` is RP2005. `--measure`
compares them word by word on the NT's accentless search key, so how far the
apparatus's Byzantine column can stand for the base text is measured, not
assumed: 97.55% of words agree in order and 69.8% of verses are identical
(2026-10-02). Most of the rest is spelling (movable nu, Δαβίδ/Δαυίδ) and the
few places where the two divide verses differently (Matt 23:13-14, 2 Cor
8:13-14), which also means a word or two of a reading can be filed under the
neighbouring verse.
"""
import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_nt_corpus as N  # noqa: E402

BOOKS = os.path.join(ROOT, "data", "books")
MANIFEST = os.path.join(BOOKS, "manifest.json")
SLUG = "tagnt-variants"

REPO = "STEPBible/STEPBible-Data"
COMMIT = "b99716b0cddb648ddb95cc786a197180f2f97d48"
CACHE = os.path.join(ROOT, "data", "corpus", "tagnt", COMMIT[:12])
DIR = "Translators Amalgamated OT+NT"
FILES = {
    f"{DIR}/TAGNT Mat-Jhn - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt":
        "ab8eaaeb68e17a1dcfa34e1e9350358f22f03bc2a97244d848750ad81044bc8e",
    f"{DIR}/TAGNT Act-Rev - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt":
        "524e32375361e6d3fa2f7ef00b87605fdc4317a762f395651a05fdc31ad031b7",
}
EDITIONS = ["NA28", "NA27", "Tyn", "SBL", "WH", "Treg", "TR", "Byz"]
EDITION_NAMES = {
    "NA28": "Nestle-Aland 28th ed. (2012)", "NA27": "Nestle-Aland 27th ed.",
    "Tyn": "Tyndale House GNT (2017)", "SBL": "SBLGNT (Holmes 2010)",
    "WH": "Westcott-Hort (1881)", "Treg": "Tregelles (1879)",
    "TR": "Scrivener's Textus Receptus (1894)", "Byz": "Robinson-Pierpont Byzantine (2005)",
}
# TAGNT's book abbreviations, in order, and the OSIS names of the kjv: ids.
TAGNT_BOOKS = ["Mat", "Mrk", "Luk", "Jhn", "Act", "Rom", "1Co", "2Co", "Gal", "Eph", "Php", "Col",
               "1Th", "2Th", "1Ti", "2Ti", "Tit", "Phm", "Heb", "Jas", "1Pe", "2Pe", "1Jn", "2Jn",
               "3Jn", "Jud", "Rev"]
OSIS = ["Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil", "Col",
        "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet", "1John",
        "2John", "3John", "Jude", "Rev"]
BOOK = dict(zip(TAGNT_BOOKS, OSIS))

RIGHTS = {
    "license": "CC BY 4.0 (STEPBible-Data, Tyndale House Cambridge); STEPBible asks that the "
               "data not be redistributed, only pointed to",
    "attribution": "TAGNT - Translators Amalgamated Greek NT, STEPBible.org, based on work at "
                   "Tyndale House Cambridge",
    "source_url": f"https://github.com/{REPO}/tree/{COMMIT}/{DIR.replace(' ', '%20')}",
    "redistribute_whole": False,
}
ROW = re.compile(r"^([0-9A-Za-z]+)\.(\d+)\.(\d+)(?:\[(\d+)\.(\d+)\])?(?:\([\d.]+\))?(?:\{[\d.]+\})?#(\d+)=(\S+)$")
EDITION_TOKEN = re.compile(r"^(NA28|NA27|Tyn|SBL|WH|Treg|TR|Byz)((?:[»«][\d.]+)*)$")


def sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def local(rel):
    return os.path.join(CACHE, *rel.split("/"))


def fetch():
    import pinned_fetch as F
    F.fetch(REPO, COMMIT, [(rel, local(rel), sha) for rel, sha in FILES.items()],
            ua="canon-corpus/nt-variants")


def verify_pins():
    bad = [rel for rel, want in FILES.items()
           if not os.path.exists(local(rel)) or sha256_file(local(rel)) != want]
    if bad:
        raise SystemExit(f"pinned inputs missing or changed: {[os.path.basename(b) for b in bad]}\n"
                         f"  run: python3 pipeline/build_nt_variants.py --fetch")


def check_licence(text, rel):
    head = text[:3000]
    if "CC BY 4.0" not in head or "Please do not redistribute it yourself" not in head:
        raise SystemExit(f"HARD STOP: {rel}: the licence lines are not the ones recorded "
                         f"(CC BY 4.0, and the request not to redistribute); re-read them")


def editions_of(cell):
    """({edition: displacement}, other witnesses) from TAGNT's editions cell.
    A displacement is 0 where the edition has the word in this place, +n or
    -n words where it has it later or earlier ("TR»1", "WH«3"), or the verse
    it moves to ("Byz«14.24": the Byzantine text prints the Romans doxology
    as 14:24-26, after 14:23). Other sigla are manuscripts and versions TAGNT cites for a
    reading (01, 03, P66, Coptic, Latin, Syriac, NIV): kept as witnesses."""
    eds, extra = {}, []
    for tok in cell.split("+"):
        tok = tok.strip()
        if not tok:
            continue
        m = EDITION_TOKEN.match(tok)
        if not m:
            extra.append(tok)
            continue
        ed, moves = m.groups()
        d = 0
        for arrow, n in re.findall(r"([»«])([\d.]+)", moves):
            if "." in n:
                d = "at " + n
                break
            d += int(n) if arrow == "»" else -int(n)
        eds[ed] = d
    return eds, extra


def significant(code):
    """TAGNT's word-type code: upper case marks a variant that changes the
    translation, lower case one too minor to; NKO is every edition."""
    return code != "NKO" and not any(c.islower() for c in code)


def read_rows():
    """Every TAGNT word row, in file order, as a dict."""
    rows = []
    for rel in FILES:
        with open(local(rel), encoding="utf-8-sig") as f:
            text = f.read()
        check_licence(text, rel)
        for line in text.split("\n"):
            cells = line.rstrip("\r").split("\t")
            m = ROW.match(cells[0]) if cells else None
            if not m:
                continue
            bk, ch, v, kch, kv, n, code = m.groups()
            if bk not in BOOK:
                raise SystemExit(f"HARD STOP: unknown book {bk!r} in {cells[0]!r}")
            kjv = f"{BOOK[bk]}.{kch or ch}.{kv or v}"
            greek = re.sub(r"\s*\([^)]*\)\s*$", "", cells[1]).strip()
            strongs, _, grammar = cells[3].partition("=")
            eds, extra = editions_of(cells[5])
            rows.append({"kjv": kjv, "tagnt": cells[0].split("#")[0], "n": int(n), "code": code,
                         "greek": greek, "strongs": strongs, "grammar": grammar,
                         "editions": eds, "extra": extra,
                         "alt_strongs": cells[12].strip() if len(cells) > 12 else "",
                         "meaning": cells[6].strip(), "spelling": cells[7].strip()})
    return rows


# "Ἀμών (t=Amōn) Amon - G0300=N-ASM-P in: TR+Byz", or several words: "ἐν τοῖς
# οὐρανοῖς (T=...) in the heavens - G1722=PREP + G3588=T-DPM + G3772=N-DPM in:
# TR+Byz". The Greek, each word's Strong's and grammar, and the editions are
# kept; TAGNT's English for it is not.
def meaning_variants(cell):
    out = []
    for part in re.split(r"(?<=[\w»«])\s*;\s*(?=\S+\s*\()|\s{2,}(?=\S+ \()", cell):
        if " in:" not in part or "(" not in part:
            continue
        head, _, eds = part.rpartition(" in:")
        greek = head.split(" (", 1)[0].strip()
        nums = re.findall(r"(G\d+\w*)=([^\s+]+)", head)
        out.append({"greek": greek, "strongs": [n for n, _ in nums], "grammar": [g for _, g in nums],
                    "editions": sorted(editions_of(eds.strip().split()[0] if eds.strip() else "")[0],
                                       key=EDITIONS.index)})
    return out


def spelling_variants(cell):
    """'Tyn+WH: Δαυεὶδ ; +TR: Δαβὶδ ;' -> [{editions, greek}]."""
    out = []
    for part in cell.split(";"):
        eds, _, greek = part.partition(":")
        eds, greek = eds.strip().lstrip("+"), greek.strip()
        if greek:
            out.append({"editions": [e for e in eds.split("+") if e], "greek": greek})
    return out


def verses(rows):
    by = {}
    for r in rows:
        by.setdefault(r["kjv"], []).append(r)
    return by


def readings(words):
    """Runs of consecutive words read by the same editions (not all eight)."""
    out, run = [], None
    for w in words:
        present = tuple(e for e in EDITIONS if e in w["editions"])
        if len(present) == len(EDITIONS):
            run = None
            continue
        sig = significant(w["code"])
        repl = [v for v in meaning_variants(w["meaning"]) if v["editions"]]
        if (run and not repl and not run["instead"] and run["in"] == list(present)
                and run["significant"] == sig and run["to"] == w["n"] - 1 and run["tagnt"] == w["tagnt"]):
            run["to"] = w["n"]
            run["words"].append(w["greek"])
            run["strongs"].append(w["strongs"])
            run["grammar"].append(w["grammar"])
        else:
            run = {"tagnt": w["tagnt"], "from": w["n"], "to": w["n"], "words": [w["greek"]], "strongs": [w["strongs"]],
                   "grammar": [w["grammar"]], "in": list(present),
                   "absent": [e for e in EDITIONS if e not in present], "significant": sig,
                   "instead": repl}
            out.append(run)
    for r in out:
        # An edition that prints another word in this slot has not omitted it.
        other = {e for v in r["instead"] for e in v["editions"]}
        r["omit"] = [e for e in r["absent"] if e not in other]
    return out


def apparatus_line(osis, rds):
    ch_v = osis.split(".", 1)[1].replace(".", ":")
    parts = []
    for r in rds:
        words = " ".join(r["words"]) if len(r["words"]) <= 6 else \
            " ".join(r["words"][:3]) + " … " + " ".join(r["words"][-2:])
        alts = [f"{v['greek']} {' '.join(v['editions'])}" for v in r["instead"]]
        if r["omit"]:
            alts.append(f"om. {' '.join(r['omit'])}")
        parts.append(f"{words}] {' '.join(r['in']) or '(none)'}; {'; '.join(alts)}"
                     + ("" if r["significant"] else " (minor)"))
    return f"{osis.split('.')[0]} {ch_v}: " + " | ".join(parts)


def build():
    verify_pins()
    rows = read_rows()
    # The registry, not data/nt: four KJV verses (Luke 17:36, Acts 8:37, 15:34,
    # 24:7) are in the TR but not in RP2018, so they have uids but no NT row.
    with open(os.path.join(ROOT, "data", "uids", "wordhoard.uids.json"), encoding="utf-8") as f:
        uid_of = {k[4:]: v for k, v in json.load(f)["uids"].items() if k.startswith("kjv:")}
    units, missing = [], []
    stats = {"words": len(rows), "verses": 0, "units": 0, "readings": 0, "significant": 0,
             "minor": 0, "spelling": 0, "meaning": 0, "displaced": 0}
    for osis, words in verses(rows).items():
        stats["verses"] += 1
        if osis not in uid_of:
            missing.append(osis)
            continue
        rds = readings(words)
        # A KJV verse fed by two TAGNT verses (Matt 17:14, Acts 2:10, ...) has
        # two runs of word numbers, so there every `n` names its TAGNT verse.
        refs = list(dict.fromkeys(w["tagnt"] for w in words))
        at = (lambda w: {"tagnt": w["tagnt"], "n": w["n"]}) if len(refs) > 1 else (lambda w: {"n": w["n"]})
        if len(refs) == 1:
            for r in rds:
                del r["tagnt"]
        spell = [{**at(w), "greek": w["greek"], "variants": spelling_variants(w["spelling"])}
                 for w in words if w["spelling"]]
        mean = [{**at(w), "greek": w["greek"], "variants": meaning_variants(w["meaning"])}
                for w in words if w["meaning"]]
        moved = [{**at(w), "greek": w["greek"],
                  "moved": {e: d for e, d in sorted(w["editions"].items(), key=lambda kv: EDITIONS.index(kv[0])) if d}}
                 for w in words if any(w["editions"].values())]
        wits = [{**at(w), "greek": w["greek"], "witnesses": w["extra"]} for w in words if w["extra"]]
        stats["spelling"] += len(spell)
        stats["meaning"] += len(mean)
        stats["displaced"] += len(moved)
        if not (rds or mean or moved):
            continue
        stats["units"] += 1
        stats["readings"] += len(rds)
        stats["significant"] += sum(1 for r in rds if r["significant"])
        stats["minor"] += sum(1 for r in rds if not r["significant"])
        unit = {"id": f"{SLUG}:{osis}", "ref": osis.split(".")[0] + " " + osis.split(".", 1)[1].replace(".", ":"),
                "text": apparatus_line(osis, rds) if rds else "",
                "links": [{"target": f"kjv:{osis}", "type": "apparatus-of", "resolved": True}],
                "lex": {"passage_uid": uid_of[osis], "tagnt_ref": refs[0],
                        **({"tagnt_refs": refs} if len(refs) > 1 else {}),
                        "readings": rds, "meaning_variants": mean, "word_order": moved,
                        "spelling_variants": spell, "witnesses": wits}}
        units.append(unit)
    if missing:
        raise SystemExit(f"HARD STOP: {len(missing)} TAGNT verses name no KJV verse in data/nt: {missing[:5]}")
    book = {"slug": SLUG, "title": "Greek New Testament: a variant apparatus of eight editions",
            "author": "STEPBible.org / Tyndale House Cambridge (TAGNT)",
            "source": {"path": os.path.relpath(CACHE, os.path.join(ROOT, "data", "corpus")),
                       "format": "tagnt-tsv", "editions": EDITION_NAMES,
                       "sha256": [FILES[r] for r in FILES]},
            "scheme": {"citation": "KJV book chapter:verse (TAGNT's KJV number where it differs "
                                   "from the NRSV's)",
                       "resolution": "word, within the verse",
                       "honesty": "TAGNT's own collation of eight printed editions, not a "
                                  "manuscript apparatus; 'significant' is TAGNT's judgement "
                                  "(upper-case variant codes). Its Byz is RP2005, not data/nt's "
                                  "RP2018: --measure says how far they agree.",
                       "note": "One unit per KJV verse where the editions differ; `text` is a "
                               "readable apparatus line, `lex` the structured readings. Word numbers `n` "
                               "count within a TAGNT verse; where a KJV verse takes words from "
                               "two, `lex.tagnt_refs` lists them and every entry names its own "
                               "`tagnt`. TAGNT's English (Berean) and Spanish columns are never "
                               "read in."},
            "rights": dict(RIGHTS),
            "stats": stats,
            "units": units}
    blob = json.dumps(book, ensure_ascii=False).encode("utf-8")
    return book, blob, entry(book, blob)


def entry(book, blob):
    return {"title": book["title"], "author": book["author"], "format": book["source"]["format"],
            "sha256": book["source"]["sha256"], "units": len(book["units"]),
            "scheme": book["scheme"], "rights": book["rights"], "stats": book["stats"],
            "built_sha256": hashlib.sha256(blob).hexdigest()}


def norm_strongs(s):
    m = re.match(r"G0*(\d+)", s)
    return f"G{m.group(1)}" if m else s


def byz_words(words):
    """TAGNT's Byzantine text of one verse as written, in Byz order: each word
    Byz prints, in Byz's spelling where TAGNT lists one, plus a slot's other
    words where those are Byz's ("meaning variants")."""
    out = []
    for w in words:
        d = w["editions"].get("Byz")
        if d is not None:
            form = w["greek"]
            for v in spelling_variants(w["spelling"]):
                if "Byz" in v["editions"]:
                    form = v["greek"]
            out.append((w["n"] + (d if isinstance(d, int) else 0), w["n"], form.split()))
            continue
        for v in meaning_variants(w["meaning"]):
            if "Byz" in v["editions"]:
                out.append((w["n"], w["n"], v["greek"].split()))
    keys = [N.search_key(re.sub(r"[^\w\u0300-\u036f\u1fbd-\u1fc1\u1fcd-\u1fcf\u1fdd-\u1fdf\u1fed-\u1fef\u1ffd\u1ffe’᾽]", "", x))
            for _, _, forms in sorted(out, key=lambda x: x[:2]) for x in forms]
    return [k for k in keys if k]


def measure():
    """TAGNT's Byz against data/nt's RP2018, verse by verse, word by word (the
    NT's own accentless search key on both sides)."""
    import difflib
    verify_pins()
    rows = read_rows()
    nt = N.load_nt()
    cit = {p["uid"]: p["citation"][4:] for p in nt["passages"]}
    ours = {}
    for t in nt["tokens"]:
        ours.setdefault(cit[t["passage_uid"]], []).append(t["search_key"])
    same = matched = total = 0
    worst = []
    vs = verses(rows)
    for osis, words in vs.items():
        byz, mine = byz_words(words), ours.get(osis, [])
        if byz == mine:
            same += 1
        sm = difflib.SequenceMatcher(None, byz, mine, autojunk=False)
        m = sum(b.size for b in sm.get_matching_blocks())
        matched += m
        total += max(len(byz), len(mine))
        worst.append((m - max(len(byz), len(mine)), osis, len(byz), len(mine)))
    tot = len(vs)
    print(f"  {tot} verses, TAGNT's Byz (RP2005) against data/nt (RP2018), accentless forms:")
    print(f"    identical verses: {same} ({100 * same / tot:.1f}%)")
    print(f"    words in common, in order: {matched:,} of {total:,} ({100 * matched / total:.2f}%)")
    for d, osis, a, b in sorted(worst)[:6]:
        print(f"      most different: {osis} ({a} words in TAGNT's Byz, {b} in RP2018, {-d} apart)")


def write_atomic(path, data):
    with open(path + ".tmp", "wb") as f:
        f.write(data)
    os.replace(path + ".tmp", path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--measure", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    if a.measure:
        return measure()
    book, blob, e = build()
    s = e["stats"]
    print(f"  {s['words']:,} words in {s['verses']:,} verses; {e['units']:,} verses where the "
          f"editions differ: {s['readings']:,} readings ({s['significant']:,} significant, "
          f"{s['minor']:,} minor), {s['meaning']:,} other words in a slot, {s['displaced']:,} "
          f"displaced, {s['spelling']:,} spelling variants")
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    if a.check:
        path = os.path.join(BOOKS, SLUG + ".json")
        if manifest.get(SLUG) != e or (os.path.exists(path) and open(path, "rb").read() != blob):
            raise SystemExit("CHECK FAILED: the rebuilt apparatus differs from the manifest entry")
        print("  CHECK PASSED: the apparatus = its committed manifest entry (built_sha256).")
        return
    write_atomic(os.path.join(BOOKS, SLUG + ".json"), blob)
    manifest[SLUG] = e
    write_atomic(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    print(f"  wrote {SLUG}.json + {len(manifest)}-entry manifest")


if __name__ == "__main__":
    main()
