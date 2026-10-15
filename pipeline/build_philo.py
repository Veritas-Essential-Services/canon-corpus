#!/usr/bin/env python3
"""
build_philo.py -- Philo of Alexandria in Greek (Cohn-Wendland, 1896-1915) and
in English (Yonge, 1854-55), both from the First1KGreek TEI, aligned section
for section.

    python3 pipeline/build_philo.py --fetch   # pinned TEI -> data/corpus/first1k/ (gitignored)
    python3 pipeline/build_philo.py           # build data/books/philo-*.json + manifest entries
    python3 pipeline/build_philo.py --check   # rebuild in memory: = the committed manifest entries
    python3 pipeline/build_philo.py --measure # how Cohn-Wendland number scripture: the evidence
    python3 tests/philo_test.py

WORKS. The 31 treatises that survive in Greek and that First1KGreek carries in
both languages (tlg0018.tlg001-031), from On the Creation to the Embassy to
Gaius: 62 books, a Greek and an English for each. Not here: the works that
survive only in Armenian or Latin (Questions on Genesis and Exodus, On
Providence, On Animals) and the fragments; they have no Cohn-Wendland text.

LICENCE (rule 6). The Greek (Cohn, Wendland and Reiter, Berlin: Reimer,
1896-1915) and Yonge's English (London: Bohn, 1854-55) are public domain.
First1KGreek's TEI of each is "Available under a Creative Commons
Attribution-ShareAlike 4.0 International License", so these books are handled
like the Apostolic Fathers and Josephus: built locally, gitignored, and only
the manifest entries committed, each with a `rights` block and
`redistribute_whole: false`.

CITATION AND ALIGNMENT. Philo is cited by treatise and Cohn-Wendland section
(`Opif. 1`, `Leg. 3.65`, `Spec. 1.177`), with the SBL abbreviations. First1KGreek
keyed BOTH files by those sections: Gregory Crane re-cut Yonge's English to the
sections of David Scholer's edition, which follow Cohn-Wendland (the English
file's revisionDesc says so). So a unit is one section, `philo-opif-cw:1` and
`philo-opif-yonge:1`, each linking to the other. Where one file has a section
the other lacks, the unit has no link and the manifest lists it under
`alignment.unmatched`; nothing is stretched to cover it.

Cohn-Wendland's additions to the transmitted text (<add>) are printed in
angle brackets, as the edition prints them; where the TEI gives a correction
beside the reading (<corr> + <sic>), the correction is the text. The apparatus,
the marginal Mangey page numbers (<note>) and heads are left out of `text`.

SCRIPTURE. Cohn-Wendland print the verse Philo is quoting or reading in
parentheses in the running text, "(Gen. 1,27)". Those are the editors' words,
so they leave `text` for links[] and resolve to KJV verse ids (resolve():
which numbering the editors used, and the measurement behind it).

Yonge's English carries a few of Bohn's running heads and page numbers that
the OCR left in the text; CRUFT lists each, by unit, as a per-book rule.

STRONG'S TAGS on the Greek, by the same fixed rules as the Apostolic Fathers
(build_apostolic_fathers.tag_word), never guessed.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_apostolic_fathers as A  # noqa: E402
import af_scripture as S  # noqa: E402
import versification as VM  # noqa: E402

BOOKS = A.BOOKS
MANIFEST = A.MANIFEST
T = A.T
REPO, COMMIT, CACHE = A.F1K_REPO, A.F1K_COMMIT, A.CACHE
SOURCE_URL = f"https://github.com/{REPO}/tree/{COMMIT}/data/tlg0018"
PINS_PATH = os.path.join(HERE, "philo_pins.json")

# TLG work, slug key, SBL abbreviation, title
WORKS = [
    ("tlg001", "opif", "Opif.", "On the Creation of the World"),
    ("tlg002", "leg", "Leg.", "Allegorical Interpretation"),
    ("tlg003", "cher", "Cher.", "On the Cherubim"),
    ("tlg004", "sacr", "Sacr.", "On the Sacrifices of Cain and Abel"),
    ("tlg005", "det", "Det.", "That the Worse Attacks the Better"),
    ("tlg006", "post", "Post.", "On the Posterity of Cain"),
    ("tlg007", "gig", "Gig.", "On the Giants"),
    ("tlg008", "deus", "Deus", "That God Is Unchangeable"),
    ("tlg009", "agr", "Agr.", "On Agriculture"),
    ("tlg010", "plant", "Plant.", "On Planting"),
    ("tlg011", "ebr", "Ebr.", "On Drunkenness"),
    ("tlg012", "sobr", "Sobr.", "On Sobriety"),
    ("tlg013", "conf", "Conf.", "On the Confusion of Tongues"),
    ("tlg014", "migr", "Migr.", "On the Migration of Abraham"),
    ("tlg015", "her", "Her.", "Who Is the Heir of Divine Things?"),
    ("tlg016", "congr", "Congr.", "On the Preliminary Studies"),
    ("tlg017", "fug", "Fug.", "On Flight and Finding"),
    ("tlg018", "mut", "Mut.", "On the Change of Names"),
    ("tlg019", "somn", "Somn.", "On Dreams"),
    ("tlg020", "abr", "Abr.", "On the Life of Abraham"),
    ("tlg021", "ios", "Ios.", "On the Life of Joseph"),
    ("tlg022", "mos", "Mos.", "On the Life of Moses"),
    ("tlg023", "decal", "Decal.", "On the Decalogue"),
    ("tlg024", "spec", "Spec.", "On the Special Laws"),
    ("tlg025", "virt", "Virt.", "On the Virtues"),
    ("tlg026", "praem", "Praem.", "On Rewards and Punishments"),
    ("tlg027", "prob", "Prob.", "That Every Good Person Is Free"),
    ("tlg028", "contempl", "Contempl.", "On the Contemplative Life"),
    ("tlg029", "aet", "Aet.", "On the Eternity of the World"),
    ("tlg030", "flacc", "Flacc.", "Against Flaccus"),
    ("tlg031", "legat", "Legat.", "On the Embassy to Gaius"),
]
EDITIONS = {
    "cw": {"file": "1st1K-grc1", "lang": "grc", "author": "Philo of Alexandria",
           "edition": "L. Cohn, P. Wendland and S. Reiter, Philonis Alexandrini opera quae "
                      "supersunt (Berlin: Reimer, 1896-1915)"},
    "yonge": {"file": "1st1K-eng1", "lang": "en", "author": "Philo of Alexandria, tr. C. D. Yonge",
              "edition": "C. D. Yonge, The Works of Philo Judaeus (London: Bohn, 1854-55)"},
}
RIGHTS = {
    "license": "CC BY-SA 4.0 (the First1KGreek digital edition); the text, Cohn-Wendland's "
               "Greek (1896-1915) or Yonge's English (1854-55), is public domain",
    "attribution": "First1KGreek, Open Greek and Latin (opengreekandlatin.org)",
    "source_url": SOURCE_URL,
    "redistribute_whole": False,
}
SKIP = {T + "note", T + "head", T + "bibl", T + "sic"}

# Yonge's English, per-book rules (rule 2: the source file is never edited).
# Bohn's running heads, page numbers and printer's colophons that the OCR left
# in the running text: (unit, exact text as read, what it should read). A row
# whose text is no longer there stops the build, so a refetch that changed the
# file is noticed instead of silently half-fixed.
CRUFT = [
    ("philo-plant-yonge:134", "the fifth she 4 called", "the fifth she called"),
    ("philo-sobr-yonge:69", " END OF VOL. I. HADDON, BROTHERS, AND CO., PRINTERS, CASTLE STREET, "
                            "FINSBURY.", ""),
    ("philo-ios-yonge:270", " END OF VOL. II. HADDON, BROTHERS, AND CO., PRINTERS, CASTLE STREET. "
                            "FINSEURY.", ""),
    ("philo-decal-yonge:177", "appropriate task. 3", "appropriate task."),
    ("philo-spec-yonge:1.337", "enumerating ON THOSE WHO OFFER SACRIFICE QAY in", "enumerating in"),
    ("philo-spec-yonge:3.86", "since he was a ON SPECIAL LAWS. 32> murderer", "since he was a murderer"),
    ("philo-virt-yonge:84", "reputation and ON HUMANITY. 43) goodwill", "reputation and goodwill"),
    ("philo-virt-yonge:152", "in vogue . 443 PHILO JUDAUS. among", "in vogue among"),
    ("philo-praem-yonge:90", "a proper reward. ON REWARDS AND PUNISHMENTS, 4iT", "a proper reward."),
    ("philo-praem-yonge:121", "life quite II 2 straight", "life quite straight"),
]

# Cohn-Wendland print the scripture Philo is quoting or reading as a
# parenthesis in the running text: "(Gen. 1,27)", "(ibid. 2)", "(I Reg. 1,28)".
# They are the editors' words, not Philo's, so they come out of `text` and go
# into links[], resolved to KJV verses through Brenton's LXX map (Philo read
# the Septuagint) by pipeline/af_scripture.py. Their Latin book names are put
# into the names that module reads; "ibid." alone is the verse last cited,
# "ibid. 7" verse 7 of that chapter, "ib. 6, 12" chapter 6 of that book.
CW_BOOKS = [(r"\bIV Reg\.", "2 Kings"), (r"\bIII Reg\.", "1 Kings"), (r"\bII Reg\.", "2 Sam."),
            (r"\bI Reg\.", "1 Sam."), (r"\bDeuter\.", "Deut."), (r"\bGenes\.", "Gen."),
            (r"\bPsalm\.?", "Ps."), (r"\bIer\.", "Jer."), (r"\bIes\.", "Is."), (r"\bIob\b", "Job"),
            (r"\bIud\.", "Judg.")]
PAREN = re.compile(r"\s*\(([^()]*\d[^()]*|\s*(?:cf\.\s*)?ib(?:id)?\.\s*)\)")
IBID = re.compile(r"^\s*(?:cf\.\s*)?ib(?:id)?\.\s*(v\.\s*)?")


def rel_path(tlg, ed):
    return f"data/tlg0018/{tlg}/tlg0018.{tlg}.{EDITIONS[ed]['file']}.xml"


def local(rel):
    return A.local(rel)


def pins():
    with open(PINS_PATH, encoding="utf-8") as f:
        return json.load(f)


def fetch():
    import pinned_fetch as F
    p = pins()
    F.fetch(REPO, COMMIT, [(rel, local(rel), p[rel]) for rel in p], ua="canon-corpus/philo")


def verify_pins():
    p = pins()
    bad = [rel for rel, want in p.items()
           if not os.path.exists(local(rel)) or A.sha256_file(local(rel)) != want]
    if bad:
        raise SystemExit(f"pinned inputs missing or changed: {bad[:3]}\n"
                         f"  run: python3 pipeline/build_philo.py --fetch")


def text_of(el):
    """The running text: notes, heads, bibl left out; <add> in angle brackets;
    a <sic> is dropped only where the TEI gives its <corr> beside it."""
    out = [el.text or ""]
    has_corr = el.find(T + "corr") is not None
    for c in el:
        if c.tag == T + "sic" and not has_corr:
            out.append(text_of(c))
        elif c.tag == T + "add":
            out.append("⟨" + text_of(c) + "⟩")
        elif c.tag not in SKIP:
            out.append(text_of(c))
        out.append(c.tail or "")
    return "".join(out)


def read(tlg, ed):
    """[(section key, text)] in document order, and the file's root."""
    rel = rel_path(tlg, ed)
    root = ET.parse(local(rel)).getroot()
    lic = root.find(f".//{T}availability/{T}licence")
    licence = A.clean("".join(lic.itertext())) if lic is not None else ""
    if "Attribution-ShareAlike 4.0" not in licence:
        raise SystemExit(f"HARD STOP: {rel}: licence line is not the CC BY-SA 4.0 recorded "
                         f"({licence!r}); re-read the rights before building")
    body = root.find(f".//{T}body/{T}div")
    rows, seen = [], set()
    for path, div in A.leaves(body):
        k = ".".join(path)
        if k in seen:
            raise SystemExit(f"HARD STOP: {rel}: two textparts cite as {k}")
        seen.add(k)
        rows.append((k, A.clean(text_of(div))))
    return rows, root


