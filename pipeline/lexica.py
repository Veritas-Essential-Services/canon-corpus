#!/usr/bin/env python3
"""lexica.py -- the shareable lexicons, and the STEPBible supplement.

Adam's ruling, 2026-09-29: the public Greek and Latin lexicons come from
sources that may be shared whole, and STEPBible is used ONLY for what they do
not have, plus the two things STEP did that nobody else has: its Septuagint
(and other beyond-Strong's) vocabulary, and its splits of one Strong's
number into the different words it covers.

  lsj-perseus      Liddell-Scott-Jones, Perseus Digital Library TEI (CC BY-SA 4.0).
                   116,497 entries; Greek in Beta Code, converted (betacode.py).
                   422,262 quotations carry their CTS URN: kept as links.
  abbott-smith     Abbott-Smith, Manual Greek Lexicon of the NT (1922), TEI by
                   translatable-exegetical-tools; the repo states lexicon AND
                   markup are public domain. Entries carry their Strong's number.
  lewis-short      Lewis & Short, A Latin Dictionary (1879), Perseus TEI (CC BY-SA
                   4.0), the eng2 file (Greek already Unicode). Quotations carry
                   CTS URNs: kept as links.
  step-greek-supplement
                   The STEPBible entries (CC BY 4.0) that are (a) numbered G6000+
                   (the LXX / beyond-Strong's vocabulary), (b) one of two or more
                   extended keys on one Strong's number (the splits), or (c) a
                   headword neither lsj-perseus nor abbott-smith has. ONE text per
                   entry -- the TFLSJ (full) text where STEP has both, else TBESG
                   -- never both editions. Measured 2026-09-29: 4,329 of 9,550
                   keys (3,841 G6000+, 297 splits, 586 gaps; categories overlap).

The whole STEP books (tbesg-greek, lsj-greek) are unchanged and stay
redistribute_whole: false. A CC BY-SA book cites its quotations by URN with
`resolved: false` until the Perseus shelf exists to resolve them to unit ids:
a labelled hole, as BDB's scripture citations are (CLAUDE.md, rule 4)."""
import json, os, re, sys, unicodedata, xml.etree.ElementTree as ET
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from betacode import to_unicode, headword_key, accented_key

PERSEUS_RIGHTS = {"license": "CC BY-SA 4.0",
                  "attribution": "Perseus Digital Library, Tufts University",
                  "source_url": "https://github.com/PerseusDL/lexica",
                  "share_alike": True,
                  "note": "May be shared whole with attribution; anything built on it is CC BY-SA too."}
STEP_ATTRIBUTION = ("Data created by www.STEPBible.org based on work at Tyndale House "
                    "Cambridge (CC BY 4.0)")


def _ws(s):
    return re.sub(r"\s+", " ", s).strip()


def _sha256(paths):
    import hashlib
    h = hashlib.sha256()
    for p in paths:
        with open(p, "rb") as f:
            h.update(f.read())
    return h.hexdigest()


def _cites(entry):
    """[{kind: cites, urn, passage, label, resolved: false}] from <bibl n="urn:cts:...">."""
    out = []
    for b in entry.iter("bibl"):
        n = b.get("n") or ""
        if not n.startswith("urn:cts:"):
            continue
        parts = n.split(":")
        work = ":".join(parts[:4])
        passage = ".".join(parts[4:]) if len(parts) > 4 else ""
        out.append({"kind": "cites", "urn": work, "passage": passage,
                    "label": _ws("".join(b.itertext())), "resolved": False})
    return out


def _lsj_text(el, greek=False):
    """Text of an LSJ element, with every lang="greek" run turned from Beta
    Code into Unicode. A child's tail belongs to its parent's language."""
    g = greek or el.get("lang") == "greek"
    parts = [to_unicode(el.text) if (g and el.text) else (el.text or "")]
    for c in el:
        parts.append(_lsj_text(c, g))
        if c.tail:
            parts.append(to_unicode(c.tail) if g else c.tail)
    return "".join(parts)


