#!/usr/bin/env python3
# fable_review: pending
"""
build_ot_corpus.py -- the Hebrew Old Testament (the Westminster Leningrad
Codex) in the four-file corpus format, one row per VERSE, every record keyed
by the KJV verse's EXISTING uid. The Greek NT's sister (build_nt_corpus.py);
the differences are written down in pipeline/README-ot-jsonl.md.

    python3 pipeline/build_ot_corpus.py             # build, write data/ot/
    python3 pipeline/build_ot_corpus.py --check     # rebuild: mint 0, byte-identical
    python3 pipeline/build_ot_corpus.py --report    # counts only, no write

    Inputs (pinned, gitignored): the WLC as the Open Scriptures Hebrew Bible
    ships it (build_versification.WLC_PINS, data/corpus/wlc/), and the
    Hebrew->KJV verse map data/versification/bhs-kjv.json (PR #5).
    Output: data/ot/<Book>/{passages,witnesses,tokens,alignments}.jsonl and
    one data/ot/manifest.json. Validator: tests/ot_corpus_test.py.

WHAT IS COMMITTED, AND WHAT IS NOT (the licence gate, ADR 0001 / launch plan D4)
    The WLC TEXT is public domain (its <work> block: "Public Domain"). OSHB's
    LEMMAS and MORPHOLOGY (the lemma= and morph= attributes, the "/" morpheme
    splits, the word ids) are CC BY 4.0 (morphhb README: "Lemma and
    morphology data are licensed under a Creative Commons Attribution 4.0
    International license"). This public repo commits only PD or own work,
    and CC BY is collected, never served whole (CLAUDE.md, the STEPBible
    precedent). So these files carry the Hebrew words, their order, ketiv and
    qere, and the codex's section marks -- and NO lemma, parsing or gloss.
    Those fields are null with the reason, and the manifest says so. Admitting
    OSHB's layer waits on ADR 0019, the ruling that would admit SBLGNT.

IDENTITY: THE VERSE ALREADY HAS ONE (house style s.2)
    Every WLC verse is read through the Hebrew->KJV map. The registry is opened
    FROZEN: a Hebrew verse is a witness of the KJV verse's passage, or it is
    left out and counted. Nothing is minted. Three cases the map raises, each
    a house DEFAULT until Adam rules (README-ot-jsonl.md s.4):
      - a Hebrew verse that is a psalm title (67): the KJV numbers no title,
        so there is no uid; left out, listed in the manifest with its text's
        location. A citation grammar for titles would be a ruling (R5).
      - a Hebrew verse holding two KJV verses (2): a witness of the one KJV
        verse no other Hebrew verse reaches, its alignment naming both.
      - a Hebrew verse numbered differently: a witness of the KJV uid, with
        the WLC's own reference as `wlc_ref` (the doxology's rule in the NT).
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
import wh_uid as U  # noqa: E402
import build_versification as V  # noqa: E402
import versification as VM  # noqa: E402

UIDS = os.path.join(ROOT, "data", "uids", "wordhoard.uids.json")
OUT = os.path.join(ROOT, "data", "ot")
FILES = ("passages", "witnesses", "tokens", "alignments")
SCHEMA = "wordhoard/corpus-jsonl/v1"
BUILT_ON = "2026-10-02"   # a constant so a rebuild is byte-identical
WITNESS = "hbo.wlc"       # Biblical Hebrew, the Westminster Leningrad Codex
FACING = "kjv.plain"
BOOKS = V.OT              # the 39 OSIS books, in the KJV's order
SCOPE = list(BOOKS)       # build() takes a narrowed list; main() never writes one
SHARD = "book"            # data/ot/<Book>/; None writes four flat files

NS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"
MAQQEF, SOF_PASUQ, PASEQ, NUN = "־", "׃", "׀", "׆"
MARKS = SOF_PASUQ + PASEQ + NUN       # printed signs that are not words
SECTION = {"x-pe": "pe", "x-samekh": "samekh"}   # open / closed paragraph
FINALS = str.maketrans("ךםןףץ", "כמנפצ")

SOURCES = {
    "wlc-4.20": {
        "what": "Hebrew text: words, ketiv and qere, section marks (pe, samekh)",
        "edition": ("Westminster Leningrad Codex 4.20 (J. Alan Groves Center), as encoded by the "
                    "Open Scriptures Hebrew Bible, github.com/openscriptures/morphhb commit "
                    + V.WLC_COMMIT[:7]),
        "license": "PD",
        "license_basis": [
            {"where": "morphhb wlc/*.xml, <work osisWork=\"WLC\"> <rights>",
             "says": "Public Domain"},
            {"where": "morphhb README.md",
             "says": ("Lemma and morphology data are licensed under a Creative Commons Attribution "
                      "4.0 International license. ... The text of the WLC remains in the Public "
                      "Domain.")},
        ],
        "taken": "the text of each <w> (morpheme slashes removed), maqqef, sof pasuq, paseq, "
                 "inverted nun, pe/samekh, and the qere of each x-qere reading",
        "not_taken": ("OSHB's lemma=, morph=, id= and n= attributes and its morpheme splits: "
                      "CC BY 4.0, outside this repo's licence gate"),
        "source_url": "https://github.com/openscriptures/morphhb/tree/" + V.WLC_COMMIT,
        "redistribute_whole": True,
        "verified": True,
        "verified_on": BUILT_ON,
    },
}
ALLOWED_LICENSES = ("PD", "own")

TOKEN_FIELDS = {
    "surface": "the WLC word as written (the ketiv where there is one), OSHB's morpheme slashes removed",
    "normalized": "derived: NFC(surface)",
    "search_key": "derived: consonants only -- every point and accent dropped, final forms folded",
    "translit": "null: no house Hebrew transliteration scheme yet (README-ot-jsonl.md s.6)",
    "lemma": "null: OSHB's lemmas are CC BY 4.0 and withheld by the licence gate",
    "parsing": "null: OSHB's morphology is CC BY 4.0 and withheld by the licence gate",
    "gloss": "null: there is no lemma to gloss from",
    "plain_form": "null",
}
WITHHELD = {"lemma": {"source": None, "status": "withheld", "why": "oshb-cc-by"},
            "parsing": {"source": None, "status": "withheld", "why": "oshb-cc-by"},
            "gloss": {"source": None, "status": "none", "why": "no lemma"}}

RULINGS = {
    "psalm-titles": {
        "status": "house default, awaiting Adam's ruling",
        "default": ("a Hebrew verse that is a psalm title has no KJV uid (the KJV numbers no "
                    "title), so it is left out and listed under versification.left_out"),
        "alternative": ("a citation grammar for titles (e.g. kjv:Ps.51.title) is a registry "
                        "ruling: once minted a uid is never taken back (R5)"),
    },
    "spans": {
        "status": "house default, awaiting Adam's ruling",
        "default": ("a Hebrew verse holding two KJV verses (2: Ps 13:6, Isa 63:19) is a witness of "
                    "the first KJV verse no other Hebrew verse reaches; its alignment names both "
                    "(type 1:2), and the other KJV verse has no Hebrew witness of its own"),
    },
    "joined": {
        "status": "house default, awaiting Adam's ruling",
        "default": ("two Hebrew verses that make one KJV verse (4: Num 26:1, 1 Sam 20:42, 1 Kgs "
                    "22:43, 1 Chr 12:4) are ONE witness of that verse: their texts joined in codex "
                    "order, tokens numbered straight through, wlc_ref listing both and "
                    "wlc_verse_starts the token where each begins"),
    },
    "sharding": {
        "status": "house default, awaiting Adam's ruling (the NT's, PR #8)",
        "default": "one folder per book under data/ot/, one manifest",
    },
    "lemmas": {
        "status": "withheld by the licence gate until ADR 0019",
        "default": "no lemma, parsing or gloss in these files",
        "alternative": ("admit OSHB's CC BY layer as its own file keyed by token address, with its "
                        "rights block and attribution, never merged into the PD files"),
    },
}


def search_key(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch) and ch not in MAQQEF + MARKS + "/")
    return s.translate(FINALS)


def tokenize(text):
    """A witness text back to its words: maqqef and spaces divide, the
    printed signs (sof pasuq, paseq, inverted nun) are not words."""
    return [w.strip(MARKS) for w in text.replace(MAQQEF, " ").split() if w.strip(MARKS)]


def _word(el):
    return "".join(el.itertext()).replace("/", "")


def read_book(osis):
    """[(wlc_ref, verse)] in the codex's order. A verse is {pieces, words,
    section, qere_only, notes}: `pieces` rebuild the printed line, each word
    {surface, ketiv, qere}."""
    root = ET.parse(os.path.join(V.WLC_DIR, osis + ".xml")).getroot()
    out = []
    for v in root.iter(NS + "verse"):
        ref = v.get("osisID")
        words, pieces, section, qere_only, notes = [], [], None, [], {}
        join_next = False
        prev = None
        for el in v:
            tag, typ = el.tag[len(NS):], el.get("type")
            if tag == "w" and prev is not None and prev.tag == NS + "w" and not (prev.tail or "").strip(" \n\t") \
                    and not re.search(r"\s", prev.tail or ""):
                # No space between two <w>: ONE word of the codex that OSHB divided
                # "for exegesis" (its own note says so). The WLC word is the token.
                words[-1]["surface"] += _word(el)
                words[-1]["divided"] = True
                pieces[-1] += _word(el)
                prev = el
                continue
            prev = el
            if tag == "w":
                w = {"surface": _word(el), "ketiv": typ == "x-ketiv", "qere": None}
                words.append(w)
                pieces.append(("" if join_next or not pieces else " ") + w["surface"])
                join_next = False
            elif tag == "seg" and typ == "x-maqqef":
                pieces.append(MAQQEF)
                join_next = True
            elif tag == "seg" and typ == "x-sof-pasuq":
                pieces.append(SOF_PASUQ)
            elif tag == "seg" and typ == "x-paseq":
                pieces.append(" " + PASEQ)
            elif tag == "seg" and typ == "x-reversednun":
                pieces.append(" " + NUN)
            elif tag == "seg" and typ in SECTION:
                section = SECTION[typ]
            elif tag == "note" and typ == "variant":
                q, glue = "", ""
                for r in el.iter():
                    if r.tag == NS + "w":
                        q += glue + _word(r)
                        glue = " "
                    elif r.tag == NS + "seg" and r.get("type") == "x-maqqef":
                        q += MAQQEF
                        glue = ""
                if words and words[-1]["ketiv"] and words[-1]["qere"] is None:
                    words[-1]["qere"] = q or None
                    words[-1]["not_read"] = not q     # an empty qere: ketiv wela qere
                    cw = el.find(NS + "catchWord")
                    span = len((cw.text or "").replace(MAQQEF, " ").split()) if cw is not None else 1
                    for back in range(2, span + 1):    # one qere read for two written words
                        words[-back]["qere_at"] = len(words)
                else:                        # qere wela ketiv: read, not written
                    qere_only.append({"after": len(words), "qere": q})
            elif tag == "note":
                k = el.get("n") or el.get("type") or "?"
                notes[k] = notes.get(k, 0) + 1
            else:
                raise SystemExit(f"HARD STOP: {ref}: unexpected <{tag} type={typ}>")
        out.append((ref, {"text": "".join(pieces).strip(), "words": words, "section": section,
                          "qere_only": qere_only, "notes": notes}))
    return out


def build(reg):
    bad = [b for b in SCOPE if not os.path.exists(os.path.join(V.WLC_DIR, b + ".xml"))
           or V.sha256(os.path.join(V.WLC_DIR, b + ".xml")) != V.WLC_PINS[b]]
    if bad:     # the map itself is committed; only the WLC is an input here
        raise SystemExit(f"HARD STOP: WLC input missing or changed: {bad[:5]}. "
                         f"Run: python3 pipeline/build_versification.py --fetch")
    vm = VM.load()
    reached = {}          # KJV ref -> the Hebrew verses whose map lands on it
    plan = []
    for osis in SCOPE:
        for ref, verse in read_book(osis):
            ts = VM.targets(ref, vm)
            plan.append((osis, ref, verse, ts))
            for t in ts:
                reached.setdefault(t, []).append(ref)

    passages, witnesses, tokens, alignments = [], [], [], []
    left_out, renumbered, spans, shards, notes = [], [], [], {}, {}
    seen, joined, divided = {}, [], 0
    groups = []           # (osis, primary KJV ref, [(wlc ref, verse, targets)]) in codex order
    for osis, ref, verse, ts in plan:
        sh = shards.setdefault(osis, {"verses": 0, "tokens": 0, "dir": osis if SHARD else ""})
        for k, n in verse["notes"].items():
            notes[k] = notes.get(k, 0) + n
        if any(t.endswith(".title") for t in ts):
            left_out.append({"wlc": ref, "kjv": ts[0], "why": "psalm title: the KJV numbers no title",
                             "words": len(verse["words"])})
            continue
        if len(ts) == 1:
            primary = ts[0]
        else:
            own = [t for t in ts if reached[t] == [ref]]
            if not own:
                raise SystemExit(f"HARD STOP: {ref} spans {ts}, every one reached by another verse")
            primary = own[0]
            spans.append({"wlc": ref, "kjv": ts, "witness_on": primary})
        if groups and groups[-1][1] == primary:
            groups[-1][2].append((ref, verse, ts))     # two Hebrew verses, one KJV verse
        elif primary in seen:
            raise SystemExit(f"HARD STOP: kjv:{primary} is reached by {seen[primary]} and, "
                             f"not next to it, {ref}")
        else:
            groups.append((osis, primary, [(ref, verse, ts)]))
        seen.setdefault(primary, []).append(ref)

    for osis, primary, members in groups:
        sh = shards[osis]
        refs = [r for r, _, _ in members]
        ts = members[0][2] if len(members) == 1 else [primary]   # the KJV verse(s) it faces
        verse = {"text": " ".join(v["text"] for _, v, _ in members),
                 "words": [w for _, v, _ in members for w in v["words"]],
                 "section": members[-1][1]["section"], "qere_only": [], "starts": []}
        n = 0
        for _, v, _ in members:
            verse["starts"].append(n + 1)
            verse["qere_only"] += [dict(q, after=q["after"] + n) for q in v["qere_only"]]
            n += len(v["words"])
        citation = "kjv:" + primary
        try:
            uid = reg.uid_for(citation)
        except U.WhUidError:
            raise SystemExit(f"HARD STOP: {citation} has no uid. Nothing is minted for a Hebrew verse.")
        b, ch, vs = primary.split(".")
        passages.append({"uid": uid, "citation": citation, "kind": "passage", "unit": "verse",
                         "book": b, "osis": primary, "chapter": int(ch), "verse": int(vs),
                         "versification": "kjv", "pericope": None, "reading_of_record": FACING,
                         "status": "machine-built from public-domain sources, unchecked"})
        w = {"address": U.address(uid, WITNESS), "passage_uid": uid, "name": WITNESS,
             "lang": "hbo", "role": "original", "register": "biblical", "textform": "masoretic",
             "text": verse["text"], "section_mark": verse["section"], "generated": False,
             "source": "wlc-4.20", "attested": "Y", "reading_of_record": False}
        if len(members) > 1:
            w["wlc_ref"] = refs
            w["wlc_verse_starts"] = verse["starts"]
            joined.append({"kjv": primary, "wlc": refs})
            renumbered.extend(r for r in refs if r != primary)
        elif refs[0] != primary:
            w["wlc_ref"] = refs[0]
            renumbered.append(refs[0])
        if verse["qere_only"]:
            w["qere_only"] = verse["qere_only"]
        witnesses.append(w)
        divided += sum(1 for wd in verse["words"] if wd.get("divided"))
        for pos, wd in enumerate(verse["words"], 1):
            norm = unicodedata.normalize("NFC", wd["surface"])
            t = {"address": U.address(uid, f"{WITNESS}.t{pos:02d}"), "passage_uid": uid,
                 "witness": WITNESS, "position": pos, "surface": wd["surface"], "normalized": norm,
                 "search_key": search_key(norm), "translit": None, "lemma": None, "lemma_key": None,
                 "parsing": None, "gloss": None, "plain_form": None, "syntax": None,
                 "provenance": None, "review": None}   # every token's is WITHHELD: the manifest says it once
            if wd["ketiv"]:
                t["ketiv"] = True
                t["qere"] = wd["qere"]
                if wd.get("qere_at"):
                    t["qere_at"] = wd["qere_at"]   # its qere is on the token at this position
                if wd.get("not_read"):
                    t["not_read"] = True     # written, not read: the qere is empty
            tokens.append(t)
        alignments.append({
            "alignment_id": f"{U.address(uid, WITNESS)}~{FACING}", "level": "section",
            "type": "1:1" if len(ts) == 1 else f"1:{len(ts)}",
            "a": [{"address": U.address(uid, WITNESS), "tokens": None}],
            "b": [{"address": U.address(reg.uid_for('kjv:' + t), FACING), "tokens": None} for t in ts],
            "confidence": "high" if len(ts) == 1 else "medium",
            "note": ("verse to verse under one uid; the KJV translates the Masoretic text, but not "
                     "this codex's every reading, so this aligns verses, not readings")})
        sh["verses"] += 1
        sh["tokens"] += len(verse["words"])

    books = set(SCOPE)
    built = {p["citation"] for p in passages}
    no_hbo = sorted(c for c in reg.map if c.startswith("kjv:") and c[4:].split(".")[0] in books
                    and c not in built)
    manifest = {
        "schema": SCHEMA, "doc": "pipeline/README-ot-jsonl.md", "built_on": BUILT_ON,
        "row_unit": "verse",
        "selection": {"title": "The Hebrew Old Testament (Westminster Leningrad Codex)",
                      "books": list(SCOPE)},
        "counts": {"passages": len(passages), "verses": len(passages), "witnesses": len(witnesses),
                   "tokens": len(tokens), "alignments": len(alignments),
                   "wlc_verses_read": len(plan), "wlc_verses_left_out": len(left_out),
                   "ketiv": sum(1 for t in tokens if t.get("ketiv")),
                   "ketiv_with_qere": sum(1 for t in tokens if t.get("qere")),
                   "ketiv_not_read": sum(1 for t in tokens if t.get("not_read")),
                   "words_oshb_divided": divided,
                   "qere_only": sum(len(w.get("qere_only", [])) for w in witnesses),
                   "tokens_with_lemma": 0, "tokens_with_parsing": 0, "tokens_with_gloss": 0},
        "shards": {"layout": SHARD or "flat", "order": list(SCOPE), "books": shards,
                   "ruling": RULINGS["sharding"]},
        "versification": {
            "of_record": "kjv", "map": "data/versification/bhs-kjv.json",
            "map_sha256": hashlib.sha256(open(VM.PATH, "rb").read()).hexdigest(),
            "map_rights": vm["rights"],
            "renumbered": len(renumbered), "spans": spans, "joined": joined, "left_out": left_out,
            "kjv_verses_without_hbo": no_hbo,
            "rulings": {k: RULINGS[k] for k in ("psalm-titles", "spans", "joined")}},
        "identity": {"rule": ("a Hebrew verse is a witness of the KJV verse passage that already "
                              "exists; registry opened frozen; nothing minted"),
                     "citation_slug": "kjv names the versification of record, not the language",
                     "reading_of_record": {"value": FACING, "note": "unchanged; a ruling"}},
        "witness": {"name": WITNESS, "lang": "hbo", "textform": "masoretic", "facing": FACING},
        "licence_gate": {"allowed": list(ALLOWED_LICENSES),
                         "rule": "launch plan D4 / ADR 0001: public-domain editions or own work only",
                         "withheld": RULINGS["lemmas"]},
        "sources": SOURCES,
        "token_fields": TOKEN_FIELDS,
        "token_provenance": {"every_token": WITHHELD,
                             "why": ("identical for every token, so stated once here and "
                                     "null on each token (saves about 55 MB)"),
                             "codes": {"oshb-cc-by": ("OSHB's lemma/morph attributes are CC BY 4.0: "
                                                      "collected, not committed (ADR 0001)")}},
        "wlc_notes_by_n": dict(sorted(notes.items())),
        "inputs_sha256": {f"wlc/{b}.xml": V.WLC_PINS[b] for b in SCOPE},
        "files_sha256": {},
    }
    return {"passages": passages, "witnesses": witnesses, "tokens": tokens,
            "alignments": alignments}, manifest


def serialize(records):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8")


def render_all(data, manifest):
    book_of = {p["uid"]: p["book"] for p in data["passages"]}
    uid = {"passages": lambda r: r["uid"],
           "alignments": lambda r: U.parse_address(r["a"][0]["address"])["uid"]}
    blobs = {}
    for k, recs in data.items():
        if SHARD:
            per = {b: [] for b in manifest["shards"]["order"]}
            for r in recs:
                per[book_of[uid.get(k, lambda r: r["passage_uid"])(r)]].append(r)
            blobs.update({f"{b}/{k}.jsonl": serialize(v) for b, v in per.items()})
        else:
            blobs[f"{k}.jsonl"] = serialize(recs)
    manifest["files_sha256"] = {k: hashlib.sha256(v).hexdigest() for k, v in sorted(blobs.items())}
    blobs["manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return blobs


def stale_outputs(out, blobs):
    found = []
    for d, _, fs in os.walk(out):
        for f in fs:
            if f.endswith(".jsonl") or f == "manifest.json":
                rel = os.path.relpath(os.path.join(d, f), out).replace(os.sep, "/")
                if rel not in blobs:
                    found.append(rel)
    return sorted(found)


def load_ot(root=ROOT, books=None):
    """The committed OT, {passages, witnesses, tokens, alignments, manifest},
    following the manifest's shards, in canon order."""
    d = os.path.join(root, "data", "ot")
    with open(os.path.join(d, "manifest.json"), encoding="utf-8") as fh:
        man = json.load(fh)
    sh = man["shards"]
    out = {k: [] for k in FILES}
    for b in ([None] if sh["layout"] == "flat" else sh["order"]):
        if b is not None and books is not None and b not in books:
            continue
        for k in FILES:
            rel = f"{k}.jsonl" if b is None else f"{sh['books'][b]['dir']}/{k}.jsonl"
            with open(os.path.join(d, rel), encoding="utf-8") as fh:
                out[k].extend(json.loads(line) for line in fh if line.strip())
    out["manifest"] = man
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--uids", default=UIDS)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    if not a.report and sorted(SCOPE) != sorted(BOOKS):
        raise SystemExit("HARD STOP: SCOPE is narrowed; writing or checking it would drop the other "
                         "books from data/ot/. Use --report, or restore SCOPE to every book.")
    reg = U.WhUidRegistry(a.uids, frozen=True)
    data, manifest = build(reg)
    blobs = render_all(data, manifest)
    for k, v in manifest["counts"].items():
        print(f"  {k:<24}{v:>8,}")
    s = reg.stats()
    print(f"  uids minted {s['minted']} / reused {s['reused']} / registry total {s['total']:,}")
    reg.assert_no_mint()
    if a.check:
        bad = [fn for fn, blob in blobs.items() if not os.path.exists(os.path.join(a.out, fn))
               or open(os.path.join(a.out, fn), "rb").read() != blob]
        if bad or stale_outputs(a.out, blobs):
            raise SystemExit(f"CHECK FAILED: {(bad or stale_outputs(a.out, blobs))[:8]}")
        print("  CHECK PASSED: minted 0, output byte-identical.")
        return
    if a.report:
        return
    for fn, blob in sorted(blobs.items(), key=lambda kv: kv[0] == "manifest.json"):
        p = os.path.join(a.out, fn)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p + ".tmp", "wb") as f:
            f.write(blob)
        os.replace(p + ".tmp", p)
    for fn in stale_outputs(a.out, blobs):
        os.remove(os.path.join(a.out, fn))
    print(f"  wrote {a.out}: {len(blobs)} files")


if __name__ == "__main__":
    main()