def editors(root):
    sd = root.find(f".//{T}sourceDesc")
    names = [A.clean(n.text or "") for n in sd.iter(T + "name")] if sd is not None else []
    dates = [A.clean(d.text or "") for d in sd.iter(T + "date")] if sd is not None else []
    vol = [A.clean(v.text or "") for v in sd.iter(T + "biblScope") if v.get("unit") == "volume"]
    return {"editors": [n for n in names if n], "date": dates[0] if dates else None,
            "volume": vol[0] if vol else None}


def cw_label(raw, last):
    """The parenthesis as af_scripture.parse_label reads it, or None if it
    names no book of scripture. `last` is (book name, chapter, verse) of the
    reference before it in the treatise, for ibid."""
    lab = raw.replace("\u2014", "-").replace("\u2013", "-")
    # A few came through First1KGreek's beta-code converter as Greek letters
    # ("ξφ. δευτ. 28,23" is "cf. Deut. 28,23"): an unaccented Greek word in a
    # reference is put back into Latin, as the Apostolic Fathers' Latin is.
    lab = A.WORD.sub(lambda m: m.group(0) if m.group(0).isascii() or A._marked(m.group(0))
                     else A._latinize(m.group(0)).capitalize(), lab)
    lab = re.sub(r"\b(?:sqq|ss|s|al)\.", " ", lab)
    for pat, name in CW_BOOKS:
        lab = re.sub(pat, name, lab)
    m = IBID.match(lab)
    if m:
        if not last:
            return None
        rest = lab[m.end():]
        if not re.search(r"\d", rest):
            rest = str(last[2]) if last[2] else ""
        verse_only = m.group(1) or not re.match(r"\s*\d+\s*,", rest)
        lab = f"{last[0]} " + (f"{last[1]}, " if verse_only else "") + rest
    # "Gen. 17,15. 16" is two verses; "Gen. 1,27. 2,7" is a second chapter.
    lab = re.sub(r"[.;]\s*(?=\d+\s*,)", "; ", lab)
    return lab if S.label_books(lab) else None