def lsj_headwords(paths):
    """{headword_key: [unit id]} -- cheap, read straight off the keys."""
    out = defaultdict(list)
    for p in paths:
        for k in re.findall(r'<entryFree[^>]*?key="([^"]+)"', open(p, encoding="utf-8").read()):
            out[headword_key(to_unicode(re.sub(r"\d+$", "", k)))].append("lsj-perseus:" + _lsj_id(k))
    return out


def _lsj_id(key):
    m = re.match(r"^(.*?)(\d+)$", key)
    base, hom = (m.group(1), m.group(2)) if m else (key, "")
    return to_unicode(base).replace(" ", "_") + (f"~h{hom}" if hom else "")


def convert_lsj_perseus(paths, slug="lsj-perseus"):
    units, cites = [], 0
    for p in sorted(paths, key=lambda x: int(re.search(r"eng(\d+)", x).group(1))):
        for e in ET.parse(p).getroot().iter("entryFree"):
            key = e.get("key") or ""
            orth = e.find("orth")
            lemma = _ws(to_unicode(orth.text or "")) if orth is not None and orth.text else to_unicode(re.sub(r"\d+$", "", key))
            # Perseus's own <*> (uncertain reading) and trailing punctuation are not the headword
            lemma = re.sub(r"<\*>", "", lemma).strip(" ,.;:·|") or lemma
            links = _cites(e)
            cites += len(links)
            hom = re.search(r"(\d+)$", key)
            units.append({"id": f"{slug}:{_lsj_id(key)}",
                          "ref": f"LSJ s.v. {lemma}" + (f" ({hom.group(1)})" if hom else ""),
                          "text": _ws(_lsj_text(e)), "links": links,
                          "lex": {"lemma": lemma, "beta": key, "headword_key": headword_key(lemma),
                                  "perseus_id": e.get("id")}})
    return {"slug": slug, "title": "A Greek-English Lexicon (Liddell-Scott-Jones)",
            "author": "H. G. Liddell, R. Scott, H. S. Jones; Perseus Digital Library",
            "source": {"path": ", ".join(os.path.basename(p) for p in paths), "format": "perseus-lexicon-tei",
                       "sha256": _sha256(sorted(paths))},
            "rights": PERSEUS_RIGHTS,
            "scheme": {"citation": "headword (Beta Code key converted to Unicode; ~hN = LSJ's homograph number)",
                       "resolution": "entry", "honesty": "exact",
                       "note": f"{cites:,} quotations carry a CTS URN, kept as links with resolved: false "
                               "until the Perseus shelf exists to resolve them."},
            "units": units}


def abbott_smith_entries(path):
    """[(lemma, strongs or '', element)]"""
    out = []
    # the real file has no TEI namespace; a namespaced copy must read the same
    for e in (x for x in ET.parse(path).getroot().iter() if x.tag.rsplit("}", 1)[-1] == "entry"):
        n = e.get("n") or ""
        lemma, _, g = n.partition("|")
        out.append((unicodedata.normalize("NFC", lemma.strip()), g.strip(), e))
    return out


def convert_abbott_smith(path, slug="abbott-smith"):
    units = []
    for lemma, g, e in abbott_smith_entries(path):
        links = []
        if re.fullmatch(r"G\d+", g):
            links.append({"kind": "lexical", "relation": "Strong's number", "target": f"strongs-greek:{g}"})
        units.append({"id": f"{slug}:{lemma.replace(' ', '_')}", "ref": f"Abbott-Smith s.v. {lemma}",
                      "text": _ws("".join(e.itertext())), "links": links,
                      "lex": {"lemma": lemma, "strongs": g, "headword_key": headword_key(lemma)}})
    return {"slug": slug, "title": "A Manual Greek Lexicon of the New Testament",
            "author": "G. Abbott-Smith (1922); TEI by translatable-exegetical-tools",
            "source": {"path": os.path.basename(path), "format": "abbott-smith-tei", "sha256": _sha256([path])},
            "rights": {"license": "Public domain",
                       "attribution": "G. Abbott-Smith, 1922; markup by translatable-exegetical-tools",
                       "source_url": "https://github.com/translatable-exegetical-tools/Abbott-Smith",
                       "note": "The repository states the lexicon and its markup are in the public domain."},
            "scheme": {"citation": "headword", "resolution": "entry", "honesty": "exact"},
            "units": units}