def lxx_numbered(book, ch):
    """Where Cohn-Wendland number as the Septuagint does (see resolve)."""
    return book == "Ps" or (book == "Exod" and ch >= 35)


def resolve(ref, ctx):
    """One Cohn-Wendland reference as link fields.

    Cohn-Wendland do not number in one scheme. They number the Psalms as the
    Septuagint (and the Vulgate) do, "Psalm. 77,49" for the KJV's Ps 78:49,
    and Exodus 35-40 by the Septuagint's chapters, whose order there is not the
    Hebrew's; everywhere else their chapter and verse are the KJV's (and the
    Vulgate's): "Deut. 23,13" is the paddle of the KJV's Deut 23:13, which
    Brenton numbers 23:14. Measured against Yonge's English of the same section
    (`--measure`; 106 references where the readings differ and the English
    decides): this rule agrees 94 times, reading everything through Brenton's
    LXX map 49 times, through the Vulgate map 89, as KJV numbers 69. So the
    rule decides, and where the other reading names a different verse it is
    kept as `alt_target`, as the Apostolic Fathers keep theirs.
    """
    corpus, book, ch, v, end = ref
    if corpus != "lxx":
        return S.resolve(ref, ctx)
    out = {"ref": S.printed(ref), "corpus": corpus}
    if v is None:
        return {**out, "resolved": False, "why": "cites a whole chapter, not a verse"}
    lxx = lxx_numbered(book, ch)

    def one(verse):
        direct = f"kjv:{book}.{ch}.{verse}"
        br = VM.resolve_brenton(f"{book}.{ch}.{verse}", ctx["bmap"], ctx["kjv_ids"])
        if not lxx and direct in ctx["kjv_ids"]:
            r = {"resolved": True, "target": direct, "numbering": "english"}
            if br.get("resolved") and br["target"] != direct:
                r["alt_target"] = br["target"]
            return r
        r = {**br, "numbering": "lxx"}
        if br.get("resolved"):
            r["via"] = "brenton-kjv"
            if br["target"] != direct and direct in ctx["kjv_ids"]:
                r["alt_target"] = direct
        return r

    r = one(v)
    out.update({k: r[k] for k in ("resolved", "target", "spans", "alt_target", "numbering", "via",
                                  "why") if k in r})
    if r.get("resolved") and end and end > v:
        last = one(end)
        if last.get("resolved"):
            out["through"] = last["target"]
    return out


def scripture(units, ctx):
    """Take Cohn-Wendland's references out of the Greek text and into links[]."""
    last = None
    for u in units:
        found = []

        def cut(m):
            nonlocal last
            lab = cw_label(m.group(1), last)
            if lab is None:
                return m.group(0)
            refs = S.parse_label(lab)
            if refs:
                last = (_name(refs[-1][1]), refs[-1][2], refs[-1][3])
            found.extend({"label": m.group(1), **resolve(r, ctx), "source": "label"}
                         for r in refs)
            return ""

        u["text"] = PAREN.sub(cut, u["text"])
        u["links"] = found + u["links"]


def _name(book):
    """A book id (Gen, 1Sam) as a name parse_label reads back."""
    return {"1Sam": "1 Sam.", "2Sam": "2 Sam.", "1Kgs": "1 Kings", "2Kgs": "2 Kings",
            "Exod": "Exod.", "Deut": "Deut.", "Isa": "Is.", "Judg": "Judg."}.get(book, book + ".")


def _paired(u):
    return any(x.get("type") in ("translation", "original") for x in u["links"])


def build_work(tlg, key, abbrev, title, ctx=None):
    out = {}
    read_ = {ed: read(tlg, ed) for ed in EDITIONS}
    keys = {ed: {k for k, t in rows if t} for ed, (rows, _) in read_.items()}
    for ed, (rows, root) in read_.items():
        other = "yonge" if ed == "cw" else "cw"
        slug, oslug = f"philo-{key}-{ed}", f"philo-{key}-{other}"
        units = []
        for k, text in rows:
            if not text:
                continue
            u = {"id": f"{slug}:{k}", "ref": f"{abbrev} {k}", "text": text, "links": []}
            if k in keys[other]:
                u["links"].append({"target": f"{oslug}:{k}",
                                   "type": "translation" if ed == "cw" else "original",
                                   "resolved": True})
            units.append(u)
        if ed == "cw" and ctx is not None:
            scripture(units, ctx)
        if ed == "yonge":
            fix = {i: (old, new) for i, old, new in CRUFT if i.startswith(slug + ":")}
            for u in units:
                if u["id"] in fix:
                    old, new = fix.pop(u["id"])
                    if old not in u["text"]:
                        raise SystemExit(f"HARD STOP: CRUFT row for {u['id']} no longer matches")
                    u["text"] = u["text"].replace(old, new)
            if fix:
                raise SystemExit(f"HARD STOP: CRUFT rows name no unit: {sorted(fix)}")
        e = EDITIONS[ed]
        rel = rel_path(tlg, ed)
        levels = "book.section" if any("." in k for k, _ in rows) else "section"
        out[slug] = {
            "slug": slug, "title": title + (" (Greek)" if ed == "cw" else " (English)"),
            "author": e["author"],
            "source": {"path": os.path.relpath(local(rel), os.path.join(ROOT, "data", "corpus")),
                       "format": "tei-first1k", "edition": e["edition"], "lang": e["lang"],
                       "volume": editors(root), "cts": f"urn:cts:greekLit:tlg0018.{tlg}.{e['file']}",
                       "sha256": A.sha256_file(local(rel))},
            "scheme": {"citation": f"{abbrev} {levels} (Cohn-Wendland)",
                       "resolution": "Cohn-Wendland section",
                       "honesty": ("exact to Cohn-Wendland's sections; the Greek is First1KGreek's "
                                   "OCR of the Berlin edition, corrected but not proofread here"
                                   if ed == "cw" else
                                   "Yonge's English as First1KGreek re-cut it to Cohn-Wendland's "
                                   "sections (after Scholer's edition); a section boundary in a "
                                   "translation is approximate, and sections the file lacks are "
                                   "listed under alignment.unmatched of the Greek"),
                       "note": "The apparatus, marginal Mangey pages and heads are left out of "
                               "`text`" + ("; editorial additions (<add>) are printed as ⟨ ⟩"
                                           if ed == "cw" else "")},
            "rights": dict(RIGHTS),
            "alignment": {"counterpart": oslug, "units": len(units),
                          "matched": sum(1 for u in units if _paired(u)),
                          "unmatched": [u["id"].split(":", 1)[1] for u in units if not _paired(u)]},
            "units": units,
        }
    return out