def convert_lewis_short(path, slug="lewis-short"):
    units, cites = [], 0
    for e in ET.parse(path).getroot().iter("entryFree"):
        key = e.get("key") or ""
        orth = e.find("orth")
        lemma = _ws("".join(orth.itertext())) if orth is not None else key
        links = _cites(e)
        cites += len(links)
        units.append({"id": f"{slug}:{key.replace(' ', '_')}", "ref": f"L&S s.v. {lemma}",
                      "text": _ws("".join(e.itertext())), "links": links,
                      "lex": {"lemma": lemma, "perseus_id": e.get("id")}})
    return {"slug": slug, "title": "A Latin Dictionary (Lewis & Short)",
            "author": "C. T. Lewis & C. Short (1879); Perseus Digital Library",
            "source": {"path": os.path.basename(path), "format": "perseus-lexicon-tei", "sha256": _sha256([path])},
            "rights": PERSEUS_RIGHTS,
            "scheme": {"citation": "headword key (Perseus's, with its homograph digit)",
                       "resolution": "entry", "honesty": "exact",
                       "note": f"{cites:,} quotations carry a CTS URN, kept as links with resolved: false."},
            "units": units}


RE_STEP_ROW = re.compile(r"^G\d{4}\t")


def step_rows(path):
    """{extended key: (lemma, translit, pos, gloss, body, relation, target_cell)}, file order."""
    out = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        if not RE_STEP_ROW.match(line):
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) < 8:
            continue
        m = re.match(r"^(\S+)\s*=\s*(.*)$", c[1].strip())
        if m:
            out[m.group(1)] = (c[3], c[4], c[5], c[6], c[7], m.group(2).strip(), c[2])
    return out


RE_GREEK_WORD = re.compile(r"[Ͱ-Ͽἀ-῿][Ͱ-Ͽἀ-῿̀-ͯ-]*")


def body_agrees(lemma, body):
    """Does a TFLSJ body open on (a spelling of) its own headword? The first
    Greek word must share its first two letters with one of the lemma's
    comma-separated forms. Loose on purpose: LSJ hyphenates stems (ἀγάπ-η)
    and spells older forms (ἀείδω for ᾄδω is flagged, and the brief text is
    used -- the safe side). Measured 2026-09-29: 131 of 9,549 bodies fail."""
    m = RE_GREEK_WORD.search(re.sub(r"<[^>]+>", " ", body or ""))
    first = headword_key(m.group(0)) if m else ""
    if not first:
        return True
    for part in re.split(r"[,;/]\s*", lemma or ""):
        k = headword_key(part)
        if not k:
            continue
        n = 0
        while n < min(len(k), len(first)) and k[n] == first[n]:
            n += 1
        if n >= min(2, len(k), len(first)):
            return True
    return False