def scripture_context():
    with open(os.path.join(ROOT, "data", "uids", "wordhoard.uids.json"), encoding="utf-8") as f:
        kjv_ids = {k for k in json.load(f)["uids"] if k.startswith("kjv:")}
    return {"kjv_ids": kjv_ids, "bmap": VM.load(VM.BRENTON_PATH), "af_ids": set()}


STOP = set("the and of to a in that he his for is it be with as not by thou thee they them "
           "shall unto but from was which all this have will your you my me on at or are so an "
           "their there were".split())


def measure(built):
    """The evidence for resolve()'s rule. For every reference whose readings
    differ (Brenton's map, the Vulgate map, the number read as the KJV's, and
    the rule), score each reading by the content words its verse shares, in
    Brenton's English, with Yonge's English of the same section, and count how
    often each reading is among the best. Needs Brenton's text
    (build_brenton_versification.py --fetch). Writes nothing."""
    import build_brenton_versification as BB
    words = lambda t: {w for w in re.findall(r"[a-z]+", t.lower()) if w not in STOP and len(w) > 2}  # noqa: E731
    bren = dict(BB.brenton())
    ctx = scripture_context()
    bmap, vmap, kjv = ctx["bmap"], VM.load(VM.VULGATE_PATH), ctx["kjv_ids"]
    back = {}
    for k in bren:
        for t in VM.targets(k, bmap):
            back.setdefault(t, []).append(k)
    score = lambda E, t: max([len(E & words(bren[b])) for b in back.get(t[4:], [])] or [-1]) if t else -1  # noqa: E731
    tally, n = {"rule": 0, "brenton": 0, "vulgate": 0, "kjv-number": 0}, 0
    for slug, (book, _, _) in built.items():
        if not slug.endswith("-cw"):
            continue
        eng = {u["id"].split(":", 1)[1]: u["text"] for u in built[slug[:-3] + "-yonge"][0]["units"]}
        for u in book["units"]:
            E = words(eng.get(u["id"].split(":", 1)[1], ""))
            for x in u["links"]:
                if x.get("corpus") != "lxx" or ":" not in x.get("ref", "") or "-" in x["ref"]:
                    continue
                b, cv = x["ref"].split(" ")
                o = f"{b}.{cv.replace(':', '.')}"
                c = {"rule": x.get("target"),
                     "brenton": VM.resolve_brenton(o, bmap, kjv).get("target"),
                     "vulgate": VM.resolve_vulgate(o, vmap, kjv).get("target"),
                     "kjv-number": f"kjv:{o}" if f"kjv:{o}" in kjv else None}
                if len(set(c.values())) == 1:
                    continue
                sc = {k: score(E, t) for k, t in c.items()}
                best = max(sc.values())
                if best <= 0:
                    continue
                n += 1
                for k in c:
                    tally[k] += sc[k] == best
    print(f"  {n} references where the readings differ and Yonge's English decides:")
    for k, v in tally.items():
        print(f"    {k:<11}{v:>4}  among the best")


def entry(book, blob):
    e = {"title": book["title"], "author": book["author"], "format": book["source"]["format"],
         "sha256": book["source"]["sha256"], "units": len(book["units"]),
         "scheme": book["scheme"], "rights": book["rights"], "alignment": book["alignment"]}
    if "tagging" in book:
        e["tagging"] = {k: v for k, v in book["tagging"].items() if k != "scheme"}
        refs = [x for u in book["units"] for x in u["links"] if "label" in x]
        e["scripture_refs"] = len(refs)
        e["scripture_refs_resolved"] = sum(1 for x in refs if x["resolved"])
    e["built_sha256"] = hashlib.sha256(blob).hexdigest()
    return e


def build():
    verify_pins()
    tables = A.tag_tables()
    ctx = scripture_context()
    out = {}
    for tlg, key, abbrev, title in WORKS:
        for slug, book in build_work(tlg, key, abbrev, title, ctx).items():
            if slug.endswith("-cw"):
                book = A.tag(book, tables)
            blob = json.dumps(book, ensure_ascii=False).encode("utf-8")
            out[slug] = (book, blob, entry(book, blob))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--measure", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    built = build()
    if a.measure:
        return measure(built)
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    words = tagged = 0
    for slug, (book, _, e) in built.items():
        al = e["alignment"]
        t = e.get("tagging")
        if t:
            words += t["words"]
            tagged += sum(t[r] for r in A.RULES)
        tag = (f" {100 * sum(t[r] for r in A.RULES) / t['words']:5.1f}% of {t['words']:,} words tagged"
               if t else "")
        print(f"  {slug:<22}{e['units']:>5} units {al['matched']:>5} aligned "
              f"{len(al['unmatched']):>3} unaligned{tag}")
    print(f"  Greek: {words:,} words, {100 * tagged / words:.1f}% tagged")
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
        A.write_atomic(os.path.join(BOOKS, slug + ".json"), blob)
        manifest[slug] = e
    A.write_atomic(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False).encode("utf-8"))
    print(f"  wrote {len(built)} books + {len(manifest)}-entry manifest")


if __name__ == "__main__":
    main()