def select_supplement(keys_lemmas, have):
    """{key: [why]} for the keys the supplement takes. keys_lemmas is
    {extended key: lemma or [lemmas]} -- TBESG and TFLSJ sometimes spell one
    headword differently, and a word counts as missing only when NEITHER
    spelling is in the shareable lexicons; have is the set of headword keys
    they hold."""
    base = lambda k: re.match(r"G\d+", k).group(0)
    per_base = Counter(base(k) for k in keys_lemmas)
    out = {}
    for k, lemma in keys_lemmas.items():
        why = []
        if int(base(k)[1:]) >= 6000:
            why.append("beyond-strongs")   # the LXX / variant vocabulary
        if per_base[base(k)] > 1:
            why.append("split")
        lemmas = [lemma] if isinstance(lemma, str) else lemma
        if not any(headword_key(x) in have for x in lemmas):
            why.append("not-in-perseus-or-abbott-smith")
        if why:
            out[k] = why
    return out


PREFERENCES = os.path.join(HERE, "..", "data", "lexicons", "step-preference-reviewed.jsonl")
CANDIDATES = os.path.join(HERE, "..", "data", "lexicons", "step-preference-candidates.jsonl")


def load_preferences(path=PREFERENCES):
    """{STEP key: "step" | "perseus"} from Adam's answers to
    docs/review/2026-09-29-step-preference.md (review.py apply)."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return {r["id"]: r["prefer"] for r in (json.loads(l) for l in f if l.strip())}


def _step_inputs(tbesg, tflsj_paths, lsj_paths, as_path):
    brief = step_rows(tbesg)
    full = {}
    for p in tflsj_paths:
        full.update(step_rows(p))
    lsj = lsj_headwords(lsj_paths)
    asm = abbott_smith_entries(as_path)
    have = set(lsj) | {headword_key(l) for l, _, _ in asm}
    keys = {k: [r[0] for r in (full.get(k), brief.get(k)) if r]
            for k in list(brief) + [k for k in full if k not in brief]}
    return brief, full, lsj, asm, have, keys


def convert_step_supplement(tbesg, tflsj_paths, lsj_paths, as_path, slug="step-greek-supplement",
                            preferences=None):
    import structure_texts as st
    brief, full, lsj, asm, have, keys = _step_inputs(tbesg, tflsj_paths, lsj_paths, as_path)
    as_by_g = defaultdict(list)
    for lemma, g, _ in asm:
        if g:
            as_by_g[g].append(f"abbott-smith:{lemma.replace(' ', '_')}")
    chosen = select_supplement(keys, have)
    # Adam's review: a `step` answer takes STEP's entry even though Perseus has the word
    prefs = load_preferences() if preferences is None else preferences
    for k, p in prefs.items():
        if p == "step" and k in keys and k not in chosen:
            chosen[k] = ["preferred-by-review"]
    units, counts = [], Counter()
    for k in keys:
        if k not in chosen:
            continue
        row = full.get(k) or brief[k]
        edition = "TFLSJ" if k in full else "TBESG"
        if k in full and k in brief and not body_agrees(full[k][0], full[k][4]):
            # the full text opens on another headword (G0001H ἆ carries ἔα's
            # body): use the brief text, which is always about this key
            row, edition = brief[k], "TBESG (the TFLSJ text opens on another headword)"
            counts["tflsj-text-set-aside"] += 1
        lemma, translit, pos, gloss, body, relation, target_cell = row
        g = st.strongs_id(re.match(r"G(\d+)", k).group(1), "greek")
        links = []
        target, parts = st._step_targets(target_cell, slug)
        for t, rel in [(target, relation)] + [(p, "a Combination of") for p in parts]:
            if not t or not rel or t == f"{slug}:{k}":
                continue
            tk = t.split(":", 1)[1]
            if t.startswith(slug + ":") and tk not in chosen:
                # a target outside the supplement points at the public Strong's entry
                num = re.match(r"G(\d+)", tk).group(1)
                t = "strongs-greek:" + st.strongs_id(num, "greek")
            links.append({"kind": "lexical", "relation": rel, "target": t})
        for t in lsj.get(headword_key(lemma), []):
            links.append({"kind": "lexical", "relation": "LSJ entry", "target": t})
        for t in as_by_g.get(g, []):
            links.append({"kind": "lexical", "relation": "Abbott-Smith entry (by Strong's number)", "target": t})
        brief_gloss = brief[k][3] if k in brief else ""
        text = " ".join(x for x in (brief_gloss or gloss, st._step_body(body)) if x)
        for w in chosen[k]:
            counts[w] += 1
        units.append({"id": f"{slug}:{k}", "ref": f"{k} {lemma}".strip() + (f" ({translit})" if translit else ""),
                      "text": text, "links": links,
                      "lex": {"lemma": lemma, "translit": translit, "pos": pos, "gloss": brief_gloss or gloss,
                              "strongs": g, "why": chosen[k],
                              "step_edition": edition}})
    return {"slug": slug, "title": "STEPBible Greek supplement: the Septuagint vocabulary, the Strong's splits, and the words the open lexicons lack",
            "author": "STEPBible.org / Tyndale House Cambridge",
            "source": {"path": ", ".join(os.path.basename(p) for p in [tbesg] + list(tflsj_paths)),
                       "format": "lexicon-tsv-subset", "sha256": _sha256([tbesg] + sorted(tflsj_paths))},
            "rights": {"license": "CC BY 4.0", "attribution": STEP_ATTRIBUTION,
                       "source_url": "https://github.com/STEPBible/STEPBible-Data",
                       "subset_of": ["tbesg-greek", "lsj-greek"], "shareable": True,
                       "note": "A selection, not the lexicon: only entries numbered G6000+, the splits of one "
                               "Strong's number, and headwords lsj-perseus and abbott-smith lack; one text "
                               "per entry. Ruled by Adam 2026-09-29. Corrections belong upstream at "
                               "github.com/STEPBible."},
            "scheme": {"citation": "Extended Strong's number (e.g. G0001G)", "resolution": "entry",
                       "honesty": "exact",
                       "note": f"{len(units):,} of {len(keys):,} STEP keys: " +
                               ", ".join(f"{n:,} {w}" for w, n in sorted(counts.items())) +
                               " (an entry can be in more than one)."},
            "units": units}


# ---------------------------------------------------------------- which STEP entries may beat Perseus
#
# STEP's TFLSJ is the same dictionary as lsj-perseus, edited by Tyndale House
# (abbreviations expanded, citations dated, scripture refs made linkable).
# Measured 2026-09-29 over the 8,331 entries both hold: the median STEP entry
# keeps 100% of the Perseus Greek, so content rarely differs. Three things
# can make STEP's entry the better one, and each is a reason on the sheet:
#
#   perseus-damaged   the matched Perseus entry carries <*> (an unreadable
#                     spot in the source); STEP's is clean
#   low-overlap       under 60% of the Perseus entry's Greek words are in
#                     STEP's: the two are probably not the same entry (a
#                     wrong homograph, or STEP filing a form under its lemma)
#   accent-lookalike  Perseus/Abbott-Smith have the word only if accents are
#                     ignored (ἁγνῶς "purely" vs ἀγνώς "unknown"), so the
#                     supplement counted it present and left STEP's out
#
# Keys the supplement already takes are not asked about. The sheet is
# docs/review/2026-09-29-step-preference.md (review.py); a `step` answer
# adds the key to the supplement as "preferred-by-review".

GREEK_WORDS = re.compile(r"[Ͱ-Ͽἀ-῿][Ͱ-Ͽἀ-῿̀-ͯ]+")
EXCERPT = 240


def _greek_set(text):
    return {headword_key(w) for w in GREEK_WORDS.findall(text)}


def _excerpt(text):
    t = _ws(text)
    return t if len(t) <= EXCERPT else t[:EXCERPT].rsplit(" ", 1)[0] + " …"


def step_preference_candidates(tbesg, tflsj_paths, lsj_paths, as_path, lsj_units=None):
    import structure_texts as st
    brief, full, lsj, asm, have, keys = _step_inputs(tbesg, tflsj_paths, lsj_paths, as_path)
    chosen = select_supplement(keys, have)
    units = lsj_units if lsj_units is not None else convert_lsj_perseus(lsj_paths)["units"]
    by_key = defaultdict(list)
    for u in units:
        by_key[u["lex"]["headword_key"]].append(u)
    exact = {accented_key(u["lex"]["lemma"]) for u in units} | {accented_key(l) for l, _, _ in asm}
    out = []
    for k in sorted(keys):
        if k in chosen:
            continue
        lemmas = keys[k]
        reasons, best, overlap = [], None, None
        if not any(accented_key(x) in exact for x in lemmas):
            reasons.append("accent-lookalike")
        step_text = st._step_body((full.get(k) or brief[k])[4])
        if k in full:
            cands = [u for x in lemmas for u in by_key.get(headword_key(x), [])]
            if cands:
                sg = _greek_set(step_text)
                best = max(cands, key=lambda u: (len(sg & _greek_set(u["text"])), u["id"]))
                pg = _greek_set(best["text"])
                overlap = round(len(sg & pg) / max(1, len(pg)), 2)
                if overlap < 0.6:
                    reasons.append("low-overlap")
                if "<*>" in best["text"]:
                    reasons.append("perseus-damaged")
        if not reasons:
            continue
        if best is None:
            cands = [u for x in lemmas for u in by_key.get(headword_key(x), [])]
            best = min(cands, key=lambda u: u["id"]) if cands else None
        out.append({"id": k, "lemma": lemmas[0], "reasons": sorted(reasons),
                    "perseus_id": best["id"] if best else None,
                    "perseus": _excerpt(best["text"]) if best else "",
                    "step": _excerpt(step_text), "overlap": overlap,
                    "suggest": "step" if reasons == ["perseus-damaged"] else None})
    rank = {"perseus-damaged": 0, "low-overlap": 1, "accent-lookalike": 2}
    out.sort(key=lambda r: (-len(r["reasons"]), min(rank[x] for x in r["reasons"]),
                            r["overlap"] if r["overlap"] is not None else 1.0, r["id"]))
    return out


def main(argv=None):
    """python3 pipeline/lexica.py --candidates [--check]
    Writes (or checks) data/lexicons/step-preference-candidates.jsonl from the
    fetched sources; review.py renders the sheet from that committed file."""
    import glob
    argv = sys.argv[1:] if argv is None else argv
    if "--candidates" not in argv:
        raise SystemExit(main.__doc__)
    d = os.path.join(HERE, "..", "data", "corpus", "lexicons")
    lsj = sorted(glob.glob(os.path.join(d, "perseus-lsj", "*.xml")))
    step = [os.path.join(d, f) for f in ("tbesg-greek.txt", "tflsj-greek-0-5624.txt", "tflsj-greek-extra.txt")]
    asp = os.path.join(d, "abbott-smith.tei.xml")
    if len(lsj) != 27 or not all(os.path.exists(p) for p in step + [asp]):
        raise SystemExit("the lexicon sources are not fetched (python3 pipeline/fetch_sources.py)")
    rows = step_preference_candidates(step[0], step[1:], lsj, asp)
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    if "--check" in argv:
        same = os.path.exists(CANDIDATES) and open(CANDIDATES, encoding="utf-8", newline="").read() == text
        print("CHECK PASSED: candidates byte-identical." if same else "CHECK FAILED: the candidates differ.")
        raise SystemExit(0 if same else 1)
    os.makedirs(os.path.dirname(CANDIDATES), exist_ok=True)
    with open(CANDIDATES + ".tmp", "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(CANDIDATES + ".tmp", CANDIDATES)
    c = Counter(x for r in rows for x in r["reasons"])
    print(f"{len(rows)} candidates -> {CANDIDATES}: " + ", ".join(f"{n} {k}" for k, n in sorted(c.items())))


if __name__ == "__main__":
    main()
